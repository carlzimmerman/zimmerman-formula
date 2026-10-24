#!/usr/bin/env python3
"""X15_c1_preferred_frame: does C1 (the khronon K^2 term, Horava lambda = 1 + beta) inside X14's window survive the
preferred-frame PPN bounds, and does it leave galaxy statics/dynamics intact in v3s?
Frozen criteria: FROZEN_CRITERIA.md (committed alone with ASSUMPTION_LEDGER.md and LITERATURE_MAP.md).

Part S0  reproductions (stop rule)                         -> checks S0-1 .. S0-5
Part D   step 1: alpha_1(k), alpha_2(k) of v3s + C1          -> checks D1, D2, X-BPS, P-A1, P-A2, P-LIN, P-RES
Part W   step 2: the window intersected with the bounds      -> verdict
Part T   step 3 (reported): Mach numbers, moving-galaxy rotation curve, Cherenkov   -> check S3-1 (derivation only)

Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x15_c1_preferred_frame.py               (exit 0 iff all pass)
      PYTHONHASHSEED=0 X15_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 x15_c1_preferred_frame.py  (m1..m5; exit 1)

kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. No dark-matter particle.
Not theory closed. Units c = 1 in the symbolic part; K = 4 pi G.
"""
import hashlib
import json
import math
import os
import resource
import subprocess
import sys
import time

import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations

MUTATE = os.environ.get("X15_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"x15_c1_preferred_frame{TAG}.out")
JS = os.path.join(HERE, f"x15_c1_preferred_frame_results{TAG}.json")
T0 = time.time()
_lines = []
CHECKS = []
RES = {"mutate": MUTATE, "checks": CHECKS}


def log(s=""):
    print(s, flush=True)
    _lines.append(s)


def check(cid, ok, value, line, required=True):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": str(value), "line": line, "required": required})
    log(f"  [{'PASS' if ok else 'FAIL'}] {cid}: {value}   (line: {line})")
    return ok


def rss_gb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e9 if sys.platform == "darwin" else r * 1024 / 1e9


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, (np.floating, float)):
        return float(o)
    if isinstance(o, (np.integer, int)):
        return int(o)
    if isinstance(o, sp.Basic):
        return str(o)
    return o


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def finish(exit_code=None):
    RES["runtime_s"] = time.time() - T0
    RES["peak_rss_gb"] = rss_gb()
    req_fail = [c["id"] for c in CHECKS if c["required"] and not c["pass"]]
    RES["required_failures"] = req_fail
    log(f"checks {sum(c['pass'] for c in CHECKS)}/{len(CHECKS)} pass; required failures {req_fail}; "
        f"{RES['runtime_s']:.0f} s; peak RSS {RES['peak_rss_gb']:.3f} GB")
    with open(OUT, "w") as fh:
        fh.write("\n".join(_lines) + "\n")
    with open(JS, "w") as fh:
        json.dump(clean(RES), fh, indent=1)
    sys.exit((0 if not req_fail else 1) if exit_code is None else exit_code)


# ------------------------------------------------------------------------------------------- constants (RAW / FITTED)
G = 6.67430e-11
C_SI = 299792458.0
GM_SUN = 1.32712440018e20
M_SUN = GM_SUN / G
M_EARTH = 5.9722e24
AU = 1.495978707e11
KPC = 3.0856775814913673e19
PC = KPC / 1e3
MPC = 1e3 * KPC
K_SI = 4 * math.pi * G
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}            # FITTED (kappa = 1/2)
LSTAR_PC = {"canonical": 21.682, "alt": 22.849}                 # FITTED (X3 D4 switched floor, via X14)
H0_SI = 67.2e3 / MPC                                            # native H0 lower end (conservative), as X14
M_MW = 6e10                                                     # ILLUSTRATIVE (X8/X10/X14)
W_KMS_X14 = [68.75, 74.8]                                       # X14 FT window speeds
R_FOLD_KPC = [11.0, 33.0, 73.0, 91.0, 156.0]                    # X14 fold radii
MUK = {"mu_0.1": 0.1 / MPC, "mu_0.03": 0.03 / MPC}             # S4 edges [1/m]
BOUNDS = {"alpha1": 1e-4, "alpha2": 2.4e-7, "alpha1_hat": 2.1e-5, "alpha2_hat": 1.6e-9}   # DOOR11 sec. 1
A22_PATH = os.path.join(ROOT, "deepseek_push", "DS_FINAL_2026_10_21", "A22_ppn_frames", "a22_checks.py")
A22_SHA = "f20cf27b89c44f96203d822f606f01f1dd484d91c0294b205ad6734699dfff95"
X14_JSON = os.path.join(ROOT, "rebuild_2026_10_22", "X14_caustic_completion", "x14_caustic_completion_results.json")
X14_JSON_SHA = "5af0afb83a8725eebdd056f4d8490301e5db437a2e658499e532dd6d1de3f96a"

log("X15_c1_preferred_frame" + ("  [MUTATE m1-m5]" if MUTATE else ""))
log("=" * 110)

# ===================================================================================================== PART S0
log("PART S0: reproductions (stop rule)")

# ---- S0-1: A22's own script, read-only, output redirected into this lane (m5: its own alpha1_forced mutation)
a22_json = os.path.join(HERE, f"a22_rerun{TAG}.json")
a22_out = os.path.join(HERE, f"a22_rerun{TAG}.out")
cmd = [sys.executable, A22_PATH, "--json-out", a22_json] + (["--mutate", "alpha1_forced"] if MUTATE else [])
env = dict(os.environ, PYTHONHASHSEED="0", OMP_NUM_THREADS="1")
sha_a22 = sha256(A22_PATH)
pr = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=HERE)
with open(a22_out, "w") as fh:
    fh.write(pr.stdout + pr.stderr)
with open(a22_json) as fh:
    a22 = json.load(fh)
n_a22 = sum(1 for c in a22["checks"] if c.get("pass"))
RES["S0_1"] = {"sha256": sha_a22, "sha_matches_frozen": sha_a22 == A22_SHA, "returncode": pr.returncode,
               "n_pass": n_a22, "n_checks": len(a22["checks"]), "status": a22["status"],
               "alpha1_ppn_order": a22["numbers"]["alpha1_ppn_order"],
               "alpha2_ppn_order": a22["numbers"]["alpha2_ppn_order"], "mutation": a22["mutation"]}
