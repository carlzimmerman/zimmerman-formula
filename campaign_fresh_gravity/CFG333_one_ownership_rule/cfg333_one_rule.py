#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG333 -- is there ONE ownership rule (which MW subsystems are OWNED = internally Newtonian, which TOP-LEVEL = isolated law)
that gets wide binaries, outer-halo globulars, classical dwarfs and ultra-faint dwarfs right at once?  See FROZEN_CRITERIA.md.

kappa = 1/2 FITTED and fixed; both footings; kernel nu_mono; on-disk inputs only; no fitting, no scans.
Run:     python3 campaign_fresh_gravity/CFG333_one_ownership_rule/cfg333_one_rule.py
MUTATE:  CFG333_MUTATE=1 python3 ...   (class labels permuted across systems; writes *_MUTATE.* outputs)
"""
import os, sys, csv, math, json
import numpy as np
from scipy.stats import chi2 as chi2dist, norm

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, LANES)
import CFG7_common as C                                                     # noqa: E402  (nu_mono, the adopted kernel)

MUTATE = os.environ.get("CFG333_MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = []


def P(s=""):
    print(s); OUT.append(s)


CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok))); P(f"   [{'PASS' if ok else 'FAIL'}] {name}  ({detail})")


G, MSUN, PC, KPC, AU = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19, 1.495978707e11
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
FOOTS = list(A0)
MW_MB = 6.0e10
FB = 0.157126                                       # CFG35 / CFG313 native cosmic baryon fraction
GEXT_SUN = 1.778e-10                                # prereg's banked solar-neighbourhood g_ext,obs
R0_KPC = 8.2
WB_Y, WB_M = 0.3, 1.5
WB_OBS = {"canonical": (1.0750, 0.0550), "alt": (1.0775, 0.0512)}   # DRY_RUN_2026-10-03 builder build


def nu_m(y):
    return float(C.nu_mono(np.array([max(float(y), 1e-14)]))[0])


def nu_s(y):
    y = max(float(y), 1e-12); return 1.0 / (1.0 - math.exp(-math.sqrt(y)))


def g_host(D_kpc, a0, Mh=MW_MB):
    gN = G * Mh * MSUN / (D_kpc * KPC) ** 2
    return nu_m(gN / a0) * gN


def g_int_law(Mb, r12_m, a0):
    gN = G * 0.5 * Mb * MSUN / r12_m ** 2
    return nu_m(gN / a0) * gN


def classify(rule, kind, g_int, g_tide, g_ext):
    """returns 'top' or 'own'"""
    if rule == "R0":
        return "top"
    if rule == "R1":
        return "top" if g_int > g_tide else "own"
    if rule == "R2":
        return "top" if kind in ("CL", "UFD") else "own"
    if rule == "R3":
        return "own" if g_int < g_ext else "top"
    raise ValueError(rule)


# ============================================================================ dwarfs (AUDIT_UFD estimator, LVD MW table)
def fnum(v):
    try:
        x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None


rows = list(csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv"))))
UFD_R, UFD_U, CL = [], [], []
for r in rows:
    MV = fnum(r["M_V"]); sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
    Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if MV is None or rh is None:
        continue
    d = dict(name=r["name"], host=r["host"], MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, Dgc=fnum(r["distance_gc"]) or Dh,
             MHI=(10 ** fnum(r["mass_HI"]) if fnum(r["mass_HI"]) is not None else 0.0))
    if MV > -7.7:
        if Dh is None:
            continue
        if sig is not None and ul is None and sig > 0:
            d["sig"] = sig; UFD_R.append(d)
        elif ul is not None:
            d["sig_ul"] = ul; UFD_U.append(d)
    else:
        if sig is not None and sig > 0:
            d["sig"] = sig; CL.append(d)


def sig_dwarf(d, foot, cls, ups=2.0, cold=True):
    a0 = A0[foot]; Mb = ups * d["LV"] + 1.33 * d["MHI"]; r = (4.0 / 3.0) * d["rh"] * PC
    if cls == "top":
        g = g_int_law(Mb, r, a0)                          # CFG313: native cold mass inert -> bare law
    else:
        M = Mb / FB if cold else Mb                       # owned: Newton on M_b/f_b (primary) or stars only
        g = G * 0.5 * M * MSUN / r ** 2
    return math.sqrt(g * r / 3.0) / 1e3


def km_median(x, xu):
    y = np.concatenate([-np.asarray(x), -np.asarray(xu)]); ev = np.concatenate([np.ones(len(x), bool), np.zeros(len(xu), bool)])
    o = np.lexsort((~ev, y)); y, ev = y[o], ev[o]
    S, n, i = 1.0, len(y), 0
    while i < len(y):
        t = y[i]; j = i; dd = 0; cc = 0
        while j < len(y) and y[j] == t:
            dd += int(ev[j]); cc += int(not ev[j]); j += 1
        if dd:
            S *= 1.0 - dd / n
            if S <= 0.5:
                return -t
        n -= dd + cc; i = j
    return -y[-1]


def dwarf_stat(kind, foot, lab, cold=True):
    """lab: dict name -> 'top'/'own'.  UFD: KM median with ULs; CL: plain median.  error = boot(1000, seed 42) (+) half Ups 1-4 shift."""
    def offs(ups):
        if kind == "UFD":
            x = np.array([math.log10(d["sig"] / sig_dwarf(d, foot, lab[d["name"]], ups, cold)) for d in UFD_R])
            xu = np.array([math.log10(d["sig_ul"] / sig_dwarf(d, foot, lab[d["name"]], ups, cold)) for d in UFD_U])
            return x, xu
        return np.array([math.log10(d["sig"] / sig_dwarf(d, foot, lab[d["name"]], ups, cold)) for d in CL]), np.array([])
    med = (lambda x, xu: km_median(x, xu)) if kind == "UFD" else (lambda x, xu: float(np.median(x)))
    x, xu = offs(2.0); m = med(x, xu)
    rng = np.random.default_rng(42); v = []
    for _ in range(1000):
        xb = x[rng.integers(0, len(x), len(x))]
        xub = xu[rng.integers(0, len(xu), len(xu))] if len(xu) else xu
        v.append(med(xb, xub))
    e = float(np.std(v)); f = 0.5 * abs(med(*offs(4.0)) - med(*offs(1.0))); tot = math.hypot(e, f)
    return dict(m=float(m), boot=e, floor=f, err=tot, z=float(m / tot))


# ============================================================================ globulars (h93 inputs and estimator)
GCDIR = os.path.join(REPO, "real_research", "data", "globular_clusters")
EBV = {"NGC 2419": 0.08, "Pal 3": 0.04, "Pal 4": 0.01, "Pal 14": 0.04}
par = {}
for line in open(os.path.join(GCDIR, "baumgardt_gc_parameters.tsv"), encoding="utf-8"):
    if line.startswith("#") or line.startswith("ClusterName"):
        continue
    f = line.rstrip("\n").split("\t"); par[f[0]] = f
prof = {}
for line in open(os.path.join(GCDIR, "baumgardt_gc_veldisp_profiles.tsv"), encoding="utf-8"):
    if line.startswith("#") or line.startswith("ClusterName"):
        continue
    f = line.rstrip("\n").split("\t")
    if f[6] == "RV":
        prof.setdefault(f[0], []).append((float(f[1]), int(f[2]), float(f[3]), float(f[4]), float(f[5])))
GC = []
for name in ["NGC 2419", "Pal 3", "Pal 4", "Pal 14"]:
    f = par[name]
    Dsun = float(f[3].split("+-")[0]); RGC = float(f[4].split("+-")[0]); Vapp = float(f[8].split("+-")[0]); rhl = float(f[11])
    MV = Vapp - 3.1 * EBV[name] - 5 * math.log10(Dsun * 1e3 / 10.0)
    g = dict(name=name, D=Dsun, RGC=RGC, LV=10 ** (0.4 * (4.83 - MV)), rhl=rhl)
    pr = prof[name]; R_pc = np.array([p[0] / 206265.0 * Dsun * 1e3 for p in pr]); s = np.array([p[2] for p in pr])
    up = np.array([p[3] for p in pr]); lo = np.array([p[4] for p in pr]); N = np.array([p[1] for p in pr])
    if len(R_pc) == 1:
        g.update(so=s[0], eso=0.5 * (up[0] + lo[0]), N=int(N[0]))
    else:
        ls = np.interp(math.log10(rhl), np.log10(R_pc), np.log10(s)); le = np.interp(math.log10(rhl), np.log10(R_pc), 0.5 * (up + lo) / s)
        j = int(np.argmin(np.abs(np.log10(R_pc) - math.log10(rhl))))
        g.update(so=10 ** ls, eso=(10 ** ls) * le, N=int(N[j]))
    GC.append(g)


def gc_sigma(g, foot, mode, ups=1.6, kern=nu_m):
    """mode: 'own' Newton | 'top' isolated law nu(y_int) | 'efe' h93's algebraic EFE nu(y_int + y_ext) with nu_s."""
    a0 = A0[foot]; r12 = (4.0 / 3.0) * g["rhl"] * PC; M = ups * g["LV"]
    sN = math.sqrt(G * M * MSUN / (6.0 * r12)) / 1e3
    yi = G * (M / 2) * MSUN / r12 ** 2 / a0; ye = G * MW_MB * MSUN / (g["RGC"] * KPC) ** 2 / a0
    if mode == "own":
        return sN
    if mode == "top":
        return sN * math.sqrt(kern(yi))
    return sN * math.sqrt(nu_s(yi + ye))


