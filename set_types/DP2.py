#!/usr/bin/python3
import random

class Duelist_Pack2:
        #The sets considered to be core sets
        sets = ["DP08", "DP09", "DP10", "DP11", "DPYG", "DPKB", "DPBC",
                "DPRP", "DPDG", "LEDU", "LED2", "LED3", "LED4", "LED5",
                "LED6", "LED7", "LED8"] 

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.rare = []
                self.supers = []
                self.ultra = []
                #per DPKB
                self.ulti = []
                #per LED7 e LED8
                self.ghost = []

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
                if(rarity == "Ultimate Rare"):
                        self.ulti.append(cardid)
                if(rarity == "Ghost Rare"):
                        self.ghost.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.commons)
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
                rarityslot = None
                rarityname = ""
                if self.ulti == [] and self.ghost == []:
                         if rarity in range(1, 666):
                             rarityslot = self.ultra[0]
                             rarityname = "Ultra Rare"
                         elif rarity in range(666, 2332):
                             rarityslot = self.supers[0]
                             rarityname = "Super Rare"
                elif self.ulti != []:
                        if rarity in range(1, 325):
                                rarityslot = self.ulti[0]
                                rarityname = "Ultimate Rare"
                        if rarity in range(325, 991):
                                rarityslot = self.ultra[0]
                                rarityname = "Ultra Rare"
                        elif rarity in range(991, 2657):
                                rarityslot = self.supers[0]
                                rarityname = "Super Rare"
                elif self.ghost != []:
                        if rarity in range(1, 35):
                                rarityslot = self.ghost[0]
                                rarityname = "Ghost Rare"
                        elif rarity in range(35, 701):
                                rarityslot = self.ultra[0]
                                rarityname = "Ultra Rare"
                        elif rarity in range(701, 2367):
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

