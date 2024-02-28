from dataclasses import dataclass


@dataclass
class Vision:
    """Object that holds the snakes vision in one direction."""

    wall: float
    food: float
    body: float