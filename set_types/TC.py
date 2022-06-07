#!/usr/bin/python3
import random

class Toon_Chaos_Like:
        #The sets considered to be core sets:
        sets = ["TOCH", "GEIM", "ANGU", "KICO", "GRCR"]

        #Create the empty arrays:
        def __init__(self):
                self.rare = []
                self.supers = []
                self.ultra = []
                self.collc = []

        #Adds a card of the given name to the given rarity:
        def add_card(self, rarity, cardid):
                if(rarity == "Rare"):
                        self.rare.append(cardid)
                if(rarity == "Super Rare"):
                        self.supers.append(cardid)
                if(rarity == "Ultra Rare"):
                        self.ultra.append(cardid)
                if(rarity == "Collector's Rare"):
                        self.collc.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.rare)
                random.shuffle(self.supers)
                random.shuffle(self.ultra)
                random.shuffle(self.collc)

        #Returns a pack of the set(STUDIA MEGLIO LA PROBABILITA' PER RENDERLA PIU' PRECISA):
        def generate_pack(self, code): 
                self.shuffle()
                pack = {}
                rarity = random.randint(1,9999)
                rarityslot = None
                rarityname = ""
                if rarity in range(1,323):
                        rarityslot = self.collc[0]
                        rarityname = "Collector's Rare"
                elif rarity in range(323,1989):
                        rarityslot = self.ultra[0]
                        rarityname = "Ultra Rare"
                else:
                        rarityslot = self.supers[0]
                        rarityname = "Super Rare"
                for i in range(0,6):
                        pack[self.rare[i]] = "Rare"
                pack[rarityslot] = rarityname
                return pack

