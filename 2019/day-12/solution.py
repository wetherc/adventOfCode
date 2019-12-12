import hashlib
import numpy as np
from re import sub
from typing import List


class Orchestrator:
    def __init__(self, moons: np.array) -> None:
        self.moons = moons
        self.velocities = np.full((4, 3), 0)

        _hist = hashlib.md5(self.moons.tostring()).hexdigest() + \
                hashlib.md5(self.velocities.tostring()).hexdigest()

        self.history = [_hist[:15]]
        self.has_looped = False
        self.steps = 0

    def advance_time_step(self):
        if not self.has_looped:
            self.steps += 1
        for pos in range(3):
            # first apply gravity
            self.velocities[:, pos] += np.vectorize(
                lambda coord: (
                    sum(self.moons[:, pos] > coord) -
                    sum(self.moons[:, pos] < coord)
                )
            )(self.moons[:, pos])

        # then adjust positions
        self.moons += self.velocities

        _hist = hashlib.md5(self.moons.tostring()).hexdigest() + \
                hashlib.md5(self.velocities.tostring()).hexdigest()

        if _hist in self.history:
            self.has_looped = True
        else:
            self.history.append(_hist[:15])

    def calculate_energy(self):
        potential = np.sum(np.abs(self.moons), axis=1)
        kinetic = np.sum(np.abs(self.velocities), axis=1)

        return np.sum(potential * kinetic)


def load_input():
    moons = []
    with open('./input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            line = sub(r'[<>,]', '', line).split()

            _coords = dict(coord.split('=') for coord in line)
            moons.append(
                np.array(
                    (int(_coords['x']), int(_coords['y']), int(_coords['z']))
                )
            )
        return np.array(moons)


def main():
    orchestrator = Orchestrator(moons = load_input())
    for _ in range(1000):
        orchestrator.advance_time_step()

    print('Positions:\n{}'.format(orchestrator.moons))
    print('Velocities:\n{}'.format(orchestrator.velocities))
    print('Energy:\t{}'.format(orchestrator.calculate_energy()))

    while not orchestrator.has_looped:
        orchestrator.advance_time_step()
        if orchestrator.steps % 10000 == 0:
            # fuuuuuuuck this is slow and I should be better
            # at my job
            print(f'Iterated through {orchestrator.steps}...')
    print(f'Looped after {orchestrator.steps} steps')


if __name__ == '__main__':
    main()
