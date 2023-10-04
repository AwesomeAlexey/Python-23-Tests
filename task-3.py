import pytest
import numpy as np
import random
from app import is_prime, next_prime, gcd, are_coprime
from typing import Union, Any
from math import gcd as author_gcd


def author_is_prime(n: int) -> Union[bool, None]:
    if bad_arg(n):
        return None
    if n < 2:
        return False

    for i in range(2, int(np.sqrt(n) + 1)):
        if n % i == 0:
            return False

    return True


def author_next_prime(a: int) -> Union[int, None]:
    if bad_arg(a):
        return None
    while not author_is_prime(a):
        a += 1
    return a


def author_are_coprime(a: int, b: int) -> Union[bool, None]:
    if type(a) == type(b) == int:
        return author_gcd(a, b) == 1
    else:
        return None


def bad_arg(arg: Any) -> bool:
    if type(arg) != int:
        return True
    if arg <= 0:
        return True
    return False


@pytest.mark.timeout(20)
def test_is_prime():
    numbers = np.random.randint(1, 1000, 100)
    for n in numbers:
        solution_answer = is_prime(int(n))
        expected_answer = author_is_prime(int(n))
        assert solution_answer == expected_answer, f"Wrong primeness for number {n}." \
                                                   f"Got: {solution_answer}, but " \
                                                   f"{expected_answer} was expected"


@pytest.mark.timeout(20)
def test_next_prime():
    numbers = np.random.randint(1, 1000, 100)

    for n in numbers:
        solution_answer = next_prime(int(n))
        expected_answer = author_next_prime(int(n))
        assert solution_answer == expected_answer, f"Wrong next prime for number {n}." \
                                                   f"Got: {solution_answer}, but " \
                                                   f"{expected_answer} was expected"


@pytest.mark.timeout(20)
def test_big_is_prime():
    n = random.randint(1_000_000_000, 1_000_000_000_000_000)
    solution_answer = is_prime(n)
    expected_answer = author_is_prime(n)
    assert solution_answer == expected_answer, f"Wrong primeness for number {n}." \
                                               f"Got: {solution_answer}, but " \
                                               f"{expected_answer} was expected"


@pytest.mark.timeout(20)
def test_big_next_prime():
    n = random.randint(1_000_000_000, 1_000_000_000_000_000)
    solution_answer = next_prime(n)
    expected_answer = author_next_prime(n)
    assert solution_answer == expected_answer, f"Wrong next prime for number {n}." \
                                               f"Got: {solution_answer}, but " \
                                               f"{expected_answer} was expected"


@pytest.mark.timeout(10)
def test_is_coprime():
    n = np.random.randint(1, 100, (100, 2))
    for n_ in n:
        a = int(n_[0])
        b = int(n_[1])
        solution_gcd = are_coprime(a, b)
        expected_gcd = author_are_coprime(a, b)
        assert solution_gcd == expected_gcd, f"Wrong coprime-ness for numbers {a} and {b}," \
                                             f"Got: {solution_gcd}, but {expected_gcd} was expected"


@pytest.mark.timeout(10)
def test_gcd():
    n = np.random.randint(1, 100, (100, 2))
    for n_ in n:
        a = int(n_[0])
        b = int(n_[1])
        solution_gcd = gcd(a, b)
        expected_gcd = author_gcd(a, b)
        assert solution_gcd == expected_gcd, f"Wrong gcd for numbers {a} and {b}," \
                                             f"Got: {solution_gcd}, but {expected_gcd} was expected"


@pytest.mark.timeout(10)
def test_negative_is_coprime():
    n = np.random.randint(-100, 100, (100, 2))
    for n_ in n:
        a = int(n_[0])
        b = int(n_[1])
        solution_gcd = are_coprime(a, b)
        expected_gcd = author_are_coprime(a, b)
        assert solution_gcd == expected_gcd, f"Wrong coprime-ness for numbers {a} and {b}," \
                                             f"Got: {solution_gcd}, but {expected_gcd} was expected"


@pytest.mark.timeout(10)
def test_negative_gcd():
    n = np.random.randint(-100, 100, (100, 2))
    for n_ in n:
        a = int(n_[0])
        b = int(n_[1])
        solution_gcd = gcd(a, b)
        expected_gcd = author_gcd(a, b)
        assert solution_gcd == expected_gcd, f"Wrong gcd for numbers {a} and {b}," \
                                             f"Got: {solution_gcd}, but {expected_gcd} was expected"


