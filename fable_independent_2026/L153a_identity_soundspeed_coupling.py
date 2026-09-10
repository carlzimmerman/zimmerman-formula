#!/usr/bin/env python3
"""
L153a -- THE FIELD-DUST'S SOUND SPEED IS NOT FREE:  c_s^2 = eps * c_ad^2,  eps = 2 c_Y Qbar / K_Q  (~ a^3)
=============================================================================================================
Object under test (L139 route 2, the surviving corner of L137-L139):
      L_dark = K(Q) - c_Y |D chi|^2 ,   Q = n^mu grad_mu chi  on the clock's foliation,  c_Y = const.
L138 established that its perturbation sound speed c_s^2 = 2 c_Y / K_QQ(a) is a "free function" that grows
as a^+3 for cosh/exp K -- and built the surviving corner on that.  L139 checked the BACKGROUND (dust) and the
HEALTH (ghost/gradient) but never the sector's response to GRAVITY.  This script computes that response.

WHAT IS COMPUTED (every load-bearing statement is a check that can fail):
  A1  Flat-space Noether currents for L(chi_t, chi_x) = K(chi_t) - c_Y chi_x^2, verified conserved on-shell.
      The energy flux is -2 c_Y chi_t chi_x, the momentum density is -K_Q chi_x: the Lorentz-violating theory
      transports ENERGY and MOMENTUM at different rates.  Their ratio is 2 c_Y Q / K_Q, and equals 1 iff
      c_Y = K_Q/(2Q) -- which is exactly the Lorentz-invariant k-essence P(X) structure.
  A2  Coupling to gravity through the lapse (Q = chi_dot / N, N = 1 + Phi): the linearised density equation is
          d^2(dn)/dt^2 - c_s^2 lap(dn) = 2 c_Y Qbar lap(Phi),
      so the dust falls into a potential well with acceleration -eps grad(Phi), eps = 2 c_Y Qbar / K_Q, while it
      GRAVITATES with its full energy density.  Identity (any K, any c_Y):  c_s^2 = eps * c_ad^2, with
      c_ad^2 = K_Q / (Qbar K_QQ) the background (adiabatic) sound speed.
  A3  Expanding background: for a gradient coefficient C(Q) ~ K_Q^p the growth equation is
          delta'' + (3p - 1) H delta' = eps 4 pi G rho_d delta - c_s^2 k^2 delta / a^2,   eps ~ a^{3(1-p)}.
      p = 1 is CDM (friction +2H, eps = 1, c_s = c_ad).  L139's constant c_Y is p = 0: friction -H, eps ~ a^3.
  A4  Numbers for SZ21's cosh K: c_ad^2(a), eps(a), c_s^2(a) along the background.
  A5  Growth ODE (k = 0.06 Mpc^-1, the third-peak scale): for p = 0 no normalisation of eps is CDM-like at both
      recombination and today; the matter-era growth index differs from CDM's for every eps_0.
      For p = 1 (the EP-consistent repair) the sector IS CDM up to the constant c_ad Jeans cut, and the late-time
      suppression at k = 0.1-1 Mpc^-1 is tabulated (an LSS diagnostic, not adjudicated here).
  A6  The static nonlinear response: n = K_Q(Qbar(1 - Phi)) => rho_d/rho_bar = exp(|Phi|/c_ad^2) for cosh K in
      its large-Z regime: the hydrostatic atmosphere has temperature c_ad^2, NOT c_s^2 (used by L153b-d).

POLARITY: each check ASSERTS a statement; PASS = true.  No check uses a literal True.
"""
import sympy as sp
import numpy as np
import json, os, sys, time
from scipy.integrate import solve_ivp

