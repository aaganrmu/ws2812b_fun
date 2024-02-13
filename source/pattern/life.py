import random
from ledz.ledz import Ledz

SPEED = 4

def rainbow(i):
    i = i%256
    if i < 85:
        return (255-i*3, i*3, 0)
    if i < 170:
        i -= 85
        return (0, 255-i*3, i*3, 0)
    i -= 170
    return (i*3, 0, 255- 3*i)

def scaler(colour, i):
    return tuple(chan*i/255 for chan in colour)

base_colour_i  = random.randint(0,255)

def colourmap(i):
    return scaler(rainbow(i+base_colour_i),i)

colour_lut = [colourmap(i) for i in range(256)]

class Life():
    def __init__(self, leds):
        self._leds = leds
        columns = self._leds.columns
        rows = self._leds.rows
        self._cells = [[random.choice([True, False]) for y in range(0,rows)] for x in range(0,columns)]
        self._colours = [[0  for y in range(0,rows)] for x in range(0,columns)]
        self._timer = 0

    def _alive(self, x, y):
        left = (x-1) % self._leds.columns
        right = (x+1) % self._leds.columns
        top = (y+1) % self._leds.columns
        bottom = (y-1) % self._leds.columns
        neighbours = self._cells[left][top] + self._cells[x][top] + self._cells[right][top] + \
                     self._cells[left][y] +                          self._cells[right][y] + \
                     self._cells[left][bottom] + self._cells[x][bottom] + self._cells[right][bottom]
        if neighbours == 2:
            return self._cells[x][y]
        elif neighbours == 3:
            return True
        return False

    def render(self):
        columns = self._leds.columns
        rows = self._leds.rows
        # Simulate life
        self._timer += SPEED
        if self._timer > 255:
            self._timer = 0
            new_cells = [[self._alive(x,y)
                for y in range(0,rows)] 
                for x in range(0,columns)]
            self._cells = new_cells


        for y in range(0, rows):
            for x in range(0, columns):
                colour = self._colours[x][y]
                if self._cells[x][y]:
                    colour = colour + SPEED
                    if colour > 255:
                        colour = 255
                else:
                    colour = colour - SPEED
                    if colour < 0:
                        colour = 0
                self._colours[x][y] = colour
                self._leds.set(x,y,colour_lut[colour])
        self._leds.show()
