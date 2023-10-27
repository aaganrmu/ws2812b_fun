import board
import digitalio
import time
import random
from ledz.ledz import Ledz


# setup
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# setup pixel array
pin = board.GP0
rows = 16
columns = 16
leds = Ledz(rows,columns,pin)

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

def colourmap(i):
    j = (i * 0.0039)
    black = min(20,i)*0.05
    r = i * black
    g = i * (0.5 + 0.5* j) * black
    b = max(i-200, 0) * black + black*5
    return (r, g, b)

# create matrix with some extra size
matrix = [[0 for y in range(0,rows+1)] for x in range(0,columns+2)]

DIFFUSION = 0.5
DAMPENING = 1.05
RANDOM_DAMPENING = 15
UPSPEED = 0.65

side_factor = DIFFUSION * DAMPENING * UPSPEED
center_factor = (1 - DIFFUSION) * DAMPENING * UPSPEED
self_factor = 1-UPSPEED

# Main loop
while True:
    for x in range(0, columns+2):
        matrix[x][0] = random.randint(0,255)
    for y in range(rows,0,-1):
        for x in range(1, columns + 1):
            offset = random.random()
            left =  matrix[x-1][y-1] * offset *side_factor
            middle = matrix[x][y-1] * center_factor
            right = matrix[x+1][y-1] * (1 - offset) * side_factor
            original = matrix[x][y] * self_factor 
            total = (int)(left+middle+right+original - random.randint(0,RANDOM_DAMPENING))
            if total < 0:
                total = 0
            matrix[x][y] = total

    for y in range(0, rows):
        for x in range(0, columns):
            leds.set(x,y,colourmap(matrix[x+1][y+1]))

    leds.show()