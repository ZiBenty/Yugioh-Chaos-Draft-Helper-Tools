#!/usr/bin/python3
import random

class War_Giants_round:
        #War of the Giants grossi (9 common, 6 super, 1 ultra):
        sets = ["BPW2"]

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.supers = []
                self.ultra = []

        #Adds a card of the given name to the given rarity:
        def add_card(self, rarity, cardid):
                if(rarity == "Common"):
                        self.commons.append(cardid)
                if(rarity == "Super Rare"):
                        self.supers.append(cardid)
                if(rarity == "Ultra Rare"):
                        self.ultra.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.commons)
                random.shuffle(self.supers)
                random.shuffle(self.ultra)

        #Returns a pack of the set:
        def generate_pack(self, code):
                self.shuffle()
                pack = {}     
                for i in range(0, 9):
                        pack[self.commons[i]] = "Common"
                for i in range(0, 6):
                        pack[self.supers[i]] = "Super Rare"
                pack[self.ultra[0]] = "Ultra Rare"
                return pack

