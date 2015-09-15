def assert_equals(a, b):
    if a != b:
        raise AssertionError('%r is not equal to %r' % (a, b))
