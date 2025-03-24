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
        return self.nr

    #moves the column index if possible based on the direction
    def moveColonna(self, s):
        l = list()
        count = 0
        if s.allElement == 1:
            l = [y for y in range(0, self.nc)]
        elif s.allElement == 2:
            for y in range(0, self.nc):
                color = 0
                for p in self.ColonneList[y]:
                    if p != 0:
                        color = p
                if color == s.color:
                    l.append(y)
        else:
            l.append(s.index % self.nc)
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

    #changes the color of the colored pixel in the column index based on color
    def changeColorColonna(self, s):
        l = list()
        count = 0
        if s.allElement == 1:
            l = [y for y in range(0, self.nc)]
        elif s.allElement == 2:
            for y in range(0, self.nc):
                color = 0
                for p in self.ColonneList[y]:
                    if p != 0:
                        color = p
                if color == s.color:
                    l.append(y)
        else:
            l.append(s.index % self.nc)
        for adapted_index in l:
            for element in self.ColonneList[adapted_index]:
                if element != 0:
                    if s.color % 2 == 0:
                        if element != 9:
                            element += 1
                            count += 1
                    else:
                        if element != 1:
                            element -= 1
                            count += 1
        if count != 0:
            return 0
        return 1

    #add a new colored pixel in the column index
    def modifyColonnaAdd(self, s):
        l = list()
        count = 0
        if s.allElement == 1:
            l = [y for y in range(0, self.nc)]
        elif s.allElement == 2:
            for y in range(0, self.nc):
                color = 0
                for p in self.ColonneList[y]:
                    if p != 0:
                        color = p
                if color == s.color:
                    l.append(y)
        else:
            l.append(s.index % self.nc)
        adapted_component = s.component % self.nr
        for adapted_index in l:
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
    def modifyColonnaDel(self, s):
        l = list()
        count = 0
        if s.allElement == 1:
            l = [y for y in range(0, self.nc)]
        elif s.allElement == 2:
            for y in range(0, self.nc):
                color = 0
                for p in self.ColonneList[y]:
                    if p != 0:
                        color = p
                if color == s.color:
                    l.append(y)
        else:
            l.append(s.index % self.nc)
        adapted_component = s.component % self.nr
        for adapted_index in l:
            if self.ColonneList[adapted_index][adapted_component] != 0:
                self.ColonneList[adapted_index][adapted_component] == 0
                count += 1
        if count != 0:
            return 0
        return 1

    #swap two pixel based on direction in the row index
    def modifyColonnaMove(self, s):
        l = list()
        count = 0
        if s.allElement == 1:
            l = [y for y in range(0, self.nc)]
        elif s.allElement == 2:
            for y in range(0, self.nc):
                color = 0
                for p in self.ColonneList[y]:
                    if p != 0:
                        color = p
                if color == s.color:
                    l.append(y)
        else:
            l.append(s.index % self.nc)
        adapted_component = s.component % self.nr
        for adapted_index in l:
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

    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for x in range(0, self.nr):
            for y in range(0, self.nc):
                grid[x][y] = self.ColonneList[y][x]
        return grid
    
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_actions[x] == columnsRepresentation.modifyColonnaAdd:
                score += 0.7
            elif performed_actions[x] == columnsRepresentation.modifyColonnaDel:
                score += 0.7
            elif performed_selection[x].allElement == 0 and performed_actions[x] != columnsRepresentation.reduceGrid and  performed_actions[x] != columnsRepresentation.expandGrid:
                score += 0.5
            score += 1
        return -score