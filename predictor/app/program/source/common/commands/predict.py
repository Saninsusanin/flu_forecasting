import os
import sys

import numpy as np
import pandas as pd

from pickle import load
from copy import deepcopy
from multiprocessing import Pool
from collections import defaultdict
from source.settings import CONFIG, MODEL
from source.common.commands.model_fitter import FitModel
from source.utils import get_config, get_models_to_fit, check_input, get_regions, get_data


def get_new_timestamps(last_date, config):
    current_date = last_date
    new_timestamps = []

    for _ in range(config['predict']['length_of_prediction_interval']):
        if current_date[1] == 52:
            current_date[0] += 1
            current_date[1] = 1
        else:
            current_date[1] += 1

        new_timestamps.append(deepcopy(current_date))

    return np.array(new_timestamps)


def task(data):
    region, disease, age = data
    path_to_model = CONFIG['PATH_TO_OUTPUT'] + os.sep + 'models' + os.sep + '#'.join(data) + '.model'

    with open(path_to_model, 'rb') as source:
        runner = load(source)
        predictions = runner.predict()

    return disease, age, predictions


def do():
    config = get_config(CONFIG['PATH_TO_CONFIG'])
    command = 'predict'
    predict_config = config[command]
    diseases = predict_config['diseases']
    ages = predict_config['ages']
    data = get_data(config, 'fit_model')
    regions = get_regions(predict_config, data)
    prefix = CONFIG['PATH_TO_OUTPUT'] + os.sep + 'models' + os.sep
    last_date = np.unique(list(zip(data['YEAR'], data['WEEK'])), axis=0)[-1]
    models_params = [(region, disease, age) for region in regions for disease in diseases for age in ages]
    models_to_fit = get_models_to_fit(models_params)

    if len(models_to_fit) > 0:

        if check_input('fit_model'):
            model_fitter = FitModel(data=data, prefix=prefix, last_date=last_date)

            with Pool(MODEL['NUMBER_OF_PROCESSES']) as p:
                p.map(model_fitter.fit_model, models_to_fit)

        else:
            sys.stderr.write(f"ERROR: you have to add data. "
                             f"Can't find these files: {' '.join(config['fit_model']['input'])}")
            exit(1)

    model_prefix = CONFIG['PATH_TO_OUTPUT'] + os.sep + 'models'
    dataframe_dict = defaultdict(list)

    path_to_model = model_prefix + os.sep + '#'.join(models_params[0]) + '.model'

    with open(path_to_model, 'rb') as source:
        runner = load(source)
        new_timestamps = get_new_timestamps(runner.get_last_date(), config)
        years = new_timestamps[:, 0].tolist()
        weeks = new_timestamps[:, 1].tolist()

    for region in regions:
        dataframe_dict['REGION_NAME'] += [region] * config['predict']['length_of_prediction_interval']
        dataframe_dict['WEEK'] += weeks
        dataframe_dict['YEAR'] += years

    with Pool(MODEL['NUMBER_OF_PROCESSES']) as p:
        result = p.map(task, models_params)

    for disease, age, predictions in result:
        dataframe_dict[f'{disease}_{age}'] += predictions

    path_to_output = CONFIG['PATH_TO_OUTPUT'] + os.sep + 'predictions' + os.sep + config['predict']['values_filename']
    dataframe = pd.DataFrame.from_dict(dataframe_dict).sort_values(['YEAR', 'WEEK'], ascending=[True, True])
    dataframe.to_csv(path_to_output + '.csv', index=False)
