#!/usr/bin/env python3
"""
What a SUB-E(z) rise implies for the theory: a two-horizon geometric-mean law that keeps Z ~ O(2pi).
====================================================================================================
The high-z data disfavor the framework's clean a0 ∝ cH(z)/Z = E(z) (a x5 rise to z~3) but permit a MILDER
rise (and the qualitative "a0 rises" survives). This file asks the theory question: if a0 rises slower than
E(z), what does that do to the cH/Z derivation and the Z coefficient? The answer is clean and (mildly)
encouraging for the framework -- the mild-rise law has a natural home and does NOT wreck the coefficient.

PARAMETRISE a0(z) = a0(0) E(z)^p.  The framework family a0 = (c/2) sqrt(G rho) fixes p by WHICH density sources
a0 (rho ~ H^2 for the total; constant for Lambda):
    p = 1  : rho = rho_total  ->  a0 = cH(z)/Z          (apparent / Hubble horizon)   -- the framework's bet
    p = 0  : rho = rho_Lambda ->  a0 = cH0 sqrt(OL)/Z    (event / de Sitter horizon)   -- the "constant" reading
    p = 1/2: GEOMETRIC MEAN   ->  a0 = c sqrt(H(z) H_L)/Z' (H_L = H0 sqrt(OL))          -- a0 set by BOTH horizons

THE DATA DO NOT PIN p (the implied p scatters from ~0.1 (Big Wheel) to ~2.9 (MUSE low-z): systematics-
dominated). But the p=1/2 geometric-mean law threads the high-z constraints far better than p=1 -- and,
crucially, it keeps the dictionary coefficient O(2pi): Z' = Z * OL^{1/4} ~ 5.3 (vs Z = 2 sqrt(8pi/3) ~ 5.79).
So a mild rise needs NOT a fine-tuned or drifting coefficient -- only a change of FUNCTIONAL FORM from cH to
c sqrt(H H_L), i.e. a0 sourced by both the (rising) apparent-horizon scale and the (constant) event-horizon
floor. That is EXACTLY the structure the 2025 "many temperatures of de Sitter" program supplies (Hawking/pode
temperature ~ H rising; a constant de Sitter floor) -- so the geometric mean is theory-motivated, not just a
data patch.

HONEST FRAMING: this is a refinement UNDER PRESSURE -- the clean, distinctive a0=cH/Z is disfavored, and the
two-horizon form is messier and post-hoc (and p=1/2 is the symmetric special case; the data, if they could
pin it, would set the weighting). What it buys: the qualitative apparent-horizon bet (a0 rises) survives, the
coefficient stays O(2pi), and the rate becomes falsifiable -- p=1 predicts a0(z=3)~4.6x, p=1/2 ~2.1x, p=0 ~1x,
so a clean deep-MOND z~3 disk separates them cleanly. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
A0 = 1.2          # local, 1e-10
Z1 = 2*np.sqrt(8*np.pi/3)


def main():
    print("#"*92)
    print("# A SUB-E(z) RISE -> a two-horizon geometric-mean law, with Z still O(2pi)")
    print("#"*92 + "\n")

    print("="*92); print("(1) THE DATA DO NOT PIN THE POWER p in a0(z)=a0(0) E(z)^p"); print("="*92)
    print(f"  {'probe':18}{'z':>5}{'a0':>7}{'implied p':>11}")
    for name, z, a0 in [("MUSE", 0.33, 1.99), ("MUSE", 1.0, 2.38), ("MUSE", 1.44, 2.71),
                        ("Big Wheel best", 3.25, 1.5), ("Big Wheel ceil", 3.25, 2.6)]:
        print(f"  {name:18}{z:>5.2f}{a0:>7.2f}{np.log(a0/A0)/np.log(E(z)):>11.2f}")
    print("  => p ranges ~0.1-2.9: systematics-dominated, no clean value. The theory question is which p is NATURAL.\n")

    print("="*92); print("(2) THE FRAMEWORK FAMILY -- p is set by which density/horizon sources a0"); print("="*92)
    print(f"  {'law':38}{'horizon':22}{'p':>4}{'a0(1)':>8}{'a0(2)':>8}{'a0(3)':>8}")
    for law, hor, p in [("a0 = cH(z)/Z", "apparent (Hubble)", 1.0),
                        ("a0 = c sqrt(H H_L)/Z'", "BOTH (geom mean)", 0.5),
                        ("a0 = cH0 sqrt(OL)/Z", "event (de Sitter)", 0.0)]:
        print(f"  {law:38}{hor:22}{p:>4.1f}{A0*E(1)**p:>8.2f}{A0*E(2)**p:>8.2f}{A0*E(3)**p:>8.2f}")
    print("  (a0 in 1e-10.) p=1 predicts a0(z=3)=5.5; p=0.5 predicts 2.6 -- and the high-z disks cap a0 <~ 2.6.\n")

    print("="*92); print("(3) THE COEFFICIENT STAYS O(2pi) -- a mild rise does NOT wreck the dictionary"); print("="*92)
    Zp = Z1*OL**0.25
    print(f"  p=1   a0=cH/Z           : Z  = 2 sqrt(8pi/3)      = {Z1:.2f}")
    print(f"  p=0.5 a0=c sqrt(H H_L)/Z': Z' = Z * OL^(1/4)       = {Zp:.2f}   (barely moved, still O(2pi))")
    print(f"  => the geometric-mean law matches a0(0) with a CONSTANT coefficient ~5.3; no fine-tuning, no drift.")
    print(f"     Only the FUNCTIONAL FORM changes: a0 sourced by both the rising apparent horizon (cH) and the")
    print(f"     constant event-horizon floor (cH_L). H_L/H0 = sqrt(OL) = {np.sqrt(OL):.3f}.\n")

    print("="*92); print("(4) WHY THIS IS THEORY-MOTIVATED, NOT JUST A PATCH"); print("="*92)
    print("""  The 2025 "many temperatures of de Sitter" (Rahman-Susskind) gives de Sitter a HIERARCHY of temperatures,
  including a Hawking/pode temperature ~ H (cosmic, rising with z) and constant-scale pieces. If a0 is set by a
  COMBINATION (geometric mean) of a rising apparent-horizon temperature and a constant event-horizon floor,
  then a0 = c sqrt(H H_L)/Z' (p=1/2) drops out -- the SAME structure that earlier resolved the interpolation's
  shape (project_manytemp_broadening.py). So one structure (many temperatures) addresses BOTH the interpolation
  shape AND a milder-than-E(z) rate. That is a non-trivial consistency, not a fresh free parameter.\n""")

    print("="*92); print("VERDICT -- honest"); print("="*92)
    print(f"""  A sub-E(z) rise is a refinement UNDER PRESSURE, reported as such: the framework's clean, distinctive
  a0 = cH(z)/Z (p=1, a0(z=3)~4.6-5.5x) is disfavored by the high-z disks. But the implied theory move is mild,
  not fatal: a two-horizon geometric-mean law a0 = c sqrt(H(z) H_L)/Z' (p=1/2) (i) threads the high-z cap
  (a0(z=3)~2.1-2.6x), (ii) keeps a CONSTANT coefficient Z' ~ 5.3 = O(2pi), and (iii) is the SAME many-
  temperatures structure that fixed the interpolation shape -- so it is theory-motivated. Costs: it abandons
  the clean "a0 = apparent-horizon surface gravity" headline for a messier two-horizon form; p=1/2 is the
  symmetric special case (the data cannot yet set the weighting); and nothing here is data-REQUIRED -- the data
  merely permit it. Falsifiable: a clean deep-MOND z~3 disk gives a0(z=3) = 4.6x (p=1) vs 2.1x (p=1/2) vs 1x
  (p=0). The qualitative apparent-horizon bet survives; the specific cH/Z law most likely does not.""")
    print("="*92)


if __name__ == "__main__":
    main()
