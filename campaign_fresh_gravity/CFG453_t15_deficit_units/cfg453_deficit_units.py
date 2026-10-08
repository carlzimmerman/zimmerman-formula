#!/usr/bin/env python3
"""CFG453: is T15/T16's group/cluster overdraft a units mismatch in the deficit x?  (criteria: FROZEN_CRITERIA.md, b1132dd48)

T15 defines x = (M_tot - M_b)/M_b but used CFG382 definition A, x_A = (M_tot - M_b - M_ph)/(5.364 M_b), for groups/clusters.
Identity: x_T15 = 5.364 x_A + (nu - 1).  D1 checks it and the measured baryon fraction; D2 re-runs the budget on x_T15.
Footings never pooled.  Run: python3 cfg453_deficit_units.py  |  CFG453_MUTATE=1 re-plants x := x_A.  Local data only.
"""
import json, math, os, sys
import numpy as np
from astropy.io import fits

MUT = os.environ.get("CFG453_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
import CFG4_common as C4  # noqa: E402  (read-only: nu_mono, as the CFG382 audit uses)

A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
BS = (0.0, 0.3)
COSMIC = 5.364
lines = []
def say(s=""):
    lines.append(s); print(s)

# ------------------------------------------------------------------ objects (CFG382 audit read, gas at the JSON R500 as CFG450)
Gcgs, MSUN_CGS, KPC_CGS = 6.674e-8, 1.989e33, 3.0857e21
xdir = os.path.join(REPO, "real_research", "data", "xcop")
r5 = json.load(open(os.path.join(xdir, "xcop_r500_ettori2019.json")))
CL = []
for nm in sorted(os.listdir(xdir)):
    d = os.path.join(xdir, nm)
    if not os.path.isdir(d) or nm not in r5 or not os.path.exists(os.path.join(d, f"{nm}_mstar.fits")):
        continue
    hm = fits.open(os.path.join(d, f"{nm}_hydro_mass.fits"))["HYDRO_MASS"].data
    F = fits.open(os.path.join(d, f"{nm}_fgas_profile.fits"))["FGAS"]
    ms = fits.open(os.path.join(d, f"{nm}_mstar.fits"))["MSTAR_SMOOTHED"].data
    Rk = r5[nm]["R500"] * 1000
    Mg = float(np.exp(np.interp(math.log(Rk / float(F.header["R500"])), np.log(np.asarray(F.data["RADIUS"], float)), np.log(np.asarray(F.data["MGAS"], float)))))
    Ms = float(np.exp(np.interp(np.log(Rk), np.log(np.asarray(ms["RADIUS"], float)), np.log(np.asarray(ms["MSTAR"], float)))))
    CL.append(dict(name=nm, R=Rk, M=float(np.interp(Rk, np.asarray(hm["RADIUS"], float), np.asarray(hm["M_FORW"], float))), Mb=Mg + Ms))
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")) if not l.startswith("#")]
hdr, rows = rows[0], [x for x in rows[1:] if len(x) > 5]
GRP = [dict(R=float(x[hdr.index("R500_kpc")]), M=float(x[hdr.index("M500_1e13")]) * 1e13, Mb=1.10 * float(x[hdr.index("Mgas500_1e12")]) * 1e12) for x in rows]

def per_object(objs, b, a0):
    out = []
    for o in objs:
        Mt = o["M"] / (1 - b)
        gN = Gcgs * o["Mb"] * MSUN_CGS / (o["R"] * KPC_CGS) ** 2
        nu = float(C4.nu_mono(np.array([gN / (a0 * 100)]))[0])
        xA = (Mt - o["Mb"] - (nu - 1) * o["Mb"]) / (COSMIC * o["Mb"])
        xT = (Mt - o["Mb"]) / o["Mb"]
        out.append(dict(Mb=o["Mb"], R=o["R"], fb=o["Mb"] / Mt, nu=nu, xA=xA, xT=xT, ident=abs(xT - (COSMIC * xA + nu - 1))))
    return out

# ------------------------------------------------------------------ T15 / T16 (as CFG451, verbatim formulas)
G = 6.674e-11; GYR = 3.156e16; TAU = 10.3 * GYR; KPC = 3.086e19
LAM = 0.028; RHO_R500 = 1.55e-24
F_R500 = 1 - math.exp(-LAM * math.sqrt(4 * math.pi * G * RHO_R500) * TAU)
RATE_R500_TAU = math.sqrt(4 * math.pi * G * RHO_R500) * TAU
def S_of_R(Mb, R, a0):
    return 1.0 / (math.exp(math.sqrt(G * Mb * 1.989e30 / a0) / KPC / R) - 1.0)
def lam_max(x, S):
    return math.inf if x >= S else -math.log(1 - x / S) / RATE_R500_TAU
def mw_points(a0):
    out = {}
    for Mb in (7.0e10, 1.0e11):
        S = S_of_R(Mb, 30.0, a0)
        for V in (188, 200, 230):
            x = ((V * 1e3) ** 2 * (30 * KPC) / G - Mb * 1.989e30) / (Mb * 1.989e30)
            rt = math.sqrt(4 * math.pi * G * (V * 1e3) ** 2 / (4 * math.pi * G * (30 * KPC) ** 2)) * TAU
            out[f"Mb{Mb:.0e}_V{V}"] = dict(feasible=x <= S, lam_max=(-math.log(1 - x / S) / rt) if x <= S else math.inf)
    return out
def budget(a0, xg, xc, Sg, Sc):
    """xg/xc = (b0, b03) deficits; Sg/Sc = S/M_b (scalars)."""
    rowsB = {"groups_b0": xg[0] - F_R500 * Sg, "groups_b03": xg[1] - F_R500 * Sg, "clusters_b0": xc[0] - F_R500 * Sc, "clusters_b03": xc[1] - F_R500 * Sc}
    win = {"groups": [lam_max(xg[0], Sg), lam_max(xg[1], Sg)], "clusters": [lam_max(xc[0], Sc), lam_max(xc[1], Sc)]}
    mw = mw_points(a0); inter = {}
    for lab, keys in (("frozen_Mb7e10", [k for k in mw if k.startswith("Mb7e+10")]), ("verbatim_both_Mb", list(mw))):
        mwl = [mw[k]["lam_max"] for k in keys if mw[k]["feasible"]]
        w = [[min(mwl), max(mwl)] if mwl else [math.inf, math.inf], win["groups"], win["clusters"]]
        lo, hi = max(v[0] for v in w), min(v[1] for v in w)
        inter[lab] = dict(inter=[lo, hi], nonempty=bool(lo <= hi and math.isfinite(lo)))
    gap = 0.028 / win["clusters"][1] if math.isfinite(win["clusters"][1]) else 0.0
    return dict(rows=rowsB, windows=win, inter=inter, V4=[gap, "STANDS" if gap >= 1.5 else ("WEAKENED" if gap >= 1.0 else "BREAKS")])

checks = {}
say(f"CFG453 T15 deficit units  MUTATE={MUT}")
say("")
D1, OUT = {}, {}
C451 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG451_t15_t16_own_footings", "cfg451_results.json")))["rows"]
D450 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG450_xcop_gas_radius_audit", "cfg450_results.json")))["deficits"]
c1err, c2err = [], []
for fk, a0 in A0.items():
    P = {b: dict(cl=per_object(CL, b, a0), gr=per_object(GRP, b, a0)) for b in BS}
    med = lambda L, k: float(np.median([o[k] for o in L]))
    ident = max(o["ident"] for b in BS for L in P[b].values() for o in L)
    xA = {k: [med(P[b][k], "xA") for b in BS] for k in ("gr", "cl")}
    xT = {k: [med(P[b][k], "xT") for b in BS] for k in ("gr", "cl")}
    fb = {k: [med(P[b][k], "fb") for b in BS] for k in ("gr", "cl")}
    nu = {k: med(P[0.0][k], "nu") for k in ("gr", "cl")}
    c2err += [abs(xA["cl"][0] - D450[fk]["0.0"]["clusters_R500"]["med"]), abs(xA["cl"][1] - D450[fk]["0.3"]["clusters_R500"]["med"])]
    # C1: def-A inputs, T15 conventions -> CFG451 rows
    ref = next(v for k, v in C451.items() if k.startswith(fk))
    Sg_c, Sc_c = S_of_R(6e12, 554.0, a0), S_of_R(2.8e13, 985.0, a0)
    bA = budget(a0, ref["deficits"][:2], ref["deficits"][2:], Sg_c, Sc_c)
    c1err += [abs(bA["rows"][k] - ref["T15"]["rows"][k]) for k in bA["rows"]]
    say(f"{fk} footing (a0 {a0:.4e})")
    say(f"  D1 identity x_T15 = 5.364 x_A + (nu-1): max |err| {ident:.1e};  median nu at R500: groups {nu['gr']:.3f}, clusters {nu['cl']:.3f}")
    say(f"  measured f_b = M_b/M_tot (b=0 / 0.3): clusters {fb['cl'][0]:.3f}/{fb['cl'][1]:.3f}, groups {fb['gr'][0]:.3f}/{fb['gr'][1]:.3f};"
        f"  T15's implied f_obs = 1/(1+x_A): clusters {1/(1+0.41):.3f}, groups {1/(1+0.79):.3f}")
    say(f"  x_A (def A, cosmic-share units): clusters {xA['cl'][0]:.4f}/{xA['cl'][1]:.4f}  groups {xA['gr'][0]:.3f}/{xA['gr'][1]:.3f}")
    say(f"  x_T15 = (M_tot-M_b)/M_b:          clusters {xT['cl'][0]:.3f}/{xT['cl'][1]:.3f}  groups {xT['gr'][0]:.3f}/{xT['gr'][1]:.3f}")
    conf = bool(0.08 <= fb["cl"][0] <= 0.25 and not (0.08 <= 1 / 1.41 <= 0.25))
    xin = (xA if MUT else xT)
    # (i) T15 conventions
    b_i = budget(a0, xin["gr"], xin["cl"], Sg_c, Sc_c)
    # (ii) per-object S: median over objects of x_i - f_law S_i (rows); windows from per-object medians of x and S
    def per_obj_rows(L, key):
        return float(np.median([(o["xA"] if MUT else o["xT"]) - F_R500 * S_of_R(o["Mb"], o["R"], a0) for o in L]))
    Sg_o = float(np.median([S_of_R(o["Mb"], o["R"], a0) for o in P[0.0]["gr"]])); Sc_o = float(np.median([S_of_R(o["Mb"], o["R"], a0) for o in P[0.0]["cl"]]))
    b_ii = budget(a0, xin["gr"], xin["cl"], Sg_o, Sc_o)
    b_ii["rows"] = {f"{k}_b{'0' if b == 0 else '03'}": per_obj_rows(P[b][kk], k) for b in BS for k, kk in (("groups", "gr"), ("clusters", "cl"))}
    for lab, bb, Sg, Sc in (("(i) T15 conventions", b_i, Sg_c, Sc_c), ("(ii) per-object S", b_ii, Sg_o, Sc_o)):
        r = bb["rows"]
        say(f"  D2 {lab}: S/M_b groups {Sg:.3f} clusters {Sc:.3f};  M_cold/M_b clusters {r['clusters_b0']:+.3f}/{r['clusters_b03']:+.3f}  groups {r['groups_b0']:+.3f}/{r['groups_b03']:+.3f}")
        w = bb["windows"]
        say(f"       lambda_max clusters [{w['clusters'][0]:.4f}, {w['clusters'][1]:.4f}] groups [{w['groups'][0]:.4f}, {w['groups'][1]:.4f}]  (inf = no ceiling: the deficit exceeds the whole kernel supply)"
            f";  V4 gap {bb['V4'][0]:.2f}x {bb['V4'][1]};  V5 frozen nonempty {bb['inter']['frozen_Mb7e10']['nonempty']}, verbatim nonempty {bb['inter']['verbatim_both_Mb']['nonempty']}")
    # like-for-like ledger
    for k, kk in (("clusters", "cl"), ("groups", "gr")):
        L = P[0.0][kk]
        ph = float(np.median([o["nu"] - 1 for o in L])); ex = float(np.median([COSMIC * o["xA"] for o in L])); tot = float(np.median([o["nu"] - 1 + COSMIC * o["xA"] for o in L]))
        say(f"  ledger b=0 {k}: law phantom {ph:.2f} M_b + beyond-law {ex:.2f} M_b = dark {tot:.2f} M_b  vs one cosmic cold share 5.364 M_b  (ratio {tot/COSMIC:.2f})")
    V1 = {lab: bool(bb["rows"]["clusters_b0"] >= 0) for lab, bb in (("i", b_i), ("ii", b_ii))}
    D1[fk] = dict(confirmed=conf, identity_err=ident, fb=fb, xA=xA, xT=xT, nu=nu)
    OUT[fk] = dict(i=b_i, ii=b_ii, V1_cluster_b0_nonneg=V1)
    say("")
checks["C1_cfg451_rows"] = bool(max(c1err) < 1e-9)
checks["C2_cfg450_xA"] = bool(max(c2err) < 1e-3)
checks["D1_identity_1e-9"] = bool(all(v["identity_err"] < 1e-9 for v in D1.values()))
confirmed = all(v["confirmed"] for v in D1.values())
nonneg = all(OUT[fk]["V1_cluster_b0_nonneg"]["i"] for fk in A0) or all(OUT[fk]["V1_cluster_b0_nonneg"]["ii"] for fk in A0)
head = ("the overdraft was a units artefact" if nonneg else "mismatch real, overdraft survives it") if confirmed else "no mismatch"
if MUT:
    checks["MUTATE_misread_returns_negative"] = bool(all(not OUT[fk]["V1_cluster_b0_nonneg"][k] for fk in A0 for k in ("i", "ii")))
say(f"D1 mismatch {'CONFIRMED' if confirmed else 'NOT CONFIRMED'};  HEADLINE: {head}")
say("checks: " + json.dumps(checks))
json.dump(dict(mutate=MUT, D1=D1, D2=OUT, headline=head, checks=checks), open(os.path.join(HERE, f"cfg453_results{TAG}.json"), "w"), indent=1, default=float)
ok = all(checks.values())
print("<LANE> COMPLETE: all checks PASS" if ok else "<LANE> COMPLETE: -- SOME CHECKS FAIL")
sys.exit(0 if ok else 1)
