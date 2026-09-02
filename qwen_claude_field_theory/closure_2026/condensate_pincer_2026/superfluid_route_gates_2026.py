#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
superfluid_route_gates_2026.py -- "the dark field IS MOND": three gates on the superfluid route, on the framework's terms.
=========================================================================================================================
Route (2026-09-02): a cold Omega_dm component, NORMAL phase on the cosmic background (clusters like CDM at 100 Mpc, escapes the
matching theorem), that condenses inside galaxies and there produces the a_0 force itself as a phonon-mediated interaction
(Berezhiani-Khoury 2015 class), with a_0 ~ sqrt(rho_DE) fixing the coupling.  Gates:
  G1  kappa <-> alpha: BK's a_0 = alpha^3 Lambda^2 / M_Pl against the framework's a_0 = kappa c sqrt(G rho_DE), with the
      superfluid scale Lambda set to Lambda_DE = rho_DE^(1/4) = 2.24 meV.  Exact map, both footings, both M_Pl conventions.
  G2  the phase of the background: a self-interaction strong enough to thermalise halos (sigma/m >= 0.1 cm^2/g, BK's
      requirement; Bullet bound <= 1 cm^2/g) has Gamma/H ~ rho v / H ~ (1+z)^2.5 growing INTO THE PAST, so the cosmic gas
      thermalised at some z_th for ANY relic velocity, and n lambda_dB^3 >> 1 there => it condensed, and T/T_c is
      constant under expansion => it stays condensed.  The "normal phase on the background" premise is tested here.
  G3  once condensed on the background, the superfluid EOS P ~ rho^3 gives c_s^2 ~ rho^2 ~ (1+z)^6.  Anchored to a
      galaxy core that the phonons must support (c_s,core ~ v_c at rho_core ~ 1e5-1e6 x mean), the background sound
      speed at recombination and at z ~ 16-45 follows with NO free parameter; the growth integrator gives P(k).
