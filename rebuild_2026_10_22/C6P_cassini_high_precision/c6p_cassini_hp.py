#!/usr/bin/env python3
"""C6P_cassini_high_precision -- high-precision rerun of C6's failed check C2 and of the v3s Solar-System gate.

Criteria: FROZEN_CRITERIA.md (committed alone first, 3da94262c4).
Run:  OMP_NUM_THREADS=1 nice -n 19 python3 -I c6p_cassini_hp.py [--mutate] [--tag TAG]
      --mutate: nu == 1 twin (A_law == 0 in the QUMOND known answer; J = I in both Route F methods). Must break H4, H5.
C6's code (covariant_push_2026_10_22/C6_literal_cassini/c6_solver.py, and D7d's solver through it) is imported read-only,
with bytecode writing off. Deterministic, no network, single thread, < 1 GB. kappa = 1/2 FITTED; footings never pooled;
not theory closed. Adopts nothing (owner 11-04 lift); the 10-24 v3s verdict stands.
"""
import os, sys, json, math, time
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
np.seterr(all="ignore")
import mpmath as mp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "../.."))
C6DIR = os.path.join(ROOT, "covariant_push_2026_10_22", "C6_literal_cassini")
sys.path.insert(0, C6DIR)
import c6_solver as C          # read-only
S = C.S                         # D7d solver, read-only

MUT = "--mutate" in sys.argv
TAG = (sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else "") + ("_MUTATE" if MUT else "")
OUT, RES, CHK = [], {"mutate": MUT}, {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def T(s): print(f"  [{s}; {time.time() - t0:.0f}s]", file=sys.stderr, flush=True)   # timing to stderr only (rerun byte-identity)
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"{name} {'PASS' if ok else 'FAIL'} {msg}")
def J_(p): return json.load(open(os.path.join(ROOT, p)))
def ms(v, d=25): return mp.nstr(v, d)
t0 = time.time()

# ---------------------------------------------------------------- inputs (read-only from the record)
GM = 1.32712440018e20; AU = 1.495978707e11; PC = 3.0857e16
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}          # exact footings (AX1)
FOOT_C6 = {"canonical": 9.36e-11, "alt": 1.13e-10}           # C6 / D7c footings (reproduction only)
BAND_H = (-3.0e-27, 9.0e-27); BAND_P = (-2.0e-27, 5.2e-27)
GAMMA_BAND = (2.1e-5 - 2 * 2.3e-5, 2.1e-5 + 2 * 2.3e-5); R_MAX_GAMMA = 11.0 * AU
LSTARS = [24.0, 50.0, 90.0]; EFS = ["E0", "E1", "E2", "E3"]
PLANETS = {"Earth": (1.0 * AU, 8.7e-15), "Mars": (1.524 * AU, 1.4e-15), "Saturn": (9.58 * AU, 7.0e-15)}
GNE_E0 = 6.913e-11
D7B = J_("doors_push_2026_10_22/D7b_cassini_Q2/d7b_cassini_q2_results.json")
D7C = J_("doors_push_2026_10_22/D7c_q2_rar_gate/d7c_q2_rar_gate_results.json")
C6J = J_("covariant_push_2026_10_22/C6_literal_cassini/c6_literal_cassini_results.json")
GE_D7B = {f: {E: v["ge_total"] for E, v in D7B["grid"][f]["none"].items()} for f in FOOT}
def A_law(y): y = np.maximum(np.asarray(y, float), 1e-300); return (2.0 / y) / (np.sqrt(1.0 + 4.0 / y) + 1.0)
def ge_of(foot, a0, E):
    if E == "E0": return GNE_E0 * (1.0 + float(A_law(np.array([GNE_E0 / a0]))[0]))
    return GE_D7B[foot][E]
XE = {f: {E: ge_of(f, FOOT[f], E) / FOOT[f] for E in EFS} for f in FOOT}
XE_C6 = {f: {E: GE_D7B[f][E] / FOOT_C6[f] for E in EFS} for f in FOOT}
RES["inputs"] = dict(GM=GM, footings=FOOT, footings_C6=FOOT_C6, band_Hees=BAND_H, band_Park=BAND_P, gamma_band=GAMMA_BAND,
                     r_max_gamma_AU=11.0, Lstar_pc=LSTARS, planets=PLANETS, x_e=XE, x_e_C6=XE_C6)
