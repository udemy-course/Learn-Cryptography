def generate_key_bytes(seed, m=2 ** 31, a=1103515245, c=12345):
    """Linear congruential generator."""
    return (a * seed + c) % m % 256


def encrypt(key, message):
    return bytes([message[i] ^ key for i in range(len(message))])


message = b"ATTACK"

key = generate_key_bytes(seed=654321)

encrypted_message = encrypt(key, message)
print(encrypted_message)

decrypted_message = encrypt(key, encrypted_message)

print(decrypted_message)
