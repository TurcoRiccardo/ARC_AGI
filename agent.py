import numpy as np
from matplotlib import pyplot as plt
from arc import train_problems, validation_problems, ArcProblem, plot_grid, describe_task_group
from arc.types import verify_is_arc_grid, ArcIOPair, ArcGrid, ArcPrediction
from arc.agents import ArcAgent
from arc.evaluation import evaluate_agent
from typing import List
from dataclasses import dataclass
import copy
from selection.selector import Selector, generateNewSelector, mutateSelector
from concurrent.futures import ProcessPoolExecutor

from representation.pixelRepresentation import pixelRepresentation
from representation.rowRepresentation import rowRepresentation
from representation.columnsRepresentation import columnsRepresentation
from representation.colorLayerRepresentation import colorLayerRepresentation
from representation.rectangleRepresentation import rectangleRepresentation
from representation.figureRepresentation import figureRepresentation
from representation.borderRepresentation import borderRepresentation


POPULATION_SIZE = 50
OFFSPRING_SIZE = 10
MAX_GENERATIONS_1 = 500
MAX_GENERATIONS_2 = 2000

@dataclass
class Individual:
    genome: object
    performed_selection: list
    performed_actions: list
    fitness: tuple = (None, 0)

@dataclass
class PossibleSolution:
    train: int
    actions: list
    selectors: List[Selector]
    err: int

@dataclass
class PossibleSolutionRepresentation:
    classe: classmethod
    list: List[PossibleSolution]
    errAvg: int
    errMin: int
    indMin: int

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
def error_rate(input: ArcGrid, output: ArcGrid):
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

