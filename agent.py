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

from representation.pixelRepresentation import pixelRepresentation
from representation.rowRepresentation import rowRepresentation
from representation.columnsRepresentation import columnsRepresentation
from representation.colorLayerRepresentation import colorLayerRepresentation
from representation.rectangleRepresentation import rectangleRepresentation
from representation.figureRepresentation import figureRepresentation
from representation.borderRepresentation import borderRepresentation


POPULATION_SIZE = 50
OFFSPRING_SIZE = 10
MAX_GENERATIONS = 2000

@dataclass
class Individual:
    genome: object
    available_actions: list
    performed_selection: list
    performed_actions: list
    fitness: tuple = (None, 0)

@dataclass
class PossibleSolution:
    train: int
    validation: int
    actions: list
    selectors: List[Selector]
    err: int

@dataclass
class PossibleSolutionRepresentation:
    classe: classmethod
    list: List[PossibleSolution]
    errTot: int
    errMin: int
    indMin: int

def parent_selection(population):
    candidates = sorted(np.random.choice(population, 2), key=lambda e: e.fitness, reverse = True)
    return candidates[0]
    
def mutation(p: Individual):
    new_gen = copy.deepcopy(p.genome)
    for _ in range(0, 10):
        #take a random action
        x = np.random.randint(0, len(p.available_actions))
        action = p.available_actions[x]
        #generate a new selector
        index = 0
        component = 0
        if p.genome.getNElement() != 0:
            index = np.random.randint(0, p.genome.getNElement())
            if p.genome.getElementComponent(index) != 0:
                component = np.random.randint(0, p.genome.getElementComponent(index))
        color = np.random.randint(0, 1)
        direction = np.random.randint(0, 4)
        s = Selector(index, component, color, direction)
        #execute the action with the selector
        r = action(new_gen, s)
        if r == 0:
            break
    new_selection = p.performed_selection.copy()
    new_selection.append(s)
    new_paction = p.performed_actions.copy()
    new_paction.append(action)
    return Individual(new_gen, p.available_actions, new_selection, new_paction)

#Classe in cui calcolo l'error rate semplicemente confrontando la grizioa di input e quella di output ed ogni differenza conta 1
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

#Algoritmo evolutivo sulla rappresentazione rep: addestro su esempio i1 e valido su esempio i2
def generate_representation_solution(rep, demo_pairs, act, i1, i2):
    rappresentationX = rep(demo_pairs[i1].x)
    rappresentationY = rep(demo_pairs[i1].y)
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

    print(population[0].fitness)
    print(population[0].genome.scoresc(rappresentationY))
    prediction = ArcIOPair(rappresentationX.rappToGrid(), rappresentationY.rappToGrid())
    prediction.plot(show=True, title=f"Input-Output")
    prediction = ArcIOPair(rappresentationY.rappToGrid(), population[0].genome.rappToGrid())
    prediction.plot(show=True, title=f"Output-OutputGenerato")


    #mi serve qualcosa che mi aiuta a generalizzare la lista di azioni-selettore ad altri esempi dello stesso problema
    #posso provare ad utilizzare un algoritmo evolutivo con mutazioni solo sul selettore e la possibilita di dupricare o cancellare coppie azioni-selettore

    rappresentationX = rep(demo_pairs[i2].x)
    c = 0
    for action in population[0].performed_actions:
        action(rappresentationX, population[0].performed_selection[c])
        c += 1
    err = error_rate(demo_pairs[i2].y, rappresentationX.rappToGrid())
    actions = copy.deepcopy(population[0].performed_actions)
    selections = copy.deepcopy(population[0].performed_selection)
    return PossibleSolution(i1, i2, actions, selections, err)

#svolgo le operazioni su tutte le combinazioni degli esempi ricevuti
def generate_representation(rep, demo_pairs, act):
    possibleSolution = list()
    errTot = 0
    errMin = 1000
    indMin = 0
    for x in range(0, len(demo_pairs)):
        for y in range(0, len(demo_pairs)):
            if x != y:
                possibleSolution.append(generate_representation_solution(rep, demo_pairs, act, x, y))
                errTot += possibleSolution[-1].err
                if possibleSolution[-1].err < errMin:
                    errMin = possibleSolution[-1].err
                    indMin = len(possibleSolution) - 1
    return PossibleSolutionRepresentation(rep, possibleSolution, errTot, errMin, indMin)

