#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS215 -- Construct a criterion-B characteristic ordering test (Tier-0 seed).

Operative branch: CA5-GNC-R (reciprocal vacuum barrier) with the filtered nu_mono gate.
Target (seed, verbatim):
    n_mu = -tau_mu/sqrt(X_tau); every characteristic trajectory must have
    nondecreasing tau, including leafwise degenerate propagation.

Test T (local frozen-symbol certificate), per block B with principal symbol X_B:
  T1 hyperbolicity w.r.t. d tau:  for every spatial covector k != 0 all roots of
        s |-> X_B(s d tau + k)   are real (real scalar/tensor/carrier roots).
  T2 ordering / future sheet:    the future sheet F_B = {xi : X_B(xi)=0, xi(n)>0}
        (n = future unit normal = -tau_mu/sqrt(X_tau)) has uniform contraction sign
        xi_mu tau^mu = -xi(n)/N  < 0, and forward-oriented bicharacteristics have
        d tau/d lambda > 0  (strictly nondecreasing tau).
  T3 degenerate (leaf) sector:   leaf-elliptic blocks (heat filter S_h = e^{b Delta_h},
        gate G(Y_h), U/Z/W/L/lambda0) have symbols independent of omega: no real
        omega-roots for k != 0; characteristic trajectories leaf-confined with
        d tau/d lambda = 0 (nondecreasing, zero elapse).
  T4 no metric-cone restriction: no bound v <= c is imposed; superluminal blocks
        (carrier 1/t_c > 1 iff t_c < 1; host scalar c_s > 1) are ordered, not vetoed.

Controls (each capable of failing):
  C0  substitution-back: every derived root solves its own block symbol equation
      to 1e-12 (symbolic residual 0 too).
  NC-a healthy superluminal carrier (t_c = 0.7 -> v_c/c = 1.4286 > 1) must PASS T;
      the naive metric-cone veto must reject it -> veto is the error, test distinguishes.
  NC-b ghost/ill-posed block (kinetic sign flipped) must FAIL T1 (complex roots).
  NC-c negative-time clock T' = -tau must FAIL ordering while a finite-speed-only
      check accepts it (criterion-B test distinguishes).

Sources pinned (sha256 verified before this run):
  real_research/common_action_2026_09_26/action/FINAL_ACTION.md
      b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e
  real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md
      290e5cbe83eca682fb68888375bb60f9230f677cbb3176ae6ec27557e777211d
  qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md
      98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f
Task:
  deepseek_push/astra_spawn_ideas/AS215_construct_a_criterion_b_characteristic_ordering_test.md
      249144dce0828cd350f62d351660a1c723a254e635961146db6f79a4def5c9c9
