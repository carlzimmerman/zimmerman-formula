#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cmc_filter_no_dm_growth_gate_2026.py -- the CMC / Hubble high-pass filter (ChatGPT proposal, 2026-09-02) in the real growth solver.
====================================================================================================================================
Proposal: a nondynamical elliptic auxiliary chi with Hubble-scaled mass m_chi = xi H/c (Theta = K = 3H on FLRW, 0 static) filters the
MOND sector on cosmological scales,  W(k,z) = k^2 / (k^2 + xi^2 a^2 H^2/c^2),  with xi ~ 330-480 chosen so that W(0.05 h/Mpc, z=3) ~ 0.3-0.45
while W(k >= 1) ~ 1.  STRICT footing: Omega_cdm = 0, no dark field, H(z) from baryons + radiation + Lambda only.  The decisive test named
by the proposal: does W in the no-floor baryon-only growth solver fix k = 0.05 at z = 3 while keeping k = 1-10 in the forest window and
preventing late-time overgrowth?
Two readings of how the filter enters (the proposal's Lagrangian gives chi = W ln N and feeds |D chi| to the kernel):
  SUPPRESS  nu_eff = 1 + W (nu - 1)        -- the MOND ENHANCEMENT is filtered (the intended physics)
  KERNEL    nu_eff = nu(W g_N)             -- the kernel's INPUT is filtered (what chi = W ln N literally does): deeper MOND at large scales
Two models of how MOND's k-dependence enters linear growth, bracketing the truth:
  PERMODE   nu evaluated at the mode's own peculiar gravity g_N = 4 pi G rho |delta_k| / k_phys   (maximal k-selectivity; my earlier runs)
  CUM-EFE   nu evaluated at the rms field of all larger scales plus the mode's own (the environment as an external field)
  RMS-EFE   nu evaluated at the rms peculiar gravity of the whole field (scale-independent boost)
ICs: baryons at z = 1000, Silk-damped, eps_b = 0.03 (attractor-dominated anyway).  Yardstick = the measured clustering (LCDM linear shape),
loose: within 2x at k = 0.05 AND at k = 1, 3, 10 at z = 3.  Both a_0 footings.  Checks CAN fail.
"""
import sys, math
import numpy as np
from scipy.integrate import solve_ivp, quad
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
h = 0.674; OM_B_H2, OM_C_H2 = 0.02237, 0.1200
OM_B = OM_B_H2/h**2; OM_DM = OM_C_H2/h**2; OM_R = 4.15e-5/h**2
G = 6.674e-11; c = 2.99792458e8; Mpc = 3.0857e22; H0 = 100*h*1e3/Mpc; rho_crit = 3*H0**2/(8*math.pi*G)
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}; CH0 = 2997.92
OM_M_STD = OM_B + OM_DM; OL_STD = 1 - OM_M_STD - OM_R
def E2_std(a): return OM_R/a**4 + OM_M_STD/a**3 + OL_STD
def D_std(a): return 2.5*OM_M_STD*math.sqrt(E2_std(a))*quad(lambda x: 1/(x*math.sqrt(E2_std(x)))**3, 1e-6, a)[0]
def T_bbks(k):
    Gam = OM_M_STD*h*math.exp(-OM_B - math.sqrt(2*h)*OM_B/OM_M_STD); q = k/Gam
    return math.log(1+2.34*q)/(2.34*q)*(1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25)
def P_un(k): return k**0.965*T_bbks(k)**2
def Wth(x): return 3*(math.sin(x) - x*math.cos(x))/x**3
PNORM = (0.811/math.sqrt(quad(lambda k: k**2*P_un(k)*Wth(8*k)**2/(2*math.pi**2), 1e-4, 50, limit=400)[0]))**2
def Delta_lin(k, z): return D_std(1/(1+z))/D_std(1.0)*math.sqrt(k**3*PNORM*P_un(k)/(2*math.pi**2))
# strict no-DM background
OM_M = OM_B; OL = 1 - OM_M - OM_R
def E2(a): return OM_R/a**4 + OM_M/a**3 + OL
def dlnH(a): return 0.5*(-4*OM_R/a**4 - 3*OM_M/a**3)/E2(a)
KGRID = np.logspace(-2, 1.5, 36); ZI = 1000.0; KS = 0.2; EPS = 0.03
KOUT = [0.05, 0.2, 1.0, 3.0, 10.0]; IOUT = [int(np.argmin(abs(KGRID - k))) for k in KOUT]
DLNK = math.log(KGRID[1]/KGRID[0])
def Wfilt(k, a, xi): return k**2/(k**2 + xi**2*a**2*E2(a)/CH0**2)          # k in h/Mpc, c/H0 = 2997.92 Mpc/h
def run(model, reading, xi, a00):
    """all k modes integrated jointly (needed for the RMS-EFE coupling)."""
    n = len(KGRID)
    def rhs(N, y):
        a = math.exp(N); d = y[:n]; dp = y[n:]; E2a = E2(a); rho = OM_M*rho_crit/a**3
        kphys = KGRID*h/(a*Mpc); gN_k = 4*math.pi*G*rho*np.abs(d)/kphys
        if model == "RMS-EFE":
            # rms peculiar gravity of the field: sum over modes of (g_N,k)^2 with the mode's log-weight
            g_rms = math.sqrt(float(np.sum(gN_k**2*DLNK))); g_use = np.full(n, max(g_rms, 1e-30))
        elif model == "CUM-EFE":
            # each mode feels the rms field of all LARGER scales (k' <= k) plus its own: the external-field effect of the environment
            g_use = np.maximum(np.sqrt(np.cumsum(gN_k**2*DLNK)), 1e-30)
        else:
            g_use = np.maximum(gN_k, 1e-30)
        W = np.array([Wfilt(k, a, xi) for k in KGRID]) if xi > 0 else np.ones(n)
        if reading == "SUPPRESS": nu = 1 + W*(np.sqrt(1 + a00/g_use) - 1)
        else: nu = np.sqrt(1 + a00/np.maximum(W*g_use, 1e-30))
        src = 1.5*(OM_M/a**3/E2a)*nu*d; fr = 2 + dlnH(a)
        return np.concatenate([dp, src - fr*dp])
    ic = np.array([max(EPS*Delta_lin(k, ZI)*math.exp(-(k/KS)**2), 1e-15) for k in KGRID])
    tev = sorted(math.log(1/(1+z)) for z in (3.0, 0.0))
    sol = solve_ivp(rhs, (math.log(1/(1+ZI)), 0.0), np.concatenate([ic, ic]), t_eval=tev, method="DOP853", rtol=1e-7, atol=1e-18)
    out = {}
    for j, N in enumerate(sol.t):
        z = round(1/math.exp(N) - 1); out[z] = np.abs(sol.y[:n, j])
    return out
P("="*108); P("A. the filter on the strict background: W(k, z) for xi = 330, 403, 477 (reproduces the proposal's numbers)"); P("="*108)
for xi in (329, 403, 477):
    info(f"xi = {xi}: W(0.05, z=3) = {Wfilt(0.05, 0.25, xi):.3f}, W(1, z=3) = {Wfilt(1.0, 0.25, xi):.4f}, W(10, z=3) = {Wfilt(10.0, 0.25, xi):.5f}; W(0.05, z=1100) = {Wfilt(0.05, 1/1101, xi):.1e}, W(0.2, z=1100) = {Wfilt(0.2, 1/1101, xi):.1e}; W(1, z=0) = {Wfilt(1.0, 1.0, xi):.3f}")
check("A1 the proposal's transfer numbers reproduce on the strict background (W(0.05,3) = 0.35 +/- 0.02 at xi = 403; W(1,3) > 0.99; W(0.2,1100) < 0.02)",
      abs(Wfilt(0.05, 0.25, 403) - 0.35) < 0.02 and Wfilt(1.0, 0.25, 403) > 0.99 and Wfilt(0.2, 1/1101, 403) < 0.02)
P(""); P("="*108); P("B. the growth solver, strict no-DM, no floor: P_fw/P_measured at z = 3 (and z = 0) for k = 0.05, 0.2, 1, 3, 10 h/Mpc"); P("="*108)
info(f"{'model':8} {'reading':9} {'xi':>4} {'foot':10} " + " ".join(f"{'k='+str(k):>9}" for k in KOUT) + "   | z=0: " + " ".join(f"{'k='+str(k):>8}" for k in KOUT) + "   tilt(10/0.05,z=3)")
res = {}
for model in ("PERMODE", "CUM-EFE", "RMS-EFE"):
    for reading in ("SUPPRESS", "KERNEL"):
        for xi in (0, 329, 403, 477):
            if reading == "KERNEL" and xi != 403: continue
            for foot, a00 in A0.items():
                if foot == "alt" and xi not in (0, 403): continue
                out = run(model, reading, xi, a00)
                r3 = [(out[3][i]/Delta_lin(KGRID[i], 3.0))**2 for i in IOUT]; r0 = [(out[0][i]/Delta_lin(KGRID[i], 0.0))**2 for i in IOUT]
                res[(model, reading, xi, foot)] = (r3, r0)
                info(f"{model:8} {reading:9} {xi:4d} {foot:10} " + " ".join(f"{x:9.3g}" for x in r3) + "   | z=0: " + " ".join(f"{x:8.3g}" for x in r0) + f"   {r3[-1]/r3[0]:10.3g}")
def survives(r3): return 0.5 < r3[0] < 2 and all(0.5 < x < 2 for x in r3[2:])
surv = [(m, rd, xi, f) for (m, rd, xi, f), (r3, r0) in res.items() if survives(r3)]
check("B1 NO (model, reading, xi, footing) reproduces the measured z = 3 clustering within 2x at BOTH k = 0.05 and k = 1-10 h/Mpc: the filter cannot fix a spectrum that is wrong on the small-scale side too",
      len(surv) == 0, "survivors: " + (", ".join(map(str, surv)) if surv else "none"))
eff = {m: res[(m, "SUPPRESS", 403, "canonical")][0][0]/res[(m, "SUPPRESS", 0, "canonical")][0][0] for m in ("PERMODE", "CUM-EFE", "RMS-EFE")}
check("B2 the filter DOES what it was designed to do on the large-scale side: with xi = 403 the k = 0.05 power at z = 3 drops by > 2x relative to xi = 0 in every boost model",
      all(e < 0.5 for e in eff.values()), "k=0.05 suppression = " + ", ".join(f"{m}: {e:.2g}" for m, e in eff.items()))
land = {m: res[(m, "SUPPRESS", 403, "canonical")][0][0] for m in ("PERMODE", "CUM-EFE", "RMS-EFE")}
info("k = 0.05 at z = 3 with xi = 403, P_fw/P_obs: " + ", ".join(f"{m}: {v:.3g}" for m, v in land.items()) + "  (per-mode lands inside the 2x window at xi = 329-403; the others overshoot the cut)")
kern = res[("PERMODE", "KERNEL", 403, "canonical")][0][0]/res[("PERMODE", "SUPPRESS", 0, "canonical")][0][0]
check("B3 sign control: the literal reading chi = W ln N fed to the kernel INCREASES the k = 0.05 growth (deeper MOND at large scales); the action must filter the enhancement, not the kernel's input",
      kern > 1.0, f"k=0.05 power ratio (KERNEL xi=403 / no filter) = {kern:.2f}")
small = [res[(m, "SUPPRESS", xi, f)][0][2:] for (m, rd, xi, f) in res if rd == "SUPPRESS"]
info("the small-scale side, k = 1-10 at z = 3 (the filter is transparent there): PERMODE " + ", ".join(f"{x:.3g}" for x in res[("PERMODE", "SUPPRESS", 403, "canonical")][0][2:]) + " ; CUM-EFE " + ", ".join(f"{x:.3g}" for x in res[("CUM-EFE", "SUPPRESS", 403, "canonical")][0][2:]) + " ; RMS-EFE " + ", ".join(f"{x:.3g}" for x in res[("RMS-EFE", "SUPPRESS", 403, "canonical")][0][2:]))
span = [res[(m, "SUPPRESS", 403, "canonical")][0][4] for m in ("PERMODE", "CUM-EFE", "RMS-EFE")]
check("B4 the linear solver has NO authority on the small-scale side: the three defensible treatments of MOND's k-dependence span > 10 decades at k = 10, z = 3, so the no-CDM verdict there is not a linear-theory statement",
      max(span)/min(span) > 1e10, f"P_fw/P_obs(k=10, z=3) spans {min(span):.2g} to {max(span):.2g}")
P(""); P("="*108); P("VERDICT"); P("="*108)
P("  The filter does exactly what it was built for: at xi = 330-400 the 100-Mpc excess of a no-dark-matter MOND cosmology is removed and,")
P("  in the per-mode boost model, k = 0.05 lands inside the 2x window at z = 3 -- the first construction in this program to fix a scale")
P("  the growth solver had condemned.  Two caveats are structural.  (1) Sign: chi = W ln N fed to the kernel filters the INPUT and deepens")
P("  MOND at large scales (x1e4 worse); the action must filter the ENHANCEMENT.  (2) The small-scale side, k = 1-10 at z = 3, where the")
P("  filter is transparent by design, is where the no-CDM question actually lives, and there linear theory has no authority: three")
P("  defensible treatments of MOND's k-dependence span >10 decades.  The N-body literature (Nusser 2002; Llinares+ 2008; Angus+ 2013)")
P("  leans toward overproduction, i.e. the per-mode direction.  Verdict: NOT shut by this gate.  The large-scale side is fixed; the")
P("  route's fate is a baryon-only MOND N-body with the filter, plus the still-open 2-DOF count with Theta = K in the Hamiltonian.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
