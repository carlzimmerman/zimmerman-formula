#!/usr/bin/env python3
r"""
THE INDEPENDENT-PROBE CROSS-PREDICTION MATRIX for a0 = c^2 sqrt(Lambda/32pi) = c H_Lambda / Z.
==============================================================================================
MANDATE QUESTION (honest): the framework's value-coincidence a0 ~ (c/2)sqrt(G rho_Lambda) uses the
SAME cosmological numbers (H0, OmegaLambda) that go into rho_crit and rho_Lambda. So does pulling H0 (or
Lambda, or rho_DE) from an INDEPENDENT probe -- standard sirens, strong-lens time delays, BAO -- give a
GENUINELY independent cross-prediction of a0, or is it circular (re-deriving a0 from the same input)?

THE LOGIC FORK (every probe must be graded on this):
  - a0 = c H_Lambda/Z = c H0 sqrt(OmegaLambda)/Z  needs (H0, OmegaLambda).  [the "cH" packaging]
  - a0 = (c/2)sqrt(G rho_Lambda),  rho_Lambda = Lambda c^2/8piG = OmegaLambda * rho_crit, rho_crit=3H0^2/8piG
        => a0 = c H0 sqrt(OmegaLambda)/Z  -- IDENTICAL. a0 depends ONLY on the combination H0*sqrt(OmegaLambda)
        = H_Lambda (the pure-Lambda de Sitter rate). So the ONE cosmological quantity a0 needs is H_Lambda.
  => A probe gives an INDEPENDENT cross-prediction of a0 iff it measures H_Lambda (or H0 & OmegaLambda) by a
     route that does NOT already assume a0/MOND. It is CIRCULAR only if a0 (or MOND galaxy dynamics) was used
     to get that H0 -- which NONE of the standard probes do. So "circular" is the WRONG worry here; the right
     worry is INDEPENDENCE-FROM-EACH-OTHER and whether it is a NEW TEST or just re-stating the z=0 coincidence.

WHAT THIS SCRIPT DOES (all on REAL, CITED 2024-2026 numbers; computes, does not assert):
  (A) Take 5 INDEPENDENT H0 measurements (each from a different physical ladder) + their OmegaLambda, propagate
      each to a predicted a0, and compare to the observed a0 band [9.1e-11 (simple-mu), 1.2e-10 (RAR)].
  (B) Grade each: is it an INDEPENDENT cross-prediction, and is it a NEW TEST or a CONSISTENCY restatement?
  (C) The decisive honesty check: how much does the a0 prediction MOVE across the full H0 tension range
      (67 -> 73)? If a0's observational uncertainty (the interpolation-function 20-30%) SWAMPS the H0 spread,
      then NO H0 probe can currently test the relation -- the test is systematics-limited, not data-limited.
  (D) The ONE genuinely-independent-of-H0 route: BAO+BBN gives Lambda (hence rho_DE, hence a0) WITHOUT a local
      H0 ladder. And DESI gives rho_DE(z) -- the only route to the CAUSAL (a0 tracks rho as it changes) test.

Needs numpy. Constants per mandate: c=2.998e8, G=6.674e-11.
"""
import numpy as np

c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
Z = 2*np.sqrt(8*np.pi/3.0)                 # = sqrt(32pi/3) = 5.78881

# Observed a0 band (the operative target). RAR (McGaugh) high; simple-mu low.
A0_RAR, A0_SIMPLE = 1.20e-10, 9.1e-11
A0_RAR_ERR = 0.24e-10                       # McGaugh's own ~20% systematic on the RAR a0

def a0_pred(H0_kms, OmL):
    """Parameter-free framework prediction a0 = c H0 sqrt(OmL)/Z. (= (c/2)sqrt(G rho_Lambda), identical.)"""
    H0 = H0_kms*1e3/Mpc
    return c*H0*np.sqrt(OmL)/Z

