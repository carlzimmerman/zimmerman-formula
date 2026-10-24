"""X13 step 0 checks (criteria c4e5a5a064 §1): the rebuilt cache and X7's / X11's committed code reproduce their committed products.
S0-1 cache column sha256 = X7's committed; S0-2 step-0 X7 per-cluster npz = X7's committed npz exactly; S0-3 the step-0 X11
analysis JSON = X11's committed JSON (git blob c1cd5455a5) on the size numbers and the main results (<= 1e-9; strings equal);
S0-4 every check of the step-0 runs PASS except X7 extract E1 (N/A: no F1 cache in this session; S0-1 replaces it).
Usage: x13_s0_check.py <cache> <step-0 scratch> [--mutate]   (--mutate: size2 class labels swapped in S0-3; S0-3 must FAIL)"""
import os, sys, json, hashlib, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
X7 = os.path.join(REB, "X7_cluster_core_significance")
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; CACHE, SOUT = ARGS
OUTF = open(os.path.join(HERE, f"x13_s0_check{TAG}.out"), "w")
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
def blob(commit, path): return subprocess.run(["git", "-C", REPO, "show", f"{commit}:{path}"], capture_output=True, check=True).stdout
# S0-1
ref = json.loads(blob("HEAD", "rebuild_2026_10_22/X7_cluster_core_significance/x7_extract_results.json"))["sha256"]
same = {k: sha_file(os.path.join(CACHE, f"{k}.npy")) == v for k, v in ref.items()}
check("S0-1", all(same.values()) and len(same) == 7, f"rebuilt cache columns vs X7's committed sha256: {same}", "all 7 identical")
# S0-2
A = np.load(os.path.join(SOUT, "x7_measure_percluster.npz")); B = np.load(os.path.join(X7, "x7_measure_percluster.npz"))
nb_ok = subprocess.run(["git", "-C", REPO, "diff", "--quiet", "HEAD", "--", "rebuild_2026_10_22/X7_cluster_core_significance/x7_measure_percluster.npz"]).returncode == 0
dev = {}; keys = sorted(set(A.files) | set(B.files))
for k in keys:
    if k not in A.files or k not in B.files: dev[k] = "missing"; continue
    a = A[k]; b = B[k]
    dev[k] = "equal" if (a.dtype.kind in "US" and np.array_equal(a, b)) or (a.dtype.kind not in "US" and a.shape == b.shape and float(np.max(np.abs(a.astype(float) - b.astype(float)))) == 0.0) else "DIFFERENT"
check("S0-2", nb_ok and all(v == "equal" for v in dev.values()), f"{len(keys)} arrays of the step-0 X7 npz vs X7's committed npz (unmodified in the tree: {nb_ok}): {sum(v == 'equal' for v in dev.values())} equal; different/missing {[k for k, v in dev.items() if v != 'equal']}",
      "all equal (max|diff| = 0)")
# S0-3
J = json.load(open(os.path.join(HERE, "x13_s0_x11_analysis_results.json")))
K = json.loads(blob("c1cd5455a5", "rebuild_2026_10_22/X11_cross_shear_diagnosis/x11_analysis_results.json"))
d3 = []; strs = []
CELLS = ("canonical|h0672", "canonical|h0686", "alt|h0672", "alt|h0686")
for c in CELLS:
    for v in ("size2", "mag2"):
        for j in range(2):
            jj = (1 - j) if (MUT and v == "size2") else j
            for q in ("A", "s_boot", "s_jk", "s_STAT", "Z_STAT"):
                d3.append(abs(J["tangential_Z_per_class"][f"{c}|{v}|{jj}"][q] - K["tangential_Z_per_class"][f"{c}|{v}|{j}"][q]))
    for v in ("size2", "size4"):
        for blk in ("E3", "E3_clip"):
            a_ = np.array(J[blk][f"{c}|{v}"]["a"]); s_ = np.array(J[blk][f"{c}|{v}"]["sig"])
            if MUT and v == "size2": a_ = a_[::-1]; s_ = s_[::-1]
            d3 += list(np.abs(a_ - np.array(K[blk][f"{c}|{v}"]["a"]))) + list(np.abs(s_ - np.array(K[blk][f"{c}|{v}"]["sig"])))
            d3 += [abs(J[blk][f"{c}|{v}"]["boot"][q] - K[blk][f"{c}|{v}"]["boot"][q]) for q in ("dchi2", "p_const")]
    d3 += [abs(J["all_MID"][c][q] - K["all_MID"][c][q]) for q in K["all_MID"][c]]
    d3.append(abs(J["Z_MID"][c] - K["Z_MID"][c]))
strs = [J["verdict"] == K["verdict"], J["E3_sub"] == K["E3_sub"]]
check("S0-3", max(d3) <= 1e-9 and all(strs), f"{len(d3)} numbers of the step-0 X11 analysis JSON vs X11's committed JSON (size2, mag2 per-class Z; E3 and E3_clip size2/size4; all_MID; Z_MID): max|diff| {max(d3):.1e};"
      f" verdict '{J['verdict']}' / E3_sub '{J['E3_sub']}' equal {strs}", "<= 1e-9; strings equal")
# S0-4
s4 = {}; ok4 = True
for st in ("x7_extract", "x7_psf_regression", "x7_measure", "x11_extract_extra", "x11_measure", "x11_randoms", "x11_analysis"):
    r = json.load(open(os.path.join(HERE, f"x13_s0_{st}_results.json")))
    fails = [k for k, v in r["checks"].items() if not v["pass_"]]
    allowed = ["E1"] if st == "x7_extract" else []
    s4[st] = f"{sum(v['pass_'] for v in r['checks'].values())}/{len(r['checks'])}" + (f" (N/A: {fails})" if fails and fails == allowed else (f" FAIL {fails}" if fails else ""))
    ok4 &= (fails == allowed) or (not fails)
check("S0-4", ok4, f"checks of the step-0 runs: {s4}", "all PASS (X7 extract E1 N/A: no F1 cache)")
kx = json.loads(blob("c1cd5455a5", "rebuild_2026_10_22/X11_cross_shear_diagnosis/x11_measure_results.json"))["npz_sha256"]; mx = sha_file(os.path.join(SOUT, "x11_measure_classes.npz"))
say(f"reported: step-0 x11_measure_classes.npz sha256 {mx[:16]}... vs X11's committed npz_sha256 {kx[:16]}...: {'identical' if mx == kx else 'DIFFERENT'}")
RES["x11_classes_npz_identical"] = (mx == kx)
RES["size_halves_step0"] ={c: {j: J["tangential_Z_per_class"][f"{c}|size2|{j}"] for j in range(2)} for c in CELLS}
npass = sum(ok for _, ok in CHECKS); say(f"X13_S0_CHECK COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
json.dump(RES, open(os.path.join(HERE, f"x13_s0_check_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if npass == len(CHECKS) else 1)
