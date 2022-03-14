import warnings

import sys
sys.path.append('source')

from source.common.management.base import MethodCaller, ManagementParser


def warn(*args, **kwargs):
    pass


warnings.warn = warn

if __name__ == '__main__':
    MethodCaller(args=ManagementParser()())()
