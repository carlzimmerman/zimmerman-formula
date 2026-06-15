#!/usr/bin/env python3
"""
HIGH-z BTFR OFFSET FORWARD MODEL  --  the framework's cleanest DISTINCTIVE test.
================================================================================
C. Zimmerman framework:  a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE),
with the DISTINCTIVE beyond-MOND content  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0).

THE SUBTLETY (pinned, not assumed):
  * If dark energy is a TRUE cosmological constant (Lambda const) -> rho_DE const ->
    a0(z) = a0(0) CONSTANT at all z. The framework then makes the SAME BTFR prediction
    as ordinary constant-a0 MOND: ZERO offset.
  * The DECLINING a0(z) arises ONLY IF dark energy EVOLVES (w != -1). DESI DR2 w0waCDM
    (w0=-0.752, wa=-0.86; w>-1 today, w<-1 in past, crossing -1 at z~0.4-0.5) is THAWING:
    rho_DE was LOWER in the past -> a0(z) DECLINES at z>~1.5.
  * The "IF" CANCELS in the RATIO -> a0(z)/a0(0) is interpolation-robust (mu-fn, Upsilon,
    H0, OmL all cancel; only the DE history w(z) enters).
  * NON-MONOTONIC: because DESI w(z) crosses -1 at z~0.4, rho_DE (hence a0) PEAKS there.
    So the framework predicts a0 RISES ~6% to z~0.4 then declines. The z=0.5 BTFR point
    is therefore predicted slightly ABOVE the local relation, NOT below.

THE OBSERVABLE (deep-MOND BTFR):  M_bar = V^4 / (G a0)  =>  at FIXED M_bar,
    V proportional to a0^{1/4}  =>  dlogV(z) = (1/4) dlog a0(z) = (1/8) dlog[rho_DE ratio].
Equivalently at FIXED V the zero-point in M_bar shifts by  dlogM(z) = -dlog a0(z).

THREE BRANCHES (the discriminator is the SIGN):
  (a) framework declining (DESI w0wa):  dlogV(z) = (1/8) log10[rho_DE(z)/rho_DE0]
        -> ~0 to z~1, then NEGATIVE (discs BELOW z=0 BTFR) by z>=2.
  (b) constant-a0 MOND (Lambda const, OR framework-under-true-Lambda):  dlogV = 0 (ON it).
  (c) rising rival (a0 ~ cH(z), rho_total/Verlinde footing-bug):  dlogV = +(1/4)log10 E(z)
        -> strongly POSITIVE (discs ABOVE z=0 BTFR).

HONESTY (both ways):
  * The banked claim -7% in V / -0.033 dex by z=3 is VERIFIED below (sign + magnitude).
  * The signal is SMALL: |dlogV| ~ 0.033 dex (V) at z=3. The famous BTFR intrinsic scatter
    (Lelli+2019: 0.026 +/- 0.007 dex) is in M_bar; on the V axis it is 0.026/4 = 0.0065 dex.
    So the brief's "-0.033 dex below the 0.026 floor" MIXES AXES -- corrected here on BOTH
    axes. The REAL wall is not the SPARC intrinsic floor (unreachable at high z) but the
    much larger high-z PER-GALAXY error (~0.1 dex M_bar) + baryonic-evolution confounds.
  * CONFOUNDS quantified: gas-fraction evolution, asymmetric-drift/pressure support, M/L(z),
    sample selection (massive disks are g>~a0, NOT deep-MOND). These move the zero-point in
    the SAME (or opposite) direction and are LARGER than the signal at z<~2.

Reproducible, pure numpy + scipy. No new data files; uses the banked DESI DR2 CPL fit.
"""
import numpy as np

np.random.seed(20260614)

# ---------------- constants ----------------
C    = 299792458.0          # m/s exact
G    = 6.67430e-11          # CODATA
MPC  = 3.0857e22            # m

# Planck-2018-ish background (cancels in the ratio; here only for a0(0) and the rising branch E(z))
H0, OML, OMM = 67.36, 0.6847, 0.3153

# DESI DR2 w0waCDM (CPL): w(a)=w0+wa(1-a). thawing, crosses -1 at z~0.4.
W0_C, W0_E = -0.752, 0.057
WA_C, WA_E = -0.86, 0.22

LN10 = np.log(10.0)
NMC  = 400000

