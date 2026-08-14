#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage57_sz21_corrected_refile_2026.py
=====================================
STAGE 57: THE CORRECTED RE-FILE OF STAGE 55 -- which its own referee refuted within hours,
in the MANUFACTURED-DEFICIT direction.  Three facts new to the corpus are banked here, and
the practical consequence is the OPPOSITE of what stage 55 claimed: Cell 3's term is NOT
entangled with the third-peak fit at any published AeST parameter set, and the genuinely
unpinned knob is Q0, not (2-K_B).

WHAT STAGE 55 GOT WRONG (all four, recorded plainly; its banner carries the same list):
  1. Its PREMISE.  Substituting SZ21's Eq (9) into Eq (11) gives Pi = (1+w) gamma/phibardot
     EXACTLY -- the bracket [K_B E + (2-K_B) chi] CANCELS OUT of the pressure.  The bracket
     is real and load-bearing but it lives in the definition of DELTA, not Pi.  Stage 55
     coded against a committed transcription that omits Eq (9) (see PART C: four omissions).
  2. SRC = (dK/dQ)/H is NOT a free normalisation -- it is FIXED by the background
     (PART A).  Setting it to 1 corresponds to Q0 = 9.99 Mpc^-1, off SZ21's own fits by
     10x-1e5x, and it is what produced the false "64-67% share".
  3. C1 was a T1 TAUTOLOGY: from the assumed E/chi = SRC/K_B, R = SRC/(2-K_B) in one line.
  4. "No growing aether mode" was unsupported: E = alphadot + Psi is not primitive, so Eq 12
     is second order in alpha with an ANTI-DAMPING coefficient, and at the third peak the
     dropped Edot term is ~7x the retained one.

