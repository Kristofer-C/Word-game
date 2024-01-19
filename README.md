# Word-game
The code and files used to create my word game called "Shattered Corpus."

Shattered Corpus is a puzzle word game where the user is presented with a set of three letters and must input an English word containing those letters consecutively. This may be known as a version of the license plate game.


### The mechanics

The game opens with some text animations which the player may skip by pressing enter, after which they are presented with the main menu. The main menu presents the player with four options: Play, How to play, Clear saved data, and Exit. The player changes the selected item with the up and down arrows and presses enter to make a choice. 

When the player selects "Play," another skippable animation plays and they are then prompted to selected a difficulty level. At the difficulty select menu, the player may press escape to return to the main menu, or use the arrows and enter to select a difficulty of play. After selecting a difficulty, they are put in the main play loop where they are presented with a puzzle randomly selected from the list of puzzles for that difficulty. The player may enter a word which is then checked for two conditions: it contains the puzzle exactly, and it is a real English word in the dictionary. If one or both conditions are not met, the player is instructed to guess again. If both conditions are met, the player is informed of the tabulated solution and the puzzle is added to a list of completed ones. The player may also input "1" to pass and get the next puzzle, or "2" to see the solution. When the player sees the solution, the puzzle is not saved as completed. In all cases other than an incorrect guess, once the player presses enter, they are presented with another puzzle. The loop continues until the player exhausts the puzzles for the selected difficulty or presses escape which immediately directs them to the main menu. 
**NOTE:** the list of puzzles completed in the session is not saved to the `save_data.txt` file until the player presses escape to return to the main menu. Progress will be lost if the user exits the application before then.

When the player selects "How to play," they are presented with a few short sentences describing the rules of the game and their input options during play. The player presses enter to return to the main menu.

When the player selects "Clear saved data," they are asked to confirm their choice before the save file is overwritten with an empty Python dictionary. The player presses enter to return to the main menu.

The app closes when the play selects "Exit."


### The puzzles and their difficulty

The three-letter puzzles (or `keys` as they are referred to in the code and file names) are sorted by the frequency in which they appear in the [Google Books Ngram Dataset](https://books.google.com/ngrams/) along with the most commonly occurring word containing the set. Cutoff points in the sorted puzzles list are used to categorize the puzzles into one of four difficulty levels: Trivial, Elementary, Challenging, and Unfair. I tried to have the trivial puzzles be the ones that require basically no thought to solve. Letter combinations such as "wer," "tho," and "sla" fit into this category. Three letter combinations that are themselves English words are excluded. The Elementary puzzles should require some brief thought and be instructive in the kind of thinking required to solve harder puzzles. Challenging puzzles are meant to take time to solve. I tried to ensure that the Challenging puzzles have solutions that most people have heard of and used, if a little obscure. The Unfair puzzles I think are aptly named. I chose the cutoff as the point along the sorted puzzles list where I no longer recognized any of the solution words. Other letter combinations have still more obscure solutions, but are ommitted from the game. 

At any point, the player is free to search the web, browse the `key_*.txt` files with solutions, or just ask the game for the answer. It is tempting to do so when you're crushing through the Elementary's and then are stumped for a few seconds on the next one. But it is much more rewarding to take the time, think outside the box, and come up with a solution. There is no penalty for failed guesses. In fact, it is difficult to judge whether a commonly used compound phrase is included as a word in the dictionary, so a barrage of guesses can be very useful and perfectly justified.

Eyeballing cutoff points in the list of puzzles sorted by frequency is not my ideal method for sorting them by difficulty. Some letter combinations that appear very frequently have solutions that are not immediately obvious, such as "opl" in "people." Conversely, letter combinations that appear infrequently can be very recognizable, such as "xci" in "excite." One idea is to sort the puzzles by the number of solution words sitting in the 1000 or 2000 most common words, but that approach has a few more tunable parameters and I didn't get that far. If you feel like keeping a list of puzzles that you think belong in another difficulty, I would be very happy to receive it.


### Notes

- The posted distribution only works on Windows.
- The word list used in the program is not complete. For example, I needed to manually add "etiquette" and a few other fairly common words.


## Files

### word_game.py
This is the Python script containing all the code to run the game.

#### \game data
The directory containing the `.txt` files that are accessed and/or written to during play.
##### `word_list.txt`


### get_word_counts.py
The Python script used to query English word frequency data from ngrams.dev with words from `word_list.txt`. It outputs the file called

### words_to_keys_counts.py
The Python script that 

