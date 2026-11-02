#!/usr/bin/env python3
"""BF2 steps 4, 5: Bullet on UX6's map under three readings of f, MG1's pair rows, Saturn. kappa = 1/2 FITTED; not theory closed. Reinstates nothing."""
import importlib.util as iu, io, json, math, os, sys
from bf2_common import *
OUT = open(os.path.join(LANE, f"bf2_bullet{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
CK = {}
def check(n, ok, d): CK[n] = bool(ok); say(f"[{'PASS' if ok else 'FAIL'}] {n}: {d}")
scan = json.load(open(os.path.join(LANE, "bf2_scan.json")))["selection"]; FORMS = {t: (v["s"], v["w"]) for t, v in scan.items() if v}
FORMS.update({t: (v["s"], v["w"]) for t, v in json.load(open(os.path.join(LANE, "bf2_amend.json"))).items()})
if MUT: FORMS = {}
# UX6's code, prefix only, its output diverted
p = os.path.join(RB, "UX6_gas_term_bullet", "ux6_bullet.py"); s = open(p).read().split('say("=" * 90); say("UX6')[0]; a = 'OUT = open(os.path.join(HERE, f"ux6_bullet{TAG}.out"), "w")'; assert s.count(a) == 1; s = s.replace(a, "import io as _io; OUT = _io.StringIO()"); U = {"__file__": p, "__name__": "b"}; exec(compile(s, p, "exec"), U)
SYS = U["SYS"]; GAS, GAL = U["GAS"], U["GAL"]; UX = json.load(open(os.path.join(RB, "UX6_gas_term_bullet", "ux6_results.json")))
def rho(comps, X, Y, Z):
    o = 0.0
    for M, a_, x, y in comps: o = o + 3 * M / (4 * math.pi * a_ ** 3) * (1 + ((X - x) ** 2 + (Y - y) ** 2 + Z ** 2) / a_ ** 2) ** -2.5
    return o
def extra(sp, C, reg=True):
    a0, form, sc = sp["a0"], sp["form"], sp.get("scale", 1.0); gv = tuple(sc * sum(q[i] for q in C["gas"]) for i in range(3)); gb = [gv[i] + C["st"][i] for i in range(3)]
    if reg: gb[1] = gb[1] + a0 / 1000.0
    g = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2); gs_ = np.maximum(g, 1e-300); L = law(g, a0); y = gs_ / a0; ex, w = sp.get("expr"), sp.get("w", 3)
    if form == "LAW": return tuple(gb[i] * (L / gs_ - 1) for i in range(3))
    if form == "UX3":  # K5: 1 + k f y, unclipped
        gg = np.sqrt(gv[0] ** 2 + gv[1] ** 2 + gv[2] ** 2); return tuple(gb[i] * (L * (1 + sp["k"] * (gg / gs_) * y) / gs_ - 1) for i in range(3))
    if form in ("Fa", "Fc"):
        if form == "Fa": f = np.clip(np.sqrt(gv[0] ** 2 + gv[1] ** 2 + gv[2] ** 2) / gs_, 0, 1)
        else:
            rg = np.maximum(sc * rho(GAS, C["X"], C["Y"], C["Z"]), 0.0); f = np.clip(rg / np.maximum(rg + rho(GAL, C["X"], C["Y"], C["Z"]), 1e-300), 0, 1)
        T = wrap(w, gs_, a0, H_of(ex, y, y * 0, f)); return tuple(gb[i] * (T / gs_ - 1) for i in range(3))
    out = [gb[i] * (L / gs_ - 1) for i in range(3)]; key = "N1" if form == "Fb" else "N2"
    for ctr, lr, tg, tb in SYS.tab[key]:
        dx = C["X"] - ctr[0]; dy = C["Y"] - ctr[1]; dz = C["Z"]; rr = np.maximum(np.sqrt(dx * dx + dy * dy + dz * dz), .5); q = np.log(rr); gg_ = np.interp(q, lr, tg); gt = np.maximum(np.interp(q, lr, tb), 1e-300); f = np.clip(gg_ / gt, 0, 1); ft = -(wrap(w, gt, a0, H_of(ex, gt / a0, gt * 0, f)) - law(gt, a0)) / rr
        out[0] = out[0] + ft * dx; out[1] = out[1] + ft * dy; out[2] = out[2] + ft * dz
    return tuple(out)
SYS.extra = extra; SP = {}
for ft in FEET:
    a0 = A0[ft]; SP[f"LAW|{ft}"] = dict(form="LAW", a0=a0, scale=2.0 if MUT else 1.0); SP[f"UX3|{ft}"] = dict(form="UX3", k=U["KFIT"][ft], a0=a0)
    for t, (ex, w) in FORMS.items():
        for F in ("Fa", "Fb", "Fb2", "Fc"): SP[f"{t}|{F}|{ft}"] = dict(form=F, expr=ex, w=w, a0=a0)
    for sc in ((.8, 1.2) if not MUT else ()): SP[f"P1|Fa|{ft}|gas{sc}"] = dict(form="Fa", expr=FORMS["P1"][0], w=FORMS["P1"][1], a0=a0, scale=sc); SP[f"P2|Fa|{ft}|gas{sc}"] = dict(form="Fa", expr=FORMS["P2"][0], w=FORMS["P2"][1], a0=a0, scale=sc)
# ell is not given: a Bullet cell with an ell form gets ell = 0, flagged in the README if any selected form reads it
for t, (ex, w) in FORMS.items(): say(f"{t}: W{w} {ex}; reads ell {'ell' in uses(ex)}")
R = U["run"](SP); O = {n: U["observe"](*R[n]) for n in SP}
for ft in FEET:
    r = UX["rows"][f"LAW|{ft}"]; o = O[f"LAW|{ft}"]; check(f"K5 LAW {ft}", max(abs(o["M300"][i] * 1.0 / r["M300"][i] - 1) for i in (0, 1)) < 1e-6, f"{o['M300']} vs {r['M300']}")
    r = UX["rows"][f"L1|{ft}|fit"]; o = O[f"UX3|{ft}"]; check(f"K5 L1 {ft}", max(abs(o["M300"][i] / r["M300"][i] - 1) for i in (0, 1)) < 1e-3 and abs(o["sub"]["dkappa"] / r["sub"]["dkappa"] - 1) < 1e-3, f"{o['M300']}, {o['sub']['dkappa']:+.3f} vs {r['M300']}, {r['sub']['dkappa']:+.3f}")
say("\nspec | main peak d_gas d_bcg Z lm | sub | dkappa m s | M300 (Z) | ratio | cls")
for n, o in O.items():
    a_, b = o["main"], o["sub"]; say(f"{n:24s} {a_['d_gas']:4.0f} {a_['d_bcg']:4.0f} {a_['Z']:+.2f} lm{int(a_['local_max'])} | {b['d_gas']:4.0f} {b['d_bcg']:4.0f} {b['Z']:+.2f} lm{int(b['local_max'])} | {a_['dkappa']:+.3f} {b['dkappa']:+.3f} | {o['M300'][0] / 1e14:.2f} ({o['ZO3'][0]:+.1f}) {o['M300'][1] / 1e14:.2f} ({o['ZO3'][1]:+.1f}) | {o['ratio']:.2f} | {o['cls']} | kmax {o['kappa_max']:.2f} {o['top'][:2]}")
LAB = {}
say("\nlabels, UX6's rule over both footings")
for t in FORMS:
    for F in ("Fa", "Fb", "Fb2", "Fc"):
        c = [O[f"{t}|{F}|{ft}"] for ft in FEET]; l = "DEAD" if all(x["pos_or_sign_fail"] for x in c) else "ALIVE" if all(x["cls"] == "PASS" for x in c) else "WOUNDED" if all(not x["pos_or_sign_fail"] for x in c) else "MIXED"; LAB[f"{t}|{F}"] = l; say(f"  {t} {F}: {l}; cells {[x['cls'] for x in c]}")
# ---------- MG1 pair model
pm = os.path.join(RB, "MG1_merger_sample", "mg1_merger.py"); sm = open(pm).read(); a = 'OUT = open(os.path.join(HERE, f"mg1_merger{TAG}.out"), "w")'; assert sm.count(a) == 1; cut = sm.index('say("=" * 90); say("MG1'); pref = sm[:cut].replace(a, "import io as _io; OUT = _io.StringIO()"); M = {"__file__": pm, "__name__": "m"}; exec(compile(pref, pm, "exec"), M)
MR = json.load(open(os.path.join(RB, "MG1_merger_sample", "mg1_results.json"))); OBS = MR["obs"]; OLDL = M["law"]
def mextra(form, k, a0, gas, star, s_, C, tabs, reg=True):
    gv, st = C["g"], C["st"]; gb = [gv[i] + st[i] for i in range(3)]
    if reg: gb[1] = gb[1] + a0 / 1000.0
    g = np.maximum(np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2), 1e-300); L = OLDL(g, a0)
    if form == "LAW": return tuple(gb[i] * (L / g - 1) for i in range(3))
    F, t = form; ex, w = FORMS[t]
    if F == "Fa":
        f = np.clip(np.sqrt(gv[0] ** 2 + gv[1] ** 2 + gv[2] ** 2) / g, 0, 1); T = wrap(w, g, a0, H_of(ex, g / a0, g * 0, f)); return tuple(gb[i] * (T / g - 1) for i in range(3))
    out = [gb[i] * (L / g - 1) for i in range(3)]; lr, tg, tb = tabs["N1" if F == "Fb" else "N2"]; dx = C["X"] - s_; dy = C["Y"]; dz = C["Z"]; rr = np.maximum(np.sqrt(dx * dx + dy * dy + dz * dz), .5); q = np.log(rr); gt = np.maximum(np.interp(q, lr, tb), 1e-300); f = np.clip(np.interp(q, lr, tg) / gt, 0, 1); ft = -(wrap(w, gt, a0, H_of(ex, gt / a0, gt * 0, f)) - OLDL(gt, a0)) / rr
    return (out[0] + ft * dx, out[1] + ft * dy, out[2] + ft * dz)
