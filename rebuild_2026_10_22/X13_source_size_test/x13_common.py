"""X13 shared measurement code (criteria c4e5a5a064 §3). COPIED WITH PROVENANCE from X11's x11_common.py (commit c1cd5455a5,
sha256 3c72b238884ffa9d...; itself X7's x7_measure.py, sha256 9646311d..., via F1/X2). Changes, and only these:
(1) VARS = this lane's source classes (criteria §3 table) and their class rules in classes(); (2) COLS adds psfD, snr, frad;
init() also loads x13_edges.json; (3) NS_ = 14: X11's 7 per-class sums + sum w, w*Z_B, w*s_B, ww*ln size, ww*ln r_psf,
ww*ln snr, ww*|e|. Everything else (constants, distances, gather, rotation hash, projection, selection, the 7 X11 sums,
rotations) is X11's code unchanged. The ALL, size2 and size4 classes equal X7's / X11's measurement exactly (x13_measure M1/M2)."""
import os, json, numpy as np
from scipy.interpolate import PchipInterpolator
from scipy import sparse
# ---------------------------------------------------------------- F1 constants, distances (verbatim X7 L31-L39)
G = 6.674e-11; C = 2.998e8; MSUN = 1.989e30; MPC = 3.0857e22; MP = 1.6726e-27; KG_PC2 = MSUN/(3.0857e16)**2
zb_ = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); DMb = np.sqrt(7.942**3/(0.295*DHb))
PCH = PchipInterpolator(np.r_[0, 0.295, zb_], np.r_[0, DMb, DMr]); HRD = 101.54
def DM(z, h): return PCH(np.minimum(np.asarray(z, float), 2.33))*HRD/h
HS = {"h070": 0.70, "h0672": 0.672, "h0686": 0.686}; HX = ("h0672", "h0686")
CELL = 0.2; NRA = int(round(360/CELL)); ZBMAX = 1.2
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:]*EDGES[:-1]); M_BIAS = -0.01
MIDB = (3, 4, 5); TB = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 1.2])
R = 200; SEED = np.uint64(0x5EED20261024)
# ---------------------------------------------------------------- source classes (X13 criteria §3)
VARS = [("ALL", 1), ("size2", 2), ("size4", 4), ("tsz", 10), ("spsf", 8), ("ssnr", 8), ("circ2", 2), ("circ4", 4), ("frad2", 2),
        ("band", 3), ("cband", 1)]
PARTITION = ("ALL", "size2", "size4", "tsz", "spsf", "ssnr", "circ2", "circ4", "frad2")     # band, cband are not partitions
OFF = {}; _o = 0
for _n, _k in VARS: OFF[_n] = _o; _o += _k
KTOT = _o
COLS = ("ra", "dec", "e1", "e2", "w", "zb", "size", "psfD", "snr", "frad")
BANDW = 0.05                                                  # half-width of the bands in ln size (criteria §2)
ST = {}
def init(cache):
    """open the cache columns (pread, no memory map: X7 A2/A3) and load the frozen edges and tile classes."""
    ST["fd"] = {}; ST["hdr"] = {}
    for k_ in COLS + ("cell",):
        p_ = os.path.join(cache, f"{k_}.npy")
        with open(p_, "rb") as f_:
            v_ = np.lib.format.read_magic(f_); sh_, fo_, dt_ = (np.lib.format.read_array_header_1_0 if v_ == (1, 0) else np.lib.format.read_array_header_2_0)(f_)
            ST["hdr"][k_] = (f_.tell(), dt_, sh_[0])
        ST["fd"][k_] = os.open(p_, os.O_RDONLY)
    off, dt, n = ST["hdr"]["cell"]; ST["cells"] = np.frombuffer(os.pread(ST["fd"]["cell"], n*4, off), dt)
    E = json.load(open(os.path.join(cache, "x11_edges.json"))); ST["edges"] = {k: np.asarray(v, np.float64) for k, v in E["edges"].items()}
    E13 = json.load(open(os.path.join(cache, "x13_edges.json"))); ST["edges13"] = {k: np.asarray(v, np.float64) for k, v in E13["edges"].items() if k != "band_halfwidth_ln"}
    assert np.array_equal(ST["edges13"]["size4_x11"], ST["edges"]["size4"]), "x13 edges built on another size4"
    return len(ST["cells"])
