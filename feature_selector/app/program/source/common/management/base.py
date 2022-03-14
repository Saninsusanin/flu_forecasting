import argparse

from importlib import import_module
from source.settings import MGMT_COMMANDS_ALIASES


class ManagementParser:
    parser = argparse.ArgumentParser(description='Parser of management console args')
    command_prefix = "runcommand"

    def __init__(self):
        self.command_choices = [alias for alias in MGMT_COMMANDS_ALIASES.keys()]
        self.add_parse_args()

    def add_parse_args(self):
        self.parser.add_argument('--%s' % self.command_prefix, choices=self.command_choices, required=True,
                                 type=str, help="Management commands")

    def __call__(self):
        return getattr(self.parser.parse_args(), self.command_prefix)


class MethodCaller:
    def __init__(self, args):
        self.aliased_path = MGMT_COMMANDS_ALIASES.get(args)

    def import_module(self):
        return import_module(self.aliased_path)

    def import_method(self):
        return getattr(self.import_module(), 'do')

    def __call__(self):
        out = self.import_method()
        out()
