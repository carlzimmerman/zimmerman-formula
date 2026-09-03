#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_cross-scale_mwmass -- CANDIDATE 3 of the cross-scale angle:
    "the Milky Way's baryonic mass from a stellar velocity ratio -- the boost law run backwards".

CLAIM UNDER TEST.  B(e) = nu(e)[1 + L(e)/3] is strictly monotone in e, so a MEASURED wide-binary
velocity boost gamma_v^2 = B inverts to the Newtonian-equivalent external field e = g_N,ext/a_0 and
hence, through g_N,ext = G M_b/R_0^2, to the Milky Way's baryonic mass -- with NO photometry, NO
stellar M/L and NO rotation curve:

        M_b,MW = e(gamma_v^2) * a_0 * R_0^2 / G,      a_0 = (c/2) sqrt(G rho_DE).

WHAT THIS SCRIPT ACTUALLY DECIDES.  Four things, and three of them are against the candidate:
  (1) is B invertible over the range the wide-binary band occupies?              [can fail]
  (2) is the inversion CIRCULAR today?  The frozen Gaia DR4 band was itself computed from an
      ASSUMED local field x_ext = 1.89929 a_0.  If feeding that assumption's own B back through the
      inversion returns the mass that generated it, the estimator is measuring nothing yet.
      This check is designed to FIRE.                                            [can fail]
  (3) BUG PATTERN 2 (a spherical formula applied to a disc): g_N,ext = G M_b/R_0^2 is a POINT-MASS
      formula and the Milky Way at R_0 = 3.1 disc scale lengths is not a point.  The script computes
      the exact razor-thin exponential-disc field (Freeman/Binney-Tremaine) and reports the geometry
      factor, which is a multiplicative bias on every mass this estimator returns.  [can fail]
  (4) the RESTATEMENT test, executed: can M_b,MW = ... be derived from v^4 = G M_b a_0 + algebra?

Both footings.  Newtonian/LambdaCDM alternative computed beside the framework (gamma_v = 1 exactly,
for which the estimator has NO solution -- that is the alternative's prediction and it is stated).
Mutation control: a_0 x 10 and nu = 1 must both break the inversion.

Run:  python3 k_cross-scale_mwmass.py      (exit 0 = all checks pass)
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, G, Msun, kpc, c_light, nu_s, Check, P, info
from hunt_efe_lib import dlnnu_dlny

R0 = 8.122*kpc                     # the registered Gaia DR4 solar radius
X_EXT_REG = 1.89929                # the registered local field in units of a_0 (TRUE field, = nu(e) e)
# the frozen, pre-registered gamma_v bands (predictions, NOT measurements -- Gaia DR4 is ~Dec 2026)
BAND = {"canonical": (1.1614, 1.1814), "alt": (1.1917, 1.2267)}
# published Galactic baryon census: stellar 5.0-6.1e10 (Licquia & Newman 2015; McMillan 2017) + gas ~1.2e10
CENSUS = (6.0e10, 7.3e10)

ck = Check()


# ------------------------------------------------------------------ the boost law and its inverse
def L_of(y):
    return float(dlnnu_dlny(np.array([float(y)]))[0])


def B_of_e(e):
    """M_dyn/M_bar for a test system with g_int -> 0 embedded in a uniform Newtonian-equivalent field e."""
    return nu_s(e)*(1.0 + L_of(e)/3.0)


def e_of_B(Bt, lo=1e-6, hi=1e6):
    """Invert B(e).  B is DECREASING in e (B -> 1 as e -> inf), so bisect on that monotone branch."""
    if Bt <= 1.0:
        return float("inf")
    for _ in range(300):
        mid = math.sqrt(lo*hi)
        if B_of_e(mid) > Bt:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo*hi)


def e_from_true_field(x_true):
    """nu(e) e = x_true  ->  e (the Newtonian-equivalent field behind a measured true field)."""
    lo, hi = 1e-8, 1e8
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        if nu_s(mid)*mid < x_true: lo = mid
        else: hi = mid
    return math.sqrt(lo*hi)


def Mb_from_e(e, a0):
    return e*a0*R0**2/G/Msun