P("=" * 100)
P("C6P_cassini_high_precision: C6's C2 at 30/50/80 digits + analytic rewrite; v3s Solar-System gate, both footings" + ("  [MUTATE nu=1]" if MUT else ""))
P("kappa = 1/2 FITTED; footings never pooled; not blind; adopts nothing; not theory closed.")
P("=" * 100)
P("x_e (exact footings): " + "; ".join(f"{f} " + ", ".join(f"{E} {XE[f][E]:.6f}" for E in EFS) for f in FOOT))

# ---------------------------------------------------------------- kernels
def chiA_gen(k, c, x, rF):      # C6's chi_gen, line for line, in mpmath
    s = mp.sqrt(max(1 - c * c, mp.mpf(0))); jp = 1 + x; jl = (1 + x) ** 2
    al = rF * k ** 2 / 2; be = (1 - rF) * k ** 2 / 2 - 1
    Axx = al + jp + be * s * s; Azz = al + jl + be * c * c; Axz = be * s * c
    return (s * s * Azz + c * c * Axx - 2 * s * c * Axz) / (Axx * Azz - Axz ** 2)
def chiA_d7d(k, c, x):          # D7d's chi, line for line, in mpmath
    jp = 1 + x; jl = (1 + x) ** 2; a = k ** 2 / 2 + jp; b = jl - jp; s2 = 1 - c * c
    A11 = a + b * c * c - 1; A22 = a + b * s2; A12 = b * c * mp.sqrt(s2)
    return A22 / (A11 * A22 - A12 ** 2)
def chiA_closed(k, c, x):       # C6's chi_C6_closed in mpmath
    m = (1 - c * c) / (1 + x) + c * c / (1 + x) ** 2
    return m / (1 - m + k ** 2 * m / 2)
def chiB0(k, c, x):             # Method B, r_F = 0 (works for float or mpf)
    q = k * k / 2; s2 = 1 - c * c
    return (1 + x * s2) / (x * (1 + x + c * c) + q * (1 + x * s2))
def chiB1(k, c, x):             # Method B, r_F = 1
    q = k * k / 2; s2 = 1 - c * c; b = x * (1 + x)
    return (q + 1 + x + b * s2) / ((q + x) * (q + 1 + x) + b * (q + x + c * c))

# ---------------------------------------------------------------- H1 sympy
import sympy as sy
kap, c_, x_ = sy.symbols("kappa c x", positive=True); s_ = sy.sqrt(1 - c_ ** 2); kh = sy.Matrix([s_, c_])
Jm = sy.diag(1 + x_, (1 + x_) ** 2); I2m = sy.eye(2)
def gen_sym(rF): return sy.simplify((kh.T * ((kap ** 2 / 2) * (rF * (I2m - kh * kh.T) + kh * kh.T) + Jm - kh * kh.T).inv() * kh)[0])
q_ = kap ** 2 / 2
r0 = sy.simplify(gen_sym(0) - (1 + x_ * (1 - c_ ** 2)) / (x_ * (1 + x_ + c_ ** 2) + q_ * (1 + x_ * (1 - c_ ** 2))))
b_ = x_ * (1 + x_)
r1 = sy.simplify(gen_sym(1) - (q_ + 1 + x_ + b_ * (1 - c_ ** 2)) / ((q_ + x_) * (q_ + 1 + x_) + b_ * (q_ + x_ + c_ ** 2)))
m_ = (1 - c_ ** 2) / (1 + x_) + c_ ** 2 / (1 + x_) ** 2
rm = sy.simplify(1 / m_ - 1 - x_ * (1 + x_ + c_ ** 2) / (1 + x_ * (1 - c_ ** 2)))
M, Ls = sy.symbols("m ell", positive=True)          # ell = 1 - m > 0
rk = sy.simplify(kap ** 2 * M / ((1 - M) + kap ** 2 * M / 2) - 2 - (-2 * (1 - M) / ((1 - M) + kap ** 2 * M / 2)))
ik = sy.simplify(sy.integrate(-2 * Ls / (Ls + kap ** 2 * M / 2), (kap, 0, sy.oo)) + sy.pi * sy.sqrt(2 * Ls / M))
ok1 = all(sy.simplify(r) == 0 for r in (r0, r1, rm, rk, ik))
check("H1", ok1, f"sympy residuals: B(r_F=0)-general {r0}; B(r_F=1)-general {r1}; 1/m-1 factorisation {rm}; kappa^2 chi-2 {rk}; kappa integral {ik} (all 0)")
T("H1")

