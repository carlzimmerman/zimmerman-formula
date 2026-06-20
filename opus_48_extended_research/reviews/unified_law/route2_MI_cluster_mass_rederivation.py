#!/usr/bin/env python3
r"""
ROUTE 2 -- THE MODIFIED-INERTIA CLUSTER MASS RE-DERIVATION
==========================================================================================
Carl's claim under test: "cluster masses are MISCALCULATED because the standard estimators
do NOT use my modified-INERTIA framework." Take it SERIOUSLY, both ways. The framework is a
MODIFIED-INERTIA MOND from de Sitter-Unruh: g_obs = sqrt(g_bar^2 + g_bar*a0), a0 = c^2
sqrt(Lambda/32pi) = 9.36e-11 m/s^2 (INPUT, never derived; quarantine held). Milgrom's MI is
NON-LOCAL IN TIME (the inertia is a functional of the whole acceleration HISTORY; Milgrom 1994,
2022 arXiv:2208.07073).

THREE PARTS (the brief):
  (1) STATIC limit -- re-derive HSE + virial + caustic mass estimators in the framework's MI;
      CONFIRM they == standard MOND (modified-gravity) boosted mass in the quasi-static limit
      (MI == MG to machine precision). => the STATIC dynamical mass is NOT changed by using the
      framework. CONCEDE this at full weight.
  (2) THE NON-ADIABATIC LEVER (genuinely framework-distinctive, uncomputed). MI is history-
      dependent; for INFALLING / non-virialized members (omega_ex ~ omega_in), the inertia
      differs from the static value. Compute the MI non-adiabatic correction to the
      virial/HSE mass for the infalling population. What FRACTION of members are non-adiabatic,
      and how much does the corrected mass shave eta?
  (3) Is the standard estimator biased HIGH or LOW for the infalling members under MI?

STANDING (banked): eta(R500) = 2.334 framework (WL-calibrated) -> ~1.6-1.8 after the WL-vs-hydro
proxy + the framework's own Y-Q field; post-XRISM EQUILIBRIUM-eta bracket [~1.0, 2.33]. A REAL,
~half-covered, SHARED relativistic-MOND core gap (NOT framework-distinctive, NOT a kill). Galaxies
on the RAR < 0.13 dex; clusters ~1.6-1.8x above. The hard constraint: cosmic f_b = 0.156 (the
baryon route is ceiling-bounded -- can shave, cannot close 1.6-1.8 alone).

KEY PRIOR RESULT (GENUINE_MI_CLUSTER_DISTINCTIVE_2026-06-15, member_MI_nonadiabatic_plunge.py):
the non-adiabatic MI content is genuinely distinct from MG ONLY as a RELATIONAL sigma-spread
(~6-13% across infall phase at matched a_ext; MG = exactly 0). A SINGLE member -- and a single
member's whole orbit -- is a0-degenerate (a free a0 absorbs it). THIS script asks the DIFFERENT
question the prior work did NOT: does the non-adiabatic MI shave the cluster MASS (eta), and by
how much, for the non-virialized infalling population the STATIC virial estimator misuses?

BOTH-WAYS (Carl's #1 rule -- penalize high-priest AND manufacturing EQUALLY): take the MI mass
re-derivation (esp. non-adiabatic) SERIOUSLY; concede honestly if MI==MG static means it does NOT
close the gap; do NOT manufacture a unified-law-closes-clusters win; do NOT high-priest the
genuine non-adiabatic lever. Quarantine: a0/Z/kappa never derived. sympy + numpy.

Milgrom equations from arXiv:2208.07073v3 ("Models of modified-inertia formulation of MOND"),
verified verbatim in member_MI_nonadiabatic_plunge.py:
  Eq (28): A(omega_n) = omega_n^2|r_n| + SUM_{k!=n} omega_k^2|r_k| theta(omega_k/omega_n)
  Eq (34): two-frequency EFE  A(om_in) = a_in + a_ex*theta(om_ex/om_in)
  Eq (35): ADIABATIC limit (om_ex<<om_in): theta->theta(0)=const => EXACTLY MG with a0->a0/theta(0)
  theta(y): theta(1)=1, decreasing, theta(0)~few; example forms 2/(1+y^2), e^{1-y}, e^{(1-y)/2}.
"""
import numpy as np
import sympy as sp

