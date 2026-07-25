#!/usr/bin/env python3
"""
wb_a0_amplitude_degeneracy.py -- CAN GAIA WIDE BINARIES DELIVER AN a0 AMPLITUDE,
OR ONLY A DEGENERATE PRODUCT?   (role: DEGENERACY TEST, 2026-07-25)
================================================================================
CONTEXT / WHY THIS SCRIPT EXISTS
  prep_2026/a0_line/reach_target.py + per_galaxy_budget.py (STEP A, committed):
  the gas-dominated a0-line box is 16.1% and ~76% of its VARIANCE is SHARED,
  non-averaging systematics (estimator 30% + Upsilon 25% + gas-cal 21%), so the
  dwarf-only floor is ~11.0-11.6%, ABOVE the ~6.31% needed to separate canonical
  a0 = cH_Lambda/Z = 9.355e-11 from the 1.13-1.20e-10 cluster at 3 sigma.
  HYPOTHESIS UNDER TEST: Gaia wide binaries (WB) carry ENTIRELY DIFFERENT
  systematics (hierarchical-triple contamination, deprojection, eccentricity
  priors, photometric masses), so a WB a0 constraint of comparable precision
  would beat the dwarf floor in a joint fit.
  THIS SCRIPT tests only the LOGICALLY PRIOR question: is a0's AMPLITUDE
  recoverable from a WB gamma measurement at all, or is it degenerate with the
  two-body coefficient C / the MI-vs-MG prescription? If the amplitude is not
  recoverable, orthogonality of systematics is moot.

FRAMEWORK ON ITS OWN TERMS (de Sitter-Unruh MODIFIED INERTIA -- not judged
through the standard-MOND lens, and NOT McGaugh's nu):
  a0 = c H_Lambda / Z = 9.36e-11 m/s^2 (canonical);  ALT footing 1.13e-10
  nu(y) = sqrt(1 + 1/y),  y = g_bar/a0,  i.e. g_obs = sqrt(g_bar^2 + g_bar a0)
  Both footings are carried on every load-bearing number (working-rule 4).
  CREDIT LINE (banked): nu = sqrt(1+1/y) is Milgrom 1999 PLA 253:273 eq 9; the
  framework's distinctive content is the cH_Lambda/Z COEFFICIENT + MI completion.

THE LAWS TESTED (all three, no cherry-picking)
  L1  no-EFE bridge (the task's law; Milgrom arXiv:2503.07106 linear/time-
      nonlocal, EFE EXACTLY absent by eq 19-20):
          V^4 = V_N^4 + C M a0   ->   gamma(g) = (1 + C a0/g)^(1/4)
  L2  EFE-saturated point-field (MG / AQUAL-class, framework nu):
          gamma(g) = (1 + C a0/(g + g_extN))^(1/4),  g_extN = framework
          Newtonian-inversion of the OBSERVED solar-neighborhood field
  L3  the framework's OWN per-star MI-EFE prescription (exact, banked
      wb_dr4_prereg_framework_curve.py boost_MI_perstar), with the banked
      observable-dilution/prescription-strength nuisance lambda in [0.5, 1.0]
      (that bracket IS the banked 1.05-1.10 band).

NOISE ANCHORING (no invented precision): per-bin sigma is anchored so that the
1-parameter profile fit on the FROZEN pipeline shape reproduces the FROZEN
forecast sigma(gamma_inf) = 0.0191 at N = 30,000 (prep_2026/gaia_dr4_prep/
wide_binary_pipeline.out, spread check).  Relative bin weights come from the
REAL Banik-exact eDR3 selection (N = 9,508; counts cached below with
provenance), rescaled to N = 30,000.  Frozen 8-bin edges reused verbatim.

HONESTY RAILS: a manufactured WIN and a manufactured DEFICIT are penalized
equally.  The degeneracy-breaking hypothesis (the gamma-vs-separation SHAPE
breaks a0 from C where a single gamma value cannot) is given its BEST case --
exact closed-form transition-scale route, perfect prescription knowledge,
maximal shape information -- before any verdict.  No "theory closed."  Exit 0
means the numbers were computed, NOT that a verdict was reached.
"""
import numpy as np
import json
import os
import math

# ----------------------------------------------------------------------------
# CONSTANTS AND BANKED INPUTS (every one traceable to a committed file)
# ----------------------------------------------------------------------------
G, MSUN, AU = 6.674e-11, 1.989e30, 1.496e11

A0_CAN = 9.36e-11        # canonical cH_Lambda/Z  (wb_dr4_prereg_framework_curve.py)
A0_ALT = 1.130e-10       # ALT footing rho_total/cH0 (PREREGISTRATION_DR4.md 1.1)
A0_MIL = 1.20e-10        # Milgrom conventional (degeneracy probe)
A0C_LINE = 9.355e-11     # a0-line canonical value used in reach_target.py
A0A_LINE = 1.1305e-10    # a0-line ALT value used in reach_target.py

GEXT_PRIMARY = 1.778e-10   # frozen primary g_ext,obs  (= 1.9 a0_can)
GEXT_ALTCONV = 2.078e-10   # frozen ALT convention Vc^2/R0, Vc=229, R0=8.178 kpc

# --- STEP-A dwarf a0-line floors (reach_target.py / per_galaxy_budget.py) ----
DWARF_FLOOR_GLS = 0.1100   # GLS-committed floor (Upsilon + gas-cal), reach_target S2
DWARF_FLOOR_SPARC = 0.1160  # best SPARC-alone stack, reach_target S4 rows 0-3
TARGET_SLN = abs(math.log(A0A_LINE / A0C_LINE)) / 3.0   # = 0.0631, the 3-sigma need

# --- FROZEN DR4 wide-binary pipeline numbers (wide_binary_pipeline.out) ------
EDGES = np.array([-1.5, -1.1, -0.8, -0.5, -0.2, 0.1, 0.5, 1.0, 2.2])
SIG_FIT_FROZEN = 0.0191    # rms over 8 independent catalogs @ gamma=1.09, N=30k
SIG_SYS_FROZEN = 0.0200    # frozen systematic allowance (PREREG 1.5)
SIG_TOT_FROZEN = math.sqrt(SIG_FIT_FROZEN**2 + SIG_SYS_FROZEN**2)   # 0.0277
N_DR4 = 30000
GAMMA_DR3_DRYRUN = 1.2050  # DR3 dry run, contamination-guard zone (PREREG 1.6)
GAMMA_MI_BAND = (1.0508, 1.1015)   # banked diluted edge / dynamical asymptote
GAMMA_MG = 1.1389                  # banked framework-as-MG asymptote

# --- REAL bin populations, Banik-exact eDR3 selection (provenance) -----------
# Reproduced from real_research/data/widebinaries/all_columns_catalog.fits.gz with
# the wb_mond_orbit_mc.py cut list (|b|>15, G<17 both, d<250 pc, RUWE<1.2 both,
# 2<s<30 kAU, ipd<=2, 0.464<Mtot<4.31, vt<=5, |d1-d2|<min(4sig,8)); N_sel=9508.
# Counts and bin-median PHYSICAL g_N (m/s^2) in the frozen 8 bins, both footings.
REAL_N_SEL = 9508
CNT_CAN = np.array([46, 273, 501, 708, 891, 1722, 3095, 2272], float)
GNMED_CAN = np.array([6.2647e-12, 1.15581e-11, 2.16734e-11, 4.25053e-11,
                      8.53111e-11, 1.91979e-10, 5.59452e-10, 1.38833e-09])
CNT_ALT = np.array([93, 326, 568, 743, 1020, 1804, 3229, 1724], float)
GNMED_ALT = np.array([7.4603e-12, 1.32363e-11, 2.56853e-11, 5.10394e-11,
                      1.03473e-10, 2.35076e-10, 6.57747e-10, 1.55302e-09])

bar = "=" * 96
sub = "-" * 96


# ----------------------------------------------------------------------------
# FRAMEWORK KERNEL (verbatim structure of the banked prereg curve script)
# ----------------------------------------------------------------------------
def nu(y):
    return np.sqrt(1.0 + 1.0 / y)


def y_newt_from_obs(y_obs):
    """Invert g_obs = sqrt(g_N^2 + g_N a0):  y_N = (-1 + sqrt(1+4 y_obs^2))/2."""
    return 0.5 * (-1.0 + np.sqrt(1.0 + 4.0 * y_obs**2))


def gextN_of(a0, gext_obs):
    """Framework Newtonian-inverted external field, PHYSICAL units (m/s^2)."""
    return a0 * y_newt_from_obs(gext_obs / a0)


