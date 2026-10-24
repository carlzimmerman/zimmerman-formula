#!/usr/bin/env python3
"""X17_beta_sound_selector: is C1's sound speed c_A a selector with the right sign (isolated galaxies at the law, cluster
cores toward the measured excess, growth not worse)?  Frozen criteria: FROZEN_CRITERIA.md (committed alone with
ASSUMPTION_LEDGER.md, 348993ca40).

Part S0  reproductions (stop rule)                                  -> checks S0-1 .. S0-5
Part P   the mu-pincer scope test                                    -> check P0
Part C   step 1: c_A by environment                                  -> check C-ID
Part H   step 2: the static hold from the action; Delta A channels   -> checks H-COV, H-PN, H-RESP
Part G   step 3: linear growth with C1 vs X4                         -> checks G-CA0, G-DISP, G-LIM
Part V   step 4 (reported) and the verdict

Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x17_beta_sound_selector.py               (exit 0 iff all pass)
      PYTHONHASHSEED=0 X17_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 x17_beta_sound_selector.py  (m1..m7; exit 1)

kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. No dark-matter particle.
Not theory closed. No shear is recomputed; record numbers are read from committed JSON.
"""
import os
import sys

if os.environ.get("PYTHONHASHSEED") != "0":           # sympy's simplification order depends on the hash seed (X14 note)
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, PYTHONHASHSEED="0"))
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import hashlib
import json
import math
import resource
import shutil
import subprocess
import tempfile
import time

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from sympy.calculus.euler import euler_equations

MUTATE = os.environ.get("X17_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"x17_beta_sound_selector{TAG}.out")
JS = os.path.join(HERE, f"x17_beta_sound_selector_results{TAG}.json")
T0 = time.time()
_lines = []
CHECKS = []
RES = {"mutate": MUTATE, "checks": CHECKS, "criteria_commit": "348993ca40"}


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
    RES["peak_rss_gb_self"] = rss_gb()
    RES["peak_rss_gb_children"] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1e9
    req_fail = [c["id"] for c in CHECKS if c["required"] and not c["pass"]]
    RES["required_failures"] = req_fail
    log(f"checks {sum(c['pass'] for c in CHECKS)}/{len(CHECKS)} pass; required failures {req_fail}; "
        f"{RES['runtime_s']:.0f} s; peak RSS self {RES['peak_rss_gb_self']:.3f} GB, children "
        f"{RES['peak_rss_gb_children']:.3f} GB")
    with open(OUT, "w") as fh:
        fh.write("\n".join(_lines) + "\n")
    with open(JS, "w") as fh:
        json.dump(clean(RES), fh, indent=1)
    sys.exit((0 if not req_fail else 1) if exit_code is None else exit_code)


# ------------------------------------------------------------------------------------------- constants (RAW / FITTED)
G = 6.67430e-11
C_SI = 299792458.0
C_KMS = C_SI / 1e3
GM_SUN = 1.32712440018e20
M_SUN = GM_SUN / G
KPC = 3.0856775814913673e19
PC = KPC / 1e3
MPC = 1e3 * KPC
K_SI = 4 * math.pi * G
K_B = 1.380649e-23
M_P = 1.67262192369e-27
T_CMB = 2.7255
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}            # FITTED (kappa = 1/2)
LSTAR_PC = {"canonical": 21.682, "alt": 22.849}                 # FITTED (X3 D4 switched floor, via X14/X15)
H0_NAT = 67.2e3 / MPC                                           # native H0 lower end (X14/X15 beta_max, drag times)
MUK = {"mu_0.1": 0.1 / MPC, "mu_0.03": 0.03 / MPC}             # S4 edges [1/m], physical
W_KMS_X14 = [68.75, 74.8]                                       # X14 FT window speeds (copied)
R_FOLD_KPC = [11.0, 33.0, 73.0, 91.0, 156.0]                    # X14 fold radii (copied)
M_MW = 6e10                                                     # ILLUSTRATIVE (X8/X10/X14/X15)
GAL_MB = [1e9, 1e10, 6e10, 2e11]                                # ILLUSTRATIVE SPARC-like span (E2)
GAL_R_KPC = [10.0, 30.0, 100.0]
CL_R_MPC = [0.3, 0.5, 1.0]                                      # E3 radii
W_BULK = [369.0, 600.0, 1000.0]                                 # ILLUSTRATIVE (X15 list)
RH_MPC = [1.0, 10.0]                                            # ILLUSTRATIVE held-halo radius (X15)
FSTAR = {"central": 0.20, "lo": 0.10, "hi": 0.30}               # F1 default and variants (ADOPTED)
MASS_BRACKET = [0.5, 1.0, 2.0]
M_MEMBER = 6e10                                                 # ILLUSTRATIVE member mass for drag
LNLAM = math.log(100.0)                                         # X15 drag
P = {k_: os.path.join(ROOT, *v_) for k_, v_ in {
    "x15_py": ("rebuild_2026_10_22", "X15_c1_preferred_frame", "x15_c1_preferred_frame.py"),
    "x15_json": ("rebuild_2026_10_22", "X15_c1_preferred_frame", "x15_c1_preferred_frame_results.json"),
    "x14_json": ("rebuild_2026_10_22", "X14_caustic_completion", "x14_caustic_completion_results.json"),
    "x4_py": ("rebuild_2026_10_22", "X4_growth_native_cap", "x4_growth.py"),
    "x4_json": ("rebuild_2026_10_22", "X4_growth_native_cap", "x4_growth_results.json"),
    "x7_json": ("rebuild_2026_10_22", "X7_cluster_core_significance", "x7_analysis_results.json"),
    "x2_json": ("rebuild_2026_10_22", "X2_cluster_outskirts", "x2_cluster_outskirts_results.json"),
    "x13_json": ("rebuild_2026_10_22", "X13_source_size_test", "x13_analysis_results.json"),
    "f1_json": ("rebuild_2026_10_22", "F1_cluster_cores", "f1_cluster_cores_results.json"),
    "f3_json": ("rebuild_2026_10_22", "F3_growth_audit", "f3_growth_audit_results.json"),
    "pincer_md": ("qwen_claude_field_theory", "closure_2026", "condensate_pincer_2026", "CONDENSATE_MU_PINCER_VERDICT.md"),
    "pincer_py": ("qwen_claude_field_theory", "closure_2026", "condensate_pincer_2026", "condensate_mu_pincer_2026.py"),
}.items()}
SHA_FROZEN = {"x15_py": "2bf2810326a938da36f95419c95aeed6660f10bf01c2cd4e955ef80cc864f9e1",
              "x15_json": "dd864fc9bdf408b7c12cfb2a60ea7d45ec3c9eb363d581e00b58d658e67d8e5e",
              "x14_json": "5af0afb83a8725eebdd056f4d8490301e5db437a2e658499e532dd6d1de3f96a",
              "x4_py": "fe0ba2b70762d3d506d359d0e4c35b06d7235837d1598de4d6e8aba3d2000b11",
              "x4_json": "1e3cad6521263aa40bb6c013c733795be81575a49cf4226179c150cf36fd5499",
              "x7_json": "c8f33d85a4867bce4a544fcad091158016272586951686aeda3c92d6fdad7f84",
              "x2_json": "81a80fc099e98e305d6dbcafd2c98ef70ae9a233cdb6b4ca43bc05a8e34ddf9e",
              "x13_json": "cdbd737ec13309f5349e8fabf968b3cd06d47d33ce512ab1aa5bd03d8137a138",
              "f1_json": "76cbfeee7462ae224019af6254d276f8d23b0c2f5a881d63864803fac6e28925",
              "f3_json": "5e0df3b412ddcfebbe6b3eedcaad277dbae74a405c6b56c114539a7084fdf84c",
              "pincer_md": "def2c4f6bf9e2dcdba2e07b32833e60d2a77eed6d4452cdd065b96ef5421a7bc",
              "pincer_py": "0e7d1a9aba0d618b48b0262ff70396ed359cf3688a348c6c382fcb6d77b89765"}
SHA_NOW = {k_: sha256(v_) for k_, v_ in P.items()}
RES["input_sha256"] = {k_: {"sha256": SHA_NOW[k_], "matches_frozen": SHA_NOW[k_] == SHA_FROZEN[k_]} for k_ in P}

log("X17_beta_sound_selector" + ("  [MUTATE m1-m7]" if MUTATE else ""))
log("=" * 110)
log("input sha256 vs frozen: " + ", ".join(f"{k_} {'ok' if SHA_NOW[k_] == SHA_FROZEN[k_] else 'CHANGED'}" for k_ in P))


# ------------------------------------------------------------------------- X14 / X15 helpers (copied with provenance)
def aqual_point(r_m, a0v, GM):
    """X14 x14_caustic_completion.py L431-435 / X15 L151-155 (copied): spherical law field and phantom of a point mass."""
    gN = GM / r_m ** 2
    g = 0.5 * (gN + math.sqrt(gN * gN + 4 * a0v * gN))
    Krho = 2 * a0v * GM / (r_m * math.sqrt(GM * GM + 4 * a0v * GM * r_m * r_m))   # 4 pi G rho_phantom
    return g, g / a0v, Krho


def p1_of(Rv):
    """X15 L660-667 (copied): streaming exponent, smallest real root > 1 of R p(p-1)(p+2)(p-3) = (p-2)(p+1)."""
    if Rv == 0:
        return 2.0
    co = np.polynomial.polynomial.polyfromroots([0, 1, -2, 3]) * Rv
    co = co - np.array([-2.0, -1.0, 1.0, 0.0, 0.0])
    rts = np.roots(co[::-1])
    real = sorted(r_.real for r_ in rts if abs(r_.imag) < 1e-9 and r_.real > 1 + 1e-12)
    return real[0]


def law_slope(gN, a0v):
    """d g / d g_N of the a0-line (X15 L680)."""
    return 0.5 + (gN + 2 * a0v) / (2 * math.sqrt(gN * gN + 4 * a0v * gN))


def Bdim(b):
    return b / (2 + 3 * b)


