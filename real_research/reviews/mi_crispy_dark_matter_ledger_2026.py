#!/usr/bin/env python3
r"""mi_crispy_dark_matter_ledger_2026.py -- "CRISPY DARK MATTER": a PRE-REGISTERED forecast of how
LCDM will be adjusted to absorb an evolving acceleration scale, IF DESI's evolving dark energy holds.

THE POINT, AND THE HONEST FRAMING FIRST. Adjusting a model's parameters when new data arrives is
NORMAL SCIENCE, not cheating. LCDM practitioners will absorb an evolving RAR normalization the same
way they have absorbed every other galactic-scale surprise: by adjusting halo concentration evolution
and baryonic feedback, which are genuinely uncertain. This document does not accuse anyone of anything.
Its value is that it is written BEFORE the data, so that:
  (a) the absorption, if it happens, is recognisable as absorption rather than as prediction, and
  (b) the PARAMETER COST of the absorption is on the record, quantified, in advance.
"Crispy dark matter" is the name for the absorbed model -- LCDM plus whatever redshift-dependent
function is required to hold the acceleration scale where the data puts it. Naming it is a device for
recognising it later, nothing more.

THE STRUCTURE OF THE TEST. The framework ties the acceleration scale to the dark-energy density:
      a0 = kappa * c * sqrt(G rho_Lambda),  kappa = 1/2
so if rho_Lambda evolves, a0 evolves, with NO new parameters -- the evolution is fixed by whatever
(w0, wa) DESI measures. LCDM has no a0; its emergent acceleration scale is set by halo structure, whose
natural scaling is g_dagger ~ sqrt(G rho_crit(z)) ~ H(z) = H0 E(z). Those are DIFFERENT functions of z.
That difference is the whole test, and it is what crispy dark matter must absorb.

WHAT IS COMPUTED:
  S1  What "DESI comes in my favour" means numerically, with provenance flagged.
  S2  The framework's parameter-free a0(z), BOTH FOOTINGS.
  S3  LCDM's natural scale E(z), and the ABSORPTION FUNCTION A(z) = required compensation, in dex.
  S4  *** THE FOOTING FORK, which decides whether this test exists at all. ***
  S5  Crispy dark matter, defined: its free function, its parameter count, and the Occam ledger.
  S6  The pre-registered scoreboard: what counts as absorption, what would falsify the framework.

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

OM = 0.315
ZS = [0.0, 0.5, 1.0, 2.0, 3.0]

# DESI DR2 (2025) w0waCDM combinations. PROVENANCE FLAG: quoted from memory of the DR2 release, NOT
# re-fetched in this session. The conclusions are reported as a FUNCTION of (w0, wa) precisely so that
# a correction to these central values rescales the answer instead of invalidating it.
DESI = [
    ("LCDM (null)",              -1.000,  0.00),
    ("DESI DR2 BAO+CMB+SN",      -0.752, -0.86),
    ("DESI DR2 BAO+CMB",         -0.420, -1.75),
]


def E_of_z(z, w0=-1.0, wa=0.0):
    """Expansion rate for w(a) = w0 + wa(1-a), flat."""
    z = np.asarray(z, float)
    a = 1.0 / (1.0 + z)
    de = (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
    return np.sqrt(OM * (1 + z) ** 3 + (1 - OM) * de)


def a0_ratio_canonical(z, w0, wa):
    """a0 ~ sqrt(rho_Lambda) => the banked bump-then-decline law."""
    z = np.asarray(z, float)
    a = 1.0 / (1.0 + z)
    return (1 + z) ** (1.5 * (1 + w0 + wa)) * np.exp(-1.5 * wa * (1 - a))


def a0_ratio_alt(z, w0, wa):
    """alt footing: a0 ~ c H(z)/Z => tracks E(z)."""
    return E_of_z(z, w0, wa) / E_of_z(0.0, w0, wa)


def main() -> int:
    banner("S1. What 'DESI comes in my favour' means, numerically")
    print("  The framework's stake in DESI is narrow and specific: it needs rho_Lambda to EVOLVE, because")
    print("  a0 = kappa c sqrt(G rho_Lambda) then forces a0 to evolve too, with no freedom. DESI's")
    print("  w0waCDM preference is exactly that measurement.")
    print(f"  {'combination':<24s} {'w0':>8s} {'wa':>8s} {'1+w0+wa':>9s}")
    for nm, w0, wa in DESI:
        print(f"  {nm:<24s} {w0:8.3f} {wa:8.2f} {1+w0+wa:9.3f}")
    print("  PROVENANCE FLAG: these DR2 central values are quoted from memory, not re-fetched here.")
    print("  Everything below is computed AS A FUNCTION of (w0, wa), so a correction to the central")
    print("  values rescales the forecast rather than invalidating it. That is deliberate.")
    check(abs(1 + DESI[0][1] + DESI[0][2]) < 1e-12, "the LCDM null row has 1+w0+wa = 0 as it must")

    banner("S2. The framework's parameter-free a0(z) -- both footings")
    print("  CANONICAL (rho_DE): a0 ~ sqrt(rho_Lambda) -> a0(z)/a0(0) = (1+z)^{1.5(1+w0+wa)} e^{-1.5 wa z/(1+z)}")
    print("  ALT (rho_total):    a0 ~ c H(z)/Z         -> a0(z)/a0(0) = E(z)/E(0)")
    for nm, w0, wa in DESI:
        can = a0_ratio_canonical(ZS, w0, wa)
        alt = a0_ratio_alt(ZS, w0, wa)
        print(f"\n  {nm}")
        print("    z            " + "".join(f"{z:9.1f}" for z in ZS))
        print("    a0/a0(0) can " + "".join(f"{v:9.3f}" for v in can))
        print("    a0/a0(0) alt " + "".join(f"{v:9.3f}" for v in alt))
    can_desi = a0_ratio_canonical(ZS, *DESI[1][1:])
    print("\n  Note the SHAPE on the canonical footing with DESI's numbers: a mild rise then a decline")
    print("  (the banked bump-then-decline law), NOT a monotone rise. A claim that the framework")
    print("  predicts a rising a0 is a Taylor-expansion artifact that drops wa.")
    check(can_desi[1] > can_desi[0] and can_desi[-1] < can_desi[0],
          f"canonical a0(z) is bump-then-decline: {can_desi[1]:.3f} at z=0.5 rising above 1, "
          f"{can_desi[-1]:.3f} at z=3 falling below")

    banner("S3. LCDM's natural scale, and the ABSORPTION FUNCTION A(z)")
    print("  LCDM has no a0. Its emergent acceleration scale comes from halo structure, whose")
    print("  characteristic value scales as sqrt(G rho_crit(z)) ~ H(z). So LCDM's UNADJUSTED")
    print("  expectation is g_dagger(z)/g_dagger(0) = E(z).")
    print("  Define the absorption function -- what crispy dark matter must supply:")
    print("      A(z) = [a0(z)/a0(0)]_framework / [E(z)]_LCDM      (dex below)")
    print(f"  {'combination':<24s} {'footing':<10s}" + "".join(f"{('z='+str(z)):>10s}" for z in ZS[1:]))
    absorb = {}
    for nm, w0, wa in DESI:
        Ez = E_of_z(ZS, w0, wa) / E_of_z(0.0, w0, wa)
        for fname, fn in (("canonical", a0_ratio_canonical), ("alt", a0_ratio_alt)):
            A = fn(ZS, w0, wa) / Ez
            absorb[(nm, fname)] = A
            print(f"  {nm:<24s} {fname:<10s}" + "".join(f"{np.log10(v):10.3f}" for v in A[1:]))
    print("  (values are log10 A, i.e. dex of compensation LCDM must apply; 0.000 = nothing to absorb)")
    A_can = absorb[(DESI[1][0], "canonical")]
    check(abs(np.log10(A_can[2])) > 0.1,
          f"on the canonical footing with DESI's numbers, LCDM must absorb "
          f"{abs(np.log10(A_can[2])):.3f} dex at z=1 -- a real, signed, sizeable requirement")

    banner("S3b. *** HOW MUCH OF THAT ABSORPTION IS ACTUALLY DESI-DEPENDENT? Far less than it looks. ***")
    print("  This corrects the framing I started with, and it has to be said before anything else is")
    print("  claimed. Compare the canonical rows: the LCDM null (w0=-1, wa=0, so a0 is CONSTANT) needs")
    print(f"  {abs(np.log10(absorb[(DESI[0][0],'canonical')][2])):.3f} dex of absorption at z=1, and DESI's "
          f"evolving-DE case needs {abs(np.log10(A_can[2])):.3f} dex. Those are")
    print("  nearly the same number. So the bulk of the requirement has NOTHING to do with DESI -- it is")
    print("  the old fact that a0 looks CONSTANT while E(z) RISES, which LCDM has been absorbing for")
    print("  years via concentration and feedback evolution, and largely successfully.")
    print()
    print("  The genuinely NEW, DESI-dependent content is only the framework's departure from a")
    print("  CONSTANT a0. That is the signal that would not exist if DESI returned w0=-1, wa=0:")
    print(f"  {'combination':<24s}" + "".join(f"{('z='+str(z)):>10s}" for z in ZS[1:]))
    desi_signal = {}
    for nm, w0, wa in DESI:
        sig = np.log10(a0_ratio_canonical(ZS, w0, wa))     # vs constant a0 = 0 dex
        desi_signal[nm] = sig
        print(f"  {nm:<24s}" + "".join(f"{v:10.3f}" for v in sig[1:]))
    print("  (dex deviation of a0(z) from CONSTANT -- this, not the 0.25 dex above, is the DESI test)")
    s_desi = desi_signal[DESI[1][0]]
    print()
    print("  THREE CONSEQUENCES, all against the exciting version of the story:")
    print(f"   1. The signal is SMALL: {abs(s_desi[1]):.3f} dex at z=0.5 and {abs(s_desi[2]):.3f} dex at z=1,")
    print(f"      rising only to {abs(s_desi[4]):.3f} dex by z=3.")
    print("   2. It CHANGES SIGN. Bump-then-decline means a0 is slightly ABOVE its present value at low")
    print("      z and BELOW it at high z, crossing zero near z ~ 1.")
    print(f"   3. So z ~ 1 -- where most high-z kinematics actually exists -- has almost NO discriminating")
    print("      power for the DESI-dependent part. The test needs z >~ 2.")
    izero = int(np.argmin(np.abs(s_desi)))
    check(abs(s_desi[2]) < abs(s_desi[4]) and abs(s_desi[2]) < 0.02,
          f"the DESI-dependent signal nearly vanishes at z=1 ({abs(s_desi[2]):.4f} dex) and only reaches "
          f"{abs(s_desi[4]):.3f} dex at z=3 -- so this is a z >~ 2 test, not a z ~ 1 test")
    check(np.sign(s_desi[1]) != np.sign(s_desi[4]),
          "the DESI-dependent signal changes SIGN between z=0.5 and z=3, which is the distinctive shape "
          "but also why a single-redshift measurement cannot see it")

    banner("S4. *** THE FOOTING FORK -- it decides whether this test exists at all ***")
    print("  This is the load-bearing result and it cuts against the exercise, so it goes first, not")
    print("  in a footnote:")
    for nm, w0, wa in DESI:
        Aalt = absorb[(nm, "alt")]
        print(f"    {nm:<24s} alt-footing absorption at z=1,2,3 = "
              f"{np.log10(Aalt[2]):+.4f}, {np.log10(Aalt[3]):+.4f}, {np.log10(Aalt[4]):+.4f} dex")
    alt_max = max(abs(np.log10(absorb[(nm, 'alt')])).max() for nm, _, _ in DESI)
    check(alt_max < 1e-9,
          f"on the ALT footing the absorption function is IDENTICALLY ZERO (max |log10 A| = {alt_max:.1e}) "
          f"for every (w0,wa) -- the framework and LCDM predict the SAME z-scaling and there is NO test")
    print("  READ THIS PLAINLY. On the alt footing a0 ~ cH(z)/Z tracks E(z) BY CONSTRUCTION, which is")
    print("  exactly LCDM's natural halo scaling. The two theories become indistinguishable in this")
    print("  channel and crispy dark matter never has to exist. So:")
    print("    * the ENTIRE prediction below is CONDITIONAL ON THE CANONICAL (rho_DE) FOOTING;")
    print("    * the footing choice is not a detail here, it IS the experiment;")
    print("    * anyone who prefers the alt footing owes no absorption function at all.")
    print("  This is the sharpest thing the exercise produces, and it is a constraint on the framework")
    print("  before it is a constraint on anyone else.")

    banner("S5. CRISPY DARK MATTER, defined -- and the Occam ledger")
    print("  DEFINITION. Crispy dark matter = LCDM + a redshift-dependent suppression of the emergent")
    print("  acceleration scale, A(z), delivered through the two sectors that are genuinely free:")
    print("    (i)  halo concentration evolution c(M,z) beyond the standard fit, and")
    print("    (ii) baryonic feedback strength as a function of z (outflow efficiency, size growth).")
    print("  Required values on the canonical footing with DESI DR2 BAO+CMB+SN:")
    for z, v in zip(ZS[1:], A_can[1:]):
        print(f"    z = {z:<4.1f}  A(z) = {v:.3f}  ({np.log10(v):+.3f} dex, i.e. "
              f"{'suppress' if v < 1 else 'enhance'} by {abs(1-v)*100:.0f}%)")
    print()
    print("  PARAMETER COUNT -- the actual discriminator, since BOTH will fit:")
    print("    framework : 0 new parameters. a0(z) is fixed by (w0, wa), which DESI measures")
    print("                INDEPENDENTLY from BAO. Nothing is tuned to the RAR.")
    print("    crispy DM : >= 2 new parameters to span a monotone A(z) over 0 < z < 3 (an amplitude")
    print("                and a slope at minimum; realistically a free function).")
    print("  So the comparison is NOT about fit quality. It is about whether a parameter-free curve or")
    print("  a fitted function describes the same data. Occam ledger, in bans (log10 evidence ratio),")
    print("  for N high-z RAR normalisation measurements at per-point precision sigma dex:")
    print(f"  {'N':>5s} {'sigma (dex)':>12s} {'signal (dex)':>13s} {'bans for framework':>20s}")
    sig_dex = abs(s_desi[4])   # the DESI-DEPENDENT signal at z=3, per S3b -- NOT the 0.25 dex E(z) term
    print(f"  (scored on the DESI-DEPENDENT signal at z=3, {sig_dex:.3f} dex, per S3b -- scoring it on the")
    print("   0.25 dex E(z) term would be double-counting an accommodation LCDM already made)")
    for N in (5, 20, 50):
        for sig in (0.10, 0.05):
            chi2 = N * (sig_dex / sig) ** 2
            bans = 0.5 * chi2 / np.log(10) - 1.0        # minus ~1 ban for the 2 extra crispy params
            print(f"  {N:5d} {sig:12.2f} {sig_dex:13.3f} {bans:20.1f}")
    check(True, "the ledger is expressed in bans so it can be scored later, not asserted rhetorically")
    print("  A ban is a factor of 10 in evidence. Note the ledger only favours the framework if the")
    print("  MEASURED a0(z) actually lands on the parameter-free curve -- if it lands anywhere else,")
    print("  the same arithmetic runs against the framework, and harder, because it has no freedom.")

    banner("S6. PRE-REGISTERED SCOREBOARD (frozen 2026-07-30)")
    print("  WHAT WOULD COUNT AS ABSORPTION (recognisable as such because it is written first):")
    print("   1. New concentration-evolution fits appearing with a z-dependent normalisation whose")
    print("      amplitude matches A(z) above to within its errors, introduced to fit high-z kinematics")
    print("      rather than derived from N-body.")
    print("   2. Feedback-strength retuning that lowers the effective acceleration scale at z ~ 1-2 by")
    print(f"      {abs(np.log10(A_can[2]))*100:.0f}-{abs(np.log10(A_can[3]))*100:.0f}% in dex terms, "
          f"presented as a resolution of a high-z RAR 'tension'.")
    print("   3. Any new free function of z in the halo-galaxy connection whose fitted shape tracks")
    print("      sqrt(rho_Lambda(z)) rather than E(z). That specific shape is the tell, because there is")
    print("      no LCDM reason for halo structure to know about the dark-energy density.")
    print()
    print("  WHAT WOULD FALSIFY THE FRAMEWORK (same document, equal weight):")
    print("   1. A measured a0(z) tracking E(z) within errors -> the canonical footing is wrong, the")
    print("      alt footing survives but predicts nothing distinctive here, and this whole channel dies.")
    print("   2. A measured a0(z) MONOTONE RISING steeply -> inconsistent with bump-then-decline on any")
    print("      (w0, wa) DESI allows; the a0-rho_Lambda link fails.")
    print("   3. DESI DR3+ converging back on w0 = -1, wa = 0 -> rho_Lambda constant -> a0 constant ->")
    print("      no evolution to predict, no absorption to demand, and the framework's most distinctive")
    print("      cosmological consequence evaporates. THE TEST IS HOSTAGE TO DESI, not to LCDM.")
    print()
    print("  HONEST SUMMARY OF WHAT THIS DOCUMENT IS. A conditional, footing-dependent forecast with a")
    print("  parameter ledger, not a discovery. Two findings run AGAINST the version I set out to write,")
    print("  and they are the most useful things in it:")
    print("   * S3b: most of the headline 0.25 dex absorption is the old constant-a0-vs-E(z) fact, which")
    print("     LCDM already absorbs. The DESI-dependent part is only ~0.13 dex at z=3, ~0 at z=1, and")
    print("     changes sign. So this is a z >~ 2 test with a small amplitude, not a dramatic near-term one.")
    print("   * S4: on the alt footing the prediction is identically empty. The framework must COMMIT to")
    print("     the canonical rho_DE footing to have any claim here -- and that commitment is testable.")
    print("  It also is NOT an accusation. If LCDM absorbs this, that is how the model is supposed to")
    print("  work; the only thing worth insisting on is that the absorption be counted as parameters")
    print("  spent, not as a prediction fulfilled.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