def read_rows(k, ii):
    """verbatim X7 read_rows: values of column k at rows ii (concatenated contiguous ranges) via os.pread."""
    off, dt, _ = ST["hdr"][k]; out = np.empty(ii.size, dt)
    if ii.size == 0: return out
    br = np.nonzero(np.diff(ii) != 1)[0] + 1; st = np.r_[0, br]; en = np.r_[br, ii.size]
    for s0, e0 in zip(st, en):
        a0 = int(ii[s0]); n0 = int(e0 - s0); out[s0:e0] = np.frombuffer(os.pread(ST["fd"][k], n0*dt.itemsize, off + a0*dt.itemsize), dt)
    return out
def gather(ra, de, th_deg):
    """verbatim X7 gather."""
    CELLS = ST["cells"]
    d0 = int(np.floor((de - th_deg + 90)/CELL)); d1 = int(np.floor((de + th_deg + 90)/CELL))
    dra = th_deg/max(np.cos(np.radians(min(abs(de) + th_deg, 89.0))), 1e-3); idx = []
    for di in range(d0, d1 + 1):
        r0 = int(np.floor(((ra - dra) % 360)/CELL)); n = int(np.ceil(2*dra/CELL)) + 1
        cells = (np.arange(r0, r0 + n) % NRA) + di*NRA
        lo = np.searchsorted(CELLS, cells, "left"); hi = np.searchsorted(CELLS, cells, "right")
        idx += [np.arange(a, b) for a, b in zip(lo, hi) if b > a]
    return np.concatenate(idx) if idx else np.zeros(0, int)
def hash_u(idx, r):
    """verbatim X7 splitmix64: uniform [0,1) from (source row index, realisation r)."""
    with np.errstate(over="ignore"):
        x = idx.astype(np.uint64)*np.uint64(1_000_003) + np.asarray(r).astype(np.uint64) + SEED
        z = x + np.uint64(0x9E3779B97F4A7C15)
        z = (z ^ (z >> np.uint64(30)))*np.uint64(0xBF58476D1CE4E5B9)
        z = (z ^ (z >> np.uint64(27)))*np.uint64(0x94D049BB133111EB)
        z = z ^ (z >> np.uint64(31))
    return (z >> np.uint64(11)).astype(np.float64)*(1.0/2**53)
def proj(f1, f2, c2p, s2p):
    """verbatim X7: record convention (e2-flipped tangential sign): returns (tangential, cross)."""
    return -(f1*c2p - f2*s2p), -(f1*s2p + f2*c2p)
def srcvars(raw):
    """per-source variables of this lane (float64): size, |e|, r_ab (float32-rounded as in x13_extract), psfD, snr, frad."""
    size = raw["size"].astype(np.float64); e1 = raw["e1"].astype(np.float64); e2 = raw["e2"].astype(np.float64); em = np.sqrt(e1**2 + e2**2)
    vs = np.isfinite(size) & (size > 0)
    with np.errstate(invalid="ignore", divide="ignore"):
        rab = np.where(em < 1, size*np.sqrt(np.clip((1 - em)/(1 + em), 0, None)), np.nan).astype(np.float32).astype(np.float64)
    return dict(size=size, em=em, rab=rab, vs=vs, vc=vs & np.isfinite(rab) & (rab > 0), psfD=raw["psfD"].astype(np.float64),
                snr=raw["snr"].astype(np.float64), frad=raw["frad"].astype(np.float64))
def classes(raw, zs, zl, c2p, s2p, sv=None):
    """per-source class index for every variable (combined axis, -1 = invalid): array (nvars, n). Edges: X11's size2/size4
    (side='right': a value equal to an edge goes to the upper class, as X11), this lane's x13_edges.json for the rest."""
    n = len(zs); E = ST["edges"]; E13 = ST["edges13"]; out = np.full((len(VARS), n), -1, np.int64)
    def edge_cls(x, valid, e): c = np.searchsorted(e, np.where(valid, x, 0.0), side="right"); return np.where(valid, c, -1)
    sv = srcvars(raw) if sv is None else sv; size, vs, rab, vc = sv["size"], sv["vs"], sv["rab"], sv["vc"]
    psfD, snr, frad = sv["psfD"], sv["snr"], sv["frad"]
    vP = np.isfinite(psfD) & (psfD > 0); vN = np.isfinite(snr) & (snr > 0); vF = np.isfinite(frad) & (frad > 0)
    tomo = np.searchsorted(TB, zs, side="left") - 1; tomo = np.where((tomo >= 0) & (tomo <= 4), tomo, -1)
    s2 = edge_cls(size, vs, E["size2"]); s4 = edge_cls(size, vs, E["size4"]); q = np.clip(s4, 0, 3)
    hiP = (np.where(vP, psfD, 0.0) >= E13["psf2q"][q]).astype(np.int64); hiN = (np.where(vN, snr, 0.0) >= E13["snr2q"][q]).astype(np.int64)
    with np.errstate(invalid="ignore", divide="ignore"):
        ls = np.log(np.where(vs, size, 1.0)); lc = np.log(np.where(vc, rab, 1.0))
    band = np.full(n, -1, np.int64)
    for j in range(3): band = np.where(vs & (np.abs(ls - np.log(E["size4"][j])) < BANDW), j, band)
    loc = {"ALL": np.zeros(n, np.int64), "size2": s2, "size4": s4,
           "tsz": np.where((tomo >= 0) & (s2 >= 0), tomo*2 + s2, -1),
           "spsf": np.where(vs & vP, s4*2 + hiP, -1), "ssnr": np.where(vs & vN, s4*2 + hiN, -1),
           "circ2": edge_cls(rab, vc, E13["circ2"]), "circ4": edge_cls(rab, vc, E13["circ4"]), "frad2": edge_cls(frad, vF, E13["frad2"]),
           "band": band, "cband": np.where(vc & (np.abs(lc - np.log(E13["cband_edge"][0])) < BANDW), 0, -1)}
    for vi, (nm, k) in enumerate(VARS):
        c = loc[nm]; out[vi] = np.where(c >= 0, c + OFF[nm], -1)
    return out
