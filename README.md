SET Game Simulator +
====================

***To study the statistics of the card game SET***

**Author:** *Mitchell Faulk*

# Description

The purpose of this repository is to provide a simulator for the [card game SET](https://en.wikipedia.org/wiki/Set_(card_game)).

The original objective was to understand the frequency distribution of the number 
of cards leftover at the end of a game, or, more specifically, how often the table
is cleared of cards entirely, a situation which we call a 'perfect game' and which 
we study in greater detail in a [series](https://mitchellmfaulk.wordpress.com/2022/09/09/clearing-the-table-in-the-game-set/) of blog posts. 

A related objective was to test whether it was possible to develop *selection* algorithms
to increase (or decrease) the likelihood of a perfect game. We wanted to design these
selection algorithms to choose, among those available SETs on the table, the one (or ones)
which would result in the most number of SETs being taken by the end of the game. In addition,
we wanted to devise algorithms which only use information available to the players throughout
the game, meaning that, in particular, the hidden (and shuffled) cards in the remaining deck
should not be included in the algorithms input data. 

Since its creation, the objective of this project has expanded, and, as of this
writing, the simulator now permits the game to be played with cards having as
many features as you'd like (the usual number of features is four). 


# How to use

Place all of the files in the same directory in your computer. (Or clone the repository.)


## Using setgametools.py

The script simulator.py is a minimal working example for using setgametools.py. 
In simulator.py, the first line imports all of the functions from setgametools.py, 
and then the next line calls the play_multiple_games() function with default values 
for all parameters: num_games=100, selection_method='random_choice', file_name=None. 

The parameter num_games refers to the number of games that are simulated. 

The parameter selection_method must be among 5 options: {'random_choice', 'quasi_thrifty', 
'thrifty', 'quasi_greedy', 'greedy'}. The 'quasi_thrifty' and 'thrifty' choices are
selection methods which are based on algorithms which try to collect as many SETs
as possible by the end of the game in order to increase the likelihood of having a 
'perfect' game. (The choice 'thrifty' improves upon 'quasi_thrifty' by a small amoung.)
The other choices are the counterparts to these, meaning that they decrease the likelihood
of having a 'perfect' game. 


By running the minimal working example simulator.py, the output should be a csv file (in
the same directory) which has the name 100_random_choice.csv. (A specific name for the output
file can be chosen with the file_name parameter.)

The csv file will display data from *each* game of the simulation. Precisely, for each game,
it will contain a number of rows, each one corresponding to a different status of the 
game being simulated. The status of a game changes when cards are removed or dealt. For each 
status, the columns keep track of the following information:

1. 'game_number' which is the number of the current game
2. 'deck_size' which is the number of cards that remain the deck
3. 'table_size' which is the current number of cards on the table
4. 'sets_available' which is the current number of available SETs on the table
5. 'sets_remain' which is the number of SETs that could be formed by replacement with the cards still available in the game
6. 'impact_factor' which is the impact factor of the SET that was selected to be removed at this step (or zero if no SETs present)


## Using SETGameClass.py

`class` SETGame(`dimension=4, table_size=dimension`)

A class to collect the data of a SETGame. 

Parameters:

- __dimension__: `int` (Default is 4)

- __table_size__: `int` (Default is `dimension`; then the starting table size for the game is 3*table_size)

Attributes:

- __.dimension__: `int` 
- __.deck__: list (of lists)
- __.table__: list (of lists)
- __.discard__: list (of lists)
- __.SETpositions__: list (of lists)
- __.selectedposition__: list 
- __.table_size__: `int`

### Examples

Constructing a game with 5 features and table size of 18

```py
>>> game = SETGame(dimension=5, table_size=6)
```

Printing all of the states of a standard game
```py
>>> game = SETGame()
>>> for status in game: # game is an iterator
>>> 	print(status)
```

Each status will return a tuple, the data of which is 
```py
status = (len_deck, table, discard, positions, selectedposition)
```
Here, `len_deck` is the number of cards remaining in the deck, and the other variables are defined as tuple versions of the corresponding attributes (e.g. `table = tuple(self.table)`). 

To print the second table of a standard game:
```py
>>> game = SETGame()
>>> iterator = iter(game)
>>> first_state = next(iterator)
>>> second_state = next(iterator)
>>> second_table = second_state[1]
>>> print(second_table)
...
...
((1, 1, 0, 2), (2, 1, 2, 2), (1, 1, 1, 1), (2, 2, 1, 0), (0, 0, 0, 1), (2, 2, 0, 2), (1, 2, 1, 2), (2, 1, 1, 0), (0, 2, 2, 0), (0, 2, 0, 0), (0, 2, 0, 2), (2, 0, 1, 0))
```

# Collaborators

Lance Rettberg has identified typos in the original version of the README file, and both Lance and Seth Rettberg have graciously listened to me rant far too much and too often about my difficulties (and successes) while working on this project. 

Rachael Creager has offered to review the scripts so far and provide feedback. 

# License

MIT License

Copyright (c) 2022 Mitchell Faulk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

