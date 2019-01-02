## Overview

Implementation of a simple game along with an AI agent, able to learn to play the game.  
The AI agent is an implementation of a Deep-Q-Network using TensorFlow.  

## Game's rule

In this game, our character has to move in a 2D grid in order to find the goal while avoiding to fall in the hole.  
In this grid, the character can either move up/down/right/left. Moving toward the edge of the grid moves the character on the other side of the grid.  

exemple of grid:  
X&nbsp;-&nbsp;&nbsp;-  
\-&nbsp;&nbsp;-&nbsp;&nbsp;-  
\-&nbsp;&nbsp;O&nbsp;-  
\-&nbsp;&nbsp;-&nbsp;&nbsp;1  
  
X: character  
0: hole  
1: goal  
