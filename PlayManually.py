import Game

class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

def GetActionFromKeyBoard():
    try:
        print('Do an action (4:Left 6:right 8:up 5: down):')
        actionInt=int(getch())

        action = Game.Action.Left
        if actionInt == 4:
            action = Game.Action.Left
        elif actionInt == 6:
            action = Game.Action.Right
        elif actionInt == 8:
            action = Game.Action.Up
        elif actionInt == 5:
            action = Game.Action.Down
        else:
            raise ValueError(str(actionInt) + ' is an invalid input')

        return action
    except ValueError as err:
        print(err.args)
        return GetActionFromKeyBoard()

def Play():
    state = Game.CreateState(None, None, None)
    print(state)

    maxMovesCount = 5
    nbMoves = 0
    while (not state.IsFinished()):
        if nbMoves == maxMovesCount:
            print('lost because did too many moves')
            return

        action = GetActionFromKeyBoard()
        print(str(action) + '\n')
        state.Move(action)
        print(state)
        nbMoves += 1

Play()