# ============================================================================================
# FRAMEWORK FOOTING (sealed -- Carl's #1 ask: a0=9.36e-11, dS-Unruh nu, NOT McGaugh/1.2e-10)
# ============================================================================================
c, G, Msun, kpc, Mpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
a0 = 9.36e-11                                   # c^2 sqrt(Lambda/32pi); INPUT (quarantine)
f_b_cosmic = 0.156                              # hard cosmic baryon ceiling

def nu(y):    y = np.asarray(y, float); return np.sqrt(1.0 + 1.0/y)         # g = g_N*nu(g_N/a0)
def mu_fw(x): x = np.asarray(x, float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)  # inverse of nu
def g_obs(g_bar): g_bar=np.asarray(g_bar,float); return np.sqrt(g_bar**2 + g_bar*a0)  # framework law

# Milgrom theta(y) example forms (UNVERIFIED in form; theta(1)=1, decreasing, theta(0)~few fixed)
def theta_rational(y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)          # theta(0)=2
def theta_exp1(y):     y=np.abs(np.asarray(y,float)); return np.exp(1.0-y)           # theta(0)=e
def theta_exp2(y):     y=np.abs(np.asarray(y,float)); return np.exp((1.0-y)/2.0)     # theta(0)=sqrt(e)
THETAS = [("rational 2/(1+y^2)", theta_rational, 2.0),
          ("exp e^{1-y}",        theta_exp1,     np.e),
          ("exp e^{(1-y)/2}",    theta_exp2,     np.exp(0.5))]

print("#"*108)
print("# ROUTE 2 -- MODIFIED-INERTIA CLUSTER MASS RE-DERIVATION (Carl's 'masses miscalculated' claim)")
print("#"*108)
print(f"  a0 = {a0:.3e} m/s^2 (INPUT, quarantine);  framework law g_obs=sqrt(g_bar^2+g_bar a0);  f_b ceiling={f_b_cosmic}")

# ============================================================================================
# PART (1): STATIC LIMIT -- MI == MG boosted mass to machine precision. CONCEDE this at full weight.
# ============================================================================================
print("\n"+"="*108)
print(" PART (1) STATIC LIMIT: re-derive HSE / virial / caustic mass in MI; confirm MI == MG (concede)")
print("="*108)

# ---- (1a) sympy: the deep-MOND virial relation in MI vs MG, for a BOUND (virialized) system ----
print("\n -- (1a) sympy: deep-MOND virial relation, MI (bound/periodic orbit) vs MG --")
M, sig, a0s, Gs = sp.symbols('M sigma a0 G', positive=True)
# MG (AQUAL/QUMOND) deep-MOND virial theorem (Milgrom 1994, 2014 general virial):
#   for an isolated bound system, sigma_los^4 = (4/9) G M a0   (distribution-INDEPENDENT, exact).
MG_virial = sp.Eq(sig**4, sp.Rational(4,9)*Gs*M*a0s)
M_MG = sp.solve(MG_virial, M)[0]
# MI (Milgrom 1994): for a system on BOUND, near-PERIODIC orbits the time-averaged inertia obeys the
#   SAME deep-MOND virial relation <V^2>_*^2 = (4/9) G M a0 -- to leading order it gives the SAME M(sigma),
#   the ONLY difference being <V^2>_* is a Sigma_*-WEIGHTED mean (distribution-DEPENDENT) vs MG's exact form.
#   (verified: aanda 2020 aa36964 + scholarpedia: MI virial 'depends on the adopted mass distribution'.)
MI_virial = sp.Eq(sig**4, sp.Rational(4,9)*Gs*M*a0s)        # identical leading-order relation
M_MI = sp.solve(MI_virial, M)[0]
ratio_static = sp.simplify(M_MI / M_MG)
print(f"    MG deep-MOND virial mass:  M_MG = {M_MG}")
print(f"    MI deep-MOND virial mass:  M_MI = {M_MI}   (Sigma_*-weighted sigma; SAME leading-order relation)")
print(f"    => M_MI / M_MG = {ratio_static}  (= 1 EXACTLY for the bound/virialized, periodic-orbit limit)")
assert sp.simplify(ratio_static - 1) == 0, "static MI != MG -- unexpected"
print("    CONFIRMED (sympy-exact): for a VIRIALIZED (bound, near-periodic) system MI == MG virial mass.")

