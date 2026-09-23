#!/usr/bin/env python3
"""D-YM1, Euclidean companion: explicit Dobrushin mass gap for Wilson SU(N).

Checks every ingredient of PROOF.md that can be checked numerically:
  (1) the total-variation lemma  sup TV = tanh(delta/4)  for log-densities
      of oscillation delta (closed form vs brute force);
  (2) the oscillation bound |T(UA) - T(UA')| <= 2 on SU(2), SU(3), SU(4);
  (3) periodic-lattice combinatorics in D = 2, 3, 4 (plaquettes per link,
      6(D-1) neighbours, <= 1 shared plaquette, time-slice graph distance);
  (4) thresholds beta_D and the gap bound m >= -ln alpha;
  (5) an exact cross-check in D = 2 for SU(2), where the transfer-matrix
      gap is known in closed form: m_exact(L) = L ln(I_1(beta)/I_2(beta)).
Monte Carlo lines are consistency checks of analytic facts, not proofs.
"""
import itertools
import json
from collections import deque
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special
from scipy.stats import unitary_group

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(20260922)


def haar_su(n, k):
    """k Haar-random SU(n) matrices."""
    u = unitary_group.rvs(n, size=k, random_state=rng)
    if k == 1:
        u = u[None]
    det = np.linalg.det(u)
    return u / (det ** (1.0 / n))[:, None, None]


def T(u, a):
    n = u.shape[-1]
    return np.real(np.trace(u @ a, axis1=-2, axis2=-1)) / n


def tv_two_point(delta):
    """max over q of TV between p and p e^g/Z, g in {0, delta} w.p. {1-q, q}."""
    u = np.expm1(delta)
    f = lambda q: -(q * (1 - q) * u / (1 + q * u))
    res = optimize.minimize_scalar(f, bounds=(0, 1), method="bounded",
                                   options={"xatol": 1e-12})
    return -res.fun


def tv_random(delta, trials=2000, k=6):
    """Random k-point distributions of g in [0, delta]: TV never exceeds tanh."""
    worst = 0.0
    for _ in range(trials):
        w = rng.dirichlet(np.ones(k))
        g = rng.uniform(0, delta, size=k)
        g[0], g[1] = 0.0, delta
        p2 = w * np.exp(g)
        p2 /= p2.sum()
        worst = max(worst, 0.5 * np.abs(p2 - w).sum())
    return worst


def periodic_lattice(D, L):
    sites = list(itertools.product(range(L), repeat=D))
    unit = [tuple(1 if k == i else 0 for k in range(D)) for i in range(D)]
    add = lambda a, b: tuple((x + y) % L for x, y in zip(a, b))
    links = [(s, i) for s in sites for i in range(D)]
    plaqs = []
    for s in sites:
        for i, j in itertools.combinations(range(D), 2):
            plaqs.append(frozenset([(s, i), (add(s, unit[i]), j),
                                    (add(s, unit[j]), i), (s, j)]))
    return sites, links, plaqs


def lattice_checks(D, L):
    sites, links, plaqs = periodic_lattice(D, L)
    per = {l: [] for l in links}
    for p in plaqs:
        assert len(p) == 4
        for l in p:
            per[l].append(p)
    nbr = {l: set().union(*per[l]) - {l} for l in links}
    pair = {}
    for p in plaqs:
        for a, b in itertools.combinations(sorted(p), 2):
            pair[(a, b)] = pair.get((a, b), 0) + 1
    # graph distance from a spatial link at time 0 (direction 0 = time)
    start = (tuple([0] * D), 1 if D > 1 else 0)
    dist = {start: 0}
    q = deque([start])
    while q:
        l = q.popleft()
        for m in nbr[l]:
            if m not in dist:
                dist[m] = dist[l] + 1
                q.append(m)
    ok_dist = True
    for (s, i), dd in dist.items():
        if i != 0:  # spatial link at time s[0]
            t = s[0]
            ok_dist &= dd >= min(t, L - t)
    return {
        "D": D, "L": L,
        "plaquettes_per_link": sorted({len(v) for v in per.values()}),
        "neighbours_per_link": sorted({len(v) for v in nbr.values()}),
        "expected_2(D-1)": 2 * (D - 1), "expected_6(D-1)": 6 * (D - 1),
        "max_plaquettes_shared_by_two_links": max(pair.values()),
        "time_slice_distance_ge_min(t,L-t)": bool(ok_dist),
    }


