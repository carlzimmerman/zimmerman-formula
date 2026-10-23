#!/usr/bin/env python3
"""C7_aest_class step V: validation of the AeST-patched CLASS against pristine CLASS (FROZEN_CRITERIA V0-V6).

Binaries (outside the repo, built by `make class` from the pristine tree and from c7_make_patch.py):
  ../_external_data/class_aest_build_2026_10_22/class_vanilla/class      (pristine source)
  ../_external_data/class_aest_build_2026_10_22/class_aest/class         (aest.patch)
  ../_external_data/class_aest_build_2026_10_22/class_aest_mutate/class  (aest_MUTATE.patch; used when C7_MUTATE=1)
Run files go to ../_external_data/class_aest_build_2026_10_22/runs_validate[_MUTATE]/ (not committed).
Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I c7_validate.py      (C7_MUTATE=1 -> *_MUTATE.out/json)
Spectra: lensed TT, TE, EE, phiphi for 2 <= l <= 2500; linear P(k, z=0) for 1e-4 <= k <= 1 Mpc^-1.
Relative difference |dX/X|; TE: |dTE|/sqrt(TT EE).
"""
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import time

import numpy as np

T0 = time.time()
MUT = os.environ.get("C7_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
BLD = os.path.join(EXT, "class_aest_build_2026_10_22")
PRISTINE = os.path.join(EXT, "class_public_v3.3.4_2026_10_22", "class_public-3.3.4")
VAN = os.path.join(BLD, "class_vanilla", "class")
AEST_DIR = os.path.join(BLD, "class_aest_mutate" if MUT else "class_aest")
AEST = os.path.join(AEST_DIR, "class")
RUNS = os.path.join(BLD, f"runs_validate{TAG}")
os.makedirs(RUNS, exist_ok=True)
OUT = open(os.path.join(HERE, f"c7_validate{TAG}.out"), "w")
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


# ------------------------------------------------------------------ provenance of the binaries and of the patch
P("== C7 validation (" + ("MUTATE build" if MUT else "aest build") + ")")
pfile = os.path.join(HERE, "aest_MUTATE.patch" if MUT else "aest.patch")
diff = []
for sub in ("include", "source"):
    for fn in sorted(os.listdir(os.path.join(PRISTINE, sub))):
        a_ = open(os.path.join(PRISTINE, sub, fn)).read().splitlines(keepends=True)
        b_ = open(os.path.join(AEST_DIR, sub, fn)).read().splitlines(keepends=True)
        if a_ != b_:
            diff.extend(difflib.unified_diff(a_, b_, fromfile=f"a/{sub}/{fn}", tofile=f"b/{sub}/{fn}"))
patch_ok = "".join(diff) == open(pfile).read()
van_src_ok = all(open(os.path.join(PRISTINE, s, f)).read() == open(os.path.join(BLD, "class_vanilla", s, f)).read()
                 for s in ("include", "source") for f in os.listdir(os.path.join(PRISTINE, s)))
RES["provenance"] = {"patch_file": os.path.basename(pfile), "patch_sha256": sha(pfile),
                     "built_tree_equals_pristine_plus_patch": patch_ok, "vanilla_tree_equals_pristine": van_src_ok,
                     "class_vanilla_sha256": sha(VAN), "class_aest_sha256": sha(AEST)}
P(f"  built AeST tree == pristine + {os.path.basename(pfile)}: {patch_ok}; vanilla tree == pristine: {van_src_ok}")
assert patch_ok and van_src_ok

# ------------------------------------------------------------------ run helpers
ENV = dict(os.environ, OMP_NUM_THREADS="1")
BASE = {"output": "tCl,pCl,lCl,mPk", "lensing": "yes", "l_max_scalars": 2600, "P_k_max_1/Mpc": 1.0,
        "write_parameters": "no", "thermodynamics_verbose": 1, "background_verbose": 2}
PLANCK = {"omega_b": 0.02237, "h": 0.6736, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544}   # V1 parameters
OMC_PL = 0.1200
CAPTION = {"omega_b": 0.02235, "100*theta_s": 1.04171, "A_s": 2.078e-9, "n_s": 0.963, "tau_reio": 0.049,
           "YHe": 0.242}                                                                       # SZ21 Fig. 1 caption
OMC_CAP = 0.1202
COSH = {"aest_K_type": 1, "aest_K_B": 0.5, "aest_Q0": 0.1, "aest_K2": 7.5e3, "aest_Z0": 1e-9}
EXPB = {"aest_K_type": 2, "aest_K_B": 0.1, "aest_Q0": 1e-4, "aest_K2": 9.5e3, "aest_Z0": 1e-17}
DUST = {"aest_K_type": 0, "aest_K_B": 0.5, "aest_Q0": 0.1}
OMCDM = 1e-8                                                                                    # premise P-CDM
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 20,
        "l_logstep": 1.026, "l_linstep": 25}