#Classe in cui cerco la serie di azioni necessarie a risolvere il problema con un algoritmo evolutivo: addestro su esempio 1 e valido su esempio 2 e poi faccio viceversa
class Agent(ArcAgent):
    def predict(self, demo_pairs: List[ArcIOPair], test_grids: List[ArcGrid]) -> List[ArcPrediction]:
        actionsPR = [pixelRepresentation.movePixel, pixelRepresentation.changeColorPixel, pixelRepresentation.removePixel, pixelRepresentation.duplicateNearPixel, pixelRepresentation.expandGrid, pixelRepresentation.reduceGrid]
        actionsRR = [rowRepresentation.moveRiga, rowRepresentation.changeColorRiga, rowRepresentation.modifyRigaAdd, rowRepresentation.modifyRigaDel, rowRepresentation.modifyRigaMove, rowRepresentation.expandGrid, rowRepresentation.reduceGrid]
        actionsCR = [columnsRepresentation.moveColonna, columnsRepresentation.changeColorColonna, columnsRepresentation.modifyColonnaAdd, columnsRepresentation.modifyColonnaDel, columnsRepresentation.modifyColonnaMove, columnsRepresentation.expandGrid, columnsRepresentation.reduceGrid]
        actionsCLR = [colorLayerRepresentation.moveLayer, colorLayerRepresentation.layerUnion, colorLayerRepresentation.delPixelLayer, colorLayerRepresentation.addPixelLayer, colorLayerRepresentation.expandGrid, colorLayerRepresentation.reduceGrid]
        actionsRER = [rectangleRepresentation.moveRectangle, rectangleRepresentation.changeColorRectangle, rectangleRepresentation.removeRectangle, rectangleRepresentation.duplicateNearRectangle, rectangleRepresentation.changeOrder, rectangleRepresentation.scaleUpRectangle, rectangleRepresentation.scaleDownRectangle, rectangleRepresentation.expandGrid, rectangleRepresentation.reduceGrid]
        actionsFR = [figureRepresentation.moveFigure, figureRepresentation.changeColorFigure, figureRepresentation.equalColorFigure, figureRepresentation.addElementFigure, figureRepresentation.removeElementFigure, figureRepresentation.mergeFigure, figureRepresentation.divideFigure, figureRepresentation.changeOrder, figureRepresentation.expandGrid, figureRepresentation.reduceGrid]
        actionsBR = [borderRepresentation.moveFigure, borderRepresentation.changeColorBorder, borderRepresentation.changeColorCenter, borderRepresentation.modifyBorderFigure, borderRepresentation.expandGrid, borderRepresentation.reduceGrid]

        possibleSolutionRep = list()

        #possibleSolutionRep.append(generate_representation(pixelRepresentation, demo_pairs, actionsPR))
        #possibleSolutionRep.append(generate_representation(rowRepresentation, demo_pairs, actionsRR))
        #possibleSolutionRep.append(generate_representation(columnsRepresentation, demo_pairs, actionsCR))
        #possibleSolutionRep.append(generate_representation(colorLayerRepresentation, demo_pairs, actionsCLR))
        #possibleSolutionRep.append(generate_representation(rectangleRepresentation, demo_pairs, actionsRER))
        #possibleSolutionRep.append(generate_representation(figureRepresentation, demo_pairs, actionsFR))
        possibleSolutionRep.append(generate_representation(borderRepresentation, demo_pairs, actionsBR))
        #rappresentazionePixelColore
        #rappresentazioneColonneColore
        #rappresentazioneRigheColore
        #rappresentazioneColoreLine
        #rappresentazioneColoreSquare


        #scelgo la miglior soluzione in base all'error rate e la applico alla griglia in input di test
        outputs = []
        possibleSolutionRep.sort(key=lambda i: i.errTot, reverse = False)
        print("Representation 1: " + str(possibleSolutionRep[0].classe))
        print("Tot Error: " + str(possibleSolutionRep[0].errTot))
        print("Min Error: " + str(possibleSolutionRep[0].errMin))
        for x in range(0, len(test_grids)):
            rappInput = possibleSolutionRep[0].classe(copy.deepcopy(test_grids[x]))
            c = 0
            ind = possibleSolutionRep[0].indMin
            for action in possibleSolutionRep[0].list[ind].actions:
                action(rappInput, possibleSolutionRep[0].list[ind].selectors[c])
                c += 1
            outputs.append([rappInput.rappToGrid()])
        return outputs
