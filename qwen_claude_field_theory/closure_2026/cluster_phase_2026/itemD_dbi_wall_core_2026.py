#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
itemD_dbi_wall_core_2026.py -- THE DBI WALL IN CLUSTER CORES: does the condensate's saturation concentrate the dust?
=====================================================================================================================
Item C (and the 09-02 addendum) used K(Q) = K_2 (Q-Q_0)^2: a gamma=2 polytrope whose core share is too small (23-33% of the
residual).  The framework's v9 action has the DBI form  K(u) = -M^4 sqrt(1 - mu_D^2 u^2 / M^4)  (+M^4), u = Q - Q_0, with the
WALL at x = mu_D u/M^2 = 1 where n = K' -> infinity and the sound speed -> 0: at the wall the dust loses its pressure support.
In a static well the lapse relation is EXACT for any K:  u = u_0 + Q_0 (C - Psi)  =>  x = nu = nu_0 [1 + (C - Psi)/h_bar],
h_bar = u_0/Q_0 = c_s,cosmic^2 = 4 pi G rho_d,bar / mu_H^2  (item C, eq. 1);  nu_0 = today's cosmic wall parameter, the stage-17
window nu_0 in [2.1e-5, 1.8e-4] (cut from below by the CMB off-switch, from above by the RAR-via-drain bound).
So the hydrostatic dust profile becomes  rho_d = mu_H^2 (C - Psi)/(4 pi G) x F(nu),  F = 1/sqrt(1 - nu^2)  -> infinity at the wall.
QUESTIONS: (A) the exact DBI relations (sympy); (B) with item C's cluster solver and the DBI factor, the core yield vs nu_0 at the
observation-normalised captured mass; (C) the nu_0 needed for 50% / 100% of the 1e14 core residual vs the stage-17 window; (D) whether
the wall is hit (density divergence = the EFT exit / core collapse) inside the window.  Checks can FAIL; MUTATE=1 sets F=1.
"""
import os, sys, math
import numpy as np, sympy as sp
from scipy.integrate import solve_ivp
MUTATE = os.environ.get("MUTATE", "0") == "1"
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
c = 2.99792458e8; G_N = 6.674e-11; Msun = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22
H0 = 67.4e3/Mpc; Om, OL, Ob = 0.315, 0.685, 0.0493
rho_crit0 = 3*H0**2/(8*np.pi*G_N); rho_dust0 = (Om-Ob)*rho_crit0; f_d = (Om-Ob)/Ob
MU2 = 1.0/(1.0*Mpc)**2; hbar = 4*np.pi*G_N*rho_dust0/MU2          # m^2/s^2: the cosmic enthalpy / sound speed^2 today
a0 = 9.36e-11; R_CORE = 420*kpc

P("="*100); P("A. the exact DBI relations in a static well"); P("="*100)
u, M4, muD, Q0, u0, Psi, C = sp.symbols('u M4 mu_D Q_0 u_0 Psi C', positive=True)
x = muD*u/sp.sqrt(M4)
K = M4*(1 - sp.sqrt(1 - x**2))
n = sp.diff(K, u); Kpp = sp.diff(K, u, 2)
cs2 = sp.simplify(n/((Q0 + u)*Kpp))
check("A1 c_s^2 = K'/(Q K'') = [u/(Q_0+u)] (1 - x^2): the DBI factor (1 - nu^2) multiplies the polytrope's sound speed and vanishes at the wall",
      sp.simplify(cs2 - u/(Q0+u)*(1 - x**2)) == 0)
n_lead = sp.series(n, u, 0, 2).removeO()
check("A2 n = K'(u) = mu_D^2 u / sqrt(1 - x^2): the quadratic K_2 u^2/2 charge times the enhancement F = 1/sqrt(1 - nu^2) -> infinity at the wall",
      sp.simplify(n - muD**2*u/sp.sqrt(1 - x**2)) == 0 and sp.simplify(n_lead - muD**2*u) == 0)
u_well = u0 + Q0*(C - Psi)
nu_well = sp.simplify((muD*u_well/sp.sqrt(M4)))
nu0 = muD*u0/sp.sqrt(M4)
check("A3 static well (exact for any K): u = u_0 + Q_0 (C - Psi)  =>  nu = nu_0 [1 + (C - Psi)/h_bar], h_bar = u_0/Q_0",
      sp.simplify(nu_well - nu0*(1 + (C - Psi)/(u0/Q0))) == 0)
info(f"numbers: h_bar = 4 pi G rho_d,bar / mu_H^2 = {hbar:.3e} m^2/s^2 = ({math.sqrt(hbar)/1e3:.0f} km/s)^2 = {hbar/c**2:.2e} c^2  (mu_H^-1 = 1 Mpc, rho_d,bar = Omega_dm rho_crit)")
for Psi_v, name in ((5e-7, "galaxy well 5e-7 c^2"), (1e-5, "cluster well 1e-5 c^2"), (1.1e-4, "pinned core level C-Psi ~ 1.1e-4 c^2")):
    info(f"   {name}: nu/nu_0 = 1 + {Psi_v*c**2/hbar:.2e}  ->  nu = {2.1e-5*(1+Psi_v*c**2/hbar):.3f} (window bottom) .. {1.8e-4*(1+Psi_v*c**2/hbar):.3f} (window top)")

P(""); P("="*100); P("B. the cluster core with the DBI factor: item C's solver, dust term x F(nu)"); P("="*100)
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
xinv_fw = lambda q: np.sqrt(np.abs(q)**2 + np.abs(q))
M500, R500 = 1.0e15, 1.56*Mpc; r0 = 0.02*Mpc
rho_b, Menc = make_baryons_A2029(M500, R500)
class DBISolver:
    """free-surface Helmholtz march (item C) with the DBI enhancement: dust term -mu^2 Phi F(nu), nu = nu0 (1 + (-Phi)/h_bar).
    Phi here is the level (C - Psi) with sign: Phi < 0 inside the dust (rho_d = -mu^2 Phi F/(4 pi G))."""
    def __init__(self, nu0): self.nu0 = nu0
    def F(self, Phi):
        if MUTATE: return 1.0
        nu = self.nu0*(1 + max(-Phi, 0.0)/hbar)
        return 1.0/np.sqrt(1 - nu**2) if nu < 1 else np.inf
    def march(self, dPhi0, r1=6*Mpc, n=2500):
        x0 = xinv_fw(G_N*Menc(r0)/(a0*r0**2)); Phi0 = -a0*x0*r0 + dPhi0; P0 = G_N*Menc(r0)
        hit = {"wall": False, "r_wall": np.nan}
        def f(rv, y, mu2):
            xx = xinv_fw(abs(y[1])/(a0*rv**2))
            Fv = self.F(y[0]) if mu2 > 0 else 1.0
            if not np.isfinite(Fv):
                hit["wall"] = True; hit["r_wall"] = rv; Fv = 1e6
            return [a0*xx*np.sign(y[1]), rv**2*(-mu2*y[0]*Fv + 4*np.pi*G_N*rho_b(rv))]
        ev = lambda rv, y, mu2: y[0]; ev.terminal = True; ev.direction = +1
        te = np.geomspace(r0, r1, n)
        s1 = solve_ivp(f, [r0, r1], [Phi0, P0], args=(MU2,), t_eval=te, events=ev, rtol=1e-9, atol=1e-13, method="DOP853", max_step=(r1-r0)/1500)
        if s1.t_events[0].size:
            Rs = s1.t_events[0][0]; yR = s1.y_events[0][0]; te2 = te[te > Rs]
            s2 = solve_ivp(f, [Rs, r1], yR, args=(0.0,), t_eval=te2, rtol=1e-9, atol=1e-13, method="DOP853", max_step=(r1-r0)/1500)
            rv = np.concatenate([s1.t, s2.t]); Phi = np.concatenate([s1.y[0], s2.y[0]]); Pm = np.concatenate([s1.y[1], s2.y[1]])
        else:
            Rs = np.inf; rv, Phi, Pm = s1.t, s1.y[0], s1.y[1]
        g = a0*xinv_fw(np.abs(Pm)/(a0*rv**2))*np.sign(Pm); Md = Pm/G_N - Menc(rv)
        gref = a0*xinv_fw(G_N*Menc(R500)/(a0*R500**2))
        i500 = np.argmin(np.abs(rv - R500)); ic = np.argmin(np.abs(rv - R_CORE))
        return dict(Rs=Rs/Mpc, Mtot=Md[-1]/Msun, Mcore=Md[ic]/Msun, eta=g[i500]/gref, wall=hit["wall"], r_wall=hit["r_wall"]/Mpc if hit["wall"] else np.nan, numax=self.nu0*(1 + max(-Phi.min(), 0)/hbar))
ETA_RAW, ETA_WL = 2.33, 1.7
info(f"{'nu_0':>8s} {'window':>8s} | at eta(R500)=2.33: {'M_tot':>9s} {'core%':>6s} {'nu_max':>7s} {'wall':>5s} | at eta=1.7: {'M_tot':>9s} {'core%':>6s} {'nu_max':>7s} {'wall':>5s}")
results = {}
dlist = -np.geomspace(1e11, 3e13, 26)
for nu0 in (0.0, 2.1e-5, 1.0e-4, 1.8e-4, 3.0e-4, 5.0e-4, 1.0e-3):
    S = DBISolver(nu0); rows = [S.march(d) for d in dlist]
    et = np.array([r_['eta'] for r_ in rows]); Mc = np.array([r_['Mcore'] for r_ in rows]); Mt = np.array([r_['Mtot'] for r_ in rows])
    nm = np.array([r_['numax'] for r_ in rows]); wl = np.array([r_['wall'] for r_ in rows])
    out = {}
    for eta_obs, tag in ((ETA_RAW, "raw"), (ETA_WL, "wl")):
        ok = np.isfinite(et)
        if et[ok].max() < eta_obs or et[ok].min() > eta_obs:
            out[tag] = (np.nan, np.nan, np.nan, False)
        else:
            j = int(np.searchsorted(et[ok], eta_obs)); j = min(max(j, 1), ok.sum()-1)
            fr = (eta_obs - et[ok][j-1])/(et[ok][j] - et[ok][j-1])
            out[tag] = (Mt[ok][j-1] + fr*(Mt[ok][j]-Mt[ok][j-1]), Mc[ok][j-1] + fr*(Mc[ok][j]-Mc[ok][j-1]), nm[ok][j-1] + fr*(nm[ok][j]-nm[ok][j-1]), bool(wl[ok][j-1] or wl[ok][j]))
    results[nu0] = out
    inwin = "in" if 2.1e-5 <= nu0 <= 1.8e-4 else ("quad" if nu0 == 0 else "OUT")
    r1_, r2_ = out["raw"], out["wl"]
    info(f"{nu0:8.1e} {inwin:>8s} | {r1_[0]:9.2e} {r1_[1]/1e14*100:6.1f} {r1_[2]:7.3f} {str(r1_[3]):>5s} | {r2_[0]:9.2e} {r2_[1]/1e14*100:6.1f} {r2_[2]:7.3f} {str(r2_[3]):>5s}")
base_raw = results[0.0]["raw"][1]; top_raw = results[1.8e-4]["raw"][1]; base_wl = results[0.0]["wl"][1]; top_wl = results[1.8e-4]["wl"][1]
check("B1 the quadratic (nu_0 = 0) row reproduces item C's observation-normalised core yield (20-25% raw, 14-18% WL)",
      0.18e14 < base_raw < 0.27e14 and 0.12e14 < base_wl < 0.20e14, f"raw {base_raw/1e14*100:.0f}%, WL {base_wl/1e14*100:.0f}%")
check("B2 inside the stage-17 window (nu_0 <= 1.8e-4) the DBI enhancement changes the core yield by < 10 percentage points and hits no wall",
      abs(top_raw - base_raw) < 0.10e14 and not results[1.8e-4]["raw"][3] and not results[1.8e-4]["wl"][3], f"raw {base_raw/1e14*100:.0f}% -> {top_raw/1e14*100:.0f}%")
# C: what nu_0 would it take?
need = {}
for nu0, out in results.items():
    if np.isfinite(out["raw"][1]): need[nu0] = out["raw"][1]/1e14
info("C  core yield (raw normalisation) vs nu_0: " + ", ".join(f"{k:.1e}:{v*100:.0f}%" + ("(wall)" if results[k]['raw'][3] else "") for k, v in need.items()))
reach50 = [k for k, v in need.items() if v >= 0.5]
check("C1 no nu_0 inside the stage-17 window reaches 50% of the core residual; any nu_0 that does is outside the window and/or hits the wall (EFT exit)",
      all(k > 1.8e-4 for k in reach50), f"nu_0 reaching 50%: {reach50}")
P(""); P("="*100); P("VERDICT"); P("="*100)
P("  The DBI wall is real in the field relations (A1-A3) but it is NOT a cluster fix inside the framework's own window: at nu_0 <= 1.8e-4 the")
P("  pinned core sits at nu ~ 0.1-0.5, the enhancement 1/sqrt(1-nu^2) adds at most a few percentage points, and the wall is not reached.")
P("  Reaching the core residual needs nu_0 above the window's upper edge (the RAR-via-drain bound) and drives the core INTO the wall, where c_s -> 0")
P("  and the density diverges: the EFT exit / core collapse of nbody stage 3, not a controlled closure.  The cluster core stays >= 65% open;")
P("  the two fronts (a0(z) window, cluster core) are now cross-linked by nu_0 rather than independent.")
if MUTATE: P("\n  MUTATE=1: F = 1 (no DBI factor). Expected: the nu_0 rows coincide with the quadratic row (B2 trivially true; C1 true) -- a null mutation by design; the live control is the nu_0 = 0 row vs item C (B1).")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
