import numpy as np
from dataclasses import dataclass
from selection.selector import Selector


@dataclass
class Rectangle:
    x: int
    y: int
    h: int
    w: int
    color: int = 0

class rectangleRepresentation:
    def __init__(self, input_grid):
        self.nr = input_grid.shape[0]
        self.nc = input_grid.shape[1]
        self.rectangleList = list()
        mask = [1 for _ in range(0, self.nc)]
        mask = [mask.copy() for _ in range(0, self.nr)]
        for x in range(self.nr):
            for y in range(self.nc):
                if input_grid[x][y] != 0 and mask[x][y] != 0:
                    newRectangle = Rectangle(x, y, 0, 0, input_grid[x][y])
                    while True:
                        newRectangle.w += 1
                        if y+newRectangle.w >= self.nc or input_grid[x][y+newRectangle.w] != newRectangle.color or mask[x][y+newRectangle.w] == 0:
                            break
                    while True:
                        newRectangle.h += 1
                        if x+newRectangle.h >= self.nr:
                            break
                        ok = 1
                        for c in range(y, y+newRectangle.w):
                            if input_grid[x+newRectangle.h][c] != newRectangle.color or mask[x][y] == 0:
                                ok = 0
                        if ok == 0:
                            break
                    #riempio la mask
                    for j in range(x, x + newRectangle.h):
                        for k in range(y, y + newRectangle.w):
                            mask[j][k] = 0
                    self.rectangleList.append(newRectangle)
    
    def getNElement(self):
        return len(self.rectangleList)
    
    def moveRectangle(self, s):
        if len(self.rectangleList) == 0:
            return 1
        adapted_index = s.index % len(self.rectangleList)
        if (s.direction % 4) == 0:
            #down
            if self.rectangleList[adapted_index].x + self.rectangleList[adapted_index].h < self.nr:
                self.rectangleList[adapted_index].x += 1
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.rectangleList[adapted_index].x > 0:
                self.rectangleList[adapted_index].x -= 1
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.rectangleList[adapted_index].y + self.rectangleList[adapted_index].w < self.nc:
                self.rectangleList[adapted_index].y += 1
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.rectangleList[adapted_index].y > 0:
                self.rectangleList[adapted_index].x -= 1
                return 0
        return 1
    
    def changeColorRectangle(self, s):
        if len(self.rectangleList) == 0:
            return
        adapted_index = s.index % len(self.rectangleList)
        if s.color % 2 == 0:
            if self.rectangleList[adapted_index].color != 9:
                self.rectangleList[adapted_index].color += 1
                return 0
        else:
            if self.rectangleList[adapted_index].color != 1:
                self.rectangleList[adapted_index].color -= 1
                return 0
        return 1

    def removeRectangle(self, s):
        if len(self.rectangleList) == 0:
            return 1
        adapted_index = s.index % len(self.rectangleList)
        self.rectangleList.pop(adapted_index)
        return 0

    def duplicateNearRectangle(self, s):
        if len(self.rectangleList) == 0:
            return 1
        adapted_index = s.index % len(self.rectangleList)
        new_rectangle = Rectangle(self.rectangleList[adapted_index].x, self.rectangleList[adapted_index].y, 1, 1, self.rectangleList[adapted_index].color)
        if (s.direction % 4) == 0:
            #down
            if new_rectangle.x + new_rectangle.h < self.nr:
                new_rectangle.x = new_rectangle.x + new_rectangle.h
                self.rectangleList.append(new_rectangle)
                return 0
        elif (s.direction % 4) == 1:
            #up
            if new_rectangle.x - 1 >= 0:
                new_rectangle.x = new_rectangle.x - 1
                self.rectangleList.append(new_rectangle)
                return 0
        elif (s.direction % 4) == 2:
            #right
            if new_rectangle.y + new_rectangle.w < self.nc:
                new_rectangle.y = new_rectangle.y + new_rectangle.w
                self.rectangleList.append(new_rectangle)
                return 0
        elif (s.direction % 4) == 3:
            #left
            if new_rectangle.y - 1 >= 0:
                new_rectangle.y = new_rectangle.y - 1
                self.rectangleList.append(new_rectangle)
                return 0
        return 1

    def changeOrder(self, s):
        if len(self.rectangleList) == 0:
            return 1
        adapted_index = s.index % len(self.rectangleList)
        if s.color % 2 == 0:
            if adapted_index + 1 < len(self.rectangleList):
                self.rectangleList[adapted_index], self.rectangleList[adapted_index + 1] = self.rectangleList[adapted_index + 1], self.rectangleList[adapted_index]
                return 0
        else:
            if adapted_index - 1 >= 0:
                self.rectangleList[adapted_index], self.rectangleList[adapted_index - 1] = self.rectangleList[adapted_index - 1], self.rectangleList[adapted_index]
                return 0
        return 1

    def scaleRectangle(self, s):
        if len(self.rectangleList) == 0:
            return 1
        adapted_index = s.index % len(self.rectangleList)
        if (s.direction % 4) == 0:
            #down
            if self.rectangleList[adapted_index].x + self.rectangleList[adapted_index].h < self.nr:
                self.rectangleList[adapted_index].h += 1
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.rectangleList[adapted_index].x > 0:
                self.rectangleList[adapted_index].h += 1
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.rectangleList[adapted_index].y + self.rectangleList[adapted_index].w < self.nc:
                self.rectangleList[adapted_index].w += 1
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.rectangleList[adapted_index].y > 0:
                self.rectangleList[adapted_index].w -= 1
                return 0
        return 1

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
                for rectangle in self.rectangleList:
                    rectangle.x += 1
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
                for rectangle in self.rectangleList:
                    rectangle.y += 1
                return 0
        return 1

    def reduceGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            if self.nr > 1:
                self.nr -= 1
                remove = list()
                for x in range(0, len(self.rectangleList)):
                    if self.rectangleList[x].x == self.nr:
                        remove.append(x)
                remove.sort(reverse = True)
                for x in remove:
                    self.rectangleList.pop(x)
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr > 1:
                self.nr -= 1
                remove = list()
                for x in range(0, len(self.rectangleList)):
                    if self.rectangleList[x].x == 0:
                        remove.append(x)
                    else:
                        self.rectangleList[x].x -= 1
                remove.sort(reverse = True)
                for x in remove:
                    self.rectangleList.pop(x)
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc > 1:
                self.nc -= 1
                remove = list()
                for x in range(0, len(self.rectangleList)):
                    if self.rectangleList[x].y == self.nc:
                        remove.append(x)
                remove.sort(reverse = True)
                for x in remove:
                    self.rectangleList.pop(x)
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc > 1:
                self.nc -= 1
                remove = list()
                for x in range(0, len(self.rectangleList)):
                    if self.rectangleList[x].y == 0:
                        remove.append(x)
                    else:
                        self.rectangleList[x].y -= 1
                remove.sort(reverse = True)
                for x in remove:
                    self.rectangleList.pop(x)
                return 0
        return 1
    
    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        for z in range(0, len(self.rectangleList)):
            if z < len(output.rectangleList):
                #distanza tra le x piu distanza tra le y
                score += abs(self.rectangleList[z].x - output.rectangleList[z].x) + abs(self.rectangleList[z].y - output.rectangleList[z].y)
                #distanza tra le h piu distanza tra le w
                score += abs(self.rectangleList[z].h - output.rectangleList[z].h) + abs(self.rectangleList[z].w - output.rectangleList[z].w)
                #distanza tra il colore
                score += abs(int(self.rectangleList[z].color) - int(output.rectangleList[z].color))
            else:
                score += self.rectangleList[z].h * self.rectangleList[z].w
        if len(output.rectangleList) - len(self.rectangleList) > 0:
            for z in range(len(self.rectangleList), len(output.rectangleList)):
                score += output.rectangleList[z].h * output.rectangleList[z].w
        return -score

    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for rectangle in self.rectangleList:
            for j in range(rectangle.x, rectangle.x + rectangle.h):
                for k in range(rectangle.y, rectangle.y + rectangle.w):
                    grid[j][k] = rectangle.color
        return grid


