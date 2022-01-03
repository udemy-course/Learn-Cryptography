import random


def is_prime(n):
    return n > 1 and all(n % i for i in range(2, int(n ** 0.5) + 1))


def get_prime(size):

    while True:
        num = random.randrange(size, size ** 2)
        if is_prime(num):
            return num


p = get_prime(100)
q = get_prime(100)

N = p * q

print(f"p={p}")
print(f"q={q}")
print(f"N=p*q={p*q}")


p = 718411
q = 686149
r = (p - 1) * (q - 1)
e = 65537


def get_d(e, r):
    for d in range(2, r):
        if d * e % r == 1:
            return d

    return False


d = get_d(e, r)
if d:
    print(d)
