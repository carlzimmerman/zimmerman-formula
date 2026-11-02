#!/usr/bin/env python3
"""LW1 keys (FROZEN_CRITERIA.md): plain-law rows through NF1's grader via DR1's tail and SL1's driver, read only; own cache; BA1's R recomputed in the run. Resumes row by row: rerun after SIGTERM.
    python3 lw1_keys.py [tag ...]
kappa = 1/2 FITTED; not theory closed."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); DR1 = os.path.join(RB, "DR1_density_term_law")
ROWS = [["R1", 0, "canonical", None], ["R1", 0, "alt", None]]
RUNS = {"g005_f034": (0.005, "0.034", 1.0), "g005_f0615": (0.005, "0.0615", 1.0), "g0_f034": (0.0, "0.034", 1.0), "g0_f0615": (0.0, "0.0615", 1.0), "MUTATE_g005_f034": (0.005, "0.034", 1.5)}
GAS = "_x = '_g = \\'Mg500 = cl[\"Mgas500\"]*qd**2.5;\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl[\"Mgas500\"]*qd**2.5*%%r;\\' %% (10 ** %r))\\n'\nsub('NX = {\"__file__\": X30SRC,', _x + 'NX = {\"__file__\": X30SRC,')\n"
T = open(os.path.join(DR1, "dr1_tail.py")).read()
def rep(a, b, n=None):
    global T
    assert T.count(a) >= 1 and (n is None or T.count(a) == n), a; T = T.replace(a, b)
rep("A0[foot]", "_A0L[foot]"); rep("a0 = A0[f]", "a0 = _A0L[f]", 1); rep("import pickle as _pk, time as _tm\n", "import pickle as _pk, time as _tm\n_A0L = {k_: v_ * float(os.environ['LW1_A0X']) for k_, v_ in A0.items()}\n", 1)
rep('r["S_1p4Mpc_med"] =', 'r["tmpl"] = {hk_: {k_: list(v_) for k_, v_ in _tmpl(ft, hk_).items()} for hk_ in HK}; r["S_1p4Mpc_med"] =', 1)
BA = open(os.path.join(RB, "BA1_joint_shear_statistic", "ba1_worker_tail.py")).read(); i = BA.index("_N = N;"); j = BA.index("_OUT = {}"); BA = BA[i:j].replace("def _keys(", "def _bkeys(")
RT = BA + '''
_ROUT = {}
for f_ in ("canonical", "alt"):
    _ROUT[f_] = {}
    for h_ in HK:
        Kb = _bkeys(_Cb, f_, h_); Kj = _bkeys(_Jr, f_, h_); ks = list(Kb); Xb = np.array([Kb[k] for k in ks]); Xj = np.array([Kj[k] for k in ks]); nj = Xj.shape[1]; Dj = Xj - Xj.mean(1, keepdims=True); Cj = (nj - 1) / nj * Dj @ Dj.T
        _ROUT[f_][h_] = dict(keys=ks, R_boot=np.corrcoef(Xb).tolist(), R_jack=(Cj / np.sqrt(np.outer(np.diag(Cj), np.diag(Cj)))).tolist())
_RES["R"] = _ROUT; _save()
'''
rep('_RES["done"] = True;', RT + '_RES["done"] = True;', 1)
if __name__ == "__main__":
    for tag in (sys.argv[1:] or RUNS):
        dex, fs, ax = RUNS[tag]; W = os.path.join(HERE, f"cache_{tag}"); os.makedirs(W, exist_ok=True); O = os.path.join(HERE, f"lw1_keys_{tag}.json")
        if os.path.exists(O) and json.load(open(O)).get("done"): print(tag, "done"); continue
        TL = os.path.join(W, "lw1_tail.py"); open(TL, "w").write(T)
        d = open(os.path.join(SL1, "sl1_harvest.py")).read()
        for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(GAS % dex if dex else "") + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(TL)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('X73_FSTAR="0.034"', f'X73_FSTAR="{fs}"')):
            assert d.count(a) == 1, a; d = d.replace(a, b)
        df = os.path.join(W, "lw1_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", LW1_A0X=str(ax), DR1_RUN=json.dumps(dict(rows=ROWS, k2=False)))
        p = subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(W, "run.log"), "w"), stderr=subprocess.STDOUT)
        print(tag, p.returncode, flush=True)
