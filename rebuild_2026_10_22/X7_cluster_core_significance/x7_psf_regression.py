"""X7 step 1a (criteria 40ae8ff09f): PSF-leakage / additive-bias regression on the KiDS-1000 SOM-gold sources on disk.
Per source e_k = c_k + alpha_k PSF_e_k (k = 1, 2), w-weighted least squares, sandwich (heteroscedastic) covariance.
LK-P (primary): one (c, alpha) pair per component per group = patch (N: 100 < RA < 260 deg, else S) x KiDS-1000 Z_B bin
(0.1,0.3], (0.3,0.5], (0.5,0.7], (0.7,0.9], (0.9,1.2]. LK-T (bracket): per THELI tile (< 1000 fitted sources -> LK-P's).
Global fit reported. Writes x7_psf_regression.out / _results.json and the per-tile table (scratch, for x7_measure.py).
Usage: x7_psf_regression.py <x7 KiDS cache> [--mutate]   (--mutate: weights dropped in the accumulators; G2 must FAIL).
Single thread, no network."""
import os, sys, json, time, resource, gc, numpy as np
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; CACHE = [a for a in sys.argv[1:] if not a.startswith("--")][0]
OUTF = open(os.path.join(HERE, f"x7_psf_regression{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
NS = int(np.load(os.path.join(CACHE, "cell.npy"), mmap_mode="r").shape[0])
HDR = {}
def col(k, a, b):
    """rows a:b of a cache column read with seek + fromfile (no memory map: mapped pages stay in ru_maxrss on macOS)."""
    p = os.path.join(CACHE, f"{k}.npy")
    if k not in HDR:
        with open(p, "rb") as f:
            v = np.lib.format.read_magic(f); sh, fo, dt = (np.lib.format.read_array_header_1_0 if v == (1, 0) else np.lib.format.read_array_header_2_0)(f)
            HDR[k] = (f.tell(), dt)
    off, dt = HDR[k]
    with open(p, "rb") as f:
        f.seek(off + a*dt.itemsize); return np.fromfile(f, dt, b - a)
TB = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 1.2])
def groups(ra, zb):
    """LK-P group 0..9 (patch*5 + tomo) and the fit flag (0.1 < Z_B <= 1.2 as stored float32, finite PSF)."""
    tomo = np.searchsorted(TB, zb.astype(np.float64), side="left") - 1
    fit = (tomo >= 0) & (tomo <= 4)
    patch = np.where((ra > 100) & (ra < 260), 0, 1)
    return patch*5 + np.clip(tomo, 0, 4), fit
NT = len(json.load(open(os.path.join(CACHE, "tiles.json")))["tiles"])
NG = 10; CH = 100_000                                                         # A2: small blocks keep the macOS allocator from growing RSS
# accumulators per (group set, component, variant): S_w, S_wp, S_wpp, S_we, S_wep; variants: 0 data, 1 e + 0.05 p, 2 e + 0.003
def acc_new(n): return np.zeros((n, 2, 3, 5))
ACC = {"G": acc_new(NG), "T": acc_new(NT), "ALL": acc_new(1)}
CNT = {"G": np.zeros(NG), "T": np.zeros(NT)}; NBAD = 0
for a in range(0, NS, CH):
    b = min(NS, a + CH)
    ra = col("ra", a, b); zb = col("zb", a, b); w = col("w", a, b).astype(np.float64)
    e = [col("e1", a, b).astype(np.float64), col("e2", a, b).astype(np.float64)]; p = [col("psf1", a, b).astype(np.float64), col("psf2", a, b).astype(np.float64)]
    tile = col("tile", a, b); g, fit = groups(ra, zb); fin = np.isfinite(p[0]) & np.isfinite(p[1]); NBAD += int((~fin).sum()); s = fit & fin
    wu = np.ones_like(w) if MUT else w
    for k in range(2):
        pk, ek, ww = p[k][s], e[k][s], wu[s]
        for v, ev in enumerate((ek, ek + 0.05*pk, ek + 0.003)):
            terms = (ww, ww*pk, ww*pk*pk, ww*ev, ww*ev*pk)
            for q, x in enumerate(terms):
                ACC["G"][:, k, v, q] += np.bincount(g[s], x, NG); ACC["T"][:, k, v, q] += np.bincount(tile[s], x, NT); ACC["ALL"][0, k, v, q] += x.sum()
    CNT["G"] += np.bincount(g[s], minlength=NG); CNT["T"] += np.bincount(tile[s], minlength=NT)
    del ra, zb, w, e, p, tile, g, fit, fin, s; gc.collect()
