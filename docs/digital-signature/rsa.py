from Crypto.PublicKey import RSA

key_pair = RSA.generate(bits=1024)
print("Public key:")
print(f' N={hex(key_pair.n)}')
print(f' e={hex(key_pair.e)}')
print("Private key:")
print(f' N={hex(key_pair.n)}')
print(f' d={hex(key_pair.d)}')


# RSA sign the message
msg = b'A message for signing'
from hashlib import sha512
hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
signature = pow(hash, key_pair.d, key_pair.n)
print("Signature:", hex(signature))