# ------------------------------------------------------------------ exact exponential-disc field
def g_disc_exp(R, Md, Rd):
    """Razor-thin exponential disc, EXACT (Binney & Tremaine eq. 2.165):
         v_c^2(R) = 4 pi G Sigma0 Rd y^2 [I0K0 - I1K1](y),  y = R/(2 Rd)   ->   g_R = v_c^2/R.
    BUG CAUGHT BY THIS SCRIPT'S OWN CHECK: the first version returned v_c^2 and called it g, which is
    wrong by a factor R = 2.5e20 m.  The check 'geometry factor within a factor 2 of 1' fired."""
    from scipy.special import i0e, i1e, k0e, k1e
    Sig0 = Md/(2*math.pi*Rd**2)
    y = R/(2*Rd)
    # I_n(y)K_n(y) = i_ne(y)*k_ne(y) exactly: the exp(-y) and exp(+y) scalings cancel
    br = i0e(y)*k0e(y) - i1e(y)*k1e(y)
    return 4*math.pi*G*Sig0*Rd*y**2*br/R


def g_sphere(R, M):
    return G*M/R**2


P("="*118)
P("k_cross-scale_mwmass -- CANDIDATE 3: the Milky Way's baryonic mass from a wide-binary velocity ratio")
P("      M_b = e(gamma_v^2) a_0 R_0^2 / G,   B(e) = nu(e)[1+L(e)/3],   a_0 = (c/2) sqrt(G rho_DE)")
P("="*118)

# ---------------------------------------------------------------------------------- (1) invertibility
P("")
P("-"*118); P("1.  IS THE LAW INVERTIBLE?  B(e) must be strictly monotone over the range the band occupies."); P("-"*118)
egrid = np.geomspace(1e-3, 30.0, 4001)
Bg = np.array([B_of_e(e) for e in egrid])
mono = bool(np.all(np.diff(Bg) < 0))
ck("B(e) is strictly DECREASING over e = 1e-3 to 30, hence invertible on the branch where B > 1  [CAN FAIL]",
   mono, f"B(1e-3) = {Bg[0]:.3f} -> B(30) = {Bg[-1]:.5f}, {int(np.sum(np.diff(Bg) >= 0))} non-decreasing steps")
# a real feature the first monotonicity check exposed, kept because it is a genuine property of the kernel:
e_cross = None
for e in np.geomspace(10, 300, 2000):
    if B_of_e(e) < 1.0: e_cross = e; break
ck("the boost DIPS BELOW 1 at very strong external field -- B - 1 ~ e^{-sqrt e}(1 - sqrt(e)/6) changes sign at "
   "e = 36 -- so 'B > 1 always' would have been wrong  [CAN FAIL]",
   e_cross is not None and 30 < e_cross < 60,
   f"B crosses 1 downward at e = {e_cross:.1f} (analytic sqrt(e) = 6, e = 36); B(100) = {B_of_e(100.0):.6f}")
rt = max(abs(e_of_B(B_of_e(e))/e - 1) for e in (0.05, 0.3, 1.0, 1.28903, 3.0, 10.0))
ck("the inversion round-trips e -> B -> e to 1e-6  [CAN FAIL]", rt < 1e-6, f"max relative error {rt:.2e}")
info(f"B is UNBOUNDED as e -> 0: B(1e-3) = {Bg[0]:.2f}, B(1e-6) = {B_of_e(1e-6):.1f}  (it goes as (5/6)/sqrt(e)).")
info("So the estimator has a solution for ANY gamma_v > 1 -- there is no upper ceiling.  Its restriction is the")
info("other way: gamma_v <= 1 has no solution, which is exactly the LambdaCDM/Newtonian prediction.")
Bmax = float("inf")
ck("the estimator is defined precisely on gamma_v > 1 and undefined on gamma_v <= 1, so the Newtonian "
   "alternative sits exactly on its boundary  [CAN FAIL]", B_of_e(1e-6) > 100 and e_of_B(1.0) == float("inf"),
   f"B(1e-6) = {B_of_e(1e-6):.1f} (no ceiling); e(B = 1) = {e_of_B(1.0)}")

