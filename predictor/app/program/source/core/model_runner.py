import numpy as np

from copy import deepcopy
from sklearn.pipeline import Pipeline
from source.settings import CONFIG, MODEL
from source.utils import get_config, get_model
from source.core.transformers import RegressionFeaturePreparator


def get_pipeline():
    return Pipeline([('regression_feature_generator',
                      RegressionFeaturePreparator(
                          number_of_measurements=MODEL['NUMBER_OF_MEASUREMENTS']))
                     ])


class ModelRunner:
    def __init__(self, time_series, last_date):
        self.command = 'fit_model'
        self.time_series = time_series
        self.config = get_config(CONFIG['PATH_TO_CONFIG'])
        pipeline = get_pipeline()
        self.features, self.target = pipeline.transform(self.time_series)
        self.model = get_model()
        self.last_date = last_date

    def fit(self):
        self.model.fit(self.features, self.target)

    def predict(self):
        self.config = get_config(CONFIG['PATH_TO_CONFIG'])

        predictions = []
        current_features = deepcopy(self.time_series[-MODEL['NUMBER_OF_MEASUREMENTS']:])

        for i in range(self.config['predict']['length_of_prediction_interval']):
            predictions.append(self.model.predict(np.array([current_features]))[0])
            current_features[:-1] = current_features[1:]
            current_features[-1] = predictions[-1]

        return [int(prediction) + 1 for prediction in predictions]

    def get_last_date(self):
        return self.last_date
