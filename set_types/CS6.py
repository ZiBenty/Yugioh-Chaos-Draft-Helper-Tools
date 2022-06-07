#!/usr/bin/python3
import random

class Core_Set6:
        #The sets considered to be core sets (TO BE ADDED):
        sets = ["ETCO", "ROTD", "PHRA", "BLVO", "LIOV", "DAMA", "BODE", "BACH"] 

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.shprint = []
                self.supers = []
                self.ultra = []
                self.secret = []
                self.star = []

        #Adds a card of the given name to the given rarity:
        def add_card(self, rarity, cardid):
                if(rarity == "Common"):
                        self.commons.append(cardid)
                if(rarity == "Short Print"):
                        self.shprint.append(cardid)
                if(rarity == "Super Rare"):
                        self.supers.append(cardid)
                if(rarity == "Ultra Rare"):
                        self.ultra.append(cardid)
                if(rarity == "Secret Rare"):
                        self.secret.append(cardid)
                if(rarity == "Starlight Rare"):
                        self.star.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.commons)
                random.shuffle(self.shprint)
                random.shuffle(self.supers)
                random.shuffle(self.ultra)
                random.shuffle(self.secret)
                random.shuffle(self.star)

        #Returns a pack of the set(STUDIA MEGLIO LA PROBABILITA' PER RENDERLA PIU' PRECISA):
        def generate_pack(self, code): 
                self.shuffle()
                pack = {}
                y = 0
                rarity = random.randint(1,9999)
                rarityslot = None
                rarityname = ""
                if rarity in range(1,209):
                        rarityslot = self.star[0]
                        rarityname = "Starlight Rare"
                elif rarity in range(209,1042):
                        rarityslot = self.secret[0]
                        rarityname = "Secret Rare"
                elif rarity in range(1042,2708):
                        rarityslot = self.ultra[0]
                        rarityname = "Ultra Rare"
                else:
                        rarityslot = self.supers[0]
                        rarityname = "Super Rare"
                for i in range(0,8):
                        rarity = random.randint(1,9999)
                        if rarity in range(1,323) and self.shprint != []:
                                pack[self.shprint[y]] = "Short Print"
                                y += 1
                        else:
                                pack[self.commons[i]] = "Common"
                pack[rarityslot] = rarityname
                return pack

