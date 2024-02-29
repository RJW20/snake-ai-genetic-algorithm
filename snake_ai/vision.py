from dataclasses import dataclass
from typing import Generator

import numpy as np

from snake_app.cartesian import Slope, Direction


@dataclass
class Vision:
    """Object that holds the snakes vision in one direction."""

    wall: float
    food: float
    body: float

    def to_ndarray(self) -> np.ndarray[float]:
        return np.array([self.wall, self.food, self.body])


def rotations(forward_direction: Direction) -> Generator[Slope, None, None]:
    """Generator that yields the search directions in clockwise order around the 
    direction the snake is heading.
    """

    slope = forward_direction.value
    for _ in range(4):
        yield slope
        yield Slope(slope.run - slope.rise, slope.run + slope.rise)
        slope = Slope(-slope.rise, slope.run)


def relative_direction(forward_direction: Direction, other_direction: Direction) -> np.ndarray[int]:
    """Return an 4 entry int ndarray representing the relative direction of other to forward.
    
    Returned array indicates whether other is [forward, right, backward, left] compared to forward_direcion.
    """

    values = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
    output = np.zeros(4)

    output[(values[other_direction.name] - values[forward_direction.name]) % 4] = 1

    return output