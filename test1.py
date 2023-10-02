import pytest


from app import my_simple_function


@pytest.mark.parametrize(['a', 'b'], [[1, 'Halo'], [2, 'babay'], [3, 'Good morning']])
def test_simple_func(a, b):
    # a = random.randint(0, 100)
    # b = 'Hello'

    assert my_simple_function(a, b) == f"{b}-{a}"

# comment