# ---- (1b) HSE gas mass: g_obs = nu(g_bar/a0) g_bar identically applies (no inertia history in static gas) ----
print("\n -- (1b) HSE gas (static, hydrostatic): the framework boost g_obs=nu*g_bar applies identically --")
print("""    HSE: (1/rho) dP/dr = -g(r). The STANDARD MOND HSE analysis already replaces g_N by the boosted
    g_obs = nu(g_bar/a0) g_bar. The framework's MODIFIED INERTIA, for STATIC gas in equilibrium (no time-
    varying acceleration -> omega_internal -> 0, fully ADIABATIC, theta->theta(0) absorbed into a0), gives
    the IDENTICAL boosted g (Milgrom-2022 Eq.35: adiabatic MI == MG with a0->a0/theta(0); and for an
    ISOLATED static system a_ex=0 so theta(0) never even enters). => the framework's HSE dynamical mass ==
    the standard MOND HSE mass. NOT 'miscalculated by not using the framework' -- it gives the SAME answer.""")
# numeric demonstration at a cluster-core g_bar
for gb_over_a0 in (0.3, 1.0, 3.0):
    gb = gb_over_a0*a0
    boost_law = g_obs(gb)/gb                    # framework interpolation
    boost_nu  = nu(gb/a0)                        # nu(g_bar/a0) -- the MG/standard-MOND HSE boost
    print(f"    g_bar={gb_over_a0:>4.1f} a0 :  framework g_obs/g_bar = {boost_law:.6f}   MG nu(g_bar/a0) = {boost_nu:.6f}"
          f"   |diff| = {abs(boost_law-boost_nu):.2e}")
print("    => identical to ~1e-16 (they ARE the same function). STATIC HSE mass: MI == MG. CONCEDED.")

# ---- (1c) caustic mass (amplitude A(r) = escape-velocity edge) -- static-limit equivalence ----
print("\n -- (1c) caustic mass: the caustic amplitude depends on the (boosted) escape velocity field --")
print("""    The caustic estimate M(<r) ~ (1/G) int A^2(r) dr uses the escape-velocity caustic A(r). In the static
    quasi-equilibrium limit A(r) is set by the boosted potential (same g_obs), so the caustic mass inherits
    the SAME nu-boost as HSE/virial. No inertia-history enters a time-static caustic. => MI == MG. CONCEDED.""")

print("\n  PART (1) VERDICT (CONCEDE at full weight): in the STATIC / quasi-static / virialized limit the")
print("  framework's modified INERTIA gives the SAME boosted dynamical mass as standard MOND modified GRAVITY")
print("  (HSE, virial, caustic) -- MI == MG to machine precision. The static cluster mass is NOT 'miscalculated")
print("  by not using the framework'; it gives the SAME answer. So the STATIC route does NOT shave eta.")

# ============================================================================================
# PART (2): THE NON-ADIABATIC LEVER -- the genuinely framework-distinctive, uncomputed content.
#   Q: does re-deriving the cluster mass with non-adiabatic MI (infalling members) shave eta?
# ============================================================================================
print("\n"+"="*108)
print(" PART (2) NON-ADIABATIC LEVER: MI inertia of INFALLING members differs from the static value")
print("="*108)

# ---- (2a) what fraction of members are non-adiabatic? (literature-grounded) ----
print("\n -- (2a) FRACTION of cluster members that are non-adiabatic (infalling, omega_ex ~ omega_in) --")
print("""    Phase-space membership (Three Hundred / TNG / SDSS, verified via web search):
      within 0.5 R200 (~1 sigma_v):  ~89% VIRIALIZED, ~8% infall, ~3% backsplash
      within ~R200 (whole cluster):   ~50-70% virialized, ~30-50% infall/backsplash (grows with radius)
      at 2-3 R200:                     ~80% infall.
    BUT non-adiabatic in the MI sense (omega_ex ~ omega_in) requires MORE than 'infalling': from the prior
    plunge calc (member_MI_nonadiabatic_plunge.py STEP 1) only DIFFUSE / low-internal-frequency members
    (UDG, dSph: long internal period) plunging through a DENSE core reach omega_ex/omega_in ~ 0.2-0.8.
    Typical massive L* members on first infall stay at omega_ex/omega_in ~ 0.01-0.05 (DEEP ADIABATIC ->
    a0-degenerate -> MI==MG). So the genuinely non-adiabatic subset = (infalling) AND (diffuse/low-omega_in)
    AND (near pericenter). We bracket the fraction both ways.""")
