import math
import random

from ledz.ledz import Ledz

ROCKET_DELAY = 100
ROCKET_DELAY_VARIATION = 90
ROCKET_SPEED = 0.05
ROCKET_SPEED_VAR = 0.02
ROCKET_TTL_MIN = 130
ROCKET_TTL_MAX = 170

EXPLOSION_AMOUNT = 9
EXPLOSION_SPEED = 0.05
EXPLOSION_DAMPENING = 0.985
EXPLOSION_GRAVITY = 0.0005
EXPLOSION_TTL_MIN = 80
EXPLOSION_TTL_MAX = 120

# Rainbow colours
def rainbow(i):
    i = i%256
    if i < 85:
        return (255-i*3, i*3, 0)
    if i < 170:
        i -= 85
        return (0, 255-i*3, i*3, 0)
    i -= 170
    return (i*3, 0, 255- 3*i)

class Rocket():
    def __init__(self, leds, x0):
        self._leds = leds
        self._x = x0
        self._y = 0
        self._dx = 0
        self._dy = ROCKET_SPEED + random.uniform(0,ROCKET_SPEED_VAR)
        self._ttl = random.randint(ROCKET_TTL_MIN, ROCKET_TTL_MAX)

    def simulate(self):
        self._x += self._dx
        self._y += self._dy
        x = (int)(self._x)
        y = (int)(self._y)
        
        r = random.randint(40,100)
        g = random.randint(20,50)
        b = random.randint(0,10)
        self._leds.set(x,y, (r,g,b))
        self._ttl -= 1
        if self._ttl < 0:
            colour = rainbow(random.randint(0,255))
            return [Explosion(
                self._leds,
                self._x,
                self._y,
                random.uniform(-EXPLOSION_SPEED, EXPLOSION_SPEED),
                random.uniform(-EXPLOSION_SPEED, EXPLOSION_SPEED),
                colour
                ) for i in range(0,EXPLOSION_AMOUNT)]
        return [self]


class Explosion():
    def __init__(self, leds, x0, y0, dx, dy, colour):
        self._leds = leds
        self._x = x0
        self._y = y0
        self._dx = dx
        self._dy = dy
        self._colour = colour
        self._ttl = random.randint(ROCKET_TTL_MIN, ROCKET_TTL_MAX)

    def simulate(self):
        self._x += self._dx
        self._y += self._dy
        self._dx *= EXPLOSION_DAMPENING
        self._dy *= EXPLOSION_DAMPENING
        self._dy -= EXPLOSION_GRAVITY
        x = (int)(self._x)
        y = (int)(self._y)
        self._leds.set(x, y, self._colour)
        
        self._ttl -= 1
        if self._ttl < 0:
            return
        return [self]


class Fireworks():
    def __init__(self, leds):
        self._leds = leds
        self._particles = []
        self._reset_time()

    def _reset_time(self):
        self._time = random.randint(-ROCKET_DELAY_VARIATION, ROCKET_DELAY_VARIATION)
            
    def render(self):
        self._time += 1
        if self._time > ROCKET_DELAY:
            self._reset_time()
            rocket = Rocket(self._leds,random.randint(0, self._leds.columns-1))
            self._particles.append(rocket)
        self._leds.fill((0,0,0))
        columns = self._leds.columns

        newparticles = []
        for particle in self._particles:
            newparticle = particle.simulate()
            if newparticle:
                newparticles.extend(newparticle)

        self._particles = newparticles

        self._leds.show()