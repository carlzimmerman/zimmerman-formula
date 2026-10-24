"""X11 step 0 (criteria 9a105431c9 §1): run X7's committed scripts READ-ONLY on a rebuilt cache.
Reads the X7 source text, checks its sha256 against the committed blob (constants below = X7 result commit b1a2ffcb6b),
applies only the declared output-path substitutions (X7 output names x7_* -> x11_s0_x7_* in this lane's dir; X7's
per-cluster npz -> the scratch dir), and executes it with X7's own argument list.
Usage: x11_step0.py <extract|regress|measure|analysis> <X7 script args...> [--mutate]
No network; single thread; the X7 code itself is unchanged."""
import os, sys, hashlib
if os.environ.get("MallocMediumZone") != "0":                       # as X7 (A3): macOS medium zone keeps freed temporaries resident
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
LANE = os.path.dirname(os.path.abspath(__file__)); X7 = os.path.join(os.path.dirname(LANE), "X7_cluster_core_significance")
SRC = {"extract": ("x7_extract.py", "505f5a2db9e1cbc86bdcb3b7e4a64e90de2ed3d6572466b38bbb287b76de2dfd"),
       "regress": ("x7_psf_regression.py", "8a4a9b04ea25329fd3ec047062d59f99e5ddb335db3609b67d9c92cae13f6ac4"),
       "measure": ("x7_measure.py", "9646311d5f063ef090803d6066b01502bbb7c41d4af054debea746c62b9a9c9b"),
       "analysis": ("x7_analysis.py", "0acb1574c1cd6f44762598635490d218c410caaddb90ea4b5f4088b28d03a7f9")}
# (old, new, expected count) per stage; every substitution must occur exactly the expected number of times
HERE_SUB = ("HERE = os.path.dirname(os.path.abspath(__file__))", "HERE = __X11_LANE__", 1)
SUBS = {"extract": [HERE_SUB, ('os.path.join(HERE, f"x7_', 'os.path.join(HERE, f"x11_s0_x7_', 2)],
        "regress": [HERE_SUB, ('os.path.join(HERE, f"x7_', 'os.path.join(HERE, f"x11_s0_x7_', 2)],
        "measure": [HERE_SUB, ('NPZ = os.path.join(HERE, f"x7_measure_percluster', 'NPZ = os.path.join(SOUT, f"x7_measure_percluster', 1),
                    ('os.path.join(HERE, f"x7_', 'os.path.join(HERE, f"x11_s0_x7_', 2)],
        "analysis": [HERE_SUB, ('os.path.join(HERE, "x7_measure_percluster.npz")', 'os.path.join(SOUT, "x7_measure_percluster.npz")', 2),
                     ('os.path.join(HERE, "x7_psf_regression_results.json")', 'os.path.join(HERE, "x11_s0_x7_psf_regression_results.json")', 1),
                     ('os.path.join(HERE, f"x7_', 'os.path.join(HERE, f"x11_s0_x7_', 2)]}
stage = sys.argv[1]; fn, want = SRC[stage]; path = os.path.join(X7, fn)
raw = open(path, "rb").read(); got = hashlib.sha256(raw).hexdigest()
assert got == want, f"X7 source changed: {fn} sha256 {got} != committed {want}"
txt = raw.decode()
for old, new, n in SUBS[stage]:
    c = txt.count(old); assert c == n, f"substitution {old!r}: {c} occurrences, expected {n}"
    txt = txt.replace(old, new)
print(f"[x11_step0] {fn} sha256 {got[:16]}... verified; {len(SUBS[stage])} output-path substitutions applied", flush=True)
sys.argv = [path] + sys.argv[2:]
g = {"__name__": "__main__", "__file__": path, "__X11_LANE__": LANE}
exec(compile(txt, path, "exec"), g)
