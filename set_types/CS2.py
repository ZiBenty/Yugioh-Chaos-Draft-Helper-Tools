#!/usr/bin/python3
import random

class Core_Set2:
        #The sets considered to be core sets
        sets = ["SOD", "RDS", "FET", "TLM", "CRV", "EEN", "SOI",
		"EOJ", "POTD", "CDIP", "STON", "FOTB"] 

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.shprint = []
                self.rare = []
                self.supers = []
                self.ultra = []
                self.ulti = []
                self.secret = []

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
                if(rarity == "Secret Rare"):
                        self.secret.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.commons)
                random.shuffle(self.shprint)
                random.shuffle(self.rare)
                random.shuffle(self.supers)
                random.shuffle(self.ultra)
                random.shuffle(self.secret)
                random.shuffle(self.ulti)

        #Returns a pack of the set(STUDIA MEGLIO LA PROBABILITA' PER RENDERLA PIU' PRECISA):
        def generate_pack(self, code): 
                self.shuffle()
                pack = {}
                y = 0
                rarity = random.randint(1,9999)
                rarityslot = None
                rarityname = ""
                if rarity in range(1,323):
                        rarityslot = self.ulti[0]
                        rarityname = "Ultimate Rare"
                if rarity in range(323,646) and self.secret != []:
                        rarityslot = self.secret[0]
                        rarityname = "Secret Rare"
                elif rarity in range(646,1062):
                        rarityslot = self.ultra[0]
                        rarityname = "Ultra Rare"
                elif rarity in range(1062,2728):
                        rarityslot = self.supers[0]
                        rarityname = "Super Rare"

                rng = None
                if rarityslot is not None:
                        rng = range(0,7)
                else:
                        rng = range(0,8)
                for i in rng:
                        rarity = random.randint(1,9999)
                        if rarity in range(1,323) and self.shprint != []:
                                pack[self.shprint[y]] = "Short Print"
                                y += 1
                        else:
                                pack[self.commons[i]] = "Common"
                if rarityslot is not None:
                        pack[self.rare[0]] = "Rare"
                        pack[rarityslot] = rarityname
                else:
                        pack[self.rare[0]] = "Rare"
                return pack

