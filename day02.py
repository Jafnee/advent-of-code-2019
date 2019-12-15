import operator
from typing import List

import pytest


END = 99
ADD = 1
MUL = 2


OPS = {
    ADD: operator.add,
    MUL: operator.mul,
}


def pt1(intcode: str):
    state = parse(intcode)
    state[1] = 12
    state[2] = 2
    return execute(state)[0]


def pt2(intcode: str):
    initial_state = parse(intcode)
    # Valid nouns & verbs are (0 - 99)
    for noun in range(100):
        for verb in range(100):
            state = initial_state.copy()
            state[1] = noun
            state[2] = verb
            if execute(state)[0] == 19690720:
                return 100 * noun + verb


def execute(state: List[int]) -> List[int]:
    """Executes Intcode program.

    Parameters
    ----------
    state : list of int
        Intcode program / initial state

    Returns
    -------
    list of int
        Final state

    """
    i = 0  # pointer
    while True:
        opcode = state[i]
        if opcode == END:
            break

        # KeyError if operation not supported
        op = OPS[opcode]
        iparam1, iparam2, ires = state[i+1:i+4]
        param1 = state[iparam1]
        param2 = state[iparam2]

        state[ires] = op(param1, param2)
        i += 4
    return state


def parse(intcode: str) -> List[int]:
    return [int(x) for x in intcode.split(',')]


def format(intcode: List[int]) -> str:
    return ",".join(str(x) for x in intcode)


@pytest.mark.parametrize('initial,expected', [
    ('1,0,0,0,99', '2,0,0,0,99'),
    ('2,3,0,3,99', '2,3,0,6,99'),
    ('2,4,4,5,99,0', '2,4,4,5,99,9801'),
    ('1,1,1,4,99,5,6,0,99', '30,1,1,4,2,5,6,0,99'),
])
def test_execute(initial, expected):
    initial_state = parse(initial)
    final_state = execute(initial_state)
    assert format(final_state) == expected


if __name__ == '__main__':
    intcode = open('day02.txt', 'r').readline()
    print(pt1(intcode))
    print(pt2(intcode))
