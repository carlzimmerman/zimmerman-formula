#!/usr/bin/env python3
"""
Scrutinizing EVERY falsifiable prediction in the repo for accuracy.
==================================================================

Carl asked: look at all the falsifiable predictions and scrutinize them. Source:
research/PENDING_MEASUREMENTS.md (the curated 'awaiting data' list). For each I
ask four questions:
  (D) DISTINCTIVE -- does it test Z2 specifically, or is it a LCDM/MOND default
      that many theories predict?
  (F) FORWARD -- a genuine prediction of an UNmeasured quantity, or a RETRODICTION
      of an already-measured one dressed as a prediction?
  (Z) Z-DEPENDENT -- does the predicted value move if the fitted Z moves?
  (M) MOVING TARGET -- has the 'prediction' been changed after data ruled out an
      earlier version?

Only (D)+(F)+not-(M) predictions carry real evidential weight for Z2.

Pure stdlib. Run:  python reviews/falsifiable_predictions_scorecard.py
"""

import math

ALPHA = 1 / 137.035999
Z2 = 32 * math.pi / 3
Z = math.sqrt(Z2)


def line(tag, name, predicted, measured_or_test, verdict):
    print(f"  [{tag}] {name}")
    print(f"        predicted: {predicted}")
    print(f"        reality:   {measured_or_test}")
    print(f"        verdict:   {verdict}\n")


def main():
    print("=" * 80)
    print("TIER-1 'falsifiable predictions' (PENDING_MEASUREMENTS.md), scrutinized")
    print("=" * 80 + "\n")

    line("NUMEROLOGY/MOVING", "1. LiteBIRD: r (tensor-scalar) = 1/(2Z^2)",
         f"{1/(2*Z2):.4f}",
         "moving target: 8*alpha=0.058 RULED OUT -> 1/(2Z^2)=0.015 adopted; "
         "App.D gives 8/Z^2=0.24. Repo says 'NO VALID DERIVATION'.",
         "Z-DEPENDENT, retrofitted. Forward-testable but ~0 weight (tensor_scalar_r_audit.py).")

    sm_run = "SM runs sin^2 UP at low Q^2 to ~0.236 (Qweak-confirmed running)"
    line("NUMEROLOGY/LIKELY-WRONG", "2. MOLLER: sin^2(theta_W) low-Q^2 = 3/13",
         f"{3/13:.5f}  (= 3/13, the numerology value ~ the M_Z-scale number)",
         sm_run,
         "ignores the ESTABLISHED low-Q^2 running. SM predicts ~0.236 at MOLLER; "
         "3/13=0.2308 is ~0.005 low = ~19sigma off. LIKELY FALSIFIED by MOLLER.")

    line("RETRODICTION", "3. JUNO: Delta m^2_21 = 7.5e-5 eV^2",
         "7.5e-5 eV^2",
         "ALREADY measured (KamLAND/solar): 7.5e-5. JUNO only sharpens it.",
         "predicting the known central value = retrodiction, not a forward prediction.")

    line("RETRODICTION/FIT", "4. Euclid: Omega_Lambda = 13/19",
         f"{13/19:.7f}  (quoted to 7 digits)",
         "measured 0.685 +/- 0.007 (Planck). Multiple repo formulas: 13/19, "
         "3Z/(8+3Z), sqrt(3pi/2)/(1+...).",
         "fit to a measured value; precision theatre (7 digits vs 1% error); "
         "multiple incompatible formulas = fitting.")

    line("LCDM-DEFAULT/TENSION", "5,7. DESI Y5 / Roman: w0 = -1.000",
         "-1.000",
         "w=-1 IS the LCDM cosmological-constant default (every LCDM model). "
         "DESI 2024 actually hints w0 != -1 (evolving DE) at ~2-3sigma.",
         "not distinctive (LCDM predicts it too), and in mild TENSION with current data.")

    line("RETRODICTION/FIT", "8. CMB-S4: Omega_m = 6/19",
         f"{6/19:.5f}",
         "measured ~0.315. Note 6/19 + 13/19 = 1 by construction (flatness).",
         "two fits (6/19, 13/19) to two measured numbers, forced to sum to 1. Numerology.")

    line("REAL-TEST / NOT Z-DISTINCTIVE", "6. Gaia DR4: MOND in wide binaries",
         "MOND boost present at a < a0",
         "CONTESTED now: Chae (signal) vs Banik/Pittordis (Newtonian).",
         "GENUINE falsifiable test -- but of MOND-vs-Newton (the premise), Z-INDEPENDENT, "
         "shared with all MOND. If Newtonian wins, the whole MOND program is hit.")

    line("THE SURVIVOR (underweighted here)", "*. JWST z>10: a0(z) = a0(0) E(z)",
         "v_flat larger by E(z)^1/4 ~ 2.2-2.4x at z=12-14",
         "the only DISTINCTIVE, Z-INDEPENDENT, pre-registered forward prediction.",
         "REAL. Oddly minor in the official list (which features the WALLABY z~0 a0=1.2e-10 "
         "RETRODICTION instead). This is the one to stake the framework on.")

    print("=" * 80)
    print("TALLY -- what the 'falsifiable predictions' actually are")
    print("=" * 80)
    rows = [
        ("Distinctive + forward + Z-independent (REAL weight)", "a0(z)~E(z) [+ maybe wide-binary MOND-premise]", "~1-2"),
        ("LCDM/MOND defaults (falsifiable but NOT distinctive)", "w0=-1, WIMP/axion nulls, RAR/mu(x)", "several"),
        ("Retrodictions of already-measured values", "Delta m^2_21, Omega_m=6/19, Omega_L=13/19, a0=1.2e-10", "several"),
        ("Numerology / moving targets", "r=1/(2Z^2), sin^2=3/13", "2"),
    ]
    for cat, ex, n in rows:
        print(f"   [{n:>8}] {cat}")
        print(f"            e.g. {ex}")
    print()
    print("=" * 80)
    print("HONEST HEADLINE")
    print("=" * 80)
    print("  Of the curated 'falsifiable predictions', the large majority are either")
    print("  RETRODICTIONS (fitting Omega_m, Omega_L, Delta m^2_21, a0 -- all already")
    print("  measured), LCDM/MOND DEFAULTS (w=-1, no-WIMP -- predicted by many theories),")
    print("  or NUMEROLOGY (r=1/(2Z^2), 3/13 -- one already a moving target, one likely")
    print("  falsified by the low-Q^2 running MOLLER will see).")
    print()
    print("  The genuinely DISTINCTIVE, FORWARD, Z-INDEPENDENT prediction is essentially")
    print("  ONE: a0(z) ~ E(z) at z>10. Everything that can actually move the needle FOR")
    print("  Z2 rests on that single test. The honest move is to stop padding the list")
    print("  with retrodictions and defaults, and put the whole weight on a0(z) -- the")
    print("  one prediction that is distinctive, cannot be retrofitted, and is testable.")
    print()
    print("  (Good practice to keep: the cryptographic pre-registration is genuinely")
    print("  sound -- it just timestamps fits as well as the real prediction. Lock a0(z).)")


if __name__ == "__main__":
    main()
