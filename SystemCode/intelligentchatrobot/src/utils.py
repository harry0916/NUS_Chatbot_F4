# _*_ coding utf-8 _*_
__author__ = 'Xu Kartmann'
__date__ = '20/08/2019'

from functools import wraps
MUTE_LOGGER = False
USE_SYNONYMS = True
from nltk.corpus import wordnet
import copy

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
        self.synonym = set([self.s] +
                           [lemma_syn_b.name() for syn_b in wordnet.synsets(self.s) for lemma_syn_b in syn_b.lemmas()])

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


class Payload_formater:

    @logger
    def __init__(self):
        self.basic_card = {
            "basicCard": {
                "title": "Title: this is a title",
                "subtitle": "This is a subtitle",
                "formattedText": "",
                "image": {
                    "url": "",
                    "accessibilityText": "Google map snapshot"
                },
                "buttons": [
                    {
                        "title": "image",
                        "openUrlAction": {
                            "url": ""
                        }
                    }
                ],
                "imageDisplayOptions": "CROPPED"
            }
        }
        self.action_template = {
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": "This is a basic card example."
                                }
                            }
                        ]
                    }
                }
            }
        }
        self.basic_card_template = copy.deepcopy(self.action_template)
        self.basic_card_template["payload"]["google"]["richResponse"]["items"].append(self.basic_card)
        self.carousel_template = copy.deepcopy(self.action_template)
        self.carousel_template["payload"]["google"]["richResponse"]["items"].append({
            "carouselBrowse": {
                "items": []
            }
        })

    @logger
    def basic_card_formatter(self, image_url: str, accessibilityText: str="image", formatted_text: str="",
                             card_title: str="Hi", card_subtitle: str="This is an empty card",
                             textToSpeech: str="This is an empty card", botton_title: str="Botton", botton_url: str=""):
        t = copy.deepcopy(self.basic_card_template)
        t["payload"]["google"]["richResponse"]["items"][1]["basicCard"]["title"] = card_title
        t["payload"]["google"]["richResponse"]["items"][1]["basicCard"]["subtitle"] = card_subtitle
        t["payload"]["google"]["richResponse"]["items"][0]["simpleResponse"]["textToSpeech"] = textToSpeech
        t["payload"]["google"]["richResponse"]["items"][1]["basicCard"]["formattedText"] = formatted_text
        t["payload"]["google"]["richResponse"]["items"][1]["basicCard"]["image"]["url"] = image_url
        t["payload"]["google"]["richResponse"]["items"][1]["basicCard"]["image"]["accessibilityText"] = accessibilityText
        t["payload"]["google"]["richResponse"]["items"][1]["basicCard"]["bottons"][0]["title"] = botton_title
        t["payload"]["google"]["richResponse"]["items"][1]["basicCard"]["bottons"][0]["openUrlAction"]["url"] = botton_url
        return t

    @logger
    def list_card_formatter(self, item_titles: list, item_descs: list, item_img_urls: list, item_img_titles: list,
                            item_urls=[], list_title: str="Check out these items",
                            textToSpeech: str = "This is an empty card",):
        assert len(item_descs) == len(item_img_titles) == len(item_img_urls) == len(item_titles) == len(item_urls), \
            f"List length must the same, but received len(item_descs)={len(item_descs)}, " \
            f"len(item_img_titles)={len(item_img_titles)}, len(item_img_urls)={len(item_img_urls)}, " \
            f"len(item_titles)={len(item_titles)}, len(item_urls)={len(item_urls)}."
        if len(item_urls) > 1:
            t = copy.deepcopy(self.carousel_template)
            for i in range(len(item_titles)):
                item = {

                    "description": item_descs[i],
                    "image": {
                        "url": item_img_urls[i],
                        "accessibilityText": item_img_titles[i]
                    },
                    "title": item_titles[i],
                    "openUrlAction": {
                        "url": item_urls[i]
                    },
                }
                t["payload"]["google"]["systemIntent"]["data"]["listSelect"]["items"].append(item)
            t["payload"]["google"]["systemIntent"]["data"]["listSelect"]["title"] = list_title
            t["payload"]["google"]["richResponse"]["items"][0]["simpleResponse"]["textToSpeech"] = textToSpeech
            return t
        else:
            return self.basic_card_formatter(item_img_urls[0], item_img_titles[0], item_descs[0], list_title, "",
                                             textToSpeech, botton_title=item_img_titles[0], botton_url=item_urls[0])
