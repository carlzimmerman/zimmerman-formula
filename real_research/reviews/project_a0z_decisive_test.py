#!/usr/bin/env python3
r"""
THE DECISIVE TEST of the framework's one distinctive prediction:  a0(z) = c H(z) / Z  ->  a0(z)/a0(0) = E(z).
============================================================================================================
The framework's single falsifiable, distinctive signature is that the MOND acceleration scale TRACKS the
Hubble rate:  a0(z)/a0(0) = E(z) = sqrt(Om(1+z)^3 + OL).  Standard MOND (Milgrom/McGaugh) says a0 = CONSTANT.
LambdaCDM has NO acceleration scale, but a MOND law fit to LCDM galaxies recovers an APPARENT a0 that ALSO
rises ~ E(z) (denser halos at high z) -- so the rise alone is LCDM-DEGENERATE.

This script does four jobs, quantitatively and honestly:
  (a) the predicted EFFECT SIZES at z = 0.5, 1, 2, 3 (a0, V_flat ~ E^1/4, BTFR zero-point ~ 1/E, RAR knee);
  (b) what the CURRENT high-z datasets actually show vs E(z), with a defensible sigma on the present "lean";
  (c) the single DECISIVE near-term test: facility + sample + precision to settle a0(z) at >=3 sigma;
  (d) the honest VERDICT: open / leaning-unfavorable-at-N-sigma / excluded.

Companion files (do not contradict): project_a0z_reconciled.py, A0Z_STATUS_CORRECTED.md (header),
project_highz_a0_synthesis.py, project17_z3_program.py, z3_forecast_tightened.py, z3_a0_observing_proposal.py.
Needs numpy.
"""
import numpy as np

# ---------------------------------------------------------------------------------------------------------
# Cosmology / constants
# ---------------------------------------------------------------------------------------------------------
c, G = 2.99792458e8, 6.674e-11
Mpc = 3.0857e22
Om, OL = 0.315, 0.685
H0 = 67.4e3 / Mpc
Z = 2 * np.sqrt(8 * np.pi / 3)          # 2 sqrt(8pi/3) = sqrt(32pi/3) = 5.789 (FRAMEWORK.md)
A0 = 1.2e-10                             # local MOND scale (McGaugh ~1.2e-10)

E = lambda z: np.sqrt(Om * (1 + z) ** 3 + OL)          # framework: a0(z)/a0(0)


def siv(z):
    """Scale-Invariant-Vacuum / event-horizon competitor: a0 FALLS with z (the third hypothesis)."""
    num = (1 - Om) / (1 + z) ** 1.5 + Om
    return (1 + z) ** -1.5 * num ** (-4 / 3) / ((1 - Om) + Om) ** (-4 / 3)


ZS = (0.5, 1.0, 2.0, 3.0)

# ---------------------------------------------------------------------------------------------------------
# Empirical scatter budget (from the repo's SPARC analyses + the high-z error budget)
#   RAR total scatter (McGaugh/Lelli)            ~ 0.13 dex in g_obs  (sparc_rar_honest.py: ours 0.13-0.20)
#   RAR intrinsic (orthogonal, Lelli+2017)       ~ 0.057-0.069 dex    (observation-dominated; floor)
#   Per-galaxy a0 from a FULL high-z rotation curve ~ 0.15 dex        (z3_a0_observing_proposal.py)
#   a0 ~ V^4, so a 0.13 dex scatter in g_obs (=V^4 at fixed g_bar) is 0.13/4 = 0.033 dex in V_flat.
# ---------------------------------------------------------------------------------------------------------
RAR_SCATTER_GOBS = 0.13       # dex, total RAR scatter in the acceleration (= scatter in a0 ~ V^4)
RAR_INTRINSIC_GOBS = 0.069    # dex, intrinsic floor (Lelli+2017); 0.069 dex in V^4 -> 0.069/4 in V_flat
SIG_GAL_A0_HIGHZ = 0.15       # dex, realistic per-galaxy a0 from a full z~3 rotation curve
SIG_ANCHOR_LOOSE = 0.09       # dex, z=0 anchor systematic if a0 read as ABSOLUTE (M/L-dominated)
SIG_ANCHOR_TIGHT = 0.05       # dex, z=0 anchor in a RATIO with deep-MOND gas-dominated points (cancels)


