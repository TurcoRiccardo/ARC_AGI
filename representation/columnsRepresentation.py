import numpy as np
import copy


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

    def getNElement(self):
        return self.nc

    def moveColonna(self, index, color, direction):
        adapted_index = index % self.nc
        if (direction % 4) == 0:
            #scalo la colonna verso l'alto
            new_colonna = list()
            for x in range(1, self.nr):
                new_colonna.append(self.ColonneList[adapted_index][x])
            new_colonna.append(self.ColonneList[adapted_index][0])
            self.ColonneList[adapted_index] = new_colonna
        elif (direction % 4) == 1:
            #scalo la colonna verso il basso
            new_colonna = list()
            new_colonna.append(self.ColonneList[adapted_index][self.nr-1])
            for x in range(0, self.nr-1):
                new_colonna.append(self.ColonneList[adapted_index][x])
            self.ColonneList[adapted_index] = new_colonna
        elif (direction % 4) == 2:
            #sposto la colonna a destra
            if adapted_index + 1 < self.nc:
                colonnaDestra = self.ColonneList[adapted_index + 1]
                self.ColonneList[adapted_index + 1] = self.ColonneList[adapted_index]
                self.ColonneList[adapted_index] = colonnaDestra
        elif (direction % 4) == 3:
            #sposto la colonna a sinista
            if adapted_index > 0:
                colonnaDestra = self.ColonneList[adapted_index]
                self.ColonneList[adapted_index] = self.ColonneList[adapted_index - 1]
                self.ColonneList[adapted_index - 1] = colonnaDestra
    
    def expandGrid(self, index, color, direction):
        adapted_index = index % self.nc
        if (direction % 4) == 0:
            #down
            self.nr += 1
            for x in range(0, self.nc):
                self.ColonneList[x].append(0)
        elif (direction % 4) == 1:
            #up
            self.nr += 1
            for x in range(0, self.nc):
                new_Colonna = list()
                new_Colonna.append(0)
                for element in self.ColonneList[x]:
                    new_Colonna.append(element)
                self.ColonneList[x] = new_Colonna
        elif (direction % 4) == 2:
            #right
            self.nc += 1
            new_Colonna = copy.deepcopy(self.ColonneList[adapted_index])
            self.ColonneList.append(new_Colonna)
        elif (direction % 4) == 3:
            #left
            self.nc += 1
            new_Colonna = copy.deepcopy(self.ColonneList[adapted_index])
            new_ColonneList = [new_Colonna]
            for colonna in self.ColonneList:
                new_ColonneList.append(colonna)
            self.ColonneList = new_ColonneList

    def reduceGrid(self, index, color, direction):
        if (direction % 4) == 0:
            #down
            if self.nr > 1:
                self.nr -= 1
                for colonna in self.ColonneList:
                    colonna.pop()
        elif (direction % 4) == 1:
            #up
            if self.nr > 1:
                self.nr -= 1
                for colonna in self.ColonneList:
                    colonna.pop(0)
        elif (direction % 4) == 2:
            #right
            if self.nc > 1:
                self.nc -= 1
                self.ColonneList.pop()
        elif (direction % 4) == 3:
            #left
            if self.nc > 1:
                self.nc -= 1
                self.ColonneList.pop(0)

    def changeColorColonna(self, index, color, direction):
        adapted_index = index % self.nc
        for element in self.ColonneList[adapted_index]:
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

    def modifyColonnaAdd(self, index, color, direction):
        adapted_index = index % self.nc
        valid_position = list()
        color = 0
        for x in range(0, self.nr):
            if self.ColonneList[adapted_index][x] == 0:
                valid_position.append(x)
            else:
                color = self.ColonneList[adapted_index][x]
        if len(valid_position) != 0:
            self.ColonneList[adapted_index][valid_position[direction % len(valid_position)]] = color

    def modifyColonnaDel(self, index, color, direction):
        adapted_index = index % self.nc
        if sum(self.ColonneList[adapted_index]) > 0:
            valid_position = list()
            for x in range(0, self.nr):
                if self.ColonneList[adapted_index][x] != 0:
                    valid_position.append(x)
            self.ColonneList[adapted_index][valid_position[direction % len(valid_position)]] = 0

    def modifyColonnaMove(self, index, color, direction):
        adapted_index = index % self.nc
        adapted_pos = direction % self.nr
        if adapted_pos == 0:
            tmp = self.ColonneList[adapted_index][self.nr - 1]
            self.ColonneList[adapted_index][self.nr - 1] = self.ColonneList[adapted_index][adapted_pos]
            self.ColonneList[adapted_index][adapted_pos] = tmp
        else:
            tmp = self.ColonneList[adapted_index][adapted_pos - 1]
            self.ColonneList[adapted_index][adapted_pos - 1] = self.ColonneList[adapted_index][adapted_pos]
            self.ColonneList[adapted_index][adapted_pos] = tmp
    
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