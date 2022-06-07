#!/usr/bin/python3
import random

class Five_Ultras_Like:
        #The sets that are 5 cards of same rarity (Ultra or Secret):
        sets = ["DUSA", "DUPO", "DUOV", "MVP1", "YMP1", "GFTP", "GFP2"]

        #Create the empty arrays:
        def __init__(self):
                self.ultra = []
                self.secret = []
                self.ghost = []

        #Adds a card of the given name to the given rarity:
        def add_card(self, rarity, cardid):
                if(rarity == "Ultra Rare"):
                        self.ultra.append(cardid)
                if(rarity == "Secret Rare"):
                        self.secret.append(cardid)
                if(rarity == "Ghost Rare"):
                        self.ghost.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.ultra)
                random.shuffle(self.secret)
                random.shuffle(self.ghost)

        #Returns a pack of the set:
        def generate_pack(self, code):
                self.shuffle()
                pack = {}
                if(self.secret != []):
                        for i in range(0, 5):
                               pack[self.secret[i]] = "Secret Rare"
                elif self.ghost != []:
                        rarity = random.randint(1, 9999)
                        if rarity in range(1, 66):
                                for i in range(0, 4):
                                        pack[self.ultra[i]] = "Ultra Rare"
                                pack[self.ghost[i]] = "Ghost Rare"
                        else:
                                for i in range(0, 5):
                                        pack[self.ultra[i]] = "Ultra Rare"
                else:
                        for i in range(0, 5):
                               pack[self.ultra[i]] = "Ultra Rare"
                return pack

