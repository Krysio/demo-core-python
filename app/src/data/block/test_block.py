import unittest
from src.data.block.Block import Block

""" ****************************** """

class TestBlock(unittest.TestCase):
	def test_fromHex(self):
		hex = '01'+'01'+'01'+'e63bb9f57a5e2d4c66c3f72b9a9f2ebebd2c0e2900f19afae09ccebea6f0c3ec'+'03'+'05aaaaaaaaaa'+'06eeeeeeeeeeee'+'05ffffffffff'
		block = Block.fromHex(hex)

		self.assertEqual(hex, block.toBuffer().toHex())