T0 = time.time(); FAILS = []; N = [0]
def check(name, ok, detail=""):
    N[0] += 1; ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    if not ok: FAILS.append(name)
    print(f"  [{tag}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__))
RES = {}

C_KMS = 299792.458; C_SI = 2.99792458e8; G = 6.674e-11; MPC = 3.0857e22
h = 0.674; H0 = h*100e3/MPC; OM, OB, OR = 0.315, 0.049, 9.24e-5; OD = OM-OB; OL = 1-OM-OR
RHO_CRIT = 3*H0**2/(8*np.pi*G); RHO_D0 = OD*RHO_CRIT
A_REC = 1/1090.

# =====================================================================================================
sec("A1 -- FLAT SPACE: energy and momentum are transported at DIFFERENT rates (Noether, on-shell)")
# =====================================================================================================
t, x = sp.symbols('t x', real=True)
cY = sp.symbols('c_Y', positive=True)
chi = sp.Function('chi')(t, x)
u, w = sp.symbols('u w', real=True)            # u = chi_t, w = chi_x
Kf = sp.Function('K')
L = Kf(u) - cY*w**2
Lu, Lw = sp.diff(L, u), sp.diff(L, w)
sub = {u: sp.diff(chi, t), w: sp.diff(chi, x)}
# canonical stress tensor T^mu_nu = dL/d(d_mu chi) d_nu chi - delta^mu_nu L
Ttt = (Lu*u - L).subs(sub)          # energy density
Txt = (Lw*u).subs(sub)              # energy flux
Ttx = (Lu*w).subs(sub)              # -(momentum density)
Txx = (Lw*w - L).subs(sub)          # momentum flux
EOM = sp.diff(Lu.subs(sub), t) + sp.diff(Lw.subs(sub), x)     # d_t(dL/du) + d_x(dL/dw) = 0
dE = sp.expand(sp.diff(Ttt, t) + sp.diff(Txt, x))
dP = sp.expand(sp.diff(Ttx, t) + sp.diff(Txx, x))
resE = sp.simplify(dE - sp.expand(EOM*sp.diff(chi, t)))
resP = sp.simplify(dP - sp.expand(EOM*sp.diff(chi, x)))
check("A1-1  energy conservation d_t(u K_u - K + c_Y w^2) + d_x(-2 c_Y u w) = 0 holds ON-SHELL (residual is "
      "exactly EOM * chi_t)", resE == 0, f"residual = {resE}")
check("A1-2  momentum conservation d_t(-K_u w) + d_x(...) = 0 holds ON-SHELL (residual is exactly EOM * chi_x)",
      resP == 0, f"residual = {resP}")
energy_flux = Txt; mom_density = -Ttx
ratio = sp.simplify(energy_flux/mom_density)
print(f"  energy density   = {sp.simplify(Ttt)}")
print(f"  energy flux      = {energy_flux}")
print(f"  momentum density = {mom_density}")
print(f"  energy flux / momentum density = {ratio}")
Qs = sp.symbols('Q', positive=True)
ratio_Q = ratio.subs({sp.diff(chi, t): Qs, sp.diff(chi, x): w})
check("A1-3  the ratio (energy flux)/(momentum density) is 2 c_Y Q / K_Q(Q): T^{0i} != T^{i0} -- energy and "
      "momentum move at different speeds unless c_Y = K_Q/(2Q)",
      sp.simplify(ratio_Q - 2*cY*Qs/sp.Derivative(Kf(Qs), Qs)) == 0, f"ratio = {ratio_Q}")
# Lorentz-invariant control: K(u) = P(u^2/2), c_Y -> P'(u^2/2)/2  ==> ratio = 1 identically
Pf = sp.Function('P'); X = sp.symbols('X', positive=True)
K_LI = Pf(u**2/2); cY_LI = sp.Rational(1, 2)*sp.diff(Pf(X), X).subs(X, u**2/2)
ratio_LI = sp.simplify(2*cY_LI*u/sp.diff(K_LI, u))
check("A1-4  CONTROL: for a Lorentz-invariant k-essence P(X), X = (u^2 - w^2)/2, i.e. K = P(u^2/2) and "
      "c_Y = P_X/2, the ratio is exactly 1 (symmetric T^{mu nu}); the mismatch IS the Lorentz violation",
      ratio_LI == 1, f"ratio_LI = {ratio_LI}")

# =====================================================================================================
sec("A2 -- GRAVITY THROUGH THE LAPSE: the sector falls with acceleration -eps grad(Phi), eps = 2 c_Y Qbar/K_Q")
# =====================================================================================================
Phi = sp.Function('Phi')(t, x)
psi = sp.Function('psi')(t, x)
Qb, KQ, KQQ, e = sp.symbols('Qbar K_Q K_QQ epsilon', positive=True)
# action density N [K(Q) - c_Y (chi_x)^2],  Q = chi_t/N,  N = 1 + Phi.  EOM: d_t(K_Q(Q)) - 2 c_Y d_x(N chi_x) = 0
Qexpr = (Qb + e*sp.diff(psi, t))/(1 + e*Phi)
KQ_lin = KQ + KQQ*(Qexpr - Qb)                          # K_Q expanded about Qbar
eom = sp.diff(KQ_lin, t) - 2*cY*sp.diff((1 + e*Phi)*e*sp.diff(psi, x), x)
eom1 = sp.expand(sp.series(eom, e, 0, 2).removeO()).coeff(e, 1)
dn = sp.expand(sp.series(KQ_lin - KQ, e, 0, 2).removeO()).coeff(e, 1)      # linear charge perturbation
print(f"  O(eps) field equation : {eom1} = 0")
print(f"  delta n               : {dn}")
# eliminate psi:  d_t^2 dn  =  K_QQ (psi_ttt - Qbar Phi_tt) ;  from eom1: K_QQ psi_tt = 2 c_Y psi_xx + K_QQ Qbar Phi_t
psi_tt = sp.solve(eom1, sp.diff(psi, t, 2))[0]
dn_tt = sp.diff(dn, t, 2).subs(sp.diff(psi, t, 3), sp.diff(psi_tt, t))
target = (2*cY/KQQ)*sp.diff(dn, x, 2) + 2*cY*Qb*sp.diff(Phi, x, 2)
check("A2-1  the linearised density equation is  d_t^2(dn) - (2 c_Y/K_QQ) d_x^2(dn) = 2 c_Y Qbar d_x^2(Phi): "
      "sound speed c_s^2 = 2 c_Y/K_QQ (L138's) AND a gravitational source with coefficient 2 c_Y Qbar",
      sp.simplify(sp.expand(dn_tt - target)) == 0, f"residual = {sp.simplify(sp.expand(dn_tt - target))}")
# a standard fluid of density rho = Qbar n obeys d_t^2(drho) - c_s^2 lap(drho) = rho_bar lap(Phi)  (Phi = Phi_N/c^2)
eps_def = 2*cY*Qb/KQ
cs2 = 2*cY/KQQ; cad2 = KQ/(Qb*KQQ)
check("A2-2  dividing by the background density Qbar K_Q: the source is eps * rho_bar lap(Phi) with "
      "eps = 2 c_Y Qbar/K_Q -- the sector's INERTIAL response to gravity is eps times its GRAVITATIONAL mass",
      sp.simplify(2*cY*Qb*Qb/(Qb*KQ) - eps_def) == 0, f"eps = {eps_def}")
check("A2-3  IDENTITY for any K and any c_Y:  c_s^2 = eps * c_ad^2,  c_ad^2 = K_Q/(Qbar K_QQ) = dP/drho of "
      "the background.  A 'free' sound speed is bought with a non-universal gravitational coupling.",
      sp.simplify(cs2 - eps_def*cad2) == 0, f"c_s^2 - eps c_ad^2 = {sp.simplify(cs2 - eps_def*cad2)}")
check("A2-4  eps = 1 (equivalence principle in the dark sector, the condition for CDM-like infall) FORCES "
      "c_Y = K_Q/(2 Qbar) -- the Lorentz-invariant k-essence value of A1-4 -- and hence c_s = c_ad: the "
      "sound speed is then LOCKED to the background equation of state (L138 B2), not free",
      sp.simplify(sp.solve(sp.Eq(eps_def, 1), cY)[0] - KQ/(2*Qb)) == 0,
      f"c_Y(eps=1) = {sp.solve(sp.Eq(eps_def, 1), cY)[0]}")

# =====================================================================================================
sec("A3 -- EXPANDING BACKGROUND: the one-parameter family C(Q) ~ K_Q^p; only p = 1 is CDM")
# =====================================================================================================
# comoving charge I_0 = a^3 K_Q(Qbar) is exactly conserved.  Fourier mode k (comoving).  Derivation (A2 in an
# FRW background, gradient coefficient C(t) = c_Y (a^3 K_Q)^{...}): with delta = dn_comoving/I_0,
#     I_0 delta_dot = -2 C(t) a k^2 psi ,      psi_dot = I_0 delta/(a^3 K_QQ) + Qbar Phi .
ts = sp.symbols('t', positive=True)
a = sp.Function('a')(ts); Cf = sp.Function('C')(ts); dl = sp.Function('delta')(ts); ps = sp.Function('psi')(ts)
Ph = sp.Function('Phi')(ts); I0, kk, KQQt = sp.symbols('I_0 k K_QQ', positive=True)
Hs = sp.diff(a, ts)/a
psi_dot = I0*dl/(a**3*KQQt) + Qb*Ph
delta_dot = -2*Cf*a*kk**2*ps/I0
delta_ddot = sp.diff(delta_dot, ts).subs(sp.diff(ps, ts), psi_dot)
# rewrite:  delta'' - (Cdot/C + H) delta'  = -(2 C k^2/(a^2 K_QQ)) delta - (2 C Qbar a/I_0) k^2 Phi
lhs = delta_ddot - (sp.diff(Cf, ts)/Cf + Hs)*delta_dot
rhs = -(2*Cf*kk**2/(a**2*KQQt))*dl - (2*Cf*Qb*a/I0)*kk**2*Ph
check("A3-1  the FRW density equation is  delta'' - (Cdot/C + H) delta' = -c_s^2 k^2 delta/a^2 - "
      "(2 C Qbar a/I_0) k^2 Phi   (exact rearrangement, verified symbolically)",
      sp.simplify(sp.expand(lhs - rhs)) == 0, f"residual = {sp.simplify(sp.expand(lhs - rhs))}")
p = sp.symbols('p', real=True)
# C = c_Y (K_Q/K_Q0)^p with K_Q = I_0/a^3  =>  Cdot/C = -3 p H ;  friction coefficient = -(Cdot/C + H) = (3p - 1) H
fric = sp.simplify(-(-3*p*Hs + Hs)/Hs)
check("A3-2  for C ~ K_Q^p (= a^{-3p}) the friction coefficient is (3p - 1) H: p = 1 gives CDM's +2H, "
      "L139's constant c_Y (p = 0) gives -H (an anti-damped, non-diluting charge flux)",
      sp.simplify(fric - (3*p - 1)) == 0, f"friction/H = {fric}")
# Poisson: k^2 Phi = -4 pi G a^2 rho_d delta  =>  gravity term = (2 C Qbar a^3/I_0) 4 pi G rho_d delta = eps 4 pi G rho_d delta
eps_p = 2*cY*Qb*a**3/I0 * (a**3)**(-p) * sp.Symbol('K_Q0')**(-p) * sp.Symbol('I_0')**p   # ~ a^{3 - 3p}
check("A3-3  the gravitational coupling scales as eps ~ a^{3(1-p)}: constant for p = 1 only; for p = 0 it "
      "changes by (1+z_rec)^3 = 1.3e9 between recombination and today",
      abs(float(sp.log(eps_p.subs({a: 2})/eps_p.subs({a: 1})).subs(p, 0)/sp.log(2)) - 3) < 1e-12
      and abs(float(sp.log(eps_p.subs({a: 2})/eps_p.subs({a: 1})).subs(p, 1)/sp.log(2))) < 1e-12,
      f"(1+z_rec)^3 = {(1/A_REC)**3:.3e}")
check("A3-4  p = 1 reproduces the CDM growth equation EXACTLY: delta'' + 2H delta' = 4 pi G rho_d delta - "
      "c_ad^2 k^2 delta/a^2 (with c_s = c_ad); this is the Lorentz-invariant k-essence dust (Scherrer 2004)",
      sp.simplify(fric.subs(p, 1) - 2) == 0 and sp.simplify((2*cY*(KQ/(2*Qb))/cY)/KQQ*Qb*KQQ/KQ - 1) == 0,
      "friction +2H, eps = 1, c_s^2 = c_ad^2")

# =====================================================================================================
sec("A4 -- NUMBERS on SZ21's cosh K:  c_ad^2(a), eps(a), c_s^2(a)")
# =====================================================================================================
# K = 2 K_2 Z_0^2 [cosh Z - 1], Z = (Q - Q_0)/Z_0:  K_Q = 2 K_2 Z_0 sinh Z = I_0/a^3,  K_QQ = 2 K_2 cosh Z
# => sinh Z(a) = (a_t/a)^3 with a_t^3 = I_0/(2 K_2 Z_0);  c_ad^2 = (Z_0/Qbar) tanh Z(a)  (exact)
def Z_of_a(av, a_t): return np.arcsinh((a_t/av)**3)
def cad2_cosh(av, a_t, cad2_inf): return cad2_inf*np.tanh(Z_of_a(av, a_t))          # cad2_inf = Z_0/Q_0
def eps_p0(av, eps0): return eps0*av**3                                              # constant c_Y
avals = np.array([A_REC, 1e-2, 1e-1, 1/3., 1.0])
print(f"  {'a':>9} | {'c_ad^2/(Z0/Q0), a_t=0.3':>24} {'a_t=1.27':>10} {'a_t=3':>8} | {'eps (p=0, eps(1)=1)':>20} "
      f"{'eps (p=0, eps(rec)=1)':>22}")
for av in avals:
    print(f"  {av:9.5f} | {np.tanh(Z_of_a(av,0.3)):24.4f} {np.tanh(Z_of_a(av,1.27)):10.4f} {np.tanh(Z_of_a(av,3.)):8.4f} "
          f"| {eps_p0(av,1.0):20.3e} {eps_p0(av,1/A_REC**3):22.3e}")
check("A4-1  cosh K: c_ad^2 = (Z_0/Q_0) tanh Z(a) is CONSTANT to <1% for a < a_t/2.4 and falls as a^-3 "
      "beyond a_t (L138 B2-3/B2-4 reproduced); a_t >= 1.27 keeps c_ad within 10% of its plateau today",
      abs(np.tanh(Z_of_a(0.3/2.4, 0.3)) - 1) < 0.01 and abs(np.tanh(Z_of_a(1.0, 1.27)) - 0.9) < 0.02,
      f"tanh Z at a = a_t/2.4: {np.tanh(Z_of_a(0.3/2.4,0.3)):.4f};  at a=1 with a_t=1.27: {np.tanh(Z_of_a(1.0,1.27)):.3f}")
check("A4-2  with constant c_Y the coupling eps = eps(1) a^3 spans 1.3e9 between recombination and today: "
      "normalised to fall like CDM today it is INERT at recombination (eps = 7.7e-10); normalised to CDM at "
      "recombination it is 1.3e9 x CDM today",
      abs(eps_p0(A_REC, 1.0)/A_REC**3 - 1) < 1e-12 and eps_p0(1.0, 1/A_REC**3) > 1e9,
      f"eps(rec | eps(1)=1) = {eps_p0(A_REC,1.0):.2e};  eps(1 | eps(rec)=1) = {eps_p0(1.0,1/A_REC**3):.2e}")
c_s_today = 300.0
cs2_today = (c_s_today/C_KMS)**2
print(f"\n  L138's corner: c_s(today) = {c_s_today:.0f} km/s with c_s^2 ~ a^3 (p = 0).  By the identity, "
      f"c_ad^2 = c_s^2/eps:")
for eps1 in (1.0, 1e-3, 1e-6, 1e-9):
    cad = np.sqrt(cs2_today/eps1)*C_KMS
    print(f"    eps(today) = {eps1:8.1e}  =>  c_ad = {cad:12.1f} km/s  (eps(rec) = {eps1*A_REC**3:.1e})")
check("A4-3  the running corner cannot be normalised into existence: c_ad = c_s(today)/sqrt(eps(today)); "
      "eps(today) = 1 gives c_ad = 300 km/s but eps(rec) = 7.7e-10; eps(rec) = 1 requires eps(today) = 1.3e9 "
      "and c_ad = 0.008 km/s (a cold dust with a 300 km/s dynamical sound speed and 1e9 x CDM infall)",
      abs(np.sqrt(cs2_today/1.0)*C_KMS - 300) < 1e-6 and np.sqrt(cs2_today/(1/A_REC**3))*C_KMS < 0.01)

# =====================================================================================================
sec("A5 -- LINEAR GROWTH ODE at the third-peak scale k = 0.06 Mpc^-1 (and the LSS diagnostic for p = 1)")
# =====================================================================================================
def E2(av): return OR/av**4 + OM/av**3 + OL
def dlnH_dlna(av):
    return 0.5*(-4*OR/av**4 - 3*OM/av**3)/E2(av)
def _S_A(av, k, p, eps0, cad2_inf, a_t):
    """source S and friction A of  delta'' + A delta' = S delta  (primes = d/dln a), with c_s^2 = eps c_ad^2."""
    eps = eps0*av**(3*(1-p))
    cs2 = eps*cad2_cosh(av, a_t, cad2_inf)
    H2 = H0**2*E2(av)
    S = eps*1.5*OD/av**3/E2(av) - cs2*C_SI**2*k**2/(av**2*H2)
    A = dlnH_dlna(av) + (3*p - 1)           # delta'' + A delta' = S delta, primes = d/dln a
    return S, A
def grow_log(k_mpc, p, eps0, cad2_inf, a_t, a_i=1e-4, a_f=1.0, f0=1.0):
    """Riccati form for monotonic modes: f = dln(delta)/dln(a), f' = S - f^2 - A f, ln(delta) = int f.
       Never overflows, so the explosive normalisations can be followed.  Returns sol with y = [f, ln delta]."""
    k = k_mpc/MPC
    def rhs(lna, y):
        S, A = _S_A(np.exp(lna), k, p, eps0, cad2_inf, a_t); f = y[0]
        return [S - f*f - A*f, f]
    return solve_ivp(rhs, [np.log(a_i), np.log(a_f)], [f0, 0.0], rtol=1e-8, atol=1e-10,
                     dense_output=True, method='Radau')
def grow_lin(k_mpc, p, eps0, cad2_inf, a_t, a_i=1e-4, a_f=1.0, f0=1.0):
    """linear form for bounded (possibly oscillating) modes.  Returns sol with y = [delta, delta']."""
    k = k_mpc/MPC
    def rhs(lna, y):
        S, A = _S_A(np.exp(lna), k, p, eps0, cad2_inf, a_t)
        return [y[1], S*y[0] - A*y[1]]
    return solve_ivp(rhs, [np.log(a_i), np.log(a_f)], [1.0, f0], rtol=1e-8, atol=1e-12,
                     dense_output=True, method='LSODA')
cad2_ref = (300.0/C_KMS)**2
# CDM control: p = 1, eps0 = 1, c_ad -> 0
cdm = grow_log(0.06, 1.0, 1.0, 1e-30, 10.0)
ln_cdm_rec = cdm.sol(np.log(A_REC))[1]; ln_cdm_1 = cdm.sol(0.0)[1]
print(f"  CDM control (p=1, eps=1, c_ad->0), k=0.06: delta(rec)/delta(a_i) = {np.exp(ln_cdm_rec):.3f}, "
      f"delta(1)/delta(rec) = {np.exp(ln_cdm_1-ln_cdm_rec):.1f}")
slope_cdm = cdm.sol(np.log(0.1))[0]
# only the dust (Omega_d = 0.266 of Omega_m) clusters in this one-fluid control, so the matter-era index is the
# analytic root of f^2 + (2 + dlnH/dlna) f = (3/2) Omega_d(a), not exactly 1
_A = 2 + dlnH_dlna(0.1); _S = 1.5*OD/0.1**3/E2(0.1)
f_expected = (-_A + np.sqrt(_A**2 + 4*_S))/2
check("A5-0  CONTROL: the integrator reproduces the analytic dust-only growth index at a = 0.1 to <1% and a "
      "delta(1)/delta(rec) of order (1+z_rec)^0.9 x (Lambda suppression)",
      abs(slope_cdm/f_expected - 1) < 0.01 and 200 < np.exp(ln_cdm_1-ln_cdm_rec) < 1500,
      f"index = {slope_cdm:.4f} vs analytic {f_expected:.4f}; delta(1)/delta(rec) = {np.exp(ln_cdm_1-ln_cdm_rec):.0f}")

print(f"\n  p = 0 (L139's constant c_Y), c_ad^2 -> c_s^2(today)/eps(today), a_t = 10 (pure a^3 regime):")
print(f"  {'eps(today)':>11} {'eps(rec)':>10} | {'ln d(rec)/d_i':>13} {'ln vs CDM':>10} | {'ln d(1)/d(rec)':>15} "
      f"{'ln vs CDM':>10} | {'MD index':>9}", flush=True)
P0 = {}
for eps1 in (1.0, 1e-3, 1e-6, 1e-9, 1/A_REC**3):
    cad2 = cs2_today/eps1
    s = grow_log(0.06, 0.0, eps1, cad2, 10.0)
    lrec = s.sol(np.log(A_REC))[1]; l1 = s.sol(0.0)[1]; idx = s.sol(np.log(0.1))[0]
    P0[eps1] = dict(ln_rec_vs_cdm=lrec-ln_cdm_rec, ln_late_vs_cdm=(l1-lrec)-(ln_cdm_1-ln_cdm_rec), idx=idx)
    print(f"  {eps1:11.1e} {eps1*A_REC**3:10.1e} | {lrec:13.3f} {lrec-ln_cdm_rec:+10.3f} | {l1-lrec:15.3e} "
          f"{(l1-lrec)-(ln_cdm_1-ln_cdm_rec):+10.3e} | {idx:9.3f}", flush=True)
s_frozen = grow_log(0.06, 0.0, 1.0, cs2_today, 10.0, f0=0.0)
print(f"  {'1.0e+00 (f0=0)':>22} | {s_frozen.sol(np.log(A_REC))[1]:13.3f} {s_frozen.sol(np.log(A_REC))[1]-ln_cdm_rec:+10.3f} | "
      f"{s_frozen.sol(0.0)[1]-s_frozen.sol(np.log(A_REC))[1]:15.3e}   <- no initial velocity: FROZEN, no infall", flush=True)
ok_p0 = all((abs(v['ln_rec_vs_cdm']) > np.log(1.1)) or (abs(v['ln_late_vs_cdm']) > np.log(1.5)) for v in P0.values())
ok_p0 = ok_p0 and abs(s_frozen.sol(np.log(A_REC))[1]) < 1e-3
check("A5-1  p = 0: for EVERY normalisation eps(today) in [7.7e-10 .. 1.3e9] the sector fails to track CDM at "
      "recombination (ratio off by >10%) OR after it (late growth off by >50%); there is no eps_0 that is "
      "CDM-like at both epochs", ok_p0)
idx_small = P0[1.0]['idx']
check("A5-2  p = 0 with eps(rec) << 1 either stays FROZEN (no initial velocity: no infall at all) or grows "
      "KINEMATICALLY as a^{5/2} in the matter era from its initial velocity (the -H anti-friction: the charge "
      "flux does not dilute), never gravitationally as a^1: the potential it sources grows as a^{3/2} instead "
      "of staying constant -- not CDM phenomenology at any amplitude",
      abs(idx_small - 2.5) < 0.05, f"matter-era index = {idx_small:.3f} (CDM 1.000; dust-only analytic {f_expected:.3f})")
big = P0[1/A_REC**3]
check("A5-3  p = 0 with eps(rec) = 1: the sector is NOT CDM at recombination either (kinematic a^3 growth in "
      "the radiation era puts it >5x above CDM) and then grows by e^{>1e3} more than CDM by today at "
      "k = 0.06 Mpc^-1 -- structure explodes",
      abs(big['ln_rec_vs_cdm']) > np.log(1.5) and big['ln_late_vs_cdm'] > 1e3,
      f"ln[d(rec)/CDM] = {big['ln_rec_vs_cdm']:+.3f}, ln[late growth/CDM] = {big['ln_late_vs_cdm']:.3e}")

print(f"\n  p = 1 (EP-consistent repair: c_s = c_ad = const, cosh with a_t = 1.27), growth relative to CDM:")
print(f"  {'c_ad km/s':>10} | " + " ".join(f"{'k=%.2f' % k:>9}" for k in (0.06, 0.1, 0.2, 0.5, 1.0)) + "   (delta(1)/delta_CDM(1))", flush=True)
P1 = {}; P1REC = {}
for cad in (150., 300., 450., 537.):
    row = []; rrec = []
    for k in (0.06, 0.1, 0.2, 0.5, 1.0):
        s = grow_lin(k, 1.0, 1.0, (cad/C_KMS)**2, 1.27); c = grow_lin(k, 1.0, 1.0, 1e-30, 10.0)
        row.append(s.sol(0.0)[0]/c.sol(0.0)[0]); rrec.append(s.sol(np.log(A_REC))[0]/c.sol(np.log(A_REC))[0])
    P1[cad] = row; P1REC[cad] = rrec
    print(f"  {cad:10.0f} | " + " ".join(f"{r:9.4f}" for r in row) + f"     [at recombination, k=0.06: {rrec[0]:.4f}]", flush=True)
check("A5-4  p = 1 (c_s = c_ad constant) tracks CDM to <1% at recombination at the third-peak scale for every "
      "c_ad <= 537 km/s -- the constant-c_s GDM regime that arXiv:1601.05097 bounds -- so the CMB side is "
      "carried by that published bound",
      all(abs(P1REC[c][0] - 1) < 0.01 for c in P1REC), "rec ratios: " + ", ".join(f"{P1REC[c][0]:.4f}" for c in P1REC))
check("A5-5  but by today the same dust has LOST its power at k >= 0.5 Mpc^-1 (|growth/CDM| < 0.1 at 300 km/s) "
      "and is suppressed 5-15% even at k = 0.06: the LSS side is NOT carried by the Planck-only bound and is "
      "left open here (it needs the baryon+MOND growth, which L142 finds overshooting on its own)",
      abs(P1[300.][3]) < 0.1 and 0.85 < P1[300.][0] < 0.96 and abs(P1[537.][2]) < 0.2,
      f"c_ad=300: k=0.06 {P1[300.][0]:.3f}, k=0.2 {P1[300.][2]:.3f}, k=0.5 {P1[300.][3]:.3f}")

# =====================================================================================================
sec("A6 -- THE STATIC NONLINEAR RESPONSE: the atmosphere temperature is c_ad^2 (independent of c_Y)")
# =====================================================================================================
# static: psi_dot = 0  =>  n(x) = K_Q(Qbar (1 - Phi))  (exact, from the EOM with all time derivatives zero)
Zb = 10.0; Z0_over_Q = 1e-6                       # large-Z regime; c_ad^2 = Z_0/Qbar (units of c^2)
def n_over_nbar(Phi_over_c2):                     # cosh K, exact
    return np.sinh(Zb - Phi_over_c2/Z0_over_Q)/np.sinh(Zb)
phis = -np.array([0.5, 1.0, 2.0, 4.0])*Z0_over_Q   # wells of depth 0.5..4 c_ad^2
ex = n_over_nbar(phis); pred = np.exp(-phis/Z0_over_Q)
check("A6-1  for cosh K in its large-Z regime the exact static response n/nbar = sinh(Zbar + |Phi|/c_ad^2)/"
      "sinh(Zbar) equals exp(|Phi|/c_ad^2) to <1e-8 -- an ISOTHERMAL atmosphere at temperature c_ad^2, with "
      "NO dependence on c_Y (hence none on L138's c_s)",
      np.all(np.abs(ex/pred - 1) < 1e-8), "max |ratio-1| = %.1e" % np.max(np.abs(ex/pred - 1)))
# and the linearised static response reproduces the Helmholtz mass term: drho = -K_QQ Qbar^2 Phi = -rho_bar Phi/c_ad^2
cad2_sym = KQ/(Qb*KQQ)
mu2_over = sp.simplify((KQQ*Qb**2)/(Qb*KQ)*cad2_sym)     # (K_QQ Qbar^2)/(rho_bar) * c_ad^2 -> 1
check("A6-2  its linearisation is drho_d = -rho_bar Phi/c_ad^2, i.e. Poisson becomes (lap + mu^2) Phi = 4 pi G "
      "rho_b with mu^2 = 4 pi G rho_bar_d/(c_ad^2 c^2): the AeST Helmholtz term IS the linear static response "
      "of the field-dust, and mu^-1 is the Jeans length of the ambient dust at sound speed c_ad (used in L153c)",
      mu2_over == 1, f"(K_QQ Qbar^2 c_ad^2)/rho_bar = {mu2_over}")
mu_inv = np.sqrt((300e3)**2/(4*np.pi*G*RHO_D0))/MPC
print(f"  mu^-1(c_ad = 300 km/s, ambient rho_d = cosmic mean {RHO_D0:.3e} kg/m^3) = {mu_inv:.2f} Mpc")

# =====================================================================================================
sec("VERDICT (A)")
# =====================================================================================================
print(f"""
  1. THE SOUND SPEED OF THE L139 FIELD-DUST IS NOT A FREE FUNCTION.  For L = K(Q) - c_Y|D chi|^2 on a slaved
     foliation, the identity  c_s^2 = eps c_ad^2  holds for every K and every c_Y, where eps = 2 c_Y Qbar/K_Q
     is the ratio of the sector's inertial response to its gravitational mass.  L138's a^+3 running of c_s^2
     (cosh/exp K, constant c_Y) IS an a^+3 running of eps: the dust does not fall into potential wells at
     recombination (eps = 7.7e-10 if it falls normally today) or falls 1.3e9 x too hard today (if it is CDM at
     recombination).  The velocity lemma's replacement was bought with an equivalence-principle violation of
     nine orders of magnitude across the CMB-to-today baseline.  L138's corner, AS FORMULATED, IS DEAD.
  2. THE ONLY EP-CONSISTENT MEMBER OF THE FAMILY IS p = 1: c_Y -> K_Q/(2 Qbar), which is the Lorentz-invariant
     k-essence structure; then c_s = c_ad, constant for cosh K below its turnover a_t (a_t >= 1.27 required).
     That sector is CDM up to a CONSTANT sound speed -- exactly the constant-c_s GDM of arXiv:1601.05097.
     The foliation buys nothing: this repaired sector does not need it.
  3. FOR THE NONLINEAR QUESTION (L153b-d) the equilibrium temperature of the dust in any static well is c_ad^2,
     not c_s^2, and for cosh K it is a single constant.  So the crux the brief names -- 'material fell in early
     and was pressurised later' -- does not arise: the atmosphere temperature never ran.
""")
RES.update(dict(identity="c_s^2 = eps c_ad^2, eps = 2 c_Y Qbar/K_Q", eps_span=(1/A_REC)**3,
                p0=[dict(eps_today=k, ln_rec_vs_cdm=v['ln_rec_vs_cdm'], ln_late_vs_cdm=v['ln_late_vs_cdm'],
                         md_index=v['idx']) for k, v in P0.items()],
                p1_growth_ratio={str(k): v for k, v in P1.items()}, p1_rec_ratio={str(k): v for k, v in P1REC.items()},
                mu_inv_300_Mpc=mu_inv,
                a_t_min_for_constant_cad=1.27, checks_total=N[0], checks_failed=len(FAILS)))
with open(os.path.join(HERE, "L153a_results.json"), "w") as f: json.dump(RES, f, indent=1, default=float)
print("=" * 112)
print(f"L153a COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.   [{time.time()-T0:.1f}s]")
if FAILS: print("FAILED: " + "; ".join(FAILS)); sys.exit(1)
print("=" * 112)