def cA_perp(x, b):
    return math.sqrt(x * Bdim(b) * C_SI ** 2) / 1e3


def cA_par(x, b):
    return math.sqrt((2 * x + x * x) * Bdim(b) * C_SI ** 2) / 1e3


def cmp_json(a, b, path="", skip=("runtime_s", "peak_rss_gb")):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        ka, kb = set(a) - set(skip), set(b) - set(skip)
        if ka != kb:
            out.append((path, f"keys differ {sorted(ka ^ kb)[:5]}"))
        for kk in sorted(ka & kb):
            out += cmp_json(a[kk], b[kk], f"{path}/{kk}", skip)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, "length"))
        else:
            for i_, (u, v) in enumerate(zip(a, b)):
                out += cmp_json(u, v, f"{path}[{i_}]", skip)
    elif isinstance(a, bool) or isinstance(b, bool):
        if a != b:
            out.append((path, f"{a} != {b}"))
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if not (a == b or (math.isnan(a) and math.isnan(b)) or
                (math.isfinite(a) and math.isfinite(b) and abs(a - b) <= 1e-12 * max(abs(a), abs(b)))):
            out.append((path, f"{a} != {b}"))
    elif a != b:
        out.append((path, f"{str(a)[:60]} != {str(b)[:60]}"))
    return out


def count_leaves(o):
    if isinstance(o, dict):
        return sum(count_leaves(v) for v in o.values())
    if isinstance(o, list):
        return sum(count_leaves(v) for v in o)
    return 1


# ===================================================================================================== PART S0
log("")
log("PART S0: reproductions (stop rule)")

# ---- S0-1: X15's own script, as a patched copy in a temporary directory (HERE -> temp dir, ROOT -> repository)
src = open(P["x15_py"]).read()
old_here = 'HERE = os.path.dirname(os.path.abspath(__file__))'
old_root = 'ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))'
patch_ok = src.count(old_here) == 1 and src.count(old_root) == 1
tmpd = tempfile.mkdtemp(prefix="x17_x15copy_")
s01 = {"patch_ok": patch_ok}
try:
    patched = src.replace(old_here, f"HERE = {tmpd!r}").replace(old_root, f"ROOT = {ROOT!r}")
    cp = os.path.join(tmpd, "x15_copy.py")
    with open(cp, "w") as fh:
        fh.write(patched)
    env = dict(os.environ, PYTHONHASHSEED="0", OMP_NUM_THREADS="1")
    env.pop("X15_MUTATE", None)
    if MUTATE:
        env["X15_MUTATE"] = "1"                              # m3: X15's own MUTATE
    t1 = time.time()
    pr = subprocess.run([sys.executable, cp], capture_output=True, text=True, env=env, cwd=tmpd, timeout=900)
    s01["returncode"] = pr.returncode
    s01["seconds"] = time.time() - t1
    jn = os.path.join(tmpd, f"x15_c1_preferred_frame_results{'_MUTATE' if MUTATE else ''}.json")
    with open(jn) as fh:
        x15_copy = json.load(fh)
finally:
    shutil.rmtree(tmpd, ignore_errors=True)
with open(P["x15_json"]) as fh:
    X15 = json.load(fh)
diffs = cmp_json(x15_copy, X15)
n_pass15 = sum(1 for c in x15_copy["checks"] if c["pass"])
s01.update({"n_pass": n_pass15, "n_checks": len(x15_copy["checks"]), "n_leaves": count_leaves(X15),
            "n_diffs": len(diffs), "first_diffs": diffs[:5], "verdict_copy": x15_copy.get("verdict")})
RES["S0_1"] = s01
check("S0-1", SHA_NOW["x15_py"] == SHA_FROZEN["x15_py"] and SHA_NOW["x15_json"] == SHA_FROZEN["x15_json"] and patch_ok
      and s01["returncode"] == 0 and n_pass15 == 13 and len(x15_copy["checks"]) == 13 and not diffs,
      f"X15 copy exit {s01['returncode']}, {n_pass15}/{len(x15_copy['checks'])} PASS, verdict '{s01['verdict_copy']}', "
      f"{len(diffs)} differing leaves of {s01['n_leaves']} vs the committed JSON ({s01['seconds']:.0f} s)"
      + (f"; first {diffs[:2]}" if diffs else ""),
      "X15's own script (patched copy) reproduces its committed JSON: c_A values and the khronon dispersion included")

# ---- S0-2: window and c_A from formulas (X14 L574/L586-597, X15 L158-173 copied)
H0_use = 2 * H0_NAT if MUTATE else H0_NAT                    # m2: H0 doubled in the copied beta_max
GM_MW = M_MW * GM_SUN
beta_min, x_fold = {}, {}
for foot, a0v in FOOT.items():
    bm = []
    x_fold[foot] = []
    for r_k in R_FOLD_KPC:
        _, xv, _ = aqual_point(r_k * KPC, a0v, GM_MW)
        x_fold[foot].append(xv)
        for w_ in W_KMS_X14:
            ww = (w_ * 1e3) ** 2
            den = xv * C_SI ** 2 - 3 * ww
            bm.append(2 * ww / den if den > 0 else float("inf"))
    beta_min[foot] = max(bm)
beta_max = {lab: 2 * H0_use ** 2 / (C_SI ** 2 * mu_ ** 2 - 3 * H0_use ** 2) for lab, mu_ in MUK.items()}
BETAS = {foot: {"beta_min": beta_min[foot], "beta_max_0.1": beta_max["mu_0.1"], "beta_max_0.03": beta_max["mu_0.03"]}
         for foot in FOOT}
rel = []
for foot in FOOT:
    rel.append(abs(beta_min[foot] / X15["S0_2"]["beta_min"][foot] - 1))
    rel += [abs(a_ / b_ - 1) for a_, b_ in zip(x_fold[foot], X15["S0_2"]["x_fold"][foot])]
for lab in MUK:
    rel.append(abs(beta_max[lab] / X15["S0_2"]["beta_max"][lab] - 1))
cA_rel = []
for foot in FOOT:
    for bl, bv in BETAS[foot].items():
        mine = [cA_perp(xv, bv) for xv in x_fold[foot]]
        rec = X15["T3a_mach"][foot][bl]["c_A_km_s"]
        cA_rel += [abs(a_ / b_ - 1) for a_, b_ in zip(mine, rec)]
    _, x_cl, _ = aqual_point(300 * KPC, FOOT[foot], 1e14 * GM_SUN)
    for row in X15["T3c_cherenkov"][foot]["rows"]:
        bv = BETAS[foot][row["beta"]]
        cA_rel.append(abs(cA_perp(x_cl, bv) / row["c_A_cluster_km_s"] - 1))
RES["S0_2"] = {"beta": BETAS, "max_rel_window_xfold": max(rel), "max_rel_cA": max(cA_rel), "n_cA_compared": len(cA_rel)}
cA_fold_rng = {foot: {bl: [min(cA_perp(x_, bv) for x_ in x_fold[foot]), max(cA_perp(x_, bv) for x_ in x_fold[foot])]
                      for bl, bv in BETAS[foot].items()} for foot in FOOT}
RES["S0_2"]["c_A_fold_range_km_s"] = cA_fold_rng
check("S0-2", max(rel) < 1e-12 and max(cA_rel) < 1e-12,
      f"beta_min can {beta_min['canonical']:.6e} alt {beta_min['alt']:.6e}; beta_max(0.1) {beta_max['mu_0.1']:.6e} "
      f"(0.03) {beta_max['mu_0.03']:.6e}; max rel diff window/x_fold {max(rel):.1e}; c_A ({len(cA_rel)} values: fold radii "
      f"x 3 beta x 2 footings + cluster points) max rel diff {max(cA_rel):.1e}; c_A at beta_max(0.1) fold radii "
      f"{cA_fold_rng['canonical']['beta_max_0.1'][0]:.0f}-{cA_fold_rng['canonical']['beta_max_0.1'][1]:.0f} / "
      f"{cA_fold_rng['alt']['beta_max_0.1'][0]:.0f}-{cA_fold_rng['alt']['beta_max_0.1'][1]:.0f} km/s",
      "window and c_A = sqrt(x beta c^2/(2+3beta)) reproduce X15's JSON to 1e-12 (both footings)")

# ---- S0-3: X14's disp (copied with provenance, x14_caustic_completion.py L93-140), C1 transport term
k, om = sp.symbols("k omega", positive=True)
r0 = sp.Symbol("rho0", real=True)
th = sp.Symbol("theta", real=True)
ML, MT = sp.symbols("M_L M_T", positive=True)
Kc, gL, muK = sp.symbols("K gamma_L mu_K", positive=True)
Bc = sp.Symbol("B", positive=True)
W2 = sp.Symbol("W2")
Mth = sp.Symbol("M_theta", positive=True)
Lst = sp.Symbol("L", positive=True)
bet = sp.Symbol("beta", positive=True)


def chi(theta_val, mu2=None):
    m2 = muK ** 2 if mu2 is None else mu2
    return k ** 2 / (Kc * Mth + theta_val * gL * k ** 2) + m2 / Kc


def disp_system(theta_val, cont_extra=0, muK2=None, source=None, baryons=None):
    """X14's disp (X3 B1-S) equations; optional baryon source (H-RESP) or dynamical baryon fluid (G-DISP)."""
    dphi, dsig, dXi, drho = sp.symbols("dphi dsigma dXi drho")
    dP = sp.symbols("dP0:3")
    kh = sp.Matrix([0, 0, 1])
    Ph = sp.Matrix([sp.sin(th), 0, sp.cos(th)])
    Hm = Kc * (MT * sp.eye(3) + (ML - MT) * Ph * Ph.T)
    dPv = sp.Matrix(dP)
    mu2 = muK ** 2 if muK2 is None else muK2
    Peq = sp.I * k * kh * dXi - theta_val * gL * k ** 2 * kh * (kh.dot(dPv)) - Hm * dPv
    unknowns = [dphi, dsig, dXi, drho] + list(dP)
    pois_src = 0
    extra = []
    if source is not None:
        pois_src = source
    if baryons is not None:
        rb, drb, dvb = baryons
        pois_src = drb
        unknowns += [drb, dvb]
        extra = [-sp.I * om * drb + sp.I * rb * k * dvb, -sp.I * om * dvb + sp.I * k * dphi]
    eqs_ = [-k ** 2 * dphi - Kc * (drho + pois_src), drho - (sp.I * k * kh.dot(dPv) - mu2 * dXi / Kc),
            -sp.I * om * drho + (r0 + cont_extra) * k ** 2 * dsig, dXi - (dphi + sp.I * om * dsig)] + list(Peq) + extra
    return eqs_, unknowns


