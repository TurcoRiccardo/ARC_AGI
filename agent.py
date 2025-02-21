import numpy as np
from matplotlib import pyplot as plt
from arc import train_problems, validation_problems, ArcProblem, plot_grid, describe_task_group
from arc.types import verify_is_arc_grid, ArcIOPair, ArcGrid, ArcPrediction
from arc.agents import ArcAgent
from arc.evaluation import evaluate_agent
from typing import List
from dataclasses import dataclass
import copy

from representation.pixelRepresentation import pixelRepresentation
from representation.rowRepresentation import rowRepresentation
from representation.columnsRepresentation import columnsRepresentation
from representation.colorLayerRepresentation import colorLayerRepresentation


POPULATION_SIZE = 50
OFFSPRING_SIZE = 10
MAX_GENERATIONS = 2000

@dataclass
class Individual:
    genome: object
    available_actions: list
    parameters: list
    performed_actions: list
    fitness: tuple = (None, 0)

def parent_selection(population):
    candidates = sorted(np.random.choice(population, 2), key=lambda e: e.fitness, reverse = True)
    return candidates[0]
    
def mutation(p: Individual):
    x = np.random.randint(0, len(p.available_actions))
    action = p.available_actions[x]
    new_gen = copy.deepcopy(p.genome)
    index = 0
    if p.genome.getNElement() != 0:
        index = np.random.randint(0, p.genome.getNElement())
    col = np.random.randint(0, 9)
    pos = np.random.randint(0, 4)
    action(new_gen, index, col, pos)
    new_parameters = p.parameters.copy()
    new_parameters.append((index, col, pos))
    new_paction = p.performed_actions.copy()
    new_paction.append(action)
    return Individual(new_gen, p.available_actions, new_parameters, new_paction)

@dataclass
class PossibleSolution:
    classe: classmethod
    actions1: list
    parameters1: list
    err1: int
    actions2: list
    parameters2: list
    err2: int

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

def generate_representation_solution(rep, demo_pairs, act):
    rappresentationX = rep(demo_pairs[0].x)
    rappresentationY = rep(demo_pairs[0].y)
    population = list()
    population.append(Individual(copy.deepcopy(rappresentationX), act, [], [], (rappresentationX.score(rappresentationY), 0)))
    population.append(Individual(copy.deepcopy(rappresentationX), act, [], [], (rappresentationX.score(rappresentationY), 0)))
    for _ in range(MAX_GENERATIONS):
        #genero gli offspring
        offspring = list()
        for _ in range(OFFSPRING_SIZE):
            p = parent_selection(population)
            o: Individual = mutation(p)
            offspring.append(o)
        #valuto il genome calcolando fitness
        for i in offspring:

            i.fitness = (i.genome.score(rappresentationY), -len(i.performed_actions))  
        #reinserisco gli offspring nella popolazione e tengo solo i primi POPULATION_SIZE individui
        population.extend(offspring)
        population.sort(key=lambda i: i.fitness, reverse = True)
        population = population[:POPULATION_SIZE]
    #Validazione: applico la miglior serie di azioni al secondo esempio e trovo l'error rate

    #print(population[0].fitness)
    #print(population[0].genome.scoresc(rappresentationY))
    #prediction = ArcIOPair(demo_pairs[0].x, demo_pairs[0].y)
    #prediction.plot(show=True, title=f"Input-Output")
    #prediction = ArcIOPair(demo_pairs[0].y, population[0].genome.rappToGrid())
    #prediction.plot(show=True, title=f"Output-OutputGenerato")



    rappresentationX = rep(demo_pairs[1].x)
    c = 0
    for action in population[0].performed_actions:
        action(rappresentationX, population[0].parameters[c][0], population[0].parameters[c][1], population[0].parameters[c][2])
        c += 1
    err1 = error_rate(demo_pairs[1].y, rappresentationX.rappToGrid())
    actions1 = copy.deepcopy(population[0].performed_actions)
    parameters1 = copy.deepcopy(population[0].parameters)
    #Ripeto procedimento ma addestro su esempio 2 e valido su esempio 1 del training set
    rappresentationX = rep(demo_pairs[1].x)
    rappresentationY = rep(demo_pairs[1].y)
    population = list()
    population.append(Individual(copy.deepcopy(rappresentationX), act, [], [], (rappresentationX.score(rappresentationY), 0)))
    population.append(Individual(copy.deepcopy(rappresentationX), act, [], [], (rappresentationX.score(rappresentationY), 0)))
    for _ in range(MAX_GENERATIONS):
        #genero gli offspring
        offspring = list()
        for _ in range(OFFSPRING_SIZE):
            p = parent_selection(population)
            o: Individual = mutation(p)
            offspring.append(o)
        #valuto il genome calcolando fitness
        for i in offspring:
            i.fitness = (i.genome.score(rappresentationY), -len(i.performed_actions))  
        #reinserisco gli offspring nella popolazione e tengo solo i primi POPULATION_SIZE individui
        population.extend(offspring)
        population.sort(key=lambda i: i.fitness, reverse = True)
        population = population[:POPULATION_SIZE]
    #Validazione: applico la miglior serie di azioni al primo esempio e trovo l'error rate
    rappresentationX = rep(demo_pairs[0].x)
    c = 0
    for action in population[0].performed_actions:
        action(rappresentationX, population[0].parameters[c][0], population[0].parameters[c][1], population[0].parameters[c][2])
        c += 1
    err = error_rate(demo_pairs[0].y, rappresentationX.rappToGrid())
    return PossibleSolution(rep, actions1, parameters1, err1, copy.deepcopy(population[0].performed_actions), copy.deepcopy(population[0].parameters), err)


