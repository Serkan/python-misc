"""
Mastermind game console, coded for 'BCO 601 Python Programlama'
course in Hacettepe University.

Coded in Python 3.4
"""
__all__ = [
    # Public API for external usages
    'start_game', 'break_code', 'play_codebreaker', 'play_codemaker'
]

__author__ = "Serkan Turgut"
__date__ = '28-11-2014'
__version__ = '1.1'
__email__ = "serkan.turgut0@gmail.com"
__status__ = "Production"

import random
import itertools
import sys


def start_game():
    """
    Starts the game by requesting input from user to select whether to
    be codemaker or codebreaker.
    :return:
    """

    def __invalid_start__():
        """Game goes on in loop unless to take a proper player parameter.  """
        print("Please enter 1 or 0 [Default] to play")
        start_game()

    try:
        option = int(input("Which one you are? [default] codebreaker"
                           " or [1] codemaker >") or 0)
    except ValueError:
        __invalid_start__()
    if option not in (0, 1):
        __invalid_start__()
    dispatch(option)


def dispatch(option):
    """
    It dispatches user's player selection to appropriate function.
    :param option: player parameter 1 - > User plays against the codebreaker
                                                            0 -> User plays against the codemaker
    :return:
    """
    players[option]()


def break_code(guess, secret):
    """
    Calculates response as count of  black and white peg(s).
    :param guess:  guessed permutation
    :param secret: the secret which is trying to be found
    """
    z = list(zip(list(guess), secret))
    # find exact matches (color and positions)
    black = [(x, y) for (x, y) in z if x == y]
    black_count = len(black)
    if len(black) == 4:
        white_count = 0
    else:
        # filter z from exact mathes to find white peg count
        white_candidate = [(x, y) for (x, y) in z if x != y]
        if len(white_candidate) > 0:
            nguess, nsecret = zip(*white_candidate)
            white_count = sum([1 for x in set(nguess) if x in nsecret])
        else:
            white_count = 0
    return str(black_count), str(white_count)


def play_codebreaker():
    """The computer is codemaker"""

    def __raise_err_if_invalid__(value):
        """
        Validates the user input whether is appropriate for mastermind
        four pegs format
        :param value: user input
        :return: raises ValueError if input is invalid
        """
        if len(value) != 4:
            raise ValueError
        for ch in value:
            if ch not in colors.keys():
                raise ValueError

    print("You selected to be the codebreaker")
    # select a secret from colors set
    secret = random.sample(colors.keys(), 4)
    # keep asking until the user breaks the code
    step = 1
    while 1:
        if step > 12:
            print ("You could not solve the secret in 12 steps. You lost the game")
            exit()
        try:
            guess = input("Guess my combination ? >")
            __raise_err_if_invalid__(guess)
            step += 1
        except ValueError:
            print('You must select four color codes from ' + str(colors.values()))
            print('Use first letters as color identifier,For instance: cbrg <ENTER>')
            continue
        black, white = break_code(guess, secret)
        if black == 4:
            print("You have got 4 (b)lack, you broke the code!!")
            break
        else:
            print("you have got " + str(black) + " (b)lack and " + str(white) + " (w)hite ")


def play_codemaker():
    """The computer is code breaker """
    print("You selected to be the codemaker")
    # knuth five guesses algorithm implemented 
    pos_secret_list = [p for p in itertools.product(colors.keys(), repeat=4)]
    results = [(right, wrong) for right in range(5)
               for wrong in range(5 - right)
               if not (right == 3 and wrong == 1)]
    # start with this initial guess to eliminate possible guesses significantly
    # colors may change but two one and two another one gives us an
    # important edge
    guess = "ccbb"
    step = 1
    while 1:
        if step > 11:
            print("I could not break the code in 12 step, step lost the game")
            break
        print ("My " + str(step) + ". guess is " + str(guess))
        # get input of black and white pegs
        try:
            res = input("Please enter how many black and "
                                         "white I have got >")
            res = black, white = tuple(res.split(","))
        except (NameError, ValueError, SyntaxError):
            print("Please enter in a proper format, like 2,1")
            continue
        if black == '4' and white == '0':
            print("I broke the code :)")
            break
        # filter possible guess list and continue
        try:
            # dont mutate the pos_secret_list unless
            # you certain response is proper
            temp = [p for p in pos_secret_list if break_code(guess, p) == res]
            guess = max(temp,
                        key=lambda x: min(sum(1 for p in temp
                                              if break_code(p, x) != r) for r in results))
        except ValueError:
            print("You entered an impossible response, please try again")
            continue
        pos_secret_list = temp
        step += 1


if __name__ == "__main__":
    # construct color dictionary (useful for codemaker and codebreaker)
    colors = {'c': '(c)yan', 'b': '(b)lue', 'r': '(r)ed', 'g': '(g)reen', 'p': '(p)ink',
              'y': '(y)ellow'}
    print("Colors that you are allowed to use : ")
    print(colors.values())
    # map handler functions to user options
    players = {0: play_codebreaker, 1: play_codemaker}
    # spawn the game
    start_game()