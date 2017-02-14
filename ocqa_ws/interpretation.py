#-*- coding: utf8 -*-
__author__ = "Danilo S. Carvalho <danilo@jaist.ac.jp>"

import re
from nltk.stem import WordNetLemmatizer
from qa_model import Question
from lang_const.eng import REL_MAP, RANK_MAP, PLACE_EXPR, PERSON_EXPR, FOOD_TERMS
from lang_const.eng import TERM_SUBST_PLACE, TERM_SUBST_TOPIC


class QuestionInterpretation:
    def __init__(self):
        self.goal = ""
        self.rank = ""
        self.subject = ""
        self.properties = {"subject": [], "condition": []}


class QuestionInterpreter:
    goal_map = {
        "q_expr_place": "place",
        "q_expr_exist": "thing",
        "q_expr_thing": "thing",
        "q_expr_person": "person",
        "q_expr_quant": "value",
        "q_expr_money": "value",
        "q_expr_mode": "mode",
        "q_expr_bool": "bool"
    }

    rank_map = {
        r"good": RANK_MAP[r"good"],
        r"bad": RANK_MAP[r"bad"],
        r"best": RANK_MAP[r"best"],
        r"worst": RANK_MAP[r"worst"],
        r"closest": RANK_MAP[r"closest"],
        r"close": RANK_MAP[r"close"],
        r"any": RANK_MAP[r"any"]
    }

    rel_map = {
        "prep_prop": REL_MAP["prep_prop"],
        "prep_loc": REL_MAP["prep_loc"],
        "prep_mov": REL_MAP["prep_mov"],
        "prep_orig": REL_MAP["prep_orig"]
    }

    def __init__(self):
        pass

    @staticmethod
    def parse_rank(str_quant):
        rank = QuestionInterpreter.rank_map[r"any"]

        if (str_quant):
            for expr in QuestionInterpreter.rank_map.keys():
                mo = re.search(expr, str_quant, re.IGNORECASE)

                if (mo):
                    rank = QuestionInterpreter.rank_map[expr]
                    break

        return rank


    @staticmethod
    def interpret(question):
        qi = QuestionInterpretation()
        wnl = WordNetLemmatizer()

        for field in set.intersection(set(QuestionInterpreter.goal_map.keys()), Question.Q_FIELDS):
            if (getattr(question, field)):
                qi.goal = QuestionInterpreter.goal_map[field]
                break

        qi.rank = QuestionInterpreter.parse_rank(" ".join([w[0] for w in question.quantifier]))
        qi.subject = [(wnl.lemmatize(term[0]), term[1]) for term in question.topic]

        str_fields = dict()
        str_fields["subject"] = " ".join([term[0] for term in qi.subject])
        str_fields["condition"] = " ".join([term[0] for term in question.condition])

        #TODO: Remove this workaround, by using a thesaurus.
        if (re.search(PLACE_EXPR, str_fields["subject"]) or re.search(FOOD_TERMS, str_fields["subject"])):
            qi.goal = "place"
        elif (re.search(PERSON_EXPR, str_fields["subject"])):
            qi.goal = "person"

        if (qi.goal == "place"):
            for term in TERM_SUBST_PLACE.keys():
                str_fields["condition"] = re.sub(term, TERM_SUBST_PLACE[term], str_fields["condition"], flags=re.IGNORECASE)
            
            for term in TERM_SUBST_TOPIC.keys():
                for i in xrange(0, len(qi.subject)):
                    qi.subject[i] = (re.sub(term, TERM_SUBST_TOPIC[term], qi.subject[i][0], flags=re.IGNORECASE), qi.subject[i][1])

        if (qi.goal == "person"):
            for term in TERM_SUBST_TOPIC.keys():
                for i in xrange(0, len(qi.subject)):
                    qi.subject[i] = (re.sub(term, TERM_SUBST_TOPIC[term], qi.subject[i][0], flags=re.IGNORECASE), qi.subject[i][1])

        for fld in str_fields.keys():
            for rel in QuestionInterpreter.rel_map.keys():
                mo = re.search(QuestionInterpreter.rel_map[rel], str_fields[fld], re.IGNORECASE)
                if (mo):
                    prop_fields = [rel.split("_")[1]]
                    for group in mo.groups():
                        prop_fields.append(group)

                    qi.properties[fld].append(tuple(prop_fields))

        return qi
