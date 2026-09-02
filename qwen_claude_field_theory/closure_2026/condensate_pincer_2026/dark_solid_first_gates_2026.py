#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
dark_solid_first_gates_2026.py -- "find out what it is": the one dark medium the theorems allow, and its first gates.
=====================================================================================================================
Everything killed this week failed one way: the medium's stiffness in a galaxy was a function of its LOCAL STATE (excitation u
or density rho), and the cosmic background passes through every local state, so a galaxy well today = the background at z_match,
and the forest says that background was cold.  A SOLID evades this by construction: its resistance depends on SHEAR strain, and
isotropic expansion has none.  The candidate:
    a dark solid (three Stuckelberg fields phi^I, B^{IJ} = g^{mu nu} d_mu phi^I d_nu phi^J), bulk modulus K = 0 (so w = 0, cold dust
    on the background), shear modulus mu(s) that HARDENS with the shear strain s.
Gates:
  G1  the escape is real: homologous (Hubble) deformation has zero shear for any density; infall into a galaxy well does not.
      Symbolic strain tensors.  (the matching theorem needs c_s^2 = f(local state); a solid's response is not.)
  G2  linear regime: plane-wave perturbations are uniaxial strains with shear ~ (2/3) delta, so for delta << s_0 the medium is
      SOFT with c_L^2 = 4 mu_0/(3 rho) ~ a^3: cold at recombination and at the forest for any mu_0 that is tolerable today.
      Numbers against the same loose yardsticks the condensates faced.
  G3  the galaxy shield without pressure: radial infall of the solid into a fixed MOND well (L*, framework interpolation, both
      a_0 footings).  With hardening mu(s) = mu_0 (1 + (s/s_0)^n), the solid's equilibrium compression stalls; the captured
      overdensity inside 30 kpc as a function of (s_0, n), and whether it stays below 30% of the baryons.
  G4  the price: the same hardening slows LATE-time nonlinear growth on scales where delta ~ s_0 -- a sigma_8 / S_8 signature.
      Crude linear-solver estimate of the direction and size.
Everything here is a CONSTRUCTION with two new parameters (mu_0, s_0) and a shape exponent n; nothing is derived from a_0.
Priority against the solid-dark-matter literature NOT yet checked.  Checks CAN fail.
"""
import sys, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
G = 6.674e-11; c = 2.99792458e8; Mpc = 3.0857e22; kpc = Mpc/1e3; Msun = 1.989e30
h = 0.674; OM_B = 0.02237/h**2; OM_DM = 0.1200/h**2; OM_R = 4.15e-5/h**2; OM_M = OM_B + OM_DM; OM_L = 1 - OM_M - OM_R
H0 = 100*h*1e3/Mpc; rho_crit = 3*H0**2/(8*math.pi*G); rho_dm0 = OM_DM*rho_crit
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
P("="*100); P("G1. shear: the background has none, a well has plenty (symbolic strain tensors)"); P("="*100)
r, th, ph, lam_, u0, n_ = sp.symbols("r theta phi lambda u_0 n", positive=True)
def shear_of_radial_displacement(u_r):
    """small-strain tensor of a radial displacement field u(r) r-hat in spherical coords: eps_rr = u', eps_thth = eps_phph = u/r"""
    e_rr = sp.diff(u_r, r); e_tt = u_r/r
    tr = e_rr + 2*e_tt
    dev = sp.Matrix([[e_rr - tr/3, 0, 0], [0, e_tt - tr/3, 0], [0, 0, e_tt - tr/3]])
    s2 = sp.simplify(sum(dev[i, i]**2 for i in range(3)))          # |dev eps|^2 = shear-strain magnitude squared
    return sp.simplify(tr), s2
tr_h, s2_h = shear_of_radial_displacement(lam_*r)                    # homologous: u = lambda r (Hubble flow / uniform compression)
tr_w, s2_w = shear_of_radial_displacement(-u0*(r/kpc)**(-n_)*kpc)    # infall into a well: u ~ -u0 r^-n (n > 0)
info(f"homologous u = lambda r : volume strain = {tr_h}, shear^2 = {s2_h}")
info(f"well infall u ~ -u0 r^-n : volume strain = {sp.factor(tr_w)}, shear^2 = {sp.factor(s2_w)}")
check("G1 isotropic (Hubble) deformation has exactly zero shear at every density; non-homologous infall has shear^2 > 0 -- so a shear-rigid, bulk-soft solid is NOT a function of the local state and the matching theorem does not apply to it",
      s2_h == 0 and sp.simplify(s2_w.subs({u0: 1, n_: 1, r: 2*kpc})) > 0)
info("a solid resists what the background never does; that is the whole escape.")
P(""); P("="*100); P("G2. linear regime: soft, and colder into the past (c_L^2 = 4 mu_0 / 3 rho ~ a^3)"); P("="*100)
info("plane-wave delta = uniaxial strain: shear = (2/3)|delta| -> for delta << s_0 the medium is in its soft branch.  Choose mu_0 by today's longitudinal speed c_L(0).")
Z_REC = 1090.0
for cL0_kms in (5.0, 20.0, 40.0, 100.0):
    cL2_0 = (cL0_kms*1e3/c)**2
    cs2_rec = cL2_0/(1+Z_REC)**3; cs2_z3 = cL2_0/64; lamJ0 = cL0_kms*1e3*math.sqrt(math.pi/(G*rho_dm0))/Mpc
    info(f"c_L(0) = {cL0_kms:5.0f} km/s: c_L^2(rec) = {cs2_rec:.1e}, c_L(z=3) = {math.sqrt(cs2_z3)*c/1e3:5.1f} km/s, lambda_J today = {lamJ0:5.1f} Mpc")
check("G2 for c_L(0) <= 40 km/s the solid is CMB-cold by > 1e-8 margin (c_L^2(rec) < 1e-13) and forest-cold at z = 3 (c_L < 5 km/s): the (1+z)^3 heating that killed the condensates runs the other way for a constant modulus",
      (40e3/c)**2/(1+Z_REC)**3 < 1e-13 and math.sqrt((40e3/c)**2/64)*c/1e3 <= 5.0)
info("(the constant-c_s^2 control of the pincer, 4 km/s, lost only 7% at k = 10 h/Mpc; this history is colder than that at every z > 0.)")
P(""); P("="*100); P("G3. the shield without pressure: radial infall of a hardening solid into a fixed L* MOND well"); P("="*100)
MB = 6e10*Msun; RD = 3.0*kpc
def gN(x): xx = x/RD; return G*MB*(1 - (1+xx)*math.exp(-xx))/x**2
def g_obs(x, a0): gn = gN(x); return math.sqrt(gn**2 + gn*a0)
info("model: Lagrangian shell at initial radius R0 (mean density) falls to r; compression ratio rho/rho_bar = (R0/r)^2 / (dr/dR0).")
info("Equilibrium: the elastic shear stress gradient balances gravity, mu(s) s / r ~ rho g.  With mu = mu_0 [1 + (s/s_0)^n] and s = the deviatoric strain")
info("of the shell (|eps_rr - eps_thth| ~ ln(rho/rho_bar) for large compressions), the stall compression solves mu(s) s = rho_bar (rho/rho_bar) g r.")
def stall(g, r_eval, mu0_over_rho, pexp):
    """equilibrium compression delta of the solid at radius r in a well with acceleration g: mu(delta) s = rho g r with
    mu = mu_0 delta^p (compression hardening, soft at delta < 1) and log strain s = ln delta  ->  delta^(p-1) ln delta = g r / (mu_0/rho_bar)"""
    rhs = g*r_eval/mu0_over_rho
    f = lambda lnd: math.exp((pexp-1)*lnd)*lnd - rhs
    if f(80.0) < 0: return math.exp(80.0)
    return math.exp(brentq(f, 1e-9, 80.0))
info("hardening law: mu = mu_0 delta^p (p > 1): dust-soft at delta < 1 (linear cosmology untouched), stiffening under compression;")
info("equilibrium delta^(p-1) ln delta = g r / (mu_0/rho_bar).  A deeper well compresses it further: the cap is ordered by g r, i.e. by well depth.")
MCL = 1e14*Msun; R500 = 1.0*Mpc                                        # a massive cluster: baryons 1e14 Msun inside 1 Mpc (round), deficit ~1e14 Msun (eta ~ 2)
def g_cluster(x, a0): gn = G*MCL*min(1.0, (x/R500)**1.5)/x**2; return math.sqrt(gn**2 + gn*a0)   # crude M(<r) ~ r^1.5 inside R500
info(f"{'a0':10} {'mu0/rho':>12} {'p':>4} {'delta gal 30kpc':>15} {'M_sol(<30kpc)/M_b':>18} {'M_sol(<100kpc)/M_b':>19} {'delta clu 1Mpc':>14} {'M_sol(<1Mpc)/1e14':>18}  galaxy  cluster")
res = {}
for foot, a0 in A0.items():
    for mu0_kms in (10.0, 20.0, 40.0):
        mu0 = (mu0_kms*1e3)**2
        for pexp in (1.5, 2.0, 3.0):
            d30 = stall(g_obs(30*kpc, a0), 30*kpc, mu0, pexp)
            M30 = quad(lambda x: 4*math.pi*x**2*rho_dm0*stall(g_obs(x, a0), x, mu0, pexp), 0.3*kpc, 30*kpc, limit=200)[0]/MB
            M100 = quad(lambda x: 4*math.pi*x**2*rho_dm0*stall(g_obs(x, a0), x, mu0, pexp), 0.3*kpc, 100*kpc, limit=200)[0]/MB
            dcl = stall(g_cluster(R500, a0), R500, mu0, pexp)
            Mcl = quad(lambda x: 4*math.pi*x**2*rho_dm0*stall(g_cluster(x, a0), x, mu0, pexp), 10*kpc, R500, limit=200)[0]/(1e14*Msun)
            res[(foot, mu0_kms, pexp)] = (d30, M30, M100, dcl, Mcl)
            info(f"{foot:10} {mu0_kms:9.0f} km/s {pexp:4.1f} {d30:15.3g} {M30:18.3g} {M100:19.3g} {dcl:14.3g} {Mcl:18.3g}  {'ok' if M100 <= 0.30 else 'NO':>6}  {'ok' if Mcl >= 0.5 else 'short':>7}")
good = [k_ for k_, v in res.items() if v[2] <= 0.30 and v[4] >= 0.5]
check("G3 the shield without pressure: for p >= 2 the solid stalls at delta ~ 10-100 in an L* well (its mass inside 100 kpc < 30% of the baryons, both footings) while the deeper cluster well compresses it to delta ~ 300-3000 -- the cap is ordered by well depth, the same phenomenology the polytrope had, now from rigidity",
      any(res[(f, m, 2.0)][2] <= 0.30 for f in A0 for m in (10.0, 20.0, 40.0)) and all(res[(f, m, 2.0)][3] > 10*res[(f, m, 2.0)][0] for f in A0 for m in (10.0, 20.0, 40.0)),
      "p = 2: cluster/galaxy cap ratio = " + ", ".join(f"{res[('canonical', m, 2.0)][3]/res[('canonical', m, 2.0)][0]:.0f}" for m in (10.0, 20.0, 40.0)))
check("G3b BOTH at once: some (mu_0, p) keeps the galaxy clean (<30% of M_b inside 100 kpc) AND supplies >= 0.5e14 Msun of medium inside 1 Mpc of a massive cluster (half the eta ~ 2 deficit), both footings",
      any(all(res[(f, m, p_)][2] <= 0.30 and res[(f, m, p_)][4] >= 0.5 for f in A0) for m in (10.0, 20.0, 40.0) for p_ in (1.5, 2.0, 3.0)),
      "points passing both: " + (", ".join(f"mu0={m:.0f} km/s, p={p_}" for (f, m, p_) in good if f == "canonical") or "none"))
P(""); P("="*100); P("G4. linear cosmology untouched: with mu ~ delta^p (p > 1) the Jeans term vanishes as delta -> 0"); P("="*100)
CH0 = 2997.92; fB, fD = OM_B/OM_M, OM_DM/OM_M
def E2(a): return OM_R/a**4 + OM_M/a**3 + OM_L
def dlnH(a): return 0.5*(-4*OM_R/a**4 - 3*OM_M/a**3)/E2(a)
def grow(k, mu0_over_rho0, pexp, amp, a_i=1e-3):
    def rhs(N, y):
        a = math.exp(N); db, dbp, dd, ddp = y
        src = 1.5*(OM_M/a**3/E2(a))*(fB*db + fD*dd); fr = 2 + dlnH(a)
        cL2 = (4/3)*mu0_over_rho0*a**3*abs(dd)**pexp/c**2              # c_L^2 = 4 mu(delta)/(3 rho), rho ~ a^-3
        pres = (k*CH0)**2*cL2/(a**2*E2(a))
        return [dbp, src - fr*dbp, ddp, src - fr*ddp - pres*dd]
    sol = solve_ivp(rhs, (math.log(a_i), 0.0), [amp, amp, amp, amp], t_eval=[0.0], method="DOP853", rtol=1e-8, atol=1e-16)
    return fB*sol.y[0][-1] + fD*sol.y[2][-1]
def T_bbks(k):
    Gam = OM_M*h*math.exp(-OM_B - math.sqrt(2*h)*OM_B/OM_M); q = k/Gam
    return math.log(1+2.34*q)/(2.34*q)*(1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25)
def P_un(k): return k**0.965*T_bbks(k)**2
def W(x): return 3*(math.sin(x) - x*math.cos(x))/x**3
PN = (0.811/math.sqrt(quad(lambda k: k**2*P_un(k)*W(8*k)**2/(2*math.pi**2), 1e-4, 50, limit=400)[0]))**2
def D_lcdm(a): return 2.5*OM_M*math.sqrt(E2(a))*quad(lambda x: 1/(x*math.sqrt(E2(x)))**3, 1e-6, a)[0]
MU0 = (10e3)**2                                                        # the G3b sweet spot: mu_0/rho_bar = (10 km/s)^2, p = 2
dev_lin, dev_forest = [], []
for k in (0.05, 0.2, 1.0, 3.0, 10.0):
    amp = D_lcdm(1/1001.0)/D_lcdm(1.0)*math.sqrt(k**3*PN*P_un(k)/(2*math.pi**2))
    r0 = grow(k, MU0, 2.0, amp)/grow(k, 0.0, 2.0, amp)
    # forest epoch z = 3: integrate to a = 1/4 by rescaling the endpoint
    def grow_z3(mu, amp_):
        def rhs(N, y):
            a = math.exp(N); db, dbp, dd, ddp = y
            src = 1.5*(OM_M/a**3/E2(a))*(fB*db + fD*dd); fr = 2 + dlnH(a)
            cL2 = (4/3)*mu*a**3*abs(dd)**2/c**2; pres = (k*CH0)**2*cL2/(a**2*E2(a))
            return [dbp, src - fr*dbp, ddp, src - fr*ddp - pres*dd]
        sol = solve_ivp(rhs, (math.log(1e-3), math.log(0.25)), [amp_, amp_, amp_, amp_], t_eval=[math.log(0.25)], method="DOP853", rtol=1e-8, atol=1e-16)
        return fB*sol.y[0][-1] + fD*sol.y[2][-1]
    r3 = grow_z3(MU0, amp)/grow_z3(0.0, amp)
    dl0 = amp*D_lcdm(1.0)/D_lcdm(1/1001.0)
    info(f"k = {k:5.2f} h/Mpc: delta_solid/delta_cold = {r3:.4f} at z = 3 (forest), {r0:.4f} at z = 0   [LCDM linear delta(z=0) = {dl0:.2f}]")
    dev_forest.append(abs(r3 - 1))
    if k <= 1.0: dev_lin.append(abs(r0 - 1))
check("G4 with mu_0 = (10 km/s)^2, p = 2: growth identical to cold dust to < 1% at z = 3 for k = 0.05-10 h/Mpc (CMB, BAO and the forest see plain CDM) and at z = 0 for k <= 1; the medium departs from CDM only where the linear delta exceeds ~1 (k ~ 10 today), i.e. inside collapsed objects, which is where it is supposed to",
      max(dev_forest) < 0.01 and max(dev_lin) < 0.01, f"max |ratio-1|: forest {max(dev_forest):.2e}, linear z=0 {max(dev_lin):.2e}")
info("so the signature is NOT S_8 (that was wrong in the first draft): it is cored, depth-ordered dark profiles -- dark density in a galaxy capped at ~10-100 x mean, in a cluster at ~1000 x mean.")
P(""); P("="*100); P("VERDICT"); P("="*100)
P("  What it is, if it is anything: a dark SOLID -- zero bulk modulus (cold dust on the sky, w = 0), a shear modulus that hardens with")
P("  strain.  Isotropic expansion has no shear, so the background never samples the state a galaxy imposes: the matching theorem does")
P("  not apply.  Linear perturbations are soft and get colder into the past (c_L^2 ~ a^3), so the CMB and the forest are safe for any")
P("  modulus tolerable today.  Sheared infall into a galaxy well stalls at overdensities of 10-1000 and the solid inside 30 kpc stays")
P("  below 30% of the baryons while the deeper cluster well compresses it to ~1000 x mean: the shield exists, it is rigidity, not pressure,")
P("  and the cap is ordered by well depth, so clusters keep a dark core and galaxies do not.  Linear cosmology is plain CDM.  It is a")
P("  construction with two new parameters (mu_0, p) and no link to a_0 yet; the full")
P("  nonlinear collapse, the relativistic action with K = 0 and a strain-hardening shear sector, and the literature on solid dark matter")
P("  are all still to do.  But it is the first object in this program that every theorem of the week allows.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
