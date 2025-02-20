import numpy as np
from matplotlib import pyplot as plt
from arc import train_problems, validation_problems, ArcProblem, plot_grid, describe_task_group
from arc.types import verify_is_arc_grid, ArcIOPair, ArcGrid, ArcPrediction
from arc.agents import ArcAgent
from arc.evaluation import evaluate_agent
from agent import Agent


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

        #trovo una soluzione outs
        agent = Agent()
        outs = agent.predict(prob.train_pairs, prob.test_inputs)

        #visualizzo soluzione del nostro agent
        for test_pair, predicitons in zip(prob.test_pairs, outs):
            for p in predicitons:
                prediction = ArcIOPair(test_pair.x, p)
                prediction.plot(show=True, title=f"Task {numprob}: Solution {1}")
