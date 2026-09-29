#!/usr/bin/env python3
"""Q1-2 -- induced current of a charged Dirac fermion in dS_4: DIRECT mode sum with order-2 adiabatic subtraction inside the integrand vs the published closed form
(Hayashinaka-Fujita-Yokoyama, arXiv:1603.04165, eq. 3.12, transcribed from the LaTeX source).

Pre-registered in Q1_PREREGISTRATION.md (with Amendments 1-3; written before this script was run).  Units H = 1, tau = -1 (a = 1), planar patch.
  J_HFY(L, M) = <J^3>_ren/(e a^3 H^3) = (1/(4 pi^2)) Int_0^inf k^2 dk Int_{-1}^{1} dr [ P_exact(k, r) - P_ad(k, r) ],   P = s_z(+k_perp) + s_z(-k_perp)
with the exact positive-frequency Whittaker modes (validated in q1_1_dirac_modes_ds4.py) and P_ad = order-<=2 Bloch-vector adiabatic series (built symbolically in q1_lib.py).
Quadrature: log-spaced Gauss-Legendre in k on (1e-6, K], Gauss-Legendre in r, fitted large-k tail c2/k^2 + c3/k^3 + c4/k^4 (as AH4).

Run:     python3 q1_2_induced_current_ds4.py                       (real run; comparator = the AMENDED closed form, the printed one is reported alongside; exit 0 iff all real checks pass)
         python3 q1_2_induced_current_ds4.py --variant printed     (the FIRST-RUN configuration: the comparator is (3.12) exactly as printed)
         python3 q1_2_induced_current_ds4.py --mutate              (control: the order-2 adiabatic term is dropped from the subtraction (order 0 only); V1 must FAIL;
                                                                    exit 1 if the targeted check FAILS as required, exit 3 if it does NOT fail = the control has no power)
"""
import sys
sys.dont_write_bytecode = True
import math
import time
import numpy as np
import mpmath as mp
from concurrent.futures import ProcessPoolExecutor
from q1_lib import PI, sz_pair, ad_pair, hfy_closed, hfy_weak

MUTATE = "--mutate" in sys.argv
VARIANT = "printed" if ("--variant" in sys.argv and sys.argv[sys.argv.index("--variant") + 1] == "printed") else "amended"
ORDER = 0 if MUTATE else 2
CHECKS = {}


def check(tag, ok, detail=""):
    CHECKS[tag.split()[0]] = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def g_of_k(k, L, M, n_r, order, raw=False):
    """g(k) = k^2 Int dr [P_exact - P_ad] (or the raw k^2 Int dr P_exact)."""
    xr, wr = np.polynomial.legendre.leggauss(n_r)
    tot = 0.0
    for r, w in zip(xr, wr):
        d = sz_pair(k, float(r), L, M)
        if not raw:
            d -= ad_pair(k, float(r), L, M, order=order)
        tot += w * d
    return k * k * tot


def _segment(args):
    a, b, L, M, n_gl, n_r, order = args
    xg, wg = np.polynomial.legendre.leggauss(n_gl)
    s = 0.0
    for x, w in zip(xg, wg):
        k = 0.5 * (b - a) * x + 0.5 * (b + a)
        s += 0.5 * (b - a) * w * g_of_k(k, L, M, n_r, order)
    return s


def _init():
    mp.mp.dps = 22


