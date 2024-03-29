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


def drawCell(X,Y, color, draw): #function that draws a single cell when you click on one
	for y in Y:
		for x in X:
			draw.point([x, y], color)
	

def drawFrame(draw, currentCells, cells, color): #function that draws the frames when the game is running
	for cellIndex in currentCells:
		try:
			for y in cells[1][cellIndex[1]]:
				for x in cells[0][cellIndex[0]]:
					draw.point([x, y], color)
		except:
			pass
	return

def nextGenLive(CurrentCells, Xedge, Yedge, survRule, birthRule): #function that creates the new CurrentCells, so the next generation of cells
	global nextGen
	nextGen = []
	nextGenDel = []
	neighbours = []
	
	for cell in CurrentCells:
		numLiveCells = 0

		if cell[0] != Xedge: #the first if conditions check if the cell is on the X or Y edge of the screen
			if [cell[0]+1, cell[1]] in CurrentCells:
				numLiveCells +=1
			elif [cell[0]+1, cell[1]] not in neighbours:
				neighbours += [[cell[0]+1, cell[1]]]

		if cell[0] != 0:
			if [cell[0]-1, cell[1]] in CurrentCells:
				numLiveCells +=1
			elif [cell[0]-1, cell[1]] not in neighbours:
				neighbours += [[cell[0]-1, cell[1]]]

		if cell[1] != Yedge:
			if [cell[0], cell[1]+1] in CurrentCells:
				numLiveCells +=1
			elif [cell[0], cell[1]+1] not in neighbours:
				neighbours += [[cell[0], cell[1]+1]]

		if cell[1] != 0:
			if [cell[0], cell[1]-1] in CurrentCells:
				numLiveCells +=1
			elif [cell[0], cell[1]-1] not in neighbours:
				neighbours += [[cell[0], cell[1]-1]]

		if cell[0] != -1 and cell[0] != Xedge and cell[1] != Yedge:
			if [cell[0]+1, cell[1]+1] in CurrentCells:
				numLiveCells +=1
			elif [cell[0]+1, cell[1]+1] not in neighbours:
				neighbours += [[cell[0]+1, cell[1]+1]]

		if cell[1] != 0 and cell[0] != Xedge:
			if [cell[0]+1, cell[1]-1] in CurrentCells:
				numLiveCells +=1
			elif [cell[0]+1, cell[1]-1] not in neighbours:
				neighbours += [[cell[0]+1, cell[1]-1]]

		if cell[0] != 0 and cell[1] != Yedge:
			if [cell[0]-1, cell[1]+1] in CurrentCells:
				numLiveCells +=1
			elif [cell[0]-1, cell[1]+1] not in neighbours:
				neighbours += [[cell[0]-1, cell[1]+1]]

		if cell[0] != 0 and cell[1] != 0:
			if [cell[0]-1, cell[1]-1] in CurrentCells:
				numLiveCells +=1
			elif [cell[0]-1, cell[1]-1] not in neighbours:
				neighbours += [[cell[0]-1, cell[1]-1]]	
		
		
		if (numLiveCells in survRule) and cell not in nextGen:
			nextGen += [cell]

		elif numLiveCells not in survRule and numLiveCells not in birthRule:
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
		
		if NumLiveCells in birthRule and Cell not in nextGen:
			nextGen += [Cell]


	return nextGen, nextGenDel
