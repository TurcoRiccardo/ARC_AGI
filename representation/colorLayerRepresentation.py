import numpy as np
from dataclasses import dataclass
from selection.selector import Selector


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

    def moveLayer(self, s):
        adapted_index = (s.index - 1) % 9
        if len(self.FigureListLayer[adapted_index]) == 0:
            return
        new_figure = list()
        if (s.direction % 4) == 0:
            #down
            for pixel in self.FigureListLayer[adapted_index]:
                if pixel.x + 1 < self.nr:
                    new_figure.append(PixelNode(pixel.x+1, pixel.y))
                elif pixel.x + 1 == self.nr:
                    new_figure.append(PixelNode(0, pixel.y))
        elif (s.direction % 4) == 1:
            #up
            for pixel in self.FigureListLayer[adapted_index]:
                if pixel.x > 0:
                    new_figure.append(PixelNode(pixel.x-1, pixel.y))
                elif pixel.x == 0:
                    new_figure.append(PixelNode(self.nr-1, pixel.y))
        elif (s.direction % 4) == 2:
            #right
            for pixel in self.FigureListLayer[adapted_index]:
                if pixel.y + 1 < self.nc:
                    new_figure.append(PixelNode(pixel.x, pixel.y+1))
                elif pixel.y + 1 == self.nc:
                    new_figure.append(PixelNode(pixel.x, 0))
        elif (s.direction % 4) == 3:
            #left
            for pixel in self.FigureListLayer[adapted_index]:
                if pixel.y > 0:
                    new_figure.append(PixelNode(pixel.x, pixel.y-1))
                elif pixel.y == 0:
                    new_figure.append(PixelNode(pixel.x, self.nc-1))
        self.FigureListLayer[adapted_index] = new_figure

    def expandGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            self.nr += 1
        elif (s.direction % 4) == 1:
            #up
            self.nr += 1
            for layer in self.FigureListLayer:
                for pixel in layer:
                    pixel.x += 1
        elif (s.direction % 4) == 2:
            #right
            self.nc += 1
        elif (s.direction % 4) == 3:
            #left
            self.nc += 1
            for layer in self.FigureListLayer:
                for pixel in layer:
                    pixel.y += 1

    def reduceGrid(self, s):
        if (s.direction % 4) == 0:
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
        elif (s.direction % 4) == 1:
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
        elif (s.direction % 4) == 2:
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
        elif (s.direction % 4) == 3:
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

    def layerUnion(self, s):
        adapted_index = (s.index - 1) % 9
        if s.color % 2 == 0:
            if adapted_index == 8:
                for pixel in self.FigureListLayer[adapted_index]:
                    ok = 0
                    for p in self.FigureListLayer[0]:
                        if p.x == pixel.x and p.y == pixel.y:
                            ok = 1
                    if ok == 0:
                        self.FigureListLayer[0].append(PixelNode(pixel.x, pixel.y))
            else:
                for pixel in self.FigureListLayer[adapted_index]:
                    ok = 0
                    for p in self.FigureListLayer[adapted_index + 1]:
                        if p.x == pixel.x and p.y == pixel.y:
                            ok = 1
                    if ok == 0:
                        self.FigureListLayer[adapted_index + 1].append(PixelNode(pixel.x, pixel.y))
        else:
            if adapted_index == 0:
                for pixel in self.FigureListLayer[adapted_index]:
                    ok = 0
                    for p in self.FigureListLayer[8]:
                        if p.x == pixel.x and p.y == pixel.y:
                            ok = 1
                    if ok == 0:
                        self.FigureListLayer[8].append(PixelNode(pixel.x, pixel.y))
            else:
                for pixel in self.FigureListLayer[adapted_index]:
                    ok = 0
                    for p in self.FigureListLayer[adapted_index - 1]:
                        if p.x == pixel.x and p.y == pixel.y:
                            ok = 1
                    if ok == 0:
                        self.FigureListLayer[adapted_index - 1].append(PixelNode(pixel.x, pixel.y))
        self.FigureListLayer[adapted_index].clear()

    def addPixelLayer(self, s):
        adapted_index = (s.index - 1) % 9
        if len(self.FigureListLayer[adapted_index]) == 0:
            return
        pixel_index = s.color % len(self.FigureListLayer[adapted_index])
        if (s.direction % 4) == 0:
            #down
            if self.FigureListLayer[adapted_index][pixel_index].x + 1 < self.nr:
                self.FigureListLayer[adapted_index].append(PixelNode(self.FigureListLayer[adapted_index][pixel_index].x + 1, self.FigureListLayer[adapted_index][pixel_index].y))
        elif (s.direction % 4) == 1:
            #up
            if self.FigureListLayer[adapted_index][pixel_index].x > 0:
                self.FigureListLayer[adapted_index].append(PixelNode(self.FigureListLayer[adapted_index][pixel_index].x - 1, self.FigureListLayer[adapted_index][pixel_index].y))
        elif (s.direction % 4) == 2:
            #right
            if self.FigureListLayer[adapted_index][pixel_index].y + 1 < self.nc:
                self.FigureListLayer[adapted_index].append(PixelNode(self.FigureListLayer[adapted_index][pixel_index].x, self.FigureListLayer[adapted_index][pixel_index].y + 1))
        elif (s.direction % 4) == 3:
            #left
            if self.FigureListLayer[adapted_index][pixel_index].y > 0:
                self.FigureListLayer[adapted_index].append(PixelNode(self.FigureListLayer[adapted_index][pixel_index].x, self.FigureListLayer[adapted_index][pixel_index].y - 1)) 

    def delPixelLayer(self, s):
        adapted_index = (s.index - 1) % 9
        if len(self.FigureListLayer[adapted_index]) == 0:
            return
        pixel_index = s.color % len(self.FigureListLayer[adapted_index])
        self.FigureListLayer[adapted_index].pop(pixel_index)

    def score(self, output):
        score = abs(output.nr - self.nr)*min(self.nc, output.nc)*2 + abs(output.nc - self.nc)*min(self.nr,  output.nr)*2 + abs(output.nr - self.nr)*abs(output.nc - self.nc)*2
        mask = [1 for i in range(0, 9) for _ in range(0, len(output.FigureListLayer[i]))]
        for lx in range(0, 9):
            for px in self.FigureListLayer[lx]:
                ok = 0
                c = 0
                for ly in range(0, 9):
                    for py in output.FigureListLayer[ly]:
                        if px.x == py.x and px.y == py.y and mask[c] == 1:
                            score += abs(int(lx + 1) - int(ly + 1))/10
                            mask[c] = 0
                            ok = 1
                            break
                        c += 1
                    if ok == 1:
                        break
                if ok != 1:
                    score += 1
        score += sum(mask)
        return -score
    
    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for x in range(1, 10):
            for pixel in self.FigureListLayer[x-1]:
                grid[pixel.x][pixel.y] = x
        return grid