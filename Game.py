from enum import Enum
import copy
import random

class Action(Enum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3

class GameStatus(Enum):
    Playing = 0
    Won = 1
    Lost = 2

class CellContent(Enum):
    Player = 1
    Goal = 2
    Hole = 3
    Empty = 4

class Pos:
    def __init__(self, x, y):
        self.m_X = x
        self.m_Y = y

    def __eq__(self, other):
        if not other:
            return False

        return self.m_X == other.m_X and self.m_Y == other.m_Y

    def __repr__(self):
        return '[x=' + str(self.m_X) + ':y=' + str(self.m_Y) + ']'

class State:
    m_Height = 4
    m_Width = 3
        
    def __init__(self, playerPos, goalPos, holePos):
        self.m_GameStatus = GameStatus.Playing

        self.ValidateInputPos([playerPos, goalPos, holePos])

        self.m_PlayerPosition = playerPos
        self.m_GoalPosition = goalPos
        self.m_HolePosition = holePos 

    def ValidateInputPos(self, positions):
        posTaken = list()
        allPosUnique = not any(position in posTaken or posTaken.append(position) for position in positions)

        if not allPosUnique:
            raise ValueError('several input positions are identique. positions:' + str(positions))

    def GetGrid(self):
        grid = [[CellContent.Empty] * self.m_Width for _ in range(self.m_Height)]
        grid[self.m_PlayerPosition.m_Y][self.m_PlayerPosition.m_X] = CellContent.Player
        grid[self.m_GoalPosition.m_Y][self.m_GoalPosition.m_X] = CellContent.Goal
        grid[self.m_HolePosition.m_Y][self.m_HolePosition.m_X] = CellContent.Hole
        return grid

    def PrintField(self, position):
        if position == self.m_PlayerPosition:
            return "X";
        elif position == self.m_GoalPosition:
            return "1"
        elif position == self.m_HolePosition:
            return "O"
        else:
            return "-"

    def __repr__(self):
        if self.m_GameStatus == GameStatus.Playing:
            display = ''
            for y in range(self.m_Height):
                display += ' '.join(self.PrintField(Pos(x, y)) for x in range(self.m_Width))
                display += '\n'
            return display
        else:
            return self.m_GameStatus.name

    def GetReward(self):
        return {
            GameStatus.Won: 10,
            GameStatus.Lost: -10
        }.get(self.m_GameStatus, -1)

    def IsFinished(self):
        return self.m_GameStatus == GameStatus.Won or self.m_GameStatus == GameStatus.Lost
    
    def UpdatePos(self, action):
        if action == Action.Left:
            self.m_PlayerPosition.m_X = self.m_Width - 1 if self.m_PlayerPosition.m_X == 0 else self.m_PlayerPosition.m_X - 1
        elif action == Action.Right:
            self.m_PlayerPosition.m_X = (self.m_PlayerPosition.m_X + 1) % self.m_Width
        elif action == Action.Up:
            self.m_PlayerPosition.m_Y = self.m_Height - 1 if self.m_PlayerPosition.m_Y == 0 else self.m_PlayerPosition.m_Y - 1
        else:
            self.m_PlayerPosition.m_Y = (self.m_PlayerPosition.m_Y + 1) % self.m_Height

    def UpdateGameStatus(self):
        if self.m_PlayerPosition == self.m_GoalPosition:
            self.m_GameStatus = GameStatus.Won
        elif self.m_PlayerPosition == self.m_HolePosition:
            self.m_GameStatus = GameStatus.Lost

    def Move(self, action):
        self.UpdatePos(action)
        self.UpdateGameStatus()
        return self

def Move(state, action):
    nextState = copy.deepcopy(state)
    return nextState.Move(action)
    

def GetAvailableRandomPos(takenPos):
    while True:
        pos = Pos(random.choice(range(State.m_Width)), random.choice(range(State.m_Height)))
        if not any(p == pos for p in takenPos):
            return pos

def CreateState(optionalPlayerPos, optionalGoalPos, optionalHolePos):
    playerPos = optionalPlayerPos if optionalPlayerPos else GetAvailableRandomPos([optionalGoalPos, optionalHolePos])
    goalPos = optionalGoalPos if optionalGoalPos else GetAvailableRandomPos([playerPos, optionalHolePos])
    holePos = optionalHolePos if optionalHolePos else GetAvailableRandomPos([playerPos, goalPos])

    return State(playerPos, goalPos, holePos)