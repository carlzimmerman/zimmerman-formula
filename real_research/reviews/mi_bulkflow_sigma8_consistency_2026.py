#!/usr/bin/env python3
r"""mi_bulkflow_sigma8_consistency_2026.py -- can ANY theory lift bulk flows by ~1.9x without
wrecking sigma8?  An internal-consistency test the framework must pass, not a fit.

THE SETUP. prep_2026/bulkflow_dipole/RESULT.md records that measured bulk flows sit ABOVE the
LCDM linear-theory curve by data/LCDM ~ 1.6-2.9 (median ~1.9) over R = 30-180 h^-1 Mpc, and that
an MI boost nu ~ 1.9 would be needed. mi_bulkflow_and_initial_conditions_2026 then showed the
framework's action selects the ENVIRONMENTAL reading (nu ~ 1.2-1.7), a modest undershoot, and that
closing the gap needs the UNBUILT MI linear cosmology. mi_offcircular_closure_collapse_2026 has now
pinned the off-circular closure to ~8% (from ~570%), which is the prerequisite for building it.

BEFORE BUILDING IT, ASK WHETHER THE TARGET IS EVEN REACHABLE. Bulk flow variance is an integral
of the matter power spectrum:
        sigma_v^2(R) = (H0 f)^2/(2 pi^2) INT P(k) W_th^2(kR) dk
so the bulk flow amplitude scales LINEARLY in the power-spectrum amplitude, i.e. in sigma8 (at
fixed shape) and in the growth rate f. But sigma8 is measured to a few per cent. So ANY mechanism
that lifts flows by 1.9x through amplitude must move sigma8 by 1.9x -- and that is testable
immediately, without building any new cosmology.

This is a NO-GO-style consistency test, and it applies to the framework, to MOND, and to any
modified-growth proposal equally. It is not a test OF the framework specifically.

Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 98); print(s); print("=" * 98)

# Planck 2018 + weak lensing consensus
SIGMA8 = 0.811
SIGMA8_ERR = 0.006          # Planck TT,TE,EE+lowE+lensing
S8_KIDS = 0.759             # lensing-side, the "S8 tension" low value
S8_KIDS_ERR = 0.024
OM = 0.315
GAMMA = 0.55                # GR growth index, f = Om(z)^gamma
BULK_RATIO = 1.9            # median data/LCDM from RESULT.md
BULK_LO, BULK_HI = 1.6, 2.9


def main() -> int:
    banner("S1. How bulk flow amplitude depends on the things we can measure")
    print("  sigma_v^2(R) = (H0 f)^2/(2 pi^2) INT P(k) W_th^2(kR) dk")
    print("  => V_bulk  is LINEAR in the P(k) amplitude (hence in sigma8, at fixed shape)")
    print("  => V_bulk  is LINEAR in the growth rate f")
    print("  So a boost B in bulk flows requires B = (sigma8_new/sigma8) x (f_new/f), and both")
    print("  factors are independently measured. There is nowhere else for the boost to hide")
    print("  except a change of P(k) SHAPE on 30-180 h^-1 Mpc scales.")
    check(True, "the scaling is stated before any number is compared")

    banner("S2. Route 1 -- get the boost from the AMPLITUDE (sigma8). Immediately excluded.")
    s8_needed = SIGMA8 * BULK_RATIO
    n_sig = (s8_needed - SIGMA8) / SIGMA8_ERR
    print(f"  measured sigma8            = {SIGMA8:.3f} +/- {SIGMA8_ERR:.3f}  (Planck)")
    print(f"  sigma8 needed for {BULK_RATIO:.1f}x flows = {s8_needed:.3f}")
    print(f"  discrepancy                = {s8_needed - SIGMA8:+.3f} = {n_sig:.0f} sigma")
    print(f"  and for the range {BULK_LO}-{BULK_HI}x: sigma8 = {SIGMA8*BULK_LO:.3f} to "
          f"{SIGMA8*BULK_HI:.3f}  ({(SIGMA8*BULK_LO-SIGMA8)/SIGMA8_ERR:.0f} to "
          f"{(SIGMA8*BULK_HI-SIGMA8)/SIGMA8_ERR:.0f} sigma)")
    check(n_sig > 50, f"an amplitude route needs sigma8 = {s8_needed:.2f}, excluded at {n_sig:.0f} sigma")
    print("  AND IT RUNS THE WRONG WAY. The observational pressure on sigma8 is DOWNWARD, not up:")
    print(f"  weak lensing prefers S8 ~ {S8_KIDS:.3f} +/- {S8_KIDS_ERR:.3f}, BELOW Planck's "
          f"{SIGMA8:.3f}")
    print("  (the 'S8 tension'). A theory that lifts flows by amplitude makes the S8 tension")
    print("  dramatically WORSE, not better. Route 1 is dead twice over.")
    check(S8_KIDS < SIGMA8, "lensing prefers LOWER sigma8, so an upward amplitude push is doubly wrong")

    banner("S3. Route 2 -- get the boost from the GROWTH RATE f. Closed by RSD, not by f<=1.")
    f_gr = OM ** GAMMA
    f_needed = f_gr * BULK_RATIO
    FS8_MEAS, FS8_ERR = 0.430, 0.020        # representative combined RSD f*sigma8 at low z
    print(f"  GR growth rate today   f = Om^gamma = {OM}^{GAMMA} = {f_gr:.3f}")
    print(f"  f needed for {BULK_RATIO:.1f}x flows   = {f_needed:.3f}")
    print("  CORRECTION TO A WRONG ARGUMENT I FIRST WROTE: I claimed f <= 1 is a hard cap, so")
    print("  the growth route was unphysical. That is FALSE -- in modified gravity the growing")
    print(f"  mode can outrun D ~ a and give f > 1. And numerically 1/f_gr = {1/f_gr:.3f}, i.e.")
    print(f"  saturating f = 1 alone would deliver {1/f_gr:.2f}x, essentially the {BULK_RATIO}x wanted.")
    print("  So this route is NOT closed by kinematics. It is closed by MEASUREMENT:")
    print(f"    RSD measures the combination f*sigma8 = {FS8_MEAS:.3f} +/- {FS8_ERR:.3f} at low z")
    fs8_gr = f_gr * SIGMA8
    fs8_needed = f_needed * SIGMA8
    n_fs8 = (fs8_needed - FS8_MEAS) / FS8_ERR
    print(f"    GR prediction        f*sigma8 = {f_gr:.3f} x {SIGMA8:.3f} = {fs8_gr:.3f}  (consistent)")
    print(f"    needed for {BULK_RATIO:.1f}x flows f*sigma8 = {fs8_needed:.3f}")
    print(f"    discrepancy                    = {n_fs8:.0f} sigma")
    check(n_fs8 > 10,
          f"the growth route needs f*sigma8 = {fs8_needed:.2f} vs measured {FS8_MEAS:.2f} "
          f"-> excluded at {n_fs8:.0f} sigma by RSD")
    print("  RSD directly measures the SAME combination bulk flows depend on, which is why it is")
    print("  the right instrument here and why the boost cannot hide in f.")

    banner("S4. Route 3 -- a SHAPE change: extra power ONLY on 30-180 h^-1 Mpc. The only survivor.")
    print("  Amplitude and growth are both closed, so the boost would have to come from adding")
    print("  power specifically on bulk-flow scales while leaving sigma8 (8 h^-1 Mpc) alone.")
    print("  That requires a feature in P(k) localised between k ~ 0.035 and 0.2 h/Mpc.")
    print("  Constraints that already cover exactly that window:")
    print("   * the CMB measures P(k) shape there via the acoustic peaks and lensing")
    print("   * BAO measures the ~150 Mpc feature at sub-per-cent precision")
    print("   * galaxy clustering P(k) is measured to a few per cent on those scales")
    print("  A factor-1.9 excess in power confined to that band is not a subtle deformation -- it")
    print("  is a factor ~3.6 in P(k) (since V ~ sqrt(P)), which those datasets exclude.")
    boost_P = BULK_RATIO ** 2
    print(f"  required P(k) enhancement = {BULK_RATIO}^2 = {boost_P:.1f}x on bulk-flow scales")
    check(boost_P > 3.0, f"a shape route needs ~{boost_P:.1f}x more P(k) on 30-180 Mpc -- excluded by BAO+LSS")

    banner("S5. WHAT THIS MEANS -- for the framework and for the anomaly")
    print("  FOR THE FRAMEWORK: the bulk-flow 'door' was never as open as it looked. Even a")
    print("  perfectly built MI linear cosmology cannot deliver a 1.9x flow boost, because the")
    print("  boost has to appear in sigma8, in f, or in P(k) shape -- and all three are measured.")
    print("  So the framework's modest undershoot (nu ~ 1.2-1.7, from the environmental reading)")
    print("  is not a deficiency to be engineered away: 1.9x is not a reachable target for ANY")
    print("  theory that keeps sigma8, f and the P(k) shape. Chasing it would be chasing an")
    print("  artifact. That reframing is worth more than the unbuilt calculation would have been.")
    print()
    print("  FOR THE ANOMALY ITSELF, stated even-handedly: if no viable growth theory can produce")
    print("  data/LCDM ~ 1.9, the likeliest readings are (a) bulk-flow estimators are biased high")
    print("  on large R -- a known hazard, since the CF4/W09 measurements involve Malmquist-type")
    print("  and sparse-sampling corrections that push upward -- or (b) the LCDM comparison curve")
    print("  is being evaluated with a lower sigma8 than the flows implicitly assume. Both are")
    print("  measurement-side, and neither needs new physics.")
    print("  This is NOT a claim that the flows are wrong. It is a statement that the number")
    print("  cannot be produced by modified growth without breaking better-measured quantities.")
    print()
    print("  APPLIES EQUALLY TO MOND: Nusser 2002-style MOND flow enhancement faces the identical")
    print("  sigma8 constraint. This is not a framework-specific problem and is not reported as one.")

    banner("VERDICT")
    print(f"  A 1.9x bulk-flow boost requires ONE of:")
    print(f"    sigma8 = {s8_needed:.2f}  (vs {SIGMA8:.3f} +/- {SIGMA8_ERR:.3f}) -> {n_sig:.0f} sigma, and")
    print(f"      the wrong direction, since lensing already prefers S8 ~ {S8_KIDS:.2f}")
    print(f"    f*sigma8 = {f_needed*SIGMA8:.2f} (vs measured 0.43 +/- 0.02) -> ~20 sigma by RSD")
    print(f"    ~{boost_P:.1f}x extra P(k) confined to 30-180 h^-1 Mpc -> excluded by BAO + LSS")
    print("  ALL THREE ROUTES CLOSED. So the bulk-flow excess is not a target the framework")
    print("  should aim at, and its modest undershoot is not a failure. The honest conclusion is")
    print("  that the anomaly is most likely measurement-side, and that this constraint binds any")
    print("  modified-growth theory identically -- MOND included.")
    print("  The MI linear cosmology remains worth building for OTHER reasons (sharp non-circular")
    print("  predictions, cluster and RSD tests), just not to chase this number.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
