"""X11 §3 (criteria 9a105431c9): the split measurement. X7's measurement loop (F1's 326 clusters, F1's random positions, seed
20261022 and acceptance; X7's estimator) with every per-bin sum also accumulated per source class (x11_common.VARS), the
rotated cross realisations per class (MID bins, X7's draws), the per-cluster tile-straddle fraction and coverage anisotropy,
and the 90-degree position-rotation identity.
Usage: x11_measure.py <x11 cache> <scratch out dir> [--mutate]
--mutate: first 20 clusters, e2 sign flipped (M1 must FAIL). Deterministic, no network, single thread."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import json, hashlib, resource, time, numpy as np
from astropy.io import fits
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
sys.path.insert(0, HERE); import x11_common as XC
T0 = time.time()
MUT = "--mutate" in sys.argv; ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; CACHE, SOUT = ARGS[0], ARGS[1]
TAG = "_MUTATE" if MUT else ""; os.makedirs(SOUT, exist_ok=True)
OUTF = open(os.path.join(HERE, f"x11_measure{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
RES["x11_common_sha256"] = sha(os.path.join(HERE, "x11_common.py"))
NS = XC.init(CACHE); say(f"sources in cache {NS:,}; classes {XC.KTOT} over {len(XC.VARS)} variables: " + " ".join(f"{n}({k})" for n, k in XC.VARS))
RES["edges"] = {k: v.tolist() for k, v in XC.ST["edges"].items()}
# ---------------------------------------------------------------- eRASS1 clusters from the FITS (verbatim X7 / F1 L78-L87)
EF = os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"); E = fits.open(EF)[1].data
CL = []
for r in E:
    ra, de, z, mg, R5 = float(r["RA_XFIT"]), float(r["DEC_XFIT"]), float(r["BEST_Z"]), float(r["MGAS500"]), float(r["R500"])
    inN = 125 <= ra <= 240 and -6 <= de <= 5; inS = (ra >= 325 or ra <= 60) and -37 <= de <= -25
    if (inN or inS) and 0.05 <= z <= 0.5 and np.isfinite(mg) and mg > 0 and np.isfinite(R5) and R5 > 0:
        off = np.degrees(np.arccos(np.clip(np.sin(np.radians(de))*np.sin(np.radians(r["DEC"])) + np.cos(np.radians(de))*np.cos(np.radians(r["DEC"]))*np.cos(np.radians(ra - r["RA"])), -1, 1)))
        CL.append(dict(name=str(r["NAME"]).strip(), ra=ra, dec=de, z=z, Mgas500=mg*1e11, M500=float(r["M500"]), R500=R5/1e3, off_deg=float(off)))
say(f"eRASS1 candidates in KiDS boxes (FITS): {len(CL)}")
# ---------------------------------------------------------------- the measurement loop (X7 / F1: same seed and acceptance)
rng = np.random.default_rng(20261022); MEAS = []; d90 = 0.0; s90max = 0.0; M3 = 0.0
HX = XC.HX; K = XC.KTOT
def m3dev(o):
    """partition check: for every variable and bin, sum of its classes' den + invalid den = ALL den."""
    dev = 0.0
    for key in HX:
        S = o["h"][key]["S"]; inv = o["h"][key]["inv"]; dall = S[2, 0]
        for vi, (nm, k) in enumerate(XC.VARS):
            tot = S[2, XC.OFF[nm]:XC.OFF[nm] + k].sum(0) + inv[vi]
            dev = max(dev, float(np.max(np.abs(tot - dall)/np.maximum(dall, 1e-300))))
    return dev
