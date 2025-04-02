from dataclasses import dataclass
import numpy as np


@dataclass
class Selector:
    index: int
    component: int
    color: int
    direction: int
    allElement: int #0 sopra, 1 sotto, 2 centro, 3 all, 4 color
    allComponent: int #0 sopra, 1 sotto, 2 centro, 3 all, 4 color

#generates a new random selector from scratch
def generateNewSelector(rappresentation):
    index = 0
    component = 0
    allElement = 0
    allComponent = 0
    if rappresentation.getNElement() != 0:
        index = np.random.randint(0, rappresentation.getNElement())
        if rappresentation.getElementComponent(index) != 0:
            component = np.random.randint(0, rappresentation.getElementComponent(index))
    allElement = np.random.randint(0, 5)
    allComponent = np.random.randint(0, 5)
    color = np.random.randint(1, 10)
    direction = np.random.randint(0, 4)
    return Selector(index, component, color, direction, allElement, allComponent)

#generates a new selector mutating the received selector
def mutateSelector(s: Selector):
    new_allElement = s.allElement
    new_allComponent = s.allComponent
    if np.random.randint(0, 2) == 0:
        l = [i for i in range(0, 5)]
        l.remove(s.allElement)
        new_allElement = l[np.random.randint(0, len(l))]
    else:
        l = [i for i in range(0, 5)]
        l.remove(s.allComponent)
        new_allComponent = l[np.random.randint(0, len(l))]
    return Selector(s.index, s.component, s.color, s.direction, new_allElement, new_allComponent)