# Purpose: flock class
from random import uniform
import math

import pygame

from boid import Boid

# TODO: implement world size


class Flock:
    def __init__(self, flock_size=10):
        self.boids = []
        self.flock_size = flock_size

        for _ in range(flock_size):
            self.new_boid()

    def new_boid(self):
        if len(self.boids) < self.flock_size:
            self.boids.append(
                Boid(
                    pygame.math.Vector2(uniform(0, 1000), uniform(0, 1000)),
                    pygame.math.Vector2.from_polar((uniform(0, 20), uniform(0, 180))),
                    target_velocity=uniform(8, 15),
                )
            )
        else:
            print("Flock size exceeded")

    def add_boids(self, sprites: pygame.sprite.Group):
        print("adding boids")
        for boid in self.boids:
            # TODO: implement debug-toggle
            if boid.debug:
                print(boid)
            sprites.add(boid)

    def update(self, dt, world_size):
        for boid in self.boids:
            boid.update(dt, world_size)

    def __str__(self):
        return f"\tFlock of {len(self.boids)} boids:\n{chr(10).join(chr(9) + chr(9) + str(b) for b in self.boids)}"


if __name__ == "__main__":
    f = Flock()
    print(f)
