import numpy as np
from dataclasses import dataclass


@dataclass
class PixelNode:
    x: int
    y: int
    color: int = 0

class colorLayerRepresentation:
    def __init__(self, input_grid):
        self.nr = input_grid.shape[0]
        self.nc = input_grid.shape[1]
        self.FigureListLayer = list()
        for c in range(1, 10):
            figure = list()
            for x in range(self.nr):
                for y in range(self.nc):
                    if input_grid[x][y] == c:
                        figure.append(PixelNode(x, y))
            self.FigureListLayer.append(figure)

    def getNElement(self):
        return 9

    def moveLayer(self, index, color, direction):
        adapted_index = index % 9
        if len(self.FigureListLayer[adapted_index]) == 0:
            return
        new_figure = list()
        if (direction % 4) == 0:
            #down
            for pixel in self.FigureListLayer[adapted_index]:
                if pixel.x + 1 < self.nr:
                    new_figure.append(PixelNode(pixel.x+1, pixel.y))
                elif pixel.x + 1 == self.nr:
                    new_figure.append(PixelNode(0, pixel.y))
        elif (direction % 4) == 1:
            #up
            for pixel in self.FigureListLayer[adapted_index]:
                if pixel.x > 0:
                    new_figure.append(PixelNode(pixel.x-1, pixel.y))
                elif pixel.x == 0:
                    new_figure.append(PixelNode(self.nr-1, pixel.y))
        elif (direction % 4) == 2:
            #right
            for pixel in self.FigureListLayer[adapted_index]:
                if pixel.y + 1 < self.nc:
                    new_figure.append(PixelNode(pixel.x, pixel.y+1))
                elif pixel.y + 1 == self.nc:
                    new_figure.append(PixelNode(pixel.x, 0))
        elif (direction % 4) == 3:
            #left
            for pixel in self.FigureListLayer[adapted_index]:
                if pixel.y > 0:
                    new_figure.append(PixelNode(pixel.x, pixel.y-1))
                elif pixel.y == 0:
                    new_figure.append(PixelNode(pixel.x, self.nc-1))
        self.FigureListLayer[adapted_index] = new_figure

    def expandGrid(self, index, color, direction):
        if (direction % 4) == 0:
            #down
            self.nr += 1
        elif (direction % 4) == 1:
            #up
            self.nr += 1
            for layer in self.FigureListLayer:
                for pixel in layer:
                    pixel.x += 1
        elif (direction % 4) == 2:
            #right
            self.nc += 1
        elif (direction % 4) == 3:
            #left
            self.nc += 1
            for layer in self.FigureListLayer:
                for pixel in layer:
                    pixel.y += 1

    def reduceGrid(self, index, color, direction):
        if (direction % 4) == 0:
            #down
            self.nr -= 1
            for layer in self.FigureListLayer:
                remove = list()
                for x in range(0, len(layer)):
                    if layer[x].x == self.nr:
                        remove.append(x)
                remove.sort(reverse = True)
                for x in remove:
                    layer.pop(x)
        elif (direction % 4) == 1:
            #up
            self.nr -= 1
            for layer in self.FigureListLayer:
                remove = list()
                for x in range(0, len(layer)):
                    if layer[x].x == 0:
                        remove.append(x)
                    else:
                        layer[x].x -= 1
                remove.sort(reverse = True)
                for x in remove:
                    layer.pop(x)
        elif (direction % 4) == 2:
            #right
            self.nc -= 1
            for layer in self.FigureListLayer:
                remove = list()
                for x in range(0, len(layer)):
                    if layer[x].y == self.nc:
                        remove.append(x)
                remove.sort(reverse = True)
                for x in remove:
                    layer.pop(x)
        elif (direction % 4) == 3:
            #left
            self.nc -= 1
            for layer in self.FigureListLayer:
                remove = list()
                for x in range(0, len(layer)):
                    if layer[x].y == self.nc:
                        remove.append(x)
                    else:
                        layer[x].y -= 1
                remove.sort(reverse = True)
                for x in remove:
                    layer.pop(x)

    def layerUnion(self, index, color, direction):
        adapted_index = index % 9
        adapted_color = color % 9
        if adapted_index != adapted_color:
            for pixel in self.FigureListLayer[adapted_index]:
                ok = 0
                for p in self.FigureListLayer[adapted_color]:
                    if p.x == pixel.x and p.y == pixel.y:
                        ok = 1
                if ok == 0:
                    self.FigureListLayer[adapted_color].append(PixelNode(pixel.x, pixel.y))
            self.FigureListLayer[adapted_index].clear()

    def addPixelLayer(self, index, color, direction):
        adapted_index = index % 9
        if len(self.FigureListLayer[adapted_index]) == 0:
            return
        pixel_index = color % len(self.FigureListLayer[adapted_index])
        if (direction % 4) == 0:
            #down
            if self.FigureListLayer[adapted_index][pixel_index].x + 1 < self.nr:
                self.FigureListLayer[adapted_index].append(PixelNode(self.FigureListLayer[adapted_index][pixel_index].x + 1, self.FigureListLayer[adapted_index][pixel_index].y))
        elif (direction % 4) == 1:
            #up
            if self.FigureListLayer[adapted_index][pixel_index].x > 0:
                self.FigureListLayer[adapted_index].append(PixelNode(self.FigureListLayer[adapted_index][pixel_index].x - 1, self.FigureListLayer[adapted_index][pixel_index].y))
        elif (direction % 4) == 2:
            #right
            if self.FigureListLayer[adapted_index][pixel_index].y + 1 < self.nc:
                self.FigureListLayer[adapted_index].append(PixelNode(self.FigureListLayer[adapted_index][pixel_index].x, self.FigureListLayer[adapted_index][pixel_index].y + 1))
        elif (direction % 4) == 3:
            #left
            if self.FigureListLayer[adapted_index][pixel_index].y > 0:
                self.FigureListLayer[adapted_index].append(PixelNode(self.FigureListLayer[adapted_index][pixel_index].x, self.FigureListLayer[adapted_index][pixel_index].y - 1)) 

    def delPixelLayer(self, index, color, direction):
        adapted_index = index % 9
        if len(self.FigureListLayer[adapted_index]) == 0:
            return
        pixel_index = color % len(self.FigureListLayer[adapted_index])
        self.FigureListLayer[adapted_index].pop(pixel_index)

    def score(self, output_grid):
        #-2 punti per posizione non giusta, -1 punto per colore sbagliato, -3 punti dimensione griglia sbagliata per casella
        score = 0
        if self.nr <= output_grid.shape[0] and self.nc <= output_grid.shape[1]:
            for x in range(self.nr):
                for y in range(self.nc):
                    if output_grid[x][y] != 0:
                        ok = 0
                        c = 1
                        color = 0
                        for layer in self.FigureListLayer:
                            for pixel in layer:
                                if x == pixel.x and y == pixel.y:
                                    if output_grid[x][y] == c:
                                        color = 1
                                    ok = 1
                            c += 1
                        if ok == 0:
                            score += 2
                        elif ok == 1 and color != 1:
                            score += 1
                    else:
                        for layer in self.FigureListLayer:
                            for pixel in layer:
                                if x == pixel.x and y == pixel.y:
                                    score += 2
        elif self.nr > output_grid.shape[0] and self.nc > output_grid.shape[1]:
            for x in range(output_grid.shape[0]):
                for y in range(output_grid.shape[1]):
                    if output_grid[x][y] != 0:
                        ok = 0
                        c = 1
                        color = 0
                        for layer in self.FigureListLayer:
                            for pixel in layer:
                                if x == pixel.x and y == pixel.y:
                                    if output_grid[x][y] == c:
                                        color = 1
                                    ok = 1
                            c += 1
                        if ok == 0:
                            score += 2
                        elif ok == 1 and color != 1:
                            score += 1
                    else:
                        for layer in self.FigureListLayer:
                            for pixel in layer:
                                if x == pixel.x and y == pixel.y:
                                    score += 2
        elif self.nr <= output_grid.shape[0] and self.nc > output_grid.shape[1]:
            for x in range(self.nr):
                for y in range(output_grid.shape[1]):
                    if output_grid[x][y] != 0:
                        ok = 0
                        c = 1
                        color = 0
                        for layer in self.FigureListLayer:
                            for pixel in layer:
                                if x == pixel.x and y == pixel.y:
                                    if output_grid[x][y] == c:
                                        color = 1
                                    ok = 1
                            c += 1
                        if ok == 0:
                            score += 2
                        elif ok == 1 and color != 1:
                            score += 1
                    else:
                        for layer in self.FigureListLayer:
                            for pixel in layer:
                                if x == pixel.x and y == pixel.y:
                                    score += 2
        elif self.nr > output_grid.shape[0] and self.nc <= output_grid.shape[1]:
            for x in range(output_grid.shape[0]):
                for y in range(self.nc):
                    if output_grid[x][y] != 0:
                        ok = 0
                        c = 1
                        color = 0
                        for layer in self.FigureListLayer:
                            for pixel in layer:
                                if x == pixel.x and y == pixel.y:
                                    if output_grid[x][y] == c:
                                        color = 1
                                    ok = 1
                            c += 1
                        if ok == 0:
                            score += 2
                        elif ok == 1 and color != 1:
                            score += 1
                    else:
                        for layer in self.FigureListLayer:
                            for pixel in layer:
                                if x == pixel.x and y == pixel.y:
                                    score += 2
        else:
            return -100
        score += abs(output_grid.shape[0] - self.nr)*min(self.nc, output_grid.shape[1])*3 + abs(output_grid.shape[1] - self.nc)*min(self.nr, output_grid.shape[0])*3 + abs(output_grid.shape[0] - self.nr)*abs(output_grid.shape[1] - self.nc)*3
        return -score
    
    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for x in range(1, 10):
            for pixel in self.FigureListLayer[x-1]:
                grid[pixel.x][pixel.y] = x
        return grid