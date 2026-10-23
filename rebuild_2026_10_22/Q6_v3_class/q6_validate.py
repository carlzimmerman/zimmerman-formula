#!/usr/bin/env python3
"""Q6_v3_class step V: validation of the Khronon (v3) variant of C7's patched CLASS (FROZEN_CRITERIA section 6 + A2).

Binaries (outside the repo):
  ../_external_data/class_aest_build_2026_10_22/class_vanilla/class            pristine source (C7's build)
  ../_external_data/class_khronon_build_2026_10_23/class_khronon/class         pristine + khronon.patch
  ../_external_data/class_khronon_build_2026_10_23/class_khronon_mutate/class  pristine + khronon_MUTATE.patch
Run files: ../_external_data/class_khronon_build_2026_10_23/runs_validate[_MUTATE]/ (not committed).
Run: OMP_NUM_THREADS=1 nice -n 19 python3 -I q6_validate.py      (Q6_MUTATE=1 -> MUTATE binary, *_MUTATE.out/json)
Models: aest_K_type 0 DUST, 4 LOB (dust background + literal c_s^2); aest_K2 = mu_K^2 [Mpc^-2]; aest_lambda_c = j1.
"""
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

import numpy as np

T0 = time.time()
MUT = os.environ.get("Q6_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
PRISTINE = os.path.join(EXT, "class_public_v3.3.4_2026_10_22", "class_public-3.3.4")
VAN = os.path.join(EXT, "class_aest_build_2026_10_22", "class_vanilla", "class")
C7TREE = os.path.join(EXT, "class_aest_build_2026_10_22", "class_aest")
BLD = os.path.join(EXT, "class_khronon_build_2026_10_23")
KDIR = os.path.join(BLD, "class_khronon_mutate" if MUT else "class_khronon")
KHR = os.path.join(KDIR, "class")
RUNS = os.path.join(BLD, f"runs_validate{TAG}")
shutil.rmtree(RUNS, ignore_errors=True)
os.makedirs(RUNS, exist_ok=True)
OUT = open(os.path.join(HERE, f"q6_validate{TAG}.out"), "w")
RES = {"mutate": MUT, "checks": {}}
NP = NC = 0


def P(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    OUT.write(s + "\n")
    OUT.flush()


def check(name, ok, value, thr, extra=None):
    global NP, NC
    NC += 1
    NP += bool(ok)
    P(f"{name} {'PASS' if ok else 'FAIL'} {value} {thr}")
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    if extra:
        RES["checks"][name].update(extra)


def sha(fn):
    return hashlib.sha256(open(fn, "rb").read()).hexdigest()


# ------------------------------------------------------------------ provenance
P("== Q6 validation (" + ("MUTATE build" if MUT else "Khronon build") + ")")
pfile = os.path.join(HERE, "khronon_MUTATE.patch" if MUT else "khronon.patch")
diff = []
for sub in ("include", "source"):
    for fn in sorted(os.listdir(os.path.join(PRISTINE, sub))):
        a_ = open(os.path.join(PRISTINE, sub, fn)).read().splitlines(keepends=True)
        b_ = open(os.path.join(KDIR, sub, fn)).read().splitlines(keepends=True)
        if a_ != b_:
            diff.extend(difflib.unified_diff(a_, b_, fromfile=f"a/{sub}/{fn}", tofile=f"b/{sub}/{fn}"))
patch_ok = "".join(diff) == open(pfile).read()
van_ok = all(open(os.path.join(PRISTINE, s, f)).read() == open(os.path.join(EXT, "class_aest_build_2026_10_22",
             "class_vanilla", s, f)).read() for s in ("include", "source") for f in os.listdir(os.path.join(PRISTINE, s)))


def changed_lines_c7(fn):
    """line numbers (1-based) of C7's file that differ from the Khronon tree."""
    a_ = open(os.path.join(C7TREE, "source", fn)).read().splitlines()
    b_ = open(os.path.join(KDIR, "source", fn)).read().splitlines()
    out = []
    for tag, i1, i2, j1_, j2 in difflib.SequenceMatcher(None, a_, b_, autojunk=False).get_opcodes():
        if tag != "equal":
            out.extend(range(i1 + 1, max(i2, i1 + 1) + 1))
    return out, a_


def span(lines, start, end):
    i = next(n for n, l in enumerate(lines) if start in l)
    j = next(n for n in range(i, len(lines)) if end in lines[n])
    return i + 1, j + 1


bg_lines, bgA = changed_lines_c7("background.c")
pt_lines, ptA = changed_lines_c7("perturbations.c")
sp_bg = span(bgA, "C7_aest_class: background of the AeST extra sector", "C7_aest_class: solve the shift charge I0")
sp_rhs = span(ptA, "C7_aest_class: the AeST extra sector's linear equations", "  return _SUCCESS_;")
sp_ic = span(ptA, "/* AeST extra sector (C7): adiabatic IC", "index_pt_chi_aest] = a*Qa*th_a/k/k + qal_a;")
sp_ic = (sp_ic[0], sp_ic[1] + 1)
others_same = all(open(os.path.join(C7TREE, s, f)).read() == open(os.path.join(KDIR, s, f)).read()
                  for s in ("include", "source") for f in os.listdir(os.path.join(C7TREE, s))
                  if not (s == "source" and f in ("background.c", "perturbations.c")))
in_spans = (all(sp_bg[0] - 1 <= n <= sp_bg[1] for n in bg_lines)
            and all(sp_rhs[0] - 1 <= n <= sp_rhs[1] + 1 or sp_ic[0] - 1 <= n <= sp_ic[1] + 1 for n in pt_lines))
RES["provenance"] = {"patch_file": os.path.basename(pfile), "patch_sha256": sha(pfile),
                     "built_tree_equals_pristine_plus_patch": patch_ok, "vanilla_tree_equals_pristine": van_ok,
                     "c7_tree_vs_khronon_only_two_functions_and_IC_block": bool(others_same and in_spans),
                     "c7_spans": {"background_aest_K": sp_bg, "perturbations_aest_rhs": sp_rhs, "IC_block": sp_ic},
                     "class_vanilla_sha256": sha(VAN), "class_khronon_sha256": sha(KHR)}
check("V_prov", patch_ok and van_ok and others_same and in_spans,
      f"tree == pristine + {os.path.basename(pfile)}: {patch_ok}; vanilla == pristine: {van_ok}; vs C7 tree only "
      f"background_aest_K {sp_bg}, perturbations_aest_rhs {sp_rhs}, IC block {sp_ic} differ: {others_same and in_spans}",
      "all true (extra check)")

# ------------------------------------------------------------------ run helpers
ENV = dict(os.environ, OMP_NUM_THREADS="1")
BASE = {"output": "tCl,pCl,lCl,mPk", "lensing": "yes", "l_max_scalars": 2600, "P_k_max_1/Mpc": 1.0,
        "write_parameters": "no", "thermodynamics_verbose": 1, "background_verbose": 2, "overwrite_root": "yes"}
PLANCK = {"omega_b": 0.02237, "h": 0.6736, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544}   # C7's V1 parameters
OMC = 0.1200
OMCDM = 1e-8
HREF = 0.67552                                     # C7 LCDM refit h: grid mu_K [h/Mpc] -> physical Mpc^-1
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 20,
        "l_logstep": 1.026, "l_linstep": 25}
EARLY = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.5, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.5}
KHRON = {"aest_Q0": 1.0, "aest_K_B": 1.0, "aest_g": 1.0}
RUNLOG = {}


