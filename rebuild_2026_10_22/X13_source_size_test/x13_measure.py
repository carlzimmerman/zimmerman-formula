"""X13 §3 (criteria c4e5a5a064): the cluster measurement with this lane's source classes.
X11's measurement loop (x11_measure.py at c1cd5455a5, sha256 6716f10a...; F1's 326 clusters, F1's random positions, seed 20261022
and acceptance; X7's estimator) copied with provenance, using x13_common (X11's x11_common with this lane's classes and 7 extra
per-class sums). Dropped from X11's loop (not used here): the 90-degree identity and the per-cluster geometry.
Usage: x13_measure.py <cache> <step-0 scratch (x7 npz, x11 classes npz)> <work dir> [--mutate]
--mutate: first 20 clusters, e2 sign flipped (M1 must FAIL). Deterministic, no network, single thread."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import json, hashlib, resource, time, numpy as np
from astropy.io import fits
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
sys.path.insert(0, HERE); import x13_common as XC
T0 = time.time()
MUT = "--mutate" in sys.argv; ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; CACHE, S0, WORK = ARGS[0], ARGS[1], ARGS[2]
TAG = "_MUTATE" if MUT else ""; os.makedirs(WORK, exist_ok=True)
OUTF = open(os.path.join(HERE, f"x13_measure{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
RES["x13_common_sha256"] = sha(os.path.join(HERE, "x13_common.py"))
NS = XC.init(CACHE); say(f"sources in cache {NS:,}; classes {XC.KTOT} over {len(XC.VARS)} variables: " + " ".join(f"{n}({k})" for n, k in XC.VARS))
RES["edges_x11"] = {k: v.tolist() for k, v in XC.ST["edges"].items()}; RES["edges_x13"] = {k: v.tolist() for k, v in XC.ST["edges13"].items()}
# ---------------------------------------------------------------- eRASS1 clusters from the FITS (verbatim X11 / X7 / F1 L78-L87)
EF = os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"); E = fits.open(EF)[1].data
CL = []
for r in E:
    ra, de, z, mg, R5 = float(r["RA_XFIT"]), float(r["DEC_XFIT"]), float(r["BEST_Z"]), float(r["MGAS500"]), float(r["R500"])
    inN = 125 <= ra <= 240 and -6 <= de <= 5; inS = (ra >= 325 or ra <= 60) and -37 <= de <= -25
    if (inN or inS) and 0.05 <= z <= 0.5 and np.isfinite(mg) and mg > 0 and np.isfinite(R5) and R5 > 0:
        CL.append(dict(name=str(r["NAME"]).strip(), ra=ra, dec=de, z=z, Mgas500=mg*1e11))
say(f"eRASS1 candidates in KiDS boxes (FITS): {len(CL)}")
# ---------------------------------------------------------------- the measurement loop (X11 / X7 / F1: same seed and acceptance)
rng = np.random.default_rng(20261022); MEAS = []; M3 = 0.0
HX = XC.HX; K = XC.KTOT
def m3dev(o):
    """partition check: for every partitioning variable and bin, sum of its classes' den + invalid den = ALL den."""
    dev = 0.0
    for key in HX:
        S = o["h"][key]["S"]; inv = o["h"][key]["inv"]; dall = S[2, 0]
        for vi, (nm, k) in enumerate(XC.VARS):
            if nm not in XC.PARTITION: continue
            tot = S[2, XC.OFF[nm]:XC.OFF[nm] + k].sum(0) + inv[vi]
            dev = max(dev, float(np.max(np.abs(tot - dall)/np.maximum(dall, 1e-300))))
    return dev
for i, cl in enumerate(CL):
    if MUT and len(MEAS) >= 20: break
    m = XC.call(cl["ra"], cl["dec"], cl["z"], rot=True, mut=MUT)
    if m is None or m["n070"] < 200: continue
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
    rec = {k: cl[k] for k in ("name", "ra", "dec", "z", "Mgas500")}; rec["nrand"] = len(rnd)
    for hi, key in enumerate(HX):
        Sc = m["h"][key]["S"]; Sr = np.array([x["h"][key]["S"] for x in rnd])                   # (14, K, 8), (nr, 14, K, 8)
        dt_c = XC.esd(Sc[0], Sc[2]); dx_c = XC.esd(Sc[1], Sc[2]); dt_r = XC.esd(Sr[:, 0], Sr[:, 2]); dx_r = XC.esd(Sr[:, 1], Sr[:, 2])
        rec[key] = dict(D=dt_c - dt_r.mean(0), Dx=dx_c - dx_r.mean(0), E=XC.err(Sc[3], Sc[2]), Ex=XC.err(Sc[4], Sc[2]), den=Sc[2], den_r=Sr[:, 2].mean(0),
                        cnt=Sc[5], cnt_r=Sr[:, 5].mean(0), sisc=Sc[6], Rx=dx_r.mean(0), Rt=dt_r.mean(0), XS=Sc[7:14].copy())
        dc = Sc[2][:, 3:6][:, :, None]; rc = XC.esd(m["rot"][hi], dc)
        rr_ = np.array([XC.esd(x["rot"][hi], x["h"][key]["S"][2][:, 3:6][:, :, None]) for x in rnd])
        rec[key]["rot"] = (rc - rr_.mean(0)).astype(np.float32)                                      # (K, 3, R)
        rec[key]["rotRx"] = rr_.mean(0).astype(np.float32)                                           # random-mean cross, rotated
    MEAS.append(rec); del m, rnd
    if len(MEAS) % 25 == 0: say(f"  measured {len(MEAS)} clusters (of {i+1} tried) [{time.time()-T0:.0f} s, RSS {rss():.2f} GB]")
