#!/usr/bin/env python3
"""SY1 search, PySR on BF1's split. Criteria FROZEN_CRITERIA.md, AMENDMENT_A1.md, AMENDMENT_A2.md.
  python3 sy1.py MODE [--maxw N] [--iters I] [--slice K] [--runs DIR] [--limit N] [--dry]     MODE: real scrambled planted mutate
A pool of one-core workers, one search each, serial and seeded. Each search saves state every K iterations, so SIGTERM loses at most one slice; rerun resumes. Yields to 1024^3 runs and compute_queue jobs, and restarts when they clear.
Outputs: runs/MODE/TAG_ARM_Wn_sSEED/front.csv, by mode. A hit is a description of data, not a theory. kappa = 1/2 FITTED; not theory closed."""
import argparse, json, os, pickle, re, shutil, signal, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); SEEDS = list(range(1, 9)); MAXFLOATS = dict(T=2, Z=0)
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
os.environ.update(JULIA_NUM_THREADS="1", PYTHON_JULIACALL_THREADS="1", PYTHON_JULIAPKG_OFFLINE="yes", PYTHONUNBUFFERED="1")
TAGS = {"T": ("P1N0", "P1N1", "P2N0", "P2N1"), "Z": ("P1N0", "P1N1", "P3N0", "P3N1")}
def tasks(mode):
    if mode == "planted":
        from_tag = dict(P1=3, P2=1, P3=2); return [(t, a, from_tag[t[:2]], s) for a in "TZ" for t in TAGS[a] for s in SEEDS]
    sd = SEEDS if mode != "mutate" else [101]
    return [("R" if mode == "real" else mode[0].upper(), a, w, s) for a in "TZ" for w in (1, 2, 3) for s in sd]
def tdir(runs, mode, t): return os.path.join(runs, mode, f"{t[0]}_{t[1]}_W{t[2]}_s{t[3]}")
LOSS = r"""
function sy1_loss(tree, dataset::Dataset{T,L}, options)::L where {T,L}
    H, ok = eval_tree_array(tree, dataset.X, options)
    !ok && return L(Inf)
    y = dataset.y; g = dataset.weights; n = length(y); NX = %d; sx = zero(T); ss = zero(T)
    @inbounds for i in 1:n
        h = H[i]; (isfinite(h) && h > zero(T)) || return L(Inf)
        b = g[i]
        p = %s
        d = y[i] - log10(p)
        if i <= NX; sx += d * d; else; ss += d * d; end
    end
    c = count(n -> n.degree == 0 && n.constant, hasfield(typeof(tree), :tree) ? getfield(tree, :tree) : tree)
    return L((sx / NX + ss / (n - NX)) / 2 + %s)
end
"""
WJ = {1: "b / 2 + sqrt(b * b / 4 + h * b)", 2: "let x = b * h; x / 2 + sqrt(x * x / 4 + x) end", 3: "(b / 2 + sqrt(b * b / 4 + b)) * h"}
def loss_str(w, arm, nx):
    return LOSS % (nx, WJ[w], f"(c > {MAXFLOATS[arm]} ? T(1000) * (c - {MAXFLOATS[arm]}) : zero(T))")
def worker(a):
    from pysr import PySRRegressor
    from sy1_export import mappings
    import numpy as np, sy1_data as DD
    mode, t = a.mode, (a.w_tag, a.w_arm, a.w_w, a.w_seed); d = tdir(a.runs, mode, t); os.makedirs(d, exist_ok=True); P = os.path.join(d, "progress.json"); S = os.path.join(d, "state.pkl"); run = os.path.join(d, "hof")
    tag = t[0] if mode == "planted" else None; X, y, yt, nx = DD.build(mode, tag); prog = json.load(open(P)) if os.path.exists(P) else dict(iters=0, secs=0.0, bf1_sha=DD.BF1_SHA)
    kw = dict(binary_operators=["+", "-", "*", "/"], unary_operators=["sqrt", "log1p", "inv1p(x) = 1 / (1 + x)", "square"], extra_sympy_mappings=mappings(), loss_function=loss_str(t[2], t[1], nx), maxsize=30, parallelism="serial", deterministic=True, random_state=t[3], warm_start=True, niterations=a.slice, output_directory=d, run_id="hof", verbosity=0, progress=False, precision=64, update=False)
    if t[1] == "Z": kw.update(should_optimize_constants=False, weight_mutate_constant=0.0, optimize_probability=0.0)
    if prog["iters"] and os.path.exists(S):
        shutil.copy(S, os.path.join(run, "checkpoint.pkl")); m = PySRRegressor.from_file(run_directory=run, extra_sympy_mappings=mappings()); m.set_params(niterations=a.slice, warm_start=True, extra_sympy_mappings=kw["extra_sympy_mappings"])
    else: m = PySRRegressor(**kw)
    names = list(DD.FEATURES)
    while prog["iters"] < a.iters:
        t0 = time.time(); m.fit(X, y, weights=yt, variable_names=names); prog["iters"] += a.slice; prog["secs"] += time.time() - t0
        shutil.copy(os.path.join(run, "checkpoint.pkl"), S + ".tmp"); os.replace(S + ".tmp", S); shutil.copy(os.path.join(run, "hall_of_fame.csv"), os.path.join(d, "front.tmp")); os.replace(os.path.join(d, "front.tmp"), os.path.join(d, "front.csv"))
        json.dump(prog, open(P + ".tmp", "w")); os.replace(P + ".tmp", P)
        if os.environ.get("SY1_POOL") and os.getppid() == 1: return 75  # the pool died; state is saved
    json.dump(dict(prog, target=a.iters), open(os.path.join(d, "DONE"), "w")); return 0
