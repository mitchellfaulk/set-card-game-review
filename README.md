# set-card-game

The purpose of this repository is to provide a simulator for the card game SET. The full
purpose is explained in much better detail in a series of blog posts, the first of which
can be found at the following link

https://mitchellmfaulk.wordpress.com/2022/09/09/clearing-the-table-in-the-game-set/. 

The game is played with a deck of 81 (= 3^4) cards, which vary in four features across
three possibilities for each feature. To simplify matters, we model the cards as 
points in a vector space of dimension 4 in characteristic 3. More precisely, each
card is a list of four elements, where each element is an integer among {0,1,2}. 

The game proceeds by identifying and collecting SETs, which are collections of three
cards satisfying certain conditions in the game's instruction manual. It turns out
that, if we identify cards with points in a vector space, then the cards lying at 
points x, y, and z form a SET if and only if x + y + z = 0. 

In usual play, the game begins with 12 cards lying face-up on the table, and SETs 
are collected from this table, being replaced by cards from the deck. In the instance
that all players agree there are no cards on the table, three more cards are temporarily
added. 

The game finishes once the deck runs out and all players agree there are no more SETs
on the table. 

During most of play, there are usually several SETs available on the table at the same
time, and, when played by humans, the first SET to be identified is removed. It is 
difficult to know which types of SETs are most often identified first (though there is
some speculation), and so to model human play, we have included a method of simulation
whereby the choice of SETs is always random. More precisely, for both of the functions

1. play_game()

2. play_multiple_games()

there is a parameter selection_method, whose default value is set to 'random_choice'
in order to model human play. When this setting is selected, every time there are 
multiple SETs on the table, the computer chooses one at random to remove. 

There are other options for selection_method as well, and, in fact, these other options
are indicative of the main purpose of this simulator. 

You see, when each game finishes, there are a certain number of cards left on the table, 
typically 6 or 9, and always a multiple of 3. In very few games (around 1% with the 
'random_choice' setting), the game ends with no cards left on the table at all. I wondered
whether different selection_method's could affect the number of cards remaining at the
game's end. In particular, I wondered whether I could devise an algorithm, which uses
only the information of available to all current players, in order to select, from those 
available SETs, the one(s) which might increase the chances of having a 'perfect' end
game. 

The 'quasi_thrify' and 'thrify' selection methods are such options, based on algorithms
present in the code. The 'quasi_thrify' option was the first implementation, and 'thrifty'
improves upon 'quasi_thrify' by a small margin. 

(Because the algorithms producing these options are of min-max type, they also naturally 
enjoy counterparts, which achieve opposite results, and which I call 'quasi_greed' and
'greedy'.)

Both of the 'quasi_thrify' and 'thrify' algorithms are based upon computations involving
a quantity that I call 'impact_factor' and which is roughly defined as follows. 

By selecting with replacement, it is possible to form, with a full deck of cards, a maximum
of 1080 SETs. But the game proceeds without replacement, and so once certain cards are 
removed from the game, they remove remove with them a certain number of elements from
this list of 1080. I call this number of elements that would be removed by a SET its impact
factor. 

Because the goal of 'quasi_thrifty' and 'thrifty' is to form as many SETs as possible, the
algorithms work by selecting those SETs with minimal impact factors, thereby leaving as many
SETs as possible to be formed later in the game. In other words, the algorithms work by 
computing the impact factor of each available SET on the table, and then selecting one of the
SETs with minimal impact factor. 

The 'thrifty' algorithm improves upon this a little further, because I noticed that there 
could be instances where two SETs both achieve minimal impact factor, and so I wanted to 
have a further ranking system which could select among such optimal options. So what the
'thrifty' algorithm does is look ahead one step, and compute the impact factor of each of 
those SETs that would be left remaining (from the original list of 1080) upon removing one
of these optimal choices. The algorithm then adds up all of these impact factors, and it 
selects the option with minimal sum. 

The play_game() function also includes a debug variable, which can be set to True if you
want to see how the game plays out. 

The play_multiple_games() function includes two other variables:

1. num_games [int], which is the number of games that are to be simulated; the default
setting is 100

2. file_name [str], which is the desired name of the csv file containing the output data;
the default setting is None, and in this case, the output file will have a name of 
str(num_games) + '_' + selection_method.csv In other words, if 200 games are simulated 
with selection_method='quasi_thrifty', then the output csv file will be 200_quasi_thrifty.csv. 

The output csv file has 6 columns, and each row represents a status of a game. The status 
changes when cards are removed or dealt. 

1. 'game_number' which is the number of the current game
2. 'deck_size' which is the number of cards that remain the deck
3. 'table_size' which is the current number of cards on the table
4. 'sets_available' which is the current number of available SETs on the table
5. 'sets_remain' which is the number of SETs that could be formed by replacement with the cards still available in the game
6. 'impact_factor' which is the impact factor of the SET that was selected to be removed at this step (or zero if no SETs present)

----

A minimal working example of the code is also provided in simulator.py. (The script will
simulate 100 games with selection_method='random_choice', and it will take approximately
2 seconds to complete the simulations. Some data from the simulations will be collected
and stored in a csv file called 100_random_choice.csv. )

