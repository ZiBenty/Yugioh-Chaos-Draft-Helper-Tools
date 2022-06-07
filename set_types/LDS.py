#!/usr/bin/python3
import random

class Legenday_Duelists_Season:
        #(15 Commons, 3 Ultra):
        sets = ["LDS1", "LDS2", "DLCS"]

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.ultra = []

        #Adds a card of the given name to the given rarity:
        def add_card(self, rarity, cardid):
                if(rarity == "Common"):
                        self.commons.append(cardid)
                if(rarity == "Ultra Rare"):
                        self.ultra.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.commons)
                random.shuffle(self.ultra)

        #Returns a pack of the set:
        def generate_pack(self, code):
                self.shuffle()
                pack = {}  
                for i in range(0, 15):
                        pack[self.commons[i]] = "Common"
                for i in range(0, 3):
                        pack[self.ultra[i]] = "Ultra Rare"
                return pack

