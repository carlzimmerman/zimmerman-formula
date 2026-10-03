#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG292 -- STRONG HYPERBOLICITY OF GR + THE BPS KHRONON (the C-H/K principal symbol) AND CRITERION-B CONE COMPATIBILITY.
XC2 left this OPEN ("strong hyperbolicity of GR + the BPS khronon on arbitrary nonlinear backgrounds").  The criteria,
formulations, tests, controls and decision rule were frozen first: FROZEN_CRITERIA.md (commit 6eaa9ea60).

THE SYSTEM.  L340's C-H/K: I_CH + c^3/(16 pi G) Int sqrt(-g)[alpha_c a.a - c_2 K^2], beta = 0, lambda_K = 1 + c_2.  Its
principal symbol is claimed (XC2 B5, XC1 A3, XC6) to be that of sqrt(-g)[R - beta K_mn K^mn - c_2 K^2 + alpha a.a]; R0
re-verifies that claim in-lane before it is used.  beta is kept symbolic only to state conditions.

FORMULATIONS (frozen).  F1: covariant, full de Donder gauge, khronon pi retained, leaf-elliptic factor removed by the
order reduction pi~ = |grad| pi; hyperbolicity w.r.t. d tau.  F2 (carries the verdict): unitary time gauge t = tau, the
spatial diffeomorphisms fixed by the spatial components of a de Donder vector -- F2a with the 4-D trace (the spatial
harmonic coordinate condition), F2b with the spatial trace -- and the lapse eliminated through its leaf-elliptic equation.

WHAT IS CHECKED.  R0 (MOND sector lower order), M (machinery: EH normalisation, gauge invariance), C1 (GR in harmonic
gauge), T1 (characteristic determinants, symbolic), C3 (Jacobson-Mattingly speeds), SH (T2-T5 at the 18 record points),
COND (conditions, symbolic) + C5 (c_S = 1 probe), C2 (minimal Horava), T6 (general frozen background), T7 (non-leaf
slicing), CB (criterion B).  MUTATE=1 flips alpha_c -> -alpha_c at the 18 points (C4): the verdict formulation must fail.

SCOPE.  Linearised, frozen-coefficient, high-frequency principal symbol; the stated gauges; backgrounds whose filtered
field does not vanish (open zero-field regions excluded, XC5).  Not a nonlinear well-posedness theorem.

Run from the repository root:
  python3 campaign_fresh_gravity/CFG292_khronon_strong_hyperbolicity/cfg292_khronon_strong_hyperbolicity.py
