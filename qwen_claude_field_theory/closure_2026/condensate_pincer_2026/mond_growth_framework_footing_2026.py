#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mond_growth_framework_footing_2026.py -- the pincer's yardsticks re-run on the FRAMEWORK's footing, not LCDM's.
==================================================================================================================
Objection (2026-09-02): the mu-pincer graded the dark fluid by NEWTONIAN linear growth (the dust carries the
structure).  On a "no dark matter" reading the dust is smooth and warm below ~10 Mpc and MOND grows the structure
from the baryons (stage 8 / route 1: the WANTED warm sector).  Nobody had computed that.  This script does, both ways:
  boost A  UNFLOORED MOND boost on the linear peculiar field (Nusser-2002 / Sanders-2001 class), the framework's own
           interpolation g = sqrt(g_N^2 + g_N a_0)  =>  nu = sqrt(1 + a_0/g_N), evaluated at the mode's rms peculiar
           gravity g_N = 4 pi G rho_m |delta_m| / k_phys, with the stage-17 a_0(z) law at the pinned nu_0.
  boost B  the framework's OWN DERIVED cosmological argument (prep_2026/mi_covariant_pt, 17/17):
           X = Z^2 (H/H_Lambda)^2 + (a_pec/a_0)^2 -- a dS-Unruh HUBBLE FLOOR under the kernel argument.
  sectors  (i) pinned Horn-1 warm dust (nu_0 = 8.8e-5, mu^-1 = 1 Mpc: the cluster paper's / "no DM" parameters) + baryons,
           with Newtonian pre-history z = 1000 -> 20 (a_0 is OFF there by the framework's own switch);
           (ii) NO dark field at all: Omega_m = Omega_b, MOND from z = 20 (crude no-DM baryon ICs, scanned x5).
Yardstick = the MEASURED clustering, which LCDM linear theory reproduces at k <= 0.2 (galaxies/BAO) and at k = 1-10 h/Mpc,
z = 2-4 (forest) to 10-20%: the framework must land within a factor 2 of it.  Both a_0 footings.  Checks CAN fail.
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
Zc = math.sqrt(32*math.pi/3); A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
NU0 = 8.8e-5                                                    # pinned Horn 1 at mu^-1 = 1 Mpc
R_PIN = NU0*(1 - OM_B - OM_DM - OM_R)/OM_DM
CS2_UNIT = 4*math.pi*G*OM_DM*rho_crit*Mpc**2/c**2
CH0 = 2997.92
def a0_of_z(z, a00): v = NU0*(1+z)**3; return a00*((1+NU0**2)/(1+v**2))**0.25
def cs2_dbi(a, nu0=NU0, R=R_PIN): v = nu0/a**3; sv = v/math.sqrt(1+v**2); return R*sv*(1-sv**2)/(1+R*sv)
class Cosmo:
    def __init__(self, om_b, om_dm):
        self.ob, self.od = om_b, om_dm; self.om = om_b + om_dm; self.ol = 1 - self.om - OM_R
        self.fb = om_b/self.om; self.fd = om_dm/self.om; self.HL = H0*math.sqrt(self.ol)
    def E2(self, a): return OM_R/a**4 + self.om/a**3 + self.ol
    def dlnH(self, a): return 0.5*(-4*OM_R/a**4 - 3*self.om/a**3)/self.E2(a)
    def D(self, a):
        return 2.5*self.om*math.sqrt(self.E2(a))*quad(lambda x: 1/(x*math.sqrt(self.E2(x)))**3, 1e-6, a)[0]
C_STD = Cosmo(OM_B, OM_DM); C_NODM = Cosmo(OM_B, 0.0)
# ---------------------------------------------------------------- the measured linear amplitude (BBKS shape, sigma8 = 0.811)
def T_bbks(k):
    Gam = C_STD.om*h*math.exp(-OM_B - math.sqrt(2*h)*OM_B/C_STD.om); q = k/Gam
    return math.log(1+2.34*q)/(2.34*q)*(1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25)
NS = 0.965
def P_unnorm(k): return k**NS*T_bbks(k)**2
def W(x): return 3*(math.sin(x) - x*math.cos(x))/x**3
s8_un = math.sqrt(quad(lambda k: k**2*P_unnorm(k)*W(8*k)**2/(2*math.pi**2), 1e-4, 50, limit=400)[0])
PNORM = (0.811/s8_un)**2
def Delta_lin(k, z, cosmo=C_STD):                                   # rms linear amplitude at (k, z), LCDM growth
    return cosmo.D(1/(1+z))/cosmo.D(1.0)*math.sqrt(k**3*PNORM*P_unnorm(k)/(2*math.pi**2))
# ---------------------------------------------------------------- growth with a MOND boost on the total peculiar field
def grow(k, cosmo, a_i, a_f, ic, cs2fun, boost, a00, z_out):
    """ic = (delta_b, delta_b', delta_d, delta_d') at a_i (absolute amplitudes); boost in {'none','A','B'}."""
    def rhs(N, y):
        a = math.exp(N); db, dbp, dd, ddp = y
        dm = cosmo.fb*db + cosmo.fd*dd
        E2 = cosmo.E2(a); rho_m = cosmo.om*rho_crit/a**3
        k_phys = k*h/(a*Mpc); gN = 4*math.pi*G*rho_m*abs(dm)/k_phys
        if boost == "none": nu = 1.0
        else:
            yv = gN/a0_of_z(1/a-1, a00)
            if boost == "B": yv = math.sqrt(Zc**2*E2*H0**2/cosmo.HL**2 + yv**2)   # the derived Hubble floor
            nu = math.sqrt(1 + 1/yv)
        src = 1.5*(cosmo.om/a**3/E2)*nu*dm; fr = 2 + cosmo.dlnH(a)
        pres = (k*CH0)**2*cs2fun(a)/(a**2*E2) if cosmo.fd > 0 else 0.0
        return [dbp, src - fr*dbp, ddp, src - fr*ddp - pres*dd]
    tev = sorted(math.log(1/(1+z)) for z in z_out)
    sol = solve_ivp(rhs, (math.log(a_i), math.log(a_f)), list(ic), t_eval=tev, method="DOP853", rtol=1e-8, atol=1e-14)
    out = {}
    for j, N in enumerate(sol.t):
        z = round(1/math.exp(N) - 1); out[z] = (sol.y[0][j], sol.y[2][j], cosmo.fb*sol.y[0][j] + cosmo.fd*sol.y[2][j])
    return out
KGRID = [0.05, 0.2, 1.0, 3.0, 10.0]
P("="*104); P("1. sector (i): pinned Horn-1 warm dust + baryons.  Newtonian pre-history z = 1000 -> 20, then boost A / B / none to z = 0"); P("="*104)
info(f"pinned R = {R_PIN:.2e}, c_s^2(0) = {cs2_dbi(1.0):.2e} c^2 (mu^-1 = {math.sqrt(cs2_dbi(1.0)/CS2_UNIT):.2f} Mpc), a_0(z=20)/a_0(0) = {a0_of_z(20, 1)/1:.3f}, a_0(z=3)/a_0(0) = {a0_of_z(3, 1):.4f}")
info(f"{'boost':8} {'footing':10} {'k':>5} {'z':>3} {'delta_rms fw':>13} {'delta_rms obs':>14} {'P_fw/P_obs':>11}  note")
res = {}
for boost in ("none", "A", "B"):
    for foot, a00 in (A0.items() if boost != "none" else [("--", A0["canonical"])]):
        for k in KGRID:
            amp20 = Delta_lin(k, 20.0)
            pre = grow(k, C_STD, 1e-3, 1/21.0, (1.0, 1.0, 1.0, 1.0), cs2_dbi, "none", a00, (20.0,))[20]
            cold = grow(k, C_STD, 1e-3, 1/21.0, (1.0, 1.0, 1.0, 1.0), lambda a: 0.0, "none", a00, (20.0,))[20]
            # absolute ICs at z = 20: the measured amplitude times the warm-dust pre-history factor, growing-mode slope
            ic = (amp20*pre[0]/cold[2], amp20*pre[0]/cold[2], amp20*pre[1]/cold[2], amp20*pre[1]/cold[2])
            late = grow(k, C_STD, 1/21.0, 1.0, ic, cs2_dbi, boost, a00, (3.0, 0.0))
            for z in (3, 0):
                obs = Delta_lin(k, float(z)); fw = abs(late[z][2]); r = (fw/obs)**2
                res[(boost, foot, k, z)] = r
                note = "NONLINEAR (delta > 1): linear value is a lower bound on the overproduction" if fw > 1 else ""
                info(f"{boost:8} {foot:10} {k:5.2f} {z:3d} {fw:13.3e} {obs:14.3e} {r:11.3g}  {note}")
rB = [res[("B", f, k, z)]/res[("none", "--", k, z)] for f in A0 for k in KGRID for z in (3, 0)]
check("1a the framework's OWN derived Hubble floor (boost B) makes MOND irrelevant to linear growth: every P(k) within 10% of the Newtonian run, both footings",
      max(abs(x-1) for x in rB) < 0.10, f"max |P_B/P_Newton - 1| = {max(abs(x-1) for x in rB):.3f}")
rA_small = [res[("A", f, k, 3)] for f in A0 for k in (1.0, 3.0, 10.0)]
rA_large = [res[("A", f, k, 3)] for f in A0 for k in (0.05, 0.2)]
check("1b (a WORKS, against my expectation) UNFLOORED boost A: the pinned warm dust + MOND-grown baryons land within 2x of the measured z = 3 power at k = 1-10 h/Mpc, both footings (the Newtonian run is 300-600x low there)",
      all(0.4 < x < 2.5 for x in rA_small), "P_fw/P_obs(z=3, k=1,3,10) = " + ", ".join(f"{x:.2f}" for x in rA_small))
check("1b' ...but overproduces the LARGE-scale power (k <= 0.2, z = 3) by > 4x, both footings: the dust clusters there and is boosted x6; 100-Mpc scales go nonlinear by z = 0",
      min(rA_large) > 4.0, "P_fw/P_obs(z=3, k=0.05,0.2) = " + ", ".join(f"{x:.1f}" for x in rA_large))
rN = [res[("none", "--", k, z)] for k in (0.2, 1.0, 3.0, 10.0) for z in (3, 0)]
check("1c and the Newtonian run (= the pincer's Horn 1 = the framework's derived footing) underproduces by > 2x at k >= 0.2", max(rN) < 0.5, f"max P_fw/P_obs at k>=0.2 = {max(rN):.3g}")
P(""); P("="*104); P("1d. the one knob: scan mu^-1 (pinned nu_0 = 8.8e-5 x mu^-1/Mpc) under the UNFLOORED boost A -- can any value get the z = 3 SHAPE right?"); P("="*104)
info(f"{'mu^-1':>8} {'nu_0':>9} " + " ".join(f"{'P/Pobs k='+str(k):>14}" for k in KGRID) + "   shape(10/0.05)   note")
scan = {}
for mu_mpc in (0.1, 0.24, 0.5, 1.0, 2.0, 5.0):
    nu0 = 8.8e-5*mu_mpc; Rr = nu0*(1 - OM_B - OM_DM - OM_R)/OM_DM
    csf = lambda a, n_=nu0, R_=Rr: cs2_dbi(a, n_, R_)
    row = []
    for k in KGRID:
        amp20 = Delta_lin(k, 20.0)
        pre = grow(k, C_STD, 1e-3, 1/21.0, (1.0, 1.0, 1.0, 1.0), csf, "none", A0["canonical"], (20.0,))[20]
        cold = grow(k, C_STD, 1e-3, 1/21.0, (1.0, 1.0, 1.0, 1.0), lambda a: 0.0, "none", A0["canonical"], (20.0,))[20]
        ic = (amp20*pre[0]/cold[2], amp20*pre[0]/cold[2], amp20*pre[1]/cold[2], amp20*pre[1]/cold[2])
        late = grow(k, C_STD, 1/21.0, 1.0, ic, csf, "A", A0["canonical"], (3.0, 0.0))
        row.append((abs(late[3][2])/Delta_lin(k, 3.0))**2)
    scan[mu_mpc] = row; shape = row[-1]/row[0]
    inwin = "in window" if 2.14e-5 <= nu0 <= 1.77e-4 else "outside window"
    info(f"{mu_mpc:6.2f} Mpc {nu0:9.2e} " + " ".join(f"{x:14.3g}" for x in row) + f"   {shape:12.3g}   {inwin}")
best = min(scan, key=lambda m: max(abs(math.log(x)) for x in scan[m]))
worst_dev = max(abs(math.log(x)) for x in scan[best])
check("1d no mu^-1 in 0.1-5 Mpc brings the unfloored z = 3 power within 2x of the measured shape at ALL of k = 0.05-10 h/Mpc: the large-scale overproduction is mu-independent",
      worst_dev > math.log(2.0), f"best mu^-1 = {best} Mpc, worst |ln(P/P_obs)| = {worst_dev:.2f} (2x = 0.69)")
P(""); P("="*104); P("2. sector (ii): NO dark field.  Omega_m = Omega_b, MOND from z = 20 on baryon ICs of eps x the measured amplitude (crude, scanned)"); P("="*104)
info("no-DM baryon ICs after recombination are ~1e-5 x growth(1100->20) ~ 5e-4 at k ~ 0.05 vs 2.5e-2 measured => eps ~ 0.02; scanned eps = 0.02, 0.1")
res2 = {}
for eps in (0.02, 0.1):
    for boost in ("A", "B"):
        for foot, a00 in A0.items():
            for k in KGRID:
                amp20 = eps*Delta_lin(k, 20.0)
                late = grow(k, C_NODM, 1/21.0, 1.0, (amp20, amp20, 0.0, 0.0), lambda a: 0.0, boost, a00, (3.0, 0.0))
                for z in (3, 0):
                    fw = abs(late[z][2]); obs = Delta_lin(k, float(z)); res2[(eps, boost, foot, k, z)] = (fw/obs)**2
            info(f"eps={eps:<5} boost {boost} {foot:10}: P_fw/P_obs at z=3 [k=0.05,0.2,1,3,10] = " + ", ".join(f"{res2[(eps, boost, foot, k, 3)]:.3g}" for k in KGRID)
                 + " | z=0: " + ", ".join(f"{res2[(eps, boost, foot, k, 0)]:.3g}" for k in KGRID))
okB = all(res2[(e, "B", f, k, z)] < 0.5 for e in (0.02, 0.1) for f in A0 for k in KGRID for z in (3, 0))
check("2a no dark field + the framework's derived floor (B): underproduces the measured clustering by > 2x at every k, z, eps (the classic no-DM failure)", okB)
tiltA = [res2[(e, "A", f, 10.0, 3)]/res2[(e, "A", f, 0.05, 3)] for e in (0.02, 0.1) for f in A0]
check("2b no dark field + unfloored boost (A): the z = 3 spectrum is TILTED relative to the measured shape by > 30x in power between k = 0.05 and 10 h/Mpc, for every IC normalisation and both footings (shape, not amplitude, kills it)",
      min(tiltA) > 30.0, f"P(10)/P(0.05) relative to measured = {min(tiltA):.0f}-{max(tiltA):.0f}")
P(""); P("="*104); P("VERDICT"); P("="*104)
P("  On the framework's OWN derived cosmological footing (the dS-Unruh Hubble floor under the kernel argument, mi_covariant_pt 17/17),")
P("  MOND does nothing to linear growth (6%): the pincer's Newtonian yardsticks ARE the framework's footing, and Horn 1 underproduces")
P("  by 40-600x at k >= 0.2.  Dropping the floor (a Nusser/Sanders MOND cosmology, which the framework's own 17/17 derivation rejects)")
P("  reproduces the z = 3 SMALL-scale power to within 2x -- a genuine works -- but overproduces the >= 100 Mpc power 5-13x at z = 3 and")
P("  makes 100-Mpc scales nonlinear by z = 0, for every mu.  A universe with no dark field at all is tilted 30-200x in shape either way.")
P("  Nothing in the framework boosts k >~ 1 h/Mpc without also boosting k ~ 0.05.  Structure needs an Omega_dm-worth of something that")
P("  clusters on 100-Mpc scales without a MOND boost, and the pincer says that something is cold on every scale above ~1 kpc.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
