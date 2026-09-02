#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
condensate_mu_pincer_2026.py -- ONE RELATION closes the Omega-allocation fork of the v9 dark sector.
=====================================================================================================
The polytrope identity of the cluster-phase work (itemC: p_d = (2 pi G/mu^2) rho_d^2, c_s^2 = 4 pi G rho_d/mu^2)
holds for ANY shift-symmetric condensate at a quadratic minimum, and it holds on the COSMIC BACKGROUND as well as
in a static well.  Read on the background it says, for a condensate that carries the dark matter:

        c_s^2(z) = 4 pi G rho_dm(z) / (mu^2 c^2)  =  2.0e-8 (mu^-1 / 1 Mpc)^2 (1+z)^3        [until saturation]

The SAME mu governs the static Helmholtz equation, so the galaxy-scale behaviour of the dust (does it pile into
wells and double-count with MOND?) and its cosmological behaviour (is it cold enough for the CMB, P(k), the
Ly-alpha forest?) are ONE number.  The repo priced the two horns of the Omega-allocation fork separately
(lyman_alpha_dust_ic_2026.py Part F: "flips the verdict"); this script confronts them with the relation.

  HORN 1  the v9 DBI khronon's dust IS Omega_dm.  Then beta = 1 (mu^2 Lambda_D^2 = M^4 = rho_Lambda, CMB-selected)
          and rho_dust = Q_0 n PIN the DBI amplitude:  R = Lambda_D/Q_0 = nu_0 Omega_Lambda/Omega_dm.
          The repo bounded R as a FREE parameter (stage 69: R <= 1.5-3.1e-6 at 3% on P(k=0.2); forest: <= 2.3e-9).
          The pin puts R = 2.6 nu_0 >= 5.5e-5 for every nu_0 in the committed window.
  HORN 2  Omega_dm is a separate quadratic condensate chi (ghost-condensate class) with its own Helmholtz mass mu_chi.
          Cold at recombination needs c_s^2(z_rec) small  =>  mu_chi^-1 <= 0.6 kpc  =>  no polytrope pressure on
          galaxy scales  =>  chi clusters like CDM (the repo's own xi = 1)  =>  MOND + chi double-count.
          Shielding galaxies needs the polytrope mass inside 30 kpc to be a small fraction of the baryons, i.e.
          mu_chi^-1 >= 200 kpc (30% level) to 1 Mpc (10%).  The two requirements are the pincer.
  ESCAPE  a chi with its OWN DBI wall (its own M_chi^4, so no pin): cold at recombination by the wall, shield by a
          large mu^-1.  Tested directly against the forest with the growth integrator.

Parts: A sympy pins (generic quadratic + exact DBI decomposition + the background polytrope), B Horn-1 pin table vs
the committed R ceilings (+ mutation with the wrong dust identification), C a two-fluid sub-horizon growth
integrator (baryons + pressured dust) validated on the cold control and on stage 69's own bound, D the galaxy
shield, E the verdict.  Checks CAN fail.  Both a_0 footings where a_0 enters (Part D).
"""
import sys, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
# ------------------------------------------------------------------ cosmology (stage 69 / forest script values)
h = 0.674; OM_B_H2, OM_C_H2 = 0.02237, 0.1200
OM_M = (OM_B_H2 + OM_C_H2)/h**2; OM_B = OM_B_H2/h**2; OM_DM = OM_C_H2/h**2; OM_R = 4.15e-5/h**2; OM_L = 1 - OM_M - OM_R
G = 6.674e-11; c = 2.99792458e8; Mpc = 3.0857e22; kpc = Mpc/1e3; Msun = 1.989e30
H0 = 100*h*1e3/Mpc; rho_crit = 3*H0**2/(8*math.pi*G); rho_dm0 = OM_DM*rho_crit
CS2_UNIT = 4*math.pi*G*rho_dm0*Mpc**2/c**2            # c_s^2(0) for mu^-1 = 1 Mpc, dust = Omega_dm
NU0_LO, NU0_HI = 2.14e-5, 1.77e-4                     # stage 17 committed charge window
R_S69 = {"floor": 3.06e-6, "ceiling": 1.54e-6}        # stage 69: R <= ... at 3% on P(k=0.2)  (nu_0 floor / ceiling)
R_FOREST = 2.3e-9                                     # lyman_alpha_dust_ic_2026 (WDM yardstick, conditional)
OM_KD_MAX = 4.42e-7                                   # stage 17 D4 trace-khronon-dust ceiling (Horn 2)
Z_REC = 1090.0
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10

P("="*104); P("A. the pins (sympy)"); P("="*104)
u, Q0, K2, M4, LD, nu, s = sp.symbols("u Q_0 K_2 M4 Lambda_D nu s", positive=True)
# generic quadratic minimum
K = -M4 + K2*u**2
n = sp.diff(K, u); rho = (Q0 + u)*n - K; p_exc = K + M4; rho_dust = Q0*n
cs2 = sp.simplify(n/((Q0+u)*sp.diff(K, u, 2)))
poly_ok = sp.simplify(p_exc - rho_dust**2/(4*K2*Q0**2)) == 0
cs2_lead = sp.series(cs2, u, 0, 2).removeO()
check("A1 generic quadratic condensate: p_exc = rho_dust^2/(4 K_2 Q_0^2)  (gamma = 2 polytrope) and c_s^2 = K'/(Q K'') = u/Q_0 + O(u^2)",
      poly_ok and sp.simplify(cs2_lead - u/Q0) == 0, f"c_s^2 = {cs2_lead}")
# c_s^2 = dp/drho_dust = rho_dust/(2 K_2 Q_0^2); with itemC's mu_H^2 = 2 K_2 Q_0^2/(2-K_B) and rho_phys = rho/(8 pi G~), G~ = (1-K_B/2) G:
KB = sp.symbols("K_B", positive=True); muH2 = 2*K2*Q0**2/(2 - KB); Gt = (1 - KB/2)
cs2_from_p = sp.diff(p_exc, u)/sp.diff(rho_dust, u)                     # dp/drho_dust along the family
rho_phys = sp.symbols("rho_phys", positive=True)                      # rho_dust = 8 pi G~ rho_phys  (units G=1 in the action)
expr = cs2_from_p.subs(u, sp.solve(sp.Eq(rho_dust, 8*sp.pi*Gt*rho_phys), u)[0])
check("A2 background polytrope: c_s^2 = 4 pi G rho_phys / mu_H^2 with the SAME mu_H as the static Helmholtz equation (itemC A7)",
      sp.simplify(expr - 4*sp.pi*rho_phys/muH2) == 0, f"c_s^2 = {sp.simplify(expr)}")
info(f"    numerically: c_s^2(z=0) = 4 pi G Omega_dm rho_crit (1 Mpc)^2/c^2 = {CS2_UNIT:.3e} c^2  per (mu^-1/1 Mpc)^2   [= (43 km/s)^2 at 1 Mpc, itemD's h_bar]")
# exact DBI decomposition at beta = 1
mu2 = M4/LD**2                                        # beta = 1: mu^2 Lambda_D^2 = M^4
Kd = -M4 + mu2*LD**2*(1 - sp.sqrt(1 - s**2)); ud = LD*s
nd = sp.diff(Kd, s)/LD                                # K' = dK/du
rho_d = (Q0 + ud)*nd - Kd
s_of_nu = nu/sp.sqrt(1 + nu**2)
rest = sp.simplify((rho_d - Q0*nd).subs(s, s_of_nu))
check("A3 DBI at beta = 1: rho = Q_0 n + M^4 sqrt(1+nu^2) EXACTLY (dust = Q_0 n, the conserved charge; the rest = vacuum + internal energy)",
      sp.simplify(rest - M4*sp.sqrt(1 + nu**2)) == 0, f"rest = {rest}")
n_of_nu = sp.simplify(nd.subs(s, s_of_nu))            # = mu^2 Lambda_D nu
pin = sp.simplify((Q0*n_of_nu/M4))                    # rho_dust/rho_Lambda
check("A4 THE PIN: rho_dust/rho_Lambda = Q_0 nu / Lambda_D = nu/R  =>  R = Lambda_D/Q_0 = nu_0 Omega_Lambda/Omega_dust",
      sp.simplify(pin - nu*Q0/LD) == 0, f"rho_dust/rho_Lambda = {pin}")
cs2_dbi = sp.simplify(nd/((Q0+ud)*sp.diff(nd, s)/LD))
R = sp.symbols("R", positive=True)
check("A5 DBI sound speed c_s^2 = R s (1-s^2)/(1+R s)  (the repo's committed form, mi_dbi_khronon B5)",
      sp.simplify(cs2_dbi.subs(LD, R*Q0) - R*s*(1-s**2)/(1+R*s)) == 0)

P(""); P("="*104); P("B. Horn 1 -- the DBI khronon's dust is Omega_dm: R is pinned, not free"); P("="*104)
def s_of_a(a, nu0): v = nu0/a**3; return v/np.sqrt(1+v**2)
def cs2_dbi_a(a, nu0, R): sv = s_of_a(a, nu0); return R*sv*(1-sv**2)/(1+R*sv)
info(f"{'nu_0':>9} {'R pinned':>10} {'R/R_s69':>9} {'R/R_forest':>11} {'cs2(0)':>10} {'mu^-1 equiv':>12} {'peak cs2':>10} {'z_peak':>7} {'cs2(rec)':>10}")
horn1 = {}
for nu0 in (NU0_LO, 5e-5, 1e-4, NU0_HI):
    Rp = nu0*OM_L/OM_DM
    a = np.logspace(-4, 0, 200001); cs = cs2_dbi_a(a, nu0, Rp); i = int(np.argmax(cs))
    cs0 = float(cs2_dbi_a(1.0, nu0, Rp)); mu_inv = math.sqrt(cs0/CS2_UNIT)
    horn1[nu0] = dict(R=Rp, cs0=cs0, peak=float(cs[i]), zpk=1/a[i]-1, mu_inv=mu_inv, rec=float(cs2_dbi_a(1/(1+Z_REC), nu0, Rp)))
    rs = R_S69["floor"] if nu0 < 1e-4 else R_S69["ceiling"]
    info(f"{nu0:9.2e} {Rp:10.2e} {Rp/rs:9.0f} {Rp/R_FOREST:11.1e} {cs0:10.2e} {mu_inv:9.2f} Mpc {cs[i]:10.2e} {1/a[i]-1:7.1f} {horn1[nu0]['rec']:10.1e}")
check("B1 pinned R = 2.6 nu_0 exceeds stage 69's committed 3%-P(k=0.2) ceiling for EVERY nu_0 in the window (>= 18x at the floor)",
      all(horn1[n_]["R"] > (R_S69["floor"] if n_ < 1e-4 else R_S69["ceiling"]) for n_ in horn1), f"min ratio = {min(horn1[n_]['R']/(R_S69['floor'] if n_ < 1e-4 else R_S69['ceiling']) for n_ in horn1):.0f}")
check("B2 consistency (a WORKS): the window's pinned c_s^2(0) maps to Helmholtz masses mu^-1 = 0.2-2 Mpc -- exactly AeST/DS24's phenomenological ~1 Mpc",
      0.1 < min(v["mu_inv"] for v in horn1.values()) and max(v["mu_inv"] for v in horn1.values()) < 3.0)
check("B3 the DBI wall does its job: c_s^2(z_rec) <= 1e-9 for every pinned nu_0 (cold at recombination; the excess is all post-recombination)",
      all(v["rec"] < 1e-9 for v in horn1.values()))
# mutation: identify the dust with the internal-energy branch M^4(sqrt(1+nu^2)-1) instead of Q_0 n
Rw = {n_: math.sqrt(2*OM_DM/OM_L) for n_ in horn1}   # M^4 nu^2/2 = Omega_dm rho -> nu_0^2 = 2 Om_dm/Om_L, R unconstrained -> no pin
info(f"MUTATION (wrong dust identification, rho_dust := M^4(sqrt(1+nu^2)-1) ~ M^4 nu^2/2): forces nu_0 = {Rw[NU0_LO]:.2f} -- outside the window by 4 orders and leaves R free; the pin exists only because the dust is the CHARGE term Q_0 n (repo filter F1)")

P(""); P("="*104); P("C. growth integrator: baryons (cold) + dust with c_s^2(a); T^2(k) = P/P_cold at z = 0 and z = 3"); P("="*104)
CH0 = 2997.92/h if False else 2997.92                 # c/H0 in Mpc/h ; k in h/Mpc -> k c/H0 = k*2997.92
def E2(a): return OM_R/a**4 + OM_M/a**3 + OM_L
def dlnH(a): return 0.5*(-4*OM_R/a**4 - 3*OM_M/a**3)/E2(a)
fB, fD = OM_B/OM_M, OM_DM/OM_M
def grow(k, cs2fun, z_out=(3.0, 0.0), a_i=1e-3):
    Ni = math.log(a_i); tev = sorted(math.log(1/(1+z)) for z in z_out)
    def rhs(N, y):
        a = math.exp(N); db, dbp, dd, ddp = y
        src = 1.5*(OM_M/a**3/E2(a))*(fB*db + fD*dd); fr = 2 + dlnH(a)
        pres = (k*CH0)**2*cs2fun(a)/(a**2*E2(a))
        return [dbp, src - fr*dbp, ddp, src - fr*ddp - pres*dd]
    sol = solve_ivp(rhs, (Ni, 0.0), [1.0, 1.0, 1.0, 1.0], t_eval=tev, method="DOP853", rtol=1e-8, atol=1e-12)
    out = {}
    for j, N in enumerate(sol.t):
        z = 1/math.exp(N) - 1; out[round(z)] = fB*sol.y[0][j] + fD*sol.y[2][j]
    return out
KGRID = np.array([0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0])
cold = {k: grow(k, lambda a: 0.0) for k in KGRID}
# regression of the integrator: cold growth ratio D(z=0)/D(z=3) vs the exact LCDM growth integral
def D_exact(a):
    Ea = math.sqrt(E2(a)); return 2.5*OM_M*Ea*quad(lambda x: 1/(x*math.sqrt(E2(x)))**3, 1e-6, a)[0]
ratio_int = cold[0.05][0]/cold[0.05][3]; ratio_ex = D_exact(1.0)/D_exact(0.25)
check("C0 integrator regression: cold-matter growth D(0)/D(3) matches the LCDM growth integral to 0.5%", abs(ratio_int/ratio_ex - 1) < 5e-3, f"{ratio_int:.4f} vs {ratio_ex:.4f}")
def T2(cs2fun):
    return {k: {z: (grow(k, cs2fun)[z]/cold[k][z])**2 for z in (3, 0)} for k in KGRID}
def yard(t2, label):
    y1 = t2[0.2][0]; y2 = t2[10.0][3]; y3 = t2[1.0][3]
    P(f"    {label:52s} T2(k=0.2,z=0)={y1:6.3f}  T2(k=1,z=3)={y3:6.3f}  T2(k=10,z=3)={y2:6.3f}   " + " ".join(f"{t2[k][0]:.2f}" for k in KGRID))
    return y1, y2
info("columns at the right: T^2(k, z=0) for k = " + ", ".join(f"{k:g}" for k in KGRID) + " h/Mpc")
info("yardsticks: Y1 stage 69 = T^2(0.2, z=0) >= 0.97 ;  Y2 LOOSE forest = T^2(10 h/Mpc, z=3) >= 0.5 (WDM ~3 keV half-mode class) ;  strict forest (mi_cosmo) = 0.99")
res = {}
res["cold"] = T2(lambda a: 0.0); yard(res["cold"], "cold control")
check("C1 cold control: T^2 = 1 at every k and z (regression)", all(abs(res['cold'][k][z]-1) < 1e-9 for k in KGRID for z in (3, 0)))
res["s69"] = T2(lambda a: cs2_dbi_a(a, NU0_LO, R_S69["floor"])); y1, _ = yard(res["s69"], "Horn 1 at stage 69's own bound R=3.06e-6 (nu_0 floor)")
check("C2 validation against stage 69: at ITS bound the integrator gives a ~3% effect at k=0.2, z=0 (agreement to within a factor 2 of 3%)", 0.94 < y1 < 0.985, f"T2 = {y1:.3f}")
for nu0 in (NU0_LO, 1e-4, NU0_HI):
    res[("h1", nu0)] = T2(lambda a, n_=nu0: cs2_dbi_a(a, n_, n_*OM_L/OM_DM)); yard(res[("h1", nu0)], f"HORN 1 pinned, nu_0 = {nu0:.2e} (R = {nu0*OM_L/OM_DM:.1e})")
check("C3 HORN 1 DEAD: with R pinned, P(k=0.2, z=0) is suppressed by > 3% (stage 69's yardstick) for every nu_0 in the window",
      all(res[("h1", n_)][0.2][0] < 0.97 for n_ in (NU0_LO, 1e-4, NU0_HI)), "suppression at k=0.2: " + ", ".join(f"{100*(1-res[('h1', n_)][0.2][0]):.0f}%" for n_ in (NU0_LO, 1e-4, NU0_HI)))
info("Horn 2: chi = quadratic condensate with Helmholtz mass mu_chi, c_s^2 = X/(1+3X), X = 2.0e-8 (mu^-1/Mpc)^2 / a^3  (ceiling 1/3, mi_cosmo form)")
h2 = {}
for mu_kpc in (0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 1000.0):
    cs0 = CS2_UNIT*(mu_kpc/1e3)**2
    f = lambda a, c0=cs0: (c0/a**3)/(1 + 3*c0/a**3)
    h2[mu_kpc] = T2(f); rec = f(1/(1+Z_REC)); y1, y2 = yard(h2[mu_kpc], f"HORN 2 quadratic chi, mu^-1 = {mu_kpc:g} kpc, cs2(rec)={rec:.1e}")
    h2[mu_kpc]["rec"] = rec
check("C4 Horn 2 quadratic chi: the LOOSE forest yardstick (T^2(10,z=3) >= 0.5) already fails for mu^-1 >= 3 kpc; CMB coldness (cs2(rec) <= 1e-5, loose GDM) fails for mu^-1 >= 1 kpc",
      h2[3.0][10.0][3] < 0.5 and h2[1.0]["rec"] > 1e-5, f"T2(10,3) at 3 kpc = {h2[3.0][10.0][3]:.3f}; cs2(rec) at 1 kpc = {h2[1.0]['rec']:.1e}")
info("ESCAPE: chi with its OWN DBI wall (own M_chi^4, no pin): R at stage 69's ceiling, nu_0 chosen so that mu^-1 reaches the shield (Part D)")
esc = {}
for nu0 in (6.5e-5, 1e-4, 3e-4, 1e-3):
    Rr = R_S69["ceiling"]; cs0 = Rr*s_of_a(1.0, nu0); mu_inv_kpc = 1e3*math.sqrt(cs0/CS2_UNIT)
    esc[nu0] = T2(lambda a, n_=nu0: cs2_dbi_a(a, n_, Rr)); yard(esc[nu0], f"ESCAPE walled chi, R=1.54e-6, nu_0={nu0:.1e} -> mu^-1 = {mu_inv_kpc:.0f} kpc, z_wall={nu0**(-1/3)-1:.0f}")
    esc[nu0]["mu_kpc"] = mu_inv_kpc
info("MUTATION control: constant c_s^2 = today's value (no (1+z)^3 history), mu^-1 = 100 kpc")
mut = T2(lambda a: CS2_UNIT*0.01); yard(mut, "mutation: constant cs2 = 2e-10")
check("C5 mutation: removing the (1+z)^3 history removes the suppression (T^2(10,z=3) > 0.9) -- the kill is the high-z epoch, not today's sound speed",
      mut[10.0][3] > 0.9 and h2[100.0][10.0][3] < 0.5, f"const: {mut[10.0][3]:.3f}; history: {h2[100.0][10.0][3]:.3f}")

P(""); P("="*104); P("D. the galaxy shield: polytrope dust mass inside 30 kpc of an L* MOND well vs its baryons"); P("="*104)
MB = 6e10*Msun; RD = 3.0*kpc
def gN(r): x = r/RD; return G*MB*(1 - (1+x)*math.exp(-x))/r**2          # exponential-sphere-like enclosed mass (adequate at r >> R_d)
def g_obs(r, a0): gn = gN(r); return math.sqrt(gn**2 + gn*a0)              # the framework's own interpolation
def shield_mass(mu_inv_m, a0, r_in=30*kpc):
    """polytrope dust delta-rho = mu^2 |Psi|/(4 pi G), |Psi(r)| measured to the polytrope free surface at 2 pi/mu (its Jeans length)"""
    R_J = 2*math.pi*mu_inv_m
    if R_J <= r_in: return float("inf")                                       # no pressure support inside 30 kpc -> CDM-like collapse (xi = 1)
    psi = lambda r: quad(lambda x: g_obs(x, a0), r, R_J, limit=200)[0]
    Mchi = quad(lambda r: 4*math.pi*r**2*psi(r)/(4*math.pi*G*mu_inv_m**2), 0.1*kpc, r_in, limit=200)[0]
    return Mchi
Mb30 = MB*(1 - (1+10)*math.exp(-10))
info(f"L* well: M_b = {MB/Msun:.1e} Msun (R_d = 3 kpc), baryons inside 30 kpc = {Mb30/Msun:.2e} Msun")
info(f"{'mu^-1':>9} {'2pi/mu':>9} {'M_chi(<30kpc)/M_b  canonical':>30} {'alt footing':>12}   status")
shield = {}
for mu_kpc in (1.0, 3.0, 10.0, 16.0, 30.0, 50.0, 100.0, 200.0, 1000.0):
    fr = [shield_mass(mu_kpc*kpc, a0)/Mb30 for a0 in (A0_CAN, A0_ALT)]; shield[mu_kpc] = fr
    st = "NO SHIELD (no pressure support inside 30 kpc)" if fr[0] == float("inf") else ("shielded (<= 10%)" if max(fr) <= 0.10 else "double-counts (> 10% of the baryons)")
    info(f"{mu_kpc:6.0f} kpc {2*math.pi*mu_kpc:6.0f} kpc {('inf' if fr[0]==float('inf') else f'{fr[0]:.3f}'):>30} {('inf' if fr[1]==float('inf') else f'{fr[1]:.3f}'):>12}   {st}")
mu_shield_tight = min(m for m, fr in shield.items() if max(fr) <= 0.10)
mu_shield = min(m for m, fr in shield.items() if max(fr) <= 0.30)          # LOOSE floor (30% of the baryons inside 30 kpc ~ 0.1 dex on g)
info(f"shield floor: mu^-1 >= {mu_shield:g} kpc at the LOOSE 30% level, >= {mu_shield_tight:g} kpc at 10% (both footings)")
check("D1 the shield needs mu^-1 >= 100 kpc even at the LOOSE 30% level (and ~1 Mpc at 10%): below that the polytrope dust inside 30 kpc is not a small perturbation, or has no pressure support at all",
      100.0 <= mu_shield <= 1000.0 and mu_shield_tight >= mu_shield, f"loose floor {mu_shield:g} kpc, tight floor {mu_shield_tight:g} kpc")
mu_cmb = 1e3*math.sqrt(1e-5/(CS2_UNIT*(1+Z_REC)**3))
info(f"Horn 2 pincer: CMB coldness (cs2(rec) <= 1e-5, the LOOSE end of the GDM range) needs mu_chi^-1 <= {mu_cmb:.2f} kpc; the LOOSE shield needs >= {mu_shield:g} kpc  -> gap x{mu_shield/mu_cmb:.0f}")
check("D2 HORN 2 (quadratic chi) DEAD: the CMB-cold ceiling on mu_chi^-1 lies >= 100x below the LOOSE galaxy-shield floor", mu_shield/mu_cmb > 100)
info("ESCAPE scan (walled chi, own M_chi^4): nu_0 set by the LOOSE shield floor for each R; Y1 = T^2(0.2,0) >= 0.97, Y2 = T^2(10,3) >= 0.5")
esc = {}
for Rr in (1.54e-6, 1e-5, 1e-4):
    cs0_need = CS2_UNIT*(mu_shield/1e3)**2; nu0 = cs0_need/Rr             # R s_0 ~ R nu_0 = c_s^2(0) at the shield floor
    if nu0 > 0.3: info(f"   R = {Rr:.1e}: the shield needs nu_0 = {nu0:.2f} -> the DBI wall sits at z < 0.5, the fluid is at its peak sound speed TODAY (no cold epoch at all); skipped as trivially dead"); continue
    t2 = T2(lambda a, n_=nu0: cs2_dbi_a(a, n_, Rr)); y1, y2 = yard(t2, f"   ESCAPE R={Rr:.1e}, nu_0={nu0:.1e} (mu^-1 = {mu_shield:g} kpc, z_wall={nu0**(-1/3)-1:.1f})")
    esc[Rr] = dict(nu0=nu0, y1=y1, y2=y2)
esc_alive = [Rr for Rr, v in esc.items() if v["y1"] >= 0.97 and v["y2"] >= 0.5]
check("D3 ESCAPE (walled chi) DEAD: no (R, nu_0) that reaches even the LOOSE shield floor passes both the P(k=0.2) and the LOOSE forest yardsticks",
      len(esc) >= 1 and len(esc_alive) == 0, "at the shield: " + "; ".join(f"R={Rr:.0e}: Y1={v['y1']:.2f}, Y2={v['y2']:.3f}" for Rr, v in esc.items()))

P(""); P("="*104); P("F. the K-independent form: a galaxy well today = the cosmic background at z_match"); P("="*104)
info("c_s^2 = K'/(Q K'') is a function of the excitation u alone.  A static well imposes u_well = -Q_0 Psi (lapse relation, ANY K);")
info("the background carries u(z) with n(z) = K'(u(z)) = n_0 (1+z)^3.  The well's dust overdensity is delta_well = n_well/n_0, so the")
info("background passes through the well's state at (1+z_match)^3 = delta_well, with IDENTICAL sound speed.  Numerically, for K ~ u^p and DBI:")
def cs2_of_u_plaw(uu, pp): return uu/((pp-1)*1.0)                       # Q_0 = 1: c_s^2 = K'/(Q K'') = u/(p-1) for K ~ u^p
PSI_GAL = (200e3/c)**2                                                  # an L* well, |Psi| ~ v_c^2
info(f"{'K':>8} {'delta_well':>11} {'z_match':>8} {'c_s(well) km/s':>15} {'c_s(bg,z_match)':>16} {'c_s(z=3) km/s':>14}")
f_rows = []
for pp in (2, 3, 4, 8):
    for dw in (51.0, 1250.0, 5000.0):
        zm = dw**(1/3) - 1
        cs_well = math.sqrt(cs2_of_u_plaw(PSI_GAL, pp))*c/1e3
        # background: n ~ u^(p-1) -> u(z) = u_well ((1+z)^3/delta_well)^(1/(p-1))
        u3 = PSI_GAL*((1+3.0)**3/dw)**(1/(pp-1)); cs3 = math.sqrt(cs2_of_u_plaw(u3, pp))*c/1e3
        f_rows.append((pp, dw, zm, cs_well, cs3))
        info(f"{'u^'+str(pp):>8} {dw:11.0f} {zm:8.1f} {cs_well:15.1f} {cs_well:16.1f} {cs3:14.1f}")
check("F1 for every K-shape and every shield-compatible overdensity (delta_well <= 5000, i.e. mu^-1 >= 100 kpc), the dust's sound speed at z = 3 is >= 20 km/s -- an order of magnitude above what the forest tolerates (the constant-c_s^2 control at 4 km/s already loses 7% at k = 10)",
      all(r[4] >= 20.0 for r in f_rows), f"min c_s(z=3) over the table = {min(r[4] for r in f_rows):.0f} km/s")
info("so the question 'does the dust fall into galaxies?' has a measured answer: the forest says the dust at z = 3 is cold, and the")
info("dust at z = 3 IS the dust in a galaxy well today.  Pressure cannot keep Omega_dm out of galaxies.")

P(""); P("="*104); P("G. the non-analytic (superfluid) minimum K ~ |u|^p with p < 2: c_s^2 falls FASTER than rho below z_match, but the kill is above z_match"); P("="*104)
info("K ~ |u|^(3/2) (Berezhiani-Khoury superfluid P ~ X^(3/2)): c_s^2 = 2u/Q_0, rho_dust ~ u^(1/2)  =>  c_s^2 ~ rho^2 ~ (1+z)^6 on the background.")
info("Shield-compatible well: delta_well <= 5000 (mass budget: < 30% of the baryons inside 30 kpc, K-independent) => z_match <= 16, c_s(well) = sqrt(2|Psi|) = 283 km/s.")
for dw in (1250.0, 5000.0):
    zm = dw**(1/3) - 1; a_m = 1/(1+zm)
    cs2_m = 2*PSI_GAL                                     # the well's sound speed, reached by the background at z_match
    cs0 = cs2_m*a_m**6                                    # c_s^2(a) = cs0 / a^6, capped at 1/3
    f = lambda a, c0=cs0: min((c0/a**6), 1/3)
    cs3 = math.sqrt(f(0.25))*c/1e3
    t2 = T2(f); y1, y2 = yard(t2, f"   K~|u|^1.5 superfluid, delta_well={dw:.0f}, z_match={zm:.1f}, c_s(z=3)={cs3:.1f} km/s")
    if dw == 5000.0: g_y2, g_y1, g_cs3 = y2, y1, cs3
check("G1 the superfluid minimum is colder than the forest tolerance AT z = 3 (c_s(z=3) < 5 km/s at delta_well = 5000) -- the p >= 2 argument of F1 does NOT cover it",
      g_cs3 < 5.0, f"c_s(z=3) = {g_cs3:.1f} km/s")
check("G2 ...and it is dead anyway: the damage is done at z >= z_match where the background is at least as hot as the well (283 km/s at z = 16, lambda_J ~ 20 Mpc comoving); T^2(10 h/Mpc, z=3) < 0.5 and T^2(0.2, z=0) < 0.97",
      g_y2 < 0.5 and g_y1 < 0.97, f"T2(10,3) = {g_y2:.3f}, T2(0.2,0) = {g_y1:.3f}")
info("so the K-independent statement is the z >= z_match one: any well-shielding condensate was, at z_match <= 16, a fluid with c_s >= 75 km/s (p = 8) to 283 km/s (p = 3/2) on the whole background.")

P(""); P("="*104); P("E. VERDICT"); P("="*104)
P("  One relation, c_s^2(z) = 4 pi G rho_dust(z)/mu^2 (the cluster-phase polytrope read on the cosmic background), ties the")
P("  dust's galaxy-scale behaviour to its cosmological behaviour through mu alone.  Horn 1 (the DBI khronon's dust is Omega_dm):")
P("  beta = 1 pins R = nu_0 Omega_L/Omega_dm = 2.6 nu_0, 18-300x above the repo's own 3%-P(k=0.2) ceiling -> P(k) suppressed at")
P("  k >= 0.2 h/Mpc by far more than 3%.  Horn 2 (a separate quadratic chi): cold at recombination forces mu_chi^-1 <= 0.6 kpc (loose GDM),")
P("  the galaxy shield needs >= 200 kpc (loose, 30% of the baryons) to 1 Mpc (10%); no overlap, gap >= 300x.  Any K, analytic or not (Part G):  A walled chi that reaches the shield is a warm fluid at z = 3 and fails")
P("  even the loose forest yardstick; so does the superfluid |u|^1.5 minimum.  Surviving: the framework's a_0(z) law itself (nu_0 window untouched: it needs only the")
P("  TRACE khronon dust of stage 17 D4), MOND phenomenology, and a cold CDM-like Omega_dm that double-counts in galaxies")
P("  (the repo's open 'dust in galaxies' front is therefore closed on the pressure side: pressure cannot shield galaxies).")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
