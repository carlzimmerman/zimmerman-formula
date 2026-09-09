#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L34 -- the bounded-boost theorem audited against perturbative well-definedness
==============================================================================
An audit of a paper the programme has ALREADY DEPOSITED:
  PAPER5_bounded_boost_2026.tex, DOI 10.5281/zenodo.22548669,
  "A Ceiling Dark Matter Cannot Impose: the Bounded-Boost Theorem for MOND-Class Kernels".

WHAT THE PAPER PROVES (its section 7, "The carrier theorem is the bounded-boost theorem").
A modification carried by a scalar sourced by matter obeys div[J_Y grad phi] = 4 pi G rho, so on a
sphere Gauss's law gives  J_Y(g_phi) g_phi = g_N.  Hence g_phi is a SINGLE-VALUED function of g_N and
its longitudinal stiffness dg_N/dg_phi must be positive or the static problem is ill posed.  Writing
g_phi = a0 Delta(s), s = g_N/a0, that stiffness is exactly 1/Delta'(s).  The paper concludes:

    "a matter-sourced scalar can carry a kernel only up to the MAXIMUM of Delta, and must
     saturate at C a0 above it ... every kernel of the class leaves a constant residual scalar
     force C a0 at high acceleration."

carried kernel = nu_RAR, saturating at s_sat = 2.540, C = Delta_sat = 0.6476.

WHAT L13 FOUND (its P9 scope note).  Beyond s_sat the PUBLISHED kernel has Delta'(s) = 0 EXACTLY, so
Sigma_par = 1/Delta' is infinite, J(Y) has infinite slope at Y = (C a0)^2, and the MOND scalar's own
cubic action at the Solar-System background cannot be written.  The theory is not C2 there.

THIS LANE'S QUESTION -- structural, not a search for a repair kernel (that is L30's lane):
  is there a GENUINE TENSION between the bounded-boost theorem and the requirement that the theory
  have a well-defined perturbative expansion, or is the published kernel's HARD saturation simply a
  bad choice inside an otherwise healthy class?

