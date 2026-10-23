#!/usr/bin/env python3
"""P2_spec_isolated_lensing: spectroscopically isolated GAMA lenses x KiDS-1000, outer lensing (0.03-3 Mpc) vs v3.

Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (a1bc996fa8, committed alone before any script, shear read or number).
Run:  OMP_NUM_THREADS=1 nice -n 15 python3 p2_spec_isolated_lensing.py <kids_source_cache_dir> <work_dir> [--mutate]
  <kids_source_cache_dir>: F1's reader cache (rebuild_2026_10_22/F1_cluster_cores/f1_extract.py output; read only).
  <work_dir>: scratch dir for this lane's measurement/model caches (not the repo).
Outputs (this lane): p2_spec_isolated_lensing{,_MUTATE}.out, p2_spec_isolated_lensing_results{,_MUTATE}.json.
--mutate: cross shear in place of tangential everywhere (K0a and K0b must fail).
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.
"""
import os, sys, subprocess
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
if not any(a.startswith("--phase=") for a in sys.argv[1:]):
    # driver (no heavy imports): phase A (sources, K0a/K0b, shear measurement -> scratch cache) and phase B (model and
    # scoring) run one after the other in separate processes, so that each stays below 1 GB RSS.
    _base = [sys.executable, os.path.abspath(__file__)] + sys.argv[1:]
    _ra = subprocess.call(_base + ["--phase=A"])
    if _ra != 0:
        sys.exit(2)
    sys.exit(subprocess.call(_base + ["--phase=B"]))
PHASE = [a for a in sys.argv[1:] if a.startswith("--phase=")][0].split("=")[1]
import json, math, time, resource, pickle, hashlib
import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial import cKDTree
from scipy.interpolate import PchipInterpolator, RegularGridInterpolator
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "rebuild_2026_10_22", "F2_outer_lensing"))
import f2_aqual as AQ                                                   # F2's own AQUAL solver + projector (read only)

np.seterr(all="ignore")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
MUT = "--mutate" in sys.argv[1:]
SFX = "_MUTATE" if MUT else ""
CACHE, WORK = ARGS[0], ARGS[1]
os.makedirs(WORK, exist_ok=True)
T0 = time.time()
OUT, RES, CHK = [], {"lane": "P2_spec_isolated_lensing", "criteria": "a1bc996fa8", "mutate": MUT}, {}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, val, thr):
    CHK[name] = bool(ok)
    P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")


def tsec():
    return f"[{time.time() - T0:.0f} s, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB]"


# ============================================================================ 0. constants and distances
G_SI, C_SI, MSUN, MPC = 6.674e-11, 2.998e8, 1.989e30, 3.0857e22
KG_PC2 = MSUN / (3.0857e16) ** 2                     # kg/m^2 per Msun/pc^2
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
H0N, OMN = 0.679, 0.3085                             # native background (F2 H1/H2)
ONEK = 0.9853                                        # B21 (1 + K)
CKMS = 2.998e5
BOX = {0: (129.0, 141.0, -2.0, 3.0), 1: (174.0, 186.0, -3.0, 2.0), 2: (211.5, 223.5, -2.0, 3.0)}
YN = np.array([0.0, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2])   # y_e nodes (frozen grid)
EDGES = np.logspace(np.log10(0.03), np.log10(3.0), 16)                          # Mpc, physical native
RCEN = np.sqrt(EDGES[1:] * EDGES[:-1])
RANGE = {"in": (RCEN > 0.03) & (RCEN <= 0.31), "O1": (RCEN > 0.4) & (RCEN < 1.1), "O2": (RCEN > 1.1) & (RCEN <= 3.0)}
RANGE["out"] = RANGE["O1"] | RANGE["O2"]
assert RANGE["O1"].sum() == 4 and RANGE["O2"].sum() == 3

ZZ = np.linspace(0.0, 2.0, 20001)


def chi_of(om, h):
    E = np.sqrt(om * (1 + ZZ) ** 3 + 1 - om)
    c = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(ZZ))]) * (CKMS / 100.0) / h
    return lambda z: np.interp(z, ZZ, c)


CHI_N = chi_of(OMN, H0N)                             # native comoving, Mpc
CHI_70 = chi_of(0.3, 0.70)                           # catalogue fiducial (LePhare masses)
DA_N = lambda z: CHI_N(z) / (1 + z)
DL_70 = lambda z: CHI_70(z) * (1 + z)

def read_fits_cols(path, cols, step=50000, rowmask=None):
    """read FITS binary-table columns with plain file reads (no memory map, so the file is not resident in RSS);
    rowmask (bool, length NAXIS2) keeps only those rows."""
    with fits.open(path, memmap=True) as h:
        hd = h[1].header; N = hd["NAXIS2"]; ROW = hd["NAXIS1"]; LOC = h.fileinfo(1)["datLoc"]
        _d = h[1].columns.dtype
    dt = np.dtype({"names": list(_d.names), "formats": [_d.fields[n][0].newbyteorder(">") for n in _d.names],
                   "offsets": [_d.fields[n][1] for n in _d.names], "itemsize": _d.itemsize})
    assert dt.itemsize == ROW
    nout = N if rowmask is None else int(rowmask.sum())
    out = {c: np.empty(nout, dt[c].newbyteorder("=")) for c in cols}
    buf = bytearray(step * ROW); pos = 0
    with open(path, "rb") as fh:
        fh.seek(LOC)
        for i in range(0, N, step):
            n = min(step, N - i)
            fh.readinto(memoryview(buf)[:n * ROW])
            rec = np.frombuffer(buf, dtype=dt, count=n)
            sel = slice(None) if rowmask is None else rowmask[i:i + n]
            k = n if rowmask is None else int(sel.sum())
            for c in cols:
                out[c][pos:pos + k] = rec[c][sel]
            pos += k
    return out


def npy_slices(path, slices, out=None):
    """read contiguous slices of a .npy file with plain file reads (no memory map), into `out` if given (reused buffer)."""
    with open(path, "rb") as fh:
        ver = np.lib.format.read_magic(fh)
        shape, fo, dtype = np.lib.format._read_array_header(fh, ver)
        off = fh.tell()
        n = sum(b - a for a, b in slices)
        out = np.empty(n, dtype) if out is None else out[:n]
        pos = 0
        for a, b in slices:
            fh.seek(off + a * dtype.itemsize)
            fh.readinto(memoryview(out[pos:pos + b - a]).cast("B"))
            pos += b - a
    return out


def npy_full(path):
    with open(path, "rb") as fh:
        ver = np.lib.format.read_magic(fh)
        shape, fo, dtype = np.lib.format._read_array_header(fh, ver)
        return np.fromfile(fh, dtype=dtype, count=int(np.prod(shape)))


# ============================================================================ 1. GAMA G3C + KiDS-bright masses
P(f"P2_spec_isolated_lensing{'  [MUTATE: cross shear]' if MUT else ''}   criteria a1bc996fa8   kappa = 1/2 FITTED; footings never pooled")
gpath = os.path.join(REPO, "campaign_fresh_gravity", "_external_data", "cfg471", "G3CGalv10.csv")
sha = hashlib.sha256(open(gpath, "rb").read()).hexdigest()
assert sha.startswith("051950e193e447eb"), sha
g = pd.read_csv(gpath)
fld = np.full(len(g), -1)
for k, (a, b, c, d) in BOX.items():
    fld[(g.RA.values >= a) & (g.RA.values <= b) & (g.Dec.values >= c) & (g.Dec.values <= d)] = k
g = g[fld >= 0].reset_index(drop=True); fld = fld[fld >= 0]
NG = len(g)
ra_g, de_g, z_g, rp_g = g.RA.values.astype(float), g.Dec.values.astype(float), g.Z.values.astype(float), g.Rpetro.values.astype(float)
G_CATAID, G_GROUP, G_RANKIC = g.CATAID.values.copy(), g.GroupID.values.copy(), g.RankIterCen.values.copy()
del g
import gc; gc.collect()
P(f"  G3CGalv10 in G09/G12/G15 boxes: {NG:,} (sha256 {sha[:16]})")


def uvec(ra, de):
    a, d = np.radians(ra), np.radians(de)
    return np.c_[np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)]


DKB = os.path.join(REPO, "real_research", "data", "lensing_rar")
_pos = read_fits_cols(os.path.join(DKB, "KiDS_DR4_brightsample.fits"), ["RAJ2000", "DECJ2000"])
inb = np.zeros(len(_pos["RAJ2000"]), bool)
for a, b, c, d in BOX.values():
    inb |= (_pos["RAJ2000"] >= a - 0.1) & (_pos["RAJ2000"] <= b + 0.1) & (_pos["DECJ2000"] >= c - 0.1) & (_pos["DECJ2000"] <= d + 0.1)
del _pos
bh = read_fits_cols(os.path.join(DKB, "KiDS_DR4_brightsample.fits"), ["RAJ2000", "DECJ2000", "masked", "MAG_AUTO_CALIB"], rowmask=inb)
lh = read_fits_cols(os.path.join(DKB, "KiDS_DR4_brightsample_LePhare.fits"), ["MASS_MED", "REDSHIFT"], rowmask=inb)
rak = bh["RAJ2000"].astype("f8"); dek = bh["DECJ2000"].astype("f8"); mskk = bh["masked"]; rmk = bh["MAG_AUTO_CALIB"].astype("f8")
lMk = lh["MASS_MED"].astype("f8"); zlk = lh["REDSHIFT"].astype("f8")
del bh, lh
kidx = np.arange(len(rak))                                    # rows already restricted to the boxes (+0.1 deg)
TK = cKDTree(uvec(rak, dek))
UG = uvec(ra_g, de_g)
dd, jj = TK.query(UG)
mt = np.degrees(2 * np.arcsin(np.minimum(dd / 2, 1))) * 3600 < 1.5
kk = np.where(mt, kidx[jj], -1)
valid = mt & (lMk[np.maximum(kk, 0)] > 0) & (zlk[np.maximum(kk, 0)] > 0)
lM70 = np.full(NG, np.nan)
zl_le = np.where(valid, zlk[np.maximum(kk, 0)], 0.1)
lM70[valid] = (lMk[kk[valid]] + 0.15 + 2 * np.log10(DL_70(z_g[valid]) / DL_70(zl_le[valid])))
gmask = np.where(mt, mskk[np.maximum(kk, 0)], 1)
# K5: GAMA completeness against KiDS-bright (masked 0, r < 19.5) inside the boxes
inb2 = np.zeros(len(rak), bool)
for a, b, c, d in BOX.values():
    inb2 |= (rak >= a) & (rak <= b) & (dek >= c) & (dek <= d)
selk = inb2 & (mskk == 0) & (rmk < 19.5)
TG = cKDTree(UG)
d2, _ = TG.query(uvec(rak[selk], dek[selk]))
k5 = float(np.mean(np.degrees(2 * np.arcsin(np.minimum(d2 / 2, 1))) * 3600 < 1.5))
check("K5_gama_completeness", k5 >= 0.90, f"{k5:.4f} (n {int(selk.sum()):,})", ">=0.90")
RES["K5"] = k5
del rak, dek, mskk, rmk, lMk, zlk, TK, inb2, selk, d2

