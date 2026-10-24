"""X13 §2 (criteria c4e5a5a064): new KiDS columns and the frozen class edges (catalogue only, no shear statistic).
Streams the KiDS-1000 SOM-gold FITS with X7's reader, filter and order (finite RA, DEC, e1, e2; weight > 0; Z_B <= 1.2; stable
sort by the 0.2 deg cell; reader copied from X11's x11_extract_extra.py, sha256 ff3fc8c0..., itself x7_extract.py L22-L63) and
writes psfD = PSF_Q11*PSF_Q22 - PSF_Q12^2, snr = model_SNratio, frad = FLUX_RADIUS into the scratch cache, then computes the
edges of criteria §2 with X11's exact weighted-quantile algorithm: PSF-size and SNR halves inside each of X11's size
quartiles, circularised-size (r_ab = size sqrt((1-|e|)/(1+|e|))) quartiles, FLUX_RADIUS median.
Needs X11's step-0 products in the cache (size.npy, x11_edges.json).
Usage: x13_extract.py <cache dir> [--mutate]   (--mutate: the reorder is skipped, into <cache>_x13mut; X1 must FAIL)
Single thread, no network."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":                       # X7 A3 / X11 A1: macOS medium zone keeps freed temporaries resident
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import fcntl, json, hashlib, resource, time, gc, numpy as np
from astropy.io import fits
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
F = os.path.join(REPO, "..", "_external_data", "kids_lensing_zsplit", "KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; CACHE = ARGS[0]
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = CACHE.rstrip("/") + "_x13mut" if MUT else CACHE; os.makedirs(OUT, exist_ok=True)
OUTF = open(os.path.join(HERE, f"x13_extract{TAG}.out"), "w")
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
# ---------------------------------------------------------------- reader (X11 x11_extract_extra.py L28-L63, same filter and order)
CELL = 0.2; NRA = int(round(360/CELL))
h = fits.open(F, memmap=True); hd = h[1].header; N = hd["NAXIS2"]; ROW = hd["NAXIS1"]; LOC = h.fileinfo(1)["datLoc"]
_d = h[1].columns.dtype
dt = np.dtype({"names": list(_d.names), "formats": [_d.fields[n][0].newbyteorder(">") for n in _d.names],
               "offsets": [_d.fields[n][1] for n in _d.names], "itemsize": _d.itemsize})
FILT = {"ra": "RAJ2000", "dec": "DECJ2000", "e1": "e1", "e2": "e2", "w": "weight", "zb": "Z_B"}
NEW = {"q11": "PSF_Q11", "q22": "PSF_Q22", "q12": "PSF_Q12", "snr": "model_SNratio", "frad": "FLUX_RADIUS"}
assert dt.itemsize == ROW, (dt.itemsize, ROW)
_r5 = h[1].data[:5]
_chk = {k: np.asarray(_r5[v], float) for k, v in {**FILT, **NEW}.items()}; del _r5; h.close()
step = 40000; OUTC = ("e1", "psfD", "snr", "frad")
tmp = {k: open(os.path.join(OUT, f"_x13tmp_{k}.bin"), "wb") for k in OUTC + ("cell",)}; nkeep = 0
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
        q11 = rec["PSF_Q11"][ok].astype(np.float64); q22 = rec["PSF_Q22"][ok].astype(np.float64); q12 = rec["PSF_Q12"][ok].astype(np.float64)
        tmp["psfD"].write((q11*q22 - q12**2).astype(np.float32).tobytes())
        tmp["snr"].write(rec["model_SNratio"][ok].astype(np.float32).tobytes())
        tmp["frad"].write(rec["FLUX_RADIUS"][ok].astype(np.float32).tobytes())
        nkeep += int(ok.sum())
        if (i//step) % 100 == 0: say(f"  {i+n:,}/{N:,} kept {nkeep:,} [{time.time()-T0:.0f} s]")
for f in tmp.values(): f.close()
cell = np.fromfile(os.path.join(OUT, "_x13tmp_cell.bin"), np.int32)
order = np.arange(len(cell), dtype=np.int32) if MUT else np.argsort(cell, kind="stable").astype(np.int32)
del cell; gc.collect()
for k in OUTC:
    a = np.fromfile(os.path.join(OUT, f"_x13tmp_{k}.bin"), np.float32); np.save(os.path.join(OUT, f"{k}{'_x13chk' if k == 'e1' else ''}.npy"), a[order]); del a; gc.collect()
    os.remove(os.path.join(OUT, f"_x13tmp_{k}.bin"))
os.remove(os.path.join(OUT, "_x13tmp_cell.bin")); del order; gc.collect()
say(f"rows {N:,} kept {nkeep:,}; wrote psfD, snr, frad [{time.time()-T0:.0f} s]")
# ---------------------------------------------------------------- X1: the re-extracted e1, reordered, equals the cache's e1.npy byte for byte
ncache = int(np.load(os.path.join(CACHE, "e1.npy"), mmap_mode="r").shape[0])
same = sha_file(os.path.join(OUT, "e1_x13chk.npy")) == sha_file(os.path.join(CACHE, "e1.npy"))
os.remove(os.path.join(OUT, "e1_x13chk.npy"))
check("X1", same and nkeep == ncache, f"re-extracted e1 after reorder byte-identical to the cache's e1.npy: {same}; kept {nkeep:,} vs cache {ncache:,}", "identical; equal counts")
RES.update(rows=N, kept=nkeep)
if MUT:                                                              # the control only needs X1; the edges of a disordered cache are meaningless
    for k in ("psfD", "snr", "frad"): os.remove(os.path.join(OUT, f"{k}.npy"))
    pk = rss(); check("X3", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB"); RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk)
    npass = sum(ok for _, ok in CHECKS); say(f"X13_EXTRACT (MUTATE) COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
    json.dump(RES, open(os.path.join(HERE, f"x13_extract_results{TAG}.json"), "w"), indent=1); sys.exit(0 if npass == len(CHECKS) else 1)
# ---------------------------------------------------------------- edges (catalogue only; X11's exact weighted quantile, chunked)
w = np.load(os.path.join(CACHE, "w.npy"))
CH = 1_000_000
def chunks(n): return [(a, min(n, a + CH)) for a in range(0, n, CH)]
def wquant(x, valid, qs):
    """X11 x11_extract_extra.wquant (weights w): the smallest value v with cumulative weight (ascending) >= q * total.
    Pass 1: 4096-bin weighted histogram over the valid range; pass 2: exact sort inside the crossing bin."""
    lo = min(float(x[a:b][valid[a:b]].min()) for a, b in chunks(len(x)) if valid[a:b].any())
    hi = max(float(x[a:b][valid[a:b]].max()) for a, b in chunks(len(x)) if valid[a:b].any()); nb = 4096
    def idx(a, b): return np.clip(np.floor((x[a:b].astype(np.float64) - lo)/max(hi - lo, 1e-300)*nb), 0, nb - 1).astype(np.int64)
    hist = np.zeros(nb)
    for a, b in chunks(len(x)):
        v = valid[a:b]; hist += np.bincount(idx(a, b)[v], w[a:b][v].astype(np.float64), nb)
    cum = np.cumsum(hist); tot = cum[-1]; out = []
    for q in qs:
        bq = int(np.searchsorted(cum, q*tot, side="left")); before = cum[bq - 1] if bq > 0 else 0.0
        xs, ws = [], []
        for a, b in chunks(len(x)):
            s = valid[a:b] & (idx(a, b) == bq); xs.append(x[a:b][s].astype(np.float64)); ws.append(w[a:b][s].astype(np.float64))
        xs = np.concatenate(xs); ws = np.concatenate(ws); o = np.argsort(xs, kind="stable"); cw = before + np.cumsum(ws[o])
        out.append(float(xs[o][min(int(np.searchsorted(cw, q*tot, side="left")), len(xs) - 1)]))
    return out
def fracs(x, valid, edges):
    wb = np.zeros(len(edges) + 1); e = np.asarray(edges, np.float64)
    for a, b in chunks(len(x)):
        v = valid[a:b]; wb += np.bincount(np.searchsorted(e, x[a:b][v].astype(np.float64), side="right"), w[a:b][v].astype(np.float64), len(e) + 1)
    return (wb/wb.sum()).tolist()
E11 = json.load(open(os.path.join(CACHE, "x11_edges.json")))["edges"]; S4 = np.asarray(E11["size4"], np.float64)
size = np.load(os.path.join(CACHE, "size.npy")); vs = np.isfinite(size) & (size > 0)
sq = np.full(len(size), -1, np.int8)
for a, b in chunks(len(size)): sq[a:b] = np.where(vs[a:b], np.searchsorted(S4, size[a:b].astype(np.float64), side="right"), -1)
EDG = {"size4_x11": S4.tolist(), "size2_x11": [float(S4[1])]}; FR = {}; NINV = {}
for k, valid_fn in (("psfD", lambda x: np.isfinite(x) & (x > 0)), ("snr", lambda x: np.isfinite(x) & (x > 0))):
    x = np.load(os.path.join(OUT, f"{k}.npy")); v = valid_fn(x); NINV[k] = int((~v).sum()); e_ = []; fr_ = []
    for q in range(4):
        vq = v & (sq == q); eq = wquant(x, vq, [0.5])[0]; e_.append(eq); fr_.append(fracs(x, vq, [eq]))
    nm = "psf2q" if k == "psfD" else "snr2q"; EDG[nm] = e_; FR[nm] = fr_
    say(f"  {k}: invalid {NINV[k]:,}; within-size-quartile w-medians {np.round(e_, 5).tolist()}; half weight fractions {np.round(fr_, 4).tolist()}")
    del x, v; gc.collect()
e1 = np.load(os.path.join(CACHE, "e1.npy")); e2 = np.load(os.path.join(CACHE, "e2.npy")); rab = np.empty(len(size), np.float32)
for a, b in chunks(len(size)):
    em = np.sqrt(e1[a:b].astype(np.float64)**2 + e2[a:b].astype(np.float64)**2)
    rab[a:b] = np.where(em < 1, size[a:b].astype(np.float64)*np.sqrt(np.clip((1 - em)/(1 + em), 0, None)), np.nan)
del e1, e2; gc.collect()
vc = vs & np.isfinite(rab) & (rab > 0); NINV["rab"] = int((~vc).sum())
EDG["circ4"] = wquant(rab, vc, [0.25, 0.5, 0.75]); EDG["circ2"] = [EDG["circ4"][1]]; FR["circ4"] = fracs(rab, vc, EDG["circ4"]); FR["circ2"] = fracs(rab, vc, EDG["circ2"])
say(f"  r_ab (circularised size, px): invalid {NINV['rab']:,}; quartile edges {np.round(EDG['circ4'], 5).tolist()} (weight fractions {np.round(FR['circ4'], 4).tolist()})")
del rab, vc; gc.collect()
x = np.load(os.path.join(OUT, "frad.npy")); v = np.isfinite(x) & (x > 0); NINV["frad"] = int((~v).sum())
EDG["frad2"] = wquant(x, v, [0.5]); FR["frad2"] = fracs(x, v, EDG["frad2"]); del x, v; gc.collect()
say(f"  FLUX_RADIUS: invalid {NINV['frad']:,}; w-median {EDG['frad2'][0]:.5f} (weight fractions {np.round(FR['frad2'], 4).tolist()})")
EDG["band_edges"] = S4.tolist(); EDG["cband_edge"] = EDG["circ2"]; EDG["band_halfwidth_ln"] = 0.05
# band populations (weight fraction of valid size rows inside each +-0.05 ln band), catalogue-wide
bw = np.zeros(3); tw = 0.0
for a, b in chunks(len(size)):
    vv = vs[a:b]; ls = np.log(np.where(vv, size[a:b].astype(np.float64), 1.0)); ww_ = w[a:b].astype(np.float64)
    for j in range(3): bw[j] += ww_[vv & (np.abs(ls - np.log(S4[j])) < 0.05)].sum()
    tw += ww_[vv].sum()
RES["band_weight_fraction"] = (bw/tw).tolist(); say(f"  size bands (+-0.05 in ln) at the X11 edges: weight fractions {np.round(bw/tw, 5).tolist()}")
del size, sq, vs; gc.collect()
json.dump(dict(edges=EDG, invalid=NINV), open(os.path.join(OUT, "x13_edges.json"), "w"), indent=1)
RES.update(edges=EDG, weight_fractions=FR, invalid=NINV)
# ---------------------------------------------------------------- X2 edges sane, halves balanced; X3 RSS
inc = all(np.all(np.isfinite(EDG[k])) for k in ("psf2q", "snr2q", "circ4", "frad2")) and np.all(np.diff(EDG["circ4"]) > 0)
hb = [f_[0] for k in ("psf2q", "snr2q") for f_ in FR[k]]; mn = min(min(FR["circ4"]), min(FR["frad2"]))
check("X2", inc and min(hb) >= 0.40 and max(hb) <= 0.60 and mn >= 0.10, f"edges finite, circ4 increasing {inc}; within-quartile lower-half weight fractions {np.round(hb, 4).tolist()}; smallest circ/frad class {mn:.4f}",
      "True; each in [0.40, 0.60]; >= 0.10")
pk = rss(); check("X3", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk)
npass = sum(ok for _, ok in CHECKS); say(f"X13_EXTRACT COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x13_extract_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
