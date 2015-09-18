#!/usr/bin/env python3

import ast
import importlib
import os.path
import sys
import traceback
from ast import Call, Load, fix_missing_locations, \
    NodeTransformer, Expr, copy_location, Name
from importlib.util import spec_from_file_location


def import_hook(path):
    if os.path.abspath('') != path:
        raise ImportError

    return Finder()


class Finder:
    def find_spec(self, module, target=None):
        file_name = module + '.py'
        if not os.path.exists(file_name):
            return None

        return spec_from_file_location(
            name=module,
            location=file_name,
            loader=Loader()
        )


class Loader:
    def exec_module(self, module):
        with open(module.__file__, 'rb') as fp:
            source = fp.read()

        tree = ast.parse(source, module.__file__)
        tree = transform(tree)
        code = compile(tree, module.__file__, 'exec')
        module.__dict__['#eq'] = assert_equals
        exec(code, module.__dict__)


class AssertRewrite(NodeTransformer):
    def visit_Assert(self, node):
        call = Call(
            func=Name(id='#eq', ctx=Load()),
            args=[
                node.test.left,
                node.test.comparators[0]
            ],
            keywords=[]
        )
        new_node = Expr(value=call)
        copy_location(new_node, node)
        fix_missing_locations(new_node)
        return new_node


def transform(module):
    transformer = AssertRewrite()
    return transformer.visit(module)


def assert_equals(a, b):
    if a != b:
        raise AssertionError('%r is not equal to %r' % (a, b))


def run_tests(module_name):
    module = importlib.import_module(module_name)
    for name in dir(module):
        if not name.startswith('test'):
            continue
        try:
            print(module_name, name, sep='.')
            getattr(module, name)()
        except Exception:
            print(traceback.format_exc())


if __name__ == '__main__':
    sys.path_hooks.insert(0, import_hook)
    sys.path_importer_cache.clear()

    for module_name in sys.argv[1:]:
        run_tests(module_name)
