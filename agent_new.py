import numpy as np
from matplotlib import pyplot as plt
from arc import train_problems, validation_problems, ArcProblem, plot_grid, describe_task_group
from arc.types import verify_is_arc_grid, ArcIOPair, ArcGrid, ArcPrediction
from arc.agents import ArcAgent
from arc.evaluation import evaluate_agent
from typing import List
from dataclasses import dataclass
import copy
from selection.selector import Selector
from concurrent.futures import ProcessPoolExecutor

from utility_new import Individual, add_mutation, swap_mutation, tweak_mutation, parent_selection, lexicase_selection, initial_analysis, NSGA2Sorter
from representation.pixelRepresentation import pixelRepresentation
from representation.rowRepresentation import rowRepresentation
from representation.columnsRepresentation import columnsRepresentation
from representation.colorLayerRepresentation import colorLayerRepresentation
from representation.rectangleRepresentation import rectangleRepresentation
from representation.figureRepresentation import figureRepresentation
from representation.coloredFigureRepresentation import coloredFigureRepresentation
from representation.borderRepresentation import borderRepresentation
from representation.firstDiagonalRepresentation import firstDiagonalRepresentation
from representation.secondDiagonalRepresentation import secondDiagonalRepresentation


POPULATION_SIZE = 50
OFFSPRING_SIZE = 10
MAX_GENERATIONS_1 = 5
MAX_GENERATIONS_2 = 50


@dataclass
class PossibleSolution:
    classe: classmethod
    actions: list
    selectors: List[Selector]
    err: int
    errAvg: int
    errMin: int


