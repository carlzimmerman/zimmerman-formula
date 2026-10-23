#!/usr/bin/env python3
"""S4_v3_muK_clusters, batch R4 of N0_board_audit (criteria f167979b09): kernel-only recomputes of tiles 22, 33, 34.
Each committed script runs UNCHANGED in a fresh child interpreter that (i) replaces the record's nu_mono (FP1/L340, held by
campaign_fresh_gravity/CFG4_common.py and CFG2_common.py) by v3's nu_1(y) = (1 + sqrt(1 + 4/y))/2 before the script imports
it, and (ii) redirects every file the script writes inside the repository into this lane (r4_out/<script>/<variant>/).
Any multiprocessing Pool a script opens is replaced by a serial map in the same process (one thread; same results).
Variants: repro (record kernel; must reproduce the committed JSON), nu1 (v3 kernel), and for CFG528b also nu1_noown
(v3 kernel + no host ownership: the R-own reading replaced by R-bar).  The record's lanes are hashed before and after.
Usage: OMP_NUM_THREADS=1 nice -n 15 python3 s4_r4_kernel_swaps.py [--mutate]   (--mutate: the repro slot uses nu_1, so R4-K0 must FAIL)
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys, json, time, hashlib, subprocess, builtins, io, math
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); CFG = os.path.join(REPO, "campaign_fresh_gravity")
OUTROOT = os.path.join(HERE, "r4_out")

SCRIPTS = {   # tile -> committed scripts (relative to campaign_fresh_gravity) and their committed results JSON
    "22": [("CFG528_sluggs_centrals_mechanism/cfg528b_measured_tracers.py", "cfg528b_measured_tracers_results.json")],
    "33": [(f"CFG303_lcdm_free_inputs/cfg303_{k}_LCDMFREE.py", f"cfg303_{k}_LCDMFREE_results.json")
           for k in ("amvrosiadis", "cfg90_noema", "kurvs", "musedark", "rc100_cristal", "xcop")],
    "34": [("CFG307_aless122_stress_test/cfg307_stress.py", "cfg307_stress_results.json"),
           ("CFG308_cristal_stress_test/cfg308_cristal_stress.py", "cfg308_cristal_stress_results.json")],
}
HASH_DIRS = ["CFG528_sluggs_centrals_mechanism", "CFG331_sluggs_centrals_environment", "CFG303_lcdm_free_inputs", "CFG307_aless122_stress_test",
             "CFG308_cristal_stress_test", "CFG213_dysmalpy_two_sided", "CFG216_rc100_within_sample", "CFG217_rc100_attack", "CFG262_musedark_zthirds_by_route",
             "CFG274_amvrosiadis_eight_discs", "CFG189_kurvs_measured_markers", "CFG229_class_m_gold", "CFG223_a0_over_cosmic_time", "CFG90_a0z_rederivation",
             "HZQ_common", "CFG515_census_edge_resolution", "CFG323_sluggs_measured_tracers"]

# ======================================================================================== child mode
def child(script_rel, variant, outdir):
    import numpy as np
    sys.path.insert(0, CFG)
    os.makedirs(outdir, exist_ok=True)
    REDIR = []
    _open = builtins.open
    def ropen(file, mode="r", *a, **k):
        if isinstance(file, (str, bytes, os.PathLike)) and any(c in mode for c in "wax+"):
            p = os.path.abspath(os.fsdecode(file))
            if p.startswith(REPO + os.sep) and not p.startswith(OUTROOT + os.sep):
                q = os.path.join(outdir, os.path.relpath(p, REPO).replace(os.sep, "__")); REDIR.append((os.path.relpath(p, REPO), os.path.relpath(q, HERE)))
                return _open(q, mode, *a, **k)
        return _open(file, mode, *a, **k)
    builtins.open = ropen; io.open = ropen
    import CFG4_common as C4, CFG2_common as C2
    orig = C4.nu_mono
    calls = {"orig": 0, "nu1": 0, "orig2": 0}
    def nu1(y):
        calls["nu1"] += 1; y = np.maximum(np.asarray(y, float), 1e-300); return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))
    def count_orig(f, key):
        def g(y): calls[key] += 1; return f(y)
        return g
    if variant.startswith("nu1"):
        new4 = new2 = nu1
    else:
        new4, new2 = count_orig(C4.nu_mono, "orig"), count_orig(C2.nu_mono, "orig2")
    for mod, new in ((C4, new4), (C2, new2)):
        old = mod.nu_mono; mod.nu_mono = new
        for name in dir(mod):
            v = getattr(mod, name)
            if isinstance(v, dict):
                for kk, vv in list(v.items()):
                    if vv is old: v[kk] = new
    probe = float(np.asarray(C4.nu_mono(1.0)))
    import multiprocessing as mp                      # one process: any Pool the script opens runs serially, in this process
    class _SerialPool:
        def __init__(self, *a, **k): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def map(self, f, it, chunksize=None): return list(map(f, it))
        def close(self): pass
        def join(self): pass
    class _Ctx:
        def Pool(self, *a, **k): return _SerialPool()
    mp.get_context = lambda method=None: _Ctx(); mp.Pool = _SerialPool
    src = _open(os.path.join(CFG, script_rel)).read()
    if variant == "nu1_noown":
        a = 'READ = {"K0": {}, "bar": dict(gas="extrap"), "own": dict(gas="extrap", own=True)}'
        assert src.count(a) == 1; src = src.replace(a, 'READ = {"K0": {}, "bar": dict(gas="extrap"), "own": dict(gas="extrap")}   # S4 R4: no ownership (v3)')
    for k in [k for k in os.environ if k.endswith("MUTATE") or k.endswith("POSTFREEZE")]: os.environ.pop(k)
    path = os.path.join(CFG, script_rel); os.chdir(os.path.dirname(path)); sys.argv = [path]
    ns = {"__file__": path, "__name__": "__main__"}
    code = 0; t0 = time.time()
    try:
        exec(compile(src, path, "exec"), ns)
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    except Exception as e:
        code = f"EXCEPTION {type(e).__name__}: {e}"
    summ = dict(script=script_rel, variant=variant, exit=code, probe_nu_at_1=probe, calls=calls, redirected=REDIR, runtime_s=time.time() - t0)
    with _open(os.path.join(outdir, "_child_summary.json"), "w") as fh: json.dump(summ, fh, indent=1, default=str)

# ======================================================================================== parent mode
def sha_dirs():
    out = {}
    for d in HASH_DIRS:
        base = os.path.join(CFG, d)
        if not os.path.isdir(base): continue
        for root, _, files in os.walk(base):
            for fn in files:
                p = os.path.join(root, fn)
                if "__pycache__" in p: continue
                out[os.path.relpath(p, REPO)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out

SKIP = ("runtime", "time_s", "seconds", "elapsed", "rss", "peak", "wall", "date", "path", "file", "sha", "tmp")
def leaves(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{pre}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from leaves(v, f"{pre}[{i}]")
    else:
        yield pre, o
def compare(a, b):
    """numeric-leaf comparison (keys with time/path-like names skipped). Returns (n_compared, n_diff, max_rel, worst, structure_ok)."""
    la = {k: v for k, v in leaves(a) if not any(s in k.lower() for s in SKIP)}; lb = {k: v for k, v in leaves(b) if not any(s in k.lower() for s in SKIP)}
    n = nd = 0; mx = 0.0; worst = None
    for k in la.keys() & lb.keys():
        x, y = la[k], lb[k]
        if isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            if isinstance(x, str) and isinstance(y, str) and x != y and not any(s in k.lower() for s in SKIP):
                n += 1; nd += 1; worst = worst or (k, x, y)
            elif x == y: n += 1
            continue
        n += 1
        if (isinstance(x, float) and math.isnan(x)) and (isinstance(y, float) and math.isnan(y)): continue
        d = abs(x - y); rel = d / max(abs(x), abs(y), 1e-300)
        if d > 1e-12 and rel > 1e-9:
            nd += 1
            if rel > mx: mx, worst = rel, (k, x, y)
    return n, nd, mx, worst, set(la) == set(lb)

def main():
    MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
    OUT = open(os.path.join(HERE, f"s4_r4_kernel_swaps{TAG}.out"), "w")
    def say(s=""): print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
    RES = {"lane": "S4_v3_muK_clusters", "batch": "R4", "criteria": "f167979b09", "mutate": MUT}; CHK = []
    def check(name, ok, val, thr):
        CHK.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    say(f"S4 R4 kernel swaps (nu_mono -> nu_1){'  [MUTATE: repro slot uses nu_1]' if MUT else ''}   kappa = 1/2 FITTED; footings never pooled")
    h0 = sha_dirs(); T0 = time.time()
    todo = [(t, s, j) for t, lst in SCRIPTS.items() for s, j in lst]
    if MUT: todo = [x for x in todo if "xcop" in x[1] or "cfg528b" in x[1]]
    for tile, script, jname in todo:
        name = os.path.splitext(os.path.basename(script))[0]
        variants = ["repro", "nu1"] + (["nu1_noown"] if "cfg528b" in script else [])
        if MUT: variants = ["repro"]
        runs = {}
        for v in variants:
            od = os.path.join(OUTROOT + TAG, name, v)
            os.makedirs(od, exist_ok=True)
            vv = ("nu1" if (MUT and v == "repro") else v)
            t1 = time.time()
            with open(os.path.join(od, "_stdout.txt"), "w") as fo:
                rc = subprocess.run([sys.executable, os.path.abspath(__file__), "--child", script, vv, od], stdout=fo, stderr=subprocess.STDOUT,
                                    env={**os.environ, "OMP_NUM_THREADS": "1"}).returncode
            sm = json.load(open(os.path.join(od, "_child_summary.json"))) if os.path.exists(os.path.join(od, "_child_summary.json")) else {"exit": f"child rc {rc}"}
            js = [q for p, q in sm.get("redirected", []) if os.path.basename(p) == jname]
            runs[v] = dict(summary=sm, json=(json.load(open(os.path.join(HERE, js[-1]))) if js else None), outdir=os.path.relpath(od, HERE))
            say(f"  [{tile}] {name} {v}: exit {sm.get('exit')}, probe nu(1) {sm.get('probe_nu_at_1')}, kernel calls {sm.get('calls')}, {len(sm.get('redirected', []))} files redirected, {time.time() - t1:.0f} s")
        committed = json.load(open(os.path.join(CFG, os.path.dirname(script), jname)))
        rep = runs["repro"]["json"]
        if rep is None:
            check(f"R4-K0[{name}]", False, "N/A: the reproduction run wrote no results JSON (" + str(runs["repro"]["summary"].get("exit")) + ")", "reproduce committed JSON")
            RES[name] = dict(tile=tile, reproduced=False, runs={k: v["summary"] for k, v in runs.items()}); continue
        n, nd, mx, worst, st = compare(committed, rep)
        check(f"R4-K0[{name}]", nd == 0 and n > 0, f"{n} leaves compared, {nd} differ (max rel {mx:.1e}; worst {worst})", "all numeric leaves rel <= 1e-9 or abs <= 1e-12")
        entry = dict(tile=tile, reproduced=bool(nd == 0 and n > 0), leaves=n, repro_ndiff=nd, repro_maxrel=mx, runs={k: v["summary"] for k, v in runs.items()})
        if not MUT:
            for v in variants[1:]:
                if runs[v]["json"] is None:
                    entry[v] = dict(error=str(runs[v]["summary"].get("exit"))); continue
                n2, nd2, mx2, w2, _ = compare(rep, runs[v]["json"])
                sm = runs[v]["summary"]; reached = bool(sm["calls"]["nu1"] > 0 and abs(sm["probe_nu_at_1"] - 1.6180339887) < 1e-9)
                entry[v] = dict(leaves=n2, ndiff=nd2, max_rel_change=mx2, worst=w2, kernel_reached=reached, nu1_calls=sm["calls"]["nu1"])
                if v == "nu1":
                    check(f"R4-K1[{name}]", reached and nd2 > 0, f"nu_1 calls {sm['calls']['nu1']}, probe {sm['probe_nu_at_1']:.10f}; {nd2}/{n2} leaves change (max rel {mx2:.2e})", "kernel reached and >= 1 leaf changes")
        RES[name] = entry
    h1 = sha_dirs()
    changed = sorted(k for k in h0.keys() | h1.keys() if h0.get(k) != h1.get(k))
    check("R4-K2", not changed, f"{len(h0)} record files hashed; changed: {changed[:5]}", "no record file changed")
    RES["checks"] = {n: ok for n, ok in CHK}; RES["runtime_s"] = time.time() - T0
    npass = sum(ok for _, ok in CHK)
    say(f"S4_R4_KERNEL_SWAPS COMPLETE: {npass}/{len(CHK)} checks PASS.  runtime {time.time() - T0:.0f} s")
    json.dump(RES, open(os.path.join(HERE, f"s4_r4_kernel_swaps_results{TAG}.json"), "w"), indent=1, default=str)
    sys.exit(0 if npass == len(CHK) else 1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--child":
        child(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        main()
