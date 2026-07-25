#!/usr/bin/env python3
"""
wb_dwarf_joint_a0.py -- STEP B / THE JOINT: can Gaia wide binaries (WB) supply an
a0-AMPLITUDE constraint whose systematics are ORTHOGONAL to the dwarf a0-line, so that the
JOINT crosses the ~6.31% one-sigma box that a 3-sigma canonical-vs-ALT separation needs?
==========================================================================================
Framework on its OWN terms (de Sitter-Unruh MODIFIED INERTIA, never the standard-MOND lens):
    a0 = c H_Lambda / Z = 9.355e-11 m/s^2  (canonical)  |  ALT rho_total/cH0 = 1.1305e-10
    nu(y) = sqrt(1 + 1/y),  y = g_bar/a0   i.e.  g_obs = sqrt(g_bar^2 + g_bar*a0)
Both footings carried on every load-bearing number (working-rule 4).

INPUTS, all COMMITTED and re-asserted here as regression anchors (nothing re-derived):
  prep_2026/a0_line/reach_target_results.json      -- STEP A: 16.104% box, 10.905% shared
                                                      floor, 11.624% best-SPARC-alone,
                                                      TARGET = 6.3129%
  prep_2026/a0_line/per_galaxy_budget_results.json -- 76.0% shared / 24.0% averaging variance
  real_research/reviews/wb_dr4_prereg_framework_curve.py -- the banked WB gamma_v targets
                                                      (MI 1.1015 dyn / 1.0508 diluted; MG 1.1389)
  prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md   -- FROZEN: sigma_fit 0.019, sigma_sys 0.020,
                                                      sigma_tot 0.028 at N=30k; DR3 gamma =
                                                      1.205 +- 0.035 = contamination-guard zone

WHAT THIS SCRIPT COMPUTES (all closed-form / numerical; no symbolic field theory):
  S1  the WB gamma_v targets, reproduced from the framework's own nu, both footings, both
      frozen g_ext conventions
  S2  the a0 LEVER  L = dln(gamma_v - 1)/dln a0  (numeric central difference AND closed-form),
      for MI-EFE, MG-EFE, and the no-EFE (Milgrom-linear) reading
  S3  THE DEGENERACY THEOREM (exact, proved by moving the number): the EFE-saturated
      asymptote gamma_inf is a function of the RATIO g_ext/a0 ONLY -> WB measures a ratio,
      not an amplitude
  S4  the SHAPE route (transition separation) -- its own lever, computed, not assumed
  S5  sigma_WB(a0)/a0: the full WB a0-error budget, including the HONEST correction that WB
      photometric masses are NOT systematic-free
  S6  THE JOINT: sigma_J(sigma_dwarf, sigma_WB, rho) on the requested grid, the crossing
      sigma_WB*, and the correlation sensitivity
  S7  contamination: one-sided, quantified in a0 units
  S8  GO / NO-GO

HONESTY RAILS: a manufactured GO and a manufactured NO-GO are penalized equally. Every WB
number is traced to a banked script or the frozen pre-registration. The one corner where WB
DOES have a strong a0 lever is computed and reported even though it is not the framework's
own reading. No "theory closed". Exit 0 = numbers computed, NOT a verdict.
"""
import numpy as np, json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
bar = "=" * 98

# ------------------------------------------------------------------ physical constants
G, MSUN, AU = 6.674e-11, 1.989e30, 1.496e11
A0C = 9.354769736111044e-11        # canonical  c H_Lambda / Z   (fire_common.A0C)
A0A = 1.1305322040279838e-10       # ALT        rho_total / c H0
A0_MOND = 1.2e-10                  # Milgrom conventional, for the interleave check
GEXT_P = 1.9 * 9.36e-11            # 1.778e-10  PRIMARY frozen g_ext,obs (prereg S1.1)
GEXT_A = 229.0e3**2 / (8.178 * 3.0856775814913673e19)   # ALT frozen g_ext = Vc^2/R0
M_TOT = 1.5 * MSUN                 # typical DR4 pair; the asymptote is M-independent

# frozen DR4 error model (PREREGISTRATION_DR4.md S1.5)
SIG_FIT_DR4, SIG_SYS_DR4 = 0.019, 0.020
SIG_TOT_DR4 = math.hypot(SIG_FIT_DR4, SIG_SYS_DR4)

# ------------------------------------------------------------------ framework kernel
nu = lambda y: np.sqrt(1.0 + 1.0 / y)
y_newt = lambda yo: 0.5 * (-1.0 + np.sqrt(1.0 + 4.0 * yo**2))   # invert g_obs -> g_N
NCOS = 4001
COS = np.linspace(-1.0, 1.0, NCOS)


def boost_MG(y_int, yE):
    """AQUAL-EFE point-field FORCE boost = <nu(|y_int e + yE z|)>_angles."""
    yt = np.sqrt(y_int**2 + yE**2 + 2.0 * y_int * yE * COS)
    return np.mean(nu(yt))


def boost_MI(y_rel, yE):
    """Framework PER-STAR MI-EFE algebraic law, equal masses (banked construction)."""
    ys = 0.5 * y_rel
    s_ = np.sqrt(1.0 - COS**2)
    y1z, y1x = yE + ys * COS, ys * s_
    y2z, y2x = yE - ys * COS, -ys * s_
    m1, m2 = np.hypot(y1z, y1x), np.hypot(y2z, y2x)
    az = nu(m1) * y1z - nu(m2) * y2z
    ax = nu(m1) * y1x - nu(m2) * y2x
    return np.mean(np.hypot(az, ax) / y_rel)


def gamma_asy(a0, gext, reading):
    """EFE-saturated velocity-boost asymptote gamma_v(s->inf)."""
    yE = y_newt(gext / a0)
    if reading == "MG":
        return math.sqrt(boost_MG(1e-6, yE))
    if reading == "MI":
        return math.sqrt(boost_MI(1e-6, yE))
    if reading == "MI_analytic":                       # closed form, banked cross-check
        L = -1.0 / (2.0 * (yE + 1.0))
        return math.sqrt(nu(yE) * (1.0 + L / 3.0))
    if reading == "MI_dil":                            # observable-dilution lower edge
        return 1.0 + 0.5 * (math.sqrt(boost_MI(1e-6, yE)) - 1.0)
    raise ValueError(reading)


def gamma_noEFE(a0, s_kAU, C=1.0, mtot=M_TOT):
    """No-EFE reading (Milgrom arXiv:2503.07106 Eq29 linear, C=1 == the framework's own
    isolated nu): V^4 = V_N^4 + C M a0 -> gamma_v = (1 + C/y)^(1/4), y = g_N,int/a0."""
    gN = G * mtot / (s_kAU * 1e3 * AU)**2
    return (1.0 + C * a0 / gN)**0.25


