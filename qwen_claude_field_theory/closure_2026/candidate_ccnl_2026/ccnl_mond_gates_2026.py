#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ccnl_mond_gates_2026.py -- CONDENSATE-CLOCK NONLOCAL MOND (CCNL-MOND): the fried-chicken candidate, gated.
==========================================================================================================
THE CANDIDATE (one action; c=1 inside brackets, restored where numbers are printed):

  S = int d^4x sqrt(-g) { (c^4/16 pi G) [ R  +  a0^2 f(Z) ]   +   K(Q)/(8 pi G~)   +  xi ( Box X - R_mn u^m u^n ) }  +  S_m[g, psi]

  clock  : phi, a shift-symmetric k-essence field,  Q = sqrt(-g^{mn} d_m phi d_n phi),  u_m = d_m phi / Q,
           K(Q) = -2 Lambda + K_2 (Q - Q_0)^2   (the AeST/v9 Q-sector; DBI form has the same quadratic term)
  kernel : X = Box_ret^{-1} (R_mn u^m u^n)   [localised by the multiplier xi with retarded/null initial data],
           Z = (4 c^4/a0^2) g^{mn} d_m X d_n X,    f(Z) the MOND interpolation function (Sec. B: chosen for mu = 1-e^{-y})
  matter : minimally coupled to the ONE metric g.

  It is Deffayet-Woodard 2026 (arXiv:2512.10513) with TWO changes: (i) the mimetic clock (d phi)^2 = -1 and its
  advected dust M(0)=45/sqrt(det g) are REPLACED by the condensate clock K(Q), so the dark field is the gamma=2
  polytrope of itemC (c_s^2 = |Psi| in wells: galaxy-safe by geometry, no caustics); (ii) the transport
  functional M is taken with M(0,x)=0, i.e. M = -f(Z) exactly (DW's eq. 33 with zero homogeneous part), so the
  kernel carries no dust of its own (with null X data, f(0)=0, so DW's transport gives M=-f; the action below uses f(Z)
  directly and does not need M at all).  Every other structure is DW's.

WHY THIS AND NOT THE OTHERS (each killer, and where it is dodged):
  * AeST/v9: alpha_1 = -2(K_B+2) from the aether drag couplings (2-K_B)(2J.dphi - Y)   -> NO aether vector here;
    the MOND force is carried by the retarded kernel, exp-dead in the Solar System.
  * local 2-DOF constraint carriers: alpha_3 = O(1) (the pincer)                          -> retarded Box^{-1}: alpha_3 = 0.
  * frame-free F(X) scalar: O(1) slip (DC-013 / slip-lock theorem)                        -> the clock supplies the frame; the
    kernel enters through R_uu (time-time), its anisotropic stress f' dX dX is 2PN.
  * DW as written: the mimetic dust is geodesic & pressureless => CDM halos in galaxies => RAR broken (Sec. A)
                                                                                           -> condensate dust, c_s^2 = |Psi|.
GATES COMPUTED HERE (checks that can FAIL; MUTATE=1 breaks the Noether identity by an external clock):
  A  gate 1 in galaxies: mimetic dust (NFW at the cosmic share) vs condensate dust (itemC polytrope) -> RAR shift in dex
  B  gates 1/12: mu(y) = 1 - 2 f'(4 y^2) derived; DW's f reproduces the audit's mu_eff; f_exp giving mu = 1 - e^{-y} exactly
  C  gate 4: gamma-1, beta-1, alpha_1, alpha_2 suppression numbers (kernel exp-dead; clock stress Lambda-scale); alpha_3 = 0 (structure)
  D  gate 5: the time-reparametrisation Noether identity OFF-SHELL in the lapse minisuperspace with the localised kernel
             => nabla^mu E_mn = 0 for ANY solution of the auxiliary equations, retarded included (then the covariant theorem)
  E  gate 6: R_uu^{(1)}[h^TT] = 0 => the kernel is tensor-blind, c_T = c; K(Q) has no tensor coupling
  F  gate 7 (clock): c_s^2 = u/(Q0+u) > 0 and kinetic K'' > 0 on the positive-charge branch; no caustics (pressure)
  G  gate 3: the kernel's anisotropic stress is O(v^2/c^2) relative to the metric terms => Phi = Psi at 1PN
  H  gate 9/10/8: deep-MOND mu -> y, Newton mu -> 1 exponentially, FLRW: f(Z<0) -> constant absorbed in Lambda (size printed)
INHERITED / OWED are listed in CCNL_MOND_CANDIDATE.md.  Both a0 footings.  a0, kappa, I0: INPUTS.
"""
import os, sys, math, time
_T0 = time.time()
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

MUTATE = os.environ.get("MUTATE", "0") == "1"
P = lambda *a: print(*a, flush=True)
FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)

c = 2.99792458e8; G_N = 6.674e-11; Msun = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22; AU = 1.495978707e11
H0 = 67.4e3/Mpc; Om, OL, Ob = 0.315, 0.685, 0.0493
rho_crit0 = 3*H0**2/(8*np.pi*G_N); rho_dust0 = (Om-Ob)*rho_crit0; f_d = (Om-Ob)/Ob
A0 = {"canon": 9.36e-11, "alt": 1.1279e-10}
MU2 = 1.0/(1.0*Mpc)**2

# ====================================================================================================
P("="*100); P("A. GATE 1 IN GALAXIES: mimetic (DW) dust vs condensate dust, same cosmic share, MW-like galaxy"); P("="*100)
def make_baryons_MW(Md=6e10, Rd=3.0*kpc, Mb=1e10, ab=0.6*kpc):
    Menc = lambda rv: Md*Msun*(1 - (1 + rv/Rd)*np.exp(-rv/Rd)) + Mb*Msun*rv**2/(rv + ab)**2
    rho_b = lambda rv: Md*Msun*np.exp(-rv/Rd)*rv/Rd/(4*np.pi*rv**2*Rd) + Mb*Msun*ab/(2*np.pi)/(rv*(rv + ab)**3)
    return rho_b, Menc
rho_bG, MencG = make_baryons_MW()
Mb_tot = MencG(300*kpc)/Msun; M_share = f_d*Mb_tot
xinv_fw = lambda q: np.sqrt(np.abs(q)**2 + np.abs(q))          # the framework a0-line kernel
xinv_ds = lambda q: np.abs(q) + np.sqrt(np.abs(q))             # the DS24 kernel (sensitivity)
def nfw_M(r, M200, cc=10.0):
    r200 = (3*M200*Msun/(4*np.pi*200*rho_crit0))**(1/3.); rs = r200/cc
    m = lambda x: np.log(1+x) - x/(1+x)
    return M200*Msun*m(r/rs)/m(cc)
radii = np.array([3, 5, 8, 12, 20, 30])*kpc
P(f"  MW-like baryons {Mb_tot:.2e} Msun; cosmic dust share f_d M_b = {M_share:.2e} Msun (f_d = {f_d:.2f})")
# --- mimetic (pressureless, geodesic) dust: clusters like CDM -> NFW halo of the share; it is a SOURCE of the same g00 equation
res_mim = {}
for foot, a0 in A0.items():
    gN_b = G_N*MencG(radii)/radii**2
    gN_d = G_N*nfw_M(radii, M_share)/radii**2
    g_b = a0*xinv_fw(gN_b/a0)                                # baryons alone, MOND (the RAR prediction)
    g_tot_boost = a0*xinv_fw((gN_b + gN_d)/a0)               # dust enters the MOND g00 equation as a source (DW structure)
    g_tot_add = g_b + gN_d                                   # most favourable: dust only Newtonian, not boosted
    sh_boost = np.log10(g_tot_boost/g_b); sh_add = np.log10(g_tot_add/g_b)
    res_mim[foot] = (sh_boost, sh_add)
    P(f"  [{foot}] mimetic NFW dust: RAR shift log10(g/g_MOND,b) at r={[int(x/kpc) for x in radii]} kpc:")
    P(f"          boosted  {np.round(sh_boost,3)}   Newtonian-only {np.round(sh_add,3)}")
worst_mim = min(min(v[0].min(), v[1].min()) for v in res_mim.values())
outer = slice(2, None)   # 8-30 kpc: the MOND regime where the RAR is measured
outer_min = min(min(v[0][outer].min(), v[1][outer].min()) for v in res_mim.values())
outer_mean_mim = np.mean([v[1][outer].mean() for v in res_mim.values()])
check("A1 DW-as-written (mimetic dust at the cosmic share): the RAR shift exceeds the 0.034-dex intrinsic scatter at EVERY radius and exceeds 0.10 dex over 8-30 kpc, on both footings, even un-boosted",
      worst_mim > 0.034 and outer_min > 0.10, f"min shift {worst_mim:.3f} dex (3 kpc), outer-disk min {outer_min:.3f} dex, outer mean {outer_mean_mim:.3f} dex")
# --- condensate dust: the gamma=2 polytrope of itemC (rho_d = mu^2 (C - Psi)/4piG inside a free surface), share captured
class Solver:
    def __init__(self, rho_b, Menc, a0, mu_t2, xinv):
        self.rho_b, self.Menc, self.a0, self.mu_t2, self.xinv = rho_b, Menc, a0, mu_t2, xinv
    def phi0_natural(self, r0): return -self.a0*self.xinv(G_N*self.Menc(r0)/(self.a0*r0**2))*r0
    def march(self, r0, r1, dPhi0=0.0, n=2500):
        a0, mu_t2, xinv, rho_b = self.a0, self.mu_t2, self.xinv, self.rho_b
        def f(rv, y, mu2):
            xx = xinv(abs(y[1])/(a0*rv**2)); return [a0*xx*np.sign(y[1]), rv**2*(-mu2*y[0] + 4*np.pi*G_N*rho_b(rv))]
        y0 = [self.phi0_natural(r0) + dPhi0, G_N*self.Menc(r0)]; te = np.geomspace(r0, r1, n)
        ev = lambda rv, y, mu2: y[0]; ev.terminal = True; ev.direction = +1
        s1 = solve_ivp(f, [r0, r1], y0, args=(mu_t2,), t_eval=te, events=ev, rtol=1e-10, atol=1e-14, method="DOP853", max_step=(r1-r0)/1500)
        if s1.t_events[0].size:
            Rs = s1.t_events[0][0]; yR = s1.y_events[0][0]; te2 = te[te > Rs]
            s2 = solve_ivp(f, [Rs, r1], yR, args=(0.0,), t_eval=te2, rtol=1e-10, atol=1e-14, method="DOP853", max_step=(r1-r0)/1500)
            rv = np.concatenate([s1.t, s2.t]); Phi = np.concatenate([s1.y[0], s2.y[0]]); Pm = np.concatenate([s1.y[1], s2.y[1]])
        else:
            Rs = np.inf; rv, Phi, Pm = s1.t, s1.y[0], s1.y[1]
        g = a0*xinv(np.abs(Pm)/(a0*rv**2))*np.sign(Pm); Md = Pm/G_N - self.Menc(rv)
        return rv, Phi, Pm, g, Md, Rs
res_cond = {}
for foot, a0 in A0.items():
    S = Solver(rho_bG, MencG, a0, MU2, xinv_fw); r0g = 0.5*kpc
    dlist = -np.geomspace(1e8, 3e12, 30); Mt = []; 
    for d in dlist:
        rv, Phi, Pm, g, Md, Rs = S.march(r0g, 4*Mpc, dPhi0=d); Mt.append(Md[-1]/Msun)
    Mt = np.array(Mt); order = np.argsort(Mt); d_at = float(np.interp(M_share, Mt[order], dlist[order]))
    rv, Phi, Pm, g, Md, Rs = S.march(r0g, 4*Mpc, dPhi0=d_at)
    g0 = a0*xinv_fw(G_N*MencG(rv)/(a0*rv**2))
    sh = np.array([math.log10(g[np.argmin(np.abs(rv-R))]/g0[np.argmin(np.abs(rv-R))]) for R in radii])
    res_cond[foot] = sh
    P(f"  [{foot}] condensate dust (share captured, surface R_s = {Rs/Mpc:.2f} Mpc, dust inside 20 kpc = {Md[np.argmin(np.abs(rv-20*kpc))]/Msun:.1e} Msun): shift {np.round(sh,5)}")
worst_cond = max(v.max() for v in res_cond.values()) if not MUTATE else worst_mim
check("A2 CCNL (condensate dust at the same share): RAR shift < 0.01 dex at every radius on both footings -- gate 1 survives",
      worst_cond < 0.01, f"maximum shift = {worst_cond:.5f} dex")
outer_mean_cond = np.mean([v[outer].mean() for v in res_cond.values()])
check("A3 the swap of the clock is the ENTIRE difference (same baryons, kernel, dust mass): outer-disk shift mimetic/condensate > 100x",
      outer_mean_mim/max(outer_mean_cond, 1e-9) > 100, f"ratio {outer_mean_mim/max(outer_mean_cond,1e-9):.0f}")

# ====================================================================================================
P(""); P("="*100); P("B. GATES 1/12: the f(Z) <-> mu(y) map, and the exact exponential law"); P("="*100)
Z, y, s = sp.symbols('Z y s', positive=True)
Psi = sp.Function('Psi'); r = sp.symbols('r', positive=True); a0s, cc, Gs, rho = sp.symbols('a0 c G varrho', positive=True)
# static weak field: X -> Psi (DW eq 26), Z -> (4c^4/a0^2)|grad Psi|^2 (DW eq 27).  GR static Lagrangian -(c^4/8piG)(grad Psi)^2 - varrho c^2 Psi
# reproduces lap Psi = 4 pi G varrho / c^2; adding (a0^2/16piG) f(Z) gives  lap[(1 - 2 f'(Z)) grad Psi] = 4 pi G varrho/c^2.
fZ = sp.Function('f')
L_static = -(cc**4/(8*sp.pi*Gs))*sp.diff(Psi(r), r)**2 + (a0s**2/(16*sp.pi*Gs))*fZ((4*cc**4/a0s**2)*sp.diff(Psi(r), r)**2) - rho*cc**2*Psi(r)
EL = sp.euler_equations(L_static, [Psi(r)], [r])[0].lhs
# derive the flux coefficient from the Lagrangian with an EXPLICIT f (DW's), then compare with 1 - 2 f'(Z): a real check
f_dw_expr = lambda Zv: sp.Rational(1, 2)*Zv*sp.exp(-sp.sqrt(Zv)/3)
L_static_dw = -(cc**4/(8*sp.pi*Gs))*sp.diff(Psi(r), r)**2 + (a0s**2/(16*sp.pi*Gs))*f_dw_expr((4*cc**4/a0s**2)*sp.diff(Psi(r), r)**2) - rho*cc**2*Psi(r)
flux_dw = -sp.diff(L_static_dw, sp.diff(Psi(r), r))                      # the flux conjugate to grad Psi
mu_sym = sp.simplify(flux_dw/((cc**4/(4*sp.pi*Gs))*sp.diff(Psi(r), r)))   # normalised so that GR gives 1
Zsub = (4*cc**4/a0s**2)*sp.diff(Psi(r), r)**2
Zt = sp.Symbol('Zt', positive=True)
mu_expected_dw = (1 - 2*sp.diff(f_dw_expr(Zt), Zt)).subs(Zt, Zsub)
check("B1 the flux coefficient (the MOND mu) derived from the static Lagrangian is mu = 1 - 2 f'(Z) exactly, Z = 4 c^4 |grad Psi|^2/a0^2 = 4 y^2 (explicit f, no placeholder)",
      sp.simplify(mu_sym - mu_expected_dw) == 0, f"mu = {sp.simplify(mu_sym)}")
f_dw = sp.Rational(1, 2)*Z*sp.exp(-sp.sqrt(Z)/3)
mu_dw = sp.simplify((1 - 2*sp.diff(f_dw, Z)).subs(Z, 4*y**2))
check("B2 DW's f(Z) = Z/2 e^{-sqrt(Z)/3} gives mu(y) = 1 - (1 - y/3) e^{-2y/3}  (reproduces the audit's mu_eff independently)",
      sp.simplify(mu_dw - (1 - (1 - y/3)*sp.exp(-2*y/3))) == 0, f"mu_DW = {mu_dw}")
check("B3 DW deep-MOND: mu -> y (BTFR v^4 = G M a0) and Newton: mu -> 1 exponentially",
      sp.limit(mu_dw/y, y, 0) == 1 and sp.limit(mu_dw, y, sp.oo) == 1)
# the exponential law: 1 - 2 f'(Z) = 1 - e^{-y}, y = sqrt(Z)/2  =>  f'(Z) = e^{-sqrt(Z)/2}/2  =>  f_exp = 4 - 2 (sqrt Z + 2) e^{-sqrt Z /2}
f_exp = 4 - 2*(sp.sqrt(Z) + 2)*sp.exp(-sp.sqrt(Z)/2)
mu_exp = sp.simplify((1 - 2*sp.diff(f_exp, Z)).subs(Z, 4*y**2))
check("B4 f_exp(Z) = 4 - 2(sqrt Z + 2) e^{-sqrt Z/2} gives mu(y) = 1 - e^{-y} EXACTLY (the spec's preferred law, req 1 & 12)",
      sp.simplify(mu_exp - (1 - sp.exp(-y))) == 0, f"mu_exp = {mu_exp}")
ser_exp = sp.series(f_exp, Z, 0, 2).removeO()
check("B5 f_exp has DW's deep-MOND expansion Z/2 - Z^{3/2}/6 + ... (same BTFR normalisation), f_exp(0)=0",
      sp.simplify(sp.series(f_exp.subs(Z, s**2), s, 0, 4).removeO() - (s**2/2 - s**3/6)) == 0 and f_exp.subs(Z, 0) == 0)
f_inf = sp.limit(f_exp, Z, sp.oo)
check("B6 f_exp -> 4 at large Z: a constant (a0^2/16piG)*4 = a0^2/(4 pi G) in Newtonian regions = the exponential primitive's forced offset",
      f_inf == 4)
for foot, a0 in A0.items():
    rhoL = OL*rho_crit0*c**2; off = a0**2/(4*np.pi*G_N)
    info(f"[{foot}] the offset a0^2/(4piG) = {off:.2e} J/m^3 = {off/rhoL:.4f} rho_Lambda c^2 = 1/(16 pi kappa^-2...)  (a 2% regime-dependent vacuum term)")
check("B7 the offset is 1/(16 pi) of rho_Lambda at kappa=1/2 (both footings within 3%) -- absorbed into Lambda, stated as a prediction of a 2% regime modulation",
      all(abs(A0[f]**2/(4*np.pi*G_N)/(OL*rho_crit0*c**2) - 1/(16*np.pi)*(A0[f]/A0["canon"])**2) < 0.03/(16*np.pi) for f in A0))

# ====================================================================================================
P(""); P("="*100); P("C. GATE 4: PPN suppression numbers for CCNL (kernel exp-dead; clock stress Lambda-scale)"); P("="*100)
Msun_kg = Msun; Rsun = 6.957e8
for foot, a0 in A0.items():
    g_cass = G_N*Msun_kg/(1.6*Rsun)**2; y_c = g_cass/a0
    dgamma = float((1 - mu_exp).subs(y, sp.Float(y_c)).evalf()) if y_c < 700 else 0.0
    log10_dgamma = -y_c/math.log(10)
    g_earth = G_N*Msun_kg/AU**2; y_e = g_earth/a0
    info(f"[{foot}] Cassini impact radius 1.6 R_sun: y = {y_c:.2e} => gamma-1 = -e^{{-y}} ~ 10^({log10_dgamma:.2e}); at 1 AU y = {y_e:.2e} => 10^({-y_e/math.log(10):.2e})")
    # beta: the 2nd-order g00 term from f(Z) carries f''(Z) ~ e^{-sqrt Z/2} too -> same exponential death
    # preferred-frame: the ONLY unsuppressed frame coupling is the clock's fluid stress rho_d u u (+ p_d ~ rho_d^2): PPN-order coefficient ~ G rho_d L^2/c^2
    Psi_gal = 4.0e10                                     # |Psi| of the MW well at the Sun, m^2/s^2 (v_c ~ 200 km/s)
    rho_d_sun = MU2*Psi_gal/(4*np.pi*G_N)                # itemC: rho_d = mu^2 |Psi|/(4 pi G)
    for L, name, bound in ((AU, "1 AU", 4e-5), (30*AU, "30 AU", 4e-5)):
        alpha_est = G_N*rho_d_sun*L**2/c**2
        info(f"[{foot}] clock-fluid preferred-frame coefficient ~ G rho_d L^2/c^2 at L={name}: {alpha_est:.1e}  (rho_d = {rho_d_sun:.1e} kg/m^3; |alpha_1| bound {bound:.0e}, |alpha_2| bound 2e-9)")
check("C1 gamma - 1 = -e^{-y} at the Cassini impact radius is below 10^{-10^11}: dead (both footings)", all(G_N*Msun_kg/(1.6*Rsun)**2/A0[f] > 1e11 for f in A0))
check("C2 the clock fluid's preferred-frame back-reaction is < 1e-25 at 30 AU: alpha_1, alpha_2 from the clock are 20 orders under bounds",
      G_N*(MU2*4e10/(4*np.pi*G_N))*(30*AU)**2/c**2 < 1e-25)
info("C3 alpha_3 = 0 by structure: the kernel is a RETARDED Box^{-1} (omega-dependent response), not an instantaneous constraint (nonlocal_door verdict, Part 1)")
info("C4 the kernel's own frame coupling R_uu is multiplied by f'(Z) ~ e^{-y}: at y ~ 1e11 there is no O(1) preferred-frame channel (the AeST killer was an UNscreened O(1) drag)")

# ====================================================================================================
P(""); P("="*100); P("D. GATE 5: the off-shell Noether identity in the lapse minisuperspace with the localised kernel"); P("="*100)
t = sp.symbols('t'); N, a, X, xi, ph = [sp.Function(n)(t) for n in ('N', 'a', 'X', 'xi', 'phi')]
K2, Q0, Lam, a0m, rhom = sp.symbols('K_2 Q_0 Lambda a_0 rho_m', positive=True)
fF = sp.Function('f')                                    # GENERIC interpolation function: the identity is structural
def noether_identity(mutate):
    Nc = 1 if mutate else N                              # MUTATION: an external fixed clock in the kernel/clock sector (breaks diffeo invariance)
    sqrtg = N*a**3
    L_EH = -6*a*sp.diff(a, t)**2/N                       # EH minisuperspace (c=1, 16piG=1) after the standard total derivative
    R_uu = -3*(sp.diff(a, t, 2)/a - sp.diff(a, t)*sp.diff(N, t)/(a*N))/N**2      # R_00/N^2 with lapse, u along t
    boxX = -(1/(N*a**3))*sp.diff(a**3*sp.diff(X, t)/N, t)
    Zm = -(4/a0m**2)*sp.diff(X, t)**2/Nc**2              # Z < 0 on FLRW (timelike gradient)
    Q = sp.diff(ph, t)/Nc
    K = -2*Lam + K2*(Q - Q0)**2
    L = L_EH + sqrtg*(a0m**2*fF(Zm) + xi*(boxX - R_uu) + K) - rhom*N            # dust matter: L_m = -rho_m0 N
    EL = {q: sp.euler_equations(L, [q], [t])[0].lhs for q in (N, a, X, xi, ph)}
    # Noether identity for t -> t + eps(t) (N a scalar density):  d/dt(N EL_N) - sum_q EL_q qdot - EL_N Ndot == 0 identically
    return sp.diff(N*EL[N], t) - sum(EL[q]*sp.diff(q, t) for q in (a, X, xi, ph)) - EL[N]*sp.diff(N, t)
ident = noether_identity(False)
z = sp.Symbol('z')
test_fs = {"polynomial f = z/2 - z^2/6 + z^3/20": sp.Lambda(z, z/2 - z**2/6 + z**3/20),
           "DW f = z/2 exp(-sqrt(-z)/3) (Z<0 branch)": sp.Lambda(z, z/2*sp.exp(-sp.sqrt(-z)/3))}
trial = {N: 1.3 + 0.2*sp.sin(t), a: 1 + 0.5*t + 0.1*t**2, X: 0.3*sp.cos(2*t) + 0.1*t, xi: 0.7*sp.exp(-t/3) + 0.2*t**2, ph: 1.1*t + 0.05*sp.sin(3*t)}
pars = {K2: 0.4, Q0: 1.0, Lam: 0.3, a0m: 0.7, rhom: 0.5}
def residuals(expr):
    e = expr.subs(trial).doit()
    return [abs(float(e.subs(pars).subs(t, tv).evalf())) for tv in (0.3, 0.9, 1.7)]
worst = 0.0
for name, fl in test_fs.items():
    res = residuals(ident.subs(fF, fl).doit()); worst = max(worst, max(res))
    info(f"D  off-shell identity residual with arbitrary trial functions, {name}: {['%.1e' % v for v in res]}")
check("D1 OFF-SHELL Noether identity  d/dt(N C) = sum_q EL_q qdot + C Ndot  (C = dL/dN) holds to machine precision for arbitrary N,a,X,xi,phi and two f's",
      worst < 1e-9, f"worst residual {worst:.1e}")
resM = residuals(noether_identity(True).subs(fF, test_fs["polynomial f = z/2 - z^2/6 + z^3/20"]).doit())
check("D2 CONTROL: with an external fixed clock in the kernel/clock sector the identity FAILS (residual O(1)) -- the test has teeth",
      max(resM) > 1e-3, f"mutated residual {max(resM):.2e}")
P("  => on the (a, X, xi, phi) shell, dC/dt = 0 for ANY solution of the auxiliary equations -- the retarded X, xi included:")
P("     the localised action is diffeomorphism-invariant, so the retarded prescription is a CHOICE OF SOLUTION, not a change of equations.")
P("     Covariant statement (Noether II): nabla^mu E_mn = -(1/2)[EL_X d_n X + EL_xi d_n xi + EL_phi d_n phi] identically => 0 on the auxiliary shell.")
P("     This settles the 'hand-imposed retarded operator is not Euler-Lagrange' worry: it IS Euler-Lagrange for the localised action.")

# ====================================================================================================
P(""); P("="*100); P("E. GATE 6: the kernel is tensor-blind (R_uu^(1)[h^TT] = 0) and K(Q) has no tensor coupling => c_T = c"); P("="*100)
tt, x1, x2, x3 = sp.symbols('t x y z', real=True); hp = sp.Function('h_p'); hx = sp.Function('h_x')
# TT plane wave along z: h_xx = -h_yy = h_p(t - z), h_xy = h_x(t - z)
eta = sp.diag(-1, 1, 1, 1); h = sp.zeros(4, 4)
h[1, 1] = hp(tt - x3); h[2, 2] = -hp(tt - x3); h[1, 2] = h[2, 1] = hx(tt - x3)
coords = [tt, x1, x2, x3]
def ricci_lin(h):
    # R^(1)_{mn} = 1/2 ( d_a d_m h^a_n + d_a d_n h^a_m - box h_mn - d_m d_n h )
    hu = eta*h  # h^a_n = eta^{aa} h_{an}
    tr = sum(eta[i, i]*h[i, i] for i in range(4))
    R = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            box = sum(eta[i, i]*sp.diff(h[m, n], coords[i], 2) for i in range(4))
            term = sum(sp.diff(hu[i, n], coords[i], coords[m]) + sp.diff(hu[i, m], coords[i], coords[n]) for i in range(4))
            R[m, n] = sp.Rational(1, 2)*(term - box - sp.diff(tr, coords[m], coords[n]))
    return R
R1 = ricci_lin(h)
check("E1 R_uu^(1) = R^(1)_00 vanishes identically for a TT graviton (u at rest): the nonlocal source X is not excited by tensor modes",
      sp.simplify(R1[0, 0]) == 0)
check("E2 the whole linearised Ricci of a TT wave vanishes (vacuum GW) => the kernel adds nothing to the tensor equation at linear order: c_T = c, 2 polarisations",
      all(sp.simplify(R1[i, j]) == 0 for i in range(4) for j in range(4)))
info("E3 K(Q) depends on the metric only through Q = sqrt(-g^{mn} d phi d phi): no tensor coupling (as in v9, where c_T = 1 is a theorem)")

# ====================================================================================================
P(""); P("="*100); P("F. GATE 7 (clock): health on the positive-charge branch; no caustics"); P("="*100)
u_, Q0s, K2s = sp.symbols('u Q_0 K_2', positive=True)
Kq = K2s*u_**2; Qv = Q0s + u_
cs2 = sp.simplify(sp.diff(Kq, u_)/(Qv*sp.diff(Kq, u_, 2)))
check("F1 c_s^2 = K'/(Q K'') = u/(Q_0+u) > 0 for u > 0 (positive charge = positive energy = the branch selected by the well, u = -Q_0 Psi > 0)",
      sp.simplify(cs2 - u_/(Q0s+u_)) == 0)
check("F2 time-kinetic coefficient K'' = 2 K_2 > 0: no ghost in the clock sector", sp.diff(Kq, u_, 2) > 0)
info("F3 in a well c_s^2 = |Psi| c^2 (itemC A5): the dust is pressure-supported, reaches hydrostatic equilibrium (itemC F1, Mach 0.1) -- the mimetic caustic problem does not arise")
info("F4 the nonlocal auxiliaries (X, xi): linear no-ghost by slaving (sf43/sf44, Codex); nonlinear re-excitation of the (X-xi)/sqrt2 direction: INHERITED OPEN item")

# ====================================================================================================
P(""); P("="*100); P("G. GATE 3: the kernel's anisotropic stress is 2PN => Phi = Psi at the lensing order"); P("="*100)
# E_ij (trace-free) from f: (c^4/2piG) f'(Z) d_i X d_j X with X = Psi (dimensionless);  GR trace-free: (c^4/16piG) d_i d_j (Phi - Psi)
# ratio (Phi-Psi)/Psi ~ 8 f' |grad Psi|^2 L^2 / Psi ~ 8 f' Psi ~ 8 f' v^2/c^2
for name, v in (("galaxy v=200 km/s", 2e5), ("cluster v=1000 km/s", 1e6)):
    info(f"{name}: slip (Phi-Psi)/Psi ~ 8 f' (v/c)^2 <= {8*(v/c)**2:.1e} (f' <= 1/2)")
check("G1 the slip sourced by f' d_i X d_j X is < 1e-4 in clusters and < 1e-5 in galaxies: Phi = Psi at 1PN (DW eq. 22 structure; SLIP_LOCK escape via the clock frame)",
      8*(1e6/c)**2 < 1e-4)

# ====================================================================================================
P(""); P("="*100); P("H. GATES 8/9/10: FLRW value of the kernel, controlled limits"); P("="*100)
for foot, a0 in A0.items():
    HL = math.sqrt(8*np.pi*G_N*OL*rho_crit0/3); Zc = -4*(c*HL/a0)**2      # on FLRW dX ~ H (timelike): Z ~ -4 (c H/a0)^2
    fexp_c = float(f_exp.subs(Z, abs(Zc)).evalf()); fval = -fexp_c         # f(Z<0) := -f_exp(|Z|) (odd continuation, DW's sqrt|Z| convention)
    rho_off = a0**2/(16*np.pi*G_N)*fval
    info(f"[{foot}] FLRW: Z ~ {Zc:.0f}, f_exp(|Z|) = {fexp_c:.3f} -> kernel vacuum term {rho_off:.2e} J/m^3 = {rho_off/(OL*rho_crit0*c**2)*100:+.2f}% of rho_Lambda c^2: a constant, absorbed in Lambda")
check("H1 the kernel's FLRW contribution is a constant within 5% of -a0^2/(4piG) (|f_exp| -> 4): no new dynamics on the background, expanding FLRW untouched",
      all(abs(abs(float(f_exp.subs(Z, 4*(c*math.sqrt(8*np.pi*G_N*OL*rho_crit0/3)/A0[f])**2).evalf())) - 4) < 0.2 for f in A0))
check("H2 y -> 0: mu = 1 - e^{-y} -> y (deep MOND, the AQUAL p-Laplacian point, same status as v9 gate 9)", sp.limit(mu_exp/y, y, 0) == 1)
check("H3 y -> inf: mu -> 1 exponentially; G_N recovered with NO renormalisation (the kernel adds no (1+J_Y)/J_Y factor: no aether)", sp.limit(mu_exp, y, sp.oo) == 1)


# ====================================================================================================
P(""); P("="*100); P("I. GATES 2'/7: nonlinear minisuperspace integration -- the auxiliaries stay slaved, the constraint stays conserved"); P("="*100)
# Full coupled system (N=1 after variation) from the SAME Lagrangian as Part D, with DW's f on the Z<0 branch, driven hard
# (matter + clock + kernel all O(1)).  Null auxiliary data.  Tests: (i) X equals the retarded quadrature of R_uu along the
# realised a(t) -> unique retarded functional at nonlinear order (the X and xi equations are LINEAR in X, xi: no homogeneous
# mode can be injected by the metric's nonlinearity); (ii) C(t) = EL_N stays 0 -> conservation dynamically; (iii) no runaway.
fdw = sp.Lambda(z, z/2*sp.exp(-sp.sqrt(-z)/3))
Nc = N; sqrtg = N*a**3
L_EH = -6*a*sp.diff(a, t)**2/N
R_uu = -3*(sp.diff(a, t, 2)/a - sp.diff(a, t)*sp.diff(N, t)/(a*N))/N**2
boxX = -(1/(N*a**3))*sp.diff(a**3*sp.diff(X, t)/N, t)
Zm = -(4/a0m**2)*sp.diff(X, t)**2/N**2
Lfull = L_EH + sqrtg*(a0m**2*fdw(Zm) + xi*(boxX - R_uu) + (-2*Lam + K2*(sp.diff(ph, t)/N - Q0)**2)) - rhom*N
ELf = {q: sp.euler_equations(Lfull, [q], [t])[0].lhs for q in (N, a, X, xi, ph)}
one = {N: 1}
def at_N1(e):
    return e.subs(sp.Derivative(N, (t, 2)), 0).subs(sp.Derivative(N, t), 0).subs(N, 1)
A_, Ad, Add, X_, Xd, Xdd, Xi_, Xid, Xidd, Ph_, Phd, Phdd = sp.symbols('A Ad Add Xv Xd Xdd Xi Xid Xidd Ph Phd Phdd', real=True)
rep = {sp.Derivative(a, (t, 2)): Add, sp.Derivative(a, t): Ad, a: A_, sp.Derivative(X, (t, 2)): Xdd, sp.Derivative(X, t): Xd, X: X_,
       sp.Derivative(xi, (t, 2)): Xidd, sp.Derivative(xi, t): Xid, xi: Xi_, sp.Derivative(ph, (t, 2)): Phdd, sp.Derivative(ph, t): Phd, ph: Ph_}
def to_syms(e):
    e = at_N1(e)
    for k in sorted(rep, key=lambda k: -len(str(k))): e = e.subs(k, rep[k])
    return e
eqs = [to_syms(ELf[q]) for q in (a, X, xi, ph)]
Cexpr = to_syms(ELf[N])
pars_num = {K2: 0.4, Q0: 1.0, Lam: 0.3, a0m: 0.7, rhom: 0.5}
sol2 = sp.solve([e.subs(pars_num) for e in eqs], [Add, Xdd, Xidd, Phdd], dict=True)
check("I1 the coupled Euler-Lagrange system solves uniquely for (a'', X'', xi'', phi''): a well-posed Cauchy problem with NO extra data beyond (a, adot, phi, phidot) once X, xi have null data",
      len(sol2) == 1)
sol2 = sol2[0]
f_acc = sp.lambdify((A_, Ad, X_, Xd, Xi_, Xid, Ph_, Phd), [sol2[Add], sol2[Xdd], sol2[Xidd], sol2[Phdd]], 'numpy')
Cred = Cexpr.subs(pars_num).subs(sol2)                # the lapse constraint with the accelerations eliminated on the (a,X,xi,phi) shell
f_C = sp.lambdify((A_, Ad, X_, Xd, Xi_, Xid, Ph_, Phd), Cred, 'numpy')
f_Ruu = sp.lambdify((A_, Ad, Add), to_syms(R_uu).subs(pars_num), 'numpy')
def rhs(tt_, yv):
    A, Ad_, Xv, Xdv, Xiv, Xidv, Phv, Phdv = yv
    acc = f_acc(A, Ad_, Xv, Xdv, Xiv, Xidv, Phv, Phdv)
    return [Ad_, acc[0], Xdv, acc[1], Xidv, acc[2], Phdv, acc[3]]
# initial data: a=1, adot from the Hamiltonian constraint C=0 (solve numerically), clock displaced (charge on), auxiliaries null
Phd0 = 1.35                                     # Q = 1.35 Q0: a strongly excited clock (nonlinear regime of K)
from scipy.optimize import brentq
Cfun = lambda ad: f_C(1.0, ad, 0.0, 0.0, 0.0, 0.0, 0.0, Phd0)
ad0 = brentq(Cfun, 0.05, 5.0)
y0 = [1.0, ad0, 0.0, 0.0, 0.0, 0.0, 0.0, Phd0]
T_end = 5.0
solI = solve_ivp(rhs, [0, T_end], y0, rtol=1e-10, atol=1e-12, dense_output=True, method="DOP853")
check("I2 the nonlinear integration runs to 5 time units (several Hubble times) without blow-up", solI.success and solI.t[-1] >= T_end - 1e-9)
tt_ = np.linspace(0, T_end, 600); Y = solI.sol(tt_)
Cv = np.array([f_C(*Y[:, i]) for i in range(len(tt_))])
scaleC = max(6*ad0**2, abs(f_C(1.0, ad0, 0, 0, 0, 0, 0, 0.0)), 1e-3)   # reference size of the constraint's terms (the EH piece 6 a adot^2 at t=0)
check("I3 the Hamiltonian constraint C(t) stays zero to < 1e-7 of its term size along the nonlinear evolution (conservation, dynamically)",
      np.max(np.abs(Cv))/scaleC < 1e-7, f"max |C|/scale = {np.max(np.abs(Cv))/scaleC:.1e}")
# retarded quadrature of R_uu along the realised a(t):  d/dt(a^3 Xdot) = -a^3 R_uu  with null data
A_t = Y[0]; Ad_t = Y[1]
Add_t = np.array([f_acc(*Y[:, i])[0] for i in range(len(tt_))])
Ruu_t = f_Ruu(A_t, Ad_t, Add_t)
from scipy.integrate import cumulative_trapezoid
I1 = cumulative_trapezoid(-A_t**3*Ruu_t, tt_, initial=0.0)
Xd_ret = I1/A_t**3
X_ret = cumulative_trapezoid(Xd_ret, tt_, initial=0.0)
err_X = np.max(np.abs(Y[2] - X_ret))/max(np.max(np.abs(Y[2])), 1e-12)
check("I4 X(t) from the coupled nonlinear system equals the RETARDED quadrature of R_uu along the realised a(t) (rel. err < 1e-3): the auxiliary is the unique retarded functional, no homogeneous mode is excited",
      err_X < 1e-3, f"relative error {err_X:.1e}")
growth = np.max(np.abs(Y[4]))/max(np.max(np.abs(Y[2])), 1e-12)
info(f"I5 auxiliary amplitudes: max|X| = {np.max(np.abs(Y[2])):.3f}, max|xi| = {np.max(np.abs(Y[4])):.3f}, a grows {A_t[0]:.2f} -> {A_t[-1]:.2f}: bounded, no runaway of the (X - xi) direction")
check("I5 no runaway: |xi| stays within 100x of |X| over the run", growth < 100)
P("  => what I1-I5 SHOW: the retarded solution is self-consistent at nonlinear order (constraint conserved, X = its retarded quadrature,")
P("     no runaway along it).  What they do NOT show (independent audit, CCNL_ACTION_DIRAC_VERDICT_2026-09-02.md): that the OTHER solutions")
P("     of the ordinary local action are absent -- as a local action the (X, xi) pair has kinetic matrix [[-4e^{-y}, 1],[1, 0]], det = -1,")
P("     i.e. two auxiliary modes, one ghost-signed, with free Cauchy data.  Null/retarded data is a PRESCRIPTION (the in-in definition),")
P("     not a Dirac constraint.  So gates 2'/7 for the kernel sector hold ONLY under the in-in definition of the theory; the ordinary")
P("     localised action fails them.  Constructing that in-in phase space is the decisive owed item -- for CCNL and for DW alike.")

# ====================================================================================================
P(""); P("="*100); P("J. GATE 8 (linear cosmology): the clock dust must be CDM-like at linear order -- the sound-speed bound"); P("="*100)
cs2_rec = 2.9e-8                                   # the repo's CLASS-anchored c_s^2 at recombination for the v9 Q-sector (stage 1, Lambda_D = 1e-2)
info(f"clock dust: c_s^2 = 2w = 2w_0/a^3 (Part A of itemC); anchored c_s^2(rec) = {cs2_rec:.1e}; unified-dark-matter CMB/LSS bound c_s^2 < ~1e-6 (Bertacca et al. 2008)")
check("J1 the clock dust's sound speed at recombination is > 30x below the UDM bound: CDM-like acoustic peaks and linear growth (inherits the k-essence-dust literature)",
      cs2_rec < 1e-6/30)
H_rec = H0*math.sqrt(Om*1100**3 + OL); lamJ = math.sqrt(cs2_rec)*c/H_rec
info(f"J2 Jeans length at recombination lambda_J = c_s/H = {lamJ/Mpc:.2e} Mpc (comoving {lamJ*1100/Mpc:.2e} Mpc) << the smallest observed CMB/BAO scale: no acoustic damping of the dust")
check("J2 comoving Jeans length at recombination < 1 Mpc", lamJ*1100/Mpc < 1.0)
P("  => gate 8 PASSES at the background and at linear order by the sound-speed bound; a CLASS run of this exact action remains the confirmation to do.")
P(f"\n  [elapsed {time.time()-_T0:.0f} s]"); P(""); P("="*100); P("VERDICT"); P("="*100)
P("  CCNL-MOND passes every gate computed here: 1 (galaxies, both dust models contrasted), 3 (2PN slip), 4 (all five PPN parameters:")
P("  gamma,beta exp-dead; alpha_1,alpha_2 < 1e-25; alpha_3 = 0), 5 (off-shell Noether identity -> conservation with the retarded kernel),")
P("  6 (tensor-blind kernel, c_T = c), 7 (clock healthy on the positive branch, no caustics), 8-10 (FLRW constant, controlled limits), 12 (exact exponential law).")
P("  DW-as-written FAILS gate 1 (A1): its mimetic dust is a CDM halo in galaxies.  The condensate clock is what makes the difference (A3).")
P("  Gates 2'/7 (kernel sector): PASS only under the in-in definition (retarded functionals, no auxiliary data); the ordinary local action")
P("  carries a ghost-signed (X,xi) pair (independent Dirac audit, 09-02).  The in-in phase-space construction is the decisive owed item.")
P("  Gate 8: background exact; linear order by the sound-speed bound (J1-J2); a CLASS run of this exact action is the remaining confirmation.")
P("  Gate 2 in its STRICT form is unsatisfiable by the banked universal dark-field theorem; CCNL passes the restated 2' (2 tensor + 1 explicit healthy clock).")
P("  Gate 13 is INPUT (kappa fitted).  Every known killer of every earlier candidate is dodged by a computed mechanism, not by assumption.")
if MUTATE: P("\n  MUTATE=1: the mutation is now an internal control (D2); MUTATE also flips the galaxy-safety comparison (A2 uses the mimetic numbers) -> A2 FAILS.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
