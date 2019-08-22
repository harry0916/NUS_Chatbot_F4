# _*_ coding utf-8 _*_
__author__ = 'Xu Kartmann'
__date__ = '20/08/2019'

import json
from utils import *

# TODO: add google map snapshot when asked location of park
# TODO: replace all [""] of dict into get method right before releasing the code


"""response = {
    "messages": [
        {
            "buttons": [
                {
                    "openUrlAction": {
                        "url": "https://www.google.com/search?biw=1745&bih=915&tbm=isch&sa=1&ei=CXddXYTCH8aS9QP394iwCw&q=iss&oq=iss&gs_l=img.3..0l10.4422.4709..5008...0.0..0.39.109.3......0....1..gws-wiz-img.......35i39.qHZQ3FSOsS4&ved=0ahUKEwjE6vPMtpTkAhVGSX0KHfc7ArYQ4dUDCAY&uact=5#imgrc=GqJTyt3VS1je5M:"
                    },
                    "title": "Direction to Zoo"
                }
            ],
            "formattedText": "AoG Card Description",
            "image": {
                "url": "https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwjylbPQtpTkAhUBT30KHanvCFcQjRx6BAgBEAQ&url=https%3A%2F%2Fcosmosmagazine.com%2Fspace%2Fmicrobes-in-space-concerns-raised-about-bacteria-in-the-iss&psig=AOvVaw15xPtD6BR6LrypsgQRJpVF&ust=1566492815479868",
                "accessibilityText": "Google map snapshot"
            },
            "platform": "google",
            "subtitle": "AoG Card Subtitle",
            "title": "AoG Card Title",
            "type": "basic_card"
        }
    ]
}"""
template = {
    "payload": {
        "google": {
            "expectUserResponse": True,
            "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                            "textToSpeech": "This is a basic card example."
                        }
                    },
                    {
                        "basicCard": {
                            "title": "Title: this is a title",
                            "subtitle": "This is a subtitle",
                            "formattedText": "",
                            "image": {
                                "url": "https://cosmos-images1.imgix.net/file/spina/photo/17322/181123-ISS-full.jpg?ixlib=rails-2.1.4&auto=format&ch=Width%2CDPR&fit=max&w=1920",
                                "accessibilityText": "Google map snapshot"
                            },
                            "buttons": [
                                {
                                    "title": "image",
                                    "openUrlAction": {
                                        "url": "https://www.google.com/search?biw=1745&bih=915&tbm=isch&sa=1&ei=CXddXYTCH8aS9QP394iwCw&q=iss&oq=iss&gs_l=img.3..0l10.4422.4709..5008...0.0..0.39.109.3......0....1..gws-wiz-img.......35i39.qHZQ3FSOsS4&ved=0ahUKEwjE6vPMtpTkAhVGSX0KHfc7ArYQ4dUDCAY&uact=5#imgrc=GqJTyt3VS1je5M:"
                                    }
                                }
                            ],
                            "imageDisplayOptions": "CROPPED"
                        }
                    }
                ]
            }
        }
    }
}


