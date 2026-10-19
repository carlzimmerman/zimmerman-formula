"""Exact finite-state audit of unconditioned Weyl/contact formulas.

The formal jet implementation supplies independent derivatives of -log Z.
The cumulant implementation uses set partitions. No QCD data are generated.
"""
import argparse
import itertools
import json
import math
from fractions import Fraction as Q
from pathlib import Path

MAX_T, MAX_U = 3, 1
ONE = {(0, 0): Q(1)}


def add(a, b):
    c = a.copy()
    for k, v in b.items():
        c[k] = c.get(k, Q(0)) + v
    return {k: v for k, v in c.items() if v}


def scale(a, n):
    return {k: v * n for k, v in a.items() if v * n}


def mul(a, b):
    c = {}
    for (ta, ua), va in a.items():
        for (tb, ub), vb in b.items():
            k = ta + tb, ua + ub
            if k[0] <= MAX_T and k[1] <= MAX_U:
                c[k] = c.get(k, Q(0)) + va * vb
    return {k: v for k, v in c.items() if v}


def exp_zero(a):
    assert not a.get((0, 0), 0)
    out, power = ONE.copy(), ONE.copy()
    for n in range(1, MAX_T + MAX_U + 1):
        power = mul(power, a)
        out = add(out, scale(power, Q(1, math.factorial(n))))
    return out


def log_one(a):
    assert a.get((0, 0)) == 1
    h = add(a, scale(ONE, -1))
    out, power = {}, ONE.copy()
    for n in range(1, MAX_T + MAX_U + 1):
        power = mul(power, h)
        out = add(out, scale(power, Q((-1) ** (n + 1), n)))
    return out


def deriv(jet, t, u=0):
    return jet.get((t, u), Q(0)) * math.factorial(t) * math.factorial(u)


def wjet(weights, actions):
    z = {}
    for w, s in zip(weights, actions):
        z = add(z, scale(exp_zero(scale(s, -1)), w))
    z = scale(z, 1 / sum(weights))
    return scale(log_one(z), -1)


def parts(items):
    if not items:
        yield []
        return
    first = items[0]
    for tail in parts(items[1:]):
        yield [(first,)] + tail
        for j in range(len(tail)):
            yield tail[:j] + [(first,) + tail[j]] + tail[j + 1:]


def mean(weights, values):
    return sum(w * v for w, v in zip(weights, values)) / sum(weights)


def cumul(weights, *vectors):
    total = Q(0)
    for partition in parts(tuple(range(len(vectors)))):
        term = Q((-1) ** (len(partition) - 1) * math.factorial(len(partition) - 1))
        for block in partition:
            prod = [math.prod(vectors[j][i] for j in block) for i in range(len(weights))]
            term *= mean(weights, prod)
        total += term
    return total


def lin(*pairs):
    return [sum(c * a[i] for c, a in pairs) for i in range(len(pairs[0][1]))]