NS_ = 14            # per-class sums: X11's num_t, num_x, den, var_t, var_x, cnt, sisc + w, w*zb, w*isc, ww*ln size, ww*ln r_psf, ww*ln snr, ww*|e|
def call(ra, de, zl, rot=True, use_vars=True, want90=False, geom=False, mut=False, min070=None):
    """one aperture (cluster or random) at lens redshift zl: X7's esd3 selection and sums, per class, both HX; h070 count.
    Returns None if < 10 sources gathered (as X7). min070: if the h 0.70 in-bin count is <= min070, return {"n070": n} only
    (a rejected random: nothing else is used). Without classes or geometry only the columns the sums need are read."""
    thmax = max(3.0/(DM(zl, h)/(1 + zl)) for h in HS.values())*1.02
    ii = gather(ra, de, np.degrees(thmax))
    if ii.size < 10: return None
    need = COLS if (use_vars or geom) else ("ra", "dec", "e1", "e2", "w", "zb")
    raw = {k: read_rows(k, ii) for k in need}
    zs = np.asarray(raw["zb"], float); keep = (zs > zl + 0.2) & (zs <= ZBMAX); ii = ii[keep]; zs = zs[keep]
    raw = {k: v[keep] for k, v in raw.items()}
    rs = np.asarray(raw["ra"]); ds = np.asarray(raw["dec"]); e1 = np.asarray(raw["e1"], float); e2 = np.asarray(raw["e2"], float); ws = np.asarray(raw["w"], float)
    if mut: e2 = -e2
    dra = (np.radians(rs) - np.radians(ra))*np.cos(np.radians(de)); dra = (dra + np.pi) % (2*np.pi) - np.pi; dde = np.radians(ds) - np.radians(de)
    th = np.hypot(dra, dde); phi = np.arctan2(dde, dra)
    et = -(e1*np.cos(2*phi) - e2*np.sin(2*phi)); ex = -(e1*np.sin(2*phi) + e2*np.cos(2*phi))
    c2p = np.cos(2*phi); s2p = np.sin(2*phi)
    sv = srcvars(raw) if use_vars else None                          # X13: per-source variables for the classes and extra sums
    cls = classes(raw, zs, zl, c2p, s2p, sv) if use_vars else np.zeros((1, len(zs)), np.int64)
    if use_vars:
        with np.errstate(invalid="ignore", divide="ignore"):
            lsz = np.where(sv["vs"], np.log(np.where(sv["vs"], sv["size"], 1.0)), 0.0)
            vP_ = np.isfinite(sv["psfD"]) & (sv["psfD"] > 0); lps = np.where(vP_, 0.25*np.log(np.where(vP_, sv["psfD"], 1.0)), 0.0)
            vN_ = np.isfinite(sv["snr"]) & (sv["snr"] > 0); lsn = np.where(vN_, np.log(np.where(vN_, sv["snr"], 1.0)), 0.0)
        emv = np.where(np.isfinite(sv["em"]), sv["em"], 0.0)
    nv = cls.shape[0]; kk_ = KTOT if use_vars else 1
    out = {"h": {}}
    for key, h in HS.items():
        DlM = float(DM(zl, h)); Dl = DlM/(1 + zl); DMs = DM(zs, h)
        isc = np.clip(4*np.pi*G/C**2*(Dl*MPC)*((DMs - DlM)/(1 + zs))/(DMs/(1 + zs)), 0, None)
        k = np.digitize(th*Dl, EDGES) - 1; g = (k >= 0) & (k < 8) & (isc > 0)
        if key == "h070":
            out["n070"] = int(g.sum())
            if min070 is not None and out["n070"] <= min070: return {"n070": out["n070"]}
            continue
        ww = ws*isc**2; iscs = np.where(isc > 0, isc, 1); vt = et/iscs; vx = ex/iscs
        S = np.zeros((NS_, kk_, 8)); inv = np.zeros((nv, 8))
        cols_ = (ww*vt, ww*vx, ww, ww**2*vt**2, ww**2*vx**2, np.ones_like(ww), isc)
        if use_vars: cols_ = cols_ + (ws, ws*zs, ws*isc, ww*lsz, ww*lps, ww*lsn, ww*emv)   # X13 extra sums
        else: cols_ = cols_ + tuple(np.zeros_like(ww) for _ in range(NS_ - 7))
        for vi in range(nv):
            c = cls[vi]; m_ = g & (c >= 0); idx = c[m_]*8 + k[m_]
            for q, val in enumerate(cols_): S[q] += np.bincount(idx, val[m_], kk_*8).reshape(kk_, 8)
            mi = g & (c < 0); inv[vi] = np.bincount(k[mi], ww[mi], 8)
        o = {"S": S, "inv": inv, "g": g, "k": k, "wv": ww/iscs}
        if want90:                                                   # positions rotated by 90 deg about the centre, ellipticities held
            et9 = -(e1*np.cos(2*(phi + np.pi/2)) - e2*np.sin(2*(phi + np.pi/2))); ex9 = -(e1*np.sin(2*(phi + np.pi/2)) + e2*np.cos(2*(phi + np.pi/2)))
            o["s90"] = np.array([np.bincount(k[g], (ww*et9/iscs)[g], 8), np.bincount(k[g], (ww*ex9/iscs)[g], 8)])
            o["s0"] = np.array([np.bincount(k[g], (ww*vt)[g], 8), np.bincount(k[g], (ww*vx)[g], 8)])
        if geom and key == "h0672":
            mm = g & np.isin(k, MIDB); wm = ww[mm]; tl = np.asarray(raw["tile"], np.int64)[mm]
            out["f_main"] = float(np.bincount(tl, wm).max()/wm.sum()) if wm.sum() > 0 else np.nan
            out["m2"] = float(abs(np.sum(wm*np.exp(2j*phi[mm])))/wm.sum()) if wm.sum() > 0 else np.nan
        out["h"][key] = o
    if rot:                                                          # rotated cross realisations, MID bins, per class (X7's draws)
        gu = np.zeros(len(ii), bool)
        for key in HX: o = out["h"][key]; gu |= o["g"] & np.isin(o["k"], MIDB)
        iu = ii[gu]; etu = et[gu]; exu = ex[gu]; nu = len(iu)
        mats = []
        for key in HX:
            o = out["h"][key]; gm = (o["g"] & np.isin(o["k"], MIDB))[gu]; kb = o["k"][gu] - 3; wv = o["wv"][gu]
            rows, colsi, vals = [], [], []
            for vi in range(nv):
                c = cls[vi][gu]; m_ = gm & (c >= 0); rows.append(c[m_]*3 + kb[m_]); colsi.append(np.nonzero(m_)[0]); vals.append(wv[m_])
            mats.append(sparse.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(colsi))), shape=(kk_*3, nu)))
        rotx = np.zeros((len(HX), kk_*3, R))
        step_ = max(1, min(R, int(100_000 // max(nu, 1))))
        for r0 in range(0, R, step_):
            rr = np.arange(r0, min(R, r0 + step_))
            th2 = 2*np.pi*hash_u(iu[:, None], rr[None, :]); cc = np.cos(th2); ss = np.sin(th2)
            exr = etu[:, None]*ss + exu[:, None]*cc; del th2, cc, ss
            for hi in range(len(HX)): rotx[hi][:, rr] = mats[hi] @ exr
            del exr
        out["rot"] = rotx.reshape(len(HX), kk_, 3, R)
    for key in HX:
        for f in ("g", "k", "wv"): out["h"][key].pop(f)
    return out
def esd(num, den):
    """X7 finish/norm: numerator/den -> ESD in Msun/pc^2 with the multiplicative bias; empty -> 0."""
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.nan_to_num(num/den/KG_PC2/(1 + M_BIAS))
def err(var, den):
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.nan_to_num(np.sqrt(var)/den/KG_PC2, nan=1e9)
