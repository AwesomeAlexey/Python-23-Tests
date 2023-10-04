import random
import pytest
from math import gcd as mgcd

from app import is_prime, next_prime, gcd, are_coprime

random.seed(1)


def author_check_argument(number: int):
    assert isinstance(number, int), 'argument is not integer'


def author_is_prime(number: int) -> bool:
    author_check_argument(number)
    if number < 2:
        return False
    i = 2
    while i * i <= number:
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


###gcd and are_coprime

def test_gcd():
    for _ in range(10):
        num_1 = random.randint(1, 1000)
        num_2 = random.randint(1, 1000)
        solution_answer = gcd(num_1, num_2)
        expected_solution = mgcd(num_1, num_2)
        assert solution_answer == expected_solution, f"Wrong answer(gcd): " \
                                                     f"got {solution_answer}, " \
                                                     f"but {expected_solution} was expected, " \
                                                     f"for numbers = {num_1}, {num_2} "


def test_are_coprime():
    for _ in range(10):
        num_1 = random.randint(1, 1000)
        num_2 = random.randint(1, 1000)
        solution_answer = are_coprime(num_1, num_2)
        expected_solution = (mgcd(num_1, num_2) == 1)
        assert solution_answer == expected_solution, f"Wrong next prime(are_coprime): " \
                                                     f"got {solution_answer}, " \
                                                     f"but {expected_solution} was expected, " \
                                                     f"for numbers = {num_1}, {num_2}"


@pytest.mark.parametrize('num_1', ['a', '1', '-1', -1, 1.0, 0.5, 0, '1/2', 'ahalay mahalay', 10])
@pytest.mark.parametrize('num_2', ['a', '1', '-1', -1, 1.0, 0.5, 0, '1/2', 'ahalay mahalay'])
def test_bad_args_gcd(num_1, num_2):
    try:
        function_result = gcd(num_1, num_2)
    except AssertionError:
        pass
    except Exception as e:
        print(f"Bad arguments must throw AssertionError."
              f"Bad arguments: \"{num_1}\", \"{num_2}\" ")
        raise e


@pytest.mark.parametrize('num_1', ['a', '1', '-1', -1, 1.0, 0.5, 0, '1/2', 'ahalay mahalay', 10])
@pytest.mark.parametrize('num_2', ['a', '1', '-1', -1, 1.0, 0.5, 0, '1/2', 'ahalay mahalay'])
def test_bad_args_are_coprime(num_1, num_2):
    try:
        function_result = are_coprime(num_1, num_2)
    except AssertionError:
        pass
    except Exception as e:
        print(f"Bad arguments must throw AssertionError."
              f"Bad arguments: \"{num_1}\", \"{num_2}\" ")
        raise e
