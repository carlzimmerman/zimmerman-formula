#!/usr/bin/env python3
"""CFG239 c3: claim (3) SD(gamma-hat)/sigma_fit, N ladder, seed averaging, MU1, MU6.
usage: CFG239_c3_fits.py --part g100|ladder|thin|mu1     (MUTATE=1 with --part mu1, MUTATE=6 with --part thin)
DR3 = code-path test only (Amdt 7(e)).  main exit 0; MUTATE exit 1 when the control bites."""
import os, sys, json, time, hashlib
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import CFG239_common as C

MUT = int(os.environ.get("MUTATE", "0"))
SEED = C.SEED
JOBS = int(os.environ.get("CFG239_JOBS", "10"))
FITDIR = C.WORK / "fits"; CSVDIR = C.WORK / "csv"


def fit_cached(path, seed=C.FIT_SEED):
    h = C.sha(path)[:16]
    f = FITDIR / f"{h}_{seed}.json"
    if f.exists():
        return json.loads(f.read_text())
    res, _ = C.run_fit(path, seed)
    f.write_text(json.dumps(res))
    return res


def fits_parallel(jobs):
    """jobs: list of (path, seed) -> list of result dicts"""
    with ThreadPoolExecutor(JOBS) as ex:
        return list(ex.map(lambda j: fit_cached(*j), jobs))


def summarize(res, name, log, rng, nboot=2000):
    out = {}
    for fp in ("can", "alt"):
        g = np.array([r[fp]["g"] for r in res]); s = np.array([r[fp]["s"] for r in res]); k = np.array([r[fp]["kappa"] for r in res])
        ratio = C.sd(g) / s.mean()
        bs = []
        for _ in range(nboot):
            ix = rng.integers(0, len(g), len(g)); bs.append(C.sd(g[ix]) / s[ix].mean())
        lo, hi = np.quantile(bs, [.16, .84])
        out[fp] = dict(n=len(g), mean_g=float(g.mean()), sd=C.sd(g), mean_sigma=float(s.mean()), ratio=float(ratio), ratio_16=float(lo),
                       ratio_84=float(hi), kappa_min=float(k.min()), kappa_max=float(k.max()))
        log(f"  {name} [{fp}] n={len(g)} mean gamma-hat {g.mean():.4f}  SD {C.sd(g):.4f}  mean sigma_fit {s.mean():.4f}  SD/sigma_fit {ratio:.3f}  (boot 16-84: {lo:.3f}-{hi:.3f})  kappa {k.min():.3f}-{k.max():.3f}")
    return out


def base_builds(mc, seeds):
    out = []
    for s in seeds:
        sig = mc.run(s)
        out.append(mc.final_mask(sig))
    return np.array(out)


