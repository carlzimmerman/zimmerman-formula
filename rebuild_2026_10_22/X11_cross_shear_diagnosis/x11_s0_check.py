"""X11 step 0 checks (criteria 9a105431c9 §1): the rebuilt cache and X7's code reproduce X7's committed products.
S0-1 cache column sha256 = X7's committed; S0-2 per-cluster npz arrays = X7's committed npz exactly; S0-3 analysis JSON = X7's
committed JSON on the listed keys (<= 1e-9); S0-4 every X7 check in the four step-0 runs PASS.
Usage: x11_s0_check.py <x11 cache> <scratch dir> [--mutate]   (--mutate: step-0 Dx sign flipped before S0-2; S0-2 must FAIL)"""
import os, sys, json, hashlib, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); X7 = os.path.join(os.path.dirname(HERE), "X7_cluster_core_significance")
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; CACHE, SOUT = ARGS
OUTF = open(os.path.join(HERE, f"x11_s0_check{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha_file(p):
    hh = hashlib.sha256()
    with open(p, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 24), b""): hh.update(blk)
    return hh.hexdigest()
ref = json.load(open(os.path.join(X7, "x7_extract_results.json")))["sha256"]
same = {k: sha_file(os.path.join(CACHE, f"{k}.npy")) == v for k, v in ref.items()}
check("S0-1", all(same.values()), f"rebuilt cache columns vs X7's committed sha256: {same}", "all 7 identical")
A = np.load(os.path.join(SOUT, "x7_measure_percluster.npz")); B = np.load(os.path.join(X7, "x7_measure_percluster.npz"))
dev = {}; keys = sorted(set(A.files) | set(B.files))
for k in keys:
    if k not in A.files or k not in B.files: dev[k] = "missing"; continue
    a = A[k]; b = B[k]
    if MUT and k == "Dx": a = -a
    dev[k] = "equal" if (a.dtype.kind in "US" and np.array_equal(a, b)) or (a.dtype.kind not in "US" and a.shape == b.shape and float(np.max(np.abs(a.astype(float) - b.astype(float)))) == 0.0) else "DIFFERENT"
check("S0-2", all(v == "equal" for v in dev.values()), f"{len(keys)} arrays of the step-0 npz vs X7's committed npz: {sum(v == 'equal' for v in dev.values())} equal; different/missing {[k for k, v in dev.items() if v != 'equal']}", "all equal (max|diff| = 0)")
J = json.load(open(os.path.join(HERE, "x11_s0_x7_analysis_results.json"))); K = json.load(open(os.path.join(X7, "x7_analysis_results.json")))
d3 = []; n3 = 0
for c in ("canonical|h0672", "canonical|h0686", "alt|h0672", "alt|h0686"):
    for b in ("MID", "OUTER"):
        for q in ("A", "A_x", "s_n_x", "p_x", "resid_x", "s_x_exc", "rand_x", "Z_rand_x", "Z_STAT", "Z_CAL", "s_STAT", "s_CAL"):
            d3.append(abs(J["all"][f"C*|boost|{c}"][b][q] - K["all"][f"C*|boost|{c}"][b][q])); n3 += 1
d3 += [abs(a - b) for a, b in zip(J["Z_MID_CAL"], K["Z_MID_CAL"])] + [abs(J["cross_profile"][k]["chi2"] - K["cross_profile"][k]["chi2"]) for k in K["cross_profile"]]
n3 += len(K["Z_MID_CAL"]) + len(K["cross_profile"])
check("S0-3", max(d3) <= 1e-9 and J["V1"] == K["V1"], f"{n3} numbers of the step-0 analysis JSON vs X7's: max|diff| {max(d3):.1e}; V1 {J['V1']} vs {K['V1']}", "<= 1e-9; V1 equal")
s4 = {}
for st in ("extract", "psf_regression", "measure", "analysis"):
    r = json.load(open(os.path.join(HERE, f"x11_s0_x7_{st}_results.json"))); s4[st] = f"{sum(v['pass_'] for v in r['checks'].values())}/{len(r['checks'])}"
check("S0-4", all(a.split("/")[0] == a.split("/")[1] for a in s4.values()), f"X7 checks in the step-0 runs: {s4}", "all PASS")
RES["step0_numbers"] = {c: {q: J["all"][f"C*|boost|{c}"]["MID"][q] for q in ("A", "A_x", "s_n_x", "p_x", "rand_x", "Z_rand_x", "Z_STAT", "Z_CAL")}
                        for c in ("canonical|h0672", "canonical|h0686", "alt|h0672", "alt|h0686")}
npass = sum(ok for _, ok in CHECKS); say(f"X11_S0_CHECK COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
json.dump(RES, open(os.path.join(HERE, f"x11_s0_check_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
