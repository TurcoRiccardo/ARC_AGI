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

    #return the total number of colored pixels
    def getNElement(self):
        return len(self.pixelList)
    
    #return the total number of pixel
    def getElementComponent(self, index):
        return self.nr * self.nc

    #moves the pixel index if possible based on the direction
    def movePixel(self, s):
        if len(self.pixelList) == 0:
            return 1
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
                    return 0
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
                    return 0
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
                    return 0
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
                    return 0
        return 1

    #moves the pixel of the same color index if possible based on the direction
    def moveColoredPixel(self, s):
        if len(self.pixelList) == 0:
            return 1
        adapted_index = s.index % len(self.pixelList)
        if (s.direction % 4) == 0:
            #down
            c = 0
            for pixel in self.pixelList.sort(key=lambda node: node.x, reverse=True):
                if pixel.color == s.color and pixel.x + 1 < self.nr:
                    ok = 0
                    for p in self.pixelList:
                        if pixel.x + 1 == p.x and pixel.y == p.y:
                            ok = 1
                        break
                    if ok == 0:
                        pixel.x += 1
                        c += 1
            if c > 0:
                return 0
        elif (s.direction % 4) == 1:
            #up
            c = 0
            for pixel in self.pixelList:
                if pixel.color == s.color and pixel.x > 0:
                    ok = 0
                    for p in self.pixelList:
                        if pixel.x - 1 == p.x and pixel.y == p.y:
                            ok = 1
                        break
                    if ok == 0:
                        pixel.x -= 1
                        c += 1
            if c > 0:
                return 0
        elif (s.direction % 4) == 2:
            #right
            c = 0
            for pixel in self.pixelList.sort(key=lambda node: node.y, reverse=True):
                if pixel.color == s.color and pixel.y + 1 < self.nc:
                    ok = 0
                    for p in self.pixelList:
                        if pixel.x == p.x and pixel.y + 1 == p.y:
                            ok = 1
                        break
                    if ok == 0:
                        pixel.y += 1
                        c += 1
            if c > 0:
                return 0
        elif (s.direction % 4) == 3:
            #left
            c = 0
            for pixel in self.pixelList:
                if pixel.color == s.color and pixel.y > 0:
                    ok = 0
                    for p in self.pixelList:
                        if pixel.x == p.x and pixel.y - 1 == p.y:
                            ok = 1
                        break
                    if ok == 0:
                        pixel.y -= 1
                        c += 1
            if c > 0:
                return 0
        return 1

    #changes the color of the pixel index based on color
    def changeColorPixel(self, s):
        if len(self.pixelList) == 0:
            return 1
        adapted_index = s.index % len(self.pixelList)
        if s.color % 2 == 0:
            if self.pixelList[adapted_index].color != 9:
                self.pixelList[adapted_index].color += 1
                return 0
        else:
            if self.pixelList[adapted_index].color != 1:
                self.pixelList[adapted_index].color -= 1
                return 0
        return 1

    #remove the pixel index
    def removePixel(self, s):
        if len(self.pixelList) == 0:
            return 1
        adapted_index = s.index % len(self.pixelList)
        self.pixelList.pop(adapted_index)
        return 0

    #generate a copy of the pixel index in the direction direction
    def duplicateNearPixel(self, s):
        if len(self.pixelList) == 0:
            return 1
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
                    self.pixelList.append(new_pixel)
                    return 0
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
                    self.pixelList.append(new_pixel)
                    return 0
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
                    self.pixelList.append(new_pixel)
                    return 0
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
                for pixel in self.pixelList:
                    pixel.x += 1
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
                for pixel in self.pixelList:
                    pixel.y += 1
                return 0
        return 1

    #reduce the grid in the direction direction
    def reduceGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            if self.nr > 1:
                self.nr -= 1
                remove = list()
                for x in range(0, len(self.pixelList)):
                    if self.pixelList[x].x == self.nr:
                        remove.append(x)
                remove.sort(reverse = True)
                for x in remove:
                    self.pixelList.pop(x)
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr > 1:
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
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc > 1:
                self.nc -= 1
                remove = list()
                for x in range(0, len(self.pixelList)):
                    if self.pixelList[x].y == self.nc:
                        remove.append(x)
                remove.sort(reverse = True)
                for x in remove:
                    self.pixelList.pop(x)
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc > 1:
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
                return 0
        return 1

    def score(self, output):
        #-1 punti per posizione non giusta, proporzionale distanza per colore sbagliato, -2 punti dimensione griglia sbagliata per casella
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        mask = [1 for _ in range(0, len(output.pixelList))]
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
    
    def optimizer(performed_actions, performed_selection):
        new_selection = list()
        new_action = list()
        mask = [1 for _ in range(0, len(performed_actions))]
        for x in range(0, len(performed_actions)):
            if performed_actions[x] == pixelRepresentation.changeColorPixel and mask[x] == 1:
                #changeColorPixel of a removePixel
                indexController = 0
                for y in range(x, len(performed_actions)):
                    if performed_actions[y] == pixelRepresentation.removePixel:
                        if performed_selection[y].index < performed_selection[x].index + indexController:
                            indexController -= 1
                        elif performed_selection[x].index + indexController == performed_selection[y].index:
                            mask[x] = 0
                            break
            




            '''
            for y in range(0, len(performed_actions)):
                if performed_actions[x] == pixelRepresentation.changeColorPixel and performed_actions[y] == pixelRepresentation.changeColorPixel and mask[x] == 1 and mask[y] == 1:
                    #double changeColorPixel
                    if performed_selection[x].index == performed_selection[y].index and performed_selection[x].color % 2 != performed_selection[y].color % 2:
                        #index si muove se duplico o rimuovo pixel
                        
                        mask[x] = 0
                        mask[y] = 0
                elif performed_actions[x] == pixelRepresentation.removePixel and performed_actions[y] == pixelRepresentation.changeColorPixel and mask[x] == 1 and mask[y] == 1:
                    #changeColorPixel of a removePixel
                    if performed_selection[x].index == performed_selection[y].index:
                        mask[y] = 0
            '''

            if mask[x] == 1:
                new_selection.append(performed_selection[x])
                new_action.append(performed_actions[x])
        return new_action, new_selection
    