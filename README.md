# Othello Game Agent
Implementation of the ``Minimax`` decision algorithm with ``Alpha-beta pruning`` optimization for Othello/Reversi, in Python, as a console application. <br />
Both ``AI vs AI`` and ``AI vs Human`` options are available.

## About Othello
Reversi is a strategy board game for two players, played on an 8×8 uncheckered board. Othello is a variant with a fixed initial setup of the board.<br />
<img src="https://www.activitytailor.com/wp-content/uploads/2011/07/othello2.jpg" width="300" /> <br />
There are sixty-four identical game pieces called disks, which are light on one side and dark on the other. <br />
Players take turns placing disks on the board with their assigned color facing up. During a play, any disks of the opponent's color that are in a straight line and bounded by the disk just placed and another disk of the current player's color are turned over to the current player's color. <br />
The objective of the game is to have the majority of disks turned to display one's color when the last playable empty square is filled. <br />
<sub>This and more on [Wikipedia](https://en.wikipedia.org/wiki/Reversi) :wink:</sub>

## Implementation
The project contains custom implementations of later used data structures:
- Map
- HashMap
- Queue
- Tree

``state.py`` - Each state is represented by the board (8x8 matrix) and num (holds the number of black and white pieces on the board saved for that state). Board fields can have one of three values:
- '-' - empty slot
- 'B' - black disk
- 'W' - white disk

Functions for fetching and playing legal moves for the said state are also implemented here.

``game_without_hash.py`` - First variant of the main project file. It contains implementation of the min and max functions for plating min/max player's moves, as well as the heuristic function used for evaluating each state. Current version is AI vs AI, but it can easily be switched so that the second player is human (the human player code is commented out).

``game.py`` - Second variant of the main project file. It's the same as game_without_hash.py, with the only difference being the added hashmap optimization - before evaluating a state, we check if the state has already been evaluated in some of the previous simulations - if so, no need to eval again, if not, we evaluate it and sasve it in the hashmap for future use.

## Running the code
Aside from the ``time`` lib used for calculating the speed with wich AI decides on its move and ``random`` used for the HashMap implementation, no external libraries were used. <br />
Simply run the ``game.py`` or ``game_without_hash.py`` to get the console app going 😃
<br />
<br />

**copyrighted by me**
