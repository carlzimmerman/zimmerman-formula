#!/usr/bin/env python3
"""X16_beta_binary_radiation: with C1 (the khronon K^2 term, Horava lambda = 1 + beta) inside X14's window, how much does
the khronon scalar's radiation change binary-pulsar orbital decay, and does it stay inside the observed Pbdot agreement
with GR?  Frozen criteria: FROZEN_CRITERIA.md (committed alone with ASSUMPTION_LEDGER.md and LITERATURE_MAP.md).

Part S0  reproductions (stop rule): X15, X14, C8 own scripts (byte-identical copies run inside this lane), this lane's
         dispersion, Peters-Mathews                                                            -> S0-1 .. S0-5
Part D   step 1 (sympy): power formula, residue, closed forms, literature control              -> D-HERM, D-GR, D-RES,
         D-ON, D-FORM, ANG, X-LIT, D-LIM
Part H   harmonics of the Kepler orbits                                                         -> H-PM
Part W   step 2: the window scored against the record's binary-pulsar bounds                   -> D-K4, P-LIN, P-WAVE, verdict
Part R   reported only (GW170817, causality, V_CM, scalings, frames, absolute Pbdot, crossover)

Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x16_beta_binary_radiation.py               (exit 0 iff all pass)
      PYTHONHASHSEED=0 X16_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 x16_beta_binary_radiation.py  (m1..m7; exit 1)

kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. No dark-matter particle.
Not theory closed. Units c = 1 and K = 4 pi G in the symbolic part; SI in the numerical part.
"""
import ast
import glob
import hashlib
import json
import math
import os
import resource
import shutil
import subprocess
import sys
import time

import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations

MUTATE = os.environ.get("X16_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"x16_beta_binary_radiation{TAG}.out")
JS = os.path.join(HERE, f"x16_beta_binary_radiation_results{TAG}.json")
RERUN = os.path.join(HERE, f"step0_reruns{TAG}")
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
        return {str(k_): clean(v_) for k_, v_ in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v_) for v_ in o]
    if isinstance(o, np.ndarray):
        return [clean(v_) for v_ in o.tolist()]
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, (np.floating, float)):
        return float(o)
    if isinstance(o, (np.integer, int)):
        return int(o)
    if isinstance(o, complex):
        return [o.real, o.imag]
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
        f"{RES['runtime_s']:.0f} s; peak RSS (this process) {RES['peak_rss_gb']:.3f} GB")
    with open(OUT, "w") as fh:
        fh.write("\n".join(_lines) + "\n")
    with open(JS, "w") as fh:
        json.dump(clean(RES), fh, indent=1)
    sys.exit((0 if not req_fail else 1) if exit_code is None else exit_code)


def relmax(a_, b_):
    return abs(a_ / b_ - 1) if b_ != 0 else abs(a_ - b_)


# ------------------------------------------------------------------------------------------- constants (RAW / FITTED)
G = 6.67430e-11
C_SI = 299792458.0
GM_SUN = 1.32712440018e20
M_SUN = GM_SUN / G
T_SUN = GM_SUN / C_SI ** 3
DAY = 86400.0
KPC = 3.0856775814913673e19
PC = KPC / 1e3
MPC = 1e3 * KPC
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}            # FITTED (kappa = 1/2); enter only through L* and beta_min
LSTAR_PC = {"canonical": 21.682, "alt": 22.849}                 # FITTED (X3 D4 switched floor, via X14/X15)
H0_SI = 67.2e3 / MPC                                            # native H0 lower end, as X14 (only in beta_max)
MUK = {"mu_0.1": 0.1 / MPC, "mu_0.03": 0.03 / MPC}
M_BG = [1.0, 100.0]                                             # screened bare / ILLUSTRATIVE Galactic (1 + x)^2 upper
R_NS = 1.2e4                                                    # ILLUSTRATIVE (record: C8, P3)
OMEGA_OVER_M = 0.3                                              # CFG291 |Omega/m|_max
RHO_GAL = 1e-21                                                 # ILLUSTRATIVE Galactic phantom upper value (as X15)
V_CMB = 369e3                                                   # ILLUSTRATIVE (CMB dipole)
NSAMP, NMAX = 8192, 400

# record files and their committed sha256 (FROZEN section 3)
P_X15 = os.path.join(ROOT, "rebuild_2026_10_22", "X15_c1_preferred_frame", "x15_c1_preferred_frame.py")
P_X15J = os.path.join(ROOT, "rebuild_2026_10_22", "X15_c1_preferred_frame", "x15_c1_preferred_frame_results.json")
P_X14 = os.path.join(ROOT, "rebuild_2026_10_22", "X14_caustic_completion", "x14_caustic_completion.py")
P_X14J = os.path.join(ROOT, "rebuild_2026_10_22", "X14_caustic_completion", "x14_caustic_completion_results.json")
P_C8 = os.path.join(ROOT, "covariant_push_2026_10_22", "C8_instantaneous", "c8_instantaneous.py")
P_C8J = os.path.join(ROOT, "covariant_push_2026_10_22", "C8_instantaneous", "c8_instantaneous_results.json")
P_LED = os.path.join(ROOT, "real_research", "reviews", "mi_pulsar_pta_precision_ledger_2026.py")
P_P3J = os.path.join(ROOT, "rebuild_2026_10_22", "P3_v3_strong_field", "p3_v3_strong_field_results.json")
SHA = {"X15": "2bf2810326a938da36f95419c95aeed6660f10bf01c2cd4e955ef80cc864f9e1",
       "X15J": "dd864fc9bdf408b7c12cfb2a60ea7d45ec3c9eb363d581e00b58d658e67d8e5e",
       "X14": "32fd2a1264183db65a2d72d3fd56a968f91c546cc0bd18a10b234d3ddedc5012",
       "X14J": "5af0afb83a8725eebdd056f4d8490301e5db437a2e658499e532dd6d1de3f96a",
       "C8": "d8f78c2679a8dabc7c1e8ae72c81f28852658c5af66ea21703e209f0f18d1ae2",
       "C8J": "1d7bc58b7785911693d626c68ef9850d9d0af6a40e0a2b8ea6c288753d6ab7d7",
       "LED": "f1688d81aecae40886c08e7188311bdc2509b337ab8b47b4fee3dff4628edbff",
       "P3J": "30eaf641e6acd3626c9bd62194ae8f34fc14f1adc0f5c6eabe793746f4e8db14"}

# binaries (FROZEN section 2; record transcriptions)
BIN = {
    "J0737-3039A/B": dict(m1=1.338185, m2=1.248868, Pb=0.1022515592973, e=0.087777023, kind="NS-NS",
                          PbdotGR=-1.247920e-12, tol=1e-3, GR_int=None, dplus=(0.999963 - 1) + 2 * 6.3e-5, sig=6.3e-5,
                          rec=("J0737-3039A/B", "J0737-3039A/B")),
    "B1913+16": dict(m1=1.4398, m2=1.3886, Pb=0.322997448918, e=0.6171340, kind="NS-NS",
                     PbdotGR=-2.402531e-12, tol=1e-3, GR_int=None, dplus=(0.9983 - 1) + 2 * 0.0016, sig=0.0016,
                     rec=("B1913+16", "B1913+16")),
    "J1738+0333": dict(m1=1.46, m2=0.181, Pb=0.3547907398724, e=3.4e-7, kind="NS-WD",
                       PbdotGR=-27.7e-15, tol=1e-2, GR_int=(-27.7e-15, 1.5e-15, 1.9e-15),
                       dplus=(25.9 + 2 * 3.2) / 27.7 - 1, sig=3.2 / 27.7, rec=("J1738+0333", "J1738+0333")),
    "J0348+0432": dict(m1=2.01, m2=0.172, Pb=0.102424062722, e=2.0e-6, kind="NS-WD",
                       PbdotGR=-0.258e-12, tol=1e-2, GR_int=(-0.258e-12, 0.008e-12, 0.011e-12),
                       dplus=1.05 + 2 * 0.18 - 1, sig=0.18, rec=None),
}
if MUTATE:
    BIN["J0737-3039A/B"]["Pb"] *= 1.01                          # m4: J0737's P_b perturbed in this lane's inputs

log("X16_beta_binary_radiation" + ("  [MUTATE m1-m7]" if MUTATE else ""))
log("=" * 110)
os.makedirs(RERUN, exist_ok=True)
env_sub = dict(os.environ, PYTHONHASHSEED="0", OMP_NUM_THREADS="1")
env_sub.pop("X16_MUTATE", None)

# ===================================================================================================== PART S0
log("PART S0: reproductions (stop rule)")

# ---- S0-1: X15's own script, byte-identical copy run in this lane's directory (its ROOT resolves to the repo root)
sha_x15 = sha256(P_X15)
cp15 = os.path.join(HERE, "x15_c1_preferred_frame.py")
shutil.copyfile(P_X15, cp15)
sha_cp15 = sha256(cp15)
env15 = dict(env_sub)
if MUTATE:
    env15["X15_MUTATE"] = "1"                                   # m1: X15's own MUTATE
else:
    env15.pop("X15_MUTATE", None)
t1 = time.time()
pr15 = subprocess.run([sys.executable, cp15], capture_output=True, text=True, env=env15, cwd=HERE, timeout=1800)
dt15 = time.time() - t1
os.remove(cp15)
d15 = os.path.join(RERUN, "x15")
os.makedirs(d15, exist_ok=True)
moved15 = []
for pat in ("x15_c1_preferred_frame*.out", "x15_c1_preferred_frame_results*.json", "a22_rerun*.out", "a22_rerun*.json"):
    for f_ in glob.glob(os.path.join(HERE, pat)):
        shutil.move(f_, os.path.join(d15, os.path.basename(f_)))
        moved15.append(os.path.basename(f_))
tag15 = "_MUTATE" if MUTATE else ""
with open(P_X15J) as fh:
    x15c = json.load(fh)
