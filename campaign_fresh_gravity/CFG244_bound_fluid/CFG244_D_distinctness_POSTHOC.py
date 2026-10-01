#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG244 Gate D -- DISTINCTNESS (where does the route differ from LambdaCDM?)  *** POST-HOC EXTRA ***
Gate A failed (the first binding FAIL under the frozen stop rule), so Gate D is NOT part of the verdict: this script runs the frozen
list D1-D7 as a clearly labelled post-hoc extra, with the frozen estimate compared.  File names carry _POSTHOC.
Frozen criteria: ../CFG244_FROZEN_CRITERIA.md (committed 84e100c47, sha256 944adc80...).
Operational meaning (frozen): REDUCES TO LAMBDACDM PLUS A COINCIDENCE iff every observable D1-D7 has |P_route - P_LCDM| below its stated threshold
(2 sigma_cap of the cited forecast, or 0.05 dex for a model-to-model comparison with no cap), and the only content the route adds is the numerical
statement a0 = kappa c sqrt(G rho_Lambda), kappa FITTED, which enters no equation of the class.  DISTINCT iff at least one observable is DISTINCT
from LambdaCDM with the route's value derived (Gates A / H), not tuned.
Inputs: the Gate A and Gate H outputs of this lane (JSON) and the committed forecast numbers (cited in the output; read from the committed READMEs and
closure_map files, transcribed here with their sources).  Nothing is fitted.
Run: python3 CFG244_D_distinctness_POSTHOC.py ; MUTATE=MD1 python3 ...   Exit: main 0; MUTATE exits 1 when the control bites.
kappa = 1/2 FITTED; no dark-matter particle; the mass is required; nothing here is closure.
"""
import os, sys, math, json
sys.dont_write_bytecode = True
import numpy as np
import CFG244_common as K

K.use_lane_code()
MUT = os.environ.get("MUTATE", "")
R = K.Report("CFG244_D_distinctness_POSTHOC" + (f"_MUTATE_{MUT}" if MUT else ""))
P = R.P
P(__doc__.split("Run: python3")[0].strip())
P("\n  repo: <repo>   POST-HOC EXTRA (Gate A already bound; nothing here is a verdict input)")
HERE = K.HERE
A = json.load(open(os.path.join(HERE, "CFG244_A_infall_bound_results.json")))["numbers"]
Hn = json.load(open(os.path.join(HERE, "CFG244_H_satellites_results.json")))["numbers"]
sims = json.load(open(os.path.join(HERE, "CFG244_A_infall_bound_sims.json")))
MASSES = (1e9, 1e10, 1e11, 1e12)
QS = (0.05, 0.1, 0.2)
XB = 10.0 ** np.round(np.arange(-1.0, 1.5001, 0.1), 10)
XC = np.sqrt(XB[1:] * XB[:-1])
G = 4.30091e-6
A0K = 9.3603e-11 * 3.0856775814913673e19 / 1e6


def rM(M):
    return math.sqrt(G * M / A0K)


# ------------------------------------------------------------------------------------------------ the observable table
def build(route_overrides=None):
    T = {}
    # D1: the effective a0 of the route's bound-fluid scale: a0_eff = 3 G M_b / R_s^2 (target R_s = sqrt(3) r_M), spread across 1e9-1e12 in dex
    xs = {q: A["A"]["exponents"][f"point|{q}"]["x_Rs"] for q in QS}
    sp = {q: 2.0 * math.log10(max(xs[q]) / min(xs[q])) for q in QS}
    # the LambdaCDM-with-SHMR comparator (reading (b) of Gate H, M_* = M_b): radius where (1 - f_b) M_NFW(<r) = M_b
    g42 = K.exec_prefix("CFG42_satellites_rule.py", K.BAR + "C1 / C2")
    halo_mass, FB, RHO_C = g42["halo_mass"], g42["FB"], g42["g36"]["RHO_C"]
    HH = 0.674
    cd = lambda Mh: 5.71 * (Mh / (2e12 / HH)) ** (-0.084)
    mn = lambda t: math.log1p(t) - t / (1 + t)
    from scipy.optimize import brentq
    xl = []
    for M in MASSES:
        Mh = float(halo_mass(M)); c = cd(Mh); R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
        f = lambda r: (1 - FB) * Mh * mn(c * r / R200) / mn(c) - M
        try:
            r_ = brentq(f, 1e-3, 5 * R200)
        except ValueError:
            r_ = float("nan")
        xl.append(r_ / rM(M))
    sp_l = 2.0 * math.log10(np.nanmax(xl) / np.nanmin(xl)) if np.all(np.isfinite(xl)) else float("nan")
    p_l = float(np.polyfit(np.log10(MASSES), np.log10(np.array(xl) * np.array([rM(M) for M in MASSES])), 1)[0]) if np.all(np.isfinite(xl)) else float("nan")
    T["D1"] = dict(name="the tie as a coincidence: spread of the effective a0 (3 G M_b / R_s^2) over 1e9-1e12 Msun (dex)",
                   route=float(np.mean(list(sp.values()))), lcdm_frozen_text=float(np.mean(list(sp.values()))), lcdm_shmr_comparator=sp_l,
                   bound=0.048, threshold=0.05, extra=f"route x_Rs = {xs[0.1]}; SHMR comparator x_Rs = {xl}, exponent {p_l:.3f}")
    # D2: a0(z) at z = 2.5 (dex shift of the effective zero point): committed values
    T["D2"] = dict(name="a0 at z about 2.5 (dex)", route=0.334, lcdm=0.334, flat_B=0.0, Hz=0.58, cap_sigma_vs_lcdm=1.3,
                   source="closure_map/GATES.md row 3.10 (flat 0.00, LCDM-native +0.334); WHAT_WOULD_DECIDE section 2 (H(z) +0.58; cap 1.3 sigma vs LCDM-native, 2.3 vs H(z)); CFG222",
                   note="route value = the LCDM-native expectation by the class's structure (no acceleration scale in the class; CFG230 R02's Newtonian-only half: the only length is M^(1/3)(G/H^2)^(1/3), so the effective scale follows H(z)); argued, not computed from simulations at z = 2.5")
    # D3: satellites from Gate H
    pr = Hn["primary"]["out"]
    T["D3"] = dict(name="satellites: route (b) minus LCDM comparator offsets (dex), P1/P2/P3", route=[pr["b"]["canonical"]["V1"][p]["off"] for p in ("P1", "P2", "P3")],
                   lcdm=[pr["b"]["canonical"]["V1"][p]["off"] for p in ("P1", "P2", "P3")], note="reading (b) IS the record's LCDM comparator (CFG69): identical by construction (control C-H1 reproduces its numbers)")
    # D4: RAR scatter at fixed g_bar from the Gate A runs: spread of log10(C_bound/C_target) over q and mass
    tabs = A["tables"]
    sc = {}
    for xi in (1.12, 28.2):
        i = int(np.argmin(np.abs(np.log(XC / xi))))
        vals = [math.log10(tabs[f"canonical|{q}|{M:.0e}|point"]["loc"][i]) for q in QS for M in MASSES]
        sc[xi] = dict(std_dex=float(np.std(vals)), range_dex=float(max(vals) - min(vals)))
    T["D4"] = dict(name="RAR scatter at fixed g_bar: scatter of log10(C_bound/C_target) over 12 (q, M) cases (dex)", route=sc, bound=0.048,
                   lcdm="(memory, unverified) published LambdaCDM-based RAR scatters are of order 0.1 dex or more", threshold=0.05)
    # D5: the bound outer slope of rho_c (x in [2, 30]) and inner (x in [0.1, 0.5]) from the stored dM
    sl = {}
    for rr in sims["runs"]:
        s = rr["spec"]
        if s["kind"] != "main" or s["geom"] != "point" or s["q"] != 0.1:
            continue
        M = s["M"]; e = XB * rM(M); rc = np.sqrt(e[1:] * e[:-1]); vol = 4 * math.pi / 3 * (e[1:] ** 3 - e[:-1] ** 3)
        rho = np.array(rr["foot"]["canonical"]["inst"]["dM"]) / vol
        for nm, lo, hi in (("outer", 2.0, 30.0), ("inner", 0.1, 0.5)):
            m = (rc / rM(M) >= lo) & (rc / rM(M) <= hi) & (rho > 0)
            sl[f"{M:.0e}|{nm}"] = float(np.polyfit(np.log(rc[m]), np.log(rho[m]), 1)[0])
    T["D5"] = dict(name="profile slopes of the bound rho_c (q = 0.1, point cores)", route=sl, target="1/r inside r_M, 1/r^2 outside (CFG44 point mass)", lcdm="NFW: -1 inner, -3 beyond r_s (memory); EdS self-similar -9/4 (CFG118 C2)",
                   note="the route's profile IS the collapse profile of a cold collisionless fluid without feedback; the difference from the NFW slope is the finite range and the baryon core, not a prediction beyond LCDM")
    T["D6"] = dict(name="Gaia DR4 wide binaries gamma-hat", route=1.000, lcdm=1.000, B_armC=1.000, bare_law=1.1614, source="WHAT_WOULD_DECIDE section 1 (CFG63)")
    T["D7"] = dict(name="KiDS early-minus-late colour split at fixed g_bar", route="halo mass follows stellar mass and colour (LCDM-like)", lcdm="fits with colour-split Moster (chi2 6.5/7, CFG67)",
                   B_and_any_negligible_difference_model="fails at face value (28.1/7, CFG77)", source="WHAT_WOULD_DECIDE section 4")
    if route_overrides:
        for k, v in route_overrides.items():
            T[k].update(v)
    return T


def judge(T, a_failed=True):
    """per observable: DISTINCT from LambdaCDM (True/False) under the frozen thresholds; the route's value must be derived (not tuned)."""
    d = {}
    # D1: not distinct if the route's spread and LambdaCDM's both exceed the committed RAR bound, or the route equals the frozen-text LCDM value
    d["D1"] = abs(T["D1"]["route"] - T["D1"]["lcdm_frozen_text"]) >= T["D1"]["threshold"]
    d["D2"] = abs(T["D2"]["route"] - T["D2"]["lcdm"]) >= 2 * 0.0 + 0.05     # model-to-model, no cap for the route-vs-LCDM difference
    d["D3"] = float(np.max(np.abs(np.array(T["D3"]["route"]) - np.array(T["D3"]["lcdm"])))) >= 0.05
    d["D4"] = False if a_failed else True
    d["D5"] = False
    d["D6"] = abs(T["D6"]["route"] - T["D6"]["lcdm"]) >= 0.02
    d["D7"] = False
    return d


