import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import time
from Grid import Grid
from Cells import Cells
from Cells import drawCell
from Cells import nextGenLive
from Cells import drawFrame
from line_profiler import LineProfiler
import os
import PIL
import getpass
import math
import random
host = getpass.getuser()
kivy.require("1.11.1")


class Drw(Widget):
    Width = int(input("\n\nWindow width (in pixels): "))
    Height = int(input("\nWindow height (in pixels): "))
    time.sleep(1)
    Window.size = (Width, Height)
    CurrentCells = [] #holds current live cells of the frame in form of columns/rows. 2D list e.g [[0,0], [4,5], .... , [column, row]]
    deleteCells = [] 
    def __init__(self,**kwargs):
        super(Drw, self).__init__(**kwargs)
        self.CellCount = 50 #initial number of columns
        with self.canvas:
            self.check = False
            self.Grids = Grid(self.CellCount, self.Width, self.Height) #2D list of grid pixel coordinates eg [[0, 50, 100], [0, 100, 200]]. 1 List for x coordinates and 1 for y coordinates
            self.Cells = Cells(self.Grids[0], self.Grids[1]) #3D list of all the cell coordinates eg [ [[0,1,2,3], [5, 6, 7]....], [[0,1,2,3,4], [6,7,8,9]....] . 1st list holds x coordinate lists and 2nd list y coordinate lists

            self.bg = Image(source= r"C:\Users\{}\Desktop\Grid.png".format(host), pos=(0,0), size = (self.Width, self.Height))
            
            self.add = Button(text = "zoom out", font_size =self.Height*0.05, size= (self.Width * 0.25, self.Height*0.10), pos = (0, 0))
            self.sub = Button(text="zoom in", font_size=self.Height*0.05, size= (self.Width * 0.25, self.Height*0.10), pos=(self.Width - self.Width * 0.25, 0))
            
            self.add.bind(on_press= self.AddClock)
            self.add.bind(on_release = self.AddClockCancel)
            self.sub.bind(on_press = self.SubClock)
            self.sub.bind(on_release = self.SubClockCancel)
            self.add_widget(self.sub)
            self.add_widget(self.add)

            self.start = Button(text="start", font_size=self.Height*0.05, size = (self.Width * 0.25, self.Height*0.10), pos=(self.Width - 2.5*(self.Width * 0.25), 0))
            self.start.bind(on_press = self.StartClock)
            self.add_widget(self.start)

    def Add(self, instance):

        self.CellCount += 1
        self.Grids = Grid(self.CellCount, self.Width, self.Height) #new grid dataset is made when zoomed out
        self.Cells = Cells(self.Grids[0], self.Grids[1]) #new cell dataset is made when zoomed out 
        drawFrame(r"C:\Users\{}\Desktop\Grid.png".format(host), self.CurrentCells, self.Cells, (255,0,0))
        drawFrame(r"C:\Users\{}\Desktop\Grid.png".format(host), self.deleteCells, self.Cells, (0,0,0))
        with self.canvas:
            self.bg.reload()

    def Sub(self, instance):
        self.CellCount -= 1
        self.Grids = Grid(self.CellCount, self.Width, self.Height)#new grid dataset is made when zoomed in
        self.Cells = Cells(self.Grids[0], self.Grids[1])#new cell dataset is made when zoomed in
        drawFrame(r"C:\Users\{}\Desktop\Grid.png".format(host), self.CurrentCells, self.Cells, (255,0,0))
        drawFrame(r"C:\Users\{}\Desktop\Grid.png".format(host), self.deleteCells, self.Cells, (0,0,0))
        with self.canvas:
            self.bg.reload()

    def AddClock(self, instance):
        self.event = Clock.schedule_interval(self.Add, 0.01) #starts clock to continually zoom out
        self.event()

    def AddClockCancel(self, instance):
        self.event.cancel() #cancels clock when you release the button
    
    def SubClock(self, instance):
        self.event = Clock.schedule_interval(self.Sub, 0.01)#starts clock to continually zoom in
        self.event()
        self.event()

    def SubClockCancel(self, instance):
        self.event.cancel()#cancels clock when you release the button

    def Draw(self, instance, X):
        self.XcellList = [x for x in self.Cells[0] if self.Xtouch+X in x][0] #finds the pixel X coordinates list containing the X coordinate you clicked with the mouse 
        self.YcellList = [x for x in self.Cells[1] if self.Ytouch+X in x][0]#finds the pixel Y coordinates list containing the Y coordinate you clicked with the mouse 
        self.cellIndexList = [self.Cells[0].index(self.XcellList), self.Cells[1].index(self.YcellList)] # produces a column/row list [column, row] of the cell you clicked with the mouse

        if self.cellIndexList not in self.CurrentCells: #checks if the cell you clicked is already clicked, if not the [column, pair] gets added to CurrentCells and the cell gets colored
            self.CurrentCells.append(self.cellIndexList)
            self.color = (255,0,0)
        elif self.checkSingleClick == True and self.cellIndexList in self.CurrentCells: #if you only clicked once, and on a cell that is already clicked/activated, it gets erased again
            self.CurrentCells.remove(self.cellIndexList)
            self.color = (0, 0,0)

        drawCell(self.XcellList,self.YcellList, self.color, r"C:\Users\{}\Desktop\Grid.png".format(host)) #function that draws (or erases, based on the previous conditions) the cell you clicked
        with self.canvas:
            self.bg.reload()
        

    def onTouchFunctions(self, touch):
        self.touchpos = touch.pos #tuple that contains the X/Y coords of your mouse click
        self.Xtouch = math.floor(self.touchpos[0]) #rounds the coords down
        self.Ytouch = math.floor(abs(self.touchpos[1]-self.Height)) #inverts the Y coord. In kivy the origin (0,0) is bottom left, in PIL it is top left
        try: 
            self.Draw(self, 0) 
            super(Drw, self).on_touch_down(touch) 

        except(IndexError): #if you press exactly on a grid pixel (in between 2 cells), you would get an Index error. In that case, just move your mouseclick 1 pixel up and left
            try:
                self.Draw(self, -1)
                super(Drw, self).on_touch_down(touch) 
            except(IndexError): #if you press on a grid pixel at the border of the window, just do nothing
                super(Drw, self).on_touch_down(touch)

    def on_touch_down(self, touch): #function if you only click once
        self.checkSingleClick = True
        self.onTouchFunctions(touch)

    def on_touch_move(self, touch): #function if you click once and then start moving (with button still pressed). Is used for drawing lines 
        self.checkSingleClick = False
        self.onTouchFunctions(touch)

    def StartClock(self, instance): 
        if self.check == True:
            self.Startevent.cancel()
            self.check = False
        
        else:
            self.Startevent = Clock.schedule_interval(self.Start, 0.1)
            self.check = True
            self.Startevent()

    def Start(self, instance):
        
        self.nextGen = nextGenLive(self.CurrentCells) #creates the next generation of live cells based on CurrentCells + list of cells which die in the next generation
        self.deleteCells = self.nextGen[1]
        self.CurrentCells = self.nextGen[0]
        
        drawFrame(r"C:\Users\{}\Desktop\Grid.png".format(host), self.deleteCells, self.Cells, (0,0,0)) #deletes cells
        drawFrame(r"C:\Users\{}\Desktop\Grid.png".format(host), self.CurrentCells, self.Cells, (255,0,0)) #creates cells
        
        with self.canvas:
            self.bg.reload()
        return
    
class G0L(App):
    def build(self):
        return Drw()

if __name__ == "__main__":
    G0L().run()
    os.remove(r"C:\Users\{}\Desktop\Grid.png".format(host)) 


# profiler = LineProfiler()
# profiler_wrapper = profiler()
# profiler_wrapper()
# profiler.print_stats()
