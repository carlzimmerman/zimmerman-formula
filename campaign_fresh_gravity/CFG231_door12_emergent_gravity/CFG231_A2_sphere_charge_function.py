#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG231_A2_sphere_charge_function -- G1 (strict and P2 reading) for every variant x geometry x mass x H x normalisation; controls C5, C6, C8.
Frozen: CFG231_FROZEN_CRITERIA.md sections 1, 2 (G1), 4, 6.
Main run: exit 0 if the reproduction controls pass (gate verdicts are results, not exit codes).
MUTATE=MU1 (prescribe the target's own ODE profile), MU4 (footing swap), MU5 (point-mass only), MU8 (admissibility off for B4):
exit 1 when the control bites (the named headline differs from the main run's), exit 0 otherwise (declared control failure, kept).
"""
import sys, os, math, json
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG231_common as C

MUT = os.environ.get("MUTATE") or None
R = C.Report("CFG231_A2_sphere_charge_function", MUT)
C.header(R, "CFG231 A2 -- G1: the charge function R(x) = 4 pi r^3 rho_D g_tot / (a0 M_b(<r)) on the point mass and the exponential sphere")

VARS = ["V0", "V2", "B1", "B2", "B3", "B4", "K3", "K1"]          # B2 == K2 (identical algebra, asserted in A1/C-checks)
GEOMS = ["point", "sphere"]
G = C.G


# ------------------------------------------------------------------------------------------------- KODE (positive control only)
def kode(geom, M, a0_kpc, h=C.H_SPHERE):
    """the target's own ODE  dw/dlnr = a0 r^2 u_N/(u_N + w),  u_N = G M_b(<r), w = G M_c(<r).  Returns dict on XGRID r (own solver)."""
    prof = C.PointMass(M) if geom == "point" else C.ExpSphere(M, h)
    rM = C.r_M_kpc(M, a0_kpc)
    r_out = C.XGRID * rM
    r0 = 1e-4 * r_out[0] if geom == "point" else 1e-7
    uN = lambda r: G * prof.Mb(r)
    if geom == "point":
        w0 = float(uN(r0) * (math.sqrt(1 + (r0 / rM) ** 2) - 1))
    else:
        gN0 = float(uN(r0) / r0 ** 2)
        w0 = r0 ** 2 * math.sqrt(0.4 * a0_kpc * gN0)                    # deep-core start (g_N(r0) << a0 checked below)
        assert gN0 < 1e-3 * a0_kpc
    rhs = lambda s, y: [a0_kpc * math.exp(2 * s) * float(uN(math.exp(s))) / (float(uN(math.exp(s))) + y[0])]
    sol = solve_ivp(rhs, (math.log(r0), math.log(r_out[-1])), [w0], method="LSODA", rtol=1e-11, atol=1e-30, dense_output=True)
    w = lambda r: sol.sol(np.log(r))[0]
    return dict(r=r_out, w=w, prof=prof, rM=rM)


def kode_R(geom, M, a0_kpc, h=C.H_SPHERE):
    k = kode(geom, M, a0_kpc, h)
    r = k["r"]
    Md = lambda rr: k["w"](rr) / G
    rho = C.ddr(Md, r, eps=1e-6) / (4 * math.pi * r ** 2)
    gtot = G * (k["prof"].Mb(r) + Md(r)) / r ** 2
    Rr = 4 * math.pi * r ** 3 * rho * gtot / (a0_kpc * k["prof"].Mb(r))
    return Rr, rho, Md(r), gtot


# ------------------------------------------------------------------------------------------------- controls
R.banner("C5  the P2 law's own phantom (= K1) on the N5 profiles of CFG44 B1: charge-function range vs N5's printed ranges (2%)")
a0k = C.AKPC(C.A0_SI["canonical"])
c5 = {}
for tag, M in (("compact", 1e10), ("diffuse", 1e8)):
    rM = C.r_M_kpc(M, a0k)
    rg = np.geomspace(0.02 * min(rM, 1.0), 300 * rM, 800)
    prof = C.ExpSphere(M, 2.0)
    v = C.variant("K1", prof, rg, a0k)
    Rr = 4 * math.pi * rg ** 3 * v["rho_D"] * v["g_tot"] / (a0k * prof.Mb(rg))
    c5[tag] = (float(Rr.min()), float(Rr.max()), float(np.mean(v["rho_D"] < 0)))
    R.P(f"  {tag:8s} exp. sphere M = {M:.0e}, h = 2: R in [{Rr.min():.3f}, {Rr.max():.3f}]; negative-density fraction {c5[tag][2]:.3f}")
ref5 = {"compact": (1.000, 2.279), "diffuse": (1.000, 2.484)}
ok5 = all(abs(c5[t][0] - ref5[t][0]) < 0.02 * ref5[t][0] and abs(c5[t][1] - ref5[t][1]) < 0.02 * ref5[t][1] for t in ref5)
R.check("C5 K1 (the P2 phantom) on the two exponential spheres: R ranges agree with CFG44 B1 N5's printed [1.000, 2.279] (compact) and [1.000, 2.484] (diffuse) to 2%",
        f"mine {c5}; N5 {ref5}", ok5)
R.num("C5", c5)

R.banner("C6  the core limit R -> 5/2 for a local deep-limit law on a cored sphere (sympy) and its numerical approach")
r_, rho0, Gs, a_ = sp.symbols("r rho0 G a", positive=True)
gN_core = sp.Rational(4, 3) * sp.pi * Gs * rho0 * r_                     # g_N = (4 pi/3) G rho0 r
gD = sp.sqrt(a_ * gN_core)                                               # deep limit of every K-law
u_ = r_ ** 2 * gD
rhoD_ = sp.diff(u_, r_) / (4 * sp.pi * Gs * r_ ** 2)
Mb_ = sp.Rational(4, 3) * sp.pi * rho0 * r_ ** 3
Rcore = sp.simplify(4 * sp.pi * r_ ** 3 * rhoD_ * gD / (a_ * Mb_))
R.P(f"  sympy: R_core = {Rcore}")
prof9 = C.ExpSphere(1e9, 2.0)
rM9 = C.r_M_kpc(1e9, a0k)
rr = np.array([1e-4, 1e-3, 1e-2, 0.1]) * rM9
v9 = C.variant("K1", prof9, rr, a0k)
R9 = 4 * math.pi * rr ** 3 * v9["rho_D"] * v9["g_tot"] / (a0k * prof9.Mb(rr))
R.P(f"  K1 on the 1e9 sphere (h = 2), a = a0: R at x = 1e-4, 1e-3, 1e-2, 0.1 = {[round(float(t), 4) for t in R9]}")
# the target's own core: g_T^2 = (2/5) a g_N (hand) -- from the KODE ODE
kk = kode("sphere", 1e9, a0k)
rc = np.array([1e-3, 1e-2]) * rM9
gT = (kk["w"](rc) + G * prof9.Mb(rc)) / rc ** 2
ratio_gT = gT ** 2 / (a0k * C.gN_of(prof9, rc))
R.P(f"  KODE (the target) in the core: g_T^2/(a g_N) at x = 1e-3, 1e-2 = {[round(float(t), 4) for t in ratio_gT]}  (hand: 2/5)")
ok6 = Rcore == sp.Rational(5, 2) and abs(float(R9[0]) - 2.5) < 0.01 and abs(float(ratio_gT[0]) - 0.4) < 0.01
R.check("C6 core limit: R -> 5/2 (sympy, exact) and numerically 2.5 at x = 1e-4 on the 1e9 sphere; the target's own core has g_T^2 = (2/5) a g_N",
        f"sympy {Rcore}; numeric R(1e-4) = {float(R9[0]):.4f}; g_T^2/(a g_N) = {float(ratio_gT[0]):.4f}", ok6)
R.num("C6", dict(R_core=str(Rcore), R_K1_1e9=[float(t) for t in R9], gT2_over_a_gN=[float(t) for t in ratio_gT]))

R.banner("C8  positive control of the pass logic: KODE (the target's own ODE) passes G1 strict on every cell and is graded M0")
c8 = []
for geom in GEOMS:
    for M in C.MASSES:
        Rr, rho, Md, gt = kode_R(geom, M, a0k)
        c8.append(dict(geom=geom, M=M, maxdev=float(np.max(np.abs(Rr - 1))), rho_min=float(rho.min()), Md_min=float(Md.min())))
mx8 = max(c["maxdev"] for c in c8)
R.P(f"  KODE over {len(c8)} cells (canonical a0): max|R-1| = {mx8:.2e}; min rho_D > 0: {all(c['rho_min'] > 0 for c in c8)}")
# cross-check against Bcommon's target ODE on one sphere and one point mass (read-only)
tf = C.BC.target_fields(C.BC.exp_sphere(1e10, 2.0), a0=a0k)
rB = np.asarray(tf["r"]); sel = (rB > 0.5) & (rB < 300)
kk2 = kode("sphere", 1e10, a0k)
gm = (kk2["w"](rB[sel]) + G * C.ExpSphere(1e10, 2.0).Mb(rB[sel])) / rB[sel] ** 2
xd = float(np.max(np.abs(gm / np.asarray(tf["g"])[sel] - 1)))
R.P(f"  my KODE solver (deep-core start at r0 = 1e-7 kpc) vs Bcommon target g_tot on the 1e10 sphere: max rel dev {xd:.2e}")
# diagnose: rerun MY solver from Bcommon's start (r0 = 1e-3 r_M, w0 = the algebraic P2 value) -- if that reproduces Bcommon, the difference is its initial transient
M10 = 1e10; prof10 = C.ExpSphere(M10, 2.0); rM10 = C.r_M_kpc(M10, a0k); r0b = 1e-3 * rM10
u0 = G * float(prof10.Mb(r0b)); w0b = u0 * (math.sqrt(1 + a0k * r0b ** 2 / u0) - 1)
rhs_b = lambda s_, y: [a0k * math.exp(2 * s_) * G * float(prof10.Mb(math.exp(s_))) / (G * float(prof10.Mb(math.exp(s_))) + y[0])]
sol_b = solve_ivp(rhs_b, (math.log(r0b), math.log(1e4 * rM10)), [w0b], method="LSODA", rtol=1e-11, atol=1e-30, dense_output=True)
gm_b = (sol_b.sol(np.log(rB[sel]))[0] + G * prof10.Mb(rB[sel])) / rB[sel] ** 2
xd_b = float(np.max(np.abs(gm_b / np.asarray(tf["g"])[sel] - 1)))
R.P(f"  my solver started exactly as Bcommon starts (r0 = 1e-3 r_M, w0 = algebraic P2 value): max rel dev vs Bcommon {xd_b:.2e}  "
    f"=> the {xd:.1e} difference is Bcommon's start-point transient (its start value is the P2 algebraic value, not the sphere target's core value), not a solver difference")
R.check("C8 KODE passes G1 strict on every cell (max|R-1| < 1e-6, ODE identity checked by numerical differentiation of my own solution), and it is M0 (prescribed profile)",
        f"max|R-1| {mx8:.1e}", mx8 < 1e-6 and all(c["rho_min"] > 0 for c in c8))
R.check("C8b my ODE solver run from Bcommon's own start reproduces the read-only Bcommon target g_tot on the 1e10 sphere (1e-6)", f"dev {xd_b:.1e}; deep-core start differs from Bcommon by {xd:.1e} (start-point transient, reported)", xd_b < 1e-6)
R.num("C8", dict(maxdev=mx8, dev_deep_start=xd, dev_bcommon_start=xd_b))

R.banner("C10  B2 == K2 (the derivative-free elastic reading is the deep-only constitutive law), checked numerically")
dmax = 0.0
for geom in GEOMS:
    for M in (1e9, 1e11):
        c_b2 = C.G1_cell("B2", geom, M, C.a_V_si("HL"), "shape"); c_k2 = C.G1_cell("K2", geom, M, C.a_V_si("HL"), "shape")
        dmax = max(dmax, max(abs(x - y) / max(abs(y), 1) for x, y in zip(c_b2["R_at"], c_k2["R_at"])))
R.check("C10 B2 and K2 give the same charge function (relative difference < 1e-6) on both geometries", f"max rel diff {dmax:.1e}", dmax < 1e-6)

# ------------------------------------------------------------------------------------------------- the main scan
R.banner("A2.1  G1 scan: variants x {point, sphere} x 7 masses x H in {H_Lambda, H0} x normalisations {shape, tie_canonical, tie_alt}")
res = {}
for v in VARS:
    res[v] = {}
    for Hc in C.HCHOICES:
        a_si = C.a_V_si(Hc)
        res[v][Hc] = {}
        for nm in C.NORMS:
            res[v][Hc][nm] = {}
            for geom in GEOMS:
                if MUT == "MU5" and geom == "sphere":
                    continue
                for M in C.MASSES:
                    if MUT == "MU1":
                        a0t = C.AKPC(C.norm_a0(nm, a_si))
                        Rr, rho, Md, gt = kode_R(geom, M, a0t)
                        cell = dict(maxdev=float(np.max(np.abs(Rr - 1))), all_in_band=bool(np.all(np.abs(Rr - 1) <= 0.1)), x_from=0.1,
                                    R_at=[float(Rr[int(np.argmin(np.abs(C.XGRID - x)))]) for x in (0.1, 1, 3, 10, 30)],
                                    adm=dict(all=True, rho_ok=True, mass_ok=True, g_ok=True), G1P2_maxdev=float("nan"))
                        cell["pass_strict"] = cell["all_in_band"]
                        cell["R_only"] = cell["all_in_band"]
                    else:
                        cell = C.G1_cell(v, geom, M, a_si, nm, Hgate_si=6 * a_si)
                        if MUT == "MU8" and v == "B4":
                            cell["pass_strict"] = cell["R_only"]                   # admissibility line removed
                    res[v][Hc][nm][f"{geom}|{M:.0e}"] = cell

summary = {}
for v in VARS:
    summary[v] = {}
    for Hc in C.HCHOICES:
        summary[v][Hc] = {}
        for nm in C.NORMS:
            cells = res[v][Hc][nm]
            n = len(cells)
            pt = {k: c for k, c in cells.items() if k.startswith("point")}
            sp_ = {k: c for k, c in cells.items() if k.startswith("sphere")}
            summary[v][Hc][nm] = dict(
                n=n, n_pass=sum(c["pass_strict"] for c in cells.values()), n_Ronly=sum(c["R_only"] for c in cells.values()),
                n_point_pass=sum(c["pass_strict"] for c in pt.values()), n_point=len(pt),
                n_sphere_pass=sum(c["pass_strict"] for c in sp_.values()), n_sphere=len(sp_),
                worst_maxdev=max(c["maxdev"] for c in cells.values()),
                point_maxdev=max((c["maxdev"] for c in pt.values()), default=float("nan")),
                sphere_maxdev=max((c["maxdev"] for c in sp_.values()), default=float("nan")),
                adm_all=all(c["adm"]["all"] for c in cells.values()),
                G1P2_worst=float(np.nanmax([c["G1P2_maxdev"] for c in cells.values()])) if any(np.isfinite(c["G1P2_maxdev"]) for c in cells.values()) else float("nan"))
R.num("summary", summary)
for v in VARS:
    for Hc in C.HCHOICES:
        for nm in C.NORMS:
            s = summary[v][Hc][nm]
            R.P(f"  {v:3s} {Hc} {nm:14s}: strict pass {s['n_pass']:2d}/{s['n']}  (R-only {s['n_Ronly']:2d}; point {s['n_point_pass']}/{s['n_point']}, sphere {s['n_sphere_pass']}/{s['n_sphere']}); "
                f"worst max|R-1| {s['worst_maxdev']:.3g} (point {s['point_maxdev']:.3g}, sphere {s['sphere_maxdev']:.3g}); admissible on all cells: {s['adm_all']}; G1-P2 worst {s['G1P2_worst']:.3g}")

R.banner("A2.2  representative R(x) rows (H_Lambda, N-shape): x = 0.1, 1, 3, 10, 30")
for v in VARS:
    for key in ("point|1e+10", "sphere|1e+09", "sphere|1e+12"):
        c = res[v]["HL"]["shape"].get(key)
        if c:
            R.P(f"  {v:3s} {key:13s}: R = {[round(t, 4) for t in c['R_at']]}; in band from x = {c['x_from']}; admissible {c['adm']['all']}")

R.banner("A2.3  reported sensitivity: CFG117's h(M) = 2, 3, 4, 5 kpc for M = 1e9..1e12 (H_Lambda, N-shape)")
sens = {}
for v in VARS:
    devs = []
    for M, h in ((1e9, 2.0), (1e10, 3.0), (1e11, 4.0), (1e12, 5.0)):
        c = C.G1_cell(v, "sphere", M, C.a_V_si("HL"), "shape", Hgate_si=6 * C.a_V_si("HL"), h=h)
        devs.append(c["maxdev"])
    sens[v] = devs
    R.P(f"  {v:3s}: max|R-1| for (1e9,h2), (1e10,h3), (1e11,h4), (1e12,h5) = {[round(t, 3) for t in devs]}")
R.num("sensitivity_h_of_M", sens)

R.banner("A2.4  the core-limit finding across the K laws (reported): sphere x = 0.1 at 1e9 M_sun, H_Lambda, N-shape")
for v in ("K1", "B2", "K3", "B4"):
    c = res[v]["HL"]["shape"]["sphere|1e+09"] if "sphere|1e+09" in res[v]["HL"]["shape"] else None
    if c:
        R.P(f"  {v}: R(0.1) = {c['R_at'][0]:.4f}")

# ------------------------------------------------------------------------------------------------- headline and MUTATE logic
def G1_strict_all(v, Hc="HL"):
    return all(summary[v][Hc][nm]["n_pass"] == summary[v][Hc][nm]["n"] for nm in C.NORMS)


head = {v: {Hc: G1_strict_all(v, Hc) for Hc in C.HCHOICES} for v in VARS}
R.P("\n  G1 strict verdict (all three normalisations, all cells, admissible), per variant and H:")
for v in VARS:
    R.P(f"    {v:3s}: H_Lambda {'PASS' if head[v]['HL'] else 'FAIL'}   H0 {'PASS' if head[v]['H0'] else 'FAIL'}")
R.num("G1_strict_verdict", head)
split = {v: {Hc: {nm: (summary[v][Hc][nm]['n_pass'] == summary[v][Hc][nm]['n']) for nm in C.NORMS} for Hc in C.HCHOICES} for v in VARS}
R.num("G1_split_by_norm", split)
R.P("  split by normalisation (H_Lambda): " + "; ".join(f"{v}: shape {split[v]['HL']['shape']}, canon {split[v]['HL']['tie_canonical']}, alt {split[v]['HL']['tie_alt']}" for v in VARS))

main_ref = "CFG231_A2_sphere_charge_function_results.json"
bites = None
if MUT:
    R.banner(f"MUTATE {MUT}: does the named headline change relative to the main run?")
    outdir = os.environ.get("CFG231_OUT", C.HERE)
    ref = json.load(open(os.path.join(outdir, main_ref)))["numbers"]
    mref = ref["summary"]
    if MUT == "MU1":
        flips = [v for v in VARS if (not ref["G1_strict_verdict"][v]["HL"]) and head[v]["HL"]]
        bites = len(flips) == len(VARS)
        R.P(f"  prescribing the target's own ODE profile flips G1 strict F -> P for {flips}: bites = {bites}. Mechanism grade of this run: M0 (prescribed)")
    elif MUT == "MU4":
        # K1, H_Lambda, point mass: tie_canonical vs tie_alt (the footing swap), and H0 vs canonical
        pass_can = mref["K1"]["HL"]["tie_canonical"]["n_point_pass"]
        pass_alt = summary["K1"]["HL"]["tie_alt"]["n_point_pass"]
        pass_h0 = mref["K1"]["H0"]["tie_canonical"]["n_point_pass"]
        R.P(f"  K1 point-mass N-tie cells passing (of 7 masses): H_Lambda vs canonical {pass_can}; H_Lambda vs alt {pass_alt} (swap); H0 vs canonical {pass_h0}")
        bites = (pass_can == 7 and pass_alt == 0)
        R.P(f"  bites = {bites} (point-mass N-tie cell flips P -> F under the footing swap)")
    elif MUT == "MU5":
        s_all = mref["K1"]["HL"]
        strict_pt = all(summary["K1"]["HL"][nm]["n_point_pass"] == summary["K1"]["HL"][nm]["n_point"] for nm in C.NORMS)
        sc_pt = all(summary["K1"]["HL"][nm]["n_point_pass"] == summary["K1"]["HL"][nm]["n_point"] for nm in ("shape", "tie_canonical"))
        R.P(f"  K1, point mass only: strict (shape AND canonical AND alt) = {strict_pt}; shape AND canonical only = {sc_pt}; full-grid strict in the main run = {ref['G1_strict_verdict']['K1']['HL']}")
        R.P("  the frozen expectation was 'K1 G1 strict flips F -> P on the point-mass-only grid'. It does NOT (the alt footing fails on the point mass too, R -> 0.7985); only the shape+canonical sub-line flips. Declared control failure of the frozen claim, kept.")
        bites = strict_pt and (not ref["G1_strict_verdict"]["K1"]["HL"])
    elif MUT == "MU8":
        b4_pt_shape_main = mref["B4"]["HL"]["shape"]["n_point_pass"]
        b4_pt_shape_mut = summary["B4"]["HL"]["shape"]["n_point_pass"]
        R.P(f"  B4 point-mass N-shape strict pass cells (of 7): main {b4_pt_shape_main}, admissibility off {b4_pt_shape_mut}")
        bites = (b4_pt_shape_main == 0 and b4_pt_shape_mut == 7)
        R.P(f"  bites = {bites}: an R-only test passes B4's point mass; the admissibility line is what fails it")
    R.num("bites", bool(bites))

if not MUT:
    nf = R.write()
    sys.exit(0 if nf == 0 else 1)
else:
    R.write()
    sys.exit(1 if bites else 0)
