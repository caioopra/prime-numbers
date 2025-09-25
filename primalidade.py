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


if __name__ == "__main__":
    # fun fact: aleatoriamente digitei um valor (121235111), que é primo :)
    num = int(input("Digite um número para testar a primalidade: "))
    if fermat_test(num):
        print(f"{num} é provavelmente primo.")
    else:
        print(f"{num} é composto.")
