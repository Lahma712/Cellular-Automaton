import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image as Bg
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
from kivy.clock import Clock
from Grid import Grid
from Cells import Cells
from Cells import drawCell
from Cells import nextGenLive
from Cells import drawFrame
from PIL import Image, ImageDraw
import math
from io import BytesIO
kivy.require("2.0.0")

class Drw(Widget):
    Width = 500
    Height = 500
    Window.size = (Width*1.5, Height)
    GWidth = int(Width) 
    GHeight = int(Height * 0.9) #grid height is a little bit shorter than the full window size because of the buttons 
    CurrentCells = [] #holds current live cells of the frame in form of columns/rows. 2D list e.g [[0,0], [4,5], .... , [column, row]]
    deleteCells = []
    survRule = [3,2] #survivl rule: number of neighbours a cell must have to survive
    birthRule= [3] #birth rule: number of neighbours a dead cell must have in order to become alive
    BgColor = (0,0,0)
    GridColor = (20,20,20)
    CellColor = (255,0,0)

    Im = Image.new("RGB", (GWidth, GHeight), BgColor)
    byte_io = BytesIO()
    Im.save(byte_io, 'PNG')
    
    def __init__(self,**kwargs):
        super(Drw, self).__init__(**kwargs)
        self.CellCount = 50 #initial number of columns
        with self.canvas:
            self.check = False
            self.Im = Image.open(self.byte_io)
            self.draw = ImageDraw.Draw(self.Im)
            self.Grids = Grid(self.CellCount, self.GWidth, self.GHeight, self.draw, self.GridColor) #2D list of grid pixel coordinates eg [[0, 50, 100], [0, 100, 200]]. 1 List for x coordinates and 1 for y coordinates
            self.Cells = Cells(self.Grids[0], self.Grids[1]) #3D list of all the cell coordinates eg [ [[0,1,2,3], [5, 6, 7]....], [[0,1,2,3,4], [6,7,8,9]....] . 1st list holds x coordinate lists and 2nd list y coordinate lists
            self.byte_io = BytesIO()
            self.Im.save(self.byte_io, 'PNG')
            self.bg = Bg(texture = self.ImageByte(self, self.byte_io.getvalue()).texture, pos=(0, self.Height * 0.1), size = (self.GWidth, self.GHeight)) #background
            
            self.add = Button(text = "zoom out", font_size =self.Height*0.05, size= (self.Width * 0.25, self.Height*0.10), pos = (0, 0))
            self.sub = Button(text="zoom in", font_size=self.Height*0.05, size= (self.Width * 0.25, self.Height*0.10), pos=(self.Width - 0.75*self.Width, 0))
            
            self.add.bind(on_press= self.AddClock)
            self.add.bind(on_release = self.ClockCancel)
            self.sub.bind(on_press = self.SubClock)
            self.sub.bind(on_release = self.ClockCancel)
            self.add_widget(self.sub)
            self.add_widget(self.add)

            self.start = Button(text="start", font_size=self.Height*0.05, size = (self.Width * 0.25, self.Height*0.10), pos=(self.Width - 0.50*self.Width, 0))
            self.start.bind(on_press = self.StartClock)
            self.add_widget(self.start)

            self.clear = Button(text="clear", font_size=self.Height*0.05, size = (self.Width *0.25, self.Height*0.10), pos =(self.Width - 0.25*self.Width, 0))
            self.clear.bind(on_press = self.Clear)
            self.add_widget(self.clear)
            
            self.SurvLabel = Label(text = "Survival Rule: ", pos = (550, 450), size = (0,0))
            self.BirthLabel = Label(text = "Birth Rule: ", pos = (540, 400), size = (0,0))

            self.SurvInput = TextInput(text = "32", pos = (600, 440), size = (90,27), font_size = 13)
            self.BirthInput = TextInput(text = "3", pos = (600, 390), size = (90,27), font_size = 13)
            self.add_widget(self.SurvInput)
            self.add_widget(self.BirthInput)
            self.survRule = [int(x) for x in self.SurvInput.text]
            self.birthRule = [int(x) for x in self.BirthInput.text]

    def ImageByte(self, instance, ImageByte):
        self.Buffer = BytesIO(ImageByte)
        self.BgIm = CoreImage(self.Buffer, ext= 'png')
        return self.BgIm

    def save(self, instance):
        self.byte_io = BytesIO()
        self.Im.save(self.byte_io, 'PNG')
        with self.canvas:
            self.bg.texture = self.ImageByte(self, self.byte_io.getvalue()).texture

    def AddSub(self, instance):
        self.Im = Image.new("RGB", (self.GWidth, self.GHeight), self.BgColor)
        self.draw = ImageDraw.Draw(self.Im)
        self.byte_io = BytesIO()
        self.Im.save(self.byte_io, 'PNG')
        try:
            self.Grids = Grid(self.CellCount, self.GWidth, self.GHeight, self.draw, self.GridColor)#new grid dataset is made when zoomed in
            self.Cells = Cells(self.Grids[0], self.Grids[1])#new cell dataset is made when zoomed in
            drawFrame(self.draw, self.CurrentCells, self.Cells, self.CellColor)
            drawFrame(self.draw, self.deleteCells, self.Cells, self.BgColor)
        except:
            pass
        self.save(self)

    def Add(self, instance):
        self.CellCount += 1
        self.AddSub(self)

    def Sub(self, instance):
        self.CellCount -= 1
        self.AddSub(self)
        
    def AddClock(self, instance):
        self.event = Clock.schedule_interval(self.Add, 0.01) #starts clock to continually zoom out
        self.event()

    def SubClock(self, instance):
        self.event = Clock.schedule_interval(self.Sub, 0.01)#starts clock to continually zoom in
        self.event()

    def ClockCancel(self, instance):
        self.event.cancel()#cancels clock when you release the button

    def Draw(self, instance, X):
        self.XcellList = [x for x in self.Cells[0] if self.Xtouch+X in x][0] #finds the pixel X coordinates list containing the X coordinate you clicked with the mouse 
        self.YcellList = [x for x in self.Cells[1] if self.Ytouch+X in x][0]#finds the pixel Y coordinates list containing the Y coordinate you clicked with the mouse 
        self.cellIndexList = [self.Cells[0].index(self.XcellList), self.Cells[1].index(self.YcellList)] # produces a column/row list [column, row] of the cell you clicked with the mouse

        if self.cellIndexList not in self.CurrentCells: #checks if the cell you clicked is already clicked, if not the [column, pair] gets added to CurrentCells and the cell gets colored
            self.CurrentCells.append(self.cellIndexList)
            self.color = self.CellColor
        elif self.checkSingleClick == True and self.cellIndexList in self.CurrentCells: #if you only clicked once, and on a cell that is already clicked/activated, it gets erased again
            self.CurrentCells.remove(self.cellIndexList)
            self.color = self.BgColor
        drawCell(self.XcellList,self.YcellList, self.color, self.draw) #function that draws (or erases, based on the previous conditions) the cell you clicked
        self.save(self)
        

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
        self.survRule = [int(x) for x in self.SurvInput.text]
        self.birthRule = [int(x) for x in self.BirthInput.text]
        if self.check == True:
            self.Startevent.cancel()
            self.check = False
        
        else:
            self.Startevent = Clock.schedule_interval(self.Start, 0.07)
            self.check = True
            self.Startevent()

    def Start(self, instance):

        self.nextGen = nextGenLive(self.CurrentCells, len(self.Cells[0])-1, len(self.Cells[1])-1, self.survRule, self.birthRule) #creates the next generation of live cells based on CurrentCells + list of cells which die in the next generation
        self.deleteCells = self.nextGen[1]
        self.CurrentCells = self.nextGen[0]
        drawFrame(self.draw, self.deleteCells, self.Cells, self.BgColor) #deletes cells
        drawFrame(self.draw, self.CurrentCells, self.Cells, self.CellColor) #creates cells
        self.save(self)
        

    def Clear(self, instance): #clears grid
        self.deleteCells = []
        self.CurrentCells =[]
        self.Img = Image.new("RGB", (self.GWidth, self.GHeight), self.BgColor)
        self.byte_io = BytesIO()
        self.Img.save(self.byte_io, 'PNG')
        self.Im = Image.open(self.byte_io)
        self.draw = ImageDraw.Draw(self.Im)
        self.Grids = Grid(self.CellCount, self.GWidth, self.GHeight, self.draw, self.GridColor) #2D list of grid pixel coordinates eg [[0, 50, 100], [0, 100, 200]]. 1 List for x coordinates and 1 for y coordinates
        self.Cells = Cells(self.Grids[0], self.Grids[1]) #3D list of all the cell coordinates eg [ [[0,1,2,3], [5, 6, 7]....], [[0,1,2,3,4], [6,7,8,9]....] . 1st list holds x coordinate lists and 2nd list y coordinate lists
        self.Im.save(self.byte_io, 'PNG')
        self.save(self)

        try:
            self.Startevent.cancel()
        except:
            pass
        self.check = False
    
class G0L(App):
    def build(self):
        return Drw()

if __name__ == "__main__":
    G0L().run()
    



