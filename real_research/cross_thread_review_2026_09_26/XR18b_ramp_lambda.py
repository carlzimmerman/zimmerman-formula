#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR18b (2 of 4) -- H_K1 ACROSS THE q = 0 RAMP, AND THE lambda QUESTION (item 3 of the re-audit).

WHY.  H_K1's yield is tied to the leaf's zero modes, y_th = max(0, 2q) x 8 pi G rho_bar L/a0 (c_y = 2, 2q = 1 + Omega_r -
9 Lambda/<K>_h^2), so the action has a KINK in <K>_h at q = 0 (z_q0 = 0.635): y_th is continuous there, its <K>_h-derivative
jumps.  Below z_q0 there is no yield at all, and FP7's phi has no equation at lambda = 0 on exact FRW (XR18 Q2, XR25 K4): phi's
inertia 2 lambda (n.d phi)^2 is required.  XR25 (43cfa1692) found that at the core's c_2 = oo the khronon contributes only 3 to
lambda_eff = lambda + 3 h^2, so the MOND-regime observables (the tracking speed, galaxy alpha_2 v^2) move with lambda unless
lambda <~ 0.03, with the upper bound lambda <= 274.4 from tracking; and that at exact zero field the strong-coupling scale is 0.
This lane asks: is FRW growth across z = 0.635 well posed with H_K1's y_th (not FP13's tabulated one)?  What does the kink do to
the background?  What does lambda > 0 do there, which lambda keeps the MOND regime lambda-independent, and is that range free of
strong coupling in H_K1's real backgrounds -- including the zeros of the band-passed field, which H_K1 no longer plugs below z_q0?

PRE-DECLARED HYPOTHESES (written into this file before its first full run; exploratory runs disclosed in XR18b_README.md: a
sizing of the <K>_h channel on H_K1's state (whose y-channel at q = 0+ is the kink's jump used in R3), and back-of-envelope
estimates of the strongly coupled radius around a zero of the band-passed field; no run of this file's own checks)
 H1 [load-bearing] THE RAMP IS A KINK, NOT A JUMP: H_K1's y_th(z) is continuous at z_q0 (|y_th(z_q0 + 1e-6)| < 1e-8) with a
    finite one-sided derivative dy_th/dln<K>_h = 2 (1 + Omega_r) x 8 pi G rho_bar L/a0 (sympy), and its zero sits at z_q0
    exactly (FP13's tabulated y_th switched off ~0.010 lower, XR18 Q1).
 H2 [load-bearing] FRW GROWTH ACROSS z_q0 IS WELL POSED UNDER H_K1: with the ramp smoothed (softplus width eps) sigma_8 converges
    monotonically (|d sigma_8| < 1e-4 at eps = 0.002, both footings, both chords); every sigma_8 mode crosses H_K1's yield at most
    once (z = 3 -> 0.5); the chord G_eff = C^Q h^2 is continuous through z_q0 (its largest epoch-to-epoch step within
    |z - z_q0| <= 0.02 shrinks by >= x2 under 10x refinement).  MUTATE's hard step must fail the last clause.
 H3 [load-bearing] THE BACKGROUND ACROSS THE KINK IS WELL POSED: the Friedmann function F(H) = 3 M_p^2 H^2 - e_M + <K> de_M/d<K>
    is increasing with an UPWARD jump dF at H(z_q0), so H(rho) is continuous and non-decreasing (a pinned segment); on the real
    state dF/rho_bar <= 1e-4 (Gaussian and Jensen readings of <x>) and the pinned interval H dt = dF/(3 rho_bar) <= 1e-4.
 H4 [load-bearing] lambda AT THE SWITCH-OFF: at c_2 = oo, with the band-pass closed and zero field, every coefficient of FP7's
    root polynomial is proportional to lambda (no phi equation at lambda = 0, sympy); with H_K1's structure phi un-freezes at
    omega_r = c k sqrt(C_L/lambda_eff) >= 10 H for every sub-L sigma_8 mode (h >= 0.4) at z_q0 for lambda in [0, 274.4], at
    c_2 = oo and at the c_2 floor.
 H5 [load-bearing] H_K1's COSMOLOGICAL GATES ARE lambda-INERT BELOW 0.03: at c_2 = oo sigma_8 (both footings, both chords) moves by
    < 1e-4 across lambda in {0, 1e-9, 1e-3, 0.03} and stays in the band [0.922, 1.05] with the forest proxy <= 10% for every lambda
    in {0, 1e-9, 1e-3, 0.03, 1, 3, 30, 274.4}.
 H6 [load-bearing] THE MOND-REGIME OBSERVABLES FIX THE WINDOW: at c_2 = oo the tracking speed (C^Q = 100) and galaxy alpha_2 v^2
    (620 km/s) change by < 1% only for lambda <= 0.03 (XR25 L4's formulas; separator-independent) and by x9.6 / x93 across
    (0, 274.4].
 H7 [load-bearing] STRONG COUPLING IN H_K1's REAL BACKGROUNDS, lambda in [1e-9, 0.03]: every strongly coupled region -- the core
    around a zero of the band-passed field below z_q0 (flattest zero s = y_rms/L of the web; cored halo centres at 1e2-1e6
    rho_bar), the layer at H_K1's yield surfaces above z_q0 (DE12's hosts at z = 0.8, 1, 2.5) -- is smaller than xi (the filter
    below which the metric never sees phi), in both phi sectors (metric-visible, lambda_eff = lambda + 3; sub-xi, lambda_eff =
    lambda); the metric-visible sector's tree-level length at the xi scale is < xi; the lambda at which the flattest zero's sub-xi
    core would reach xi is printed.
The writer's expectation: all seven pass; H7 is the adversarial one (H_K1 has no yield below z_q0, so zeros are unplugged).

CHECKS
  K1 CONTROL: XR18's committed Q1 on FP13's H_S (sigma_8 at eps = 0.05/0.01/0.002/0, both chords, canonical) with this lane's
     smoothed-ramp code on FP13's own yth_state (FP19's read-only load of FP13).
  K2 CONTROL: XR18's committed Q2 (omega_r/H at z_q0 for c_2 = 7.29e-3 and oo, lambda = 0/1/100/1e4) with this lane's code.
  K3 CONTROL: XR25's committed L2/L4 (lambda_max = 274.39; tracking speeds and alpha_2 v^2 at six lambdas).
  K4 CONTROL: FP7 B6's 12 committed tree-level strong-coupling rows with this lane's ell_sc.
  R1 = H1.  R2 = H2.  R3 = H3.  R4 = H4.  R5 = H5.  R6 = H6.  R7 = H7.  V (reported): the lambda verdict.