#Classe in cui cerco la serie di azioni necessarie a risolvere il problema con un algoritmo evolutivo: addestro su esempio 1 e valido su esempio 2 e poi faccio viceversa
class Agent(ArcAgent):
    def predict(self, demo_pairs: List[ArcIOPair], test_grids: List[ArcGrid]) -> List[ArcPrediction]:
        actionsPR = [pixelRepresentation.movePixel, pixelRepresentation.changeColorPixel, pixelRepresentation.RemovePixel, pixelRepresentation.DuplicateNearPixel, pixelRepresentation.expandGrid, pixelRepresentation.reduceGrid]
        actionsRR = [rowRepresentation.moveRiga, rowRepresentation.changeColorRiga, rowRepresentation.modifyRigaAdd, rowRepresentation.modifyRigaDel, rowRepresentation.modifyRigaMove, rowRepresentation.expandGrid, rowRepresentation.reduceGrid]
        actionsCR = [columnsRepresentation.moveColonna, columnsRepresentation.changeColorColonna, columnsRepresentation.modifyColonnaAdd, columnsRepresentation.modifyColonnaDel, columnsRepresentation.modifyColonnaMove, columnsRepresentation.expandGrid, columnsRepresentation.reduceGrid]
        actionsCLR = [colorLayerRepresentation.moveLayer, colorLayerRepresentation.layerUnion, colorLayerRepresentation.addPixelLayer, colorLayerRepresentation.delPixelLayer, colorLayerRepresentation.expandGrid, colorLayerRepresentation.reduceGrid]

        possibleSolution = list()

        #possibleSolution.append(generate_representation_solution(pixelRepresentation, demo_pairs, actionsPR))
        #possibleSolution.append(generate_representation_solution(rowRepresentation, demo_pairs, actionsRR))
        #possibleSolution.append(generate_representation_solution(columnsRepresentation, demo_pairs, actionsCR))
        possibleSolution.append(generate_representation_solution(colorLayerRepresentation, demo_pairs, actionsCLR))



        #scelgo la miglior soluzione in base all'error rate e la applico alla griglia in input di test
        possibleSolution.sort(key=lambda i: i.err1 + i.err2, reverse = False)
        rappInput = possibleSolution[0].classe(copy.deepcopy(test_grids[0]))
        c = 0
        print(possibleSolution[0].classe)
        print(possibleSolution[0].err1)
        print(possibleSolution[0].err2)
        if possibleSolution[0].err1 < possibleSolution[0].err2:
            for action in possibleSolution[0].actions1:
                action(rappInput, possibleSolution[0].parameters1[c][0], possibleSolution[0].parameters1[c][1], possibleSolution[0].parameters1[c][2])
                c += 1
        else:
            for action in possibleSolution[0].actions2:
                action(rappInput, possibleSolution[0].parameters2[c][0], possibleSolution[0].parameters2[c][1], possibleSolution[0].parameters2[c][2])
                c += 1
        outputs = []
        outputs.append([rappInput.rappToGrid()])
        return outputs
