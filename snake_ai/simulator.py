from .player import Player
from .settings import simulation_settings


def calculate_fitness(left_count: int, right_count: int, forward_count: int, total_score: int, longest_edge: int, lifespan: int) -> float:
    """Return a value determining how 'good' a player is.
    
    This will be a function of stats.
    """

    '''
    #blackist any players that are only turning in one direction
    if min(left_count, right_count, forward_count) == 0:
        return .0
    
    age = left_count + right_count + forward_count
    adjusted_age = age // ((longest_edge / 10) * lifespan)
    adjusted_score = total_score / lifespan

    fitness = adjusted_age + ((2**adjusted_score) + (adjusted_score**2.1)*500) - (((.25 * adjusted_age)**1.3) * (adjusted_score**1.2))
    
    #blacklist any players doing too badly
    fitness = max(fitness, .0)
    
    return fitness
    '''

    return .1


def simulate(player: Player) -> Player:
    """Assign the player its fitness.
    
    Run the player in its environment dependent on simulation_settings.
    Collect stats and then calculate the fitness of the player and assign it.
    """

    player.start_state()

    left_count = right_count = forward_count = total_score = 0
    longest_edge = max(player.grid_size)
    best_score = 0

    lifespan = simulation_settings['lifespan']
    deaths = 0
    time_since_eaten = 0
    current_length = player.length
    while deaths < lifespan:

        player.look()
        move = player.think()
        player.move(move)

        #edit move counters
        match(move):
            case 'left':
                left_count += 1
            case 'right':
                right_count += 1
            case 'forward':
                forward_count += 1

        #increase time_since_eaten
        if player.length == current_length:
            time_since_eaten += 1
        else:
            time_since_eaten = 0
            current_length = player.length
        
        #restart if needed
        M = max(6, min(player.length, longest_edge))   #variable for determining progress     
        if player.is_dead or time_since_eaten == M * longest_edge:
            deaths += 1
            score = player.length - player.start_length
            best_score = max(best_score, score)
            total_score += score
            if deaths < lifespan:
                player.start_state()
                current_length = player.length
                time_since_eaten = 0
        
    player.best_score = best_score

    player.fitness = calculate_fitness(left_count=left_count, right_count=right_count, forward_count=forward_count, total_score=total_score, longest_edge=longest_edge, lifespan=lifespan)
    return player


