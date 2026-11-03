#!/usr/bin/env python3
"""BF3 K1, K2, K3: exact path against RQ3's law row and BF2's P3, P7; cheap against exact. Exit 1 on a failure. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys, time
from bf3_common import *
OUT = open(os.path.join(LANE, f"bf3_k1{TAG}.out"), "w"); CH = {}; RES = {}
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
def check(n, ok, d): CH[n] = bool(ok); say(f"[{'PASS' if ok else 'FAIL'}] {n}: {d}")
BF2 = os.path.join(RB, "BF2_near_miss_family", "results")
def cheap(R, Hf, w):
    a = R.a0; H = Hf(R.y, R.ell, R.f); bl = wrap(w, R.gbL, a, H[R.sL]) / R.gbL; c = float(((R.yw - R.Mw @ bl) ** 2).sum()); o = dict(chi=c)
    for k, sl in zip(GF, (R.sG0, R.sG1)):
        b = (wrap(w, R.gbG, a, H[sl]) / R.gbG).reshape(63, -1); o[str(k)] = float(-(R.ls - (.5 * np.log10((b * R.W).sum(1)) - 3)).mean())
    return o
P3 = "(inv1p((sqrt(f)/(pi*y)))*sq(((f+0.5)*(f+2.0))))"
FORMS = {"law": ("1.0", "H", 3, "law"), "P3": (None, "H", 2, "P3"), "P7": (None, "H", 2, "P7")}
import re
for t in ("P3", "P7", "P8"):
    src = open(os.path.join(RB, "BF2_near_miss_family", "candidates", t + ".py")).read(); FORMS[t] = (re.search(r"EXPR = '([^']+)'", src).group(1), "H", int(re.search(r"WRAP = (\d)", src).group(1)), t)
t0 = time.time()
for ft in FEET:
    E = Exact(ft); R = Rows(ft); RES[ft] = {}; rf = {t: json.load(open(os.path.join(BF2, f"{t}.json")))["footings"][ft]["rows"] for t in ("law", "P3", "P7", "P8")}
    for t, (s, fam, w, _) in FORMS.items():
        Hf = form_fn(s, fam); o = E.all(Hf, w); ch = cheap(R, Hf, w); RES[ft][t] = dict(exact=o, cheap=ch); r = rf[t]; say(f"{ft} {t}: A30 cov {o['lens']['cov']:.3f} (RQ3 {r['A30']['value']:.3f}) sys {o['lens']['sys']:.2f} sys b=0 {o['lens']['sys_b0']:.2f} | cheap sys lower bound {ch['chi']:.2f} | B1-style f.6 {o['G']['0.6']['v']:+.4f} Z {o['G']['0.6']['Z']:+.2f} f.3 Z {o['G']['0.3']['Z']:+.2f} f.85 Z {o['G']['0.85']['Z']:+.2f} cheap {ch['0.6']:+.4f},{ch['0.3']:+.4f} | X {o['X']['mean']:+.4f} Z {o['X']['Z']:+.2f} scatter {o['X']['scatter']:.3f} rms {o['X']['rms']:.3f} (RQ3 B23 {r['B23']['value']:+.4f}) | S rms {o['S']['rms']:.4f} U {o['S']['U']:.2f} tilt {o['S']['tilt']:+.3f} (RQ3 {r['A1']['value']:.4f},{r['A2']['value']:.2f})")
        tol = 1e-3 if t == "law" else .05
        check(f"K{'1' if t == 'law' else '2'} {ft} {t} A30", abs(o["lens"]["cov"] - r["A30"]["value"]) <= tol, f"{o['lens']['cov']:.4f} vs {r['A30']['value']:.4f}")
        check(f"K{'1' if t == 'law' else '2'} {ft} {t} X", abs(o["X"]["mean"] - r["B23"]["value"]) <= 1e-3, f"{o['X']['mean']:+.5f} vs {r['B23']['value']:+.5f}")
        check(f"K{'1' if t == 'law' else '2'} {ft} {t} S", abs(o["S"]["rms"] - r["A1"]["value"]) <= 1e-3 and abs(o["S"]["U"] - r["A2"]["value"]) <= .005, f"{o['S']['rms']:.5f} {o['S']['U']:.2f} vs {r['A1']['value']:.5f} {r['A2']['value']:.2f}")
        if t == "law":
            check(f"K1 {ft} law B1", abs(o["G"]["0.6"]["v"] - r["B1"]["value"]) <= 1e-3, f"{o['G']['0.6']['v']:+.5f} vs {r['B1']['value']:+.5f}")
    # K3: cheap against exact on 50 frozen random forms, plus above
    d, n = pool(ft, "real")[:2]; rng = np.random.default_rng(20261102); pick = rng.choice(len(d["names"]), 50, replace=False); dl, dg, nb = [], [], 0
    for i in pick:
        s = d["names"][i]; Hf = form_fn(s, "A"); w = int(rng.integers(1, 4)); ch = cheap(R, Hf, w)
        if not np.isfinite(ch["chi"]) or not np.isfinite(ch['0.6']): nb += 1; continue
        m = E.lens_model(Hf, w)
        if not np.isfinite(m).all(): nb += 1; continue
        dl.append((ch["chi"], E.chi(m, E.Yn, E.Csys)[0])); dg.append((ch['0.6'], E.groups(Hf, w, .6)["v"]))
    dl = np.array(dl); dg = np.array(dg); near = dl[:, 1] < 400; RES[ft]["K3"] = dict(lens=dl.tolist(), groups=dg.tolist(), nonfinite=nb)
    say(f"K3 {ft}: {len(dl)} random forms, {nb} non-finite; cheap/exact lens ratio median {np.median(dl[:, 0] / dl[:, 1]):.3f} max {np.max(dl[:, 0] / dl[:, 1]):.3f}; among exact < 400 (n {near.sum()}): max ratio {np.max(dl[near, 0] / dl[near, 1]) if near.any() else float('nan'):.3f}; groups |cheap - exact| median {np.nanmedian(np.abs(dg[:, 0] - dg[:, 1])):.4f} max {np.nanmax(np.abs(dg[:, 0] - dg[:, 1])):.4f}")
    say(f"   wall {time.time() - t0:.0f} s")
json.dump(dict(checks=CH, res=RES), open(os.path.join(LANE, f"bf3_k1{TAG}.json"), "w"), indent=0, sort_keys=True, default=float)
say(f"failed checks: {[k for k, v in CH.items() if not v]}"); OUT.close(); sys.exit(1 if MUT or not all(CH.values()) else 0)
