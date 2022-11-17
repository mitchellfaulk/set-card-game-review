from bitarray import bitarray

a = bitarray('100')
b = bitarray('010')
c = bitarray('001')

lst = [a,b,c]

deck = []

for feature1 in lst:
	for feature2 in lst:
		for feature3 in lst:
			for feature4 in lst:
				card = feature1 + feature2 + feature3 + feature4
				deck.append(card)

print(len(deck))

# returns 81, which is the number of cards

def is_set(card1, card2, card3):
	return (card1 | card2 | card3) == (card1 ^ card2 ^ card3)

lst_sets = []

for card1 in deck: 
	for card2 in deck:
		if card2 == card1:
			continue
		for card3 in deck:
			if card3 == card1 or card3 == card2:
				continue
			if is_set(card1, card2, card3):
				lst_sets.append([card1, card2, card3])

print(len(lst_sets))

# returns 6480, which is 6 times the number of SETs (for a SET, the order of the items doesn't matter and there are 6 ways to order 3 cards) 



