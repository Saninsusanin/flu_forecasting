import os
import json

import pandas as pd

from source.settings import CONFIG
from sklearn.pipeline import Pipeline
from source.core.transformers import RegionStatistics


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
