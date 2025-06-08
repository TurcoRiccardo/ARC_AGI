import numpy as np
from dataclasses import dataclass
from selection.selector import Selector


@dataclass
class PixelNode:
    x: int
    y: int
    color: int = 0

#In FigureListLayer i colori sono scalati di 1
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

    #return the total number of layer (one layer for each color)
    def getNElement(self):
        return 9
    
    #return the total number of pixel in the layer index
    def getElementComponent(self, index):
        adapted_index = (index - 1) % 9
        return (len(self.FigureListLayer[adapted_index]),)
    
    #return the list of layer index
    def generateIndexList(self, s):
        l = list()
        if s.allElement == 3:
            #all
            l = [x for x in range(0, 9)]
        else:
            #sopra sotto centro color
            l.append(s.index % 9)
        return l

    #return the list of component index
    def generateComponentList(self, s, adapted_index):
        l = list()
        if s.allComponent1 == 1:
            #da destra
            l.append(len(self.FigureListLayer[adapted_index]) - (s.component[0] % len(self.FigureListLayer[adapted_index])) - 1)
        elif s.allComponent1 == 2:
            #centro
            if len(self.FigureListLayer[adapted_index]) % 2 == 1:
                l.append(len(self.FigureListLayer[adapted_index]) // 2)
            else:
                l.append(len(self.FigureListLayer[adapted_index]) // 2 - 1)
                l.append(len(self.FigureListLayer[adapted_index]) // 2)
        elif s.allComponent1 >= 3:
            #all color
            l = [x for x in range(0, len(self.FigureListLayer[adapted_index]))]
        else:
            #da sinistra
            l.append(s.component[0] % len(self.FigureListLayer[adapted_index]))
        return l


    #moves all the pixel in the layer index based on the direction
    def moveLayer(self, s):
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if len(self.FigureListLayer[adapted_index]) != 0:
                new_figure = list()
                if (s.direction % 4) == 0:
                    #down
                    for pixel in self.FigureListLayer[adapted_index]:
                        if pixel.x + 1 < self.nr:
                            new_figure.append(PixelNode(pixel.x+1, pixel.y))
                        elif pixel.x + 1 == self.nr:
                            new_figure.append(PixelNode(0, pixel.y))
                    self.FigureListLayer[adapted_index] = new_figure
                    count += 1
                elif (s.direction % 4) == 1:
                    #up
                    for pixel in self.FigureListLayer[adapted_index]:
                        if pixel.x > 0:
                            new_figure.append(PixelNode(pixel.x-1, pixel.y))
                        elif pixel.x == 0:
                            new_figure.append(PixelNode(self.nr-1, pixel.y))
                    self.FigureListLayer[adapted_index] = new_figure
                    count += 1
                elif (s.direction % 4) == 2:
                    #right
                    for pixel in self.FigureListLayer[adapted_index]:
                        if pixel.y + 1 < self.nc:
                            new_figure.append(PixelNode(pixel.x, pixel.y+1))
                        elif pixel.y + 1 == self.nc:
                            new_figure.append(PixelNode(pixel.x, 0))
                    self.FigureListLayer[adapted_index] = new_figure
                    count += 1
                elif (s.direction % 4) == 3:
                    #left
                    for pixel in self.FigureListLayer[adapted_index]:
                        if pixel.y > 0:
                            new_figure.append(PixelNode(pixel.x, pixel.y-1))
                        elif pixel.y == 0:
                            new_figure.append(PixelNode(pixel.x, self.nc-1))
                    self.FigureListLayer[adapted_index] = new_figure
                    count += 1
        if count != 0:
            return 0
        return 1

    #move a pixel in the selected layer index in the direction direction
    def moveLayerPixel(self, s):
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if len(self.FigureListLayer[adapted_index]) != 0:
                lc = self.generateComponentList(s, adapted_index)
                for adapted_component in lc:
                    if (s.direction % 4) == 0:
                        if self.FigureListLayer[adapted_index][adapted_component].x + 1 < self.nr:
                            #down
                            self.FigureListLayer[adapted_index][adapted_component].x += 1
                            count += 1
                    elif (s.direction % 4) == 1:
                        if self.FigureListLayer[adapted_index][adapted_component].x > 0:
                            #up
                            self.FigureListLayer[adapted_index][adapted_component].x -= 1
                            count += 1
                    elif (s.direction % 4) == 2:
                        if self.FigureListLayer[adapted_index][adapted_component].y + 1 < self.nc:
                            #right
                            self.FigureListLayer[adapted_index][adapted_component].y += 1
                            count += 1
                    elif (s.direction % 4) == 3:
                        if self.FigureListLayer[adapted_index][adapted_component].y > 0:
                            #left
                            self.FigureListLayer[adapted_index][adapted_component].y -= 1
                            count += 1
        if count != 0:
            return 0
        return 1

    #move the pixel of the layer index in another layer based on the color 
    def layerUnion(self, s):
        count = 0
        l = self.generateIndexList(s)
        if (s.color % 2) == 0:
            l.sort(key=lambda i: i, reverse=True)
        elif (s.color % 2) == 1:
            l.sort(key=lambda i: i, reverse=False)
        for adapted_index in l:
            if s.color % 2 == 0:
                if adapted_index != 8:
                    for pixel in self.FigureListLayer[adapted_index]:
                        ok = 0
                        for p in self.FigureListLayer[adapted_index + 1]:
                            if p.x == pixel.x and p.y == pixel.y:
                                ok = 1
                        if ok == 0:
                            self.FigureListLayer[adapted_index + 1].append(PixelNode(pixel.x, pixel.y))
                    self.FigureListLayer[adapted_index].clear()
                    count += 1
            else:
                if adapted_index != 0:
                    for pixel in self.FigureListLayer[adapted_index]:
                        ok = 0
                        for p in self.FigureListLayer[adapted_index - 1]:
                            if p.x == pixel.x and p.y == pixel.y:
                                ok = 1
                        if ok == 0:
                            self.FigureListLayer[adapted_index - 1].append(PixelNode(pixel.x, pixel.y))
                    self.FigureListLayer[adapted_index].clear()
                    count += 1
        if count != 0:
            return 0
        return 1

    #remove a pixel from the layer index
    def delPixelLayer(self, s):
        count = 0
        li = self.generateIndexList(s)
        for adapted_index in li:
            if len(self.FigureListLayer[adapted_index]) != 0:
                lc = self.generateComponentList(s, adapted_index)
                lc.sort(key=lambda i: i, reverse=True)
                for adapted_component in lc:
                    self.FigureListLayer[adapted_index].pop(adapted_component)
                    count += 1
        if count != 0:
            return 0
        return 1

    #add a pixel in the layer index near the pixel component in the direction direction
    def addPixelLayer(self, s):
        count = 0
        l = self.generateIndexList(s)
        for adapted_index in l:
            if len(self.FigureListLayer[adapted_index]) != 0:
                lc = self.generateComponentList(s, adapted_index)
                newPixel = []
                for adapted_component in lc:
                    pixel = PixelNode(self.FigureListLayer[adapted_index][adapted_component].x, self.FigureListLayer[adapted_index][adapted_component].y)
                    newPixel.append((adapted_index+1, pixel))
                    count += 1
                if len(newPixel) > 0:
                    newPixel.sort(key=lambda i: i[0], reverse=True)
                    for (index, fig) in newPixel:
                        self.FigureListLayer[adapted_index].insert(index, fig)
        if count != 0:
            return 0
        return 1

    #expand the grid in the direction direction
    def expandGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            if self.nr < 30:
                self.nr += 1
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr < 30:
                self.nr += 1
                for layer in self.FigureListLayer:
                    for pixel in layer:
                        pixel.x += 1
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc < 30:
                self.nc += 1
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc < 30:
                self.nc += 1
                for layer in self.FigureListLayer:
                    for pixel in layer:
                        pixel.y += 1
                return 0
        return 1

    #reduce the grid in the direction direction
    def reduceGrid(self, s):
        if (s.direction % 4) == 0:
            #down
            if self.nr > 1:
                self.nr -= 1
                for layer in self.FigureListLayer:
                    remove = list()
                    for x in range(0, len(layer)):
                        if layer[x].x == self.nr:
                            remove.append(x)
                    remove.sort(reverse = True)
                    for x in remove:
                        layer.pop(x)
                return 0
        elif (s.direction % 4) == 1:
            #up
            if self.nr > 1:
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
                return 0
        elif (s.direction % 4) == 2:
            #right
            if self.nc > 1:
                self.nc -= 1
                for layer in self.FigureListLayer:
                    remove = list()
                    for x in range(0, len(layer)):
                        if layer[x].y == self.nc:
                            remove.append(x)
                    remove.sort(reverse = True)
                    for x in remove:
                        layer.pop(x)
                return 0
        elif (s.direction % 4) == 3:
            #left
            if self.nc > 1:
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
                return 0
        return 1


    #fitness function
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
    
    #transform the representation into an ARC grid
    def rappToGrid(self):
        grid = np.zeros([self.nr, self.nc], dtype=np.uint8)
        for x in range(1, 10):
            for pixel in self.FigureListLayer[x-1]:
                grid[pixel.x][pixel.y] = x
        return grid
    
    #function that calculates a score based on the selectors used
    def scoreAction(performed_actions, performed_selection):
        score = 0
        for x in range(0, len(performed_actions)):
            if performed_actions[x] == colorLayerRepresentation.moveLayerPixel or performed_actions[x] == colorLayerRepresentation.addPixelLayer or performed_actions[x] == colorLayerRepresentation.delPixelLayer:
                score += 0.5
            score += 1
        return -score
    
    #return the list of actions
    def actionList(demo_pairs):     
        l = [colorLayerRepresentation.moveLayer, colorLayerRepresentation.moveLayerPixel, colorLayerRepresentation.layerUnion, colorLayerRepresentation.delPixelLayer, colorLayerRepresentation.addPixelLayer, colorLayerRepresentation.expandGrid, colorLayerRepresentation.reduceGrid]
        

        return l
    
    #return the list of base actions
    def baseActionList(demo_pairs):
        l = [colorLayerRepresentation.moveLayer, colorLayerRepresentation.expandGrid, colorLayerRepresentation.reduceGrid]


        return l