def heavy_live():
    try:
        s = json.load(open(os.path.join(REPO, "compute_queue", "status.json"))); rx = s.get("config", {}).get("external_heavy_regex") or r"cfg6[0-9][0-9]_pm\.py|run_65[04]\.py|cfg596_pm|cfg960_sctm_pm\.py|run_960\.py"
        if s.get("running") or any(x.get("footprint_gb", 0) >= 1 for x in s.get("external_heavy") or []): return "compute_queue job"
    except Exception: rx = r"cfg6[0-9][0-9]_pm\.py|run_65[04]\.py|cfg596_pm|cfg960_sctm_pm\.py|run_960\.py"
    for l in subprocess.run(["ps", "-axo", "pid=,comm=,command="], capture_output=True, text=True).stdout.splitlines():
        t = l.split(None, 2)
        if len(t) == 3 and not re.search(r"(^|/)(bash|zsh|sh|grep|pgrep|ps|tail|nohup)$", t[1]) and re.search(rx, t[2]) and int(t[0]) != os.getpid(): return "1024^3 run " + t[0]
    return ""
def mem_free_gb():
    v = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout; g = lambda k: int(re.search(k + r":\s+(\d+)", v).group(1)); return (g("Pages free") + g("Pages inactive")) * 16384 / 1e9
def pool(a):
    T = tasks(a.mode)
    if a.limit: T = T[:a.limit]
    os.makedirs(os.path.join(a.runs, a.mode), exist_ok=True); stop = dict(x=0); W = {}; fails = {}
    signal.signal(signal.SIGTERM, lambda *_: stop.__setitem__("x", 1)); signal.signal(signal.SIGINT, lambda *_: stop.__setitem__("x", 1)); ncpu = os.cpu_count()
    def say(*m): print(time.strftime("%m-%d %H:%M:%S"), f"[{a.mode}]", *m, flush=True)
    def stop_all():
        for p in W.values():
            try: os.killpg(p.pid, signal.SIGTERM)
            except OSError: pass
        t0 = time.time()
        while time.time() - t0 < 20 and any(p.poll() is None for p in W.values()): time.sleep(1)
        for p in W.values():
            if p.poll() is None:
                try: os.killpg(p.pid, signal.SIGKILL)
                except OSError: pass
            p.wait()
        W.clear()
    last = 0
    while True:
        if stop["x"]: stop_all(); say("SIGTERM: checkpointed, exit 75"); return 75
        for t, p in list(W.items()):
            if p.poll() is not None:
                del W[t]; rc = p.returncode
                if not os.path.exists(os.path.join(tdir(a.runs, a.mode, t), "DONE")): fails[t] = fails.get(t, 0) + 1; say("worker exit", rc, t, "try", fails[t])
                else: say("done", t)
        pend = [t for t in T if not os.path.exists(os.path.join(tdir(a.runs, a.mode, t), "DONE")) and t not in W and fails.get(t, 0) < 3]
        if not pend and not W:
            bad = [t for t in T if not os.path.exists(os.path.join(tdir(a.runs, a.mode, t), "DONE"))]; say(f"finished, {len(T) - len(bad)} of {len(T)} searches, failed {bad}"); return 1 if bad else 0
        h = heavy_live()
        if h:
            if W: say("yielding to", h); stop_all()
            time.sleep(60); continue
        now = time.time()
        if pend and now - last >= a.ramp:
            load = os.getloadavg()[0]; free = ncpu - max(load, len(W)); m = mem_free_gb()
            if len(W) < a.maxw and m >= 6.0 and (a.fixed or not W or free >= 1.0):
                t = pend[0]; lg = open(os.path.join(a.runs, a.mode, "workers.log"), "a"); cmd = [sys.executable, os.path.abspath(__file__), a.mode, "--runs", a.runs, "--iters", str(a.iters), "--slice", str(a.slice), "--w-tag", t[0], "--w-arm", t[1], "--w-w", str(t[2]), "--w-seed", str(t[3])]
                W[t] = subprocess.Popen(cmd, start_new_session=True, env=dict(os.environ, SY1_POOL="1"), stdout=lg, stderr=subprocess.STDOUT, cwd=HERE); last = now; say(f"start {t}: {len(W)} workers, load {load:.1f}, free+inactive {m:.0f} GB")
        time.sleep(5)
def dry(a):
    import numpy as np, sy1_data as DD
    for t in tasks(a.mode)[:1] if a.mode != "planted" else [(x, "T", 0, 1) for x in TAGS["T"]] + [(x, "Z", 0, 1) for x in TAGS["Z"]]:
        X, y, yt, nx = DD.build(a.mode, t[0] if a.mode == "planted" else None); print(a.mode, t, X.shape, "NX", nx, "finite", bool(np.all(np.isfinite(y))), "tasks", len(tasks(a.mode)), "bf1", DD.BF1_SHA)
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("mode", choices=["real", "scrambled", "planted", "mutate"]); ap.add_argument("--maxw", type=int, default=os.cpu_count() - 1); ap.add_argument("--iters", type=int, default=2); ap.add_argument("--slice", type=int, default=1); ap.add_argument("--runs", default=os.path.join(HERE, "runs")); ap.add_argument("--limit", type=int, default=0); ap.add_argument("--ramp", type=float, default=90.0); ap.add_argument("--dry", action="store_true"); ap.add_argument("--fixed", action="store_true", help="hold maxw workers whatever the load; the memory floor and the yield to heavy runs still apply")
    ap.add_argument("--w-tag"); ap.add_argument("--w-arm"); ap.add_argument("--w-w", type=int); ap.add_argument("--w-seed", type=int); a = ap.parse_args(); sys.path.insert(0, HERE)
    if a.dry: dry(a); sys.exit(0)
    sys.exit(worker(a) if a.w_tag else pool(a))
