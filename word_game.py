# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
from json import load, dump
from keyboard import wait, send, read_key
from numpy import loadtxt as loadtxt
from numpy import array, delete
from multiprocessing import Process, SimpleQueue, freeze_support
from random import random


# Some initial stuff
os.system("")
N=3 # The length of the keys/puzzles being used.
LINE_CLEAR = '\x1b[2K' # ANSI sequence to clear the current printed line
LINE_UP = '\033[1A' # ANSI sequence to move up a printed line.
data_dir='game data\\'


def resource_path(relative_path):
    '''
    Get absolute path to resource, works for dev and for PyInstaller
    '''
    
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def flush_input():
    '''
    Prevents keys pressed during the game and menu selections from showing up
    at the next input() or in the command line when the program ends.
    '''
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def clear():
    '''
    Clears the terminal window.
    '''
    os.system('cls' if os.name == 'nt' else 'clear')


def greet():
    '''
    Performs the greeting animation.
    '''
    
    # The phrase to use for greeting
    word="Greetings"
    
    # Cycle through the length of the word, displaying consecutive groups of 
    # three letters
    i=0
    while i<=2:
        
        j=i%(len(word)-N+1)
        print(j*" "+word[j:j+N]+(len(word)-j)*" ", end="\r")
        sleep(0.5)
        i+=1
        
    while i<=len(word)-N:
        
        j=i%(len(word)-N+1)
        print(j*" "+word[j:j+N]+(len(word)-j)*" ", end="\r")
        sleep(max(0.1, 0.4-i*0.05))
        i+=1
        
    sleep(1)    


    # Start flashing the whole word until it disappears    
    i=0
    while i<13:   
        print(" "*len(word), end="\r")
        sleep(0.001*i*i)
        print(word, end="\r")
        sleep(0.001*i*i)
        i+=1
    print(" "*len(word), end="\r")
                 
    sleep(2)


def cascade(word_list, n=100, dt=0.015):
    '''
    Rapidly prints random snippets of words in the word list.
    '''
    i=0
    while i<=n:
        
        phrase=""
        for word in word_list:
            r=random()
            if len(word)>N:
                j=int(r*(len(word)-N+1))
                word=j*" "+word[j:j+N]+(len(word)-j-N)*" "
            elif r>0.3:
                word=" "*len(word)
            phrase=phrase+word+" "
        print(phrase)
        sleep(dt)
        i+=1
    

def welc():
    '''
    Runs the "welcome to Shattered Corpus cascade animation."
    '''
    dt=0.015
    word_list=["Welcome"]
    cascade(word_list, 50, dt)
    word_list=["Welcome","to",]
    cascade(word_list, 50, dt)
    word_list=["Welcome","to","Shattered", "Corpus"]
    cascade(word_list, 200, dt)    
    word_list=["       ","  ","Shattered", "Corpus"]
    cascade(word_list, 25, dt)
    
    for i in range(50):
        print(" ")
        sleep(dt)
    clear()
    sleep(2)
    
    
def intro_animations():
    '''Plays the introductory animations.'''
    
    sleep(1)
    greet() # Play the greeting animation
    welc() # Play the "Welcome to the Terminal" animation
    send('enter') # Press and release the enter key so the program
    # isn't waiting for the user to hit enter after the animations are done
    
    
def difficulty_select_animation():
    '''
    Animates the 'select your difficulty' heading.
    '''
    
    #clear()
    n=30
    dt=0.05
    i=1
    word_list=["Select", "your", "difficulty"]
    phrase_len=0
    for word in word_list:
        phrase_len+=len(word)+1
    
    while i<=n:
        
        if i>0.75*n:
            dt=0.05*(i+1-0.75*n)
        print(end=LINE_CLEAR)
        
        phrase=""
        for word in word_list:
            r=random()
            if len(word)>N:
                j=int(r*(len(word)-N+1))
                word=j*" "+word[j:j+N]+(len(word)-j-N)*" "
            elif r>0.3:
                word=" "*len(word)
            phrase=phrase+word+" "
        print(phrase+":", end="\r")
        sleep(dt)
        i+=1

    sleep(0.5)
    send('enter')

        
