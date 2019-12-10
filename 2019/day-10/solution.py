from typing import List


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
    row = 0
    with open('./input_test.txt', 'r') as f:
        for line in f:
            coords = [elem for elem in line]
            for idx, elem in enumerate(coords):
                if elem == '#':
                    points.append(Point(idx, row))
            row += 1
    return points


def check_is_blocking(start: Point, end: Point, midpoints: List[Point]) -> bool:
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

        if abs(cross_product) != 0:
            continue

        dot_product = (
            (mid.x - start.x) *
            (end.x - start.x) +
            (mid.y - start.y) *
            (end.y - start.y)
        )
        if dot_product < 0:
            continue

        squared_length_ba = (
            (end.x - start.x) *
            (end.x - start.x) +
            (end.y - start.y) *
            (end.y - start.y)
        )
        if dot_product > squared_length_ba:
            return False

    return True


def main():
    asteroids = load_input()
    # This is going to operate in O(n^3) runtime complexity
    # and that makes me hate myself, but I'm also too lazy
    # to do anything about it until it becomes an actual
    # problem, so that's where I'm at right now.
    for asteroid in asteroids:
        endpoints = [
            endpoint for endpoint in asteroids
            if (endpoint.x, endpoint.y) != (asteroid.x, asteroid.y)]
        for endpoint in endpoints:
            midpoints = [
                midpoint for midpoint in endpoints
                if (abs(endpoint.x), abs(endpoint.y)) <= \
                   (abs(midpoint.x), abs(midpoint.y)) <= \
                   (abs(asteroid.x), abs(asteroid.y))
            ]
            _visible_to_src = True
            if not midpoints:
                continue
            if not check_is_blocking(asteroid, endpoint, midpoints):
                asteroid.num_visible += 1
        print(f'{(asteroid.x, asteroid.y)}: {asteroid.num_visible}')


if __name__ == '__main__':
    main()