# proxy masses and the completeness limit (0.01 z bins)
ZB_ = np.arange(0.0, 0.6001, 0.01); NZB = len(ZB_) - 1
zbin = np.clip(np.digitize(z_g, ZB_) - 1, 0, NZB - 1)
mlc = lM70 + 0.4 * rp_g - 2 * np.log10(DL_70(z_g))
cz_ = np.array([np.nanmedian(mlc[valid & (zbin == i)]) if (valid & (zbin == i)).sum() >= 20 else np.nan for i in range(NZB)])
cz_ = pd.Series(cz_).interpolate(limit_direction="both").values
lim_ = lM70 - 0.4 * (19.8 - rp_g)
MLIM = np.array([np.nanpercentile(lim_[valid & (zbin == i)], 95) if (valid & (zbin == i)).sum() >= 50 else np.nan for i in range(NZB)])
MLIM = pd.Series(MLIM).interpolate(limit_direction="both").values
proxy = cz_[zbin] - 0.4 * rp_g + 2 * np.log10(DL_70(z_g))
sc_proxy = float(np.nanstd((proxy - lM70)[valid]))
lMa = np.where(valid, lM70, proxy)                           # all-galaxy h70 mass (LePhare or proxy)
dlt = np.where(valid, 0.0, 0.30)                             # frozen proxy margin
P(f"  LePhare valid {int(valid.sum()):,} / {NG:,}; proxy scatter {sc_proxy:.3f} dex (frozen margin 0.30); "
  f"M_lim95 at z 0.1/0.2/0.3: {MLIM[10]:.2f}/{MLIM[20]:.2f}/{MLIM[30]:.2f}")
P(f"  {tsec()}")
RES["inventory"] = dict(n_gama=NG, n_lephare_valid=int(valid.sum()), proxy_scatter=sc_proxy, MLIM95=MLIM.tolist())


# (CHI_N * h / 0.70) / CHI_70 is the Omega_m-only ratio q_DA, as F2; native M* = lm70 + 2 log(0.70/h) + 2 log q_DA
def qDA(z):
    return CHI_N(z) * H0N / 0.70 / CHI_70(z)


def lMs_nat(lm70, z, h=H0N):
    return lm70 + 2 * np.log10(0.70 / h) + 2 * np.log10(qDA(z))


def lMb_nat(lm70, z, h=H0N, fhot=0.5):
    ms = 10 ** lMs_nat(lm70, z, h)
    return np.log10(ms * (1 + 10 ** (-0.69 * lm70 + 6.63) + fhot))


lMb_g = lMb_nat(lMa, z_g)                                    # native baryonic mass of every G3C galaxy
DA_g = DA_N(z_g)


def edge_mpc(ra, de, f, z):
    out = np.empty(len(ra))
    for k, (a, b, c, d) in BOX.items():
        m = f == k
        cosd = np.cos(np.radians(de[m]))
        out[m] = np.minimum.reduce([(ra[m] - a) * cosd, (b - ra[m]) * cosd, de[m] - c, d - de[m]])
    return np.radians(out) * DA_N(z)


XG = (CHI_N(z_g)[:, None] * UG)                                 # comoving redshift-space positions (Mpc)
T3 = cKDTree(XG)


def cyl_pairs(ra_c, de_c, z_c, Rmax, dvmax=1000.0):
    """pairs (centre, G3C galaxy) with projected physical separation < Rmax (at the centre z) and |dv| < dvmax,
    found through a 3D comoving sphere that contains the cylinder. Returns cid, j, Rproj (Mpc)."""
    Uc = uvec(ra_c, de_c); Xc = CHI_N(z_c)[:, None] * Uc; DAc = DA_N(z_c)
    dz = dvmax / CKMS * (1 + z_c)
    half = np.maximum(CHI_N(z_c + dz) - CHI_N(z_c), CHI_N(z_c) - CHI_N(np.maximum(z_c - dz, 0)))
    r3 = np.sqrt((Rmax * (1 + z_c)) ** 2 + half ** 2) * 1.01
    lists = T3.query_ball_point(Xc, r=r3)
    cnt = np.array([len(l) for l in lists])
    if cnt.sum() == 0:
        return np.zeros(0, int), np.zeros(0, int), np.zeros(0)
    flat = np.concatenate([np.asarray(l, int) for l in lists]); cid = np.repeat(np.arange(len(cnt)), cnt)
    Rp = np.arccos(np.clip(np.einsum("ij,ij->i", UG[flat], Uc[cid]), -1, 1)) * DAc[cid]
    dv = CKMS * np.abs(z_g[flat] - z_c[cid]) / (1 + z_c[cid])
    ok = (Rp < Rmax) & (dv < dvmax)
    return cid[ok], flat[ok], Rp[ok]


def veto_hits(ra_c, de_c, z_c, lm_c, Riso, self_idx=None, chunk=300):
    """True where a G3C galaxy j (j != self) has R_proj < Riso, |dv| < 1000 km/s and lMa_j + delta_j >= lm_c."""
    n = len(ra_c); out = np.zeros(n, bool)
    for i0 in range(0, n, chunk):
        sl = slice(i0, min(n, i0 + chunk))
        cid, flat, Rp = cyl_pairs(ra_c[sl], de_c[sl], z_c[sl], Riso)
        hit = lMa[flat] + dlt[flat] >= lm_c[sl][cid]
        if self_idx is not None:
            hit &= flat != self_idx[sl][cid]
        out[sl] = np.bincount(cid[hit], minlength=min(n, i0 + chunk) - i0) > 0
    return out


# ============================================================================ 2. lens samples, iso-randoms, randoms
cand = valid & (gmask == 0) & (lM70 >= 8.5) & (lM70 < 11.0) & (z_g > 0.05) & (z_g < 0.50)
comp = lM70 >= MLIM[zbin]
edge = edge_mpc(ra_g, de_g, fld, z_g)
idxC = np.where(cand & comp & (edge >= 1.0))[0]
v1 = veto_hits(ra_g[idxC], de_g[idxC], z_g[idxC], lM70[idxC], 1.0, self_idx=idxC)
idxS1 = idxC[~v1]
e3 = edge[idxS1] >= 3.0
v3 = veto_hits(ra_g[idxS1], de_g[idxS1], z_g[idxS1], lM70[idxS1], 3.0, self_idx=idxS1)
inS3 = e3 & ~v3
idxS3 = idxS1[inS3]
P(f"  lens candidates (z, M*, mask, LePhare) {int(cand.sum()):,}; complete {int((cand & comp).sum()):,}; "
  f"S1 (R_iso 1 Mpc) {len(idxS1):,}; S3 (R_iso 3 Mpc, primary) {len(idxS3):,}")
RES["samples"] = dict(candidates=int(cand.sum()), complete=int((cand & comp).sum()), S1=len(idxS1), S3=len(idxS3))
rng = np.random.default_rng(20261023)
AREA_W = np.array([(math.radians(b - a)) * (math.sin(math.radians(d)) - math.sin(math.radians(c))) for a, b, c, d in BOX.values()])


def draw_positions(n):
    f = rng.integers(0, 3, n)
    ra = np.empty(n); de = np.empty(n)
    for k, (a, b, c, d) in BOX.items():
        m = f == k
        ra[m] = rng.uniform(a, b, m.sum())
        de[m] = np.degrees(np.arcsin(rng.uniform(math.sin(math.radians(c)), math.sin(math.radians(d)), m.sum())))
    return ra, de, f


def make_iso(src_idx, Riso, n_target, veto=True, emin=None):
    emin = Riso if emin is None else emin
    out = []; tried = 0
    while sum(len(o[0]) for o in out) < n_target and tried < 200 * max(1, len(src_idx)):
        nb = 5000
        li = src_idx[rng.integers(0, len(src_idx), nb)]
        ra, de, f = draw_positions(nb)
        z = z_g[li]; lm = lM70[li]
        ok = edge_mpc(ra, de, f, z) >= emin
        if veto:
            vv = np.zeros(nb, bool); vv[ok] = veto_hits(ra[ok], de[ok], z[ok], lm[ok], Riso)
            ok &= ~vv
        out.append((ra[ok], de[ok], z[ok], lm[ok], f[ok], li[ok])); tried += nb
    cat = [np.concatenate([o[i] for o in out])[:n_target] for i in range(6)]
    return cat, tried


(I3ra, I3de, I3z, I3lm, I3f, I3src), tr3 = make_iso(idxS3, 3.0, 4 * len(idxS3))
(I1ra, I1de, I1z, I1lm, I1f, I1src), tr1 = make_iso(idxS1, 1.0, 2 * len(idxS1))
(Rra, Rde, Rz, Rlm, Rf, Rsrc), trR = make_iso(idxS1, 1.0, 3 * len(idxS1), veto=False, emin=1.0)
P(f"  iso-randoms I3 {len(I3ra):,} (acceptance {len(I3ra) / tr3:.3f}); I1 {len(I1ra):,} ({len(I1ra) / tr1:.3f}); randoms R {len(Rra):,}")
RES["samples"].update(I3=len(I3ra), I1=len(I1ra), R=len(Rra), acc_I3=len(I3ra) / tr3, acc_I1=len(I1ra) / tr1,
                      acc_lens_S3_given_S1=float(inS3.sum() / max(1, e3.sum())))
# K3: nesting and a brute-force re-veto (no tree)
def brute_veto(ra, de, z, lm, Riso, self_i=None):
    u = uvec(np.array([ra]), np.array([de]))[0]
    ang = np.arccos(np.clip(UG @ u, -1, 1)); Rp = ang * DA_N(z)
    dv = CKMS * np.abs(z_g - z) / (1 + z)
    hit = (Rp < Riso) & (dv < 1000) & (lMa + dlt >= lm)
    if self_i is not None: hit[self_i] = False
    return bool(hit.any())
k3s = sum(brute_veto(ra_g[i], de_g[i], z_g[i], lM70[i], 3.0, i) for i in idxS3[:200])
k3i = sum(brute_veto(I3ra[i], I3de[i], I3z[i], I3lm[i], 3.0) for i in range(min(200, len(I3ra))))
nest = bool(np.all(np.isin(idxS3, idxS1)))
k3c = bool(np.all(comp[idxS3]) and np.all(edge[idxS3] >= 3.0))
check("K3_samples", nest and k3c and k3s == 0 and k3i == 0, f"S3 in S1 {nest}; complete+edge {k3c}; brute violations lens {k3s} iso {k3i}", "0 violations")
P(f"  {tsec()}")