def p_low(so, sp, N):
    return float(chi2dist.cdf((N - 1) * (so / sp) ** 2, N - 1))


UPS_DRAWS = 1.6 * 10 ** (0.15 * np.random.default_rng(931).standard_normal(4000))


def gc_stat(foot, modes):
    ys, es = [], []
    for g, md in zip(GC, modes):
        ys.append(math.log(g["so"] / gc_sigma(g, foot, md))); es.append(math.hypot(g["eso"] / g["so"], 1 / math.sqrt(2 * (g["N"] - 1))))
    w = 1 / np.array(es) ** 2; m = float(np.sum(w * np.array(ys)) / np.sum(w)); em = 1 / math.sqrt(np.sum(w))
    U = 1.6 * math.exp(2 * m); eU = U * 2 * em
    tj = (U - 2.2) / eU if U > 2.2 else ((U - 1.3) / eU if U < 1.3 else 0.0)
    pl, pt = [], []
    for g, md in zip(GC, modes):
        F = np.array([p_low(g["so"], gc_sigma(g, foot, md, u), g["N"]) for u in UPS_DRAWS])
        pl.append(float(np.mean(F))); pt.append(float(np.mean(2 * np.minimum(F, 1 - F))))
    fis = lambda ps: float(chi2dist.sf(-2 * np.sum(np.log(np.clip(ps, 1e-300, 1))), 2 * len(ps)))
    pL, pT = fis(pl), fis(pt)
    L = float(norm.isf(max(pL, 1e-300))); T = float(norm.isf(max(pT, 1e-300)))
    return dict(ups=U, eups=eU, t_joint=tj, L=L, T_reported=T, pL=pL, m=(U - 2.2 if U > 2.2 else (U - 1.3 if U < 1.3 else 0.0)), err=eU)


