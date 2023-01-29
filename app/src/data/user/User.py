from src.lib.structure import TypedStructure
from src.lib.buffer import buffer
from src.data.key.Key import Key

TYPE_USER_GROUP_ADMIN = 1
TYPE_USER_GROUP_USER = 2

TYPE_USER_ROOT = 0
TYPE_USER_ADMIN = 1
TYPE_USER_PUBLIC = 2
TYPE_USER_ANONIM = 3

@TypedStructure
class User:
	def readBuffer(self, buffer: buffer):
		self.type = buffer.readUleb128()
		return self

@User.type(TYPE_USER_ROOT)
class UserRoot:
	key: Key

	def readBuffer(self, buffer: buffer):
		self.key = Key.fromBuffer(buffer)
		return self

	def toBuffer(self) -> buffer:
		return buffer.concat([
			buffer.encodeUleb128(self.type),
			self.key.toBuffer()
		])
	
	def __strData__(self):
		return str(self.key)

@User.type(TYPE_USER_ADMIN)
class UserAdmin:
	version: int = 1
	id: int = 0
	level: int = 0
	timeStart: int = 0
	timeEnd: int = 0
	flags: int = 0
	key: Key

	def readBuffer(self, buffer: buffer):
		self.version = buffer.readUleb128()
		self.id = buffer.readUleb128()
		self.level = buffer.readUleb128()
		self.key = Key.fromBuffer(buffer)
		self.timeStart = buffer.readUleb128()
		self.timeEnd = buffer.readUleb128()
		self.flags = buffer.readUleb128()
		return self

	def toBuffer(self) -> buffer:
		return buffer.concat([
			buffer.encodeUleb128(self.type),
			buffer.encodeUleb128(self.version),
			buffer.encodeUleb128(self.id),
			buffer.encodeUleb128(self.level),
			self.key.toBuffer(),
			buffer.encodeUleb128(self.timeStart),
			buffer.encodeUleb128(self.timeEnd),
			buffer.encodeUleb128(self.flags)
		])

	def __strData__(self) -> str:
		result = "{"
		result += "version="+ str(self.version)
		result += ",id="+ str(self.id)
		result += ",level="+ str(self.level)
		result += ",key="+ str(self.key)
		result += ",timeStart="+ str(self.timeStart)
		result += ",timeEnd="+ str(self.timeEnd)
		result += ",flags="+ str(self.flags)
		result += "}"
		return result
