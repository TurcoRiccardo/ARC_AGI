from dataclasses import dataclass


@dataclass
class Selector:
    index: int
    component: int
    color: int
    direction: int