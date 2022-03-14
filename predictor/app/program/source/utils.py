import os
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from source.settings import MODEL, CONFIG
from source.core.transformers import RegionStatistics
from sklearn.linear_model import LinearRegression, HuberRegressor


def get_config(path_to_config):
    with open(path_to_config, 'r') as config_file:
        config = json.load(config_file)

    return config


def get_data(config, command):
    dataframe = None
    pipeline = Pipeline([('region_statistics',
                         RegionStatistics(service_columns=['REGION_NAME',
                                                           'DISTRICT_NAME',
                                                           'LPU_NAME',
                                                           'YEAR',
                                                           'WEEK']))])

    for file_name in config[command]['input']:
        file_extension = file_name.split('.')[-1]
        engine = 'xlrd' if file_extension in ['.xls'] else 'openpyxl'
        path_to_input = CONFIG['PATH_TO_INPUT'] + os.sep + file_name

        if dataframe is None:
            dataframe = pipeline.transform(pd.read_excel(path_to_input, engine=engine))
        else:
            tmp = pipeline.transform(pd.read_excel(path_to_input, engine=engine))
            dataframe = pd.concat((dataframe, tmp[tmp.columns.difference(dataframe.columns)]), axis=1)

    return dataframe


def get_model():
    algorithm = MODEL['BACKBONE']

    if algorithm == 'LinearRegression':
        model = LinearRegression()
    elif algorithm == 'HuberRegressor':
        model = HuberRegressor(max_iter=10000)
    elif algorithm == 'XGBRegressor':
        model = XGBRegressor(n_jobs=-1, n_estimators=30, max_depth=6)
    else:
        model = HuberRegressor(max_iter=10000)

    return model


def get_models_to_fit(models_params):
    models_to_fit = []
    model_names = set([model_params[0] + '#' +
                       model_params[1] + '#' +
                       model_params[2] for model_params in models_params])

    for root, dirs, files in os.walk(CONFIG['PATH_TO_OUTPUT'] + os.sep + 'models'):
        models_to_fit += [model_name.split('#') for model_name in list(model_names.difference(set(files)))]

        return models_to_fit


def check_input(command):
    config = get_config(CONFIG['PATH_TO_CONFIG'])

    for root, dirs, files in os.walk(CONFIG['PATH_TO_INPUT']):
        result = True
        files = set(files)

        for file_name in config[command]['input']:
            result &= file_name in files

        return result


def save_predictions(config, predictions):
    predicted_dict = {'REGION_NAME': [config['fit_model']['region_name']] * len(predictions),
                      f'{config["fit_model"]["disease_name"]}_{config["fit_model"]["age_group"]}': predictions}
    path_to_output = CONFIG['PATH_TO_OUTPUT'] + os.sep + 'predictions' + os.sep + config['predict']['values_filename']
    pd.DataFrame.from_dict(predicted_dict).to_csv(path_to_output, index=False)
    print(f"saved to {path_to_output}")


def get_regions(config, data):
    existing_regions = data['REGION_NAME'].unique()

    if type(config['regions']) is str and config['regions'] == 'all':
        return existing_regions
    else:
        regions = set(config['regions']).intersection(set(existing_regions))

        if len(regions) < len(config['regions']):
            print('check regions parameter in config')
            exit(1)

        return list(regions)


def plot_predictions(config, predictions, previous_values):
    plt.plot(list(range(len(previous_values))), previous_values)
    updated_predictions = np.zeros(len(predictions) + 1)
    updated_predictions[0] = previous_values[-1]
    updated_predictions[1:] = predictions
    plt.plot(list(range(len(previous_values) - 1, len(previous_values) + len(predictions))), updated_predictions)
    plt.legend(['previous_values', 'predictions'])
    plt.title(f'{config["fit_model"]["disease_name"]}_{config["fit_model"]["age_group"]} '
              f'region - {config["fit_model"]["region_name"]}')
    path_to_output = CONFIG['PATH_TO_OUTPUT'] + os.sep + 'predictions' + os.sep + config['predict']['plot_filename']
    plt.savefig(path_to_output)
    print(f'saved to {path_to_output}')