@pytest.mark.timeout(10)
def test_zero_is_coprime():
    n = np.random.randint(-100, 100, 100)
    for n_ in n:
        a = 0
        b = int(n_)
        solution_coprime_left_zero = are_coprime(a, b)
        solution_coprime_right_zero = are_coprime(a, b)
        assert solution_coprime_left_zero == solution_coprime_right_zero, f"Why the results for are_coprime({a},{b})" \
                                                                          f" = {solution_coprime_left_zero}" \
                                                                          f"and are_coprime({b}, {a}) = " \
                                                                          f"{solution_coprime_right_zero} " \
                                                                          f"are not the same?"
        solution_coprime = solution_coprime_left_zero
        expected_coprime = author_are_coprime(a, b)
        assert solution_coprime == expected_coprime, f"Wrong coprime-ness for numbers {a} and {b}," \
                                                     f"Got: {solution_coprime}, but {expected_coprime} was expected"


@pytest.mark.timeout(10)
def test_zero_gcd():
    n = np.random.randint(-100, 100, 100)
    for n_ in n:
        a = 0
        b = int(n_)
        solution_gcd_left_zero = gcd(a, b)
        solution_gcd_right_zero = gcd(b, a)
        assert solution_gcd_left_zero == solution_gcd_right_zero, f"Why the results for gcd({a},{b}) = {solution_gcd_left_zero}" \
                                                                  f"and gcd({b}, {a}) = {solution_gcd_right_zero} are not the same?"
        solution_gcd = solution_gcd_left_zero
        expected_gcd = author_gcd(a, b)
        assert solution_gcd == expected_gcd, f"Wrong gcd for numbers {a} and {b}," \
                                             f"Got: {solution_gcd}, but {expected_gcd} was expected"


@pytest.mark.timeout(10)
@pytest.mark.parametrize('arg_1', ['a', '1', '-1', 1.0, 0.5, '1/2', 'ahalay mahalay', '1'])
@pytest.mark.parametrize('arg_2', ['a', '1', '-1', 1.0, 0.5, '1/2', 'ahalay mahalay', 1])
def test_bad_args_are_coprime(arg_1, arg_2):
    try:
        function_result = are_coprime(arg_1, arg_2)
        assert False, f"Bad arguments must lead to AssertionError. " \
                      f"Bad arguments: \"{arg_1}\" as {type(arg_1)} and \"{arg_2}\" as {type(arg_2)} , " \
                      f"are_coprime({arg_1}, {arg_2}) function result: {function_result}"
    except AssertionError:
        pass
    except Exception:
        raise


@pytest.mark.timeout(10)
@pytest.mark.parametrize('arg_1', ['a', '1', '-1', 1.0, 0.5, '1/2', 'ahalay mahalay', '1'])
@pytest.mark.parametrize('arg_2', ['a', '1', '-1', 1.0, 0.5, '1/2', 'ahalay mahalay', 1])
def test_bad_args_gcd(arg_1, arg_2):
    try:
        function_result = gcd(arg_1, arg_2)
        assert False, f"Bad arguments must lead to Assertion Error. " \
                      f"Bad arguments: \"{arg_1}\" as {type(arg_1)} and \"{arg_2}\" as {type(arg_2)} , " \
                      f"gcd({arg_1}, {arg_2}) function result: {function_result}"
    except AssertionError:
        pass
    except Exception:
        raise


@pytest.mark.timeout(2)
@pytest.mark.parametrize('arg', ['a', '1', '-1', -1, 1.0, 0.5, 0, '1/2', 'ahalay mahalay'])
def test_bad_arg_is_prime(arg):
    try:
        function_result = is_prime(arg)
        assert False, f"Bad arguments must lead to AssertionError. " \
                      f"Bad argument: \"{arg}\" as {type(arg)}, " \
                      f"is_prime({arg}) function result: {function_result}"
    except AssertionError:
        pass
    except Exception as ex:
        raise ex


@pytest.mark.timeout(2)
@pytest.mark.parametrize('arg', ['a', '1', '-1', -1, 1.0, 0.5, 0, '1/2', 'ahalay mahalay'])
def test_bad_arg_next_prime(arg):
    try:
        function_result = next_prime(arg)
        assert False, f"Bad arguments must lead to AssertionError. " \
                      f"Bad argument: \"{arg}\" as {type(arg)}, " \
                      f"next_prime({arg}) function result: {function_result}"
    except AssertionError:
        pass
    except Exception:
        raise