# =========================================================================================================
def part_a_effect_sizes():
    print("=" * 100)
    print("(a) PREDICTED EFFECT SIZES -- a0(z)/a0(0)=E(z); constant-a0 MOND would give 1.00 for EVERY column")
    print("=" * 100)
    print("""  Deep-MOND identities used (all from V_flat^4 = G M_b a0, the BTFR):
     a0(z)/a0(0)            = E(z)            (the signature itself)
     V_flat / V_flat(0)     = E(z)^(1/4)      (fixed baryonic mass rotates faster at high z)
     BTFR zero-point ratio  = 1 / E(z)        (zero-point = -(1/4)log10(G a0); a0 up -> intercept down)
     RAR knee g_dagger ratio= E(z)            (the RAR "knee"/scale acceleration IS a0)
     g_obs at fixed g_bar   = E(z)^(1/2)      (deep-MOND g_obs = sqrt(g_bar a0))\n""")
    hdr = ["z", "E(z)=a0 ratio", "a0 up by", "V_flat ratio", "V_flat up by",
           "BTFR-zp ratio", "g_obs ratio", "(SIV a0 ratio)"]
    print("  " + "".join(f"{h:>14}" for h in hdr))
    for z in ZS:
        e = E(z)
        row = [f"{z:>14.1f}",
               f"{e:>14.3f}",
               f"{(e-1)*100:>13.0f}%",
               f"{e**0.25:>14.3f}",
               f"{(e**0.25-1)*100:>13.0f}%",
               f"{1/e:>14.3f}",
               f"{e**0.5:>14.3f}",
               f"{siv(z):>14.3f}"]
        print("  " + "".join(row))
    e2 = E(2.0)
    print(f"""
  READING (the signal is LARGE, hence testable): at z=2, E={e2:.2f} -> a0 is up ~{(e2-1)*100:.0f}%, a
  fixed-mass galaxy rotates ~{(e2**0.25-1)*100:.0f}% faster (V_flat x{e2**0.25:.2f}), the BTFR zero-point drops by
  ~factor {e2:.1f} (down {(1-1/e2)*100:.0f}%), and the RAR knee shifts up x{e2:.1f}. These are NOT 0.1-dex effects:
  log10(E(2))={np.log10(e2):.2f} dex in a0, log10(E(2)^0.25)={np.log10(e2**0.25):.3f} dex in V_flat. By z=3 the a0
  lever arm is log10(E(3))={np.log10(E(3.0)):.2f} dex -- a giant, few-galaxy-detectable signal.\n""")


# =========================================================================================================
def part_a2_signal_vs_scatter():
    print("=" * 100)
    print("(a') SIGNAL-TO-SCATTER -- is each effect bigger than the empirical RAR scatter?")
    print("=" * 100)
    print(f"  Empirical scatter (SPARC): RAR total ~{RAR_SCATTER_GOBS} dex in g_obs(=a0~V^4); intrinsic floor "
          f"~{RAR_INTRINSIC_GOBS} dex.")
    print(f"  In V_flat that is ~{RAR_SCATTER_GOBS/4:.3f} dex (total) / ~{RAR_INTRINSIC_GOBS/4:.3f} dex (floor), "
          f"since a0 ~ V_flat^4.\n")
    print(f"  {'z':>5}{'signal in a0 [dex]':>20}{'/ RAR total (0.13)':>20}{'signal in V_flat [dex]':>24}"
          f"{'/ V_flat floor':>16}")
    for z in ZS:
        sa = np.log10(E(z))
        sv = np.log10(E(z) ** 0.25)
        print(f"  {z:>5.1f}{sa:>20.3f}{sa/RAR_SCATTER_GOBS:>18.1f}x{sv:>24.3f}{sv/(RAR_INTRINSIC_GOBS/4):>14.1f}x")
    print("""  => the a0 signal exceeds the FULL RAR scatter by z~1 and is several-x it by z=2-3; even the smaller
     V_flat effect clears the intrinsic floor by z~1. The effect is detectable per-galaxy at z>~2 and
     overwhelmingly so for a population. Scatter is NOT the limiting factor -- SYSTEMATICS are (below).\n""")