# ============================================================================ wide binaries
def wb_fields(foot):
    a0 = A0[foot]; gint = nu_m(WB_Y) * WB_Y * a0
    s = math.sqrt(G * WB_M * MSUN / (WB_Y * a0))
    return gint, 2 * GEXT_SUN * s / (R0_KPC * KPC), GEXT_SUN, s


def wb_stat(foot, cls):
    gp = 1.0 if cls == "own" else math.sqrt(nu_m(WB_Y))
    g, sg = WB_OBS[foot]
    return dict(gamma_pred=gp, m=g - gp, err=sg, z=(g - gp) / sg)


# ============================================================================ labels per rule (classification on the canonical footing? no: per footing)
def labels(rule, foot):
    a0 = A0[foot]; lab = {}
    gi, gt, ge, s = wb_fields(foot); lab["WB"] = classify(rule, "WB", gi, gt, ge)
    for g in GC:
        r12 = (4.0 / 3.0) * g["rhl"] * PC; gi = g_int_law(1.6 * g["LV"], r12, a0); gh = g_host(g["RGC"], a0)
        lab["GC:" + g["name"]] = classify(rule, "GC", gi, 2 * gh * r12 / (g["RGC"] * KPC), gh)
    for kind, lst in (("CL", CL), ("UFD", UFD_R + UFD_U)):
        for d in lst:
            r12 = (4.0 / 3.0) * d["rh"] * PC; gi = g_int_law(2.0 * d["LV"] + 1.33 * d["MHI"], r12, a0); gh = g_host(d["Dgc"], a0)
            lab[f"{kind}:{d['name']}"] = classify(rule, kind, gi, 2 * gh * r12 / (d["Dgc"] * KPC), gh)
    return lab


