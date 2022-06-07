#!/usr/bin/python3
import random

class Star_Pack:
        #Star Pack sets (2 commons, 1 starfoil)
        sets = ["SP13", "SP14" ,"SP15", "SP17", "SP18"]

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.starfoil = []

        #Adds a card of the given name to the given rarity:
        def add_card(self, rarity, cardid):
                if(rarity == "Common"):
                        self.commons.append(cardid)
                if(rarity == "Starfoil Rare" or rarity == "Shatterfoil Rare"):
                        self.starfoil.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.commons)
                random.shuffle(self.starfoil)

        #Returns a pack of the set:
        def generate_pack(self, code):
                self.shuffle()
                pack = {}
                if code == "SP17":
                        pack[self.starfoil[0]] = "Shatterfoil Rare"
                else:
                        pack[self.starfoil[0]] = "Starfoil Rare"
                for i in range(0,2):
                        pack[self.commons[i]] = "Common"
                return pack

