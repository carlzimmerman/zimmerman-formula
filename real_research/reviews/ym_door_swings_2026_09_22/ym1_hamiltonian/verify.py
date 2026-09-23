#!/usr/bin/env python3
"""D-YM1, Hamiltonian door: the explicit strong-coupling threshold X_d.

PROOF.md proves a volume-uniform spectral gap for the Kogut-Susskind
Hamiltonian of I15,

    H_I15 = (x/2) sum_l C_l + (b_N/x) sum_p (1 - T_p),

by a space-time cluster expansion (Dyson expansion + Ueltschi 2004,
Theorem 1).  The analytic proof reduces everything to a handful of scalar
inequalities in the parameters (G, a1, a2, c, lambda).  This script

  (1) checks the lattice combinatorics the proof uses (plaquettes per link,
      links shared by two plaquettes, event slots),
  (2) checks the tree-criticality constant K* = 6^6/7^7 and the monotone
      fixed-point iteration used for the branching bound,
  (3) evaluates every scalar condition of PROOF.md Sec. 5-6 in 60-digit
      arithmetic, optimises the free parameter G, and
  (4) prints the explicit thresholds X_d for d = 2, 3, 4 and several
      magnetic normalisations b_N, uniform in N where stated.

Units: energies are measured with C_F = 1 (lambda/C_F is the only input);
lambda = 2 b_N / x^2 is the normalised magnetic coupling of PROOF.md Sec. 1.
Nothing here is fitted.  The numbers are consequences of the displayed
inequalities; the inequalities themselves are proved in PROOF.md.
"""
import itertools
import json
from pathlib import Path

from mpmath import mp, mpf, exp, sqrt

mp.dps = 60
HERE = Path(__file__).resolve().parent
KSTAR = mpf(6) ** 6 / mpf(7) ** 7          # sup_G G/(1+G)^7, attained at G = 1/6
SLOTS = 8                                  # 4 links x {before, after}
LABELS = 16                                # <= 2^4 post-event P/Q choices


