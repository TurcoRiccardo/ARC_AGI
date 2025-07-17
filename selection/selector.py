from dataclasses import dataclass
import numpy as np


@dataclass
class Selector:
    index: int
    component: int
    color: int
    direction: int
    allElement: int #0 sopra, 1 sotto, 2 centro, 3 all, 4 color
    allComponent1: int #0 sopra, 1 sotto, 2 centro, 3 all, 4 color
    allComponent2: int #0 sopra, 1 sotto, 2 centro, 3 all, 4 color

#generates a new random selector from scratch
def generateNewSelector(rappresentation):
    index = 0
    component = (0,)
    ok = 0
    ne = rappresentation.getNElement()
    if ne != 0:
        index = np.random.randint(0, ne)
        ec = rappresentation.getElementComponent(index)
        for val in ec:
            if val <= 0:
                ok = 1
        if ok == 0:
            component = np.random.randint(0, ec)
    allElement = np.random.randint(0, 5)
    allComponent1 = np.random.randint(0, 5)
    allComponent2 = np.random.randint(0, 5)
    if allElement == 4:
        colorList = list(rappresentation.getColors())
        if 0 in colorList:
            colorList.remove(0)
        color = np.random.choice(colorList)
    else:
        color = np.random.randint(1, 10)
    direction = np.random.randint(0, 4)
    return Selector(index, component, color, direction, allElement, allComponent1, allComponent2)

#generates a new selector mutating the received selector
def mutateSelector(s: Selector):
    new_allElement = s.allElement
    new_allComponent1 = s.allComponent1
    new_allComponent2 = s.allComponent2
    c = np.random.randint(0, 3)
    if c == 0:
        l = [i for i in range(0, 5)]
        l.remove(s.allElement)
        new_allElement = l[np.random.randint(0, len(l))]
    elif c == 1:
        l = [i for i in range(0, 5)]
        l.remove(s.allComponent1)
        new_allComponent1 = l[np.random.randint(0, len(l))]
    else:
        l = [i for i in range(0, 5)]
        l.remove(s.allComponent2)
        new_allComponent2 = l[np.random.randint(0, len(l))]
    return Selector(s.index, s.component, s.color, s.direction, new_allElement, new_allComponent1, new_allComponent2)

#generates a new random selector from scratch
def generateNewSelector_new(rappresentationList):
    index = 0
    component = (0,)
    nemin = 1000
    for i in range(0, len(rappresentationList)):
        ne = rappresentationList[i].getNElement()
        if ne != 0:
            if ne <= nemin:
                nemin = ne
                index = np.random.randint(0, ne)
                ec = rappresentationList[i].getElementComponent(index)
                ok = 0
                for val in ec:
                    if val <= 0:
                        ok = 1
                if ok == 0:
                    component = np.random.randint(0, ec)
    allElement = np.random.randint(0, 5)
    allComponent1 = np.random.randint(0, 5)
    allComponent2 = np.random.randint(0, 5)
    color = np.random.randint(1, 10)
    if allElement == 4:
        colorSet = set()
        for i in range(0, len(rappresentationList)):
            colorSet.update(rappresentationList[i].getColors())
        colorList = list(colorSet)
        if 0 in colorList:
            colorList.remove(0)
        if len(colorList) != 0:
            color = np.random.choice(colorList)
    direction = np.random.randint(0, 4)
    return Selector(index, component, color, direction, allElement, allComponent1, allComponent2)