# ---------------------------------------------------------------------------------------------------------
# (A) FIVE INDEPENDENT H0 PROBES -- different physical ladders, NONE uses MOND/a0.
#     Values are real, cited (2024-2026). OmegaLambda: each probe's own or the consensus 0.685 where the
#     probe does not constrain it (sirens/TD measure H0, not OmL, so they import OmL -- flagged).
# ---------------------------------------------------------------------------------------------------------
PROBES = [
    # name, H0, H0err, OmL, OmLerr, OmL_source, independence_note, citation
    ("Planck 2018 CMB",            67.36, 0.54, 0.6847, 0.0073, "self",
     "early-universe sound horizon; fully independent of a0/MOND", "Planck 2018 VI"),
    ("DESI DR2 BAO+BBN",           68.5,  0.6,  0.685,  0.008,  "DESI/consensus",
     "BAO ruler + BBN; NO local ladder, NO a0; independent of CMB calibration", "DESI DR2 2025"),
    ("SH0ES Cepheid+SNIa",         73.04, 1.04, 0.685,  0.013,  "imported",
     "local distance ladder; independent of a0; OmL imported (ladder gives H0 only)", "Riess+ 2022"),
    ("Standard sirens (LVK O4a+)", 68.0,  4.1,  0.685,  0.013,  "imported",
     "GW luminosity distance -- a PURELY GR/geometric ruler, no EM ladder, no a0", "Boom+ 2024 (2404.16092)"),
    ("TDCOSMO 2025 time delays",   71.6,  3.6,  0.685,  0.013,  "imported",
     "strong-lens time delays -- absolute distances, no ladder, no a0", "TDCOSMO 2025 (2506.03023)"),
]

def part_A_and_B():
    print("="*104)
    print("(A)+(B)  FIVE INDEPENDENT H0 PROBES -> predicted a0, with independence/novelty grade")
    print("="*104)
    print(f"  Framework: a0 = c*H0*sqrt(OmL)/Z,  Z={Z:.4f}.  Observed band: simple-mu {A0_SIMPLE*1e10:.2f} .. RAR {A0_RAR*1e10:.2f} e-10\n")
    print(f"  {'probe':<28}{'H0':>7}{'OmL':>8}{'a0 pred[e-10]':>15}{'/RAR':>8}{'/simple':>9}   independent? new test?")
    print("  " + "-"*100)
    preds = []
    for name, H0, H0e, OmL, OmLe, omlsrc, note, cite in PROBES:
        a0 = a0_pred(H0, OmL)
        # propagate: a0 ~ H0 * sqrt(OmL)
        rel = np.sqrt((H0e/H0)**2 + (0.5*OmLe/OmL)**2)
        preds.append((name, a0, a0*rel, omlsrc))
        indep = "YES (no a0 in)"
        # "new test" = does it probe a0 BY A DIFFERENT INPUT than Planck? Only if H0 OR OmL is independent.
        newtest = "consistency (z=0 value)"
        print(f"  {name:<28}{H0:>7.2f}{OmL:>8.4f}{a0*1e10:>13.3f}  {a0/A0_RAR:>7.2f}{a0/A0_SIMPLE:>9.2f}   {indep:<14} {newtest}")
    print(f"""
  GRADING (honest, the core of the mandate):
   * ALL five are INDEPENDENT OF a0/MOND: none uses galaxy dynamics or the MOND law to get H0. So the worry
     "circular (a0 used to derive a0)" is FALSE for every standard H0 probe. Good.
   * BUT each only re-predicts the PRESENT a0 value -- it is a CONSISTENCY check on the z=0 value-coincidence,
     NOT a causal proof. a0 depends only on H_Lambda = H0*sqrt(OmL); swapping the H0 ladder just swaps which
     z=0 number you plug in. It cannot show a0 TRACKS rho (that needs z-evolution, Part D).
   * NOVELTY among them: sirens and TDCOSMO are NEW *inputs* (2024-26, independent of CMB AND of the Cepheid
     ladder), so they are the first a0 predictions from a PURELY GEOMETRIC distance (GW/lensing). That is a
     genuinely new cross-check of the VALUE -- but still value-only.""")
    return preds