s01 = (sha_a22 == A22_SHA and pr.returncode == 0 and n_a22 == 13 and len(a22["checks"]) == 13
       and a22["numbers"]["alpha1_ppn_order"] == 0 and a22["numbers"]["alpha2_ppn_order"] == 0)
check("S0-1", s01, f"a22_checks.py sha ok {sha_a22 == A22_SHA}, exit {pr.returncode}, {n_a22}/{len(a22['checks'])} PASS, "
      f"alpha1/alpha2 PPN order {a22['numbers']['alpha1_ppn_order']}/{a22['numbers']['alpha2_ppn_order']}"
      + (" (A22 --mutate alpha1_forced: m5)" if MUTATE else ""),
      "A22's record script reproduces alpha_1 = alpha_2 = 0 at PPN order (13/13)")


# ---- S0-2: X14's window from X14's formulas (copied with provenance: x14_caustic_completion.py L431-435, L574, L586-597)
def aqual_point(r_m, a0v, GM):
    gN = GM / r_m ** 2
    g = 0.5 * (gN + math.sqrt(gN * gN + 4 * a0v * gN))
    Krho = 2 * a0v * GM / (r_m * math.sqrt(GM * GM + 4 * a0v * GM * r_m * r_m))   # 4 pi G rho_phantom
    return g, g / a0v, Krho


H0_use = 2 * H0_SI if MUTATE else H0_SI                     # m4: H0 doubled in the copied beta_max
GM_MW = M_MW * GM_SUN
beta_min = {}
X_FOLD = {}
for foot, a0v in FOOT.items():
    bm = []
    X_FOLD[foot] = []
    for r_k in R_FOLD_KPC:
        _, xv, _ = aqual_point(r_k * KPC, a0v, GM_MW)
        X_FOLD[foot].append(xv)
        for w_ in W_KMS_X14:
            ww = (w_ * 1e3) ** 2
            den = xv * C_SI ** 2 - 3 * ww
            bm.append(2 * ww / den if den > 0 else float("inf"))
    beta_min[foot] = max(bm)
beta_max = {lab: 2 * H0_use ** 2 / (C_SI ** 2 * mu_ ** 2 - 3 * H0_use ** 2) for lab, mu_ in MUK.items()}
sha_x14 = sha256(X14_JSON)
with open(X14_JSON) as fh:
    x14 = json.load(fh)
x14w = x14["classes"]["C1"]["FT_window"]
rel = []
for foot in FOOT:
    rel.append(abs(beta_min[foot] / x14w["beta_min_conservative(M-1=x)"][foot] - 1))
for lab in MUK:
    rel.append(abs(beta_max[lab] / x14w["beta_max"][lab] - 1))
RES["S0_2"] = {"beta_min": beta_min, "beta_max": beta_max, "x14_json_sha256": sha_x14,
               "x14_sha_matches_frozen": sha_x14 == X14_JSON_SHA, "max_rel_diff": max(rel),
               "x_fold": X_FOLD}
check("S0-2", sha_x14 == X14_JSON_SHA and max(rel) < 1e-12,
      f"beta_min can {beta_min['canonical']:.6e} alt {beta_min['alt']:.6e}; beta_max(0.1) {beta_max['mu_0.1']:.6e}, "
      f"(0.03) {beta_max['mu_0.03']:.6e}; max rel diff vs X14 JSON {max(rel):.1e}",
      "X14's C1 window reproduced from its own formulas to 1e-12 (both footings)")

# ---- the linear unitary-gauge system (FROZEN section 1), fields of (t, z); k along z, w = (w_x, 0, w_z)
t, z = sp.symbols("t z", real=True)
k, Kc, L, Mp, Ms, Mb = sp.symbols("k K L M_P M_s M", positive=True)
beta = sp.Symbol("beta", positive=True)
Th = sp.Symbol("Theta", nonnegative=True)
wx, wz, om = sp.symbols("w_x w_z omega", real=True)
nf, psf, N1f, N3f, P1f, P3f, Sf = [sp.Function(s)(t, z) for s in ("n", "psi", "N1", "N3", "P1", "P3", "S")]
FIELDS = [nf, psf, N1f, N3f, P1f, P3f]


def lagrangian(beta_c, theta, with_P=True, with_src=True, current=1):
    """quadratic unitary-gauge Lagrangian (FROZEN section 1). beta_c: coefficient of the C1 term (lambda - 1)."""
    dz = lambda f: sp.diff(f, z)
    dt = lambda f: sp.diff(f, t)
    S = {("x", "x"): 0, ("y", "y"): 0, ("z", "z"): dz(N3f), ("x", "z"): dz(N1f) / 2}
    Kxx = -dt(psf)
    Kyy = -dt(psf)
    Kzz = -dt(psf) - S[("z", "z")]
    Kxz = -S[("x", "z")]
    KK = Kxx ** 2 + Kyy ** 2 + Kzz ** 2 + 2 * Kxz ** 2
    Ktr = Kxx + Kyy + Kzz
    Lg = (2 * dz(psf) ** 2 - 4 * dz(nf) * dz(psf) + KK - (1 + beta_c) * Ktr ** 2) / (4 * Kc)
    LP = 0
    if with_P:
        gL = Kc * L ** 2 / 2
        LP = P3f * dz(nf) - Kc * Mp / 2 * (P1f ** 2 + P3f ** 2) - gL * theta / 2 * dz(P3f) ** 2
    Lsrc = 0
    if with_src:
        Lsrc = -Ms * (nf + (wx ** 2 + wz ** 2) * psf - current * (wx * N1f + wz * N3f)) * Sf
    return Lg + LP + Lsrc


def plane_wave_system(Lag, fields, omega_val, with_src=True):
    E = sp.exp(sp.I * (k * z - omega_val * t))
    amps = sp.symbols("A_n A_psi A_N1 A_N3 A_P1 A_P3")
    amap = dict(zip([nf, psf, N1f, N3f, P1f, P3f], amps))
    eqs = euler_equations(Lag, fields, [t, z])
    sub = {f: amap[f] * E for f in fields}
    if with_src:
        sub[Sf] = E
    out = []
    for e in eqs:
        ex = (e.lhs - e.rhs).subs(sub).doit()
        out.append(sp.simplify(sp.expand(ex / E)))
    return out, [amap[f] for f in fields]


