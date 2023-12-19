import random
from ledz.ledz import Ledz

BLUR = 0.20
FADE = 0.999
CORNER = 0.5
SPEED = 0.1
BRIGHTNESS = 60
STARTVALUE = 10

OTHERS = (BLUR)/4*FADE
SELF = (1-BLUR)*FADE

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
    return tuple(int(chan*(i+1)/256)for chan in colour)

base_colour_i  = random.randint(0,255)
base_colour = rainbow(random.randint(0,255))
def colourmap(i):
    colour = scaler(rainbow(i+base_colour_i),i)
    print(colour) 
    return colour


colour_lut = [colourmap(i) for i in range(256)]

dx_lut = [SPEED,SPEED*0.71,0,-SPEED*0.71,-SPEED,-SPEED*0.71,0,SPEED*0.71]
dy_lut = [0,-SPEED*0.71,-SPEED,-SPEED*0.71,0,SPEED*0.71,SPEED,SPEED*0.71]
class Flow():
    def __init__(self, leds):
        self._leds = leds
        # create matrix with some extra size to simplify mirroring.
        # One extra column left/right
        # One extra row at top/bottom
        columns = self._leds.columns
        rows = self._leds.rows
        self._matrix = [[STARTVALUE for y in range(0,rows+2)] for x in range(0,columns+2)]

        # Set start position and direction of 'bug'
        self._x = random.randint(0, columns)
        self._y = random.randint(0, rows)
        self._dir = random.randint(0,7)

    def render(self):
        columns = self._leds.columns
        rows = self._leds.rows

        self._x = (self._x + dx_lut[self._dir]) % columns
        self._y = (self._y + dy_lut[self._dir]) % rows

        if random.random() < CORNER*SPEED:
            self._dir = (self._dir + random.randint(-1,1)) % 8


        x = int(self._x) + 1
        y = int(self._y) + 1
        new_value = self._matrix[x][y] + BRIGHTNESS
        if new_value > 255:
            new_value = 255
        self._matrix[x][y] = new_value

        
        # Go through all rows
        for y in range(1, rows + 1):
            # Go through each pixel in a row
            for x in range(1, columns + 1):
                left =  self._matrix[x-1][y]
                right = self._matrix[x+1][y]
                bottom = self._matrix[x][y-1]
                top = self._matrix[x][y+1]
                original = self._matrix[x][y] 
                total = ((left+right+top+bottom)*OTHERS + original * SELF)
                self._matrix[x][y] = total

        # Copy edges
        for y in range(1, rows + 1):
            self._matrix[0][y] = self._matrix[columns][y]
            self._matrix[columns+1][y] = self._matrix[1][y]
        for x in range(1, columns + 1):
            self._matrix[x][0] = self._matrix[x][rows]
            self._matrix[x][rows+1] = self._matrix[x][1]




        # convert fire to led ligths
        for y in range(0, rows):
            for x in range(0, columns):
                self._leds.set(x,y,colour_lut[int(self._matrix[x+1][y+1])]) 

        self._leds.show()