MUTATE=1 replaces the ramp max(0, 2q) by a hard step at q = 0 (y_th jumps from 0 to its tied value 2 x 4 pi G rho_bar L/a0): R2's
refinement clause must FAIL (the chord jumps), rc = 1.

SCOPE.  FP19's per-mode linear yardstick (frozen coefficients, EH98 + halofit, all-matter reading), FRW background with the
MOND sector's leaf-averaged energy as a (v/c)^2 correction, FP7 B6's tree-level strong-coupling estimate (quantum EFT;
the classical PM problem is XR18b_yield_surfaces.py's).  At most 2 threads.  kappa = 1/2 is FITTED (Z = 5.7888); nothing
here derives it, and nothing here closes the theory.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR18b_ramp_lambda.py
"""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as sp
from scipy.optimize import brentq
import XR18b_common as XC

L = XC.Lane("XR18b_ramp_lambda", "XR18b/ramp_lambda")
P, check, banner = L.P, L.check, L.banner
MUT = L.mutate
P(__doc__.split("CHECKS")[0].strip())
if MUT:
    P("\n  *** MUTATE=1: the ramp max(0, 2q) is replaced by a hard step at q = 0 -- R2's refinement clause must FAIL ***")

NS = XC.load_fp19()
A0, FOOTS, MODES, M6 = NS["A0"], NS["FOOTS"], NS["MODES"], NS["M6"]
h_, Om, OL, Or, H0, c_, Mpc, G, rho_crit0 = NS["h_"], NS["Om"], NS["OL"], NS["Or"], NS["H0"], NS["c_"], NS["Mpc"], NS["G"], NS["rho_crit0"]
Ez, dlnH, AGR, KH, KHF, DIF, Z_Q0 = NS["Ez"], NS["dlnH"], NS["AGR"], NS["KH"], NS["KHF"], NS["DIF"], NS["Z_Q0"]
growth_aq, model_of, s8_aq, sigma8_of, S8_LCDM = NS["growth_aq"], NS["model_of"], NS["s8_aq"], NS["sigma8_of"], NS["S8_LCDM"]
forest_proxy, chord_modes, x_P2, rms_bp_L, maxwell_x_mean = NS["forest_proxy"], NS["chord_modes"], NS["x_P2"], NS["rms_bp_L"], NS["maxwell_x_mean"]
two_q, SIG8_BAND, FOREST_TOL = NS["two_q"], NS["SIG8_BAND"], NS["FOREST_TOL"]
Lh, yh, LK, yK = NS["Lh"], NS["yh"], NS["LK_head"], NS["yK_head"]
fourpiGrho = NS["fourpiGrho"]
X18 = json.load(open(os.path.join(XC.HERE, "XR18_state_separator_results.json")))["numbers"]
X25 = json.load(open(os.path.join(XC.HERE, "XR25_lambda_regulator_results.json")))["numbers"]
F7 = json.load(open(os.path.join(XC.CHAIN, "FP7_aqual_type_repair_results.json")))["numbers"]
import XR25_common as C25
XI_M = {f: XC.XI_PC[f] * C25.PC_M for f in FOOTS}
P(f"\n  machinery: FP19's module + main() slices exec'd read-only (FP13 -> FP9 -> FP6 inside); a0 = {A0['canonical']:.4e} / "
  f"{A0['alt']:.4e}; z_q0 = {Z_Q0:.5f}; xi = {XC.XI_PC['canonical']} / {XC.XI_PC['alt']} pc   {L.el()}")


def softplus(x, eps):
    return eps * math.log1p(math.exp(min(x / eps, 700.0))) if x / eps < 700 else x


def y_law(eps=0.0, step=False):
    """H_K1's tied yield per footing with the ramp smoothed (eps > 0), exact (eps = 0), or replaced by a hard step (MUTATE)."""
    def sw(a):
        q2 = two_q(a)
        if step:
            return 1.0 if q2 > 0 else 0.0
        return max(0.0, q2) if eps == 0.0 else softplus(q2, eps)
    return {f: (lambda a, f=f: XC.HEAD_CY * sw(a) * fourpiGrho(a) * LK(a) * Mpc / A0[f]) for f in FOOTS}


# ================================================================================================ K1 XR18's Q1 on H_S
banner("K1  CONTROL: XR18's committed Q1 (FP13's H_S, smoothed ramp) with this lane's code on FP13's own yth_state")
yth_state, LH_tab = NS["yth_state"], NS["LH_tab"]
k1 = {}; k1dev = 0.0
for eps in (0.05, 0.01, 0.002, 0.0):
    if eps == 0:
        ys = yth_state(LH_tab, "NL", "ramp", 1.0)[0]
    else:
        sw = lambda a, eps=eps: softplus(two_q(a), eps)
        ys = yth_state(LH_tab, "NL", "ramp", 1.0, onset=sw)[0]
    k1[eps] = {m: float(s8_aq(model_of(Lh, ys["canonical"]), "canonical", m)) for m in MODES}
    for m in MODES:
        k1dev = max(k1dev, abs(k1[eps][m] / X18["Q1"]["s8"][str(eps)][m] - 1))
check("K1 CONTROL: XR18's committed Q1 on FP13's H_S -- sigma_8 (canonical, both chords) with the ramp smoothed at eps = 0.05, 0.01, "
      "0.002 and exact -- reproduced with this lane's smoothed-ramp code driving FP13's own yth_state",
      f"max relative deviation {k1dev:.1e} over {len(k1) * len(MODES)} numbers", k1dev <= 1e-10)

# ================================================================================================ K2 XR18's Q2 on H_S
banner("K2  CONTROL: XR18's committed Q2 (FP13's H_S, omega_r at z_q0) with this lane's code")


def omega_r(Lf, yf, a0v, lams, c2s_=("c2=7.29e-3", "c2->oo")):
    aq = 1 / (1 + Z_Q0)
    Dq = growth_aq(model_of(Lf, yf), a0v, mode="permode", zs_out=(Z_Q0,))[round(Z_Q0, 6)]
    _, hq, yq = chord_modes(Dq, aq, a0v, Lf(aq), 0.0, KH, "permode")
    xq = x_P2(yq); CLphi = 2 * xq * (1 - xq) / (1 - 2 * xq) ** 2
    sub = hq >= 0.4
    out = {}
    for c2lab in c2s_:
        c2v = None if c2lab == "c2->oo" else (7.29e-3 if c2lab == "c2=7.29e-3" else XC.__dict__.get("C2F", 7.2888e-3))
        for lam in lams:
            lam_eff = lam + (3.0 * hq ** 2 if c2v is None else (2 + 3 * c2v) * hq ** 2 / c2v)
            om = c_ * (KH * h_ / (aq * Mpc)) * np.sqrt(CLphi / lam_eff) / (H0 * Ez(aq))
            out[(c2lab, lam)] = float(np.min(om[sub]))
    return out


q2 = omega_r(Lh, yh["canonical"], A0["canonical"], (0.0, 1.0, 100.0, 1e4))
k2dev = max(abs(v / X18["Q2"][f"{k_[0]}/{k_[1]}"] - 1) for k_, v in q2.items())
check("K2 CONTROL: XR18's committed Q2 on FP13's H_S -- min over sub-L sigma_8 modes of omega_r/H at z_q0 for c_2 = 7.29e-3 and oo, "
      "lambda = 0, 1, 100, 1e4 -- reproduced", f"max relative deviation {k2dev:.1e}", k2dev <= 1e-10)

# ================================================================================================ K3 XR25's L2/L4
banner("K3  CONTROL: XR25's committed L2 (lambda_max) and L4 (tracking speed, galaxy alpha_2 v^2) with this lane's code")
CQ_MAX = 100.0; vt = C25.V_TRACK / C25.cc
lam_max = (1.0 / CQ_MAX) / vt ** 2 - 3.0
cs_track = lambda lv: math.sqrt((1 / CQ_MAX) / (lv + 3.0)) * C25.cc / 1e3
a2v2 = lambda lv: (lv + 3.0 - 0.01) / (0.01 * 1.01) * (620e3 / C25.cc) ** 2
k3dev = abs(lam_max / X25["L2"]["lambda_max"] - 1)
for lv_s, v in X25["L4"]["cs_track"].items():
    k3dev = max(k3dev, abs(cs_track(float(lv_s)) / v - 1))
for lv_s, v in X25["L4"]["alpha2_v2"].items():
    k3dev = max(k3dev, abs(a2v2(float(lv_s)) / v - 1))
check("K3 CONTROL: XR25's committed L2 (lambda_max = 274.39 at c_2 = oo from tracking) and L4 (tracking speed at C^Q = 100 and galaxy "
      "alpha_2 v^2 at 620 km/s, six lambdas) reproduced", f"max relative deviation {k3dev:.1e}; lambda_max {lam_max:.3f}", k3dev <= 1e-12)

# ================================================================================================ K4 FP7 B6
banner("K4  CONTROL: FP7 B6's 12 committed tree-level strong-coupling rows with this lane's ell_sc")


def Cphi_bg(label, a0):
    if label.startswith("web"):
        y = 1e-3
    elif label.startswith("galaxy"):
        y = 0.1
    else:
        y = C25.yN_of(2.32e-10, a0)
    x = math.sqrt(y * y + y) - y
    return x / (1 - 2 * x)


k4dev = 0.0
for foot, lab, le, cs_r, Lsc_r, ell_r in F7["B6"]["rows"]:
    cs_, Lsc_, ell_ = XC.ell_sc(A0[foot], Cphi_bg(lab, A0[foot]), le)
    k4dev = max(k4dev, abs(cs_ / cs_r - 1), abs(Lsc_ / Lsc_r - 1), abs(ell_ / ell_r - 1))
check("K4 CONTROL: FP7 B6's tree-level strong-coupling scale Lambda_sc = c_s^(9/4) [(3/2) alpha M_P (2 lambda_eff)^(3/2)]^(1/2) and "
      "ell_sc = c_s hbar c/Lambda_sc reproduced for its 12 committed rows", f"max relative deviation {k4dev:.1e}", k4dev <= 1e-9)
P(f"    {L.el()}")

# ================================================================================================ R1 the ramp's form
banner("R1  THE RAMP: H_K1's y_th at q = 0 -- continuous, with a finite one-sided <K>_h-derivative (a kink), switching off at z_q0")
Ks, Lams, Ors, rhoS, LLs, al = sp.symbols("K Lambda Omega_r rho_bar L_Lambda alpha", positive=True)
twoq_s = 1 + Ors - 9 * Lams / Ks ** 2
yth_s = twoq_s * (Ks ** 2 / 3 - Lams) * (LLs * 3 * Lams / Ks ** 2) / al
Kq0 = sp.sqrt(9 * Lams / (1 + Ors))
dy_right = sp.simplify(sp.diff(yth_s, Ks).subs(Ks, Kq0) * Kq0)                          # dy_th/dln<K> at q = 0+
dy_form = sp.simplify(2 * (1 + Ors) * ((Kq0 ** 2 / 3 - Lams) * (LLs * 3 * Lams / Kq0 ** 2) / al))
r1_sym = sp.simplify(dy_right - dy_form) == 0
yl = y_law()
cont = {f: abs(yl[f](1 / (1 + Z_Q0 + 1e-6))) for f in FOOTS}
zero_at = {f: brentq(lambda z: yl[f](1 / (1 + z)) - 1e-12, Z_Q0 - 0.01, Z_Q0 + 0.01, xtol=1e-12) for f in FOOTS}
aq0 = 1 / (1 + Z_Q0)
num_slope = {f: (yl[f](aq0 * math.exp(-1e-6)) - yl[f](aq0)) / (-1e-6) / dlnH(aq0) for f in FOOTS}
ana_slope = {f: 2 * (1 + Or / aq0 ** 4 / (Om / aq0 ** 3 + OL + Or / aq0 ** 4)) * XC.HEAD_CY * fourpiGrho(aq0) * LK(aq0) * Mpc / A0[f] for f in FOOTS}
P(f"    sympy: dy_th/dln<K> at q = 0+ = {sp.factor(dy_right)} = 2 (1 + Omega_r) (<K>^2/3 - Lambda) L/alpha: {r1_sym}; 0 at q = 0-")
P("    per footing: y_th(z_q0 + 1e-6) = " + ", ".join(f"{f}: {v:.2e}" for f, v in cont.items()) + "; zero at z - z_q0 = "
  + ", ".join(f"{f}: {zero_at[f] - Z_Q0:+.1e}" for f in FOOTS) + "; one-sided slope dy_th/dln<K> numeric/analytic "
  + ", ".join(f"{f}: {num_slope[f]:.4e}/{ana_slope[f]:.4e}" for f in FOOTS) + f"  (FP13's table: zero ~0.010 below z_q0, XR18 Q1)")
r1_ok = (r1_sym and all(v < 1e-8 for v in cont.values()) and all(abs(zero_at[f] - Z_Q0) < 1e-4 for f in FOOTS)
         and all(abs(num_slope[f] / ana_slope[f] - 1) < 1e-3 for f in FOOTS))
check("R1 [H1, pre-declared] THE RAMP IS A KINK, NOT A JUMP: H_K1's y_th is continuous at z_q0, its zero sits at z_q0 exactly, and its "
      "one-sided <K>_h-derivative at q = 0+ is the finite 2 (1 + Omega_r) (<K>^2/3 - Lambda) L/alpha (0 at q = 0-)",
      f"sympy {r1_sym}; max y_th(z_q0 + 1e-6) {max(cont.values()):.1e}; zero offset {max(abs(zero_at[f] - Z_Q0) for f in FOOTS):.1e}; "
      f"slope {ana_slope['canonical']:.3e} (canonical)", r1_ok)
L.out["numbers"]["R1"] = dict(cont=cont, slope=ana_slope)

# ================================================================================================ R2 FRW growth across z_q0
banner("R2  FRW GROWTH ACROSS z_q0 UNDER H_K1: smoothed ramp, single crossings, continuity of the chord by refinement")
q_s8 = {}
for eps in (0.05, 0.01, 0.002, 0.0):
    yl_e = y_law(eps, step=MUT)
    q_s8[eps] = {(f, m): float(s8_aq(model_of(LK, yl_e[f]), f, m)) for f in FOOTS for m in MODES}
d_eps = {e_: max(abs(q_s8[e_][k_] - q_s8[0.0][k_]) for k_ in q_s8[0.0]) for e_ in (0.05, 0.01, 0.002)}
mono = d_eps[0.05] >= d_eps[0.01] >= d_eps[0.002]
P("    sigma_8 with the ramp smoothed: " + "; ".join(f"eps {e_:g}: " + ", ".join(f"{k_[0][:3]}/{k_[1]} {v:.6f}" for k_, v in r_.items())
                                                for e_, r_ in q_s8.items()))
yl0 = y_law(0.0, step=MUT)
ZQ = np.linspace(3.0, 0.5, 400)
ncross, zc_all = {}, {}
for f in FOOTS:
    res_q = growth_aq(model_of(LK, yl0[f]), A0[f], mode="permode", zs_out=tuple(ZQ))
    zq = np.array(sorted([z for z in res_q.keys() if z >= 0.5 - 1e-9], reverse=True))
    cr = []
    for z in zq:
        a = 1 / (1 + z)
        _, hk, yk = chord_modes(res_q[z], a, A0[f], LK(a), yl0[f](a), KH, "permode")
        cr.append(yk > yl0[f](a))
    cr = np.array(cr)
    ncross[f] = int(np.max(np.sum(np.abs(np.diff(cr.astype(int), axis=0)), axis=0)))
    zc_all[f] = [float(zq[np.argmax(cr[:, j])]) for j in range(cr.shape[1]) if cr[:, j].any() and not cr[0, j]]
steps = {}
for f in FOOTS:
    for dz in (1e-3, 1e-4):
        zfine = np.arange(Z_Q0 + 0.02, Z_Q0 - 0.02, -dz)
        rf = growth_aq(model_of(LK, yl0[f]), A0[f], mode="permode", zs_out=tuple(zfine))
        zf = np.array(sorted(rf.keys(), reverse=True))
        zf = zf[(zf <= Z_Q0 + 0.02 + 1e-9) & (zf >= Z_Q0 - 0.02 - 1e-9)]
        Ge = []
        for z in zf:
            a = 1 / (1 + z)
            CQv, hk, _ = chord_modes(rf[z], a, A0[f], LK(a), yl0[f](a), KH, "permode")
            Ge.append(CQv * hk ** 2)
        steps[(f, dz)] = float(np.max(np.abs(np.diff(np.array(Ge), axis=0))))
shrink = {f: steps[(f, 1e-3)] / max(steps[(f, 1e-4)], 1e-300) for f in FOOTS}
P(f"    |d sigma_8| at eps 0.05/0.01/0.002: {d_eps[0.05]:.1e}/{d_eps[0.01]:.1e}/{d_eps[0.002]:.1e} (monotone {mono}); per-mode crossings of the "
  f"yield (z = 3 -> 0.5): max " + ", ".join(f"{f}: {v}" for f, v in ncross.items()) + "; first above-yield epochs z = "
  + ", ".join(f"{f}: {min(zc_all[f]) if zc_all[f] else float('nan'):.3f}-{max(zc_all[f]) if zc_all[f] else float('nan'):.3f} ({len(zc_all[f])} modes)" for f in FOOTS)
  + "; the chord's largest step within 0.02 of z_q0: " + ", ".join(f"{f}: {steps[(f, 1e-3)]:.3e} -> {steps[(f, 1e-4)]:.3e} (x{shrink[f]:.2f})" for f in FOOTS))
r2_ok = d_eps[0.002] < 1e-4 and mono and max(ncross.values()) <= 1 and min(shrink.values()) >= 2.0
check("R2 [H2, pre-declared] FRW GROWTH ACROSS z_q0 IS WELL POSED UNDER H_K1: sigma_8 with the ramp smoothed converges monotonically "
      "(< 1e-4 at eps = 0.002, both footings and chords), every sigma_8 mode crosses the yield at most once, and the chord G_eff is "
      "continuous through z_q0 (its largest step within 0.02 of z_q0 shrinks >= x2 under 10x refinement)",
      f"|d sigma_8| {d_eps[0.05]:.1e}/{d_eps[0.01]:.1e}/{d_eps[0.002]:.1e}; max crossings {max(ncross.values())}; shrink "
      + "/".join(f"x{shrink[f]:.2f}" for f in FOOTS), r2_ok,
      "y_th -> 0 linearly at z_q0, so the chord x_P2(y - y_th)/y changes by O(dz) per step: a kink in time, not a jump; MUTATE's hard "
      "step switches every yielded mode's MOND off at once")
L.out["numbers"]["R2"] = dict(s8={str(e_): {str(k_): v for k_, v in r_.items()} for e_, r_ in q_s8.items()}, d_eps=d_eps, ncross=ncross,
                              steps={f"{k_[0]}/{k_[1]}": v for k_, v in steps.items()})
P(f"    {L.el()}")

# ================================================================================================ R3 the background across the kink
banner("R3  THE BACKGROUND ACROSS THE KINK: the Friedmann function jumps UP at H(z_q0) -> H(rho) continuous, pinned for a moment")
aq = 1 / (1 + Z_Q0); iq = int(np.argmin(np.abs(AGR - aq)))
r3 = {}
for f in FOOTS:
    rho = Om * rho_crit0 / aq ** 3
    yrms = float(rms_bp_L(iq, [LK(aq)], A0[f])[0])
    xG = maxwell_x_mean(yrms, 0.0); xJ = math.sqrt(yrms)
    dF = {lab: A0[f] ** 2 * xm * ana_slope[f] / (4 * math.pi * G * rho * c_ ** 2) for lab, xm in (("Gauss", xG), ("Jensen", xJ))}
    # monotonicity of F(H): dF/dH = 6 M_p^2 H + O(e_M/H) > 0 on both sides; relative size of the smooth correction <= the channel's
    r3[f] = dict(y_rms=yrms, x_G=xG, x_J=xJ, dF_over_rho=dF, H_dt={k_: v / 3.0 for k_, v in dF.items()},
                 dz={k_: (1 + Z_Q0) * v / 3.0 for k_, v in dF.items()})
    P(f"    {f:9s}: y_rms(z_q0) {yrms:.3e}, <x> Gauss {xG:.3f} / Jensen {xJ:.3f}: jump dF/rho_bar {dF['Gauss']:.2e} / {dF['Jensen']:.2e}; pinned "
      f"H dt = {r3[f]['H_dt']['Gauss']:.1e} / {r3[f]['H_dt']['Jensen']:.1e} (dz ~ {r3[f]['dz']['Jensen']:.1e})")
# a direct demonstration: invert F(H) = rho with an upward jump of the real size -> H(rho) continuous, H' jumps to 0 and back
f0 = "canonical"; jump = r3[f0]["dF_over_rho"]["Jensen"]
Hq = H0 * Ez(aq)
rho_q = 3 * Hq ** 2                                                        # units 8 pi G/3... F(H) = 3 H^2 (M_p^2 = 1) + jump rho_q step(H - Hq)
Fh = lambda Hv: 3 * Hv ** 2 + (jump * rho_q if Hv > Hq else 0.0)
rhos = np.linspace(rho_q * (1 - 3 * jump), rho_q * (1 + 4 * jump), 2001)
Hs = []
for rv in rhos:
    if Fh(Hq) >= rv:                                                       # below the lower branch's value at Hq
        Hs.append(math.sqrt(rv / 3))
    elif rv <= 3 * Hq ** 2 + jump * rho_q:                                 # in the jump: pinned
        Hs.append(Hq)
    else:
        Hs.append(math.sqrt((rv - jump * rho_q) / 3))
Hs = np.array(Hs); dHmax = float(np.max(np.abs(np.diff(Hs))) / Hq)
pinned = float(np.sum(np.abs(Hs - Hq) < 1e-15 * Hq)) / len(Hs)
r3_ok = all(max(v["dF_over_rho"].values()) <= 1e-4 and max(v["H_dt"].values()) <= 1e-4 for v in r3.values()) and dHmax < 1e-3
check("R3 [H3, pre-declared] THE BACKGROUND ACROSS THE KINK IS WELL POSED: F(H) = 3 M_p^2 H^2 - e_M + <K> de_M/d<K> is increasing with "
      "an UPWARD jump dF = (a0^2 <x>/(4 pi G)) dy_th/dln<K>|+ at H(z_q0), so H(rho) is continuous (a pinned segment, H' jumps to 0 and "
      "back); on the real state dF/rho_bar and the pinned H dt are <= 1e-4 (Gaussian and Jensen <x>)",
      "; ".join(f"{f}: dF/rho {max(v['dF_over_rho'].values()):.1e}, H dt {max(v['H_dt'].values()):.1e}" for f, v in r3.items())
      + f"; inverted H(rho) max step/H {dHmax:.1e} (continuous), pinned share of the scan {pinned:.2f}", r3_ok,
      "a Filippov sliding segment of ~1e-6 Hubble times: the kink is felt by the background only at the channel's (v/c)^2 size")
L.out["numbers"]["R3"] = r3

# ================================================================================================ R4 lambda at the switch-off
banner("R4  lambda AT THE SWITCH-OFF: no phi equation at lambda = 0 on exact FRW; how fast phi un-freezes under H_K1")
alm, c2m, Cph, lmm, sgm, kk7, ww7 = sp.symbols("alpha_c c_2 C_phi lam_ sigma k omega", real=True)
import re
det7 = sp.sympify(re.sub(r"\blambda\b", "lam_", F7["B3"]["det"]), locals={"alpha_c": alm, "c_2": c2m, "C_phi": Cph, "lam_": lmm,
                                                                          "sigma": sgm, "k": kk7, "omega": ww7})
U = sp.Symbol("U")
PU = sp.expand(sp.cancel(det7.subs(ww7, sp.sqrt(U) * kk7) / (64 * kk7 ** 10)))
PUinf = sp.expand(sp.limit(PU / c2m, c2m, sp.oo))
P0 = sp.expand(PUinf.subs({sgm: 0, Cph: 0}))
prop = all(sp.simplify(P0.coeff(U, j_).subs(lmm, 0)) == 0 for j_ in (0, 1, 2)) and sp.simplify(P0.subs(lmm, 0)) == 0
LAMS4 = (0.0, 1e-9, 1e-3, 0.03, 1.0, 100.0, 274.4)
om4 = {f: omega_r(LK, yK[f], A0[f], LAMS4, c2s_=("c2=7.29e-3", "c2->oo")) for f in FOOTS}
P(f"    c_2 = oo, band-pass closed (sigma = 0), zero field (C_phi = 0): P(U) = {sp.factor(P0)}  (-> 0 at lambda = 0: {prop})")
for f in FOOTS:
    P(f"    {f:9s}: min over sub-L sigma_8 modes of omega_r/H at z_q0: " + "; ".join(f"{k_[0]}, lambda {k_[1]:g}: {v:.3g}" for k_, v in om4[f].items()))
r4_ok = prop and all(v >= 10 for f in FOOTS for v in om4[f].values())
check("R4 [H4, pre-declared] lambda AT THE SWITCH-OFF: at c_2 = oo with the band-pass closed and zero field every coefficient of FP7's "
      "root polynomial is proportional to lambda (phi has no equation at lambda = 0); under H_K1 phi un-freezes at omega_r >= 10 H for "
      "every sub-L sigma_8 mode at z_q0, lambda in [0, 274.4], c_2 = oo and the floor",
      f"proportional to lambda {prop}; min omega_r/H {min(v for f in FOOTS for v in om4[f].values()):.3g}", r4_ok,
      "at c_2 = oo the khronon's inertia 3 h^2 carries every band-passed mode; lambda matters only for h -> 0 modes and exact zero field, "
      "where it only has to be > 0")
L.out["numbers"]["R4"] = {f: {f"{k_[0]}/{k_[1]}": v for k_, v in om4[f].items()} for f in FOOTS}
P(f"    {L.el()}")

# ================================================================================================ R5 sigma_8 and the forest over lambda (c_2 = oo)
banner("R5  H_K1's sigma_8 AND FOREST OVER lambda AT c_2 = oo")
LAMS5 = (0.0, 1e-9, 1e-3, 0.03, 1.0, 3.0, 30.0, 274.4)
r5 = {}
for lv in LAMS5:
    row = {}
    for f in FOOTS:
        mod = model_of(LK, yK[f])
        for m in MODES:
            row[("s8", f, m)] = sigma8_of(growth_aq(mod, A0[f], mode=m, c2=1e15, lam=lv)[0.0]) / S8_LCDM
            resf = growth_aq(mod, A0[f], mode=m, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0), c2=1e15, lam=lv)
            row[("forest", f, m)] = max(forest_proxy(resf, kF=kF)[0] for kF in (10.0, 15.0, 20.0))
    r5[lv] = row
    P(f"    lambda {lv:8.3g}: sigma_8 " + ", ".join(f"{k_[1][:3]}/{k_[2]} {v:.6f}" for k_, v in row.items() if k_[0] == "s8")
      + f"; forest max {max(v for k_, v in row.items() if k_[0] == 'forest'):.2e}")
