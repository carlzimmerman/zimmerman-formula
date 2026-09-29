#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG168 main run (referee of CFG162), exactly as frozen in CFG168_FROZEN_CRITERIA.md.
    ZF_REPO=<repo> python3 cfg168_main.py > CFG168_main.out                 (rc 0 iff my own controls pass)
    CFG168_MUTATE=k python3 cfg168_main.py > CFG168_MUTATE_k.out           (rc 1 iff the control bites; M5 and M7 informational)
Independence stops at the imported CFG165 pipeline (see criteria section 1). CFG162's script/out/json are not opened by this."""
import sys
import json
import time
import math
sys.dont_write_bytecode = True
from cfg168_common import *      # noqa

t0 = time.time()
P("CFG168 main; repo = <repo>; mutate =", MUT)
S = load_S("inc_star_deg")
A = load_A()
OUT = {"mutate": MUT}
CTRL = {}

# ------------------------------------------------------------------- MUTATE set-up
MU_DEC = 0.67
anchor_mode = "pooled"
if MUT == "1":
    S = clone(S, V=S.V * 10 ** 0.3, eV=S.eV * 10 ** 0.3)
elif MUT == "3":
    anchor_mode = "none"
elif MUT == "4":
    MU_DEC = 1.5
elif MUT == "5":
    rng = np.random.default_rng(168)
    p = rng.permutation(len(S.sig))
    S = clone(S, sig=S.sig[p], esig=S.esig[p], grad2=S.grad2[p])
KW = dict(anchor_mode=anchor_mode)

# ------------------------------------------------------------------- my controls
if MUT == "0":
    # C1: alpha := 2R/R_d equals the module's own P2
    c_a = cellx(S, A, spec_alpha("two", lambda y: 2 * y), 0.67)
    c_p2 = cellx(S, A, M.spec("P2"), 0.67)
    d1 = max(abs(c_a[l]["dprime"] - c_p2[l]["dprime"]) for l in ("flat", "H"))
    CTRL["C1_alpha_2y_equals_P2"] = d1 < 1e-12
    P(f"C1 alpha=2R/Rd vs P2: max diff {d1:.2e}  {'PASS' if d1 < 1e-12 else 'FAIL'}")
    # C2: Price alpha
    y = 50.0
    a50 = float(alpha_price(y))
    ex = y + 0.5 - 1 / (8 * y)
    h = 1e-5
    yy = 7.3
    num = -(math.log(k0(yy * math.exp(h))) - math.log(k0(yy * math.exp(-h)))) / (2 * h)
    d_num = abs(float(alpha_price(yy)) - num)
    ok2 = abs(a50 - ex) < 2e-4 and d_num < 1e-6
    CTRL["C2_price_alpha"] = ok2
    P(f"C2 Price alpha(50)={a50:.7f} vs y+1/2-1/(8y)={ex:.7f} (diff {a50-ex:.2e}); numeric -dlnK0/dlny diff {d_num:.1e}  {'PASS' if ok2 else 'FAIL'}")
    # C3: README rows
    rows = {0.6: (0.058, -0.092), 1.0: (0.1441, -0.0060), 1.4: (0.211, 0.060)}
    ok3 = True
    for s, (tf, th) in rows.items():
        c = K21cell(S, A, s)
        d = max(abs(c["flat"]["dprime"] - tf), abs(c["H"]["dprime"] - th))
        ok3 &= d <= 0.005
        P(f"C3 s={s}: mine {c['flat']['dprime']:+.4f}/{c['H']['dprime']:+.4f} vs CFG160 row {tf:+.4f}/{th:+.4f}  max diff {d:.4f}")
    cp2 = cellx(S, A, M.spec("P2"), 0.67)
    dp2 = max(abs(cp2["flat"]["dprime"] - 0.390), abs(cp2["H"]["dprime"] - 0.237))
    ok3 &= dp2 <= 0.005
    P(f"C3 P2 cell: mine {cp2['flat']['dprime']:+.4f} +-{cp2['flat']['sigma']:.4f} / {cp2['H']['dprime']:+.4f} vs CFG141 +0.390/+0.237, diff {dp2:.4f}")
    CTRL["C3_rows"] = bool(ok3)
    # C4 monotone
    sg = np.arange(0, 6.0001, 0.05)
    yv = np.array([dflat_K21(S, A, s) for s in sg])
    ok4 = bool(np.all(np.diff(yv) > 0))
    CTRL["C4_monotone"] = ok4
    P(f"C4 Delta'_flat(s) strictly increasing on [0,6]: {ok4}  (values at 0, 1, 3, 6: {yv[0]:+.3f} {yv[20]:+.3f} {yv[60]:+.3f} {yv[-1]:+.3f})")
    # C5 ids and x-range
    x = S.R / S.Reff - 1
    ok5 = sorted(S.ids) == sorted(S.fdm_ids) and np.all(np.isfinite(S.V)) and x.min() >= 0 and x.max() <= 4
    CTRL["C5_ids_x"] = bool(ok5)
    P(f"C5 ids = f_DM rows: {sorted(S.ids) == sorted(S.fdm_ids)}; x range {x.min():.2f}-{x.max():.2f}: {'PASS' if ok5 else 'FAIL'}")

