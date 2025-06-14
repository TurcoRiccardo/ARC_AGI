import numpy as np
from matplotlib import pyplot as plt
from arc import train_problems, validation_problems, ArcProblem, plot_grid, describe_task_group
from arc.types import verify_is_arc_grid, ArcIOPair, ArcGrid, ArcPrediction
from arc.agents import ArcAgent
from arc.evaluation import evaluate_agent
from agent import Agent
from agent_new import Agent_new
from argparse import ArgumentParser


def main(args):
    describe_task_group(validation_problems)
    #apply the agent to all the evaluation problem
    if args.new == False:
        agent = Agent()
    else:
        agent = Agent_new(args.parent_selection, args.survival_selection)
    results = evaluate_agent(agent)
    print(results)
    assert results.accuracy < 0.5
    assert results.accuracy_any < 0.5
    assert results.shape_accuracy > 0 

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--new', default=True)
    parser.add_argument('--parent_selection', type=int, default=0) #default 0 -> tournament_selection; 1 -> lexicase_selection
    parser.add_argument('--survival_selection', type=int, default=0) #default 0 -> aggregate fitness; 1 -> NSGA2Sorter
    main(parser.parse_args())