# ============================================================================ 3. sources (F1 cache, GAMA region in memory)
CELL = 0.2; NRA = int(round(360 / CELL))
BOX_SL = {}
if PHASE == "A":
    CA = npy_full(os.path.join(CACHE, "cell.npy"))
    for kb, (a, b, c, d) in BOX.items():                                # each box with a 1.1-1.2 deg margin
        rows = []
        for drow in range(int(np.floor((c - 1.1 + 90) / CELL)), int(np.floor((d + 1.1 + 90) / CELL)) + 1):
            c0 = int(np.floor((a - 1.2) / CELL)); c1 = int(np.floor((b + 1.2) / CELL))
            rows.append((drow * NRA + c0, drow * NRA + c1))
        sl_ = [(int(np.searchsorted(CA, np.int32(lo), "left")), int(np.searchsorted(CA, np.int32(hi), "right"))) for lo, hi in rows]
        BOX_SL[kb] = [(x, y) for x, y in sorted(sl_) if y > x]
    del CA
SRC = {}; UCELL = CSTART = CEND = None; SRC_BOX = [None]
_BUF = {}
if PHASE == "A":
    NMAXB = max(sum(y - x for x, y in sl_) for sl_ in BOX_SL.values())
    _BUF.update({k: np.empty(NMAXB, dt) for k, dt in (("ra", "f8"), ("dec", "f8"), ("e1", "f4"), ("e2", "f4"), ("w", "f4"),
                                                      ("zb", "f4"), ("cell", "i4"), ("chiN", "f4"))})   # reused for every box


def load_box(kb):
    """load one GAMA box's sources (with margin) into the reused buffers."""
    global UCELL, CSTART, CEND
    if SRC_BOX[0] == kb:
        return
    sl_ = BOX_SL[kb]; n = sum(y - x for x, y in sl_)
    for k in ("ra", "dec", "e1", "e2", "w", "zb", "cell"):
        SRC[k] = npy_slices(os.path.join(CACHE, f"{k}.npy"), sl_, out=_BUF[k])
    _cs = SRC.pop("cell")
    assert np.all(_cs[1:] >= _cs[:-1])
    CSTART = np.r_[0, np.flatnonzero(_cs[1:] != _cs[:-1]) + 1]       # compact cell index (sorted cells, first rows)
    UCELL = _cs[CSTART].copy(); CEND = np.r_[CSTART[1:], n]
    SRC["chiN"] = _BUF["chiN"][:n]
    for i0 in range(0, n, 200000):
        SRC["chiN"][i0:i0 + 200000] = CHI_N(SRC["zb"][i0:i0 + 200000].astype(float))
    SRC_BOX[0] = kb


if PHASE == "A":
    _o0 = len(OUT)
    NSRC_BOX = {kb: sum(y - x for x, y in sl_) for kb, sl_ in BOX_SL.items()}
    P(f"  sources per GAMA box incl. margin (cache rows, Z_B <= 1.2, w > 0): " + ", ".join(f"G{['09', '12', '15'][k]} {n:,}" for k, n in NSRC_BOX.items()))


def box_of(ra):
    f = np.full(len(ra), -1)
    for kb, (a, b, c, d) in BOX.items():
        f[(ra >= a - 1.0) & (ra <= b + 1.0)] = kb
    return f


def measure_boxes(cra, cde, cz, conv, nb=15, extra=None):
    """measure() for centres in any box, loading one box's sources at a time."""
    fb = box_of(cra); assert np.all(fb >= 0)
    out = {k: np.zeros((len(cra), nb)) for k in ("WG", "WX", "WW", "W2", "NN")}
    for kb in range(3):
        sel = np.where(fb == kb)[0]
        if not len(sel): continue
        load_box(kb)
        m = measure(cra[sel], cde[sel], cz[sel], conv, nb=nb, extra=None if extra is None else extra[sel])
        for k in out: out[k][sel] = m[k]
    return out


def ranges_for(ra, de, th_deg):
    d0 = int(np.floor((de - th_deg + 90) / CELL)); d1 = int(np.floor((de + th_deg + 90) / CELL))
    dra = th_deg / max(np.cos(np.radians(min(abs(de) + th_deg, 89.0))), 1e-3)
    los, his = [], []
    for di in range(d0, d1 + 1):
        r0 = int(np.floor(((ra - dra) % 360) / CELL)); n = int(np.ceil(2 * dra / CELL)) + 1
        cells = ((np.arange(r0, r0 + n) % NRA) + di * NRA).astype(UCELL.dtype)
        pos = np.searchsorted(UCELL, cells); pos = np.minimum(pos, len(UCELL) - 1)
        hit = UCELL[pos] == cells
        los.append(CSTART[pos[hit]]); his.append(CEND[pos[hit]])
    lo = np.concatenate(los); hi = np.concatenate(his); m = hi > lo
    return lo[m], hi[m]


def measure(cra, cde, cz, conv, nb=15, extra=None, maxpairs=100_000):
    """Per-centre sums WG (tangential), WX (cross), WW, W2, N in nb bins.
    conv: 'native' (this lane), 'f1' (F1 conventions, K0a), 'record' (CFG110 conventions, K0b; extra = Mgal)."""
    n = len(cra)
    WG = np.zeros((n, nb)); WX = np.zeros((n, nb)); WW = np.zeros((n, nb)); W2 = np.zeros((n, nb)); NN = np.zeros((n, nb))
    if conv == "native":
        chil = CHI_N(cz); Dl = chil / (1 + cz); thmax = 3.0 / Dl * 1.02; chis_all = SRC["chiN"]
    elif conv == "f1":
        chil = F1_DM(cz); Dl = chil / (1 + cz); thmax = 3.0 / Dl * 1.02; chis_all = None
    else:
        chil = extra[:, 1].copy(); Dl = chil / (1 + cz); thmax = 3.0 * (1 + cz) / chil * 1.0001; chis_all = None   # record lens chi
    plan = []
    for i in range(n):
        lo, hi = ranges_for(cra[i], cde[i], np.degrees(thmax[i]) * (1.0 if conv != "record" else 1.5))
        plan.append((lo, hi, int((hi - lo).sum())))
    i = 0
    while i < n:
        j = i; tot = 0
        while j < n and (tot + plan[j][2] <= maxpairs or j == i):
            tot += plan[j][2]; j += 1
        los = np.concatenate([plan[q][0] for q in range(i, j)]); his = np.concatenate([plan[q][1] for q in range(i, j)])
        cidr = np.concatenate([np.full(len(plan[q][0]), q - i) for q in range(i, j)])
        L = his - los
        if L.sum() == 0:
            i = j; continue
        cid = np.repeat(cidr, L)
        off = np.repeat(los - np.concatenate([[0], np.cumsum(L)[:-1]]), L)
        idx = np.arange(L.sum()) + off
        cz_b = cz[i:j][cid]
        zs = SRC["zb"][idx].astype(float)
        keep = zs > cz_b + 0.2
        if conv == "f1":
            keep &= zs <= 1.2                                  # F1's float64 cut drops the float32 Z_B = 1.20 rows
        idx, cid, zs, cz_b = idx[keep], cid[keep], zs[keep], cz_b[keep]
        rac = cra[i:j][cid]; dec_ = cde[i:j][cid]
        if conv == "record":
            dra0 = np.radians(SRC["ra"][idx]) - np.radians(rac); dde = np.radians(SRC["dec"][idx]) - np.radians(dec_)
            keep = dra0 ** 2 + dde ** 2 < (thmax[i:j][cid] / 1.0001) ** 2
            idx, cid, zs, cz_b, dra0, dde, dec_ = idx[keep], cid[keep], zs[keep], cz_b[keep], dra0[keep], dde[keep], dec_[keep]
            x = dra0 * np.cos(np.radians(dec_)); y = dde
            zs_all_rec = zs; cid_all_rec = cid
        else:
            dra0 = np.radians(SRC["ra"][idx]) - np.radians(rac)
            dra0 = (dra0 + np.pi) % (2 * np.pi) - np.pi
            x = dra0 * np.cos(np.radians(dec_)); y = np.radians(SRC["dec"][idx]) - np.radians(dec_)
        th2 = x * x + y * y; th = np.sqrt(th2)
        Rp = th * Dl[i:j][cid]
        if conv == "record":
            Mg = extra[i:j, 0][cid]
            gb = G_SI * Mg * MSUN / (Rp * MPC) ** 2
            k = np.digitize(gb, REC_GB) - 1
        else:
            k = np.searchsorted(EDGES if conv == "native" else F1_EDGES, Rp, "right") - 1
        ok = (k >= 0) & (k < nb)
        idx, cid, zs, x, y, th2, k = idx[ok], cid[ok], zs[ok], x[ok], y[ok], th2[ok], k[ok]
        if conv == "native":
            chis = SRC["chiN"][idx].astype(float)
        elif conv == "f1":
            chis = F1_DM(zs)
        else:
            # the record's DC(): per lens, a 2048-point table on [0, max Z_B of that lens's background sources]
            zmx = np.zeros(j - i); np.maximum.at(zmx, cid_all_rec, zs_all_rec)
            ztab = np.linspace(0, 1, 2048)[None, :] * zmx[:, None]
            Et = np.sqrt(0.3 * (1 + ztab) ** 3 + 0.7)
            tab = np.concatenate([np.zeros((j - i, 1)), np.cumsum(0.5 * (1 / Et[:, 1:] + 1 / Et[:, :-1]) * np.diff(ztab, axis=1), axis=1)], axis=1) * (C_SI / (70e3 / MPC)) / MPC
            tt = np.clip(zs / np.maximum(zmx[cid], 1e-12) * 2047, 0, 2047); i0 = np.minimum(tt.astype(np.int64), 2046); fr = tt - i0
            chis = tab[cid, i0] * (1 - fr) + tab[cid, i0 + 1] * fr
        cl = chil[i:j][cid]
        isc = np.clip(4 * np.pi * G_SI / C_SI ** 2 * (Dl[i:j][cid] * MPC) * (1 - cl / chis), 0, None)
        ok = isc > 0
        idx, cid, x, y, th2, k, isc = idx[ok], cid[ok], x[ok], y[ok], th2[ok], k[ok], isc[ok]
        c2 = (x * x - y * y) / th2; s2 = 2 * x * y / th2
        e1 = SRC["e1"][idx].astype(float); e2 = SRC["e2"][idx].astype(float); w = SRC["w"][idx].astype(float)
        et = -(e1 * c2 - e2 * s2); ex = -(e1 * s2 + e2 * c2)
        key = cid * nb + k; nn_ = (j - i) * nb
        WG[i:j] += np.bincount(key, w * isc * et, nn_).reshape(j - i, nb)
        WX[i:j] += np.bincount(key, w * isc * ex, nn_).reshape(j - i, nb)
        WW[i:j] += np.bincount(key, w * isc * isc, nn_).reshape(j - i, nb)
        W2[i:j] += np.bincount(key, (w * isc * et) ** 2, nn_).reshape(j - i, nb)
        NN[i:j] += np.bincount(key, None, nn_).reshape(j - i, nb)
        i = j
    if MUT:
        WG, WX = WX, WG                                        # MUTATE: cross shear in place of tangential
    return dict(WG=WG, WX=WX, WW=WW, W2=W2, NN=NN)