# ---------------------------------------------------------------- H2/H3 C2 rerun
kk = np.logspace(-3, 3, 61); cc = np.linspace(-0.999, 0.999, 41); kk2 = np.logspace(-2, 3, 51)
XS_D7D = (0.3, 1.15, 2.6, 5.0); XS_AQ = (0.3, 1.0, 1.9, 2.6, 5.0); XS_CL = (0.3, 1.15, 2.6)
def c2_items(chi_gen, chi_d7d, chi_cl, conv, absf):
    w_d7d = max(absf(chi_gen(conv(k), conv(c), conv(x), 1) - chi_d7d(conv(k), conv(c), conv(x))) for x in XS_D7D for k in kk for c in cc)
    w_aq = 0
    for x in XS_AQ:
        X = conv(x); mu = X / (1 + X); L0 = 1 / (1 + X)
        w_aq = max(w_aq, max(absf(1 + chi_gen(conv(0.0), conv(c), X, 0) - 1 / (mu * (1 + L0 * conv(c) ** 2))) for c in cc))
    w_iso = max(absf(chi_gen(conv(k), conv(c), conv(0.0), 0) / chi_gen(conv(k), conv(c), conv(0.0), 1) - 1) for k in kk2 for c in cc)
    w_cl = max(absf(chi_gen(conv(k), conv(c), conv(x), 0) - chi_cl(conv(k), conv(c), conv(x))) for x in XS_CL for k in kk for c in cc)
    return dict(rF1_vs_D7d=w_d7d, kappa0_vs_AQUAL=w_aq, isolated_rF0_vs_rF1_rel=w_iso, rF0_vs_closed=w_cl)
# float C6 (vectorised exactly as C6 did) for H3/H4
kkv = kk[:, None]; ccv = cc[None, :]
f_d7d = max(float(np.max(np.abs(C.chi_gen(kkv, ccv, x, 1.0) - S.chi(kkv, ccv, x)))) for x in XS_D7D)
f_aq = 0.0
for x in XS_AQ:
    mu = x / (1 + x); L0 = 1 / (1 + x); f_aq = max(f_aq, float(np.max(np.abs(1 + C.chi_gen(0.0, cc, x, 0.0) - 1 / (mu * (1 + L0 * cc ** 2))))))
f_iso = float(np.max(np.abs(C.chi_gen(kk2[:, None], ccv, 0.0, 0.0) / C.chi_gen(kk2[:, None], ccv, 0.0, 1.0) - 1)))
f_cl = max(float(np.max(np.abs(C.chi_gen(kkv, ccv, x, 0.0) - C.chi_C6_closed(kkv, ccv, x)))) for x in XS_CL)
FLOAT_C6 = dict(rF1_vs_D7d=f_d7d, kappa0_vs_AQUAL=f_aq, isolated_rF0_vs_rF1_rel=f_iso, rF0_vs_closed=f_cl)
# Method B in float64: the general kernel is replaced by its stable rewrite (B0 at r_F = 0, B1 at r_F = 1). The references
# are C6's own float expressions where they do not cancel (D7d chi at x_e >= 0.3, the linear-AQUAL formula, the closed
# form at x_e >= 0.3); the x_e = 0 item compares B0 with B1 (both exactly 2/kappa^2 there).
B_items = dict(
    rF1_vs_D7d=max(float(np.max(np.abs(chiB1(kkv, ccv, x) - S.chi(kkv, ccv, x)))) for x in XS_D7D),
    kappa0_vs_AQUAL=max(float(np.max(np.abs(1 + chiB0(0.0, cc, x) - 1 / ((x / (1 + x)) * (1 + cc ** 2 / (1 + x)))))) for x in XS_AQ),
    isolated_rF0_vs_rF1_rel=float(np.max(np.abs(chiB0(kk2[:, None], ccv, 0.0) / chiB1(kk2[:, None], ccv, 0.0) - 1))),
    rF0_vs_closed=max(float(np.max(np.abs(chiB0(kkv, ccv, x) - C.chi_C6_closed(kkv, ccv, x)))) for x in XS_CL))
