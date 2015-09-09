import ast


class AssertRewrite(ast.NodeTransformer):
    def visit_Assert(self, node):
        name_node = ast.Name(id='print', ctx=ast.Load())
        call_node = ast.Call(
            func=name_node,
            args=[ast.Str('Asserting!!!')],
            keywords=[],
        )
        print_node = ast.Expr(value=call_node)

        ast.copy_location(print_node, node)
        ast.fix_missing_locations(print_node)

        return [print_node, node]