# =============================================================== S0 regression anchors
print(bar); print("S0 -- REGRESSION ANCHORS: the committed STEP-A structure (nothing re-derived)")
print(bar)
RT = json.load(open(os.path.join(HERE, "reach_target_results.json")))
PG = json.load(open(os.path.join(HERE, "per_galaxy_budget_results.json")))
TARGET = RT["target_sln"]
S_BOX = RT["box_now_pct"] / 100.0                   # 16.104%  today
S_FLOOR_UG = RT["floor_glscommit_pct"] / 100.0      # 10.905%  shared floor (U,G)
S_FLOOR_UGE = RT["floor_committed_pct"] / 100.0     # 14.038%  shared floor (U,G,Est)
S_BEST_SPARC = RT["best_sparc_alone_pct"] / 100.0   # 11.624%  best SPARC-alone
S_COND = RT["best_conditional_pct"] / 100.0         # 6.778%   full external-prior stack
assert abs(100 * TARGET - 6.3129) < 1e-3
assert abs(100 * S_BOX - 16.104) < 1e-2
assert abs(100 * S_FLOOR_UG - 10.905) < 1e-2
assert abs(100 * S_BEST_SPARC - 11.624) < 1e-2
assert abs(TARGET - abs(math.log(A0A / A0C)) / 3.0) < 1e-12, "target != ln-gap/3"
shared_var = PG["var_shares"]["Ups"] + PG["var_shares"]["gascal"] + PG["var_shares"]["estimator"]
avg_var = PG["var_shares"]["stat"] + PG["var_shares"]["dist"] + PG["var_shares"]["inc"]
assert abs(shared_var - 0.760) < 0.002 and abs(avg_var - 0.240) < 0.002
print(f"  3-sigma separation requirement: ln(a0_ALT/a0_canon)/3 = {100*TARGET:.4f}%   <-- THE TARGET")
print(f"  dwarf a0-line box TODAY            : {100*S_BOX:6.3f}%   (N=310 pts / 49 gas-dom galaxies)")
print(f"  dwarf variance: SHARED (no averaging) {100*shared_var:.1f}%  |  AVERAGING {100*avg_var:.1f}%")
print(f"  dwarf shared floor (Ups+gascal)     : {100*S_FLOOR_UG:6.3f}%   <-- the STEP-A wall")
print(f"  dwarf shared floor (+ estimator)    : {100*S_FLOOR_UGE:6.3f}%")
print(f"  dwarf best SPARC-alone (TRGB+GLS+2x): {100*S_BEST_SPARC:6.3f}%   ({S_BEST_SPARC/TARGET:.2f}x target)")
print(f"  dwarf full external-prior stack     : {100*S_COND:6.3f}%   (still > target)")

# =============================================================== S1 WB gamma targets
print(); print(bar)
print("S1 -- WB gamma_v TARGETS from the framework's OWN nu (both footings, both g_ext)")
print(bar)
print(f"  g_ext PRIMARY (frozen) = {GEXT_P:.4e} m/s^2      g_ext ALT (Vc^2/R0) = {GEXT_A:.4e}"
      f"  ({100*(GEXT_A/GEXT_P-1):+.1f}%)")
print(f"  {'footing a0':>14}{'g_ext':>10}{'y_ext,obs':>11}{'y_ext,N':>9}"
      f"{'MI dyn':>9}{'MI dil':>9}{'MG':>9}")
TARG = {}
for fl, a0v in (("canon", A0C), ("ALT", A0A)):
    for gl, gv in (("primary", GEXT_P), ("alt", GEXT_A)):
        yE = y_newt(gv / a0v)
        mi, md, mg = gamma_asy(a0v, gv, "MI"), gamma_asy(a0v, gv, "MI_dil"), gamma_asy(a0v, gv, "MG")
        TARG[(fl, gl)] = dict(yE=yE, MI=mi, MI_dil=md, MG=mg)
        print(f"  {a0v:>14.4e}{gl:>10}{gv/a0v:>11.4f}{yE:>9.4f}{mi:>9.4f}{md:>9.4f}{mg:>9.4f}")
b = TARG[("canon", "primary")]
assert abs(b["MG"] - 1.1389) < 5e-4, "MG asymptote off banked 1.1389"
assert abs(b["MI"] - 1.1015) < 5e-4, "MI asymptote off banked 1.1015"
assert abs(b["MI_dil"] - 1.0508) < 5e-4, "diluted edge off banked 1.0508"
assert abs(gamma_asy(A0C, GEXT_P, "MI_analytic") - 1.0998) < 5e-4
assert abs(b["yE"] - 1.4647) < 2e-3
print("  [banked WB targets reproduced: MI 1.1015 / diluted 1.0508 / MG 1.1389, y_ext,N 1.4647]")
print(f"  NOTE the interleave: canonical-a0 MG ({TARG[('canon','primary')]['MG']:.4f}) vs ALT-a0 MI "
      f"({TARG[('ALT','primary')]['MI']:.4f}) differ by only {abs(TARG[('canon','primary')]['MG']-TARG[('ALT','primary')]['MI']):.4f}")
print("  in gamma_v -- a 21% a0 change is nearly ERASED by switching the EFE reading (S2/S5).")

# =============================================================== S2 the a0 lever
print(); print(bar)
print("S2 -- THE a0 LEVER  L = dln(gamma_v - 1)/dln a0   (numeric AND closed-form)")
print(bar)


def lever_asy(a0, gext, reading, h=1e-3):
    """d ln(gamma-1)/d ln a0 by central difference in ln a0."""
    gp, gm = gamma_asy(a0 * math.exp(h), gext, reading), gamma_asy(a0 * math.exp(-h), gext, reading)
    return (math.log(gp - 1.0) - math.log(gm - 1.0)) / (2 * h)


def lever_MG_closed(a0, gext):
    """Closed form for the MG asymptote gamma = sqrt(nu(yE)):
         gN_ext = 0.5(-a0 + sqrt(a0^2 + 4 gext^2)),  yE = gN_ext/a0
         dln gN_ext/dln a0 = 0.5 a0 (a0/sqrt(a0^2+4gext^2) - 1)/gN_ext
         dln gamma/dln yE = -1/(4 yE nu^2);  dln(gamma-1) = (gamma/(gamma-1)) dln gamma."""
    R = math.sqrt(a0**2 + 4 * gext**2)
    gNe = 0.5 * (-a0 + R)
    dln_gNe = 0.5 * a0 * (a0 / R - 1.0) / gNe
    dln_yE = dln_gNe - 1.0
    yE = gNe / a0
    nn = nu(yE)
    gam = math.sqrt(nn)
    return (gam / (gam - 1.0)) * (-1.0 / (4.0 * yE * nn**2)) * dln_yE


print(f"  {'reading':<26}{'footing':>8}{'g_ext':>9}{'gamma-1':>10}{'L numeric':>11}"
      f"{'L closed':>10}{'sig(a0)/a0 per 0.01 in gamma':>30}")
LEV = {}
for reading, lab in (("MG", "MG-EFE (AQUAL point)"), ("MI", "MI-EFE per-star (framework)"),
                     ("MI_dil", "MI-EFE, obs-diluted edge")):
    for fl, a0v in (("canon", A0C), ("ALT", A0A)):
        gv = GEXT_P
        g = gamma_asy(a0v, gv, reading)
        Ln = lever_asy(a0v, gv, reading)
        Lc = lever_MG_closed(a0v, gv) if reading == "MG" else float("nan")
        # sigma(a0)/a0 = [sigma(gamma)/(gamma-1)] / L
        per = (0.01 / (g - 1.0)) / Ln
        LEV[(reading, fl)] = dict(gamma=g, L=Ln, per001=per)
        print(f"  {lab:<26}{fl:>8}{'primary':>9}{g-1:>10.4f}{Ln:>11.4f}"
              f"{Lc:>10.4f}{100*per:>29.2f}%")
assert abs(LEV[("MG", "canon")]["L"] - lever_MG_closed(A0C, GEXT_P)) < 2e-3, "MG lever numeric != closed form"
print("  [numeric lever == closed form for MG to <2e-3: the lever is verified, not asserted]")
print()
print("  READING: L ~ 1.0-1.3 means (gamma_v - 1) responds ~LINEARLY to a0 -- the lever is not")
print(f"  tiny. The problem is the DENOMINATOR: gamma_v - 1 is only ~{b['MI']-1:.3f} (MI) / "
      f"{b['MG']-1:.3f} (MG),")
