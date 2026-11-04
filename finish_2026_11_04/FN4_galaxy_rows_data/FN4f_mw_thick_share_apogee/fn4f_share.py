#!/usr/bin/env python3
"""FN4f stage A: the local thick-disc (high-alpha) share of the stellar column from APOGEE DR17 + astroNN, without a selection
function, by the frozen chemistry-blind count-ratio estimator; then stage B's placement of the law's Milky Way cells.
Criteria FROZEN_CRITERIA.md; amendments AMENDMENTS.md (A1 join, A2 units, A3 flags, A4 bins).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I fn4f_share.py      (FN4F_MUTATE=1: [Mg/Fe] shuffled in the sample)
kappa = 1/2 FITTED; not theory closed."""
import itertools, json, math, os, resource, sys, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DATA = os.path.join(os.path.dirname(REPO), "_external_data", "apogee_dr17_2026_11")
CACHE = os.path.join(HERE, "cache"); os.makedirs(CACHE, exist_ok=True)
MUT = os.environ.get("FN4F_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
R0, ZSUN = 8.122, 0.0208
OUT = []; RES = {"mutate": MUT}; T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return f"[{time.time() - T0:.0f} s, max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB]"


def read_cols(path, cols, chunk=20000):
    with fits.open(path, memmap=True, lazy_load_hdus=True) as h:
        off = h.fileinfo(1)["datLoc"]; n = int(h[1].header["NAXIS2"]); rl = int(h[1].header["NAXIS1"]); dt = h[1].columns.dtype.newbyteorder(">")
    assert dt.itemsize == rl
    out = {c: [] for c in cols}
    with open(path, "rb") as f:
        f.seek(off)
        for i0 in range(0, n, chunk):
            m = min(chunk, n - i0); arr = np.frombuffer(f.read(m * rl), dtype=dt, count=m)
            for c in cols:
                a = arr[c]
                out[c].append(np.char.strip(a.astype(str)) if a.dtype.kind == "S" else a.astype(np.float64 if a.dtype.kind == "f" else np.int64))
    return {c: np.concatenate(v) for c, v in out.items()}


cache = os.path.join(CACHE, "cols.npz")
if os.path.exists(cache):
    A = dict(np.load(cache, allow_pickle=False))
else:
    S = read_cols(os.path.join(DATA, "allStar-dr17-synspec_rev1.fits"), ["APOGEE_ID", "TELESCOPE", "RA", "DEC", "GLON", "GLAT", "SNR", "TEFF", "LOGG", "FE_H", "FE_H_FLAG", "MG_FE", "MG_FE_FLAG", "ASPCAPFLAG", "EXTRATARG"])
    N = read_cols(os.path.join(DATA, "apogee_astroNN-DR17.fits"), ["APOGEE_ID", "TELESCOPE", "RA", "DEC", "weighted_dist", "weighted_dist_error"])
    A = {k: v for k, v in S.items()}; A.update({"nn_" + k: v for k, v in N.items()})
    np.savez(cache, **A)
P(f"FN4f stage A{' MUTATE ([Mg/Fe] shuffled)' if MUT else ''}. kappa = 1/2 FITTED; not theory closed. Rows {len(A['RA']):,} {rss()}")

# KA4 join (A1)
dpos = np.hypot((A["RA"] - A["nn_RA"]) * np.cos(np.radians(A["DEC"])), A["DEC"] - A["nn_DEC"]) * 3600
join = (A["APOGEE_ID"] == A["nn_APOGEE_ID"]) & (A["TELESCOPE"] == A["nn_TELESCOPE"]) & (dpos <= 1.0)
KA4 = float(join.mean()) >= 0.99; RES["KA4"] = dict(joined_fraction=float(join.mean()), passed=bool(KA4))
P(f"KA4 join (APOGEE_ID, TELESCOPE, position <= 1\"): {join.mean() * 100:.3f} % of rows -> {'PASS' if KA4 else 'FAIL'}")

d_kpc = A["nn_weighted_dist"] / 1000.0; fe = A["FE_H"]; mg = A["MG_FE"].copy()
cut = (join & (A["EXTRATARG"] == 0) & ((A["ASPCAPFLAG"] >> 23) & 1 == 0) & (A["SNR"] >= 70) & (A["LOGG"] >= 1.0) & (A["LOGG"] <= 3.5)
       & (A["TEFF"] >= 3900) & (A["TEFF"] <= 5500) & np.isfinite(fe) & np.isfinite(mg) & (A["FE_H_FLAG"] == 0) & (A["MG_FE_FLAG"] == 0)
       & (fe >= -1.0) & (fe <= 0.5) & np.isfinite(d_kpc) & (d_kpc > 0) & (A["nn_weighted_dist_error"] / A["nn_weighted_dist"] <= 0.2))
P(f"sample after cuts: {int(cut.sum()):,}; median distance {np.median(A['nn_weighted_dist'][cut]):.0f} pc (A2 check: pc)")
if MUT:
    rng = np.random.default_rng(20261104); idx = np.nonzero(cut)[0]; mg[idx] = mg[rng.permutation(idx)]


def geom(dscale):
    l = np.radians(A["GLON"]); b = np.radians(A["GLAT"]); d = d_kpc * dscale
    x = R0 - d * np.cos(b) * np.cos(l); y = d * np.cos(b) * np.sin(l); return np.hypot(x, y), d * np.sin(b) + ZSUN


def trough_line(sel):
    """A trough in the [Mg/Fe] KDE (bandwidth 0.02) between 0.05 and 0.25 in 0.1-dex [Fe/H] bins from -0.9 to +0.1; straight-line fit."""
    from scipy.ndimage import gaussian_filter1d
    xs, ys = [], []; edges = np.arange(-0.3, 0.6001, 0.0005); cen = 0.5 * (edges[1:] + edges[:-1]); win = (cen >= 0.05) & (cen <= 0.25)
    for c in np.arange(-0.85, 0.06, 0.1):
        q = sel & (fe >= c - 0.05) & (fe < c + 0.05); m = mg[q]
        if m.size < 200: continue
        dens = gaussian_filter1d(np.histogram(m, edges)[0].astype(float), 0.02 / 0.0005, mode="constant")   # Gaussian KDE, bandwidth 0.02
        xs.append(c); ys.append(float(cen[win][np.argmin(dens[win])]))
    b1, b0 = np.polyfit(xs, ys, 1); return float(b0), float(b1), xs, ys


def counts(Rg, zg, line, zr, sel):
    b0, b1 = line; hi = mg > b0 + b1 * fe; edges = np.r_[np.arange(0.2, 2.41, 0.2), 2.5] if zr == (0.2, 2.5) else np.arange(0.4, 2.01, 0.2)
    az = np.abs(zg); base = sel & (Rg >= R0 - 1) & (Rg <= R0 + 1)
    nh = np.histogram(az[base & hi], edges)[0]; nl = np.histogram(az[base & ~hi], edges)[0]; zm = np.histogram(az[base], edges, weights=az[base])[0] / np.maximum(np.histogram(az[base], edges)[0], 1)
    return nh, nl, zm


def fit_ratio(nh, nl, zm):
    ok = (nh >= 5) & (nl >= 5)
    if ok.sum() < 3: return float("nan"), float("nan")
    y = np.log(nh[ok] / nl[ok]); w = 1.0 / (1.0 / nh[ok] + 1.0 / nl[ok]); X = np.c_[np.ones(ok.sum()), -zm[ok]]
    beta = np.linalg.solve(X.T @ (X * w[:, None]), X.T @ (w * y)); return float(math.exp(beta[0])), float(beta[1])


def share(r0, kap, hlo, c):
    den = kap + 1.0 / hlo
    if not (np.isfinite(r0) and np.isfinite(kap)) or den <= 0: return float("nan"), float("nan")
    hhi = 1.0 / den; sN = r0 * hhi / (r0 * hhi + hlo); return float(sN * c / (sN * c + 1 - sN)), float(hhi)


sel0 = cut.copy()
Rg1, zg1 = geom(1.0); scyl = sel0 & (Rg1 >= R0 - 1) & (Rg1 <= R0 + 1) & (np.abs(zg1) <= 2.5)
b0, b1, tx, ty = trough_line(scyl); line0 = (b0, b1)
ka2v = b0 + b1 * (-0.3); KA2 = 0.10 <= ka2v <= 0.22
RES["split"] = dict(intercept=b0, slope=b1, bins=tx, troughs=ty, at_m03=ka2v)
P(f"split line: [Mg/Fe] = {b0:+.4f} {b1:+.4f} [Fe/H]  (troughs {np.round(ty, 3).tolist()}); at [Fe/H] -0.3: {ka2v:.3f} -> KA2 {'PASS' if KA2 else 'FAIL'} (0.10-0.22)")

nh, nl, zm = counts(Rg1, zg1, line0, (0.2, 2.5), sel0); r0, kap = fit_ratio(nh, nl, zm); s_p, hhi_p = share(r0, kap, 0.30, 1.0)
RES["primary"] = dict(n_hi=nh.tolist(), n_lo=nl.tolist(), z_mean=zm.tolist(), r0=r0, kappa=kap, h_hi=hhi_p, share=s_p, n_cyl=int((nh + nl).sum()))
P(f"primary: solar-cylinder stars in 0.2-2.5 kpc {int((nh + nl).sum()):,} (high-alpha {int(nh.sum()):,}); r0 {r0:.4f}, kappa {kap:.3f}/kpc -> h_hi {hhi_p:.3f} kpc, share {s_p:.4f}")
KA3 = np.isfinite(hhi_p) and 0.54 <= hhi_p <= 1.26; RES["KA3"] = dict(h_hi=hhi_p, line=[0.54, 1.26], passed=bool(KA3))
P(f"KA3 thick scale height {hhi_p:.3f} kpc in 0.54-1.26 -> {'PASS' if KA3 else 'FAIL'}")

# bootstrap per (line, z range, distance scale); h_lo and c act after the counts
rng = np.random.default_rng(20261106); ids = np.nonzero(sel0)[0]
lines = {"trough": line0, "trough+0.02": (b0 + 0.02, b1), "trough-0.02": (b0 - 0.02, b1)}
VAR = {}
for (ln_, L), zr, ds in itertools.product(lines.items(), [(0.2, 2.5), (0.4, 2.0)], [0.9, 1.0, 1.1]):
    Rg, zg = (Rg1, zg1) if ds == 1.0 else geom(ds)
    nh, nl, zm = counts(Rg, zg, L, zr, sel0); r0c, kc = fit_ratio(nh, nl, zm)
    boots = []
    for _ in range(300):
        pick = np.zeros(len(sel0), np.int64); np.add.at(pick, rng.choice(ids, size=len(ids), replace=True), 1)
        b = L; hi = mg > b[0] + b[1] * fe; az = np.abs(zg); base = (pick > 0) & (Rg >= R0 - 1) & (Rg <= R0 + 1)
        edges = np.r_[np.arange(0.2, 2.41, 0.2), 2.5] if zr == (0.2, 2.5) else np.arange(0.4, 2.01, 0.2)
        nh_ = np.histogram(az[base & hi], edges, weights=pick[base & hi])[0]; nl_ = np.histogram(az[base & ~hi], edges, weights=pick[base & ~hi])[0]
        zm_ = np.histogram(az[base], edges, weights=az[base] * pick[base])[0] / np.maximum(np.histogram(az[base], edges, weights=pick[base])[0], 1)
        boots.append(fit_ratio(nh_, nl_, zm_))
    boots = np.array(boots)
    for hlo, c in itertools.product([0.25, 0.30, 0.35], [0.7, 1.0, 1.4]):
        s, hh = share(r0c, kc, hlo, c); sb = np.array([share(a, k, hlo, c)[0] for a, k in boots]); sd = float(np.nanstd(sb))
        VAR[f"{ln_}|z{zr[0]}-{zr[1]}|d{ds}|hlo{hlo}|c{c}"] = dict(share=s, sd=sd, h_hi=hh, lo=s - 2 * sd, hi=s + 2 * sd)
    P(f"  variant {ln_:<12s} z {zr} d x{ds}: r0 {r0c:.4f}, kappa {kc:.3f} {rss()}")
prim = VAR["trough|z0.2-2.5|d1.0|hlo0.3|c1.0"]
lo = min(v["lo"] for v in VAR.values() if np.isfinite(v["lo"])); hi = max(v["hi"] for v in VAR.values() if np.isfinite(v["hi"]))
RES.update(variants=VAR, primary_share=prim["share"], sigma_stat=prim["sd"], band=[lo, hi], band_width=hi - lo)
P(f"\nshare (primary) {prim['share']:.4f} +- {prim['sd']:.4f} (stat); band B = [{lo:.4f}, {hi:.4f}], width {hi - lo:.4f}")
for k in ("hlo0.25|c1.0", "hlo0.35|c1.0", "hlo0.3|c0.7", "hlo0.3|c1.4"):
    v = VAR[f"trough|z0.2-2.5|d1.0|{k}"]; P(f"  primary counts, {k}: share {v['share']:.4f}")

# KA1 planted sample: two exponentials, share 0.20, chemistry-blind selection in |z|, Poisson, at the real sample's size
def ka1():
    g = np.random.default_rng(424242); n_tot = int(RES["primary"]["n_cyl"]); hlo, hhi, s = 0.30, 0.90, 0.20
    ratio = s / (1 - s) * hlo / hhi                                   # n_hi0 / n_lo0 for share s
    zz = np.linspace(0.2, 2.5, 2301); sel = np.exp(-zz / 0.8)          # any chemistry-blind selection
    lam_lo = np.exp(-zz / hlo) * sel; lam_hi = ratio * np.exp(-zz / hhi) * sel; tot = (lam_lo + lam_hi).sum(); k = n_tot / tot
    edges = np.r_[np.arange(0.2, 2.41, 0.2), 2.5]; ib = np.clip(np.digitize(zz, edges) - 1, 0, len(edges) - 2)
    mu_lo = np.bincount(ib, lam_lo * k, minlength=len(edges) - 1); mu_hi = np.bincount(ib, lam_hi * k, minlength=len(edges) - 1)
    zm = np.bincount(ib, zz * (lam_lo + lam_hi), minlength=len(edges) - 1) / np.bincount(ib, lam_lo + lam_hi, minlength=len(edges) - 1)
    nl = g.poisson(mu_lo); nh = g.poisson(mu_hi); r0_, k_ = fit_ratio(nh, nl, zm); s_, h_ = share(r0_, k_, hlo, 1.0)
    return s_, h_
s1, h1 = ka1(); KA1 = abs(s1 - 0.20) <= 0.01 and abs(h1 - 0.90) <= 0.05
RES["KA1"] = dict(share=s1, h_hi=h1, passed=bool(KA1)); P(f"KA1 planted (share 0.20, h_hi 0.90): recovered {s1:.4f}, {h1:.3f} -> {'PASS' if KA1 else 'FAIL'}")

# stage B
RECORD = 0.2633; width_ok = (hi - lo) <= 0.15
checks = dict(KA1=bool(KA1), KA2=bool(KA2), KA3=bool(KA3), KA4=bool(KA4)); okc = all(checks.values())
if not okc or not width_ok:
    label = "NOT MEASURABLE"; why = "a known answer failed" if not okc else "band wider than 0.15"
elif lo <= RECORD <= hi:
    label = "CELLS INSIDE"; why = "X5's box share 0.2633 lies inside B: form R's in-prior passing cells (1 canonical, 6 alt, LW1) sit at an allowed share"
else:
    label = "NEEDS STAGE-B SOLVES"; why = "0.2633 outside B: form R must be re-solved at B's edges and centre (frozen)"
RES.update(checks=checks, label=label, reason=why, record_share=RECORD)
P(f"\nchecks {checks}; band width ok {width_ok}")
P(f"LABEL{' (MUTATE)' if MUT else ''}: {label} ({why}). Forms A and Q fail at every share on record (0.12-0.35).")
P(f"done {rss()}")
json.dump(RES, open(os.path.join(HERE, f"fn4f_share{TAG}.json"), "w"), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, f"fn4f_share{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit((1 if label == "NOT MEASURABLE" else 0) if MUT else (0 if okc else 1))
