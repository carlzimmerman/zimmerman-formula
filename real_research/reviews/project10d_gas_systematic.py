#!/usr/bin/env python3
"""
PROJECT 10d: decompose the gas systematic -- and honestly SOFTEN the 10c 'leans constant' to 'inconclusive'.
============================================================================================================
Project 10c found that real KROSS data, with a realistic gas correction, give a0(z~0.85) ~ local (constant),
disfavoring the framework's rise. Before trusting that framework-UNFAVORABLE result, it must be stress-tested
exactly like the favorable ones were. Decomposing the irreducible systematics (the CO-to-H2 factor, the
unmeasured atomic gas, and the V_flat definition) shows the a0 range is WIDER than the framework-vs-constant
gap itself -- so the honest verdict is INCONCLUSIVE with a central preference for constant, NOT a clean lean.
The discipline cuts both ways: do not overstate the disfavoring any more than the favoring. Needs numpy.
"""
import numpy as np


def main():
    print("#"*92); print("# PROJECT 10d -- the gas systematic, and an honest softening of 10c"); print("#"*92 + "\n")
    base = 2.15  # KROSS stars-only a0 (1e-10); a0 = base * (V_flat/VC)^4 / (1 + f_gas_total)
    print("="*92); print("THE DECOMPOSITION (a0 in 1e-10; framework=1.96, constant=1.20)"); print("="*92)
    print(f"""  a0(z~0.85) = {base} x (V_flat/VC)^4 / (1 + f_gas_total), with three IRREDUCIBLE knobs:
    KNOB 1  molecular gas x alpha_CO (CO-to-H2 conversion, ~factor 2 either way): f_mol in [0.4, 1.2]
    KNOB 2  ATOMIC (HI) gas -- UNMEASURED at high z: f_HI in [0.0, 0.6]
    KNOB 3  V_flat vs the catalogued VC (a0 ~ V^4 amplifies it): (V_flat/VC) in [0.9, 1.1] -> ^4 in [0.66, 1.46]\n""")
    for name, fg, vr, desc in [
        ("framework-favoring extreme", 0.4, 1.1, "low gas + V_flat high"),
        ("central best estimate", 1.1, 1.0, "Tacconi molecular + modest HI, VC=V_flat"),
        ("constant-favoring extreme", 1.8, 0.9, "high gas + V_flat low")]:
        a0 = base*vr**4/(1+fg)
        fav = "ABOVE framework" if a0 > 1.96 else ("~framework" if a0 > 1.7 else ("~constant" if a0 > 0.95 else "below constant"))
        print(f"  {name:27}: a0 = {a0:.2f}   -> {fav:16} ({desc})")
    print(f"""
  => the systematic range is a0 ~ 0.5-2.5e-10 -- WIDER than the framework(1.96)-to-constant(1.20) gap. The
  CENTRAL best estimate (~1.0) leans constant, but the irreducible gas+V_flat systematic SPANS BOTH MODELS.\n""")

    print("="*92); print("THE HONEST CORRECTION TO 10c"); print("="*92)
    print("""  Project 10c said the real data 'mildly disfavor' the framework at ~1-2 sigma. That slightly OVERSTATES
  it: the central value does lean constant, but the systematic is large enough that it is not robust -- a
  framework defender can sit at the low-gas/high-V_flat corner (a0=2.25, above the framework) without being
  unreasonable. The fair statement is: the real data are INCONCLUSIVE on framework-vs-constant, with a
  CENTRAL PREFERENCE for constant. Not support for the rise (the curated 3-point claim does not survive), but
  not a clean disfavoring either. The same stress-test that deflated the framework's favorable claims must,
  in fairness, deflate this unfavorable one too. Reported symmetrically.\n""")

    print("="*92); print("WHAT A GAS-CLEAN MEASUREMENT NEEDS (why no existing sample suffices)"); print("="*92)
    print("""  To collapse this range you need, per galaxy: (1) CO with a calibrated alpha_CO AND an atomic-gas
  constraint (so M_bar is measured, not scaled); (2) a resolved rotation curve reaching the flat part (so
  V_flat is measured, not extrapolated); (3) deep-MOND-tail (low-surface-brightness) selection so V^4=G M_bar a0
  applies cleanly. No current high-z sample has all three: the gas-measured samples (PHIBSS/Genzel) are
  massive/HSB (wrong regime, biased V_flat), and the kinematic samples (KROSS/KMOS3D) lack per-galaxy gas. So
  the gas-limited result is genuinely the best the existing data allow -- which is the empirical case FOR the
  dedicated deep-MOND-tail + gas-census program (Project 17), now reinforced by having hit the wall directly.\n""")

    print("="*92); print("PROJECT 10d VERDICT"); print("="*92)
    print("""  The real high-z a0 is irreducibly gas+V_flat-limited: the systematic (~0.5-2.5e-10) is wider than the
  framework-vs-constant gap, so the data are INCONCLUSIVE, with a central preference for constant. This
  honestly softens 10c (from 'mildly disfavored' to 'inconclusive, central leans constant') -- the discipline
  applied symmetrically to the framework-unfavorable result. Net real-data status: the curated 'rise' is not
  supported, the central estimate leans constant, and a clean verdict requires the per-galaxy gas + V_flat +
  deep-tail measurement that only a dedicated program (Project 17) provides. The wall is real and now mapped.""")
    print("="*92)


if __name__ == "__main__":
    main()
