import unittest
from src.data.user.User import User, UserRoot, UserAdmin, TYPE_USER_ROOT
from src.data.key.Key import Key, KeySecp256k1, TYPE_KEY_Secp256k1
from src.lib.buffer import buffer

""" ****************************** """

class TestUser(unittest.TestCase):	
	def test_create(self):
		adminUser = UserAdmin()
		adminUser.id = 33
		adminUser.level = 2
		adminUser.key = KeySecp256k1.fromHex('02bdf16174de309bdfcc8b969fe80b7cb93a98bac0ca657f86d9963d4b2e6ded16')
		adminUser.timeEnd = 32232
		adminUser.timeStart = 100

		adminUserBuffered = adminUser.toBuffer()
		adminUserFromBuffer = User.fromBuffer(adminUserBuffered)
	
		self.assertEqual(adminUserBuffered, adminUserFromBuffer.toBuffer())

	def test_fromHex(self):
		rootUser = User.fromHex('000102230d022655e3087cfa5725a70ba5c342389d37faa3fcc8ef9760a2b19d59107e')

		self.assertEqual(rootUser.type, TYPE_USER_ROOT)
		self.assertEqual(rootUser.key.type, TYPE_KEY_Secp256k1)
		self.assertEqual(rootUser.key.key.toHex(), '02230d022655e3087cfa5725a70ba5c342389d37faa3fcc8ef9760a2b19d59107e')

