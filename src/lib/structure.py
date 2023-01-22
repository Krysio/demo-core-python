from abc import abstractmethod
from src.lib.buffer import buffer

def TypedStructure(cls):
	mapOfSubclasses = {}

	class ClassDecorator(cls):
		__className__ = cls.__name__
		type = 0
		invalid = False

		def readBuffer(self, buffer):
			"""
			:param buffer: Buffer with encoded data
			:type buffer: buffer
			:return: Self or SubClass instance
			:rtype: type[cls]
			"""
			super().readBuffer(buffer)
			try:
				if self.type in mapOfSubclasses:
					return mapOfSubclasses[self.type].fromBuffer(buffer)
				else:
					self.invalid = True
			except:
				self.invalid = True
			return self

		@classmethod
		def fromBuffer(cls, buffer: buffer):
			return cls().readBuffer(buffer)

		@classmethod
		def fromBytes(cls, bytearray: bytes | bytearray | buffer):
			return cls().readBuffer(buffer(bytearray))

		@classmethod
		def fromHex(cls, hex: str):
			return cls().readBuffer(buffer.fromHex(hex))

		@abstractmethod
		def toBuffer(self) -> buffer: pass

		def __init__(self):
			self._cls = cls
		def __str__(self):
			result = '<'+ self.__className__
			if self.invalid:
				result += ':!'
			else:
				strData = self.__strData__()
				if strData:
					result += ':'+ strData
			result += '>'
			return result
		def __strData__(self):
			return ''

		@classmethod
		def type(cls, type):
			def decorator(child_cls):
				class Override(child_cls, cls):
					def __init__(cls):
						cls.__className__ = child_cls.__name__
						cls._cls = child_cls
						cls.type = type
				
				mapOfSubclasses[type] = Override

				return Override
			return decorator

	return ClassDecorator
