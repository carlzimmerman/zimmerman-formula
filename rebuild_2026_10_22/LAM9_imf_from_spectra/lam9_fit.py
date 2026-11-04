"""LAM9 fit runner (criteria 9c1f411110, amendment A1). One fit per sum and variant (A, then B); failures counted, never refit.
Job contract (compute_queue/JOB_CONTRACT.md): single thread; SIGTERM/SIGINT or compute_queue/YIELD -> checkpoint at the next sum
boundary and exit 75; --resume skips finished sums and exits 0 when complete; every line fsync'd, a torn last line is dropped.
  python3 -I lam9_fit.py --prepare                           stack rebuild + check, step 5, K donor lists (no fit)
  python3 -I lam9_fit.py --phase donors|all --shard K --nshard N [--resume]
  python3 -I lam9_fit.py --merge                             merged lam9_fit_A.jsonl / lam9_fit_B.jsonl in this folder
Shards split the job list by index mod N, so each sum is fitted by exactly one process. κ = ½ FITTED; not theory closed."""
import os, sys, json, signal, time, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"  # before numpy
warnings.filterwarnings("ignore", message=".*encountered in matmul", category=RuntimeWarning)  # spurious on macOS Accelerate (LAM2 A3)
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import lam9_core as L
QY = os.path.join(L.ROOT, "compute_queue", "YIELD")
stop = False
def _term(*_):
    global stop; stop = True
signal.signal(signal.SIGTERM, _term); signal.signal(signal.SIGINT, _term)
arg = sys.argv[1:]
def opt(k, d=None): return arg[arg.index(k) + 1] if k in arg else d
os.makedirs(os.path.join(L.WORK, "w"), exist_ok=True); os.makedirs(os.path.join(L.WORK, "fits"), exist_ok=True)

def prepare():
    S = L.sample(); out = {"lane": "LAM9", "step": "prepare", "note": "κ = ½ FITTED; not theory closed. No fit.", "counts": S["counts"]}
    st = L.build_stack(S); st0 = np.load(L.STACK0); dmax = float(np.nanmax(np.abs(st[:, 2] - st0[:, 2])))
    out["stack_rebuild_max_abs_diff_vs_stage0"] = dmax; assert dmax == 0.0, dmax
    tmp = os.path.join(L.WORK, "narrow_stack.tmp.npy"); np.save(tmp, st); os.replace(tmp, os.path.join(L.WORK, "narrow_stack.npy"))
    wave, narrow = st[:, 0], st[:, 2]; rows = []
    for i in np.flatnonzero(S["cand"]):
        p = L.prep(S["path"][S["pifu"][i]], narrow); assert np.allclose(np.load(S["path"][S["pifu"][i]])["wave"], wave)
        rows.append(dict(i=int(i), plateifu=str(S["pifu"][i]), step5=bool(L.step5(p)), cov_nai=p["cov_nai"], cov_tio2=p["cov_tio2"], z=p["z"],
                         sn_nai_scaled=p["sn_nai"] / np.sqrt(max(S["chi2k"][i], 1.0)), nA=int(len(p["goodA"])), nB=int(len(p["goodB"]))))
    ok = [r for r in rows if r["step5"]]; out["counts"]["step5_pass"] = len(ok); out["counts"]["step5_excluded"] = len(rows) - len(ok)
    sn = np.array([r["sn_nai_scaled"] for r in ok]); edges = np.percentile(sn, [100 / 3, 200 / 3]); out["k_thirds_edges"] = edges.tolist()
    rng = np.random.default_rng(L.SEED); don = []
    for t in range(3):
        lo, hi = ([-np.inf] + edges.tolist())[t], (edges.tolist() + [np.inf])[t]
        pool = [r["plateifu"] for r in ok if lo <= r["sn_nai_scaled"] < hi]; perm = [pool[j] for j in rng.permutation(len(pool))]
        for o, pf in enumerate(perm): don.append((t, o, pf))
    with open(os.path.join(HERE, "lam9_k_donors.csv"), "w") as fo:
        fo.write("# LAM9 K donor order (A1): per third of the chi2_kin-scaled Na I S/N, a seed-20261105 permutation. κ = ½ FITTED; not theory closed.\n")
        fo.write("third,order,plateifu\n"); [fo.write(f"{t},{o},{pf}\n") for t, o, pf in don]
    json.dump(dict(out, rows=rows), open(os.path.join(HERE, "lam9_prepare.json"), "w", encoding="utf-8"), indent=0, ensure_ascii=False, default=float)
    print(json.dumps(out["counts"]), "edges", edges, flush=True)

def donor_lines(): return [l for l in open(os.path.join(HERE, "lam9_k_donors.csv")).read().splitlines() if l.strip() and not l.startswith("#")][1:]
def done_set():
    D = {}
    for fn in sorted(os.listdir(os.path.join(L.WORK, "fits"))):
        if fn.endswith(".jsonl"):
            for r in L.read_jsonl(os.path.join(L.WORK, "fits", fn)): D.setdefault(r["plateifu"], {})[r["variant"]] = r
    return D

