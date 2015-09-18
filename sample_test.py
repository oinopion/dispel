def double(x):
    return x * 2


def test_doubling():
    expected = 5
    assert double(2) == expected


def test_str():
    assert str(2) == double(1)


def test_ok():
    assert 2 + 2 == 4