def score(labfoot):
    """labfoot: foot -> label dict.  Returns per population per footing tension dicts and pass flags."""
    res = {}
    for foot in FOOTS:
        lab = labfoot[foot]
        res[("WB", foot)] = wb_stat(foot, lab["WB"])
        res[("GC", foot)] = gc_stat(foot, [lab["GC:" + g["name"]] for g in GC])
        res[("CL", foot)] = dwarf_stat("CL", foot, {d["name"]: lab["CL:" + d["name"]] for d in CL})
        res[("UFD", foot)] = dwarf_stat("UFD", foot, {d["name"]: lab["UFD:" + d["name"]] for d in UFD_R + UFD_U})
    passes = {}
    for pop in ("WB", "GC", "CL", "UFD"):
        ok = True
        for foot in FOOTS:
            r = res[(pop, foot)]
            ok &= (abs(r["t_joint"]) < 2 and r["L"] < 2) if pop == "GC" else abs(r["z"]) < 2
        passes[pop] = ok
    return res, passes


def tens(pop, r):
    return f"joint {r['t_joint']:+.2f}, L {r['L']:.2f}" if pop == "GC" else f"{r['z']:+.2f}"


# ============================================================================ run
P(f"CFG333 one ownership rule{' -- MUTATE (class labels permuted)' if MUTATE else ''}")
P("=" * 110)
P(f"units: 1 WB + {len(GC)} GC + {len(CL)} CL + {len(UFD_R)}+{len(UFD_U)} UFD;  kernel nu_mono;  owned dwarfs Newton on M_b/f_b (f_b {FB})")
RULES = ["R0", "R1", "R2", "R3"]
LAB = {rule: {foot: labels(rule, foot) for foot in FOOTS} for rule in RULES}
RESULTS = {"labels_counts": {}, "rules": {}}
for rule in RULES:
    for foot in FOOTS:
        lab = LAB[rule][foot]
        cnt = {k: f"{sum(1 for n, v in lab.items() if n.split(':')[0] == k and v == 'top')}/{sum(1 for n in lab if n.split(':')[0] == k)} top"
               for k in ("WB", "GC", "CL", "UFD")}
        RESULTS["labels_counts"][f"{rule}|{foot}"] = cnt
P("\nclass counts (top-level / all):")
for k, v in RESULTS["labels_counts"].items():
    P(f"   {k:14s} {v}")
P("   GC labels R1/R3 canonical: " + "; ".join(f"{g['name']} {LAB['R1']['canonical']['GC:' + g['name']]}/{LAB['R3']['canonical']['GC:' + g['name']]}" for g in GC))

SC = {}
if not MUTATE:
    for rule in RULES:
        res, ps = score(LAB[rule]); SC[rule] = (res, ps)
