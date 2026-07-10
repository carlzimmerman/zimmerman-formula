#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANE C -- THE STRUCTURAL QUESTION AQUAL CANNOT ASK
====================================================================================================
Branch B: baryons displace the dark-energy medium (Verlinde-class ELASTIC SOLID, two moduli:
shear mu + bulk K). Deep regime banked: g_D = sqrt(a0_V g_bar/6), a0_V = cH_Lambda = Z*a0,
coefficient sqrt(Z/6) = 0.982 of the required lensing source.

THE GATE: the medium's own Cassini Q2 vs the 5.2e-27 s^-2 ceiling, WITHOUT killing
(a) the Saturn enclosed-mass monopole bound, (c) SPARC high-y (g_obs=g_bar at y~6-10),
(d) the deep-regime 0.982.

LANE C asks what scalar AQUAL cannot: does the TENSOR (strain-invariant) structure of an elastic
medium parametrically suppress the external-field anisotropic coupling (the Q2 source) relative
to scalar AQUAL, while KEEPING the magnitude-EFE (monopole screen + Chae galactic EFE)?

  (C1) Linear superposition + the sqrt nonlinearity: expand the LOCAL-MODULUS realization
       R(|g_sun+g_ext|) to second order in lambda = g_sun/g_ext at the transition shell; get the
       l=2 Legendre coefficient ANALYTICALLY (sympy); compare to the AQUAL mu'-term (L0).
  (C2) Two-moduli structure: angular integrals of the pre-strain cross-coupling for the
       BULK (trace) channel vs the SHEAR (deviatoric) channel vs the scalar |g| channel.
  (C3) EFE phenomenology cross-check: can the medium keep the galaxy-scale magnitude-EFE
       (Chae+ 2020-21) while suppressing the solar-system Q2? Which structure separates them?