with open(os.path.join(d15, f"x15_c1_preferred_frame_results{tag15}.json")) as fh:
    x15r = json.load(fh)
n15 = sum(1 for c in x15r["checks"] if c["pass"])
same_str = all(x15r["S0_3"][th]["omega2_roots"] == x15c["S0_3"][th]["omega2_roots"] for th in ("Theta1", "Theta0")) and \
    x15r["D"]["alpha1_k"] == x15c["D"]["alpha1_k"] and x15r["D"]["alpha2_k"] == x15c["D"]["alpha2_k"]
win_dev = max(relmax(x15r["surviving_windows"][f_][l_][i_], x15c["surviving_windows"][f_][l_][i_])
              for f_ in ("canonical", "alt") for l_ in ("mu_0.1", "mu_0.03") for i_ in (0, 1)) \
    if all(x15r["surviving_windows"][f_][l_] for f_ in ("canonical", "alt") for l_ in ("mu_0.1", "mu_0.03")) else float("inf")
s01 = (sha_x15 == SHA["X15"] and sha_cp15 == SHA["X15"] and sha256(P_X15J) == SHA["X15J"] and pr15.returncode == 0
       and n15 == 13 and len(x15r["checks"]) == 13 and x15r["verdict"] == "C1 SURVIVES PPN" and same_str and win_dev < 1e-12)
RES["S0_1"] = {"sha_ok": sha_x15 == SHA["X15"], "copy_sha_ok": sha_cp15 == SHA["X15"], "returncode": pr15.returncode,
               "n_pass": n15, "n_checks": len(x15r["checks"]), "verdict": x15r["verdict"],
               "root_and_alpha_strings_identical": same_str, "window_max_rel_dev": win_dev, "runtime_s": dt15,
               "outputs": moved15, "omega2_root_Theta1": x15r["S0_3"]["Theta1"]["omega2_roots"]}
check("S0-1", s01, f"X15 copy sha ok {sha_cp15 == SHA['X15']}, exit {pr15.returncode}, {n15}/{len(x15r['checks'])} PASS, "
      f"verdict '{x15r['verdict']}', root/alpha strings identical {same_str}, window dev {win_dev:.1e}, {dt15:.0f} s"
      + (" (X15_MUTATE=1: m1)" if MUTATE else ""),
      "X15's own code reproduces its khronon root, alpha_1(k), alpha_2(k) and surviving window")


# ---- S0-2: X14's own script (copy run in step0_reruns/x14) + this lane's recomputation from X14's formulas
def aqual_point(r_m, a0v, GM):                                 # X14 L431-435 via X15 (copied with provenance)
    gN = GM / r_m ** 2
    g = 0.5 * (gN + math.sqrt(gN * gN + 4 * a0v * gN))
    Krho = 2 * a0v * GM / (r_m * math.sqrt(GM * GM + 4 * a0v * GM * r_m * r_m))
    return g, g / a0v, Krho


d14 = os.path.join(RERUN, "x14")
os.makedirs(d14, exist_ok=True)
cp14 = os.path.join(d14, "x14_caustic_completion.py")
shutil.copyfile(P_X14, cp14)
sha_cp14 = sha256(cp14)
t1 = time.time()
pr14 = subprocess.run([sys.executable, cp14], capture_output=True, text=True, env=env_sub, cwd=d14, timeout=1800)
dt14 = time.time() - t1
os.remove(cp14)
with open(P_X14J) as fh:
    x14c = json.load(fh)
with open(os.path.join(d14, "x14_caustic_completion_results.json")) as fh:
    x14r = json.load(fh)
wr, wc = x14r["classes"]["C1"]["FT_window"], x14c["classes"]["C1"]["FT_window"]
KMIN, KMAX = "beta_min_conservative(M-1=x)", "beta_max"
dev14 = max([relmax(wr[KMIN][f_], wc[KMIN][f_]) for f_ in FOOT] + [relmax(wr[KMAX][l_], wc[KMAX][l_]) for l_ in MUK])
# own recomputation (X15 S0-2 copy of X14's formulas; m2 doubles H0 here)
H0_use = 2 * H0_SI if MUTATE else H0_SI
GM_MW = 6e10 * GM_SUN
bmin_own = {}
for foot, a0v in FOOT.items():
    bm = []
    for r_k in [11.0, 33.0, 73.0, 91.0, 156.0]:
        _, xv, _ = aqual_point(r_k * KPC, a0v, GM_MW)
        for w_ in [68.75, 74.8]:
            ww = (w_ * 1e3) ** 2
            den = xv * C_SI ** 2 - 3 * ww
            bm.append(2 * ww / den if den > 0 else float("inf"))
    bmin_own[foot] = max(bm)
bmax_own = {lab: 2 * H0_use ** 2 / (C_SI ** 2 * mu_ ** 2 - 3 * H0_use ** 2) for lab, mu_ in MUK.items()}
dev_own = max([relmax(bmin_own[f_], wr[KMIN][f_]) for f_ in FOOT] + [relmax(bmax_own[l_], wr[KMAX][l_]) for l_ in MUK])
n14 = sum(1 for c in x14r["checks"] if c["pass"])
s02 = (sha_cp14 == SHA["X14"] and sha256(P_X14J) == SHA["X14J"] and pr14.returncode == 0 and n14 == 24
       and len(x14r["checks"]) == 24 and dev14 < 1e-12 and dev_own < 1e-12)
BETA_MIN = {f_: wr[KMIN][f_] for f_ in FOOT}
BETA_MAX = {l_: wr[KMAX][l_] for l_ in MUK}
RES["S0_2"] = {"copy_sha_ok": sha_cp14 == SHA["X14"], "returncode": pr14.returncode, "n_pass": n14,
               "n_checks": len(x14r["checks"]), "rerun_vs_committed_max_rel": dev14, "own_vs_rerun_max_rel": dev_own,
               "beta_min": BETA_MIN, "beta_max": BETA_MAX, "own_beta_min": bmin_own, "own_beta_max": bmax_own,
               "runtime_s": dt14}
check("S0-2", s02, f"X14 copy exit {pr14.returncode}, {n14}/{len(x14r['checks'])} PASS; beta_min can {BETA_MIN['canonical']:.6e}"
      f" alt {BETA_MIN['alt']:.6e}, beta_max(0.1) {BETA_MAX['mu_0.1']:.6e} (0.03) {BETA_MAX['mu_0.03']:.6e}; rerun vs committed "
      f"{dev14:.1e}, own formulas vs rerun {dev_own:.1e}; {dt14:.0f} s" + (" (H0 doubled: m2)" if MUTATE else ""),
      "X14's own code reproduces its C1 window to 1e-12; this lane's copy of X14's formulas agrees")

# ---- the linear unitary-gauge system (X15 FROZEN section 1, `lagrangian` copied with provenance; source generalised)
t, z = sp.symbols("t z", real=True)
k, Kc, L, Mp = sp.symbols("k K L M_P", positive=True)
beta = sp.Symbol("beta", positive=True)
al = sp.Symbol("alpha", positive=True)
Th = sp.Symbol("Theta", nonnegative=True)
om = sp.Symbol("omega", positive=True)
rho_s, T_s, Jx_s, Jz_s = sp.symbols("rho T J_x J_z", real=True)
Txx, Tyy, Txy = sp.symbols("T_xx T_yy T_xy", real=True)
nf, psf, N1f, N3f, P1f, P3f, Sf = [sp.Function(s)(t, z) for s in ("n", "psi", "N1", "N3", "P1", "P3", "S")]
hpf, hxf = [sp.Function(s)(t, z) for s in ("h_p", "h_x")]
FIELDS6 = [nf, psf, N1f, N3f, P1f, P3f]
FIELDS4A = [nf, psf, N1f, N3f]


def lagrangian(beta_c, theta, mode="P"):
    """X15's quadratic unitary-gauge Lagrangian with a general source -rho n - T psi + J.N.
    mode 'P': v3s (+ C1); mode 'alpha': constant-alpha khronometric control (P sector -> alpha (n_z)^2/(4K)); 'GR': neither."""
    dz = lambda f: sp.diff(f, z)
    dt = lambda f: sp.diff(f, t)
    Kxx = -dt(psf)
    Kyy = -dt(psf)
    Kzz = -dt(psf) - dz(N3f)
    Kxz = -dz(N1f) / 2
    KK = Kxx ** 2 + Kyy ** 2 + Kzz ** 2 + 2 * Kxz ** 2
    Ktr = Kxx + Kyy + Kzz
    Lg = (2 * dz(psf) ** 2 - 4 * dz(nf) * dz(psf) + KK - (1 + beta_c) * Ktr ** 2) / (4 * Kc)
    LP = 0
    if mode == "P":
        gL = Kc * L ** 2 / 2
        LP = P3f * dz(nf) - Kc * Mp / 2 * (P1f ** 2 + P3f ** 2) - gL * theta / 2 * dz(P3f) ** 2
    elif mode == "alpha":
        LP = al * dz(nf) ** 2 / (4 * Kc)
    Lsrc = (-rho_s * nf - T_s * psf + Jx_s * N1f + Jz_s * N3f) * Sf
    return Lg + LP + Lsrc


def lagrangian_TT(beta_c, src_factor=sp.Rational(1, 2)):
    """TT tensor sector: (1/4K)[K_ij K_ij - (1+beta)K^2 + R3^(2)] + (1/2) h_ij T^ij, R3^(2) = -(1/4)(d_z h_ij)^2."""
    h = sp.Matrix([[hpf, hxf, 0], [hxf, -hpf, 0], [0, 0, 0]])
    Kij = h.applyfunc(lambda f: sp.diff(f, t) / 2)
    KK = sum(Kij[i, j] ** 2 for i in range(3) for j in range(3))
    Ktr = sum(Kij[i, i] for i in range(3))
    R3 = -sum(sp.diff(h[i, j], z) ** 2 for i in range(3) for j in range(3)) / 4
    Tm = sp.Matrix([[Txx, Txy, 0], [Txy, Tyy, 0], [0, 0, 0]])
    Lsrc = src_factor * sum(h[i, j] * Tm[i, j] for i in range(3) for j in range(3)) * Sf
    return (KK - (1 + beta_c) * Ktr ** 2 + R3) / (4 * Kc) + Lsrc


