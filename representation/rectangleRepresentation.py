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
    
    #return the total number of rectangle
    def getNElement(self):
        return len(self.rectangleList)
    
    #return the total number of pixel in the rectangle
    def getElementComponent(self, index):
        adapted_index = index % len(self.rectangleList)
        return (self.rectangleList[adapted_index].h * self.rectangleList[adapted_index].w,)
    
    #return the list of rectangle index
    def generateIndexList(self, s):
        l = list()
        if s.allElement == 1:
            #sotto
            l.append(len(self.rectangleList) - (s.index % len(self.rectangleList)) - 1)
        elif s.allElement == 2:
            #centro
            if len(self.rectangleList) % 2 == 1:
                l.append(len(self.rectangleList) // 2)
            else:
                l.append(len(self.rectangleList) // 2 - 1)
                l.append(len(self.rectangleList) // 2)
        elif s.allElement == 3:
            #all
            l = [x for x in range(0, len(self.rectangleList))]
        elif s.allElement == 4:
            #color
            for x in range(0, len(self.rectangleList)):
                if self.rectangleList[x].color == s.color:
                    l.append(x)
        else:
            #sopra
            l.append(s.index % len(self.rectangleList))
        return l
    

    #moves the rectangle index based on the direction
    def moveRectangle(self, s):
        if len(self.rectangleList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        if (s.direction % 4) == 0:
            l.sort(key=lambda i: self.rectangleList[i].x, reverse=True)
        elif (s.direction % 4) == 1:
            l.sort(key=lambda i: self.rectangleList[i].x, reverse=False)
        elif (s.direction % 4) == 2:
            l.sort(key=lambda i: self.rectangleList[i].y, reverse=True)
        elif (s.direction % 4) == 3:
            l.sort(key=lambda i: self.rectangleList[i].y, reverse=False)
        for adapted_index in l:
            if (s.direction % 4) == 0:
                #down
                if self.rectangleList[adapted_index].x + self.rectangleList[adapted_index].h < self.nr:
                    self.rectangleList[adapted_index].x += 1
                    count += 1
            elif (s.direction % 4) == 1:
                #up
                if self.rectangleList[adapted_index].x > 0:
                    self.rectangleList[adapted_index].x -= 1
                    count += 1
            elif (s.direction % 4) == 2:
                #right
                if self.rectangleList[adapted_index].y + self.rectangleList[adapted_index].w < self.nc:
                    self.rectangleList[adapted_index].y += 1
                    count += 1
            elif (s.direction % 4) == 3:
                #left
                if self.rectangleList[adapted_index].y > 0:
                    self.rectangleList[adapted_index].x -= 1
                    count += 1
        if count != 0:
            return 0
        return 1
    
    #changes the color of the rectangle index based on color
    def changeColorRectangle(self, s):
        if len(self.rectangleList) == 0:
            return
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if s.color % 2 == 0:
                if self.rectangleList[adapted_index].color != 9:
                    self.rectangleList[adapted_index].color += 1
                    count += 1
            else:
                if self.rectangleList[adapted_index].color != 1:
                    self.rectangleList[adapted_index].color -= 1
                    count += 1
        if count != 0:
            return 0
        return 1

    #remove the rectangle index
    def removeRectangle(self, s):
        if len(self.rectangleList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        l.sort(key=lambda i: i, reverse=True)
        for adapted_index in l:
            self.rectangleList.pop(adapted_index)
            count += 1
        if count != 0:
            return 0
        return 1

    #duplicate the selected rectangle
    def duplicateRectangle(self, s):
        if len(self.rectangleList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        duplicatedRectangle = []
        for adapted_index in l:
            new_rectangle = Rectangle(self.rectangleList[adapted_index].x, self.rectangleList[adapted_index].y, self.rectangleList[adapted_index].h, self.rectangleList[adapted_index].w, self.rectangleList[adapted_index].color)
            duplicatedRectangle.append((adapted_index, new_rectangle))
            count += 1
        if count != 0:
            duplicatedRectangle.sort(key=lambda i: i[0], reverse=True)
            for (index, fig) in duplicatedRectangle:
                self.rectangleList.insert(index, fig)
            return 0
        return 1

    #change the order of the rectangle based on color in the rectangle list
    def changeOrder(self, s):
        if len(self.rectangleList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        if (s.color % 2) == 0:
            l.sort(key=lambda i: i, reverse=True)
        elif (s.color % 2) == 1:
            l.sort(key=lambda i: i, reverse=False)
        for adapted_index in l:
            if s.color % 2 == 0:
                if adapted_index + 1 < len(self.rectangleList):
                    self.rectangleList[adapted_index], self.rectangleList[adapted_index + 1] = self.rectangleList[adapted_index + 1], self.rectangleList[adapted_index]
                    count += 1
            else:
                if adapted_index - 1 >= 0:
                    self.rectangleList[adapted_index], self.rectangleList[adapted_index - 1] = self.rectangleList[adapted_index - 1], self.rectangleList[adapted_index]
                    count += 1
        if count != 0:
            return 0
        return 1

    #scale up the rectangle index in the direction direction
    def scaleUpRectangle(self, s):
        if len(self.rectangleList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if (s.direction % 4) == 0:
                #down
                if self.rectangleList[adapted_index].x + self.rectangleList[adapted_index].h < self.nr:
                    self.rectangleList[adapted_index].h += 1
                    count += 1
            elif (s.direction % 4) == 1:
                #up
                if self.rectangleList[adapted_index].x > 0:
                    self.rectangleList[adapted_index].x -= 1
                    self.rectangleList[adapted_index].h += 1
                    count += 1
            elif (s.direction % 4) == 2:
                #right
                if self.rectangleList[adapted_index].y + self.rectangleList[adapted_index].w < self.nc:
                    self.rectangleList[adapted_index].w += 1
                    count += 1
            elif (s.direction % 4) == 3:
                #left
                if self.rectangleList[adapted_index].y > 0:
                    self.rectangleList[adapted_index].y -= 1
                    self.rectangleList[adapted_index].w += 1
                    count += 1
        if count != 0:
            return 0
        return 1
    
    #scale down the rectangle index in the direction direction
    def scaleDownRectangle(self, s):
        if len(self.rectangleList) == 0:
            return 1
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if (s.direction % 4) == 0:
                #down
                if self.rectangleList[adapted_index].h > 1:
                    self.rectangleList[adapted_index].h -= 1
                    count += 1
            elif (s.direction % 4) == 1:
                #up
                if self.rectangleList[adapted_index].h > 1:
                    self.rectangleList[adapted_index].x += 1
                    self.rectangleList[adapted_index].h -= 1
                    count += 1
            elif (s.direction % 4) == 2:
                #right
                if self.rectangleList[adapted_index].w > 1:
                    self.rectangleList[adapted_index].w -= 1
                    count += 1
            elif (s.direction % 4) == 3:
                #left
                if self.rectangleList[adapted_index].w > 1:
                    self.rectangleList[adapted_index].y += 1
                    self.rectangleList[adapted_index].w -= 1
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

    #reduce the grid in the direction direction
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
    

    #fitness function
    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        for z in range(0, len(self.rectangleList)):
            if z < len(output.rectangleList):
                #distanza tra le x piu distanza tra le y
                score += abs(self.rectangleList[z].x - output.rectangleList[z].x) + abs(self.rectangleList[z].y - output.rectangleList[z].y)
                #distanza tra le h piu distanza tra le w
                score += abs(self.rectangleList[z].h - output.rectangleList[z].h) + abs(self.rectangleList[z].w - output.rectangleList[z].w)
                #distanza tra il colore
                if self.rectangleList[z].color != 0 and output.rectangleList[z].color != 0:
                    score += abs(int(self.rectangleList[z].color) - int(output.rectangleList[z].color))
                elif self.rectangleList[z].color == 0 and output.rectangleList[z].color == 0:
                    score += 0
                else:
                    score += 1
            else:
                score += self.rectangleList[z].h * self.rectangleList[z].w
        if len(output.rectangleList) - len(self.rectangleList) > 0:
            for z in range(len(self.rectangleList), len(output.rectangleList)):
                score += output.rectangleList[z].h * output.rectangleList[z].w * 1.5
        return -score

    #transform the representation into an ARC grid
    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for rectangle in self.rectangleList:
            for j in range(rectangle.x, rectangle.x + rectangle.h):
                for k in range(rectangle.y, rectangle.y + rectangle.w):
                    grid[j][k] = rectangle.color
        return grid

    #function that calculates a score based on the selectors used
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_selection[x].allElement < 3: 
                score += 0.5
            if performed_actions[x] == rectangleRepresentation.removeRectangle or performed_actions[x] == rectangleRepresentation.duplicateRectangle or performed_actions[x] == rectangleRepresentation.changeOrder:
                score += 0.5
            score += 1
        return -score
    
    #return the list of actions
    def actionList(pc):     
        l = [rectangleRepresentation.moveRectangle, rectangleRepresentation.changeOrder, rectangleRepresentation.scaleUpRectangle, rectangleRepresentation.scaleDownRectangle]
        if pc.countDim > 0:
            l.append(rectangleRepresentation.expandGrid)
            l.append(rectangleRepresentation.reduceGrid)
        if pc.countColor != pc.numProb:
            l.append(rectangleRepresentation.changeColorRectangle)
        if pc.countRemove > 0:
            l.append(rectangleRepresentation.removeRectangle)
        if pc.countAdd > 0:
            l.append(rectangleRepresentation.duplicateRectangle)
        return l
    
    #return the list of base actions
    def baseActionList(pc):
        l = [rectangleRepresentation.moveRectangle, rectangleRepresentation.changeOrder]
        if pc.countColor != pc.numProb:
            l.append(rectangleRepresentation.changeColorRectangle)
        if pc.countAdd > 0:
            l.append(rectangleRepresentation.duplicateRectangle)
        if pc.countDim > 0:
            l.append(rectangleRepresentation.expandGrid)
            l.append(rectangleRepresentation.reduceGrid)
        return l