#!/usr/bin/env python3
"""Finite complete charge sectors: density commutators, spectral moments, gap tail.

The lattice identity is exact for its stated regulator. It is not a simulation
of scalar particle formation and does not establish a continuum occupied phase.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for n in range(total + 1):
            for tail in compositions(total - n, length - 1):
                yield (n,) + tail


def basis_fixed_q(L, Q):
    states = []
    for nb in range(Q // 2 + 1):
        for aa in compositions(Q - 2 * nb, L):
            for bb in compositions(nb, L):
                states.append(aa + bb)
    return states


def monomial(state, annihilate, create):
    out = list(state)
    amp = 1.0
    for i in annihilate:
        amp *= math.sqrt(out[i])
        out[i] -= 1
        if out[i] < 0:
            return None, 0.0
    for i in create:
        out[i] += 1
        amp *= math.sqrt(out[i])
    return tuple(out), amp


def operator(states, terms):
    ix = {s: i for i, s in enumerate(states)}
    out = np.zeros((len(states), len(states)), complex)
    for col, state in enumerate(states):
        for coefficient, annihilate, create in terms:
            dest, amp = monomial(state, annihilate, create)
            if amp:
                out[ix[dest], col] += coefficient * amp
    return out


def comm(a, b):
    return a @ b - b @ a


def run_case(Q, M):
    L, m = 4, 1.0
    states = basis_fixed_q(L, Q)
    ba, bb, conversion = [], [], []
    for j in range(L):
        jj = (j + 1) % L
        for offset, terms in ((0, ba), (L, bb)):
            terms.extend([(1., [j + offset], [jj + offset]),
                          (1., [jj + offset], [j + offset])])
        conversion.extend([(0.07, [j, j], [L + j]),
                           (0.07, [L + j], [j, j])])
    Ba, Bb = operator(states, ba), operator(states, bb)
    Hc = operator(states, conversion)
    ta, tb = 1 / (2 * m), 1 / (2 * M)
    diagonal = []
    for state in states:
        a, b = np.array(state[:L]), np.array(state[L:])
        diagonal.append((M - 2 * m) * sum(b) + 2 * ta * sum(a)
                        + 2 * tb * sum(b) + .11 * sum(a * (a - 1))
                        + .03 * sum(a * b) + .02 * sum(b * (b - 1)))
    H = np.diag(diagonal) - ta * Ba - tb * Bb + Hc
    ev, U = np.linalg.eigh(H)
    ground, gaps = U[:, 0], ev - ev[0]
    tests = []
    counts = {"matrix_identities": 0, "spectral_identities": 0, "zero_mode_controls": 0}
    max_error = 0.
    for k in (0., math.pi / 2, math.pi):
        phase = np.exp(-1j * k * np.arange(L))
        for label, wb in (("reference", 2 * m), ("bare_rest", M)):
            D = np.diag([m * np.dot(phase, s[:L]) + wb * np.dot(phase, s[L:]) for s in states])
            lhs = comm(D.conj().T, comm(H, D))
            rhs = 2 * (1 - math.cos(k)) * (ta * m * m * Ba + tb * wb * wb * Bb)
            rhs = rhs - (wb - 2 * m) ** 2 * Hc
            err = float(np.max(np.abs(lhs - rhs)))
            assert err < 2e-12, (Q, M, k, label, err)
            max_error = max(max_error, err)
            counts["matrix_identities"] += 1
            amplitudes_plus = U.conj().T @ D @ ground
            amplitudes_minus = U.conj().T @ D.conj().T @ ground
            moment = .5 * np.sum(gaps * (abs(amplitudes_plus) ** 2 + abs(amplitudes_minus) ** 2)) / L
            double = .5 * np.vdot(ground, lhs @ ground).real / L
            spectral_error = abs(moment - double)
            assert spectral_error < 2e-12
            counts["spectral_identities"] += 1
            if k == 0 and label == "reference":
                assert np.linalg.norm(comm(H, D)) < 1e-12
                assert abs(moment) < 1e-12
                counts["zero_mode_controls"] += 1
            if k == 0 and label == "bare_rest":
                expected = -(M - 2 * m) ** 2 * np.vdot(ground, Hc @ ground).real / (2 * L)
                assert abs(moment - expected) < 2e-12
                assert moment > 1e-10
                counts["zero_mode_controls"] += 1
            tests.append({"k": k, "operator": label, "moment": float(moment),
                          "commutator_error": err, "spectral_error": float(spectral_error)})
    assert np.linalg.norm(comm(H, H)) == 0
    return {"Q": Q, "M": M, "dimension": len(states), "counts": counts,
            "max_matrix_error": max_error, "rows": tests}


def gap_controls():
    # Units p_sat=a=d0=1; d(Delta)=Delta^(-alpha).
    # The target static moment is integral w/Delta=1. The dynamic first
    # moment has logarithmic UV divergence for alpha=0, finite alpha>0.
    analytic_integral = lambda L: math.asinh(L) - L / math.sqrt(1 + L * L)
    rows = []
    for L in (2., 10., 100., 1.e4):
        numerical = quad(lambda x: x*x/(1+x*x)**1.5, 0, L, epsabs=1e-11)[0]
        exact = analytic_integral(L)
        assert abs(numerical - exact) < 1e-9
        rows.append({"L": L, "integral_w_Delta": exact, "M1_constant_d": 2 * exact})
    static = quad(lambda x: 1/(1+x*x)**1.5, 0, np.inf)[0]
    assert abs(static - 1) < 1e-11
    alpha = 1 / 3
    number = quad(lambda x: x ** (1+alpha) / (1+x*x)**1.5, 0, np.inf)[0]
    dynamic = 2 * quad(lambda x: x ** (2-2*alpha)/(1+x*x)**1.5, 0, np.inf)[0]
    assert math.isfinite(number) and math.isfinite(dynamic)
    # For alpha=1/3,d0=1,m=4, each site saturates 2 Omega d²=m.
    assert abs(dynamic - 2 * number) < 1e-8
    return {"static_integral": static, "cutoff_rows": rows,
            "variable_d_alpha": alpha, "number_integral": number,
            "dynamic_M1": dynamic, "checks": 7,
            "interpretation": "An explicit variable-d moment-compatible family is not a physical dipole derivation."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    cases = [run_case(Q, M) for Q in (2, 4) for M in (2.002, 2.03)]
    result = {"status": "passed", "cases": cases, "gap_controls": gap_controls(),
              "bounds": {"max_dimension": 85, "L": 4, "Q": [2, 4]},
              "scope": "Complete finite lattice charge sectors; continuum identities derived analytically in SUM_RULES.md."}
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "passed", "cases": len(cases),
                      "matrix_identities": sum(c["counts"]["matrix_identities"] for c in cases),
                      "spectral_identities": sum(c["counts"]["spectral_identities"] for c in cases),
                      "zero_mode_controls": sum(c["counts"]["zero_mode_controls"] for c in cases),
                      "gap_checks": 7,
                      "max_matrix_error": max(c["max_matrix_error"] for c in cases)}))
