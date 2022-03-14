from source.settings import CONFIG
from source.utils import get_config


def greedy_add(number_of_features, fitness):
    config = get_config(CONFIG['PATH_TO_CONFIG'])
    left_features_ids = set(list(range(number_of_features)))
    best_combination = list()

    while True:
        best_fitness = None
        best_feature = None

        for feature_id in left_features_ids:
            best_combination.append(feature_id)
            current_fitness = fitness(best_combination)

            if best_fitness is None or current_fitness < best_fitness:
                best_feature = feature_id

            best_combination.pop()

        if best_feature is None:
            break

        left_features_ids.remove(best_feature)
        best_combination.append(best_feature)

        if len(best_combination) >= config['select_features']['percent_of_features'] * number_of_features:
            break

    return best_combination
