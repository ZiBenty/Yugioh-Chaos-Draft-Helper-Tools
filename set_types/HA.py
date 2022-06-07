#!/usr/bin/python3
import random

class Hidden_Arsenal_Like:
        #The sets that are considered Hidden Arsenal like (4 supers, 1 secret):
        sets = ["HA01", "HA02", "HA03", "HA04", "HA05", "HA06", "HA07", "NUMH",
                "DRLG", "THSF", "WSUP", "DRL2", "FUEN", "SPWA", "DASA", "SHVA",
                "HISU", "INCH", "FIGA", "MYFI", "SESL", "PEVO", "NUMH", "DRLG",
                "DRL2", "DRL3", "BLLR", "BLRR", "BLHR", "BLAR", "BROL", "PP01",
                "PP02", "DESO"]

        #Create the empty arrays:
        def __init__(self):
                self.supers = []
                self.secret = []
                #per PEVO e DRLG3 E BL
                self.ultra = []
                #per BLAR e BROL
                self.star = []
                #10000 DRAGON
                self.shiny = []

        #Adds a card of the given name to the given rarity:
        def add_card(self, rarity, cardid):
                if(rarity == "Super Rare"):
                        self.supers.append(cardid)
                if(rarity == "Ultra Rare"):
                        self.ultra.append(cardid)
                if("Secret Rare" in rarity and "10000" not in rarity):
                        self.secret.append(cardid)
                if(rarity == "Starlight Rare"):
                        self.star.append(cardid)
                if("10000" in rarity):
                        self.shiny.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.supers)
                random.shuffle(self.secret)
                random.shuffle(self.ultra)
                random.shuffle(self.star)

        #Returns a pack of the set:
        def generate_pack(self, code):
                self.shuffle()
                pack = {}
                #PEVO
                if(self.ultra != [] and self.secret == []):
                    for i in range(0, 3):
                        pack[self.supers[i]] = "Super Rare"
                    for i in range(0, 2):
                        pack[self.ultra[i]] = "Ultra Rare"
                #Nuovi DRLG e BL
                elif(self.ultra != [] and self.supers == []):
                        rarity = random.randint(1, 9999)
                        rarityslot = None
                        rarityname = ""
                        #BLAR
                        if(self.shiny != []):
                                if rarity in range(1, 138):
                                        rarityslot = self.shiny[0]
                                        rarityname = "10000 Secret Rare"
                                elif rarity in range(138, 554):
                                        rarityslot = self.star[0]
                                        rarityname = "Starlight Rare"
                                if rarityslot is not None:
                                        for i in range(0, 3):
                                            pack[self.ultra[i]] = "Ultra Rare"
                                        pack[rarityslot] = rarityname
                                else:
                                        for i in range(0, 4):
                                            pack[self.ultra[i]] = "Ultra Rare"
                                pack[self.secret[0]] = "Secret Rare"
                        #BROL
                        elif(self.star != []):
                                if rarity in range(1, 416):
                                        rarityslot = self.star[0]
                                        rarityname = "Starlight Rare"
                                if rarityslot is not None:
                                        for i in range(0, 3):
                                            pack[self.ultra[i]] = "Ultra Rare"
                                        pack[rarityslot] = rarityname
                                else:
                                        for i in range(0, 4):
                                            pack[self.ultra[i]] = "Ultra Rare"
                                pack[self.secret[0]] = "Secret Rare"
                        else:
                                for i in range(0, 4):
                                    pack[self.ultra[i]] = "Ultra Rare"
                                pack[self.secret[0]] = "Secret Rare"
                else:
                        for i in range(0, 4):
                                pack[self.supers[i]] = "Super Rare"
                        pack[self.secret[0]] = "Secret Rare"
                return pack

