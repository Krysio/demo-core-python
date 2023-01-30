import unittest
from src.data.block.Block import Block

""" ****************************** """

hexBase = '01'+'01'+'01'+'e63bb9f57a5e2d4c66c3f72b9a9f2ebebd2c0e2900f19afae09ccebea6f0c3ec'
hex1 = hexBase +'03'+'05aaaaaaaaaa'+'06eeeeeeeeeeee'+'05ffffffffff'
hex2 = hexBase +'03'+'06eeeeeeeeeeee'+'05aaaaaaaaaa'+'05ffffffffff'

class TestBlock(unittest.TestCase):
	def test_fromHex(self):
		block = Block.fromHex(hex1)

		self.assertEqual(hex1, block.toBuffer().toHex())
	
	def test_sortTxns(self):
		block = Block.fromHex(hex2)

		self.assertEqual(hex1, block.toBuffer().toHex())

	def test_iter(self):
		block = Block.fromHex(hex2)
		array = []

		i = 0

		for txn in block:
			array.append(txn)
			i += 1
			if i > 3:
				break

		self.assertEqual('aaaaaaaaaa', array[0].toHex())
		self.assertEqual('eeeeeeeeeeee', array[1].toHex())
		self.assertEqual('ffffffffff', array[2].toHex())
		self.assertEqual(i, 3)

	def test_hash(self):
		block1 = Block.fromHex(hex1)
		block2 = Block.fromHex(hexBase)
		hash1 = block1.getHash().toHex()
		hash2 = block1.getHash().toHex()
		hash3 = block2.getHash().toHex()

		self.assertEqual(hash1, hash2)
		self.assertNotEqual(hash1, hash3)
