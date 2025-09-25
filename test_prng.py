import math
from typing import Dict, Tuple, Type

from PRNG import PRNG
from LCG import LCG
from XORShift import XORShift


class PRNGTester:
    def __init__(self, prng_class: Type[PRNG], seed: int = 12345):
        self.prng_class = prng_class
        self.seed = seed
        self.results = {}

    def test_reproducibility(self) -> bool:
        """Verifca se mesma seed produz mesma sequência"""
        prng1 = self.prng_class(self.seed)
        prng2 = self.prng_class(self.seed)

        sequence1 = [prng1.next() for _ in range(100)]
        sequence2 = [prng2.next() for _ in range(100)]

        return sequence1 == sequence2

    def test_randbits_format(self) -> Dict[str, bool]:
        """Verifica se método produz números com quantidade correta de bits"""
        prng = self.prng_class(self.seed)
        results = {}

        for k in [1, 4, 8, 16, 32, 64]:
            valid_bits = True
            for _ in range(50):
                num = prng.randbits(k)

                # verifica se o número está no formato correto
                if k == 1:
                    valid_format = num == 1
                else:
                    # MSB deve ser igual a 1 e número caber em k bits
                    min_val = 1 << (k - 1)  # 2^(k-1)
                    max_val = (1 << k) - 1  # 2^k - 1
                    valid_format = min_val <= num <= max_val

                if not valid_format:
                    valid_bits = False
                    break

            results[f"{k}_bits"] = valid_bits

        return results

    def test_uniformity_chi_square(
        self, sample_size: int = 10000, bins: int = 100
    ) -> Tuple[bool, float]:
        """Testes de Chi-quadrado"""
        prng = self.prng_class(self.seed)

        # gera amostras normalizadas [0, 1)
        samples = []
        for _ in range(sample_size):
            raw = prng.next()
            normalized = raw / (2**32)  # assume 32 bits na saída
            samples.append(normalized)

        bin_counts = [0] * bins
        for sample in samples:
            bin_idx = min(int(sample * bins), bins - 1)
            bin_counts[bin_idx] += 1

        expected = sample_size / bins

        chi_square = sum(
            (observed - expected) ** 2 / expected for observed in bin_counts
        )

        df = bins - 1

        critical_value = 124.342

        is_uniform = chi_square <= critical_value

        return is_uniform, chi_square

    def test_bit_distribution(self, sample_size: int = 10000) -> Dict[int, float]:
        """Testa distribuição de bits individuais"""
        prng = self.prng_class(self.seed)
        bit_counts = [0] * 32  # Assume 32-bit output

        for _ in range(sample_size):
            num = prng.next()
            for bit_pos in range(32):
                if (num >> bit_pos) & 1:
                    bit_counts[bit_pos] += 1

        # calcula proporção de 1s para cada bit
        bit_proportions = {
            pos: count / sample_size for pos, count in enumerate(bit_counts)
        }

        return bit_proportions

    def test_runs(self, sample_size: int = 1000) -> Tuple[bool, int]:
        prng = self.prng_class(self.seed)
        samples = [prng.next() for _ in range(sample_size)]

        # calcula mediana
        sorted_samples = sorted(samples)
        median = sorted_samples[len(sorted_samples) // 2]

        # Converte para sequência binária
        binary_seq = [1 if x >= median else 0 for x in samples]

        runs = 1
        for i in range(1, len(binary_seq)):
            if binary_seq[i] != binary_seq[i - 1]:
                runs += 1

        n1 = sum(binary_seq)  # 1s
        n0 = sample_size - n1  # 0s

        if n1 == 0 or n0 == 0:
            return False, runs

        expected_runs = (2 * n1 * n0) / sample_size + 1
        variance = (2 * n1 * n0 * (2 * n1 * n0 - sample_size)) / (
            sample_size**2 * (sample_size - 1)
        )

        if variance > 0:
            z_score = abs(runs - expected_runs) / math.sqrt(variance)
            is_random = z_score <= 1.96  # confiança 95%
        else:
            is_random = False

        return is_random, runs

    def test_serial_correlation(
        self, sample_size: int = 1000, lag: int = 1
    ) -> Tuple[bool, float]:
        """Testa correlação serial"""
        prng = self.prng_class(self.seed)
        samples = [prng.next() / (2**32) for _ in range(sample_size)]

        if len(samples) <= lag:
            return False, 0.0

        x = samples[:-lag]
        y = samples[lag:]

        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi * xi for xi in x)
        sum_y2 = sum(yi * yi for yi in y)

        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))

        if denominator == 0:
            return False, 0.0

        correlation = numerator / denominator

        # Testa se correlação é significativametne diferente de 0
        std_error = 1 / math.sqrt(n)
        z_score = abs(correlation) / std_error

        is_uncorrelated = z_score <= 1.96  # 95% confidence

        return is_uncorrelated, correlation

    def test_period_detection(self, max_iterations: int = 100000) -> Tuple[bool, int]:
        """Detecta período do PRNG"""
        prng = self.prng_class(self.seed)
        seen_states = {}

        for i in range(max_iterations):
            if hasattr(prng, "state"):
                state = prng.state
            elif (
                hasattr(prng, "w")
                and hasattr(prng, "x")
                and hasattr(prng, "y")
                and hasattr(prng, "z")
            ):
                state = (prng.x, prng.y, prng.z, prng.w)
            else:
                return False, -1

            if state in seen_states:
                period = i - seen_states[state]
                return True, period

            seen_states[state] = i
            prng.next()

        return False, -1

    def run_all_tests(self) -> Dict[str, any]:
        print(f"Executando testes de PRNG para {self.prng_class.__name__}...")

        results = {}

        print("Testando reprodutibilidade...")
        results["reproducible"] = self.test_reproducibility()

        print("Testando formato randbits...")
        results["randbits_format"] = self.test_randbits_format()

        print("Testando uniformidade (chi-quadrado)...")
        uniform_result, chi_square = self.test_uniformity_chi_square()
        results["uniform"] = uniform_result
        results["chi_square_statistic"] = chi_square

        print("Testando distribuição de bits...")
        bit_dist = self.test_bit_distribution()

        bit_balance = all(0.45 <= prop <= 0.55 for prop in bit_dist.values())
        results["bit_balanced"] = bit_balance
        results["bit_proportions"] = bit_dist

        print("Testando runs...")
        runs_random, num_runs = self.test_runs()
        results["runs_random"] = runs_random
        results["num_runs"] = num_runs

        print("Testando correlação serial...")
        uncorrelated, correlation = self.test_serial_correlation()
        results["uncorrelated"] = uncorrelated
        results["serial_correlation"] = correlation

        print("Testando detecção de período...")
        period_found, period = self.test_period_detection()
        results["period_found"] = period_found
        results["period"] = period

        return results

    def print_report(self, results: Dict[str, any]) -> None:
        """Print a formatted test report."""
        print(f"\n{'=' * 60}")
        print(f"RELATÓRIO DE TESTE PRNG: {self.prng_class.__name__}")
        print(f"{'=' * 60}")
        print(f"Seed utilizada: {self.seed}")
        print()

        print("TESTES BÁSICOS:")
        print(f"  Reprodutível: {'✓' if results['reproducible'] else '✗'}")
        print(f"  Bits equilibrados: {'✓' if results['bit_balanced'] else '✗'}")
        print()

        print("TESTES DE FORMATO RANDBITS:")
        for test_name, passed in results["randbits_format"].items():
            print(f"  {test_name}: {'✓' if passed else '✗'}")
        print()

        print("TESTES ESTATÍSTICOS:")
        print(f"  Distribuição uniforme: {'✓' if results['uniform'] else '✗'}")
        print(f"    Estatística chi-quadrado: {results['chi_square_statistic']:.3f}")
        print(f"  Runs aleatórios: {'✓' if results['runs_random'] else '✗'}")
        print(f"    Número de runs: {results['num_runs']}")
        print(f"  Sem correlação serial: {'✓' if results['uncorrelated'] else '✗'}")
        print(f"    Coeficiente de correlação: {results['serial_correlation']:.6f}")
        print()

        print("TESTE DE PERÍODO:")
        if results["period_found"]:
            print(f"  Período detectado: {results['period']}")
        else:
            print("  Período não encontrado nas primeiras 100.000 iterações")
        print()

        basic_tests = [results["reproducible"], results["bit_balanced"]]
        randbits_tests = list(results["randbits_format"].values())
        statistical_tests = [
            results["uniform"],
            results["runs_random"],
            results["uncorrelated"],
        ]

        all_tests = basic_tests + randbits_tests + statistical_tests
        passed_tests = sum(all_tests)
        total_tests = len(all_tests)

        print("AVALIAÇÃO GERAL:")
        print(f"  Testes aprovados: {passed_tests}/{total_tests}")
        print(f"  Taxa de sucesso: {(passed_tests / total_tests) * 100:.1f}%")

        if passed_tests == total_tests:
            print("  Status: ✓ EXCELENTE - Todos os testes aprovados")
        elif passed_tests >= total_tests * 0.8:
            print("  Status: ⚠ BOM - A maioria dos testes aprovados")
        elif passed_tests >= total_tests * 0.6:
            print("  Status: ⚠ REGULAR - Alguns problemas detectados")
        else:
            print("  Status: ✗ RUIM - Múltiplas falhas")


def main():
    test_seed = 12345

    print("Testando Gerador Linear Congruencial (LCG)...")
    lcg_tester = PRNGTester(LCG, test_seed)
    lcg_results = lcg_tester.run_all_tests()
    lcg_tester.print_report(lcg_results)

    print("\n" + "=" * 80 + "\n")

    print("Testando Gerador XORShift...")
    xorshift_tester = PRNGTester(XORShift, test_seed)
    xorshift_results = xorshift_tester.run_all_tests()
    xorshift_tester.print_report(xorshift_results)


if __name__ == "__main__":
    main()
