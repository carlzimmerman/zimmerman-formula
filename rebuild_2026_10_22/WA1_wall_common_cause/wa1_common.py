#!/usr/bin/env python3
"""WA1 common: RQ3's acceptance.py loaded with caches redirected here, logic unedited; candidates; priors. kappa = 1/2 FITTED; not theory closed."""
import importlib.util, json, math, os, sys, types
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
try: os.nice(19)
except OSError: pass
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); RQ = os.path.join(RB, "RQ3_acceptance_v2")
CANDS = dict(LAW=os.path.join(RQ, "candidates", "law.py"), UX3=os.path.join(RQ, "candidates", "ux3_term.py"), P3=os.path.join(RB, "BF2_near_miss_family", "candidates", "P3.py"), P7=os.path.join(RB, "BF2_near_miss_family", "candidates", "P7.py"), MX1=os.path.join(RB, "MX1_max_rule", "cand_P.py"), BK2=os.path.join(HERE, "cand_bk2.py"), CAL=os.path.join(RQ, "candidates", "cold_halo.py"))
KEYC = dict(LAW=(os.path.join(RQ, "cache_keys"), "law"), UX3=(os.path.join(RQ, "cache_keys"), "ux3_term"), P3=(os.path.join(RB, "BF2_near_miss_family", "cache_keys"), "P3"), P7=(os.path.join(RB, "BF2_near_miss_family", "cache_keys"), "P7"), MX1=(os.path.join(RB, "MX1_max_rule", "acc", "cache_keys"), "cand_P"), BK2=(os.path.join(HERE, "cache_k2"), "BK2"))
SCORE = dict(LAW=os.path.join(RQ, "results", "law.json"), UX3=os.path.join(RQ, "results", "ux3_term.json"), P3=os.path.join(RB, "BF2_near_miss_family", "results", "P3.json"), P7=os.path.join(RB, "BF2_near_miss_family", "results", "P7.json"), MX1=os.path.join(RB, "MX1_max_rule", "acc", "results", "cand_P.json"), CAL=os.path.join(RQ, "results", "cold_halo.json"))
FEET = ("canonical", "alt"); REAL = ("LAW", "UX3", "P3", "P7", "MX1", "BK2")
# centre, sigma; physical units per FROZEN_CRITERIA.md section 2
NUIS = dict(ups=(0.0, 0.10), hse=(0.06, 0.06), gas_abs=(0.0, 0.02), gas_rel=(0.005, 0.017), carry=(2.7774425603108597, 0.20), tilt=(-0.10, 0.10), dist=(0.0, 0.03), lens=(0.0, 0.03), fstar=(0.04775, 0.01375))
NN = list(NUIS); RHO = dict(ups_fstar=0.5)
def prior_corr():
    P = np.eye(len(NN)); i, j = NN.index("ups"), NN.index("fstar"); P[i, j] = P[j, i] = RHO["ups_fstar"]; return P
def phys(theta):
    """theta dict in sigma -> physical"""
    return {k: NUIS[k][0] + NUIS[k][1] * float(theta.get(k, 0.0)) for k in NUIS}
def load_acc():
    if "wa1_acc" in sys.modules: return sys.modules["wa1_acc"]
    p = os.path.join(RQ, "acceptance.py"); s = open(p).read(); OUTD = os.path.join(HERE, "acc"); os.makedirs(OUTD, exist_ok=True)
    a = 'HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO'; assert s.count(a) == 1; s = s.replace(a, f'OUTD = {OUTD!r}; ' + a)
    for x in ('os.path.join(HERE, "cache_crg"', 'os.path.join(HERE, f"cache_keys"', 'os.path.join(HERE, "results"', 'os.path.join(HERE, "cache_keys"'):
        s = s.replace(x, x.replace("HERE,", "OUTD,"))
    m = types.ModuleType("wa1_acc"); m.__file__ = p; sys.modules["wa1_acc"] = m; sys.path.insert(0, RQ); exec(compile(s, p, "exec"), m.__dict__); return m
def load_cand(cid):
    p = CANDS[cid]; sp = importlib.util.spec_from_file_location("cand_" + cid, p); c = importlib.util.module_from_spec(sp); sp.loader.exec_module(c); return c