print("  so a sigma(gamma) of 0.01 is ALREADY a ~7-10% a0 error, and 0.028 (the frozen DR4")
print("  total) is a ~19-22% a0 error. This is an EFE-SATURATION penalty, not a data-quality one.")
print()
print("  The no-EFE reading (Milgrom linear Eq29, C=1 == the framework's own isolated nu) has")
print("  NO g_ext at all -> a much better lever, but predicts a LARGE boost at wide separation:")
print(f"  {'s [kAU]':>8}{'y=gN/a0':>10}{'gamma_v':>10}{'L':>8}{'sig(a0)/a0 @ sig(gam)=0.028':>30}")
NOEFE = {}
for s in (5., 10., 15., 20., 30.):
    g = gamma_noEFE(A0C, s)
    yv = G * M_TOT / (s * 1e3 * AU)**2 / A0C
    Ln = 0.25 * (1.0 / yv) / (1.0 + 1.0 / yv) * g / (g - 1.0)
    frac = (SIG_TOT_DR4 / (g - 1.0)) / Ln
    NOEFE[s] = dict(y=yv, gamma=g, L=Ln, frac=frac)
    print(f"  {s:>8.0f}{yv:>10.4f}{g:>10.4f}{Ln:>8.4f}{100*frac:>29.2f}%")
print("  ==> the a0-SENSITIVE corner is the DEEP no-EFE regime (gamma_v -> 1.6-1.8 by 20-30 kAU).")
print("  Banked (wb_deprojection_mc): the DR3 deep bins sit ~2-3 sigma above the calibrated")
print("  Newtonian MC while a MOND upper bound OVERSHOOTS them by 6-22 sigma. So the corner")
print("  with the GOOD a0 lever is the corner the data already disfavours, and the corner the")
print("  data allows (EFE-saturated, gamma ~ 1.10-1.14) is the corner with the BAD lever.")
print("  That trade is the structural reason WB is a weak a0-AMPLITUDE probe.")

# =============================================================== S3 degeneracy theorem
print(); print(bar)
print("S3 -- THE DEGENERACY THEOREM (exact): the WB asymptote measures g_ext/a0, NOT a0")
print(bar)
print("  gamma_inf depends on a0 ONLY through y_ext,N = y_N(g_ext/a0). Therefore")
print("  gamma_inf(lambda*g_ext, lambda*a0) = gamma_inf(g_ext, a0) IDENTICALLY. Prove by moving")
print("  the number (rescale BOTH by lambda and watch gamma_inf not move):")
print(f"  {'lambda':>8}{'a0':>12}{'g_ext':>12}{'MI dyn':>12}{'MG':>12}{'|dMI|':>11}{'|dMG|':>11}")
mx = 0.0
for lam in (0.5, 0.7, 1.0, 1.3, 2.0, 3.0):
    mi, mg = gamma_asy(A0C * lam, GEXT_P * lam, "MI"), gamma_asy(A0C * lam, GEXT_P * lam, "MG")
    dmi, dmg = abs(mi - b["MI"]), abs(mg - b["MG"])
    mx = max(mx, dmi, dmg)
    print(f"  {lam:>8.1f}{A0C*lam:>12.4e}{GEXT_P*lam:>12.4e}{mi:>12.6f}{mg:>12.6f}"
          f"{dmi:>11.2e}{dmg:>11.2e}")
assert mx < 1e-12, f"scaling degeneracy is NOT exact ({mx:.2e}) -- recheck"
print(f"  [EXACT to {mx:.1e} = machine precision. THE DEGENERACY IS A THEOREM, not an estimate.]")
print()
print("  CONSEQUENCE (this is task item 3, and the answer is WORSE than 'a0 x C'): the frozen")
print("  DR4 statistic is a 1-parameter profile on the ASYMPTOTE gamma_inf (prereg S1.3). An")
print("  asymptote measurement therefore constrains the RATIO g_ext/a0. By the theorem the")
print("  transfer is EXACT, not linearized: a g_ext error of factor f moves the inferred a0 by")
print("  the SAME factor f, so sigma(ln a0) = sigma(ln g_ext) identically -- no cancellation.")
GEXT_EXACT = abs(math.log(GEXT_A / GEXT_P))
print(f"    g_ext CONVENTION span (primary 1.778e-10 vs Vc^2/R0 2.078e-10 = {100*(GEXT_A/GEXT_P-1):+.1f}%):")
print(f"      EXACT a0 systematic (by the theorem)      = |ln(g_ext,alt/g_ext,pri)| = {100*GEXT_EXACT:.1f}%")
gext_sys = {}
for reading in ("MI", "MG"):
    gp = gamma_asy(A0C, GEXT_P, reading); ga = gamma_asy(A0C, GEXT_A, reading)
    dgam = abs(ga - gp)
    L = LEV[(reading, "canon")]["L"]
    fr = (dgam / (gp - 1.0)) / L
    gext_sys[reading] = fr
    print(f"      linearized cross-check, {reading}-EFE: dgamma = {dgam:.4f} -> {100*fr:.1f}% "
          f"(agrees with the exact {100*GEXT_EXACT:.1f}% to {100*abs(fr-GEXT_EXACT):.1f} pts; the")
    print(f"        gap is pure finite-step curvature, and the EXACT number is the one to quote)")
gext_sys["exact"] = GEXT_EXACT
print("  HONESTY BOTH WAYS: this is a frozen MODELLING-CONVENTION span, not a measurement error.")
print("  The Galactic radial acceleration Vc^2/R0 is itself known to ~2-3% (Vc = 229 +- 2 km/s,")
print("  R0 = 8.178 +- 0.026 kpc), so a RESOLVED convention would leave only ~3-6% here. g_ext")
print("  is therefore NOT the binding term -- but the convention MUST be resolved before any WB")
print("  a0 number is quoted, and the prereg deliberately froze BOTH values (no freedom later).")

# =============================================================== S4 the shape route
print(); print(bar)
print("S4 -- THE SHAPE ROUTE: does the TRANSITION SEPARATION give an a0 lever free of g_ext?")
print(bar)
print("  Frozen transition shape (prereg S1.3): gamma(y) = 1 + (gamma_inf-1) y_extN/(y_extN+y).")
print("  The knee sits at g_N,int = y_extN*a0 = g_ext,N = 0.5(-a0 + sqrt(a0^2 + 4 g_ext^2)),")
print("  i.e. r_knee = sqrt(G M / g_ext,N). a0 enters ONLY as a sub-leading correction:")


def r_knee(a0, gext, mtot=M_TOT):
    gNe = 0.5 * (-a0 + math.sqrt(a0**2 + 4 * gext**2))
    return math.sqrt(G * mtot / gNe) / (1e3 * AU)


h = 1e-3
dlnr = (math.log(r_knee(A0C * math.exp(h), GEXT_P)) - math.log(r_knee(A0C * math.exp(-h), GEXT_P))) / (2 * h)
R = math.sqrt(A0C**2 + 4 * GEXT_P**2)
gNe = 0.5 * (-A0C + R)
dlnr_closed = -0.5 * (0.5 * A0C * (A0C / R - 1.0) / gNe)
print(f"  r_knee(canonical) = {r_knee(A0C, GEXT_P):.3f} kAU   (g_ext,N = {gNe:.4e} m/s^2)")
print(f"  d ln r_knee / d ln a0 = {dlnr:+.5f} (numeric) = {dlnr_closed:+.5f} (closed form)")
assert abs(dlnr - dlnr_closed) < 1e-4
amp = 1.0 / abs(dlnr)
print(f"  ==> AMPLIFICATION {amp:.1f}x: sigma(a0)/a0 = {amp:.1f} * sigma(r_knee)/r_knee.")
print(f"      Reaching sigma(a0)/a0 = {100*TARGET:.2f}% needs the knee separation to "
      f"{100*TARGET/amp:.2f}%, i.e. +-{1e3*TARGET/amp*r_knee(A0C,GEXT_P):.0f} AU on an "
      f"{r_knee(A0C,GEXT_P):.2f} kAU knee.")
