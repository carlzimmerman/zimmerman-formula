"""X2_cluster_outskirts replay (criteria 40624db7e9): F1's per-cluster KiDS measurement replayed with F1's own estimator,
random loop and seed (code copied verbatim from rebuild_2026_10_22/F1_cluster_cores/f1_cluster_cores.py L19-L117), extended
only to also return the cross shear, each random's ESD (for random-minus-random) and the source moments
m_k = sum w Sigma_crit^-k (k = 2..8 per A1, for the reduced-shear term).
Usage: x2_replay.py <F1 KiDS column cache dir> <dir holding F1's f1_meas.pkl and f1_meas_MUTATE.pkl> [--mutate]
--mutate: first 20 clusters only, e2 sign flipped (R1 must FAIL). Deterministic, no network, single thread."""
import os, sys, json, pickle, hashlib, resource, time, numpy as np
from scipy.interpolate import PchipInterpolator
from astropy.io import fits
_trap = getattr(np, "trapezoid", None) or np.trapz
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; CACHE, F1DIR = ARGS[0], ARGS[1]
TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"x2_replay{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
# ---------------------------------------------------------------- F1 constants, distances, sources (verbatim F1 L19-L44)
G = 6.674e-11; C = 2.998e8; MSUN = 1.989e30; MPC = 3.0857e22; MP = 1.6726e-27; KG_PC2 = MSUN/(3.0857e16)**2
zb_ = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); DMb = np.sqrt(7.942**3/(0.295*DHb))
PCH = PchipInterpolator(np.r_[0, 0.295, zb_], np.r_[0, DMb, DMr]); HRD = 101.54
def DM(z, h): return PCH(np.minimum(np.asarray(z, float), 2.33))*HRD/h
HS = {"h070": 0.70, "h0672": 0.672, "h0686": 0.686}
CELL = 0.2; NRA = int(round(360/CELL))
S = {}
def remap():
    """A2 (memory only): (re)open the KiDS columns as read-only memory maps; dropping the old maps unmaps the touched file pages,
    which macOS counts in ru_maxrss. Values are unchanged (R1/R2 re-verify)."""
    global CELLS
    import gc; S.clear(); CELLS = None; gc.collect()
    S.update({k: np.load(os.path.join(CACHE, f"{k}.npy"), mmap_mode="r") for k in ("ra", "dec", "e1", "e2", "w", "zb", "cell")})
    CELLS = S["cell"]
remap(); NS = len(S["cell"])
ZBMAX = 1.2
say(f"sources in cache {NS:,}")
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:]*EDGES[:-1]); M_BIAS = -0.01
def gather(ra, de, th_deg):
    d0 = int(np.floor((de - th_deg + 90)/CELL)); d1 = int(np.floor((de + th_deg + 90)/CELL))
    dra = th_deg/max(np.cos(np.radians(min(abs(de) + th_deg, 89.0))), 1e-3); idx = []
    for di in range(d0, d1 + 1):
        r0 = int(np.floor(((ra - dra) % 360)/CELL)); n = int(np.ceil(2*dra/CELL)) + 1
        cells = (np.arange(r0, r0 + n) % NRA) + di*NRA
        lo = np.searchsorted(CELLS, cells, "left"); hi = np.searchsorted(CELLS, cells, "right")
        idx += [np.arange(a, b) for a, b in zip(lo, hi) if b > a]
    return np.concatenate(idx) if idx else np.zeros(0, int)
EXACT = []                                                        # R3 material (first 3 clusters)
NMOM = 6                                                          # A1 (pre-result): moments m3..m8, series to 6th order
def esd2(ra, de, zl, hs, want_exact=False):
    """F1 esd() verbatim for the tangential (and, separately, the cross) channel; extra: moments m3..m5 per bin."""
    thmax = max(3.0/(DM(zl, h)/(1 + zl)) for h in hs.values())*1.02
    ii = gather(ra, de, np.degrees(thmax))
    if ii.size < 10: return None
    zs = np.asarray(S["zb"][ii], float); keep = (zs > zl + 0.2) & (zs <= ZBMAX); ii = ii[keep]; zs = zs[keep]
    rs = np.asarray(S["ra"][ii]); ds = np.asarray(S["dec"][ii]); e1 = np.asarray(S["e1"][ii], float); e2 = np.asarray(S["e2"][ii], float); ws = np.asarray(S["w"][ii], float)
    if MUT: e2 = -e2
    dra = (np.radians(rs) - np.radians(ra))*np.cos(np.radians(de)); dra = (dra + np.pi) % (2*np.pi) - np.pi; dde = np.radians(ds) - np.radians(de)
    th = np.hypot(dra, dde); phi = np.arctan2(dde, dra)
    et = -(e1*np.cos(2*phi) - e2*np.sin(2*phi)); ex = -(e1*np.sin(2*phi) + e2*np.cos(2*phi))
    out = {}
    for key, h in hs.items():
        DlM = float(DM(zl, h)); Dl = DlM/(1 + zl); DMs = DM(zs, h)
        isc = np.clip(4*np.pi*G/C**2*(Dl*MPC)*((DMs - DlM)/(1 + zs))/(DMs/(1 + zs)), 0, None)
        k = np.digitize(th*Dl, EDGES) - 1; g = (k >= 0) & (k < 8) & (isc > 0)
        ww = ws*isc**2
        o = {}
        for ch, val0 in (("t", et), ("x", ex)):
            val = val0/np.where(isc > 0, isc, 1)
            o[ch] = (np.bincount(k[g], (ww*val)[g], 8), np.bincount(k[g], ww[g], 8), np.bincount(k[g], (ww**2*val**2)[g], 8), int(g.sum()))
        o["m"] = np.array([np.bincount(k[g], (ww*isc**p)[g], 8) for p in range(1, NMOM + 1)])  # m3 .. m8 (A1)
        if want_exact and key == "h0672":
            St = 300*KG_PC2                                                                    # Sigma_t = 300 Msun/pc^2 in kg/m^2
            EXACT.append((np.bincount(k[g], (ww/(1 - isc*St))[g], 8), o["t"][1], o["m"], St))
        out[key] = o
    return out