else:
    # MUTATE: permute labels across all units, per rule, per footing (same permutation for both footings)
    def permuted(rule, seed):
        rng = np.random.default_rng(seed); out = {}
        keys = list(LAB[rule]["canonical"].keys()); perm = rng.permutation(len(keys))
        for foot in FOOTS:
            vals = [LAB[rule][foot][k] for k in keys]
            out[foot] = {k: vals[perm[i]] for i, k in enumerate(keys)}
        return out
    for rule in RULES:
        res, ps = score(permuted(rule, 333)); SC[rule] = (res, ps)

P("\n4 x 3 MATRIX (+ R0 control row): PASS/FAIL within 2 sigma on both footings; tensions canonical | alt")
P(f"   {'rule':4s} | {'WB':28s} | {'GC (joint-Ups t, L sigma)':44s} | {'CL':22s} | {'UFD':22s} | passes")
for rule in RULES:
    res, ps = SC[rule]; cells = []
    for pop, wdt in (("WB", 28), ("GC", 44), ("CL", 22), ("UFD", 22)):
        s = f"{'P' if ps[pop] else 'F'} {tens(pop, res[(pop, 'canonical')])} | {tens(pop, res[(pop, 'alt')])}"
        cells.append(f"{s:{wdt}s}")
    n = sum(ps.values())
    P(f"   {rule:4s} | " + " | ".join(cells) + f" | {n}/4")
    RESULTS["rules"][rule] = dict(passes=ps, n_pass=n, res={f"{p}|{f}": v for (p, f), v in res.items()})

P("\ndetail (offsets in dex for dwarfs; gamma for WB; Upsilon for GC):")
for rule in RULES:
    res, _ = SC[rule]
    for foot in FOOTS:
        w, g, c, u = res[("WB", foot)], res[("GC", foot)], res[("CL", foot)], res[("UFD", foot)]
        P(f"   {rule} {foot:9s}: WB gamma_pred {w['gamma_pred']:.4f} | GC Ups {g['ups']:.2f}+-{g['eups']:.2f} L {g['L']:.2f} (T {g['T_reported']:.2f} reported) | "
          f"CL {c['m']:+.3f}+-{c['err']:.3f} | UFD {u['m']:+.4f}+-{u['err']:.4f}")

# reported variant: owned dwarfs stars-only Newton (R1/R3 classify some dwarfs owned)
P("\nreported: owned dwarfs with stars-only Newton (no cold share), canonical | alt")
for rule in ("R1", "R3"):
    for kind in ("CL", "UFD"):
        vals = []
        for foot in FOOTS:
            lab = LAB[rule][foot]; lst = CL if kind == "CL" else UFD_R + UFD_U
            vals.append(dwarf_stat(kind, foot, {d["name"]: lab[f"{kind}:{d['name']}"] for d in lst}, cold=False))
        P(f"   {rule} {kind:3s}: {vals[0]['m']:+.3f} (z {vals[0]['z']:+.2f}) | {vals[1]['m']:+.3f} (z {vals[1]['z']:+.2f})")
        RESULTS[f"starsonly|{rule}|{kind}"] = vals

