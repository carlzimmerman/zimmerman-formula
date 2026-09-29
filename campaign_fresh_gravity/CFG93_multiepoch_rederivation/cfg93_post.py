"""CFG93 POST-HOC block (written and run AFTER the frozen main and MUTATE runs; not part of the pass lines).
P1 star-level influence tables (which stars carry the cleaned sigma);
P2 exceedance probabilities: with sigma_true = the bare-law sigma, how often does a DM91-like binary population at the real
   cadence (exact stars, not resampled) give a sigma at least as large as observed (single, all-epoch mean, cleaned) and a
   single/all-mean ratio at least as large as observed?
P3 |g| error definitions for the Tuc II gradient."""
import os, sys, math, numpy as np, pandas as pd
from multiprocessing import Pool
from scipy import stats
import cfg93 as C
def sim_exact(rng, pool, sigma, fbin, pop):
    N = len(pool); idx = np.arange(N)
    ne = np.array([len(pool[i][1]) for i in idx]); starts = np.concatenate([[0], np.cumsum(ne)[:-1]])
    T = np.concatenate([pool[i][0] - pool[i][0][0] for i in idx]); E = np.concatenate([pool[i][1] for i in idx])
    sid = np.repeat(np.arange(N), ne)
    v0 = rng.normal(0, sigma, N); isb = rng.random(N) < fbin; nb = int(isb.sum())
    V = v0[sid] + rng.normal(size=len(E)) * E
    if nb:
        o = C.sample_orbits(rng, nb, pop); bmap = -np.ones(N, int); bmap[isb] = np.arange(nb)
        m = isb[sid]; bi = bmap[sid[m]]; V[m] += C.kepler_rv(T[m], {k: v[bi] for k, v in o.items()})
    W = 1 / E**2; sw = np.add.reduceat(W, starts); vm = np.add.reduceat(W * V, starts) / sw; em = 1 / np.sqrt(sw)
    chi2 = np.add.reduceat(W * (V - vm[sid])**2, starts)
    pv = np.where(ne >= 2, stats.chi2.sf(chi2, np.maximum(ne - 1, 1)), 1.0); keep = pv >= 0.01
    s1 = C.fit_sigma(V[starts], E[starts], False)["s"]; sa = C.fit_sigma(vm, em, False)["s"]; sc = C.fit_sigma(vm[keep], em[keep], False)["s"]
    return s1, sa, sc, int((~keep).sum())
def _job(a):
    name, pool, sigma, f, pop, n, seed, obs = a
    rng = np.random.default_rng(seed); r = np.array([sim_exact(rng, pool, sigma, f, pop) for _ in range(n)])
    s1, sa, sc, nf = r.T
    return dict(name=name, sigma=sigma, f=f, pop=pop, n=n,
                P_single=float((s1 >= obs["single"]).mean()), P_all=float((sa >= obs["allmean"]).mean()),
                P_clean=float((sc >= obs["clean"]).mean()), P_joint=float(((s1 >= obs["single"]) & (sc >= obs["clean"])).mean()),
                P_ratio=float(((s1 / np.maximum(sa, 1e-9)) >= obs["single"] / obs["allmean"]).mean()),
                P_shrink=float(((sa / np.maximum(sc, 1e-9)) >= 1.0).mean()),
                med_single=float(np.median(s1)), med_all=float(np.median(sa)), med_clean=float(np.median(sc)), mean_flag=float(nf.mean()))