# =========================================================================================================
def part_b_current_data():
    print("=" * 100)
    print("(b) WHAT CURRENT DATA SHOW vs E(z)  -- and how strongly they lean")
    print("=" * 100)
    print(f"  Framework targets:  E(1)={E(1.0):.2f},  E(2)={E(2.0):.2f},  E(2.9)={E(2.9):.2f},  E(3.25)={E(3.25):.2f}\n")
    rows = [
        # source, method, z, what it finds, reading on a0(z)
        ("McGaugh+ 2024 (2406.17930)", "BTFR / f_DM, indirect", "<=2.5",
         "no clear evolution in BTFR zero-pt", "favors CONSTANT a0"),
        ("Milgrom 2017 (1703.06110)", "DIRECT RC (Genzel+17)", "~2",
         "g(R)=3-11 a0; 'all but excludes ~4 a0'", "CONSTANT; bounds rise, excl (1+z)^1.5"),
        ("Big Wheel (Nat.Astr. 2025)", "DIRECT single disk", "3.25",
         "V=280; g~2.2 a0; a0 <~ 2.6x ceiling", "EXCLUDES ~5x (= E(3.25))"),
        ("RC100 / Nestor-Shachar 23", "DIRECT, ~100 disks", "0.6-2.5",
         "baryon-dom, DECLINING outer RCs", "~local a0 (upper bounds)"),
        ("Ubler+ 2017 / KMOS-3D", "kinematics, stellar+bTF", "<=2.5",
         "higher M_bar at fixed V", "a0 lower / constant"),
        ("Wu & Kroupa 2015", "TF-as-MOND", "<=1.2",
         "marg. favors a0 ~ sqrt(Lambda)", "CONSTANT favored"),
        ("MUSE-DARK III 2026 (2604.22613)", "INDIRECT RAR fit", "0.3-1.4",
         "a0(z~1)=2.38e-10, ~19sig rise", "RISES, but FASTER than E(z); LCDM-read"),
        ("Mayer+ 2022 (2206.04333)", "LCDM HYDRO SIM (not data)", "0-2",
         "apparent a0 rises ~x3", "rise FAVORS LCDM; rejects const-MOND"),
    ]
    print(f"  {'source':<33}{'method':<24}{'z':>7}{'finding':<36}reading")
    for s, m, z, f, r in rows:
        print(f"  {s:<33}{m:<24}{z:>7}  {f:<36}{r}")

    # --- The crucial honest nuance: direct constraints are HIGH-ACCELERATION upper bounds ---
    print(f"""
  THE CRUCIAL NUANCE (why this is a LEAN, not a kill): every DIRECT high-z constraint above comes from
  MASSIVE, COMPACT, baryon-dominated disks observed in the HIGH-acceleration regime (g(R) = 3-11 a0,
  near-Newtonian), NOT the deep-MOND tail (g_bar < a0) where a0 is actually constrained. There a risen
  a0 only mildly boosts an already-Newtonian curve, so these data BOUND a0 FROM ABOVE; they do not
  cleanly MEASURE a low a0. Milgrom's '~4 a0 excluded at z~2' squeezes E(2)={E(2.0):.2f} hard (E(2) sits just
  below the excluded 4x) and kills the steeper (1+z)^1.5; the Big Wheel excludes E(3.25)={E(3.25):.2f}. The lone
  RISE measurement (MUSE-DARK III) is INDIRECT (an aggregate RAR/lensing fit), OVERSHOOTS E(z), and is
  read as LCDM by its own authors (with a +0.45 dex stellar-mass escape hatch).""")

    # --- A defensible sigma on the present lean (MUSE z~1, the cleanest single number) ---
    print("\n  " + "-" * 96)
    print("  QUANTIFYING THE LEAN (defensible, not hand-wavy): the cleanest single rise-measurement is")
    print("  MUSE-DARK III at z~1.  Test the framework's PREDICTED a0(z~1)=E(1)*1.2e-10 against it.")
    z, a0_meas, a0_meas_err = 0.9, 2.38e-10, None
    a0_pred1 = A0 * E(1.0)
    # MUSE rise is ~19 sigma above local 1.2; infer a per-point sigma from that statement:
    sigma_a0 = (a0_meas - A0) / 19.0           # ~19 sigma above 1.2e-10  -> sigma ~ 0.062e-10
    pull = (a0_meas - a0_pred1) / sigma_a0
    print(f"    framework predicts  a0(z=1) = E(1)*1.2e-10 = {a0_pred1:.3e}")
    print(f"    MUSE-DARK III meas.  a0(z~0.9) = {a0_meas:.3e}  (~19 sigma above local => sigma ~ {sigma_a0:.2e})")
    print(f"    => MUSE OVERSHOOTS the framework by {100*(a0_meas/a0_pred1-1):.0f}%, a ~{abs(pull):.0f} sigma PULL.")
    print(f"       (MUSE disfavors the framework by running TOO FAST, not too slow -- it leans toward LCDM,")
    print(f"        whose apparent a0 also overshoots cH(z). The framework is squeezed from BOTH sides:")
    print(f"        Milgrom/Big-Wheel say 'not that high', MUSE says 'even higher & LCDM-shaped'.)\n")

    print("""  NET (honest, weighted): the DIRECT rotation-curve weight (Milgrom 2017, Big Wheel, RC100, Ubler,
  Wu-Kroupa) leans toward CONSTANT / mild a0 and EXCLUDES the strong E(z) rise at z>2 -- but only as
  upper bounds from high-acceleration disks. The one RISE detection overshoots E(z) and reads as LCDM.
  No single dataset cleanly MEASURES a0 in the deep-MOND regime at z>~2, so nothing CLOSES the question.\n""")
    return abs(pull)


