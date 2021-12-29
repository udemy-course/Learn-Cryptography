def lcg(m, a, c, seed):
    """Linear congruential generator."""
    return (a * seed + c) % m


# https://en.wikipedia.org/wiki/Linear_congruential_generator
m = 2 ** 31
a = 1103515245
c = 12345
seed = 1

for _ in range(10):
    rand_n = lcg(m, a, c, seed)
    print(rand_n)
    seed = rand_n
