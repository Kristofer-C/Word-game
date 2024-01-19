# Word-game
The code and files used to create my word game called "Shattered Corpus."

Shattered Corpus is a puzzle word game where the user is presented with a set of three letters and must input an English word containing those letters consecutively. This may be known as a version of the license plate game.

### The puzzles and their difficulty

The three-letter puzzles (or `keys` as they are referred to in the code and file names) are sorted by the frequency in which they appear in the [Google Books Ngram Dataset](https://books.google.com/ngrams/) along with the most commonly occurring word containing the set. Cutoff points in the sorted puzzles list are used to categorize the puzzles into one of four difficulty levels: Trivial, Elementary, Challenging, and Unfair. I tried to have the trivial puzzles be the ones that require basically no thought to solve. Letter combinations such as "wer," "tho," and "sla" fit into this category. Three letter combinations that are themselves English words are excluded. The Elementary puzzles should often require some thought and be instructive in the kind of thinking required to solve harder puzzles. Challenging puzzles are meant to take time to solve. I tried to ensure that the Challenging puzzles have solutions that most people have heard of and used, if a little obscure. The Unfair puzzles I think are aptly named. I chose the cutoff as the point along the sorted puzzles list where I no longer recognized any of the words. Other letter combinations have still more obscure solutions, but are ommitted from the game. 

Eyeballing cutoff points in the list of puzzles sorted by frequency is not my ideal method for sorting them by difficulty. Some letter combinations that appear very frequently have solutions that are not immediately obvious, such as "opl" in "people." Conversely, letter combinations that appear infrequently can be very recognizable, such as "xci" in "excite." One idea is to sort the puzzles by the number of solutions sitting in the 1000 or 2000 most common words, but that approach has a few more tunable parameters and I didn't get that far. 

### The mechanics

The game opens with some terminal animations which the player may skip by pressing enter, after which they are presented with the main menu. The main menu presents the player with four options: Play, How to play, Clear saved data, and Exit. The player changes the selected item with the up and down arrows and presses enter to make a choice. When the user selects Play, they are then prompted to selected a difficulty level. At the difficulty select menu, the player may press escape to return to the main menu, or use the arrows and enter to select a difficulty of play. After selecting a difficulty, they are put in the main play loop. 





### word_game.py
This is the Python script containing all the code to run the game.

### get_word_counts.py
The Python script used to query English word frequency data from ngrams.dev 

