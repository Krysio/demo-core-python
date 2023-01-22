from src.data.RawFrame import RawFrame
import src.data.Txn
import src.data.Key
import src.lib.structure
import src.lib.crypto.secp256k1

RawFrame(bytearray.fromhex('ff'))
test = RawFrame(bytearray.fromhex('e58e2601ff'))
print(test, test.isValid())
