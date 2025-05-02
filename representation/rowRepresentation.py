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
    def getElementComponent(self, index):
        return (self.nc,)

    #return the list of row index
    def generateIndexList(self, s):
        l = list()
        if s.allElement == 1:
            #sotto
            l.append(self.nr - (s.index % self.nr) - 1)
        elif s.allElement == 2:
            #centro
            if self.nr % 2 == 1:
                l.append(self.nr // 2)
            else:
                l.append(self.nr // 2 - 1)
                l.append(self.nr // 2)
        elif s.allElement == 3:
            #all the row
            l = [x for x in range(0, self.nr)]
        elif s.allElement == 4:
            #the row need to contain a crtaint color
            for x in range(0, self.nr):
                ok = 0
                for p in self.RigheList[x]:
                    if p == s.color:
                        ok = 1
                if ok == 1:
                    l.append(x)
        else:
            #sopra
            l.append(s.index % self.nr)
        return l
    
    #return the list of component index
    def generateComponentList(self, s, adapted_index):
        l = list()
        if s.allComponent == 1:
            #da destra
            l.append(self.nc - (s.component[0] % self.nc) - 1)
        elif s.allComponent == 2:
            #centro
            if self.nc % 2 == 1:
                l.append(self.nc // 2)
            else:
                l.append(self.nc // 2 - 1)
                l.append(self.nc // 2)
        elif s.allComponent == 3:
            #all
            l = [x for x in range(0, self.nc)]
        elif s.allComponent == 4:
            #component of the selected color
            for c, p in enumerate(self.RigheList[adapted_index]):
                if p == s.color:
                    l.append(c)
        else:
            #da sinistra
            l.append(s.component[0] % self.nc)
        return l

    #moves the row index if possible based on the direction
    def moveRow(self, s):
        count = 0
        l = self.generateIndexList(s)
        if (s.direction % 4) == 0 and s.allElement == 2 and len(l) > 1:
            #sposto le righe colorate sotto    
            l.sort(key=lambda i: i, reverse=False)
            for x in range(0, len(l)-1):
                if x + 1 < len(l):
                    rigaSopra = self.RigheList[l[x]]
                    self.RigheList[l[x]] = self.RigheList[l[x + 1]]
                    self.RigheList[l[x + 1]] = rigaSopra
                    count += 1
                elif x + 1 == len(l):
                    rigaSopra = self.RigheList[l[x]]
                    self.RigheList[l[x]] = self.RigheList[l[0]]
                    self.RigheList[l[0]] = rigaSopra
                    count += 1
        elif (s.direction % 4) == 1 and s.allElement == 2 and len(l) > 1:
            #sposto le righe colorate sopra
            l.sort(key=lambda i: i, reverse=True)
            for x in range(0, len(l)-1):
                if x > 0:
                    rigaSopra = self.RigheList[l[x - 1]]
                    self.RigheList[l[x - 1]] = self.RigheList[l[x]]
                    self.RigheList[l[x]] = rigaSopra
                    count += 1
                elif x == 0:
                    rigaSopra = self.RigheList[l[-1]]
                    self.RigheList[l[-1]] = self.RigheList[l[x]]
                    self.RigheList[l[x]] = rigaSopra
                    count += 1
        else:
            if (s.direction % 4) == 0 and s.allElement == 1:
                l.sort(key=lambda i: i, reverse=False)
                l.pop(-1)
            elif (s.direction % 4) == 1 and s.allElement == 1:
                l.sort(key=lambda i: i, reverse=True)
                l.pop(-1)
            for adapted_index in l:
                if (s.direction % 4) == 0:
                    #sposto riga sotto
                    if adapted_index + 1 < self.nr:
                        rigaSopra = self.RigheList[adapted_index]
                        self.RigheList[adapted_index] = self.RigheList[adapted_index + 1]
                        self.RigheList[adapted_index + 1] = rigaSopra
                        count += 1
                    elif adapted_index + 1 == self.nr:
                        rigaSopra = self.RigheList[0]
                        self.RigheList[0] = self.RigheList[adapted_index]
                        self.RigheList[adapted_index] = rigaSopra
                        count += 1
                elif (s.direction % 4) == 1:
                    #sposto riga sopra
                    if adapted_index > 0:
                        rigaSopra = self.RigheList[adapted_index - 1]
                        self.RigheList[adapted_index - 1] = self.RigheList[adapted_index]
                        self.RigheList[adapted_index] = rigaSopra
                        count += 1
                    elif adapted_index == 0:
                        rigaSopra = self.RigheList[self.nr - 1]
                        self.RigheList[self.nr - 1] = self.RigheList[adapted_index]
                        self.RigheList[adapted_index] = rigaSopra
                        count += 1
                elif (s.direction % 4) == 2:
                    #scalo la riga verso destra
                    new_riga = list()
                    new_riga.append(self.RigheList[adapted_index][self.nc-1])
                    for x in range(0, self.nc-1):
                        new_riga.append(self.RigheList[adapted_index][x])
                    self.RigheList[adapted_index] = new_riga
                    count += 1
                elif (s.direction % 4) == 3:
                    #scalo la riga verso sinistra
                    new_riga = list()
                    for x in range(1, self.nc):
                        new_riga.append(self.RigheList[adapted_index][x])
                    new_riga.append(self.RigheList[adapted_index][0])
                    self.RigheList[adapted_index] = new_riga
                    count += 1
        if count != 0:
            return 0
        return 1

    #changes the color of the colored pixels in the row index based on color
    def changeColorRow(self, s):
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            for x in range(0, self.nc):
                if self.RigheList[adapted_index][x] != 0:
                    if s.color % 2 == 0:
                        if self.RigheList[adapted_index][x] != 9:
                            self.RigheList[adapted_index][x] += 1
                            count += 1
                    else:
                        if self.RigheList[adapted_index][x] != 1:
                            self.RigheList[adapted_index][x] -= 1
                            count += 1
        if count != 0:
            return 0
        return 1

    #changes the color of the selected pixel in the row index based on color
    def changeColorRowPixel(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            for adapted_component in lc:
                if self.RigheList[adapted_index][adapted_component] != 0:
                    if s.color % 2 == 0:
                        if self.RigheList[adapted_index][adapted_component] != 9:
                            self.RigheList[adapted_index][adapted_component] += 1
                            count += 1
                    else:
                        if self.RigheList[adapted_index][adapted_component] != 1:
                            self.RigheList[adapted_index][adapted_component] -= 1
                            count += 1
        if count != 0:
            return 0
        return 1

    #add a new colored pixel in the row index
    def modifyRowAdd(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            for adapted_component in lc:
                if self.RigheList[adapted_index][adapted_component] == 0:
                    color = 1
                    for p in self.RigheList[adapted_index]:
                        if p != 0:
                            color = p
                            break
                    self.RigheList[adapted_index][adapted_component] == color
                    count += 1
        if count != 0:
            return 0
        return 1
        
    #delete a colored pixel in the row index
    def modifyRowDel(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            for adapted_component in lc:
                if self.RigheList[adapted_index][adapted_component] != 0:
                    self.RigheList[adapted_index][adapted_component] == 0
                    count += 1
        if count != 0:
            return 0
        return 1
    
    #swap two pixel based on direction in the row index
    def modifyRowMove(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            if (s.direction % 2) == 0:
                lc.sort(key=lambda i: i, reverse=True)
            elif (s.direction % 2) == 1:
                lc.sort(key=lambda i: i, reverse=False)
            if len(lc) == self.nc:
                lc.pop(-1)
            for adapted_component in lc:
                if (s.direction % 2) == 0:
                    #swappo andando verso destra
                    if adapted_component + 1 < self.nc:
                        tmp = self.RigheList[adapted_index][adapted_component + 1]
                        self.RigheList[adapted_index][adapted_component + 1] = self.RigheList[adapted_index][adapted_component]
                        self.RigheList[adapted_index][adapted_component] = tmp
                        count += 1
                    elif adapted_component + 1 == self.nc:
                        tmp = self.RigheList[adapted_index][0]
                        self.RigheList[adapted_index][0] = self.RigheList[adapted_index][adapted_component]
                        self.RigheList[adapted_index][adapted_component] = tmp
                        count += 1
                elif (s.direction % 2) == 1:
                    #swappo andando verso sinistra
                    if adapted_component - 1 >= 0:
                        tmp = self.RigheList[adapted_index][adapted_component - 1]
                        self.RigheList[adapted_index][adapted_component - 1] = self.RigheList[adapted_index][adapted_component]
                        self.RigheList[adapted_index][adapted_component] = tmp
                        count += 1 
                    elif adapted_component == 0:
                        tmp = self.RigheList[adapted_index][self.nc - 1]
                        self.RigheList[adapted_index][self.nc - 1] = self.RigheList[adapted_index][adapted_component]
                        self.RigheList[adapted_index][adapted_component] = tmp
                        count += 1 
        if count != 0:
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
    
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_selection[x].allElement < 3: 
                score += 0.5
            if performed_actions[x] == rowRepresentation.changeColorRowPixel or performed_actions[x] == rowRepresentation.modifyRowAdd or performed_actions[x] == rowRepresentation.modifyRowDel or performed_actions[x] == rowRepresentation.modifyRowMove:
                score += 0.5
            score += 1
        return -score