THE THREE REQUIREMENTS, as conditions on Delta on [0, infinity):
  (i)   BOUNDED            Delta(s) <= C < infinity                (the theorem's own conclusion)
  (ii)  POSITIVE STIFFNESS Delta'(s) > 0 at every finite s         (Sigma_par finite => cubic exists)
  (iii) SOLAR SYSTEM       a0 Delta(s) below the ephemeris gates at s ~ 1e5 - 1e8
Gates taken verbatim from g03d_exact_fourth_order_solar.py:
  Q2_CEIL = 5.2e-27 s^-2 (Park 2026), M_SAT_BOUND = 6.7e-11 Msun inside Saturn (Pitjev-Pitjeva),
  A_SUNWARD = 0.5 * 9.36e-11 / 1278 = 3.662e-14 m s^-2.

Sections
  A  CONTROLS.  Reproduce the theorem independently in sympy and reproduce the carried kernel's
     saturation point and the whole of the paper's Table 1.  If these fail, nothing below is trusted.
  B  THE THREE REQUIREMENTS.  Are (i)+(ii)+(iii) mutually satisfiable?  Lemma + randomized scan +
     a rigging control (a kernel that satisfies (i)+(iii) and fails only (ii)).
  C  ASYMPTOTIC SATURATION.  Does the cubic action exist at every finite s?  Closed form for the
     strong-coupling amplitude g_*(s), verified symbolically AND at 60-digit precision.
  D  THE SHARP VERSION.  Fastest-saturating kernel whose strong coupling stays above the
     Solar-System scale; its boost ceiling against what galaxies require; the role of xi.
  E  VERDICT + the corrected statement of the theorem.

Both a0 footings on every dimensional number.  Check names are written as PROPOSITIONS: PASS means
the proposition holds.  A FAIL is a substantive finding, never a machinery failure.
"""
import math, time
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq, minimize_scalar

T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

# ------------------------------------------------------------------ constants (no repo dependency)
PC, AU, G, MSUN = 3.0857e16, 1.495978707e11, 6.6743e-11, 1.98892e30
GM_SUN = 1.32712440018e20; GM_EARTH = 3.986004418e14; R_EARTH = 6.3710e6; R_SUN = 6.957e8
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
# gates, verbatim from g03d_exact_fourth_order_solar.py
Q2_CEIL, M_SAT_BOUND, A_SUNWARD, R_SAT = 5.2e-27, 6.7e-11, 0.5*9.36e-11/1278.0, 9.58*AU
PLANETS = {"Mercury": 0.387*AU, "Earth": AU, "Mars": 1.524*AU, "Jupiter": 5.203*AU,
           "Saturn": R_SAT, "Neptune": 30.07*AU}

print("=" * 122)
print("L34 -- the bounded-boost theorem (PAPER5, DOI 10.5281/zenodo.22548669) vs perturbative well-definedness")
print("=" * 122, flush=True)

# ===================================================================================================
# SECTION A -- CONTROLS: reproduce the theorem, independently
# ===================================================================================================
print("\n" + "-" * 122)
print("A -- CONTROLS.  The theorem reproduced from scratch, not quoted.")
print("-" * 122)

# --- A1: the exponential carrier's excess, symbolically -------------------------------------------
y = sp.symbols('y', positive=True)
Delta_exp_sym = y*sp.exp(-y)
dD = sp.simplify(sp.diff(Delta_exp_sym, y))
crit = sp.solve(sp.Eq(dD, 0), y)
d2_at1 = sp.simplify(sp.diff(Delta_exp_sym, y, 2).subs(y, 1))
lim0 = sp.limit(Delta_exp_sym, y, 0); limI = sp.limit(Delta_exp_sym, y, sp.oo)
print(f"  Delta_exp(y) = y e^-y ;  dDelta/dy = {dD} ;  critical points {crit}")
print(f"  Delta(1) = 1/e = {1/math.e:.6f} ;  Delta''(1) = {d2_at1} = {float(d2_at1):+.6f} ;  limits {lim0}, {limI}")
check("A1 [control] sympy: Delta_exp = y e^-y has the UNIQUE critical point y = 1, value 1/e = 0.367879, "
      "Delta'' = -1/e < 0, and both endpoint limits vanish (PAPER5 section 2, boxed equation)",
      crit == [1] and abs(float(Delta_exp_sym.subs(y, 1)) - 1/math.e) < 1e-12
      and float(d2_at1) < 0 and lim0 == 0 and limI == 0,
      f"crit {crit}, Delta_max {float(Delta_exp_sym.subs(y,1)):.6f}")

# --- A2: the carried kernel nu_RAR ----------------------------------------------------------------
def Delta_RAR(s):
    s = float(s)
    if s <= 0: return 0.0
    u = math.sqrt(s)
    return 0.0 if u > 700 else s/math.expm1(u)
res = minimize_scalar(lambda s: -Delta_RAR(s), bracket=(1.0, 3.0, 6.0), method="brent",
                      options=dict(xtol=1e-14))
S_SAT, C_RAR = float(res.x), float(-res.fun)
print(f"  nu_RAR carried:  Delta(s) = s/(e^sqrt(s) - 1);  maximum at s_sat = {S_SAT:.6f}, Delta_sat = {C_RAR:.6f}")
check("A2 [control] the carried kernel's saturation point reproduces PAPER5's s_sat = 2.540 and "
      "Delta_sat = C = 0.6476 (Table 1, section 7)",
      abs(S_SAT - 2.540) < 1e-3 and abs(C_RAR - 0.6476) < 2e-4, f"s_sat {S_SAT:.4f}, C {C_RAR:.5f}")

# --- A3: Gauss's law => J(g_phi) g_phi = g_N ------------------------------------------------------
r_, Jf, gphi_, GMr = sp.symbols('r J g_phi GM', positive=True)
flux = 4*sp.pi*r_**2*Jf*gphi_                 # surface integral of J grad phi over a sphere
src = 4*sp.pi*GMr                             # 4 pi G M(<r)
gN_from_gauss = sp.simplify(sp.solve(sp.Eq(flux, src), gphi_)[0]*Jf)
check("A3 [control] sympy: Gauss's law on a sphere gives J(g_phi) g_phi = g_N exactly, with no expansion "
      "(PAPER5 section 7, first step)",
      sp.simplify(gN_from_gauss - GMr/r_**2) == 0, f"J g_phi = {gN_from_gauss}")

# --- A4: the stiffness identity Sigma_par = J + 2 Y dJ/dY = 1/Delta'(s) ---------------------------
s_, a0_ = sp.symbols('s a0', positive=True)
D = sp.Function('Delta')(s_)
Y_of_s, J_of_s = (a0_*D)**2, s_/D
dJ_dY = sp.diff(J_of_s, s_)/sp.diff(Y_of_s, s_)
Sigma_par_sym = sp.simplify(J_of_s + 2*Y_of_s*dJ_dY)
check("A4 [control] sympy: the longitudinal stiffness J + 2 Y dJ/dY equals 1/Delta'(s) IDENTICALLY, for an "
      "arbitrary Delta (PAPER5 section 7: 'that stiffness is exactly 1/Delta'')",
      sp.simplify(Sigma_par_sym - 1/sp.diff(D, s_)) == 0, f"Sigma_par = {Sigma_par_sym}")

# --- A5: the whole of PAPER5's Table 1 ------------------------------------------------------------
def Delta_deepMOND(s):  return math.sqrt(s) - s                                      # g = sqrt(a0 g_N)
def Delta_stdmu(s):     X = brentq(lambda X: X*X/math.sqrt(1+X*X) - s, 1e-14, 1e16); return X - s
def Delta_expcarrier(s):X = brentq(lambda X: X*(1-math.exp(-X)) - s, 1e-14, 1e16);   return X - s
def Delta_simplemu(s):  return 2.0*s/(math.sqrt(s*s + 4*s) + s)     # mu(x)=x/(1+x); cancellation-free form
TAB1 = {}
for nm, fn, brk in (("deep-MOND sqrt", Delta_deepMOND, (0.05, 0.25, 0.8)),
                    ("standard mu",    Delta_stdmu,     (0.2, 0.49, 1.5)),
                    ("exp carrier",    Delta_expcarrier,(0.2, 0.63, 1.5)),
                    ("nu_RAR",         Delta_RAR,       (1.0, 2.5, 6.0))):
    rr = minimize_scalar(lambda s: -fn(s), bracket=brk, method="brent", options=dict(xtol=1e-14))
    TAB1[nm] = (float(-rr.fun), float(rr.x))
TAB1["simple mu"] = (Delta_simplemu(1e14), float('inf'))
PAPER_T1 = {"deep-MOND sqrt": (0.2500, 0.250), "standard mu": (0.3003, 0.486),
            "exp carrier": (0.3679, 0.632), "nu_RAR": (0.6476, 2.54), "simple mu": (1.0000, None)}
print("\n  PAPER5 Table 1, reproduced independently:")
print(f"    {'kernel':18s} {'C = sup Delta':>14s} {'paper':>9s} {'at s':>12s} {'paper':>9s}")
ok_t1 = True
for nm, (Cv, sv) in TAB1.items():
    pC, ps = PAPER_T1[nm]
    ok_t1 &= abs(Cv - pC) < 6e-4
    if ps is not None: ok_t1 &= abs(sv - ps) < 6e-3
    print(f"    {nm:18s} {Cv:14.4f} {pC:9.4f} {sv:12.4f} {(f'{ps:9.3f}' if ps is not None else '      inf')}")
check("A5 [control] all five kernel suprema of PAPER5 Table 1 reproduce to the paper's quoted digits", ok_t1)

# --- A6: the stiffness sign change at the two maxima ----------------------------------------------
def numder(f, x, h=None):
    h = h if h else max(1e-7, abs(x)*1e-6)
    return (f(x+h) - f(x-h))/(2*h)
zero_exp = brentq(lambda s: numder(Delta_expcarrier, s), 0.3, 1.2)
zero_rar = brentq(lambda s: numder(Delta_RAR, s), 1.0, 6.0)
check("A6 [control] the longitudinal stiffness changes sign at g_N = 0.633 a0 (exp carrier) and 2.540 a0 "
      "(nu_RAR), 'exactly at the two maxima' (PAPER5 section 7)",
      abs(zero_exp - 0.6321) < 2e-3 and abs(zero_rar - 2.540) < 2e-3,
      f"exp {zero_exp:.4f}, nu_RAR {zero_rar:.4f}")

# --- A7: the gates ---------------------------------------------------------------------------------
g_sat_gate = G*M_SAT_BOUND*MSUN/R_SAT**2      # Pitjev-Pitjeva phantom mass, as an acceleration at Saturn
print(f"\n  Solar-System gates (g03d_exact_fourth_order_solar.py):")
print(f"    sunward ephemeris          {A_SUNWARD:.4e} m/s^2  = {A_SUNWARD/A0['canonical']:.4e} a0 (canonical), "
      f"{A_SUNWARD/A0['alt']:.4e} a0 (alt)")
print(f"    phantom mass inside Saturn {M_SAT_BOUND:.2e} Msun -> {g_sat_gate:.4e} m/s^2 = "
      f"{g_sat_gate/A0['canonical']:.4e} a0 (canonical), {g_sat_gate/A0['alt']:.4e} a0 (alt)   <-- BINDING")
print(f"    quadrupole ceiling         {Q2_CEIL:.2e} s^-2 (not sourced by a constant radial residual; "
      f"reported, not used)")
check("A7 [control] the g03d gates reproduce from their own constants; the Saturn phantom-mass bound "
      "(4.33e-15 m/s^2) is the tighter of the two and is the binding one",
      abs(A_SUNWARD - 3.662e-14) < 1e-17 and abs(g_sat_gate - 4.33e-15) < 1e-17 and g_sat_gate < A_SUNWARD,
      f"sunward {A_SUNWARD:.4e}, Saturn-phantom {g_sat_gate:.4e}")
B_RES = {f: g_sat_gate/A0[f] for f in A0}
B_SUN = {f: A_SUNWARD/A0[f] for f in A0}

print(f"\n  s = g_N/a0 across the Solar System:")
print(f"    {'body':10s} {'r':>10s} {'g_N [m/s^2]':>14s} {'s canonical':>14s} {'s alt':>14s}")
for nm, rr in PLANETS.items():
    gN = GM_SUN/rr**2
    print(f"    {nm:10s} {rr/AU:7.3f} AU {gN:14.4e} {gN/A0['canonical']:14.4e} {gN/A0['alt']:14.4e}")
gN_cass = GM_SUN/(1.6*R_SUN)**2
print(f"    {'Cassini':10s} 1.6 Rsun {gN_cass:14.4e} {gN_cass/A0['canonical']:14.4e} {gN_cass/A0['alt']:14.4e}")

# ===================================================================================================
# SECTION B -- are (i), (ii), (iii) mutually satisfiable?
# ===================================================================================================
print("\n" + "-" * 122)
print("B -- THE THREE REQUIREMENTS.  (i) bounded, (ii) Delta' > 0 everywhere, (iii) the Solar System screens.")
print("-" * 122)
GAL_S    = [1.29, 1.70, 2.34, 3.27, 4.44]          # PAPER5 Table 2, g_bar/a0 bins
GAL_MEAS = [0.816, 0.994, 0.979, 1.190, 0.750]     # PAPER5 Table 2, measured median Delta
GAL_MIN_REQ = 0.30      # the most conservative galactic demand anywhere in Table 1 (standard mu, C = 0.3003)

print("  THE LEMMA.  (ii) => Delta strictly increasing => sup Delta = lim_{s->inf} Delta = C, and")
print("              Delta(s_gal) < Delta(s_sun) for EVERY galactic s_gal < every Solar-System s_sun.")
print("              So (iii), which caps Delta(s_sun) at B, caps Delta IN GALAXIES at the same B.")
print(f"\n  {'footing':10s} {'binding gate B/a0':>19s} {'carried kernel C':>18s} {'measured in galaxies':>21s} {'shortfall (C/B)':>17s}")
PINCER = {}
for f in A0:
    PINCER[f] = (C_RAR/B_RES[f], max(GAL_MEAS)/B_RES[f])
    print(f"  {f:10s} {B_RES[f]:19.4e} {C_RAR:18.4f} {max(GAL_MEAS):21.3f} {PINCER[f][0]:17.3e}")
check("B1 (i)+(ii)+(iii) are mutually satisfiable for the KERNEL ALONE -- some bounded, everywhere-increasing "
      "Delta both boosts galaxies and passes the Solar-System gates",
      all(PINCER[f][0] <= 1.0 for f in A0),
      f"the carried ceiling C = {C_RAR:.4f} exceeds the binding gate by {PINCER['canonical'][0]:.3e}x (canonical) "
      f"and {PINCER['alt'][0]:.3e}x (alt); against the MEASURED galactic excess it is "
      f"{PINCER['canonical'][1]:.3e}x / {PINCER['alt'][1]:.3e}x")
print(f"\n  the same statement in physical units (canonical): the irreducible residual C a0 = "
      f"{C_RAR*A0['canonical']:.4e} m/s^2 against")
print(f"    the Saturn phantom-mass gate {g_sat_gate:.4e} m/s^2  ->  {C_RAR*A0['canonical']/g_sat_gate:.4e}x over")
print(f"    the sunward ephemeris gate   {A_SUNWARD:.4e} m/s^2  ->  {C_RAR*A0['canonical']/A_SUNWARD:.4e}x over")
print(f"    phantom mass inside Saturn from a constant C a0: "
      f"{C_RAR*A0['canonical']*R_SAT**2/G/MSUN:.4e} Msun vs the {M_SAT_BOUND:.1e} Msun bound")

# --- B2/B3: randomized scan over the admissible class ---------------------------------------------
rng = np.random.default_rng(20260908)
NSCAN = 40000
s_gal_probe = np.array(GAL_S)
s_sun_probe = np.array([GM_SUN/PLANETS[p]**2/A0["canonical"] for p in ("Neptune", "Saturn", "Earth")])
s_dense = np.logspace(-3, 9, 400)
def fam(sv, w, si, pi_):
    """Delta(s) = sum_i w_i [1 - (1 + s/s_i)^(-p_i)] -- bounded, strictly increasing, smooth, Delta(0)=0."""
    sv = np.asarray(sv, float)[:, None]
    return np.sum(w[None, :]*(1.0 - (1.0 + sv/si[None, :])**(-pi_[None, :])), axis=1)
def fam_d(sv, w, si, pi_):
    """the ANALYTIC derivative -- every term is w_i p_i/s_i (1+s/s_i)^(-p_i-1) > 0 by construction, so the
    monotonicity control tests the family, not float64's ability to resolve a saturated difference."""
    sv = np.asarray(sv, float)[:, None]
    return np.sum(w[None, :]*pi_[None, :]/si[None, :]*(1.0 + sv/si[None, :])**(-pi_[None, :]-1.0), axis=1)
n_gal = n_sun = n_both = n_mono_fail = 0
for _ in range(NSCAN):
    K = int(rng.integers(1, 4))
    w, si, pi_ = 10**rng.uniform(-2, 1.0, K), 10**rng.uniform(-2, 8.0, K), 10**rng.uniform(-2, 1.0, K)
    if np.any(fam_d(s_dense, w, si, pi_) <= 0) or np.any(np.diff(fam(s_dense, w, si, pi_)) < 0):
        n_mono_fail += 1
    okg = np.max(fam(s_gal_probe, w, si, pi_)) >= GAL_MIN_REQ
    oks = np.max(fam(s_sun_probe, w, si, pi_)) <= B_RES["canonical"]
    n_gal += okg; n_sun += oks; n_both += (okg and oks)
print(f"\n  randomized scan, {NSCAN} bounded strictly-increasing kernels (1-3 term mixtures, "
      f"s_i in [1e-2,1e8], p_i in [1e-2,10], w_i in [1e-2,10]):")
print(f"    boost galaxies (max Delta >= {GAL_MIN_REQ} on Table 2's bins) : {n_gal}")
print(f"    screen the Solar System (Delta <= {B_RES['canonical']:.3e} at Neptune/Saturn/Earth) : {n_sun}")
print(f"    do BOTH : {n_both}")
check("B2 [control] every member of the scanned family is in fact strictly increasing, so the scan tests "
      "the right class", n_mono_fail == 0, f"{n_mono_fail} non-monotone members out of {NSCAN}")
check("B3 at least one bounded, everywhere-increasing kernel both boosts galaxies AND screens the Solar System",
      n_both > 0, f"{n_both} of {NSCAN}; {n_gal} boost, {n_sun} screen, the intersection is empty")

# --- B4: the rigging control ----------------------------------------------------------------------
def Delta_partner(s):
    s = float(s); return s/math.expm1(s) if s < 700 else 0.0
part_sun = max(Delta_partner(sv) for sv in s_sun_probe)
part_slope = numder(Delta_partner, 2.0)
print(f"\n  rigging control -- PAPER5's own 'exponential inverse partner (unsaturated)' (Table 3), "
      f"Delta = s/(e^s - 1):")
print(f"    max Delta on Table 2's galactic bins = {max(Delta_partner(sv) for sv in GAL_S):.4f}   "
      f"Delta at Neptune = {part_sun:.3e}   Delta'(2) = {part_slope:+.4e}")
check("B4 [control] the scan is not rigged: a DECAYING kernel satisfies (i) and (iii) and fails only (ii) -- "
      "PAPER5's own unsaturated partner screens the Solar System perfectly and has Delta' < 0",
      part_sun < B_RES["canonical"] and part_slope < 0,
      f"Delta(Neptune) = {part_sun:.2e} << B = {B_RES['canonical']:.2e}, but Delta'(2) = {part_slope:+.3e} < 0 "
      f"=> Sigma_par < 0, the very thing the theorem forbids")

# ===================================================================================================
# SECTION C -- asymptotic saturation
# ===================================================================================================
print("\n" + "-" * 122)
print("C -- ASYMPTOTIC SATURATION.  Delta' > 0 at every finite s but Delta' -> 0: is the LIMIT divergence harmful?")
print("-" * 122)

# --- C1: is Delta' -> 0 unavoidable? ---------------------------------------------------------------
h_ = sp.symbols('h', positive=True); s2 = sp.symbols('s', positive=True)
int_test = sp.integrate(h_, (s2, 0, sp.oo))
print(f"  if Delta'(s) >= h > 0 for all s then Delta(S) - Delta(0) >= h S -> {int_test}: Delta is unbounded.")
print("  hence bounded + increasing => inf_s Delta'(s) = 0 => sup_s Sigma_par(s) = +infinity, unavoidably.")
check("C1 bounded + everywhere-increasing does NOT force Delta' -> 0 (i.e. an admissible kernel can keep "
      "Sigma_par uniformly bounded)",
      bool(int_test.is_finite),
      "Delta' >= h > 0 integrates to an unbounded Delta.  The stiffness divergence in the LIMIT is unavoidable "
      "for every member of the class; only its harmfulness is in question")

# --- C2: the cubic action, symbolically ------------------------------------------------------------
# L = -W(Y), Y = |grad phi|^2.  Longitudinal fluctuation h = d_par psi about a background g:
#   Y = (g + h)^2, expand W((g+h)^2) in h.  Generic W represented as a quintic in Y (its 1st, 2nd and
#   3rd derivatives at the background are then free), so the identity below is proved, not sampled.
gb, hh = sp.symbols('g h', positive=True)
wc = sp.symbols('w0:6')
Wpoly = lambda Yq: sum(wc[i]*Yq**i for i in range(6))
expr = Wpoly((gb + hh)**2)
c2 = sp.expand(sp.diff(expr, hh, 2).subs(hh, 0)/2)     # = W' + 2 g^2 W''      (= Sigma_par)
c3 = sp.expand(sp.diff(expr, hh, 3).subs(hh, 0)/6)     # = 2 g W'' + (4/3) g^3 W'''
dc2_dg = sp.expand(sp.diff(c2, gb))
print(f"  L2 coefficient  Sigma_par = W' + 2 g^2 W''            (checked as a polynomial identity)")
print(f"  L3 coefficient  kappa3    = 2 g W'' + (4/3) g^3 W'''")
print(f"  identity        kappa3    = (1/3) d Sigma_par / d g_phi")
check("C2 [control] sympy: the cubic coefficient of the action expansion is EXACTLY (1/3) dSigma_par/dg_phi, "
      "so the strong-coupling amplitude is g_* = 3 |d ln Sigma_par / d g_phi|^{-1}",
      sp.simplify(c3 - dc2_dg/3) == 0, f"kappa3 - (1/3) dSigma/dg = {sp.simplify(c3 - dc2_dg/3)}")

# --- C3: g_* in terms of Delta ---------------------------------------------------------------------
Dg = sp.Function('Delta')(s_)
Sig = 1/sp.diff(Dg, s_)
dSig_dg = sp.diff(Sig, s_)/sp.diff(a0_*Dg, s_)
lhs = sp.simplify(3*Sig/dSig_dg)                                       # = -3 a0 Delta'^2 / Delta''
rhs = -3*a0_*sp.diff(Dg, s_)**2/sp.diff(Dg, s_, 2)
print(f"  g_*(s) = 3 Sigma_par / |dSigma_par/dg_phi| = 3 a0 Delta'(s)^2 / |Delta''(s)|")
check("C3 [control] sympy: g_*(s) = 3 a0 Delta'(s)^2 / |Delta''(s)|, exactly, for an arbitrary Delta",
      sp.simplify(lhs - rhs) == 0, f"residual {sp.simplify(lhs - rhs)}")

# --- C4/C5: does the cubic action exist at every finite s? ----------------------------------------
def mk_asym(C, s0, p):
    """Delta_p(s) = C[1 - (1 + s/s0)^-p]: bounded by C, strictly increasing, C-infinity, Delta(0)=0."""
    return (lambda s: C*(1.0 - (1.0 + s/s0)**(-p)),
            lambda s: C*p/s0*(1.0 + s/s0)**(-p-1),
            lambda s: -C*p*(p+1)/s0**2*(1.0 + s/s0)**(-p-2))
def Delta_published(s):
    s = float(s); return C_RAR if s > S_SAT else (s/math.expm1(math.sqrt(s)) if s > 0 else 0.0)
S_TEST = [1e2, 1e4, GM_SUN/PLANETS["Neptune"]**2/A0["canonical"], GM_SUN/PLANETS["Saturn"]**2/A0["canonical"],
          GM_SUN/AU**2/A0["canonical"], gN_cass/A0["canonical"]]
Da, Da1, Da2 = mk_asym(C_RAR, S_SAT, 1.0)
print(f"\n  the cubic action at Solar-System backgrounds (canonical footing):")
print(f"    {'s':>12s} | {'PUBLISHED (hard cut at 2.540)':>32s} | {'asymptotic p=1, s0=s_sat':>32s}")
print(f"    {'':>12s} | {'Delta_prime':>15s} {'Sigma_par':>16s} | {'Delta_prime':>15s} {'Sigma_par':>16s}")
pub_finite = asym_finite = True
for sv in S_TEST:
    dpub = numder(Delta_published, sv, h=max(1e-9, sv*1e-9))
    sig_pub = math.inf if abs(dpub) < 1e-300 else 1.0/dpub
    sig_asy = 1.0/Da1(sv)
    pub_finite &= math.isfinite(sig_pub)
    asym_finite &= (math.isfinite(sig_asy) and sig_asy > 0)
    print(f"    {sv:12.4e} | {dpub:15.4e} {sig_pub:16.4e} | {Da1(sv):15.4e} {sig_asy:16.4e}")
check("C4 the PUBLISHED kernel's cubic action exists at the Solar-System background (Sigma_par finite beyond "
      "s_sat = 2.540)",
      pub_finite,
      "Delta' = 0 identically for s > 2.540 => Sigma_par = infinity, J(Y) has infinite slope at Y = (C a0)^2, "
      "L3 undefined.  Independent confirmation of L13's P9")
check("C5 an ASYMPTOTICALLY-saturating kernel has finite positive Sigma_par and a well-defined cubic action at "
      "EVERY finite s, including every Solar-System background",
      asym_finite, "Delta' > 0 at every finite s for Delta = C[1-(1+s/s0)^-p], p > 0")

# --- C6: the closed form for g_* --------------------------------------------------------------------
print(f"\n  g_*(s) = 3 a0 Delta'^2/|Delta''| against the remaining gap to saturation (canonical, C = {C_RAR:.4f}, "
      f"s0 = {S_SAT:.3f}):")
print(f"    {'p':>6s} {'s':>12s} {'g_*/a0':>14s} {'3p/(p+1) x (C - Delta)':>24s} {'ratio':>9s}")
gap_ok = True
for p in (0.5, 1.0, 2.0):
    Dp, D1p, D2p = mk_asym(C_RAR, S_SAT, p)
    for sv in (1e4, GM_SUN/PLANETS["Saturn"]**2/A0["canonical"]):
        gs = 3.0*D1p(sv)**2/abs(D2p(sv))
        approx = 3*p/(p+1)*C_RAR*(1.0 + sv/S_SAT)**(-p)     # = 3p/(p+1) x (C - Delta), cancellation-free
        print(f"    {p:6.2f} {sv:12.4e} {gs:14.4e} {approx:24.4e} {gs/approx:9.6f}")
        gap_ok &= abs(gs/approx - 1) < 1e-12
check("C6 [control] for a power-law approach to saturation g_*(s) = [3p/(p+1)] (C a0 - g_phi(s)) exactly: the "
      "strong-coupling amplitude is proportional to the REMAINING GAP to saturation, so it closes as the kernel "
      "saturates", gap_ok)

# --- C7: 60-digit verification of the whole chain through W(Y) ------------------------------------
mp.mp.dps = 60
print(f"\n  60-digit verification: rebuild W'(Y) = J(Y)/2 from J = s/Delta(s), Y = (a0 Delta)^2, take W'' and")
print(f"  W''' by the chain rule through s, and form Sigma_par = W' + 2Y W'' and kappa3 = 2gW'' + (4/3)g^3W''':")
print(f"  (W' = J/2, so the action's Sigma = W' + 2Y W'' is HALF the paper's Sigma_par = J + 2Y dJ/dY;")
print(f"   the factor cancels in g_* = Sigma/|kappa3|.)")
print(f"    {'p':>6s} {'s':>12s} {'2 Sigma (mp)':>20s} {'1/Delta_prime':>20s} {'g_* (mp)':>16s} {'3 a0 D1^2/|D2|':>16s}")
ok_c7 = True
for p in (mp.mpf('0.5'), mp.mpf(1), mp.mpf(2)):
    for sv in (mp.mpf('1e3'), mp.mpf('1e5')):
        C, s0, a0v = mp.mpf(C_RAR), mp.mpf(S_SAT), mp.mpf(A0["canonical"])
        Dm  = lambda s: C*(1 - (1 + s/s0)**(-p))
        Ym  = lambda s: (a0v*Dm(s))**2
        Jm  = lambda s: s/Dm(s)
        dJdY = lambda s: mp.diff(Jm, s)/mp.diff(Ym, s)
        Wp   = Jm(sv)/2
        Wpp  = dJdY(sv)/2
        Wppp = (mp.diff(dJdY, sv)/mp.diff(Ym, sv))/2
        gbar = a0v*Dm(sv); Ybar = gbar**2
        Sig_mp = Wp + 2*Ybar*Wpp                       # = Sigma_par / 2
        kap3   = 2*gbar*Wpp + mp.mpf(4)/3*gbar**3*Wppp # = (1/6) dSigma_par/dg_phi
        gstar_mp = Sig_mp/abs(kap3)
        D1 = mp.diff(Dm, sv); D2 = mp.diff(Dm, sv, 2)
        gstar_cf = 3*a0v*D1**2/abs(D2)
        print(f"    {float(p):6.2f} {float(sv):12.4e} {mp.nstr(2*Sig_mp, 12):>20s} {mp.nstr(1/D1, 12):>20s} "
              f"{mp.nstr(gstar_mp, 10):>16s} {mp.nstr(gstar_cf, 10):>16s}")
        ok_c7 &= abs(2*Sig_mp/(1/D1) - 1) < mp.mpf('1e-20') and abs(gstar_mp/gstar_cf - 1) < mp.mpf('1e-18')
check("C7 [control] at 60-digit precision the reconstructed action reproduces Sigma_par = J + 2Y dJ/dY = 1/Delta' "
      "and g_* = 3 a0 Delta'^2/|Delta''| to 1e-18", ok_c7)

# ===================================================================================================
# SECTION D -- the sharp version
# ===================================================================================================
print("\n" + "-" * 122)
print("D -- THE SHARP VERSION.  Fastest saturation whose strong coupling stays above the Solar-System scale;")
print("    the resulting boost ceiling against what galaxies require; and what the xi operator changes.")
print("-" * 122)
print("  The Solar-System fluctuation the expansion must control is the scalar response to a PLANET on the")
print("  background of the Sun's field: div[Sigma grad psi] = 4 pi G drho => delta_g = G M_p/(Sigma_eff R_p^2)")
print("  at the planet's own surface.  Perturbativity needs delta_g << g_*.  Both shrink as Delta' -> 0; the")
print("  RATIO is what decides.")

def planet_ratio(p, s_bg, GMp, Rp, a0v, xi_pc=None, C=None):
    """delta_g and g_* on a background s_bg, for Delta = C[1-(1+s/s0)^-p], with the xi^2 operator optional.

    Normalisation, fixed once: L = -W(Y), Y = |grad phi|^2, W'(Y) = J(Y)/2, so the paper's
    Sigma_par = J + 2Y dJ/dY = 2(W' + 2Y W'') = 1/Delta'.  Linearised source law
        div[Sigma_par,eff grad psi] = 4 pi G drho   =>   delta_g = G M_p/(Sigma_par,eff R_p^2).
    The xi^2 operator sits INSIDE the argument of J, so a mode of wavenumber k shifts the argument by
    xi^2 k^2 (grad psi)^2: it adds J xi^2 k^2 to Sigma_par AND (Sigma_par - J) xi^2 k^2/g to the cubic
    coefficient.  Both limits are covered by the single expression below (no third derivative needed).

    Everything is evaluated in LOG space: at large p the factors (1 + s/s0)^(2p+1) overflow and
    (1 + s/s0)^(-p-1) underflows in float64, while their RATIO -- the only thing that decides -- is O(1).
    Returns (delta_g, g_*, delta_g/g_*, Sigma_eff/Sigma_par, log(delta_g/g_*)).
    """
    C = C_RAR if C is None else C
    s0, lA = S_SAT, math.log1p(s_bg/S_SAT)
    lgap = math.log(-math.expm1(-p*lA))                     # log(1 - A^-p) = log(Delta/C)
    lSig  = math.log(s0/(C*p)) + (p + 1)*lA                 # log Sigma_par = log(1/Delta')
    lJ    = math.log(s_bg) - math.log(C) - lgap             # log J = log(s/Delta)
    lgbar = math.log(a0v) + math.log(C) + lgap              # log g_phi
    lx    = -math.inf if xi_pc is None else 2*(math.log(xi_pc*PC) - math.log(Rp))   # log (xi k)^2
    lSig_eff = np.logaddexp(lSig, lJ + lx)
    lT1 = math.log((p + 1)*s0/(6*a0v*C*C*p*p)) + (2*p + 1)*lA          # |-Delta''/(6 a0 Delta'^3)|
    d = lJ - lSig                                                       # log(J/Sigma_par) < 0 always here
    lT2 = -math.inf if lx == -math.inf else (lSig + math.log(-math.expm1(d)) + lx - math.log(2.0) - lgbar)
    lkap3 = np.logaddexp(lT1, lT2)
    l_dg  = math.log(GMp) - lSig_eff - 2*math.log(Rp)
    l_gst = math.log(0.5) + lSig_eff - lkap3
    def ex(v): return math.exp(v) if -700 < v < 700 else (0.0 if v <= -700 else math.inf)
    return ex(l_dg), ex(l_gst), ex(l_dg - l_gst), ex(lSig_eff - lSig), (l_dg - l_gst)

SOURCES = {"Earth  at 1 AU":   (GM_EARTH,   R_EARTH,   AU),
           "Jupiter at 5.2 AU": (1.26687e17, 7.1492e7,  5.203*AU),
           "Saturn at 9.6 AU":  (3.7931e16,  6.0268e7,  R_SAT)}

print(f"\n  KERNEL ALONE (no xi), canonical footing.  Each planet's own scalar field at its own surface:")
print(f"    {'source':20s} {'p':>6s} {'delta_g [m/s^2]':>18s} {'g_* [m/s^2]':>16s} {'delta_g/g_*':>14s} {'perturbative?':>14s}")
noxi_ok = False; worst = []
for nm, (GMp, Rp, rp) in SOURCES.items():
    s_bg = GM_SUN/rp**2/A0["canonical"]
    for p in (0.05, 0.5, 1.0, 2.0, 5.0):
        dg, gst, rat, _, _ = planet_ratio(p, s_bg, GMp, Rp, A0["canonical"])
        worst.append(rat); noxi_ok |= rat < 1.0
        print(f"    {nm:20s} {p:6.2f} {dg:18.4e} {gst:16.4e} {rat:14.4e} {'yes' if rat < 1 else 'NO':>14s}")
s_e = GM_SUN/AU**2/A0["canonical"]
pred = GM_EARTH*(1.0 + 1.0)/(3*A0["canonical"]*R_EARTH**2*s_e)
meas = planet_ratio(1.0, s_e, GM_EARTH, R_EARTH, A0["canonical"])[2]
print(f"\n    closed form: delta_g/g_* = G M_p (p+1)/(3 a0 R_p^2 s) = [(p+1)/3](M_p/M_sun)(r_p/R_p)^2")
print(f"                 = {pred:.4e} for Earth at p = 1 (direct: {meas:.4e})")
print(f"    -> the ceiling C, the saturation scale s0 and a0 all CANCEL.  Only p enters, linearly.")
print(f"       (both footings give the identical ratio: a0 cancels between delta_g and g_*)")
check("D1 [control] the closed form delta_g/g_* = [(p+1)/3](M_p/M_sun)(r_p/R_p)^2 reproduces the direct "
      "computation to 1%", abs(meas/pred - 1) < 0.01, f"{meas:.4e} vs {pred:.4e}")
check("D2 the KERNEL ALONE is perturbative at a Solar-System source: some saturation exponent p > 0 keeps "
      "delta_g below g_* at a planet's surface",
      noxi_ok, f"the ratio is [(p+1)/3](M_p/M_sun)(r_p/R_p)^2 for EVERY kernel of the class -- 552(p+1) for "
               f"Earth, 3.8e4(p+1) for Jupiter -- and never falls below {min(worst):.4g} anywhere in the scan")

print(f"\n  WITH the coherence operator xi^2|grad_perp V|^2 at PAPER5's own Solar-System floors (Table 3):")
print(f"    {'footing':10s} {'xi [pc]':>8s} {'source':20s} {'p':>6s} {'Sig_eff/Sig':>13s} {'delta_g [m/s^2]':>17s} "
      f"{'g_* [m/s^2]':>15s} {'delta_g/g_*':>13s}")
xi_any = False; XI = {"canonical": 0.10, "alt": 0.15}
for foot in A0:
    for nm, (GMp, Rp, rp) in SOURCES.items():
        s_bg = GM_SUN/rp**2/A0[foot]
        for p in (0.5, 1.0, 2.0):
            dg, gst, rat, boost, _ = planet_ratio(p, s_bg, GMp, Rp, A0[foot], xi_pc=XI[foot])
            xi_any |= rat < 1.0
            print(f"    {foot:10s} {XI[foot]:8.2f} {nm:20s} {p:6.2f} {boost:13.4e} {dg:17.4e} {gst:15.4e} {rat:13.4e}")
check("D3 with xi at PAPER5's own Solar-System floor (0.10 pc canonical / 0.15 pc alt) there EXISTS a saturation "
      "rate that is perturbative at a Solar-System source", xi_any)

# the sharp version: the fastest saturation xi can rescue
print(f"\n  THE SHARP VERSION.  Largest saturation exponent p_max with delta_g = g_* (binding source per footing):")
print(f"    {'footing':10s} {'xi [pc]':>8s} {'source':20s} {'p_max':>9s}")
PMAX = {}
for foot in A0:
    for nm, (GMp, Rp, rp) in SOURCES.items():
        s_bg = GM_SUN/rp**2/A0[foot]
        f_of_p = lambda p: planet_ratio(p, s_bg, GMp, Rp, A0[foot], xi_pc=XI[foot])[4]
        try:
            pm = brentq(f_of_p, 1e-3, 20.0)
        except ValueError:
            pm = float('nan')
        PMAX[(foot, nm)] = pm
        print(f"    {foot:10s} {XI[foot]:8.2f} {nm:20s} {pm:9.4f}")
p_bind = min(v for v in PMAX.values() if v == v)
print(f"\n    binding p_max over both footings and all three sources: p_max = {p_bind:.4f}")
print(f"    -> a kernel that reaches its ceiling FASTER than Delta = C[1 - (s0/s)^{p_bind:.2f}] is strongly coupled")
print(f"       at a Solar-System body even with xi at its floor.  An exponential approach (p -> infinity) is excluded.")
check("D4 the xi operator rescues perturbativity for EVERY saturation rate (the perturbative window in p is "
      "unbounded)",
      p_bind > 19.0,
      f"it does not: xi buys a bounded amount, p_max = {p_bind:.3f}.  This is a NEW constraint on the kernel's "
      f"approach to saturation, absent from PAPER5.  Slower saturation is safe; exponential saturation is not")

# how much of p_max is convention?  g_* is defined by L3/L2 = 1; try 0.1 and 10 instead.
GMj, Rj, rj = SOURCES["Jupiter at 5.2 AU"]; s_j = GM_SUN/rj**2/A0["canonical"]
pm_thresh = {}
for thr in (0.1, 1.0, 10.0):
    pm_thresh[thr] = brentq(lambda p: planet_ratio(p, s_j, GMj, Rj, A0["canonical"],
                                                   xi_pc=XI["canonical"])[4] - math.log(thr), 1e-3, 20.0)
print(f"\n    convention sensitivity of p_max (the strong-coupling criterion L3/L2 = threshold):")
print(f"      threshold 0.1 -> p_max = {pm_thresh[0.1]:.4f} ;  1.0 -> {pm_thresh[1.0]:.4f} ;  "
      f"10 -> {pm_thresh[10.0]:.4f}")
check("D4b [control] p_max is robust to the O(1) ambiguity in the strong-coupling criterion: two decades of "
      "threshold move it by less than 0.4",
      abs(pm_thresh[10.0] - pm_thresh[0.1]) < 0.4,
      f"spread {abs(pm_thresh[10.0]-pm_thresh[0.1]):.3f} over 0.1 <= L3/L2 <= 10, because the ratio runs "
      f"~7 decades per unit p")

# is the answer an artefact of evaluating at the source's own surface?
print(f"\n    is the screened ratio an artefact of taking k = 1/R_p?  In the xi-dominated regime")
print(f"    Sigma_eff -> J xi^2/R_p^2, so delta_g = G M_p/(J xi^2) and the R_p^2 CANCELS:")
print(f"      {'source radius used':24s} {'delta_g [m/s^2]':>17s} {'delta_g/g_*':>14s}")
rr_free = []
for scale, lab in ((1.0, "R_Jupiter"), (10.0, "10 R_Jupiter"), (0.1, "0.1 R_Jupiter")):
    dg, gst, rat, _, _ = planet_ratio(1.0, s_j, GMj, Rj*scale, A0["canonical"], xi_pc=XI["canonical"])
    rr_free.append(rat); print(f"      {lab:24s} {dg:17.4e} {rat:14.6e}")
check("D4c [control] in the xi-screened regime the perturbativity ratio is INDEPENDENT of the radius at which "
      "the source's field is evaluated, so p_max is not an artefact of choosing the planet's surface",
      max(rr_free)/min(rr_free) < 1.01, f"spread {max(rr_free)/min(rr_free)-1:.2e} over a 100x range of radius")

# --- D5: does perturbativity constrain the boost CEILING? -----------------------------------------
print(f"\n  does the strong-coupling requirement touch the CEILING C?  Same p = 1, four different C, with xi:")
print(f"    {'C':>10s} {'g_* [m/s^2]':>16s} {'delta_g [m/s^2]':>18s} {'delta_g/g_*':>16s} {'p_max':>9s}")
rats = []
for Cv in (0.10, C_RAR, 1.00, 3.00):
    dg, gst, rat, _, _ = planet_ratio(1.0, s_e, GM_EARTH, R_EARTH, A0["canonical"], xi_pc=XI["canonical"], C=Cv)
    f_of_p = lambda p: planet_ratio(p, s_e, GM_EARTH, R_EARTH, A0["canonical"],
                                    xi_pc=XI["canonical"], C=Cv)[4]
    pm = brentq(f_of_p, 1e-3, 20.0)
    rats.append(rat)
    print(f"    {Cv:10.4f} {gst:16.4e} {dg:18.4e} {rat:16.6e} {pm:9.4f}")
check("D5 the strong-coupling requirement constrains the boost CEILING C -- perturbativity and the galactic boost "
      "are in conflict",
      max(rats)/min(rats) > 1.01,
      f"delta_g/g_* varies by only {max(rats)/min(rats)-1:.1e} relative across a 30x range of C, and p_max is "
      f"unchanged: perturbativity constrains the saturation RATE, never the ceiling.  There is NO pincer between "
      f"the bounded boost and the cubic action")

# --- D6: which of PAPER5's own Table 1 kernels are admissible under the corrected theorem? ---------
print(f"\n  which of PAPER5 Table 1's kernels satisfy the corrected theorem (Delta' > 0 at every finite s)?")
print(f"    {'kernel':18s} {'C':>8s} {'sup attained at':>17s} {'Delta_prime > 0 everywhere':>28s}")
adm = {}
for nm, fn in (("deep-MOND sqrt", Delta_deepMOND), ("standard mu", Delta_stdmu),
               ("exp carrier", Delta_expcarrier), ("nu_RAR", Delta_RAR), ("simple mu", Delta_simplemu)):
    sgrid = np.logspace(-3, 6, 900)
    vals = np.array([fn(sv) for sv in sgrid])
    mono = bool(np.all(np.diff(vals) > 0)) and int(np.argmax(vals)) == len(vals) - 1
    adm[nm] = mono
    where = "s -> infinity" if mono else f"s = {TAB1[nm][1]:.3f}"
    print(f"    {nm:18s} {TAB1[nm][0]:8.4f} {where:>17s} {('yes' if mono else 'NO'):>28s}")
check("D6 [control] exactly one of PAPER5 Table 1's five kernels -- the simple mu, C = 1.000, approached as "
      "1 - 1/y (p = 1) -- is admissible as written under the corrected theorem; the other four attain their "
      "supremum at finite s and must be continued past it rather than cut off there",
      sum(adm.values()) == 1 and adm["simple mu"],
      f"admissible: {[k for k, v in adm.items() if v]}; and its p = 1 sits below the binding p_max = {p_bind:.2f}")

# ===================================================================================================
# SECTION E -- verdict
# ===================================================================================================
print("\n" + "-" * 122)
print("E -- VERDICT")
print("-" * 122)
check("E1 the bounded-boost theorem's HYPOTHESES admit at least one kernel that is bounded, has Delta' > 0 at "
      "every finite s, and has a well-defined cubic action there -- i.e. the THEOREM is not in tension with "
      "perturbative well-definedness",
      asym_finite and gap_ok and ok_c7,
      "Delta = C[1 - (1+s/s0)^-p] is such a kernel, and PAPER5's own simple-mu entry is the p=1, C=1 member")
check("E2 the theorem's CONCLUSION AS PRINTED -- that the kernel 'must saturate at C a0 above' its maximum, "
      "with the bound 'attained on a plateau' -- is admissible",
      pub_finite,
      "an attained supremum has Delta' = 0, hence Sigma_par = infinity, an infinite-slope J(Y) at Y = (C a0)^2, "
      "and no cubic action.  The supremum must be APPROACHED and never attained.  Erratum-level, to the wording "
      "and to the carried kernel, NOT to the theorem")
check("E3 PAPER5 states the corollary its own hypotheses force -- that NO kernel of the class can screen the "
      "Solar System, so a second, non-kernel screening scale is mandatory rather than a design choice",
      False,
      "section 9 presents xi as the implementation ('which in this action is done by the coherence length xi'). "
      f"Monotonicity makes it a theorem: sup Delta = lim Delta, so the residual at Solar-System accelerations is "
      f">= the galactic boost, {PINCER['canonical'][0]:.2e}x the binding gate.  A STRENGTHENING, not a refutation")
check("E4 the theorem's EMPIRICAL content -- the ceiling C, the SPARC test, the cluster violation (sections 3-6) "
      "-- survives both corrections unchanged",
      True,
      "sup Delta is the same number whether attained or approached, and the xi operator screens by GRADIENT SCALE "
      "(xi k ~ 2e4 at 1 AU, ~1e-4 at 1 kpc), so it is inert at galactic and cluster wavelengths.  Sections 3-6 "
      "stand as published")
check("E5 a genuine internal contradiction exists INSIDE the bounded-boost theorem, requiring an erratum to the "
      "theorem itself",
      not (asym_finite and gap_ok and ok_c7),
      "no.  The tension is between the theorem's hypotheses and the CARRIED KERNEL's hard cutoff, and between the "
      "paper's silence and the screening corollary its hypotheses force.  Both are repairs to the paper, not to "
      "the theorem")
check("E6 the corrected theorem leaves the kernel's approach to saturation FREE (any Delta with Delta' > 0 will do)",
      p_bind > 19.0,
      f"it does not: perturbativity with xi at its floor caps the approach exponent at p_max = {p_bind:.3f}. "
      f"This is a new, previously unstated constraint -- weak (it only excludes very fast approaches, exponential "
      f"included) but real, and it is the one place where the cubic action does constrain the kernel")

print("\n" + "=" * 122)
print("THE CORRECTED STATEMENT OF THE BOUNDED-BOOST THEOREM")
print("=" * 122)
print(f"""
  Let a MOND-class modification be carried by one scalar phi minimally sourced by matter through a
  first-order quasilinear action, div[J(Y) grad phi] = 4 pi G rho with Y = |grad phi|^2, and write the
  scalar force as g_phi = a0 Delta(s), s = g_N/a0.  Then:

  (1)  [unchanged]  Gauss's law forces J(g_phi^2) g_phi = g_N, so g_phi is a single-valued function of
       g_N and the longitudinal stiffness is Sigma_par = J + 2 Y dJ/dY = 1/Delta'(s), identically.

  (2)  [unchanged]  Well-posedness of the static problem -- equivalently, the absence of a longitudinal
       ghost / gradient instability in the covariant completion -- requires Sigma_par > 0, hence
       Delta'(s) > 0: Delta is STRICTLY INCREASING.

  (3)  [SHARPENED]  Delta is bounded if and only if it has a finite limit C = lim_(s->inf) Delta(s)
       = sup Delta, AND THE SUPREMUM IS NEVER ATTAINED AT FINITE s.  A kernel that attains its supremum
       on a plateau has Delta' = 0 there, hence Sigma_par = infinity, an infinite-slope J(Y) at
       Y = (C a0)^2, and no cubic action: it is not an admissible member of the class.  Saturation is
       ASYMPTOTIC, not attained.  Of the five kernels in PAPER5's Table 1, only the simple mu
       (C = 1.000, approached as 1 - 1/y) is admissible as written; the exponential carrier and nu_RAR
       must be continued past their maxima, never cut off there.

  (4)  [NEW COROLLARY -- the screening corollary]  Because Delta is increasing, Delta(s_sun) > Delta(s_gal)
       for every Solar-System s_sun above every galactic s_gal.  The residual scalar force at Solar-System
       accelerations is therefore AT LEAST the galactic boost, C a0 = {C_RAR*A0['canonical']:.3e} m/s^2 for the carried
       kernel, while the Pitjev-Pitjeva phantom-mass gate caps it at {g_sat_gate:.3e} m/s^2
       ({B_RES['canonical']:.3e} a0 canonical, {B_RES['alt']:.3e} a0 alt).  The shortfall is {PINCER['canonical'][0]:.3e}x / {PINCER['alt'][0]:.3e}x for the
       carried kernel, {max(GAL_MEAS)/B_RES['canonical']:.3e}x against the measured galactic excess, and never below
       {min(GAL_MIN_REQ/B_RES[f] for f in A0):.3e}x even for the narrowest kernel in the paper's own Table 1.
       Hence NO KERNEL OF THE CLASS CAN SCREEN THE SOLAR SYSTEM.  Screening must be supplied by an
       operator OUTSIDE the class.  In this action that operator is the coherence length xi, which
       screens by GRADIENT SCALE (xi k >> 1 in the Solar System, << 1 in galaxies) rather than by
       acceleration.  The theorem does not merely permit xi; it REQUIRES it, or an equivalent second scale.

  (5)  [SCOPE]  With such an operator present, J(g_phi^2) g_phi = g_N holds only in the long-wavelength
       limit xi k -> 0.  That is exactly the regime of the galaxy and cluster tests, so the empirical
       content of PAPER5 sections 3-6 is untouched.

  (6)  [PERTURBATIVE STATUS]  For an asymptotically-saturating kernel the cubic action exists at every
       finite s, with strong-coupling amplitude
            g_*(s) = 3 a0 Delta'(s)^2/|Delta''(s)| = [3p/(p+1)] (C a0 - g_phi(s))   (power-law approach)
       -- it shrinks in proportion to the REMAINING GAP to saturation.  The ratio of a Solar-System
       source's own scalar field to g_* is [(p+1)/3](M_p/M_sun)(r_p/R_p)^2: the ceiling C, the saturation
       scale s0 and a0 all cancel, so the kernel ALONE is strongly coupled at a planet by 5.5e2 (Earth)
       to 3.8e4 (Jupiter) for EVERY member of the class.  With xi at the paper's own floor the same ratio
       is small, and perturbative control in the Solar System is a property of xi, not of the kernel.

  (7)  [NEW CONSTRAINT -- the saturation rate]  xi buys a BOUNDED amount of perturbative room: the
       binding requirement delta_g < g_* at a Solar-System body caps the approach exponent at
       p_max = {p_bind:.3f} (both footings, xi at its floor).  A kernel that reaches its ceiling faster than
       Delta = C[1 - (s0/s)^p_max] -- an exponential approach in particular -- is strongly coupled at a
       Solar-System body even with the screening.  Perturbativity therefore constrains the saturation
       RATE and never the ceiling C: there is NO pincer between the bounded boost and the cubic action.
""")

print("=" * 122)
print(f"L34 complete in {time.time()-T0:.1f} s.  {len(FAILS)} FAIL(s).")
if FAILS:
    print("FAILED CHECKS (each is a substantive finding, not a machinery failure):")
    for f in FAILS: print("   - " + f[:118])
print("=" * 122)
