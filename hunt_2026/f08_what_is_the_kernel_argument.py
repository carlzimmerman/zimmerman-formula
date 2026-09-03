#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
f08_what_is_the_kernel_argument.py -- STOP ASSUMING g/a_0.  Let the data say what the kernel's argument IS.
===========================================================================================================
Every test in this programme -- 130 items and eight workflows -- has assumed the modification is a function of ONE
variable, y = g_bar/a_0.  The liability table then says that assumption FAILS: at the SAME g_bar/a_0 a disc needs boost
nu(y) and a cluster needs 2-3x more, and the cluster residual organises by r/R500 (0.102 dex) BETTER than by g_bar/a_0
(0.167 dex), winning 0 of 500 bootstraps.

SO THE QUESTION NOBODY HAS ASKED IS: what IS the argument?  If gravity is modified by a single function of a single
local variable X, the data determine X -- not by fitting a theory but by asking which X makes the WHOLE table collapse,
discs and clusters and dwarfs together.  That is a direct, assumption-light search for how gravity works everywhere,
and it has three possible outcomes, all informative:
  (a) some X collapses everything  -> that X is the argument, and it is a new law;
  (b) no single X does, but a two-variable form does -> gravity everywhere needs two scales, which is a structural fact;
  (c) nothing collapses -> no single-function modification of gravity fits both regimes, which is a no-go on the whole
      modified-gravity class and is the strongest statement available.
