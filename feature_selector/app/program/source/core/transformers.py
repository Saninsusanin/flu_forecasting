import numpy as np
import pandas as pd

from collections import defaultdict
from sklearn.base import TransformerMixin, BaseEstimator


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


class TrainTestSplit(BaseEstimator, TransformerMixin):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def fit(self, data):
        pass

    def transform(self, data):
        features_matrix, target = data

        return features_matrix[:int(self.percentage * len(target)), :], target[:int(self.percentage * len(target))], \
               features_matrix[int(self.percentage * len(target)):, :], target[int(self.percentage * len(target)):]
