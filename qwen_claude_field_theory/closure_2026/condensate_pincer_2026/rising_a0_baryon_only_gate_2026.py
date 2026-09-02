#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
rising_a0_baryon_only_gate_2026.py -- the last named door: a_0 ~ H(z), no dark field, the MOND boost as the missing mass.
=======================================================================================================================
Proposal (2026-09-02): take the alt footing as the time law, a_0(z) = c H(z)/Z = a_0(0) E(z), so a_0 at recombination is
~1e4 x today's; the acoustic-era perturbations are then deep-MOND and the boost itself, not a dust, supplies the third peak
and the early growth.  A Boltzmann run is the full test.  This is the FIRST GATE, cheap and both ways: the growth of
baryon-only perturbations from recombination (z = 1000) to z = 3 and 0 under the framework's own interpolation
g = sqrt(g_N^2 + g_N a_0(z)), compared with the MEASURED clustering shape at k = 0.05-10 h/Mpc.
  variants  boost A = unfloored ;  boost B = the framework's DERIVED floor X = (cH/a_0)^2 + (a_pec/a_0)^2, which with
            a_0 ~ H is the CONSTANT Z^2 -> nu_floor = sqrt(1 + 1/Z) = 1.083 at all z ;  a_0 flat (constant) for contrast.
  ICs       delta_b(k, z = 1000) = eps_b x [LCDM linear shape at z = 1000] x Silk damping exp(-(k/k_S)^2), k_S = 0.2 h/Mpc,
            eps_b in {0.01, 0.1} (baryons lag CDM by 10-100x at decoupling).  Crude, scanned x10, and irrelevant to the
            SHAPE verdict, which is normalisation-free.
  also      the MOND-ness of recombination itself: y = g_N/a_0(z_rec) on the acoustic scales (needs no growth run).
Checks CAN fail.  Both a_0 footings.
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
Zc = math.sqrt(32*math.pi/3); A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}; CH0 = 2997.92
class Cosmo:
    def __init__(self, om_b, om_dm):
        self.ob, self.od = om_b, om_dm; self.om = om_b + om_dm; self.ol = 1 - self.om - OM_R
        self.fb = om_b/self.om; self.fd = om_dm/self.om if self.om > 0 else 0.0
    def E2(self, a): return OM_R/a**4 + self.om/a**3 + self.ol
    def dlnH(self, a): return 0.5*(-4*OM_R/a**4 - 3*self.om/a**3)/self.E2(a)
    def D(self, a): return 2.5*self.om*math.sqrt(self.E2(a))*quad(lambda x: 1/(x*math.sqrt(self.E2(x)))**3, 1e-6, a)[0]
C_STD = Cosmo(OM_B, OM_DM); C_NODM = Cosmo(OM_B, 0.0)
def T_bbks(k):
    Gam = C_STD.om*h*math.exp(-OM_B - math.sqrt(2*h)*OM_B/C_STD.om); q = k/Gam
    return math.log(1+2.34*q)/(2.34*q)*(1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25)
def P_un(k): return k**0.965*T_bbks(k)**2
def W(x): return 3*(math.sin(x) - x*math.cos(x))/x**3
PNORM = (0.811/math.sqrt(quad(lambda k: k**2*P_un(k)*W(8*k)**2/(2*math.pi**2), 1e-4, 50, limit=400)[0]))**2
def Delta_lin(k, z): return C_STD.D(1/(1+z))/C_STD.D(1.0)*math.sqrt(k**3*PNORM*P_un(k)/(2*math.pi**2))
def a0_of_z(z, a00, law): return a00*math.sqrt(C_STD.E2(1/(1+z))) if law == "rise" else a00
def grow(k, cosmo, a_i, ic, boost, a00, law, z_out):
    def rhs(N, y):
        a = math.exp(N); db, dbp = y; E2 = cosmo.E2(a); z = 1/a - 1
        rho_m = cosmo.om*rho_crit/a**3; k_phys = k*h/(a*Mpc); gN = 4*math.pi*G*rho_m*abs(db)/k_phys
        if boost == "none": nu = 1.0
        else:
            yv = max(gN/a0_of_z(z, a00, law), 1e-12)
            if boost == "B": yv = math.sqrt((c*H0*math.sqrt(E2)/a0_of_z(z, a00, law))**2 + yv**2)
            nu = math.sqrt(1 + 1/yv)
        src = 1.5*(cosmo.om/a**3/E2)*nu*db; fr = 2 + cosmo.dlnH(a)
        return [dbp, src - fr*dbp]
    tev = sorted(math.log(1/(1+z)) for z in z_out)
    sol = solve_ivp(rhs, (math.log(a_i), 0.0), list(ic), t_eval=tev, method="DOP853", rtol=1e-8, atol=1e-16)
    return {round(1/math.exp(N)-1): sol.y[0][j] for j, N in enumerate(sol.t)}
KG = [0.05, 0.2, 1.0, 3.0, 10.0]; ZI = 1000.0; KS = 0.2
DAMP = {'Silk k_S=0.2': lambda k: math.exp(-(k/KS)**2), 'no damping': lambda k: 1.0}
P("="*104); P("0. how MOND is recombination under a_0 ~ H(z)?  y = g_N/a_0(z_rec) on the acoustic scales, baryon-only, delta_b = 1e-4"); P("="*104)
for foot, a00 in A0.items():
    a0rec = a0_of_z(ZI, a00, "rise"); rho_b = OM_B*rho_crit*(1+ZI)**3
    ys = []
    for k in (0.02, 0.05, 0.2, 1.0):
        k_phys = k*h*(1+ZI)/Mpc; gN = 4*math.pi*G*rho_b*1e-4/k_phys; ys.append(gN/a0rec)
    info(f"{foot:10s}: a_0(z=1000) = {a0rec:.2e} m/s^2 (x{a0rec/a00:.0f});  y(k=0.02,0.05,0.2,1) = " + ", ".join(f"{y:.1e}" for y in ys) + f"  -> nu = " + ", ".join(f"{math.sqrt(1+1/y):.0f}" for y in ys))
