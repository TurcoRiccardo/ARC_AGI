import numpy as np
from matplotlib import pyplot as plt
from arc import train_problems, validation_problems, ArcProblem, plot_grid, describe_task_group
from arc.types import verify_is_arc_grid, ArcIOPair, ArcGrid, ArcPrediction
from arc.agents import ArcAgent
from arc.evaluation import evaluate_agent
from agent import Agent
from tqdm.auto import tqdm
from argparse import ArgumentParser


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

def main(args):
    describe_task_group(train_problems)
    c = 0
    tsc = 0
    avg = 0
    #apply the agent to every problem in the loop
    for numprob in tqdm(range(args.min, args.max)):
        prob : ArcProblem = train_problems[numprob]

        #visualizzo il problema prob in esame
        if args.show_train_pairs != False:
            for i, pair in enumerate(prob.train_pairs, start=1):
                pair.plot(show=True, title=f"Task {numprob}: Demo {i}")
        if args.show_test_pairs == True:
            for i, pair in enumerate(prob.test_pairs, start=1):
                pair.plot(show=True, title=f"Task {numprob}: Test {i}")
            print(f"\nTrain problem number {numprob}")

        #trovo una soluzione outs
        agent = Agent()
        outs = agent.predict(prob.train_pairs, prob.test_inputs)

        i = 1
        #visualizzo soluzione del nostro agent
        for test_pair, predictions in zip(prob.test_pairs, outs):
            for p in predictions:
                prediction = ArcIOPair(test_pair.x, p)
                err = error_rate(test_pair.y, p)
                avg += err
                print("Error on the test: " + str(err))
                if err == 0:
                    tsc += 1
                if args.show_solution == True:
                    prediction.plot(show=True, title=f"Task {numprob}: Solution {i}")
            i += 1
        c += 1
    #statistiche sul test set
    print("number of tasks executed: " + str(c))
    print("Average error per task: " + str(avg/c))
    print("Number of Task solved correctly: " + str(tsc))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--min', type=int, default=0) #the program execute the problem from min to max on the test dataset
    parser.add_argument('--max', type=int, default=400)
    parser.add_argument('--show_test_pairs', default=True)
    parser.add_argument('--show_solution', default=True)
    parser.add_argument('--show_train_pairs', default=False)
    main(parser.parse_args())

#python test.py --min 0 --max 10 --show_test_pairs "false" --show_solution "false" --show_train_pairs "true"