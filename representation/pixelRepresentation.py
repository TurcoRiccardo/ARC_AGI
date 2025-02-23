import numpy as np
from dataclasses import dataclass
from selection.selector import Selector


@dataclass
class PixelNode:
    x: int
    y: int
    color: int = 0

class pixelRepresentation:
    def __init__(self, input_grid):
        self.nr = input_grid.shape[0]
        self.nc = input_grid.shape[1]
        self.pixelList = list()
        for x in range(self.nr):
            for y in range(self.nc):
                if input_grid[x][y] != 0:
                    self.pixelList.append(PixelNode(x, y, input_grid[x][y]))

    def getNElement(self):
        return len(self.pixelList)

    def movePixel(self, s):
        if len(self.pixelList) == 0:
            return
        adapted_index = s.index % len(self.pixelList)
        if (s.direction % 4) == 0:
            if self.pixelList[adapted_index].x + 1 < self.nr:
                #down
                ok = 0
                for pixel in self.pixelList:
                    if self.pixelList[adapted_index].x + 1 == pixel.x and self.pixelList[adapted_index].y == pixel.y:
                        ok = 1
                        break
                if ok == 0:
                    self.pixelList[adapted_index].x += 1
        elif (s.direction % 4) == 1:
            if self.pixelList[adapted_index].x > 0:
                #up
                ok = 0
                for pixel in self.pixelList:
                    if self.pixelList[adapted_index].x - 1 == pixel.x and self.pixelList[adapted_index].y == pixel.y:
                        ok = 1
                        break
                if ok == 0:
                    self.pixelList[adapted_index].x -= 1
        elif (s.direction % 4) == 2:
            if self.pixelList[adapted_index].y + 1 < self.nc:
                #right
                ok = 0
                for pixel in self.pixelList:
                    if self.pixelList[adapted_index].x == pixel.x and self.pixelList[adapted_index].y + 1 == pixel.y:
                        ok = 1
                        break
                if ok == 0:
                    self.pixelList[adapted_index].y += 1
        elif (s.direction % 4) == 3:
            if self.pixelList[adapted_index].y > 0:
                #left
                ok = 0
                for pixel in self.pixelList:
                    if self.pixelList[adapted_index].x == pixel.x and self.pixelList[adapted_index].y - 1 == pixel.y:
                        ok = 1
                        break
                if ok == 0:
                    self.pixelList[adapted_index].y -= 1

    def expandGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            self.nr += 1
        elif (s.direction % 4) == 1:
            #up
            self.nr += 1
            for pixel in self.pixelList:
                pixel.x += 1
        elif (s.direction % 4) == 2:
            #right
            self.nc += 1
        elif (s.direction % 4) == 3:
            #left
            self.nc += 1
            for pixel in self.pixelList:
                pixel.y += 1

    def reduceGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            self.nr -= 1
            remove = list()
            for x in range(0, len(self.pixelList)):
                if self.pixelList[x].x == self.nr:
                    remove.append(x)
            remove.sort(reverse = True)
            for x in remove:
                self.pixelList.pop(x)
        elif (s.direction % 4) == 1:
            #up
            self.nr -= 1
            remove = list()
            for x in range(0, len(self.pixelList)):
                if self.pixelList[x].x == 0:
                    remove.append(x)
                else:
                    self.pixelList[x].x -= 1
            remove.sort(reverse = True)
            for x in remove:
                self.pixelList.pop(x)
        elif (s.direction % 4) == 2:
            #right
            self.nc -= 1
            remove = list()
            for x in range(0, len(self.pixelList)):
                if self.pixelList[x].y == self.nc:
                    remove.append(x)
            remove.sort(reverse = True)
            for x in remove:
                self.pixelList.pop(x)
        elif (s.direction % 4) == 3:
            #left
            self.nc -= 1
            remove = list()
            for x in range(0, len(self.pixelList)):
                if self.pixelList[x].y == 0:
                    remove.append(x)
                else:
                    self.pixelList[x].y -= 1
            remove.sort(reverse = True)
            for x in remove:
                self.pixelList.pop(x)

    def changeColorPixel(self, s):
        if len(self.pixelList) == 0:
            return
        adapted_index = s.index % len(self.pixelList)
        if s.color % 2 == 0:
            if self.pixelList[adapted_index].color == 9:
                self.pixelList[adapted_index].color = 1
            else:
                self.pixelList[adapted_index].color += 1
        else:
            if self.pixelList[adapted_index].color == 1:
                self.pixelList[adapted_index].color = 9
            else:
                self.pixelList[adapted_index].color -= 1

    def RemovePixel(self, s):
        if len(self.pixelList) == 0:
            return
        adapted_index = s.index % len(self.pixelList)
        self.pixelList.pop(adapted_index)

    def DuplicateNearPixel(self, s):
        if len(self.pixelList) == 0:
            return
        adapted_index = s.index % len(self.pixelList)
        new_pixel = PixelNode(self.pixelList[adapted_index].x, self.pixelList[adapted_index].y, self.pixelList[adapted_index].color)
        if (s.direction % 4) == 0:
            #down
            if new_pixel.x + 1 < self.nr:
                ok = 0
                for pixel in self.pixelList:
                    if new_pixel.x + 1 == pixel.x and new_pixel.y == pixel.y:
                        ok = 1
                        break
                if ok == 0:
                    new_pixel.x += 1
        elif (s.direction % 4) == 1:
            #up
            if new_pixel.x > 0:
                ok = 0
                for pixel in self.pixelList:
                    if new_pixel.x - 1 == pixel.x and new_pixel.y == pixel.y:
                        ok = 1
                        break
                if ok == 0:
                    new_pixel.x -= 1
        elif (s.direction % 4) == 2:
            #right
            if new_pixel.y + 1 < self.nc:
                ok = 0
                for pixel in self.pixelList:
                    if new_pixel.x == pixel.x and new_pixel.y + 1 == pixel.y:
                        ok = 1
                        break
                if ok == 0:
                    new_pixel.y += 1
        elif (s.direction % 4) == 3:
            #left
            if new_pixel.y > 0:
                ok = 0
                for pixel in self.pixelList:
                    if new_pixel.x == pixel.x and new_pixel.y - 1 == pixel.y:
                        ok = 1
                        break
                if ok == 0:
                    new_pixel.y -= 1
        self.pixelList.append(new_pixel)

    def score(self, output):
        #-1 punti per posizione non giusta, proporzionale distanza per colore sbagliato, -2 punti dimensione griglia sbagliata per casella
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        mask = [1 for _ in range(0, len(output.pixelList))]
        ok = 0
        for px in self.pixelList:
            ok = 0
            c = 0
            for py in output.pixelList:
                if px.x == py.x and px.y == py.y and mask[c] == 1:
                    score += abs(int(px.color) - int(py.color))/10
                    mask[c] = 0
                    ok = 1
                    break
                c += 1
            if ok != 1:
                score += 1
        score += sum(mask)
        return -score

    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for pixel in self.pixelList:
            grid[pixel.x][pixel.y] = pixel.color
        return grid