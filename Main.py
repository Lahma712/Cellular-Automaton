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
    Width = int(input("\nWindow width (in pixels): "))
    Height = int(input("\nWindow height (in pixels): "))
    time.sleep(1)
    Window.size = (Width, Height)
    CurrentCells = []

    def __init__(self,**kwargs):
        super(Drw, self).__init__(**kwargs)
        self.CellCount = 50
        with self.canvas:
            self.check = False
            self.Grids = Grid(self.CellCount, self.Width, self.Height)
            self.Cells = Cells(self.Grids[0], self.Grids[1])

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
        self.Grids = Grid(self.CellCount, self.Width, self.Height)
        self.Cells = Cells(self.Grids[0], self.Grids[1])
        self.CurrentCells = []
        
        with self.canvas:
            self.bg.reload()

    def Sub(self, instance):
        self.CellCount -= 1
        self.Grids = Grid(self.CellCount, self.Width, self.Height)
        self.Cells = Cells(self.Grids[0], self.Grids[1])
        self.CurrentCells = []
        
        with self.canvas:
            self.bg.reload()

    def AddClock(self, instance):
        self.event = Clock.schedule_interval(self.Add, 0.01)
        self.event()

    def AddClockCancel(self, instance):
        self.event.cancel()
    
    def SubClock(self, instance):
        self.event = Clock.schedule_interval(self.Sub, 0.01)
        self.event()

    def SubClockCancel(self, instance):
        self.event.cancel()

    def Draw(self, instance, X):
        self.XcellList = [x for x in self.Cells[0] if self.Xtouch+X in x][0]
        self.YcellList = [x for x in self.Cells[1] if self.Ytouch+X in x][0]
        self.cellIndexList = [self.Cells[0].index(self.XcellList), self.Cells[1].index(self.YcellList)]

        if self.cellIndexList not in self.CurrentCells:
            self.CurrentCells.append(self.cellIndexList)
            self.color = (255,0,0)
        elif self.checkSingleClick == True and self.cellIndexList in self.CurrentCells:
            self.CurrentCells.remove(self.cellIndexList)
            self.color = (0, 0,0)

        drawCell(self.XcellList,self.YcellList, self.color, r"C:\Users\{}\Desktop\Grid.png".format(host))
        with self.canvas:
            self.bg.reload()
        

    def onTouchFunctions(self, touch):
        self.touchpos = touch.pos
        self.Xtouch = math.floor(self.touchpos[0])
        self.Ytouch = math.floor(abs(self.touchpos[1]-self.Height))
        try:
            self.Draw(self, 0) 
            super(Drw, self).on_touch_down(touch) 

        except(IndexError):
            try:
                self.Draw(self, -1)
                super(Drw, self).on_touch_down(touch) 
            except(IndexError):
                super(Drw, self).on_touch_down(touch)

    def on_touch_down(self, touch):
        self.checkSingleClick = True
        self.onTouchFunctions(touch)

    def on_touch_move(self, touch):
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
        
        self.nextGen = nextGenLive(self.CurrentCells)
        self.deleteCells = self.nextGen[1]
        self.CurrentCells = self.nextGen[0]
        
        drawFrame(r"C:\Users\{}\Desktop\Grid.png".format(host), self.deleteCells, self.Cells, (0,0,0))
        drawFrame(r"C:\Users\{}\Desktop\Grid.png".format(host), self.CurrentCells, self.Cells, (255,0,0))
        
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
