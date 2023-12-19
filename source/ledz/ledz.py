import math
import neopixel
from ledz.pos import Pos


# modification of range() that's usefull for drawing pixels between points
def path(start, stop):
    if start < stop:
        return range(start, stop + 1)
    else:
        return range(stop, start + 1)

class Ledz:
    def __init__(self, rows, columns, pin, brightness=0.1):
        self._rows = rows
        self._columns = columns
        pixels = rows*columns
        self._pixels = neopixel.NeoPixel(pin, pixels, brightness=brightness, auto_write=False)
        self.calculate_led_matrix()

    # Maps x and y into a led number. The leds are in a back and forth snake pattern
    def _led(self, x, y):
        if (y % 2 == 0):
            return y * self._columns + x
        else:
            return y*self._columns + self._columns-1-x

    def calculate_led_matrix(self):
        self._matrix = [[self._led(x,y) for y in range(0,self._rows)] for x in range(0,self._columns)]

    def set(self, x, y, colour):
        try:
            led = self._matrix[x][y]
        except IndexError:
            return

        self._pixels[led]=colour
        
    def set_all(self, matrix):
        for x in range(0,self.columns):
            for y in range(0,self.columns):
                self.set(x,y,matrix[x][y])

    def fill(self, colour):
        self._pixels.fill(colour)

    def rect(self, pos1, pos2, colour):
        for x in path(pos1.x, pos2.x):
            for y in path(pos1.y, pos2.y):
                self.set(x, y, colour)


    def bres_line_high(self, pos1, pos2, colour):
        return


    def show(self):
        self._pixels.show()

    @property
    def columns(self):
        return self._columns

    @property
    def rows(self):
        return self._rows