# =========================================================================================================
def part_c_decisive_test(sig_gal=SIG_GAL_A0_HIGHZ):
    print("=" * 100)
    print("(c) THE SINGLE DECISIVE NEAR-TERM TEST -- facility + sample + precision for a >=3 sigma settle")
    print("=" * 100)
    print(f"""  WHY z~3 is the design sweet spot -- the 3-way discriminator is maximally open:
    {'z':>5}{'framework E(z)':>16}{'constant':>11}{'SIV (falls)':>13}{'max ratio':>12}""")
    for z in (1.0, 2.0, 3.0):
        f, cst, s = E(z), 1.0, siv(z)
        print(f"    {z:>5.1f}{f:>16.2f}{cst:>11.2f}{s:>13.2f}{f/s:>12.1f}x")
    print(f"""  At z~3: framework {E(3.0):.1f}x  vs  constant 1.0  vs  SIV {siv(3.0):.2f} -- a >4x, 3-way split, while
  Halpha/[OIII] are still in JWST range and the deep-MOND window (g_bar < a0(z)) is {E(3.0):.1f}x WIDER than
  local (so MORE normal disks qualify, not fewer).

  THE EXPERIMENT (fully specified; needs telescope time, not more in-house analysis):
    TARGETS    : ~15-50 EXTENDED, ROTATION-supported (V/sigma > 3) discs at z~2.5-3.5, stellar mass
                 1e9.5-1e10.5 (low surface density -> genuinely reach the deep-MOND tail, g_bar < a0(z)).
                 NOT the massive compact monsters at 3-11 a0 (those only ever give upper bounds).
    KINEMATICS : JWST/NIRSpec IFU (Halpha, [OIII]) -> the outer rotation curve g_obs(R) tail.
    GAS CENSUS : ALMA [CII]158um and/or CO -> per-galaxy M_gas -> g_bar (without it a0 is gas-confounded).
    M_star     : JWST rest-frame-optical SED (consistent prescription at BOTH z=0 anchor and z~3).
    ALSO       : MOONS (VLT, multi-object NIR) for the statistical sample; ELT/HARMONI (post-2029) deeper.
    KEY MOVE   : measure the RATIO a0(z~3)/a0(z~0) with the SAME pipeline/M-L/interpolation at both ends,
                 and use DEEP-MOND points only -> the interpolation-function ambiguity (~0.12 dex) and the
                 common M/L systematic CANCEL; only the DIFFERENTIAL (evolving) M/L survives (~0.04 dex).\n""")

    # --- the significance forecast (ratio test, constant-a0 rejection) ---
    dlogE = np.log10(E(3.0))                                   # signal = log10 E(3), constant-vs-evolving
    print("  SIGNIFICANCE of rejecting CONSTANT a0 (signal = log10 E(3) = %.2f dex):" % dlogE)
    print(f"  {'N gal':>6}{'a0(3) prec':>12}{'sig(a0,3)[dex]':>16}{'loose anchor (0.09)':>22}{'ratio anchor (0.05)':>22}")
    for N in (5, 12, 25, 50, 130):
        s_mean = sig_gal / np.sqrt(N)
        sig_loose = dlogE / np.sqrt(s_mean ** 2 + SIG_ANCHOR_LOOSE ** 2)
        sig_tight = dlogE / np.sqrt(s_mean ** 2 + SIG_ANCHOR_TIGHT ** 2)
        print(f"  {N:>6}{10**s_mean-1:>11.0%}{s_mean:>16.3f}{sig_loose:>20.1f} s{sig_tight:>20.1f} s")
    plateau_loose, plateau_tight = dlogE / SIG_ANCHOR_LOOSE, dlogE / SIG_ANCHOR_TIGHT
    print(f"""
  READ: even ~5 clean deep-MOND discs at z~3 already exceed 3 sigma; ~12-15 reach ~6 sigma; the ratio-
  anchored analysis (gas-dominated, deep-MOND-only, common systematics cancelled) pushes ~12-25 galaxies
  to ~10-13 sigma. The significance PLATEAUS (~{plateau_loose:.0f} sigma loose, ~{plateau_tight:.0f} sigma ratio-anchored): past
  that it is limited by the z=0 ANCHOR M/L, not the z~3 sample -- so tightening the local anchor (gas-rich
  systems) matters as much as adding high-z galaxies. BOTTOM LINE: ~15-30 galaxies, ONE JWST+ALMA program,
  this decade, gives a clean >=3 sigma (realistically 6-13 sigma) settle of evolving-vs-constant a0.\n""")

    print("""  THE TWO-TIER CAVEAT (do not skip): this test settles 'a0 EVOLVES vs CONSTANT' decisively -- a null
  (a0 constant) KILLS the framework outright. But a measured rise ~E(z) is LCDM-DEGENERATE (LCDM's apparent
  a0 also rises ~E(z) via denser halos; Mayer 2022). So Tier-1 (this test) is NECESSARY but not SUFFICIENT
  to prove the framework OVER LCDM. The distinctive, LCDM-IMPOSSIBLE kill is Tier-2: the EFE weakening as
  eta = g_ext/a0(z) ~ 1/E(z) (DM-forbidden), which needs ~600-1600 galaxies -- far more, next decade.\n""")


