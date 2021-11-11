# Conways Game of Life
As a fun little project to waste some time and continue my programming over the summer break I began this project to create a Conway's Game of Life in python using pygame.
Conway's Game of Life is a cellular automaton. it consists of cells, which using only a couple simple mathematical rules can come to life, die, and propegate depending on starting conditions.
The rules of this game are:
1. If a cell has one or fewer neighbors who are alive it dies
2. If a cell has four or more neighbors who are alive it dies
3. If a cell has exactly two or three neighbors who are alive it survives
4. If a cell is not alive and is surrounded by exactly three neighbors who are alive it comes to life
## An example of it running can be seen below
![](conwaysgame.gif)
## breaking down the code
The project was created using object oriented programming, each square on the map is of the class cell who's attributes can be seen below:
```python
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
```
Each cell is initialized as not alive and is assigned a row and column at instantiation. Each cell has two lists which hold other cells, one is called neighbors which holds all 8 cells adjecent to the cell and the other is friends which contains all of the cells neighbors which are currently alive.
Some methods of the cell class are quite simple such as :
- isAlive() - returns bool 
- makeAlive() - changes cells alive attribute to true
- makeDead() - changes cells alive attribute to false
- getX() - returns cells x position
- getY() - returns cells y position
- changeColor() - changes color of cell from white to black if dead or black to white if dead
- drawNode() - draws the cell on the window
- updateFriends() - clears the friends list after each update

### More Interesting Methods/Functions
#### getNeighbor():
```python
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
```
There most likely was a cleaner way to write this but here I am manualy checking each of the surrounding cells by reference to their row and column and checking if the cell is within the map before appending to the cells neighbor list to avoid an indexError.

#### getFriends():
```python
    def getFriends(self):
        for friendCell in self.neighbors:
            if friendCell.isAlive() == True:
                if not friendCell in self.friends:
                    self.friends.append(friendCell)
```
This simply iterates through the list of neighbors and checks if they are alive, if so they are added to the cells friend list

#### useDN():
```python

def useDN(cellMap):
    for row in cellMap:
        for cell in row:
            if (len(cell.friends)) >= 1:
                    if cell.alive == True:
                        if len(cell.friends) >= 4:
                            cell.makeDead()
                        if len(cell.friends) < 2:
                            cell.makeDead()
                    if cell.alive == False:
                        if len(cell.friends) == 3:
                            cell.makeAlive()
```
This is the function that is actually checking the friends list and updating the cell's alive attribute acordingly. This is where the rules of Conway's Game of Life are implemented 

#### drawLines():
```python
def drawLines(win, col, totalRows, totalColumns, thick, cellThick, windowW, windowH):
    for i in range(0, totalColumns + 2):
        pygame.draw.line(win, col, (((i * cellThick)), 0), (((i * cellThick)), windowH), thick) # draws line from the cell's x co-ord to the bottom

    for i in range(0, totalRows + 2):
        pygame.draw.line(win, col, ((0, (i * cellThick))), ((windowW ,(i * cellThick))), thick) # draws line from the cell's y co-ord to the end of the screen

```
As the name implies this function draws the lines seen on the map, it does so by using the total number of columns combined with the width of each cell to get the coordinates for each line drawn (they are drawn over the cell). This must be done on every update so that the lines arent simply overwritten after the first game update.
#### Other functions
- getRows()
- getCols()

These return the number of rows and columns that can fit on the window given its width and height and the the width of each cell 
### The Main
#### Creating and Storing the Map
```python
for col in range(0, totalColums + 1):
    for row in range(0, totalRows):
        newCell = Cell(Black, cellThickness, row, col, totalColums, totalRows, window) # creates new cells
        if len(fatList) == totalColums : # if the number of cells in this list is equal to the width of the map, add list to cellmap and clear for next row
            cellMap.append(fatList)
            fatList = []# 
        fatList.append(newCell) # add cell to row
```
this loop uses the known number of columns and rows to loop over and create the map which consists of a list of lists. First the cells are created and then added to a temporary list called fatList which represents a row on the map, once the number of cells in this temporary list is equal to the number of columns on the map the whole temp list is added to another list called cellMap which is the main structure which is used to refer to and access cells in the main. 

#### Gathering Data on Cell Neighbors
```python
for row in cellMap:
    for cell in row:
        cell.getNeighbor(cell.row, cell.column, totalRows-1, totalColums-1, cellMap)
```
This just quickly runs through the map and gathers the data for each cells neighbor attribute used later in the code, run before the main game loop.

#### Game Loop
```python
while True:
    for item in cellMap:
        for currentcell in item:
            currentcell.drawNode()
            drawLines(window, Grey, totalRows, totalColums, lineThickness, cellThickness, Width, Height)
            currentcell.updateFriends()
            currentcell.getFriends()
    useDN(cellMap)
    pygame.display.update()
```
The whole game loop can be seen here, first looping over the entire map checking all cells and updating any cell's attributes if they need to be, then drawing the lines between the cells . After this loop the useDN function is called and actually updates all of the cell alive states at once.

## Downsides
- As the game map is generated as a list of lists and rendering is done by looping through this list increasing map sizes leads to very rapidly increasing the time between each update. using a screen width of 1000 (what is being used in the gif above) is a good compramise between map size and speed as the time between each update is not that slow
- Cells cannot yet be updated dynamically and must be pre-configured before running, in a future visit to this project I may take on the task of adding user interaction in the form of pausing and updating cells in run-time. (example of cells being brought to life before run time below)
```python
cellMap[10][11].makeAlive()
cellMap[11][12].makeAlive()
cellMap[12][10].makeAlive()
cellMap[12][11].makeAlive()
cellMap[12][12].makeAlive()
```
makes the configuration seen in the gif

### Other interesting configurations
![](gif2.gif)

I got all of my information for the explaination of the game from this [site](https://playgameoflife.com/) that lets you play with this simulation and does it significantly better than I have
