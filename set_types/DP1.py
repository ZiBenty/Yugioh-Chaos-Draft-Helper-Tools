#!/usr/bin/python3
import random

class Duelist_Pack1:
        #The sets considered to be core sets
        sets = ["DP1", "DP2", "DP03", "DP04", "DP05", "DP06", "DP07"] 

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.rare = []
                self.supers = []
                self.ultra = []

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

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.commons)
                random.shuffle(self.rare)
                random.shuffle(self.supers)
                random.shuffle(self.ultra)

        #Returns a pack of the set(STUDIA MEGLIO LA PROBABILITA' PER RENDERLA PIU' PRECISA):
        def generate_pack(self, code): 
                self.shuffle()
                pack = {}
                y = 0
                rarity = random.randint(1,9999)
                rarityslot = None
                rarityname = ""
                if rarity in range(1, 417):
                        rarityslot = self.ultra[0]
                        rarityname = "Ultra Rare"
                elif rarity in range(417, 2083):
                        rarityslot = self.supers[0]
                        rarityname = "Super Rare"
                rng = None
                if rarityslot is not None:
                        rng = range(0,3)
                else:
                        rng = range(0,4)
                for i in rng:
                        pack[self.commons[i]] = "Common"
                if rarityslot is not None:
                        pack[self.rare[0]] = "Rare"
                        pack[rarityslot] = rarityname
                else:
                        pack[self.rare[0]] = "Rare"
                return pack

