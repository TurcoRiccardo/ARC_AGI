import numpy as np
from dataclasses import dataclass
from selection.selector import Selector

#la diagonale che va dal vertice in alto a sinistra al vertice in basso a destra
# 1 2 3
# 4 5 6
#
# 3
# 2 6
# 1 5
# 4
class firstDiagonalRepresentation:
    def __init__(self, input_grid):
        self.nr = input_grid.shape[0]
        self.nc = input_grid.shape[1]
        self.DiagonaleList = list()
        # Diagonali che partono dalla prima riga
        for col in range(self.nc):
            i = 0
            j = col
            diag = []
            while i < self.nr and j < self.nc:
                diag.append(input_grid[i][j])
                i += 1
                j += 1
            self.DiagonaleList.append(diag)
        self.DiagonaleList = self.DiagonaleList[::-1]
        # Diagonali che partono dalla prima colonna, escludendo la prima riga
        for row in range(1, self.nr):
            i = row
            j = 0
            diag = []
            while i < self.nr and j < self.nc:
                diag.append(input_grid[i][j])
                i += 1
                j += 1
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
                for x in range(0, len(self.DiagonaleList) - 1):
                    if len(self.DiagonaleList[x + 1]) >= max:
                        max = len(self.DiagonaleList[x + 1])
                        if x < self.nr - 1:
                            self.DiagonaleList[x].append(0)
                self.DiagonaleList.insert(0, [0])
                return 0
        elif (s.direction % 4) == 3:
            #left
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
        elif (s.direction % 4) == 3:
            #left
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
        return 1
    
    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        for i in range(0, min(len(self.DiagonaleList), len(output.DiagonaleList))):
            for c in range(0, min(len(self.DiagonaleList[i]), len(output.DiagonaleList[i]))):
                if self.DiagonaleList[i][c] == 0 or output.DiagonaleList[i][c] == 0:
                    score += 1
                else:
                    score += abs(int(self.DiagonaleList[i][c]) - int(output.DiagonaleList[i][c]))/10
        return -score

    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        col = self.nc - 1
        max = 0
        m = 1
        for diag in self.DiagonaleList:
            if len(diag) <= max:
                if col >= 0:
                    x = 0
                    y = col
                else:
                    x = m
                    y = 0
                for p in diag:
                    grid[x][y] = p
                    x += 1
                    y += 1
                if col > 0:
                    col -= 1
                else:
                    m += 1
            else:
                max = len(diag)
                x = 0
                y = col
                for p in diag:
                    grid[x][y] = p
                    x += 1
                    y += 1
                col -= 1
        return grid
    
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_selection[x].allElement < 3: 
                score += 0.5
            #if performed_actions[x] == firstDiagonalRepresentation.modifyRowAdd or performed_actions[x] == firstDiagonalRepresentation.modifyRowDel:
            #    score += 0.5
            score += 1
        return -score
