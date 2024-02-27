import random
from matplotlib import pyplot as plt


MIN_EATERS = 3
MAX_PARTICIPANTS_AMOUNT = 5

names = ['freyatron', 'imilien', 'juliaan', 'hafthor bjornsson', 'kobalt']

board = { name: 0 for name in names }

iterations = 356

cooking_amount = { name: 0 for name in names }

# def get_cook_random(eaters, _):
#     return eaters[0], eaters[1:]

def get_cook_imilien(participants, board):
    cook = max(participants, key=lambda name: board[name])
    return cook, [part for part in participants if part != cook]

def update_board_imilien(cook, eaters, board):
    for eater in eaters:
        board[eater] += 1

    board[cook] = 0

def get_cook_kurb(participants, board):
    cook = min(participants, key=lambda name: board[name])
    return cook, [part for part in participants if part != cook]

def update_board_kurb(cook, eaters, board):
    for eater in eaters:
        board[eater] -= 1
    board[cook] += len(eaters)

for it in range(iterations):
    # print(f'============================== ITERATION {it} ===============================')
    participants_amount = random.randrange(MIN_EATERS, MAX_PARTICIPANTS_AMOUNT + 1)
    participants = random.sample(names[:MAX_PARTICIPANTS_AMOUNT], participants_amount)
    # print(f'participants: {participants}')
    cook, eaters = get_cook_kurb(participants, board)
    cooking_amount[cook] += len(eaters)
    # print('cook:', cook)
    # print('eaters:', eaters)
    update_board_kurb(cook, eaters, board)
    # print('board', board)
    # print()

print(f'cooking amounts: {cooking_amount}')

plt.bar(names, [cooking_amount[name] for name in names])
plt.show()