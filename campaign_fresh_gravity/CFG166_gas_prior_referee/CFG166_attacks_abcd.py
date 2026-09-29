#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG166 attacks (a)-(e), as frozen in CFG166_FROZEN_CRITERIA.md section 6.  Imports the main module (shared helpers) and, through it,
the CFG165 map code (SHARED, not independent).  Written before any CFG164 script/.out/.json was opened.

Run: ZF_REPO=<repo> python3 CFG166_attacks_abcd.py > CFG166_attacks.out    (rc 0)
"""
import os
import sys
import json
import math
import time
import itertools

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import CFG166_gas_prior_referee as G

P = G.P
SEEDA = 166
N4 = 4000


def cls_line(c):
    return f"flat {c['flat']:.3f} rival {c['rival']:.3f} both {c['both']:.3f} neither {c['neither']:.3f}"


def rank(x):
    o = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    r[o] = np.arange(len(x))
    return r


def spearman(x, y):
    return float(np.corrcoef(rank(x), rank(y))[0, 1])


def olsn(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    dof = len(y) - X.shape[1]
    s2 = float(res @ res) / dof
    cov = s2 * np.linalg.inv(X.T @ X)
    return beta, np.sqrt(np.diag(cov)), math.sqrt(s2)


def run(pipe, mu, s=1.0):
    zf, zh = pipe.eval(mu, s)
    return G.classes(zf, zh)


def main():
    t0 = time.time()
    out = {}
    pipe = G.Pipe("inc_star_deg")
    S = pipe.S
    G.KURVS15_POS = S.ids.index(15)
    C = G.load_phibss()
    sel = G.win(C)
    mrows = C.mu[sel]
    z17 = C.z < 1.7
    fit = G.ols(C.lm[z17] - 10.5, np.log10(C.mu[z17]))
    lmK, zK = S.logM, S.z
    prim = G.summarise(pipe, G.draw_rows(np.random.default_rng(SEEDA), 40000, mrows), (1.0, 1.62))
    pc = prim["P2"]["1.00"]
    pc16 = prim["P2"]["1.62"]
    P("=" * 110)
    P("CFG166 attacks (a)-(e).  repo=<repo>")
    P("=" * 110)
    P(f"primary (N=40000, seed 166), s=1.00: {cls_line(pc)} ; s=1.62: {cls_line(pc16)}")
    out["primary_ref"] = dict(s100=pc, s162=pc16)

    # ======================================================================================= (a)
    P("\n" + "#" * 100 + "\n(a) matching rule / low-mass extrapolation\n" + "#" * 100)
    lm17 = C.lm[sel]
    P(f"a0 vacuity: rows with log M* >= 10.40 among the 17: {int(np.sum(np.round(lm17, 2) >= 10.40))} of {len(lm17)} (all): the restriction is vacuous")
    # a1
    med = np.median(lm17)
    lo, hi = np.where(lm17 < med)[0], np.where(lm17 >= med)[0]
    P(f"a1 split of the 17 at median log M* = {med:.3f}: low half n={len(lo)} row-mu median {np.median(mrows[lo]):.3f} ; high half n={len(hi)} median {np.median(mrows[hi]):.3f}")
    a1 = {}
    for nm, ix in (("low", lo), ("high", hi)):
        o = G.summarise(pipe, G.draw_rows(np.random.default_rng(SEEDA), N4, mrows[ix]), (1.0, 1.62))
        a1[nm] = dict(n=len(ix), row_med=float(np.median(mrows[ix])), mbar_med=o["median"], s100=o["P2"]["1.00"], s162=o["P2"]["1.62"])
        P(f"   {nm:4s} half: mu-bar median {o['median']:.3f}; s=1: {cls_line(o['P2']['1.00'])}; s=1.62: rival {o['P2']['1.62']['rival']:.3f}")
    rho17 = spearman(lm17, mrows)
    rho38 = spearman(C.lm[z17], C.mu[z17])
    P(f"   Spearman rho(mu, log M*): 17 matched rows {rho17:+.3f}; 38 z<1.7 rows {rho38:+.3f}")
    out["a1"] = dict(split=a1, rho17=rho17, rho38=rho38)
    # a2 slope grid
    P(f"a2 slope grid (a(10.5)={fit['a']:.4f}, scatter {fit['scatter']:.3f} fixed; N={N4}, seed {SEEDA}); fitted b={fit['b']:.3f}, se={fit['se_b']:.3f}")
    a2 = {}
    grid = [("+0.22", 0.22), ("0", 0.0), ("-0.11", -0.11), ("-0.22 (fit)", fit["b"]), ("-0.33", -0.33), ("-0.44", -0.44), ("-0.66", -0.66),
            ("b_hat-se", fit["b"] - fit["se_b"]), ("b_hat+se", fit["b"] + fit["se_b"])]
    for nm, b in grid:
        o = G.summarise(pipe, G.draw_M(np.random.default_rng(SEEDA), N4, fit, lmK, slope=b), (1.0, 1.62))
        a2[nm] = dict(b=float(b), mbar=o["median"], s100=o["P2"]["1.00"], s162=o["P2"]["1.62"])
        P(f"   b={nm:12s} ({b:+.3f}): mu-bar median {o['median']:.3f}; s=1: {cls_line(o['P2']['1.00'])}; s=1.62: flat {o['P2']['1.62']['flat']:.3f} rival {o['P2']['1.62']['rival']:.3f}")
    out["a2"] = a2
    span1 = max(a2[k]["s100"]["rival"] for k in ("b_hat-se", "b_hat+se", "-0.22 (fit)")) - min(a2[k]["s100"]["rival"] for k in ("b_hat-se", "b_hat+se", "-0.22 (fit)"))
    P(f"   span of P(lean rival, s=1) across b in [b_hat-se, b_hat+se]: {span1:.3f} (EXTRAPOLATION-DRIVEN if >= 0.20)")
    # a3
    P("a3 slope significance")
    rng = np.random.default_rng(SEEDA)
    x, y = C.lm[z17] - 10.5, np.log10(C.mu[z17])
    bb = []
    for i in range(2000):
        ix = rng.integers(0, len(x), len(x))
        if np.ptp(x[ix]) == 0:
            continue
        bb.append(G.ols(x[ix], y[ix])["b"])
    bp = [G.ols(x, rng.permutation(y))["b"] for i in range(2000)]
    pperm = float(np.mean(np.abs(bp) >= abs(fit["b"])))
    P(f"   b_hat {fit['b']:+.3f} se {fit['se_b']:.3f} t {fit['b']/fit['se_b']:+.2f}; bootstrap 16-84%: {np.percentile(bb,16):+.3f} .. {np.percentile(bb,84):+.3f}; permutation p (two-sided, 2000) {pperm:.3f}")
    out["a3"] = dict(b=fit["b"], se=fit["se_b"], t=fit["b"] / fit["se_b"], boot16=float(np.percentile(bb, 16)), boot84=float(np.percentile(bb, 84)), perm_p=pperm)
    # a4 variant M+
    P("a4 Variant M+ (bootstrap the 38 rows per draw, refit, then draw)")
    rng = np.random.default_rng(SEEDA)
    f = G.sysfac(rng, N4)
    mus = np.empty((N4, 10))
    n38 = len(x)
    for i in range(N4):
        ix = rng.integers(0, n38, n38)
        if np.ptp(x[ix]) == 0:
            ix = np.arange(n38)
        fi = G.ols(x[ix], y[ix])
        mus[i] = 10.0 ** (fi["a"] + fi["b"] * (lmK - 10.5) + fi["scatter"] * rng.standard_normal(10))
    mus *= f[:, None]
    oMp = G.summarise(pipe, mus, (1.0, 1.62))
    G.fmt_sum("Variant M+", oMp)
    oM = G.summarise(pipe, G.draw_M(np.random.default_rng(SEEDA), N4, fit, lmK), (1.0, 1.62))
    dM = {k: oMp["P2"]["1.00"][k] - oM["P2"]["1.00"][k] for k in ("flat", "rival", "both", "neither")}
    dP = {k: oMp["P2"]["1.00"][k] - pc[k] for k in ("flat", "rival", "both", "neither")}
    P("   M+ minus M (s=1):", {k: round(v, 3) for k, v in dM.items()})
    P("   M+ minus primary (s=1):", {k: round(v, 3) for k, v in dP.items()})
    out["a4"] = dict(Mplus=oMp, M=oM, dM=dM, dP=dP)
    # a5 kernel
    P("a5 each disc at its own mass: kernel prior on the 38 z<1.7 rows")
    a5 = {}
    lm38, mu38 = C.lm[z17], C.mu[z17]
    for w in (0.2, 0.3, 0.5):
        rng = np.random.default_rng(SEEDA)
        f = G.sysfac(rng, N4)
        mus = np.empty((N4, 10))
        ess = []
        for j in range(10):
            wt = np.exp(-0.5 * ((lmK[j] - lm38) / w) ** 2)
            p = wt / wt.sum()
            ess.append(float(1.0 / np.sum(p ** 2)))
            mus[:, j] = mu38[rng.choice(len(mu38), size=N4, p=p)]
        mus *= f[:, None]
        o = G.summarise(pipe, mus, (1.0, 1.62))
        a5[f"w={w}"] = dict(ess=ess, mbar=o["median"], s100=o["P2"]["1.00"], s162=o["P2"]["1.62"])
        P(f"   w={w}: ESS per disc {[round(e,1) for e in ess]}; mu-bar median {o['median']:.3f} (16-84 {o['p16']:.3f}-{o['p84']:.3f}); s=1: {cls_line(o['P2']['1.00'])}; s=1.62 rival {o['P2']['1.62']['rival']:.3f}")
    out["a5"] = a5
    kr = [a5[k]["s100"]["rival"] for k in a5]
    span5 = max(kr) - min(kr)
    dM_ = max(abs(dP[k]) for k in dP)
    P(f"   a5 span of P(lean rival, s=1) across kernel widths {span5:.3f}; kernel(w=0.3) minus primary rival {a5['w=0.3']['s100']['rival'] - pc['rival']:+.3f}; M+ max |class change vs primary| {dM_:.3f}")
    a_driven = (span1 >= 0.20) or (span5 >= 0.20) or (dM_ >= 0.10)
    a_t = abs(fit["b"] / fit["se_b"])
    verdict_a = ("EXTRAPOLATION-DRIVEN" if a_driven else "EXTRAPOLATION-ROBUST") + ("; mass trend UNDETERMINED (|b|/se < 2)" if a_t < 2 else "; mass trend detected (|b|/se >= 2)")
    P(f"   VERDICT (a): {verdict_a}   [span1 {span1:.3f}, span5 {span5:.3f}, M+ max change {dM_:.3f}, |t| {a_t:.2f}]")
    out["verdict_a"] = verdict_a

    # ======================================================================================= (b)
    P("\n" + "#" * 100 + "\n(b) selection biases\n" + "#" * 100)
    b = {}
    # b2 z exponent
    sel51 = np.arange(len(C.mu))
    X = np.column_stack([np.ones(len(sel51)), C.lm - 10.5, np.log10(1 + C.z)])
    beta, se, sc = olsn(X, np.log10(C.mu))
    P(f"b2 in-repo fit log10 mu = c + b (logM-10.5) + gamma log10(1+z), 51 clean rows: b={beta[1]:+.3f}+-{se[1]:.3f}, gamma={beta[2]:+.2f}+-{se[2]:.2f}, scatter {sc:.3f}")
    P(f"   |gamma-2.5| = {abs(beta[2]-2.5):.2f} vs 2 se = {2*se[2]:.2f}: declared 2.5 {'CONSISTENT' if abs(beta[2]-2.5) <= 2*se[2] else 'INCONSISTENT'} (confounded: z~2.2 rows more massive)")
    ratio = ((1 + zK)[None, :] / (1 + C.z[sel])[:, None]) ** 2.5
    P(f"   Variant Z factor [(1+z_i)/(1+z_CO,j)]^2.5: median {np.median(ratio):.3f}, mean {ratio.mean():.3f}")
    # also without mass term
    X2 = np.column_stack([np.ones(len(sel51)), np.log10(1 + C.z)])
    b2, se2, _ = olsn(X2, np.log10(C.mu))
    P(f"   z-only fit gamma = {b2[1]:+.2f}+-{se2[1]:.2f}")
    b["b2"] = dict(b=float(beta[1]), se_b=float(se[1]), gamma=float(beta[2]), se_gamma=float(se[2]), gamma_zonly=float(b2[1]), se_zonly=float(se2[1]),
                   consistent=bool(abs(beta[2] - 2.5) <= 2 * se[2]), ratio_median=float(np.median(ratio)))
    # b3 bounding run
    P("b3 flagged rows (upper limits / inconsistent / secondary): inventory")
    inv = []
    for r in C.allrows:
        if r["ul"] or r["inc"] or r["comp"] == "se":
            lmr = math.log10(r["mstar"]) if r["mstar"] > 0 else float("nan")
            inv.append((r["name"], "UL" if r["ul"] else ("INC" if r["inc"] else "SE"), r["z"], lmr))
            P(f"   {r['name']:14s} {'UL' if r['ul'] else ('INC' if r['inc'] else 'SE'):4s} z_CO={r['z']} logM*={lmr:.2f}")
    add_lo, add_hi = [], []
    for r in C.allrows:
        if (r["ul"] or r["inc"]) and (not math.isfinite(r["z"])) and r["mstar"] > 0 and 9.5 <= math.log10(r["mstar"]) <= 10.8:
            if r["ul"]:
                add_lo.append(0.0)
                add_hi.append(r["mmol"] / r["mstar"])
            else:
                q = r["fgas_q"] / (1 - r["fgas_q"])
                rcc = r["mmol"] / r["mstar"]
                add_lo.append(min(q, rcc))
                add_hi.append(max(q, rcc))
    P(f"   flagged rows with NaN z and log M* in [9.5,10.8] (redshift unknown; bound only): {len(add_lo)}; low-bound mu {np.round(add_lo,2).tolist()}, high-bound mu {np.round(add_hi,2).tolist()}")
    b3 = {}
    for nm, add in (("primary only", []), ("+rows at low bound", add_lo), ("+rows at high bound", add_hi)):
        rows_ = np.concatenate([mrows, np.array(add)]) if add else mrows
        o = G.summarise(pipe, G.draw_rows(np.random.default_rng(SEEDA), N4, rows_), (1.0,))
        b3[nm] = dict(n=len(rows_), mbar=o["median"], s100=o["P2"]["1.00"])
        P(f"   {nm:22s} n={len(rows_)}: mu-bar median {o['median']:.3f}; s=1 {cls_line(o['P2']['1.00'])}")
    b["b3"] = dict(inventory=inv, bound=b3)
    P("   => the detection bias cannot be tested from the matched rows (no flagged row has a z_CO in the window); the bound uses unknown-z rows and is labelled a bound.")
    # b4 sSFR
    I = G.load_kurvs_extra()
    ssK = np.array([float(I[i]["sfr_msun_yr"]) / 10 ** float(I[i]["logMstar"]) * 1e9 for i in S.ids])
    ok = np.isfinite(C.sfr) & (C.sfr > 0)
    ss = C.sfr / C.mstar * 1e9
    P(f"b4 sSFR (per Gyr): KURVS ten median {np.median(ssK):.2f} (range {ssK.min():.2f}-{ssK.max():.2f}); PHIBSS 17 matched median {np.nanmedian(ss[sel]):.2f} (n finite {int(np.sum(ok[sel]))}); tracers differ (H-alpha vs IR/UV): level offset only flagged")
    okc = ok
    X3 = np.column_stack([np.ones(okc.sum()), C.lm[okc] - 10.5, np.log10(1 + C.z[okc]), np.log10(ss[okc])])
    b3f, se3f, sc3 = olsn(X3, np.log10(C.mu[okc]))
    P(f"   partial fit on {okc.sum()} clean rows with SFR: log mu = c + b logM + gamma log(1+z) + beta log sSFR: beta = {b3f[3]:+.2f}+-{se3f[3]:.2f}, b={b3f[1]:+.2f}+-{se3f[1]:.2f}, gamma={b3f[2]:+.2f}+-{se3f[2]:.2f}")
    rng = np.random.default_rng(SEEDA)
    fs = G.sysfac(rng, N4)
    sm = np.where(np.isfinite(ss[sel]) & (ss[sel] > 0), ss[sel], np.nan)
    good = np.isfinite(sm)
    mus = np.empty((N4, 10))
    essb = []
    for j in range(10):
        wt = np.where(good, np.exp(-0.5 * ((np.log10(ssK[j]) - np.log10(np.where(good, sm, 1.0))) / 0.3) ** 2), 0.0)
        p = wt / wt.sum()
        essb.append(float(1.0 / np.sum(p ** 2)))
        mus[:, j] = mrows[rng.choice(len(mrows), size=N4, p=p)]
    mus *= fs[:, None]
    o = G.summarise(pipe, mus, (1.0,))
    fac = o["median"] / prim["median"]
    P(f"   sSFR-reweighted prior (kernel 0.3 dex): ESS per disc {[round(e,1) for e in essb]}; mu-bar median {o['median']:.3f} (x{fac:.2f} vs primary); s=1 {cls_line(o['P2']['1.00'])}")
    P(f"   VERDICT (b4): {'sSFR-INSENSITIVE' if 1/1.25 <= fac <= 1.25 else 'sSFR-SENSITIVE'} (factor {fac:.2f}; threshold 1.25)")
    b["b4"] = dict(ssK_med=float(np.median(ssK)), ssP_med=float(np.nanmedian(ss[sel])), beta=float(b3f[3]), se_beta=float(se3f[3]), ess=essb,
                   mbar=o["median"], factor=float(fac), s100=o["P2"]["1.00"])
    # b5 toy alpha_CO(M)
    rng = np.random.default_rng(SEEDA)
    mu0 = G.draw_rows(rng, N4, mrows)
    mult = 10.0 ** (0.3 * (10.5 - lmK))
    o = G.summarise(pipe, mu0 * mult[None, :], (1.0, 1.62))
    P(f"b5 toy mass-dependent alpha_CO multiplier 10^(0.3(10.5-logM*_i)) (range x{mult.min():.2f}-x{mult.max():.2f}; a guess, no repo data): mu-bar median {o['median']:.3f}; s=1 {cls_line(o['P2']['1.00'])}; s=1.62 rival {o['P2']['1.62']['rival']:.3f}")
    b["b5"] = dict(mult=mult.tolist(), mbar=o["median"], s100=o["P2"]["1.00"], s162=o["P2"]["1.62"])
    out["b"] = b

    # ======================================================================================= (c)
    P("\n" + "#" * 100 + "\n(c) window-edge grid\n" + "#" * 100)
    frozen17 = set(sel.tolist())
    zlos = (0.95, 1.00, 1.05, 1.10, 1.20, 1.30)
    zhis = (1.6, 1.7, 2.5)
    mlos = (9.5, 10.45, 10.60)
    mhis = (10.70, 10.75, 10.80, 10.85, 10.90, 11.00, 11.30)
    cache = {}
    rows = []
    skipped = 0
    for zl, zh, ml, mh in itertools.product(zlos, zhis, mlos, mhis):
        ix = G.win(C, zl, zh, ml, mh)
        if len(ix) < 8:
            skipped += 1
            rows.append(dict(zlo=zl, zhi=zh, mlo=ml, mhi=mh, n=len(ix), skipped=True))
            continue
        key = tuple(ix.tolist())
        if key not in cache:
            o = G.summarise(pipe, G.draw_rows(np.random.default_rng(SEEDA), N4, C.mu[ix]), (1.0,))
            cache[key] = (o["median"], o["P2"]["1.00"], float(np.median(C.mu[ix])))
        mb, cc, rm = cache[key]
        rows.append(dict(zlo=zl, zhi=zh, mlo=ml, mhi=mh, n=len(ix), overlap=len(set(ix.tolist()) & frozen17), mbar=mb, row_med=rm, **cc))
    valid = [r for r in rows if not r.get("skipped")]
    P(f"   {len(rows)} windows; {skipped} with < 8 rows skipped; {len(valid)} evaluated on {len(cache)} distinct row sets (identical row sets share draws)")

    def modal(r):
        return max(("flat", "rival", "both", "neither"), key=lambda k: r[k])
    nrival = sum(1 for r in valid if modal(r) == "rival")
    frac_modal = nrival / len(valid)
    P(f"   (i) lean rival modal in {nrival}/{len(valid)} = {frac_modal:.3f} of windows with N>=8 (pass >= 0.80)")
    near = [r for r in valid if r["overlap"] >= 12]
    maxdev = max(abs(r["rival"] - 0.55) for r in near)
    worst = max(near, key=lambda r: abs(r["rival"] - 0.55))
    P(f"   (ii) windows sharing >= 12 rows with the frozen 17: {len(near)}; max |P(lean rival)-0.55| = {maxdev:.3f} at z[{worst['zlo']},{worst['zhi']}] logM[{worst['mlo']},{worst['mhi']}] (n={worst['n']}, overlap {worst['overlap']}) (pass <= 0.12)")
    hi68 = sum(1 for r in valid if r["rival"] >= 0.68)
    P(f"   windows with P(lean rival) >= 0.68: {hi68}/{len(valid)} = {hi68/len(valid):.3f} (H1 edge-dependent if >= 0.20)")
    pass_c = frac_modal >= 0.80 and maxdev <= 0.12
    nd_i = sum(1 for k in cache.values() if max(("flat", "rival", "both", "neither"), key=lambda q: k[1][q]) == "rival")
    P(f"   distinct row sets with lean rival modal: {nd_i}/{len(cache)} = {nd_i/len(cache):.3f}")
    P(f"   VERDICT (c): {'NOT TUNED (both lines pass)' if pass_c else 'NOT STABLE to its own edges (a pass line fails)'}; H1 label {'edge-dependent' if hi68/len(valid) >= 0.20 else 'stable'}")
    P("   P(lean rival, s=1) over (z_lo rows) x (log M*_hi columns), log M*_lo = 9.5, z_hi = 1.7   [n rows in brackets]")
    P("   z_lo \\ M_hi  " + "  ".join(f"{m:>11.2f}" for m in mhis))
    for zl in zlos:
        line = []
        for mh in mhis:
            r = [q for q in rows if q["zlo"] == zl and q["zhi"] == 1.7 and q["mlo"] == 9.5 and q["mhi"] == mh][0]
            line.append("     skipped" if r.get("skipped") else f"{r['rival']:.2f}[{r['n']:2d}]".rjust(11))
        P(f"   {zl:<12.2f}" + "  ".join(line))
    P("   single-step moves from the frozen window (all other edges frozen); largest change in each class:")
    base = [q for q in rows if q["zlo"] == 1.0 and q["zhi"] == 1.7 and q["mlo"] == 9.5 and q["mhi"] == 10.8][0]
    steps = {}
    for edge, vals_, fro in (("zlo", zlos, 1.0), ("zhi", zhis, 1.7), ("mlo", mlos, 9.5), ("mhi", mhis, 10.8)):
        best = {k: 0.0 for k in ("flat", "rival", "both")}
        for v in vals_:
            kw = dict(zlo=1.0, zhi=1.7, mlo=9.5, mhi=10.8)
            kw[edge] = v
            r = [q for q in rows if all(q[e] == kw[e] for e in kw)][0]
            if r.get("skipped"):
                continue
            for k in best:
                best[k] = max(best[k], abs(r[k] - base[k]))
        steps[edge] = best
        P(f"     edge {edge}: max |dP| flat {best['flat']:.3f} rival {best['rival']:.3f} both {best['both']:.3f}")
    out["c"] = dict(rows=rows, frac_modal=frac_modal, maxdev=maxdev, hi68=hi68 / len(valid), pass_c=bool(pass_c), steps=steps, n_distinct=len(cache), distinct_modal_rival=nd_i)

    # ======================================================================================= (d)
    P("\n" + "#" * 100 + "\n(d) marginalisation definition\n" + "#" * 100)
    d = {}
    N = 40000
    items = [("1 frozen (empirical, per-disc independent)", dict(mode="indep")), ("2 hyperprior bootstrap", dict(mode="hyper")),
             ("3 lognormal fit", dict(mode="lognormal")), ("4 coherent one-row-per-draw", dict(mode="coherent")),
             ("5 per-disc scatter off (row median)", dict(mode="median")), ("6 systematics off", dict(mode="indep", sys=False))]
    res_d = {}
    for nm, kw in items:
        mu = G.draw_rows(np.random.default_rng(SEEDA), N, mrows, **kw)
        o = G.summarise(pipe, mu, (1.0,))
        res_d[nm] = o
        c = o["P2"]["1.00"]
        P(f"   {nm:44s} mu-bar median {o['median']:.3f} width {o['width_dex']:.3f} dex; s=1: {cls_line(c)}")
    # item 7
    mu = G.draw_rows(np.random.default_rng(SEEDA), N, mrows)
    mbar = np.median(mu, axis=1)
    c7 = run(pipe, np.repeat(mbar[:, None], 10, axis=1))
    P(f"   {'7 constant mu = mu-bar (all discs equal)':44s} s=1: {cls_line(c7)}")
    res_d["7 constant mu-bar"] = c7
    p1 = res_d[items[0][0]]["P2"]["1.00"]
    diffs = {}
    for nm in (items[1][0], items[2][0]):
        diffs[nm] = max(abs(res_d[nm]["P2"]["1.00"][k] - p1[k]) for k in ("flat", "rival", "both", "neither"))
        P(f"   max class difference of item {nm[:1]} vs item 1: {diffs[nm]:.3f}")
    modal1 = max(("flat", "rival", "both"), key=lambda k: p1[k])
    keep = {}
    for nm in [items[3][0], items[4][0], items[5][0]]:
        c = res_d[nm]["P2"]["1.00"]
        keep[nm] = max(("flat", "rival", "both"), key=lambda k: c[k]) == modal1
    keep7 = max(("flat", "rival", "both"), key=lambda k: c7[k]) == modal1
    robust = all(v < 0.05 for v in diffs.values()) and all(keep.values()) and keep7
    P(f"   modal class of item 1: {modal1}; kept by items 4,5,6: {list(keep.values())}, item 7: {keep7}")
    P(f"   VERDICT (d): {'DEFINITION-ROBUST' if robust else 'DEFINITION-DEPENDENT'} (items 1-3 max diff {max(diffs.values()):.3f}; threshold 0.05)")
    P(f"   width: with both systematics {res_d[items[0][0]]['width_dex']:.3f} dex; systematics only {res_d[items[4][0]]['width_dex']:.3f} dex; intrinsic scatter only {res_d[items[5][0]]['width_dex']:.3f} dex")
    P("   class of a constant mu at s=1 (no systematics; the mu-bar values the probabilities integrate over):")
    scan = {}
    for mu_ in (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0):
        r = pipe.cellz(np.full(10, mu_), 1.0)
        cl = G.M165.classify(r[0], r[1])
        scan[str(mu_)] = dict(zf=r[0], zh=r[1], cls=cl)
        P(f"     mu={mu_:4.2f}: z_flat {r[0]:+.2f} z_H {r[1]:+.2f} -> {cl}")
    d["res"] = {k: v for k, v in res_d.items()}
    d["diffs"] = diffs
    d["robust"] = bool(robust)
    d["scan"] = scan
    out["d"] = d

    # ======================================================================================= (e)
    P("\n" + "#" * 100 + "\n(e) extras\n" + "#" * 100)
    e = {}
    mu = G.draw_rows(np.random.default_rng(SEEDA), N4, mrows)
    pipe2 = G.Pipe("inc_sfr_deg")
    o = G.summarise(pipe2, mu, (1.0,))
    P(f"   inc_sfr_deg vs inc_star_deg (N={N4}): inc_star {cls_line(G.summarise(pipe, mu, (1.0,))['P2']['1.00'])}; inc_sfr {cls_line(o['P2']['1.00'])}")
    e["inc_sfr"] = o["P2"]["1.00"]
    zf, zh = pipe.eval(mu, 3.0, kind="P2")
    zf3, zh3 = pipe.eval(mu, 3.0)
    P(f"   s=3: P2 spec {cls_line(G.classes(zf, zh))}; alpha x 3.0 {cls_line(G.classes(zf3, zh3))}")
    e["s3"] = dict(P2spec=G.classes(zf, zh), alpha3=G.classes(zf3, zh3))
    # anchor unscaled at s=1.62
    sp_anch = G.M165.spec("P4", scale=1.0)
    n = 1500
    zs_a, zs_b = [], []
    for i in range(n):
        ra = G.M165.cell(S, pipe.AS, pipe.sp(1.62), mu[i], 0.0, "canonical")
        rb = G.M165.cell(S, pipe.AS, pipe.sp(1.62), mu[i], 0.0, "canonical", sp_anchor=sp_anch)
        zs_a.append((ra["flat"]["z"], ra["H"]["z"]))
        zs_b.append((rb["flat"]["z"], rb["H"]["z"]))
    za, zb = np.array(zs_a), np.array(zs_b)
    ca, cb = G.classes(za[:, 0], za[:, 1]), G.classes(zb[:, 0], zb[:, 1])
    P(f"   anchor scaled vs unscaled at s=1.62 (N={n}): scaled {cls_line(ca)}; unscaled {cls_line(cb)}; median |dz_flat| {np.median(np.abs(za[:,0]-zb[:,0])):.3f}")
    e["anchor"] = dict(scaled=ca, unscaled=cb)
    fit0 = dict(fit)
    fit0["scatter"] = fit["scatter0"]
    o0 = G.summarise(pipe, G.draw_M(np.random.default_rng(SEEDA), N4, fit0, lmK), (1.0,))
    o2 = G.summarise(pipe, G.draw_M(np.random.default_rng(SEEDA), N4, fit, lmK), (1.0,))
    P(f"   Variant M scatter ddof0 ({fit['scatter0']:.3f}) vs ddof2 ({fit['scatter']:.3f}): s=1 {cls_line(o0['P2']['1.00'])} | {cls_line(o2['P2']['1.00'])}")
    e["ddof"] = dict(ddof0=o0["P2"]["1.00"], ddof2=o2["P2"]["1.00"])
    out["e"] = e

    out["elapsed_s"] = round(time.time() - t0, 1)
    P(f"\nelapsed {out['elapsed_s']} s")
    with open(os.path.join(HERE, "CFG166_attacks_results.json"), "w") as f:
        json.dump(out, f, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else (bool(o) if isinstance(o, np.bool_) else str(o)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
