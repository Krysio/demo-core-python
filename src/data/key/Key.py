from abc import abstractmethod
from src.lib.structure import TypedStructure
from src.lib.crypto.sha256 import sha256
from src.lib.crypto.secp256k1 import secp256k1
from src.lib.buffer import buffer

TYPE_KEY_Secp256k1 = 1

@TypedStructure
class Key:
	def readBuffer(self, buffer: buffer):
		self.type = buffer.readUleb128()
		return self

	@abstractmethod
	def verifySignature(self, signature, message) -> bool: pass

@Key.type(TYPE_KEY_Secp256k1)
class KeySecp256k1(Key):
	def readBuffer(self, buffer: buffer):
		self.key = buffer.readBlob(33)
		return self

	def toBuffer(self) -> buffer:
		return buffer.concat([
			buffer.encodeUleb128(self.type),
			self.key
		])

	def verifySignature(self, signature: buffer, content: buffer):
		message = sha256(content)
		return secp256k1.verify(signature, message, self.key)

	def __str__(self):
		return '<'+ self.__className__ +':'+ self.key.toHex() +'>'
