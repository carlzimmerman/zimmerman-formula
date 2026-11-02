#!/usr/bin/env python3
"""AF1 stage 2: Pi reduction, model-free ranking, sample-identity control, separability. No formula. FROZEN_CRITERIA.md, AMENDMENT_A1.md.
kappa = 1/2 FITTED; not theory closed."""
import csv, hashlib, json, math, os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.stats import rankdata
from sklearn.feature_selection import mutual_info_regression
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); OUT = []
PLANT = "--plant" in sys.argv; PLANT2 = "--plant2" in sys.argv; TAG = "_PLANT" if PLANT else "_PLANT2" if PLANT2 else ""; SEED = 20261102
def P(s): print(s, flush=True); OUT.append(s)
def load(foot):
    R = list(csv.DictReader(open(os.path.join(HERE, f"af1_table_{foot}.csv")))); D = {k: np.array([x[k] for x in R]) for k in ("sample", "system", "split_id", "method")}
    for k in R[0]:
        if k not in D: D[k] = np.array([float(x[k]) if x[k] != "" else np.nan for x in R])
    l10 = lambda a: np.log10(np.where(a > 0, a, np.nan)); V = dict(ly=l10(D["y"]), ly_gas=l10(D["y_gas"]), ly_star=l10(D["y_star"]), f_gas=np.where(np.isin(D["sample"], ["dwarfs", "shearM", "shearT"]), np.nan, D["f_gas"]), lell=l10(D["ell"]), lx_rad=l10(D["x_rad"]), gas_slope=D["gas_slope"], lsig_eff=l10(D["sig_eff"]), morph=D["morph"], env_dens=np.log10(1 + D["env_dens"]), env_halo=D["env_halo"], lx_host=l10(D["x_host"]), ld_host=l10(D["d_host"]), lz=l10(D["z"]), m_sys=D["m_sys"], lkT=l10(D["kT_cl"]), lM500=np.where(D["sample"] == "XCOP", np.nan, D["lM500"]), lM500_HSE=np.where(D["sample"] == "XCOP", D["lM500"], np.nan), lv2c=l10(D["leaky_v2c"]))
    return D, V
LEAKY = {"lv2c", "lM500_HSE"}
SAMPLES = ["SPARC", "LT", "groups", "XCOP", "shearM", "dwarfs", "MW"]; CLUST = {"XCOP", "shearM"}
MOCK = dict(SPARC=.10, LT=.15, groups=.10, XCOP=.05, shearM=.05, shearT=.05, dwarfs=.15, MW=.05)
def law(g, a=1.0): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
def rho(a, b):
    a = a - a.mean(); b = b - b.mean(); d = np.sqrt((a * a).sum() * (b * b).sum()); return float((a * b).sum() / d) if d > 0 else 0.0
def part(a, ly):
    d = 3 if len(a) >= 12 else 1; X = np.vander((ly - ly.mean()) / (ly.std() + 1e-9), d + 1); return a - X @ np.linalg.lstsq(X, a, rcond=None)[0]
def perm_between(x, y, rng, line=None):
    x = x - x.mean(); y = y - y.mean(); n = len(x); nrm = math.sqrt((x * x).sum() * (y * y).sum()); ob = abs((x * y).sum() / nrm); c = 0; tot = 0; floor = 2.0 / math.factorial(n) if n < 12 else 0.0
    for N in (2000, 18000):
        for k in range(0, N, 500):
            ix = np.argsort(rng.random((min(500, N - k), n)), axis=1); c += int((np.abs((x[ix] * y).sum(1) / nrm) >= ob - 1e-12).sum()); tot += ix.shape[0]
        if (c + 1) / (tot + 1) > .01: break
    return (c + 1) / (tot + 1), floor
def perm_within(rx, ry, sy, rng):
    """sign flip per system on the demeaned variable. Exact when few systems"""
    u, inv = np.unique(sy, return_inverse=True); S = np.bincount(inv, rx * ry, len(u)); nrm = math.sqrt((rx * rx).sum() * (ry * ry).sum()); ob = abs(S.sum() / nrm); K = len(u)
    if K <= 14:
        F = ((np.arange(2 ** K)[:, None] >> np.arange(K)) & 1) * 2 - 1; return float((np.abs(F @ S / nrm) >= ob - 1e-12).mean()), 2.0 ** (1 - K)
    c = 0; tot = 0
    for N in (2000, 18000):
        for k in range(0, N, 1000):
            F = rng.integers(0, 2, (min(1000, N - k), K)) * 2 - 1; c += int((np.abs(F @ S / nrm) >= ob - 1e-12).sum()); tot += F.shape[0]
        if (c + 1) / (tot + 1) > .01: break
    return (c + 1) / (tot + 1), 0.0
