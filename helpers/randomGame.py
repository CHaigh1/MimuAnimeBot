import random

def randomGame():
    gamesByLine = []
    with open('games.txt', 'r') as f:
        gamesByLine = f.readlines()

    return gamesByLine[random.randint(0, len(gamesByLine) - 1)][:-1]

def addGame(game):
    with open('games.txt', 'a') as f:
        f.write('\n' + game)