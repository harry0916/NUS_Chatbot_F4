# _*_ coding utf-8 _*_
__author__ = 'Xu Kartmann'
__date__ = '20/08/2019'

import json
from utils import *

# TODO: add google map snapshot when asked location of park


class QueryFactory:

    @logger
    def __init__(self, datafile="./data/night_safari.json", frontend="default"):
        self.data_dict = self._build_knowledge_base(datafile)
        self.lexicon = Lexicon(self.data_dict)
        self.params = None
        self.intent = None

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
    def order(self, params: dict, intent: str):
        self.params = params
        self.intent = intent

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
            if self.frontend == "default":
                return self.data_dict.get("description") + "."
            return self.card_fmt.basic_card_formatter(image_url=self.data_dict["img"],
                                                      accessibilityText="Description of night safari",
                                                      formatted_text=self.data_dict.get("description"),
                                                      card_title="Night Safari",
                                                      textToSpeech="Here is the description of night safari",
                                                      botton_title="Homepage",
                                                      botton_url=self.data_dict["url"])

        elif query_kw == "where":
            if self.frontend == "default":
                return f"Our Night Safari Area is located at {self.data_dict.get('location').get('Address')}."
            return self.card_fmt.basic_card_formatter(image_url=self.data_dict["map"],
                                                      accessibilityText="The map of night safari",
                                                      formatted_text=f"Our Night Safari Area is located at "
                                                                     f"{self.data_dict.get('location').get('Address')}",
                                                      card_title="This is our address:",
                                                      card_subtitle=self.data_dict.get('location').get('Address'),
                                                      textToSpeech=f"This is our address: "
                                                                   f"{self.data_dict.get('location').get('Address')}",
                                                      botton_title="View on google map",
                                                      botton_url=self.map_url_converter(self.data_dict.get('location').
                                                                                        get('Address')))

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
            return self.card_fmt.list_card_formatter(list_title="Check out these programmes:",
                                                     textToSpeech="Check out these programmes",
                                                     item_titles=list(self.lexicon.programm.keys()),
                                                     item_descs=[info.get("info") for info in
                                                                 self.lexicon.programm.values()],
                                                     item_img_urls=[info.get("image") for info in
                                                                    self.lexicon.programm.values()],
                                                     item_img_titles=list(self.lexicon.programm.keys()),
                                                     item_urls=[info.get("url") for info in
                                                                self.lexicon.programm.values()])
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
                           f" at {info.get('time')}." if "time" in info.keys() else "."
                elif query_kw == "where":
                    return f"The venue of {self.params.get('Event')} will be at {info.get('position')}"
                elif query_kw == "bring":
                    return f"You don't have to bring any thing, but {info.get('tips')}" if info.get('tips') \
                        else f"Sorry, we don't know about that for {self.params.get('Event')}."
                else:
                    return ""
        if myString("event") == myString(self.params.get('Event')):
            if self.frontend == "default":
                desc = '\n\n'.join(
                    tuple(f"\"{desc.get('name')}\"\n{desc.get('content')}." for desc in self.data_dict.get('event')))
                return f"Check out these events: \n{desc}"
            return self.card_fmt.list_card_formatter(list_title="Check out these events:",
                                                     textToSpeech="Check out these events",
                                                     item_titles=list(self.lexicon.event.keys()),
                                                     item_descs=[info.get("content") for info in
                                                                 self.lexicon.event.values()],
                                                     item_img_urls=[info.get("image") for info in
                                                                    self.lexicon.event.values()],
                                                     item_img_titles=list(self.lexicon.event.keys()),
                                                     item_urls=[""] * len(self.lexicon.event.keys()))
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
            if self.frontend == "default":
                desc = '\n\n'.join(
                    tuple(f"{zone.get('name')}\n{zone.get('info')}" for zone in self.data_dict.get('animals')))
                return f"Learn about these animals:\n{desc}."
            return self.card_fmt.list_card_formatter(list_title="Learn about these animals:",
                                                     textToSpeech="Learn about these animals",
                                                     item_titles=list(self.lexicon.animal.keys()),
                                                     item_descs=["Range: " + info.get('Range') for info in
                                                                 self.data_dict.get('animals')],
                                                     item_img_urls=[info.get("img") for info in
                                                                    self.lexicon.animal.values()],
                                                     item_img_titles=list(self.lexicon.animal.keys()),
                                                     item_urls=[info.get("url") for info in
                                                                self.lexicon.animal.values()])
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
            if self.frontend == "default":
                desc = '\n\n'.join(
                    tuple(f"{zone.get('name')}\n{zone.get('info')}." for zone in self.data_dict.get('zone')))
                return f"Check out these zones: \n{desc}"
            return self.card_fmt.list_card_formatter(item_titles=list(self.lexicon.zone.keys()),
                                                     item_urls=[info.get("url") for info in self.lexicon.zone.values()],
                                                     item_descs=[info.get("info") for info in self.lexicon.zone.values()],
                                                     item_img_titles=list(self.lexicon.zone.keys()),
                                                     item_img_urls=[info.get("img") for info in self.lexicon.zone.values()],
                                                     list_title="Check out these zones:",
                                                     textToSpeech="Check out these zones")
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
            if self.frontend == "default":
                desc = '\n\n'.join(
                    tuple(f"{shop.get('name')}\n{shop.get('info')}." for shop in self.data_dict.get('DiningandShop').get('gift')))
                return f"Check out these shops: \n{desc}"
            return self.card_fmt.list_card_formatter(item_titles=list(self.lexicon.shop.keys()),
                                                     item_descs=[info.get("info") for info in
                                                                 self.lexicon.shop.values()],
                                                     item_urls=[info.get("url") for info in self.lexicon.shop.values()],
                                                     item_img_titles=list(self.lexicon.shop.keys()),
                                                     item_img_urls=[info.get("img") for info in
                                                                    self.lexicon.shop.values()],
                                                     list_title="Check out these shops:",
                                                     textToSpeech="Check out these shops")
        elif myString("Restaurant") == myString(self.params.get('DineandShop')):
            if self.frontend == "default":
                desc = '\n\n'.join(
                    tuple(f"{rest.get('name')}\n{rest.get('info')}." for rest in self.data_dict.get('DiningandShop').get('Restaurant')))
                return f"Check out these restaurants: {desc}"
            return self.card_fmt.list_card_formatter(item_titles=list(self.lexicon.dine.keys()),
                                                     item_descs=[info.get("info") for info in
                                                                 self.lexicon.dine.values()],
                                                     item_urls=[info.get("url") for info in self.lexicon.dine.values()],
                                                     item_img_titles=list(self.lexicon.dine.keys()),
                                                     item_img_urls=[info.get("img") for info in
                                                                    self.lexicon.dine.values()],
                                                     list_title="Check out these restaurants:",
                                                     textToSpeech="Check out these restaurants")
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
            if self.frontend == "default":
                listing = '\n\n'.join(
                    tuple(f"\"{p.get('name')}\"\n{p.get('info').get('ticket')}." for p in self.data_dict.get('promotions')))
                return f"Check out these promotions: {listing}"
            return self.card_fmt.list_card_formatter(item_titles=list(self.lexicon.promotion.keys()),
                                                     item_descs=[info.get("info").get("ticket") for info in
                                                                 self.lexicon.promotion.values()],
                                                     item_urls=[info.get("url") for info in
                                                                self.lexicon.promotion.values()],
                                                     item_img_urls=[info.get("img") for info in
                                                                    self.lexicon.promotion.values()],
                                                     item_img_titles=list(self.lexicon.promotion.keys()),
                                                     list_title="Check out these promotions:",
                                                     textToSpeech="Check out these promotions")
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
                    return f"Time information about {self.params.get('Activities')}: \n{info.get('time')}."
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
                return f"Check out these activities:\n{descs}"
            elif self.frontend == "action":
                return self.card_fmt.list_card_formatter(list_title="Check out these activities",
                                                         textToSpeech="Check out these activities:",
                                                         item_titles=list(self.lexicon.activities.keys()),
                                                         item_descs=[info.get("content") for info in
                                                                     self.lexicon.activities.values()],
                                                         item_img_urls=[info.get("img") for info in
                                                                        self.lexicon.activities.values()],
                                                         item_img_titles=list(self.lexicon.activities.keys()),
                                                         item_urls=[info.get("url") for info in
                                                                    self.lexicon.activities.values()])
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
            if self.frontend == "default":
                desc = '\n\n'.join(
                    tuple(f"\"{show.get('name')}\"\nSchedule:{show.get('time')}." for show in self.data_dict.get('show')))
                return f"Check out these shows: {desc}"
            return self.card_fmt.list_card_formatter(list_title="Check out these shows:",
                                                     textToSpeech="Check out these shows",
                                                     item_titles=list(self.lexicon.show.keys()),
                                                     item_descs=[f"Schedule: {info.get('time')}\n"
                                                                 f"Duration:{info.get('duration')}" for info in
                                                                 self.lexicon.show.values()],
                                                     item_img_urls=[info["img"] for info in self.lexicon.show.values()],
                                                     item_img_titles=list(self.lexicon.show.keys()),
                                                     item_urls=[info["url"] for info in self.lexicon.show.values()])
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
            desc = '\n'.join(
                tuple(f"{name}: ${price.get('price')}" for name, price in self.data_dict.get('Accessibility').items()))
            return f"These accessibility facilities are available: \n{desc}."
        else:
            return ""

    @logger
    def parse(self):
        if not self.params or not self.params.get('QueryKeywords'):
            return ""
        if self.intent == "nightsafariIntentSolver":
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
            if self.params["NivigateKeyword"]:
                return self.card_fmt.basic_card_formatter(image_url=self.map_url_converter(self.params["address"]),
                                                          accessibilityText="Here is a direction from your location to the zoo.",
                                                          formatted_text="Here is a direction from your location to the zoo.",
                                                          card_title="Map result",
                                                          textToSpeech="Here is a direction from your location to the zoo.",
                                                          botton_title="View on map",
                                                          botton_url=self.map_direction_converter(self.params["address"],
                                                                                                  self.data_dict.get(
                                                                                                      'location').get(
                                                                                                      'Address')))
            return ""

    @logger
    def map_url_converter(self, address: str):
        address.replace(" ", "+")
        address.replace(",", "%2C")
        return f"https://www.google.com/maps/search/?api=1&query={address}"

    @logger
    def map_direction_converter(self, origin: str, destination: str):
        origin.replace(" ", "+")
        origin.replace(",", "%2C")
        destination.replace(" ", "+")
        destination.replace(",", "%2C")
        return f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}"