print("  Banked (wb_dr4_prereg_framework_curve.py header): sky-plane deprojection alone shifts")
print("  the transition by ~10-20% in s. And the frozen DR4 fit does NOT fit shape at all --")
print("  prereg S1.3: 'the gate certifies ASYMPTOTE RECOVERY, not shape discrimination.'")
print("  ==> THE SHAPE ROUTE IS DEAD, for a physical reason: once g_ext > a0 (locally 1.9 a0),")
print("      EFE saturation puts BOTH the plateau height AND the knee under g_ext's control.")

# =============================================================== S5 sigma_WB(a0) budget
print(); print(bar)
print("S5 -- sigma_WB(a0)/a0: THE HONEST WB a0-ERROR BUDGET")
print(bar)


def a0err(sig_gamma, reading="MI", fl="canon"):
    d = LEV[(reading, fl)]
    return (sig_gamma / (d["gamma"] - 1.0)) / d["L"]


print("  (a) STATISTICAL + FROZEN-SYSTEMATIC (prereg S1.5, N=30k DR4):")
print(f"  {'sigma(gamma) source':<46}{'value':>8}{'MI: sig(a0)/a0':>17}{'MG: sig(a0)/a0':>17}")
rows_sg = [("DR4 frozen total sigma_tot", SIG_TOT_DR4),
           ("DR4 statistical only sigma_fit", SIG_FIT_DR4),
           ("DR4 frozen systematic only sigma_sys (N->inf)", SIG_SYS_DR4),
           ("hypothetical sigma(gamma) = 0.010", 0.010),
           ("DR3 dry run sigma (10,624 pairs)", 0.035)]
for lab, sg in rows_sg:
    print(f"  {lab:<46}{sg:>8.3f}{100*a0err(sg,'MI'):>16.1f}%{100*a0err(sg,'MG'):>16.1f}%")
sig_wb_dr4 = a0err(SIG_TOT_DR4, "MI")
sig_wb_stat_floor = a0err(SIG_SYS_DR4, "MI")
print(f"  ==> even with INFINITE statistics the frozen sigma_sys=0.020 floors WB at "
      f"{100*sig_wb_stat_floor:.1f}% (MI) / {100*a0err(SIG_SYS_DR4,'MG'):.1f}% (MG).")
print()
print("  (b) WB PHOTOMETRIC MASSES -- CORRECTING THE PRIOR OVERSTATEMENT ('no Upsilon at all'):")
SIG_M_COH = 0.055        # Banik+24 S2.3.3 mass-calibration error (pipeline uses 5% per pair)
N_DR4 = 30000
# vtilde = v/sqrt(GM/s): a COHERENT dlnM shifts every vtilde by -dlnM/2, hence gamma by -gamma*dlnM/2
for reading in ("MI", "MG"):
    g = LEV[(reading, "canon")]["gamma"]
    dgam = 0.5 * SIG_M_COH * g
    print(f"    COHERENT {100*SIG_M_COH:.1f}% mass-calibration offset, UNABSORBED: dgamma = "
          f"{dgam:.4f} -> sigma(a0)/a0 = {100*a0err(dgam,reading):.1f}%  ({reading})")
rand = 0.5 * 0.05 / math.sqrt(N_DR4) * 1.2533     # per-pair random, median efficiency factor
print(f"    PER-PAIR RANDOM 5% mass scatter at N={N_DR4}: dgamma = {rand:.5f} -> "
      f"sigma(a0)/a0 = {100*a0err(rand,'MI'):.2f}%  (negligible: it DOES average down)")
print("    => WB masses are ~5.5% (main-sequence M_G->M cubic), vs the dwarf 0.10 dex = 23%")
print("       stellar M/L. TIGHTER, YES -- BUT NOT ABSENT: unabsorbed, the COHERENT part alone")
print(f"       is a ~{100*a0err(0.5*SIG_M_COH*LEV[('MI','canon')]['gamma'],'MI'):.0f}% a0 systematic, i.e. the SAME ORDER as the dwarf shared floor.")
print("       It is absorbed by the frozen anchored-kappa nuisance (window [0.95,1.05] in vtilde")
print("       = +-10% in mass, which brackets 5.5%), leaving a residual inside sigma_sys=0.020.")
print("       That absorption is SHAPE-DEPENDENT (kappa is anchored on the high-y bins where the")
print("       boost is ~1), and shape is a flagged NON-tunable systematic (prereg S1.3). So the")
print("       honest statement is: absorbed, not absent -- and its absorption is a liability.")
print()
print("  (c) THEORY-SIDE PRESCRIPTION SYSTEMATIC (the dominant term):")


def a0_from_gamma(gtarget, gext, reading, lo=2e-11, hi=1e-9):
    """Invert the asymptote for a0 at fixed measured gamma (bisection; monotone in a0)."""
    f = lambda a: gamma_asy(a, gext, reading) - gtarget
    if f(lo) * f(hi) > 0:
        return float("nan")
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if f(lo) * f(m) <= 0:
            hi = m
        else:
            lo = m
    return 0.5 * (lo + hi)


gfix = b["MG"]                       # a single measured gamma_v = 1.1389
a_mg = a0_from_gamma(gfix, GEXT_P, "MG")
a_mi = a0_from_gamma(gfix, GEXT_P, "MI")
print(f"    ONE measured gamma_v = {gfix:.4f} maps to  a0 = {a_mg:.4e} under MG-EFE")
print(f"                                            a0 = {a_mi:.4e} under MI-EFE  "
      f"(ratio {a_mi/a_mg:.3f})")
presc_mimg = abs(math.log(a_mi / a_mg))
print(f"    => MI-vs-MG READING alone = {100*presc_mimg:.0f}% a0 systematic, and the prereg S1.5")
print(f"       PRE-DECLARES MI-vs-MG as 'likely UNDECIDABLE in DR4' (needs N~45k AND sigma_sys<0.01).")
a_up = a0_from_gamma(1.10, GEXT_P, "MI")
a_lo = a0_from_gamma(1.05, GEXT_P, "MI")
presc_band = abs(math.log(a_lo / a_up))
print(f"    WORSE: the framework's OWN frozen MI target is a BAND 1.05-1.10 (prescription +")
print(f"       observable-dilution bracket, explicitly 'not a theorem'). Inverting the band:")
print(f"       gamma=1.10 -> a0 = {a_up:.4e};  gamma=1.05 -> a0 = {a_lo:.4e}  "
      f"(ratio {a_lo/a_up:.2f} = {100*presc_band:.0f}% in ln a0)")
print(f"       The framework's own prediction band is {presc_band/abs(math.log(A0A/A0C)):.1f}x WIDER than the whole")
print(f"       canonical-vs-ALT footing gap it would have to resolve ({100*abs(math.log(A0A/A0C)):.1f}%).")
print()
print("  (d) THE ASSEMBLED WB a0 BUDGET (quadrature; both readings, canonical footing):")
budgets = {}
for name, terms in (
    ("BEST CASE  (stat+sys only, prescription+g_ext ASSUMED SOLVED)",
     [("DR4 sigma_tot", sig_wb_dr4)]),
    ("REALISTIC  (+ resolved g_ext convention at 3%)",
     [("DR4 sigma_tot", sig_wb_dr4), ("g_ext at 3%", 0.03)]),
    ("AS FROZEN  (+ frozen g_ext convention span, exact)",
     [("DR4 sigma_tot", sig_wb_dr4), ("g_ext convention", GEXT_EXACT)]),
    ("AS FROZEN + MI-vs-MG reading undecided",
     [("DR4 sigma_tot", sig_wb_dr4), ("g_ext convention", GEXT_EXACT),
      ("MI-vs-MG", presc_mimg)]),
    ("AS FROZEN + the framework's OWN 1.05-1.10 band",
     [("DR4 sigma_tot", sig_wb_dr4), ("g_ext convention", GEXT_EXACT),
      ("MI band 1.05-1.10", presc_band)]),
    ("FULLY REPAIRED (sig_gam 0.010 + g_ext 3% + prescription a theorem)",
     [("sigma(gamma)=0.010", a0err(0.010, "MI")), ("g_ext at 3%", 0.03)]),
):
    tot = math.sqrt(sum(v**2 for _, v in terms))
    budgets[name] = tot
    print(f"    {name:<58}{100*tot:>7.1f}%   [" + " + ".join(f"{k} {100*v:.1f}%" for k, v in terms) + "]")

