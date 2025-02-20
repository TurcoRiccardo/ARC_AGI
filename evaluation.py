import numpy as np
from matplotlib import pyplot as plt
from arc import train_problems, validation_problems, ArcProblem, plot_grid, describe_task_group
from arc.types import verify_is_arc_grid, ArcIOPair, ArcGrid, ArcPrediction
from arc.agents import ArcAgent
from arc.evaluation import evaluate_agent
from agent import Agent

if __name__ == '__main__':
    describe_task_group(validation_problems)
    #apply the agent to all the evaluation problem
    agent = Agent()
    results = evaluate_agent(agent)
    print(results)
    assert results.accuracy < 0.5
    assert results.accuracy_any < 0.5
    assert results.shape_accuracy > 0 
