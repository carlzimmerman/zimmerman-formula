"""Step 3: bootstrap, leave-one-out, 4-of-7 splits, k grid, propagation to keys, passing windows."""
import sys, json, itertools, math
import numpy as np
from scipy.interpolate import PchipInterpolator as PI
from scipy.stats import chi2 as chi2dist
import cu1_core as c
out_name = sys.argv[1] if len(sys.argv) > 1 else "cu1_stress.json"
xc = c.XC(); sh = c.Shear(); out = {}
FIT = [0, 2, 4, 6]
def wt_of(ids):
    w = np.zeros(7)
    for i in ids:
        w[i] += 1
    return w
def pct(v, w=None):
    v = np.asarray(v, float)
    if w is None:
        w = np.ones(v.size)
    o = np.argsort(v); cw = np.cumsum(w[o]) / w.sum()
    return [float(v[o][np.searchsorted(cw, q)]) for q in (0.16, 0.5, 0.84)]
for foot in ("canonical", "alt"):
    r = {}
    k0 = xc.fit(foot, wt_of(FIT))
    # bootstrap of the four, exact
    ms = list(itertools.combinations_with_replacement(FIT, 4))
    pw = []
    k4 = []
    for s in ms:
        cnt = [s.count(i) for i in FIT]
        pw.append(math.factorial(4) / np.prod([math.factorial(q) for q in cnt]) / 4**4)
        k4.append(xc.fit(foot, wt_of(s)))
    k4 = np.array(k4); pw = np.array(pw)
    rng = np.random.default_rng(20261102)
    k7 = np.array([xc.fit(foot, np.bincount(rng.integers(0, 7, 7), minlength=7)) for _ in range(2000)])
    r["k_fit"] = k0
    r["boot4"] = dict(n=len(ms), pct=pct(k4, pw), sd=float(np.sqrt((pw * (k4 - (pw * k4).sum())**2).sum())), min=float(k4.min()), max=float(k4.max()))
    r["boot7"] = dict(n=2000, pct=pct(k7), sd=float(k7.std(ddof=1)), min=float(k7.min()), max=float(k7.max()))
    r["k_all7"] = xc.fit(foot, np.ones(7))
    r["loo4"] = {xc.names[i]: xc.fit(foot, wt_of([j for j in FIT if j != i])) for i in FIT}
    r["loo7"] = {xc.names[i]: xc.fit(foot, wt_of([j for j in range(7) if j != i])) for i in range(7)}
    r["single"] = {xc.names[i]: xc.fit(foot, wt_of([i])) for i in range(7)}
    splits = []
    for s in itertools.combinations(range(7), 4):
        k = xc.fit(foot, wt_of(s)); h = [i for i in range(7) if i not in s]
        m, rms = xc.stat(foot, k, h); ma, ra = xc.stat(foot, k)
        splits.append(dict(fit=[xc.names[i] for i in s], k=k, hold_mean=m, hold_rms=rms, all_mean=ma, all_rms=ra, hold_pass=bool(abs(m) <= .05 and rms <= .1), all_pass=bool(abs(ma) <= .05 and ra <= .1)))
    # k grid, direct
    span = max(k4.max(), k7.max(), max(s["k"] for s in splits))
    grid = np.unique(np.concatenate([np.linspace(0, span * 1.05, 22), [k0]]))
    Z = {hk: np.zeros((grid.size, 15)) for hk in c.HS}
    for j, k in enumerate(grid):
        for hk in c.HS:
            res, nb, _ = sh.grade(foot, hk, float(k))
            Z[hk][j] = [res[q]["Z"] for q in sh.KEYS]
    r["grid"] = grid.tolist(); r["Zgrid"] = {hk: Z[hk].tolist() for hk in c.HS}
    itp = {hk: PI(grid, Z[hk], axis=0) for hk in c.HS}
    def summary(k):
        zz = {hk: itp[hk](k) for hk in c.HS}
        worst = np.max([np.abs(zz[hk]) for hk in c.HS], axis=0)
        ps = []
        for hk in c.HS:
            res = {q: {"Z": zz[hk][j]} for j, q in enumerate(sh.KEYS)}
            ps.append(sh.joint(foot, hk, res)[2])
        return zz, int((worst <= 2).sum()), min(ps), ps
    def prop(ks, wts=None):
        wts = np.ones(len(ks)) if wts is None else wts
        wts = wts / wts.sum()
        cnt = {}; all_, m3, pj = [], [], []
        for k, w in zip(ks, wts):
            zz, n, p, _ = summary(float(k))
            cnt[n] = cnt.get(n, 0) + w
            all_.append(zz["h0672"][sh.KEYS.index("G-OUT-all")]); m3.append(zz["h0672"][sh.KEYS.index("G-OUT-M3")]); pj.append(p)
        return dict(count_prob={str(a): float(b) for a, b in sorted(cnt.items())},
                    P15=float(cnt.get(15, 0)), Pge14=float(sum(v for a, v in cnt.items() if a >= 14)),
                    OUTall=pct(all_, wts), M3=pct(m3, wts), joint_p_worse=pct(pj, wts),
                    P_joint_pass=float(sum(w for p, w in zip(pj, wts) if p >= .05)))
    r["prop_boot4"] = prop(k4, pw)
    r["prop_boot7"] = prop(k7[:600])
    r["prop_note"] = "boot7 propagated on the first 600 of 2000 k draws"
    r["prop_splits"] = prop([s["k"] for s in splits])
    # Z_k per key
    sk = {"boot4": r["boot4"]["sd"], "boot7": r["boot7"]["sd"]}
    dz = {hk: itp[hk].derivative()(k0) for hk in c.HS}
    r["dZdk"] = {hk: {q: float(dz[hk][j]) for j, q in enumerate(sh.KEYS)} for hk in c.HS}
    r["Z_k_err_boot7"] = {q: float(abs(dz["h0672"][j]) * sk["boot7"]) for j, q in enumerate(sh.KEYS)}
    r["Z_k_err_boot4"] = {q: float(abs(dz["h0672"][j]) * sk["boot4"]) for j, q in enumerate(sh.KEYS)}
    fine = np.linspace(0, grid[-1], 4001)
    zf = {hk: itp[hk](fine) for hk in c.HS}
    wr = np.max([np.abs(zf[hk]) for hk in c.HS], axis=0)
    win = {}
    for j, q in enumerate(sh.KEYS):
        ok = wr[:, j] <= 2
        win[q] = [float(fine[ok].min()), float(fine[ok].max())] if ok.any() else None
    r["pass_window"] = win
    n = (wr <= 2).sum(1)
    r["max_keys"] = int(n.max())
    okm = n == n.max()
    r["max_keys_window"] = [float(fine[okm].min()), float(fine[okm].max())]
    r["max_keys_failing"] = [q for j, q in enumerate(sh.KEYS) if wr[okm][0, j] > 2]
    r["count_by_k"] = {("%.2f" % fine[i]): int(n[i]) for i in range(0, fine.size, 200)}
    # interpolation accuracy at k0 vs the direct cell
    r["splits"] = splits
    g = json.load(open("cu1_grade.json"))[foot]
    r["itp_err_at_k0"] = float(max(abs(itp[hk](k0)[j] - g[hk]["Z"][q]) for hk in c.HS for j, q in enumerate(sh.KEYS)))
    r["itp_err_midgrid"] = None
    hk = "h0672"; km = 0.5 * (grid[8] + grid[9]); res, _, _ = sh.grade(foot, hk, float(km))
    r["itp_err_midgrid"] = float(max(abs(itp[hk](km)[j] - res[q]["Z"]) for j, q in enumerate(sh.KEYS)))
    out[foot] = r
    print(foot, "k", round(k0, 3), "all7", round(r["k_all7"], 3), "boot4", r["boot4"], "boot7", r["boot7"])
    print(" loo4", {a: round(b, 2) for a, b in r["loo4"].items()})
    print(" loo7", {a: round(b, 2) for a, b in r["loo7"].items()})
    print(" single", {a: round(b, 2) for a, b in r["single"].items()})
    print(" splits k %.2f..%.2f, hold_pass %d/35, all_pass %d/35" % (min(s["k"] for s in splits), max(s["k"] for s in splits), sum(s["hold_pass"] for s in splits), sum(s["all_pass"] for s in splits)))
    for nm in ("prop_boot4", "prop_boot7", "prop_splits"):
        print(" ", nm, r[nm])
    print(" Z_k boot7", {q[2:]: round(v, 2) for q, v in r["Z_k_err_boot7"].items()})
    print(" windows", {q[2:]: (None if v is None else [round(v[0], 1), round(v[1], 1)]) for q, v in win.items()})
    print(" max keys", r["max_keys"], r["max_keys_window"], r["max_keys_failing"], "itp", r["itp_err_at_k0"], r["itp_err_midgrid"])
json.dump(out, open(out_name, "w"), indent=1, sort_keys=True)
