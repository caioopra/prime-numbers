from time import time
from math import ceil

from PRNG import PRNG


class XORShift(PRNG):
    """
    Implementação de um gerador Xorshift de 128 bits.
    O estado é composto por quatro inteiros de 32 bits.
    Referência: Marsaglia, G. (2003). Xorshift RNGs.
    """

    def __init__(self, seed=None):
        if seed is None:
            seed = int(time() * 1e6)

        # inicialização do estado com base na
        self.x = seed & 0xFFFFFFFF
        self.y = (seed >> 32) & 0xFFFFFFFF
        self.z = (seed >> 64) & 0xFFFFFFFF
        self.w = (seed >> 96) & 0xFFFFFFFF

        # garantir que nenhum estado seja zero
        if self.x == 0 and self.y == 0 and self.z == 0 and self.w == 0:
            self.x = 1  # o estado não pode ser todo zero

    def next(self):
        """Gera o próximo número pseudo-aleatório (32 bits)"""
        t = self.x ^ (self.x << 11) & 0xFFFFFFFF

        self.x, self.y, self.z = self.y, self.z, self.w

        self.w = (self.w ^ (self.w >> 19)) ^ (t ^ (t >> 8))

        return self.w

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
        rand_val |= 1 << (k - 1)

        return rand_val


if __name__ == "__main__":
    xorshift = XORShift(seed=12345)
    print("10 números pseudo-aleatórios gerados pelo XORShift:")
    for _ in range(10):
        print(xorshift.next())

    print("\nNúmeros pseudo-aleatórios com 10 bits:")
    for _ in range(10):
        print(bin(xorshift.randbits(10)))
