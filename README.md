# set-card-game

In this repository, you will find 

1. A file containing Python code to simulate the playing of the card game Set.

   From Wikipedia: 
   In the usual game, a deck consists of 81 unique cards that vary in four 
   features across three possibilities for each kind of feature: number of 
   shapes (one, two, or three), shape (diamond, squiggle, oval), shading 
   (solid, striped, or open), and color (red, green, or purple). Each possible 
   combination of features (e.g. a card with three striped green diamonds) 
   appears as a card precisely once in the deck.
   
   In the game, certain combinations of three cards are said to make up a set. 
   For each one of the four categories of features — color, number, shape, 
   and shading — the three cards must display that feature as either a) all 
   the same, or b) all different. Put another way: For each feature the three 
   cards must avoid having two cards showing one version of the feature and 
   the remaining card showing a different version.
   
   
   The aspects of the game have been translated to be simulated more easily
   by Python code:
      a. A card consists of a tuple of 4 numbers in base 3. 
      b. A Set consists of a collection of three tuples satisfying the property
         that for each coordinate, either all of the numbers in that coordinate
         are the same or they are all different. 
   
2. The python code includes several functions. Here are some listed according to
   significance:
   a. play_multiple_games(num_games=1000, selection_method='random_choice')
      This function takes two input parameters num_games and selection_method. 
      The parameter num_games is the number of total games to be simulated, and
      its default value is 1000. 
      
      The selection_method parameter describes how the sets are to be selected,
      throughout the entire game, when multiple sets appear on the table at once.
      The selection_method parameter can be among two values 'random_choice' or 
      'impact_factor', with 'random_choice' being the default value. 
      
      i. The value 'random_choice' means that sets are selected randomly among the
         possibilities that appear on the table. This selection method should, we 
         believe, model normal human play. 
      
      ii. The value 'impact_factor' means that sets are selected according to an
          algorithm (described below) which selects the first set on the table with
          the lowest impact factor, a number which describes how many of the possible
          remaining sets would be unavailable after removing the three cards from the
          table (because every card could participate in a number of possible sets).
      
      The output of the function is a dataframe which collects some data during
      every step of game play during each game that is simulated. 
      
      
      

   
   
