#!/usr/bin/env python3
import sys
import string
import random
import getopt

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
    print(f'sol: \t{formatted_sol}\t\toptions: {options}')

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
            elif round[1][i] in solution and round[1][i] not in wrong_place:
                wrong_place.append(round[1][i]) 
                if round[1][i] in right_place:
                    right_place.remove(round[1][i])

        feedback = [DOT_FILLED for _ in right_place] + [DOT_EMPTY for _ in wrong_place] 
        feedback += [NO_DOT for _ in range(len(solution)-(len(wrong_place)+len(right_place)))]

        round[2] = feedback
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
            break

    update_ui(state, options=options, solution=solution)
    print(f'\x1B[{len(state)+1}B')


def usage():
    print('iuwbrg')


def main():
    argv = sys.argv[1:]
    try:
        opts, _ = getopt.getopt(argv, "s:t:w:h", ["algo=", "width=","help"])
    except Exception as exp:
        raise Exception(exp)

    tries = 10 # default
    option_places = 4 # default
    solution = None
    options = None
    algo = None

    for opt, arg in opts:
        if opt in ['-s']:
            solution = list(arg.upper())
            if len(set(solution)) != len(solution):
                raise Exception('Solution must not contain double characters')
            option_places = len(solution)
        elif opt in ['-t']:
            tries = int(arg)
        elif opt in ['-w', '--width']:
            if solution is None:
                if int(arg) > 12:
                    raise Exception(f'Max {opt} is 12')
                option_places = int(arg)
            else: 
                print('ignoring \'{opt}\' for \'-s\' is already specified')
        elif opt in ['--algo']:
            algo = int(arg)
        elif opt in ('-h', '--help'):
            usage()
            sys.exit()


    if solution is None:
        options = random.sample(string.ascii_uppercase, option_places*2)
        solution = random.sample(options, option_places)
    else:
        options = random.sample([x for x in string.ascii_uppercase if x not in solution], option_places)
        options+=solution
    options.sort()

    state = [[nr, [*'_'*option_places], [*NO_DOT*option_places]] for nr in [*range(1, tries+1)]]

    if algo == 1:
        pass
    elif algo == 2:
        pass
    else:
        mainloop_human(state, options, solution)


if __name__ == "__main__":
    main()
