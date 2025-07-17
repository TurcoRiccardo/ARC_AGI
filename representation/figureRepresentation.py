import numpy as np
from dataclasses import dataclass
from selection.selector import Selector

@dataclass
class PixelNode:
    x: int
    y: int
    color: int = 0

@dataclass
class Figure:
    grid: np.ndarray
    pos: PixelNode
    h: int
    w: int
    color: int

#fills a list with the pixels of the figure
def ricFindFigure(grid, posX, posY, pixelList, color, mask, nc, nr):
    if mask[posX][posY] == 1 and grid[posX][posY] == color:
        mask[posX][posY] = 0
        pixelList.append(PixelNode(posX, posY, color))
    if posX+1 < nr:
        #down
        if grid[posX+1][posY] == color and mask[posX+1][posY] == 1:
            ricFindFigure(grid, posX+1, posY, pixelList, color, mask, nc, nr)
    if posX > 0:
        #up
        if grid[posX-1][posY] == color and mask[posX-1][posY] == 1:
            ricFindFigure(grid, posX-1, posY, pixelList, color, mask, nc, nr)
    if posY+1 < nc:
        #right
        if grid[posX][posY+1] == color and mask[posX][posY+1] == 1:
            ricFindFigure(grid, posX, posY+1, pixelList, color, mask, nc, nr)
    if posY > 0:
        #left
        if grid[posX][posY-1] == color and mask[posX][posY-1] == 1:
            ricFindFigure(grid, posX, posY-1, pixelList, color, mask, nc, nr)
    return 

