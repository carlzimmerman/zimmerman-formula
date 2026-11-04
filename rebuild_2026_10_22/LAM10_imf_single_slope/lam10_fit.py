"""LAM10 full fits (criteria e70770e272), run only if K1 passes: one single-slope chi2 profile per sum and variant (A, then B)
for LAM9's 1586 step-5 galaxies. Each sum is fitted once; failures counted, never refit. Job contract as LAM9's runner.
  python3 -I lam10_fit.py --shard K --nshard N [--resume]
  python3 -I lam10_fit.py --merge                      lam10_fits.json in this folder
κ = ½ FITTED; not theory closed."""
import os, sys, json, signal, time, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
warnings.filterwarnings("ignore", message=".*encountered in matmul", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import lam10_core as C
L9 = C.L9
QY = os.path.join(L9.ROOT, "compute_queue", "YIELD"); FD = os.path.join(C.WORK, "fits"); os.makedirs(FD, exist_ok=True)
stop = False
def _term(*_):
    global stop; stop = True
signal.signal(signal.SIGTERM, _term); signal.signal(signal.SIGINT, _term)
arg = sys.argv[1:]
def opt(k, d=None): return arg[arg.index(k) + 1] if k in arg else d
def jobs(): return sorted(r["plateifu"] for r in json.load(open(os.path.join(C.L9DIR, "lam9_prepare.json")))["rows"] if r["step5"])

def run(k, nk):
    S = L9.sample(); wave, narrow = L9.load_stack(); out = os.path.join(FD, f"lam10_fit.s{k}of{nk}.jsonl"); L9.read_jsonl(out, repair=True)
    D = {}
    for fn in os.listdir(FD):
        if fn.endswith(".jsonl"):
            for r in L9.read_jsonl(os.path.join(FD, fn)): D.setdefault(r["plateifu"], {})[r["variant"]] = r
    mine = [j for n_, j in enumerate(jobs()) if n_ % nk == k]; todo = [j for j in mine if not ("A" in D.get(j, {}) and "B" in D.get(j, {}))]
    print(f"shard {k}/{nk}: {len(mine)} jobs, {len(todo)} to do", flush=True)
    if not todo: sys.exit(0)
    with open(out, "a") as fo:
        for pf in todo:
            if stop or os.path.exists(QY): print("yield: exit 75", flush=True); fo.close(); sys.exit(75)
            t0 = time.time(); kin = S["FIT"][pf]; p = L9.prep(S["path"][pf], narrow); tpl, lam_t, n_t = L9.templates_for(p)
            for v in ("A", "B"):
                if v in D.get(pf, {}): continue
                r = dict(plateifu=pf, variant=v, z=p["z"], ngood=int(len(p["goodA"] if v == "A" else p["goodB"])))
                try: r.update(status="ok", **C.profile(p, tpl, lam_t, n_t, kin, v))
                except Exception as ex: r["status"] = f"error: {ex}"
                r["sec"] = round(time.time() - t0, 1); L9.append_jsonl(fo, r)
    sys.exit(0)

def merge():
    rows = []
    for fn in sorted(os.listdir(FD)):
        if fn.endswith(".jsonl"): rows += L9.read_jsonl(os.path.join(FD, fn), repair=True)
    out = {}
    for v in ("A", "B"):
        R = {}
        for r in rows:
            if r["variant"] == v: assert r["plateifu"] not in R, f"duplicate {r['plateifu']} {v}"; R[r["plateifu"]] = r
        miss = [p for p in jobs() if p not in R]; print(f"variant {v}: {len(R)}, missing {len(miss)}, errors {sum(1 for r in R.values() if r['status'] != 'ok')}", flush=True)
        out[v] = [R[p] for p in sorted(R)]
    fn = os.path.join(HERE, "lam10_fits.json")
    json.dump(dict(note="κ = ½ FITTED; not theory closed. LAM10 single-slope profile fits, variants A and B.", **out), open(fn + ".tmp", "w", encoding="utf-8"),
              indent=0, ensure_ascii=False, default=float); os.replace(fn + ".tmp", fn)

if __name__ == "__main__":
    merge() if "--merge" in arg else run(int(opt("--shard", "0")), int(opt("--nshard", "1")))
