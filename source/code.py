import board
import digitalio
import time
import random
from ledz.ledz import Ledz
from pattern.fire import Fire
from pattern.circles import Circles
from pattern.fireworks import Fireworks
from pattern.flow import Flow


from pattern.lines import Lines

# setup default blinking led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# setup pixel array
pin = board.GP0
rows = 16
columns = 16
leds = Ledz(rows,columns,pin,brightness=0.3)

TIME_MIN = 60
TIME_MAX = 60
patterns = [Fire, Circles, Fireworks, Flow]
patterns = [Flow]
# patterns = [Lines]
time_switch = 0
current_index = -1

# Main loop
while True:
    if time_switch < time.time():
        time_switch = time.time() + random.randint(TIME_MIN, TIME_MAX)
        old_index = current_index
        while current_index == old_index:
            current_index = random.randint(0,len(patterns)-1)
        pattern = patterns[current_index]
        current = pattern(leds)
    current.render()