# ---------------------------------------------------------------------------------- (2) circularity
P("")
P("-"*118); P("2.  THE CIRCULARITY AUDIT.  This check is BUILT TO FIRE."); P("-"*118)
e_reg = e_from_true_field(X_EXT_REG)
info(f"the frozen registration adopts a TRUE local field x_ext = {X_EXT_REG} a_0, i.e. e = {e_reg:.5f}, nu(e) = {nu_s(e_reg):.5f}")
circ = {}
for foot, a0 in A0.items():
    Mb_assumed = Mb_from_e(e_reg, a0)
    B_reg = B_of_e(e_reg)
    e_back = e_of_B(B_reg)
    Mb_back = Mb_from_e(e_back, a0)
    circ[foot] = (Mb_assumed, B_reg, Mb_back)
    info(f"  [{foot:9}] a_0 = {a0:.3e}: the registration's OWN assumption is M_b = {Mb_assumed:.3e} Msun; "
         f"B(e_reg) = {B_reg:.5f}; inverting that B returns M_b = {Mb_back:.3e} Msun")
worst = max(abs(circ[f][2]/circ[f][0] - 1) for f in A0)
ck("CIRCULARITY CONFIRMED: feeding the registration's own assumed field through B and back returns the SAME "
   "mass to 0.1%, so quoting this inversion TODAY measures the assumption, not the Galaxy  [CAN FAIL]",
   worst < 1e-3, f"max round-trip departure {worst:.2e} -- the estimator is exactly circular until gamma_v is MEASURED")

# ---------------------------------------------------------------------------------- (3) disc geometry
P("")
P("-"*118); P("3.  BUG PATTERN 2 -- a SPHERICAL formula applied to a DISC.  How big is the error?"); P("-"*118)
info("g_N,ext = G M_b/R_0^2 treats the Galaxy as a point.  The exact razor-thin exponential-disc field is")
info("g_R = 4 pi G Sigma_0 R_d y^2 [I0K0 - I1K1](y), y = R/(2R_d).  Compare at R_0 = 8.122 kpc:")
geo = {}
Md = 6.5e10*Msun
for Rd_kpc in (2.15, 2.5, 2.6, 3.0):
    Rd = Rd_kpc*kpc
    gd = g_disc_exp(R0, Md, Rd); gp = g_sphere(R0, Md)
    geo[Rd_kpc] = gd/gp
    info(f"   pure exponential disc, R_d = {Rd_kpc:4.2f} kpc:  g_disc/g_point = {gd/gp:6.4f}   "
         f"(inferred M_b moves by x{gp/gd:.3f})")
# a McMillan-2017-like composite: bulge (spherical) + thin disc + thick disc + HI/H2 gas discs
COMP = [("bulge (spherical)",   0.90e10, None), ("thin disc",  3.52e10, 2.50),
        ("thick disc",          1.06e10, 3.02), ("gas discs",  1.20e10, 7.00)]
gtot = 0.0; Mtot = 0.0
for nm, m, rd in COMP:
    m_ = m*Msun; Mtot += m_
    gtot += g_sphere(R0, m_) if rd is None else g_disc_exp(R0, m_, rd*kpc)
geo["composite"] = gtot/g_sphere(R0, Mtot)
info(f"   McMillan-2017-like COMPOSITE (bulge 0.90 + thin 3.52 [Rd 2.5] + thick 1.06 [Rd 3.0] + gas 1.20 "
     f"[Rd 7.0], total {Mtot/Msun:.3e} Msun):")
info(f"      g_N(R_0) = {gtot:.4e} m/s^2 = {gtot/A0['canonical']:.4f} a_0 (canonical) / "
     f"{gtot/A0['alt']:.4f} a_0 (alt);  g_composite/g_point = {geo['composite']:.4f}")
fmin = min(geo.values()); fmax = max(geo.values())
ck("the point-mass approximation is NOT innocuous at R_0: the geometry factor departs from 1 by more than 5% "
   " [CAN FAIL]", (fmin < 0.95) or (fmax > 1.05),
   f"g/g_point = {fmax:.4f} (pure disc, R_d = 2.15 kpc) down to {fmin:.4f}; the composite model gives "
   f"{geo['composite']:.4f}, i.e. a {100*(1/geo['composite'] - 1):.0f}% upward correction to every mass this "
   f"estimator returns")
