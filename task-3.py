import random
import pytest
from math import sqrt

from typing import List, Tuple
from app import is_prime, next_prime

random.seed(1)


def author_check_argument(number: int):
    assert isinstance(number, int), 'argument is not integer'


def author_is_prime(number: int) -> bool:
    author_check_argument(number)
    if number < 2:
        return False
    i = 2
    while i*i <= number:
        if number % i == 0:
            return False
        i += 1
    return True


def author_next_prime(number: int) -> int:
    author_check_argument(number)
    b = number
    while not author_is_prime(b):
        b += 1
    return b


def author_print_all_primes():
    n = 2
    while True:
        if author_is_prime(n):
            print(n)
        n += 1



# def author_get_sequence_length(n: int) -> Tuple[int, List[int]]:
#     sequence = [n]
#     while n != 1:
#         n = 3 * n + 1 if n % 2 else n // 2
#         sequence.append(n)
#
#     return len(sequence), sequence


# def author_get_longest_sequence(lower: int, upper: int) -> Tuple[int, int]:
#
#     max_length, _ = author_get_sequence_length(lower)
#     max_n = lower
#
#     for n in range(lower + 1, upper + 1):
#         sequence_length, seq = author_get_sequence_length(n)
#         if sequence_length > max_length:
#             max_n = n
#             max_length = sequence_length
#
#     return max_n, max_length


def test_is_prime():
    for _ in range(10):
        test_n = random.randint(1, 100)
        solution_answer = is_prime(test_n)
        expected_solution = author_is_prime(test_n)
        assert solution_answer == expected_solution, f"Wrong answer(is_prime): " \
                                                   f"got {solution_answer}, " \
                                                   f"but {expected_solution} was expected, " \
                                                   f"for number = {test_n} "

def test_next_prime():
    for _ in range(10):
        test_n = random.randint(1, 100)
        solution_next = next_prime(test_n)
        expected_next = author_next_prime(test_n)
        assert solution_next == expected_next, f"Wrong next prime(next_prime): " \
                                                   f"got {solution_next}, " \
                                                   f"but {expected_next} was expected, " \
                                                   f"for number = {test_n}"


### TODO:

# @pytest.mark.parametrize('n', [19_789_690_303_392_599_159_037, 98_789_690_423_392_599_179_037])
# def test_hypothesis_is_prime(n):
#     solution_answer = is_prime(n)
#     expected_solution = author_is_prime(n)
#     assert solution_answer == expected_solution, f"Wrong answer(is_prime): " \
#                                                  f"got {solution_answer}, " \
#                                                  f"but {expected_solution} was expected, "
#
# @pytest.mark.parametrize('n', [19_789_690_303_392_599_159_037, 98_789_690_423_392_599_179_037])
# def test_hypothesis_next_prime(n):
#     solution_next = next_prime(n)
#     expected_next = author_next_prime(n)
#     assert solution_next == expected_next, f"Wrong answer(is_prime): " \
#                                                  f"got {solution_next}, " \
#                                                  f"but {expected_next} was expected, "
#


@pytest.mark.parametrize('arg', ['a', '1', '-1', -1, 1.0, 0.5, 0, '1/2', 'ahalay mahalay'])
def test_bad_args_is_prime(arg):
    try:
        function_result = is_prime(arg)
    except AssertionError:
        pass
    except Exception as e:
        print(f"Bad arguments must throw AssertionError."
              f"Bad argument: \"{arg}\", ")
        raise e

@pytest.mark.parametrize('arg', ['a', '1', '-1', -1, 1.0, 0.5, 0, '1/2', 'ahalay mahalay'])
def test_bad_args_next_prime(arg):
    try:
        function_result = next_prime(arg)
    except AssertionError:
        pass
    except Exception as e:
        print(f"Bad arguments must throw AssertionError."
              f"Bad argument: \"{arg}\", ")
        raise e

