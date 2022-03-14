import os

MGMT_COMMANDS_ALIASES = {
    'fit_model': 'common.commands.fit_model',
    'predict': 'common.commands.predict'
}

CONFIG = {
    'PATH_TO_CONFIG':
        os.environ.get('PATH_TO_CONFIG', '/config.json'),
    'PATH_TO_INPUT':
        os.environ.get('PATH_TO_INPUT', '/input'),
    'PATH_TO_OUTPUT':
        os.environ.get('PATH_TO_OUTPUT', '/output')

}

MODEL = {
    'BACKBONE':
        os.environ.get('BACKBONE', 'HuberRegressor'),
    'SMOOTH':
        os.environ.get('SMOOTH', False),
    'NUMBER_OF_MEASUREMENTS':
        os.environ.get('NUMBER_OF_MEASUREMENTS', 53),
    'NUMBER_OF_PROCESSES':
        os.environ.get('NUMBER_OF_PROCESSES', 4)
}
