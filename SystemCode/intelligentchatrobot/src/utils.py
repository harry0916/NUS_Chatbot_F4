# _*_ coding utf-8 _*_
__author__ = 'Xu Kartmann'
__date__ = '20/08/2019'

from functools import wraps
MUTE_LOGGER = False
USE_SYNONYMS = True
from nltk.corpus import wordnet


def logger(f):
    @wraps(f)
    def func(*args, **kwargs):
        if not MUTE_LOGGER:
            print("=" * 20)
            print(f"{func.__name__}({args}, {kwargs.items()}) is called.")
        res = f(*args, **kwargs)
        if not MUTE_LOGGER:
            print(f"{func.__name__} output: {res}")
        return res
    return func


class Lexicon:

    @logger
    def __init__(self, data_file: dict):
        self.base = data_file
        self.animal = self._animal_lexicon()
        self.chitchat = self._chitchat_animal_lexicon()
        self.event = self._event_lexicon()
        self.activities = self._activities_lexicon()
        self.zone = self._zone_lexicon()
        self.show = self._show_lexicon()
        self.dine, self.shop = self._dineandshop_lexicon()
        self.pricegroup = self._pricegroup_lexicon()
        self.programm = self._programm_lexicon()
        self.promotion = self._promotion_lexicon()
        self.accessibility = self._accessibility_lexicon()

    @logger
    def _animal_lexicon(self):
        return {
            animal["name"].lower(): {k: v for k, v in animal.items() if k != "name"}
            for animal in self.base["animals"]
        }

    @logger
    def _chitchat_animal_lexicon(self):
        return {
            act["name"].lower().split("Keepers' Chit-Chat ")[-1]: {k: v for k, v in act.items() if k != "name"}
            for act in self.base["activities"]
        }

    @logger
    def _zone_lexicon(self):
        return {
            zone["name"].lower(): {k: v for k, v in zone.items() if k != "name"}
            for zone in self.base["zone"]
        }

    @logger
    def _activities_lexicon(self):
        return {
            act["name"].lower(): {k: v for k, v in act.items() if k != "name"}
            for act in self.base["activities"]
        }

    @logger
    def _event_lexicon(self):
        return {
            event["name"].lower(): {k: v for k, v in event.items() if k != "name"}
            for event in self.base["events"]
        }

    @logger
    def _show_lexicon(self):
        return {
            show["name"].lower(): {k: v for k, v in show.items() if k != "name"}
            for show in self.base["show"]
        }

    @logger
    def _dineandshop_lexicon(self):
        return {
            dine["name"].lower(): {k: v for k, v in dine.items() if k != "name"}
            for dine in self.base["DiningandShop"]["Restaurant"]
        }, {
            shop["name"].lower(): {k: v for k, v in shop.items() if k != "name"}
            for shop in self.base["DiningandShop"]["gift"]
        }

    @logger
    def _pricegroup_lexicon(self):
        return {
            k.lower(): v
            for k, v in list(self.base["ticket"]["Admission ticket prices"].items()) +
                        list(self.base["Admission rates"]["price"].items())
        }

    @logger
    def _promotion_lexicon(self):
        return {
            promotion["name"].lower(): {k: v for k, v in promotion.items() if k != "name"}
            for promotion in self.base["promotions"]
        }

    @logger
    def _programm_lexicon(self):
        return {
            prog["name"].lower(): {k: v for k, v in prog.items() if k != "name"}
            for prog in self.base["program"]
        }

    @logger
    def _accessibility_lexicon(self):
        return self.base['Accessibility']

class myString:
    def __init__(self, s: str):
        self.s = s.lower()
        if " " in self.s:
            self.s.replace(" ", "_")
        self.synonym = set([lemma_syn_b.name() for syn_b in wordnet.synsets(self.s)
                            for lemma_syn_b in syn_b.lemmas()] + [self.s])

    @logger
    def __eq__(self, other):
        if not self.s and not other.s:
            return True

        # only use ambiguous matching when both string are single words
        if USE_SYNONYMS:
            return self.s in other.synonym or other.s in self.synonym
        else:
            return self.s == other.s

    def __repr__(self):
        return self.s