def model(ktype, mu_h=None, j1=-1.0):
    d = {**KHRON, "aest_K_type": ktype, "aest_lambda_c": j1, "aest_K2": 1.0 if mu_h is None else (mu_h * HREF) ** 2}
    return d


def run(name, binary, params, timeout=1200):
    root = os.path.join(RUNS, name + "_")
    p = dict(BASE)
    p.update(params)
    p["root"] = root
    ini = root + ".ini"
    with open(ini, "w") as fh:
        for k_, v_ in p.items():
            fh.write(f"{k_} = {v_}\n")
    t_launch = time.time()
    try:
        r = subprocess.run(["nice", "-n", "19", binary, ini], capture_output=True, text=True, env=ENV, timeout=timeout)
    except subprocess.TimeoutExpired:
        RUNLOG[name] = {"timed_out_s": timeout}
        return None
    if r.returncode != 0:
        RUNLOG[name] = {"failed": (r.stdout + r.stderr)[-400:]}
        return None
    assert os.path.getmtime(root + "_cl_lensed.dat") >= t_launch - 1, "stale-output guard"
    out = {"cl": np.loadtxt(root + "_cl_lensed.dat"), "pk": np.loadtxt(root + "_pk.dat")}
    m = re.search(r"100\*theta_s = ([0-9.]+)", r.stdout)
    out["theta_s"] = float(m.group(1)) if m else np.nan
    m = re.search(r"baryon drag stops.*?\n.*?\n\s+with comoving sound horizon rs = ([0-9.]+)", r.stdout)
    out["rs_drag"] = float(m.group(1)) if m else np.nan
    RUNLOG[name] = {"seconds": round(time.time() - t_launch, 2), "theta_s": out["theta_s"], "rs_drag": out["rs_drag"]}
    return out


