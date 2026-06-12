#!/usr/bin/env python3
"""
agentHH independent fit (2026-06-12): the keystone extraction redone with an independent fitter.

Context: the saved agentHH script's fit_osc_model collapses numerically (overflow at L1054; q pegs
at +155.0364 in BOTH 3d2 and 3d runs = a broken bound/init in code the agent was editing when it
died). The pipeline DATA are sound (the [3d-1] scan table is byte-identical across two independent
runs; the pipeline itself is gate-validated to 1e-35 against Gamma closed forms). This script fits
that banked table with scipy, with three honesty guards:
  (G1) SELF-VALIDATION: fit the 'pred' column first — it is the bare (C1) target with KNOWN
       parameters (A=1, q=-1/3, al=ct=2.1388, be=sqrt3*ct, phi=pi/8, s=1/3). The fitter must
       recover them or its verdict on the data column is void.
  (G2) MULTI-START: 200 dispersed random inits (s in [0.15,0.8], al in [0.3,6], be/al in [0.5,4],
       q in [-3,1]) — report the global best and the spread; no init placed at the target.
  (G3) RIVAL INDICES: best fits with s FROZEN at 1/2 and 1 (the rival classes) — compare residuals.
Model: D(nu) = A * nu^q * exp(-al*nu^s) * cos(be*nu^s + phi), fit SIGNED on all 16 points.
Targets (from the script's own printed targets): s=1/3, al=2.13875, be/al=sqrt3=1.73205, q=-1/3.
"""
import numpy as np
from scipy.optimize import least_squares

rng = np.random.default_rng(20260612)

nu = np.array([4.096, 5.832, 8.000, 10.648, 13.824, 17.576, 21.952, 27.000,
               32.768, 39.304, 46.656, 54.872, 64.000, 74.088, 85.184, 97.336])
D = np.array([+1.435222e-02, -7.748661e-03, -1.363932e-02, -8.348990e-03,
              -1.349531e-03, +2.470333e-03, +2.873668e-03, +1.598310e-03,
              +2.489429e-04, -4.582363e-04, -5.406332e-04, -3.145350e-04,
              -6.577796e-05, +7.273299e-05, +9.753810e-05, +6.179302e-05])
P = np.array([+1.531819e-02, +6.883945e-03, +3.135830e-04, -2.336846e-03,
              -2.232369e-03, -1.141146e-03, -1.937461e-04, +2.546777e-04,
              +3.048780e-04, +1.809094e-04, +4.872908e-05, -2.481293e-05,
              -4.152249e-05, -2.854844e-05, -1.015426e-05, +1.761193e-06])
CT = 2.13875
TGT = dict(s=1/3, al=CT, lock=np.sqrt(3.0), q=-1/3)

def model(p, x):
    A, q, al, be, phi, s = p
    return A * x**q * np.exp(-al * x**s) * np.cos(be * x**s + phi)

# FIXED reference envelope for weighting (fit-INDEPENDENT — v1's fit-dependent weights let the
# optimizer inflate A to deflate the cost; caught by the G1 self-validation, fixed here):
# scale weights by the data's own decade via a smooth |y| envelope estimate.
def make_weights(x, y):
    ay = np.abs(y)
    # smooth envelope estimate: running max over neighbors, then geometric smoothing
    env = np.array([max(ay[max(0, i - 1):i + 2].max(), 1e-12) for i in range(len(ay))])
    return 1.0 / env

def resid(p, x, y, w):
    return (model(p, x) - y) * w

def fit_multistart(x, y, n=200, s_fix=None, q_fix=None):
    w = make_weights(x, y)
    best, sols = None, []
    for _ in range(n):
        s0 = s_fix if s_fix is not None else rng.uniform(0.15, 0.8)
        q0 = q_fix if q_fix is not None else rng.uniform(-3, 1)
        al0 = rng.uniform(0.3, 6.0)
        p0 = [rng.uniform(0.2, 5) * rng.choice([-1, 1]), q0,
              al0, al0 * rng.uniform(0.5, 4.0), rng.uniform(-np.pi, np.pi), s0]
        lo = [-50, -3 if q_fix is None else q_fix - 1e-12, 0.1, 0.1, -2 * np.pi,
              0.05 if s_fix is None else s_fix - 1e-12]
        hi = [50, 1 if q_fix is None else q_fix + 1e-12, 12, 40, 2 * np.pi,
              1.2 if s_fix is None else s_fix + 1e-12]
        try:
            r = least_squares(resid, p0, args=(x, y, w), bounds=(lo, hi), max_nfev=20000)
        except Exception:
            continue
        c = float(np.sum(r.fun**2))
        sols.append((c, r.x))
        if best is None or c < best[0]:
            best = (c, r.x)
    return best, sols

