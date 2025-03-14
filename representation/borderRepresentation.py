import numpy as np
from dataclasses import dataclass
from selection.selector import Selector

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

def ricEscapeLine(grid, posX, posY, cnt):
    if posX == 0 or posX == grid.shape[0]-1 or posY == 0 or posY == grid.shape[1]-1:
        return 1
    grid[posX][posY] = 1
    #up
    if grid[posX+1][posY] == 0:
        cnt = ricEscapeLine(grid, posX+1, posY, cnt)
    #right
    if cnt == 0 and grid[posX][posY+1] == 0:
        cnt = ricEscapeLine(grid, posX, posY+1, cnt)
    #down
    if cnt == 0 and grid[posX-1][posY] == 0:
        cnt = ricEscapeLine(grid, posX-1, posY, cnt)
    #left
    if cnt == 0 and grid[posX][posY-1] == 0:
        cnt = ricEscapeLine(grid, posX, posY-1, cnt)
    return cnt

@dataclass
class PixelNode:
    x: int
    y: int
    color: int = 0

@dataclass
class FigureBorder:
    border: list[PixelNode]
    center: list[PixelNode]
    grid: np.ndarray
    x: int
    y: int

class borderRepresentation:
    def __init__(self, input_grid):
        self.nr = input_grid.shape[0]
        self.nc = input_grid.shape[1]
        self.borderList = list()
        mask = np.ones((self.nr, self.nc), dtype=int)
        for x in range(0, self.nr):
            for y in range(0, self.nc):
                if input_grid[x][y] != 0 and mask[x][y] == 1:
                    pixel = list()
                    ricFindFigure(input_grid, x, y, pixel, mask, self.nc, self.nr)
                    xMax = 0
                    xMin = 1000
                    yMax = 0
                    yMin = 1000
                    for p in pixel:
                        if xMax < p.x:
                            xMax = p.x
                        if xMin > p.x:
                            xMin = p.x
                        if yMax < p.y:
                            yMax = p.y
                        if yMin > p.y:
                            yMin = p.y
                    fb = FigureBorder([], [], np.zeros((xMax-xMin+1, yMax-yMin+1), dtype=int), xMin, yMin)
                    for p1 in pixel:
                        okMaxX = 0
                        okMinX = 0
                        okMaxY = 0
                        okMinY = 0
                        for p2 in pixel:
                            #down
                            if p1.x < p2.x and p1.y == p2.y:
                                okMaxX = 1
                            #up
                            if p1.x > p2.x and p1.y == p2.y:
                                okMinX = 1
                            #right
                            if p1.x == p2.x and p1.y < p2.y:
                                okMaxY = 1
                            #left
                            if p1.x == p2.x and p1.y > p2.y:
                                okMinY = 1
                        if okMaxX == 0 or okMinX == 0 or okMaxY == 0 or okMinY:
                            fb.border.append(p1)
                    #creating a grid with border = 1, center colored pixel = 2, center pixel = 3
                    for p in fb.border:
                        fb.grid[p.x - fb.x][p.y - fb.y] = 1
                    for p in fb.center:
                        fb.grid[p.x - fb.x][p.y - fb.y] = 2
                    for x in range(1, fb.grid.shape[0] - 1):
                        for y in range(1, fb.grid.shape[1] - 1):
                            if fb.grid[x][y] == 0 and ricEscapeLine(fb.grid.copy(), x, y, 0) == 0:
                                fb.grid[x][y] = 3
                    #adding center colored pixel
                    for p in pixel:
                        if p not in fb.border:
                            fb.center.append(p)
                    #adding center pixel
                    for x in range(0, fb.grid.shape[0]):
                        for y in range(0, fb.grid.shape[1]):
                            if fb.grid[x][y] == 3:
                                fb.center.append(PixelNode(x + fb.x, y + fb.y, 0))
                    self.borderList.append(fb)

    #return the total number of border
    def getNElement(self):
        return len(self.borderList)
    
    #return the total number of element in the border index
    def getElementComponent(self, index):
        return len(self.borderList[index].border)
    
    #moves the border index based on the direction
    def moveFigure(self, s):
        if len(self.borderList) == 0:
            return 1
        adapted_index = s.index % len(self.borderList)
        if (s.direction % 4) == 0:
            #down
            if self.borderList[adapted_index].grid.shape[0] + self.borderList[adapted_index].x < self.nr:
                for b in self.borderList[adapted_index].border:
                    b.x += 1
                for c in self.borderList[adapted_index].center:
                    c.x += 1
                self.borderList[adapted_index].x += 1
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.borderList[adapted_index].x > 0:
                for b in self.borderList[adapted_index].border:
                    b.x -= 1
                for c in self.borderList[adapted_index].center:
                    c.x -= 1
                self.borderList[adapted_index].x -= 1
                return 0
        elif (s.direction % 4) == 2:
            #right
           if self.borderList[adapted_index].grid.shape[1] + self.borderList[adapted_index].y < self.nc:
                for b in self.borderList[adapted_index].border:
                    b.y += 1
                for c in self.borderList[adapted_index].center:
                    c.y += 1
                self.borderList[adapted_index].y += 1
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.borderList[adapted_index].y > 0:
                for b in self.borderList[adapted_index].border:
                    b.y -= 1
                for c in self.borderList[adapted_index].center:
                    c.y -= 1
                self.borderList[adapted_index].y -= 1
                return 0
        return 1
    
    #changes the color of the figure border index based on color
    def changeColorBorder(self, s):
        if len(self.borderList) == 0:
            return 1
        adapted_index = s.index % len(self.borderList)
        if s.color % 2 == 0:
            for p in self.borderList[adapted_index].border:
                if p.color != 9:
                    p.color += 1
            return 0
        else:
            for p in self.borderList[adapted_index].border:
                if p.color != 1:
                    p.color -= 1
            return 0
        
    #changes the color of the figure center index based on color
    def changeColorCenter(self, s):
        if len(self.borderList) == 0:
            return 1
        adapted_index = s.index % len(self.borderList)
        if s.color % 2 == 0:
            for p in self.borderList[adapted_index].center:
                if p.color != 9:
                    p.color += 1
            return 0
        else:
            for p in self.borderList[adapted_index].center:
                if p.color != 1:
                    p.color -= 1
            return 0
    





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
                for f in self.borderList:
                    for b in f.border:
                        b.x += 1
                    for c in f.center:
                        c.x += 1
                    f.x += 1
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
                for f in self.borderList:
                    for b in f.border:
                        b.y += 1
                    for c in f.center:
                        c.y += 1
                    f.y += 1
                return 0
        return 1

    #reduce the grid in the direction direction
    def reduceGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            if self.nr > 1:
                ok = 0
                for fb in self.borderList:
                    if fb.grid.shape[0] + fb.x >= self.nr - 1:
                        ok = 1
                if ok == 0:
                    self.nr -= 1
                    return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr > 1:
                ok = 0
                for fb in self.borderList:
                    if fb.x > 0:
                        ok = 1
                if ok == 0:
                    self.nr -= 1
                    for fb in self.borderList:
                        fb.x -= 1
                    return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc > 1:
                ok = 0
                for fb in self.borderList:
                    if fb.grid.shape[1] + fb.y >= self.nc - 1:
                        ok = 1
                if ok == 0:
                    self.nc -= 1
                    return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc > 1:
                ok = 0
                for fb in self.borderList:
                    if fb.y > 0:
                        ok = 1
                if ok == 0:
                    self.nc -= 1
                    for fb in self.borderList:
                        fb.y -= 1
                    return 0
        return 1

    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        for z in range(0, len(self.borderList)):
            if z < len(output.borderList):
                #penalita distanza
                score += abs(int(self.borderList[z].x) - int(output.borderList[z].x))/10 + abs(int(self.borderList[z].y) - int(output.borderList[z].y))/10
                #Verifica se due figure hanno la stessa dimensione
                score += abs(output.borderList[z].grid.shape[0] - self.borderList[z].grid.shape[0])*min(self.borderList[z].grid.shape[1], output.borderList[z].grid.shape[1]) + abs(output.borderList[z].grid.shape[1] - self.borderList[z].grid.shape[1])*min(self.borderList[z].grid.shape[0],  output.borderList[z].grid.shape[0]) + abs(output.borderList[z].grid.shape[0] - self.borderList[z].grid.shape[0])*abs(output.borderList[z].grid.shape[1] - self.borderList[z].grid.shape[1])
                #penalita colore bordi
                pxmask = [1 for _ in range(0, len(self.borderList[z].border))]
                pymask = [1 for _ in range(0, len(output.borderList[z].border))]
                colorPenality = 0
                cx = 0
                for px in self.borderList[z].border:
                    cy = 0
                    for py in output.borderList[z].border:
                        if (px.x - self.borderList[z].x) == (py.x - output.borderList[z].x) and (px.y - self.borderList[z].y) == (py.y - output.borderList[z].y) and pymask[cy] == 1:
                            colorPenality += abs(int(px.color) - int(py.color))/10
                            pxmask[cx] = 0
                            pymask[cy] = 0
                            break
                        cy += 1
                    cx += 1
                score += colorPenality + sum(pxmask) + sum(pymask)
                #penalita colore centro
                pxmask = [1 for _ in range(0, len(self.borderList[z].center))]
                pymask = [1 for _ in range(0, len(output.borderList[z].center))]
                colorPenality = 0
                cx = 0
                for px in self.borderList[z].center:
                    cy = 0
                    for py in output.borderList[z].center:
                        if (px.x - self.borderList[z].x) == (py.x - output.borderList[z].x) and (px.y - self.borderList[z].y) == (py.y - output.borderList[z].y) and pymask[cy] == 1:
                            colorPenality += abs(int(px.color) - int(py.color))/10
                            pxmask[cx] = 0
                            pymask[cy] = 0
                            break
                        cy += 1
                    cx += 1
                score += colorPenality + sum(pxmask) + sum(pymask)
            else:
                score += len(self.borderList[z].border)
                score += len(self.borderList[z].center)
        if len(output.borderList) - len(self.borderList) > 0:
            for z in range(len(self.borderList), len(output.borderList)):
                score += len(self.borderList[z].border)
                score += len(self.borderList[z].center)
        return -score

    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for fb in self.borderList:
            for b in fb.border:
                grid[b.x][b.y] = b.color
            for c in fb.center:
                grid[c.x][c.y] = c.color
        return grid