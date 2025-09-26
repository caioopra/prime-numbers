from time import time
from math import ceil
from typing import Optional

from PRNG import PRNG


class XORShift(PRNG):
    """
    Implementação de um gerador pseudo-aleatório xorshift de 128 bits.

    Utiliza operações XOR e deslocamentos de bits para gerar números pseudo-aleatórios
    de alta qualidade e período longo. o estado interno é mantido em quatro registradores
    de 32 bits cada, proporcionando um período de aproximadamente 2^128 - 1.

    Características:
    - Período extremamente longo (2^128 - 1)
    - Operações rápidas (apenas XOR e shifts)
    - Boa distribuição estatística
    - Pequeno uso de memória (4 palavras de 32 bits)

    Referência: Marsaglia, G. (2003). "Xorshift RNGs". Journal of Statistical Software.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        if seed is None:
            seed = int(time() * 1e6)

        # inicialização do estado interno dividindo a semente em quatro palavras de 32 bits
        self.x = seed & 0xFFFFFFFF
        self.y = (seed >> 32) & 0xFFFFFFFF
        self.z = (seed >> 64) & 0xFFFFFFFF
        self.w = (seed >> 96) & 0xFFFFFFFF

        # garantir que o estado não seja completamente zero (condição degenerada)
        if self.x == 0 and self.y == 0 and self.z == 0 and self.w == 0:
            self.x = (
                1  # pelo menos um valor deve ser não-zero para funcionamento correto
            )

    def next(self) -> int:
        """
        Gera o próximo número pseudo-aleatório de 32 bits usando o algoritmo xorshift.

        Aplica transformações XOR com deslocamentos específicos (11, 19, 8) que foram
        escolhidos por Marsaglia para maximizar o período e a qualidade estatística.

        Returns:
            int: número pseudo-aleatório de 32 bits
        """
        # primeira transformação: XOR com deslocamento à esquerda
        t = self.x ^ (self.x << 11) & 0xFFFFFFFF

        # rotação do estado: x←y, y←z, z←w
        self.x, self.y, self.z = self.y, self.z, self.w

        # segunda transformação: combina deslocamentos à direita de w e t
        self.w = (self.w ^ (self.w >> 19)) ^ (t ^ (t >> 8))

        return self.w

    def randbits(self, k: int) -> int:
        """
        Gera um número pseudo-aleatório com exatamente k bits.

        Combina múltiplas chamadas de next() quando necessário para obter
        o número desejado de bits. O bit mais significativo é sempre definido
        como 1 para garantir que o número tenha exatamente k bits.

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
    xorshift = XORShift(seed=12345)
    print("10 números pseudo-aleatórios gerados pelo XORShift:")
    for _ in range(10):
        print(xorshift.next())

    print("\nNúmeros pseudo-aleatórios com 10 bits:")
    for _ in range(10):
        print(bin(xorshift.randbits(10)))
