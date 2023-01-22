import unittest
from src.lib.structure import TypedStructure

""" ****************************** """

@TypedStructure
class Base:
	def readBuffer(self, buffer):
		self.type = buffer.readUleb128()
		return self
	def baseMethod(self):
		return 1
	def overrideMethod(self):
		return 3

@Base.type(2)
class Sub:
	def readBuffer(self, buffer):
		self.data = buffer.readUleb128()
		return self
	def subMethod(self):
		return 2
	def overrideMethod(self):
		return 4

""" ****************************** """

class TestStructure(unittest.TestCase):
	def test_fromHex(self):
		result = Base.fromHex('0202')

		self.assertEqual(result.type, 2)

	def test_methods(self):
		sub = Base.fromHex('0202')

		self.assertEqual(sub.baseMethod(), 1)
		self.assertEqual(sub.subMethod(), 2)
		self.assertEqual(sub.overrideMethod(), 4)
	
	def test_toString(self):
		self.assertEqual(str(Base.fromHex('0102')), '<Base:!>')
		self.assertEqual(str(Base.fromHex('0202')), '<Sub:type=2>')

if __name__ == '__main__':
	unittest.main()
