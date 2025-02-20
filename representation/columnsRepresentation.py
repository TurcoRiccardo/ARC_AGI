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
                element = (element + color) % 10

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
    
    def score(self, output_grid):
        #-2 punti per posizione non giusta, -1 punto per colore sbagliato, -3 punti dimensione griglia sbagliata per casella
        score = 0
        if self.nr <= output_grid.shape[0] and self.nc <= output_grid.shape[1]:
            for x in range(self.nr):
                for y in range(self.nc):
                    if output_grid[x][y] != self.ColonneList[y][x]:
                        score += 1
                        if output_grid[x][y] == 0 or self.ColonneList[y][x] == 0:
                            score += 1
        elif self.nr > output_grid.shape[0] and self.nc > output_grid.shape[1]:
            for x in range(output_grid.shape[0]):
                for y in range(output_grid.shape[1]):
                    if output_grid[x][y] != self.ColonneList[y][x]:
                        score += 1
                        if output_grid[x][y] == 0 or self.ColonneList[y][x] == 0:
                            score += 1
        elif self.nr <= output_grid.shape[0] and self.nc > output_grid.shape[1]:
            for x in range(self.nr):
                for y in range(output_grid.shape[1]):
                    if output_grid[x][y] != self.ColonneList[y][x]:
                        score += 1
                        if output_grid[x][y] == 0 or self.ColonneList[y][x] == 0:
                            score += 1
        elif self.nr > output_grid.shape[0] and self.nc <= output_grid.shape[1]:
            for x in range(output_grid.shape[0]):
                for y in range(self.nc):
                    if output_grid[x][y] != self.ColonneList[y][x]:
                        score += 1
                        if output_grid[x][y] == 0 or self.ColonneList[y][x] == 0:
                            score += 1
        else:
            return -100
        score += abs(output_grid.shape[0] - self.nr)*min(self.nc, output_grid.shape[1])*3 + abs(output_grid.shape[1] - self.nc)*min(self.nr, output_grid.shape[0])*3 + abs(output_grid.shape[0] - self.nr)*abs(output_grid.shape[1] - self.nc)*3
        return -score

    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for x in range(0, self.nr):
            for y in range(0, self.nc):
                grid[x][y] = self.ColonneList[y][x]
        return grid