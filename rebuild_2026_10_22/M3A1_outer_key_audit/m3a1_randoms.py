#!/usr/bin/env python3
"""M3A1 C4d (FROZEN_CRITERIA.md): extended random points, X11's placement, count and seed (20 per cluster, 1-3 deg, default_rng(20261025), accepted if the h 0.70 count > 0.5 x the cluster's, up to 60 tries), tangential and cross per bin. Estimator verbatim X7's esd3. K3 re-measures Draw and, with F1's seed, Rmean.
    python3 m3a1_randoms.py <F1 KiDS cache> [--k3] [--mutate]
Checkpoint every cluster to cache_randoms (SIGTERM safe; the generator state is saved). One thread. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, signal, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.interpolate import PchipInterpolator
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); CACHE = [a for a in sys.argv[1:] if not a.startswith("--")][0]; MUT = "--mutate" in sys.argv; K3 = "--k3" in sys.argv
G = 6.674e-11; C = 2.998e8; MSUN = 1.989e30; MPC = 3.0857e22; KG_PC2 = MSUN / (3.0857e16) ** 2
zb_ = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295); DMb = np.sqrt(7.942 ** 3 / (0.295 * DHb))
PCH = PchipInterpolator(np.r_[0, 0.295, zb_], np.r_[0, DMb, DMr]); HRD = 101.54
def DM(z, h): return PCH(np.minimum(np.asarray(z, float), 2.33)) * HRD / h
HS = {"h070": 0.70, "h0672": 0.672, "h0686": 0.686}; HX = ("h0672", "h0686"); CELL = 0.2; NRA = int(round(360 / CELL)); ZBMAX = 1.2
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); M_BIAS = -0.01; COLS = ("ra", "dec", "e1", "e2", "w", "zb"); FD = {}; HDR = {}
for k_ in COLS + ("cell",):
    p_ = os.path.join(CACHE, f"{k_}.npy")
    with open(p_, "rb") as f_:
        v_ = np.lib.format.read_magic(f_); sh_, fo_, dt_ = (np.lib.format.read_array_header_1_0 if v_ == (1, 0) else np.lib.format.read_array_header_2_0)(f_); HDR[k_] = (f_.tell(), dt_, sh_[0])
    FD[k_] = os.open(p_, os.O_RDONLY)
def read_rows(k, ii):
    off, dt, _ = HDR[k]; out = np.empty(ii.size, dt)
    if ii.size == 0: return out
    br = np.nonzero(np.diff(ii) != 1)[0] + 1; st = np.r_[0, br]; en = np.r_[br, ii.size]
    for s0, e0 in zip(st, en):
        a0 = int(ii[s0]); n0 = int(e0 - s0); out[s0:e0] = np.frombuffer(os.pread(FD[k], n0 * dt.itemsize, off + a0 * dt.itemsize), dt)
    return out
CELLS = np.frombuffer(os.pread(FD["cell"], HDR["cell"][2] * 4, HDR["cell"][0]), HDR["cell"][1])
def gather(ra, de, th_deg):
    d0 = int(np.floor((de - th_deg + 90) / CELL)); d1 = int(np.floor((de + th_deg + 90) / CELL)); dra = th_deg / max(np.cos(np.radians(min(abs(de) + th_deg, 89.0))), 1e-3); idx = []
    for di in range(d0, d1 + 1):
        r0 = int(np.floor(((ra - dra) % 360) / CELL)); n = int(np.ceil(2 * dra / CELL)) + 1; cells = (np.arange(r0, r0 + n) % NRA) + di * NRA; lo = np.searchsorted(CELLS, cells, "left"); hi = np.searchsorted(CELLS, cells, "right"); idx += [np.arange(a, b) for a, b in zip(lo, hi) if b > a]
    return np.concatenate(idx) if idx else np.zeros(0, int)
def call(ra, de, zl, min070=None):
    thmax = max(3.0 / (DM(zl, h) / (1 + zl)) for h in HS.values()) * 1.02; ii = gather(ra, de, np.degrees(thmax))
    if ii.size < 10: return None
    raw = {k: read_rows(k, ii) for k in COLS}; zs = np.asarray(raw["zb"], float); keep = (zs > zl + 0.2) & (zs <= ZBMAX); zs = zs[keep]
    rs = np.asarray(raw["ra"][keep]); ds = np.asarray(raw["dec"][keep]); e1 = np.asarray(raw["e1"][keep], float); e2 = np.asarray(raw["e2"][keep], float); ws = np.asarray(raw["w"][keep], float)
    if MUT: e2 = -e2
    dra = (np.radians(rs) - np.radians(ra)) * np.cos(np.radians(de)); dra = (dra + np.pi) % (2 * np.pi) - np.pi; dde = np.radians(ds) - np.radians(de); th = np.hypot(dra, dde); phi = np.arctan2(dde, dra)
    et = -(e1 * np.cos(2 * phi) - e2 * np.sin(2 * phi)); ex = -(e1 * np.sin(2 * phi) + e2 * np.cos(2 * phi)); out = {}
    for key, h in HS.items():
        DlM = float(DM(zl, h)); Dl = DlM / (1 + zl); DMs = DM(zs, h); isc = np.clip(4 * np.pi * G / C ** 2 * (Dl * MPC) * ((DMs - DlM) / (1 + zs)) / (DMs / (1 + zs)), 0, None); k = np.digitize(th * Dl, EDGES) - 1; g = (k >= 0) & (k < 8) & (isc > 0)
        if key == "h070":
            out["n070"] = int(g.sum())
            if min070 is not None and out["n070"] <= min070: return out
            continue
        ww = ws * isc ** 2; iscs = np.where(isc > 0, isc, 1); den = np.bincount(k[g], ww[g], 8)
        with np.errstate(invalid="ignore", divide="ignore"):
            t = np.nan_to_num(np.bincount(k[g], (ww * et / iscs)[g], 8) / den / KG_PC2 / (1 + M_BIAS)); x = np.nan_to_num(np.bincount(k[g], (ww * ex / iscs)[g], 8) / den / KG_PC2 / (1 + M_BIAS))
        out[key] = (t, x, den)
    return out
X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); N = len(X["name"]); HJ = {"h0672": 1, "h0686": 2}
Tg = np.digitize(X["Mgas500"], np.quantile(X["Mgas500"], [1 / 3, 2 / 3]))
TAG = "_MUTATE" if MUT else ""
def P(s, L=[]): print(s, flush=True); L.append(s); return L
if K3:
    # first 3 clusters: F1's loop, F1's seed, its own candidate order; plus Draw on all of M3
    E = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data; CL = []
    for r in E:
        ra, de, z, mg, R5 = float(r["RA_XFIT"]), float(r["DEC_XFIT"]), float(r["BEST_Z"]), float(r["MGAS500"]), float(r["R500"]); inN = 125 <= ra <= 240 and -6 <= de <= 5; inS = (ra >= 325 or ra <= 60) and -37 <= de <= -25
        if (inN or inS) and 0.05 <= z <= 0.5 and np.isfinite(mg) and mg > 0 and np.isfinite(R5) and R5 > 0: CL.append(dict(name=str(r["NAME"]).strip(), ra=ra, dec=de, z=z))
    rng = np.random.default_rng(20261022); done = 0; dr = dm = 0.0; sc = float(np.max(np.abs(X["Draw"][:3]))); sr = float(np.max(np.abs(X["Rmean"][:3])))
    for cl in CL:
        if done >= 3: break
        m = call(cl["ra"], cl["dec"], cl["z"])
        if m is None or (lambda: False)(): continue
        n0 = m["n070"]
        if n0 < 200: continue
        rnd = []
        for _ in range(10):
            a = rng.uniform(0, 2 * np.pi); s = rng.uniform(1, 3); rra, rde = (cl["ra"] + s * np.cos(a) / np.cos(np.radians(cl["dec"]))) % 360, cl["dec"] + s * np.sin(a); rr = call(rra, rde, cl["z"], min070=0.5 * n0)
            if rr is not None and rr["n070"] > 0.5 * n0: rnd.append(rr)
            if len(rnd) >= 6: break
        if len(rnd) < 5: continue
        i = [str(x).strip() for x in X["name"]].index(cl["name"])
        for hk in HX:
            dm = max(dm, float(np.max(np.abs(m[hk][0] - X["Draw"][i, HJ[hk]])))); dr = max(dr, float(np.max(np.abs(np.mean([q[hk][0] for q in rnd], 0) - X["Rmean"][i, HJ[hk]]))))
        done += 1
    da = 0.0; idx = np.where(Tg == 2)[0] if not MUT else np.where(Tg == 2)[0][:5]
    for i in idx:
        m = call(float(X["ra"][i]), float(X["dec"][i]), float(X["z"][i])); da = max(da, max(float(np.max(np.abs(m[hk][0] - X["Draw"][i, HJ[hk]]))) for hk in HX))
    ok = dm <= 1e-6 * sc and dr <= 1e-6 * sr and da <= 1e-6 * sc; L = P(f"K3 {TAG}: first 3 clusters on F1's seed: max|d Draw| {dm:.2e}, |d Rmean| {dr:.2e}, of scales {sc:.1f}, {sr:.1f}; Draw on {len(idx)} of M3 {da:.2e}: {'PASS' if ok else 'FAIL'}")
    open(os.path.join(HERE, f"m3a1_randoms_k3{TAG}.out"), "w").write("\n".join(L) + "\n"); sys.exit(0 if ok else 1)
# the set
CD = os.path.join(HERE, "cache_randoms"); os.makedirs(CD, exist_ok=True); CK = os.path.join(CD, "state.json"); A = os.path.join(CD, "arrays.npz"); rng = np.random.default_rng(20261025); I0 = 0
Rt = np.zeros((N, 2, 8)); Rx = np.zeros((N, 2, 8)); DN = np.zeros((N, 2, 8)); Rv = np.zeros((N, 2, 8)); NA = np.zeros(N, int)
if os.path.exists(CK):
    s = json.load(open(CK)); rng.bit_generator.state = s["rng"]; I0 = s["i"]; a = np.load(A); Rt, Rx, DN, Rv, NA = a["Rt"], a["Rx"], a["DN"], a["Rv"], a["NA"]; print(f"resumed at {I0}", flush=True)
STOP = {"v": False}; signal.signal(signal.SIGTERM, lambda *a: STOP.update(v=True))
for i in range(I0, N):
    ra, de, z = float(X["ra"][i]), float(X["dec"][i]), float(X["z"][i]); m = call(ra, de, z, min070=None); n0 = m["n070"]; acc = []; ntry = 0
    while len(acc) < 20 and ntry < 60:
        a_ = rng.uniform(0, 2 * np.pi); s_ = rng.uniform(1, 3); ntry += 1; rra, rde = (ra + s_ * np.cos(a_) / np.cos(np.radians(de))) % 360, de + s_ * np.sin(a_); rr = call(rra, rde, z, min070=0.5 * n0)
        if rr is not None and rr["n070"] > 0.5 * n0: acc.append(rr)
    NA[i] = len(acc)
    for hi, hk in enumerate(HX):
        t = np.array([q[hk][0] for q in acc]); x = np.array([q[hk][1] for q in acc]); Rt[i, hi] = t.mean(0); Rx[i, hi] = x.mean(0); DN[i, hi] = np.mean([q[hk][2] for q in acc], 0); Rv[i, hi] = t.var(0, ddof=1) / len(acc)
    tmp = A + ".tmp.npz"; np.savez(tmp, Rt=Rt, Rx=Rx, DN=DN, Rv=Rv, NA=NA); os.replace(tmp, A); json.dump(dict(i=i + 1, rng=rng.bit_generator.state), open(CK + ".tmp", "w")); os.replace(CK + ".tmp", CK)
    if (i + 1) % 25 == 0: print(f"{i + 1} clusters, {int(NA.sum())} randoms", flush=True)
    if STOP["v"]: print("SIGTERM: checkpointed", flush=True); sys.exit(75)
np.savez_compressed(os.path.join(HERE, "m3a1_randoms.npz"), Rt=Rt, Rx=Rx, DN=DN, Rv=Rv, NA=NA, name=X["name"]); print(f"done: {int(NA.sum())} randoms", flush=True)
