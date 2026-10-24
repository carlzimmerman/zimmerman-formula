"""X13 §4 (criteria c4e5a5a064): test (e), the source-size split on an independent lens sample.
Lenses: F2's lens catalogue (real_research/data/lensing_rar/lr_lenses.npz, all 181,477; F2's 50 patches from cfg96_stack.npz).
Estimator: P2's measure() (P2_spec_isolated_lensing/p2_spec_isolated_lensing.py at 1ebfa54245, sha256 8420630a...), COPIED WITH
PROVENANCE: 'native' convention (Z_B > z_l + 0.2, weights w*Sigma_crit^-2, flat Omega_m 0.3085, h 0.679, P2's 15 bins over
0.03-3 Mpc, bins 0-11 measured) and the 'record' (CFG110) convention for check G1 (P2's K0b). Changes, and only these: per-source
classes (ALL; size2 at X11's edge; circ2 at this lane's edge; the +-0.05 ln band at the size2 edge) with sums per class
(WG, WX, WW, W2, NN, and WE = sum ww*|e|); sources loaded per 0.2-deg declination row window instead of per GAMA box;
centres accumulated per patch. Random points: one per lens (default_rng(20261026): all angles, then all separations;
uniform angle, 1-3 deg, the lens's z), kept if its "in"-range ALL count exceeds 0.5 x its lens's (no retry).
Usage: x13_galaxy.py <cache> <work dir> [--mutate]
--mutate: cross shear in place of tangential (G1 must FAIL); lenses of the first 6 declination rows only.
kappa = 1/2 FITTED (not used: no model enters); footing-independent; single thread, no network."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import json, math, time, resource, hashlib
import numpy as np
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; CACHE, WORK = ARGS[0], ARGS[1]
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; os.makedirs(WORK, exist_ok=True)
OUTF = open(os.path.join(HERE, f"x13_galaxy{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
np.seterr(all="ignore")
# ============================================================================ P2 section 0: constants and distances (verbatim)
G_SI, C_SI, MSUN, MPC = 6.674e-11, 2.998e8, 1.989e30, 3.0857e22
KG_PC2 = MSUN / (3.0857e16) ** 2
H0N, OMN = 0.679, 0.3085
CKMS = 2.998e5
EDGES = np.logspace(np.log10(0.03), np.log10(3.0), 16)                          # Mpc, physical native (P2)
RCEN = np.sqrt(EDGES[1:] * EDGES[:-1])
NBM = 12                                                                         # bins 0-11 measured (criteria §4)
ZZ = np.linspace(0.0, 2.0, 20001)
def chi_of(om, h):
    E = np.sqrt(om * (1 + ZZ) ** 3 + 1 - om)
    c = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(ZZ))]) * (CKMS / 100.0) / h
    return lambda z: np.interp(z, ZZ, c)
CHI_N = chi_of(OMN, H0N)
# record (CFG110) conventions (P2 K0b, verbatim)
_zr = np.linspace(0, 1.5, 2048); _Er = np.sqrt(0.3 * (1 + _zr) ** 3 + 0.7)
_chir = np.concatenate([[0], np.cumsum(0.5 * (1 / _Er[1:] + 1 / _Er[:-1]) * np.diff(_zr))]) * (C_SI / (70e3 / MPC)) / MPC
REC_GB = np.logspace(np.log10(1e-15), np.log10(5e-12), 16)
def npy_slices(path, slices, out=None):
    """P2 verbatim: read contiguous slices of a .npy file with plain file reads (no memory map)."""
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
# ============================================================================ sources: per declination-row window
CELL = 0.2; NRA = int(round(360 / CELL))
CA = np.load(os.path.join(CACHE, "cell.npy"))
E11 = json.load(open(os.path.join(CACHE, "x11_edges.json")))["edges"]; E13 = json.load(open(os.path.join(CACHE, "x13_edges.json")))["edges"]
S2E = float(E11["size2"][0]); C2E = float(E13["circ2"][0]); BANDW = 0.05
SRC = {}; UCELL = CSTART = CEND = None; WIN = [None]
NCL = 6                                                      # 0 ALL, 1-2 size2 S/L, 3-4 circ2 S/L, 5 band at the size2 edge
def load_window(r0, r1):
    """sources of declination rows r0..r1 (inclusive): the cache rows of cells [r0*NRA, (r1+1)*NRA)."""
    global UCELL, CSTART, CEND
    if WIN[0] == (r0, r1): return
    a = int(np.searchsorted(CA, np.int32(r0 * NRA), "left")); b = int(np.searchsorted(CA, np.int32((r1 + 1) * NRA), "left"))
    for k in ("ra", "dec", "e1", "e2", "w", "zb", "size"):
        SRC[k] = npy_slices(os.path.join(CACHE, f"{k}.npy"), [(a, b)])
    cs = CA[a:b]; n = b - a
    if n:
        CSTART = np.r_[0, np.flatnonzero(cs[1:] != cs[:-1]) + 1]; UCELL = cs[CSTART].copy(); CEND = np.r_[CSTART[1:], n]
    else:
        CSTART = np.zeros(0, np.int64); UCELL = np.zeros(0, CA.dtype); CEND = np.zeros(0, np.int64)
    SRC["chiN"] = CHI_N(SRC["zb"].astype(float)).astype(np.float32)                 # P2 stores chiN as float32
    size = SRC["size"].astype(np.float64); e1 = SRC["e1"].astype(np.float64); e2 = SRC["e2"].astype(np.float64); em = np.sqrt(e1 ** 2 + e2 ** 2)
    vs = np.isfinite(size) & (size > 0)
    rab = np.where(em < 1, size * np.sqrt(np.clip((1 - em) / (1 + em), 0, None)), np.nan).astype(np.float32).astype(np.float64)
    vc = vs & np.isfinite(rab) & (rab > 0)
    SRC["em"] = np.where(np.isfinite(em), em, 0.0)
    SRC["c_s2"] = np.where(vs, 1 + (np.where(vs, size, 0) >= S2E), -1).astype(np.int8)       # side='right' as X11: equal -> upper
    SRC["c_c2"] = np.where(vc, 3 + (np.where(vc, rab, 0) >= C2E), -1).astype(np.int8)
    SRC["c_b"] = np.where(vs & (np.abs(np.log(np.where(vs, size, 1.0)) - math.log(S2E)) < BANDW), 5, -1).astype(np.int8)
    del SRC["size"]; WIN[0] = (r0, r1)
def ranges_for(ra, de, th_deg):
    """P2 verbatim."""
    d0 = int(np.floor((de - th_deg + 90) / CELL)); d1 = int(np.floor((de + th_deg + 90) / CELL))
    dra = th_deg / max(np.cos(np.radians(min(abs(de) + th_deg, 89.0))), 1e-3)
    los, his = [], []
    for di in range(d0, d1 + 1):
        r0 = int(np.floor(((ra - dra) % 360) / CELL)); n = int(np.ceil(2 * dra / CELL)) + 1
        cells = ((np.arange(r0, r0 + n) % NRA) + di * NRA).astype(UCELL.dtype)
        if len(UCELL) == 0: continue
        pos = np.searchsorted(UCELL, cells); pos = np.minimum(pos, len(UCELL) - 1)
        hit = UCELL[pos] == cells
        los.append(CSTART[pos[hit]]); his.append(CEND[pos[hit]])
    if not los: return np.zeros(0, np.int64), np.zeros(0, np.int64)
    lo = np.concatenate(los); hi = np.concatenate(his); m = hi > lo
    return lo[m], hi[m]
def thmax_of(cz, conv, extra=None):
    if conv == "native":
        Dl = CHI_N(cz) / (1 + cz); return EDGES[NBM] / Dl * 1.02                   # P2 uses 3.0 Mpc; only bins 0-11 are measured here
    chil = extra[:, 1]; return 3.0 * (1 + cz) / chil * 1.0001 * 1.5
def measure(cra, cde, cz, conv, nb, extra=None, maxpairs=100_000):
    """P2's measure() with per-class sums. Returns OUT (n, NCL, 6 [WG, WX, WW, W2, NN, WE], nb) and INV (n, 2 [size2, circ2], nb) (WW of
    sources outside the classes); 'record' accumulates the ALL class only."""
    n = len(cra); OUT = np.zeros((n, NCL, 6, nb)); INV = np.zeros((n, 2, nb))
    if conv == "native":
        chil = CHI_N(cz); Dl = chil / (1 + cz); thmax = EDGES[NBM] / Dl * 1.02
    else:
        chil = extra[:, 1].copy(); Dl = chil / (1 + cz); thmax = 3.0 * (1 + cz) / chil * 1.0001
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
            k = np.searchsorted(EDGES, Rp, "right") - 1
        ok = (k >= 0) & (k < nb)
        idx, cid, zs, x, y, th2, k = idx[ok], cid[ok], zs[ok], x[ok], y[ok], th2[ok], k[ok]
        if conv == "native":
            chis = SRC["chiN"][idx].astype(float)
        else:
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
        vals = (w * isc * et, w * isc * ex, w * isc * isc, (w * isc * et) ** 2, np.ones_like(w), w * isc * isc * SRC["em"][idx])
        nn_ = (j - i) * NCL * nb
        cvs = [np.zeros(len(idx), np.int64)] + ([SRC["c_s2"][idx].astype(np.int64), SRC["c_c2"][idx].astype(np.int64), SRC["c_b"][idx].astype(np.int64)] if conv == "native" else [])
        for cv in cvs:
            m = cv >= 0; key = (cid[m] * NCL + cv[m]) * nb + k[m]
            for q, val in enumerate(vals):
                OUT[i:j, :, q, :] += np.bincount(key, val[m], nn_).reshape(j - i, NCL, nb)
        if conv == "native":
            for vi, cv in enumerate(cvs[1:3]):
                m = cv < 0; INV[i:j, vi] += np.bincount(cid[m] * nb + k[m], (w * isc * isc)[m], (j - i) * nb).reshape(j - i, nb)
        i = j
    if MUT:
        OUT[:, :, [0, 1]] = OUT[:, :, [1, 0]]                                     # MUTATE: cross shear in place of tangential
    return OUT, INV
def measure_rows(cra, cde, cz, conv, nb, extra=None, label="", patch=None, accept=None, PTo=None, PVo=None, NPo=None):
    """measure centres grouped by declination row; each row's window covers the rows its largest angle reaches.
    Without patch: returns the per-centre sums (small samples only). With patch: per row, the "in"-range ALL counts are kept
    per centre, centres with accept(counts, sel) True are added to the per-patch sums PTo/PVo/NPo, and the counts and the
    partition deviation are returned (no per-centre arrays are kept)."""
    n = len(cra); row = np.floor((cde + 90) / CELL).astype(np.int64); th = np.degrees(thmax_of(cz, conv, extra)); t1 = time.time()
    OUT = np.zeros((n, NCL, 6, nb)) if patch is None else None; CNT = np.zeros(n); dev = 0.0
    urows = np.unique(row)
    for ri, r in enumerate(urows):
        sel = np.where(row == r)[0]; kr = int(np.ceil(th[sel].max() / CELL))
        load_window(r - kr, r + kr)
        o, v = measure(cra[sel], cde[sel], cz[sel], conv, nb, None if extra is None else extra[sel])
        if patch is None:
            OUT[sel] = o
        else:
            c_ = o[:, 0, 4, 0:8].sum(1); CNT[sel] = c_
            for c0, vi in ((1, 0), (3, 1)):
                tot = o[:, c0, 2] + o[:, c0 + 1, 2] + v[:, vi]; dev = max(dev, float(np.max(np.abs(tot - o[:, 0, 2]) / np.maximum(o[:, 0, 2], 1e-300))))
            a_ = accept(c_, sel)
            np.add.at(PTo, patch[sel][a_], o[a_]); np.add.at(PVo, patch[sel][a_], v[a_]); np.add.at(NPo, patch[sel][a_], 1.0)
        del o, v
        if (ri + 1) % 20 == 0 or ri + 1 == len(urows): say(f"    {label} rows {ri+1}/{len(urows)} [{time.time()-t1:.0f} s, RSS {rss():.2f} GB]")
    return (OUT if patch is None else (CNT, dev))
# ============================================================================ lenses, patches, randoms
DKB = os.path.join(REPO, "real_research", "data", "lensing_rar")
LN = np.load(os.path.join(DKB, "lr_lenses.npz")); STK = np.load(os.path.join(DKB, "cfg96_stack.npz"))
RES["lenses_sha256"] = sha(os.path.join(DKB, "lr_lenses.npz")); RES["cfg96_stack_sha256"] = sha(os.path.join(DKB, "cfg96_stack.npz"))
lra, lde, lz = LN["ra"].astype(float), LN["dec"].astype(float), LN["z"].astype(float); PATCH = STK["patch"].astype(np.int64); NPATCH = 50
NLALL = len(lra); assert len(PATCH) == NLALL
rng = np.random.default_rng(20261026)
ang = rng.uniform(0, 2 * np.pi, NLALL); sep = rng.uniform(1, 3, NLALL)
rra = (lra + sep * np.cos(ang) / np.cos(np.radians(lde))) % 360; rde = lde + sep * np.sin(ang)
use = np.ones(NLALL, bool)
if MUT:
    lrow = np.floor((lde + 90) / CELL).astype(np.int64); use = np.isin(lrow, np.unique(lrow)[:6])
say(f"lenses {NLALL:,} (z {lz.min():.3f}-{lz.max():.3f}); used {int(use.sum()):,}; patches {len(np.unique(PATCH))}; edges size2 {S2E:.4f} px, circ2 {C2E:.5f} px, band +-{BANDW} in ln")
# ============================================================================ G1: P2's K0b (record convention) on the first 2,000 lenses
PL = np.load(os.path.join(DKB, "cfg110_perlens.npz"))
rk = np.arange(2000)
mr = measure_rows(lra[rk], lde[rk], lz[rk], "record", 15, extra=np.c_[LN["Mgal"][rk].astype(float), LN["chi"][rk].astype(float)], label="G1 record")
WGr, WWr = PL["WG"][rk].sum(0), PL["WW"][rk].sum(0); WGm, WWm = mr[:, 0, 0].sum(0), mr[:, 0, 2].sum(0)
rWW = float(WWm.sum() / WWr.sum())
sig = np.sqrt(mr[:, 0, 3].sum(0)) / WWm; ratio = (WGm / WWm) / (WGr / WWr); good = np.abs(WGm / WWm) / sig > 3
rmed = float(np.median(ratio[good])) if good.any() else float("nan")
check("G1", (0.90 <= rWW <= 1.000001) and (0.95 <= rmed <= 1.05), f"record (CFG110) convention, first 2,000 catalogue lenses: WW ratio {rWW:.7f}; median DeltaSigma ratio {rmed:.6f} over {int(good.sum())} bins",
      "[0.90,1.000001] & [0.95,1.05] (P2 K0b)")
RES["G1"] = dict(WW_ratio=rWW, median_ratio=rmed, nbins=int(good.sum()), per_bin_ratio=ratio.tolist()); del PL, mr
# ============================================================================ pass 1: lenses; pass 2: randoms (acceptance vs the lens count)
li = np.where(use)[0]
PT = {"L": np.zeros((NPATCH, NCL, 6, NBM)), "R": np.zeros((NPATCH, NCL, 6, NBM))}; PV = {"L": np.zeros((NPATCH, 2, NBM)), "R": np.zeros((NPATCH, 2, NBM))}
NP = {"L": np.zeros(NPATCH), "R": np.zeros(NPATCH)}
cL, g2a = measure_rows(lra[li], lde[li], lz[li], "native", NBM, label="lenses", patch=PATCH[li], accept=lambda c_, s_: np.ones(len(s_), bool),
                       PTo=PT["L"], PVo=PV["L"], NPo=NP["L"])
cntL = np.zeros(NLALL); cntL[li] = cL; nzero = int((cL == 0).sum())
cR, g2b = measure_rows(rra[li], rde[li], lz[li], "native", NBM, label="randoms", patch=PATCH[li], accept=lambda c_, s_: c_ > 0.5 * cL[s_],
                       PTo=PT["R"], PVo=PV["R"], NPo=NP["R"])
acc = cR > 0.5 * cL
say(f"lenses measured {len(li):,} (zero 'in' count: {nzero:,}); randoms accepted {int(acc.sum()):,} of {len(li):,} ({acc.mean():.3f})")
RES.update(n_lenses=int(len(li)), n_lens_zero_count=nzero, n_rand_accepted=int(acc.sum()), rand_acceptance=float(acc.mean()))
g2 = max(g2a, g2b)
check("G2", g2 <= 1e-12, f"size2 and circ2 halves + invalid = ALL (WW, every centre and bin): max rel dev {g2:.1e}", "<= 1e-12")
NPZ = os.path.join(WORK, f"x13_galaxy_sums{TAG}.npz")
np.savez(NPZ, PT_L=PT["L"], PT_R=PT["R"], PV_L=PV["L"], PV_R=PV["R"], NP_L=NP["L"], NP_R=NP["R"], edges=EDGES, rcen=RCEN, nbm=NBM,
         classes=np.array(["ALL", "size2_S", "size2_L", "circ2_S", "circ2_L", "band_size2"]), sums=np.array(["WG", "WX", "WW", "W2", "NN", "WE"]))
RES["npz_sha256"] = sha(NPZ); say(f"wrote scratch {os.path.basename(NPZ)} sha256 {RES['npz_sha256'][:16]}...")
pk = rss(); check("G3", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk)
npass = sum(ok for _, ok in CHECKS); say(f"X13_GALAXY COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x13_galaxy_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
