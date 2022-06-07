#!/usr/bin/python3
import random
import os.path
import sys
import json
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import DBC

class Battle_Pack:
        #The Battle Packs
        #<https://github.com/adosreis/Yugioh-Pack-Opening-Simulator/wiki/Battle-Pack-1>:
        sets = ["BP01", "BP02", "BP03", "MIL1", "BPW2"]

        #Create the empty arrays:
        def __init__(self):
                self.commons = []
                self.rares = []
                self.shiny = []
                self.starfoil = []
                #per MIL1
                self.supers = []
                self.ultra = []

        #Adds a card of the given name to the given rarity:
        def add_card(self, rarity, cardid):
                if(rarity == "Common"):
                        self.commons.append(cardid)
                if(rarity == "Rare"):
                        self.rares.append(cardid)
                if(rarity == "Super Rare"):
                        self.supers.append(cardid)
                if(rarity == "Ultra Rare"):
                        self.ultra.append(cardid)
                if(rarity == "Mosaic Rare" or rarity == "Shatterfoil Rare"):
                        self.shiny.append(cardid)
                if(rarity == "Starfoil Rare"):
                        self.starfoil.append(cardid)

        #Shuffles all the rarities in one simple call:
        def shuffle(self):
                random.shuffle(self.commons)
                random.shuffle(self.rares)
                random.shuffle(self.supers)
                random.shuffle(self.ultra)
                random.shuffle(self.shiny)
                random.shuffle(self.starfoil)

        #Returns a pack of the set:
        def generate_pack(self, code):
                self.shuffle()
                pack = {}
                dec = DBC.DBdecoder()
                if code == "BP01":
                        pack[self.starfoil[0]] = "Starfoil Rare"
                        rarity = random.randint(1,100)
                        #36% probability of finding xyz
                        if rarity in range(1, 37):
                                for c in self.rares:
                                        if "XYZ Monster" in dec.DBdecode(c, "type"):
                                                pack[c] = "Rare"
                                                break
                        else:
                                for c in self.rares:
                                        if "XYZ Monster" in dec.DBdecode(c, "type"):
                                                pack[c] = "Rare"
                                                break
                        slots = [True, False, False]
                        i = 0
                        y = 0
                        for c in self.commons:
                               y += 1
                               f = open(os.path.join(sys.path[0], "structs/dictsetcodes.txt"), "r")
                               contents = f.read()
                               setcodesdictionary = json.loads(contents)
                               f.close()
                               f = open(os.path.join(sys.path[0], "sets/BP01.txt"), "r")
                               contents = f.read()
                               packCards = json.loads(contents)
                               f.close()
                               sets = setcodesdictionary[c]
                               for s in sets:
                                       if "BP01" in s and packCards[c] == "Common":
                                               setnum = int(s.split("-EN",1)[1])
                                               if (setnum >= 56 and setnum <= 110) and slots[0]:
                                                        pack[c] = "Common"
                                                        slots[0] = False
                                                        i += 1
                                                        slots[1] = True
                                               elif (setnum >= 111 and setnum <= 170) and slots[1]:
                                                        pack[c] = "Common"
                                                        slots[1] = False
                                                        i += 1
                                                        slots[2] = True
                                               elif (setnum >= 171 and setnum <= 220) and slots[2]:
                                                        pack[c] = "Common"
                                                        slots[2] = False
                                                        i += 1
                                                        break
                               if i == len(slots):
                                        break
                elif code == "MIL1":
                        rarity = random.randint(1, 9999)
                        rarityslot = None
                        rarityname = ""
                        if rarity in range(1, 833):
                                rarityslot = self.ultra[0]
                                rarityname = "Ultra Rare"
                        elif rarity in range(833, 2499):
                                rarityslot = self.supers[0]
                                rarityname = "Super Rare"
                        if rarityslot is not None:
                                pack[rarityslot] = rarityname
                                pack[self.rares[0]] = "Rare"
                        else:
                                pack[self.rares[0]] = "Rare"
                        rng = None
                        if rarityslot is not None:
                                rng = range(0, 3)
                        else:
                                rng = range(0, 4)
                        for i in rng:
                                pack[self.commons[i]] = "Common"
                elif code == "BPW2": #War of the Giants grossi (9 common, 6 super, 1 ultra)
                        for i in range(0, 9):
                               pack[self.commons[i]] = "Common"
                        for i in range(0, 6):
                               pack[self.supers[i]] = "Super Rare"
                        pack[self.ultra[0]] = "Ultra Rare"
                else: #BP02 e BP03
                        if code == "BP02":
                                pack[self.shiny[0]] = "Mosaic Rare"
                        elif code == "BP03":
                                pack[self.shiny[0]] = "Shatterfoil Rare"
                        pack[self.rares[0]] = "Rare"
                        for i in range(0, 3):
                              pack[self.commons[i]] = "Common"
                return pack
