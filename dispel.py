#!/usr/bin/env python3.4
#
# TODO:
#  - load designated file
#  - rewrite assert statement
#  - execute tests

import re
import sys
import importlib
import traceback

SUCCESS = '.'
FAILURE = 'F'


def main(*test_file_names):
    modules = import_from_files(test_file_names)
    tests = find_module_tests(modules)
    results = execute_all_tests(tests)
    print_report(results)


def import_from_files(file_names):
    for file_name in file_names:
        module_name = re.sub(r'\.py$', '', file_name)
        yield importlib.import_module(module_name)


def find_module_tests(modules):
    for module in modules:
        test_names = [n for n in dir(module) if n.startswith('test')]
        yield from (getattr(module, n) for n in test_names)


def execute_all_tests(tests):
    return [(t, execute_test(t)) for t in tests]


def execute_test(test):
    try:
        test()
        return SUCCESS, None
    except KeyboardInterrupt:
        raise
    except Exception as e:
        return FAILURE, sys.exc_info()


def print_report(results):
    errors = []
    for test, (symbol, exc_info) in results:
        module, name = test.__module__, test.__name__
        print('%s.%s: %s' % (module, name, symbol))

        if symbol == FAILURE:
            errors.append((test, exc_info))

    for test, (type, value, tb) in errors:
        print('\n=== %s.%s ===' % (test.__module__, test.__name__))
        traceback.print_exception(type, value, tb)


if __name__ == '__main__':
    main(*sys.argv[1:])
