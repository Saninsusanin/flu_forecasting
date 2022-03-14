from math import fabs
from xgboost import XGBRegressor
from source.settings import CONFIG
from source.utils import get_data, get_config
from source.core.transformers import TrainTestSplit
from sklearn.metrics import mean_absolute_percentage_error


class Fitness:
    config = get_config(CONFIG['PATH_TO_CONFIG'])
    data = get_data(config, 'select_features')
    model = XGBRegressor(n_jobs=-1, booster='gblinear')
    train_matrix, train_target, test_matrix, test_target = \
        TrainTestSplit(percentage=config['select_features']['percentage']).\
            transform((data[data.columns.difference([config['select_features']['target_column_name']])].to_numpy(),
                       data[config['select_features']['target_column_name']].to_numpy().reshape(-1)))

    def __call__(self, feature_indices):
        current_train_matrix = self.train_matrix[:, feature_indices]
        current_train_target = self.train_target
        current_test_matrix = self.test_matrix[:, feature_indices]
        current_test_target = self.test_target
        self.model.fit(current_train_matrix, current_train_target)
        predictions = self.model.predict(current_test_matrix)

        return mean_absolute_percentage_error(current_test_target, predictions)

    def get_weights(self, feature_indices):
        current_train_matrix = self.train_matrix[:, feature_indices]
        current_train_target = self.train_target
        self.model.fit(current_train_matrix, current_train_target)
        weights = [fabs(weight) for weight in self.model.coef_]
        denominator = sum(weights)
        weights = [weight / denominator for weight in weights]

        return weights
