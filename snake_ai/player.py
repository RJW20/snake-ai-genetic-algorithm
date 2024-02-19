from snake_app import Snake
from genetic_algorithm import BasePlayer

import numpy as np


class Player(Snake, BasePlayer):
    """Player existing in the game with a Genome to control its movements."""

    def __init__(self, **kwargs) -> None:
        super(Player, self).__init__(**kwargs)

    def think(self) -> str:
        """Feed the input into the Genome and turn the output into a valid move."""

        genome_input = np.array()
        for _, vision in vars(self.vision).items():
            np.concatenate(genome_input, np.array([1.0/distance for __, distance in vars(vision).items]))   #use 1/distance so snake can see infinitely
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

        d['_fitness'] = self._fitness
        d['_best_score'] = self._best_score
        d['_genome'] = self._genome

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

        self._fitness = d['_fitness']
        self._best_score = d['_best_score']
        self._genome = d['_genome']

    def empty_clone(self) -> BasePlayer:
        """Return a new instance of self's class without a genome."""
        pass