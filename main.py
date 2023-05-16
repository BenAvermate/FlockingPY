import argparse
import pygame
import sys
from world import World
from pygame.locals import *

global world

default_size = {"x": 1000, "y": 1000}
default_boids = 50
default_flocks = 1

fps = 30


def generate_world(sprites, flocks=default_flocks, boids=default_boids):
    global world
    world = World(flocks, boids, default_size)
    print(world)
    add_sprites(sprites)


def draw_sprites(screen, background, sprites):
    sprites.clear(screen, background)
    dirty = sprites.draw(screen)
    pygame.display.update(dirty)


def add_sprites(sprites):
    world.add_flocks(sprites)


def update(dt, sprites):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == KEYDOWN:
            mods = pygame.key.get_mods()
            if event.key == pygame.K_q:
                # quit
                pygame.quit()
                sys.exit(0)
            elif event.key == pygame.K_UP:
                # add boids
                if mods & pygame.KMOD_SHIFT:
                    add_sprites(sprites, 100)
                else:
                    add_sprites(sprites, 10)
            elif event.key == pygame.K_DOWN:
                # remove boids
                if mods & pygame.KMOD_SHIFT:
                    sprites.remove(sprites.sprites()[:100])
                else:
                    sprites.remove(sprites.sprites()[:10])
            elif event.key == pygame.K_d:
                # toggle debug
                for boid in sprites:
                    boid.debug = not boid.debug
            elif event.key == pygame.K_r:
                # reset
                world.reset()
                sprites.empty()
                add_sprites(sprites)

    for sprite in sprites:
        sprite.update(dt, sprites)


def main(args):
    pygame.init()

    clock = pygame.time.Clock()

    pygame.display.set_caption("Flocking")
    window_width, window_height = [int(x) for x in args.geometry.split("x")]
    flags = pygame.DOUBLEBUF

    screen = pygame.display.set_mode((window_width, window_height), flags)
    screen.set_alpha(None)
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(pygame.Color("black"))

    sprites = pygame.sprite.RenderUpdates()

    # FIXME: use the args for spawning boids and flocks
    generate_world(sprites, args.num_flocks, args.num_boids)

    dt = 1 / fps

    while True:
        update(dt, sprites)
        draw_sprites(screen, background, sprites)
        dt = clock.tick(fps) / fps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Emergent flocking.")
    parser.add_argument(
        "--geometry",
        metavar="WxH",
        type=str,
        default=f"{default_size['x']}x{default_size['y']}",
        help="geometry of window",
    )
    parser.add_argument(
        "--number_of_boids",
        dest="num_boids",
        default=default_boids,
        help="number of boids to generate",
    )
    parser.add_argument(
        "--number_of_flocks",
        dest="num_flocks",
        default=default_flocks,
        help="number of flocks to generate",
    )
    args = parser.parse_args()

    main(args)

# pygame.init()
# screen = pygame.display.set_mode((size["x"], size["y"]))
# clock = pygame.time.Clock()
# running = True
# dt = 0

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # fill the screen with a color to wipe away anything from last frame
#     background = pygame.Surface(screen.get_size()).convert()
#     background.fill(pygame.Color("black"))

#     world.run()
#     # print(world)
#     boids = pygame.sprite.RenderUpdates()
#     boids.add(boid for flock in world.flocks for boid in flock.boids)
#     boids.clear(screen, background)
#     dirty = boids.draw(screen)
#     pygame.display.update(dirty)

#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_w]:
#         player_pos.y -= 300 * dt
#     if keys[pygame.K_s]:
#         player_pos.y += 300 * dt
#     if keys[pygame.K_a]:
#         player_pos.x -= 300 * dt
#     if keys[pygame.K_d]:
#         player_pos.x += 300 * dt

#     # flip() the display to put your work on screen
#     pygame.display.flip()

#     # limits FPS to 60
#     # dt is delta time in seconds since last frame, used for framerate-
#     # independent physics.
#     dt = clock.tick(60) / 1000

# pygame.quit()

# if __name__ == "__main__":
#     try:
#         steps = int(input("Amount many iterations (empty for infinite)? ") or -1)
#     except ValueError:
#         print("Invalid input")
#     else:
#         input(f'Press enter to start {steps if steps!=-1 else "infinite"} iterations')
#         print(world)
#         if steps < -1:
#             print("Invalid input")
#         elif steps == -1:
#             while True:
#                 world.run()
#                 print(world)
#                 time.sleep(0.1)
#         else:
#             for i in range(steps):
#                 world.run()
#                 print(world)
#                 time.sleep(0.01)
