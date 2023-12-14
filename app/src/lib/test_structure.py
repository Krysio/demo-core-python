import unittest
from src.lib.structure import TypedStructure

""" ****************************** """

@TypedStructure
class BaseClass:
	def readBuffer(self, buffer):
		self.type = buffer.readUleb128()
		return self
	def baseMethod(self):
		return 1
	def overrideMethod(self):
		return 3

@BaseClass.type(2)
class SubClass:
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
		result = BaseClass.fromHex('0202')

		self.assertEqual(result.type, 2)

	def test_methods(self):
		sub = BaseClass.fromHex('0202')

		self.assertEqual(sub.baseMethod(), 1)
		self.assertEqual(sub.subMethod(), 2)
		self.assertEqual(sub.overrideMethod(), 4)
	
	def test_toString(self):
		self.assertEqual(str(BaseClass.fromHex('0102')), '<Base:!>')
		self.assertEqual(str(BaseClass.fromHex('0202')), '<Sub>')

if __name__ == '__main__':
	unittest.main()
