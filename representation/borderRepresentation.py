import numpy as np
from dataclasses import dataclass
from selection.selector import Selector

class borderRepresentation:
    def __init__(self, input_grid):
        self.nr = input_grid.shape[0]
        self.nc = input_grid.shape[1]
        self.borderList = list()





    #return the total number of border
    def getNElement(self):
        return len(self.borderList)
    
    #return the total number of element in the border index
    def getElementComponent(self, index):
        return len(self.borderList[index])