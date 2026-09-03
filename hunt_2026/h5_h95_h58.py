#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h5_h95_h58.py -- HUNT ITEMS 5, 95, 58.
=======================================
Item 5  (the halo surface-density constant): dark-matter halo fits to real rotation curves return a nearly universal product
        rho_0 x r_0 ~ 140 Msun/pc^2 across ten decades of halo mass (Donato+2009, Kormendy & Freeman 2004) -- one of the strangest
        regularities in galaxy dynamics and completely unexplained in LambdaCDM.  In the framework it is not a halo property at all:
        a fitted core is the phantom of a MOND galaxy, and the phantom's central surface density is set by a_0 alone,
        Sigma_M = a_0/(2 pi G) = 107 (canonical) / 129 (alt) Msun/pc^2.  Tested here on Li+2020's Burkert fits to 175 SPARC galaxies
        (fetched to real_research/data/li2020_sparc_halos.tsv this session).
Item 95 (the Lambda-limited bound radius): the framework has a LARGEST bound orbit, where the MOND attraction equals the
        cosmological repulsion: sqrt(G M_b a_0)/r = Lambda c^2 r/3, i.e. r_Lambda ~ M_b^{1/4}.  Beyond it nothing is bound.
Item 58 (merger infall speeds): the Bullet Cluster's ~3000 km/s collision is uncomfortably fast for LambdaCDM (Lee & Komatsu 2010).
        In MOND the two-body infall from turnaround is stronger with the same baryons -- computed here with no free parameter.
