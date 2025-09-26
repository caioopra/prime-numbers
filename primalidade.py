import random


def fermat_test(n: int, k: int = 20) -> bool:
    """
    Teste de primalidade de Fermat baseado no Pequeno Teorema de Fermat.

    Verifica se a^(n-1) ≡ 1 (mod n) para k bases aleatórias.
    Se alguma base falhar no teste, n é composto com certeza.
    Se todas as bases passarem, n é provavelmente primo.

    Limitações:
    - Vulnerável a números de Carmichael (compostos que passam no teste para todas as bases coprimas)
    - Probabilidade de erro não é facilmente calculável devido aos números de Carmichael

    Args:
        n (int): número a ser testado para primalidade
        k (int): número de bases aleatórias a serem testadas (padrão: 20)

    Returns:
        bool: False se n é composto, True se provavelmente primo
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False

    return True


def miller_rabin_test(n: int, k: int = 20) -> bool:
    """
    Teste de primalidade de Miller-Rabin, uma extensão mais robusta do teste de Fermat.

    Baseia-se no fato de que se n é primo ímpar e n-1 = 2^s × d (onde d é ímpar),
    então para qualquer base a coprima com n:
    - ou a^d ≡ 1 (mod n)
    - ou a^(2^r × d) ≡ -1 (mod n) para algum r ∈ [0, s-1]

    Vantagens sobre Fermat:
    - Não é vulnerável a números de Carmichael
    - Probabilidade de erro bem definida: no máximo (1/4)^k para n composto
    - Determinístico para números pequenos com bases específicas

    Args:
        n (int): número a ser testado para primalidade
        k (int): número de rodadas/bases a serem testadas (padrão: 20)

    Returns:
        bool: False se n é composto, True se provavelmente primo
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # decomposição: escreve n-1 como 2^s × d, onde d é ímpar
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        # escolhe base aleatória no intervalo [2, n-2]
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        # primeira condição: a^d ≡ 1 (mod n) ou a^d ≡ -1 (mod n)
        if x == 1 or x == n - 1:
            continue

        # testa as potências subsequentes: a^(2^r × d) para r = 1, 2, ..., s-1
        is_composite = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:  # encontrou a^(2^r × d) ≡ -1 (mod n)
                is_composite = False
                break

        # se nenhuma condição foi satisfeita, n é composto
        if is_composite:
            return False

    return True


if __name__ == "__main__":
    # fun fact: aleatoriamente digitei um valor (121235111), que é primo :)
    num = int(input("Digite um número para testar a primalidade: "))
    if fermat_test(num):
        print(f"{num} é provavelmente primo.")
    else:
        print(f"{num} é composto.")

    if miller_rabin_test(num):
        print(f"{num} é provavelmente primo.")
    else:
        print(f"{num} é composto.")
