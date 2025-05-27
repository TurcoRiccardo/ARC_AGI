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
    gtype: np.ndarray
    pos: PixelNode
    h: int
    w: int

#fills a list with the pixels of the figure
def ricFindFigure(grid, posX, posY, pixel, mask, nc, nr):
    if mask[posX][posY] == 1:
        mask[posX][posY] = 0
        pixel.append(PixelNode(posX, posY, grid[posX][posY]))
    if posX+1 < nr:
        #down
        if grid[posX+1][posY] != 0 and mask[posX+1][posY] == 1:
            ricFindFigure(grid, posX+1, posY, pixel, mask, nc, nr)
    if posX+1 < nr and posY+1 < nc:
        #down-right
        if grid[posX+1][posY+1] != 0 and mask[posX+1][posY+1] == 1:
            ricFindFigure(grid, posX+1, posY+1, pixel, mask, nc, nr)
    if posX+1 < nr and posY > 0:
        #down-left
        if grid[posX+1][posY-1] != 0 and mask[posX+1][posY-1] == 1:
            ricFindFigure(grid, posX+1, posY-1, pixel, mask, nc, nr)
    if posX > 0:
        #up
        if grid[posX-1][posY] != 0 and mask[posX-1][posY] == 1:
            ricFindFigure(grid, posX-1, posY, pixel, mask, nc, nr)
    if posX > 0 and posY+1 < nc:
        #up-right
        if grid[posX-1][posY+1] != 0 and mask[posX-1][posY+1] == 1:
            ricFindFigure(grid, posX-1, posY+1, pixel, mask, nc, nr)
    if posX > 0 and posY > 0:
        #up-left
        if grid[posX-1][posY-1] != 0 and mask[posX-1][posY-1] == 1:
            ricFindFigure(grid, posX-1, posY-1, pixel, mask, nc, nr)
    if posY+1 < nc:
        #right
        if grid[posX][posY+1] != 0 and mask[posX][posY+1] == 1:
            ricFindFigure(grid, posX, posY+1, pixel, mask, nc, nr)
    if posY > 0:
        #left
        if grid[posX][posY-1] != 0 and mask[posX][posY-1] == 1:
            ricFindFigure(grid, posX, posY-1, pixel, mask, nc, nr)
    return 

#return 0 if we are in a closed border
def ricEscapeLine(grid, posX, posY):
    cnt = 0
    if posX == 0 or posX == grid.shape[0]-1 or posY == 0 or posY == grid.shape[1]-1:
        return cnt + 1
    grid[posX][posY] = 1
    #up
    if grid[posX+1][posY] == 0:
        cnt += ricEscapeLine(grid, posX+1, posY)
    #right
    if cnt == 0 and grid[posX][posY+1] == 0:
        cnt += ricEscapeLine(grid, posX, posY+1)
    #down
    if cnt == 0 and grid[posX-1][posY] == 0:
        cnt += ricEscapeLine(grid, posX-1, posY)
    #left
    if cnt == 0 and grid[posX][posY-1] == 0:
        cnt += ricEscapeLine(grid, posX, posY-1)
    return cnt