# ------------------------------------------------------------------- R0 power (before curves)
P("\nR0 power: (Delta'_flat - Delta'_H)/sigma at the decision cell (mu=%.2f)" % MU_DEC)
R0 = {}
for s in (0, 1, 2, 4):
    c = K21cell(S, A, s, MU_DEC, **KW)
    sm = 0.5 * (c["flat"]["sigma"] + c["H"]["sigma"])
    dd = c["flat"]["dprime"] - c["H"]["dprime"]
    R0[s] = dict(mean=dd / sm, flat=dd / c["flat"]["sigma"], H=dd / c["H"]["sigma"])
    P(f"  s={s}: sep {dd:.4f}  /mean sigma {dd/sm:.2f}   /sigma_flat {dd/c['flat']['sigma']:.2f}  /sigma_H {dd/c['H']['sigma']:.2f}")
OUT["R0"] = R0

# ------------------------------------------------------------------- H1 and crossings
P("\nDecision cell curves (mu=%.2f, delta=0, canonical):" % MU_DEC)
for s in (0, 0.25, 0.5, 0.6, 0.75, 1.0, 1.4, 2, 3, 4):
    c = K21cell(S, A, s, MU_DEC, **KW)
    P(f"  s={s:4.2f}: flat {c['flat']['dprime']:+.4f} +-{c['flat']['sigma']:.4f} ({c['flat']['z']:+.2f}s)  H {c['H']['dprime']:+.4f} +-{c['H']['sigma']:.4f} ({c['H']['z']:+.2f}s)  {M.classify(c['flat']['z'], c['H']['z'])}")
swap = (MUT == "2")
cr = crossings(S, A, mu=MU_DEC, swap=swap, **KW)
if MUT == "7":
    sg = np.arange(0, 4.0001, 0.25)
    y = np.array([(lambda r: r["flat"]["dprime"] + r["H"]["dprime"])(K21cell(S, A, s, MU_DEC, **KW)) for s in sg])
    k = np.where(np.sign(y[:-1]) * np.sign(y[1:]) < 0)[0]
    s_lin = float(sg[k[0]] - y[k[0]] * (sg[k[0] + 1] - sg[k[0]]) / (y[k[0] + 1] - y[k[0]])) if len(k) else None
    P(f"M7 grid-interpolated s_mid (step 0.25): {fmt(s_lin)} vs brentq {fmt(cr['s_mid'])}")
    cr_lin = s_lin
P(f"\nCROSSINGS (brentq): s_mid={fmt(cr['s_mid'],4)}  s_f2={fmt(cr['s_f2'],4)}  s_h2={fmt(cr['s_h2'],4)}   {'(label-swapped 2-sigma definitions)' if swap else ''}")
OUT["crossings"] = cr
H1 = cr["s_mid"] is not None
P(f"H1 (s_mid exists in [0,4]): {H1}")