def lattice_combinatorics(d, L=5):
    """Plaquettes per link, links shared by two plaquettes, in a box of Z^d."""
    sites = list(itertools.product(range(L), repeat=d))
    units = [tuple(1 if k == i else 0 for k in range(d)) for i in range(d)]

    def add(a, b):
        return tuple(x + y for x, y in zip(a, b))

    inside = lambda s: all(0 <= c < L for c in s)
    links = {(s, i) for s in sites for i in range(d) if inside(add(s, units[i]))}
    plaqs = []
    for s in sites:
        for i, j in itertools.combinations(range(d), 2):
            ls = [(s, i), (add(s, units[i]), j), (add(s, units[j]), i), (s, j)]
            if all(l in links for l in ls):
                plaqs.append(frozenset(ls))
    per_link = {}
    for p in plaqs:
        for l in p:
            per_link.setdefault(l, []).append(p)
    max_per_link = max(len(v) for v in per_link.values())
    # interior link: every one of its 2(d-1) plaquettes present
    centre = tuple(L // 2 for _ in range(d))
    interior = len(per_link[(centre, 0)])
    shared_links = max(len(p & q) for p, q in itertools.combinations(plaqs, 2))
    # two distinct links lie in at most one common plaquette
    pair_count = {}
    for p in plaqs:
        for l1, l2 in itertools.combinations(sorted(p), 2):
            pair_count[(l1, l2)] = pair_count.get((l1, l2), 0) + 1
    shared_plaq = max(pair_count.values())
    return {
        "d": d, "box": L,
        "max_plaquettes_per_link": max_per_link,
        "interior_plaquettes_per_link": interior,
        "expected_2(d-1)": 2 * (d - 1),
        "max_links_shared_by_two_plaquettes": shared_links,
        "max_plaquettes_shared_by_two_links": shared_plaq,
    }


def smallest_root(kappa, tol=mpf(10) ** -50):
    """Monotone iteration G_{n+1} = kappa (1+G_n)^7 from G_0 = 0."""
    g = mpf(0)
    for _ in range(100000):
        nxt = kappa * (1 + g) ** 7
        if abs(nxt - g) < tol:
            return nxt
        g = nxt
    raise RuntimeError("no convergence: kappa above K*?")


def parameters(d, theta, G):
    """Scalar data of PROOF.md Sec. 5-6 in units C_F = 1.

    theta = b/C_F is the decay rate b of the correlation bound; the gap
    theorem gives gap(H) >= b.  Given G, the proof sets
        a1 = 4 G^2,  c = (1 - theta)/(1 + G + G^2),  a2 = c G (1+G),
    so that c = 1 - a2 - theta, and lambda from kappa = G/(1+G)^7 with
        kappa = 32 (d-1) lambda e^{a1} / c.
    """
    G = mpf(G)
    a1 = 4 * G ** 2
    c = (1 - theta) / (1 + G + G ** 2)
    a2 = c * G * (1 + G)
    lam = G * c * exp(-a1) / (32 * (d - 1) * (1 + G) ** 7)
    kappa = 2 * (d - 1) * LABELS * lam * exp(a1) / c
    R = LABELS * lam * exp(a1) * (1 + G) ** SLOTS
    A = G ** 2
    cB = 1 - theta - 3 * a2
    kappaB = 2 * (d - 1) * LABELS * lam * exp(3 * a1) / cB if cB > 0 else mpf("inf")
    return dict(G=G, a1=a1, a2=a2, c=c, lam=lam, kappa=kappa, R=R, A=A,
                cB=cB, kappaB=kappaB)


def check_parameters(d, theta, p, full=True):
    """Every scalar inequality the proof uses, evaluated.

    On [0, 1/6] the map G -> G/(1+G)^7 is increasing, so G <= 1/6 already
    makes G the smallest root; full=True re-derives it by iteration.
    """
    tol = mpf(10) ** -40
    G = p["G"]
    out = {
        "G_le_1/6": G <= mpf(1) / 6,
        "kappa_le_Kstar": p["kappa"] <= KSTAR,
        "c_identity": abs(p["c"] + p["a2"] + theta - 1) < tol,
        "c_positive": p["c"] > 0,
        # KP: a2 >= 2(d-1) R  (event contacts)  and  a1 >= 4 A (covering contacts)
        "KP_a2": p["a2"] - 2 * (d - 1) * p["R"] > -tol,
        "KP_a1": p["a1"] - 4 * p["A"] > -tol,
        # boundary sums (Sec. 7): node e^{3 a1}, edge rate cB = 1 - theta - 3 a2
        "boundary_cB_positive": p["cB"] > 0,
        "boundary_kappaB_lt_Kstar": p["kappaB"] < KSTAR,
    }
    if full:
        out["G_is_smallest_root"] = abs(smallest_root(p["kappa"]) - G) < mpf(10) ** -30
    return out


def optimise(d, theta, grid=2000):
    """Largest admissible lambda over G in (0, 1/6], all conditions strict."""
    best = None
    for k in range(1, grid + 1):
        G = mpf(k) / (6 * grid)
        p = parameters(d, theta, G)
        ok = check_parameters(d, theta, p, full=False)
        if all(ok.values()) and (best is None or p["lam"] > best["lam"]):
            best = p
    return best


def run():
    report = {"Kstar": str(KSTAR)}
    checks = []

    def check(name, predicate, **data):
        checks.append({"name": name, "passed": bool(predicate), **data})

    # (1) lattice combinatorics
    combi = [lattice_combinatorics(d, L=5 if d < 4 else 4) for d in (2, 3, 4)]
    for row in combi:
        check(f"plaquettes_per_link_d{row['d']}",
              row["max_plaquettes_per_link"] == row["expected_2(d-1)"]
              and row["interior_plaquettes_per_link"] == row["expected_2(d-1)"], **row)
        check(f"two_plaquettes_share_le_1_link_d{row['d']}",
              row["max_links_shared_by_two_plaquettes"] == 1)
        check(f"two_links_share_le_1_plaquette_d{row['d']}",
              row["max_plaquettes_shared_by_two_links"] == 1)
    report["combinatorics"] = combi

    # (2) tree criticality
    g = mpf(1) / 6
    check("Kstar_is_value_at_1/6", abs(g / (1 + g) ** 7 - KSTAR) < mpf(10) ** -50)
    derivative_left = (g / (1 + g) ** 7) - ((g - mpf(10) ** -8) / (1 + g - mpf(10) ** -8) ** 7)
    derivative_right = ((g + mpf(10) ** -8) / (1 + g + mpf(10) ** -8) ** 7) - (g / (1 + g) ** 7)
    check("Kstar_is_maximum", derivative_left > 0 and derivative_right < 0)
    root = smallest_root(KSTAR * mpf("0.999"))
    check("iteration_converges_below_Kstar", root < mpf(1) / 6, root=float(root))

    # (3)-(4) thresholds
    # normalisations: (label, b_N/C_F as a function of N or a uniform bound)
    CF = lambda n: mpf(n * n - 1) / (2 * n)
    norms = {
        "uniform_all_N_bN<=2N": mpf(16) / 3,        # sup_N 2N/C_F = 16/3 (N=2)
        "SU2_bN=2": 2 / CF(2),
        "SU3_bN=2": 2 / CF(3),
        "SU2_bN=N": 2 / CF(2),
        "SU3_bN=N": 3 / CF(3),
    }
    thetas = [mpf(1) / 4, mpf(1) / 2, mpf(3) / 4]
    table = []
    for d in (2, 3, 4):
        for theta in thetas:
            best = optimise(d, theta)
            conds = check_parameters(d, theta, best)
            check(f"all_conditions_d{d}_theta{float(theta)}", all(conds.values()),
                  **{k: bool(v) for k, v in conds.items()})
            row = {
                "d": d,
                "rate_b_over_CF": float(theta),
                "G": float(best["G"]),
                "a1": float(best["a1"]), "a2": float(best["a2"]), "c": float(best["c"]),
                "kappa": float(best["kappa"]), "kappaB": float(best["kappaB"]),
                "lambda_max_over_CF": float(best["lam"]),
                "gap_I15_lower_bound": f"(x/2)*{float(theta)}*C_F",
                "X_d": {k: float(sqrt(2 * v / best["lam"])) for k, v in norms.items()},
            }
            table.append(row)
    report["thresholds"] = table

    report["grid_optimum_reference"] = (
        "NOT CERTIFIED: best G on a 1/12000 grid sits on kappa_B ~ K*, where the "
        "Gamma_0t marked-path step needs strict inequality; quote only 'headline'")

    # CERTIFIED choice used in PROOF.md: G = 7/100, b = C_F/2.  This keeps a
    # 6% margin on the boundary condition kappa_B < K* (the grid optimum sits
    # on it).  b = C_F/2 reproduces I15's gap bound x C_F/4 >= 3x/16.
    G_cert, theta_cert = mpf(7) / 100, mpf(1) / 2
    report["headline"] = {}
    for d in (2, 3, 4):
        p = parameters(d, theta_cert, G_cert)
        conds = check_parameters(d, theta_cert, p)
        check(f"certified_G=7/100_d{d}", all(conds.values()),
              **{k: bool(v) for k, v in conds.items()})
        check(f"certified_margin_d{d}", p["kappaB"] <= mpf("0.95") * KSTAR,
              kappaB_over_Kstar=float(p["kappaB"] / KSTAR))
        report["headline"][f"X_{d}"] = {
            "G": "7/100", "b": "C_F/2",
            "lambda_star_over_CF": float(p["lam"]),
            "a1": float(p["a1"]), "a2_over_CF": float(p["a2"]), "c_over_CF": float(p["c"]),
            "kappa": float(p["kappa"]), "kappaB_over_Kstar": float(p["kappaB"] / KSTAR),
            **{k: float(sqrt(2 * v / p["lam"])) for k, v in norms.items()},
            "gap_bound": "gap(H_I15) >= x C_F/4 >= 3x/16",
        }
    report["checks"] = checks
    report["all_passed"] = all(c["passed"] for c in checks)
    return report


if __name__ == "__main__":
    rep = run()
    (HERE / "results.json").write_text(json.dumps(rep, indent=2, default=str) + "\n")
    print("K* = 6^6/7^7 =", float(KSTAR))
    for d, h in rep["headline"].items():
        print(d, {k: (float(f"{v:.5g}") if isinstance(v, float) else v) for k, v in h.items()})
    print()
    for r in rep["thresholds"]:
        print(f"d={r['d']} b/C_F={r['rate_b_over_CF']:.2f} G={r['G']:.4f} "
              f"lambda_max/C_F={r['lambda_max_over_CF']:.4e} "
              f"kappa={r['kappa']:.4f} kappaB={r['kappaB']:.4f} "
              f"X_d(uniform)={r['X_d']['uniform_all_N_bN<=2N']:.1f}")
    failed = [c["name"] for c in rep["checks"] if not c["passed"]]
    print("\nFAILED:", failed if failed else "none")
    print("ALL CHECKS PASSED" if rep["all_passed"] else "CHECKS FAILED")