EARLY = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.5, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.5}
RUNLOG = {}


def run(name, binary, params):
    ini = os.path.join(RUNS, name + ".ini")
    root = os.path.join(RUNS, name + "_")
    p = dict(BASE)
    p.update(params)
    p["root"] = root
    with open(ini, "w") as fh:
        for k_, v_ in p.items():
            fh.write(f"{k_} = {v_}\n")
    t = time.time()
    r = subprocess.run(["nice", "-n", "15", binary, ini], capture_output=True, text=True, env=ENV)
    if r.returncode != 0:
        raise RuntimeError(f"{name}: CLASS failed: {r.stdout[-500:]} {r.stderr[-500:]}")
    log = r.stdout
    out = {"cl": np.loadtxt(root + "00_cl_lensed.dat"), "pk": np.loadtxt(root + "00_pk.dat")}
    m = re.search(r"100\*theta_s = ([0-9.]+)", log)
    out["theta_s"] = float(m.group(1)) if m else np.nan
    m = re.search(r"baryon drag stops.*?\n.*?\n\s+with comoving sound horizon rs = ([0-9.]+)", log)
    out["rs_drag"] = float(m.group(1)) if m else np.nan
    m = re.search(r"AeST: K_type=\d+, I0 = ([0-9.e+-]+) Mpc\^-1, Q\(1\) = ([0-9.e+-]+), ca2\(1\) = ([0-9.e+-]+)", log)
    if m:
        out["I0"], out["Q1"], out["ca2_1"] = (float(m.group(i)) for i in (1, 2, 3))
    m = re.search(r"h = ([0-9.]+)", log)
    RUNLOG[name] = {"seconds": round(time.time() - t, 2), "theta_s": out["theta_s"], "rs_drag": out["rs_drag"]}
    for kk in ("I0", "Q1", "ca2_1"):
        if kk in out:
            RUNLOG[name][kk] = out[kk]
    return out


def lrange(cl):
    return (cl[:, 0] >= 2) & (cl[:, 0] <= 2500)


def diffs(A, B):
    """max relative differences of B vs A: TT, TE (normalised), EE, phiphi, P(k)."""
    a, b = A["cl"], B["cl"]
    assert np.array_equal(a[:, 0], b[:, 0])
    m = lrange(a)
    d = {"TT": float(np.max(np.abs(b[m, 1] / a[m, 1] - 1))),
         "EE": float(np.max(np.abs(b[m, 2] / a[m, 2] - 1))),
         "TE": float(np.max(np.abs(b[m, 3] - a[m, 3]) / np.sqrt(a[m, 1] * a[m, 2]))),
         "pp": float(np.max(np.abs(b[m, 5] / a[m, 5] - 1)))}
    pa, pb = A["pk"], B["pk"]
    km = (pa[:, 0] >= 1e-4) & (pa[:, 0] <= 1.0)
    if pa.shape == pb.shape and np.allclose(pa[:, 0], pb[:, 0], rtol=1e-6):
        d["pk"] = float(np.max(np.abs(pb[km, 1] / pa[km, 1] - 1)))
    else:   # different k sampling (precision switch): interpolate B onto A in log-log
        lb = np.interp(np.log(pa[km, 0]), np.log(pb[:, 0]), np.log(pb[:, 1]))
        d["pk"] = float(np.max(np.abs(np.exp(lb - np.log(pa[km, 1])) - 1)))
    return d


def fmt(d):
    return ", ".join(f"{k}={v:.2e}" for k, v in d.items())


def cl_only(d):
    return {k: v for k, v in d.items() if k != "pk"}


SPEC = {}