# ------------------------------------------------------------------- bootstrap + gas bracket + footing (main run only)
targets = dict(s_mid=0.67, s_f2=0.73, s_h2=0.60, boot=(0.51, 0.85), gasb={0.25: 0.44, 1.5: 1.11, 4.0: 2.39}, alt=0.66,
               be_s1=(2.11, 0.62),
               place={"D&S 2010": 1.42, "P3 (fixed height)": 1.62, "Price 2022 (n=1)": 1.69, "P2 (self-grav.)": 3.00},
               own={"P0": ((-2.3, -4.6), "non-diagnostic (both outside)"), "K21": ((3.3, -0.1), "lean rival"),
                    "D&S 2010": ((4.1, 1.2), "lean rival"), "P3 (fixed height)": ((3.5, 1.3), "lean rival"),
                    "Price 2022 (n=1)": ((4.7, 1.9), "lean rival"), "P2 (self-grav.)": ((6.0, 3.7), "non-diagnostic (both outside)")},
               be_pl={"K21": (2.11, 0.62), "D&S 2010": (3.10, 1.26), "P3 (fixed height)": (3.56, 1.56), "Price 2022 (n=1)": (3.73, 1.67), "P2 (self-grav.)": (None, 3.83)},
               R0={0: 2.5, 1: 3.4, 2: 3.1, 4: 2.6})
V = {}      # verdict rows


def score(group, name, mine, target, tol):
    ok = (mine is not None) and (target is not None) and abs(mine - target) <= tol
    V.setdefault(group, []).append(dict(name=name, mine=mine, target=target, tol=tol, ok=bool(ok)))
    P(f"  [{group}] {name}: mine {fmt(mine)} target {target} line {tol}  -> {'ok' if ok else 'MISS'}")