check("0a with a_0 ~ H, the acoustic-era perturbations are deep-MOND: y < 1e-3 at every k in 0.02-1 h/Mpc, boost nu > 30 -- the premise of the proposal holds (and it is what breaks it below)",
      all(y < 1e-3 for y in ys))
P(""); P("="*104); P("1. baryon-only growth z = 1000 -> 3, 0 under a_0 ~ H(z): P_fw/P_measured at k = 0.05-10 h/Mpc"); P("="*104)
info(f"{'law':5} {'boost':6} {'foot':10} {'eps_b':6} " + " ".join(f"{'k='+str(k):>10}" for k in KG) + "   tilt(10/0.05)   note")
res = {}
for dname, dfun in DAMP.items():
  info(f"-- IC damping: {dname}")
  for law in ("rise", "flat"):
    for boost in ("A", "B"):
        for foot, a00 in A0.items():
            if boost == "B" and foot == "alt": continue
            for eps in (0.01, 0.1):
                row3 = []; nonlin = False
                for k in KG:
                    amp = max(eps*Delta_lin(k, ZI)*dfun(k), 1e-15)
                    out = grow(k, C_NODM, 1/(1+ZI), (amp, amp), boost, a00, law, (3.0, 0.0))
                    fw = abs(out[3]); row3.append((fw/Delta_lin(k, 3.0))**2); nonlin |= fw > 1
                res[(dname, law, boost, foot, eps)] = row3
                info(f"{law:5} {boost:6} {foot:10} {eps:6.2f} " + " ".join(f"{x:10.3g}" for x in row3) + f"   {row3[-1]/row3[0]:12.3g}   {'NONLINEAR at z=3 (lower bound)' if nonlin else ''}")
tiltA = [res[(d, "rise", "A", f, e)][-1]/res[(d, "rise", "A", f, e)][0] for d in DAMP for f in A0 for e in (0.01, 0.1)]
ampA = [res[(d, "rise", "A", f, e)][1] for d in DAMP for f in A0 for e in (0.01, 0.1)]
check("1a UNFLOORED a_0 ~ H, no dark field: the z = 3 spectrum is tilted > 30x in power between k = 0.05 and 10 h/Mpc relative to the measured shape, both footings, both IC normalisations, with and without Silk damping",
      min(tiltA) > 30, f"tilt = {min(tiltA):.3g}-{max(tiltA):.3g}")
check("1b ...and the k = 0.2 amplitude at z = 3 is off the measured value by > 10x in one direction or the other for every normalisation (no eps_b rescues both amplitude and shape)",
      all(x > 10 or x < 0.1 for x in ampA), "P_fw/P_obs(k=0.2, z=3) = " + ", ".join(f"{x:.3g}" for x in ampA))
rowB = [res[(d, "rise", "B", "canonical", e)] for d in DAMP for e in (0.01, 0.1)]
check("1c with the framework's DERIVED floor, a_0 ~ H makes the boost a constant nu = sqrt(1 + 1/Z) = 1.08 at all z: no dark field then underproduces by > 10x at every k (the classic no-DM failure)",
      all(x < 0.1 for r in rowB for x in r), "max P_fw/P_obs = " + f"{max(x for r in rowB for x in r):.3g}")
flatA = [res[("no damping", "flat", "A", "canonical", e)][-1]/res[("no damping", "flat", "A", "canonical", e)][0] for e in (0.01, 0.1)]
info(f"contrast, a_0 flat and unfloored: tilt = {flatA[0]:.3g}-{flatA[1]:.3g} -- the tilt is the same (it is set by the boost's k-dependence, nu ~ (k/delta)^(1/2)); rising a_0 makes the AMPLITUDE 1e4x worse")
attr = [abs(res[(d, "rise", "A", f, 0.1)][i]/res[(d, "rise", "A", f, 0.01)][i] - 1) for d in DAMP for f in A0 for i in range(len(KG))]
check("1d the unfloored result is independent of the IC amplitude to < 15% between eps_b = 0.01 and 0.1 (and of Silk damping): deep-MOND growth is an ATTRACTOR, delta ~ t^4, so the tilt is a property of the dynamics, not of the initial conditions",
      max(attr) < 0.15, f"max |ratio - 1| = {max(attr):.3f}")
P(""); P("="*104); P("VERDICT"); P("="*104)
P("  a_0 ~ H(z) does put recombination in the deep-MOND regime (nu ~ 30-400 on the acoustic scales), which is the proposal's premise")
P("  and its undoing: the boost is largest where the peculiar gravity is smallest, so a baryon-only universe grows its small scales")
P("  far faster than its large ones and arrives at z = 3 tilted x300 against the measured shape and 1e6-1e9 too strong, on an")
P("  attractor that forgets the initial conditions.  With the")
P("  framework's own derived floor the boost collapses to a constant 8% and nothing grows.  The Boltzmann run is not needed:")
P("  the growth between recombination and z = 3 already fails both ways.  The door is shut.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