# =============================================================== S6 THE JOINT
print(); print(bar)
print("S6 -- THE JOINT: sigma_J(a0) for independent (orthogonal-systematic) dwarf + WB")
print(bar)


def joint(sd, sw, rho=0.0):
    """Inverse-variance combination of two measurements of the same ln a0, correlation rho."""
    num = sd**2 * sw**2 * (1.0 - rho**2)
    den = sd**2 + sw**2 - 2.0 * rho * sd * sw
    return math.sqrt(num / den)


def sw_needed(sd, tgt=TARGET):
    """sigma_WB that pushes the independent joint to exactly tgt (nan if impossible)."""
    if sd <= tgt:
        return 0.0
    v = 1.0 / tgt**2 - 1.0 / sd**2
    return math.sqrt(1.0 / v)


assert abs(joint(0.10, 0.10) - 0.10 / math.sqrt(2)) < 1e-12, "joint formula broken"
assert abs(joint(0.116, 1e6) - 0.116) < 1e-6, "joint must reduce to sigma_d as sigma_w->inf"
GRID_W = [0.05, 0.10, 0.15, 0.25, 0.40]
DWARF = [("today, committed box", S_BOX), ("best SPARC-alone (TRGB+GLS+2x)", S_BEST_SPARC),
         ("shared floor Ups+gascal (the wall)", S_FLOOR_UG),
         ("committed floor incl. estimator", S_FLOOR_UGE),
         ("full external-prior stack", S_COND)]
print(f"  (a) JOINT sigma(a0)/a0 on the requested grid  [independent, rho = 0]")
hdr = f"  {'sigma_dwarf':<36}{'alone':>8}" + "".join(f"{'W='+str(int(100*x))+'%':>9}" for x in GRID_W) + f"{'sig_WB* for 6.31%':>19}"
print(hdr)
JOINTTAB = {}
for lab, sd in DWARF:
    cells = [joint(sd, sw) for sw in GRID_W]
    need = sw_needed(sd)
    JOINTTAB[lab] = dict(sigma_dwarf=sd, joint={str(w): j for w, j in zip(GRID_W, cells)},
                         sw_needed=need)
    print(f"  {lab:<36}{100*sd:>7.2f}%" + "".join(f"{100*c:>8.2f}%" for c in cells)
          + f"{100*need:>18.2f}%")
print(f"  (target = {100*TARGET:.2f}%; entries at or below it would be a GO)")
print()
print("  (b) THE DECISIVE CROSSING -- how good must WB be to break the STEP-A wall?")
for lab, sd in DWARF[:4]:
    need = sw_needed(sd)
    sg_mi = need * LEV[("MI", "canon")]["L"] * (LEV[("MI", "canon")]["gamma"] - 1.0)
    sg_mg = need * LEV[("MG", "canon")]["L"] * (LEV[("MG", "canon")]["gamma"] - 1.0)
    print(f"    dwarf at {100*sd:5.2f}%  ->  needs sigma_WB(a0) <= {100*need:5.2f}%"
          f"   <=>  sigma(gamma_v) <= {sg_mi:.4f} (MI) / {sg_mg:.4f} (MG)")
need_best = sw_needed(S_BEST_SPARC)
sg_req_mi = need_best * LEV[("MI", "canon")]["L"] * (LEV[("MI", "canon")]["gamma"] - 1.0)
sg_req_mg = need_best * LEV[("MG", "canon")]["L"] * (LEV[("MG", "canon")]["gamma"] - 1.0)
print(f"    ==> the requirement is sigma_WB(a0) ~ {100*need_best:.1f}%, i.e. sigma(gamma_v) ~ "
      f"{sg_req_mi:.4f}-{sg_req_mg:.4f}.")
print(f"        The FROZEN DR4 sigma_tot is {SIG_TOT_DR4:.3f} ({SIG_TOT_DR4/sg_req_mi:.1f}x too large) and the")
print(f"        FROZEN sigma_sys alone is {SIG_SYS_DR4:.3f} ({SIG_SYS_DR4/sg_req_mi:.1f}x too large) -- so N=infinity")
print("        does NOT fix it at the frozen systematic allowance.")
print()
print("  (c) WHAT THE JOINT ACTUALLY BUYS at the deliverable sigma_WB (dwarf at its floor):")
print(f"  {'WB budget scenario':<58}{'sig_WB':>8}{'joint':>9}{'canon-vs-ALT':>14}")
base_sig = joint(S_FLOOR_UG, 1e9)
print(f"  {'(dwarf floor alone, no WB)':<58}{'--':>8}{100*base_sig:>8.2f}%"
      f"{abs(math.log(A0A/A0C))/base_sig:>13.2f}s")
for name, sw in budgets.items():
    j = joint(S_FLOOR_UG, sw)
    print(f"  {name:<58}{100*sw:>7.1f}%{100*j:>8.2f}%{abs(math.log(A0A/A0C))/j:>13.2f}s")
print()
print("  (d) ORTHOGONALITY IS NECESSARY BUT NOT SUFFICIENT -- correlation sensitivity.")
print("      Residual correlation channel: both constraints turn the SAME nu into an observable")
print("      (dwarf 'estimator choice' 8.8%, WB 'EFE prescription'); not a shared offset, but")
print("      not provably rho=0 either. Shown for the realistic sigma_WB values:")
print(f"  {'sigma_dwarf':<20}{'sigma_WB':>9}" + "".join(f"{'rho='+str(r):>11}" for r in (0.0, 0.3, 0.5)))
for sw in (0.15, sig_wb_dr4, 0.40):
    print(f"  {'floor 10.90%':<20}{100*sw:>8.1f}%" + "".join(
        f"{100*joint(S_FLOOR_UG, sw, r):>10.2f}%" for r in (0.0, 0.3, 0.5)))
print("      Correlation DEGRADES the joint over the range that matters (rho=0.3 costs ~1 pt).")
print(f"      CAVEAT (stated, not hidden): the dependence is NON-monotonic once rho exceeds")
print(f"      min/max = sigma_d/sigma_W (= {S_FLOOR_UG/sig_wb_dr4:.2f} here) -- beyond that the optimal GLS weight on")
print("      WB turns NEGATIVE (differencing), which only helps if rho is known exactly. We do")
print("      NOT lean on that regime. Bounded conclusion: over rho in [0,0.5] the joint never")
print("      beats the rho=0 value and never gets worse than dwarf-alone, so the verdict below")
print("      is not correlation-driven in either direction.")

# ---- (e) the ONE corner where WB does cross: on top of a fully-upgraded dwarf constraint ----
print()
print("  (e) THE ONE GO CORNER (reported so the NO-GO is not manufactured): the dwarf full")
print("      external-prior stack (reach_target.py step 5) lands at 6.78% = 2.79 sigma -- a NEAR")
print("      MISS. There, a merely-mediocre WB constraint IS enough to top it over 3 sigma:")
print(f"  {'sigma_WB':<34}{'joint with dwarf 6.78%':>24}{'canon-vs-ALT':>14}{'':>3}")
GAP = abs(math.log(A0A / A0C))
go_corner = {}
for lab, sw in (("(none -- dwarf stack alone)", None), ("15% (needs prescription solved)", 0.15),
                ("17.35% = the exact crossing", sw_needed(S_COND)),
                (f"{100*a0err(SIG_TOT_DR4,'MG'):.0f}% (DR4 frozen, MG reading)", a0err(SIG_TOT_DR4, "MG")),
                (f"{100*sig_wb_dr4:.0f}% (DR4 frozen, MI reading)", sig_wb_dr4),
                ("69% (DR4 + the MI band carried)", budgets["AS FROZEN + the framework's OWN 1.05-1.10 band"])):
    j = S_COND if sw is None else joint(S_COND, sw)
    go_corner[lab] = j
    flag = "GO" if j <= TARGET else "no"
    print(f"  {lab:<34}{100*j:>23.2f}%{GAP/j:>13.2f}s{flag:>4}")
