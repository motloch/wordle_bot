"""
A bot that solves a Wordle riddle based on a series of user inputs that encodes the
green/yellow/gray squares provided by the website
"""

import numpy as np
from wordle_io import load_words_as_array_of_int, read_user_input
from utils import which_compatible, find_next_guess
from constants import NCHAR, ORD_A

# Load allowed words / solutions as arrays of integers. Get their numbers.
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

# Continue until we have only one solution left
while len(solns) > 1:
    user_input = read_user_input(guess)

    # Discard noncompatible solutions
    filt = which_compatible(solns, letters_present, guess_arr, user_input)
    solns = solns[filt] 
    letters_present = letters_present[filt]

    guess, guess_arr = find_next_guess(wlist, solns, letters_present)

solution = ''.join([chr(ORD_A + c) for c in solns[0]]).upper()
print('\nSolution is: ', solution)