H2 = {"float_C6_general": FLOAT_C6, "method_B_float64": B_items, "method_A": {}}
DPS = [30, 50, 80]
if not MUT:
    for d in DPS:
        mp.mp.dps = d
        it = c2_items(chiA_gen, chiA_d7d, chiA_closed, lambda v: mp.mpf(float(v)), abs)
        H2["method_A"][str(d)] = {k: ms(v, 6) for k, v in it.items()}
        H2["method_A"][f"{d}_max"] = float(max(it.values()))
        T(f"C2 method A at {d} digits")
    mp.mp.dps = 80
    # H3: locate the float error: float general kernel vs 80-digit literal kernel at x_e = 0
    e0 = e1 = 0.0; where = None
    for k in kk2:
        for c in cc:
            K, Cc = mp.mpf(float(k)), mp.mpf(float(c))
            a0h = chiA_gen(K, Cc, mp.mpf(0), 0); a1h = chiA_gen(K, Cc, mp.mpf(0), 1)
            d0 = float(abs(float(C.chi_gen(k, c, 0.0, 0.0)) / a0h - 1)); d1 = float(abs(float(C.chi_gen(k, c, 0.0, 1.0)) / a1h - 1))
            if d0 > e0: e0, where = d0, (float(k), float(c))
            e1 = max(e1, d1)
    H2["H3_float_error_vs_80digits"] = dict(rF0_general_max_rel=e0, at_kappa_c=where, rF1_general_max_rel=e1,
                                             exact_value_both_kernels="2/kappa^2 (Method B, x_e = 0)")
    okA = all(H2["method_A"][f"{d}_max"] < 1e-12 for d in DPS)
    okB = max(B_items.values()) < 1e-12
    check("H2", okA and okB, "C2 four sub-items, max over items: Method A " + ", ".join(f"{d} digits {H2['method_A'][f'{d}_max']:.1e}" for d in DPS) +
          f"; Method B float64 {max(B_items.values()):.1e} (" + ", ".join(f"{k} {v:.1e}" for k, v in B_items.items()) + ") (< 1e-12)")
    rel3 = abs(f_iso / C6J["C2"]["isolated_rF0_vs_rF1_rel"] - 1)
    check("H3", rel3 <= 1e-6 and max(e0, e1) >= 1e-12,
          f"C6 float x_e=0 r_F=0 vs r_F=1 recomputed {f_iso:.4e} vs C6 JSON {C6J['C2']['isolated_rF0_vs_rF1_rel']:.4e} (rel {rel3:.1e} <= 1e-6); "
          f"float error vs 80 digits: general r_F=0 {e0:.2e} at (kappa, c) = ({where[0]:.3g}, {where[1]:.3g}), general r_F=1 {e1:.2e} (>= 1e-12: failure located)")
RES["H2_C2"] = H2

# ---------------------------------------------------------------- Route F I2: Method B (closed form) and Method A (literal, nested)
def I2_B(x):
    x = mp.mpf(x)
    f = lambda c: (3 * c * c - 1) / 2 * mp.sqrt(x * (1 + x + c * c) / (1 + x * (1 - c * c)))
    return -5 * mp.pi / mp.sqrt(2) * 2 * mp.quad(f, [0, mp.mpf(1) / 2, 1])
def c2_tail(x):
    x = mp.mpf(x); return 5 * mp.quad(lambda c: (x * (1 + x + c * c) / (1 + x * (1 - c * c))) * (3 * c * c - 1) / 2, [0, 1])
KMAX = mp.mpf(10) ** 7
def I2_A(x):
    x = mp.mpf(x)
    inner = lambda k: 5 * mp.quad(lambda c: chiA_gen(k, c, x, 0) * (3 * c * c - 1) / 2, [0, mp.mpf(1) / 2, 1])
    pts = [0] + [mp.mpf(10) ** e for e in range(-2, 8)]
    return mp.quad(lambda k: k * k * inner(k), pts) - 4 * c2_tail(x) / KMAX
def Q2_of(I2, L): return -2 * GM / (5 * math.pi * L ** 3) * I2

XEF = {f: {E: (0.0 if MUT else XE[f][E]) for E in EFS} for f in FOOT}
XEF_C6 = {f: {E: (0.0 if MUT else XE_C6[f][E]) for E in EFS} for f in FOOT}
IB, IA = {}, {}
for d in DPS:
    mp.mp.dps = d
    IB[d] = {f"{f}|{E}": I2_B(XEF[f][E]) for f in FOOT for E in EFS}
