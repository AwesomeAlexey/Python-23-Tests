import random

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

    max_length, seq = author_get_sequence_length(upper)
    max_n = upper

    for n in range(lower, upper):
        sequence_length, seq = author_get_sequence_length(n)
        if sequence_length > max_length:
            max_n = n
            max_length = sequence_length

    return max_n, max_length


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
