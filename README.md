# ARC_AGI
My personal solution for ARK_AGI benchmark (https://arcprize.org/)
- official repo: https://github.com/fchollet/ARC-AGI

## Packages
- representation: contains the possible representations of the grid.


## Requirements
- numpy
- matplotlib
- arc-py: (https://github.com/ikamensh/arc-py) Used to convert the original .json files to numpy arrays, view them with matplotlib.

## Description
The ARC-AGI (Abstraction and Reasoning Corpus - Artificial General Intelligence) benchmark is a dataset created by François Chollet to test AI's ability for abstract reasoning. It consists of a series of tasks based on colored grids, where the AI must infer rules and transformations from a few examples without explicit instructions.
ARC is designed to assess human-like cognitive skills such as generalization, analogy, and pattern recognition, posing a challenge for traditional machine learning models. The benchmark is considered a key test for measuring progress toward Artificial General Intelligence (AGI).

### Grid dimension
A grid can have any height or width between 1x1 and 30x30 inclusive (average height is 9 and average width is 10).

### List of Colors
- 0: Black
- 1: Blue
- 2: Red
- 3: Green
- 4: Yellow
- 5: Cyan
- 6: Magenta
- 7: Grey
- 8: Brown
- 9: Orange
