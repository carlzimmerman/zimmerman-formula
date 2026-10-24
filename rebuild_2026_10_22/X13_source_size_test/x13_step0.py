"""X13 step 0 (criteria c4e5a5a064 §1): run X7's and X11's committed scripts READ-ONLY on a rebuilt cache.
Re-executes itself with MallocMediumZone=0 first (so no executed script re-executes itself under its own path), reads the
script's source text, checks its sha256 against the committed blob (X7: the values X11's x11_step0.py recorded for X7's
result commit b1a2ffcb6b; X11: result commit c1cd5455a5), applies only the declared path substitutions (each must occur the
declared number of times) and executes it with its own argument list.
Outputs land in this lane as x13_s0_x7_* / x13_s0_x11_*; large products go to the scratch dirs given as arguments.
Usage: x13_step0.py <x7_extract|x7_regress|x7_measure|x11_extract|x11_measure|x11_randoms|x11_analysis> <script args...>
No network; single thread; the X7 / X11 code itself is unchanged."""
import os, sys, hashlib
if os.environ.get("MallocMediumZone") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0", "PYTHONDONTWRITEBYTECODE": "1"})
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
LANE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(LANE)
X7 = os.path.join(REB, "X7_cluster_core_significance"); X11 = os.path.join(REB, "X11_cross_shear_diagnosis")
SRC = {"x7_extract": (X7, "x7_extract.py", "505f5a2db9e1cbc86bdcb3b7e4a64e90de2ed3d6572466b38bbb287b76de2dfd"),
       "x7_regress": (X7, "x7_psf_regression.py", "8a4a9b04ea25329fd3ec047062d59f99e5ddb335db3609b67d9c92cae13f6ac4"),
       "x7_measure": (X7, "x7_measure.py", "9646311d5f063ef090803d6066b01502bbb7c41d4af054debea746c62b9a9c9b"),
       "x11_extract": (X11, "x11_extract_extra.py", "ff3fc8c0dafb1dbc0443c4bea584786ffbcbb92f09e76560fc8222d535c2c408"),
       "x11_measure": (X11, "x11_measure.py", "6716f10a0080e21732c5deab8b20a95ccae43b1f3a908446d5834db7fcd218d6"),
       "x11_randoms": (X11, "x11_randoms.py", "4a20ab20b3579e01e0d905608c746479fc783e396e2258103910d9ecde5934d9"),
       "x11_analysis": (X11, "x11_analysis.py", "f85cf03f623f91645e9f811e07e2663f7b6116284a91519831337bee8e83ca2c")}
X11_COMMON_SHA = "3c72b238884ffa9d29838d57315119f67193a3ca3435876786f317f2023967b0"   # x11_common.py at c1cd5455a5
HERE_SUB = ("HERE = os.path.dirname(os.path.abspath(__file__))", "HERE = __X13_LANE__", 1)
IMP = ("sys.path.insert(0, HERE); import x11_common as XC", "sys.path.insert(0, __X11_DIR__); import x11_common as XC", 1)
CSHA = ('sha(os.path.join(HERE, "x11_common.py"))', 'sha(os.path.join(__X11_DIR__, "x11_common.py"))', 1)
O7 = ('os.path.join(HERE, f"x7_', 'os.path.join(HERE, f"x13_s0_x7_', 2)
O11 = ('os.path.join(HERE, f"x11_', 'os.path.join(HERE, f"x13_s0_x11_', 2)
SUBS = {"x7_extract": [HERE_SUB, O7],
        "x7_regress": [HERE_SUB, O7],
        "x7_measure": [HERE_SUB, ('NPZ = os.path.join(HERE, f"x7_measure_percluster', 'NPZ = os.path.join(SOUT, f"x7_measure_percluster', 1), O7],
        "x11_extract": [HERE_SUB, O11],
        "x11_measure": [HERE_SUB, IMP, CSHA, O11],
        "x11_randoms": [HERE_SUB, IMP, CSHA, ('os.path.join(HERE, "x11_randoms_results_P1.json")', 'os.path.join(HERE, "x13_s0_x11_randoms_results_P1.json")', 1),
                        ('os.path.join(HERE, f"x11_', 'os.path.join(HERE, f"x13_s0_x11_', 3)],
        "x11_analysis": [HERE_SUB, ('"x11_s0_x7_psf_regression_results.json"', '"x13_s0_x7_psf_regression_results.json"', 1),
                         ('os.path.join(HERE, "x11_randoms_results.json")', 'os.path.join(HERE, "x13_s0_x11_randoms_results.json")', 1),
                         ('os.path.join(HERE, "x11_measure_results.json")', 'os.path.join(HERE, "x13_s0_x11_measure_results.json")', 1), O11]}
stage = sys.argv[1]; d, fn, want = SRC[stage]; path = os.path.join(d, fn)
raw = open(path, "rb").read(); got = hashlib.sha256(raw).hexdigest()
assert got == want, f"source changed: {fn} sha256 {got} != committed {want}"
if stage.startswith("x11_"):
    cs = hashlib.sha256(open(os.path.join(X11, "x11_common.py"), "rb").read()).hexdigest()
    assert cs == X11_COMMON_SHA, f"x11_common.py changed: {cs}"
txt = raw.decode()
for old, new, n in SUBS[stage]:
    c = txt.count(old); assert c == n, f"substitution {old!r}: {c} occurrences, expected {n}"
    txt = txt.replace(old, new)
print(f"[x13_step0] {fn} sha256 {got[:16]}... verified; {len(SUBS[stage])} path substitutions applied", flush=True)
sys.argv = [path] + sys.argv[2:]
g = {"__name__": "__main__", "__file__": path, "__X13_LANE__": LANE, "__X11_DIR__": X11}
exec(compile(txt, path, "exec"), g)
