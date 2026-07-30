#!/usr/bin/env python3
r"""mi_forecast_systematics_audit_2026.py -- audit the two remaining live forecasts for the error I made
in Proposition 7: quoting sqrt(N) scaling on an uncertainty that is COHERENT and does not average down.

WHY. mi_dsph_closure_test_real_data_2026 showed Prop 7's forecast failed for exactly one reason: it
scaled the error as sigma_obj/sqrt(N) when the dominant term (stellar Upsilon_V) is common to the whole
sample. That is a generic failure mode, so the other two live forecasts are audited here rather than
trusted. Both are checked against their OWN frozen text, not against a paraphrase.

  FRONT A -- wide-binary gamma_v (PREREGISTRATION_DR4.md Sections 1.4-1.5)
  FRONT B -- s^TX SME boost dipole (same file, Section 2.4)

WHAT IS COMPUTED:
  S1  Front A's error model, reconstructed from the frozen text. Does sigma_sys survive N -> infinity?
  S2  Front A's quoted "N >~ 12,200, expected DECIDABLE" -- reproduce it, and check what it assumed.
  S3  Front A's sigma_sys = 0.02 against the LITERATURE SPREAD on the same quantity. The real finding.
  S4  Front B -- does it make any sqrt(N) claim at all? And what improvement decides it?
  S5  Verdict per front, and which of the two needs an amendment.

Exit 0 = ran and all internal checks held. No hard-coded verdicts.
"""
from __future__ import annotations
import numpy as np

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

# --- FROZEN values, quoted verbatim from PREREGISTRATION_DR4.md ---
SIG_SYS = 0.02            # 1.5: frozen allowance
SIG_FIT_30K = 0.019       # 1.5: sigma_fit at N = 30000
N_REF = 30000
G_NEWT, G_MI, G_MG, G_MOND = 1.00, 1.09, 1.137, 1.33
N_QUOTED = 12200          # 1.5: "Newton vs MI 1.09 at 3 sigma needs N >~ 12,200"
N_QUOTED_MG = 45000
# s^TX, Section 2.1/2.4
STX_PRED_CAN, STX_PRED_ALT = 8.68e-10, 1.048e-9
STX_BOUND = 1.3e-9        # Hees+ 2016 combined multi-planet secular fit
STX_SINGLE_CHANNEL = 1.5e-7   # 2.4: Cassini-Saturn direct-range alone
# literature gamma_v values the prereg itself cites / the DR3 dry run
LIT = {"Chae 2026 (arXiv:2601.21728)": 1.26, "Banik+24 Newtonian-consistent": 1.00,
       "prereg DR3 dry run (guard zone)": 1.205}


def sig_fit(N):
    return SIG_FIT_30K * np.sqrt(N_REF / np.asarray(N, float))


def sig_tot(N):
    return np.sqrt(sig_fit(N) ** 2 + SIG_SYS ** 2)


