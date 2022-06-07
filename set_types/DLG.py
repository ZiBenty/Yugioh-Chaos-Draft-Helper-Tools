#!/usr/bin/python3
import random

class Dark_Legends:
        sets = ["DLG1"] 

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.rare = []
                self.supers = []
                self.ultra = []
                #solo in promo
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
                if(rarity == "Secret Rare"):
                        self.secret.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.commons)
                random.shuffle(self.rare)
                random.shuffle(self.supers)
                random.shuffle(self.ultra)
                random.shuffle(self.secret)

        #Returns a pack of the set(STUDIA MEGLIO LA PROBABILITA' PER RENDERLA PIU' PRECISA):
        def generate_pack(self, code): 
                self.shuffle()
                pack = {}
                rarity = random.randint(1,9999)
                rarityslots = random.randint(1, 2)
                rarityind = 0
                for i in range(0, 12):
                        if rarity in range(1, 833) and rarityslots > 0:
                                pack[self.ultra[rarityind]] = "Ultra Rare"
                                rarityslots -= 1
                                rarityind += 1
                        elif rarity in range(833, 2499) and rarityslots > 0:
                                pack[self.supers[rarityind]] = "Super Rare"
                                rarityslots -= 1
                                rarityind += 1
                        elif rarityslots > 0:
                                pack[self.rare[rarityind]] = "Rare"
                                rarityslots -= 1
                                rarityind += 1
                        else:
                                pack[self.commons[i]] = "Common"
                return pack