def _point(args):
    L, M, Ks, n_seg, n_gl, n_r, order = args
    mp.mp.dps = 22
    k0 = 1e-6
    Kmax = max(Ks)
    edges = np.exp(np.linspace(math.log(k0), math.log(Kmax), n_seg + 1))
    # cumulative truncated integrals at each requested K (K values must be edge values -> build edges through them)
    out = {}
    # rebuild edges so that every K in Ks is an edge
    pts = sorted(set([k0] + list(Ks)))
    edges = []
    for lo, hi in zip(pts[:-1], pts[1:]):
        n = max(4, int(round(n_seg * (math.log(hi) - math.log(lo)) / (math.log(Kmax) - math.log(k0)))))
        seg = np.exp(np.linspace(math.log(lo), math.log(hi), n + 1))
        edges += list(seg[:-1])
    edges.append(Kmax)
    edges = np.array(edges)
    cum = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        cum += _segment((a, b, L, M, n_gl, n_r, order))
        for K in Ks:
            if abs(b - K) < 1e-9 * K:
                out[K] = cum
    res = {}
    for K in Ks:
        ks = np.array([0.5 * K, 0.75 * K, K])
        fs = np.array([g_of_k(kk, L, M, n_r, order) * kk * kk for kk in ks])
        A = np.array([[1.0, 1.0 / kk, 1.0 / (kk * kk)] for kk in ks])
        c2, c3, c4 = np.linalg.solve(A, fs)
        tail = c2 / K + c3 / (2 * K * K) + c4 / (3 * K ** 3)
        res[K] = (out[K] / (4 * PI ** 2), (out[K] + tail) / (4 * PI ** 2), c2)
    return res


def _rawfit(args):
    L, M, ks, n_r = args
    mp.mp.dps = 22
    return [g_of_k(k, L, M, n_r, 2, raw=True) / (4 * PI ** 2) for k in ks]


