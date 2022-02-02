"""
Script that uses selenium to solve today's Wordle challenge
"""
from selenium.webdriver import Chrome
from website_interactions import initial_click, get_key_buttons, get_result
import time
import numpy as np
from wordle_io import load_words_as_array_of_int, read_user_input
from utils import which_compatible, find_next_guess
from constants import NCHAR, ORD_A, DELAY

# Needs Chrome installed!
driver = Chrome()
driver.get("https://www.powerlanguage.co.uk/wordle/")

# Get rid of the help element blocking the view
initial_click(driver)
# Get button elements representing the keyboard
buttons = get_key_buttons(driver)

# Load allowed words / solutions as arrays of integers. Get their cardinality.
wlist = load_words_as_array_of_int('wordlist.txt')
NW = len(wlist)
solns = load_words_as_array_of_int('solutions.txt')
NS = len(solns)

# For each possible solution we precompute characters present in it to speed things up
letters_present = np.zeros((NS, NCHAR), dtype = 'bool')
for i, sol in enumerate(solns):
    for lett in sol:
        letters_present[i, lett] = True

# Pick ROATE as the first guess. 
guess = 'roate'
# In the form of an int array, which is the representation of words we have been using.
guess_arr = [ord(x) - ORD_A for x in guess]
# We are on our first guess
guess_no = 1

not_solved = True

# Continue until we have only one solution left
while not_solved:

    # Use selenium to enter the guess onto the webpage
    print('Guessing: ', guess)
    for c in guess:
        buttons[c].click()
    buttons['enter'].click()

    # Wait for the graphic to pass
    time.sleep(DELAY)

    # Read off the result (example: gyxxy)
    result = get_result(driver, guess_no)
    print('Result: ', result)

    guess_no += 1
    if result == 'ggggg':
        not_solved = False

    # Discard noncompatible solutions
    filt = which_compatible(solns, letters_present, guess_arr, result)
    solns = solns[filt] 
    letters_present = letters_present[filt]

    # Pick the remaining solution, or find the next best guess
    if len(solns) == 1:
        guess_arr = solns[0]
        guess = ''.join([chr(ORD_A + c) for c in solns[0]])
    else:
        guess, guess_arr = find_next_guess(wlist, solns, letters_present)

# Output the final solution one more time
solution = ''.join([chr(ORD_A + c) for c in solns[0]]).upper()
print('\nSolution is: ', solution)