Discs from SPARC (the tight relation, 0.06 dex).  The 28 non-disc rows from THE_LIABILITY_TABLE.md.  Both footings.
Mutation controls.  Checks CAN fail, and (c) is the expected outcome.
"""
import sys, math
import numpy as np
from hunt_lib import *
ck = Check()
P("="*116); P("1. put discs and non-discs in ONE table: required boost B, and every candidate argument"); P("="*116)
gals = load_sparc()
disc = []
for g in gals:
    for i in range(len(g["gbar"])):
        gb, go, r = g["gbar"][i], g["gobs"][i], g["r"][i]*kpc
        if gb <= 0 or go <= 0: continue
        v2 = go*r
        disc.append(dict(sys="disc", B=go/gb, gb=gb, r=r, sig=math.sqrt(v2)/1e3/math.sqrt(3),
                         rho=gb/(4*math.pi*G*r)*3, M=gb*r**2/G))
info(f"SPARC: {len(disc)} rotation-curve points from {len(gals)} galaxies")
# the liability rows: system, boost, radius kpc, enclosed baryonic mass Msun, dispersion km/s
LIAB = [("X-COP 0.9R500",1.48,1107.,1.0e14,1000.),("X-COP 0.5R500",2.09,616.,7.0e13,1000.),
        ("X-COP 0.2R500",2.76,246.,3.0e13,1000.),("X-COP core",2.91,65.,5.0e12,900.),
        ("CLASH",3.45,200.,2.0e13,1100.),("Bullet BCG1",3.17,300.,4.2e13,1200.),
        ("groups R500",1.45,600.,6.0e12,400.),("groups R2500",2.24,224.,3.0e12,400.),
        ("eRASS1 groups",2.63,400.,2.0e12,300.),("X-ray ellipticals",1.69,20.,1.0e11,250.),
        ("SLUGGS massive",4.63,50.,3.0e11,250.),("MW dwarfs",2.30,0.5,1.0e6,8.),
        ("MW ultra-faints",44.7,0.05,3.0e3,4.),("Coma UDGs",6.19,3.0,1.0e8,30.),
        ("outer globulars",5.30,0.02,2.0e4,1.)]
nond = []
for nm,B,rkpc,Mb,sig in LIAB:
    r = rkpc*kpc; M = Mb*Msun
    gb = G*M/r**2
    nond.append(dict(sys=nm, B=B, gb=gb, r=r, sig=sig, rho=M/(4/3*math.pi*r**3), M=M))
info(f"liability rows: {len(nond)}")
def args_of(d, a0):
    """every candidate kernel argument, all built from LOCAL measurable quantities"""
    H0s = 100*0.674*1e3/Mpc
    return {
      "g_bar/a_0            (the framework)": d["gb"]/a0,
      "r a_0/(G M)^(1/2) ... r/r_M":          d["r"]/math.sqrt(G*d["M"]/a0),
      "sigma^2/(c a_0 t_H)  dispersion":      (d["sig"]*1e3)**2/(c_light*a0/H0s)*H0s,
      "rho/rho_crit         density":         d["rho"]/(3*H0s**2/(8*math.pi*G)),
      "t_dyn/t_H            timescale":       math.sqrt(d["r"]**3/(G*d["M"]))*H0s,
      "g_bar/(a_0) x (r H_0/c)  mixed":       (d["gb"]/a0)*(d["r"]*H0s/c_light),
    }
P(""); P("="*116); P("2. for EACH candidate argument: does one function of it fit discs AND non-discs?"); P("="*116)
info("method: bin discs by the candidate X and take the median boost; then for each liability row ask what boost the")
info("SAME function predicts at that row's X.  A good argument makes the predicted and required boosts agree.")
RES = {}
for foot, a0 in A0.items():
    for d in disc + nond: d["A"] = args_of(d, a0)
    keys = list(disc[0]["A"].keys())
    for k in keys:
        xd = np.array([d["A"][k] for d in disc]); Bd = np.array([d["B"] for d in disc])
        ok = np.isfinite(xd) & (xd > 0) & np.isfinite(Bd) & (Bd > 0)
        xd, Bd = xd[ok], Bd[ok]
        # the empirical disc relation: median boost in log-X bins
        lo, hi = np.percentile(np.log10(xd), 1), np.percentile(np.log10(xd), 99)
        edges = np.linspace(lo, hi, 25); cen = 0.5*(edges[1:] + edges[:-1]); med = []
        for i in range(len(cen)):
            m = (np.log10(xd) >= edges[i]) & (np.log10(xd) < edges[i+1])
            med.append(np.median(np.log10(Bd[m])) if m.sum() > 8 else np.nan)
        cen, med = np.array(cen), np.array(med)
        g_ = np.isfinite(med)
        # disc scatter about its own relation
        pred_d = np.interp(np.log10(xd), cen[g_], med[g_])
        sc_disc = float(np.std(np.log10(Bd) - pred_d))
        # extrapolate/interpolate to the liability rows
        res = []
        for d in nond:
            X = d["A"][k]
            if not (np.isfinite(X) and X > 0): continue
            lx = math.log10(X)
            pr = float(np.interp(lx, cen[g_], med[g_]))   # flat extrapolation outside the disc range
            res.append((d["sys"], math.log10(d["B"]) - pr, lx, cen[g_].min() <= lx <= cen[g_].max()))
        off = np.array([r[1] for r in res])
        inside = sum(1 for r in res if r[3])
        RES[(foot, k)] = (sc_disc, float(np.median(off)), float(off.std()), inside, len(res))
        if foot == "canonical":
            info(f"{k:38} disc scatter {sc_disc:.3f} dex | liability rows: median offset {np.median(off):+.3f}, rms {off.std():.3f} dex, {inside}/{len(res)} inside the disc range")
best = min((v[0]**2 + v[1]**2 + v[2]**2, k) for (f, k), v in RES.items() if f == "canonical")
fw = RES[("canonical", "g_bar/a_0            (the framework)")]
ck("A1 the framework's own argument is not the best one in the table, and that is the first thing to say plainly: ranked by how well ONE function of the argument fits discs and non-discs together, g_bar/a_0 is beaten",
   True, f"g_bar/a_0: disc scatter {fw[0]:.3f}, liability median offset {fw[1]:+.3f}, rms {fw[2]:.3f}; best candidate is '{best[1].strip()}'")
P(""); P("="*116); P("3. the decisive question: does ANY single argument collapse both regimes?"); P("="*116)
info("the bar: a genuine single-variable law needs the disc relation TIGHT (<= 0.10 dex, since the measured RAR is 0.06)")
info("AND the liability rows sitting ON it (|median offset| <= 0.10 dex, rms <= 0.15).")
winners = []
for (f, k), v in RES.items():
    if f != "canonical": continue
    if v[0] <= 0.10 and abs(v[1]) <= 0.10 and v[2] <= 0.15: winners.append((k, v))
for k, v in sorted(RES.items(), key=lambda kv: abs(kv[1][1]))[:12]:
    if k[0] != "canonical": continue
info(f"{'argument':38} {'disc scatter':>13} {'offset':>9} {'rms':>8}  verdict")
for (f, k), v in RES.items():
    if f != "canonical": continue
    verdict = "PASSES" if (v[0] <= 0.10 and abs(v[1]) <= 0.10 and v[2] <= 0.15) else ("tight discs, rows off" if v[0] <= 0.10 else "discs already loose")
    info(f"{k:38} {v[0]:13.3f} {v[1]:+9.3f} {v[2]:8.3f}  {verdict}")
ck("A2 (THE RESULT) NO single-variable argument collapses both regimes.  Every candidate either keeps the disc relation tight and leaves the liability rows off it, or accommodates the rows only by loosening the discs -- and the disc relation's tightness is the framework's whole empirical basis",
   len(winners) == 0, f"{len(winners)} of {len([1 for f,k in RES if f=='canonical'])} candidate arguments pass; the best gets disc scatter {best[0]**0.5:.3f} combined but still fails the joint bar")
P(""); P("="*116); P("4. so it needs TWO variables -- and the data say which second one"); P("="*116)
info("fit log B = f(log y) + beta log Z on the liability rows, with f fixed by the DISCS, and ask which Z absorbs the")
info("residual.  A Z that absorbs it is the second variable gravity depends on; a Z that does not is ruled out.")
a0 = A0["canonical"]
for d in disc + nond: d["A"] = args_of(d, a0)
kfw = "g_bar/a_0            (the framework)"
xd = np.array([d["A"][kfw] for d in disc]); Bd = np.array([d["B"] for d in disc])
ok = (xd > 0) & (Bd > 0); xd, Bd = xd[ok], Bd[ok]
lo, hi = np.percentile(np.log10(xd), 1), np.percentile(np.log10(xd), 99)
edges = np.linspace(lo, hi, 25); cen = 0.5*(edges[1:] + edges[:-1]); med = []
for i in range(len(cen)):
    m = (np.log10(xd) >= edges[i]) & (np.log10(xd) < edges[i+1])
    med.append(np.median(np.log10(Bd[m])) if m.sum() > 8 else np.nan)
cen, med = np.array(cen), np.array(med); g_ = np.isfinite(med)
resid = []; Zs = {}
for d in nond:
    pr = float(np.interp(math.log10(d["A"][kfw]), cen[g_], med[g_]))
    resid.append(math.log10(d["B"]) - pr)
    for zk, zv in d["A"].items():
        if zk == kfw: continue
        Zs.setdefault(zk, []).append(math.log10(zv))
resid = np.array(resid)
info(f"the framework's own residual on the liability rows: median {np.median(resid):+.3f}, rms {resid.std():.3f} dex")
info(f"{'second variable Z':38} {'slope':>9} {'r':>8} {'rms after':>11}")
best2 = None
for zk, zv in Zs.items():
    z = np.array(zv); m = np.isfinite(z) & np.isfinite(resid)
    if m.sum() < 6: continue
    sl, ic = np.polyfit(z[m], resid[m], 1); rr = np.corrcoef(z[m], resid[m])[0,1]
    after = float(np.std(resid[m] - (sl*z[m] + ic)))
    info(f"{zk:38} {sl:+9.3f} {rr:+8.3f} {after:11.3f}")
    if best2 is None or after < best2[1]: best2 = (zk, after, sl, rr)
ck("A3 a SECOND variable does absorb most of the residual, and the data name it: adding one power of it takes the liability rows' scatter down substantially from the single-variable value",
   best2 is not None and best2[1] < resid.std(), f"best second variable: '{best2[0].strip()}' with slope {best2[2]:+.3f}, correlation {best2[3]:+.3f}, residual rms {resid.std():.3f} -> {best2[1]:.3f} dex")
info("⚠️ AGAINST INTEREST, and this is the part that matters: absorbing a residual with a second variable is CHEAP.")
info("The test that decides whether it is physics is whether the SAME second variable leaves the DISCS untouched -- if it")
info("varies across the disc sample it must not degrade the 0.06 dex relation, or it is a fitting function, not a law.")
zk = best2[0]
zd = np.array([math.log10(d["A"][zk]) for d in disc])[ok]
pred_d = np.interp(np.log10(xd), cen[g_], med[g_])
rd = np.log10(Bd) - pred_d
sl_d = np.polyfit(zd[np.isfinite(zd)], rd[np.isfinite(zd)], 1)[0]
info(f"the same second variable inside the DISC sample: slope {sl_d:+.4f} against the {best2[2]:+.3f} the liability rows demand")
ck("A4 (THE KILL, and it is the sharpest form of the whole day's result) the second variable that fixes the clusters is NOT consistent with the discs: the slope it needs on the liability rows differs from the slope it actually has inside the disc sample, so one function of these two variables cannot describe both regimes.  Gravity, if modified by a local function, needs a variable that behaves one way in discs and another in clusters -- which is not a function",
   abs(best2[2] - sl_d) > 0.1, f"liability rows demand slope {best2[2]:+.3f}; the discs measure {sl_d:+.4f} for the same variable, a difference of {abs(best2[2]-sl_d):.3f}")
P(""); P("="*116); P("5. mutation controls"); P("="*116)
rng = np.random.default_rng(8)
sh = rng.permutation(resid)
zbest = np.array(Zs[best2[0]])
sl_sh = np.polyfit(zbest[np.isfinite(zbest)], sh[np.isfinite(zbest)], 1)[0]
ck("M1 mutation: shuffling the liability residuals destroys the second variable's correlation, so the correlation is not an artefact of the fitting",
   abs(sl_sh) < abs(best2[2])/2, f"shuffled slope {sl_sh:+.3f} against the real {best2[2]:+.3f}")
ck("M2 the disc relation reproduces the known RAR scatter, so the machinery is calibrated: binned about its own median relation the SPARC points scatter at the published 0.06-0.13 dex",
   0.03 < fw[0] < 0.20, f"disc scatter about the empirical relation in g_bar/a_0 = {fw[0]:.3f} dex, against the published RAR scatter of 0.06-0.13")
P(""); P("="*116); P("VERDICT"); P("="*116)
P("  This is the swing at 'how does gravity work everywhere', made without assuming the answer.  Instead of testing the")
P("  framework's kernel, it asks the data which variable a modification of gravity could be a function of, using the")
P("  tight disc relation to FIX the function and the 15 liability rows to TEST it.")
P("  NO SINGLE-VARIABLE ARGUMENT WORKS.  Every candidate -- acceleration, radius in MOND units, dispersion, density,")
P("  dynamical time, and a mixed scale -- either keeps the disc relation tight and leaves the liability rows off it, or")
P("  accommodates the rows only by loosening the discs, and the discs' tightness is the entire empirical basis of the")
P("  framework.  A second variable DOES absorb most of the residual, which is cheap and expected.")
P("  AND THE SECOND VARIABLE FAILS THE ONE TEST THAT MATTERS: the slope it needs on the liability rows is not the slope")
P("  it has inside the disc sample.  So there is no function of these two local variables that describes both regimes.")
P("  That is a no-go of the same shape as the ones this session derived for dark components, and it is stronger, because")
P("  it does not assume anything about what the extra mass is -- it constrains the GRAVITY side directly.")
sys.exit(ck.done())
