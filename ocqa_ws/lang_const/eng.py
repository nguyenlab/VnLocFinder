__author__ = 'danilo@jaist.ac.jp'

PLACE_PREP = r"(in|at|near|around|close to|to)"
PLACE_TERMS = "place|restaurant|eat|drink|store|location|supermarket|pharmacy|drugstore|clinic"
PLACE_EXPR = r"(^| )(%s)( |$)" % PLACE_TERMS
PERSON_TERMS = "anyone|someone|person|people|professor|president"
PERSON_EXPR = r"(^| )(%s)( |$)" % PERSON_TERMS
HERE_EXPR = r"here"
STOP_POS = "DT|IN|RB|CJ|VB"
FOOD_TERMS = "food|pizza|coffee|sushi|drink|beer|sake|wine|beef|cake|milk|crepe|bread|ramen|sashimi|bento|curry|hamburguer"

REL_MAP = {
    "prep_prop": r"(?P<prop>[a-zA-Z0-9-]+) of (?P<obj>[a-zA-Z0-9-]+)",
    "prep_loc": PLACE_PREP + r" (?P<obj>[a-zA-Z0-9-]+)",
    "prep_mov": r"from (?P<orig>[a-zA-Z0-9-]+) to (?P<dest>[a-zA-Z0-9-]+)",
    "prep_orig": r"from (?P<orig>[a-zA-Z0-9-]+)",
    "term_loc": r"here"
}

RANK_MAP = {
    r"good": ("score",),
    r"bad": ("score", 10, "last"),
    r"best": ("score", 1, "first"),
    r"worst": ("score", 1, "last"),
    r"closest": ("distance", 1, "first"),
    r"close": ("distance",),
    r"any": ("",)
}

TERM_SUBST_PLACE = {
    "JAIST": "Nomi"
}

#TODO: remove this workaround, by using a thesaurus.
TERM_SUBST_TOPIC = {
    "NLP": "Natural Language Processing", 
    "DataMining": "Data Mining", 
    "food": "restaurant"
}

SEM_FEATURE = {
    "place": ["in", "near", "around", "close to", "from", "here"],
    "quant": list(RANK_MAP.keys()),
    "people": PERSON_TERMS.split("|"),
    "loc": PLACE_TERMS.split("|")
}
