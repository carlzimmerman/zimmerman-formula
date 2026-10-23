#!/usr/bin/env python3
"""Q7_bs25_cosmology step V (FROZEN_CRITERIA section 6): validation of the DBI case (aest_K_type 5) added to Q6's
Khronon CLASS.

Binaries (outside the repo):
  ../_external_data/class_aest_build_2026_10_22/class_vanilla/class                  pristine (C7's build)
  ../_external_data/class_khronon_build_2026_10_23/class_khronon/class               Q6 (pristine + khronon.patch)
  ../_external_data/class_khronon_dbi_build_2026_10_23/class_dbi[_mutate]/class     Q6 tree + dbi[_MUTATE].patch
Run files: ../_external_data/class_khronon_dbi_build_2026_10_23/runs_validate[_MUTATE]/ (not committed).
Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I q7_validate.py      (Q7_MUTATE=1 -> MUTATE binary, *_MUTATE.out/json)
Precision choices fixed before any run (not stated in the frozen text): V1 and V2 use tol_perturbations_integration =
1e-7 (as Q6's dust gate V1); V0 uses CLASS defaults; V3-V5 as Q6's A3 gates.
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

import mpmath as mp
import numpy as np

T0 = time.time()
MUT = os.environ.get("Q7_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
PRISTINE = os.path.join(EXT, "class_public_v3.3.4_2026_10_22", "class_public-3.3.4")
VAN = os.path.join(EXT, "class_aest_build_2026_10_22", "class_vanilla", "class")
Q6DIR = os.path.join(EXT, "class_khronon_build_2026_10_23", "class_khronon")
Q6BIN = os.path.join(Q6DIR, "class")
BLD = os.path.join(EXT, "class_khronon_dbi_build_2026_10_23")
DDIR = os.path.join(BLD, "class_dbi_mutate" if MUT else "class_dbi")
DBI = os.path.join(DDIR, "class")
RUNS = os.path.join(BLD, f"runs_validate{TAG}")
shutil.rmtree(RUNS, ignore_errors=True)
os.makedirs(RUNS, exist_ok=True)
OUT = open(os.path.join(HERE, f"q7_validate{TAG}.out"), "w")
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


def save():
    RES["elapsed_s"] = round(time.time() - T0, 1)
    json.dump(RES, open(os.path.join(HERE, f"q7_validate_results{TAG}.json"), "w"), indent=1, default=float)


# ------------------------------------------------------------------ V_prov
P("== Q7 validation (" + ("MUTATE build" if MUT else "DBI build") + ")")
q6patch = os.path.join(REPO, "rebuild_2026_10_22", "Q6_v3_class", "khronon.patch")
pfile = os.path.join(HERE, "dbi_MUTATE.patch" if MUT else "dbi.patch")


def tree_diff(A, B):
    out = []
    for sub in ("include", "source"):
        for fn in sorted(os.listdir(os.path.join(A, sub))):
            a_ = open(os.path.join(A, sub, fn)).read().splitlines(keepends=True)
            b_ = open(os.path.join(B, sub, fn)).read().splitlines(keepends=True)
            if a_ != b_:
                out.extend(difflib.unified_diff(a_, b_, fromfile=f"a/{sub}/{fn}", tofile=f"b/{sub}/{fn}"))
    return "".join(out)


q6_ok = tree_diff(PRISTINE, Q6DIR) == open(q6patch).read()
dbi_ok = tree_diff(Q6DIR, DDIR) == open(pfile).read()


def fn_span(lines, start):
    i = next(n for n, l in enumerate(lines) if l.startswith(start))
    j = next(n for n in range(i, len(lines)) if lines[n] == "}" and lines[n - 1].strip() == "return _SUCCESS_;")
    return i + 1, j + 1


def changed(fn):
    a_ = open(os.path.join(Q6DIR, "source", fn)).read().splitlines()
    b_ = open(os.path.join(DDIR, "source", fn)).read().splitlines()
    out = []
    for tag, i1, i2, _, _ in difflib.SequenceMatcher(None, a_, b_, autojunk=False).get_opcodes():
        if tag != "equal":
            out.extend(range(i1 + 1, max(i2, i1 + 1) + 1))
    return out, a_


bgc, bgA = changed("background.c")
ptc, ptA = changed("perturbations.c")
sp_bg = fn_span(bgA, "int background_aest_K(")
sp_pt = fn_span(ptA, "static int perturbations_aest_rhs(")
others = all(open(os.path.join(Q6DIR, s, f)).read() == open(os.path.join(DDIR, s, f)).read()
             for s in ("include", "source") for f in os.listdir(os.path.join(Q6DIR, s))
             if not (s == "source" and f in ("background.c", "perturbations.c")))
in_spans = all(sp_bg[0] <= n <= sp_bg[1] for n in bgc) and all(sp_pt[0] <= n <= sp_pt[1] for n in ptc)
RES["provenance"] = {"dbi_patch": os.path.basename(pfile), "dbi_patch_sha256": sha(pfile), "q6_patch_sha256": sha(q6patch),
                     "q6_tree_equals_pristine_plus_khronon_patch": q6_ok, "dbi_tree_equals_q6_plus_dbi_patch": dbi_ok,
                     "only_two_functions_differ_from_q6": bool(others and in_spans),
                     "q6_spans": {"background_aest_K": sp_bg, "perturbations_aest_rhs": sp_pt},
                     "changed_lines_q6_numbering": {"background.c": bgc, "perturbations.c": ptc},
                     "class_vanilla_sha256": sha(VAN), "class_q6_sha256": sha(Q6BIN), "class_dbi_sha256": sha(DBI)}
check("V_prov", q6_ok and dbi_ok and others and in_spans,
      f"Q6 tree == pristine + khronon.patch: {q6_ok}; tree == Q6 + {os.path.basename(pfile)}: {dbi_ok}; "
      f"only background_aest_K {sp_bg} / perturbations_aest_rhs {sp_pt} differ: {others and in_spans}", "all true")
save()

# ------------------------------------------------------------------ V_unit: the two functions as built, in a C harness
P("== V_unit: C harness compiled from the two function texts of the built tree")


def extract(path, start):
    lines = open(path).read().splitlines()
    i0, j0 = fn_span(lines, start)
    return "\n".join(lines[i0 - 1:j0])


HARN = os.path.join(BLD, f"unit{TAG}")
shutil.rmtree(HARN, ignore_errors=True)
os.makedirs(HARN)
csrc = r"""#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define _SUCCESS_ 0
#define _FAILURE_ 1
#define class_stop(err, ...) do { snprintf(err, 1024, __VA_ARGS__); fprintf(stderr, "%s\n", err); return _FAILURE_; } while (0)
struct background { double aest_I0, aest_K2, aest_Z0, aest_lambda_c; int aest_K_type; char error_message[1024];
  int index_bg_a, index_bg_H, index_bg_Q_aest, index_bg_Kz_aest, index_bg_Kp_aest, index_bg_ca2_aest; };