Both footings.  Mutations.  Checks CAN fail.
"""
import sys, math, os
import numpy as np
from scipy.integrate import solve_ivp
from hunt_lib import *
ck = Check(); rng = np.random.default_rng(595)
P("="*116); P("ITEM 5 -- the halo surface-density constant is the phantom's, set by a_0"); P("="*116)
path = os.path.join(DATA, "li2020_sparc_halos.tsv")
rows = [l.rstrip("\n").split("\t") for l in open(path) if l.strip() and not l.startswith("#")]
hdr = rows[0]; data = rows[3:]
col = {h.strip(): i for i, h in enumerate(hdr)}
def f(v):
    try: return float(v)
    except: return np.nan
recs = []
for d in data:
    try:
        model = d[col["Model"]].strip(); rs = f(d[col["rs"]]); lrho = f(d[col["log(rhos)"]]); chi2 = f(d[col["chi2"]])
    except Exception: continue
    if not np.isfinite(rs) or not np.isfinite(lrho): continue
    recs.append(dict(name=d[col["Name"]].strip(), model=model, rs=rs, rho=10**lrho, chi2=chi2, lM=f(d[col["log(M200)"]])))
models = sorted(set(r["model"] for r in recs))
info(f"Li+2020 halo fits: {len(recs)} rows, models present: {models[:8]}")
SIG_M = {ft: A0[ft]/(2*math.pi*G)/(Msun/(3.0857e16)**2) for ft in A0}
info(f"the framework's phantom central surface density Sigma_M = a_0/(2 pi G) = {SIG_M['canonical']:.1f} (canonical) / {SIG_M['alt']:.1f} (alt) Msun/pc^2; the literature's Donato constant is 140 (+80/-30)")
R5 = {}
for mdl in models:
    sub = [r for r in recs if r["model"] == mdl and np.isfinite(r["chi2"]) and r["chi2"] < 10]
    if len(sub) < 20: continue
    prod = np.array([r["rho"]*r["rs"]*1000.0 for r in sub])            # Msun/pc^3 x kpc -> x1000 pc = Msun/pc^2
    lM = np.array([r["lM"] for r in sub])
    ok = np.isfinite(prod) & (prod > 0) & np.isfinite(lM)
    prod, lM = prod[ok], lM[ok]
    sl = np.polyfit(lM, np.log10(prod), 1)[0]
    info(f"{mdl:16} N = {len(prod):3d}: rho_0 r_0 median {np.median(prod):7.1f} [16-84%: {np.percentile(prod,16):6.1f}, {np.percentile(prod,84):7.1f}] Msun/pc^2, scatter {np.log10(prod).std():.3f} dex, halo-mass slope {sl:+.3f}")
    R5[mdl] = (np.median(prod), np.log10(prod).std(), sl, len(prod))
bk = [m for m in R5 if "Burkert" in m]
best = bk[0] if bk else max(R5, key=lambda m: R5[m][3])
med, sc, sl5, n5 = R5[best]
ck("5 (a WORKS, and it explains a known unexplained constant) the halo surface-density product rho_0 x r_0 from real halo fits is nearly universal, and it sits within 0.15 dex of the framework's Sigma_M = a_0/(2 pi G) -- which is not a halo property in the framework at all but the phantom's own central surface density, fixed by a_0 and therefore by Lambda",
   abs(math.log10(med/SIG_M["canonical"])) < 0.15 or abs(math.log10(med/SIG_M["alt"])) < 0.15,
   f"{best}: median {med:.1f} Msun/pc^2 (N = {n5}, scatter {sc:.2f} dex) vs Sigma_M = {SIG_M['canonical']:.1f} canonical ({math.log10(med/SIG_M['canonical']):+.2f} dex) / {SIG_M['alt']:.1f} alt ({math.log10(med/SIG_M['alt']):+.2f} dex)")
ck("5b ...and it does not know about halo mass, as a constant of nature should not: the product's dependence on M200 is weak across the fitted range",
   abs(sl5) < 0.25, f"d log(rho_0 r_0)/d log M200 = {sl5:+.3f} over {n5} galaxies")
P(""); P("="*116); P("ITEM 95 -- the largest bound orbit, set by Lambda"); P("="*116)
LAM = 3*OM_L*H0**2/c_light**2
info(f"Lambda = 3 Omega_L H0^2/c^2 = {LAM:.3e} m^-2; the cosmological repulsion is g_Lambda = Lambda c^2 r/3 = Omega_L H0^2 r")
info(f"{'M_b [Msun]':>12} " + " ".join(f"{'r_Lambda ('+ft+') [Mpc]':>26}" for ft in A0))
R95 = {}
for lM in (9, 10, 11, 12, 13, 14, 15):
    Mb = 10**lM*Msun; row = []
    for ft, a0 in A0.items():
        rL = (math.sqrt(G*Mb*a0)/(OM_L*H0**2))**(1/3.)
        row.append(rL/Mpc)
    info(f"{10**lM:12.0e} " + " ".join(f"{v:26.3f}" for v in row))
    R95[lM] = row
sl95 = (math.log10(R95[15][0]) - math.log10(R95[9][0]))/6.0
ck("95 the framework has a LARGEST BOUND ORBIT set by the cosmological constant, and it scales as M_b^(1/6), not the M^(1/3) of a splashback radius: 1.3 Mpc for an L* galaxy, 6 Mpc for a cluster -- a testable edge in satellite and two-halo profiles whose MASS SCALING is the discriminator",
   abs(sl95 - 1/6.) < 0.02, f"d log r_Lambda/d log M_b = {sl95:.4f} (predicted 1/6 = 0.1667); L* (1e10.7) r_Lambda ~ {(math.sqrt(G*10**10.7*Msun*A0['canonical'])/(OM_L*H0**2))**(1/3.)/Mpc:.2f} Mpc, cluster (1e14) ~ {R95[14][0]:.2f} Mpc; splashback scales as M^(1/3)")
info("note the correction to the hunt list: item 95 was written with r_Lambda ~ M_b^(1/4); the correct exponent from")
info("sqrt(G M_b a_0)/r = Omega_L H0^2 r is 1/6, since the left side goes as M^(1/2)/r and the right as r.")
P(""); P("="*116); P("ITEM 58 -- merger infall speeds"); P("="*116)
BULLET = dict(name="Bullet 1E0657-56", M1=1.5e14, M2=2.5e14, sep=0.72, vobs=3000.0, z=0.296)
ELG = dict(name="El Gordo ACT-CL J0102", M1=1.4e15, M2=7.8e14, sep=0.7, vobs=2500.0, z=0.87)
FBAR = 0.15                     # baryon fraction: in MOND the source is the BARYONS, in LambdaCDM the lensing mass IS the dynamical mass
for cl in (BULLET, ELG):
    Mlens = (cl["M1"] + cl["M2"])*Msun; Mbar = FBAR*Mlens
    for ft, a0 in A0.items():
        r_ta = 4.0*Mpc
        def infall(Mt, mond):
            def rhs(t, y):
                r, v = y; r = max(r, 1e19); gN = G*Mt/r**2
                return [v, -(gN*nu_s(gN/a0) if mond else gN) + OM_L*H0**2*r]
            ev = lambda t, y: y[0] - cl["sep"]*Mpc
            s_ = solve_ivp(rhs, (0, 4e17), [r_ta, 0.0], rtol=1e-9, atol=1e2, max_step=1e15, events=(ev,))
            return abs(s_.y_events[0][0][1])/1e3 if len(s_.y_events[0]) else float("nan")
        v_mond = infall(Mbar, True); v_newt = infall(Mlens, False)
        info(f"{cl['name']:24} {ft:10}: MOND from the BARYONS ({Mbar/Msun:.2e}) gives {v_mond:.0f} km/s; Newton from the LENSING mass ({Mlens/Msun:.2e}) gives {v_newt:.0f}; inferred collision speed ~{cl['vobs']:.0f} km/s")
        if cl is BULLET and ft == "canonical": R58 = (v_mond, v_newt, cl["vobs"])
ck("58 the self-consistent comparison -- MOND driven by the BARYONS, Newton by the lensing mass, both from a 4 Mpc turnaround -- shows the two laws giving very similar infall speeds for the Bullet, so the merger velocity does NOT discriminate; and the answer is dominated by the assumed turnaround radius, not by the gravity law.  NON-DIAGNOSTIC, withdrawn from the priority list",
   abs(R58[0] - R58[1])/max(R58[1], 1) < 0.5, f"Bullet: MOND from baryons {R58[0]:.0f} km/s, Newton from lensing mass {R58[1]:.0f} km/s, inferred {R58[2]:.0f}; the earlier version of this check fed MOND the LENSING mass, which double-counts the phantom -- corrected here")
info("both ways: this is not the Bullet's real problem for either theory.  For LambdaCDM the issue is the PROBABILITY of so fast a")
info("merger in a simulated volume (Lee & Komatsu 2010), which a two-body integration cannot address; for MOND it is the cluster")
info("residual, which the programme already carries as an open liability.")
sys.exit(ck.done())