say(f"sources {NS:,}; fitted {int(CNT['G'].sum()):,}; non-finite PSF_e {NBAD:,}; tiles {NT} [{time.time()-T0:.0f} s]")
def solve(A):
    """(c, alpha) per row and component from the normal equations; A[..., v, :] -> returns array (..., 3 variants, 2)."""
    Sw, Swp, Swpp, Swe, Swep = (A[..., q] for q in range(5))
    det = Sw*Swpp - Swp**2
    with np.errstate(invalid="ignore", divide="ignore"):
        c = (Swpp*Swe - Swp*Swep)/det; al = (Sw*Swep - Swp*Swe)/det
    return np.stack([c, al], -1)
SOL = {k: solve(v) for k, v in ACC.items()}                                     # (n, 2 comp, 3 variants, 2 [c, alpha])
# ---------------------------------------------------------------- sandwich covariance (second pass) for LK-P groups, tiles (diag), global
MEAT = {"G": np.zeros((NG, 4, 4)), "ALL": np.zeros((1, 4, 4))}; MT = np.zeros((NT, 2, 3))   # tiles: per comp sum w^2 r^2 [1, p, p^2]
for a in range(0, NS, CH):
    b = min(NS, a + CH)
    ra = col("ra", a, b); zb = col("zb", a, b); w = col("w", a, b).astype(np.float64)
    e = [col("e1", a, b).astype(np.float64), col("e2", a, b).astype(np.float64)]; p = [col("psf1", a, b).astype(np.float64), col("psf2", a, b).astype(np.float64)]
    tile = col("tile", a, b); g, fit = groups(ra, zb); s = fit & np.isfinite(p[0]) & np.isfinite(p[1])
    wu = (np.ones_like(w) if MUT else w)[s]; gs = g[s]; ts = tile[s]
    X = []
    for key, idx in (("G", gs), ("ALL", np.zeros_like(gs))):
        sol = SOL[key][:, :, 0, :]
        r = [e[k][s] - sol[idx, k, 0] - sol[idx, k, 1]*p[k][s] for k in range(2)]
        u = [wu*r[0], wu*r[0]*p[0][s], wu*r[1], wu*r[1]*p[1][s]]                          # score components (c1, a1, c2, a2)
        n = MEAT[key].shape[0]
        for i in range(4):
            for j in range(i, 4):
                v = np.bincount(idx, u[i]*u[j], n); MEAT[key][:, i, j] += v
                if j != i: MEAT[key][:, j, i] += v
    solT = SOL["T"][:, :, 0, :]
    for k in range(2):
        r = e[k][s] - solT[ts, k, 0] - solT[ts, k, 1]*p[k][s]; u2 = (wu*r)**2
        for q, x in enumerate((u2, u2*p[k][s], u2*p[k][s]**2)): MT[:, k, q] += np.bincount(ts, x, NT)
    del ra, zb, w, e, p, tile, g, fit, s, wu, gs, ts; gc.collect()
def sandwich(A, M):
    """4x4 covariance of (c1, alpha1, c2, alpha2): bread block-diag per component."""
    out = np.zeros((A.shape[0], 4, 4))
    for n in range(A.shape[0]):
        Binv = np.zeros((4, 4))
        for k in range(2):
            Sw, Swp, Swpp = A[n, k, 0, 0], A[n, k, 0, 1], A[n, k, 0, 2]
            Binv[2*k:2*k+2, 2*k:2*k+2] = np.linalg.inv(np.array([[Sw, Swp], [Swp, Swpp]]))
        out[n] = Binv @ M[n] @ Binv
    return out