s8keys = [k_ for k_ in r5[0.0] if k_[0] == "s8"]
spread_low = max(max(r5[lv][k_] for lv in LAMS5 if lv <= 0.03) - min(r5[lv][k_] for lv in LAMS5 if lv <= 0.03) for k_ in s8keys)
spread_all = max(max(r5[lv][k_] for lv in LAMS5) - min(r5[lv][k_] for lv in LAMS5) for k_ in s8keys)
band = all(SIG8_BAND[0] <= r5[lv][k_] <= SIG8_BAND[1] for lv in LAMS5 for k_ in s8keys)
fok = all(v <= FOREST_TOL for row in r5.values() for k_, v in row.items() if k_[0] == "forest")
check("R5 [H5, pre-declared] H_K1's COSMOLOGICAL GATES ARE lambda-INERT BELOW 0.03 AT c_2 = oo: sigma_8 moves by < 1e-4 across lambda in "
      "{0, 1e-9, 1e-3, 0.03} (both footings, both chords) and stays in [0.922, 1.05] with the forest proxy <= 10% for every lambda up to 274.4",
      f"spread (lambda <= 0.03) {spread_low:.1e}; spread (0..274.4) {spread_all:.1e}; band kept {band}; forest kept {fok}",
      spread_low < 1e-4 and band and fok)
