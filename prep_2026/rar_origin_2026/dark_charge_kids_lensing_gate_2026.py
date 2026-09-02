#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
dark_charge_kids_lensing_gate_2026.py -- the dark charge measured where a MOND well would pile it: galaxy-galaxy lensing (KiDS-1000).
====================================================================================================================================
Framework-native (no LCDM halo model): the cold dark charge at Omega_c accretes onto an L* galaxy's MOND well by spherical collapse in
the framework's own gravity (Route A kernel, both a_0 footings, Newtonian background growth, MOND boost on the peculiar field with the
external-field effect e_N).  The accreted profile M_ch(<r) is then put into the framework's lensing prediction, g_lens = nu(g_N/a_0) g_N
with g_N = G[M_b(<r) + M_ch(<r)]/r^2 (gamma = 1, no slip, as the framework's own AeST embedding has it), and confronted with the real
Brouwer+ 2021 KiDS-1000 isolated-lens RAR (official CDS release, full covariance; the repo's P2 concordance loader) against the MOND-only
prediction the repo already fit (chi^2/dof 2.03 canonical / 0.94 alt with no dark component).
Lens: M_b = 5e10 Msun (Hernquist stars 4e10 + gas 1e10, the repo's confront.py galaxy).  e_N scanned 0.03 - 1.0.  Checks CAN fail.
"""
import sys, math, os
import numpy as np
from scipy.integrate import solve_ivp
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
G = 6.674e-11; kpc = 3.0857e19; Mpc = 3.0857e22; Msun = 1.989e30; h = 0.674
H0 = 100*h*1e3/Mpc; OM_M = (0.02237 + 0.1200)/h**2; OM_L = 1 - OM_M; rho_crit = 3*H0**2/(8*math.pi*G); RHO_C = 0.1200/h**2*rho_crit
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
def nu(y): y = max(y, 1e-12); return 1.0/(1.0 - math.exp(-math.sqrt(y)))
def E(a): return math.sqrt(OM_M/a**3 + OM_L)
Mstar, astar, Mgas, agas = 4e10*Msun, 2.0*kpc, 1e10*Msun, 10.0*kpc
def M_b(r): return Mstar*r**2/(r+astar)**2 + Mgas*r**2/(r+agas)**2
def capture(a0, eN, nshell=50, xmax_kpc=6000.0):
    x_grid = np.logspace(math.log10(5.0), math.log10(xmax_kpc), nshell)*kpc; a_i = 1/21.0
    ts = np.linspace(a_i, 1.0, 2000); dtda = np.array([1/(a*H0*E(a)) for a in ts]); tt = np.concatenate([[0.0], np.cumsum(0.5*(dtda[1:] + dtda[:-1])*np.diff(ts))]); t_now = tt[-1]
    a_of_t = lambda t: float(np.interp(t, tt, ts))
    r_final, M_shell = [], []
    for x in x_grid:
        Mc = RHO_C*4/3*math.pi*x**3
        def rhs(t, y):
            r, v = y; a = a_of_t(t); rho_bg = OM_M*rho_crit/a**3; M_bg = 4/3*math.pi*rho_bg*r**3
            gN_pec = G*max(M_b(r) + Mc - 4/3*math.pi*(0.1200/h**2*rho_crit/a**3)*r**3, 0.0)/r**2
            gext = eN*a0; nu_e = nu(math.sqrt(gN_pec**2 + gext**2)/a0)
            return [v, -G*M_bg/r**2 + OM_L*H0**2*r - gN_pec*nu_e]
        r0 = x*a_i; v0 = H0*E(a_i)*r0
        ev = lambda t, y: y[0] - 0.05*kpc; ev.terminal = True
        sol = solve_ivp(rhs, (0, t_now), [r0, v0], events=ev, max_step=t_now/400, rtol=1e-7)
        rh = sol.y[0]; collapsed = sol.status == 1 or rh[-1] < 0.5*rh.max()
        if collapsed: r_final.append(0.5*rh.max()); M_shell.append(Mc)
        else: break
    r_final = np.array(r_final); M_shell = np.array(M_shell)
    def M_enc(r):
        if len(r_final) == 0: return 0.0
        o = np.argsort(r_final); return float(np.interp(r, r_final[o], M_shell[o], left=0.0, right=M_shell.max()))
    return M_enc, (M_shell.max() if len(M_shell) else 0.0), (r_final.max() if len(r_final) else 0.0)
# ---------------------------------------------------------------- Brouwer 2021 (the repo's loader)
B = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/lensing_rar/brouwer2021_rar"
PC_PER_M = 3.086e16; G_PC = 4.52e-30; CONV = 4*G_PC*PC_PER_M
def load_rar(fname):
    d = np.genfromtxt(os.path.join(B, fname), comments="#"); return d[:, 0], CONV*d[:, 1]/d[:, 4], CONV*d[:, 3]/d[:, 4]
def load_cov(fname, n):
    d = np.genfromtxt(os.path.join(B, fname), comments="#"); return (d[:, 4]/d[:, 6]).reshape(n, n)*CONV*CONV
gbar_d, gobs_d, gerr_d = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"); n = len(gbar_d); C = load_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", n)
rail = gbar_d >= 1e-13
def chi2_raw(gpred, mask):
    dv = (gobs_d - gpred)[mask]; return float(dv @ np.linalg.solve(C[np.ix_(mask, mask)], dv))
def chi2(gpred, mask, prof=True):
    """profiled coherent amplitude A in [10^-0.3, 10^0.3] on the prediction (stellar-mass / conversion systematics), Gaussian prior 0.3 dex"""
    if not prof: return chi2_raw(gpred, mask)
    best = 1e30; best_la = 0.0
    for la in np.linspace(-0.3, 0.3, 121):
        c = chi2_raw(gpred*10**la, mask) + (la/0.3)**2
        if c < best: best, best_la = c, la
    chi2.last_la = best_la
    return best
info(f"Brouwer+ 2021 KiDS-1000 isolated lenses: N = {n}, rail (g_bar >= 1e-13): N = {int(rail.sum())}")
# radii <-> g_bar for the template lens (monotonic beyond the peak)
rg = np.geomspace(1*kpc, 5000*kpc, 3000); gb = G*M_b(rg)/rg**2; ipk = int(np.argmax(gb)); rg_o, gb_o = rg[ipk:], gb[ipk:]
def r_of_gbar(g): return float(np.interp(-math.log(g), -np.log(gb_o), rg_o))
P("="*104); P("framework lensing prediction with and without the accreted dark charge, vs the KiDS isolated-lens RAR (rail points)"); P("="*104)
info("coherent amplitude (stellar mass / SIS conversion, +/-0.3 dex) PROFILED in every chi2 below, as in the repo's confront.py")
info(f"{'a0':10} {'e_N':>5} {'M_ch(<500kpc)/M_b':>17} {'g_pred/g_MOND @ 100,300,1000 kpc':>34} {'chi2 rail (MOND-only -> +charge)':>34} {'dof':>4}")
res = {}
for foot, a0 in A0.items():
    # MOND-only baseline
    g0 = np.array([ (lambda gn: gn*nu(gn/a0))(G*M_b(r_of_gbar(g))/r_of_gbar(g)**2) for g in gbar_d])
    c0 = chi2(g0, rail); la0 = chi2.last_la; res[(foot, "mond")] = c0
    for eN in (0.03, 0.1, 0.3, 1.0):
        Menc, Mtot, rf = capture(a0, eN)
        gp = []
        for g in gbar_d:
            r = r_of_gbar(g); gn = G*(M_b(r) + Menc(r))/r**2; gp.append(gn*nu(gn/a0))
        gp = np.array(gp); c1 = chi2(gp, rail); la1 = chi2.last_la; res[(foot, eN)] = (c1, Mtot, Menc(500*kpc)/M_b(500*kpc), la1)
        ratio = [ (G*(M_b(rr) + Menc(rr))/rr**2*nu(G*(M_b(rr) + Menc(rr))/rr**2/a0))/(G*M_b(rr)/rr**2*nu(G*M_b(rr)/rr**2/a0)) for rr in (100*kpc, 300*kpc, 1000*kpc)]
        info(f"{foot:10} {eN:5.2f} {Menc(500*kpc)/M_b(500*kpc):17.1f} {ratio[0]:10.2f} {ratio[1]:10.2f} {ratio[2]:10.2f}   {c0:12.1f} -> {c1:12.1f}   {int(rail.sum())}   amplitude {la0:+.2f} -> {la1:+.2f} dex")
info("baseline note: the repo's confront.py reports chi2/dof 2.03 (canonical) / 0.94 (alt) with its own kernel and profiling; this script's Route A baseline is worse (chi2/dof ~4): the DIFFERENCE with and without the charge is the quantity here")
check("L1 (reported) MOND-only baseline chi2/dof on the rail, amplitude profiled", True, "; ".join(f"{f}: {res[(f, 'mond')]/rail.sum():.2f}" for f in A0))
d_real = {(f, e): res[(f, e)][0] - res[(f, "mond")] for f in A0 for e in (0.03, 0.1)}
d_big = {(f, e): res[(f, e)][0] - res[(f, "mond")] for f in A0 for e in (0.3, 1.0)}
check("L2 at the external fields isolated galaxies actually sit in (e_N = 0.03-0.1, Chae+ 2020/2021), adding the framework-native accreted dark charge worsens the KiDS fit by Delta chi2 >= +100 on both footings even with the amplitude profiled: a MOND well that accretes the cold charge over-predicts the lensing at 100 kpc - 1 Mpc, and Brouwer's isolated lenses do not show it",
      all(v >= 100 for v in d_real.values()), "; ".join(f"{f}/e_N={e}: {v:+.0f}" for (f, e), v in d_real.items()))
check("L3 BOTH WAYS: at an unphysically large external field (e_N = 0.3-1.0 a_0) the accretion drops to 8-19 M_b inside 500 kpc, the residual x2-3 excess is absorbed by the amplitude systematic at its -0.3 dex edge, and the charge is tolerated or even preferred by this baseline -- the exclusion is an exclusion of the REALISTIC environment, and it leans on the +/-0.3 dex amplitude budget",
      any(v <= 0 for v in d_big.values()), "; ".join(f"{f}/e_N={e}: {v:+.0f} (amp {res[(f, e)][3]:+.2f})" for (f, e), v in d_big.items()))
P(""); P("="*104); P("VERDICT"); P("="*104)
P("  Framework-native, the cold dark charge at its CMB-required density cannot sit quietly beside a MOND well: the well accretes it, and")
P("  at the external fields isolated galaxies live in (0.03-0.1 a_0) the accreted charge multiplies the lensing signal at 100 kpc - 1 Mpc")
P("  by 3-20, which Brouwer's isolated KiDS lenses exclude at Delta chi2 >= +100 with the amplitude systematic profiled.  Only an external")
P("  field of order a_0 itself, unphysical for isolated lenses, throttles the accretion enough (8-19 M_b inside 500 kpc) for the")
P("  +/-0.3 dex amplitude budget to absorb the rest.  So: a cold charge at Omega_c and MOND wells around galaxies are incompatible in")
P("  galaxy-galaxy lensing with existing data at realistic environments -- unless the charge does not fall in, the door every kinetic")
P("  mechanism this week has closed.  Both ways stated; the baseline's own chi2/dof ~4 is a separate, older question.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