def difficulty_menu_update(index):
    '''
    Updates the display of the difficulty menu according to the provided
    currently selected index.
    '''
    
    # The list of difficulties as broken words
    diff_list_broken=["  ivi  ", "     nta  ", "   lle     ", "  fai "]
    dt=0.1
       
    # The list to be displayed. Contains the options as broken forms except the
    # one currently selected by the index variable. If no arrow press has been
    # made yet, display all options as broken (unselected)
    disp_list=diff_list_broken.copy()
    if index!=None:
        dt=0
        disp_list[index]=diff_names[index]
        print(LINE_UP*len(disp_list), end="\r")
    
    # Display the list with the current selection.
    for diff in disp_list:
        print(diff)
        sleep(dt)

    
        
def difficulty_menu():
    '''
    Displays the difficulty menu and allows the user to make a selection.
    Returns the index of the difficulty list that was selected.
    '''
    # Start the difficulty select animation as a different process so it can be
    # skipped.
    process=Process(target=difficulty_select_animation, daemon=True)
    process.start()
    
    # If/when the escape key is pressed, terminate the animations
    wait('enter')
    if process.is_alive():
        process.terminate()
    print("\n")
    
    
    n=4 # The number of difficulty options
    index=None # Set index to None to trigger an initial menu setup
    difficulty_menu_update(index) # Display the initial menu setup
    #wait('down') # Wait for the user to press the down arrow
    sleep(0.4) # Wait a little bit.
    index=0 # Set the index to 0
    difficulty_menu_update(index)
    sleep(0.2)  

    # Allow the user to cycle between selections with the arrow keys until
    # they press enter or escape
    event=read_key()
    while not (event=='enter' or event=='esc'):
    
        if event=='down':
            index=(index+1)%n
            difficulty_menu_update(index)
            
        elif event=='up':
            index=(index-1)%n
            difficulty_menu_update(index)
        
        sleep(0.2)  
        
        event=read_key()
        
    flush_input()
    
    # Return the selected difficulty index if they pressed enter
    if event=='enter':
        return index 
    # if they pressed escape, return to the main menu.
    else:
        main()
    

def puzzle_loop(fileno, q, dictionary, keys, solutions):
    '''
    This is the main game loop. In each iteration, it randomly selects a key 
    from the list, waits for the user's guess, and checks if it works.
    '''
    
    #clear()
    # Open the SDINT so that inputs can be taken in the subprocess
    sys.stdin = os.fdopen(fileno)

    while len(keys)>0:
        
        # Randomly select the index of a key for the next puzzle
        key_ind=int(random()*len(keys))
        key=keys[key_ind] # Get the key
        solution=solutions[key_ind] # Get the solution
        print(key) # Display the key
        
        cont=False
        while not cont:
            
            # Read the users input
            guess=input().strip().lower()
            
            # If the user chooses to skip
            if guess=='1':
                
                cont=True
            
            # If the user chooses to reveal the answer
            elif guess=='2':
                print("One solution is: %s"%solution) # Print the solution
                cont=True
                input() # Wait for the user to press enter to continue
                           
            
            # If the user guesses the word and gets it right
            elif len(guess)>=len(key) and guess in dictionary and key in guess:
                
                q.put(key) # Put the completed key in the queue 
                # Remove the key and solution from the respective lists
                keys=delete(keys, key_ind)
                solutions=delete(solutions, key_ind)
                cont=True
                print("well done.")
                
                # If the user guessed a different solution that the saved one,
                # reveal the solution
                if not guess==solution:
                    print("Another solution is: %s."%solution)

                input() # Wait for the user to press enter to continue
 
            # If the user's input does not match
            else:
                print("Guess again.")
        
                
        clear() # Clear the screen for the next puzzle
    
    # If the loop ended, the user completed the difficulty.
    # Send escape so that the main process isn't waiting for the user.
    send('esc')


