#!/usr/bin/env python3
"""CFG239 c5 (POST HOC, written after the frozen-criteria runs were saved and after the half-symmetric-difference
definition was noticed in the quoted 142.3): (a) the flip statistic as (N(0->k)+N(k->0))/2 with its null; (b) seed averaging with
random groups instead of consecutive blocks.  DR3 = code-path test only (Amdt 7(e)).  exit 0."""
import numpy as np
import CFG239_common as C
import CFG239_c3_fits as F3
import CFG239_c2_flips as F2

SEED = C.SEED


def main():
    log = C.Tee(C.HERE / "CFG239_c5_posthoc.out")
    log("CFG239 c5 POST HOC | repo <repo> | DR3 = code-path test only (Amdt 7(e))")
    h0 = C.guard()
    B = C.load_builder(); arr = C.build_array(B, C.EXT / "stage_F.npz", "k0"); mc = C.MC(B, arr)
    av, thr = mc.av_ok, mc.thr
    rng = np.random.default_rng(23905)
    Pf = np.array([((mc.run(s) <= thr) & av) for s in F2.FRO])
    Pe = np.array([((mc.run(s) <= thr) & av) for s in F2.EST]); p3 = Pe.mean(0)
    Mf = F2.omat(Pf)
    half = (Mf[0, 1:] + Mf[1:, 0]) / 2
    log(f"(a) frozen seeds SEED+0..9: one-direction mean N(0->k) {Mf[0,1:].mean():.2f}; reverse {Mf[1:,0].mean():.2f}; half-symmetric difference mean {half.mean():.2f}")
    log("    (the quoted '142.3 one-way' of the calc chat is reproduced by the half-symmetric-difference definition: see the post-run compare)")
    reps = []
    for _ in range(4000):
        B_ = rng.random((10, len(p3))) < p3
        M = F2.omat(B_); reps.append(((M[0, 1:] + M[1:, 0]) / 2).mean())
    reps = np.array(reps)
    z = (half.mean() - reps.mean()) / reps.std(ddof=1)
    log(f"    null (E3 p-hat, 4000 reps): mean {reps.mean():.1f} SD {reps.std(ddof=1):.1f}; observed {half.mean():.1f}: z = {z:+.2f}")
    E1 = ((Pf.mean(0)) * (1 - Pf.mean(0))).sum()
    log(f"    their predictor sum p(1-p) over ten seeds (E1) = {E1:.1f}: observed - E1 = {half.mean()-E1:+.1f} = {(half.mean()-E1)/reps.std(ddof=1):+.2f} null SD; E3 = {(p3*(1-p3)).sum()*200/199:.1f}: observed - E3 = {half.mean()-(p3*(1-p3)).sum()*200/199:+.1f} = {(half.mean()-(p3*(1-p3)).sum()*200/199)/reps.std(ddof=1):+.2f} SD")
    # (b)
    res = [F3.fit_cached(F3.CSVDIR / f"g100_{i:03d}.csv") for i in range(1, 101)]
    log("(b) seed averaging, random m-subsets of the 100 G-only builds (2000 draws each); ratio = SD_m / [SD_1 sqrt((N-m)/((N-1) m))] (1 = independent builds)")
    for fp in ("can", "alt"):
        g = np.array([r[fp]["g"] for r in res]); sd1 = C.sd(g); N = len(g)
        row = []
        for m in (2, 5, 10, 20, 50):
            means = np.array([g[rng.choice(N, m, replace=False)].mean() for _ in range(2000)])
            row.append((m, means.std(ddof=1) / (sd1 * np.sqrt((N - m) / ((N - 1) * m)))))
        log(f"    [{fp}] " + "; ".join(f"m={m}: {r:.2f}" for m, r in row))
    # (c) pooled G-only ratio over all distinct G-only builds fitted in this lane (needs the post-run compare's CSVs if present)
    paths = [F3.CSVDIR / f"g100_{i:03d}.csv" for i in range(0, 101)] + [F3.CSVDIR / f"cmp_g50_{k:02d}.csv" for k in range(1, 51)]
    paths = [q for q in paths if q.exists()]
    allres = [F3.fit_cached(q) for q in paths]
    log(f"(c) pooled G-only builds ({len(allres)} distinct seeds; {'with' if len(paths) > 101 else 'WITHOUT'} the SEED+1..50 set)")
    F3.summarize(allres, "pooled G-only", log, rng)
    kur = []
    for fp in ("can", "alt"):
        g = np.array([r[fp]["g"] for r in allres]); z = (g - g.mean()) / g.std()
        log(f"    [{fp}] gamma-hat distribution over builds: skew {np.mean(z**3):+.2f}, excess kurtosis {np.mean(z**4)-3:+.2f}; quantisation step of gamma-hat 0.0025 (distinct values {len(set(np.round(g,4)))})")
    assert C.guard() == h0
    log("guard after run ok")


if __name__ == "__main__":
    main()