#Evolutionary algorithm on rep representation trained on example i and returns the best individual
def generate_representation_solution(rep, demo_pairs, act, indice):
    rappresentationX = rep(demo_pairs[indice].x)
    rappresentationY = rep(demo_pairs[indice].y)
    population = list()
    for _ in range(0, POPULATION_SIZE//2):
        population.append(Individual(copy.deepcopy(rappresentationX), [], [], (rappresentationX.score(rappresentationY), 0)))
    #first part of the evolutionary algorithm: we start creating individuals from scratch
    for _ in range(MAX_GENERATIONS_1):
        #genero gli offspring
        offspring = list()
        for _ in range(OFFSPRING_SIZE):
            p = parent_selection(population)
            o: Individual = add_mutation(p, act)
            offspring.append(o)
        #valuto il genome calcolando fitness
        for i in offspring:
            i.fitness = (i.genome.score(rappresentationY), rep.scoreAction(i.performed_actions, i.performed_selection))  
        #reinserisco gli offspring nella popolazione e tengo solo i primi POPULATION_SIZE individui
        population.extend(offspring)
        population.sort(key=lambda i: i.fitness, reverse = True)
        population = population[:POPULATION_SIZE]
    #second part of the evolutionary algorithm: we improve the individuals created
    for _ in range(MAX_GENERATIONS_2):
        #genero gli offspring
        offspring = list()
        for _ in range(OFFSPRING_SIZE):
            r = np.random.random()
            if r > 0.4:
                #add
                p = parent_selection(population)
                o: Individual = add_mutation(p, act)
                offspring.append(o)
            elif r > 0.2:
                #tweak
                p = parent_selection(population)
                o: Individual = tweak_mutation(p, act, rappresentationX)
                offspring.append(o)
            else:
                #swap
                p = parent_selection(population)
                o: Individual = swap_mutation(p, act, rappresentationX)
                offspring.append(o)
        #valuto il genome calcolando fitness
        for i in offspring:
            i.fitness = (i.genome.score(rappresentationY), rep.scoreAction(i.performed_actions, i.performed_selection))  
        #reinserisco gli offspring nella popolazione e tengo solo i primi POPULATION_SIZE individui
        population.extend(offspring)
        population.sort(key=lambda i: i.fitness, reverse = True)
        population = population[:POPULATION_SIZE]
    
    '''
    print("azioni")
    print(population[0].performed_actions)
    print(len(population[0].performed_actions))
    print(population[0].performed_selection)
    print(population[0].fitness)
    prediction = ArcIOPair(rappresentationX.rappToGrid(), rappresentationY.rappToGrid())
    prediction.plot(show=True, title=f"Input-Output")
    prediction = ArcIOPair(rappresentationY.rappToGrid(), population[0].genome.rappToGrid())
    prediction.plot(show=True, title=f"Output-OutputGenerato")
    '''

    return population[0]

#Validation: I apply the set of actions to the example and find the error rate
def evaluate_representation(rep, individual, inputGrid, outputGrid):
    rappresentationX = rep(inputGrid)
    for action, selector in zip(individual.performed_actions, individual.performed_selection):
        action(rappresentationX, selector)
    err = error_rate(outputGrid, rappresentationX.rappToGrid())
    return err - individual.fitness[0] - individual.fitness[1]/10

#I perform the operations on all the combinations of the examples received
def generate_representation(rep, demo_pairs, act):
    possibleSolution = list()
    AvgTot = 0
    errMin = 1000
    indMin = 0
    bestIndividual = None
    for x in range(0, len(demo_pairs)):
        errAvg = 0
        bestIndividual = generate_representation_solution(rep, demo_pairs, act, x)

        #mi serve qualcosa che mi aiuta a generalizzare la lista di azioni-selettore ad altri esempi dello stesso problema
        #posso provare ad utilizzare un algoritmo evolutivo con mutazioni solo sul selettore e la possibilita di dupricare o cancellare coppie azioni-selettore
        #Generalizer: 
        #new_action, new_selection = borderRepresentation.generalizer(population[0].performed_actions, population[0].performed_selection)

        for y in range(0, len(demo_pairs)):
            if x != y:
                errAvg += evaluate_representation(rep, bestIndividual, demo_pairs[y].x, demo_pairs[y].y)
        if len(demo_pairs) > 1:
            possibleSolution.append(PossibleSolution(x, copy.deepcopy(bestIndividual.performed_actions), copy.deepcopy(bestIndividual.performed_selection), errAvg/(len(demo_pairs)-1)))
            AvgTot += possibleSolution[-1].err
            if possibleSolution[-1].err < errMin:
                errMin = possibleSolution[-1].err
                indMin = x
    return PossibleSolutionRepresentation(rep, possibleSolution, AvgTot/len(demo_pairs), errMin, indMin)

#Class where I compare the results received from the various representations and apply the best one to the test grid
class Agent(ArcAgent):
    def predict(self, demo_pairs: List[ArcIOPair], test_grids: List[ArcGrid]) -> List[ArcPrediction]:
        actionsPR = [pixelRepresentation.movePixel, pixelRepresentation.movePixel, pixelRepresentation.changeColorPixel, pixelRepresentation.removePixel, pixelRepresentation.duplicateNearPixel, pixelRepresentation.expandGrid, pixelRepresentation.reduceGrid]
        actionsRR = [rowRepresentation.moveRiga, rowRepresentation.changeColorRiga, rowRepresentation.modifyRigaAdd, rowRepresentation.modifyRigaDel, rowRepresentation.modifyRigaMove, rowRepresentation.expandGrid, rowRepresentation.reduceGrid]
        actionsCR = [columnsRepresentation.moveColonna, columnsRepresentation.changeColorColonna, columnsRepresentation.modifyColonnaAdd, columnsRepresentation.modifyColonnaDel, columnsRepresentation.modifyColonnaMove, columnsRepresentation.expandGrid, columnsRepresentation.reduceGrid]
        actionsCLR = [colorLayerRepresentation.moveLayer, colorLayerRepresentation.layerUnion, colorLayerRepresentation.delPixelLayer, colorLayerRepresentation.addPixelLayer, colorLayerRepresentation.expandGrid, colorLayerRepresentation.reduceGrid]
        actionsRER = [rectangleRepresentation.moveRectangle, rectangleRepresentation.changeColorRectangle, rectangleRepresentation.removeRectangle, rectangleRepresentation.duplicateNearRectangle, rectangleRepresentation.changeOrder, rectangleRepresentation.scaleUpRectangle, rectangleRepresentation.scaleDownRectangle, rectangleRepresentation.expandGrid, rectangleRepresentation.reduceGrid]
        actionsFR = [figureRepresentation.moveFigure, figureRepresentation.changeColorFigure, figureRepresentation.addElementFigure, figureRepresentation.removeElementFigure, figureRepresentation.mergeFigure, figureRepresentation.divideFigure, figureRepresentation.changeOrder, figureRepresentation.expandGrid, figureRepresentation.reduceGrid]
        actionsBR = [borderRepresentation.moveFigure, borderRepresentation.changeColorBorder, borderRepresentation.changeColorCenter2, borderRepresentation.changeColorCenter3, borderRepresentation.modifyBorderFigure, borderRepresentation.expandGrid, borderRepresentation.reduceGrid]
        possibleSolutionRep = list()
        reps = [
            (pixelRepresentation, actionsPR),
            (rowRepresentation, actionsRR),
            (columnsRepresentation, actionsCR),
            (colorLayerRepresentation, actionsCLR),
            (rectangleRepresentation, actionsRER),
            (figureRepresentation, actionsFR),
            (borderRepresentation, actionsBR)
        ]
        #rappresentazione in cui ho delle figure che posso prolungare con ostacoli e elementi sovrapposti

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(generate_representation, rep, demo_pairs, actions) for rep, actions in reps]
            possibleSolutionRep = [f.result() for f in futures]

        #I choose the best solution based on the error rate and apply it to the test input grid
        outputs = []
        possibleSolutionRep.sort(key=lambda i: i.errAvg, reverse = False)
        print("\nRepresentation: " + str(possibleSolutionRep[0].classe))
        print("Avg Error: " + str(possibleSolutionRep[0].errAvg))
        print("Min Error: " + str(possibleSolutionRep[0].errMin))
        for x in range(0, len(test_grids)):
            rappInput = possibleSolutionRep[0].classe(copy.deepcopy(test_grids[x]))
            ind = possibleSolutionRep[0].indMin
            for action, selector in zip(possibleSolutionRep[0].list[ind].actions, possibleSolutionRep[0].list[ind].selectors):
                action(rappInput, selector)
            outputs.append([rappInput.rappToGrid()])
        return outputs
