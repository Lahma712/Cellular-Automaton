# Conway-s-Game-of-Life

This is my Python implementation of the famous "Conway's Game of Life", which was discovered by the british mathematician <b>John Horton Conway</b> in 1970.
The game plays out on a 2D plane and is based on a 2D cellular automaton (see automata theory by <b>Stanislaw Marcin Ulam</b>). I implemented the GUI using Kivy 2.0.0
and PIL (Python Imaging Library).

# Instructions:

<b>Download the lastest release</b> and follow the install instructions <b>or download the source code</b> and run <i>GOL.py</i> from an IDE

- Draw a shape on the plane by clicking and moving the mouse cursor.
- To erase a drawn cell, click on it again.
- To start the automaton, click on the "Start" button (you can also pause by clicking on it again).
- To zoom in/out, click on the "zoom in"/"zoom out" buttons.
- To erase everything, click on the "clear" button. 

<img src= "https://media.giphy.com/media/cD0W6gHurzo0i3VShF/giphy.gif" width=500>

(framerate/quality loss due to GIF conversion) 

# How it works:

The rules are very simple. You begin by drawing some cells onto the grid (in some arbitrary shape). 

Each cell can either be "alive" or "dead". There are 4 rules:

- A dead cell with exactly 3 living neighbours becomes alive
- A living cell with less than 2 neighbours dies out of isolation
- A living cell with more than 3 neighbours dies out of overcrowding
- A living cell with 2 or 3 neighbours stays alive

The cells which you draw are considered to be "alive" (red cells). After starting the automaton, with each frame, the state of every cell is updated according to the 4 rules 
described above.

# Changing the ruleset:

You can also change the ruleset by changing the <b><i>survival rule</i></b> and/or <b><i>birth rule</i></b>. Playing around with the ruleset can give rise to interesting results!

- Survival rule: Number of neighbouring cells a live cell must have in order to survive. The default is set to <b>3 or 2</b>
- Birth rule: Number of neighbouring cells a dead cell must have in order to become alive. The default is set to <b>3</b>

Note on syntax: The numbers have to be entered in a concatenated form, f.ex if the survival rule is <b>3 or 2</b>, you enter it as <b>32</b>
# Dependencies:

-Python 3.x

-Kivy 2.0.0

-PIL (Python Imaging Library)

# Sources:
- https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
