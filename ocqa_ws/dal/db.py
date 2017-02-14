#-*- coding: utf8 -*-
__author__ = "Danilo S. Carvalho <danilo@jaist.ac.jp>"

import pymongo
from pymongo import MongoClient
from qa_model import QALink, Answer


class QAStore:
    def __init__(self):
        self.conn = MongoClient("localhost")
        self.db = self.conn["ocqa"]
        self.questions = self.db["questions"]
        self.answers = self.db["answers"]
        self.qalinks = self.db["qalinks"]
        self.answers.create_index([("uid", pymongo.ASCENDING)], unique=True)
        self.answers.create_index([("keywords", pymongo.ASCENDING)])
        self.answers.create_index([("name", pymongo.ASCENDING)])
        self.answers.create_index([("area", pymongo.ASCENDING)])

    def insert_question(self, question):
        if (not self.questions.count({"uid": question.uid})):
            self.questions.insert_one(question.to_dict())

    def update_question(self, question):
            self.questions.replace_one({"uid": question.uid}, question.to_dict())

    def get_question(self, filter_dict):
        return self.questions.find_one(filter_dict, {"_id": 0})

    def get_questions(self, filter_dict):
        return self.questions.find(filter_dict, {"_id": 0})

    def insert_answer(self, answer):
        if (not self.answers.count({"uid": answer.uid})):
            self.answers.insert_one(answer.to_dict())

    def insert_answers(self, answers):
        try:
            return self.answers.insert_many([ans.to_dict() for ans in answers], ordered=False)
        except pymongo.errors.DuplicateKeyError:
            pass

        return 0

    def update_answer(self, answer):
        if (isinstance(answer, Answer)):
            self.answers.update_one({"uid": answer.uid}, {"$set": answer.to_dict()})
        elif (isinstance(answer, dict)):
            uid = answer["uid"]
            del answer["uid"]
            self.answers.update_one({"uid": uid}, {"$set": answer})


    def exist_answer(self, answer):
        return self.answers.count({"uid": answer.uid}) != 0

    def get_answer(self, filter_dict):
        return self.answers.find_one(filter_dict, {"_id": 0})

    def get_answers(self, filter_dict):
        return self.answers.find(filter_dict, {"_id": 0})

    def insert_qalink(self, question, answer, rank):
        qalink = QALink(question, answer, rank)
        self.qalinks.insert_one(qalink.to_dict())

    def get_question_answers(self, question):
        ans_uids = [doc["answer_uid"] for doc in self.qalinks.find({"question_uid": question.uid})]

        return self.answers.find({"uid": {"$in": ans_uids}})

    def get_answer_questions(self, answer):
        q_uids = [doc["question_uid"] for doc in self.qalinks.find({"answer_uid": answer.uid})]

        return self.questions.find({"uid": {"$in": q_uids}})


class DBQuery:
    def __init__(self):
        pass


class DBRetriever:
    def __init__(self):
        pass

    def fetch(self):
        pass
