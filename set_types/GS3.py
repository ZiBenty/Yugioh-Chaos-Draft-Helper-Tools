#!/usr/bin/python3
import random

class Gold_Series3:
        #The set codes for Gold Series sets:
        sets = ["MAGO", "MGED"]

        #Create the empty arrays:
        def __init__(self):
                self.rare = []
                self.golds = []

        #Adds a card of the given name to the given rarity:
        def add_card(self, rarity, cardid):
                if("Gold Rare" in rarity):
                        self.golds.append(cardid)
                if(rarity == "Rare"):
                        self.rare.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.golds)
                random.shuffle(self.rare)

        #Returns a pack of the set:
        def generate_pack(self, code):
                self.shuffle()
                pack = {}
                for i in range(0, 5):
                        pack[self.rare[i]] = "Rare"
                for i in range(0, 2):
                        pack[self.golds[i]] = "Premium Gold Rare"
                return pack
