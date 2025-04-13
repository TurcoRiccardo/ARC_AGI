import numpy as np
from dataclasses import dataclass
from selection.selector import Selector

#diagonale che va dal vertice in alto a destra al vertice in basso a sinistra
# 1 2 3
# 4 5 6
#
# 1
# 2 4
# 3 5
# 6
class secondDiagonalRepresentation:
    def __init__(self, input_grid):
        self.nr = input_grid.shape[0]
        self.nc = input_grid.shape[1]
        self.DiagonaleList = list()
        col = 0
        m = 1
        for d in range(0, self.nr + self.nc - 1):
            diag = []
            if d < self.nc:
                x = 0
                y = col
                while x < self.nr and y >= 0:
                    diag.append(input_grid[x][y])
                    x += 1
                    y -= 1
                col += 1
            else:
                x = m
                y = self.nc - 1
                while x < self.nr and y >= 0:
                    diag.append(input_grid[x][y])
                    x += 1
                    y -= 1
                m += 1
            self.DiagonaleList.append(diag)
    
    #return the total number of diagonal
    def getNElement(self):
        return len(self.DiagonaleList)
    
    #return the total number of element in the diagonal
    def getElementComponent(self, index):
        return len(self.DiagonaleList[index])

    #return the list of diagonal index
    def generateIndexList(self, s):
        l = list()
        if s.allElement == 1:
            #sotto
            l.append(len(self.DiagonaleList) - (s.index % len(self.DiagonaleList)) - 1)
        elif s.allElement == 2:
            #centro
            if len(self.DiagonaleList) % 2 == 1:
                l.append(len(self.DiagonaleList) // 2)
            else:
                l.append(len(self.DiagonaleList) // 2 - 1)
                l.append(len(self.DiagonaleList) // 2)
        elif s.allElement == 3:
            #all the row
            l = [x for x in range(0, len(self.DiagonaleList))]
        elif s.allElement == 4:
            #the row need to contain a crtaint color
            for x in range(0, len(self.DiagonaleList)):
                ok = 0
                for p in self.DiagonaleList[x]:
                    if p == s.color:
                        ok = 1
                if ok == 1:
                    l.append(x)
        else:
            #sopra
            l.append(s.index % len(self.DiagonaleList))
        return l
    
    #return the list of component index
    def generateComponentList(self, s, adapted_index):
        l = list()
        if s.allComponent == 1:
            #da destra
            l.append(len(self.DiagonaleList[adapted_index]) - (s.component % len(self.DiagonaleList[adapted_index])) - 1)
        elif s.allComponent == 2:
            #centro
            if len(self.DiagonaleList[adapted_index]) % 2 == 1:
                l.append(len(self.DiagonaleList[adapted_index])// 2)
            else:
                l.append(len(self.DiagonaleList[adapted_index]) // 2 - 1)
                l.append(len(self.DiagonaleList[adapted_index]) // 2)
        elif s.allComponent == 3:
            #all
            l = [x for x in range(0, len(self.DiagonaleList[adapted_index]))]
        elif s.allComponent == 4:
            #component of the selected color
            for c, p in enumerate(self.DiagonaleList[adapted_index]):
                if p == s.color:
                    l.append(c)
        else:
            #da sinistra
            l.append(s.component % len(self.DiagonaleList[adapted_index]))
        return l

    #moves the diagonal index if possible based on the direction
    def moveDiagonal(self, s):
        count = 0
        l = self.generateIndexList(s)
        if (s.direction % 4) == 2:
            l.sort(key=lambda i: i, reverse=True)
        elif (s.direction % 4) == 3:
            l.sort(key=lambda i: i, reverse=False)
        if len(l) == len(self.DiagonaleList):
            l.pop(-1)
        for adapted_index in l:
            if (s.direction % 4) == 0:
                #scalo diagonale sotto
                new_diagonale = list()
                new_diagonale.append(self.DiagonaleList[adapted_index][-1])
                for x in range(0, len(self.DiagonaleList[adapted_index])-1):
                    new_diagonale.append(self.DiagonaleList[adapted_index][x])
                self.DiagonaleList[adapted_index] = new_diagonale
                count += 1
            elif (s.direction % 4) == 1:
                #scalo diagonale sopra
                new_diagonale = list()
                for x in range(1, len(self.DiagonaleList[adapted_index])):
                    new_diagonale.append(self.DiagonaleList[adapted_index][x])
                new_diagonale.append(self.DiagonaleList[adapted_index][0])
                self.DiagonaleList[adapted_index] = new_diagonale
                count += 1
            elif (s.direction % 4) == 2:
                #sposto la diagonale verso destra
                if adapted_index + 1 < len(self.DiagonaleList):
                    if len(self.DiagonaleList[adapted_index]) > len(self.DiagonaleList[adapted_index + 1]):
                        diagonaleSinistra = self.DiagonaleList[adapted_index][:-1]
                        color = 0
                        for p in self.DiagonaleList[adapted_index + 1]:
                            if p != 0:
                                color = p
                        self.DiagonaleList[adapted_index + 1].append(color)
                        self.DiagonaleList[adapted_index] = self.DiagonaleList[adapted_index + 1]
                        self.DiagonaleList[adapted_index + 1] = diagonaleSinistra
                    elif len(self.DiagonaleList[adapted_index]) < len(self.DiagonaleList[adapted_index + 1]):
                        color = 0
                        for p in self.DiagonaleList[adapted_index]:
                            if p != 0:
                                color = p
                        self.DiagonaleList[adapted_index].append(color)
                        diagonaleSinistra = self.DiagonaleList[adapted_index]
                        self.DiagonaleList[adapted_index] = self.DiagonaleList[adapted_index + 1][:-1]
                        self.DiagonaleList[adapted_index + 1] = diagonaleSinistra
                    else:
                        diagonaleSinistra = self.DiagonaleList[adapted_index]
                        self.DiagonaleList[adapted_index] = self.DiagonaleList[adapted_index + 1]
                        self.DiagonaleList[adapted_index + 1] = diagonaleSinistra
                    count += 1
                elif adapted_index + 1 == len(self.DiagonaleList):
                    diagonaleSinistra = self.DiagonaleList[0]
                    self.DiagonaleList[0] = self.DiagonaleList[adapted_index]
                    self.DiagonaleList[adapted_index] = diagonaleSinistra
                    count += 1
            elif (s.direction % 4) == 3:
                #sposto la diagonale verso sinistra
                if adapted_index > 0:
                    if len(self.DiagonaleList[adapted_index]) > len(self.DiagonaleList[adapted_index - 1]):
                        color = 0
                        for p in self.DiagonaleList[adapted_index - 1]:
                            if p != 0:
                                color = p
                        self.DiagonaleList[adapted_index - 1].append(color)
                        diagonaleSinistra = self.DiagonaleList[adapted_index - 1]
                        self.DiagonaleList[adapted_index - 1] = self.DiagonaleList[adapted_index][:-1]
                        self.DiagonaleList[adapted_index] = diagonaleSinistra
                    elif len(self.DiagonaleList[adapted_index]) < len(self.DiagonaleList[adapted_index - 1]):
                        diagonaleSinistra = self.DiagonaleList[adapted_index - 1][:-1]
                        color = 0
                        for p in self.DiagonaleList[adapted_index]:
                            if p != 0:
                                color = p
                        self.DiagonaleList[adapted_index].append(color)
                        self.DiagonaleList[adapted_index - 1] = self.DiagonaleList[adapted_index]
                        self.DiagonaleList[adapted_index] = diagonaleSinistra
                    else:
                        diagonaleSinistra = self.DiagonaleList[adapted_index - 1]
                        self.DiagonaleList[adapted_index - 1] = self.DiagonaleList[adapted_index]
                        self.DiagonaleList[adapted_index] = diagonaleSinistra
                    count += 1
                elif adapted_index == 0:
                    diagonaleSinistra = self.DiagonaleList[-1]
                    self.DiagonaleList[-1] = self.DiagonaleList[adapted_index]
                    self.DiagonaleList[adapted_index] = diagonaleSinistra
                    count += 1
        if count != 0:
            return 0
        return 1
    
    #changes the color of the colored pixel in the diagonal index based on color
    def changeColorDiagonal(self, s):
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            for y in range(0, len(self.DiagonaleList[adapted_index])):
                if self.DiagonaleList[adapted_index][y] != 0:
                    if s.color % 2 == 0:
                        if self.DiagonaleList[adapted_index][y] != 9:
                            self.DiagonaleList[adapted_index][y] += 1
                            count += 1
                    else:
                        if self.DiagonaleList[adapted_index][y] != 1:
                            self.DiagonaleList[adapted_index][y] -= 1
                            count += 1
        if count != 0:
            return 0
        return 1
    
    #add a new colored pixel in the diagonal index
    def modifyDiagonalAdd(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            for adapted_component in lc:
                if self.DiagonaleList[adapted_index][adapted_component] == 0:
                    color = 1
                    for p in self.DiagonaleList[adapted_index]:
                        if p != 0:
                            color = p
                            break
                    self.DiagonaleList[adapted_index][adapted_component] == color
                    count += 1
        if count != 0:
            return 0
        return 1
    
    #delete a colored pixel in the diagonal index
    def modifyDiagonalDel(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            for adapted_component in lc:
                if self.DiagonaleList[adapted_index][adapted_component] != 0:
                    self.DiagonaleList[adapted_index][adapted_component] == 0
                    count += 1
        if count != 0:
            return 0
        return 1
    
    #swap two pixel based on direction in the row index
    def modifyDiagonalMove(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            lc = self.generateComponentList(s, adapted_index)
            if (s.direction % 2) == 0:
                lc.sort(key=lambda i: i, reverse=True)
            elif (s.direction % 2) == 1:
                lc.sort(key=lambda i: i, reverse=False)
            if len(lc) == len(self.DiagonaleList[adapted_index]):
                lc.pop(-1)
            for adapted_component in lc:
                if (s.direction % 2) == 0:
                    #swappo andando verso destra
                    if adapted_component + 1 < len(self.DiagonaleList[adapted_index]):
                        tmp = self.DiagonaleList[adapted_index][adapted_component + 1]
                        self.DiagonaleList[adapted_index][adapted_component + 1] = self.DiagonaleList[adapted_index][adapted_component]
                        self.DiagonaleList[adapted_index][adapted_component] = tmp
                        count += 1
                    elif adapted_component + 1 == len(self.DiagonaleList[adapted_index]):
                        tmp = self.DiagonaleList[adapted_index][0]
                        self.DiagonaleList[adapted_index][0] = self.DiagonaleList[adapted_index][adapted_component]
                        self.DiagonaleList[adapted_index][adapted_component] = tmp
                        count += 1
                elif (s.direction % 2) == 1:
                    #swappo andando verso sinistra
                    if adapted_component - 1 >= 0:
                        tmp = self.DiagonaleList[adapted_index][adapted_component - 1]
                        self.DiagonaleList[adapted_index][adapted_component - 1] = self.DiagonaleList[adapted_index][adapted_component]
                        self.DiagonaleList[adapted_index][adapted_component] = tmp
                        count += 1 
                    elif adapted_component == 0:
                        tmp = self.DiagonaleList[adapted_index][-1]
                        self.DiagonaleList[adapted_index][-1] = self.DiagonaleList[adapted_index][adapted_component]
                        self.DiagonaleList[adapted_index][adapted_component] = tmp
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
                max = 0
                self.DiagonaleList.append([0])
                for x in range(0, len(self.DiagonaleList) - 1):
                    if len(self.DiagonaleList[x + 1]) <= max:
                        if x >= len(self.DiagonaleList) - self.nc:
                            self.DiagonaleList[x].append(0)
                    else:
                        max = len(self.DiagonaleList[x + 1])
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr < 30:
                self.nr += 1
                max = 0
                for x in range(0, len(self.DiagonaleList) - 1):
                    if len(self.DiagonaleList[x + 1]) >= max:
                        max = len(self.DiagonaleList[x + 1])
                        if x < self.nc - 1:
                            self.DiagonaleList[x].insert(0, 0)
                self.DiagonaleList.insert(0, [0])
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc < 30:
                self.nc += 1
                max = 0
                self.DiagonaleList.append([0])
                for x in range(0, len(self.DiagonaleList) - 1):
                    if len(self.DiagonaleList[x + 1]) <= max:
                        if x >= len(self.DiagonaleList) - self.nr:
                            self.DiagonaleList[x].insert(0, 0)
                    else:
                        max = len(self.DiagonaleList[x + 1])
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc < 30:
                self.nc += 1
                max = 0
                for x in range(0, len(self.DiagonaleList) - 1):
                    if len(self.DiagonaleList[x + 1]) >= max:
                        max = len(self.DiagonaleList[x + 1])
                        if x < self.nr - 1:
                            self.DiagonaleList[x].append(0)
                self.DiagonaleList.insert(0, [0])
                return 0
        return 1

    #reduce the grid in the direction direction
    def reduceGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            if self.nr > 1:
                self.nr -= 1
                max = 0
                for x in range(0, len(self.DiagonaleList) - 1):
                    if len(self.DiagonaleList[x + 1]) <= max:
                        if x > self.nr - 1:
                            self.DiagonaleList[x].pop(-1)
                    else:
                        max = len(self.DiagonaleList[x + 1])
                self.DiagonaleList.pop(-1)
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr > 1:
                self.nr -= 1
                max = 0
                self.DiagonaleList.pop(0)
                for x in range(0, len(self.DiagonaleList) - 1):
                    if len(self.DiagonaleList[x + 1]) >= max:
                        max = len(self.DiagonaleList[x + 1])
                        if x < self.nc - 1:
                            self.DiagonaleList[x].pop(0)
                    elif len(self.DiagonaleList[x]) == max:
                        if x < self.nc - 1:
                            self.DiagonaleList[x].pop(0)
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc > 1:
                self.nc -= 1
                max = 0
                for x in range(0, len(self.DiagonaleList) - 1):
                    if len(self.DiagonaleList[x + 1]) <= max:
                        if x > self.nc - 1:
                            self.DiagonaleList[x].pop(0)
                    else:
                        max = len(self.DiagonaleList[x + 1])
                self.DiagonaleList.pop(-1)
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc > 1:
                self.nc -= 1
                max = 0
                self.DiagonaleList.pop(0)
                for x in range(0, len(self.DiagonaleList) - 1):
                    if len(self.DiagonaleList[x + 1]) >= max:
                        max = len(self.DiagonaleList[x + 1])
                        if x < self.nr - 1:
                            self.DiagonaleList[x].pop(-1)
                    elif len(self.DiagonaleList[x]) == max:
                        if x < self.nr - 1:
                            self.DiagonaleList[x].pop(-1)
                return 0
        return 1

    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        for i in range(0, min(len(self.DiagonaleList), len(output.DiagonaleList))):
            for c in range(0, min(len(self.DiagonaleList[i]), len(output.DiagonaleList[i]))):
                if self.DiagonaleList[i][c] != output.DiagonaleList[i][c]:
                    if self.DiagonaleList[i][c] == 0 or output.DiagonaleList[i][c] == 0:
                        score += 1
                    else:
                        score += abs(int(self.DiagonaleList[i][c]) - int(output.DiagonaleList[i][c]))/10
        return -score

    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        col = 0
        m = 1
        for c, diag in enumerate(self.DiagonaleList):
            if c < self.nc:
                x = 0
                y = col
                for p in diag:
                    grid[x][y] = p
                    x += 1
                    y -= 1
                col += 1
            else:
                x = m
                y = self.nc - 1
                for p in diag:
                    grid[x][y] = p
                    x += 1
                    y -= 1
                m += 1
        return grid
    
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_selection[x].allElement < 3: 
                score += 0.5
            if performed_actions[x] == secondDiagonalRepresentation.modifyDiagonalAdd or performed_actions[x] == secondDiagonalRepresentation.modifyDiagonalDel or performed_actions[x] == secondDiagonalRepresentation.reduceGrid or performed_actions[x] == secondDiagonalRepresentation.expandGrid:
                score += 0.5
            score += 1
        return -score