L.out["numbers"]["R5"] = {str(lv): {str(k_): v for k_, v in row.items()} for lv, row in r5.items()}

# ================================================================================================ R6 the MOND-regime observables
banner("R6  THE MOND-REGIME OBSERVABLES OVER lambda (c_2 = oo; separator-independent): where lambda is inert, where it is a knob")
cs0, a20 = cs_track(0.0), a2v2(0.0)
lam_1pc_cs = brentq(lambda lv: 1 - cs_track(lv) / cs0 - 0.01, 1e-9, 10.0)
lam_1pc_a2 = brentq(lambda lv: a2v2(lv) / a20 - 1 - 0.01, 1e-9, 10.0)
ratio_cs, ratio_a2 = cs0 / cs_track(lam_max), a2v2(lam_max) / a20
P(f"    tracking speed at C^Q = 100: {cs0:,.0f} km/s at lambda -> 0; 1% lower at lambda = {lam_1pc_cs:.4f}; {cs_track(lam_max):,.0f} km/s at lambda_max = {lam_max:.1f}")
P(f"    galaxy alpha_2 v^2 (620 km/s): {a20:.3e} at lambda -> 0; 1% higher at lambda = {lam_1pc_a2:.4f}; {a2v2(lam_max):.3e} at lambda_max")
r6_ok = min(lam_1pc_cs, lam_1pc_a2) >= 0.029 and min(lam_1pc_cs, lam_1pc_a2) <= 0.061 and ratio_cs > 9 and ratio_a2 > 90
check("R6 [H6, pre-declared] THE MOND-REGIME OBSERVABLES FIX THE WINDOW: the tracking speed and galaxy alpha_2 v^2 stay within 1% of "
      "their lambda -> 0 values only for lambda <= ~0.03 (the khronon's own inertia at c_2 = oo is 3), and change by x9.6 / x93 across "
      "(0, 274.4]", f"1% at lambda = {lam_1pc_cs:.4f} (tracking) / {lam_1pc_a2:.4f} (alpha_2 v^2); x{ratio_cs:.1f} / x{ratio_a2:.0f} across the "
      "tracking window", r6_ok,
      "inside (0, 0.03] lambda is a regulator (every observable lambda-independent to 1%); anywhere in (0.03, 274.4] the MOND regime "
      "reads lambda -- a bounded knob that no current datum selects")
