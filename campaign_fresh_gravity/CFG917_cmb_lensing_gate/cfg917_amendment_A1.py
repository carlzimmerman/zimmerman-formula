#!/usr/bin/env python3
"""CFG917 ADDENDUM A1 (POST HOC, commit 187f895aa): K3b' replaces the frozen K3b, then the frozen class and the A1 class of every scored
pair are tabulated side by side, with Part A's CFG649 label and the gate reading (FROZEN_CRITERIA.md 'Scope and reading').

K3b'(i)  the PS1 (non-marginalised) fiducial correction = the full linear-correction windows (TT, EE, TE, PP) applied to the FFP10 lensed
         CMB + PP spectra, <= 2% per band (FFP10 is the correction's fiducial; windows read correctly).
K3b'(ii) this lane's likelihood code reproduces the package's PS1 unit-test value 8.705 (CAMB 1.6.6, unit-test parameters, halofit
         'mead', exactly as the package's test; code-test input only, enters no model or verdict) to <= 0.15.
Reads cfg917_<PAIR>.json / cfg917_<PAIR>_MUTATE.json / cfg917_partA_<PAIR>.json; never rewrites them.
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg917_amendment_A1.py   -> cfg917_A1_classes.out / .json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cfg917_lib as LB

OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P("CFG917 ADDENDUM A1 (POST HOC): K3b' and the frozen / A1 classes side by side")
D = LB.load_pr4(); Xf = LB.load_ffp10()
Fps1 = np.loadtxt(os.path.join(LB.PR4D, LB.STEM + "_lensing_fiducial_correction.dat"))[:, 1]
Cps1 = np.loadtxt(os.path.join(LB.PR4D, LB.STEM + "_cov.dat")); Cip = np.linalg.inv(Cps1)
MW = [np.loadtxt(os.path.join(LB.PR4D, LB.STEM + f"_lens_delta_window/window{b}.dat")) for b in range(1, 10)]
t = np.loadtxt(os.path.join(LB.PR4D, "FFP10_wdipole_lensedCls.dat")); Lc = t[:, 0].astype(int)
CF = {c: np.zeros(LB.LMAX + 1) for c in ("TT", "EE", "TE")}
for c, j in (("TT", 1), ("EE", 2), ("TE", 4)):
    m = Lc <= LB.LMAX; CF[c][Lc[m]] = t[m, j]
def corr(b, C, X):
    w = MW[b]; L = w[:, 0].astype(int); m = (L >= 2) & (L <= LB.LMAX); L, w = L[m], w[m]
    return sum((w[:, 1 + i] * C[c][L]).sum() for i, c in enumerate(("TT", "EE", "TE"))) + (w[:, 4] * X[L]).sum()
dev_i = np.array([corr(b, CF, Xf) / Fps1[b] - 1 for b in range(9)])
ok_i = bool(np.all(np.abs(dev_i) <= 0.02))
P("K3b'(i) PS1 fiducial correction vs full windows x FFP10 (TT, EE, TE, PP), per band rel dev: " + " ".join(f"{v:+.1e}" for v in dev_i)
  + f" -> {'PASS' if ok_i else 'FAIL'} (<= 0.02)")
import camb
opts = {"ombh2": 0.022274, "omch2": 0.11913, "cosmomc_theta": 0.01040867, "As": 0.2132755716e-8, "ns": 0.96597, "tau": 0.0639,
        "lens_potential_accuracy": 1, "lmax": LB.LMAX, "halofit_version": "mead"}
r = camb.get_results(camb.set_params(**opts))
cls = r.get_total_cls(LB.LMAX, CMB_unit="muK"); pp = r.get_lens_potential_cls(LB.LMAX)[:, 0]
CT = {"TT": cls[:, 0], "EE": cls[:, 1], "TE": cls[:, 3]}; Xt = np.zeros(LB.LMAX + 1); Xt[:len(pp)] = pp[:LB.LMAX + 1]
B = LB.wsum(D["W"], Xt) + np.array([corr(b, CT, Xt) for b in range(9)]) - Fps1      # PS1 binned theory (A_planck = 1)
c_ii = LB.qform(B - D["d"], Cip); ok_ii = abs(c_ii - 8.705) <= 0.15
P(f"K3b'(ii) PS1 package unit test: -2 lnL = {c_ii:.4f} vs 8.705 -> {'PASS' if ok_ii else 'FAIL'} (<= 0.15)  "
  "[CAMB + halofit 'mead': code-test input only]")
K3bp = ok_i and ok_ii
F_marged_decomp = (Fps1 - D["F"]).tolist()
P("context: F_PS1 - F_marged (= M_CMB . C_ref) per band: " + " ".join(f"{v:.4e}" for v in F_marged_decomp))

rows = {}
for pair in ("NC1x", "T1x", "T2x", "NC2x"):
    fn = os.path.join(LB.HERE, f"cfg917_{pair}.json")
    if not os.path.exists(fn):
        P(f"\n{pair}: Part B not scored yet (cfg917_{pair}.json absent)"); continue
    J = json.load(open(fn)); ck = J["checks"]
    others_ok = all(v["ok"] for k, v in ck.items() if v.get("gating", True) and k != "K3b")
    bites = J.get("mutate_bites")
    a1 = J["class_rule_value"] if (others_ok and K3bp and bites) else "NOT DIAGNOSTIC"
    pa = os.path.join(LB.HERE, f"cfg917_partA_{pair}.json"); pam = os.path.join(LB.HERE, f"cfg917_partA_{pair}_MUTATE.json")
    lab = json.load(open(pa))["B_grav"]["labels"]["8-400"] if os.path.exists(pa) else None
    dA = json.load(open(pa))["B_grav"]["canonical"]["8-400"]["dA"] if os.path.exists(pa) else None
    rng = json.load(open(pa))["B_grav"]["ranges"]["8-400"] if os.path.exists(pa) else None
    pmut = json.load(open(pam)).get("mutate_bites") if os.path.exists(pam) else None
    def gate(cls):
        if lab is None: return f"{cls} (Part A not run)"
        if cls == "EXCLUDED" or (lab or "").startswith("UNSAFE"): return "FAIL"
        if cls == "CONSISTENT" and lab in ("SAFE", "CONDITIONAL"): return "PASS"
        return cls
    pr = J["primary"]; mem = J["members"]
    rows[pair] = dict(foot=J["foot"], inputs=J["inputs"], dchi2=pr["dchi2"], chi2_F=pr["chi2_F"], chi2_S0=pr["chi2_S0"], p_F=pr["p_F"], p_S0=pr["p_S0"],
                      robust={m: mem[m]["dchi2"] for m in mem}, class_frozen=J["class"], class_A1=a1, class_rule_value=J["class_rule_value"],
                      flags_frozen=J["flags"], partA_label=lab, partA_dA=dA, partA_range=rng, partA_mutate_bites=pmut,
                      gate_frozen=gate(J["class"]), gate_A1=gate(a1))
    P(f"\n{pair} ({J['foot']}, {J['inputs']}): dchi2 {pr['dchi2']:+.4f} (chi2 F {pr['chi2_F']:.3f} p {pr['p_F']:.3f}; S0 {pr['chi2_S0']:.3f} p {pr['p_S0']:.3f}); "
      f"robust [{min(rows[pair]['robust'].values()):+.4f}, {max(rows[pair]['robust'].values()):+.4f}]")
    P(f"   Part B class AS FROZEN: {J['class']}  |  under A1: {a1}")
    P(f"   Part A (CFG649 checklist, unchanged script): canonical dA {dA:+.4f}, bracket [{rng[0]:+.4f}, {rng[1]:+.4f}] -> {lab}"
      f" (CFG649 MUTATE bites {pmut}: M2c's 'dA > 0' clause assumes a boost; quadrature identity passes)")
    P(f"   GATE READING: as frozen {rows[pair]['gate_frozen']}  |  under A1 {rows[pair]['gate_A1']}")
RES = dict(lane="CFG917", part="addendum_A1", addendum_commit="187f895aa", criteria_commit="0289e4ad4",
           K3b_prime=dict(ok=K3bp, i=dict(ok=ok_i, dev=dev_i.tolist()), ii=dict(ok=bool(ok_ii), chi2=c_ii, reference=8.705)),
           F_PS1_minus_F_marged=F_marged_decomp, pairs=rows,
           note="POST HOC amendment; frozen classes are reported next to A1 classes; never pooled across footings; CONSISTENT does not mean the data favour the framework")
P("\nkappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
json.dump(RES, open(os.path.join(LB.HERE, "cfg917_A1_classes.json"), "w"), indent=1)
open(os.path.join(LB.HERE, "cfg917_A1_classes.out"), "w").write("\n".join(OUT) + "\n")
