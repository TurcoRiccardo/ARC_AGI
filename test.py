import numpy as np
from matplotlib import pyplot as plt
from arc import train_problems, validation_problems, ArcProblem, plot_grid, describe_task_group
from arc.types import verify_is_arc_grid, ArcIOPair, ArcGrid, ArcPrediction
from arc.agents import ArcAgent
from arc.evaluation import evaluate_agent
from agent import Agent


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

if __name__ == '__main__':
    describe_task_group(train_problems)
    #apply the agent to every problem in the loop
    for numprob in range(3, 4):
        prob : ArcProblem = train_problems[numprob]

        #visualizzo il problema prob in esame
        #for i, pair in enumerate(prob.train_pairs, start=1):
        #    pair.plot(show=True, title=f"Task {numprob}: Demo {i}")
        for i, pair in enumerate(prob.test_pairs, start=1):
            pair.plot(show=True, title=f"Task {numprob}: Test {i}")
        print(f"\nTrain problem number {numprob}")

        #trovo una soluzione outs
        agent = Agent()
        outs = agent.predict(prob.train_pairs, prob.test_inputs)

        #visualizzo soluzione del nostro agent
        for test_pair, predictions in zip(prob.test_pairs, outs):
            for p in predictions:
                prediction = ArcIOPair(test_pair.x, p)
                print("Error on the test: " + str(error_rate(test_pair.y, p)))
                prediction.plot(show=True, title=f"Task {numprob}: Solution {1}")