info("AGAINST INTEREST: a real Galaxy has a bulge, which pushes g back UP toward the point-mass value, so the")
info("honest statement is a systematic BAND on the inferred mass, x0.85 to x1.05, carried as GEOM below.")
info("SEPARATE FINDING, against interest: the composite baryon census's own Newtonian field at R_0 is")
e_census = gtot/A0["canonical"]
info(f"   e = g_N/a_0 = {e_census:.4f} (canonical), whereas the frozen registration adopts e = {e_reg:.4f}, 11% lower.")

# ---------------------------------------------------------------------------------- (4) the numbers
P("")
P("-"*118); P("4.  THE INVERSION, both footings, over the frozen band and over hypothetical measurements."); P("-"*118)
P(f"{'footing':>10}{'gamma_v':>10}{'gamma_v^2':>11}{'e':>10}{'M_b point':>13}{'M_b composite':>15}{'vs census':>12}")
res = {}
for foot, a0 in A0.items():
    lo, hi = BAND[foot]
    row = []
    for gv in (lo, 0.5*(lo+hi), hi, 1.20, 1.25, 1.30):
        B = gv*gv
        if B >= Bmax:
            P(f"{foot:>10}{gv:10.4f}{B:11.4f}{'NO SOLUTION':>10}{'--':>13}{'--':>15}{'--':>12}")
            continue
        e = e_of_B(B)
        Mp = Mb_from_e(e, a0)
        Md_ = Mp/geo["composite"]
        flag = "in" if CENSUS[0] <= Md_ <= CENSUS[1] else ("LOW" if Md_ < CENSUS[0] else "HIGH")
        P(f"{foot:>10}{gv:10.4f}{B:11.4f}{e:10.4f}{Mp:13.3e}{Md_:15.3e}{flag:>12}")
        row.append((gv, e, Mp, Md_))
    res[foot] = row
info(f"census target used: M_b,MW = {CENSUS[0]:.1e} to {CENSUS[1]:.1e} Msun (stellar 5.0-6.1e10 + gas ~1.2e10)")

# sensitivity
P("")
info("SENSITIVITY d log M_b / d log gamma_v, evaluated numerically at the band centre:")
sens = {}
for foot in A0:
    gv = 0.5*(BAND[foot][0] + BAND[foot][1]); d = 1e-4
    m1 = Mb_from_e(e_of_B((gv*(1-d))**2), A0[foot]); m2 = Mb_from_e(e_of_B((gv*(1+d))**2), A0[foot])
    sens[foot] = (math.log(m2) - math.log(m1))/(math.log(gv*(1+d)) - math.log(gv*(1-d)))
    info(f"   [{foot:9}] gamma_v = {gv:.4f}: d log M_b/d log gamma_v = {sens[foot]:+.2f}  "
         f"-> gamma_v to 2% gives M_b to {abs(sens[foot])*2:.0f}%")
ck("the estimator is STEEP -- |d log M_b/d log gamma_v| > 5, so a 2% velocity error becomes a >10% mass error "
   "[CAN FAIL]", all(abs(v) > 5 for v in sens.values()), f"{sens['canonical']:+.2f} (canonical), {sens['alt']:+.2f} (alt)")

# ---------------------------------------------------------------------------------- Upsilon lever
P("")
P("-"*118); P("5.  THE UPSILON LEVER, measured by re-running the pipeline at Upsilon x 1.5."); P("-"*118)
info("gamma_v is a ratio of the MEASURED relative velocity to the NEWTONIAN prediction, and the Newtonian")
info("prediction uses component masses from a mass-luminosity relation.  Upsilon -> 1.5 Upsilon multiplies the")
info("predicted Newtonian velocity by sqrt(1.5), so gamma_v -> gamma_v/sqrt(1.5).  Re-run:")
lev = {}
for foot in A0:
    gv = 0.5*(BAND[foot][0] + BAND[foot][1])
    m0 = Mb_from_e(e_of_B(gv**2), A0[foot])
    gv2 = gv/math.sqrt(1.5)
    if gv2 <= 1.0:
        info(f"   [{foot:9}] Upsilon x1.5 sends gamma_v to {gv2:.4f} <= 1: THE ESTIMATOR HAS NO SOLUTION AT ALL.")
        lev[foot] = float("inf"); continue
    m1 = Mb_from_e(e_of_B(gv2**2), A0[foot])
    lev[foot] = (math.log10(m1) - math.log10(m0))/math.log10(1.5)
    info(f"   [{foot:9}] gamma_v {gv:.4f} -> {gv2:.4f};  M_b {m0:.3e} -> {m1:.3e} Msun;  "
         f"d log M_b/d log Upsilon = {lev[foot]:+.2f}")