T("I2 method B ladder")
if not MUT:
    for d in DPS:
        mp.mp.dps = d
        IA[d] = {}
        for f in FOOT:
            for E in EFS:
                IA[d][f"{f}|{E}"] = I2_A(XEF[f][E])
        T(f"I2 method A at {d} digits")
mp.mp.dps = 80
RES["I2"] = {"method_B": {str(d): {k: ms(v, 30) for k, v in IB[d].items()} for d in DPS},
             "method_A": {str(d): {k: ms(v, 30) for k, v in IA[d].items()} for d in IA}}
if not MUT:
    h6 = max(float(abs(IA[d][k] / IB[d][k] - 1)) for d in DPS for k in IB[d])
    check("H6", h6 <= 1e-14, f"Method A (literal kernel, nested, 80/50/30 digits) vs Method B (closed form), 8 fields x 3 precisions: max rel {h6:.1e} (<= 1e-14)")
    lb = max(float(abs(IB[d][k] / IB[80][k] - 1)) for d in (30, 50) for k in IB[80])
    la = max(float(abs(IA[d][k] / IA[80][k] - 1)) for d in (30, 50) for k in IA[80])
    fall = all(H2["method_A"][f"{d}_max"] <= 10.0 ** (-(d - 10)) for d in DPS)
    check("H7", lb <= 1e-25 and la <= 1e-14 and fall,
          f"ladder 30/50 vs 80 digits: Method B max rel {lb:.1e} (<= 1e-25), Method A {la:.1e} (<= 1e-14); C2 max per rung " +
          ", ".join(f"{d}: {H2['method_A'][f'{d}_max']:.1e} (<= 1e-{d - 10})" for d in DPS))
    RES["H6_A_vs_B_max_rel"] = h6; RES["H7_ladder"] = dict(B=lb, A=la)

# ---------------------------------------------------------------- H4 C6 float reproduction where nothing cancels
mp.mp.dps = 50
d4 = max(abs(FLOAT_C6[k] - C6J["C2"][k]) for k in ("rF1_vs_D7d", "kappa0_vs_AQUAL", "rF0_vs_closed"))
q_float, q_B, rr = [], [], []
for f in FOOT:
    for L in LSTARS:
        for E in EFS:
            ref = C6J["R1_physical"][f"{f}|{L:g}|{E}"]["Q2"]
            qf = float(C.routeF_Q2(GM, L * PC, XEF_C6[f][E], 0.0)); qb = Q2_of(float(I2_B(XEF_C6[f][E])), L * PC)
            q_float.append(abs(qf / ref - 1)); q_B.append(abs(qb / ref - 1) if qb != 0 else 1.0)
for f in FOOT:
    for L in LSTARS:
        for pl, (r, bnd) in PLANETS.items():
            vals = [float(C.routeF_radial(GM, L * PC, XE_C6[f][E], r, 0.0)) for E in EFS]
            rr.append(abs(max(abs(v) for v in vals) / bnd / C6J["R2_planets"][f"{f}|{L:g}|{pl}"]["ratio"] - 1))
RES["H4"] = dict(C2_nocancel_max_abs_diff=d4, R1_float_max_rel=max(q_float), R1_methodB_max_rel=max(q_B), R2_float_max_rel=max(rr))
check("H4", d4 <= 1e-15 and max(q_float) <= 1e-12 and max(q_B) <= 1e-8 and max(rr) <= 1e-12,
      f"C2 non-cancelling float items vs C6 JSON |d| {d4:.1e} (<= 1e-15); C6 float R1 Q2, 24 cells, rel {max(q_float):.1e} (<= 1e-12); "
      f"Method B 50 digits vs C6 R1 rel {max(q_B):.1e} (<= 1e-8); C6 float R2 ratios rel {max(rr):.1e} (<= 1e-12)")
T("H4")