def diffs(A, B, pk=True):
    a, b = A["cl"], B["cl"]
    assert np.array_equal(a[:, 0], b[:, 0])
    m = (a[:, 0] >= 2) & (a[:, 0] <= 2500)
    d = {"TT": float(np.max(np.abs(b[m, 1] / a[m, 1] - 1))),
         "EE": float(np.max(np.abs(b[m, 2] / a[m, 2] - 1))),
         "TE": float(np.max(np.abs(b[m, 3] - a[m, 3]) / np.sqrt(a[m, 1] * a[m, 2]))),
         "pp": float(np.max(np.abs(b[m, 5] / a[m, 5] - 1)))}
    if pk:
        pa, pb = A["pk"], B["pk"]
        km = (pa[:, 0] >= 1e-4) & (pa[:, 0] <= 1.0)
        if pa.shape == pb.shape and np.allclose(pa[:, 0], pb[:, 0], rtol=1e-6):
            d["pk"] = float(np.max(np.abs(pb[km, 1] / pa[km, 1] - 1)))
        else:
            lb = np.interp(np.log(pa[km, 0]), np.log(pb[:, 0]), np.log(pb[:, 1]))
            d["pk"] = float(np.max(np.abs(np.exp(lb - np.log(pa[km, 1])) - 1)))
    return d


def fmt(d):
    return ", ".join(f"{k}={v:.2e}" for k, v in d.items())


TOL7 = {"tol_perturbations_integration": 1e-7}
KOFF = {**PLANCK, "omega_cdm": OMC}
KON = {**PLANCK, "omega_cdm": OMCDM, "omega_aest": OMC - OMCDM}

# ------------------------------------------------------------------ V0
v0a = run("V0_van", VAN, KOFF)
v0b = run("V0_khronon_off", KHR, KOFF)
d0 = diffs(v0a, v0b)
check("V0_no_sector", max(d0.values()) == 0.0, fmt(d0), "bit-identical (extra check)")

# ------------------------------------------------------------------ V1: DUST with j1 = 0 vs pristine, both gauges
for gname in ("synchronous", "newtonian"):
    g = {"gauge": gname}
    vv = run(f"V1_van_{gname}", VAN, {**KOFF, **TOL7, **g})
    dd = run(f"V1_dust_j0_{gname}", KHR, {**KON, **model(0, None, 0.0), **TOL7, **g})
    if dd is None:
        check(f"V1_dust_{gname}", False, f"CLASS failed: {RUNLOG[f'V1_dust_j0_{gname}']}", "<= 1e-4; <= 1e-6")
        continue
    d1 = diffs(vv, dd)
    bg = {"theta_s": abs(dd["theta_s"] / vv["theta_s"] - 1), "rs_drag": abs(dd["rs_drag"] / vv["rs_drag"] - 1)}
    check(f"V1_dust_{gname}", max(d1.values()) <= 1e-4 and max(bg.values()) <= 1e-6,
          fmt(d1) + f"; 100theta_s {bg['theta_s']:.1e}, r_drag {bg['rs_drag']:.1e}",
          "<= 1e-4 every spectrum; background <= 1e-6", {"diffs": d1, "background": bg})
    RES[f"_van_{gname}"] = True
    if gname == "synchronous":
        VV1 = vv
# reported beside V1 (not gated): DUST j1 = -1; LOB at mu_K = 1e6 h/Mpc with j1 = 0 (600 s limit) and j1 = -1
rep = {}
for nm, pr, to in (("DUST_j1m1", {**model(0, None, -1.0)}, 1200), ("LOB_mu1e6_j1m1", {**model(4, 1e6, -1.0)}, 1200),
                   ("LOB_mu1e6_j10", {**model(4, 1e6, 0.0)}, 600)):
    o = run(f"V1r_{nm}", KHR, {**KON, **pr, **TOL7}, timeout=to)
    rep[nm] = diffs(VV1, o) if o is not None else RUNLOG[f"V1r_{nm}"]
    P(f"  (reported) {nm} vs pristine (synchronous, tol 1e-7): " + (fmt(rep[nm]) if o is not None else str(rep[nm])))