def main() -> int:
    banner("S1. FRONT A -- the error model does the right thing structurally")
    print("  Frozen text: sigma_tot = sqrt(sigma_fit^2 + 0.02^2), sigma_fit scales as sqrt(30000/N).")
    print("  So the systematic is held OUTSIDE the sqrt(N) and survives N -> infinity. This is exactly")
    print("  what Prop 7 failed to do, and Front A gets it RIGHT. Credit where due.")
    print(f"  {'N':>9s} {'sigma_fit':>10s} {'sigma_tot':>10s} {'floor?':>8s}")
    for N in (5000, 12200, 21600, 30000, 100000, 1000000):
        print(f"  {N:9d} {float(sig_fit(N)):10.4f} {float(sig_tot(N)):10.4f} "
              f"{'-> 0.020' if N >= 1000000 else '':>8s}")
    check(abs(float(sig_tot(10**9)) - SIG_SYS) < 1e-4,
          f"sigma_tot -> {SIG_SYS} as N -> infinity, i.e. the systematic does NOT average down. The "
          f"structure is correct and Front A is NOT making Prop 7's mistake")

    banner("S2. But the QUOTED sample size is statistical-only. Reproduce and check.")
    d_newt = G_MI - G_NEWT
    print(f"  Newton-vs-MI separation to detect: |1.09 - 1.00| = {d_newt:.3f} in gamma_v")
    n_stat = N_REF * (SIG_FIT_30K / (d_newt / 3.0)) ** 2
    print(f"  Using sigma_fit ALONE (statistical only): 3 sigma needs sigma_fit <= {d_newt/3:.4f},")
    print(f"      N >= 30000 * (0.019/{d_newt/3:.4f})^2 = {n_stat:.0f}   <-- reproduces the quoted "
          f"{N_QUOTED}")
    check(abs(n_stat - N_QUOTED) / N_QUOTED < 0.10,
          f"the frozen figure {N_QUOTED} is reproduced to {100*abs(n_stat-N_QUOTED)/N_QUOTED:.0f}% by a "
          f"STATISTICAL-ONLY calculation -- so it excludes sigma_sys, as its own label 'statistical' says")
    need_fit = np.sqrt(max((d_newt / 3.0) ** 2 - SIG_SYS ** 2, 0.0))
    n_tot = N_REF * (SIG_FIT_30K / need_fit) ** 2 if need_fit > 0 else np.inf
    print(f"  Using sigma_tot (systematic INCLUDED): need sigma_tot <= {d_newt/3:.4f}, so")
    print(f"      sigma_fit <= {need_fit:.4f}  ->  N >= {n_tot:.0f}")
    print(f"  RATIO: the honest requirement is {n_tot/N_QUOTED:.2f}x the quoted figure.")
    check(n_tot > N_QUOTED,
          f"including the frozen sigma_sys raises the Newton-vs-MI requirement from {N_QUOTED} to "
          f"{n_tot:.0f}, a factor {n_tot/N_QUOTED:.2f} -- the label 'statistical' is doing real work and "
          f"is easy to miss next to the words 'expected DECIDABLE'")
    print(f"  The saturation ceiling is what actually matters: z_max = {d_newt/SIG_SYS:.2f} sigma for")
    print(f"  Newton-vs-MI, and {(G_MG-G_MI)/SIG_SYS:.2f} sigma for MI-vs-MG, no matter how large N gets.")
    check((G_MG - G_MI) / SIG_SYS < 3.0,
          f"MI-vs-MG ceilings at {(G_MG-G_MI)/SIG_SYS:.2f} sigma even at infinite N -- which is exactly why "
          f"the prereg pre-declares it 'likely UNDECIDABLE' and demands sigma_sys < 0.01. Handled correctly")

    banner("S3. *** THE REAL FINDING: is sigma_sys = 0.02 CREDIBLE? ***")
    print("  The frozen allowance covers: eccentricity-model mismatch +/-0.015, a0-footing spread")
    print("  <=0.005, residual shape/g_ext dependence. Note what is NOT itemised: UNDETECTED")
    print("  COMPANIONS, which the prereg elsewhere calls the contamination axis and which pushes")
    print("  gamma_v coherently UP for the whole sample.")
    print("  Now compare against the published spread on this very quantity:")
    for k, v in LIT.items():
        print(f"      {k:<36s} gamma_v = {v:.3f}")
    spread = max(LIT.values()) - min(LIT.values())
    print(f"  Literature spread on gamma_v: {spread:.3f}")
    print(f"  Frozen sigma_sys:             {SIG_SYS:.3f}")
    print(f"  ratio = {spread/SIG_SYS:.1f}")
    check(spread / SIG_SYS > 5.0,
          f"two careful groups differ by {spread:.2f} in gamma_v on overlapping data while the frozen "
          f"systematic allowance is {SIG_SYS:.2f} -- a factor {spread/SIG_SYS:.0f}. sigma_sys = 0.02 is "
          f"NOT credible as an allowance for the dominant coherent term")
    print("  WHAT THIS DOES AND DOES NOT MEAN. It does NOT mean the prereg is wrong to freeze a number:")
    print("  freezing 0.02 before data is far better practice than fitting it afterwards. It means the")
    print("  number is optimistic, and that the prereg's own contamination-guard machinery (the >1.20")
    print("  guard zone, cut 12's NSS screen, the strictness ladder) is carrying more weight than")
    print("  sigma_sys is. Those are qualitative guards; sigma_sys is the quantitative one, and it is")
    print(f"  {spread/SIG_SYS:.0f}x smaller than the field's own disagreement.")
    print("  CONSEQUENCE FOR THE BANDS: at sigma_sys = 0.02 the 1.083-1.145 window reads as")
    print("  'non-Newtonian at >=3 sigma AND MI-compatible'. If the true coherent systematic is even")
    print(f"  {3*SIG_SYS:.2f}, that window is inside 1 sigma of Newton and decides nothing.")
    for alt_sys in (0.05, 0.10, 0.26):
        z = d_newt / np.sqrt(SIG_FIT_30K**2 + alt_sys**2)
        print(f"      if sigma_sys were {alt_sys:.2f}: Newton-vs-MI ceiling = {z:.2f} sigma at N=30k")

    banner("S4. FRONT B -- s^TX. Does it make a sqrt(N) claim? No. Check what it does claim.")
    print("  Frozen Section 2.4 states the single Cassini-Saturn channel reaches sigma(s^TX) ~ 1.5e-7,")
    print("  '~2 orders short of the prediction', detection significance ~0.006 sigma, and that the")
    print("  decision 'lives in the multi-planet combined fit'. That is a sensitivity statement with NO")
    print("  sqrt(N) extrapolation attached. Front B is CLEAN of Prop 7's error.")
    print(f"  {'quantity':<34s} {'value':>12s}")
    print(f"  {'prediction, canonical':<34s} {STX_PRED_CAN:12.3e}")
    print(f"  {'prediction, alt':<34s} {STX_PRED_ALT:12.3e}")
    print(f"  {'published bound (Hees+ 2016)':<34s} {STX_BOUND:12.3e}")
    print(f"  {'single-channel sensitivity':<34s} {STX_SINGLE_CHANNEL:12.3e}")
    print(f"  margin (bound/prediction): {STX_BOUND/STX_PRED_CAN:.2f}x canonical, "
          f"{STX_BOUND/STX_PRED_ALT:.2f}x alt")
    check(abs(STX_BOUND / STX_PRED_CAN - 1.50) < 0.02,
          f"the frozen 1.50x / 1.24x margins reproduce exactly from the quoted numbers")
    print("  THE AUDIT QUESTION FOR FRONT B is therefore different: not 'does the error average down'")
    print("  but 'can the BOUND improve enough to decide, or is it systematics-floored?'")
    imp_needed = STX_BOUND / (STX_PRED_CAN / 3.0)
    print(f"  To reach a 3-sigma statement either way, the bound must tighten to "
          f"{STX_PRED_CAN/3:.3e},")
    print(f"  i.e. improve by {imp_needed:.1f}x.")
    print(f"  The single-channel route is {STX_SINGLE_CHANNEL/(STX_PRED_CAN/3):.0f}x away from that, so it")
    print("  cannot contribute -- exactly as Section 2.4 says.")
    check(imp_needed > 3.0,
          f"a {imp_needed:.1f}x bound improvement is needed to decide Front B, and the prereg makes no "
          f"claim that it will happen -- the honest gap is that nobody has checked whether ephemeris "
          f"SME bounds CAN improve {imp_needed:.1f}x or are systematics-floored")
    print("  WHY THAT MATTERS: ephemeris SME bounds come from a combined multi-planet secular fit with")
    print("  strong correlations between coefficients and modelling systematics, so they do NOT scale as")
    print("  sqrt(observations). A 4.5x improvement is a claim about ephemeris systematics, not about")
    print("  data volume, and it is UNVERIFIED in this corpus either way.")
    print(f"  Note also the margin is thin: at {STX_BOUND/STX_PRED_CAN:.2f}x, a mere "
          f"{STX_BOUND/STX_PRED_CAN:.2f}x tightening puts the prediction AT the bound.")

    banner("S5. VERDICT -- per front")
    print("  FRONT A (wide binary): STRUCTURE CORRECT, ALLOWANCE OPTIMISTIC.")
    print("   * It does NOT make Prop 7's error: sigma_sys sits outside the sqrt(N) and survives")
    print(f"     N -> infinity, ceilinging Newton-vs-MI at {d_newt/SIG_SYS:.1f} sigma and MI-vs-MG at "
          f"{(G_MG-G_MI)/SIG_SYS:.1f} sigma.")
    print(f"   * The quoted 'N >~ {N_QUOTED}, expected DECIDABLE' is STATISTICAL-ONLY (reproduced here");
    print(f"     to {100*abs(n_stat-N_QUOTED)/N_QUOTED:.0f}%); with sigma_sys included it is N >~ {n_tot:.0f}.")
    print(f"   * sigma_sys = 0.02 is {spread/SIG_SYS:.0f}x smaller than the published disagreement on the same")
    print("     quantity, and does not itemise undetected companions -- the dominant coherent term.")
    print("   * RECOMMENDED AMENDMENT (pre-data, in the open): state the saturation ceilings explicitly")
    print("     next to the sample-size figures, and either raise sigma_sys or justify 0.02 against the")
    print("     Chae/Banik disagreement. Raising it AFTER data would be unusable, so it must be now.")
    print()
    print("  FRONT B (s^TX): CLEAN, and the honest gap is elsewhere.")
    print("   * No sqrt(N) claim is made anywhere; Section 2.4 is an exemplary sensitivity statement.")
    print(f"   * Deciding it needs a {imp_needed:.1f}x bound improvement, which is a statement about")
    print("     ephemeris systematics rather than data volume, and is UNVERIFIED.")
    print(f"   * The {STX_BOUND/STX_PRED_CAN:.2f}x margin is thin enough that the front is close to the edge in")
    print("     both directions: a modest tightening excludes the prediction; a stall leaves it")
    print("     permanently undecided.")
    print("   * RECOMMENDED: no amendment needed. Add one open item -- check whether the Hees-class")
    print("     bound is photon-limited or systematics-floored, since that decides whether Front B is a")
    print("     live front or a parked one.")
    print()
    print("  NET: one of the two forecasts needed auditing and it was not the one I expected. Front B")
    print("  was already honest. Front A is structurally sound but carries an allowance that the field's")
    print("  own scatter contradicts by an order of magnitude.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
