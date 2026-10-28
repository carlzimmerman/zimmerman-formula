#!/usr/bin/env python3
"""Exact finite arithmetic accompanying the Yang--Mills bounds manuscript.

Python standard library only. Run this file to replace only RESULTS.json next
to it. No numerical optimization, matrix eigensolver, or analytic theorem is
invoked. All predicates use integers, fractions, or exact polynomials.
"""

from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from math import comb, factorial, isqrt
from pathlib import Path
import platform
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
SOURCES = (
    "real_research/ym1_bdl_extension_2026/constants.py",
    "real_research/ym1_bdl_extension_2026/DERIVATION.md",
    "fable_independent_2026/lean_2026/I19_ym1_bdl_threshold.lean",
    "fable_independent_2026/lean_2026/I21_ym1_combinatorics.lean",
    "real_research/reviews/yang_mills_continuum_2026_09_22/blocking/SCHUR_GAP.md",
    "real_research/reviews/yang_mills_continuum_2026_09_22/layer/PROOF.md",
    "real_research/reviews/yang_mills_continuum_2026_09_22/one_shot/PROOF.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact(value):
    """Serialize rational evidence without a floating-point conversion."""
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): exact(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [exact(v) for v in value]
    return value


CHECKS = []


def check(name, condition, evidence):
    CHECKS.append({"name": name, "passed": bool(condition), "evidence": exact(evidence)})


def sqrt_up(value, digits=15):
    """Smallest multiple of 10**(-digits) whose square is >= value."""
    scale = 10**digits
    ceiling = (value.numerator * scale**2 + value.denominator - 1) // value.denominator
    root = isqrt(ceiling)
    return F(root + (root * root < ceiling), scale)


def matrix_product(a, b):
    if len(a[0]) != len(b):
        raise ValueError("Incompatible matrix dimensions")
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def matrix_difference(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def threshold_checks():
    s = 4
    g0sq = sum(F(comb(s - 1, t - 1), t*t) for t in range(1, s + 1))
    gSsq = (s + 1)**2 * sum(F(comb(s, t), (t + 1)**2) for t in range(s + 1))
    check("s4_sector_sums", (g0sq, gSsq) == (F(103, 48), F(887, 12)),
          {"gamma0_squared": g0sq, "gammaS_squared": gSsq})
    g0, gS = sqrt_up(g0sq), sqrt_up(gSsq)
    grid = F(1, 10**15)
    expected = (F(1464866319270579, 10**15), F(1074685031377411, 125000000000000))
    check("s4_upward_sqrt_bounds", (g0, gS) == expected
          and (g0-grid)**2 < g0sq <= g0**2 and (gS-grid)**2 < gSsq <= gS**2,
          {"gamma0_upper": g0, "gammaS_upper": gS, "grid": grid})
    beta = [g0] + [2**k * (g0*s**k + k*gS*s**(k-1)) for k in range(1, 2*s+1)]
    lam = F(1190829, 100000000)  # exactly 0.01190829, rounded down
    mu = F(7714031583367, 257393552939521)  # fixed I19 witness, no optimization
    q = sum(beta[k] * mu**k / factorial(k) for k in range(2*s+1))
    qp = sum(beta[k] * mu**(k-1) / factorial(k-1) for k in range(1, 2*s+1))
    # Independent Horner evaluation checks the polynomial and its derivative.
    q_horner = beta[-1] / factorial(2*s)
    for k in reversed(range(2*s)):
        q_horner = q_horner * mu + beta[k] / factorial(k)
    qp_horner = beta[-1] / factorial(2*s-1)
    for k in reversed(range(1, 2*s)):
        qp_horner = qp_horner * mu + beta[k] / factorial(k-1)
    check("s4_polynomial_evaluation", q == q_horner and qp == qp_horner,
          {"degree": 8, "beta_upper": beta, "method": "power sums and independent Horner evaluation"})
    check("s4_rational_certificate", lam > 0 and mu > 0 and all(v > 0 for v in beta)
          and mu-lam*q >= 0 and 2*lam*qp < 1,
          {"lambda": lam, "mu": mu, "majorant_slack": mu-lam*q,
           "derivative_slack": 1-2*lam*qp, "derivative_bound": 2*lam*qp})
    x, incidence = F(599, 10), 4
    coupling = F(32, 3) * incidence / x**2
    check("d3_safe_threshold", coupling <= lam,
          {"x": x, "D": incidence, "lambda_upper_at_x": coupling,
           "certificate_lambda": lam, "slack": lam-coupling})
    # Coefficients in z=N^2 after clearing the positive denominator 3(z-1):
    # 32(z-1)-24z = 8(z-4). Positivity for N>=2 is a prose argument.
    lhs, rhs = (-32, 32-24), (-8*4, 8)
    check("uniform_N_rational_identity", lhs == rhs and F(8*4, 4-1) == F(32, 3),
          {"identity": "32/3 - 8*N^2/(N^2-1) = 8*(N^2-4)/(3*(N^2-1))",
           "cleared_coefficients_constant_then_z": lhs, "equality_at_N": 2})


def bdl_checks():
    totals = [k*4*3*2**k*2**(k-1) + 4*2**k*2**k for k in range(1, 5)]
    independent = [3*k*2**(2*k+1) + 2**(2*k+2) for k in range(1, 5)]
    check("bdl_corrected_constant", totals == independent and max(totals) == 7168 <= 8192,
          {"k": [1, 2, 3, 4], "totals": totals, "maximum": max(totals), "bound": 2**13})
    # Columns are input kets, rows are output kets; index=4u+2v+w.
    create = [[int(i == 7 and j == 0) for j in range(8)] for i in range(8)]
    flip = [[int(i == (j ^ 3)) for j in range(8)] for i in range(8)]
    lower = [[int(i < 4 and j == i+4) for j in range(8)] for i in range(8)]
    comm = matrix_difference(matrix_product(create, flip), matrix_product(flip, create))
    result = matrix_product(lower, comm)
    nonzero = [(i, j, result[i][j]) for i in range(8) for j in range(8) if result[i][j]]
    eye = [[int(i == j) for j in range(8)] for i in range(8)]
    m, p, mj = {0}, {1, 2}, {0, 1, 2}
    check("bdl_three_qubit_counterexample", result[0][0] == -1
          and nonzero == [(0, 0, -1), (3, 3, 1)] and matrix_product(flip, flip) == eye
          and mj <= m | p and len(mj) > 2*len(m) and len(mj) == 3*len(m),
          {"basis": "index=4*u+2*v+w; rows output, columns input",
           "creation": create, "flip_vw": flip, "lower_u": lower,
           "commutator": comm, "nonzero_entries_after_lowering": nonzero,
           "vacuum_matrix_element": result[0][0], "M": sorted(m), "p": sorted(p), "Mj": sorted(mj)})


def schur_checks():
    h = [[0, 0, 0], [0, 2, 1], [0, 1, 1]]
    factor = [[0, 1, 0], [0, 1, 1]]
    # Gram factor proves nonnegativity; its kernel is span(e_1).
    v = [[0], [1], [-2]]
    numerator = matrix_product(transpose(v), matrix_product(h, v))[0][0]
    denominator = matrix_product(transpose(v), v)[0][0]
    quotient = F(numerator, denominator)
    s, g, d = F(1), F(2), F(1)
    gamma = s/g
    corrected = gamma*d/(gamma+d)
    check("schur_metric_counterexample", matrix_product(transpose(factor), factor) == h
          and quotient == F(2, 5) < F(1, 2) and corrected == F(1, 3),
          {"H_M1": h, "gram_factor": factor, "trial_vector": v,
           "trial_energy": numerator, "trial_norm_squared": denominator,
           "rayleigh_quotient": quotient, "unweighted_S_gap": s,
           "metric_G_excited_entry": g, "correct_gamma": gamma,
           "false_unweighted_harmonic_bound": F(1, 2), "corrected_bound": corrected})
    s1, g1 = F(2)-F(1, 2), F(1)+F(1, 4)
    k1 = s1/g1
    # In Q(sqrt(2)), write C=(c0*sqrt(2),c1). D*C=B is exactly
    # 4*c0+c1=1 and 2*c0+4*c1=0; no radical approximation is used.
    c0, c1 = F(2, 7), F(-1, 7)
    s2, g2 = F(4)-2*c0, F(1)+2*c0*c0+c1*c1
    k2 = s2/g2
    check("schur_oscillator_sectors", 4*c0+c1 == 1 and 2*c0+4*c1 == 0
          and (s1, g1, k1) == (F(3, 2), F(5, 4), F(6, 5))
          and (s2, g2, k2) == (F(24, 7), F(58, 49), F(84, 29))
          and k1 < k2 < 3 and k2 != 2*k1,
          {"C2_coefficients": [c0, c1], "S1": s1, "G1": g1, "K1": k1,
           "S2": s2, "G2": g2, "K2": k2, "K2_minus_2K1": k2-2*k1,
           "scope": "Only n=1,2 sectors; exclusion of n>=3 requires the analytic bound H_n>=nI."})


# Sparse exact Laurent polynomials: exponent tuples -> rational coefficients.
def p_add(*polys):
    answer = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            answer[monomial] = answer.get(monomial, F(0)) + coefficient
    return {m: c for m, c in answer.items() if c}


def p_scale(poly, scalar):
    return {m: c*scalar for m, c in poly.items() if c*scalar}


def p_mul(a, b):
    answer = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x+y for x, y in zip(ma, mb))
            answer[m] = answer.get(m, F(0)) + ca*cb
    return {m: c for m, c in answer.items() if c}


def exponent_checks():
    # Variables (m,D,b,p,x); t=s_*^2, A/s+B*s is the exponent.
    a = {(1, 2, 0, 0, 0): F(3, 2)}
    b = {(0, 0, 1, 1, -2): F(8)}
    t = {(1, 2, -1, -1, 2): F(3, 16)}
    cb_over_x_squared = {(1, 2, 1, 1, -2): F(48)}
    bt = p_mul(b, t)
    # General square identity in independent variables (A,B,t).
    av, bv, tv = {(1, 0, 0): F(1)}, {(0, 1, 0): F(1)}, {(0, 0, 1): F(1)}
    btv = p_mul(bv, tv)
    plus, minus = p_add(av, btv), p_add(av, p_scale(btv, -1))
    lhs = p_add(p_mul(plus, plus), p_scale(p_mul(av, btv), -4))
    rhs = p_mul(minus, minus)
    check("finite_block_exponent_algebra", bt == a
          and p_scale(p_mul(a, b), 4) == cb_over_x_squared and lhs == rhs,
          {"A": "3*m*D^2/2", "B": "8*b*p/x^2",
           "s_star_squared": "3*m*x^2*D^2/(16*b*p)",
           "minimum_exponent_squared": "48*m*D^2*b*p/x^2",
           "identity": "(A+B*t)^2-4*A*B*t=(A-B*t)^2",
           "scope": "Formal Laurent-polynomial identities; positivity, heat estimates and minimization interpretation remain prose."})


def printed_table_checks():
    """Check the exact witnesses printed in the final manuscript, separately."""
    for s, lam, g0, g1, r in [
        (3, F("0.01790402"), F("1.269295517644"), F("5.859465277083"), F("0.03911425")),
        (4, F("0.01190829"), F("1.464866319271"), F("8.597480251020"), F("0.02996979")),
    ]:
        g0sq = sum(F(comb(s-1, t-1), t*t) for t in range(1, s+1))
        g1sq = (s+1)**2 * sum(F(comb(s, t), (t+1)**2) for t in range(s+1))
        beta = [g0] + [2**k * (g0*s**k + k*g1*s**(k-1)) for k in range(1, 2*s+1)]
        q = sum(beta[k]*r**k/factorial(k) for k in range(2*s+1))
        qp = sum(beta[k]*r**(k-1)/factorial(k-1) for k in range(1, 2*s+1))
        check(f"printed_s{s}_rational_witness",
              g0*g0 >= g0sq and g1*g1 >= g1sq
              and r-lam*q > F(3, 10**8) and 1-2*lam*qp > F(9, 10**7),
              {"lambda": lam, "r": r, "gamma0_upper": g0, "gamma1_upper": g1,
               "supersolution_slack": r-lam*q, "gap_slack": 1-2*lam*qp})
    for d, x in [(2, F("42.4")), (3, F("59.9")), (4, F("73.4"))]:
        coupling = F(32, 3)*2*(d-1)/x**2
        check(f"printed_d{d}_safe_link_threshold", coupling <= F("0.01190829"),
              {"x": x, "worst_case_lambda": coupling})
    coupling = F(32, 3)*3/F("42.3")**2
    check("printed_d2_safe_vertex_threshold", coupling <= F("0.01790402"),
          {"x": F("42.3"), "worst_case_lambda": coupling})


def git_metadata(root):
    if root is None:
        return {"commit": None, "dirty": None, "observation": "No original repository found; standalone execution."}
    try:
        def git(*args):
            return subprocess.run(["git", "-C", str(root), *args], check=True,
                                  capture_output=True, text=True, timeout=15).stdout.strip()
        commit = git("rev-parse", "HEAD")
        status = git("status", "--porcelain", "--untracked-files=normal")
        return {"commit": commit, "dirty": bool(status),
                "dirty_entries_count": len(status.splitlines()),
                "observation": "Whole-repository status, including untracked files; unrelated edits may be present."}
    except (OSError, subprocess.SubprocessError) as error:
        return {"commit": None, "dirty": None, "observation": str(error)}


def main():
    started_at = datetime.now(timezone.utc).isoformat()
    started = time.perf_counter()
    root = next((p for p in HERE.parents if (p / SOURCES[0]).is_file()), None)
    paths = [Path(__file__).resolve()]
    source_records = []
    for source in SOURCES:
        path = root / source if root else None
        record = {"path": source, "role": "documentary provenance; not imported or executed",
                  "available": bool(path and path.is_file())}
        if record["available"]:
            record["sha256_before"] = digest(path)
            paths.append(path)
        source_records.append(record)
    before = {str(path): digest(path) for path in paths}
    repo = git_metadata(root)
    threshold_checks()
    bdl_checks()
    schur_checks()
    exponent_checks()
    printed_table_checks()
    unchanged = all(digest(path) == before[str(path)] for path in paths)
    for record in source_records:
        if record["available"]:
            record["sha256_after"] = digest(root / record["path"])
    check("inputs_unchanged_during_run", unchanged,
          {"scope": "script and every available documentary source; missing sources are optional"})
    passed = all(item["passed"] for item in CHECKS)
    results = {"passed": passed, "check_count": len(CHECKS), "checks": CHECKS}
    canonical = json.dumps(results, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report = {
        "schema": "yang-mills-bounds-exact-verification-v1",
        "assertion_tested": "Exact finite arithmetic and formal polynomial identities listed in results.checks.",
        "non_claims": [
            "No proof of analytic BDL extension, infinite-dimensional limits, heat-kernel estimates, or operator-domain lemmas.",
            "No continuum Yang--Mills construction, mass-gap proof, or novelty certification.",
            "No Lean compiler run; references identify existing independent certificates only.",
            "No exhaustive parameter scan, numerical optimization, or floating-point predicate.",
        ],
        "coefficient_domain": "Integers, fractions, and sparse Laurent polynomials over Q.",
        "command": [sys.executable, str(Path(__file__).resolve())],
        "environment": {"software": [{"name": "Python", "version": platform.python_version()}],
                        "platform": platform.platform(), "hardware": platform.machine(),
                        "third_party_dependencies": []},
        "repository": repo,
        "randomness": {"used": False, "seed": None},
        "run": {"started_at": started_at, "runtime_seconds": time.perf_counter()-started,
                "status": "completed" if passed else "failed", "exit_status": 0 if passed else 1},
        "input_artifacts": [{"path": "verify_release.py", "sha256_before": before[str(paths[0])],
                             "sha256_after": digest(paths[0])}],
        "documentary_sources": source_records,
        "results": results,
        "results_payload_sha256": hashlib.sha256(canonical).hexdigest(),
        "hash_convention": "SHA-256 of UTF-8 json.dumps(results, sort_keys=True, separators=(',', ':')). This is a payload hash, not a hash of the containing file.",
        "manifest_limit": "This self-contained report is not a separate validated mathbox v2 run manifest; an enclosing release manifest can hash RESULTS.json without self-reference.",
    }
    (HERE / "RESULTS.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{'PASS' if passed else 'FAIL'}: {len(CHECKS)} exact checks; {HERE / 'RESULTS.json'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
