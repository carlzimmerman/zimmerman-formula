#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANE 3 -- P6 AND THE FALSIFIERS (Branch B det-class elastic medium)
====================================================================================================
(a) THE TAIL: does the det-class + Verlinde's OWN elastic-to-rigid crossover (S_M <= S_DE)
    produce the steepened high-y tail the Saturn monopole needs, or is the tail a separate dial?
(b) DIRECTIONAL-EFE FALSIFIER: what directional-EFE amplitude does the lane-1 w imply at galaxy
    scales, what do data say (Chae+ 2020-22: amplitude-only), and the precise kill condition.
(c) GW CHECK: if the shear sector IS linearized GR, do GWs propagate at c with 2 polarizations?

Framework premises (reason from THESE): dS-Unruh modified inertia reframed source-side (Branch B);
a0 = cH_Lambda/Z = 9.36e-11 canonical (a0_V = cH_Lambda = Z a0), alt a0 = 1.13e-10 (a0_V = cH0).
Banked lane-C structure: bulk(J1) = pure l=0 (screens monopole), shear(e) = pure l=2 (sources Q2),
Q2_medium = w x Q2_scalar-class, w <= 0.22-0.26 canonical / 0.17-0.19 alt (P5).
Det-class: E(eps) = (mu/2) J2 + F(det(1+eps)).

