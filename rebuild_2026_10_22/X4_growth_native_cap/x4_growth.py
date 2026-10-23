#!/usr/bin/env python3
"""X4_growth_native_cap step 0 (G0a-c) + step 1, question (i) (FROZEN_CRITERIA.md sections 1-3, committed alone first):
v3's linear growth at the mu_K that S4's isolated-galaxy guard allows (0.03 Mpc^-1 passes, 0.1 Mpc^-1 fails; physical).

  OMP_NUM_THREADS=1 nice -n 15 python3 -I x4_growth.py              -> x4_growth.out, x4_growth_results.json
  X4_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 -I x4_growth.py  -> *_MUTATE.out / *_MUTATE.json (G0a and G0b must FAIL)

Estimators: F3's sub-horizon ODE (copied verbatim, J_x kernel, a_i = 1e-3 primary) and Q6's validated Khronon CLASS (LOB,
read-only use of the built binary). a0 is absent at linear order: neither footing enters; kappa = 1/2 FITTED does not enter.
No PM simulation; no download; no mu_K other than 0.03 and 0.1 Mpc^-1 (stop rule).
"""
import json
import math
import os
import re
import resource
import shutil
import subprocess
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

T0 = time.time()
MUT = os.environ.get("X4_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
KHR = os.path.join(EXT, "class_khronon_build_2026_10_23", "class_khronon_mutate" if MUT else "class_khronon", "class")
RUNS = os.path.join(EXT, "x4_growth_native_cap_2026_10_23", f"runs_step1{TAG}")
shutil.rmtree(RUNS, ignore_errors=True)
os.makedirs(RUNS, exist_ok=True)
OUT = open(os.path.join(HERE, f"x4_growth{TAG}.out"), "w")
RES = {"lane": "X4_growth_native_cap", "script": "x4_growth.py", "date": "2026-10-23", "mutate": MUT, "checks": {},
       "note": "a0 absent at linear order (neither footing enters); kappa = 1/2 FITTED; omega_K FITTED; numbers only"}
NP = NC = 0


def P(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    OUT.write(s + "\n")
    OUT.flush()


def check(name, ok, value, thr):
    global NP, NC
    NC += 1
    NP += bool(ok)
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {value}   (line: {thr})")
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}


def save():
    RES["elapsed_s"] = round(time.time() - T0, 1)
    RES["peak_rss_GB_self"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    RES["peak_rss_GB_children"] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1e9
    json.dump(RES, open(os.path.join(HERE, f"x4_growth_results{TAG}.json"), "w"), indent=1, default=float)


P(__doc__)
P(f"MUTATE = {MUT}; Q6 binary: {os.path.relpath(KHR, REPO)}")

F3R = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F3_growth_audit", "f3_growth_audit_results.json")))
Q6R = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "Q6_v3_class", "q6_native_results.json")))

# ------------------------------------------------------------------ F3's growth solvers, copied verbatim (f3_growth_audit.py L88-150)
# (the only change: under X4_MUTATE the kernel is replaced by s = 1, the no-hold control of FROZEN_CRITERIA section 5)


def make_E(Om, h, rad=True):
    Or = (4.18e-5 / h ** 2) if rad else 0.0
    OL = 1.0 - Om - Or
    return (lambda a: math.sqrt(Om * a ** -3 + Or * a ** -4 + OL)), Or


def growth_ratio(kk, mu_h, Om, Ob, h, kernel="jeans", a_i=1e-3, rad=True):
    """two-fluid sub-horizon growth (baryons Newtonian at every k; BS dust kernel s(x), x = k/(a mu)); returns
    delta_m(k, a = 1) / delta_m(mu -> inf).  Vectorised over kk (h/Mpc)."""
    Ek, Or = make_E(Om, h, rad); OK = Om - Ob; kk = np.asarray(kk, float); n = len(kk)
    def s_of(a, mu):
        if mu is None: return np.ones(n)
        if MUT: return np.ones(n)                                    # MUTATE: no hold
        x2 = (kk / (a * mu)) ** 2
        return (1.0 - x2) if kernel == "jeans" else 1.0 / (1.0 + x2)
    def solve(mu):
        def rhs(x, st):
            a = math.exp(x); E = Ek(a); eps = 1e-6
            dlnE = (math.log(Ek(a * math.exp(eps))) - math.log(Ek(a * math.exp(-eps)))) / (2 * eps)
            dens = 1.5 * a ** -3 / E ** 2
            db, gb, dk, gk = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
            src_b = dens * (Ob * db + OK * dk); src_k = dens * (Ob * db + OK * dk * s_of(a, mu))
            return np.concatenate([gb, -(2 + dlnE) * gb + src_b, gk, -(2 + dlnE) * gk + src_k])
        st0 = np.concatenate([np.full(n, a_i), np.full(n, a_i), np.full(n, a_i), np.full(n, a_i)])
        sol = solve_ivp(rhs, [math.log(a_i), 0.0], st0, method="DOP853", rtol=1e-7, atol=1e-12)
        y_ = sol.y[:, -1]; return (Ob * y_[:n] + OK * y_[2 * n:3 * n]) / Om
    return solve(mu_h) / solve(None)


