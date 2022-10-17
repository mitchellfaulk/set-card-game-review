from itertools import product
import pandas as pd
import random
import time
import csv
from datetime import timedelta

full_deck = list(product(range(3), repeat=4))

def list_all_sets():
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
	return list_of_all_sets

list_of_all_sets = list_all_sets()

def find_sets_indices(table):
	indices = []

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
					indices.append([i,j,k])

	return indices

def impact_factor(indices, table, list_of_remaining_sets):
	factor = 0
	set_on_table = [table[indices[i]] for i in range(0,3)]

	for set_of_cards in list_of_remaining_sets:
		if not set(set_on_table).isdisjoint(set_of_cards):
			factor += 1

	return factor

def min_impact_indices(possible_sets_indices, table, list_of_remaining_sets):
	min_impact_factor = 120
	min_impact_indices = possible_sets_indices[0]

	for i in range(len(possible_sets_indices)):
		if impact_factor(possible_sets_indices[i], table, list_of_remaining_sets) < min_impact_factor:
			min_impact_factor = impact_factor(possible_sets_indices[i], table, list_of_remaining_sets)
			min_impact_indices = possible_sets_indices[i]

	return min_impact_indices

def max_impact_indices(possible_sets_indices, table, list_of_remaining_sets):
	max_impact_factor = -1
	max_impact_indices = possible_sets_indices[0]

	for i in range(len(possible_sets_indices)):
		if impact_factor(possible_sets_indices[i], table, list_of_remaining_sets) > max_impact_factor:
			max_impact_factor = impact_factor(possible_sets_indices[i], table, list_of_remaining_sets)
			max_impact_indices = possible_sets_indices[i]

	return max_impact_indices

def all_min_impact_indices(possible_sets_indices, table, list_of_remaining_sets):
	min_impact_factor = 120

	for i in range(len(possible_sets_indices)):
		if impact_factor(possible_sets_indices[i], table, list_of_remaining_sets) < min_impact_factor:
			min_impact_factor = impact_factor(possible_sets_indices[i], table, list_of_remaining_sets)

	all_min_impact_indices = []

	for indices in possible_sets_indices:
		if impact_factor(indices, table, list_of_remaining_sets) == min_impact_factor:
			all_min_impact_indices.append(indices)

	return all_min_impact_indices

def all_max_impact_indices(possible_sets_indices, table, list_of_remaining_sets):
	max_impact_factor = -1

	for i in range(len(possible_sets_indices)):
		if impact_factor(possible_sets_indices[i], table, list_of_remaining_sets) > max_impact_factor:
			max_impact_factor = impact_factor(possible_sets_indices[i], table, list_of_remaining_sets)

	all_max_impact_indices = []

	for indices in possible_sets_indices:
		if impact_factor(indices, table, list_of_remaining_sets) == max_impact_factor:
			all_max_impact_indices.append(indices)

	return all_max_impact_indices

def remove_impacted_sets(indices, table, list_of_remaining_sets):
	set_on_table = [table[indices[i]] for i in range(0,3)]
	sets_to_be_eliminated = []

	for set_of_cards in list_of_remaining_sets:
		if not set(set_on_table).isdisjoint(set_of_cards):
			sets_to_be_eliminated.append(set_of_cards)

	for set_of_cards in sets_to_be_eliminated:
		list_of_remaining_sets.remove(set_of_cards)

	return [list_of_remaining_sets, sets_to_be_eliminated]

def impact_factor_set(set_of_three, list_of_remaining_sets):
	factor = 0

	for set_of_cards in list_of_remaining_sets:
		if not set(set_of_three).isdisjoint(set_of_cards):
			factor += 1

	return factor

def best_indices_among_min_impact(all_min_impact_indices, table, list_of_remaining_sets, found_sets):
	min_extended_impact = 100000
	if len(found_sets) < 1:
		min_extended_impact_indices = all_min_impact_indices[0]
	else:


		for indices in all_min_impact_indices:
			set_on_table = [table[indices[i]] for i in range(0,3)]
			next_list_of_remaining_sets = list_of_remaining_sets[:]
			sets_to_be_eliminated = []
			for set_of_cards in next_list_of_remaining_sets:
				if not set(set_on_table).isdisjoint(set_of_cards):
					sets_to_be_eliminated.append(set_of_cards)
			for set_of_cards in sets_to_be_eliminated:
				next_list_of_remaining_sets.remove(set_of_cards)
			extended_impact = 0
			for set_of_three in next_list_of_remaining_sets:
				extended_impact += impact_factor_set(set_of_three, next_list_of_remaining_sets)
			if extended_impact < min_extended_impact:
				min_extended_impact_indices = indices
				min_extended_impact = extended_impact

	return min_extended_impact_indices

