from primalidade import fermat_test, miller_rabin_test


def gcd(a: int, b: int) -> int:
    """
    Calcula o máximo divisor comum usando o algoritmo de Euclides.

    Args:
        a (int): primeiro número
        b (int): segundo número

    Returns:
        int: máximo divisor comum de a e b
    """
    while b:
        a, b = b, a % b
    return a


def fermat_test_coprime_bases(n: int, k: int = 20) -> bool:
    """
    Teste de Fermat usando apenas bases coprimas com n.

    Esta versão específica demonstra a vulnerabilidade fundamental do teste de Fermat
    para números de Carmichael. Um número de Carmichael é um número composto n tal que
    a^(n-1) ≡ 1 (mod n) para todo inteiro a coprimo com n.

    Diferenças da versão padrão:
    - Só testa bases que são coprimas com n (gcd(a,n) = 1)
    - Garante que todos os números de Carmichael passarão no teste
    - Demonstra por que o teste de Fermat não é confiável

    Args:
        n (int): número a ser testado para primalidade
        k (int): número de bases coprimas a serem testadas (padrão: 20)

    Returns:
        bool: False se n é composto, True se provavelmente primo (ou Carmichael)
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # encontra k bases coprimas com n, começando de 2
    coprime_bases = []
    candidate = 2
    while len(coprime_bases) < k and candidate < n:
        if gcd(candidate, n) == 1:
            coprime_bases.append(candidate)
        candidate += 1

    # se não encontramos bases coprimas suficientes, n é muito pequeno ou tem muitos fatores
    if len(coprime_bases) < k:
        return False

    # aplica o teste de Fermat para cada base coprima
    for base in coprime_bases:
        if pow(base, n - 1, n) != 1:
            return False  # encontrou uma testemunha, n é composto

    return True


def test_carmichael_vulnerability() -> None:
    """
    Demonstra a vulnerabilidade do teste de Fermat para números de Carmichael.

    Testa três números de Carmichael conhecidos (561, 1105, 1729) usando:
    1. Teste de Fermat com bases aleatórias (pode ocasionalmente detectar composição)
    2. Teste de Fermat com bases coprimas (sempre falhará em detectar composição)
    3. Teste de Miller-Rabin (detectará corretamente que são compostos)

    Os números de Carmichael são a razão pela qual o teste de Fermat
    não é considerado um teste de primalidade confiável.
    """

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

