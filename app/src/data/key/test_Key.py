import unittest
from src.data.key.Key import Key
from src.lib.buffer import buffer

""" ****************************** """

class TestKey(unittest.TestCase):
	def test_example(self):
		# <buffer:32:e76bdb31e051e985376c804dade738800450e2861ff08015b1f63b712669cb62:0> private
		# <buffer:33:03576a47bbe0a97797aa96564e77d4ca27c2aaf630e7a08196c2c4481f09418522:0> public
		# <buffer:32:315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3:0> message
		# <buffer:32:6246efc88ae4aa025e48c9c7adc723d5c97171a1fa6233623c7251ab8e57602f:0> hash(message)
		# <buffer:64:0f4146612479a9e3f577b7757ba33da239152272b717e3ffbe96f48276160aaf45da41056dcaaf5b46e7574eb83ccf978c24749016048b19712cf308640c2ba3:0> signature(hash(message))
		key = Key.fromHex('0103576a47bbe0a97797aa96564e77d4ca27c2aaf630e7a08196c2c4481f09418522')

		self.assertEqual(str(key), '<KeySecp256k1:03576a47bbe0a97797aa96564e77d4ca27c2aaf630e7a08196c2c4481f09418522>')
		self.assertTrue(key.verifySignature(
			buffer.fromHex('0f4146612479a9e3f577b7757ba33da239152272b717e3ffbe96f48276160aaf45da41056dcaaf5b46e7574eb83ccf978c24749016048b19712cf308640c2ba3'),
			buffer.fromHex('315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3')
		))