def finish(t):
    num, den, var, n = t
    with np.errstate(invalid="ignore", divide="ignore"):
        return num/den/KG_PC2/(1 + M_BIAS), np.sqrt(var)/den/KG_PC2, den, n
# ---------------------------------------------------------------- eRASS1 clusters from the FITS (verbatim F1 L78-L87)
EF = os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"); RES["erass1_fits_sha256"] = sha(EF)
E = fits.open(EF)[1].data
CL = []
for r in E:
    ra, de, z, mg, R5 = float(r["RA_XFIT"]), float(r["DEC_XFIT"]), float(r["BEST_Z"]), float(r["MGAS500"]), float(r["R500"])
    inN = 125 <= ra <= 240 and -6 <= de <= 5; inS = (ra >= 325 or ra <= 60) and -37 <= de <= -25
    if (inN or inS) and 0.05 <= z <= 0.5 and np.isfinite(mg) and mg > 0 and np.isfinite(R5) and R5 > 0:
        off = np.degrees(np.arccos(np.clip(np.sin(np.radians(de))*np.sin(np.radians(r["DEC"])) + np.cos(np.radians(de))*np.cos(np.radians(r["DEC"]))*np.cos(np.radians(ra - r["RA"])), -1, 1)))
        CL.append(dict(name=str(r["NAME"]).strip(), ra=ra, dec=de, z=z, Mgas500=mg*1e11, MgL=float(r["MGAS500_L"])*1e11, MgH=float(r["MGAS500_H"])*1e11,
                       R500=R5/1e3, off_deg=float(off)))
say(f"eRASS1 candidates in KiDS boxes (FITS): {len(CL)}")
# ---------------------------------------------------------------- the measurement loop (F1 L99-L116, same seed and acceptance)
rng = np.random.default_rng(20261022); MEAS = []
for i, cl in enumerate(CL):
    del EXACT[len(MEAS):]                                         # drop R3 material of a rejected cluster
    if i % 15 == 14: remap()                                      # A2: bound the mapped-page footprint
    if MUT and len(MEAS) >= 20: break
    m = esd2(cl["ra"], cl["dec"], cl["z"], HS, want_exact=(len(MEAS) < 3))
    if m is None or m["h070"]["t"][3] < 200: continue
    rnd = []
    for _ in range(10):
        a = rng.uniform(0, 2*np.pi); s = rng.uniform(1, 3)
        rr = esd2((cl["ra"] + s*np.cos(a)/np.cos(np.radians(cl["dec"]))) % 360, cl["dec"] + s*np.sin(a), cl["z"], HS)
        if rr is not None and rr["h070"]["t"][3] > 0.5*m["h070"]["t"][3]: rnd.append(rr)
        if len(rnd) >= 6: break
    if len(rnd) < 5: continue
    rec = dict(cl)
    for key in HS:
        out = {}
        for ch in ("t", "x"):
            d, e, den, n = finish(m[key][ch]); R = [finish(x[key][ch]) for x in rnd]
            Rd = np.nan_to_num(np.array([x[0] for x in R]))
            out[ch] = dict(D=np.nan_to_num(d) - Rd.mean(0), E=np.nan_to_num(e, nan=1e9), den=den, den_r=np.array([x[2] for x in R]).mean(0),
                           DRR=Rd[:3].mean(0) - Rd[3:].mean(0))
        out["m"] = m[key]["m"]; out["nrand"] = len(rnd)
        rec[key] = out
    MEAS.append(rec)
    if len(MEAS) % 50 == 0: say(f"  measured {len(MEAS)} clusters (of {i+1} tried) [{time.time()-T0:.0f} s]")