# ---- S0-3: khronon dispersion of this lane's system vs X3/X14 (no source, scalar sector n, psi, N3, P3)
beta_act = -beta if MUTATE else beta                       # m1: C1 sign flipped in this lane's action
s03 = {}
s03_ok = True
for tv in (1, 0):
    Lag = lagrangian(beta_act, tv, with_P=True, with_src=False)
    eqs, amps = plane_wave_system(Lag, [nf, psf, N3f, P3f], om, with_src=False)
    Mat = sp.linear_eq_to_matrix(eqs, amps)[0]
    det = sp.factor(sp.simplify(Mat.det()))
    W2 = sp.Symbol("W2")
    roots = [sp.simplify(r_) for r_ in sp.solve(sp.Eq(sp.numer(sp.together(det)).subs(om, sp.sqrt(W2)), 0), W2)]
    expected = beta / (2 + 3 * beta) * k ** 2 * (Mp - 1 + tv * L ** 2 * k ** 2 / 2)   # X14: (Bk^2/K)(k^2/chi - K)
    resid = [sp.simplify(r_ - expected) for r_ in roots]
    hit = any(r_ == 0 for r_ in resid)
    s03[f"Theta{tv}"] = {"det": str(det), "omega2_roots": [str(r_) for r_ in roots], "expected": str(expected),
                         "residuals": [str(r_) for r_ in resid], "match": hit}
    s03_ok = s03_ok and hit and len(roots) == 1
RES["S0_3"] = s03
check("S0-3", s03_ok, f"omega^2 roots Theta1 {s03['Theta1']['omega2_roots']}, Theta0 {s03['Theta0']['omega2_roots']}; "
      f"expected beta k^2 (M - 1 + Theta L^2 k^2/2)/(2 + 3 beta)",
      "this lane's unitary-gauge system has exactly X3/X14's khronon root at rho_tau = 0, both sides (residual 0)")

# ---- the moving-source solve and the gauge-invariant extraction (FROZEN section 1)
eps, a_, b_ = sp.symbols("epsilon a b", positive=True)


def solve_moving(beta_c, theta, with_P=True, current=1):
    Lag = lagrangian(beta_c, theta, with_P=with_P, with_src=True, current=current)
    flds = FIELDS if with_P else [nf, psf, N1f, N3f]
    eqs, amps = plane_wave_system(Lag, flds, k * wz, with_src=True)
    sol = sp.linsolve(eqs, amps)
    sol = list(sol)
    if not sol:
        return None, amps, eqs
    s = dict(zip(amps, sol[0]))
    return s, amps, eqs


def extract(s, amps):
    """alpha_1(k), alpha_2(k), U_N(k), gamma from the gauge invariants N1 and Phi_inv = n - (Omega/k) N3."""
    An, Apsi, AN1, AN3 = amps[0], amps[1], amps[2], amps[3]
    free = set()
    for v in s.values():
        free |= v.free_symbols & set(amps)
    phi_inv = sp.simplify(s[An] - wz * s[AN3])
    N1 = sp.simplify(s[AN1])
    gauge_free_ok = not (phi_inv.free_symbols & set(amps)) and not (N1.free_symbols & set(amps))
    scal = {wx: eps * a_, wz: eps * b_, Ms: Mb / sp.sqrt(1 - eps ** 2 * (a_ ** 2 + b_ ** 2))}
    phs = sp.series(sp.simplify(phi_inv.subs(scal)), eps, 0, 3).removeO()
    n1s = sp.series(sp.simplify(N1.subs(scal)), eps, 0, 2).removeO()
    UN = sp.simplify(-phs.coeff(eps, 0))
    n1c = sp.simplify(n1s.coeff(eps, 1))
    c2 = sp.expand(sp.simplify(phs.coeff(eps, 2)))
    cxx = sp.simplify(c2.coeff(a_, 2).subs(b_, 0))
    czz = sp.simplify(c2.coeff(b_, 2).subs(a_, 0))
    cross = sp.simplify(c2 - cxx * a_ ** 2 - czz * b_ ** 2)
    al1 = sp.simplify(-2 * n1c / (a_ * UN) - 8)
    al2 = sp.simplify(3 + al1 / 2 - (czz - cxx) / UN)
    neg_pow = [p for p in (-1, -2) if sp.simplify(phs.coeff(eps, p)) != 0]
    return {"U_N": UN, "alpha1": al1, "alpha2": al2, "phi_inv": phi_inv, "N1": N1, "cross_term": cross,
            "gauge_free_ok": gauge_free_ok, "free_gauge_symbols": [str(f_) for f_ in free],
            "singular_eps_powers": neg_pow}


# ---- S0-4: GR control (P sector removed, beta = 0; m3: matter current dropped)
cur = 0 if MUTATE else 1
sGR, aGR, _ = solve_moving(0, 0, with_P=False, current=cur)
if sGR is None:      # e.g. m3: without the matter current the GR equations are inconsistent (no conserved momentum)
    RES["S0_4"] = {"solution_exists": False}
    check("S0-4", False, "GR system with this source has NO solution (inconsistent linear system)",
          "the extraction gives GR's alpha_1 = alpha_2 = 0 exactly, independent of the gauge function")
else:
    exGR = extract(sGR, aGR)
    RES["S0_4"] = {"solution_exists": True, "alpha1": str(exGR["alpha1"]), "alpha2": str(exGR["alpha2"]),
                   "U_N": str(exGR["U_N"]), "gauge_invariants_free_of_gauge_function": exGR["gauge_free_ok"],
                   "free_gauge_symbols": exGR["free_gauge_symbols"], "cross_term": str(exGR["cross_term"])}
    UN_GR_ok = sp.simplify(exGR["U_N"] - Kc * Mb / k ** 2) == 0
    check("S0-4", exGR["alpha1"] == 0 and exGR["alpha2"] == 0 and exGR["gauge_free_ok"] and UN_GR_ok,
          f"GR: alpha1 = {exGR['alpha1']}, alpha2 = {exGR['alpha2']}, U_N = {exGR['U_N']}, free gauge symbol(s) "
          f"{exGR['free_gauge_symbols']} absent from the invariants: {exGR['gauge_free_ok']}",
          "the extraction gives GR's alpha_1 = alpha_2 = 0 exactly, independent of the gauge function")