def disp(theta_val, cont_extra=0, muK2=None):
    eqs_, unk = disp_system(theta_val, cont_extra, muK2)
    Msys = sp.linear_eq_to_matrix(eqs_, unk)[0]
    det = sp.factor(sp.simplify(Msys.det()))
    sol_ = sp.solve(sp.Eq(det.subs(om, sp.sqrt(W2)), 0), W2)
    return sp.simplify(sol_[0]) if len(sol_) == 1 else None


def to_Mth(expr):
    e = sp.simplify(expr.subs(ML, 1 / ((1 / Mth - sp.sin(th) ** 2 / MT) / sp.cos(th) ** 2)))
    return sp.simplify(e)


t_s03 = time.time()
s03 = {}
ok03 = True
for tv in (1, 0):
    w2 = to_Mth(disp(tv, cont_extra=Bc * k ** 2 / Kc))
    rec = sp.simplify(w2 - (r0 + Bc * k ** 2 / Kc) * (k ** 2 / chi(tv) - Kc))
    x15root = bet * k ** 2 * (Mth - 1 + tv * Lst ** 2 * k ** 2 / 2) / (2 + 3 * bet)
    r15 = sp.simplify(w2.subs({r0: 0, muK: 0}).subs({Bc: bet / (2 + 3 * bet), gL: Kc * Lst ** 2 / 2}) - x15root)
    s03[f"Theta{tv}"] = {"omega2": str(w2), "minus_record_form": str(rec), "minus_X15_root": str(r15)}
    ok03 = ok03 and rec == 0 and r15 == 0
RES["S0_3"] = s03
check("S0-3", ok03, f"omega^2 - (rho + Bk^2/K)(k^2/chi - K) = {s03['Theta1']['minus_record_form']} (Theta 1), "
      f"{s03['Theta0']['minus_record_form']} (Theta 0); at rho = mu_K = 0 minus X15's root beta k^2(M - 1 + Theta "
      f"L^2k^2/2)/(2+3beta): {s03['Theta1']['minus_X15_root']}, {s03['Theta0']['minus_X15_root']} "
      f"({time.time() - t_s03:.1f} s)", "X14's dispersion with C1 rebuilt; equals X15's khronon root (residual 0)")

# ---- S0-4: record cluster numbers (read only)
X7 = json.load(open(P["x7_json"]))
X2 = json.load(open(P["x2_json"]))
X13 = json.load(open(P["x13_json"]))
F1 = json.load(open(P["f1_json"]))
CELLS = ["canonical|h0672", "canonical|h0686", "alt|h0672", "alt|h0686"]
A_terc = {}
for c_ in CELLS:
    a_ = list(X7["trend"][f"terciles|{c_}|MID|CAL"]["A"])
    s_ = list(X7["trend"][f"terciles|{c_}|MID|CAL"]["sig"])
    if MUTATE:
        a_, s_ = a_[::-1], s_[::-1]                           # m4: terciles read in reversed order
    A_terc[c_] = {"A": a_, "sig": s_}
PRINTED = {"canonical|h0672": [1.10, 1.85, 1.84], "canonical|h0686": [1.11, 1.92, 1.88],
           "alt|h0672": [1.00, 1.70, 1.69], "alt|h0686": [1.02, 1.76, 1.73]}
ok_x7 = all(round(A_terc[c_]["A"][i_], 2) == PRINTED[c_][i_] for c_ in CELLS for i_ in range(3))
ok_order = all(A_terc[c_]["A"][0] < min(A_terc[c_]["A"][1:]) for c_ in CELLS)
tm = X2["tercile_median_Mgas500"]
ok_x2 = (float(f"{tm['T1']:.2g}") == 3.3e12 and float(f"{tm['T2']:.3g}") == 1.17e13 and float(f"{tm['T3']:.3g}") == 2.92e13
         and tm["T2"] == X7["mass"]["M_med"])
zc = X13["Z_MID_corr"]
PRINT13 = {"canonical|h0672": (1.657, 4.77), "canonical|h0686": (1.703, 4.99), "alt|h0672": (1.520, 4.11),
           "alt|h0686": (1.562, 4.35)}
ok_x13 = all(round(zc[c_]["A"], 3) == PRINT13[c_][0] and round(zc[c_]["Z"], 2) == PRINT13[c_][1] for c_ in CELLS)
MG05 = F1["dust"]["canonical"]["median_Mgas_0p5"]
MG10 = F1["dust"]["canonical"]["median_Mgas_1p0"]
ok_f1 = MG05 == F1["dust"]["alt"]["median_Mgas_0p5"] and MG10 == F1["dust"]["alt"]["median_Mgas_1p0"] and MG10 > MG05 > 0
E_need = {foot: {T: min(A_terc[c_]["A"][i_] - 1 for c_ in CELLS if c_.startswith(foot)) for T, i_ in (("T2", 1), ("T3", 2))}
          for foot in FOOT}
RES["S0_4"] = {"A_MID_CAL_terciles": A_terc, "tercile_median_Mgas500": tm, "X13_corrected": {c_: zc[c_] for c_ in CELLS},
               "F1_median_Mgas_0p5": MG05, "F1_median_Mgas_1p0": MG10, "E_needed": E_need,
               "sha_ok": {k_: SHA_NOW[k_] == SHA_FROZEN[k_] for k_ in ("x7_json", "x2_json", "x13_json", "f1_json")}}
check("S0-4", ok_x7 and ok_order and ok_x2 and ok_x13 and ok_f1 and all(RES["S0_4"]["sha_ok"].values()),
      f"X7 tercile A_MID CAL " + "; ".join(f"{c_} " + "/".join(f"{v:.3f}" for v in A_terc[c_]["A"]) for c_ in CELLS)
      + f" (printed match {ok_x7}, T1 lowest {ok_order}); X2 MGAS500 medians {tm['T1']:.4g}/{tm['T2']:.5g}/{tm['T3']:.5g} "
      f"({ok_x2}); X13 corrected A/Z match {ok_x13}; F1 median M_gas(<0.5, <1.0 Mpc) {MG05:.4g}, {MG10:.4g} Msun",
      "record cluster numbers read from committed JSON equal the record's printed values (no shear recomputed)")

# ---- S0-5: X4's growth ODE (F3's solver as copied in x4_growth.py L68-91; background A via classy)
F3R = json.load(open(P["f3_json"]))
X4 = json.load(open(P["x4_json"]))


def make_E(Om, h, rad=True):
    Or = (4.18e-5 / h ** 2) if rad else 0.0
    OL = 1.0 - Om - Or
    return (lambda a: math.sqrt(Om * a ** -3 + Or * a ** -4 + OL)), Or


def growth_ratio_x4(kk, mu_h, Om, Ob, h, kernel="bsk2", a_i=1e-3, rad=True, mut_s1=False):
    """F3's two-fluid sub-horizon growth, verbatim from x4_growth.py (m5: kernel s = 1, X4's own MUTATE)."""
    Ek, Or = make_E(Om, h, rad); OK = Om - Ob; kk = np.asarray(kk, float); n = len(kk)
    def s_of(a, mu):
        if mu is None: return np.ones(n)
        if mut_s1: return np.ones(n)
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

pa = F3R["K2"]["A_c2b_refit"]["params"]
hA = pa["h"]
cA_ = Class()
cA_.set({"omega_b": pa["omega_b"], "omega_cdm": pa["omega_cdm"], "h": hA, "ln10^{10}A_s": pa["lnAs"], "n_s": pa["n_s"],
         "tau_reio": pa["tau"], "N_ur": 3.044, "T_cmb": 2.7255, "output": "mPk", "P_k_max_h/Mpc": 60.0, "z_max_pk": 4.0})
cA_.compute()
KS = np.geomspace(1e-4, 50.0, 1500)
PkA = np.array([cA_.pk_lin(k_ * hA, 0.0) for k_ in KS]) * hA ** 3
cA_.struct_cleanup()
OmA, ObA = (pa["omega_b"] + pa["omega_cdm"]) / hA ** 2, pa["omega_b"] / hA ** 2
OKA = OmA - ObA
W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
_trapz = getattr(np, "trapezoid", None) or np.trapz


def sig8(Pk, T=None):
    Pk = Pk if T is None else Pk * T ** 2
    return math.sqrt(_trapz(Pk * W8(KS * 8.0) ** 2 * KS ** 2, KS) / (2 * math.pi ** 2))


KT = np.geomspace(1e-3, 3.0, 36)


def sig8_from_T(T):
    Tf = np.interp(np.log(KS), np.log(KT), T, left=T[0], right=T[-1])
    return sig8(PkA, Tf) / sig8(PkA)


MU_H = {"mu_0.1": 0.1 / hA, "mu_0.03": 0.03 / hA}             # physical Mpc^-1 -> h/Mpc at h_A (X4 conversion)
s05 = {}
for lab, X4lab in (("mu_0.03", "0.03"), ("mu_0.1", "0.1")):
    for col, ai in (("bsk2_ai0.001", 1e-3), ("bsk2_ai0.0001", 1e-4)):
        Tx = growth_ratio_x4(KT, MU_H[lab], OmA, ObA, hA, "bsk2", ai, mut_s1=MUTATE)
        r_ = sig8_from_T(Tx)
        s05[f"{lab}|{col}"] = {"this": r_, "X4": X4["ode"][X4lab][col]["sigma8_ratio"]}
