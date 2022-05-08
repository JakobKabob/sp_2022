#!/usr/bin/env python3
import sys
import string
import random
import getopt
import time
from pprint import pprint

DOT_FILLED = '\u25CF'
DOT_EMPTY = '\u25CB'
NO_DOT = '\u25CC'
PLACE = '\u2594'


def update_ui(state: list, options, solution=None):
    """
    Redraws current state as a UI

    Parameters:
    state (list): input state
    options (list): options to be displayed
    solution (list): solution to be displayed (optional)

    Returns:
    bool: True if all guesses are in the right place
    """
    if solution:
        formatted_sol = ' '.join([*solution])
    else:
        formatted_sol = ' '.join([*'_'*len(state[0][1])])
    print(f'sol: \t{formatted_sol}\t\tset: {options}')

    formatted_state = ''
    for round in state[::-1]:
        option_places = '{} '*len(state[0][1])
        round_str = '{nr}\t' + option_places + '| {feedback}\n'
        round_str = round_str.format(nr=round[0],
                                     *round[1],
                                     feedback=''.join(round[2]))
        formatted_state += round_str

    print(formatted_state+f'\x1B[{len(state)+2}F')


def set_feedback(state: list, solution) -> bool:
    """
    Changes updates feedback of state, returns bool which indicates a win.

    Parameters:
    state (list): input state
    solution (list): solution to be checked against

    Returns:
    bool: True if all guesses are in the right place
    """
    for round in state:
        wrong_place = []
        right_place = []
        for i in range(len(round[1])):
            if round[1][i] == solution[i] and round[1][i] not in right_place:
                right_place.append(round[1][i]) 
                if round[1][i] in wrong_place:
                    wrong_place.remove(round[1][i])
            elif round[1][i] in solution and round[1][i] not in wrong_place+right_place:
                wrong_place.append(round[1][i]) 
                if round[1][i] in right_place:
                    right_place.remove(round[1][i])

        feedback = [DOT_FILLED for _ in right_place] + [DOT_EMPTY for _ in wrong_place] 
        feedback += [NO_DOT for _ in range(len(solution)-(len(wrong_place)+len(right_place)))]

        round[2] = feedback
        with open('state.txt', 'w') as file:
            pprint(state, stream=file)
        if len(right_place) == len(solution):
            return True

    return False


def is_valid_guess(guess: str, options: list, solution: list):
    """"Returns True if guess is valid.""" 
    for letter in guess: 
        if letter not in options or len(guess) != len(solution):
            return False
    return True


def mainloop_human(state: list, options: list, solution: list):
    """
    Mainloop for a normal game.

    Parameters:
    state (list): input state
    solution (list): solution to be checked against
    options (list): options from which a user can choose
    """
    # the ui overwrites itself with every round, based on the shared state, this means that the cursor needs to be 
    # in the very same spot every round.
    for round_number in range(len(state)):

        while True:
            update_ui(state, options=options)
            print(f'\x1B[{len(state)+1}Binput:\t', end='')
            guess = input().upper()
            if not is_valid_guess(guess, options, solution):
                print('\x1B[1A\t\t\tinput not okay', end='')
                print(f'\x1B[{len(state)+1}F',end='')
            else:
                print('\x1B[1A\t\t                                                     ', end='')
                print(f'\x1B[{len(state)+1}F',end='')
                break

        state[round_number][1] = [*guess.upper()]
        if set_feedback(state, solution):
            update_ui(state, options=options, solution=solution)
            print(f'\x1B[{len(state)+1}B')
            print('you won!')
            exit(0)

    update_ui(state, options=options, solution=solution)
    print(f'\x1B[{len(state)+1}B')
    print('u lost')


def mainloop_simple_algo(state: list, options: list, solution: list):
    """
    Mainloop simple algorithm.

    Parameters:
    state (list): input state
    solution (list): solution to be checked against
    options (list): options from which a user can choose
    """
    for round_number in range(len(state)):

        update_ui(state, options=options)
        guess = random.sample(options, len(state[0][1])) 

        state[round_number][1] = guess
        if set_feedback(state, solution):
            update_ui(state, options=options, solution=solution)
            print(f'\x1B[{len(state)+1}B')
            print('you lost!')
            exit(0)

        time.sleep(1)

    update_ui(state, options=options, solution=solution)
    print(f'\x1B[{len(state)+1}B')
    print('you won!')


def usage():
    title = 'Mastermind implementation Structured Programming 2022 - Jochem Boerma\n'
    text = 'This implementation of mastermind has two distinct modes: \"choose\" and \"guess\", when using \
            \nwithout any options the gamemode \"guess\" will be assumed with a solution length of 4 and 6 \
            \ndistinct values to choose from. \
            \nIf you want to play in \"choose\" mode you have to use the --solution [STRING] option. \
            \n\nAlso, this implementation uses letters instead of colours\n'
    
    options = ['-p --positions[NUMBER]: default=4',
        '-v --values[NUMBER] default=6',
        '-r --rounds[NUMBER] default=10',
        '-s --solution[STRING]: implicit \"choose\" mode setting',
        '-a --algo[STRING]: decide on the algorithm the computer will use while in \"choose\" mode, default is \"simple\"' ]

    print(title)
    print(text)
    print('options:\n\t' + '\n\t'.join(options))


def main():
    argv = sys.argv[1:]
    try:
        opts, _ = getopt.getopt(argv, "a:s:v:p:r:h", ["algo=", "solution=", "values=", "positions=", "rounds=","help"])
    except Exception as exp:
        raise Exception(exp)

    tries = 10 # default
    option_places = 4 # default
    solution = None
    options = None
    algo = None
    set_count = None

    for opt, arg in opts:
        if opt in ['-s', '--solution']:
            solution = list(arg.upper())
            if len(set(solution)) != len(solution):
                raise Exception('Solution must not contain double characters')
            option_places = len(solution)
        elif opt in ['-r', '--rounds']:
            tries = int(arg)
        elif opt in ['-p', '--positions']:
            if solution is None:
                if int(arg) > 12:
                    raise Exception(f'Max {opt} is 12')
                option_places = int(arg)
            else: 
                print('ignoring \'{opt}\' for \'-s\' is already specified')
        elif opt in ['-a', '--algo']:
            algo = int(arg)
        elif opt in ['-v', '--values']:
            set_count = int(arg)
        elif opt in ('-h', '--help'):
            usage()
            sys.exit()


    if solution is None:
        options = random.sample(string.ascii_uppercase, (option_places*2) if set_count is None else set_count)
        solution = random.sample(options, option_places)
    else:
        if len(set(solution)) != len(solution):
            raise Exception('no support for duplicates in solution!')
        options = random.sample([x for x in string.ascii_uppercase if x not in solution], (option_places*2) if set_count is None else set_count)
        options+=solution
    options.sort()

    state = [[nr, [*'_'*option_places], [*NO_DOT*option_places]] for nr in [*range(1, tries+1)]]

    if solution is None:
        mainloop_human(state, options, solution)
    elif algo is None or algo == "simple":
        print(f'You are playing against "simple"')
        mainloop_simple_algo(state, options, solution)
    else:
        raise Exception(f'bruh no algo called {algo}')

if __name__ == "__main__":
    print('(first time? Use python mastermind.py --help)')
    main()
