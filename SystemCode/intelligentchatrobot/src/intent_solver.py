# _*_ coding utf-8 _*_
__author__ = 'Xu Kartmann'
__date__ = '20/08/2019'

import json
from utils import *

# TODO: add google map snapshot when asked location of park
# TODO: replace all [""] of dict into get method right before releasing the code


class QueryFactory:

    @logger
    def __init__(self, datafile="../data/night_safari.json", frontend="default"):
        self.data_dict = self._build_knowledge_base(datafile)
        self.lexicon = Lexicon(self.data_dict)
        self.params = None

        self.kws = ["what", "when", "how much", "where", "bring"]
        self.subdomain2Method = {
            "chitchat-animal": self.activities_intent,
            "animalAttribute": self.animal_intent,
            "Price-group": self.admission_intent
        }
        self.domain2Method = {
            "Event": self.event_intent,
            "Animal": self.animal_intent,
            "Zone": self.zone_intent,
            "DineandShop": self.dine_and_shop_intent,
            "Programm": self.programm_intent,
            "Promotion": self.promotion_intent,
            "Activities": self.activities_intent,
            "Show": self.show_intent,
            "Accessibility": self.access_intent,
            "Admission": self.admission_intent
        }
        self.frontend = frontend
        if self.frontend == "action":
            self.card_fmt = Payload_formater()

    def _build_knowledge_base(self, datafile: str):
        with open(datafile, 'rb') as f:
            data_dict = json.loads(f.read())
        return data_dict.get('Night Safari')

    @logger
    def order(self, params: dict):
        self.params = params

    @logger
    def admission_intent(self, query_kw):
        if query_kw == "when" or self.params.get("TimeBoundary"):
            if myString("open") == myString(self.params.get("TimeBoundary")):
                return f"Night Safari opens at {self.data_dict.get('time').get('Opening Hours')}."
            elif myString("close") == myString(self.params.get("TimeBoundary")):
                return f"Night Safari closes at {self.data_dict.get('time').get('Closing Hours')}."
            elif myString("last entry") == myString(self.params.get("TimeBoundary")):
                return f"The last entry of Night Safari is {self.data_dict.get('time').get('Last entry')}."
            elif myString("time slot") == myString(self.params.get("TimeBoundary")):
                return f"The time slot of Night Safari is {self.data_dict.get('time').get('Admission time slots')}."
            else:
                return f"Opening: {self.data_dict.get('time').get('Opening Hours')}" \
                       f"; Closing: {self.data_dict.get('time').get('Closing Hours')}" \
                       f"; Admission time slots: {self.data_dict.get('time').get('Admission time slots')}" \
                       f"; Last entry: {self.data_dict.get('time').get('Last entry')}."
        elif query_kw == "what":
            return self.data_dict.get("description")
        elif query_kw == "where":
            return f"Our Night Safari Area is located at {self.data_dict.get('location').get('Address')}.\n" \
                   f"Check out this park map :)"
        elif query_kw == "how much":
            for group_name, info in self.lexicon.pricegroup.items():
                if myString(group_name) == myString(self.params.get("Price-group")):
                    return f"Admission rate for {group_name}: {info}. \n Beyond that, ONLINE orders enjoy " \
                           f"{self.data_dict.get('ticket').get('Online discount')} off. " \
                           f"{self.data_dict.get('ticket').get('tips')}"
            return "Admission rates: \n" + \
                   "\n".join(tuple([f"{group_name}: ${info}" for group_name, info in self.lexicon.pricegroup.items()]))
        elif query_kw == "bring":
            return f"Please bring your {self.data_dict.get('Admission rates').get('bring')} is you like."

    @logger
    def admission_intent_card(self, query_kw):
        if query_kw == "when" or self.params.get("TimeBoundary"):
            if myString("open") == myString(self.params.get("TimeBoundary")):
                return f"Night Safari opens at {self.data_dict.get('time').get('Opening Hours')}."
            elif myString("close") == myString(self.params.get("TimeBoundary")):
                return f"Night Safari closes at {self.data_dict.get('time').get('Closing Hours')}."
            elif myString("last entry") == myString(self.params.get("TimeBoundary")):
                return f"The last entry of Night Safari is {self.data_dict.get('time').get('Last entry')}."
            elif myString("time slot") == myString(self.params.get("TimeBoundary")):
                return f"The time slot of Night Safari is {self.data_dict.get('time').get('Admission time slots')}."
            else:
                return f"Opening: {self.data_dict.get('time').get('Opening Hours')}.\n" \
                       f"; Closing: {self.data_dict.get('time').get('Closing Hours')}.\n" \
                       f"; Admission time slots: {self.data_dict.get('time').get('Admission time slots')}.\n" \
                       f"; Last entry: {self.data_dict.get('time').get('Last entry')}."
        elif query_kw == "what":
            return self.data_dict.get("description")
        elif query_kw == "where":

            return f"Our Night Safari Area is located at {self.data_dict.get('location').get('Address')}.\n" \
                   f"Check out this park map :)"
        elif query_kw == "how much":
            for group_name, info in self.lexicon.pricegroup.items():
                if myString(group_name) == myString(self.params.get("Price-group")):
                    return f"Admission rate for {group_name}: {info}. \n Beyond that, ONLINE orders enjoy " \
                           f"{self.data_dict.get('ticket').get('Online discount')} off. " \
                           f"{self.data_dict.get('ticket').get('tips')}"
            return "Admission rates: \n" + \
                   "\n".join(tuple([f"{group_name}: ${info}" for group_name, info in self.lexicon.pricegroup.items()]))
        elif query_kw == "bring":
            return f"Please bring your {self.data_dict.get('Admission rates').get('bring')} is you like."

    @logger
    def programm_intent(self, query_kw):
        for prog, info in self.lexicon.programm.items():
            if myString(prog) == myString(self.params.get("Programm")):
                if query_kw == "what":
                    return self.data_dict.get("program").get("info") + f"check out this link to find more! {info.get('url')}"
                elif query_kw == "how much":
                    return f"{self.params.get('Programm')} cost {info.get('price')}"
                elif query_kw == "when":
                    return f"The length of {self.params.get('Programm')} is about {info.get('duration')}"
        if myString("programmes") == myString(self.params.get('Programm')):
            if self.frontend == "default":
                descs= '\n\n'.join(tuple(f"\"{program.get('name')}\"\n{program.get('info')}." for program in self.data_dict.get('program')))
                return f"Check out these programmes:\n{descs}"
            elif self.frontend == "action":
                return self.card_fmt.list_card_formatter(list_title="Check out these programmes",
                                                         textToSpeech="Check out these programmes:",
                                                         item_titles=list(self.lexicon.programm.keys()),
                                                         item_descs=[info.get("info") for info in self.lexicon.programm.values()],
                                                         item_img_urls=[info.get("image") for info in self.lexicon.programm.values()]
                                                         )
        else:
            return ""

    @logger
    def event_intent(self, query_kw):
        for event_name, info in self.lexicon.event.items():
            if myString(event_name) == myString(self.params.get("Event")):
                if query_kw == "what":
                    return f"{self.params.get('Event')}: {info.get('content')}."
                elif query_kw == "how much":
                    return f"{self.params.get('Event')} don't have a price tag, which means it's free!"
                elif query_kw == "when":
                    return f"{self.params.get('Event')} is going to be hold on {info.get('date')}" + \
                           " at {info.get('time')}." if "time" in info.keys() else "."
                elif query_kw == "where":
                    return f"The venue of {self.params.get('Event')} will be at {info.get('position')}"
                elif query_kw == "bring":
                    return f"You don't have to bring any thing, but {info.get('tips')}" if info.get('tips') \
                        else f"Sorry, we don't know about that for {self.params.get('Event')}."
                else:
                    return ""
        if myString("event") == myString(self.params.get('Event')):
            desc = '\n\n'.join(
                tuple(f"\"{desc.get('name')}\"\n{desc.get('content')}." for desc in self.data_dict.get('event')))
            return f"Check out these events: {desc}"
        else:
            return ""

    @logger
    def animal_intent(self, query_kw):
        for animal_name, info in self.lexicon.animal.items():
            if myString(animal_name) == myString(self.params.get("Animal")):
                if self.params.get("animalAttribute"):
                    return f"The {self.params.get('animalAttribute')} of {animal_name} is " \
                           f"{info.get(self.params.get('animalAttribute')).lower()}."
                elif query_kw == "what":
                    descs = '. '.join(tuple(desc.get('name') + ': ' + desc.get('content') for desc in info.get('info')))
                    return f"{self.params.get('Animal')}: {descs}."
                elif query_kw == "where":
                    for zone, info in self.lexicon.zone.items():
                        for animal_exist in list(info.get('Animals').split(',')):
                            if myString(animal_name) == myString(animal_exist):
                                return f"The zone where {animal_name} lives is {zone}."
                    return f"Sorry, we don't know where the {animal_name} lives in the zoo."
                else:
                    return f"Sorry, we don't know about that for {self.params.get('Animal')}."
        if myString("animal") == myString(self.params.get('Animal')):
            desc = desc = '\n\n'.join(
                tuple(f"{zone.get('name')}\n{zone.get('info')}." for zone in self.data_dict.get('animals')))
            return f"Learn about this animal: {self.data_dict.get('animals')[0].get('name')}: {desc}."
        else:
            return ""

    @logger
    def zone_intent(self, query_kw):
        for zone_name, info in self.lexicon.zone.items():
            if myString(zone_name) == myString(self.params.get("Zone")):
                if query_kw == "what":
                    return f"In {self.params.get('Zone')} lives {info.get('Animals')}. {info.get('info')}."
                else:
                    return f"Sorry, we don't know about that for {self.params.get('Zone')}."
        if myString("zone") == myString(self.params.get('Zone')):
            desc = '\n\n'.join(
                tuple(f"{zone.get('name')}\n{zone.get('info')}." for zone in self.data_dict.get('zone')))
            return f"Check out these zones: {desc}"
        else:
            return ""

    @logger
    def dine_and_shop_intent(self, query_kw):
        for rest, info in self.lexicon.dine.items():
            if myString(rest) == myString(self.params.get("DineandShop")):
                if query_kw == "what":
                    return info.get('info') + '.'
                elif query_kw == "when":
                    return f"The business hours of {self.params.get('DineandShop')} is {info.get('time')}."
                elif query_kw == "where":
                    return f"{self.params.get('DineandShop')}: located at {info.get('location')}."
                elif query_kw == "how much" and "Buffet" in rest:
                    desc = ', '.join(tuple(group + ': $' + price for group, price in info.get('price').items()))
                    return f"The price of {self.params.get('DineandShop')}: {desc}."
        for shop, info in self.lexicon.shop.items():
            if myString(shop) == myString(self.params.get('DineandShop')):
                if query_kw == "when":
                    return f"The business hours of {self.params.get('DineandShop')} is {info.get('time')}."
                elif query_kw == "where":
                    return f"{self.params.get('DineandShop')} is located at {info.get('location')}."
                elif query_kw == "what":
                    return info.get('info') + '.'
                else:
                    return f"Sorry, we don't know about that for {self.params.get('DineandShop')}."
        if myString("gift shop") == myString(self.params.get('DineandShop')):
            desc = '\n\n'.join(
                tuple(f"{shop.get('name')}\n{shop.get('info')}." for shop in self.data_dict.get('DiningandShop').get('gift')))
            return f"Check out these shops: {desc}"
        elif myString("Restaurant") == myString(self.params.get('DineandShop')):
            desc = '\n\n'.join(
                tuple(f"{rest.get('name')}\n{rest.get('info')}." for rest in self.data_dict.get('DiningandShop').get('Restaurant')))
            return f"Check out these restaurants: {desc}"
        else:
            return ""

    @logger
    def promotion_intent(self, query_kw):
        for prom, info in self.lexicon.promotion.items():
            if myString(prom) == myString(self.params.get('Membership')):
                if query_kw == "what":
                    desc = ', '.join(k + ': ' + v for k, v in info.get('info').items())
                    return f"Lobang: {self.params.get('Membership')}; \n" \
                           f"Valid {info.get('date')}; \n" \
                           f"{desc}; \n" \
                           f"Check out this link to find more! {info.get('url')}."
                elif query_kw == "when":
                    return f"Valid {info.get('date')}."
                else:
                    return f"Sorry, we don't know about that for {self.params.get('Membership')}."
        if myString("promotion") == myString(self.params.get('Promotion')):
            listing = '\n\n'.join(
                tuple(f"\"{p.get('name')}\"\n{p.get('info').get('ticket')}." for p in self.data_dict.get('promotions')))
            return f"Check out these promotion: {listing}"
        else:
            return ""

    @logger
    def activities_intent(self, query_kw):
        for act, info in self.lexicon.activities.items():
            if myString(act) == myString(self.params.get('Activities')):
                if myString(act) == myString("Keepers' Chit-Chat") and self.params.get("chitchat-animal"):
                    info.update(info.get('chit-chat animal').get(self.params.get("chitchat-animal").lower()))
                    act += " " + self.params.get("chitchat-animal")
                if query_kw == "what":
                    return f"{act}: {info.get('content')}."
                elif query_kw == "when":
                    return info.get('time') + '.'
                elif query_kw == "where" and "position" in info.keys():
                    return f"The {act} happens at {info.get('position')}."
                elif query_kw == "how much" and 'price' in info.keys():
                    return '; \n'.join(tuple(f"{group}: ${price}" for group, price in info.get('price').items())) + '.'
                else:
                    return f"Sorry, we don't know about that for {act}."
        if myString("activities") == myString(self.params.get('Activities')):
            if self.frontend == "default":
                descs= '\n\n'.join(
                    tuple(f"\"{act.get('name')}\"\n{act.get('content')}." for act in self.data_dict.get('activities')))
                return f"Check out these programmes:\n{descs}"
            elif self.frontend == "action":
                return self.card_fmt.list_card_formatter(list_title="Check out these activities",
                                                         textToSpeech="Check out these activities:",
                                                         item_titles=list(self.lexicon.activities.keys()),
                                                         item_descs=[info.get("content") for info in self.lexicon.activities.values()],
                                                         item_img_urls=[info.get("img") for info in self.lexicon.activities.values()],
                                                         item_img_titles=list(self.lexicon.activities.keys()),
                                                         item_urls=[info.get("url") for info in self.lexicon.activities.values()]
                                                         )
        else:
            return ""

    @logger
    def show_intent(self, query_kw):
        for show, info in self.lexicon.show.items():
            if myString(show) == myString(self.params.get('Show')):
                if query_kw == "when":
                    return f"Here's the schedule of {self.params.get('Show')}: \n" \
                           f"{info.get('time')}. Duration of each session is around {info.get('duration')}."
                elif query_kw == "where":
                    return f"The {self.params.get('Show')} is located at {info.get('position')}."
                else:
                    return f"Sorry, we don't know about that for {self.params.get('Show')}."
        if myString("shows") == myString(self.params.get('Show')):
            desc = '\n\n'.join(
                tuple(f"\"{show.get('name')}\"\nSchedule:{show.get('time')}." for show in self.data_dict.get('show')))
            return f"Check out these shows: {desc}"
        else:
            return ""

    @logger
    def access_intent(self, query_kw):
        for access, info in self.lexicon.accessibility.items():
            if myString(access) == myString(self.params.get('Accessibility')):
                if query_kw == "how much":
                    ret = f"The {self.params.get('Accessibility')} costs ${info.get('price')}." if info.get('price') \
                        else f"The {self.params.get('Accessibility')} is free of charge."
                    if 'discount' in info.keys():
                        ret += info.get('discount')
                    return ret
                else:
                    return f"Sorry, we don't know about that for {self.params.get('Accessibility')}."
        if myString("Accessibility") == myString(self.params.get('Accessibility')):
            desc = '\n\n'.join(
                tuple(f"{name}: ${price.get('price')}" for name, price in self.data_dict.get('Accessibility').items()))
            return f"These accessibility facilities are available: {desc}."
        else:
            return ""

    @logger
    def parse(self):
        if not self.params or not self.params.get('QueryKeywords'):
            return ""
        for kw in self.kws:
            if len(self.params.get("QueryKeywords")) > 1 and "what" in self.params.get("QueryKeywords"):
                self.params.get("QueryKeywords").remove("what")
            if myString(kw) == myString(self.params.get("QueryKeywords")[0]):
                for domain, method in self.domain2Method.items():
                    if self.params.get(domain):
                        ret = method(kw)
                        if isinstance(ret, str):
                            return {"fulfillmentText": method(kw)}
                        return method(kw)
                for subdomain, method in self.subdomain2Method.items():
                    if self.params.get(subdomain):
                        ret = method(kw)
                        if isinstance(ret, str):
                            return {"fulfillmentText": method(kw)}
                        return method(kw)
        return ""
