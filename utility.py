import numpy as np
import copy
from selection.selector import Selector, generateNewSelector, mutateSelector
from dataclasses import dataclass


@dataclass
class Individual:
    genome: object
    performed_selection: list
    performed_actions: list
    fitness: tuple = (None, 0)

#For parent selection we use Tournament Selection
def parent_selection(population):
    candidates = sorted(np.random.choice(population, 2), key=lambda e: e.fitness, reverse = True)
    return candidates[0]

#add a new action to the parent generating a new individual
def add_mutation(p: Individual, available_actions):
    new_gen = copy.deepcopy(p.genome)
    for _ in range(0, 5):
        #take a random action
        x = np.random.randint(0, len(available_actions))
        action = available_actions[x]
        #generate a new selector
        s = generateNewSelector(p.genome)
        #execute the action with the selector
        r = action(new_gen, s)
        if r == 0:
            break
    new_selection = p.performed_selection.copy()
    new_selection.append(s)
    new_paction = p.performed_actions.copy()
    new_paction.append(action)
    return Individual(new_gen, new_selection, new_paction)

#improve the list of actions by tweaking the selector of a given action of the parent generating a new individual
def tweak_mutation(p: Individual, available_actions, initial_representation):
    if len(p.performed_actions) == 0:
        return add_mutation(p, available_actions)
    new_gen = copy.deepcopy(initial_representation)
    new_paction = []
    new_selection = []
    x = np.random.randint(0, len(p.performed_actions))
    for i, (action, selector) in enumerate(zip(p.performed_actions, p.performed_selection)):
        if i == x:
            new_selector = mutateSelector(selector)
        else:
            new_selector = copy.deepcopy(selector)
        action(new_gen, new_selector)
        new_paction.append(action)
        new_selection.append(new_selector)
    return Individual(new_gen, new_selection, new_paction)

#change the order of the list of actions of the parent generating a new individual
def swap_mutation(p: Individual, available_actions, initial_representation):
    if len(p.performed_actions) <= 1:
        return add_mutation(p, available_actions)
    new_gen = copy.deepcopy(initial_representation)
    new_paction = []
    new_selection = []
    x = np.random.randint(0, len(p.performed_actions) - 1)
    for i in range(0, len(p.performed_actions)):
        if i == x:
            selector = copy.deepcopy(p.performed_selection[i+1])
            action = p.performed_actions[i+1]
        elif i == x + 1:
            selector = copy.deepcopy(p.performed_selection[i-1])
            action = p.performed_actions[i-1]
        else:
            selector = copy.deepcopy(p.performed_selection[i])
            action = p.performed_actions[i]
        action(new_gen, selector)
        new_paction.append(action)
        new_selection.append(selector)
    return Individual(new_gen, new_selection, new_paction)

#Class where I calculate the error rate simply by comparing the input and output grid and each difference counts 1
def error_rate(input, output):
    val = 0
    if input.shape[0] <= output.shape[0] and input.shape[1] <= output.shape[1]:
        for x in range(input.shape[0]):
            for y in range(input.shape[1]):
                if input[x][y] != output[x][y]:
                    val += 1
    elif input.shape[0] > output.shape[0] and input.shape[1] > output.shape[1]:
        for x in range(output.shape[0]):
            for y in range(output.shape[1]):
                if input[x][y] != output[x][y]:
                    val += 1
    elif input.shape[0] <= output.shape[0] and input.shape[1] > output.shape[1]:
        for x in range(input.shape[0]):
            for y in range(output.shape[1]):
                if input[x][y] != output[x][y]:
                    val += 1
    elif input.shape[0] > output.shape[0] and input.shape[1] <= output.shape[1]:
        for x in range(output.shape[0]):
            for y in range(input.shape[1]):
                if input[x][y] != output[x][y]:
                    val += 1
    else:
        return 100
    val += abs(output.shape[0] - input.shape[0])*min(input.shape[1], output.shape[1]) + abs(output.shape[1] - input.shape[1])*min(input.shape[0], output.shape[0]) + abs(output.shape[0] - input.shape[0])*abs(output.shape[1] - input.shape[1])
    return val

@dataclass
class PixelNode:
    x: int
    y: int
    color: int = 0