# ---------------------------------------------------------------- H5 QUMOND known answer (AX1 K1)
Afun = (lambda y: np.zeros_like(np.asarray(y, float))) if MUT else A_law
def q_int(A, eta, nr=20000, nm=200, rmin=1e-7, rmax=1e5):
    u = np.linspace(math.log(rmin), math.log(rmax), nr); r = np.exp(u); mu, w = np.polynomial.legendre.leggauss(nm)
    g = (1.0 / r ** 2)[:, None]; Mx = mu[None, :]
    a = A(np.sqrt(eta * eta + g * g + 2 * eta * g * Mx))
    f = (a * (eta * (3 * Mx - 5 * Mx ** 3) + g * (1 - 3 * Mx * Mx))) @ w
    return 1.5 * float(np.trapz(f / r, u))
GE_KIN = {"E1": 1.9 * 9.36e-11, "E2": 2.2 * 9.36e-11, "E3": 2.6 * 9.36e-11}
def eta_of(A, a0, E):
    if E == "E0": return GNE_E0 / a0
    t = GE_KIN[E] / a0; return brentq(lambda x: x * (1.0 + float(A(np.array([x]))[0])) - t, 1e-8, t)
h5 = []
for f, a0 in FOOT_C6.items():
    for E in EFS:
        ref = D7C["Q2"]["L"][f]["Q2"][E]; v = abs(q_int(Afun, eta_of(Afun, a0, E))) * 1.5 * a0 / math.sqrt(GM / a0); h5.append(abs(v / ref - 1))
RES["H5_max_rel"] = max(h5)
check("H5", max(h5) <= 1e-2, f"plain QUMOND law Q2 vs D7c 'L' (PAPER58 QUMOND), 8 cells, max rel {max(h5):.2e} (<= 1e-2)")
T("H5")

# ---------------------------------------------------------------- H8, H9
h8 = max(abs(ge_of(f, FOOT_C6[f], "E0") / GE_D7B[f]["E0"] - 1) for f in FOOT)
check("H8", h8 <= 1e-12, f"g_e(E0) recomputed at C6's a0 vs D7b, both footings, rel {h8:.1e} (<= 1e-12)")
mars24 = GM / (24 * PC) ** 2 / 1.4e-15
check("H9", abs(mars24 / 0.173 - 1) <= 2e-2, f"hedgehog Mars at 24 pc {mars24:.4f} of bound vs AX1/C6 0.173 (rel {abs(mars24 / 0.173 - 1):.1e} <= 2e-2)")
if MUT:
    allzero = all(IB[d][k] == 0 for d in DPS for k in IB[d])
    check("M1", (not CHK["H4"]) and (not CHK["H5"]) and allzero, f"MUTATE bites: H4 {CHK['H4']}, H5 {CHK['H5']}, every screened Q2 = 0: {allzero}")

