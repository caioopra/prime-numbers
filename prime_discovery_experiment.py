"""
Experimento de Descoberta de Números Primos

Este módulo implementa um experimento que utiliza o gerador LCG para produzir
candidatos ímpares e testa sua primalidade usando os testes de Miller-Rabin e Fermat.
Mede o tempo necessário para encontrar o primeiro número primo para cada tamanho de bits.
"""

import time
import statistics
from typing import Dict, List, Tuple

from LCG import LCG
from primalidade import miller_rabin_test, fermat_test


class PrimeDiscoveryExperiment:
    """Experimento para medir tempo de descoberta de números primos"""

    def __init__(self):
        self.tamanhos_bits = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
        self.seed_experimento = 42
        self.resultados = {}

    def gerar_candidato_impar(self, prng: LCG, bits: int) -> int:
        """Gera um candidato ímpar usando o LCG"""
        candidato = prng.randbits(bits)
        # Garantir que é ímpar
        if candidato % 2 == 0:
            candidato |= 1
        return candidato

    def buscar_primo(self, bits: int) -> Dict:
        """
        Busca o primeiro número primo para um dado número de bits.
        Retorna dicionário com estatísticas da busca.
        """
        prng = LCG(seed=self.seed_experimento)

        inicio = time.perf_counter()
        candidatos_testados = 0

        while True:
            candidatos_testados += 1
            candidato = self.gerar_candidato_impar(prng, bits)

            # Testar com Miller-Rabin (k=20)
            miller_rabin_resultado = miller_rabin_test(candidato, k=20)

            # Testar com Fermat (k=20)
            fermat_resultado = fermat_test(candidato, k=20)

            # Se qualquer um dos testes classifica como primo, paramos
            if miller_rabin_resultado or fermat_resultado:
                fim = time.perf_counter()
                tempo_decorrido = (fim - inicio) * 1000  # ms

                return {
                    'primo_encontrado': candidato,
                    'bits': bits,
                    'tempo_ms': tempo_decorrido,
                    'candidatos_testados': candidatos_testados,
                    'miller_rabin_positivo': miller_rabin_resultado,
                    'fermat_positivo': fermat_resultado,
                    'ambos_positivos': miller_rabin_resultado and fermat_resultado
                }

    def executar_experimento_completo(self) -> Dict:
        """Executa o experimento completo para todos os tamanhos de bits"""

        print("=" * 80)
        print("EXPERIMENTO DE DESCOBERTA DE NÚMEROS PRIMOS")
        print("=" * 80)
        print(f"Seed utilizado: {self.seed_experimento}")
        print("Testes de primalidade: Miller-Rabin (k=20) e Fermat (k=20)")
        print("Critério de parada: Primeiro número classificado como primo por qualquer teste")
        print()

        for bits in self.tamanhos_bits:
            print(f"\nTESTANDO GERAÇÃO DE PRIMOS COM {bits} BITS:")
            print("-" * 50)

            resultado = self.buscar_primo(bits)
            self.resultados[bits] = resultado

            # Mostrar resultados
            print(f"Primo encontrado: {resultado['primo_encontrado']}")
            print(f"Tempo decorrido: {resultado['tempo_ms']:.6f} ms")
            print(f"Candidatos testados: {resultado['candidatos_testados']}")
            print(f"Miller-Rabin positivo: {'Sim' if resultado['miller_rabin_positivo'] else 'Não'}")
            print(f"Fermat positivo: {'Sim' if resultado['fermat_positivo'] else 'Não'}")
            print(f"Ambos testes positivos: {'Sim' if resultado['ambos_positivos'] else 'Não'}")

        self._gerar_relatorio()

        return self.resultados

    def _gerar_relatorio(self):
        """Gera relatório final dos resultados"""

        print("\n" + "=" * 80)
        print("RELATÓRIO FINAL - DESCOBERTA DE PRIMOS")
        print("=" * 80)

        print(f"\n{'Bits':<8} {'Tempo (ms)':<15} {'Candidatos':<12} {'Miller-Rabin':<13} {'Fermat':<8} {'Ambos':<8}")
        print("-" * 70)

        tempos = []
        candidatos_total = []
        miller_rabin_sucessos = 0
        fermat_sucessos = 0
        ambos_sucessos = 0

        for bits in self.tamanhos_bits:
            resultado = self.resultados[bits]
            tempos.append(resultado['tempo_ms'])
            candidatos_total.append(resultado['candidatos_testados'])

            if resultado['miller_rabin_positivo']:
                miller_rabin_sucessos += 1
            if resultado['fermat_positivo']:
                fermat_sucessos += 1
            if resultado['ambos_positivos']:
                ambos_sucessos += 1

            mr_result = 'Sim' if resultado['miller_rabin_positivo'] else 'Não'
            fermat_result = 'Sim' if resultado['fermat_positivo'] else 'Não'
            both_result = 'Sim' if resultado['ambos_positivos'] else 'Não'

            print(f"{bits:<8} {resultado['tempo_ms']:<15.6f} {resultado['candidatos_testados']:<12} "
                  f"{mr_result:<13} {fermat_result:<8} {both_result}")

        # Estatísticas finais
        print("\n" + "-" * 70)
        print("ESTATÍSTICAS RESUMO:")
        print(f"Tempo médio: {statistics.mean(tempos):.6f} ms")
        print(f"Tempo mínimo: {min(tempos):.6f} ms")
        print(f"Tempo máximo: {max(tempos):.6f} ms")
        print(f"Desvio padrão dos tempos: {statistics.stdev(tempos):.6f} ms")
        print()
        print(f"Candidatos médios testados: {statistics.mean(candidatos_total):.1f}")
        print(f"Total de candidatos testados: {sum(candidatos_total)}")
        print()
        print(f"Sucessos Miller-Rabin: {miller_rabin_sucessos}/{len(self.tamanhos_bits)} ({miller_rabin_sucessos/len(self.tamanhos_bits)*100:.1f}%)")
        print(f"Sucessos Fermat: {fermat_sucessos}/{len(self.tamanhos_bits)} ({fermat_sucessos/len(self.tamanhos_bits)*100:.1f}%)")
        print(f"Ambos testes positivos: {ambos_sucessos}/{len(self.tamanhos_bits)} ({ambos_sucessos/len(self.tamanhos_bits)*100:.1f}%)")


def main():
    """Função principal para executar o experimento"""

    print("Iniciando experimento de descoberta de números primos...")
    print("Este processo pode levar alguns minutos dependendo do hardware.\n")

    # Criar e executar experimento
    experimento = PrimeDiscoveryExperiment()

    inicio_total = time.time()
    resultados = experimento.executar_experimento_completo()
    fim_total = time.time()

    # Tempo total
    tempo_total = fim_total - inicio_total
    print(f"\n{'=' * 80}")
    print("EXPERIMENTO CONCLUÍDO")
    print(f"{'=' * 80}")
    print(f"Tempo total de execução: {tempo_total:.2f} segundos")

    return resultados


if __name__ == "__main__":
    resultados = main()