COV = {k: sandwich(ACC[k], MEAT[k]) for k in ("G", "ALL")}
def tile_err():
    s = np.full((NT, 2, 2), np.nan)
    for k in range(2):
        Sw, Swp, Swpp = ACC["T"][:, k, 0, 0], ACC["T"][:, k, 0, 1], ACC["T"][:, k, 0, 2]; det = Sw*Swpp - Swp**2
        with np.errstate(invalid="ignore", divide="ignore"):
            i00, i01, i11 = Swpp/det, -Swp/det, Sw/det
            m0, m1, m2 = MT[:, k, 0], MT[:, k, 1], MT[:, k, 2]
            s[:, k, 0] = np.sqrt(i00*i00*m0 + 2*i00*i01*m1 + i01*i01*m2); s[:, k, 1] = np.sqrt(i01*i01*m0 + 2*i01*i11*m1 + i11*i11*m2)
    return s
TERR = tile_err()
# ---------------------------------------------------------------- report
GN = [f"{'N' if g < 5 else 'S'}{['0.1-0.3', '0.3-0.5', '0.5-0.7', '0.7-0.9', '0.9-1.2'][g % 5]}" for g in range(NG)]
say("\nLK-P (patch x tomographic bin): c_k, alpha_k +- sandwich sigma; fitted sources")
LKP = {}
for g in range(NG):
    c1, a1 = SOL["G"][g, 0, 0]; c2, a2 = SOL["G"][g, 1, 0]; sd = np.sqrt(np.diag(COV["G"][g]))
    LKP[GN[g]] = dict(group=g, n=int(CNT["G"][g]), c1=float(c1), alpha1=float(a1), c2=float(c2), alpha2=float(a2), cov=COV["G"][g].tolist(), sig=sd.tolist())
    say(f"  {GN[g]:9s} n {int(CNT['G'][g]):>9,}  c1 {c1:+.2e}+-{sd[0]:.1e}  a1 {a1:+.4f}+-{sd[1]:.4f}   c2 {c2:+.2e}+-{sd[2]:.1e}  a2 {a2:+.4f}+-{sd[3]:.4f}")
c1, a1 = SOL["ALL"][0, 0, 0]; c2, a2 = SOL["ALL"][0, 1, 0]; sd = np.sqrt(np.diag(COV["ALL"][0]))
say(f"  GLOBAL    c1 {c1:+.2e}+-{sd[0]:.1e}  a1 {a1:+.4f}+-{sd[1]:.4f}   c2 {c2:+.2e}+-{sd[2]:.1e}  a2 {a2:+.4f}+-{sd[3]:.4f}")
RES["LKP"] = LKP; RES["global"] = dict(c1=float(c1), alpha1=float(a1), c2=float(c2), alpha2=float(a2), sig=sd.tolist())
okT = CNT["T"] >= 1000
TT = np.zeros((NT, 4)); TG = np.zeros(NT, int)                                     # tile -> (c1, a1, c2, a2); fallback group by majority
for k in range(2): TT[:, 2*k] = SOL["T"][:, k, 0, 0]; TT[:, 2*k + 1] = SOL["T"][:, k, 0, 1]
# fallback for small tiles: LK-P group of the tile's majority (patch from RA of the tile centre is not stored; use the group table by tile counts)
GT = np.zeros((NT, NG))
for a in range(0, NS, CH):
    b = min(NS, a + CH); g, fit = groups(col("ra", a, b), col("zb", a, b)); t = col("tile", a, b)
    np.add.at(GT, (t[fit], g[fit]), 1); del g, fit, t
TG = np.argmax(GT, 1)
for n in np.nonzero(~okT)[0]:
    gg = TG[n]; TT[n] = [SOL["G"][gg, 0, 0, 0], SOL["G"][gg, 0, 0, 1], SOL["G"][gg, 1, 0, 0], SOL["G"][gg, 1, 0, 1]]
say(f"\nLK-T (per tile): {int(okT.sum())} tiles fitted (>= 1000 sources), {int((~okT).sum())} take LK-P; median n {np.median(CNT['T'][okT]):.0f}")
for k, nm in ((0, "c1"), (1, "alpha1"), (2, "c2"), (3, "alpha2")):
    v = TT[okT, k]; say(f"  {nm:6s} median {np.median(v):+.4f}  16-84% {np.percentile(v,16):+.4f} {np.percentile(v,84):+.4f}")