if MUT == "0":
    P("\nBootstrap of the ten KURVS discs (anchor fixed), N=2000")
    for seed in (168, 169):
        res, none, G = bootstrap(S, A, 2000, seed)
        p = {k: pct(v) for k, v in res.items()}
        P(f"  seed {seed}: s_mid 16/50/84 = {p['s_mid'][0]:.3f}/{p['s_mid'][1]:.3f}/{p['s_mid'][2]:.3f}; no-root counts {none}; s_f2 {p['s_f2'][0]:.3f}/{p['s_f2'][1]:.3f}/{p['s_f2'][2]:.3f}; s_h2 {p['s_h2'][0]:.3f}/{p['s_h2'][1]:.3f}/{p['s_h2'][2]:.3f}")
        OUT[f"boot_{seed}"] = dict(pct=p, none=none)
        if seed == 168:
            boot168 = res["s_mid"]
            P(f"  grid-vs-brentq control on the full sample: {abs(cross_from_curves(G['s'], *curves_from(G, np.arange(10)))['s_mid'] - cr['s_mid']):.2e}")
            CTRL["C6_grid_root_vs_brentq"] = abs(cross_from_curves(G['s'], *curves_from(G, np.arange(10)))['s_mid'] - cr['s_mid']) < 1e-4
            np.save("CFG168_boot_smid_seed168.npy", np.array(boot168))
    P("  bootstrap seed 168 vs 169 percentile agreement: max |diff| = %.3f" % max(abs(a - b) for a, b in zip(OUT["boot_168"]["pct"]["s_mid"], OUT["boot_169"]["pct"]["s_mid"])))

    P("\nGas-bracket crossings (canonical, delta=0) and alt footing")
    gb = {}
    for mu in (0.25, 0.67, 1.5, 4.0):
        c = crossings(S, A, mu=mu)
        gb[mu] = c
        P(f"  mu={mu}: s_mid {fmt(c['s_mid'],3)}  s_f2 {fmt(c['s_f2'],3)}  s_h2 {fmt(c['s_h2'],3)}")
    alt = crossings(S, A, foot="alt")
    P(f"  alt footing (mu=0.67): s_mid {fmt(alt['s_mid'],3)} s_f2 {fmt(alt['s_f2'],3)} s_h2 {fmt(alt['s_h2'],3)}")
    OUT["gas_bracket"] = {str(k): v for k, v in gb.items()}
    OUT["alt"] = alt

    P("\nFull-grid verdict counts (24 cells = 4 mu x 3 delta x 2 footing)")
    counts = {}
    for s in np.arange(0, 4.0001, 0.25):
        cnt = dict(flat=0, rival=0, both_within=0, neither=0)
        for mu in MUS:
            for dl in DELS:
                for ft in FOOTS:
                    c = K21cell(S, A, s, mu, dl, ft)
                    cl = M.classify(c["flat"]["z"], c["H"]["z"])
                    if cl == "lean flat": cnt["flat"] += 1
                    elif cl == "lean rival": cnt["rival"] += 1
                    elif "within" in cl: cnt["both_within"] += 1
                    else: cnt["neither"] += 1
        counts[float(s)] = cnt
        P(f"  s={s:4.2f}: lean flat {cnt['flat']:2d}  lean rival {cnt['rival']:2d}  both within {cnt['both_within']:2d}  neither {cnt['neither']:2d}")
    OUT["counts"] = counts

    P("\nGas axis at s = 1 (60 log-spaced mu in [0.25, 4]); break-evens by brentq on continuous mu")
    mus = np.exp(np.linspace(math.log(0.25), math.log(4.0), 60))
    curve = [(float(m), K21cell(S, A, 1.0, float(m))) for m in mus]
    OUT["gas_axis_s1"] = [dict(mu=m, flat=c["flat"]["dprime"], sf=c["flat"]["sigma"], H=c["H"]["dprime"], sh=c["H"]["sigma"]) for m, c in curve]
    for m, c in curve[::10] + [curve[-1]]:
        P(f"  mu={m:5.2f}: flat {c['flat']['dprime']:+.3f} ({c['flat']['z']:+.2f}s)  H {c['H']['dprime']:+.3f} ({c['H']['z']:+.2f}s)")
    be = {}
    for law in ("flat", "H"):
        be[law] = breakeven_mu(lambda m, law=law: K21cell(S, A, 1.0, m)[law]["dprime"])
    P(f"  break-evens at s=1 (continuous root): flat {fmt(be['flat'],3)}  rival {fmt(be['H'],3)}")
    # README-style: mu grid of step 0.25 in [0.25, 4], linear interpolation of Delta'
    mg = np.arange(0.25, 4.0001, 0.25)
    for law in ("flat", "H"):
        y = np.array([K21cell(S, A, 1.0, float(m))[law]["dprime"] for m in mg])
        k = np.where(np.sign(y[:-1]) * np.sign(y[1:]) < 0)[0]
        lin = float(mg[k[0]] - y[k[0]] * 0.25 / (y[k[0] + 1] - y[k[0]])) if len(k) else None
        ylog = np.log(mg)
        logint = float(math.exp(ylog[k[0]] - y[k[0]] * (ylog[k[0] + 1] - ylog[k[0]]) / (y[k[0] + 1] - y[k[0]]))) if len(k) else None
        be[law + "_grid_lin"] = lin
        be[law + "_grid_loglin"] = logint
    P(f"  README-style step-0.25 grid, linear interpolation in mu: flat {fmt(be['flat_grid_lin'],3)} rival {fmt(be['H_grid_lin'],3)};  in log mu: flat {fmt(be['flat_grid_loglin'],3)} rival {fmt(be['H_grid_loglin'],3)}")
    OUT["breakeven_s1"] = be

    # ---------------------------------------------------------------- placements
    P("\nPlacements (s_eq: root of Delta'_flat(s K21) = Delta'_flat(prescription) at the decision cell; prescription also on the anchor)")
    place = {}
    for name, sp in PRESC.items():
        if name == "P0":
            c = K21cell(S, A, 0.0)
            seq = 0.0
        elif name == "K21":
            c = K21cell(S, A, 1.0)
            seq = 1.0
        else:
            c = cellx(S, A, sp, 0.67)
            seq = s_eq(S, A, c["flat"]["dprime"], "flat")
        cls = M.classify(c["flat"]["z"], c["H"]["z"])
        # break-evens: via s_eq K21 (README style) and direct
        via = direct = None
        if seq is not None:
            via = tuple(breakeven_mu(lambda m, law=law: K21cell(S, A, seq, m)[law]["dprime"]) for law in ("flat", "H"))
        if name not in ("P0", "K21"):
            direct = tuple(breakeven_mu(lambda m, law=law, sp=sp: cellx(S, A, sp, m)[law]["dprime"]) for law in ("flat", "H"))
        elif name == "K21":
            direct = via
        place[name] = dict(s_eq=seq, flat=(c["flat"]["dprime"], c["flat"]["sigma"], c["flat"]["z"]), H=(c["H"]["dprime"], c["H"]["sigma"], c["H"]["z"]), cls=cls, be_via=via, be_direct=direct)
        P(f"  {name:20s} s_eq {fmt(seq,3)}  flat {c['flat']['dprime']:+.3f} ({c['flat']['z']:+.2f}s) H {c['H']['dprime']:+.3f} ({c['H']['z']:+.2f}s) {cls}")
        P(f"  {'':20s} break-even flat/rival via s_eq: {tuple(fmt(v,3) for v in via) if via else None}; direct: {tuple(fmt(v,3) for v in direct) if direct else None}")
    OUT["placement"] = place

    # ---------------------------------------------------------------- verdict table vs README targets
    P("\nSCORING against the CFG162 README targets (pass lines of criteria section 3)")
    score("crossings", "s_mid", cr["s_mid"], targets["s_mid"], 0.02)
    score("crossings", "s_f2", cr["s_f2"], targets["s_f2"], 0.02)
    score("crossings", "s_h2", cr["s_h2"], targets["s_h2"], 0.02)
    pb = OUT["boot_168"]["pct"]["s_mid"]
    score("crossings", "boot 16%", pb[0], targets["boot"][0], 0.03)
    score("crossings", "boot 84%", pb[2], targets["boot"][1], 0.03)
    score("crossings", "alt footing s_mid", alt["s_mid"], targets["alt"], 0.02)
    score("gas-bracket crossings", "s_mid mu=0.25", gb[0.25]["s_mid"], targets["gasb"][0.25], 0.03)
    score("gas-bracket crossings", "s_mid mu=1.5", gb[1.5]["s_mid"], targets["gasb"][1.5], 0.03)
    score("gas-bracket crossings", "s_mid mu=4", gb[4.0]["s_mid"], targets["gasb"][4.0], 0.05)
    score("break-evens", "flat s=1 (continuous)", be["flat"], targets["be_s1"][0], 0.03)
    score("break-evens", "rival s=1 (continuous)", be["H"], targets["be_s1"][1], 0.03)
    for name in ("D&S 2010", "P3 (fixed height)", "Price 2022 (n=1)"):
        tf, th = targets["be_pl"][name]
        score("break-evens", f"{name} flat (via s_eq)", place[name]["be_via"][0], tf, 0.08)
        score("break-evens", f"{name} rival (via s_eq)", place[name]["be_via"][1], th, 0.08)
    score("break-evens", "P2 rival (via s_eq)", place["P2 (self-grav.)"]["be_via"][1], 3.83, 0.08)
    p2f = place["P2 (self-grav.)"]["be_via"][0]
    P(f"  P2 flat break-even (via s_eq) {fmt(p2f,2)}: README says >4 -> {'ok' if (p2f is None or p2f > 4) else 'MISS'}")
    V["break-evens"].append(dict(name="P2 flat > 4", mine=p2f, target=">4", tol=None, ok=bool(p2f is None or p2f > 4)))
    for name in ("D&S 2010", "P3 (fixed height)", "Price 2022 (n=1)", "P2 (self-grav.)"):
        if name in targets["place"]:
            score("placements", f"s_eq {name}", place[name]["s_eq"], targets["place"][name], 0.10 if name.startswith("P2") else 0.03)
    for name, ((tzf, tzh), tcls) in targets["own"].items():
        p_ = place[name]
        okz = abs(p_["flat"][2] - tzf) <= 0.3 and abs(p_["H"][2] - tzh) <= 0.3 and p_["cls"] == tcls
        V["placements"].append(dict(name=f"own cell {name}", mine=(round(p_["flat"][2], 2), round(p_["H"][2], 2), p_["cls"]), target=(tzf, tzh, tcls), tol=0.3, ok=bool(okz)))
        P(f"  [placements] own cell {name}: mine {p_['flat'][2]:+.2f}/{p_['H'][2]:+.2f} {p_['cls']}  target {tzf}/{tzh} {tcls} -> {'ok' if okz else 'MISS'}")
    for s, cnt in ((1.0, (14, 6)), (0.5, (4, 10))):
        c = counts[s]
        okc = abs(c["rival"] - cnt[0]) <= 1 and abs(c["flat"] - cnt[1]) <= 1
        V.setdefault("counts", []).append(dict(name=f"s={s} rival/flat", mine=(c["rival"], c["flat"]), target=cnt, ok=bool(okc)))
        P(f"  [counts] s={s}: rival {c['rival']} flat {c['flat']} target {cnt[0]}/{cnt[1]} (line 1 cell) -> {'ok' if okc else 'MISS'}")
    okhi = all(counts[s]["flat"] == 0 for s in counts if s >= 2.5)
    V["counts"].append(dict(name="no lean-flat cell for s>=2.5", mine=[counts[s]["flat"] for s in counts if s >= 2.5], target=0, ok=bool(okhi)))
    P(f"  [counts] no lean-flat cell for s >= 2.5: {okhi}")
    for s, t in targets["R0"].items():
        score("power", f"R0 s={s} (mean sigma)", R0[s]["mean"], t, 0.3)

    # ordering claims
    P("\nOrdering claims")
    ord_ = {}
    smid = {mu: gb[mu]["s_mid"] for mu in (0.67, 1.5, 4.0)}
    pl = {k: v["s_eq"] for k, v in place.items() if k not in ("P0",)}
    ok1 = all(pl[k] > smid[0.67] for k in pl)
    P(f"  O1 mu=0.67, s_mid={smid[0.67]:.3f}: " + "; ".join(f"{k} {v:.2f} (margin {v - smid[0.67]:+.2f})" for k, v in pl.items()) + f" -> all above: {ok1}")
    ok2 = pl["K21"] < smid[1.5] and all(pl[k] > smid[1.5] for k in ("D&S 2010", "P3 (fixed height)", "Price 2022 (n=1)"))
    P(f"  O2 mu=1.5, s_mid={smid[1.5]:.3f}: margins " + "; ".join(f"{k} {v - smid[1.5]:+.2f}" for k, v in pl.items()) + f" -> K21 below, D&S/P3/Price above: {ok2}")
    ok3 = all(pl[k] < smid[4.0] for k in pl if not k.startswith("P2")) and pl["P2 (self-grav.)"] > smid[4.0]
    P(f"  O3 mu=4, s_mid={smid[4.0]:.3f}: margins " + "; ".join(f"{k} {v - smid[4.0]:+.2f}" for k, v in pl.items()) + f" -> all but P2 below: {ok3}")
    marg = min(abs(pl[k] - smid[m]) for m in smid for k in pl)
    okm = (ok1 and ok2 and ok3 and marg >= 0.03)
    V["ordering"] = [dict(name="O1", ok=bool(ok1)), dict(name="O2", ok=bool(ok2)), dict(name="O3", ok=bool(ok3)), dict(name="min margin >= 0.03", mine=marg, ok=bool(marg >= 0.03))]
    kband = (0.6, 1.4)
    P(f"  K21's +-40% band {kband}: lower edge 0.6 vs s_mid(0.67) = {smid[0.67]:.3f}: the band edge is {'below' if 0.6 < smid[0.67] else 'above'} s_mid;  vs s_h2 {cr['s_h2']:.3f}")
    OUT["ordering"] = dict(O1=ok1, O2=ok2, O3=ok3, min_margin=marg, K21_band_lo_below_smid=bool(0.6 < smid[0.67]))

    P("\nVERDICT PER GROUP (REPRODUCES = all rows within lines; PARTLY = at least half; DISAGREES = fewer)")
    for g, rows in V.items():
        n_ok = sum(r["ok"] for r in rows)
        v = "REPRODUCES" if n_ok == len(rows) else ("PARTLY" if n_ok * 2 >= len(rows) else "DISAGREES")
        P(f"  {g:24s} {n_ok}/{len(rows)}  {v}")
    OUT["verdict_rows"] = V