def part_g100(log, mc, arr, rng):
    seeds = [SEED] + [SEED + 2000 + j for j in range(100)]
    t0 = time.time()
    M = base_builds(mc, seeds)
    paths = []
    for i, s in enumerate(seeds):
        p = CSVDIR / f"g100_{i:03d}.csv"; C.write_csv(arr, M[i], p); paths.append(p)
    log(f"  built {len(seeds)} G-only catalogues in {time.time()-t0:.0f} s; final counts mean {M.sum(1).mean():.1f} SD {C.sd(M.sum(1)):.1f}")
    flips = [int((M[0] & ~M[i]).sum()) for i in range(1, len(seeds))]
    log(f"  one-way flips vs frozen k=0: mean {np.mean(flips):.1f} SD {C.sd(flips):.1f} (as % of final {np.mean(flips)/M[0].sum()*100:.2f}%)")
    res = fits_parallel([(p, C.FIT_SEED) for p in paths])
    log(f"  fitted {len(res)} builds ({time.time()-t0:.0f} s)")
    out = {"flips_mean": float(np.mean(flips)), "counts": M.sum(1).tolist()}
    out["g101"] = summarize(res, "G-only K=100 (+k0)", log, rng)
    out["g100_only"] = summarize(res[1:], "G-only 100 new builds (k0 excluded)", log, rng)
    fo = fits_parallel([(paths[0], C.FIT_SEED + j) for j in range(1, 51)])
    fo_all = [res[0]] + fo
    out["fit_only"] = summarize(fo_all, "fit-only control (k0 CSV, fit seeds +0..50)", log, rng)
    for fp in ("can", "alt"):
        out["fit_only"][fp]["ratio_vs_build_sigma"] = out["fit_only"][fp]["sd"] / out["g101"][fp]["mean_sigma"]
        bo = np.sqrt(max(0, out["g101"][fp]["sd"] ** 2 - out["fit_only"][fp]["sd"] ** 2))
        out["g101"][fp]["build_only_sd"] = float(bo)
        log(f"  [{fp}] fit-only SD / mean sigma_fit {out['fit_only'][fp]['ratio_vs_build_sigma']:.3f}; build-only SD = sqrt(SD^2 - fitonly^2) = {bo:.4f} = {bo/out['g101'][fp]['mean_sigma']:.3f} sigma_fit")
    # k=0 z-score
    for fp in ("can", "alt"):
        g = np.array([r[fp]["g"] for r in res[1:]])
        z0 = (res[0][fp]["g"] - g.mean()) / C.sd(g)
        out["g101"][fp]["z0"] = float(z0)
        log(f"  [{fp}] frozen build k=0 gamma-hat {res[0][fp]['g']:.4f} vs mean of 100 builds {g.mean():.4f}: z = {z0:+.2f} SD_build")
    # seed averaging
    log("  seed averaging: SD of group means of m builds (non-overlapping groups of the 100 new builds)")
    sa = {}
    for fp in ("can", "alt"):
        g = np.array([r[fp]["g"] for r in res[1:]]); sd1 = C.sd(g)
        row = {}
        for m in (1, 2, 5, 10, 20):
            ng = 100 // m; gm = g[:ng * m].reshape(ng, m).mean(1)
            sdm = C.sd(gm) if ng > 1 else float("nan")
            row[m] = dict(sd=sdm, ratio=float(sdm * np.sqrt(m) / sd1), groups=ng)
        sa[fp] = row
        log(f"    [{fp}] " + "; ".join(f"m={m}: SD {row[m]['sd']:.4f} x sqrt(m)/SD1 = {row[m]['ratio']:.2f}" for m in row))
    out["seed_avg"] = sa
    # consensus catalogue
    p = M[1:].mean(0); cons = (p > 0.5) & arr["av_ok"]
    pc = CSVDIR / "g100_consensus.csv"; C.write_csv(arr, cons, pc)
    rc = fit_cached(pc)
    out["consensus"] = {}
    for fp in ("can", "alt"):
        g = np.array([r[fp]["g"] for r in res[1:]])
        d = (rc[fp]["g"] - g.mean()) / out["g101"][fp]["mean_sigma"]
        out["consensus"][fp] = dict(g=rc[fp]["g"], dist_sigma_fit=float(d), n=int(cons.sum()))
        log(f"    consensus catalogue (p-hat>0.5 over the 100 builds, N={int(cons.sum())}) [{fp}] gamma-hat {rc[fp]['g']:.4f}: distance from mean of builds {d:+.3f} sigma_fit (line |d|<=0.15)")
    # random-thinning equivalence: flips one-way / N
    n_fin = M[0].sum(); mean_flips = np.mean(flips)
    hand = np.sqrt(2 * mean_flips / n_fin) / np.sqrt(2)
    out["thinning_hand"] = float(hand)
    log(f"  hand estimate of SD/sigma_fit if flipped pairs were average pairs: {hand:.3f}")
    # verdict lines
    for fp in ("can", "alt"):
        r = out["g101"][fp]["ratio"]
        out["g101"][fp]["in_0.20_0.40"] = bool(0.20 <= r <= 0.40)
    return out


def hashbucket(ids):
    return ((ids.astype(np.uint64) * np.uint64(11400714819323198485)) >> np.uint64(62)).astype(int)


