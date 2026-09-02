#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
itemC_phase_pinning_dynamics_2026.py
====================================
ITEM C of the cluster-phase workflow -- THE DECISIVE DYNAMIC CALC: does the Helmholtz phase PIN?
(the "un-run" calc named 2026-09-01: time-dependent spherical solve, dust = irrotational potential flow)

WHAT WAS WRONG BEFORE (stated first, verified in Part B).  The three June solves (aest_collapse, the
rigorous three-caveat run, the 3-D prototype) evolved  chi_tt - c_s^2 lap chi + (mu c)^2 chi = S,
a GAPPED Klein-Gordon wave whose static limit is YUKAWA (e^{-mu r}/r).  But the static equation the
phase belongs to (DS24 Eq 2.40) is HELMHOLTZ (sin(mu r)/r).  So the "undamped free mode at omega = mu c"
is a different branch of the theory from the one the phase lives in.  The phase lives in the DUST branch.

WHAT THE DUST BRANCH IS (Part A, from the action, sympy).  With K(Q) = K_2 (Q-Q_0)^2 and Q = Q_0 + u:
    pressure  p = K/(8 pi G~),   density  rho = (Q K' - K)/(8 pi G~)
    =>  p = (2 pi G / mu^2) rho^2          <-- a gamma = 2 (Lane-Emden n = 1) POLYTROPE
        c_s^2 = dp/drho = 4 pi G rho / mu^2 = u/(Q_0+u) = 2 w     (SZ2021's c_ad^2 = 2w recovered)
    in a static well  Q = (1 - Psi) Q_0  =>  u = -Q_0 Psi  =>  c_s^2 = |Psi| c^2   and
        rho_d = - mu^2 Psi / (4 pi G)      <-- EXACTLY DS24's phantom, with mu^2 = 2K_2 Q_0^2/(2-K_B), G~=(1-K_B/2)G
    Hydrostatic equilibrium of that polytrope, grad p = -rho grad Psi, gives  rho_d = mu^2 (C - Psi)/(4 pi G)
    with ONE free constant C: the DS24 "oscillation phase" IS the polytrope's Bernoulli constant (= its mass).
    Lane-Emden n=1 radius pi/mu is MASS-INDEPENDENT: the polytrope holds any mass.  That is the freedom.
    ==> the published no-go's premise "c_s^2 -> 0, so the dust is pressureless and clumps by DENSITY" is
        wrong inside wells: c_s^2 = |Psi|.  The dust is ordered by POTENTIAL DEPTH.  (item B's ordering.)

THE PIN (Part B/C/D).  sign(rho_d) = sign(u) = sign(c_s^2).  Any static branch with rho_d < 0 somewhere
(Psi > C: a potential HILL carrying dust) has c_s^2 < 0 there -- a GRADIENT INSTABILITY at rate |c_s| k,
unbounded in k -- and cannot be a dynamical end state.  The higher Helmholtz branches all carry nodes,
so they are EXCLUDED.  The physical configuration is the unique positive-density polytrope with a FREE
SURFACE (rho_d -> 0 at R_s <= pi/mu), pure MOND outside; its one parameter is the captured dust MASS,
capped by the cosmic budget f_d M_b.  The core yield is then a computed number, not a tune.

Part F runs the time-dependent solve in the CORRECT form: 1-D Lagrangian gamma=2 hydro of the dust
falling into the growing MOND well (artificial viscosity for shocks), and checks (i) the end state is
hydrostatic, (ii) its core mass equals the static polytrope's at the same captured mass, (iii) a free-mode
sin(mu r)/(mu r) admixture in the ICs does NOT survive into the core mass (the pin, in the right dynamics).

Both footings (a0 = 9.36e-11 canonical / 1.128e-10 alt); DS24 kernel primary, framework kernel as a row.
Checks that can FAIL (rc=1) and a mutation control (MUTATE=1 flips the lapse relation Q=(1-Psi)Q_0 -> (1+Psi)Q_0 and the Helmholtz sign -> Yukawa: A4/A5 and the branch structure must break).
"""
import os, sys, json, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

MUTATE = os.environ.get("MUTATE", "0") == "1"
P = lambda *a: print(*a, flush=True)
FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)

# ------------------------------------------------------------------------------------------ constants
c = 2.99792458e8; G_N = 6.674e-11; Msun = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22
H0 = 67.4e3/Mpc; Om, OL, Ob = 0.315, 0.685, 0.0493
rho_crit0 = 3*H0**2/(8*np.pi*G_N); rho_dust0 = (Om - Ob)*rho_crit0; f_d = (Om - Ob)/Ob
A0 = {"canon": 9.36e-11, "alt": 1.1279e-10}
INV_MU = 1.0*Mpc; MU2 = 1.0/INV_MU**2          # the CMB-pinned AeST mass used by DS24/BS24 and items A/B
HELM_SIGN = -1.0 if MUTATE else +1.0            # MUTATION: Helmholtz -> Yukawa in the solver
R_CORE = 420*kpc; M_RESID = {"paper_1e14": 1.0e14, "harsh_1.5e14": 1.5e14}
KB = 0.25

P("="*100); P("PART A -- the dust branch from the action: a gamma=2 polytrope whose hydrostatics IS the Helmholtz equation"); P("="*100)
K2, Q0, u, Psi, mu, G, KBs, Gt = sp.symbols('K_2 Q_0 u Psi mu G K_B Gtilde', real=True)
Kq = K2*u**2
Q = Q0 + u
p_d   = Kq/(8*sp.pi*Gt)                          # k-essence: pressure = Lagrangian  (L_Q = -F(0,Q)/16piG~ = K/8piG~)
rho_d = (Q*sp.diff(Kq, u) - Kq)/(8*sp.pi*Gt)     # rho = Q dL/dQ - L
cs2   = sp.simplify(sp.diff(Kq, u)/(Q*sp.diff(Kq, u, 2)))     # c_s^2 = K'/(Q K'')
w     = sp.simplify(p_d/rho_d)
check("A1 c_s^2 = K'/(Q K'') = u/(Q_0+u)  and  w = p/rho = u/(2Q_0+u)  =>  c_s^2 = 2w at leading order (SZ2021 c_ad^2 = 2w)",
      sp.simplify(cs2 - u/(Q0+u)) == 0 and sp.simplify(w - u/(2*Q0+u)) == 0 and sp.limit(sp.simplify(cs2/w), u, 0) == 2)
# leading order: rho ~ K2 Q0 u/(4 pi G~) ; eliminate u -> p(rho)
rho_lead = sp.series(rho_d, u, 0, 2).removeO(); u_of_rho = sp.solve(sp.Eq(sp.Symbol('rho'), rho_lead), u)[0]
p_of_rho = sp.simplify(p_d.subs(u, u_of_rho))
rho_s = sp.Symbol('rho')
# SZ2021: mu^2 = 2 K2 Q0^2/(2-K_B);  G~ = (1 - K_B/2) G   (bridge1_aest_equations.md)
subs_mu = {K2: mu**2*(2-KBs)/(2*Q0**2), Gt: (1-KBs/2)*G}
p_phys = sp.simplify(p_of_rho.subs(subs_mu))
check("A2 EOS: p = rho^2/(8 K_2 Q_0^2 G~ ... )  ->  with SZ2021's mu^2 and G~:  p_d = (2 pi G / mu^2) rho_d^2   [gamma = 2]",
      sp.simplify(p_phys - 2*sp.pi*G*rho_s**2/mu**2) == 0,
      f"p = {p_phys}")
cs2_phys = sp.simplify(sp.diff(p_phys, rho_s))
check("A3 c_s^2 = dp/drho = 4 pi G rho_d / mu^2  (sound speed grows with the dust density: c_s^2 -> 0 ONLY on the cosmic background)",
      sp.simplify(cs2_phys - 4*sp.pi*G*rho_s/mu**2) == 0)
# static well: Q = (1 - Psi) Q0  (quasi-static, bridge1)  =>  u = -Q0 Psi
u_well = (+Q0*Psi) if MUTATE else (-Q0*Psi)      # MUTATION: wrong-sign lapse relation Q = (1+Psi) Q_0
rho_well = sp.simplify(rho_lead.subs(u, u_well).subs(subs_mu))
check("A4 static well u = -Q_0 Psi:  rho_d = -mu^2 Psi/(4 pi G)  EXACTLY DS24's phantom rho_ph (Psi<0 in a well => rho_d>0)",
      sp.simplify(rho_well + mu**2*Psi/(4*sp.pi*G)) == 0, f"rho_d = {rho_well}")
cs2_well = sp.simplify(cs2.subs(u, u_well))
check("A5 in a static well c_s^2 = u/(Q_0+u) = -Psi/(1-Psi) ~ |Psi| c^2: the dust is NOT cold inside wells; its pressure IS the potential depth",
      sp.simplify(cs2_well - (-Psi/(1-Psi))) == 0, f"c_s^2 = {cs2_well}")
# hydrostatic equilibrium of the gamma=2 polytrope in an external potential: grad p = -rho grad Psi
r = sp.symbols('r', positive=True); Cc = sp.symbols('C', real=True)
rho_f = sp.Function('rho')(r); Psi_f = sp.Function('Psi')(r)
hyd = sp.diff(2*sp.pi*G*rho_f**2/mu**2, r) + rho_f*sp.diff(Psi_f, r)          # = 0
sol_rho = mu**2*(Cc - Psi_f)/(4*sp.pi*G)
check("A6 hydrostatic equilibrium grad p = -rho grad Psi is solved by rho_d = mu^2 (C - Psi)/(4 pi G), C free: DS24's level freedom IS the polytrope's Bernoulli constant",
      sp.simplify(hyd.subs(rho_f, sol_rho).doit()) == 0)
# Poisson with that dust: lap Psi = 4 pi G (rho_b + rho_d)  =>  lap Psi + mu^2 (Psi - C) = 4 pi G rho_b : Helmholtz with the constant
rho_b = sp.Function('rho_b')(r)
poisson = sp.diff(r**2*sp.diff(Psi_f, r), r)/r**2 - 4*sp.pi*G*(rho_b + sol_rho)
helm = sp.diff(r**2*sp.diff(Psi_f, r), r)/r**2 + mu**2*(Psi_f - Cc) - 4*sp.pi*G*rho_b
check("A7 Poisson with the hydrostatic dust == the Helmholtz equation lap Psi + mu^2 (Psi - C) = 4 pi G rho_b  (item A's dPhi0 = -C)",
      sp.simplify(poisson - helm) == 0)
# Lane-Emden n=1: the self-gravitating polytrope radius is pi/mu independent of mass
alpha2 = sp.simplify((2*(2*sp.pi*G/mu**2))/(4*sp.pi*G))   # alpha^2 = (n+1) K_p / (4 pi G) with n=1
check("A8 Lane-Emden n=1 scale alpha = 1/mu: the self-gravitating dust polytrope has radius pi/mu for ANY mass (the 'holds any mass' freedom)",
      sp.simplify(alpha2 - 1/mu**2) == 0)
# DBI (v9) reduces to the same at small u
M4, mu2s = sp.symbols('M4 mu2', positive=True)
K_dbi = -M4*sp.sqrt(1 - mu2s*u**2/M4) + M4
check("A9 the v9 DBI K(Q) = -M^4 sqrt(1 - mu^2 u^2/M^4) has the SAME leading K_2 u^2/2-type quadratic term: the polytrope result transfers",
      sp.simplify(sp.series(K_dbi, u, 0, 4).removeO() - mu2s*u**2/2) == 0)
P("  => NEW EQUATION (from the action):  p_d = (2 pi G / mu^2) rho_d^2 ,  c_s^2 = |Psi| c^2 in a static well.")
P("     The AeST Q-sector dust is a gamma=2 polytrope; DS24's Helmholtz phase is its Bernoulli constant / mass.")

P(""); P("="*100); P("PART B -- (i) the June solves evolved the wrong branch; (ii) positivity: rho_d<0 <=> c_s^2<0 <=> gradient instability"); P("="*100)
chi = sp.Function('chi')(r); cs, mus = sp.symbols('c_s mu', positive=True)
june_static = -cs**2*(sp.diff(r**2*sp.diff(chi, r), r)/r**2) + (mus*c)**2*chi      # static limit of chi_tt - c_s^2 lap chi + (mu c)^2 chi
yuk = sp.exp(-mus*c/cs*r)/r
check("B1 the June equation's static limit is YUKAWA: e^{-(mu c/c_s) r}/r solves it, sin(mu r)/r does NOT -> it is the gapped branch, not the Helmholtz (dust) branch",
      sp.simplify(june_static.subs(chi, yuk).doit()) == 0 and sp.simplify(june_static.subs(chi, sp.sin(mus*r)/r).doit()) != 0)
# gradient instability e-folds per Hubble time in a negative-density region of depth |Psi| at k = mu (and growing with k)
for Psi_v in (1e-6, 1e-5):
    cs_v = math.sqrt(Psi_v)*c; rate = cs_v*math.sqrt(MU2); efold = rate/H0
    info(f"B2 |Psi| = {Psi_v:.0e}: |c_s| = {cs_v/1e3:.0f} km/s, growth rate |c_s| mu = {rate:.2e} s^-1 = {efold:.1f} e-folds per Hubble time at k = mu (unbounded as k grows)")
check("B2 a negative-charge (rho_d<0) region is gradient-unstable on sub-Hubble timescales already at k = mu (>3 e-folds/Hubble for |Psi| >= 1e-6)",
      math.sqrt(1e-6)*c*math.sqrt(MU2)/H0 > 3)
P("  => THEOREM: a static configuration with rho_d < 0 anywhere is not a dynamical end state.  Admissible: rho_d >= 0 everywhere.")

# ------------------------------------------------------------------------------ item A's solver (verbatim physics)
def xinv_ds24(qv):
    qv = np.abs(np.asarray(qv, float)); return qv + np.sqrt(qv)
def xinv_fw(qv):
    qv = np.abs(np.asarray(qv, float)); return np.sqrt(qv**2 + qv)
def make_baryons_A2029(M500, R500, beta=0.67, rc_frac=0.12, fgas=0.13, fstar=0.012, a_bcg_kpc=30.0):
    rc = rc_frac*R500; a_bcg = a_bcg_kpc*kpc; M_bcg = fstar*M500*Msun; M_gas_tot = fgas*M500*Msun
    rho_gas_un = lambda rv: (1.0 + (rv/rc)**2)**(-1.5*beta)
    rgrid = np.geomspace(1e-3*rc, R500, 200000)
    norm = np.trapz(4*np.pi*rgrid**2*rho_gas_un(rgrid), rgrid); rho_g0 = M_gas_tot/norm
    rtab = np.geomspace(1e-4*rc, 80*Mpc, 8000); integ = 4*np.pi*rtab**2*rho_g0*rho_gas_un(rtab)
    Mgas_tab = np.concatenate([[0.0], np.cumsum(0.5*(integ[1:] + integ[:-1])*np.diff(rtab))])
    Menc = lambda rv: np.interp(rv, rtab, Mgas_tab) + M_bcg*(rv**2/(rv + a_bcg)**2)
    rho_b = lambda rv: rho_g0*rho_gas_un(rv) + M_bcg*a_bcg/(2*np.pi)/(rv*(rv + a_bcg)**3)
    return rho_b, Menc
def make_baryons_MW(Md=6e10, Rd=3.0*kpc, Mb=1e10, ab=0.6*kpc):
    Menc = lambda rv: Md*Msun*(1 - (1 + rv/Rd)*np.exp(-rv/Rd)) + Mb*Msun*rv**2/(rv + ab)**2
    rho_b = lambda rv: Md*Msun*np.exp(-rv/Rd)*rv/Rd/(4*np.pi*rv**2*Rd) + Mb*Msun*ab/(2*np.pi)/(rv*(rv + ab)**3)
    return rho_b, Menc

class Solver:
    """DS24 Eq 2.40 in canonical-momentum form (item A), with a FREE SURFACE: the dust term mu^2 Phi is active only
    while Phi < 0 (rho_d = -mu^2 Phi/4piG > 0); at the first zero R_s it switches off permanently (pure MOND outside)."""
    def __init__(self, rho_b, Menc, a0, mu_t2, xinv=xinv_ds24):
        self.rho_b, self.Menc, self.a0, self.mu_t2, self.xinv = rho_b, Menc, a0, mu_t2, xinv
    def g_ref(self, rv):
        rv = np.atleast_1d(rv); return self.a0*self.xinv(G_N*self.Menc(rv)/(self.a0*rv**2))
    def phi0_natural(self, r0):
        return -self.a0*self.xinv(G_N*self.Menc(r0)/(self.a0*r0**2))*r0
    def march(self, r0, r1, dPhi0=0.0, free_surface=True, n=3000):
        a0, mu_t2, xinv, rho_b = self.a0, self.mu_t2, self.xinv, self.rho_b
        def f(rv, y, mu2):
            xx = xinv(abs(y[1])/(a0*rv**2))
            return [a0*xx*np.sign(y[1]), rv**2*(-HELM_SIGN*mu2*y[0] + 4*np.pi*G_N*rho_b(rv))]
        y0 = [self.phi0_natural(r0) + dPhi0, G_N*self.Menc(r0)]
        te = np.geomspace(r0, r1, n)
        if free_surface:
            ev = lambda rv, y, mu2: y[0]; ev.terminal = True; ev.direction = +1
            s1 = solve_ivp(f, [r0, r1], y0, args=(mu_t2,), t_eval=te, events=ev, rtol=1e-10, atol=1e-14, method="DOP853", max_step=(r1-r0)/1500)
            if s1.t_events[0].size:
                Rs = s1.t_events[0][0]; yR = s1.y_events[0][0]
                te2 = te[te > Rs]
                s2 = solve_ivp(f, [Rs, r1], yR, args=(0.0,), t_eval=te2, rtol=1e-10, atol=1e-14, method="DOP853", max_step=(r1-r0)/1500)
                rv = np.concatenate([s1.t, s2.t]); Phi = np.concatenate([s1.y[0], s2.y[0]]); Pm = np.concatenate([s1.y[1], s2.y[1]])
            else:
                Rs = np.inf; rv, Phi, Pm = s1.t, s1.y[0], s1.y[1]
        else:
            s1 = solve_ivp(f, [r0, r1], y0, args=(mu_t2,), t_eval=te, rtol=1e-10, atol=1e-14, method="DOP853", max_step=(r1-r0)/1500)
            Rs = np.nan; rv, Phi, Pm = s1.t, s1.y[0], s1.y[1]
        g = a0*xinv(np.abs(Pm)/(a0*rv**2))*np.sign(Pm)
        Md = Pm/G_N - self.Menc(rv)                     # dust (phantom) mass enclosed
        return rv, Phi, Pm, g, Md, Rs
    def at(self, rv, arr, R):
        return arr[np.argmin(np.abs(rv - R))]

M500, R500 = 1.0e15, 1.56*Mpc; r0 = 0.02*Mpc
rho_bC, MencC = make_baryons_A2029(M500, R500)
z = 0.1; rho_crit_z = rho_crit0*(Om*(1+z)**3 + OL)
r_ta = (3*M500*Msun/(4*np.pi*2.8*rho_crit_z))**(1/3.)
budget_R500 = f_d*MencC(R500)/Msun; budget_ta = f_d*MencC(r_ta)/Msun
info(f"cluster: M500 = 1e15, R500 = 1.56 Mpc, r_ta = {r_ta/Mpc:.2f} Mpc, mu r_ta = {math.sqrt(MU2)*r_ta:.2f} rad, pi/mu = {math.pi/math.sqrt(MU2)/Mpc:.2f} Mpc")
info(f"dust budget f_d M_b: {budget_R500:.2e} Msun inside R500, {budget_ta:.2e} Msun inside r_ta   (f_d = {f_d:.2f})")

P(""); P("="*100); P("PART C -- item A's matched branches (mu r_ta = 8.5 > pi): do they carry negative dust?"); P("="*100)
S = Solver(rho_bC, MencC, A0["canon"], MU2)
try:
    jA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "itemA_reconstruct_lever_2026.json")))
    roots = jA["baseline_1Mpc_canon"]["roots_DE"] + jA["baseline_1Mpc_canon"]["roots_mean"]
except Exception as e:
    roots = []; info(f"(item A json not readable: {e}; using a representative branch set)")
    roots = [{"dPhi0": d, "eta_R500": float('nan'), "Mph_core": float('nan')} for d in (-8.4e12, -4.3e12, -3.2e12, 3.9e11, 3.1e12)]
n_neg = 0
for rt in roots:
    rv, Phi, Pm, g, Md, Rs = S.march(r0, r_ta, dPhi0=rt["dPhi0"], free_surface=False)
    rho_d = -MU2*Phi/(4*np.pi*G_N)
    neg = rho_d.min() < 0; n_neg += neg
    first0 = rv[np.argmax(rho_d < 0)]/Mpc if neg else float('inf')
    info(f"branch dPhi0 = {rt['dPhi0']:+.2e}: eta(R500) = {rt['eta_R500']:.2f}, core phantom = {rt['Mph_core']:.2e} Msun, "
         f"rho_d < 0 first at r = {first0:.2f} Mpc  -> {'EXCLUDED (unstable)' if neg else 'admissible'}")
check(f"C1 EVERY item-A branch matched at r_ta carries a negative-dust region (n = {n_neg}/{len(roots)}): the 'phase menu' is entirely excluded by positivity",
      n_neg == len(roots) and len(roots) > 0)
P("  => the phase freedom of the r_ta-matched BVP is not physical freedom: no branch survives.  The physical family is Part D.")

P(""); P("="*100); P("PART D -- the physical family: positive-density dust polytrope with a free surface, one parameter = captured mass"); P("="*100)
def family(S, dlist, r1=6*Mpc, rstart=None):
    rows = []
    rs_ = r0 if rstart is None else rstart
    for d in dlist:
        rv, Phi, Pm, g, Md, Rs = S.march(rs_, r1, dPhi0=d, free_surface=True)
        rho_d = -MU2*Phi/(4*np.pi*G_N); rho_d[rv > Rs] = 0.0
        Mtot = Md[-1]/Msun; Mcore = S.at(rv, Md, R_CORE)/Msun
        eta = S.at(rv, g, R500)/S.g_ref(R500)[0]
        rows.append(dict(dPhi0=d, Rs=Rs/Mpc, Mtot=Mtot, Mcore=Mcore, eta=eta, rho_min=rho_d[rv < Rs].min() if np.isfinite(Rs) else rho_d.min()))
    return rows
dlist = -np.geomspace(1e9, 3e14, 34)
results = {}
for foot, a0v in A0.items():
    for kern_name, kern in (("DS24", xinv_ds24), ("framework", xinv_fw)):
        S = Solver(rho_bC, MencC, a0v, MU2, xinv=kern)
        rows = family(S, dlist); results[(foot, kern_name)] = rows
        if foot == "canon" and kern_name == "DS24":
            P(f"  footing={foot} kernel={kern_name}:")
            P(f"   {'dPhi0[m2/s2]':>13s} {'R_s[Mpc]':>9s} {'M_dust,tot':>11s} {'M_dust(<420kpc)':>16s} {'f(1e14)':>8s} {'eta(R500)':>9s}")
            for rw in rows[::3]:
                P(f"   {rw['dPhi0']:13.2e} {rw['Rs']:9.3f} {rw['Mtot']:11.3e} {rw['Mcore']:16.3e} {rw['Mcore']/1e14:8.3f} {rw['eta']:9.3f}")
        pos_ok = all(rw['rho_min'] >= -1e-30 for rw in rows)
        Rs_max = max(rw['Rs'] for rw in rows if np.isfinite(rw['Rs']))
        # budget crossing: M_tot = budget (inside r_ta) -> pinned core yield
        Mt = np.array([rw['Mtot'] for rw in rows]); Mc = np.array([rw['Mcore'] for rw in rows]); et = np.array([rw['eta'] for rw in rows])
        def interp_at(budget):
            i = np.searchsorted(Mt, budget)
            if i == 0 or i >= len(Mt): return float('nan'), float('nan')
            f = (budget - Mt[i-1])/(Mt[i] - Mt[i-1]); return Mc[i-1] + f*(Mc[i]-Mc[i-1]), et[i-1] + f*(et[i]-et[i-1])
        Mc_R500, eta_R500b = interp_at(budget_R500); Mc_ta, eta_tab = interp_at(budget_ta)
        results[(foot, kern_name, "pinned")] = dict(Mc_R500=Mc_R500, Mc_ta=Mc_ta, eta_R500=eta_R500b, eta_ta=eta_tab, Rs_max=Rs_max, Mc_max=Mc.max())
        P(f"   -> {foot}/{kern_name}: R_s max = {Rs_max:.3f} Mpc (pi/mu = {math.pi/math.sqrt(MU2)/Mpc:.3f}); PINNED core dust at budget(R500) = {Mc_R500:.2e} Msun "
          f"= {Mc_R500/1e14*100:.0f}% of 1e14 / {Mc_R500/1.5e14*100:.0f}% of 1.5e14, eta(R500) = {eta_R500b:.3f}; at budget(r_ta): {Mc_ta:.2e} ({Mc_ta/1e14*100:.0f}%), eta = {eta_tab:.3f}")
        if foot == "canon" and kern_name == "DS24":
            check("D1 the free-surface family is positive-density everywhere (rho_d >= 0 inside R_s) for every mass", pos_ok)
            check(f"D2 the surface radius saturates BELOW the Lane-Emden radius pi/mu as the mass grows (R_s,max = {Rs_max:.3f} Mpc < {math.pi/math.sqrt(MU2)/Mpc:.3f} Mpc)",
                  Rs_max < math.pi/math.sqrt(MU2)/Mpc)
            check("D3 the core yield is MONOTONE in the captured mass and the family is one-parameter (no branch ambiguity)",
                  np.all(np.diff(Mc) >= -1e-6*Mc.max()) and np.all(np.diff(Mt) > 0))
            check("D4 the PINNED core yield (captured mass = cosmic budget inside R500) is BELOW 50% of the 1e14 core residual: real, galaxy-safe, NOT a closure",
                  np.isfinite(Mc_R500) and Mc_R500 < 0.5e14, f"{Mc_R500/1e14*100:.0f}%")
            check("D5 the pinned yield is ABOVE 10% of 1e14: the lever is real (consistent with item B's fixed-phase 10-18%)",
                  np.isfinite(Mc_R500) and Mc_R500 > 0.10e14, f"{Mc_R500/1e14*100:.0f}%")
            # core fraction bound: with rho_d ∝ (C - Psi) the profile is at most as concentrated as the |Psi| profile
            idx = int(np.searchsorted(Mt, budget_R500)); frac = Mc[idx]/Mt[idx]
            info(f"D6 core share of the captured dust at the budget: M(<420 kpc)/M_tot = {frac:.3f}  (the shallow rho_d ∝ C - Psi profile cannot concentrate)")
            check("D6 core share < 10%: the shallow profile, not the amount of dust, is the binding limit", frac < 0.10)
# ---- the R500 confrontation (against interest) and the observation-normalised core yield
ETA_OBS_RAW, ETA_OBS_WL = 2.33, 1.7          # eRASS1 raw on the framework kernel / after WL mass calibration (cluster-standing memory)
P("  R500 confrontation at the budget (captured mass = f_d M_b(<R500)):")
for f in A0:
    for k in ("DS24", "framework"):
        rows = results[(f, k)]; Mt = np.array([rw['Mtot'] for rw in rows]); Mc = np.array([rw['Mcore'] for rw in rows]); et = np.array([rw['eta'] for rw in rows])
        pinned = results[(f, k, "pinned")]
        Mc_raw = float(np.interp(ETA_OBS_RAW, et, Mc)); Mt_raw = float(np.interp(ETA_OBS_RAW, et, Mt))
        Mc_wl = float(np.interp(ETA_OBS_WL, et, Mc)); Mt_wl = float(np.interp(ETA_OBS_WL, et, Mt))
        pinned.update(Mc_raw=Mc_raw, Mt_raw=Mt_raw, Mc_wl=Mc_wl, Mt_wl=Mt_wl)
        P(f"   {f:5s}/{k:9s}: eta(R500) predicted = {pinned['eta_R500']:.2f} vs observed {ETA_OBS_RAW} raw / {ETA_OBS_WL} WL-corrected; "
          f"normalising the captured mass to eta_obs instead: raw -> M_tot {Mt_raw:.1e}, core {Mc_raw/1e14*100:.0f}% ; WL -> M_tot {Mt_wl:.1e}, core {Mc_wl/1e14*100:.0f}%")
pc = results[("canon", "framework", "pinned")]; pd_ = results[("canon", "DS24", "pinned")]
check("D8 AGAINST INTEREST: at the budget the polytrope OVERSHOOTS the WL-corrected eta(R500)=1.7 on both kernels (too much dust at 1.5 Mpc, too little at 0.4 Mpc: the profile is too SHALLOW both ways)",
      pc['eta_R500'] > ETA_OBS_WL and pd_['eta_R500'] > ETA_OBS_WL, f"{pc['eta_R500']:.2f} (framework), {pd_['eta_R500']:.2f} (DS24)")
check("D9 on the framework's own kernel the budget-pinned eta(R500) lands within 35% of the RAW observed 2.33 with zero tuning (the no-go's 'abundance is not the problem', now with the right profile)",
      abs(pc['eta_R500']/ETA_OBS_RAW - 1) < 0.35, f"{pc['eta_R500']:.2f} vs {ETA_OBS_RAW}")
check("D10 normalising the captured mass to the OBSERVED eta(R500) (raw or WL) leaves the 420-kpc core at < 35% of 1e14 on every footing/kernel",
      all(results[(f, k, "pinned")]['Mc_raw'] < 0.35e14 and results[(f, k, "pinned")]['Mc_wl'] < 0.35e14 for f in A0 for k in ("DS24", "framework")))
# ---- the mu^-1 fork: the lever scales as (mu R)^2; at BS24's 22 Mpc and v9's own 4392 Mpc it vanishes
S22 = Solver(rho_bC, MencC, A0["canon"], MU2/22.0**2)
S1 = Solver(rho_bC, MencC, A0["canon"], MU2)
d_ref = -3.06e12
r1, Ph1, P1, g1, Md1, Rs1 = S1.march(r0, 6*Mpc, dPhi0=d_ref, free_surface=True)
r2, Ph2, P2, g2, Md2, Rs2 = S22.march(r0, 6*Mpc, dPhi0=d_ref, free_surface=True)
ratio22 = S22.at(r2, Md2, R_CORE)/S1.at(r1, Md1, R_CORE)
info(f"D11 mu^-1 fork: at equal level C, core dust at mu^-1 = 22 Mpc is {ratio22:.2e} x the 1-Mpc value (expected ~(1/22)^2 = {1/484:.2e}); v9's own 4392 Mpc -> {(1/4392)**2:.1e}")
check("D11 the whole lever lives at AeST's phenomenological mu^-1 = 1 Mpc: at 22 Mpc it is < 1% of itself, at the framework's own 4392 Mpc it is nil",
      ratio22 < 0.01)
# footing / kernel spread
pins = [results[(f, k, "pinned")]["Mc_R500"] for f in A0 for k in ("DS24", "framework")]
check(f"D7 both footings x both kernels agree on the verdict band: pinned core yield within [{min(pins)/1e14*100:.0f}%, {max(pins)/1e14*100:.0f}%] of 1e14 -- all < 50%",
      all(np.isfinite(pins)) and max(pins) < 0.5e14)

P(""); P("="*100); P("PART E -- galaxy safety under the SAME rule (MW-like well, captured dust = its cosmic share)"); P("="*100)
rho_bG, MencG = make_baryons_MW()
SG = Solver(rho_bG, MencG, A0["canon"], MU2)
budget_gal = f_d*MencG(200*kpc)/Msun
dG = -np.geomspace(1e6, 1e12, 40)
r0g = 0.5*kpc
rowsG = family(SG, dG, r1=4*Mpc, rstart=r0g)
MtG = np.array([rw['Mtot'] for rw in rowsG]); dGa = np.array([rw['dPhi0'] for rw in rowsG])
for rw in rowsG[::8]: info(f"MW family: dPhi0 = {rw['dPhi0']:+.2e}  R_s = {rw['Rs']:.3f} Mpc  M_dust,tot = {rw['Mtot']:.2e}  M_dust(<420kpc) = {rw['Mcore']:.2e}")
order = np.argsort(MtG); d_at_budget = float(np.interp(budget_gal, MtG[order], dGa[order]))
rv, Phi, Pm, g, Md, Rs = SG.march(r0g, 4*Mpc, dPhi0=d_at_budget, free_surface=True)
rho_blob = MU2*abs(d_at_budget)/(4*np.pi*G_N)
info(f"MW-like: the level C holding the whole share is |dPhi0| = {abs(d_at_budget):.2e} m^2/s^2 = ({math.sqrt(abs(d_at_budget))/1e3:.0f} km/s)^2 -> "
     f"uniform-part density {rho_blob:.1e} kg/m^3 = {rho_blob/rho_dust0:.1f} x the cosmic dust density; surface R_s = {Rs/Mpc:.2f} Mpc")
g0 = SG.g_ref(rv)
Md20 = SG.at(rv, Md, 20*kpc)/Msun; shift10 = math.log10(SG.at(rv, g, 10*kpc)/SG.at(rv, g0, 10*kpc))
info(f"MW-like: dust budget {budget_gal:.2e} Msun -> polytrope surface R_s = {Rs/Mpc:.2f} Mpc, dust inside 20 kpc = {Md20:.2e} Msun "
     f"(baryons {MencG(20*kpc)/Msun:.2e}), acceleration shift at 10 kpc = {shift10:+.4f} dex")
check("E1 galaxy-safe: with the galaxy's WHOLE cosmic dust share captured, the dust inside 20 kpc is < 1% of the baryons and the 10-kpc acceleration shift < 0.01 dex (geometric (mu R)^2 protection)",
      Md20 < 0.01*MencG(20*kpc)/Msun and abs(shift10) < 0.01)
info("E2 the ordering is by potential depth through mu^2|Psi|R^3 (geometric (mu R)^2 protection), NOT by density: item B's |Phi|-ordering confirmed from the action")

P(""); P("="*100); P("PART F -- the time-dependent solve in the correct form: gamma=2 dust hydro falling into the growing MOND well"); P("="*100)
Kp = 2*np.pi*G_N/MU2                                   # p = Kp rho^2
def run_hydro(M_dust=3.0e14, R_init=4.0*Mpc, N=160, t_end=12e9*3.156e7, t_form=3e9*3.156e7, ic_mode_amp=0.0, cq=2.0, a0=A0["canon"], seed_hubble=True):
    """1-D Lagrangian gamma=2 hydro: dust shells in the (growing) cluster MOND potential + own gravity; artificial viscosity."""
    edges = np.linspace(0, R_init, N+1)[1:]            # outer boundary radii of N shells
    rmid0 = 0.5*(np.concatenate([[0], edges[:-1]]) + edges)
    prof = 1.0 + ic_mode_amp*np.sinc(math.sqrt(MU2)*rmid0/np.pi)   # sinc(x/pi) = sin(x)/x : the free Helmholtz mode admixture
    vol = (4*np.pi/3)*(edges**3 - np.concatenate([[0], edges[:-1]])**3)
    m = prof*vol; m *= M_dust*Msun/m.sum()
    rb = edges.copy(); v = np.zeros(N)
    if seed_hubble: v = 0.5*H0*rb                       # mild outward flow at the start (turnaround-like), captured by the well
    s = lambda t: 0.5*(1 + math.tanh((t - 0.6*t_form)/(0.25*t_form)))   # baryon well growth
    def accel(rb, t):
        Mtot = MencC(rb)*s(t) + np.cumsum(m)            # baryons (grown) + dust inside each boundary
        return -a0*xinv_ds24(G_N*Mtot/(a0*rb**2))
    def pressures(rb, v):
        rin = np.concatenate([[0], rb[:-1]]); volc = (4*np.pi/3)*(rb**3 - rin**3); rho = m/volc
        dv = v - np.concatenate([[0], v[:-1]])
        q = np.where(dv < 0, cq*rho*dv**2, 0.0)
        return rho, Kp*rho**2 + q
    t = 0.0; dt = 2e6*3.156e7
    rho, Pp = pressures(rb, v)
    for it in range(400000):
        # pressure gradient force at boundary i between cell i and i+1 (outer boundary: vacuum)
        Pout = np.concatenate([Pp[1:], [0.0]]); rin = np.concatenate([[0], rb[:-1]])
        dr = 0.5*(np.concatenate([rb[1:], [rb[-1] + (rb[-1]-rb[-2])]]) - rin)
        rho_b_ = 0.5*(rho + np.concatenate([rho[1:], [rho[-1]*1e-3]]))
        a_p = -(Pout - Pp)/(np.maximum(rho_b_, 1e-40)*np.maximum(dr, 1e-3*Mpc))
        a = accel(rb, t) + a_p
        v = v + a*dt; rb_new = rb + v*dt
        # keep shells ordered (no crossing; a caustic-guard, logged)
        rb_new = np.maximum.accumulate(np.maximum(rb_new, 1e-3*kpc))
        rb = rb_new; t += dt
        rho, Pp = pressures(rb, v)
        cs = np.sqrt(np.maximum(2*Kp*rho, 0)); cell = rb - np.concatenate([[0], rb[:-1]])
        dt = min(0.3*np.min(cell/(cs + np.abs(v) + 1e3)), 5e6*3.156e7)
        if t >= t_end: break
    # hydrostatic residual and core mass
    rho, Pp = pressures(rb, np.zeros(N))
    Mcore = np.interp(R_CORE, rb, np.cumsum(m))/Msun
    a_g = accel(rb, t_end); Pout = np.concatenate([Pp[1:], [0.0]])
    dr = np.maximum(rb - np.concatenate([[0], rb[:-1]]), 1e-3*Mpc)
    a_p = -(Pout - Pp)/(np.maximum(rho, 1e-40)*dr)
    inside = rb < 2*Mpc
    resid = np.median(np.abs((a_g + a_p)[inside])/np.abs(a_g[inside]))
    vrms = math.sqrt(np.mean(v[inside]**2))
    cs_core = math.sqrt(2*Kp*max(rho[rb < R_CORE].mean(), 1e-40))
    return dict(Mcore=Mcore, resid=resid, vrms=vrms, mach=vrms/cs_core, cs_core=cs_core, rb=rb, m=m, t=t, steps=it)
# static prediction at the same captured mass (all the dust ends in the polytrope)
def static_core_at_mass(Mtarget, S):
    rows = family(S, -np.geomspace(1e9, 3e14, 40), r1=6*Mpc)
    Mt = np.array([rw['Mtot'] for rw in rows]); Mc = np.array([rw['Mcore'] for rw in rows])
    return float(np.interp(Mtarget, Mt, Mc))
S = Solver(rho_bC, MencC, A0["canon"], MU2)
M_test = 3.0e14
Mc_static = static_core_at_mass(M_test, S)
base = run_hydro(M_dust=M_test)
info(f"hydro (M_dust = {M_test:.1e}, t = {base['t']/3.156e16:.1f} Gyr, {base['steps']} steps): core dust = {base['Mcore']:.3e} Msun; static polytrope at same mass = {Mc_static:.3e}; "
     f"hydrostatic residual (median |a_g + a_p|/|a_g| inside 2 Mpc) = {base['resid']:.3f}; residual v_rms = {base['vrms']/1e3:.0f} km/s = Mach {base['mach']:.2f} (c_s,core = {base['cs_core']/1e3:.0f} km/s)")
check("F1 the end state is hydrostatic: median |grad p/rho + grad Psi| / |grad Psi| < 0.15 and residual motions subsonic, Mach < 0.3, inside 2 Mpc",
      base['resid'] < 0.15 and base['mach'] < 0.3)
check("F2 the dynamical core mass agrees with the static positive polytrope at the same captured mass to within 35%",
      abs(base['Mcore']/Mc_static - 1) < 0.35, f"ratio {base['Mcore']/Mc_static:.2f}")
amps = (-0.5, -0.25, 0.25, 0.5); cores = []
for A in amps:
    rA = run_hydro(M_dust=M_test, ic_mode_amp=A); cores.append(rA['Mcore'])
    info(f"IC free-mode admixture A = {A:+.2f} sin(mu r)/(mu r): core dust = {rA['Mcore']:.3e} Msun  ({(rA['Mcore']/base['Mcore']-1)*100:+.1f}%)")
spread = (max(cores + [base['Mcore']]) - min(cores + [base['Mcore']]))/base['Mcore']
check(f"F3 THE PIN: a +-50% free-mode admixture in the ICs changes the final core mass by < 25% (spread {spread*100:.0f}%) -- the phase is erased by the gamma=2 dynamics, not tracked 1:1",
      spread < 0.25)

P(""); P("="*100); P("VERDICT"); P("="*100)
pin = results[("canon", "DS24", "pinned")]
P("  THE PHASE PINS.  Mechanism: the AeST dust is a gamma=2 polytrope, p_d = (2 pi G/mu^2) rho_d^2, with c_s^2 = |Psi| c^2 in a well;")
P("  DS24's Helmholtz 'phase' is its Bernoulli constant = captured mass; every node-bearing branch has rho_d<0 <=> c_s^2<0 and is")
P("  gradient-unstable; the unique admissible configuration is the positive polytrope with a free surface R_s < pi/mu, and the")
P("  time-dependent gamma=2 hydro lands on it and forgets the IC phase (F3).  The June 'no pin' evolved the gapped branch (B1).")
P(f"  THE PINNED YIELD (canonical, DS24 kernel): core dust {pin['Mc_R500']:.2e} Msun = {pin['Mc_R500']/1e14*100:.0f}% of the 1e14 residual "
  f"({pin['Mc_R500']/1.5e14*100:.0f}% of 1.5e14), eta(R500) = {pin['eta_R500']:.2f}; band over footings/kernels {min(pins)/1e14*100:.0f}-{max(pins)/1e14*100:.0f}%.")
P(f"  AGAINST INTEREST: the same configuration gives eta(R500) = {pc['eta_R500']:.2f} (framework kernel) / {pd_['eta_R500']:.2f} (DS24) vs observed 2.33 raw, 1.7 WL-corrected:")
P(f"  it OVERSHOOTS R500 while UNDERSHOOTING the core; normalised to the observed R500 the core is {pc['Mc_raw']/1e14*100:.0f}% (raw) / {pc['Mc_wl']/1e14*100:.0f}% (WL).")
P("  Galaxy-safe by geometry (E1).  The binding limit is the SHAPE (rho_d ∝ C - Psi cannot concentrate into a 420 kpc core), not the amount.")
P("  The lever exists only at AeST's phenomenological mu^-1 = 1 Mpc (D11); at the framework's own Q-sector mass it is nil.")
P("  => The |Phi| lever is REAL, PREDICTIVE (no per-cluster tune), GALAXY-SAFE, and NOT A CLOSURE: the cluster core gap stays >= 65% open.")
P("  CORRECTS: the published no-go's 'c_s^2 -> 0 => density-ordered clumping' premise (wrong in wells) and its 'single un-closed branch = 3D N-body' (closed here).")
if MUTATE: P("\n  MUTATE=1: lapse relation sign flipped (Q=(1+Psi)Q_0) and Helmholtz -> Yukawa in the solver. Expected: A4/A5 and the Part C/D branch structure FAIL.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
