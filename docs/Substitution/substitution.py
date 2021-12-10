import string
import random


def generate_key():
    letters = [l for l in string.ascii_letters[26:]]
    random.shuffle(letters)
    
    return dict(zip(string.ascii_letters[26:], letters))


def encrypt(key, message):
    cipher = ""
    for l in message:
        if l in key:
            cipher += key[l]
        else:
            cipher += ""
    return cipher

key = generate_key()
print(key)

print(encrypt(key, "ATTACK"))
