import numpy as np
import pandas as pd

from collections import defaultdict
from sklearn.base import TransformerMixin, BaseEstimator
from statsmodels.nonparametric.smoothers_lowess import lowess


class RegionStatistics(BaseEstimator, TransformerMixin):
    def __init__(self, service_columns):
        self.service_columns = service_columns

    def fit(self, data):
        pass

    def transform(self, dataframe):
        dataframe_dict = defaultdict(list)
        timestamps = np.unique(list(zip(dataframe['YEAR'], dataframe['WEEK'])), axis=0)
        regions = dataframe['REGION_NAME'].unique()

        for year, week in timestamps:
            for region in regions:
                dataframe_dict['YEAR'].append(year)
                dataframe_dict['WEEK'].append(week)
                dataframe_dict['REGION_NAME'].append(region)
                tmp = dataframe[(dataframe['YEAR'] == year) &
                                (dataframe['WEEK'] == week) &
                                (dataframe['REGION_NAME'] == region)][dataframe.columns.difference(self.service_columns)].sum()

                for feature_name in tmp.index:
                    dataframe_dict[feature_name].append(tmp[feature_name])

        return pd.DataFrame.from_dict(dataframe_dict)


class TimeSeriesExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, disease, age, region, smooth):
        self.disease = disease
        self.age = age
        self.region = region
        self.smooth = smooth

    def fit(self, data):
        pass

    def transform(self, feature_dataframe):
        time_series = feature_dataframe[feature_dataframe['REGION_NAME'] == self.region][f'{self.disease}_{self.age}'].to_numpy()
        timestamps = np.unique(list(zip(feature_dataframe['YEAR'], feature_dataframe['WEEK'])), axis=0)

        if self.smooth:
            timestamps = np.array([stamp[0] * 53 + stamp[1] for stamp in timestamps])
            smoothed = lowess(np.array(time_series), timestamps, frac=0.06)
            time_series = smoothed[:, 1]

        return np.array(time_series)


class RegressionFeaturePreparator(BaseEstimator, TransformerMixin):
    def __init__(self, number_of_measurements: int):
        self.number_of_measurements = number_of_measurements

    def fit(self, data):
        pass

    def transform(self, time_series):
        regression_dataframe_features = pd.DataFrame()

        for measurement_number in range(self.number_of_measurements):
            regression_dataframe_features[f'y_{self.number_of_measurements - measurement_number}'] = \
                time_series[measurement_number:len(time_series) - self.number_of_measurements + measurement_number]

        return regression_dataframe_features.to_numpy(), \
               time_series[self.number_of_measurements:]
