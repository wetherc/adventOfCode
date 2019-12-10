from typing import List
import numpy as np
import copy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.num_visible = 0


def load_input() -> List[Point]:
    '''Parses input file and returns a list of Point objects
    with the (x, y) coordinates of each point.

    Points are assumed to exist as one-dimensional objects existing
    in the exact center of their bounding box. No more than 1 point
    may exist at any 1 unit-by-1 unit bounding box on the coordinate
    plane.
    '''
    points = []
    width = 0
    height = 0

    with open('./input.txt', 'r') as f:
        for line in f:
            coords = [elem for elem in line]
            width = max(width, len(coords))
            for idx, elem in enumerate(coords):
                if elem == '#':
                    points.append(Point(idx, height))
            height += 1
    return points, width, height


def check_is_blocked(start: Point, end: Point, midpoints: List[Point]) -> bool:
    '''Uses the crossproduct of (b-a) and (c-a) to determine
    if the points are aligned (a crossproduct of 0 denotes that
    we form a 0-area triangle among the three points, implying
    that they are linear with respect to one another).

    We then use the dot product of (b-a) and (c-a) to determine
    whether point b lies between points c and a. Specifically, this
    is the case if is positive and is less than the square of the
    distance between a and b.
    '''
    for mid in midpoints:
        cross_product = (
            (mid.y - start.y) *
            (end.x - start.x) -
            (mid.x - start.x) *
            (end.y - start.y)
        )

        # skip to the next candidate point if
        # area of the triangle is non-zero
        if abs(cross_product) != 0:
            continue

        dot_product = (
            (mid.x - start.x) *
            (end.x - start.x) +
            (mid.y - start.y) *
            (end.y - start.y)
        )

        # skip to the next candidate point if
        # midpoint is outside the bounts of the
        # start/endpoints
        if dot_product < 0:
            continue

        squared_length_ba = (
            (end.x - start.x) *
            (end.x - start.x) +
            (end.y - start.y) *
            (end.y - start.y)
        )

        if dot_product > squared_length_ba:
            return True

    return False


def boooOOOooom(base, asteroid_field, width, height):
    def angle_between(p1, p2):
        # https://stackoverflow.com/a/31735642
        # I'm lazy
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return np.rad2deg((ang1 - ang2) % (2 * np.pi))

    def euclidean_distance(base, asteroid):
        dist = ((asteroid.x - base.x)**2 + (asteroid.y - base.y)**2 )**0.5
        return dist

    coordinates = {}
    # Set a reference at 12:00 with our asteroid base
    # re-centered at (0, 0)
    reference = (0, -1 * base.y)
    for asteroid in asteroid_field:
        distance = euclidean_distance(base, asteroid)
        angle = angle_between(
            (asteroid.x - base.x, asteroid.y - base.y),
            reference)
        if not coordinates.get(angle):
            coordinates[angle] = {
                distance: asteroid
            }
        else:
            coordinates[angle][distance] = asteroid
            coordinates[angle] = dict(sorted(coordinates[angle].items()))

    coordinates = dict(sorted(coordinates.items()))
    _i = 0
    _kaboomed = None

    while _i < min(200, len(asteroid_field)):
        _temp = copy.deepcopy(coordinates)
        for coord, asteroids in _temp.items():
            if _i >= 200:
                break
            _kaboomed = asteroids[list(asteroids.keys())[0]]
            del coordinates[coord][list(asteroids.keys())[0]]

            if len(coordinates[coord]) == 0:
                del coordinates[coord]

            _i += 1
    print(f'Kabooming {_i}th asteroid at {(_kaboomed.x, _kaboomed.y)}')
    print((_kaboomed.x * 100) + _kaboomed.y)


def main():
    asteroids, width, height = load_input()

    # This is going to operate in O(n^3) runtime complexity
    # and that makes me hate myself, but I'm also too lazy
    # to do anything about it until it becomes an actual
    # problem, so that's where I'm at right now.
    max_point = Point(0, 0)
    max_nodes_visible = 0

    print(f'Iterating through all candidate asteroids')
    print(
        f'This is in O(n^3) runtime complexity, so grab '
        f'some coffee or something while you wait...')
    for asteroid in asteroids:
        endpoints = [
            endpoint for endpoint in asteroids
            if (endpoint.x, endpoint.y) != (asteroid.x, asteroid.y)]
        for endpoint in endpoints:
            midpoints = [
                midpoint for midpoint in endpoints
                if (midpoint.x, midpoint.y) != (endpoint.x, endpoint.y)]
            _visible_to_src = True
            if not check_is_blocked(asteroid, endpoint, midpoints):
                asteroid.num_visible += 1
        if asteroid.num_visible > max_nodes_visible:
            max_nodes_visible = asteroid.num_visible
            max_point = asteroid

    print(
        f'Asteroid at point {(max_point.x, max_point.y)} '
        f'has {max_nodes_visible} visible')

    asteroid_field = [
        asteroid for asteroid in asteroids
        if asteroid != max_point]
    boooOOOooom(max_point, asteroid_field, width, height)


if __name__ == '__main__':
    main()