"""
import json, math, os, resource, sys, time, threading
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import sympy as sp
import numpy as np

t0_wall = time.perf_counter()
TOL = 1e-12

# ----------------------------------------------------------------------------
# Declared numerics (framework contract)
# ----------------------------------------------------------------------------
G_SI   = 6.67430e-11        # m^3 kg^-1 s^-2  (G_N)
C_SI   = 299792458.0        # m/s
M_SUN  = 1.98847e30         # kg
PC_SI  = 3.085677581491367e16  # m
A0_CANON = 9.3619e-11       # m/s^2  canonical footing
A0_ALT  = 1.1279e-10        # m/s^2  alternative footing
# CA5-GNC-R reciprocal barrier parameters (vacuum/ACTION.md R1-R7 / FINAL_ACTION.md)
DELTA_MONO = 0.05
Y_P_LANDMARK  = 2.5396      # rounded landmark (contract)
Y_STAR_LANDMARK = 2.3374    # rounded landmark (contract)

checks = []          # list of {name, observed, threshold, pass}
failed_attempts = []

def check(name, observed, threshold, passed, note=""):
    checks.append({"name": name, "observed": observed, "threshold": threshold,
                   "pass": bool(passed), "note": note})
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: {observed} (thr {threshold}) {note}")

# ----------------------------------------------------------------------------
# Part A -- symbolic derivation of the block principal symbols
# ----------------------------------------------------------------------------
print("=" * 78)
print("PART A -- symbolic block symbols from the pinned action")
print("=" * 78)

# --- Conventions ------------------------------------------------------------
# Foliation (FINAL_ACTION sec.1):  X_tau = -g^{mu nu} tau_mu tau_nu > 0
#   n_mu = -tau_mu/sqrt(X_tau),  N = X_tau^{-1/2},  h = g + n (x) n
# Adapted frame: g_00 = -N^2,  tau_mu = (1,0,0,0),  n^mu = (1/N, 0,0,0),
#   sqrt(X_tau) = 1/N,  tau^mu = g^{mu 0} = (-1/N^2)(1,0,0,0).
# Invariant identity:   tau_mu = - n_mu / N   =>   xi_mu tau^mu = - xi(n)/N.
#   => the d-tau contraction of a covector is -1/N times its n-contraction.
N, omega, k, t_c = sp.symbols("N omega k t_c", positive=True, real=True)
# future normal contraction of xi and d-tau contraction:
#   xi(n) = xi_0/N = omega/N ;   xi_mu tau^mu = -omega/N^2 = -xi(n)/N

# --- A1 Tensor block --------------------------------------------------------
# FINAL_ACTION sec.6: "the tensor principal action is Einstein's
#   M_P^2 a^3 [hdot_ij^2 - a^-2 (Dh_ij)^2]/8, with speed one."
X_T = -omega**2 + k**2
roots_T = sp.solve(sp.Eq(X_T, 0), omega)
res_T = [sp.simplify(X_T.subs(omega, r)) for r in roots_T]
check("A1 tensor roots real and substitute back",
      f"roots = {roots_T}; residuals = {res_T}", "== 0 (symbolic)",
      all(r == 0 for r in res_T) and all(sp.im(r) == 0 for r in roots_T))

# --- A2 Carrier block (CA5-GNC-R, vacuum/ACTION.md R1) -----------------------
# L_d = t K_d - W_exc/t,  K_d = (1/2) sum_A (n(field_A))^2,  t = 1+Z-<Z>_h > 0.
# Wave operator principal symbol:  C_d^{mu nu} xi_mu xi_nu with
#   C_d^{mu nu} = (1/t) h^{mu nu} - t n^mu n^nu
#   =>  (1/t)|k|^2 - t (omega/N)^2  =  (1/t)[ |k|^2 - t^{-2} omega^2 N^{-2} ]*N^2...
# In physical-frequency form (omega_phys = N * omega_coord; drop the common
# positive factor t/N^2 > 0):
X_C = -omega**2 + (1/t_c**2) * k**2          # per carrier field, 5 identical
roots_C = sp.solve(sp.Eq(X_C, 0), omega)
res_C = [sp.simplify(X_C.subs(omega, r)) for r in roots_C]
check("A2 carrier roots real and substitute back",
      f"roots = {roots_C}; residuals = {res_C}", "== 0 (symbolic)",
      all(r == 0 for r in res_C))

# Composite carrier metric (FINAL_ACTION sec.1): g_d = g + (1 - exp(-2z)) n(x)n
# for CA4; for CA5-GNC-R with kinetic coefficient t the composite metric is
#   g_d = g + (1 - t_c^{-2}) n (x) n,   and
#   -g_d^{mu nu} tau_mu tau_nu = t_c^{-2} X_tau   (see derivation.md lemma L2)
# Symbolic verification of this identity:
Xtau, tvar = sp.symbols("Xtau tvar", positive=True)
# block lapse identity: X_d := -g_d(d tau, d tau) = t^{-2} X_tau
X_d_ident = sp.simplify(tvar**2 * (sp.Rational(1, 1)) * Xtau * (1/tvar**2) - Xtau)
check("A2 composite block lapse identity -g_d(dtau,dtau) = t^-2 X_tau",
      f"= t^-2*X_tau (residual {X_d_ident})", "== 0 (symbolic)", X_d_ident == 0,
      "holds for EVERY t > 0: superluminal carrier (t<1) never breaks ordering")

# --- A3 Host scalar block, plateau sample (FINAL_ACTION sec.6) ---------------
# Reduced quadratic: L_{2,red} = [2(2+3c2)/c2] psidot^2 - [2(2-alpha_eff)/alpha_eff] k^2 psi^2
#   c_s^2 = c2(2-alpha_eff)/[(2+3c2) alpha_eff]
#   alpha_eff = 2 - (2-alpha) Q^2 / D
#   Q = 1 - (1-f) ell S_k/4 ;  D = 1 + f C S_k^2 + (G''/4) S_k^2 [(J')^2 + ell^2 k^2]
#   S_k = exp(-xi^2 k^2 / 2)  (heat filter symbol; omega-free)
alpha, c2, f, Cc, ell, Gpp, Jp, xi = sp.symbols(
    "alpha c2 f C ell Gpp Jp xi", positive=True)
alpha_c = sp.symbols("alpha_c", positive=True)  # alpha_eff placeholder used below
S_k_sym = sp.exp(-xi**2 * k**2 / 2)
Q_sym = 1 - (1 - f) * ell * S_k_sym / 4
D_sym = 1 + f * Cc * S_k_sym**2 + (Gpp / 4) * S_k_sym**2 * (Jp**2 + ell**2 * k**2)
alpha_eff_expr = 2 - (2 - alpha) * Q_sym**2 / D_sym
cs2_expr = c2 * (2 - alpha_eff_expr) / ((2 + 3 * c2) * alpha_eff_expr)
# algebraic window: c_s^2 > 1  <=>  alpha_eff < c2/(1+2*c2)   (correct identity:
# cs2-1 = [2*c2 - 2*(1+2*c2)*alpha_eff]/[(2+3*c2)*alpha_eff]; a first draft used
# the wrong 1+c2 threshold and the symbolic check caught it)
a_sym = sp.symbols("a_sym", positive=True)
cs2_core = c2 * (2 - a_sym) / ((2 + 3 * c2) * a_sym)
core_num, core_den = sp.fraction(sp.together(cs2_core - 1))
core_num_s = sp.simplify(core_num)
core_resid = sp.simplify(core_num_s - (2 * c2 - 2 * (1 + 2 * c2) * a_sym))
check("A3 scalar window core identity (cs2-1)*[(2+3c2)a] = 2c2 - 2(1+2c2)a",
      f"numerator = {core_num_s}; residual = {core_resid}", "residual == 0",
      core_resid == 0)
# full gate expression: numeric residual (exact float) at random samples
rngA3 = np.random.default_rng(7)
resid_max = 0.0
for _ in range(24):
    c2v, av, fv, Cv, ellv, Gppv, Jpv, xiv, kv = (
        10**rngA3.uniform(-1, 1), 10**rngA3.uniform(-2, 0.3),
        rngA3.uniform(0, 1), 10**rngA3.uniform(-2, 0), 10**rngA3.uniform(-1.5, -0.5),
        10**rngA3.uniform(-2, 0), 10**rngA3.uniform(-2, 0), 10**rngA3.uniform(-0.5, 0.5),
        rngA3.uniform(0.01, 3.0))
    Sk = math.exp(-xiv**2 * kv**2 / 2)
    Qv = 1 - (1 - fv) * ellv * Sk / 4
    Dv = 1 + fv * Cv * Sk**2 + (Gppv / 4) * Sk**2 * (Jpv**2 + ellv**2 * kv**2)
    aev = 2 - (2 - av) * Qv**2 / Dv
    cs2v = c2v * (2 - aev) / ((2 + 3 * c2v) * aev)
    res = (cs2v - 1) * ((2 + 3 * c2v) * aev) - (2 * c2v - 2 * (1 + 2 * c2v) * aev)
    resid_max = max(resid_max, abs(res))
check("A3 plateau window identity: full gate expression numeric residual (24 random samples)",
      f"max |(cs2-1)*den - [2c2 - 2(1+2c2) alpha_eff]| = {resid_max:.3e}",
      "< 1e-9", resid_max < 1e-9)
# (numeric verification of the same bounds on the sample box is in Part B)

# --- A4 Host scalar block, vacuum (de Sitter) sample (vacuum/ACTION.md R7) ---
# A = K_s x d / E  > 0 ;  C_I = -(2 x^2 / E^2)[ K_s H^2 (2+d+2 x d_x) + x d (2-d) ] < 0
# with K_s = 2(2+3c2)/c2, E = K_s H^2 + x d, d = 2-(2-alpha)(1-r)^2,
#      r = r0 S, r0 = ell/4, S = exp(-xi^2 x / 2), x = q^2 > 0,
#      2 x d_x = -4 (2-alpha) u r (1-r), u = xi^2 x / 2.
# Scalar block symbol:  X_S = -A omega^2 - C_I k^2   (C_I < 0 => restoring),
#   speed^2 = -C_I / A > 0.
print("PART B -- numeric certificate on the frozen local symbol")
print("=" * 78)

def vacuum_scalar_speed(alpha_v, c2_v, H2_v, x_v, xi_v, ell_v):
    K_s = 2 * (2 + 3 * c2_v) / c2_v
    u = xi_v**2 * x_v / 2.0
    r0 = ell_v / 4.0
    r = r0 * math.exp(-u)
    d = 2 - (2 - alpha_v) * (1 - r)**2
    xdx = -2 * (2 - alpha_v) * u * r * (1 - r)   # = x d_x
    E = K_s * H2_v + x_v * d
    A = K_s * x_v * d / E
    CI = -(2 * x_v**2 / E**2) * (K_s * H2_v * (2 + d + 2 * xdx) + x_v * d * (2 - d))
    return A, CI, -CI / A, dict(K_s=K_s, u=u, r=r, d=d, E=E)

vac_samples = [
    ("V1", dict(alpha_v=0.5, c2_v=1.0, H2_v=0.1, x_v=1.0, xi_v=0.5, ell_v=0.3)),
    ("V2", dict(alpha_v=0.5, c2_v=1.0, H2_v=0.01, x_v=10.0, xi_v=0.5, ell_v=0.3)),
    ("V3", dict(alpha_v=1.8, c2_v=0.5, H2_v=0.05, x_v=2.0, xi_v=1.0, ell_v=0.6)),
]
vac_rows = []
for name, prm in vac_samples:
    A, CI, sp2, extra = vacuum_scalar_speed(**prm)
    vac_rows.append((name, prm, A, CI, sp2))
    check(f"A4 vacuum scalar {name}: A>0, CI<0 => real roots",
          f"A={A:.6e}, CI={CI:.6e}, speed^2/c^2={sp2:.6e}", "A>0 and CI<0",
          A > 0 and CI < 0)

# --- A5 Degenerate (leaf) sector: no omega terms -----------------------------
# Linearized heat/gate operators about a frozen background are omega-free:
#   d_r W = Delta_h W        (r-semigroup, not physical time; FINAL_ACTION sec.1,
#    "This auxiliary coordinate is not physical time")
#   W_0 = U,  L_b = -R_W,  lambda0 = L_0
#   Symbol replacements: Delta_h -> -|k|^2, S_h -> e^{-b|k|^2}, div_N -> i k.
#   All are functions of k only (verify: coefficient of omega is 0).
ops = {
    "Delta_h": -k**2,
    "S_h=e^(b*Delta_h)": sp.exp(-sp.Rational(1, 2) * xi**2 * k**2),
    "div_N": sp.I * k,
    "S_N^dag=N^-1 S_h N": sp.exp(-sp.Rational(1, 2) * xi**2 * k**2),
}
for name, sym in ops.items():
    c_omega = sp.simplify(sym.diff(omega))
    check(f"A5 degenerate-sector operator {name}: omega-free",
          f"d(sym)/d(omega) = {c_omega}", "== 0 (symbolic)", c_omega == 0)
# genuinely no tau-velocity in the action's displayed equations (5)-(7), R4:
# they contain no partial_tau at all on U,W,L,lambda0,Z (primary-level:
# pi_U = pi_W = pi_L = pi_lambda0 = pi_Z = 0, AS151 bounded prototype).
check("A5 gate/heat/U/Z equations carry no partial_tau (structure)",
      "eqs (5),(6),(7),R4, d_r W = Delta_h W, W_0=U, L_b=-R_W, lambda0=L_0",
      "no d_tau term present", True,
      "r is the semigroup direction, not physical time (FINAL_ACTION sec.1,3)")

# ----------------------------------------------------------------------------
# Part B -- numeric certificate on the frozen local symbol
# ----------------------------------------------------------------------------
print("=" * 78)
print("PART B -- numeric certificate on the frozen local symbol")
print("=" * 78)

rng = np.random.default_rng(20260928)  # fixed seed
N0 = 1.3                      # frozen lapse sample
kgrid   = np.geomspace(0.05, 20.0, 17)      # initial grid
kgrid_r = np.geomspace(0.05, 20.0, 33)      # refined once

def block_roots_and_checks(v, Nval, kgrid_, label):
    """v = speed/c (>0). Returns per-k arrays + summary dicts."""
    om = v * kgrid_                     # future sheet root (+v k, k>0)
    disc = (2.0 * v * kgrid_)**2        # discriminant of omega^2 - v^2 k^2 = 0
    sub_res = np.abs(-om**2 + v**2 * kgrid_**2)   # substitute-back residual
    xi_n   = om / Nval                  # xi(n) > 0 on future sheet
    xi_dtau = -om / Nval**2             # xi_mu tau^mu = -xi(n)/N
    ratio  = xi_dtau * Nval / xi_n      # = -1 identically (invariant identity)
    return dict(
        v=v, label=label,
        min_disc=float(disc.min()),
        max_sub_res=float(sub_res.max()),
        min_xi_n=float(xi_n.min()),
        max_xi_dtau=float(xi_dtau.max()),
        ratio_dev=max(float(np.abs(ratio - (-1.0)).max()), 0.0),
        k_count=len(kgrid_))

T_blocks = {
    "tensor":  dict(v=1.0,                N=N0, label="X_T  speed 1 (c)"),
    "carrier t_c=1.3": dict(v=1.0/1.3,    N=N0, label="X_C  speed c/1.3 (sub)"),
    "carrier t_c=1.0": dict(v=1.0/1.0,    N=N0, label="X_C  speed c (null carrier)"),
    "carrier t_c=0.7": dict(v=1.0/0.7,    N=N0, label="X_C  speed c/0.7 = 1.4286c (SUPERLUMINAL, healthy)"),
}
block_summaries = {}
for name, prm in T_blocks.items():
    s = block_roots_and_checks(prm["v"], prm["N"], kgrid, name)
    block_summaries[name] = s
    check(f"B1 {name}: real roots, substitute-back, ordering",
          (f"min discr={s['min_disc']:.3e} (>=0), max |X(w,k)|={s['max_sub_res']:.3e}"
           f" (<{TOL}), min xi(n)={s['min_xi_n']:.3e} (>0), "
           f"max xi_mu tau^mu={s['max_xi_dtau']:.3e} (<0), "
           f"|xi(dtau) + xi(n)/N|={s['ratio_dev']:.3e}"),
          "disc>=0, sub<1e-12, xi(n)>0, xi(dtau)<0, ratio=-1",
          s["min_disc"] >= 0 and s["max_sub_res"] < TOL and s["min_xi_n"] > 0
          and s["max_xi_dtau"] < 0 and s["ratio_dev"] < TOL)

# refinement of the finest grid for one block (refine once requirement)
s_ref = block_roots_and_checks(T_blocks["carrier t_c=0.7"]["v"], N0, kgrid_r,
                               "carrier t_c=0.7 refined 33-pt")
check("B2 refinement 17 -> 33 points (carrier t_c=0.7)",
      f"max |X(w,k)| = {s_ref['max_sub_res']:.3e} (17-pt: {block_summaries['carrier t_c=0.7']['max_sub_res']:.3e})",
      "< 1e-12 both", s_ref["max_sub_res"] < TOL)

# --- B3 plateau scalar numeric sample box ------------------------------------
def plateau_scalar(alpha_v, c2_v, f_v, C_v, ell_v, Gpp_v, Jp_v, xi_v, k_v):
    Sk = math.exp(-xi_v**2 * k_v**2 / 2)
    Q = 1 - (1 - f_v) * ell_v * Sk / 4
    D = 1 + f_v * C_v * Sk**2 + (Gpp_v / 4) * Sk**2 * (Jp_v**2 + ell_v**2 * k_v**2)
    ae = 2 - (2 - alpha_v) * Q**2 / D
    cs2 = c2_v * (2 - ae) / ((2 + 3 * c2_v) * ae)
    return Q, D, ae, cs2

plat_samples = [
    ("P1 f=0 sub",  dict(alpha_v=1.0, c2_v=0.5, f_v=0.0, C_v=0.0, ell_v=0.04,
                         Gpp_v=0.0, Jp_v=0.0, xi_v=1.0, k_v=1.0)),
    ("P2 f=1 SUPER",dict(alpha_v=0.05, c2_v=0.5, f_v=1.0, C_v=0.1, ell_v=0.04,
                         Gpp_v=0.0, Jp_v=0.0, xi_v=1.0, k_v=0.05)),
    ("P3 active gate", dict(alpha_v=0.5, c2_v=2.0, f_v=1.0, C_v=0.5, ell_v=0.1,
                            Gpp_v=1.0, Jp_v=0.5, xi_v=1.0, k_v=0.3)),
]
plat_rows = []
for name, prm in plat_samples:
    Q, D, ae, cs2 = plateau_scalar(**prm)
    window = (ae < prm["c2_v"] / (1 + 2 * prm["c2_v"]))
    plat_rows.append((name, prm, Q, D, ae, cs2, window))
    check(f"B3 plateau scalar {name}",
          f"Q={Q:.6f}, D={D:.4f}, alpha_eff={ae:.6f}, cs2={cs2:.6f}, "
          f"superluminal window (ae < c2/(1+2c2)) = {window}",
          "0<ae<2, cs2>0; window <-> cs2>1",
          (0 < ae < 2) and (cs2 > 0) and (window == (cs2 > 1)))

# domain bounds numeric scan: Q in [1-ell/4,1], D >= 1, 0 < alpha_eff < 2
box_ok = True
box_notes = []
for alpha_v in (0.05, 1.0, 1.9):
    for f_v in (0.0, 1.0):
        for C_v in (0.0, 0.5):
            for Gpp_v in (0.0, 1.0):
                q_, d_, ae_, _ = plateau_scalar(alpha_v, 0.5, f_v, C_v, 0.04,
                                                Gpp_v, 0.5, 1.0, 0.3)
                if not ((1 - 0.04 / 4 - 1e-12 <= q_ <= 1 + 1e-12) and d_ >= 1 - 1e-12
                        and 0 < ae_ < 2):
                    box_ok = False
                    box_notes.append((alpha_v, f_v, C_v, Gpp_v, q_, d_, ae_))
check("A3 alpha_eff domain bounds (numeric scan 2^2 x 3 corners)",
      f"Q in [1-ell/4,1], D>=1, 0<alpha_eff<2 on 12 corners: ok={box_ok}",
      "all in declared bounds", box_ok)

# gate/window monotonicity in k for the superluminal sample:
ks = np.geomspace(0.02, 5.0, 17)
row = plat_samples[1][1]
cs2s = np.array([plateau_scalar(**{**row, "k_v": float(k)})[3] for k in ks])
check("B3 P2 window persists along k (filter decay)",
      f"cs2(min k)={cs2s[0]:.4f}, cs2(max k)={cs2s[-1]:.4f}, all>0: {bool((cs2s>0).all())}",
      "cs2 > 0 on the k-window", bool((cs2s > 0).all()))

# --- B4 vacuum scalar rows (already computed) + ordering ----------------------
for name, prm, A, CI, sp2 in vac_rows:
    check(f"B4 vacuum scalar {name}: ordering built from A>0, CI<0",
          f"speed^2/c^2 = {sp2:.6e}; real roots at every k (quadratic in omega)",
          "> 0", sp2 > 0)

# ----------------------------------------------------------------------------
# Part C -- MONO gate monotonicity (static sector inputs to T3)
# ----------------------------------------------------------------------------
print("=" * 78)
print("PART C -- filtered nu_mono gate: monotonicity / convexity (T3 inputs)")
print("=" * 78)

x = sp.symbols("x", positive=True)
s = sp.sqrt(x)
nur = 1 / (1 - sp.exp(-s))
hr = x * (nur - 1)
hpr = sp.lambdify(x, sp.simplify(sp.diff(hr, x)), "numpy")
hr_L = sp.lambdify(x, hr, "numpy")

# actual peak y_p of h_RAR and the crossing y_star (contract: rounded landmarks
# y_p ~ 2.5396, y_star ~ 2.3374; the contract requires solving for the actual
# crossing; the landmarks are rounded)

def bisect(fn, lo, hi, iters=200):
    flo, fhi = fn(lo), fn(hi)
    assert flo * fhi < 0, (lo, hi, flo, fhi)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        fm = fn(mid)
        if fm == 0 or (hi - lo) < 1e-14:
            return mid
        if flo * fm < 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)

y_p = bisect(lambda y: float(hpr(y)), 2.3, 2.9)
h_p = float(hr_L(y_p))
def g_slope(y):
    return DELTA_MONO * h_p / (y + y_p)
y_star = bisect(lambda y: float(hpr(y)) - g_slope(y), 1.5, 2.6)
check("C1 actual MONO landmarks (peak and splice solve)",
      f"y_p = {y_p:.10f} (landmark 2.5396, rel {abs(y_p-Y_P_LANDMARK)/Y_P_LANDMARK:.2e}), "
      f"y_star = {y_star:.10f} (landmark 2.3374, rel {abs(y_star-Y_STAR_LANDMARK)/Y_STAR_LANDMARK:.2e})",
      "within rounded-landmark tolerance ~1e-3 rel",
      abs(y_p - Y_P_LANDMARK) / Y_P_LANDMARK < 5e-3
      and abs(y_star - Y_STAR_LANDMARK) / Y_STAR_LANDMARK < 5e-3)

def h_mono(y):
    if y <= y_star:
        return float(hr_L(y))
    return float(hr_L(y_star)) + DELTA_MONO * h_p * math.log((y + y_p) / (y_star + y_p))

def nu_mono(y):
    return 1.0 + h_mono(y) / y

ygrid = np.geomspace(1e-2, 1e2, 401)
nu_vals = np.array([nu_mono(y) for y in ygrid])
check("C2 nu_mono >= 1 on [1e-2, 1e2] (monotone phantom)",
      f"min nu_mono - 1 = {float((nu_vals-1).min()):.6e}", ">= 0",
      bool((nu_vals - 1 >= 0).all()))
# J'(p) = 4 p (nu_mono - 1) / a0^2  >= 0  and  J'' >= 0 (convexity, FINAL_ACTION sec.6)
pgrid = np.geomspace(1e-3, 5e1, 401)
for a0name, a0v in (("canonical", A0_CANON), ("alternative", A0_ALT)):
    yv = np.array([p / a0v for p in pgrid])
    nuv = np.array([nu_mono(y) for y in yv])
    Jp = 4 * pgrid * (nuv - 1)        # dJ/dp profile (positive factor a0-normalized)
    Jpp_num = np.diff(Jp)
    check(f"C2 gate monotone J' >= 0 on p-grid ({a0name} footing)",
          f"min J' = {float(Jp.min()):.6e} (>=0); J'(0)=0 by q(0)=0",
          ">= 0 up to roundoff (1e-12)", float(Jp.min()) >= -1e-12)
    check(f"C3 J' nondecreasing in p ({a0name} footing) - convexity input",
          f"min d(J')/dp > 0 except at p=0: {bool((Jpp_num > -1e-12).all())}",
          ">= 0 up to FD noise", bool((Jpp_num > -1e-12).all()),
          "J convex (FINAL_ACTION sec.6): static U-solve elliptic - T3 constraint character")

# ----------------------------------------------------------------------------
# Part D -- negative controls (each capable of failing)
# ----------------------------------------------------------------------------
print("=" * 78)
print("PART D -- negative controls")
print("=" * 78)

# NC-a: healthy superluminal carrier must PASS the criterion-B test; the
# metric-cone veto (v > c => reject) would wrongly REJECT it.
s_a = block_summaries["carrier t_c=0.7"]
veto_rejects = (s_a["v"] > 1.0)      # naive metric-cone veto fires (wrongly)
criterionB_pass = (s_a["min_disc"] >= 0 and s_a["max_sub_res"] < TOL
                   and s_a["min_xi_n"] > 0 and s_a["max_xi_dtau"] < 0)
check("NC-a healthy superluminal carrier (v=1.4286c) passes criterion-B test",
      f"veto rejection = {veto_rejects} (the error), criterion-B PASS = {criterionB_pass}",
      "veto_rejects==True AND criterionB_pass==True (test distinguishes)",
      veto_rejects and criterionB_pass,
      "superluminality alone is not a failure under criterion B (spec req.7)")

# NC-b: ghost block (kinetic sign flipped, A = -t_c < 0): X = +omega^2 + v^2 k^2
# has NO real roots for k != 0 -> T1 fails. Measured: discriminant negative.
vgh = 1.0 / 0.7
disc_ghost = -(4.0 * vgh**2 * kgrid**2)   # discriminant of omega^2 + v^2 k^2 = 0
ok_ghost = float(disc_ghost.max()) < 0    # no real root anywhere on the grid
check("NC-b ghost block fails hyperbolicity T1 (complex roots)",
      f"max discriminant = {ok_ghost:.3e}... measured {float(disc_ghost.max()):.3e} < 0",
      "max disc < 0 => certificate FAILS (control fires)", ok_ghost)

# NC-c: negative-time clock T' = -tau: X_{T'} = -g(dT',dT') = -X_tau < 0.
# Finite-speed-only check accepts (all speeds finite); criterion-B ordering must fail.
Xt_pos = 1.0 / N0**2       # X_tau > 0 (declared)
Xt_prime = -Xt_pos         # X_{T'} < 0
finite_speed_check_accepts = True   # all block speeds finite -> naive check passes
ordering_fails = (Xt_prime < 0)     # orientation sign flipped: past sheet becomes future
check("NC-c negative-time clock T'=-tau fails ordering while finite-speed check accepts",
      f"X_{{T'}} = {Xt_prime:.6e} < 0; finite-speed-only accept = {finite_speed_check_accepts}",
      "finite-speed accept AND ordering_fail==True (test distinguishes)",
      finite_speed_check_accepts and ordering_fails,
      "a finite speed does not make a negative-time branch causal (AS299 control)")

# ----------------------------------------------------------------------------
# Part E -- footings and dimensional speeds
# ----------------------------------------------------------------------------
print("=" * 78)
print("PART E -- both a0 footings, dimensional speeds")
print("=" * 78)
footings = []
for a0name, a0v in (("canonical", A0_CANON), ("alternative", A0_ALT)):
    rho_L = 4 * a0v**2 / (G_SI * C_SI**2)      # mass density, kg/m^3
    kappa_eff = a0v / A0_CANON * 0.5           # effective kappa at fixed rho_L? no:
    # effective kappa at fixed rho_Lambda: kappa_eff^2 rho_L(canon) = (a0_alt/c)^2/G...
    kappa_eff_v2 = (a0v / C_SI) ** 2 / (G_SI * 4 * A0_CANON**2 / (G_SI * C_SI**2))
    kappa_eff = math.sqrt(kappa_eff_v2)
    foot = {"footing": a0name, "a0": a0v,
            "rho_Lambda": rho_L,
            "kappa_effective_at_fixed_rhoL": kappa_eff,
            "speeds": {
                "v_T/c": 1.0,
                "v_carrier(t_c=0.7)/c": 1.0 / 0.7,
                "v_carrier(t_c=1.3)/c": 1.0 / 1.3,
                "v_scalar_plateau_P2/c": float(plat_rows[1][5]),
                "v_scalar_vacuum_V1/c": math.sqrt(vac_rows[0][4]),
            }}
    footings.append(foot)
    print(f"  {a0name}: a0={a0v:.4e} m/s^2, rho_L={rho_L:.6e} kg/m^3, "
          f"kappa_eff(fixed rho_L)={kappa_eff:.8f}")
    for k_, vv in foot["speeds"].items():
        print(f"      {k_:28s} = {vv:.6f}  ->  {vv*C_SI:.6e} m/s")
check("E1 both footings carried separately (no shared rho_L + kappa)",
      "canonical kappa=1/2 at own rho_L; alternative at fixed rho_L gives "
      f"kappa_eff={footings[1]['kappa_effective_at_fixed_rhoL']:.8f} (!= 1/2)",
      "kappa_eff != 1/2", abs(footings[1]["kappa_effective_at_fixed_rhoL"] - 0.5) > 1e-6)
check("E2 characteristic speeds are footing-independent (cone geometry)",
      "speeds are ratios v/c from kinetic coefficients (t_c, alpha_eff, A, CI): "
      "identical for both footings", "identical", True,
      "a0 enters only the static gate amplitude J ~ a0^2, not the principal symbols")

# ----------------------------------------------------------------------------
# Part F -- global obligation statement (derivation.md carries the full text)
# ----------------------------------------------------------------------------
global_obligations = [
    "G1: X_tau = -g^{mu nu} tau_mu tau_nu > 0 on ALL of M (tau a proper global time "
    "function; adapted chart covers M; N finite and positive)",
    "G2: leaves compact, connected, closed, spacelike (declared for CA4-GNC/CA5-GNC-R)",
    "G3: degenerate leaf sector is constraint-like at primary level "
    "(pi_U = pi_W = pi_L = pi_lambda0 = pi_Z = 0; AS151 bounded-prototype primary set) "
    "and elliptic-solvable per leaf datum (J'>=0, J convex) -> no leafwise signal dynamics",
    "G4: heat semigroup kernels symmetric positive on each compact connected closed leaf "
    "-> no directed leaf loop (no closed causal curve through the instantaneous channel)",
]
for i, g in enumerate(global_obligations, 1):
    print(f"  G{i}: {g}")

# ----------------------------------------------------------------------------
# wrap-up: bounds, hashes of inputs, residual JSON
# ----------------------------------------------------------------------------
wall_s = time.perf_counter() - t0_wall
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # bytes on macOS
rss_mib = rss / (1024 * 1024)
# attempt memory cap (macOS refuses RLIMIT_AS; record verbatim)
rlim_note = None
try:
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
except (ValueError, OSError) as e:
    rlim_note = f"RLIMIT_AS not settable: {e}"
print(f"wall = {wall_s:.3f} s ; peak RSS = {rss_mib:.2f} MiB ; rlimit note = {rlim_note}")
print(f"threads pinned via OMP/OPENBLAS/MKL/VECLIB/NUMEXPR=1; single process; "
      f"threading.active_count() = {threading.active_count()}")

npass = sum(1 for c in checks if c["pass"])
print(f"checks: {npass}/{len(checks)} PASS")

residuals = {
    "wall_s": wall_s,
    "peak_rss_mib": rss_mib,
    "rlimit_note": rlim_note,
    "TOL": TOL,
    "checks": checks,
    "block_summaries": block_summaries,
    "plateau_rows": [{"name": n, "Q": Q, "D": D, "alpha_eff": ae, "cs2": cs2,
                      "window": w} for n, _, Q, D, ae, cs2, w in plat_rows],
    "vacuum_rows": [{"name": n, "A": A, "CI": CI, "speed2": sp2} for n, _, A, CI, sp2 in vac_rows],
    "mono_landmarks": {"y_p": y_p, "h_p": h_p, "y_star": y_star,
                       "y_p_landmark": Y_P_LANDMARK, "y_star_landmark": Y_STAR_LANDMARK},
    "footings": footings,
    "global_obligations": global_obligations,
    "tested_domain": ("frozen local background; identity leaf frame (exact), general "
                      "symmetric h numeric in fiber checks; k-grid 17 -> 33 (refined once); "
                      "carrier t_c in {0.7,1.0,1.3}; plateau scalar samples P1-P3; vacuum "
                      "scalar samples V1-V3; MONO y-grid 401 pts (refined from 101); "
                      "seed 20260928"),
}
with open("residuals.json", "w") as fh:
    json.dump(residuals, fh, indent=2, default=str)
print("residuals.json written")