def main(result):
    checks = []
    fixtures = []

    def check(label, lhs, rhs=Q(0)):
        if lhs != rhs:
            raise AssertionError((label, str(lhs), str(rhs)))
        checks.append(label)

    # A scalar Z=exp(-s) verifies the nontrivial formal log/exp operations.
    scalar = {(1, 0): Q(2, 3), (2, 0): Q(-3, 7), (3, 1): Q(5, 11)}
    check("jet_log_exp_inverse", wjet([Q(1)], [scalar]), scalar)
    check("partition_count_n4", len(list(parts(tuple(range(4))))), 15)

    for f in range(16):
        weights = [Q((i + 2) * (f + 1) % 11 + 1, i + 1) for i in range(5)]
        actions = []
        for i in range(5):
            s = {}
            for a, b in itertools.product(range(4), range(2)):
                if (a, b) != (0, 0):
                    s[a, b] = Q((i + 1) ** (1 + b) * (f + 2) + (-1) ** i * (a + 1),
                                  (a + b + 2) * (i + 2) * math.factorial(a))
            actions.append(s)
        w = wjet(weights, actions)
        x = [deriv(s, 1) for s in actions]
        y = [deriv(s, 2) for s in actions]
        z = [deriv(s, 3) for s in actions]
        j = [deriv(s, 0, 1) for s in actions]
        xu = [deriv(s, 1, 1) for s in actions]
        yu = [deriv(s, 2, 1) for s in actions]
        zu = [deriv(s, 3, 1) for s in actions]
        avg = lambda v: mean(weights, v)
        cov = lambda a, b: cumul(weights, a, b)
        kap = lambda *a: cumul(weights, *a)
        bvec = lin((1, y), (-4, x))
        cvec = lin((1, yu), (-4, xu))
        hvec = lin((1, z), (-6, y), (8, x))
        huvec = lin((1, zu), (-6, yu), (8, xu))
        e = avg(bvec) - cov(x, x)
        eu = avg(cvec) - cov(bvec, j) - 2 * cov(x, xu) + kap(x, x, j)
        fvec = [bb - (xx - avg(x)) ** 2 for bb, xx in zip(bvec, x)]
        reduced = avg(cvec) - 2 * cov(x, xu) - cov(fvec, j)
        k = avg(hvec) - 3 * cov(x, y) + 6 * cov(x, x) + kap(x, x, x)
        ku = (avg(huvec) - cov(hvec, j) - 3 * cov(xu, y) - 3 * cov(x, yu)
              + 3 * kap(x, y, j) + 12 * cov(x, xu) - 6 * kap(x, x, j)
              + 3 * kap(xu, x, x) - kap(x, x, x, j))
        prefix = "fixture_%02d_" % f
        check(prefix + "W_t", deriv(w, 1), avg(x))
        check(prefix + "W_tt", deriv(w, 2), avg(y) - cov(x, x))
        check(prefix + "E", e, deriv(w, 2) - 4 * deriv(w, 1))
        check(prefix + "E_u", eu, deriv(w, 2, 1) - 4 * deriv(w, 1, 1))
        check(prefix + "E_u_reduced", eu, reduced)
        check(prefix + "F_mean", avg(fvec), e)
        check(prefix + "K", k, deriv(w, 3) - 6 * deriv(w, 2) + 8 * deriv(w, 1))
        check(prefix + "K_u", ku, deriv(w, 3, 1) - 6 * deriv(w, 2, 1) + 8 * deriv(w, 1, 1))
        for label, a, b in [("X_Xu", x, xu), ("F_J", fvec, j)]:
            assert cov(a, b) ** 2 <= cov(a, a) * cov(b, b)
            checks.append(prefix + "Cauchy_Schwarz_" + label)
        square_bound = 3 * (avg(cvec) ** 2 + 4 * cov(x, x) * cov(xu, xu)
                            + cov(fvec, fvec) * cov(j, j))
        assert eu ** 2 <= square_bound
        checks.append(prefix + "rational_squared_charge_bound")
        fixtures.append({"fixture": f, "states": 5, "E": str(e), "E_u": str(eu),
                         "K": str(k), "K_u": str(ku), "E_u_squared_bound": str(square_bound)})

    # Common c-number metric factors are invisible to variances but not E.
    for p in (-2, 0, 2, 3, 4, 6):
        for c in (Q(2, 5), Q(-3, 7)):
            s = {(a, b): c * Q(p ** a, math.factorial(a)) * (1 if b == 0 else Q(5, 3))
                 for a, b in itertools.product(range(4), range(2)) if (a, b) != (0, 0)}
            w = wjet([Q(1), Q(2)], [s, s])
            check("common_p%d_c%s_E" % (p, c), deriv(w, 2) - 4 * deriv(w, 1), c * p * (p - 4))
            check("common_p%d_c%s_Eu" % (p, c), deriv(w, 2, 1) - 4 * deriv(w, 1, 1),
                  Q(5, 3) * c * p * (p - 4))
            check("common_p%d_c%s_K" % (p, c), deriv(w, 3) - 6 * deriv(w, 2) + 8 * deriv(w, 1),
                  c * p * (p - 2) * (p - 4))
    # b=(4Omega/3)A and p=3 imply normalized extraction 1, independent of Omega.
    check("sphere_E_area_normalization", -Q(1, 4) * Q(4, 3) * 3 * (3 - 4), 1)
    check("sphere_K_area_normalization", -Q(1, 4) * Q(4, 3) * 3 * (3 - 2) * (3 - 4), 1)

    # Actual source-action derivative structure, finite reflection-paired fixture.
    coords = (-2, -1, 1, 2)
    e0 = (Q(1, 3), Q(2, 7), Q(3, 5), Q(5, 11))
    b0 = (Q(2, 3), Q(4, 7), Q(1, 5), Q(7, 11))
    beta = Q(7, 3)
    actions = []
    for evec, bvec in ((e0, b0), (tuple(reversed(e0)), tuple(reversed(b0)))):
        jet = {}
        for a in range(1, 4):
            jet[a, 0] = beta * sum(ee * (-zz) ** a + (bb * zz if a == 1 else 0)
                                     for zz, ee, bb in zip(coords, evec, bvec))
        actions.append(jet)
    weights = [Q(1), Q(1)]
    w = wjet(weights, actions)
    xr = [deriv(s, 1) for s in actions]
    yr = [deriv(s, 2) for s in actions]
    check("Rindler_reflection_first", deriv(w, 1), 0)
    check("Rindler_reflection_third", deriv(w, 3), 0)
    check("Rindler_action_first", xr[0], beta * sum(z * (b - e) for z, e, b in zip(coords, e0, b0)))
    check("Rindler_action_second", yr[0], 2 * beta * sum(z * z * e for z, e in zip(coords, e0)))
    check("Rindler_W_second_contact", deriv(w, 2), mean(weights, yr) - cumul(weights, xr, xr))

    payload = {"status": "passed", "exact_checks": len(checks), "checks": checks,
               "fixtures": fixtures, "arithmetic": "fractions.Fraction; exact rational bivariate jets t<=3,u<=1",
               "assertion_tested": "Contact-complete E,E_u,K,K_u and reduced covariance formula equal independent -logZ jet derivatives in 16 five-state fixtures; local metric counterterm and Rindler reflection checks",
               "non_claims": ["No QCD ensemble", "No physical A or A_u", "No universal limiting assertion from finite fixtures", "No source phase-boundary data integrated as sphere stress"]}
    Path(result).write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"status": payload["status"], "exact_checks": len(checks), "fixtures": len(fixtures)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", required=True)
    main(parser.parse_args().result)
