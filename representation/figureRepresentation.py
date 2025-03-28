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
                    fig = Figure([], input_grid[x][y])
                    ricFindFigure(input_grid, x, y, fig, mask, self.nc, self.nr)
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
    
    #moves the figure index based on the direction
    def moveFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if (s.direction % 4) == 0:
                #down
                ok = 1
                for p in self.figureList[adapted_index].l:
                    if p.x + 1 >= self.nr:
                        ok = 0
                if ok == 1:
                    for p in self.figureList[adapted_index].l:
                        p.x += 1
                    count += 1
            elif (s.direction % 4) == 1:
                #up
                ok = 1
                for p in self.figureList[adapted_index].l:
                    if p.x <= 0:
                        ok = 0
                if ok == 1:
                    for p in self.figureList[adapted_index].l:
                        p.x -= 1
                    count += 1
            elif (s.direction % 4) == 2:
                #right
                ok = 1
                for p in self.figureList[adapted_index].l:
                    if p.y + 1 >= self.nc:
                        ok = 0
                if ok == 1:
                    for p in self.figureList[adapted_index].l:
                        p.y += 1
                    count += 1
            elif (s.direction % 4) == 3:
                #left
                ok = 1
                for p in self.figureList[adapted_index].l:
                    if p.y <= 0:
                        ok = 0
                if ok == 1:
                    for p in self.figureList[adapted_index].l:
                        p.y -= 1
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
                val = self.figureList[adapted_index].l[0].x
                newPixel = list()
                for p in self.figureList[adapted_index].l:
                    if val < p.x:
                        val = p.x
                for p in self.figureList[adapted_index].l:
                    if p.x + 1 < self.nr and p.x == val:
                        newPixel.append(PixelNode(p.x + 1, p.y, self.figureList[adapted_index].color))
                if len(newPixel) > 0:
                    self.figureList[adapted_index].l.extend(newPixel)
                    count += 1
            elif (s.direction % 4) == 1:
                #up
                val = self.figureList[adapted_index].l[0].x
                newPixel = list()
                for p in self.figureList[adapted_index].l:
                    if val > p.x:
                        val = p.x
                for p in self.figureList[adapted_index].l:
                    if p.x > 0 and p.x == val:
                        newPixel.append(PixelNode(p.x - 1, p.y, self.figureList[adapted_index].color))
                if len(newPixel) > 0:
                    self.figureList[adapted_index].l.extend(newPixel)
                    count += 1
            elif (s.direction % 4) == 2:
                #right
                val = self.figureList[adapted_index].l[0].y
                newPixel = list()
                for p in self.figureList[adapted_index].l:
                    if val < p.y:
                        val = p.y
                for p in self.figureList[adapted_index].l:
                    if p.y + 1 < self.nc and p.y == val:
                        newPixel.append(PixelNode(p.x, p.y + 1, self.figureList[adapted_index].color))
                if len(newPixel) > 0:
                    self.figureList[adapted_index].l.extend(newPixel)
                    count += 1
            elif (s.direction % 4) == 3:
                #left
                val = self.figureList[adapted_index].l[0].y
                newPixel = list()
                for p in self.figureList[adapted_index].l:
                    if val > p.y:
                        val = p.y
                for p in self.figureList[adapted_index].l:
                    if p.y > 0 and p.y == val:
                        newPixel.append(PixelNode(p.x, p.y - 1, self.figureList[adapted_index].color))
                if len(newPixel) > 0:
                    self.figureList[adapted_index].l.extend(newPixel)
                    count += 1
        if count != 0:
            return 0
        return 1

    #remove a element in the figure
    def removeElementFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        l.sort(key=lambda i: i, reverse=True)
        for adapted_index in l:
            if len(self.figureList[adapted_index].l) > 1:
                adapted_component = s.component % len(self.figureList[adapted_index].l)
                self.figureList[adapted_index].l.pop(adapted_component)
                count += 1
            else:
                self.figureList.pop(adapted_index)
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
                self.nr -= 1
                removeFig = list()
                for f in range(0, len(self.figureList)):
                    remove = list()
                    for p in range(0, len(self.figureList[f].l)):
                        if self.figureList[f].l[p].x == self.nr:
                            remove.append(p)
                    for x in sorted(remove, reverse=True):
                        self.figureList[f].l.pop(x)
                    if len(self.figureList[f].l) == 0:
                        removeFig.append(f)
                for x in sorted(removeFig, reverse=True):
                    self.figureList.pop(x)
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr > 1:
                self.nr -= 1
                removeFig = list()
                for f in range(0, len(self.figureList)):
                    remove = list()
                    for p in range(0, len(self.figureList[f].l)):
                        if self.figureList[f].l[p].x == 0:
                            remove.append(p)
                        else:
                            self.figureList[f].l[p].x -= 1
                    for x in sorted(remove, reverse=True):
                        self.figureList[f].l.pop(x)
                    if len(self.figureList[f].l) == 0:
                        removeFig.append(f)
                for x in sorted(removeFig, reverse=True):
                    self.figureList.pop(x)
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc > 1:
                self.nc -= 1
                removeFig = list()
                for f in range(0, len(self.figureList)):
                    remove = list()
                    for p in range(0, len(self.figureList[f].l)):
                        if self.figureList[f].l[p].y == self.nc:
                            remove.append(p)
                    for x in sorted(remove, reverse=True):
                        self.figureList[f].l.pop(x)
                    if len(self.figureList[f].l) == 0:
                        removeFig.append(f)
                for x in sorted(removeFig, reverse=True):
                    self.figureList.pop(x)
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc > 1:
                self.nc -= 1
                removeFig = list()
                for f in range(0, len(self.figureList)):
                    remove = list()
                    for p in range(0, len(self.figureList[f].l)):
                        if self.figureList[f].l[p].y == 0:
                            remove.append(p)
                        else:
                            self.figureList[f].l[p].y -= 1
                    for x in sorted(remove, reverse=True):
                        self.figureList[f].l.pop(x)
                    if len(self.figureList[f].l) == 0:
                        removeFig.append(f)
                for x in sorted(removeFig, reverse=True):
                    self.figureList.pop(x)
                return 0
        return 1

    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        for z in range(0, len(self.figureList)):
            if z < len(output.figureList):
                #normalizza le coordinate rispetto al punto in alto a sinistra (anche esterno dalla figura)
                pxminx = 100
                pxminy = 100
                for p in self.figureList[z].l:
                    if pxminx > p.x:
                        pxminx = p.x
                    if pxminy > p.y:
                        pxminy = p.y
                pyminx = 100
                pyminy = 100
                for p in output.figureList[z].l:
                    if pyminx > p.x:
                        pyminx = p.x
                    if pyminy > p.y:
                        pyminy = p.y
                #Verifica se due figure hanno la stessa forma
                pxmask = [1 for _ in range(0, len(self.figureList[z].l))]
                pymask = [1 for _ in range(0, len(output.figureList[z].l))]
                colorPenality = 0
                cx = 0
                for px in self.figureList[z].l:
                    cy = 0
                    for py in output.figureList[z].l:
                        if (px.x - pxminx) == (py.x - pyminx) and (px.y - pxminy) == (py.y - pyminy) and pymask[cy] == 1:
                            colorPenality += abs(int(px.color) - int(py.color))/10
                            pxmask[cx] = 0
                            pymask[cy] = 0
                            break
                        cy += 1
                    cx += 1
                #aggiorno lo score per la figura z: colore, distanza, pixel non coperti
                score += colorPenality + abs(int(pxminx) - int(pyminx))/10 + abs(int(pxminy) - int(pyminy))/10 + sum(pxmask) + sum(pymask)
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
            if performed_actions[x] == figureRepresentation.addElementFigure or performed_actions[x] == figureRepresentation.removeElementFigure or performed_actions[x] == figureRepresentation.changeOrder:
                score += 0.5
            score += 1
        return -score