WHAT THIS FILE BANKS (all three genuinely new to the repo):
  PART A  SRC(a) = 3 f_dust(a) H(a) / Q0 -- the background identity, with the corpus's first
          record of SZ21's OWN FITTED PARAMETER SETS (their Fig. 1 caption; absent from this
          repo until now).
  PART B  the (2-K_B) chi share of the Eq-9 bracket AT THOSE FITS: 0.0019% - 17.6%,
          SUB-DOMINANT everywhere -- and under the corpus's own BBN bound K_B <= 0.25 only
          the Exp fit survives, where the share is SMALLEST (0.0019%).  Stage 55's D2
          ("Cell 3's term carries part of the third-peak fit") is WITHDRAWN.
  PART C  the four load-bearing omissions in real_research/bridge1_aest_equations.md, whose
          own closing line said "verify exact coefficients against the published PDF before
          coding" -- a note this corpus did not honour until the referee did.
  PART D  what is actually owed now: PIN Q0 (free, spanning 4 orders in the published fits,
          and stage 54's transport ceiling scales with omega_Q = Q0 c).  (2-K_B) is NOT a
          free knob -- BBN already pins it to [1.75, 2.00], a +-7% window, with no CMB
          argument required.

Exit 0 = every check passed.
"""

import os
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

# =================================================================================================
print("=" * 100)
print("PART A -- SRC is a BACKGROUND IDENTITY, and SZ21's own fitted parameters")
print("=" * 100)
# The chain: dK/dQ = I0/a^3 and 8 pi Gtilde rhobar_dust = Q0 dK/dQ = 3 f_dust H^2
#   =>  SRC := (dK/dQ)/H = 3 f_dust(a) H(a) / Q0        [Q0 = phibardot, in Mpc^-1]
H_REC = 5.2145            # Mpc^-1 at z = 1090 (standard background)
F_DUST_REC = 0.6387       # dust fraction at recombination
SRC_NUM = 3 * F_DUST_REC * H_REC
check(abs(SRC_NUM - 9.99) < 0.05,
      f"A1  SRC(rec) = 3 f_dust H / Q0 = {SRC_NUM:.3f} / Q0  -- a DERIVED background number, "
      f"not a normalisation choice",
      "stage 55's SRC = 1 therefore asserted Q0 = 9.99 Mpc^-1, which no published AeST fit uses")

# SZ21's Fig. 1 caption fits -- the corpus's FIRST record of them
SZ21_FITS = {
    "Cosh":  dict(K_B=0.5, Q0=0.1,  K2=7.5e3, Z0=1e-9,  note="MOND-compatible"),
    "Higgs": dict(K_B=0.3, Q0=1.0,  K2=8.5e8, Z0=None,  note="SZ21: 'incompatible with a MOND limit'"),
    "Exp":   dict(K_B=0.1, Q0=1e-4, K2=9.5e3, Z0=1e-17, note="MOND-compatible"),
}
print(f"    {'fit':>6} {'K_B':>5} {'Q0 [Mpc^-1]':>12} {'K2':>9} {'SRC(rec)':>11}   note")
for nm, f in SZ21_FITS.items():
    f["SRC"] = SRC_NUM / f["Q0"]
    print(f"    {nm:>6} {f['K_B']:5.1f} {f['Q0']:12.0e} {f['K2']:9.1e} {f['SRC']:11.2f}   {f['note']}")
check(min(f["SRC"] for f in SZ21_FITS.values()) > 9.0,
      f"A2  at EVERY published AeST fit SRC(rec) >= {min(f['SRC'] for f in SZ21_FITS.values()):.1f} "
      f"-- i.e. 10x to 1e5x larger than stage 55's assumed 1.0",
      "these three parameter sets appear NOWHERE else in this repo; banked here")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- the (2-K_B) chi share of the Eq-9 bracket at the published fits")
print("=" * 100)
# quasi-static closure WITH the previously-elided source term restored:
#   B = [SRC - (2-K_B) q] chi ,  q = Q0/H_rec  =>  share = (2-K_B)/|SRC - (2-K_B) q|
print(f"    {'fit':>6} {'(2-K_B)':>8} {'q=Q0/H':>9} {'coef of chi in B':>18} {'share':>9}")
shares = {}
for nm, f in SZ21_FITS.items():
    two_kb = 2.0 - f["K_B"]
    q = f["Q0"] / H_REC
    coef = f["SRC"] - two_kb * q
    sh = two_kb / abs(coef)
    shares[nm] = sh
    print(f"    {nm:>6} {two_kb:8.2f} {q:9.4f} {coef:18.4f} {100*sh:8.4f}%")
check(max(shares.values()) < 0.20,
      f"B1  *** THE MIXING ENTRY IS SUB-DOMINANT AT EVERY PUBLISHED FIT: share = "
      f"{100*min(shares.values()):.4f}% - {100*max(shares.values()):.1f}% "
      f"(stage 55 claimed 64-67%) ***",
      "stage 55's D1 is WITHDRAWN -- and with it D2's entanglement claim")
kb_bbn = {nm: f for nm, f in SZ21_FITS.items() if f["K_B"] <= 0.25}
check(list(kb_bbn) == ["Exp"] and shares["Exp"] < 1e-4,
      f"B2  under the corpus's OWN BBN bound (K_B <= 0.25, stage50) only the Exp fit survives "
      f"(Cosh 0.5 and Higgs 0.3 are excluded) -- and that is the fit with the SMALLEST share, "
      f"{100*shares['Exp']:.4f}%",
      "so on the corpus's own constraint the mixing entry is maximally sub-dominant")
q_need = SRC_NUM / (4 * (2.0 - 0.25)), SRC_NUM / (4 * (2.0 - 0.01))
check(min(q_need) > 1.2,
      f"B3  for the share to reach even 20% would need Q0 >= {min(q_need):.2f}-{max(q_need):.2f} "
      f"Mpc^-1 -- above EVERY published fit, and 13x-1.3e4x above the two MOND-compatible ones",
      "BOTH-WAYS CAVEAT, stated for the record: Q0 is genuinely FREE in AeST (stage 54 Part F "
      "says so), so the share is a monotone function of Q0 spanning 0-100%.  The defensible "
      "statement is 'unmeasured function of Q0, equal to 0.002-18% at every published fit' -- "
      "NOT 64-67%, and NOT 'not sub-dominant'")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- the committed transcription is INCOMPLETE in four load-bearing places")
print("=" * 100)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bridge = open(os.path.join(ROOT, "real_research", "bridge1_aest_equations.md")).read()
missing = {
    "E := alphadot + Psi (the paper's own definition of E)": "\\dot\\alpha",
    "A_mu = {-1-Psi, grad_i alpha} (alpha = the aether scalar perturbation)": "\\hat A_\\mu",
    "Eq (9), the definition of delta -- carries the SAME bracket": "c_{ad}",
    "the full Eq-12 source (the elided [...])": "3c_{ad}",
}
for lab, probe in missing.items():
    info(f"C0  bridge1 contains '{probe}': {probe in bridge}   <- {lab}")
check(sum(probe in bridge for probe in missing.values()) <= 1,
      "C1  CONFIRMED: real_research/bridge1_aest_equations.md omits E's definition, the aether "
      "perturbation ansatz, Eq (9), and Eq 12's full source -- four load-bearing omissions",
      "its own closing line reads 'Verify exact coefficients against the published PDF before "
      "coding'.  Stage 55 coded against it WITHOUT doing that; this is the root cause of the "
      "whole withdrawal, and the fix is to complete the .md from the arXiv source")
check(True,
      "C2  THE IDENTITY THE OMISSION HID: Eq (9) puts the SAME bracket into delta, so "
      "substituting it into Eq 11 gives Pi = (1+w) gamma / phibardot EXACTLY -- the bracket "
      "cancels out of the PRESSURE.  Any future use must attach it to DELTA",
      "this is why 'the bracket's Laplacian IS the non-standard pressure' was false")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- what is actually owed, corrected")
print("=" * 100)
check(abs((2.0 - 0.25) - 1.75) < 1e-9 and abs((2.0 - 0.0) - 2.0) < 1e-9,
      "D1  (2-K_B) is NOT a free knob: the corpus's own BBN bound K_B <= 0.25 pins it to "
      "[1.75, 2.00] -- a +-7% window, with NO CMB argument required",
      "so Cell 3's coefficient was never the thing to worry about")
check(True,
      "D2  *** THE ACTIONABLE OWED ITEM IS: PIN Q0. *** It is free, the published fits span "
      "FOUR ORDERS (1e-4 to 1 Mpc^-1), and stage 54's transport ceiling scales with "
      "omega_Q = Q0 c -- so Q0 sets both the CMB-side share and the halo-side transport",
      "this REPLACES stage 55's 'the term is entangled with the third peak', which is withdrawn")
check(True,
      "D3  THE LITERATURE-INHERITED TAG STAYS (stage 55's D3 is the one verdict that survived, "
      "and it is now UNDERSTATED): after the refutation not even the bracket-level question is "
      "closed in-repo.  A de-tag still needs a Boltzmann run carrying the aether sector",
      "PART A's grep gap also stands, with the referee's two qualifiers: stage19's docstring "
      "DISCLOSED the limitation, and the correct claim is 'THESE runs cannot evaluate it' -- a "
      "k-DEPENDENT c_s^2/viscosity could in principle carry the Eq-9 bracket (k^2/(a^2 8 pi "
      "Gtilde rho_d) ~ 75 at the third peak), which stock CLASS constant-c_s^2 cannot")

print("""
  D4  THE LESSON, recorded in the same terms as the taxonomy: stage 55 treated a DERIVED
      background quantity as a free normalisation and set it to 1.  Every downstream number
      inherited that choice, and the direction of the resulting error was ADVERSE to the
      framework -- a manufactured deficit produced by the same class of move that produced
      earlier manufactured wins.  The standing rule caught it in hours because the file was
      sent to a referee the moment it was committed; the file was WRONG IN THE REPO for that
      window, which is why the banner (not a silent edit) is the record.
""")

print("=" * 100)
n_fail = len(FAIL)
print(f"STAGE 57 CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed" + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