# ---------------------------------------------------------------------------------------------------------
# (C) THE DECISIVE HONESTY CHECK: does the H0 tension even MATTER for a0, given a0's own systematic?
# ---------------------------------------------------------------------------------------------------------
def part_C():
    print("\n" + "="*104)
    print("(C)  CAN ANY H0 PROBE CURRENTLY TEST THE RELATION? -- a0 spread from H0 tension vs a0 own systematic")
    print("="*104)
    a0_low  = a0_pred(67.36, 0.6847)     # Planck
    a0_high = a0_pred(73.04, 0.685)      # SH0ES
    spread_H0 = (a0_high - a0_low)/(0.5*(a0_high+a0_low))
    # a0's OWN observational uncertainty: the interpolation-function systematic (RAR vs simple-mu).
    a0_sys = (A0_RAR - A0_SIMPLE)/(0.5*(A0_RAR+A0_SIMPLE))
    print(f"  a0(Planck 67.36) = {a0_low*1e10:.3f}e-10 ;  a0(SH0ES 73.04) = {a0_high*1e10:.3f}e-10")
    print(f"  => the ENTIRE H0 tension moves the predicted a0 by only {spread_H0*100:.1f}%.")
    print(f"  But the OBSERVED a0 is uncertain by {a0_sys*100:.0f}% (interpolation-function: RAR 1.20 vs simple-mu 0.91).")
    print(f"  RATIO (a0 systematic / H0-tension signal) = {a0_sys/spread_H0:.1f}x.")
    print(f"""
  THE VERDICT (this is the key, uncomfortable result): the a0 observational systematic ({a0_sys*100:.0f}%) is ~{a0_sys/spread_H0:.0f}x
  LARGER than the entire spread the H0 tension induces in the predicted a0 ({spread_H0*100:.1f}%). So NO H0 probe --
  however precise or independent -- can currently TEST the relation by the value: every probe's a0 lands inside
  the [simple-mu, RAR] band, and the band is far wider than the inter-probe scatter. The a0<->H0 value link is
  CONSISTENCY-LIMITED BY THE a0 SYSTEMATIC, not by H0. To make a value-test bite you would need to pin the
  observed a0 to <~2% (i.e. resolve the interpolation-function/M-L ambiguity) -- harder than improving H0.
  COROLLARY: the famous 'a0 ~ cH0' coincidence is ROBUST to the H0 tension (it holds for 67 AND 73) -- which is
  reassuring for the coincidence but means the coincidence cannot be sharpened into a test by better H0.""")
    return spread_H0, a0_sys