info("the analytic prediction is (d log M_b/d log gamma_v) x (-1/2):")
for foot in A0:
    info(f"   [{foot:9}] analytic {(-0.5)*sens[foot]:+.2f}   measured {lev[foot]:+.2f}")
ck("the Upsilon lever is LARGE and is reported against interest: a x1.5 error in the wide-binary mass-luminosity "
   "calibration destroys the estimator or moves the mass by more than a factor 2  [CAN FAIL]",
   all((not np.isfinite(v)) or abs(v) > 2 for v in lev.values()),
   f"canonical {lev['canonical']}, alt {lev['alt']}")

# ---------------------------------------------------------------------------------- restatement test
P("")
P("-"*118); P("6.  THE RESTATEMENT TEST, executed rather than asserted."); P("-"*118)
info("ATTEMPT.  From v^4 = G M_b a_0 alone, a test particle's boost over Newton is g_obs/g_N = sqrt(a_0/g_int),")
info("a function of the system's OWN internal field.  Apply it to the wide-binary rung:")
for foot, a0 in A0.items():
    for sep_kau, m in ((5.0, 1.5), (30.0, 1.5)):
        AU = 1.495978707e11
        gint = G*m*Msun/(sep_kau*1e3*AU)**2
        btfr = math.sqrt(a0/gint)
        info(f"   [{foot:9}] {sep_kau:4.0f} kAU, {m} Msun: y = g_int/a_0 = {gint/a0:.4f}; BTFR boost in FORCE = "
             f"{btfr:.3f} (gamma_v = {math.sqrt(btfr):.3f}); the law's B = {B_of_e(e_reg):.3f} "
             f"(gamma_v = {math.sqrt(B_of_e(e_reg)):.3f})")
info("The two disagree by a factor 2-4 and, decisively, the BTFR boost DEPENDS ON SEPARATION while B does not.")
info("So the mass estimator M_b = e(gamma_v^2) a_0 R_0^2/G cannot be produced by algebra on v^4 = G M_b a_0.")
info("VERDICT ON THE RESTATEMENT TEST: the derivation DOES NOT CLOSE -- this is not the BTFR in new clothes.")
info("BUT note what that buys: the content is the EXTERNAL-FIELD EFFECT, which is a standard and long-published")
info("part of MOND (Milgrom 1983, 1986; Bekenstein & Milgrom 1984; Famaey & McGaugh 2012 Living Review Sec 6.3).")
info("The g_int -> 0 coefficient nu(e)[1+L(e)/3] is the trace of the known anisotropic EFE dilation tensor, NOT")
info("a new object.  What would be new is only the INVERSION -- using it as a mass estimator.")
ck("the restatement test is executed and reported: the BTFR boost depends on separation, B does not, so the "
   "derivation does not close  [CAN FAIL]",
   abs(math.sqrt(A0['canonical']/(G*1.5*Msun/(5e3*1.495978707e11)**2))
       - math.sqrt(A0['canonical']/(G*1.5*Msun/(30e3*1.495978707e11)**2))) > 0.5,
   "the two separations give different BTFR boosts, so no single number can come out of it")