Checks CAN fail.  Both a_0 footings.  BK's EOS normalisation (P = rho^3/(12 Lambda^2 m^6)) is used ONLY to quote an m,
flagged as recalled-from-the-paper; every kill below is independent of it.
"""
import sys, math
import numpy as np
from scipy.integrate import solve_ivp
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
h = 0.674; OM_B_H2, OM_C_H2 = 0.02237, 0.1200
OM_B = OM_B_H2/h**2; OM_DM = OM_C_H2/h**2; OM_R = 4.15e-5/h**2; OM_M = OM_B + OM_DM; OM_L = 1 - OM_M - OM_R
G = 6.674e-11; c = 2.99792458e8; hbar = 1.054571817e-34; kB = 1.380649e-23; eV = 1.602176634e-19; Mpc = 3.0857e22
H0 = 100*h*1e3/Mpc; rho_crit = 3*H0**2/(8*math.pi*G); rho_dm0 = OM_DM*rho_crit; rho_DE = OM_L*rho_crit*c**2
EV4_J = eV/((hbar*c/eV)**3)                                   # 1 eV^4 in J/m^3
LAM_DE = (rho_DE/EV4_J)**0.25                                 # eV
MPL_RED = math.sqrt(hbar*c/(8*math.pi*G))*c**2/eV             # reduced Planck mass, eV
MPL_NON = math.sqrt(hbar*c/G)*c**2/eV
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
P("="*104); P("G1. kappa <-> alpha with Lambda = Lambda_DE"); P("="*104)
info(f"Lambda_DE = rho_DE^(1/4) = {LAM_DE*1e3:.3f} meV ; M_Pl(reduced) = {MPL_RED:.3e} eV ; M_Pl(non-reduced) = {MPL_NON:.3e} eV")
def a0_from_alpha(alpha, Lam_eV, Mpl_eV): return c*(alpha**3*Lam_eV**2/Mpl_eV)*eV/hbar     # m/s^2
res_g1 = {}
for foot, a0 in A0.items():
    kappa = a0/(c*math.sqrt(G*rho_DE/c**2))
    for conv, Mpl in (("reduced", MPL_RED), ("non-reduced", MPL_NON)):
        alpha = (a0*hbar/(eV*c)*Mpl/LAM_DE**2)**(1/3)
        res_g1[(foot, conv)] = (kappa, alpha)
        info(f"{foot:10s} a_0 = {a0:.3e}: kappa = {kappa:.3f} ; M_Pl {conv:12s}: alpha = {alpha:.3f}  (check a_0(alpha) = {a0_from_alpha(alpha, LAM_DE, Mpl):.3e})")
kap_c, alp_c = res_g1[("canonical", "reduced")]
check("G1 the map is exact and O(1): alpha^3 = kappa/sqrt(8 pi) (reduced M_Pl) => kappa = 1/2 gives alpha = 0.464; kappa is an admissible superfluid coupling",
      abs(alp_c**3 - kap_c/math.sqrt(8*math.pi)) < 1e-3 and 0.3 < alp_c < 0.8, f"alpha = {alp_c:.3f}, kappa/sqrt(8pi) = {kap_c/math.sqrt(8*math.pi):.4f}")
info("note: BK's rotation-curve fits quote alpha ~ 2.5-5.7 with Lambda ~ 0.05 meV; only the combination alpha^3 Lambda^2 is fixed by a_0, so Lambda = Lambda_DE with alpha = 0.46 is the SAME a_0 -- the fits' other Lambda-dependence is not re-checked here")

P(""); P("="*104); P("G2. the phase of the cosmic background: thermalisation Gamma = rho (sigma/m) v vs H, and n lambda_dB^3"); P("="*104)
def E(z): return math.sqrt(OM_R*(1+z)**4 + OM_M*(1+z)**3 + OM_L)
def z_therm(sig_m, v0):
    """smallest z at which Gamma(z) = rho_dm(z) (sigma/m) v0 (1+z) equals H(z); Gamma/H ~ (1+z)^2.5 in the matter era"""
    f = lambda z: rho_dm0*(1+z)**3*sig_m*v0*(1+z)/(H0*E(z)) - 1.0
    lo, hi = 0.0, 1e9
    if f(lo) > 0: return 0.0
    for _ in range(200):
        mid = math.sqrt((lo+1)*(hi+1)) - 1
        if f(mid) > 0: hi = mid
        else: lo = mid
    return hi
info(f"{'sigma/m':>12} {'v_0 today':>10} {'z_therm':>9} {'rho/rho_0':>10} {'Gamma_halo/H0':>14}   n lambda_dB^3 at z_therm (m = 0.3 / 1 eV)")
rows = []
for sig_cm2g in (0.1, 1.0):
    sig_m = sig_cm2g*0.1                                        # cm^2/g -> m^2/kg
    for v0 in (1e-3, 1.0, 100.0):                               # km/s: ultra-cold, cold, warm relic
        zt = z_therm(sig_m, v0*1e3)
        gam_halo = 1e-21*sig_m*2e5/H0                           # inner halo: rho = 1e-21 kg/m^3 (0.015 Msun/pc^3, r <~ 10 kpc), v = 200 km/s
        ns = []
        for m_eV in (0.3, 1.0):
            m = m_eV*eV/c**2; n = rho_dm0*(1+zt)**3/m; v = v0*1e3*(1+zt)
            lam = 2*math.pi*hbar/(m*v); ns.append(n*lam**3)
        rows.append((sig_cm2g, v0, zt, gam_halo, ns))
        info(f"{sig_cm2g:9.1f} cm2/g {v0:7.0e} km/s {zt:9.0f} {(1+zt)**3:10.1e} {gam_halo:14.1f}   {ns[0]:.1e} / {ns[1]:.1e}")
check("G2a every (sigma/m, v_0) that thermalises the inner halo (Gamma_halo/H0 >= 1) also thermalised the background at some z_th <= 1e5, with n lambda_dB^3 > 10 there for m = 0.3-1 eV: the background CONDENSED",
      all(r[2] < 1e5 and min(r[4]) > 10 for r in rows if r[3] >= 1) and any(r[3] >= 1 for r in rows),
      "z_th = " + ", ".join(f"{r[2]:.0f}" for r in rows))
info("under expansion T ~ a^-2 and T_c ~ n^(2/3) ~ a^-2, so T/T_c is constant: a condensate formed at z_th does not evaporate.  The premise 'normal phase on the background' fails for this class.")

P(""); P("="*104); P("G3. the condensed background: c_s^2 = c_s,core^2 (rho/rho_core)^2, anchored to the galaxy core the phonons must support"); P("="*104)
Z_REC = 1090.0
def cs2_bg(a, cs_core_kms, dcore):
    x = (cs_core_kms*1e3/c)**2*((1/a**3)/dcore)**2
    return x/(1 + 3*x)                                          # relativistic ceiling 1/3
CH0 = 2997.92; fB, fD = OM_B/OM_M, OM_DM/OM_M
def E2(a): return OM_R/a**4 + OM_M/a**3 + OM_L
def dlnH(a): return 0.5*(-4*OM_R/a**4 - 3*OM_M/a**3)/E2(a)
def grow(k, cs2fun, z_out=(3.0, 0.0), a_i=1e-3):
    def rhs(N, y):
        a = math.exp(N); db, dbp, dd, ddp = y
        src = 1.5*(OM_M/a**3/E2(a))*(fB*db + fD*dd); fr = 2 + dlnH(a)
        pres = (k*CH0)**2*cs2fun(a)/(a**2*E2(a))
        return [dbp, src - fr*dbp, ddp, src - fr*ddp - pres*dd]
    tev = sorted(math.log(1/(1+z)) for z in z_out)
    sol = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0, 1.0, 1.0], t_eval=tev, method="DOP853", rtol=1e-8, atol=1e-12)
    return {round(1/math.exp(N)-1): fB*sol.y[0][j] + fD*sol.y[2][j] for j, N in enumerate(sol.t)}
KG = [0.2, 1.0, 3.0, 10.0]
cold = {k: grow(k, lambda a: 0.0) for k in KG}
info(f"{'c_s,core':>9} {'rho_core/mean':>13} {'z_match':>8} {'cs2(z=16)':>10} {'cs2(z=45)':>10} {'cs2(rec)':>10} {'T2(0.2,z=0)':>12} {'T2(1,3)':>8} {'T2(10,3)':>9}  CMB-cold?  forest?")
g3 = {}
for cs_core in (200.0, 50.0, 10.0, 1.0):
    for dcore in (1e5, 1e6):
        f = lambda a, cc=cs_core, dc=dcore: cs2_bg(a, cc, dc)
        t2 = {k: {z: (grow(k, f)[z]/cold[k][z])**2 for z in (3, 0)} for k in KG}
        rec = f(1/(1+Z_REC)); c16 = f(1/17.0); c45 = f(1/46.0)
        g3[(cs_core, dcore)] = dict(rec=rec, y1=t2[0.2][0], y2=t2[10.0][3])
        info(f"{cs_core:6.0f} km/s {dcore:13.0e} {dcore**(1/3)-1:8.0f} {c16:10.1e} {c45:10.1e} {rec:10.1e} {t2[0.2][0]:12.3f} {t2[1.0][3]:8.3f} {t2[10.0][3]:9.3f}  {'yes' if rec <= 1e-5 else 'NO':>8}  {'yes' if t2[10.0][3] >= 0.5 else 'NO':>6}")
phys = [(cc, dc) for cc in (200.0, 50.0, 10.0) for dc in (1e5, 1e6)]
check("G3a with the phonons supporting a galaxy core (c_s,core >= 10 km/s, any rho_core in 1e5-1e6 x mean) the condensed background is HOT at recombination: c_s^2(z_rec) > 1e-5 (loose GDM ceiling), most anchors relativistic",
      all(g3[p]["rec"] > 1e-5 for p in phys), "cs2(rec) = " + ", ".join(f"{g3[p]['rec']:.1e}" for p in phys))
check("G3b and it fails the LOOSE forest yardstick T^2(10 h/Mpc, z=3) >= 0.5 for every such anchor", all(g3[p]["y2"] < 0.5 for p in phys),
      "T2(10,3) = " + ", ".join(f"{g3[p]['y2']:.3f}" for p in phys))
info(f"the boundary: CMB-cold needs c_s,core <= ~1 km/s at rho_core = 1e6 x mean (cs2(rec) = {g3[(1.0, 1e6)]['rec']:.1e}), i.e. a superfluid 200x too soft to hold up a 200 km/s core; the phonon-force regime needs the opposite.")
# recalled BK normalisation, quoted only: P = rho^3/(12 Lambda^2 m^6)  =>  m^6 = rho_core^2/(4 Lambda^2 c_s,core^2)  (natural units)
rho_core_eV4 = 1e5*rho_dm0*c**2/EV4_J; cs2 = (2e5/c)**2
m6 = rho_core_eV4**2/(4*LAM_DE**2*cs2); m_eV = m6**(1/6)
info(f"(recalled BK EOS, unverified here) with Lambda = Lambda_DE and c_s,core = 200 km/s at 1e5 x mean: m = {m_eV:.2f} eV -- in BK's eV range, so the microphysics is not what fails")

P(""); P("="*104); P("VERDICT"); P("="*104)
P("  G1 works: kappa = 1/2 IS an admissible superfluid coupling (alpha = 0.46 with Lambda = Lambda_DE).  G2 closes the route's premise:")
P("  any self-interaction that thermalises halos thermalised the background earlier (Gamma/H grows into the past), where the gas")
P("  condensed and stays condensed.  G3 then applies the matching logic to the superfluid EOS: the background sound speed is")
P("  relativistic at recombination and 10-200 km/s at z ~ 16-45 for every core the phonons could support.  The dark field cannot")
P("  be MOND in galaxies and CDM on the background with one equation of state.  The door named in the one-sentence answer is shut.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
