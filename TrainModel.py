import shutil
from distutils.dir_util import copy_tree

import Game
import ExperienceReplayer as ER
import Exploration
import Model

def OverrideDir(destination, source):
    shutil.rmtree(destination, ignore_errors=True)
    copy_tree(source, destination)

def CreateAndTrainModel(modelToSavePath):
    discountFactor = 0.9
    learningRate = 1

    trainingEstimator = Model.GetModel(modelToSavePath + "_trainning")
    targetEstimator = Model.GetModel(modelToSavePath)

    Model.CreateModelIfDoesntExist(modelToSavePath + "_trainning", trainingEstimator)
    Model.CreateModelIfDoesntExist(modelToSavePath, targetEstimator)

    experienceContainer = ER.ExperienceContainer(10000)

    maxMovesCount = 10
    epochCount = 1000
    totalMoves = 0
    for epoch in range(epochCount):
        print('epoch:' + str(epoch))
        state = Game.CreateState(None, Game.Pos(1, 2), None)
        print(state)
        nbMoves = 0
        tooManyMoves = False
        while (not (state.IsFinished() or tooManyMoves)):
            nbMoves += 1
            totalMoves += 1

            action = Exploration.GetNextActionBoltzmann(Model.GetQValue(state, targetEstimator), epoch, epochCount)
            print(str(action) + '\n')

            nextState = Game.Move(state, action)

            experienceContainer.Add(state, action, nextState.GetReward(), nextState)

            state = nextState

            tooManyMoves = nbMoves == maxMovesCount

            print(state if not tooManyMoves else 'lost because did too many moves')

            if totalMoves % 5 == 0:
                Model.TrainModelWithExperienceReplay(experienceContainer, trainingEstimator, targetEstimator, discountFactor, learningRate)

            if totalMoves % 25 == 0:
                targetEstimator = trainingEstimator

    OverrideDir(modelToSavePath, modelToSavePath + "_trainning")

modelPath = 'models/model'
CreateAndTrainModel(modelPath)