def plane_wave_matrix(Lag, fields):
    """EL equations on A e^{i(kz - omega t)}: EL = Dmat A + S (D = Dmat, S = source vector)."""
    E = sp.exp(sp.I * (k * z - om * t))
    amps = sp.symbols(" ".join(f"A{i}" for i in range(len(fields))))
    eqs = euler_equations(Lag, fields, [t, z])
    sub = {f: a_ * E for f, a_ in zip(fields, amps)}
    sub[Sf] = E
    rows = []
    for e in eqs:
        ex = (e.lhs - e.rhs).subs(sub).doit()
        rows.append(sp.expand(sp.simplify(ex / E)))
    Dm, bv = sp.linear_eq_to_matrix(rows, amps)
    return sp.Matrix(Dm).applyfunc(sp.simplify), sp.Matrix(-bv).applyfunc(sp.simplify)


Bsym = beta / (2 + 3 * beta)
W2 = sp.Symbol("W2", positive=True)


def omega2_roots(det):
    num = sp.numer(sp.together(det))
    return [sp.simplify(r_) for r_ in sp.solve(sp.Eq(num.subs(om, sp.sqrt(W2)), 0), W2)]


# ---- S0-3: this lane's dispersion (scalar block) and the tensor root with C1 present
beta_s03 = -beta if MUTATE else beta                            # m3: C1's sign flipped for the dispersion check only
s03 = {}
s03_ok = True
for tv in (1, 0):
    D6t, _ = plane_wave_matrix(lagrangian(beta_s03, tv, "P"), FIELDS6)
    sc = [0, 1, 3, 5]
    det_s = sp.factor(sp.simplify(D6t.extract(sc, sc).det()))
    roots = omega2_roots(det_s)
    expected = beta / (2 + 3 * beta) * k ** 2 * (Mp - 1 + tv * L ** 2 * k ** 2 / 2)
    resid = [sp.simplify(r_ - expected) for r_ in roots]
    x15str = sp.sympify(x15c["S0_3"][f"Theta{tv}"]["omega2_roots"][0], locals={"beta": beta, "k": k, "L": L, "M_P": Mp})
    vs15 = [sp.simplify(r_ - x15str) for r_ in roots]
    hit = len(roots) == 1 and resid[0] == 0 and vs15[0] == 0
    s03[f"Theta{tv}"] = {"det": str(det_s), "roots": [str(r_) for r_ in roots], "residual": [str(r_) for r_ in resid],
                         "vs_X15_string": [str(r_) for r_ in vs15], "match": hit}
    s03_ok = s03_ok and hit
DT, ST = plane_wave_matrix(lagrangian_TT(beta), [hpf, hxf])
detT = sp.factor(DT.det())
rootsT = omega2_roots(detT)
cT_ok = len(rootsT) == 1 and sp.simplify(rootsT[0] - k ** 2) == 0
s03["tensor"] = {"det": str(detT), "roots": [str(r_) for r_ in rootsT], "c_T_is_1": cT_ok}
RES["S0_3"] = s03
check("S0-3", s03_ok and cT_ok, f"scalar omega^2 roots Theta1 {s03['Theta1']['roots']}, Theta0 {s03['Theta0']['roots']} "
      f"(= X15's strings: {s03['Theta1']['vs_X15_string']}, {s03['Theta0']['vs_X15_string']}); tensor omega^2 = {rootsT} with C1"
      + (" (C1 sign flipped: m3)" if MUTATE else ""),
      "single khronon root beta k^2 (M - 1 + Theta L^2 k^2/2)/(2 + 3 beta), identical to X15; c_T = 1")


# ---- S0-4: C8's own script (copy run in step0_reruns/c8): K7 block; AST parse of the ledger and C8 PSR tables
def psr_tables(path):
    """AST-parse (no execution) every assignment `PSR = {name: dict(...)}` in a file."""
    with open(path) as fh:
        tree = ast.parse(fh.read())
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id == "PSR" for t_ in node.targets) \
                and isinstance(node.value, ast.Dict):
            tab = {}
            for kn, vn in zip(node.value.keys, node.value.values):
                name = ast.literal_eval(kn)
                if isinstance(vn, ast.Call):
                    d_ = {}
                    for kw in vn.keywords:
                        try:
                            d_[kw.arg] = ast.literal_eval(kw.value)
                        except ValueError:
                            if isinstance(kw.value, ast.BinOp) and isinstance(kw.value.op, ast.Div):
                                d_[kw.arg] = ast.literal_eval(kw.value.left) / ast.literal_eval(kw.value.right)
                    tab[name] = d_
            out.append(tab)
    return out


d8 = os.path.join(RERUN, "c8")
os.makedirs(d8, exist_ok=True)
cp8 = os.path.join(d8, "c8_instantaneous.py")
shutil.copyfile(P_C8, cp8)
sha_cp8 = sha256(cp8)
t1 = time.time()
pr8 = subprocess.run([sys.executable, cp8], capture_output=True, text=True, env=env_sub, cwd=d8, timeout=1800)
dt8 = time.time() - t1
os.remove(cp8)
with open(P_C8J) as fh:
    c8c = json.load(fh)
with open(os.path.join(d8, "c8_instantaneous_results.json")) as fh:
    c8r = json.load(fh)
k7c, k7r = c8c["K7"]["systems"], c8r["K7"]["systems"]
dev8 = 0.0
for nm in k7c:
    for key in ("a_m", "frac_Pbdot_precision"):
        dev8 = max(dev8, relmax(k7r[nm][key], k7c[nm][key]))
    for Ls in ("L20", "L24", "L90"):
        for key in ("eps", "eps_over_precision"):
            dev8 = max(dev8, relmax(k7r[nm][Ls][key], k7c[nm][Ls][key]))
        for fk in ("canonical", "alt"):
            dev8 = max(dev8, relmax(k7r[nm][Ls]["nonlinear"][fk], k7c[nm][Ls]["nonlinear"][fk]))
k7pass = any(c["id"] == "K7" and c["pass"] for c in c8r["checks"])
worst8 = c8r["K7"]["worst_ratio"]
led = [tb for tb in psr_tables(P_LED) if "J0737-3039A/B" in tb][0]
c8t = [tb for tb in psr_tables(P_C8) if "J0737-3039A/B" in tb][0]
tab_ok = True
tab_rows = {}
for nm in ("J0737-3039A/B", "B1913+16", "J1738+0333"):
    lp, cp_ = led[nm], c8t[nm]
    ok_ = (relmax(cp_["Pb"], lp["Pb"]) < 1e-12 and relmax(cp_["M"], lp["M"]) < 1e-12
           and relmax(cp_["frac"], lp["fPbdot"]) < 1e-12)
    tab_rows[nm] = {"ledger": {"Pb": lp["Pb"], "M": lp["M"], "fPbdot": lp["fPbdot"]},
                    "C8": {"Pb": cp_["Pb"], "M": cp_["M"], "frac": cp_["frac"]}, "agree": ok_}
    tab_ok = tab_ok and ok_
src_ok = "0.999963(63)" in led["J0737-3039A/B"]["src"] and "0.999963(63)" in c8t["J0737-3039A/B"]["src"]
# this lane's inputs against the record table (A1 PRE-RESULT: P_b and m1 + m2 to 1e-5) and C8's K7 formula (record inputs)
PC_C8 = 3.0856775814913673e16
inp_ok = True
inp_rows = {}
for nm in ("J0737-3039A/B", "B1913+16", "J1738+0333"):
    b_ = BIN[nm]
    dPb = relmax(b_["Pb"], led[nm]["Pb"])
    dM = relmax(b_["m1"] + b_["m2"], led[nm]["M"])
    inp_rows[nm] = {"dPb_rel": dPb, "dMtot_rel": dM}
    inp_ok = inp_ok and dPb < 1e-5 and dM < 1e-5
own8 = 0.0
for nm in k7c:
    a_ = (GM_SUN * c8t[nm]["M"] * (c8t[nm]["Pb"] * 86400) ** 2 / (4 * np.pi ** 2)) ** (1 / 3)
    for Ls in (20, 24, 90):
        own8 = max(own8, relmax((a_ / (Ls * PC_C8)) ** 2, k7c[nm][f"L{Ls}"]["eps"]))
s04 = (sha_cp8 == SHA["C8"] and sha256(P_C8J) == SHA["C8J"] and sha256(P_LED) == SHA["LED"] and pr8.returncode == 0
       and k7pass and dev8 < 1e-12 and abs(worst8 / 3.219e-14 - 1) < 1e-3 and tab_ok and src_ok and inp_ok and own8 < 1e-9)
RES["S0_4"] = {"copy_sha_ok": sha_cp8 == SHA["C8"], "returncode": pr8.returncode, "K7_pass": k7pass,
               "K7_rerun_vs_committed_max_rel": dev8, "worst_ratio": worst8, "tables": tab_rows,
               "J0737_src_has_0.999963(63)": src_ok, "lane_inputs_vs_record": inp_rows, "own_K7_eps_max_rel": own8,
               "runtime_s": dt8, "c8_stdout_tail": pr8.stdout.strip().splitlines()[-1] if pr8.stdout.strip() else ""}
check("S0-4", s04, f"C8 copy exit {pr8.returncode}, K7 {'PASS' if k7pass else 'FAIL'}, K7 block vs committed {dev8:.1e}, "
      f"worst ratio {worst8:.4e}; ledger/C8 tables agree {tab_ok}, '0.999963(63)' {src_ok}; lane inputs vs record "
      f"(P_b, m1+m2): " + ", ".join(f"{nm} {v_['dPb_rel']:.1e}/{v_['dMtot_rel']:.1e}" for nm, v_ in inp_rows.items()) + "; "
      f"own K7 eps {own8:.1e}; {dt8:.0f} s" + (" (J0737 P_b x 1.01: m4)" if MUTATE else ""),
      "C8's own code reproduces the record's binary-pulsar K7 block (double pulsar 0.999963(63), precision 6.3e-5)")


