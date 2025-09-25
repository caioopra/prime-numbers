"""
Experimentos de Performance com Geradores de Números Pseudo-Aleatórios (PRNGs)

Este módulo realiza experimentos de performance com os algoritmos LCG (Linear Congruential Generator)
e XORShift implementados, medindo o tempo de geração de números com diferentes quantidades de bits.

Algoritmos testados:
- LCG (Linear Congruential Generator): Baseado na implementação ANSI C
- XORShift: Implementação de 128 bits baseada em Marsaglia (2003)
"""

import time
import statistics
from typing import List, Tuple, Dict, Any

from LCG import LCG
from XORShift import XORShift


class ExperimentosPRNG:
    """Classe para realizar experimentos de performance com PRNGs"""

    def __init__(self):
        self.tamanhos_bits = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
        self.num_amostras = 16
        self.resultados = {}

    def medir_tempo_geracao(self, prng, bits: int) -> Tuple[List[float], float]:
        """
        Mede o tempo de geração de números pseudo-aleatórios com k bits.

        Args:
            prng: Instância do gerador (LCG ou XORShift)
            bits: Número de bits para gerar

        Returns:
            Tupla contendo (tempos_individuais, tempo_médio)
        """
        tempos = []

        for _ in range(self.num_amostras):
            inicio = time.perf_counter()
            _ = prng.randbits(bits)
            fim = time.perf_counter()

            tempo_geracao = (fim - inicio) * 1000  # Converter para milissegundos
            tempos.append(tempo_geracao)

        tempo_medio = statistics.mean(tempos)
        return tempos, tempo_medio

    def executar_experimento_completo(self) -> Dict[str, Any]:
        """Executa o experimento completo para ambos os algoritmos"""

        print("=" * 80)
        print("EXPERIMENTOS DE PERFORMANCE - GERADORES PSEUDO-ALEATÓRIOS")
        print("=" * 80)
        print()

        # Inicializar geradores com seed fixo para reproducibilidade
        seed_experimento = 42

        for nome_algoritmo, classe_prng in [("LCG", LCG), ("XORShift", XORShift)]:
            print(f"\n{'=' * 50}")
            print(f"TESTANDO ALGORITMO: {nome_algoritmo}")
            print(f"{'=' * 50}")

            prng = classe_prng(seed=seed_experimento)
            resultados_algoritmo = {}

            print(f"\nGerador inicializado com seed: {seed_experimento}")
            print(f"Número de amostras por tamanho: {self.num_amostras}")
            print(f"Tamanhos de bits testados: {self.tamanhos_bits}")
            print("\n" + "-" * 80)

            for bits in self.tamanhos_bits:
                print(f"\nTESTANDO GERAÇÃO DE {bits} BITS:")
                print("-" * 40)

                # Reinicializar gerador para cada teste
                prng = classe_prng(seed=seed_experimento)

                tempos_individuais, tempo_medio = self.medir_tempo_geracao(prng, bits)

                # Calcular estatísticas adicionais
                tempo_min = min(tempos_individuais)
                tempo_max = max(tempos_individuais)
                desvio_padrao = (
                    statistics.stdev(tempos_individuais)
                    if len(tempos_individuais) > 1
                    else 0
                )

                # Armazenar resultados
                resultados_algoritmo[bits] = {
                    "tempos_individuais": tempos_individuais,
                    "tempo_medio_ms": tempo_medio,
                    "tempo_min_ms": tempo_min,
                    "tempo_max_ms": tempo_max,
                    "desvio_padrao_ms": desvio_padrao,
                }

                # Mostrar resultados formatados
                print(f"Tempo médio de geração: {tempo_medio:.6f} ms")
                print(f"Tempo mínimo: {tempo_min:.6f} ms")
                print(f"Tempo máximo: {tempo_max:.6f} ms")
                print(f"Desvio padrão: {desvio_padrao:.6f} ms")
                print(
                    f"Tempos individuais (ms): {[f'{t:.6f}' for t in tempos_individuais[:5]]}..."
                )

                # Verificar se o número gerado tem o tamanho correto
                numero_teste = prng.randbits(bits)
                bits_reais = numero_teste.bit_length()
                print(
                    f"Verificação: Número gerado tem {bits_reais} bits (esperado: {bits})"
                )

            self.resultados[nome_algoritmo] = resultados_algoritmo

        # Gerar resumo comparativo
        self._gerar_resumo_comparativo()

        return self.resultados

    def _gerar_resumo_comparativo(self):
        """Gera um resumo comparativo entre os algoritmos"""

        print("\n" + "=" * 80)
        print("RESUMO COMPARATIVO DE PERFORMANCE")
        print("=" * 80)

        print(
            f"\n{'Bits':<8} {'LCG (ms)':<15} {'XORShift (ms)':<15} {'Diferença':<12} {'Mais Rápido':<12}"
        )
        print("-" * 70)

        for bits in self.tamanhos_bits:
            tempo_lcg = self.resultados["LCG"][bits]["tempo_medio_ms"]
            tempo_xorshift = self.resultados["XORShift"][bits]["tempo_medio_ms"]

            diferenca = abs(tempo_lcg - tempo_xorshift)
            mais_rapido = "LCG" if tempo_lcg < tempo_xorshift else "XORShift"

            print(
                f"{bits:<8} {tempo_lcg:<15.6f} {tempo_xorshift:<15.6f} {diferenca:<12.6f} {mais_rapido:<12}"
            )

        # Calcular médias gerais
        media_lcg = statistics.mean([
            self.resultados["LCG"][bits]["tempo_medio_ms"]
            for bits in self.tamanhos_bits
        ])
        media_xorshift = statistics.mean([
            self.resultados["XORShift"][bits]["tempo_medio_ms"]
            for bits in self.tamanhos_bits
        ])

        print(f"\n{'MÉDIAS GERAIS:':<8}")
        print(f"LCG: {media_lcg:.6f} ms")
        print(f"XORShift: {media_xorshift:.6f} ms")
        print(
            f"Algoritmo mais rápido em média: {'LCG' if media_lcg < media_xorshift else 'XORShift'}"
        )

    def exportar_resultados_csv(
        self, nome_arquivo: str = "resultados_experimentos.csv"
    ):
        """Exporta os resultados para um arquivo CSV"""

        import csv

        with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)

            # Cabeçalho
            writer.writerow([
                "Algoritmo",
                "Bits",
                "Tempo_Medio_ms",
                "Tempo_Min_ms",
                "Tempo_Max_ms",
                "Desvio_Padrao_ms",
            ])

            # Dados
            for algoritmo in ["LCG", "XORShift"]:
                for bits in self.tamanhos_bits:
                    resultado = self.resultados[algoritmo][bits]
                    writer.writerow([
                        algoritmo,
                        bits,
                        f"{resultado['tempo_medio_ms']:.6f}",
                        f"{resultado['tempo_min_ms']:.6f}",
                        f"{resultado['tempo_max_ms']:.6f}",
                        f"{resultado['desvio_padrao_ms']:.6f}",
                    ])

        print(f"\nResultados exportados para: {nome_arquivo}")


def main():
    """Função principal para executar os experimentos"""

    print("Iniciando experimentos de performance com PRNGs...")
    print("Este processo pode levar alguns minutos dependendo do hardware.")
    print()

    # Criar instância do experimento
    experimento = ExperimentosPRNG()

    # Executar experimentos
    inicio_total = time.time()
    resultados = experimento.executar_experimento_completo()
    fim_total = time.time()

    # Estatísticas finais
    tempo_total = fim_total - inicio_total
    print(f"\n{'=' * 80}")
    print("EXPERIMENTOS CONCLUÍDOS")
    print(f"{'=' * 80}")
    print(f"Tempo total de execução: {tempo_total:.2f} segundos")
    print(
        f"Total de gerações testadas: {len(experimento.tamanhos_bits) * experimento.num_amostras * 2}"
    )
    print("Algoritmos testados: LCG, XORShift")

    # Exportar resultados
    experimento.exportar_resultados_csv()

    print("\nPara recuperar métricas específicas:")
    print("- Verifique o arquivo 'resultados_experimentos.csv'")
    print("- Os resultados também estão armazenados na variável 'resultados'")

    return resultados


if __name__ == "__main__":
    resultados = main()
