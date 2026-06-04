#!/usr/bin/env python3
"""
SYNTHESIS: the weight of DIRECT high-z rotation-curve evidence disfavors a0 ∝ E(z); MUSE-DARK III dissents.
=========================================================================================================
Carl asked: is the Big Wheel the only z~3 measurement? No. Collecting every real z>1 constraint on the MOND
acceleration scale a0(z), the DIRECT rotation-curve evidence consistently DISFAVORS the framework's strong
rise a0 = cH(z)/Z = a0(0) E(z); the lone strong-rising claim (MUSE-DARK III) is an INDIRECT RAR fit. The
framework predicts a0/a0(0) = E(z): 3.0x at z=2, 4.6x at z=2.9, 5.0x at z=3.25.

THE LEDGER (each with its method and what it says about a0(z)):

  Big Wheel, z=3.25 (Nature Astron. 2025) -- DIRECT single disk.
    V_rot=280 km/s at R_eff (g~2.2 a0_local: HIGH-ACCELERATION regime, so an UPPER BOUND not a clean deep-MOND
    measurement). a0_eff = V^4/(G M_bar) ~ 1e-10; robust gas-only ceiling 2.6x local. => EXCLUDES the predicted
    5x. (project_highz_bigwheel_a0.py)

  Milgrom 2017 (arXiv:1703.06110) on Genzel+2017 RC -- DIRECT, ~z~2.
    The high-z disks sit at g(R_1/2) = (3-11) a0 (high-acceleration), and the data "all but EXCLUDE a value of
    the MOND constant of ~4 a0 at z~2", explicitly eliminating a0 ∝ (1+z)^{3/2}. Standard (local) a0 broadly
    reproduces the declining curves. => a strong rise is EXCLUDED at z~2; framework's 3.0x is borderline.

  RC100 / Nestor-Shachar 2023; Genzel/Lang 2017 -- DIRECT, z=0.6-2.5, ~100 disks.
    Massive high-z disks are baryon-dominated with DECLINING outer rotation curves (high-acceleration). =>
    consistent with ~local a0 in the Newtonian regime; no evidence for a strongly risen a0 (upper bounds).

  KMOS3D / Ubler 2017; baryonic TF to z~2.5 -- DIRECT-ish (kinematics).
    The BARYONIC TF zero-point does NOT strongly evolve (only the stellar TF does). The BTFR zero-point IS
    G a0, so a roughly constant baryonic-TF zero-point => a0 roughly CONSTANT, not x5.

  Wu & Kroupa 2015 (arXiv:0809.2790) -- TF-as-MOND test to z~1.2.
    Both a0 ∝ H and a0 ∝ sqrt(Lambda) formally excluded within errors; with systematics, MARGINALLY FAVORS
    a0 ∝ sqrt(Lambda) (CONSTANT / event-horizon), not a0 ∝ H (rising).

  MUSE-DARK III 2026 (A&A) -- INDIRECT RAR fit, intermediate z (0.3-1.4) -- THE DISSENTER.
    a0(z)=1.0+1.59z rises, even faster than H(z). The one dataset favoring a strong rise; an aggregate RAR fit
    on lensing+dynamics, not direct outer rotation curves.

HONEST READING: the strong rise a0 ∝ E(z) (the framework's specific bet) is DISFAVORED by the DIRECT high-z
rotation-curve evidence (Big Wheel + Milgrom/Genzel + RC100 + the ~constant baryonic TF zero-point), and the
single supporting result is an indirect intermediate-z RAR fit. A MILD rise (~1.5-2x by z~1) is not excluded
by the high-z upper bounds; a 5x rise to z~3 is. So the framework is squeezed toward "constant or mildly
rising", and its specific cH(z)/Z = E(z) law is in real, multiply-corroborated tension. Caveat both ways: the
direct high-z disks are high-acceleration (upper bounds, not precision a0); MUSE-DARK III could carry RAR-fit
systematics. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def main():
    print("#"*92)
    print("# SYNTHESIS -- high-z a0(z): direct rotation curves disfavor the x5 rise; MUSE-DARK III dissents")
    print("#"*92 + "\n")

    print("="*92); print("FRAMEWORK PREDICTION a0(z)/a0(0) = E(z), and what each real probe finds"); print("="*92)
    for z in (1.0, 2.0, 2.9, 3.25):
        print(f"  z={z:>4}:  predicted a0/a0(0) = E(z) = {E(z):.2f}x")
    print()
    rows = [
        ("Big Wheel z=3.25",     "DIRECT disk",      "a0 <~ 2.6x (ceiling); ~1x",  "EXCLUDES 5x"),
        ("Milgrom/Genzel z~2",   "DIRECT RC",        "g=(3-11)a0; excl ~4x",       "EXCLUDES (1+z)^1.5"),
        ("RC100 z=0.6-2.5",      "DIRECT, ~100",     "baryon-dom, declining RCs",  "~local a0 (upper bnds)"),
        ("KMOS3D baryonic TF",   "kinematics",       "BTFR zero-point ~constant",  "a0 ~ CONSTANT"),
        ("Wu&Kroupa z<1.2",      "TF-MOND",          "marg. favors a0~sqrt(Lam)",  "CONSTANT favored"),
        ("MUSE-DARK III z<1.4",  "INDIRECT RAR fit", "a0=1.0+1.59z (rising)",      "RISING (dissenter)"),
    ]
    print(f"  {'probe':22}{'method':18}{'finding':30}{'on a0(z)':>22}")
    for r in rows:
        print(f"  {r[0]:22}{r[1]:18}{r[2]:30}{r[3]:>22}")
    print()

    print("="*92); print("HOW THE BIG WHEEL WAS MEASURED -- the honest caveat Carl flagged"); print("="*92)
    print("""  V_rot=280 km/s is the inclination-corrected MAXIMUM, measured at 1 R_eff = 9.6 kpc. There g_obs = V^2/R
  ~ 2.6e-10 ~ 2.2 a0_local -- the HIGH-ACCELERATION (near-Newtonian) regime, NOT deep MOND. So the Big Wheel
  does not cleanly MEASURE a low a0; it BOUNDS it from above (a risen a0 would over-boost the baryons and
  demand V >~ 374 km/s; only 280 is seen). Same regime as ALL the massive high-z disks (Milgrom: g=3-11 a0).
  => the right statement is "a0 <~ 2-3x local at z~3 (5x excluded)", corroborated by the whole direct sample,
  not "a0 = 1e-10 measured". The conclusion (strong rise disfavored) is robust; the precision is not.\n""")

    print("="*92); print("VERDICT"); print("="*92)
    print(f"""  No -- the Big Wheel is not the only z>1 probe, and the others CORROBORATE it. Every DIRECT high-z
  rotation-curve constraint (Big Wheel z=3.25; Milgrom on Genzel z~2; RC100; the ~constant baryonic-TF zero-
  point) disfavors the framework's strong a0 ∝ E(z) rise: massive high-z disks are baryon-dominated, high-
  acceleration systems whose rotation is reproduced with ~local a0, and a ~4-5x rise (predicted E(2)={E(2):.1f}x,
  E(3.25)={E(3.25):.1f}x) is excluded/disfavored. The ONE result favoring a strong rise -- MUSE-DARK III -- is an
  indirect intermediate-z RAR fit. So the central bet is squeezed toward CONSTANT or at most MILD rise; the
  specific cH(z)/Z = E(z) law is in real, multiply-corroborated observational tension. Honest both ways: the
  direct disks give upper bounds (not precision a0), and MUSE could carry fit systematics -- but the WEIGHT of
  direct evidence is against the x5 rise. The clean settler remains a deep-MOND (low-acceleration, OUTER)
  rotation curve of a normal z~3 disk -- not a baryon-dominated monster sitting at 3-11 a0.""")
    print("="*92)


if __name__ == "__main__":
    main()
