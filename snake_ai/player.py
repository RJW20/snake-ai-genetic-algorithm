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

    def __getstate__(self) -> dict:
        """Return a dictionary containing attribute names and their values as (key, value) pairs.
        
        All values must also be pickleable i.e. not use __slots__ or have __getstate__ and __setstate__ methods like this.
        If this class uses __slots__ or extends one that does this must be changed.
        """

        return self.__dict__

    def __setstate__(self, d: dict) -> BasePlayer:
        """Load the attributes in the dictionary d into self.
        
        If this class uses __slots__ or extends one that does this must be changed.
        """

        self.__dict__ = d

    def empty_clone(self) -> BasePlayer:
        """Return a new instance of self's class without a genome."""
        pass