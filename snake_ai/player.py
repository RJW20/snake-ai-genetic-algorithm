from snake_app import Snake
from genetic_algorithm import BasePlayer

import numpy as np


class Player(Snake, BasePlayer):
    """Player existing in the game with a Genome to control its movements."""

    def __init__(self, **kwargs) -> None:
        super(Player, self).__init__(**kwargs)
        self._fitness = 0
        self._best_score = 0

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
    
    def restart(self, score: int) -> None:
        """Return the state to the beginning of a game."""

        self.length  = self.length - score
        self.start_state()

    def __getstate__(self) -> dict:
        """Return a dictionary containing attribute names and their values as (key, value) pairs.
        
        All values must also be pickleable i.e. not use __slots__ or have __getstate__ and __setstate__ methods like this.
        If this class uses __slots__ or extends one that does this must be changed.
        """

        d = dict()

        d['grid_size'] = self.grid_size
        d['body'] = self.body
        d['length'] = self.length
        d['direcion'] = self.direction
        d['target'] = self.target
        d['vision'] = self.vision

        d['fitness'] = self.fitness
        d['best_score'] = self.best_score
        d['genome'] = self.genome

        return d

    def __setstate__(self, d: dict) -> BasePlayer:
        """Load the attributes in the dictionary d into self.
        
        If this class uses __slots__ or extends one that does this must be changed.
        """

        self.grid_size = d['grid_size']
        self.body = d['body']
        self.length = d['length']
        self.direction = d['direcion']
        self.target = d['target']
        self.vision = d['vision']

        self.fitness = d['fitness']
        self.best_score = d['best_score']
        self.genome = d['genome']

    def empty_clone(self) -> BasePlayer:
        """Return a new instance of self's class without a genome."""
        pass