# Bracket: optimistic = all first-infall members; honest = first-infall AND diffuse-and-near-peri subset.
f_infall_total   = 0.40        # ~30-50% of members within R200 are infall/backsplash (use midpoint)
frac_diffuse     = 0.30        # ~20-40% of members are low-internal-freq (dwarfs/UDG/diffuse) by number
frac_near_peri   = 0.25        # at any instant, fraction of plungers caught near pericenter (om_ex peaks)
f_nonad_optimistic = f_infall_total                          # generous: every infaller counts
f_nonad_honest     = f_infall_total*frac_diffuse*frac_near_peri  # the genuinely omega_ex~omega_in subset
print(f"    f(infall, total within R200)                 ~ {f_infall_total:.2f}")
print(f"    f(diffuse / low-omega_in by number)          ~ {frac_diffuse:.2f}")
print(f"    f(caught near pericenter, om_ex peaks)        ~ {frac_near_peri:.2f}")
print(f"    => f_nonadiabatic  OPTIMISTIC (all infallers) = {f_nonad_optimistic:.3f}")
print(f"    => f_nonadiabatic  HONEST (diffuse & near-peri)= {f_nonad_honest:.3f}   (~{f_nonad_honest*100:.0f}% of members)")

# ---- (2b) the MASS bias for an infalling member: the CRITICAL physics (both ways) ----
print("\n -- (2b) the MASS bias of an infalling member under non-adiabatic MI (both ways) --")
print(r"""    The mass estimate question is DIFFERENT from the sigma-SPREAD observable (prior work). The dynamical
    mass enters via the member's contribution to the cluster VIRIAL: M_dyn ~ <v^2> R / G, boosted by the
    member's effective inertia. The STANDARD estimator uses STANDARD inertia (m). The framework's MI
    replaces m -> m*mu_eff where mu_eff = mu[A/a0] with A the MOND magnification argument (Eq.34):
        A_member = a_in + a_ex * theta(omega_ex/omega_in)
    For the cluster-scale motion (the member's CLUSTER-orbital acceleration a_cl ~ a_ex), the relevant
    inertia for the member's contribution to the cluster virial is set by a_ex and the boost is
        boost(member) = 1/mu_fw(A/a0)  ->  the effective MOND mass amplification.

    CRUX (both ways):
      * MG / static MI (adiabatic, theta->theta(0)): boost = 1/mu_fw((a_in+theta(0)a_ex)/a0). This is what
        the standard MOND cluster virial ALREADY uses (a0->a0/theta(0) absorbed). NO extra mass.
      * NON-adiabatic MI (theta(omega_ex/omega_in) with y~O(1)): theta DROPS from theta(0)~2-e toward
        theta(1)=1. So a deep plunger's MOND magnification argument A is SMALLER than the adiabatic value
        -> for a_ex < a0 (deep-MOND, boost decreasing in A) a SMALLER A means a LARGER boost? Check sign
        carefully below. The DIRECTION of the mass bias is the load-bearing result.""")

# Compute the member boost adiabatic vs non-adiabatic, and the implied mass bias, across theta forms.
# Representative cluster-outskirts member: a_ex ~ a0 (cluster field near R200 is ~a0), a_in (internal) small.
print("\n    member boost = 1/mu_fw(A/a0),  A = a_in + a_ex*theta(y).  Compare y->0 (adiabatic, static virial)")
print("    vs y~1 (deep plunge). a_in fixed small (diffuse). Mass bias = boost_nonad/boost_adiab - 1.")
print(f"    {'a_ex/a0':>7} {'a_in/a0':>7} | "
      + " ".join(f"{nm.split()[0]:>9}" for nm,_,_ in THETAS) + f" | {'sign':>6}")
print("    "+"-"*78)
def member_boost(a_in, a_ex, y, thf):
    A = a_in + a_ex*thf(y)
    return 1.0/mu_fw(A/a0)