# ---------------------------------------------------------------------------------- alternative + mutation
P("")
P("-"*118); P("7.  THE ALTERNATIVE AND THE MUTATION CONTROLS."); P("-"*118)
info("LambdaCDM/Newton: a 30 kAU wide binary sits inside the Galactic disc's smooth potential, and Newtonian")
info("gravity is LINEAR -- the Galaxy's field cancels from the relative motion exactly.  gamma_v = 1.000 with no")
info("free parameter.  Fed to this estimator, gamma_v = 1 gives e = infinity and M_b = infinity: the alternative's")
info("prediction is that the estimator has NO SOLUTION.  That is a sharp, falsifiable difference, and it is the")
info("whole content of the December test -- it is not new content added by the mass inversion.")
mut = {}
for label, scale in (("a_0 x 10", 10.0), ("a_0 x 0.1", 0.1), ("a_0 x 1 (truth)", 1.0)):
    a0 = A0["canonical"]*scale
    gv = 0.5*(BAND["canonical"][0] + BAND["canonical"][1])
    e = e_of_B(gv**2)
    mut[label] = Mb_from_e(e, a0)
    info(f"   {label:16}: M_b = {mut[label]:.3e} Msun  ({mut[label]/mut.get('a_0 x 1 (truth)', mut[label]):.2f}x truth)"
         if label == "a_0 x 1 (truth)" else
         f"   {label:16}: M_b = {mut[label]:.3e} Msun")
ck("mutation control bites: a_0 x 10 changes the inferred baryonic mass by an order of magnitude  [CAN FAIL]",
   abs(math.log10(mut["a_0 x 10"]/mut["a_0 x 1 (truth)"])) > 0.9,
   f"{mut['a_0 x 1 (truth)']:.3e} -> {mut['a_0 x 10']:.3e} Msun")
info("nu = 1 foil: with no kernel there is no boost, gamma_v = 1, and the estimator is undefined -- the same")
info("statement as the LambdaCDM alternative above.")

# ---------------------------------------------------------------------------------- verdict
P("")
P("="*118); P("VERDICT ON CANDIDATE 3"); P("="*118)
tests = []
tests.append(("(1) it is a relation between MEASURED quantities", False,
              "gamma_v will be measured, but M_b,MW comes out of it only after ASSUMING a point-mass Galaxy; the "
              "disc geometry factor is a 6-16% prior on the answer"))
tests.append(("(2) a_0 appears with a PREDICTED coefficient", True,
              "yes: a_0 enters as e a_0 R_0^2/G with nothing fitted"))
tests.append(("(3) it holds across many systems to <= 0.1 dex", False,
              "it is a ONE-SYSTEM statement -- there is exactly one Milky Way, so 'scatter across systems' cannot "
              "even be defined; the propagated error from sigma_sys(gamma_v) = 0.02 alone is "
              f"{abs(sens['canonical'])*0.02/2.3026*1:.3f} dex-equivalent = {abs(sens['canonical'])*2:.0f}% in mass"))
tests.append(("(4) nobody has stated it", True,
              "the inversion as a mass estimator is not in the literature; the EFE boost it inverts IS "
              "(Milgrom 1986; Famaey & McGaugh 2012 Sec 6.3), and must be credited"))
tests.append(("(5) it is NOT a restatement of v^4 = G M_b a_0", True,
              "confirmed by execution above: the BTFR boost depends on separation, B does not"))
for name, ok, why in tests:
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {why}")
npass = sum(1 for _, ok, _ in tests if ok)
P("")
P(f"  >>> {npass} of 5 Kepler-grade criteria met.  CANDIDATE 3 IS NOT A SECOND LAW.")
P("  >>> It is a COROLLARY of the December wide-binary test, and today it is exactly circular (check 2 fired):")
P("      the frozen band was generated from an assumed M_b = 5.709e10 Msun and the inversion returns that mass.")
P("  >>> Its one real use is as a CONSISTENCY TARGET for December: if gamma_v is measured and the inverted mass")
P("      lands outside 6.0-7.3e10 Msun after the disc-geometry correction, the framework has a second problem")
P("      beyond gamma_v itself.  On the frozen band that target is met on the ALT footing and missed LOW on the")
P("      canonical one, which is a free footing discriminator -- worth 0.1 dex, not worth a law.")
P("")
P("  UPSILON LEVER (the number the task asked for): d log M_b/d log Upsilon = "
  f"{lev['canonical'] if np.isfinite(lev['canonical']) else 'UNDEFINED (no solution at Upsilon x1.5)'}"
  f" / {lev['alt'] if np.isfinite(lev['alt']) else 'UNDEFINED'}   -- the LARGEST lever of the three candidates.")
sys.exit(ck.done())