if __name__ == "__main__":
    print("=" * 112)
    print(f"Q1-2 induced current of a Dirac fermion in dS_4 -- mode: " + ("MUTATE CONTROL (order-2 adiabatic term dropped)" if MUTATE else "REAL RUN") + f"   comparator variant: {VARIANT}")
    print("=" * 112, flush=True)
    ex = ProcessPoolExecutor(max_workers=14, initializer=_init)

    # ------------------------------------------------------------------ V0: transcription of (3.12)
    print("\n0. closed form (3.12) from the LaTeX source: finite and linear as L -> 0, odd in L, and -> the weak-field formula (4.3)")

    def v0(variant):
        ok = True
        lines = []
        for M in (0.5, 1.0, 2.0):
            a3 = hfy_closed(1e-3, M, variant=variant) / 1e-3
            a4 = hfy_closed(1e-4, M, variant=variant) / 1e-4
            wk = hfy_weak(M)
            rel = abs(a4 - a3) / max(abs(a3), 1e-300)
            relw = abs(a4 - wk) / abs(wk)
            lines.append(f"     [{variant}] M = {M}: J/L at 1e-3: {a3:+.6e}   at 1e-4: {a4:+.6e}   (4.3): {wk:+.6e}   rel(1e-3 vs 1e-4) {rel:.1e}   rel(1e-4 vs (4.3)) {relw:.1e}")
            ok = ok and rel < 1e-3 and relw < 1e-4
        fp = hfy_closed(0.4, 1.0, variant=variant)
        fm = hfy_closed(-0.4, 1.0, variant=variant)
        odd = abs(fp + fm) / abs(fp)
        lines.append(f"     [{variant}] oddness: J(+0.4, 1.0) = {fp:+.8f}, J(-0.4, 1.0) = {fm:+.8f}, |J(+)+J(-)|/|J(+)| = {odd:.1e}")
        return ok and odd < 1e-3, lines
    v0p_ok, lines = v0("printed")
    print("\n".join(lines))
    v0a_ok, lines = v0("amended")
    print("\n".join(lines))
    if VARIANT == "printed":
        check("V0 the closed form (3.12) exactly as printed is finite and linear as L -> 0, odd, and equals (4.3) at L -> 0", v0p_ok, "")
    else:
        check("V0a the AMENDED closed form (Ei prefactor e^{-2 pi r s}) is finite and linear as L -> 0, odd, and equals (4.3) at L -> 0", v0a_ok, "")
        print(f"     (informational, registered in the first run: the closed form exactly as printed passes V0: {v0p_ok})")

    # ------------------------------------------------------------------ V1: direct vs closed form
    GRID = [(0.5, 2.0), (1.0, 1.5), (0.3, 1.0), (0.5, 0.6), (1.5, 0.8), (0.4, 1.4), (0.3, 3.0), (2.0, 1.0), (0.2, 0.4), (0.05, 1.0), (0.05, 3.0), (0.3, 0.15)]
    print(f"\n1. DIRECT mode sum (order-{ORDER} adiabatic subtraction inside the integrand; K = 200; tail fitted) vs closed form (3.12) [{VARIANT}]")
    t0 = time.time()
    futs = [ex.submit(_point, (L, M, [200.0], 80, 16, 40, ORDER)) for (L, M) in GRID]
    res = [f.result() for f in futs]
    print(f"     ({time.time() - t0:.0f} s)")
    print("     L       M       direct J_HFY      closed J_HFY     ratio       tail c2")
    ratios = []
    closed_vals = {}
    for (L, M), r_ in zip(GRID, res):
        jd = r_[200.0][1]
        jc = hfy_closed(L, M, variant=VARIANT)
        closed_vals[(L, M)] = jc
        ratios.append(jd / jc)
        print(f"     {L:5.2f}  {M:5.2f}   {jd:+.9f}   {jc:+.9f}   {jd / jc:+.6f}   {r_[200.0][2]:+.2e}", flush=True)
    worst = max(abs(abs(x) - 1.0) for x in ratios)
    same_sign = all((x > 0) == (ratios[0] > 0) for x in ratios)
    v1_ok = worst <= 2e-3 and same_sign
    print(f"     worst | |ratio| - 1 | = {worst:.2e}; sign of direct/closed: {'+' if np.median(ratios) > 0 else '-'} ({'consistent' if same_sign else 'INCONSISTENT'})")
    check("V1 direct = closed form (3.12) on the twelve-point grid, worst relative difference <= 2e-3, one consistent sign", v1_ok, f"(variant {VARIANT}; worst {worst:.1e})")
    if VARIANT == "amended" and not MUTATE:
        # also the printed one, for the record
        rp = [res[i][200.0][1] / hfy_closed(L, M, variant="printed") for i, (L, M) in enumerate(GRID)]
        print("     (informational: direct/closed with (3.12) exactly as printed:  " + ", ".join(f"{x:+.3g}" for x in rp) + ")")

    if MUTATE:
        failed = not CHECKS["V1"]
        print("\nMUTATE CONTROL: the order-2 adiabatic term was dropped from the subtraction (order 0 only; s_1 cancels in the block sum).")
        print(f"  V1 {'FAILED as required -- the control works' if failed else 'DID NOT FAIL -- the check has no power'}")
        sys.exit(1 if failed else 3)

    # ------------------------------------------------------------------ V1s: sign / Schwinger limit at large L
    print("\n1s. sign check independent of the comparator: large L, direct sum vs the Minkowski Schwinger asymptote of HFY (4.2): J ~ L^2 e^{-pi M^2/L}/(6 pi^3)")
    L, M = 8.0, 1.0
    rs = ex.submit(_point, (L, M, [400.0], 100, 16, 40, 2)).result()
    jd = rs[400.0][1]
    asym = L ** 2 * math.exp(-PI * M ** 2 / L) / (6 * PI ** 3)
    print(f"     L = {L}, M = {M}: direct J_HFY = {jd:+.6f}   (4.2) asymptote {asym:+.6f}   ratio {jd / asym:.3f}   closed (3.12)[{VARIANT}] = {hfy_closed(L, M, variant=VARIANT):+.6f}")
    check("V1s at L = 8, M = 1 the direct J_HFY is positive and within [0.6, 1.6] of the Schwinger asymptote (4.2)", jd > 0 and 0.6 <= jd / asym <= 1.6, "")

    # ------------------------------------------------------------------ V1r: ln Lambda coefficient from the raw exact modes
    print("\n1r. RAW exact-mode integrand G(k) = (k^2/(4 pi^2)) Int dr P_exact (no adiabatic terms): fit c1 k + c0 + c_{-1}/k + c_{-2}/k^2 + c_{-3}/k^3, (L, M) = (0.3, 1.0)")
    Lr, Mr = 0.3, 1.0
    KS = [60.0, 90.0, 135.0, 200.0, 300.0, 450.0]
    futs = [ex.submit(_rawfit, (Lr, Mr, [k], 64)) for k in KS]
    G = np.array([f.result()[0] for f in futs])
    A = np.array([[k, 1.0, 1.0 / k, 1.0 / k ** 2, 1.0 / k ** 3] for k in KS])
    coef, *_ = np.linalg.lstsq(A, G, rcond=None)
    c1, c0, cm1, cm2, cm3 = coef
    e1, em1 = -2 * Lr / (3 * PI ** 2), Lr / (3 * PI ** 2)
    print(f"     fit: c1 = {c1:+.8f} (expected {e1:+.8f}, rel {abs(c1 / e1 - 1):.1e});  c0 = {c0:+.2e};  c_-1 = {cm1:+.8f} (expected {em1:+.8f}, rel {abs(cm1 / em1 - 1):.1e});  c_-2 = {cm2:+.3e}, c_-3 = {cm3:+.3e}")
    check("V1r exact-mode raw integrand: c1 = -2L/(3 pi^2) and c_{-1} = +L/(3 pi^2) (the ln Lambda coefficient 1/(3 pi^2)) to 3%, |c0| <= 3e-3 |c1|",
          abs(c1 / e1 - 1) < 0.03 and abs(cm1 / em1 - 1) < 0.03 and abs(c0) <= 3e-3 * abs(c1), "")

    # ------------------------------------------------------------------ V2: K convergence
    print("\n2. K-convergence of the truncated (no tail) subtracted integral at (L, M) = (0.3, 1.0): order 2 (real) and order 0 only (the control configuration, run here for the record)")
    KK = [100.0, 200.0, 400.0]
    f2 = ex.submit(_point, (0.3, 1.0, KK, 100, 16, 40, 2))
    f0 = ex.submit(_point, (0.3, 1.0, KK, 100, 16, 40, 0))
    r2, r0 = f2.result(), f0.result()
    print("     K        order 2 truncated   order 2 +tail      order 0 truncated")
    for K in KK:
        print(f"     {K:6.0f}   {r2[K][0]:+.9f}    {r2[K][1]:+.9f}    {r0[K][0]:+.9f}")
    drift2 = abs(r2[400.0][1] - r2[100.0][1]) / abs(r2[400.0][1])
    drift2_trunc = abs(r2[400.0][0] - r2[100.0][0]) / abs(r2[400.0][1])
    drift0 = abs(r0[400.0][0] - r0[100.0][0]) / abs(r2[400.0][1])
    print(f"     relative drift K = 100 -> 400: order 2 with fitted tail {drift2:.2e} (truncated, no tail: {drift2_trunc:.2e}, the k^-3 remainder);  order 0 only (truncated) {drift0:.2e}  (log divergence L ln4/(3 pi^2) = {0.3 * math.log(4) / (3 * PI ** 2):.5f} in absolute terms)")
    check("V2 (Amendment 3 wording) the order-2-subtracted integral with its fitted tail converges (drift K = 100 -> 400 < 1e-4 relative) whereas order 0 only drifts by > 5% (logarithmic divergence)", drift2 < 1e-4 and drift0 > 0.05, "")

    print("\n" + "=" * 112)
    passed = sum(CHECKS.values())
    print(f"CHECKS: {passed}/{len(CHECKS)} passed   (comparator variant: {VARIANT})")
    print("Scope: one Dirac fermion, minimal coupling, dS_4 planar patch, in-vacuum, constant-energy-density field, order-2 adiabatic subtraction; no backreaction.")
    sys.exit(0 if passed == len(CHECKS) else 1)