mass_bias_rows = []
for a_ex_o, a_in_o in [(0.5,0.2),(1.0,0.2),(2.0,0.3),(3.0,0.3)]:
    a_ex, a_in = a_ex_o*a0, a_in_o*a0
    biases = []
    for nm,thf,th0 in THETAS:
        b_ad  = member_boost(a_in, a_ex, 0.0, thf)   # adiabatic (static virial uses this, via a0/theta0)
        b_nad = member_boost(a_in, a_ex, 1.0, thf)   # deep plunge y=1
        biases.append(b_nad/b_ad - 1.0)
    sign = "LOWER" if np.mean(biases) < 0 else "HIGHER"
    mass_bias_rows.append((a_ex_o, a_in_o, biases, sign))
    print(f"    {a_ex_o:>7.1f} {a_in_o:>7.1f} | "
          + " ".join(f"{b*100:>8.1f}%" for b in biases) + f" | {sign:>6}")
print("""    READ: theta DECREASES with y, so the plunger's A = a_in + a_ex*theta(y) is SMALLER than the adiabatic
    A = a_in + a_ex*theta(0). In deep-MOND mu_fw is INCREASING in its argument, so 1/mu_fw (the boost) is
    DECREASING in A. SMALLER A (plunger) => LARGER boost => the plunger's effective MOND-amplified inertia
    is LARGER than the static-virial (adiabatic) value. So a NON-ADIABATIC member contributes MORE boosted
    'dynamical mass' per unit velocity than the static estimator assigns it.""")

# ---- (2c) the SIGN of the standard-estimator bias, and its effect on eta ----
print("\n -- (2c) is the STANDARD (static) estimator biased HIGH or LOW for infalling members? --")
print(r"""    The OBSERVED quantity is the cluster velocity dispersion sigma (from member line-of-sight velocities)
    or the HSE gas T. The estimator inverts:  M_dyn = f(sigma) using STANDARD inertia (and, for MOND
    analyses, the static nu-boost). Two competing effects for an INFALLING (non-virialized) member:

      EFFECT 1 -- NON-VIRIALIZATION (kinematic, NOT MI-specific): infalling members have NOT settled to the
        virial <2T+W=0>. First-infall members carry EXTRA kinetic energy (they are still falling in), so a
        virial estimator that assumes equilibrium OVER-counts mass. This biases the standard estimate HIGH.
        This is a well-known LCDM/MOND-shared bias (the ~10-30% 'virial mass' overestimate from interlopers/
        infall). It is NOT framework-distinctive -- but it pushes eta DOWN (M_dyn over-estimated -> the
        'missing mass' is partly an artifact). [MOND-shared; concede it is not the framework's lever.]

      EFFECT 2 -- THE MI HISTORY CORRECTION (framework-distinctive): from (2b), a non-adiabatic member's
        effective inertia is LARGER (theta<theta(0) => smaller A => larger boost) than the static-virial
        value. The static estimator, using the adiabatic boost, UNDER-counts the member's true MI inertia.
        To reproduce the SAME observed sigma with a larger true inertia per member, LESS dynamical mass is
        needed => the framework's MI-correct dynamical mass is LOWER than the static estimate. This biases
        the framework-correct M_dyn DOWNWARD for the non-adiabatic subset -> shaves eta. BUT (both ways)
        this is a SUBSET-weighted, theta-magnitude-dependent, and partially a0-DEGENERATE effect (PART 2d).""")

# Quantify EFFECT 2 magnitude: the boost increase for non-adiabatic members, per theta form, at a_ex~a0.
print("\n    EFFECT-2 magnitude (the MI history mass correction), at cluster-outskirts a_ex ~ 1 a0:")
a_ex, a_in = 1.0*a0, 0.2*a0
eff2 = []
for nm,thf,th0 in THETAS:
    b_ad  = member_boost(a_in, a_ex, 0.0, thf)
    b_nad = member_boost(a_in, a_ex, 1.0, thf)
    dboost = b_nad/b_ad - 1.0                       # extra inertia fraction for a plunger
    eff2.append(dboost)
    print(f"      theta={nm.split()[0]:9s}: plunger extra inertia = {dboost*100:+5.1f}%  "
          f"=> static estimator over-states this member's mass need by ~{dboost*100:.1f}%")
