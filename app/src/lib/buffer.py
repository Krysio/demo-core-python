from typing import Iterable

class buffer(bytearray):
	cursor: int = 0
	
	@staticmethod
	def fromHex(hex: str):
		return buffer.fromhex(hex)

	#region Magic

	def __str__(self):
		return '<buffer:'+ str(len(self)) +':'+ self.hex() +':'+ str(self.cursor) +'>'

	def __iter__(self):
		return self

	def __next__(self):
		if self.cursor >= len(self):
			raise StopIteration
		self.cursor += 1
		return self[self.cursor - 1]

	def __add__(self, second):
		return self.concat([self, second])
	def __iadd__(self, second):
		return self.concat([self, second])

	def __lt__(self, other): return self.__compare_iterator(other, '<')
	def __le__(self, other): return self.__compare_iterator(other, '<=')
	def __eq__(self, other): return self.__compare_iterator(other, '==')
	def __ne__(self, other): return self.__compare_iterator(other, '!=')
	def __ge__(self, other): return self.__compare_iterator(other, '>=')
	def __gt__(self, other): return self.__compare_iterator(other, '>')

	def __compare_iterator(self, other, operator: str):
		assert type(other) == buffer
		lenA = len(self)
		lenB = len(other)
		if lenA != lenB:
			if operator == '==': return False
		maxLen = min(lenA, lenB)
		i = 0
		while i < maxLen:
			if self[i] != other[i]:
				if operator == '==': return False
				if self[i] < other[i]:
					if operator == '<': return True
					if operator == '<=': return True
					if operator == '>': return False
					if operator == '>=': return False
				else:
					if operator == '<': return False
					if operator == '<=': return False
					if operator == '>': return True
					if operator == '>=': return True
			i += 1
		if lenA != lenB:
			if operator == '!=': return True
			if lenA < lenB:
				if operator == '<': return True
				if operator == '<=': return True
			else:
				if operator == '>': return True
				if operator == '>=': return True
		else:
			if operator == '!=': return False
			if operator == '==': return True
			if operator == '>=': return True
			if operator == '<=': return True
	
	#endregion Magic
	#region Leb128

	@staticmethod
	def encodeLeb128(value: int):
		result = []
		while True:
			byte = value & 0x7f
			value = value >> 7
			if (value == 0 and byte & 0x40 == 0) or (value == -1 and byte & 0x40 != 0):
				result.append(byte)
				return buffer(result)
			result.append(0x80 | byte)

	@staticmethod
	def decodeLeb128(buffer: bytearray) -> int:
		result = 0
		for i, byte in enumerate(buffer):
			result = result + ((byte & 0x7f) << (i * 7))
		if byte & 0x40 != 0:
			result |= - (1 << (i * 7) + 7)
		return result

	#endregion Leb128
	#region Uleb128

	@staticmethod
	def encodeUleb128(value: int):
		assert value >= 0
		result = []
		i = 0
		while True:
			byte = value & 0x7f
			value = value >> 7
			i += 1
			if value == 0:
				result.append(byte)
				return buffer(result)
			result.append(0x80 | byte)

	@staticmethod
	def decodeUleb128(buffer) -> int:
		result = 0
		for i, byte in enumerate(buffer):
			result = result + ((byte & 0x7f) << (i * 7))
			if (byte & 0x80) == 0:
				break
		return result

	#endregion Uleb128
	#region Methods

	def toHex(self):
		return self.hex()

	def digest(self):
		return bytes(self)

	def lenRest(self) -> int:
		return len(self) - self.cursor
	
	def rest(self):
		return buffer(self[self.cursor:])

	def readLeb128(self):
		return self.decodeLeb128(self)

	def readUleb128(self):
		return self.decodeUleb128(self)

	def readBlob(self, size: int = 0):
		if size == 0:
			size = self.readUleb128()
		result = buffer(self[self.cursor:self.cursor + size])
		self.cursor += size
		return result

	def seek(self, cursorPosition: int):
		self.cursor = max(min(0, cursorPosition), len(self))

	@staticmethod
	def concat(iterable: Iterable[bytes | bytearray]):
		return buffer(bytearray().join(iterable))
	
	#endregion Methods

assert buffer.fromHex('01ff').readUleb128() == 1
assert buffer.encodeUleb128(1) == buffer.fromHex('01')
assert buffer.fromHex('8001').readUleb128() == 128
assert buffer.encodeUleb128(128) == buffer.fromHex('8001')
assert buffer.fromHex('e58e26').readUleb128() == 624485
assert buffer.encodeUleb128(624485) == buffer.fromHex('e58e26')
assert buffer.fromHex('e58e26ff').readUleb128() == 624485

assert buffer.fromHex('c0bb78').readLeb128() == -123456
assert buffer.fromHex('c0bb78ff').readLeb128() == -123456
assert buffer.encodeLeb128(-123456) == buffer.fromHex('c0bb78')

assert buffer.fromHex('1122') < buffer.fromHex('1133')
assert buffer.fromHex('1122') <= buffer.fromHex('1133')
assert buffer.fromHex('112211') < buffer.fromHex('1133')
assert buffer.fromHex('ffffffffff') > buffer.fromHex('eeeeeeeeeeee')
assert buffer.fromHex('ffffffffff') >= buffer.fromHex('eeeeeeeeeeee')
assert buffer.fromHex('ffffffffff') != buffer.fromHex('eeeeeeeeeeee')
assert False == (buffer.fromHex('ffffffffff') < buffer.fromHex('eeeeeeeeeeee'))
assert False == (buffer.fromHex('ffffffffff') <= buffer.fromHex('eeeeeeeeeeee'))
assert False == (buffer.fromHex('ffffffffff') == buffer.fromHex('eeeeeeeeeeee'))
assert buffer.fromHex('ffff') == buffer.fromHex('ffff')
assert buffer.fromHex('ffff11') > buffer.fromHex('ffff')
assert buffer.fromHex('ffff') < buffer.fromHex('ffff11')