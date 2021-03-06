import numpy as np
from constants import WLEN, ORD_A

def load_words_as_array_of_int(fname):
    """
    Load a list of words - each of length WLEN - from a file into a numpy array, one word
    per row. To speed up, use np.byte data type. In the output array, 'a' is represented
    as zero, 'b' as one, ...
    """

    wlist_orig = open(fname).read().splitlines()

    wlist = np.zeros((len(wlist_orig), WLEN), dtype = np.byte)
    for i, word in enumerate(wlist_orig):
        for j, char in enumerate(word):
            wlist[i, j] = ord(char) - ORD_A

    return wlist

def read_user_input(bot_guess):
    """
    Given guess generated by the bot, writes it out and inquires about the result. Does
    basic checking of the input and asks until it gets correct input (string of five
    letters g/y/x), which is then returned.
    """

    print('My guess is "' + bot_guess.upper() +'", what is the result? '+
        '(Green = g, Yellow = y, Gray = x; Example: gyxxy)')

    correct = False
    while not correct:
        correct = True
        user_input = input('Result: ')

        if len(user_input) != WLEN:
            print('Wrong length')
            correct = False

        for i in range(WLEN):
            if user_input[i] not in ['g', 'y', 'x']:
                print('Wrong character')
                correct = False

    return user_input
