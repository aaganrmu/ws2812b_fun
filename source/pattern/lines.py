
from ledz.ledz import Ledz
from ledz.pos import Pos
import random

def rainbow(i):
    i = i%256
    if i < 85:
        return (255-i*3, i*3, 0)
    if i < 170:
        i -= 85
        return (0, 255-i*3, i*3, 0)
    i -= 170
    return (i*3, 0, 255- 3*i)

class Lines():
    def __init__(self, leds):
        self._leds = leds

    def render(self):
        a = Pos(random.randint(0,15), random.randint(0,15))
        b = Pos(random.randint(0,15), random.randint(0,15))
        colour = rainbow(random.randint(0,255))
        self._leds.rect(a, b, colour)
        self._leds.show()