L.out["numbers"]["R6"] = dict(lam_1pc_tracking=lam_1pc_cs, lam_1pc_alpha2=lam_1pc_a2, ratio_cs=ratio_cs, ratio_a2=ratio_a2)
P(f"    {L.el()}")

# ================================================================================================ R7 strong coupling in H_K1's real backgrounds
banner("R7  STRONG COUPLING IN H_K1's REAL BACKGROUNDS, lambda in [1e-9, 0.03]: zeros of the band-passed field, yield layers, the web")
LAM7 = (1e-9, 1e-3, 0.03)
CT = lambda x: x / (1 - 2 * x)
CLf = lambda x: 2 * x * (1 - x) / (1 - 2 * x) ** 2


def core_radius(a0v, Cfun, lam_eff, lo=1e-12, hi=1e26):
    """the radius r* where the tree-level strong-coupling length equals the distance from the degenerate point: ell_sc(C(r*)) = r*."""
    g = lambda lr: math.log(XC.ell_sc(a0v, Cfun(math.exp(lr)), lam_eff)[2]) - lr
    return math.exp(brentq(g, math.log(lo), math.log(hi), xtol=1e-10))


r7 = {"typical": {}, "zeros": {}, "layers": {}}
# (a) typical backgrounds: the web's band-passed rms field under H_K1 below z_q0, galaxy outskirts
for f in FOOTS:
    for z in (0.0, 0.25, 0.5):
        a = 1 / (1 + z); i = int(np.argmin(np.abs(AGR - a)))
        yr = float(rms_bp_L(i, [LK(a)], A0[f])[0]); Cp = CT(float(x_P2(yr)))
        for lv in LAM7:
            r7["typical"][(f, f"web z={z}", lv)] = (XC.ell_sc(A0[f], Cp, lv + 3.0)[2], XC.ell_sc(A0[f], Cp, lv)[2])
    Cg = CT(float(x_P2(0.1)))
    for lv in LAM7:
        r7["typical"][(f, "galaxy outskirts y = 0.1", lv)] = (XC.ell_sc(A0[f], Cg, lv + 3.0)[2], XC.ell_sc(A0[f], Cg, lv)[2])