Both footings where they matter: canonical a0=9.36e-11 (a0_V=cH_Lambda), alt a0=1.13e-10 (cH0).
HONESTY: verified both directions; the scalar-proxy Q2 is confronted, not assumed; the family
that threads is named WITH its price. numpy/scipy/sympy only; exit 0.
"""
import numpy as np
import sympy as sp
from scipy import integrate, optimize

# ------------------------------------------------------------------ constants (SI)
c_l  = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
AU   = 1.495978707e11
kpc  = 3.0857e19
Mpc  = 3.0857e22

Z        = np.sqrt(32*np.pi/3.0)          # 5.7873
A0_CANON = 9.36e-11                        # cH_Lambda/Z (canonical, rho_DE footing)
A0_ALT   = 1.13e-10                        # cH0/Z-ish   (rho_total/cH0 footing)
cH_Lam   = Z*A0_CANON                      # 5.418e-10 (framework medium scale)
H0       = 67.4e3/Mpc
cH0      = c_l*H0                          # 6.55e-10 (Verlinde-original medium scale)

# Cassini (Park+ 2026, arXiv:2602.17884)
Q2_C, Q2_S = 1.6e-27, 1.8e-27
Q2_CEIL    = Q2_C + 2*Q2_S                 # 5.2e-27 s^-2 (2-sigma ceiling)

# Solar-system inputs
GEXT_LIST  = [1.9e-10, 2.15e-10, 2.32e-10, 2.4e-10]   # galactocentric field at the Sun
r_sat, r_mars, r_nep = 9.5826*AU, 1.5237*AU, 30.07*AU
g_sat, g_mars, g_nep = G*Msun/r_sat**2, G*Msun/r_mars**2, G*Msun/r_nep**2
M_SAT_BOUND  = 7.9e-11*Msun               # Pitjev-Pitjeva unmodeled mass < Saturn (task canonical)
M_SAT_BOUND2 = 1.7e-10*Msun               # looser literature variant carried in lane3
M_MARS_BOUND = 1.0e-11*Msun
EPM_DG_SENS  = (A0_CANON/2)/10**3.8       # banked: a0/2 tail = 10^3.8 over EPM perihelion sens.

def nu_fw(y):
    return np.sqrt(1.0 + 1.0/y)

print("="*100)
print(" LANE C -- ELASTIC-TENSOR vs SCALAR-AQUAL STRUCTURE OF THE EXTERNAL-FIELD Q2")
print("="*100)
print(f"  Z=sqrt(32pi/3)={Z:.4f}; a0 canonical={A0_CANON:.3e} (a0_V=cH_Lam={cH_Lam:.3e});")
print(f"  a0 alt={A0_ALT:.3e} (cH0={cH0:.3e}); Cassini 2-sigma ceiling Q2={Q2_CEIL:.2e} s^-2")

# ====================================================================================================
# PART C1 -- ANALYTIC: the sqrt-law anisotropic cross-term vs the AQUAL mu' term
# ====================================================================================================
# Local-modulus realization (the scalar proxy of the medium): response magnitude R(|g_tot|),
#   g_tot = g_ext e + g_sun rhat',  lambda = g_sun/g_ext,  c = cos(angle between -rhat and e).
#   |g_tot| = g_ext (1 + 2 lam c + lam^2)^{1/2}.
# Legendre-project delta R / R(g_ext) to O(lam^2). For power law R ~ |g|^s (p := s/2):
print("\n" + "="*100)
print(" (C1) ANALYTIC l=2 coefficient of the local-modulus cross-term (sympy, exact)")
print("="*100)
lam, cc, p = sp.symbols('lambda c p', positive=True)
expr = (1 + 2*lam*cc + lam**2)**p
ser  = sp.expand(sp.series(expr, lam, 0, 3).removeO())
P0, P1s, P2s = sp.Integer(1), cc, (3*cc**2-1)/2
a0c = sp.simplify(sp.Rational(1,2)*sp.integrate(ser-1, (cc,-1,1)))
a1c = sp.simplify(sp.Rational(3,2)*sp.integrate(ser*P1s, (cc,-1,1)))
a2c = sp.simplify(sp.Rational(5,2)*sp.integrate(ser*P2s, (cc,-1,1)))
a2_formula = sp.Rational(4,3)*p*(p-1)*lam**2
assert sp.simplify(a2c - a2_formula) == 0, "l=2 series coefficient does not match (4/3)p(p-1)lam^2"
print(f"  response ~ |g_e + g_s|^s = g_e^s (1+2 lam c+lam^2)^(s/2),  p=s/2:")
print(f"    l=0 shift : {sp.nsimplify(a0c)}")
print(f"    l=1 dipole: {sp.nsimplify(a1c)}   (Q2-invisible; secular quadrupole needs l=2)")
print(f"    l=2 quad  : {sp.nsimplify(a2c)}  ==  (4/3) p (p-1) lam^2   [VERIFIED symbolically]")
for s_val, tag in [(sp.Rational(1,2), "raw Verlinde sqrt g_D~sqrt(a0_V|g|/6)"),
                   (sp.Rational(1,2), "deep-MOND AQUAL phantom (nu-1)g -> sqrt(a0 g)")]:
    val = a2_formula.subs(p, s_val/2).subs(lam,1)
    print(f"    s={s_val} ({tag}): l=2 coeff = {sp.nsimplify(val)} * lam^2")
print("  => IDENTICAL -1/4 lam^2 for the raw sqrt medium and deep-MOND AQUAL: the local-modulus")
print("     realization of the medium is AQUAL-CLASS. NO parametric suppression from the sqrt law.")

# framework nu at the actual transition (y ~ etilde): local log-slope s(y) and the general
# non-power-law l=2 coefficient a2 = (s^2 - 2s + y s'(y))/3 (derived from F',F'' of R(g)):
def s_of_y(y, R):            # s = dlnR/dlng at g = y*a0 (log-slope of the response magnitude)
    h = 1e-5
    return (np.log(R(y*(1+h))) - np.log(R(y*(1-h))))/(2*h)
def a2_general(y, R):
    h = 1e-4
    s  = s_of_y(y, R)
    sp_ = (s_of_y(y*(1+h), R) - s_of_y(y*(1-h), R))/(2*h)   # y ds/dy = ds/dlny
    return (s*s - 2*s + sp_)/3.0
R_phantom = lambda y: (nu_fw(y)-1.0)*y          # phantom response (nu-1)g in a0 units
R_rawsqrt = lambda y: np.sqrt(Z/6.0)*np.sqrt(y) # raw displacement medium
# AQUAL mu' term: mu(g) = g_N/g with framework mapping g^2 = g_N^2 + g_N a0 -> L0 = dln mu/dln g
def L0_aqual(y_obs):
    def mu(yo):
        gN = (-1.0 + np.sqrt(1.0 + 4.0*yo*yo))/2.0
        return gN/yo
    h = 1e-5
    return (np.log(mu(y_obs*(1+h))) - np.log(mu(y_obs*(1-h))))/(2*h)
print(f"\n  At the transition shell (background y = etilde = g_ext/a0), the O(1) ledger:")
print(f"  {'footing':<12}{'etilde':>8}{'s_phantom':>11}{'a2_phantom':>12}{'s_rawsqrt':>11}{'a2_rawsqrt':>12}{'AQUAL L0':>10}")
for a0v, tag in [(A0_CANON,"canonical"),(A0_ALT,"alt")]:
    et = 2.32e-10/a0v
    print(f"  {tag:<12}{et:>8.3f}{s_of_y(et,R_phantom):>11.3f}{a2_general(et,R_phantom):>12.3f}"
          f"{s_of_y(et,R_rawsqrt):>11.3f}{a2_general(et,R_rawsqrt):>12.3f}{L0_aqual(et):>10.3f}")
print("""  READING (C1): every scalar (local-|g|) realization carries an O(1) anisotropic cross-term:
  the sqrt law's l=2 coefficient (-1/4 deep; -0.07..-0.25 at the shell) is the SAME O(1) family
  as the AQUAL mu'-term (L0 ~ 0.2 there); NONE of them is zero. Suppressed it is NOT (the full
  nonlinear q-integral in C3 is the quantitative version). The scalar proxy Q2 stands for this
  entire sub-family -- if the medium's nonlinearity reads the local field/strain MODULUS, Lane B's
  scalar Q2 is the TRUE class value, not an upper bound.""")

# ====================================================================================================
# PART C2 -- THE TENSOR STRUCTURE: bulk (trace) vs shear (deviatoric) pre-strain coupling
# ====================================================================================================
print("="*100)
print(" (C2) TWO-MODULI ANGULAR STRUCTURE (sympy, exact angular integrals)")
print("="*100)
# Pre-strain of the galaxy at the Sun (locally uniform): eps_gal = (t/3) I + d (e e - I/3),
#   t = trace (volumetric), d = deviatoric amplitude, e = unit vector to the GC.
# Sun's probe strain (radial displacement u = f(r) rhat):
#   eps_sun = (fp - f/r) rhat rhat + (f/r) I   [fp := f'(r)]
th, ph = sp.symbols('theta phi', real=True)
t_, d_, fp_, fr_ = sp.symbols('t d f_p f_r', real=True)   # fr_ := f/r
e_vec = sp.Matrix([0,0,1])
rhat  = sp.Matrix([sp.sin(th)*sp.cos(ph), sp.sin(th)*sp.sin(ph), sp.cos(th)])
I3    = sp.eye(3)
eps_gal = (t_/3)*I3 + d_*(e_vec*e_vec.T - I3/3)
eps_sun = (fp_-fr_)*(rhat*rhat.T) + fr_*I3
contr   = sp.expand(sp.trace(eps_gal.T*eps_sun))          # eps_gal : eps_sun
contr   = sp.simplify(contr)
# Legendre projections over the shell (measure sin(th) dth dph / 4pi):
def proj(expr_, Pl):
    return sp.simplify(sp.integrate(sp.integrate(expr_*Pl*sp.sin(th), (th,0,sp.pi)), (ph,0,2*sp.pi))/(4*sp.pi))
c2 = sp.cos(th)
P2t = (3*c2**2-1)/2
l0_full = proj(contr, 1)
l2_full = sp.simplify(proj(contr, P2t)*5)   # a2 = 5 <f P2> for unit-normalized measure
print(f"  eps_gal : eps_sun = {contr}")
print(f"  l=0 projection = {l0_full}      [trace channel ONLY: shear (d) drops out exactly]")
print(f"  l=2 projection = {l2_full}      [deviatoric channel ONLY: bulk (t) drops out exactly]")
assert sp.simplify(l0_full.subs(t_,0)) == 0, "shear pre-strain leaks into l=0"
assert sp.simplify(l2_full.subs(d_,0)) == 0, "bulk pre-strain leaks into l=2"
# and the bulk invariant J1 is blind to the pre-strain DIRECTION to ALL orders:
assert sp.simplify(sp.trace(d_*(e_vec*e_vec.T - I3/3))) == 0
print("  VERIFIED: tr[deviatoric] == 0 exactly -> any response law reading J1 = tr(eps) alone is")
print("  blind to the pre-strain direction to ALL orders (J1 of a uniform pre-strain is a scalar).")
# scalar comparison: modulus coupling wastes weight on l=0 AND locks screen to distortion
c2_dec_l0 = sp.Rational(1,2)*sp.integrate(cc**2, (cc,-1,1))
c2_dec_l2 = sp.Rational(5,2)*sp.integrate(cc**2*(3*cc**2-1)/2, (cc,-1,1))
print(f"  scalar |g| channel: c^2 = {c2_dec_l0} P0 + {c2_dec_l2} P2  (screen and quadrupole LOCKED in one term)")
print("""  READING (C2) -- the structural theorem of this lane:
   * The elastic solid has TWO independent strain invariants: J1=tr(eps) (bulk) and
     J2=eps_dev:eps_dev (shear). The angular algebra above shows the exact decoupling:
        BULK  channel: pure l=0 -- it SCREENS the monopole but can NOT source Q2 (no direction).
        SHEAR channel: pure l=2 -- it sources Q2 but does NOT screen the monopole.
   * Scalar AQUAL has ONE invariant, |grad phi|: its single nonlinear function mu must do BOTH
     jobs, so the mu' that fits the RAR transition necessarily drags the O(1) l=2 term
     (that lock IS the Desmond RAR-vs-Q2 tension).
   * A medium whose NONLINEARITY (the MOND/nu response + high-strain stiffening) lives in the
     BULK sector, with a LINEAR (harmonic) shear sector, has an ISOTROPIC linearized operator
     around the galactic pre-strain: mu=const contributes no anisotropy (superposition in the
     deviatoric sector -- task point (1): a linear medium's response is independent of pre-strain);
     V(J1) contributes stiffness that depends on WHERE you are, not on WHICH direction e points.
     => Q2 = 0 at leading order; residuals only from pre-strain GRADIENTS across the solar system
        (tidal, ~ r_t/R_gc) and from SHEAR ANHARMONICITY w (the priced dial, Part C3/C4).
   * Verlinde's own narrative fits the bulk home: the entropy displacement IS a volume effect;
     but his medium also needs shear RIGIDITY (elastic-not-fluid) -- mu>0 is required, only its
     LINEARITY is the new posit.""")
r_t = np.sqrt(G*Msun/2.32e-10)
print(f"  tidal residual scale: r_t = sqrt(GM/g_ext) = {r_t/AU:.0f} AU; r_t/R_gc = {r_t/(8.2*kpc):.2e}")
print(f"  -> gradient-induced Q2 ~ (r_t/R_gc) x scalar class value ~ 1e-6 x 1.6e-26 ~ 2e-32 s^-2: dead-negligible")

# ====================================================================================================
# PART C3 -- THE QUANTITATIVE GATE: scalar-class Q2 (Milgrom q-integral) = the UPPER BOUND,
#            and the shear-anharmonicity budget w_max that clears the ceiling
# ====================================================================================================
print("="*100)
print(" (C3) Q2 GATE: AQUAL-class value reproduced (cross-check), tensor budget w_max")
print("="*100)
# Milgrom (2009) QUMOND quadrupole, eq (12) of Desmond+2024 (same integral as the committed
# aest_cassini_quadrupole_full.py baseline -- reproduced here as the cross-check):
def q_integral(etilde, numo, eN=None):
    if eN is None:  # framework nu: eN nu(eN) = etilde -> eN^2 + eN = etilde^2 (exact)
        eN = (-1.0 + np.sqrt(1.0 + 4.0*etilde**2))/2.0
    def ig(xi, v):
        D = eN*eN + v**4 + 2*eN*v*v*xi
        if D <= 0: return 0.0
        Y = np.sqrt(D)
        return numo(Y)*(eN*(3*xi-5*xi**3) + v*v*(1-3*xi*xi))/np.sqrt(D)
    val,_ = integrate.dblquad(ig, 0.0, 60.0, lambda v: -1.0, lambda v: 1.0,
                              epsabs=1e-10, epsrel=1e-8)
    return 1.5*val, eN
def Q2_scalar(a0v, gext, numo, eN=None):
    q, eN = q_integral(gext/a0v, numo, eN)
    return -(3.0*a0v**1.5)/(2.0*np.sqrt(G*Msun))*q, q, eN

# cross-check rows on the standard 'simple' nu (the aest script's validation regime):
def nu_simple(y): return 0.5 + np.sqrt(0.25 + 1.0/y)
print("  cross-check (simple nu, a0=1.2e-10 -- the committed baseline's validation regime):")
for et in (1.5, 2.0, 2.32/1.2):
    eN = optimize.brentq(lambda x: x*nu_simple(x)-et, 1e-8, 1e3)
    Q2v, q, _ = Q2_scalar(1.2e-10, et*1.2e-10, lambda y: nu_simple(y)-1.0, eN=eN)
    print(f"    etilde={et:.3f}: q={q:+.4f}  Q2={Q2v:+.3e} s^-2  ({abs(Q2v)/Q2_CEIL:.2f}x ceiling)")

numo_fw = lambda y: nu_fw(y) - 1.0
Y_C, N_TAIL = 10.0, 1.0        # steepened tail: (nu-1)*(Y_C/y)^n for y>Y_C (SPARC-invisible)
def numo_steep(y, yc=Y_C, n=N_TAIL):
    base = nu_fw(y) - 1.0
    return base if y <= yc else base*(yc/y)**n

print(f"\n  framework nu = sqrt(1+1/y): the scalar-class Q2 (this IS Lane B's proxy):")
print(f"  {'footing':<11}{'g_ext':>9}{'etilde':>8}{'eN':>7}{'q':>9}{'Q2 [s^-2]':>12}{'x ceiling':>10}{'sigma':>8}{'w_max':>8}")
print("  " + "-"*86)
res = {}
for a0v, tag in [(A0_CANON,"canonical"), (A0_ALT,"alt")]:
    for gext in GEXT_LIST:
        Q2v, q, eN = Q2_scalar(a0v, gext, numo_fw)
        sig = (abs(Q2v)-Q2_C)/Q2_S
        res[(tag,gext)] = abs(Q2v)
        print(f"  {tag:<11}{gext:>9.2e}{gext/a0v:>8.2f}{eN:>7.2f}{q:>9.4f}{Q2v:>12.2e}"
              f"{abs(Q2v)/Q2_CEIL:>9.2f}x{sig:>8.1f}{Q2_CEIL/abs(Q2v):>8.3f}")
Q2_can = res[("canonical",2.32e-10)]; Q2_alt = res[("alt",2.32e-10)]
# steepened tail does NOT fix the scalar Q2 (sourced at y~etilde~2, not at y>10):
Q2_st,_,_ = Q2_scalar(A0_CANON, 2.32e-10, numo_steep)
print(f"\n  steepened-tail scalar Q2 (canonical, g_ext=2.32e-10): {abs(Q2_st):.2e} s^-2 "
      f"(vs {Q2_can:.2e} unsteepened: {100*abs(abs(Q2_st)/Q2_can-1):.1f}% change)")
print("  => tail steepening (the monopole fix, C4) does NOT clear Q2 -- Q2 is sourced at y~2.")
print("     The ONLY dial that clears Q2 is the tensor one: Q2_medium = w x Q2_scalar, where")
print("     w = fractional SHEAR anharmonicity at the galactic pre-strain (w=1: all-shear = AQUAL;")
print("     w=0: linear shear/nonlinear bulk = direction-blind screen).")
w_can = Q2_CEIL/Q2_can; w_alt = Q2_CEIL/Q2_alt
w_can_lo = Q2_CEIL/max(res[("canonical",g)] for g in GEXT_LIST)
w_alt_lo = Q2_CEIL/max(res[("alt",g)] for g in GEXT_LIST)
print(f"  SHEAR-ANHARMONICITY BUDGET: w_max(canonical) = {w_can:.2f} (worst over g_ext {w_can_lo:.2f});")
print(f"                              w_max(alt)       = {w_alt:.2f} (worst over g_ext {w_alt_lo:.2f})")
print("  Angular ledger from (C2): the shear channel is PURE l=2 (no l=0 dilution) -> per unit")
print("  anharmonicity it is as Q2-efficient as AQUAL (same 2/3 P2 weight); there is NO angular")
print("  free lunch -- the suppression must come from w itself being small.")

# ====================================================================================================
# PART C4 -- THE OTHER THREE NEEDLES for the named family (nonlinear-bulk / linear-shear medium)
# ====================================================================================================
print("="*100)
print(" (C4) THE SEE-SAW CLOSED? monopole, SPARC high-y, deep 0.982 for the named family")
print("="*100)
# (a) Saturn/Mars enclosed-mass monopole. In the self-dominated region (r << r_t) the external
# screen cannot help (g_sun >> g_ext); the framework nu's own 1/(2y) tail gives the banked failure;
# the bulk-stiffening law must steepen ABOVE the SPARC-constrained range (y_c ~ 10):
print("  (a) MONOPOLE (self-dominated region; the external screen only cuts r > r_t):")
print(f"  {'footing':<11}{'y_sat':>10}{'M_eff(nu) [Msun]':>17}{'/bound':>9}{'orders':>8}")
for a0v, tag in [(A0_CANON,"canonical"), (A0_ALT,"alt")]:
    y_s = g_sat/a0v
    Me = (nu_fw(y_s)-1.0)*Msun
    print(f"  {tag:<11}{y_s:>10.2e}{Me/Msun:>17.3e}{Me/M_SAT_BOUND:>8.0f}x{np.log10(Me/M_SAT_BOUND):>8.2f}")
print(f"    -> reproduces the banked 3.3-4.0-order failure of ANY pure-nu-screened source monopole.")
print(f"    steepened bulk law (nu-1)*(y_c/y)^n for y>y_c={Y_C:.0f} (invisible to SPARC, y_max~10):")
print(f"    {'footing':<11}{'n':>5}{'M_eff(Sat)':>12}{'/PP-bound':>11}{'/loose':>8}{'M_eff(Mars)':>13}{'/bound':>9}{'dg(Sat)':>10}{'/EPMsens':>9}")
n_min = {}
for a0v, tag in [(A0_CANON,"canonical"), (A0_ALT,"alt")]:
    y_s, y_m = g_sat/a0v, g_mars/a0v
    for n in (0.75, 0.82, 1.0, 1.5, 2.0):
        Ms = (nu_fw(y_s)-1.0)*(Y_C/y_s)**n*Msun
        Mm = (nu_fw(y_m)-1.0)*(Y_C/y_m)**n*Msun
        dg = (nu_fw(y_s)-1.0)*(Y_C/y_s)**n*g_sat
        print(f"    {tag:<11}{n:>5.2f}{Ms/Msun:>12.2e}{Ms/M_SAT_BOUND:>10.2f}x{Ms/M_SAT_BOUND2:>7.2f}x"
              f"{Mm/Msun:>13.2e}{Mm/M_MARS_BOUND:>8.3f}x{dg:>10.2e}{dg/EPM_DG_SENS:>8.3f}x")
    # exact threshold n_min for the strict Pitjev-Pitjeva bound:
    n_min[tag] = np.log(((nu_fw(y_s)-1.0)*Msun)/M_SAT_BOUND)/np.log(y_s/Y_C)
    print(f"    {tag}: n_min(strict 7.9e-11 Msun bound) = {n_min[tag]:.3f}")
assert 0.5 < n_min["canonical"] < 1.5
dg_nep = (nu_fw(g_nep/A0_CANON)-1.0)*(Y_C/(g_nep/A0_CANON))**1.0*g_nep
print(f"    Neptune check (weakest orbit, n=1, canonical): dg = {dg_nep:.2e} m/s^2 "
      f"({dg_nep/EPM_DG_SENS:.2f}x Saturn-grade sens; Neptune ranging is ~2-3 orders weaker -> safe)")
print("    NOTE the structural win vs Desmond: AQUAL needs SHARPNESS AT y~2 (where the RAR forbids")
print("    it) to fix Q2; here Q2 is fixed by direction-blindness, and steepness is needed only at")
print("    y>10 where NOTHING galactic constrains the law.")

# (c) SPARC high-y: the medium response must be nu-shaped (posited stiffening = banked P2), and the
# tail steepening must sit above the data:
print("\n  (c) SPARC HIGH-Y (data pin g_obs=g_bar at y~6-10):")
print(f"    {'y':>5}{'raw-sqrt overshoot':>20}{'nu-medium':>11}{'steepened(y_c=10)':>19}")
for y in (6.0, 8.0, 10.0):
    over_raw = np.sqrt(Z/6.0)/(np.sqrt(y)*(nu_fw(y)-1.0))
    over_st  = numo_steep(y)/(nu_fw(y)-1.0)
    print(f"    {y:>5.0f}{over_raw:>19.2f}x{1.00:>10.2f}x{over_st:>18.2f}x")
print("    -> raw Verlinde: 5x overshoot at y=6 (banked, reproduced). The nu-shaped bulk law fixes")
print("       it BY THE SAME POSIT (P2) already priced in lane3; steepening at y>10 changes nothing")
print("       in the SPARC window (deviation exactly 0 for y<=y_c).")

# (d) deep-regime 0.982:
print("\n  (d) DEEP REGIME (the 0.982 lensing match that motivates Branch B):")
for a0v, a0V, tag in [(A0_CANON, cH_Lam, "canonical (a0_V=cH_Lam)"), (A0_ALT, cH0, "alt (a0_V=cH0)")]:
    coef = np.sqrt((a0V/6.0)/a0v)
    print(f"    {tag:<26}: sqrt((a0_V/6)/a0) = {coef:.4f}")
print("    -> untouched: the bulk-sector nonlinearity at y<<1 is the Verlinde quadratic-energy")
print("       matching; tail steepening (y>10) and shear linearity do not enter at y<<1.")

# ====================================================================================================
# PART C5 -- THE EFE TRADE-OFF (task point 3): does Q2-suppression kill the galactic EFE?
# ====================================================================================================
print("="*100)
print(" (C5) EFE CROSS-CHECK: galaxy-scale EFE (Chae+) vs solar-system Q2 -- separated by STRUCTURE")
print("="*100)
# Chae+ 2020-21: EFE detected in SPARC rotation-curve declines at environmental e = g_ext/a0 ~
# 0.03-0.1 (magnitude effect). The trace-screen medium responds to the external strain MAGNITUDE:
print(f"  {'regime':<28}{'y range':>12}{'effect':>34}")
print(f"  {'Chae galactic EFE':<28}{'0.01-0.1':>12}{'magnitude (RC decline vs |g_ext|)':>34}")
print(f"  {'Cassini Q2':<28}{'~2.0-2.6':>12}{'DIRECTION (l=2 around the Sun)':>34}")
# sensitivity of the framework nu screen at the two operating points:
for y in (0.05, 2.3):
    dlnnu = -1.0/(2.0*(y+1.0))       # dln nu/dln y for nu=sqrt(1+1/y)
    print(f"    dln(nu)/dln(y) at y={y:<5}: {dlnnu:+.3f}")
print("""  READING (C5): in the bulk-reading medium the EFE is a MAGNITUDE effect (J1 of the total
  strain sets the local stiffness) -- it survives IN FULL at galactic operating points, because
  suppressing Q2 required killing the DIRECTIONAL (deviatoric) coupling, not the magnitude one.
  Chae's detection is a magnitude-level signal (RC declines correlated with |g_ext|): COMPATIBLE.
  There is ALSO a y-separation (EFE lives at y~0.03-0.1 where dln nu/dln y ~ -0.5 is strong; Q2
  at y~2.3 where the screen is stiffening), but the load-bearing separation is TENSORIAL, not y.
  THE PRICE, stated honestly: the medium's EFE is ISOTROPIC -- it predicts NO dependence of the
  RC distortion on disk orientation relative to g_ext, whereas AQUAL predicts an oriented
  (lopsided) distortion. A confirmed DIRECTIONAL EFE detection in galaxies would kill w<<1 and
  re-impose the scalar Q2 -> a new falsifiable discriminator, and the honest cost of this escape.""")

# galactic pre-strain amplitude honesty flag:
gN_gal = 1.9e-10
gD_gal = np.sqrt(cH_Lam*gN_gal/6.0)
eps_gal_est = 2.0*gD_gal/A0_CANON
print(f"  HONESTY FLAG -- pre-strain amplitude: eps_gal ~ 2 g_D/a0 ~ {eps_gal_est:.1f} (Verlinde")
print(f"  normalization, O(1) convention-dependent): the medium sits at O(1) strain at the Sun.")
print(f"  'Linear shear at O(1) strain' therefore constrains MATERIAL + GEOMETRIC anharmonicity")
print(f"  combined to w < {w_can:.2f} (canonical) / {w_alt:.2f} (alt) -- a real material posit, not a freebie:")
print(f"  generic solids have O(1) geometric nonlinearity at O(1) strain. Nothing in Verlinde's")
print(f"  entropy argument fixes w; it is a NEW dial the scalar theory does not even possess.")

# ====================================================================================================
# VERDICT
# ====================================================================================================
print("="*100)
print(" LANE C VERDICT")
print("="*100)
print(f"""  (1) The sqrt law does NOT self-suppress: local-modulus realization l=2 coefficient = -1/4
      lam^2 (exact, = deep-MOND AQUAL); at the shell -0.07..-0.25 vs AQUAL L0 ~ 0.2: same O(1)
      family, none zero (and the full nonlinear q-integral below confirms quantitatively).
      => Lane B's scalar-proxy Q2 ({Q2_can:.1e} canonical / {Q2_alt:.1e} alt, = {Q2_can/Q2_CEIL:.1f}x / {Q2_alt/Q2_CEIL:.1f}x ceiling)
      is the TRUE class value for any modulus-reading medium: that sub-family is DEAD at Cassini.
  (2) The tensor structure changes the answer STRUCTURALLY: bulk(trace) channel is pure l=0
      (screens, cannot source Q2 -- direction-blind to all orders, sympy-exact); shear(deviatoric)
      channel is pure l=2 (sources Q2, cannot screen). Scalar AQUAL's single invariant LOCKS the
      two (that lock is the Desmond tension); the elastic solid UNLOCKS them.
  (3) NAMED THREADING FAMILY (Branch B stays alive CONDITIONALLY):
      f = [nu-shaped nonlinear BULK sector V(J1) (posit P2, banked) with tail steepened to
      (nu-1)(y_c/y)^n, y_c~10, n >= {n_min['canonical']:.2f} (new posit P6, SPARC-invisible)] +
      [LINEAR shear sector, anharmonicity w <= {w_can_lo:.2f}-{w_can:.2f} canonical / {w_alt_lo:.2f}-{w_alt:.2f} alt (new posit P5)].
      Then: (a) Saturn monopole PASSES (n=1: {(nu_fw(g_sat/A0_CANON)-1)*(Y_C/(g_sat/A0_CANON)):.1e} vs 7.9e-11 Msun bound, {M_SAT_BOUND/Msun/((nu_fw(g_sat/A0_CANON)-1)*(Y_C/(g_sat/A0_CANON))):.0f}x under);
             (b) Cassini Q2 PASSES (w x scalar value; tidal residual ~1e-32);
             (c) SPARC high-y PASSES (nu-shaped for y<=10, deviation 0);
             (d) deep 0.982 PASSES (untouched at y<<1). Galactic magnitude-EFE SURVIVES (C5).
      PRICE: P5 (shear linearity at O(1) strain -- undialed by any derivation, and falsified by
      any confirmed DIRECTIONAL galactic EFE) + P6 (high-y tail steepening) on top of banked P1-P4.
  Lane C answer to the fork question: the scalar-proxy Q2 is an UPPER BOUND for the elastic class,
  attained at w=1 (all-shear anharmonicity); it is NOT the forced class value. Branch B is not
  killed by Cassini -- it is HOSTAGE to a material property (w) that nothing yet derives.""")
print("EXIT 0")