NCOS = 4001
COS = np.linspace(-1.0, 1.0, NCOS)
SIN = np.sqrt(np.clip(1.0 - COS**2, 0.0, None))


def boost_MG(y_int, y_ext_N):
    yt = np.sqrt(y_int**2 + y_ext_N**2 + 2.0 * y_int * y_ext_N * COS)
    return float(np.mean(nu(yt)))


def boost_MI_perstar(y_rel, y_ext_N):
    """Framework per-star algebraic MI law, equal masses (banked verbatim)."""
    ys = 0.5 * y_rel
    y1z, y1x = y_ext_N + ys * COS, ys * SIN
    y2z, y2x = y_ext_N - ys * COS, -ys * SIN
    m1, m2 = np.hypot(y1z, y1x), np.hypot(y2z, y2x)
    az = nu(m1) * y1z - nu(m2) * y2z
    ax = nu(m1) * y1x - nu(m2) * y2x
    return float(np.mean(np.hypot(az, ax) / y_rel))


# ------------------------ the three gamma(g) laws ---------------------------
def gamma_L1(g, C, a0):
    """no-EFE bridge: V^4 = V_N^4 + C M a0."""
    return (1.0 + C * a0 / g)**0.25


def gamma_L2(g, C, a0, gext_obs):
    """EFE-saturated point-field (MG/AQUAL-class, framework nu)."""
    gE = gextN_of(a0, gext_obs)
    return (1.0 + C * a0 / (g + gE))**0.25


def gamma_L3(g, lam, a0, gext_obs):
    """framework's OWN per-star MI-EFE prescription, strength/dilution lambda."""
    gE = gextN_of(a0, gext_obs)
    yE = gE / a0
    g = np.atleast_1d(np.asarray(g, float))
    out = np.array([math.sqrt(boost_MI_perstar(gi / a0, yE)) for gi in g])
    return 1.0 + lam * (out - 1.0)


def gamma_MGexact(g, lam, a0, gext_obs):
    """MG/AQUAL angle-averaged point-field with the framework nu (exact)."""
    gE = gextN_of(a0, gext_obs)
    yE = gE / a0
    g = np.atleast_1d(np.asarray(g, float))
    out = np.array([math.sqrt(boost_MG(gi / a0, yE)) for gi in g])
    return 1.0 + lam * (out - 1.0)


def gamma_frozen_shape(g, ginf, a0, gext_obs):
    """The FROZEN pipeline transition shape (used only for noise anchoring)."""
    gE = gextN_of(a0, gext_obs)
    return 1.0 + (ginf - 1.0) * gE / (gE + g)


# ----------------------------------------------------------------------------
# NOISE MODEL, ANCHORED TO THE FROZEN sigma(gamma_inf) = 0.0191 @ N = 30,000
# ----------------------------------------------------------------------------
def per_bin_sigma(cnt, gN, a0, gext_obs, n_target=N_DR4, n_real=REAL_N_SEL,
                  sig_target=SIG_FIT_FROZEN, ginf_ref=1.09):
    """sigma_b = k/sqrt(N_b), N_b = real bin fractions rescaled to n_target, with
    k fixed by requiring the 1-parameter Fisher error on the frozen shape to equal
    the FROZEN forecast sig_target. No invented precision anywhere."""
    Nb = cnt * (n_target / n_real)
    shape = np.where(Nb > 0, 1.0 / np.sqrt(np.maximum(Nb, 1.0)), np.inf)
    dg = (gamma_frozen_shape(gN, ginf_ref + 1e-4, a0, gext_obs)
          - gamma_frozen_shape(gN, ginf_ref - 1e-4, a0, gext_obs)) / 2e-4
    F1 = float(np.sum((dg / shape)**2))          # with k = 1
    k = sig_target * math.sqrt(F1)               # so that 1/sqrt(F1/k^2) = target
    return k * shape, Nb, k


# ----------------------------------------------------------------------------
# FISHER MACHINERY (numerical central differences in log-parameters)
# ----------------------------------------------------------------------------
def jacobian(fun, theta_log, gN, h=1e-4):
    """d gamma_b / d ln theta_j, columns = parameters."""
    J = np.zeros((len(gN), len(theta_log)))
    for j in range(len(theta_log)):
        tp = list(theta_log); tm = list(theta_log)
        tp[j] += h; tm[j] -= h
        gp = np.atleast_1d(fun([math.exp(t) for t in tp], gN))
        gm = np.atleast_1d(fun([math.exp(t) for t in tm], gN))
        J[:, j] = (gp - gm) / (2 * h)
    return J


def fisher_report(J, sig, names, priors=None):
    """Fisher matrix, eigen-spectrum, marginalized sigmas (pseudo-inverse if
    singular), and the pairwise correlation matrix."""
    W = 1.0 / sig**2
    F = J.T @ (J * W[:, None])
    if priors is not None:
        for j, p in enumerate(priors):
            if p is not None and p > 0:
                F[j, j] += 1.0 / p**2
    ev, evec = np.linalg.eigh(F)
    cond = ev.max() / max(ev.min(), 1e-300)
    if ev.min() <= ev.max() * 1e-12:
        Cov = np.linalg.pinv(F, rcond=1e-10)
        singular = True
    else:
        Cov = np.linalg.inv(F)
        singular = False
    sd = np.sqrt(np.clip(np.diag(Cov), 0, None))
    corr = Cov / np.outer(np.maximum(sd, 1e-300), np.maximum(sd, 1e-300))
    return dict(F=F, ev=ev, evec=evec, cond=cond, Cov=Cov, sd=sd, corr=corr,
                singular=singular, names=names)


def weighted_cos(v1, v2, sig):
    """cosine between two derivative vectors in the inverse-noise metric."""
    W = 1.0 / sig**2
    n1 = math.sqrt(float(np.sum(W * v1 * v1)))
    n2 = math.sqrt(float(np.sum(W * v2 * v2)))
    return float(np.sum(W * v1 * v2)) / (n1 * n2)


def joint_sigma(*sigmas):
    return 1.0 / math.sqrt(sum(1.0 / s**2 for s in sigmas if np.isfinite(s) and s > 0))


RESULTS = {}

# ============================================================================
print(bar)
print("D0 -- REGRESSION ANCHORS (banked numbers reproduced, both footings)")
print(bar)
yE_can = gextN_of(A0_CAN, GEXT_PRIMARY) / A0_CAN
yE_alt = gextN_of(A0_ALT, GEXT_PRIMARY) / A0_ALT
asy_MI_can = math.sqrt(boost_MI_perstar(1e-6, yE_can))
asy_MG_can = math.sqrt(boost_MG(1e-6, yE_can))
print(f"  y_extN canonical = {yE_can:.4f}  (banked 1.4647)   "
      f"y_extN alt = {yE_alt:.4f}  (banked 1.1513)")
print(f"  MI-EFE asymptote = {asy_MI_can:.4f} (banked 1.1015)   "
      f"diluted edge = {1+0.5*(asy_MI_can-1):.4f} (banked 1.0508)")
print(f"  MG/AQUAL asymptote = {asy_MG_can:.4f} (banked 1.1389)")
assert abs(yE_can - 1.4647) < 2e-3 and abs(yE_alt - 1.1513) < 2e-3
assert 1.095 < asy_MI_can < 1.105 and abs(asy_MG_can - 1.137) < 5e-3
print(f"  STEP-A dwarf floors: GLS-committed {100*DWARF_FLOOR_GLS:.1f}% | "
      f"SPARC-alone stack {100*DWARF_FLOOR_SPARC:.1f}% ; 3-sigma need "
      f"{100*TARGET_SLN:.2f}%")
print(f"  FROZEN DR4 WB errors: sigma_fit {SIG_FIT_FROZEN:.4f} | sigma_sys "
      f"{SIG_SYS_FROZEN:.4f} | sigma_tot {SIG_TOT_FROZEN:.4f}  (N={N_DR4})")
sig_can, Nb_can, k_can = per_bin_sigma(CNT_CAN, GNMED_CAN, A0_CAN, GEXT_PRIMARY)
sig_alt, Nb_alt, k_alt = per_bin_sigma(CNT_ALT, GNMED_ALT, A0_ALT, GEXT_PRIMARY)
print(f"\n  noise anchoring (canonical): k = {k_can:.4f}; per-bin sigma(gamma):")
print("   bin  log10y range      N_b(DR4)   g_N [m/s^2]   sigma_b")
for b in range(8):
    print(f"   {b:>2}   [{EDGES[b]:+.1f},{EDGES[b+1]:+.1f})   {Nb_can[b]:9.0f}   "
          f"{GNMED_CAN[b]:.3e}   {sig_can[b]:.4f}")