def best_indices_among_max_impact(all_max_impact_indices, table, list_of_remaining_sets, found_sets):
	max_extended_impact = -1
	if len(found_sets) < 1:
		max_extended_impact_indices = all_max_impact_indices[0]
	else:


		for indices in all_max_impact_indices:
			set_on_table = [table[indices[i]] for i in range(0,3)]
			next_list_of_remaining_sets = list_of_remaining_sets[:]
			sets_to_be_eliminated = []
			for set_of_cards in next_list_of_remaining_sets:
				if not set(set_on_table).isdisjoint(set_of_cards):
					sets_to_be_eliminated.append(set_of_cards)
			for set_of_cards in sets_to_be_eliminated:
				next_list_of_remaining_sets.remove(set_of_cards)
			extended_impact = 0
			for set_of_three in next_list_of_remaining_sets:
				extended_impact += impact_factor_set(set_of_three, next_list_of_remaining_sets)
			if extended_impact > max_extended_impact:
				max_extended_impact_indices = indices
				max_extended_impact = extended_impact

	return max_extended_impact_indices

def get_indices_of_min_ext_impact(lst_indices, table, deck, list_of_remaining_sets, found_sets):
	if found_sets == 0:
		indices_of_min_ext_impact = lst_indices[0]

	else:
		min_average = 10000
		for indices in lst_indices:
			average = average_extended_impact(indices, table, deck, list_of_remaining_sets)
			if average < min_average:
				min_average = average
				min_extended_impact_indices = indices

		return min_extended_impact_indices

def del_by_indices(list_object, indices):
    indices = sorted(indices, reverse=True)

    for index in indices:
        if index < len(list_object):
            list_object.pop(index)

def play_game(selection_method = 'random_choice', debug=False):
	if selection_method not in ['random_choice', 'quasi_thrifty', 'quasi_greedy', 'thrifty', 'greedy']:
		print('Selection method of {selection_method} not acceptable. Please choose an acceptable selection method.'.format(selection_method=selection_method))
		return None
	deck = full_deck[:]
	list_of_remaining_sets = list_of_all_sets[:]
	random.shuffle(deck)
	table = deck[:12]
	del deck[:12]
	found_sets = []
	game_data = []
	if debug:
		print('The game has started. The dealer deals 12 cards to the table. Here they are:')
		print(table)

	while len(find_sets_indices(table)) > 0 or len(deck) > 0:
		if len(find_sets_indices(table)) == 0:
			if debug:
				print('No SETs are present on the table.')
			game_status = [len(deck), len(table), 0, len(list_of_remaining_sets), 0]
			game_data.append(game_status)
			table.extend(deck[:3])
			del deck[:3]
			if debug:
				print('The dealer deals 3 new cards to the table, and here is the new table.')
				print(table)
				print(str(len(deck)) + ' cards still remain in the deck.')
		else:
			if debug:
				print('At least one SET is present on the table.')
			list_possible_sets_indices = find_sets_indices(table)
			if debug:
				print('Here is a list of all available SETs according to their positions on the table.')
				print(list_possible_sets_indices)
			if selection_method == 'random_choice': 
				choice_indices = random.choice(list_possible_sets_indices)
			if selection_method == 'quasi_thrifty':
				choice_indices = min_impact_indices(list_possible_sets_indices, table, list_of_remaining_sets)
			if selection_method == 'quasi_greedy':
				choice_indices = max_impact_indices(list_possible_sets_indices, table, list_of_remaining_sets)
			if selection_method == 'thrifty':
				lst_min_impact_indices = all_min_impact_indices(list_possible_sets_indices, table, list_of_remaining_sets)
				choice_indices = best_indices_among_min_impact(lst_min_impact_indices, table, list_of_remaining_sets, found_sets)
			if selection_method == 'greedy':
				lst_max_impact_indices = all_max_impact_indices(list_possible_sets_indices, table, list_of_remaining_sets)
				choice_indices = best_indices_among_max_impact(lst_max_impact_indices, table, list_of_remaining_sets, found_sets)
			selected_set = [table[index] for index in choice_indices]
			if debug:
				print('The SET in position {choice_indices} is chosen to be removed.'.format(choice_indices=choice_indices))
			game_status = [len(deck), len(table), len(list_possible_sets_indices), len(list_of_remaining_sets), impact_factor(choice_indices, table, list_of_remaining_sets)]
			game_data.append(game_status)
			list_of_remaining_sets, sets_to_be_eliminated = remove_impacted_sets(choice_indices, table, list_of_remaining_sets)
			found_sets.append(selected_set)
			del_by_indices(table, choice_indices)
			if len(deck) == 0:
				if debug:
					print('Here is the new table.')
					print(table)
				continue
			else:
				if len(table) > 9:
					if debug:
						print('Here is the new table.')
						print(table)
				else:
					table.extend(deck[:3])
					del deck[:3]
					if debug:
						print('The dealer deals 3 more cards to the table.')
						print(str(len(deck)) + ' cards still remain in the deck.')
						print('Here is the new table.')
						print(table)


	game_status = [len(deck), len(table), 0, len(list_of_remaining_sets), 0]
	game_data.append(game_status)
	if debug:
		print('There are no available SETs on the table, and no more cards remain in the deck. Therefore, the game has ended. There are {num_cards} cards left on the table:'.format(num_cards=len(table)))
		print(table)

	return game_data, len(table)