say(f"  median per-tile sigma: alpha1 {np.nanmedian(TERR[okT,0,1]):.4f} alpha2 {np.nanmedian(TERR[okT,1,1]):.4f}  c1 {np.nanmedian(TERR[okT,0,0]):.1e} c2 {np.nanmedian(TERR[okT,1,0]):.1e}")
chi_a = [float(np.nansum(((TT[okT, 2*k + 1] - np.average(TT[okT, 2*k + 1], weights=1/TERR[okT, k, 1]**2))/TERR[okT, k, 1])**2)) for k in range(2)]
say(f"  tile-to-tile alpha scatter chi2 / dof: alpha1 {chi_a[0]:.0f} / {int(okT.sum()) - 1}, alpha2 {chi_a[1]:.0f} / {int(okT.sum()) - 1}")
RES["LKT"] = dict(n_fitted=int(okT.sum()), n_fallback=int((~okT).sum()), median=[float(np.median(TT[okT, k])) for k in range(4)],
                  p16=[float(np.percentile(TT[okT, k], 16)) for k in range(4)], p84=[float(np.percentile(TT[okT, k], 84)) for k in range(4)],
                  alpha_scatter_chi2=chi_a)
np.savez(os.path.join(CACHE, f"x7_lkt_table{TAG}.npz"), coef=TT, n=CNT["T"], fitted=okT, err=TERR)
json.dump(dict(LKP=LKP), open(os.path.join(CACHE, f"x7_lkp_table{TAG}.json"), "w"))
# ---------------------------------------------------------------- G1 injection linearity; G2 direct lstsq on one group
d1 = max(float(np.max(np.abs(SOL["G"][:, k, 1, 1] - SOL["G"][:, k, 0, 1] - 0.05))) for k in range(2))
d1c = max(float(np.max(np.abs(SOL["G"][:, k, 1, 0] - SOL["G"][:, k, 0, 0]))) for k in range(2))
d2 = max(float(np.max(np.abs(SOL["G"][:, k, 2, 0] - SOL["G"][:, k, 0, 0] - 0.003))) for k in range(2))
d2a = max(float(np.max(np.abs(SOL["G"][:, k, 2, 1] - SOL["G"][:, k, 0, 1]))) for k in range(2))
check("G1", max(d1, d1c, d2, d2a) <= 1e-6, f"alpha shift err {d1:.1e}, c unchanged {d1c:.1e}; c shift err {d2:.1e}, alpha unchanged {d2a:.1e}", "<= 1e-6")
GT2 = 2                                                                                   # KiDS-N, Z_B (0.5, 0.7]
nG2 = int(CNT["G"][GT2]); dev = 0.0; nfill = 0
for k in range(2):                                                                     # one component at a time, preallocated
    w_ = np.empty(nG2); e_ = np.empty(nG2); p_ = np.empty(nG2); nfill = 0
    for a in range(0, NS, CH):
        b = min(NS, a + CH); g, fit = groups(col("ra", a, b), col("zb", a, b)); p1 = col("psf1", a, b); p2 = col("psf2", a, b)
        s = fit & (g == GT2) & np.isfinite(p1) & np.isfinite(p2); m_ = int(s.sum())
        if nfill + m_ > nG2: nfill = nG2 + 1; break
        w_[nfill:nfill + m_] = col("w", a, b)[s]; e_[nfill:nfill + m_] = col(f"e{k+1}", a, b)[s]; p_[nfill:nfill + m_] = (p1, p2)[k][s]; nfill += m_
        del g, fit, p1, p2, s
    if nfill != nG2: break
    sw = np.sqrt(w_); sol, *_ = np.linalg.lstsq(np.stack([sw, sw*p_], 1), sw*e_, rcond=None)
    dev = max(dev, abs(sol[0]/SOL["G"][GT2, k, 0, 0] - 1), abs(sol[1]/SOL["G"][GT2, k, 0, 1] - 1))
    del w_, e_, p_, sw; gc.collect()
check("G2", dev <= 1e-8 and nfill == nG2, f"direct weighted lstsq vs accumulators (group {GN[GT2]}, n {nfill:,}): max rel dev {dev:.1e}", "<= 1e-8")
pk = rss(); check("G3", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
RES.update(n_sources=NS, n_fitted=int(CNT["G"].sum()), nonfinite_psf=NBAD, runtime_s=time.time() - T0, peak_rss_GB=pk)
npass = sum(ok for _, ok in CHECKS); say(f"X7_PSF_REGRESSION COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x7_psf_regression_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