class figureRepresentation:
    def __init__(self, input_grid):
        self.nr = input_grid.shape[0]
        self.nc = input_grid.shape[1]
        self.figureList = list()
        mask = np.ones((self.nr, self.nc), dtype=int)
        for x in range(0, self.nr):
            for y in range(0, self.nc):
                if input_grid[x][y] != 0 and mask[x][y] == 1:
                    pixelList = list()
                    xMax = 0
                    xMin = 1000
                    yMax = 0
                    yMin = 1000
                    ricFindFigure(input_grid, x, y, pixelList, input_grid[x][y], mask, self.nc, self.nr)
                    for p in pixelList:
                        if xMax < p.x:
                            xMax = p.x
                        if xMin > p.x:
                            xMin = p.x
                        if yMax < p.y:
                            yMax = p.y
                        if yMin > p.y:
                            yMin = p.y
                    fig = Figure(np.zeros((xMax-xMin+1, yMax-yMin+1), dtype=int), PixelNode(xMin, yMin), xMax-xMin+1, yMax-yMin+1, input_grid[x][y])
                    for p in pixelList:
                        fig.grid[p.x - xMin][p.y - yMin] = 1
                    self.figureList.append(fig)

    #return the total number of figure
    def getNElement(self):
        return len(self.figureList)
    
    #return a set of colors used in the grid
    def getColors(self):
        colorSet = set()
        for f in self.figureList:
            colorSet.add(f.color)
        return colorSet

    #return the number of row and column in the figure
    def getElementComponent(self, index):
        return (self.figureList[index].h, self.figureList[index].w)
    
    #return the list of figure index
    def generateIndexList(self, s):
        l = list()
        if s.allElement == 1:
            #sotto
            l.append(len(self.figureList) - (s.index % len(self.figureList)) - 1)
        elif s.allElement == 2:
            #centro
            if len(self.figureList) % 2 == 1:
                l.append(len(self.figureList) // 2)
            else:
                l.append(len(self.figureList) // 2 - 1)
                l.append(len(self.figureList) // 2)
        elif s.allElement == 3:
            #all
            l = [x for x in range(0, len(self.figureList))]
        elif s.allElement == 4:
            #color
            for x in range(0, len(self.figureList)):
                if self.figureList[x].color == s.color:
                    l.append(x)
        else:
            #sopra
            l.append(s.index % len(self.figureList))
        return l
    
    #return the list of component index
    def generateComponentList_row(self, s, adapted_index):
        l = list()
        if s.allComponent1 == 1:
            #dal basso
            l.append(self.figureList[adapted_index].h - (s.component[0] % self.figureList[adapted_index].h) - 1)
        elif s.allComponent1 == 2:
            #centro
            if self.figureList[adapted_index].h % 2 == 1:
                l.append(self.figureList[adapted_index].h // 2)
            else:
                l.append(self.figureList[adapted_index].h // 2 - 1)
                l.append(self.figureList[adapted_index].h // 2)
        elif s.allComponent1 >= 3:
            #all color
            l = [x for x in range(0, self.figureList[adapted_index].h)]
        else:
            #dall'alto
            l.append(s.component[0] % self.figureList[adapted_index].h)
        return l
    
    #return the list of component index
    def generateComponentList_column(self, s, adapted_index):
        l = list()
        if s.allComponent2 == 1:
            #da destra
            l.append(self.figureList[adapted_index].w - (s.component[1] % self.figureList[adapted_index].w) - 1)
        elif s.allComponent2 == 2:
            #centro
            if self.figureList[adapted_index].w % 2 == 1:
                l.append(self.figureList[adapted_index].w // 2)
            else:
                l.append(self.figureList[adapted_index].w // 2 - 1)
                l.append(self.figureList[adapted_index].w // 2)
        elif s.allComponent2 >= 3:
            #all color
            l = [x for x in range(0, self.figureList[adapted_index].w)]
        else:
            #da sinistra
            l.append(s.component[1] % self.figureList[adapted_index].w)
        return l


    #moves the figure index based on the direction
    def moveFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if (s.direction % 4) == 0:
                #down    
                if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h < self.nr:
                    self.figureList[adapted_index].pos.x += 1
                    count += 1
            elif (s.direction % 4) == 1:
                #up
                if self.figureList[adapted_index].pos.x > 0:
                    self.figureList[adapted_index].pos.x -= 1
                    count += 1
            elif (s.direction % 4) == 2:
                #right
                if self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w < self.nc:
                    self.figureList[adapted_index].pos.y += 1
                    count += 1
            elif (s.direction % 4) == 3:
                #left
                if self.figureList[adapted_index].pos.y > 0:
                    self.figureList[adapted_index].pos.y -= 1
                    count += 1
        if count != 0:
            return 0
        return 1

    #changes the color of the figure index based on color
    def changeColorFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if s.color % 2 == 0:
                if self.figureList[adapted_index].color != 9:
                    self.figureList[adapted_index].color += 1
                    count += 1
            else:
                if self.figureList[adapted_index].color != 1:
                    self.figureList[adapted_index].color -= 1
                    count += 1
        if count != 0:
            return 0
        return 1
    
    #add a element in the figure in the selected row
    def addElementFigure_row(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            lc = self.generateComponentList_row(s, adapted_index)
            for adapted_component in lc:
                if (s.direction % 2) == 0:
                    #right
                    indY = 0
                    for y in range(0, self.figureList[adapted_index].w):
                        if self.figureList[adapted_index].grid[adapted_component][y] > 0:
                            indY = y
                    if indY + 1 == self.figureList[adapted_index].w:
                        if self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w < self.nc:
                            self.figureList[adapted_index].grid = np.hstack([self.figureList[adapted_index].grid, np.zeros((1, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, 1)])
                            self.figureList[adapted_index].w += 1
                            self.figureList[adapted_index].grid[adapted_component][indY + 1] = 1
                            count += 1
                    else:
                        self.figureList[adapted_index].grid[adapted_component][indY + 1] = 1
                        count += 1
                elif (s.direction % 2) == 1:
                    #left
                    indY = 0
                    for y in range(0, self.figureList[adapted_index].w):
                        if self.figureList[adapted_index].grid[adapted_component][y] > 0:
                            indY = y
                            break
                    if indY == 0:
                        if self.figureList[adapted_index].pos.y > 0:
                            self.figureList[adapted_index].grid = np.hstack([np.zeros((1, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, 1), self.figureList[adapted_index].grid])
                            self.figureList[adapted_index].pos.y -= 1
                            self.figureList[adapted_index].w += 1
                            self.figureList[adapted_index].grid[adapted_component][indY - 1] = 1
                            count += 1
                    else:
                        self.figureList[adapted_index].grid[adapted_component][indY - 1] = 1
                        count += 1
        if count != 0:
            return 0
        return 1
    
    #add a element in the figure in the selected column
    def addElementFigure_column(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            lc = self.generateComponentList_column(s, adapted_index)
            for adapted_component in lc:
                if (s.direction % 4) == 0:
                    #down
                    indX = 0
                    for x in range(0, self.figureList[adapted_index].h):
                        if self.figureList[adapted_index].grid[x][adapted_component] > 0:
                            indX = x
                    if indX + 1 == self.figureList[adapted_index].h:
                        if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h < self.nr:
                            self.figureList[adapted_index].grid = np.vstack([self.figureList[adapted_index].grid, np.zeros((1, self.figureList[adapted_index].w), dtype=int)])
                            self.figureList[adapted_index].h += 1
                            self.figureList[adapted_index].grid[indX + 1][adapted_component] = 1
                            count += 1
                    else:
                        self.figureList[adapted_index].grid[indX + 1][adapted_component] = 1
                        count += 1
                elif (s.direction % 4) == 1:
                    #up
                    indX = 0
                    for x in range(0, self.figureList[adapted_index].h):
                        if self.figureList[adapted_index].grid[x][adapted_component] > 0:
                            indX = x
                            break
                    if indX == 0:
                        if self.figureList[adapted_index].pos.x > 0:
                            self.figureList[adapted_index].grid = np.vstack([np.zeros((1, self.figureList[adapted_index].w), dtype=int), self.figureList[adapted_index].grid])
                            self.figureList[adapted_index].pos.x -= 1
                            self.figureList[adapted_index].h += 1
                            self.figureList[adapted_index].grid[indX - 1][adapted_component] = 1
                            count += 1
                    else:
                        self.figureList[adapted_index].grid[indX - 1][adapted_component] = 1
                        count += 1
        if count != 0:
            return 0
        return 1

    #move the selected row in the figure
    def moveElementFigure_row(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            mod = 0
            lc = self.generateComponentList_row(s, adapted_index)
            if self.figureList[adapted_index].w > 1:
                for adapted_component in lc:
                    if (s.direction % 2) == 0:
                        #right
                        if self.figureList[adapted_index].grid[adapted_component][-1] != 0:
                            if self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w < self.nc:
                                self.figureList[adapted_index].grid = np.hstack([self.figureList[adapted_index].grid, np.zeros((1, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, 1)])
                                self.figureList[adapted_index].w += 1
                                for y in reversed(range(0, self.figureList[adapted_index].w-1)):
                                    self.figureList[adapted_index].grid[adapted_component][y + 1] = self.figureList[adapted_index].grid[adapted_component][y]
                                mod += 1
                        else:
                            for y in reversed(range(0, self.figureList[adapted_index].w-1)):
                                self.figureList[adapted_index].grid[adapted_component][y + 1] = self.figureList[adapted_index].grid[adapted_component][y]
                            mod += 1
                    elif (s.direction % 2) == 1:
                        #left
                        if self.figureList[adapted_index].grid[adapted_component][0] != 0:
                            if self.figureList[adapted_index].pos.y > 0:
                                self.figureList[adapted_index].grid = np.hstack([np.zeros((1, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, 1), self.figureList[adapted_index].grid])
                                self.figureList[adapted_index].pos.y -= 1
                                self.figureList[adapted_index].w += 1
                                for y in range(1, self.figureList[adapted_index].w):
                                    self.figureList[adapted_index].grid[adapted_component][y - 1] = self.figureList[adapted_index].grid[adapted_component][y]
                                mod += 1
                        else:
                            for y in range(1, self.figureList[adapted_index].w):
                                self.figureList[adapted_index].grid[adapted_component][y - 1] = self.figureList[adapted_index].grid[adapted_component][y]
                            mod += 1
                if mod > 0:
                    #right
                    ok = 0
                    for x in range(0, self.figureList[adapted_index].h):
                        if self.figureList[adapted_index].grid[x][-1] > 0:
                            ok = 1
                            break
                    if ok == 0:
                        self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[:,0:self.figureList[adapted_index].w-1]
                        self.figureList[adapted_index].w -= 1
                    #left
                    ok = 0
                    for x in range(0, self.figureList[adapted_index].h):
                        if self.figureList[adapted_index].grid[x][0] > 0:
                            ok = 1
                            break
                    if ok == 0:
                        self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[:,1:self.figureList[adapted_index].w]
                        self.figureList[adapted_index].pos.y += 1
                        self.figureList[adapted_index].w -= 1
                count += mod
        if count != 0:
            return 0
        return 1
    
    #move the selected column in the figure
    def moveElementFigure_column(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            mod = 0
            lc = self.generateComponentList_column(s, adapted_index)
            if self.figureList[adapted_index].h > 1:
                for adapted_component in lc:
                    if (s.direction % 2) == 0:
                        #down
                        if self.figureList[adapted_index].grid[-1][adapted_component] != 0:
                            if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h < self.nr:
                                self.figureList[adapted_index].grid = np.vstack([self.figureList[adapted_index].grid, np.zeros((1, self.figureList[adapted_index].w), dtype=int)])
                                self.figureList[adapted_index].h += 1
                                for x in reversed(range(0, self.figureList[adapted_index].h-1)):
                                    self.figureList[adapted_index].grid[x + 1][adapted_component] = self.figureList[adapted_index].grid[x][adapted_component]
                                mod += 1
                        else:
                            for x in reversed(range(0, self.figureList[adapted_index].h-1)):
                                self.figureList[adapted_index].grid[x + 1][adapted_component] = self.figureList[adapted_index].grid[x][adapted_component]
                            mod += 1
                    elif (s.direction % 2) == 1:
                        #up
                        if self.figureList[adapted_index].grid[0][adapted_component] != 0:
                            if self.figureList[adapted_index].pos.x > 0:
                                self.figureList[adapted_index].grid = np.vstack([np.zeros((1, self.figureList[adapted_index].w), dtype=int), self.figureList[adapted_index].grid])
                                self.figureList[adapted_index].pos.x -= 1
                                self.figureList[adapted_index].h += 1
                                for x in range(1, self.figureList[adapted_index].h):
                                    self.figureList[adapted_index].grid[x - 1][adapted_component] = self.figureList[adapted_index].grid[x][adapted_component]
                                mod += 1
                        else:
                            for x in range(1, self.figureList[adapted_index].h):
                                self.figureList[adapted_index].grid[x - 1][adapted_component] = self.figureList[adapted_index].grid[x][adapted_component]
                            mod += 1
                if mod > 0:
                    #down
                    ok = 0
                    for y in range(0, self.figureList[adapted_index].w):
                        if self.figureList[adapted_index].grid[-1][y] > 0:
                            ok = 1
                            break
                    if ok == 0:
                        self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[0:self.figureList[adapted_index].h-1,:]
                        self.figureList[adapted_index].h -= 1
                    #up
                    ok = 0
                    for y in range(0, self.figureList[adapted_index].w):
                        if self.figureList[adapted_index].grid[0][y] > 0:
                            ok = 1
                            break
                    if ok == 0:
                        self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[1:self.figureList[adapted_index].h,:]
                        self.figureList[adapted_index].pos.x += 1
                        self.figureList[adapted_index].h -= 1
                count += mod
        if count != 0:
            return 0
        return 1

    #remove the element in the figure in the selected row
    def removeElementFigure_row(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            lc = self.generateComponentList_row(s, adapted_index)
            lc.sort(key=lambda i: i, reverse=True)
            for adapted_component in lc:
                if self.figureList[adapted_index].h > 1:
                    indY = 0
                    c = 0
                    if (s.direction % 2) == 0:
                        #right
                        for y in range(0, self.figureList[adapted_index].w):
                            if self.figureList[adapted_index].grid[adapted_component][y] > 0:
                                indY = y
                                c += 1
                    elif (s.direction % 2) == 1:
                        #left
                        for y in range(0, self.figureList[adapted_index].w):
                            if self.figureList[adapted_index].grid[adapted_component][y] > 0:
                                if c == 0:
                                    indY = y
                                c += 1
                    if c <= 1:
                        if adapted_component == 0:
                            self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[1:self.figureList[adapted_index].h,:]
                            self.figureList[adapted_index].pos.x += 1
                            self.figureList[adapted_index].h -= 1
                            count += 1
                        else:
                            self.figureList[adapted_index].grid = np.vstack([self.figureList[adapted_index].grid[0:adapted_component,:], self.figureList[adapted_index].grid[adapted_component+1:self.figureList[adapted_index].h,:]])
                            self.figureList[adapted_index].h -= 1
                            count += 1
                    else:
                        self.figureList[adapted_index].grid[adapted_component][indY] = 0
                        count += 1
        if count != 0:
            return 0
        return 1

    #remove the element in the figure in the selected column
    def removeElementFigure_column(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            lc = self.generateComponentList_column(s, adapted_index)
            lc.sort(key=lambda i: i, reverse=True)
            for adapted_component in lc:
                if self.figureList[adapted_index].w > 1:
                    indX = 0
                    c = 0
                    if (s.direction % 2) == 0:
                        #down
                        for x in range(0, self.figureList[adapted_index].h):
                            if self.figureList[adapted_index].grid[x][adapted_component] > 0:
                                indX = x
                                c += 1
                    elif (s.direction % 2) == 1:
                        #up
                        for x in range(0, self.figureList[adapted_index].h):
                            if self.figureList[adapted_index].grid[x][adapted_component] > 0:
                                if c == 0:
                                    indX = x
                                c += 1
                    if c <= 1:
                        if adapted_component == 0:
                            self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[:,1:self.figureList[adapted_index].w]
                            self.figureList[adapted_index].pos.y += 1
                            self.figureList[adapted_index].w -= 1
                            count += 1
                        else:
                            self.figureList[adapted_index].grid = np.hstack([self.figureList[adapted_index].grid[:,0:adapted_component], self.figureList[adapted_index].grid[:,adapted_component+1:self.figureList[adapted_index].w]])
                            self.figureList[adapted_index].w -= 1
                            count += 1
                    else:
                        self.figureList[adapted_index].grid[indX][adapted_component] = 0
                        count += 1
        if count != 0:
            return 0
        return 1

    #duplicate the selected figure from the figure list
    def duplicateFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        duplicatedFigure = []
        for adapted_index in l:
            fig = Figure(self.figureList[adapted_index].grid.copy(), PixelNode(self.figureList[adapted_index].pos.x, self.figureList[adapted_index].pos.y), self.figureList[adapted_index].h, self.figureList[adapted_index].w, self.figureList[adapted_index].color)
            duplicatedFigure.append((adapted_index, fig))
            count += 1
        if count != 0:
            duplicatedFigure.sort(key=lambda i: i[0], reverse=True)
            for (index, fig) in duplicatedFigure:
                self.figureList.insert(index, fig)
            return 0
        return 1
    
    #remove a figure from the figure list based on the index
    def removeFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        li = self.generateIndexList(s)
        li.sort(key=lambda i: i, reverse=True)
        for adapted_index in li:
            self.figureList.pop(adapted_index)
            count += 1
        if count != 0:
            return 0
        return 1

    #rotate a figure based on the direction direction
    def rotateFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if (s.direction % 2) == 0:
                #rotate to the right
                if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].w <= self.nr and self.figureList[adapted_index].pos.y + self.figureList[adapted_index].h <= self.nc:
                    newGrid = np.zeros([self.figureList[adapted_index].w, self.figureList[adapted_index].h], dtype=np.uint8)
                    for x in range(self.figureList[adapted_index].h):
                        for y in range(self.figureList[adapted_index].w):
                            newGrid[y][self.figureList[adapted_index].h - x - 1] = self.figureList[adapted_index].grid[x][y]
                    self.figureList[adapted_index].grid = newGrid
                    tmp = self.figureList[adapted_index].h
                    self.figureList[adapted_index].h = self.figureList[adapted_index].w
                    self.figureList[adapted_index].w = tmp
                    count += 1
            elif (s.direction % 2) == 1:
                #rotate to the left
                if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].w <= self.nr and self.figureList[adapted_index].pos.y + self.figureList[adapted_index].h <= self.nc:
                    newGrid = np.zeros([self.figureList[adapted_index].w, self.figureList[adapted_index].h], dtype=np.uint8)
                    for x in range(self.figureList[adapted_index].h):
                        for y in range(self.figureList[adapted_index].w):
                            newGrid[self.figureList[adapted_index].w - y - 1][x] = self.figureList[adapted_index].grid[x][y]
                    self.figureList[adapted_index].grid = newGrid
                    tmp = self.figureList[adapted_index].h
                    self.figureList[adapted_index].h = self.figureList[adapted_index].w
                    self.figureList[adapted_index].w = tmp
                    count += 1
        if count != 0:
            return 0
        return 1

    #merge 2 figure based on the direction direction
    def mergeFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        removefig = set()
        l = self.generateIndexList(s)
        for adapted_index in l:
            if adapted_index not in removefig:
                if (s.direction % 4) == 0:
                    #down
                    if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h < self.nr:
                        indexFigure = set()
                        for y in range(0, self.figureList[adapted_index].w):
                            if self.figureList[adapted_index].grid[-1][y] > 0:
                                for indfig in range(0, len(self.figureList)):
                                    if self.figureList[indfig].color == self.figureList[adapted_index].color and adapted_index != indfig:
                                        ok = 0
                                        for j in range(0, self.figureList[indfig].h):
                                            for k in range(0, self.figureList[indfig].w):
                                                if self.figureList[indfig].grid[j][k] != 0:
                                                    if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h == self.figureList[indfig].pos.x + j and self.figureList[adapted_index].pos.y + y == self.figureList[indfig].pos.y + k:
                                                        if indfig not in removefig:
                                                            indexFigure.add(indfig)
                                                            removefig.add(indfig)
                                                        ok = 1
                                                        break
                                            if ok == 1:
                                                break
                        if len(indexFigure) > 0:
                            for f in sorted(indexFigure, reverse=True):
                                #guardo a sotto
                                if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h - 1 < self.figureList[f].pos.x + self.figureList[f].h - 1:
                                    inc = self.figureList[f].pos.x + self.figureList[f].h - 1 - (self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h - 1)
                                    self.figureList[adapted_index].h += inc
                                    self.figureList[adapted_index].grid = np.vstack([self.figureList[adapted_index].grid, np.zeros((inc, self.figureList[adapted_index].w), dtype=int)])
                                #guardo a sopra
                                if self.figureList[adapted_index].pos.x > self.figureList[f].pos.x:
                                    inc = self.figureList[adapted_index].pos.x - self.figureList[f].pos.x
                                    self.figureList[adapted_index].pos.x -= inc
                                    self.figureList[adapted_index].h += inc
                                    self.figureList[adapted_index].grid = np.vstack([np.zeros((inc, self.figureList[adapted_index].w), dtype=int), self.figureList[adapted_index].grid])
                                #guardo a destra
                                if self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w - 1 < self.figureList[f].pos.y + self.figureList[f].w - 1:
                                    inc = self.figureList[f].pos.y + self.figureList[f].w - 1 - (self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w - 1)
                                    self.figureList[adapted_index].w += inc
                                    self.figureList[adapted_index].grid = np.hstack([self.figureList[adapted_index].grid, np.zeros((inc, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, inc)])
                                #guardo a sinistra
                                if self.figureList[adapted_index].pos.y > self.figureList[f].pos.y:
                                    inc = self.figureList[adapted_index].pos.y - self.figureList[f].pos.y
                                    self.figureList[adapted_index].pos.y -= inc
                                    self.figureList[adapted_index].w += inc
                                    self.figureList[adapted_index].grid = np.hstack([np.zeros((inc, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, inc), self.figureList[adapted_index].grid])
                                #copio grigia
                                diffx = self.figureList[f].pos.x - self.figureList[adapted_index].pos.x
                                diffy = self.figureList[f].pos.y - self.figureList[adapted_index].pos.y 
                                for x in range(0, self.figureList[f].h):
                                    for y in range(0, self.figureList[f].w):
                                        if self.figureList[f].grid[x][y] > 0:
                                            self.figureList[adapted_index].grid[diffx + x][diffy + y] = 1
                            count += 1
                elif (s.direction % 4) == 1:
                    #up
                    if self.figureList[adapted_index].pos.x > 0:
                        indexFigure = set()
                        for y in range(0, self.figureList[adapted_index].w):
                            if self.figureList[adapted_index].grid[0][y] > 0:
                                for indfig in range(0, len(self.figureList)):
                                    if self.figureList[indfig].color == self.figureList[adapted_index].color and adapted_index != indfig:
                                        ok = 0
                                        for j in range(0, self.figureList[indfig].h):
                                            for k in range(0, self.figureList[indfig].w):
                                                if self.figureList[indfig].grid[j][k] != 0:
                                                    if self.figureList[adapted_index].pos.x - 1 == self.figureList[indfig].pos.x + j and self.figureList[adapted_index].pos.y + y == self.figureList[indfig].pos.y + k:
                                                        if indfig not in removefig:
                                                            indexFigure.add(indfig)
                                                            removefig.add(indfig)
                                                        ok = 1
                                                        break
                                            if ok == 1:
                                                break
                        if len(indexFigure) > 0:
                            for f in sorted(indexFigure, reverse=True):
                                #guardo a sotto
                                if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h - 1 < self.figureList[f].pos.x + self.figureList[f].h - 1:
                                    inc = self.figureList[f].pos.x + self.figureList[f].h - 1 - (self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h - 1)
                                    self.figureList[adapted_index].h += inc
                                    self.figureList[adapted_index].grid = np.vstack([self.figureList[adapted_index].grid, np.zeros((inc, self.figureList[adapted_index].w), dtype=int)])
                                #guardo a sopra
                                if self.figureList[adapted_index].pos.x > self.figureList[f].pos.x:
                                    inc = self.figureList[adapted_index].pos.x - self.figureList[f].pos.x
                                    self.figureList[adapted_index].pos.x -= inc
                                    self.figureList[adapted_index].h += inc
                                    self.figureList[adapted_index].grid = np.vstack([np.zeros((inc, self.figureList[adapted_index].w), dtype=int), self.figureList[adapted_index].grid])
                                #guardo a destra
                                if self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w - 1 < self.figureList[f].pos.y + self.figureList[f].w - 1:
                                    inc = self.figureList[f].pos.y + self.figureList[f].w - 1 - (self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w - 1)
                                    self.figureList[adapted_index].w += inc
                                    self.figureList[adapted_index].grid = np.hstack([self.figureList[adapted_index].grid, np.zeros((inc, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, inc)])
                                #guardo a sinistra
                                if self.figureList[adapted_index].pos.y > self.figureList[f].pos.y:
                                    inc = self.figureList[adapted_index].pos.y - self.figureList[f].pos.y
                                    self.figureList[adapted_index].pos.y -= inc
                                    self.figureList[adapted_index].w += inc
                                    self.figureList[adapted_index].grid = np.hstack([np.zeros((inc, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, inc), self.figureList[adapted_index].grid])
                                #copio grigia
                                diffx = self.figureList[f].pos.x - self.figureList[adapted_index].pos.x
                                diffy = self.figureList[f].pos.y - self.figureList[adapted_index].pos.y 
                                for x in range(0, self.figureList[f].h):
                                    for y in range(0, self.figureList[f].w):
                                        if self.figureList[f].grid[x][y] > 0:
                                            self.figureList[adapted_index].grid[diffx + x][diffy + y] = 1
                            count += 1
                elif (s.direction % 4) == 2:
                    #right
                    if self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w < self.nc:
                        indexFigure = set()
                        for x in range(0, self.figureList[adapted_index].h):
                            if self.figureList[adapted_index].grid[x][-1] > 0:
                                for indfig in range(0, len(self.figureList)):
                                    if self.figureList[indfig].color == self.figureList[adapted_index].color and adapted_index != indfig:
                                        ok = 0
                                        for j in range(0, self.figureList[indfig].h):
                                            for k in range(0, self.figureList[indfig].w):
                                                if self.figureList[indfig].grid[j][k] != 0:
                                                    if self.figureList[adapted_index].pos.x + x == self.figureList[indfig].pos.x + j and self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w == self.figureList[indfig].pos.y + k:
                                                        if indfig not in removefig:
                                                            indexFigure.add(indfig)
                                                            removefig.add(indfig)
                                                        ok = 1
                                                        break
                                            if ok == 1:
                                                break
                        if len(indexFigure) > 0:
                            for f in sorted(indexFigure, reverse=True):
                                #guardo a sotto
                                if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h - 1 < self.figureList[f].pos.x + self.figureList[f].h - 1:
                                    inc = self.figureList[f].pos.x + self.figureList[f].h - 1 - (self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h - 1)
                                    self.figureList[adapted_index].h += inc
                                    self.figureList[adapted_index].grid = np.vstack([self.figureList[adapted_index].grid, np.zeros((inc, self.figureList[adapted_index].w), dtype=int)])
                                #guardo a sopra
                                if self.figureList[adapted_index].pos.x > self.figureList[f].pos.x:
                                    inc = self.figureList[adapted_index].pos.x - self.figureList[f].pos.x
                                    self.figureList[adapted_index].pos.x -= inc
                                    self.figureList[adapted_index].h += inc
                                    self.figureList[adapted_index].grid = np.vstack([np.zeros((inc, self.figureList[adapted_index].w), dtype=int), self.figureList[adapted_index].grid])
                                #guardo a destra
                                if self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w - 1 < self.figureList[f].pos.y + self.figureList[f].w - 1:
                                    inc = self.figureList[f].pos.y + self.figureList[f].w - 1 - (self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w - 1)
                                    self.figureList[adapted_index].w += inc
                                    self.figureList[adapted_index].grid = np.hstack([self.figureList[adapted_index].grid, np.zeros((inc, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, inc)])
                                #guardo a sinistra
                                if self.figureList[adapted_index].pos.y > self.figureList[f].pos.y:
                                    inc = self.figureList[adapted_index].pos.y - self.figureList[f].pos.y
                                    self.figureList[adapted_index].pos.y -= inc
                                    self.figureList[adapted_index].w += inc
                                    self.figureList[adapted_index].grid = np.hstack([np.zeros((inc, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, inc), self.figureList[adapted_index].grid])
                                #copio grigia
                                diffx = self.figureList[f].pos.x - self.figureList[adapted_index].pos.x
                                diffy = self.figureList[f].pos.y - self.figureList[adapted_index].pos.y 
                                for x in range(0, self.figureList[f].h):
                                    for y in range(0, self.figureList[f].w):
                                        if self.figureList[f].grid[x][y] > 0:
                                            self.figureList[adapted_index].grid[diffx + x][diffy + y] = 1
                            count += 1
                elif (s.direction % 4) == 3:
                    #left
                    if self.figureList[adapted_index].pos.y > 0:
                        indexFigure = set()
                        for x in range(0, self.figureList[adapted_index].h):
                            if self.figureList[adapted_index].grid[x][0] > 0:
                                for indfig in range(0, len(self.figureList)):
                                    if self.figureList[indfig].color == self.figureList[adapted_index].color and adapted_index != indfig:
                                        ok = 0
                                        for j in range(0, self.figureList[indfig].h):
                                            for k in range(0, self.figureList[indfig].w):
                                                if self.figureList[indfig].grid[j][k] != 0:
                                                    if self.figureList[adapted_index].pos.x + x == self.figureList[indfig].pos.x + j and self.figureList[adapted_index].pos.y - 1 == self.figureList[indfig].pos.y + k:
                                                        if indfig not in removefig:
                                                            indexFigure.add(indfig)
                                                            removefig.add(indfig)
                                                        ok = 1
                                                        break
                                            if ok == 1:
                                                break
                        if len(indexFigure) > 0:
                            for f in sorted(indexFigure, reverse=True):
                                #guardo a sotto
                                if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h - 1 < self.figureList[f].pos.x + self.figureList[f].h - 1:
                                    inc = self.figureList[f].pos.x + self.figureList[f].h - 1 - (self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h - 1)
                                    self.figureList[adapted_index].h += inc
                                    self.figureList[adapted_index].grid = np.vstack([self.figureList[adapted_index].grid, np.zeros((inc, self.figureList[adapted_index].w), dtype=int)])
                                #guardo a sopra
                                if self.figureList[adapted_index].pos.x > self.figureList[f].pos.x:
                                    inc = self.figureList[adapted_index].pos.x - self.figureList[f].pos.x
                                    self.figureList[adapted_index].pos.x -= inc
                                    self.figureList[adapted_index].h += inc
                                    self.figureList[adapted_index].grid = np.vstack([np.zeros((inc, self.figureList[adapted_index].w), dtype=int), self.figureList[adapted_index].grid])
                                #guardo a destra
                                if self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w - 1 < self.figureList[f].pos.y + self.figureList[f].w - 1:
                                    inc = self.figureList[f].pos.y + self.figureList[f].w - 1 - (self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w - 1)
                                    self.figureList[adapted_index].w += inc
                                    self.figureList[adapted_index].grid = np.hstack([self.figureList[adapted_index].grid, np.zeros((inc, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, inc)])
                                #guardo a sinistra
                                if self.figureList[adapted_index].pos.y > self.figureList[f].pos.y:
                                    inc = self.figureList[adapted_index].pos.y - self.figureList[f].pos.y
                                    self.figureList[adapted_index].pos.y -= inc
                                    self.figureList[adapted_index].w += inc
                                    self.figureList[adapted_index].grid = np.hstack([np.zeros((inc, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, inc), self.figureList[adapted_index].grid])
                                #copio grigia
                                diffx = self.figureList[f].pos.x - self.figureList[adapted_index].pos.x
                                diffy = self.figureList[f].pos.y - self.figureList[adapted_index].pos.y 
                                for x in range(0, self.figureList[f].h):
                                    for y in range(0, self.figureList[f].w):
                                        if self.figureList[f].grid[x][y] > 0:
                                            self.figureList[adapted_index].grid[diffx + x][diffy + y] = 1
                            count += 1
        if count != 0:
            #rimuovo figure unite
            for f in sorted(removefig, reverse=True):
                self.figureList.pop(f)
            return 0
        return 1

    #divide the selected figure based on the selected row
    def divideFigure_row(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        dividedFigure = []
        for adapted_index in l:
            lc = self.generateComponentList_row(s, adapted_index)
            lc.sort(key=lambda i: i, reverse=True)
            for adapted_component in lc:
                if self.figureList[adapted_index].h > 1 and adapted_component+1 < self.figureList[adapted_index].h:
                    fig = Figure(self.figureList[adapted_index].grid[adapted_component+1:self.figureList[adapted_index].h,:], PixelNode(self.figureList[adapted_index].pos.x+adapted_component+1, self.figureList[adapted_index].pos.y), self.figureList[adapted_index].h-(adapted_component+1), self.figureList[adapted_index].w, self.figureList[adapted_index].color)
                    self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[0:adapted_component+1,:]
                    self.figureList[adapted_index].h -= (self.figureList[adapted_index].h - (adapted_component+1))
                    dividedFigure.append((adapted_index+1, fig))
                    count += 1
        if count != 0:
            dividedFigure.sort(key=lambda i: i[0], reverse=True)
            for (index, fig) in dividedFigure:
                self.figureList.insert(index, fig)
            return 0
        return 1
    
    #divide the selected figure based on the selected column
    def divideFigure_column(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        dividedFigure = []
        for adapted_index in l:
            lc = self.generateComponentList_column(s, adapted_index)
            lc.sort(key=lambda i: i, reverse=True)
            for adapted_component in lc:
                if self.figureList[adapted_index].w > 1 and adapted_component+1 < self.figureList[adapted_index].w:
                    fig = Figure(self.figureList[adapted_index].grid[:,adapted_component+1:self.figureList[adapted_index].w], PixelNode(self.figureList[adapted_index].pos.x, self.figureList[adapted_index].pos.y+adapted_component+1), self.figureList[adapted_index].h, self.figureList[adapted_index].w-(adapted_component+1), self.figureList[adapted_index].color)
                    self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[:,0:adapted_component+1]
                    self.figureList[adapted_index].w -= (self.figureList[adapted_index].w - (adapted_component+1))
                    dividedFigure.append((adapted_index+1, fig))
                    count += 1
        if count != 0:
            dividedFigure.sort(key=lambda i: i[0], reverse=True)
            for (index, fig) in dividedFigure:
                self.figureList.insert(index, fig)
            return 0
        return 1

    #change the order of the figure based on color in the figure list
    def changeOrder(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        if (s.color % 2) == 0:
            l.sort(key=lambda i: i, reverse=True)
        elif (s.color % 2) == 1:
            l.sort(key=lambda i: i, reverse=False)
        for adapted_index in l:
            if s.color % 2 == 0:
                if adapted_index + 1 < len(self.figureList):
                    self.figureList[adapted_index], self.figureList[adapted_index + 1] = self.figureList[adapted_index + 1], self.figureList[adapted_index]
                    count += 1
            else:
                if adapted_index - 1 >= 0:
                    self.figureList[adapted_index], self.figureList[adapted_index - 1] = self.figureList[adapted_index - 1], self.figureList[adapted_index]
                    count += 1
        if count != 0:
            return 0
        return 1
    
    #expand the grid in the direction direction
    def expandGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            if self.nr < 30:
                self.nr += 1
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr < 30:
                self.nr += 1
                for f in self.figureList:
                    f.pos.x += 1
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc < 30:
                self.nc += 1
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc < 30:
                self.nc += 1
                for f in self.figureList:
                    f.pos.y += 1
                return 0
        return 1

    #reduce the grid in the direction direction
    def reduceGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            if self.nr > 1:
                ok = 0
                for fig in self.figureList:
                    if fig.pos.x + fig.h >= self.nr - 1:
                        ok = 1
                        break
                if ok == 0:
                    self.nr -= 1
                    return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr > 1:
                ok = 0
                for fig in self.figureList:
                    if fig.pos.x == 0:
                        ok = 1
                        break
                if ok == 0:
                    self.nr -= 1
                    for fig in self.figureList:
                        fig.pos.x -= 1
                    return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc > 1:
                ok = 0
                for fig in self.figureList:
                    if fig.pos.y + fig.w >= self.nc - 1:
                        ok = 1
                        break
                if ok == 0:
                    self.nc -= 1
                    return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc > 1:
                ok = 0
                for fig in self.figureList:
                    if fig.pos.y == 0:
                        ok = 1
                        break
                if ok == 0:
                    self.nc -= 1
                    for fig in self.figureList:
                        fig.pos.y -= 1
                    return 0
        return 1


    #fitness function
    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        for z in range(0, len(self.figureList)):
            if z < len(output.figureList):
                #Verifica se due figure hanno la stessa forma normalizzando le coordinate rispetto al punto in alto a sinistra (anche esterno dalla figura)
                for x in range(0, min(self.figureList[z].h, output.figureList[z].h)):
                    for y in range(0, min(self.figureList[z].w, output.figureList[z].w)):
                        if self.figureList[z].grid[x][y] == 1 and output.figureList[z].grid[x][y] == 1:
                            score += abs(int(self.figureList[z].color) - int(output.figureList[z].color))/10
                        else:
                            if self.figureList[z].grid[x][y] != output.figureList[z].grid[x][y]:
                                score += 1
                #figure con diverse dimensioni
                score += abs(self.figureList[z].h - output.figureList[z].h)*min(self.figureList[z].w, output.figureList[z].w) + abs(self.figureList[z].w - output.figureList[z].w)*min(self.figureList[z].h, output.figureList[z].h) + abs(output.figureList[z].h - self.figureList[z].h)*abs(output.figureList[z].w - self.figureList[z].w)
                #distance
                score += abs(int(self.figureList[z].pos.x) - int(output.figureList[z].pos.x))/10 + abs(int(self.figureList[z].pos.y) - int(output.figureList[z].pos.y))/10
            else:
                score += self.figureList[z].h * self.figureList[z].w * 1.2
        if len(output.figureList) - len(self.figureList) > 0:
            for z in range(len(self.figureList), len(output.figureList)):
                score += output.figureList[z].h * output.figureList[z].w * 1.5
        return -score
    
    #fitness function unbias
    def score_unbias(self, output):
        score = abs(output.nr - self.nr) + abs(output.nc - self.nc)
        for z in range(0, len(self.figureList)):
            if z < len(output.figureList):
                for x in range(0, min(self.figureList[z].h, output.figureList[z].h)):
                    for y in range(0, min(self.figureList[z].w, output.figureList[z].w)):
                        if self.figureList[z].grid[x][y] == 1 and output.figureList[z].grid[x][y] == 1:
                            score += abs(int(self.figureList[z].color) - int(output.figureList[z].color))
                        else:
                            if self.figureList[z].grid[x][y] != output.figureList[z].grid[x][y]:
                                score += 1
                #figure con diverse dimensioni
                score += abs(self.figureList[z].h - output.figureList[z].h) + abs(self.figureList[z].w - output.figureList[z].w)
                #distance
                score += abs(int(self.figureList[z].pos.x) - int(output.figureList[z].pos.x)) + abs(int(self.figureList[z].pos.y) - int(output.figureList[z].pos.y))
            else:
                score += self.figureList[z].h * self.figureList[z].w
        if len(output.figureList) - len(self.figureList) > 0:
            for z in range(len(self.figureList), len(output.figureList)):
                score += output.figureList[z].h * output.figureList[z].w
        return -score

    #transform the representation into an ARC grid
    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for f in self.figureList:
            for x in range(0, f.h):
                for y in range(0, f.w):
                    if f.grid[x][y] != 0:
                        grid[f.pos.x + x][f.pos.y + y] = f.color
        return grid
    
    #function that calculates a score based on the selectors used
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_selection[x].allElement < 3: 
                score += 0.5
            if performed_actions[x] == figureRepresentation.rotateFigure or performed_actions[x] == figureRepresentation.removeFigure or performed_actions[x] == figureRepresentation.mergeFigure or performed_actions[x] == figureRepresentation.divideFigure_row or performed_actions[x] == figureRepresentation.divideFigure_column:
                score += 0.5
            score += 1
        return -score
    
    #return the list of actions
    def actionList(pc):     
        l = [figureRepresentation.moveFigure, figureRepresentation.moveElementFigure_row, figureRepresentation.moveElementFigure_column, figureRepresentation.rotateFigure, figureRepresentation.mergeFigure,  figureRepresentation.changeOrder]    
        # figureRepresentation.divideFigure_row, figureRepresentation.divideFigure_column,
        if pc.countDim != pc.numProb:
            l.append(figureRepresentation.expandGrid)
            l.append(figureRepresentation.reduceGrid)
        if pc.countColor != pc.numProb:
            l.append(figureRepresentation.changeColorFigure)
        if pc.countRemove > 0:
            l.append(figureRepresentation.removeElementFigure_row)
            l.append(figureRepresentation.removeElementFigure_column)
            l.append(figureRepresentation.removeFigure)
        if pc.countAdd > 0:
            l.append(figureRepresentation.addElementFigure_row)
            l.append(figureRepresentation.addElementFigure_column)
            l.append(figureRepresentation.duplicateFigure)
        return l
    
    #return the list of base actions
    def baseActionList(pc):
        l = [figureRepresentation.moveFigure, figureRepresentation.changeOrder]
        if pc.countColor != pc.numProb:
            l.append(figureRepresentation.changeColorFigure)
        if pc.countAdd > 0:
            l.append(figureRepresentation.duplicateFigure)
        if pc.countDim != pc.numProb:
            l.append(figureRepresentation.expandGrid)
            l.append(figureRepresentation.reduceGrid)
        return l