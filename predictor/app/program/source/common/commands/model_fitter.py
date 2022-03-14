from pickle import dump
from source.settings import MODEL
from source.core.model_runner import ModelRunner
from source.core.transformers import TimeSeriesExtractor


class CheckColumnName:
    def __init__(self, data):
        self.real_column = set(data.columns.values)

    def __call__(self, column_name):
        return column_name in self.real_column


class FitModel:
    def __init__(self, data, prefix, last_date):
        self.data = data
        self.prefix = prefix
        self.last_date = last_date

    def fit_model(self, data):
        region, disease, age = data
        check_column_name = CheckColumnName(self.data)

        if check_column_name(f'{disease}_{age}'):
            time_series_extractor = TimeSeriesExtractor(disease=disease,
                                                        age=age,
                                                        region=region,
                                                        smooth=MODEL['SMOOTH'])
            time_series = time_series_extractor.transform(self.data)
            runner = ModelRunner(time_series=time_series, last_date=self.last_date)
            runner.fit()

            with open(self.prefix + ('#'.join([region, disease, age]) + '.model'), 'wb') as destination:
                dump(runner, destination)
        else:
            print(f'this combination of {disease} and {age} is not present in the data')