RES["S0_5"] = s05
check("S0-5", all(abs(v["this"] / v["X4"] - 1) <= 1e-4 for v in s05.values()),
      "; ".join(f"{k_} {v['this']:.6f} vs X4 {v['X4']:.6f}" for k_, v in s05.items()),
      "F3/X4's ODE copy reproduces X4's committed sigma8 ratios (each <= 1e-4 relative)")

S0_OK = all(c["pass"] for c in CHECKS if c["id"].startswith("S0-"))
RES["S0_all_pass"] = S0_OK
if not S0_OK and not MUTATE:
    log("STOP RULE: a step-0 reproduction failed; verdict UNDECIDED, nothing further is scored.")
    RES["verdict"] = "UNDECIDED (step 0 failed)"
    finish(1)

# ===================================================================================================== PART P
log("")
log("PART P: the mu-pincer scope test (P0)")
xs, rhob, rhow, mus = sp.symbols("x rho_bar rho_well mu", positive=True)
x0 = sp.Symbol("x_0", nonnegative=True)
if MUTATE:                                                     # m7: density-keyed polytrope in place of c_A^2
    cA2 = {"perp": Kc * rhob / mus ** 2, "par": Kc * rhob / mus ** 2}
    well = {lab: e.subs(rhob, rhow) for lab, e in cA2.items()}
    frw_at_well_density = {lab: e.subs(rhob, rhow) for lab, e in cA2.items()}
else:
    cA2 = {"perp": Bc * ((1 + x0) - 1), "par": Bc * ((1 + x0) ** 2 - 1)}     # B (M_theta - 1), x = |grad Xi|/a0
    well = {lab: e.subs(x0, xs) for lab, e in cA2.items()}                     # static well: x > 0
    frw_at_well_density = {lab: e.subs(x0, 0) for lab, e in cA2.items()}       # FRW: x = 0, any density
frw_zero = all(sp.simplify(e) == 0 and sp.diff(e, rhob) == 0 for e in frw_at_well_density.values())
well_pos = all(sp.simplify(e).is_positive for e in well.values())
recur = all(sp.simplify(frw_at_well_density[lab] - well[lab]) == 0 for lab in cA2)
inside = recur or not frw_zero
RES["P0"] = {"cA2": {k_: str(v) for k_, v in cA2.items()}, "FRW": {k_: str(v) for k_, v in frw_at_well_density.items()},
             "well": {k_: str(v) for k_, v in well.items()}, "FRW_identically_zero": frw_zero, "well_positive": well_pos,
             "background_revisits_well_state": recur, "inside_pincer_scope": inside,
             "statement": "pincer premise: c_s a function of the dust's local state, so a well's c_s recurs on the "
                          "background at z_match; C1's c_A^2 = B c^2 (M_theta - 1) is keyed to x = |grad Xi|/a0"}
check("P0", frw_zero and well_pos and not recur,
      f"FRW (x = 0): c_A^2 = {RES['P0']['FRW']} for every density; well: {RES['P0']['well']} (> 0: {well_pos}); "
      f"background re-visits the well's c_A: {recur} -> inside the pincer's scope: {inside}",
      "C1's c_A is outside the mu-pincer's premise (zero on FRW at every density, positive in every static well)")

# ===================================================================================================== PART C
log("")
log("PART C (step 1): c_A by environment, both footings")
gr_, gN_, a0s, rs_, Bs_ = sp.symbols("g g_N a_0 r B", positive=True)
gexpr = (gN_ + sp.sqrt(gN_ ** 2 + 4 * a0s * gN_)) / 2
cid_sym = sp.simplify((gexpr * rs_) / (Bs_ * gexpr / a0s) - a0s * rs_ / Bs_)
TAB = {"E1_background": {}, "E2_galaxies": {}, "E3_clusters": {}}
cid_num = []
r_beta = {foot: {bl: Bdim(bv) * C_SI ** 2 / FOOT[foot] / KPC for bl, bv in BETAS[foot].items()} for foot in FOOT}
RES["r_beta_kpc"] = r_beta
# E1: background
Ek_A, _ = make_E(OmA, hA, True)
H0_A = 100e3 * hA / MPC
cs_b = math.sqrt(5.0 / 3.0 * K_B * T_CMB * 1101 / (1.22 * M_P)) / 1e3
for foot in FOOT:
    Ls = LSTAR_PC[foot] * PC
    TAB["E1_background"][foot] = {}
    for bl, bv in BETAS[foot].items():
        Bc2 = Bdim(bv) * C_SI ** 2
        mu_lab = "mu_0.03" if bl == "beta_max_0.03" else "mu_0.1"
        rows = {}
        for zlab, zz in (("z0", 0.0), ("z1100", 1100.0)):
            a_ = 1 / (1 + zz)
            rows[zlab] = {"c_A_km_s": 0.0, "stiffness_only_speed_at_k_1perMpc_km_s": math.sqrt(Bc2 * Ls ** 2 / 2) / MPC / 1e3,
                          "IR_rate_over_H": math.sqrt(Bc2) * MUK[mu_lab] / (H0_A * Ek_A(a_)),
                          "IR_rate_over_H_native_H0_z0": math.sqrt(Bc2) * MUK[mu_lab] / H0_NAT if zz == 0 else None,
                          "compare_speed_km_s": 369.0 if zz == 0 else cs_b,
                          "compare_label": "bulk flow 369 km/s (ILLUSTRATIVE)" if zz == 0 else "baryon sound speed at z = 1100",
                          "Mach": "infinite (c_A = 0)"}
        TAB["E1_background"][foot][bl] = {"mu_K": mu_lab, **rows}
# E2: galaxies
for foot, a0v in FOOT.items():
    TAB["E2_galaxies"][foot] = {}
    for bl, bv in BETAS[foot].items():
        Bc2 = Bdim(bv) * C_SI ** 2
        rows = []
        for Mb in GAL_MB:
            for rk in GAL_R_KPC:
                rm = rk * KPC
                g, xv, Krho = aqual_point(rm, a0v, Mb * GM_SUN)
                vc = math.sqrt(g * rm) / 1e3
                cp, cl = cA_perp(xv, bv), cA_par(xv, bv)
                ceff = math.sqrt((Krho * rm ** 2 + Bc2) * xv) / 1e3
                cid_num.append(abs((vc / cp) ** 2 / (a0v * rm / Bc2) - 1))
                rows.append({"M_b": Mb, "r_kpc": rk, "x": xv, "v_c_km_s": vc, "c_A_perp_km_s": cp, "c_A_par_km_s": cl,
                             "c_eff_k1r_km_s": ceff, "Mach_internal_perp": vc / cp, "Mach_369_perp": 369.0 / cp})
        TAB["E2_galaxies"][foot][bl] = rows


# E3: clusters (terciles)
def mb_enclosed(T, r_mpc, fstar=FSTAR["central"], fac=1.0):
    p_ = math.log(MG10 / MG05) / math.log(2.0)
    mg_med = {0.3: MG05 * (0.3 / 0.5) ** p_, 0.5: MG05, 1.0: MG10}[r_mpc]
    return fac * (1 + fstar) * (tm[T] / tm["T2"]) * mg_med


TERC = ["T1", "T2", "T3"]
for foot, a0v in FOOT.items():
    TAB["E3_clusters"][foot] = {}
    for bl, bv in BETAS[foot].items():
        Bc2 = Bdim(bv) * C_SI ** 2
        rows = []
        for T in TERC:
            for rmp in CL_R_MPC:
                for fac in MASS_BRACKET:
                    rm = rmp * MPC
                    Mb = mb_enclosed(T, rmp, fac=fac)
                    g, xv, Krho = aqual_point(rm, a0v, Mb * GM_SUN)
                    vc = math.sqrt(g * rm) / 1e3
                    cp, cl = cA_perp(xv, bv), cA_par(xv, bv)
                    ceff = math.sqrt((Krho * rm ** 2 + Bc2) * xv) / 1e3
                    cid_num.append(abs((vc / cp) ** 2 / (a0v * rm / Bc2) - 1))
                    rows.append({"tercile": T, "r_Mpc": rmp, "mass_factor": fac, "M_b": Mb, "x": xv, "v_c_km_s": vc,
                                 "c_A_perp_km_s": cp, "c_A_par_km_s": cl, "c_eff_k1r_km_s": ceff,
                                 "Mach_internal_perp": vc / cp,
                                 "Mach_bulk_perp": {f"{w_:.0f}": w_ / cp for w_ in W_BULK}})
        TAB["E3_clusters"][foot][bl] = rows
RES["cA_table"] = TAB
check("C-ID", cid_sym == 0 and max(cid_num) < 1e-12,
      f"symbolic v_c^2/c_A,perp^2 - a0 r/B = {cid_sym}; numeric max rel {max(cid_num):.1e} over {len(cid_num)} points; "
      f"r_beta = B c^2/a0: " + "; ".join(f"{foot} " + ", ".join(f"{bl} {v:.1f} kpc" for bl, v in r_beta[foot].items())
                                          for foot in FOOT),
      "internal Mach v_c/c_A,perp = sqrt(r/r_beta) is mass-independent for the spherical law")