# ---- S0-5: A22 at beta = 0 in this lane's system: (a) static hedgehog, (b) PPN-order alpha's of the moving source
Lst = lagrangian(0, 1, with_P=True, with_src=True)
eqs_st, amps_st = plane_wave_system(Lst.subs({wx: 0, wz: 0}), FIELDS, 0, with_src=True)
sol_st = list(sp.linsolve(eqs_st, amps_st))
st = dict(zip(amps_st, sol_st[0]))
n_st = sp.simplify(st[amps_st[0]].subs({Mp: 1, Ms: Mb}))
psi_st = sp.simplify(st[amps_st[1]].subs({Mp: 1, Ms: Mb}))
target_st = -Kc * Mb / k ** 2 * (1 + 2 / (L ** 2 * k ** 2))      # A22 eq. 8 in Fourier space
r_st = [sp.simplify(n_st - target_st), sp.simplify(psi_st - target_st)]
s0, a0s, _ = solve_moving(0, 1, with_P=True)
ex0 = extract({kk: sp.simplify(vv.subs(Mp, 1)) for kk, vv in s0.items()}, a0s) if s0 is not None else None
lim0 = {}
if ex0 is not None:
    for nm in ("alpha1", "alpha2"):
        lim0[nm] = sp.simplify(sp.limit(ex0[nm], k, sp.oo))
RES["S0_5"] = {"static_n": str(n_st), "static_psi": str(psi_st), "A22_eq8_fourier": str(target_st),
               "static_residuals": [str(x_) for x_ in r_st],
               "moving_beta0_solution_exists": s0 is not None,
               "moving_beta0": ({"alpha1_k": str(ex0["alpha1"]), "alpha2_k": str(ex0["alpha2"]),
                                 "U_N_k": str(ex0["U_N"]), "singular_eps_powers": ex0["singular_eps_powers"],
                                 "alpha1_ppn_order": str(lim0.get("alpha1")),
                                 "alpha2_ppn_order": str(lim0.get("alpha2"))} if ex0 is not None else None)}
s05_ok = all(x_ == 0 for x_ in r_st) and ex0 is not None and lim0.get("alpha1") == 0 and lim0.get("alpha2") == 0
check("S0-5", s05_ok, f"static n, psi - A22 eq.8 = {r_st}; beta = 0 moving source: alpha1(k) = "
      f"{ex0['alpha1'] if ex0 else None}, alpha2(k) = {ex0['alpha2'] if ex0 else None}, U_N = "
      f"{ex0['U_N'] if ex0 else None}; PPN order {lim0}",
      "A22 reproduced at beta = 0: static hedgehog Phi = Psi = -GM/r + (GM/L*^2) r; PPN-order alpha_1 = alpha_2 = 0")

S0_OK = all(c["pass"] for c in CHECKS if c["id"].startswith("S0-"))
RES["S0_all_pass"] = S0_OK
if not S0_OK and not MUTATE:
    log("STOP RULE: a step-0 reproduction failed; verdict UNDECIDED, nothing further is scored.")
    RES["verdict"] = "UNDECIDED (step 0 failed)"
    finish(1)

# ===================================================================================================== PART D
log("")
log("PART D (step 1): alpha_1(k), alpha_2(k) of v3s + C1, screened branch (M = 1, Theta = 1)")
TH_SS = 0 if MUTATE else 1                                  # m2: stiffness removed in the Solar-System system
sC, aC, _ = solve_moving(beta_act, TH_SS, with_P=True)
exC = extract({kk: sp.simplify(vv.subs(Mp, 1)) for kk, vv in sC.items()}, aC)
al1 = exC["alpha1"]
al2 = exC["alpha2"]
eta = 2 / (Mp + TH_SS * L ** 2 * k ** 2 / 2)
eta1 = eta.subs(Mp, 1)
gam_k = sp.simplify(psi_st / n_st)
d3_a1 = sp.simplify(al1 - (-4 * eta1))
cand2 = eta1 * (eta1 * (1 + 2 * beta) - beta) / (beta * (2 - eta1))
d3_a2 = sp.simplify(al2 - cand2)
RES["D"] = {"alpha1_k": str(al1), "alpha2_k": str(al2), "U_N_k": str(exC["U_N"]), "gamma_k_static": str(gam_k),
            "eta_k": str(eta1), "alpha1_minus_(-4 eta)": str(d3_a1),
            "alpha2_minus_eta(eta(1+2beta)-beta)/(beta(2-eta))": str(d3_a2),
            "singular_eps_powers": exC["singular_eps_powers"], "cross_term": str(exC["cross_term"])}
check("D1", al1.is_finite is not False and not exC["singular_eps_powers"],
      f"alpha1(k) = {al1}  [alpha1 + 4 eta = {d3_a1}]", "alpha_1(k) derived in closed form (analytic in w)")
check("D2", al2.is_finite is not False and not exC["singular_eps_powers"],
      f"alpha2(k) = {al2}  [minus eta(eta(1+2b)-b)/(b(2-eta)): {d3_a2}]; gamma(k) static = {gam_k}",
      "alpha_2(k) derived in closed form (analytic in w)")

# ---- X-BPS: leading order in small (eta, beta) at fixed eta/beta vs BPS Eq. 91 (PROVISIONAL); exact vs record aether
et, s_ = sp.symbols("eta s", positive=True)
# express alpha's through eta: L^2 k^2 = 2(2 - eta)/eta at M = 1, Theta = 1 (screened); on m2 eta is fixed at 2
if TH_SS == 1:
    Lk2 = 2 * (2 - et) / et
    a1_eta = sp.simplify(al1.subs(L, sp.sqrt(Lk2) / k))
    a2_eta = sp.simplify(al2.subs(L, sp.sqrt(Lk2) / k))
else:
    a1_eta = sp.simplify(al1)
    a2_eta = sp.simplify(al2)
