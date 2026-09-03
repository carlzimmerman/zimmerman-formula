#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""u12_extra_variable_modifications.py -- CLASS (b): modifications that add a NEW VARIABLE beside y.

u11 closed the class of modifications that are functions of y alone.  The obvious next move is to let the
boost depend on something else as well -- a potential depth, a length scale, a surface density, a mass, the
external field, or what kind of object it is.  This script tests that class.

TWO STRUCTURAL FACTS ARE ESTABLISHED FIRST, because they collapse most of the candidate list:

  (i)  THE MEAN ENCLOSED SURFACE DENSITY IS NOT A NEW VARIABLE.  For a spherical enclosed mass,
           Sigma_enc = M/(pi r^2) = g_bar/(pi G)
       exactly -- it is g_bar in different units.  So a Sigma-dependent modification IS a y-dependent one
       and is already excluded by u11.  Verified numerically as check 0c.

  (ii) EVERY OTHER ENCLOSED-QUANTITY VARIABLE IS A FUNCTION OF (g_bar, r).
           M = g_bar r^2/G,   Phi = GM/r = g_bar r,   rho_bar = 3 g_bar/(4 pi G r)
       and the map (g_bar, r) -> (Phi, rho_bar) is invertible.  So the whole space of "local enclosed-quantity"
       modifications is exactly the space of functions f(y, r), and it can be tested in one shot.

The decisive test of f(y, r) is not a fit.  It is a COLLISION: find liability systems that sit at the same
(y, r) as SPARC rotation-curve points, which need zero.  A tidal dwarf galaxy at y = 0.038 and r = 4.8 kpc is
at the same place in (y, r) as ordinary SPARC dwarf discs, and needs -0.68 dex.

WHAT IS COMPUTED
  0  the two structural facts, verified numerically
  1  the single-variable organiser search over 10 candidates, with a look-elsewhere correction
  2  the (y, r) COLLISION TEST against SPARC -- the no-go for the whole local class
  3  the attempts, each fitted then handed to the keeper battery:
       B1  the framework's OWN first law generalised: a_0 = (c/2) sqrt(G (rho_Lambda + xi rho_bar))
       B2  a potential-depth modification: a_0 -> a_0 [1 + (Phi/Phi_c)^q]^s
       B3  a fixed LENGTH scale: nu -> nu [1 + A/(1 + (l/r)^2)]
       B4  a support-type boost (pressure-supported systems get x(1+A))
       B5  the structural classification u01 found: bound star cluster / galaxy / DM-deficient galaxy
       B6  a_0 proportional to H(z) -- the one modification aimed at the evolution liability alone
  4  mutation controls, both footings, the LambdaCDM alternative beside
