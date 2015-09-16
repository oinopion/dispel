import ast


class SimpleAssertRewrite(ast.NodeTransformer):
    def visit_Assert(self, node):
        print_node = ast.Expr(value=ast.Call(
            func=ast.Name(id='print', ctx=ast.Load()),
            args=[ast.Str('Asserting!!!')],
            keywords=[],
        ))

        ast.copy_location(print_node, node)
        ast.fix_missing_locations(print_node)

        return [print_node, node]


class AssertRewrite(ast.NodeTransformer):
    def visit_Assert(self, node):
        if not is_eq(node.test):
            return node

        func = ast.Attribute(
            value=ast.Name(id='@utils', ctx=ast.Load()),
            attr='assert_equals',
            ctx=ast.Load(),
        )
        call = ast.Call(
            func=func,
            args=[node.test.left, node.test.comparators[0]],
            keywords=[]
        )

        new_node = ast.Expr(value=call)
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


def is_eq(node):
    return (isinstance(node, ast.Compare) and
            len(node.ops) == 1 and
            isinstance(node.ops[0], ast.Eq))


def transform(ast_tree):
    import_node = ast.Import(
        names=[ast.alias('test_utils', '@utils')],
        lineno=0, col_offset=0,
    )
    ast_tree.body[0:0] = [import_node]
    transformer = AssertRewrite()
    return transformer.visit(ast_tree)