def play():
    '''
    The code that runs when the user selects play from the main menu. It loads 
    the saved data, checks if the user has completed every puzzle, runs the 
    difficulty menu and ensures the user's choice is one they have not completed,
    removes the saved list of completed puzzles from the default list of puzzles
    for the selected difficulty, starts the puzzle-playing loop, waits for the 
    user to press escape for it to kill the puzzle loop, saves the data, then 
    checks if the user completed all the puzzles in that difficulty.
    '''
    
    clear()   
    # Load the save data
    with open(savef, 'r') as f:
        save_dict=load(f)
        
    # If the user has completed every puzzle in each difficulty
    # Send them back to the main menu until the erase their progress.
    if len(save_dict["Complete"])==len(diff_names):
        sleep(0.5)
        print("Congratulations.")
        sleep(1)
        print("You have completed every puzzle. \
You are encouraged to erase the saved data and begin again.")
        wait("enter")
        main()
    
    
    # Get the difficulty level from the user
    diff_name=diff_names[difficulty_menu()]          
        
    # Make sure the user selects a difficulty with some puzzles left to 
    # solve before continuing
    while diff_name in save_dict["Complete"]:
        
        print("All puzzles in %s have been completed. \
Select another difficulty."%diff_name)
        wait('enter')
        clear()
        diff_name=diff_names[difficulty_menu()]    
    
    # Load the keys and solutions for the selected difficulty
    keys, solutions=loadtxt(resource_path(data_dir+'keys_'+diff_name+'.txt'),
                               dtype=str,
                               usecols=(0,2)).T
    num_puzzles=len(keys) # The number of puzzles in the difficulty before removing
        # the saved ones
              
    # Delete completed keys from the keys list if there are any
    if len(save_dict[diff_name])>0:
        
        # Find the index in the keys and solutions lists of the completed keys
        remove_inds=[]
        for key in save_dict[diff_name]:
            remove_inds.append((key==keys).nonzero()[0][0])
        remove_inds=array(remove_inds)
    
        # Delete items from the keys and solutions lists 
        keys=delete(keys, remove_inds)
        solutions=delete(solutions, remove_inds)
       
    # Start the play loop
    clear()
    fn = sys.stdin.fileno() # Read the name of the SDINT file
    q=SimpleQueue() # Start a queue
    play_proc=Process(target=puzzle_loop, 
                      args=(fn, q, dictionary, keys, solutions), 
                      daemon=True)
    play_proc.start()

    # Let the play run until the user hits escape or finishes the difficulty
    wait('esc')
          
    # Add the list of completed keys to the save dictionary
    while not q.empty():
        save_dict[diff_name].append(q.get())
    
    # End the play process
    if play_proc.is_alive():
        play_proc.terminate()
    
    # IF the user completed the difficulty, inform them and wait for enter.
    if len(save_dict[diff_name])==num_puzzles:
        save_dict["Complete"].append(diff_name) # Add the current difficulty
            # to the list of completed ones
        
        # If the user has now completed every puzzle in each difficulty, send 
        # them back to the main menu until they erase their progress.
        if len(save_dict["Complete"])==len(diff_names):
            sleep(0.5)
            print("Congratulations.")
            sleep(1)
            print("You have completed every puzzle. \
You are encouraged to erase the saved data and begin again.")
            wait("enter")

        else:
            print("Congratulations. You have completed all the puzzles in %s."%diff_name)    
            wait('enter')
        
    # Save progress
    with open(savef, 'w') as f:
        dump(save_dict, f)
    
    
def how_to_play():
    '''
    The code that runs when the user selects 'how to play' from the main menu.
    Clears the screen and displays a description of the game. Waits for the 
    user to press enter before ending.
    '''
    
    clear()
    print("How to play:\n")
    print(
'Each puzzle is a set of three letters that appear consecutively\n\
in at least one English word. Input a word containing the three\n\
consecutive letters and press enter. To skip a puzzle, input 1. \n\
To see a solution, input 2. To return to the main menu at any time,\n\
press escape.')
    print("\nPress enter to return to the main menu.")
    
    wait('enter')
    
    
