import string


def generate_key(shift):
    letters = string.ascii_letters[26:]
    key = {}
    num = 0
    for c in letters:
        key[c] = letters[(num + shift) % len(letters)]
        num += 1
    return key


def get_decryption_key(shift):
    dkey = {}
    letters = string.ascii_letters[26:]
    num = 0
    for c in letters:
        dkey[letters[(num + shift) % len(letters)]] = c
        num += 1
    return dkey


def encrypt(key, message):
    cipher = ""
    for c in message:
        if c in key:
            cipher += key[c]
        else:
            cipher += c
    return cipher


key = generate_key(3)
message = "ATTACK"
cipher = encrypt(key, message)
print(cipher)
dkey = get_decryption_key(3)
print(key)
print(dkey)
print(encrypt(dkey, cipher))