class coloredFigureRepresentation:
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
                    ricFindFigure(input_grid, x, y, pixelList, mask, self.nc, self.nr)
                    for p in pixelList:
                        if xMax < p.x:
                            xMax = p.x
                        if xMin > p.x:
                            xMin = p.x
                        if yMax < p.y:
                            yMax = p.y
                        if yMin > p.y:
                            yMin = p.y
                    fig = Figure(np.zeros((xMax-xMin+1, yMax-yMin+1), dtype=int), np.zeros((xMax-xMin+1, yMax-yMin+1), dtype=int), PixelNode(xMin, yMin), xMax-xMin+1, yMax-yMin+1)
                    for p in pixelList:
                        fig.grid[p.x - xMin][p.y - yMin] = p.color
                    for x in range(0, fig.h):
                        for y in range(0, fig.w):
                            if fig.grid[x][y] > 0:
                                if ricEscapeLine(fig.grid.copy(), x, y) > 0:
                                    #border pixel
                                    fig.gtype[x][y] = 1
                                else:
                                    #center pixel
                                    fig.gtype[x][y] = 2
                    self.figureList.append(fig)

    #return the total number of figure
    def getNElement(self):
        return len(self.figureList)
    
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
            for i in range(0, len(self.figureList)):
                ok = 0
                for x in range(0, self.figureList[i].h):
                    for y in range(0, self.figureList[i].w):
                        if self.figureList[i].grid[x][y] == s.color:
                            ok = 1
                            break
                if ok == 1:
                    l.append(i)
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
    
    #changes the color of the border of the figure index based on color
    def changeColorFigureBorder(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            for x in range(0, self.figureList[adapted_index].h):
                for y in range(0, self.figureList[adapted_index].w):
                    if self.figureList[adapted_index].grid[x][y] > 0 and self.figureList[adapted_index].gtype[x][y] == 1:
                        if s.color % 2 == 0:
                            if self.figureList[adapted_index].grid[x][y] != 9:
                                self.figureList[adapted_index].grid[x][y] += 1
                                count += 1
                        else:
                            if self.figureList[adapted_index].grid[x][y] != 1:
                                self.figureList[adapted_index].grid[x][y] -= 1
                                count += 1  
        if count != 0:
            return 0
        return 1
    
    #changes the color of the center of the figure index based on color
    def changeColorFigureCenter(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            for x in range(0, self.figureList[adapted_index].h):
                for y in range(0, self.figureList[adapted_index].w):
                    if self.figureList[adapted_index].grid[x][y] > 0 and self.figureList[adapted_index].gtype[x][y] == 2:
                        if s.color % 2 == 0:
                            if self.figureList[adapted_index].grid[x][y] != 9:
                                self.figureList[adapted_index].grid[x][y] += 1
                                count += 1
                        else:
                            if self.figureList[adapted_index].grid[x][y] != 1:
                                self.figureList[adapted_index].grid[x][y] -= 1
                                count += 1
        if count != 0:
            return 0
        return 1
    
    #changes the color of a pixel in the figure index based on color
    def changeColorFigure_row_column(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            lcr = self.generateComponentList_row(s, adapted_index)
            lcc = self.generateComponentList_column(s, adapted_index)
            for adapted_component_row in lcr:
                for adapted_component_column in lcc:
                    if self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] > 0:
                        if s.color % 2 == 0:
                            if self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] != 9:
                                self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] += 1
                                count += 1
                        else:
                            if self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] != 1:
                                self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] -= 1
                                count += 1
        if count != 0:
            return 0
        return 1

    #fill the center of the figure index based on color
    def fillFigureCenter(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            for x in range(0, self.figureList[adapted_index].h):
                for y in range(0, self.figureList[adapted_index].w):
                    if self.figureList[adapted_index].grid[x][y] == 0:
                        if ricEscapeLine(self.figureList[adapted_index].grid.copy(), x, y) == 0:
                            self.figureList[adapted_index].grid[x][y] = s.color
                            self.figureList[adapted_index].gtype[x][y] = 2
                            count += 1
        if count != 0:
            return 0
        return 1

    #expand the figure in the direction direction
    def expandFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if (s.direction % 4) == 0:
                #down    
                if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].h < self.nr:
                    self.figureList[adapted_index].grid = np.vstack([self.figureList[adapted_index].grid, np.zeros((1, self.figureList[adapted_index].w), dtype=int)])
                    self.figureList[adapted_index].gtype = np.vstack([self.figureList[adapted_index].gtype, np.zeros((1, self.figureList[adapted_index].w), dtype=int)])
                    self.figureList[adapted_index].h += 1
                    count += 1
            elif (s.direction % 4) == 1:
                #up
                if self.figureList[adapted_index].pos.x > 0:
                    self.figureList[adapted_index].grid = np.vstack([np.zeros((1, self.figureList[adapted_index].w), dtype=int), self.figureList[adapted_index].grid])
                    self.figureList[adapted_index].gtype = np.vstack([np.zeros((1, self.figureList[adapted_index].w), dtype=int), self.figureList[adapted_index].gtype])
                    self.figureList[adapted_index].pos.x -= 1
                    self.figureList[adapted_index].h += 1
                    count += 1
            elif (s.direction % 4) == 2:
                #right
                if self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w < self.nc:
                    self.figureList[adapted_index].grid = np.hstack([self.figureList[adapted_index].grid, np.zeros((1, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, 1)])
                    self.figureList[adapted_index].gtype = np.hstack([self.figureList[adapted_index].gtype, np.zeros((1, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, 1)])
                    self.figureList[adapted_index].w += 1
                    count += 1
            elif (s.direction % 4) == 3:
                #left
                if self.figureList[adapted_index].pos.y > 0:
                    self.figureList[adapted_index].grid = np.hstack([np.zeros((1, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, 1), self.figureList[adapted_index].grid])
                    self.figureList[adapted_index].gtype = np.hstack([np.zeros((1, self.figureList[adapted_index].h), dtype=int).reshape(self.figureList[adapted_index].h, 1), self.figureList[adapted_index].gtype])
                    self.figureList[adapted_index].pos.y -= 1
                    self.figureList[adapted_index].w += 1
                    count += 1
        if count != 0:
            return 0
        return 1

    #reduce the figure in the direction direction
    def reduceFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if (s.direction % 4) == 0:
                #down    
                if self.figureList[adapted_index].h > 1:
                    ok = 0
                    for y in range(0, self.figureList[adapted_index].w):
                        if self.figureList[adapted_index].grid[-1][y] > 0:
                            ok = 1
                            break
                    if ok == 0:
                        self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[0:self.figureList[adapted_index].h - 1,:]
                        self.figureList[adapted_index].gtype = self.figureList[adapted_index].gtype[0:self.figureList[adapted_index].h - 1,:]
                        self.figureList[adapted_index].h -= 1
                        count += 1
            elif (s.direction % 4) == 1:
                #up
                if self.figureList[adapted_index].h > 1:
                    ok = 0
                    for y in range(0, self.figureList[adapted_index].w):
                        if self.figureList[adapted_index].grid[0][y] > 0:
                            ok = 1
                            break
                    if ok == 0:
                        self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[1:self.figureList[adapted_index].h,:]
                        self.figureList[adapted_index].gtype = self.figureList[adapted_index].gtype[1:self.figureList[adapted_index].h,:]
                        self.figureList[adapted_index].pos.x += 1
                        self.figureList[adapted_index].h -= 1
                        count += 1
            elif (s.direction % 4) == 2:
                #right
                if self.figureList[adapted_index].w > 1:
                    ok = 0
                    for x in range(0, self.figureList[adapted_index].h):
                        if self.figureList[adapted_index].grid[x][-1] > 0:
                            ok = 1
                            break
                    if ok == 0:
                        self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[:,0:self.figureList[adapted_index].w - 1]
                        self.figureList[adapted_index].gtype = self.figureList[adapted_index].gtype[:,0:self.figureList[adapted_index].w - 1]
                        self.figureList[adapted_index].w -= 1
                        count += 1
            elif (s.direction % 4) == 3:
                #left
                if self.figureList[adapted_index].w > 1:
                    ok = 0
                    for x in range(0, self.figureList[adapted_index].h):
                        if self.figureList[adapted_index].grid[x][0] > 0:
                            ok = 1
                            break
                    if ok == 0:
                        self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[:,1:self.figureList[adapted_index].w]
                        self.figureList[adapted_index].gtype = self.figureList[adapted_index].gtype[:,1:self.figureList[adapted_index].w]
                        self.figureList[adapted_index].pos.y += 1
                        self.figureList[adapted_index].w -= 1
                        count += 1
        if count != 0:
            return 0
        return 1

    #add a element in the figure in the selected row and column
    def addElementFigure_row_column(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            lcr = self.generateComponentList_row(s, adapted_index)
            lcc = self.generateComponentList_column(s, adapted_index)
            if (s.direction % 4) == 0:
                lcr.sort(key=lambda i: i, reverse=True)
            elif (s.direction % 4) == 1:
                lcr.sort(key=lambda i: i, reverse=False)
            elif (s.direction % 4) == 2:
                lcc.sort(key=lambda i: i, reverse=True)
            elif (s.direction % 4) == 3:
                lcc.sort(key=lambda i: i, reverse=False)
            for adapted_component_row in lcr:
                for adapted_component_column in lcc:
                    if self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] > 0:
                        if (s.direction % 4) == 0:
                            if s.color % 2 == 0:
                                #down
                                if adapted_component_row + 1 < self.figureList[adapted_index].h:
                                    if self.figureList[adapted_index].grid[adapted_component_row + 1][adapted_component_column] == 0:
                                        self.figureList[adapted_index].grid[adapted_component_row + 1][adapted_component_column] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column]
                                        count += 1
                            else:
                                #down left
                                if adapted_component_row + 1 < self.figureList[adapted_index].h and adapted_component_column > 0:
                                    if self.figureList[adapted_index].grid[adapted_component_row + 1][adapted_component_column - 1] == 0:
                                        self.figureList[adapted_index].grid[adapted_component_row + 1][adapted_component_column - 1] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] 
                                        count += 1
                        elif (s.direction % 4) == 1:
                            if s.color % 2 == 0:
                                #up
                                if adapted_component_row > 0:
                                    if self.figureList[adapted_index].grid[adapted_component_row - 1][adapted_component_column] == 0:
                                        self.figureList[adapted_index].grid[adapted_component_row - 1][adapted_component_column] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] 
                                        count += 1
                            else:
                                #up right
                                if adapted_component_row > 0 and adapted_component_column + 1 < self.figureList[adapted_index].w:
                                    if self.figureList[adapted_index].grid[adapted_component_row - 1][adapted_component_column + 1] == 0:
                                        self.figureList[adapted_index].grid[adapted_component_row - 1][adapted_component_column + 1] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] 
                                        count += 1
                        elif (s.direction % 4) == 2:
                            if s.color % 2 == 0:
                                #right
                                if adapted_component_column + 1 < self.figureList[adapted_index].w:
                                    if self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column + 1] == 0:
                                        self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column + 1] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] 
                                        count += 1
                            else:
                                #right down
                                if adapted_component_column + 1 < self.figureList[adapted_index].w and adapted_component_row + 1 < self.figureList[adapted_index].h:
                                    if self.figureList[adapted_index].grid[adapted_component_row + 1][adapted_component_column + 1] == 0:
                                        self.figureList[adapted_index].grid[adapted_component_row + 1][adapted_component_column + 1] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] 
                                        count += 1
                        elif (s.direction % 4) == 3:
                            if s.color % 2 == 0:
                                #left
                                if adapted_component_column > 0:
                                    if self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column - 1] == 0:
                                        self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column - 1] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] 
                                        count += 1
                            else:
                                #left up
                                if adapted_component_column > 0 and adapted_component_row > 0:
                                    if self.figureList[adapted_index].grid[adapted_component_row - 1][adapted_component_column - 1] == 0:
                                        self.figureList[adapted_index].grid[adapted_component_row - 1][adapted_component_column - 1] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] 
                                        count += 1
        if count != 0:
            for adapted_index in l:
                for x in range(0, self.figureList[adapted_index].h):
                    for y in range(0, self.figureList[adapted_index].w):
                        if self.figureList[adapted_index].grid[x][y] > 0:
                            if ricEscapeLine(self.figureList[adapted_index].grid.copy(), x, y) > 0:
                                #border pixel
                                self.figureList[adapted_index].gtype[x][y] = 1
                            else:
                                #center pixel
                                self.figureList[adapted_index].gtype[x][y] = 2
                        else:
                            self.figureList[adapted_index].gtype[x][y] = 0
            return 0
        return 1

    #move a pixel in the figure based on the direction
    def moveElementFigure_row_column(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            lcr = self.generateComponentList_row(s, adapted_index)
            lcc = self.generateComponentList_column(s, adapted_index)
            if (s.direction % 4) == 0:
                lcr.sort(key=lambda i: i, reverse=True)
            elif (s.direction % 4) == 1:
                lcr.sort(key=lambda i: i, reverse=False)
            elif (s.direction % 4) == 2:
                lcc.sort(key=lambda i: i, reverse=True)
            elif (s.direction % 4) == 3:
                lcc.sort(key=lambda i: i, reverse=False)
            for adapted_component_row in lcr:
                for adapted_component_column in lcc:
                    if (s.direction % 4) == 0:
                        #down
                        if adapted_component_row + 1 < self.figureList[adapted_index].h:
                            tmp = self.figureList[adapted_index].grid[adapted_component_row + 1][adapted_component_column]
                            self.figureList[adapted_index].grid[adapted_component_row + 1][adapted_component_column] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] 
                            self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] = tmp
                            count += 1
                    elif (s.direction % 4) == 1:
                        #up
                        if adapted_component_row > 0:
                            tmp = self.figureList[adapted_index].grid[adapted_component_row - 1][adapted_component_column]
                            self.figureList[adapted_index].grid[adapted_component_row - 1][adapted_component_column] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] 
                            self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] = tmp
                            count += 1
                    elif (s.direction % 4) == 2:
                        #right
                        if adapted_component_column + 1 < self.figureList[adapted_index].w:
                            tmp = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column + 1]
                            self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column + 1] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] 
                            self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] = tmp
                            count += 1
                    elif (s.direction % 4) == 3:
                        #left
                        if adapted_component_column > 0:
                            tmp = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column - 1]
                            self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column - 1] = self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] 
                            self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] = tmp
                            count += 1
        if count != 0:
            for adapted_index in l:
                for x in range(0, self.figureList[adapted_index].h):
                    for y in range(0, self.figureList[adapted_index].w):
                        if self.figureList[adapted_index].grid[x][y] > 0:
                            if ricEscapeLine(self.figureList[adapted_index].grid.copy(), x, y) > 0:
                                #border pixel
                                self.figureList[adapted_index].gtype[x][y] = 1
                            else:
                                #center pixel
                                self.figureList[adapted_index].gtype[x][y] = 2
                        else:
                            self.figureList[adapted_index].gtype[x][y] = 0
            return 0
        return 1

    #remove the element in the figure in the selected row and column
    def removeElementFigure_row_column(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            lcr = self.generateComponentList_row(s, adapted_index)
            lcc = self.generateComponentList_column(s, adapted_index)
            for adapted_component_row in lcr:
                for adapted_component_column in lcc:
                    if self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] > 0:
                        self.figureList[adapted_index].grid[adapted_component_row][adapted_component_column] = 0
                        count += 1
        if count != 0:
            for adapted_index in l:
                for x in range(0, self.figureList[adapted_index].h):
                    for y in range(0, self.figureList[adapted_index].w):
                        if self.figureList[adapted_index].grid[x][y] > 0:
                            if ricEscapeLine(self.figureList[adapted_index].grid.copy(), x, y) > 0:
                                #border pixel
                                self.figureList[adapted_index].gtype[x][y] = 1
                            else:
                                #center pixel
                                self.figureList[adapted_index].gtype[x][y] = 2
                        else:
                            self.figureList[adapted_index].gtype[x][y] = 0
            return 0
        return 1

    #duplicate the selected figure based on the direction direction
    def duplicateFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        duplicatedFigure = []
        for adapted_index in l:
            fig = Figure(self.figureList[adapted_index].grid.copy(), self.figureList[adapted_index].gtype.copy(), PixelNode(self.figureList[adapted_index].pos.x, self.figureList[adapted_index].pos.y), self.figureList[adapted_index].h, self.figureList[adapted_index].w)
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
                    #rotate grid
                    newGrid = np.zeros([self.figureList[adapted_index].w, self.figureList[adapted_index].h], dtype=np.uint8)
                    for x in range(self.figureList[adapted_index].h):
                        for y in range(self.figureList[adapted_index].w):
                            newGrid[y][self.figureList[adapted_index].h - x - 1] = self.figureList[adapted_index].grid[x][y]
                    self.figureList[adapted_index].grid = newGrid
                    #rotate gtype
                    newGrid = np.zeros([self.figureList[adapted_index].w, self.figureList[adapted_index].h], dtype=np.uint8)
                    for x in range(self.figureList[adapted_index].h):
                        for y in range(self.figureList[adapted_index].w):
                            newGrid[y][self.figureList[adapted_index].h - x - 1] = self.figureList[adapted_index].gtype[x][y]
                    self.figureList[adapted_index].gtype = newGrid
                    #reverse dimensions
                    tmp = self.figureList[adapted_index].h
                    self.figureList[adapted_index].h = self.figureList[adapted_index].w
                    self.figureList[adapted_index].w = tmp
                    count += 1
            elif (s.direction % 2) == 1:
                #rotate to the left
                if self.figureList[adapted_index].pos.x + self.figureList[adapted_index].w <= self.nr and self.figureList[adapted_index].pos.y + self.figureList[adapted_index].h <= self.nc:
                    #rotate grid
                    newGrid = np.zeros([self.figureList[adapted_index].w, self.figureList[adapted_index].h], dtype=np.uint8)
                    for x in range(self.figureList[adapted_index].h):
                        for y in range(self.figureList[adapted_index].w):
                            newGrid[self.figureList[adapted_index].w - y - 1][x] = self.figureList[adapted_index].grid[x][y]
                    self.figureList[adapted_index].grid = newGrid
                    #rotate gtype
                    newGrid = np.zeros([self.figureList[adapted_index].w, self.figureList[adapted_index].h], dtype=np.uint8)
                    for x in range(self.figureList[adapted_index].h):
                        for y in range(self.figureList[adapted_index].w):
                            newGrid[self.figureList[adapted_index].w - y - 1][x] = self.figureList[adapted_index].gtype[x][y]
                    self.figureList[adapted_index].gtype = newGrid
                    #reverse dimensions
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
                                    if adapted_index != indfig:
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
                                            self.figureList[adapted_index].grid[diffx + x][diffy + y] = self.figureList[f].grid[x][y]
                                #ricreo gtype
                                newGrid = np.zeros([self.figureList[adapted_index].h, self.figureList[adapted_index].w], dtype=np.uint8)
                                for x in range(0, self.figureList[adapted_index].h):
                                    for y in range(0, self.figureList[adapted_index].w):
                                        if self.figureList[adapted_index].grid[x][y] > 0:
                                            if ricEscapeLine(self.figureList[adapted_index].grid.copy(), x, y) > 0:
                                                #border pixel
                                                newGrid[x][y] = 1
                                            else:
                                                #center pixel
                                                newGrid[x][y] = 2
                                self.figureList[adapted_index].gtype = newGrid
                            count += 1
                elif (s.direction % 4) == 1:
                    #up
                    if self.figureList[adapted_index].pos.x > 0:
                        indexFigure = set()
                        for y in range(0, self.figureList[adapted_index].w):
                            if self.figureList[adapted_index].grid[0][y] > 0:
                                for indfig in range(0, len(self.figureList)):
                                    if adapted_index != indfig:
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
                                            self.figureList[adapted_index].grid[diffx + x][diffy + y] = self.figureList[f].grid[x][y]
                                #ricreo gtype
                                newGrid = np.zeros([self.figureList[adapted_index].h, self.figureList[adapted_index].w], dtype=np.uint8)
                                for x in range(0, self.figureList[adapted_index].h):
                                    for y in range(0, self.figureList[adapted_index].w):
                                        if self.figureList[adapted_index].grid[x][y] > 0:
                                            if ricEscapeLine(self.figureList[adapted_index].grid.copy(), x, y) > 0:
                                                #border pixel
                                                newGrid[x][y] = 1
                                            else:
                                                #center pixel
                                                newGrid[x][y] = 2
                                self.figureList[adapted_index].gtype = newGrid
                            count += 1
                elif (s.direction % 4) == 2:
                    #right
                    if self.figureList[adapted_index].pos.y + self.figureList[adapted_index].w < self.nc:
                        indexFigure = set()
                        for x in range(0, self.figureList[adapted_index].h):
                            if self.figureList[adapted_index].grid[x][-1] > 0:
                                for indfig in range(0, len(self.figureList)):
                                    if adapted_index != indfig:
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
                                            self.figureList[adapted_index].grid[diffx + x][diffy + y] = self.figureList[f].grid[x][y]
                                #ricreo gtype
                                newGrid = np.zeros([self.figureList[adapted_index].h, self.figureList[adapted_index].w], dtype=np.uint8)
                                for x in range(0, self.figureList[adapted_index].h):
                                    for y in range(0, self.figureList[adapted_index].w):
                                        if self.figureList[adapted_index].grid[x][y] > 0:
                                            if ricEscapeLine(self.figureList[adapted_index].grid.copy(), x, y) > 0:
                                                #border pixel
                                                newGrid[x][y] = 1
                                            else:
                                                #center pixel
                                                newGrid[x][y] = 2
                                self.figureList[adapted_index].gtype = newGrid
                            count += 1
                elif (s.direction % 4) == 3:
                    #left
                    if self.figureList[adapted_index].pos.y > 0:
                        indexFigure = set()
                        for x in range(0, self.figureList[adapted_index].h):
                            if self.figureList[adapted_index].grid[x][0] > 0:
                                for indfig in range(0, len(self.figureList)):
                                    if adapted_index != indfig:
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
                                            self.figureList[adapted_index].grid[diffx + x][diffy + y] = self.figureList[f].grid[x][y]
                                #ricreo gtype
                                newGrid = np.zeros([self.figureList[adapted_index].h, self.figureList[adapted_index].w], dtype=np.uint8)
                                for x in range(0, self.figureList[adapted_index].h):
                                    for y in range(0, self.figureList[adapted_index].w):
                                        if self.figureList[adapted_index].grid[x][y] > 0:
                                            if ricEscapeLine(self.figureList[adapted_index].grid.copy(), x, y) > 0:
                                                #border pixel
                                                newGrid[x][y] = 1
                                            else:
                                                #center pixel
                                                newGrid[x][y] = 2
                                self.figureList[adapted_index].gtype = newGrid
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
                    fig = Figure(self.figureList[adapted_index].grid[adapted_component+1:self.figureList[adapted_index].h,:], self.figureList[adapted_index].gtype[adapted_component+1:self.figureList[adapted_index].h,:], PixelNode(self.figureList[adapted_index].pos.x+adapted_component+1, self.figureList[adapted_index].pos.y), self.figureList[adapted_index].h-(adapted_component+1), self.figureList[adapted_index].w)
                    self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[0:adapted_component+1,:]
                    self.figureList[adapted_index].gtype = self.figureList[adapted_index].gtype[0:adapted_component+1,:]
                    self.figureList[adapted_index].h -= (self.figureList[adapted_index].h - (adapted_component+1))
                    dividedFigure.append((adapted_index+1, fig))
                    count += 1
        if count != 0:
            for adapted_index in l:
                for x in range(0, self.figureList[adapted_index].h):
                    for y in range(0, self.figureList[adapted_index].w):
                        if self.figureList[adapted_index].grid[x][y] > 0:
                            if ricEscapeLine(self.figureList[adapted_index].grid.copy(), x, y) > 0:
                                #border pixel
                                self.figureList[adapted_index].gtype[x][y] = 1
                            else:
                                #center pixel
                                self.figureList[adapted_index].gtype[x][y] = 2
                        else:
                            self.figureList[adapted_index].gtype[x][y] = 0
            dividedFigure.sort(key=lambda i: i[0], reverse=True)
            for (index, fig) in dividedFigure:
                for x in range(0, fig.h):
                    for y in range(0, fig.w):
                        if fig.grid[x][y] > 0:
                            if ricEscapeLine(fig.grid.copy(), x, y) > 0:
                                #border pixel
                                fig.gtype[x][y] = 1
                            else:
                                #center pixel
                                fig.gtype[x][y] = 2
                        else:
                            fig.gtype[x][y] = 0
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
                    fig = Figure(self.figureList[adapted_index].grid[:,adapted_component+1:self.figureList[adapted_index].w], self.figureList[adapted_index].gtype[:,adapted_component+1:self.figureList[adapted_index].w], PixelNode(self.figureList[adapted_index].pos.x, self.figureList[adapted_index].pos.y+adapted_component+1), self.figureList[adapted_index].h, self.figureList[adapted_index].w-(adapted_component+1))
                    self.figureList[adapted_index].grid = self.figureList[adapted_index].grid[:,0:adapted_component+1]
                    self.figureList[adapted_index].gtype = self.figureList[adapted_index].gtype[:,0:adapted_component+1]
                    self.figureList[adapted_index].w -= (self.figureList[adapted_index].w - (adapted_component+1))
                    dividedFigure.append((adapted_index+1, fig))
                    count += 1
        if count != 0:
            for adapted_index in l:
                for x in range(0, self.figureList[adapted_index].h):
                    for y in range(0, self.figureList[adapted_index].w):
                        if self.figureList[adapted_index].grid[x][y] > 0:
                            if ricEscapeLine(self.figureList[adapted_index].grid.copy(), x, y) > 0:
                                #border pixel
                                self.figureList[adapted_index].gtype[x][y] = 1
                            else:
                                #center pixel
                                self.figureList[adapted_index].gtype[x][y] = 2
                        else:
                            self.figureList[adapted_index].gtype[x][y] = 0
            dividedFigure.sort(key=lambda i: i[0], reverse=True)
            for (index, fig) in dividedFigure:
                for x in range(0, fig.h):
                    for y in range(0, fig.w):
                        if fig.grid[x][y] > 0:
                            if ricEscapeLine(fig.grid.copy(), x, y) > 0:
                                #border pixel
                                fig.gtype[x][y] = 1
                            else:
                                #center pixel
                                fig.gtype[x][y] = 2
                        else:
                            fig.gtype[x][y] = 0
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
                '''
                #creo liste pixel 
                pli = []
                for x in range(0, self.figureList[z].h):
                    for y in range(0, self.figureList[z].w):
                        if self.figureList[z].grid[x][y] > 0:
                            pli.append((x, y, self.figureList[z].grid[x][y]))
                plo = []
                for x in range(0, output.figureList[z].h):
                    for y in range(0, output.figureList[z].w):
                        if output.figureList[z].grid[x][y] > 0:
                            plo.append((x, y, output.figureList[z].grid[x][y]))        
                for k in range(0, len(pli)):
                    if k < len(plo):
                        #distance
                        score += abs(int(pli[k][0]) - int(plo[k][0]))/10 + abs(int(pli[k][1]) - int(plo[k][1]))/10
                        #color
                        score += abs(int(pli[k][2]) - int(plo[k][2]))/10
                    else:
                        score += 1
                if len(plo) > len(pli):
                    for k in range(len(pli), len(plo)):
                        score += 1
                '''
                #Verifica se due figure hanno la stessa forma normalizzando le coordinate rispetto al punto in alto a sinistra (anche esterno dalla figura)
                for x in range(0, min(self.figureList[z].h, output.figureList[z].h)):
                    for y in range(0, min(self.figureList[z].w, output.figureList[z].w)):
                        if self.figureList[z].grid[x][y] > 0 and output.figureList[z].grid[x][y] > 0:
                            score += abs(int(self.figureList[z].grid[x][y]) - int(output.figureList[z].grid[x][y]))/10
                        else:
                            if self.figureList[z].grid[x][y] != output.figureList[z].grid[x][y]:
                                score += 1
                #figure con diverse dimensioni
                score += abs(self.figureList[z].h - output.figureList[z].h)*min(self.figureList[z].w, output.figureList[z].w) + abs(self.figureList[z].w - output.figureList[z].w)*min(self.figureList[z].h, output.figureList[z].h) + abs(output.figureList[z].h - self.figureList[z].h)*abs(output.figureList[z].w - self.figureList[z].w)

                #distance figure
                score += abs(int(self.figureList[z].pos.x) - int(output.figureList[z].pos.x))/10 + abs(int(self.figureList[z].pos.y) - int(output.figureList[z].pos.y))/10
            else:
                score += self.figureList[z].h * self.figureList[z].w * 1.2
        if len(output.figureList) - len(self.figureList) > 0:
            for z in range(len(self.figureList), len(output.figureList)):
                score += output.figureList[z].h * output.figureList[z].w * 1.5
        return -score

    #transform the representation into an ARC grid
    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for f in self.figureList:
            for x in range(0, f.h):
                for y in range(0, f.w):
                    grid[f.pos.x + x][f.pos.y + y] = f.grid[x][y]
        return grid
    
    #function that calculates a score based on the selectors used
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_selection[x].allElement < 3: 
                score += 0.5
            if performed_actions[x] == coloredFigureRepresentation.rotateFigure or performed_actions[x] == coloredFigureRepresentation.removeFigure or performed_actions[x] == coloredFigureRepresentation.mergeFigure or performed_actions[x] == coloredFigureRepresentation.removeElementFigure_row_column or performed_actions[x] == coloredFigureRepresentation.divideFigure_row or performed_actions[x] == coloredFigureRepresentation.divideFigure_column:
                score += 0.5
            score += 1
        return -score
    
    #return the list of actions
    def actionList(pc):     
        l = [coloredFigureRepresentation.moveFigure, coloredFigureRepresentation.expandFigure, coloredFigureRepresentation.reduceFigure, coloredFigureRepresentation.moveElementFigure_row_column, coloredFigureRepresentation.rotateFigure, coloredFigureRepresentation.mergeFigure, coloredFigureRepresentation.divideFigure_row, coloredFigureRepresentation.divideFigure_column, coloredFigureRepresentation.changeOrder]
        if pc.countDim != pc.numProb:
            l.append(coloredFigureRepresentation.expandGrid)
            l.append(coloredFigureRepresentation.reduceGrid)
        if pc.countColor != pc.numProb:
            l.append(coloredFigureRepresentation.changeColorFigureBorder)
            l.append(coloredFigureRepresentation.changeColorFigureCenter)
            l.append(coloredFigureRepresentation.changeColorFigure_row_column)
        if pc.countRemove > 0:
            l.append(coloredFigureRepresentation.removeElementFigure_row_column)
            l.append(coloredFigureRepresentation.removeFigure)
        if pc.countAdd > 0:
            l.append(coloredFigureRepresentation.fillFigureCenter)
            l.append(coloredFigureRepresentation.addElementFigure_row_column)
            l.append(coloredFigureRepresentation.duplicateFigure)
        return l
    
    #return the list of base actions
    def baseActionList(pc):
        l = [coloredFigureRepresentation.moveFigure, coloredFigureRepresentation.expandFigure, coloredFigureRepresentation.reduceFigure, coloredFigureRepresentation.changeOrder]
        if pc.countAdd > 0:
            l.append(coloredFigureRepresentation.duplicateFigure)
        if pc.countDim != pc.numProb:
            l.append(coloredFigureRepresentation.expandGrid)
            l.append(coloredFigureRepresentation.reduceGrid)
        return l