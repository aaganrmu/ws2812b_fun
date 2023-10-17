import board
import digitalio
import time
import neopixel
import math

# setup
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# setup pixel array
pixel_pin = board.GP0
rows = 16
columns = 16

num_pixels = rows*columns

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)

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


# Converts coordinates to pixel number
def matrix(x, y):
    if (y % 2 == 0):
        return(y*columns+x)
    else:
        return(y*columns + columns-1-x)



i = 0
# Main loop
while True:

    for y in range(0,16):
        dy = rows/2 -0.5 -y 
        dysqr = dy*dy
        for x in range(0,16):
            dx = columns/2 - 0.5 - x
            dxsqr = dx*dx
            d = math.sqrt(dxsqr+dysqr)
            pixel = matrix(x,y)
            pixels[pixel]=rainbow(i+math.floor(d*25))
    pixels.show()
    i -= 2