class QueryFactory:

    @logger
    def __init__(self, datafile="./data/night_safari.json"):
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

    def _build_knowledge_base(self, datafile: str):
        with open(datafile, 'rb') as f:
            data_dict = json.loads(f.read())
        return data_dict['Night Safari']

    @logger
    def order(self, params: dict):
        self.params = params

    @logger
    def admission_intent(self, query_kw):
        if query_kw == "when" or self.params["TimeBoundary"]:
            if myString("open") == myString(self.params["TimeBoundary"]):
                return f"Night Safari opens at {self.data_dict['time']['Opening Hours']}."
            elif myString("close") == myString(self.params["TimeBoundary"]):
                return f"Night Safari closes at {self.data_dict['time']['Closing Hours']}."
            elif myString("last entry") == myString(self.params["TimeBoundary"]):
                return f"The last entry of Night Safari is {self.data_dict['time']['Last entry']}."
            elif myString("time slot") == myString(self.params["TimeBoundary"]):
                return f"The time slot of Night Safari is {self.data_dict['time']['Admission time slots']}."
            else:
                return f"Opening: {self.data_dict['time']['Opening Hours']}" \
                       f"; Closing: {self.data_dict['time']['Closing Hours']}" \
                       f"; Admission time slots: {self.data_dict['time']['Admission time slots']}" \
                       f"; Last entry: {self.data_dict['time']['Last entry']}."
        elif query_kw == "what":
            return self.data_dict["description"]
        elif query_kw == "where":
            return f"Our Night Safari Area is located at {self.data_dict['location']['Address']}.\n" \
                   f"Check out this park map :)"
        elif query_kw == "how much":
            for group_name, info in self.lexicon.pricegroup.items():
                if myString(group_name) == myString(self.params["Price-group"]):
                    return f"Admission rate for {group_name}: {info}. \n Beyond that, ONLINE orders enjoy " \
                           f"{self.data_dict['ticket']['Online discount']} off. " \
                           f"{self.data_dict['ticket']['tips']}"
            return "Admission rates: \n" + \
                   "\n".join(tuple([f"{group_name}: ${info}" for group_name, info in self.lexicon.pricegroup.items()]))
        elif query_kw == "bring":
            return f"Please bring your {self.data_dict['Admission rates']['bring']} is you like."

    @logger
    def programm_intent(self, query_kw):
        for prog, info in self.lexicon.programm.items():
            if myString(prog) == myString(self.params["Programm"]):
                if query_kw == "what":
                    return self.data_dict["program"]["info"] + f"check out this link to find more! {info['url']}"
                elif query_kw == "how much":
                    return f"{self.params['Programm']} cost {info['price']}"
                elif query_kw == "when":
                    return f"The length of {self.params['Programm']} is about {info['duration']}"
        if myString("programmes") == myString(self.params['Programm']):
            return f"Check out this program: \"{self.data_dict['program'][0]['name']}\".\n {self.data_dict['program'][0]['info']}."
        else:
            return ""

    @logger
    def event_intent(self, query_kw):
        for event_name, info in self.lexicon.event.items():
            if myString(event_name) == myString(self.params["Event"]):
                if query_kw == "what":
                    return f"{self.params['Event']}: {info['content']}."
                elif query_kw == "how much":
                    return f"{self.params['Event']} don't have a price tag, which means it's free!"
                elif query_kw == "when":
                    return f"{self.params['Event']} is going to be hold on {info['date']}" + \
                           " at {info['time']}." if "time" in info.keys() else "."
                elif query_kw == "where":
                    return f"The venue of {self.params['Event']} will be at {info['position']}"
                elif query_kw == "bring":
                    return f"You don't have to bring any thing, but {info['tips']}" if info['tips'] \
                        else f"Sorry, we don't know about that for {self.params['Event']}."
                else:
                    return ""
        if myString("event") == myString(self.params['Event']):
            return f"Check out this event: \"{self.data_dict['events'][0]['name']}\".\n {self.data_dict['events'][0]['content']}."
        else:
            return ""

    @logger
    def animal_intent(self, query_kw):
        for animal_name, info in self.lexicon.animal.items():
            if myString(animal_name) == myString(self.params["Animal"]):
                if self.params["animalAttribute"]:
                    return f"The {self.params['animalAttribute']} of {animal_name} is " \
                           f"{info[self.params['animalAttribute']].lower()}."
                elif query_kw == "what":
                    descs = '. '.join(tuple(desc['name'] + ': ' + desc['content'] for desc in info['info']))
                    return f"{self.params['Animal']}: {descs}."
                elif query_kw == "where":
                    for zone, info in self.lexicon.zone.items():
                        for animal_exist in list(info['Animals'].split(',')):
                            if myString(animal_name) == myString(animal_exist):
                                return f"The zone where {animal_name} lives is {zone}."
                    return f"Sorry, we don't know where the {animal_name} lives in the zoo."
                else:
                    return f"Sorry, we don't know about that for {self.params['Animal']}."
        if myString("animal") == myString(self.params['Animal']):
            desc = '. '.join(tuple(desc['name'] + ': ' + desc['content'] for desc in self.data_dict['animals'][0]['info']))
            return f"Learn about this animal: {self.data_dict['animals'][0]['name']}: {desc}."
        else:
            return ""

    @logger
    def zone_intent(self, query_kw):
        for zone_name, info in self.lexicon.zone.items():
            if myString(zone_name) == myString(self.params["Zone"]):
                if query_kw == "what":
                    return f"In {self.params['Zone']} lives {info['Animals']}. {info['info']}."
                else:
                    return f"Sorry, we don't know about that for {self.params['Zone']}."
        if myString("zone") == myString(self.params['Zone']):
            return f"Learn about this zone: {self.data_dict['zone'][0]['name']}: {self.data_dict['zone'][0]['info']}."
        else:
            return ""

    @logger
    def dine_and_shop_intent(self, query_kw):
        for rest, info in self.lexicon.dine.items():
            if myString(rest) == myString(self.params["DineandShop"]):
                if query_kw == "what":
                    return info['info'] + '.'
                elif query_kw == "when":
                    return f"The business hours of {self.params['DineandShop']} is {info['time']}."
                elif query_kw == "where":
                    return f"{self.params['DineandShop']}: located at {info['location']}."
                elif query_kw == "how much" and "Buffet" in rest:
                    desc = ', '.join(tuple(group + ': $' + price for group, price in info['price'].items()))
                    return f"The price of {self.params['DineandShop']}: {desc}."
        for shop, info in self.lexicon.shop.items():
            if myString(shop) == myString(self.params['DineandShop']):
                if query_kw == "when":
                    return f"The business hours of {self.params['DineandShop']} is {info['time']}."
                elif query_kw == "where":
                    return f"{self.params['DineandShop']} is located at {info['location']}."
                elif query_kw == "what":
                    return info['info'] + '.'
                else:
                    return f"Sorry, we don't know about that for {self.params['DineandShop']}."
        if myString("gift shop") == myString(self.params['DineandShop']):
            return f"Check out this shop: {self.data_dict['DiningandShop']['gift'][0]['name']}:" \
                   f" {self.data_dict['DiningandShop']['gift'][0]['info']}."
        elif myString("Restaurant") == myString(self.params['DineandShop']):
            return f"Check out this restaurant: {self.data_dict['DiningandShop']['Restaurant'][0]['name']}: " \
                   f"{self.data_dict['DiningandShop']['Restaurant'][0]['info']}."
        else:
            return ""

    @logger
    def promotion_intent(self, query_kw):
        for prom, info in self.lexicon.promotion.items():
            if myString(prom) == myString(self.params['Membership']):
                if query_kw == "what":
                    desc = ', '.join(k + ': ' + v for k, v in info['info'].items())
                    return f"Lobang: {self.params['Membership']}; \n" \
                           f"Valid {info['date']}; \n" \
                           f"{desc}; \n" \
                           f"Check out this link to find more! {info['url']}."
                elif query_kw == "when":
                    return f"Valid {info['date']}."
                else:
                    return f"Sorry, we don't know about that for {self.params['Membership']}."
        if myString("promotion") == myString(self.params['Promotion']):
            listing = '\n'.join(tuple(f"{name}: {info['info']['ticket']}" for name, info in self.lexicon.promotion.items()))
            return f"Check out this promotion: \n" \
                   f"{listing}."
        else:
            return ""

    @logger
    def activities_intent(self, query_kw):
        for act, info in self.lexicon.activities.items():
            if myString(act) == myString(self.params['Activities']):
                if myString(act) == myString("Keepers' Chit-Chat") and self.params["chitchat-animal"]:
                    info.update(info['chit-chat animal'][self.params["chitchat-animal"].lower()])
                    act += " " + self.params["chitchat-animal"]
                if query_kw == "what":
                    return f"{act}: {info['content']}."
                elif query_kw == "when":
                    return info['time'] + '.'
                elif query_kw == "where" and "position" in info.keys():
                    return f"The {act} happens at {info['position']}."
                elif query_kw == "how much" and 'price' in info.keys():
                    return '; \n'.join(tuple(f"{group}: ${price}" for group, price in info['price'].items())) + '.'
                else:
                    return f"Sorry, we don't know about that for {act}."
        if myString("activities") == myString(self.params['Activities']):
            return f"Check out this activity: {self.data_dict['activities'][0]['name']}: " \
                   f"{self.data_dict['activities'][0]['content']}."
        else:
            return ""

    @logger
    def show_intent(self, query_kw):
        for show, info in self.lexicon.show.items():
            if myString(show) == myString(self.params['Show']):
                if query_kw == "when":
                    return f"Here's the schedule of {self.params['Show']}: \n" \
                           f"{info['time']}. Duration of each session is around {info['duration']}."
                elif query_kw == "where":
                    return f"The {self.params['Show']} is located at {info['position']}."
                else:
                    return f"Sorry, we don't know about that for {self.params['Show']}."
        if myString("shows") == myString(self.params['Show']):
            desc = '; \n'.join(tuple(f"{show['name']} - schedule:{show['time']}" for show in self.data_dict['show']))
            return f"Check out these shows: {desc}."
        else:
            return ""

    @logger
    def access_intent(self, query_kw):
        for access, info in self.lexicon.accessibility.items():
            if myString(access) == myString(self.params['Accessibility']):
                if query_kw == "how much":
                    ret = f"The {self.params['Accessibility']} costs ${info['price']}." if info['price'] \
                        else f"The {self.params['Accessibility']} is free of charge."
                    if 'discount' in info.keys():
                        ret += info.get('discount')
                    return ret
                else:
                    return f"Sorry, we don't know about that for {self.params['Accessibility']}."
        if myString("Accessibility") == myString(self.params['Accessibility']):
            desc = '; \n'.join(tuple(f"{name}: ${price['price']}" for name, price in self.data_dict['Accessibility'].items()))
            return f"These accessibility facilities are available: {desc}."
        else:
            return ""

    @logger
    def parse(self):
        if (len(self.params["QueryKeywords"]) == 0):
            return ""
        for kw in self.kws:
            if len(self.params["QueryKeywords"]) > 1 and "what" in self.params["QueryKeywords"]:
                self.params["QueryKeywords"].remove("what")
            if myString(kw) == myString(self.params["QueryKeywords"][0]):
                for domain, method in self.domain2Method.items():
                    if self.params[domain]:
                        return method(kw)
                for subdomain, method in self.subdomain2Method.items():
                    if self.params[subdomain]:
                        return method(kw)
        return ""