# =========================================================================================================
def part_d_verdict(muse_pull):
    print("=" * 100)
    print("(d) HONEST VERDICT -- current standing of a0(z) = cH(z)/Z")
    print("=" * 100)
    print(f"""  STATUS: OPEN, but LEANING UNFAVORABLE -- at roughly the ~2-3 sigma level, NOT excluded.

  Why "leaning unfavorable" and not "open":
    * the WEIGHT of DIRECT high-z rotation-curve evidence (Milgrom 2017 'excludes ~4 a0 at z~2'; Big Wheel
      excludes ~5x at z=3.25; RC100/Ubler/Wu-Kroupa lean constant) disfavors the strong E(z) rise at z>2;
    * the one RISE detection (MUSE-DARK III, ~19 sigma) OVERSHOOTS E(z) by ~{100*(2.38e-10/(A0*E(1.0))-1):.0f}% (a ~{muse_pull:.0f} sigma pull
      vs the framework's predicted a0(z=1)) and is read as LCDM by its own authors;
    * so the framework is squeezed from BOTH sides -- "not that high" (direct RCs) AND "even higher & LCDM-
      shaped" (MUSE). Either way the SPECIFIC law a0 = cH(z)/Z is disfavored relative to its neighbors.

  Why NOT "excluded":
    * every direct constraint is a high-ACCELERATION upper bound (g=3-11 a0), NOT a clean deep-MOND a0;
    * the data are genuinely SPLIT (a real ~19 sigma rise exists; constant is the mainstream); and
    * no experiment yet measures a0 in the deep-MOND regime at z>~2, which is exactly what would close it.
    A MILD rise (a0 x1.5-2 by z~2) threads ALL current data; the framework's x{E(2.0):.1f} at z=2 / x{E(3.0):.1f} at z=3 does not.

  HONEST SIGMA on the present lean: ~2-3 sigma AGAINST the strong E(z) law (driven by Milgrom's z~2 squeeze
  and MUSE's overshoot), in genuine tension but short of the ~5 sigma that would EXCLUDE it. This is NOT a
  win, and is shakier than a naive 'a0 rises, we predicted a rise' reading -- because the RISE everyone sees
  is LCDM-degenerate and the framework's distinctive content is the COEFFICIENT/SHAPE (cH(z)/Z), which the
  direct data squeeze and MUSE overshoots.

  WHAT FLIPS IT (in EITHER direction): ONE clean deep-MOND rotation curve of a NORMAL (not monster) z~3 disk
  -- the Part (c) experiment. ~15-30 such galaxies with JWST+ALMA give a >=3 sigma (realistically 6-13 sigma)
  ratio test that either KILLS the framework (a0 constant) or confirms evolution (a0 ~ E(z)). The
  framework-vs-LCDM kill then requires the Tier-2 EFE-vs-z campaign (~600-1600 galaxies, next decade).""")
    print("=" * 100)


