import time
from math import ceil

from PRNG import PRNG


class LCG(PRNG):
    """
    Implementação de Gerador Linear Congruente (LCG - Linear Congruential Generator).
    Parâmetros (a, c, m) baseados na implementação ANSI C (Saucier, R. (2000). Computer Generation of Statistical Distributions)
    """

    def __init__(self, seed=None):
        # Parâmetros do LCG
        self.m = 2**32
        self.a = 1103515245
        self.c = 12345

        if seed is None:
            # tempo do sistema como seed
            self.state = int(time.time() * 1e6)
        else:
            self.state = seed

    def next(self):
        """Gera o próximo número pseudo-aleatório."""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def randbits(self, k):
        """
        Gera um número pseudo-aleatório com exatamente k bits.
        Para garantir k bits, o bit mais significativo é sempre 1.
        """
        if k <= 0:
            return 0

        num_words = ceil(k / 32)

        rand_val = 0
        for _ in range(num_words):
            rand_val = (rand_val << 32) | self.next()

        # garantindo que número tem k bits
        rand_val &= (1 << k) - 1
        rand_val |= 1 << (k - 1)  # força MSB a ser 1

        return rand_val


if __name__ == "__main__":
    lcg = LCG(seed=12345)
    print("10 números pseudo-aleatórios gerados pelo LCG:")
    for _ in range(10):
        print(lcg.next())

    print("\nNúmeros pseudo-aleatórios com 10 bits:")
    for _ in range(10):
        print(bin(lcg.randbits(4096)))
