# Purpose: Boid class
import math
import pygame
from random import uniform
from sprite import Sprite


# TODO: implement mass


class Boid(Sprite):
    debug = True

    def __init__(
        self,
        position=pygame.math.Vector2(uniform(0, 1000), uniform(0, 1000)),
        velocity=pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1)),
        mass=1,
        max_force=2,
        target_velocity=5,
        neighborhood_range=1,
        neighborhood_angle=120,
    ):
        Boid.set_boundary()
        super().__init__(
            position,
            velocity,
            mass,
            max_force,
            target_velocity,
            neighborhood_range,
            neighborhood_angle,
        )
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
        self.debug = Boid.debug

    # TODO: implement flocking rules
    # call limit_force() before returning
    def separation(self, boids):
        return

    def alignment(self, boids):
        return

    def cohesion(self, boids):
        return

    def accelerate(self):
        diff = self.velocity.as_polar()[0] - self.target_velocity
        # TODO: toggle for drop off in acceleration
        if math.fabs(diff) > 0.2:
            return pygame.Vector2(diff * 0.5, self.velocity.as_polar()[1])
        else:
            return pygame.Vector2(0, self.velocity.as_polar()[1])

    # TODO: implement obstacle avoidance

    # TODO: implement goal seeking

    def update(self, dt, boids):
        steering = pygame.Vector2()

        if self.bounce:
            Exception("Not implemented")

        neighbors = self.get_neighbors(boids)
        if neighbors:
            separation = self.separation(neighbors)
            alignment = self.alignment(neighbors)
            cohesion = self.cohesion(neighbors)
            acceleration = self.accelerate()

            steering += separation + alignment + cohesion + acceleration

        super().update(dt, steering)

    def get_neighbors(self, boids):
        neighbors = []
        for boid in boids:
            if boid != self:
                distance = self.position.distance_to(boid.position)
                if distance < self.neighborhood_range:
                    neighbors.append(boid)
        return neighbors

    def __str__(self):
        return f"Boid at {self.position} with velocity {self.velocity.as_polar()}"

    def __eq__(self, other):
        return (
            self.position == other.position
            and self.velocity == other.velocity
            and self.mass == other.mass
        )

    def __hash__(self) -> int:
        return super.__hash__(self)


if __name__ == "__main__":
    b = Boid()
    print(b.__str__())