def part_ladder(log, mc, arr, rng):
    seeds = [SEED + 3000 + j for j in range(30)]
    t0 = time.time()
    M = base_builds(mc, seeds)
    sets = {"q0": [0], "q1": [1], "q2": [2], "q3": [3], "h0": [0, 1], "h1": [2, 3], "all": [0, 1, 2, 3]}
    bk = hashbucket(arr["id1"])
    jobs, meta = [], []
    for i in range(len(seeds)):
        for name, bs in sets.items():
            m = M[i] & np.isin(bk, bs)
            p = CSVDIR / f"lad_{i:02d}_{name}.csv"; C.write_csv(arr, m, p)
            jobs.append((p, C.FIT_SEED)); meta.append((i, name, int(m.sum())))
    log(f"  built {len(seeds)} builds x 7 subsets ({len(jobs)} fits) in {time.time()-t0:.0f} s; bucket sizes of k0: " + str([int(((bk == b) & M[i]).sum()) for b in range(4) for i in [0]]))
    res = fits_parallel(jobs)
    log(f"  fitted in {time.time()-t0:.0f} s")
    # tensors
    G = {fp: {nm: np.full(len(seeds), np.nan) for nm in sets} for fp in ("can", "alt")}
    Sg = {fp: {nm: np.full(len(seeds), np.nan) for nm in sets} for fp in ("can", "alt")}
    N = {nm: np.zeros(len(seeds)) for nm in sets}
    for (i, nm, n_), r in zip(meta, res):
        N[nm][i] = n_
        for fp in ("can", "alt"):
            G[fp][nm][i] = r[fp]["g"]; Sg[fp][nm][i] = r[fp]["s"]
    rungs = {"N~1550": ["q0", "q1", "q2", "q3"], "N~3100": ["h0", "h1"], "N~6200": ["all"]}

    def rung_stats(ix, fp):
        out = []
        for rn, names in rungs.items():
            var = np.mean([C.sd(G[fp][nm][ix]) ** 2 for nm in names])
            sfit = np.mean([Sg[fp][nm][ix].mean() for nm in names])
            nn = np.mean([N[nm][ix].mean() for nm in names])
            out.append((nn, np.sqrt(var) / sfit, np.sqrt(var), sfit))
        return out

    res_out = {}
    for fp in ("can", "alt"):
        allix = np.arange(len(seeds))
        st = rung_stats(allix, fp)
        lnN = np.log([s[0] for s in st]); lnr = np.log([s[1] for s in st])
        slope = np.polyfit(lnN, lnr, 1)[0]
        bsl = []
        for _ in range(2000):
            ix = rng.integers(0, len(seeds), len(seeds)); s2 = rung_stats(ix, fp)
            bsl.append(np.polyfit(np.log([s[0] for s in s2]), np.log([s[1] for s in s2]), 1)[0])
        lo, hi = np.quantile(bsl, [.025, .975])
        for (nn, r, sd_, sf), (rn, _) in zip(st, rungs.items()):
            log(f"  [{fp}] {rn}: N={nn:.0f} pooled SD {sd_:.4f} / sigma_fit {sf:.4f} = {r:.3f}")
        log(f"  [{fp}] slope of ln(ratio) on ln N = {slope:+.3f}; bootstrap 95% interval ({lo:+.3f}, {hi:+.3f}); contains 0: {lo<=0<=hi}; inside (-0.30,+0.30): {-0.30<lo and hi<0.30}")
        # per-subset spread
        for rn, names in rungs.items():
            log(f"      {rn} per-subset SD/mean sigma_fit: " + ", ".join(f"{C.sd(G[fp][nm])/Sg[fp][nm].mean():.3f}" for nm in names))
        res_out[fp] = dict(rungs=[dict(N=float(a), ratio=float(b)) for a, b, _, _ in st], slope=float(slope), ci=(float(lo), float(hi)),
                           contains0=bool(lo <= 0 <= hi), inside=bool(-0.30 < lo and hi < 0.30))
    return res_out


def part_thin(log, mc, arr, rng):
    base = np.array(mc.final_mask(mc.run(SEED)))
    rows = np.flatnonzero(base)
    out = {}
    for f in ((0.0,) if MUT == 6 else (0.05, 0.02)):
        nb = 3 if MUT == 6 else 30
        jobs = []
        for i in range(nb):
            r = np.random.default_rng(239000 + int(f * 1000) * 100 + i)
            keep = np.ones(len(base), bool)
            drop = r.choice(rows, int(round(f * len(rows))), replace=False); m = base.copy(); m[drop] = False
            p = CSVDIR / f"thin_{int(f*1000)}_{i:02d}.csv"; C.write_csv(arr, m, p); jobs.append((p, C.FIT_SEED))
        res = fits_parallel(jobs)
        s = summarize(res, f"thinning f={f}", log, rng, nboot=500)
        pred = float(np.sqrt(f / (1 - f))) if f > 0 else 0.0
        log(f"    predicted SD/sigma_fit = sqrt(f/(1-f)) = {pred:.3f}")
        for fp in ("can", "alt"):
            s[fp]["pred"] = pred; s[fp]["within_0.05"] = bool(abs(s[fp]["ratio"] - pred) <= 0.05)
        out[str(f)] = s
    return out


