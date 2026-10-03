#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG317 POST HOC (labelled; written after the main run; no frozen verdict depends on it).

Why: the frozen T2 (per-object Spearman of log R_need,0 against log R_ind over the satellites) PASSED (rho +0.63, p 1e-4) while T1 and T3 failed.
A pass is verified as hard as a fail.  Both quantities are expected to fall with baryonic mass for reasons unrelated to baryon loss:
  - R_need,0 is either 0 (no extra mass needed) or at least the switch-on factor R_switch = M_ph,edge / [(1 - f_b) M_b / f_b], and R_switch grows
    towards low mass (the law's own phantom per unit baryon grows);
  - R_ind follows the dwarf mass-metallicity relation.
So T2 could be a common-mass correlation.  Diagnostics (V1 canonical, the frozen primary; the other three combinations reported):
  PH1  Spearman of log R_need,0 and of log R_ind with log M_b (M_b = M* + 1.33 M_HI, the estimator's own inventory).
  PH2  partial Spearman of log R_need,0 and log R_ind controlling for log M_b (ranks residualised linearly on the rank of M_b), permutation p.
  PH3  T2 restricted to objects with R_need,0 > 1 (a positive offset at R = 1).
  PH4  a mass-only proxy in place of R_ind (-log M_b): its Spearman with log R_need,0.  If it matches T2's rho, T2 carries no information beyond mass.
  PH5  within-population Spearman (each satellite sample on its own).
  PH6  C2's frozen identity control failed on P2a (+0.0060 > 0.005 at the linearly interpolated R_need,0); a bisection on the harness locates the
       zero exactly and reports how far the interpolation was off.
Run: python3 campaign_fresh_gravity/CFG317_baryon_loss_cold_mass/cfg317_posthoc.py   (after the main run)
"""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.stats import spearmanr, rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C
R = C.Report("cfg317_posthoc", False)
R.slug = "cfg317_posthoc_POSTHOC"
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
J = json.load(open(os.path.join(HERE, "cfg317_baryon_loss_results.json")))["numbers"]
KEYS = ["ufd", "cls", "col", "m31", "fld"]
COMBOS = [("nfw", "canonical"), ("nfw", "alt"), ("sis", "canonical"), ("sis", "alt")]


def perm_p(x, y, n=10000, seed=317):
    r0 = spearmanr(x, y).correlation; rng = np.random.default_rng(seed)
    c = sum(spearmanr(x, rng.permutation(y)).correlation >= r0 - 1e-15 for _ in range(n))
    return float(r0), (c + 1) / (n + 1)


def partial(x, y, m, n=10000, seed=317):
    rx, ry, rm = rankdata(x), rankdata(y), rankdata(m)
    A = np.vstack([rm, np.ones_like(rm)]).T
    ex = rx - A @ np.linalg.lstsq(A, rx, rcond=None)[0]; ey = ry - A @ np.linalg.lstsq(A, ry, rcond=None)[0]
    r0 = float(np.corrcoef(ex, ey)[0, 1]); rng = np.random.default_rng(seed)
    c = sum(np.corrcoef(ex, rng.permutation(ey))[0, 1] >= r0 - 1e-15 for _ in range(n))
    return r0, (c + 1) / (n + 1)


def collect(prof, foot):
    xs, ys, ms, ks = [], [], [], []
    for k in KEYS:
        est = J["EST"][f"-0.2|{k}"]; need = J["OBJNEED"][f"{prof}|{foot}|{k}"]
        for o, nd in zip(est, need):
            if o is None:
                continue
            xs.append(o["lR"]); ys.append(nd); ms.append(math.log10(o["Ms"] + o["Mg"])); ks.append(k)
    return np.array(xs), np.array(ys), np.array(ms), np.array(ks)


RES = {}
for prof, foot in COMBOS:
    x, y, m, k = collect(prof, foot)
    t2 = perm_p(x, y)
    ph1 = (spearmanr(y, m).correlation, spearmanr(x, m).correlation)
    ph2 = partial(x, y, m)
    sel = y > 0
    ph3 = perm_p(x[sel], y[sel]) + (int(sel.sum()),)
    ph4 = spearmanr(-m, y).correlation
    ph5 = {kk: (float(spearmanr(x[k == kk], y[k == kk]).correlation), int((k == kk).sum())) for kk in KEYS}
    RES[f"{prof}|{foot}"] = dict(T2=t2, PH1=ph1, PH2=ph2, PH3=ph3, PH4=ph4, PH5=ph5)
    P(f"\n  -- {'V1' if prof == 'nfw' else 'V2'} {foot}: T2 rho {t2[0]:+.3f} (p {t2[1]:.4f}, n {len(x)})")
    P(f"     PH1 rho(log R_need,0, log M_b) {ph1[0]:+.3f}; rho(log R_ind, log M_b) {ph1[1]:+.3f}")
    P(f"     PH2 partial rho controlling for log M_b {ph2[0]:+.3f}, one-sided p {ph2[1]:.4f}")
    P(f"     PH3 objects with R_need,0 > 1 only: rho {ph3[0]:+.3f}, p {ph3[1]:.4f} (n {ph3[2]})")
    P(f"     PH4 mass-only proxy (-log M_b) against log R_need,0: rho {ph4:+.3f}")
    P("     PH5 within-population rho: " + "; ".join(f"{kk} {v[0]:+.2f} (n {v[1]})" for kk, v in ph5.items()))
pr = RES["nfw|canonical"]
check("PH (reported) is T2's pass more than a common-mass correlation? (V1 canonical)",
      f"T2 rho {pr['T2'][0]:+.3f}; mass-only proxy rho {pr['PH4']:+.3f}; partial rho at fixed mass {pr['PH2'][0]:+.3f} (p {pr['PH2'][1]:.4f}); "
      f"positive-offset objects only {pr['PH3'][0]:+.3f} (p {pr['PH3'][1]:.4f})", True, load_bearing=False)

# PH6 bisection for P2a on the harness (V1 canonical)
p313 = os.path.join(LANES, "CFG313_native_collapse_mass", "cfg313_native_rescore.py")
src = open(p313).read(); src = src[:src.index("MODES = {}")]
ns = {"__file__": p313, "__name__": "cfg313_prefix"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "cfg313_prefix", "exec"), ns)
FB0 = float(ns["FB0"]); SC = {"R": 1.0}
ns["mc_native"] = lambda Mb: SC["R"] * Mb / (FB0 * ns["CFG"]["fbx"])


def mk(fn):
    return lambda Ms, colour, Mb: SC["R"] * Mb / (FB0 * ns["CFG"]["fbx"])


ns["make_mc"] = mk
ns["make_floor"] = lambda: (lambda floor_mh, Mb: (floor_mh / 1e9) * SC["R"] * Mb / (FB0 * ns["CFG"]["fbx"]))


def stat(lr):
    SC["R"] = 10 ** lr
    b, _ = ns["run_mode"]("native", "nfw")
    return b["CL"][("cls", "canonical", "S")]["med"]


lr_i = J["NEED"]["nfw|canonical|P2a"]["lr0"]
lo, hi = lr_i - 0.05, lr_i + 0.05
slo, shi = stat(lo), stat(hi)
for _ in range(25):
    mid = 0.5 * (lo + hi); sm = stat(mid)
    if sm > 0:
        lo = mid
    else:
        hi = mid
check("PH6 (reported) P2a's zero crossing by bisection (V1 canonical) against the frozen linear interpolation",
      f"interpolated log R_need,0 {lr_i:.4f}; bisection {0.5 * (lo + hi):.4f} (bracket statistic {slo:+.4f} / {shi:+.4f}); difference {0.5 * (lo + hi) - lr_i:+.4f} dex "
      f"-- negligible against T3's 0.3 dex and P2a is unlabelled", True, load_bearing=False)
R.num("RES", RES); R.num("PH6", dict(interp=lr_i, bisect=0.5 * (lo + hi)))
R.write(here=HERE)