M["extra"] = mextra
import csv as _csv
rows = M.get("rows"); say(f"\nMG1 table rows found in prefix: {len(rows) if rows else 0}")
MD = {}
if rows and not MUT:
    for r in rows:
        tag = f"{r['system']} {r['sub']}"
        if tag not in OBS or not (OBS[tag].get("counted") and OBS[tag].get("s_over_row", 0) > 2): continue
        sp = {}
        for ft in FEET:
            sp[f"LAW|{ft}"] = ("LAW", 0, A0[ft])
            for t in FORMS:
                for F in ("Fa", "Fb", "Fb2"): sp[f"{t}|{F}|{ft}"] = ((F, t), 0, A0[ft])
        MD[tag], _ = M["run_pair"]((r["M_gas"], r["a_gas"]), (r["M_star"], r["a_star"]), r["s"], sp); say(f"  {tag:20s} obs {OBS[tag]['label']:8s} " + " ".join(f"{k}:{MD[tag][f'{k}|canonical']['dkappa']:+.2f}" for k in ("LAW", "P3|Fa", "P7|Fa", "P8|Fa", "P3|Fb2", "P7|Fb2", "P8|Fb2")))
    VER = {}
    for ft in FEET:
        for t in FORMS:
            for F in ("Fa", "Fb", "Fb2"):
                hit = {n: MD[n][f"{t}|{F}|{ft}"]["dkappa"] for n in MD}; bad = [n for n, d in hit.items() if OBS[n]["label"] == "GAL" and d <= 0]; ss = {OBS[n]["system"] for n in bad}; sysall = {OBS[n]["system"] for n in hit}; v = "INSUFFICIENT" if len(sysall) < 3 else ("DEAD IN GENERAL" if len(ss) >= 3 and len(bad) / len(hit) >= 2 / 3 else "NOT GENERALISED"); VER[f"{t}|{F}|{ft}"] = dict(v=v, wrong=len(bad), n=len(hit), sys=len(ss)); say(f"  {t} {F} {ft}: {v}; GAL with dkappa <= 0: {len(bad)} of {len(hit)} in {len(ss)} systems")
