import time
from math import ceil
from typing import Optional

from PRNG import PRNG


class LCG(PRNG):
    """
    Implementação de Gerador Linear Congruente (LCG - Linear Congruential Generator).

    O LCG utiliza a fórmula: X_{n+1} = (a * X_n + c) mod m
    onde a é o multiplicador, c é o incremento e m é o módulo.

    Parâmetros utilizados são baseados na implementação ANSI C, que proporcionam
    um período completo de 2^32 e boa distribuição para a maioria das aplicações.

    Características:
    - Algoritmo simples e rápido
    - Período de 2^32 (aproximadamente 4.3 bilhões)
    - Baixo uso de memória (apenas um estado)
    - Qualidade estatística moderada

    Referência: Saucier, R. (2000). "Computer Generation of Statistical Distributions"
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        # Parâmetros do LCG baseados no padrão ANSI C
        self.m = 2**32  # módulo: 2^32
        self.a = 1103515245  # multiplicador
        self.c = 12345  # incremento

        if seed is None:
            # usa timestamp atual como semente padrão
            self.state = int(time.time() * 1e6)
        else:
            self.state = seed

    def next(self) -> int:
        """
        Gera o próximo número pseudo-aleatório usando a fórmula LCG.

        Aplica a recorrência linear: state = (a * state + c) mod m

        Returns:
            int: próximo número da sequência pseudo-aleatória (32 bits)
        """
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def randbits(self, k: int) -> int:
        """
        Gera um número pseudo-aleatório com exatamente k bits.

        Combina múltiplas saídas do LCG quando k > 32. O bit mais significativo
        é sempre definido como 1 para garantir que o resultado tenha exatamente k bits.

        Args:
            k (int): número de bits desejados

        Returns:
            int: número com exatamente k bits pseudo-aleatórios
        """
        if k <= 0:
            return 0

        # calcula quantas palavras de 32 bits são necessárias
        num_words = ceil(k / 32)

        rand_val = 0
        for _ in range(num_words):
            rand_val = (rand_val << 32) | self.next()

        # aplica máscara para manter apenas k bits
        rand_val &= (1 << k) - 1
        # força o MSB para garantir exatamente k bits
        rand_val |= 1 << (k - 1)

        return rand_val


if __name__ == "__main__":
    lcg = LCG(seed=12345)
    print("10 números pseudo-aleatórios gerados pelo LCG:")
    for _ in range(10):
        print(lcg.next())

    print("\nNúmeros pseudo-aleatórios com 10 bits:")
    for _ in range(10):
        print(bin(lcg.randbits(4096)))
