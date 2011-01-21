import serial

class BuzzerHandler(object)
	def __init__(self, path):
		self.s = serial.Serial(path)
	def getBuzzer(self):
		self.s.flushInput()
		return int(self.s.read())