#I perform the operations on all the combinations of the examples received
def generate_representation(rep, demo_pairs, base_act, act):
    rappresentationX = []
    rappresentationY = []
    sorter = NSGA2Sorter()
    for i in range(0, len(demo_pairs)):
        rappresentationX.append(rep(demo_pairs[i].x))
        rappresentationY.append(rep(demo_pairs[i].y))

    #first part of the evolutionary algorithm: we start creating individuals from scratch with base actions
    #--------------------------------------generating the first part of the initial population with base_act--------------------------------------
    population1 = list()
    for _ in range(0, POPULATION_SIZE//2):
        new_individual = Individual([], [], [])
        scores = []
        for i in range(0, len(demo_pairs)):
            new_individual.genome.append(copy.deepcopy(rappresentationX[i]))
            scores.append(rappresentationX[i].score(rappresentationY[i]))
        new_individual.fitness = (scores, (np.sum(scores), 0))
        population1.append(new_individual)
    for _ in range(MAX_GENERATIONS_1 * len(demo_pairs[0].y) * len(demo_pairs[0].y[0])):
        #genero gli offspring
        offspring = list()
        for _ in range(OFFSPRING_SIZE):
            p = parent_selection(population1)
            #p = lexicase_selection(population1)
            o: Individual = add_mutation(p, base_act)
            if o != None:
                offspring.append(o)
        #valuto il genome calcolando fitness
        for i in offspring:
            scores = [i.genome[c].score(rappresentationY[c]) for c in range(len(demo_pairs))]
            i.fitness = (scores, (np.sum(scores), rep.scoreAction(i.performed_actions, i.performed_selection)))
        #reinserisco gli offspring nella popolazione e tengo solo i primi POPULATION_SIZE individui
        population1.extend(offspring)
        #population1.sort(key=lambda i: i.fitness[1], reverse = True) #sorting con fitness aggregata
        population1 = sorter.sort_population(population1) #NSGA2Sorter
        population1 = population1[:POPULATION_SIZE//2]
    
    #--------------------------------------generating the second part of the initial population with act--------------------------------------
    population2 = list()
    for _ in range(0, POPULATION_SIZE//2):
        new_individual = Individual([], [], [])
        scores = []
        for i in range(0, len(demo_pairs)):
            new_individual.genome.append(copy.deepcopy(rappresentationX[i]))
            scores.append(rappresentationX[i].score(rappresentationY[i]))
        new_individual.fitness = (scores, (np.sum(scores), 0))
        population2.append(new_individual)

    #-----------------------------------second part of the evolutionary algorithm: we improve the individuals created-----------------------------------
    population = list()
    population.extend(population1)
    population.extend(population2)
    print("EA Genetations: " + str(MAX_GENERATIONS_2 * len(demo_pairs[0].y) * len(demo_pairs[0].y[0])))
    for _ in range(MAX_GENERATIONS_2 * len(demo_pairs[0].y) * len(demo_pairs[0].y[0])):
        #genero gli offspring
        offspring = list()
        for _ in range(OFFSPRING_SIZE):
            r = np.random.random()
            if r > 0.8:
                #add
                #p = parent_selection(population)
                p = lexicase_selection(population)
                o: Individual = add_mutation(p, act)
            elif r > 0.4:
                #tweak
                #p = parent_selection(population)
                p = lexicase_selection(population)
                o: Individual = tweak_mutation(p, act, rappresentationX)
            else:
                #swap
                #p = parent_selection(population)
                p = lexicase_selection(population)
                o: Individual = swap_mutation(p, act, rappresentationX)
            if o != None:
                offspring.append(o)
        #valuto il genome calcolando fitness
        for i in offspring:
            scores = [i.genome[c].score(rappresentationY[c]) for c in range(len(demo_pairs))]
            i.fitness = (scores, (np.sum(scores), rep.scoreAction(i.performed_actions, i.performed_selection)))
        #reinserisco gli offspring nella popolazione e tengo solo i primi POPULATION_SIZE individui
        population.extend(offspring)
        #population.sort(key=lambda i: i.fitness[1], reverse = True) #sorting con fitness aggregata
        population = sorter.sort_population(population) #NSGA2Sorter
        population = population[:POPULATION_SIZE]

    
    print("azioni")
    print(population[0].performed_actions)
    print(len(population[0].performed_actions))
    print(population[0].performed_selection)
    print(population[0].fitness)
    prediction = ArcIOPair(rappresentationX[0].rappToGrid(), rappresentationY[0].rappToGrid())
    prediction.plot(show=True, title=f"Input-Output")
    prediction = ArcIOPair(rappresentationY[0].rappToGrid(), population[0].genome[0].rappToGrid())
    prediction.plot(show=True, title=f"Output-OutputGenerato")
    prediction = ArcIOPair(rappresentationY[1].rappToGrid(), population[0].genome[1].rappToGrid())
    prediction.plot(show=True, title=f"Output-OutputGenerato")
    ''''''

    errMin = 10000
    sum = 0
    for i in range(0, len(demo_pairs)):
        val = abs(population[0].genome[i].score(rappresentationY[i]))
        sum += val
        if val < errMin:
            errMin = val
    return PossibleSolution(rep, copy.deepcopy(population[0].performed_actions), copy.deepcopy(population[0].performed_selection), population[0].fitness, sum/len(demo_pairs), errMin)

#Class where I compare the results received from the various representations and apply the best one to the test grid
class Agent_new(ArcAgent):
    def predict(self, demo_pairs: List[ArcIOPair], test_grids: List[ArcGrid]) -> List[ArcPrediction]:
        pc = initial_analysis(demo_pairs)
        reps = [
            #(pixelRepresentation, pixelRepresentation.baseActionList(pc), pixelRepresentation.actionList(pc)),
            #(rowRepresentation, rowRepresentation.baseActionList(pc), rowRepresentation.actionList(pc)),
            #(columnsRepresentation, columnsRepresentation.baseActionList(pc), columnsRepresentation.actionList(pc)),
            #(colorLayerRepresentation, colorLayerRepresentation.baseActionList(pc), colorLayerRepresentation.actionList(pc)), #old
            #(rectangleRepresentation, rectangleRepresentation.baseActionList(pc), rectangleRepresentation.actionList(pc)),
            #(figureRepresentation, figureRepresentation.baseActionList(pc), figureRepresentation.actionList(pc)),
            (coloredFigureRepresentation, coloredFigureRepresentation.baseActionList(pc), coloredFigureRepresentation.actionList(pc)),
            #(borderRepresentation, borderRepresentation.baseActionList(pc), borderRepresentation.actionList(pc)), #old
            #(firstDiagonalRepresentation, firstDiagonalRepresentation.baseActionList(pc), firstDiagonalRepresentation.actionList(pc)),
            #(secondDiagonalRepresentation, secondDiagonalRepresentation.baseActionList(pc), secondDiagonalRepresentation.actionList(pc))
        ]
        #rappresentazione in cui ho delle figure che posso prolungare con ostacoli e elementi sovrapposti
        #un idea e quella di inserire azioni nelle base_action in base ad un analisi iniziale delle griglie
        #algoritmo evolutivo su piu test assieme

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(generate_representation, rep, demo_pairs, base_act, actions) for rep, base_act, actions in reps]
            possibleSolution = [f.result() for f in futures]

        #I choose the best solution based on the error rate and apply it to the test input grid
        outputs = []
        possibleSolution.sort(key=lambda i: i.errAvg, reverse = False)
        print("Representation: " + str(possibleSolution[0].classe))
        print("Avg Error: " + str(possibleSolution[0].errAvg))
        print("Min Error: " + str(possibleSolution[0].errMin))
        for x in range(0, len(test_grids)):
            rappInput = possibleSolution[0].classe(copy.deepcopy(test_grids[x]))
            for action, selector in zip(possibleSolution[0].actions, possibleSolution[0].selectors):
                action(rappInput, selector)
            outputs.append([rappInput.rappToGrid()])
        return outputs