def demean(a, inv, K):
    return a - (np.bincount(inv, a, K) / np.bincount(inv, minlength=K))[inv]
def tests(foot, D, V, r, rng):
    Tb = []
    for s in SAMPLES + ["shearT"]:
        m = D["sample"] == s
        for vn, vv in V.items():
            if s == "shearT" and vn != "lkT" and vn != "lM500": continue
            q = m & np.isfinite(vv)
            if q.sum() < 8 or np.nanstd(vv[q]) < 1e-9: continue
            ly = V["ly"][q]; sy = D["system"][q]; x = vv[q]; y = r[q]; u, inv = np.unique(sy, return_inverse=True); K = len(u)
            # mock noise leak
            def mock(mode):
                o = []
                g = np.random.default_rng(SEED + 7)
                for _ in range(20):
                    e = g.normal(0, MOCK[s], K)[inv]; yt = 10 ** ly * 10 ** (-e); rm = np.log10(law(yt) / law(10 ** ly))
                    if mode == "b":
                        a = np.bincount(inv, rm, K) / np.bincount(inv, minlength=K); b = np.bincount(inv, x, K) / np.bincount(inv, minlength=K); o.append(abs(rho(rankdata(a), rankdata(b))))
                    else: o.append(abs(rho(demean(rankdata(rm), inv, K), demean(rankdata(x), inv, K))))
                return float(np.mean(o))
            if K >= 5:
                a = np.bincount(inv, y, K) / np.bincount(inv, minlength=K); b = np.bincount(inv, x, K) / np.bincount(inv, minlength=K); ll = np.bincount(inv, ly, K) / np.bincount(inv, minlength=K)
                if np.std(b) > 1e-9:
                    ra, rb = rankdata(a), rankdata(b); p, fl = perm_between(rb, ra, rng); pp = np.nan
                    if vn != "ly": pp, _ = perm_between(part(rb, ll), part(ra, ll), rng)
                    Tb.append(dict(sample=s, var=vn, level="between", n=K, rho=rho(ra, rb), p=p, floor=fl, p_partial=pp, mock=mock("b"), mi=float(mutual_info_regression(b[:, None], a, n_neighbors=min(5, K - 1), random_state=0)[0])))
            if q.sum() >= K + 6 and K >= 3:
                dx = demean(x, inv, K)
                if np.std(dx) > 1e-9:
                    rx = demean(rankdata(x), inv, K); ry = demean(rankdata(y), inv, K); p, fl = perm_within(rx, ry, sy, rng); pp = np.nan
                    if vn != "ly":
                        rl = demean(rankdata(ly), inv, K); pp, _ = perm_within(part(rx, rl), part(ry, rl), sy, rng)
                    Tb.append(dict(sample=s, var=vn, level="within", n=int(q.sum()), rho=rho(rx, ry), p=p, floor=fl, p_partial=pp, mock=mock("w"), mi=float(mutual_info_regression(dx[:, None], demean(y, inv, K), n_neighbors=5, random_state=0)[0])))
    return Tb
