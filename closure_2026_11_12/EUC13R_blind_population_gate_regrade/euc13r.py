"""EUC13R main run: blind re-grade of EUC13's population source gate, from the frozen criteria text only.

EUC13R_MUTATE=newton: mutation twin (a0 -> 1e-30, point estimates only); writes euc13r_newton.json; exits 1 if every
member's b_med point rises on both footings, 3 otherwise. Main run exits 0 when it completes.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys
import time
import zlib

import numpy as np
from scipy import stats as sst

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import euc13r_core as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("EUC13R_MUTATE", "") == "newton"
SEED = 20261112
NDRAW, NREP, NERR = 200, 400, 40
FPS = ("canonical", "alt")
SETTINGS = [(mu, w) for mu in ("mu3", "mu10", "mumarg") for w in ("full", "sis")]
BANDS = {"canonical": [(-0.19, 0.22), (-0.05, 0.30), (0.03, 0.32)], "alt": [(-0.19, 0.21), (-0.06, 0.34), (0.03, 0.31)]}
CLASSES = ["<1.0", "1.0-1.3", ">=1.3"]
T0 = time.time()
OUT = {}


def log(*a):
    print(f"[{time.time() - T0:7.1f}s]", *a, flush=True)


# ------------------------------------------------------------------ sample P and geometry
key, obj = C.load_eclipse()
rows, removed = C.select_P(key, obj)
L = C.lens_arrays(rows)
N = len(rows)
assert N == 3192, N
cls = np.digitize(L["tE"], [1.0, 1.3])          # 0: <1.0, 1: 1.0-1.3, 2: >=1.3
OUT["N_P"] = N
OUT["class_counts"] = [int((cls == k).sum()) for k in range(3)]


def geometry(zl, tE, te, logm):
    DA = C.EUCLID.DA(zl)
    return tE * C.ARCSEC * DA, te * C.ARCSEC * DA, 10 ** logm


rng_err = np.random.default_rng([SEED, 1])


def hw(lo, hi):
    w = (hi - lo) / 2.0
    return np.where(np.isfinite(w) & (w > 0) & (lo > -90) & (hi > -90), w, 0.0)


ERR = []
for r in range(NERR):
    zs_hw = np.where((L["zlo"] > -90) & (L["zhi"] > -90), np.maximum(L["zhi"] - L["zlo"], 0) / (2 * 1.04), 0.0)
    zl_ = np.maximum(L["zl"] + rng_err.standard_normal(N) * zs_hw, 0.05)
    mhw = np.where((L["logm_lo"] > -90) & (L["logm_hi"] > -90), 0.5 * (L["logm_lo"] + L["logm_hi"]), 0.0)
    lm_ = L["logm"] + rng_err.standard_normal(N) * np.maximum(mhw, 0)
    tE_ = np.maximum(L["tE"] + rng_err.standard_normal(N) * hw(L["tE_lo"], L["tE_hi"]), 0.1 * L["tE"])
    te_ = np.maximum(L["te"] + rng_err.standard_normal(N) * hw(L["te_lo"], L["te_hi"]), 0.1 * L["te"])
    ERR.append(dict(zl=zl_, tE=tE_, te=te_, logm=lm_))
CAT = dict(zl=L["zl"], tE=L["tE"], te=L["te"], logm=L["logm"])
REALS = ERR + [CAT]           # index NERR = catalogued
for d in REALS:
    d["RE"], d["Rek"], d["M"] = geometry(d["zl"], d["tE"], d["te"], d["logm"])


def a0_of(fp):
    return 1e-30 / C.ACC_SI if MUT else C.A0[fp]


log("building b tables", "(newton twin)" if MUT else "")
TAB = {}
for fp in FPS:
    reals = [NERR] if MUT else range(NERR + 1)
    TAB[fp] = {}
    for r in reals:
        d = REALS[r]
        TAB[fp][r] = C.build_table(d["RE"], d["Rek"], L["n"], d["M"], a0_of(fp))
    log("tables done", fp)
NFALLBACK = {fp: 0 for fp in FPS}


def b_of(fp, r, idx, zs):
    """b for lenses idx (realisation r) at source redshifts zs (same length). nan where zs is nan."""
    d = REALS[r]
    zl, RE = d["zl"][idx], d["RE"][idx]
    zs = np.asarray(zs, float)
    out = np.full(len(idx), np.nan)
    ok = np.isfinite(zs) & (zs > zl)
    if not ok.any():
        return out
    logT = np.log10(math.pi * RE[ok] ** 2 * C.EUCLID.sigcr(zl[ok], zs[ok]))
    b, oob = C.interp_rows(TAB[fp][r][idx[ok]], logT)
    if oob.any():
        NFALLBACK[fp] += int(oob.sum())
        j = np.where(ok)[0][oob]
        ii = idx[j]
        b[oob] = C.solve_b_direct(d["RE"][ii], d["Rek"][ii], L["n"][ii], d["M"][ii], 10 ** logT[oob], a0_of(fp))
    out[ok] = b
    return out


def stat(b, classes):
    keep = np.isfinite(b)
    res = dict(b_med=float(np.median(b[keep])) if keep.any() else np.nan,
               f25=float(np.mean(b[keep] > 0.25)) if keep.any() else np.nan, n=int(keep.sum()))
    for k in range(3):
        m = keep & (classes == k)
        res[f"b_med_c{k}"] = float(np.median(b[m])) if m.any() else np.nan
    return res


def summarise(draws, reps):
    out = {}
    for q in draws[0]:
        if q == "n":
            out["n_kept_point_median"] = float(np.median([d[q] for d in draws]))
            continue
        pt = float(np.nanmedian([d[q] for d in draws]))
        rv = np.array([d[q] for d in reps], float) if reps else None
        if rv is not None:
            q2, q50, q97 = np.nanpercentile(rv, [2.5, 50, 97.5])
            out[q] = dict(point=pt, lo=pt + q2 - q50, hi=pt + q97 - q50, raw=[float(q2), float(q50), float(q97)])
        else:
            out[q] = dict(point=pt)
    return out


# ------------------------------------------------------------------ KA2 (cheap repeat) and KA5
for fp in FPS:
    b = b_of(fp, NERR, np.arange(N), np.full(N, 1100.0))
    OUT[f"source_free_b_med_{fp}"] = float(np.median(b))
    log("source-free b_med (table path)", fp, round(float(np.median(b)), 4))

ka5_ok = True
rng5 = np.random.default_rng([SEED, 5])
for fp in FPS:
    ii = rng5.integers(0, N, 300)
    zs = CAT["zl"][ii] + 0.2 + rng5.random(300) * (6.0 - CAT["zl"][ii] - 0.2)
    bt = b_of(fp, NERR, ii, zs)
    d = REALS[NERR]
    T = math.pi * d["RE"][ii] ** 2 * C.EUCLID.sigcr(d["zl"][ii], zs)
    bd = C.solve_b_direct(d["RE"][ii], d["Rek"][ii], L["n"][ii], d["M"][ii], T, a0_of(fp))
    mx = float(np.max(np.abs(bt - bd)))
    OUT[f"KA5_{fp}"] = dict(max_abs_db=mx, passed=mx <= 0.003)
    ka5_ok &= mx <= 0.003
    log("KA5", fp, mx)


# ------------------------------------------------------------------ M1, M2 published samples
def pub_sample(name):
    if name == "M1":
        for rule in ("A1", "A2", "A3"):
            s = C.agel_sample(rule)
            if len(s) == 90:
                return s, rule
        return C.agel_sample("A1"), "A1"
    for rule in ("S1", "S2", "S3"):
        s = C.slf4_sample(rule)
        if len(s) == 49:
            return s, rule
    return C.slf4_sample("S1"), "S1"


def match_draw(rng, zl, pzl, pzs):
    """EUC10 Part B recipe: 10 nearest published systems in z_l, draw, redraw <= 20 tries. Returns zs (nan dropped)."""
    cand = np.argsort(np.abs(zl[:, None] - pzl[None, :]), axis=1, kind="stable")[:, :10]
    ch = rng.integers(0, 10, size=(len(zl), 20))
    zc = pzs[np.take_along_axis(cand, ch, axis=1)]
    valid = zc > zl[:, None] + 0.2
    first = np.argmax(valid, axis=1)
    zs = zc[np.arange(len(zl)), first]
    return np.where(valid.any(axis=1), zs, np.nan), cand


def run_pub(name, fp_list=FPS, reps=True):
    samp, rule = pub_sample(name)
    pzl = np.array([s[0] for s in samp]); pzs = np.array([s[1] for s in samp])
    res = dict(rule=rule, N=len(samp), median_zs_sample=float(np.median(pzs)))
    for fp in fp_list:
        rng = np.random.default_rng([SEED, 10 + (name == "M2"), FPS.index(fp)])
        draws, zsmed, ka3 = [], [], []
        # direct-solve b for every (lens, candidate) pair at catalogued values (KA3 path)
        cand = np.argsort(np.abs(CAT["zl"][:, None] - pzl[None, :]), axis=1, kind="stable")[:, :10]
        d = REALS[NERR]
        pairs_l = np.repeat(np.arange(N), 10)
        pairs_z = pzs[cand.ravel()]
        bdir = np.full(len(pairs_l), np.nan)
        okp = pairs_z > CAT["zl"][pairs_l] + 0.2
        T = math.pi * d["RE"][pairs_l[okp]] ** 2 * C.EUCLID.sigcr(d["zl"][pairs_l[okp]], pairs_z[okp])
        bdir[okp] = C.solve_b_direct(d["RE"][pairs_l[okp]], d["Rek"][pairs_l[okp]], L["n"][pairs_l[okp]],
                                     d["M"][pairs_l[okp]], T, a0_of(fp))
        bdir = bdir.reshape(N, 10)
        for _ in range(NDRAW):
            ch = rng.integers(0, 10, size=(N, 20))
            zc = pzs[np.take_along_axis(cand, ch, axis=1)]
            valid = zc > CAT["zl"][:, None] + 0.2
            first = np.argmax(valid, axis=1)
            col = ch[np.arange(N), first]
            zs = np.where(valid.any(axis=1), zc[np.arange(N), first], np.nan)
            bt = b_of(fp, NERR, np.arange(N), zs)
            bd = np.where(np.isfinite(zs), bdir[np.arange(N), col], np.nan)
            draws.append(stat(bt, cls))
            ka3.append(float(np.nanmedian(bd)))
            zsmed.append(float(np.nanmedian(zs)))
        rp = []
        if reps:
            for k in range(NREP):
                idx = rng.integers(0, N, N)
                r = k % NERR
                ps = rng.integers(0, len(samp), len(samp))
                zl_ = REALS[r]["zl"][idx]
                zs, _ = match_draw(rng, zl_, pzl[ps], pzs[ps])
                rp.append(stat(b_of(fp, r, idx, zs), cls[idx]))
        res[fp] = summarise(draws, rp)
        res[fp]["KA3_direct_point"] = float(np.median(ka3))
        res[fp]["median_zs_on_P"] = float(np.median(zsmed))
        log(name, fp, "point b_med table", round(res[fp]["b_med"]["point"], 4), "direct", round(float(np.median(ka3)), 4))
    return res


# ------------------------------------------------------------------ M3 forward model
H = np.loadtxt(os.path.join(HERE, "cosmos_counts_euc13r.csv"), delimiter=",")
WIN = C.Window(H)
flux = C.load_mer_flux()
mk = np.array([C.mer_key(m) for m in L["mer"]])
F_L = np.array([flux.get(x, np.nan) for x in mk])
have = np.isfinite(F_L) & (F_L > 0) & (L["ratio"] > 0)
m_arc = np.where(have, 23.9 - 2.5 * np.log10(np.where(have, L["ratio"] * F_L, 1.0)), np.nan)
OUT["m_arc"] = dict(n_have=int(have.sum()), n_without=int((~have).sum()),
                    median=float(np.nanmedian(m_arc)), p16_p84=[float(x) for x in np.nanpercentile(m_arc, [16, 84])])
no = np.where(~have)[0]
hv = np.where(have)[0]
X = np.c_[CAT["zl"] / 0.1, np.log10(CAT["tE"]) / 0.1]
DON = np.empty((len(no), 20), int)
for k, i in enumerate(no):
    dd = np.sum((X[hv] - X[i]) ** 2, axis=1)
    DON[k] = hv[np.argsort(dd, kind="stable")[:20]]
# expanded predictive rows: rows 0..N-1 are the lenses (own m_arc or nan); extra rows for (no-lens, donor)
EXP_lens = np.concatenate([np.arange(N), np.repeat(no, 20)])
EXP_m = np.concatenate([m_arc, m_arc[DON.ravel()]])
NE = len(EXP_lens)
SUPPORT = (C.ZC[None, :] >= CAT["zl"][:, None] + 0.2 - 1e-9) & (C.ZC[None, :] <= 6.0)
W_SIS = np.where(SUPPORT, C.EUCLID.dls_ds(CAT["zl"][:, None], C.ZC[None, :]) ** 2, 0.0)
FGRID = np.exp(np.linspace(math.log(0.2), math.log(5.0), 31))
SIGCR_Z = C.EUCLID.sigcr(CAT["zl"][:, None], C.ZC[None, :])     # (N,120), inf below z_l


def w_full(lens_rows, logB, fp):
    """theta_E(z)^2 / R_E^2 on ZC for lenses lens_rows at multipliers 10^logB (per row)."""
    d = REALS[NERR]
    R = (d["RE"][lens_rows][:, None] * FGRID[None, :]).ravel()
    rep = np.repeat(lens_rows, len(FGRID))
    out = np.zeros((len(lens_rows), len(C.ZC)))
    for s in range(0, len(R), 31 * 500):
        sl = slice(s, min(len(R), s + 31 * 500))
        wu, h = C.h_nodes(R[sl], d["Rek"][rep[sl]], L["n"][rep[sl]], d["M"][rep[sl]])
        B = 10 ** np.repeat(logB, len(FGRID))[sl]
        m = C.m2d_from_nodes(R[sl], wu, h, B, a0_of(fp))
        sb = np.log10(m / (math.pi * R[sl] ** 2)).reshape(-1, 31)
        for k in range(sb.shape[0]):
            row = s // 31 + k
            li = lens_rows[row]
            lsc = np.log10(SIGCR_Z[li])
            fin = np.isfinite(lsc)
            lf = np.full(len(C.ZC), np.log(0.2))
            lf[fin] = np.interp(-lsc[fin], -sb[k], np.log(FGRID))      # -sb increasing with f
            out[row] = np.exp(2 * lf)
    return out


B_CAT = {}
for fp in FPS:
    zz = np.where(SUPPORT, C.ZC[None, :], np.nan)
    B_CAT[fp] = np.full((N, len(C.ZC)), np.nan)
    for j in range(len(C.ZC)):
        col = zz[:, j]
        if np.isfinite(col).any():
            B_CAT[fp][:, j] = b_of(fp, NERR, np.arange(N), col)
B_INF = {fp: b_of(fp, NERR, np.arange(N), np.full(N, 1100.0)) for fp in FPS}


def nz_rows(setting):
    nz = np.zeros((NE, len(C.ZC)))
    cl = np.full(NE, np.nan)
    ok = np.isfinite(EXP_m)
    nz[ok], cl[ok] = C.n_of_z(WIN, EXP_m[ok], setting)
    return nz, cl


def wmedian_b(p, brow):
    c = np.cumsum(p, axis=1)
    j = np.argmax(c >= 0.5 * c[:, -1:], axis=1)
    return brow[np.arange(len(j)), j]


def normalise(p):
    s = p.sum(axis=1, keepdims=True)
    return p / np.where(s > 0, s, 1.0)


def build_pred(setting, weight, fp, fixed_logB=None):
    nz, cl = nz_rows(setting)
    rows_l = EXP_lens
    info = dict(clamped_weight_mean=float(np.nanmean(cl[:N][have])))
    if weight == "sis":
        p = normalise(nz * W_SIS[rows_l])
        return p, info
    brow = B_CAT[fp][rows_l]
    if fixed_logB is not None:
        p = normalise(nz * w_full(rows_l, np.full(NE, fixed_logB), fp) * SUPPORT[rows_l])
        return p, info
    logB = B_INF[fp][rows_l].copy()
    ch = []
    for it in range(3):
        p = normalise(nz * w_full(rows_l, logB, fp) * SUPPORT[rows_l])
        new = wmedian_b(p, brow)
        ch.append(float(np.nanmax(np.abs(new - logB))))
        logB = new
    p = normalise(nz * w_full(rows_l, logB, fp) * SUPPORT[rows_l])
    info.update(B_iteration_max_change=ch, median_logB=float(np.median(logB[:N])))
    return p, info


def draw_rows(rng, idx):
    """Predictive row for each lens in idx (a donor row chosen at random for lenses without m_arc)."""
    rows = idx.copy()
    pos = {int(i): k for k, i in enumerate(no)}
    for j, i in enumerate(idx):
        if not have[i]:
            rows[j] = N + 20 * pos[int(i)] + rng.integers(0, 20)
    return rows


NO_POS = np.full(N, -1)
NO_POS[no] = np.arange(len(no))


def draw_rows_fast(rng, idx):
    rows = idx.copy()
    m = ~have[idx]
    rows[m] = N + 20 * NO_POS[idx[m]] + rng.integers(0, 20, m.sum())
    return rows


def sample_z(rng, P_rows):
    c = np.cumsum(P_rows, axis=1)
    u = rng.random(len(P_rows))[:, None] * c[:, -1:]
    j = np.minimum(np.sum(c < u, axis=1), len(C.ZC) - 1)
    return j


def run_m3(pred, fp, reps=True, tag=""):
    rng = np.random.default_rng([SEED, 30, FPS.index(fp), zlib.crc32(tag.encode()) % 10000])
    draws, zsm = [], []
    allidx = np.arange(N)
    for _ in range(NDRAW):
        rows = draw_rows_fast(rng, allidx)
        j = sample_z(rng, pred[rows])
        b = B_CAT[fp][allidx, j]
        draws.append(stat(b, cls))
        zsm.append(float(np.median(C.ZC[j])))
    rp = []
    if reps:
        for k in range(NREP):
            idx = rng.integers(0, N, N)
            r = k % NERR
            rows = draw_rows_fast(rng, idx)
            Pr = pred[rows]
            zl_ = REALS[r]["zl"][idx]
            zs = np.full(N, np.nan)
            todo = np.ones(N, bool)
            for _t in range(20):
                if not todo.any():
                    break
                j = sample_z(rng, Pr[todo])
                z = C.ZC[j]
                okz = z >= zl_[todo] + 0.2
                ii = np.where(todo)[0]
                zs[ii[okz]] = z[okz]
                todo[ii[okz]] = False
            rp.append(stat(b_of(fp, r, idx, zs), cls[idx]))
    res = summarise(draws, rp)
    res["median_zs_on_P"] = float(np.median(zsm))
    return res


# ------------------------------------------------------------------ validation (sis weight)
def cdf_piecewise(p):
    c = np.concatenate([[0.0], np.cumsum(p)])
    c /= c[-1]
    return lambda z: np.interp(z, C.ZEDGES, c)


def pred_single(m, zl, setting):
    nz, cl = C.n_of_z(WIN, np.array([m]), setting)
    sup = (C.ZC >= zl + 0.2 - 1e-9) & (C.ZC <= 6.0)
    w = np.where(sup, C.EUCLID.dls_ds(zl, C.ZC) ** 2, 0.0)
    p = nz[0] * w
    return p / p.sum()


def validation():
    out = {}
    s2, _ = pub_sample("M2")
    v1 = [(s[0], s[1], C.vis_proxy(s[5])) for s in s2]
    v1 = [x for x in v1 if np.isfinite(x[2])]
    out["V1_N"] = len(v1)
    # V2 list: own position matches
    allkey = [(r, obj.get(r["unique_identifier"])) for r in key]
    kra = np.array([C._fl(r["ra"]) for r, o in allkey]); kde = np.array([C._fl(r["dec"]) for r, o in allkey])
    refs = []
    for name, zs, ra, de in [(s[2], s[1], s[3], s[4]) for s in C.agel_sample("A2")]:
        refs.append(("AGEL", name, zs, ra, de))
    for s in C.slf4_sample("S2"):
        refs.append(("SLF4", s[2], s[1], s[3], s[4]))
    for r in C.load_slacs():
        try:
            ra, de = C.sexa_to_deg(r["RAJ2000"], r["DEJ2000"]); zs = float(r["zsrc"])
        except (ValueError, KeyError):
            continue
        refs.append(("SLACS", r["SDSS"], zs, ra, de))
    matched = {}
    for src, name, zs, ra, de in refs:
        dd = np.hypot((kra - ra) * math.cos(math.radians(de)), kde - de) * 3600
        j = int(np.argmin(dd))
        if dd[j] <= 2.0:
            uid = allkey[j][0]["unique_identifier"]
            matched.setdefault(uid, (src, name, zs, float(dd[j])))
    for uid, zs in (("EUCL-DR1-L012826", 1.1374), ("EUCL-DR1-L014688", 0.9926), ("EUCL-DR1-L006816", 0.4685)):
        matched[uid] = ("EUC2", uid, zs, 0.0)       # EUC2's confirmed pairs take precedence
    byuid = {r["unique_identifier"]: (r, o) for r, o in allkey}
    v2 = []
    for uid, (src, name, zs, sep) in sorted(matched.items()):
        if uid not in byuid:          # not in the key catalogue (grade C/X): no key-catalogue photo-z
            v2.append(dict(uid=uid, src=src, name=name, zs=zs, sep=sep, evaluable=False, zl=None, m_arc=None,
                           grade="not in key catalogue"))
            continue
        r, o = byuid[uid]
        mid = C.mer_key(o["MER_object_id"]) if o else ""
        F = flux.get(mid, np.nan)
        ratio = C._fl(r["eclipse_vis_ratio_ls_l"])
        phz = C._fl(r["eclipse_median_phz"])
        sz = C._fl(o["desi_deflector_specz"]) if o else np.nan
        ev = np.isfinite(F) and F > 0 and ratio > 0 and phz > 0
        zl = sz if (np.isfinite(sz) and sz > 0) else phz
        v2.append(dict(uid=uid, src=src, name=name, zs=zs, sep=sep, evaluable=bool(ev), zl=float(zl),
                       m_arc=float(23.9 - 2.5 * math.log10(ratio * F)) if ev else None, grade=r["lens_grade"]))
    out["V2_list"] = v2
    ev2 = [x for x in v2 if x["evaluable"]]
    out["V2_N_evaluable"] = len(ev2)
    surv = []
    for mu in ("mu3", "mu10", "mumarg"):
        ps = [pred_single(m, zl, mu) for zl, zs, m in v1]
        mix = np.mean(ps, axis=0)
        F = cdf_piecewise(mix)
        cgrid = np.concatenate([[0.0], np.cumsum(mix)]); cgrid /= cgrid[-1]
        med_mix = float(np.interp(0.5, cgrid, C.ZEDGES))
        obs = np.array([x[1] for x in v1])
        ksp = float(sst.kstest(obs, F).pvalue)
        v1pass = abs(med_mix - np.median(obs)) <= 0.25 and ksp > 0.01
        res = dict(V1_median_mixture=med_mix, V1_median_observed=float(np.median(obs)), V1_ks_p=ksp, V1_pass=bool(v1pass))
        if len(ev2) >= 5:
            u = np.array([cdf_piecewise(pred_single(x["m_arc"], x["zl"], mu))(x["zs"]) for x in ev2])
            kp = float(sst.kstest(u, "uniform").pvalue)
            ext = int(np.sum(np.minimum(u, 1 - u) < 0.005))
            v2pass = kp > 0.01 and ext <= 1
            res.update(V2_pit=[float(x) for x in u], V2_ks_p=kp, V2_extreme=ext, V2_pass=bool(v2pass), V2_applied=True)
        else:
            v2pass = True
            res.update(V2_applied=False)
        res["survives"] = bool(v1pass and v2pass)
        if res["survives"]:
            surv.append(mu)
        out[mu] = res
        log("validation", mu, {k: v for k, v in res.items() if k != "V2_pit"})
    out["surviving_mu"] = surv
    return out


# ------------------------------------------------------------------ run
def gate_words(members, fp):
    ub = [m[fp]["b_med"]["hi"] for m in members]
    lb = [m[fp]["b_med"]["lo"] for m in members]
    g = "POPULATION GATE HOLDS" if all(x <= 0.15 for x in ub) else (
        "POPULATION GATE FAILS" if all(x >= 0.25 for x in lb) else "NO VERDICT")
    fu = [m[fp]["f25"]["hi"] for m in members]
    fl = [m[fp]["f25"]["lo"] for m in members]
    f = "CEILING BROKEN" if all(x >= 0.25 for x in fl) else ("CEILING HOLDS" if all(x <= 0.10 for x in fu) else "NO VERDICT")
    return g, f


def band_word(v, band):
    return "inside" if band[0] <= v <= band[1] else ("above" if v > band[1] else "below")


def envelope(setres, fp, q):
    return dict(lo=min(s[fp][q]["lo"] for s in setres), hi=max(s[fp][q]["hi"] for s in setres),
                points=[s[fp][q]["point"] for s in setres])


if not MUT:
    VAL = validation()
    OUT["validation"] = VAL
    M1 = run_pub("M1"); OUT["M1"] = M1
    M2 = run_pub("M2"); OUT["M2"] = M2
    OUT["KA3"], OUT["KA4"] = {}, {}
    refs = {"M1": {"canonical": 0.238, "alt": 0.220}, "M2": {"canonical": 0.298, "alt": 0.282}}
    ka3_ok = ka4_ok = True
    for nm, M in (("M1", M1), ("M2", M2)):
        for fp in FPS:
            d = M[fp]["KA3_direct_point"]
            t = M[fp]["b_med"]["point"]
            OUT["KA3"][f"{nm}_{fp}"] = dict(value=d, ref=refs[nm][fp], diff=d - refs[nm][fp],
                                            passed=abs(d - refs[nm][fp]) <= 0.002)
            OUT["KA4"][f"{nm}_{fp}"] = dict(table=t, direct=d, diff=t - d, passed=abs(t - d) <= 0.005)
            ka3_ok &= abs(d - refs[nm][fp]) <= 0.002
            ka4_ok &= abs(t - d) <= 0.005
    log("KA3", OUT["KA3"]); log("KA4", OUT["KA4"])
    M3 = {}
    for fp in FPS:
        for (mu, w) in SETTINGS:
            if mu not in VAL["surviving_mu"] and False:
                pass
            p, info = build_pred(mu, w, fp)
            r = run_m3(p, fp, tag=f"{mu}_{w}")
            r["info"] = info
            M3.setdefault(f"{mu}_{w}", {})[fp] = r
            log("M3", mu, w, fp, round(r["b_med"]["point"], 4), info)
        for lb in (0.0, 0.5):
            p, info = build_pred("mumarg", "full", fp, fixed_logB=lb)
            r = run_m3(p, fp, reps=False, tag=f"fixed{lb}")
            M3.setdefault(f"mumarg_full_fixedb{lb}", {})[fp] = r
    OUT["M3"] = M3
    surv_sets = [f"{mu}_{w}" for mu in VAL["surviving_mu"] for w in ("full", "sis")]
    OUT["M3_surviving_settings"] = surv_sets
    words = {}
    for fp in FPS:
        members = [M1, M2]
        if surv_sets:
            env_b = envelope([M3[s] for s in surv_sets], fp, "b_med")
            env_f = envelope([M3[s] for s in surv_sets], fp, "f25")
            members.append({fp: {"b_med": env_b, "f25": env_f}})
            OUT.setdefault("M3_envelope", {})[fp] = dict(b_med=env_b, f25=env_f)
        g, f = gate_words(members, fp)
        checks_ok = ka5_ok and ka3_ok and ka4_ok
        words[fp] = dict(gate=g if checks_ok else "NOT EVALUABLE", f25=f if checks_ok else "NOT EVALUABLE",
                         gate_with_KA3_waived=g, f25_with_KA3_waived=f, M3_in_gate=bool(surv_sets))
        # theta_E class readings
        rd = {}
        for nm, M in [("M1", M1), ("M2", M2)] + [(f"M3_{s}", M3[s]) for s in surv_sets]:
            rd[nm] = {CLASSES[k]: dict(**M[fp][f"b_med_c{k}"], band=BANDS[fp][k],
                                       word=band_word(M[fp][f"b_med_c{k}"]["point"], BANDS[fp][k])) for k in range(3)}
        OUT.setdefault("class_readings", {})[fp] = rd
    OUT["words"] = words
    OUT["checks"] = dict(KA5=ka5_ok, KA3=ka3_ok, KA4=ka4_ok)
    OUT["fallback_direct_solves"] = NFALLBACK
    for fp in FPS:
        log("WORDS", fp, words[fp])
    with open(os.path.join(HERE, "euc13r.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, default=float)
    log("done")
    sys.exit(0)
else:
    # newton twin: point estimates of every member under a0 -> 1e-30, against law-S points recomputed here
    pts = {}
    for label, mut in (("newton", True), ("lawS", False)):
        MUT = mut
        for fp in FPS:
            d = REALS[NERR]
            TAB[fp][NERR] = C.build_table(d["RE"], d["Rek"], L["n"], d["M"], a0_of(fp))
            for j in range(len(C.ZC)):
                col = np.where(SUPPORT[:, j], C.ZC[j], np.nan)
                if np.isfinite(col).any():
                    B_CAT[fp][:, j] = b_of(fp, NERR, np.arange(N), col)
            B_INF[fp] = b_of(fp, NERR, np.arange(N), np.full(N, 1100.0))
        pts[label] = {"M1": run_pub("M1", reps=False), "M2": run_pub("M2", reps=False)}
        for fp in FPS:
            for (mu, w) in SETTINGS:
                p, info = build_pred(mu, w, fp)
                pts[label].setdefault(f"M3_{mu}_{w}", {})[fp] = run_m3(p, fp, reps=False, tag=f"{mu}_{w}")
    rise = {}
    allrise = True
    for mem in pts["newton"]:
        for fp in FPS:
            a = pts["newton"][mem][fp]["b_med"]["point"]; b = pts["lawS"][mem][fp]["b_med"]["point"]
            rise[f"{mem}_{fp}"] = dict(newton=a, lawS=b, rises=bool(a > b))
            allrise &= a > b
            log("twin", mem, fp, round(a, 4), round(b, 4))
    with open(os.path.join(HERE, "euc13r_newton.json"), "w") as fh:
        json.dump(dict(rise=rise, all_rise=bool(allrise)), fh, indent=1, default=float)
    log("twin all rise:", allrise)
    sys.exit(1 if allrise else 3)