from classy import Class


def class_run(wb, wc, h, lnA, ns, tau=0.0544, zs=(0.0,)):
    c = Class(); c.set({"omega_b": wb, "omega_cdm": wc, "h": h, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau, "N_ur": 3.044,
                        "T_cmb": 2.7255, "output": "mPk", "P_k_max_h/Mpc": 60.0, "z_max_pk": 4.0})
    c.compute(); return c


KS = np.geomspace(1e-4, 50.0, 1500)


def pk0(c, h):   # (Mpc/h)^3 at k in h/Mpc, z = 0, linear
    return np.array([c.pk_lin(k * h, 0.0) for k in KS]) * h ** 3


W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3


def sig8(Pk, T=None):
    Pk = Pk if T is None else Pk * T ** 2
    return math.sqrt(np.trapz(Pk * W8(KS * 8.0) ** 2 * KS ** 2, KS) / (2 * math.pi ** 2))


KT = np.geomspace(1e-3, 3.0, 36)


def sig8_ratio(Pk, mu_h, Om, Ob, h, kernel, a_i):
    T = growth_ratio(KT, mu_h, Om, Ob, h, kernel, a_i)
    Tf = np.interp(np.log(KS), np.log(KT), T, left=T[0], right=T[-1])
    return sig8(Pk, Tf) / sig8(Pk), T


# ------------------------------------------------------------------ background A (F3's stored parameters) and the conversion
pa = F3R["K2"]["A_c2b_refit"]["params"]
hA = pa["h"]
cA = class_run(pa["omega_b"], pa["omega_cdm"], hA, pa["lnAs"], pa["n_s"], pa["tau"])
PkA = pk0(cA, hA)
OmA, ObA = (pa["omega_b"] + pa["omega_cdm"]) / hA ** 2, pa["omega_b"] / hA ** 2
s8A = cA.sigma8()
P(f"== background A (F3 K2): h_A = {hA:.10f}, Omega_m {OmA:.6f}, Omega_b {ObA:.6f}, sigma8 {s8A:.6f} "
  f"(F3 stored {F3R['K2']['A_c2b_refit']['sigma8']:.6f})")
cA.struct_cleanup()

MU_CAP_PHYS = 10.0                                   # Mpc^-1 (mu^-1 = 100 kpc), BS24 Eq. 39
mu_cap_h = MU_CAP_PHYS / hA
f3_cap = F3R["K4"]["BS24_Eq39_edge_100kpc"]
check("G0c_conversion", abs(mu_cap_h / f3_cap["mu_hMpc"] - 1) <= 1e-9,
      f"10 Mpc^-1 / h_A = {mu_cap_h:.10f} h/Mpc vs F3's mu_hMpc {f3_cap['mu_hMpc']:.10f}", "<= 1e-9 relative")
MU_GUARD = {"0.03": 0.03, "0.1": 0.1}                # Mpc^-1, physical (S4's grid: 0.03 passes, 0.1 fails, both footings)
CONV = {k: {"mu_per_Mpc_phys": v, "mu_hMpc_at_hA": v / hA, "mu_inv_Mpc_phys": 1 / v} for k, v in MU_GUARD.items()}
RES["conversion"] = {"h_A": hA, "rule": "mu[h/Mpc] = mu[Mpc^-1] / h_A; S4's mu_K is physical Mpc^-1; CLASS aest_K2 = mu^2 [Mpc^-2]",
                     "cap": {"mu_per_Mpc_phys": MU_CAP_PHYS, "mu_hMpc_at_hA": mu_cap_h}, "guard_points": CONV}