for foot in FOOT:
    for bl in BETAS[foot]:
        e1 = TAB["E1_background"][foot][bl]
        g2 = TAB["E2_galaxies"][foot][bl]
        c3 = [r_ for r_ in TAB["E3_clusters"][foot][bl] if r_["mass_factor"] == 1.0]
        log(f"  {foot} {bl}: FRW c_A = 0 (z 0, 1100); stiffness-only {e1['z0']['stiffness_only_speed_at_k_1perMpc_km_s']:.2e} "
            f"km/s at k = 1/Mpc; IR rate/H z0 {e1['z0']['IR_rate_over_H']:.3f}, z1100 {e1['z1100']['IR_rate_over_H']:.2e}; "
            f"galaxies 10-100 kpc c_A,perp {min(r_['c_A_perp_km_s'] for r_ in g2):.0f}-{max(r_['c_A_perp_km_s'] for r_ in g2):.0f}"
            f" (par {min(r_['c_A_par_km_s'] for r_ in g2):.0f}-{max(r_['c_A_par_km_s'] for r_ in g2):.0f}) vs v_c "
            f"{min(r_['v_c_km_s'] for r_ in g2):.0f}-{max(r_['v_c_km_s'] for r_ in g2):.0f}; cluster cores 0.3-1 Mpc c_A,perp "
            + ", ".join(f"{T} {min(r_['c_A_perp_km_s'] for r_ in c3 if r_['tercile'] == T):.0f}-"
                        f"{max(r_['c_A_perp_km_s'] for r_ in c3 if r_['tercile'] == T):.0f}" for T in TERC)
            + f" vs v_c {min(r_['v_c_km_s'] for r_ in c3):.0f}-{max(r_['v_c_km_s'] for r_ in c3):.0f} km/s")

# ===================================================================================================== PART H
log("")
log("PART H (step 2): the static hold from the action")
# ---- H-COV (a): K from tau for a static diagonal metric, tau = t
tt, X1, X2_, X3_ = sp.symbols("t x1 x2 x3", real=True)
crd = [tt, X1, X2_, X3_]
Nf = sp.Function("N")(X1, X2_, X3_)
hf = [sp.Function(f"h{i}")(X1, X2_, X3_) for i in (1, 2, 3)]
tauf = sp.Function("tau")(tt, X1, X2_, X3_)


def K_of(gdiag, tau_expr):
    ginv = [1 / gg for gg in gdiag]
    sqrtg = sp.sqrt(-gdiag[0] * gdiag[1] * gdiag[2] * gdiag[3])
    dtau = [sp.diff(tau_expr, c_) for c_ in crd]
    Xn = -sum(ginv[i] * dtau[i] ** 2 for i in range(4))
    n_up = [ginv[i] * (-dtau[i] / sp.sqrt(Xn)) for i in range(4)]
    return sum(sp.diff(sqrtg * n_up[i], crd[i]) for i in range(4)) / sqrtg


gstat = [-Nf ** 2] + hf
K_static = sp.simplify(K_of(gstat, tauf).subs(tauf, tt).doit())
h1t = sp.Function("h1t")(tt, X1, X2_, X3_)
K_nonstatic = sp.simplify(K_of([-Nf ** 2, h1t, hf[1], hf[2]], tauf).subs(tauf, tt).doit())
# ---- H-COV (b): ADM spherical ansatz; Euler-Lagrange of N sqrt(h) K^2 on static configurations
t_, r_ = sp.symbols("t r", real=True)
Na, Sa, Aa, Ba = [sp.Function(nm)(t_, r_) for nm in ("N", "S", "A", "Bf")]
sqh = Aa * Ba ** 2
Ktr = (sp.diff(sp.log(sqh), t_) - sp.diff(sqh * Sa, r_) / sqh) / Na
if MUTATE:                                                     # m1: acceleration squared a_i a^i in place of K^2
    L_op = Na * sqh * (sp.diff(Na, r_) / (Na * Aa)) ** 2
else:
    L_op = Na * sqh * Ktr ** 2
ELs = euler_equations(L_op, [Na, Sa, Aa, Ba], [t_, r_])
N0, A0, B0 = [sp.Function(nm)(r_) for nm in ("N0", "A0", "B0")]
el_static = [sp.simplify((e.lhs - e.rhs).subs({Sa: 0, Na: N0, Aa: A0, Ba: B0}).doit()) for e in ELs]
hcov_ok = K_static == 0 and all(e == 0 for e in el_static)
RES["H_COV"] = {"K_static_diag_metric_tau_t": str(K_static), "K_nonstatic_control": str(K_nonstatic),
                "EL_on_static": {nm: str(e) for nm, e in zip(("N", "S", "A", "Bf"), el_static)},
                "operator": "a_i a^i (MUTATE m1)" if MUTATE else "K^2"}
check("H-COV", hcov_ok and K_nonstatic != 0,
      f"(a) static metric, tau = t: K = {K_static} (non-static control K = {str(K_nonstatic)[:60]}...); (b) EL of "
      f"N sqrt(h) {'a_i a^i' if MUTATE else 'K^2'} w.r.t. N, S, A, Bf on S = 0, d_t = 0: {[str(e)[:40] for e in el_static]}",
      "C1 (K^2) contributes nothing to any field equation of a static held configuration, at all orders")
# ---- H-PN: X15's 3D PN Lagrangian L3 (copied, X15 L609-628)
X, Y, Z = sp.symbols("x y z", real=True)
T = sp.Symbol("t", real=True)
Bs, wx, wy, wz, Cst = sp.symbols("B w_x w_y w_z C", real=True)
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
      - Wf(sum(p_ ** 2 for p_ in Pv)) - Kc * Lst ** 2 / 4 * divv(Pv) ** 2 + mu2 * Xi3 ** 2 / (2 * Kc)
      - Bs / (2 * Kc) * lap(sig3) ** 2)
ELpn = euler_equations(L3, [phi3, sig3] + Pv, [T, X, Y, Z])
ex = [e.lhs - e.rhs for e in ELpn]
dB = [sp.simplify(sp.diff(e, Bs)) for e in ex]
b_sig = sp.simplify(dB[1] * Bs)
b_sig_ok = any(sp.simplify(b_sig - sg * Bs / Kc * lap(lap(sig3))) == 0 for sg in (1, -1))
held = {"static": -Cst * T, "boosted": -Cst * T - (wx * X + wy * Y + wz * Z)}
b_on = {nm: sp.simplify(b_sig.subs(sig3, s_e).doit()) for nm, s_e in held.items()}
hpn_ok = dB[0] == 0 and all(d_ == 0 for d_ in dB[2:]) and b_sig_ok and all(v == 0 for v in b_on.values())
RES["H_PN"] = {"dEL_dB": [str(d_) for d_ in dB], "B_part_sigma": str(b_sig), "B_part_on_held": {k_: str(v) for k_, v in b_on.items()}}
check("H-PN", hpn_ok, f"dEL/dB: phi {dB[0]}, P {dB[2:]}; sigma B-part = +/-(B/K) lap^2 sigma: {b_sig_ok}; on sigma = -Ct: "
      f"{b_on['static']}, on sigma = -Ct - w.x (boosted held): {b_on['boosted']}",
      "PN level: B enters only the sigma (charge) equation via (B/K) lap^2 sigma, which vanishes on held configurations")
# ---- H-RESP: moving-source linear response on a uniform held background (WKB)
drb = sp.Symbol("drho_b")
eqs_r, unk_r = disp_system(0, cont_extra=Bc * k ** 2 / Kc, muK2=0, source=drb)
A_r, b_r = sp.linear_eq_to_matrix(eqs_r, unk_r)
sol_r = A_r.LUsolve(b_r)
ratio = to_Mth(sp.cancel(sol_r[3] / drb))
expect = 1 / ((Mth - 1) - om ** 2 / (Kc * r0 + Bc * k ** 2))
resp_res = sp.simplify(ratio - expect)
mu_ = sp.Symbol("mu_c", positive=True)
half = sp.Rational(1, 2)
# A2 (POST-RESULT, check code only): RUN1 left 2 atanh(1/2) - ln 3 (identically 0) unsimplified; rewrite in logs first
avg_sub = sp.simplify((sp.integrate(1 / (1 - half ** 2 * mu_ ** 2), (mu_, 0, 1)) - sp.atanh(half) / half).rewrite(sp.log))
avg_num = [abs(float(sp.Integral(1 / (1 - sp.Float(mv) ** 2 * mu_ ** 2), (mu_, 0, 1)).evalf(30)) / (math.atanh(mv) / mv) - 1)
           for mv in (0.3, 0.9)]


def P_dir(M):
    """direction-averaged response factor (H-RESP): artanh(M)/M (M < 1); principal value ln((M+1)/(M-1))/(2M) (M > 1)."""
    if M < 1e-8:
        return 1.0
    if M < 1:
        return math.atanh(M) / M
    return math.log((M + 1) / (M - 1)) / (2 * M)


pv_chk = []
for Mv in (1.5, 3.0):
    pv = quad(lambda u: 1.0 / (1 + Mv * u), 0, 1, weight="cauchy", wvar=1.0 / Mv)[0]   # PV int_0^1 du/(1 - M^2 u^2)
    pv = -pv / Mv                                                                       # 1/(1-M^2u^2)=1/((1-Mu)(1+Mu))
    pv_chk.append(abs(pv / P_dir(Mv) - 1))
hresp_ok = resp_res == 0 and avg_sub == 0 and max(avg_num) < 1e-12 and max(pv_chk) < 1e-8
RES["H_RESP"] = {"drho_tau_over_drho_b": str(ratio), "expected": str(expect), "residual": str(resp_res),
                 "avg_check_at_half": str(avg_sub), "avg_rel_err_at_0.3_0.9": avg_num, "PV_supersonic_rel_err": pv_chk}
check("H-RESP", hresp_ok, f"drho_tau/drho_b = {ratio}; minus 1/((M_theta - 1) - omega^2/(K rho + B k^2)) = {resp_res}; "
      f"direction average artanh(Ma)/Ma (check at Ma = 1/2: {avg_sub}); supersonic principal value rel err {max(pv_chk):.1e}",
      "moving-source response on a uniform held background derived (w -> 0: static sub-phantom 1/(M_theta - 1))")

# ---- numbers: Delta A channels per footing, beta, tercile (mass factor 1 graded; bracket reported)


def maxwell_avg(c, sigma):
    pdf = lambda w: math.sqrt(2 / math.pi) * w * w / sigma ** 3 * math.exp(-w * w / (2 * sigma * sigma))
    f = lambda w: P_dir(w / c) * pdf(w)
    top = c + 14 * sigma
    if c < top:
        I1 = quad(f, 0, c, limit=400)[0]
        I2 = quad(f, c, top, limit=400)[0]
    else:
        I1, I2 = quad(f, 0, top, limit=400)[0], 0.0
    norm = quad(pdf, 0, top, limit=400)[0]
    return (I1 + I2) / norm