# ---- S0-5: Peters-Mathews from this lane's inputs vs the record's GR Pbdot
def f_e(e):
    return (1 + 73 / 24 * e ** 2 + 37 / 96 * e ** 4) / (1 - e ** 2) ** 3.5


def pbdot_gr(b_):
    m = b_["m1"] + b_["m2"]
    return -(192 * math.pi / 5) * (2 * math.pi / (b_["Pb"] * DAY)) ** (5 / 3) * T_SUN ** (5 / 3) * b_["m1"] * b_["m2"] \
        / m ** (1 / 3) * f_e(b_["e"])


s05 = True
pm_rows = {}
for nm, b_ in BIN.items():
    v_ = pbdot_gr(b_)
    dv = relmax(v_, b_["PbdotGR"])
    ok_ = dv < b_["tol"]
    if b_["GR_int"]:
        c_, up, dn = b_["GR_int"]
        ok_ = ok_ and (c_ - dn <= v_ <= c_ + up)
    pm_rows[nm] = {"PM": v_, "record": b_["PbdotGR"], "rel": dv, "tol": b_["tol"], "ok": ok_}
    s05 = s05 and ok_
RES["S0_5"] = pm_rows
check("S0-5", s05, "; ".join(f"{nm}: {r_['PM']:.6e} vs {r_['record']:.6e} (rel {r_['rel']:.1e})" for nm, r_ in pm_rows.items()),
      "Peters-Mathews with this lane's inputs reproduces the record's GR Pbdot (1e-3; 1e-2 and inside the interval)")

with open(P_P3J) as fh:
    p3 = json.load(fh)
RES["P3_double_pulsar_mixing_eps_max"] = {"value": p3["double_pulsar_mixing_eps_max"], "sha_ok": sha256(P_P3J) == SHA["P3J"]}
log(f"  reported: P3 double_pulsar_mixing_eps_max = {p3['double_pulsar_mixing_eps_max']:.3e} (read, not rerun)")

S0_OK = all(c["pass"] for c in CHECKS if c["id"].startswith("S0-"))
RES["S0_all_pass"] = S0_OK
if not S0_OK and not MUTATE:
    log("STOP RULE: a step-0 reproduction failed; verdict UNDECIDED, nothing further is scored.")
    RES["verdict"] = "UNDECIDED (step 0 failed)"
    finish(1)

# ===================================================================================================== PART D
log("")
log("PART D (step 1): the scalar's radiation in v3s + C1 (sympy)")
D6, S6 = plane_wave_matrix(lagrangian(beta, Th, "P"), FIELDS6)
herm = sp.simplify(D6 - D6.H) == sp.zeros(6, 6)
SC, VE = [0, 1, 3], [2, 4]
decoupled = all(sp.simplify(D6[i, j]) == 0 for i in [0, 1, 3, 5] for j in VE)
detV = sp.simplify(D6.extract(VE, VE).det())
vec_no_omega = not detV.has(om)
Dss, DsP, DPP = D6.extract(SC, SC), D6.extract(SC, [5]), D6[5, 5]
Deff = (Dss - DsP * D6.extract([5], SC) / DPP).applyfunc(sp.simplify)
real_sym = sp.simplify(Deff - Deff.T) == sp.zeros(3, 3) and all(sp.simplify(sp.im(e_)) == 0 for e_ in Deff)
src_P3_zero = sp.simplify(S6[5]) == 0 and sp.simplify(S6[4]) == 0
RES["D_HERM"] = {"hermitian": herm, "scalar_vector_decoupled": decoupled, "vector_det": str(detV),
                 "vector_det_has_omega": not vec_no_omega, "Deff_real_symmetric": real_sym, "P_source_zero": src_P3_zero,
                 "Deff": str(Deff), "S": str(S6.T)}
check("D-HERM", herm and decoupled and vec_no_omega and real_sym and src_P3_zero,
      f"D(omega,k) Hermitian {herm}; scalar/vector blocks decoupled {decoupled}; vector det {detV} (no omega zero "
      f"{vec_no_omega}); (n, psi, N3) block after eliminating P3 real symmetric {real_sym}",
      "plane-wave operator Hermitian; only the scalar block can radiate")

# ---- residue at the scalar pole (screened Theta = 1)
Deff1 = Deff.subs(Th, 1).applyfunc(sp.simplify)
Svec = sp.Matrix([S6[0], S6[1], S6[3]])
detE = sp.factor(sp.simplify(Deff1.det()))
w2s_list = omega2_roots(detE)
w2s = w2s_list[0]
adjE = Deff1.adjugate().applyfunc(sp.simplify)
omS = sp.sqrt(w2s)
dden = sp.simplify((sp.diff(detE, om) / (2 * om)).subs(om, omS))
Rmat = (adjE.subs(om, omS) / dden).applyfunc(sp.simplify)          # R = lim (w_S^2 - w^2)(-D^-1) = adj/det'(w_S^2)
eta_k = 2 / (Mp + L ** 2 * k ** 2 / 2)
Sig = T_s + 2 / eta_k * rho_s - omS * Jz_s / (Bsym * k)
Rform = sp.simplify((Svec.T * Rmat * Svec)[0])
res_form = sp.simplify(Rform - Kc * Bsym * Sig ** 2)
vvec = -sp.Matrix([2 / eta_k, 1, omS / (Bsym * k)])
res_mat = (Rmat - Kc * Bsym * vvec * vvec.T).applyfunc(sp.simplify)
minors = [sp.simplify(Rmat[i, j] * Rmat[p, q] - Rmat[i, q] * Rmat[p, j]) for i in range(3) for p in range(3)
          for j in range(3) for q in range(3) if i < p and j < q]
rank1 = all(m_ == 0 for m_ in minors)
KB_pos = sp.simplify(Kc * Bsym).is_positive
RES["D_RES"] = {"omega_S2": str(w2s), "n_roots": len(w2s_list), "R_form_minus_KB_Sigma2": str(res_form),
                "R_matrix_minus_KB_vvT": str(res_mat), "rank1": rank1, "KB_positive": KB_pos,
                "Sigma": "T + (2/eta) rho - omega J_z/(B k)"}
check("D-RES", len(w2s_list) == 1 and res_form == 0 and res_mat == sp.zeros(3, 3) and rank1 and KB_pos,
      f"omega_S^2 = {w2s}; S^T R S - K B Sigma^2 = {res_form}; R - K B v v^T = 0: {res_mat == sp.zeros(3, 3)}; rank 1 {rank1}; "
      f"K B > 0 {KB_pos}", "residue rank 1, positive for beta > 0, S^dag R S = K B |T + (2/eta) rho - omega J/(B k)|^2")

Sig_on = sp.simplify(Sig.subs(Jz_s, omS * rho_s / k))
don = sp.simplify(Sig_on - (T_s + rho_s))
RES["D_ON"] = {"Sigma_on_shell_conserved_minus_(T+rho)": str(don)}
check("D-ON", don == 0, f"Sigma(J = omega rho/k, on shell) - (T + rho) = {don}",
      "a conserved source couples on shell through T + rho")

# ---- n_g and the closed forms per harmonic (symbols: c_S = omega/k)
ng_expr = sp.simplify(k * sp.diff(w2s, k) / w2s)
ng_target = 2 + L ** 2 * k ** 2 / (Mp - 1 + L ** 2 * k ** 2 / 2)
ng_ok = sp.simplify(ng_expr - ng_target) == 0
cS, ng, Gs, Bs, Q2s, I2s, D2s = sp.symbols("c_S n_g G B Q2 I2 D2", positive=True)
kk = om / cS


def P_generic(angint):
    """(pi omega/2) Int d^3k/(2 pi)^3 K B |Sigma|^2 delta(omega^2 - omega_S^2) = (pi omega/2)(1/8 pi^3)(k^3/(n_g omega^2)) K B angint"""
    return sp.pi * om / 2 / (8 * sp.pi ** 3) * kk ** 3 / (ng * om ** 2) * 4 * sp.pi * Gs * Bs * angint


Zk = 1 + kk ** 2 / (3 * om ** 2)
two_over_eta_on = 1 + om ** 2 / (Bs * kk ** 2)
Pq = P_generic(kk ** 4 / 4 * sp.Rational(8, 15) * sp.pi * Q2s)
Pm = P_generic(4 * sp.pi * om ** 4 / 4 * Zk ** 2 * I2s)
Pd = P_generic(sp.Rational(4, 3) * sp.pi * kk ** 2 * two_over_eta_on ** 2 * D2s)
tq = Gs * Bs / (30 * ng) * om ** 6 * Q2s / cS ** 7
tm = Gs * Bs / (4 * ng) * (1 + 1 / (3 * cS ** 2)) ** 2 * om ** 6 * I2s / cS ** 3
td = Gs / (3 * ng * Bs) * (1 + Bs / cS ** 2) ** 2 * om ** 4 * D2s / cS
form_res = [sp.simplify(Pq - tq), sp.simplify(Pm - tm), sp.simplify(Pd - td)]
RES["D_FORM"] = {"n_g": str(ng_expr), "n_g_minus_target": str(sp.simplify(ng_expr - ng_target)),
                 "P_quad": str(tq), "P_mono": str(tm), "P_dip": str(td), "residuals": [str(r_) for r_ in form_res]}
check("D-FORM", ng_ok and all(r_ == 0 for r_ in form_res),
      f"n_g = {ng_expr}; P_quad = {tq}; P_mono = {tm}; P_dip = {td}; residuals {form_res}",
      "closed per-harmonic forms from the power formula (on-shell Sigma, isotropic angular integrals)")