for k, v in CONV.items():
    P(f"  mu_K = {k} Mpc^-1 (physical; mu^-1 = {v['mu_inv_Mpc_phys']:.4g} Mpc) = {v['mu_hMpc_at_hA']:.6f} h/Mpc at h_A")
save()

# ------------------------------------------------------------------ G0a: F3 K4 reproduced at the cap
P("== G0a: F3's ODE copy reproduces F3 K4 at the BS24 cap (background A)")
G0A = {}
for col, kern, ai in (("bsk2_ai0.001", "bsk2", 1e-3), ("bsk2_ai0.0001", "bsk2", 1e-4), ("jeans_ai0.001", "jeans", 1e-3)):
    r_, _ = sig8_ratio(PkA, mu_cap_h, OmA, ObA, hA, kern, ai)
    G0A[col] = {"this": r_, "F3": f3_cap[col]["sigma8_ratio"]}
    P(f"  {col}: {r_:.6f} vs F3 {f3_cap[col]['sigma8_ratio']:.6f}")
RES["G0a"] = G0A
check("G0a_F3_ODE_reproduced", all(abs(v["this"] / v["F3"] - 1) <= 1e-4 for v in G0A.values()),
      "; ".join(f"{k} {v['this']:.6f} vs {v['F3']:.6f}" for k, v in G0A.items()), "each |r/r_F3 - 1| <= 1e-4")
save()

# ------------------------------------------------------------------ step 1, ODE at the guard points
P("== step 1 ODE: F3's ODE at mu_K = 0.03 and 0.1 Mpc^-1 (physical), background A")
ODE = {}
for lab, mu in MU_GUARD.items():
    mu_h = mu / hA
    ODE[lab] = {"mu_hMpc_at_hA": mu_h}
    for col, kern, ai in (("bsk2_ai0.001", "bsk2", 1e-3), ("bsk2_ai0.0001", "bsk2", 1e-4),
                          ("jeans_ai0.001", "jeans", 1e-3), ("jeans_ai0.0001", "jeans", 1e-4)):
        if kern == "jeans" and (3.0 / (ai * mu_h)) > 3000:          # F3's own skip rule (f3_growth_audit.py L232)
            ODE[lab][col] = None
            P(f"  mu {lab}: {col} skipped by F3's rule (3/(a_i mu_h) = {3.0 / (ai * mu_h):.3g} > 3000)")
            continue
        r_, T_ = sig8_ratio(PkA, mu_h, OmA, ObA, hA, kern, ai)
        ODE[lab][col] = {"sigma8_ratio": r_, "sigma8": r_ * s8A, "T_at_k": {f"{k_:.4g}": float(t_) for k_, t_ in zip(KT[::5], T_[::5])}}
        P(f"  mu {lab} Mpc^-1 ({mu_h:.5f} h/Mpc): {col} sigma8 ratio {r_:.6f} (sigma8 {r_ * s8A:.5f})")
RES["ode"] = ODE
save()

# ------------------------------------------------------------------ Q6's Boltzmann (LOB), runner copied from q6_native.py
P("== step 0/1 Boltzmann: Q6's validated Khronon CLASS (LOB), C7 LCDM refit P0, Q6 precision (high + start x0.25)")
C7F = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C7_aest_class", "c7_native_results.json")))["fits"]["LCDM"]
P0 = np.array([C7F["params"][k] for k in ("omega_b", "omega_dm(FITTED)", "100theta_s", "ln10^10A_s", "n_s", "tau")])
ENV = dict(os.environ, OMP_NUM_THREADS="1")
HIGH = {"tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 20,
        "l_logstep": 1.026, "l_linstep": 25}