# F1 conventions (K0a), copied from rebuild_2026_10_22/F1_cluster_cores/f1_cluster_cores.py (read only)
_zb = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; _DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
_DHb = 21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295); _DMb = np.sqrt(7.942 ** 3 / (0.295 * _DHb))
_PCH = PchipInterpolator(np.r_[0, 0.295, _zb], np.r_[0, _DMb, _DMr])
F1_DM = lambda z: _PCH(np.minimum(np.asarray(z, float), 2.33)) * 101.54 / 0.70
F1_EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9)
# record (CFG110) conventions (K0b)
_zr = np.linspace(0, 1.5, 2048); _Er = np.sqrt(0.3 * (1 + _zr) ** 3 + 0.7)
_chir = np.concatenate([[0], np.cumsum(0.5 * (1 / _Er[1:] + 1 / _Er[:-1]) * np.diff(_zr))]) * (C_SI / (70e3 / MPC)) / MPC
REC_DC = lambda z: np.interp(z, _zr, _chir)
REC_GB = np.logspace(np.log10(1e-15), np.log10(5e-12), 16)

PHA = os.path.join(WORK, f"p2_phaseA{SFX}.json")
if PHASE == "A":
    # ---- K0a: F1 per-cluster reproduction
    f1p = os.path.join(CACHE, "f1_meas.pkl")
    if os.path.exists(f1p):
        F1M = [o for o in pickle.load(open(f1p, "rb"))
               if any(a <= o["ra"] <= b and c <= o["dec"] <= d for a, b, c, d in BOX.values())][:30]
        m = measure_boxes(np.array([o["ra"] for o in F1M]), np.array([o["dec"] for o in F1M]), np.array([o["z"] for o in F1M]), "f1", nb=8)
        with np.errstate(all="ignore"):
            Dm = np.nan_to_num(m["WG"] / m["WW"] / KG_PC2 / (1 - 0.01))
        devD = max(float(np.max(np.abs(Dm[c] - o["h070"]["Draw"]) / o["h070"]["E"])) for c, o in enumerate(F1M))
        devW = max(float(np.max(np.abs(m["WW"][c] - o["h070"]["den"]) / np.maximum(o["h070"]["den"], 1e-300) * (o["h070"]["den"] > 0))) for c, o in enumerate(F1M))
        k0a = max(devD, devW)
        check("K0a_F1_per_cluster", k0a <= 1e-6, f"{k0a:.1e} (|dD|/sigma {devD:.1e}, rel den {devW:.1e}; {len(F1M)} F1 clusters in the GAMA boxes)", "<=1e-6")
        RES["K0a"] = dict(dev_D_over_sigma=devD, dev_den=devW)
    else:
        P("K0a_F1_per_cluster N/A (no f1_meas.pkl in the cache dir)"); RES["K0a"] = "N/A"
    # ---- K0b: record per-lens (CFG110) reproduction
    LN = np.load(os.path.join(DKB, "lr_lenses.npz")); PL = np.load(os.path.join(DKB, "cfg110_perlens.npz"))
    inG = np.zeros(len(LN["ra"]), bool)
    for a, b, c, d in BOX.values():
        inG |= (LN["ra"] >= a) & (LN["ra"] <= b) & (LN["dec"] >= c) & (LN["dec"] <= d)
    rk = np.where(inG)[0][:2000]
    mr = measure_boxes(LN["ra"][rk].astype(float), LN["dec"][rk].astype(float), LN["z"][rk].astype(float), "record",
                      extra=np.c_[LN["Mgal"][rk].astype(float), LN["chi"][rk].astype(float)])
    WGr, WWr = PL["WG"][rk].sum(0), PL["WW"][rk].sum(0)
    WGm, WWm = mr["WG"].sum(0), mr["WW"].sum(0)
    rWW = float(WWm.sum() / WWr.sum())
    with np.errstate(all="ignore"):
        sig = np.sqrt(mr["W2"].sum(0)) / WWm
        ratio = (WGm / WWm) / (WGr / WWr)
        good = np.abs(WGm / WWm) / sig > 3
    rmed = float(np.median(ratio[good])) if good.any() else float("nan")
    check("K0b_record_per_lens", (0.90 <= rWW <= 1.000001) and (0.95 <= rmed <= 1.05),
          f"WW ratio {rWW:.7f}; median DeltaSigma ratio {rmed:.6f} over {int(good.sum())} bins (2,000 record lenses in GAMA)", "[0.90,1.000001] & [0.95,1.05]")
    RES["K0b"] = dict(WW_ratio=rWW, median_ratio=rmed, nbins=int(good.sum()), per_bin_ratio=ratio.tolist())
    del LN, PL
    K0_LINES = OUT[_o0:]
else:                                                          # phase B: replay phase A's K0 checks
    _pa = json.load(open(PHA))
    for _l in _pa["K0_lines"]:
        P(_l)
    for _k in ("K0a_F1_per_cluster", "K0b_record_per_lens"):
        if _k in _pa["checks"]: CHK[_k] = _pa["checks"][_k]
    RES["K0a"] = _pa["K0a"]; RES["K0b"] = _pa["K0b"]; RES["phaseA_peak_RSS_GB"] = _pa["peak_RSS_GB"]
P(f"  {tsec()}")

# ============================================================================ 4. measurement of all centres (cached in WORK)
CEN = dict(
    ra=np.concatenate([ra_g[idxS1], I3ra, I1ra, Rra]), dec=np.concatenate([de_g[idxS1], I3de, I1de, Rde]),
    z=np.concatenate([z_g[idxS1], I3z, I1z, Rz]))
NL, NI3, NI1, NR = len(idxS1), len(I3ra), len(I1ra), len(Rra)
SETS = {"L": np.arange(NL), "I3": NL + np.arange(NI3), "I1": NL + NI3 + np.arange(NI1), "R": NL + NI3 + NI1 + np.arange(NR)}
hkey = hashlib.sha256(CEN["ra"].tobytes() + CEN["dec"].tobytes() + CEN["z"].tobytes() + EDGES.tobytes() + b"native-v1").hexdigest()[:16]
mfile = os.path.join(WORK, f"p2_meas_{hkey}.npz")
if os.path.exists(mfile):
    MEAS = dict(np.load(mfile))
    P(f"  measurement cache {os.path.basename(mfile)} reused")
else:
    assert PHASE == "A", "phase B needs phase A's measurement cache"
    fbc = box_of(CEN["ra"])
    order = np.lexsort((CEN["z"], fbc))                         # box by box, low z first
    MEAS = {k: np.zeros((len(order), 15)) for k in ("WG", "WX", "WW", "W2", "NN")}
    for c0 in range(0, len(order), 4000):
        sel = order[c0:c0 + 4000]
        m = measure_boxes(CEN["ra"][sel], CEN["dec"][sel], CEN["z"][sel], "native")
        if MUT:
            m["WG"], m["WX"] = m["WX"], m["WG"]                 # store unmutated (tangential) in the cache
        for k in MEAS: MEAS[k][sel] = m[k]
        P(f"    measured {min(c0 + 4000, len(order)):,}/{len(order):,} centres  {tsec()}")
    np.savez(mfile, **MEAS)
if MUT:
    MEAS["WG"], MEAS["WX"] = MEAS["WX"].copy(), MEAS["WG"].copy()
SRC.clear(); _BUF.clear()                                      # sources no longer needed
if PHASE == "A":
    _pk = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    json.dump(dict(K0_lines=K0_LINES, checks={k: CHK[k] for k in ("K0a_F1_per_cluster", "K0b_record_per_lens") if k in CHK},
                   K0a=RES.get("K0a"), K0b=RES.get("K0b"), peak_RSS_GB=_pk), open(PHA, "w"))
    print(f"  phase A done: peak RSS {_pk:.2f} GB; runtime {time.time() - T0:.0f} s", flush=True)
    sys.exit(0)
cfld = np.full(len(CEN["ra"]), -1)
for k, (a, b, c, d) in BOX.items():
    m_ = (CEN["ra"] >= a) & (CEN["ra"] <= b)
    cfld[m_] = k
PATCH = cfld * 12 + np.clip(np.floor(CEN["ra"] - np.array([BOX[k][0] for k in range(3)])[cfld]).astype(int), 0, 11)
NP_ = 36
P(f"  centres L {NL:,} I3 {NI3:,} I1 {NI1:,} R {NR:,}; patches {len(np.unique(PATCH))}  {tsec()}")

# ============================================================================ 5. catalogue external field (case b)
# 1/Vmax baryonic mass function -> C_b(z)
Mb70 = 10 ** lMa * (1 + 10 ** (-0.69 * lMa + 6.63) + 0.5)
zsel = (z_g > 0.02) & (z_g < 0.30)
DLz = DL_70(z_g)
zgrid = np.linspace(0.0, 0.8, 8001); DLgrid = DL_70(zgrid)
zmax = np.interp(DLz * 10 ** ((19.8 - rp_g) / 5), DLgrid, zgrid)
zmax = np.clip(zmax, z_g, 0.30)
OMEGA = AREA_W.sum()
Vmax = OMEGA / 3 * (CHI_N(zmax) ** 3 - CHI_N(0.02) ** 3)
MbN = 10 ** lMb_g
mbins = np.arange(6.0, 12.6, 0.1)
rho_cum = lambda lmmin: float(np.sum((MbN / Vmax)[zsel & (lMa >= lmmin)]))
rho_tot = rho_cum(8.0)
CB = np.array([min(1.0, rho_cum(max(MLIM[i], 8.0)) / rho_tot) for i in range(NZB)])
Cb_g = CB[zbin]
OMB_RHO = 0.0224 * 2.775e11                                     # Omega_b rho_crit, Msun/Mpc^3 (h-independent)
F_BARY = OMB_RHO / rho_tot
P(f"  1/Vmax: rho_b,gal (lM >= 8) {rho_tot:.3e} Msun/Mpc^3 = {rho_tot / OMB_RHO:.3f} of Omega_b rho_crit; "
  f"C_b(z) at 0.1/0.2/0.3: {CB[10]:.3f}/{CB[20]:.3f}/{CB[29]:.3f}")
RES["field_calib"] = dict(rho_b_gal=rho_tot, frac_of_Omega_b=rho_tot / OMB_RHO, C_b=CB.tolist(), F_baryon_tracing=F_BARY)

