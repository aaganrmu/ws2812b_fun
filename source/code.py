import board
import digitalio
import time
from ledz.ledz import Ledz
from pattern.fire import Fire
from pattern.circles import Circles


# setup default blinking led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# setup pixel array
pin = board.GP0
rows = 16
columns = 16
leds = Ledz(rows,columns,pin)



current_pattern = Fire(leds)

# Main loop
while True:
    current_pattern.render()