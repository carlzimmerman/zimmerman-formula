#!/usr/bin/env python3
"""LD1 (FROZEN_CRITERIA.md d7db4e3403): late-decaying cold component (CLASS dcdm -> dr) against the CMB-lensing gate.
    python3 ld1.py            -> ld1.json / ld1.out
    python3 ld1.py --mutate   -> ld1_MUTATE.json / .out   (lifetime 0.2 Gyr: D1 must FAIL)
Read-only use of QX3 iter2 (CLASS + PR4 lensing), QX15 (theta), KD1 (kd1.json). kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.abspath(os.path.join(HERE, ".."))
MUT = "--mutate" in sys.argv; TAG = "ld1_MUTATE" if MUT else "ld1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
def load_prefix(path, marker, name):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}
    a = sys.argv; sys.argv = [path]
    try: exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a
    return ns
Q3 = load_prefix(os.path.join(CL, "QX3_cmb_growth", "iter2_kq_dust", "iter2.py"), 'if __name__ == "__main__":', "qx3_iter2_lib")
Q15 = json.load(open(os.path.join(CL, "QX15_cmb_primary_likelihood", "qx15.json")))
KD = json.load(open(os.path.join(CL, "KD1_unpinned_kq_dust", "kd1.json")))
Class, CHI2_LINE = Q3["Class"], Q3["CHI2_LINE"]
GYR_KMSMPC = 977.792          # 1/(km/s/Mpc) in Gyr

def run(ob, od, h, ns, tau, gam, cls=True):
    M = Class()
    p = {'h': h, 'omega_b': ob, 'n_s': ns, 'tau_reio': tau, 'A_s': Q3["AS0"], 'N_ur': 3.046, 'T_cmb': 2.7255}
    if gam > 0: p.update({'omega_cdm': 1e-7, 'omega_ini_dcdm': od, 'Gamma_dcdm': gam})
    else: p.update({'omega_cdm': od})
    if cls: p.update({'output': 'tCl,lCl', 'l_max_scalars': Q3["LMAX"] + 100})
    M.set(p); M.compute(); return M
def theta(M): return M.theta_s_100()
def survive(M):
    b = M.get_background(); z = b['z']; r = b['(.)rho_dcdm']
    i_hi = int(np.argmin(abs(z - 1e4))); i0 = int(np.argmin(abs(z)))
    return float(r[i0] / (r[i_hi] / (1 + z[i_hi]) ** 3))
def age(M): return float(M.age())

RES = dict(tag=TAG, criteria="d7db4e3403", note="TEST lane, adopts nothing. kappa = 1/2 FITTED; not theory closed", footings={})
P(f"LD1 {'MUTATE (lifetime 0.2 Gyr)' if MUT else 'MAIN'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")
for f in ("canonical", "alt"):
    th = Q15["footings"][f]["main"]["theta"]; h0 = float(Q15["footings"][f]["main"]["h"])
    ob, ns, tau, od = th["omega_b"], th["n_s"], th["tau"], th["omega_d"]
    ud = KD["footings"][f]["uniform_f_diag"]; Smax = ud["SPARC_f_max"] / ud["capture_f"]
    FO = dict(omega_b=ob, omega_d_ini=od, n_s=ns, tau=tau, h_QX15=h0, S_max=Smax)
    # KA: Gamma = 0 at QX15 h reproduces KD1 G9a
    M = run(ob, od, h0, ns, tau, 0.0); th0 = theta(M); c0, A0 = Q3["best_amp_chi2"](Q3["X_of"](M)); M.struct_cleanup()
    ref = KD["footings"][f]["G9a_shape"]["chi2_mu_inf"]; FO["KA"] = dict(chi2=float(c0), ref=ref, PASS=bool(abs(c0 - ref) <= 1e-3), theta_s_100=th0)
    P(f"[{f}] KA Gamma=0: chi2 {c0:.4f} vs KD1 {ref:.4f} -> {'PASS' if FO['KA']['PASS'] else 'FAIL'}; 100 theta_s {th0:.6f}")
    def h_for(gam):
        def g(h):
            M = run(ob, od, h, ns, tau, gam, cls=False); v = theta(M) - th0; M.struct_cleanup(); return v
        return brentq(g, 0.55, 1.4, xtol=1e-6)
    if MUT:
        t_life = 0.2
        gam = GYR_KMSMPC / t_life
    else:
        def sres(lg):
            gam = 10 ** lg; h = h_for(gam); M = run(ob, od, h, ns, tau, gam, cls=False); s = survive(M); M.struct_cleanup()
            return math.log(s) - math.log(Smax)
        lg = brentq(sres, 1.5, 2.6, xtol=1e-4); gam = 10 ** lg
    h = h0 if MUT else h_for(gam)        # MUTATE: theta_s cannot be held with the [0.55, 1.4] bracket at 0.2 Gyr; QX15 h used (disclosed)
    M = run(ob, od, h, ns, tau, gam)
    S = survive(M); tl = GYR_KMSMPC / gam; X = Q3["X_of"](M); c, A = Q3["best_amp_chi2"](X)
    cfix = None
    try:
        cfix = float(Q3["LIB"].qform(1.0 * (Q3["LIB"].wsum(Q3["D"]["W"], X) + Q3["LIB"].wsum(Q3["D"]["M"], X)) * (math.exp(th["lnAs1e10"]) / 1e10 / Q3["AS0"])
                                     - Q3["D"]["F"] - Q3["D"]["d"], Q3["D"]["Cinv"]))
    except Exception as e: cfix = f"n/a: {e}"
    FO.update(Gamma_kmsMpc=gam, lifetime_Gyr=tl, h=h, survive_today=S, age_Gyr=age(M), D1_chi2=float(c), A_refit_over_AS0=float(A),
              D2_chi2_As_fixed=cfix, D3_disc_and_cluster_f_today=ud["capture_f"] * S, D1_PASS=bool(c <= CHI2_LINE))
    M.struct_cleanup()
    P(f"[{f}] Gamma {gam:.3f} km/s/Mpc (lifetime {tl:.3f} Gyr), h {h:.5f}, surviving share {S:.4f} (S_max {Smax:.4f}), age {FO['age_Gyr']:.3f} Gyr")
    P(f"[{f}] D1 CMB-lensing chi2 {c:.3f} (line {CHI2_LINE}) A_s refit x {A:.4f} -> {'PASS' if FO['D1_PASS'] else 'FAIL'}; D2 fixed-A_s chi2 {cfix}")
    P(f"[{f}] D3 captured share today f = {FO['D3_disc_and_cluster_f_today']:.3f} (clusters need ~4.2: this class does not carry them)")
    RES["footings"][f] = FO
RES["label"] = ("MUTATE: D1 " + ("FAILS both -> BITES" if not any(RES["footings"][f]["D1_PASS"] for f in RES["footings"]) else "PASSES -> NO BITE")) if MUT else \
    ("D1 PASS both footings: late-decay escape at lensing level" if all(RES["footings"][f]["D1_PASS"] for f in RES["footings"]) else "FAIL")
P("LABEL: " + RES["label"])
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=str)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
