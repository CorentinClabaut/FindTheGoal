import os

import Game
import Exploration
import Model

def PlayWithModel(modelPath):
    if not os.path.isdir(modelPath):
        print("No model: " + modelPath)
        return

    estimator = Model.GetModel(modelPath)

    state = Game.CreateState(None, Game.Pos(1, 2), None)
    print(state)

    maxMovesCount = 5
    nbMoves = 0
    while (not state.IsFinished()):
        if nbMoves == maxMovesCount:
            print('lost because did too many moves')
            return

        action = Exploration.GetBestAction(Model.GetQValue(state, estimator))
        print(str(action) + '\n')
        state.Move(action)
        print(state)
        nbMoves += 1

modelPath = 'models/model'
PlayWithModel(modelPath)