print(f"  [check] 1-param Fisher on the frozen shape -> sigma(gamma_inf) = "
      f"{SIG_FIT_FROZEN:.4f} BY CONSTRUCTION (anchor, not a prediction)")
RESULTS["anchors"] = dict(yE_can=yE_can, yE_alt=yE_alt, asy_MI=asy_MI_can,
                          asy_MG=asy_MG_can, k_noise_can=k_can,
                          sigma_bins_can=sig_can.tolist(), Nb_can=Nb_can.tolist(),
                          target_sln=TARGET_SLN,
                          dwarf_floor_gls=DWARF_FLOOR_GLS)

# ============================================================================
print()
print(bar)
print("D1 -- LAW L1 (no-EFE, the task's law): THE a0-C DEGENERACY IS EXACT")
print(bar)
print("  gamma(g) = (1 + C a0/g)^(1/4).  a0 and C appear ONLY in the product C*a0,")
print("  so d gamma/d lnC == d gamma/d ln a0 POINTWISE, at every separation.")
for a0lab, a0v, gNv, sigv in (("canonical", A0_CAN, GNMED_CAN, sig_can),
                              ("ALT      ", A0_ALT, GNMED_ALT, sig_alt)):
    f1 = lambda th, g: gamma_L1(g, th[0], th[1])
    J = jacobian(f1, [math.log(1.0), math.log(a0v)], gNv)
    dmax = float(np.max(np.abs(J[:, 0] - J[:, 1])))
    cosang = weighted_cos(J[:, 0], J[:, 1], sigv)
    R = fisher_report(J, sigv, ["lnC", "ln a0"])
    print(f"  [{a0lab}] max_b |dgamma/dlnC - dgamma/dln a0| = {dmax:.2e} "
          f"(machine zero)   weighted cos = {cosang:.15f}")
    print(f"             Fisher eigenvalues = {R['ev'][0]:.3e}, {R['ev'][1]:.3e}  "
          f"-> cond = {R['cond']:.3e}  det = {np.linalg.det(R['F']):.3e}")
    print(f"             null eigenvector (lnC, ln a0) = "
          f"({R['evec'][0,0]:+.4f}, {R['evec'][1,0]:+.4f})  == the C*a0 = const ray")
    if a0lab.strip() == "canonical":
        RESULTS["L1"] = dict(max_deriv_diff=dmax, weighted_cos=cosang,
                             eig=R['ev'].tolist(), det=float(np.linalg.det(R['F'])),
                             null_vec=R['evec'][:, 0].tolist())
print("  The gamma(separation) SHAPE gives ZERO breaking here: the whole curve is a")
print("  RIGID one-parameter family in (C*a0).  sigma(ln a0) with C free = INFINITE.")
print("  => In the strictly no-EFE reading (Milgrom arXiv:2503.07106, EFE absent by")
print("     his eq 19-20 -- the reading with the LARGEST WB signal), a0's amplitude is")
print("     STRICTLY unmeasurable from wide binaries.  Only C*a0 is observable.")

# ============================================================================
print()
print(bar)
print("D2 -- LAW L2 (EFE-saturated point-field): DOES THE SECOND SCALE BREAK IT?")
print(bar)
print("  gamma(g) = (1 + C a0/(g + g_extN))^(1/4).  Now there are TWO scales, so the")
print("  curve has an AMPLITUDE (C*a0) and a TRANSITION LOCATION (g_extN).  Test 1:")
print("  treat (C, a0, g_extN) as free -- i.e. forget the framework's own inversion.")
for a0lab, a0v, gNv, sigv in (("canonical", A0_CAN, GNMED_CAN, sig_can),
                              ("ALT      ", A0_ALT, GNMED_ALT, sig_alt)):
    gE0 = gextN_of(a0v, GEXT_PRIMARY)
    f2free = lambda th, g: (1.0 + th[0] * th[1] / (g + th[2]))**0.25
    J = jacobian(f2free, [math.log(1.0), math.log(a0v), math.log(gE0)], gNv)
    R = fisher_report(J, sigv, ["lnC", "ln a0", "ln gE"])
    print(f"  [{a0lab}] eigenvalues {np.array2string(R['ev'], precision=3)}  "
          f"cond {R['cond']:.2e}  singular={R['singular']}")
    print(f"             null eigenvector (lnC, ln a0, ln gE) = "
          f"({R['evec'][0,0]:+.4f}, {R['evec'][1,0]:+.4f}, {R['evec'][2,0]:+.4f})")
    if a0lab.strip() == "canonical":
        RESULTS["L2_free"] = dict(eig=R['ev'].tolist(),
                                  null_vec=R['evec'][:, 0].tolist(),
                                  singular=bool(R['singular']))
print("  READING: still EXACTLY singular along (lnC, ln a0, ln gE) = (+1,-1,0)/sqrt2.")
print("  The second scale breaks the AMPLITUDE-vs-TRANSITION degeneracy -- it does NOT")
print("  break a0-vs-C.  The shape measures g_extN; the amplitude measures C*a0.")
print()
print("  Test 2: impose the framework's OWN inversion g_extN = g_extN(a0, g_ext,obs).")
print("  Now a0 enters BOTH the amplitude and the transition, so the exact null lifts.")
hdr = (f"  {'footing':<10}{'cos(a0,C)':>11}{'infl.':>8}"
       f"{'s(ln a0)|C,gx fix':>19}{'s(ln a0)|C free':>17}{'s(ln a0)|gx 2.4%':>18}")
print(hdr); print(sub)
L2rows = {}
for a0lab, a0v, gNv, sigv in (("canonical", A0_CAN, GNMED_CAN, sig_can),
                              ("ALT", A0_ALT, GNMED_ALT, sig_alt)):
    f2 = lambda th, g: gamma_L2(g, th[0], th[1], th[2])
    th0 = [math.log(1.0), math.log(a0v), math.log(GEXT_PRIMARY)]
    J = jacobian(f2, th0, gNv)
    cosCa0 = weighted_cos(J[:, 1], J[:, 0], sigv)
    infl = 1.0 / math.sqrt(max(1.0 - cosCa0**2, 1e-30))
    # (i) prescription and g_ext both perfectly known -> a0 alone
    F_a0 = float(np.sum((J[:, 1] / sigv)**2)); s_alone = 1.0 / math.sqrt(F_a0)
    # (ii) C free, g_ext fixed
    R2 = fisher_report(J[:, :2], sigv, ["lnC", "ln a0"])
    s_Cfree = R2['sd'][1]
    # (iii) C fixed, g_ext with a 2.4% astronomical prior (Vc 1.2%, R0 0.3%)
    R3 = fisher_report(J[:, [1, 2]], sigv, ["ln a0", "ln gx"], priors=[None, 0.024])
    s_gxprior = R3['sd'][0]
    print(f"  {a0lab:<10}{cosCa0:>11.6f}{infl:>8.1f}{s_alone:>19.3f}"
          f"{s_Cfree:>17.1f}{s_gxprior:>18.3f}")
    L2rows[a0lab] = dict(cos_a0_C=cosCa0, inflation=infl, sig_a0_alone=s_alone,
                         sig_a0_Cfree=s_Cfree, sig_a0_gxprior=s_gxprior)
RESULTS["L2_framework"] = L2rows
print("  (columns are FRACTIONAL sigma on a0, i.e. sigma(ln a0); 'gx' = g_ext,obs)")
print("  READING, stated in the framework's favour first: with the prescription C FIXED")
print("  and g_ext PERFECTLY known, the FULL CURVE does formally measure a0, and at")
print("  ~10-13% -- BETTER than the asymptote-only route (D4) because a0 also moves the")
print("  TRANSITION LOCATION, which is genuine extra shape information.  That is the")
print("  strongest honest form of the shape-breaks-it hypothesis and it is granted.")
print("  But it is COUNTERFACTUAL twice over: (a) the frozen sigma_sys = 0.02 is zeroed,")
print("  and that allowance explicitly covers 'residual shape/g_ext dependence' -- i.e.")
print("  exactly the leverage being used; (b) C fixed requires an MI completion that is")
print("  banked as UNWRITTEN.  Let C float and cos(a0,C) ~ 0.9987 inflates by x19.5.")