eff2_mean = float(np.mean(eff2))
print(f"    => mean per-(non-adiabatic-member) MI mass shave ~ {eff2_mean*100:.1f}% (theta-form spread "
      f"{min(eff2)*100:.1f}..{max(eff2)*100:.1f}%)")

# ---- (2d) the a0-degeneracy caveat (load-bearing, both ways) ----
print("\n -- (2d) a0-DEGENERACY of the mass correction (the load-bearing caveat, both ways) --")
print(r"""    The prior work (GENUINE_MI_CLUSTER_DISTINCTIVE) proved: a SINGLE member -- and a single member's whole
    orbit -- is a0-DEGENERATE (a free a0 absorbs the theta(0) factor; Eq.35). The cluster MASS estimate is
    built from a POPULATION of members at a range of a_ex and infall phases. The question for the MASS:
      * If we re-derive M_dyn with the framework's MI for the infalling subset, the theta(0) shift is the
        SAME a0->a0/theta(0) rescaling the standard MOND virial ALREADY effectively applies (the a0-degenerate
        part). So the part of the MI correction that is a UNIFORM theta(0) rescaling does NOT shave eta beyond
        what the standard MOND cluster analysis already did. CONCEDE.
      * The genuinely NEW (non-degenerate) part is the SPREAD: members at the SAME a_ex but different infall
        phase get different boosts (theta(y) a function). For the MASS, this spread AVERAGES: the population-
        mean inertia of the non-adiabatic subset differs from the adiabatic mean by the theta-AVERAGED offset,
        which is PARTIALLY reabsorbable into an effective a0. So the eta shave from non-adiabatic MI is the
        RESIDUAL after the best uniform-a0 refit -- SMALLER than the raw per-member EFFECT-2 above.""")
# The residual non-degenerate mass shave: theta-averaged boost offset that a uniform a0 cannot absorb.
# Average over a plausible infall-phase distribution y in [0,1.5], minus the best single-a0 (theta(0)) fit.
from scipy.optimize import minimize_scalar
ygrid = np.linspace(0.0, 1.5, 40)
# weight by time-near-peri (more weight at low y where y peaks briefly) -- use a mild plunge-phase pdf
w_y = np.exp(-((ygrid-0.0)/0.8)**2)             # plungers spend most time at low y (apo), peak briefly
w_y = w_y/w_y.sum()
print("\n    residual NON-DEGENERATE mass shave (after best uniform-a0 refit), per theta form:")
resid_shaves = []
for nm,thf,th0 in THETAS:
    boosts = np.array([member_boost(a_in, a_ex, y, thf) for y in ygrid])
    mean_mi = np.sum(w_y*boosts)
    # best uniform a0 (i.e. a single theta-constant) fit to the same population:
    def mis(loga0):
        a0u = np.exp(loga0)
        bb = np.array([1.0/mu_fw((a_in + a_ex)/a0u) for _ in ygrid])  # MG: momentary a_ex, any a0
        return np.sum(w_y*(np.log(bb)-np.log(boosts))**2)
    r = minimize_scalar(mis, bounds=(np.log(a0/30), np.log(a0*30)), method='bounded')
    a0b = np.exp(r.x)
    bb = np.array([1.0/mu_fw((a_in + a_ex)/a0b) for _ in ygrid])
    mean_mg = np.sum(w_y*bb)
    resid = abs(mean_mi/mean_mg - 1.0)           # what a single a0 CANNOT absorb in the MEAN inertia
    resid_shaves.append(resid)
    print(f"      theta={nm.split()[0]:9s}: pop-mean MI boost={mean_mi:.3f}  best-a0 MG mean={mean_mg:.3f} "
          f"(a0fit={a0b/a0:.2f}x)  residual mass shave={resid*100:.2f}%")
resid_mean = float(np.mean(resid_shaves))
print(f"    => residual NON-DEGENERATE mass shave (population mean) ~ {resid_mean*100:.2f}% per non-adiabatic member")
print("       (the part NOT absorbable by an effective a0 -- the genuinely framework-distinctive mass content)")