for i, cl in enumerate(CL):
    if MUT and len(MEAS) >= 20: break
    m = XC.call(cl["ra"], cl["dec"], cl["z"], rot=True, want90=True, geom=True, mut=MUT)
    if m is None or m["n070"] < 200: continue
    for key in HX:
        s0 = m["h"][key]["s0"]; s9 = m["h"][key]["s90"]; d90 = max(d90, float(np.max(np.abs(s9 + s0)))); s90max = max(s90max, float(np.max(np.abs(s0))))
    rnd = []
    for _ in range(10):
        a = rng.uniform(0, 2*np.pi); s = rng.uniform(1, 3)
        rra, rde = (cl["ra"] + s*np.cos(a)/np.cos(np.radians(cl["dec"]))) % 360, cl["dec"] + s*np.sin(a)
        rr = XC.call(rra, rde, cl["z"], rot=True, mut=MUT, min070=0.5*m["n070"])
        if rr is not None and rr["n070"] > 0.5*m["n070"]:
            rnd.append(rr)
        if len(rnd) >= 6: break
    if len(rnd) < 5: continue
    M3 = max(M3, m3dev(m), max(m3dev(x) for x in rnd))
    rec = {k: cl[k] for k in ("name", "ra", "dec", "z", "Mgas500", "M500", "off_deg")}; rec["f_main"] = m["f_main"]; rec["m2"] = m["m2"]; rec["nrand"] = len(rnd)
    for hi, key in enumerate(HX):
        Sc = m["h"][key]["S"]; Sr = np.array([x["h"][key]["S"] for x in rnd])                   # (7, K, 8), (nr, 7, K, 8)
        dt_c = XC.esd(Sc[0], Sc[2]); dx_c = XC.esd(Sc[1], Sc[2]); dt_r = XC.esd(Sr[:, 0], Sr[:, 2]); dx_r = XC.esd(Sr[:, 1], Sr[:, 2])
        rec[key] = dict(D=dt_c - dt_r.mean(0), Dx=dx_c - dx_r.mean(0), E=XC.err(Sc[3], Sc[2]), Ex=XC.err(Sc[4], Sc[2]), den=Sc[2], den_r=Sr[:, 2].mean(0),
                        cnt=Sc[5], cnt_r=Sr[:, 5].mean(0), sisc=Sc[6], DRR=dt_r[:3].mean(0) - dt_r[3:].mean(0), Rx=dx_r.mean(0), Rt=dt_r.mean(0))
        # rotated cross realisations, MID bins: cluster/den_k - mean over randoms (each normalised by its own den_k), as X7
        dc = Sc[2][:, 3:6][:, :, None]; rc = XC.esd(m["rot"][hi], dc)
        rr_ = np.array([XC.esd(x["rot"][hi], x["h"][key]["S"][2][:, 3:6][:, :, None]) for x in rnd])
        rec[key]["rot"] = (rc - rr_.mean(0)).astype(np.float32)                                      # (K, 3, R)
        rec[key]["rotRx"] = rr_.mean(0).astype(np.float32)                                           # random-mean cross, rotated
    MEAS.append(rec); del m, rnd
    if len(MEAS) % 25 == 0: say(f"  measured {len(MEAS)} clusters (of {i+1} tried) [{time.time()-T0:.0f} s, RSS {rss():.2f} GB]")
N = len(MEAS); say(f"clusters used: {N}")
# ---------------------------------------------------------------- M1: the ALL class reproduces the step-0 npz (X7's measurement)
S0N = os.path.join(SOUT, "x7_measure_percluster.npz"); X = np.load(S0N); RES["step0_npz_sha256"] = sha(S0N)
hmap = {"h0672": 1, "h0686": 2}; n = min(N, len(X["name"]))
names = all(MEAS[i]["name"] == str(X["name"][i]) for i in range(n)) and N == len(X["name"])
scale = float(np.max(np.abs(X["D"]))); dmax = 0.0; rmax = 0.0
for i in range(n):
    for key, hj in hmap.items():
        o = MEAS[i][key]
        for a_, b_ in (("D", "D"), ("Dx", "Dx"), ("E", "E"), ("Ex", "Ex"), ("DRR", "DRR"), ("Rmeanx", "Rx"), ("Rmean", "Rt")):
            dmax = max(dmax, float(np.max(np.abs(X[a_][i, hj] - o[b_][0]))))
        for a_, b_ in (("den", "den"), ("den_r", "den_r")):
            rmax = max(rmax, float(np.max(np.abs(X[a_][i, hj] - o[b_][0])/np.maximum(np.abs(X[a_][i, hj]), 1e-300))))
check("M1", names and dmax <= 1e-9*scale and rmax <= 1e-9, f"N {N} vs step-0 {len(X['name'])}, names {names}, ALL class max|dD, dDx, dE, dDRR, dRmean| {dmax:.2e} (scale {scale:.0f}), max rel den {rmax:.1e}",
      "N 326, names equal, <= 1e-9 x max|D|; rel <= 1e-9")