# ============================================================================
print()
print(bar)
print("D3 -- LAW L3: THE FRAMEWORK'S OWN PER-STAR MI-EFE PRESCRIPTION (exact)")
print(bar)
print("  gamma(g) = 1 + lambda*(sqrt(boost_MI_perstar(g/a0, y_extN)) - 1).")
print("  lambda is the banked prescription+observable-dilution nuisance: lambda=1 is")
print("  the dynamical asymptote 1.1015, lambda=0.5 the diluted edge 1.0508 -- that")
print("  bracket IS the banked 1.05-1.10 band, and it is NOT optional (the MI")
print("  completion is unwritten; the per-star law is a PRESCRIPTION, banked flag).")
hdr = (f"  {'law':<12}{'footing':<10}{'cos(a0,lam)':>13}{'infl.':>8}"
       f"{'s(lna0)|lam,gx':>16}{'s(lna0)|lam free':>18}{'s(lna0)|all free':>18}")
print(hdr); print(sub)
L3rows = {}
for lawlab, lawfun in (("MI per-star", gamma_L3), ("MG point-fld", gamma_MGexact)):
    for a0lab, a0v, gNv, sigv in (("canonical", A0_CAN, GNMED_CAN, sig_can),
                                  ("ALT", A0_ALT, GNMED_ALT, sig_alt)):
        f3 = lambda th, g: lawfun(g, th[0], th[1], th[2])
        th0 = [math.log(1.0), math.log(a0v), math.log(GEXT_PRIMARY)]
        J = jacobian(f3, th0, gNv, h=1e-3)
        cos_al = weighted_cos(J[:, 1], J[:, 0], sigv)
        infl = 1.0 / math.sqrt(max(1.0 - cos_al**2, 1e-30))
        s_alone = 1.0 / math.sqrt(float(np.sum((J[:, 1] / sigv)**2)))
        R2 = fisher_report(J[:, :2], sigv, ["ln lam", "ln a0"])
        R3 = fisher_report(J, sigv, ["ln lam", "ln a0", "ln gx"],
                           priors=[None, None, 0.024])
        print(f"  {lawlab:<12}{a0lab:<10}{cos_al:>13.6f}{infl:>8.1f}"
              f"{s_alone:>16.3f}{R2['sd'][1]:>18.2f}{R3['sd'][1]:>18.2f}")
        L3rows[f"{lawlab}|{a0lab}"] = dict(cos_a0_lam=cos_al, inflation=infl,
                                           sig_a0_alone=s_alone,
                                           sig_a0_lamfree=float(R2['sd'][1]),
                                           sig_a0_allfree=float(R3['sd'][1]))
RESULTS["L3"] = L3rows
print("  THE CRUX, stated plainly: the a0 derivative and the prescription-strength")
print("  derivative are nearly PARALLEL as functions of separation (cos ~ 0.99+).")
print("  The gamma(separation) SHAPE therefore does NOT supply an independent handle:")
print("  a0 and the prescription move the curve in almost the same direction, so the")
print("  marginalized a0 error blows up by the inflation factor above.")

# ---------------------------------------------------------------- D3b ladder
print()
print("  D3b -- THE SYSTEMATIC LADDER on the framework's OWN MI-EFE law (full curve,")
print("  canonical footing; the frozen sigma_sys is folded in the two defensible ways).")
print("  A coherent gamma-offset of sigma_sys is equivalent to a prior on ln lambda of")
print(f"  sigma_sys/(gamma_asy - 1) = {SIG_SYS_FROZEN:.3f}/{asy_MI_can-1:.4f} = "
      f"{SIG_SYS_FROZEN/(asy_MI_can-1):.3f}.")
LAM_PRIOR_SYS = SIG_SYS_FROZEN / (asy_MI_can - 1.0)
# banked prescription brackets expressed as ln-lambda priors (uniform width/sqrt12)
LAM_PRIOR_MIBAND = ((GAMMA_MI_BAND[1] - GAMMA_MI_BAND[0]) / (asy_MI_can - 1.0)
                    / math.sqrt(12.0))
LAM_PRIOR_FULL = ((GAMMA_MG - GAMMA_MI_BAND[0]) / (asy_MI_can - 1.0)
                  / math.sqrt(12.0))
f3c = lambda th, g: gamma_L3(g, th[0], th[1], th[2])
th0c = [math.log(1.0), math.log(A0_CAN), math.log(GEXT_PRIMARY)]
Jc = jacobian(f3c, th0c, GNMED_CAN, h=1e-3)


def a0_sigma(sig_b, lam_prior, gx_prior, J=Jc):
    R = fisher_report(J, sig_b, ["ln lam", "ln a0", "ln gx"],
                      priors=[lam_prior, None, gx_prior])
    return float(R['sd'][1])


sig_floor = np.hypot(sig_can, SIG_SYS_FROZEN)   # sigma_sys as a per-bin error floor
LADDER = [
    ("L0 stat only, lambda + g_ext EXACT (counterfactual best case)",
     a0_sigma(sig_can, 1e-6, 1e-6)),
    ("L1 stat only, g_ext 2.4% prior, lambda EXACT",
     a0_sigma(sig_can, 1e-6, 0.024)),
    ("L2 sigma_sys as a per-bin error floor, lambda + g_ext EXACT",
     a0_sigma(sig_floor, 1e-6, 1e-6)),
    ("L3 sigma_sys as a coherent lambda prior, g_ext 2.4%",
     a0_sigma(sig_can, LAM_PRIOR_SYS, 0.024)),
    ("L4 + g_ext frozen-convention spread 15.6% instead of 2.4%",
     a0_sigma(sig_can, LAM_PRIOR_SYS, abs(math.log(GEXT_ALTCONV / GEXT_PRIMARY)))),
    ("L5 banked MI band 1.0508-1.1015 as the lambda prior, g_ext 2.4%",
     a0_sigma(sig_can, LAM_PRIOR_MIBAND, 0.024)),
    ("L6 full MI-to-MG bracket 1.0508-1.1389 as the prior, g_ext 2.4%",
     a0_sigma(sig_can, LAM_PRIOR_FULL, 0.024)),
    ("L7 lambda entirely free (no prescription knowledge at all)",
     a0_sigma(sig_can, None, 0.024)),
]
print(f"  {'rung':<62}{'s(ln a0)':>10}{'vs dwarf 11.0%':>16}")
print(sub)
for lab, s in LADDER:
    print(f"  {lab:<62}{100*s:>9.1f}%{s/DWARF_FLOOR_GLS:>15.1f}x")
RESULTS["L3_ladder"] = {lab: s for lab, s in LADDER}
RESULTS["lam_priors"] = dict(sys=LAM_PRIOR_SYS, mi_band=LAM_PRIOR_MIBAND,
                             full=LAM_PRIOR_FULL)
print(sub)
print("  Only rung L0 -- prescription EXACT, g_ext EXACT, systematics ZEROED -- gets WB")
print("  inside a factor 1 of the dwarf floor.  Every rung that admits a real, banked")
print("  uncertainty lands 1.5-13x worse.  L2 vs L0 shows the a0 leverage is carried by")
print("  the deep bins the frozen sigma_sys allowance is precisely about.")

# --------------------------------------------------- robustness of bin weights
print()
print("  D3c -- ROBUSTNESS: the conclusion must not be an artifact of the bin-weight")
print("  model (real eDR3 fractions rescaled to N=30k).  Re-tilt the counts by g_N^p,")
print("  renormalize to N=30k, re-anchor k to the SAME frozen sigma_fit, recompute:")
print(f"  {'tilt p':>8}{'deep frac':>11}{'s(lna0) L0':>13}{'s(lna0) L3':>13}"
      f"{'cos(a0,lam)':>13}")
ROB = {}
for p in (-0.4, -0.2, 0.0, 0.2, 0.4):
    cnt_t = CNT_CAN * (GNMED_CAN / GNMED_CAN[4])**p
    cnt_t = cnt_t / cnt_t.sum() * CNT_CAN.sum()
    sg, Nbt, kt = per_bin_sigma(cnt_t, GNMED_CAN, A0_CAN, GEXT_PRIMARY)
    deepf = float(cnt_t[:4].sum() / cnt_t.sum())
    s0 = a0_sigma(sg, 1e-6, 1e-6)
    s3 = a0_sigma(sg, LAM_PRIOR_SYS, 0.024)
    cs = weighted_cos(Jc[:, 1], Jc[:, 0], sg)
    print(f"  {p:>8.1f}{deepf:>11.3f}{100*s0:>12.1f}%{100*s3:>12.1f}%{cs:>13.6f}")
    ROB[str(p)] = dict(deep_frac=deepf, sig_a0_L0=s0, sig_a0_L3=s3, cos=cs)
