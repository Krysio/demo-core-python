from hashlib import sha256 as _sha256
from src.lib.buffer import buffer

def sha256(bytestr: bytes) -> bytes:
	return buffer(_sha256(bytestr).digest())

EMPTY_HASH_SHA256 = buffer.fromHex('0000000000000000000000000000000000000000000000000000000000000000')