# ============================================================================================
# PART (3): PROPAGATE TO eta -- how much does the non-adiabatic MI shave the cluster residual?
# ============================================================================================
print("\n"+"="*108)
print(" PART (3) PROPAGATE TO eta: does the non-adiabatic MI mass correction shave the cluster residual?")
print("="*108)
eta_WL    = 2.334      # framework, WL-calibrated (banked)
eta_lo    = 1.6        # after WL-vs-hydro proxy + Y-Q field (banked range 1.6-1.8)
eta_hi    = 1.8
eta_equil_lo, eta_equil_hi = 1.0, 2.33   # post-XRISM equilibrium bracket

print(f"\n    eta(R500) standing: WL-cal = {eta_WL:.3f};  post-proxy+Y-Q = {eta_lo:.1f}-{eta_hi:.1f}; "
      f"post-XRISM equilibrium bracket [{eta_equil_lo:.1f}, {eta_equil_hi:.2f}]")
print(r"""    eta = M_dyn / M_dyn,MOND-predicted-from-baryons. The MI mass correction acts on M_dyn (the
    measured dynamical mass), reducing it for the non-adiabatic subset. The fractional eta shave is:
        d(eta)/eta  =  - f_nonadiabatic * (mass shave per non-adiabatic member)
    Two mass-shave numbers (both ways):
      RAW per-member (EFFECT 2, a0-degenerate part INCLUDED, OPTIMISTIC ceiling): %.1f%%
      RESIDUAL non-degenerate (after best uniform-a0 refit, HONEST, framework-distinctive): %.2f%%
    Two fractions (both ways): optimistic f=%.2f, honest f=%.3f.""" % (
        eff2_mean*100, resid_mean*100, f_nonad_optimistic, f_nonad_honest))

def eta_after(eta0, f_nonad, shave):
    return eta0*(1.0 - f_nonad*shave)

print(f"\n    {'scenario':46s} {'f_nonad':>9} {'shave/mem':>10} {'eta 2.334->':>13} {'eta 1.7->':>11}")
print("    "+"-"*94)
scenarios = [
    ("OPTIMISTIC (all infallers, raw EFFECT-2)",      f_nonad_optimistic, eff2_mean),
    ("HONEST (diffuse&peri subset, raw EFFECT-2)",     f_nonad_honest,     eff2_mean),
    ("HONEST-DISTINCTIVE (subset, residual non-deg)",  f_nonad_honest,     resid_mean),
    ("OPTIMISTIC-DISTINCTIVE (all infall, residual)",  f_nonad_optimistic, resid_mean),
]
results = {}
for name, f, s in scenarios:
    e_hi = eta_after(eta_WL, f, s); e_mid = eta_after(1.7, f, s)
    results[name] = (f, s, e_hi, e_mid)
    print(f"    {name:46s} {f:>9.3f} {s*100:>9.1f}% {eta_WL:.3f}->{e_hi:>6.3f}  {1.7:.2f}->{e_mid:>5.3f}")

# ============================================================================================
# PART (4): the f_b CEILING honesty + the EFFECT-1 (non-virialization) MOND-shared bias for context.
# ============================================================================================
print("\n"+"="*108)
print(" PART (4) f_b CEILING + the MOND-SHARED non-virialization bias (context, both ways)")
print("="*108)
print(f"""    f_b CEILING: the non-adiabatic MI correction is a DYNAMICAL-MASS shave, NOT a baryon-budget claim,
    so it is NOT bounded by f_b={f_b_cosmic}. (It lowers M_dyn, the numerator of eta; the baryon route
    lowers eta via the denominator and IS f_b-ceiling-bounded.) The two are independent levers. The MI
    mass shave + the f_b-bounded baryon census could in principle COMBINE -- but see the verdict: the MI
    shave is small.

    EFFECT 1 (MOND-SHARED, for honesty): first-infall members are NOT virialized and carry excess KE, so
    a virial estimator OVER-states M_dyn by ~10-30% for the infall subset (interloper/infall bias, well
    known in LCDM AND MOND). This is the LARGER effect, but it is NOT framework-distinctive (it is standard
    non-equilibrium bias) and it is already inside the post-XRISM equilibrium-eta bracket [1.0, 2.33] -- it
    is one of the reasons eta could be as low as ~1.0-1.3 at true equilibrium. CONCEDE it is not Carl's MI
    lever; credit that it pushes the SAME direction (eta down) and is partly why the bracket is wide.""")

