from typing import Iterable, Tuple, Set


Coord = Tuple[int, int]

# Starting wire coord
CENTRAL_PORT = (0, 0)


def pt1(wire1: Iterable[str], wire2: Iterable[str]) -> int:
    """Find the distance of the closest point of wire intersection."""
    wire1_coords = get_wire_coords(wire1)
    wire2_coords = get_wire_coords(wire2)
    intersections = wire1_coords.intersection(wire2_coords)
    intersections.remove(CENTRAL_PORT)

    # Smallest manhattan distance
    return min(get_distance(x, y) for x, y in intersections)


def get_wire_coords(wire: Iterable[str]) -> Set[Coord]:
    """Convert wire actions into coordinates."""
    cur_pos = CENTRAL_PORT
    coords = set()
    for action in wire:
        # Update cur_pos after applying action
        *action_coords, cur_pos = move(cur_pos, action)
        coords.update([*action_coords, cur_pos])
    return(coords)


def move(cur_pos: Coord, action: str) -> Iterable[Coord]:
    """Generator of coordinates for a wire action.

    Includes starting position.

    """
    x, y = cur_pos
    # Include current pos too
    yield (x, y)

    # e.g action = R1337
    direction = action[:1]  # 'R'
    steps = int(action[1:])  # 1337

    step_fn = {
        'R': lambda step: (x + step, y),
        'L': lambda step: (x - step, y),
        'U': lambda step: (x, y + step),
        'D': lambda step: (x, y - step),
    }
    # Coordinates yielded after every action
    yield from (step_fn[direction](step) for step in range(1, steps+1))


def get_distance(x: int, y: int) -> int:
    """Get manhattan distance from origin.

    All measurements taken against (0, 0).

    """
    return abs(x) + abs(y)


if __name__ == '__main__':
    with open('day03.txt', 'r') as f:
        wire1, wire2 = (line.strip().split(',') for line in f)

    print(pt1(wire1, wire2))
