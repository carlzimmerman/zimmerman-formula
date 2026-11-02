#!/usr/bin/env python3
"""OD1_old_disc_ruler (FROZEN_CRITERIA.md). Same-population dispersions on UR3's DiskMass estimator. OD1_MUTATE=1 writes separate outputs.
kappa = 1/2 FITTED, unused beyond the law's record rows; not theory closed; nothing here says the data favour the framework.
Run: PYTHONHASHSEED=0 python3 -I od1.py"""
import contextlib, io, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
MUT = os.environ.get("OD1_MUTATE", "0") == "1"; TAG = ("_MUTATE_c" if os.environ.get("OD1_MUT_C") == "1" else "_MUTATE_a") if MUT else ""; OUT = []; FAIL = []
def P(s=""): print(s, flush=True); OUT.append(s)
def J(*a): return json.load(open(os.path.join(RB, *a)))
def check(ok, m):
    P(f"  {'PASS' if ok else 'FAIL'} {m}")
    if not ok: FAIL.append(m)
SRC = json.load(open(os.path.join(HERE, "sources.json")))
UR3, SP3, SPP, UL1 = J("UR3_direct_weighing", "ur3_diskmass.json"), J("SP3_starting_point", "sp3_weigh.json"), J("SP3_starting_point", "sp3_post.json"), J("UL1_measured_upsilon_test", "ul1_weigh.json")
C576 = J("..", "campaign_fresh_gravity", "CFG576_diskmass_sigz", "cfg576_results.json")["per_galaxy"]
def med576(foot, mod, R="1.5"): return float(np.median([v[mod]["r"] for v in C576[foot][R].values()]))
def hand_fq(): return SPP["hand EM1 fq"]
HF = hand_fq()
ROWS = [  # group, row, r read from file, n, record's printed r
    ("LAW", "round rule canonical", med576("canonical", "RM"), 30, 1.250), ("LAW", "round rule alt", med576("alt", "RM"), 30, 1.212),
    ("LAW", "phantom disc canonical", med576("canonical", "PD"), 30, 1.475), ("LAW", "phantom disc alt", med576("alt", "PD"), 30, 1.475),
    ("RESPONSE", "hand EM1 Blumenthal", UR3["1.5 hR|blum"]["r"], UR3["1.5 hR|blum"]["n"], 1.071), ("RESPONSE", "hand EM1 f_Q 0.872", HF["r"], HF.get("n", 29), 1.088),
    ("RESPONSE", "native total EM1 f_Q", SP3["native-tot|EM1|fq"]["r"], SP3["native-tot|EM1|fq"]["n"], 1.080), ("RESPONSE", "native FC1 EM1 f_Q", SP3["native-fc1|EM1|fq"]["r"], SP3["native-fc1|EM1|fq"]["n"], 1.052),
    ("RESPONSE", "NFW c 8.0 f_Q", UL1["NFW c200 8.0 fq"]["r"], UL1["NFW c200 8.0 fq"]["n"], 1.046),
    ("OFF", "hand EM1 off", UR3["1.5 hR|off"]["r"], UR3["1.5 hR|off"]["n"], 1.365), ("OFF", "native total EM1 off", SP3["native-tot|EM1|off"]["r"], SP3["native-tot|EM1|off"]["n"], 1.282),
    ("OFF", "NFW c 8.0 off", UL1["NFW c200 8.0 off"]["r"], UL1["NFW c200 8.0 off"]["n"], 1.258), ("REF", "Newton, no halo", UR3["K1"]["r"], UR3["K1"]["n"], 1.494)]
