# Purpose: World class for the boids simulation
from flock import Flock


class World:
    def __init__(self, number_of_flocks=1, flock_size=10, size={"x": 100, "y": 100}):
        self.size = size
        self.flocks = []
        self.number_of_flocks = number_of_flocks

        for i in range(number_of_flocks):
            self.new_flock(flock_size)

    def new_flock(
        self,
        flock_size=10,
    ):
        if len(self.flocks) < self.number_of_flocks:
            self.flocks.append(Flock(flock_size))
        else:
            print("Flocks exceeded")

    def add_flocks(self, sprites):
        print("adding flocks")
        for flock in self.flocks:
            flock.add_boids(sprites)

    def update(self, dt):
        for flock in self.flocks:
            flock.update(dt, self.size)

    def __str__(self):
        while next(self.print()):
            return next(self.print())

    def print(self):
        yield f"World of {len(self.flocks)} flocks:\n{chr(10).join(str(f) for f in self.flocks)}"


if __name__ == "__main__":
    w = World()
    print(w)
