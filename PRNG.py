from abc import ABC, abstractmethod


class PRNG(ABC):
    """
    Classe abstrata base para geradores de números pseudo-aleatórios (PRNGs).

    Define a interface comum que todos os PRNGs devem implementar,
    garantindo compatibilidade entre diferentes algoritmos de geração.
    """

    @abstractmethod
    def next(self) -> int:
        """
        Gera o próximo número pseudo-aleatório da sequência.

        Returns:
            int: próximo número da sequência pseudo-aleatória
        """
        pass

    @abstractmethod
    def randbits(self, k: int) -> int:
        """
        Gera um número inteiro com exatamente k bits pseudo-aleatórios.

        Args:
            k (int): número de bits desejados

        Returns:
            int: número inteiro com k bits, onde o bit mais significativo é sempre 1
        """
        pass
