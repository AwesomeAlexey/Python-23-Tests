import random
import pytest

from typing import List, Tuple
from app import get_seq_len, get_longest_seq

random.seed(1)


def author_get_sequence_length(n: int) -> Tuple[int, List[int]]:
    sequence = [n]
    while n != 1:
        n = 3 * n + 1 if n % 2 else n // 2
        sequence.append(n)

    return len(sequence), sequence


def author_get_longest_sequence(lower: int, upper: int) -> Tuple[int, int]:

    max_length, _ = author_get_sequence_length(lower)
    max_n = lower

    for n in range(lower + 1, upper + 1):
        sequence_length, seq = author_get_sequence_length(n)
        if sequence_length > max_length:
            max_n = n
            max_length = sequence_length

    return max_n, max_length


@pytest.mark.timeout(20)
def test_get_sequence_length():
    for _ in range(10):
        test_n = random.randint(1, 100)
        solution_length = get_seq_len(test_n)
        expected_length, expected_sequence = author_get_sequence_length(test_n)
        assert solution_length == expected_length, f"Wrong length: " \
                                                   f"got {solution_length}, " \
                                                   f"but {expected_length} was expected, " \
                                                   f"expected sequence for n = {test_n} is: " \
                                                   f"{expected_sequence}"

@pytest.mark.timeout(20)
def test_get_longest_sequence():
    for _ in range(10):
        lower = random.randint(1, 100)
        upper = lower + random.randint(1, 100)
        solution_n, solution_length = get_longest_seq(lower, upper)
        expected_n, expected_length = author_get_longest_sequence(lower, upper)
        assert solution_n == expected_n, f"Wrong n. Got {solution_n}, but {expected_n} was expected"
        assert solution_length == expected_length, f"Wrong length: " \
                                                   f"got {solution_length}, " \
                                                   f"but {expected_length} was expected"


@pytest.mark.timeout(20)
@pytest.mark.parametrize('n', [19_789_690_303_392_599_159_037, 98_789_690_423_392_599_179_037])
def test_hypothesis(n):
    solution_length = get_seq_len(n)
    expected_length, expected_sequence = author_get_sequence_length(n)
    assert solution_length == expected_length, f"Wrong length: " \
                                               f"got {solution_length}, " \
                                               f"but {expected_length} was expected"


@pytest.mark.timeout(2)
@pytest.mark.parametrize('arg', ['a', '1', '-1', -1, 1.0, 0.5, 0, '1/2', 'ahalay mahalay'])
def test_bad_args_get_seq_len(arg):
    function_result = get_seq_len(arg)
    assert function_result is None, f"Bad arguments must lead to None. " \
                                    f"Bad argument: \"{arg}\", " \
                                    f"function result: {function_result}"


@pytest.mark.timeout(2)
@pytest.mark.parametrize('lower', ['a', '1', '-1', -1, 1.0, 0.5, 0, '1/2', 'ahalay mahalay', 100])
@pytest.mark.parametrize('upper', ['a', '1', '-1', -1, 1.0, 0.5, 0, '1/2', 'ahalay mahalay', 10])
def test_bad_args_get_longest_seq(lower, upper):
    print(lower, upper)
    try:
        function_result = get_longest_seq(lower, upper)
        assert function_result is None, f"Bad arguments must lead to None. " \
                                    f"Bad arguments are: lower: \"{lower}\", upper: \"{upper}\"." \
                                    f"function result: {function_result}"
    except TypeError as ex:
        msg = f"Bad arguments must lead to None. " \
              f"Bad arguments are: lower: \"{lower}\", upper: \"{upper}\"." \
              f"Function failed with Exception: " + str(ex)
        raise TypeError(msg)
