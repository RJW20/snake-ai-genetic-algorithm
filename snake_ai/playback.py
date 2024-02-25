import pygame

from snake_app import Grid
from genetic_algorithm import Population
from .player import Player
from .settings import player_args
from .settings import genetic_algorithm_settings
from .settings import playback_settings


##bind settings to variables
population_size = genetic_algorithm_settings['population_settings']
total_generations = genetic_algorithm_settings['total_generations']
history_folder = genetic_algorithm_settings['history_folder']
history_type = genetic_algorithm_settings['history_type']
history_value = genetic_algorithm_settings['history_value']
block_width = playback_settings['block_width']
block_padding = playback_settings['block_padding']


def playback() -> None:
    """Show playback of the result of running the genetic algorithm on snake.
    
    Do not alter settings.py between running the genetic algorithm and running this.
    Switch between generations with the left and right arrow keys.
    Speed up or slow down the playback with the j and k keys.
    """

    #initialize the grid the game will be modelled from
    grid = Grid(player_args['grid_size'], block_width, block_padding)

    #pygame setup
    screen = pygame.display.set_mode(grid.board_size)
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    running = True

    #intialize the playback population
    playback_pop = PlaybackPopulation(history_folder, history_type, history_value, population_size, player_args)

    while running:

        exit()
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT():
                running = False
                break

            #handle key presses
            if event.type == pygame.KEYDOWN:
                pass

        #run the snakes

        #draw the snakes

    pygame.quit()


class PlaybackPopulation(Population):
    """Extension of Population class with methods allowing us to manipulate
    which genomes are loaded.

    Will determine its own size and automatically load the first genomes.
    """

    def __init__(self, 
                 history_folder: str,
                 history_type: str, 
                 history_value: int, 
                 og_pop_size: int, 
                 player_args: dict
                 ) -> None:
        
        self.folder = history_folder
        self.current_generation = 1

        self.is_champs = False
        pop_size = og_pop_size
        match(history_type):
            case('none'):
                raise Exception('No history was saved during evolution. If you would like ' + \
                                'to view playback, please adjust history settings and run again.')
            case('champ'):
                pop_size = 1
                self.is_champs = True
            case('absolute'):
                pop_size = history_value
            case('percentage'):
                pop_size = int(og_pop_size * history_value)
            case _:
                raise Exception(f'Invalid history type {history_type}')
        self.size = pop_size
        self.players = [Player(**player_args) for _ in range(pop_size)]

        if self.is_champs:
            self.load(history_folder)
        else:
            self.new_gen()

    def new_gen(self) -> None:
        """Load generation {self.gen_id}."""

        self.load(f'{history_folder}/{self.current_generation}')