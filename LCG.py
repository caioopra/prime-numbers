import time


class LCG:
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
