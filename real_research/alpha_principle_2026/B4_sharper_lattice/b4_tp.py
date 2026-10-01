"""B4 triple-point analysis (library + CLI): per-point equal-weight line positions beta_A*(L, beta_F) (JSON files results/<grp>_L<L>_bF<bF>.json written by the point jobs)
-> finite-size extrapolation (1/L^4; L^-2 alternative as systematic) -> straight-line fits on the declared segments S1, S2 -> intersection (D-TP) with Monte-Carlo error propagation
-> 1/alpha(M_P) (conversion of b2_4_confrontation.per_group, inherited) with the beta_F-beta_A correlation kept; fit-range systematic from the declared alternative segments.
Usage: python3 b4_tp.py su2|su3 [kind=weight|height] [win|prod]     (prints; writes b4_tp_<grp>_<kind>[_prod].json)"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PI = math.pi
SEG = {
    "su2": dict(S1=[0.2, 0.3, 0.4], S2=[0.6, 0.7, 0.8], alt=[("S1' ", [0.0, 0.1, 0.2, 0.3, 0.4], [0.6, 0.7, 0.8]), ("S1''", [0.3, 0.4], [0.6, 0.7, 0.8]),
                                                              ("S2' ", [0.2, 0.3, 0.4], [0.55, 0.6, 0.7, 0.8, 0.9]), ("S2''", [0.2, 0.3, 0.4], [0.55, 0.6, 0.7]),
                                                              ("S1'+S2'", [0.0, 0.1, 0.2, 0.3, 0.4], [0.55, 0.6, 0.7, 0.8, 0.9])], N=2),
    "su3": dict(S1=[0.0, 0.4, 0.8], S2=[1.2, 1.6], alt=[("S1' ", [0.4, 0.8], [1.2, 1.6]), ("S2' ", [0.0, 0.4, 0.8], [1.2, 1.6, 2.0]), ("S1'+S2'", [0.4, 0.8], [1.2, 1.6, 2.0])], N=3),
}


def per_group(N, b_adj, b_f, expo, mut=False):
    C_adj, C_f = (1.0 if (mut and N == 2) else N), (N * N - 1) / (2.0 * N)
    full = 4 * PI * (C_adj * b_adj + C_f * b_f) / (N * N - 1)
    a_full = 1.0 / full
    if expo:
        fa, ff = math.exp(-PI * C_adj * a_full), math.exp(-PI * C_f * a_full)
    else:
        fa, ff = 1 - PI * C_adj * a_full, 1 - PI * C_f * a_full
    return 4 * PI * (C_adj * b_adj * fa + C_f * b_f * ff) / (N * N - 1)


def _load(grp, kind, src):
    pts = {}
    for p in sorted(glob.glob(os.path.join(HERE, "results", f"{grp}{'W' if src == 'win' else ''}_L*_bF*.json"))):
        d = json.load(open(p))
        k = "b" if kind == "weight" else "b_height"
        e = "err" if kind == "weight" else "err_height"
        if d.get(k) is None or d.get("dropped"):
            continue
        err = d[e]
        if src == "win" and d.get("vals") and len(d["vals"]) >= 2:
            # hot-start versus cold-start replicas (even / odd index): a systematic disagreement is hysteresis inside windows; the error is at least half the difference
            hot, cold = np.mean(d["vals"][0::2]), np.mean(d["vals"][1::2])
            err = max(err, abs(hot - cold) / 2.0)
        pts.setdefault(round(d["bF"], 4), {})[d["L"]] = (d[k], err, d)
    return pts


def load_points(grp, kind="weight", src="win", sig_est=0.0):
    """src 'win' = windowed Wang-Landau estimator (files <grp>W_*) at every L; 'prod' = full-range flat-histogram production (files <grp>_*) at every L;
    'mix' = the pre-registered fallback of Amendment 2: production at L = 4, windowed at L >= 6 (the windowed values carry the estimator systematic sig_est in quadrature)."""
    if src == "mix":
        pw, pp = _load(grp, "weight", "win"), _load(grp, kind, "prod")
        pts = {}
        for bF, v in pp.items():
            if 4 in v:
                pts.setdefault(bF, {})[4] = v[4]
        for bF, v in pw.items():
            for L, x in v.items():
                if L >= 6:
                    pts.setdefault(bF, {})[L] = (x[0], math.hypot(x[1], sig_est), x[2])
        return pts
    return _load(grp, kind, src)


def extrapolate(Ls_vals, power=4):
    """Ls_vals: list of (L, x, sigma).  x(L) = c + a / L^power, weighted LSQ (exact with 2 points; with 1 point returns it).  Returns c, sigma_c."""
    if len(Ls_vals) == 1:
        L, x, s = Ls_vals[0]
        return x, s
    L = np.array([v[0] for v in Ls_vals], float); x = np.array([v[1] for v in Ls_vals]); s = np.array([max(v[2], 1e-6) for v in Ls_vals])
    A = np.vstack([np.ones_like(L), L ** -power]).T
    w = 1 / s ** 2
    cov = np.linalg.inv(A.T @ (A * w[:, None]))
    beta = cov @ (A.T @ (w * x))
    return beta[0], math.sqrt(cov[0, 0])


def fss_point(vals):
    """vals: {L: (b, err, d)}.  returns nominal c (1/L^4), sigma_stat (propagated), sigma_ext (declared B2 formula)"""
    lv = sorted((L, v[0], v[1]) for L, v in vals.items())
    c4, s4 = extrapolate(lv, 4)
    if len(lv) == 1:
        return c4, s4, 0.0, lv
    c2, _ = extrapolate(lv, 2)
    sext = max(abs(c4 - c2), abs(lv[-1][1] - lv[-2][1]) / 2.0)
    return c4, s4, sext, lv


def line_fit(x, y, s):
    x = np.asarray(x, float); y = np.asarray(y, float); w = 1 / np.maximum(np.asarray(s, float), 1e-6) ** 2
    A = np.vstack([np.ones_like(x), x]).T
    cov = np.linalg.inv(A.T @ (A * w[:, None]))
    beta = cov @ (A.T @ (w * y))
    return beta  # intercept, slope


def intersect(b1, b2):
    # y = a1 + m1 x = a2 + m2 x
    if abs(b1[1] - b2[1]) < 1e-9:
        return None
    x = (b2[0] - b1[0]) / (b1[1] - b2[1])
    return x, b1[0] + b1[1] * x


def triple_point(c, S1, S2):
    """c: {bF: (value, sigma)} ; returns (bF, bA) intersection of line fits through the S1 and S2 points that exist in c"""
    p1 = [b for b in S1 if b in c]; p2 = [b for b in S2 if b in c]
    if len(p1) < 2 or len(p2) < 2:
        return None
    f1 = line_fit(p1, [c[b][0] for b in p1], [c[b][1] for b in p1])
    f2 = line_fit(p2, [c[b][0] for b in p2], [c[b][1] for b in p2])
    return intersect(f1, f2), f1, f2, p1, p2


B2BR = {"su2": {0.0: (2.520, 2.520), 0.2: (2.500, 2.520), 0.4: (2.460, 2.460), 0.6: (2.200, 2.340), 0.7: (1.950, 2.175), 0.8: (1.800, 1.950)},
        "su3": {0.0: (5.900, 6.650), 0.4: (5.800, 6.550), 0.8: (5.650, 6.450), 1.2: (4.750, 6.200), 1.6: (4.350, 5.500), 2.4: (3.550, 4.100)}}


def b2_consistency(grp, kind="weight", src="win"):
    """G-B2 (reported, not gated): the L = 4 equal-weight value vs the B2 L = 4 hysteresis bracket widened by one grid step (0.02 SU(2), 0.25 SU(3))"""
    pad = 0.02 if grp == "su2" else 0.25
    pts = load_points(grp, kind, src)
    out = []
    for bF, br in sorted(B2BR[grp].items()):
        if bF in pts and 4 in pts[bF]:
            v = pts[bF][4][0]
            out.append((bF, v, br, br[0] - pad <= v <= br[1] + pad))
    return out


def analyze(grp, kind="weight", ndraw=20000, seed=7, verbose=True, src="win", sig_est=0.0, transfer=False, common_shift=0.0):
    cfg = SEG[grp]; N = cfg["N"]
    pts = load_points(grp, kind, src, sig_est=sig_est)
    if sig_est > 0 and src != "mix":
        pts = {b: {L: (v[0], math.hypot(v[1], sig_est), v[2]) for L, v in vals.items()} for b, vals in pts.items()}
    if not pts:
        return dict(status="NO POINTS")
    nom, sig, ext = {}, {}, {}
    shifts = []
    for bF, vals in pts.items():
        c, s, e, lv = fss_point(vals)
        nom[bF] = c; sig[bF] = math.hypot(s, e); ext[bF] = e
        if len(vals) >= 2 and 4 in vals:
            shifts.append(c - vals[4][0])
    shift_info = None
    if transfer and shifts:
        # points available at L = 4 only: apply the mean finite-size shift measured at the points that have L = 4 and a larger L, with max(std, 0.5|mean|) as extra uncertainty
        sbar = float(np.mean(shifts)); sstd = float(np.std(shifts, ddof=1)) if len(shifts) > 1 else 0.0
        extra = max(sstd, 0.5 * abs(sbar))
        shift_info = dict(mean=sbar, std=sstd, n=len(shifts), extra=extra)
        for bF, vals in pts.items():
            if len(vals) == 1 and 4 in vals:
                nom[bF] = vals[4][0] + sbar; sig[bF] = math.hypot(vals[4][1], extra); ext[bF] = extra
                pts[bF] = {4: (vals[4][0], vals[4][1], vals[4][2])}
    c_nom = {b: (nom[b], sig[b]) for b in nom}
    res = triple_point(c_nom, cfg["S1"], cfg["S2"])
    if res is None:
        return dict(status="NOT IDENTIFIED", why="fewer than 2 line points on a segment", have=sorted(nom))
    (bFt, bAt), f1, f2, p1, p2 = res
    # Monte-Carlo propagation: redraw every raw beta_A*(L,bF) with its jackknife error, redo FSS, fits, intersection
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(ndraw):
        cd = {}
        cs = rng.normal(0, common_shift) if common_shift > 0 else 0.0
        for bF, vals in pts.items():
            lv = [(L, rng.normal(v[0], v[1]), v[1]) for L, v in sorted(vals.items())]
            if transfer and shift_info is not None and len(vals) == 1:
                c4, s4 = lv[0][1] + shift_info["mean"], lv[0][2]
            else:
                c4, s4 = extrapolate(lv, 4)
            cd[bF] = (c4 + cs + rng.normal(0, ext[bF]), math.hypot(s4, ext[bF]))
        r = triple_point(cd, cfg["S1"], cfg["S2"])
        if r is not None and r[0] is not None:
            draws.append(r[0])
    draws = np.array(draws)
    sF = 0.5 * (np.percentile(draws[:, 0], 84) - np.percentile(draws[:, 0], 16)); sA = 0.5 * (np.percentile(draws[:, 1], 84) - np.percentile(draws[:, 1], 16))
    inv_e = np.array([N and 3 * per_group(N, d[1], d[0], True) for d in draws])
    inv_n = np.array([3 * per_group(N, d[1], d[0], False) for d in draws])
    nom_e, nom_n = 3 * per_group(N, bAt, bFt, True), 3 * per_group(N, bAt, bFt, False)
    s_stat = 0.5 * (np.percentile(inv_e, 84) - np.percentile(inv_e, 16))
    # fit-range systematic: alternative segments
    alts = []
    for name, a1, a2 in cfg["alt"]:
        r = triple_point(c_nom, a1, a2)
        if r is None or r[0] is None:
            alts.append((name, None)); continue
        (bf, ba) = r[0]
        alts.append((name, (bf, ba, 3 * per_group(N, ba, bf, True))))
    dev = [abs(a[1][2] - nom_e) for a in alts if a[1] is not None]
    s_fit = max(dev) if dev else 0.0
    # curvature test: quadratic fits through all points on each side (needs >= 4 points per side)
    out = dict(status="IDENTIFIED", grp=grp, kind=kind, bF=bFt, bA=bAt, sF=sF, sA=sA, inv_expo=nom_e, inv_not=nom_n, s_stat=s_stat, s_fit=s_fit, s_lat=math.hypot(s_stat, s_fit),
               frac_lat=math.hypot(s_stat, s_fit) / nom_e, s_inh=abs(nom_e - nom_n), segs=(p1, p2), corr=float(np.corrcoef(draws[:, 0], draws[:, 1])[0, 1]),
               points={str(b): dict(c=nom[b], sig=sig[b], ext=ext[b], L={str(L): [v[0], v[1]] for L, v in pts[b].items()}) for b in sorted(nom)},
               alts=[(a[0], a[1]) for a in alts], line1=list(f1), line2=list(f2), shift_info=shift_info, common_shift=common_shift)
    out["b2_check"] = b2_consistency(grp, kind, src)
    if grp == "su2" and 0.0 in nom:
        out["G_K"] = dict(value=nom[0.0], sigma=sig[0.0], ok=bool(2.40 <= nom[0.0] <= 2.60))
    if verbose:
        for bF, v, br, ok in out["b2_check"]:
            print(f"   G-B2 bF={bF}: B4 L=4 value {v:.4f} vs B2 bracket [{br[0]:.3f}, {br[1]:.3f}] -> {'consistent' if ok else 'INCONSISTENT'}")
        if "G_K" in out:
            print(f"   G-K pure adjoint (beta_F = 0) infinite-volume beta_A = {nom[0.0]:.4f} +- {sig[0.0]:.4f}; declared acceptance [2.40, 2.60]: {'PASS' if out['G_K']['ok'] else 'FAIL'}")
        print(f"[{grp} {kind}] line points (FSS 1/L^4)" + (f"; L=4-only points shifted by the mean measured finite-size shift {shift_info['mean']:+.4f} (std {shift_info['std']:.4f}, n={shift_info['n']})" if shift_info else "") + ":")
        for b in sorted(nom):
            print(f"   bF={b:5.2f}: " + "  ".join(f"L={L}: {v[0]:.4f}+-{v[1]:.4f}" for L, v in sorted(pts[b].items())) + f"   -> infinity {nom[b]:.4f} +- {sig[b]:.4f} (ext {ext[b]:.4f})")
        print(f"   S1 fit (points {p1}): beta_A = {f1[0]:.4f} + {f1[1]:.4f} beta_F;  S2 fit (points {p2}): beta_A = {f2[0]:.4f} + {f2[1]:.4f} beta_F")
        print(f"   triple point (D-TP) = ({bFt:.4f} +- {sF:.4f}, {bAt:.4f} +- {sA:.4f}), correlation {out['corr']:+.2f}")
        print(f"   1/alpha(M_P): exponentiated {nom_e:.2f}, not exponentiated {nom_n:.2f}; stat+FSS {s_stat:.2f}; fit-range systematic {s_fit:.2f}; lattice total {out['s_lat']:.2f} ({100 * out['frac_lat']:.1f}%)")
        for name, a in alts:
            print(f"     alt {name}: " + ("n/a" if a is None else f"({a[0]:.3f}, {a[1]:.4f}) -> 1/alpha {a[2]:.2f}"))
    return out


if __name__ == "__main__":
    grp = sys.argv[1]
    kind = sys.argv[2] if len(sys.argv) > 2 else "weight"
    src = sys.argv[3] if len(sys.argv) > 3 else "win"
    r = analyze(grp, kind, src=src)
    json.dump(r, open(os.path.join(HERE, f"b4_tp_{grp}_{kind}" + ("" if src == "win" else "_prod") + ".json"), "w"), indent=1, default=str)