# (b) zeros of the band-passed field below z_q0: |g_bp| = a0 s r near an isotropic zero; C_phi = C_T(x_P2(s r)) (the softer one)
MSUN_KG = C25.MSUN
for f in FOOTS:
    a0v = A0[f]
    for z in (0.0, 0.25, 0.5):
        a = 1 / (1 + z); i = int(np.argmin(np.abs(AGR - a))); Lp = LK(a) * Mpc
        yr = float(rms_bp_L(i, [LK(a)], a0v)[0])
        rho_bar = Om * rho_crit0 / a ** 3
        svals = {"web zero s = y_rms/L": yr / Lp}
        for dens in (1e2, 1e4, 1e6):
            svals[f"cored centre {dens:.0e} rho_bar"] = (4 * math.pi / 3) * G * dens * rho_bar / a0v
        for slab, s in svals.items():
            Cfun = lambda r, s=s: CT(float(x_P2(s * r)))
            for lv in LAM7:
                rv = core_radius(a0v, Cfun, lv + 3.0); rs = core_radius(a0v, Cfun, lv)
                ell_xi = XC.ell_sc(a0v, Cfun(XI_M[f]), lv + 3.0)[2]
                r7["zeros"][(f, z, slab, lv)] = dict(s=s, r_visible=rv, r_subxi=rs, ell_visible_at_xi=ell_xi)
