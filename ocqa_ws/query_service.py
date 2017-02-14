#-*- coding: utf8 -*-
__author__ = "Danilo S. Carvalho <danilo@jaist.ac.jp>"

import web
import json
import re
import math
import pymongo
from qa_model import Question
from qa_model import PlaceAnswer, PersonAnswer, OrganizationAnswer, OrganizationPlaceAnswer, EntType
from segmentation import QuestionExtractor
from interpretation import QuestionInterpreter
from lang_const.eng import PLACE_PREP, HERE_EXPR, STOP_POS, RANK_MAP
from dal.db import QAStore
from mock_bd import kb

IMG_HOST = "http://150.65.242.105:4080/images/"
DEF_NUM_ANSWERS = 20

urls = (
    '/qa_serv/query.*', 'Query',
    '/qa_serv/qseg.*', 'SegQuery',
    '/qa_serv/qtrain.*', 'TrainQuery',
    '/qa_serv/datadict', 'DataDict'
)
app = web.application(urls, globals())

qextr = QuestionExtractor()
qextr.load_examples()
qextr.train()

store = QAStore()


class Query:
    def GET(self):
        query = web.input(query="")["query"].replace("?","")
        question = qextr.from_string(query)

        cachefile = open("query_cache.txt", mode='a')
        cachefile.write(query + "\n")

        segmentfile = open("query_segments.txt", mode='a')
        segmentfile.write(question.to_penntbk() + "\n")

        interpretation = QuestionInterpreter.interpret(question)

        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Allow-Credentials", "true")

        if (interpretation.goal == "place"):
            return json.dumps(Query.search_places(interpretation))

        elif (interpretation.goal == "person"):
            return json.dumps(Query.search_people(interpretation))

        return json.dumps([])

        # return json.dumps([question.to_dict()])
        # return json.dumps(QuestionInterpreter.interpret(question).__dict__)


    @staticmethod
    def search_places(interpretation):
        answers = []
        condition_subquery = []
        topic_subquery = []
        keyword_subquery = []

        for prop in interpretation.properties["condition"]:
            if (prop[0] == "loc" and (prop[1] == HERE_EXPR or (re.match(PLACE_PREP, prop[1]) and prop[2] == HERE_EXPR))):
                answers.append({"name": " ".join([w[0] for w in interpretation.subject if w[1] not in STOP_POS.split("|")]), "uri": "gps://here"})
            elif (prop[0] == "loc"):
                if (not re.match(PLACE_PREP, prop[1])):
                    #condition_subquery.append({"$or": [{"area": prop[1]}, {"area": prop[1].lower()}, {"area": prop[1].title()}]})
                    #condition_subquery.append({"area": {"$regex": r"^" + prop[1] + r"$", "$options": "i"}})
                    condition_subquery.append({"area": {"$regex": r"^" + prop[1], "$options": "i"}})
                else:
                    #condition_subquery.append({"$or": [{"area": prop[2]}, {"area": prop[2].lower()}, {"area": prop[1].title()}]})
                    #condition_subquery.append({"area": {"$regex": r"^" + prop[2] + r"$", "$options": "i"}})
                    condition_subquery.append({"area": {"$regex": r"^" + prop[2], "$options": "i"}})

        # for prop in interpretation.properties["subject"]:
        #     if (prop[0] == "prop"):
        #         condition_subquery.append({"name": {"$regex": prop[2]}})

        subj_words = set([t[0].lower() for t in interpretation.subject if (t[0] not in list(RANK_MAP.keys()) and t[1] not in STOP_POS.split("|"))])
        for term in subj_words:
            topic_subquery.append({"name": {"$regex": term, "$options": "i"}})
            keyword_subquery.append({"keywords": {"$regex": term, "$options": "i"}})

        dbquery = {"$and": []}
        if (condition_subquery):
            dbquery["$and"].extend(condition_subquery)

        dbquery["$and"].append({"$or": [{"$and": topic_subquery}, {"$and": keyword_subquery}]})

        num_answers = 20
        direction = pymongo.DESCENDING
        if (interpretation.rank[0] == "score"):
            if (len(interpretation.rank) > 2):
                num_answers = interpretation.rank[1]
                direction = pymongo.DESCENDING if (interpretation.rank[2] == "first") else pymongo.ASCENDING

        answers.extend(list(store.get_answers(dbquery).sort("customerReviews.score", direction)[0:num_answers]))

        for ans in answers:
            if ("pictureURL" in ans.keys() and ans["pictureURL"]):
                if (not re.match(r"https?://.+", ans["pictureURL"])):
                    ans["pictureURL"] = IMG_HOST + "answer/" + ans["pictureURL"]
            else:
                ans["pictureURL"] = IMG_HOST + "generic_jp.gif"



        return answers

    @staticmethod
    def search_people(interpretation):
        answers = []

        people_answers = list(store.get_answers({"entType": EntType.PERSON}))

        subj_words = set([t[0].lower() for t in interpretation.subject if t[1] not in STOP_POS.split("|")])
        for person in people_answers:
            name_words = set([nw.lower() for nw in person["name"].split()])
            keywords = set([kw.lower() for kw in person["keywords"]])

            score = len(name_words.intersection(subj_words))
            for word in subj_words:
                for keyword in keywords:
                    if (re.match(word, keyword)):
                        score += 2
                    elif (re.search(word, keyword)):
                        score += 1

            answers.append((person, score))

        srtd_answers = sorted(answers, key=lambda x: x[1], reverse=True)[0:20]
        max_score = max([ans[1] for ans in srtd_answers])

        return [ans[0] for ans in srtd_answers if (ans[1] > 0 and float(max_score) / ans[1] < 2.0)]


