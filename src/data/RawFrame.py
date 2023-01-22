from src.lib.buffer import buffer

FRAME_TYPE_TXN = 1
FRAME_TYPE_BLOCK = 2

VALID_TYPES = [FRAME_TYPE_TXN, FRAME_TYPE_BLOCK]

class RawFrame:
	def __init__common(self):
		try:
			self.version = self.buffer.readUleb128()
			self.type = self.buffer.readUleb128()
			self.data = self.buffer.rest()
			self.invalid = False
		except:
			self.invalid = True
	def __init__(self, buffer: buffer):
		self.buffer = buffer
		self.__init__common()
	def __init__(self, bytearray: bytearray):
		self.buffer = buffer(bytearray)
		self.__init__common()

	### Magic

	def __str__(self) -> str:
		if self.invalid:
			return "<RawFrame !>"
		else:
			return "<RawFrame v:"+ str(self.version) +" t:"+ str(self.type) +" d:"+ str(len(self.data)) +">"

	### Methods

	def isValid(self) -> bool:
		if self.invalid: return False
		if not self.type in VALID_TYPES: return False
		if len(self.data) <= 0: return False
		return True
