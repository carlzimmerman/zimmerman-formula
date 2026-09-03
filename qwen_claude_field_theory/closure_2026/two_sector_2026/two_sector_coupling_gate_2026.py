#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
two_sector_coupling_gate_2026.py -- THE LAST DOOR: a dark charge in a second metric.  Exact linear kernels, then the anchors.
=============================================================================================================================
The dark-sector debug left one structure standing: a dark component that sources the visible potential on cosmological scales
(CMB, growth) but is screened around galaxies (KiDS: <= 6-14% of a CDM-like halo) and partly present in clusters (X-COP: 32-46%).
Ghost-free Hassan-Rosen bigravity with each matter sector minimally coupled to its own metric (visible -> g, dark -> f) is the
minimal realisation (the Boulware-Deser ghost returns only for DOUBLY coupled species).  This script:
  A. derives the linear two-sector Newtonian and lensing kernels from the mode decomposition (sympy): with beta = M_f^2/M_g^2,
     G_u = 1/(8 pi (M_g^2 + M_f^2)),  m the massive-mode mass, a g-observer sees
        g-source:  Phi = -G_u M/r [1 + (4/3) beta e^{-mr}]     lensing [1 + beta e^{-mr}]
        f-source:  Phi = -G_u M/r [1 - (4/3) e^{-mr}]          lensing [1 - e^{-mr}]
     i.e. the dark sector is INVISIBLE to light and REPULSIVE (-1/3) to dynamics inside 1/m, and fully attractive beyond it --
     exactly the scale structure the debug asked for.  (Vainshtein screening only changes 4/3 -> 1 inside r_V.)
  B. the two galaxy-scale anchors PIN 1/m: KiDS (coupling <= 0.14 at 250 kpc) and X-COP (0.32-0.46 at R500 ~ 1 Mpc) -- a WORKS.
  C. the cosmological anchor in PHYSICAL units: the CMB acoustic scales at recombination (third peak, damping tail) are 40-130 kpc
     PHYSICAL -- the same physical scales as the KiDS rail today -- and there the coupling must be ~1.  A fixed physical 1/m cannot
     be both.  (Interleaving, in physical scale.)
  D. the comoving alternative (a cutoff that scales with a): the two-fluid growth integrator with the dark-to-baryon coupling
     W(k) = m_c^2/(k^2 + m_c^2) at the KiDS-pinned comoving 1/m_c >= 1.7 Mpc: baryon P(k) at z = 3 (the forest) and z = 0 vs LCDM.