DA = {}
for foot, a0v in FOOT.items():
    DA[foot] = {}
    for bl, bv in BETAS[foot].items():
        Bc2 = Bdim(bv) * C_SI ** 2
        cells = []
        for T_ in TERC:
            for rmp in CL_R_MPC:
                for fac in MASS_BRACKET:
                    rm = rmp * MPC
                    Mb = mb_enclosed(T_, rmp, fac=fac)
                    g, xv, Krho = aqual_point(rm, a0v, Mb * GM_SUN)
                    gN = Mb * GM_SUN / rm ** 2
                    vc = math.sqrt(g * rm)
                    cp, cl = cA_perp(xv, bv) * 1e3, cA_par(xv, bv) * 1e3
                    lawp = law_slope(gN, a0v)
                    Rv = Bc2 / (Krho * rm ** 2)
                    p1 = p1_of(Rv)
                    bulk = []
                    for w_ in W_BULK:
                        for RH in RH_MPC:
                            sup = w_ * 1e3 > cp
                            dlng = None if sup else ((lawp - 1) * (p1 - 1) * (p1 ** 2 + 2) / 3 * (w_ * 1e3) ** 2 / vc ** 2
                                                     * (rm / (RH * MPC)) ** (2 * (p1 - 1)))
                            bulk.append({"w_km_s": w_, "R_h_Mpc": RH, "supersonic": sup,
                                         "dA": None if sup else math.expm1(dlng)})
                    mem = {}
                    avgs = {"c_perp": maxwell_avg(cp, vc / math.sqrt(2)), "c_par": maxwell_avg(cl, vc / math.sqrt(2))}
                    for fl, fs in FSTAR.items():
                        for ml, mval in (("m_perp", xv), ("m_par", 2 * xv + xv * xv)):
                            for cl_lab, avg in avgs.items():
                                mem[f"{fl}|{ml}|{cl_lab}"] = {"avgP": avg,
                                                             "dA": fs / (1 + fs) / mval * (avg - 1) * gN / g}
                    dragrow = None
                    if vc > cp:
                        a_drag = 4 * math.pi * G * M_MEMBER * GM_SUN * (Krho / K_SI) * LNLAM / vc ** 2
                        dragrow = (vc / a_drag) * H0_NAT
                    cells.append({"tercile": T_, "r_Mpc": rmp, "mass_factor": fac, "x": xv, "v_c_km_s": vc / 1e3,
                                  "c_A_perp_km_s": cp / 1e3, "R": Rv, "p1": p1, "dg_dgN": lawp, "bulk": bulk,
                                  "members": mem, "t_drag_member_over_tH": dragrow})
        DA[foot][bl] = cells
RES["DeltaA_cells"] = DA


def summarize(foot, bl, fac=1.0, memkey="central|m_perp|c_perp", with_members=True):
    out = {}
    for T_ in TERC:
        cs = [c_ for c_ in DA[foot][bl] if c_["tercile"] == T_ and c_["mass_factor"] == fac]
        plus, minus, n_sup, n_bulk = [], [], 0, 0
        for c_ in cs:
            bvals = [b_["dA"] for b_ in c_["bulk"] if b_["dA"] is not None]
            n_sup += sum(1 for b_ in c_["bulk"] if b_["supersonic"])
            n_bulk += len(c_["bulk"])
            dm = c_["members"][memkey]["dA"] if with_members else 0.0
            plus.append(0.0 + max(max(bvals, default=0.0), 0.0) + max(dm, 0.0))
            minus.append(0.0 + min(min(bvals, default=0.0), 0.0) + min(dm, 0.0))
        bulk_all = [b_["dA"] for c_ in cs for b_ in c_["bulk"] if b_["dA"] is not None]
        mem_all = [c_["members"][memkey]["dA"] for c_ in cs]
        out[T_] = {"dA_plus": max(plus), "dA_minus": min(minus), "bulk_max": max(bulk_all, default=None),
                   "bulk_min": min(bulk_all, default=None), "mem_max": max(mem_all), "mem_min": min(mem_all),
                   "n_bulk_supersonic": n_sup, "n_bulk": n_bulk}
    return out


SUMM = {foot: {bl: summarize(foot, bl) for bl in BETAS[foot]} for foot in FOOT}
SUMM_BR = {}
for foot in FOOT:
    SUMM_BR[foot] = {}
    for bl in BETAS[foot]:
        vals_p, vals_m = [], []
        for fac in MASS_BRACKET:
            for mk in DA[foot][bl][0]["members"]:
                s_ = summarize(foot, bl, fac, mk)
                vals_p.append(max(v["dA_plus"] for v in s_.values()))
                vals_m.append(min(v["dA_minus"] for v in s_.values()))
        SUMM_BR[foot][bl] = {"dA_plus_max_bracket": max(vals_p), "dA_minus_min_bracket": min(vals_m)}
RES["DeltaA_summary"] = SUMM
RES["DeltaA_bracket"] = SUMM_BR
for foot in FOOT:
    for bl in BETAS[foot]:
        s_ = SUMM[foot][bl]
        log(f"  {foot} {bl}: " + "; ".join(
            f"{T_} dA+ {s_[T_]['dA_plus']:+.4f} dA- {s_[T_]['dA_minus']:+.4f} (bulk "
            + (f"{s_[T_]['bulk_min']:+.4f}..{s_[T_]['bulk_max']:+.4f}" if s_[T_]['bulk_max'] is not None else "n/a")
            + f", {s_[T_]['n_bulk_supersonic']}/{s_[T_]['n_bulk']} supersonic; members {s_[T_]['mem_min']:+.4f}.."
              f"{s_[T_]['mem_max']:+.4f})" for T_ in TERC)
            + f"; bracket dA+ {SUMM_BR[foot][bl]['dA_plus_max_bracket']:+.4f} dA- {SUMM_BR[foot][bl]['dA_minus_min_bracket']:+.4f}")
DRAG = {foot: {bl: {T_: [c_["t_drag_member_over_tH"] for c_ in DA[foot][bl] if c_["tercile"] == T_ and
                         c_["mass_factor"] == 1.0 and c_["r_Mpc"] == 0.5][0] for T_ in TERC} for bl in BETAS[foot]}
        for foot in FOOT}
RES["drag_member_0p5Mpc_over_tH"] = DRAG
log("  member drag t/t_H at 0.5 Mpc (only where v_c > c_A): " + "; ".join(
    f"{foot} {bl} " + "/".join("sub" if v is None else f"{v:.2f}" for v in DRAG[foot][bl].values())
    for foot in FOOT for bl in BETAS[foot]))

# ===================================================================================================== PART G
log("")
log("PART G (step 3): linear growth with C1 on FRW (x = 0)")
# ---- G-CA0: no k^2 (sound-speed) term on FRW
w2_frw = sp.simplify((r0 + Bc * k ** 2 / Kc) * (k ** 2 / chi(0, mu2=0).subs(Mth, 1) - Kc))
w2_frw_stiff = sp.simplify((r0 + Bc * k ** 2 / Kc) * (k ** 2 / chi(1, mu2=0).subs(Mth, 1) - Kc))
w2_frw_mu = sp.simplify((r0 + Bc * k ** 2 / Kc) * (k ** 2 / chi(0).subs(Mth, 1) - Kc))
check("G-CA0", w2_frw == 0, f"omega^2 on FRW (M_theta = 1, mu_K = 0, Theta = 0) = {w2_frw}; with stiffness Theta = 1: "
      f"{w2_frw_stiff}; with mu_K: {w2_frw_mu} (tachyonic, X14's IR band)",
      "c_A = 0 on FRW at linear order: C1 cannot Jeans-suppress the background khronon")
RES["G_CA0"] = {"omega2_frw": str(w2_frw), "omega2_frw_stiff": str(w2_frw_stiff), "omega2_frw_muK": str(w2_frw_mu)}
# ---- G-DISP: X14's disp + a dynamical baryon fluid at x = 0 (M_L = M_T = 1), finite mu_K
rb, dvb_, drb_ = sp.symbols("rho_b dv_b drho_bdyn")
lam = sp.Symbol("lambda")
eqs_g, unk_g = disp_system(0, cont_extra=Bc * k ** 2 / Kc, baryons=(rb, drb_, dvb_))
Mg = sp.linear_eq_to_matrix([e.subs({ML: 1, MT: 1}) for e in eqs_g], unk_g)[0]
detg = sp.expand(Mg.det(method="berkowitz"))
poly_l = sp.expand(detg.subs(om, sp.sqrt(-lam)))
s_sym = muK ** 2 / (k ** 2 + muK ** 2)
Tsym = Kc * rb + (Kc * r0 + Bc * k ** 2) * s_sym
Dsym = -Kc * rb * (Kc * r0 + Bc * k ** 2) * (1 - s_sym)
target = lam ** 2 - Tsym * lam + Dsym
quo = sp.cancel(poly_l / sp.expand(target * (k ** 2 + muK ** 2)))
gdisp_sym_ok = quo.free_symbols.isdisjoint({lam, om})
RES["G_DISP_symbolic"] = {"det_polynomial_in_lambda": str(poly_l), "target": str(target), "quotient": str(quo)}


def khr_drive(a, kk, beta):
    """C1 transport factor F = 1 + B k_p^2/(K rho_tau) = 1 + f1 a and dlnF/dlna (m6: F -> 1/F)."""
    f1 = Bdim(beta) * (C_KMS * np.asarray(kk, float) / 100.0) ** 2 / (1.5 * OKA)
    F = 1.0 + f1 * a
    dlnF = f1 * a / F
    if MUTATE:
        return 1.0 / F, -dlnF
    return F, dlnF