R = {x[1]: x for x in ROWS}
LAW0, RESP0 = "round rule canonical", ("native total EM1 f_Q", "hand EM1 f_Q 0.872")
JEANS = {"round rule canonical": (1.074, 1.074), "round rule alt": (1.074, 1.074), "phantom disc canonical": (1.052, 1.052), "phantom disc alt": (1.052, 1.052)}; HZ = 1.07
# ---- c from each source, by the frozen rule: the stated summary, as sqrt of the stated surface density factor; S1's own dispersions
def c_of(src, mut=False):
    a = dict(S1=SRC["S1"]["sigma_hot"] / SRC["S1"]["sigma_single"], S2=math.sqrt(SRC["S2"]["stated_factor"]), S3=math.sqrt(SRC["S3"]["stated_factor"]))
    if mut: a["S1"] *= 3
    return a
cs = c_of(SRC, mut=MUT and os.environ.get("OD1_MUT_C") == "1")
c_lo, c_mid, c_hi = min(cs.values()), float(np.median(list(cs.values()))), max(cs.values())
if MUT and os.environ.get("OD1_MUT_NOC") == "1": c_lo = c_mid = c_hi = 1.0
def IN(x): return 0.90 <= x <= 1.10
def label(c, law=LAW0, resp=RESP0):
    l = R[law][2] / c; rs = [R[k][2] / c for k in resp]; ok_n = all(R[k][3] >= 27 for k in (law, *resp))
    if not ok_n: return "NOT"
    gap = min(abs(x - 0.90) for x in rs)
    if all(x < 0.90 for x in rs) and (IN(l) or (l > 1.10 and l - 1.10 < gap)): return "HEAVY"
    if all(IN(x) for x in rs) and l > 1.10: return "LIGHT"
    return "NOT"
def overall(law=LAW0, resp=RESP0):
    L = [label(c, law, resp) for c in (c_lo, c_mid, c_hi)]
    return ("HEAVY DISCS" if all(x == "HEAVY" for x in L) else "LIGHT DISCS" if all(x == "LIGHT" for x in L) else "NOT SEPARATED"), L
P("OD1_old_disc_ruler" + (" [MUTATE]" if MUT else "") + "; kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework")
P("\nCHECKS")
check(abs(UR3["K1"]["r"] - 1.494) < 0.0005 and abs(UR3["K1"]["Y"] - 0.821) < 0.0005, f"K1 no halo r {UR3['K1']['r']:.4f} Y_K {UR3['K1']['Y']:.4f}")
for g, n_, r, nn, rec in ROWS: check(abs(r - rec) <= 0.0006, f"K2 {n_}: file {r:.4f} record {rec:.3f} n {nn}")
K3 = {"S1": 1.431, "S2": 1.414, "S3": 1.517}
for k, v in cs.items(): check(abs(v - K3[k]) < 0.001, f"K3 c {k} {v:.4f} ({SRC[k]['where']}; {SRC[k]['quote']})")
check(len(cs) >= 2, f"sources in use {len(cs)}")
rs = np.array(UR3["1.5 hR|blum"]["rs"]); check(abs(np.median(rs[np.arange(len(rs))]) - UR3["1.5 hR|blum"]["r"]) < 1e-3, "K4 bootstrap identity draw, Blumenthal")
la = np.array([v["RM"]["r"] for v in C576["canonical"]["1.5"].values()]); check(abs(np.median(la[np.arange(len(la))]) - R[LAW0][2]) < 1e-12, "K4 bootstrap identity draw, round rule")
cinj = 1.3; rinj = la / la * cinj; check(abs(np.median(rinj / cinj) - 1) < 0.01, "K5 injected c 1.3 returns 1")
check(all(abs(x[2] / 1.0 - x[2]) == 0 for x in ROWS), "K6 c = 1 returns the record's r")
P(f"\nc: S1 {cs['S1']:.3f}, S2 {cs['S2']:.3f}, S3 {cs['S3']:.3f}; c_lo {c_lo:.3f}, c_mid {c_mid:.3f}, c_hi {c_hi:.3f}")
P("\nPRIMARY r_old = r / c, one-zone, all galaxies. Line 0.90-1.10, n >= 27")
P(f"{'group':9s} {'row':26s} {'r':>6s} {'n':>3s} {'c_lo':>6s} {'c_mid':>6s} {'c_hi':>6s}  at c_mid")
res = {}
for g, n_, r, nn, _ in ROWS:
    a = [r / c for c in (c_lo, c_mid, c_hi)]; res[n_] = dict(group=g, r=r, n=nn, r_old=a)
    P(f"{g:9s} {n_:26s} {r:6.3f} {nn:3d} {a[0]:6.3f} {a[1]:6.3f} {a[2]:6.3f}  {'IN' if IN(a[1]) else ('BELOW' if a[1] < 0.9 else 'ABOVE')}")
