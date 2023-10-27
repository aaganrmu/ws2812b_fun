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


    def render(self):
        