def ricFindFigure(grid, posX, posY, pixel, mask, nc, nr):
    if mask[posX][posY] == 1:
        mask[posX][posY] = 0
        pixel.append(PixelNode(posX, posY, grid[posX][posY]))
    if posX+1 < nr:
        #down
        if grid[posX+1][posY] != 0 and mask[posX+1][posY] == 1:
            ricFindFigure(grid, posX+1, posY, pixel, mask, nc, nr)
    if posX+1 < nr and posY+1 < nc:
        #down-right
        if grid[posX+1][posY+1] != 0 and mask[posX+1][posY+1] == 1:
            ricFindFigure(grid, posX+1, posY+1, pixel, mask, nc, nr)
    if posX+1 < nr and posY > 0:
        #down-left
        if grid[posX+1][posY-1] != 0 and mask[posX+1][posY-1] == 1:
            ricFindFigure(grid, posX+1, posY-1, pixel, mask, nc, nr)
    if posX > 0:
        #up
        if grid[posX-1][posY] != 0 and mask[posX-1][posY] == 1:
            ricFindFigure(grid, posX-1, posY, pixel, mask, nc, nr)
    if posX > 0 and posY+1 < nc:
        #up-right
        if grid[posX-1][posY+1] != 0 and mask[posX-1][posY+1] == 1:
            ricFindFigure(grid, posX-1, posY+1, pixel, mask, nc, nr)
    if posX > 0 and posY > 0:
        #up-left
        if grid[posX-1][posY-1] != 0 and mask[posX-1][posY-1] == 1:
            ricFindFigure(grid, posX-1, posY-1, pixel, mask, nc, nr)
    if posY+1 < nc:
        #right
        if grid[posX][posY+1] != 0 and mask[posX][posY+1] == 1:
            ricFindFigure(grid, posX, posY+1, pixel, mask, nc, nr)
    if posY > 0:
        #left
        if grid[posX][posY-1] != 0 and mask[posX][posY-1] == 1:
            ricFindFigure(grid, posX, posY-1, pixel, mask, nc, nr)
    return 

@dataclass
class InfoDemoPairs:
    row_separator: list
    column_separator: list
    have_legend: int
    starting_point_list_i: list
    grid_list_i: list
    starting_point_list_o: list
    grid_list_o: list

#Class in which we analyze the elements that are present in a demo_pairs 
def analyze_demo_pairs(input, output):
    mc = InfoDemoPairs([], [], -1, [], [], [], [])
    #analyze if the grid contain a legend
    grid = np.zeros((input.shape[0], input.shape[1]), dtype=int)
    #row separation
    for x in range(0, input.shape[0]):
        mask = [1 for _ in range(0, input.shape[1])]
        color = 0
        for y in range(0, input.shape[1]):
            if input[x][y] != 0:
                if color == 0:
                    color = input[x][y]
                if color == input[x][y]:
                    mask[y] = 0
        if sum(mask) == 0:
            #finded a separation row
            mc.row_separator.append(x)
            for y in range(0, input.shape[1]):
                grid[x][y] = color
    #column separation
    for y in range(0, input.shape[1]):
        mask = [1 for _ in range(0, input.shape[0])]
        color = 0
        for x in range(0, input.shape[0]):
            if input[x][y] != 0:
                if color == 0:
                    color = input[x][y]
                if color == input[x][y]:
                    mask[x] = 0
        if sum(mask) == 0:
            #finded a separation column
            mc.column_separator.append(y)
            for x in range(0, input.shape[0]):
                grid[x][y] = color
    #analyze different area of the grid
    if len(mc.row_separator) > 0:
        for i in range(0, len(mc.row_separator)):
            for c in range(0, len(mc.column_separator)):

                for x in range(0, i):
                    for y in range(0, c):
                        print()
    elif len(mc.column_separator) > 0:
        for c in range(0, len(mc.column_separator)):
            for x in range(0, input.shape[0]):
                for y in range(0, c):
                    print()
        
        for x in range(0, input.shape[0]):
            for y in range(mc.column_separator[-1], input.shape[1]):
                print()







    #find object in the input grid
    mask = np.ones((input.shape[0], input.shape[1]), dtype=int)
    for x in range(0, input.shape[0]):
        for y in range(0, input.shape[1]):
            if input[x][y] != 0 and mask[x][y] == 1:
                pixel = list()
                ricFindFigure(input, x, y, pixel, mask, input.shape[0], input.shape[1])
                xMax = 0
                xMin = 1000
                yMax = 0
                yMin = 1000
                for p in pixel:
                    if xMax < p.x:
                        xMax = p.x
                    if xMin > p.x:
                        xMin = p.x
                    if yMax < p.y:
                        yMax = p.y
                    if yMin > p.y:
                        yMin = p.y
                mc.starting_point_list_i.append(PixelNode(xMin, yMin))
                mc.grid_list_i.append(np.zeros((xMax-xMin+1, yMax-yMin+1), dtype=int))
    #find object in the output grid
    mask = np.ones((output.shape[0], output.shape[1]), dtype=int)
    for x in range(0, output.shape[0]):
        for y in range(0, output.shape[1]):
            if output[x][y] != 0 and mask[x][y] == 1:
                pixel = list()
                ricFindFigure(output, x, y, pixel, mask, output.shape[0], output.shape[1])
                xMax = 0
                xMin = 1000
                yMax = 0
                yMin = 1000
                for p in pixel:
                    if xMax < p.x:
                        xMax = p.x
                    if xMin > p.x:
                        xMin = p.x
                    if yMax < p.y:
                        yMax = p.y
                    if yMin > p.y:
                        yMin = p.y
                mc.starting_point_list_o.append(PixelNode(xMin, yMin))
                mc.grid_list_o.append(np.zeros((xMax-xMin+1, yMax-yMin+1), dtype=int))
    #



