from abc import abstractmethod
from src.lib.buffer import buffer
from src.data.Key import Key, KeySecp256k1

TYPE_USER_GROUP_ADMIN = 1
TYPE_USER_GROUP_USER = 2

TYPE_USER_ROOT = 0
TYPE_USER_ADMIN = 1
TYPE_USER_PUBLIC = 2
TYPE_USER_ANONIM = 3

mapOfTypes = {}

class User:
	invalid: bool = False
	type: int = 0

	#region Buffer

	def readBuffer(self, buffer: buffer):
		try:
			self.type = buffer.readUleb128()
			if self.type in mapOfTypes:
				return mapOfTypes[self.type].fromBuffer(buffer)
		except:
			self.invalid = True
		return self
	
	@staticmethod
	def fromBuffer(buffer: buffer):
		return User().readBuffer(buffer)

	@staticmethod
	def fromBytes(bytearray: bytes | bytearray | buffer):
		return User().readBuffer(buffer(bytearray))

	@staticmethod
	def fromHex(hex: str):
		return User().readBuffer(buffer.fromHex(hex))

	@abstractmethod
	def toBuffer(self) -> buffer: pass

	#endregion Buffer
	#region Magic

	def __str__(self) -> str:
		if self.invalid:
			return "<User !>"
		else:
			return "<User type="+ str(self.type) +">"

	#endregion Magic

class UserRoot(User):
	type: int = TYPE_USER_ROOT

	#region Buffer

	def readBuffer(self, buffer: buffer):
		try:
			self.key = KeySecp256k1.fromBuffer(buffer)
		except:
			self.invalid = True
		return self
	
	@staticmethod
	def fromBuffer(buffer: buffer):
		return UserRoot().readBuffer(buffer)

	@staticmethod
	def fromBytes(bytearray: bytes | bytearray | buffer):
		return UserRoot().readBuffer(buffer(bytearray))

	@staticmethod
	def fromHex(hex: str):
		return UserRoot().readBuffer(buffer.fromHex(hex))

	def toBuffer(self) -> buffer:
		return buffer.concat([
			buffer.encodeLeb128(self.type),
			self.key.toBuffer()
		])

	#endregion Buffer
	#region Magic

	def __str__(self) -> str:
		if self.invalid:
			return "<UserRoot !>"
		else:
			return "<UserRoot:key="+ str(self.key) +">"

	#endregion Magic

mapOfTypes[TYPE_USER_ROOT] = UserRoot

class UserAdmin(User):
	type: int = TYPE_USER_ADMIN
	version: int = 1
	id: int = 0
	level: int = 0
	timeStart: int = 0
	timeEnd: int = 0
	flags: int = 0

	#region Buffer

	def readBuffer(self, buffer: buffer):
		try:
			self.version = buffer.readUleb128()
			self.id = buffer.readUleb128()
			self.level = buffer.readUleb128()
			self.key = Key.fromBuffer(buffer)
			self.timeStart = buffer.readUleb128()
			self.timeEnd = buffer.readUleb128()
			self.flags = buffer.readUleb128()
		except:
			self.invalid = True
		return self
	
	@staticmethod
	def fromBuffer(buffer: buffer):
		return UserAdmin().readBuffer(buffer)

	@staticmethod
	def fromBytes(source):
		"""
		:param source: Data source
		:type source: bytes | bytearray | buffer
		:return: Self Instance
		:rtype: UserAdmin
		"""
		return UserAdmin().readBuffer(buffer(source))

	@staticmethod
	def fromHex(hex: str):
		return UserAdmin().readBuffer(buffer.fromHex(hex))

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

	#endregion Buffer
	#region Magic

	def __str__(self) -> str:
		if self.invalid:
			return "<UserAdmin !>"
		else:
			result = "<UserAdmin"
			result += ":version="+ str(self.version)
			result += ":id="+ str(self.id)
			result += ":level="+ str(self.level)
			result += ":key="+ str(self.key)
			result += ":timeStart="+ str(self.timeStart)
			result += ":timeEnd="+ str(self.timeEnd)
			result += ":flags="+ str(self.flags)
			result += ">"
			return result

	#endregion Magic

mapOfTypes[TYPE_USER_ADMIN] = UserAdmin

#region Tests

rootUser = User.fromHex('000102230d022655e3087cfa5725a70ba5c342389d37faa3fcc8ef9760a2b19d59107e')
print(rootUser)
adminUser = UserAdmin()
adminUser.id = 33
adminUser.level = 2
adminUser.key = KeySecp256k1.fromHex('02bdf16174de309bdfcc8b969fe80b7cb93a98bac0ca657f86d9963d4b2e6ded16')
adminUser.timeEnd = 32232
adminUser.timeStart = 100
print(adminUser)
adminUserBuffer = adminUser.toBuffer()
print(User.fromBuffer(adminUserBuffer))

assert rootUser.type == TYPE_USER_ROOT

#endregion Tests
