#!/usr/bin/python3
import random

class Gold_Series1:
	#The set codes for Gold Series sets:
	sets = ["GLD1", "GLD2", "GLD3", "GLD4", "GLD5"]

	#Create the empty arrays:
	def __init__(self):
		self.commons = []
		self.golds = []
		#per GLD5
		self.ghosts = []

	#Adds a card of the given name to the given rarity:
	def add_card(self, rarity, cardid):
		if(rarity == "Common"):
			self.commons.append(cardid)
		if(rarity == "Gold Rare"):
			self.golds.append(cardid)
		if("Ghost" in rarity):
		        self.ghosts.append(cardid)

	#Shuffles all the rarities in one simple call:
	def shuffle(self):
		random.shuffle(self.commons)
		random.shuffle(self.golds)
		random.shuffle(self.ghosts)

	#Returns a pack of the set:
	def generate_pack(self, code):
		self.shuffle()
		pack = {}
		for i in range(0, 22):
			pack[self.commons[i]] = "Common"
		if(self.ghosts != []):
			for i in range(0, 2):
				pack[self.golds[i]] = "Gold Rare"
			pack[self.ghosts[0]] = "Ghost/Gold Rare"
		else:
			for i in range(0, 3):
			    pack[self.golds[i]] = "Gold Rare"
		return pack