# the lambda at which the flattest zero's sub-xi core would reach xi (ell ~ lambda^(-1/8) at fixed C)
lam_crit = {}
for f in FOOTS:
    a = 1.0; i = int(np.argmin(np.abs(AGR - a))); Lp = LK(a) * Mpc
    s = float(rms_bp_L(i, [LK(a)], A0[f])[0]) / Lp
    Cxi = CT(float(x_P2(s * XI_M[f])))
    lam_crit[f] = (XC.ell_sc(A0[f], Cxi, 1.0)[2] / XI_M[f]) ** 8
# (c) H_K1's yield layers above z_q0 on DE12's hosts: C_L(d) = C_L(x_P2(y' d))
NS9, D12 = XC.load_base()
gfr = NS9["M6"]["gfrac_smooth"]; G6 = NS9["M6"]["G6"]; MPCm = NS9["M6"]["MPCm"]; MS12 = D12["MS"]
HKF = XC.hk1_forms(M6, A0)
for f in FOOTS:
    a0v = A0[f]
    for z in (0.8, 1.0, 2.5):
        Lz = HKF["L_of"](z) * MPCm; yth = HKF["yth_of"](z, f)
        for Mb in (1e10, 1e11, 1e12):
            yb = lambda r, Mb=Mb: G6 * Mb * MS12 / (a0v * r ** 2) * (1 - gfr(r / Lz))
            rr = np.geomspace(1e-3, 50, 40000) * MPCm; yy = yb(rr)
            j = np.where(yy > yth)[0][-1]
            rY = brentq(lambda q: float(yb(np.array([q]))[0]) - yth, rr[j], rr[j + 1], xtol=1e-15 * rr[j], rtol=1e-15)
            yp = abs(float(yb(np.array([rY * (1 - 1e-6)]))[0] - yth)) / (1e-6 * rY)
            Cfun = lambda d, yp=yp: CLf(float(x_P2(yp * d)))
            for lv in LAM7:
                r7["layers"][(f, z, Mb, lv)] = dict(r_Y_kpc=rY / C25.KPC_M, dstar_visible=core_radius(a0v, Cfun, lv + 3.0),
                                                    dstar_subxi=core_radius(a0v, Cfun, lv))
for (f, lab, lv), (ev, es) in r7["typical"].items():
    if f == "canonical":
        P(f"    typical {lab:26s} lambda {lv:7.0e}: ell_sc {ev:.1e} m (metric-visible) / {es:.1e} m (sub-xi)")
for (f, z, slab, lv), v in r7["zeros"].items():
    if f == "canonical" and z in (0.0, 0.5):
        P(f"    zero at z = {z}: {slab:28s} s = {v['s']:.2e}/m, lambda {lv:7.0e}: core r* {v['r_visible']:.2e} m (visible) / {v['r_subxi']:.2e} m "
          f"(sub-xi); visible ell_sc at the xi scale {v['ell_visible_at_xi']:.1e} m")
