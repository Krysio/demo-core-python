import unittest
from src.lib.crypto.secp256k1 import secp256k1
from src.lib.buffer import buffer

""" ****************************** """

message = buffer.fromHex('315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3')

""" ****************************** """

class TestStructure(unittest.TestCase):
	def test_signing(self):
		success, privateKey, publicKey = secp256k1.getKeys()
		self.assertTrue(success)

		success, signature = secp256k1.sign(message, privateKey)
		self.assertTrue(success)

		self.assertTrue(secp256k1.verify(
			signature, message, publicKey
		))

	def test_example(self):
		# <Buffer:32:2ac900b6fe2eda30be37cebdc39ac3cddefae7b17898ce930f5bfae0d7bfed00:0> private
		# <Buffer:33:0246dd57d4137e2d7cb7926844ad0f2cc4dc2bbdc4e8a10b6bb8d2bbf586cf5da5:0> public
		# <Buffer:64:932ebac414ca8c74b9cd7e9e18a732a1d3e2bed4c260ec015c5c43d634d619a62fa137a2ba88421ec93fe05e14d2bfb553f1a0034535109ad63933bb6fbe4bb9:0> signature
		self.assertTrue(secp256k1.verify(
			buffer.fromHex('932ebac414ca8c74b9cd7e9e18a732a1d3e2bed4c260ec015c5c43d634d619a62fa137a2ba88421ec93fe05e14d2bfb553f1a0034535109ad63933bb6fbe4bb9'),
			message,
			buffer.fromHex('0246dd57d4137e2d7cb7926844ad0f2cc4dc2bbdc4e8a10b6bb8d2bbf586cf5da5')
		))

if __name__ == '__main__':
	unittest.main()