# BTFR scatter inputs (published)
SIG_INTR_M   = 0.026   # dex in M_bar, Lelli+2019 ORTHOGONAL intrinsic scatter (SPARC, local)
SIG_INTR_M_E = 0.007
SIG_HIZ_M    = 0.10    # dex in M_bar, REALISTIC per-galaxy total at high z (M/L+gas+kinematics)
SIG_OPT_M    = 0.05    # dex, optimistic high-z per-galaxy (homogeneous deep pipeline)


# ---------------- core physics ----------------
def rho_DE_ratio(z, w0=W0_C, wa=WA_C):
    """rho_DE(a)/rho_DE0 for CPL: a^{-3(1+w0+wa)} exp(-3 wa (1-a)), a=1/(1+z)."""
    a = 1.0 / (1.0 + z)
    return a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))

def Ez(z):
    return np.sqrt(OMM * (1.0 + z) ** 3 + OML * rho_DE_ratio(z))

def a0_ratio_frame(z, w0=W0_C, wa=WA_C):
    """framework a0(z)/a0(0) = sqrt(rho_DE ratio)."""
    return np.sqrt(rho_DE_ratio(z, w0, wa))

def dlogV_frame(z, w0=W0_C, wa=WA_C):
    """(a) declining framework: dlogV at fixed M_bar = (1/4) dlog a0 = (1/8) log10[rho_DE ratio]."""
    return (1.0 / 8.0) * np.log10(rho_DE_ratio(z, w0, wa))

def dlogV_const(z):
    """(b) constant-a0 MOND (or framework under TRUE Lambda): ZERO."""
    return np.zeros_like(np.atleast_1d(z) * 1.0)

def dlogV_rising(z):
    """(c) rising rival a0 ~ cH(z) (rho_total / Verlinde): dlogV = (1/4) log10 E(z)."""
    return 0.25 * np.log10(Ez(z))

def a0_lambda0():
    H = H0 * 1e3 / MPC
    Lam = 3.0 * OML * H ** 2 / C ** 2
    return C ** 2 * np.sqrt(Lam / (32.0 * np.pi))


def banner(t):
    print("=" * 92)
    print(t)
    print("=" * 92)