# controls
P("\nCONTROLS")
gefe = {f: gc_stat(f, ["efe"] * 4) for f in FOOTS}
gN = {f: gc_stat(f, ["own"] * 4) for f in FOOTS}
P(f"   h93 EFE law: L {gefe['canonical']['L']:.2f} | {gefe['alt']['L']:.2f}; joint Ups {gefe['canonical']['ups']:.3f} | Newton {gN['canonical']['ups']:.3f}")
RESULTS["control_h93"] = dict(efe=gefe, newton=gN)
if not MUTATE:
    check("C1 h93 reproduced: L 4.6 / 4.9 sigma (+-0.1), joint Ups 0.76 (EFE) and 2.14 (Newton) (+-0.01)",
          abs(gefe["canonical"]["L"] - 4.6) < 0.1 and abs(gefe["alt"]["L"] - 4.9) < 0.1 and abs(gefe["canonical"]["ups"] - 0.76) < 0.01
          and abs(gN["canonical"]["ups"] - 2.14) < 0.01, f"L {gefe['canonical']['L']:.2f}/{gefe['alt']['L']:.2f}, Ups {gefe['canonical']['ups']:.3f}/{gN['canonical']['ups']:.3f}")
    u0 = SC["R0"][0]
    check("C2 AUDIT_UFD reproduced: +0.3245 / +0.3045 (5e-4), z 3.77 / 3.55 (0.02)",
          abs(u0[("UFD", "canonical")]["m"] - 0.3245) < 5e-4 and abs(u0[("UFD", "alt")]["m"] - 0.3045) < 5e-4
          and abs(u0[("UFD", "canonical")]["z"] - 3.77) < 0.02 and abs(u0[("UFD", "alt")]["z"] - 3.55) < 0.02,
          f"{u0[('UFD', 'canonical')]['m']:+.4f} z {u0[('UFD', 'canonical')]['z']:.2f} | {u0[('UFD', 'alt')]['m']:+.4f} z {u0[('UFD', 'alt')]['z']:.2f}")
    h93_iso = [1.653, 7.360, 5.042, 10.433]
    ours = []
    for g in GC:
        r12 = (4.0 / 3.0) * g["rhl"] * PC; yi = G * 0.8 * g["LV"] * MSUN / r12 ** 2 / A0["canonical"]; ours.append((nu_s(yi), nu_m(yi)))
    check("C3 R0 = bare law: GC isolated nu_s(y_int) = h93's printed nu(isolated) (5e-4), nu_mono = nu_s there (1e-6); UFD row = C2",
          all(abs(a - b) < 5e-4 for (a, _), b in zip(ours, h93_iso)) and all(abs(a - c) < 1e-6 * a for a, c in ours),
          "nu_s " + ", ".join(f"{a:.3f}" for a, _ in ours))
    best = max(RULES[1:], key=lambda r: (RESULTS["rules"][r]["n_pass"], -max(abs(v.get("z", v.get("t_joint", 0))) for v in RESULTS["rules"][r]["res"].values())))
    RESULTS["best_rule"] = best
    nb = RESULTS["rules"][best]["n_pass"]
    if any(RESULTS["rules"][r]["n_pass"] == 4 for r in RULES[1:]):
        verdict = "ONE RULE WORKS"
    elif nb == 3:
        verdict = "PARTIAL (best " + best + "; fails " + ",".join(p for p, ok in RESULTS["rules"][best]["passes"].items() if not ok) + ")"
    else:
        verdict = "NONE"
    RESULTS["verdict"] = verdict
    P(f"\nVERDICT: {verdict}")
else:
    base = json.load(open(os.path.join(HERE, "cfg333_one_rule_results.json")))
    best = base["best_rule"]; nb = base["rules"][best]["n_pass"]
    nm = RESULTS["rules"][best]["n_pass"]
    check(f"MUTATE seed 333: best rule {best} pass count drops ({nb} -> {nm})", nm < nb, f"{nb} -> {nm}")
    def permuted2(rule, seed):
        rng = np.random.default_rng(seed); keys = list(LAB[rule]["canonical"].keys()); perm = rng.permutation(len(keys))
        return {foot: {k: [LAB[rule][foot][q] for q in keys][perm[i]] for i, k in enumerate(keys)} for foot in FOOTS}
    cnts = [sum(score(permuted2(best, 1000 + i))[1].values()) for i in range(50)]
    RESULTS["mutate_50"] = cnts
    check(f"MUTATE 50 permutations: mean pass count of {best} below unmutated {nb}", np.mean(cnts) < nb, f"mean {np.mean(cnts):.2f}, max {max(cnts)}")

n_ok = sum(ok for _, ok in CHECKS)
P(f"\n{n_ok}/{len(CHECKS)} checks pass")
RESULTS["checks"] = {n: ok for n, ok in CHECKS}
open(os.path.join(HERE, f"cfg333_one_rule{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RESULTS, open(os.path.join(HERE, f"cfg333_one_rule{TAG}_results.json"), "w"), indent=1, default=float)
sys.exit(0 if n_ok == len(CHECKS) else 1)
