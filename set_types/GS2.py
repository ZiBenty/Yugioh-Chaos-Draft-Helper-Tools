#!/usr/bin/python3
import random

class Gold_Series2:
	#The set codes for Gold Series sets:
	sets = ["PGLD", "PGL2", "PGL3"]

	#Create the empty arrays:
	def __init__(self):
		self.golds = []
		self.secret = []

	#Adds a card of the given name to the given rarity:
	def add_card(self, rarity, cardid):
		if(rarity == "Gold Rare"):
			self.golds.append(cardid)
		if("Secret" in rarity):
		        self.secret.append(cardid)

	#Shuffles all the rarities in one simple call:
	def shuffle(self):
		random.shuffle(self.golds)
		random.shuffle(self.secret)

	#Returns a pack of the set:
	def generate_pack(self, code):
		self.shuffle()
		pack = {}
		for i in range(0, 3):
			pack[self.golds[i]] = "Gold Rare"
		for i in range(0, 2):
                        pack[self.secret[i]] = "Gold Secret Rare"
		return pack
