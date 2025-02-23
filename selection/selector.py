from dataclasses import dataclass


@dataclass
class Selector:
    index: int
    color: int
    direction: int