def growth_C1(kk, mu_h, beta, a_i=1e-3, a_out=(0.25, 1.0)):
    """F3/X4's ODE (as growth_ratio_x4) with C1: khronon drive x F, friction (2 + dlnE - dlnF). Returns delta_m(k, a_out)."""
    Ek, _ = make_E(OmA, hA, True)
    kk = np.asarray(kk, float)
    n = len(kk)
    Ob, OK = ObA, OKA

    def s_of(a):
        if mu_h is None:
            return np.ones(n)
        x2 = (kk / (a * mu_h)) ** 2
        return 1.0 / (1.0 + x2)

    def rhs(x, st):
        a = math.exp(x); E = Ek(a); eps = 1e-6
        dlnE = (math.log(Ek(a * math.exp(eps))) - math.log(Ek(a * math.exp(-eps)))) / (2 * eps)
        dens = 1.5 * a ** -3 / E ** 2
        db, gb, dk, gk = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
        if beta == 0:
            F, dlnF = 1.0, 0.0
        else:
            F, dlnF = khr_drive(a, kk, beta)
        src_b = dens * (Ob * db + OK * dk); src_k = F * dens * (Ob * db + OK * dk * s_of(a))
        return np.concatenate([gb, -(2 + dlnE) * gb + src_b, gk, -(2 + dlnE - dlnF) * gk + src_k])
    st0 = np.concatenate([np.full(n, a_i)] * 4)
    sol = solve_ivp(rhs, [math.log(a_i), 0.0], st0, method="DOP853", rtol=1e-7, atol=1e-12,
                    t_eval=[math.log(a_) for a_ in a_out])
    return {a_: (Ob * sol.y[:n, j] + OK * sol.y[2 * n:3 * n, j]) / OmA for j, a_ in enumerate(a_out)}


# numeric G-DISP: the ODE's frozen-time source matrix vs the symbolic roots
gd = []
for (a_t, kk_t, lab, bkey) in ((0.01, 1.0, "mu_0.1", "beta_max_0.1"), (0.5, 0.3, "mu_0.03", "beta_max_0.03"),
                               (1.0, 3.0, "mu_0.1", "beta_min")):
    bv = BETAS["canonical"][bkey]
    Ek, _ = make_E(OmA, hA, True)
    dens = 1.5 * a_t ** -3 / Ek(a_t) ** 2
    s_v = 1.0 / (1.0 + (kk_t / (a_t * MU_H[lab])) ** 2)
    F_v, _ = khr_drive(a_t, [kk_t], bv)
    F_v = float(np.asarray(F_v).ravel()[0])
    Mode = dens * np.array([[ObA, OKA], [F_v * ObA, F_v * OKA * s_v]])
    ev = np.sort(np.linalg.eigvals(Mode).real)
    Kb, Kt = dens * ObA, dens * OKA                             # K rho / H^2
    Bk2 = Bdim(bv) * (C_KMS * kk_t / 100.0) ** 2 / a_t ** 2 / Ek(a_t) ** 2   # B k_p^2 / H^2
    num = {rb: Kb, r0: Kt, Kc: 1.0, Bc: Bk2, k: 1.0, muK: math.sqrt(s_v / (1 - s_v))}
    Tn, Dn = float(Tsym.subs(num)), float(Dsym.subs(num))
    roots = np.sort(np.array([(Tn + math.sqrt(Tn * Tn - 4 * Dn)) / 2, (Tn - math.sqrt(Tn * Tn - 4 * Dn)) / 2]))
    gd.append({"a": a_t, "k_hMpc": kk_t, "beta": bkey, "ode_eig": ev.tolist(), "sym_roots": roots.tolist(),
               "rel": float(max(abs(ev - roots) / np.abs(roots)))})
RES["G_DISP_numeric"] = gd
check("G-DISP", gdisp_sym_ok and max(g_["rel"] for g_ in gd) < 1e-10,
      f"det (baryons + khronon, x = 0) / [(lambda^2 - T lambda + D)(k^2 + mu^2)] = {quo}; ODE source-matrix eigenvalues vs "
      f"roots at 3 points: max rel {max(g_['rel'] for g_ in gd):.1e}",
      "coupled baryon-khronon dispersion with C1 on FRW: lambda^2 - T lambda + D, T = K rho_b + (K rho_tau + B k^2)s, "
      "D = -K rho_b (K rho_tau + B k^2)(1 - s); the ODE carries exactly these coefficients")
# ---- G-LIM and growth numbers
glim = []
for lab in MU_H:
    Tx = growth_ratio_x4(KT, MU_H[lab], OmA, ObA, hA, "bsk2", 1e-3)
    g0 = growth_C1(KT, MU_H[lab], 0.0, 1e-3, a_out=(1.0,))[1.0] / growth_C1(KT, None, 0.0, 1e-3, a_out=(1.0,))[1.0]
    glim.append(float(np.max(np.abs(g0 / Tx - 1))))
check("G-LIM", max(glim) <= 1e-10, f"C1 ODE at beta = 0 vs X4's ODE copy: max rel {max(glim):.1e}",
      "at beta = 0 the C1 growth ODE is X4's ODE exactly")
K_REP = np.array([0.1, 0.3, 1.0, 3.0, 10.0])
GROW = {}
for foot in FOOT:
    GROW[foot] = {}
    for lab in MU_H:
        bset = (("beta_min", BETAS[foot]["beta_min"]),
                ("beta_max_0.1" if lab == "mu_0.1" else "beta_max_0.03", BETAS[foot]["beta_max_0.1" if lab == "mu_0.1" else "beta_max_0.03"]))
        GROW[foot][lab] = {}
        for ai in (1e-3, 1e-4):
            dust_T = growth_C1(KT, None, 0.0, ai, a_out=(1.0,))[1.0]
            R0 = sig8_from_T(growth_C1(KT, MU_H[lab], 0.0, ai, a_out=(1.0,))[1.0] / dust_T)
            dust_rep = growth_C1(K_REP, None, 0.0, ai)
            for bl, bv in bset:
                gT = growth_C1(KT, MU_H[lab], bv, ai, a_out=(1.0,))[1.0]
                Rb = sig8_from_T(gT / dust_T)
                rep = growth_C1(K_REP, MU_H[lab], bv, ai)
                rep0 = growth_C1(K_REP, MU_H[lab], 0.0, ai)
                T2 = {zl: ((rep[a_] / dust_rep[a_]) ** 2).tolist() for zl, a_ in (("z0", 1.0), ("z3", 0.25))}
                T2_0 = {zl: ((rep0[a_] / dust_rep[a_]) ** 2).tolist() for zl, a_ in (("z0", 1.0), ("z3", 0.25))}
                maxT2 = max(max(v) for v in T2.values())
                ratio_R = Rb / R0
                if maxT2 > 2:
                    cls = "WORSE (overshoot)"
                elif ratio_R <= 0.95:
                    cls = "WORSE (suppressed)"
                elif ratio_R >= 1.05:
                    cls = "BETTER"
                else:
                    cls = "UNCHANGED"
                GROW[foot][lab][f"{bl}|ai{ai:g}"] = {"beta": bv, "R_beta": Rb, "R_0": R0, "R_ratio": ratio_R,
                                                    "T2": T2, "T2_beta0": T2_0, "max_T2": maxT2, "class": cls,
                                                    "k_hMpc": K_REP.tolist()}
RES["growth"] = GROW


def coupled_rate(a, kk, beta, mu_h):
    Ek, _ = make_E(OmA, hA, True)
    dens = 1.5 * a ** -3
    s_v = 1.0 / (1.0 + (kk / (a * mu_h)) ** 2)
    Bk2 = Bdim(beta) * (C_KMS * kk / 100.0) ** 2 / a ** 2
    Tn = dens * ObA + (dens * OKA + Bk2) * s_v
    Dn = -dens * ObA * (dens * OKA + Bk2) * (1 - s_v)
    lp = (Tn + math.sqrt(Tn * Tn - 4 * Dn)) / 2
    return math.sqrt(lp) / Ek(a)


RATES = {}
for lab in MU_H:
    bkey = "beta_max_0.1" if lab == "mu_0.1" else "beta_max_0.03"
    RATES[lab] = {f"{zl}|k{kk:g}": {"beta0": coupled_rate(a_, kk, 0.0, MU_H[lab]),
                                     bkey: coupled_rate(a_, kk, BETAS["canonical"][bkey], MU_H[lab])}
                  for zl, a_ in (("z1100", 1 / 1101), ("z0", 1.0)) for kk in (1.0, 10.0)}
RES["coupled_growth_rate_over_H"] = RATES
for foot in FOOT:
    for lab in MU_H:
        for key, v in GROW[foot][lab].items():
            if key.endswith("ai0.001"):
                log(f"  {foot} {lab} {key}: R {v['R_beta']:.5f} vs R(0) {v['R_0']:.5f} (x{v['R_ratio']:.3f}); T^2 z0 "
                    + "/".join(f"{t_:.3g}" for t_ in v["T2"]["z0"]) + " z3 " + "/".join(f"{t_:.3g}" for t_ in v["T2"]["z3"])
                    + f" at k {K_REP.tolist()} h/Mpc -> {v['class']}")
log("  coupled growth rate sqrt(lambda+)/H (canonical beta_max): " + "; ".join(
    f"{lab} {kz}: " + ", ".join(f"{bk} {vv:.3g}" for bk, vv in v.items()) for lab in RATES for kz, v in RATES[lab].items()))

# ===================================================================================================== PART V
log("")
log("PART V: step 4 (reported) and the verdict")
REQ = ("P0", "C-ID", "H-COV", "H-PN", "H-RESP", "G-LIM", "G-CA0", "G-DISP")
req_ok = all(c["pass"] for c in CHECKS if c["id"] in REQ)
gal_moving = {}
for foot in FOOT:
    gal_moving[foot] = {}
    for bl in BETAS[foot]:
        rows = [r_ for r_ in X15["T3b_rotation"][foot] if r_["beta"] == bl and not r_["supersonic"]]
        gal_moving[foot][bl] = max((r_["dlog10g"] for r_ in rows), default=float("nan"))
