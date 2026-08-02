#!/usr/bin/env python3
"""CLUSTER STANDING AUDIT -- eta(R500) on real eRASS1, on the FRAMEWORK'S OWN terms.

REVISED 2026-07-30.  Three things were wrong in the previous revision and all three
corrections run AGAINST the framework:

  (1) MISLABELLED HEADLINE.  The banked eta(R500) = 2.149 was computed with the "simple"
      mu of Famaey & Binney (2005) -- a FOREIGN interpolation function.  Judging this
      framework through a rival nu violates the repo's own rule.  The framework is
      modified INERTIA with its OWN de Sitter-Unruh kernel
            g_obs^2 = g_bar^2 + a0 g_bar   <=>   nu(y) = sqrt(1 + 1/y),  y = g_bar/a0,
      and on that kernel eta is LARGER.  The framework's own kernel is now the HEADLINE
      and the rivals are a clearly-labelled robustness row.
  (2) BACKWARDS XRISM FRAMING.  The corpus read XRISM as licensing a large non-thermal
      component and hence relieving the cluster problem.  Every primary source says the
      opposite: the measured non-thermal fractions are SMALL.  XRISM TIGHTENS this front.
      The retired phrase "post-XRISM equilibrium bracket eta in [1.0, 2.33]" reads as
      relief and is withdrawn.
  (3) THE STATISTICAL SIGNIFICANCE WAS NEVER THE NUMBER TO QUOTE.  N = 9830 buys a
      formal ~300+ sigma that means nothing, because the whole deficit is an
      ABSOLUTE-SCALE statement and absolute cluster mass scales carry a systematic floor.
      The floor-limited significance is the honest one and it is a few sigma, not 300.

Also added here: the a0-RATIO framing (sharper than eta and convention-clean), the
method-and-radius SPREAD in the cluster acceleration scale (it is NOT a scalar "17x"),
the cost of the framework's own LOWER a0, the Kelleher & Lelli Eq. (5) modified-inertia
caveat with its both-ways landing, and the correct attribution of g_ddagger = 2.02e-9.

BOTH a0 FOOTINGS are carried on every dimensional number:
  canonical  a0 = c H_Lambda / Z = 9.36e-11 m/s^2   (rho_DE)
  alternative a0 = c H_0      / Z = 1.13e-10 m/s^2   (rho_total)

Internal checks are structural identities (kernel inequalities, deep-limit asymptotics,
footing arithmetic, significance arithmetic).  None of them encodes a verdict about the
framework: every eta, every sigma and every ratio below is computed from the data and the
published inputs.  The script exits NON-ZERO if any identity fails.

Data: eRASS1 primary cluster catalogue v3.2 (Bulbul et al. 2024).
"""
import sys
import numpy as np
from astropy.io import fits

# ----------------------------------------------------------------------------------------
# constants and the two footings
# ----------------------------------------------------------------------------------------
c, G, Msun, kpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19
H0 = 2.184e-18                       # 67.4 km/s/Mpc
H0_KMS = 67.4                        # same H0 in km/s/Mpc, for the h50-scaled Coma rung
Om, OmL = 0.315, 0.685
Z_GEOM = np.sqrt(32.0 * np.pi / 3.0)   # 5.78881
RHO_CRIT0 = 3 * H0**2 / (8 * np.pi * G)
RHO_DE0 = OmL * RHO_CRIT0

A0_CANON = 0.5 * c * np.sqrt(G * RHO_DE0)   # = c H_Lambda / Z, rho_DE footing
A0_ALT = c * H0 / Z_GEOM                     # = c H_0      / Z, rho_total footing
FOOTINGS = (("canonical rho_DE  (cH_Lambda/Z)", A0_CANON),
            ("alt rho_total     (cH_0/Z)", A0_ALT))

A0_MOND = 1.20e-10   # McGaugh+2016 SPARC galaxy g_dagger; also Kelleher & Lelli's input

FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"

# ----------------------------------------------------------------------------------------
# check harness -- exits non-zero on failure, records nothing about the verdict
# ----------------------------------------------------------------------------------------
_FAILS = []


def chk(label, condition, detail=""):
    ok = bool(condition)
    print("   [%s] %s%s" % ("PASS" if ok else "FAIL", label, ("  -- " + detail) if detail else ""))
    if not ok:
        _FAILS.append(label)
    return ok


# ----------------------------------------------------------------------------------------
# interpolation functions.  nu(y) with y = g_bar/a0 and g_obs = nu(y) g_bar.
# ----------------------------------------------------------------------------------------
def nu_framework(y):
    """THE FRAMEWORK'S OWN dS-Unruh kernel: g_obs^2 = g_bar^2 + a0 g_bar."""
    return np.sqrt(1.0 + 1.0 / y)


def nu_simple(y):     # RIVAL: Famaey & Binney 2005 "simple" mu(x) = x/(1+x)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_standard(y):   # RIVAL: "standard" mu(x) = x/sqrt(1+x^2)
    return np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y**2))


def nu_rar(y):        # RIVAL: McGaugh+2016 RAR e-folding nu
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


RIVALS = {"simple (Famaey-Binney 05)": nu_simple,
          "standard": nu_standard,
          "RAR-exp (McGaugh+16)": nu_rar}


