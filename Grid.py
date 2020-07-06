from PIL import Image, ImageDraw
import random
import getpass
host = getpass.getuser()
def Grid(hCellCount, Width, Height):
    Im = Image.new("RGB", (Width, Height), (0,0,0))
    draw = ImageDraw.Draw(Im)
    
    def contin(a, b, c, ExcessPixels, CellWidth, Axis, CellCount, C, counter, intv): #fuction that continues the algorithm with parameters given from the init function
        C += CellWidth+a
        Axis += [C]
        for _ in range(ExcessPixels-1): #loop that places pixels with adjusted distance due to excess pixels ('b' is +1 or +0 depending if number of Excesspixels is less/more than half number of cells)
            C += CellWidth+b
            Axis += [C]
            counter -= 1
            for _ in range(intv): #loop that places pixels with normal distance (without adjusted distance due to excesspixels)
                C += CellWidth+c
                Axis += [C]
                counter -= 1
        for _ in range(counter-1): #loop that places rest of grid pixels once there are no more excesspixels
            C += CellWidth+c
            Axis += [C]
        return


    def init(a, b, c , d, ExcessPixels, CellWidth, Axis, CellCount, C, counter):
        try:
            intv = abs((CellCount - ExcessPixels)//(ExcessPixels-1)) #interval, excesspixel comes every intv'th pixel
            if intv == CellCount: #if excessspixels = 0
                    contin(a, 99, c, ExcessPixels, CellWidth, Axis, CellCount, C, counter, intv) # second position '99' doesnt play any role here
                    return
        except: #if excesspixels = 1
            intv = abs((CellCount - 1))
            contin(b, 99, c, ExcessPixels, CellWidth, Axis, CellCount, C, counter, intv)
            return
        contin(b, d, c, ExcessPixels, CellWidth, Axis, CellCount, C, counter, intv) #if excesspixels not 0 and not 1
        return


    def grid(Axis, CellCount, CellWidth, ExcessPixels):
        C = 0  # counter for grid pixel position
        counter = CellCount
        if ExcessPixels > CellCount//2: #checks if excesspixels are more than half the number of cells
            ExcessPixels = CellCount - ExcessPixels
            init(-2, -1, 1, 0, ExcessPixels, CellWidth, Axis, CellCount, C, counter)
        else: # if excesspixels are less than half the number of cells
            init(-1, 0, 0, 1, ExcessPixels, CellWidth, Axis, CellCount, C, counter)

   
    def Draw(a, b, color): #draws pixels on image
        for y in b:
            for x in a:
                draw.point([x, y], color)

    hCellWidth = Width // hCellCount  # Pixel width per cell (horizontal pixels)
    hExcessPixels = Width % hCellCount #excess pixels if there is a rest
    vCellCount = Height // hCellWidth  # number of vertical cells
    vCellWidth = Height // vCellCount  # Pixel height per cell (vertical pixels)
    vExcessPixels = Height % vCellCount
    HGrid = [0]
    VGrid = [0]
    
    gcolor = (50,50,50)
    grid(HGrid, vCellCount, vCellWidth, vExcessPixels)
    grid(VGrid, hCellCount, hCellWidth, hExcessPixels)
    
    Draw(range(Width), HGrid, gcolor)
    Draw(VGrid, range(Height), gcolor)
   
    Im.save(r"C:\Users\{}\Desktop\Grid.png".format(host))
    return HGrid, VGrid, vCellCount
