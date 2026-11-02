#!/usr/bin/env python3
"""LM1 grader driver (FROZEN_CRITERIA.md): the plain law through NF1's grader via DR1's tail and SL1's driver, read only, as LW1. Dumps per-cluster law and Newton vectors. Own cache; each job resumes: rerun after SIGTERM.
    python3 lm1_grade.py [job ...]
kappa = 1/2 FITTED; not theory closed."""
import json, os, subprocess, sys
import numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); DR1 = os.path.join(RB, "DR1_density_term_law"); M3 = os.path.join(RB, "M3A1_outer_key_audit")
ROWS = [["R1", 0, "canonical", None], ["R1", 0, "alt", None]]
# job: f*, a0 factor, per-cluster gas factor file or None
RUNS = {"BASE_f034": ("0.034", 1.0, None), "BASE_f0615": ("0.0615", 1.0, None), "C1aM3_f034": ("0.034", 1.0, os.path.join(M3, "m3a1_factor_C1a_M3.json")), "C1acapall_f034": ("0.034", 1.0, os.path.join(HERE, "lm1_factor_C1a_capall.json")), "C2a_f034": ("0.034", 1.0, os.path.join(M3, "m3a1_factor_C2a.json")), "MUTATE_f034": ("0.034", 1.5, None)}
def capfile():
    X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); names = [str(x).strip() for x in X["name"]]
    E = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data; EN = [str(s).strip() for s in E["NAME"]]; ix = {n: i for i, n in enumerate(EN)}; J = np.array([ix[n] for n in names]); mg, lo, hi = (np.asarray(E[k], float) for k in ("MGAS500", "MGAS500_L", "MGAS500_H"))
    with np.errstate(all="ignore"):
        sig = 0.5 * (np.log10(mg[J] / lo[J]) + np.log10(hi[J] / mg[J])); good = np.isfinite(sig)
    F = json.load(open(os.path.join(M3, "m3a1_factor_C1a.json"))); O = {n: (float(F[n]) if (g and s <= 0.2) else 1.0) for n, g, s in zip(names, good, sig)}
    json.dump(O, open(os.path.join(HERE, "lm1_factor_C1a_capall.json"), "w"), indent=0)
T = open(os.path.join(DR1, "dr1_tail.py")).read()
def rep(a, b, n=None):
    global T
    assert T.count(a) >= 1 and (n is None or T.count(a) == n), a; T = T.replace(a, b)