RES["V1_reported"] = rep

# ------------------------------------------------------------------ V2: convergence, LOB mu_K = 361 h/Mpc, j1 = -1
L361 = {**KON, **model(4, 361.0, -1.0)}
L148 = {**KON, **model(4, 14.8, -1.0)}
c_def = run("V2_lob361_default", KHR, L361)
c_hi = run("V2_lob361_high", KHR, {**L361, **HIGH})
v_def = run("V2_van_default", VAN, KOFF)
v_hi = run("V2_van_high", VAN, {**KOFF, **HIGH})
d2a, d2v = diffs(c_def, c_hi), diffs(v_def, v_hi)
thr2 = {k: max(2e-3, 2 * d2v[k]) for k in d2a}
check("V2_convergence", all(d2a[k] <= thr2[k] for k in d2a), "LOB361 " + fmt(d2a) + " | vanilla " + fmt(d2v),
      "each <= max(2e-3, 2 x vanilla)", {"khronon": d2a, "vanilla": d2v})

# ------------------------------------------------------------------ V3: gauge consistency, LOB at 361 and 14.8 h/Mpc
v_nw = run("V3_van_newtonian", VAN, {**KOFF, "gauge": "newtonian"})
d3v = diffs(v_def, v_nw)
thr3 = {k: max(1e-3, 3 * d3v[k]) for k in d3v}
for lab, pr, a_sy in (("361", L361, c_def), ("14.8", L148, None)):
    if a_sy is None:
        a_sy = run(f"V3_lob{lab}_synchronous", KHR, pr)
    a_nw = run(f"V3_lob{lab}_newtonian", KHR, {**pr, "gauge": "newtonian"})
    d3 = diffs(a_sy, a_nw)
    check(f"V3_gauge_LOB{lab}", all(d3[k] <= thr3[k] for k in thr3), "LOB " + fmt(d3) + " | vanilla " + fmt(d3v),
          "TT/TE/EE/pp/P(k) each <= max(1e-3, 3 x vanilla)", {"khronon": d3, "vanilla": d3v})
    RES[f"LOB{lab}_vs_LCDM_same_params"] = diffs(v_def, a_sy)
    P(f"  (reported) LOB {lab} h/Mpc vs pristine LCDM at the same parameters: {fmt(RES[f'LOB{lab}_vs_LCDM_same_params'])}")

# ------------------------------------------------------------------ V5: IC attractor, LOB 361
c_early = run("V5_lob361_early", KHR, {**L361, **EARLY})
v_early = run("V5_van_early", VAN, {**KOFF, **EARLY})
d5a, d5v = diffs(c_def, c_early), diffs(v_def, v_early)
check("V5_ic_attractor", all(d5a[k] <= d5v[k] + 1e-4 for k in d5a), "LOB361 " + fmt(d5a) + " | vanilla " + fmt(d5v),
      "each <= vanilla + 1e-4", {"khronon": d5a, "vanilla": d5v})

# ------------------------------------------------------------------ AMENDMENT A3 supplementary gates (post-result)
P("== AMENDMENT A3 supplementary gates (post-result; the frozen V2/V3/V5 lines above stay as printed)")


def ndiffs(A, B, R):
    """max |B - A| in units of the reference (pristine LCDM) spectrum R; TE in units of sqrt(TT EE)_R; same k grid."""
    a, b, r = A["cl"], B["cl"], R["cl"]
    assert np.array_equal(a[:, 0], b[:, 0]) and np.array_equal(a[:, 0], r[:, 0])
    m = (a[:, 0] >= 2) & (a[:, 0] <= 2500)
    d = {"TT": float(np.max(np.abs(b[m, 1] - a[m, 1]) / r[m, 1])),
         "EE": float(np.max(np.abs(b[m, 2] - a[m, 2]) / r[m, 2])),
         "TE": float(np.max(np.abs(b[m, 3] - a[m, 3]) / np.sqrt(r[m, 1] * r[m, 2]))),
         "pp": float(np.max(np.abs(b[m, 5] - a[m, 5]) / r[m, 5]))}
    pa, pb, pr = A["pk"], B["pk"], R["pk"]
    assert pa.shape == pb.shape == pr.shape and np.allclose(pa[:, 0], pb[:, 0], rtol=1e-6) and np.allclose(pa[:, 0], pr[:, 0], rtol=1e-6)
    km = (pa[:, 0] >= 1e-4) & (pa[:, 0] <= 1.0)
    d["pk"] = float(np.max(np.abs(pb[km, 1] - pa[km, 1]) / pr[km, 1]))
    return d


