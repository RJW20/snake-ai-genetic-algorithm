from dataclasses import dataclass
from typing import Generator

from snake_app.cartesian import Slope, Direction


@dataclass
class Vision:
    """Object that holds the snakes vision in one direction."""

    wall: float
    food: float
    body: float


def rotations(forward_direction: Direction) -> Generator[Slope, None, None]:
    """Generator that yields the search directions in clockwise order around the 
    direction the snake is heading.
    """

    slope = forward_direction.value
    for _ in range(4):
        yield Slope(slope.run - slope.rise, slope.run + slope.rise)
        slope = Slope(-slope.rise, slope.run)
        yield slope