print("      HONEST READING: WB is NOT the wall-breaker -- it cannot rescue the 10.9-11.6% dwarf")
print("      floor (S6a/S6c). Its only real use for the AMPLITUDE is as a ~0.3-0.5 sigma TOP-UP on")
print("      a dwarf constraint that has ALREADY been dragged to ~6.8% by its own dedicated")
print("      campaign -- and even that top-up needs the EFE prescription resolved first, because")
print("      with the framework's own 1.05-1.10 band carried, WB contributes essentially nothing.")

# ---- (f) THE JOINT ON THE SIBLING AGENT'S OWN sigma_WB LADDER -----------------------
SIB = os.path.join(REPO, "real_research", "reviews", "wb_a0_amplitude_degeneracy_results.json")
sib_joint = {}
if os.path.exists(SIB):
    sj = json.load(open(SIB))
    print()
    print("  (f) THE JOINT ON THE WB AGENT'S OWN LADDER (wb_a0_amplitude_degeneracy.py, the")
    print("      DEGENERACY-TEST role). That script does the STRONGER thing: a Fisher fit to the")
    print("      FULL frozen 8-bin gamma(y) curve with the prescription strength lambda as a")
    print("      marginalized nuisance -- so it lets SHAPE information try to break the")
    print("      lambda-a0 degeneracy, which my asymptote-only budget (S5) cannot.")
    print("      INDEPENDENT CROSS-CHECKS between the two scripts (different methods):")
    dg = sj["D4"]["dgdlna0_MI_canonical"]
    print(f"        d gamma/d ln a0 (MI, canonical): theirs {dg:.5f} -> L = {dg/(b['MI']-1):.4f};"
          f"  mine {LEV[('MI','canon')]['L']:.4f}  (agree to {abs(dg/(b['MI']-1)-LEV[('MI','canon')]['L']):.1e})")
    print(f"        MI/MG asymptotes: theirs {sj['anchors']['asy_MI']:.4f}/{sj['anchors']['asy_MG']:.4f};"
          f"  mine {b['MI']:.4f}/{b['MG']:.4f}")
    print(f"        a0-lambda correlation cos = {sj['L3']['MI per-star|canonical']['cos_a0_lam']:.4f},"
          f" variance inflation {sj['L3']['MI per-star|canonical']['inflation']:.1f}x"
          f"  <- the degeneracy, measured")
    sL3 = sj["L3_ladder"]["L3 sigma_sys as a coherent lambda prior, g_ext 2.4%"]
    sL4 = sj["L3_ladder"]["L4 + g_ext frozen-convention spread 15.6% instead of 2.4%"]
    print(f"      TWO INDEPENDENT METHODS, SAME ANSWER: their L3/L4 = {100*sL3:.1f}%/{100*sL4:.1f}% vs my")
    print(f"      asymptote-only {100*sig_wb_dr4:.1f}%/{100*budgets['AS FROZEN  (+ frozen g_ext convention span, exact)']:.1f}%"
          f" -- agreeing to {100*abs(sL4-budgets['AS FROZEN  (+ frozen g_ext convention span, exact)']):.1f} pts (~20% relative). The 21-29% DR4 figure is robust.")
    print(f"      Their L5 ({100*sj['L3_ladder']['L5 banked MI band 1.0508-1.1015 as the lambda prior, g_ext 2.4%']:.1f}%) is FAR more favourable than my hard-quadrature"
          f" {100*presc_band:.0f}%-band")
    print(f"      treatment, because marginalizing over lambda with shape lets the curve absorb part")
    print(f"      of the band. THEIRS IS THE BETTER TREATMENT AND I ADOPT IT -- my 69.6% row is a")
    print(f"      conservative upper bound (band fully degenerate), theirs the properly marginalized one.")
    print()
    print(f"      TWO SEPARATE VERDICT COLUMNS -- do NOT conflate them:")
    print(f"        'breaks WALL?' = joint with the dwarf 10.90% FLOOR reaches {100*TARGET:.2f}%  (the Step-A question)")
    print(f"        'tops CORNER?' = joint with the dwarf 6.78% external-prior stack reaches it")
    print(f"  {'WB agent ladder row':<62}{'sig_WB':>8}{'J@10.90%':>10}{'J@11.62%':>10}"
          f"{'J@6.78%':>9}{'breaks WALL?':>13}{'tops CORNER?':>13}")
    for k in sorted(sj["L3_ladder"].keys()):
        sw = sj["L3_ladder"][k]
        js = [joint(sd, sw) for sd in (S_FLOOR_UG, S_BEST_SPARC, S_COND)]
        wall = "NO-GO" if js[0] > TARGET else "GO"
        corner = "GO" if js[2] <= TARGET else "no"
        sib_joint[k] = dict(sigma_wb=sw, joint_floor=js[0], joint_best=js[1], joint_cond=js[2],
                            breaks_wall=(js[0] <= TARGET), tops_corner=(js[2] <= TARGET))
        print(f"  {k[:62]:<62}{100*sw:>7.1f}%" + "".join(f"{100*j:>9.2f}%" for j in js)
              + f"{wall:>13}{corner:>13}")
    print(f"      EVERY row is NO-GO against the WALL. The GO's are all in the CORNER column, i.e.")
    print(f"      they are top-ups on a dwarf constraint already dragged to 6.78% by its own campaign.")
    L0 = sj["L3_ladder"]["L0 stat only, lambda + g_ext EXACT (counterfactual best case)"]
    print(f"      THE SHARPEST FORM OF THE VERDICT: even their L0 -- the COUNTERFACTUAL BEST CASE,")
    print(f"      prescription EXACT, g_ext EXACT, zero systematics, full 8-bin DR4 statistics --")
    print(f"      gives sigma_WB = {100*L0:.2f}%, and the joint with the dwarf floor is "
          f"{100*joint(S_FLOOR_UG, L0):.2f}% > {100*TARGET:.2f}%.")
    print(f"      WB cannot break the STEP-A wall even in a world with no WB systematics at all.")
    print(f"      It crosses ONLY on top of the 6.78% dwarf external-prior stack (last column).")

# =============================================================== S7 contamination
print(); print(bar)
print("S7 -- CONTAMINATION: one-sided, and it maps OFF THE TOP of the contested a0 band")
print(bar)
G_DR3, S_DR3 = 1.205, 0.035
for reading in ("MG", "MI"):
    a_dr3 = a0_from_gamma(G_DR3, GEXT_P, reading)
    print(f"    DR3 dry-run gamma_v = {G_DR3} (guard zone) inverted under {reading}-EFE -> "
          f"a0 = {a_dr3:.4e} = {a_dr3/A0C:.2f}x canonical")
