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
                    fig = Figure(np.zeros((xMax-xMin+1, yMax-yMin+1), dtype=int), PixelNode(xMin, yMin), xMax-xMin+1, yMax-yMin+1)
                    for p in pixelList:
                        fig.grid[p.x - xMin][p.y - yMin] = p.color
                    self.figureList.append(fig)

    #return the total number of figure
    def getNElement(self):
        return len(self.figureList)
    
    #return 
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

    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        for z in range(0, len(self.figureList)):
            if z < len(output.figureList):
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
                #distance
                score += abs(int(self.figureList[z].pos.x) - int(output.figureList[z].pos.x))/10 + abs(int(self.figureList[z].pos.y) - int(output.figureList[z].pos.y))/10
            else:
                score += self.figureList[z].h * self.figureList[z].w * 1.2
        if len(output.figureList) - len(self.figureList) > 0:
            for z in range(len(self.figureList), len(output.figureList)):
                score += output.figureList[z].h * output.figureList[z].w * 1.5
        return -score

    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for f in self.figureList:
            for x in range(0, f.h):
                for y in range(0, f.w):
                    grid[f.pos.x + x][f.pos.y + y] = f.grid[x][y]
        return grid
    
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_selection[x].allElement < 3: 
                score += 0.5
            #if performed_actions[x] == coloredFigureRepresentation.rotateFigure or performed_actions[x] == coloredFigureRepresentation.removeFigure or performed_actions[x] == coloredFigureRepresentation.mergeFigure or performed_actions[x] == coloredFigureRepresentation.divideFigure_row or performed_actions[x] == coloredFigureRepresentation.divideFigure_column:
            #    score += 0.5
            score += 1
        return -score

