from itertools import product
import pandas as pd
import numpy as np
import random
import time
import csv
from datetime import timedelta

# Create a function that removes multiple elements from a list_object according to a list of indices
def delete_multiple_element(list_object, indices):
    indices = sorted(indices, reverse=True)
    for index in indices:
        if index < len(list_object):
            list_object.pop(index)

# Create a function that finds the indices of all available sets on the table
def find_sets_indices(table):
	possible_sets_indices = []
	for i in range(len(table)):
		for j in range(i+1, len(table)):
			card_to_set = []
			for l in range(4):
				if table[i][l] == table[j][l]:
					card_to_set.append(table[i][l])
				else:
					card_to_set.append(3-table[i][l]-table[j][l])
			card_to_set_tuple = tuple(card_to_set)
			for k in range(j+1, len(table)):
				if table[k] == card_to_set_tuple:
					possible_sets_indices.append([i,j,k])
	return possible_sets_indices

# Create a function that returns the impact factor of a single Set on the table using the indices of the Set and the remaining available Sets in the game
def impact_factor(indices, table, list_of_remaining_sets):
	factor = 0
	set_on_table = [table[indices[i]] for i in range(0,3)]
	for set_of_cards in list_of_remaining_sets:
		if not set(set_on_table).isdisjoint(set_of_cards):
			factor += 1
	return factor

# Create a function that selects the indices of the first set which exhibits minimum impact factor 
def min_impact_indices(possible_sets_indices, table, list_of_remaining_sets):
	min_impact_factor = 120
	min_impact_indices = possible_sets_indices[0]
	for i in range(len(possible_sets_indices)):
		if impact_factor(possible_sets_indices[i], table, list_of_remaining_sets) < min_impact_factor:
			min_impact_factor = impact_factor(possible_sets_indices[i], table, list_of_remaining_sets)
			min_impact_indices = possible_sets_indices[i]
	return min_impact_indices

# Create a function which removes the impacted sets from the list of remaining sets
def remove_impacted_sets(indices, table, list_of_remaining_sets):
	set_on_table = [table[indices[i]] for i in range(0,3)]

	sets_to_be_eliminated = []

	for set_of_cards in list_of_remaining_sets:
		if not set(set_on_table).isdisjoint(set_of_cards):
			sets_to_be_eliminated.append(set_of_cards)

	for set_of_cards in sets_to_be_eliminated:
		list_of_remaining_sets.remove(set_of_cards)

	return [list_of_remaining_sets, sets_to_be_eliminated]




# Create the full deck of cards, where each card is a tuple of 4 numbers in base 3
full_deck = list(product(range(3), repeat=4))

# Create the list of all possible sets to be made from a full deck
list_of_all_sets = []
for i in range(len(full_deck)):
	for j in range(i+1, len(full_deck)):
		card_to_set = []
		for l in range(4):
			if full_deck[i][l] == full_deck[j][l]:
				card_to_set.append(full_deck[i][l])
			else:
				card_to_set.append(3-full_deck[i][l]-full_deck[j][l])
		card_to_set_tuple = tuple(card_to_set)
		set_of_three = [full_deck[i], full_deck[j], card_to_set_tuple]
		set_of_three.sort()
		if set_of_three not in list_of_all_sets:
			list_of_all_sets.append(set_of_three)



# Create a funtion that plays a single game
def play_game(selection_method = 'random_choice'):
	deck = full_deck[:]
	list_of_remaining_sets = list_of_all_sets[:]
	random.shuffle(deck)
	table = deck[:12]
	del deck[:12]
	found_sets = []
	game_data = []

	while len(find_sets_indices(table)) > 0 or len(deck) > 0:
		if len(find_sets_indices(table)) == 0:
			game_status = [len(deck), len(list_of_remaining_sets), 0, len(table)]
			game_data.append(game_status)
			table.extend(deck[:3])
			del deck[:3]
		else:
			list_possible_sets_indices = find_sets_indices(table)
			if selection_method == 'random_choice': 
				choice_indices = random.choice(list_possible_sets_indices)
			if selection_method == 'impact_factor':
				choice_indices = min_impact_indices(list_possible_sets_indices, table, list_of_remaining_sets)
			selected_set = [table[index] for index in choice_indices]
			game_status = [len(deck), len(list_of_remaining_sets), impact_factor(choice_indices, table, list_of_remaining_sets), len(table)]
			game_data.append(game_status)
			list_of_remaining_sets, sets_to_be_eliminated = remove_impacted_sets(choice_indices, table, list_of_remaining_sets)
			found_sets.append(selected_set)
			delete_multiple_element(table, choice_indices)
			if len(table) > 9 or len(deck) == 0:
				pass
			if len(table) <= 9:
				table.extend(deck[:3])
				del deck[:3]
	game_status = [len(deck),len(list_of_remaining_sets), 0, len(table)]
	game_data.append(game_status)

	return game_data, len(table)

# Create a function that plays multiple games
def play_multiple_games(num_games=1000, selection_method='random_choice'): 
	games_played = 0
	hundreds_games_played = 0
	full_data = []
	list_of_num_cards_remaining = []

	start = time.time()

	for i in range(num_games):
		data, num_cards_remaining = play_game(selection_method)
		data_with_game_number = [datum + [games_played] for datum in data]
		full_data.extend(data_with_game_number)
		list_of_num_cards_remaining.append(num_cards_remaining)

		games_played += 1

		if games_played % 100 == 0:
			hundreds_games_played += 1
			print('{games_played} games have been played!'.format(games_played=games_played))

	end = time.time()
	total_time = end - start

	print('Done!')
	print('{num_games} games were played.'.format(num_games=num_games))
	print('The time it took was the following:')
	print(timedelta(seconds=total_time))
	print('Here were the number of times the table was cleared:')
	print(list_of_num_cards_remaining.count(0))

	df = pd.DataFrame(full_data)
	df.columns = ["deck_size", "sets_remain", "impact_factor",'table_size','game_number']

	df.to_csv('full_data.csv', index=False)
	print('Full data was collected in a csv file named full_data.')


#play_multiple_games(1000, selection_method='impact_factor')