def field3d(Rf_list=(5.0, 10.0, 20.0), Rin=1.0, chunk=100):
    out = {("c", rf): np.zeros((NG, 3)) for rf in Rf_list}
    out.update({("lo", 10.0): np.zeros((NG, 3))})
    rmax = max(Rf_list)
    for i0 in range(0, NG, chunk):
        sl = np.arange(i0, min(NG, i0 + chunk))
        lists = T3.query_ball_point(XG[sl], r=rmax * (1 + z_g[sl]))
        cnt = np.array([len(l) for l in lists]); flat = np.concatenate([np.asarray(l, int) for l in lists]); cid = np.repeat(np.arange(len(sl)), cnt)
        dv = XG[flat] - XG[sl][cid]
        s = np.sqrt(np.einsum("ij,ij->i", dv, dv)) / (1 + z_g[sl][cid])        # physical Mpc
        ok = (flat != sl[cid]) & (s >= Rin)
        flat, cid, dv, s = flat[ok], cid[ok], dv[ok], s[ok]
        un = dv / (s * (1 + z_g[sl][cid]))[:, None]
        gmag = G_SI * MbN[flat] * MSUN / (s * MPC) ** 2
        for rf in Rf_list:
            m_ = s <= rf
            for ax in range(3):
                out[("c", rf)][sl, ax] += np.bincount(cid[m_], (gmag / Cb_g[flat] * un[:, ax])[m_], len(sl))
        m_ = s <= 10.0
        for ax in range(3):
            out[("lo", 10.0)][sl, ax] += np.bincount(cid[m_], (gmag * un[:, ax])[m_], len(sl))
    return {k: np.sqrt(np.einsum("ij,ij->i", v, v)) for k, v in out.items()}


def field_slab(Rin=1.0, Rf=10.0, chunk=150):
    gv = np.zeros((NG, 3))
    for i0 in range(0, NG, chunk):
        sl = np.arange(i0, min(NG, i0 + chunk))
        cid, flat, Rp = cyl_pairs(ra_g[sl], de_g[sl], z_g[sl], Rf)
        ok = (flat != sl[cid]) & (Rp >= Rin)
        flat, cid, Rp = flat[ok], cid[ok], Rp[ok]
        d3 = UG[flat] - UG[sl][cid]; d3 -= np.einsum("ij,ij->i", d3, UG[sl][cid])[:, None] * UG[sl][cid]
        un = d3 / np.maximum(np.sqrt(np.einsum("ij,ij->i", d3, d3)), 1e-300)[:, None]
        gm = G_SI * MbN[flat] * MSUN / (Rp * MPC) ** 2 / Cb_g[flat]
        for ax in range(3):
            gv[sl, ax] += np.bincount(cid, gm * un[:, ax], len(sl))
    return np.sqrt(np.einsum("ij,ij->i", gv, gv))


ffile = os.path.join(WORK, "p2_field_v1.npz")
if os.path.exists(ffile) and np.load(ffile)["n"] == NG:
    _f = np.load(ffile); GF = {k: _f[k] for k in ("c5", "c10", "c20", "lo10", "slab")}
else:
    F3 = field3d(); GF = dict(c5=F3[("c", 5.0)], c10=F3[("c", 10.0)], c20=F3[("c", 20.0)], lo10=F3[("lo", 10.0)], slab=field_slab())
    np.savez(ffile, n=NG, **GF)
YE = {foot: {k: v / A0[foot] for k, v in GF.items()} for foot in FOOTS}
for foot in FOOTS:
    YE[foot]["bary"] = YE[foot]["c10"] * F_BARY
    YE[foot]["matter"] = YE[foot]["bary"] * (1 + 5.364)
ye_rep = {}
for foot in FOOTS:
    ye_rep[foot] = {k: dict(median=float(np.median(v[idxS3])), p16=float(np.percentile(v[idxS3], 16)), p84=float(np.percentile(v[idxS3], 84)))
                    for k, v in YE[foot].items()}
    P(f"  [{foot}] S3 lens catalogue y_e (median, 16-84%): " + "; ".join(f"{k} {d['median']:.2e} ({d['p16']:.1e}-{d['p84']:.1e})" for k, d in ye_rep[foot].items()))
RES["ye_S3"] = ye_rep
P(f"  {tsec()}")

# ============================================================================ 6. AQUAL solutions on the y_e grid (F2 solver), K1
sfile = os.path.join(WORK, "p2_efe_v1.pkl")
if os.path.exists(sfile):
    SOL = pickle.load(open(sfile, "rb"))
else:
    SOL = {}
    for ye in YN[1:]:
        s = AQ.solve_efe(float(ye))
        SOL[float(ye)] = dict(r=s["r"], M=s["M"], M_far=s["M_far"], x_e=s["x_e"], iters=s["iters"], resid=s["resid"])
    pickle.dump(SOL, open(sfile, "wb"))
s1 = SOL[1e-6]
sg_ = np.array([0.1, 0.3, 1, 3, 10])
k1a = float(np.max(np.abs(np.interp(np.log(sg_), np.log(s1["r"]), s1["M"]) / AQ.M_iso(sg_) - 1)))
k1b = 0.0
for ye, s in SOL.items():
    if ye < 1e-5: continue
    far = s["r"] >= 10 / s["x_e"]
    k1b = max(k1b, float(np.max(np.abs(s["M"][far] / s["M_far"] - 1))))
check("K1_isolated_limit", k1a <= 1e-3, f"{k1a:.1e}", "<=1e-3")
check("K1_far_field", k1b <= 0.02, f"{k1b:.1e}", "<=0.02")
RES["efe_solves"] = {f"{ye:g}": dict(x_e=s["x_e"], iters=int(s["iters"]), resid=float(s["resid"]), M_far=float(s["M_far"])) for ye, s in SOL.items()}


def m_dimless(sgrid, ye):
    """dimensionless lensing mass M_eff(<s)/M of a point mass in a uniform field y_e (orientation-averaged)."""
    if ye == 0.0:
        return AQ.M_iso(sgrid)
    s = SOL[float(ye)]
    Me = np.interp(np.log(sgrid), np.log(s["r"]), s["M"], left=np.nan, right=s["M_far"])
    return np.where(np.isnan(Me), AQ.M_iso(sgrid), Me)


# ============================================================================ 7. T_own tables (F2's profile), area-averaged in the 15 bins
RGRID_PC = np.logspace(1.0, 10.0, 3601)
LMG = np.round(np.arange(6.8, 11.81, 0.04), 2)
NSUB = 12


def bin_avg(Rpc_edges, fun):
    """area-weighted average of fun(R) over each bin (R in pc); fun takes an array of R."""
    out = np.empty(len(Rpc_edges) - 1)
    lr = np.log(Rpc_edges)
    sub = np.concatenate([np.exp(lr[b] + (np.arange(NSUB) + 0.5) / NSUB * (lr[b + 1] - lr[b])) for b in range(len(out))])
    v = np.concatenate([fun(sub[i:i + 60]) for i in range(0, len(sub), 60)]).reshape(len(out), NSUB)
    wts = sub.reshape(len(out), NSUB) ** 2
    return np.sum(v * wts, 1) / np.sum(wts, 1)


def meff_lens(foot, lms, lmc, f_hot_abs, ye):
    """F2's meff_profile: extended baryons (point stars + cold gas, uniform hot sphere 100 kpc), isolated AQUAL x EFE ratio."""
    a0 = A0[foot] * 3.0857e16 / 1e6; Gpc = 4.30091e-3
    Ms = 10 ** lms; Mcold = 10 ** lmc; Mpt = Ms + Mcold; Mhot = f_hot_abs
    Mb = Mpt + Mhot * np.minimum(1.0, (RGRID_PC / 1e5) ** 3)
    Miso = Mb * AQ.nu_simple(Gpc * Mb / RGRID_PC ** 2 / a0)
    if ye == 0.0:
        return Miso, "linear"
    rM = math.sqrt(Gpc * (Mpt + Mhot) / a0)
    sg = RGRID_PC / rM
    s = SOL[float(ye)]
    Me = np.interp(np.log(sg), np.log(s["r"]), s["M"], left=np.nan, right=s["M_far"])
    Cr = np.where(np.isnan(Me), 1.0, Me / AQ.M_iso(sg))
    return Miso * Cr, "const"


def town_table(foot, h=H0N, dMs=0.0, fhot=0.5, edges=EDGES):
    """T_own[lMG (native M* at h), node, bin] in Msun/pc^2; cold gas from the catalogue h70 mass (F2)."""
    tab = np.empty((len(LMG), len(YN), 15))
    Rpe = edges * 1e6
    for gi, lm in enumerate(LMG):
        lm70 = lm - 2 * np.log10(0.70 / h)
        lmc = lm + (-0.69 * lm70 + 6.63)
        for ni, ye in enumerate(YN):
            M, tail = meff_lens(foot, lm + dMs, lmc, fhot * 10 ** lm, ye)
            tab[gi, ni] = bin_avg(Rpe, lambda R: AQ.delta_sigma(R, RGRID_PC, M, tail))
    return tab


tfile = os.path.join(WORK, "p2_town_v2.pkl")
TOWN = pickle.load(open(tfile, "rb")) if os.path.exists(tfile) else {}
OATS = {"central": {}, "fhot0": dict(fhot=0.0), "fhot1": dict(fhot=1.0), "Ms-0.2": dict(dMs=-0.2), "Ms+0.2": dict(dMs=0.2),
        "h0.672": dict(h=0.672), "h0.686": dict(h=0.686)}
dirty = False
for foot in FOOTS:
    for name, kw in OATS.items():
        if (foot, name) not in TOWN:
            kw2 = dict(kw)
            if "h" in kw2: kw2["edges"] = EDGES * H0N / kw2["h"]
            TOWN[(foot, name)] = town_table(foot, **kw2); dirty = True
if dirty:
    pickle.dump(TOWN, open(tfile, "wb"))
P(f"  T_own tables ready  {tsec()}")


def node_weights(ye):
    """interpolation weights over the YN nodes: linear in y_e below 1e-6, linear in log y_e above; clamp at 1e-2."""
    ye = np.clip(np.asarray(ye, float), 0, YN[-1])
    i_hi = np.searchsorted(YN, ye, "right"); i_hi = np.clip(i_hi, 1, len(YN) - 1); i_lo = i_hi - 1
    lo, hi = YN[i_lo], YN[i_hi]
    t = np.where(i_lo == 0, ye / hi, (np.log(np.maximum(ye, 1e-300)) - np.log(np.where(lo > 0, lo, 1))) / (np.log(hi) - np.log(np.where(lo > 0, lo, 1))))
    t = np.clip(t, 0, 1)
    return i_lo, i_hi, t


def town_per_lens(foot, oat, lm70, z, ye):
    h = OATS[oat].get("h", H0N)
    lm = lMs_nat(lm70, z, h)
    tab = TOWN[(foot, oat)]
    gx = np.clip((lm - LMG[0]) / (LMG[1] - LMG[0]), 0, len(LMG) - 1.001); i0 = gx.astype(int); fx = gx - i0
    a, b, t = node_weights(ye)
    def at(nidx):
        return (1 - fx)[:, None] * tab[i0, nidx] + fx[:, None] * tab[i0 + 1, nidx]
    return (1 - t)[:, None] * at(a) + t[:, None] * at(b)


