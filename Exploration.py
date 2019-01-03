import random
import numpy as np

import Game

def GetBestAction(qValues):
    return Game.Action(np.argmax(qValues))

def GetNextActionEGreedy(getQValues, epsilon):
    if random.random() > epsilon:
        return random.choice([Game.Action.Left, Game.Action.Right, Game.Action.Up, Game.Action.Down])
    else:
        return GetBestAction(getQValues())

def softmax(values):
    return np.exp(values) / float(sum(np.exp(values)))

def GetNextActionBoltzmann(qValues, epoch, epochCount):
    temperature = (-4.99 / epochCount) * epoch + 5

    probs = softmax([qValue / temperature for qValue in qValues])
    actionVal = np.random.choice(probs, 1, p=probs)

    return Game.Action(np.where(probs==actionVal)[0])