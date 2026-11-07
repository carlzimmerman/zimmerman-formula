#!/usr/bin/env python3
"""HC1 G9 (criteria c207d70254): CMB-lensing SHAPE with the fixed thermal fermion as the only non-baryonic matter.
QX3 iter2's G1 statistic exactly (cfg917_lib read-only: raw PR4 lensing, 9 bandpowers, binning; A_s fitted analytically),
8 corners, fermion m = 93.14 eV x 0.11958060 (fixed), omega_cdm = 0.
    python3 hc1_g9.py           -> hc1_g9.json / .out   (KA5, then the fermion)
    python3 hc1_g9.py --mutate  -> hc1_g9_MUTATE.json / .out  (baryons only; must FAIL every corner)
EXPERIMENT: adopts nothing; no-particle rule lifted for HC1 only. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, itertools
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity/CFG917_cmb_lensing_gate"))
import cfg917_lib as LIB
from classy import Class
MUT = "--mutate" in sys.argv; TAG = "hc1_g9_MUTATE" if MUT else "hc1_g9"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
D = LIB.load_pr4(); LMAX = LIB.LMAX; Larr = np.arange(LMAX + 1.0); AS0 = 2.0e-9; LINE = 18.48
OMF = 0.11958060485606123; M_EV = 93.14 * OMF; TNCDM = 0.71611
Q3 = json.load(open(os.path.join(REPO, "closure_2026_11_06/QX3_cmb_growth/iter2_kq_dust/iter2.json")))

def run(ob, H0, ns, mode, od=None, pk=False):
    p = {'output': 'tCl,lCl,mPk' if pk else 'tCl,lCl', 'l_max_scalars': LMAX + 100, 'h': H0 / 100, 'omega_b': ob, 'A_s': AS0,
         'n_s': ns, 'tau_reio': 0.06, 'N_ur': 3.046, 'T_cmb': 2.7255}
    if mode == "dust": p['omega_cdm'] = od
    elif mode == "baryons": p['omega_cdm'] = 1e-7
    else:
        p.update({'omega_cdm': 1e-7, 'N_ncdm': 1, 'm_ncdm': M_EV, 'T_ncdm': TNCDM, 'deg_ncdm': 1.0,
                  'ncdm_fluid_approximation': 3, 'tol_ncdm_bg': 1e-10})
    if pk: p.update({'P_k_max_1/Mpc': 3.0, 'z_max_pk': 3.0})
    M = Class(); M.set(p); M.compute(); return M
def chi2_amp(M):
    pp = M.raw_cl(LMAX)['pp']; X = (Larr * (Larr + 1)) ** 2 * pp / (2 * np.pi)
    u = LIB.wsum(D["W"], X) + LIB.wsum(D["M"], X); a = LIB.qform(u, D["Cinv"], D["d"] + D["F"]); b = LIB.qform(u, D["Cinv"]); A = a / b
    r = A * u - D["F"] - D["d"]; return float(LIB.qform(r, D["Cinv"])), float(A), (A * u).tolist(), (D["d"] + D["F"]).tolist()

RES = dict(tag=TAG, criteria="c207d70254", m_eV=M_EV, omega_f=OMF, note="EXPERIMENT; adopts nothing; no-particle rule lifted for HC1 only. kappa = 1/2 FITTED; not theory closed")
P(f"HC1 G9 {'MUTATE (baryons only)' if MUT else 'MAIN'}: m {M_EV:.4f} eV, T_ncdm {TNCDM}, deg 1, omega_f target {OMF:.5f}. kappa = 1/2 FITTED; not theory closed.")
# KA5
c0 = Q3["G1"][0]; Md = run(0.0215, 65.0, 0.95, "dust", od=c0["omega_d_best"]); cd, _, _, _ = chi2_amp(Md); Md.struct_cleanup()
Mb = run(0.0215, 65.0, 0.95, "baryons"); cb, _, _, _ = chi2_amp(Mb); Mb.struct_cleanup()
Mf = run(0.0215, 65.0, 0.95, "fermion"); onc = float(Mf.Omega_nu * (0.65 ** 2)) if hasattr(Mf, "Omega_nu") else float("nan")
try: onc = float(Mf.get_current_derived_parameters(['Omega_ncdm_tot'])['Omega_ncdm_tot']) * 0.65 ** 2
except Exception: pass
Mf.struct_cleanup()
ka = dict(dust_chi2=cd, dust_rec=c0["chi2_min"], baryons_chi2=cb, baryons_rec=c0["mutate_baryons_only_chi2"], omega_ncdm=onc,
          ok=bool(abs(cd - c0["chi2_min"]) <= 1e-3 and abs(cb - c0["mutate_baryons_only_chi2"]) <= 1e-3 and abs(onc / OMF - 1) <= 0.01))
RES["KA5"] = ka
P(f"KA5 dust chi2 {cd:.4f} (rec {c0['chi2_min']:.4f}); baryons only {cb:.2f} (rec {c0['mutate_baryons_only_chi2']:.2f}); CLASS omega_ncdm {onc:.5f} (target {OMF:.5f}) -> {'PASS' if ka['ok'] else 'FAIL'}")
if not ka["ok"]:
    P("KA5 FAIL: stop, nothing graded."); json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1); open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)
rows = []
for ob, H0, ns in itertools.product((0.0215, 0.0230), (65.0, 75.0), (0.95, 0.98)):
    M = run(ob, H0, ns, "baryons" if MUT else "fermion"); c, A, mod, dat = chi2_amp(M)
    row = dict(omega_b=ob, H0=H0, n_s=ns, chi2=c, A_s_implied=A * AS0, model_bp=mod, data_bp=dat, ratio_bp=[m_ / d_ for m_, d_ in zip(mod, dat)])
    if not MUT:
        Mdd = run(ob, H0, ns, "dust", od=OMF); cdd, Ad, modd, _ = chi2_amp(Mdd); Mdd.struct_cleanup()
        row.update(dust_same_omega_chi2=cdd, fermion_over_dust_bp=[a / b for a, b in zip(mod, modd)])
        Mp = run(ob, H0, ns, "fermion", pk=True); Mq = run(ob, H0, ns, "dust", od=OMF, pk=True); h = H0 / 100
        row["Pk_ratio_z0_fermion_over_dust"] = {str(k): float(Mp.pk_lin(k * h, 0.0) / Mq.pk_lin(k * h, 0.0)) for k in (0.01, 0.03, 0.1, 0.27, 1.0)}
        row["sigma8_fermion_unscaled_As2e-9"] = float(Mp.sigma8()); row["sigma8_dust_unscaled_As2e-9"] = float(Mq.sigma8())
        Mp.struct_cleanup(); Mq.struct_cleanup()
    M.struct_cleanup(); rows.append(row)
    P(f"  corner ob {ob} H0 {H0:g} ns {ns}: chi2 {c:.2f} (line {LINE}), A_s {A * AS0:.3e}; model/data per bandpower {[round(x, 3) for x in row['ratio_bp']]}"
      + ("" if MUT else f"; dust at the same omega {cdd:.2f}; fermion/dust bp {[round(x, 3) for x in row['fermion_over_dust_bp']]}; P(k) fermion/dust z0 {[(k, round(v, 3)) for k, v in row['Pk_ratio_z0_fermion_over_dust'].items()]}"))
RES["corners"] = rows; worst = max(r["chi2"] for r in rows); best = min(r["chi2"] for r in rows); RES["worst_chi2"] = worst; RES["best_chi2"] = best
if MUT:
    bites = all(r["chi2"] > LINE for r in rows); RES["MUTATE_bites"] = bites
    P(f"MUTATE baryons only: min chi2 {best:.1f} -> {'BITES (every corner > 18.48)' if bites else 'NO BITE'}")
else:
    RES["G9"] = "PASS" if worst <= LINE else "FAIL"
    P(f"G9 CMB lensing shape: worst corner chi2 {worst:.2f}, best {best:.2f}, line {LINE} -> {RES['G9']} (footing-free: linear CLASS has no a0 term)")
P("EXPERIMENT; adopts nothing; no-particle rule lifted for HC1 only. kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1); open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (not MUT or RES["MUTATE_bites"]) else 1)