lead1 = sp.simplify(sp.limit(a1_eta.subs({et: s_ * et, beta: s_ * beta}) / s_, s_, 0))
lead2 = sp.simplify(sp.limit(a2_eta.subs({et: s_ * et, beta: s_ * beta}) / s_, s_, 0))
bps1 = -4 * et
bps2 = et * (et - beta) / (2 * beta)
aether2 = et * (et + 2 * beta * et - beta) / (beta * (2 - et))
xb1 = sp.simplify(lead1 - bps1)
xb2 = sp.simplify(lead2 - bps2)
xa2 = sp.simplify(a2_eta - aether2)
xa1 = sp.simplify(a1_eta - (-4 * et))
RES["X_BPS"] = {"alpha1_of_eta": str(a1_eta), "alpha2_of_eta": str(a2_eta), "leading_alpha1": str(lead1),
                "leading_alpha2": str(lead2), "BPS_eq91_alpha1": str(bps1), "BPS_eq91_alpha2": str(bps2),
                "residual_leading_alpha1": str(xb1), "residual_leading_alpha2": str(xb2),
                "record_aether_c13_0_alpha2": str(aether2), "exact_alpha2_minus_aether": str(xa2),
                "exact_alpha1_minus_minus4eta": str(xa1)}
check("X-BPS", xb1 == 0 and xb2 == 0,
      f"leading order: alpha1 - (-4 eta) = {xb1}, alpha2 - eta(eta - beta)/(2 beta) = {xb2}; exact alpha2 - record "
      f"aether(c13 = 0) = {xa2}", "BPS 2011 Eq. 91 (PROVISIONAL) reproduced in the matching limit alpha_BPS = eta, "
      "beta_BPS = 0, lambda' = beta")

# ---- P-A1, P-A2: PPN order
a1_inf = sp.simplify(sp.limit(al1, k, sp.oo))
a2_inf = sp.simplify(sp.limit(al2, k, sp.oo))
RES["PPN_order"] = {"alpha1_inf": str(a1_inf), "alpha2_inf": str(a2_inf)}
check("P-A1", a1_inf == 0, f"lim_(kL*->inf) alpha1 = {a1_inf}", "PPN-order alpha_1 = 0 on the screened branch, all beta > 0")
check("P-A2", a2_inf == 0, f"lim_(kL*->inf) alpha2 = {a2_inf}", "PPN-order alpha_2 = 0 on the screened branch, all beta > 0")

# ---- residual coefficients: alpha(k) = sum_m c_m (L k)^(-2m)
u_ = sp.Symbol("u", positive=True)                          # u = 1/(L k)^2
NM = 3


def res_coeffs(expr):
    e = sp.simplify(expr.subs(L, 1 / (k * sp.sqrt(u_))))
    ser = sp.series(e, u_, 0, NM + 1).removeO()
    return [sp.simplify(ser.coeff(u_, m)) for m in range(0, NM + 1)]


c_a1 = res_coeffs(al1)
c_a2 = res_coeffs(al2)
RES["residual_coeffs"] = {"alpha1": [str(c) for c in c_a1], "alpha2": [str(c) for c in c_a2]}
log(f"  residual coefficients (L k)^(-2m), m = 0..{NM}: alpha1 {c_a1}; alpha2 {c_a2}")


def f_n(n, r):   # inverse Fourier transform of 1/k^(2n)
    return (-1) ** (n + 1) * r ** (2 * n - 3) / (4 * math.pi * math.factorial(2 * n - 2))


def ratio_iso(m, r, Ls):     # w_i U structure: term (L k)^(-2m) relative to the U-type term
    return f_n(1 + m, r) / (f_n(1, r) * Ls ** (2 * m))


def ratio_lon(m, r, Ls):     # k_i k_j U/k^2 structure, n_i n_j coefficient, relative to m = 0
    def nn(n):
        p = 2 * n - 3
        A = (-1) ** (n + 1) / (4 * math.pi * math.factorial(2 * n - 2))
        return -A * p * (p - 2) * r ** (p - 2)
    return nn(2 + m) / (nn(2) * Ls ** (2 * m))


f_a1 = [sp.lambdify(beta, c, "math") for c in c_a1]
f_a2 = [sp.lambdify(beta, c, "math") for c in c_a2]


def _num(f, bval):
    """numeric coefficient; a non-numeric or nan coefficient (e.g. a direction-dependent degenerate extraction) -> inf."""
    try:
        v = float(f(bval))
    except (TypeError, ValueError, ZeroDivisionError, NameError):
        return float("inf")
    return float("inf") if math.isnan(v) else v


def alpha_eq(bval, r, Ls):
    a1 = sum(abs(_num(f_a1[m], bval) * ratio_iso(m, r, Ls)) for m in range(1, NM + 1))
    a2 = sum(abs(_num(f_a2[m], bval) * ratio_lon(m, r, Ls)) for m in range(1, NM + 1))
    a1_0 = _num(f_a1[0], bval)
    a2_0 = _num(f_a2[0], bval)
    return a1_0, a2_0, a1, a2


TESTS = [("Earth-Moon", 3.844e8, M_EARTH, ["alpha1"]), ("1 AU", AU, M_SUN, ["alpha1", "alpha2"]),
         ("30 AU", 30 * AU, M_SUN, ["alpha1", "alpha2"]), ("binary J1738", 1.73e9, 1.65 * M_SUN, ["alpha1_hat"]),
         ("NS radius", 1.2e4, 1.4 * M_SUN, ["alpha2_hat"])]
RHO_GAL = 1e-21                                             # ILLUSTRATIVE upper Galactic phantom near the Sun [kg/m^3]
RHO_SUN_1AU = None