def clear_saved():
    '''
    The code that runs when the user selects 'clear saved data' from the main 
    menu. It asks the user to confirm their choice to clear the saved data. If 
    yes, it replaces the data in the save file with an empty dictionary, 
    displays a confirmation message and waits for the user to press enter before
    ending. If no, the function ends.
    '''
    
    clear()
    # Warn the user about erasing saved data.
    print("Clearing the save data will erase all progress. Continue?")
    
    # Run a quick yes/no menu
    yn=['No', "Yes"]
    index=0
    for i, x in enumerate(yn):
        sleep(0.1)
        print(f"{'>'*int(i==index):<2}{x}")
    sleep(0.2)
    event=read_key()
    while event!='enter':
        
        if event in ['up', 'down']:
            index=(index+1)%len(yn)
        
        print((len(yn)+1)*LINE_UP)
        for i, x in enumerate(yn):
            print(f"{'>'*int(i==index):<2}{x:<3}")
            
        sleep(0.2)    
        event=read_key()
    
    
    # If the user elected to erase the data
    if index==1:
    
        # Create an empty dictionary
        empty_save_dict={"Complete":[]}
        for diff in diff_names:
            empty_save_dict[diff]=[]
        
        # And write it to the save file
        with open(savef, 'w') as f:
            dump(empty_save_dict, f)
        
        print("Save data has been erased.\nPress enter to return to the main menu.")
        wait('enter')
    
    
def main_menu_update(index):
    '''
    Updates the display of the difficulty menu according to the provided
    currently selected index.
    '''
    
    # The list of menu items to select from
    menu_list=["Play", "How to play", "Clear saved data", "Exit"]
    menu_list_broken=["Pla ", "How to pla ", " lea    ved dat ", " xit"]
    dt=0.1 # Print out the menu options slightly slower the first time
       
    # The list to be displayed. Contains the options as broken forms except the
    # one currently selected by the index variable. If no arrow press has been
    # made yet, display all options as broken (unselected)
    disp_list=menu_list_broken.copy()
    if index!=None:
        dt=0 # Remove the print out delay if this is not the first time.
        disp_list[index]=menu_list[index]
        print(LINE_UP*len(disp_list), end="\r")
    
    # Display the list with the current selection.
    for item in disp_list:
        print(item)
        sleep(dt)
  
        
def main_menu():
    '''
    Displays the difficulty menu and allows the user to make a selection.
    Returns the index of the difficulty list that was selected.
    '''
                
    n=4 # The number of menu options
    index=None # Set index to None to trigger an initial menu setup
    main_menu_update(index) # Display the initial menu setup
    sleep(0.4) # Wait for a sec
    index=0 # Set the index to 0
    main_menu_update(index) # Update the display to show "Trivial" as selected
    sleep(0.2) # Wait so not too many key presses are registered at once
    
    # Allow the user to cycle between selections with the arrow keys until
    # they press enter
    event=read_key()
    while not event=='enter':
    
        if event=='down':
            index=(index+1)%n
            
        elif event=='up':
            index=(index-1)%n
        
        main_menu_update(index)
        sleep(0.2)
        event=read_key()
        
    return index # Return the selected main menu index
    

def main():
    '''
    The main function that starts the game, beginning with the main menu.
    '''

    clear()
    menu_index=main_menu() # Get the selected menu index from the user.
    
    # The user selected 'Play'
    if menu_index==0:

        # Run the play function which ends when the user presses escape or 
        # completes the difficulty.
        play()
        main() # Return to the main menu
    
    
    # The user selected 'How to play'
    if menu_index==1:
        
        # Run the how to play function which waits for the user to press enter
        # before ending.
        how_to_play()
        main() # Return to the main menu
        
        
    # The user selected 'Clear saved data'
    if menu_index==2:
        
        # Run the clear saved data function, which waits for the user to choose
        # to erase the saved data and press enter before ending.
        clear_saved()
        main() # Return to the main menu
        
        
    # User selected 'Exit'
    if menu_index==3:
        
        flush_input() # Clear the buffer of keystrokes so they aren't sent to 
        # the command line when the program finishes.
        sys.exit()
        
        

if __name__=="__main__":

    freeze_support()

    # Define the different file names to be loaded depending on the selected
    # difficulty
    diff_names=['Trivial',
                'Elementary',
                'Challenging',
                'Unfair']
    
    # Load the list of accepetable words
    dictionary=loadtxt(resource_path(data_dir+"word_list.txt"), dtype=str)
    savef=resource_path(data_dir+'save_data.txt') # The name of the save file

    # Start the beginning animations as a separate process so it can be skipped
    clear()
    input("Press enter to begin.")
    
    clear()
    process=Process(target=intro_animations, daemon=True)
    process.start()
    # If/when the enter key is pressed, terminate the animations
    wait('enter')
    if process.is_alive():
        process.terminate()
    
    main()


    
    
    