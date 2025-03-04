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

class figureRepresentation:
    def __init__(self, input_grid):
        self.nr = input_grid.shape[0]
        self.nc = input_grid.shape[1]
        self.figureList = list()


        m = [1 for _ in range(0, self.nc)]
        mask = [m.copy() for _ in range(0, self.nr)]
        for x in range(0, self.nr):
            for y in range(0, self.nc):
                if input_grid[x][y] != 0 and mask[x][y] == 1:
                    fig = Figure([])
                    fig.l.append(PixelNode(x, y, input_grid[x][y]))
                    ok = 1
                    while ok == 1:
                        ok = 0
                        #serve ricorsione




                    mask[x][y] = 0
                    for j in range(x, self.nr):
                        for k in range(0, self.nc):
                            if input_grid[j][k] != 0 and mask[j][k] == 1:
                                for p in fig.l:
                                    if k > 0 and mask[j][k] == 1:
                                        #sinistra
                                        if j == p.x and k - 1 == p.y:
                                            mask[j][k] = 0
                                            fig.l.append(PixelNode(j, k, input_grid[j][k]))
                                    if k + 1 < self.nc and mask[j][k] == 1:
                                        #destra
                                        if j == p.x and k + 1 == p.y:
                                            mask[j][k] = 0
                                            fig.l.append(PixelNode(j, k, input_grid[j][k]))
                                    if j + 1 < self.nr and mask[j][k] == 1:
                                        #sotto
                                        if j + 1 == p.x and k == p.y:
                                            mask[j][k] = 0
                                            fig.l.append(PixelNode(j, k, input_grid[j][k]))
                                    if j > 0 and mask[j][k] == 1:
                                        #sopra
                                        if j - 1 == p.x and k == p.y:
                                            mask[j][k] = 0
                                            fig.l.append(PixelNode(j, k, input_grid[j][k]))
                    self.figureList.append(fig)

    #return the total number of figure
    def getNElement(self):
        return len(self.figureList)
    
    #return the total number of element in the figure index
    def getElementComponent(self, index):
        return len(self.figureList[index].l)
    
    #moves the figure index based on the direction
    def moveFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        adapted_index = s.index % len(self.figureList)
        if (s.direction % 4) == 0:
            #down
            ok = 1
            for p in self.figureList[adapted_index].l:
                if p.x + 1 >= self.nr:
                    ok = 0
            if ok == 1:
                for p in self.figureList[adapted_index].l:
                    p.x += 1
                return 0
        elif (s.direction % 4) == 1:
            #up
            ok = 1
            for p in self.figureList[adapted_index].l:
                if p.x <= 0:
                    ok = 0
            if ok == 1:
                for p in self.figureList[adapted_index].l:
                    p.x -= 1
                return 0
        elif (s.direction % 4) == 2:
            #right
            ok = 1
            for p in self.figureList[adapted_index].l:
                if p.y + 1 >= self.nc:
                    ok = 0
            if ok == 1:
                for p in self.figureList[adapted_index].l:
                    p.y += 1
                return 0
        elif (s.direction % 4) == 3:
            #left
            ok = 1
            for p in self.figureList[adapted_index].l:
                if p.y <= 0:
                    ok = 0
            if ok == 1:
                for p in self.figureList[adapted_index].l:
                    p.y -= 1
                return 0
        return 1

    #changes the color of the figure index based on color
    def changeColorFigure(self, s):
        if len(self.figureList) == 0:
            return 1
        adapted_index = s.index % len(self.figureList)
        if s.color % 2 == 0:
            for p in self.figureList[adapted_index].l:
                if p.color != 9:
                    p.color += 1
            return 0
        else:
            for p in self.figureList[adapted_index].l:
                if p.color != 1:
                    p.color -= 1
            return 0

    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        for z in range(0, len(self.figureList)):
            if z < len(output.figureList):
                mask = [1 for _ in range(0, len(output.figureList[z].l))]
                for px in self.figureList[z].l:
                    ok = 0
                    c = 0
                    for py in output.figureList[z].l:
                        if px.x == py.x and px.y == py.y and mask[c] == 1:
                            score += abs(int(px.color) - int(py.color))/10
                            mask[c] = 0
                            ok = 1
                            break
                        c += 1
                    if ok != 1:
                        score += 1
                score += sum(mask)
            else:
                score += len(self.figureList[z].l)
        if len(output.figureList) - len(self.figureList) > 0:
            for z in range(len(self.figureList), len(output.figureList)):
                score += len(output.figureList[z].l)
        return -score
    
    def scoresc(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        print("start")
        print(score)
        print(output.figureList)
        for z in range(0, len(self.figureList)):
            if z < len(output.figureList):
                mask = [1 for _ in range(0, len(output.figureList[z].l))]
                for px in self.figureList[z].l:
                    ok = 0
                    c = 0
                    for py in output.figureList[z].l:
                        if px.x == py.x and px.y == py.y and mask[c] == 1:
                            score += abs(int(px.color) - int(py.color))/10
                            mask[c] = 0
                            ok = 1
                            break
                        c += 1
                    if ok != 1:
                        score += 1
                score += sum(mask)
            else:
                score += len(self.figureList[z].l)
        print("prefin")
        print(len(output.figureList) - len(self.figureList))
        print(score)
        if len(output.figureList) - len(self.figureList) > 0:
            for z in range(len(self.figureList), len(output.figureList)):
                score += len(output.figureList[z].l)
        print("fin")
        return -score

    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for f in self.figureList:
            for p in f.l:
                grid[p.x][p.y] = p.color
        return grid