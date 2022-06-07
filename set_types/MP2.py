#!/usr/bin/python3
import random

class Mega_Pack2:
        #New Mega Packs (14 common, 1 rare, 1 super, 1 ultra, 1 secret):
        sets = ["MP20", "MP21"]

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.rare = []
                self.supers = []
                self.ultra = []
                self.secret = []

        #Adds a card of the given name to the given rarity:
        def add_card(self, rarity, cardid):
                if(rarity == "Common"):
                        self.commons.append(cardid)
                if(rarity == "Rare"):
                        self.rare.append(cardid)
                if(rarity == "Super Rare"):
                        self.supers.append(cardid)
                if(rarity == "Ultra Rare"):
                        self.ultra.append(cardid)
                if("Secret Rare" in rarity):
                        self.secret.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.commons)
                random.shuffle(self.rare)
                random.shuffle(self.supers)
                random.shuffle(self.secret)
                random.shuffle(self.ultra)

        #Returns a pack of the set:
        def generate_pack(self, code):
                self.shuffle()
                pack = {}     
                for i in range(0, 14):
                        pack[self.commons[i]] = "Common"
                pack[self.rare[0]] = "Rare"
                pack[self.supers[0]] = "Super Rare"
                pack[self.ultra[0]] = "Ultra Rare"
                pack[self.secret[0]] = "Prismatic Secret Rare"
                return pack