RESULTS["robustness_binweights"] = ROB
print("  The near-parallelism (cos) and the ladder ordering are STABLE across a factor")
print("  ~3 swing in the deep-bin fraction: the degeneracy is geometric, not a")
print("  weighting artifact.")

# ------------------------------------------- D3d: the strongest steelman for shape
print()
print("  D3d -- STEELMAN: if the MI and MG SHAPES differ (not just their amplitudes),")
print("  the curve could identify the prescription and thereby FREE a0.  Test it: fit")
print("  each law to the OTHER law's curve over a (lambda, a0) grid and report (i) the")
print("  a0 bias from mis-identifying the prescription, (ii) the residual chi2 -- i.e.")
print("  whether DR4 could tell the two shapes apart at all once amplitude is refit.")
A0GRID = A0_CAN * np.exp(np.linspace(math.log(0.10), math.log(10.0), 181))
LAMGRID = np.exp(np.linspace(math.log(0.05), math.log(20.0), 181))


def profile_a0(truth, law, sig=sig_can):
    """chi2 profiled over lambda at each a0 -- the honest 1-D likelihood in a0."""
    prof = np.empty(len(A0GRID))
    lamb = np.empty(len(A0GRID))
    for i, a0v in enumerate(A0GRID):
        c2 = np.empty(len(LAMGRID))
        for j, lam in enumerate(LAMGRID):
            m = law(GNMED_CAN, lam, a0v, GEXT_PRIMARY)
            c2[j] = float(np.sum(((truth - m) / sig)**2))
        k = int(np.argmin(c2)); prof[i] = c2[k]; lamb[i] = LAMGRID[k]
    return prof, lamb


STEEL = {}
for tlab, tlaw, flab, flaw in (("MG point-field", gamma_MGexact, "MI per-star", gamma_L3),
                               ("MI per-star", gamma_L3, "MG point-field", gamma_MGexact),
                               ("MI per-star", gamma_L3, "MI per-star", gamma_L3)):
    truth = tlaw(GNMED_CAN, 1.0, A0_CAN, GEXT_PRIMARY)
    prof, lamb = profile_a0(truth, flaw)
    i0 = int(np.argmin(prof)); d = prof - prof[i0]
    r1 = A0GRID[d <= 1.0] / A0_CAN
    r9 = A0GRID[d <= 9.0] / A0_CAN
    edge1 = (r1.min() <= A0GRID[0]/A0_CAN * 1.001) or (r1.max() >= A0GRID[-1]/A0_CAN*0.999)
    print(f"      truth={tlab:<15} model={flab:<15} chi2_min={prof[i0]:6.3f} "
          f"a0_hat/a0_true={A0GRID[i0]/A0_CAN:5.2f}  lam={lamb[i0]:5.2f}")
    print(f"          profiled a0 range: dchi2<=1 -> [{r1.min():.2f}, {r1.max():.2f}] x a0_true"
          f" ; dchi2<=9 -> [{r9.min():.2f}, {r9.max():.2f}]"
          f"{'   <-- HITS GRID EDGE (unbounded)' if edge1 else ''}")
    STEEL[f"{tlab}->{flab}"] = dict(chi2_min=prof[i0], a0_ratio=A0GRID[i0]/A0_CAN,
                                    lam=lamb[i0], r1=[r1.min(), r1.max()],
                                    r9=[r9.min(), r9.max()], grid_edge=bool(edge1))
RESULTS["steelman_shape"] = STEEL
print("      READING (both directions): even the SELF-FIT row (truth=MI, model=MI, i.e.")
print("      perfect model knowledge apart from lambda) has a chi2 valley that runs to")
print("      the edge of a factor-10 a0 grid -- the profile likelihood in a0 is FLAT once")
print("      lambda is free.  And cross-fitting MG data with the MI law leaves chi2_min")
print("      far below the ~8 expected from an 8-bin draw: the two prescriptions are")
print("      SHAPE-INDISTINGUISHABLE at DR4 precision once the amplitude is refit.")
print("      This CLOSES the steelman two ways: (a) the shape carries no usable")
print("      prescription information, so it cannot free a0 by identifying the")
print("      prescription; (b) the lambda-rescaling parametrization used above is")
print("      ADEQUATE -- it is not understating a real shape difference.")

# ============================================================================
print()
print(bar)
print("D4 -- AMPLITUDE-ONLY MAPPING: d gamma/d ln a0, AND THE PRESCRIPTION BRACKET")
print(bar)


def dgamma_dlna0(a0, gext_obs, law="MI", h=1e-3):
    """Deep asymptote derivative d gamma_inf / d ln a0 at fixed g_ext,obs."""
    def asy(a0v):
        yE = gextN_of(a0v, gext_obs) / a0v
        return math.sqrt(boost_MI_perstar(1e-6, yE) if law == "MI"
                         else boost_MG(1e-6, yE))
    return (asy(a0 * math.exp(h)) - asy(a0 * math.exp(-h))) / (2 * h)


print("  (a) sensitivity of the deep asymptote to a0 at fixed physical g_ext,obs:")
D4 = {}
for law in ("MI", "MG"):
    for lab, a0v in (("canonical", A0_CAN), ("ALT", A0_ALT)):
        d = dgamma_dlna0(a0v, GEXT_PRIMARY, law)
        print(f"      {law} {lab:<10} d gamma_inf/d ln a0 = {d:+.4f}   "
              f"=> 1% in a0 moves gamma by {abs(d)/100:.5f}")
        D4[f"dgdlna0_{law}_{lab}"] = d
d_MI = D4["dgdlna0_MI_canonical"]
print(f"  cross-check vs banked degeneracy statement: Milgrom a0=1.2e-10 gives MI")
mil_asy = math.sqrt(boost_MI_perstar(1e-6, gextN_of(A0_MIL, GEXT_PRIMARY) / A0_MIL))
print(f"      asymptote {mil_asy:.4f} vs canonical {asy_MI_can:.4f}: "
      f"d(gamma)={mil_asy-asy_MI_can:+.4f} for d(ln a0)={math.log(A0_MIL/A0_CAN):+.4f}")
print(f"      -> secant slope {(mil_asy-asy_MI_can)/math.log(A0_MIL/A0_CAN):+.4f}, "
      f"local {d_MI:+.4f}  (banked: '22% a0 shift -> 3.3% gamma shift')")
print()
print("  (b) INVERT: what a0 precision does a given gamma precision buy, with the")
print("      prescription and g_ext PERFECTLY known (the most generous possible case)?")
for lab, sg in (("sigma_fit (stat only)", SIG_FIT_FROZEN),
                ("sigma_sys (frozen allowance)", SIG_SYS_FROZEN),
                ("sigma_tot (frozen total)", SIG_TOT_FROZEN)):
    print(f"      {lab:<32} {sg:.4f}  ->  sigma(ln a0) = "
          f"{sg/abs(d_MI)*100:6.1f}%")
sig_a0_best = SIG_TOT_FROZEN / abs(d_MI)
sig_a0_sysfloor = SIG_SYS_FROZEN / abs(d_MI)
print(f"      WB a0 SYSTEMATIC FLOOR (N -> infinity, sigma_fit -> 0): "
      f"{100*sig_a0_sysfloor:.1f}%")
print(f"      -- compare the dwarf a0-line floor {100*DWARF_FLOOR_GLS:.1f}% and the "
      f"3-sigma need {100*TARGET_SLN:.2f}%")
print()
print("  (c) the PRESCRIPTION BRACKET as an a0 error (the killer):")
C_of_gamma = lambda gam, a0, gx: (gam**4 - 1.0) * gextN_of(a0, gx) / a0
for lab, gam in (("MI diluted edge", GAMMA_MI_BAND[0]),
                 ("MI dynamical", GAMMA_MI_BAND[1]),
                 ("framework-as-MG", GAMMA_MG),
                 ("DR3 dry run (guard zone)", GAMMA_DR3_DRYRUN)):
    print(f"      {lab:<26} gamma={gam:.4f}  ->  implied C_eff = "
          f"{C_of_gamma(gam, A0_CAN, GEXT_PRIMARY):.4f}")
Clo = C_of_gamma(GAMMA_MI_BAND[0], A0_CAN, GEXT_PRIMARY)
Chi = C_of_gamma(GAMMA_MG, A0_CAN, GEXT_PRIMARY)
print(f"      prescription span C_eff in [{Clo:.3f}, {Chi:.3f}] = factor "
      f"{Chi/Clo:.2f}.  Because gamma sees only C*a0 in the asymptote, at FIXED")
