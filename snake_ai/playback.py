import pygame

from snake_app import Grid
from genetic_algorithm import Population
from .player import Player
from .settings import player_args
from .settings import genetic_algorithm_settings
from .settings import playback_settings


##bind settings to variables
population_size = genetic_algorithm_settings['population_size']
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
    speed = 5
    running = True

    #intialize the playback population
    playback_pop = PlaybackPopulation(history_folder=history_folder, 
                                      history_type=history_type,
                                      history_value=history_value, 
                                      og_pop_size=population_size,
                                      total_generations=total_generations,
                                      player_args=player_args)
    
    #select the first snakes
    snakes = playback_pop.current_players
    for snake in snakes:
        snake.start_state()

    while running:
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            #handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    playback_pop.current_generation = min(playback_pop.current_generation + 1, total_generations)
                elif event.key == pygame.K_LEFT:
                    playback_pop.current_generation = max(playback_pop.current_generation - 1, 1)

                if not playback_pop.is_champs:
                    playback_pop.new_gen()

                snakes = playback_pop.current_players
                for snake in snakes:
                    snake.start_state()

        #move all snakes
        for snake in snakes:
            snake.look()
            move = snake.think()
            snake.move(move)

            #remove any that have died
            if snake.is_dead:
                snakes.remove(snake)

        #restart them if all are dead
        if len(snakes) == 0:
            snakes = playback_pop.current_players
            for snake in snakes:
                snake.start_state()

        #fill the screen to wipe last frame
        screen.fill((40,40,40))

        #draw the snakes and their foods
        for snake in snakes:
            pygame.draw.rect(screen, 'red', pygame.Rect(grid.gridpoint_to_coordinates(snake.target.position), (grid.block_width, grid.block_width)))
            for pos in snake.body:
                pygame.draw.rect(screen, 'green', pygame.Rect(grid.gridpoint_to_coordinates(pos), (grid.block_width, grid.block_width)))
                    
        #display the changes
        pygame.display.flip()
        
        #advance to next frame at chosen speed
        clock.tick(speed) / 1000

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
                 total_generations: int,
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
                pop_size = total_generations
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
            self.load(history_folder)   #load all champs
        else:
            self.new_gen()              #load just the first gen

    def new_gen(self) -> None:
        """Load generation {self.current_generation}.
        
        Change self.current_generation to the desired value before calling.
        """

        self.load(f'{history_folder}/{self.current_generation}')

    @property
    def current_players(self) -> list[Player]:
        """Return the players we're currently playing back."""

        if self.is_champs:
            return [self.players[self.current_generation]]
        else:
            return self.players