# ============================================================================ 8. offset machinery (neighbour term), K2
SG = np.logspace(-4, 8, 3001)
UGR = np.logspace(-1.0, 5.5, 391)                                 # 60 per decade (K2 accuracy)
VGR = np.logspace(-3.0, 5.5, 511)
TGL, WGL = np.polynomial.legendre.leggauss(96)
TGL = 0.5 * np.pi * (TGL + 1); WGL = 0.5 * np.pi * WGL


def ext_profile(ye):
    """dimensionless extended (phantom) part: f(s) = 2 pi s^2 Sigma_ext(s) and M_cyl,ext(s) on SG."""
    m = m_dimless(SG, ye) - 1.0
    tail = "linear" if ye == 0.0 else "const"
    lr = np.log(SG); dMdr = np.gradient(m, lr) / SG
    tl = dMdr[-1] if tail == "linear" else 0.0
    ch = np.cosh(AQ.TT); sh = np.sinh(AQ.TT); th_ = np.tanh(AQ.TT)
    w = np.full(AQ.TT.size, AQ.TT[1] - AQ.TT[0]); w[0] *= 0.5; w[-1] *= 0.5
    Sig = np.empty(SG.size); Mcyl = np.empty(SG.size)
    for c0 in range(0, SG.size, 100):
        R = SG[c0:c0 + 100]
        r = R[:, None] * ch[None, :]
        fv = np.interp(np.log(r), lr, dMdr, left=dMdr[0], right=tl)
        Mcyl[c0:c0 + 100] = np.interp(np.log(R), lr, m) + np.sum(fv * (1 - th_) * R[:, None] * sh * w, axis=1)
        Sig[c0:c0 + 100] = np.sum(fv / ch * w, axis=1) / (2 * math.pi * R)
    return 2 * math.pi * SG ** 2 * Sig, Mcyl


def mc_table(fS, Mcyl):
    """M_c,ext(u, v): projected extended mass inside a circle of radius u whose centre is v from the profile centre."""
    lS = np.log(SG)
    part = np.empty((len(UGR), len(VGR)))
    for u0 in range(0, len(UGR), 4):
        U = UGR[u0:u0 + 4, None, None]; V = VGR[None, :, None]
        a = np.abs(U - V); b = U + V
        s = a + (b - a) * (1 - np.cos(TGL[None, None, :])) / 2
        ds = (b - a) * np.sin(TGL[None, None, :]) / 2
        arg = np.clip((s * s + V * V - U * U) / (2 * s * V), -1, 1)
        integ = np.interp(np.log(s), lS, fS) / s * (np.arccos(arg) / np.pi) * ds
        part[u0:u0 + 4] = np.sum(integ * WGL[None, None, :], axis=2)
    inner = np.where(VGR[None, :] < UGR[:, None], np.interp(np.log(np.maximum(UGR[:, None] - VGR[None, :], 1e-12)), lS, Mcyl), 0.0)
    return inner + part


ofile = os.path.join(WORK, "p2_offset_v2.npz")
if os.path.exists(ofile):
    _o = np.load(ofile); MCT = _o["MCT"]; MCYL = _o["MCYL"]; FS = _o["FS"]
else:
    MCT = np.empty((len(YN), len(UGR), len(VGR))); MCYL = np.empty((len(YN), SG.size)); FS = np.empty((len(YN), SG.size))
    for ni, ye in enumerate(YN):
        FS[ni], MCYL[ni] = ext_profile(float(ye))
        MCT[ni] = mc_table(FS[ni], MCYL[ni])
    np.savez(ofile, MCT=MCT, MCYL=MCYL, FS=FS)
MCI = [RegularGridInterpolator((np.log(UGR), np.log(VGR)), np.log(np.maximum(MCT[ni], 1e-300)), bounds_error=False, fill_value=None)
       for ni in range(len(YN))]                                     # log-log interpolation
P(f"  offset tables ready  {tsec()}")

LMB_T = np.round(np.arange(7.0, 12.51, 0.05), 3)                 # neighbour native log M_b type grid
DGR = np.logspace(-3, np.log10(6.0), 121)                         # Mpc
NSUBB = 17


def mc_ext(ni, u, v):
    v = np.maximum(v, VGR[0])
    return np.exp(MCI[ni](np.c_[np.log(u), np.log(v)]))


def gtable(foot, ni, lmb, dgrid=DGR):
    """extended-part bin-averaged tangential DeltaSigma (Msun/pc^2) about a centre, for a neighbour of native log M_b
    at the offsets dgrid (Mpc); shape (15, len(dgrid))."""
    Mb = 10 ** lmb
    rM = math.sqrt(G_SI * Mb * MSUN / A0[foot]) / MPC                # Mpc
    out = np.empty((15, len(dgrid)))
    for k in range(15):
        R1, R2 = EDGES[k], EDGES[k + 1]
        Rs = np.exp(np.linspace(np.log(R1), np.log(R2), NSUBB))
        uu = np.repeat(Rs / rM, len(dgrid)); vv = np.tile(dgrid / rM, NSUBB)
        Mc = mc_ext(ni, uu, vv).reshape(NSUBB, len(dgrid))
        hstep = (np.log(R2) - np.log(R1)) / (NSUBB - 1)
        wS = np.ones(NSUBB); wS[1:-1:2] = 4; wS[2:-1:2] = 2; wS *= hstep / 3
        integ = np.sum(Mc * wS[:, None], axis=0)
        out[k] = Mb * (2 * integ - (Mc[-1] - Mc[0])) / (math.pi * ((R2 * 1e6) ** 2 - (R1 * 1e6) ** 2))
    return out


def point_part(Mb, d):
    """exact bin-averaged tangential DeltaSigma (Msun/pc^2) of point masses Mb at offsets d (Mpc); shape (n, 15)."""
    R1 = EDGES[:-1][None, :]; R2 = EDGES[1:][None, :]; dd_ = d[:, None]
    P1 = np.where(dd_ < R2, 2 * np.log(R2 / np.maximum(R1, dd_)), 0.0)
    P2 = ((dd_ >= R1) & (dd_ < R2)).astype(float)
    return Mb[:, None] * (P1 - P2) / (np.pi * ((R2 * 1e6) ** 2 - (R1 * 1e6) ** 2))


gfile = os.path.join(WORK, "p2_gtab_v2.npz")
if os.path.exists(gfile):
    GT = dict(np.load(gfile)); GT = {f: GT[f] for f in FOOTS}
else:
    GT = {f: np.empty((len(LMB_T), len(YN), 15, len(DGR))) for f in FOOTS}
    for f in FOOTS:
        for ti, lmb in enumerate(LMB_T):
            for ni in range(len(YN)):
                GT[f][ti, ni] = gtable(f, ni, lmb)
    np.savez(gfile, **GT)
P(f"  neighbour tables ready  {tsec()}")

# ---- K2 checks
Rt = np.array([0.03, 0.3, 3.0]); rg_ = np.logspace(-6, 6, 6001)
pm = AQ.delta_sigma(Rt, rg_, np.ones_like(rg_), "const") * math.pi * Rt ** 2
sis = AQ.delta_sigma(Rt, rg_, rg_.copy(), "linear") * 4 * Rt
k2a = float(max(np.max(np.abs(pm - 1)), np.max(np.abs(sis - 1))))
# (ii) offset machinery at d -> 0 vs the centred bin average of the same extended profile (lM_b 10.5, y_e 1e-4)
ni4 = int(np.where(YN == 1e-4)[0][0]); lmb_t = 10.5
Mb_t = 10 ** lmb_t; rM_t = math.sqrt(G_SI * Mb_t * MSUN / A0["canonical"]) / MPC
g0 = gtable("canonical", ni4, lmb_t, dgrid=np.array([1e-9]))[:, 0]
mext = (m_dimless(SG, 1e-4) - 1.0) * Mb_t
cent = bin_avg(EDGES * 1e6, lambda R: AQ.delta_sigma(R / (rM_t * 1e6), SG, mext, "const") / (rM_t * 1e6) ** 2)
k2b = float(np.max(np.abs(g0 / cent - 1)))
# (iii) the frac integral reproduces a point mass for a narrow Gaussian profile
sgm = 1e-3
fG = 2 * math.pi * SG ** 2 * np.exp(-SG ** 2 / (2 * sgm ** 2)) / (2 * math.pi * sgm ** 2)
McG = 1 - np.exp(-SG ** 2 / (2 * sgm ** 2))
uu_ = np.array([1.0, 1.0, 10.0, 10.0, 100.0]); vv_ = np.array([0.5, 2.0, 3.0, 30.0, 99.0])
_U, _V = UGR, VGR
UGR, VGR = uu_, vv_
mcG = np.diag(mc_table(fG, McG))
UGR, VGR = _U, _V
k2c = float(np.max(np.abs(mcG - (vv_ < uu_).astype(float))))
# (iv) uniform sheet of identical neighbours (y_e 1e-4 profile) gives ~0
dfine = np.logspace(-4, np.log10(80.0), 1500)
gsheet = gtable("canonical", ni4, lmb_t, dgrid=dfine) + point_part(np.full(dfine.size, Mb_t), dfine).T
integ_ = np.trapz(gsheet * 2 * np.pi * dfine[None, :], dfine, axis=1)
absint = np.trapz(np.abs(gsheet) * 2 * np.pi * dfine[None, :], dfine, axis=1)
k2d = float(np.max(np.abs(integ_) / absint))
check("K2_projection", k2a <= 1e-3 and k2b <= 1e-3 and k2c <= 1e-3 and k2d <= 1e-2,
      f"analytic {k2a:.1e}; offset d->0 {k2b:.1e}; Gaussian->point {k2c:.1e}; uniform sheet {k2d:.1e}", "<=1e-3,1e-3,1e-3,1e-2")
RES["K2"] = dict(analytic=k2a, centred=k2b, point=k2c, sheet=k2d)
P(f"  {tsec()}")

# ============================================================================ 9. neighbour pairs and T_nbr per centre
self_c = np.full(len(CEN["ra"]), -1); self_c[:NL] = idxS1
PAIRS = []
for i0 in range(0, len(CEN["ra"]), 300):
    sl = np.arange(i0, min(len(CEN["ra"]), i0 + 300))
    cid, flat, dd = cyl_pairs(CEN["ra"][sl], CEN["dec"][sl], CEN["z"][sl], 6.0)
    cid = sl[cid]
    ok = flat != self_c[cid]
    PAIRS.append((cid[ok].astype(np.int32), flat[ok].astype(np.int32), dd[ok]))
PC = np.concatenate([p[0] for p in PAIRS]); PJ = np.concatenate([p[1] for p in PAIRS])
PD = np.concatenate([p[2] for p in PAIRS]).astype(np.float32)
del PAIRS
P(f"  neighbour pairs (d < 6 Mpc, |dv| < 1000 km/s): {len(PC):,}  {tsec()}")
tix = np.clip(np.round((lMb_g - LMB_T[0]) / 0.05).astype(int), 0, len(LMB_T) - 1)
MBN_g = 10 ** lMb_g