rep("A0[foot]", "_A0L[foot]"); rep("a0 = A0[f]", "a0 = _A0L[f]", 1); rep("import pickle as _pk, time as _tm\n", "import pickle as _pk, time as _tm\n_A0L = {k_: v_ * float(os.environ['LM1_A0X']) for k_, v_ in A0.items()}\n", 1)
rep('r["S_1p4Mpc_med"] =', 'r["tmpl"] = {hk_: {k_: list(v_) for k_, v_ in _tmpl(ft, hk_).items()} for hk_ in HK}; r["S_1p4Mpc_med"] =', 1)
DUMP = r'''
_RCv = np.asarray(NX["RC"] if "RC" in NX else NX["NS2"]["RC"], float); _D = {"RC": _RCv, "T3M": NX["T3M"], "TID": NX["TID"], "I": NX["I"], "PATCH": NX["PATCH"], "MPC": float(NX["MPC"])}
_LAW.update(rd="R1", c=0, mut=None, on=True)
for f_ in ("canonical", "alt"):
    for hk in HK:
        V_ = np.zeros((N, 8)); VN = np.zeros((N, 8)); MB_ = np.zeros((N, 8)); ML_ = np.zeros((N, 8)); R5 = np.zeros(N); Mt = np.zeros(N)
        for i in ALLI:
            i = int(i); pp = prep(i, f_, hk); m_, _s = _msrc(pp["Mb"], f_); V_[i] = _dv0(i, f_, hk, m_); VN[i] = _dv0(i, f_, hk, pp["Mb"]); rr_ = _RCv * float(NX["MPC"]); MB_[i] = np.interp(rr_, RM, pp["Mb"]) / MSUNE; ML_[i] = np.interp(rr_, RM, m_) / MSUNE; R5[i] = float(pp["R500"]); Mt[i] = float(pp["Mb"][-1]) / MSUNE
        PREP.clear()
        q = f"{f_}_{hk}"; _D["V_" + q] = V_; _D["VN_" + q] = VN; _D["Mb_" + q] = MB_; _D["ML_" + q] = ML_; _D["R500_" + hk] = R5; _D["vC_" + q] = DC_[(f_, hk)]; _D["n_" + q] = NX["MEAS"][(f_, hk)]["n"]
    a0_ = _A0L[f_]; _g = []
    for o in GROUPS:
        Mb_ = 10 ** o["lM"] * MS540; a_ = o["Re"] * KP540 / HERN_RE; re_ = o["Re"] * KP540; Min = Mb_ * re_ ** 2 / (re_ + a_) ** 2; gN = G540 * Min / re_ ** 2; u = G540 * Mb_ / a_ ** 2; gb = M_H / XG ** 2 * u; g = _comb(gb, gb, a0_, "R1") / u; s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * g * XG, LXG) / 3.0) * G540 * Mb_ / a_
        _g.append([o["ls"], 0.5 * math.log10(s2) - 3.0, o["els"], o["lM"], o["Re"], gN / a0_, float(0.5 * gN + math.sqrt(0.25 * gN ** 2 + a0_ * gN)) * re_ ** 2 / G540 / MS540, Min / MS540])
    _D["groups_" + f_] = np.array(_g)
np.savez_compressed(os.environ["LM1_DUMP"], **_D)
'''
rep('_RES["done"] = True;', DUMP + '_RES["done"] = True;', 1)
if __name__ == "__main__":
    capfile()
    for tag in (sys.argv[1:] or RUNS):
        fs, ax, fac = RUNS[tag]; W = os.path.join(HERE, f"cache_{tag}"); os.makedirs(W, exist_ok=True); O = os.path.join(W, "keys.json"); D = os.path.join(W, "dump.npz")
        if os.path.exists(O) and os.path.exists(D) and json.load(open(O)).get("done"): print(tag, "done", flush=True); continue
        if fac:
            GAS = f"""_x = '_g = \\'Mg500 = cl["Mgas500"]*qd**2.5;\\'\\nassert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl["Mgas500"]*qd**2.5*\\' + repr(10 ** 0.005) + \\'*LM1F[cl["name"]];\\'); codeX = codeX.replace("PREP = {{}}\\\\n", "PREP = {{}}\\\\nimport json as _jj; LM1F = _jj.load(open(%r))\\\\n", 1)\\n' % {fac!r}
sub('NX = {{"__file__": X30SRC,', _x + 'NX = {{"__file__": X30SRC,')
"""
        else:
            GAS = "_x = '_g = \\'Mg500 = cl[\"Mgas500\"]*qd**2.5;\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl[\"Mgas500\"]*qd**2.5*%%r;\\' %% (10 ** %r))\\n'\nsub('NX = {\"__file__\": X30SRC,', _x + 'NX = {\"__file__\": X30SRC,')\n" % 0.005
        TL = os.path.join(W, "lm1_tail.py"); open(TL, "w").write(T); d = open(os.path.join(SL1, "sl1_harvest.py")).read()
        for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(GAS) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(TL)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('X73_FSTAR="0.034"', f'X73_FSTAR="{fs}"')):
            assert d.count(a) == 1, a; d = d.replace(a, b)
        df = os.path.join(W, "lm1_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, LM1_DUMP=D, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", LM1_A0X=str(ax), DR1_RUN=json.dumps(dict(rows=ROWS, k2=False)))
        p = subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(W, "run.log"), "w"), stderr=subprocess.STDOUT)
        print(tag, p.returncode, flush=True)