HONESTY: 'tail is a separate dial / P6 stays a posit' and 'crossover forces it' are BOTH
reportable; every fork run both footings; the SPARC confrontation is the REAL point-level fit
(pipeline verbatim from decider_sparc_pointlevel.py, benchmark asserted), not an eyeball.
"""
import numpy as np, sympy as sp, glob, os
from scipy import integrate, optimize

# ----------------------------------------------------------------- constants (SI)
c_l  = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
AU   = 1.495978707e11
kpc  = 3.0857e19
Mpc  = 3.0857e22
hbar = 1.054571817e-34

Z        = np.sqrt(32*np.pi/3.0)            # 5.7873
A0_CANON = 9.36e-11                          # cH_Lambda/Z (canonical, rho_DE footing)
A0_ALT   = 1.13e-10                          # cH0/Z-ish   (rho_total/cH0 footing)
cH_Lam   = Z*A0_CANON                        # 5.418e-10  (framework medium scale a0_V)
H0       = 67.4e3/Mpc
cH0      = c_l*H0                            # 6.55e-10   (Verlinde-original a0_V)

# Cassini Q2 (Park+2026): ceiling
Q2_C, Q2_S = 1.6e-27, 1.8e-27
Q2_CEIL    = Q2_C + 2*Q2_S                   # 5.2e-27 s^-2

# solar-system inputs (lane-C conventions)
r_sat, r_mars, r_nep = 9.5826*AU, 1.5237*AU, 30.07*AU
g_sat  = G*Msun/r_sat**2
g_mars = G*Msun/r_mars**2
g_nep  = G*Msun/r_nep**2
M_SAT_BOUND  = 7.9e-11*Msun                  # Pitjev-Pitjeva strict
M_SAT_BOUND2 = 1.7e-10*Msun                  # loose variant
M_MARS_BOUND = 1.0e-11*Msun
EPM_DG_SENS  = (A0_CANON/2)/10**3.8          # banked EPM perihelion sensitivity proxy

nu_fw = lambda y: np.sqrt(1.0 + 1.0/np.maximum(y, 1e-15))

print("="*100)
print(" LANE 3 -- P6 (THE TAIL) AND THE FALSIFIERS (directional EFE, GW sector)")
print("="*100)
print(f"  Z = {Z:.4f};  a0 canonical {A0_CANON:.3e} (a0_V=cH_Lam={cH_Lam:.3e});"
      f"  a0 alt {A0_ALT:.3e} (a0_V=cH0={cH0:.3e})")

# ====================================================================================================
# PART A0 -- THE MAPPING (get it right and state it)
# ====================================================================================================
print("\n" + "="*100)
print(" (A0) THE STRAIN MAPPING: high-y is LARGE source strain, deep MOND is SMALL strain")
print("="*100)
# Verlinde 1611.02269 (fetched, exact coefficients):
#   S_M(r)  = 2 pi M c r / hbar          (entropy REMOVED by matter M within r)
#   S_DE(r) = (r/L) A(r) c^3/(4 G hbar)  (volume-law dark-energy entropy),  A = 4 pi r^2, L = c/H
#   his 'strain' filling fraction: eps_M(r) := |S_M|/S_DE.
# eps_M = [2 pi M c r/hbar] / [pi r^3 c^3/(G hbar L)] = 2 G M L/(c^2 r^2) = 2 g_bar/(c H).
r_s, M_s, L_s, G_s, cs, hb = sp.symbols('r M L G c hbar', positive=True)
S_M  = 2*sp.pi*M_s*cs*r_s/hb
S_DE = (r_s/L_s)*(4*sp.pi*r_s**2)*cs**3/(4*G_s*hb)
eps_M_sym = sp.simplify(S_M/S_DE)
assert sp.simplify(eps_M_sym - 2*(G_s*M_s/r_s**2)*L_s/cs**2) == 0
print("  Verlinde budget ratio (sympy-exact from his S_M, S_DE):")
print(f"    eps_M = |S_M|/S_DE = {eps_M_sym} = 2 g_bar L/c^2 = 2 g_bar/(cH) = 2y/Z_eff")
print("  MAPPING: eps_M is linear in y = g_bar/a0. HIGH-y = LARGE source strain (budget overdrawn);")
print("  deep MOND (y<<1) = SMALL strain = the elastic regime. [NB: this is the SOURCE/entropy strain;")
print("  lane C's eps_gal~2.8 is the RESPONSE strain 2 g_D/a0 -- a different O(1) quantity. The")
print("  crossover criterion lives in eps_M.]")
yc_canon = cH_Lam/(2*A0_CANON)   # eps_M = 1  <=>  g_bar = a0_V/2  <=>  y = a0_V/(2 a0)
yc_alt   = cH0/(2*A0_ALT)
print(f"\n  CROSSOVER eps_M = 1  <=>  g_bar = a0_V/2  (Verlinde eq 1.3: Sigma < a0_V/(8 pi G)):")
print(f"    canonical: y_c = cH_Lam/(2 a0) = Z/2      = {yc_canon:.4f}")
print(f"    alt:       y_c = cH0/(2 a0_alt)           = {yc_alt:.4f}")
print(f"  => y_c ~ 2.9 on BOTH footings (the ratio a0_V/a0 ~ Z is footing-invariant): the crossover")
print(f"     LOCATION is DERIVED, parameter-free, from Verlinde's own entropy bookkeeping.")
print(f"  Sun's galactic environment: y_ext ~ 2.0-2.6 < y_c = 2.9: the local medium sits AT ~70-90%")
print(f"     of budget -- marginally elastic (consistent with lane C's O(1) pre-strain).")

# ====================================================================================================
# PART A1 -- det-class geometry (exact) + what the displacement match fixes
# ====================================================================================================
print("\n" + "="*100)
print(" (A1) det-CLASS GEOMETRY (sympy-exact) + F FIXED BY THE DISPLACEMENT MATCH IS SCALE-FREE")
print("="*100)
e11,e22,e33,e12,e13,e23 = sp.symbols('e11 e22 e33 e12 e13 e23', real=True)
E = sp.Matrix([[e11,e12,e13],[e12,e22,e23],[e13,e23,e33]])
I3 = sp.eye(3)
J1 = sp.trace(E)
Edev = E - (J1/3)*I3
J2 = sp.trace(Edev*Edev)
detE = sp.det(I3+E)
I1 = J1
I2 = sp.Rational(1,2)*(sp.trace(E)**2 - sp.trace(E*E))
I3i = sp.det(E)
assert sp.simplify(detE - (1+I1+I2+I3i)) == 0
poly2 = sp.Poly(sp.expand(detE - (1 + J1 + J1**2/3 - J2/2)), e11,e22,e33,e12,e13,e23)
min_deg = min(sum(m) for m in poly2.monoms())
assert min_deg >= 3
print("  det(1+eps) = 1 + I1 + I2 + I3  [EXACT];  det = 1 + J1 + J1^2/3 - J2/2 + O(eps^3)  [VERIFIED:")
print(f"    residual is pure O(eps^{min_deg})]. Shear enters the volume only at SECOND order.")
t = sp.Symbol('t', real=True)
edir = sp.Matrix([[1,0,0],[0,-1,0],[0,0,0]])       # a traceless (pure shear) direction
eps0 = sp.Symbol('epsilon0', real=True)
d_first = sp.diff(sp.det(I3 + eps0*I3 + t*edir), t).subs(t,0)
assert sp.simplify(d_first) == 0
print("  First-order det-derivative in a SHEAR direction about an isotropic pre-strain = 0 EXACTLY")
print("  => the F-sector's leading EFE coupling is through J_bg (SCALAR); directional coupling")
print("     starts at second order (-F'(e_bg:e_probe) + F'' terms) -- the lane-1 w. [Re-verified.]")

# what the deep displacement match fixes: F'(delta) ~ delta^2 (cubic F), hence SCALE-FREE:
print("""
  F FIXED BY THE DISPLACEMENT MATCH (two equivalent packagings, same phenomenology):
    (i)  Verlinde form: harmonic medium + entropy-displacement work linear in u; his eq 7.40
         int_0^r G M_D^2/r'^2 dr' = M_b a0_V r/6, valid ONLY where eps_M < 1. d/dr => POINTWISE
         g_D^2 = a0_V g_bar / 6 -- a pure power law.
    (ii) det-class effective form: bulk force balance F'(delta) ~ g_bar with g_D ~ a0-scale * delta
         => F'(delta) ~ delta^2, i.e. F ~ |delta|^3 (the AQUAL deep action transplanted to J1).
  EITHER WAY the matched law g_D = sqrt(a0_V g_bar/6) is SCALE-FREE in y: it contains NO scale
  at which to end the MOND response. THE TAIL CANNOT COME FROM THE det-CLASS F ITSELF.
  The ONLY scale the medium owns is eps_M ~ 1 (entropy budget exhausted) -- Verlinde's crossover.
  => The question 'is the tail a separate dial?' becomes: does the BUDGET fix the tail?""")

# ====================================================================================================
# PART A2 -- THE THREE READINGS OF THE CROSSOVER, CONFRONTED (Saturn / Mars / EPM / Neptune)
# ====================================================================================================
print("="*100)
print(" (A2) THREE READINGS OF S_M <= S_DE ABOVE y_c -- WHICH SURVIVE THE MONOPOLE GATE?")
print("="*100)
print("""  Reading 1 (CAP):       the medium may deliver apparent mass up to the budget maximum:
                         M_D <= M_cap(r) with 2 pi M_cap c r/hbar = S_DE(r) => M_cap = r^2 cH/(2G),
                         i.e. g_D -> cH/2 = Z a0/2 CONSTANT. (Budget as a mere ceiling.)
  Reading 2 (DEPLETION): where eps_M > 1 matter has removed ALL the volume-law entropy; no medium
                         left to respond; response -> 0. (Verlinde's own text: inside, 'gravity is
                         well described by general relativity' -- area law dominates.)
  Reading 3 (THROTTLE):  response efficiency = the AVAILABLE entropy fraction:
                         T(y) = min(1, S_DE/S_M) = min(1, y_c/y)  -- the MINIMAL depletion profile,
                         an EXACT n=1 power tail with derived onset y_c = Z/2. (nu-1)_eff = (nu-1) T.""")
# --- Reading 1: cap
print("  [Reading 1: CAP]  g_D -> cH/2 const; confront EPM/ephemerides:")
for a0v, a0V, tag in [(A0_CANON, cH_Lam, "canonical"), (A0_ALT, cH0, "alt")]:
    gcap = a0V/2
    Mcap_sat = r_sat**2*a0V/(2*G)
    print(f"    {tag:<10}: g_D = {gcap:.2e} m/s^2 = {gcap/EPM_DG_SENS:.1e}x EPM sens "
          f"({np.log10(gcap/EPM_DG_SENS):.1f} orders); M_cap(Sat) = {Mcap_sat/Msun:.2e} Msun "
          f"= {Mcap_sat/M_SAT_BOUND:.1e}x strict bound ({np.log10(Mcap_sat/M_SAT_BOUND):.1f} orders)")
print("    => CAP alone is DEAD (the const-a0 tail failure, ~4.6 orders). The budget as a mere")
print("       ceiling does NOT save Saturn.")

# --- required average tail exponent (power-law from the DERIVED y_c)
print(f"\n  Required average tail exponent n_min from the DERIVED onset y_c (strict Saturn bound):")
n_min = {}
for a0v, ycv, tag in [(A0_CANON, yc_canon, "canonical"), (A0_ALT, yc_alt, "alt")]:
    y_s = g_sat/a0v
    n_min[tag] = np.log(((nu_fw(y_s)-1.0)*Msun)/M_SAT_BOUND)/np.log(y_s/ycv)
    print(f"    {tag:<10}: y_sat = {y_s:.3e}, n_min = {n_min[tag]:.3f}"
          f"   (lane C's 0.82 was for the POSITED y_c=10; the derived earlier onset relaxes it)")

# --- Readings 2/3: Saturn / Mars / EPM / Neptune margins
print(f"\n  [Readings 2/3]  monopole margins (T=hard depletion: 0 above y_c; T=throttle: y_c/y):")
print(f"    {'footing':<10}{'reading':<12}{'M_eff(Sat)/Msun':>16}{'/strict':>10}{'/loose':>10}"
      f"{'M_eff(Mars)':>13}{'/bound':>9}{'dg(Sat)':>11}{'/EPMsens':>10}")
for a0v, ycv, tag in [(A0_CANON, yc_canon, "canonical"), (A0_ALT, yc_alt, "alt")]:
    y_s, y_m = g_sat/a0v, g_mars/a0v
    for rd, Tfun in [("depletion", lambda y, yc: 0.0), ("throttle", lambda y, yc: yc/y)]:
        Ms = (nu_fw(y_s)-1.0)*Tfun(y_s, ycv)*Msun
        Mm = (nu_fw(y_m)-1.0)*Tfun(y_m, ycv)*Msun
        dg = (nu_fw(y_s)-1.0)*Tfun(y_s, ycv)*g_sat
        print(f"    {tag:<10}{rd:<12}{Ms/Msun:>16.2e}{Ms/M_SAT_BOUND:>9.3f}x{Ms/M_SAT_BOUND2:>9.3f}x"
              f"{Mm/Msun:>13.2e}{Mm/M_MARS_BOUND:>8.1e}x{dg:>11.2e}{dg/EPM_DG_SENS:>9.3f}x")
    y_n = g_nep/a0v
    dgn = (nu_fw(y_n)-1.0)*(ycv/y_n)*g_nep
    print(f"    {tag:<10}{'(Neptune, throttle)':<24}dg = {dgn:.2e} m/s^2 = {dgn/EPM_DG_SENS:.3f}x "
          f"Saturn-grade sens (Neptune ranging ~2-3 orders weaker: safe)")
assert (nu_fw(g_sat/A0_CANON)-1.0)*(yc_canon/(g_sat/A0_CANON))*Msun < M_SAT_BOUND
assert (nu_fw(g_sat/A0_ALT)-1.0)*(yc_alt/(g_sat/A0_ALT))*Msun < M_SAT_BOUND
print("    => THROTTLE (the SLOWEST budget-consistent depletion, exact n=1 > n_min~0.74-0.76)")
print("       PASSES the strict Saturn bound by ~18-26x on both footings; Mars by ~5e3x; EPM by ~38x.")
print("       Anything from n=0.75 up to full depletion passes the monopole; the pinch moves to SPARC.")

# ====================================================================================================
# PART A3 -- THE REAL SPARC POINT-LEVEL CONFRONTATION (pipeline verbatim, benchmark asserted)
# ====================================================================================================
print("\n" + "="*100)
print(" (A3) SPARC POINT-LEVEL FIT (real 175-galaxy data) OF THE DERIVED-TAIL MEMBERS")
print("="*100)
DATADIR = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
def load_sparc():
    Rl,Vol,eVl,Vg2l,Vd2l,Vb2l = [],[],[],[],[],[]
    for f in sorted(glob.glob(os.path.join(DATADIR,"*_rotmod.dat"))):
        try: d = np.genfromtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        R,Vobs,eV,Vgas,Vdisk,Vbul = (d[:,i] for i in range(6))
        Rl.append(R*kpc); Vol.append(Vobs); eVl.append(eV)
        Vg2l.append(np.sign(Vgas)*Vgas**2); Vd2l.append(Vdisk**2); Vb2l.append(Vbul**2)
    return (np.concatenate(Rl),np.concatenate(Vol),np.concatenate(eVl),
            np.concatenate(Vg2l),np.concatenate(Vd2l),np.concatenate(Vb2l))
Rm,Vobs,eV,Vg2,Vd2,Vb2 = load_sparc()
gobs = (Vobs*1e3)**2/Rm
wgt  = 1.0/np.clip(eV,1,None)**2*np.clip(Vobs,1,None)**2
UGRID = np.arange(0.30,1.2001,0.025)
def fit(boost, a0):
    best = (None,1e9)
    for Ud in UGRID:
        gb = (Vg2 + Ud*Vd2 + 1.4*Ud*Vb2)*1e6/Rm
        ok = (gb>0)&(gobs>0)&np.isfinite(gb)&(Vobs>0)
        gp = gb[ok]*(1.0 + boost(gb[ok]/a0))
        r  = np.log10(gobs[ok]) - np.log10(gp)
        rms = np.sqrt(np.sum(wgt[ok]*r**2)/np.sum(wgt[ok]))
        if rms < best[1]: best = (Ud, rms)
    return best
F_fw = lambda y: nu_fw(y) - 1.0
def T_hard(y, yc):   return np.minimum(1.0, yc/np.maximum(y,1e-15))
def T_m2(y, yc):     return (1.0 + (np.maximum(y,1e-15)/yc)**2)**-0.5     # smooth, same n=1 tail
def T_n(y, yc, n):   return np.where(y<=yc, 1.0, (yc/np.maximum(y,1e-15))**n)
def T_cut(y, yc):    return (y<=yc).astype(float)
print(f"  {len(Rm)} SPARC points; pre-committed decider rule: ALIVE drms<=0.010, DEAD rms>0.122, COND between.")
for tag, a0, ycv in [("CANONICAL", A0_CANON, yc_canon), ("ALT", A0_ALT, yc_alt)]:
    Uf, rf = fit(F_fw, a0)
    bench = "  [BENCH OK]" if abs(rf-0.108) < 0.012 else "  [BENCH DRIFT]"
    print(f"\n  --- {tag} (y_c={ycv:.3f}): framework-nu benchmark rms={rf:.4f} @ Ups={Uf:.2f}{bench}")
    if a0 == A0_CANON:
        assert abs(rf-0.108) < 0.012 and abs(Uf-0.70) < 0.10, "pipeline broken"
    members = [("throttle n=1 (hard min)",  lambda y: F_fw(y)*T_hard(y,ycv)),
               ("throttle n=1 (smooth m=2)",lambda y: F_fw(y)*T_m2(y,ycv)),
               ("tail n=0.75 (n_min edge)", lambda y: F_fw(y)*T_n(y,ycv,0.75)),
               ("tail n=2",                 lambda y: F_fw(y)*T_n(y,ycv,2.0)),
               ("HARD CUTOFF at y_c",       lambda y: F_fw(y)*T_cut(y,ycv))]
    for name, Fb in members:
        U, r = fit(Fb, a0); d = r - rf
        v = "ALIVE" if d <= 0.010 else ("DEAD" if r > 0.122 else "COND")
        print(f"    {name:>26}: Ups={U:.2f}  rms={r:.4f}  drms={d:+.4f}   [{v}]")
print("""  LENSING-NORM check (deep 0.982): all T-members = 1 identically for y <= y_c ~ 2.9 (hard/T_n/cut)
  -- the y ~ 0.03-0.3 lensing/deep window is UNTOUCHED, 0.982 intact EXACTLY. The smooth m=2 variant
  suppresses by (1+(y/2.9)^2)^-1/2 < 0.2% at y<=0.3: also intact.""")

# ====================================================================================================
# PART A4 -- Q2 GATE RECHECK: the throttled response through the banked kernel; updated w budget
# ====================================================================================================
print("="*100)
print(" (A4) Q2 RECHECK WITH THE DERIVED TAIL (banked QUMOND kernel) -> updated w budget")
print("="*100)
def q_integral(etilde, numo):
    eN = (-1.0 + np.sqrt(1.0 + 4.0*etilde**2))/2.0      # framework-nu mapping (background y<yc: unthrottled)
    def ig(xi, v):
        D = eN*eN + v**4 + 2*eN*v*v*xi
        if D <= 0: return 0.0
        Y = np.sqrt(D)
        return numo(Y)*(eN*(3*xi-5*xi*xi*xi) + v*v*(1-3*xi*xi))/np.sqrt(D)
    val,_ = integrate.dblquad(ig, 0.0, 60.0, lambda v:-1.0, lambda v:1.0, epsabs=1e-9, epsrel=1e-7)
    return 1.5*val
def Q2_of(a0v, gext, numo):
    q = q_integral(gext/a0v, numo)
    return abs((3.0*a0v**1.5)/(2.0*np.sqrt(G*Msun))*q)
print(f"  {'footing':<11}{'g_ext':>9}{'Q2 fw-nu':>12}{'Q2 throttled':>14}{'ratio':>8}"
      f"{'w_max (fw)':>12}{'w_max (thr)':>13}")
wmax = {}
for a0v, ycv, tag in [(A0_CANON, yc_canon, "canonical"), (A0_ALT, yc_alt, "alt")]:
    worst_fw, worst_th = 0.0, 0.0
    for gext in (1.9e-10, 2.32e-10, 2.6e-10):
        numo_f  = lambda Y: nu_fw(Y)-1.0
        numo_th = lambda Y: (nu_fw(Y)-1.0)*min(1.0, ycv/Y)
        Qf, Qt = Q2_of(a0v, gext, numo_f), Q2_of(a0v, gext, numo_th)
        worst_fw, worst_th = max(worst_fw,Qf), max(worst_th,Qt)
        print(f"  {tag:<11}{gext:>9.2e}{Qf:>12.2e}{Qt:>14.2e}{Qt/Qf:>8.3f}"
              f"{Q2_CEIL/Qf:>12.3f}{Q2_CEIL/Qt:>13.3f}")
    wmax[tag] = (Q2_CEIL/worst_fw, Q2_CEIL/worst_th)
print(f"""  => HONEST SURPRISE, reported as computed: throttling the Y > y_c regions INCREASES |Q2| by
     1-3% (the q-integrand has cancelling sign regions; the throttle removes some negative-
     contributing ones). The w budget is ESSENTIALLY UNCHANGED, tightening marginally:
     worst-corner w <= {wmax['canonical'][0]:.3f} -> {wmax['canonical'][1]:.3f} (canonical), {wmax['alt'][0]:.3f} -> {wmax['alt'][1]:.3f} (alt).
     The derived P6 neither rescues nor burdens P5. (Background shell y~2.0-2.6 < y_c stays
     unthrottled: lane C's structural analysis unchanged.)""")

# ====================================================================================================
# PART B -- THE DIRECTIONAL-EFE FALSIFIER
# ====================================================================================================
print("="*100)
print(" (B) DIRECTIONAL EFE: det-class predicts NEARLY ISOTROPIC galactic EFE; amplitude + kill test")
print("="*100)
# Legendre structure of a local-modulus (AQUAL-class) response, re-derived fresh (sympy):
lam, cc, s_ = sp.symbols('lambda c s', positive=True)
expr = (1 + 2*lam*cc + lam**2)**(s_/2)          # |g_in rhat + g_ext e|^s / g_in^s, lam = g_ext/g_in
ser  = sp.expand(sp.series(expr, lam, 0, 3).removeO())
a1 = sp.simplify(sp.Rational(3,2)*sp.integrate(ser*cc, (cc,-1,1)))
a2 = sp.simplify(sp.Rational(5,2)*sp.integrate(ser*(3*cc**2-1)/2, (cc,-1,1)))
print(f"  AQUAL-class response ~ |g_tot|^s, lam = g_ext/g_in (GALAXY frame: internal-dominated):")
print(f"    l=1 (lopsided) coeff a1 = {a1}   l=2 coeff a2 = {sp.simplify(a2)}")
assert sp.simplify(a1 - s_*lam) == 0
assert sp.simplify(a2 - sp.Rational(1,3)*s_*(s_-2)*lam**2) == 0
print("    [VERIFIED: a1 = s*lam exactly at O(lam); a2 = s(s-2)/3 * lam^2]")
# observable: modulation of the PHANTOM part only; asymmetry in g_obs = f_D * a_l, f_D = (nu-1)/nu
def slope_R(y):     # log-slope of phantom response R = (nu-1)*y at y
    h = 1e-5
    R = lambda yy: (nu_fw(yy)-1.0)*yy
    return (np.log(R(y*(1+h))) - np.log(R(y*(1-h))))/(2*h)
print(f"\n  AQUAL-class directional amplitudes at galactic operating points (phantom-share weighted),")
print(f"  vs det-class (= w x AQUAL; lane-1 budget w <= 0.26 canonical / 0.19 alt):")
print(f"  {'y_in':>6}{'e_ext':>7}{'lam':>7}{'s(y)':>7}{'f_D':>7}{'A_g(l=1)':>10}{'A_v(l=1)':>10}"
      f"{'A_g(l=2)':>10}{'detclass A_v(l=1)':>19}")
for y_in in (0.1, 0.3, 1.0):
    for e_ext in (0.03, 0.06, 0.10):
        lamv = e_ext/y_in
        if lamv > 0.8: continue                     # expansion validity
        sv  = slope_R(y_in)
        fD  = (nu_fw(y_in)-1.0)/nu_fw(y_in)
        A1g = sv*lamv*fD                             # fractional l=1 modulation of g_obs
        A2g = abs(sv*(sv-2)/3)*lamv**2*fD
        print(f"  {y_in:>6.2f}{e_ext:>7.3f}{lamv:>7.3f}{sv:>7.3f}{fD:>7.3f}{A1g:>10.4f}{A1g/2:>10.4f}"
              f"{A2g:>10.4f}{0.26*A1g/2:>13.4f} (can)")
print("""  READING: AQUAL-class predicts an ALIGNED (with g_ext) near/far kinematic asymmetry of outer
  rotation curves at the ~1-4% level in velocity for golden-galaxy conditions (e~0.05-0.1,
  y_in~0.1-0.3, lam~0.2-0.6); the det-class medium predicts <= w x that, i.e. <~ 0.3-1% (canonical)
  / <~0.2-0.8% (alt). O(lam^2) truncation: treat lam>~0.5 rows as scale estimates only.

  LITERATURE (honest check, 2026-07 web search):
   * Chae+2020 (ApJ 904,51; arXiv:2009.11525): EFE detected 8-11 sigma in golden galaxies, >4 sigma
     blind over 153 SPARC -- via an ANGLE-AVERAGED fit function nu(y;e) (fixed 60-deg geometry).
     AMPLITUDE-ONLY. No directional information used or extracted.
   * Chae+2021 SEP II (ApJ 921; arXiv:2109.04745): environmental g_ext estimated FROM large-scale
     structure and compared to fitted e -- consistent. Still MAGNITUDE-only; but the LSS g_ext
     VECTORS now exist for the sample.
   * Chae 2022 (ApJ 941, arXiv:2201.02109): numerical EFE solutions -- AXISYMMETRIC case
     (g_ext parallel to rotation axis): explicitly the non-directional configuration.
   * Directional/lopsided EFE signatures exist in the literature ONLY as PREDICTIONS/simulations
     (Wu+2017 ApJ lopsidedness; Candlish+2018 MNRAS 480,5362 cluster disks; Banik+2024 ring
     galaxies) -- NO observational detection of an ALIGNED asymmetry to date.
  => Current EFE data are amplitude-only: they CANNOT distinguish w~1 (AQUAL) from w<<1 (det-class).
     The det-class is NOT in tension with any existing EFE observation; equally, nothing yet
     confirms its distinctive isotropy.

  KILL CONDITION (precise, falsifiable): stack outer-RC near/far asymmetries (or HI isophote
  lopsidedness) of the Chae golden/high-e SPARC galaxies on the LSS-DERIVED g_ext DIRECTION
  (vectors already computed in Chae+2021 II).
    - ALIGNED asymmetry detected at the AQUAL amplitude (A_v ~ 1-4%, scaling as s*lam*f_D/2):
      w ~ 1 => Q2_medium = Q2_scalar-class = {0:.1f}-{1:.1f}x the Cassini ceiling => BRANCH B DEAD.
    - Null at the <~0.5% level: w <~ 0.15-0.25 CONFIRMED at galaxy scales -- P5 gets its first
      empirical support (and AQUAL-class MOND takes the hit instead).
  This is a data-in-hand test: SPARC kinematics + Chae II environment vectors suffice.""".format(
      1.0/wmax['canonical'][0], 1.0/wmax['alt'][0]))

# ====================================================================================================
# PART C -- GW SECTOR: shear waves = GR gravitons; speed, polarizations, GW170817
# ====================================================================================================
print("="*100)
print(" (C) GW CHECK: the linear shear sector as GR -- speed c, 2 polarizations, GW170817 margins")
print("="*100)
print("""  STRUCTURE (Branch B construction): ONE shared metric; the medium enters as a SOURCE
  (stress-energy), not as a modification of the graviton kinetic term. The lane-1 identification
  sets the shear stiffness at the Fierz-Pauli normalization mu ~ c^4/(32 pi G) (strain = h/2):
    * TT sector: the 2 transverse-traceless strain modes ARE the GR gravitons BY IDENTIFICATION --
      exactly 2 polarizations, speed c at the level of the linear (harmonic) shear term.
    * The medium's own longitudinal (bulk) phonon is a MATTER-sector sound wave in the dark-energy
      medium, not a metric polarization: detectors couple to it only through its (negligible)
      gravitational field. No extra GW polarizations are introduced.
  CORRECTION TO c_T from the medium's stresses: the bulk pre-stress at MOND strains enters the
  TT dispersion as an effective mass/stress term ~ sigma_bulk/(mu k^2):
    sigma_bulk ~ rho_DE c^2 (the a0-scale stress: a0^2/G ~ rho_DE c^2), mu k^2 = GR kinetic term
    => dc^2/c^2 ~ 32 pi G rho_DE/(c^2 k^2) = 4 Lambda_eff / k^2  (the standard 'Lambda does not
       move GW speed' scaling -- here it is the medium's ENTIRE stress budget).""")
GW170817 = 4.5e-16
for tag, Hval in [("canonical (H_Lambda)", cH_Lam/c_l), ("alt (H0, rho_total)", H0)]:
    Lam_eff = 3*Hval**2/c_l**2
    for f_gw, band in [(100.0, "LIGO 100 Hz"), (1e-8, "PTA 1e-8 Hz")]:
        k = 2*np.pi*f_gw/c_l
        dc2 = 4*Lam_eff/k**2
        marg = np.log10(GW170817/(dc2/2)) if f_gw > 1 else float('nan')
        extra = f"  margin vs GW170817 = 10^{marg:.1f}" if f_gw > 1 else "  (no speed bound there; still tiny)"
        print(f"    {tag:<22} {band:<13}: dc^2/c^2 ~ {dc2:.1e}{extra}")
dc2_ligo = 4*(3*(cH_Lam/c_l)**2/c_l**2)/((2*np.pi*100/c_l)**2)
assert dc2_ligo/2 < 1e-30
print(f"""    Birefringence from the galactic shear pre-strain (w-suppressed anharmonic coupling):
      dc/c(+ vs x) ~ w * eps_bg * (4 Lambda/k^2) <~ 0.26 * 3 * 1e-40 ~ 1e-40: nothing.
    Photon-vs-graviton: both propagate on the one shared metric through the same medium stress;
      relative delay over 40 Mpc ~ (dc/c) D/c ~ {0.5*dc2_ligo*40*Mpc/c_l:.0e} s vs the measured 1.7 s window.
  VERDICT (c): GW170817-SAFE not just photon-vs-graviton but within the GW sector itself, by
  ~24-25 ORDERS on both footings; 2 polarizations by construction (the medium adds a matter-sector
  bulk phonon, not a metric mode). HONEST LIMIT: this is the dimensional-analysis level -- Branch B
  still has NO covariant action; the medium's inertial density (hence the bulk phonon's own
  dispersion and its cosmological perturbations) is UNDEFINED (Verlinde is quasi-static). What IS
  robust: any medium stress bounded by rho_DE c^2 moves c_T by <~ Lambda/k^2 -- the safety margin
  does not depend on the unwritten action's details.""")

# ====================================================================================================
# VERDICT
# ====================================================================================================
print("="*100)
print(" LANE 3 VERDICT")
print("="*100)
print(f"""  (a) THE TAIL -- P6 IS ~80% DERIVED, NOT A FREE DIAL:
      * Mapping: eps_M = |S_M|/S_DE = 2y/Z_eff (Verlinde's exact coefficients, sympy-verified):
        HIGH-y = LARGE source strain. Crossover eps_M=1 at y_c = {yc_canon:.2f} (canonical) /
        {yc_alt:.2f} (alt) -- DERIVED, footing-invariant, parameter-free.
      * The det-class F fixed by the displacement match is SCALE-FREE: the tail canNOT come from F.
        It comes from Verlinde's own budget -- the crossover is FORCED; only its PROFILE is a choice:
          - CAP reading: DEAD (const g_D = cH/2, ~4.6 orders over EPM/Saturn).
          - THROTTLE reading T = min(1, S_DE/S_M): FORCES exact n = 1 >= n_min ~ 0.74-0.76;
            Saturn strict PASS x18-26 under, Mars x5e3, EPM x38, Neptune safe -- both footings;
            SPARC point-level (REAL data, benchmark asserted): ALIVE with ZERO penalty -- drms is
            in fact slightly NEGATIVE (-0.001 to -0.002 dex; within the non-diagnostic M/L band,
            not claimed as a preference); deep 0.982 EXACTLY intact; Q2 budget essentially
            unchanged (w_max {wmax['canonical'][0]:.3f} -> {wmax['canonical'][1]:.3f} canonical: +1-3% kernel shift, reported honestly).
          - HARD CUTOFF at y_c: monopole trivially safe; ALSO SPARC-ALIVE (drms ~ -0.002 both
            footings): even the sharpest profile costs nothing at SPARC -- the whole
            [n~0.75, hard-cut] window is open on the real fit.
      * Residual posit (P6'): 'depletion-not-cap' + the profile within the [n~0.75, hard] window.
        The LOCATION and the NECESSITY of the tail are no longer posits.
  (b) DIRECTIONAL EFE -- THE FALSIFIER IS LIVE AND DATA-IN-HAND, CURRENTLY UNDECIDED:
      det-class predicts nearly-isotropic galactic EFE (aligned RC asymmetry <= w x AQUAL's 1-4%,
      i.e. <~0.3-1%); Chae+ 2020-22 detections are AMPLITUDE-ONLY (angle-averaged/axisymmetric);
      no directional detection exists either way. KILL: aligned asymmetry at AQUAL amplitude
      (stack SPARC outer-RC asymmetry on Chae-II LSS g_ext vectors) => w~1 => Q2 wall returns
      at {1.0/wmax['canonical'][0]:.1f}-{1.0/wmax['alt'][0]:.1f}x ceiling => Branch B dead. Null at <0.5% => first empirical support for P5.
  (c) GW SECTOR -- SAFE BY ~25 ORDERS: shear sector = GR gravitons (2 polarizations, speed c);
      medium stresses move c_T by ~4 Lambda/k^2 ~ 1e-40 at LIGO frequencies (both footings);
      bulk phonon is matter-sector, not a metric polarization. Honest limit: no covariant action;
      the margin is robust to that (bounded by rho_DE c^2), the bulk-sector dynamics are not.""")
print("EXIT 0")