# ---------------------------------------------------------------- M2: ALL-class rotations reproduce the step-0 extras (cross, MID)
XE = np.load(os.path.join(SOUT, "x7_measure_extras.npz")); ROT = XE["rot"]; RES["step0_extras_sha256"] = sha(os.path.join(SOUT, "x7_measure_extras.npz"))
rsc = float(np.max(np.abs(ROT[:n, :, :, 1, 3:6]))); m2d = 0.0
for i in range(n):
    for hi, key in enumerate(HX):
        m2d = max(m2d, float(np.max(np.abs(ROT[i, hi, :, 1, 3:6] - MEAS[i][key]["rot"][0].T))), float(np.max(np.abs(ROT[i, hi, :, 4, 3:6] - MEAS[i][key]["rotRx"][0].T))))
del ROT, XE
check("M2", m2d <= 1e-6*rsc, f"ALL-class rotated cross (and random-mean cross) vs step-0 extras, MID bins: max|diff| {m2d:.2e} (scale {rsc:.1f})", "<= 1e-6 x max")
check("M3", M3 <= 1e-12, f"classes partition every variable: max rel |sum(class den) + invalid den - ALL den| {M3:.1e}", "<= 1e-12")
check("M4", d90 <= 1e-9*s90max, f"90-degree position rotation: max|stack(rotated) + stack| {d90:.2e} (scale {s90max:.3e}; all {N} cluster calls, t and x, both h)", "<= 1e-9 x max")
RES["identity90"] = dict(max_abs=d90, scale=s90max)
# ---------------------------------------------------------------- M5: rotated stacks centre on zero, per h and class (W from the class's own E_x)
m5 = []
for key in HX:
    v = np.zeros((K, XC.R))
    for o in MEAS:
        Ex = o[key]["Ex"][:, 3:6]; W = np.where(Ex < 1e8, 1/Ex**2, 0)
        v += (W[:, :, None]*o[key]["rot"]).sum(1)
    sd = v.std(1, ddof=1); ok_ = sd > 0
    m5 += (np.abs(v.mean(1))[ok_]/(sd[ok_]/np.sqrt(XC.R))).tolist()
check("M5", max(m5) <= 4, f"|mean|/(std/sqrt R) over {len(m5)} (h, class): max {max(m5):.2f}, median {np.median(m5):.2f}", "<= 4")
# ---------------------------------------------------------------- products (scratch: large; compact summary in the JSON)
NPZ = os.path.join(SOUT, f"x11_measure_classes{TAG}.npz")
arr = lambda f: np.array([[o[key][f] for key in HX] for o in MEAS])
np.savez(NPZ, name=np.array([o["name"] for o in MEAS]), ra=np.array([o["ra"] for o in MEAS]), dec=np.array([o["dec"] for o in MEAS]),
         z=np.array([o["z"] for o in MEAS]), Mgas500=np.array([o["Mgas500"] for o in MEAS]), off_deg=np.array([o["off_deg"] for o in MEAS]),
         f_main=np.array([o["f_main"] for o in MEAS]), m2=np.array([o["m2"] for o in MEAS]), nrand=np.array([o["nrand"] for o in MEAS]),
         hx=np.array(HX), varnames=np.array([n_ for n_, _ in XC.VARS]), varsizes=np.array([k_ for _, k_ in XC.VARS]),
         D=arr("D"), Dx=arr("Dx"), E=arr("E"), Ex=arr("Ex"), den=arr("den"), den_r=arr("den_r"), cnt=arr("cnt"), cnt_r=arr("cnt_r"), sisc=arr("sisc"),
         DRR=arr("DRR"), Rx=arr("Rx"), Rt=arr("Rt"), rot=arr("rot"), rotRx=arr("rotRx"))
RES["npz_sha256"] = sha(NPZ); say(f"wrote scratch {os.path.basename(NPZ)} sha256 {RES['npz_sha256'][:16]}...")
RES["f_main_median"] = float(np.nanmedian([o["f_main"] for o in MEAS])); RES["m2_median"] = float(np.nanmedian([o["m2"] for o in MEAS]))
pk = rss(); check("M6", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
RES.update(N=N, R=XC.R, runtime_s=time.time() - T0, peak_rss_GB=pk)
npass = sum(ok for _, ok in CHECKS); say(f"X11_MEASURE COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x11_measure_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