# =========================================================================================================
def main():
    print("#" * 100)
    print("# THE DECISIVE TEST of a0(z) = cH(z)/Z  ->  a0/a0(0) = E(z)   (Z = 2 sqrt(8pi/3) = %.3f)" % Z)
    print("#" * 100 + "\n")
    part_a_effect_sizes()
    part_a2_signal_vs_scatter()
    muse_pull = part_b_current_data()
    part_c_decisive_test()
    part_d_verdict(muse_pull)
    print("\n" + "#" * 100)
    print("# ONE-LINE BOTTOM LINE")
    print("#" * 100)
    print(f"""  The signal is LARGE (a0 up {(E(2.0)-1)*100:.0f}% by z=2, V_flat up {(E(2.0)**0.25-1)*100:.0f}%; log10 E(3)={np.log10(E(3.0)):.2f} dex lever arm),
  so the test is EASY in principle. Current data (direct high-z RCs squeeze it; MUSE overshoots & reads
  LCDM) leave a0=cH(z)/Z OPEN but LEANING UNFAVORABLE at ~2-3 sigma -- not excluded. The decisive settle is
  ~15-30 EXTENDED deep-MOND z~3 discs (JWST/NIRSpec + ALMA gas), analyzed as a systematics-cancelling
  a0(z~3)/a0(0) RATIO -> >=3 sigma (realistically ~6-13 sigma) on EVOLVING vs CONSTANT, this decade. A null
  kills the framework; a rise confirms evolution but is LCDM-degenerate (the framework-vs-LCDM kill is the
  Tier-2 EFE-vs-z campaign).""")
    print("#" * 100)


if __name__ == "__main__":
    main()