N = len(MEAS); say(f"clusters used: {N}")
# ---------------------------------------------------------------- M1: the ALL class reproduces the step-0 X7 npz
S0N = os.path.join(S0, "x7_measure_percluster.npz"); X = np.load(S0N); RES["step0_x7_npz_sha256"] = sha(S0N)
hmap = {"h0672": 1, "h0686": 2}; n = min(N, len(X["name"]))
names = all(MEAS[i]["name"] == str(X["name"][i]) for i in range(n)) and N == len(X["name"])
scale = float(np.max(np.abs(X["D"]))); dmax = 0.0; rmax = 0.0
for i in range(n):
    for key, hj in hmap.items():
        o = MEAS[i][key]
        for a_, b_ in (("D", "D"), ("Dx", "Dx"), ("E", "E"), ("Ex", "Ex"), ("Rmeanx", "Rx"), ("Rmean", "Rt")):
            dmax = max(dmax, float(np.max(np.abs(X[a_][i, hj] - o[b_][0]))))
        for a_, b_ in (("den", "den"), ("den_r", "den_r")):
            rmax = max(rmax, float(np.max(np.abs(X[a_][i, hj] - o[b_][0])/np.maximum(np.abs(X[a_][i, hj]), 1e-300))))
check("M1", names and dmax <= 1e-9*scale and rmax <= 1e-9, f"N {N} vs step-0 {len(X['name'])}, names {names}, ALL class max|dD, dDx, dE, dEx, dRmean, dRmeanx| {dmax:.2e} (scale {scale:.0f}), max rel den {rmax:.1e}",
      "N 326, names equal, <= 1e-9 x max|D|; rel <= 1e-9")
del X
# ---------------------------------------------------------------- M2: size2 / size4 classes reproduce the step-0 X11 classes npz
XN = os.path.join(S0, "x11_measure_classes.npz"); XM = np.load(XN); RES["step0_x11_npz_sha256"] = sha(XN)
vn11 = [str(v) for v in XM["varnames"]]; vk11 = [int(k) for k in XM["varsizes"]]; off11 = {}; _o = 0
for v_, k_ in zip(vn11, vk11): off11[v_] = _o; _o += k_
m2a = 0.0; m2r = 0.0; sc2 = 0.0
for v_, k_ in (("size2", 2), ("size4", 4)):
    s11 = slice(off11[v_], off11[v_] + k_); s13 = slice(XC.OFF[v_], XC.OFF[v_] + k_)
    for f_ in ("D", "Dx", "E", "Rt"):
        A11 = XM[f_][:n, :, s11]; A13 = np.array([[MEAS[i][key][f_][s13] for key in HX] for i in range(n)]); sc2 = max(sc2, float(np.max(np.abs(A11))))
        m2a = max(m2a, float(np.max(np.abs(A11 - A13))))
    for f_ in ("den", "den_r"):
        A11 = XM[f_][:n, :, s11]; A13 = np.array([[MEAS[i][key][f_][s13] for key in HX] for i in range(n)])
        m2r = max(m2r, float(np.max(np.abs(A11 - A13)/np.maximum(np.abs(A11), 1e-300))))
names11 = [str(s) for s in XM["name"]][:n] == [MEAS[i]["name"] for i in range(n)]
del XM
check("M2", names11 and m2a <= 1e-9*max(sc2, 1.0) and m2r <= 1e-9, f"size2/size4 classes vs step-0 X11 classes npz: names {names11}; max|dD, dDx, dE, dRt| {m2a:.2e} (scale {sc2:.0f}); max rel den, den_r {m2r:.1e}",
      "<= 1e-9 x max; rel <= 1e-9")
check("M3", M3 <= 1e-12, f"partitioning variables {list(XC.PARTITION)}: max rel |sum(class den) + invalid den - ALL den| {M3:.1e}", "<= 1e-12")
# ---------------------------------------------------------------- products (scratch)
NPZ = os.path.join(WORK, f"x13_measure_classes{TAG}.npz")
arr = lambda f: np.array([[o[key][f] for key in HX] for o in MEAS])
np.savez(NPZ, name=np.array([o["name"] for o in MEAS]), ra=np.array([o["ra"] for o in MEAS]), dec=np.array([o["dec"] for o in MEAS]),
         z=np.array([o["z"] for o in MEAS]), Mgas500=np.array([o["Mgas500"] for o in MEAS]), nrand=np.array([o["nrand"] for o in MEAS]),
         hx=np.array(HX), varnames=np.array([n_ for n_, _ in XC.VARS]), varsizes=np.array([k_ for _, k_ in XC.VARS]),
         D=arr("D"), Dx=arr("Dx"), E=arr("E"), Ex=arr("Ex"), den=arr("den"), den_r=arr("den_r"), cnt=arr("cnt"), cnt_r=arr("cnt_r"), sisc=arr("sisc"),
         Rx=arr("Rx"), Rt=arr("Rt"), XS=arr("XS"), rot=arr("rot"), rotRx=arr("rotRx"))
RES["npz_sha256"] = sha(NPZ); say(f"wrote scratch {os.path.basename(NPZ)} sha256 {RES['npz_sha256'][:16]}...")
pk = rss(); check("M4", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
RES.update(N=N, R=XC.R, runtime_s=time.time() - T0, peak_rss_GB=pk)
npass = sum(ok for _, ok in CHECKS); say(f"X13_MEASURE COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x13_measure_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
