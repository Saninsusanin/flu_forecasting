# nii_gripp

## Description

This program selects most valuable features

## User guide

Next command will run the program:
```
python manage.py [-h] | [--runcommand {select_features}]
```

Command example:
```
python manage.py --runcommand select_features
```

Runcommand options description:

1. select_features - this option select features that mostly influence on the prediction. To start training you have to add config file.
The default one is `config.json`. If you want to use another file you have to set environment variable `PATH_TO_CONFIG`.
In that variable you have to add a relative path to new config file. In that config file you have to set a few values: 
`percentage` - float number that represents how many data(in percentage from all existing data) will be passed to a model to train,
`input` - a relative path to data,  
`target_column_name` - name of the target column,
`features` - an array of the column names from passed data. The power of influence of these columns on target_column will be estimated. 
`most_valuable_features_filename` - the name of the file that will contain most valuable features,
`percent_of_features` - float number that represents how many most valuable features will be returned(`percent_of_features` * number_of_features),
`method` - this option has to possible values: `brute_force` - checks all possible combinations of features, 
`greedy_add` - works much faster than `brute_force`, but checks not all possible feature combinations.

Input description:

For proper work of this program two files are needed: first - a file with disease statistics, second - a file with features. 
Rows in these two files have to be sorted in order in which time flows. 
Both files have to have these service columns: `REGION_NAME`, `YEAR`, `WEEK`.
The best case - shapes(number of rows) in these two files the same and for row number `i` in first file corresponds row number `i` from second file.

Output description:

1. select features command output: .csv file that contains two columns: 
`FEATURES` - column with names of a features, 
`WEIGHTS` - column with corresponding weight of a feature

## Advanced settings
`NUMBER_OF_PROCESSES` - number of precesses to work with

## Using docker
First of all - build 
`docker-compose build`

And now to run the program:

`docker-compose run --entrypoint "python manage.py --runcommand select_features" gripp_feature_selector` - for feature selection

All results will be saved in output directory, all input data must be placed in input folder