print(f"    Both land ABOVE standard-MOND {A0_MOND:.2e} and above the ALT footing {A0A:.3e} --")
print(f"    i.e. off the top of the entire {A0C:.3e}-{A0_MOND:.2e} contested band. The signature of")
print("    CONTAMINATION, not of an a0 measurement, exactly as the prereg pre-declared (S1.6).")
f_trip_absorb = 0.195                    # banked wb_threshold_audit: 0.19-0.20 absorbs the excess
dgam_dftrip = (G_DR3 - 1.0) / f_trip_absorb
dg_budget = sg_req_mi
print(f"    Banked (wb_threshold_audit): a Newtonian population needs f_triple ~ 0.19-0.20 to")
print(f"    absorb the DR3 deep-bin excess -> dgamma/df_triple ~ {dgam_dftrip:.2f} per unit fraction.")
print(f"    To hold the a0-amplitude systematic inside the required dgamma = {dg_budget:.4f}, the")
print(f"    RESIDUAL hidden-companion fraction must be known to Delta f_triple <= "
      f"{dg_budget/dgam_dftrip:.4f} ({100*dg_budget/dgam_dftrip:.1f}% absolute).")
print("    The frozen sigma_sys = 0.020 covers eccentricity, footing and shape -- it carries NO")
print("    residual-contamination allowance. Using WB for an a0 AMPLITUDE would require adding")
print("    one, and it is one-sided (contamination only pushes gamma, hence a0, UP).")
print("    DR4's NSS screen (cut 12) is the designed detector for exactly this, and the NSS-off")
print("    ladder rung MEASURES what it removes -- but 1%-absolute residual-triple control is an")
print("    unbudgeted, unproven requirement, not a banked capability.")

# =============================================================== S8 verdict
print(); print(bar)
print("S8 -- GO / NO-GO")
print(bar)
best = budgets["BEST CASE  (stat+sys only, prescription+g_ext ASSUMED SOLVED)"]
frozen = budgets["AS FROZEN + the framework's OWN 1.05-1.10 band"]
print(f"  (i)  IS THE HYPOTHESIS TRUE? YES on orthogonality: WB systematics (hierarchical")
print(f"       contamination, deprojection, eccentricity prior, photometric MS masses) share NO")
print(f"       offset with the dwarf line (stellar M/L, HI gas calibration, distance, estimator).")
print(f"       The joint therefore DOES combine as independent measurements -- S6 is valid.")
print(f"  (ii) BUT ORTHOGONALITY IS NOT THE BINDING CONSTRAINT. The requirement is")
print(f"       sigma_WB(a0) <= {100*need_best:.1f}% (dwarf at {100*S_BEST_SPARC:.2f}%) / {100*sw_needed(S_FLOOR_UG):.1f}% (dwarf at its {100*S_FLOOR_UG:.2f}% floor).")
print(f"       Deliverable today (DR3): NOTHING -- gamma = 1.205 +- 0.035 is in the frozen")
print(f"         contamination-guard zone, pre-declared 'evidence for nothing'; inverted it gives")
print(f"         a0 = 1.4-1.7x canonical, off the top of the contested band (S7). NO CONSTRAINT.")
print(f"       Deliverable with DR4 at the frozen allowances: sigma_WB(a0) = {100*sig_wb_dr4:.0f}% (MI) /"
      f" {100*a0err(SIG_TOT_DR4,'MG'):.0f}% (MG),")
print(f"         floored at {100*sig_wb_stat_floor:.0f}% even at N = infinity by the frozen sigma_sys = 0.020.")
print(f"       With the framework's own frozen MI band 1.05-1.10 carried: {100*frozen:.0f}% (my hard-quadrature")
print(f"         upper bound) / 16.9% (the WB agent's properly-marginalized Fisher value, adopted).")
if sib_joint:
    _L0 = sib_joint["L0 stat only, lambda + g_ext EXACT (counterfactual best case)"]
    print(f"       THE DECISIVE NUMBER (S6f, the WB agent's own COUNTERFACTUAL BEST CASE -- prescription")
    print(f"         EXACT, g_ext EXACT, no systematics at all, full 8-bin DR4 statistics):")
    print(f"         sigma_WB = {100*_L0['sigma_wb']:.2f}%  ->  joint with the dwarf floor = {100*_L0['joint_floor']:.2f}%  >  {100*TARGET:.2f}%.")
    print(f"         WB fails to break the wall even in a world where WB has NO systematics. The")
    print(f"         NO-GO is therefore STRUCTURAL, not a data-quality or contamination complaint.")
print(f"  (iii) VERDICT: **NO-GO now, NO-GO with DR4 as frozen, as a WALL-BREAKER.** The joint at the DR4-deliverable")
print(f"       sigma_WB moves the dwarf floor {100*S_FLOOR_UG:.2f}% -> {100*joint(S_FLOOR_UG, sig_wb_dr4):.2f}%, i.e. canonical-vs-ALT from")
print(f"       {abs(math.log(A0A/A0C))/S_FLOOR_UG:.2f} sigma to {abs(math.log(A0A/A0C))/joint(S_FLOOR_UG, sig_wb_dr4):.2f} sigma -- a gain of "
      f"{abs(math.log(A0A/A0C))/joint(S_FLOOR_UG, sig_wb_dr4)-abs(math.log(A0A/A0C))/S_FLOOR_UG:+.2f} sigma. Not a wall-breaker.")
print(f"       BUT NOT 'no help at all' (S6e): if the DWARF side is first dragged to its full")
print(f"       external-prior stack ({100*S_COND:.2f}% = {GAP/S_COND:.2f} sigma, itself a dedicated ~30-50-dwarf")
print(f"       TRGB + 0.05-dex M/L + 5%-HI campaign), then a WB constraint at <= {100*sw_needed(S_COND):.1f}% tops it")
print(f"       over 3 sigma. Whether DR4 clears {100*sw_needed(S_COND):.1f}% is METHOD-DEPENDENT and genuinely marginal:")
print(f"       my asymptote-only budget says {100*a0err(SIG_TOT_DR4,'MG'):.0f}% (MG) / {100*sig_wb_dr4:.0f}% (MI) -- BOTH MISS; the WB agent's")
print(f"       full-curve marginalized L5 says 16.9% -- CLEARS, but by 0.02 pts (6.29 vs 6.31%).")
print(f"       So: a coin-flip on ANALYSIS METHOD at the 0.1-sigma level, not a robust GO. It")
print(f"       vanishes outright on their L3/L4/L6 rows (21-25%) and on L7 (prescription free).")
print(f"  (iv) WHY -- and it is NOT the reason one would guess. The blocker is not contamination")
print(f"       and not photometric masses; it is EFE SATURATION. Locally g_ext = 1.9 a0 > a0, so")
print(f"       (S3, exact) the WB asymptote is a function of g_ext/a0 ONLY: a RATIO, never an")
print(f"       amplitude. The one regime with a strong a0 lever (deep, no-EFE, gamma -> 1.6-1.8)")
print(f"       is the regime existing data already disfavours (S2). Layered on top, the")
print(f"       framework's own MI-EFE target is a BAND 1.05-1.10 whose inversion spans")
print(f"       {100*presc_band:.0f}% in a0 -- {presc_band/abs(math.log(A0A/A0C)):.1f}x the footing gap it would have to resolve.")
print(f"  (v)  WHAT WOULD CHANGE IT (stated so the door is not falsely closed):")
print(f"       1. WRITE THE MI COMPLETION so the EFE prescription is a theorem, not a band. This")
print(f"          is the single largest term ({100*presc_band:.0f}%) and it is a THEORY task, not an observing one.")
print(f"       2. Resolve the g_ext convention (primary vs Vc^2/R0) -> the EXACT {100*GEXT_EXACT:.0f}% becomes ~3%")
print(f"          (Vc^2/R0 is known to ~2-3%); this is cheap and should be done regardless.")
print(f"       3. Beat sigma_sys = 0.020 down below ~0.010 (eccentricity model + shape), which the")
print(f"          prereg pre-declares as NOT assumable and forbids shrinking post hoc.")
print(f"       With ALL THREE done, sigma_WB(a0) -> {100*a0err(0.010,'MI'):.0f}% (MI), and the joint with the dwarf")
print(f"       floor is {100*joint(S_FLOOR_UG, a0err(0.010,'MI')):.2f}% -- STILL above {100*TARGET:.2f}%. Even the fully-repaired WB")
print(f"       channel does not, by itself, reach 3 sigma.")
print(f"  (vi) The honest ranking of levers for the a0 AMPLITUDE is therefore UNCHANGED by this")
print(f"       analysis: the dwarf-side external inputs (0.05-dex M/L prior + 5% HI calibration +")
print(f"       a resolved estimator, reach_target.py step 5 -> {100*S_COND:.2f}%) remain the shortest path,")
print(f"       and the WB channel's real value stays what the prereg already froze it as: a test")
print(f"       of the nu + EFE PRESCRIPTION (Newton vs boost), not a measurement of a0.")
print("  Neither footing is excluded; nothing here is 'closed'.")

