import pygame

from snake_app import Grid
from genetic_algorithm import Population
from .player import Player
from .settings import player_args
from .settings import genetic_algorithm_settings
from .settings import playback_settings


##bind settings to variables
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
    dt = 0

    #intialize the population

    #load gen 1's history


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