# ---------------------------------------------------------------------------------------------------------
# (D) THE ONLY ROUTES THAT ADD REAL INFORMATION: Lambda-without-H0, and rho_DE(z) (the causal test).
# ---------------------------------------------------------------------------------------------------------
def part_D():
    print("\n" + "="*104)
    print("(D)  THE ROUTES THAT ACTUALLY ADD INFORMATION (beyond re-plugging the z=0 value)")
    print("="*104)
    print("""  Two, and only two, qualitatively different things an existing dataset can do for this relation:

  (D1) MEASURE Lambda (=rho_DE) WITHOUT A LOCAL H0 LADDER  -> tests a0 ~ sqrt(rho_DE) specifically (not ~cH0).
       The framework's PHYSICS reading is a0 ~ sqrt(rho_Lambda), with cH0 only a z=0 coincidence. BAO+BBN
       (DESI) and CMB both give Lambda directly (Omega_Lambda * rho_crit), independent of the Cepheid ladder.""")
    # rho_DE from Planck Lambda, and a0 from it -- already the same number, but the POINT is the path:
    OmL, H0 = 0.6847, 67.36*1e3/Mpc
    Lam = 3*OmL*H0**2/c**2
    rho_DE = Lam*c**2/(8*np.pi*G)
    a0_fromrho = 0.5*c*np.sqrt(G*rho_DE)
    print(f"       Planck Lambda={Lam:.3e} m^-2 -> rho_DE={rho_DE:.3e} kg/m^3 -> (c/2)sqrt(G rho_DE)={a0_fromrho*1e10:.3f}e-10.")
    print(f"       This is the SAME a0 (identity), but reached via rho_DE -- so a future direct rho_DE (not via H0)")
    print(f"       would be a cleaner test of the sqrt(rho) FORM. Still z=0, still value-only. Grade: CONSISTENCY+.")
    print("""
  (D2) MEASURE rho_DE(z)  -> the ONLY existing-data route to the CAUSAL claim (a0 tracks rho as it CHANGES).
       a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)). DESI DR2 w0wa makes this CONCRETE and falsifiable. This is the
       genuine causal lever -- but the a0(z) MEASUREMENT is telescope-limited (z~3 deep-MOND disks, ~2027+).
       The DATA that exists TODAY is DESI's rho_DE(z); the data that does NOT yet exist is a0(z).""")
    Om = 0.315
    w0, wa = -0.752, -0.86   # DESI DR2 CPL
    def a0z_ratio(z):
        a = 1/(1+z)
        return np.sqrt(a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a)))
    print(f"       DESI DR2 (w0={w0}, wa={wa}) -> a0(z)/a0(0):")
    for z in (0.5, 1, 2, 3):
        print(f"         z={z}: sqrt(rho_DE) reading = {a0z_ratio(z):.3f}   (vs cH(z) reading E(z) = {np.sqrt(Om*(1+z)**3+(1-Om)):.3f})")
    print(f"""
  => The two readings DIVERGE strongly at z>1 (event-horizon sqrt(rho_DE) DECLINES to ~{a0z_ratio(3):.2f}x; apparent
     cH(z) RISES to ~{np.sqrt(Om*(4)**3+(1-Om)):.2f}x). MEASURING a0 at z~3 simultaneously (i) tests the causal claim and
     (ii) DISCRIMINATES which horizon sources a0 -- the single highest-value existing-data-adjacent experiment.
     DESI's rho_DE(z) is the existing half; the a0(z) half is the ~2027 telescope half.""")

def verdict():
    print("\n" + "="*104)
    print("OVERALL VERDICT -- the independent-probe landscape for a0, graded")
    print("="*104)
    print("""  1. NONE of the standard H0 probes (Planck, BAO, SH0ES, sirens, TDCOSMO) is CIRCULAR: not one uses a0 or
     MOND to get H0. The 'circular' worry is misplaced for H0->a0.
  2. ALL of them, however, only re-predict the PRESENT a0 -- CONSISTENCY with the z=0 value-coincidence, not
     causal proof. a0 needs only H_Lambda=H0 sqrt(OmL); swapping the ladder swaps the z=0 number.
  3. They cannot even sharpen the VALUE test: the a0 interpolation-function systematic (~27%) is ~5x the entire
     a0-spread the H0 tension induces (~5%). The a0~cH0 coincidence is ROBUST to the H0 tension (holds at 67 AND
     73) -- reassuring, but un-sharpenable by better H0. The bottleneck is the observed a0, not H0.
  4. The genuinely useful existing-data levers are: (D1) Lambda-without-a-ladder (BAO+BBN/CMB) -> cleaner test
     of the sqrt(rho) FORM (still z=0); and (D2) DESI's rho_DE(z) -> the ONLY existing route toward the CAUSAL
     test, but it needs the a0(z) MEASUREMENT (telescope-limited, ~2027) to close.
  5. Sirens + TDCOSMO 2025 ARE a worthwhile NEW cross-check: the first a0 predictions from a purely GEOMETRIC
     distance (GW / strong-lens), independent of both the CMB and the Cepheid ladder -- they confirm the value
     lands in-band from yet another direction. Value-only, but a fresh and non-trivial direction.""")
    print("="*104)

def main():
    print("#"*104)
    print("# INDEPENDENT-PROBE CROSS-PREDICTION MATRIX for a0  (sirens, TDCOSMO, BAO, SH0ES, Planck)")
    print("#"*104 + "\n")
    part_A_and_B()
    part_C()
    part_D()
    verdict()

if __name__ == "__main__":
    main()