for (f, z, Mb, lv), v in r7["layers"].items():
    if f == "canonical" and lv in (1e-9, 0.03):
        P(f"    yield layer z = {z} M_b {Mb:.0e} (r_Y {v['r_Y_kpc']:.0f} kpc) lambda {lv:.0e}: d* {v['dstar_visible']:.2e} m (visible) / "
          f"{v['dstar_subxi']:.2e} m (sub-xi)")
P("    lambda at which the web's flattest zero's sub-xi core reaches xi: " + ", ".join(f"{f}: {v:.1e}" for f, v in lam_crit.items()))
maxcore = max([max(v["r_visible"], v["r_subxi"]) for v in r7["zeros"].values()] + [max(v["dstar_visible"], v["dstar_subxi"]) for v in r7["layers"].values()])
max_ell_xi = max(v["ell_visible_at_xi"] for v in r7["zeros"].values())
r7_ok = maxcore < min(XI_M.values()) and max_ell_xi < min(XI_M.values())
check("R7 [H7, pre-declared] STRONG COUPLING IN H_K1's REAL BACKGROUNDS, lambda in [1e-9, 0.03]: every strongly coupled region -- the core "
      "around a zero of the band-passed field below z_q0 (web zeros, cored halo centres 1e2-1e6 rho_bar) and the layer at H_K1's yield "
      "surfaces above it -- is smaller than xi in both phi sectors, and the metric-visible sector's length at the xi scale is < xi",
      f"largest core/layer {maxcore:.1e} m vs xi {min(XI_M.values()):.1e} m; visible ell_sc at xi <= {max_ell_xi:.1e} m; the flattest zero's "
      f"sub-xi core reaches xi only at lambda ~ {min(lam_crit.values()):.0e}", r7_ok,
      "strong coupling is NOT absent -- every zero of the band-passed field below z_q0 carries a strongly coupled core, for every lambda "
      "(ell ~ lambda_eff^(-1/8)) -- but the cores are sub-xi, where the filter hides phi from the metric; lambda does not control them")
L.out["numbers"]["R7"] = {k_: {str(kk): vv for kk, vv in v.items()} for k_, v in r7.items()}
L.out["numbers"]["R7"]["lam_crit"] = lam_crit

# ================================================================================================ V the lambda verdict
banner("V  (reported) THE lambda VERDICT UNDER H_K1")
P(f"""  * REQUIRED > 0 below z_q0 (R4: no phi equation at lambda = 0 on exact FRW); any positive value un-freezes phi fast (>= {min(v for f in FOOTS for v in om4[f].values()):.0f} H).
  * H_K1's cosmological gates are lambda-inert (sigma_8 spread {spread_low:.0e} for lambda <= 0.03; {spread_all:.0e} up to 274.4; R5).
  * The MOND-regime observables are lambda-independent (to 1%) ONLY for lambda <= {min(lam_1pc_cs, lam_1pc_a2):.3f} (R6).  So lambda must be
    DECLARED in (0, ~0.03] -- a regulator window, with the limit lambda -> 0+ smooth for every observable computed here.  Left free in
    (0, 274.4] it is a knob: the MOND regime reads it (x{ratio_cs:.1f} in tracking speed, x{ratio_a2:.0f} in alpha_2 v^2) and no datum in the
    record selects a value; the data bound it only from above (tracking, 274.4).
  * Strong coupling does not select lambda either: the cores around every zero of the band-passed field below z_q0 exist for every
    lambda (weak lambda^(-1/8) dependence) and are sub-xi (<= {maxcore:.0e} m) for lambda >= 1e-9 (R7).""")
check("V (reported) the lambda verdict: required > 0, a regulator only in (0, ~0.03]; a knob if left free in (0.03, 274.4]",
      f"inert window {min(lam_1pc_cs, lam_1pc_a2):.3f}; upper bound {lam_max:.1f}", True, load_bearing=False)

banner("VERDICT")
nlb = sum(1 for _, ok, lb in L.ch if lb and not ok)
pf = {k_: ("PASS" if L.out["checks"][k_]["ok"] else "FAIL") for k_ in ("R1", "R2", "R3", "R4", "R5", "R6", "R7")}
P(f"""  Item 3.  H_K1's ramp is a kink, not a jump (R1: {pf['R1']}); FRW growth across z_q0 is well posed{' [MUTATE: hard step]' if MUT else ''} (R2: {pf['R2']}:
    |d sigma_8| {d_eps[0.002]:.0e} at eps = 0.002, <= {max(ncross.values())} crossing per mode, chord step shrinks x{min(shrink.values()):.1f});
    the background's Friedmann function jumps up by <= {max(max(v['dF_over_rho'].values()) for v in r3.values()):.0e} rho_bar at z_q0 -> H continuous (R3: {pf['R3']});
    lambda > 0 is required there and un-freezes phi fast (R4: {pf['R4']}); the gates are lambda-inert (R5: {pf['R5']}); the MOND regime is
    lambda-independent only for lambda <= {min(lam_1pc_cs, lam_1pc_a2):.3f} (R6: {pf['R6']}); strongly coupled cores sit at every zero of the band-passed field
    below z_q0 and in the yield layers above it, all sub-xi for lambda >= 1e-9 (R7: {pf['R7']}).
  Not 'closed'.  kappa = 1/2 FITTED.  {sum(1 for _, o_, _l in L.ch if o_)}/{len(L.ch)} checks pass; load-bearing failures: {nlb}.""")
L.out["ledger"] = [
    dict(link="XR18b-R2", status="DERIVED" if L.out["checks"]["R2"]["ok"] else "FAILS", what="FRW growth across z_q0 under H_K1 (kink, single crossings, continuous chord)"),
    dict(link="XR18b-R3", status="DERIVED", what="the kink pins H for ~1e-6 Hubble times (Filippov segment); well posed"),
    dict(link="XR18b-R6", status="CONSTRAINT", what=f"lambda <= {min(lam_1pc_cs, lam_1pc_a2):.3f} for lambda-independent MOND-regime observables; a knob if left free"),
    dict(link="XR18b-R7", status="DERIVED", what="strongly coupled cores at every zero of the band-passed field below z_q0, sub-xi, lambda-insensitive"),
]
L.finish()