def play_multiple_games(num_games=100, selection_method='random_choice', file_name=None): 
	if selection_method not in ['random_choice', 'quasi_thrifty', 'quasi_greedy', 'thrifty', 'greedy']:
		print('Selection method of {selection_method} not acceptable. Please choose an acceptable selection method.'.format(selection_method=selection_method))
		return None
	print('Playing {num_games} games with {selection_method} selection method...'.format(num_games=num_games, selection_method=selection_method))
	if selection_method == 'random_choice' or selection_method == None:
		total_time = round(num_games/45)
	elif selection_method == 'quasi_greedy' or selection_method == 'quasi_thrifty':
		total_time = round(num_games/32)
	else:
		total_time = round(num_games/.5)
	minutes = total_time // 60
	seconds = total_time % 60
	if minutes == 0:
		print('The simulations will take approximately {seconds} seconds'.format(seconds=seconds))
	else:
		print('The simulations will take approximately {minutes} minutes and {seconds} seconds:'.format(minutes=minutes, seconds=seconds))

	games_played = 0
	full_data = []
	list_of_num_cards_remaining = []

	start = time.time()

	for i in range(num_games):
		data, num_cards_remaining = play_game(selection_method)
		data_with_game_number = [[games_played] + datum for datum in data]
		full_data.extend(data_with_game_number)
		list_of_num_cards_remaining.append(num_cards_remaining)

		games_played += 1

	

	end = time.time()
	total_time = round(end - start)
	minutes = total_time // 60
	seconds = total_time % 60

	print('Done!')
	print('{num_games} games were played.'.format(num_games=num_games))
	if minutes == 0:
		print('The actual time it took was about {seconds} seconds'.format(seconds=seconds))
	else:
		print('The actual time it took was about {minutes} minutes and {seconds} seconds'.format(minutes=minutes, seconds=seconds))
	total_rate = round(num_games/total_time, 1)
	print("That's a rate of about {total_rate} games per second!".format(total_rate = total_rate))
	print('Here were the number of times the table was cleared:')
	print(list_of_num_cards_remaining.count(0))

	df = pd.DataFrame(full_data)
	df.columns = ["game_number", "deck_size", "table_size", "sets_available", "sets_remain", "impact_factor"]

	if file_name == None:
		df.to_csv(str(num_games) + '_' + selection_method + '.csv', index=False)
		print('Full data was collected in a csv file named {num_games}_{selection_method}.csv'.format(num_games=num_games, selection_method=selection_method))
	else:
		df.to_csv(file_name + '.csv', index=False)
		print('Full data was collected in a csv file named {file_name}.csv'.format(file_name=file_name))

