from coincurve.context import GLOBAL_CONTEXT
from coincurve._libsecp256k1 import ffi, lib
from coincurve.flags import EC_COMPRESSED
from coincurve.utils import (
	DEFAULT_NONCE,
	get_valid_secret
)
from src.lib.buffer import buffer

class secp256k1:
	@staticmethod
	def sign(message: buffer, privateKey: buffer) -> tuple[bool, buffer]:
		assert len(message) == 32
		signatureRaw = ffi.new('secp256k1_ecdsa_signature *')
		nonce_fn, nonce_data = DEFAULT_NONCE
		result = bool(lib.secp256k1_ecdsa_sign(
			GLOBAL_CONTEXT.ctx,
			signatureRaw,
			bytes(message),
			bytes(privateKey),
			nonce_fn,
			nonce_data
		))
		if result:
			signatureCompact = ffi.new('unsigned char[64]');
			result = bool(lib.secp256k1_ecdsa_signature_serialize_compact(
				GLOBAL_CONTEXT.ctx,
				signatureCompact,
				signatureRaw
			))
			if result:
				return True, buffer(ffi.buffer(signatureCompact, 64))
		return False, buffer()

	@staticmethod
	def verify(signatureCompact: buffer, message: buffer, publicKeyCompact: buffer) -> bool:
		assert len(signatureCompact) == 64
		signature = ffi.new('secp256k1_ecdsa_signature *')
		result = bool(lib.secp256k1_ecdsa_signature_parse_compact(
			GLOBAL_CONTEXT.ctx,
			signature,
			bytes(signatureCompact)
		))
		if result:
			publicKey = ffi.new('secp256k1_pubkey *')
			result = bool(lib.secp256k1_ec_pubkey_parse(
				GLOBAL_CONTEXT.ctx,
				publicKey,
				bytes(publicKeyCompact),
				33
			))
			if result:
				return bool(lib.secp256k1_ecdsa_verify(
					GLOBAL_CONTEXT.ctx,
					signature,
					bytes(message),
					publicKey
				))
		return False
	
	@staticmethod
	def getKeys() -> tuple[bool, buffer, buffer]:
		privateKey = get_valid_secret()
		publicKeyRaw = ffi.new('secp256k1_pubkey *')
		result = bool(lib.secp256k1_ec_pubkey_create(GLOBAL_CONTEXT.ctx, publicKeyRaw, privateKey))
		if result:
			publicKeyCompact = ffi.new('unsigned char [33]')
			lib.secp256k1_ec_pubkey_serialize(
				GLOBAL_CONTEXT.ctx,
				publicKeyCompact,
				ffi.new('size_t *', 33),
				publicKeyRaw,
				EC_COMPRESSED
			)
			return result, buffer(privateKey), buffer(ffi.buffer(publicKeyCompact, 33))
		return False, buffer(), buffer()