# ---- P-LIN and P-RES on a 41-point log grid across each window, both footings, both mu_K
win = {}
plin_ok = True
pres_ok = True
worst = {}
for foot in FOOT:
    Ls = LSTAR_PC[foot] * PC
    win[foot] = {}
    for lab in MUK:
        bgrid = np.geomspace(beta_min[foot], beta_max[lab], 41) if beta_max[lab] > beta_min[foot] else np.array([])
        rows = []
        surv = []
        for bval in bgrid:
            Bc2 = bval / (2 + 3 * bval) * C_SI ** 2
            ok_all = True
            rowt = {}
            for name, r, Mbody, which in TESTS:
                Krho = 2 * G * Mbody / (Ls ** 2 * r) + K_SI * RHO_GAL
                if name == "Earth-Moon":
                    Krho += 2 * G * M_SUN / (Ls ** 2 * AU)
                dom = Bc2 / (Krho * r ** 2)
                cS = math.sqrt(Bc2 / 2) * Ls / r                  # c_S(k = 1/r) ~ sqrt(B/2) L* k (stiff side, M = 1)
                a1_0, a2_0, a1r, a2r = alpha_eq(bval, r, Ls)
                lin = dom >= 1e3 and cS >= 1e7
                okb = True
                for wb in which:
                    val = (abs(a1_0) + a1r) if wb.startswith("alpha1") else (abs(a2_0) + a2r)
                    okb = okb and val < BOUNDS[wb]
                    key = (foot, lab, name, wb)
                    if key not in worst or val > worst[key]:
                        worst[key] = val
                rowt[name] = {"C1_dominance": dom, "c_S_m_s": cS, "alpha1_eq": abs(a1_0) + a1r,
                              "alpha2_eq": abs(a2_0) + a2r, "linear_ok": lin, "bounds_ok": okb}
                ok_all = ok_all and lin and okb
                plin_ok = plin_ok and lin
                pres_ok = pres_ok and okb
            rows.append({"beta": float(bval), "tests": rowt, "all_ok": ok_all})
            if ok_all:
                surv.append(float(bval))
        win[foot][lab] = {"grid_n": len(bgrid), "surviving_n": len(surv),
                          "surviving_range": [min(surv), max(surv)] if surv else None,
                          "edges": {"beta_min": rows[0] if rows else None, "beta_max": rows[-1] if rows else None}}
RES["window_scan"] = win
RES["worst_alpha_eq"] = {" | ".join(k_): v_ for k_, v_ in worst.items()}
for foot in FOOT:
    for lab in MUK:
        e0 = win[foot][lab]["edges"]["beta_min"]["tests"]
        log(f"  {foot} {lab}: " + "; ".join(f"{nm} a1_eq {e0[nm]['alpha1_eq']:.2e} a2_eq {e0[nm]['alpha2_eq']:.2e} "
                                             f"dom {e0[nm]['C1_dominance']:.1e} cS {e0[nm]['c_S_m_s']:.1e}"
                                             for nm in e0) + " (at beta_min)")
worst_line = "; ".join(f"{k_[0]} {k_[1]} {k_[2]} {k_[3]} {v_:.2e} (bound {BOUNDS[k_[3]]:.1e})"
                       for k_, v_ in worst.items() if k_[1] == "mu_0.1")
check("P-LIN", plin_ok, "C1 dominance B/(K rho_tau r^2) >= 1e3 and c_S(1/r) >= 1e7 m/s at every test radius, every scored "
      "beta, both footings, both mu_K", "linearisation valid (C1 dominates the khronon's charge transport; subsonic)")
check("P-RES", pres_ok, f"worst alpha-equivalents over the mu_K = 0.1 windows: {worst_line}",
      "non-PPN residuals below every bound at its test radius across each window, both footings")

# ---- unscreened branch (reported): Theta = 0, M = M_theta
sU, aU, _ = solve_moving(beta_act, 0, with_P=True)
exU = extract(sU, aU)
fa1U = sp.lambdify((Mp, beta), exU["alpha1"], "math")
fa2U = sp.lambdify((Mp, beta), exU["alpha2"], "math")
unscr = {}
for foot in FOOT:
    unscr[foot] = []
    for r_k, xv in zip(R_FOLD_KPC, X_FOLD[foot]):
        for Mth in (1 + xv, (1 + xv) ** 2):
            for bl, bval in (("beta_min", beta_min[foot]), ("beta_max_0.1", beta_max["mu_0.1"])):
                a1v = fa1U(Mth, bval)
                a2v = fa2U(Mth, bval)
                unscr[foot].append({"r_kpc": r_k, "x": xv, "M_theta": Mth, "beta": bl, "alpha1": a1v, "alpha2": a2v,
                                    "alpha2_w2_at_70": a2v * (70e3 / C_SI) ** 2,
                                    "alpha2_w2_at_369": a2v * (369e3 / C_SI) ** 2})
RES["unscreened"] = {"alpha1_k": str(exU["alpha1"]), "alpha2_k": str(exU["alpha2"]), "values": unscr}
log(f"  unscreened (Theta 0, M = M_theta; reported): alpha1 = {exU['alpha1']}, alpha2 = {exU['alpha2']}")
for foot in FOOT:
    vals = unscr[foot]
    log(f"    {foot}: alpha1 in [{min(v['alpha1'] for v in vals):.2f}, {max(v['alpha1'] for v in vals):.2f}]; alpha2 in "
        f"[{min(v['alpha2'] for v in vals):.2e}, {max(v['alpha2'] for v in vals):.2e}]; alpha2 (w/c)^2 at 70 km/s up to "
        f"{max(v['alpha2_w2_at_70'] for v in vals):.2f}, at 369 km/s up to {max(v['alpha2_w2_at_369'] for v in vals):.2f}")

# ===================================================================================================== PART W
log("")
log("PART W (step 2): verdict")
req_D = all(c["pass"] for c in CHECKS if c["id"] in ("D1", "D2", "X-BPS", "P-A1", "P-A2", "P-LIN", "P-RES"))
nonempty = {foot: {lab: win[foot][lab]["surviving_n"] > 0 for lab in MUK} for foot in FOOT}
if not S0_OK:
    verdict = "UNDECIDED (step 0 failed)"
elif not all(c["pass"] for c in CHECKS if c["id"] in ("D1", "D2", "X-BPS", "P-A1", "P-A2", "P-LIN")):
    verdict = "UNDECIDED (a required derivation check failed)"
elif all(nonempty[f_]["mu_0.1"] for f_ in FOOT):
    verdict = "C1 SURVIVES PPN"
elif not any(nonempty[f_][l_] for f_ in FOOT for l_ in MUK):
    verdict = "WINDOW CLOSED BY PPN"
elif nonempty["canonical"]["mu_0.1"] != nonempty["alt"]["mu_0.1"]:
    verdict = "UNDECIDED (footings disagree)"
else:
    verdict = "UNDECIDED"