if __name__ == "__main__":
    lvd = pd.read_csv(os.path.join(C.REPO, "dsph", "lvd_dwarf_mw.csv")).set_index("key")
    stars = C.build_stars(C.parse(), lvd)
    out = []
    for key in ("bootes_1", "tucana_2"):
        r = C.run_pipeline(stars, lvd, key, dict(C.DEF)); ids = r["idx"]
        print(f"\n=== P1 {C.NAMES[key]}: members (N_ep, mean v, e_mean, chi2, dof, p, flagged) sorted by |v-median| ===")
        vmed = np.median([stars[key][i]["vm"] for i in ids])
        rows = []
        for i in ids:
            s = stars[key][i]; n = len(s["v"]); m, em_, c2 = C.star_stats(s["v"], s["e"]); p = stats.chi2.sf(c2, n - 1) if n > 1 else np.nan
            rows.append((abs(m - vmed), n, m, em_, c2, n - 1, p, (n > 1 and p < 0.01)))
        rows.sort(reverse=True)
        for x in rows[:10]: print("  Nep %2d  v %8.2f  e %5.2f  chi2 %8.1f dof %2d  p %.2e  %s" % (x[1], x[2], x[3], x[4], x[5], x[6] if x[6] == x[6] else -1, "FLAGGED" if x[7] else ""))
        # leave-one-out sigma_clean
        vm, em = r["vm"], r["em"]; base = C.fit_sigma(vm, em)["s"]
        loo = np.array([C.fit_sigma(np.delete(vm, j), np.delete(em, j))["s"] for j in range(len(vm))])
        print(f"  cleaned sigma {base:.3f}; leave-one-out range {loo.min():.3f}-{loo.max():.3f}; largest single-star change {np.max(np.abs(loo-base)):.3f} km/s (offset shift {math.log10(loo.min()/base):+.3f} / {math.log10(loo.max()/base):+.3f})")
        # cleaning-aggressiveness ladder
        print("  ladder (sigma, offset canon): single %.2f (%+.3f) | allmean %.2f (%+.3f) | clean p<0.01 %.2f (%+.3f) | paperflag %.2f (%+.3f)" % (
            r["single"]["s"], r["off_single_canon"][0], r["allmean"]["s"], r["off_allmean_canon"][0], r["clean"]["s"], r["off_clean_canon"][0], r["paperflag"]["s"], r["off_paperflag_canon"][0]))
    # P2
    print("\n=== P2 exceedance probabilities (exact real cadence, sigma_true = bare-law sigma) ===")
    jobs = []; sd = 1
    for key in ("bootes_1", "tucana_2"):
        r = C.run_pipeline(stars, lvd, key, dict(C.DEF)); pool = [(stars[key][i]["t"], stars[key][i]["e"]) for i in r["idx"]]
        obs = dict(single=r["single"]["s"], allmean=r["allmean"]["s"], clean=r["clean"]["s"]); sg = r["sl"]["canon"]
        for pop in ("dm91", "dm91nocut", "meanlogP4", "flat"):
            for f in (0.5, 0.9):
                sd += 1; jobs.append((C.NAMES[key], pool, sg, f, pop, 3000, sd, obs))
    with Pool(16) as pl: res = pl.map(_job, jobs)
    print(f"{'sys':6s}{'pop':>10s}{'f':>5s} | P(single>=obs) P(all>=obs) P(clean>=obs) P(joint) P(single/all>=obs) | med single/all/clean | mean n_flag")
    for x in res:
        print(f"{x['name']:6s}{x['pop']:>10s}{x['f']:5.1f} | {x['P_single']:14.4f}{x['P_all']:11.4f}{x['P_clean']:13.4f}{x['P_joint']:9.4f}{x['P_ratio']:19.4f} | {x['med_single']:.2f}/{x['med_all']:.2f}/{x['med_clean']:.2f} | {x['mean_flag']:.2f}")
    # P3
    rt = C.run_pipeline(stars, lvd, "tucana_2", dict(C.DEF)); L = lvd.loc["tucana_2"]; ids = rt["idx"]; kept = [ids[j] for j in range(len(ids)) if rt["keep"][j]]
    xi, eta = C.tangent(np.array([stars["tucana_2"][i]["ra"] for i in kept]), np.array([stars["tucana_2"][i]["de"] for i in kept]), L["ra"], L["dec"])
    g1 = C.grad_fit(rt["vm"], rt["em"], xi, eta, True); a, b = g1["beta"][1], g1["beta"][2]; cv = g1["cov"]
    g = math.hypot(a, b); var = (a * a * cv[1, 1] + 2 * a * b * cv[1, 2] + b * b * cv[2, 2]) / g**2
    print(f"\n=== P3 Tuc II |g| = {g:.3f}; error along the gradient direction sqrt((a^2Caa+2abCab+b^2Cbb))/|g| = {math.sqrt(var):.2f}; per-half-light-radius (rhalf {L['rhalf']/60:.3f} deg): {g*L['rhalf']/60:.3f} +/- {math.sqrt(var)*L['rhalf']/60:.2f}; xi,eta extent {np.ptp(xi):.3f},{np.ptp(eta):.3f} deg")

    # P4: alternative sigma_law conventions found by reading CFG51 AFTER the frozen runs: R = LVD rhalf_sph_physical (circularised), floor = half the
    # range of the offset over Upsilon_V {1,2,4} and the deep-MOND estimator
    print("\n=== P4 sigma_law convention check (post-hoc; CFG51 script read only after the frozen runs) ===")
    def sl2(MV, Rpc, ups, a0, deep=False):
        Ms = ups * 10**(0.4 * (4.83 - MV)); r = 4 / 3 * Rpc; Mb = Ms / 2; gN = C.G_PC * Mb / r**2; a0p = a0 * C.PC_M / 1e6
        g = math.sqrt(gN * a0p) if deep else gN * C.nu(gN / a0p); return math.sqrt(g * r / 3)
    ref = {"bootes_1": (0.21939, 0.08913, 2.4613), "tucana_2": (0.46493, 0.12825, 3.6251)}
    for key in ("bootes_1", "tucana_2"):
        L = lvd.loc[key]; r = C.run_pipeline(stars, lvd, key, dict(C.DEF)); fit = r["clean"]
        for lab, Rpc in (("R=rhalf_arcmin*d (frozen)", C.sigma_law(L["M_V"], L["rhalf"], L["distance"], C.A0["canon"])[2]), ("R=rhalf_sph_physical", L["rhalf_sph_physical"])):
            offs = [math.log10(fit["s"] / sl2(L["M_V"], Rpc, u, C.A0["canon"])) for u in (1.0, 2.0, 4.0)] + [math.log10(fit["s"] / sl2(L["M_V"], Rpc, 2.0, C.A0["canon"], True))]
            fl = 0.5 * (max(offs) - min(offs)); off = offs[1]
            up = math.log10((fit["s"] + fit["up"]) / fit["s"]); dn = math.log10(fit["s"] / (fit["s"] - fit["dn"])); st = 0.5 * (up + dn)
            tot = math.hypot(st, fl)
            print(f"  {C.NAMES[key]:6s} {lab:28s} sigma_law {sl2(L['M_V'], Rpc, 2.0, C.A0['canon']):.4f} offset {off:+.5f} floor {fl:.5f} stat {st:.5f} err {tot:.5f} z {off/tot:.4f}   [CFG51 unrounded: off {ref[key][0]:+.5f} err {ref[key][1]:.5f} z {ref[key][2]:.4f}]")
    # P5: bigger parametric bootstrap for the Boo I mixture LR
    r = C.run_pipeline(stars, lvd, "bootes_1", dict(C.DEF)); vm, em = r["vm"], r["em"]; e2 = em**2
    one = C.fit_sigma(vm, em); mu1 = float(np.average(vm, weights=1 / (one["s"]**2 + e2)))
    T0 = one["m2"] + len(vm) * math.log(2 * math.pi) - C.fit_mix(vm, e2)["m2"]
    args = [(50000 + b, mu1, one["s"], e2) for b in range(4000)]
    with Pool(16) as pl: Tb = np.array(pl.map(C._boot_one, args))
    Tb = np.maximum(Tb, 0.0)
    print(f"\n=== P5 Boo I LR bootstrap, 4000 draws: T={T0:.3f}; P(T*>=T) = {np.mean(Tb >= T0):.4f} +/- {math.sqrt(np.mean(Tb>=T0)*(1-np.mean(Tb>=T0))/4000):.4f}; null median {np.median(Tb):.3f}, 95th pct {np.percentile(Tb, 95):.2f}; fraction with T*=0 {np.mean(Tb<=1e-6):.3f}")

    # P6: restrict to stars whose variability is TESTABLE (>=2 or >=3 epochs) and unflagged
    print("\n=== P6 testable stars only (post-hoc) ===")
    for key in ("bootes_1", "tucana_2"):
        r = C.run_pipeline(stars, lvd, key, dict(C.DEF)); ids = r["idx"]; sl = r["sl"]["canon"]
        nep = np.array([len(stars[key][i]["v"]) for i in ids]); vmA = np.array([stars[key][i]["vm"] for i in ids]); emA = np.array([stars[key][i]["em"] for i in ids])
        keep = r["keep"]
        for lab, msk in (("all cleaned", keep), (">=2 epochs, cleaned", keep & (nep >= 2)), (">=3 epochs, cleaned", keep & (nep >= 3)), ("single-epoch only (untestable)", nep == 1)):
            if msk.sum() < 3: continue
            f = C.fit_sigma(vmA[msk], emA[msk])
            o = C.off_err(f, sl) if f["s"] > 0 else None
            print(f"  {C.NAMES[key]:6s} {lab:32s} N={int(msk.sum()):3d} sigma {f['s']:.2f} (+{f['up'] if f['up'] is not None else float('nan'):.2f} -{f['dn'] if f['dn'] is not None else float('nan'):.2f})  offset {'%+.3f +/- %.3f (%.2f sig)' % (o[0], o[1], o[0]/o[1]) if o else 'sigma=0 (UL only)'}")