def run(phase, k, nk):
    S = L.sample(); wave, narrow = L.load_stack()
    P = json.load(open(os.path.join(HERE, "lam9_prepare.json")))
    ok = sorted(r["plateifu"] for r in P["rows"] if r["step5"])
    if phase == "donors":
        jobs = [l.split(",")[2].strip() for l in donor_lines() if int(l.split(",")[1]) < 110]
    else: jobs = ok
    mine = [j for n_, j in enumerate(jobs) if n_ % nk == k]; D = done_set()
    todo = [j for j in mine if not ("A" in D.get(j, {}) and "B" in D.get(j, {}))]
    print(f"phase {phase} shard {k}/{nk}: {len(mine)} jobs, {len(todo)} to do", flush=True)
    if not todo: sys.exit(0)
    idx = {p: i for i, p in enumerate(S["pifu"])}
    out = os.path.join(L.WORK, "fits", f"lam9_fit.{phase}.s{k}of{nk}.jsonl"); L.read_jsonl(out, repair=True)
    with open(out, "a") as fo:
        for pf in todo:
            if stop or os.path.exists(QY): print("yield: checkpoint at a sum boundary, exit 75", flush=True); fo.close(); sys.exit(75)
            t0 = time.time(); i = idx[pf]; kin = S["FIT"][pf]; p = L.prep(S["path"][pf], narrow)
            try: tpl, lam_t, n_t = L.templates_for(p)
            except Exception as ex:
                for v in ("A", "B"): L.append_jsonl(fo, dict(plateifu=pf, variant=v, status=f"error: templates: {ex}"))
                continue
            for v in ("A", "B"):
                if v in D.get(pf, {}): continue
                r = dict(plateifu=pf, variant=v, z=p["z"], start=p["start"], ngood=int(len(p["goodA"] if v == "A" else p["goodB"])), cov_nai=p["cov_nai"], cov_tio2=p["cov_tio2"])
                try:
                    f = L.fit(p, tpl, lam_t, kin, v); sb = L.summary(f["wb"], n_t); sa = L.summary(f["wa"], n_t)
                    r.update(status="ok", chi2a=f["chi2a"], chi2b=f["chi2b"], **sb, gamma_a=sa["gamma"], alpha_a=sa["alpha"], alpha_ku2_a=sa["alpha_ku2"], alpha_tian_a=sa["alpha_tian"])
                    if v == "A": r.update({f"res_{a}": b for a, b in L.window_resid(p, f).items()})
                    L.save_npz_atomic(os.path.join(L.WORK, "w", f"{pf}_{v}.npz"), wb=f["wb"].astype(np.float32), wa=f["wa"].astype(np.float32), mpoly=f["mpoly"].astype(np.float32), chi2a=f["chi2a"])
                except Exception as ex: r["status"] = f"error: {ex}"
                r["sec"] = round(time.time() - t0, 1); L.append_jsonl(fo, r)
    sys.exit(0)

def merge(donors_only=False):
    S = L.sample(); P = json.load(open(os.path.join(HERE, "lam9_prepare.json"))); ok = sorted(r["plateifu"] for r in P["rows"] if r["step5"])
    if donors_only: ok = sorted(set(l.split(",")[2].strip() for l in donor_lines() if int(l.split(",")[1]) < 110))
    rows = []
    for fn in sorted(os.listdir(os.path.join(L.WORK, "fits"))):
        if fn.endswith(".jsonl"): rows += L.read_jsonl(os.path.join(L.WORK, "fits", fn), repair=True)
    OUTD = {}
    for v in ("A", "B"):
        R = {}
        for r in rows:
            if r["variant"] == v: assert r["plateifu"] not in R, f"duplicate fit {r['plateifu']} {v}"; R[r["plateifu"]] = r
        miss = [pf for pf in ok if pf not in R]; print(f"variant {v}: {len(R)} lines, missing {len(miss)}, errors {sum(1 for r in R.values() if r['status'] != 'ok')}", flush=True)
        if donors_only: OUTD[v] = [R[pf] for pf in sorted(R) if pf in ok]; continue
        name = f"lam9_fit_{v}.jsonl"; tmp = os.path.join(HERE, name + ".tmp")
        with open(tmp, "w") as fo:
            for pf in sorted(R):
                if pf in ok: fo.write(json.dumps(R[pf], default=float) + "\n")
        os.replace(tmp, os.path.join(HERE, name))
    if donors_only:
        fn = os.path.join(HERE, "lam9_fit_donors.json"); json.dump(dict(note="κ = ½ FITTED; not theory closed. The K donors' real fits (330 sums, variants A and B).", **OUTD),
                                                                  open(fn + ".tmp", "w", encoding="utf-8"), indent=0, ensure_ascii=False, default=float); os.replace(fn + ".tmp", fn)

if __name__ == "__main__":
    if "--prepare" in arg: prepare()
    elif "--merge" in arg: merge(donors_only="donors" in arg)
    else: run(opt("--phase", "all"), int(opt("--shard", "0")), int(opt("--nshard", "1")))
