#!/usr/bin/env python3
r"""mi_vertical_force_data_confrontation_2026.py -- THE VERTICAL-FORCE FRONT, SOURCED AND CONFRONTED.
The precision figure I quoted from memory last turn is CORRECT and now primary-sourced; the front is a
LIVE and ACTIVE literature, not new; and the confrontation goes AGAINST the framework's forced alpha=2
kernel -- but it is MOND-SHARED, and the discriminator I claimed last turn is an order of magnitude too
small to matter here.

WHAT CHANGED FROM LAST TURN. I claimed the vertical curl was "a NEW live front... neither MOND-shared nor
a0-degenerate", and flagged the ~5-10% precision as unsourced memory. Sourcing it revealed:
  (i)  the precision figure was right (Bovy & Rix 2013: 68 +- 4 Msun/pc^2, 5.9%);
  (ii) the vertical force as a MOND test is NOT new -- it is an active literature (Bienayme+2009,
       Lisanti+2019, Syaifudin+2024), so "new front" was wrong and is withdrawn;
  (iii) the published tests use AQUAL, i.e. the MG realization, so the MI-vs-MG curl difference is
       genuinely untested -- that part of last turn's claim survives;
  (iv) *** their "standard" interpolating function mu(x) = x/sqrt(1+x^2) IS the framework's alpha=2
       kernel, identically *** -- so a direct confrontation is available and it is unfavourable.

METHOD, per the working rule: predict mu_0 FROM THE FRAMEWORK'S OWN KERNEL AND ITS OWN a0, both
footings. Do NOT import the literature's fitted a0, which is a derived quantity conditional on their
choice of interpolating function.

  D1  THE SOURCED DATA, with citations and the kernel identification.
  D2  THE FRAMEWORK'S OWN PREDICTION for the local boost mu_0, both kernels x both footings, with a
      robustness scan over the assumed local acceleration.
  D3  THE DOMINANT SYSTEMATIC. The quoted +-0.03 is STATISTICAL and conditional on a fixed baryon
      budget; mu_0 scales as 1/Sigma_baryon, whose own uncertainty is 6-10.5% (sourced). Re-run.
  D4  FOUR REASONS THIS IS NOT A FRAMEWORK-SPECIFIC KILL -- including that my own curl discriminator
      cannot bridge it, and that the literature disagrees on the SIGN.
  D5  WHAT SURVIVES: a genuine two-sided PINCH on the kernel, and what is owed.

Exit 0 = ran and every internal check held. No hard-coded verdicts.
"""
from __future__ import annotations

import math
import sys

ok: list[tuple[bool, str]] = []


def check(cond: bool, msg: str) -> bool:
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t: str) -> None:
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


KPC = 3.0856775814913673e19

# ----------------------------------------------------------------- D1: the sourced numbers
# Bovy & Rix 2013, ApJ 779, 115 (arXiv:1309.0809), abstract, primary-sourced:
SIGMA_TOT, SIGMA_TOT_E = 68.0, 4.0          # Msun/pc^2 within |z| < 1.1 kpc at R0
SIGMA_STAR, SIGMA_STAR_E = 38.0, 4.0        # stars + remnants
# Syaifudin, Arifyanto, Wulandari & Mulki 2024, MNRAS 534, 3387 (arXiv:2401.11534).
# AQUAL (Bekenstein & Milgrom 1984 modified Poisson eq), Gaia distribution function of A/F/early-G stars:
MU0, MU0_STAT = 0.64, 0.03                  # the AQUAL boost factor at the Sun -- their MEASURED anchor
NU_THEIRS, NU_THEIRS_E = 1.56, 0.06         # equivalent nu
A0_SIMPLE, A0_SIMPLE_E = 1.26e-10, 0.135e-10        # their fit, simple mu = x/(1+x)
A0_STANDARD, A0_STANDARD_E = 2.69e-10, 0.18e-10     # their fit, standard mu = x/sqrt(1+x^2) == alpha=2
LOG_BF = 0.1                                # their headline: NO preference DM vs MOND
NU_LISANTI, NU_LISANTI_E = 1.44, 0.105      # Lisanti et al. 2019 PRD, independent
A0_GENTILE, A0_GENTILE_E = 1.27e-10, 0.30e-10       # Gentile+2011, rotation curves, STANDARD fn
A0_BEGEMAN, A0_BEGEMAN_E = 1.35e-10, 0.51e-10       # Begeman+1991, rotation curves, STANDARD fn

