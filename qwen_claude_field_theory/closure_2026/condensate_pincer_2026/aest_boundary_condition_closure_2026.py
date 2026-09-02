#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
aest_boundary_condition_closure_2026.py -- AeST's free boundary constant is not free: charge conservation fixes it, and the fixed value
======================================================================================================================================
is excluded by the KiDS-1000 isolated-lens relation for EVERY value of the mass parameter.

The AeST quasistatic spherical system (Skordis & Zlosnik 2021 eqs. 5-6; Mistele, McGaugh & Hossenfelder 2023 eqs. 1a-1b, f_G = 1):
    (1/r^2)(r^2 Phi_hat')'                 = 4 pi G (rho_b + rho_c)
    (1/r^2)(r^2 mu_tilde(|phi'|/a_0) phi')' = 4 pi G (rho_b + rho_c)
    rho_c = (m^2 / 4 pi G) (C - Phi_hat - phi)                       [C = phi_dot/Q_0, the "chemical potential" of MMH23]
so that the total potential Phi = Phi_hat + phi obeys the Helmholtz-sourced MOND equation, the charge in the well is
rho_c = (m^2/4 pi G)(C - Phi), and the one integration constant is C.  MMH23 left C free per galaxy ("we do not know of any
mechanism that would result in these particular boundary conditions") and found that for m^2 >~ 1e-3 - 1 Mpc^-2 AeST departs from
MOND inside the KiDS radii.  The matching theorem (this programme) supplies the mechanism: rho_c is the conserved shift charge,
n proportional to a^-3, and the well holds whatever charge fell into it.  This script (i) solves the AeST system with C free (MMH23's
horn), (ii) fixes C so the well holds the charge the framework-native accretion delivers (spherical collapse in the same gravity,
external field e_N = 0.03-0.1, the repo's dark_charge_kids_lensing_gate), and (iii) counts the mass directly when the Helmholtz
arrangement cannot hold it in equilibrium.  Confronted with Brouwer+ 2021 KiDS-1000 isolated lenses, full covariance, coherent
amplitude +/-0.3 dex profiled, both a_0 footings.  Checks CAN fail.  Mutation: zero charge must reproduce the MOND-only chi^2.
"""
import sys, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
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
# ---------------------------------------------------------------- framework-native accretion (the repo's gate, verbatim)
def capture(a0, eN, nshell=50, xmax_kpc=6000.0):
    x_grid = np.logspace(math.log10(5.0), math.log10(xmax_kpc), nshell)*kpc; a_i = 1/21.0
    ts = np.linspace(a_i, 1.0, 2000); dtda = np.array([1/(a*H0*E(a)) for a in ts]); tt = np.concatenate([[0.0], np.cumsum(0.5*(dtda[1:] + dtda[:-1])*np.diff(ts))]); t_now = tt[-1]
    a_of_t = lambda t: float(np.interp(t, tt, ts))
    r_final, M_shell = [], []
    for x in x_grid:
        Mc = RHO_C*4/3*math.pi*x**3
        def rhs(t, y):
            r, v = y; a = a_of_t(t); rho_bg = OM_M*rho_crit/a**3; M_bg = 4/3*math.pi*rho_bg*r**3
            gN_pec = G*max(M_b(r) + Mc - 4/3*math.pi*(RHO_C/a**3)*r**3, 0.0)/r**2
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
    return M_enc
# ---------------------------------------------------------------- Brouwer 2021 (the repo's loader)
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "real_research", "data", "lensing_rar", "brouwer2021_rar")
PC_PER_M = 3.086e16; G_PC = 4.52e-30; CONV = 4*G_PC*PC_PER_M
def load_rar(fname):
    d = np.genfromtxt(os.path.join(B, fname), comments="#"); return d[:, 0], CONV*d[:, 1]/d[:, 4], CONV*d[:, 3]/d[:, 4]
def load_cov(fname, n):
    d = np.genfromtxt(os.path.join(B, fname), comments="#"); return (d[:, 4]/d[:, 6]).reshape(n, n)*CONV*CONV
gbar_d, gobs_d, gerr_d = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"); n = len(gbar_d); C = load_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", n)
rail = gbar_d >= 1e-13; allm = np.ones(n, bool)
def chi2_raw(gpred, mask):
    dv = (gobs_d - gpred)[mask]; return float(dv @ np.linalg.solve(C[np.ix_(mask, mask)], dv))
def chi2(gpred, mask):
    best = 1e30; best_la = 0.0
    for la in np.linspace(-0.3, 0.3, 121):
        c = chi2_raw(gpred*10**la, mask) + (la/0.3)**2
        if c < best: best, best_la = c, la
    chi2.last_la = best_la; return best
rg = np.geomspace(1*kpc, 5000*kpc, 3000); gb = G*M_b(rg)/rg**2; ipk = int(np.argmax(gb)); rg_o, gb_o = rg[ipk:], gb[ipk:]
def r_of_gbar(g): return float(np.interp(-math.log(g), -np.log(gb_o), rg_o))
r_data = np.array([r_of_gbar(g) for g in gbar_d])
info(f"Brouwer+ 2021 KiDS-1000 isolated lenses: N = {n}; rail g_bar >= 1e-13: N = {int(rail.sum())} (template lens M_b = 5e10 Msun: r = {r_data[rail].min()/kpc:.0f}-{r_data[rail].max()/kpc:.0f} kpc; all points to {r_data.max()/kpc:.0f} kpc)")
# ---------------------------------------------------------------- the AeST spherical system, outward integration
R_MAX = 3.5*Mpc; R_MIN = 0.05*kpc
def aest_solve(m2_Mpc, D0, a0):
    """state y = [M_c(<r), D = C - Phi(r)];  rho_c = m^2 D/(4 pi G);  Phi' = g_tot = nu(g_N/a0) g_N,  g_N = G(M_b + M_c)/r^2.
    Returns callables M_c(r), g_tot(r) on a dense grid.  D0 = C - Phi(0) is the boundary constant (MMH23's chemical potential)."""
    m2 = m2_Mpc/Mpc**2
    def rhs(r, y):
        Mc, D = y; gN = G*(M_b(r) + Mc)/r**2; gt = gN*nu(gN/a0)
        return [m2*r**2*D/G, -gt]
    rr = np.geomspace(R_MIN, R_MAX, 1200)
    sol = solve_ivp(rhs, (R_MIN, R_MAX), [0.0, D0], t_eval=rr, method="Radau", rtol=1e-7, atol=[1e20, 1e-3])
    Mc = sol.y[0]; gN = G*(M_b(rr) + Mc)/rr**2; gt = np.array([g*nu(g/a0) for g in gN])
    return (lambda r: float(np.interp(r, rr, Mc))), (lambda r: float(np.interp(r, rr, gt))), rr, Mc, sol.y[1]
def gpred_from(gfun): return np.array([gfun(r) for r in r_data])
def gpred_mass(Menc, a0):
    out = []
    for r in r_data:
        gN = G*(M_b(r) + Menc(r))/r**2; out.append(gN*nu(gN/a0))
    return np.array(out)
M2_SCAN = [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0]           # Mpc^-2  (mu^-1 = 100 Mpc ... 0.1 Mpc)
R_MATCH = 250*kpc
P("="*118); P("0. MOND-only baseline (no charge) and the accreted charge the framework delivers"); P("="*118)
base = {}; acc = {}
for foot, a0 in A0.items():
    g0 = gpred_mass(lambda r: 0.0, a0); base[foot] = (chi2(g0, rail), chi2.last_la, chi2(g0, allm), chi2.last_la)
    info(f"{foot:10} MOND-only: chi2 rail = {base[foot][0]:.1f} (amp {base[foot][1]:+.2f} dex), chi2 all = {base[foot][2]:.1f} (amp {base[foot][3]:+.2f} dex)")
    for eN in (0.03, 0.1, 0.3):
        Menc = capture(a0, eN); acc[(foot, eN)] = Menc
        info(f"{foot:10} accreted charge at e_N = {eN:4.2f}: M_c(<100 kpc)/M_b = {Menc(100*kpc)/M_b(100*kpc):6.1f}   M_c(<250 kpc)/M_b = {Menc(R_MATCH)/M_b(R_MATCH):6.1f}   M_c(<1 Mpc)/M_b = {Menc(Mpc)/M_b(Mpc):6.1f}")
# mutation: zero charge through the AeST solver reproduces the MOND-only chi2
mut_ok = True; mut_note = []
for foot, a0 in A0.items():
    rr0 = np.geomspace(R_MIN, R_MAX, 4000); g0r = np.array([G*M_b(r)/r**2*nu(G*M_b(r)/r**2/a0) for r in rr0]); Phi0m = -float(np.trapz(g0r, rr0))
    for D0 in (0.0, abs(Phi0m), -abs(Phi0m)):
        Mc, gt, *_ = aest_solve(1e-12, D0, a0); c = chi2(gpred_from(gt), rail); mut_note.append(f"{c:.2f}")
        if abs(c - base[foot][0]) > 0.01*base[foot][0]: mut_ok = False
check("M0 mutation control: m^2 -> 0 (no Helmholtz charge) reproduces the MOND-only chi2 on the rail to 1% for any boundary constant, both footings", mut_ok, "chi2 = " + ", ".join(mut_note))
info("note: C = Phi(0) is NOT zero charge in AeST -- D = C - Phi falls below zero outward and the well acquires negative charge (the oscillatory regime of VSB24 / the negative density of DS24); only m^2 -> 0 switches the charge off")
P(""); P("="*118); P("1. HORN 1 (MMH23): C free per galaxy.  For each m^2, the best boundary constant vs the KiDS rail (and vs all 15 points)"); P("="*118)
info(f"{'a0':10} {'m^2 [Mpc^-2]':>12} {'mu^-1':>9} {'best D0/Phi0':>12} {'M_c(<250)/M_b':>13} {'chi2 rail: MOND -> best':>24} {'Dchi2':>7} {'chi2 all: MOND -> best':>23} {'Dchi2':>7}")
horn1 = {}; horn1_all = {}
for foot, a0 in A0.items():
    rr0 = np.geomspace(R_MIN, R_MAX, 4000); g0r = np.array([G*M_b(r)/r**2*nu(G*M_b(r)/r**2/a0) for r in rr0]); Phi0 = -float(np.trapz(g0r, rr0))   # MOND well depth, C = 0 at 3.5 Mpc
    for m2 in M2_SCAN:
        best = (1e30, None, None, None, None); best_all = (1e30, None, None, None)
        for f in np.concatenate([-np.geomspace(1e-3, 30, 25)[::-1], [0.0], np.geomspace(1e-3, 30, 25)]):
            D0 = f*abs(Phi0)
            Mc, gt, *_ = aest_solve(m2, D0, a0); gp = gpred_from(gt); c_r = chi2(gp, rail); c_a = chi2(gp, allm)
            if c_r < best[0]: best = (c_r, f, Mc(R_MATCH)/M_b(R_MATCH), c_a, D0)
            if c_a < best_all[0]: best_all = (c_a, f, Mc(R_MATCH)/M_b(R_MATCH), c_r)
        horn1[(foot, m2)] = best; horn1_all[(foot, m2)] = best_all
        info(f"{foot:10} {m2:12.0e} {1/math.sqrt(m2):7.2f} Mpc {best[1]:12.3g} {best[2]:13.2f} {base[foot][0]:11.1f} -> {best[0]:8.1f} {best[0]-base[foot][0]:+7.1f} {base[foot][2]:11.1f} -> {best[3]:8.1f} {best[3]-base[foot][2]:+7.1f}   | best over ALL 15: D0/Phi0 = {best_all[1]:.3g}, M_c(<250)/M_b = {best_all[2]:.2f}, chi2 all {base[foot][2]:.1f} -> {best_all[0]:.1f} ({best_all[0]-base[foot][2]:+.1f}), its rail chi2 {best_all[3]:.1f} ({best_all[3]-base[foot][0]:+.1f})")
small = [horn1[(f, m2)][0] - base[f][0] for f in A0 for m2 in (1e-4, 1e-3)]
check("H1a (MMH23's small-m^2 limit) for m^2 <= 1e-3 Mpc^-2 (mu^-1 >= 30 Mpc) a free constant exists for which AeST is at least as good as MOND on the rail (Delta chi2 <= +1), both footings",
      all(x <= 1.0 for x in small), "Delta chi2 = " + ", ".join(f"{x:+.2f}" for x in small))
big = [horn1[(f, m2)][0] - base[f][0] for f in A0 for m2 in (10.0, 100.0)] + [horn1_all[(f, m2)][0] - base[f][2] for f in A0 for m2 in (10.0, 100.0)]
check("H1b (MMH23's tension reproduced) for m^2 >= 10 Mpc^-2 (mu^-1 <= 0.3 Mpc) NO constant brings AeST within Delta chi2 < +10 of MOND, on the rail or on all 15 points, both footings",
      all(x >= 10 for x in big), "Delta chi2 (rail; all) = " + ", ".join(f"{x:+.1f}" for x in big))
works = [(f, m2, horn1[(f, m2)][0] - base[f][0], horn1[(f, m2)][2], horn1[(f, m2)][3] - base[f][2]) for f in A0 for m2 in (1e-2, 1e-1, 1.0)]
check("H1c (a WORKS for AeST with C free, both ways) for m^2 = 1e-2 - 1 Mpc^-2 a constant exists that IMPROVES the rail fit over MOND by Delta chi2 <= -10 with ~1-2 M_b of charge inside 250 kpc -- but that same constant wrecks the outer 8 points by Delta chi2 >= +100: the rail's preference for extra mass at 100-250 kpc cannot be met by a Helmholtz charge without over-filling 0.3-2 Mpc",
      all(w[2] <= -10 and w[4] >= 100 for w in works), "; ".join(f"{w[0]}/m2={w[1]:.0e}: rail {w[2]:+.1f} (M_c/M_b={w[3]:.2f}), all {w[4]:+.0f}" for w in works))
allfit = [horn1_all[(f, m2)][0] - base[f][2] for f in A0 for m2 in M2_SCAN if m2 >= 1e-2]
info("H1d (reported) best-over-all-15 Delta chi2 for m^2 >= 1e-2: " + ", ".join(f"{x:+.1f}" for x in allfit) + "  -- MMH23's statement that deviations set in inside the KiDS range unless m^2 <~ 1e-3 - 1 Mpc^-2 (their 1e-15 vs 1e-13 cuts)")
P(""); P("="*118); P("2. HORN 2 (this programme): C fixed by charge conservation.  The well holds the charge that fell in (M_c(<250 kpc) = accreted), for every m^2"); P("="*118)
info("2a Helmholtz arrangement: D0 solved so that M_c(<250 kpc) matches the accretion; the required C - Phi(0) in units of the MOND well depth says whether the charge can sit in quasistatic equilibrium at all (|D0/Phi0| ~ 1) or is a dynamical pile-up (|D0/Phi0| >> 1)")
info(f"{'a0':10} {'e_N':>5} {'m^2':>7} {'D0/Phi0 needed':>15} {'M_c(<100)/M_b':>13} {'M_c(<1Mpc)/M_b':>14} {'chi2 rail: MOND -> fixed':>25} {'Dchi2':>8} {'amp':>6}")
horn2 = {}; cap = {}
for foot, a0 in A0.items():
    rr0 = np.geomspace(R_MIN, R_MAX, 4000); g0r = np.array([G*M_b(r)/r**2*nu(G*M_b(r)/r**2/a0) for r in rr0]); Phi0 = -float(np.trapz(g0r, rr0))
    for eN in (0.03, 0.1, 0.3):
        Menc = acc[(foot, eN)]; target = Menc(R_MATCH)
        for m2 in M2_SCAN:
            fM = lambda lf: aest_solve(m2, 10**lf*abs(Phi0), a0)[0](R_MATCH) - target
            try: lf = brentq(fM, -6, 12, xtol=1e-4)
            except ValueError: lf = float("nan")
            if math.isnan(lf): horn2[(foot, eN, m2)] = None; info(f"{foot:10} {eN:5.2f} {m2:7.0e}   no equilibrium solution holds the charge"); continue
            D0 = 10**lf*abs(Phi0); Mc, gt, *_ = aest_solve(m2, D0, a0); gp = gpred_from(gt); c_r = chi2(gp, rail); la = chi2.last_la
            horn2[(foot, eN, m2)] = (c_r, 10**lf, Mc(100*kpc)/M_b(100*kpc), Mc(Mpc)/M_b(Mpc), la)
            info(f"{foot:10} {eN:5.2f} {m2:7.0e} {10**lf:15.3g} {Mc(100*kpc)/M_b(100*kpc):13.1f} {Mc(Mpc)/M_b(Mpc):14.1f} {base[foot][0]:12.1f} -> {c_r:9.1f} {c_r-base[foot][0]:+8.1f} {la:+6.2f}")
        # 2b direct mass count with the accreted profile itself (arrangement-independent)
        gp = gpred_mass(Menc, a0); c_r = chi2(gp, rail); la = chi2.last_la; cap[(foot, eN)] = (c_r, la)
        info(f"{foot:10} {eN:5.2f} {'profile':>7} {'(accreted M_c(<r) as is)':>15} {Menc(100*kpc)/M_b(100*kpc):13.1f} {Menc(Mpc)/M_b(Mpc):14.1f} {base[foot][0]:12.1f} -> {c_r:9.1f} {c_r-base[foot][0]:+8.1f} {la:+6.2f}")
real = [(k, v) for k, v in horn2.items() if k[1] in (0.03, 0.1) and v is not None]
check("H2a at the external fields isolated galaxies live in (e_N = 0.03-0.1), the charge-fixed AeST well is excluded on the KiDS rail at Delta chi2 >= +100 for EVERY m^2 from 1e-4 to 100 Mpc^-2, both footings, amplitude profiled",
      len(real) == 2*2*len(M2_SCAN) and all(v[0] - base[k[0]][0] >= 100 for k, v in real), f"min Delta chi2 = {min(v[0]-base[k[0]][0] for k, v in real):+.0f} over {len(real)} cases")
need = [v[1] for k, v in real if k[2] <= 0.1]; need1 = [v[1] for k, v in real if k[2] == 1.0]
check("H2b for m^2 <= 0.1 Mpc^-2 (mu^-1 >= 3 Mpc, MMH23's lensing-allowed range) the constant needed to hold the accreted charge is C - Phi(0) >= 25x the MOND well depth (5-10x at m^2 = 1): the charge cannot sit in quasistatic equilibrium there, it is a dynamical pile-up, and the mass count (2b) is the operative prediction",
      all(x >= 25 for x in need), f"min D0/|Phi0| = {min(need):.3g} (m^2 <= 0.1); {min(need1):.3g}-{max(need1):.3g} at m^2 = 1")
direct = [cap[(f, e)][0] - base[f][0] for f in A0 for e in (0.03, 0.1)]
check("H2c the arrangement-independent mass count (accreted profile as is) is excluded at Delta chi2 >= +100 at e_N = 0.03-0.1, both footings (the repo's gate, re-derived here)",
      all(x >= 100 for x in direct), "Delta chi2 = " + ", ".join(f"{x:+.0f}" for x in direct))
loose = [cap[(f, 0.3)][0] - base[f][0] for f in A0] + [v[0] - base[k[0]][0] for k, v in horn2.items() if k[1] == 0.3 and v is not None]
check("H2d BOTH WAYS: at an unphysical external field e_N = 0.3 the accretion is throttled and at least one configuration is absorbed by the +/-0.3 dex amplitude budget (Delta chi2 <= +4): the closure is a closure of the realistic environment, and it leans on the amplitude budget exactly as the repo's gate does",
      any(x <= 4 for x in loose), f"min Delta chi2 at e_N = 0.3 = {min(loose):+.1f}")
P(""); P("="*118); P("VERDICT"); P("="*118)
P("  MMH23 showed AeST departs from MOND at KiDS radii unless m^2 <~ 1e-3 - 1 Mpc^-2 AND each galaxy's boundary constant C is tuned, and")
P("  said no mechanism was known to set C.  The matching theorem is the mechanism: the well's charge is the conserved shift charge that")
P("  fell in.  With C fixed that way, AeST is excluded on the KiDS-1000 isolated rail at Delta chi2 >= +100 for every m^2 from 1e-4 to")
P("  100 Mpc^-2 and both a_0 footings, at the external fields isolated galaxies actually sit in (0.03-0.1 a_0).  For the m^2 MMH23's")
P("  lensing horn allows, the charge cannot even sit in quasistatic equilibrium (C - Phi(0) >= 10 well depths): it is a pile-up, and")
P("  the mass count is what lensing sees.  Both ways: an external field of order 0.3 a_0, unphysical for isolated lenses, throttles the")
P("  accretion into the +/-0.3 dex amplitude budget.  Closure of AeST at galaxy-lensing scales given (a) the accretion estimate (spherical")
P("  collapse, EFE, no N-body of AeST exists) and (b) the +/-0.3 dex amplitude budget; horn 1 is MMH23's, horn 2 is this programme's.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