# ------------------------------------------------------------------ V0: patched code without the sector == pristine
SPEC["van"] = run("van", VAN, {**PLANCK, "omega_cdm": OMC_PL})
SPEC["noaest"] = run("noaest", AEST, {**PLANCK, "omega_cdm": OMC_PL})
d0 = diffs(SPEC["van"], SPEC["noaest"])
check("V0_no_sector", max(d0.values()) == 0.0, fmt(d0), "bit-identical (extra check, not frozen)")

# ------------------------------------------------------------------ V1: exact dust limit vs pristine, both gauges
TOL7 = {"tol_perturbations_integration": 1e-7}
for gname in ("synchronous", "newtonian"):
    g = {"gauge": gname}
    vv = run(f"V1_van_{gname}", VAN, {**PLANCK, "omega_cdm": OMC_PL, **TOL7, **g})
    dd = run(f"V1_dust_{gname}", AEST, {**PLANCK, "omega_cdm": OMCDM, "omega_aest": OMC_PL - OMCDM, **DUST,
                                         **TOL7, **g})
    d1 = diffs(vv, dd)
    bg = {"theta_s": abs(dd["theta_s"] / vv["theta_s"] - 1), "rs_drag": abs(dd["rs_drag"] / vv["rs_drag"] - 1)}
    check(f"V1_dust_{gname}", max(d1.values()) <= 1e-4 and max(bg.values()) <= 1e-6,
          fmt(d1) + f"; 100theta_s {bg['theta_s']:.1e}, r_drag {bg['rs_drag']:.1e}",
          "<= 1e-4 every spectrum; background <= 1e-6", {"diffs": d1, "background": bg})
    # same comparison at default tolerance: reported, not scored
    vv0 = run(f"V1d_van_{gname}", VAN, {**PLANCK, "omega_cdm": OMC_PL, **g})
    dd0 = run(f"V1d_dust_{gname}", AEST, {**PLANCK, "omega_cdm": OMCDM, "omega_aest": OMC_PL - OMCDM, **DUST, **g})
    d1d = diffs(vv0, dd0)
    P(f"  (reported) dust vs pristine at default tolerance, {gname}: {fmt(d1d)}")
    RES[f"V1_default_tol_{gname}"] = d1d

# ------------------------------------------------------------------ benchmarks at the SZ21 caption parameters
bench = {}
for bn, kp in (("cosh", COSH), ("exp", EXPB)):
    bench[bn] = {**CAPTION, "omega_cdm": OMCDM, "omega_aest": OMC_CAP - OMCDM, **kp}
VANCAP = {**CAPTION, "omega_cdm": OMC_CAP}

# V2: convergence (Cosh)
c_def = run("V2_cosh_default", AEST, bench["cosh"])
c_hi = run("V2_cosh_high", AEST, {**bench["cosh"], **HIGH})
v_def = run("V2_van_default", VAN, VANCAP)
v_hi = run("V2_van_high", VAN, {**VANCAP, **HIGH})
d2a, d2v = diffs(c_def, c_hi), diffs(v_def, v_hi)
thr2 = {k: max(2e-3, 2 * d2v[k]) for k in d2a}
check("V2_convergence", all(d2a[k] <= thr2[k] for k in d2a), "AeST " + fmt(d2a) + " | vanilla " + fmt(d2v),
      "each <= max(2e-3, 2 x vanilla)", {"aest": d2a, "vanilla": d2v})

# V3: gauge consistency (Cosh, Exp)
v_sy = v_def
v_nw = run("V3_van_newtonian", VAN, {**VANCAP, "gauge": "newtonian"})
d3v = diffs(v_sy, v_nw)
thr3 = {k: max(1e-3, 3 * d3v[k]) for k in ("TT", "TE", "EE", "pp")}
for bn in ("cosh", "exp"):
    a_sy = c_def if bn == "cosh" else run("V3_exp_synchronous", AEST, bench["exp"])
    a_nw = run(f"V3_{bn}_newtonian", AEST, {**bench[bn], "gauge": "newtonian"})
    SPEC[bn] = a_sy
    d3 = diffs(a_sy, a_nw)
    check(f"V3_gauge_{bn}", all(d3[k] <= thr3[k] for k in thr3), "AeST " + fmt(d3) + " | vanilla " + fmt(d3v),
          "TT/TE/EE/pp each <= max(1e-3, 3 x vanilla); P(k) reported", {"aest": d3, "vanilla": d3v})

