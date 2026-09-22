"""Exact finite checks of the RG budget identities and explicit obstructions.

These are not Yang--Mills simulations. Universal arguments are in REPORT.md.
Python standard library only; all asserted comparisons use Fraction.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def main():
    checks = []
    # Compare recursive and expanded physical budgets with nonconstant losses.
    # This checks the indexing of P_j and a_j independently of the derivation.
    for L in (2, 3, 5):
        for K in range(1, 21):
            spacing = [F(L) ** (j - K) for j in range(K + 1)]
            eps = [F(1, 10 * (K - j + 1) ** 2) for j in range(K)]
            delta = [F(1, 100 * (K - j + 1) ** 3) for j in range(K)]
            gap = F(2)
            for j in reversed(range(K)):
                gap = (1 - eps[j]) * gap / L - delta[j]
            product, err = F(1), F(0)
            for j in range(K):
                err += product * delta[j] / spacing[j]
                product *= 1 - eps[j]
            assert gap / spacing[0] == 2 * product - err
    checks.append({"check": "telescoping_identity", "cases": 60, "passed": True})

    # Direct finite sum vs finite geometric closed forms; no float tolerance.
    records = []
    for L in (2, 3, 5):
        r = F(1, L)
        s, q = F(3, 2), F(2, 3)
        upper = s / (L - 1) + q * L / F((L - 1) ** 2)
        for K in (1, 2, 5, 10, 20, 40):
            direct = sum((s + q * n) * r ** n for n in range(1, K + 1))
            geometric = r * (1 - r ** K) / (1 - r)
            weighted = r * (1 - (K + 1) * r ** K + K * r ** (K + 1)) / (1 - r) ** 2
            assert direct == s * geometric + q * weighted
            assert 0 < direct < upper
            records.append({"L": L, "K": K, "sum": str(direct), "upper": str(upper)})
    checks.append({"check": "inverse_gap_budget", "cases": len(records), "passed": True})

    # Positive gaps obeying every transport inequality but collapsing physically.
    collapse = []
    for K in range(6, 81):
        spacing0 = F(1, 2 ** K)
        gap0 = F(1, 2 ** (2 * K))
        delta0 = F(1, (K + 1) ** 2)
        assert gap0 >= F(1, 2 ** K) - delta0
        assert gap0 / spacing0 == F(1, 2 ** K)
        if K in (6, 10, 20, 40, 80):
            collapse.append({"K": K, "terminal_mass": "1", "fine_mass": str(gap0 / spacing0)})
    checks.append({"check": "polynomial_error_collapse", "cases": 75, "passed": True})

    # Nonzero eigenvalues of H_t have p(z)=z^2-(t^2+2)z+1.
    # The metric-correct harmonic lower bound b=1/(t^2+2) has p(b)>0
    # and lies left of the vertex, hence at/below the smaller root.
    for t in (0, 1, 2, 3, 10, 100):
        trace = F(t * t + 2)
        bound = 1 / trace
        assert bound <= trace / 2
        assert bound * bound - trace * bound + 1 > 0
        if t >= 2:
            # p(1/2)<0 means 1/2 lies strictly between the eigenvalues.
            assert F(1, 4) - trace / 2 + 1 < 0
    checks.append({"check": "induced_metric_counterexample", "cases": 6, "passed": True})
    result = {
        "interpretation": "Exact finite assertions checked; universal proofs in REPORT.md; no Yang--Mills RG estimate established.",
        "checks": checks,
        "inverse_gap_records": records,
        "collapse_records": collapse,
    }
    output = Path(__file__).parent / "run" / "results.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks": checks, "result": result["interpretation"]}, indent=2))


if __name__ == "__main__":
    main()
