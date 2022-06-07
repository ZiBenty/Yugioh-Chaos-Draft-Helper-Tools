#!/usr/bin/python3
import random

class OTS_Like:
        #The sets considered to be core sets
        sets = ["TP1", "TP2", "TP3", "TP4", "TP5", "TP6", "TP7", "TP8",
                "CP01", "CP02", "CP03", "CP04", "CP05", "CP06", "CP07", "CP08",
                "TU01", "TU02", "TU03", "TU04", "TU05", "TU06", "TU07", "TU08",
                "AP01", "AP02", "AP03", "AP04", "AP05", "AP06", "AP07", "AP08",
                "OP01", "OP02", "OP03", "OP04", "OP05", "OP06", "OP07", "OP08",
                "OP09", "OP10", "OP11", "OP12", "OP13", "OP14", "OP15", "OP16"] 

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.shprint = []
                self.rare = []
                self.supers = []
                self.ultra = []
                self.ulti = []

        #Adds a card of the given name to the given rarity:
        def add_card(self, rarity, cardid):
                if(rarity == "Common"):
                        self.commons.append(cardid)
                if(rarity == "Short Print"):
                        self.shprint.append(cardid)
                if(rarity == "Rare"):
                        self.rare.append(cardid)
                if(rarity == "Super Rare"):
                        self.supers.append(cardid)
                if(rarity == "Ultra Rare"):
                        self.ultra.append(cardid)
                if(rarity == "Ultimate Rare"):
                        self.ulti.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.commons)
                random.shuffle(self.shprint)
                random.shuffle(self.rare)
                random.shuffle(self.supers)
                random.shuffle(self.ultra)
                random.shuffle(self.ulti)

        #Returns a pack of the set(STUDIA MEGLIO LA PROBABILITA' PER RENDERLA PIU' PRECISA):
        def generate_pack(self, code): 
                self.shuffle()
                pack = {}
                y = 0
                rarity = random.randint(1,9999)
                com = 0
                if "CP" in code or "TP" in code: #champion and tournament pack
                        if rarity in range(0, 209):
                                pack[self.ultra[0]] = "Ultra Rare"
                        elif rarity in range(209, 1042):
                                pack[self.supers[0]] = "Super Rare"
                        elif rarity in range(1042, 4375):
                                pack[self.rare[0]] = "Rare"
                        else:
                                pack[self.commons[0]] = "Common"
                                com += 1
                elif "TU" in code: #turbo packs
                        if rarity in range(1,323):
                                pack[self.ulti[0]] = "Ultimate Rare"
                        elif rarity in range(323, 646):
                                pack[self.ultra[0]] = "Ultra Rare"
                        elif rarity in range(646, 1479):
                                pack[self.supers[0]] = "Super Rare"
                        else:
                                pack[self.rare[0]] = "Rare"
                else: #ots and astral packs
                        if rarity in range(1,556):
                                pack[self.ulti[0]] = "Ultimate Rare"
                        else:
                                pack[self.supers[0]] = "Super Rare"
                for i in range(0,2):
                        rarity = random.randint(1,9999)
                        if rarity in range(1,323) and self.shprint != []:
                                pack[self.shprint[y]] = "Short Print"
                                y += 1
                        else:
                                pack[self.commons[i+com]] = "Common"
                return pack

