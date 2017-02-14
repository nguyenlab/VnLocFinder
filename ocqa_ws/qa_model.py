#-*- coding: utf8 -*-
__author__ = "Danilo S. Carvalho <danilo@jaist.ac.jp>"

import re
import hashlib
from nltk import pos_tag, word_tokenize


class Question:
    Q_FIELDS = ["q_expr_exist",
                "q_expr_place",
                "q_expr_thing",
                "q_expr_person",
                "q_expr_quant",
                "q_expr_money",
                "q_expr_mode",
                "q_expr_bool",
                "quantifier",
                "topic",
                "condition"]

    def __init__(self, query):
        self.tok_query = word_tokenize(query)
        self.pos = pos_tag(self.tok_query)
        self.seg_query = []

        for field in Question.Q_FIELDS:
            setattr(self, field, [])

    def __len__(self):

        return len(self.tok_query)

    @property
    def query(self):
        return " ".join(self.tok_query)

    @property
    def uid(self):
        hashing = hashlib.md5()
        hashing.update(self.query)

        return hashing.hexdigest()

    def set_field(self, fieldname, value):
        tok_value = word_tokenize(value)
        setattr(self, fieldname, pos_tag(tok_value))

    def to_dict(self):
        dic = self.__dict__
        dic["uid"] = self.uid

        return dic

    def to_penntbk(self):
        root_str = u"(ROOT %s)"
        noclass_str = u"(NOCLS %s)"
        tree_list = []
        query_copy = unicode(self.query).strip()
        buffer_nocls = u""

        while (query_copy != u""):
            for field in Question.Q_FIELDS:
                if (getattr(self, field)):
                    matched = False
                    field_val = u" ".join([w[0] for w in getattr(self, field)]).strip()
                    mo = re.match(re.escape(field_val), query_copy, re.UNICODE)
                    if (mo):
                        if (buffer_nocls):
                            tree_list.append(noclass_str % buffer_nocls)
                            buffer_nocls = u""

                        query_copy = query_copy.replace(mo.group(0), u"").strip()
                        tree_list.append(u"(%s %s)" % (field.upper(), field_val))
                        matched = True



            if (not matched):
                if (len(query_copy) > 1):
                    buffer_nocls += query_copy[0]
                    query_copy = query_copy[1:]
                else:
                    if (buffer_nocls):
                        tree_list.append(noclass_str % buffer_nocls)

                    break

        return root_str % (u" ".join(tree_list))


class EntType:
    NONE = 0
    PERSON = 1
    PLACE = 2
    ORGANIZATION = 4
    VALUE = 8


class Answer(object):
    def __init__(self):
        self.name = ""
        self.entType = EntType.NONE
        self.pictureURL = ""
        self.summary = ""
        self.uri = ""
        self.keywords = []
        self.nativeName = u""

    def __eq__(self, other):
        return self.uri == other.uri

    def __hash__(self):
        return hash(self.uri)

    @property
    def uid(self):
        hashing = hashlib.md5()
        hashing.update(self.uri)

        return hashing.hexdigest()

    def to_dict(self):
        dic = dict(self.__dict__)
        dic["uid"] = self.uid
        return dic

    def from_dict(self, other):
        if (isinstance(other, dict)):
            del other["uid"]

            for field in other.keys():
                setattr(self, field, other[field])


class PersonAnswer(Answer):
    def __init__(self):
        super(PersonAnswer, self).__init__()
        self.entType = EntType.PERSON


class PlaceAnswer(Answer):
    def __init__(self):
        super(PlaceAnswer, self).__init__()
        self.address = ""
        self.area = []
        self.nativeAddress = u""
        self.gpsPosition = (0.0, 0.0)
        self.entType = EntType.PLACE


class OrganizationAnswer(Answer):
    def __init__(self):
        super(OrganizationAnswer, self).__init__()
        self.telephoneNumber = ""
        self.customerReviews = []
        self.entType = EntType.ORGANIZATION

    def to_dict(self):
        dic = dict(self.__dict__)
        dic["uid"] = self.uid
        dic["customerReviews"] = []

        for review in self.customerReviews:
            if (isinstance(review, dict)):
                dic["customerReviews"].append(review)
            else:
                dic["customerReviews"].append(review.__dict__)

        return dic


class OrganizationPlaceAnswer(PlaceAnswer, OrganizationAnswer):
    def __init__(self):
        super(OrganizationPlaceAnswer, self).__init__()
        self.entType = EntType.ORGANIZATION + EntType.PLACE




class CustomerReview:
    def __init__(self):
        self.score = 0.0
        self.comments = ""


class QALink:
    def __init__(self, question, answer, rank):
        question_uid = question.uid
        answer_uid = answer.uid
        rank = rank

    def to_dict(self):
        return self.__dict__