print(f"      measured gamma this is a factor-{Chi/Clo:.2f} ({100*math.log(Chi/Clo):.0f}% in ln)"
      f" uncertainty on a0 -- from THEORY, not data.")
dgam_band = GAMMA_MG - GAMMA_MI_BAND[0]
print(f"      equivalently: the band width d(gamma)={dgam_band:.4f} maps through "
      f"d gamma/d ln a0 = {d_MI:.4f} to")
print(f"      sigma(ln a0) = {100*dgam_band/abs(d_MI):.0f}%  (MI-band-only, "
      f"1.0508->1.1015: {100*(GAMMA_MI_BAND[1]-GAMMA_MI_BAND[0])/abs(d_MI):.0f}%; "
      f"MI-vs-MG only: {100*(GAMMA_MG-GAMMA_MI_BAND[1])/abs(d_MI):.0f}%)")
print()
print("  (d) the CONTAMINATION axis in a0 units (why DR3 is evidence for nothing):")
dcon = GAMMA_DR3_DRYRUN - GAMMA_MI_BAND[1]
print(f"      DR3 dry run gamma = {GAMMA_DR3_DRYRUN:.4f} sits {dcon:+.4f} above the MI")
print(f"      dynamical asymptote -> if read as an a0 measurement that is "
      f"{100*dcon/abs(d_MI):+.0f}% in a0")
print(f"      (a factor {math.exp(dcon/abs(d_MI)):.2f}).  Contamination biases gamma UP only,")
print("      so it biases any WB-derived a0 UP only -- a ONE-SIDED, not averaging, error.")
RESULTS["D4"] = dict(D4, sig_a0_best=sig_a0_best, sig_a0_sysfloor=sig_a0_sysfloor,
                     C_eff_lo=Clo, C_eff_hi=Chi, C_span=Chi/Clo,
                     sig_a0_prescription_band=dgam_band/abs(d_MI),
                     sig_a0_MIband=(GAMMA_MI_BAND[1]-GAMMA_MI_BAND[0])/abs(d_MI),
                     sig_a0_MIvsMG=(GAMMA_MG-GAMMA_MI_BAND[1])/abs(d_MI),
                     dr3_a0_offset=dcon/abs(d_MI))

# ============================================================================
print()
print(bar)
print("D5 -- THE g_ext SYSTEMATIC AND THE CLOSED-FORM SHAPE ROUTE (best case for")
print("      the degeneracy-breaking hypothesis)")
print(bar)
print("  The ONLY C-free route to a0: the shape's transition location measures g_extN")
print("  in PHYSICAL units; the framework's own inversion then gives a0 with NO")
print("  reference to C:      a0 = (g_ext,obs^2 - g_extN^2)/g_extN.")
print("  Closed-form log-derivatives (u = g_extN/a0, exact):")
print("      d ln a0 / d ln g_extN   = -(2u + 1)")
print("      d ln a0 / d ln g_ext,obs = +2(u + 1)")
D5 = {}
for lab, a0v, gNv, sigv in (("canonical", A0_CAN, GNMED_CAN, sig_can),
                            ("ALT", A0_ALT, GNMED_ALT, sig_alt)):
    u = gextN_of(a0v, GEXT_PRIMARY) / a0v
    lev_gE, lev_gx = -(2*u + 1), 2*(u + 1)
    # numeric verification of the closed forms
    h = 1e-5
    gE0 = gextN_of(a0v, GEXT_PRIMARY)
    a0_of_gE = lambda gE, gx: (gx**2 - gE**2) / gE
    num_gE = (math.log(a0_of_gE(gE0*math.exp(h), GEXT_PRIMARY))
              - math.log(a0_of_gE(gE0*math.exp(-h), GEXT_PRIMARY))) / (2*h)
    num_gx = (math.log(a0_of_gE(gE0, GEXT_PRIMARY*math.exp(h)))
              - math.log(a0_of_gE(gE0, GEXT_PRIMARY*math.exp(-h)))) / (2*h)
    assert abs(num_gE - lev_gE) < 1e-4 and abs(num_gx - lev_gx) < 1e-4
    # maximal shape information: 2-param Fisher over (ln A, ln gE), A = C*a0
    fA = lambda th, g: (1.0 + th[0] / (g + th[1]))**0.25
    JA = jacobian(fA, [math.log(1.0*a0v), math.log(gE0)], gNv)
    RA = fisher_report(JA, sigv, ["ln A", "ln gE"])
    s_lngE = float(RA['sd'][1])
    s_a0_shape = abs(lev_gE) * s_lngE
    s_a0_shape_tot = math.hypot(s_a0_shape, abs(lev_gx) * 0.024)
    print(f"  [{lab}] u = {u:.4f}: lever on g_extN = {lev_gE:+.3f}, on g_ext,obs "
          f"= {lev_gx:+.3f}  (both VERIFIED numerically)")
    print(f"           maximal shape measurement of the transition: sigma(ln g_extN) "
          f"= {100*s_lngE:.1f}%  (marginalizing the amplitude C*a0)")
    print(f"           -> sigma(ln a0) from the shape alone = {100*s_a0_shape:.0f}% ; "
          f"with a 2.4% g_ext,obs prior = {100*s_a0_shape_tot:.0f}%")
    D5[lab] = dict(u=u, lever_gE=lev_gE, lever_gx=lev_gx, sig_ln_gE=s_lngE,
                   sig_a0_shape=s_a0_shape, sig_a0_shape_tot=s_a0_shape_tot)
gx_conv = math.log(GEXT_ALTCONV / GEXT_PRIMARY)
u_can = gextN_of(A0_CAN, GEXT_PRIMARY) / A0_CAN
print(f"  FROZEN g_ext CONVENTION SPREAD: 1.778e-10 vs 2.078e-10 = "
      f"{100*gx_conv:.1f}% in ln g_ext,obs")
print(f"      through the +{2*(u_can+1):.2f} lever that is "
      f"{100*2*(u_can+1)*gx_conv:.0f}% on a0 by the shape route,")
gam_p = math.sqrt(boost_MI_perstar(1e-6, gextN_of(A0_CAN, GEXT_PRIMARY)/A0_CAN))
gam_a = math.sqrt(boost_MI_perstar(1e-6, gextN_of(A0_CAN, GEXT_ALTCONV)/A0_CAN))
print(f"      and {100*abs(gam_a-gam_p)/abs(d_MI):.0f}% on a0 by the amplitude route "
      f"(the two frozen g_ext values move the MI asymptote {gam_p:.4f} -> {gam_a:.4f}).")
print("  READING: the shape route is C-FREE (a genuine degeneracy break) but the")
print("  transition-location lever AMPLIFIES errors ~3.3-3.9x, and the frozen g_ext")
print("  convention spread alone is a ~60-80% a0 systematic through it.  It is the")
print("  weakest of the three routes, not the rescue.")
print()
print("  Additional non-averaging WB systematic (task item 1, honestly quantified):")
print("  photometric masses. vtilde ~ M^(-1/2) and the g_N axis ~ M, so a COHERENT")
print("  mass-scale offset d lnM shifts gamma by -d lnM/2 plus a transition shift.")
for dlnM in (0.02, 0.03, 0.05):
    print(f"      global M-L offset {100*dlnM:.0f}% -> d gamma = {-0.5*dlnM:+.4f} -> "
          f"sigma(ln a0) = {100*abs(0.5*dlnM/d_MI):.0f}%  (amplitude route)")
print(f"  So WB masses are NOT systematic-free: a 3% coherent main-sequence M-L offset")
print(f"  already costs ~{100*abs(0.5*0.03/d_MI):.0f}% in a0 -- MORE than the ENTIRE dwarf {100*DWARF_FLOOR_GLS:.1f}% floor.")
# the mass-lever comparison, computed not asserted (per_galaxy_budget_results.json)
DWARF_SYSU_FRAC = 0.0810        # sysU / a0hat, gas-dominated budget
DWARF_SIG_LNU = math.log(10) * 0.10   # 0.10 dex -> 0.2303 in ln
lev_dwarf = DWARF_SYSU_FRAC / DWARF_SIG_LNU
lev_wb = abs(0.5 / d_MI)
print(f"  Mass-lever comparison, computed: dwarf a0-line d ln a0/d ln Upsilon = "
      f"{DWARF_SYSU_FRAC:.4f}/{DWARF_SIG_LNU:.4f} = {lev_dwarf:.2f};")
