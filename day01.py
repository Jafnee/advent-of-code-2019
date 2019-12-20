def pt1(masses):
    return sum(get_fuel(mass) for mass in masses)


def pt2(masses):
    return sum(get_fuel_rec(mass) for mass in masses)


def get_fuel(mass: int):
    return mass // 3 - 2


def get_fuel_rec(mass):
    if (fuel := get_fuel(mass)) <= 0:
        return 0
    return fuel + get_fuel_rec(fuel)


def test_fuel_needed():
    assert get_fuel(12) == 2
    assert get_fuel(14) == 2
    assert get_fuel(1969) == 654
    assert get_fuel(100756) == 33583


def test_fuel_rec():
    assert get_fuel_rec(1969) == 966
    assert get_fuel_rec(100756) == 50346


if __name__ == '__main__':
    masses = [int(mass) for mass in open('day01.txt', 'r')]
    print(pt1(masses))
    print(pt2(masses))
