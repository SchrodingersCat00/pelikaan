import random
from typing import Callable
from matplotlib import pyplot as plt


random.seed(0)
PARTICIPANTS = ['freyatron', 'imilien', 'juliaan', 'hafthor bjornsson', 'kobalt']


def get_cook_imilien(hungries, board):
    cook = max(hungries, key=lambda name: board[name])
    return cook


def update_board_imilien(cook, eaters, board):
    for eater in eaters:
        board[eater] += 1

    board[cook] = 0


def get_cook_kurb(hungries, board):
    cook = min(hungries, key=lambda name: board[name])
    return cook


def update_board_kurb(cook, eaters, board):
    for eater in eaters:
        board[eater] -= 1

    board[cook] += len(eaters)


def update_meals_balance(cook, hungries, meals_balance):
    meals_balance['cooked'][cook] += len(hungries)
    for hungry in hungries:
        meals_balance['eaten'][hungry] += 1


class Algorithm:
    def __init__(self, get_cook, update_board, **config):
        self.get_cook = get_cook
        self.update_board = update_board
        self.config = config

    def run(self, participants):
        board = { name: 0 for name in participants }
        meals_balance = { 
            'cooked': { name: 0 for name in participants }, 
            'eaten': { name: 0 for name in participants }
        }
        for day in range(self.config['cook_days']):
            hungries_amount = random.randrange(
                self.config['min_hungries'], 
                len(participants) + 1
            )
            hungries = random.sample(participants, hungries_amount)
            cook = self.get_cook(hungries, board)
            update_meals_balance(cook, hungries, meals_balance)
            eaters = [x for x in hungries if x != cook]
            self.update_board(cook, eaters, board)

            if 'enable_logging' in self.config and self.config['enable_logging']:
                log_cooking_day(day, hungries, cook, eaters, board)

        return { 
            name: meals_balance['cooked'][name] - meals_balance['eaten'][name] 
            for name in participants
        }


def log_cooking_day(day, hungries, cook, eaters, board):
    print(f'============================== COOKING DAY {day} ===============================')
    print(f'hungries: {hungries}')
    print('cook:', cook)
    print('eaters:', eaters)
    print('board', board)
    print()


def main():
    cook_days = 200
    min_hungries = 3
    algorithms = {
        'kurb': Algorithm(
            get_cook_kurb, 
            update_board_kurb, 
            cook_days=cook_days,
            min_hungries=min_hungries, 
        ),
        'imilien': Algorithm(
            get_cook_imilien,
            update_board_imilien,
            cook_days=cook_days,
            min_hungries=min_hungries,
        ),
        'random': Algorithm(
            lambda hungries, _: random.choice(hungries),
            lambda *_: None,
            cook_days=cook_days,
            min_hungries=min_hungries,
        )
    }


    ITERATIONS = 1000

    most_scammed_per_algo = {}
    for algo_name, algo in algorithms.items():
        most_scammed = []
        for it in range(ITERATIONS):
            diffs = algo.run(PARTICIPANTS)
            most_scammed.append(max(diffs.values()))
        
        most_scammed_per_algo[algo_name] = sum(most_scammed)/len(most_scammed)
    
    print(most_scammed_per_algo)

    plt.bar(most_scammed_per_algo.keys(), most_scammed_per_algo.values())
    plt.show()

if __name__ == '__main__':
    main()