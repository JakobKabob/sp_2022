import string
import random

def check_result(solution, question):
    assert len(solution) == len(question)
    rightplace = somewhere = 0
    for i in range(len(question)):
        if question[i] == solution[i]:
            rightplace += 1
        elif question[i] in solution:
            somewhere += 1

    return (rightplace, somewhere)


def losa(solution, question):
    assert len(solution) == len(question)

    





set = [l for l in string.ascii_uppercase[0:6]]
solution = random.sample(set, 4)

