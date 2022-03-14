import os

import numpy as np
import pandas as pd

from source.settings import CONFIG
from source.utils import get_config
from source.core.fitness.model_based_fitness import Fitness
from source.core.feature_selectors.greedy_add import greedy_add
from source.core.feature_selectors.brute_force import brute_force


def do():
    fitness = Fitness()
    config = get_config(CONFIG['PATH_TO_CONFIG'])
    columns = np.array(config['select_features']['features'])

    path_to_output = CONFIG['PATH_TO_OUTPUT'] + os.sep + 'selected_features' + \
                     os.sep + config['select_features']['most_valuable_features_filename']
    if config['select_features']['method'] == 'brute_force':
        method = brute_force
    elif config['select_features']['method'] == 'greedy_add':
        method = greedy_add
    else:
        method = greedy_add

    best_combination = method(len(columns), fitness)
    weights = fitness.get_weights(best_combination)
    dataframe_dict = dict(FEATURES=columns[tuple([best_combination])], WEIGHTS=weights)
    dataframe = pd.DataFrame.from_dict(dataframe_dict).sort_values(['WEIGHTS'], ascending=[False])
    dataframe.to_csv(path_to_output + '.csv', index=False)
