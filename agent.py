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

from utility import Individual, add_mutation, swap_mutation, tweak_mutation, error_rate, parent_selection, analyze_demo_pairs
from representation.pixelRepresentation import pixelRepresentation
from representation.rowRepresentation import rowRepresentation
from representation.columnsRepresentation import columnsRepresentation
from representation.colorLayerRepresentation import colorLayerRepresentation
from representation.rectangleRepresentation import rectangleRepresentation
from representation.figureRepresentation import figureRepresentation
from representation.borderRepresentation import borderRepresentation
from representation.firstDiagonalRepresentation import firstDiagonalRepresentation
from representation.secondDiagonalRepresentation import secondDiagonalRepresentation


POPULATION_SIZE = 50
OFFSPRING_SIZE = 10
MAX_GENERATIONS_1 = 500
MAX_GENERATIONS_2 = 2000


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

#Evolutionary algorithm on rep representation trained on example i and returns the best individual
def generate_representation_solution(rep, demo_pairs, base_act, act, indice):
    rappresentationX = rep(demo_pairs[indice].x)
    rappresentationY = rep(demo_pairs[indice].y)

    #first part of the evolutionary algorithm: we start creating individuals from scratch with base actions
    #generating the first part of the initial population with base_act
    population1 = list()
    for _ in range(0, POPULATION_SIZE//2):
        population1.append(Individual(copy.deepcopy(rappresentationX), [], [], (rappresentationX.score(rappresentationY), 0)))
    for _ in range(MAX_GENERATIONS_1):
        #genero gli offspring
        offspring = list()
        for _ in range(OFFSPRING_SIZE):
            p = parent_selection(population1)
            o: Individual = add_mutation(p, base_act)
            if o != None:
                offspring.append(o)
        #valuto il genome calcolando fitness
        for i in offspring:
            i.fitness = (i.genome.score(rappresentationY), rep.scoreAction(i.performed_actions, i.performed_selection))  
        #reinserisco gli offspring nella popolazione e tengo solo i primi POPULATION_SIZE individui
        population1.extend(offspring)
        population1.sort(key=lambda i: i.fitness, reverse = True)
        population1 = population1[:POPULATION_SIZE//2]
    
    #generating the second part of the initial population with act
    population2 = list()
    for _ in range(0, POPULATION_SIZE//2):
        population2.append(Individual(copy.deepcopy(rappresentationX), [], [], (rappresentationX.score(rappresentationY), 0)))
    '''
    for _ in range(MAX_GENERATIONS_1):
        #genero gli offspring
        offspring = list()
        for _ in range(OFFSPRING_SIZE):
            p = parent_selection(population2)
            o: Individual = add_mutation(p, act)
            if o != None:
                offspring.append(o)
        #valuto il genome calcolando fitness
        for i in offspring:
            i.fitness = (i.genome.score(rappresentationY), rep.scoreAction(i.performed_actions, i.performed_selection))  
        #reinserisco gli offspring nella popolazione e tengo solo i primi POPULATION_SIZE individui
        population2.extend(offspring)
        population2.sort(key=lambda i: i.fitness, reverse = True)
        population2 = population2[:POPULATION_SIZE//2]
    '''
    #second part of the evolutionary algorithm: we improve the individuals created
    population = list()
    population.extend(population1)
    population.extend(population2)
    for _ in range(MAX_GENERATIONS_2):
        #genero gli offspring
        offspring = list()
        for _ in range(OFFSPRING_SIZE):
            r = np.random.random()
            if r > 0.8:
                #add
                p = parent_selection(population)
                o: Individual = add_mutation(p, act)
            elif r > 0.4:
                #tweak
                p = parent_selection(population)
                o: Individual = tweak_mutation(p, act, rappresentationX)
            else:
                #swap
                p = parent_selection(population)
                o: Individual = swap_mutation(p, act, rappresentationX)
            if o != None:
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
    return err + abs(individual.fitness[0]) + abs(individual.fitness[1]/10)

#I perform the operations on all the combinations of the examples received
def generate_representation(rep, demo_pairs, base_act, act):
    possibleSolution = list()
    AvgTot = 0
    errMin = 1000
    indMin = 0
    bestIndividual = None
    #for x in range(0, len(demo_pairs)):
    #    analyze_demo_pairs(demo_pairs[x].x, demo_pairs[x].y)
    



    for x in range(0, len(demo_pairs)):
        errAvg = 0
        bestIndividual = generate_representation_solution(rep, demo_pairs, base_act, act, x)

        #mi serve qualcosa che mi aiuta a generalizzare la lista di azioni-selettore ad altri esempi dello stesso problema
        #posso provare ad utilizzare un algoritmo evolutivo con mutazioni solo sul selettore e la possibilita di dupricare o cancellare coppie azioni-selettore
        #guardo se ci sono delle mutazioni di colore senon ci sono non uso il colore, guardo se ci sono mutazioni nel numero di elementi se ...
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
        base_actionPR = [pixelRepresentation.movePixel, pixelRepresentation.expandGrid, pixelRepresentation.reduceGrid]
        actionsPR = [pixelRepresentation.movePixel, pixelRepresentation.changeColorPixel, pixelRepresentation.duplicatePixel, pixelRepresentation.removePixel, pixelRepresentation.expandGrid, pixelRepresentation.reduceGrid]
        base_actionRR = [rowRepresentation.moveRow, rowRepresentation.expandGrid, rowRepresentation.reduceGrid]
        actionsRR = [rowRepresentation.moveRow, rowRepresentation.changeColorRow, rowRepresentation.changeColorRowPixel, rowRepresentation.modifyRowAdd, rowRepresentation.modifyRowDel, rowRepresentation.modifyRowMove, rowRepresentation.expandGrid, rowRepresentation.reduceGrid]
        base_actionCR = [columnsRepresentation.moveColumn, columnsRepresentation.expandGrid, columnsRepresentation.reduceGrid]
        actionsCR = [columnsRepresentation.moveColumn, columnsRepresentation.changeColorColumn, columnsRepresentation.changeColorColumnPixel, columnsRepresentation.modifyColumnAdd, columnsRepresentation.modifyColumnDel, columnsRepresentation.modifyColumnMove, columnsRepresentation.expandGrid, columnsRepresentation.reduceGrid]
        base_actionCLR = [colorLayerRepresentation.moveLayer, colorLayerRepresentation.expandGrid, colorLayerRepresentation.reduceGrid]
        actionsCLR = [colorLayerRepresentation.moveLayer, colorLayerRepresentation.moveLayerPixel, colorLayerRepresentation.layerUnion, colorLayerRepresentation.delPixelLayer, colorLayerRepresentation.addPixelLayer, colorLayerRepresentation.expandGrid, colorLayerRepresentation.reduceGrid]
        base_actionRER = [rectangleRepresentation.moveRectangle, rectangleRepresentation.expandGrid, rectangleRepresentation.reduceGrid]
        actionsRER = [rectangleRepresentation.moveRectangle, rectangleRepresentation.changeColorRectangle, rectangleRepresentation.removeRectangle, rectangleRepresentation.duplicateNearRectangle, rectangleRepresentation.changeOrder, rectangleRepresentation.scaleUpRectangle, rectangleRepresentation.scaleDownRectangle, rectangleRepresentation.expandGrid, rectangleRepresentation.reduceGrid]
        base_actionFR = [figureRepresentation.duplicateFigure, figureRepresentation.removeFigure, figureRepresentation.changeOrder, figureRepresentation.expandGrid, figureRepresentation.reduceGrid]
        actionsFR = [figureRepresentation.moveFigure, figureRepresentation.changeColorFigure, figureRepresentation.addElementFigure_row, figureRepresentation.addElementFigure_column, figureRepresentation.removeElementFigure_row, figureRepresentation.removeElementFigure_column, figureRepresentation.duplicateFigure, figureRepresentation.removeFigure, figureRepresentation.rotateFigure, figureRepresentation.mergeFigure, figureRepresentation.divideFigure_row, figureRepresentation.divideFigure_column, figureRepresentation.changeOrder, figureRepresentation.expandGrid, figureRepresentation.reduceGrid]    
        base_actionBR = [borderRepresentation.moveBorder, borderRepresentation.expandGrid, borderRepresentation.reduceGrid]
        actionsBR = [borderRepresentation.moveBorder, borderRepresentation.changeColorBorder, borderRepresentation.changeColorCenter2, borderRepresentation.changeColorCenter3, borderRepresentation.modifyBorderFigure, borderRepresentation.expandGrid, borderRepresentation.reduceGrid]
        base_actionFDR = [firstDiagonalRepresentation.moveDiagonal, firstDiagonalRepresentation.expandGrid, firstDiagonalRepresentation.reduceGrid]
        actionsFDR = [firstDiagonalRepresentation.moveDiagonal, firstDiagonalRepresentation.changeColorDiagonal, firstDiagonalRepresentation.modifyDiagonalAdd, firstDiagonalRepresentation.modifyDiagonalDel, firstDiagonalRepresentation.modifyDiagonalMove, firstDiagonalRepresentation.expandGrid, firstDiagonalRepresentation.reduceGrid]
        base_actionSDR = [secondDiagonalRepresentation.moveDiagonal, secondDiagonalRepresentation.expandGrid, secondDiagonalRepresentation.reduceGrid]
        actionsSDR = [secondDiagonalRepresentation.moveDiagonal, secondDiagonalRepresentation.changeColorDiagonal, secondDiagonalRepresentation.modifyDiagonalAdd, secondDiagonalRepresentation.modifyDiagonalDel, secondDiagonalRepresentation.modifyDiagonalMove, secondDiagonalRepresentation.expandGrid, secondDiagonalRepresentation.reduceGrid]
        possibleSolutionRep = list()
        reps = [
            #(pixelRepresentation, base_actionPR, actionsPR),
            #(rowRepresentation, base_actionRR, actionsRR),
            #(columnsRepresentation, base_actionCR, actionsCR),
            (colorLayerRepresentation, base_actionCLR, actionsCLR),
            #(rectangleRepresentation, base_actionRER, actionsRER),
            #(figureRepresentation, base_actionFR, actionsFR),
            #(borderRepresentation, base_actionBR, actionsBR),
            #(firstDiagonalRepresentation, base_actionFDR, actionsFDR),
            #(secondDiagonalRepresentation, base_actionSDR, actionsSDR)
        ]
        #rappresentazione in cui ho delle figure che posso prolungare con ostacoli e elementi sovrapposti

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(generate_representation, rep, demo_pairs, base_act, actions) for rep, base_act, actions in reps]
            possibleSolutionRep = [f.result() for f in futures]

        #I choose the best solution based on the error rate and apply it to the test input grid
        outputs = []
        possibleSolutionRep.sort(key=lambda i: i.errAvg, reverse = False)
        print("Representation: " + str(possibleSolutionRep[0].classe))
        print("Avg Error: " + str(possibleSolutionRep[0].errAvg))
        print("Min Error: " + str(possibleSolutionRep[0].errMin))
        for x in range(0, len(test_grids)):
            rappInput = possibleSolutionRep[0].classe(copy.deepcopy(test_grids[x]))
            ind = possibleSolutionRep[0].indMin
            for action, selector in zip(possibleSolutionRep[0].list[ind].actions, possibleSolutionRep[0].list[ind].selectors):
                action(rappInput, selector)
            outputs.append([rappInput.rappToGrid()])
        return outputs
