import random
from ledz.ledz import Ledz

DIFFUSION = 0.5
DAMPENING = 1.05
RANDOM_DAMPENING = 15
UPSPEED = 0.65

side_factor = DIFFUSION * DAMPENING * UPSPEED
center_factor = (1 - DIFFUSION) * DAMPENING * UPSPEED
self_factor = 1-UPSPEED

# def colourmap(i):
#     black = min(20,i)*0.05
#     r = i * black
#     g = i * black* 0.3
#     b = 0
#     return (r, g, b)

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
base_colour = rainbow(random.randint(0,255))
def colourmap(i):
    return scaler(rainbow(i+base_colour_i),i)


colour_lut = [colourmap(i) for i in range(256)]

class Fire():
    def __init__(self, leds):
        self._leds = leds
        # create matrix with some extra size to calculate fire effect.
        # One extra column left/right
        # One extra row at bottom for 'firewood'
        columns = self._leds.columns
        rows = self._leds.rows
        self._matrix = [[0 for y in range(0,rows+1)] for x in range(0,columns+2)]
        for x in range(0, columns+2):
            self._matrix[x][0] = random.randint(0,255)


    def render(self):
        columns = self._leds.columns
        rows = self._leds.rows
        # Manipulate 'firewood'
        for x in range(0, columns+2):
            self._matrix[x][0] = (self._matrix[x][0] + random.randint(0,10)) % 255


        # Update each row of fire based on what's below
        for y in range(rows,0,-1):
            # Set 'wind' for this row
            offset = random.random()
            left_factor = offset*side_factor
            right_factor = (1-offset)*side_factor

            # Go through each pixel in a row
            for x in range(1, columns + 1):
                left =  self._matrix[x-1][y-1] * left_factor
                middle = self._matrix[x][y-1] * center_factor
                right = self._matrix[x+1][y-1] * right_factor
                original = self._matrix[x][y] * self_factor 
                total = (left+middle+right+original - random.randint(0,RANDOM_DAMPENING))
                if total < 0:
                    total = 0
                if total >= 255:
                    total = 255
                self._matrix[x][y] = total

        # convert fire to led ligths
        for y in range(0, rows):
            for x in range(0, columns):
                self._leds.set(x,y,colour_lut[int(self._matrix[x+1][y+1])])

        self._leds.show()
