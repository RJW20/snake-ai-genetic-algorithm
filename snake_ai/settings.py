player_args = {

    #grid properties
    'grid_size': (30, 30),  #(width, height)

    #snake properties
    'length': 3     #note will be set to min(grid_size)//2 if larger than that to prevent some of the body starting outside the grid

}


genetic_algorithm_settings = {

    #population properties
    'population_size': 1000,        #number of players in the population
    'creation_type': 'new',         #options are ['new', 'load']
    'load_folder': 'latest_genomes',           #folder to load from if applicable
    'save_folder': 'latest_genomes',              #folder to save to
    'total_generations': 500,       #number of generations to run to

    #genome properties
    'structure': ((24, ), (16, 'sigmoid'), (3, 'softmax')),    #options for activation are ['sigmoid', 'relu', 'softmax', 'linear']

    #evolution properties
    'parent_percentage': 0.2,       #percentage of parents to repopulate the next generation from
    'crossover_type': 'one-point',  #options are ['one-point', 'uniform']
    'mutation_type': 'gaussian',    #options are ['gaussian', 'uniform']
    'mutation_rate': 0.05,          #probability a gene will mutate

}


simulation_settings = {

}


playback_settings = {

    #grid properties
    'block_width': 20,
    'block_padding': 1,

}