# V5: IC attractor (Cosh): earlier start
c_early = run("V5_cosh_early", AEST, {**bench["cosh"], **EARLY})
v_early = run("V5_van_early", VAN, {**VANCAP, **EARLY})
d5a, d5v = diffs(c_def, c_early), diffs(v_def, v_early)
check("V5_ic_attractor", all(d5a[k] <= d5v[k] + 1e-4 for k in d5a), "AeST " + fmt(d5a) + " | vanilla " + fmt(d5v),
      "each <= vanilla + 1e-4", {"aest": d5a, "vanilla": d5v})

# V6 (diagnostic): limit continuity, Cosh with Z0 x {1, 0.1, 0.01} vs the dust limit at the same parameters
dustcap = run("V6_dust", AEST, {**CAPTION, "omega_cdm": OMCDM, "omega_aest": OMC_CAP - OMCDM, **DUST,
                                "aest_K_B": COSH["aest_K_B"], "aest_Q0": COSH["aest_Q0"]})
v6 = {}
for f in (1.0, 0.1, 0.01):
    r_ = c_def if f == 1.0 else run(f"V6_cosh_Z0x{f}", AEST, {**bench["cosh"], "aest_Z0": COSH["aest_Z0"] * f})
    v6[str(f)] = diffs(dustcap, r_)
    P(f"  V6 (diagnostic) Cosh Z0 x {f}: deviation from dust limit {fmt(v6[str(f)])}")
RES["V6_limit_continuity"] = v6
mono = all(v6["0.01"][k] <= v6["0.1"][k] <= v6["1.0"][k] for k in v6["1.0"])
P(f"  V6 monotone shrink as Z0 -> 0 (all spectra): {mono}   [diagnostic, not gating]")
RES["V6_monotone"] = mono
# V6 repeated at the V2 high-precision settings (diagnostic): separates physics from default-precision noise
dusthi = run("V6hi_dust", AEST, {**CAPTION, "omega_cdm": OMCDM, "omega_aest": OMC_CAP - OMCDM, **DUST,
                                 "aest_K_B": COSH["aest_K_B"], "aest_Q0": COSH["aest_Q0"], **HIGH})
v6h = {}
for f in (1.0, 0.1, 0.01):
    r_ = c_hi if f == 1.0 else run(f"V6hi_cosh_Z0x{f}", AEST, {**bench["cosh"], "aest_Z0": COSH["aest_Z0"] * f, **HIGH})
    v6h[str(f)] = diffs(dusthi, r_)
    P(f"  V6hi (diagnostic, high precision) Cosh Z0 x {f}: deviation from dust limit {fmt(v6h[str(f)])}")
RES["V6hi_limit_continuity"] = v6h
monoh = all(v6h["0.01"][k] <= v6h["0.1"][k] <= v6h["1.0"][k] for k in v6h["1.0"])
P(f"  V6hi monotone shrink as Z0 -> 0 (all spectra): {monoh}   [diagnostic, not gating]")
RES["V6hi_monotone"] = monoh
# also: benchmark vs pristine LCDM at the same caption parameters (reported)
RES["bench_vs_LCDM"] = {bn: diffs(v_def, SPEC[bn]) for bn in ("cosh", "exp")}
for bn in ("cosh", "exp"):
    P(f"  (reported) {bn} benchmark vs pristine LCDM, caption parameters: {fmt(RES['bench_vs_LCDM'][bn])}")

ready = all(RES["checks"][c]["pass"] for c in ("V1_dust_synchronous", "V1_dust_newtonian", "V2_convergence",
                                               "V3_gauge_cosh", "V3_gauge_exp", "V5_ic_attractor"))
RES["native_prediction_ready_this_build"] = ready
RES["runs"] = RUNLOG
RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, f"c7_validate_results{TAG}.json"), "w"), indent=1)
P(f"  native-prediction-ready conditions on this build (V1, V2, V3, V5): {ready}; elapsed {RES['elapsed_s']} s")
P(f"C7_VALIDATE COMPLETE: {NP}/{NC} checks PASS.")
OUT.close()
sys.exit(0 if NP == NC else 1)
