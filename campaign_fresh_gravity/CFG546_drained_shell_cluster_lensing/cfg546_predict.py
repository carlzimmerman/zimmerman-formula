#!/usr/bin/env python3
"""CFG546 Step P: the drained-shell templates from the R5 (shell-draw) engine against the matched S0 control.

Implements FROZEN_CRITERIA.md (baf7e3dd4), Step P, K1, K2, K3-input and MUTATE-SIM.
Inputs (read-only): ../../../_external_data/cfg530_work/profiles/N{512,256}/cfg526_{LRcan,LRalt,S0}_L200{.npz,_rhog.npy,_rhop.npy}
Outputs: cfg546_predict.out / cfg546_predict_results.json  (CFG546_MUTATE=1 -> *_MUTATE.*: shuffled centres)
Run: nice -n 10 python3 cfg546_predict.py
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2"); os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "2")
import json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_external_data"))
PROF = os.path.join(EXT, "cfg530_work", "profiles")
MUTATE = os.environ.get("CFG546_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"cfg546_predict{TAG}.out")
JS = os.path.join(HERE, f"cfg546_predict{TAG}_results.json")
L = 200.0
DTA = 11.805621559499391            # CFG361 table, z = 0
XB = np.round(np.arange(0.0, 4.0001, 0.1), 4)   # x = r/r_ta bin edges
XC = 0.5 * (XB[1:] + XB[:-1])
BINS = {"groups": (13.2, 14.2), "clusters": (14.2, 16.5)}
NBOOT = 200
RNG = np.random.default_rng(546)
_lines = []
RES = {"mutate": MUTATE, "criteria_commit": "baf7e3dd4", "xc": XC.tolist(), "runs": {}, "checks": {}}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); _lines.append(s)


def check(name, detail, ok, gated=True):
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if gated else ' (reported)'} {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail, gated=gated)
    return ok


def subcube(f, c, h):
    n = f.shape[0]
    idx = [np.arange(ci - h, ci + h + 1) % n for ci in c]
    return f[np.ix_(idx[0], idx[1], idx[2])]


_RGRID = {}


def rgrid(h):
    if h not in _RGRID:
        a = np.arange(-h, h + 1, dtype=np.float32)
        _RGRID[h] = np.sqrt(a[:, None, None] ** 2 + a[None, :, None] ** 2 + a[None, None, :] ** 2)
    return _RGRID[h]


def block_corr(fa, fb, nb=64, R=8.0):
    n = fa.shape[0]; s = n // nb
    A = np.asarray(fa, np.float64).reshape(nb, s, nb, s, nb, s).mean(axis=(1, 3, 5))
    B = np.asarray(fb, np.float64).reshape(nb, s, nb, s, nb, s).mean(axis=(1, 3, 5))
    k = 2 * np.pi * np.fft.fftfreq(nb, d=L / nb)
    kk = np.sqrt(k[:, None, None] ** 2 + k[None, :, None] ** 2 + k[None, None, :] ** 2)
    x = np.where(kk > 0, kk * R, 1e-6); W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    As = np.fft.ifftn(np.fft.fftn(A - A.mean()) * W).real; Bs = np.fft.ifftn(np.fft.fftn(B - B.mean()) * W).real
    return float(np.sum(As * Bs) / math.sqrt(np.sum(As ** 2) * np.sum(Bs ** 2)))


def run(N, fname, s0name="S0"):
    t0 = time.time()
    d = os.path.join(PROF, f"N{N}")
    npz = np.load(os.path.join(d, f"cfg526_{s0name}_L200.npz"), allow_pickle=True)
    Om = float(npz["Om"]); dx = L / N
    rhobar = 2.775e11 * Om
    S = np.load(os.path.join(d, f"cfg526_{s0name}_L200_rhop.npy"), mmap_mode="r")
    SG = np.load(os.path.join(d, f"cfg526_{s0name}_L200_rhog.npy"), mmap_mode="r")
    F = np.load(os.path.join(d, f"cfg526_{fname}_L200_rhog.npy"), mmap_mode="r")
    key = f"N{N}_{fname}"
    P(f"\n================ {key} vs {s0name} (N{N}, dx {dx:.4f} Mpc/h, Om {Om:.4f})")
    mS = float(np.mean(S, dtype=np.float64)); mF = float(np.mean(F, dtype=np.float64)); mSG = float(np.mean(SG, dtype=np.float64))
    sgdiff = float(np.max(np.abs(np.asarray(SG[::4, ::4, ::4]) - np.asarray(S[::4, ::4, ::4]))))
    rc = block_corr(S, F)
    k1 = check(f"K1 {key}", f"mean S0 {mS:.7f}, mean F {mF:.7f}, |dmean| {abs(mF - mS):.2e}; S0 rhog=rhop (subsampled max diff {sgdiff:.2e}); "
               f"8 Mpc/h top-hat corr(F,S0) {rc:.4f}", abs(mS - 1) < 1e-5 and abs(mF - mS) < 1e-4 and rc >= 0.95)
    pk = np.asarray(npz["pk"]); ron = np.asarray(npz["ron"], float)
    # r_ta per candidate from the S0 field
    rta = np.zeros(len(pk)); keep = ron > 0
    for i in np.where(keep)[0]:
        h = int(math.ceil(1.6 * ron[i] / dx)) + 2
        cube = subcube(S, pk[i], h); r = rgrid(h)
        rb = np.floor(r / 0.25).astype(np.int32).ravel()
        ms = np.bincount(rb, weights=cube.ravel().astype(np.float64)); ns = np.bincount(rb)
        cm = np.cumsum(ms) / np.maximum(np.cumsum(ns), 1)
        ok = np.where(cm >= DTA)[0]
        rta[i] = (ok.max() + 1) * 0.25 * dx if len(ok) else 0.0
    Mta = DTA * rhobar * 4 / 3 * np.pi * rta ** 3
    lM = np.log10(np.maximum(Mta, 1.0))
    # de-duplicate (heavier first)
    order = np.argsort(-Mta); kept = []
    pos = pk * dx
    kp = np.zeros((0, 3)); kr = np.zeros(0)
    for i in order:
        if rta[i] <= 0: continue
        if len(kept):
            dd = np.abs(kp - pos[i]); dd = np.minimum(dd, L - dd)
            if np.any(np.sqrt((dd ** 2).sum(1)) < kr): continue
        kept.append(i); kp = np.vstack([kp, pos[i]]); kr = np.append(kr, rta[i])
    kept = np.array(kept)
    step = 10 ** (math.log10(8.0 / dx) / 13)       # coarse ron grid ratio (geomspace(dx, 8, 14))
    ratio = rta[kept] / np.maximum(ron[kept], 1e-9)
    fr = float(np.mean((ratio <= step * 1.0001) & (ratio >= 1 / step * 0.9999 * 1.0)))
    check(f"K2 {key}", f"{len(kept)} kept centres; recomputed r_ta / npz ron within one coarse step ({step:.3f}) for {fr:.3f}", fr >= 0.90)
    out = {"n_kept": int(len(kept)), "dx": dx, "K2_frac": fr, "bins": {}}
    # centres for MUTATE: uniform random positions carrying the same r_ta list
    cen = pk.copy()
    if MUTATE:
        cen = RNG.integers(0, N, size=pk.shape)
    # projections for the 2D cross-check (not in MUTATE)
    proj = None
    if not MUTATE:
        proj = {ax: (np.asarray(F.sum(axis=ax, dtype=np.float64)), np.asarray(S.sum(axis=ax, dtype=np.float64))) for ax in range(3)}
    for bname, (lo, hi) in BINS.items():
        sel = kept[(lM[kept] >= lo) & (lM[kept] < hi)]
        if len(sel) == 0:
            P(f"  {bname}: no centres"); continue
        med_rta = float(np.median(rta[sel]))
        resolved = med_rta / dx >= 5
        mF_ = np.zeros((len(sel), len(XC))); mS_ = np.zeros((len(sel), len(XC))); mT_ = np.zeros((len(sel), len(XC)))
        dF_ = np.full((len(sel), len(XC)), np.nan); dS_ = np.full((len(sel), len(XC)), np.nan)
        for n_, i in enumerate(sel):
            h = int(math.ceil(4.0 * rta[i] / dx)) + 1
            r = rgrid(h) * dx / rta[i]
            cf = subcube(F, cen[i], h); cs = subcube(S, cen[i], h)
            cst = subcube(S, pk[i], h) if MUTATE else cs     # MUTATE: denominator from the true halo-centred S0 profile
            b = np.floor(r / 0.1).astype(np.int32).ravel(); m = b < len(XC)
            cnt = np.bincount(b[m], minlength=len(XC)).astype(float)
            mF_[n_] = np.bincount(b[m], weights=cf.ravel()[m].astype(np.float64), minlength=len(XC)) / np.maximum(cnt, 1)
            mS_[n_] = np.bincount(b[m], weights=cs.ravel()[m].astype(np.float64), minlength=len(XC)) / np.maximum(cnt, 1)
            mT_[n_] = np.bincount(b[m], weights=cst.ravel()[m].astype(np.float64), minlength=len(XC)) / np.maximum(cnt, 1)
            mF_[n_][cnt == 0] = np.nan; mS_[n_][cnt == 0] = np.nan
            if proj is not None:
                accF = np.zeros(len(XC)); accS = np.zeros(len(XC)); nn = 0
                for ax in range(3):
                    ij = [c for a, c in enumerate(cen[i]) if a != ax]
                    idx = [np.arange(c - h, c + h + 1) % N for c in ij]
                    pF = proj[ax][0][np.ix_(idx[0], idx[1])]; pS = proj[ax][1][np.ix_(idx[0], idx[1])]
                    a = np.arange(-h, h + 1); R = np.sqrt(a[:, None] ** 2 + a[None, :] ** 2) * dx / rta[i]
                    bb = np.floor(R / 0.1).astype(np.int32).ravel(); mm = bb < len(XC)
                    c2 = np.bincount(bb[mm], minlength=len(XC)).astype(float)
                    sF = np.bincount(bb[mm], weights=pF.ravel()[mm], minlength=len(XC)); sS = np.bincount(bb[mm], weights=pS.ravel()[mm], minlength=len(XC))
                    cumc = np.concatenate([[0], np.cumsum(c2)[:-1]])
                    cF = np.concatenate([[0], np.cumsum(sF)[:-1]]); cS = np.concatenate([[0], np.cumsum(sS)[:-1]])
                    with np.errstate(invalid="ignore", divide="ignore"):
                        dsF = cF / cumc - sF / c2; dsS = cS / cumc - sS / c2
                    accF += dsF; accS += dsS; nn += 1
                dF_[n_] = accF / nn; dS_[n_] = accS / nn
        def stack(mf, ms, mt, ix=None):
            if ix is not None: mf, ms, mt = mf[ix], ms[ix], mt[ix]
            a = np.nanmean(mf, 0); s = np.nanmean(ms, 0); t = np.nanmean(mt, 0)
            return (a - s) / (t - 1.0)
        rel = stack(mF_, mS_, mT_)
        boots = np.array([stack(mF_, mS_, mT_, RNG.integers(0, len(sel), len(sel))) for _ in range(NBOOT)])
        sig = np.nanstd(boots, 0)
        sm = lambda v: np.convolve(np.nan_to_num(v), np.ones(3) / 3, mode="same")
        x13 = (XC >= 1.0) & (XC <= 3.0); x021 = (XC >= 0.2) & (XC <= 1.0)
        def DE(v):
            s3 = sm(v); return float(-np.min(s3[x13])), float(np.max(s3[x021]))
        D, E = DE(rel); Db = np.array([DE(b)[0] for b in boots]); sD = float(np.std(Db))
        sgn = rel.copy(); xs = None
        for j in range(1, len(XC)):
            if XC[j] > 0.3 and sm(rel)[j - 1] > 0 >= sm(rel)[j]: xs = float(XC[j]); break
        mean13 = float(np.nanmean(np.abs(rel[x13])))
        T2 = None; T2s = None
        if proj is not None:
            num = np.nanmean(dF_ - dS_, 0); den = np.nanmean(dS_, 0); T2 = num / den
            bt = []
            for _ in range(NBOOT):
                ix = RNG.integers(0, len(sel), len(sel)); bt.append(np.nanmean(dF_[ix] - dS_[ix], 0) / np.nanmean(dS_[ix], 0))
            T2s = np.nanstd(np.array(bt), 0)
        exists = (D >= 0.02) and (D / max(sD, 1e-12) >= 3)
        P(f"  {bname}: {len(sel)} centres, median log M_ta {np.median(lM[sel]):.2f}, median r_ta {med_rta:.2f} Mpc/h ({med_rta / dx:.1f} cells) "
          f"{'RESOLVED' if resolved else 'UNRESOLVED (<5 cells)'}")
        P(f"    rel(x) at x = {np.round(XC[1::3], 2).tolist()}")
        P(f"      {np.round(rel[1::3], 4).tolist()}")
        P(f"      +- {np.round(sig[1::3], 4).tolist()}")
        P(f"    depletion depth D (min over 1-3 r_ta, 3-bin smoothed) = {D:+.4f} +- {sD:.4f}; inner excess E (0.2-1 r_ta) = {E:+.4f}; "
          f"sign change at x = {xs}; mean |rel| over 1-3 r_ta = {mean13:.4f}; drained shell predicted: {exists}")
        if T2 is not None:
            P(f"    T2D(X) [Delta Sigma ratio] at X = {np.round(XC[1::3], 2).tolist()}")
            P(f"      {np.round(T2[1::3], 4).tolist()}  +- {np.round(T2s[1::3], 4).tolist()}")
        out["bins"][bname] = dict(n=int(len(sel)), lM_med=float(np.median(lM[sel])), rta_med=med_rta, resolved=bool(resolved),
                                  rel=np.nan_to_num(rel).tolist(), rel_sig=np.nan_to_num(sig).tolist(), D=D, D_sig=sD, E=E, x_sign=xs,
                                  mean_abs_rel_1_3=mean13, drained_shell_predicted=bool(exists),
                                  S0_profile=np.nanmean(mS_, 0).tolist(),
                                  T2D=None if T2 is None else np.nan_to_num(T2).tolist(), T2D_sig=None if T2s is None else np.nan_to_num(T2s).tolist())
    P(f"  ({time.time() - t0:.0f} s)")
    RES["runs"][key] = out
    del proj
    return out


P(__doc__.split("Run:")[0].strip())
if MUTATE:
    P("\n*** MUTATE: centres replaced by uniform random positions carrying the same r_ta list ***")
r512 = run(512, "LRcan")
r256c = run(256, "LRcan")
r256a = run(256, "LRalt")

if not MUTATE:
    P("\n== Footing construction: alt primary = 256^3 alt template x s_res (512 can onto 256 can, 0.2 <= x <= 3)")
    RES["templates"] = {}
    m = (XC >= 0.2) & (XC <= 3.0)
    for b in BINS:
        if b not in r512["bins"] or b not in r256c["bins"]: continue
        a = np.array(r512["bins"][b]["rel"]); c = np.array(r256c["bins"][b]["rel"]); al = np.array(r256a["bins"][b]["rel"])
        s = float(np.sum(a[m] * c[m]) / np.sum(c[m] ** 2))
        RES["templates"][b] = {"canonical": a.tolist(), "alt": (s * al).tolist(), "s_res": s,
                               "canonical_256": c.tolist(), "alt_256": al.tolist(),
                               "canonical_sig": r512["bins"][b]["rel_sig"], "alt_sig": (s * np.array(r256a["bins"][b]["rel_sig"])).tolist()}
        P(f"  {b}: s_res = {s:.3f}")
else:
    P("\n== MUTATE-SIM gate: |rel| over 1-3 r_ta at random centres vs halo-centred (from cfg546_predict_results.json)")
    try:
        base = json.load(open(os.path.join(HERE, "cfg546_predict_results.json")))
        for k, v in RES["runs"].items():
            for b, bb in v["bins"].items():
                h = base["runs"][k]["bins"][b]["mean_abs_rel_1_3"]; r = bb["mean_abs_rel_1_3"]
                check(f"MUTATE-SIM {k} {b}", f"random {r:.4f} vs halo-centred {h:.4f} (ratio {r / max(h, 1e-12):.3f})", r <= 0.10 * h or r <= 0.005)
    except FileNotFoundError:
        check("MUTATE-SIM", "baseline results missing; run without MUTATE first", False)

json.dump(RES, open(JS, "w"), indent=1)
open(OUT, "w").write("\n".join(_lines) + "\n")
