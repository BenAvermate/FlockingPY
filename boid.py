# Purpose: Boid class
import math
import pygame
from random import uniform
from sprite import Sprite


# TODO: implement mass


class Boid(Sprite):
    debug = False

    def __init__(
        self,
        position=pygame.math.Vector2(uniform(0, 1000), uniform(0, 1000)),
        velocity=pygame.math.Vector2.from_polar((uniform(0, 20), uniform(0, 180))),
        mass=1,
        max_force=2,
        target_velocity=uniform(8, 15),
        perception_range=70,
        neighborhood_range=35,
        neighborhood_angle=120,
    ):
        Boid.set_boundary()
        super().__init__(
            position,
            velocity,
            mass,
            max_force,
            target_velocity,
            perception_range,
            neighborhood_range,
            neighborhood_angle,
        )
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
        self.debug = Boid.debug

    def separation(self, boids):
        separation = pygame.Vector2()
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if distance < self.neighborhood_range:
                separation += self.position - boid.position
        return self.limit_force(separation)

    def alignment(self, boids):
        steering = pygame.Vector2()
        for boid in boids:
            steering += boid.velocity
        steering /= len(boids)
        steering -= self.velocity
        return self.limit_force(steering) / 8

    def cohesion(self, boids):
        steering = pygame.Vector2()
        for boid in boids:
            steering += boid.position
            steering /= len(boids)
            steering -= self.position
        return self.limit_force(steering) / 100

    def accelerate(self):
        diff = self.target_velocity - self.velocity.as_polar()[0]
        # TODO: toggle for drop off in acceleration
        if math.fabs(diff) > 0.2:
            return pygame.Vector2.from_polar((diff * 0.1, self.velocity.as_polar()[1]))
        else:
            return pygame.Vector2.from_polar((0, self.velocity.as_polar()[1]))

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
            steering += separation + alignment + cohesion

        acceleration = self.accelerate()
        steering += acceleration
        super().update(dt, steering)

    # TODO: implement neighborhood angle
    def get_neighbors(self, boids):
        neighbors = []
        for boid in boids:
            if boid != self:
                distance = self.position.distance_to(boid.position)
                if distance < self.perception_range:
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
