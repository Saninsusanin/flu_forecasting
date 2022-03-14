# nii_gripp

## Description

This program makes an interval forecast of a number of disabled people by some disease on the next weeks, based on previous statistics

## User guide

Next command will run the program:
```
python manage.py [-h] | [--runcommand {fit_model, predict}]
```

Command example:
```
python manage.py --runcommand fit_model
```

Runcommand options description:

1. fit_model - this option starts part of the program that trains model. To start training you have to add config file.
The default one is `config.json`. If you want to use another file you have to set environment variable `PATH_TO_CONFIG`.
In that variable you have to add a relative path to new config file. In that config file you have to set a few values: 
`diseases` - an array of disease abbreviations, `ages` - an array of possible age groups
(in passed data have to exist column `disease_name`_`age_group`), 
`input` - contains a relative path to data (current version of the program supports .xls, .xslx formats), 
`regions` - an array regions for which current model will train to predict or string - `all` to make a forecast for all regions that present in the input file, 

2. predict - this option runs predictor. To get predictions you have to add config file.
The default one is `config.json`. If you want to use another file you have to set environment variable `PATH_TO_CONFIG`.
In that variable you have to add a relative path to new config file. In that config file you have to set a few values: 
`length_of_prediction_interval` - integer number that represents number of weeks for which predictor will make a forecast, 
`values_filename` - a relative path to output file with a predictions

Input description:

For proper work of this program two files are needed: first - a file with disease statistics, second - a file with features. 
Rows in these two files have to be sorted in order in which time flows. 
Both files have to have these service columns: `REGION_NAME`, `YEAR`, `WEEK`.
The best case - shapes(number of rows) in these two files the same and for row number `i` in first file corresponds row number `i` from second file.

Output description:

1. fit_model command output: this command saves models that are used to make a forecast
2. predict command output: this command saves predictions as a .csv file with forecast for all regions and all diseases and age groups on which last model was fitted.
This .csv file contains these columns: `REGION_NAME`, `YEAR`, `WEEK`, and all acceptable combinations of disease name and age group(`disease_age` - is name for that type of column)

## Advanced settings
`NUMBER_OF_MEASUREMENTS` - this environment variable sets number of weeks on which forecast will be based(default value - 53)

`BACKBONE` -  this environment variable sets the backbone of the autoregression model. Now two backbones are available - 
`HuberRegressor`, `XGBRegressor`

`SMOOTH` - this environment variable defines will outliers in data be smoothed. Possible values - true or false

`NUMBER_OF_PROCESSES` - number of processes to work with

## Using docker
First of all - build 
`docker-compose build`

And now to run the program:
`docker-compose run --entrypoint "python manage.py --runcommand fit_model" gripp_predictor` - to fit new model

`docker-compose run --entrypoint "python manage.py --runcommand predict" gripp_predictor` - to make forecast

All results will be saved in output directory, all input data must be placed in input folder