from math import ceil
from itertools import combinations
from source.settings import CONFIG
from source.utils import get_config


def brute_force(number_of_features, fitness):
    config = get_config(CONFIG['PATH_TO_CONFIG'])
    features_ids = list(range(number_of_features))
    best_fitness = None
    best_combination = None

    for current_number_of_features in range(1, ceil(config['select_features']['percent_of_features'] * number_of_features) + 1):
        for current_combination in combinations(features_ids, current_number_of_features):
            current_fitness = fitness(current_combination)

            if best_fitness is None or current_fitness < best_fitness:
                best_fitness = current_fitness
                best_combination = current_combination

    return best_combination
