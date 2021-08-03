import pygame
import time 
from tkinter import *   

pygame.init()
White = (230,230,230)
Black = (0, 0, 0)
Grey = (128, 128, 128)

paused = False
Height = 1000
Width = 1000
cellThickness = 40
lineThickness = 4
totalColums = 0
totalRows = 0
fatList = []
rowList = []
cellMap = []
window = pygame.display.set_mode((Width,Height))

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

    def getNeighbor(self, row, column, totalRow, totalCol, list):


        if not row + 1 > totalRow:
             self.neighbors.append(list[column][row + 1])

        if not row - 1 < 0:
             self.neighbors.append(list[column][row - 1])

        if not column + 1 > totalCol:
             self.neighbors.append(list[column+1][row])

        if not column - 1 < 0:
             self.neighbors.append(list[column-1][row])

        # diagonals -----------
        if not row + 1 > totalRow and not column + 1 > totalCol:
            self.neighbors.append(list[column + 1][row + 1])

        if not row + 1 > totalRow and not column - 1 < 0:
            self.neighbors.append(list[column-1][row+1])

        if not row - 1 < 0 and not column + 1 > totalCol:
            self.neighbors.append(list[column+1][row-1])

        if not row - 1 < 0 and not column - 1 < 0:
            self.neighbors.append(list[column-1][row-1])

    def getFriends(self):
        for friendCell in self.neighbors:
            if friendCell.isAlive() == True:
                if not friendCell in self.friends:
                    self.friends.append(friendCell)

    def updateFriends(self):
        self.friends.clear()

def drawLines(win, col, totalRows, totalColumns, thick, cellThick, windowW, windowH):
    for i in range(0, totalColumns + 1):
        pygame.draw.line(win, col, (((i * cellThick)), 0), (((i * cellThick)), windowH), thick) # draws line from the cell's x co-ord to the bottom

    for i in range(0, totalRows + 1):
        pygame.draw.line(win, col, ((0, (i * cellThick))), ((windowW ,(i * cellThick))), thick) # draws line from the cell's y co-ord to the end of the screen

def getRows(height, cellW):
    return height // cellW

def getCols(width, cellW):
    return width // cellW

def useDN(cellMap):
    for row in cellMap:
        for cell in row:
            if cell.alive == True:
                if len(cell.friends) >= 4:
                    cell.makeDead()
                if len(cell.friends) < 2:
                    cell.makeDead()
            if cell.alive == False:
                if len(cell.friends) == 3:
                    cell.makeAlive()

totalColums = getCols(Width, cellThickness) # gets total rows depending on the dimensions of the screen
totalRows = getRows(Height, cellThickness)


# main ================================================= main

for col in range(0, totalColums + 1):
    for row in range(0, totalRows):
        newCell = Cell(Black, cellThickness, row, col, totalColums, totalRows, window) # creates new cells
        if len(fatList) == totalColums : # if the number of cells in this list is equal to the width of the map, add list to cellmap and clear for next row
            cellMap.append(fatList)
            fatList = []
        fatList.append(newCell) # add cell to row

cellMap[10][11].makeAlive()
cellMap[11][12].makeAlive()
cellMap[12][10].makeAlive()
cellMap[12][11].makeAlive()
cellMap[12][12].makeAlive()

for row in cellMap:
    for cell in row:
        cell.getNeighbor(cell.row, cell.column, totalRows-1, totalColums-1, cellMap)

while True:
    for item in cellMap:
        for currentcell in item:
            currentcell.drawNode()
            drawLines(window, Grey, totalRows, totalColums, lineThickness, cellThickness, Width, Height)
            currentcell.updateFriends()
            currentcell.getFriends()
    useDN(cellMap)
    for event in pygame.event.get():
        if event.type == pygame.K_SPACE:
            paused = True
            while paused == True:
                print("burh")
                for event in pygame.event.get():
                    if event.type == pygame.K_SPACE:
                        paused ==False

    pygame.display.update()


pygame.quit()
    