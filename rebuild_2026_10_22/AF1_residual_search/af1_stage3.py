#!/usr/bin/env python3
"""AF1 stage 3 fit: PySR on Stage 2's survivors with full coverage. job = canonical | alt | scrambled | planted. One thread. Resume: a job with a finished hof csv exits 0; killed job restarts from scratch (SIGTERM stops at once, nothing partial is read).
Features z-scored on train. Holdouts never enter. kappa = 1/2 FITTED; not theory closed."""
import csv, hashlib, json, os, sys, time
os.environ["JULIA_NUM_THREADS"] = "1"; os.environ["PYTHON_JULIACALL_THREADS"] = "1"
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SAMPLES = ["SPARC", "LT", "groups", "XCOP", "shearM", "dwarfs", "MW"]; FEAT = ["ly", "ly_star", "lell", "m_sys"]; SEED = 20261102; NIT = int(os.environ.get("AF1_NIT", 150))
def load(foot):
    R = [x for x in csv.DictReader(open(os.path.join(HERE, f"af1_table_{foot}.csv"))) if x["sample"] in SAMPLES]; g = lambda k: np.array([float(x[k]) if x[k] != "" else np.nan for x in R]); D = dict(sample=np.array([x["sample"] for x in R]), system=np.array([x["system"] for x in R]), r=g("r"), sig=g("sigma_r"), ly=np.log10(g("y")), ly_star=np.log10(np.maximum(g("y_star"), 1e-12)), lell=np.log10(g("ell")), m_sys=g("m_sys"), f=g("f_gas"), y_gas=g("y_gas"))
    D["train"] = np.array([int(hashlib.sha256(x["split_id"].encode()).hexdigest(), 16) % 2 == 0 for x in R]); s = np.nan_to_num(D["sig"], nan=.1); w = 1 / (s ** 2 + .05 ** 2)
    for q in SAMPLES:
        for t in (True, False):
            m = (D["sample"] == q) & (D["train"] == t); w[m] /= w[m].sum() if m.any() else 1
    D["w"] = w; X = np.column_stack([D[k] for k in FEAT]); tr = D["train"]; mu = np.average(X[tr], axis=0, weights=w[tr]); sd = np.sqrt(np.average((X[tr] - mu) ** 2, axis=0, weights=w[tr])); D["X"] = (X - mu) / sd; D["mu"] = mu; D["sd"] = sd; return D
def main(job):
    foot = "alt" if job == "alt" else "canonical"; O = os.path.join(HERE, "pysr_runs", job); os.makedirs(O, exist_ok=True); SUF = os.environ.get("AF1_SUF", ""); O += SUF; os.makedirs(O, exist_ok=True); F = os.path.join(HERE, f"af1_hof_{job}{SUF}.csv")
    if os.path.exists(F): print(job, "done"); return
    D = load(foot); tr = D["train"]; X = D["X"][tr]; y = D["r"][tr].copy(); w = D["w"][tr] / D["w"][tr].mean(); g = np.random.default_rng(SEED)
    if job == "scrambled":
        sy = D["system"][tr]; sm = D["sample"][tr]
        for s in SAMPLES:  # target of a system handed to another system's rows inside the sample: sample means kept
            m = np.nonzero(sm == s)[0]; u = np.unique(sy[m])
            if len(u) >= 5: mp = dict(zip(u, g.permutation(u))); y[m] = np.array([g.choice(y[m][sy[m] == mp[a]]) for a in sy[m]])
            else: y[m] = g.permutation(y[m])
    if job == "planted": y = 0.2 * X[:, 0] ** 2 - 0.3 * X[:, 2] + 0.1 + g.normal(0, .1, len(y))
    from pysr import PySRRegressor
    t0 = time.time(); m = PySRRegressor(niterations=NIT, populations=12, population_size=33, maxsize=25, maxdepth=10, binary_operators=["+", "-", "*", "/"], unary_operators=["exp", "log", "sqrt", "square"], nested_constraints={"exp": {"exp": 0, "log": 1}, "log": {"log": 0, "exp": 1}, "sqrt": {"sqrt": 0}}, complexity_of_constants=1, elementwise_loss="L2DistLoss()", parallelism="serial", deterministic=True, random_state=SEED, progress=False, verbosity=0, output_directory=O, run_id="r", procs=0)
    m.fit(X, y, weights=w, variable_names=[f"z_{k}" for k in FEAT]); H = m.equations_
    tmp = F + ".tmp"; H[["complexity", "loss", "equation"]].to_csv(tmp, index=False); os.replace(tmp, F); json.dump(dict(mu=D["mu"].tolist(), sd=D["sd"].tolist(), feat=FEAT, seconds=time.time() - t0, nit=NIT, n_train=int(tr.sum())), open(os.path.join(HERE, f"af1_hof_{job}{SUF}.json"), "w"), indent=1); print(job, "finished", time.time() - t0)
main(sys.argv[1])