# ---- ANG: angular identities by quadrature; D-GR: the tensor sector through the same power formula
rng = np.random.default_rng(16)
mu_gl, w_gl = np.polynomial.legendre.leggauss(24)
phis = np.linspace(0, 2 * np.pi, 48, endpoint=False)
dirs, wts = [], []
for mu_, wmu in zip(mu_gl, w_gl):
    st_ = math.sqrt(1 - mu_ ** 2)
    for ph in phis:
        dirs.append(np.array([st_ * math.cos(ph), st_ * math.sin(ph), mu_]))
        wts.append(wmu * 2 * np.pi / len(phis))
dirs, wts = np.array(dirs), np.array(wts)
Araw = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
Qr = (Araw + Araw.T) / 2
Qr = Qr - np.trace(Qr) / 3 * np.eye(3)
Dr = rng.normal(size=3) + 1j * rng.normal(size=3)
q_dir = np.einsum("ni,ij,nj->n", dirs, Qr, dirs)
ang1 = abs(np.sum(wts * abs(q_dir) ** 2) / (8 * np.pi / 15 * np.sum(abs(Qr) ** 2)) - 1)
ang2 = abs(np.sum(wts * q_dir)) / np.sqrt(np.sum(abs(Qr) ** 2))
ang3 = abs(np.sum(wts * abs(dirs @ Dr) ** 2) / (4 * np.pi / 3 * np.sum(abs(Dr) ** 2)) - 1)
RES["ANG"] = {"quad": ang1, "mono_quad_cross": ang2, "dipole": ang3}
check("ANG", max(ang1, ang2, ang3) < 1e-12, f"rel. dev. {ang1:.1e}, {ang2:.1e}, {ang3:.1e}",
      "isotropic angular identities (8 pi/15, 0, 4 pi/3) by quadrature")

src_fac = 1 if MUTATE else sp.Rational(1, 2)                    # m5: tensor source h_ij T^ij instead of (1/2) h_ij T^ij
DT2, ST2 = plane_wave_matrix(lagrangian_TT(beta, src_fac), [hpf, hxf])
detT2 = sp.factor(DT2.det())
RT = []
for i in range(2):
    dpol = sp.simplify(DT2[i, i])
    RT.append(sp.simplify(2 * k / sp.diff(dpol, om).subs(om, k)))        # lim (k^2 - w^2)(-1/D) = 1/(dD/dw^2) at w = k