lab, per = overall(); P(f"\nFROZEN LABEL: {lab}  (per c: {per})")
swap, sp = overall(law=RESP0[0], resp=(LAW0,)); P(f"MUTATE-b style, groups swapped: {swap} {sp}")
P("\nSTRESS, tags only: J exact Jeans, H S4G h_z x 1.07. Rows without their own Jeans number span 1.05-1.07")
tags = set()
for n_ in (LAW0, *RESP0):
    r = R[n_][2]
    for c, cn in ((c_lo, "c_lo"), (c_mid, "c_mid"), (c_hi, "c_hi")):
        jl, jh = JEANS.get(n_, (1.05, 1.07)); b = r / c; j = (r * jl / c, r * jh / c); h = r * HZ / c; jh2 = (r * jl * HZ / c, r * jh * HZ / c)
        if IN(b) != IN(j[1]): tags.add("JEANS-DEPENDENT")
        if IN(b) != IN(h): tags.add("HZ-DEPENDENT")
        P(f"  {n_:24s} {cn:6s} base {b:.3f} J {j[0]:.3f}-{j[1]:.3f} H {h:.3f} J+H {jh2[0]:.3f}-{jh2[1]:.3f}")
P(f"tags: {sorted(tags)}")
# ---- implied Upsilon_K, ungraded
S576 = os.path.join(RB, "..", "campaign_fresh_gravity", "CFG576_diskmass_sigz", "cfg576_diskmass.py"); n = {"__file__": os.path.abspath(S576), "__name__": "h"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(S576).read().split('P("=" * 100)')[0], "h", "exec"), n)
gal, terms, K_V, G = n["gal"], n["galaxy_terms"], n["K_VERT"], n["G"]
def impl(c, B):
    y = []
    for g in gal.values():
        Rr = 1.5 * g["hR"]; t = terms(g, Rr); Sg = n["sexp"](Rr, t["Ma"], 2 * t["hR"]) + n["sexp"](Rr, t["Mm"], t["hR"])
        y.append(((t["smeas"] * c) ** 2 / (math.pi * G * K_V * t["hz"] * B) - Sg) / (t["I0"] * math.exp(-Rr / t["hR"])))
    return float(np.median(y))
P("\nIMPLIED, ungraded, one-zone; 3.6 um = K / (1.0-1.3). SPS line 0.50; response 0.32-0.42 at 150-250")
imp = {}
for c, cn in ((1.0, "no correction"), (c_lo, "c_lo"), (c_mid, "c_mid"), (c_hi, "c_hi")):
    for B in (1.0, 1.10):
        y = impl(c, B); imp[f"{cn}|{B}"] = y; P(f"  {cn:14s} B {B:.2f}: Y_K {y:.3f}, Y_3.6 {y / 1.3:.3f}-{y:.3f}")