# ---------------------------------------------------------------- GATE (exact footings)
P("")
P("GATE (exact footings; Method B at 80 digits; Q2 BN11/Hees sign)")
GATE = {}
for f in FOOT:
    g = dict(G2a={}, G2b={}, G2c={}, R3={})
    for L in LSTARS:
        for E in EFS:
            q = Q2_of(IB[80][f"{f}|{E}"], mp.mpf(L * PC))
            g["G2a"][f"{L:g}|{E}"] = dict(Q2=ms(q, 20), Q2_f=float(q), hees=bool(BAND_H[0] <= q <= BAND_H[1]), park=bool(BAND_P[0] <= q <= BAND_P[1]),
                                          over_Hees_upper=float(q / BAND_H[1]), over_Park_upper=float(q / BAND_P[1]))
        hh = mp.mpf(GM) / mp.mpf(L * PC) ** 2
        for pl, (r, bnd) in PLANETS.items():
            mono = [float(C.routeF_radial(GM, L * PC, XEF[f][E], r, 0.0)) for E in EFS] if not MUT else [0.0]
            g["G2b"][f"{L:g}|{pl}"] = dict(hedgehog_over_bound=float(hh / bnd), routeF_monopole_over_bound=max(abs(v) for v in mono) / bnd)
        gam = 2 * (R_MAX_GAMMA / (L * PC)) ** 2
        g["G2c"][f"{L:g}"] = dict(structural="gamma = 1, alpha1 = alpha2 = 0 at beta = 0 (record X15 / A22, carried)", proxy_abs_gamma_minus_1=gam,
                                  inside=bool(GAMMA_BAND[0] <= gam <= GAMMA_BAND[1] and GAMMA_BAND[0] <= -gam <= GAMMA_BAND[1]))
        if not MUT:
            s20 = 20e3 * AU; GMb = 1.5 * GM
            g["R3"][f"{L:g}"] = [math.sqrt(1 + float(C.routeF_radial(GMb, L * PC, XEF[f][E], s20, 0.0)) / (GMb / s20 ** 2)) - 1 for E in EFS]
    qs = [v["Q2_f"] for v in g["G2a"].values()]
    ok2a = all(v["hees"] and v["park"] for v in g["G2a"].values())
    ok2b = all(v["hedgehog_over_bound"] < 1 and v["routeF_monopole_over_bound"] < 1 for v in g["G2b"].values())
    ok2c = all(v["inside"] for v in g["G2c"].values())
    g["summary"] = dict(Q2_min=min(qs), Q2_max=max(qs), margin_Hees_min=BAND_H[1] / max(abs(q) for q in qs) if max(qs) > 0 else None,
                        margin_Park_min=BAND_P[1] / max(abs(q) for q in qs) if max(qs) > 0 else None,
                        worst_planet=max(g["G2b"].items(), key=lambda kv: max(kv[1].values()))[0],
                        worst_planet_ratio=max(max(v.values()) for v in g["G2b"].values()),
                        gamma_proxy_max=max(v["proxy_abs_gamma_minus_1"] for v in g["G2c"].values()), G2a=ok2a, G2b=ok2b, G2c=ok2c)
    GATE[f] = g
    sm = g["summary"]
    for L in LSTARS:
        row = [g["G2a"][f"{L:g}|{E}"]["Q2_f"] for E in EFS]
        P(f"  {f:9s} L*={L:3.0f} pc  Q2 E0-E3 = " + " ".join(f"{q:.4e}" for q in row) +
          f"  max/9.0e-27 {max(row) / 9e-27:.2e}  max/5.2e-27 {max(row) / 5.2e-27:.2e}  | planets (hedgehog / Route F mono): " +
          ", ".join(f"{pl} {g['G2b'][f'{L:g}|{pl}']['hedgehog_over_bound']:.4f}/{g['G2b'][f'{L:g}|{pl}']['routeF_monopole_over_bound']:.4f}" for pl in PLANETS) +
          f"  | |gamma-1| proxy {g['G2c'][f'{L:g}']['proxy_abs_gamma_minus_1']:.2e}" +
          ("" if MUT else "  | R3 gamma_v-1 " + " ".join(f"{v:.3e}" for v in g["R3"][f"{L:g}"])))
    P(f"  {f:9s} G2a {'PASS' if ok2a else 'FAIL'} (Q2 {sm['Q2_min']:.3e} to {sm['Q2_max']:.3e}; Hees margin >= {sm['margin_Hees_min'] or float('nan'):.3e}, Park >= {sm['margin_Park_min'] or float('nan'):.3e}); "
      f"G2b {'PASS' if ok2b else 'FAIL'} (worst {sm['worst_planet']} {sm['worst_planet_ratio']:.4f}); G2c {'PASS' if ok2c else 'FAIL'} (proxy <= {sm['gamma_proxy_max']:.2e}, band [-2.5e-5, 6.7e-5])")
RES["gate"] = GATE

# ---------------------------------------------------------------- labels
allok = all(CHK.values())
LAB = {}
for f in FOOT:
    sm = GATE[f]["summary"]
    if MUT or not allok: LAB[f] = "still UNDECIDED (failed checks: " + ", ".join(k for k, v in CHK.items() if not v) + ")"
    elif sm["G2a"] and sm["G2b"] and sm["G2c"]: LAB[f] = "PASS"
    else: LAB[f] = "FAIL [" + ", ".join(k for k in ("G2a", "G2b", "G2c") if not sm[k]) + "]"
RES["labels"] = LAB; RES["checks"] = CHK
P("")
P(f"CHECKS {sum(CHK.values())}/{len(CHK)} PASS: " + ", ".join(f"{k} {'P' if v else 'F'}" for k, v in CHK.items()))
P("LABELS: " + "; ".join(f"{f} {v}" for f, v in LAB.items()))
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, mp.mpf): return ms(o, 30)
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, f"c6p_cassini_hp{TAG}.json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, f"c6p_cassini_hp{TAG}.out"), "w").write("\n".join(OUT) + "\n")
T("done")
sys.exit(0 if (allok and not MUT) else 1)