No a_0 enters (the dark sector is a_0-blind); the MOND side is the baseline both footings share.  Checks CAN fail.  Mutation: W = 1.
"""
import sys, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
P("="*118); P("A. linear two-sector kernels from the mode decomposition (sympy)"); P("="*118)
Mg2, Mf2, m, r, M = sp.symbols("M_g2 M_f2 m r M", positive=True)
beta = Mf2/Mg2
# quadratic action: (Mg2/2) hg E hg + (Mf2/2) hf E hf - (m^2 Meff2/8) FP(hg - hf) + (hg Tg + hf Tf)/2,   Meff2 = Mg2 Mf2/(Mg2 + Mf2)
# modes: u = (Mg2 hg + Mf2 hf)/(Mg2 + Mf2) (massless, Planck^2 = Mg2 + Mf2),  v = hg - hf (Fierz-Pauli, Planck^2 = Meff2, mass m)
# hg = u + [Mf2/(Mg2+Mf2)] v,  hf = u - [Mg2/(Mg2+Mf2)] v  (cross kinetic terms cancel: verified below)
Msum = Mg2 + Mf2; Meff2 = Mg2*Mf2/Msum
cg_u, cg_v = 1, Mf2/Msum          # projections of a g-observer's metric onto (u, v)
cf_u, cf_v = 1, -Mg2/Msum         # of an f-observer's metric
# static Green's functions with the ½ h T coupling:  massless: Phi = -M/(8 pi Planck^2 r) [dyn], same for lensing
#                                                     Fierz-Pauli: Phi = -(4/3) M e^{-mr}/(8 pi Planck^2 r) [dyn],  lensing coefficient 1
Gu = 1/(8*sp.pi*Msum); Gv = 1/(8*sp.pi*Meff2)
def kernel(c_obs_u, c_obs_v, c_src_u, c_src_v, dyn=True):
    fac = sp.Rational(4, 3) if dyn else 1
    return sp.simplify((c_obs_u*c_src_u*Gu + c_obs_v*c_src_v*Gv*fac*sp.exp(-m*r))/Gu)   # in units of -G_u M/r
# cross-kinetic cancellation
hg = sp.Symbol("u") + cg_v*sp.Symbol("v"); hf = sp.Symbol("u") + cf_v*sp.Symbol("v")
cross = sp.simplify(sp.expand(Mg2*hg**2 + Mf2*hf**2).coeff(sp.Symbol("u")*sp.Symbol("v")))
check("A0 the mode decomposition diagonalises the kinetic term (u-v cross term vanishes identically)", cross == 0)
K_gg = kernel(cg_u, cg_v, cg_u, cg_v); K_gf = kernel(cg_u, cg_v, cf_u, cf_v); K_ff = kernel(cf_u, cf_v, cf_u, cf_v)
L_gg = kernel(cg_u, cg_v, cg_u, cg_v, dyn=False); L_gf = kernel(cg_u, cg_v, cf_u, cf_v, dyn=False)
info(f"g-observer, g-source  (dyn):  {K_gg}      lensing: {L_gg}")
info(f"g-observer, f-source  (dyn):  {K_gf}      lensing: {L_gf}")
info(f"f-observer, f-source  (dyn):  {K_ff}")
check("A1 g<-g: 1 + (4/3) beta e^{-mr} (dynamics), 1 + beta e^{-mr} (lensing)", sp.simplify(K_gg - (1 + sp.Rational(4, 3)*beta*sp.exp(-m*r))) == 0 and sp.simplify(L_gg - (1 + beta*sp.exp(-m*r))) == 0)
check("A2 g<-f: 1 - (4/3) e^{-mr} (dynamics: repulsive -1/3 inside 1/m), 1 - e^{-mr} (lensing: invisible inside 1/m), independent of beta", sp.simplify(K_gf - (1 - sp.Rational(4, 3)*sp.exp(-m*r))) == 0 and sp.simplify(L_gf - (1 - sp.exp(-m*r))) == 0)
check("A3 f<-f: 1 + (4/3) e^{-mr}/beta -- the dark sector's own short-range gravity is enhanced by 4/(3 beta)", sp.simplify(K_ff - (1 + sp.Rational(4, 3)*sp.exp(-m*r)/beta)) == 0)
info("A4 cosmological coupling: beyond 1/m only the massless mode acts, with G_u = G_N/(1+beta) for EVERY pair; BBN/CMB hold G_cosmo/G_N to ~5% => beta <= 0.05 => the dark sector's own short-range gravity is >= 27 G_N (A3).  Vainshtein screening of the helicity-0 (r < r_V) turns 4/3 -> 1: invisible rather than repulsive.")
P(""); P("="*118); P("B. the two galaxy-scale anchors pin 1/m (a WORKS)"); P("="*118)
kpc = 1.0; Mpc = 1000.0
def Lcoup(rr, inv_m): return 1 - math.exp(-rr/inv_m)
# KiDS: dark_sector_debug D1 -- <= 0.14 of a CDM-like halo at the rail (39-228 kpc; use 250 kpc): coupling(250 kpc) <= 0.14
inv_m_kids = 250*kpc/(-math.log(1 - 0.14))
# X-COP: dark_sector_debug D2 -- 0.32-0.46 of a CDM halo at R500 ~ 1 Mpc
inv_m_cl = (1*Mpc/(-math.log(1 - 0.46)), 1*Mpc/(-math.log(1 - 0.32)))
info(f"KiDS rail: L(250 kpc) <= 0.14  =>  1/m >= {inv_m_kids/Mpc:.2f} Mpc;   X-COP: L(1 Mpc) = 0.32-0.46  =>  1/m = {inv_m_cl[0]/Mpc:.2f}-{inv_m_cl[1]/Mpc:.2f} Mpc")
check("B1 (a WORKS) the KiDS galaxy bound and the X-COP cluster need are CONSISTENT for one massive-mode range: 1/m = 1.7-2.6 Mpc satisfies both", inv_m_kids <= inv_m_cl[1], f"window 1/m in [{max(inv_m_kids, inv_m_cl[0])/Mpc:.2f}, {inv_m_cl[1]/Mpc:.2f}] Mpc")
INV_M = max(inv_m_kids, inv_m_cl[0])
for rr in (40, 100, 250, 500, 1000, 2000):
    info(f"   at 1/m = {INV_M/Mpc:.2f} Mpc: r = {rr:5d} kpc  lensing coupling {Lcoup(rr, INV_M):.2f}   dynamics (linear) {1 - 4/3*math.exp(-rr/INV_M):+.2f}   (Vainshtein-screened: {Lcoup(rr, INV_M):.2f})")
P(""); P("="*118); P("C. the cosmological anchor in PHYSICAL units: the CMB was made at galaxy scales"); P("="*118)
z_rec = 1090.0; chi_star = 13900.0                      # Mpc comoving to last scattering
scales = {"sound horizon r_s": 144.6, "1st peak l=220": 2*math.pi*chi_star/220, "3rd peak l=800": 2*math.pi*chi_star/800, "damping tail l=2000": 2*math.pi*chi_star/2000, "damping tail l=3000": 2*math.pi*chi_star/3000}
info(f"{'CMB feature':22} {'comoving Mpc':>12} {'PHYSICAL at z=1090 (kpc)':>26}   coupling there at 1/m = {INV_M/Mpc:.2f} Mpc (physical, fixed)")
phys = {}
for k_, v in scales.items():
    ph = v/(1+z_rec)*1000; phys[k_] = ph; info(f"{k_:22} {v:12.1f} {ph:26.0f}   {Lcoup(ph, INV_M):.3f}")
info(f"KiDS rail today: 39-228 kpc physical, coupling required <= 0.14;  CMB third peak + damping tail: {phys['damping tail l=3000']:.0f}-{phys['3rd peak l=800']:.0f} kpc physical, coupling required ~ 1 (the dark sector is what makes H3/H1)")
overlap = (phys["damping tail l=3000"] < 228) and (phys["3rd peak l=800"] > 39)
check("C1 THE PHYSICAL-SCALE INTERLEAVING: the CMB's third peak and damping tail were made at 30-100 kpc PHYSICAL, inside the KiDS rail's 39-228 kpc, with opposite coupling requirements -- no fixed physical transition scale can serve both",
      overlap and Lcoup(phys["3rd peak l=800"], INV_M) < 0.1, f"coupling at the 3rd peak's physical scale with the KiDS-pinned 1/m = {Lcoup(phys['3rd peak l=800'], INV_M):.3f} (needs ~1)")
P(""); P("="*118); P("D. the comoving alternative: cutoff scaling with a.  Two-fluid growth, baryons feel the dark sector through W(k) = m_c^2/(k^2+m_c^2)"); P("="*118)
h = 0.674; OM_B = 0.02237/h**2; OM_DM = 0.1200/h**2; OM_R = 4.15e-5/h**2; OM_M = OM_B + OM_DM; OM_L = 1 - OM_M - OM_R
fb, fd = OM_B/OM_M, OM_DM/OM_M; CH0 = 2997.92
def E2(a): return OM_R/a**4 + OM_M/a**3 + OM_L
def dlnH(a): return 0.5*(-4*OM_R/a**4 - 3*OM_M/a**3)/E2(a)
def grow(k_hmpc, W, a_i=1e-3, z_out=(3.0, 0.0)):
    def rhs(N, y):
        a = math.exp(N); db, dbp, dd, ddp = y; pref = 1.5*(OM_M/a**3/E2(a)); fr = 2 + dlnH(a)
        return [dbp, pref*(fb*db + W*fd*dd) - fr*dbp, ddp, pref*(W*fb*db + fd*dd) - fr*ddp]
    tev = sorted(math.log(1/(1+z)) for z in z_out)
    sol = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0, 1.0, 1.0], t_eval=tev, method="DOP853", rtol=1e-8, atol=1e-14)
    return {round(1/math.exp(N)-1): (sol.y[0][j], sol.y[2][j]) for j, N in enumerate(sol.t)}
KGRID = [0.2, 1.0, 3.0, 10.0]
ref = {(k, z): grow(k, 1.0)[z] for k in KGRID for z in (3, 0)}
check("M0 mutation control: W = 1 gives identical baryon and dark growth (the LCDM two-fluid limit)", all(abs(ref[(k, z)][0]/ref[(k, z)][1] - 1) < 1e-6 for k in KGRID for z in (3, 0)))
info(f"{'1/m_c [Mpc com.]':>16} " + " ".join(f"{'Pb/PLCDM k='+str(k)+' z=3':>18}" for k in KGRID) + " |" + " ".join(f"{'z=0 k='+str(k):>12}" for k in KGRID))
resD = {}
for inv_mc in (0.25, 0.5, 1.0, INV_M/Mpc, 2.6, 4.0):
    mc = 1.0/inv_mc                                              # Mpc^-1 comoving
    row = {}
    for k in KGRID:
        kM = k*h; W = mc**2/(kM**2 + mc**2); g = grow(k, W)
        for z in (3, 0): row[(k, z)] = (g[z][0]/ref[(k, z)][0])**2
    resD[inv_mc] = row
    info(f"{inv_mc:16.2f} " + " ".join(f"{row[(k,3)]:18.3f}" for k in KGRID) + " |" + " ".join(f"{row[(k,0)]:12.3f}" for k in KGRID))
pin = resD[INV_M/Mpc]
check("D1 at the KiDS-pinned comoving cutoff (1/m_c >= 1.7 Mpc) the BARYON power the z = 3 forest measures is suppressed by more than 20% at k = 1-3 h/Mpc and by more than 50% at k = 10 h/Mpc, against a forest that agrees with LCDM to ~10%: the comoving version is excluded by the forest",
      pin[(1.0, 3)] < 0.8 and pin[(3.0, 3)] < 0.8 and pin[(10.0, 3)] < 0.5, f"P_b/P_LCDM(z=3) at k = 1, 3, 10 = {pin[(1.0,3)]:.2f}, {pin[(3.0,3)]:.2f}, {pin[(10.0,3)]:.2f}")
check("D2 ...and it also cuts the z = 0 galaxy power at k = 0.2-1 h/Mpc (BOSS/DESI, few-percent data): suppression > 5% at k = 1", pin[(1.0, 0)] < 0.95, f"P_b/P_LCDM(z=0, k=1) = {pin[(1.0,0)]:.3f}, k=0.2: {pin[(0.2,0)]:.3f}")
small = resD[0.25]
info(f"both ways: a comoving cutoff short enough for the forest (1/m_c = 0.25 Mpc: P_b/P at z=3, k=1..10 = {small[(1.0,3)]:.2f}, {small[(3.0,3)]:.2f}, {small[(10.0,3)]:.2f}) gives coupling {Lcoup(250, 250):.2f} at 250 kpc today -- the KiDS bound (<= 0.14) fails by x{Lcoup(250, 250)/0.14:.0f}")
P(""); P("="*118); P("VERDICT"); P("="*118)
P("  The two-sector door has exactly the right SHAPE: in ghost-free bigravity a dark sector on the second metric is invisible to light")
P("  and repulsive to dynamics inside 1/m and fully attractive beyond it, and the two galaxy-scale anchors you already own agree on the")
P("  range, 1/m = 1.7-2.6 Mpc (KiDS and X-COP, independently).  It fails on the third anchor, and the failure is a theorem about scales,")
P("  not about ghosts: the CMB's third peak and damping tail were made at 30-100 kpc PHYSICAL, the same physical scales as the KiDS rail")
P("  today, and there the dark sector must gravitate fully.  A fixed physical range cannot serve both; a comoving range that serves the")
P("  CMB cuts the baryon power the z = 3 forest measures by 30-90% at k = 1-10 h/Mpc.  So the dark-to-visible coupling cannot be a")
P("  function of scale, physical or comoving -- the same conclusion the environment debug reached for local variables.  What is left")
P("  is a switch on COLLAPSE itself (single-stream vs multi-stream), which no metric theory provides.  The last door closes on the data.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