# =============================================================== JSON
out = dict(
    target_sln=TARGET, target_pct=100 * TARGET,
    a0_canon=A0C, a0_alt=A0A, ln_gap=abs(math.log(A0A / A0C)),
    dwarf=dict(box_now=S_BOX, best_sparc_alone=S_BEST_SPARC, floor_UG=S_FLOOR_UG,
               floor_UGE=S_FLOOR_UGE, cond_stack=S_COND,
               shared_var_frac=shared_var, averaging_var_frac=avg_var),
    wb_targets={f"{k[0]}_{k[1]}": v for k, v in
                ((k, {kk: float(vv) for kk, vv in v.items()}) for k, v in TARG.items())},
    levers={f"{k[0]}_{k[1]}": dict(gamma=v["gamma"], L=v["L"],
                                   a0err_per_0p01_gamma=v["per001"]) for k, v in LEV.items()},
    lever_noEFE={str(k): v for k, v in NOEFE.items()},
    degeneracy_exact_max_dev=float(mx),
    gext_convention_a0_sys=gext_sys,
    gext_convention_a0_sys_exact=GEXT_EXACT,
    go_corner_dwarf_at_cond_stack={k: v for k, v in go_corner.items()},
    go_corner_sw_needed=sw_needed(S_COND),
    joint_on_wb_agent_ladder=sib_joint,
    shape_route=dict(r_knee_kAU=r_knee(A0C, GEXT_P), dlnr_dlna0=dlnr, amplification=amp,
                     required_knee_precision=TARGET / amp),
    wb_mass_sys=dict(coherent_frac=SIG_M_COH,
                     a0_sys_if_unabsorbed_MI=a0err(0.5 * SIG_M_COH * LEV[("MI", "canon")]["gamma"], "MI"),
                     a0_sys_if_unabsorbed_MG=a0err(0.5 * SIG_M_COH * LEV[("MG", "canon")]["gamma"], "MG"),
                     random_part_a0_sys=a0err(rand, "MI"),
                     status="absorbed by anchored-kappa nuisance, NOT absent; absorption is shape-dependent"),
    prescription_sys=dict(MI_vs_MG_lnfrac=presc_mimg, MI_band_1p05_1p10_lnfrac=presc_band,
                          a0_from_gamma1p139_MG=a_mg, a0_from_gamma1p139_MI=a_mi,
                          a0_from_gamma1p10_MI=a_up, a0_from_gamma1p05_MI=a_lo),
    sigma_wb_budgets={k: v for k, v in budgets.items()},
    sigma_wb_dr4_frozen=sig_wb_dr4, sigma_wb_infinite_N_floor=sig_wb_stat_floor,
    joint_grid={k: dict(sigma_dwarf=v["sigma_dwarf"], joint=v["joint"], sw_needed=v["sw_needed"])
                for k, v in JOINTTAB.items()},
    crossing=dict(sw_needed_at_best_sparc=need_best, sw_needed_at_floor=sw_needed(S_FLOOR_UG),
                  sw_needed_at_box_now=sw_needed(S_BOX),
                  required_sigma_gamma_MI=sg_req_mi, required_sigma_gamma_MG=sg_req_mg,
                  frozen_sigma_tot_dr4=SIG_TOT_DR4, frozen_sigma_sys_dr4=SIG_SYS_DR4,
                  shortfall_factor_vs_sigtot=SIG_TOT_DR4 / sg_req_mi,
                  shortfall_factor_vs_sigsys=SIG_SYS_DR4 / sg_req_mi),
    joint_at_dr4=dict(sigma_dwarf=S_FLOOR_UG, sigma_wb=sig_wb_dr4,
                      joint=joint(S_FLOOR_UG, sig_wb_dr4),
                      sigma_canon_vs_alt_dwarf_only=abs(math.log(A0A / A0C)) / S_FLOOR_UG,
                      sigma_canon_vs_alt_joint=abs(math.log(A0A / A0C)) / joint(S_FLOOR_UG, sig_wb_dr4)),
    joint_fully_repaired_wb=dict(sigma_wb=a0err(0.010, "MI"),
                                 joint=joint(S_FLOOR_UG, a0err(0.010, "MI"))),
    dr3_inversion={r: a0_from_gamma(G_DR3, GEXT_P, r) for r in ("MG", "MI")},
    contamination=dict(dgamma_dftriple=dgam_dftrip, required_delta_ftriple=dg_budget / dgam_dftrip,
                       frozen_sigma_sys_includes_contamination=False),
    verdict_headline="NO-GO as a wall-breaker, and STRUCTURALLY so: even a WB constraint with ZERO "
                     "systematics (prescription exact, g_ext exact, full 8-bin DR4 statistics) gives "
                     "sigma_WB = 9.99%, whose joint with the 10.90% dwarf floor is 7.37% -- still above "
                     "the 6.31% target. Adding a perfect WB channel does not break the Step-A wall. "
                     "The only crossing is a ~0.3-0.5 sigma TOP-UP on a dwarf constraint already "
                     "dragged to 6.78% by its own dedicated TRGB+M/L+HI campaign.",
    verdict="NO-GO as a wall-breaker. TODAY (DR3): no a0 constraint at all -- gamma=1.205+-0.035 sits "
            "in the frozen contamination-guard zone and inverts to a0 = 1.45-1.86x canonical, off the "
            "top of the contested band. WITH DR4 as frozen: sigma_WB(a0) = 19% (MG) / 24% (MI), floored "
            "at 14-18% even at N=infinity by the frozen sigma_sys=0.020, versus the ~7.5-7.7% required "
            "to push the 10.9-11.6% dwarf floor below the 6.31% target; the joint gains only +0.17 "
            "sigma (1.74 -> 1.90). Orthogonality of the systematics is REAL and the joint arithmetic is "
            "valid -- it is simply not the binding constraint. The binding constraints are (1) EFE "
            "saturation, which makes the WB asymptote an EXACT function of g_ext/a0 (a RATIO, never an "
            "amplitude; verified to machine precision), and (2) the framework's own MI-EFE target being "
            "a BAND 1.05-1.10 that inverts to a 63% a0 range, 3.3x the footing gap it must resolve. "
            "ONE CONDITIONAL GO CORNER: if the dwarf side is first dragged to its full external-prior "
            "stack (6.78% = 2.79 sigma), a WB constraint at <= 17.4% tops it over 3 sigma -- DR4 as "
            "frozen delivers 19% (MG) / 24% (MI), so that corner is a coin-flip on the EFE reading and "
            "vanishes entirely if the 1.05-1.10 band is carried. WB's banked role is unchanged: a test "
            "of the nu+EFE PRESCRIPTION, not a measurement of a0. Nothing here is closed.",
)
json.dump(out, open(os.path.join(HERE, "wb_dwarf_joint_a0_results.json"), "w"), indent=1, default=float)
print("\n[wb_dwarf_joint_a0_results.json written]")
print("EXIT 0: joint computed. Exit code is not a verdict.")