def part_thin2(log, mc, arr, rng):
    """POST HOC (after seeing the f = 2%/5% thinning plateau; NOT a frozen-criteria item): smaller random thinnings and a row-order shuffle
    of the identical catalogue, to locate the fit's own response floor to catalogue perturbations."""
    base = np.array(mc.final_mask(mc.run(SEED)))
    rows = np.flatnonzero(base)
    out = {}
    for f in (0.001, 0.005, 0.01):
        jobs = []
        for i in range(20):
            r = np.random.default_rng(239500 + int(f * 10000) * 100 + i)
            drop = r.choice(rows, int(round(f * len(rows))), replace=False); m = base.copy(); m[drop] = False
            p = CSVDIR / f"thin2_{int(f*10000)}_{i:02d}.csv"; C.write_csv(arr, m, p); jobs.append((p, C.FIT_SEED))
        res = fits_parallel(jobs)
        out[str(f)] = summarize(res, f"POST HOC thinning f={f} ({int(round(f*len(rows)))} pairs dropped)", log, rng, nboot=500)
    # identical pair set, shuffled row order
    import csv as _csv
    src = CSVDIR / "thin2_shuf_src.csv"; C.write_csv(arr, base, src)
    lines = open(src).read().splitlines(); head, body = lines[0], lines[1:]
    jobs = []
    for i in range(20):
        r = np.random.default_rng(239900 + i); ix = r.permutation(len(body))
        p = CSVDIR / f"thin2_shuf_{i:02d}.csv"; open(p, "w").write("\n".join([head] + [body[j] for j in ix]) + "\n"); jobs.append((p, C.FIT_SEED))
    res = fits_parallel(jobs)
    out["shuffle"] = summarize(res, "POST HOC identical pair set, rows shuffled (20 orders)", log, rng, nboot=500)
    return out


def part_mu1(log, mc, arr, rng):
    seeds = [SEED] * 3 if MUT == 0 else [SEED + 2000, SEED + 2001, SEED + 2002]
    M = base_builds(mc, seeds)
    paths = []
    for i in range(3):
        p = CSVDIR / f"mu1_{MUT}_{i}.csv"; C.write_csv(arr, M[i], p); paths.append(p)
    shas = [C.sha(p)[:16] for p in paths]
    res = fits_parallel([(p, C.FIT_SEED) for p in paths])
    out = {"sha": shas}
    for fp in ("can", "alt"):
        g = [r[fp]["g"] for r in res]; out[fp] = C.sd(g)
    log(f"  seeds {'identical (SEED x3)' if MUT == 0 else 'DISTINCT (mutated)'}: csv sha {shas}; flips {int((M[0]&~M[1]).sum())}, {int((M[0]&~M[2]).sum())}; sigma_build canonical {out['can']!r} alt {out['alt']!r}")
    out["zero"] = len(set(shas)) == 1 and out["can"] == 0.0 and out["alt"] == 0.0
    return out


def main():
    part = sys.argv[sys.argv.index("--part") + 1] if "--part" in sys.argv else "g100"
    if MUT == 1: part = "mu1"
    if MUT == 6: part = "thin"
    tag = part + (f"_MUTATE{MUT}" if MUT else "")
    log = C.Tee(C.HERE / f"CFG239_c3_fits_{tag}.out")
    log("CFG239 c3 fits | part", part, "| repo <repo> | DR3 = code-path test only (Amdt 7(e)) | MUTATE =", MUT)
    C.WORK.mkdir(exist_ok=True); FITDIR.mkdir(exist_ok=True); CSVDIR.mkdir(exist_ok=True)
    h0 = C.guard()
    B = C.load_builder(); arr = C.build_array(B, C.EXT / "stage_F.npz", "k0"); mc = C.MC(B, arr)
    rng = np.random.default_rng(23903)
    t0 = time.time()
    fn = dict(g100=part_g100, ladder=part_ladder, thin=part_thin, mu1=part_mu1, thin2=part_thin2)[part]
    res = fn(log, mc, arr, rng)
    C.jdump(res, C.HERE / f"CFG239_c3_fits_{tag}.json")
    log(f"done in {time.time()-t0:.0f} s")
    assert C.guard() == h0; log("guard after run ok")
    if MUT == 1:
        bites = not res["zero"]
        log("MUTATE1: assertion 'distinct seeds give sigma_build = 0' " + ("FAILS -> control bites (exit 1)" if bites else "holds (toothless)"))
        sys.exit(1 if bites else 0)
    if MUT == 6:
        ok = res["0.0"]["can"]["ratio"] > 0.10
        log("MUTATE6: f=0 thinning, assertion 'harness detects build noise (ratio>0.10)' " + ("holds" if ok else "FAILS -> control bites (exit 1)"))
        sys.exit(0 if ok else 1)
    if part == "mu1":
        log("MU1 main: identical seeds -> identical csv, sigma_build exactly 0 on both footings:", res["zero"])
    sys.exit(0)


if __name__ == "__main__":
    main()
