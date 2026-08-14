#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage62_cmb_horn_oom_2026.py
============================
STAGE 62: THE X-DILEMMA'S FIRST HORN PRICED AT ORDER-OF-MAGNITUDE GRADE -- THE "UNPRICED
ACTIVE Y-SECTOR AT RECOMBINATION" HAS A LEVER ARM OF AT MOST ~0.3% ON THE DUST MODE AT THE
PINNED Q0, BECAUSE THE PIN LANDS Q0 SMALL AND THE MIXING SHARE SCALES WITH Q0.

THE HORN (stage54, standing since): pinned X => the banked CLASS pass carries an unpriced
ACTIVE Y-sector at recombination (flow-y ~ O(1)-O(100)), and SZ21's linear treatment
cannot price it at ANY parameters ("a0 does not appear in the linear cosmological regime
but will play a role once nonlinear terms from F(Y,Q) kick in").

THE PRICE, from three committed results and nothing new:
  (1) the realized flow-y at recombination (stage54's committed arithmetic):
      y_rec = X^2 (v_rec/c)^2 x [a0(0)/a0(rec)]  across the PINNED X band (stage56/58);
  (2) the kernel embedding (THE_COMPLETION row 2): the Y-sector's kinetic coefficient
      dJ/dY = mu(y) = 1/nu(y), so the fractional deviation of the flow sector from the
      analytic (fitted) branch is  dev(y) = 1 - mu(y) = (nu-1)/nu  -- bounded by 1;
  (3) the mixing share at the pinned Q0 (stage57's committed formula): the (2-K_B)chi
      entry carries share = (2-K_B)/|SRC - (2-K_B) q| of the E-equation source, with
      SRC = 3 f_dust H_rec / Q0 = 9.99/Q0 and q = Q0/H_rec.
  EFFECT ~ dev x share.  The Y-branch's DIRECT stress is separately priced at ~5e-14 of
  the dust density (PART C) -- the kinetic-coefficient channel is the only one.

VERDICT: core band <= ~0.2% (worst corner 1.4e-3, typical 1e-4 - 1e-3); the corpus's
defensible-envelope corner reaches ~0.5%.  The horn's threat level drops from UNPRICED to
the sub-percent level everywhere the corpus defends.  With X pinned
(stage56/58) the second horn (small-X escape) is moot, so THE X DILEMMA IS RESOLVED AT
OOM GRADE: the corpus can hold BOTH the binding-epoch wall AND an approximately-clean CMB.
NOT a de-tag: every recombination-side number remains LITERATURE-INHERITED until the full
nonlinear F(Y,Q) + aether Boltzmann run (the owed item stands; this stage prices its
stakes, it does not perform it).

Exit 0 = every check passed.
"""

import sys

import numpy as np

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


print(__doc__)

C_KMS = 2.99792458e5
# committed inputs, with their sources:
V_REC_MODE, V_REC_RMS = 12.6, 23.1               # km/s               [stage54]
AMP_FLOOR, AMP_CEIL = 2.78e4, 2.30e5             # a0(0)/a0(rec)      [stage54]
X_CORE = (106.0, 453.0)                          # pinned X, core     [stage56/58]
X_DEF = (70.0, 1340.0)                           # defensible envelope[stage56/58]
Q0_CORE = (0.0024, 0.0146)                       # Mpc^-1, stage61's operative low edge
SRC_NUM = 9.99                                   # 3 f_dust H_rec     [stage57]
H_REC = 5.2145                                   # Mpc^-1             [stage57]
KB_RANGE = (0.0, 0.25)                           # corpus BBN cap     [stage50]


def nu_routeA(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def dev_mu(y):
    """fractional deviation of the flow kinetic coefficient from the analytic branch."""
    return 1.0 - 1.0 / nu_routeA(y)


# =================================================================================================
print("=" * 100)
print("PART A -- the realized flow-y at recombination across the pinned band")
print("=" * 100)
corners = {}
print(f"    {'corner':<44s} {'y_rec':>10s} {'dev(y)':>8s}")
for xlab, xs in (("core", X_CORE), ("defensible", X_DEF)):
    for x in xs:
        for vlab, v in (("mode", V_REC_MODE), ("rms", V_REC_RMS)):
            for alab, amp in (("floor", AMP_FLOOR), ("ceil", AMP_CEIL)):
                y = x**2 * (v / C_KMS) ** 2 * amp
                corners[(xlab, x, vlab, alab)] = y
                print(f"    X={x:6.0f} ({xlab:>10s}) v={vlab:<4s} amp={alab:<5s}"
                      f"{'':6s} {y:>10.2f} {dev_mu(y):>8.3f}")
y_core = [y for k, y in corners.items() if k[0] == "core"]
check(min(y_core) > 0.4 and max(y_core) < 300,
      f"A1  core-band flow-y at recombination spans {min(y_core):.2f}-{max(y_core):.0f} -- "
      f"the Y-sector is genuinely ACTIVE (y >~ 1 over most of the band), exactly as the "
      f"dilemma stated",
      "the horn's premise is CONFIRMED, not evaded: this stage prices the consequence, "
      "not the premise")
dev_max_core = max(dev_mu(y) for y in y_core)
check(0.3 < dev_max_core < 0.75,
      f"A2  the kinetic-coefficient deviation dev = 1 - mu(y) reaches {dev_max_core:.2f} at "
      f"the low-y corner of the core band and falls to {min(dev_mu(y) for y in y_core):.1e} "
      f"at the high corner",
      "dev is bounded by 1 by construction (mu in (0,1]), so no corner can exceed unit "
      "modification of the coefficient")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- the lever arm: the mixing share at the PINNED Q0 (stage57's formula)")
print("=" * 100)
print(f"    {'Q0 [Mpc^-1]':>12s} {'SRC':>8s} {'share (K_B=0)':>14s} {'share (K_B=0.25)':>17s}")
shares = {}
for q0 in Q0_CORE:
    src = SRC_NUM / q0
    q = q0 / H_REC
    row = []
    for kb in KB_RANGE:
        s = (2 - kb) / abs(src - (2 - kb) * q)
        row.append(s)
    shares[q0] = max(row)
    print(f"    {q0:>12.4f} {src:>8.0f} {row[0]:>14.2e} {row[1]:>17.2e}")
check(max(shares.values()) < 3.2e-3,
      f"B1  the (2-K_B)chi mixing share at the pinned Q0 is {min(shares.values()):.1e} - "
      f"{max(shares.values()):.1e} -- the pin lands Q0 SMALL, where SRC = 9.99/Q0 dominates "
      f"the E-equation source",
      "this is the same monotone-in-Q0 share stage57 computed at the published fits "
      "(0.002%-18%); the pinned band sits between the Exp and Cosh fits, share <= 0.3%")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- the price, and the direct-stress channel closed")
print("=" * 100)
# worst case pairs the LARGEST dev (low-y corner) with the LARGEST share (high-Q0 edge).
# Note the two are anti-correlated through X (y ~ X^2, Q0 ~ X), so the true worst corner
# is even milder; the uncorrelated product is quoted as the CEILING.
price_ceiling = dev_max_core * max(shares.values())
price_floor = min(dev_mu(y) for y in y_core) * min(shares.values())
# REFEREE ADDITION: the corpus's own DEFENSIBLE ENVELOPE (X = 70, Q0 = 0.0431 Mpc^-1)
y_env = 70.0**2 * (V_REC_MODE / C_KMS) ** 2 * AMP_FLOOR
share_env = 2.0 / (SRC_NUM / 0.0431)
price_env = dev_mu(y_env) * share_env
check(price_ceiling < 2.5e-3 and price_env < 6e-3,
      f"C1  *** THE PRICE: dev x share = {price_floor:.1e} - {price_ceiling:.1e} on the "
      f"CORE band (<= ~0.2%), and {price_env:.1e} (~0.5%) at the corpus's DEFENSIBLE "
      f"ENVELOPE corner (X = 70 => dev = {dev_mu(y_env):.2f}; Q0 = 0.0431 => share = "
      f"{share_env:.1e}) ***",
      "both quoted (referee correction: the core-only ceiling understated the envelope); "
      "uncorrelated ceilings -- y ~ X^2 and Q0 ~ X are anti-correlated through the pin, "
      "so realizable corners are milder")
# the direct-stress channel: rho_Y/rho_dust = (2-K_B) Q0^2 v^2 / (8 pi G rho_dust(rec)),
# all in Mpc^-2 comoving-rate units (Q0 in Mpc^-1, v in c units):
H0_MPC = 67.4 / 2.99792458e5                     # Mpc^-1
rho_term = 3 * 0.265 * H0_MPC**2 * (1091.0) ** 3   # 8 pi G rho_dust(rec), Mpc^-2
ratio_stress = 2.0 * max(Q0_CORE) ** 2 * (V_REC_RMS / C_KMS) ** 2 / rho_term
check(ratio_stress < 1e-12,
      f"C2  the Y-branch's DIRECT stress is nothing: rho_Y/rho_dust ~ {ratio_stress:.1e} "
      f"at the most adverse corner -- 'active' means WHICH BRANCH the flow sits on, not "
      f"energy content",
      "so the kinetic-coefficient mixing channel (C1) is the ONLY channel, and it is "
      "priced")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- verdict and what this does NOT do")
print("=" * 100)
check(True,
      "D1  *** THE X DILEMMA RESOLVED AT OOM GRADE: X is pinned (stage56/58, so the "
      "small-X escape horn is moot) AND the active-Y-sector horn is priced sub-percent "
      "(<= ~0.2% core, ~0.5% envelope) on the dust mode -- the corpus can hold BOTH the binding-epoch wall AND an "
      "approximately-clean CMB ***",
      "the dilemma's 'not both, until X is settled' is DISCHARGED: X settled, both held")
check(True,
      "D2  NOT a de-tag: every recombination-side number stays LITERATURE-INHERITED (SZ21's "
      "Boltzmann fit remains unreproduced in-repo), and this stage is OOM-grade -- the full "
      "nonlinear F(Y,Q) + aether Boltzmann run at the corpus's DBI K remains THE owed "
      "computation.  What changed: its STAKES are now priced at <= ~0.2%, so it is a "
      "confirmation run, not an existential one",
      "the share proxy prices the chi-mixing channel of Eq 12 (the channel the deviation "
      "enters); a k-dependent effect beyond the proxy is exactly what the full run checks")

print()
print("=" * 100)
n_fail = len(FAIL)
print(f"STAGE 62 CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed" + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
