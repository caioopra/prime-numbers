import random


def fermat_test(n, k=20):
    """
    Teste de primalidade de Fermat.

    Retorna False se n é composto. True se provavelmente n é primo.
    Vulnerável a números de Carmichael
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


def miller_rabin_test(n, k=20):
    """
    Teste de primalidade de Miller-Rabin.

    Retorna False se n é composto, True se n é provavelmente primo.

    k é o número de rodadas, aumentando a confiança.
    Probabilidade de erro para n composto: (1/4)^k.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # escreve n-1 como 2^s * d, onde d é ímpar
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        is_composite = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                is_composite = False
                break

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
