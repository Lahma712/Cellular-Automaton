# Conway-s-Game-of-Life

This is my Python implementation of the famous "Conway's Game of Life", which was discovered by the british mathematician <b>John Horton Conway</b> in 1970.
The game plays out on a 2D plane and is based on a 2D cellular automaton (see automata theory by <b>Stanislaw Marcin Ulam</b>). I implemented the GUI using Kivy 2.0.0
and PIL (Python Imaging Library).

# <b>How to use: </b>

<b>Download the lastest release</b> and follow the instructions <b>or download the source code</b> and run the <i>GOL.py</i> from an IDE

- Draw a shape on the plane by clicking and moving the mouse cursor.
- To erase a drawn cell, click on it again.
- To start the automaton, click on the "Start" button (you can also pause by clicking on it again).
- To zoom in/out, click on the "zoom in"/"zoom out" buttons.
- To erase everything, click on the "clear" button. 

![gif](https://media.giphy.com/media/cD0W6gHurzo0i3VShF/giphy.gif)

(framerate/quality loss due to GIF conversion) 

# <b>How it works: </b>

The rules are very simple. You begin by drawing some cells onto the grid (in some arbitrary shape). 

Each cell can either be "alive" or "dead", depending on how many living neighbours it has:

- A dead cell with exactly 3 living neighbours becomes alive
- A living cell with less than 2 neighbours dies out of isolation
- A living cell with more than 3 neighbours dies out of overcrowding
- A living cell with 2 or 3 neighbours stays alive

The cells which you draw are considered to be "alive" (red cells). After starting the automaton, with each frame, the state of every cell is updated according to the 4 rules 
described above.


# <b>Dependencies:</b>

-Python 3.8

-Kivy 2.0.0

-PIL (Python Imaging Library)

# <b>Sources: </b>
- https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
