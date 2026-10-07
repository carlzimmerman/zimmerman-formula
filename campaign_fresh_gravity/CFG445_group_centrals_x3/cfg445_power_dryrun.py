#!/usr/bin/env python3
"""CFG445 POWER DRY-RUN (frozen in FROZEN_CRITERIA.md, a1a2a05ac).  Builds the REAL selection (classes, host masses, luminosities,
>= 3 rings at g_bar < 1e-10.5: g_bar only, no g_obs, no residual) and runs the frozen pipeline on MOCK residuals with +0.10 dex
injected into every central.  No real residual is computed here.  Outputs: cfg445_power_dryrun.out, _results.json,
cfg445_selection.csv (the scoring sample)."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg445_common as K  # noqa: E402

OUT = open(os.path.join(HERE, "cfg445_power_dryrun.out"), "w", encoding="utf-8")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.write(s + "\n")


P("=" * 110)
P("CFG445 POWER DRY-RUN -- selection + mock residuals only (criteria a1a2a05ac)")
P("=" * 110)
groups = K.Groups()
# ---- SPARC
gal, mt = K.load_sparc_classes()
S = []
for g in gal:
    m = g["meta"]
    if not m or m["Q"] > 2 or g["name"] not in mt:
        continue
    cl = K.classify(mt[g["name"]])
    if cl is None:
        continue
    if K.n_outer(K.sparc_gbar(g), g["Vobs"]) < 3:
        continue
    S.append(dict(name=g["name"], src="SPARC", cl=cl, logMh=mt[g["name"]]["logMh"], logL=np.log10(max(m["L36"], 1e-4)),
                  cat=mt[g["name"]]["cat"]))
P("SPARC scoring sample: " + ", ".join(f"{k} {sum(1 for s in S if s['cl'] == k)}" for k in ("GC", "SAT", "F")))
# ---- WALLABY
W = K.load_wallaby(groups)
tally = {}
for g in W:
    tally[g["excl"] or "eligible"] = tally.get(g["excl"] or "eligible", 0) + 1
P(f"WALLABY unique kinematic galaxies: {len(W)}; " + ", ".join(f"{k} {v}" for k, v in sorted(tally.items())))
nW0 = len(S)
wexcl = {}
for g in W:
    if g["excl"]:
        continue
    K.wallaby_baryons(g)
    cl = K.classify(g["rec"])
    no = K.n_outer(g["gbar"], g["V"])
    if no < 3:
        wexcl["< 3 outer rings"] = wexcl.get("< 3 outer rings", 0) + 1
        continue
    S.append(dict(name=g["name"], src="WALLABY", cl=cl, logMh=g["rec"]["logMh"], logL=g["logL"], cat=g["rec"]["cat"]))
P(f"WALLABY eligible but dropped: {wexcl}")
P("WALLABY scoring sample: " + ", ".join(f"{k} {sum(1 for s in S[nW0:] if s['cl'] == k)}" for k in ("GC", "SAT", "F")))
with open(os.path.join(HERE, "cfg445_selection.csv"), "w", encoding="utf-8") as fh:
    fh.write("name,source,class,catalogue,logMh,logL\n")
    for s in S:
        fh.write(f"{s['name']},{s['src']},{s['cl']},{s['cat']},{s['logMh']:.3f},{s['logL']:.3f}\n")
P("WALLABY centrals: " + ", ".join(f"{s['name']}({s['cat']},{s['logMh']:.2f},logL {s['logL']:.2f})" for s in S[nW0:] if s["cl"] == "GC"))

A = [s for s in S if s["cl"] in ("GC", "F")]
cls = np.array([s["cl"] for s in A])
src = np.array([s["src"] for s in A])
logL = np.array([s["logL"] for s in A])
x = np.array([s["logMh"] for s in A])
gc = np.where(cls == "GC")[0]
_, ngc_used, _ = K.delta_lm(np.zeros(len(A)), cls, src, logL)
nF = int((cls == "F").sum())
P(f"\nprimary sample: GC {len(gc)} (with a same-source field control within 0.2 dex: {ngc_used}), F {nF}")
for s in ("SPARC", "WALLABY"):
    gi = gc[src[gc] == s]
    _, nu, _ = K.delta_lm(np.zeros(len(A)), cls, src, logL, idx_gc=gi)
    P(f"  {s}: GC {len(gi)}, with controls {nu}, F {int(((cls == 'F') & (src == s)).sum())}")
SIG = {"SPARC": 0.14, "WALLABY": 0.18}
sig = np.array([SIG[s] for s in src])


def one(rng, step, nb, gc_mult=1):
    cl2, src2, L2, x2, sg2 = cls, src, logL, x, sig
    if gc_mult != 1:
        extra = rng.choice(gc, int(round((gc_mult - 1) * len(gc))))
        keep = np.concatenate([np.arange(len(A)), extra])
        cl2, src2, L2, x2, sg2 = cls[keep], src[keep], logL[keep], x[keep], sig[keep]
    R = rng.normal(0, sg2)
    R[cl2 == "GC"] += step
    D, ngu, _ = K.delta_lm(R, cl2, src2, L2)
    sD = float(np.std(K.boot_lm(R, cl2, src2, L2, rng, nb)))
    db, _ = K.dbic_src(x2, R, src2)
    return K.verdict(D, sD, db, ngu, int((cl2 == "F").sum())), D, sD, db


rng = np.random.default_rng(4450)
NM, NB = 1000, 300
res = [one(rng, 0.10, NB) for _ in range(NM)]
pw = float(np.mean([r[0] == "TWO-REGIME SUPPORTED" for r in res]))
P(f"\nMAIN: +0.10 dex injected, {NM} mocks ({NB} bootstraps each -- departure: frozen primary uses 5,000; speed):")
P(f"  power (fraction SUPPORTED) = {pw:.3f}; median Delta_LM {np.median([r[1] for r in res]):+.3f}, median sigma "
  f"{np.median([r[2] for r in res]):.3f}, median S {np.median([r[1] / r[2] for r in res]):.2f}, median dBIC "
  f"{np.median([r[3] for r in res]):+.2f}")
P(f"  fraction with S > 3: {np.mean([r[1] / r[2] > 3 for r in res]):.3f}; with dBIC > 2: {np.mean([r[3] > 2 for r in res]):.3f}")
cls_p = "POWERED" if pw >= 0.8 else ("MARGINAL" if pw >= 0.5 else "UNDERPOWERED")
P(f"  POWER CLASS: {cls_p}")
null = [one(rng, 0.0, NB) for _ in range(300)]
P(f"  null (no injection, 300 mocks): false SUPPORTED rate {np.mean([r[0] == 'TWO-REGIME SUPPORTED' for r in null]):.3f}, "
  f"NOT SUPPORTED rate {np.mean([r[0] == 'NOT SUPPORTED' for r in null]):.3f}")
scan = {}
P("\nscan (200 mocks per point, 200 bootstraps):")
for st in (0.05, 0.10, 0.15, 0.20, 0.30, 0.40):
    rr = [one(rng, st, 200) for _ in range(200)]
    scan[st] = float(np.mean([r[0] == "TWO-REGIME SUPPORTED" for r in rr]))
    P(f"  step {st:.2f} dex: power {scan[st]:.3f}  (S>3 {np.mean([r[1] / r[2] > 3 for r in rr]):.2f}, dBIC>2 {np.mean([r[3] > 2 for r in rr]):.2f})")
nsc = {}
for mlt in (2, 3, 4, 6):
    rr = [one(rng, 0.10, 200, mlt) for _ in range(200)]
    nsc[mlt] = float(np.mean([r[0] == "TWO-REGIME SUPPORTED" for r in rr]))
    P(f"  centrals x{mlt} (resampled, ~{mlt * len(gc)} GC) at 0.10 dex: power {nsc[mlt]:.3f}  "
      f"(S>3 {np.mean([r[1] / r[2] > 3 for r in rr]):.2f}, dBIC>2 {np.mean([r[3] > 2 for r in rr]):.2f})")
OUT.close()
json.dump(dict(lane="CFG445", nGC=int(len(gc)), nGC_used=int(ngc_used), nF=nF, power_0p10=pw, power_class=cls_p,
               scan={str(k): v for k, v in scan.items()}, n_scale={str(k): v for k, v in nsc.items()},
               wallaby_tally=tally, wallaby_dropped=wexcl),
          open(os.path.join(HERE, "cfg445_power_dryrun_results.json"), "w"), indent=1)