START = {"start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25}
TCMB = 2.7255
OMCDM = 1e-8
HREF = 0.67552
KH = {"aest_Q0": 1.0, "aest_K_B": 1.0, "aest_g": 1.0, "aest_lambda_c": -1.0}
FAILMSG = {}
RUNINFO = {}


def run(name, binary, params):
    p = {"output": "tCl,pCl,lCl,mPk", "lensing": "yes", "l_max_scalars": 2508,
         "T_cmb": TCMB, "write_parameters": "no", "input_verbose": 1, "background_verbose": 2,
         "fourier_verbose": 1, "overwrite_root": "yes", **HIGH, **START, **params}
    p["P_k_max_h/Mpc"] = 10.0
    root = os.path.join(RUNS, name + "_")
    p["root"] = root
    with open(root + ".ini", "w") as fh:
        for k_, v_ in p.items():
            fh.write(f"{k_} = {v_}\n")
    t_launch = time.time()
    rss0 = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    try:
        r = subprocess.run(["nice", "-n", "15", binary, root + ".ini"], capture_output=True, text=True, env=ENV, timeout=1800)
    except subprocess.TimeoutExpired:
        FAILMSG[name] = "timeout 1800 s"
        return None
    RUNINFO[name] = {"seconds": round(time.time() - t_launch, 1),
                     "children_peak_rss_GB_so_far": max(rss0, resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss) / 1e9}
    if r.returncode != 0:
        FAILMSG[name] = (r.stdout + r.stderr).strip().splitlines()[-1][-300:]
        return None
    assert os.path.getmtime(root + "_pk.dat") >= t_launch - 1, "stale-output guard"
    log = r.stdout
    out = {}
    m = re.search(r"found 'h = ([0-9.eE+-]+)'", log)
    out["h"] = float(m.group(1)) if m else np.nan
    m = re.search(r"sigma8=([0-9.]+) for total matter", log)
    out["sigma8"] = float(m.group(1)) if m else np.nan
    out["pk"] = np.loadtxt(root + "_pk.dat")
    return out


def params(ktype, mu_phys=None):
    wb, wd, th, lnA, ns, tau = P0
    return {"omega_b": wb, "100*theta_s": th, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau,
            "omega_cdm": OMCDM, "omega_aest": wd - OMCDM, **KH, "aest_K_type": ktype,
            "aest_K2": 1.0 if mu_phys is None else mu_phys ** 2}


B = {}
B["DUST"] = run("DUST_fix", KHR, params(0))
B["LOB_14.8"] = run("LOB_14.8_fix", KHR, params(4, 14.8 * HREF))
q6d, q6l = Q6R["fixed"]["DUST"]["sigma8"], Q6R["fixed"]["LOB_14.8"]["sigma8"]
q6rb = Q6R["fixed"]["LOB_14.8"]["R_B"]
okb = B["DUST"] is not None and B["LOB_14.8"] is not None
rb_cap = (B["LOB_14.8"]["sigma8"] / B["DUST"]["sigma8"]) if okb else np.nan
check("G0b_Q6_reproduced", okb and abs(B["DUST"]["sigma8"] / q6d - 1) <= 1e-4 and abs(B["LOB_14.8"]["sigma8"] / q6l - 1) <= 1e-4
      and abs(rb_cap / q6rb - 1) <= 1e-4,
      f"DUST sigma8 {B['DUST']['sigma8'] if B['DUST'] else None} vs Q6 {q6d}; LOB 14.8 {B['LOB_14.8']['sigma8'] if B['LOB_14.8'] else None} "
      f"vs Q6 {q6l}; R_B {rb_cap:.6f} vs Q6 {q6rb:.6f}", "each <= 1e-4 relative")
save()

P("== step 1 Boltzmann: LOB at mu_K = 0.03 and 0.1 Mpc^-1 (aest_K2 = mu^2; no h enters)")
RB = {"cap_14.8hMpc": rb_cap}
for lab, mu in MU_GUARD.items():
    o = run(f"LOB_{lab}perMpc_fix", KHR, params(4, mu))
    B[f"LOB_{lab}"] = o
    if o is None:
        RB[lab] = None
        P(f"  mu {lab} Mpc^-1: CLASS did not complete: {FAILMSG.get(f'LOB_{lab}perMpc_fix')}")
        continue
    RB[lab] = o["sigma8"] / B["DUST"]["sigma8"] if B["DUST"] else np.nan
    a = B["DUST"]["pk"]
    rat = {f"{k_:g}": float(np.exp(np.interp(np.log(k_), np.log(o["pk"][:, 0]), np.log(o["pk"][:, 1]))
                                   - np.interp(np.log(k_), np.log(a[:, 0]), np.log(a[:, 1])))) for k_ in (0.1, 0.3, 1.0, 3.0, 10.0)}
    RES.setdefault("boltzmann_Pk_over_DUST_z0", {})[lab] = rat
    P(f"  mu {lab} Mpc^-1: sigma8 {o['sigma8']:.6g}, R_B = {RB[lab]:.6f}; P/P_DUST(z=0) at k[h/Mpc] "
      + ", ".join(f"{k_}: {v:.3e}" for k_, v in rat.items()) + f"; {RUNINFO[f'LOB_{lab}perMpc_fix']}")
RES["R_B"] = RB
RES["runinfo"] = RUNINFO
RES["class_failures"] = FAILMSG
check("G2_boltzmann_runs_complete", all(RB.get(l) is not None for l in MU_GUARD)
      and all(v["seconds"] <= 1800 for v in RUNINFO.values()),
      f"R_B: {RB}; runs {RUNINFO}", "both LOB runs complete, each <= 30 min (FAIL allowed; then the ODE alone is used)")
save()

# ------------------------------------------------------------------ reported: the literal quadratic background at these mu (Q7's step-B algebra, lambda_D = 0)
HUB = 1.0 / 2997.92458
H0 = HREF * HUB
OMK = P0[1] / HREF ** 2
OMG = 2.4728e-5 * (TCMB / 2.7255) ** 4 / HREF ** 2 * 1.0
OMR = OMG * (1 + 3.044 * 7 / 8 * (4 / 11) ** (4 / 3))
TMEV0 = 8.617333e-11 * TCMB


def a_of_T(T_MeV, gs):
    return (TMEV0 / T_MeV) * (3.909 / gs) ** (1 / 3)


BBN1 = (a_of_T(1.0, 10.75), 10.75 / (2 + 3.044 * 7 / 8 * (4 / 11) ** (4 / 3) * 2) * (3.909 / 10.75) ** (4 / 3), 10.75 / 1.75)


def rho8(a, I0, m2, lam):
    Z = I0 / (2 * m2 * a ** 3)
    r = math.sqrt(1 + lam * Z * Z)
    return I0 / a ** 3 + 2 * m2 * Z * Z / (r + 1)


def I0_root(m2, lam):
    tgt = 3 * H0 ** 2 * OMK
    return brentq(lambda I: rho8(1.0, I, m2, lam) - tgt, 1e-3 * tgt, tgt, xtol=1e-30, rtol=1e-14)


LIT = {}
for lab, mu in {**MU_GUARD, "cap": 14.8 * HREF}.items():
    m2 = mu ** 2
    I0 = I0_root(m2, 0.0)
    aT, fr, nrel = BBN1
    LIT[lab] = {"dNeff_equiv_1MeV_literal_quadratic": rho8(aT, I0, m2, 0.0) / (3 * H0 ** 2 * OMR / aT ** 4 * fr) * nrel,
                "a_at_eps_1": (I0 / (2 * m2)) ** (1 / 3)}
    P(f"  reported: literal quadratic K at mu = {lab}: dNeff,equiv(1 MeV) = {LIT[lab]['dNeff_equiv_1MeV_literal_quadratic']:.3e}; "
      f"Qbar - 1 = 1 at a = {LIT[lab]['a_at_eps_1']:.4g} (BBN line 0.5)")
okc = abs(LIT["cap"]["dNeff_equiv_1MeV_literal_quadratic"] / Q6R["stepB"]["rows"]["14.8"]["dNeff_equiv_1MeV"] - 1) <= 1e-3
RES["literal_background_reported"] = LIT
RES["literal_background_reported"]["cap_reproduces_Q6_stepB"] = bool(okc)
save()

# ------------------------------------------------------------------ G1: monotone sanity
cap_ode = {c: f3_cap[c]["sigma8_ratio"] for c in ("bsk2_ai0.001", "bsk2_ai0.0001")}
mono = []
for c in cap_ode:
    if ODE["0.03"].get(c) and ODE["0.1"].get(c):
        mono.append(ODE["0.03"][c]["sigma8_ratio"] <= ODE["0.1"][c]["sigma8_ratio"] <= cap_ode[c])
if RB.get("0.03") is not None and RB.get("0.1") is not None:
    mono.append(RB["0.03"] <= RB["0.1"] <= rb_cap)
check("G1_monotone_in_mu", len(mono) > 0 and all(mono),
      "ODE " + "; ".join(f"{c}: {ODE['0.03'][c]['sigma8_ratio']:.5f} <= {ODE['0.1'][c]['sigma8_ratio']:.5f} <= {cap_ode[c]:.5f}"
                         for c in cap_ode if ODE['0.03'].get(c) and ODE['0.1'].get(c))
      + (f"; R_B {RB['0.03']:.5f} <= {RB['0.1']:.5f} <= {rb_cap:.5f}" if RB.get("0.03") is not None and RB.get("0.1") is not None else ""),
      "R(0.03) <= R(0.1) <= R(cap) for every estimator")
save()

# ------------------------------------------------------------------ gap factors
K5 = F3R["K5"]["windows"]
mu95_F3 = {k: {"mu_hMpc": v["mu_min_hMpc"], "mu_per_Mpc_phys": v["mu_min_hMpc"] * hA} for k, v in K5.items()}
mu95_Q6_lower = {"mu_hMpc": 2542.0, "mu_per_Mpc_phys": 2542.0 * HREF, "note": "Q6: R_B(2542 h/Mpc) = 0.8827 < 0.95, so mu_95 > 2542 h/Mpc"}
GAP = {"sigma8_shortfall_0.95_over_R": {}, "mu_gap_mu95_over_mu_guard": {}}
for lab in MU_GUARD:
    row = {}
    if RB.get(lab):
        row["R_B"] = 0.95 / RB[lab]
    for c in ("bsk2_ai0.001", "bsk2_ai0.0001"):
        if ODE[lab].get(c):
            row[f"ODE_{c}"] = 0.95 / ODE[lab][c]["sigma8_ratio"]
    GAP["sigma8_shortfall_0.95_over_R"][lab] = row
    g = {f"F3_{k}": v["mu_per_Mpc_phys"] / MU_GUARD[lab] for k, v in mu95_F3.items()}
    g["Q6_boltzmann_lower_bound"] = mu95_Q6_lower["mu_per_Mpc_phys"] / MU_GUARD[lab]
    GAP["mu_gap_mu95_over_mu_guard"][lab] = g
GAP["mu95_inherited"] = {"F3_K5": mu95_F3, "Q6": mu95_Q6_lower}
RES["gaps"] = GAP
for lab in MU_GUARD:
    P(f"  gaps at mu_K = {lab} Mpc^-1: 0.95/R = " + ", ".join(f"{k} {v:.3g}" for k, v in GAP["sigma8_shortfall_0.95_over_R"][lab].items())
      + "; mu_95/mu_guard = " + ", ".join(f"{k} {v:.4g}" for k, v in GAP["mu_gap_mu95_over_mu_guard"][lab].items()))

# ------------------------------------------------------------------ verdict (i), frozen classes (FROZEN_CRITERIA section 3)
prim = "R_B" if (RB.get("0.03") is not None and RB.get("0.1") is not None) else "ODE_bsk2_ai0.001"
def R_of(lab, which):
    if which == "R_B":
        return RB.get(lab)
    return ODE[lab]["bsk2_ai0.001"]["sigma8_ratio"]
r03p, r10p = R_of("0.03", prim), R_of("0.1", prim)
r10o = R_of("0.1", "ODE_bsk2_ai0.001")
g1ok = RES["checks"]["G1_monotone_in_mu"]["pass"]
repro_ok = RES["checks"]["G0a_F3_ODE_reproduced"]["pass"] and (RES["checks"]["G0b_Q6_reproduced"]["pass"] or prim != "R_B")
if not repro_ok:
    vi = "UNDECIDED (reproduction failed)"
elif r10p < 0.95 and r10o < 0.95 and g1ok:
    vi = "GROWTH FAILS AT THE NATIVE CAP"
elif r03p >= 0.95 and g1ok:
    vi = "GROWTH PASSES AT THE NATIVE CAP"
else:
    vi = "UNDECIDED"
RES["verdict_i"] = {"class": vi, "primary_estimator": prim, "R_primary": {"0.03": r03p, "0.1": r10p},
                    "R_ODE_bsk2_ai0.001": {"0.03": R_of("0.03", "ODE_bsk2_ai0.001"), "0.1": r10o},
                    "guard_edge_bracket": "S4's guard edge lies in (0.03, 0.1) Mpc^-1; with G1 monotonicity R(edge) lies in [R(0.03), R(0.1))"}
check("V_i_verdict", True, f"{vi}: primary {prim} R(0.03) = {r03p:.5f}, R(0.1) = {r10p:.5f}; ODE (a_i 1e-3) R(0.1) = {r10o:.5f}",
      "computed (the verdict is a result)")
save()
P(f"X4 STEP 1 COMPLETE: {NP}/{NC} checks PASS; elapsed {time.time() - T0:.0f} s; peak RSS self "
  f"{RES['peak_rss_GB_self']:.2f} GB, children {RES['peak_rss_GB_children']:.2f} GB")
sys.exit(0 if NP == NC else 1)
