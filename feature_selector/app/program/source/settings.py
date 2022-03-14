import os

MGMT_COMMANDS_ALIASES = {
    'select_features': 'common.commands.select_features'
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
    'NUMBER_OF_PROCESSES':
        os.environ.get('NUMBER_OF_PROCESSES', 4)
}
