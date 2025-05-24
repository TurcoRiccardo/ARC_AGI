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
        return (self.nr * self.nc,)
    
    #return the list of pixel index
    def generateIndexList(self, s):
        l = list()
        if s.allElement == 1:
            #sotto
            l.append(len(self.pixelList) - (s.index % len(self.pixelList)) - 1)
        elif s.allElement == 2:
            #centro
            if len(self.pixelList) % 2 == 1:
                l.append(len(self.pixelList) // 2)
            else:
                l.append(len(self.pixelList) // 2 - 1)
                l.append(len(self.pixelList) // 2)
        elif s.allElement == 3:
            #all
            l = [x for x in range(0, len(self.pixelList))]
        elif s.allElement == 4:
            #color
            for x in range(0, len(self.pixelList)):
                if self.pixelList[x].color == s.color:
                    l.append(x)
        else:
            #sopra
            l.append(s.index % len(self.pixelList))
        return l


    #moves the pixel index if possible based on the direction
    def movePixel(self, s):
        if len(self.pixelList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if (s.direction % 4) == 0:
                if self.pixelList[adapted_index].x + 1 < self.nr:
                    #down
                    self.pixelList[adapted_index].x += 1
                    count += 1
            elif (s.direction % 4) == 1:
                if self.pixelList[adapted_index].x > 0:
                    #up
                    self.pixelList[adapted_index].x -= 1
                    count += 1
            elif (s.direction % 4) == 2:
                if self.pixelList[adapted_index].y + 1 < self.nc:
                    #right
                    self.pixelList[adapted_index].y += 1
                    count += 1
            elif (s.direction % 4) == 3:
                if self.pixelList[adapted_index].y > 0:
                    #left
                    self.pixelList[adapted_index].y -= 1
                    count += 1
        if count != 0:
            return 0
        return 1

    #changes the color of the pixel index based on color
    def changeColorPixel(self, s):
        if len(self.pixelList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if s.color % 2 == 0:
                if self.pixelList[adapted_index].color != 9:
                    self.pixelList[adapted_index].color += 1
                    count += 1
            else:
                if self.pixelList[adapted_index].color != 1:
                    self.pixelList[adapted_index].color -= 1
                    count += 1
        if count != 0:
            return 0
        return 1

    #remove the pixel index
    def removePixel(self, s):
        if len(self.pixelList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        l.sort(key=lambda i: i, reverse=True)
        for adapted_index in l:
            self.pixelList.pop(adapted_index)
            count += 1
        if count != 0:
            return 0
        return 1

    #generate a copy of the pixel index
    def duplicatePixel(self, s):
        if len(self.pixelList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        newPixel = []
        for adapted_index in l:
            new_pixel = PixelNode(self.pixelList[adapted_index].x, self.pixelList[adapted_index].y, self.pixelList[adapted_index].color)
            newPixel.append((adapted_index+1, new_pixel))
            count += 1
        if count != 0:
            newPixel.sort(key=lambda i: i[0], reverse=True)
            for (index, fig) in newPixel:
                self.pixelList.insert(index, fig)
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


    #fitness function
    def score(self, output):
        #-1 punti per posizione non giusta, proporzionale distanza per colore sbagliato, -2 punti dimensione griglia sbagliata per casella
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        for z in range(0, len(self.pixelList)):
            if z < len(output.pixelList):
                #distance
                score += abs(int(self.pixelList[z].x) - int(output.pixelList[z].x))/10 + abs(int(self.pixelList[z].y) - int(output.pixelList[z].y))/10
                #color
                score += abs(int(self.pixelList[z].color) - int(output.pixelList[z].color))/10
        else:
            score += 1 * 1.2
        if len(output.pixelList) - len(self.pixelList) > 0:
            score += (len(output.pixelList) - len(self.pixelList)) * 1.5
        return -score

    #transform the representation into an ARC grid
    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for pixel in self.pixelList:
            grid[pixel.x][pixel.y] = pixel.color
        return grid
    
    #function that calculates a score based on the selectors used
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_selection[x].allElement < 3: 
                score += 0.5
            if performed_actions[x] == pixelRepresentation.duplicatePixel or performed_actions[x] == pixelRepresentation.removePixel:
                score += 0.5
            score += 1
        return -score
    
    #return the list of actions
    def actionList(pc):     
        l = [pixelRepresentation.movePixel]
        if pc.countDim != pc.numProb:
            l.append(pixelRepresentation.expandGrid)
            l.append(pixelRepresentation.reduceGrid)
        if pc.countColor != pc.numProb:
            l.append(pixelRepresentation.changeColorPixel)
        if pc.countRemove > 0:
            l.append(pixelRepresentation.removePixel)
        if pc.countAdd > 0:
            l.append(pixelRepresentation.duplicatePixel)
        return l
    
    #return the list of base actions
    def baseActionList(pc):
        l = []
        if pc.countAdd > 0:
            l.append(pixelRepresentation.duplicatePixel)
        if pc.countDim != pc.numProb:
            l.append(pixelRepresentation.expandGrid)
            l.append(pixelRepresentation.reduceGrid)
        return l