def report(tag, best, sols):
    c, (A, q, al, be, phi, s) = best
    lock = be / al
    print(f"  [{tag}] cost = {c:.4e}  s = {s:.5f}  al = {al:.5f}  be/al = {lock:.5f}  "
          f"q = {q:+.4f}  A = {A:+.4f}  phi = {phi:+.4f}")
    near = [x for x in sols if x[0] < 1.5 * c]
    ss = np.array([x[1][5] for x in near]); als = np.array([x[1][2] for x in near])
    print(f"        basin: {len(near)}/{len(sols)} starts within 1.5x cost; "
          f"s spread [{ss.min():.4f},{ss.max():.4f}]  al spread [{als.min():.4f},{als.max():.4f}]")
    return c, s, al, lock, q

print("=" * 100)
print("agentHH INDEPENDENT FIT — the keystone extraction, scipy, multi-start, self-validated")
print("=" * 100)

print("\n(G1) SELF-VALIDATION on the 'pred' column (known: A=1, q=-1/3, al=2.13875, "
      "be/al=1.73205, phi=0.3927, s=1/3):")
bestP, solsP = fit_multistart(nu, P)
cP, sP, alP, lockP, qP = report("pred", bestP, solsP)
okP = (abs(sP - 1/3) < 0.01 and abs(alP / CT - 1) < 0.02 and abs(lockP / np.sqrt(3) - 1) < 0.02)
print(f"        SELF-VALIDATION: {'PASS' if okP else 'FAIL'} "
      f"(|s-1/3|={abs(sP-1/3):.4f}, al/ct={alP/CT:.4f}, lock/sqrt3={lockP/np.sqrt(3):.4f})")

print("\n(G2) THE DATA column, s free, 200 dispersed starts:")
bestD, solsD = fit_multistart(nu, D)
cD, sD, alD, lockD, qD = report("data", bestD, solsD)
print(f"        vs targets: |s-1/3| = {abs(sD-1/3):.4f}; al/ct = {alD/CT:.4f}; "
      f"lock/sqrt3 = {lockD/np.sqrt(3):.4f}; q = {qD:+.4f} (target -1/3)")

print("\n(G3) RIVAL INDICES (s frozen):")
for sfx in (0.5, 1.0):
    b, ss = fit_multistart(nu, D, n=120, s_fix=sfx)
    print(f"  s = {sfx}: best cost = {b[0]:.4e}  (free-s best = {cD:.4e}; "
          f"ratio = {b[0]/cD:.2f}x worse)" if b else f"  s = {sfx}: no convergence")

print("\n(G4) CONSTRAINED CLASS FIT — q = -1/3 theory-fixed (removes the finite-window envelope")
print("      degeneracy q<->al; the class prescribes q, the fit tests s/al/lock):")
print("  pred (self-validation, q fixed):")
bP2, sP2 = fit_multistart(nu, P, q_fix=-1/3)
cP2, sPv, alPv, lockPv, _ = report("pred|q", bP2, sP2)
okP2 = (abs(sPv - 1/3) < 0.01 and abs(alPv / CT - 1) < 0.03 and abs(lockPv / np.sqrt(3) - 1) < 0.03)
print(f"        SELF-VALIDATION (constrained): {'PASS' if okP2 else 'FAIL'} "
      f"(|s-1/3|={abs(sPv-1/3):.4f}, al/ct={alPv/CT:.4f}, lock/sqrt3={lockPv/np.sqrt(3):.4f})")
print("  data (q fixed):")
bD2, sD2 = fit_multistart(nu, D, q_fix=-1/3)
cD2, sDv, alDv, lockDv, _ = report("data|q", bD2, sD2)
print(f"        vs targets: |s-1/3| = {abs(sDv-1/3):.4f}; al/ct = {alDv/CT:.4f}; "
      f"lock/sqrt3 = {lockDv/np.sqrt(3):.4f}")
print("\nVERDICT-INPUT: the decisive read is (G4): self-validation must PASS constrained, and the "
      "data fit's (s, al, lock) vs targets + (G3)'s rival rejection then constitute the record.")
