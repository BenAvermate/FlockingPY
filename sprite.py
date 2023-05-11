import pygame
import math


# TODO: implement noise in velocity
# TODO: implement noise in acceleration
# TODO: implement toggle for wall bounce/wrapping


class Sprite(pygame.sprite.Sprite):
    image = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.polygon(image, (255, 255, 255), [(15, 5), (0, 2), (0, 8)])
    # pygame.draw.circle(image, (255, 255, 255), (5, 5), 50)

    def __init__(
        self,
        position,
        velocity,
        mass,
        max_force,
        target_velocity,
        neighborhood_range,
        neighborhood_angle,
    ):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.heading = 0.0
        self.bounce = False
        self.mass = mass
        self.max_force = max_force
        self.target_velocity = target_velocity
        self.neighborhood_range = neighborhood_range
        self.neighborhood_angle = neighborhood_angle

        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))

    def update(self, dt, steering):
        self.acceleration = steering * dt
        new_velocity = self.velocity + self.acceleration * dt
        speed, new_heading = new_velocity.as_polar()

        # TODO: implement max turn rate
        # _, old_heading = self.velocity.as_polar()
        # heading_diff = 180 - (180 - new_heading + old_heading) % 360
        # heading_diff = 180 - (new_heading - old_heading) % 360

        self.velocity.from_polar((speed, new_heading))

        # TODO: implement max speed

        self.position += self.velocity * dt

        if self.bounce:
            # TODO: bounce off walls
            Exception("Not implemented")
        else:
            self.wrap()

        self.image = pygame.transform.rotate(Sprite.image, -new_heading)

        if self.debug:
            print(self)

            center = pygame.Vector2((50, 50))

            velocity = pygame.Vector2(self.velocity)
            speed = velocity.length()
            velocity += center

            acceleration = pygame.Vector2(self.acceleration)
            acceleration += center

            steering = pygame.Vector2(steering)
            steering += center

            overlay = pygame.Surface((100, 100), pygame.SRCALPHA)
            overlay.blit(self.image, center - (10, 10))

            pygame.draw.line(overlay, pygame.Color("green"), center, velocity, 3)
            pygame.draw.line(
                overlay, pygame.Color("red"), center + (5, 0), acceleration + (5, 0), 3
            )
            pygame.draw.line(
                overlay, pygame.Color("blue"), center - (5, 0), steering - (5, 0), 3
            )

            self.image = overlay
            self.rect = overlay.get_rect(center=self.position)
        else:
            self.rect = self.image.get_rect(center=self.position)

    def wrap(self):
        if self.position.x < 0:
            self.position.x += Sprite.max_x
        elif self.position.x > Sprite.max_x:
            self.position.x -= Sprite.max_x

        if self.position.y < 0:
            self.position.y += Sprite.max_y
        elif self.position.y > Sprite.max_y:
            self.position.y -= Sprite.max_y

    @staticmethod
    def set_boundary(edge_distance_pct=5):
        info = pygame.display.Info()
        Sprite.max_x = info.current_w
        Sprite.max_y = info.current_h
        margin_w = Sprite.max_x * edge_distance_pct / 100
        margin_h = Sprite.max_y * edge_distance_pct / 100
        Sprite.edges = [
            margin_w,
            margin_h,
            Sprite.max_x - margin_w,
            Sprite.max_y - margin_h,
        ]

    def limit_force(self, force):
        if 0 < force.magnitude() > self.max_force:
            force.scale_to_length(self.max_force)
        return force
