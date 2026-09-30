"""CFG236 attack (d): prior-dominated gas.  Frozen grid G0-G9.  Seed 2363."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG236_common as c

SEED = 2363
B = 2000
NDRAW = 1000
o = c.Out("attack_d")
c.header(o, "CFG236 attack (d): prior-dominated gas")
T = c.load_numeric()
idx, cnt = c.sample(T)
C = c.get_cols(T, idx)
z = C["z"]
zmed = float(np.median(z))
ids = T["muse_id"][idx].astype(int)
lo95 = T["gas_density_lo95"][idx]
hi95 = T["gas_density_hi95"][idx]
Sig = C["Sig"]
pd = (hi95 >= 14) & (lo95 < 1)
o.P(f"prior-dominated (hi95 >= 14 and lo95 < 1): {int(pd.sum())} of {len(pd)} rows in S (all 126 rows: {int(np.sum((T['gas_density_hi95']>=14)&(T['gas_density_lo95']<1)))} of {int(np.isfinite(T['gas_density_hi95']).sum())})")
o.P(f"constrained rows (not prior-dominated), ids: {sorted(ids[~pd].tolist())}")
o.P(f"fitted Sigma_HI: median {np.median(Sig):.2f}, 16-84 [{np.percentile(Sig,16):.1f},{np.percentile(Sig,84):.1f}]; hi95 >= 14: {int((hi95>=14).sum())}; lo95 < 1: {int((lo95<1).sum())}; Sigma within 5..10: {int(((Sig>5)&(Sig<10)).sum())}")
o.P(f"  Spearman(z, fitted Sigma_HI) = {c.stats.spearmanr(z, Sig)[0]:+.2f} (a z-trend in the gas prior would feed route (ii))")
cons = {"R198": dict(mode="R198")}
DAT = c.dat_available()
if DAT:
    dat = c.load_dat(T, idx)
    cons["R199a"] = dict(mode="R199", gperp=c.gperp_reading(dat["v1"], C["Re"], C["incl"], "a"))


def sl(cfg, sel=None):
    R = c.routes(C, cfg)
    cols = {r: np.log10(R["a0_" + r]) for r in ("i", "ii", "iii")}
    if sel is not None:
        cols = {r: np.where(sel, v, np.nan) for r, v in cols.items()}
    out = {r: c.theil_sen(z, cols[r]) for r in cols}
    both = np.isfinite(cols["i"]) & np.isfinite(cols["ii"])
    out["d"] = c.theil_sen(z, np.where(both, cols["ii"], np.nan)) - c.theil_sen(z, np.where(both, cols["i"], np.nan))
    out["n_ii"] = int(np.isfinite(cols["ii"]).sum())
    return out


def pw_quant(u, med, lo, hi, cap=15.0):
    out = np.where(u < 0.025, lo * u / 0.025,
           np.where(u < 0.5, lo + (med - lo) * (u - 0.025) / 0.475,
            np.where(u < 0.975, med + (hi - med) * (u - 0.5) / 0.475, hi + (cap - hi) * (u - 0.975) / 0.025)))
    return out


res = {}
for nm, base in cons.items():
    o.P(f"\n=== {nm} ===")
    prim = c.routes(C, base)
    cols = {r: np.log10(prim["a0_" + r]) for r in ("i", "ii", "iii")}
    st, _ = c.slope_table(z, cols, B, SEED, {"d": ("i", "ii")})
    hw = 0.5 * (st["ii"]["hi"] - st["ii"]["lo"])
    o.P(f"primary: b_i {st['i']['b']:+.3f}; b_ii {st['ii']['b']:+.3f} [{st['ii']['lo']:+.3f},{st['ii']['hi']:+.3f}] (half-width {hw:.3f}); Delta b {st['d']['b']:+.3f}")
    G = {}
    grid = [("G0 fitted median", {}), ("G1 Sigma=0", dict(Sig=0.0)), ("G2 Sigma=15", dict(Sig=15.0)), ("G3 Sigma=7.5", dict(Sig=7.5)),
            ("G6 tilt +0.3", dict(Sig=Sig * 10 ** (0.3 * (z - zmed)))), ("G6 tilt -0.3", dict(Sig=Sig * 10 ** (-0.3 * (z - zmed)))),
            ("G8 coeff x0.5", dict(gcoef=0.5)), ("G8 coeff x2", dict(gcoef=2.0)),
            ("G9 H2 x0.5", dict(mu_scale=0.5)), ("G9 H2 x2", dict(mu_scale=2.0)),
            ("G9 H2 tilt +0.3", dict(tH=0.3)), ("G9 H2 tilt -0.3", dict(tH=-0.3))]
    for lab, cfg in grid:
        s = sl(dict(base, **cfg))
        G[lab] = s
        o.P(f"   {lab:18s}: b_i {s['i']:+.3f}  b_ii {s['ii']:+.3f}  b_iii {s['iii']:+.3f}  Delta b {s['d']:+.3f}  n(ii) {s['n_ii']}")
    # G7 constrained only
    s7 = sl(base, sel=~pd)
    o.P(f"   G7 constrained rows only (n={int((~pd).sum())}): b_i {s7['i']:+.3f}  b_ii {s7['ii']:+.3f} (n_ii {s7['n_ii']})  b_iii {s7['iii']:+.3f}  Delta b {s7['d']:+.3f}")
    s7b = sl(base, sel=pd)
    o.P(f"   prior-dominated rows only (n={int(pd.sum())}): b_i {s7b['i']:+.3f}  b_ii {s7b['ii']:+.3f}  b_iii {s7b['iii']:+.3f}  Delta b {s7b['d']:+.3f}")
    G["G7"] = s7
    # G4, G5 draws
    rng = np.random.default_rng(SEED)
    for lab in ("G4 U(0,15)", "G5 posterior quantile"):
        vals = []
        dd = []
        for t in range(NDRAW):
            if lab.startswith("G4"):
                sg = rng.uniform(0, 15, len(z))
            else:
                sg = pw_quant(rng.uniform(0, 1, len(z)), Sig, lo95, hi95)
            s = sl(dict(base, Sig=sg))
            vals.append(s["ii"]); dd.append(s["d"])
        vals = np.array(vals); dd = np.array(dd)
        q = np.nanpercentile(vals, [2.5, 50, 97.5])
        o.P(f"   {lab}: b_ii mean {np.nanmean(vals):+.3f} SD {np.nanstd(vals):.3f}, 2.5/50/97.5 = {q[0]:+.3f}/{q[1]:+.3f}/{q[2]:+.3f}; Delta b mean {np.nanmean(dd):+.3f} SD {np.nanstd(dd):.3f}")
        G[lab] = dict(mean=float(np.nanmean(vals)), sd=float(np.nanstd(vals)), q=q.tolist(), d_mean=float(np.nanmean(dd)))
    core = [G[k]["ii"] for k in ("G0 fitted median", "G1 Sigma=0", "G2 Sigma=15", "G3 Sigma=7.5", "G6 tilt +0.3", "G6 tilt -0.3", "G8 coeff x0.5", "G8 coeff x2")]
    Rg = 0.5 * (max(core) - min(core))
    Rg_all = max(Rg, 0.5 * (G["G4 U(0,15)"]["q"][2] - G["G4 U(0,15)"]["q"][0]), 0.5 * (G["G5 posterior quantile"]["q"][2] - G["G5 posterior quantile"]["q"][0]))
    ratio = Rg / hw
    cl = "contained" if ratio <= 0.25 else ("partly" if ratio <= 1.0 else "dominates")
    o.P(f"   R_g (half-range of b_ii over G0-G3, G6, G8) = {Rg:.3f}; with the G4/G5 2.5-97.5 half-ranges {Rg_all:.3f}; bootstrap half-width {hw:.3f}; ratio {ratio:.2f} -> '{cl}'")
    o.P(f"   total interval (bootstrap CI widened linearly by R_g): [{st['ii']['lo']-Rg:+.3f},{st['ii']['hi']+Rg:+.3f}]")
    refs = c.ref_slopes(z[np.isfinite(cols["ii"])])
    tot = dict(b=st["ii"]["b"], lo=st["ii"]["lo"] - Rg, hi=st["ii"]["hi"] + Rg, sd=st["ii"]["sd"])
    o.P(f"   with the gas range included: laws inside/outside the widened interval: { {k: (tot['lo'] <= v <= tot['hi']) for k, v in refs.items()} }")
    res[nm] = dict(primary=st, grid=G, Rg=Rg, Rg_all=Rg_all, hw=hw, ratio=ratio, cls=cl, constrained_ids=sorted(ids[~pd].tolist()), n_pd=int(pd.sum()))
o.res = dict(res, n_pd=int(pd.sum()))
o.finish()
sys.exit(0)