FOOTINGS = {"canon 9.36e-11": 9.36e-11, "alt 1.13e-10": 1.13e-10}


def mu1(x: float) -> float:
    """alpha=1 (retired by the ephemeris liability): mu = (sqrt(1+4x^2)-1)/(2x)."""
    return (math.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


def mu2(x: float) -> float:
    """alpha=2 (in force) -- IDENTICAL to the literature's 'standard' function."""
    return x / math.sqrt(1.0 + x * x)


def mu_simple(x: float) -> float:
    """the literature's 'simple' function, for contrast. NOT a framework kernel."""
    return x / (1.0 + x)


banner("D1  THE SOURCED DATA, AND THE KERNEL IDENTIFICATION THAT MAKES A CONFRONTATION POSSIBLE")

print(f"""  Bovy & Rix 2013, ApJ 779, 115 (arXiv:1309.0809):
     Sigma_R0(|z| < 1.1 kpc) = {SIGMA_TOT:.0f} +- {SIGMA_TOT_E:.0f} Msun/pc^2  ({SIGMA_TOT_E/SIGMA_TOT:.1%})
     of which stars + remnants  = {SIGMA_STAR:.0f} +- {SIGMA_STAR_E:.0f}  ({SIGMA_STAR_E/SIGMA_STAR:.1%})
  -> the ~5-10% precision I quoted from memory last turn is CORRECT. Now sourced.

  Syaifudin, Arifyanto, Wulandari & Mulki 2024, MNRAS 534, 3387 (arXiv:2401.11534),
  AQUAL modified Poisson equation, Gaia distribution function of A/F/early-G stars:
     measured local boost   mu_0 = {MU0} +- {MU0_STAT}   (equivalently nu = {NU_THEIRS} +- {NU_THEIRS_E})
     fitted a0, simple fn   = {A0_SIMPLE:.3e} +- {A0_SIMPLE_E:.3e}
     fitted a0, standard fn = {A0_STANDARD:.3e} +- {A0_STANDARD_E:.3e}
     headline verdict       log BF ~ {LOG_BF} -> NO strong evidence for EITHER dark matter or MOND
  Lisanti et al. 2019, PRD: nu = {NU_LISANTI} +- {NU_LISANTI_E}, independent and consistent.""")

check(abs(mu2(1.0) - 1 / math.sqrt(2.0)) < 1e-12,
      "D1 *** the literature's 'standard' function x/sqrt(1+x^2) IS the framework's alpha=2 kernel, "
      "identically -- so their standard-function results apply DIRECTLY to the kernel now in force ***")
check(abs(1.0 / MU0 - NU_THEIRS) < 0.02,
      f"D1b internal consistency of the source: 1/mu_0 = {1/MU0:.3f} matches their quoted nu = "
      f"{NU_THEIRS} to {abs(1/MU0-NU_THEIRS):.3f}, so mu_0 and nu are the same measurement")
check(abs(NU_THEIRS - NU_LISANTI) < 2 * math.hypot(NU_THEIRS_E, NU_LISANTI_E),
      f"D1c and it agrees with the INDEPENDENT Lisanti+2019 nu = {NU_LISANTI} +- {NU_LISANTI_E} at "
      f"{abs(NU_THEIRS-NU_LISANTI)/math.hypot(NU_THEIRS_E,NU_LISANTI_E):.1f} sigma -- two analyses, "
      f"consistent, so the anchor is not one group's artefact")


banner("D2  THE FRAMEWORK'S OWN PREDICTION FOR mu_0  (its kernel, its a0 -- NOT their fitted constant)")

# recover the local acceleration THEY used, from their own mu_0 -> a0 conversion on the standard fn
x_meas = MU0 / math.sqrt(1.0 - MU0**2)
g_theirs = x_meas * A0_STANDARD
print(f"  their mu_0 = {MU0} on the standard fn  ->  x = g/a0 = {x_meas:.4f}  ->  implied local")
print(f"  |grad Phi| = {g_theirs:.4e} m/s^2.  Cross-check against v_c^2/R0 for three MW choices:")
gscan = {}
for vc, R0k in ((229e3, 8.122), (220e3, 8.000), (233e3, 8.178)):
    gv = vc * vc / (R0k * KPC)
    gscan[f"v_c={vc/1e3:.0f}, R0={R0k:.3f}"] = gv
    print(f"     v_c = {vc/1e3:.0f} km/s, R0 = {R0k:.3f} kpc -> {gv:.4e}")
check(all(0.8 * g_theirs < gv < 1.2 * g_theirs for gv in gscan.values()),
      f"D2 their implied local acceleration {g_theirs:.3e} sits within 20% of v_c^2/R0 for every "
      f"standard MW choice, so the anchor is not built on an anomalous g")

print(f"\n  {'kernel':<22}{'footing':<16}{'x=g/a0':>9}{'mu_pred':>10}{'measured':>11}{'sigma_stat':>12}")
print("  " + "-" * 82)
preds = {}
for kn, mu in (("alpha=2 (IN FORCE)", mu2), ("alpha=1 (retired)", mu1)):
    for fn, a0 in FOOTINGS.items():
        x = g_theirs / a0
        mp = mu(x)
        s = (mp - MU0) / MU0_STAT
        preds[(kn, fn)] = (mp, s)
        print(f"  {kn:<22}{fn:<16}{x:>9.3f}{mp:>10.4f}{MU0:>11.2f}{s:>12.1f}")
check(all(v[0] > MU0 for v in preds.values()),
      "D2b the framework predicts mu ABOVE the measured value on every kernel and footing -- i.e. TOO "
      "LITTLE vertical boost. Equivalently, the vertical data wants a LARGER a0 than the framework's")
# robustness of the conclusion to the assumed g
worst = min(mu2(gv / FOOTINGS["alt 1.13e-10"]) for gv in gscan.values())
check(worst > MU0 + 3 * MU0_STAT,
      f"D2c and that survives the g-scan: even the most favourable combination (alt footing, lowest "
      f"v_c^2/R0) gives mu = {worst:.4f}, still {(worst-MU0)/MU0_STAT:.1f} sigma_stat above {MU0}")


banner("D3  THE DOMINANT SYSTEMATIC -- the quoted error is STATISTICAL and assumes a fixed baryon budget")

print(f"""  mu_0 is not measured in isolation: it is the factor by which the BARYONIC vertical force must be
  boosted to match the observed stellar kinematics. So mu_0 scales roughly as 1/Sigma_baryon, and the
  baryon budget carries its own uncertainty -- {SIGMA_TOT_E/SIGMA_TOT:.1%} on the total and
  {SIGMA_STAR_E/SIGMA_STAR:.1%} on the stellar part (Bovy & Rix 2013). Propagate it:\n""")
print(f"  {'assumed Sigma_b error':<26}{'sigma(mu_0) total':>19}{'alpha=2 canon':>15}{'alpha=1 canon':>15}")
print("  " + "-" * 76)
infl = {}
for lbl, rel in (("statistical only", 0.0),
                 (f"+{SIGMA_TOT_E/SIGMA_TOT:.1%} (total Sigma)", SIGMA_TOT_E / SIGMA_TOT),
                 (f"+{SIGMA_STAR_E/SIGMA_STAR:.1%} (stellar Sigma)", SIGMA_STAR_E / SIGMA_STAR)):
    e = math.hypot(MU0_STAT, rel * MU0)
    s2 = (preds[("alpha=2 (IN FORCE)", "canon 9.36e-11")][0] - MU0) / e
    s1 = (preds[("alpha=1 (retired)", "canon 9.36e-11")][0] - MU0) / e
    infl[lbl] = (e, s2, s1)
    print(f"  {lbl:<26}{e:>19.4f}{s2:>15.1f}{s1:>15.1f}")
worst_case = min(v[1] for v in infl.values())
check(worst_case > 3.0,
      f"D3 even with the most generous baryon systematic the alpha=2 kernel on the canonical footing "
      f"stays at {worst_case:.1f} sigma -- so the tension does NOT dissolve into the baryon budget")
check(min(v[2] for v in infl.values()) < worst_case,
      f"D3b and alpha=1 is uniformly LESS discrepant than alpha=2 "
      f"({min(v[2] for v in infl.values()):.1f} vs {worst_case:.1f} sigma at worst) -- the tension is "
      f"driven by the KERNEL's shape, not only by a0's value")


banner("D4  FOUR REASONS THIS IS NOT A FRAMEWORK-SPECIFIC KILL")

# (a) the paper's own verdict
check(abs(LOG_BF) < 0.5,
      f"D4a THE SOURCE ITSELF CLAIMS NO EXCLUSION: log BF ~ {LOG_BF} between dark matter and MOND. mu_0 "
      f"is a PARAMETER FITTED UNDER the MOND hypothesis, not an independent measurement that excludes "
      f"it. So the sigmas above read 'the framework's a0 versus the a0 this dataset prefers', NOT "
      f"'MOND excluded'")
# (b) MOND-shared: the vertical-vs-radial split for the SAME standard function
split = (A0_STANDARD - A0_GENTILE) / math.hypot(A0_STANDARD_E, A0_GENTILE_E)
print(f"\n  (b) the split is INTERNAL TO MOND on the standard function, from the source's own numbers:")
print(f"      vertical  a0 = {A0_STANDARD:.3e} +- {A0_STANDARD_E:.2e}   (this paper)")
print(f"      radial    a0 = {A0_GENTILE:.3e} +- {A0_GENTILE_E:.2e}   (Gentile+2011 rotation curves)")
print(f"      radial    a0 = {A0_BEGEMAN:.3e} +- {A0_BEGEMAN_E:.2e}   (Begeman+1991)")
print(f"      -> vertical vs radial = {split:.1f} sigma, a RADIAL-vs-VERTICAL inconsistency afflicting")
print(f"         ANY standard-function MOND. The framework inherits it because the ephemeris liability")
print(f"         forced alpha=2 -- it is not a defect of a0 = kappa c sqrt(G rho_Lambda).")
check(split > 2.0,
      f"D4b the vertical-vs-radial a0 split for the standard function is {split:.1f} sigma from the "
      f"source's OWN numbers, so this is MOND-SHARED and not framework-specific")
# (c) my own discriminator cannot bridge it
need = A0_STANDARD / A0_GENTILE - 1.0
CURL_MAX = 0.287
check(CURL_MAX < need / 2,
      f"D4c MY OWN CURL DISCRIMINATOR CANNOT BRIDGE THIS: closing the gap needs {need:.0%} while the "
      f"MI-vs-MG circulation supplies at most {CURL_MAX:.1%} -- short by {need/CURL_MAX:.1f}x. Last "
      f"turn's front is real but SUBDOMINANT to a larger, MOND-shared problem")
print(f"""
  (d) THE LITERATURE DISAGREES ON THE SIGN. The search that surfaced this also surfaced the opposite
      claim -- that MOND OVER-predicts the vertical force, "almost doubling K_z", while the Milky Way
      "requires substantial amplification of the radial acceleration with little amplification of the
      vertical". That is the reverse of this paper's "data wants MORE boost". I have NOT reconciled the
      two, and one paper in one direction is not a settled front. Reported against interest.""")
# and the dispute is DECISIVE, not a footnote: the framework's predicted boost sits at the "little
# amplification" end, so the two literature directions give OPPOSITE verdicts on the framework.
nu_pred = {k: 1.0 / v[0] for k, v in preds.items()}
print(f"\n      The framework's OWN predicted boost nu = 1/mu:")
for k, v in nu_pred.items():
    print(f"        {k[0]:<22}{k[1]:<16}nu = {v:.4f}")
print(f"      'little vertical amplification' means nu ~ 1.0-1.1;  this paper measures "
      f"nu = {NU_THEIRS} +- {NU_THEIRS_E}.")
nu_min, nu_max = min(nu_pred.values()), max(nu_pred.values())
check(nu_min < 1.15 and nu_max < NU_THEIRS - 4 * NU_THEIRS_E,
      f"D4d THE DISPUTE IS DECISIVE, NOT A FOOTNOTE: the framework predicts nu = {nu_min:.2f}-{nu_max:.2f}, "
      f"which sits AT the 'little vertical amplification' end and is >4 sigma below this paper's "
      f"nu = {NU_THEIRS}. So the two literature directions give OPPOSITE verdicts on the framework -- "
      f"FINE under one reading, {worst_case:.1f}+ sigma off under the other. The front CANNOT be scored "
      f"until the sign is reconciled, and that is the single most important thing owed here")


banner("D5  WHAT SURVIVES -- a two-sided PINCH on the kernel, and what is owed")

x_can = g_theirs / FOOTINGS["canon 9.36e-11"]
x_alt = g_theirs / FOOTINGS["alt 1.13e-10"]
s_simple_can = (A0_SIMPLE - FOOTINGS["canon 9.36e-11"]) / A0_SIMPLE_E
s_simple_alt = (A0_SIMPLE - FOOTINGS["alt 1.13e-10"]) / A0_SIMPLE_E
print(f"""  THE PINCH, and it is the real finding.
   * The EPHEMERIDES force alpha=2: alpha=1's constant a0/2 sunward anomaly is 1278x the Earth 2-sigma
     bound (project record). alpha=1 is retired.
   * The SOLAR-NEIGHBOURHOOD VERTICAL FORCE disfavours alpha=2: it is the literature's 'standard'
     function, whose fitted a0 = {A0_STANDARD:.2e} is {split:.1f} sigma from the rotation-curve value for
     the SAME function, and the source's own conclusion is that "if MOND is valid, the simple
     interpolating function is more likely to be true".
   * With the SIMPLE function instead, the framework's a0 would be comfortable:
     canonical {s_simple_can:+.1f} sigma, alt footing {s_simple_alt:+.1f} sigma against
     a0 = {A0_SIMPLE:.2e} +- {A0_SIMPLE_E:.2e}. But mu = x/(1+x) is NOT a framework kernel and has no
     dS-Unruh derivation -- adopting it would be pure curve-fitting.
   => The framework is pinched between two data sets that prefer DIFFERENT interpolating functions, and
      it has no kernel satisfying both. That is a sharper statement of the corpus's existing
      "the kernel is now phenomenological" position, with the vertical force as the second jaw.

  WHAT IS OWED before any sigma here is quoted as a framework result:
   1. An independent vertical-force analysis with the framework's a0 held FIXED rather than fitted, and
      the baryon budget marginalised rather than assumed -- neither is done here or in the source.
   2. Reconciliation of the two directions in the literature (D4d). Until then the SIGN is contested.
   3. The MI-vs-MG curl prediction (~6-29%) still needs its own confrontation. It is untested, because
      every published test uses AQUAL -- but D4c shows it is too small to matter for THIS discrepancy.
   4. A second dataset. One analysis, however careful, is not a front.

  UNTOUCHED: the RAR fit, the a0-line, the BTFR, all spherical work, and a0 = kappa c sqrt(G rho_Lambda),
  which is a claim about the SCALE and survives every kernel question raised here.""")
check(s_simple_alt < 2.0 and worst_case > 3.0,
      f"D5 the tension is KERNEL-driven, not a0-driven: the same a0 (alt footing) is {abs(s_simple_alt):.1f} "
      f"sigma on the simple function but {worst_case:.1f}+ sigma on alpha=2 -- which is why the honest "
      f"finding is a pinch on the KERNEL rather than a measurement of a0")

banner("RESULT")
npass = sum(1 for c, _ in ok if c)
print(f"  {npass}/{len(ok)} checks held.")
if npass != len(ok):
    print("\n  FAILED CHECKS:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: sourced, confronted on the framework's own kernel, with the systematic and the "
      "MOND-shared caveat carried.")