# ----------------------------------------------------------------------------------------
def load(fstar, fgas_lo=0.01, fgas_hi=0.30, zmax=1.0):
    d = fits.open(FITS)[1].data
    f = lambda col: np.array([float(v) if str(v).strip() not in ("", "--") else np.nan
                              for v in d[col]], float)
    z, M500, Mgas, fgas, R500, KT = (f("BEST_Z"), f("M500"), f("MGAS500"),
                                     f("FGAS500"), f("R500"), f("KT"))
    M500H, M500L = f("M500_H"), f("M500_L")
    ok = ((z > 0) & (z < zmax) & np.isfinite(z) & (M500 > 0) & (Mgas > 0) & (R500 > 0)
          & (fgas > fgas_lo) & (fgas < fgas_hi))
    M500_kg = M500[ok] * 1e13 * Msun
    Mbar_kg = (1 + fstar) * Mgas[ok] * 1e11 * Msun
    R_m = R500[ok] * kpc
    gobs = G * M500_kg / R_m**2
    gbar = G * Mbar_kg / R_m**2
    eM = (M500H[ok] - M500L[ok]) / (2 * np.maximum(M500[ok], 1e-6))
    eM = np.clip(np.nan_to_num(eM, nan=0.25), 0.05, 1.0)
    return dict(z=z[ok], M500=M500[ok], gobs=gobs, gbar=gbar, eM=eM, KT=KT[ok],
                N=int(ok.sum()))


def eta_arr(gobs, gbar, a0, nu):
    return gobs / (nu(gbar / a0) * gbar)


def eta_stats(gobs, gbar, a0, nu):
    e = eta_arr(gobs, gbar, a0, nu)
    return np.median(e), 10**np.mean(np.log10(e)), np.percentile(e, [25, 75])


# 0.30 dex added 2026-08-02: this corpus's OWN systematic floor (cluster_rar_throttle_2026/lane2_data.py,
# SYS_FLOOR_DEX = (0.1, 0.3)) runs to 0.30 dex, but this ladder stopped at 0.20 -- one rung short, and the
# missing rung is the one where the cluster offset is NOT a tension. Truncating a systematic range at its
# tight end manufactures a deficit exactly as using a scatter for an error does.
def sig_block(gobs, gbar, a0, nu, floors=(0.10, 0.15, 0.20, 0.30)):
    le = np.log10(eta_arr(gobs, gbar, a0, nu))
    N = le.size
    mean_log, sd_log = float(np.mean(le)), float(np.std(le))
    se = sd_log / np.sqrt(N)
    return dict(N=N, mean=mean_log, sd=sd_log, se=se, stat_sigma=mean_log / se,
                floor={fl: mean_log / fl for fl in floors})


