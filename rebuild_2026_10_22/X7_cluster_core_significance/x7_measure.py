"""X7 step 1b/1c (criteria 40ae8ff09f): F1's per-cluster KiDS measurement replayed (F1's estimator, random loop, seed and
acceptance; code as X2's x2_replay.py, itself verbatim F1 L19-L117) on my own KiDS cache (x7_extract.py), extended with
(a) the PSF-leakage templates: LK-P per (group, coefficient) and LK-T at its per-tile coefficients (x7_psf_regression.py),
(b) the raw random-point stacks, (c) R = 200 rotated-source realisations (splitmix64 hash of (row index, r), same rotation of a
source in every aperture), tangential, cross and random-minus-random.
Usage: x7_measure.py <x7 KiDS cache> <scratch out dir> [--mutate]
--mutate: first 20 clusters only, e2 sign flipped (M1 must FAIL). Deterministic, no network, single thread."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":                                # macOS: the medium malloc zone keeps freed multi-MB
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})   # temporaries resident (RSS rule)
import json, hashlib, resource, time, gc, numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.stats import kstest
from astropy.io import fits
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
MUT = "--mutate" in sys.argv; ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; CACHE, SOUT = ARGS[0], ARGS[1]
TAG = "_MUTATE" if MUT else ""; os.makedirs(SOUT, exist_ok=True)
OUTF = open(os.path.join(HERE, f"x7_measure{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
# ---------------------------------------------------------------- F1 constants, distances (verbatim F1 L19-L44 via X2)
G = 6.674e-11; C = 2.998e8; MSUN = 1.989e30; MPC = 3.0857e22; MP = 1.6726e-27; KG_PC2 = MSUN/(3.0857e16)**2
zb_ = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); DMb = np.sqrt(7.942**3/(0.295*DHb))
PCH = PchipInterpolator(np.r_[0, 0.295, zb_], np.r_[0, DMb, DMr]); HRD = 101.54
def DM(z, h): return PCH(np.minimum(np.asarray(z, float), 2.33))*HRD/h
HS = {"h070": 0.70, "h0672": 0.672, "h0686": 0.686}; HX = ("h0672", "h0686")
CELL = 0.2; NRA = int(round(360/CELL)); ZBMAX = 1.2
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:]*EDGES[:-1]); M_BIAS = -0.01
COLS = ("ra", "dec", "e1", "e2", "w", "zb", "psf1", "psf2", "tile"); FD = {}; HDR = {}
for k_ in COLS + ("cell",):
    p_ = os.path.join(CACHE, f"{k_}.npy")
    with open(p_, "rb") as f_:
        v_ = np.lib.format.read_magic(f_); sh_, fo_, dt_ = (np.lib.format.read_array_header_1_0 if v_ == (1, 0) else np.lib.format.read_array_header_2_0)(f_)
        HDR[k_] = (f_.tell(), dt_, sh_[0])
    FD[k_] = os.open(p_, os.O_RDONLY)
def read_rows(k, ii):
    """values of column k at rows ii (ii = concatenated contiguous ranges, as gather() returns), read with os.pread:
    no memory map (macOS keeps touched mapped pages in ru_maxrss). Equal to memmap[ii]."""
    off, dt, _ = HDR[k]; out = np.empty(ii.size, dt)
    if ii.size == 0: return out
    br = np.nonzero(np.diff(ii) != 1)[0] + 1; st = np.r_[0, br]; en = np.r_[br, ii.size]
    for s0, e0 in zip(st, en):
        a0 = int(ii[s0]); n0 = int(e0 - s0); out[s0:e0] = np.frombuffer(os.pread(FD[k], n0*dt.itemsize, off + a0*dt.itemsize), dt)
    return out
CELLS = np.frombuffer(os.pread(FD["cell"], HDR["cell"][2]*4, HDR["cell"][0]), HDR["cell"][1]); NS = len(CELLS); say(f"sources in cache {NS:,}")
def gather(ra, de, th_deg):
    d0 = int(np.floor((de - th_deg + 90)/CELL)); d1 = int(np.floor((de + th_deg + 90)/CELL))
    dra = th_deg/max(np.cos(np.radians(min(abs(de) + th_deg, 89.0))), 1e-3); idx = []
    for di in range(d0, d1 + 1):
        r0 = int(np.floor(((ra - dra) % 360)/CELL)); n = int(np.ceil(2*dra/CELL)) + 1
        cells = (np.arange(r0, r0 + n) % NRA) + di*NRA
        lo = np.searchsorted(CELLS, cells, "left"); hi = np.searchsorted(CELLS, cells, "right")
        idx += [np.arange(a, b) for a, b in zip(lo, hi) if b > a]
    return np.concatenate(idx) if idx else np.zeros(0, int)
# ---------------------------------------------------------------- leakage coefficients (x7_psf_regression.py products in the cache)
LKP = json.load(open(os.path.join(CACHE, "x7_lkp_table.json")))["LKP"]; NG = 10
LKT = np.load(os.path.join(CACHE, "x7_lkt_table.npz"))["coef"]                       # (ntile, 4) = c1, a1, c2, a2
TB = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 1.2])
def groups(ra, zb):
    tomo = np.searchsorted(TB, zb.astype(np.float64), side="left") - 1
    return np.where((ra > 100) & (ra < 260), 0, 1)*5 + np.clip(tomo, 0, 4)
RES["lkp_sha256"] = sha(os.path.join(CACHE, "x7_lkp_table.json")); RES["lkt_sha256"] = sha(os.path.join(CACHE, "x7_lkt_table.npz"))
# ---------------------------------------------------------------- rotation hash (splitmix64), R realisations
R = 200; SEED = np.uint64(0x5EED20261024)
def hash_u(idx, r):
    """uniform [0,1) from (source row index, realisation r); same (idx, r) -> same u."""
    with np.errstate(over="ignore"):
        x = idx.astype(np.uint64)*np.uint64(1_000_003) + np.asarray(r).astype(np.uint64) + SEED
        z = x + np.uint64(0x9E3779B97F4A7C15)
        z = (z ^ (z >> np.uint64(30)))*np.uint64(0xBF58476D1CE4E5B9)
        z = (z ^ (z >> np.uint64(27)))*np.uint64(0x94D049BB133111EB)
        z = z ^ (z >> np.uint64(31))
    return (z >> np.uint64(11)).astype(np.float64)*(1.0/2**53)
_t = np.arange(1_000_000, dtype=np.int64); _u1 = hash_u(_t[:, None] // 5, (_t % 5)[:, None])[:, 0]; _u2 = hash_u(_t[:, None] // 5, (_t % 5)[:, None])[:, 0]
_ks = kstest(_u1, "uniform").pvalue
check("M4", np.array_equal(_u1, _u2) and _ks > 1e-3, f"deterministic {np.array_equal(_u1, _u2)}; KS p {_ks:.3f} (1e6 draws)", "identical; p > 1e-3")
RES["hash_ks_p"] = float(_ks); del _t, _u1, _u2
# ---------------------------------------------------------------- the estimator (X2 esd2 verbatim for the basic sums) + extras context
def proj(f1, f2, c2p, s2p):
    """record convention (e2-flipped tangential sign): returns (tangential, cross)."""
    return -(f1*c2p - f2*s2p), -(f1*s2p + f2*c2p)
def esd3(ra, de, zl, hs):
    thmax = max(3.0/(DM(zl, h)/(1 + zl)) for h in hs.values())*1.02
    ii = gather(ra, de, np.degrees(thmax))
    if ii.size < 10: return None, None
    raw = {k: read_rows(k, ii) for k in COLS}
    zs = np.asarray(raw["zb"], float); keep = (zs > zl + 0.2) & (zs <= ZBMAX); ii = ii[keep]; zs = zs[keep]
    rs = np.asarray(raw["ra"][keep]); ds = np.asarray(raw["dec"][keep]); e1 = np.asarray(raw["e1"][keep], float); e2 = np.asarray(raw["e2"][keep], float); ws = np.asarray(raw["w"][keep], float)
    p1r, p2r, tlr = raw["psf1"][keep], raw["psf2"][keep], raw["tile"][keep]; del raw
    if MUT: e2 = -e2
    dra = (np.radians(rs) - np.radians(ra))*np.cos(np.radians(de)); dra = (dra + np.pi) % (2*np.pi) - np.pi; dde = np.radians(ds) - np.radians(de)
    th = np.hypot(dra, dde); phi = np.arctan2(dde, dra)
    et = -(e1*np.cos(2*phi) - e2*np.sin(2*phi)); ex = -(e1*np.sin(2*phi) + e2*np.cos(2*phi))
    out = {}; ctx = {"h": {}}
    for key, h in hs.items():
        DlM = float(DM(zl, h)); Dl = DlM/(1 + zl); DMs = DM(zs, h)
        isc = np.clip(4*np.pi*G/C**2*(Dl*MPC)*((DMs - DlM)/(1 + zs))/(DMs/(1 + zs)), 0, None)
        k = np.digitize(th*Dl, EDGES) - 1; g = (k >= 0) & (k < 8) & (isc > 0)
        ww = ws*isc**2
        o = {}
        for ch, val0 in (("t", et), ("x", ex)):
            val = val0/np.where(isc > 0, isc, 1)
            o[ch] = (np.bincount(k[g], (ww*val)[g], 8), np.bincount(k[g], ww[g], 8), np.bincount(k[g], (ww**2*val**2)[g], 8), int(g.sum()))
        o["m"] = np.array([np.bincount(k[g], (ww*isc**p)[g], 8) for p in range(1, 7)])
        out[key] = o
        if key in HX: ctx["h"][key] = (k, g, ww, np.where(isc > 0, isc, 1))
    ctx.update(ii=ii, ra=rs, zb=zs, e1=e1, e2=e2, c2p=np.cos(2*phi), s2p=np.sin(2*phi), et=et, ex=ex, psf1=p1r, psf2=p2r, tile=tlr)
    return out, ctx
def extras(ctx, fixed=None):
    """templates and rotated realisations for one call: numerators sum ww*val per bin (normalised later by the call's den)."""
    ii = ctx["ii"]; c2p, s2p = ctx["c2p"], ctx["s2p"]
    p1 = np.asarray(ctx["psf1"], float); p2 = np.asarray(ctx["psf2"], float); fin = np.isfinite(p1) & np.isfinite(p2)
    p1 = np.where(fin, p1, 0.0); p2 = np.where(fin, p2, 0.0); one = fin.astype(float); grp = groups(ctx["ra"], ctx["zb"])
    tl = LKT[np.asarray(ctx["tile"])]
    fields = {"c1": (one, 0*one), "a1": (p1, 0*one), "c2": (0*one, one), "a2": (0*one, p2)}
    fT = (one*(tl[:, 0] + tl[:, 1]*p1), one*(tl[:, 2] + tl[:, 3]*p2))
    out = {"P": np.zeros((len(HX), 4, 2, NG, 8)), "T": np.zeros((len(HX), 2, 8)), "E": np.zeros((len(HX), 2, 8)), "rot": None}
    PT = {t: proj(f[0], f[1], c2p, s2p) for t, f in fields.items()}; TT = proj(fT[0], fT[1], c2p, s2p); EE = proj(ctx["e1"], ctx["e2"], c2p, s2p)
    for hi, hk in enumerate(HX):
        k, g, ww, iscs = ctx["h"][hk]; kg = k[g]
        for ti, t in enumerate(("c1", "a1", "c2", "a2")):
            for ci in range(2):
                out["P"][hi, ti, ci] = np.bincount(grp[g]*8 + kg, (ww*(PT[t][ci]/iscs))[g], NG*8).reshape(NG, 8)
        for ci in range(2):
            out["T"][hi, ci] = np.bincount(kg, (ww*(TT[ci]/iscs))[g], 8); out["E"][hi, ci] = np.bincount(kg, (ww*(EE[ci]/iscs))[g], 8)
    # rotated realisations on the union of in-bin sources
    gu = np.zeros(len(ii), bool)
    for hk in HX: gu |= ctx["h"][hk][1]
    iu = ii[gu]; etu = ctx["et"][gu]; exu = ctx["ex"][gu]; nu = len(iu)
    nreal = R if fixed is None else 1
    rot = np.zeros((len(HX), nreal, 2, 8))
    hsub = []
    for hk in HX:
        k, g, ww, iscs = ctx["h"][hk]; gm = g[gu]; hsub.append((k[gu][gm], (ww/iscs)[gu][gm], gm))
    step_ = max(1, min(nreal, int(100_000 // max(nu, 1))))                                     # small blocks (macOS allocator RSS)
    for r0 in range(0, nreal, step_):
        rr = np.arange(r0, min(nreal, r0 + step_)); nr = len(rr)
        if fixed is None: th2 = 2*np.pi*hash_u(iu[:, None], rr[None, :])
        else: th2 = np.full((nu, 1), 2*fixed)
        cc = np.cos(th2); ss = np.sin(th2)
        etr = etu[:, None]*cc - exu[:, None]*ss; exr = etu[:, None]*ss + exu[:, None]*cc; del cc, ss, th2
        for hi, (kh, wv, gm) in enumerate(hsub):
            kk = (kh[:, None]*1 + 8*np.arange(nr)[None, :]).ravel()
            rot[hi, rr, 0] = np.bincount(kk, (wv[:, None]*etr[gm]).ravel(), nr*8).reshape(nr, 8)
            rot[hi, rr, 1] = np.bincount(kk, (wv[:, None]*exr[gm]).ravel(), nr*8).reshape(nr, 8)
        del etr, exr
    out["rot"] = rot
    return out
def finish(t):
    num, den, var, n = t
    with np.errstate(invalid="ignore", divide="ignore"):
        return num/den/KG_PC2/(1 + M_BIAS), np.sqrt(var)/den/KG_PC2, den, n
def norm(num, den):
    """extras numerators -> ESD with the call's own den (den broadcast over the last axis = bins)."""
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.nan_to_num(num/den/KG_PC2/(1 + M_BIAS))
# ---------------------------------------------------------------- eRASS1 clusters from the FITS (verbatim F1 L78-L87)
EF = os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"); E = fits.open(EF)[1].data
CL = []
for r in E:
    ra, de, z, mg, R5 = float(r["RA_XFIT"]), float(r["DEC_XFIT"]), float(r["BEST_Z"]), float(r["MGAS500"]), float(r["R500"])
    inN = 125 <= ra <= 240 and -6 <= de <= 5; inS = (ra >= 325 or ra <= 60) and -37 <= de <= -25
    if (inN or inS) and 0.05 <= z <= 0.5 and np.isfinite(mg) and mg > 0 and np.isfinite(R5) and R5 > 0:
        off = np.degrees(np.arccos(np.clip(np.sin(np.radians(de))*np.sin(np.radians(r["DEC"])) + np.cos(np.radians(de))*np.cos(np.radians(r["DEC"]))*np.cos(np.radians(ra - r["RA"])), -1, 1)))
        CL.append(dict(name=str(r["NAME"]).strip(), ra=ra, dec=de, z=z, Mgas500=mg*1e11, M500=float(r["M500"]), R500=R5/1e3, off_deg=float(off)))
say(f"eRASS1 candidates in KiDS boxes (FITS): {len(CL)}")
# ---------------------------------------------------------------- the measurement loop (F1 L99-L116: same seed and acceptance)
rng = np.random.default_rng(20261022); MEAS = []; NID = 0
for i, cl in enumerate(CL):
    if MUT and len(MEAS) >= 20: break
    m, mctx = esd3(cl["ra"], cl["dec"], cl["z"], HS)
    if m is None or m["h070"]["t"][3] < 200: continue
    mx = extras(mctx); fx = [extras(mctx, fixed=0.0), extras(mctx, fixed=np.pi/4)] if len(MEAS) < 3 else None; del mctx
    rnd = []; rnx = []; rpos = []
    for _ in range(10):
        a = rng.uniform(0, 2*np.pi); s = rng.uniform(1, 3)
        rra, rde = (cl["ra"] + s*np.cos(a)/np.cos(np.radians(cl["dec"]))) % 360, cl["dec"] + s*np.sin(a)
        rr, rctx = esd3(rra, rde, cl["z"], HS)
        if rr is not None and rr["h070"]["t"][3] > 0.5*m["h070"]["t"][3]:
            rnd.append(rr); rnx.append((extras(rctx), [extras(rctx, fixed=0.0), extras(rctx, fixed=np.pi/4)] if fx is not None else None)); rpos.append((rra, rde))
        del rctx
        if len(rnd) >= 6: break
    if len(rnd) < 5: continue
    rec = dict(cl); rec["rpos"] = rpos
    for key in HS:
        out = {}
        for ch in ("t", "x"):
            d, e, den, n = finish(m[key][ch]); Rr = [finish(x[key][ch]) for x in rnd]
            Rd = np.nan_to_num(np.array([x[0] for x in Rr]))
            out[ch] = dict(D=np.nan_to_num(d) - Rd.mean(0), E=np.nan_to_num(e, nan=1e9), den=den, den_r=np.array([x[2] for x in Rr]).mean(0),
                           DRR=Rd[:3].mean(0) - Rd[3:].mean(0), Draw=np.nan_to_num(d), Rmean=Rd.mean(0))
        out["m"] = m[key]["m"]; out["nrand"] = len(rnd)
        rec[key] = out
    # extras at the cluster level: cluster - mean(randoms), each call normalised by its own den (t-channel den, as the data)
    dc = np.array([m[hk]["t"][1] for hk in HX]); dr = [np.array([x[hk]["t"][1] for hk in HX]) for x in rnd]       # (2, 8)
    def comb(get, extra_axes):
        c = norm(get(mx), dc.reshape((2,) + (1,)*extra_axes + (8,))); rs_ = np.array([norm(get(x[0]), d_.reshape((2,) + (1,)*extra_axes + (8,))) for x, d_ in zip(rnx, dr)])
        return c - rs_.mean(0), rs_
    rec["P"], _ = comb(lambda o: o["P"], 3); rec["T"], _ = comb(lambda o: o["T"], 1); rec["Eid"], _ = comb(lambda o: o["E"], 1)
    rot_c = norm(mx["rot"], dc.reshape(2, 1, 1, 8)); rot_r = np.array([norm(x[0]["rot"], d_.reshape(2, 1, 1, 8)) for x, d_ in zip(rnx, dr)])
    rec["rot"] = np.stack([rot_c[:, :, 0] - rot_r[:, :, :, 0].mean(0), rot_c[:, :, 1] - rot_r[:, :, :, 1].mean(0),
                           rot_r[:3, :, :, 0].mean(0) - rot_r[3:, :, :, 0].mean(0), rot_r[:, :, :, 0].mean(0), rot_r[:, :, :, 1].mean(0)],
                          2).astype(np.float32)                      # (2h, R, 5 [t, x, RR, random-mean t, random-mean x], 8)
    if fx is not None:
        fr = []
        for j in range(2):
            c_ = norm(fx[j]["rot"], dc.reshape(2, 1, 1, 8)); r_ = np.array([norm(x[1][j]["rot"], d_.reshape(2, 1, 1, 8)) for x, d_ in zip(rnx, dr)])
            fr.append(c_[:, 0] - r_[:, :, 0].mean(0))                                                          # (2h, 2ch, 8)
        rec["fixed"] = fr
    MEAS.append(rec); del mx, rnx, fx
    if len(MEAS) % 25 == 0: say(f"  measured {len(MEAS)} clusters (of {i+1} tried) [{time.time()-T0:.0f} s, RSS {rss():.2f} GB]")
N = len(MEAS); say(f"clusters used: {N}")
# ---------------------------------------------------------------- M1: equality with X2's committed replay npz
X2N = os.path.join(REB, "X2_cluster_outskirts", "x2_replay_percluster.npz"); X = np.load(X2N); RES["x2_npz_sha256"] = sha(X2N)
keys = ["h070", "h0672", "h0686"]; assert list(X["hkeys"]) == keys
n = min(N, len(X["name"])); names = all(MEAS[i]["name"] == str(X["name"][i]) for i in range(n)) and N == len(X["name"])
dmax = 0.0; rmax = 0.0; scale = float(np.max(np.abs(X["D"])))
for i in range(n):
    for hi, hk in enumerate(keys):
        for a_, b_ in (("D", ("t", "D")), ("Dx", ("x", "D")), ("DRR", ("t", "DRR")), ("E", ("t", "E"))):
            dmax = max(dmax, float(np.max(np.abs(X[a_][i, hi] - MEAS[i][hk][b_[0]][b_[1]]))))
        for a_, b_ in (("den", ("t", "den")), ("den_r", ("t", "den_r"))):
            rmax = max(rmax, float(np.max(np.abs(X[a_][i, hi] - MEAS[i][hk][b_[0]][b_[1]])/np.maximum(np.abs(X[a_][i, hi]), 1e-300))))
        rmax = max(rmax, float(np.max(np.abs(X["m3to8"][i, hi] - MEAS[i][hk]["m"])/np.maximum(np.abs(X["m3to8"][i, hi]), 1e-300))))
check("M1", names and dmax <= 1e-9*scale and rmax <= 1e-9, f"N {N} vs X2 {len(X['name'])}, names {names}, max|dD| {dmax:.2e} (scale {scale:.0f}), max rel den/m {rmax:.1e}",
      "N 326, names equal, <= 1e-9 x max|D|; rel <= 1e-9")
# ---------------------------------------------------------------- M2: template path identity; M3: rotation identities
d2 = 0.0
for o in MEAS:
    for hi, hk in enumerate(HX):
        d2 = max(d2, float(np.max(np.abs(o["Eid"][hi, 0] - o[hk]["t"]["D"]))), float(np.max(np.abs(o["Eid"][hi, 1] - o[hk]["x"]["D"]))))
check("M2", d2 <= 1e-9*scale, f"template path with (e1, e2): max|diff| vs D, Dx {d2:.2e}", "<= 1e-9 x max|D|")
d3 = 0.0
for o in MEAS[:3]:
    for hi, hk in enumerate(HX):
        d3 = max(d3, float(np.max(np.abs(o["fixed"][0][hi, 0] - o[hk]["t"]["D"]))), float(np.max(np.abs(o["fixed"][0][hi, 1] - o[hk]["x"]["D"]))),
                 float(np.max(np.abs(o["fixed"][1][hi, 0] + o[hk]["x"]["D"]))))
check("M3", d3 <= 1e-9*scale, f"theta=0 -> D, Dx; theta=pi/4 -> D_t = -D_x: max|diff| {d3:.2e} (first 3 clusters)", "<= 1e-9 x max|D|")
# ---------------------------------------------------------------- M5: rotated stacks centre on zero (W-weighted MID sums)
m5 = []
for hi, hk in enumerate(HX):
    for ci in range(5):
        v = np.zeros(R)
        for o in MEAS:
            Eh = o[hk]["t"]["E"]; W = np.where(Eh < 1e8, 1/Eh**2, 0)
            v += (W[None, 3:6]*o["rot"][hi, :, ci, 3:6]).sum(1)
        m5.append(abs(v.mean())/(v.std(ddof=1)/np.sqrt(R)))
check("M5", max(m5) <= 4, f"|mean|/(std/sqrt R) per (h, channel t/x/RR/random-mean t/x): {np.round(m5, 2).tolist()}", "<= 4")
# ---------------------------------------------------------------- products
names_ = np.array([o["name"] for o in MEAS])
NPZ = os.path.join(HERE, f"x7_measure_percluster{TAG}.npz")
ar = lambda ch, f, ks=keys: np.array([[o[k][ch][f] for k in ks] for o in MEAS], float)
LKPc = np.array([[LKP[gn][c] for c in ("c1", "alpha1", "c2", "alpha2")] for gn in sorted(LKP, key=lambda g: LKP[g]["group"])])  # (10, 4)
leakP = np.array([np.einsum("htcgb,gt->hcb", o["P"], LKPc) for o in MEAS])                                  # (N, 2h, 2ch, 8)
psfpat = np.array([o["P"][:, [1, 3]].sum((1, 3)) for o in MEAS])                                            # alpha = 1, c = 0: (N, 2h, 2ch, 8)
np.savez_compressed(NPZ, name=names_, ra=np.array([o["ra"] for o in MEAS]), dec=np.array([o["dec"] for o in MEAS]), z=np.array([o["z"] for o in MEAS]),
                    Mgas500=np.array([o["Mgas500"] for o in MEAS]), M500=np.array([o["M500"] for o in MEAS]), hkeys=np.array(keys), hx=np.array(HX),
                    D=ar("t", "D"), E=ar("t", "E"), den=ar("t", "den"), den_r=ar("t", "den_r"), DRR=ar("t", "DRR"), Dx=ar("x", "D"), Ex=ar("x", "E"),
                    Draw=ar("t", "Draw"), Rmean=ar("t", "Rmean"), Drawx=ar("x", "Draw"), Rmeanx=ar("x", "Rmean"),
                    m3to8=np.array([[o[k]["m"] for k in keys] for o in MEAS], float), nrand=np.array([o["h070"]["nrand"] for o in MEAS]),
                    leakP=leakP, leakT=np.array([o["T"] for o in MEAS]), psfpat=psfpat, LKPcoef=LKPc)
RES["npz_sha256"] = sha(NPZ)
XN = os.path.join(SOUT, f"x7_measure_extras{TAG}.npz")
np.savez(XN, P=np.array([o["P"] for o in MEAS]), rot=np.array([o["rot"] for o in MEAS]), name=names_,
         rpos=np.array([np.array(o["rpos"] + [(np.nan, np.nan)]*(6 - len(o["rpos"]))) for o in MEAS]))
RES["extras_sha256"] = sha(XN)
say(f"wrote {os.path.basename(NPZ)} sha256 {RES['npz_sha256'][:16]}... and scratch {os.path.basename(XN)} sha256 {RES['extras_sha256'][:16]}...")
pk = rss(); check("M6", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
RES.update(N=N, R=R, runtime_s=time.time() - T0, peak_rss_GB=pk)
npass = sum(ok for _, ok in CHECKS); say(f"X7_MEASURE COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x7_measure_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
