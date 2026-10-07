#!/usr/bin/env python3
r"""CFG445 SCORING -- group centrals x3 (criteria FROZEN_CRITERIA.md, a1a2a05ac; power dry-run committed before this ran).
kappa = 1/2 FITTED; both footings (CFG4_common.A0).  No dark-matter particle; the cold-fluid mass is still required.
Outputs: cfg445_score.out, cfg445_score_results.json, cfg445_residuals.csv  (MUTATE=1: *_MUTATE, residual table not rewritten)."""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg445_common as K  # noqa: E402

C = K.C
MUTATE = os.environ.get("MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
NB, NPERM, SEED = 5000, 2000, 445
OUT = open(os.path.join(HERE, f"cfg445_score{SUF}.out"), "w", encoding="utf-8")
CH, NUM = [], {}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.write(s + "\n")
    OUT.flush()


def check(name, measured, ok, lb=True):
    CH.append((name, bool(ok), lb, str(measured)))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}\n         measured: {measured}")


def jc(o):
    if isinstance(o, dict):
        return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return float(o) if np.isfinite(o) else str(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


P("=" * 118)
P(f"CFG445 group centrals x3 -- SCORING (MUTATE={int(MUTATE)}); criteria a1a2a05ac")
P("=" * 118)

# ---------------------------------------------------------------- controls on the machinery
Rd, M = 3.0, 5e10
Rs = np.linspace(0.05, 40, 800)
Sig = M / (2 * np.pi * Rd ** 2) * np.exp(-Rs / Rd) / 1e6
Rt = np.linspace(2 * Rd, 6 * Rd, 9)
rat = K.ring_sum_g(Rs, Sig, Rt) / K.freeman_g(M, Rd, Rt)
check("C-thin ring-sum vs Freeman within 2% at 2-6 R_d (test disc R_d 3 kpc, 5e10 Msun, frozen softening 0.1 kpc)",
      f"max |ratio-1| = {np.max(np.abs(rat - 1)):.4f} (at 2 R_d {rat[0]:.4f})", np.max(np.abs(rat - 1)) <= 0.02)
rat2 = K.ring_sum_g(Rs, Sig, Rt, soft=0.01) / K.freeman_g(M, Rd, Rt)
P(f"         diagnostic: with softening 0.01 kpc max |ratio-1| = {np.max(np.abs(rat2 - 1)):.4f}")

groups = K.Groups()
gal, mt = K.load_sparc_classes()
nq = sum(1 for g in gal if g["meta"] and g["meta"]["Q"] <= 2)
check("C1 load_sparc: 175 galaxies, 163 with Q <= 2", f"{len(gal)} / {nq}", len(gal) == 175 and nq == 163)
W = K.load_wallaby(groups)
for g in W:
    if not g["excl"]:
        K.wallaby_baryons(g)
dhi = [K.hi_mass_check(g) - g["logMHI_cat"] for g in W if not g["excl"] and K.n_outer(g["gbar"], g["V"]) >= 3]
check("C-HI WALLABY: 2 pi int SD_FO R dR vs source-catalogue log M_HI, median |diff| <= 0.15 dex",
      f"N {len(dhi)}, median diff {np.median(dhi):+.3f}, median |diff| {np.median(np.abs(dhi)):.3f}",
      np.median(np.abs(dhi)) <= 0.15)


def build(a0, ups=K.UPS_K, soft=K.SOFT, dkey=None, wallaby=True, sparc=True):
    rows = []
    if sparc:
        for g in gal:
            m = g["meta"]
            if not m or m["Q"] > 2 or g["name"] not in mt:
                continue
            cl = K.classify(mt[g["name"]])
            if cl is None:
                continue
            r = K.resid(g["R"], g["Vobs"], g["eV"], K.sparc_gbar(g), a0)
            if r is None:
                continue
            rows.append(dict(name=g["name"], src="SPARC", cl=cl, R=r[0], npt=r[1], logMh=mt[g["name"]]["logMh"],
                             logMd=mt[g["name"]]["logMd"], logL=math.log10(max(m["L36"], 1e-4)), rec=mt[g["name"]]))
    if wallaby:
        for g in W:
            if g["excl"]:
                continue
            D = None
            if dkey == "group":
                D = g["rec"].get("Dgrp", np.nan)
                if not np.isfinite(D):
                    D = g["rec"]["D"]
            if ups != K.UPS_K or soft != K.SOFT or D is not None:
                h = dict(g)
                K.wallaby_baryons(h, ups=ups, soft=soft, D=D)
            else:
                h = g
            cl = K.classify(h["rec"])
            r = K.resid(h["R"], h["V"], h["eV"], h["gbar"], a0, efloor=2.0)
            if r is None:
                continue
            rows.append(dict(name=g["name"], src="WALLABY", cl=cl, R=r[0], npt=r[1], logMh=h["rec"]["logMh"],
                             logMd=h["rec"]["logMd"], logL=h["logL"], rec=h["rec"]))
    return rows


def score(rows, rng, nb=NB, win=K.WIN, mcut=K.MCUT, key="logMh", mutate=False, label=""):
    A = []
    for r in rows:
        rec = dict(r["rec"])
        cl = K.classify(rec, mcut, key) if key in rec else None
        if cl in ("GC", "F"):
            A.append((r, cl))
    Rv = np.array([a[0]["R"] for a in A])
    if mutate:
        Rv = Rv + 0.1 * np.array([a[1] == "GC" for a in A])
    cls = np.array([a[1] for a in A])
    src = np.array([a[0]["src"] for a in A])
    logL = np.array([a[0]["logL"] for a in A])
    x = np.array([a[0][key] for a in A])
    D, ngu, d = K.delta_lm(Rv, cls, src, logL, win)
    bs = K.boot_lm(Rv, cls, src, logL, rng, nb, win)
    sD = float(np.nanstd(bs))
    db, fits = K.dbic_src(x, Rv, src, mcut)
    nF = int((cls == "F").sum())
    v = K.verdict(D, sD, db, ngu, nF)
    raw = float(np.median(Rv[cls == "GC"]) - np.median(Rv[cls == "F"])) if (cls == "GC").any() else float("nan")
    per = {}
    for s in ("SPARC", "WALLABY"):
        gi = np.where((cls == "GC") & (src == s))[0]
        if len(gi):
            ds, ns, _ = K.delta_lm(Rv, cls, src, logL, win, idx_gc=gi)
            per[s] = dict(nGC=int(len(gi)), nGC_used=ns, nF=int(((cls == "F") & (src == s)).sum()), Delta_LM=ds)
    return dict(label=label, nGC=int((cls == "GC").sum()), nGC_used=ngu, nF=nF, Delta_LM=D, sigma=sD,
                S=(D / sD if sD > 0 else float("nan")), dBIC=db, step_jump=fits["step"]["beta"][-1],
                slope=fits["linear"]["beta"][-1], raw_Delta=raw, per_source=per, verdict=v), (Rv, cls, src, logL)


VERD = {}
for foot in C.FOOTS:
    a0 = C.A0[foot]
    rng = np.random.default_rng(SEED)
    P("\n" + "=" * 118 + f"\nFOOTING {foot}: a0 = {a0:.4e} m/s^2 (kappa = 1/2 fitted)\n" + "=" * 118)
    rows = build(a0)
    by = {k: [r for r in rows if r["cl"] == k] for k in ("GC", "SAT", "F")}
    for s in ("SPARC", "WALLABY"):
        P(f"{s}: GC {sum(r['src'] == s for r in by['GC'])}, SAT {sum(r['src'] == s for r in by['SAT'])}, "
          f"F {sum(r['src'] == s for r in by['F'])}")
    if foot == "canonical":
        g393 = sorted(r["name"] for r in by["GC"] if r["src"] == "SPARC")
        f393 = sum(1 for r in by["F"] if r["src"] == "SPARC")
        check("C-SPARC: SPARC GC/F equal CFG393's (15 GC / 91 F)", f"{len(g393)} GC / {f393} F", len(g393) == 15 and f393 == 91)
        if not MUTATE:
            with open(os.path.join(HERE, "cfg445_residuals.csv"), "w", encoding="utf-8") as fh:
                fh.write("name,source,class,catalogue,logMh,logL,npt,R_canonical\n")
                for r in rows:
                    fh.write(f"{r['name']},{r['src']},{r['cl']},{r['rec']['cat']},{r['logMh']:.3f},{r['logL']:.3f},{r['npt']},{r['R']:+.4f}\n")
    P("  GC: " + ", ".join(f"{r['name']}({r['src'][0]},{r['logMh']:.2f},L{r['logL']:.2f},{r['R']:+.3f})"
                           for r in sorted(by["GC"], key=lambda r: -r["logMh"])))
    res, (Rv, cls, src, logL) = score(rows, rng, mutate=MUTATE, label="primary")
    P(f"(primary) Delta_LM = {res['Delta_LM']:+.4f} +- {res['sigma']:.4f} dex (S = {res['S']:+.2f}); GC used {res['nGC_used']} "
      f"of {res['nGC']}; F {res['nF']}")
    for s, v in res["per_source"].items():
        P(f"   {s}: GC {v['nGC']} (used {v['nGC_used']}), F {v['nF']}, Delta_LM {v['Delta_LM']:+.4f}")
    P(f"(secondary) unmatched pooled Delta = median(GC) - median(F) = {res['raw_Delta']:+.4f}")
    P(f"(step vs slope) dBIC(linear - step) = {res['dBIC']:+.2f}; step jump {res['step_jump']:+.4f}, slope {res['slope']:+.4f}/dex")
    P(f"VERDICT [{foot}]: {res['verdict']}")
    VERD[foot] = res["verdict"]
    out = dict(primary=res)
    # C5 permutation within source
    gcm = cls == "GC"
    perm = np.empty(NPERM)
    for k in range(NPERM):
        c2 = cls.copy()
        for s in ("SPARC", "WALLABY"):
            ii = np.where(src == s)[0]
            c2[ii] = rng.permutation(cls[ii])
        perm[k] = K.delta_lm(Rv, c2, src, logL)[0]
    pp = float(np.nanmean(np.abs(perm) >= abs(res["Delta_LM"])))
    check(f"C5 [{foot}] within-source label-permutation p for |Delta_LM|", f"p = {pp:.4f}", True, lb=False)
    out["perm_p"] = pp
    # C3 identity
    mx = 0.0
    for r in rows:
        if r["src"] == "SPARC":
            g = next(x for x in gal if x["name"] == r["name"])
            rr = K.resid(g["R"], g["Vobs"], g["eV"], K.sparc_gbar(g), a0)[0]
        else:
            g = next(x for x in W if x["name"] == r["name"])
            h = K.wallaby_baryons(dict(g))
            rr = K.resid(h["R"], h["V"], h["eV"], h["gbar"], a0, efloor=2.0)[0]
        mx = max(mx, abs(rr - r["R"]))
    if MUTATE:
        mx = max(mx, 0.1)  # the mutated R_g used differ from source by 0.1 for centrals by construction
    check(f"C3 [{foot}] every R_g used equals R_g recomputed from source (<= 1e-9 dex)", f"max |diff| = {mx:.3e}", mx <= 1e-9)
    if MUTATE:
        r0, _ = score(rows, np.random.default_rng(SEED), mutate=False, label="unmutated")
        check(f"MUT [{foot}] Delta_LM rises by 0.100 +- 0.005; verdict reaches SUPPORTED?",
              f"shift {res['Delta_LM'] - r0['Delta_LM']:+.4f}; {r0['verdict']} -> {res['verdict']}; S {res['S']:+.2f}, dBIC {res['dBIC']:+.2f}",
              abs(res["Delta_LM"] - r0["Delta_LM"] - 0.1) <= 0.005, lb=False)
        check(f"MUT [{foot}] injected +0.1 dex is DETECTED (verdict TWO-REGIME SUPPORTED)", res["verdict"],
              res["verdict"] == "TWO-REGIME SUPPORTED", lb=False)
        out["unmutated"] = r0
    # sensitivities
    if not MUTATE:
        P("-- sensitivities (reported, no verdict weight; 1,000 bootstraps)")
        sens = {}
        for lab, kw, skw in (("Upsilon_K 0.45", dict(ups=0.45), {}), ("Upsilon_K 0.80", dict(ups=0.80), {}),
                             ("mcut 12.3", {}, dict(mcut=12.3)), ("mcut 12.7", {}, dict(mcut=12.7)),
                             ("WALLABY only", dict(sparc=False), {}), ("SPARC only", dict(wallaby=False), {}),
                             ("window 0.3 dex", {}, dict(win=0.3)), ("KT2017 logMd", {}, dict(key="logMd")),
                             ("POSTHOC softening 0.01 kpc", dict(soft=0.01), {}),
                             ("POSTHOC KT2017 group distance", dict(dkey="group"), {})):
            rr = build(a0, **kw)
            sr, _ = score(rr, np.random.default_rng(SEED + 1), nb=1000, label=lab, **skw)
            sens[lab] = sr
            P(f"   {lab:30s}: GC {sr['nGC']:3d} (used {sr['nGC_used']:3d}), F {sr['nF']:3d}; Delta_LM {sr['Delta_LM']:+.4f} +- "
              f"{sr['sigma']:.4f} (S {sr['S']:+.2f}); dBIC {sr['dBIC']:+.2f}; {sr['verdict']}")
        out["sensitivities"] = sens
    NUM[foot] = out

P("\n" + "=" * 118)
fin = min(VERD.values(), key=lambda s: K.LADDER[s])
P(f"FOOTING VERDICTS: {VERD}  ->  REPORTED (weaker): {fin}")
npass = sum(1 for c in CH if c[1])
nlb = sum(1 for c in CH if not c[1] and c[2])
detect = all(c[1] for c in CH if c[0].startswith("MUT") and "DETECTED" in c[0])
P(f"\n  {npass}/{len(CH)} checks pass; load-bearing failures: {nlb}")
rc = 1 if (nlb or (MUTATE and detect)) else 0
P(f"rc = {rc}" + ("  (MUTATE: exit 1 when the injected step is detected, and C3 fails by design)" if MUTATE else ""))
json.dump(jc(dict(lane="CFG445", mutate=MUTATE, verdicts=VERD, reported=fin, numbers=NUM,
                  checks=[dict(name=c[0], ok=c[1], load_bearing=c[2], measured=c[3]) for c in CH])),
          open(os.path.join(HERE, f"cfg445_score_results{SUF}.json"), "w"), indent=1)
OUT.close()
sys.exit(rc)
