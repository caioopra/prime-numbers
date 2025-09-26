from primalidade import fermat_test, miller_rabin_test


def gcd(a, b):
    """Calcula o máximo divisor comum"""
    while b:
        a, b = b, a % b
    return a


def fermat_test_coprime_bases(n, k=20):
    """
    Teste de Fermat usando apenas bases coprimas com n.
    Esta versão demonstra a vulnerabilidade dos números de Carmichael.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Encontra k bases coprimas com n
    coprime_bases = []
    candidate = 2
    while len(coprime_bases) < k and candidate < n:
        if gcd(candidate, n) == 1:
            coprime_bases.append(candidate)
        candidate += 1

    # Se não encontramos k bases coprimas, o número provavelmente é muito pequeno
    if len(coprime_bases) < k:
        return False

    # Testa cada base coprima
    for base in coprime_bases:
        if pow(base, n - 1, n) != 1:
            return False

    return True


def test_carmichael_vulnerability():
    """Demonstra a vulnerabilidade do teste de Fermat para números de Carmichael"""

    carmichael_numbers = [561, 1105, 1729]

    print("=== Demonstração da Vulnerabilidade do Teste de Fermat ===\n")

    for num in carmichael_numbers:
        print(f"Testando {num} (número de Carmichael):")

        # Teste de Fermat original (com bases aleatórias)
        fermat_random = fermat_test(num, k=20)

        # Teste de Fermat apenas com bases coprimas
        fermat_coprime = fermat_test_coprime_bases(num, k=20)

        # Miller-Rabin
        miller_rabin = miller_rabin_test(num, k=20)

        print(f"  Fermat (bases aleatórias, k=20): {fermat_random}")
        print(f"  Fermat (apenas bases coprimas, k=20): {fermat_coprime}")
        print(f"  Miller-Rabin (k=20): {miller_rabin}")

        # Verificação manual da composição
        factors = []
        if num == 561:
            factors = [3, 11, 17]
        elif num == 1105:
            factors = [5, 13, 17]
        elif num == 1729:
            factors = [7, 13, 19]

        if factors:
            product = 1
            for f in factors:
                product *= f
            print(f"  Verificação: {num} = {' × '.join(map(str, factors))} = {product}")

        print()


if __name__ == "__main__":
    test_carmichael_vulnerability()