OUT["controls"] = CTRL

# ------------------------------------------------------------------- MUTATE outcomes
rc = 0
if MUT == "0":
    rc = 0 if all(CTRL.values()) else 1
    P("\nmy controls:", CTRL, "-> exit", rc)
else:
    bites = False
    if MUT == "1":
        P("\nM1: velocities x 10^0.3. Delta'_flat at s=0,1,4:", [round(K21cell(S, A, s, MU_DEC)["flat"]["dprime"], 3) for s in (0, 1, 4)])
        bites = not H1
        P("M1 s_mid exists:", H1, "-> bites (H1 fails)" if bites else "-> DOES NOT BITE")
    elif MUT == "2":
        base = crossings(S, A)
        P(f"M2: label-swapped 2-sigma crossings. s_mid {fmt(cr['s_mid'],3)} (unswapped {fmt(base['s_mid'],3)}), s_f2 {fmt(cr['s_f2'],3)} (unswapped {fmt(base['s_f2'],3)}), s_h2 {fmt(cr['s_h2'],3)} (unswapped {fmt(base['s_h2'],3)})")
        bites = (cr["s_f2"] is None or abs(cr["s_f2"] - base["s_f2"]) > 0.3) or (cr["s_h2"] is None or abs(cr["s_h2"] - base["s_h2"]) > 0.3)
        P("M2 s_mid unchanged (label-symmetric):", abs(cr["s_mid"] - base["s_mid"]) < 1e-9, "; 2-sigma headline bites:", bites)
    elif MUT == "3":
        base = crossings(S, load_A())
        P(f"M3: anchor removed. s_mid {fmt(cr['s_mid'],3)} vs {fmt(base['s_mid'],3)}")
        bites = cr["s_mid"] is None or abs(cr["s_mid"] - base["s_mid"]) > 0.2
    elif MUT == "4":
        P(f"M4: decision cell at mu=1.5: s_mid {fmt(cr['s_mid'],3)} (README 1.11)")
        bites = cr["s_mid"] is None or abs(cr["s_mid"] - 0.669) > 0.2
    elif MUT == "5":
        P(f"M5 (informational): sigma_out permuted seed 168: s_mid {fmt(cr['s_mid'],3)} vs 0.669")
        bites = cr["s_mid"] is None or abs(cr["s_mid"] - 0.669) > 0.05
    elif MUT == "6":
        c0 = cellx(S, A, PRESC["Price 2022 (n=1)"], 0.67)
        s_p0 = s_eq(S, A, c0["flat"]["dprime"], "flat")
        spy = spec_alpha("Pricemut", lambda y: y)
        cy = cellx(S, A, spy, 0.67)
        s_py = s_eq(S, A, cy["flat"]["dprime"], "flat")
        spn = spec_alpha("DSneg", lambda y: -0.92 * y)
        cn = cellx(S, A, spn, 0.67)
        s_dn = s_eq(S, A, cn["flat"]["dprime"], "flat")
        P(f"M6(i) Price alpha=y: s_eq {fmt(s_py,3)} vs correct {fmt(s_p0,3)}; M6(ii) D&S sign flipped: Delta'_flat {cn['flat']['dprime']:+.3f}, s_eq {fmt(s_dn,3)} (None = unplaced)")
        bites = (s_py is None or abs(s_py - s_p0) > 0.03) or s_dn is None
    elif MUT == "7":
        bites = abs(cr_lin - cr["s_mid"]) > 0.02
        P(f"M7 (informational): |grid - root| = {abs(cr_lin - cr['s_mid']):.4f}")
    rc = 1 if bites else 0
    P(f"MUTATE {MUT}: {'BITES' if bites else 'DOES NOT BITE'} -> exit {rc}")

fn = "CFG168_main_results.json" if MUT == "0" else f"CFG168_MUTATE_{MUT}_results.json"
with open(fn, "w") as f:
    json.dump(OUT, f, indent=1, default=lambda o: None if o is None else (float(o) if isinstance(o, (np.floating,)) else str(o)))
P(f"\nsaved {fn}; runtime {time.time()-t0:.1f}s")
sys.exit(rc)
