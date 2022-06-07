#!/usr/bin/python3
import random
import os.path
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import DBC

class Reprint_Pack1:
        #The reprint sets with set number of type cards (3 traps, 3 spells, 6 monsters):
        sets = ["DB1", "DB2", "DR1", "DR2", "DR03", "DR04"] 

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.rare = []
                self.supers = []
                self.ultra = []
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
                packlayout = ["Trap", "Trap", "Trap", "Spell", "Spell", "Spell",
                              "Monster", "Monster", "Monster", "Monster", "Monster", "Monster"]
                rarityslots = random.randint(1, 2)
                commonind = 0
                rarityind = 0
                blacklist = []
                dec = DBC.DBdecoder()
                for i in range(0, 12):
                        rarity = random.randint(1,9999)
                        rslot = random.randint(1,100)
                        if rslot in range(1,20) and rarity in range(1, 833) and rarityslots > 0:
                                for c in self.ultra:
                                      if packlayout[i] in dec.DBdecode(c, "type") and c not in blacklist:
                                              pack[c] = "Ultra Rare"
                                              blacklist.append(c)
                                              rarityslots -= 1
                                              rarityind += 1
                                              break
                        elif rslot in range(1,20) and rarity in range(833, 2499) and rarityslots > 0:
                                for c in self.supers:
                                      if packlayout[i] in dec.DBdecode(c, "type") and c not in blacklist:
                                              pack[c] = "Super Rare"
                                              blacklist.append(c)
                                              rarityslots -= 1
                                              rarityind += 1
                                              break
                        elif (rslot in range(1,20) or i in range(10,12)) and rarityslots > 0:
                                for c in self.rare:
                                      if packlayout[i] in dec.DBdecode(c, "type") and c not in blacklist:
                                              pack[c] = "Rare"
                                              blacklist.append(c)
                                              rarityslots -= 1
                                              rarityind += 1
                                              break
                        else:
                                for c in self.commons:
                                      if packlayout[i] in dec.DBdecode(c, "type") and c not in blacklist:
                                              pack[c] = "Common"
                                              blacklist.append(c)
                                              commonind += 1
                                              break
                return pack

