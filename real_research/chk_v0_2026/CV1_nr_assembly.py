#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CV1 -- V0 FOR THE C-H/K BRANCH, STEP 1: THE NON-RELATIVISTIC ACTION THE COVARIANT V0 MUST REDUCE TO.

The author's 2026-09-26 decision (recipe, second user-decision block) keeps the C-H/K branch -- the C-H/K khronon with
the leaf average, the vacuum gate and the region kernel -- as its own branch.  Its one covariant action ("V0" in the
cross-thread review, real_research/cross_thread_review_2026_09_26/) was never written.  The region kernel (L361) and
the kernel-invisible pair (L353) exist only as non-relativistic Lagrangians with different chassis: L353 is C-H's
first-order form (Phi a multiplier for lap u = 4 pi G rho), L361 carries its own Newtonian potential phi with a
|grad phi|^2 term and couples baryons directly to its auxiliaries.  This lane writes ONE non-relativistic Lagrangian,
on C-H's chassis, that contains both, with baryons coupled only to the metric potential Phi (requirement 11), and
checks that its Euler-Lagrange equations reduce exactly to L361's and to requirement 1's.  CV2 writes the covariant
action and shows it reduces to this Lagrangian.

THE LAGRANGIAN (units of potential; S = C-H's symmetric heat filter; M^2 = m^2 (1 - f); q(Z) = 2 int_0^sqrt(Z) h(s) ds
so q'(Z) = nu(sqrt Z) - 1; f = the gate, prescribed here, varied in CV3):
  L = -(rho_b + rho_d) Phi - [2 grad Phi.grad u - |grad u|^2]/(8 pi G)                   C-H's chassis
      + a0^2 f q(|grad S w|^2/a0^2)/(8 pi G)                                               the region kernel (q-form)
      + Psi [(lap - M^2) w - f lap(u - v)]/(8 pi G)                                        the region field (multiplier Psi)
      + lam [lap v - 4 pi G (rho_d - <rho_d>)]/(8 pi G)                                    L353's pair (projected source)
      - sigma M^2 w^2/(8 pi G)                                                             L361's web self-term (sigma = 1)
  The kernel reads w, whose source f lap(u - v) = 4 pi G f (rho_b - <rho_b>) is the GATED BARYON density, screened in the
  web by M.  Baryons couple only to Phi.  The dark component couples to Phi and, through L353's pair, to lam.

WHAT THIS LANE CHECKS
  A1 [sympy, one dimension, a concrete non-trivial kernel, S = 1] the Euler-Lagrange equations are
       lap u = 4 pi G rho;  lap v = 4 pi G (rho_d - <rho_d>);  (lap - M^2) w = f lap(u - v);
       (lap - M^2) Psi = 2 div[f q' grad w] + 2 sigma M^2 w;  lap Phi = lap u + lap(f Psi)/2;  lam = -f Psi,
     so Phi = u + f P with P = Psi/2 the gated phantom, and the dark component's potential Phi + lam/2 = u is Newtonian
     (L353's reciprocity, now for the region kernel).
  A2 [reduction (i): the operative requirement-1 equations on a gate-on plateau] f = 1, M = 0, no dark component:
       lap u = 4 pi G rho_b and lap Phi = 4 pi G rho_b + div[(nu - 1) grad u] exactly (zero residual).
  A3 [reduction (ii): L361] at sigma = 1 (S = 1, isolated system): (u, w, P) solve L361's committed field equations
     (phi = u, chi = w, psi = P + w) with zero residual, and the forces agree species by species.  sigma = 0 differs by
     exactly the self-term M^2 w in the phantom's equation.
  A4 [the filter's adjoint, discrete] on a periodic grid with S = exp(b lap) as a symmetric matrix and a smooth analytic
     kernel (the adjoint's placement does not depend on the kernel; nu_mono is used in A5), the gradient of the discrete
     action (finite differences) equals the stated discrete field equations with S^T.
  A5 [C7, the source/force operator, named] the kernel's argument is w: the source is restricted to the gate-weighted
     baryons and screened in the web, and the response enters baryons weighted by f (Phi = u + f P).  In a spherical
     region: inside (f = 1) the baryon acceleration is nu_mono(g_N/a0) g_N to the grid's accuracy for both sigma; beyond
     the transition (f = 0) it is Newtonian; sigma changes the force only inside the transition layer, by the amount
     reported (L361 said: a thin layer, no force inside a spherical region).
  A6 [the homogeneous zero lies on the off-plateau] the gate W(t) = g(t)/(g(t) + g(1 - t)), g = e^{-1/t} (t > 0),
     vanishes for t <= 0 and every derivative tends to 0 at t -> 0+; on flat FRW the curvature variable R^(3) + sigma^2 = 0,
     so t = 0, f and all its derivatives vanish, M^2 = m^2, and w = Psi = 0: the kernel, its source and the phantom are
     absent from the homogeneous background and from its perturbation theory to every order.  The sqrt(eps) zero-field
     response (XC5 E6) therefore never arises there.  This holds for the curvature-based gate variable; each other
     "door" (matter-only, absolute vs contrast density) must show its own homogeneous background is off-plateau.
  MUTATE=1 removes the gate and the screening from the kernel's source (f -> 1, M -> 0 in the w equation): the kernel
  then reads every baryon, and A3 (L361's equations) must FAIL.  rc = 1.

SCOPE.  Non-relativistic, f prescribed.  The covariant action and its reductions to this Lagrangian, to L340's static
block and to FRW are CV2; the gate varied as an action term (the dark-energy thread's piece) is CV3.  On a closed leaf the
Poisson sources carry the leaf mean (the mean belongs to the FRW background), so the kernel's source is the gated baryon
CONTRAST f (rho_b - <rho_b>); L361 in open space has f rho_b.  They coincide for an isolated system.

Run from the repository root:  python3 real_research/chk_v0_2026/CV1_nr_assembly.py
"""
import os, sys, json, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")      # macOS Accelerate's spurious FP flags (finiteness checked)
import sympy as sp
from scipy.optimize import brentq
from scipy.linalg import expm
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "CV1", "CV1_nr_assembly"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
RNG = np.random.default_rng(20260926)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the kernel's source is ungated and unscreened (f -> 1, M -> 0 in the w equation); A3 must FAIL ***")

# ============================================================================================ A1 the field equations
banner("A1  THE EULER-LAGRANGE EQUATIONS (sympy, one dimension, concrete non-trivial kernel, S = 1)")
x = sp.symbols("x", real=True)
G_, a0_, c1, d1 = sp.symbols("G a0 c1 d1", positive=True)
sig, rdbar = sp.symbols("sigma rhobar_d", real=True)
Phi, u, v, lam, w, Psi = [sp.Function(n)(x) for n in ("Phi", "u", "v", "lam", "w", "Psi")]
rb, rd, f, M2 = [sp.Function(n)(x) for n in ("rho_b", "rho_d", "f", "M2")]
qc = lambda s: c1 * s ** sp.Rational(3, 2) + d1 * sp.log(1 + s)          # q = Q - Z for a concrete kernel
qcp = lambda s: sp.Rational(3, 2) * c1 * sp.sqrt(s) + d1 / (1 + s)       # q'(Z) (= nu - 1 for a real kernel)
d_ = lambda F, n=1: sp.diff(F, x, n)
wp = d_(w); s_w = wp ** 2 / a0_ ** 2
fs, Ms = (sp.Integer(1), sp.Integer(0)) if MUTATE else (f, M2)          # MUTATE: ungated, unscreened source
EPG = 8 * sp.pi * G_


def lagrangian(sigma_):
    return (-(rb + rd) * Phi - (2 * d_(Phi) * d_(u) - d_(u) ** 2) / EPG
            + a0_ ** 2 * f * qc(s_w) / EPG
            + Psi * (d_(w, 2) - Ms * w - fs * (d_(u, 2) - d_(v, 2))) / EPG
            + lam * (d_(v, 2) - 4 * sp.pi * G_ * (rd - rdbar)) / EPG
            - sigma_ * M2 * w ** 2 / EPG)


Lag = lagrangian(sig)
EL = {str(F_.func): sp.expand(sp.euler_equations(Lag, [F_], x)[0].lhs * EPG) for F_ in (Phi, u, v, lam, w, Psi)}
target = {
    "Phi": 2 * d_(u, 2) - EPG * (rb + rd),                                                  # lap u = 4 pi G rho
    "lam": d_(v, 2) - 4 * sp.pi * G_ * (rd - rdbar),                                         # lap v = 4 pi G (rho_d - <rho_d>)
    "Psi": d_(w, 2) - Ms * w - fs * (d_(u, 2) - d_(v, 2)),                                   # (lap - M^2) w = f lap(u - v)
    "w": d_(Psi, 2) - Ms * Psi - 2 * d_(f * qcp(s_w) * wp) - 2 * sig * M2 * w,               # (lap - M^2) Psi = 2 div[f q' grad w] + 2 sigma M^2 w
    "u": 2 * d_(Phi, 2) - 2 * d_(u, 2) - d_(fs * Psi, 2),                                    # lap Phi = lap u + lap(f Psi)/2
    "v": d_(lam, 2) + d_(fs * Psi, 2),                                                       # lap lam = -lap(f Psi)
}
dev = {k_: sp.simplify(EL[k_] - target[k_]) for k_ in target}
for k_ in target:
    P(f"    delta {k_:3s}: residual against the stated field equation = {dev[k_]}")
# the potentials the two species feel: baryons Phi; dark component Phi + lam/2 (its coupling -rho_d Phi - rho_d lam/2)
Pph = sp.Function("P")(x)
Phi_sol = u + fs * Pph                                                                       # from delta u with Psi = 2 P
lam_sol = -2 * fs * Pph                                                                      # from delta v
dark_pot = sp.simplify(Phi_sol + lam_sol / 2 - u)
coup = sp.expand(-sp.diff(Lag, rd) * 1)                                                      # -dL/drho_d = Phi + lam/2
coup_ok = sp.simplify(coup - (Phi + lam / 2)) == 0
P(f"    dark component's coupling -dL/d rho_d = {sp.simplify(coup)}  (= Phi + lam/2: {coup_ok})")
P(f"    on shell Phi = u + f P, lam = -2 f P  ->  dark component's potential - u = {dark_pot}  (Newtonian only)")
OUT["numbers"]["A1"] = {k_: str(v_) for k_, v_ in dev.items()}
check("A1 the Euler-Lagrange equations are the stated field equations: the kernel reads w (gated, screened baryon field), "
      "baryons feel Phi = u + f P, and the dark component feels u (Newtonian only)",
      f"residuals {[str(v_) for v_ in dev.values()]}; dark potential - u = {dark_pot}",
      all(v_ == 0 for v_ in dev.values()) and dark_pot == 0 and coup_ok,
      "baryons couple only to Phi, so matter is minimally coupled; the region kernel's phantom enters the metric potential "
      "through C-H's u-equation, and L353's pair removes it from the dark component's force exactly")

# ============================================================================================ A2 reduction (i)
banner("A2  REDUCTION (i): THE OPERATIVE REQUIREMENT-1 EQUATIONS ON A GATE-ON PLATEAU (f = 1, M = 0, no dark component)")
sub_on = {f: 1, M2: 0, rd: 0, rdbar: 0}
w_on = u - v                                                              # (lap) w = lap(u - v): w = u - v on a closed leaf / decaying BC
eqs_on = {k_: sp.simplify(target[k_].subs(sub_on).doit()) for k_ in ("Phi", "Psi", "w", "u")}
# with rho_d = 0, v = 0 (lap v = 0 on a closed leaf), w = u; Psi = 2 P
res_u = sp.simplify(eqs_on["Phi"] - (2 * d_(u, 2) - EPG * rb))                  # lap u = 4 pi G rho_b
lapPhi = sp.simplify(sp.solve(sp.Eq(eqs_on["u"].subs(Psi, 2 * Pph), 0), d_(Phi, 2))[0])
lapP = sp.simplify(sp.solve(sp.Eq(eqs_on["w"].subs({Psi: 2 * Pph, w: u}).doit(), 0), d_(Pph, 2))[0])
req1 = d_(u, 2) + d_(qcp(d_(u) ** 2 / a0_ ** 2) * d_(u))                        # lap Phi = lap u + div[(nu - 1) grad u]
resid_req1 = sp.simplify(lapPhi.subs(d_(Pph, 2), lapP) - req1)
P(f"    on the plateau: lap u equation residual {res_u}; lap Phi = {lapPhi}; lap P = {lapP}")
P(f"    requirement 1 (operative): lap Phi = 4 pi G rho_b + div[(nu_mono - 1) grad u];  residual = {resid_req1}")
check("A2 on a gate-on plateau the action gives the operative requirement-1 equations exactly (lap u = 4 pi G rho_b, "
      "lap Phi = 4 pi G rho_b + div[(nu - 1) grad u]; with S restored, S* div[(nu - 1) grad S u])",
      f"residuals {res_u}, {resid_req1}", res_u == 0 and resid_req1 == 0,
      "reduction (i) of the cross-thread review's V0 pass criteria; the filter's placement is checked in A4")

# ============================================================================================ A3 reduction (ii) L361
banner("A3  REDUCTION (ii): L361's COMMITTED FIELD EQUATIONS (sigma = 1, S = 1, isolated system)")
phi_, psi_, chi_ = [sp.Function(n)(x) for n in ("phi361", "psi361", "chi361")]
Qc = lambda s: s + qc(s)
L361 = (-(rb + rd) * phi_ - d_(phi_) ** 2 / EPG
        - f * rb * psi_ - (2 * d_(psi_) * wp + 2 * M2 * psi_ * w - a0_ ** 2 * f * Qc(s_w) - (1 - f) * wp ** 2) / EPG
        + f * rb * chi_ + (d_(chi_) ** 2 + M2 * chi_ ** 2) / EPG)                         # verbatim from L361 R0
EL361 = {str(F_.func): sp.expand(sp.euler_equations(L361, [F_], x)[0].lhs * 4 * sp.pi * G_) for F_ in (phi_, psi_, w, chi_)}
# CV1's on-shell configuration mapped into L361's variables: phi = u, chi = w, psi = P + w, with P = Psi/2
on = {rdbar: 0}
subs_map = {phi_: u, chi_: w, psi_: Pph + w}
# CV1's own equations (sigma = 1) solved for the second derivatives they fix
sol_u2 = sp.solve(sp.Eq(target["Phi"].subs(on), 0), d_(u, 2))[0]
sol_w2 = sp.solve(sp.Eq(target["Psi"].subs(on).subs(d_(v, 2), 4 * sp.pi * G_ * rd), 0), d_(w, 2))[0]
sol_P2 = sp.solve(sp.Eq(target["w"].subs(sig, 1).subs(Psi, 2 * Pph).doit(), 0), d_(Pph, 2))[0]
res361 = {}
for k_, e_ in EL361.items():
    r_ = e_.subs(subs_map).doit()
    r_ = r_.subs(d_(Pph, 2), sol_P2).subs(d_(w, 2), sol_w2).subs(d_(u, 2), sol_u2)
    res361[k_] = sp.simplify(r_)
    P(f"    L361 delta {k_:9s} on CV1's solution: residual = {res361[k_]}")
# the forces: L361 baryons feel phi + f (psi - chi) = u + f P = CV1's Phi; the dark component feels phi = u = CV1's
forces_ok = sp.simplify((u + f * ((Pph + w) - w)) - Phi_sol) == 0              # L361's phi + f(psi - chi) vs CV1's Phi
# sigma = 0: the one difference
sol_P2_0 = sp.solve(sp.Eq(target["w"].subs(sig, 0).subs(Psi, 2 * Pph).doit(), 0), d_(Pph, 2))[0]
diff_sigma = sp.simplify(sol_P2 - sol_P2_0)
P(f"    forces species by species identical: {forces_ok};  sigma = 1 minus sigma = 0 in lap P: {diff_sigma}")
OUT["numbers"]["A3"] = {"residuals": {k_: str(v_) for k_, v_ in res361.items()}, "sigma_difference": str(diff_sigma)}
check("A3 at sigma = 1 CV1's solution solves L361's committed Euler-Lagrange equations with zero residual (phi = u, "
      "chi = w, psi = P + w), and each species feels the same potential; sigma = 0 differs by exactly the self-term M^2 w",
      f"residuals {[str(v_) for v_ in res361.values()]}; forces equal {forces_ok}; sigma difference {diff_sigma}",
      all(v_ == 0 for v_ in res361.values()) and forces_ok and sp.simplify(diff_sigma - M2 * w) == 0,
      "L361 = CV1 at sigma = 1 on C-H's chassis: baryons now couple only to the metric potential, and L361's self-term "
      "is one explicit web mass term -sigma M^2 w^2/(8 pi G)")

# ============================================================================================ nu_mono (L340's construction)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e_=1e-6):
    return (h_rar(y * (1 + e_)) - h_rar(y * (1 - e_))) / (2 * y * e_)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
Q_MONO = np.concatenate([[0.0], np.cumsum(0.5 * (H_MONO[1:] + H_MONO[:-1]) * np.diff(YG))])   # int_0^y h ds
def nu_m1(y):                                                                                 # nu_mono - 1 = h/y
    y = np.maximum(np.asarray(y, float), 1e-12); return np.interp(np.log10(y), LYG, H_MONO) / y
def q_mono(Z):                                                                                # q(Z) = 2 int_0^sqrt(Z) h
    y = np.sqrt(np.maximum(np.asarray(Z, float), 1e-24)); return 2.0 * np.interp(np.log10(y), LYG, Q_MONO)

# ============================================================================================ A4 the filter's adjoint
banner("A4  THE FILTER'S ADJOINT: discrete action gradient vs the stated field equations with S^T (periodic grid)")
C1N, D1N = 0.3, 0.5
q_an = lambda Z: C1N * Z ** 1.5 + D1N * np.log1p(Z)                      # A1's analytic kernel, q = Q - Z
qp_an = lambda Z: 1.5 * C1N * np.sqrt(Z) + D1N / (1 + Z)                 # q'(Z)
NG, Lbox = 48, 1.0
hx = Lbox / NG
Dm = (np.roll(np.eye(NG), 1, axis=1) - np.eye(NG)) / hx                  # forward difference, periodic
LAP = -Dm.T @ Dm
Smat = expm(0.5 * (2.5 * hx) ** 2 * LAP)                                 # heat filter, xi = 2.5 cells
Gd, a0d, sgd = 1.0, 1.0, 1.0
fx = 0.5 * (1 + np.tanh((np.cos(2 * np.pi * np.arange(NG) / NG)) * 3))   # a gate profile between 0 and 1
M2x = 30.0 * (1 - fx)
rbx = 1.0 + 0.5 * np.sin(2 * np.pi * np.arange(NG) / NG); rbx -= rbx.mean()
rdx = 0.7 * np.cos(4 * np.pi * np.arange(NG) / NG); rdx -= rdx.mean()
fe = 0.5 * (fx + np.roll(fx, -1))                                        # f on edges


def action(Fv):
    Ph, uu, vv, la, ww, Ps = np.split(Fv, 6)
    Dw = Dm @ (Smat @ ww)
    A = (np.sum(-(rbx + rdx) * Ph) - (2 * (Dm @ Ph) @ (Dm @ uu) - (Dm @ uu) @ (Dm @ uu)) / (8 * np.pi * Gd)
         + a0d ** 2 * np.sum(fe * q_an(Dw ** 2 / a0d ** 2)) / (8 * np.pi * Gd)
         + Ps @ (LAP @ ww - M2x * ww - fx * (LAP @ (uu - vv))) / (8 * np.pi * Gd)
         + la @ (LAP @ vv - 4 * np.pi * Gd * rdx) / (8 * np.pi * Gd)
         - sgd * np.sum(M2x * ww ** 2) / (8 * np.pi * Gd))
    return A * hx


def stated_gradient(Fv):
    Ph, uu, vv, la, ww, Ps = np.split(Fv, 6)
    Dw = Dm @ (Smat @ ww)
    k8 = 1.0 / (8 * np.pi * Gd)
    gPh = -(rbx + rdx) - 2 * k8 * (Dm.T @ (Dm @ uu))
    gu = k8 * (-2 * Dm.T @ (Dm @ Ph) + 2 * Dm.T @ (Dm @ uu)) - k8 * (LAP.T @ (fx * Ps))
    gv = k8 * (LAP.T @ la) + k8 * (LAP.T @ (fx * Ps))
    gla = k8 * (LAP @ vv - 4 * np.pi * Gd * rdx)
    gw = (k8 * 2 * Smat.T @ (Dm.T @ (fe * qp_an(Dw ** 2 / a0d ** 2) * Dw))
          + k8 * (LAP.T @ Ps - M2x * Ps) - k8 * 2 * sgd * M2x * ww)
    gPs = k8 * (LAP @ ww - M2x * ww - fx * (LAP @ (uu - vv)))
    return np.concatenate([gPh, gu, gv, gla, gw, gPs]) * hx


Fv0 = RNG.standard_normal(6 * NG) * 0.3
g_st = stated_gradient(Fv0)
g_fd = np.zeros_like(Fv0); eps_fd = 1e-6
for i_ in range(Fv0.size):
    e_ = np.zeros_like(Fv0); e_[i_] = eps_fd
    g_fd[i_] = (action(Fv0 + e_) - action(Fv0 - e_)) / (2 * eps_fd)
finite4 = bool(np.all(np.isfinite(g_fd)) and np.all(np.isfinite(g_st)) and np.all(np.isfinite(Smat)))
rel = float(np.max(np.abs(g_fd - g_st)) / np.max(np.abs(g_st)))
# control: put S instead of S^T in the w gradient with a NON-symmetric filter, to show the check sees the adjoint
Sns = Smat @ (np.eye(NG) + 0.3 * np.diag(np.linspace(-1, 1, NG)))
rel_ctrl = None
_Ssave = Smat; Smat = Sns
g_fd2 = np.zeros_like(Fv0)
for i_ in range(4 * NG, 5 * NG):
    e_ = np.zeros_like(Fv0); e_[i_] = eps_fd
    g_fd2[i_] = (action(Fv0 + e_) - action(Fv0 - e_)) / (2 * eps_fd)
Ph_, uu_, vv_, la_, ww_, Ps_ = np.split(Fv0, 6)
Dw_ = Dm @ (Sns @ ww_)
k8_ = 1.0 / (8 * np.pi * Gd)
gw_wrong = (k8_ * 2 * Sns @ (Dm.T @ (fe * qp_an(Dw_ ** 2 / a0d ** 2) * Dw_)) + k8_ * (LAP.T @ Ps_ - M2x * Ps_)
            - k8_ * 2 * sgd * M2x * ww_) * hx
rel_ctrl = float(np.max(np.abs(g_fd2[4 * NG:5 * NG] - gw_wrong)) / np.max(np.abs(gw_wrong)))
Smat = _Ssave
P(f"    discrete gradient vs stated equations (with S^T): max relative difference {rel:.2e} over {Fv0.size} components")
P(f"    control: a non-symmetric filter with S in place of S^T in the w equation: relative difference {rel_ctrl:.2e}")
OUT["numbers"]["A4"] = {"rel_diff": rel, "control_rel_diff": rel_ctrl}
check("A4 with the heat filter as a symmetric matrix, the discrete action's gradient equals the "
      "stated field equations (the kernel's force enters as S^T div[f (nu - 1) grad S w]); a wrong adjoint is detected",
      f"max rel. difference {rel:.1e}; wrong-adjoint control {rel_ctrl:.1e}; all finite {finite4}",
      finite4 and rel < 1e-6 and rel_ctrl > 1e-3,
      "the filter sits on both sides of the kernel as in C-H (ACTION.md: S*_N = N^-1 S N at non-constant lapse; CV2)")

# ============================================================================================ A5 C7 named + spherical region
banner("A5  THE SOURCE/FORCE OPERATOR (C7), NAMED, AND ONE SPHERICAL REGION: inside, transition layer, web")
# units: kpc, km/s, Msun;  G in kpc (km/s)^2 / Msun
GK = 4.30091e-6
A0K = 9.3619e-11 * 3.0856775814913673e19 / 1e6                    # canonical a0 in (km/s)^2/kpc
MB, AH = 1e11, 3.0                                                 # Hernquist baryons
RE, DW = 100.0, 20.0                                               # region edge and transition width (kpc)
NR = 24000
rr = np.linspace(0.05, 1600.0, NR); dr = rr[1] - rr[0]


def gate_profile(r):
    t = np.clip((RE + DW - r) / DW, -1, 2)                         # 1 inside RE, 0 beyond RE + DW, C-infinity in between
    g = lambda s: np.where(s > 0, np.exp(-1.0 / np.maximum(s, 1e-300)), 0.0)
    return g(t) / (g(t) + g(1 - t))


rho_b = MB * AH / (2 * np.pi * rr * (rr + AH) ** 3)
fr = gate_profile(rr)


def radial_solve(src, M2r):
    """(1/r^2)(r^2 X')' - M2 X = src; X'(r_min) from regularity, X -> 0 at r_max (screened web)."""
    rp, rm = rr + dr / 2, rr - dr / 2
    lo = rm ** 2 / (rr ** 2 * dr ** 2); up = rp ** 2 / (rr ** 2 * dr ** 2); di = -(lo + up) - M2r
    Am = diags([lo[1:], di, up[:-1]], [-1, 0, 1], format="lil"); b = src.copy()
    Am[0, 0] = -up[0]; Am[0, 1] = up[0]                            # zero flux at the inner edge (regular centre)
    Am[NR - 1, :] = 0; Am[NR - 1, NR - 1] = 1.0; b[NR - 1] = 0.0
    return spsolve(Am.tocsr(), b)


rows5 = {}
ur = radial_solve(4 * np.pi * GK * rho_b, np.zeros(NR))            # u: Newtonian potential of all baryons (unscreened)
gN_enc = np.gradient(ur, dr)                                       # the same discretisation's Newtonian field
for minv in (100.0, 500.0):
    M2r = (1.0 / minv) ** 2 * (1 - fr)
    wr = radial_solve(4 * np.pi * GK * fr * rho_b, M2r)
    wpr = np.gradient(wr, dr)
    flux = rr ** 2 * fr * nu_m1(np.abs(wpr) / A0K) * wpr
    divsrc = np.gradient(flux, dr) / rr ** 2
    res = {}
    for sg_ in (1.0, 0.0):
        Pr = radial_solve(divsrc + sg_ * M2r * wr, M2r)
        gb = gN_enc + np.gradient(fr * Pr, dr)                     # -d/dr of (u + f P): u' = +g_N (attractive convention)
        res[sg_] = gb
    inside = (rr > 2.0) & (rr < RE - 5.0)
    qumond = (1.0 + nu_m1(gN_enc / A0K)) * gN_enc
    err_in = float(np.max(np.abs(res[1.0][inside] / qumond[inside] - 1)))
    layer = (rr >= RE - 5.0) & (rr <= RE + DW + 5.0)
    web = rr > RE + DW + 2.0
    dsig_layer = float(np.max(np.abs(res[1.0][layer] - res[0.0][layer]) / gN_enc[layer]))
    dsig_in = float(np.max(np.abs(res[1.0][inside] - res[0.0][inside]) / gN_enc[inside]))
    web_newt = float(np.max(np.abs(res[1.0][web] / gN_enc[web] - 1)))
    rows5[minv] = {"err_inside_vs_qumond": err_in, "sigma_diff_inside": dsig_in, "sigma_diff_layer": dsig_layer,
                   "web_minus_newton": web_newt}
    P(f"    1/m = {minv:5.0f} kpc: inside |g/g_QUMOND(nu_mono) - 1| <= {err_in:.1e}; sigma = 1 vs 0: inside {dsig_in:.1e}, "
      f"transition layer {dsig_layer:.2e} of g_N; beyond the layer |g/g_N - 1| <= {web_newt:.1e}")
OUT["numbers"]["A5"] = {str(k_): v_ for k_, v_ in rows5.items()}
P("    the operator: SOURCE restricted to the gate-weighted baryon contrast and screened in the web (w), RESPONSE weighted")
P("    by f (Phi = u + f P).  The PM runs mask the response of the all-baryon field; the merger solver restricts the source")
P("    per region; V0's operator is source-restricted + screened + f-weighted response (XR5 compared PM with L361's at")
P("    static scope: <= 2.2e-3 of the phantom monopole).")
check("A5 one spherical region: inside the plateau the baryon acceleration is nu_mono(g_N/a0) g_N (the requirement-1 "
      "law) for both sigma; beyond the transition it is Newtonian; sigma acts only inside the transition layer, where "
      "its effect is order unity in g_N",
      "; ".join(f"1/m = {k_:.0f}: inside {v_['err_inside_vs_qumond']:.1e}, sigma inside {v_['sigma_diff_inside']:.1e}, "
                f"layer {v_['sigma_diff_layer']:.1e}, web {v_['web_minus_newton']:.1e}" for k_, v_ in rows5.items()),
      all(v_["err_inside_vs_qumond"] < 2e-3 and v_["sigma_diff_inside"] < 1e-3 and v_["web_minus_newton"] < 1e-3
          for v_ in rows5.values()),
      "sigma is NOT negligible: inside the edge layer it moves the baryon force by ~1 g_N (a sizeable fraction of the "
      "deep-MOND phantom there), so it is a physical choice at region edges, not bookkeeping.  V0 declares sigma = 1 (L361, "
      "the record's construction, so reduction (ii) is exact); sigma = 0 is the pure (nu - 1) phantom.  Edge-sensitive "
      "observables (L352's compensated lensing profile) must be scored with the sigma they assume")

# ============================================================================================ A6 off-plateau
banner("A6  THE HOMOGENEOUS ZERO LIES ON THE GATE'S OFF-PLATEAU")
t_ = sp.symbols("t", positive=True)
gW = sp.exp(-1 / t_)
Wt = gW / (gW + sp.exp(-1 / (1 - t_)))
lims = [sp.limit(sp.diff(Wt, t_, n_), t_, 0, "+") for n_ in range(0, 5)]
P(f"    W(t) = e^(-1/t)/(e^(-1/t) + e^(-1/(1-t))): lim t->0+ of W^(n), n = 0..4: {lims}  (W = 0 for t <= 0 by definition)")
P("    flat FRW: R^(3) = 0 and sigma_ij = 0, so the curvature variable R = R^(3) + sigma^2 = 0, t = 27 Lambda R/(8 x_c D) = 0,")
P("    f = 0 with every derivative; M^2 = m^2; the w equation (lap - m^2) w = 0 and the Psi equation give w = Psi = 0.")
OUT["numbers"]["A6"] = {"limits": [str(l_) for l_ in lims]}
check("A6 the gate and its first four derivatives vanish as t -> 0+ (and W = 0 for t <= 0): on FRW (R = 0) the kernel, its "
      "source and the phantom are absent to every order of perturbation theory, so XC5 E6's sqrt(eps) never arises there",
      f"limits {lims}", all(l_ == 0 for l_ in lims),
      "for the curvature-based gate variable; each other 'door' must show its own homogeneous background is off-plateau "
      "(the dark-energy thread's piece, CV3); Lean CV1 certifies the flatness to every order (Mathlib's smoothTransition)")

banner("VERDICT")
P(f"""  One non-relativistic Lagrangian on C-H's chassis carries the region kernel and L353's pair with baryons coupled only to
  the metric potential.  Its field equations: the kernel reads w, the gate-weighted baryon field screened in the web;
  baryons feel Phi = u + f P; the dark component feels u (A1).  On a gate-on plateau they are the operative
  requirement-1 equations (A2).  With the explicit web self-term (sigma = 1) they are L361's committed equations with zero
  residual (A3); sigma = 0 is the pure (nu - 1) phantom and differs only inside the transition layer -- but by order
  unity in g_N there, so sigma is a physical edge choice that V0 must declare (A5).  The filter
  enters as S^T div[...] S (A4).  The source/force operator is named: source restricted and screened, response f-weighted
  (A5).  The homogeneous background sits on the gate's exact off-plateau (A6).  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