"""
import os, sys, json, math, time, re
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq
from sympy.polys.matrices import DomainMatrix

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from cfg292_lib import (R4, PAIRS, XI, HV, PIV, UV, VARS_H, L_EH, L_gf, L_khronon, L_aether, khronon_linear,
                        symbol_matrix, deDonder)

MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "CFG292", "cfg292_khronon_strong_hyperbolicity"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "frozen_criteria_commit": "6eaa9ea60", "checks": {}, "numbers": {}}
T0 = time.time()
mp.mp.dps = 60


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (finding, not load-bearing)'} {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT IS CHECKED")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: alpha_c -> -alpha_c at every record point; the verdict formulation must FAIL (C4) ***")

al, be, c2 = sp.symbols("alpha beta c_2", real=True)
lam, kk = sp.symbols("lambda k", real=True)
HALF = sp.Rational(1, 2)
ETA = sp.diag(-1, 1, 1, 1)
DT = [1, 0, 0, 0]

# ============================================================================================ inputs
banner("INPUTS: the record values (committed files)")
L340 = json.load(open(os.path.join(REPO, "real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json")))
L350 = json.load(open(os.path.join(REPO, "real_research/g03_audit_2026/L350_chk_cosmological_G_gate_results.json")))
XC1J = json.load(open(os.path.join(REPO, "real_research/extra_crispy_2026/XC1_strong_coupling_chk_results.json")))
XC2J = json.load(open(os.path.join(REPO, "real_research/extra_crispy_2026/XC2_wellposedness_scoping_results.json")))
XC6J = json.load(open(os.path.join(REPO, "real_research/extra_crispy_2026/XC6_filter_variation_soft_leg_results.json")))
RECIPE = open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md"), encoding="utf-8").read()
AC_MIN, AC_MAX = L340["numbers"]["P1"]["alpha_c_min"], L340["numbers"]["P1"]["alpha_c_max"]
C2_MIN, C2_MAX = L340["numbers"]["P1"]["c2_min"], L340["numbers"]["P1"]["c2_max"]
CAPS = sorted(float(r["c2_ceiling"]) for r in L350["numbers"]["G2"]["rows"])
LAMK_EDGE_OK = "1<λ_K≤1.10" in RECIPE
C2_RECIPE = 0.10
def rat(x):
    return sp.Rational(f"{x:.5e}")                      # 6 significant digits
ALPHAS = [rat(AC_MIN), rat(AC_MAX)]
C2S = [rat(c) for c in CAPS] + [rat(C2_MIN), rat(C2_MAX), rat(C2_RECIPE)]
POINTS = [(a, c) for a in ALPHAS for c in C2S]
SIGN = -1 if MUTATE else 1
P(f"    L340 P1 window: alpha_c in ({AC_MIN:.4e}, {AC_MAX:.2e}), c_2 in ({C2_MIN:.4e}, {C2_MAX:.4f})")
P(f"    L350 G2 Planck-era c_2 ceilings: {', '.join(f'{c:.3e}' for c in CAPS)}")
P(f"    recipe sec. 9 lambda_K edge '1<lambda_K<=1.10' present: {LAMK_EDGE_OK} -> c_2 = {C2_RECIPE}")
P(f"    XC1 A9 UV khronon speed range: {XC1J['numbers']['A9']['cs_uv_min']:.4g} .. {XC1J['numbers']['A9']['cs_uv_max']:.4g} c")
P(f"    18 evaluation points (alpha_c x c_2), exact rationals at 6 significant digits{'; alpha_c sign FLIPPED (MUTATE)' if MUTATE else ''}")
OUT["numbers"]["inputs"] = {"alpha_c": [str(a) for a in ALPHAS], "c2": [str(c) for c in C2S], "lambdaK_edge_in_recipe": LAMK_EDGE_OK,
                            "XC1_A9": XC1J["numbers"]["A9"]}

# ============================================================================================ R0
banner("R0  RE-VERIFICATION: the MOND sector is lower order (XC2 B5), U = ln N kills C-H (XC1 A3), delta S (XC6)")
# (a) committed results, re-applying XC2's own rule
b5_key = [k_ for k_ in XC2J["checks"] if k_.startswith("B5")][0]
r5 = {float(k_): v_ for k_, v_ in XC2J["numbers"]["B5"].items()}
pf5 = {float(k_): v_ for k_, v_ in XC2J["numbers"]["B5_prefactor"].items()}
vals5 = [r5[k_] for k_ in sorted(r5)]
rule5 = (len(vals5) == 3 and vals5[0] > vals5[1] > vals5[2] and vals5[2] < 1e-4 and max(pf5.values()) / min(pf5.values()) < 5)
xc6_ok = all(v_["ok"] for k_, v_ in XC6J["checks"].items() if k_[:2] in ("D3", "D4"))
xc1_a3 = [v_["ok"] for k_, v_ in XC1J["checks"].items() if k_.startswith("A3")][0]
P(f"    XC2 B5 committed: ok = {XC2J['checks'][b5_key]['ok']}; ratios {', '.join(f'{k_:.0f}/xi: {v_:.2e}' for k_, v_ in sorted(r5.items()))}; "
  f"rule re-applied: {rule5};  XC6 D3, D4 ok: {xc6_ok};  XC1 A3 ok: {xc1_a3}")
# (b) the frozen-coefficient symbol of S^T D^T C D S, order -infinity
kq, xq, CTs, CLs, nn_ = sp.symbols("k xi C_T C_L n", positive=True)
cth = sp.Symbol("c", real=True)                                         # cos of the angle between k and the field
symMOND = sp.exp(-xq**2 * kq**2) * kq**2 * (CTs * (1 - cth**2) + CLs * cth**2)
ratio_bound = sp.simplify(symMOND / kq**2)
lim_ok = sp.limit(kq**nn_ * sp.exp(-xq**2 * kq**2), kq, sp.oo) == 0
P(f"    symbol of S^T D^T C D S: {symMOND};  / k^2 = {ratio_bound};  k^n e^(-xi^2 k^2) -> 0 for every n > 0: {lim_ok}")
# (c) U elimination with the filtered q-term: Schur complement, order -infinity, positive
uu, vv = sp.symbols("u v", real=True); CC, EE = sp.symbols("C E", positive=True)
Lq = 2 * kq**2 * (uu + vv)**2 + 2 * CC * EE * kq**2 * uu**2
ustar = sp.solve(sp.diff(Lq, uu), uu)[0]
schur = sp.simplify(Lq.subs(uu, ustar))
schur_ok = sp.simplify(schur - 2 * kq**2 * vv**2 * CC * EE / (1 + CC * EE)) == 0
lim2 = sp.limit(kq**nn_ * CC * sp.exp(-xq**2 * kq**2) / (1 + CC * sp.exp(-xq**2 * kq**2)), kq, sp.oo) == 0
P(f"    U-elimination: Schur complement = {schur}  (= 2k^2 v^2 C E/(1 + C E): {schur_ok}); x k^n -> 0: {lim2}")
# (d) nu_mono rebuilt (L340 A1) and an independent numerical B5 on a zero-free and a zero-containing background
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e_=1e-6):
    return (h_rar(y * (1 + e_)) - h_rar(y * (1 - e_))) / (2 * y * e_)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
CT_f = lambda y: np.interp(np.log10(y), LYG, H_MONO) / y
CL_f = lambda y: np.interp(np.log10(y), LYG, DH_MONO)
yp_ok = abs(Y_P - L340["numbers"]["A1"]["y_p"]) < 1e-6
yy = np.logspace(-3, 4, 1401)
ct_min, cl_min = float(CT_f(yy).min()), float(CL_f(yy).min())
ct_small = {f"{y_:.0e}": float(CT_f(y_)) for y_ in (1e-2, 1e-4, 1e-6, 1e-8)}
NG = 64; dx = 1.0 / NG; XIF = 2.5 * dx
kx = 2 * np.pi * np.fft.fftfreq(NG, d=dx); KX, KY = np.meshgrid(kx, kx, indexing="ij"); K2 = KX**2 + KY**2
SK = np.exp(-0.5 * XIF**2 * K2)
RNG = np.random.default_rng(292)
def grad(f):
    fh = np.fft.fft2(f); return np.real(np.fft.ifft2(1j * KX * fh)), np.real(np.fft.ifft2(1j * KY * fh))
def div(gx, gy):
    return np.real(np.fft.ifft2(1j * KX * np.fft.fft2(gx) + 1j * KY * np.fft.fft2(gy)))
def filt(f):
    return np.real(np.fft.ifft2(SK * np.fft.fft2(f)))
smooth = filt(filt(filt(RNG.standard_normal((NG, NG)))))
xg = (np.arange(NG) + 0.5) * dx; XX, YY = np.meshgrid(xg, xg, indexing="ij")
sgx, sgy = grad(smooth); smooth /= np.max(np.hypot(sgx, sgy))
def b5_ratio(Ubg_gx, Ubg_gy, Kxi):
    """power iteration of the linearised filtered MOND operator on |k| >= Kxi/xi, divided by K^2 (EH principal order)."""
    r = np.maximum(np.hypot(Ubg_gx, Ubg_gy), 1e-14); ex_, ey_ = Ubg_gx / r, Ubg_gy / r
    CT, CL = CT_f(r), CL_f(r)
    Kc = Kxi / XIF; mask = (np.sqrt(K2) >= Kc).astype(float)
    v = np.real(np.fft.ifft2(mask * np.fft.fft2(RNG.standard_normal((NG, NG)))))
    nrm = 0.0
    for _ in range(40):
        wx, wy = grad(filt(v)); par = wx * ex_ + wy * ey_
        Mv = -filt(div(CT * wx + (CL - CT) * par * ex_, CT * wy + (CL - CT) * par * ey_))
        Mv = np.real(np.fft.ifft2(mask * np.fft.fft2(Mv))); nrm = np.linalg.norm(Mv); v = Mv / (nrm + 1e-300)
    return nrm / Kc**2, float(CT.max()), float(r.min())
# zero-free background: uniform field y0 = 0.5 a0 plus a 30% smooth modulation (filtered field never vanishes)
gmax_ = np.max(np.hypot(sgx, sgy))
bgs = {"zero-free": (0.5 + 0.15 * sgx / np.max(np.abs(sgx)), 0.15 * sgy / np.max(np.abs(sgy))),
       "isolated zeros": (3.0 * sgx / gmax_, 3.0 * sgy / gmax_)}
R0num = {}
for nm, (gx_, gy_) in bgs.items():
    rows_ = {}
    for Kxi in (2.0, 3.0, 4.0):
        rr_, ctmax, ymin = b5_ratio(gx_, gy_, Kxi)
        rows_[Kxi] = {"ratio": rr_, "prefactor": rr_ / math.exp(-Kxi**2), "CT_max": ctmax, "y_min": ymin}
    R0num[nm] = rows_
    P(f"    numerical B5 ({nm:14s}): " + "; ".join(f"K = {k_:.0f}/xi: ratio {v_['ratio']:.2e}, prefactor {v_['prefactor']:.2f}"
                                               for k_, v_ in rows_.items()) + f";  min y = {rows_[2.0]['y_min']:.2e}, max C_T = {rows_[2.0]['CT_max']:.1f}")
zf = R0num["zero-free"]; zr = [zf[k_]["ratio"] for k_ in (2.0, 3.0, 4.0)]; zp = [zf[k_]["prefactor"] for k_ in (2.0, 3.0, 4.0)]
num_ok = zr[0] > zr[1] > zr[2] and zr[2] < 1e-4 and max(zp) / min(zp) < 5
P(f"    nu_mono rebuilt: y_p match {yp_ok}; min C_T = {ct_min:.2e}, min C_L = {cl_min:+.2e} (y in 1e-3..1e4); "
  f"C_T at small y: {ct_small}  (~ y^(-1/2): unbounded at zero field)")
OUT["numbers"]["R0"] = {"XC2_B5_ratios": r5, "XC2_B5_prefactors": pf5, "rule_reapplied": rule5, "XC6_D3_D4": xc6_ok,
                        "XC1_A3": xc1_a3, "symbol": str(symMOND), "schur": str(schur), "numerical": R0num,
                        "CT_min": ct_min, "CL_min": cl_min, "CT_small_y": ct_small}
check("R0 the MOND sector is order -infinity where the filtered field is non-zero: XC2 B5 (committed, rule re-applied), "
      "the frozen symbol e^{-xi^2 k^2} k^T C k (sympy), the U-elimination Schur complement 2k^2 C E/(1+CE) (sympy, positive), "
      "an independent power iteration on a zero-free background, and XC6 D3/D4 (delta S) all agree",
      f"XC2 B5 {XC2J['checks'][b5_key]['ok']}/rule {rule5}; symbol limit {lim_ok}; Schur {schur_ok}/{lim2}; numeric zero-free "
      f"ratios {', '.join(f'{x:.1e}' for x in zr)} (prefactors {', '.join(f'{x:.1f}' for x in zp)}); XC6 {xc6_ok}; XC1 A3 {xc1_a3}",
      XC2J["checks"][b5_key]["ok"] and rule5 and lim_ok and schur_ok and lim2 and num_ok and xc6_ok and xc1_a3 and yp_ok
      and ct_min > 0 and cl_min > 0,
      "so the principal symbol of C-H/K is GR + the BPS khronon; disclosed: C_T = nu - 1 ~ y^(-1/2) is unbounded where the "
      "filtered field vanishes (the 'isolated zeros' row has a larger prefactor), so open zero-field regions are outside scope")

# ============================================================================================ M machinery
banner("M  MACHINERY: Einstein-Hilbert normalisation, the gauge-fixing constant, khronon linearisation, gauge invariance")
LE = L_EH(ETA)
from cfg292_lib import dH
fd, fz = sp.symbols("fd fz")
sub = {s_: 0 for s_ in LE.free_symbols}; sub[dH[0][1][2]] = fd; sub[dH[3][1][2]] = fz
tt = sp.factor(LE.xreplace(sub))
pp_, qq_ = sp.symbols("p1:4"), sp.symbols("q1:4")
sub = {s_: 0 for s_ in LE.free_symbols}
for i in (1, 2, 3):
    sub[dH[i][0][0]] = -2 * pp_[i - 1]
    for j in (1, 2, 3):
        sub[dH[i][j][j]] = -2 * qq_[i - 1]
newt = sp.expand(LE.xreplace(sub))
newt_target = sp.expand(sum(2 * q_**2 - 4 * p_ * q_ for p_, q_ in zip(pp_, qq_)))
cg = sp.Symbol("c_gf")
Pg = symbol_matrix(LE + L_gf(ETA, cg, "full"), VARS_H)
cgf_sol = sp.solve([sp.Poly(e_, *XI).coeff_monomial(XI[0] * XI[1]) for e_ in Pg if e_ != 0], cg)
CGF = cgf_sol[cg] if isinstance(cgf_sol, dict) else cgf_sol[0][0]
xi2 = -XI[0]**2 + XI[1]**2 + XI[2]**2 + XI[3]**2
PGR = symbol_matrix(LE + L_gf(ETA, CGF, "full"), VARS_H)
G0 = PGR.applyfunc(lambda e_: sp.cancel(e_ / xi2))
gr_prop = all(sp.Poly(e_, *XI).total_degree() <= 0 for e_ in G0 if e_ != 0) and G0.det() != 0
LK, QK = L_khronon(ETA, DT, al, be, c2)
z_ = sp.symbols("z0:4")
def gauge_vec(gbar, dtau, with_pi=True):
    ginv = gbar.inv(); zup = [sum(ginv[m, n] * z_[n] for n in R4) for m in R4]
    v = [XI[m] * z_[n] + XI[n] * z_[m] for (m, n) in PAIRS]
    return sp.Matrix(v + ([sum(zup[m] * dtau[m] for m in R4)] if with_pi else []))
PFULL0 = symbol_matrix(LE + LK, VARS_H + [PIV])
ginv_res = (PFULL0 * gauge_vec(ETA, DT)).applyfunc(sp.expand)
PiPi = sp.factor(PFULL0[10, 10])
P(f"    TT wave h_12 = f(t,z): L = {tt}   (positive kinetic term);  static Newtonian: L - (2|grad psi|^2 - 4 grad phi.grad psi) = "
  f"{sp.simplify(newt - newt_target)}  (ACTION.md's weak static form)")
P(f"    gauge-fixing constant fixed by C1: c_gf = {CGF};  GR + gauge term = (xi.xi) x constant invertible matrix: {gr_prop}")
P(f"    khronon on the aligned flat background: delta ln N = {QK['dlnN']};  K^(1) = {QK['K1']}")
P(f"    a^(1)_i = {QK['a1_dn'][1:]};  Pi-Pi symbol = {PiPi}  (decoupling limit alpha xi_0^2 k^2 - (beta + c_2) k^4)")
P(f"    EH + khronon symbol annihilates every pure-gauge vector (delta h = -L_z g, delta pi = -z.d tau): {all(e_ == 0 for e_ in ginv_res)}")
OUT["numbers"]["M"] = {"TT": str(tt), "c_gf": str(CGF), "dlnN": str(QK["dlnN"]), "K1": str(QK["K1"]), "PiPi": str(PiPi)}
check("M the quadratic EH Lagrangian has the right sign and normalisation (TT kinetic +1/2, ACTION.md's static 2|grad psi|^2 "
      "- 4 grad phi.grad psi); c_gf makes GR's symbol (xi.xi) x const; the khronon linearisation reproduces delta ln N = "
      "-pi_t - h_00/2, K = h_kk,t/2 - d_i h_0i - Lap pi; the symbol is diffeomorphism invariant",
      f"TT {tt}; Newtonian residual {sp.simplify(newt - newt_target)}; c_gf {CGF}; gauge residual zero {all(e_ == 0 for e_ in ginv_res)}",
      sp.simplify(tt - (fd - fz) * (fd + fz) / 2) == 0 and sp.simplify(newt - newt_target) == 0 and CGF == HALF and gr_prop
      and all(e_ == 0 for e_ in ginv_res) and sp.simplify(PiPi - 2 * (XI[1]**2 + XI[2]**2 + XI[3]**2) *
      (al * XI[0]**2 - (be + c2) * (XI[1]**2 + XI[2]**2 + XI[3]**2))) == 0)

# ============================================================================================ helicity blocks
def helicity_blocks(Pz, V):
    """congruence H11 = a + b, H22 = a - b; return names, the transformed matrix, and the blocks (off-block entries checked)."""
    n = len(V); names = [str(v_) for v_ in V]
    i11, i22 = names.index("H11"), names.index("H22")
    S = sp.eye(n); S[i11, i22] = 1; S[i22, i11] = 1; S[i22, i22] = -1
    Pp = (S.T * Pz * S).applyfunc(sp.expand)
    names[i11], names[i22] = "a", "b"
    blocks = {"scalar": [x for x in ["H00", "H03", "H33", "a", "Pi", "U3"] if x in names],
              "vector1": [x for x in ["H01", "H13", "U1"] if x in names], "vector2": [x for x in ["H02", "H23", "U2"] if x in names],
              "tensor+": ["b"], "tensorx": ["H12"]}
    off = [(names[i], names[j]) for i in range(n) for j in range(n) if Pp[i, j] != 0
           and not any(names[i] in b_ and names[j] in b_ for b_ in blocks.values())]
    out = {bn: Pp.extract([names.index(x) for x in b_], [names.index(x) for x in b_]) for bn, b_ in blocks.items()}
    return out, blocks, off


def schur_lapse(Pb, idx=0):
    """eliminate the lapse row/column idx (must be lambda-free and non-zero)."""
    p00 = Pb[idx, idx]
    rest = [i for i in range(Pb.rows) if i != idx]
    Prr = Pb.extract(rest, rest); Pr0 = Pb.extract(rest, [idx])
    return (Prr - Pr0 * Pr0.T / p00).applyfunc(sp.expand), p00


def det_poly(Mx, var):
    """exact determinant of a matrix polynomial in var with rational coefficients (DomainMatrix over QQ[var])."""
    ring = sp.QQ[var]
    return sp.Poly(ring.to_sympy(DomainMatrix.from_Matrix(Mx.applyfunc(sp.expand)).convert_to(ring).det()), var)


FORMS = {"F1": ("full", True), "F2a": ("spatial4", False), "F2b": ("spatial3", False)}
def form_lagrangian(name, gbar=ETA, dtau=DT, alpha=al, beta=be, cc2=c2):
    mode, with_pi = FORMS[name]
    Lk_, _ = L_khronon(gbar, dtau, alpha, beta, cc2)
    return L_EH(gbar) + Lk_ + L_gf(gbar, CGF, mode), (VARS_H + [PIV]) if with_pi else list(VARS_H)


SYMP = {}
for nm in FORMS:
    Lf, Vf = form_lagrangian(nm)
    SYMP[nm] = (symbol_matrix(Lf, Vf), Vf)

# ============================================================================================ C1 GR
banner("C1  CONTROL: GR alone (no khronon) in harmonic gauge")
def analyse_pencil(Pl, lamv=lam):
    """exact: leading matrix, roots, reality, multiplicity vs nullity of P(root)."""
    n = Pl.rows
    detp = det_poly(Pl, lamv)
    A = Pl.applyfunc(lambda e_: sp.Poly(e_, lamv).coeff_monomial(lamv**2))
    A_inv = (detp.degree() == 2 * n) and A.det() != 0
    res = {"A_invertible": bool(A_inv), "degree": detp.degree(), "n": n, "roots": [], "real": True, "diag": True}
    if detp.is_zero:
        res.update(real=False, diag=False); return res
    _, facs = sp.factor_list(detp.as_expr(), lamv)
    for f_, m_ in facs:
        fp = sp.Poly(f_, lamv)
        if fp.degree() == 0:
            continue
        rts = sp.roots(fp)
        if sum(rts.values()) != fp.degree():
            rts = {r_: 1 for r_ in fp.all_roots()}
        for r_, mr in rts.items():
            mult = m_ * mr
            isreal = bool(r_.is_real)
            if mult > 1 and isreal:
                M_ = Pl.xreplace({lamv: r_})
                null = n - M_.rank(simplify=True)
            elif isreal:
                null = 1
            else:
                null = None
            res["roots"].append({"root": str(r_), "root_expr": r_, "root_float": float(sp.re(sp.N(r_, 30))) if isreal else complex(sp.N(r_, 20)),
                                 "mult": int(mult), "nullity": null, "real": isreal})
            res["real"] &= isreal
            res["diag"] &= (null == mult)
    res["strong"] = bool(res["A_invertible"] and res["real"] and res["diag"])
    return res


Pz_gr = PGR.xreplace({XI[0]: lam, XI[1]: 0, XI[2]: 0, XI[3]: 1})
blk_gr, _, off_gr = helicity_blocks(Pz_gr, VARS_H)
gr_res = {bn: analyse_pencil(Pb) for bn, Pb in blk_gr.items()}
gr_speeds = sorted({round(abs(r_["root_float"]), 12) for v_ in gr_res.values() for r_ in v_["roots"]})
for bn, v_ in gr_res.items():
    P(f"    {bn:8s}: A invertible {v_['A_invertible']}, roots " + ", ".join(f"{r_['root']} (mult {r_['mult']}, null {r_['nullity']})" for r_ in v_["roots"]))
gr_ok = all(v_["strong"] for v_ in gr_res.values()) and gr_speeds == [1.0] and not off_gr
OUT["numbers"]["C1"] = {k_: v_ for k_, v_ in gr_res.items()}
check("C1 GR in harmonic gauge is strongly hyperbolic: every helicity block has an invertible leading matrix, real roots +-1 "
      "and complete eigenvectors (nullity = multiplicity)", f"speeds {gr_speeds}; strong in every block: {gr_ok}", gr_ok)

# ============================================================================================ T1 characteristic determinants
banner("T1  CHARACTERISTIC DETERMINANTS, symbolic in (alpha, beta, c_2), khat = z, u aligned")
SCAL = al * (1 - be) * (2 + be + 3 * c2) * lam**2 - (be + c2) * (2 - al) * kk**2      # scalar factor, expected
CS2 = (be + c2) * (2 - al) / (al * (1 - be) * (2 + be + 3 * c2))
T1 = {}
t1_ok = True
for nm, (Pf, Vf) in SYMP.items():
    Pz = Pf.xreplace({XI[0]: lam, XI[1]: 0, XI[2]: 0, XI[3]: kk})
    blks, bdef, off = helicity_blocks(Pz, Vf)
    dets = {bn: sp.factor(Pb.det()) for bn, Pb in blks.items()}
    T1[nm] = {bn: str(d_) for bn, d_ in dets.items()}
    gpow = 4 if nm == "F1" else 2
    exp_scal = kk**2 * (kk**2 - lam**2)**gpow * SCAL
    r_s = sp.simplify(dets["scalar"] / exp_scal)
    r_v = sp.simplify(dets["vector1"] / ((be - 1) * (kk**2 - lam**2)**2))
    r_t = sp.simplify(dets["tensor+"] / ((1 - be) * lam**2 - kk**2))
    ok_ = (not off) and r_s.is_number and r_s != 0 and r_v.is_number and r_v != 0 and r_t.is_number and r_t != 0 \
        and sp.simplify(dets["vector1"] - dets["vector2"]) == 0 and sp.simplify(dets["tensor+"] - dets["tensorx"]) == 0
    t1_ok &= ok_
    P(f"    {nm}: off-block entries {off if off else 'none'}")
    P(f"      scalar  {bdef['scalar']}: det = {r_s} * k^2 (k^2 - lambda^2)^{gpow} [alpha(1-beta)(2+beta+3c_2) lambda^2 - (beta+c_2)(2-alpha) k^2]")
    P(f"      vector  {bdef['vector1']} (x2): det = {r_v} * (beta - 1)(k^2 - lambda^2)^2   -- gauge/constraint only, no physical vector mode")
    P(f"      tensor  (x2): det = {r_t} * [(1 - beta) lambda^2 - k^2]")
cs2_lit = (be + c2) * (2 - al) / (al * (1 - be) * (2 + be + 3 * c2))
OUT["numbers"]["T1"] = T1
check("T1 every determinant factors exactly: tensor (1-beta) lambda^2 = k^2 (c_T^2 = 1/(1-beta)); vector blocks carry only the "
      "gauge speed 1 (no vector mode: hypersurface orthogonality); scalar = k^2 (leaf-elliptic, instantaneous) x (k^2 - "
      "lambda^2)^m (gauge/constraint) x the khronon factor, c_S^2 = (beta+c_2)(2-alpha)/(alpha(1-beta)(2+beta+3c_2)); identical in "
      "F1, F2a, F2b; block-diagonality verified", f"all identities hold: {t1_ok}", t1_ok,
      "the leaf-elliptic k^2 (the lapse/instantaneous mode) is a factor in every formulation; F1's pi~ = |grad| pi reduction "
      "removes it, F2's lapse elimination removes it")

# ============================================================================================ C3 Einstein-aether
banner("C3  CONTROL: Einstein-aether wave speeds (Jacobson & Mattingly 2004; Jacobson 2008 eqs 11-13), exact at a test point")
c1t, c2t, c3t, c4t = sp.Rational(1, 10), sp.Rational(1, 5), sp.Rational(1, 20), sp.Rational(1, 30)
c13, c14, c123 = c1t + c3t, c1t + c4t, c1t + c2t + c3t
s2_lit = 1 / (1 - c13); s1_lit = (2 * c1t - c1t**2 + c3t**2) / (2 * c14 * (1 - c13))
s0_lit = c123 * (2 - c14) / (c14 * (1 - c13) * (2 + c13 + 3 * c2t))
s0_alt = (c123 / c14) * (2 - c14) / (2 * (1 + c2t)**2 - c123 * (1 + c2t + c123))       # the form shown on the arXiv HTML render
LAE = L_EH(ETA) + L_aether(c1t, c2t, c3t, c4t) + L_gf(ETA, CGF, "full")
VAE = list(VARS_H) + [UV[1], UV[2], UV[3]]
PAE = symbol_matrix(LAE, VAE).xreplace({XI[0]: lam, XI[1]: 0, XI[2]: 0, XI[3]: 1})
blk_ae, bdef_ae, off_ae = helicity_blocks(PAE, VAE)
found = {}
for bn in ("tensor+", "vector1", "scalar"):
    d_ = sp.Poly(sp.expand(blk_ae[bn].det()), lam)
    _, facs = sp.factor_list(d_.as_expr(), lam)
    sq = []
    for f_, m_ in facs:
        fp = sp.Poly(f_, lam)
        if fp.degree() == 2 and fp.coeff_monomial(lam) == 0:
            s2v = -fp.coeff_monomial(1) / fp.coeff_monomial(lam**2)
            if s2v != 1:
                sq.append(s2v)
        elif fp.degree() == 1:
            r_ = -fp.coeff_monomial(1) / fp.coeff_monomial(lam)
            if abs(r_) != 1:
                sq.append(r_**2)
    found[bn] = sorted(set(sq))
P(f"    test point (c1, c2, c3, c4) = ({c1t}, {c2t}, {c3t}, {c4t}); off-block entries: {off_ae if off_ae else 'none'}")
P(f"    tensor: found s^2 = {found['tensor+']}  literature 1/(1-c13) = {s2_lit}")
P(f"    vector: found s^2 = {found['vector1']}  literature (2c1 - c1^2 + c3^2)/(2 c14 (1-c13)) = {s1_lit}")
P(f"    scalar: found s^2 = {found['scalar']}  literature c123(2-c14)/(c14(1-c13)(2+c13+3c2)) = {s0_lit} (HTML-render form: {s0_alt})")
map_ok = sp.simplify(CS2 - cs2_lit) == 0
gen_alt = sp.simplify((c2 + be) * (2 - al) / (al * (1 - be) * (2 + be + 3 * c2))
                      - ((be + c2) / al) * (2 - al) / (2 * (1 + c2)**2 - (be + c2) * (1 + c2 + be + c2))) == 0
c3_ok = found["tensor+"] == [s2_lit] and found["vector1"] == [s1_lit] and found["scalar"] == [s0_lit] and s0_alt == s0_lit and map_ok \
    and gen_alt and not off_ae
OUT["numbers"]["C3"] = {"found": {k_: [str(x) for x in v_] for k_, v_ in found.items()}, "lit": [str(s2_lit), str(s1_lit), str(s0_lit)]}
check("C3 the machinery reproduces all three Einstein-aether speeds exactly at the test point, the two published forms of "
      "s_0^2 agree, and the khronometric scalar factor of T1 equals s_0^2 under (c14, c13, c2) -> (alpha, beta, c_2) "
      "(Guemruekcueoglu+18 eq. 4, used by XC1)", f"found {found}; map identity {map_ok}; form identity {gen_alt}", c3_ok)

# ============================================================================================ SH at the 18 points
banner("SH  STRONG HYPERBOLICITY AT THE 18 RECORD POINTS (T2 leading matrix, T3 real roots, T4 complete eigenvectors; exact)")
def exact_point(nm, a_, c_, b_=0):
    Pf, Vf = SYMP[nm]
    Pz = Pf.xreplace({al: a_, be: b_, c2: c_, XI[0]: lam, XI[1]: 0, XI[2]: 0, XI[3]: 1})
    blks, _, off = helicity_blocks(Pz, Vf)
    out, lapse = {}, None
    for bn, Pb in blks.items():
        if bn == "scalar" and not FORMS[nm][1]:
            Pb, p00 = schur_lapse(Pb, 0)
            lapse = p00
        out[bn] = analyse_pencil(Pb)
    lapse_ok = True if lapse is None else (sp.Poly(lapse, lam).degree() <= 0 and lapse != 0)
    strong = all(v_["strong"] for v_ in out.values()) and lapse_ok and not off
    return out, strong, lapse
SH = {nm: [] for nm in FORMS}
for nm in FORMS:
    for (a_, c_) in POINTS:
        res, strong, lapse = exact_point(nm, SIGN * a_, c_)
        sc = res["scalar"]
        phys = [r_ for r_ in sc["roots"] if abs(abs(r_["root_float"]) - 1) > 1e-9] if sc["real"] else sc["roots"]
        cS = max(abs(r_["root_float"]) for r_ in phys) if (phys and sc["real"]) else None
        defic = [(bn, r_["root"], r_["mult"], r_["nullity"]) for bn, v_ in res.items() for r_ in v_["roots"]
                 if r_["real"] and r_["nullity"] != r_["mult"]]
        SH[nm].append({"alpha": str(SIGN * a_), "c2": str(c_), "strong": strong, "A_inv": all(v_["A_invertible"] for v_ in res.values()),
                       "real": all(v_["real"] for v_ in res.values()), "deficient": defic, "c_S": cS,
                       "lapse": None if lapse is None else str(lapse),
                       "nonreal": [r_["root_float"] for v_ in res.values() for r_ in v_["roots"] if not r_["real"]][:2]})
    n_ok = sum(r_["strong"] for r_ in SH[nm])
    ex = SH[nm][0]
    P(f"    {nm:3s}: strongly hyperbolic at {n_ok}/18 points;  e.g. alpha_c = {float(sp.Rational(ex['alpha'])):.3e}, c_2 = "
      f"{float(sp.Rational(ex['c2'])):.3e}: A invertible {ex['A_inv']}, roots real {ex['real']}, deficient eigenvalues "
      f"{[(d_[0], d_[1], f'mult {d_[2]} null {d_[3]}') for d_ in ex['deficient']] if ex['deficient'] else 'none'}"
      + (f", non-real roots e.g. {ex['nonreal']}" if ex["nonreal"] else ""))
cS_vals = [r_["c_S"] for r_ in SH["F2a"] if r_["c_S"]]
if cS_vals:
    P(f"    scalar speed over the 18 points (F2a): {min(cS_vals):.4g} .. {max(cS_vals):.4g} c   (XC1 A9: "
      f"{XC1J['numbers']['A9']['cs_uv_min']:.4g} .. {XC1J['numbers']['A9']['cs_uv_max']:.4g} c)")
OUT["numbers"]["SH_exact"] = SH
F2a_all = all(r_["strong"] for r_ in SH["F2a"]); F2b_all = all(r_["strong"] for r_ in SH["F2b"]); F1_all = all(r_["strong"] for r_ in SH["F1"])
same_speeds = all(r1["c_S"] is not None and r2["c_S"] is not None and abs(r1["c_S"] / r2["c_S"] - 1) < 1e-12
                  for r1, r2 in zip(SH["F1"], SH["F2a"])) if not MUTATE else False
check("SH-F2a (the leaf-sliced formulation that carries the verdict: t = tau, spatial harmonic coordinates, lapse elliptic) "
      "is strongly hyperbolic at all 18 record points (T2-T4 exact, every helicity block)",
      f"{sum(r_['strong'] for r_ in SH['F2a'])}/18", F2a_all,
      "T5 (uniformity in khat) is tested below on the unsplit matrices")
check("SH-F2b (spatial-trace variant) is strongly hyperbolic at all 18 points", f"{sum(r_['strong'] for r_ in SH['F2b'])}/18; "
      f"deficiency e.g. {SH['F2b'][0]['deficient']}", F2b_all,
      "reported whatever the outcome (frozen); a Jordan block at the gauge speed is a property of this gauge choice", load_bearing=False)
check("SH-F1 (covariant full de Donder + khronon) is strongly hyperbolic at all 18 points", f"{sum(r_['strong'] for r_ in SH['F1'])}/18; "
      f"deficiency e.g. {SH['F1'][0]['deficient']}; physical speeds equal to F2a's: {same_speeds}", F1_all,
      "reported whatever the outcome (frozen); a gauge-sector Jordan block: pi shifts under the residual harmonic gauge "
      "modes, which share speed 1 with the constraint modes", load_bearing=False)

# ============================================================================================ T5 uniformity in khat
banner("T5  UNIFORMITY IN khat: unsplit matrices at z and 5 random rational unit directions (exact spectra and nullities; "
       "eigenvector-matrix condition number in mpmath, 60 digits, Frobenius-orthonormal field basis)")
def to_mp(Mx):
    return mp.matrix([[mp.mpf(int(sp.numer(x))) / int(sp.denom(x)) for x in row] for row in Mx.tolist()])
def frob_scale(Vf):
    return [mp.mpf(1) if (str(v_) == "Pi" or str(v_)[1] == str(v_)[2]) else 1 / mp.sqrt(2) for v_ in Vf]
def abc_exact(Pl):
    return [Pl.applyfunc(lambda e_: sp.Poly(e_, lam).coeff_monomial(m_)) for m_ in (lam**2, lam, sp.Integer(1))]
def exact_full(nm, a_, c_, khat, b_=0):
    """the unsplit exact pencil at an exact unit direction khat; F2: the lapse H00 eliminated."""
    Pf, Vf = SYMP[nm]
    Pl = Pf.xreplace({al: a_, be: b_, c2: c_, XI[0]: lam, XI[1]: khat[0], XI[2]: khat[1], XI[3]: khat[2]}).applyfunc(sp.expand)
    V = list(Vf)
    if not FORMS[nm][1]:
        Pl, _ = schur_lapse(Pl, 0); V = V[1:]
    return Pl, V
def null_basis_mp(Pn, tol=mp.mpf(10)**-30):
    U_, Sv, Vt = mp.svd_r(Pn)
    smax = max(Sv)
    return [[Vt[i, j] for j in range(Pn.cols)] for i in range(len(Sv)) if Sv[i] < tol * max(smax, 1)]
def eig_cond(Pl, V, roots):
    """condition number of the companion's eigenvector matrix, eigenspace-orthonormal bases: eigenvectors (v, lambda v),
    v in ker P(lambda) (exact roots supplied); None if any eigenspace is incomplete."""
    S = mp.diag(frob_scale(V))
    A, B, C = [S * to_mp(X_) * S for X_ in abc_exact(Pl)]
    n = len(V); cols = []
    for r_, m_ in roots:
        lv = mp.mpf(str(sp.N(r_, 80)))
        nb = null_basis_mp(A * lv**2 + B * lv + C)
        if len(nb) != m_:
            return None
        Lm = mp.matrix(2 * n, len(nb))
        for jj, v_ in enumerate(nb):
            for r in range(n):
                Lm[r, jj] = v_[r]; Lm[n + r, jj] = lv * v_[r]
        Q_, _ = mp.qr(Lm, mode="skinny")
        cols += [[Q_[i, j] for i in range(2 * n)] for j in range(Q_.cols)]
    if len(cols) != 2 * n:
        return None
    T = mp.matrix(2 * n, 2 * n)
    for j, col in enumerate(cols):
        for i in range(2 * n):
            T[i, j] = col[i]
    _, sv, _ = mp.svd_r(T)
    return max(sv) / min(sv)
rng5 = np.random.default_rng(29202)
def rat_dir():
    a_ = sp.Rational(int(rng5.integers(-9, 10)), int(rng5.integers(1, 10)))
    b_ = sp.Rational(int(rng5.integers(-9, 10)), int(rng5.integers(1, 10)))
    den = 1 + a_**2 + b_**2
    return [2 * a_ / den, 2 * b_ / den, (1 - a_**2 - b_**2) / den]
DIRS = [[sp.Integer(0), sp.Integer(0), sp.Integer(1)]] + [rat_dir() for _ in range(5)]
unit_ok = all(sum(x**2 for x in d_) == 1 for d_ in DIRS)
P(f"    directions (exact unit vectors: {unit_ok}): " + "; ".join("(" + ", ".join(str(x) for x in d_) + ")" for d_ in DIRS))
T5 = {nm: [] for nm in FORMS}
for nm in FORMS:
    for (a_, c_) in POINTS:
        sigs, conds, strongs = [], [], []
        for d_ in DIRS:
            Pl, V = exact_full(nm, SIGN * a_, c_, d_)
            res = analyse_pencil(Pl)
            sig = sorted((round(float(sp.re(sp.N(r_["root_expr"], 30))), 9), round(float(sp.im(sp.N(r_["root_expr"], 30))), 9),
                          r_["mult"], r_["nullity"]) for r_ in res["roots"])
            sigs.append(sig); strongs.append(res["strong"])
            conds.append(eig_cond(Pl, V, [(r_["root_expr"], r_["mult"]) for r_ in res["roots"]]) if res["strong"] else None)
        same_spec = all(s_ == sigs[0] for s_ in sigs)
        same_cond = all(c__ is not None for c__ in conds) and max(abs(c__ / conds[0] - 1) for c__ in conds) < mp.mpf(10)**-20
        T5[nm].append({"alpha": str(SIGN * a_), "c2": str(c_), "strong_all_dirs": all(strongs), "same_spectrum": bool(same_spec),
                       "cond": None if conds[0] is None else float(conds[0]), "cond_equal": bool(same_cond),
                       "max_rel_cond_spread": None if not same_cond else float(max(abs(c__ / conds[0] - 1) for c__ in conds)),
                       "spectrum_z": sigs[0]})
    r0_ = T5[nm][0]
    P(f"    {nm:3s}: same exact spectrum (roots, multiplicities, nullities) in all 6 directions at "
      f"{sum(r_['same_spectrum'] for r_ in T5[nm])}/18 points; strongly hyperbolic in every direction at "
      f"{sum(r_['strong_all_dirs'] for r_ in T5[nm])}/18; condition number equal across khat at {sum(r_['cond_equal'] for r_ in T5[nm])}/18")
    P(f"         point 1 spectrum at z (re, im, mult, nullity): {r0_['spectrum_z']};  condition number {r0_['cond']}")
OUT["numbers"]["T5"] = T5
t5_F2a = unit_ok and all(r_["same_spectrum"] and r_["strong_all_dirs"] and r_["cond_equal"] for r_ in T5["F2a"])
conds_F2a = [r_["cond"] for r_ in T5["F2a"] if r_["cond"]]
check("T5 F2a is uniformly diagonalisable in khat: at every point the 6 directions give the same exact real roots, complete "
      "eigenvectors and the same eigenvector-matrix condition number (eigenspace-orthonormal bases, relative spread < 1e-20)",
      f"{sum(r_['same_spectrum'] and r_['strong_all_dirs'] and r_['cond_equal'] for r_ in T5['F2a'])}/18; condition numbers "
      + (f"{min(conds_F2a):.3e} .. {max(conds_F2a):.3e}" if conds_F2a else "n/a"), t5_F2a,
      "rotation covariance about the aether: the bound is direction-independent; it grows with c_S as alpha_c -> 0")
SH_F2a = F2a_all and t5_F2a
SH_F2b = F2b_all and all(r_["same_spectrum"] and r_["strong_all_dirs"] and r_["cond_equal"] for r_ in T5["F2b"])
SH_F1 = F1_all and all(r_["same_spectrum"] and r_["strong_all_dirs"] and r_["cond_equal"] for r_ in T5["F1"])

# ============================================================================================ COND + C5
banner("COND  THE CONDITIONS (symbolic), and C5 the c_S = 1 probe")
COND = {}
for nm in FORMS:
    Pf, Vf = SYMP[nm]
    Pz = Pf.xreplace({XI[0]: lam, XI[1]: 0, XI[2]: 0, XI[3]: 1})
    blks, _, _ = helicity_blocks(Pz, Vf)
    Ps = blks["scalar"]; lapse = None
    if not FORMS[nm][1]:
        Ps, lapse = schur_lapse(Ps, 0)
    A_s = Ps.applyfunc(lambda e_: sp.Poly(e_, lam).coeff_monomial(lam**2))
    detA = sp.factor(A_s.det())
    rk_gen = Ps.xreplace({lam: 1}).rank(simplify=True); rk_b0 = Ps.xreplace({lam: 1, be: 0}).rank(simplify=True)
    gmult = 4 if nm == "F1" else 2
    vec = blks["vector1"]; rv_gen = vec.xreplace({lam: 1}).rank(simplify=True); rv_b0 = vec.xreplace({lam: 1, be: 0}).rank(simplify=True)
    COND[nm] = {"lapse_coeff": None if lapse is None else str(sp.factor(lapse)), "detA_scalar": str(detA),
                "scalar_null_at_1_generic": Ps.rows - rk_gen, "scalar_null_at_1_beta0": Ps.rows - rk_b0, "scalar_mult_at_1": gmult,
                "vector_null_at_1_generic": 2 - rv_gen, "vector_null_at_1_beta0": 2 - rv_b0, "vector_mult_at_1": 2}
    P(f"    {nm:3s}: lapse coefficient {COND[nm]['lapse_coeff']};  det A (scalar block{', after lapse elimination' if lapse is not None else ''}) = {detA}")
    P(f"         at the gauge speed lambda = 1: scalar nullity {Ps.rows - rk_gen} (beta generic) / {Ps.rows - rk_b0} (beta = 0) vs "
      f"multiplicity {gmult};  vector nullity {2 - rv_gen} / {2 - rv_b0} vs 2")
# C5: c_S^2 = 1 at beta = 0, c_2 = c2_max -> alpha = c_2/(1 + 2 c_2)
c2p = sp.Rational(1, 15); a5 = c2p / (1 + 2 * c2p)
cs2_5 = CS2.subs({al: a5, be: 0, c2: c2p})
res5, strong5, _ = exact_point("F2a", a5, c2p)
r5s = [(r_["root"], r_["mult"], r_["nullity"]) for r_ in res5["scalar"]["roots"]]
P(f"    C5 probe (F2a): alpha = {a5}, c_2 = {c2p}, beta = 0 -> c_S^2 = {cs2_5};  scalar roots (root, mult, nullity): {r5s};  strong: {strong5}")
COND["C5"] = {"alpha": str(a5), "c2": str(c2p), "cS2": str(cs2_5), "roots": r5s, "strong": strong5}
OUT["numbers"]["COND"] = COND
f2a = COND["F2a"]
cond_ok = (f2a["scalar_null_at_1_beta0"] == f2a["scalar_mult_at_1"] and f2a["vector_null_at_1_beta0"] == 2
           and f2a["scalar_null_at_1_generic"] < f2a["scalar_mult_at_1"] and cs2_5 == 1
           and sp.simplify(sp.sympify(f2a["detA_scalar"], locals={"alpha": al, "beta": be, "c_2": c2})
                           + al * (be - 1) * (be + 3 * c2 + 2) / (2 * al - 1)) == 0
           and sp.simplify(sp.sympify(f2a["lapse_coeff"], locals={"alpha": al}) - (2 * al - 1) / 4) == 0)
check("COND F2a's conditions, derived: lapse elliptic iff alpha != 1/2 (gauge term); leading matrix invertible iff alpha (1-beta)"
      "(2+beta+3c_2) != 0 (det A); complete eigenvectors at the gauge speed iff beta = 0 (scalar and vector blocks); C5: at "
      "c_S^2 = 1 the merged eigenvalue stays semisimple, so c_S = 1 is NOT an extra condition in F2a",
      f"F2a: {f2a}; C5 (alpha = 1/17, c_2 = 1/15): roots {r5s}, strong = {strong5}", cond_ok,
      "beta = 0 is the chassis value (c_T = 1 exactly, L340), so the condition is met; for beta != 0 this gauge degenerates "
      "(tensor speed != gauge speed) and another gauge would be needed")

# ============================================================================================ C2 minimal Horava
banner("C2  CONTROL: minimal Horava gravity (alpha = 0, beta = 0, c_2 = c2_max)")
C2res = {}
for nm in ("F1", "F2a"):
    res0, strong0, lapse0 = exact_point(nm, sp.Integer(0), rat(C2_MAX))
    C2res[nm] = {"strong": strong0, "A_inv_scalar": res0["scalar"]["A_invertible"], "degree": res0["scalar"]["degree"],
                 "n": res0["scalar"]["n"], "lapse": None if lapse0 is None else str(lapse0)}
    P(f"    {nm}: scalar block leading matrix invertible {res0['scalar']['A_invertible']} (det degree {res0['scalar']['degree']} "
      f"vs 2n = {2 * res0['scalar']['n']}); strongly hyperbolic: {strong0}")
c2_ok = all((not v_["strong"]) and (not v_["A_inv_scalar"]) for v_ in C2res.values())
OUT["numbers"]["C2"] = C2res
check("C2 minimal Horava (alpha = 0) is NOT strongly hyperbolic in F1 or F2a, for the predicted reason: the scalar's xi_0^2 "
      "coefficient vanishes (singular leading matrix; the mode obeys an equation first order in time -- Jacobson & Pulakkat 2025)",
      f"{C2res}", c2_ok)

# ============================================================================================ T6 general frozen background
banner("T6  A GENERAL FROZEN BACKGROUND: lapse 13/10, shift (1/5, -1/10, 1/7), non-diagonal gamma_ij, tau = t")
Nl = sp.Rational(13, 10); Nsh = sp.Matrix([sp.Rational(1, 5), sp.Rational(-1, 10), sp.Rational(1, 7)])
GAM = sp.Matrix([[1, sp.Rational(1, 5), 0], [sp.Rational(1, 5), sp.Rational(6, 5), sp.Rational(1, 10)], [0, sp.Rational(1, 10), sp.Rational(9, 10)]])
Nlow = GAM * Nsh
GB = sp.zeros(4, 4); GB[0, 0] = -Nl**2 + (Nsh.T * GAM * Nsh)[0]
for i in range(3):
    GB[0, i + 1] = GB[i + 1, 0] = Nlow[i]
    for j in range(3):
        GB[i + 1, j + 1] = GAM[i, j]
spd = all(GAM[:i, :i].det() > 0 for i in (1, 2, 3))       # Sylvester: gamma_ij positive definite
a6, c6 = rat(AC_MAX) * SIGN, rat(C2_MAX)
k6 = [sp.Rational(1, 3), sp.Rational(-2, 5), sp.Rational(3, 4)]
s6 = sp.Symbol("s", positive=True)
qk = (sp.Matrix(k6).T * GAM.inv() * sp.Matrix(k6))[0]
Nk = sum(Nsh[i] * k6[i] for i in range(3))
cs2_6 = CS2.subs({al: a6, be: 0, c2: c6})
T6 = {}
for nm in ("F1", "F2a"):
    Lf, Vf = form_lagrangian(nm, GB, DT, a6, 0, c6)
    P6 = (symbol_matrix(Lf, Vf) / sp.sqrt(-GB.det())).applyfunc(sp.expand)      # every term carries sqrt(-g): divide it out
    m1 = 10 if nm == "F1" else 8
    quos, rems = {}, {}
    for sv in (1, 2):                                   # the magnitude s of the spatial covector: s = 1 and s = 2
        P6s = P6.xreplace({XI[0]: lam, XI[1]: sv * k6[0], XI[2]: sv * k6[1], XI[3]: sv * k6[2]}).applyfunc(sp.expand)
        det6 = det_poly(P6s, lam).as_expr()
        cone1 = (lam - sv * Nk)**2 - Nl**2 * sv**2 * qk
        coneS = (lam - sv * Nk)**2 - Nl**2 * cs2_6 * sv**2 * qk
        quo, rem = sp.div(sp.Poly(det6, lam), sp.Poly(sp.expand(cone1**m1 * coneS), lam))
        quos[sv], rems[sv] = quo.as_expr(), rem
    rem = rems[1] if rems[2].is_zero else rems[2]
    quo_e = quos[1]
    ell_ok = all(r_.is_zero for r_ in rems.values()) and all(sp.Poly(q_, lam).degree() == 0 and q_ != 0 for q_ in quos.values()) \
        and sp.simplify(quos[2] / quos[1] - 4) == 0
    P6s = P6.xreplace({XI[0]: lam, XI[1]: s6 * k6[0], XI[2]: s6 * k6[1], XI[3]: s6 * k6[2]}).applyfunc(sp.expand)
    # numerical strong hyperbolicity at s = 1 (pencil in lambda; F2a: eliminate ker A)
    Pl = P6s.xreplace({s6: 1})
    A = Pl.applyfunc(lambda e_: sp.Poly(e_, lam).coeff_monomial(lam**2))
    B = Pl.applyfunc(lambda e_: sp.Poly(e_, lam).coeff_monomial(lam))
    C = Pl.applyfunc(lambda e_: sp.Poly(e_, lam).coeff_monomial(1))
    kerA = A.nullspace()
    if kerA:
        Kv = sp.Matrix.hstack(*kerA)
        comp = sp.Matrix.hstack(*[v_ for v_ in (A.columnspace())])
        Sb = sp.Matrix.hstack(comp, Kv)
        Ap, Bp, Cp = (Sb.T * A * Sb), (Sb.T * B * Sb), (Sb.T * C * Sb)
        nk = Kv.cols; nr = Sb.cols - nk
        lam_free = all(Ap[i, j] == 0 and Bp[i, j] == 0 for i in range(nr, nr + nk) for j in range(nr, nr + nk))
        Pk = Cp[nr:, nr:]
        Prk_B, Prk_C = Bp[:nr, nr:], Cp[:nr, nr:]
        Pki = Pk.inv()
        A2 = Ap[:nr, :nr] - Prk_B * Pki * Prk_B.T
        B2 = Bp[:nr, :nr] - (Prk_B * Pki * Prk_C.T + Prk_C * Pki * Prk_B.T)
        C2m = Cp[:nr, :nr] - Prk_C * Pki * Prk_C.T
        lapse_note = f"ker A dim {nk}, its block lambda-free {lam_free}, invertible {Pk.det() != 0}"
    else:
        A2, B2, C2m, lapse_note = A, B, C, "A invertible"
    n2 = A2.rows
    Pl2 = (A2 * lam**2 + B2 * lam + C2m).applyfunc(sp.expand)
    real6 = bool(qk > 0 and cs2_6 > 0)
    roots6 = [(Nk + sg * Nl * sp.sqrt(qk), m1) for sg in (1, -1)] + [(Nk + sg * Nl * sp.sqrt(qk * cs2_6), 1) for sg in (1, -1)]
    nulls6 = []
    if real6:
        A_, B_, C_ = [to_mp(X_) for X_ in abc_exact(Pl2)]
        for r_, m_ in roots6:
            lv = mp.mpf(str(sp.N(r_, 80)))
            nulls6.append((float(lv), m_, len(null_basis_mp(A_ * lv**2 + B_ * lv + C_))))
    comp6 = real6 and all(x[1] == x[2] for x in nulls6)
    detA2 = A2.det() != 0
    pred = sorted(float(sp.N(r_, 30)) for r_, _ in roots6) if real6 else []
    got = sorted(round(x[0], 9) for x in nulls6)
    T6[nm] = {"cone_division_exact": bool(rem.is_zero), "quotient": str(quo_e), "elliptic_factor_s2": bool(ell_ok),
              "real": real6, "complete": comp6, "A_invertible_after_reduction": bool(detA2), "roots_mult_nullity": nulls6,
              "predicted": [round(x, 9) for x in pred], "lapse": lapse_note}
    P(f"    {nm}: det P = [cone_1]^{m1} [cone_S] x q(s), remainders zero at s = 1, 2: {all(r_.is_zero for r_ in rems.values())};  "
      f"q lambda-free with q(2)/q(1) = {sp.nsimplify(quos[2] / quos[1]) if quos[1] != 0 else 'n/a'} (leaf-elliptic, ~ s^2 gamma^ij k_i k_j): {ell_ok}")
    P(f"         at s = 1 ({lapse_note}; reduced A invertible {detA2}): roots N^i k_i +- N s_A |k|_gamma (value, multiplicity, nullity) "
      f"{[(round(x[0], 9), x[1], x[2]) for x in nulls6]};  real {real6}, complete {comp6}")
t6_ok = spd and all(v_["cone_division_exact"] and v_["elliptic_factor_s2"] and v_["real"] and v_["A_invertible_after_reduction"]
                    for v_ in T6.values()) and T6["F2a"]["complete"]
OUT["numbers"]["T6"] = T6
check("T6 on a general frozen background (lapse, shift, non-diagonal gamma) every characteristic factor is a cone "
      "(xi_0 - N^i k_i)^2 = N^2 s_A^2 gamma^{ij} k_i k_j with s_A in {1, c_S}, the left-over factor is the leaf-elliptic "
      "gamma^{ij} k_i k_j; the roots are real; F2a's eigenvectors are complete there too (F1 keeps its gauge-sector Jordan "
      "block, see SH-F1)",
      "; ".join(f"{k_}: exact {v_['cone_division_exact']}, elliptic {v_['elliptic_factor_s2']}, real {v_['real']}, complete {v_['complete']}"
                for k_, v_ in T6.items()), t6_ok if not MUTATE else (spd and all(v_["cone_division_exact"] for v_ in T6.values())),
      "the principal symbol at any point depends only on (g, d tau) there: the aligned computation is the general frozen one")

# ============================================================================================ T7 non-leaf slicing
banner("T7  A SLICING THAT IS NOT THE KHRONON'S: aether boosted v = 3/5 relative to coordinate time (F1, flat metric)")
gam7 = sp.Rational(5, 4); vb = sp.Rational(3, 5)
u_dn = [-gam7, gam7 * vb, 0, 0]
dtau7 = [-u_dn[m] for m in R4]
Lf7, Vf7 = form_lagrangian("F1", ETA, dtau7, rat(AC_MAX) * SIGN, 0, rat(C2_MAX))
P7 = symbol_matrix(Lf7, Vf7).xreplace({XI[0]: lam, XI[1]: 0, XI[2]: 1, XI[3]: 0}).applyfunc(sp.expand)
det7 = det_poly(P7, lam)
hfac = sp.Poly((gam7**2 - 1) * lam**2 + 1, lam)                  # h^{mu nu} xi xi for xi = (lambda, 0, 1, 0)
q7, r7 = sp.div(det7, hfac)
fac7 = sp.factor_list(q7.as_expr(), lam)[1] if r7.is_zero else []
rts7 = sum(([f_] * m_ for f_, m_ in fac7 if sp.Poly(f_, lam).degree() > 0), [])
deg7 = sum(sp.Poly(f_, lam).degree() for f_ in rts7)
real_rest = bool(fac7) and all(len(sp.real_roots(sp.Poly(f_, lam))) == sp.Poly(f_, lam).degree() for f_, _ in fac7
                               if sp.Poly(f_, lam).degree() > 0)
nonreal_h = sp.Poly(hfac, lam).nroots()
fac7_rows = [(sp.Poly(f_, lam).degree(), m_, len(sp.real_roots(sp.Poly(f_, lam))) == sp.Poly(f_, lam).degree()) for f_, m_ in fac7
             if sp.Poly(f_, lam).degree() > 0]
cS7 = CS2.subs({al: rat(AC_MAX) * SIGN, be: 0, c2: rat(C2_MAX)})
Qdt = {"light cone (s = 1)": gam7**2 - (gam7**2 - 1), "scalar cone (s = c_S)": gam7**2 - cS7 * (gam7**2 - 1)}
P(f"    k perpendicular to v: det P divisible by h(xi, xi) = (gamma^2 - 1) lambda^2 + 1: {r7.is_zero};  its roots {nonreal_h} (non-real);  "
  f"the remaining {deg7} roots (exact factorisation, Sturm count) all real: {real_rest}")
P(f"    remaining factors (degree, multiplicity, all roots real): {fac7_rows}")
P(f"    Q_A(dt) = (u.dt)^2 - s_A^2 h(dt, dt) for the coordinate time: " + ", ".join(f"{k_}: {float(v_):.4g}" for k_, v_ in Qdt.items())
  + "  -> dt lies outside the superluminal scalar cone's dual: t = const is not spacelike for that mode either")
OUT["numbers"]["T7"] = {"divisible": bool(r7.is_zero), "h_roots": [str(x) for x in nonreal_h], "rest_all_real": bool(real_rest),
                        "rest_factors": fac7_rows, "Q_dt": {k_: str(v_) for k_, v_ in Qdt.items()}}
check("T7 relative to a time function other than tau the leaf-elliptic factor h^{mu nu} xi_mu xi_nu has non-real roots "
      "(k perpendicular to the boost): the evolution must be posed on tau-leaves, i.e. the preferred time of criterion B is forced",
      f"divisible {r7.is_zero}; h roots {nonreal_h}", r7.is_zero and all(abs(sp.im(x)) > 0.1 for x in nonreal_h),
      "found too: the light-cone factors stay real-rooted (Q(dt) = 1 > 0), but the superluminal scalar cone also gives non-real "
      "roots in this slicing, since Q_S(dt) = gamma^2 - c_S^2 (gamma^2 - 1) < 0; a Cauchy slice must lie inside every cone's dual, "
      "which for c_S ~ 1e3-1e6 forces slices within ~1/c_S of the leaves")

# ============================================================================================ CB criterion B
banner("CB  CRITERION B: one preferred time compatible with every characteristic cone")
uS = sp.symbols("u0:4"); xS = sp.symbols("x0:4")
sA = sp.Symbol("s_A", positive=True)
# aligned frame: u = (1,0,0,0), h = diag(0,1,1,1); d tau = (1,0,0,0) (N = 1)
hmat = sp.diag(0, 1, 1, 1); u_up = sp.Matrix([1, 0, 0, 0]); dtv = sp.Matrix([1, 0, 0, 0])
Qa = lambda xi_: (u_up.T * xi_)[0]**2 - sA**2 * (xi_.T * hmat * xi_)[0]
q_dt = sp.simplify(Qa(dtv))
h_ev = hmat.eigenvals()
kernel_ok = (hmat * dtv) == sp.zeros(4, 1) and h_ev == {0: 1, 1: 3}
xi_s = sp.Matrix(sp.symbols("e0:4", real=True))
Hs = -(u_up.T * xi_s)[0]**2 + sA**2 * (xi_s.T * hmat * xi_s)[0]
ray = sp.Matrix([sp.diff(Hs, xi_s[m]) for m in R4])
dtau_ray = sp.simplify((dtv.T * sp.diag(1, 1, 1, 1) * ray)[0])          # d tau(xdot) = xdot^0 in the aligned frame
# on the cone, u.xi = 0 forces h(xi, xi) = 0, hence xi = 0: no ray is tangent to a leaf
cone_on = sp.solve(sp.Eq(Hs, 0), xi_s[0])
tangent = [sp.simplify(dtau_ray.subs(xi_s[0], c_)) for c_ in cone_on]
spd_ok = all(sp.simplify(t_**2 - 4 * sA**2 * (xi_s[1]**2 + xi_s[2]**2 + xi_s[3]**2)) == 0 for t_ in tangent)
speeds = sorted(set([1.0] + [r_["c_S"] for r_ in SH["F2a"] if r_["c_S"]]))
finite_pos = (not MUTATE) and all(r_["real"] for r_ in SH["F2a"]) and all(0 < s_ < math.inf for s_ in speeds)
P(f"    Q_A(d tau) = {q_dt} > 0 for every finite s_A: every leaf is spacelike for every finite cone, however superluminal")
P(f"    h^{{mu nu}}: eigenvalues {h_ev}, kernel = span(d tau) (only the leaf itself is characteristic for the elliptic factor): {kernel_ok}")
P(f"    ray d tau(xdot) = {dtau_ray};  on the cone (d tau(xdot))^2 = 4 s_A^2 |k|^2 > 0 for k != 0: {spd_ok} -> no characteristic ray "
  "is tangent to a leaf; each cone's two sheets lie on opposite sides; parametrised forward they move forward in tau")
P(f"    characteristic speeds found (F2a, all 18 points, aether frame): gauge/tensor 1, scalar {min(speeds[1:]) if len(speeds) > 1 else 'n/a'} "
  f".. {max(speeds) if speeds else 'n/a'} c; all real, positive, finite: {finite_pos}")
OUT["numbers"]["CB"] = {"Q_dtau": str(q_dt), "kernel_ok": kernel_ok, "ray_dtau": str(dtau_ray), "speeds_range": [min(speeds), max(speeds)],
                        "finite_positive": finite_pos}
check("CB criterion B holds on the tested scope: every cone is (u.xi)^2 = s_A^2 h(xi,xi) with the common axis u and 0 < s_A^2 < "
      "inf (tensor/gauge 1, scalar speeds as measured at the 18 points), so every leaf is spacelike for every cone and no ray points backward in tau; "
      "the leaf-elliptic factor's only characteristic conormal is d tau (instantaneous propagation within a leaf, allowed)",
      f"Q(d tau) = {q_dt}; kernel {kernel_ok}; transversality {spd_ok}; speeds finite and positive {finite_pos} "
      f"(scalar {min(speeds[1:]) if len(speeds) > 1 else float('nan'):.4g} .. {max(speeds):.4g} c)",
      q_dt == 1 and kernel_ok and spd_ok and finite_pos and t6_ok,
      "no closed causal curves follows once tau is a global time function (X > 0 everywhere), which C-H/K assumes by construction")

# ============================================================================================ C4 preview + verdict
banner("VERDICT (frozen decision rule, FROZEN_CRITERIA.md sec. 6)")
if not MUTATE:
    resm, strongm, _ = exact_point("F2a", -rat(AC_MAX), rat(C2_MAX))
    P(f"    C4 preview in this run (non-load-bearing): alpha_c -> -alpha_c at (alpha_max, c2_max): F2a strongly hyperbolic {strongm}; "
      f"scalar roots real {resm['scalar']['real']}")
    OUT["numbers"]["C4_preview"] = {"strong": strongm, "scalar_real": resm["scalar"]["real"]}
r0_ok = OUT["checks"][[k_ for k_ in OUT["checks"] if k_.startswith("R0")][0]]["ok"]
controls_ok = gr_ok and c2_ok and c3_ok
phys_real = all(r_["real"] for nm in FORMS for r_ in SH[nm])
conditional = (SH_F2a or SH_F2b) and SH_F1 and same_speeds and t6_ok and OUT["checks"][[k_ for k_ in OUT["checks"] if k_.startswith("CB")][0]]["ok"] \
    and r0_ok and controls_ok
kill = controls_ok and not phys_real
open_rule = (phys_real and not (SH_F1 or SH_F2a or SH_F2b)) or (not controls_ok) or (not r0_ok)
if MUTATE:
    verdict = "MUTATE RUN (C4): " + ("the verdict formulation FAILS, as required" if not SH_F2a else "the verdict formulation did NOT fail -- C4 FAILED")
elif conditional:
    verdict = "CONDITIONAL"
elif kill:
    verdict = "KILL"
elif open_rule:
    verdict = "OPEN"
else:
    verdict = ("OPEN (frozen-rule fall-through: the CONDITIONAL rule also required F1 to be strongly hyperbolic and it is not -- a "
               "gauge-sector Jordan block -- while the leaf-sliced F2a that sec. 2 designated to carry the verdict IS strongly "
               "hyperbolic; neither the KILL nor the OPEN clause applies as written; a post-hoc reading would be CONDITIONAL)")
OUT["verdict"] = verdict
OUT["summary"] = {"SH_F1": SH_F1, "SH_F2a": SH_F2a, "SH_F2b": SH_F2b, "same_physical_speeds_F1_F2a": same_speeds, "controls_ok": controls_ok,
                  "R0": r0_ok, "T6": t6_ok, "physical_speeds_real": phys_real}
P(f"""  F2a strongly hyperbolic (T2-T5): {SH_F2a};  F2b: {SH_F2b};  F1: {SH_F1};  same physical speeds F1/F2a: {same_speeds}
  controls C1/C2/C3: {gr_ok}/{c2_ok}/{c3_ok};  R0: {r0_ok};  T6: {t6_ok};  physical speeds real: {phys_real}
  VERDICT: {verdict}
  Scope: linearised, frozen-coefficient, high-frequency principal symbol; F2a = khronon time t = tau, spatial harmonic
  coordinates (spatial components of the de Donder condition), lapse from its leaf-elliptic equation; backgrounds whose
  filtered MOND field does not vanish.  Conditions found: alpha_c != 0 (with c_S^2 > 0: alpha_c > 0 for c_2 > 0), beta = 0
  in this gauge (c_T = 1), c_S^2 = c_2(2 - alpha_c)/(alpha_c(2 + 3 c_2)) finite and positive, alpha_c != 1/2 (a gauge artefact);
  c_S = 1 is not an extra condition (C5).
  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_pass"], OUT["n_fail_load_bearing"] = len(CH), sum(1 for _, ok, _ in CH if ok), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