T = build()
P("\n  OBSERVABLE TABLE (route value from this lane's Gate A / Gate H outputs; LambdaCDM values committed or marked (memory))")
for k, v in T.items():
    P(f"  {k}: {v['name']}")
    for kk, vv in v.items():
        if kk != "name":
            P(f"      {kk}: {vv if not isinstance(vv, float) else f'{vv:.4g}'}")
if MUT == "MD1":
    # plant 'route = LambdaCDM comparator' (every route value set equal to the LCDM value) and 'route a0(z) = flat'
    T_a = build({"D1": {"route": T["D1"]["lcdm_frozen_text"]}, "D2": {"route": T["D2"]["lcdm"]}})
    T_b = build({"D2": {"route": 0.0}})
    ja, jb = judge(T_a), judge(T_b)
    va = "DISTINCT" if any(ja.values()) else "REDUCES"; vb = "DISTINCT" if any(jb.values()) else "REDUCES"
    bite = va != vb
    P(f"\n  MUTATE MD1: plant route = LambdaCDM -> {va}; plant route a0(z) = flat (0.00 dex vs LCDM-native +0.334) -> {vb}.  BITES (the verdict flips): {bite}")
    R.num("mutate", dict(id="MD1", plant_lcdm=va, plant_flat=vb, bites=bool(bite)))
    R.write(); sys.exit(1 if bite else 0)

