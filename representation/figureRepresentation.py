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
    l: list[PixelNode]
    xMax: int
    xMin: int
    yMax: int
    yMin: int
    color: int

def ricFindFigure(grid, posX, posY, fig, mask, nc, nr):
    if mask[posX][posY] == 1 and grid[posX][posY] == fig.color:
        mask[posX][posY] = 0
        fig.l.append(PixelNode(posX, posY, fig.color))
    if posX+1 < nr:
        #down
        if grid[posX+1][posY] == fig.color and mask[posX+1][posY] == 1:
            ricFindFigure(grid, posX+1, posY, fig, mask, nc, nr)
    if posX > 0:
        #up
        if grid[posX-1][posY] == fig.color and mask[posX-1][posY] == 1:
            ricFindFigure(grid, posX-1, posY, fig, mask, nc, nr)
    if posY+1 < nc:
        #right
        if grid[posX][posY+1] == fig.color and mask[posX][posY+1] == 1:
            ricFindFigure(grid, posX, posY+1, fig, mask, nc, nr)
    if posY > 0:
        #left
        if grid[posX][posY-1] == fig.color and mask[posX][posY-1] == 1:
            ricFindFigure(grid, posX, posY-1, fig, mask, nc, nr)
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
                    fig = Figure([], 0, 1000, 0, 1000, input_grid[x][y])
                    ricFindFigure(input_grid, x, y, fig, mask, self.nc, self.nr)
                    for p in fig.l:
                        if fig.xMax < p.x:
                            fig.xMax = p.x
                        if fig.xMin > p.x:
                            fig.xMin = p.x
                        if fig.yMax < p.y:
                            fig.yMax = p.y
                        if fig.yMin > p.y:
                            fig.yMin = p.y
                    self.figureList.append(fig)

    #return the total number of figure
    def getNElement(self):
        return len(self.figureList)
    
    #return the total number of element in the figure index
    def getElementComponent(self, index):
        return len(self.figureList[index].l)
    
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
                if self.figureList[x].l[0].color == s.color:
                    l.append(x)
        else:
            #sopra
            l.append(s.index % len(self.figureList))
        return l
    
    #return the list of component index
    def generateComponentList(self, s, adapted_index):
        l = list()
        if s.allComponent == 1:
            #da destra
            l.append(len(self.figureList[adapted_index].l) - (s.component % len(self.figureList[adapted_index].l)) - 1)
        elif s.allComponent == 2:
            #centro
            if len(self.figureList[adapted_index].l) % 2 == 1:
                l.append(len(self.figureList[adapted_index].l) // 2)
            else:
                l.append(len(self.figureList[adapted_index].l) // 2 - 1)
                l.append(len(self.figureList[adapted_index].l) // 2)
        elif s.allComponent >= 3:
            #all color
            l = [x for x in range(0, len(self.figureList[adapted_index].l))]
        else:
            #da sinistra
            l.append(s.component % len(self.figureList[adapted_index].l))
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
                if self.figureList[adapted_index].xMax + 1 < self.nr:
                    for p in self.figureList[adapted_index].l:
                        p.x += 1
                    self.figureList[adapted_index].xMax += 1
                    self.figureList[adapted_index].xMin += 1
                    count += 1
            elif (s.direction % 4) == 1:
                #up
                if self.figureList[adapted_index].xMin > 0:
                    for p in self.figureList[adapted_index].l:
                        p.x -= 1
                    self.figureList[adapted_index].xMax -= 1
                    self.figureList[adapted_index].xMin -= 1
                    count += 1
            elif (s.direction % 4) == 2:
                #right
                if self.figureList[adapted_index].yMax + 1 < self.nc:
                    for p in self.figureList[adapted_index].l:
                        p.y += 1
                    self.figureList[adapted_index].yMax += 1
                    self.figureList[adapted_index].yMin += 1
                    count += 1
            elif (s.direction % 4) == 3:
                #left
                if self.figureList[adapted_index].yMin > 0:
                    for p in self.figureList[adapted_index].l:
                        p.y -= 1
                    self.figureList[adapted_index].yMax -= 1
                    self.figureList[adapted_index].yMin -= 1
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
                    for p in self.figureList[adapted_index].l:
                        p.color += 1
                    self.figureList[adapted_index].color += 1
                count += 1
            else:
                if self.figureList[adapted_index].color != 1:
                    for p in self.figureList[adapted_index].l:
                        p.color -= 1
                    self.figureList[adapted_index].color -= 1
                count += 1
        if count != 0:
            return 0
        return 1

    #add a element in the figure
    def addElementFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if (s.direction % 4) == 0:
                #down
                if self.figureList[adapted_index].xMax + 1 < self.nr:
                    newPixel = list()
                    for p in self.figureList[adapted_index].l:
                        if p.x == self.figureList[adapted_index].xMax:
                            newPixel.append(PixelNode(p.x + 1, p.y, self.figureList[adapted_index].color))
                    if len(newPixel) > 0:
                        self.figureList[adapted_index].l.extend(newPixel)
                        self.figureList[adapted_index].xMax += 1
                        count += 1
            elif (s.direction % 4) == 1:
                #up
                if self.figureList[adapted_index].xMin > 0:
                    newPixel = list()
                    for p in self.figureList[adapted_index].l:
                        if p.x == self.figureList[adapted_index].xMin:
                            newPixel.append(PixelNode(p.x - 1, p.y, self.figureList[adapted_index].color))
                    if len(newPixel) > 0:
                        self.figureList[adapted_index].l.extend(newPixel)
                        self.figureList[adapted_index].xMin -= 1
                        count += 1
            elif (s.direction % 4) == 2:
                #right
                if self.figureList[adapted_index].yMax + 1 < self.nc:
                    newPixel = list()
                    for p in self.figureList[adapted_index].l:
                        if p.y == self.figureList[adapted_index].yMax:
                            newPixel.append(PixelNode(p.x, p.y + 1, self.figureList[adapted_index].color))
                    if len(newPixel) > 0:
                        self.figureList[adapted_index].l.extend(newPixel)
                        self.figureList[adapted_index].yMax += 1
                        count += 1
            elif (s.direction % 4) == 3:
                #left
                if self.figureList[adapted_index].yMin > 0:
                    newPixel = list()
                    for p in self.figureList[adapted_index].l:
                        if p.y == self.figureList[adapted_index].yMin:
                            newPixel.append(PixelNode(p.x, p.y - 1, self.figureList[adapted_index].color))
                    if len(newPixel) > 0:
                        self.figureList[adapted_index].l.extend(newPixel)
                        self.figureList[adapted_index].yMin -= 1
                        count += 1
        if count != 0:
            return 0
        return 1

    #remove a element in the figure
    def removeElementFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        li = self.generateIndexList(s)
        li.sort(key=lambda i: i, reverse=True)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            lc.sort(key=lambda i: i, reverse=True)
            for adapted_component in lc:
                if len(self.figureList[adapted_index].l) > 1:
                    self.figureList[adapted_index].l.pop(adapted_component)
                    for p in self.figureList[adapted_index].l:
                        if self.figureList[adapted_index].xMax < p.x:
                            self.figureList[adapted_index].xMax = p.x
                        if self.figureList[adapted_index].xMin > p.x:
                            self.figureList[adapted_index].xMin = p.x
                        if self.figureList[adapted_index].yMax < p.y:
                            self.figureList[adapted_index].yMax = p.y
                        if self.figureList[adapted_index].yMin > p.y:
                            self.figureList[adapted_index].yMin = p.y
                    count += 1
                else:
                    self.figureList.pop(adapted_index)
                    count += 1
        if count != 0:
            return 0
        return 1

    #duplicate the selected figure based on the direction direction
    def duplicateFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if (s.direction % 4) == 0:
                #down
                height = (self.figureList[adapted_index].xMax - self.figureList[adapted_index].xMin + 1)
                if self.figureList[adapted_index].xMax + height < self.nr:
                    newPixel = list()
                    for p in self.figureList[adapted_index].l:
                        newPixel.append(PixelNode(p.x + height, p.y, self.figureList[adapted_index].color))
                    self.figureList.append(Figure(newPixel, self.figureList[adapted_index].xMax + height, self.figureList[adapted_index].xMin + height, self.figureList[adapted_index].yMax, self.figureList[adapted_index].yMin, self.figureList[adapted_index].color))
                    count += 1
            elif (s.direction % 4) == 1:
                #up
                height = (self.figureList[adapted_index].xMax - self.figureList[adapted_index].xMin + 1)
                if self.figureList[adapted_index].xMin - height >= 0:
                    newPixel = list()
                    for p in self.figureList[adapted_index].l:
                        newPixel.append(PixelNode(p.x - height, p.y, self.figureList[adapted_index].color))
                    self.figureList.append(Figure(newPixel, self.figureList[adapted_index].xMax - height, self.figureList[adapted_index].xMin - height, self.figureList[adapted_index].yMax, self.figureList[adapted_index].yMin, self.figureList[adapted_index].color))
                    count += 1
            elif (s.direction % 4) == 2:
                #right
                width = (self.figureList[adapted_index].yMax - self.figureList[adapted_index].yMin + 1)
                if self.figureList[adapted_index].yMax + width < self.nc:
                    newPixel = list()
                    for p in self.figureList[adapted_index].l:
                        newPixel.append(PixelNode(p.x, p.y + width, self.figureList[adapted_index].color))
                    self.figureList.append(Figure(newPixel, self.figureList[adapted_index].xMax, self.figureList[adapted_index].xMin, self.figureList[adapted_index].yMax + width, self.figureList[adapted_index].yMin + width, self.figureList[adapted_index].color))
                    count += 1
            elif (s.direction % 4) == 3:
                #left
                width = (self.figureList[adapted_index].yMax - self.figureList[adapted_index].yMin + 1)
                if self.figureList[adapted_index].yMin - width >= 0:
                    newPixel = list()
                    for p in self.figureList[adapted_index].l:
                        newPixel.append(PixelNode(p.x, p.y - height, self.figureList[adapted_index].color))
                    self.figureList.append(Figure(newPixel, self.figureList[adapted_index].xMax, self.figureList[adapted_index].xMin, self.figureList[adapted_index].yMax - width, self.figureList[adapted_index].yMin - width, self.figureList[adapted_index].color))
                    count += 1
        if count != 0:
            return 0
        return 1

    #merge 2 figure based on the direction direction
    def mergeFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if adapted_index < len(self.figureList):
                if (s.direction % 4) == 0:
                    #down
                    indexFigure = set()
                    for p1 in self.figureList[adapted_index].l:
                        if p1.x + 1 < self.nr:
                            for f2 in range(0, len(self.figureList)):
                                if f2 != adapted_index:
                                    for p2 in self.figureList[f2].l:
                                        if p1.x+1 == p2.x and p1.y == p2.y and p1.color == p2.color:
                                            indexFigure.add(f2)
                    if len(indexFigure) > 0:
                        existing_pixels = {(p.x, p.y) for p in self.figureList[adapted_index].l}
                        newPixel = list()
                        for f in sorted(indexFigure, reverse=True):
                            figureToMerge = self.figureList[f]
                            for p2 in figureToMerge.l:
                                if (p2.x, p2.y) not in existing_pixels:
                                    newPixel.append(p2)
                                    existing_pixels.add((p2.x, p2.y))
                        self.figureList[adapted_index].l.extend(newPixel)
                        for f in sorted(indexFigure, reverse=True):
                            self.figureList.pop(f)
                        count += 1
                elif (s.direction % 4) == 1:
                    #up
                    indexFigure = set()
                    for p1 in self.figureList[adapted_index].l:
                        if p1.x > 0:
                            for f2 in range(0, len(self.figureList)):
                                if f2 != adapted_index:
                                    for p2 in self.figureList[f2].l:
                                        if p1.x-1 == p2.x and p1.y == p2.y and p1.color == p2.color:
                                            indexFigure.add(f2)
                    if len(indexFigure) > 0:
                        existing_pixels = {(p.x, p.y) for p in self.figureList[adapted_index].l}
                        newPixel = list()
                        for f in sorted(indexFigure, reverse=True):
                            figureToMerge = self.figureList[f]
                            for p2 in figureToMerge.l:
                                if (p2.x, p2.y) not in existing_pixels:
                                    newPixel.append(p2)
                                    existing_pixels.add((p2.x, p2.y))
                        self.figureList[adapted_index].l.extend(newPixel)
                        for f in sorted(indexFigure, reverse=True):
                            self.figureList.pop(f)
                        count += 1
                elif (s.direction % 4) == 2:
                    #right
                    indexFigure = set()
                    for p1 in self.figureList[adapted_index].l:
                        if p1.y + 1 < self.nc:
                            for f2 in range(0, len(self.figureList)):
                                if f2 != adapted_index:
                                    for p2 in self.figureList[f2].l:
                                        if p1.x == p2.x and p1.y+1 == p2.y and p1.color == p2.color:
                                            indexFigure.add(f2)
                    if len(indexFigure) > 0:
                        existing_pixels = {(p.x, p.y) for p in self.figureList[adapted_index].l}
                        newPixel = list()
                        for f in sorted(indexFigure, reverse=True):
                            figureToMerge = self.figureList[f]
                            for p2 in figureToMerge.l:
                                if (p2.x, p2.y) not in existing_pixels:
                                    newPixel.append(p2)
                                    existing_pixels.add((p2.x, p2.y))
                        self.figureList[adapted_index].l.extend(newPixel)
                        for f in sorted(indexFigure, reverse=True):
                            self.figureList.pop(f)
                        count += 1
                elif (s.direction % 4) == 3:
                    #left
                    indexFigure = set()
                    for p1 in self.figureList[adapted_index].l:
                        if p1.y > 0:
                            for f2 in range(0, len(self.figureList)):
                                if f2 != adapted_index:
                                    for p2 in self.figureList[f2].l:
                                        if p1.x == p2.x and p1.y-1 == p2.y and p1.color == p2.color:
                                            indexFigure.add(f2)
                    if len(indexFigure) > 0:
                        existing_pixels = {(p.x, p.y) for p in self.figureList[adapted_index].l}
                        newPixel = list()
                        for f in sorted(indexFigure, reverse=True):
                            figureToMerge = self.figureList[f]
                            for p2 in figureToMerge.l:
                                if (p2.x, p2.y) not in existing_pixels:
                                    newPixel.append(p2)
                                    existing_pixels.add((p2.x, p2.y))
                        self.figureList[adapted_index].l.extend(newPixel)
                        for f in sorted(indexFigure, reverse=True):
                            self.figureList.pop(f)
                        count += 1
        if count != 0:
            return 0
        return 1

    #divide a figure 
    def divideFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            fig = Figure([], self.figureList[adapted_index].color)
            if (s.direction % 4) == 0:
                #down
                val = self.figureList[adapted_index].l[0].x
                ok = 0
                for p in self.figureList[adapted_index].l:
                    if val < p.x:
                        val = p.x
                    if p.x != val:
                        ok = 1
                if ok != 0:
                    remPixel = list()
                    for p in range(0, len(self.figureList[adapted_index].l)):
                        if val == self.figureList[adapted_index].l[p].x:
                            remPixel.append(p)
                            fig.l.append(self.figureList[adapted_index].l[p])
                    if len(remPixel) > 0:
                        for ind in sorted(remPixel, reverse=True):
                            self.figureList[adapted_index].l.pop(ind)
                        self.figureList.append(fig)
                        count += 1
            elif (s.direction % 4) == 1:
                #up
                val = self.figureList[adapted_index].l[0].x
                ok = 0
                for p in self.figureList[adapted_index].l:
                    if val > p.x:
                        val = p.x
                        if p.x != val:
                            ok = 1
                if ok != 0:
                    remPixel = list()
                    for p in range(0, len(self.figureList[adapted_index].l)):
                        if val == self.figureList[adapted_index].l[p].x:
                            remPixel.append(p)
                            fig.l.append(self.figureList[adapted_index].l[p])
                    if len(remPixel) > 0:
                        for ind in sorted(remPixel, reverse=True):
                            self.figureList[adapted_index].l.pop(ind)
                        self.figureList.append(fig)
                        count += 1
            elif (s.direction % 4) == 2:
                #right
                val = self.figureList[adapted_index].l[0].y
                ok = 0
                for p in self.figureList[adapted_index].l:
                    if val < p.y:
                        val = p.y
                        if p.y != val:
                            ok = 1
                if ok != 0:
                    remPixel = list()
                    for p in range(0, len(self.figureList[adapted_index].l)):
                        if val == self.figureList[adapted_index].l[p].y:
                            remPixel.append(p)
                            fig.l.append(self.figureList[adapted_index].l[p])
                    if len(remPixel) > 0:
                        for ind in sorted(remPixel, reverse=True):
                            self.figureList[adapted_index].l.pop(ind)
                        self.figureList.append(fig)
                        count += 1
            elif (s.direction % 4) == 3:
                #left
                val = self.figureList[adapted_index].l[0].y
                ok = 0
                for p in self.figureList[adapted_index].l:
                    if val > p.y:
                        val = p.y
                        if p.y != val:
                            ok = 1
                if ok != 0:
                    remPixel = list()
                    for p in range(0, len(self.figureList[adapted_index].l)):
                        if val == self.figureList[adapted_index].l[p].y:
                            remPixel.append(p)
                            fig.l.append(self.figureList[adapted_index].l[p])
                    if len(remPixel) > 0:
                        for ind in sorted(remPixel, reverse=True):
                            self.figureList[adapted_index].l.pop(ind)
                        self.figureList.append(fig)
                        count += 1
        if count != 0:
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
                    for p in f.l:
                        p.x += 1
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
                    for p in f.l:
                        p.y += 1
                return 0
        return 1

    #reduce the grid in the direction direction
    def reduceGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            if self.nr > 1:
                ok = 0
                for fig in self.figureList:
                    if fig.xMax >= self.nr - 1:
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
                    if fig.xMin == 0:
                        ok = 1
                        break
                if ok == 0:
                    self.nr -= 1
                    for fig in self.figureList:
                        fig.xMax -= 1
                        fig.xMin -= 1
                        for p in fig.l:
                            p.x -= 1
                    return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc > 1:
                ok = 0
                for fig in self.figureList:
                    if fig.yMax >= self.nc - 1:
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
                    if fig.yMin == 0:
                        ok = 1
                        break
                if ok == 0:
                    self.nc -= 1
                    for fig in self.figureList:
                        fig.yMax -= 1
                        fig.yMin -= 1
                        for p in fig.l:
                            p.y -= 1
                    return 0
        return 1

    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        for z in range(0, len(self.figureList)):
            if z < len(output.figureList):
                #Verifica se due figure hanno la stessa forma normalizzando le coordinate rispetto al punto in alto a sinistra (anche esterno dalla figura)
                pxmask = [1 for _ in range(0, len(self.figureList[z].l))]
                pymask = [1 for _ in range(0, len(output.figureList[z].l))]
                colorPenality = 0
                cx = 0
                for px in self.figureList[z].l:
                    cy = 0
                    for py in output.figureList[z].l:
                        if (px.x - self.figureList[z].xMin) == (py.x - output.figureList[z].xMin) and (px.y - self.figureList[z].yMin) == (py.y - output.figureList[z].yMin) and pymask[cy] == 1:
                            colorPenality += abs(int(px.color) - int(py.color))/10
                            pxmask[cx] = 0
                            pymask[cy] = 0
                            break
                        cy += 1
                    cx += 1
                #aggiorno lo score per la figura z: colore, distanza, pixel non coperti
                score += colorPenality + abs(int(self.figureList[z].xMin) - int(output.figureList[z].xMin))/10 + abs(int(self.figureList[z].yMin) - int(output.figureList[z].yMin))/10 + sum(pxmask) + sum(pymask)
            else:
                score += len(self.figureList[z].l)
        if len(output.figureList) - len(self.figureList) > 0:
            for z in range(len(self.figureList), len(output.figureList)):
                score += len(output.figureList[z].l) * 1.2
        return -score

    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for f in self.figureList:
            for p in f.l:
                grid[p.x][p.y] = p.color
        return grid
    
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_selection[x].allElement < 3: 
                score += 0.5
            if performed_actions[x] == figureRepresentation.addElementFigure or performed_actions[x] == figureRepresentation.removeElementFigure or performed_actions[x] == figureRepresentation.mergeFigure or performed_actions[x] == figureRepresentation.divideFigure:
                score += 0.5
            score += 1
        return -score