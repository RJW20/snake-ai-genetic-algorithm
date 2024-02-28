from copy import deepcopy

import numpy as np

from snake_app import Snake
from genetic_algorithm import BasePlayer
from snake_app.cartesian import Point, Slope, Direction
from .vision import Vision


class Player(Snake, BasePlayer):
    """Player existing in the game with a Genome to control its movements."""

    def __init__(self, **kwargs) -> None:
        super(Player, self).__init__(**kwargs)
        self.score = 0
        self.fitness = 0
        self.best_score = 0
        self.vision: np.ndarray = np.zeros(24)

    def look_in_direction(self, direction: Slope) -> tuple[bool, Vision]:
        """Return the distance to walls, food and own body in the given direction.
        
        Also return a bool indicating if food is in that direction so we know to stop searching for it.
        """

    def look(self) -> None:
        """Set the snakes vision.
        
        Can see in 8 directions around the snake (cardinal and ordinal compass points).
        """

    def think(self) -> str:
        """Feed the input into the Genome and turn the output into a valid move."""

        genome_input = np.concatenate((np.array([1.0/distance for _, distance in vars(self.vision.walls).items()]),
                                       np.array([1.0/distance for _, distance in vars(self.vision.food).items()]),
                                       np.array([1.0/distance for _, distance in vars(self.vision.body).items()])))
        genome_output = self.genome.propagate(genome_input)

        #turn output into move
        match(np.argmax(genome_output)):
            case 0:
                move = 'forward'
            case 1:
                move = 'right'
            case 2:
                move = 'left'
        
        return move
    
    def __getstate__(self) -> dict:
        """Return a dictionary containing attribute names and their values as (key, value) pairs.
        
        All values must also be pickleable i.e. not use __slots__ or have __getstate__ and __setstate__ methods like this.
        If this class uses __slots__ or extends one that does this must be changed.
        """

        d = dict()

        d['grid_size'] = self.grid_size
        d['start_length'] = self.start_length
        d['body'] = self.body
        d['direcion'] = self.direction
        d['target'] = self.target
        d['vision'] = self.vision

        d['score'] = self.score
        d['fitness'] = self.fitness
        d['best_score'] = self.best_score
        d['genome'] = self.genome

        return d

    def __setstate__(self, d: dict) -> BasePlayer:
        """Load the attributes in the dictionary d into self.
        
        If this class uses __slots__ or extends one that does this must be changed.
        """

        self.grid_size = d['grid_size']
        self.start_length = d['start_length']
        self.body = d['body']
        self.direction = d['direcion']
        self.target = d['target']
        self.vision = d['vision']

        self.score = d['score']
        self.fitness = d['fitness']
        self.best_score = d['best_score']
        self.genome = d['genome']

    def empty_clone(self) -> BasePlayer:
        """Return a new instance of self's class without a genome."""

        clone = deepcopy(self)
        clone.fitness = 0
        clone.best_score = 0
        clone.genome = None

        return clone