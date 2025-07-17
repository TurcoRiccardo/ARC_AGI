import numpy as np
import copy
from selection.selector import Selector, generateNewSelector_new, mutateSelector
from dataclasses import dataclass


@dataclass
class Individual:
    genome: list
    performed_selection: list
    performed_actions: list
    fitness: tuple = (None, 0)

#For parent selection we use Tournament Selection
def tournament_selection(population):
    candidates = sorted(np.random.choice(population, 2), key=lambda e: e.fitness, reverse = True)
    return candidates[0]

#For parent selection we use lexicase selection
def lexicase_selection(population):
    candidates = population.copy()
    test_cases = list(range(len(population[0].genome)))
    np.random.shuffle(test_cases)
    for test in test_cases:
        # Trova il miglior punteggio su questo test
        best_score = max([ind.fitness[0][test] for ind in candidates])
        # Filtra solo quelli col punteggio migliore su questo test
        candidates = [ind for ind in candidates if ind.fitness[0][test] == best_score]
        if len(candidates) == 1:
            return candidates[0]
    # Se alla fine ce ne sono ancora più di uno, ne sceglie uno a caso
    return np.random.choice(candidates)

#add a new action to the parent generating a new individual
def add_mutation(p: Individual, available_actions):
    new_gen = copy.deepcopy(p.genome)
    for _ in range(0, 5):
        #take a random action
        x = np.random.randint(0, len(available_actions))
        action = available_actions[x]
        #generate a new selector ------------> da vedere come generare il selettore
        s = generateNewSelector_new(p.genome)
        #execute the action with the selector
        r = 0
        for c in range(0, len(p.genome)):
            sas = action(new_gen[c], s)
            if sas == None:
                print("errore")
                print(action)
            r += int(sas)
        if r < len(p.genome):
            break
    if r == len(p.genome):
        return None
    new_selection = p.performed_selection.copy()
    new_selection.append(s)
    new_paction = p.performed_actions.copy()
    new_paction.append(action)
    return Individual(new_gen, new_selection, new_paction)

#improve the list of actions by tweaking the selector of a given action of the parent generating a new individual
def tweak_mutation(p: Individual, available_actions, initial_representation):
    if len(p.performed_actions) == 0:
        return add_mutation(p, available_actions)
    new_gen = []
    for i in range(0, len(initial_representation)):
        new_gen.append(copy.deepcopy(initial_representation[i]))
    new_paction = []
    new_selection = []
    x = np.random.randint(0, len(p.performed_actions))
    for i, (action, selector) in enumerate(zip(p.performed_actions, p.performed_selection)):
        if i == x:
            new_selector = mutateSelector(selector)
        else:
            new_selector = copy.deepcopy(selector)
        for c in range(0, len(new_gen)):
            action(new_gen[c], new_selector)
        new_paction.append(action)
        new_selection.append(new_selector)
    return Individual(new_gen, new_selection, new_paction)

#change the order of the list of actions of the parent generating a new individual
def swap_mutation(p: Individual, available_actions, initial_representation):
    if len(p.performed_actions) <= 1:
        return add_mutation(p, available_actions)
    new_gen = []
    for i in range(0, len(initial_representation)):
        new_gen.append(copy.deepcopy(initial_representation[i]))
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
        for c in range(0, len(new_gen)):
            action(new_gen[c], selector)
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
class ProblemConsideration:
    countDim: int
    countColor: int
    countRemove: int
    countAdd: int
    numProb: int

#initial analysis in which we observe the characteristics of the problem
def initial_analysis(demo_pairs):
    pc = ProblemConsideration(0, 0, 0, 0, len(demo_pairs))
    for i in range(0, len(demo_pairs)):
        colorListInput = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        colorListOutput = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for x in range(0, demo_pairs[i].x.shape[0]):
            for y in range(0, demo_pairs[i].x.shape[1]):
                colorListInput[demo_pairs[i].x[x][y]] += 1
        for x in range(0, demo_pairs[i].y.shape[0]):
            for y in range(0, demo_pairs[i].y.shape[1]):
                colorListOutput[demo_pairs[i].y[x][y]] += 1
        #guardo dimensione griglia
        if demo_pairs[i].x.shape[0] == demo_pairs[i].y.shape[0] and demo_pairs[i].x.shape[1] == demo_pairs[i].y.shape[1]:
            pc.countDim += 1
        #guardo colore
        ok = 0
        for c in range(1, 10):
            if colorListInput[c] != colorListOutput[c]:
                ok = 1
        if ok == 0:
            pc.countColor += 1
        #guardo aggiunta nuovi pixel
        if colorListInput[0] > colorListOutput[0]:
            #aggiunta
            pc.countAdd += 1
        elif colorListInput[0] < colorListOutput[0]:
            #rimozione 
            pc.countRemove += 1
    return pc

#algoritmo multi-obiettivo a dominanza di Pareto con ordinamento per fronti di non-dominanza e crowding distance
class NSGA2Sorter:
    def dominates(self, ind1, ind2):
        better_in_any = False
        for s1, s2 in zip(ind1.fitness[0], ind2.fitness[0]):
            if s1 < s2:
                return False  # ind1 è peggiore in almeno un obiettivo
            elif s1 > s2:
                better_in_any = True
        return better_in_any

    def fast_non_dominated_sort(self, population):
        fronts = [[]]
        domination_counts = {}
        dominated_solutions = {}
        # Mappo id -> individuo per recuperarlo facilmente
        id_to_individual = {id(ind): ind for ind in population}
        for p in population:
            indp = id(p)
            dominated_solutions[indp] = []
            domination_counts[indp] = 0
            for q in population:
                indq = id(q)
                if indp == indq:
                    continue
                if self.dominates(p, q):
                    dominated_solutions[indp].append(indq)
                elif self.dominates(q, p):
                    domination_counts[indp] += 1
            if domination_counts[indp] == 0:
                fronts[0].append(p)
        i = 0
        while len(fronts[i]) > 0:
            next_front = []
            for p in fronts[i]:
                indp = id(p)
                for indq in dominated_solutions[indp]:
                    domination_counts[indq] -= 1
                    if domination_counts[indq] == 0:
                        next_front.append(id_to_individual[indq])
            i += 1
            fronts.append(next_front)
        fronts.pop()  # l'ultimo è vuoto
        return fronts

    def calculate_crowding_distance(self, front):
        if len(front) == 0:
            return {}
        elif len(front) == 1:
            return {id(front[0]): float('inf')}
        num_objectives = len(front[0].fitness[0])
        distance = {id(ind): 0 for ind in front}
        for m in range(num_objectives):
            front.sort(key=lambda ind: ind.fitness[0][m], reverse=True)
            fmax = front[0].fitness[0][m]
            fmin = front[-1].fitness[0][m]
            distance[id(front[0])] = float('inf')
            distance[id(front[-1])] = float('inf')
            for i in range(1, len(front) - 1):
                prev_f = front[i - 1].fitness[0][m]
                next_f = front[i + 1].fitness[0][m]
                if fmax != fmin:
                    distance[id(front[i])] += (next_f - prev_f) / (fmax - fmin)
        return distance

    def sort_population(self, population):
        fronts = self.fast_non_dominated_sort(population)
        sorted_population = []
        for front in fronts:
            if len(front) == 0:
                continue
            distance = self.calculate_crowding_distance(front)
            front.sort(key=lambda ind: distance[id(ind)], reverse=True)
            sorted_population.extend(front)
        return sorted_population