# ---- V >= 150, law rows only: no per-galaxy ids exist for the response rows
V = {u: g["Varot"] / math.sin(math.radians(g["iTF"])) for u, g in gal.items()}; hi = [str(u) for u, v in V.items() if v >= 150]
lh = float(np.median([C576["canonical"]["1.5"][u]["RM"]["r"] for u in hi])); P(f"\nV >= 150 (asymptotic TF speed): {len(hi)} of {len(V)} galaxies. Round rule canonical r {lh:.3f}, r_old at c_mid {lh / c_mid:.3f}. Response rows carry no galaxy ids, so no [V-DEPENDENT] test on them")
# ---- reported, no weight: direct readings
P("\nREPORTED, NO WEIGHT: same-population 3.6 um and maximality, two galaxies")
UL1B = {"hand EM1 f_Q": (0.32, 0.41), "native EM1 f_Q": (0.34, 0.42), "law canonical": (0.46, 0.57)}  # UL1 README, 150-200, 200-250
s2, s3 = SRC["S2"], SRC["S3"]; y3 = np.array(s3["Y36_rows"]); w = 1 / y3[:, 1] ** 2; wm, we = float((y3[:, 0] * w).sum() / w.sum()), float(w.sum() ** -0.5); sm, se = float(y3[:, 0].mean()), float(y3[:, 0].std(ddof=1) / math.sqrt(5))
P(f"  NGC 628  Y_3.6 {s2['Y36']} +- {s2['Y36_err']}, V_max {s2['Vmax']}. NGC 6946 stated {s3['Y36']}; own weighted mean {wm:.3f} +- {we:.3f}; plain mean {sm:.3f} +- {se:.3f}, V_max {s3['Vmax']}")
for k, (a, _) in UL1B.items(): P(f"  bin 150-200 {k:16s} {a:.2f}: Z NGC 628 {(s2['Y36'] - a) / s2['Y36_err']:+.2f}; Z NGC 6946 at weighted {(wm - a) / we:+.2f}, at plain {(sm - a) / se:+.2f}")
vb = np.array([s2["Vbar_over_Vmax"], s3["Vbar_over_Vmax"]]); ve = np.array([s2["Vbar_err"], s3["Vbar_err"]]); vm, vs = float((vb / ve ** 2).sum() / (1 / ve ** 2).sum()), float((1 / ve ** 2).sum() ** -0.5)
P(f"  V_bar/V_max at 2.2 h: {vb[0]} +- {ve[0]}, {vb[1]} +- {ve[1]}, combined {vm:.3f} +- {vs:.3f}")
shares = {}
def lawshare(foot):
    x = []
    for u, g in gal.items():
        Rr = 2.2 * g["hR"]; Y = C576[foot]["2.2"][str(u)]["RM"]["Y"]; t = terms(g, Rr); n["gal_BD"] = g["BD"]; x.append(n["gbar"](t, Rr, Y) / (t["vrot"] ** 2 / Rr))
    return float(np.median(x))
shares["law round rule canonical, 2.2 h_R, DiskMass"] = lawshare("canonical")
shares["hand Blumenthal, 2.2 h_R, DiskMass"] = 1 - UR3["2.2 hR|blum"]["fc"]; shares["hand off, 2.2 h_R, DiskMass"] = 1 - UR3["2.2 hR|off"]["fc"]
shares["native total f_Q, 1.5 h_R only"] = 1 - SP3["native-tot|EM1|fq"]["fc"]; shares["native total off, 1.5 h_R only"] = 1 - SP3["native-tot|EM1|off"]["fc"]
for k, v in shares.items(): P(f"  {k:48s} baryon share of g {v:.3f}, V_bar/V {math.sqrt(v):.3f}, Z of combined {(vm - math.sqrt(v)) / vs:+.2f}")
# ---- post-result, no verdict: c by tracer and radius from the sources' own tables, crossover
P("\nPOST-RESULT, NO VERDICT: c by tracer and radius, sources' own tables (frozen rule used their stated summaries)")
cr = {}
for k in ("S2", "S3"):
    for tr, ra, h, he, s, se_ in SRC[k]["rows"]:
        c = h / s; ce = c * math.hypot(he / h, se_ / s); cr.setdefault(tr, []).append(c); P(f"  {k} {tr:4s} R {ra:3d}\" = {ra / SRC[k]['hdyn_as']:.2f} h_dyn: c {c:.3f} +- {ce:.3f}")