""" + extract(os.path.join(DDIR, "source", "background.c"), "int background_aest_K(") + "\n" + \
    extract(os.path.join(DDIR, "source", "perturbations.c"), "static int perturbations_aest_rhs(") + r"""
int main(void) {
  struct background b; int type; double mu2, I0, lam, a, k;
  b.index_bg_a = 0; b.index_bg_H = 1; b.index_bg_Q_aest = 2; b.index_bg_Kz_aest = 3; b.index_bg_Kp_aest = 4;
  b.index_bg_ca2_aest = 5; b.aest_lambda_c = -1.;
  while (scanf("%d %lf %lf %lf %lf %lf", &type, &mu2, &I0, &lam, &a, &k) == 6) {
    double Q, Kz, Kp, ca2, pv[6], y[4] = {1., 0., 0., 0.}, cs2;
    b.aest_K_type = type; b.aest_K2 = mu2; b.aest_I0 = I0; b.aest_Z0 = lam;
    if (background_aest_K(&b, a, &Q, &Kz, &Kp, &ca2) != _SUCCESS_) { printf("ERR\n"); continue; }
    pv[0] = a; pv[1] = 1.0; pv[2] = Q; pv[3] = Kz; pv[4] = Kp; pv[5] = ca2;
    perturbations_aest_rhs(&b, k, pv, 0., 0., y, NULL, &cs2);
    printf("%.17e %.17e %.17e %.17e %.17e\n", Q, Kz, Kp, ca2, cs2);
  }
  return 0;
}
"""
open(os.path.join(HARN, "harness.c"), "w").write(csrc)
rc = subprocess.run(["nice", "-n", "15", "cc", "-O3", "-o", os.path.join(HARN, "harness"), os.path.join(HARN, "harness.c"), "-lm"],
                    capture_output=True, text=True)
assert rc.returncode == 0, rc.stderr
HREF = 0.67552
H0 = HREF / 2997.92458
I0u = 3 * H0**2 * (0.12063 / HREF**2)
MU_CAP = 14.8 * HREF
MUS = {"cap": MU_CAP, "1e6hMpc": 1e6 * HREF}
AS = np.geomspace(1e-14, 1.0, 30)
KS = (1e-5, 1e-3, 0.1, 10.0)
pts = [(mk, mv, a_, k_) for mk, mv in MUS.items() for a_ in AS for k_ in KS]


def harness(rows):
    txt = "\n".join(f"{t} " + " ".join(f"{float(v):.17g}" for v in (m2, i0, lm, a_, k_)) for t, m2, i0, lm, a_, k_ in rows) + "\n"
    r = subprocess.run([os.path.join(HARN, "harness")], input=txt, capture_output=True, text=True)
    return [list(map(float, l.split())) for l in r.stdout.strip().splitlines()]


def rel(x, y):
    return abs(x - y) / max(abs(y), 1e-300)


# (i) lambda_D = 0 exactly: DBI == LIT
lit = harness([(3, mv**2, I0u, 0.0, a_, k_) for _, mv, a_, k_ in pts])
dbi0 = harness([(5, mv**2, I0u, 0.0, a_, k_) for _, mv, a_, k_ in pts])
m_i = max(rel(x, y) for r1, r2 in zip(dbi0, lit) for x, y in zip(r1, r2))
check("V_unit_i_lambda0_equals_LIT", len(dbi0) == len(pts) and m_i <= 1e-13,
      f"{len(pts)} points; max rel |DBI(lambda=0) - LIT| over (Q, K, K', c_ad^2, c_s^2) = {m_i:.2e}", "<= 1e-13")
# (ii) finite lambda_D vs BS Eqs. 88, 89a/b, 94a/b and Eq. 71 (mpmath; frozen 50 digits, A1 (ii-b) 120 digits)
LAMS = (1e-6, 1.0, 30.0, 1e6, 1e12, 1e24)
OUTS = {lm: harness([(5, mv**2, I0u, lm, a_, k_) for _, mv, a_, k_ in pts]) for lm in LAMS}


def unit_ii(dps):
  mp.mp.dps = dps
  worst = {}
  for lm in LAMS:
      out = OUTS[lm]
      mx = {"Q88": 0.0, "rho89a": 0.0, "p89b": 0.0, "w94a": 0.0, "cad94b": 0.0, "cs2_Eq71": 0.0}
      for (_, mv, a_, k_), (Qc, Kzc, Kpc, ca2c, cs2c) in zip(pts, out):
          M2, I, L, A, K = mp.mpf(mv)**2, mp.mpf(I0u), mp.mpf(lm), mp.mpf(a_), mp.mpf(k_)
          Zm = I / (2 * M2 * A**3)
          sq = mp.sqrt(1 + L * Zm**2)
          Q88 = 1 + 1 / mp.sqrt(L + (2 * M2 * A**3 / I)**2)
          rho = I / A**3 + 2 * M2 / L * (-1 + sq)
          p = 2 * M2 / L * (1 - 1 / sq)
          w = Zm / (1 + L * Zm**2 + (1 + Zm) * sq)
          cad = Zm / ((1 + L * Zm**2) * (sq + Zm))
          cs2 = cad / (1 + cad * K**2 / (A**2 * (rho + p) / 2))
          code = {"Q88": Qc, "rho89a": Qc * Kpc - Kzc, "p89b": Kzc, "w94a": Kzc / (Qc * Kpc - Kzc), "cad94b": ca2c, "cs2_Eq71": cs2c}
          ref = {"Q88": Q88, "rho89a": rho, "p89b": p, "w94a": w, "cad94b": cad, "cs2_Eq71": cs2}
          for n in mx:
              mx[n] = max(mx[n], float(abs(mp.mpf(code[n]) - ref[n]) / abs(ref[n])))
      worst[f"{lm:g}"] = mx
  return worst


worst = unit_ii(50)
m_ii = max(max(v.values()) for v in worst.values())
check("V_unit_ii_finite_lambda_vs_BS", m_ii <= 1e-10,
      f"lambda_D {list(worst)}: max rel = {m_ii:.2e}; worst per quantity " +
      ", ".join(f"{n} {max(v[n] for v in worst.values()):.1e}" for n in next(iter(worst.values()))),
      "<= 1e-10 (Q vs Eq.88, rho/p vs 89a/b, w/c_ad^2 vs 94a/b, c_s^2 vs Eq.71)", {"per_lambda": worst})
worst_b = unit_ii(120)
m_iib = max(max(v.values()) for v in worst_b.values())
check("V_unit_ii_b_120digits_A1", m_iib <= 1e-10,
      f"lambda_D {list(worst_b)}: max rel = {m_iib:.2e}; worst per quantity " +
      ", ".join(f"{n} {max(v[n] for v in worst_b.values()):.1e}" for n in next(iter(worst_b.values()))),
      "<= 1e-10 (A1: reference at 120 digits)", {"per_lambda": worst_b})
save()

# ------------------------------------------------------------------ run helpers (Q6's)
ENV = dict(os.environ, OMP_NUM_THREADS="1")
BASE = {"output": "tCl,pCl,lCl,mPk", "lensing": "yes", "l_max_scalars": 2600, "P_k_max_1/Mpc": 1.0,
        "write_parameters": "no", "thermodynamics_verbose": 1, "background_verbose": 2, "overwrite_root": "yes"}
PLANCK = {"omega_b": 0.02237, "h": 0.6736, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544}
OMC, OMCDM = 0.1200, 1e-8
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 20,
        "l_logstep": 1.026, "l_linstep": 25}
TOL7 = {"tol_perturbations_integration": 1e-7}
KHRON = {"aest_Q0": 1.0, "aest_K_B": 1.0, "aest_g": 1.0, "aest_lambda_c": -1.0}
KOFF = {**PLANCK, "omega_cdm": OMC}
KON = {**PLANCK, "omega_cdm": OMCDM, "omega_aest": OMC - OMCDM}
MU_P1, MU_P2 = 1 / 0.223, 1 / 22.3
RUNLOG = {}


def model(ktype, mu=None, lam=None):
    d = {**KHRON, "aest_K_type": ktype, "aest_K2": 1.0 if mu is None else mu**2}
    if lam is not None:
        d["aest_Z0"] = lam
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
        r = subprocess.run(["nice", "-n", "15", binary, ini], capture_output=True, text=True, env=ENV, timeout=timeout)
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


def ndiffs(A, B, R):
    a, b, r = A["cl"], B["cl"], R["cl"]
    assert np.array_equal(a[:, 0], b[:, 0]) and np.array_equal(a[:, 0], r[:, 0])
    m = (a[:, 0] >= 2) & (a[:, 0] <= 2500)
    d = {"TT": float(np.max(np.abs(b[m, 1] - a[m, 1]) / r[m, 1])),
         "EE": float(np.max(np.abs(b[m, 2] - a[m, 2]) / r[m, 2])),
         "TE": float(np.max(np.abs(b[m, 3] - a[m, 3]) / np.sqrt(r[m, 1] * r[m, 2]))),
         "pp": float(np.max(np.abs(b[m, 5] - a[m, 5]) / r[m, 5]))}
    pa, pb, pr = A["pk"], B["pk"], R["pk"]
    assert pa.shape == pb.shape and np.allclose(pa[:, 0], pb[:, 0], rtol=1e-6)      # model vs model: same grid
    km = (pa[:, 0] >= 1e-4) & (pa[:, 0] <= 1.0)
    if pr.shape == pa.shape and np.allclose(pa[:, 0], pr[:, 0], rtol=1e-6):
        ref = pr[km, 1]
    else:                                                                            # A1: reference onto the model grid
        ref = np.exp(np.interp(np.log(pa[km, 0]), np.log(pr[:, 0]), np.log(pr[:, 1])))
    d["pk"] = float(np.max(np.abs(pb[km, 1] - pa[km, 1]) / ref))
    return d


def fmt(d):
    return ", ".join(f"{k}={v:.2e}" for k, v in d.items())


# ------------------------------------------------------------------ V0: types 0 and 4 bit-identical to Q6's binary
okv0, txt0 = True, []
for nm, pr in (("DUST", model(0)), ("LOB14.8", model(4, MU_CAP))):
    a_ = run(f"V0_q6_{nm}", Q6BIN, {**KON, **pr})
    b_ = run(f"V0_dbi_{nm}", DBI, {**KON, **pr})
    same = a_ is not None and b_ is not None and np.array_equal(a_["cl"], b_["cl"]) and np.array_equal(a_["pk"], b_["pk"])
    okv0 &= bool(same)
    txt0.append(f"{nm}: {'identical' if same else 'DIFFERENT'}")
check("V0_types_0_4_bit_identical_to_Q6", okv0, "; ".join(txt0), "bit-identical C_l and P(k)")
save()

# ------------------------------------------------------------------ V1: lambda_D -> 0 vs Q6's LIT at mu_gate
P("== V1: DBI (lambda_D = 1e-25) vs Q6's LIT at the smallest mu_gate where Q6's binary runs LIT")
mu_gate, lit_o = None, None
for mh in (1e13, 1e14, 1e15, 1e16, 1e17):
    o = run(f"V1_q6LIT_{mh:g}", Q6BIN, {**KON, **model(3, mh * HREF), **TOL7})
    P(f"  Q6 LIT at {mh:g} h/Mpc: " + ("runs" if o is not None else f"refused: {RUNLOG[f'V1_q6LIT_{mh:g}'].get('failed', '')[-160:]!r}"))
    if o is not None:
        mu_gate, lit_o = mh, o
        break
RES["V1_mu_gate_hMpc"] = mu_gate
if mu_gate is None:
    check("V1_lambda0_vs_LIT", False, "no mu_gate in {1e13..1e17} h/Mpc: Q6's LIT never starts", "<= 1e-5 (NOT RUN)")
else:
    dbi_o = run(f"V1_dbi_l1e-25_{mu_gate:g}", DBI, {**KON, **model(5, mu_gate * HREF, 1e-25), **TOL7})
    dust_o = run("V1_dust", DBI, {**KON, **model(0), **TOL7})
    if dbi_o is None:
        check("V1_lambda0_vs_LIT", False, f"DBI run failed: {RUNLOG[f'V1_dbi_l1e-25_{mu_gate:g}']}", "<= 1e-5")
    else:
        d1 = diffs(lit_o, dbi_o)
        dld = diffs(dust_o, lit_o) if dust_o is not None else {}
        check("V1_lambda0_vs_LIT", max(d1.values()) <= 1e-5,
              f"mu_gate {mu_gate:g} h/Mpc: DBI(1e-25) vs LIT {fmt(d1)} | (reported) LIT vs DUST {fmt(dld)}",
              "every spectrum <= 1e-5 (tol 1e-7)", {"dbi_vs_lit": d1, "lit_vs_dust": dld})
save()
# AMENDMENT A1 supplementary gates V1b, V1c
if mu_gate is None:
    check("V1b_lambda0_bitwise_vs_LIT_A1", False, "no mu_gate", "bit-identical")
    check("V1c_noise_floor_A1", False, "no mu_gate", "<= max(1e-5, 2N)")
else:
    db0 = run(f"V1b_dbi_l0_{mu_gate:g}", DBI, {**KON, **model(5, mu_gate * HREF, 0.0), **TOL7})
    same = db0 is not None and np.array_equal(db0["cl"], lit_o["cl"]) and np.array_equal(db0["pk"], lit_o["pk"])
    check("V1b_lambda0_bitwise_vs_LIT_A1", bool(same), f"DBI(lambda_D = 0) vs Q6 LIT at {mu_gate:g} h/Mpc: "
          + ("bit-identical" if same else "DIFFERENT"), "bit-identical C_l and P(k) (A1)")
    pert = {**KON, **model(3, mu_gate * HREF), **TOL7}
    pert["aest_K2"] = (mu_gate * HREF) ** 2 * (1 + 1e-10)
    lp = run(f"V1c_q6LIT_mu2x(1+1e-10)_{mu_gate:g}", Q6BIN, pert)
    if lp is None or dbi_o is None:
        check("V1c_noise_floor_A1", False, f"run failed: {RUNLOG.get(f'V1c_q6LIT_mu2x(1+1e-10)_{mu_gate:g}')}", "<= max(1e-5, 2N)")
    else:
        Nf = diffs(lit_o, lp)
        thr1c = {k: max(1e-5, 2 * Nf[k]) for k in Nf}
        check("V1c_noise_floor_A1", all(d1[k] <= thr1c[k] for k in d1),
              f"DBI(1e-25) vs LIT {fmt(d1)} | N (LIT at mu^2(1+1e-10) vs mu^2) {fmt(Nf)}",
              "each <= max(1e-5, 2N) (A1)", {"dbi_vs_lit": d1, "noise_floor": Nf})
save()

# ------------------------------------------------------------------ V2: lambda_D -> infinity vs DUST, both gauges
for gname in ("synchronous", "newtonian"):
    g = {"gauge": gname}
    dd = run(f"V2_dust_{gname}", DBI, {**KON, **model(0), **TOL7, **g})
    db = run(f"V2_dbi_cap_l1e30_{gname}", DBI, {**KON, **model(5, MU_CAP, 1e30), **TOL7, **g})
    if dd is None or db is None:
        check(f"V2_lambda_inf_vs_DUST_{gname}", False, f"CLASS failed: {RUNLOG.get(f'V2_dbi_cap_l1e30_{gname}')}", "<= 1e-4; <= 1e-6")
        continue
    d2 = diffs(dd, db)
    bg = {"theta_s": abs(db["theta_s"] / dd["theta_s"] - 1), "rs_drag": abs(db["rs_drag"] / dd["rs_drag"] - 1)}
    check(f"V2_lambda_inf_vs_DUST_{gname}", max(d2.values()) <= 1e-4 and max(bg.values()) <= 1e-6,
          fmt(d2) + f"; 100theta_s {bg['theta_s']:.1e}, r_drag {bg['rs_drag']:.1e}",
          "<= 1e-4 every spectrum; background <= 1e-6", {"diffs": d2, "background": bg})
save()

if MUT:                                                   # MUTATE: V_unit (ii) and V2 must fail; nothing else needed
    RES["runs"] = RUNLOG
    save()
    P(f"Q7_VALIDATE COMPLETE: {NP}/{NC} checks PASS.")
    OUT.close()
    sys.exit(0 if NP == NC else 1)

# ------------------------------------------------------------------ V3: gauge (A3 form), DBI P1 and C30
P1 = {**KON, **model(5, MU_P1, 30.0)}
C30 = {**KON, **model(5, MU_CAP, 30.0)}
v_def = run("V3_van_default", VAN, KOFF)
v_nw = run("V3_van_newtonian", VAN, {**KOFF, "gauge": "newtonian"})
d3v = ndiffs(v_def, v_nw, v_def)
thr3 = {k: max(1e-3, 3 * d3v[k]) for k in d3v}
p1_def = None
for lab, pr in (("P1", P1), ("C30", C30)):
    a_sy = run(f"V3_{lab}_synchronous", DBI, pr)
    a_nw = run(f"V3_{lab}_newtonian", DBI, {**pr, "gauge": "newtonian"})
    if a_sy is None or a_nw is None:
        check(f"V3_gauge_{lab}", False, f"CLASS failed: {RUNLOG.get(f'V3_{lab}_synchronous')} {RUNLOG.get(f'V3_{lab}_newtonian')}", "")
        continue
    if lab == "P1":
        p1_def = a_sy
    d3 = ndiffs(a_sy, a_nw, v_def)
    check(f"V3_gauge_{lab}", all(d3[k] <= thr3[k] for k in thr3), "DBI " + fmt(d3) + " | vanilla " + fmt(d3v),
          "|dX|/X_LCDM each <= max(1e-3, 3 x vanilla)", {"dbi": d3, "vanilla": d3v})
    RES[f"{lab}_vs_LCDM_same_params"] = diffs(v_def, a_sy)
    P(f"  (reported) DBI {lab} vs pristine LCDM at the same parameters: {fmt(RES[f'{lab}_vs_LCDM_same_params'])}")
save()

# ------------------------------------------------------------------ V4: convergence (same k grid), DBI P1
K20 = {"k_per_decade_for_pk": 20}
c_d20 = run("V4_P1_default_k20", DBI, {**P1, **K20})
c_hi = run("V4_P1_high", DBI, {**P1, **HIGH})
v_d20 = run("V4_van_default_k20", VAN, {**KOFF, **K20})
v_hi = run("V4_van_high", VAN, {**KOFF, **HIGH})
d4, d4v = ndiffs(c_d20, c_hi, v_hi), ndiffs(v_d20, v_hi, v_hi)
thr4 = {k: max(2e-3, 2 * d4v[k]) for k in d4}
check("V4_convergence_same_grid", all(d4[k] <= thr4[k] for k in d4), "DBI P1 " + fmt(d4) + " | vanilla " + fmt(d4v),
      "|dX|/X_LCDM each <= max(2e-3, 2 x vanilla)", {"dbi": d4, "vanilla": d4v})
save()

# ------------------------------------------------------------------ V5: IC attractor, start x0.25 vs x0.125, DBI P1
Q4 = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25}
Q8 = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.125, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.125}
c4_, c8_ = run("V5_P1_x0.25", DBI, {**P1, **Q4}), run("V5_P1_x0.125", DBI, {**P1, **Q8})
v4_, v8_ = run("V5_van_x0.25", VAN, {**KOFF, **Q4}), run("V5_van_x0.125", VAN, {**KOFF, **Q8})
d5, d5v = diffs(c4_, c8_, pk=False), diffs(v4_, v8_, pk=False)
d5["pk"], d5v["pk"] = ndiffs(c4_, c8_, v4_)["pk"], ndiffs(v4_, v8_, v4_)["pk"]
check("V5_ic_attractor_x0.25", all(d5[k] <= d5v[k] + 1e-4 for k in d5), "DBI P1 " + fmt(d5) + " | vanilla " + fmt(d5v),
      "each <= vanilla + 1e-4 (C_l relative, P(k) in units of LCDM)", {"dbi": d5, "vanilla": d5v})
frozen_ready = all(c["pass"] for n, c in RES["checks"].items() if not n.endswith("_A1"))
A1SET = ("V_prov", "V_unit_i_lambda0_equals_LIT", "V_unit_ii_b_120digits_A1", "V0_types_0_4_bit_identical_to_Q6",
         "V1b_lambda0_bitwise_vs_LIT_A1", "V1c_noise_floor_A1", "V2_lambda_inf_vs_DUST_synchronous",
         "V2_lambda_inf_vs_DUST_newtonian", "V3_gauge_P1", "V3_gauge_C30", "V4_convergence_same_grid", "V5_ic_attractor_x0.25")
ready = all(RES["checks"].get(n, {"pass": False})["pass"] for n in A1SET)
RES["dbi_ready_frozen_this_build"] = frozen_ready
RES["dbi_ready_A1_this_build"] = ready
P(f"  DBI ready (frozen gates) on this build: {frozen_ready}")
RES["runs"] = RUNLOG
save()
P(f"  DBI ready (A1 gates) on this build: {ready}; elapsed {RES['elapsed_s']} s")
P(f"Q7_VALIDATE COMPLETE: {NP}/{NC} checks PASS.")
OUT.close()
sys.exit(0 if NP == NC else 1)
