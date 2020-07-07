from Grid import Grid
from PIL import Image, ImageDraw
import getpass
host = getpass.getuser()

def Cells(HGrid, VGrid): #function that creates dataset of the XY coords of every cell
	def cells(grid, Cells):
		for x in range(len(grid)-1):
			cell = [y for y in range(grid[x]+1, grid[x+1])]
			Cells.append(cell)
	
	XCells = []
	YCells = []
	cells(HGrid, YCells)
	cells(VGrid, XCells)
	return XCells, YCells
	
def drawCell(X,Y, color, source): #function that draws a single cell when you click on one

	Im = Image.open(source)
	draw = ImageDraw.Draw(Im)
	for y in Y:
		for x in X:
			draw.point([x, y], color)
	Im.save(r"C:\Users\{}\Desktop\Grid.png".format(host))

def drawFrame(source, currentCells, cells, color): #function that draws the frames when the game is running
	Im = Image.open(source)
	draw = ImageDraw.Draw(Im)
	
	for cellIndex in currentCells:
		try:
			for y in cells[1][cellIndex[1]]:
				for x in cells[0][cellIndex[0]]:
					draw.point([x, y], color)
		except:
			pass
			
	Im.save(r"C:\Users\{}\Desktop\Grid.png".format(host))

	return

def nextGenLive(CurrentCells): #function that creates the new CurrentCells, so the next generation of cells
	global nextGen
	nextGen = []
	nextGenDel = []
	neighbours = []
	
	for cell in CurrentCells:
		numLiveCells = 0
		
		if [cell[0]+1, cell[1]] in CurrentCells:
			numLiveCells +=1
		elif [cell[0]+1, cell[1]] not in neighbours:
			neighbours += [[cell[0]+1, cell[1]]]

		if [cell[0]-1, cell[1]] in CurrentCells:
			numLiveCells +=1
		elif [cell[0]-1, cell[1]] not in neighbours:
			neighbours += [[cell[0]-1, cell[1]]]


		if [cell[0], cell[1]+1] in CurrentCells:
			numLiveCells +=1
		elif [cell[0], cell[1]+1] not in neighbours:
			neighbours += [[cell[0], cell[1]+1]]

		if [cell[0], cell[1]-1] in CurrentCells:
			numLiveCells +=1
		elif [cell[0], cell[1]-1] not in neighbours:
			neighbours += [[cell[0], cell[1]-1]]

		if [cell[0]+1, cell[1]+1] in CurrentCells:
			numLiveCells +=1
		elif [cell[0]+1, cell[1]+1] not in neighbours:
			neighbours += [[cell[0]+1, cell[1]+1]]
		
		if [cell[0]+1, cell[1]-1] in CurrentCells:
			numLiveCells +=1
		elif [cell[0]+1, cell[1]-1] not in neighbours:
			neighbours += [[cell[0]+1, cell[1]-1]]
		
		if [cell[0]-1, cell[1]+1] in CurrentCells:
			numLiveCells +=1
		elif [cell[0]-1, cell[1]+1] not in neighbours:
			neighbours += [[cell[0]-1, cell[1]+1]]

		
		if [cell[0]-1, cell[1]-1] in CurrentCells:
			numLiveCells +=1
		elif [cell[0]-1, cell[1]-1] not in neighbours:
			neighbours += [[cell[0]-1, cell[1]-1]]	
		
		
		if (numLiveCells == 2 or numLiveCells == 3) and cell not in nextGen:
			nextGen += [cell]

		if numLiveCells > 3 or numLiveCells < 2:
			nextGenDel += [cell]
	

	for Cell in neighbours:
		NumLiveCells = 0
		if [Cell[0]+1, Cell[1]] in CurrentCells:
			NumLiveCells +=1

		if [Cell[0]-1, Cell[1]] in CurrentCells:
			NumLiveCells +=1

		if [Cell[0], Cell[1]+1] in CurrentCells:
			NumLiveCells +=1

		if [Cell[0], Cell[1]-1] in CurrentCells:
			NumLiveCells +=1

		if [Cell[0]+1, Cell[1]+1] in CurrentCells:
			NumLiveCells +=1

		if [Cell[0]+1, Cell[1]-1] in CurrentCells:
			NumLiveCells +=1

		if [Cell[0]-1, Cell[1]+1] in CurrentCells:
			NumLiveCells +=1

		if [Cell[0]-1, Cell[1]-1] in CurrentCells:
			NumLiveCells +=1
		
		if NumLiveCells == 3 and Cell not in nextGen:
			nextGen += [Cell]


	return nextGen, nextGenDel