def shearcl(foot, rng):
    """A1: per cluster, MID and OUTER. Weighted Pearson on rank."""
    RE = os.path.dirname(HERE); from astropy.io import fits
    d = np.load(os.path.join(RE, "LM1_law_missing_mass_map", "cache_BASE_f034", "dump.npz")); X = np.load(os.path.join(RE, "X7_cluster_core_significance", "x7_measure_percluster.npz")); i = 1; h = "h0672"
    W = np.where(X["E"][:, i] < 1e8, 1 / X["E"][:, i] ** 2, 0); B0 = X["den"][:, i].sum(0) / X["den_r"][:, i].sum(0); n = W * B0[None, :] * (X["D"][:, i] - X["leakP"][:, 0, 0]); Vv = d[f"V_{foot}_{h}"]; Mb = d[f"Mb_{foot}_{h}"]; RC = d["RC"]
    E = fits.open(os.path.join(os.path.dirname(RE), "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data; nm = {str(s).strip(): k for k, s in enumerate(E["NAME"])}; KT = np.array([float(E["KT"][nm[str(s).strip()]]) if str(s).strip() in nm else np.nan for s in X["name"]]); KT[~np.isin(np.arange(len(KT)), d["I"])] = np.nan
    Rs = []; a0 = dict(canonical=9.360324825027975e-11, alt=1.1312e-10)[foot]
    for band, bins in (("MID", [3, 4, 5]), ("OUTER", [6, 7])):
        nn = n[:, bins].sum(1); vv = Vv[:, bins].sum(1); ok0 = vv > 0; A = nn / np.where(ok0, vv, 1); wt = vv ** 2 / np.maximum((W[:, bins] * 1.0).sum(1), 1e-300)  # V^2 / sum W: inverse variance of A
        yb = (6.674e-11 * Mb[:, bins[0]] * 1.989e30 / (RC[bins[0]] * 3.0857e22) ** 2) / a0
        for vn, x in (("ly_band", np.log10(np.maximum(yb, 1e-300))), ("lM500", np.log10(np.asarray(X["M500"], float))), ("lz", np.log10(np.asarray(X["z"], float))), ("lkT", np.log10(np.where(KT > 0, KT, np.nan)))):
            q = ok0 & np.isfinite(x) & np.isfinite(A); a = A[q]; w = wt[q] / wt[q].sum(); r_ = rankdata(x[q]); r_ = (r_ - (w * r_).sum()); aa = a - (w * a).sum(); nrm = math.sqrt((w * r_ * r_).sum() * (w * aa * aa).sum()); ob = (w * r_ * aa).sum() / nrm; c = 0; tot = 0
            for N in (2000, 18000):
                for k in range(0, N, 500):
                    ix = np.argsort(rng.random((min(500, N - k), len(a))), axis=1); ws = w[ix]; rr = r_[ix]; rr = rr - (ws * rr).sum(1, keepdims=True); am = (ws * a).sum(1, keepdims=True); aq = a - am
                    t = (ws * rr * aq).sum(1) / np.sqrt((ws * rr * rr).sum(1) * (ws * aq * aq).sum(1)); c += int((np.abs(t) >= abs(ob)).sum()); tot += len(t)
                if (c + 1) / (tot + 1) > .01: break
            # POST-RESULT column, own generator so raw p stay as first run: rank partial on the other two of (ly_band, lM500, lz)
            tri = dict(ly_band=np.log10(np.maximum(yb, 1e-300)), lM500=np.log10(np.asarray(X["M500"], float)), lz=np.log10(np.asarray(X["z"], float))); Z_ = np.column_stack([np.ones(q.sum())] + [rankdata(v_[q]) for k_, v_ in tri.items() if k_ != vn]); sw_ = np.sqrt(w)[:, None]; pr_ = lambda t_: t_ - Z_ @ np.linalg.lstsq(Z_ * sw_, t_ * sw_[:, 0], rcond=None)[0]; x_ = pr_(rankdata(x[q])); a_ = pr_(a); nr_ = math.sqrt((w * x_ * x_).sum() * (w * a_ * a_).sum()); ob_ = (w * x_ * a_).sum() / nr_; g_ = np.random.default_rng(SEED + 11); ix_ = np.argsort(g_.random((5000, len(a))), axis=1); pc_ = (int((np.abs((w * x_ * a_[ix_]).sum(1) / nr_) >= abs(ob_)).sum()) + 1) / 5001
            Rs.append(dict(sample="shearCL", var=vn, level=band, n=int(q.sum()), rho=float(ob), p=(c + 1) / (tot + 1), floor=0.0, p_partial=pc_, rho_partial=float(ob_), mock=0.0, mi=np.nan))
    return Rs
def holm(T):
    idx = [i for i, t in enumerate(T) if t["var"] not in LEAKY and t["var"] != "pure_noise"]; o = sorted(idx, key=lambda i: T[i]["p"]); N = len(o); mx = 0.0
    for k, i in enumerate(o):
        mx = max(mx, min(1.0, T[i]["p"] * (N - k))); T[i]["p_holm"] = mx; T[i]["line"] = 0.05 / (N - k)
        T[i]["floor_lbl"] = bool(T[i]["floor"] > 0.05 / N)
    for i, t in enumerate(T):
        t.setdefault("p_holm", float("nan")); t.setdefault("line", float("nan")); t.setdefault("floor_lbl", False)
    return N
def binned(V_, r, w, nb=10):
    e = np.unique(np.quantile(V_, np.linspace(0, 1, nb + 1))); e[0] -= 1e-9; e[-1] += 1e-9; b = np.digitize(V_, e) - 1; return e, b
def eqw(samp):
    w = np.zeros(len(samp));
    for s in set(samp): w[samp == s] = 1.0 / (samp == s).sum()
    return w
def pooled_gain(x, r, w, nb=10):
    e, b = binned(x, r, w, nb); K = len(e) - 1; sw = np.bincount(b, w, K); m = np.bincount(b, w * r, K) / np.where(sw > 0, sw, 1); return 1 - (w * (r - m[b]) ** 2).sum() / (w * (r - (w * r).sum() / w.sum()) ** 2).sum()
def identity(D, V, r, rng, Nfam):
    samp = D["sample"]; mk = np.isin(samp, SAMPLES); Rs = {}; cl = np.isin(samp, list(CLUST))
    lab = dict(zip(SAMPLES, np.random.default_rng(SEED).permutation(len(SAMPLES)) * 1.0)); Vp = dict(V); Vp["LABEL_CONTROL"] = np.array([lab.get(s, np.nan) for s in samp])
    for vn, x in Vp.items():
        q = mk & np.isfinite(x); ss = sorted(set(samp[q]))
        if len(ss) < 2 or np.std(x[q]) < 1e-9: continue
        xq, rq, sq = x[q], r[q], samp[q]; w = eqw(sq); ob = pooled_gain(xq, rq, w); c = 0; tot = 0
        for N in (500, 1500, 18000):
            for _ in range(N):
                xp = xq.copy()
                for s in ss:
                    m = sq == s; xp[m] = rng.permutation(xq[m])
                c += pooled_gain(xp, rq, w) >= ob; tot += 1
            if (c + 1) / (tot + 1) > .01 or vn == "LABEL_CONTROL": break
        A = None; cg = cl[q]
        if cg.any() and (~cg).any():
            ra = rankdata(xq); wc = eqw(cg.astype(str)); A = float(((w * 0 + 1) * 0).sum()) ; n1 = cg.sum(); n0 = (~cg).sum(); A = float((ra[cg].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)); A = max(A, 1 - A)
        # LOSO
        lo = {}
        for s in ss:
            tr = sq != s; te = sq == s; xr = xq[tr]; rr = rq[tr]; wr = eqw(sq[tr]); e, b = binned(xr, rr, wr); K = len(e) - 1; sw = np.bincount(b, wr, K); mm = np.bincount(b, wr * rr, K) / np.where(sw > 0, sw, 1); cov = float(((xq[te] >= e[0]) & (xq[te] <= e[-1])).mean()); pr = mm[np.clip(np.digitize(xq[te], e) - 1, 0, K - 1)]; c0 = (wr * rr).sum() / wr.sum()
            sse = ((rq[te] - pr) ** 2).sum(); sst = (rq[te] ** 2).sum(); ssc = ((rq[te] - c0) ** 2).sum(); lo[s] = dict(cov=cov, R2_vs_law=float(1 - sse / sst), R2_vs_const=float(1 - sse / ssc), R2_const_vs_law=float(1 - ssc / sst))
        good = [s for s in lo if lo[s]["cov"] >= .5]; Rs[vn] = dict(gain=float(ob), p_strat=(c + 1) / (tot + 1), auc=A, loso=lo, n_cov=len(good), n_loso_pos=sum(1 for s in good if lo[s]["R2_vs_law"] > 0 and lo[s]["R2_vs_const"] > 0), samples=ss)
    return Rs
def sep_one(a, b, r, tr, te):
    def tab(x):
        e = np.unique(np.quantile(x[tr], np.linspace(0, 1, 7))); e[0] = -np.inf; e[-1] = np.inf; return np.clip(np.digitize(x, e) - 1, 0, len(e) - 2), len(e) - 1
    ia, na = tab(a); ib, nb = tab(b); mu = r[tr].mean(); f = np.zeros(na); h = np.zeros(nb)
    for _ in range(30):
        for k in range(na):
            m = tr & (ia == k); f[k] = (r[m] - mu - h[ib[m]]).mean() if m.any() else 0
        for k in range(nb):
            m = tr & (ib == k); h[k] = (r[m] - mu - f[ia[m]]).mean() if m.any() else 0
    add = mu + f[:, None] + h[None, :]; Tb = add.copy()
    for i in range(na):
        for j in range(nb):
            m = tr & (ia == i) & (ib == j)
            if m.sum() >= 3: Tb[i, j] = r[m].mean()
    u, s, vt = np.linalg.svd(Tb); pr = s[0] * np.outer(u[:, 0], vt[0]); rms = lambda M: float(np.sqrt(((r[te] - M[ia[te], ib[te]]) ** 2).mean())); c = float(np.sqrt(((r[te] - mu) ** 2).mean())); ra, rp, rf = rms(add), rms(pr), rms(Tb)
    if rf >= c * 0.98: L = "NOISE-LIMITED"
    else:
        gf = c - rf; ga = c - ra; gp = c - rp; A_ = ga >= .9 * gf; P_ = gp >= .9 * gf; L = "ADDITIVE and PRODUCT both" if A_ and P_ else "ADDITIVE" if A_ else "PRODUCT" if P_ else "NEITHER"
    return dict(const=c, add=ra, prod=rp, full=rf, label=L, n_te=int(te.sum()))
def separ(D, V, r):
    par = np.array([int(hashlib.sha256(s.encode()).hexdigest(), 16) % 2 for s in D["split_id"]]) == 0; s = D["sample"]; O = {}; reg = dict(clusters=np.isin(s, ["XCOP", "shearM"]), galaxies=np.isin(s, ["SPARC", "LT", "MW"]), pooled=np.isin(s, SAMPLES))
    names = ["ly", "ly_gas", "ly_star", "f_gas", "lell", "m_sys", "lx_rad"]
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            for rn, m in reg.items():
                q = m & np.isfinite(V[a]) & np.isfinite(V[b])
                if q.sum() < 30 or np.std(V[a][q]) < 1e-9 or np.std(V[b][q]) < 1e-9: continue
                tr = par[q]; te = ~par[q]
                if tr.sum() < 12 or te.sum() < 12: continue
                O[f"{a}|{b}|{rn}"] = sep_one(V[a][q], V[b][q], r[q], tr, te)
    return O
def pi_rank():
    # columns: g_bar, g_gas, g_star, R, Sigma, sigma_or_T(velocity^2), Phi_b, t_b, a0, c, G ; rows L, T, M
    names = ["g_bar", "g_gas", "g_star", "R", "Sigma_phot", "v_obs", "Phi_b", "t_b", "kT/m", "a0", "c", "G"]; Dm = np.array([[1, 1, 1, 1, -2, 1, 2, 0, 2, 1, 1, 3], [-2, -2, -2, 0, 0, -1, -2, 1, -2, -2, -1, -2], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -1]]); rk = int(np.linalg.matrix_rank(Dm)); return dict(variables=names, rank=rk, n_pi=len(names) - rk, basis="y=g_bar/a0, f=g_gas/g_bar (y_gas=f y, y_star=(1-f) y), ell=R a0/c^2, s=G Sigma_phot/a0, beta2=v_obs^2/c^2 [LEAKY], tau=kT/(m c^2), [Phi_b/c^2 = y ell and t_b a0/c = sqrt(ell/y) are redundant by construction], plus scales a0, c, G fixing units: 12 variables - rank 3 = 9 groups, 3 of them spent on constants (a0/(c^2/R) etc already in ell), 2 redundant")
def main():
    RES = dict(pi=pi_rank()); P(f"AF1 stage 2{' PLANT' if PLANT else ''}; kappa = 1/2 FITTED; not theory closed"); P("Pi: rank " + str(RES["pi"]["rank"]) + "; " + RES["pi"]["basis"])
    for foot in ("canonical", "alt"):
        rng = np.random.default_rng(SEED); D, V = load(foot); r = D["r"].copy()
        V["pure_noise"] = np.random.default_rng(SEED + 1).normal(size=len(r))
        if PLANT:
            r = np.random.default_rng(SEED + 2).normal(0, .1, len(r)) + 0.3 * np.log10(1 + np.nan_to_num(10 ** V["ly_gas"]))
        if PLANT2:  # POST-RESULT power test: frozen plant's amplitude was invisible (y_gas ~ 0.02). UX3's own term, k 13.29, on noise 0.1
            r = np.random.default_rng(SEED + 2).normal(0, .1, len(r)) + np.log10(1 + 13.29 * np.nan_to_num(10 ** V["ly_gas"]))
        T = tests(foot, D, V, r, rng)
        if not PLANT and not PLANT2: T += shearcl(foot, rng)
        N = holm(T); RES[foot] = dict(family=N, tests=T); P(f"\n[{foot}] family {N} CLEAN tests; first Holm line {0.05 / N:.2e}; floor-limited {sum(t['floor_lbl'] for t in T)}")
        for t in sorted(T, key=lambda t: t["p"]):
            if t["p_holm"] <= .05 or t["var"] in LEAKY or t["floor_lbl"]:
                P(f"  {t['sample']:7s} {t['level']:7s} {t['var']:10s} n {t['n']:4d} rho {t['rho']:+.3f} mock {t['mock']:.3f} p {t['p']:.2e} holm {t['p_holm']:.3f} p_part {t['p_partial']:.2e} MI {t['mi']:.3f}{' FLOOR' if t['floor_lbl'] else ''}{' LEAKY' if t['var'] in LEAKY else ''}")
        P("  shearCL all, rank-weighted r (partial on the other two of ly_band, lM500, lz; POST-RESULT):")
        for t in T:
            if t["sample"] == "shearCL": P(f"    {t['level']:6s} {t['var']:8s} n {t['n']} r {t['rho']:+.3f} p {t['p']:.1e} partial {t.get('rho_partial', 0):+.3f} p {t['p_partial']:.1e}")
        I = identity(D, V, r, rng, N); RES[foot]["identity"] = I; P(f"[{foot}] identity: var gain p_strat AUC LOSO+/cov")
        for k, v in sorted(I.items(), key=lambda kv: -kv[1]["gain"]): P(f"  {k:14s} gain {v['gain']:.3f} p {v['p_strat']:.1e} AUC {v['auc'] if v['auc'] is None else round(v['auc'], 3)} LOSO {v['n_loso_pos']}/{v['n_cov']} samples {len(v['samples'])}  " + " ".join(f"{s}:{v['loso'][s]['R2_vs_law']:+.2f}/{v['loso'][s]['cov']:.1f}" for s in v["samples"]))
        Sp = separ(D, V, r); RES[foot]["sep"] = Sp; P(f"[{foot}] separability, held-out rms: const add prod full label")
        for k, v in sorted(Sp.items()): P(f"  {k:28s} {v['const']:.3f} {v['add']:.3f} {v['prod']:.3f} {v['full']:.3f} n {v['n_te']:4d} {v['label']}")
        # verdict per variable
        Sv = {}
        for t in T:
            if t["var"] in LEAKY or t["var"] == "pure_noise": continue
            if t["p_holm"] <= .05 and abs(t["rho"]) > 2 * t["mock"]: Sv.setdefault(t["var"], []).append(dict(sample=t["sample"], level=t["level"], rho=t["rho"], p_partial=t["p_partial"]))
        RES[foot]["within_survivors"] = Sv; RES[foot]["noise_survives"] = [t for t in T if t["var"] == "pure_noise" and t["p"] <= 0.05 / N]
    bf = {v for v in RES["canonical"]["within_survivors"] if v in RES["alt"]["within_survivors"]}; O = {}
    for v in sorted(bf):
        Ic = RES["canonical"]["identity"].get(v); Ia = RES["alt"]["identity"].get(v); F = RES["canonical"]["family"]; Fa = RES["alt"]["family"]; ca = Ic and Ia and Ic["p_strat"] < .05 / F and Ia["p_strat"] < .05 / Fa and Ic["n_loso_pos"] >= math.ceil(Ic["n_cov"] / 2) and Ia["n_loso_pos"] >= math.ceil(Ia["n_cov"] / 2) and Ic["n_cov"] >= 2; lo = Ic and Ic["auc"] is not None and Ic["auc"] >= .95
        shad = all(not (x["p_partial"] < .01) for x in RES["canonical"]["within_survivors"][v]) and v != "ly"
        O[v] = dict(survives_within=True, carries_across=bool(ca), label_only=bool(lo), y_shadow=bool(shad), where=[f"{x['sample']}/{x['level']} {x['rho']:+.2f}" for x in RES["canonical"]["within_survivors"][v]])
    RES["verdict"] = O; P("\nVERDICT per variable (both footings):")
    for k, v in O.items(): P(f"  {k:10s} {'CARRIES ACROSS' if v['carries_across'] else 'within only'}{' LABEL-LIKE AUC>=.95' if v['label_only'] else ''}{' y-SHADOW' if v['y_shadow'] else ''}: {', '.join(v['where'])}")
    P(f"pure_noise survives: canonical {len(RES['canonical']['noise_survives'])}, alt {len(RES['alt']['noise_survives'])}")
    json.dump(RES, open(os.path.join(HERE, f"af1_stage2{TAG}.json"), "w"), indent=0, sort_keys=True, default=float); open(os.path.join(HERE, f"af1_stage2{TAG}.out"), "w").write("\n".join(OUT) + "\n")
main()
