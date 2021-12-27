import random


def generate_key(n):

    return bytes([random.randrange(0, 256) for i in range(n)])


def xor(key, message):
    length = min(len(key), len(message))
    return bytes([key[i] ^ message[i] for i in range(length)])


message = b"ATTACK"
key = generate_key(len(message))
cipher = xor(key=key, message=message)

print(cipher)

print(xor(key=key, message=cipher))