fJp = sp.lambdify((Txx, Tyy, Txy), ST2[0], "numpy")
fJx = sp.lambdify((Txx, Tyy, Txy), ST2[1], "numpy")
RTn = [float(r_.subs(Kc, 4 * sp.pi)) for r_ in RT]              # G = 1 numerics
Tr = -0.5 * Qr                                                  # T^ij = -(1/2) omega^2 I_ij at omega = 1 (STF part)
acc = 0.0
for nvec, wv in zip(dirs, wts):
    tmp = np.array([0.0, 0.0, 1.0]) if abs(nvec[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    e1 = np.cross(nvec, tmp)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(nvec, e1)
    Rm = np.array([e1, e2, nvec])
    Tk = Rm @ Tr @ Rm.T
    acc += wv * (RTn[0] * abs(fJp(Tk[0, 0], Tk[1, 1], Tk[0, 1])) ** 2 + RTn[1] * abs(fJx(Tk[0, 0], Tk[1, 1], Tk[0, 1])) ** 2)
P_GR_formula = math.pi / 2 / (8 * math.pi ** 3) * (1 / 2) * acc     # omega = k = 1, n_g = 2
P_GR_target = np.sum(abs(Qr) ** 2) / 10                           # (G/10) omega^6 |Q|^2 at G = omega = 1
dgr = abs(P_GR_formula / P_GR_target - 1)
RES["D_GR"] = {"tensor_det": str(detT2), "residues": [str(r_) for r_ in RT], "P_formula": P_GR_formula,
               "P_target": P_GR_target, "rel_dev": dgr}
check("D-GR", dgr < 1e-10, f"tensor residues {RT}; P_formula/[(G/10) omega^6 |Q|^2] - 1 = {dgr:.1e}"
      + (" (source factor 1: m5)" if MUTATE else ""), "the power formula reproduces GR's quadrupole flux (G/5)<Q'''Q'''>")

# ---- X-LIT: constant-alpha control vs Yagi et al. 2014 Eqs. 118, 120-124 (PROVISIONAL), and the dispersive statement
DA, SA = plane_wave_matrix(lagrangian(beta, 1, "alpha"), FIELDS4A)
DsA = DA.extract([0, 1, 3], [0, 1, 3])
detA = sp.factor(sp.simplify(DsA.det()))
w2a = omega2_roots(detA)[0]
cs2_lane = sp.simplify(w2a / k ** 2)
lam = beta                                                      # the record's beta is BPS/Yagi's lambda
bB = sp.Integer(0)                                              # beta_BPS = 0
cs2_yagi = (al - 2) * (bB + lam) / (al * (bB - 1) * (2 + bB + 3 * lam))
a1_kh = 4 * (al - 2 * bB) / (bB - 1)
a2_kh = (al - 2 * bB) * (-bB ** 2 + bB * (al - 3) + al + lam * (-1 - 3 * bB + 2 * al)) / ((bB - 1) * (lam + bB) * (al - 2))
Zy = (a1_kh - 2 * a2_kh) * (1 - bB) / (3 * (2 * bB - al))
csy = sp.sqrt(cs2_yagi)
A1m1_y = 3 * al * (Zy - 1) ** 2 / (2 * csy * (2 - al))
B1_y = al * Zy ** 2 / (4 * csy * (2 - al))
C_y = 4 / (3 * csy ** 3 * al * (2 - al))
csl = sp.sqrt(cs2_lane)
# residue of the control: K B |T + (2/alpha) rho - omega J/(B k)|^2
adjA = DsA.adjugate().applyfunc(sp.simplify)
omA = sp.sqrt(w2a)
ddA = sp.simplify((sp.diff(detA, om) / (2 * om)).subs(om, omA))
SvA = sp.Matrix([SA[0], SA[1], SA[3]])
RformA = sp.simplify((SvA.T * (adjA.subs(om, omA) / ddA) * SvA)[0])
resA = sp.simplify(RformA - Kc * Bsym * (T_s + 2 / al * rho_s - omA * Jz_s / (Bsym * k)) ** 2)
ngA = sp.simplify(k * sp.diff(w2a, k) / w2a)
# lane coefficients (n_g = 2): quad ratio B/(3 n_g c^7); mono G-coefficient of <I'''^2> = B Z^2/(2 n_g c^3);
# dipole G-coefficient of <Sigma-dot^2> (momentum frame) = 2/(3 n_g B c)(1 + B/c^2)^2; frame A (m6) drops (1 + B/c^2)^2
lane_q = Bsym / (3 * 2 * csl ** 7)
lane_m = Bsym * (1 + 1 / (3 * csl ** 2)) ** 2 / (2 * 2 * csl ** 3)
dip_frame = 1 if MUTATE else (1 + Bsym / csl ** 2) ** 2          # m6: dipole in the sum m v = 0 frame
lane_d = 2 / (3 * 2 * Bsym * csl) * dip_frame
xl = [sp.simplify(cs2_lane - cs2_yagi), sp.simplify(lane_q - A1m1_y), sp.simplify(lane_m - B1_y),
      sp.simplify(lane_d - C_y), resA, sp.simplify(ngA - 2)]
xl = [sp.simplify(sp.radsimp(x_)) for x_ in xl]
# dispersive statement: v3s + C1 coefficients = (2/n_g) x Yagi at alpha = eta(k_S), c_s = omega/k_S (c_s^2 = B(2 - eta)/eta)
et = sp.Symbol("eta", positive=True)
cs_e = sp.sqrt(Bsym * (2 - et) / et)
yq, ym, yd = [x_.subs(al, et) for x_ in (A1m1_y, B1_y, C_y)]
disp = [sp.simplify(Bsym / (3 * ng * cs_e ** 7) - 2 / ng * yq),
        sp.simplify(Bsym * (1 + 1 / (3 * cs_e ** 2)) ** 2 / (2 * ng * cs_e ** 3) - 2 / ng * ym),
        sp.simplify(2 / (3 * ng * Bsym * cs_e) * (1 + Bsym / cs_e ** 2) ** 2 - 2 / ng * yd)]
disp = [sp.simplify(sp.radsimp(x_)) for x_ in disp]
# Einstein-aether (Foster via Yagi Eqs. 107-114) in the matching limit c14 = alpha, c+ = c13 = 0, c2 = lambda (reported)
c14, c2a = al, lam
w0sq = (2 - c14) * c2a / ((2 + 3 * c2a) * c14)
aeth = [sp.simplify(w0sq - cs2_yagi)]
RES["X_LIT"] = {"cs2_lane": str(cs2_lane), "cs2_yagi_eq118": str(sp.simplify(cs2_yagi)), "Z_yagi_minus_1": str(sp.simplify(Zy - 1)),
                "residuals[cs2, A1-1/ct, B1, C, residue, n_g-2]": [str(x_) for x_ in xl],
                "dispersive_(2/n_g)_statement_residuals": [str(x_) for x_ in disp],
                "aether_w0^2_minus_cs^2": [str(x_) for x_ in aeth],
                "lane_coeffs": {"quad": str(sp.simplify(lane_q)), "mono": str(sp.simplify(lane_m)), "dip": str(sp.simplify(lane_d))},
                "yagi_coeffs": {"A1-1/ct": str(sp.simplify(A1m1_y)), "B1": str(sp.simplify(B1_y)), "C": str(sp.simplify(C_y))}}
check("X-LIT", all(x_ == 0 for x_ in xl) and all(x_ == 0 for x_ in disp),
      f"constant-alpha control minus Yagi Eqs. 118, 121-124 [c_s^2, A1 - 1/c_t, B1, C, residue form, n_g - 2] = {xl}; "
      f"v3s+C1 minus (2/n_g) Yagi(alpha = eta, c_s = omega/k_S) = {disp}" + (" (dipole in the sum m v = 0 frame: m6)" if MUTATE else ""),
      "the machinery reproduces the khronometric binary flux exactly (PROVISIONAL literature); v3s + C1 = (2/n_g) x it at alpha = eta(k_S)")

# ---- D-LIM: L* -> infinity (P decoupled) at fixed (omega, beta, M), exact dispersion; GR + lambda alone
mM = sp.Symbol("m", nonnegative=True)                           # M = 1 + m
qL = (-mM + sp.sqrt(mM ** 2 + 2 * L ** 2 * om ** 2 / Bs)) / L ** 2
ngL = 2 + L ** 2 * qL / (mM + L ** 2 * qL / 2)
cS1 = om / sp.sqrt(qL)
coef_q = Bs / (30 * ngL * cS1 ** 7)
coef_m = Bs / (4 * ngL) * (1 + 1 / (3 * cS1 ** 2)) ** 2 / cS1 ** 3
coef_d = 1 / (3 * ngL * Bs) * (1 + Bs / cS1 ** 2) ** 2 / cS1
lims = [sp.limit(c_, L, sp.oo) for c_ in (coef_q, coef_m, coef_d)]
DG, _ = plane_wave_matrix(lagrangian(beta, 1, "GR"), FIELDS4A)
detG = sp.simplify(DG.extract([0, 1, 3], [0, 1, 3]).det())
rootsG = omega2_roots(detG) if detG != 0 else []
RES["D_LIM"] = {"limits_Lstar_inf[quad, mono, dip]": [str(x_) for x_ in lims], "GR_plus_lambda_scalar_det": str(detG),
                "GR_plus_lambda_omega2_roots": [str(r_) for r_ in rootsG]}
check("D-LIM", all(x_ == 0 for x_ in lims) and len(rootsG) == 0,
      f"lim_(L*->inf) [quad, mono, dip] coefficients = {lims}; GR + lambda-only scalar det {detG} has omega^2 roots {rootsG}",
      "the scalar flux vanishes when the P sector decouples (eta -> 0); GR + C1 alone has no radiating scalar")

# ===================================================================================================== PART H
log("")
log("PART H: Kepler harmonics")
SKIP_KEPLER = MUTATE                                            # m7: eccentric anomaly = mean anomaly


def harmonics(b_):
    m1, m2, e = b_["m1"], b_["m2"], b_["e"]
    m = m1 + m2
    GMt = m * GM_SUN
    Pb = b_["Pb"] * DAY
    Om = 2 * math.pi / Pb
    a = (GMt / Om ** 2) ** (1 / 3)
    mu = m1 * m2 / m * M_SUN
    Mm = 2 * np.pi * np.arange(NSAMP) / NSAMP
    E = Mm.copy()
    if not SKIP_KEPLER:
        E = Mm + e * np.sin(Mm)
        for _ in range(60):
            E = E - (E - e * np.sin(E) - Mm) / (1 - e * np.cos(E))
    x = a * (np.cos(E) - e)
    y = a * math.sqrt(1 - e ** 2) * np.sin(E)

    def hm(arr):
        return 2 * np.fft.ifft(arr)[1:NMAX + 1]
    xn, yn = hm(x), hm(y)
    Ixx, Iyy, Ixy = hm(mu * x * x), hm(mu * y * y), hm(mu * x * y)
    Ikk = Ixx + Iyy
    Q2 = abs(Ixx - Ikk / 3) ** 2 + abs(Iyy - Ikk / 3) ** 2 + abs(Ikk / 3) ** 2 + 2 * abs(Ixy) ** 2
    n = np.arange(1, NMAX + 1)
    return dict(Om=Om, a=a, mu=mu, m_kg=m * M_SUN, e=e, n=n, w=n * Om, Q2=Q2, I2=abs(Ikk) ** 2, r2=abs(xn) ** 2 + abs(yn) ** 2,
                Ikk=Ikk, Qmax=np.sqrt(Q2))


HAR = {nm: harmonics(b_) for nm, b_ in BIN.items()}
hpm_ok = True
hpm = {}
for nm, h in HAR.items():
    PGR = np.sum(G / C_SI ** 5 / 10 * h["w"] ** 6 * h["Q2"])
    PM = 32 / 5 * G ** 4 * (h["mu"]) ** 2 * h["m_kg"] ** 3 * f_e(h["e"]) / (C_SI ** 5 * h["a"] ** 5)
    acc2 = np.sum(0.5 * h["w"] ** 4 * h["r2"])
    acc2_t = (G * h["m_kg"]) ** 2 * (1 + h["e"] ** 2 / 2) / (h["a"] ** 4 * (1 - h["e"] ** 2) ** 2.5)
    d1, d2 = relmax(PGR, PM), relmax(acc2, acc2_t)
    hpm[nm] = {"P_GR_harmonic_sum_W": PGR, "Peters_Mathews_W": PM, "rel": d1, "acc2_rel": d2}
    hpm_ok = hpm_ok and d1 < 1e-6 and d2 < 1e-6
RES["H_PM"] = hpm
check("H-PM", hpm_ok, "; ".join(f"{nm}: P_GR rel {v_['rel']:.1e}, <|a|^2> rel {v_['acc2_rel']:.1e}" for nm, v_ in hpm.items())
      + (" (Kepler skipped: m7)" if MUTATE else ""), "harmonic sums reproduce Peters-Mathews f(e) and the dipole (1 + e^2/2) factor")

# ===================================================================================================== PART W
log("")
log("PART W (step 2): the window against the record's binary-pulsar bounds")
K_SI = 4 * math.pi * G


def sens(bval, Ls, M, m_ns):
    eta_R = 2 / (M + Ls ** 2 / (2 * R_NS ** 2))
    a1 = -4 * eta_R
    a2 = eta_R * (eta_R * (1 + 2 * bval) - bval) / (bval * (2 - eta_R))
    s1 = OMEGA_OVER_M * abs(a1 - 2 * a2 / 3)
    s2 = 3 * s1
    s3 = max(s2, G * m_ns * M_SUN / (C_SI ** 2 * Ls))
    return {"sigma0": 0.0, "sigma1": s1, "sigma2": s2, "sigma3": s3, "sigmaX": OMEGA_OVER_M * bval}


def disp_k(w, B, Ls, M):
    q = (-(M - 1) + np.sqrt((M - 1) ** 2 + 2 * Ls ** 2 * w ** 2 / (B * C_SI ** 2))) / Ls ** 2
    kS = np.sqrt(q)
    ch = w / (kS * C_SI)
    eta = 2 / (M + Ls ** 2 * q / 2)
    ngv = 2 + Ls ** 2 * q / (M - 1 + Ls ** 2 * q / 2)
    return kS, ch, eta, ngv


def score(nm, bval, Ls, M):
    b_, h = BIN[nm], HAR[nm]
    B = bval / (2 + 3 * bval)
    w = h["w"]
    kS, ch, eta, ngv = disp_k(w, B, Ls, M)
    Z = 1 + 1 / (3 * ch ** 2)
    pref = G / C_SI ** 5
    PGRn = pref / 10 * w ** 6 * h["Q2"]
    Pq_n = pref * B / (30 * ngv * ch ** 7) * w ** 6 * h["Q2"]
    Pm_n = pref * B / (4 * ngv * ch ** 3) * Z ** 2 * w ** 6 * h["I2"]
    Pd1_n = G / C_SI ** 3 / (3 * ngv * B * ch) * (1 + B / ch ** 2) ** 2 * w ** 4 * h["mu"] ** 2 * h["r2"]
    A2 = 2 * (Z - 1) / ((eta - 2) * ch ** 3)
    A3 = 2 / (3 * eta * (2 - eta) * ch ** 5)
    B2c = Z / (3 * ch ** 3 * (eta - 2))
    B3c = 1 / (9 * eta * ch ** 5 * (2 - eta))
    PGR = PGRn.sum()
    dq, dm = Pq_n.sum() / PGR, Pm_n.sum() / PGR
    dd1 = Pd1_n.sum() / PGR
    m_ns = max(b_["m1"], b_["m2"]) if b_["kind"] == "NS-NS" else b_["m1"]
    sv = sens(bval, Ls, M, m_ns)
    out = {"delta_quad": dq, "delta_mono": dm, "delta_dip_per_ds2": dd1, "s": sv}
    for br, s_ in sv.items():
        PS = np.sum(2 / ngv * ((abs(A2) * s_ + abs(A3) * s_ ** 2) * PGRn + (abs(B2c) * s_ + abs(B3c) * s_ ** 2) * pref * 0.5
                               * w ** 6 * h["I2"]))
        out[f"delta_{br}"] = dq + dm + s_ ** 2 * dd1 + PS / PGR
        out[f"deltaS_{br}"] = PS / PGR
    out["s_crit"] = math.sqrt(max(b_["dplus"] - dq - dm, 0) / dd1)
    # significant harmonics, validity margins
    wq = PGRn / PGR
    wm = Pm_n / max(Pm_n.sum(), 1e-300)
    wd = Pd1_n / dd1 / PGR
    sig = (wq > 1e-20) | (wm > 1e-20) | (wd > 1e-20)
    stiff = (Ls ** 2 * kS ** 2 / 2)[sig] / (1e3 * max(M - 1, 1))
    out["k4_margin_min"] = float(stiff.min())
    out["ng_dev_max"] = float(abs(ngv[sig] - 4).max())
    out["ka_max"] = float((kS[sig] * h["a"] * (1 + h["e"])).max())
    # P-LIN: C1 dominance at r = 2 pi/k_S (n = 1 and the strongest GR harmonic) and at r = a
    lin = []
    for i_ in sorted({0, int(np.argmax(PGRn))}):
        rS = 2 * math.pi / kS[i_]
        rho_t = h["m_kg"] / (2 * math.pi * Ls ** 2 * rS) + RHO_GAL
        lin.append(B * C_SI ** 2 * kS[i_] ** 2 / (K_SI * rho_t))
    rho_a = h["m_kg"] / (2 * math.pi * Ls ** 2 * h["a"]) + RHO_GAL
    lin.append(B * C_SI ** 2 / (K_SI * rho_a * h["a"] ** 2))
    out["C1_dominance_min"] = float(min(lin))
    # P-WAVE under sigma3 at the strongest scalar harmonic
    ds3 = sv["sigma3"]
    PSn = Pq_n + Pm_n + ds3 ** 2 * Pd1_n
    i_ = int(np.argmax(PSn))
    kk_, wc_ = kS[i_], w[i_] / C_SI
    rS = 2 * math.pi / kk_
    Sig_m = 0.5 * wc_ ** 2 * Z[i_] * abs(h["Ikk"][i_])
    Sig_q = 0.5 * kk_ ** 2 * h["Qmax"][i_]
    Sig_d = (1 + wc_ ** 2 / (B * kk_ ** 2)) * kk_ * h["mu"] * ds3 * math.sqrt(h["r2"][i_])
    dDP = B * (Sig_m + Sig_q + Sig_d) * kk_ ** 4 / (2 * math.pi * rS * ngv[i_] * wc_ ** 2)
    bgDP = h["m_kg"] / (2 * math.pi * Ls ** 2 * rS)
    out["wave_ratio"] = dDP / bgDP
    out["phase_speed_c"] = float(ch[1] if len(ch) > 1 else ch[0])     # n = 2
    out["group_speed_c"] = float(ngv[1] / 2 * ch[1])
    out["k_S_n2"] = float(kS[1])
    out["eta_kS_n2"] = float(eta[1])
    out["lambda_S_n2_m"] = float(2 * math.pi / kS[1])
    out["n_g_n2"] = float(ngv[1])
    out["PGR_W"] = PGR
    return out


BR_SCORED = ["sigma0", "sigma1", "sigma2", "sigma3"]
KEEP = {"delta_quad", "delta_mono", "delta_dip_per_ds2", "delta_sigma0", "delta_sigma1", "delta_sigma2", "delta_sigma3",
        "delta_sigmaX", "s", "s_crit", "k4_margin_min", "ng_dev_max", "ka_max", "C1_dominance_min", "wave_ratio",
        "phase_speed_c", "eta_kS_n2"}                           # A3 (POST-RESULT): JSON grid rows store these keys only
grid_res = {}
win = {}
k4_ok, lin_ok, wave_ok = True, True, True
worst = {}
mu_corr = max((mu_ ** 2) * (LSTAR_PC[f_] * PC) ** 2 / 2 for mu_ in MUK.values() for f_ in FOOT)
lin_ok = lin_ok and mu_corr <= 1e-3
for foot in FOOT:
    Ls = LSTAR_PC[foot] * PC
    grid_res[foot] = {}
    win[foot] = {}
    for lab in MUK:
        bgrid = np.geomspace(BETA_MIN[foot], BETA_MAX[lab], 41) if BETA_MAX[lab] > BETA_MIN[foot] else np.array([])
        rows = []
        surv = []
        for bval in bgrid:
            row = {"beta": float(bval), "binaries": {}}
            ok_pt = True
            for nm in BIN:
                per_M = {}
                for M in M_BG:
                    sc_ = score(nm, bval, Ls, M)
                    per_M[f"M{M:g}"] = sc_
                    for br in BR_SCORED:
                        ok_pt = ok_pt and sc_[f"delta_{br}"] <= BIN[nm]["dplus"]
                    k4_ok = k4_ok and sc_["k4_margin_min"] >= 1 and sc_["ng_dev_max"] <= 1e-2 and sc_["ka_max"] <= 1e-2
                    lin_ok = lin_ok and sc_["C1_dominance_min"] >= 1e3
                    wave_ok = wave_ok and sc_["wave_ratio"] <= 1e-3
                    for key in ("delta_sigma3", "delta_sigmaX", "delta_mono", "delta_quad", "wave_ratio", "C1_dominance_min",
                                "k4_margin_min", "ka_max", "ng_dev_max"):
                        wk = (foot, lab, nm, key)
                        val = sc_[key]
                        if key in ("C1_dominance_min", "k4_margin_min"):
                            worst[wk] = min(worst.get(wk, float("inf")), val)
                        else:
                            worst[wk] = max(worst.get(wk, 0.0), val)
                    wk = (foot, lab, nm, "s_crit_min")
                    worst[wk] = min(worst.get(wk, float("inf")), sc_["s_crit"])
                row["binaries"][nm] = {mk: {k_: v_ for k_, v_ in d_.items() if k_ in KEEP} for mk, d_ in per_M.items()}
            row["pass"] = ok_pt
            rows.append(row)
            if ok_pt:
                surv.append(float(bval))
        grid_res[foot][lab] = rows
        win[foot][lab] = {"grid_n": len(bgrid), "surviving_n": len(surv),
                          "surviving_range": [min(surv), max(surv)] if surv else None}
RES["grid"] = grid_res
RES["window"] = win
RES["worst"] = {" | ".join(k_): v_ for k_, v_ in worst.items()}
RES["mu_K_correction_max"] = mu_corr
for foot in FOOT:
    for lab in MUK:
        log(f"  {foot} {lab}: surviving {win[foot][lab]['surviving_n']}/{win[foot][lab]['grid_n']} {win[foot][lab]['surviving_range']}")
        for nm in BIN:
            log(f"    {nm:14s} delta_mono <= {worst[(foot, lab, nm, 'delta_mono')]:.3e}, delta_quad <= "
                f"{worst[(foot, lab, nm, 'delta_quad')]:.3e}, delta(sigma3) <= {worst[(foot, lab, nm, 'delta_sigma3')]:.3e} "
                f"(delta+ {BIN[nm]['dplus']:.3g}); s_crit >= {worst[(foot, lab, nm, 's_crit_min')]:.3e}; "
                f"counterfactual sigmaX delta <= {worst[(foot, lab, nm, 'delta_sigmaX')]:.3e}")
k4_line = "; ".join(f"{k_[0]} {k_[1]} {k_[2]}: stiff margin {worst[(k_[0], k_[1], k_[2], 'k4_margin_min')]:.1e}, "
                    f"|n_g-4| {worst[(k_[0], k_[1], k_[2], 'ng_dev_max')]:.1e}, k a {worst[(k_[0], k_[1], k_[2], 'ka_max')]:.1e}"
                    for k_ in worst if k_[3] == "k4_margin_min" and k_[1] == "mu_0.03")
check("D-K4", k4_ok, k4_line, "radiated k on the stiff (k^4) side, n_g = 4 to 1e-2, multipole/near-zone k a <= 1e-2, every point")
lin_line = "; ".join(f"{k_[0]} {k_[1]} {k_[2]}: {worst[k_]:.1e}" for k_ in worst if k_[3] == "C1_dominance_min")
check("P-LIN", lin_ok, f"min C1 dominance {lin_line}; mu_K correction mu_K^2 L*^2/2 <= {mu_corr:.1e}",
      "C1 dominates khronon charge transport (>= 1e3) at r = 2 pi/k_S and r = a; dropped mu_K term <= 1e-3")
wave_line = "; ".join(f"{k_[0]} {k_[1]} {k_[2]}: {worst[k_]:.1e}" for k_ in worst if k_[3] == "wave_ratio" and k_[1] == "mu_0.1")
check("P-WAVE", wave_ok, f"max delta(D.P)/background at r = 2 pi/k_S (sigma3): {wave_line}",
      "the radiated wave leaves D.P > 0 (switch on; linear) by >= 1e3")

# ---- verdict
req_D = ["D-HERM", "D-GR", "D-RES", "D-ON", "D-FORM", "ANG", "X-LIT", "D-LIM", "D-K4", "H-PM", "P-LIN", "P-WAVE"]
d_ok = all(c["pass"] for c in CHECKS if c["id"] in req_D)
full = {f_: {l_: win[f_][l_]["surviving_n"] == win[f_][l_]["grid_n"] > 0 for l_ in MUK} for f_ in FOOT}
nonempty = {f_: {l_: win[f_][l_]["surviving_n"] > 0 for l_ in MUK} for f_ in FOOT}
if not S0_OK:
    verdict = "UNDECIDED (step 0 failed)"
elif not d_ok:
    verdict = "UNDECIDED (a required step-1 check failed)"
elif all(full[f_][l_] for f_ in FOOT for l_ in MUK):
    verdict = "C1 PASSES BINARY PULSARS"
elif nonempty["canonical"]["mu_0.1"] != nonempty["alt"]["mu_0.1"]:
    verdict = "UNDECIDED (footings disagree)"
elif all(nonempty[f_]["mu_0.1"] for f_ in FOOT):
    verdict = "WINDOW NARROWED TO " + "; ".join(f"{f_} {l_} {win[f_][l_]['surviving_range']}" for f_ in FOOT for l_ in MUK)
elif not any(nonempty[f_][l_] for f_ in FOOT for l_ in MUK):
    verdict = "WINDOW CLOSED"
else:
    verdict = "UNDECIDED"
# the named condition: counterfactual sigmaX and the s_crit range
sx_fail = {}
for foot in FOOT:
    for lab in MUK:
        fails = [r_["beta"] for r_ in grid_res[foot][lab]
                 if any(r_["binaries"][nm][f"M{M:g}"]["delta_sigmaX"] > BIN[nm]["dplus"] for nm in BIN for M in M_BG)]
        by_bin = {nm: sum(1 for r_ in grid_res[foot][lab]
                          if any(r_["binaries"][nm][f"M{M:g}"]["delta_sigmaX"] > BIN[nm]["dplus"] for M in M_BG)) for nm in BIN}
        sx_fail[f"{foot} {lab}"] = {"n_fail": len(fails), "range": [min(fails), max(fails)] if fails else None,
                                    "n_fail_by_binary": by_bin}
scrit = {nm: [min(worst[(f_, l_, nm, "s_crit_min")] for f_ in FOOT for l_ in MUK)] for nm in BIN}
RES["verdict"] = verdict
RES["window_full"] = full
RES["sigmaX_counterfactual_failures"] = sx_fail
RES["s_crit_min_over_window"] = scrit
log(f"  VERDICT: {verdict}")
log(f"  condition: NS |s1 - s2| < s_crit (min over the window) {', '.join(f'{nm} {v_[0]:.2e}' for nm, v_ in scrit.items())}; "
    f"counterfactual sigmaX (s = 0.3 beta) fails at {sx_fail}")

# ===================================================================================================== PART R
log("")
log("PART R (reported only)")
rep = {}
# R1 GW170817: c_T = 1 (S0-3); scalar speed at 100 Hz
w100 = 2 * math.pi * 100
rep["R1"] = {"c_T_is_1": cT_ok, "c_S_100Hz_c": {f"{f_} {bl}": float(disp_k(np.array([w100]), bv / (2 + 3 * bv), LSTAR_PC[f_] * PC, 1.0)[1][0])
                                              for f_ in FOOT for bl, bv in (("beta_min", BETA_MIN[f_]), ("beta_max_0.03", BETA_MAX["mu_0.03"]))}}
# R2 causality: speeds; tilted-slice quartic (I1-type) for w = 369 km/s along k'
r2 = {}
wv = V_CMB / C_SI
gam = 1 / math.sqrt(1 - wv ** 2)
for f_ in FOOT:
    Ls = LSTAR_PC[f_] * PC
    for bl, bv in (("beta_min", BETA_MIN[f_]), ("beta_max_0.03", BETA_MAX["mu_0.03"])):
        B = bv / (2 + 3 * bv)
        A1m = B * Ls ** 2 / 2                                   # c = 1: omega = sqrt(A) k^2 [m^2]
        kap_I1 = 1 / (2 * math.sqrt(A1m) * wv)
        uc = None
        for u in np.geomspace(1e-3, 1e3, 601):
            kap = u * kap_I1
            wref = math.sqrt(A1m) * kap ** 2
            # gam^2 (wref x + w kap)^2 - A gam^4 (kap + w wref x)^4 = 0, divided by wref^2 (M = 1)
            p1 = np.poly1d([gam * 1.0, gam * wv * kap / wref]) ** 2
            p2 = np.poly1d([gam * wv * wref / kap, gam * 1.0]) ** 4
            poly = p1 - p2
            rts = np.roots(poly.coeffs)
            if np.max(abs(rts.imag)) > 1e-8 * max(1.0, np.max(abs(rts))):
                uc = u
                break
        r2[f"{f_} {bl}"] = {"kappa_I1_estimate_per_m": kap_I1, "kappa_c_numeric_per_m": (uc * kap_I1) if uc else None,
                            "u_c": uc}
rep["R2"] = {"tilted_slice": r2, "J0737_speeds_n2": {f"{f_} {bl}": {k_: score("J0737-3039A/B", bv, LSTAR_PC[f_] * PC, 1.0)[k_]
                                                                    for k_ in ("phase_speed_c", "group_speed_c", "k_S_n2", "eta_kS_n2",
                                                                               "lambda_S_n2_m", "n_g_n2")}
                                                     for f_ in FOOT for bl, bv in (("beta_min", BETA_MIN[f_]),
                                                                                   ("beta_max_0.1", BETA_MAX["mu_0.1"]),
                                                                                   ("beta_max_0.03", BETA_MAX["mu_0.03"]))}}
# R3 V_CM / c_S at the double pulsar (n = 2)
rep["R3"] = {k_: V_CMB / C_SI / v_["phase_speed_c"] for k_, v_ in rep["R2"]["J0737_speeds_n2"].items()}
# R4 scaling exponents at fixed omega (J0737 n = 2), M = 1: d ln coef / d ln beta and d ln L*


def coefs(bv, Ls, w):
    B = bv / (2 + 3 * bv)
    kS_, ch_, eta_, ng_ = disp_k(np.array([w]), B, Ls, 1.0)
    ch_, ng_ = ch_[0], ng_[0]
    return np.array([B / (30 * ng_ * ch_ ** 7), B / (4 * ng_ * ch_ ** 3) * (1 + 1 / (3 * ch_ ** 2)) ** 2,
                     1 / (3 * ng_ * B * ch_) * (1 + B / ch_ ** 2) ** 2])


w2 = 2 * HAR["J0737-3039A/B"]["Om"]
Lc = LSTAR_PC["canonical"] * PC
b0 = BETA_MIN["canonical"]
eb = np.log(coefs(b0 * 1.01, Lc, w2) / coefs(b0 / 1.01, Lc, w2)) / np.log(1.01 ** 2)
eL = np.log(coefs(b0, Lc * 1.01, w2) / coefs(b0, Lc / 1.01, w2)) / np.log(1.01 ** 2)
rep["R4"] = {"dln/dln_beta[quad, mono, dip]": eb, "dln/dln_Lstar[quad, mono, dip]": eL}
# R5 dipole frame factor (1 + B/c_S^2)^2 - 1 at J0737 (n = 1), beta edges
rep["R5"] = {}
for f_ in FOOT:
    for bl, bv in (("beta_min", BETA_MIN[f_]), ("beta_max_0.03", BETA_MAX["mu_0.03"])):
        B = bv / (2 + 3 * bv)
        ch1 = disp_k(np.array([HAR["J0737-3039A/B"]["Om"]]), B, LSTAR_PC[f_] * PC, 1.0)[1][0]
        rep["R5"][f"{f_} {bl}"] = (1 + B / ch1 ** 2) ** 2 - 1
# R6 absolute Pbdot shifts at the window edges (M = 1), sigma0 and sigma3
rep["R6"] = {}
for f_ in FOOT:
    for lab in MUK:
        for edge, rr in (("beta_min", grid_res[f_][lab][0]), ("beta_max", grid_res[f_][lab][-1])):
            for nm in BIN:
                sc_ = rr["binaries"][nm]["M1"]
                rep["R6"][f"{f_} {lab} {edge} {nm}"] = {"beta": rr["beta"], "delta_sigma0": sc_["delta_sigma0"],
                                                         "delta_sigma3": sc_["delta_sigma3"],
                                                         "dPbdot_sigma3_s_per_s": sc_["delta_sigma3"] * BIN[nm]["PbdotGR"],
                                                         "delta_over_1sigma_sigma3": sc_["delta_sigma3"] / BIN[nm]["sig"],
                                                         "s_crit": sc_["s_crit"], "s_sigma1": sc_["s"]["sigma1"],
                                                         "s_sigma3": sc_["s"]["sigma3"], "s_sigmaX": sc_["s"]["sigmaX"],
                                                         "delta_sigmaX": sc_["delta_sigmaX"]}
# R7 k^2 -> k^4 crossover for M = 100
rep["R7"] = {}
for f_ in FOOT:
    Ls = LSTAR_PC[f_] * PC
    kx = math.sqrt(2 * 99) / Ls
    for bl, bv in (("beta_min", BETA_MIN[f_]), ("beta_max_0.03", BETA_MAX["mu_0.03"])):
        B = bv / (2 + 3 * bv)
        rep["R7"][f"{f_} {bl}"] = {"k_x_per_m": kx, "omega_x_rad_s": math.sqrt(2 * B * 99) * C_SI * kx}
# R8 (A3, POST-RESULT reporting only): sensitivity of delta to the Galactic background M (1 vs 100), max over the grid
r8 = 0.0
for f_ in FOOT:
    for l_ in MUK:
        for rr in grid_res[f_][l_]:
            for nm in BIN:
                d1_, d100_ = rr["binaries"][nm]["M1"]["delta_sigma3"], rr["binaries"][nm]["M100"]["delta_sigma3"]
                r8 = max(r8, abs(d1_ / d100_ - 1))
rep["R8_max_rel_change_delta_sigma3_M1_vs_M100"] = r8
RES["reported"] = rep
log(f"  R8 max |delta(sigma3; M = 1)/delta(sigma3; M = 100) - 1| over the grid: {r8:.2e}")
log(f"  R1 c_T = 1: {cT_ok}; scalar speed at 100 Hz (units of c): {rep['R1']['c_S_100Hz_c']}")
log(f"  R2 double pulsar n = 2: {rep['R2']['J0737_speeds_n2']}")
log(f"  R2 tilted slice (w = 369 km/s): {r2}")
log(f"  R3 V_CM/c_S: {rep['R3']}")
log(f"  R4 exponents d ln coef/d ln beta [quad, mono, dip] {np.round(eb, 4)}, d ln/d ln L* {np.round(eL, 4)}")
log(f"  R5 (1 + B/c_S^2)^2 - 1: {rep['R5']}")
log(f"  R7 crossover (M = 100): {rep['R7']}")
for key_, v_ in rep["R6"].items():
    if " M" not in key_:
        log(f"  R6 {key_}: delta(sigma0) {v_['delta_sigma0']:.3e}, delta(sigma3) {v_['delta_sigma3']:.3e}, dPbdot "
            f"{v_['dPbdot_sigma3_s_per_s']:.3e} s/s, s_crit {v_['s_crit']:.3e}, s(sigma1) {v_['s_sigma1']:.2e}, "
            f"s(sigma3) {v_['s_sigma3']:.2e}; sigmaX s {v_['s_sigmaX']:.2e} -> delta {v_['delta_sigmaX']:.3e}")

# ===================================================================================================== verdict lines
log("")
log("VERDICT")
log(f"  {verdict}")
if MUTATE:
    must_fail = {"S0-1": "m1", "S0-2": "m2", "S0-3": "m3", "S0-4": "m4", "S0-5": "m4", "D-GR": "m5", "X-LIT": "m6", "H-PM": "m7"}
    failed = {c["id"] for c in CHECKS if not c["pass"]}
    RES["mutate_required_failures"] = {cid: (cid in failed) for cid in must_fail}
    log(f"  MUTATE: required failures {RES['mutate_required_failures']}; all failed checks {sorted(failed)}")
finish()