RES["verdict"] = verdict
RES["window_nonempty"] = nonempty
RES["surviving_windows"] = {foot: {lab: win[foot][lab]["surviving_range"] for lab in MUK} for foot in FOOT}
log(f"  VERDICT: {verdict}")
for foot in FOOT:
    log(f"  {foot}: surviving window " + "; ".join(f"{lab} {win[foot][lab]['surviving_range']} "
                                                  f"({win[foot][lab]['surviving_n']}/{win[foot][lab]['grid_n']})"
                                                  for lab in MUK))

# ===================================================================================================== PART T
log("")
log("PART T (step 3, reported only): Mach numbers, moving-galaxy rotation curve, Cherenkov")
# (3a) Mach numbers with X14's c_A at beta_max(0.1), scaled to beta_min and beta_max(0.03)
W_LIST = [70.0, 220.0, 369.0, 600.0, 1000.0]
cA_x14 = x14w["c_A_at_beta_max_mu0.1_km_s"]


def cA_scale(b_to, b_from):
    return math.sqrt(b_to * (2 + 3 * b_from) / (b_from * (2 + 3 * b_to)))


mach = {}
for foot in FOOT:
    mach[foot] = {}
    for bl, bval in (("beta_min", beta_min[foot]), ("beta_max_0.1", x14w["beta_max"]["mu_0.1"]),
                     ("beta_max_0.03", x14w["beta_max"]["mu_0.03"])):
        cs = [c_ * cA_scale(bval, x14w["beta_max"]["mu_0.1"]) for c_ in cA_x14[foot]]
        mach[foot][bl] = {"c_A_km_s": cs, "Mach": {f"{w_:.0f}": [w_ / c_ for c_ in cs] for w_ in W_LIST}}
RES["T3a_mach"] = mach
for foot in FOOT:
    for bl in mach[foot]:
        cs = mach[foot][bl]["c_A_km_s"]
        log(f"  {foot} {bl}: c_A {min(cs):.0f}-{max(cs):.0f} km/s at the fold radii; Mach " +
            ", ".join(f"w {w_:.0f}: {w_ / max(cs):.2f}-{w_ / min(cs):.2f}" for w_ in W_LIST))

# (3b) S3-1: the steady O(w) khronon equation from the 3D PN Lagrangian + C1, and the l = 1 indicial polynomial
X, Y, Z = sp.symbols("x y z", real=True)
T = sp.Symbol("t", real=True)
Bs, A_ = sp.symbols("B A", positive=True)
mu2 = sp.Symbol("mu2", nonnegative=True)
phi3 = sp.Function("phi")(T, X, Y, Z)
sig3 = sp.Function("sigma")(T, X, Y, Z)
Pv = [sp.Function(f"P{i}")(T, X, Y, Z) for i in range(3)]
Wf = sp.Function("W")
grad = lambda f: [sp.diff(f, v) for v in (X, Y, Z)]
divv = lambda V: sum(sp.diff(V[i], v) for i, v in enumerate((X, Y, Z)))
lap = lambda f: sum(sp.diff(f, v, 2) for v in (X, Y, Z))
Xi3 = phi3 - sp.diff(sig3, T) + sum(g_ ** 2 for g_ in grad(sig3)) / 2
rho_m3 = sp.Function("rho_m")(X, Y, Z)
L3 = (-sum(g_ ** 2 for g_ in grad(phi3)) / (2 * Kc) - rho_m3 * phi3 + sum(Pv[i] * grad(Xi3)[i] for i in range(3))
      - Wf(sum(p_ ** 2 for p_ in Pv)) - Kc * L ** 2 / 4 * divv(Pv) ** 2 + mu2 * Xi3 ** 2 / (2 * Kc)
      - Bs / (2 * Kc) * lap(sig3) ** 2)
el_sig = euler_equations(L3, [sig3], [T, X, Y, Z])[0].lhs
rho_t3 = divv(Pv) - mu2 * Xi3 / Kc
v3 = [-g_ for g_ in grad(sig3)]
cont = sp.diff(rho_t3, T) + divv([rho_t3 * v3[i] for i in range(3)]) + Bs / Kc * lap(lap(sig3))
r_s31a = min((sp.expand(el_sig - sg * cont) for sg in (1, -1)), key=lambda e: len(str(e)))
r_s31a = sp.simplify(r_s31a) if r_s31a != 0 else r_s31a
# steady O(w) form with rho_tau = rho0(x) given, sigma = w z + dsigma (galaxy frame, wind along -z), first order in w
wv = sp.Symbol("w", positive=True)
rho0 = A_ / (X ** 2 + Y ** 2 + Z ** 2)
rr = sp.sqrt(X ** 2 + Y ** 2 + Z ** 2)
p_ = sp.Symbol("p")
g_test = Z * rr ** (p_ - 1)                                 # f(r) cos(theta) with f = r^p
steady = lambda ds, wval: (-wval * sp.diff(rho0, Z) - divv([rho0 * gg for gg in grad(ds)]) + Bs / Kc * lap(lap(ds)))
E_st = steady(g_test, 0)
ind_pts = []
for (x0, y0, z0) in ((0, 0, 1), (1, 2, 2)):
    r0_ = sp.sqrt(x0 ** 2 + y0 ** 2 + z0 ** 2)
    ind_pts.append(sp.expand(sp.simplify(E_st.subs({X: x0, Y: y0, Z: z0}) / (z0 * r0_ ** (p_ - 5)))))
indicial = sp.factor(ind_pts[0])
ind_same = sp.simplify(ind_pts[0] - ind_pts[1]) == 0
target_ind = sp.expand(Bs / Kc * p_ * (p_ - 1) * (p_ + 2) * (p_ - 3) - A_ * (p_ - 2) * (p_ + 1))
r_s31b = sp.simplify(sp.expand(indicial) - target_ind)
r_s31c = sp.simplify(steady(-wv * Z, wv))                    # fully held particular solution
RES["S3_1"] = {"sigma_EL_vs_continuity_residual": str(r_s31a), "indicial": str(indicial), "indicial_same_at_two_points": ind_same,
               "indicial_minus_target": str(r_s31b), "held_particular_residual": str(r_s31c)}
