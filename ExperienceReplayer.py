import collections
import random

class Experience:
    def __init__(self, state, action, reward, nextState):
        self.m_State = state
        self.m_Action = action
        self.m_Reward = reward
        self.m_NextState = nextState

    def __repr__(self):
        return "Experience: \n" + str(self.m_State) + "\n" + str(self.m_Action) + "\n" + str(self.m_Reward) + "\n" + str(self.m_NextState)

class ExperienceContainer:
    def __init__(self, size):
        self.m_Experiences = collections.deque(maxlen=size)

    def Add(self, state, action, reward, nextState):
        self.m_Experiences.append(Experience(state, action, reward, nextState))

    def GetRandomSample(self, sampleSize):
        nSamples = min(len(self.m_Experiences), sampleSize)
        return random.sample(self.m_Experiences, nSamples)

    def __repr__(self):
        return str(self.m_Experiences)