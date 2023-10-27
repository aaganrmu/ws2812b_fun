import math
import random
from ledz.ledz import Ledz

SPEED = -3
RIPPLES = 32

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


class Circles():
    def __init__(self, leds):
        self._leds = leds
        self._x0 = random.uniform(0,self._leds.columns-1)
        self._y0 = random.uniform(0,self._leds.rows-1)
        self._i = 0


    def render(self):
        columns = self._leds.columns
        rows = self._leds.rows
        for y in range(0,rows):
            dy = math.pow((y - self._y0), 2)
            for x in range(0,columns):
                dx = math.pow((x - self._x0),2)
                d = (int)(math.sqrt(dx+dy) * RIPPLES + self._i)
                self._leds.set(x,y,rainbow(d))

        self._leds.show()
        self._i = (self._i + SPEED) % 255