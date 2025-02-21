import numpy as np
import copy


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

    def getNElement(self):
        return self.nr

    def moveRiga(self, index, color, direction):
        adapted_index = index % self.nr
        if (direction % 4) == 0:
            #sposto riga sopra
            if adapted_index > 0:
                rigaSopra = self.RigheList[adapted_index - 1]
                self.RigheList[adapted_index - 1] = self.RigheList[adapted_index]
                self.RigheList[adapted_index] = rigaSopra
        elif (direction % 4) == 1:
            #sposto riga sotto
            if adapted_index + 1 < self.nr:
                rigaSopra = self.RigheList[adapted_index]
                self.RigheList[adapted_index] = self.RigheList[adapted_index + 1]
                self.RigheList[adapted_index + 1] = rigaSopra
        elif (direction % 4) == 2:
            #scalo la riga verso destra
            new_riga = list()
            new_riga.append(self.RigheList[adapted_index][self.nc-1])
            for x in range(0, self.nc-1):
                new_riga.append(self.RigheList[adapted_index][x])
            self.RigheList[adapted_index] = new_riga
        elif (direction % 4) == 3:
            #scalo la riga verso sinistra
            new_riga = list()
            for x in range(1, self.nc):
                new_riga.append(self.RigheList[adapted_index][x])
            new_riga.append(self.RigheList[adapted_index][0])
            self.RigheList[adapted_index] = new_riga

    def expandGrid(self, index, color, direction):
        adapted_index = index % self.nr
        if (direction % 4) == 0:
            #down
            self.nr += 1
            new_Riga = copy.deepcopy(self.RigheList[adapted_index])
            self.RigheList.append(new_Riga) 
        elif (direction % 4) == 1:
            #up
            self.nr += 1
            new_Riga = copy.deepcopy(self.RigheList[adapted_index])
            new_RigheList = [new_Riga]
            for riga in self.RigheList:
                new_RigheList.append(riga)
            self.RigheList = new_RigheList
        elif (direction % 4) == 2:
            #right
            self.nc += 1
            for x in range(0, self.nr):
                self.RigheList[x].append(0)
        elif (direction % 4) == 3:
            #left
            self.nc += 1
            for x in range(0, self.nr):
                new_riga = list()
                new_riga.append(0)
                for element in self.RigheList[x]:
                    new_riga.append(element)
                self.RigheList[x] = new_riga

    def reduceGrid(self, index, color, direction):
        if (direction % 4) == 0:
            #down
            if self.nr > 1:
                self.nr -= 1
                self.RigheList.pop()
        elif (direction % 4) == 1:
            #up
            if self.nr > 1:
                self.nr -= 1
                self.RigheList.pop(0)
        elif (direction % 4) == 2:
            #right
            if self.nc > 1:
                self.nc -= 1
                for riga in self.RigheList:
                    riga.pop()
        elif (direction % 4) == 3:
            #left
            if self.nc > 1:
                self.nc -= 1
                for riga in self.RigheList:
                    riga.pop(0)

    def changeColorRiga(self, index, color, direction):
        adapted_index = index % self.nr
        for element in self.RigheList[adapted_index]:
            if element != 0:
                if color % 2 == 0:
                    if element == 9:
                        element = 1
                    else:
                        element += 1
                else:
                    if element == 1:
                        element = 9
                    else:
                        element -= 1

    def modifyRigaAdd(self, index, color, direction):
        adapted_index = index % self.nr
        valid_position = list()
        color = 0
        for x in range(0, self.nc):
            if self.RigheList[adapted_index][x] == 0:
                valid_position.append(x)
            else:
                color = self.RigheList[adapted_index][x]
        if len(valid_position) != 0:
            self.RigheList[adapted_index][valid_position[direction % len(valid_position)]] = color
        
    def modifyRigaDel(self, index, color, direction):
        adapted_index = index % self.nr
        if sum(self.RigheList[adapted_index]) > 0:
            valid_position = list()
            for x in range(0, self.nc):
                if self.RigheList[adapted_index][x] != 0:
                    valid_position.append(x)
            self.RigheList[adapted_index][valid_position[direction % len(valid_position)]] = 0
    
    def modifyRigaMove(self, index, color, direction):
        adapted_index = index % self.nr
        adapted_pos = direction % self.nc
        if adapted_pos == 0:
            tmp = self.RigheList[adapted_index][self.nc - 1]
            self.RigheList[adapted_index][self.nc - 1] = self.RigheList[adapted_index][adapted_pos]
            self.RigheList[adapted_index][adapted_pos] = tmp
        else:
            tmp = self.RigheList[adapted_index][adapted_pos - 1]
            self.RigheList[adapted_index][adapted_pos - 1] = self.RigheList[adapted_index][adapted_pos]
            self.RigheList[adapted_index][adapted_pos] = tmp

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