from collections import defaultdict

import pytest


def pt1(puzzle_input: str):
    min, max = parse_range(puzzle_input)
    valid_passwords = valid_passwords_gen(min, max, checks=[
        has_no_decreasing_digits,
        has_doubles
    ])
    # FIXME: Can reduce memory here with sum(1 for _ in generator)
    return len(list(valid_passwords))


def pt2(puzzle_input: str):
    min, max = parse_range(puzzle_input)
    valid_passwords = valid_passwords_gen(min, max, checks=[
        has_no_decreasing_digits,
        has_strict_doubles
    ])
    return len(list(valid_passwords))


def valid_passwords_gen(min, max, checks):
    for val in range(min, max+1):
        # Very wasteful
        # FIXME: get the valid min and max range without looping through each
        # FIXME: each check is looping digits again. re-use same loop
        # FIXME: due to digits increasing, can optimise doubles checking.
        # e.g not possible for 4544 to be valid. Means a simpler counter based
        # check works
        if not all(check(val) for check in checks):
            continue
        yield val


def has_no_decreasing_digits(val: int):
    """Check if value has decreasing digits.

    Going from left to right, the digits never decrease;
    they only ever increase or stay the same (like 111123 or 135679).

    """
    val = str(val)
    for idx, digit in list(enumerate(val))[:-1]:
        if int(digit) > int(val[idx + 1]):
            return False
    return True


def has_doubles(val: int):
    """Check if value has doubles.

    Two adjacent digits are the same (like 22 in 122345).

    """
    val = str(val)
    for idx, digit in list(enumerate(val))[:-1]:
        if digit == val[idx + 1]:
            return True
    return False


def has_strict_doubles(val: int):
    """Check if value has doubles.

    The two adjacent matching digits are not part of a
    larger group of matching digits.

    112233 meets these criteria because the digits never decrease
    and all repeated digits are exactly two digits long.

    123444 no longer meets the criteria
    (the repeated 44 is part of a larger group of 444).

    111122 meets the criteria
    (even though 1 is repeated more than twice, it still contains a double 22).

    """
    occurrences = defaultdict(int)
    val = str(val)
    prev_digit = val[0]
    for digit in val[1:]:
        # compare against next el
        # If last item, compare against previous
        if digit == prev_digit:
            occurrences[digit] += 1
        prev_digit = digit
    # Only 1 occurrence, if single double found
    return 1 in occurrences.values()


def parse_range(puzzle_input):
    return [int(x) for x in puzzle_input.split('-')]


@pytest.mark.parametrize('val,expected', [
    ('112233', True),
    ('111122', True),
    ('566888', True),
    ('123444', False),
])
def test_has_strict_doubles(val, expected):
    assert has_strict_doubles(val) is expected


if __name__ == '__main__':
    puzzle_input = open('day04.txt', 'r').read().strip()
    print(pt1(puzzle_input))
    print(pt2(puzzle_input))
