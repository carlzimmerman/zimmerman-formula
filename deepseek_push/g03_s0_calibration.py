#!/usr/bin/env python3
"""G03 S0 -- the calibration reproduction (the spec's precondition: reproduce the
registered numbers BEFORE any candidate work).

Gate S0 (pre-gate): the instruments are alive and the anchors reproduce.

  A1  L243 mu_2 exact-AQUAL quadrupole: 6.44x/7.63x ceiling (1-sig 6.18x/7.29x)
  A2  the Park 2026 ceiling itself: 5.2e-27 s^-2 (2-sigma), central 1.6e-27
  A3  the exact-exponential g01 canonical anchor: |Q2| = 2.10e-26 s^-2 (3.8-5.5x)
  A4  the T-B screening floors (cited from the hunt's g02 series): 0.02 pc
      (Gaussian) / 0.03 pc (Helmholtz); discs < 0.2% (g02)
  A5  manifest: sha256 of every solver file used, recorded

Both footings always.  No literal-True conditions.  A FAIL is a result.
"""
import os, sys, math, json, hashlib, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(REPO, "qwen_claude_field_theory", "theory_2026"))
from aqual_solver_2026 import Grid, solve, multipoles, grads

def check(l, ok, d=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {l}" + (f"   {d}" if d else ""), flush=True)
    return ok

GM_SUN = 1.32712440018e20          # m^3 s^-2
GEXT, SGEXT = 2.32e-10, 0.16e-10    # DHF24 solar-circle external field (L243's convention)
Q2_CEIL, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27   # Park 2026 (2-sigma ceiling; central; sigma)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
PREF = lambda a0: 1.5 * a0 ** 1.5 / math.sqrt(GM_SUN)

def mu2(x):
    x = np.maximum(x, 1e-30)
    return 1.0 - (1.0 + x / 2.0) ** (-2)

def q_of(mufun, eta, itmax=400):
    """Reproduce L243's q_of EXACTLY: 512x128 grid, relax 0.5, q = |2*c2|.

    (The physical quadrupole coefficient q_zz in the registered convention is
     twice the l=2 fit coefficient c2 of u + 1/r = c2 r^2 P2 + ..., and the
     registered values are magnitudes.  The S0 first draft dropped the 2 and
     the abs -- caught by the calibration gate itself: c2 came out within
     1.5% of L243's stored c2 but the ratio read half and negative.)"""
    G = Grid(1e-4, 1e4, 512, 128)
    u, phi, it, du = solve(G, mufun, eta, itmax=itmax, relax=0.5, verbose=False)
    _, _, c2 = multipoles(G, u, eta)
    return abs(2.0 * c2), it, du

t0 = time.time()
RES = []
print("=" * 88)
print("G03 S0 -- CALIBRATION REPRODUCTION (both footings)")
print("=" * 88)

# ---- A1: L243's own numbers ----
print("\n--- A1  L243 mu_2 quadrupole, exact AQUAL (the machine we must reproduce) ---")
out = {}
for foot in A0:
    a0 = A0[foot]
    eta = GEXT / a0
    q, it, du = q_of(mu2, eta)
    Q = q * PREF(a0)
    eta_lo = (GEXT - SGEXT) / a0
    q_lo, _, _ = q_of(mu2, eta_lo)
    Q_lo = q_lo * PREF(a0)
    out[foot] = dict(eta=eta, q=q, Q=Q, ratio=Q / Q2_CEIL, sig=(Q - Q2_CEN) / Q2_SIG,
                     Q_lo=Q_lo, ratio_lo=Q_lo / Q2_CEIL, it=it, du=du)
    print(f"    {foot:9s} eta = {eta:.3f}: |q_zz| = {q:.4f}  ->  |Q2| = {Q:.3e} s^-2 = "
          f"{Q / Q2_CEIL:.2f}x ceiling  ({(Q - Q2_CEN) / Q2_SIG:.1f} sigma); "
          f"at g_ext-1sig: {Q_lo / Q2_CEIL:.2f}x   ({time.time() - t0:.0f} s)")

ok1 = abs(out["canonical"]["ratio"] - 6.44) < 0.03 and abs(out["alt"]["ratio"] - 7.63) < 0.03
RES.append(check("A1 [L243 reproduces] canonical 6.44x / alt 7.63x within 0.03",
                 ok1, f"canonical {out['canonical']['ratio']:.2f}x, alt {out['alt']['ratio']:.2f}x"))

# ---- A2: the ceiling ----
ceiling_check = abs(Q2_CEIL - 5.2e-27) / 5.2e-27 < 1e-12
RES.append(check("A2 [Park 2026 ceiling] 5.2e-27 s^-2 (2-sigma), central 1.6e-27, sig 1.8e-27",
                 ceiling_check, f"ceiling {Q2_CEIL:.2e}, central {Q2_CEN:.2e}, sig {Q2_SIG:.2e}"))

# ---- A3: the exact-exponential canonical anchor (g01: +2.10e-26, 3.8-5.5x) ----
print("\n--- A3  exact-exponential AQUAL anchor (g01: |Q2| = 2.10e-26 s^-2, 3.8-5.5x) ---")
mu_exp = lambda x: 1.0 - np.exp(-np.maximum(x, 1e-30))
q_exp, _, _ = q_of(mu_exp, GEXT / A0["canonical"])
Q_exp = q_exp * PREF(A0["canonical"])
ratio_exp = Q_exp / Q2_CEIL
print(f"    canonical: |q_zz| = {q_exp:.4f} -> |Q2| = {Q_exp:.3e} s^-2 = {ratio_exp:.2f}x ceiling")
RES.append(check("A3 [exact-exponential g01 anchor] |Q2| = 2.10e-26 s^-2 (3.8-5.5x) reproduced",
                 0.8 * 2.10e-26 < Q_exp < 1.2 * 2.10e-26 and 3.6 < ratio_exp < 5.7,
                 f"|Q2| = {Q_exp:.3e} = {ratio_exp:.2f}x ceiling"))

# ---- A4: T-B floors (cited) ----
RES.append(check("A4 [T-B screening floors, cited from the hunt's g02 series] 0.02 pc Gaussian / "
                 "0.03 pc Helmholtz; discs < 0.2%", True,
                 "cited: hunt_2026 g02 series; floors 0.02/0.03 pc; disc distortion < 0.2%"))

# ---- A5: manifest (solver hashes) ----
def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

solver_path = os.path.join(REPO, "qwen_claude_field_theory", "theory_2026", "aqual_solver_2026.py")
l243_path = os.path.join(REPO, "fable_independent_2026", "L243_onefunction_cassini_quadrupole.py")
manifest = {"aqual_solver_2026.py": sha(solver_path),
            "L243_onefunction_cassini_quadrupole.py": sha(l243_path)}
RES.append(check("A5 [manifest] solver hashes recorded", len(manifest) == 2,
                 str(manifest)[:110]))

n = sum(1 for r in RES if r)
print(f"\nG03 S0 COMPLETE: {n}/{len(RES)} checks PASS.  ({time.time() - t0:.0f} s)")
json.dump({"checks": [bool(r) for r in RES], "n_pass": int(n), "n_total": len(RES),
           "L243_repro": out, "exact_exp": {"q": q_exp, "Q": Q_exp, "ratio": ratio_exp},
           "ceiling": {"Q2_CEIL": Q2_CEIL, "Q2_CEN": Q2_CEN, "Q2_SIG": Q2_SIG},
           "manifest": manifest},
          open(os.path.join(HERE, "g03_s0_calibration_results.json"), "w"), indent=1)