static_zero = all(c["pass"] for c in CHECKS if c["id"] in ("H-COV", "H-PN"))
RES["isolated_galaxy_change_dex"] = {"static": 0.0 if static_zero else None, "moving_subsonic_max_X15": gal_moving}
def foot_class(S, foot):
    """FROZEN_CRITERIA section 8, rules 3-7, for one footing; returns the class and the triggers that set it."""
    right, triggers = [], []
    for bl in BETAS[foot]:
        mu_lab = "mu_0.03" if bl == "beta_max_0.03" else "mu_0.1"
        gcls = GROW[foot][mu_lab][f"{bl}|ai0.001"]["class"]
        s_ = S[bl]
        sel = (s_["T2"]["dA_plus"] >= 0.25 * E_need[foot]["T2"] and s_["T3"]["dA_plus"] >= 0.25 * E_need[foot]["T3"]
               and s_["T1"]["dA_plus"] <= 0.5 * min(s_["T2"]["dA_plus"], s_["T3"]["dA_plus"])
               and gal_moving[foot][bl] <= 0.05 and static_zero)
        bulk_na = all(s_[T_]["n_bulk_supersonic"] == s_[T_]["n_bulk"] for T_ in ("T2", "T3"))
        if sel and not bulk_na:
            right.append((bl, gcls))
        for T_ in ("T2", "T3"):
            if s_[T_]["dA_minus"] <= -0.10:
                triggers.append(f"{bl}: {T_} dA- {s_[T_]['dA_minus']:+.4f} <= -0.10")
        if s_["T1"]["dA_plus"] >= 0.10 and s_["T1"]["dA_plus"] > max(s_["T2"]["dA_plus"], s_["T3"]["dA_plus"]):
            triggers.append(f"{bl}: T1 dA+ {s_['T1']['dA_plus']:+.4f} >= 0.10 and > T2 {s_['T2']['dA_plus']:+.4f}, "
                            f"T3 {s_['T3']['dA_plus']:+.4f} (inverted ordering)")
    inert = static_zero and all(abs(S[bl][T_][kk_]) < 0.10 for bl in BETAS[foot] for T_ in TERC
                                for kk_ in ("dA_plus", "dA_minus"))
    if right:
        v = ("RIGHT-SIGN SELECTOR" if any(not g_.startswith("WORSE") for _, g_ in right) else "SELECTOR BUT GROWTH WORSE")
    elif triggers:
        v = "WRONG SIGN"
    elif inert:
        v = "INERT"
    else:
        v = "UNDECIDED"
    return v, triggers, right


foot_verdict, foot_triggers = {}, {}
for foot in FOOT:
    foot_verdict[foot], foot_triggers[foot], _ = foot_class(SUMM[foot], foot)
RES["verdict_triggers"] = foot_triggers
bulk_na_all = {foot: {bl: [T_ for T_ in ("T2", "T3") if SUMM[foot][bl][T_]["n_bulk_supersonic"] == SUMM[foot][bl][T_]["n_bulk"]]
                      for bl in BETAS[foot]} for foot in FOOT}
if not S0_OK:
    verdict = "UNDECIDED (step 0 failed)"
elif not req_ok and not (RES["P0"]["inside_pincer_scope"] and all(c["pass"] for c in CHECKS if c["id"] in REQ and c["id"] != "P0")):
    verdict = "UNDECIDED (a required check failed)"
elif RES["P0"]["inside_pincer_scope"]:
    verdict = "EXCLUDED BY THE PINCER"
elif foot_verdict["canonical"] != foot_verdict["alt"]:
    verdict = "UNDECIDED (footings disagree)"
else:
    verdict = foot_verdict["canonical"]
RES["verdict"] = verdict
RES["verdict_per_footing"] = foot_verdict
RES["bulk_channel_all_supersonic"] = bulk_na_all
# step 4 (reported): ordering and S4 onset
order = {foot: {bl: [SUMM[foot][bl][T_]["dA_plus"] for T_ in TERC] for bl in BETAS[foot]} for foot in FOOT}
sub_by_mass = {foot: {bl: {T_: [w_ for w_ in W_BULK if all(w_ < r_["c_A_perp_km_s"] for r_ in TAB["E3_clusters"][foot][bl]
                                                             if r_["tercile"] == T_ and r_["mass_factor"] == 1.0)]
                          for T_ in TERC} for bl in BETAS[foot]} for foot in FOOT}
RES["step4"] = {"dA_plus_by_tercile": order, "bulk_speeds_subsonic_at_all_core_radii": sub_by_mass,
                "S4_onset": "unchanged: S4's static mu_K branch is a static held configuration, so H-COV/H-PN apply "
                            "(C1 adds nothing); r_C ~ M^(1/6) ordering stands" if static_zero else "not established"}
log(f"  dA+ by tercile (T1/T2/T3): " + "; ".join(f"{foot} {bl} " + "/".join(f"{v:+.4f}" for v in order[foot][bl])
                                                 for foot in FOOT for bl in BETAS[foot]))
log(f"  bulk speeds subsonic at all core radii (T1/T2/T3): " + "; ".join(
    f"{foot} {bl} " + "/".join(str([int(w_) for w_ in sub_by_mass[foot][bl][T_]]) for T_ in TERC)
    for foot in FOOT for bl in BETAS[foot]))
log(f"  isolated galaxies: static change 0 (H-COV, H-PN); moving, subsonic (X15 T3b) max dlog10 g: " + "; ".join(
    f"{foot} {bl} {v:.3f}" for foot in FOOT for bl, v in gal_moving[foot].items()))
log(f"  E_needed (A_MID,CAL - 1, min over h): {E_need}")
# ---- A2 POST-RESULT diagnostics (reported only; NO verdict weight)
log("")
log("A2 POST-RESULT DIAGNOSTICS (reported only; no verdict weight)")
# (a) H-RESP's own k -> 0 limit keeps a moving member's total sub-phantom charge static (omega^2/(K rho + B k^2) -> 0),
#     while the frozen member estimator applied the k -> infinity (c_A) response to that monopole. Re-grade without it.
SUMM_NOMEM = {foot: {bl: summarize(foot, bl, with_members=False) for bl in BETAS[foot]} for foot in FOOT}
diag_a = {foot: dict(zip(("class", "triggers"), foot_class(SUMM_NOMEM[foot], foot)[:2])) for foot in FOOT}
k0_lim = sp.limit(expect.subs(om, k * sp.Symbol("w_cos", positive=True)), k, 0)
RES["A2_diag_members_off"] = {"summary": SUMM_NOMEM, "class_per_footing": diag_a, "H_RESP_k0_limit": str(k0_lim)}
log(f"  (a) H-RESP response at k -> 0 with omega = k w cos: {k0_lim} (static: the moving member's total sub-phantom is "
    f"unchanged at linear order). Frozen rules with the member channel set to 0: "
    + "; ".join(f"{foot} {v_['class']} {v_['triggers']}" for foot, v_ in diag_a.items()))
for foot in FOOT:
    log(f"      {foot} dA+ (T1/T2/T3) without members: " + "; ".join(
        f"{bl} " + "/".join(f"{SUMM_NOMEM[foot][bl][T_]['dA_plus']:+.4f}" for T_ in TERC) for bl in BETAS[foot]))
# (b) coupled growth rate at beta_min (the frozen report gave beta_max only)
diag_b = {}
for foot in FOOT:
    for lab in MU_H:
        diag_b[f"{foot}|{lab}"] = {f"{zl}|k{kk:g}": coupled_rate(a_, kk, BETAS[foot]["beta_min"], MU_H[lab])
                                   for zl, a_ in (("z1100", 1 / 1101), ("z0", 1.0)) for kk in (1.0, 10.0)}
RES["A2_diag_rate_beta_min"] = diag_b
log("  (b) coupled growth rate sqrt(lambda+)/H at beta_min: " + "; ".join(
    f"{key} " + ", ".join(f"{kz} {vv:.3g}" for kz, vv in v.items()) for key, v in diag_b.items()))
# (c) the cells that set the bulk maxima at beta_max(0.03)
diag_c = {}
for foot in FOOT:
    for T_ in TERC:
        best = None
        for c_ in DA[foot]["beta_max_0.03"]:
            if c_["tercile"] != T_ or c_["mass_factor"] != 1.0:
                continue
            for b_ in c_["bulk"]:
                if b_["dA"] is not None and (best is None or b_["dA"] > best["dA"]):
                    best = {"dA": b_["dA"], "w_km_s": b_["w_km_s"], "R_h_Mpc": b_["R_h_Mpc"], "r_Mpc": c_["r_Mpc"],
                            "v_c_km_s": c_["v_c_km_s"], "c_A_perp_km_s": c_["c_A_perp_km_s"], "p1": c_["p1"]}
        diag_c[f"{foot}|{T_}"] = best
RES["A2_diag_bulk_max_cells_beta_max_0.03"] = diag_c
log("  (c) bulk maxima at beta_max(0.03): " + "; ".join(
    f"{key} {v_['dA']:+.4f} (w {v_['w_km_s']:.0f}, r {v_['r_Mpc']} Mpc, R_h {v_['R_h_Mpc']} Mpc, v_c {v_['v_c_km_s']:.0f}, "
    f"c_A {v_['c_A_perp_km_s']:.0f} km/s, p1 {v_['p1']:.3f})" for key, v_ in diag_c.items()))
log("")
log("VERDICT")
log(f"  {verdict}  (per footing: {foot_verdict}; heavy terciles with every bulk cell supersonic: {bulk_na_all})")
log(f"  triggers: {foot_triggers}")
if MUTATE:
    must_fail = {"H-COV": "m1", "S0-2": "m2", "S0-1": "m3", "S0-4": "m4", "S0-5": "m5", "G-DISP": "m6", "P0": "m7"}
    failed = {c["id"] for c in CHECKS if not c["pass"]}
    RES["mutate_required_failures"] = {cid: (cid in failed) for cid in must_fail}
    log(f"  MUTATE: required failures {RES['mutate_required_failures']}; all failed checks {sorted(failed)}")
finish()
