from abc import ABC, abstractmethod
from src.data.Block import Block
from src.data.User import TYPE_USER_GROUP_ADMIN, TYPE_USER_GROUP_USER
from src.lib.buffer import buffer

class Txn:
	def __init__common(self):
		self.invalid = False
		try:
			if self.block:
				self.version = self.buffer.readUleb128()
			self.type = self.buffer.readUleb128()
			self.data = self.buffer.readBlob()
		except:
			self.invalid = True
	def __init__(self, bytearray: bytearray):
		self.buffer = buffer(bytearray)
		self.__init__common()
	def __init__(self, buffer: buffer):
		self.buffer = buffer
		self.__init__common()
	def __init__(self, bytearray: bytearray, block: Block):
		self.buffer = buffer(bytearray)
		self.block = block
		self.__init__common()
	def __init__(self, buffer: buffer, block: Block):
		self.buffer = buffer
		self.block = block
		self.__init__common()

	def isInternal() -> bool: return False
	def isSimple() -> bool: return False
	def isMultiSignet() -> bool: return False

	@abstractmethod
	def isValid() -> bool: pass

	@abstractmethod
	def getUserGroup() -> str: pass

class TxnInternal(Txn):
	def isInternal() -> bool: return True
	def isValid() -> bool: return True

class TxnSimple(Txn):
	def __init__common(self):
		super().__init__common()
		if not self.invalid:
			try:
				self.author = self.buffer.readUleb128()
				if self.getUserGroup() == TYPE_USER_GROUP_ADMIN:
					self.signedIndex = self.buffer.readUleb128()
				else:
					self.signedHash = self.buffer.readBlob(32)
			except:
				self.invalid = True

	def isSimple() -> bool: return True

class TxnMultiSigned(Txn):
	def isMultiSigned() -> bool: return True
