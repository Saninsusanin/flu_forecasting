import os

import numpy as np

from multiprocessing import Pool
from source.settings import MODEL, CONFIG
from source.common.commands.model_fitter import FitModel
from source.utils import get_config, get_data, get_regions


def do():
    config = get_config(CONFIG['PATH_TO_CONFIG'])
    command = 'fit_model'
    fit_config = config[command]
    diseases = fit_config['diseases']
    ages = fit_config['ages']
    data = get_data(config, command)
    regions = get_regions(fit_config, data)
    prefix = CONFIG['PATH_TO_OUTPUT'] + os.sep + 'models' + os.sep
    last_date = np.unique(list(zip(data['YEAR'], data['WEEK'])), axis=0)[-1]

    model_fitter = FitModel(data=data, prefix=prefix, last_date=last_date)
    models_params = [(region, disease, age) for region in regions for disease in diseases for age in ages]

    with Pool(MODEL['NUMBER_OF_PROCESSES']) as p:
        p.map(model_fitter.fit_model, models_params)
