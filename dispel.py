#!/usr/bin/env python3.4

import ast
import importlib.util
import os.path
import sys
import transformer


def import_hook(path):
    # import_hook will be called for every item in `sys.path`
    if os.path.abspath('') == path:
        return Finder()
    else:
        raise ImportError


sys.path_hooks.insert(0, import_hook)
sys.path_importer_cache.clear()


class Finder:
    def find_spec(self, module, target=None):
        file_name = module + '.py'
        spec = importlib.util.spec_from_file_location(
            name=module, location=file_name, loader=Loader())
        return spec


class Loader:
    def exec_module(self, module):
        with open(module.__file__, 'rb') as fp:
            source_bytes = fp.read()

        ast_tree = ast.parse(source_bytes, module.__file__)
        ast_tree = transformer.transform(ast_tree)
        code = compile(ast_tree, module.__file__, 'exec')
        exec(code, module.__dict__)


if __name__ == '__main__':
    import sample_test

    sample_test.test_doubling()