class SegQuery:
    def GET(self):
        query = web.input(query="")["query"].replace("?","")
        question = qextr.from_string(query)

        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Allow-Credentials", "true")

        segs = {"quant": " ".join([w[0] for w in question.quantifier]),
                "topic": " ".join([w[0] for w in question.topic]),
                "cond": " ".join([w[0] for w in question.condition])}

        for field in Question.Q_FIELDS:
            qexpr = getattr(question, field)
            if ("q_expr_" in field and qexpr):
                segs["qexpr"] = " ".join([w[0] for w in qexpr])
                segs["qtype"] = field.split("_")[-1]

        return json.dumps(segs)


class TrainQuery:
    def GET(self):
        try:
            query = web.input(query="", qexpr="", quant="", topic="", cond="")["query"].replace("?", "")
            qtype = web.input(query="", qexpr="", quant="", topic="", cond="")["qtype"]
            qexpr = web.input(query="", qexpr="", quant="", topic="", cond="")["qexpr"]
            quant = web.input(query="", qexpr="", quant="", topic="", cond="")["quant"]
            topic = web.input(query="", qexpr="", quant="", topic="", cond="")["topic"]
            cond = web.input(query="", qexpr="", quant="", topic="", cond="")["cond"]

            question_sys = qextr.from_string(query)
            question_usr = Question(query)
            question_usr.set_field("q_expr_" + qtype, qexpr)
            question_usr.set_field("quantifier", quant)
            question_usr.set_field("topic", topic)
            question_usr.set_field("condition", cond)

            cachefile = open("query_train_submissions.txt", mode='a')
            cachefile.write(query.encode("utf8") + "\n")
            cachefile.write(question_usr.to_penntbk().encode("utf8") + "\n")
            cachefile.write("[S]" + question_sys.to_penntbk().encode("utf8") + "\n\n")
            cachefile.close()

            web.header("Access-Control-Allow-Origin", "*")
            web.header("Access-Control-Allow-Credentials", "true")

            return json.dumps({"usr_seg": question_usr.to_penntbk(),
                               "sys_seg": question_sys.to_penntbk()})

        except Exception as e:
            return ""



class DataDict:
    def GET(self):
        ddict = dict()
        ddict["PersonAnswer"] = PersonAnswer().to_dict()
        ddict["PlaceAnswer"] = PlaceAnswer().to_dict()
        ddict["OrganizationAnswer"] = OrganizationAnswer().to_dict()
        ddict["OrganizationPlaceAnswer"] = OrganizationPlaceAnswer().to_dict()

        return json.dumps(ddict)

if __name__ == "__main__":
    app.run()
