import numpy as np
import copy
from selection.selector import Selector


class rowRepresentation:
    def __init__(self, input_grid):
        self.nr = input_grid.shape[0]
        self.nc = input_grid.shape[1]
        self.RigheList = list()
        for x in input_grid:
            riga = list()
            for y in x:
                riga.append(y)
            self.RigheList.append(copy.deepcopy(riga))

    #return the total number of row
    def getNElement(self):
        return self.nr
    
    #return the total number of column
    def getElementComponent(self):
        return self.nc

    #moves the row index if possible based on the direction
    def moveRiga(self, s):
        adapted_index = s.index % self.nr
        if (s.direction % 4) == 0:
            #sposto riga sopra
            if adapted_index > 0:
                rigaSopra = self.RigheList[adapted_index - 1]
                self.RigheList[adapted_index - 1] = self.RigheList[adapted_index]
                self.RigheList[adapted_index] = rigaSopra
                return 0
        elif (s.direction % 4) == 1:
            #sposto riga sotto
            if adapted_index + 1 < self.nr:
                rigaSopra = self.RigheList[adapted_index]
                self.RigheList[adapted_index] = self.RigheList[adapted_index + 1]
                self.RigheList[adapted_index + 1] = rigaSopra
                return 0
        elif (s.direction % 4) == 2:
            #scalo la riga verso destra
            new_riga = list()
            new_riga.append(self.RigheList[adapted_index][self.nc-1])
            for x in range(0, self.nc-1):
                new_riga.append(self.RigheList[adapted_index][x])
            self.RigheList[adapted_index] = new_riga
            return 0
        elif (s.direction % 4) == 3:
            #scalo la riga verso sinistra
            new_riga = list()
            for x in range(1, self.nc):
                new_riga.append(self.RigheList[adapted_index][x])
            new_riga.append(self.RigheList[adapted_index][0])
            self.RigheList[adapted_index] = new_riga
            return 0
        return 1

    #changes the color of the colored pixel in the row index based on color
    def changeColorRiga(self, s):
        adapted_index = s.index % self.nr
        ok = 0
        for element in self.RigheList[adapted_index]:
            if element != 0:
                if s.color % 2 == 0:
                    if element != 9:
                        element += 1
                        ok = 1
                else:
                    if element != 1:
                        element -= 1
                        ok = 1
        if ok == 1:
            return 0
        return 1

    #add a new colored pixel in the row index
    def modifyRigaAdd(self, s):
        adapted_index = s.index % self.nr
        adapted_component = s.component % self.nc
        if self.RigheList[adapted_index][adapted_component] == 0:
            color = 1
            for p in self.RigheList[adapted_index]:
                if p != 0:
                    color = p
                    break
            self.RigheList[adapted_index][adapted_component] == color
            return 0
        return 1
        
    #delete a colored pixel in the row index
    def modifyRigaDel(self, s):
        adapted_index = s.index % self.nr
        adapted_component = s.component % self.nc
        if self.RigheList[adapted_index][adapted_component] != 0:
            self.RigheList[adapted_index][adapted_component] == 0
            return 0
        return 1
    
    #swap two pixel based on direction in the row index
    def modifyRigaMove(self, s):
        adapted_index = s.index % self.nr
        adapted_component = s.component % self.nc
        if (s.direction % 4) == 0:
            #swappo andando verso destra
            if adapted_component + 1 < self.nc:
                tmp = self.RigheList[adapted_index][adapted_component + 1]
                self.RigheList[adapted_index][adapted_component + 1] = self.RigheList[adapted_index][adapted_component]
                self.RigheList[adapted_index][adapted_component] = tmp
                return 0
        elif (s.direction % 4) == 1:
            #swappo andando verso sinistra
            if adapted_component - 1 >= 0:
                tmp = self.RigheList[adapted_index][adapted_component - 1]
                self.RigheList[adapted_index][adapted_component - 1] = self.RigheList[adapted_index][adapted_component]
                self.RigheList[adapted_index][adapted_component] = tmp
                return 0  
        return 1

    #expand the grid in the direction direction
    def expandGrid(self, s):
        adapted_index = s.index % self.nr
        if (s.direction % 4) == 0:
            #down
            if self.nr < 30:
                self.nr += 1
                new_Riga = copy.deepcopy(self.RigheList[adapted_index])
                self.RigheList.append(new_Riga) 
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr < 30:
                self.nr += 1
                new_Riga = copy.deepcopy(self.RigheList[adapted_index])
                new_RigheList = [new_Riga]
                for riga in self.RigheList:
                    new_RigheList.append(riga)
                self.RigheList = new_RigheList
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc < 30:
                self.nc += 1
                for x in range(0, self.nr):
                    self.RigheList[x].append(0)
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc < 30:
                self.nc += 1
                for x in range(0, self.nr):
                    new_riga = list()
                    new_riga.append(0)
                    for element in self.RigheList[x]:
                        new_riga.append(element)
                    self.RigheList[x] = new_riga
                return 0
        return 1

    #reduce the grid in the direction direction
    def reduceGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            if self.nr > 1:
                self.nr -= 1
                self.RigheList.pop()
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr > 1:
                self.nr -= 1
                self.RigheList.pop(0)
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc > 1:
                self.nc -= 1
                for riga in self.RigheList:
                    riga.pop()
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc > 1:
                self.nc -= 1
                for riga in self.RigheList:
                    riga.pop(0)
                return 0
        return 1

    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        if self.nr <= output.nr and self.nc <= output.nc:
            for x in range(self.nr):
                for y in range(self.nc):
                    if output.RigheList[x][y] != self.RigheList[x][y]:
                        if output.RigheList[x][y] == 0 or self.RigheList[x][y] == 0:
                            score += 1
                        else:
                            score += abs(int(self.RigheList[x][y]) - int(output.RigheList[x][y]))/10
        elif self.nr > output.nr and self.nc > output.nc:
            for x in range(output.nr):
                for y in range(output.nc):
                    if output.RigheList[x][y] != self.RigheList[x][y]:
                        if output.RigheList[x][y] == 0 or self.RigheList[x][y] == 0:
                            score += 1
                        else:
                            score += abs(int(self.RigheList[x][y]) - int(output.RigheList[x][y]))/10
        elif self.nr <= output.nr and self.nc > output.nc:
            for x in range(self.nr):
                for y in range(output.nc):
                    if output.RigheList[x][y] != self.RigheList[x][y]:
                        if output.RigheList[x][y] == 0 or self.RigheList[x][y] == 0:
                            score += 1
                        else:
                            score += abs(int(self.RigheList[x][y]) - int(output.RigheList[x][y]))/10
        elif self.nr > output.nr and self.nc <= output.nc:
            for x in range(output.nr):
                for y in range(self.nc):
                    if output.RigheList[x][y] != self.RigheList[x][y]:
                        if output.RigheList[x][y] == 0 or self.RigheList[x][y] == 0:
                            score += 1
                        else:
                            score += abs(int(self.RigheList[x][y]) - int(output.RigheList[x][y]))/10
        return -score

    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for x in range(0, self.nr):
            for y in range(0, self.nc):
                grid[x][y] = self.RigheList[x][y]
        return grid