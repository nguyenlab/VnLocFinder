#-*- coding: utf8 -*-
__author__ = "Danilo S. Carvalho <danilo@jaist.ac.jp>"

from nltk import Tree
from nltk import word_tokenize
from pycrfsuite import ItemSequence, Trainer, Tagger

from qa_model import Question
from config import MODEL_FILE, EXAMPLES_FILE
from lang_const.eng import SEM_FEATURE


class QuestionFeatureExtractor:
    @staticmethod
    def get_features(question):
        features = []
        for i in xrange(0, len(question)):
            word_feats = dict()
            word_feats["token"] = question.tok_query[i].lower()
            word_feats["prevtoken"] = question.tok_query[i].lower()
            word_feats["nexttoken"] = question.tok_query[i].lower()
            word_feats["pos"] = question.pos[i][1]
            word_feats["prevpos"] = question.pos[i - 1][1] if (i > 0) else "-#"
            word_feats["nextpos"] = question.pos[i + 1][1] if (i < len(question) - 1) else "#-"
            word_feats["istitle"] = question.tok_query[i].istitle()
            word_feats["isdigit"] = question.tok_query[i].isdigit()
            word_feats["semtype"] = "unk"

            for typ in SEM_FEATURE.keys():
                if question.tok_query[i].lower() in SEM_FEATURE[typ]:
                    word_feats["semtype"] = typ
                    break

            features.append(word_feats)

        return features

    @staticmethod
    def get_labels(question):
        return [tok[2] for tok in question.seg_query]


class QuestionExtractor:
    def __init__(self):
        self.model_file = MODEL_FILE
        self.examples = []

    @staticmethod
    def from_tree(query, tree_str):
        tree = Tree.fromstring(tree_str)
        q = Question(query)
        pos_idx = 0

        for st in tree.subtrees(lambda stt: stt.label() != "ROOT"):
            leaves = st.leaves()
            tok_seq = word_tokenize(" ".join(leaves))
            pos_idx_prev = pos_idx

            if (len(tok_seq) == 1):
                label = st.label() + "__S"
            else:
                label = ""

            for i in xrange(0, len(tok_seq)):
                if (not label):
                    if (i == 0):
                        label = st.label() + "__B"
                    elif (i == len(tok_seq) - 1):
                        label = st.label() + "__E"
                    else:
                        label = st.label() + "__M"

                q.seg_query.append((tok_seq[i], q.pos[pos_idx][1], label))
                pos_idx += 1
                label = ""

            setattr(q, st.label().lower(), zip(tok_seq, [pos[1] for pos in q.pos[pos_idx_prev:pos_idx]]))

        return q

    def from_string(self, query):
        q = Question(query)
        self.extract(q)

        return q

    def add_example(self, query, tree_str):
        q = QuestionExtractor.from_tree(query, tree_str)
        self.examples.append(q)

    def load_examples(self):
        ifile = open(EXAMPLES_FILE)

        while True:
            query = ifile.readline().replace("?", "")
            seg_query = ifile.readline().replace("?", "")
            ifile.readline()

            if (not query):
                break
            elif (query == ""):
                continue
            else:
                self.add_example(query, seg_query)

    def train(self):
        trainer = Trainer(algorithm="lbfgs")
        for question in self.examples:
            features = QuestionFeatureExtractor.get_features(question)
            labels = QuestionFeatureExtractor.get_labels(question)

            trainer.append(ItemSequence(features), labels)

        trainer.train(self.model_file)

    def extract(self, question):
        tagger = Tagger()
        tagger.open(self.model_file)

        predict_labels = tagger.tag(QuestionFeatureExtractor.get_features(question))

        for i in xrange(0, len(predict_labels)):
            token = question.tok_query[i]
            postag = question.pos[i][1]
            label = predict_labels[i]
            question.seg_query.append((token, postag, label))
            field, border_type = label.split("__")

            if (border_type == "S" or border_type == "B"):
                setattr(question, field.lower(), [(token, postag)])
            else:
                cur_value = getattr(question, field.lower())
                cur_value.append((token, postag))
                setattr(question, field.lower(), cur_value)


