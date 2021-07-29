import pygame
import time 

pygame.init()
White = (230,230,230)
Black = (0, 0, 0)
Grey = (128, 128, 128)

Width = 800
cellThickness = 40
lineThickness = 4
totalColums = 0
totalRows = 0
fatList = []
rowList = []
cellMap = []
window = pygame.display.set_mode((Width,Width))

class Cell:
    def __init__(self, color, width, row, column, totalCol, totalRow, window):
        self.color = color
        self.x = row * width
        self.y = column * width
        self.width = width
        self.row = row
        self.column = column
        self.neighbors = []
        self.totalColumns = totalCol
        self.totalRows = totalRow
        self.alive = False
        self.window = window
        self.friends = []


    def isAlive(self):
        if self.alive == False:
            return False
        if self.alive == True:
            return True

    def makeAlive(self):
        self.alive = True
        self.color = White

    def makeDead(self):
        self.alive = False
        self.color = Black

    def getX(self):
        return (self.row)

    def getY(self):
        return(self.column)

    def drawNode(self):
        pygame.draw.rect(self.window, self.color, pygame.Rect(self.x, self.y, self.width, self.width))

    def changeColor(self, alive, color):
        if self.alive == True:
            self.color = Black
        if self.alive == False:
            self.color = White

    def getNeighbor(self, currentcell, row, column, totalRow, totalCol, list):


        if not row + 1 > totalRow:
             currentcell.neighbors.append(list[column][row + 1])

        if not row - 1 < 0:
             currentcell.neighbors.append(list[column][row - 1])

        if not column + 1 > totalCol:
             currentcell.neighbors.append(list[column+1][row])

        if not column - 1 < 0:
             currentcell.neighbors.append(list[column-1][row])

        # diagonals -----------
        if not row + 1 > totalRow and not column + 1 > totalCol:
            currentcell.neighbors.append(list[column + 1][row + 1])

        if not row + 1 > totalRow and not column - 1 < 0:
            currentcell.neighbors.append(list[column-1][row+1])

        if not row - 1 < 0 and not column + 1 > totalCol:
            currentcell.neighbors.append(list[column+1][row-1])

        if not row - 1 < 0 and not column - 1 < 0:
            currentcell.neighbors.append(list[column-1][row-1])

    def getFriends(self):
        for friendCell in self.neighbors:
            if friendCell.isAlive() == True:
                if not friendCell in self.friends:
                    self.friends.append(friendCell)

    def updateFriends(self):
        self.friends.clear()


def drawLines(win, col, totalRows, totalColumns, thick, cellThick, windowW, windowH):
    for i in range(0, totalColumns + 2):
        pygame.draw.line(win, col, (((i * cellThick)), 0), (((i * cellThick)), windowH), thick) # draws line from the cell's x co-ord to the bottom

    for i in range(0, totalRows + 2):
        pygame.draw.line(win, col, ((0, (i * cellThick))), ((windowW ,(i * cellThick))), thick) # draws line from the cell's y co-ord to the end of the screen

def getRows(height, cellW):
    return height // cellW

def getCols(width, cellW):
    return width // cellW

def useDN(cellMap):
    for row in cellMap:
        for cell in row:
            if (len(cell.friends)) >= 1:
                print("cell at row:" + str(cell.row) + " col:" + str(cell.column) + " has " + str(len(cell.friends)) + "friends")
            if cell.alive == True:
                if len(cell.friends) >= 4:
                    cell.makeDead()
                if len(cell.friends) < 2:
                    cell.makeDead()
            if cell.alive == False:
                if len(cell.friends) == 3:
                    cell.makeAlive()


totalColums = getCols(Width, cellThickness) # gets total rows depending on the dimensions of the screen
totalRows = getRows(Width, cellThickness)


for col in range(0, totalColums + 1):
    for row in range(0, totalRows):
        newCell = Cell(Black, cellThickness, row, col, totalColums, totalRows, window) # creates new cells
        if len(fatList) == totalColums : # if the number of cells in this list is equal to the width of the map, add list to cellmap and clear for next row
            cellMap.append(fatList)
            fatList = []# 
        fatList.append(newCell) # add cell to row


# main ================================================= main

cellMap[10][10].makeAlive()
cellMap[10][11].makeAlive()
cellMap[10][9].makeAlive()
cellMap[9][11].makeAlive()
cellMap[8][10].makeAlive()
count = 0
#for item in cellMap:
#    for cell in item:
#        cell.getNeighbor(cell, cell.row, cell.column, totalRows-1, totalColums-1, cellMap)

while True:
    for item in cellMap:
        for currentcell in item:
            currentcell.drawNode()
            drawLines(window, Grey, totalRows, totalColums, lineThickness, cellThickness, Width, Width)
            currentcell.getNeighbor(currentcell, currentcell.row, currentcell.column, totalRows-1, totalColums-1, cellMap)
            currentcell.updateFriends()
            currentcell.getFriends()
    count = count + 1
    useDN(cellMap)
    pygame.display.flip()
    time.sleep(.1)


# to do list
# fix problem, either neighbor list or friend list is not updating 