print(f"  WB d ln a0/d ln M = 0.5/{abs(d_MI):.4f} = {lev_wb:.2f}  ->  the WB mass lever is")
print(f"  {lev_wb/lev_dwarf:.1f}x STEEPER.  Main-sequence M-L models ARE tighter than galaxy")
print(f"  Upsilon (~2-5% vs 0.10 dex = {100*DWARF_SIG_LNU:.0f}%), but the steeper lever cancels most of")
print("  that advantage.  The prior claim that WB carries 'no Upsilon at all' is")
print("  CORRECTED here, not upheld: the axis is different, the magnitude is not.")
RESULTS["mass_lever"] = dict(dwarf=lev_dwarf, wb=lev_wb, ratio=lev_wb/lev_dwarf)
RESULTS["D5"] = dict(D5, gext_convention_lnspread=gx_conv,
                     a0_sys_from_gext_shape=2*(u_can+1)*gx_conv,
                     a0_sys_from_gext_amp=abs(gam_a-gam_p)/abs(d_MI),
                     a0_sys_from_ML_3pct=abs(0.5*0.03/d_MI))

# ============================================================================
print()
print(bar)
print("D6 -- THE JOINT WITH THE DWARF a0-LINE: WHAT WOULD WB HAVE TO DELIVER?")
print(bar)
need = 1.0 / math.sqrt(1.0/TARGET_SLN**2 - 1.0/DWARF_FLOOR_GLS**2)
need_sparc = 1.0 / math.sqrt(1.0/TARGET_SLN**2 - 1.0/DWARF_FLOOR_SPARC**2)
print(f"  3-sigma separation of canonical from the 1.13-1.20e-10 cluster needs a")
print(f"  joint sigma(ln a0) <= {100*TARGET_SLN:.2f}%.")
print(f"  Given the dwarf floor {100*DWARF_FLOOR_GLS:.1f}% (GLS-committed), WB must "
      f"deliver sigma(ln a0) <= {100*need:.2f}%")
print(f"  Given the dwarf floor {100*DWARF_FLOOR_SPARC:.1f}% (SPARC-alone stack), WB "
      f"must deliver <= {100*need_sparc:.2f}%")
print(f"  i.e. WB would have to be a TIGHTER a0 measurement than the dwarf line is,")
print(f"  not merely a comparable one.  Via the ASYMPTOTE-ONLY route that requires")
print(f"  sigma(gamma) <= {abs(d_MI)*need:.4f} -- vs the frozen sigma_sys allowance alone = "
      f"{SIG_SYS_FROZEN:.4f} ({SIG_SYS_FROZEN/(abs(d_MI)*need):.1f}x too")
print(f"  large) and sigma_tot = {SIG_TOT_FROZEN:.4f} "
      f"({SIG_TOT_FROZEN/(abs(d_MI)*need):.1f}x too large).  The FULL-CURVE route below does")
print("  better than that and is the one the ladder uses.")
print()
print("  Joint ladder (quadrature; WB and dwarf systematics ARE orthogonal, so this")
print("  IS the fair combination -- the orthogonality hypothesis is fully granted).")
print("  WB sigmas are the FULL-CURVE Fisher numbers from the D3b ladder, i.e. the")
print("  best (not the worst) route available at each level of knowledge.")
LAD = dict(LADDER)
sig_ML3 = abs(0.5 * 0.03 / d_MI)
print(f"  {'WB scenario':<60}{'s_WB':>9}{'joint':>9}{'3sig?':>7}")
print(sub)
scen = [
    ("A. lambda+g_ext EXACT, sigma_sys ZEROED (counterfactual best)",
     LAD["L0 stat only, lambda + g_ext EXACT (counterfactual best case)"]),
    ("B. A + 3% coherent photometric M-L offset",
     math.hypot(LAD["L0 stat only, lambda + g_ext EXACT (counterfactual best case)"],
                sig_ML3)),
    ("C. lambda EXACT, g_ext 2.4% prior, sigma_sys ZEROED",
     LAD["L1 stat only, g_ext 2.4% prior, lambda EXACT"]),
    ("D. sigma_sys as a per-bin floor, lambda+g_ext EXACT",
     LAD["L2 sigma_sys as a per-bin error floor, lambda + g_ext EXACT"]),
    ("E. frozen sigma_sys as a lambda prior + g_ext 2.4% (realistic)",
     LAD["L3 sigma_sys as a coherent lambda prior, g_ext 2.4%"]),
    ("F. E + 3% coherent photometric M-L offset",
     math.hypot(LAD["L3 sigma_sys as a coherent lambda prior, g_ext 2.4%"], sig_ML3)),
    ("G. banked MI band 1.0508-1.1015 as the prescription prior",
     LAD["L5 banked MI band 1.0508-1.1015 as the lambda prior, g_ext 2.4%"]),
    ("H. full MI-to-MG bracket 1.0508-1.1389 as the prior",
     LAD["L6 full MI-to-MG bracket 1.0508-1.1389 as the prior, g_ext 2.4%"]),
    ("I. no prescription knowledge (lambda free)",
     LAD["L7 lambda entirely free (no prescription knowledge at all)"]),
    ("J. C-free transition-location route only (D5)",
     D5["canonical"]["sig_a0_shape_tot"]),
]
JOINT = {}
for lab, sw in scen:
    j = joint_sigma(DWARF_FLOOR_GLS, sw)
    ok = "GO" if j <= TARGET_SLN else "no"
    print(f"  {lab:<60}{100*sw:>8.1f}%{100*j:>8.2f}%{ok:>7}")
    JOINT[lab] = dict(sig_wb=sw, joint=j, three_sigma=bool(j <= TARGET_SLN))
print(sub)
print(f"  dwarf-alone reference: {100*DWARF_FLOOR_GLS:.2f}%   target "
      f"{100*TARGET_SLN:.2f}%   WB must beat {100*need:.2f}% for the joint to reach it")
print("  Rows G/H use uniform-bracket sigmas (width/sqrt12) so the banked theory")
print("  bracket is NOT inflated beyond a fair reading.")
best_joint = min(JOINT[l]["joint"] for l in JOINT)
sig_L0 = LAD["L0 stat only, lambda + g_ext EXACT (counterfactual best case)"]
n_need = N_DR4 * (sig_L0 / need)**2
print(f"  BEST joint on the whole ladder = {100*best_joint:.2f}% "
      f"({'reaches' if best_joint <= TARGET_SLN else 'still short of'} "
      f"{100*TARGET_SLN:.2f}%); shortfall factor "
      f"{best_joint/TARGET_SLN:.2f}x.")
print(f"  Statistical-only N requirement, in the COUNTERFACTUAL best case (row A: no")
print(f"  systematics at all, prescription and g_ext exact): sigma scales as 1/sqrt(N),")
print(f"  so reaching the {100*need:.2f}% WB budget needs N ~ {n_need:,.0f} pairs "
      f"vs the {N_DR4:,} the frozen")
print("  pre-registration forecasts -- and that row is the one that zeroes the very")
print("  systematics the frozen sigma_sys allowance exists to cover.")
_D6EXTRA = dict(n_pairs_needed_bestcase=n_need, best_joint=best_joint,
                sig_wb_L0=sig_L0)
RESULTS["D6"] = dict(_D6EXTRA, need_vs_gls=need, need_vs_sparc=need_sparc,
                     need_sigma_gamma=abs(d_MI)*need,
                     joint=JOINT, dwarf_floor=DWARF_FLOOR_GLS,
                     target=TARGET_SLN)

# ============================================================================
print()
print(bar)
print("D7 -- WHAT WB *CAN* DO (the honest positive, reported symmetrically)")
print(bar)
print("  Run the inference BACKWARDS: fix a0 from the dwarf a0-line and ask what the")
print("  same DR4 gamma measurement then determines.")
for lab, a0v, gNv, sigv in (("canonical", A0_CAN, GNMED_CAN, sig_can),
                            ("ALT", A0_ALT, GNMED_ALT, sig_alt)):
    f3 = lambda th, g: gamma_L3(g, th[0], th[1], th[2])
    th0 = [math.log(1.0), math.log(a0v), math.log(GEXT_PRIMARY)]
    J = jacobian(f3, th0, gNv, h=1e-3)
    s_lam = 1.0 / math.sqrt(float(np.sum((J[:, 0] / sigv)**2)))
    # with the frozen sigma_sys folded in on the asymptote
    d_lam = asy_MI_can - 1.0
    s_lam_tot = math.hypot(s_lam, SIG_SYS_FROZEN / d_lam)
    print(f"  [{lab}] sigma(ln lambda) = {100*s_lam:.1f}% stat, "
          f"{100*s_lam_tot:.1f}% with the frozen sigma_sys")
    RESULTS.setdefault("D7", {})[lab] = dict(sig_ln_lambda=s_lam,
                                             sig_ln_lambda_tot=s_lam_tot)
