import tensorflow as tf

from functools import partial
import os
import numpy as np

import Game

def train_input_fn(features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    return dataset.shuffle(1000).repeat().batch(batch_size)

def eval_input_fn(features):
    dataset = tf.data.Dataset.from_tensor_slices(dict(features))
    return dataset.batch(1)

def GetFeatures(state):
    grid = state.GetGrid()
    features = {
        'Grid': [[col.value for row in grid for col in row]]
    }
    return features

def GetFeaturesFromList(states):
    grids = [state.GetGrid() for state in states]

    features = {
        'Grid': [[col.value for row in grid for col in row] for grid in grids]
    }
    return features

def GetLabels(expectedResult):
    labels = [[
        expectedResult[Game.Action.Left.value], 
        expectedResult[Game.Action.Right.value], 
        expectedResult[Game.Action.Up.value], 
        expectedResult[Game.Action.Down.value]
    ]]
    return labels

def GetLabelsFromList(expectedResults):
    labels = []
    for expectedResult in expectedResults:
        labels += GetLabels(expectedResult)
    return labels


def GetQValue(state, estimator):
    features = GetFeatures(state)

    predictions = estimator.predict(
        input_fn=lambda:eval_input_fn(features))

    return list(predictions)[0]['predictions']

def GetUpdatedQValue(state, action, reward, nextState, trainingEstimator, targetEstimator, discountFactor, learningRate):
    QVal = GetQValue(state, trainingEstimator)

    nextQVal = 0
    if (not nextState.IsFinished()):
        trainningQVal = GetQValue(nextState, trainingEstimator)
        bestTrainningAction = np.argmax(trainningQVal)
        targetQVals = GetQValue(nextState, targetEstimator)
        nextQVal = targetQVals[bestTrainningAction]

    QVal[action.value] = QVal[action.value] + learningRate * (reward + (discountFactor * nextQVal) - QVal[action.value])
    return QVal

def TrainModel(state, expectedResult, estimator):
    features = GetFeatures(state)
    labels = GetLabels(expectedResult)

    estimator.train(
        input_fn=lambda:train_input_fn(features, labels, 1),
        steps=500)

def TrainModelWithExperienceReplay(experienceContainer, trainingEstimator, targetEstimator, discountFactor, learningRate):
    print("TrainModelWithExperienceReplay")
    batchSize = 30

    sampleExperiences = experienceContainer.GetRandomSample(batchSize)

    states = [experience.m_State for experience in sampleExperiences]

    expectedResults = [GetUpdatedQValue(experience.m_State, experience.m_Action, experience.m_Reward, experience.m_NextState, trainingEstimator, targetEstimator, discountFactor, learningRate) for experience in sampleExperiences]

    features = GetFeaturesFromList(states)
    labels = GetLabelsFromList(expectedResults)

    trainingEstimator.train(
        input_fn=lambda:train_input_fn(features, labels, batchSize),
        steps=500)

def GetModel(modelPath):
    my_feature_columns = []
    my_feature_columns.append(tf.feature_column.numeric_column(key='Grid', shape=12))

    estimator = tf.estimator.DNNRegressor(
        feature_columns=my_feature_columns,
        hidden_units=[100, 100],
        label_dimension=4,
        model_dir=modelPath)

    return estimator

def CreateModelIfDoesntExist(modelToSavePath, estimator):
    if not os.path.isdir(modelToSavePath):
        print("Create model: " + modelToSavePath)
        TrainModel(Game.CreateState(None, None, None), [0, 0, 0, 0], estimator)