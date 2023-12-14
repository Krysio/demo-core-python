from __future__ import annotations
from abc import abstractmethod
from src.lib.buffer import buffer

__version__ = '1.0'

def Structure(cls):
	"""
	Decorator for buffer structures
	"""
	class ClassDecorator(cls):
		__className__ = cls.__name__

		@classmethod
		def fromBuffer(cls, buffer: buffer):
			"""
			Load data from buffer

			BaseClass.fromBuffer(buffer)

			:param buffer: Buffer with encoded data
			:type buffer: buffer
			:return: Self or SubClass instance
			:rtype: type[cls]
			"""
			return cls().readBuffer(buffer)

		@classmethod
		def fromBytes(cls, bytearray: bytes | bytearray | buffer):
			"""
			Load data from bytes

			BaseClass.fromBytes(bytes([1, 16, 32]))

			:param bytearray: Array with encoded data
			:type bytearray: bytes | bytearray | buffer
			:return: Self or SubClass instance
			:rtype: type[cls]
			"""
			return cls().readBuffer(buffer(bytearray))

		@classmethod
		def fromHex(cls, hex: str):
			"""
			Load data from hex-string

			BaseClass.fromHex('0102')

			:param hex: Hex-string with encoded data
			:type hex: string
			:return: Self or SubClass instance
			:rtype: type[cls]
			"""
			return cls().readBuffer(buffer.fromHex(hex))

		@abstractmethod
		def readBuffer(self, buffer):
			"""
			Load data from buffer

			:param buffer: Buffer with encoded data
			:type buffer: buffer
			:return: Self or SubClass instance
			:rtype: type[cls]
			"""
			return super().readBuffer()

		@abstractmethod
		def toBuffer(self) -> buffer:
			"""
			Serialize to buffer

			:return: Serialized buffer structure
			:rtype:	buffer
			"""
			return super().toBuffer()

	return ClassDecorator

def TypedStructure(cls):
	"""
	Decorator for buffer structures whith variants

	@TypedStructure
	class BaseClass:
		pass
	@BaseClass.type(1)
	class SubClass:
		pass
	"""
	mapOfSubclasses = {}

	class ClassDecorator(cls):
		""" copy the class name """
		__className__ = cls.__name__
		type = 0
		invalid = False

		def readBuffer(self, buffer):
			"""
			Load data from buffer

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
			"""
			Load data from buffer

			BaseClass.fromBuffer(buffer)

			:param buffer: Buffer with encoded data
			:type buffer: buffer
			:return: Self or SubClass instance
			:rtype: type[cls]
			"""
			return cls().readBuffer(buffer)

		@classmethod
		def fromBytes(cls, bytearray: bytes | bytearray | buffer):
			"""
			Load data from bytes

			BaseClass.fromBytes(bytes([1, 16, 32]))

			:param bytearray: Array with encoded data
			:type bytearray: bytes | bytearray | buffer
			:return: Self or SubClass instance
			:rtype: type[cls]
			"""
			return cls().readBuffer(buffer(bytearray))

		@classmethod
		def fromHex(cls, hex: str):
			"""
			Load data from hex-string

			BaseClass.fromHex('0102')

			:param hex: Hex-string with encoded data
			:type hex: string
			:return: Self or SubClass instance
			:rtype: type[cls]
			"""
			return cls().readBuffer(buffer.fromHex(hex))

		@classmethod
		def type(cls, type):
			"""
			Decorator that gets a type for sub classes

			@TypedStructure
			class BaseClass:
				pass
			@BaseClass.type(1)
			class SubClass:
				pass

			:param type: Type of sub class
			:type type: int
			"""
			def decorator(child_cls):
				class Override(child_cls, cls):
					def __init__(cls):
						cls.__className__ = child_cls.__name__
						cls._cls = child_cls
						cls.type = type
				
				mapOfSubclasses[type] = Override

				return Override
			return decorator

		@abstractmethod
		def toBuffer(self) -> buffer:
			"""
			Serialize to buffer

			:return: Serialized buffer structure
			:rtype:	buffer
			"""
			return super().toBuffer()

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

	return ClassDecorator