del EXACT[len(MEAS):]; N = len(MEAS); say(f"clusters used: {N}")
# ---------------------------------------------------------------- R1 / R2: equality with F1's caches
def cmp(pk, ch):
    F = pickle.load(open(pk, "rb")); n = min(len(F), N)
    names = all(F[i]["name"] == MEAS[i]["name"] for i in range(n)) and (len(F) == N or MUT)
    dmax = 0.0; scale = 0.0
    for i in range(n):
        for key in HS:
            for f_, g_ in (("D", "D"), ("E", "E"), ("den", "den"), ("den_r", "den_r")):
                a = np.asarray(F[i][key][f_], float); b = np.asarray(MEAS[i][key][ch][g_], float)
                dmax = max(dmax, float(np.max(np.abs(a - b)/np.maximum(np.abs(a), 1e-300)))) if f_ in ("den", "den_r") else max(dmax, float(np.max(np.abs(a - b))))
                if f_ == "D": scale = max(scale, float(np.max(np.abs(a))))
    return names, len(F), dmax, scale
pk1 = os.path.join(F1DIR, "f1_meas.pkl"); pk2 = os.path.join(F1DIR, "f1_meas_MUTATE.pkl")
RES["f1_meas_sha256"] = sha(pk1); RES["f1_meas_MUTATE_sha256"] = sha(pk2)
say(f"F1 cache sha256 {RES['f1_meas_sha256']} / MUTATE {RES['f1_meas_MUTATE_sha256']}")
nm1, n1, d1, s1 = cmp(pk1, "t"); nm2, n2, d2, s2 = cmp(pk2, "x")
check("R1", nm1 and N == n1 and d1 <= 1e-9*max(s1, 1.0) and RES["f1_meas_sha256"].startswith("961ea4fc"),
      f"N {N} vs F1 {n1}, names {nm1}, max|diff| {d1:.2e} (D scale {s1:.1f})", "N 326, names equal, <= 1e-9 x max|D|, sha 961ea4fc...")
check("R2", nm2 and N == n2 and d2 <= 1e-9*max(s2, 1.0), f"cross: N {N} vs F1 MUTATE {n2}, max|diff| {d2:.2e}", "equal to F1 MUTATE cache")
# ---------------------------------------------------------------- R3: reduced-shear series vs exact source average
r3 = 0.0
for ex_num, den, mom, St in EXACT[:3]:
    ok = den > 0
    exact = ex_num[ok]/den[ok]; series = 1 + sum(St**(p + 1)*mom[p][ok]/den[ok] for p in range(NMOM))
    r3 = max(r3, float(np.max(np.abs(series/exact - 1))))
    RES.setdefault("R3_kappa_eff", []).append((St*mom[0][ok]/den[ok]).tolist())
check("R3", len(EXACT) >= 3 and r3 <= 1e-6, f"max|series/exact - 1| = {r3:.2e} over {min(len(EXACT),3)} clusters", "<= 1e-6 at Sigma_t = 300 Msun/pc^2")
pk = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
check("R4", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
# ---------------------------------------------------------------- products
if not MUT:
    keys = list(HS)
    arr = lambda ch, f: np.array([[o[k][ch][f] for k in keys] for o in MEAS], float)
    out = dict(name=np.array([o["name"] for o in MEAS]), ra=np.array([o["ra"] for o in MEAS]), dec=np.array([o["dec"] for o in MEAS]),
               z=np.array([o["z"] for o in MEAS]), Mgas500=np.array([o["Mgas500"] for o in MEAS]), MgL=np.array([o["MgL"] for o in MEAS]),
               MgH=np.array([o["MgH"] for o in MEAS]), R500=np.array([o["R500"] for o in MEAS]), off_deg=np.array([o["off_deg"] for o in MEAS]),
               hkeys=np.array(keys), D=arr("t", "D"), E=arr("t", "E"), den=arr("t", "den"), den_r=arr("t", "den_r"), DRR=arr("t", "DRR"),
               Dx=arr("x", "D"), Ex=arr("x", "E"), DRRx=arr("x", "DRR"),
               m3to8=np.array([[o[k]["m"] for k in keys] for o in MEAS], float), nrand=np.array([o["h070"]["nrand"] for o in MEAS]))
    NPZ = os.path.join(HERE, "x2_replay_percluster.npz"); np.savez_compressed(NPZ, **out); RES["npz_sha256"] = sha(NPZ)
    say(f"wrote {os.path.basename(NPZ)} sha256 {RES['npz_sha256']}")
RES.update(N=N, runtime_s=time.time() - T0, peak_rss_GB=pk)
npass = sum(ok for _, ok in CHECKS); say(f"X2_REPLAY COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x2_replay_results{TAG}.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
sys.exit(0 if npass == len(CHECKS) else 1)