else: VER = {}
# ---------- Saturn
T = json.load(open(os.path.join(RQ3, "tolerances.json")))["PLANETS"]["Saturn"]; AU = 149597870700.0; GMs = 1.32712440018e20; r_ = T["a_au"] * AU; gN = GMs / r_ ** 2; sig = T["dg_tight"] * max(T["EPM"], T["INPOP"]) / min(T["EPM"], T["INPOP"]); SAT = {}
for ft in FEET:
    a0 = A0[ft]; v = np.array([gN]); SAT[f"law|{ft}"] = dict(anom=float(abs(law(v, a0)[0] - gN)), Z=float(abs(law(v, a0)[0] - gN) / sig)); say(f"\nSaturn {ft}: gN {gN:.4e}, y {gN / a0:.3e}, sigma {sig:.3e}; law anomaly {SAT[f'law|{ft}']['anom']:.3e}, Z {SAT[f'law|{ft}']['Z']:.3e}")
    for t, (ex, w) in FORMS.items():
        for f0 in (0.0, 1.0):
            H = H_of(ex, v / a0, v * 0 + r_ * a0 / C ** 2, v * 0 + f0); gp = wrap(w, v, a0, H)[0]; SAT[f"{t}|{ft}|f{f0:g}"] = dict(H=float(H[0]), anom=float(abs(gp - gN)), Z=float(abs(gp - gN) / sig), rel=float(gp / gN - 1)); say(f"  {t} f={f0:g}: H {H[0]:.6g}, g/gN-1 {gp / gN - 1:+.3e}, Z {abs(gp - gN) / sig:.3e}")
json.dump(dict(checks=CK, rows=O, labels=LAB, mg1=MD, mg1_verdicts=VER, saturn=SAT), open(os.path.join(LANE, f"bf2_bullet{TAG}.json"), "w"), indent=0, sort_keys=True, default=float); say(f"failed checks {[k for k, v in CK.items() if not v]}"); OUT.close()
if MUT: sys.exit(1)