print("  So DR4 WB, with a0 supplied externally, constrains the nu+EFE PRESCRIPTION")
print("  (the MI-vs-MG / dilution axis) to ~15-25% -- which is exactly what the")
print("  frozen pre-registration already claims: 'DR4 gamma_v constrains the nu+EFE")
print("  prescription, NOT the value a0 = 9.36e-11.'  That is a real deliverable; it")
print("  is just NOT an a0 amplitude, so it cannot enter the a0 joint.")
print("  It also inherits the frozen MI-vs-MG verdict: separating 1.09 from 1.137 at")
print("  3 sigma needs N ~ 45,000 AND sigma_sys < 0.01 -- pre-declared likely")
print("  UNDECIDABLE in DR4.")

# ============================================================================
print()
print(bar)
print("VERDICT (degeneracy test; a manufactured win and a manufactured deficit are")
print("         penalized equally)")
print(bar)
print("  1. NO-EFE READING (L1, Milgrom arXiv:2503.07106 -- the largest-signal WB")
print("     reading): the a0-C degeneracy is EXACT.  d gamma/d lnC and d gamma/d ln a0")
print(f"     are identical to machine precision ({RESULTS['L1']['max_deriv_diff']:.1e}), the "
      f"2x2 Fisher determinant is")
print(f"     {RESULTS['L1']['det']:.2e}, and the null direction is the C*a0 = const ray.  The")
print("     gamma(separation) SHAPE is a RIGID one-parameter family in C*a0 and adds")
print("     ZERO breaking.  a0's amplitude is STRICTLY unmeasurable here.")
print("  2. EFE READINGS (L2/L3): the second scale g_extN lifts the EXACT degeneracy,")
print("     but only weakly -- the a0 and prescription derivative vectors are nearly")
print(f"     parallel (weighted cos = "
      f"{RESULTS['L3']['MI per-star|canonical']['cos_a0_lam']:.4f} for the framework's own MI-EFE law),")
print(f"     inflating sigma(ln a0) by x{RESULTS['L3']['MI per-star|canonical']['inflation']:.1f}.  "
      f"SO: THE SHAPE DOES NOT BREAK THE")
print("     a0-C DEGENERACY.  It breaks the AMPLITUDE-vs-TRANSITION degeneracy, which")
print("     is a different (and insufficient) thing.")
_sf = RESULTS['steelman_shape']['MI per-star->MI per-star']
_cf = RESULTS['steelman_shape']['MG point-field->MI per-star']
print("     CONFIRMED NON-LINEARLY (D3d, not just by Fisher): with the prescription")
print("     strength free, the PROFILE chi2 in a0 is FLAT -- dchi2<=1 spans")
print(f"     [{_sf['r1'][0]:.2f}, {_sf['r1'][1]:.2f}] x a0_true even when the model is the TRUE law, and it")
print("     runs off a factor-10 grid.  And MG data fitted with the MI law gives")
print(f"     chi2_min = {_cf['chi2_min']:.2f} on 8 bins at a0_hat = {_cf['a0_ratio']:.1f} x a0_true: the two")
print("     prescriptions are SHAPE-INDISTINGUISHABLE at DR4 precision, so mis-picking")
print("     one biases a0 by up to an ORDER OF MAGNITUDE with no chi2 penalty.")
print("  3. WHAT DOES BREAK, AND BY HOW MUCH (stated in the framework's favour first):")
print("     the framework's OWN inversion g_extN(a0, g_ext,obs) does supply a second,")
print("     a0-dependent scale, so with the prescription EXACT and g_ext EXACT the full")
print(f"     curve formally measures a0 at {100*sig_L0:.1f}% -- genuinely BETTER than the")
print(f"     asymptote-only route ({100*(SIG_FIT_FROZEN/abs(d_MI)):.0f}%), and comparable to the dwarf "
      f"{100*DWARF_FLOOR_GLS:.1f}% floor.")
print("     That is the strongest honest form of the shape-breaks-it hypothesis and it")
print("     is granted in full.  It still fails the joint, on arithmetic:")
print(f"       the joint needs WB <= {100*need:.2f}% -- TIGHTER than the dwarf floor itself,")
print(f"       because 1/6.31^2 - 1/{100*DWARF_FLOOR_GLS:.1f}^2 leaves only that much room.")
print(f"       best joint anywhere on the ladder = {100*best_joint:.2f}%, i.e. "
      f"{best_joint/TARGET_SLN:.2f}x short.")
print(f"       and even that row needs N ~ {n_need:,.0f} pairs, not the {N_DR4:,} forecast.")
print("  4. THE REALISTIC ROWS ARE MUCH WORSE, and the reasons are all banked, not")
print("     invented: the frozen sigma_sys = 0.02 read as a coherent prescription")
print(f"     offset gives {100*LAD['L3 sigma_sys as a coherent lambda prior, g_ext 2.4%']:.0f}%; "
      f"the banked MI band 1.0508-1.1015 gives "
      f"{100*LAD['L5 banked MI band 1.0508-1.1015 as the lambda prior, g_ext 2.4%']:.0f}%;")
print(f"     the full MI-to-MG bracket 1.0508-1.1389 is a factor-{Chi/Clo:.2f} range in C_eff,")
print(f"     i.e. ~{100*dgam_band/abs(d_MI):.0f}% in a0 from THEORY ALONE.  A 3% coherent photometric")
print(f"     M-L offset costs {100*sig_ML3:.0f}% (WB masses are NOT systematic-free).  And")
print(f"     contamination adds a ONE-SIDED upward bias worth {100*dcon/abs(d_MI):+.0f}% in a0 at the")
print("     DR3 dry-run level -- which is exactly why gamma=1.205 is evidence for")
print("     nothing.  No row on the ladder reaches 3 sigma in the joint.")
print("  5. VERDICT: NO -- WB cannot supply a usable a0 AMPLITUDE for the joint.")
print("     * In the no-EFE reading it supplies ONLY the product C*a0 (exact degeneracy).")
print("     * In the EFE readings it supplies a0 only after the prescription is FIXED,")
print("       and the framework's MI completion is banked as UNWRITTEN, so the")
print("       prescription bracket is a real, non-optional 45-78% a0 uncertainty.")
print("     * Even granting a fixed prescription, exact g_ext, and full orthogonality of")
print(f"       WB-vs-dwarf systematics, the joint reaches {100*best_joint:.2f}%, not "
      f"{100*TARGET_SLN:.2f}%.")
print("     So the ORTHOGONALITY PREMISE OF THE HYPOTHESIS IS CORRECT and irrelevant:")
print("     the blocker is not shared systematics, it is that a0 and the two-body /")
print("     prescription coefficient enter the wide-binary observable in the same")
print("     combination.  This is a DEGENERACY wall.  More pairs, tighter screens and")
print("     DR4's new NSS cut do not touch it.")
print("  6. WHAT WOULD CHANGE THIS (open doors, stated because they exist): (i) a")
print("     WRITTEN MI completion that FIXES C_eff from first principles -- WB then")
print(f"     becomes a real if weak ~{100*LAD['L2 sigma_sys as a per-bin error floor, lambda + g_ext EXACT']:.0f}% a0 datum "
      f"(joint {100*joint_sigma(DWARF_FLOOR_GLS, LAD['L2 sigma_sys as a per-bin error floor, lambda + g_ext EXACT']):.2f}%), still short but no")
print("     longer degenerate; (ii) an independent g_ext,obs at ~1% (the two FROZEN")
print("     conventions differ by 16%) to make the C-free transition-location route")
print("     usable; (iii) DR4 radial velocities removing the deprojection prior-")
print("     sensitivity the banked wb_mond_orbit_mc.py flagged; (iv) attacking the")
print("     DWARF side instead -- the estimator-choice term is 30% of that variance and")
print("     is an ANALYSIS ambiguity, not a data limitation.  None closed; none in hand.")
print("  NOT 'theory closed'.  The framework's a0 amplitude is simply not what a wide-")
print("  binary gamma measures.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "wb_a0_amplitude_degeneracy_results.json")
json.dump(RESULTS, open(out, "w"), indent=1, default=float)
print(f"\n[{os.path.basename(out)} written]")
print("EXIT 0: degeneracy geometry computed. Exit code is not a verdict.")