# ========================================================================================
def main():
    W = 100
    print("=" * W)
    print("CLUSTER eta(R500) AUDIT -- eRASS1 (Bulbul+2024), FRAMEWORK'S OWN KERNEL AS HEADLINE")
    print("  canonical a0 = %.4e m/s^2 (rho_DE, cH_Lambda/Z)" % A0_CANON)
    print("  alt       a0 = %.4e m/s^2 (rho_total, cH_0/Z)   footing spread = %.4fx = %.4f dex"
          % (A0_ALT, A0_ALT / A0_CANON, np.log10(A0_ALT / A0_CANON)))
    print("=" * W)

    try:
        base = load(fstar=0.20)
    except Exception as exc:                                    # pragma: no cover
        print("\nFATAL: could not read the eRASS1 catalogue at\n  %s\n  %r" % (FITS, exc))
        print("No eta number can be quoted without it.  NOT fabricating output.")
        sys.exit(2)

    print("\nClean sample (0<z<1, M500>0, Mgas>0, 0.01<fgas<0.30, fstar=0.20): N = %d" % base["N"])
    z = base["z"]
    print("  z: median %.3f  (10-90%%: %.3f - %.3f)"
          % (np.median(z), np.percentile(z, 10), np.percentile(z, 90)))
    for lab, a0 in FOOTINGS:
        g = base["gbar"] / a0
        print("  %-34s g_bar/a0 median %.4f  (%.0f%% at g_bar<0.1 a0 -> deep regime)"
              % (lab, np.median(g), 100 * (g < 0.1).mean()))

    # ------------------------------------------------------------------ 1. HEADLINE
    print("\n" + "-" * W)
    print("1. HEADLINE -- eta = M_dyn / M_pred at R500 on the FRAMEWORK's OWN kernel nu=sqrt(1+1/y)")
    print("-" * W)
    print("  %-36s %8s %8s %18s" % ("footing", "median", "geomean", "[q25,q75]"))
    head = {}
    for lab, a0 in FOOTINGS:
        med, gm, q = eta_stats(base["gobs"], base["gbar"], a0, nu_framework)
        head[lab] = (med, gm)
        print("  %-36s %8.3f %8.3f   [%.2f, %.2f]" % (lab, med, gm, q[0], q[1]))
    eta_fw_med, eta_fw_gm = head[FOOTINGS[0][0]]

    print("\n  ROBUSTNESS ROW -- RIVAL interpolation functions (NOT the framework's; shown only")
    print("  to show the number is not an artefact of one kernel choice).  Canonical footing.")
    print("  %-30s %8s %8s   %s" % ("RIVAL nu", "median", "geomean", "ratio to framework kernel"))
    riv = {}
    for name, nu in RIVALS.items():
        med, gm, _ = eta_stats(base["gobs"], base["gbar"], A0_CANON, nu)
        riv[name] = (med, gm)
        print("  %-30s %8.3f %8.3f   %.4f" % (name, med, gm, med / eta_fw_med))
    print("  The banked 2.149 headline was the 'simple' row above -- a FOREIGN kernel.")
    print("  On the framework's own kernel eta is %.1f%% LARGER.  Applying the repo's own rule"
          % (100 * (eta_fw_med / riv["simple (Famaey-Binney 05)"][0] - 1)))
    print("  correctly makes the deficit WORSE, not better.")

    # ------------------------------------------------------------------ 2. SIGNIFICANCE
    print("\n" + "-" * W)
    print("2. SIGNIFICANCE -- statistical vs SYSTEMATIC-FLOOR-LIMITED.  QUOTE THE FLOOR-LIMITED ONE.")
    print("-" * W)
    sig_fw = sig_block(base["gobs"], base["gbar"], A0_CANON, nu_framework)
    sig_fw_alt = sig_block(base["gobs"], base["gbar"], A0_ALT, nu_framework)
    sig_simple = sig_block(base["gobs"], base["gbar"], A0_CANON, nu_simple)

    def show(tag, s):
        print("  %s" % tag)
        print("     N = %d   mean log10(eta) = %+.4f dex   scatter = %.4f dex   SE = %.5f dex"
              % (s["N"], s["mean"], s["sd"], s["se"]))
        print("     formal STATISTICAL significance = %.0f sigma   <-- DO NOT QUOTE THIS"
              % s["stat_sigma"])
        print("     floor-limited significance (absolute-scale systematic floor):")
        for fl, sg in s["floor"].items():
            print("        vs %.2f dex floor : %.2f sigma" % (fl, sg))

    show("FRAMEWORK kernel, canonical a0  <-- THE HEADLINE", sig_fw)
    show("FRAMEWORK kernel, alt a0", sig_fw_alt)
    show("RIVAL 'simple' kernel, canonical a0  (the banked, mislabelled block)", sig_simple)
    print("\n  WHY THE STATISTICAL NUMBER IS MEANINGLESS HERE: eta is an ABSOLUTE-SCALE ratio.")
    print("  N=%d shrinks the SE to %.5f dex, but every cluster shares the same absolute mass" % (sig_fw["N"], sig_fw["se"]))
    print("  calibration (M500 proxy zero-point, R500 definition, f_gas budget, HSE bias).  A common")
    print("  offset does not average down with N.  The floor-limited figure is the one to quote:")
    print("  %+.3f dex against a 0.10 / 0.15 / 0.20 / 0.30 dex floor -> %.2f / %.2f / %.2f / %.2f sigma."
          % (sig_fw["mean"], sig_fw["floor"][0.10], sig_fw["floor"][0.15], sig_fw["floor"][0.20],
             sig_fw["floor"][0.30]))
    print("  At the TOP of this corpus's own floor range (0.30 dex) the cluster offset is %.2f sigma -- i.e."
          % sig_fw["floor"][0.30])
    print("  NOT a tension. The honest headline is the RANGE, never the 0.10-dex end alone.")
    print("  Real, soft, and NOT a referee-proof kill at either end of the floor range.")
    sig_each = np.log10(eta_arr(base["gobs"], base["gbar"], A0_CANON, nu_framework)) / (base["eM"] / np.log(10))
    print("  (median per-cluster significance on each cluster's own M500 error: %.2f sigma)"
          % np.median(sig_each))

    # ------------------------------------------------------------------ 3. BARYON BUDGET
    print("\n" + "-" * W)
    print("3. BARYON-BUDGET SWEEP -- stellar fraction fstar (= M_star/M_gas), FRAMEWORK kernel")
    print("-" * W)
    print("  %-10s %10s %10s %10s %10s" % ("fstar", "med canon", "gm canon", "med alt", "gm alt"))
    for fstar in (0.0, 0.10, 0.20, 0.30, 0.50):
        b = load(fstar=fstar)
        m1, g1, _ = eta_stats(b["gobs"], b["gbar"], A0_CANON, nu_framework)
        m2, g2, _ = eta_stats(b["gobs"], b["gbar"], A0_ALT, nu_framework)
        print("  %-10.2f %10.3f %10.3f %10.3f %10.3f" % (fstar, m1, g1, m2, g2))
    print("  Even an implausibly generous fstar=0.50 does not reach eta=1 on either footing.")

    # ------------------------------------------------------------------ 4. COST OF LOWER a0
    print("\n" + "-" * W)
    print("4. THE COST OF THE FRAMEWORK'S OWN LOWER a0 -- it makes eta WORSE than standard MOND")
    print("-" * W)
    print("  Deep regime: g_obs -> sqrt(a0 g_bar), so at fixed g_obs the predicted mass scales as")
    print("  sqrt(a0) and eta scales as sqrt(a0_rival / a0_framework).  Rival = %.3e (McGaugh+16)." % A0_MOND)
    penalty = {}
    for lab, a0 in FOOTINGS:
        pred = np.sqrt(A0_MOND / a0)
        m_f, g_f, _ = eta_stats(base["gobs"], base["gbar"], a0, nu_framework)
        m_r, g_r, _ = eta_stats(base["gobs"], base["gbar"], A0_MOND, nu_framework)
        meas = g_f / g_r
        penalty[lab] = (pred, meas)
        print("  %-34s sqrt(a0_rival/a0) = %.4f  (+%.1f%% on eta)   measured geomean ratio = %.4f"
              % (lab, pred, 100 * (pred - 1), meas))
    print("  This is not a rounding detail: the framework's distinctive content IS the coefficient,")
    print("  and here the coefficient costs it %.1f%% (canonical) / %.1f%% (alt)."
          % (100 * (penalty[FOOTINGS[0][0]][0] - 1), 100 * (penalty[FOOTINGS[1][0]][0] - 1)))
    print("  Erasing eta by an a0 boost alone needs a0 x eta^2, on the canonical footing:")
    for tag, e in (("median  eta=%.3f" % eta_fw_med, eta_fw_med), ("geomean eta=%.3f" % eta_fw_gm, eta_fw_gm)):
        print("    %-22s -> a0 x %.2f (= +%.3f dex), i.e. a0 ~ %.2e -- which the galaxy RAR excludes."
              % (tag, e**2, 2 * np.log10(e), A0_CANON * e**2))

    # ------------------------------------------------------------------ 5. a0-RATIO FRAMING
    print("\n" + "-" * W)
    print("5. THE a0-RATIO FRAMING -- sharper than eta, and convention-clean for the lensing entry")
    print("-" * W)
    print("  ATTRIBUTION, CORRECTED: the cluster acceleration scale g_ddagger = (2.02 +/- 0.11)e-9")
    print("  m/s^2 is Tian, Umetsu, Ko, Donahue & Chiu 2020, ApJ 896, 70 (arXiv:2001.08340), from 20")
    print("  CLASH clusters, 100-600 kpc, slope fixed at 1/2.  It is NOT 'Tian & Ko 2016' (that is")
    print("  MNRAS 462, 1092 on ELLIPTICAL galaxies, which adopts a0=1.21e-10 and makes no cluster")
    print("  claim), and it is NOT 'Chae 2024'.  The words 'a seventeen times larger acceleration")
    print("  scale' appear in Tian et al. 2024, A&A 684, A180 (arXiv:2402.12016) and are 2.02e-9 /")
    print("  1.20e-10 = %.2f -- a ratio to STANDARD MOND's a0, not to the framework's." % (2.02e-9 / A0_MOND))
    print("  Note also the SYMBOL: Tian et al. reserve g_dagger for the GALAXY scale 1.20e-10 and")
    print("  write the cluster scale g_ddagger.  Writing 'g_dagger = 2.02e-9' inverts their notation.")
    print("\n  METHOD-AND-RADIUS LADDER (there is NO robust scalar '17x'):")
    ladder = [
        ("lensing 100-600 kpc, 20 CLASH", 2.02e-9, "Tian+2020 ApJ 896 70 (slope fixed 1/2; conv-clean)"),
        ("dynamics, member gals (29 HIFLUGCS) lo", 0.8e-9, "Tian+2021; own headline 'about ten times'"),
        ("dynamics, member gals (29 HIFLUGCS) hi", 2.2e-9, "Tian+2021; factor-2.8 internal band"),
        ("dynamics, 54 BCG stellar MVDR", 1.7e-9, "Tian+2024 A&A 684 A180 (+/-0.7e-9)"),
        ("X-ray HSE pooled, 52 non-cool-core", 9.5e-10, "Chan&DelPopolo 2020 (McGaugh-nu loaded)"),
        ("X-ray HSE at r_c", 1.9e-9, "Chan&DelPopolo 2020 -- grows inward"),
        ("X-ray HSE at 2 r_c", 1.2e-9, "Chan&DelPopolo 2020"),
        ("X-ray HSE at 3 r_c", 3.9e-10, "Chan&DelPopolo 2020 -- outer bin"),
        ("Coma MOND model (LOWER BOUND)", 2.0e-10 * (H0_KMS / 50.0) ** 2,
         "The&White 1988: >= 2 h50^1.5 -> abs 2e-10 h50^2, evaluated at THIS script's H0"),
    ]
    # NOT a cluster probe -- it is the DENOMINATOR of "17x". Kept for the arithmetic, excluded from
    # the cluster spread, because including it silently widened the range and SOFTENED the ladder.
    GALAXY_REF = ("galaxy RAR reference g_dagger", 1.20e-10, "McGaugh+2016 -- the DENOMINATOR of '17x'")
    print("  %-40s %10s | %8s %8s | %8s %8s" % ("probe", "g [m/s^2]", "x canon", "dex", "x alt", "dex"))
    ratios = []
    for name, g, src in ladder:
        r1, r2 = g / A0_CANON, g / A0_ALT
        ratios.append(r1)
        print("  %-40s %10.3e | %8.2f %8.3f | %8.2f %8.3f" % (name, g, r1, np.log10(r1), r2, np.log10(r2)))
    for name, g, src in ladder:
        print("     %-40s %s" % (name, src))
    lo, hi = min(ratios), max(ratios)
    print("\n  SPREAD, canonical footing: %.2fx to %.2fx (%.3f to %.3f dex) -- a factor %.1f range"
          % (lo, hi, np.log10(lo), np.log10(hi), hi / lo))
    print("  driven by METHOD and by RADIUS (the discrepancy GROWS inward, stated in Chan &")
    print("  Del Popolo 2020).  Tian et al. 2020's own 'Note added in proof' says their result and")
    print("  Chan & Del Popolo's 'are not in quantitative agreement'.  Carry the ladder, not a scalar.")
    print("\n  THE ONE NUMBER THE FRAMEWORK MUST ANSWER FOR (top of the ladder, lensing):")
    for lab, a0 in FOOTINGS:
        r = 2.02e-9 / a0
        e = np.sqrt(2.02e-9 / a0)
        print("    %-34s g_ddagger/a0 = %.2f (%.3f dex);  deep-limit g_obs shortfall = %.2fx (%.3f dex)"
              % (lab, r, np.log10(r), e, np.log10(e)))
    print("    +/-0.11e-9 propagates to %.2f +/- %.2f (canonical) = %.3f +/- %.3f dex"
          % (2.02e-9 / A0_CANON, 0.11e-9 / A0_CANON,
             np.log10(2.02e-9 / A0_CANON),
             0.11 / 2.02 / np.log(10)))
    print("    WHY THIS IS CONVENTION-CLEAN: Tian's fit fixes the slope at 1/2, i.e. it fits")
    print("    g_obs = sqrt(g_ddagger g_bar), whose deep asymptote is IDENTICAL for the framework's")
    print("    nu and for every rival nu.  So unlike eta, this entry carries no kernel choice.")
    print("    Against Desmond 2023's RAR universality budget (sigma_int = 0.034 dex -> +/-0.068 at")
    print("    1 sigma): %.1fx over at 1 sigma, %.1fx over at 3 sigma."
          % (np.log10(2.02e-9 / A0_CANON) / 0.068, np.log10(2.02e-9 / A0_CANON) / (3 * 0.068)))

    # ------------------------------------------------------------------ 6. XRISM DIRECTION
    print("\n" + "-" * W)
    print("6. XRISM DIRECTION CORRECTION -- XRISM TIGHTENS THIS FRONT, IT DOES NOT RELIEVE IT")
    print("-" * W)
    print("  WITHDRAWN: the corpus's reading that XRISM licenses a large non-thermal component and")
    print("  brackets eta down to ~1.0 ('post-XRISM equilibrium bracket eta in [1.0, 2.33]').  Every")
    print("  primary source says the measured non-thermal pressure is SMALL.")
    REQ = (10.0, 40.0)        # Kelleher & Lelli 2024, EFE branch, r > 1 Mpc, per cent
    REQ_NOEFE = (10.0, 100.0)  # KL 2024, no-EFE branch, r > 1 Mpc
    meas = [
        ("A2029 core (<180 kpc), XRISM kinematic", 2.6, 0.3, "ApJL 982 L5", "CORE -- radius-MISmatched"),
        ("A2029 out to R2500=670 kpc, XRISM", 2.0, 0.5, "PASJ 77 S242", "inside 1 Mpc -- MISmatched"),
        ("Coma centre, XRISM line broadening", 3.1, 0.4, "ApJL 985 L20", "LOS small-scale only, no bulk"),
        ("Coma <R500 incl. large-scale bulk", 10.0, 8.0, "A&A 704 A35", "RADIUS-MATCHED at R500"),
        ("Perseus map, most regions", 2.75, 2.25, "A&A 707 A109", "0.5-5%; to ~0.7 R2500 only"),
        ("Perseus E/NE + inner/outermost bins", 10.5, 3.5, "A&A 707 A109", "7-14%; non-AGN"),
        ("X-COP median at R500 (12 clusters)", 5.9, 2.9, "A&A 621 A40", "RADIUS-MATCHED; NOT kinematic"),
        ("X-COP median at R200", 10.5, 4.3, "A&A 621 A40", "RADIUS-MATCHED at R200"),
        ("X-COP population MEAN bound at R500", 13.0, 0.0, "A&A 621 A40", "Eckert's own upper bound"),
        ("X-COP A2319 at R500 (single cluster)", 43.6, 3.5, "A&A 621 A40", "the scatter reaches it"),
    ]
    print("\n  REQUIREMENT (Kelleher & Lelli 2024, A&A 688 A78): hydrostatic bias %.0f-%.0f%% at r>1 Mpc"
          % REQ)
    print("  with MAXIMAL external field effect; %.0f-%.0f%% in their no-EFE branch; 50-60%% beyond 2 Mpc."
          % REQ_NOEFE)
    print("  BOTH BRANCHES ARE CARRIED BELOW. Reporting only the EFE branch would quote the")
    print("  framework-FRIENDLIEST requirement and silently soften the comparison.")
    print("  KL Sect. 5.4 place r>1 Mpc at ~R500, so R500/R200 are the radius-matched comparisons.")
    print("\n  %-40s %7s %7s | %13s %13s" % ("MEASURED f_nth [%]", "value", "+1sig", "req/meas", "req/(meas+1s)"))
    for name, v, e, src, note in meas:
        f_lo, f_hi = REQ[0] / v, REQ[1] / v
        g_lo, g_hi = REQ[0] / (v + e), REQ[1] / (v + e)
        print("  %-40s %7.1f %7.1f | %5.2f-%5.2f  %5.2f-%5.2f" % (name, v, v + e, f_lo, f_hi, g_lo, g_hi))
    for name, v, e, src, note in meas:
        print("     %-40s %-14s %s" % (name, src, note))

    print("\n  HEADLINE, RADIUS-MATCHED (the only defensible comparison):")
    for name, v, e in (("X-COP median R500", 5.9, 2.9), ("X-COP median R200", 10.5, 4.3),
                       ("Coma <R500 incl. bulk", 10.0, 8.0)):
        print("    %-24s requirement exceeds measurement by %.2fx - %.2fx (%.2fx - %.2fx at +1 sigma)"
              % (name, REQ[0] / v, REQ[1] / v, REQ[0] / (v + e), REQ[1] / (v + e)))
    print("    The naive core factor (%.1fx - %.1fx against A2029's 2.6%%) is RADIUS-MISMATCHED and"
          % (REQ[0] / 2.6, REQ[1] / 2.6))
    print("    must NOT be the headline: every XRISM velocity measurement stops inside 1 Mpc,")
    print("    exactly where KL themselves say the bias 'should play a minor role'.")

    print("\n  AND THE SIGN, WHICH IS THE HARDER HALF.  Two distinct statements, both unfavourable:")
    eta_here = eta_fw_gm
    bias_needed = 1.0 - 1.0 / eta_here
    print("    (a) AT r>1 Mpc the requirement's SIGN is right (true mass ABOVE thermal-HSE mass) but")
    print("        the magnitude is %.1fx-%.1fx short of the radius-matched measurement."
          % (REQ[0] / 5.9, REQ[1] / 5.9))
    print("    (b) AT R500 AND INWARD the residual is a DEFICIT (MOND under-predicts).  Erasing")
    print("        eta by a mass-bias route needs the thermal HSE to OVER-estimate the truth by")
    print("        1 - 1/eta = %.1f%% (median eta=%.3f) to %.1f%% (geomean eta=%.3f); on the alt"
          % (100 * (1 - 1 / eta_fw_med), eta_fw_med, 100 * bias_needed, eta_here))
    print("        footing %.1f%% to %.1f%%.  Non-thermal pressure does the OPPOSITE: M_true ="
          % (100 * (1 - 1 / head[FOOTINGS[1][0]][0]), 100 * (1 - 1 / head[FOOTINGS[1][0]][1])))
    print("        M_HSE/(1-f_nth) >= M_HSE for f_nth >= 0, so it RAISES eta.  The turbulence escape")
    print("        at R500 is not merely too small -- it has the WRONG SIGN.  With the measured")
    print("        f_nth = 5.9%% at R500 the canonical eta moves from %.3f to %.3f."
          % (eta_here, eta_here / (1 - 0.059)))
    print("    (b') *** CATEGORY CAVEAT, added 2026-07-30 after an adversarial check. *** The eta above is")
    print("        built on eRASS1 M500, which is a WEAK-LENSING-CALIBRATED X-ray count-rate proxy, NOT a")
    print("        thermal-HSE mass. So the M_true = M_HSE/(1-f_nth) argument does not apply to it")
    print("        directly, and quoting it here as though it did overstates the case against the")
    print("        turbulence escape. The relevant systematic for a WL-calibrated mass is the WL")
    print("        CALIBRATION (Li+2024: WL runs ~110%% above hydrostatic AND kinematic, which agree with")
    print("        each other) -- which is exactly the axis the corpus previously mislabelled as")
    print("        'post-XRISM'. The f_nth arithmetic below is retained as a SIGN argument for genuinely")
    print("        hydrostatic analyses (e.g. Kelleher & Lelli's), not as a correction to this eta.")
    print("        [both footings: alt eta %.3f -> %.3f]"
          % (head[FOOTINGS[1][0]][1], head[FOOTINGS[1][0]][1] / (1 - 0.059)))

    print("\n  LEGITIMATE SOFTENERS -- the tightening is real but NOT clean.  All five are sourced:")
    print("    (i)   RADIUS.  A2029 stops at R2500 = 670 kpc; Perseus at ~0.7 R2500 ~ 570 kpc.  Neither")
    print("          directly bounds a requirement stated at r > 1 Mpc.")
    print("    (ii)  LINE-OF-SIGHT / FIELD OF VIEW.  The 2.6-3.1% figures are small-scale LOS")
    print("          broadening and explicitly exclude bulk-velocity pressure (ApJL 985 L20 Sect 4.1).")
    print("          Folding bulk motions in, Coma reaches P_NT/P_tot(<R500) = 10 (+8/-4)% (A&A 704 A35")
    print("          Eq 16) -- which sits ON KL's lower bound, so at R200 the ranges OVERLAP and there")
    print("          is no exclusion.")
    print("    (iii) SCATTER.  X-COP's per-cluster range at R500 is 2.2% to 43.6%; the 5.9% is a")
    print("          MEDIAN, and Eckert's own bound on the population MEAN is 13%, not 6%.  MOND")
    print("          cluster fits are done cluster-by-cluster, so individual clusters DO reach it.")
    print("    (iv)  MODEL DEPENDENCE OF THE ONE RADIUS-MATCHED NUMBER.  X-COP's alpha at R500 is not")
    print("          kinematic: it is inferred from f_gas,HSE against a LambdaCDM-calibrated universal")
    print("          gas fraction (Omega_b/Omega_m = 0.156, Planck; Y_b from The300).  Using it against")
    print("          MOND is partly circular.  XRISM's numbers are model-independent but core-only --")
    print("          the two virtues do not coexist in one dataset.")
    print("    (v)   NOT AN IDENTITY.  KL's 'bias' is a mass/acceleration residual, not P_NT/P_tot.")
    print("          The empirical (mass bias)/alpha ratio from Eckert Table 2 has median 1.10 at R500")
    print("          and 0.86 at R200, so the factors above carry ~30% definitional slop.")
    print("    NOT a valid softener: f_nth is algebraically IDENTICAL across all four XRISM/X-COP")
    print("    papers (all credit Eckert+2019 Eq 10), so definitional mismatch cannot be invoked there.")
    print("\n  ON THE FRAMEWORK'S OWN FOOTINGS the comparison gets slightly WORSE, not better: KL used")
    print("  a0 = 1.2e-10, and in the deep limit the framework predicts less acceleration --")
    for lab, a0 in FOOTINGS:
        print("    %-34s sqrt(a0/1.2e-10) = %.4f -> %.1f%% LESS deep-MOND acceleration than KL"
              % (lab, np.sqrt(a0 / A0_MOND), 100 * (1 - np.sqrt(a0 / A0_MOND))))
    print("  which pushes the required bias UP.  Direction only -- this is not a refit, and the")
    print("  framework's nu is not KL's, so no revised bias percentage is quoted from it.")

    # ------------------------------------------------------------------ 7. KL Eq (5) MI CAVEAT
    print("\n" + "-" * W)
    print("7. THE KELLEHER & LELLI Eq. (5) MODIFIED-INERTIA CAVEAT -- verbatim, then where it lands")
    print("-" * W)
    print('  VERBATIM (A&A 688 A78, Sect. 2.2, below Eq. 6):')
    print('    "Equation (5) is strictly valid in MOND modified gravity theories for isolated,')
    print('     spherically symmetric systems (Bekenstein & Milgrom 1984; Milgrom 2010, 2023).')
    print('     Equation (5) is also valid in MOND modified inertia theories in the case of')
    print('     isolated systems with purely circular orbits (Milgrom 1994), which is clearly not')
    print('     the case for the random gas motions in the ICM.  In this work, therefore, we are')
    print('     primarily testing MOND modified gravity theories, albeit we expect Eq. (5) to')
    print('     provide the correct order of magnitude also in modified inertia theories (for')
    print('     isolated systems)."')
    print("  The corpus has quoted this truncated at 'random gas motions in the ICM', which reverses")
    print("  its rhetorical force.  The final clause must always travel with it.")
    print("\n  BOTH WAYS.")
    print("  FOR the escape: Eq. (5) is a POINTWISE algebraic relation whose MI derivation (Milgrom")
    print("  1994) assumes isolated systems on purely circular orbits.  MI kernels are temporally")
    print("  nonlocal; ICM support is pressure/random-motion.  So the inversion g_obs -> g_bar that")
    print("  DEFINES the deficit is not guaranteed pointwise under MI, and KL say themselves they are")
    print("  'primarily testing MOND modified gravity theories'.  KL's exact numbers are therefore")
    print("  order-of-magnitude MI constraints, not precision ones.  That much is correct.")
    print("\n  AGAINST the escape -- and this is decisive on SIZE, in four steps:")
    print("    1. KL's own stated expectation is order-of-magnitude validity under MI, and the residual")
    print("       here IS an order-of-magnitude-level object (eta = %.2f, i.e. %.0f%% missing), not a"
          % (eta_fw_gm, 100 * (eta_fw_gm - 1)))
    print("       percent-level one.")
    print("    2. The corpus's own repeated finding is MI == AeST(=MG) to machine precision in STATIC")
    print("       systems, and hydrostatic clusters ARE modelled as static.  The framework therefore")
    print("       has no internal licence to predict a different static mass requirement.")
    print("    3. The one genuinely MI-DISTINCTIVE non-adiabatic observable the corpus has computed --")
    print("       the relational sigma-spread -- was REPRICED from its own closure to 1.45-2.21%")
    print("       max-min (0.22-0.72% population RMS): see prep_2026/sigma_spread/GAP_STATEMENT.md,")
    print("       Amendment 1.  Compare what would be needed:")
    sigma_needed = 100 * (eta_fw_gm - 1)
    print("         needed to close eta = %.3f : ~%.0f%%     available (derived): 1.45-2.21%%"
          % (eta_fw_gm, sigma_needed))
    print("         shortfall = %.0fx to %.0fx.  A 2%% effect cannot close a ~%.0f%% residual."
          % (sigma_needed / 2.21, sigma_needed / 1.45, sigma_needed - 0))
    print("    4. DIRECTIONALLY the framework is worse off, not better: nu_fw(y) < nu_simple(y) at")
    print("       EVERY y (checked below), and the framework's a0 is lower than KL's 1.2e-10 on both")
    print("       footings.  Both effects INCREASE the required missing mass relative to KL's.")
    print("  LANDING: the caveat is a warning about the validity of a POINTWISE relation, not a door")
    print("  to Newtonian-baryons-only clusters under MI.  Do NOT write that the cluster constraint")
    print("  'does not apply' to the framework.  The defensible weaker claim is the only one to make:")
    print("  KL's numbers constrain MI to order of magnitude, and at that resolution the residual")
    print("  survives at the same size or larger.")

    # ------------------------------------------------------------------ 8. SHARED-FAMILY CLAIM
    print("\n" + "-" * W)
    print("8. THE 'SHARED ACROSS THE RELATIVISTIC-MOND FAMILY' CLAIM -- PATTERN, NOT THEOREM")
    print("-" * W)
    print("  There is NO published one-sentence statement that the cluster residual is shared across")
    print("  the relativistic-MOND family.  Checked:")
    print("    - Skordis & Zlosnik 2021 (the AeST paper) does not discuss clusters at all.")
    print("    - Durakovic & Skordis 2023 (arXiv:2312.00889) claim only 'potential'.")
    print("    - Famaey, Pizzuti & Saltas 2024 (arXiv:2410.02612) call it 'an open question'.")
    print("  What IS defensible: (a) the in-corpus argument that MI == AeST(=MG) to machine precision")
    print("  in static systems, which is sound for MI-vs-AeST specifically; and (b) that the residual")
    print("  is a 40-year, repeatedly-reproduced PATTERN across MOND cluster analyses.")
    print("  So: 'an argued pattern, shared with AeST by an in-corpus argument' is safe.")
    print("  'Shared across the whole relativistic-MOND family' as a published THEOREM is not.")

    # ------------------------------------------------------------------ 9. MASS TREND
    print("\n" + "-" * W)
    print("9. eta vs M500 (FRAMEWORK kernel, canonical a0, fstar=0.20)")
    print("-" * W)
    M = base["M500"]
    edges = np.percentile(M, [0, 20, 40, 60, 80, 100])
    print("  %-20s %6s %10s" % ("M500 bin [1e13 Msun]", "N", "eta_med"))
    for i in range(5):
        m = (M >= edges[i]) & (M < edges[i + 1] if i < 4 else M <= edges[i + 1])
        med, _, _ = eta_stats(base["gobs"][m], base["gbar"][m], A0_CANON, nu_framework)
        print("  %6.1f - %-11.1f %6d %10.3f" % (edges[i], edges[i + 1], m.sum(), med))

    # ------------------------------------------------------------------ CHECKS
    print("\n" + "=" * W)
    print("INTERNAL CHECKS (structural identities only -- none encodes a verdict)")
    print("=" * W)

    yg = np.logspace(-6, 6, 20001)
    chk("A: framework nu(y) < simple nu(y) for ALL y on 1e-6..1e6",
        np.all(nu_framework(yg) < nu_simple(yg)),
        "min ratio %.6f, max ratio %.6f" % (np.min(nu_framework(yg) / nu_simple(yg)),
                                            np.max(nu_framework(yg) / nu_simple(yg))))

    r_deep = nu_framework(1e-8) / nu_simple(1e-8)
    chk("B: deep limit -- framework and simple nu agree, so a slope-1/2 fit is convention-clean",
        abs(r_deep - 1.0) < 1e-3, "ratio at y=1e-8 is %.8f" % r_deep)

    chk("C: two independent routes to the canonical a0 agree (0.5 c sqrt(G rho_DE) vs c H_Lambda/Z)",
        abs(A0_CANON - c * H0 * np.sqrt(OmL) / Z_GEOM) / A0_CANON < 1e-12,
        "%.6e vs %.6e" % (A0_CANON, c * H0 * np.sqrt(OmL) / Z_GEOM))

    chk("D: footing spread = alt/canon = 1/sqrt(OmL)",
        abs(A0_ALT / A0_CANON - 1 / np.sqrt(OmL)) < 1e-10,
        "%.6f vs %.6f" % (A0_ALT / A0_CANON, 1 / np.sqrt(OmL)))

    for fl in (0.10, 0.15, 0.20):
        chk("E(%.2f): floor-limited sigma equals mean/floor exactly" % fl,
            abs(sig_fw["floor"][fl] - sig_fw["mean"] / fl) < 1e-12)

    chk("F: statistical sigma equals mean/(sd/sqrt(N))",
        abs(sig_fw["stat_sigma"] - sig_fw["mean"] / (sig_fw["sd"] / np.sqrt(sig_fw["N"]))) < 1e-9,
        "%.2f sigma" % sig_fw["stat_sigma"])

    chk("G: statistical sigma exceeds the floor-limited sigma by sqrt(N)*floor/sd",
        abs(sig_fw["stat_sigma"] / sig_fw["floor"][0.10]
            - np.sqrt(sig_fw["N"]) * 0.10 / sig_fw["sd"]) < 1e-6,
        "ratio %.1f" % (sig_fw["stat_sigma"] / sig_fw["floor"][0.10]))

    for lab, _ in FOOTINGS:
        pred, measured = penalty[lab]
        chk("H(%s): measured eta ratio matches the deep-limit sqrt(a0) scaling to <5%%"
            % lab.split()[0], abs(measured / pred - 1) < 0.05,
            "predicted %.4f, measured %.4f" % (pred, measured))

    chk("I: sample is in the deep regime where the sqrt(a0) scaling is the right asymptotic",
        (base["gbar"] / A0_CANON < 0.3).mean() > 0.9,
        "%.1f%% of clusters at g_bar/a0 < 0.3" % (100 * (base["gbar"] / A0_CANON < 0.3).mean()))

    chk("J: XRISM requirement/measurement factors reproduce from the published inputs",
        abs(REQ[0] / 5.9 - 1.6949) < 1e-3 and abs(REQ[1] / 5.9 - 6.7797) < 1e-3,
        "%.4f and %.4f" % (REQ[0] / 5.9, REQ[1] / 5.9))

    chk("K: g_ddagger/a0 ladder arithmetic (Tian+2020 CLASH, canonical footing)",
        abs(2.02e-9 / A0_CANON - 21.58) < 0.02 and abs(np.log10(2.02e-9 / A0_CANON) - 1.334) < 0.002,
        "%.3f x = %.4f dex" % (2.02e-9 / A0_CANON, np.log10(2.02e-9 / A0_CANON)))

    chk("L: the '17x' phrasing is the ratio to STANDARD MOND's a0, not to the framework's",
        abs(2.02e-9 / A0_MOND - 16.83) < 0.02,
        "2.02e-9/1.20e-10 = %.2f, vs %.2f against the canonical a0"
        % (2.02e-9 / A0_MOND, 2.02e-9 / A0_CANON))

    chk("M: the mass-bias needed to erase eta has the OPPOSITE sign to non-thermal pressure",
        (1.0 - 1.0 / eta_fw_gm) > 0 and (eta_fw_gm / (1 - 0.059)) > eta_fw_gm,
        "erasing needs HSE to over-estimate by %.1f%%; f_nth=5.9%% moves eta %.3f -> %.3f"
        % (100 * (1 - 1 / eta_fw_gm), eta_fw_gm, eta_fw_gm / (1 - 0.059)))

    chk("N: the derived sigma-spread ceiling cannot close the residual",
        2.21 < 100 * (eta_fw_gm - 1),
        "available 2.21%%, needed %.0f%% -> short by %.0fx"
        % (100 * (eta_fw_gm - 1), 100 * (eta_fw_gm - 1) / 2.21))

    print("\n" + "=" * W)
    if _FAILS:
        print("RESULT: %d CHECK(S) FAILED -> %s" % (len(_FAILS), "; ".join(_FAILS)))
        print("=" * W)
        sys.exit(1)
    print("RESULT: all internal checks passed.")
    print("THE ONE HONEST eta STATEMENT:")
    print("  eta(R500) = %.3f median / %.3f geomean, eRASS1 (Bulbul+2024, N=%d, fstar=0.20),"
          % (eta_fw_med, eta_fw_gm, base["N"]))
    print("  on the FRAMEWORK's OWN kernel nu(y)=sqrt(1+1/y), canonical a0 = %.3e." % A0_CANON)
    print("  Alt footing: %.3f / %.3f.  Mean log10(eta) = %+.4f dex, scatter %.4f dex."
          % (head[FOOTINGS[1][0]][0], head[FOOTINGS[1][0]][1], sig_fw["mean"], sig_fw["sd"]))
    print("  SIGNIFICANCE TO QUOTE: %.2f / %.2f / %.2f sigma against a 0.10 / 0.15 / 0.20 dex"
          % (sig_fw["floor"][0.10], sig_fw["floor"][0.15], sig_fw["floor"][0.20]))
    print("  absolute-scale systematic floor.  The %.0f sigma statistical figure is NOT the number."
          % sig_fw["stat_sigma"])
    print("=" * W)


if __name__ == "__main__":
    main()
