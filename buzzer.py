import serial

class BuzzerManager(object):
	def __init__(self, path):
		self.s = serial.Serial(path)
		self.s.open()
	def getBuzzer(self):
		print 'waiting for buzzer...'
		self.s.flushInput()
		resp = self.s.read()
		return ord(resp)