"""
import os, sys, math, json
import numpy as np
from scipy.optimize import minimize_scalar, minimize
from scipy.stats import spearmanr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *
from u10_ledger import ledger, dedup, Keepers, KEEPER_TOL, keeper_verdict, nu_routeA

ck = Check(); rng = np.random.default_rng(12)
c_l = c_light
RHO_L = OM_L*rho_crit                    # the framework's own rho_Lambda, from Planck via hunt_lib
OUT = {}

P("="*118)
P("u12 -- MODIFICATIONS THAT ADD A NEW VARIABLE BESIDE y")
P("="*118)

K = {f: Keepers(f) for f in ("canonical", "alt")}
BASE = {f: K[f].all(nu_routeA) for f in K}
L = {f: ledger(f, "iso") for f in ("canonical", "alt")}
rows = sorted(L["canonical"], key=lambda r: r["y"])
b = BASE["canonical"]

# ==================================================================================================== 0
P("\n" + "-"*118)
P("(0) TWO STRUCTURAL FACTS THAT COLLAPSE THE CANDIDATE LIST")
P("-"*118)
info(f"the framework's own dark-energy density, from Planck via hunt_lib:  rho_Lambda = {RHO_L:.4e} kg/m^3")
a0_from_rho = 0.5*c_l*math.sqrt(G*RHO_L)
ck("0a the first law reproduces the canonical footing from rho_Lambda with kappa = 1/2",
   abs(math.log10(a0_from_rho/A0["canonical"])) < 0.05,
   f"(c/2) sqrt(G rho_Lambda) = {a0_from_rho:.3e} vs canonical {A0['canonical']:.3e} ({math.log10(a0_from_rho/A0['canonical']):+.3f} dex)")

sig = np.array([r["Sigma"] for r in rows]); gb = np.array([r["g_bar"] for r in rows])
ck("0b Sigma_enc = g_bar/(pi G) EXACTLY -- the mean enclosed surface density is g_bar in other units, so a "
   "surface-density modification is a kernel modification and is already excluded by u11",
   float(np.max(np.abs(sig/(gb/(math.pi*G)) - 1.0))) < 1e-12,
   f"max |Sigma pi G/g_bar - 1| = {float(np.max(np.abs(sig/(gb/(math.pi*G)) - 1.0))):.2e} over the 37 rows")

# invertibility of (g_bar, r) -> (Phi, rho_bar)
Phi = np.array([r["Phi"] for r in rows]); rho = np.array([r["rho_bar"] for r in rows])
r_m = np.array([r["r"] for r in rows])
r_rec = np.sqrt(3*Phi/(4*math.pi*G*rho)); g_rec = Phi/r_rec
ck("0c every enclosed-quantity variable (M, Phi, Sigma, rho_bar) is a function of (g_bar, r) and the map is "
   "invertible, so the entire local class is the class of functions f(y, r)",
   float(np.max(np.abs(r_rec/r_m - 1))) < 1e-10 and float(np.max(np.abs(g_rec/gb - 1))) < 1e-10,
   f"max relative reconstruction error {max(float(np.max(np.abs(r_rec/r_m-1))), float(np.max(np.abs(g_rec/gb-1)))):.2e}")

# ==================================================================================================== 1
P("\n" + "-"*118)
P("(1) THE SINGLE-VARIABLE ORGANISER SEARCH -- which variable, if any, organises the 37 liabilities?")
P("-"*118)
Bv = np.array([r["B"] for r in rows])
CAND = {
    "log y  (the framework's own)": np.log10([r["y"] for r in rows]),
    "log r [kpc]":                  np.log10([r["r_kpc"] for r in rows]),
    "log M_enc [Msun]":             np.log10([r["M_enc_msun"] for r in rows]),
    "log Phi = G M/r":              np.log10([r["Phi"] for r in rows]),
    "log Sigma_enc":                np.log10([r["Sigma"] for r in rows]),
    "log rho_bar (enclosed)":       np.log10([r["rho_bar"] for r in rows]),
    "log (1 + x_ext/y)":            np.log10([1 + r["x_ext"]/r["y"] for r in rows]),
    "x_ext (external field)":       np.array([r["x_ext"] for r in rows]),
    "support: pressure/lensing=1":  np.array([0.0 if r["support"] == "rotation" else 1.0 for r in rows]),
    "class: cluster=1":             np.array([1.0 if r["cls"] == "cluster" else 0.0 for r in rows]),
    "structural: star cluster=1":   np.array([1.0 if r["name"] in ("pal3", "pal4", "pal14", "ngc2419") else 0.0 for r in rows]),
    "structural: LCDM says DM-rich": np.array([0.0 if r["name"] in ("pal3", "pal4", "pal14", "ngc2419",
                                                                   "ngc1052_df2", "ngc1052_df4", "tidal_dwarfs")
                                               else 1.0 for r in rows]),
}
# BUG PATTERN 5, checked and not assumed.  B and every variable built from g_bar share g_bar, so a common
# baryon-budget error delta = d log g_bar drives the rows along a fixed slope in each plane:
#     d B/d delta = -(1 + n),   n = dln nu/dln y      and     d X/d delta = +1 for X built from g_bar, 0 for r
# The degeneracy slope is therefore -(1+n) for y, Sigma, M, Phi and rho_bar, and ZERO for radius and for the
# categorical variables.  A measured slope that lands on the degeneracy slope is not evidence of a law.
n_med = float(np.median([(math.log(nu_s(r["y"]*1.001)) - math.log(nu_s(r["y"]*0.999)))/0.002 for r in rows]))
DEGEN = {"log y  (the framework's own)": -(1 + n_med), "log Sigma_enc": -(1 + n_med),
         "log M_enc [Msun]": -(1 + n_med), "log Phi = G M/r": -(1 + n_med),
         "log rho_bar (enclosed)": -(1 + n_med)}
info(f"the ledger's median kernel log-slope is n = {n_med:+.3f}, so a shared baryon-budget error moves rows along "
     f"a slope of {-(1+n_med):+.3f} in every plane whose X is built from g_bar, and along 0 in the radius plane")

P(f"  {'candidate variable':34s} {'slope':>8s} {'degen':>7s} {'rho(B)':>8s} {'p_perm':>8s} {'rho(|B|)':>9s} {'p_perm':>8s} {'resid':>7s}")
best = None; RES = {}
for nm, x in CAND.items():
    rs_ = float(spearmanr(x, Bv).statistic); ra_ = float(spearmanr(x, np.abs(Bv)).statistic)
    ps = float(np.mean([abs(spearmanr(x, rng.permutation(Bv)).statistic) >= abs(rs_) for _ in range(4000)]))
    pa = float(np.mean([abs(spearmanr(x, rng.permutation(np.abs(Bv))).statistic) >= abs(ra_) for _ in range(4000)]))
    A = np.vstack([x, np.ones_like(x)]).T
    coef = np.linalg.lstsq(A, Bv, rcond=None)[0]
    res = float(np.sqrt(np.mean((Bv - A @ coef)**2)))
    dg = DEGEN.get(nm, 0.0)
    flag = "  <-- consistent with the shared-g_bar degeneracy, not evidence of a law" if (nm in DEGEN and abs(coef[0]-dg) < 0.35) else ""
    RES[nm] = dict(rho_signed=rs_, p_signed=ps, rho_abs=ra_, p_abs=pa, resid=res, slope=float(coef[0]), degen=dg)
    P(f"  {nm:34s} {coef[0]:+8.3f} {dg:+7.3f} {rs_:+8.3f} {ps:8.4f} {ra_:+9.3f} {pa:8.4f} {res:7.3f}{flag}")
    if best is None or res < best[1]: best = (nm, res)
raw = float(np.sqrt(np.mean(Bv**2)))
nlook = len(CAND)

# the organisers that survive BOTH the look-elsewhere correction and the degeneracy check
surv = [nm for nm, v in RES.items()
        if v["p_signed"]*nlook < 0.05 and not (nm in DEGEN and abs(v["slope"] - DEGEN[nm]) < 0.35)]
info(f"raw ledger rms {raw:.3f} dex; best single variable '{best[0]}' at {best[1]:.3f} dex "
     f"({100*(1-best[1]/raw):.0f}% of the variance removed)")
info(f"variables that organise the SIGNED residual at a look-elsewhere-corrected p < 0.05 AND are not explained by "
     f"the shared-g_bar degeneracy: {len(surv)} of {nlook} -- " + ", ".join(f"'{x}'" for x in surv))
ck("1a AGAINST THE FRAMEWORK AND AGAINST THE HYPOTHESIS THIS SECTION WAS WRITTEN TO TEST.  The first version of this "
   "check asserted that NO variable organises the signed liability; it FAILED and is replaced by what the data say.  "
   "Several do -- and every one of them is either a proxy for what kind of object it is, or a radius, and none of them "
   "is the framework's own acceleration",
   len(surv) >= 1 and "log y  (the framework's own)" not in surv,
   f"{len(surv)} surviving organisers, none of them log y (log y: rho = {RES['log y  (the framework\'s own)']['rho_signed']:+.3f}, "
   f"p = {RES['log y  (the framework\'s own)']['p_signed']:.3f})")
sup = RES["support: pressure/lensing=1"]
lcd = RES["structural: LCDM says DM-rich"]
rr_ = RES["log r [kpc]"]; rb_ = RES["log rho_bar (enclosed)"]
info(f"THE STRONGEST ORGANISER IN THE TABLE is not a gravitational variable: 'does LambdaCDM give this object a dark "
     f"halo' -- rho = {lcd['rho_signed']:+.3f}, p = {lcd['p_signed']:.4f}, residual {lcd['resid']:.3f} dex from {raw:.3f}, "
     f"i.e. {100*(1-lcd['resid']/raw):.0f}% of the variance removed by ONE binary label.  It replicates the p = 0.0024 "
     f"split u01 found on the pressure-supported block alone, on the full 37-row table.")
info(f"the strongest GRAVITATIONAL organiser is the RADIUS, slope {rr_['slope']:+.3f} dex per dex, rho = {rr_['rho_signed']:+.3f}, "
     f"p = {rr_['p_signed']:.4f} -- and radius is the one variable in the list immune to the shared-g_bar degeneracy, "
     f"so it is not an artefact of the baryon budget.  It is tested as an explicit modification below (B3b).")
info(f"the mean enclosed baryon density looks like a strong organiser (rho = {rb_['rho_signed']:+.3f}) but its measured "
     f"slope {rb_['slope']:+.3f} sits {abs(rb_['slope']-DEGEN['log rho_bar (enclosed)']):.2f} from the "
     f"{DEGEN['log rho_bar (enclosed)']:+.3f} a shared baryon-budget error produces by itself -- bug pattern 5, and it is "
     f"why B1 below is tested by its keeper damage and not by its ledger fit.")
info(f"support type on its own is NOT significant on the full table (rho = {sup['rho_signed']:+.3f}, p = {sup['p_signed']:.3f}); "
     f"the pattern u01 saw in the disc/lensing block does not survive the addition of the cluster and pressure blocks.")

# two-variable: is (y, r) enough?
X2 = np.vstack([np.log10([r["y"] for r in rows]), np.log10([r["r_kpc"] for r in rows]), np.ones(len(rows))]).T
c2 = np.linalg.lstsq(X2, Bv, rcond=None)[0]
res2 = float(np.sqrt(np.mean((Bv - X2 @ c2)**2)))
X3 = np.vstack([np.log10([r["y"] for r in rows]), np.log10([r["r_kpc"] for r in rows]),
                np.array([0.0 if r["support"] == "rotation" else 1.0 for r in rows]), np.ones(len(rows))]).T
c3 = np.linalg.lstsq(X3, Bv, rcond=None)[0]
res3 = float(np.sqrt(np.mean((Bv - X3 @ c3)**2)))
info(f"a LINEAR function of (log y, log r) -- three parameters, the whole local class linearised -- leaves "
     f"{res2:.3f} dex of {raw:.3f}; adding support type as a fourth leaves {res3:.3f}")

# ==================================================================================================== 2
P("\n" + "-"*118)
P("(2) THE COLLISION TEST -- liability systems that sit where SPARC rotation-curve points sit")
P("-"*118)
gs = K["canonical"].gbar/A0["canonical"]
rs_kpc = np.concatenate([g["r"] for g in K["canonical"].gals])
gname = np.concatenate([[g["name"]]*len(g["r"]) for g in K["canonical"].gals])
res_sparc = np.log10(K["canonical"].gobs) - np.log10(nu_routeA(gs)*K["canonical"].gbar)
P(f"  {'liability system':22s} {'y':>8s} {'r_kpc':>8s} {'B':>7s} | {'SPARC pts within 0.2 dex in BOTH':>32s} {'their B':>10s} {'gap':>7s} {'sigma':>7s}")
COLL = []
for r in rows:
    m = (np.abs(np.log10(gs/r["y"])) < 0.2) & (np.abs(np.log10(rs_kpc/r["r_kpc"])) < 0.2)
    n = int(m.sum())
    if n < 20: continue
    bs = float(np.median(res_sparc[m])); sd = float(np.std(res_sparc[m]))
    gap = r["B"] - bs
    COLL.append((r, n, bs, sd, gap))
    P(f"  {r['name']:22s} {r['y']:8.4f} {r['r_kpc']:8.2f} {r['B']:+7.3f} | {n:32d} {bs:+10.3f} {gap:+7.3f} {abs(gap)/sd:7.1f}")
big = [c for c in COLL if abs(c[4]) > 0.3]
ck("2a THE LOCAL NO-GO -- there are liability systems occupying the SAME (y, r) cell as tens or hundreds of SPARC "
   "rotation-curve points, needing corrections that differ from SPARC's by far more than SPARC's own scatter.  "
   "Since every enclosed-quantity variable is a function of (y, r) (check 0c), NO local modification of that kind can serve both",
   len(big) >= 1, "; ".join(f"{c[0]['name']}: {c[4]:+.3f} dex from {c[1]} SPARC points at the same (y, r), {abs(c[4])/c[3]:.1f} sigma"
                            for c in big))
for c in big:
    r, n, bs, sd, gap = c
    info(f"{r['name']} sits at y = {r['y']:.4f}, r = {r['r_kpc']:.2f} kpc with {n} SPARC points in the same cell "
         f"(from {len(set(gname[(np.abs(np.log10(gs/r['y']))<0.2)&(np.abs(np.log10(rs_kpc/r['r_kpc']))<0.2)]))} galaxies).  "
         f"It needs {r['B']:+.3f} dex; they need {bs:+.3f} +- {sd:.3f}.")
OUT["collisions"] = [dict(name=c[0]["name"], n=c[1], sparc_B=c[2], sparc_sd=c[3], gap=c[4]) for c in COLL]

# ==================================================================================================== 3
P("\n" + "-"*118)
P("(3) THE ATTEMPTS")
P("-"*118)


def apply_gpred(rowset, gp):
    out = []
    for r in rowset:
        pred = float(np.asarray(gp(np.array([r["g_bar"]]), np.array([r["r"]])), float).ravel()[0])
        out.append(math.log10(r["g_obs"]/pred))
    return np.array(out)


def run(tag, name, gp, npar, rowset, footing, note=""):
    rms0 = float(np.sqrt(np.mean([r["B"]**2 for r in rowset])))
    Bn = apply_gpred(rowset, gp); rms1 = float(np.sqrt(np.mean(Bn**2)))
    kk = K[footing].all_g(gp); brk = keeper_verdict(BASE[footing], kk)
    fixed = sum(1 for r, bn in zip(rowset, Bn) if abs(bn) < abs(r["B"]) - 0.05)
    worse = sum(1 for r, bn in zip(rowset, Bn) if abs(bn) > abs(r["B"]) + 0.05)
    P(f"\n  [{tag}] {name}   ({npar} free parameter{'s' if npar != 1 else ''}, {footing} footing){('  ' + note) if note else ''}")
    P(f"        ledger rms  {rms0:.3f} -> {rms1:.3f} dex   median |B| {float(np.median([abs(r['B']) for r in rowset])):.3f} -> "
      f"{float(np.median(np.abs(Bn))):.3f}   improved {fixed}/{len(rowset)}, worse {worse}/{len(rowset)}")
    P(f"        keepers: " + ("NONE BROKEN" if not brk else f"{len(brk)} BROKEN"))
    for x in brk: P(f"           - {x}")
    if not brk:
        P(f"           (rar_rms {BASE[footing]['rar_rms']:.4f}->{kk['rar_rms']:.4f}, renzo {BASE[footing]['renzo_beta']:.3f}->{kk['renzo_beta']:.3f}, "
          f"lens {BASE[footing]['lens_slope']:.3f}->{kk['lens_slope']:.3f}, tail {BASE[footing]['tail_slope']:.3f}->{kk['tail_slope']:.3f})")
    return dict(tag=tag, name=name, npar=npar, footing=footing, rms0=rms0, rms1=rms1,
                improved=fixed, worsened=worse, keepers_broken=brk)


ATT = []
for foot in ("canonical", "alt"):
    a0 = A0[foot]; rs_ = L[foot]

    # ---- B1 the framework's own first law, generalised: a_0 = (c/2) sqrt(G (rho_L + xi rho_bar))
    def gp_B1(xi):
        def f(gbar, r):
            gbar = np.asarray(gbar, float); r = np.asarray(r, float)
            rho_b = 3*gbar/(4*math.pi*G*r)
            a0e = a0*np.sqrt(np.maximum(1.0 + xi*rho_b/RHO_L, 1e-8))
            return nu_routeA(gbar/a0e)*gbar
        return f
    def fB1(lx):
        xi = 10**lx
        return float(np.sqrt(np.mean(apply_gpred(rs_, gp_B1(xi))**2)))
    rB1 = minimize_scalar(fB1, bounds=(-12, 2), method="bounded")
    xi = 10**rB1.x
    rho_gal = np.median(3*K[foot].gbar/(4*math.pi*G*np.concatenate([g["r"] for g in K[foot].gals])*kpc))
    rho_cl = np.median([r["rho_bar"] for r in rs_ if r["cls"] == "cluster"])
    ATT.append(run("B1", f"the FIRST LAW GENERALISED: a_0 = (c/2) sqrt(G [rho_Lambda + xi rho_bar(<r)]), best xi = {xi:.3e}",
                   gp_B1(xi), 1, rs_, foot,
                   note=f"[median rho_bar/rho_Lambda: SPARC {rho_gal/RHO_L:.3e}, clusters {rho_cl/RHO_L:.3e} -- "
                        f"galaxies are {rho_gal/rho_cl:.0f}x DENSER, so this term acts on the keepers first]"))
    if foot == "canonical":
        P("        the fit ran to the LOWER BOUND, i.e. its answer is 'switch this term off'.  The scan that shows why,")
        P("        with the keeper damage beside it -- and the xi the cluster front alone would need:")
        rsc_ = [r for r in rs_ if r["cls"] == "cluster"]
        P(f"        {'xi':>10s} {'ledger rms':>11s} {'cluster rms':>12s} {'RAR rms':>9s} {'RAR med':>9s} {'BTFR slope':>11s} {'keepers broken':>15s}")
        for lx in (-8, -7, -6, -5, -4, -3):
            g_ = gp_B1(10.0**lx)
            kk_ = K[foot].all_g(g_); br_ = keeper_verdict(BASE[foot], kk_)
            P(f"        {10.0**lx:10.0e} {float(np.sqrt(np.mean(apply_gpred(rs_, g_)**2))):11.3f} "
              f"{float(np.sqrt(np.mean(apply_gpred(rsc_, g_)**2))):12.3f} {kk_['rar_rms']:9.4f} {kk_['rar_med']:+9.4f} "
              f"{kk_['btfr_slope']:11.3f} {len(br_):15d}")
        def fcl(lx): return float(np.sqrt(np.mean(apply_gpred(rsc_, gp_B1(10.0**lx))**2)))
        rcl = minimize_scalar(fcl, bounds=(-12, 2), method="bounded")
        kkc = K[foot].all_g(gp_B1(10.0**rcl.x)); brc = keeper_verdict(BASE[foot], kkc)
        P(f"        the CLUSTER ROWS ALONE prefer xi = {10.0**rcl.x:.2e} (cluster rms {float(np.sqrt(np.mean([r['B']**2 for r in rsc_]))):.3f} -> {rcl.fun:.3f}),")
        P(f"        and at that xi the keeper battery breaks {len(brc)} keepers: " + ("; ".join(x for x in brc) if brc else "none"))
        ck("3b the framework's own first law does not generalise to rho_Lambda + xi rho_bar: fitted to the whole ledger "
           "the best xi is ZERO (the optimiser runs to the boundary), and the xi the cluster front alone wants breaks "
           "the keepers, because SPARC galaxies are two orders of magnitude denser in baryons than cluster outskirts",
           xi < 1e-8 and len(brc) >= 1,
           f"whole-ledger best xi = {xi:.1e} (boundary); cluster-only xi = {10.0**rcl.x:.1e} breaks {len(brc)} keepers; "
           f"rho_bar(SPARC)/rho_bar(clusters) = {rho_gal/rho_cl:.0f}")

    # ---- B2 a potential-depth modification: a_0 -> a_0 [1 + (Phi/Phi_c)^q]
    def gp_B2(lPhic, q, s):
        Phic = 10**lPhic
        def f(gbar, r):
            gbar = np.asarray(gbar, float); r = np.asarray(r, float)
            Ph = gbar*r
            a0e = a0*(1.0 + (Ph/Phic)**q)**s
            return nu_routeA(gbar/a0e)*gbar
        return f
    def fB2(v):
        lPhic, q, s = v
        if not (6 <= lPhic <= 14 and 0.05 <= q <= 4 and -2 <= s <= 2): return 1e3
        return float(np.sqrt(np.mean(apply_gpred(rs_, gp_B2(lPhic, q, s))**2)))
    bB2 = min((minimize(fB2, [p0, q0, s0], method="Nelder-Mead", options=dict(maxiter=4000))
               for p0 in (8, 10, 12) for q0 in (0.3, 1.0, 2.0) for s0 in (-0.5, 0.5)), key=lambda z: z.fun)
    ATT.append(run("B2", f"a POTENTIAL-DEPTH modification: a_0 -> a_0 [1 + (Phi/Phi_c)^q]^s with "
                         f"Phi_c = {10**bB2.x[0]:.2e} m^2/s^2 (v_c = {math.sqrt(10**bB2.x[0])/1e3:.0f} km/s), q = {bB2.x[1]:.2f}, s = {bB2.x[2]:+.2f}",
                   gp_B2(*bB2.x), 3, rs_, foot))

    # ---- B3 a fixed LENGTH scale
    def gp_B3(A_, lell):
        ell = (10**lell)*kpc
        def f(gbar, r):
            gbar = np.asarray(gbar, float); r = np.asarray(r, float)
            return nu_routeA(gbar/a0)*gbar*(1.0 + A_/(1.0 + (ell/r)**2))
        return f
    def fB3(v):
        A_, lell = v
        if not (-0.95 <= A_ <= 20 and -2 <= lell <= 4.5): return 1e3
        return float(np.sqrt(np.mean(apply_gpred(rs_, gp_B3(A_, lell))**2)))
    bB3 = min((minimize(fB3, [a_, l_], method="Nelder-Mead", options=dict(maxiter=3000))
               for a_ in (0.3, 1.0, 3.0) for l_ in (0.0, 1.5, 2.5, 3.5)), key=lambda z: z.fun)
    ATT.append(run("B3", f"a FIXED LENGTH SCALE: nu -> nu [1 + A/(1 + (l/r)^2)] with A = {bB3.x[0]:.2f}, l = {10**bB3.x[1]:.1f} kpc",
                   gp_B3(*bB3.x), 2, rs_, foot))

    # ---- B3b the DIRECT implementation of section 1's surviving gravitational organiser: a power law in RADIUS
    def gp_B3b(m_, lC):
        C = 10**lC
        def f(gbar, r):
            gbar = np.asarray(gbar, float); r = np.asarray(r, float)
            return nu_routeA(gbar/a0)*gbar*C*(r/(10*kpc))**m_
        return f
    def fB3b(v):
        m_, lC = v
        if not (-1.5 <= m_ <= 1.5 and -1.5 <= lC <= 1.5): return 1e3
        return float(np.sqrt(np.mean(apply_gpred(rs_, gp_B3b(m_, lC))**2)))
    bB3b = min((minimize(fB3b, [m0, c0], method="Nelder-Mead", options=dict(maxiter=3000))
                for m0 in (-0.3, 0.0, 0.3) for c0 in (-0.3, 0.0, 0.3)), key=lambda z: z.fun)
    ATT.append(run("B3b", f"a RADIAL POWER LAW -- the direct implementation of the only gravitational organiser that "
                          f"survived section 1: g_pred = nu(y) g_bar x {10**bB3b.x[1]:.3f} (r/10 kpc)^{bB3b.x[0]:+.3f}",
                   gp_B3b(*bB3b.x), 2, rs_, foot,
                   note="[a rotation curve spans a decade in r inside ONE galaxy, so this is applied to the keepers too]"))

    # ---- B4 support-type boost (NOT a gravitational law; the empirical claim tested on its own terms)
    def gp_B4_factory(A_):
        # this one cannot be written as g_pred(g_bar, r): it needs to know what kind of system it is.
        # Evaluated on the ledger directly, and on the keepers by noting that SPARC is rotation-supported
        # (so A_ never acts there) -- which is exactly why it breaks no keeper and explains nothing.
        return A_
    def fB4(A_):
        Bn = []
        for r in rs_:
            f_ = (1.0 + A_) if r["support"] != "rotation" else 1.0
            Bn.append(r["B"] - math.log10(f_))
        return float(np.sqrt(np.mean(np.array(Bn)**2)))
    rB4 = minimize_scalar(fB4, bounds=(-0.9, 10), method="bounded")
    A4_ = rB4.x
    Bn4 = np.array([r["B"] - math.log10((1.0 + A4_) if r["support"] != "rotation" else 1.0) for r in rs_])
    rms0 = float(np.sqrt(np.mean([r["B"]**2 for r in rs_])))
    P(f"\n  [B4] a SUPPORT-TYPE boost: pressure-supported and lensed systems get x{1+A4_:.3f}, rotation-supported x1   "
      f"(1 free parameter, {foot} footing)")
    P(f"        ledger rms  {rms0:.3f} -> {float(np.sqrt(np.mean(Bn4**2))):.3f} dex   "
      f"improved {sum(1 for r, bn in zip(rs_, Bn4) if abs(bn) < abs(r['B'])-0.05)}/{len(rs_)}, "
      f"worse {sum(1 for r, bn in zip(rs_, Bn4) if abs(bn) > abs(r['B'])+0.05)}/{len(rs_)}")
    P( "        keepers: NONE BROKEN BY CONSTRUCTION -- SPARC, the BTFR, Renzo and the inner diversity are all")
    P( "        rotation-supported, so this modification is INVISIBLE to every keeper.  That is not a pass; it is")
    P( "        the statement that the modification is untestable where the framework's evidence lives.")
    P(f"        AND IT DOES NOT WORK ANYWAY: inside the pressure-supported block the residual after the boost is")
    pres = [(r, bn) for r, bn in zip(rs_, Bn4) if r["support"] != "rotation"]
    P(f"        {float(np.sqrt(np.mean([bn**2 for _, bn in pres]))):.3f} dex over {len(pres)} rows, spanning "
      f"{min(bn for _, bn in pres):+.3f} to {max(bn for _, bn in pres):+.3f} -- the sign split survives it.")
    ATT.append(dict(tag="B4", name="support-type boost", npar=1, footing=foot, rms0=rms0,
                    rms1=float(np.sqrt(np.mean(Bn4**2))), improved=int(sum(1 for r, bn in zip(rs_, Bn4) if abs(bn) < abs(r["B"])-0.05)),
                    worsened=int(sum(1 for r, bn in zip(rs_, Bn4) if abs(bn) > abs(r["B"])+0.05)),
                    keepers_broken=["(none, and that is the problem: no keeper is rotation-free, so this "
                                    "modification is invisible to all of them)"]))

    # ---- B5 the structural classification: star cluster / DM-deficient galaxy / halo galaxy
    def cls5(r):
        if r["name"] in ("pal3", "pal4", "pal14", "ngc2419"): return "star_cluster"
        if r["name"] in ("ngc1052_df2", "ngc1052_df4", "tidal_dwarfs"): return "dm_deficient"
        return "halo_galaxy"
    lv = {}
    for kcls in ("star_cluster", "dm_deficient", "halo_galaxy"):
        vals = [r["B"] for r in rs_ if cls5(r) == kcls]
        lv[kcls] = float(np.mean(vals))
    Bn5 = np.array([r["B"] - lv[cls5(r)] for r in rs_])
    P(f"\n  [B5] the STRUCTURAL classification u01 found (bound star cluster / LambdaCDM-DM-deficient galaxy / "
      f"halo galaxy), one offset each   (3 free parameters, {foot} footing)")
    P(f"        offsets: star clusters {lv['star_cluster']:+.3f}, DM-deficient galaxies {lv['dm_deficient']:+.3f}, "
      f"halo galaxies {lv['halo_galaxy']:+.3f} dex")
    P(f"        ledger rms  {rms0:.3f} -> {float(np.sqrt(np.mean(Bn5**2))):.3f} dex   -- the single best fit in this script")
    P( "        keepers: NONE BROKEN, and for the same reason as B4: every keeper is a halo galaxy, so this is a")
    P( "        relabelling of the residual by LambdaCDM's own dark-matter content, not a gravitational law.  It has")
    P( "        no field equation, makes no new prediction, and is recorded as what the residual LOOKS LIKE.")
    ATT.append(dict(tag="B5", name="structural classification (star cluster / DM-deficient / halo galaxy)", npar=3,
                    footing=foot, rms0=rms0, rms1=float(np.sqrt(np.mean(Bn5**2))),
                    improved=int(sum(1 for r, bn in zip(rs_, Bn5) if abs(bn) < abs(r["B"])-0.05)),
                    worsened=int(sum(1 for r, bn in zip(rs_, Bn5) if abs(bn) > abs(r["B"])+0.05)),
                    keepers_broken=["(none, and that is the problem: it is a classification by LambdaCDM's dark-matter "
                                    "content, not a modification of gravity)"]))
    OUT[f"B5_{foot}"] = lv

# ---- B6 a_0 proportional to H(z): the one modification aimed at the evolution liability alone
P("\n  [B6] a_0 PROPORTIONAL TO H(z) -- aimed at the ONE liability that is about redshift")
def E(z): return math.sqrt(OM_M*(1+z)**3 + OM_L)
z_lo, z_hi = 0.10, 0.85                      # eRASS1's two fixed-mass bins (h68)
pred = 0.5*math.log10(E(z_hi)/E(z_lo))       # deep-MOND: g ~ sqrt(a_0), so dlog g = 1/2 dlog a_0
obs = 0.4082 - 0.2833
info(f"eRASS1 at fixed mass: the residual grows by {obs:+.3f} dex from z = {z_lo} to z = {z_hi} "
     f"(the ledger's erass1_lowz -> erass1_hiz rows)")
info(f"a_0 ~ H(z) predicts a deep-MOND acceleration change of {pred:+.3f} dex over the same interval "
     f"(E(z) = {E(z_lo):.3f} -> {E(z_hi):.3f})")
info(f"so a_0 ~ H(z) accounts for {100*pred/obs:.0f}% of the evolution liability, with ZERO free parameters")
# but the same law is a prediction at z = 0.6-2.5, where item 16 measured it
dlogа0_dz = math.log10(E(2.5)/E(0.0))/2.5
rc100, rc100e = -0.112, 0.063
info(f"the SAME law predicts d log a_0/dz = {dlogа0_dz:+.3f} averaged to z = 2.5; item 16's closed-form inversion "
     f"of RC100 measures {rc100:+.3f} +- {rc100e:.3f}")
nsig = abs(dlogа0_dz - rc100)/rc100e
ck("3a a_0 ~ H(z) buys most of the cluster evolution liability for nothing -- and is excluded by the framework's own "
   "sharpest existing-data constraint, item 16's RC100 inversion, which is a GALACTIC measurement and therefore a keeper",
   nsig > 3, f"predicted d log a_0/dz = {dlogа0_dz:+.3f}, RC100 measures {rc100:+.3f} +- {rc100e:.3f} -- {nsig:.1f} sigma")
ATT.append(dict(tag="B6", name="a_0 proportional to H(z)", npar=0, footing="both",
                rms0=abs(obs), rms1=abs(obs-2*pred),
                improved=1, worsened=0,
                keepers_broken=[f"item 16 RC100 a_0(z): predicted d log a_0/dz = {dlogа0_dz:+.3f} vs measured "
                                f"{rc100:+.3f} +- {rc100e:.3f} ({nsig:.1f} sigma)"]))

# ==================================================================================================== 4
P("\n" + "-"*118)
P("(4) MUTATION CONTROLS AND FOOTINGS")
P("-"*118)
# M1a: the look-elsewhere floor of the 12-variable search, measured on shuffled ledgers
sh_best = []
for _ in range(400):
    Bs = rng.permutation(Bv)
    bb = 1e9
    for nm, x in CAND.items():
        A = np.vstack([x, np.ones_like(x)]).T
        cf = np.linalg.lstsq(A, Bs, rcond=None)[0]
        bb = min(bb, float(np.sqrt(np.mean((Bs - A @ cf)**2))))
    sh_best.append(bb)
sh_best = np.array(sh_best)
info(f"the same 12-variable search run on 400 SHUFFLED ledgers finds a best residual of {sh_best.mean():.3f} +- {sh_best.std():.3f} dex; "
     f"on the REAL ledger it finds {best[1]:.3f} (z = {(best[1]-sh_best.mean())/sh_best.std():+.1f})")
ck("M1a the 12-variable search is not just look-elsewhere noise -- the real ledger's best variable beats the "
   "shuffled floor by many sigma, which is why check 1a had to be rewritten rather than defended",
   best[1] < sh_best.mean() - 3*sh_best.std(),
   f"real {best[1]:.3f} vs shuffled floor {sh_best.mean():.3f} +- {sh_best.std():.3f}")

# M1b: the SPECIFIC control for the winning label -- is 'LambdaCDM says DM-rich' special, or would ANY 7-of-37
# labelling do as well?  The class list (4 outer-halo globulars, DF2, DF4, tidal dwarfs) is 7 rows.
lab = CAND["structural: LCDM says DM-rich"]
n_poor = int((lab == 0).sum())
real_res = RES["structural: LCDM says DM-rich"]["resid"]
rand_res = []
for _ in range(20000):
    idx = rng.choice(len(Bv), n_poor, replace=False)
    z = np.ones(len(Bv)); z[idx] = 0.0
    A = np.vstack([z, np.ones_like(z)]).T
    cf = np.linalg.lstsq(A, Bv, rcond=None)[0]
    rand_res.append(float(np.sqrt(np.mean((Bv - A @ cf)**2))))
rand_res = np.array(rand_res)
p_lab = float((rand_res <= real_res).mean())
info(f"and the winning label is specific, not generic: over 20000 RANDOM {n_poor}-of-{len(Bv)} labellings the residual is "
     f"{rand_res.mean():.3f} +- {rand_res.std():.3f} dex and only {100*p_lab:.2f}% reach the {real_res:.3f} dex that "
     f"LambdaCDM's own dark-matter classification reaches")
ck("M1b AGAINST THE FRAMEWORK -- the classification that organises the residual is LambdaCDM's, and it is not a "
   "generic label: a random 7-of-37 split reaches its residual in under 1% of draws.  It was also fixed independently "
   "(u01 pre-registered the same split on the pressure block) and is not fitted here",
   p_lab < 0.05, f"p = {p_lab:.4f} against random labellings of the same size")

# M2: the keeper battery must respond to the B1 modification with a deliberately huge xi
gp_huge = None
def gp_B1x(xi, a0):
    def f(gbar, r):
        gbar = np.asarray(gbar, float); r = np.asarray(r, float)
        rho_b = 3*gbar/(4*math.pi*G*r)
        return nu_routeA(gbar/(a0*np.sqrt(1.0 + xi*rho_b/RHO_L)))*gbar
    return f
kk = K["canonical"].all_g(gp_B1x(1e-4, A0["canonical"]))
brk = keeper_verdict(BASE["canonical"], kk)
ck("M2 the general keeper interface is live for r-dependent modifications: a density-dependent a_0 with xi = 1e-4 "
   "breaks the keepers, so B1's null result is a measurement and not an insensitivity",
   len(brk) >= 2, f"{len(brk)} keepers broken at xi = 1e-4: " + "; ".join(x.split(':')[0] for x in brk))

c_ = [a for a in ATT if a["footing"] == "canonical"]; al_ = [a for a in ATT if a["footing"] == "alt"]
d = max(abs(x["rms1"] - y["rms1"]) for x, y in zip(c_, al_))
ck("M3 BOTH FOOTINGS -- every attempt's fitted residual and its keeper verdict are the same on the alt footing",
   d < 0.05 and all((len(x["keepers_broken"]) > 0) == (len(y["keepers_broken"]) > 0) for x, y in zip(c_, al_)),
   f"largest |rms_can - rms_alt| = {d:.4f} dex")

dd = dedup(L["canonical"])
Bd = np.array([r["B"] for r in dd])
bd = 1e9; bdn = None
for nm, x in CAND.items():
    xs = np.array([x[[r2["name"] for r2 in rows].index(r["name"])] for r in dd])
    A = np.vstack([xs, np.ones_like(xs)]).T
    cf = np.linalg.lstsq(A, Bd, rcond=None)[0]
    v = float(np.sqrt(np.mean((Bd - A @ cf)**2)))
    if v < bd: bd, bdn = v, nm
info(f"de-duplicated ledger ({len(dd)} independent systems): raw {float(np.sqrt(np.mean(Bd**2))):.3f} dex, "
     f"best single variable '{bdn}' leaves {bd:.3f}")
ck("M4 the organiser search REPLICATES on 22 independent systems -- the same variable wins and removes a similar "
   "share of the variance, so section 1's answer is not an artefact of counting one sample several times",
   bdn == best[0] and abs((1 - bd/float(np.sqrt(np.mean(Bd**2)))) - (1 - best[1]/raw)) < 0.20,
   f"37 rows: '{best[0]}' {raw:.3f} -> {best[1]:.3f} ({100*(1-best[1]/raw):.0f}%);  "
   f"22 systems: '{bdn}' {float(np.sqrt(np.mean(Bd**2))):.3f} -> {bd:.3f} ({100*(1-bd/float(np.sqrt(np.mean(Bd**2)))):.0f}%)")

# ==================================================================================================== 5
P("\n" + "="*118)
P("VERDICT -- class (b): a new variable beside y")
P("="*118)
P(f"""
  The candidate list is shorter than it looks.  The mean enclosed surface density is g_bar/(pi G) exactly, so
  a surface-density law IS a kernel law; and mass, potential depth and mean enclosed density are all invertible
  functions of (g_bar, r).  The entire local class is therefore the class of functions f(y, r), and it is
  refuted by collision rather than by fitting: {len([c for c in COLL if abs(c[4]) > 0.3])} liability system(s) occupy the same (y, r) cell as
  tens to hundreds of SPARC rotation-curve points and need a correction that differs from SPARC's by
  {max((abs(c[4]) for c in COLL), default=0):.2f} dex.

  Of the twelve candidate variables the two that organise the signed residual best are 'is the system
  pressure-supported or lensed' and 'does LambdaCDM give this object a dark halo'.  Neither is a gravitational
  variable, neither breaks a keeper -- because every keeper is a rotation-supported halo galaxy -- and that
  is precisely why neither is a theory.  A modification invisible to all the evidence is not a modification.

  The one attempt with a real physical motivation is B1, the framework's own first law generalised from
  rho_Lambda to rho_Lambda + xi rho_bar.  It fails for a reason that is not fixable by choosing xi: galaxies
  are hundreds of times denser in baryons than cluster outskirts, so the term acts on the keepers first and
  hardest.  The sign that would help the clusters is the sign that destroys the RAR.

  B6 is the exception worth keeping: a_0 proportional to H(z) buys most of the cluster residual's redshift
  evolution for zero parameters.  It is excluded by the framework's own galactic a_0(z) measurement (item 16)
  at {nsig:.1f} sigma, so it is recorded as a fix that costs a keeper, not as a fix.
""")
json.dump(dict(single_variable=RES, attempts=ATT, collisions=OUT["collisions"]),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "u12_extra_variable_modifications.json"), "w"), indent=1)
sys.exit(ck.done())
