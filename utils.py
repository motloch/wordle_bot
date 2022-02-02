import numpy as np
from constants import WLEN, ORD_A

def which_compatible(solns, letters_present, guess, message):
    """
    Given a set of solutions, guess and the resulting green-yellow-gray message, return a
    boolean array signalling whether given solution is compatible with the message.

    letters_present is used to speed things up and each row one hot encodes which letters
    are present in given solution candidate.
    """

    # Start with all solutions being allowed
    filt = np.ones(len(solns), dtype = 'bool')

    # Go through the letters and investigate compatiblity with the received message
    for i in range(WLEN):

        # i-th letter is green -> only pick solutions with the same i-th letter
        if message[i] == 'g':
            filt *= (solns[:, i] == guess[i])
        # i-th letter is yellow -> this letter must be present in the solution
        elif message[i] == 'y':
            filt *= letters_present[:, guess[i]]
        # i-th letter is gray -> this letter must be absent in the solution
        # (assuming this letter is not present in guess twice and the other
        # occurrence is yellow/green)
        elif (guess[i] not in guess[:i]) and (guess[i] not in guess[(i+1):]):
            filt *= np.logical_not(letters_present[:, guess[i]])

    # Return only the solutions compatible with the message
    return filt

def get_num_compatible(solns, letters_present, guess, true_sol):
    """
    Calculate how many of the candidate solutions are compatible with the
    gray-green-yellow pattern revealed by the guess.

    We are given integer arrays representing a set of allowed solutions, our guess and a
    true solution.

    letters_present is used to speed things up and each row one hot encodes which letters
    are present in the given solution candidate.
    """
    NS = len(solns)

    # Start with all solutions being allowed
    filt = np.ones(NS, dtype = 'bool')

    # Go through the letters
    for i in range(WLEN):

        # i-th letter is green -> only pick solutions with the same i-th letter
        if guess[i] == true_sol[i]:
            filt *= (solns[:, i] == true_sol[i])
        else:
            # i-th letter is yellow -> this letter must be present in the solution
            if np.count_nonzero(guess[i] == true_sol):
                filt *= letters_present[:, guess[i]]
            # i-th letter is gray -> this letter must be absent in the solution
            else:
                filt *= np.logical_not(letters_present[:, guess[i]])

    # Count the number of compatible solutions
    return np.sum(filt)

def find_next_guess(wlist, solns, letters_present):
    """
    Given a list of allowed words and solutions, find the optimal next guess.

    By making a guess we restrict the potential solutions to a subset. We choose a guess
    for which the expected size of this subset is the smallest possible.
    """

    NS = len(solns)
    NW = len(wlist)

    # For a given guess, for each possible solution calculate how many solutions are still
    # allowed after revealing the green-yellow-gray pattern
    remaining = np.zeros(NS, dtype = int)

    # Keeping track of the optimal found solution
    best_val = 1000
    best_str = ''
    best_arr = []

    # Cycle through the initial guesses
    for i in range(NW):

        # Cycle through solutions and calculate the expected number of solutions remaining
        # if we start the guessing with the NW-th word
        for j in range(NS):
            remaining[j] = get_num_compatible(solns, letters_present, wlist[i], solns[j])
        remaining_ev = np.mean(remaining)

        # When we find improvement
        if remaining_ev < best_val:
            best_val = remaining_ev
            best_str = ''.join([chr(ORD_A + c) for c in wlist[i]])
            best_arr = wlist[i]

    return best_str, best_arr
