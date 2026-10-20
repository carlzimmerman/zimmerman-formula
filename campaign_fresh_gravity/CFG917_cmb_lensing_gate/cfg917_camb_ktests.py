#!/usr/bin/env python3
"""CFG917 K3d / K3e (FROZEN_CRITERIA.md B4, commit 0289e4ad4): code and normalisation checks that need CAMB.  One process, < 1 GB.

K3d  Limber normalisation: this lane's Limber code fed with the NATIVE linear spectrum (IC table Plin0 x native D^2, native background)
     vs CAMB 1.6.6's LINEAR C_L^phiphi at the native parameters, binned with the PR4 windows: <= 3% in every band.
     (Linear CAMB is the framework-native IC generator of CFG654 section 1; here a normalisation check only.)
K3e  the package's own unit-test value -2 lnL = 8.368 (PlanckPR4LensingMarged) from CAMB at the unit-test parameters with
     lens_potential_accuracy 1 and halofit 'mead', exactly as the package's test: reproduced by this lane's likelihood code to <= 0.15.
     The CAMB/halofit spectrum is a CODE-TEST input only; it enters no model, no dchi2 and no verdict.
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg917_camb_ktests.py   -> cfg917_camb_ktests.out / .json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cfg917_lib as LB
import camb

T0 = time.time(); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P(f"CFG917 CAMB K-tests (K3d normalisation, K3e package unit test); CAMB {camb.__version__}")
D = LB.load_pr4(); RES = dict(lane="CFG917", part="camb_ktests", criteria_commit="0289e4ad4", camb=camb.__version__)

# ---------------- K3d: native linear normalisation
T = np.load(os.path.join(LB.C654, "cfg654_ics_tables_cmb.npz"))
h = float(T["h"]); As = float(T["As"]); ns = float(T["ns"])
p = camb.CAMBparams()
p.set_cosmology(ombh2=float(T["omega_b"]), omch2=float(T["omega_c"]), omk=0.0, mnu=0.0, num_massive_neutrinos=0, nnu=3.044, TCMB=2.7255,
                tau=0.0544, H0=100 * h)
p.InitPower.set_params(As=As, ns=ns, pivot_scalar=0.05)
p.set_dark_energy(w=-1.0, wa=0.0)
p.set_for_lmax(LB.LMAX, lens_potential_accuracy=1)
p.NonLinear = camb.model.NonLinear_none
r = camb.get_results(p)
pp = r.get_lens_potential_cls(LB.LMAX)[:, 0]                  # [L(L+1)]^2 C_L / 2pi
Xc = np.zeros(LB.LMAX + 1); Xc[:len(pp)] = pp[:LB.LMAX + 1]
inp = LB.Inputs("native_cmb")
zg = LB.zgrid()
Xl = LB.limber_X(lambda k, a, z: inp.Plin0(k) * inp.D(a) ** 2, inp, zg, inp.Om)
bc, bl = LB.wsum(D["W"], Xc), LB.wsum(D["W"], Xl)
dev = bl / bc - 1
ok3d = bool(np.all(np.abs(dev) <= 0.03))
P("K3d per band (this Limber / CAMB linear - 1): " + " ".join(f"{x:+.4f}" for x in dev) + f"  -> {'PASS' if ok3d else 'FAIL'} (<= 0.03)")
P(f"     context: chi_* native = {inp.chi_star:.1f} Mpc/h; CAMB linear binned band 2 = {bc[1]:.4e}")
RES["K3d"] = dict(ok=ok3d, dev=dev.tolist(), camb_binned=bc.tolist(), limber_binned=bl.tolist(), chi_star=inp.chi_star,
                  params=dict(omega_b=float(T["omega_b"]), omega_c=float(T["omega_c"]), h=h, As=As, ns=ns, mnu=0.0, nnu=3.044, nonlinear="none"))

# ---------------- K3e: the package's unit test (tests/tests_pr4lensing.py test_indep, CMB-marginalised value 8.368)
camb_params = {"ombh2": 0.022274, "omch2": 0.11913, "cosmomc_theta": 0.01040867, "As": 0.2132755716e-8, "ns": 0.96597, "tau": 0.0639}
opts = camb_params.copy(); opts["lens_potential_accuracy"] = 1; opts["lmax"] = LB.LMAX; opts["halofit_version"] = "mead"
pars = camb.set_params(**opts); res = camb.get_results(pars)
pp2 = res.get_lens_potential_cls(LB.LMAX)[:, 0]
Xt = np.zeros(LB.LMAX + 1); Xt[:len(pp2)] = pp2[:LB.LMAX + 1]
chi2 = LB.pr4_chi2(D, Xt)
ok3e = abs(chi2 - 8.368) <= 0.15
P(f"K3e package unit test: -2 lnL (PlanckPR4LensingMarged) = {chi2:.4f} vs published test value 8.368 -> {'PASS' if ok3e else 'FAIL'} (<= 0.15)")
P("     (CAMB + halofit 'mead' spectrum: code-test input only; enters no model, no dchi2, no verdict)")
RES["K3e"] = dict(ok=bool(ok3e), chi2=chi2, reference=8.368, tol=0.15, params=opts)
RES["runtime_s"] = time.time() - T0
try:
    import resource; RES["maxrss_gb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
except Exception:
    pass
P(f"runtime {RES['runtime_s']:.0f} s; maxrss {RES.get('maxrss_gb', 0):.2f} GB. kappa = 1/2 FITTED; not theory closed.")
base = os.path.join(LB.HERE, "cfg917_camb_ktests")
json.dump(RES, open(base + ".json", "w"), indent=1); open(base + ".out", "w").write("\n".join(OUT) + "\n")
