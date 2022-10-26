from itertools import product
from random import shuffle, choice 
import pandas as pd


def isSET(dimension, card1, card2, card3):
		for l in range(dimension):
			if card1[l] == card2[l]:
				if card3[l] != card1[l]:
					return False
			else:
				if card3[l] == card1[l] or card3[l] == card2[l]:
					return False
		return True

class SETGame:
	def __init__(self, dimension=None, table_size=None): 
		self.dimension = dimension if dimension else 4
		self.deck = list(product(range(3), repeat=self.dimension))
		self.table = []
		self.discard = []
		self.SETpositions = []
		self.selectedposition = []
		self.table_size = 3 * table_size if table_size else 3 * self.dimension

	def shuffle(self):
		shuffle(self.deck)

	def deal(self):
		counter = 0
		while len(self.table) < self.table_size:
			self.table.append(self.deck.pop())
			counter += 1
		self.noveltyindex = len(self.table) - counter

	def findSETs(self):
		for i in range(len(self.table)):
			for j in range(i+1, len(self.table)):
				for k in range(max(j+1, self.noveltyindex), len(self.table)):
					if [i,j,k] in self.SETpositions:
						pass
					elif isSET(self.dimension, self.table[i], self.table[j], self.table[k]):
						self.SETpositions.append([i,j,k])

	def chooseSET(self):
		if self.SETpositions:
			self.selectedposition = choice(self.SETpositions)
		else:
			self.selectedposition = []

	def removeSET(self):
		SETposition = self.selectedposition
		i, j, k = SETposition

		d = {}
		for l in range(len(self.table)):
			if l < i:
				d[l] = l
			elif i < l < j:
				d[l] = l - 1
			elif j < l < k:
				d[l] = l - 2
			elif k < l:
				d[l] = l - 3
			else:
				pass

		SET = [self.table.pop(i) for i in SETposition[::-1]]

		for i, position in reversed(list(enumerate(self.SETpositions))):
			if not set(position).isdisjoint(SETposition):
				self.SETpositions.pop(i)

		for l, position in enumerate(self.SETpositions):
			new_position = [d[index] for index in position]
			self.SETpositions[l] = new_position

		self.discard.append(SET)

	def __iter__(self):
		self.shuffle()
		return self

	def __next__(self):
		picked_position = None
		if len(self.deck) == 3 ** self.dimension:
			self.deal()
			self.findSETs()
			self.chooseSET()
			
		else:
			if self.selectedposition:
				self.removeSET()
				if self.deck:
					self.deal()
				self.findSETs()
				self.chooseSET()
				
			else:
				if self.deck:
					for _ in range(3):
						new_card = self.deck.pop()
						self.table.append(new_card)
					self.findSETs()
					self.chooseSET()
					
				else:
					raise StopIteration
		len_deck = len(self.deck)
		table = tuple(self.table)
		discard = tuple(self.discard)
		positions = tuple(self.SETpositions)
		selectedposition = tuple(self.selectedposition)
		status = (len_deck, table, discard, positions, selectedposition) # return hashable data
		return status

	def to_csv(self, file_name):
		data = []
		for status in self:
			data.append(status)
		df = pd.DataFrame(data)
		df.to_csv(file_name, index=False)


def simulate(num_games=1000, dimension=None, table_size=None, file_name=None):
	full_data = []
	counter = 0
	for _ in range(num_games):
		game = SETGame(dimension, table_size)
		data = [[counter] + list(status) for status in game]
		full_data.extend(data)
		counter += 1
	df = pd.DataFrame(full_data)
	df.columns = ["game_number", "deck_size", "table", "discard", "SET_positions", "selected_position"]
	if not file_name:
		df.to_csv(str(num_games) + '.csv', index=False)
	else:
		df.to_csv(file_name, index=False)

		