import neopixel

class Ledz:
	def __init__(self, rows, columns, pin, brightness=0.1):
		self._rows = rows
		self._columns = columns
		pixels = rows*columns
		self._pixels = neopixel.NeoPixel(pin, pixels, brightness=brightness, auto_write=False)
		self.calculate_led_matrix()

	def _led(self, x, y):
		if (y % 2 == 0):
			return y * self._columns + x
		else:
			return y*self._columns + self._columns-1-x

	def calculate_led_matrix(self):
		self._matrix = [[self._led(x,y) for y in range(0,self._rows)] for x in range(0,self._columns)]

	def set(self, x, y, colour):
		led = self._matrix[x][y]
		self._pixels[led]=colour

	def set_all(self, matrix):
		for x in range(0,self.columns):
			for y in range(0,self.columns):
				self.set(x,y,matrix[x][y])

	def show(self):
		self._pixels.show()
