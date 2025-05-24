import numpy as np
from matplotlib import pyplot as plt
from arc import train_problems, validation_problems, ArcProblem, plot_grid, describe_task_group
from arc.types import verify_is_arc_grid, ArcIOPair, ArcGrid, ArcPrediction
from arc.agents import ArcAgent
from arc.evaluation import evaluate_agent
from agent import Agent
from tqdm.auto import tqdm
from argparse import ArgumentParser
from utility import error_rate


def main(args):
    describe_task_group(train_problems)
    c = 0
    tsc = 0
    avg = 0
    #apply the agent to every problem in the loop
    for numprob in tqdm(range(args.min, args.max)):
        prob : ArcProblem = train_problems[numprob]

        #visualizzo il problema prob in esame
        print("Problem number: " + str(numprob))
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

#Correctly solved problems: 1, 3, 9