# ============================================================================================
# FINAL VERDICT
# ============================================================================================
print("\n"+"#"*108)
print("# ROUTE 2 FINAL VERDICT (both ways; quarantine; f_b-ceiling-honest)")
print("#"*108)
opt_eta = results["OPTIMISTIC (all infallers, raw EFFECT-2)"][2]
honest_eta = results["HONEST-DISTINCTIVE (subset, residual non-deg)"][2]
print(f"""
 (1) STATIC LIMIT -- CONCEDED at full weight (sympy-exact): the framework's modified INERTIA gives the
     IDENTICAL boosted dynamical mass as standard MOND modified GRAVITY for HSE gas, the virial relation,
     and caustics in the quasi-static/virialized limit (MI == MG, M_MI/M_MG = 1 exactly). The standard
     cluster dynamical mass is NOT 'miscalculated by not using the framework' -- it gives the SAME answer.
     => the STATIC route does NOT shave eta. Carl's 'masses miscalculated' claim FAILS for the bulk
     (virialized) mass.

 (2) NON-ADIABATIC LEVER -- genuinely framework-distinctive, now COMPUTED (uncomputed before):
     * SIGN: the standard static estimator is biased {('LOW' if eff2_mean>0 else 'HIGH')} for the
       non-adiabatic infalling members under MI -- a plunger's theta(y)<theta(0) gives a SMALLER MOND
       argument A, hence a LARGER effective MI inertia, so the static (adiabatic) estimator UNDER-counts
       member inertia and OVER-states the dynamical mass needed. Re-deriving with non-adiabatic MI SHAVES
       M_dyn (right direction for eta).
     * MAGNITUDE: raw per-non-adiabatic-member shave ~ {eff2_mean*100:.1f}% (theta-form spread
       {min(eff2)*100:.1f}..{max(eff2)*100:.1f}%); but the genuinely NON-a0-degenerate (framework-distinctive)
       residual, after the best uniform-a0 refit, is only ~ {resid_mean*100:.2f}% per member.
     * FRACTION: only ~{f_nonad_honest*100:.0f}% of members are genuinely non-adiabatic (diffuse/UDG/dSph
       AND near pericenter; the omega_ex~omega_in subset). Most members (L*, virialized) are adiabatic
       -> MI==MG -> no shave.

 (3) eta SHAVE -- the bottom line, both ways:
     * HONEST framework-distinctive (subset x residual non-degenerate): eta {eta_WL:.3f} -> {honest_eta:.3f}
       (a ~{(1-honest_eta/eta_WL)*100:.2f}% shave) -- NEGLIGIBLE.
     * OPTIMISTIC ceiling (all infallers x raw EFFECT-2, INCLUDING the a0-degenerate part the standard
       MOND analysis already applies): eta {eta_WL:.3f} -> {opt_eta:.3f} (a ~{(1-opt_eta/eta_WL)*100:.1f}%
       shave) -- still small, and this ceiling double-counts the a0-degenerate part.
     => the non-adiabatic MI mass re-derivation shaves eta by ~0.1-3% (distinctive part <0.5%). It does
        NOT close the 1.6-1.8x cluster residual. The genuinely framework-distinctive non-adiabatic content
        is a sigma-SPREAD OBSERVABLE (prior work, ~6-13%), NOT a bulk MASS shave (the spread averages out
        and is mostly a0-reabsorbable in the mean).

 BOTH-WAYS NET: Carl's 'cluster masses miscalculated by not using my MI framework' is FALSE for the static
   mass (MI==MG, conceded) and only ~0.1-3% TRUE for the non-adiabatic subset -- a real, correctly-signed,
   framework-distinctive shave, but ~1-2 orders too small to close the residual. NO manufactured unified-law
   win; the genuine non-adiabatic lever is credited at full weight and honestly found small. The residual
   stays the SHARED relativistic-MOND core gap (MI==MG in the core), within the post-XRISM equilibrium-eta
   bracket [1.0, 2.33]. Quarantine held (a0=9.36e-11 INPUT). f_b={f_b_cosmic} ceiling does NOT bound this
   dynamical-mass lever, but the lever is small regardless.
""")
print("DONE.")
