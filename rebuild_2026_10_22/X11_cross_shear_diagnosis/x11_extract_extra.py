"""X11 §2 (criteria 9a105431c9): extra KiDS columns and the frozen class edges (catalogue only, no shear statistic).
Streams the KiDS-1000 SOM-gold FITS with X7's reader, filter and order (finite RA, DEC, e1, e2; weight > 0; Z_B <= 1.2; stable
sort by the 0.2 deg sky cell; code as x7_extract.py) and writes mag (MAG_AUTO), size (bias_corrected_scalelength_pixels),
psfT (PSF_Q11 + PSF_Q22), nbr (neighbour_distance) into the scratch cache, then computes the class edges of criteria §2:
w-quantiles (mag, size, psfT, psfE, nbr), tile-seeing groups, the Delta z_ls edge, and the MAG_AUTO count slope.
Usage: x11_extract_extra.py <x11 cache dir> [--mutate]   (--mutate: the reorder is skipped, into <cache>_x11mut; X1 must FAIL)
Single thread, no network."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":                       # A1 (X7's A3 fix): macOS medium zone keeps freed 1-8 MB temporaries resident
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
import fcntl, json, hashlib, resource, time, gc, numpy as np
from astropy.io import fits
from scipy.interpolate import PchipInterpolator
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
F = os.path.join(REPO, "..", "_external_data", "kids_lensing_zsplit", "KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; CACHE = ARGS[0]
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = CACHE.rstrip("/") + "_x11mut" if MUT else CACHE; os.makedirs(OUT, exist_ok=True)
OUTF = open(os.path.join(HERE, f"x11_extract_extra{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
def sha_file(p):
    hh = hashlib.sha256()
    with open(p, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 24), b""): hh.update(blk)
    return hh.hexdigest()
# ---------------------------------------------------------------- reader (x7_extract.py L22-L63, same filter and order)
CELL = 0.2; NRA = int(round(360/CELL))
h = fits.open(F, memmap=True); hd = h[1].header; N = hd["NAXIS2"]; ROW = hd["NAXIS1"]; LOC = h.fileinfo(1)["datLoc"]
_d = h[1].columns.dtype
dt = np.dtype({"names": list(_d.names), "formats": [_d.fields[n][0].newbyteorder(">") for n in _d.names],
               "offsets": [_d.fields[n][1] for n in _d.names], "itemsize": _d.itemsize})
FILT = {"ra": "RAJ2000", "dec": "DECJ2000", "e1": "e1", "e2": "e2", "w": "weight", "zb": "Z_B"}
NEW = {"mag": "MAG_AUTO", "size": "bias_corrected_scalelength_pixels", "q11": "PSF_Q11", "q22": "PSF_Q22", "nbr": "neighbour_distance"}
assert dt.itemsize == ROW, (dt.itemsize, ROW)
_r5 = h[1].data[:5]
_chk = {k: np.asarray(_r5[v], float) for k, v in {**FILT, **NEW}.items()}; del _r5; h.close()
step = 40000; OUTC = ("e1", "mag", "size", "psfT", "nbr")
tmp = {k: open(os.path.join(OUT, f"_x11tmp_{k}.bin"), "wb") for k in OUTC + ("cell",)}; nkeep = 0
with open(F, "rb", buffering=0) as fh:
    try: fcntl.fcntl(fh.fileno(), getattr(fcntl, "F_NOCACHE", 48), 1)
    except OSError: pass
    fh.seek(LOC); buf = bytearray(step*ROW)
    for i in range(0, N, step):
        n = min(step, N - i); mv = memoryview(buf)[:n*ROW]; got = fh.readinto(mv); assert got == n*ROW
        rec = np.frombuffer(mv, dtype=dt, count=n)
        if i == 0:
            assert all(np.allclose(rec[v][:5].astype(float), _chk[k], equal_nan=True) for k, v in {**FILT, **NEW}.items()), "byte order"
        c = {k: rec[v].astype(np.float64) for k, v in FILT.items()}
        ok = np.isfinite(c["ra"]) & np.isfinite(c["dec"]) & np.isfinite(c["e1"]) & np.isfinite(c["e2"]) & (c["w"] > 0) & (c["zb"] <= 1.2)
        cell = (np.floor((c["dec"][ok] + 90)/CELL).astype(np.int64)*NRA + np.floor((c["ra"][ok] % 360)/CELL).astype(np.int64)).astype(np.int32)
        tmp["cell"].write(cell.tobytes()); tmp["e1"].write(c["e1"][ok].astype(np.float32).tobytes())
        tmp["mag"].write(rec["MAG_AUTO"][ok].astype(np.float32).tobytes())
        tmp["size"].write(rec["bias_corrected_scalelength_pixels"][ok].astype(np.float32).tobytes())
        tmp["psfT"].write((rec["PSF_Q11"][ok].astype(np.float64) + rec["PSF_Q22"][ok].astype(np.float64)).astype(np.float32).tobytes())
        tmp["nbr"].write(rec["neighbour_distance"][ok].astype(np.float32).tobytes())
        nkeep += int(ok.sum())
        if (i//step) % 100 == 0: say(f"  {i+n:,}/{N:,} kept {nkeep:,} [{time.time()-T0:.0f} s]")
for f in tmp.values(): f.close()
cell = np.fromfile(os.path.join(OUT, "_x11tmp_cell.bin"), np.int32)
order = np.arange(len(cell), dtype=np.int32) if MUT else np.argsort(cell, kind="stable").astype(np.int32)
del cell; gc.collect()
for k in OUTC:
    a = np.fromfile(os.path.join(OUT, f"_x11tmp_{k}.bin"), np.float32); np.save(os.path.join(OUT, f"{k}{'_x11chk' if k == 'e1' else ''}.npy"), a[order]); del a; gc.collect()
    os.remove(os.path.join(OUT, f"_x11tmp_{k}.bin"))
os.remove(os.path.join(OUT, "_x11tmp_cell.bin")); del order; gc.collect()
say(f"rows {N:,} kept {nkeep:,}; wrote mag, size, psfT, nbr [{time.time()-T0:.0f} s]")
# ---------------------------------------------------------------- X1: the re-extracted e1, reordered, equals the cache's e1.npy byte for byte
ncache = int(np.load(os.path.join(CACHE, "e1.npy"), mmap_mode="r").shape[0])
same = sha_file(os.path.join(OUT, "e1_x11chk.npy")) == sha_file(os.path.join(CACHE, "e1.npy"))
os.remove(os.path.join(OUT, "e1_x11chk.npy"))
check("X1", same and nkeep == ncache, f"re-extracted e1 after reorder byte-identical to the cache's e1.npy: {same}; kept {nkeep:,} vs cache {ncache:,}", "identical; equal counts")
RES.update(rows=N, kept=nkeep)
# ---------------------------------------------------------------- class edges (catalogue only; chunked, exact)
def col(name, d=OUT): return np.load(os.path.join(d, f"{name}.npy"))
w = np.load(os.path.join(CACHE, "w.npy"))                                         # float32; converted per chunk
CH = 1_000_000
def chunks(n): return [(a, min(n, a + CH)) for a in range(0, n, CH)]
def wquant(x, valid, qs, wt=None):
    """exact weighted quantile: the smallest value v with cumulative weight (ascending order) >= q * total.
    Pass 1: 4096-bin weighted histogram over the valid range; pass 2: exact sort inside the crossing bin. wt None -> w."""
    lo = min(float(x[a:b][valid[a:b]].min()) for a, b in chunks(len(x)) if valid[a:b].any())
    hi = max(float(x[a:b][valid[a:b]].max()) for a, b in chunks(len(x)) if valid[a:b].any()); nb = 4096
    def idx(a, b): return np.clip(np.floor((x[a:b].astype(np.float64) - lo)/max(hi - lo, 1e-300)*nb), 0, nb - 1).astype(np.int64)
    def wts(a, b): return np.ones(b - a) if wt == "unit" else w[a:b].astype(np.float64)
    hist = np.zeros(nb)
    for a, b in chunks(len(x)):
        v = valid[a:b]; hist += np.bincount(idx(a, b)[v], wts(a, b)[v], nb)
    cum = np.cumsum(hist); tot = cum[-1]; out = []
    for q in qs:
        bq = int(np.searchsorted(cum, q*tot, side="left")); before = cum[bq - 1] if bq > 0 else 0.0
        xs, ws = [], []
        for a, b in chunks(len(x)):
            s = valid[a:b] & (idx(a, b) == bq); xs.append(x[a:b][s].astype(np.float64)); ws.append(wts(a, b)[s])
        xs = np.concatenate(xs); ws = np.concatenate(ws); o = np.argsort(xs, kind="stable"); cw = before + np.cumsum(ws[o])
        out.append(float(xs[o][min(int(np.searchsorted(cw, q*tot, side="left")), len(xs) - 1)]))
    return out
def fracs(x, valid, edges):
    wb = np.zeros(len(edges) + 1); e = np.asarray(edges, np.float64)
    for a, b in chunks(len(x)):
        v = valid[a:b]; wb += np.bincount(np.searchsorted(e, x[a:b][v].astype(np.float64), side="right"), w[a:b][v].astype(np.float64), len(e) + 1)
    return (wb/wb.sum()).tolist()
VALID = {"mag": lambda x: np.isfinite(x) & (x > 10) & (x < 35), "size": lambda x: np.isfinite(x) & (x > 0),
         "psfT": lambda x: np.isfinite(x) & (x > 0), "psfE": lambda x: np.isfinite(x), "nbr": lambda x: np.isfinite(x)}
EDG = {}; FR = {}; NINV = {}
for k in ("mag", "size", "psfT", "psfE", "nbr"):
    if k == "psfE":
        x = np.load(os.path.join(CACHE, "psf1.npy")); x2 = np.load(os.path.join(CACHE, "psf2.npy"))
        for a, b in chunks(len(x)): x[a:b] = np.sqrt(x[a:b].astype(np.float64)**2 + x2[a:b].astype(np.float64)**2)
        del x2; gc.collect()
    else:
        x = col(k)
    v = VALID[k](x); NINV[k] = int((~v).sum())
    if k == "nbr":
        e = wquant(x, v, [0.5]); EDG["nbr2"] = e; FR["nbr2"] = fracs(x, v, e)
    else:
        e = wquant(x, v, [0.25, 0.5, 0.75]); EDG[f"{k}4"] = e; FR[f"{k}4"] = fracs(x, v, e)
        if k in ("mag", "size"): EDG[f"{k}2"] = [e[1]]; FR[f"{k}2"] = fracs(x, v, [e[1]])
    if k == "psfT":
        tile = np.load(os.path.join(CACHE, "tile.npy")); NT = int(tile.max()) + 1; sw = np.zeros(NT); swx = np.zeros(NT)
        for a, b in chunks(len(x)):
            vv = v[a:b]; ww_ = w[a:b][vv].astype(np.float64); sw += np.bincount(tile[a:b][vv], ww_, NT); swx += np.bincount(tile[a:b][vv], ww_*x[a:b][vv], NT)
        tmean = np.where(sw > 0, swx/np.where(sw > 0, sw, 1), np.nan); o = np.argsort(np.where(np.isfinite(tmean), tmean, np.inf), kind="stable")
        cexcl = np.cumsum(sw[o]) - sw[o]; mid = (cexcl + 0.5*sw[o])/sw.sum()
        tcls = np.empty(NT, np.int16); tcls[o] = np.clip(np.floor(3*mid), 0, 2).astype(np.int16)
        np.save(os.path.join(OUT, "tilecls.npy"), tcls)
        FR["tile3"] = (np.array([sw[tcls == c].sum() for c in range(3)])/sw.sum()).tolist()
        RES["tile3_mean_psfT_upper_edges"] = [float(np.nanmax(tmean[tcls == c])) for c in range(2)]; RES["tile3_ntiles"] = np.bincount(tcls, minlength=3).tolist()
        del tile, sw, swx, tmean, o, cexcl, mid; gc.collect()
    say(f"  {k}: invalid {NINV[k]:,}; " + "; ".join(f"{kk} edges {np.round(EDG[kk], 5).tolist()} (weight fractions {np.round(FR[kk], 4).tolist()})" for kk in EDG if kk[:-1] == k))
    del x, v; gc.collect()
say(f"  tile3: tiles per class {RES['tile3_ntiles']}; class upper mean-psfT {np.round(RES['tile3_mean_psfT_upper_edges'], 4).tolist()}; weight fractions {np.round(FR['tile3'], 4).tolist()}")
# Delta z_ls edge: 326 clusters (z from X7's committed npz), w-weighted Z_B histogram, pair weight w * Sigma_crit^-2 (h 0.672)
G = 6.674e-11; C = 2.998e8; MPC = 3.0857e22
zb_ = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]          # verbatim F1 / X7 distances
DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); DMb = np.sqrt(7.942**3/(0.295*DHb))
PCH = PchipInterpolator(np.r_[0, 0.295, zb_], np.r_[0, DMb, DMr]); HRD = 101.54
def DM(z, h): return PCH(np.minimum(np.asarray(z, float), 2.33))*HRD/h
zb = np.load(os.path.join(CACHE, "zb.npy")); EZ = np.arange(-0.005, 1.2051, 0.01); hz = np.zeros(len(EZ) - 1)
for a, b in chunks(len(zb)): hz += np.histogram(zb[a:b].astype(np.float64), EZ, weights=w[a:b].astype(np.float64))[0]
zc = 0.5*(EZ[1:] + EZ[:-1]); del zb; gc.collect()
X7N = np.load(os.path.join(REB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); zl_all = np.asarray(X7N["z"], float)
dz_all, wt_all = [], []
for zl in zl_all:
    s = (zc > zl + 0.2) & (zc <= 1.2); DlM = float(DM(zl, 0.672)); Dl = DlM/(1 + zl); DMs = DM(zc[s], 0.672)
    isc = np.clip(4*np.pi*G/C**2*(Dl*MPC)*((DMs - DlM)/(1 + zc[s]))/(DMs/(1 + zc[s])), 0, None); pw = hz[s]*isc**2
    if pw.sum() > 0: dz_all.append(zc[s] - zl); wt_all.append(pw/pw.sum())
dz_all = np.concatenate(dz_all); wt_all = np.concatenate(wt_all); o = np.argsort(dz_all, kind="stable"); cw = np.cumsum(wt_all[o])
EDG["dzls2"] = [float(dz_all[o][np.searchsorted(cw, 0.5*cw[-1])])]
say(f"  dzls2: edge Z_B - z_l = {EDG['dzls2'][0]:.4f} (pooled over {len(zl_all)} clusters, pair weight w Sigma_crit^-2, h 0.672)")
# MAG_AUTO count slope (E2 only)
m = col("mag"); vm = VALID["mag"](m); pc = np.array(wquant(m, vm, [0.10, 0.25, 0.40, 0.50, 0.60, 0.75], wt="unit"))
EM = np.arange(10, 35.0001, 0.1); cnt = np.zeros(len(EM) - 1)
for a, b in chunks(len(m)): cnt += np.histogram(m[a:b][vm[a:b]].astype(np.float64), EM)[0]
mc = 0.5*(EM[1:] + EM[:-1]); del m, vm; gc.collect()
SL = {}
for lab, (a, b) in (("central", (pc[1], pc[4])), ("bracket_lo", (pc[0], pc[3])), ("bracket_hi", (pc[2], pc[5]))):
    s_ = (mc >= a) & (mc <= b) & (cnt > 0); sl = float(np.polyfit(mc[s_], np.log10(cnt[s_]), 1)[0]); SL[lab] = dict(range=[float(a), float(b)], s=sl, alpha=2.5*sl)
say("  MAG_AUTO count slope: " + "; ".join(f"{k} [{v['range'][0]:.2f}, {v['range'][1]:.2f}] s {v['s']:.4f} alpha {v['alpha']:.3f}" for k, v in SL.items()))
RES.update(edges=EDG, weight_fractions=FR, invalid=NINV, count_slope=SL, mag_percentiles=dict(zip(["p10", "p25", "p40", "p50", "p60", "p75"], pc.tolist())))
json.dump(dict(edges=EDG, count_slope=SL, invalid=NINV), open(os.path.join(OUT, "x11_edges.json"), "w"), indent=1)
# ---------------------------------------------------------------- X2 edges sane, classes balanced; X3 RSS
inc = all(np.all(np.isfinite(e)) and np.all(np.diff(e) > 0) for e in EDG.values())
minfr = min(min(v) for v in FR.values())
check("X2", inc and minfr >= 0.10, f"edges finite and strictly increasing {inc}; smallest class weight fraction {minfr:.4f}", "True; >= 0.10")
pk = rss(); check("X3", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk)
npass = sum(ok for _, ok in CHECKS); say(f"X11_EXTRACT_EXTRA COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x11_extract_extra_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
