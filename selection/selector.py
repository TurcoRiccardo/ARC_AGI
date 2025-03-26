from dataclasses import dataclass
import numpy as np


@dataclass
class Selector:
    index: int
    component: int
    color: int
    direction: int
    allElement: int #0 sopra, 1 sotto, 2 centro, 3 all, 4 color

#ha senso una nn per generare i selettori ??????

def generateNewSelector(rappresentation):
    index = 0
    component = 0
    allElement = 0
    if rappresentation.getNElement() != 0:
        index = np.random.randint(0, rappresentation.getNElement())
        if rappresentation.getElementComponent(index) != 0:
            component = np.random.randint(0, rappresentation.getElementComponent(index))
    allElement = np.random.randint(0, 5)
    color = np.random.randint(1, 10)
    direction = np.random.randint(0, 4)
    return Selector(index, component, color, direction, allElement)