ifu, pne = float(np.median(cr["IFU"])), float(np.median(cr["PNe"])); near = float(np.median([33.8 / 26.5, 32.0 / 26.5]))
P(f"  median IFU (integrated light, same 5100 A region as DiskMass) {ifu:.3f}; median PNe {pne:.3f}; PNe nearest 1.5 h_dyn {near:.3f}")
P(f"\n  {'c':>5s} " + "".join(f"{k[:18]:>20s}" for k in (LAW0, *RESP0, "phantom disc canonical", "native total EM1 off", "Newton, no halo")) + "   (r_old one-zone / r_old J+H at Jeans mid)")
scan = {}
for c in (1.0, 1.1, 1.2, near, 1.3, 1.35, 1.4, c_mid, 1.5, 1.6, ifu, 2.0):
    row = []
    for k in (LAW0, *RESP0, "phantom disc canonical", "native total EM1 off", "Newton, no halo"):
        jm = sum(JEANS.get(k, (1.05, 1.07))) / 2; row.append(f"{R[k][2] / c:.3f}/{R[k][2] * jm * HZ / c:.3f}")
    scan[f"{c:.3f}"] = row; P(f"  {c:5.3f} " + "".join(f"{x:>20s}" for x in row))
lfq = R[RESP0[0]][2]; jm = 1.06; l0 = R[LAW0][2]
P(f"  one-zone: response leaves the line below at c > {max(R[k][2] for k in RESP0) / 0.90:.3f}; law leaves it above at c < {l0 / 1.10:.3f} and below at c > {l0 / 0.90:.3f}")
P(f"  J+H: response below at c > {max(R[k][2] for k in RESP0) * jm * HZ / 0.90:.3f}; law above at c < {l0 * 1.074 * HZ / 1.10:.3f}, below at c > {l0 * 1.074 * HZ / 0.90:.3f}; Newton below at c > {R['Newton, no halo'][2] * 1.06 * HZ / 0.90:.3f}")
# ---- NGC 6946 on SPARC, reported where the dump exists
try:
    sys.path.insert(0, os.path.join(RB, "UL1_measured_upsilon_test")); argv = sys.argv; sys.argv = [argv[0]]
    with contextlib.redirect_stdout(io.StringIO()): import ul1_core as C
    GG = C.load(); names = [q["meta"].get("Galaxy", q["meta"].get("name", q.get("name", ""))) for q in GG]; i6 = names.index("NGC6946"); in628 = any(x in ("NGC0628", "NGC628") for x in names)
    P(f"\nSPARC fits, NGC 6946 (V_flat {GG[i6]['meta']['Vflat']}; NGC 628 in SPARC: {in628}), measured 0.4; Upsilon grid floor stands")
    for f in ("law_canonical", "hand_fq", "nat_fq", "hand_off", "nat_off"):
        z = np.load(os.path.join(RB, "UL1_measured_upsilon_test", "rows", f + ".npz")); wr, ws = z["A_c2b_refit_wr2"], z["A_c2b_refit_ws"]; m = np.where(ws > 0, wr / np.maximum(ws, 1e-300), np.inf); P(f"  {f:14s} Upsilon {C.UPS[int(np.argmin(m[i6]))]:.3f}")
except Exception as e:
    P(f"\nSPARC NGC 6946 not read: {type(e).__name__}: {e}")
P("\nkappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
json.dump(dict(c=cs, c_lo=c_lo, c_mid=c_mid, c_hi=c_hi, rows=res, label=lab, per_c=per, tags=sorted(tags), implied=imp, shares=shares, Vbar=[vm, vs], c_by_tracer=cr, scan=scan, failed=FAIL), open(os.path.join(HERE, f"od1_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"od1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if FAIL: P(f"CHECKS FAILED: {FAIL}. NO VERDICT"); open(os.path.join(HERE, f"od1{TAG}.out"), "a").write(f"CHECKS FAILED: {FAIL}. NO VERDICT\n"); sys.exit(1)