def su2_character_ratio(j2, beta):
    """c_j/(d_j c_0) for f = exp(beta cos theta) on SU(2), by quadrature.

    j2 = 2j.  Haar density on the class angle: (2/pi) sin^2 theta.
    """
    chi = lambda th: np.sin((j2 + 1) * th) / np.sin(th)
    w = lambda th: (2 / np.pi) * np.sin(th) ** 2 * np.exp(beta * np.cos(th))
    c_j = integrate.quad(lambda th: w(th) * chi(th), 0, np.pi, limit=200)[0]
    c_0 = integrate.quad(w, 0, np.pi, limit=200)[0]
    return c_j / ((j2 + 1) * c_0)


def run():
    checks = []

    def check(name, predicate, **data):
        checks.append({"name": name, "passed": bool(predicate), **data})

    # (1) TV lemma
    for delta in (0.05, 0.2, 0.5, 1.0, 2.0, 4.0):
        two = tv_two_point(delta)
        rnd = tv_random(delta)
        check(f"tv_lemma_delta{delta}",
              abs(two - np.tanh(delta / 4)) < 1e-9 and rnd <= np.tanh(delta / 4) + 1e-12,
              two_point_max=two, tanh=np.tanh(delta / 4), random_worst=rnd)

    # (2) oscillation and Haar averages
    for n in (2, 3, 4):
        u, a, a2 = haar_su(n, 20000), haar_su(n, 20000), haar_su(n, 20000)
        diff = np.abs(T(u, a) - T(u, a2))
        check(f"osc_bound_SU{n}", diff.max() <= 2 + 1e-12, max_abs_diff=float(diff.max()))

    # (3) lattice combinatorics
    lat = []
    for D, L in ((2, 3), (2, 5), (3, 3), (3, 4), (4, 3)):
        row = lattice_checks(D, L)
        lat.append(row)
        check(f"lattice_D{D}_L{L}",
              row["plaquettes_per_link"] == [2 * (D - 1)]
              and row["neighbours_per_link"] == [6 * (D - 1)]
              and row["max_plaquettes_shared_by_two_links"] == 1
              and row["time_slice_distance_ge_min(t,L-t)"], **row)

    # (4) thresholds: alpha = 6(D-1) tanh(beta), uniform in N
    thresholds = []
    for D in (2, 3, 4):
        z = 6 * (D - 1)
        row = {"D": D, "alpha(beta)": f"{z}*tanh(beta)",
               "beta_W_max_all_N": float(np.arctanh(1 / z))}
        for n in (2, 3, 4):
            row[f"SZZ_2023_beta_W_max_SU{n}"] = n * n / (16 * (D - 1))
        row["gap_bound_m(beta)"] = {
            str(b): float(-np.log(z * np.tanh(b)))
            for b in (0.001, 0.005, 0.01, 0.02, 0.04) if z * np.tanh(b) < 1
        }
        thresholds.append(row)
    check("beta_4D_value", abs(thresholds[2]["beta_W_max_all_N"] - np.arctanh(1 / 18)) < 1e-15,
          beta=thresholds[2]["beta_W_max_all_N"])

    # (5) exact D = 2 SU(2) cross-check
    exact = []
    for beta in (0.02, 0.05, 0.1, 0.15):
        ratio_q = su2_character_ratio(1, beta)
        ratio_b = special.iv(2, beta) / special.iv(1, beta)
        alpha = 6 * np.tanh(beta)
        for L in (3, 4, 8):
            m_exact = -L * np.log(ratio_b)
            exact.append({"beta": beta, "L": L, "m_exact": float(m_exact),
                          "dobrushin_bound": float(-np.log(alpha)),
                          "quadrature_vs_bessel": float(abs(ratio_q - ratio_b))})
            check(f"2D_exact_beta{beta}_L{L}",
                  abs(ratio_q - ratio_b) < 1e-10 and m_exact >= -np.log(alpha),
                  m_exact=float(m_exact), bound=float(-np.log(alpha)))

    return {"thresholds": thresholds, "lattice": lat, "exact_2D": exact,
            "checks": checks, "all_passed": all(c["passed"] for c in checks)}


if __name__ == "__main__":
    rep = run()
    (HERE / "results.json").write_text(json.dumps(rep, indent=2, default=float) + "\n")
    for t in rep["thresholds"]:
        print(t)
    print()
    failed = [c["name"] for c in rep["checks"] if not c["passed"]]
    print("FAILED:", failed if failed else "none")
    print("ALL CHECKS PASSED" if rep["all_passed"] else "CHECKS FAILED")