check("S3-1", r_s31a == 0 and r_s31b == 0 and r_s31c == 0 and ind_same,
      f"sigma-EL -/+ [d_t rho + div(rho v) + (B/K) lap^2 sigma] = {r_s31a}; l = 1 indicial {indicial}; minus "
      f"[(B/K)p(p-1)(p+2)(p-3) - A(p-2)(p+1)] = {r_s31b}; dsigma = -w z residual {r_s31c}",
      "3b steady equation and indicial polynomial derived from the 3D PN Lagrangian + C1 (residual 0)")

# numbers: MW-mass AQUAL phantom, streaming exponent, rotation-curve change estimate
R_LIST_KPC = [10.0, 30.0, 100.0]
RH_MPC = [1.0, 10.0]


def p1_of(Rv):
    if Rv == 0:
        return 2.0
    co = np.polynomial.polynomial.polyfromroots([0, 1, -2, 3]) * Rv
    co = co - np.array([-2.0, -1.0, 1.0, 0.0, 0.0])           # (p-2)(p+1) = p^2 - p - 2 -> [-2, -1, 1]
    rts = np.roots(co[::-1])
    real = sorted(r_.real for r_ in rts if abs(r_.imag) < 1e-9 and r_.real > 1 + 1e-12)
    return real[0]


rot = {}
for foot, a0v in FOOT.items():
    rot[foot] = []
    for bl, bval in (("beta_0", 0.0), ("beta_min", beta_min[foot]), ("beta_max_0.1", beta_max["mu_0.1"]),
                     ("beta_max_0.03", beta_max["mu_0.03"])):
        Bc2 = bval / (2 + 3 * bval) * C_SI ** 2
        for r_k in R_LIST_KPC:
            rm = r_k * KPC
            g, xv, Krho = aqual_point(rm, a0v, GM_MW)
            gN = GM_MW / rm ** 2
            lawp = 0.5 + (gN + 2 * a0v) / (2 * math.sqrt(gN * gN + 4 * a0v * gN))
            Rv = Bc2 / (Krho * rm ** 2)
            p1 = p1_of(Rv)
            vc2 = g * rm
            cA_loc = math.sqrt(Bc2 * xv) / 1e3
            for RH in RH_MPC:
                for w_ in W_LIST:
                    sup = w_ > cA_loc
                    dlng = (lawp - 1) * (p1 - 1) * (p1 ** 2 + 2) / 3 * (w_ * 1e3) ** 2 / vc2 * (rm / (RH * MPC)) ** (2 * (p1 - 1))
                    rot[foot].append({"beta": bl, "r_kpc": r_k, "R_h_Mpc": RH, "w_km_s": w_, "R": Rv, "p1": p1,
                                      "dg/dgN": lawp, "v_c_km_s": math.sqrt(vc2) / 1e3, "c_A_local_km_s": cA_loc,
                                      "supersonic": sup, "dlog10g": dlng / math.log(10)})
RES["T3b_rotation"] = rot
for foot in FOOT:
    for bl in ("beta_0", "beta_min", "beta_max_0.1", "beta_max_0.03"):
        sub = [r_ for r_ in rot[foot] if r_["beta"] == bl]
        p1s = sorted({round(r_["p1"], 4) for r_ in sub})
        sub_ok = [r_ for r_ in sub if not r_["supersonic"]]
        over = sorted({r_["w_km_s"] for r_ in sub_ok if r_["dlog10g"] > 0.05})
        sup = sorted({r_["w_km_s"] for r_ in sub if r_["supersonic"]})
        mx = max((r_["dlog10g"] for r_ in sub_ok), default=float("nan"))
        log(f"  {foot} {bl}: p1 {p1s}; max subsonic dlog10 g {mx:.3f} dex; w with > 0.05 dex somewhere (subsonic) "
            f"{over}; w supersonic somewhere {sup}")

# (3c) Cherenkov / supersonic drag bound
rho_crit = 3 * H0_SI ** 2 / (8 * math.pi * G)
GM_CL = 1e14 * GM_SUN
cher = {}
for foot, a0v in FOOT.items():
    _, x_cl, Krho_cl = aqual_point(300 * KPC, a0v, GM_CL)
    rho_cl = Krho_cl / K_SI
    lnL = math.log(100.0)
    cher[foot] = {"rho_crit": rho_crit, "rho_cluster_phantom_300kpc": rho_cl, "x_cluster_300kpc": x_cl, "rows": []}
    for bl, bval in (("beta_min", beta_min[foot]), ("beta_max_0.1", beta_max["mu_0.1"])):
        cA_cl = math.sqrt(bval / (2 + 3 * bval) * C_SI ** 2 * x_cl) / 1e3
        for w_ in (600.0, 1000.0):
            for lab, rho in (("cosmic dust <= rho_crit", rho_crit), ("cluster phantom 300 kpc", rho_cl)):
                a_drag = 4 * math.pi * G * GM_MW * rho * lnL / (w_ * 1e3) ** 2   # F/M = 4 pi G^2 M rho lnL / w^2
                t_drag = (w_ * 1e3) / a_drag
                cher[foot]["rows"].append({"beta": bl, "w_km_s": w_, "medium": lab, "c_A_cluster_km_s": cA_cl,
                                           "supersonic_in_cluster": w_ > cA_cl, "t_drag_over_tH": t_drag * H0_SI})
RES["T3c_cherenkov"] = cher
for foot in FOOT:
    log(f"  {foot}: rho_crit {rho_crit:.2e}, cluster phantom (300 kpc) {cher[foot]['rho_cluster_phantom_300kpc']:.2e} kg/m^3; "
        + "; ".join(f"{r_['beta']} w {r_['w_km_s']:.0f} {r_['medium']}: t_drag/t_H {r_['t_drag_over_tH']:.2e}"
                    f" (cluster c_A {r_['c_A_cluster_km_s']:.0f} km/s)" for r_ in cher[foot]["rows"]))

# ===================================================================================================== verdict lines
log("")
log("VERDICT")
log(f"  {verdict}")
if MUTATE:
    must_fail = {"S0-1": "m5", "S0-2": "m4", "S0-3": "m1", "S0-4": "m3", "P-A1": "m2"}
    failed = {c["id"] for c in CHECKS if not c["pass"]}
    RES["mutate_required_failures"] = {cid: (cid in failed) for cid in must_fail}
    log(f"  MUTATE: required failures {RES['mutate_required_failures']}; all failed checks {sorted(failed)}")
finish()
