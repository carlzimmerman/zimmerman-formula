"""X11 §3 / §5 N1 (criteria 9a105431c9): extended random points. 20 new random positions per cluster (numpy
default_rng(20261025); F1/X7's placement: uniform angle, 1-3 deg away, the cluster's z; accepted if the h 0.70 in-bin count
exceeds 0.5 x the cluster's; up to 60 tries), ALL sources: raw tangential and cross ESD per bin, counts, and R = 200 rotated
cross realisations (MID bins, X7's draws). Part 1 re-measures F1's own randoms of the first 3 clusters with this code path (R1).
Usage: x11_randoms.py <x11 cache> <scratch dir with step-0 products> [--part1|--part2] [--mutate]   (--mutate: 5 clusters, e2 flipped; R1 must FAIL)
A2 (PRE-RESULT, implementation): the full run exceeds 30 min, so it runs in two parts (clusters 0-162, 163-325); part 1 saves its
arrays and the numpy generator state to scratch, part 2 resumes with that state (identical draws to one run). R1 runs in part 1."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import json, hashlib, resource, time, numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import x11_common as XC
T0 = time.time()
MUT = "--mutate" in sys.argv; ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; CACHE, SOUT = ARGS[0], ARGS[1]
P1 = "--part1" in sys.argv; P2 = "--part2" in sys.argv; TAG = ("_MUTATE" if MUT else "") + ("_P1" if P1 else "")
OUTF = open(os.path.join(HERE, f"x11_randoms{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
RES["x11_common_sha256"] = sha(os.path.join(HERE, "x11_common.py"))
NS = XC.init(CACHE); HX = XC.HX
X = np.load(os.path.join(SOUT, "x7_measure_percluster.npz")); XE = np.load(os.path.join(SOUT, "x7_measure_extras.npz"))
NAMES = [str(s) for s in X["name"]]; N = len(NAMES); NUSE = 5 if MUT else N; I0, I1 = (0, 163) if P1 else ((163, NUSE) if P2 else (0, NUSE))
PART = os.path.join(SOUT, "x11_randoms_part1_state.npz")
say(f"sources {NS:,}; clusters {N} (step-0 npz); using {NUSE}")
def stack(calls, key):
    """mean over calls of the raw t/x ESD per bin, counts, den; and the rotated cross (MID, normalised per call)."""
    S = np.array([c["h"][key]["S"][:, 0] for c in calls])                                     # (n, 7, 8)
    t = XC.esd(S[:, 0], S[:, 2]); x = XC.esd(S[:, 1], S[:, 2])
    hi = HX.index(key); rot = np.array([XC.esd(c["rot"][hi][0], c["h"][key]["S"][2][0][3:6][:, None]) for c in calls])   # (n, 3, R)
    return t.mean(0), x.mean(0), S[:, 5].mean(0), S[:, 2].mean(0), rot.mean(0)
# ---------------------------------------------------------------- R1: F1's own randoms of the first 3 clusters, this code path
r1 = 0.0; r1r = 0.0; sc = float(np.max(np.abs(X["Rmeanx"][:3]))) + float(np.max(np.abs(X["Rmean"][:3])))
for i in (range(3) if not P2 else []):
    pos = [p for p in XE["rpos"][i] if np.isfinite(p[0])]
    calls = [XC.call(float(p[0]), float(p[1]), float(X["z"][i]), rot=True, use_vars=False, mut=MUT) for p in pos]
    for hi, key in enumerate(HX):
        t, x, _, _, rot = stack(calls, key); hj = 1 + hi
        r1 = max(r1, float(np.max(np.abs(t - X["Rmean"][i, hj]))), float(np.max(np.abs(x - X["Rmeanx"][i, hj]))))
        r1r = max(r1r, float(np.max(np.abs(rot.T - XE["rot"][i, hi, :, 4, 3:6]))))
if not P2: check("R1", r1 <= 1e-9*sc and r1r <= 1e-6*float(np.max(np.abs(XE["rot"][:3, :, :, 4, 3:6]))),
      f"F1 randoms (first 3 clusters) re-measured: max|d Rmean, Rmeanx| {r1:.2e} (scale {sc:.1f}); rotated random-mean cross {r1r:.2e}", "<= 1e-9 x max; <= 1e-6 x max")
# ---------------------------------------------------------------- the extended random set
rng = np.random.default_rng(20261025); NR = 20; OUT = {k: [] for k in ("Rt", "Rx", "cnt", "den", "rot", "nacc", "ntry")}
if P2:                                                               # resume: part 1's arrays and generator state
    S1 = np.load(PART, allow_pickle=False); rng.bit_generator.state = json.loads(str(S1["rng_state"]))
    for k in OUT: OUT[k] = list(S1[k])
    J1 = json.load(open(os.path.join(HERE, "x11_randoms_results_P1.json"))); RES["part1_checks"] = J1["checks"]
    for nm_, c_ in J1["checks"].items():
        nm2 = nm_ if nm_ != "R3" else "R3_part1"; CHECKS.append((nm2, c_["pass_"])); RES.setdefault("checks", {})[nm2] = c_
        say(f"{nm2} (part 1) {'PASS' if c_['pass_'] else 'FAIL'} {c_['value']} {c_['threshold']}")
    say(f"resumed after {len(OUT['nacc'])} clusters (part 1 sha256 {sha(PART)[:16]}...)")
for i in range(I0, I1):
    ra, de, z = float(X["ra"][i]), float(X["dec"][i]), float(X["z"][i])
    m = XC.call(ra, de, z, rot=False, use_vars=False); n0 = m["n070"]; acc = []; ntry = 0
    while len(acc) < NR and ntry < 60:
        a = rng.uniform(0, 2*np.pi); s = rng.uniform(1, 3); ntry += 1
        rra, rde = (ra + s*np.cos(a)/np.cos(np.radians(de))) % 360, de + s*np.sin(a)
        rr = XC.call(rra, rde, z, rot=True, use_vars=False, mut=MUT, min070=0.5*n0)
        if rr is not None and rr["n070"] > 0.5*n0: acc.append(rr)
    per = [stack(acc, key) for key in HX]
    OUT["Rt"].append([p[0] for p in per]); OUT["Rx"].append([p[1] for p in per]); OUT["cnt"].append([p[2] for p in per]); OUT["den"].append([p[3] for p in per])
    OUT["rot"].append(np.array([p[4] for p in per], np.float32)); OUT["nacc"].append(len(acc)); OUT["ntry"].append(ntry)
    if (i + 1) % 25 == 0: say(f"  {i+1} clusters, {sum(OUT['nacc'])} extended randoms [{time.time()-T0:.0f} s, RSS {rss():.2f} GB]")
if P1:
    np.savez(PART, rng_state=json.dumps(rng.bit_generator.state), **{k: np.array(v) for k, v in OUT.items()})
    pk = rss(); check("R3", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB"); RES.update(part1_sha256=sha(PART), runtime_s=time.time() - T0, peak_rss_GB=pk, n_done=len(OUT["nacc"]))
    npass = sum(ok for _, ok in CHECKS); say(f"X11_RANDOMS PART 1 COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
    json.dump(RES, open(os.path.join(HERE, f"x11_randoms_results{TAG}.json"), "w"), indent=1); sys.exit(0 if npass == len(CHECKS) else 1)
na = np.array(OUT["nacc"]); say(f"extended randoms: {na.sum()} accepted ({na.min()}-{na.max()} per cluster; {np.sum(OUT['ntry'])} tries)")
RES.update(n_accepted=int(na.sum()), n_min=int(na.min()), n_max=int(na.max()), n_tries=int(np.sum(OUT["ntry"])))
# ---------------------------------------------------------------- R2: rotated extended stacks centre on zero (cluster W from X7's E)
ROT = np.array(OUT["rot"]); r2 = []
for hi, key in enumerate(HX):
    Et = X["E"][:NUSE, 1 + hi][:, 3:6]; W = np.where(Et < 1e8, 1/Et**2, 0); v = (W[:, None, :]*np.transpose(ROT[:, hi], (0, 2, 1))).sum((0, 2))
    r2.append(abs(v.mean())/(v.std(ddof=1)/np.sqrt(XC.R)))
check("R2", max(r2) <= 4, f"|mean|/(std/sqrt R) per h: {np.round(r2, 2).tolist()}", "<= 4")
NPZ = os.path.join(SOUT, f"x11_randoms{TAG}.npz")
np.savez(NPZ, name=np.array(NAMES[:NUSE]), hx=np.array(HX), Rt=np.array(OUT["Rt"]), Rx=np.array(OUT["Rx"]), cnt=np.array(OUT["cnt"]), den=np.array(OUT["den"]),
         rot=ROT, nacc=na)
RES["npz_sha256"] = sha(NPZ); say(f"wrote scratch {os.path.basename(NPZ)} sha256 {RES['npz_sha256'][:16]}...")
pk = rss(); check("R3", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk)
npass = sum(ok for _, ok in CHECKS); say(f"X11_RANDOMS COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x11_randoms_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