def tnbr(foot, ye_gal=None, node=None, subset=None):
    """per-centre neighbour term (Ncentres, 15); ye_gal: per-galaxy y_e (case b) or node index (uniform)."""
    sel = np.arange(len(PC)) if subset is None else np.where(np.isin(PC, subset))[0]
    out = np.zeros((len(CEN["ra"]), 15))
    G_ = GT[foot]
    for c0 in range(0, len(sel), 8000):
        s = sel[c0:c0 + 8000]
        pd_ = PD[s].astype(float)
        gd = np.clip((np.log(np.maximum(pd_, DGR[0])) - np.log(DGR[0])) / (np.log(DGR[1]) - np.log(DGR[0])), 0, len(DGR) - 1.001)
        d0 = gd.astype(np.int64); fd = (gd - d0)[:, None]
        t = tix[PJ[s]]
        if node is not None:
            a = np.full(len(s), node); b = a; w = np.zeros(len(s))
        else:
            a, b, w = node_weights(ye_gal[PJ[s]])
        ext = ((1 - w)[:, None] * ((1 - fd) * G_[t, a, :, d0] + fd * G_[t, a, :, d0 + 1])
               + w[:, None] * ((1 - fd) * G_[t, b, :, d0] + fd * G_[t, b, :, d0 + 1]))
        contrib = ext + point_part(MBN_g[PJ[s]], pd_)
        for k in range(15):
            out[:, k] += np.bincount(PC[s], contrib[:, k], len(out))
    return out


TN = {}
for foot in FOOTS:
    TN[(foot, "a")] = tnbr(foot, node=0)
    TN[(foot, "b")] = tnbr(foot, ye_gal=YE[foot]["c10"])
    TN[(foot, "b_lo")] = tnbr(foot, ye_gal=YE[foot]["lo10"])
P(f"  T_nbr computed (a, b, b_lo; both footings)  {tsec()}")

# ============================================================================ 10. stacks, F2 amplitudes, verdicts
fK = 1.0 / KG_PC2 / ONEK


def patch_sums(cidx, arr):
    out = np.zeros((NP_, 15)); np.add.at(out, PATCH[cidx], arr); return out


def stack(terms, model=None, dscale=1.0, use="WG"):
    """terms: list of (centre indices, sign, per-centre model array or None). Returns d, m, replicates."""
    d = 0.0; mm = 0.0; dj = 0.0; mj = 0.0
    for cidx, sg_, mod in terms:
        sgm_ = patch_sums(cidx, MEAS[use][cidx]); swm = patch_sums(cidx, MEAS["WW"][cidx])
        tg, tw = sgm_.sum(0), swm.sum(0)
        d = d + sg_ * tg / tw * fK * dscale
        dj = dj + sg_ * (tg[None] - sgm_) / (tw[None] - swm) * fK * dscale
        if mod is not None:
            smm = patch_sums(cidx, MEAS["WW"][cidx] * mod[cidx] if mod.shape[0] == len(CEN["ra"]) else MEAS["WW"][cidx] * mod)
            tm = smm.sum(0)
            mm = mm + sg_ * tm / tw
            mj = mj + sg_ * (tm[None] - smm) / (tw[None] - swm)
    var = (NP_ - 1) / NP_ * np.sum((dj - dj.mean(0)) ** 2, axis=0)
    return dict(d=d, m=mm, dj=dj, mj=mj, var=var)


def amps(st):
    d, mm, dj, mj, var = st["d"], st["m"], st["dj"], st["mj"], st["var"]
    o = {}
    for lab, msk in RANGE.items():
        sel = msk & np.isfinite(d) & (var > 0)
        w = np.where(sel, mm / var, 0.0)
        A = float(np.sum(w * d) / np.sum(w * mm))
        Aj = np.sum(w[None] * dj, axis=1) / np.sum(w[None] * mj, axis=1)
        sA = float(math.sqrt((NP_ - 1) / NP_ * np.sum((Aj - Aj.mean()) ** 2)))
        o[f"A_{lab}"] = A; o[f"sA_{lab}"] = sA
    return o


def cls_amp(A, s):
    if A - 1 > 3 * s: return "short"
    if 1 - A > 3 * s: return "over"
    if abs(A - 1) <= 2 * s: return "consistent"
    return "between"


def cross_A(st_a, m_b):
    """A of model b relative to model a with a's weights, per range."""
    var, ma = st_a["var"], st_a["m"]; o = {}
    for lab, msk in RANGE.items():
        sel = msk & (var > 0)
        w = np.where(sel, ma / var, 0.0)
        o[lab] = float(np.sum(w * m_b) / np.sum(w * ma))
    return o


L3 = SETS["L"][inS3]; L1 = SETS["L"]
lens_g3 = idxS3; lens_g1 = idxS1


def town_lens(foot, case, oat="central", lens_g=idxS1, node=None):
    if case == "a" or node is not None:
        ye = np.zeros(len(lens_g)) if node is None else np.full(len(lens_g), YN[node])
    else:
        ye = YE[foot]["c10" if case == "b" else ("lo10" if case == "b_lo" else case)][lens_g]
    return town_per_lens(foot, oat, lM70[lens_g], z_g[lens_g], ye)


def full_model(foot, case, oat="central", tn=None):
    """per-centre model: T_own for lens centres (S1 superset) + T_nbr for every centre."""
    tn = TN[(foot, case if case in ("a", "b", "b_lo") else "b")] if tn is None else tn
    mod = tn.copy()
    mod[:NL] += town_lens(foot, case, oat)
    return mod


def primary(foot, case, oat="central", sample="S3", raw=False, no_nbr=False, dscale=1.0, tn=None):
    mod = full_model(foot, case, oat, tn)
    if no_nbr:
        mod = np.zeros_like(mod); mod[:NL] = town_lens(foot, case, oat)
    Lc = L3 if sample == "S3" else L1
    Ic = SETS["I3"] if sample == "S3" else SETS["I1"]
    other = SETS["R"] if raw else Ic
    return stack([(Lc, +1, mod), (other, -1, mod)], dscale=dscale)


VER = {}; AMP = {}
for foot in FOOTS:
    sa = primary(foot, "a"); sb = primary(foot, "b"); sbl = primary(foot, "b_lo")
    Aa, Ab, Abl = amps(sa), amps(sb), amps(sbl)
    AMP[foot] = dict(a=Aa, b=Ab, b_lo=Abl)
    xa = cross_A(sa, sb["m"])
    S = {r: abs(xa[r] - 1) / Aa[f"sA_{r}"] for r in ("O1", "O2")}
    Smax = max(S.values())
    ca = (cls_amp(Aa["A_O1"], Aa["sA_O1"]), cls_amp(Aa["A_O2"], Aa["sA_O2"]))
    cb = (cls_amp(Ab["A_O1"], Ab["sA_O1"]), cls_amp(Ab["A_O2"], Ab["sA_O2"]))
    if Smax < 3:
        v = "UNDECIDABLE (N too small)"
    elif cb == ("consistent", "consistent"):
        v = "v3 PASSES (catalogue EFE)"
    elif ca == ("consistent", "consistent"):
        v = "v3 FAILS (EFE tension)"
    elif "short" in ca:
        v = "v3 FAILS (short even at zero external field)"
    elif "over" in cb:
        v = "v3 FAILS (overshoots even with the catalogue EFE)"
    else:
        v = "UNDECIDABLE (between)"
    Nneed = int(math.ceil(len(idxS3) * (3 / Smax) ** 2)) if Smax > 0 else None
    VER[foot] = dict(verdict=v, cls_a=ca, cls_b=cb, S=S, Smax=Smax, A_b_over_a=xa, N=len(idxS3), N_needed=Nneed)
    P(f"\n  [{foot}] S3 primary  (Delta = L - I3; model T_own + T_nbr(L) - T_nbr(I3))")
    for lab, A_ in (("(a) y_e = 0", Aa), ("(b) catalogue y_e", Ab), ("(b) lower bracket", Abl)):
        P(f"    {lab:22s} A_in {A_['A_in']:.3f}+-{A_['sA_in']:.3f}  A_O1 {A_['A_O1']:.3f}+-{A_['sA_O1']:.3f}  "
          f"A_O2 {A_['A_O2']:.3f}+-{A_['sA_O2']:.3f}  A_out {A_['A_out']:.3f}+-{A_['sA_out']:.3f}")
    P(f"    model (b)/(a) with (a)'s weights: O1 {xa['O1']:.3f}  O2 {xa['O2']:.3f};  S = O1 {S['O1']:.2f}, O2 {S['O2']:.2f} sigma")
    P(f"    classes (O1, O2): (a) {ca}; (b) {cb}")
    P(f"    VERDICT [{foot}]: {v}" + (f"; N_needed = {Nneed:,} (N = {len(idxS3):,})" if v.startswith("UNDECIDABLE (N") else ""))
    prof = dict(R=RCEN.tolist(), d=sa["d"].tolist(), sig=np.sqrt(sa["var"]).tolist(), m_a=sa["m"].tolist(), m_b=sb["m"].tolist(),
                m_b_lo=sbl["m"].tolist(), cov=((NP_ - 1) / NP_ * (sa["dj"] - sa["dj"].mean(0)).T @ (sa["dj"] - sa["dj"].mean(0))).tolist())
    VER[foot]["profile"] = prof
    P("    R (Mpc)     " + " ".join(f"{r:7.3f}" for r in RCEN))
    P("    Delta       " + " ".join(f"{x:7.3f}" for x in sa["d"]))
    P("    sigma       " + " ".join(f"{x:7.3f}" for x in np.sqrt(sa["var"])))
    P("    model (a)   " + " ".join(f"{x:7.3f}" for x in sa["m"]))
    P("    model (b)   " + " ".join(f"{x:7.3f}" for x in sb["m"]))
LANE = VER["canonical"]["verdict"] if VER["canonical"]["verdict"] == VER["alt"]["verdict"] else "UNDECIDABLE (footing split)"
P(f"\n  LANE VERDICT (both footings): {LANE}")
RES["verdict"] = VER; RES["lane_verdict"] = LANE; RES["amplitudes_S3"] = AMP
P(f"  {tsec()}")

# ---- K4: cross-shear null of Delta (S3)
stx = stack([(L3, +1, None), (SETS["I3"], -1, None)], use="WX")
okx = stx["var"] > 0
chi2x = float(np.sum(stx["d"][okx] ** 2 / stx["var"][okx])); px = float(stats.chi2.sf(chi2x, int(okx.sum())))
check("K4_cross_null", px >= 0.001, f"chi2 {chi2x:.1f}/{int(okx.sum())} p {px:.3g}", "p>=0.001")
RES["K4"] = dict(chi2=chi2x, n=int(okx.sum()), p=px, dX=stx["d"].tolist())

