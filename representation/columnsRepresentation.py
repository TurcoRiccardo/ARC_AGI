import numpy as np
import copy
from selection.selector import Selector


class columnsRepresentation:
    def __init__(self, input_grid):
        self.nr = input_grid.shape[0]
        self.nc = input_grid.shape[1]
        self.ColonneList = list()
        for x in input_grid.T:
            colonna = list()
            for y in x:
                colonna.append(y)
            self.ColonneList.append(copy.deepcopy(colonna))

    #return the total number of column
    def getNElement(self):
        return self.nc
    
    #return the total number of row 
    def getElementComponent(self, index):
        return (self.nr,)

    #return the list of column index
    def generateIndexList(self, s):
        l = list()
        if s.allElement == 1:
            #sotto
            l.append(self.nc - (s.index % self.nc) - 1)
        elif s.allElement == 2:
            #centro
            if self.nc % 2 == 1:
                l.append(self.nc // 2)
            else:
                l.append(self.nc // 2 - 1)
                l.append(self.nc // 2)
        elif s.allElement == 3:
            #all
            l = [y for y in range(0, self.nc)]
        elif s.allElement == 4:
            #color
            for y in range(0, self.nc):
                color = 0
                for p in self.ColonneList[y]:
                    if p != 0:
                        color = p
                if color == s.color:
                    l.append(y)
        else:
            #sopra
            l.append(s.index % self.nc)
        return l

    #return the list of component index
    def generateComponentList(self, s, adapted_index):
        l = list()
        if s.allComponent1 == 1:
            #da destra
            l.append(self.nr - (s.component[0] % self.nr) - 1)
        elif s.allComponent1 == 2:
            #centro
            if self.nc % 2 == 1:
                l.append(self.nr // 2)
            else:
                l.append(self.nr // 2 - 1)
                l.append(self.nr // 2)
        elif s.allComponent1 == 3:
            #all
            l = [x for x in range(0, self.nr)]
        elif s.allComponent1 == 4:
            #component of the selected color
            for c, p in enumerate(self.ColonneList[adapted_index]):
                if p == s.color:
                    l.append(c)
        else:
            #da sinistra
            l.append(s.component[0] % self.nr)
        return l


    #moves the column index if possible based on the direction
    def moveColumn(self, s):
        count = 0
        l = self.generateIndexList(s)
        if (s.direction % 4) == 2 and s.allElement == 2 and len(l) > 1:
            #sposto le colonne colorate a destra    
            l.sort(key=lambda i: i, reverse=True)
            for x in range(0, len(l)-1):
                if x + 1 < len(l):
                    colonnaDestra = self.ColonneList[l[x + 1]]
                    self.ColonneList[l[x + 1]] = self.ColonneList[l[x]]
                    self.ColonneList[l[x]] = colonnaDestra
                    count += 1
                elif x + 1 == len(l):
                    colonnaDestra = self.ColonneList[l[0]]
                    self.ColonneList[l[0]] = self.ColonneList[l[x]]
                    self.ColonneList[l[x]] = colonnaDestra
                    count += 1
        elif (s.direction % 4) == 3 and s.allElement == 2 and len(l) > 1:
            #sposto le colonne colorate a sinista
            l.sort(key=lambda i: i, reverse=False)
            for x in range(0, len(l)-1):
                if x > 0:
                    colonnaDestra = self.ColonneList[l[x]]
                    self.ColonneList[l[x]] = self.ColonneList[l[x - 1]]
                    self.ColonneList[l[x - 1]] = colonnaDestra
                    count += 1
                elif x == 0:
                    colonnaDestra = self.ColonneList[l[x]]
                    self.ColonneList[l[x]] = self.ColonneList[l[-1]]
                    self.ColonneList[l[-1]] = colonnaDestra
                    count += 1
        else:
            if (s.direction % 4) == 2 and s.allElement == 1:
                l.sort(key=lambda i: i, reverse=True)
                l.pop(-1)
            elif (s.direction % 4) == 3 and s.allElement == 1:
                l.sort(key=lambda i: i, reverse=False)
                l.pop(-1)
            for adapted_index in l:
                if (s.direction % 4) == 0:
                    #scalo la colonna verso il basso
                    new_colonna = list()
                    new_colonna.append(self.ColonneList[adapted_index][self.nr-1])
                    for x in range(0, self.nr-1):
                        new_colonna.append(self.ColonneList[adapted_index][x])
                    self.ColonneList[adapted_index] = new_colonna
                    count += 1
                elif (s.direction % 4) == 1:
                    #scalo la colonna verso l'alto
                    new_colonna = list()
                    for x in range(1, self.nr):
                        new_colonna.append(self.ColonneList[adapted_index][x])
                    new_colonna.append(self.ColonneList[adapted_index][0])
                    self.ColonneList[adapted_index] = new_colonna
                    count += 1
                elif (s.direction % 4) == 2:
                    #sposto la colonna a destra      
                    if adapted_index + 1 < self.nc:
                        colonnaDestra = self.ColonneList[adapted_index + 1]
                        self.ColonneList[adapted_index + 1] = self.ColonneList[adapted_index]
                        self.ColonneList[adapted_index] = colonnaDestra
                        count += 1
                    elif adapted_index + 1 == self.nc:
                        colonnaDestra = self.ColonneList[0]
                        self.ColonneList[0] = self.ColonneList[adapted_index]
                        self.ColonneList[adapted_index] = colonnaDestra
                        count += 1
                elif (s.direction % 4) == 3:
                    #sposto la colonna a sinista
                    if adapted_index > 0:
                        colonnaDestra = self.ColonneList[adapted_index]
                        self.ColonneList[adapted_index] = self.ColonneList[adapted_index - 1]
                        self.ColonneList[adapted_index - 1] = colonnaDestra
                        count += 1
                    elif adapted_index == 0:
                        colonnaDestra = self.ColonneList[self.nc - 1]
                        self.ColonneList[self.nc - 1] = self.ColonneList[adapted_index]
                        self.ColonneList[adapted_index] = colonnaDestra
                        count += 1
        if count != 0:
            return 0
        return 1

    #changes the color of the colored pixels in the column index based on color
    def changeColorColumn(self, s):
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            for x in range(0, self.nr):
                if self.ColonneList[adapted_index][x] != 0:
                    if s.color % 2 == 0:
                        if self.ColonneList[adapted_index][x] != 9:
                            self.ColonneList[adapted_index][x] += 1
                            count += 1
                    else:
                        if self.ColonneList[adapted_index][x] != 1:
                            self.ColonneList[adapted_index][x] -= 1
                            count += 1
        if count != 0:
            return 0
        return 1

    #changes the color of the selected pixel in the column index based on color
    def changeColorColumnPixel(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            for adapted_component in lc:
                if self.ColonneList[adapted_index][adapted_component] != 0:
                    if s.color % 2 == 0:
                        if self.ColonneList[adapted_index][adapted_component] != 9:
                            self.ColonneList[adapted_index][adapted_component] += 1
                            count += 1
                    else:
                        if self.ColonneList[adapted_index][adapted_component] != 1:
                            self.ColonneList[adapted_index][adapted_component] -= 1
                            count += 1
        if count != 0:
            return 0
        return 1

    #add a new colored pixel in the column index
    def modifyColumnAdd(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            for adapted_component in lc:
                if self.ColonneList[adapted_index][adapted_component] == 0:
                    color = 1
                    for p in self.ColonneList[adapted_index]:
                        if p != 0:
                            color = p
                            break
                    self.ColonneList[adapted_index][adapted_component] == color
                    count += 1
        if count != 0:
            return 0
        return 1

    #delete a colored pixel in the row index
    def modifyColumnDel(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            for adapted_component in lc:
                if self.ColonneList[adapted_index][adapted_component] != 0:
                    self.ColonneList[adapted_index][adapted_component] == 0
                    count += 1
        if count != 0:
            return 0
        return 1

    #swap two pixel based on direction in the row index
    def modifyColumnMove(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            if (s.direction % 2) == 0:
                lc.sort(key=lambda i: i, reverse=True)
            elif (s.direction % 2) == 1:
                lc.sort(key=lambda i: i, reverse=False)
            if len(lc) == self.nr:
                lc.pop(-1)
            for adapted_component in lc:
                if (s.direction % 2) == 0:
                    #swappo andando verso il basso
                    if adapted_component + 1 < self.nr:
                        tmp = self.ColonneList[adapted_index][adapted_component + 1]
                        self.ColonneList[adapted_index][adapted_component + 1] = self.ColonneList[adapted_index][adapted_component]
                        self.ColonneList[adapted_index][adapted_component] = tmp
                        count += 1
                    elif adapted_component + 1 == self.nr:
                        tmp = self.ColonneList[adapted_index][0]
                        self.ColonneList[adapted_index][0] = self.ColonneList[adapted_index][adapted_component]
                        self.ColonneList[adapted_index][adapted_component] = tmp
                        count += 1
                elif (s.direction % 2) == 1:
                    #swappo andando verso l'alto
                    if adapted_component - 1 >= 0:
                        tmp = self.ColonneList[adapted_index][adapted_component - 1]
                        self.ColonneList[adapted_index][adapted_component - 1] = self.ColonneList[adapted_index][adapted_component]
                        self.ColonneList[adapted_index][adapted_component] = tmp
                        count += 1  
                    elif adapted_component == 0:
                        tmp = self.ColonneList[adapted_index][self.nr - 1]
                        self.ColonneList[adapted_index][self.nr - 1] = self.ColonneList[adapted_index][adapted_component]
                        self.ColonneList[adapted_index][adapted_component] = tmp
                        count += 1  
        if count != 0:
            return 0
        return 1
    
    #expand the grid in the direction direction
    def expandGrid(self, s):
        adapted_index = s.index % self.nc
        if (s.direction % 4) == 0:
            #down
            if self.nr < 30:
                self.nr += 1
                for x in range(0, self.nc):
                    self.ColonneList[x].append(0)
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr < 30:
                self.nr += 1
                for x in range(0, self.nc):
                    new_Colonna = list()
                    new_Colonna.append(0)
                    for element in self.ColonneList[x]:
                        new_Colonna.append(element)
                    self.ColonneList[x] = new_Colonna
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc < 30:
                self.nc += 1
                new_Colonna = copy.deepcopy(self.ColonneList[adapted_index])
                self.ColonneList.append(new_Colonna)
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc < 30:
                self.nc += 1
                new_Colonna = copy.deepcopy(self.ColonneList[adapted_index])
                new_ColonneList = [new_Colonna]
                for colonna in self.ColonneList:
                    new_ColonneList.append(colonna)
                self.ColonneList = new_ColonneList
                return 0
        return 1

    #reduce the grid in the direction direction
    def reduceGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            if self.nr > 1:
                self.nr -= 1
                for colonna in self.ColonneList:
                    colonna.pop()
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr > 1:
                self.nr -= 1
                for colonna in self.ColonneList:
                    colonna.pop(0)
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc > 1:
                self.nc -= 1
                self.ColonneList.pop()
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc > 1:
                self.nc -= 1
                self.ColonneList.pop(0)
                return 0
        return 1


    #fitness function
    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        if self.nr <= output.nr and self.nc <= output.nc:
            for x in range(self.nr):
                for y in range(self.nc):
                    if output.ColonneList[y][x] != self.ColonneList[y][x]:
                        if output.ColonneList[y][x] == 0 or self.ColonneList[y][x] == 0:
                            score += 1
                        else:
                            score += abs(int(self.ColonneList[y][x]) - int(output.ColonneList[y][x]))/10
        elif self.nr > output.nr and self.nc > output.nc:
            for x in range(output.nr):
                for y in range(output.nc):
                    if output.ColonneList[y][x] != self.ColonneList[y][x]:
                        if output.ColonneList[y][x] == 0 or self.ColonneList[y][x] == 0:
                            score += 1
                        else:
                            score += abs(int(self.ColonneList[y][x]) - int(output.ColonneList[y][x]))/10
        elif self.nr <= output.nr and self.nc > output.nc:
            for x in range(self.nr):
                for y in range(output.nc):
                    if output.ColonneList[y][x] != self.ColonneList[y][x]:
                        if output.ColonneList[y][x] == 0 or self.ColonneList[y][x] == 0:
                            score += 1
                        else:
                            score += abs(int(self.ColonneList[y][x]) - int(output.ColonneList[y][x]))/10
        elif self.nr > output.nr and self.nc <= output.nc:
            for x in range(output.nr):
                for y in range(self.nc):
                    if output.ColonneList[y][x] != self.ColonneList[y][x]:
                        if output.ColonneList[y][x] == 0 or self.ColonneList[y][x] == 0:
                            score += 1
                        else:
                            score += abs(int(self.ColonneList[y][x]) - int(output.ColonneList[y][x]))/10
        return -score

    #transform the representation into an ARC grid
    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for x in range(0, self.nr):
            for y in range(0, self.nc):
                grid[x][y] = self.ColonneList[y][x]
        return grid
    
    #function that calculates a score based on the selectors used
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_selection[x].allElement < 3: 
                score += 0.5
            if performed_actions[x] == columnsRepresentation.changeColorColumnPixel or performed_actions[x] == columnsRepresentation.modifyColumnAdd or performed_actions[x] == columnsRepresentation.modifyColumnDel or performed_actions[x] == columnsRepresentation.modifyColumnMove:
                score += 0.5
            score += 1
        return -score
    
    #return the list of actions
    def actionList(pc):     
        l = [columnsRepresentation.moveColumn, columnsRepresentation.modifyColumnMove]
        if pc.countDim != pc.numProb:
            l.append(columnsRepresentation.expandGrid)
            l.append(columnsRepresentation.reduceGrid)
        if pc.countColor != pc.numProb:
            l.append(columnsRepresentation.changeColorColumn)
            l.append(columnsRepresentation.changeColorColumnPixel)
        if pc.countRemove > 0:
            l.append(columnsRepresentation.modifyColumnDel)
        if pc.countAdd > 0:
            l.append(columnsRepresentation.modifyColumnAdd)
        return l
    
    #return the list of base actions
    def baseActionList(pc):
        l = [columnsRepresentation.moveColumn]
        if pc.countColor != pc.numProb:
            l.append(columnsRepresentation.changeColorColumn)
        if pc.countDim != pc.numProb:
            l.append(columnsRepresentation.expandGrid)
            l.append(columnsRepresentation.reduceGrid)
        return l