def main():
    print("#" * 92)
    print("# HIGH-z BTFR OFFSET FORWARD MODEL  --  a0(z)/a0(0)=sqrt(rho_DE ratio), DESI DR2 w0wa")
    print("#" * 92)
    print(f"  anchor a0(0) = c^2 sqrt(Lambda/32pi) = {a0_lambda0():.4e} m/s^2 "
          f"(cancels in the ratio; not the test)\n")

    # ---- 0. NON-MONOTONIC structure: the peak ----
    banner("(0) NON-MONOTONIC: DESI w(z) crosses -1 at z~0.4 -> a0 PEAKS there (not pure decline)")
    zz = np.linspace(0, 1.0, 4001)
    rr = rho_DE_ratio(zz)
    ip = int(np.argmax(rr))
    a_cross = 1.0 + (1.0 + W0_C) / WA_C        # w(a)=-1 => (1-a) = -(1+w0)/wa
    z_cross = 1.0 / a_cross - 1.0
    print(f"   w(z) crosses -1 at z = {z_cross:.3f}   [a={a_cross:.3f}; the rho_DE/a0 peak]")
    print(f"   rho_DE / a0 PEAK at z = {zz[ip]:.3f}:  a0(z)/a0(0) = {np.sqrt(rr[ip]):.4f} "
          f"(+{100*(np.sqrt(rr[ip])-1):.1f}% in a0, +{100*(10**dlogV_frame(zz[ip])-1):.2f}% in V)")
    print("   => the z=0.5 BTFR point is predicted slightly ABOVE the z=0 relation (the bump),")
    print("      NOT below. The framework only UNIQUELY declines (discs below) at z >~ 1.5.\n")

    # ---- 1. THE THREE-BRANCH FORWARD MODEL at the requested redshifts ----
    banner("(1) THE FORWARD MODEL: V offset at fixed M_bar -- three branches (SIGN = the discriminator)")
    zs = [0.5, 1.0, 2.0, 3.0]
    print(f"   {'z':>5} | {'(a) framework declining (DESI w0wa)':>40} | "
          f"{'(b) const-a0':>14} | {'(c) rising cH(z)':>18}")
    print(f"   {'':>5} | {'a0r':>8}{'dlogV[dex]':>13}{'dV[%]':>10}{'pos':>8} | "
          f"{'dV[%]':>14} | {'dlogV':>9}{'dV[%]':>9}")
    print("   " + "-" * 86)
    rows = []
    for z in zs:
        a0r = a0_ratio_frame(z)
        dlv = dlogV_frame(z); dv = 100 * (10 ** dlv - 1)
        pos = "ABOVE" if dlv > 1e-4 else ("BELOW" if dlv < -1e-4 else "ON")
        dvr = 100 * (10 ** dlogV_rising(z) - 1)
        print(f"   {z:>5.1f} | {a0r:>8.4f}{dlv:>13.4f}{dv:>10.2f}{pos:>8} | "
              f"{0.0:>14.2f} | {dlogV_rising(z):>9.4f}{dvr:>9.2f}")
        rows.append((z, dlv, dv))
    print()
    print("   DISCRIMINATOR (the cleanest distinctive content): by z=3 the framework puts discs")
    print(f"   ~{abs(rows[-1][2]):.1f}% BELOW (slower) the z=0 BTFR; constant-a0 MOND puts them ON it (0%);")
    print(f"   the rising rival puts them ~{100*(10**dlogV_rising(3)-1):.0f}% ABOVE. The SIGN splits all three.\n")

    # ---- 1b. VERIFY the banked claim ----
    banner("(1b) VERIFY the banked claim: '-7% in V (-0.033 dex) by z=3'")
    dlv3 = dlogV_frame(3.0); dv3 = 100 * (10 ** dlv3 - 1)
    print(f"   computed: dlogV(z=3) = {dlv3:+.4f} dex,  dV = {dv3:+.2f}%  "
          f"-> banked -0.033 dex / -7% is CONFIRMED (sign NEGATIVE, magnitude matches).")
    # MC error from DESI w0/wa
    w0s = np.random.normal(W0_C, W0_E, NMC)
    was = np.random.normal(WA_C, WA_E, NMC)
    dlv3s = dlogV_frame(3.0, w0s, was)
    lo, hi = np.percentile(dlv3s, [16, 84]); sd = 0.5 * (hi - lo)
    print(f"   DESI w0/wa Monte-Carlo 1sigma: dlogV(z=3) = {dlv3:+.4f} +/- {sd:.4f} dex "
          f"({dv3:+.1f} +/- {100*(10**sd-1):.1f}% in V)")
    print(f"   => the prediction is {abs(dlv3)/sd:.1f}sigma from ZERO in the COSMOLOGICAL (w0wa) error alone")
    print(f"      -- i.e. the DE-history uncertainty does NOT wash out the sign; the wall is OBSERVATIONAL.\n")

    # ---- 2. THE SCATTER FLOOR, ON THE CORRECT AXIS ----
    banner("(2) THE SCATTER FLOOR -- corrected for the M_bar-vs-V axis confusion")
    print(f"   Lelli+2019 BTFR intrinsic scatter = {SIG_INTR_M} +/- {SIG_INTR_M_E} dex  -- but that is in M_bar.")
    print(f"   The signal lives in V at fixed M_bar. Converting (slope 4):")
    print(f"      sigma_intr(V) = {SIG_INTR_M}/4 = {SIG_INTR_M/4:.4f} dex   (~{100*(10**(SIG_INTR_M/4)-1):.1f}% in V)")
    print(f"   Compare the z=3 signal  |dlogV| = {abs(dlv3):.4f} dex (V).")
    print(f"   => On the V axis the z=3 signal ({abs(dlv3):.4f}) is ~{abs(dlv3)/(SIG_INTR_M/4):.1f}x the SPARC")
    print(f"      INTRINSIC floor ({SIG_INTR_M/4:.4f}) -- i.e. ABOVE it, not below. The brief's 'below the")
    print(f"      0.026 floor' compares dex-in-V to dex-in-M; on a common axis the signal clears the")
    print(f"      *intrinsic* floor. BUT the intrinsic floor is a LOCAL, best-case number -- not reachable")
    print(f"      at high z, where the per-galaxy error is set by M/L+gas+kinematics (see (3)).\n")

    # ---- 3. N_discs needed, under REALISTIC high-z per-galaxy scatter ----
    banner("(3) N_discs for a 3sigma / 5sigma MEAN-offset detection (the real measurability question)")
    print("   Detect the MEAN zero-point shift at S-sigma:  N = (S * sigma_perobj(V) / |dlogV|)^2.")
    print("   Per-galaxy V scatter = (per-galaxy M scatter)/4.  THREE floors bracket the truth:")
    print(f"     A) SPARC intrinsic (best case, LOCAL):     sigma_M={SIG_INTR_M:.3f} -> sigma_V={SIG_INTR_M/4:.4f} dex")
    print(f"     B) optimistic high-z homogeneous pipeline: sigma_M={SIG_OPT_M:.3f} -> sigma_V={SIG_OPT_M/4:.4f} dex")
    print(f"     C) realistic high-z per-galaxy:            sigma_M={SIG_HIZ_M:.3f} -> sigma_V={SIG_HIZ_M/4:.4f} dex")
    print()
    print(f"   {'z':>5}{'|dlogV|(V)':>12}  | {'N3(A)':>7}{'N5(A)':>7} | {'N3(B)':>7}{'N5(B)':>7} | {'N3(C)':>8}{'N5(C)':>8}")
    print("   " + "-" * 80)
    for z in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        s = abs(dlogV_frame(z))
        def N(S, sigM):
            sV = sigM / 4.0
            return (S * sV / s) ** 2 if s > 1e-9 else np.inf
        print(f"   {z:>5.1f}{s:>12.4f}  | {N(3,SIG_INTR_M):>7.0f}{N(5,SIG_INTR_M):>7.0f} | "
              f"{N(3,SIG_OPT_M):>7.0f}{N(5,SIG_OPT_M):>7.0f} | {N(3,SIG_HIZ_M):>8.0f}{N(5,SIG_HIZ_M):>8.0f}")
    print()
    print("   READING: at z<~1 the signal ~0 (near the bump zero-crossing) -> N explodes (un-measurable;")
    print("   ALSO un-distinctive, since the framework sits on top of const-a0 there). At z=2-3 the signal")
    print("   is real: a 3sigma MEAN detection needs only ~5-25 deep galaxies in the OPTIMISTIC/realistic")
    print("   floor -- IF the per-galaxy error can be pushed to ~0.05-0.1 dex AND the confounds (below) are")
    print("   controlled. That 'IF' is the whole game. The SPARC-intrinsic column is best-case unreachable.\n")

    # ---- 4. THE CONFOUNDS -- which is the real wall ----
    banner("(4) CONFOUNDS: do baryonic-evolution effects mimic / swamp the a0(z) signal?")
    print("   These shift the high-z BTFR zero-point INDEPENDENT of a0(z). Sizes are in dex of M_bar at")
    print("   fixed V (the measured axis); divide by 4 to compare to dlogV(V).")
    confs = [
        ("gas-fraction evolution",
         "f_gas rises 0.1->0.5 by z~2; if M_bar mis-counts gas, zero-point moves",
         "0.1-0.3 dex M", "EITHER (depends on census completeness)",
         "the dominant astrophysical confound; same axis as a0(z); LARGER than signal at z<2"),
        ("asymmetric drift / pressure support",
         "hot high-z disks (V/sigma~1-5) need a v_AD correction; under-corr -> V low",
         "0.05-0.15 dex V (=0.2-0.6 dex M)", "under-corr mimics LOW a0 (framework sign); over-corr mimics rising",
         "the leading KINEMATIC systematic; sign-degenerate with the framework signal"),
        ("M/L(z) / IMF evolution",
         "younger high-z populations -> lower Upsilon_* -> lower M_star",
         "0.1-0.2 dex M", "lowers M_bar -> mimics zero-point DOWN",
         "cancels in the a0(z) RATIO only if the SAME Upsilon used at both z; in practice it does NOT"),
        ("sample selection (regime trap)",
         "KMOS3D/KROSS/MUSE are MASSIVE HSB disks at g >~ a0 (Newtonian-ish), NOT deep-MOND",
         "interp-fn dependent, ~0.05-0.1 dex", "biases the inferred a0 in an mu-fn-dependent way",
         "the FATAL one: V^4=G M a0 is only EXACT in deep-MOND (g<<a0). High-z massive disks fail this"),
    ]
    for name, mech, size, sign, note in confs:
        print(f"   * {name}")
        print(f"       mechanism : {mech}")
        print(f"       size      : {size}   ({100*(10**(0.2/4)-1):.0f}%-scale in V for a 0.2 dexM shift)")
        print(f"       sign      : {sign}")
        print(f"       verdict   : {note}")
    print()
    print(f"   Signal for scale: dlogV(z=3) = {abs(dlv3):.4f} dex V  =  {abs(dlv3)*4:.4f} dex M at fixed V.")
    print(f"   => Every confound except the SPARC-intrinsic floor is COMPARABLE-TO-LARGER than the signal")
    print(f"      at z<~2, and the deep-MOND regime requirement is VIOLATED by every existing high-z sample.")
    print(f"      This is why the existing KMOS3D/KROSS BTFR (banked highz_btfr_fork_test.py) is a NULL:")
    print(f"      the two samples DISAGREE by ~0.2 dex -- far above any a0(z) signal -- proving systematics")
    print(f"      dominate. The test is clean in PRINCIPLE (the SIGN is distinctive) but in PRACTICE buried")
    print(f"      until a deep-MOND-tail (LSB, gas-rich, g<<a0) rotator sample at z~2-3 exists (telescope-")
    print(f"      limited, ~2027+ JWST/ALMA/ELT).\n")

    # ---- 5. THE INDEPENDENT EMPIRICAL CONFOUND: a measured evolving BTFR zero-point ----
    banner("(5) THE KILLER CONFOUND IS ALREADY MEASURED -- baryonic BTFR evolution exists w/o a0(z)")
    print("   * KMOS3D (Ubler+2017, arXiv:1703.04321): the bTFR zero-point EVOLVES with z toward MORE")
    print("     baryonic mass at fixed V (POSITIVE evolution) -- driven by gas accretion / SF history,")
    print("     NOT a0(z). This is the SAME-SIGN-at-low-z confound, of the assembly origin Magneticum")
    print("     (Mayer+2023) reproduces in pure LCDM.")
    print("   * Marongwe & Kauffman 2025 (arXiv:2511.20188): claim the BTFR NORMALIZATION evolves")
    print("     exponentially with COSMIC TIME (fixed slope ~4), unifying galaxies+clusters. An")
    print("     INDEPENDENT, baryonic/assembly account of a moving zero-point -- degenerate with any")
    print("     a0(z) reading. Existence proof that 'the BTFR zero-point moves' is NOT evidence for the")
    print("     framework: it is the generic expectation, of multiple physical origins.")
    print("   => A bare detection of BTFR offset confirms NOTHING distinctive. ONLY the deep-MOND-regime,")
    print("      gas-controlled, NEGATIVE-by-z>=2 sign -- against the positive assembly drift -- is the")
    print("      framework's signature, and it must be disentangled from these confounds.\n")

    # ---- 6. NET ----
    banner("(6) NET -- both ways")
    print("   DISTINCTIVE? YES in principle: the SIGN (discs BELOW z=0 BTFR by z>=2) is shared with")
    print("     NOTHING else -- const-a0 MOND = ON, rising rival = ABOVE. But it is CONDITIONAL on DE")
    print("     EVOLVING: if Lambda is a true constant, a0(z)=a0(0) and the framework predicts ZERO offset,")
    print("     IDENTICAL to const-a0 MOND -> NO distinctive signal. The distinctive test EXISTS only in")
    print("     the DESI-evolving-DE world; it is a conditional, falsifiable bet, not a standing prediction.")
    print("   CLEAN or BURIED? Clean in PRINCIPLE (interp-robust, mu/Upsilon/H0 cancel in the ratio).")
    print("     BURIED in PRACTICE at z<~2 (signal < confounds < per-galaxy error) and at z<1 the framework")
    print("     bump puts the signal at ~0 (un-distinctive there anyway). Only z~2-3 deep-MOND samples can")
    print("     deliver it, and none exist yet (the regime trap kills every current massive-disk sample).")
    print("   CURRENT LEAN: the ONE direct multi-point measurement (MUSE-DARK III, Ciocan 2026) finds a0")
    print("     RISING (~+1.59e-10/z), the WRONG sign for the declining branch -- de-systematized to ~1.5sigma")
    print("     against (LCDM-degenerate, never reaching a clean exclusion). DESI DR2 w0wa is sign-ALIGNED")
    print("     (rho_DE lower in past) but DESI measures rho_DE, NOT a0 -- 'DESI confirms a0(z)' is FORBIDDEN.")
    print("     These pull OPPOSITE ways. Net: leaning mildly UNFAVOURABLE on the direct axis, not falsified.")
    print()
    print("   ONE-LINE: the high-z BTFR offset is the framework's cleanest DISTINCTIVE discriminator BY SIGN,")
    print("   verified at -7%/-0.033 dex (V) by z=3 -- but it is conditional on evolving DE, sits at the")
    print("   confound floor below z~2, needs deep-MOND z~2-3 disks that don't yet exist, and the one")
    print("   existing direct a0(z) measurement currently leans the WRONG way (~1.5sigma).")


if __name__ == "__main__":
    main()