# ============================================================================ 11. reported diagnostics (not verdict lines)
P("\n  REPORTED (not verdict lines)")
DIAG = {}
for foot in FOOTS:
    D = {}
    # robustness tags
    for tag, kw in (("raw L-R", dict(raw=True)), ("no T_nbr", dict(no_nbr=True)), ("S1 (L-I1)", dict(sample="S1"))):
        A_a = amps(primary(foot, "a", **kw)); A_b = amps(primary(foot, "b", **kw))
        D[tag] = dict(a=A_a, b=A_b, cls_a=(cls_amp(A_a["A_O1"], A_a["sA_O1"]), cls_amp(A_a["A_O2"], A_a["sA_O2"])),
                      cls_b=(cls_amp(A_b["A_O1"], A_b["sA_O1"]), cls_amp(A_b["A_O2"], A_b["sA_O2"])))
        P(f"   [{foot}] {tag:10s} (a) O1 {A_a['A_O1']:.3f}+-{A_a['sA_O1']:.3f} O2 {A_a['A_O2']:.3f}+-{A_a['sA_O2']:.3f} {D[tag]['cls_a']} | "
          f"(b) O1 {A_b['A_O1']:.3f}+-{A_b['sA_O1']:.3f} O2 {A_b['A_O2']:.3f}+-{A_b['sA_O2']:.3f} {D[tag]['cls_b']}")
    Ablo = AMP[foot]["b_lo"]
    D["b_lo_cls"] = (cls_amp(Ablo["A_O1"], Ablo["sA_O1"]), cls_amp(Ablo["A_O2"], Ablo["sA_O2"]))
    P(f"   [{foot}] (b) lower-bracket field classes {D['b_lo_cls']}")
    # environment-only stack I3 - R vs T_nbr(I3) - T_nbr(R)
    for case in ("a", "b"):
        se = stack([(SETS["I3"], +1, TN[(foot, case)]), (SETS["R"], -1, TN[(foot, case)])])
        D[f"env_{case}"] = dict(d=se["d"].tolist(), sig=np.sqrt(se["var"]).tolist(), m=se["m"].tolist())
    se = D["env_a"]
    P(f"   [{foot}] environment-only I3 - R (Msun/pc^2) O1/O2 bins: data " + " ".join(f"{x:.3f}" for x in np.array(se['d'])[RANGE['out']])
      + " | +-" + " ".join(f"{x:.3f}" for x in np.array(se['sig'])[RANGE['out']])
      + " | T_nbr (a) " + " ".join(f"{x:.3f}" for x in np.array(se['m'])[RANGE['out']])
      + " | (b) " + " ".join(f"{x:.3f}" for x in np.array(D['env_b']['m'])[RANGE['out']]))
    # one at a time (T_own only; T_nbr held at the case)
    oat = {}
    for name in OATS:
        if name == "central": continue
        h = OATS[name].get("h", H0N)
        ds = h / H0N
        A_a = amps(primary(foot, "a", oat=name, dscale=ds)); A_b = amps(primary(foot, "b", oat=name, dscale=ds))
        oat[name] = dict(a=A_a, b=A_b)
    for name, ds in (("Sigma_crit -3%", 0.97), ("Sigma_crit +3%", 1.03)):
        oat[name] = dict(a=amps(primary(foot, "a", dscale=ds)), b=amps(primary(foot, "b", dscale=ds)))
    for name, o in oat.items():
        P(f"   [{foot}] OAT {name:15s} (a) O1 {o['a']['A_O1']:.3f} O2 {o['a']['A_O2']:.3f} | (b) O1 {o['b']['A_O1']:.3f} O2 {o['b']['A_O2']:.3f}")
    D["OAT"] = oat
    # brackets of (b): T_own with the bracket field, T_nbr held at (b) central
    br = {}
    for key in ("c5", "c20", "slab", "bary", "matter"):
        mod = TN[(foot, "b")].copy(); mod[:NL] += town_per_lens(foot, "central", lM70[idxS1], z_g[idxS1], YE[foot][key][idxS1])
        br[key] = amps(stack([(L3, +1, mod), (SETS["I3"], -1, mod)]))
        P(f"   [{foot}] (b) bracket {key:6s} median y_e {ye_rep[foot][key]['median']:.2e}: A_O1 {br[key]['A_O1']:.3f}+-{br[key]['sA_O1']:.3f} "
          f"A_O2 {br[key]['A_O2']:.3f}+-{br[key]['sA_O2']:.3f}")
    D["brackets"] = br
    # uniform-y_e scan -> y_allow
    scan = {}
    sub = np.concatenate([L3, SETS["I3"]])
    for ni in range(len(YN)):
        tn_ = tnbr(foot, node=ni, subset=sub)
        mod = tn_.copy(); mod[:NL] += town_lens(foot, "a", node=ni)
        scan[f"{YN[ni]:g}"] = amps(stack([(L3, +1, mod), (SETS["I3"], -1, mod)]))
    allow = [YN[ni] for ni in range(len(YN)) if scan[f"{YN[ni]:g}"]["A_O1"] <= 1 + 2 * scan[f"{YN[ni]:g}"]["sA_O1"]
             and scan[f"{YN[ni]:g}"]["A_O2"] <= 1 + 2 * scan[f"{YN[ni]:g}"]["sA_O2"]]
    y_allow = max(allow) if allow else None
    D["scan"] = scan; D["y_allow"] = y_allow
    # AMENDMENT A1 (post-result, reported only): the lower side, the smallest grid field the data do not overshoot
    need = [YN[ni] for ni in range(len(YN)) if scan[f"{YN[ni]:g}"]["A_O1"] >= 1 - 2 * scan[f"{YN[ni]:g}"]["sA_O1"]
            and scan[f"{YN[ni]:g}"]["A_O2"] >= 1 - 2 * scan[f"{YN[ni]:g}"]["sA_O2"]]
    D["y_need_A1"] = min(need) if need else None
    P(f"   [{foot}] A1 (post-result): smallest grid y_e with A_O1, A_O2 >= 1 - 2 sigma (data not below the model) = {D['y_need_A1']}")
    # AMENDMENT A1 (post-result, reported only): S1's own decisiveness and the significance of its O2 deficit at y_e = 0
    s1a = primary(foot, "a", sample="S1"); s1b = primary(foot, "b", sample="S1")
    A1a = amps(s1a); x1 = cross_A(s1a, s1b["m"])
    D["S1_A1"] = dict(S={r: abs(x1[r] - 1) / A1a[f"sA_{r}"] for r in ("O1", "O2")}, A_b_over_a=x1,
                      O2_deficit_sigma_a=(1 - A1a["A_O2"]) / A1a["sA_O2"], N=len(idxS1))
    P(f"   [{foot}] A1 (post-result): S1 model (b)/(a) O1 {x1['O1']:.3f} O2 {x1['O2']:.3f}; S = O1 {D['S1_A1']['S']['O1']:.2f}, "
      f"O2 {D['S1_A1']['S']['O2']:.2f} sigma; S1 O2 below the y_e = 0 model by {D['S1_A1']['O2_deficit_sigma_a']:.1f} sigma (N {len(idxS1):,})")
    P(f"   [{foot}] uniform y_e scan: " + "; ".join(f"{k}: O1 {v['A_O1']:.2f}+-{v['sA_O1']:.2f} O2 {v['A_O2']:.2f}+-{v['sA_O2']:.2f}" for k, v in scan.items()))
    P(f"   [{foot}] y_allow (largest grid y_e with A_O1, A_O2 <= 1 + 2 sigma) = {y_allow}; S3 median catalogue y_e central "
      f"{ye_rep[foot]['c10']['median']:.2e}, lower {ye_rep[foot]['lo10']['median']:.2e}")
    # needed extra lensing mass and boost
    D["required_extra"] = {c: {r: AMP[foot][c][f"A_{r}"] - 1 for r in ("in", "O1", "O2")} for c in ("a", "b")}
    DIAG[foot] = D
WWL = MEAS["WW"][L3].sum(0) / len(L3); WWR = MEAS["WW"][SETS["R"]].sum(0) / len(SETS["R"])
WWI = MEAS["WW"][SETS["I3"]].sum(0) / len(SETS["I3"])
boost = (WWL / WWR).tolist(); boostI = (WWL / WWI).tolist()
P("   source weight per centre, S3 lenses / randoms R: " + " ".join(f"{x:.3f}" for x in boost))
P("   source weight per centre, S3 lenses / iso-randoms I3 (same z, M* draw; the boost): " + " ".join(f"{x:.3f}" for x in boostI))
DIAG["boost_vs_R"] = boost; DIAG["boost_vs_I3"] = boostI
# lens properties: G3C membership, GKV mass offset (G09)
sat = (G_GROUP[idxS3] > 0) & (G_RANKIC[idxS3] > 1)
DIAG["S3_g3c_nonCentral_frac"] = float(sat.mean())
gk = pd.read_csv(os.path.join(REPO, "..", "_external_data", "gama_dr4_gkv", "gkv_stellarmass_g09.csv"))
gk = gk.drop_duplicates("CATAID").set_index("CATAID")
cat3 = G_CATAID[idxS3]; hasg = np.isin(cat3, gk.index.values)
off = (gk.loc[cat3[hasg], "logmstar"].values - lM70[idxS3][hasg])
okg = np.isfinite(off) & (gk.loc[cat3[hasg], "logmstar"].values > 5)
DIAG["GKV_minus_LePhare"] = dict(n=int(okg.sum()), median=float(np.median(off[okg])) if okg.any() else None,
                                 nmad=float(1.4826 * np.median(np.abs(off[okg] - np.median(off[okg])))) if okg.any() else None)
P(f"   S3 lenses that are G3C non-central group members: {DIAG['S3_g3c_nonCentral_frac']:.3f}; "
  f"GKV - LePhare(+0.15) in G09: median {DIAG['GKV_minus_LePhare']['median']:+.3f} dex, NMAD {DIAG['GKV_minus_LePhare']['nmad']:.3f} (n {DIAG['GKV_minus_LePhare']['n']})")
P(f"   S3: median z {np.median(z_g[idxS3]):.3f}, median lM70 {np.median(lM70[idxS3]):.2f}")
DIAG["S3_median_z"] = float(np.median(z_g[idxS3])); DIAG["S3_median_lM70"] = float(np.median(lM70[idxS3]))
RES["diagnostics"] = DIAG

# ============================================================================ 12. outputs
ncheck = len(CHK); npass = sum(CHK.values())
P(f"\n  peak RSS phase A {RES.get('phaseA_peak_RSS_GB', float('nan')):.2f} GB, phase B {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB "
  f"(separate processes); phase B runtime {time.time() - T0:.0f} s")
P(f"P2_SPEC_ISOLATED_LENSING COMPLETE: {npass}/{ncheck} checks PASS.")
RES["checks"] = CHK


def _js(o):
    if isinstance(o, dict): return {str(k): _js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_js(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.ndarray): return _js(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return None
    return o


json.dump(_js(RES), open(os.path.join(HERE, f"p2_spec_isolated_lensing_results{SFX}.json"), "w"), indent=1)
open(os.path.join(HERE, f"p2_spec_isolated_lensing{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == ncheck else 1)