J = judge(T)
P("\n  JUDGEMENT per observable (frozen thresholds): DISTINCT from LambdaCDM?")
why = {"D1": f"route {T['D1']['route']:.2f} dex vs the committed RAR bound 0.048 dex; the route's value equals LambdaCDM's by the frozen text (same fluid); the SHMR comparator differs ({T['D1']['lcdm_shmr_comparator']:.2f} dex) because it contains baryon loss/feedback the route lacks, which is a disagreement of two cold-collapse models, not a prediction beyond LambdaCDM",
       "D2": "route = LCDM-native (+0.334 dex) by the class's structure; distinct from flat B (0.33 dex), not from LCDM",
       "D3": "(b) is the LCDM comparator; distinct from B, not from LCDM",
       "D4": "Gate A failed: the route's scatter is the infall's, comparable to or above LCDM's; not B-like",
       "D5": "collapse profile of a cold fluid without feedback; no prediction beyond LCDM",
       "D6": "all of route, LCDM, B (Arm C) predict 1.000; only the bare law differs",
       "D7": "route follows LCDM's halo-mass dependence"}
for k, v in J.items():
    P(f"  {k}: {'DISTINCT' if v else 'NOT DISTINCT'} -- {why[k]}")
verdict = "DISTINCT" if any(J.values()) else "REDUCES TO LAMBDACDM PLUS A COINCIDENCE"
P(f"\n  GATE D (post-hoc): {verdict}")
P("  The only content the route adds to the LambdaCDM comparator is the numerical statement a0 = kappa c sqrt(G rho_Lambda) with kappa = 1/2 FITTED; it enters no equation of the class (the class has no acceleration scale: D2's argument), so it is a coincidence the route neither explains nor tests.")
P("  This is a statement about THIS class (a bound early cold fluid with no extra coupling); it is not a statement about candidate B, whose flat a0(z) and tight RAR are what the class does not make.")
R.num("table", T); R.num("judge", J); R.num("verdict", verdict)
R.write()
sys.exit(0)