K20 = {"k_per_decade_for_pk": 20}
c_d20 = run("V2b_lob361_default_k20", KHR, {**L361, **K20})
v_d20 = run("V2b_van_default_k20", VAN, {**KOFF, **K20})
d2b, d2bv = ndiffs(c_d20, c_hi, v_hi), ndiffs(v_d20, v_hi, v_hi)
thr2b = {k: max(2e-3, 2 * d2bv[k]) for k in d2b}
check("V2b_convergence_same_grid", all(d2b[k] <= thr2b[k] for k in d2b), "LOB361 " + fmt(d2b) + " | vanilla " + fmt(d2bv),
      "|dX|/X_LCDM each <= max(2e-3, 2 x vanilla) (A3)", {"khronon": d2b, "vanilla": d2bv})
d3bv = ndiffs(v_def, v_nw, v_def)
thr3b = {k: max(1e-3, 3 * d3bv[k]) for k in d3bv}
for lab, pr in (("361", L361), ("14.8", L148)):
    a_sy = c_def if lab == "361" else run(f"V3b_lob{lab}_synchronous", KHR, pr)
    a_nw = run(f"V3b_lob{lab}_newtonian", KHR, {**pr, "gauge": "newtonian"})
    d3b = ndiffs(a_sy, a_nw, v_def)
    check(f"V3b_gauge_LOB{lab}", all(d3b[k] <= thr3b[k] for k in thr3b), "LOB " + fmt(d3b) + " | vanilla " + fmt(d3bv),
          "|dX|/X_LCDM each <= max(1e-3, 3 x vanilla) (A3)", {"khronon": d3b, "vanilla": d3bv})
Q4 = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25}
Q8 = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.125, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.125}
c4_, c8_ = run("V5b_lob361_x0.25", KHR, {**L361, **Q4}), run("V5b_lob361_x0.125", KHR, {**L361, **Q8})
v4_, v8_ = run("V5b_van_x0.25", VAN, {**KOFF, **Q4}), run("V5b_van_x0.125", VAN, {**KOFF, **Q8})
d5b, d5bv = diffs(c4_, c8_, pk=False), diffs(v4_, v8_, pk=False)
d5b["pk"], d5bv["pk"] = ndiffs(c4_, c8_, v4_)["pk"], ndiffs(v4_, v8_, v4_)["pk"]
check("V5b_ic_attractor_x0.25", all(d5b[k] <= d5bv[k] + 1e-4 for k in d5b), "LOB361 " + fmt(d5b) + " | vanilla " + fmt(d5bv),
      "each <= vanilla + 1e-4 (A3; C_l relative, P(k) in units of LCDM)", {"khronon": d5b, "vanilla": d5bv})
readyA3 = all(RES["checks"][c]["pass"] for c in ("V1_dust_synchronous", "V1_dust_newtonian", "V2b_convergence_same_grid",
                                                 "V3b_gauge_LOB361", "V3b_gauge_LOB14.8", "V5b_ic_attractor_x0.25"))
RES["native_prediction_ready_A3_this_build"] = readyA3
P(f"  native-prediction-ready (A3 gates V1, V2b, V3b, V5b) on this build: {readyA3}")
ready = all(RES["checks"][c]["pass"] for c in ("V1_dust_synchronous", "V1_dust_newtonian", "V2_convergence",
                                               "V3_gauge_LOB361", "V3_gauge_LOB14.8", "V5_ic_attractor"))
RES["native_prediction_ready_this_build"] = ready
RES["runs"] = RUNLOG
RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, f"q6_validate_results{TAG}.json"), "w"), indent=1)
P(f"  native-prediction-ready conditions on this build (V1, V2, V3, V5): {ready}; elapsed {RES['elapsed_s']} s")
P(f"Q6_VALIDATE COMPLETE: {NP}/{NC} checks PASS.")
OUT.close()
sys.exit(0 if NP == NC else 1)
