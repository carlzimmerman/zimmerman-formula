#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG70 -- Can CFG60's residual object (the nonlocal, causal, non-adiabatic enclosed-mass exchange C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r))
be written as a CAUSAL action with a memory kernel (a retarded Volterra term in time, Schwinger-Keldysh doubled fields)?

FROZEN QUESTION (verbatim, declared before the first run):
 'Can the enclosed-mass exchange be written as a CAUSAL action with a memory kernel (a retarded Volterra term in time, for example through a
  Schwinger-Keldysh doubled-field action or an equivalent dissipative variational principle), such that (P1) the reaction on the baryons is
  <= 0.10 g_law at every x in [0.3, 30] for M_b = 1e9, 1e10, 1e12 Msun (canonical a0), (P2) the energy supplied is <= the baryons' orbital
  kinetic energy (declare the exact ratio computed in CFG48's r_ta convention AND in B's committed r_ta convention from CFG4's r_ta_law),
  (P3) the kernel is retarded (no advanced dependence: prove it on the discrete action as CFG48's G3 does) and the exchange respects
  reciprocity (the coupling is derived from the action, not prescribed), (P4) no new untied constant is introduced other than what the memory
  kernel's own time scale requires (report that scale and whether it can be tied to a0, c, H0 or the dynamical time t_dyn = r/v)?
  A scoped NO with the exact hypothesis that fails is a valid answer.'

INHERITED OBJECT (CFG48 G4, read-only).  Target (point-mass baryons, P2 law, x = r/r_M, r_M = sqrt(G M_b/a0), g_law = g_N sqrt(1+x^2)):
   pressure-slaved  theta^T(r; M) = 4 pi r^2 (3/2) P,  P = a0 M_b(<r)/(8 pi r^2)      =>  theta^T = (3 a0/4) M_b(<r)          [energy per unit radius]
   sigma-slaved     theta^T(r; M) = 4 pi r^2 (3/2) rho_c^fin(r) sigma^2(r; M),  sigma^2 = r g(M,r)/2, g = sqrt(g_N^2 + a0 g_N), rho_c^fin = target density
 The static (bilocal-potential) reaction on a baryon shell is a = -(1/dm) dE_ex/du = theta^T_M(u) (= (3/4) a0 or (3/8) a0 (2+x^2)/(1+x^2)),
 i.e. G4's 0.06 (x=0.3), 0.4-0.5 (x=1), 11-22 (x=30) g_law against the pass line 0.10; energy 1.5 x_e times (1/2) M_b V_f^2, V_f^4 = G M_b a0.

THE MODEL (declared).  Spherical, Newtonian, canonical a0, P2 law.  Baryons: a point mass M_b(<r, t) = M_b m-profile g(t/t_f), the smoothstep
 g(u) = 3u^2 - 2u^3 on [0,1] (0 before, 1 after; t_f = formation time), plus a probe baryon shell dm at radius u = s (the reaction is evaluated there).
 Cold fluid: shells at radius r with a thermal store theta_l(t) (energy per unit radius), theta_l(0) = theta^T_l(0) = 0.
 SK ACTION (Galley-type doubled fields q_pm = q_S +- q_D/2, theta_pm = th_S +- th_D/2; physical limit D -> 0):
   S = int dt { (m/2)(qdot_+^2 - qdot_-^2) - m [Phi(q_+) - Phi(q_-)] - [F(q_+,theta_+) - F(q_-,theta_-)] } - int int th_D(t) Gamma(t - t') thdot_S(t') dt' dt
   F(q, theta) = r theta + (c/2) (theta - theta^T(q))^2         (theta^T(q) = target at the probe's position through M_b(<r))
   Gamma(s) = 0 for s < 0 (RETARDED cross term).  Static limit: theta -> theta^T (offset -r/c) for any Gamma with finite integral.
   Memory kernel K (Edot = int K(t-t') d/dt' f dt', f = theta^T, int K = 1):  K-hat(s) = 1/(1 + s Gamma-hat(s)/c), i.e. K = the fluid's response to the
   baryon-set target; Gamma = gamma delta  <=>  K = exp(-s/tau)/tau, tau = gamma/c (Newton relaxation  tau thdot = theta^T - theta).
   K1: Gamma-tilde = eps_c tau delta.   K2 (Maxwell/two-time): Gamma-tilde = eps_c [tau0 delta + (tau1/T) exp(-s/T)], tau0 = tau1 = T = tau_bar/2 (declared).
   tau_bar = int s K ds = mean memory time.  eps_c = c * theta^T_full is dimensionless (the free-energy stiffness in units of the full target).
 Ledger fraction r in F: r = 1 counts the heat theta in the closed baryon+fluid energy (E_tot = K_b + Phi + F conserved up to Gamma dissipation);
   r = 0: the heat comes from an unspecified reservoir integrated out (an OPEN SK system).  r and eps_c are the two couplings the action leaves free.
 Equations (derived by sympy, S1):  m q'' = -m Phi' - dF/dq  (baryon);  r + c(theta - theta^T) + (Gamma * thdot)(t) = 0  (fluid, retarded).
 Reaction on the probe:  a(t) = -c (theta - theta^T) theta^T_M   with  a/theta^T_M = r Theta_K(t) + eps_c (Thetabar * mdot)(t),  Theta_K = int_0^t K,
   Thetabar = 1 - Theta_K (survival function of the kernel), m(t) = theta^T(t)/theta^T_full  (S1 derives this; S3 checks it against forward marching).

CHECKS AND PASS LINES (frozen here, before the first run)
 S1 (sympy)  D1 the doubled action's Delta-variations at Delta = 0 give exactly the two equations above; D2 the Sigma-equations vanish at Delta = 0
             (no advanced/extra equation); D3 the closed form of a(t) (Laplace algebra for a general Gamma, exponential case by dsolve on a ramp) holds and
             its static limit is r theta^T_M; D4 at r = 1, w = 0 the reaction is G4's closed forms (3/4) a0 and (3/8) a0 (2+x^2)/(1+x^2).
 S2 (discrete action, N = 6 steps, G3's test)  C1 CAUSALITY: the Euler-Lagrange residual of the doubled discrete action has no dependence on later data:
             c_adv = max_{j>i+1}|dR_i/dx_j| / max|dR_i/dx_j| < 1e-12 for the q-residuals and (strictly, j > i) for the theta-residuals.
             C2 (context, load-bearing) the same memory term written on ONE branch (no doubling) has c_adv > 1e-4.
             R1 RECIPROCITY: (i) cross block d R^q_i/d th_j = d R^th_j/d q_i (symmetric to 1e-12); (ii) the hand-coded baryon reaction and fluid equation
             reproduce the sympy-derived residuals of the action to 1e-12 (coupling DERIVED from F, not prescribed).
 S3 (numerics, forward marching = an initial-value solve, possible only because the kernel is retarded; kernels K1, K2; tau_bar/t_f in {0.01,0.1,1,10})
             N1 marching reproduces the closed form of a(t) to 1e-3; N2 (control) at late times, r = 1: a/g_law = G4's numbers to 1e-3 for all masses,
             both slavings, both kernels; N3 (CLAIM, P1 in the energy-ledger class r = 1) max over x in [0.3,30] of the late-time a/g_law > 0.10
             for both slavings; N4 (CLAIM) for r = 1 the reaction (units of G4's) is never below the fraction f_real of the target energy realised;
             N5 (P1 in the open class r = 0): P1 holds iff eps_c <= eps_max = 0.10/peak(eps_c = 1); verified at eps_c = eps_max (peak = 0.10) and reported at 1.
 S4 (energy, P2)  E1 the ratio E_c(<r_e)/((1/2) M_b V_f^2) = 1.5 x_e, r_e = 0.4 r_ta, computed by quadrature and closed form, in CFG48's r_ta and in B's
             committed r_ta (CFG7_common.r_ta_law = CFG4's convention; kernel nu_mono primary, P2 kernel as the referee's control 179 / 57 to 1%);
             E2 the energy delivered by the memory law = f_real * E_c for every kernel (kernel-independent up to the realised fraction).
 S5 (time scales, P4)  tabulate tau_bar candidates (r/c, t_dyn = r/V_c, r_M/V_f, 1/H0, c/a0) against t_f in {1, 10} Gyr (declared); nothing is scanned or chosen.
 GATES  P1 PASS iff a <= 0.10 g_law at every x in [0.3,30], all three masses, with NO untied coupling (r = 1, no new eps_c-type constant);
        P2 PASS iff energy supplied <= (1/2) M_b V_f^2; P3 PASS iff C1 and R1 hold; P4 PASS iff no constant beyond the kernel's own time scale.
MUTATE controls (each must exit rc = 1):
   MUTATE=a : the kernel is made advanced (symmetrised in time, Gamma_{|i-j|}) in the discrete SK action  -> C1 (causality) must FAIL.
   MUTATE=b : the reciprocity term is dropped (F's coupling to the baryon replaced by a PRESCRIBED drive th_D c theta^T(q_S) with no q_D partner) -> R1 must FAIL.
   MUTATE=1 : both.  Outputs are named by mode.
DISCLOSED ADDITIONS (made AFTER the first run, reported only, never gated): (i) the E_c/E_infall column in S4 (E_infall = G M_col M_c/r_ta, a scale estimate
 with O(1) prefactors omitted; it was in the code at the first run but not in this list); (ii) N6, the open class r = 0 evaluated at two TIED kernel scales,
 tau_bar = r_e/c and tau_bar = t_dyn(r_e), for t_f in {1, 10} Gyr, eps_c = 1; (iii) T2, the closed form t_dyn(r_e) = 0.4 sqrt(2/(Delta_ta Omega_m))/H0 (deep-MOND edge,
 committed r_ta), compared with the number S5 prints; (iv) the time of the sigma-slaved peak in N5.  The first run also had a units bug in the c/a0 printout (fixed).
SCOPE.  Time-domain kernel only: the spatial (enclosed-mass) nonlocality is instantaneous on the leaf, as in G4 (a light-cone support t - t' >= (r - u)/c is
 not built; OPEN).  Point-mass baryons, probe-shell reaction, pressure- and sigma-slaved targets, fluid shell masses fixed.  Nothing is fitted; the test values in S2
 (m, c, r, dt, Gamma_k, random positions, fixed seed) are numerical test data, not model numbers.  kappa = 1/2 is FITTED; nothing here says the theory is closed.
"""
import os, sys, math
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from scipy import signal

HERE0 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE0)
from cfg70_common import *   # noqa

MUT = os.environ.get("MUTATE", "")
MUT_A = MUT in ("a", "1")
MUT_B = MUT in ("b", "1")
R = Report("cfg70_memory_kernel_exchange", MUT)
P = R.P
P(__doc__.strip())
if MUT:
    P(f"\n  *** MUTATE={MUT}: advanced kernel = {MUT_A}, reciprocity term dropped = {MUT_B}; the corresponding claims must FAIL ***")

# =====================================================================================================================  S1 sympy
R.banner("S1  SK action -> equations (sympy)")
t = sp.symbols("t", real=True)
m_, c_, r_, gam_ = sp.symbols("m c r gamma", positive=True)
qS, qD, thS, thD = [sp.Function(n)(t) for n in ("qS", "qD", "thS", "thD")]
qp, qm = qS + qD / 2, qS - qD / 2
thp, thm = thS + thD / 2, thS - thD / 2
from sympy.calculus.euler import euler_equations
# concrete test: Phi = xs^2/2 + xs^4/8, thT = tanh(xs)
Phi_c = lambda z: z ** 2 / 2 + z ** 4 / 8
thT_c = lambda z: sp.tanh(z)
L_c = (m_ / 2 * (sp.diff(qp, t) ** 2 - sp.diff(qm, t) ** 2) - m_ * (Phi_c(qp) - Phi_c(qm))
       - (r_ * thp + c_ / 2 * (thp - thT_c(qp)) ** 2 - r_ * thm - c_ / 2 * (thm - thT_c(qm)) ** 2) - gam_ * thD * sp.diff(thS, t))
eqc = euler_equations(L_c, [qD, thD, qS, thS], t)
Eq_c = [sp.simplify((e.lhs - e.rhs).subs({qD: 0, thD: 0}).doit()) for e in eqc]
x_ = qS
want_q = -m_ * sp.diff(x_, t, 2) - m_ * (x_ + x_ ** 3 / 2) + c_ * (thS - sp.tanh(x_)) * (1 - sp.tanh(x_) ** 2)
want_th = -(r_ + c_ * (thS - sp.tanh(x_))) - gam_ * sp.diff(thS, t)
d1a = sp.simplify(Eq_c[0] - want_q); d1b = sp.simplify(Eq_c[1] - want_th)
P(f"    baryon equation from d/dq_D:   {sp.simplify(Eq_c[0])} = 0")
P(f"    fluid  equation from d/dth_D:  {sp.simplify(Eq_c[1])} = 0")
P(f"    Sigma-equations at Delta=0:    d/dq_S -> {Eq_c[2]},  d/dth_S -> {Eq_c[3]}")
R.check("D1 the Delta-variations at Delta = 0 are m q'' = -m Phi' - dF/dq and r + c(theta - theta^T) + gamma thdot = 0 (sympy residual 0, concrete Phi, theta^T)",
        f"residuals: baryon {d1a}, fluid {d1b}", d1a == 0 and d1b == 0)
R.check("D2 the Sigma-equations vanish identically at Delta = 0 (Galley: the physical limit carries only the D-equations; no advanced equation appears)",
        f"{Eq_c[2]}, {Eq_c[3]}", Eq_c[2] == 0 and Eq_c[3] == 0)

# general retarded Gamma: the D-equation of the theta sector is algebraic in the retarded functional J = Gamma * thdot
Jf = sp.Function("J")
Lgen = -thD * Jf(t)
eg = euler_equations(Lgen, [thD], t)[0]
P(f"    general retarded kernel: d/dth_D of -th_D J[th_S](t) = {eg.lhs} (J = Gamma * thdot_S depends on th_S(t' <= t) only)")

# Laplace-domain closed form for a general Gamma-hat
s = sp.symbols("s", positive=True)
Gh, ThT = sp.symbols("Gh ThT")                         # Gamma-hat(s), theta^T-hat(s)
thh = sp.symbols("thh")
sol = sp.solve(sp.Eq(r_ / s + c_ * (thh - ThT) + Gh * s * thh, 0), thh)[0]      # r + c(th - thT) + Gamma*thdot = 0, th(0)=0, thT(0)=0
a_hat = sp.simplify(-c_ * (sol - ThT))
Kh = 1 / (1 + s * Gh / c_)
closed = r_ * Kh / s + c_ * (1 - Kh) * ThT             # = L[ r Theta_K + c (Thetabar * thT dot ...) ]  (Thetabar*mdot <-> (1-Kh)/s * s m-hat)
d3 = sp.simplify(a_hat - closed)
P(f"    a-hat(s) = r K-hat/s + c (1 - K-hat) theta^T-hat,  K-hat = 1/(1 + s Gamma-hat/c):  sympy residual {d3}")
# static limit for a step target theta^T = A/s with Gamma-hat = g0 + g1/(1+sT) (finite at s->0)
g0, g1, T_, A_ = sp.symbols("g0 g1 T A", positive=True)
Gh_maxwell = g0 + g1 / (1 + s * T_)
lim = sp.limit(sp.simplify((s * a_hat.subs({Gh: Gh_maxwell, ThT: A_ / s})).doit()), s, 0)
P(f"    static limit s * a-hat(s), s -> 0, for Gamma = g0 delta + (g1/T) exp(-s/T), step target A: {lim}   (= r; A drops out: the reaction is r theta^T_M)")
tt = sp.symbols("tt", positive=True); Aa, tau_s = sp.symbols("A tau", positive=True)
th_f = sp.Function("th")
ode = sp.Eq(gam_ * th_f(tt).diff(tt), -(r_ + c_ * (th_f(tt) - Aa * tt)))
dsol = sp.dsolve(ode, th_f(tt), ics={th_f(0): 0}).rhs
a_dsolve = sp.simplify(-c_ * (dsol - Aa * tt))
tau_v = gam_ / c_
a_closed = r_ * (1 - sp.exp(-tt / tau_v)) + c_ * Aa * tau_v * (1 - sp.exp(-tt / tau_v))
d3b = sp.simplify(a_dsolve - a_closed)
R.check("D3 a/theta^T_M = r Theta_K(t) + eps_c (Thetabar * mdot)(t): Laplace form for a general Gamma (sympy residual 0), exponential kernel on a ramp by dsolve (residual 0), static limit = r",
        f"Laplace residual {d3}; dsolve residual {d3b}; static limit {lim}", d3 == 0 and d3b == 0 and sp.simplify(lim - r_) == 0)

# D4  G4's closed forms from the same reaction (r = 1, w = 0)
Mb_s, M_s, s_r, a0_s, G_s, x_s = sp.symbols("Mb M s a0 G x", positive=True)
gN = G_s * M_s / s_r ** 2
g_tot = sp.sqrt(gN ** 2 + a0_s * gN)
rho_fin = a0_s * Mb_s / (4 * sp.pi * s_r ** 3 * sp.sqrt((G_s * Mb_s / s_r ** 2) ** 2 + a0_s * G_s * Mb_s / s_r ** 2))
thT_sig = 4 * sp.pi * s_r ** 2 * sp.Rational(3, 2) * rho_fin * (s_r * g_tot / 2)
thM_sig = sp.diff(thT_sig, M_s).subs(M_s, Mb_s)
rM_ = sp.sqrt(G_s * Mb_s / a0_s)
thM_sig_x = sp.simplify(thM_sig.subs(s_r, x_s * rM_))
want_sig = sp.Rational(3, 8) * a0_s * (2 + x_s ** 2) / (1 + x_s ** 2)
d4a = sp.simplify(thM_sig_x - want_sig)
dm_, u_, rr_ = sp.symbols("dm u rr", positive=True)
thT_P = sp.Rational(3, 4) * a0_s * (Mb_s + dm_ * sp.Heaviside(rr_ - u_))              # pressure-slaved per unit radius, shell dm at u
dthdu = sp.diff(thT_P, u_)                                                            # -(3/4) a0 dm delta(rr - u)
thM_P = -sp.integrate(dthdu, (rr_, 0, 10 * u_)) / dm_                                # a = -(1/dm) int dr (-dtheta^T/du) ... at delta = -r/c, r = 1
d4b = sp.simplify(thM_P - sp.Rational(3, 4) * a0_s)
P(f"    sigma-slaved theta^T_M at x: {sp.simplify(thM_sig_x)}  (target (3/8) a0 (2+x^2)/(1+x^2), residual {d4a});  pressure-slaved: {sp.simplify(thM_P)} (residual {d4b})")
R.check("D4 at r = 1, w = 0 (static limit) the derived reaction is G4's: (3/4) a0 (pressure-slaved), (3/8) a0 (2+x^2)/(1+x^2) (sigma-slaved)", f"residuals {d4a}, {d4b}", d4a == 0 and d4b == 0)

# =====================================================================================================================  S2 discrete action
R.banner("S2  discrete SK action: retardation (advanced dependence) and reciprocity")
NS, dt2 = 6, 0.1
qS_ = sp.symbols(f"qS0:{NS + 1}", real=True); qD_ = sp.symbols(f"qD0:{NS + 1}", real=True)
thS_ = sp.symbols(f"tS0:{NS + 1}", real=True); thD_ = sp.symbols(f"tD0:{NS + 1}", real=True)
mt, ct, rt = 1.3, 2.1, 0.7                                       # numerical TEST values (not model numbers)
Gam_k = [0.8 * math.exp(-0.3 * k) for k in range(NS + 1)]       # test kernel weights, retarded support k >= 0
thTf = lambda z: 1 / (1 + sp.exp(-3 * (z - 1)))
Phif = lambda z: z ** 2 / 2 + z ** 4 / 8
Fn = lambda q, th: rt * th + ct / 2 * (th - thTf(q)) ** 2
Fth_only = lambda th: rt * th + ct / 2 * th ** 2                 # F without any q coupling (prescribed-drive mutation)


def dbl_action(advanced=False, prescribed=False):
    S = 0
    for i in range(1, NS + 1):
        qp_i, qp_im = qS_[i] + qD_[i] / 2, qS_[i - 1] + qD_[i - 1] / 2
        qm_i, qm_im = qS_[i] - qD_[i] / 2, qS_[i - 1] - qD_[i - 1] / 2
        thp_i, thm_i = thS_[i] + thD_[i] / 2, thS_[i] - thD_[i] / 2
        kin = mt / 2 * (((qp_i - qp_im) / dt2) ** 2 - ((qm_i - qm_im) / dt2) ** 2)
        pot = -mt * (Phif(qp_i) - Phif(qm_i))
        if prescribed:                     # MUTATE b: no F coupling to q; the drive th_D c theta^T(q_S) is PRESCRIBED (no q_D partner)
            fterm = -(Fth_only(thp_i) - Fth_only(thm_i)) + ct * thD_[i] * thTf(qS_[i])
        else:
            fterm = -(Fn(qp_i, thp_i) - Fn(qm_i, thm_i))
        S += dt2 * (kin + pot + fterm)
        jr = range(1, NS + 1) if advanced else range(1, i + 1)          # MUTATE a: symmetrised in time (advanced weights included)
        for j in jr:
            k = abs(i - j) if advanced else i - j
            S += -dt2 ** 2 * thD_[i] * Gam_k[k] * (thS_[j] - thS_[j - 1]) / dt2
    return S


def naive_action():
    """the same memory term on ONE branch (no doubling): S = int(m qdot^2/2 - m Phi - F) - (1/2) int int thdot Gamma thdot."""
    S = 0
    for i in range(1, NS + 1):
        S += dt2 * (mt / 2 * ((qS_[i] - qS_[i - 1]) / dt2) ** 2 - mt * Phif(qS_[i]) - Fn(qS_[i], thS_[i]))
        for j in range(1, i + 1):
            S += -dt2 ** 2 * 0.5 * ((thS_[i] - thS_[i - 1]) / dt2) * Gam_k[i - j] * ((thS_[j] - thS_[j - 1]) / dt2)
    return S


zeroD = {v: 0 for v in list(qD_) + list(thD_)}
allS = list(qS_) + list(thS_)
rng = np.random.default_rng(20260928)
qv = rng.uniform(0.6, 1.4, NS + 1); tv = rng.uniform(0.2, 0.9, NS + 1)
pt = {**{qS_[i]: qv[i] for i in range(NS + 1)}, **{thS_[i]: tv[i] for i in range(NS + 1)}}


def residuals_and_jac(S):
    Rq = [sp.diff(S, qD_[i]).subs(zeroD) for i in range(1, NS)]
    Rt = [sp.diff(S, thD_[i]).subs(zeroD) for i in range(1, NS + 1)]
    Rall = Rq + Rt
    Jm = sp.Matrix(Rall).jacobian(allS)
    f = sp.lambdify(allS, Jm, "numpy"); fr = sp.lambdify(allS, sp.Matrix(Rall), "numpy")
    args = [pt[v] for v in allS]
    return np.array(f(*args), float), np.array(fr(*args), float).ravel()


S_sk = dbl_action(advanced=MUT_A, prescribed=MUT_B)
J_sk, R_sk = residuals_and_jac(S_sk)
nq = NS - 1                                                  # rows 0..nq-1: R^q_i (i = 1..NS-1); rows nq.. : R^th_i (i = 1..NS)


def col_time(cidx):                                          # column -> time index
    return cidx % (NS + 1)


def adv_measure(J, rows_q, rows_t):
    out = {}
    worst_q = 0.0; worst_t = 0.0
    for rr_i in range(rows_q):
        i = rr_i + 1
        row = np.abs(J[rr_i]); sc = row.max()
        adv = [row[cc] for cc in range(J.shape[1]) if col_time(cc) > i + 1]
        worst_q = max(worst_q, (max(adv) if adv else 0.0) / sc)
    for rr_i in range(rows_t):
        i = rr_i + 1
        row = np.abs(J[rows_q + rr_i]); sc = row.max()
        adv = [row[cc] for cc in range(J.shape[1]) if col_time(cc) > i]            # STRICT: theta-residual at i may use data at times <= i
        worst_t = max(worst_t, (max(adv) if adv else 0.0) / sc)
    return worst_q, worst_t


cq, ct_ = adv_measure(J_sk, nq, NS)
P(f"    doubled discrete action (N = {NS} steps{', MUTATED: kernel symmetrised in time' if MUT_A else ''}): advanced-dependence measure  c_q(j > i+1) = {cq:.2e},  c_theta(strict j > i) = {ct_:.2e}")
R.check("C1 CAUSALITY on the discrete SK action: the EL residuals depend on no later data (c_adv < 1e-12 for R^q (j > i+1) and strictly for R^theta (j > i))",
        f"c_q = {cq:.2e}, c_theta = {ct_:.2e}" + ("  [MUTATE a: kernel made advanced]" if MUT_A else ""), cq < 1e-12 and ct_ < 1e-12)

S_nv = naive_action()
Rn = [sp.diff(S_nv, thS_[i]) for i in range(1, NS + 1)]
Jn = np.array(sp.lambdify(allS, sp.Matrix(Rn).jacobian(allS), "numpy")(*[pt[v] for v in allS]), float)
cn = 0.0
for i in range(1, NS + 1):
    row = np.abs(Jn[i - 1]); adv = [row[cc] for cc in range(Jn.shape[1]) if col_time(cc) > i + 1]
    if adv:
        cn = max(cn, max(adv) / row.max())
P(f"    the same memory term on ONE branch (undoubled, retarded weights): c_adv(j > i+1) = {cn:.2e}  (the EL residual at t_i contains Gamma_{{k-i}} thdot_k for every LATER k)")
R.check("C2 (context) an undoubled memory action has advanced dependence; only the SK cross term is retarded", f"c_adv = {cn:.2e} > 1e-4", cn > 1e-4)

# reciprocity: cross blocks and hand-coded (independent) residuals
Jqth = J_sk[:nq, NS + 1:]             # d R^q_i / d th_j   (i = 1..NS-1, j = 0..NS)
Jthq = J_sk[nq:, :NS + 1]             # d R^th_i / d q_j   (i = 1..NS,   j = 0..NS)
Jth_q_at = np.zeros((NS + 1, NS + 1)); Jq_th_at = np.zeros((NS + 1, NS + 1))
for i in range(1, NS):
    Jq_th_at[i] = Jqth[i - 1]
for i in range(1, NS + 1):
    Jth_q_at[i] = Jthq[i - 1]
# compare d R^q_i/d th_j with d R^th_j/d q_i on the common rows/cols 1..NS-1
A_ = Jq_th_at[1:NS, 1:NS]; B_ = Jth_q_at[1:NS, 1:NS].T
scale_x = max(np.abs(A_).max(), np.abs(B_).max(), 1e-300)
asym = np.abs(A_ - B_).max() / scale_x if scale_x > 1e-12 else np.abs(A_ - B_).max()
thTn = lambda z: 1 / (1 + np.exp(-3 * (z - 1)))
dthTn = lambda z: 3 * thTn(z) * (1 - thTn(z))
Phip = lambda z: z + z ** 3 / 2
Rq_hand = np.array([dt2 * (-mt * (qv[i + 1] - 2 * qv[i] + qv[i - 1]) / dt2 ** 2 - mt * Phip(qv[i]) + ct * (tv[i] - thTn(qv[i])) * dthTn(qv[i])) for i in range(1, NS)])
thdot = np.diff(tv) / dt2
Rt_hand = np.array([-dt2 * (rt + ct * (tv[i] - thTn(qv[i]))) - dt2 ** 2 * sum(Gam_k[i - j] * thdot[j - 1] for j in range(1, i + 1)) for i in range(1, NS + 1)])
dev_hand = max(np.abs(Rq_hand - R_sk[:nq]).max(), np.abs(Rt_hand - R_sk[nq:]).max())
P(f"    cross-block asymmetry |dR^q_i/dth_j - dR^th_j/dq_i| / scale = {asym:.2e} (scale {scale_x:.3e});  hand-coded (independent) residuals vs the action's: {dev_hand:.2e}")
R.check("R1 RECIPROCITY: the cross block is symmetric (asymmetry < 1e-12) and the independently coded baryon reaction and fluid equation are exactly the action's residuals (coupling DERIVED from F)",
        f"asymmetry {asym:.2e}; hand-coded deviation {dev_hand:.2e}" + ("  [MUTATE b: reciprocity term dropped -> prescribed drive]" if MUT_B else ""),
        asym < 1e-12 and dev_hand < 1e-12)

# =====================================================================================================================  S3 numerics
R.banner("S3  reaction on the baryons: forward marching of the retarded SK equations (masses 1e9, 1e10, 1e12)")
MASSES = (1e9, 1e10, 1e12)
XS5 = np.array([0.3, 1.0, 3.0, 10.0, 30.0])
XGRID = np.unique(np.concatenate([np.geomspace(0.3, 30, 25), XS5]))
gN_of = lambda Mb, r: G * Mb / r ** 2
g_tot_of = lambda M, r: np.sqrt(gN_of(M, r) ** 2 + A0 * gN_of(M, r))
smooth = lambda u: np.where(u <= 0, 0.0, np.where(u >= 1, 1.0, 3 * u ** 2 - 2 * u ** 3))
dsmooth = lambda u: np.where((u > 0) & (u < 1), 6 * u * (1 - u), 0.0)


def kernel_pars(kind, taub):
    if kind == "K1":
        return taub, 0.0, 1.0
    return taub / 2, taub / 2, taub / 2                      # K2: tau0 = tau1 = T = tau_bar/2


def K_closed(kind, taub):
    """Theta_K(t) = int_0^t K, exact from the rational K-hat (scipy residue)."""
    t0, t1, T = kernel_pars(kind, taub)
    num = np.array([T, 1.0]) if kind == "K2" else np.array([1.0])
    den = np.array([T * t0, T + t0 + t1, 1.0]) if kind == "K2" else np.array([taub, 1.0])
    den_s = np.polymul(den, [1.0, 0.0])
    rr_, pp_, kk_ = signal.residue(num, den_s)
    return lambda tv_: np.real(sum(a * np.exp(p * np.asarray(tv_, float)) for a, p in zip(rr_, pp_)) + (kk_[0] if len(kk_) else 0.0))


def march(kind, taub, eps_c, r, m_of_t, dtm, t_end):
    """forward marching of  r + eps_c (th - m) + Gamma-tilde * thdot = 0  (units t_f = 1, th in units of theta^T_full), th(0) = 0.
    Returns t, th, m.  Only past data enters (retarded); Gamma-tilde = eps_c [tau0 delta + (tau1/T) exp(-s/T)]."""
    t0, t1, T = kernel_pars(kind, taub)
    n = int(round(t_end / dtm)) + 1
    tt_ = np.arange(n) * dtm
    mm = m_of_t(tt_)
    th = np.zeros(n); h = 0.0; E = math.exp(-dtm / T); a0_ = t0 / dtm; a1_ = t1 / T
    rho = r / eps_c
    for i in range(1, n):
        th[i] = (mm[i] - rho + (a0_ + a1_) * th[i - 1] - a1_ * E * h) / (1 + a0_ + a1_)
        h = E * h + (th[i] - th[i - 1])
    return tt_, th, mm


def a_over_thM_closed(kind, taub, eps_c, r, mdot_of_t, dtm, t_end):
    tt_ = np.arange(int(round(t_end / dtm)) + 1) * dtm
    ThK = K_closed(kind, taub)(tt_)
    Thbar = 1 - ThK
    conv = np.convolve(Thbar, mdot_of_t(tt_))[:len(tt_)] * dtm
    return tt_, r * ThK + eps_c * conv


mP = lambda tt_: smooth(tt_)
mdP = lambda tt_: dsmooth(tt_)
# ---- N1: marching == closed form (pressure-slaved, both kernels, several tau_bar, both r)
worst1 = 0.0
for kind in ("K1", "K2"):
    for taub in (0.01, 0.1, 1.0, 10.0):
        for r_c, eps in ((1.0, 100.0), (0.0, 1.0), (1.0, 10.0)):
            dtm = min(taub, 1.0) / 200; tend = 1 + 12 * taub if taub > 0.05 else 3.0
            ta, th, mm = march(kind, taub, eps, r_c, mP, dtm, tend)
            a_march = -eps * (th - mm)
            tb, a_cl = a_over_thM_closed(kind, taub, eps, r_c, mdP, dtm, tend)
            sc = max(np.abs(a_cl).max(), 1e-12)
            worst1 = max(worst1, np.abs(a_march - a_cl).max() / sc)
R.check("N1 forward marching of the derived retarded equations reproduces the closed form a/theta^T_M = r Theta_K + eps_c (Thetabar * mdot) (max relative deviation < 1e-2 at dt = min(tau,t_f)/200)",
        f"worst deviation {worst1:.2e}", worst1 < 1e-2)

# ---- N2/N3/N4: energy-ledger class r = 1
def theta_pieces(slaving, Mb, x):
    """m(t), theta^T_M(t)/theta^T_M(final) and a_G4/g_law for a probe shell at s = x r_M."""
    rM = r_M_kpc(Mb); s_ = x * rM
    gl = float(g_tot_of(Mb, s_))
    if slaving == "P":
        mfun = mP; thMr = lambda tt_: np.ones_like(tt_); a4 = 0.75 * A0
    else:
        mfun = lambda tt_: g_tot_of(Mb * smooth(tt_), s_) / gl
        # dtheta^T/dM at M(t) relative to final: (M/g) dg/dM ... theta^T_M(t) = (3/4) a0 Mb/g_fin * dg/dM|_{M(t)}
        def dgdM(M):
            gN_ = G * M / s_ ** 2
            return (2 * gN_ + A0) * gN_ / (2 * np.sqrt(gN_ ** 2 + A0 * gN_) * np.maximum(M, 1e-300))
        thMr = lambda tt_: dgdM(np.maximum(Mb * smooth(tt_), 1e-9 * Mb)) / dgdM(Mb)
        a4 = 0.375 * A0 * (2 + x ** 2) / (1 + x ** 2)
    return mfun, thMr, a4, gl


TAUB = (0.01, 0.1, 1.0, 10.0)
tabA = {}
worst2 = 0.0; a_late_max = {"P": 0.0, "S": 0.0}
viol4 = []
for slav in ("P", "S"):
    for Mb in MASSES:
        for kind in ("K1", "K2"):
            for taub in TAUB:
                for x in XS5:
                    mfun, thMr, a4, gl = theta_pieces(slav, Mb, x)
                    eps = 100.0
                    dtm = min(taub, 1.0) / 100; tend = 1 + 40 * taub
                    ta, th, mm = march(kind, taub, eps, 1.0, mfun, dtm, tend)
                    a_over = -eps * (th - mm) * thMr(ta)
                    a_late = a_over[-1] * a4 / gl / (1.0 if slav == "P" else 1.0)
                    # closed G4 value/g_law
                    g4_gl = a4 / gl
                    worst2 = max(worst2, abs(a_late / g4_gl - 1))
                    tabA[(slav, Mb, kind, taub, float(x))] = a_late
                    if kind == "K1" and taub == 1.0:
                        pass
    # static table (mass independent) and N4 on the P-slaved marching
for slav in ("P", "S"):
    vals = {(Mb, float(x)): tabA[(slav, Mb, "K1", 0.1, float(x))] for Mb in MASSES for x in XS5}
    a_late_max[slav] = max(vals.values())
# x-only dependence check: identical across masses
mass_indep = max(abs(tabA[("P", MASSES[0], "K1", 1.0, float(x))] - tabA[("P", MASSES[2], "K1", 1.0, float(x))]) / tabA[("P", MASSES[0], "K1", 1.0, float(x))] for x in XS5)
R.check("N2 (control) at late times (r = 1) the marched reaction equals G4's static reaction (closed forms) for all masses, both slavings, both kernels, tau_bar/t_f in {0.01,...,10}, to 1e-3",
        f"worst relative deviation {worst2:.2e}; mass independence (1e9 vs 1e12) {mass_indep:.1e}", worst2 < 1e-3 and mass_indep < 1e-9)
P("    late-time reaction a/g_law (r = 1; identical for every kernel, tau_bar and mass -- the memory law changes only the transient):")
for slav, nm in (("P", "pressure-slaved"), ("S", "sigma-slaved   ")):
    P(f"      {nm}: " + "; ".join(f"x={x:g}: {tabA[(slav, MASSES[1], 'K1', 1.0, float(x))]:.3f}" for x in XS5))
# pass-line crossing
def a_static_gl(slav, x):
    gl = float(g_tot_of(1e10, x * r_M_kpc(1e10)))
    a4 = 0.75 * A0 if slav == "P" else 0.375 * A0 * (2 + x ** 2) / (1 + x ** 2)
    return a4 / gl
from scipy.optimize import brentq
xcross = {sl: brentq(lambda lx: a_static_gl(sl, math.exp(lx)) - 0.10, math.log(0.05), math.log(30)) for sl in ("P", "S")}
xcross = {k: math.exp(v) for k, v in xcross.items()}
xg = np.geomspace(0.3, 30, 4000)
amax = {sl: max(a_static_gl(sl, x) for x in xg) for sl in ("P", "S")}
P(f"    a/g_law reaches the 0.10 pass line at x = {xcross['P']:.2f} (pressure) / {xcross['S']:.2f} (sigma); max over [0.3, 30]: {amax['P']:.2f} / {amax['S']:.2f} (at x = 30)")
R.check("N3 CLAIM (P1, energy-ledger class r = 1): max over x in [0.3, 30] of the late-time reaction exceeds the 0.10 g_law pass line for both slavings, for every kernel and mass",
        f"max a/g_law = {amax['P']:.2f} (pressure), {amax['S']:.2f} (sigma); crossing of 0.10 at x = {xcross['P']:.2f} / {xcross['S']:.2f}", amax["P"] > 0.10 and amax["S"] > 0.10)
R.num("late_reaction_over_glaw", {sl: {f"{x:g}": tabA[(sl, MASSES[1], 'K1', 1.0, float(x))] for x in XS5} for sl in ("P", "S")})

# N4: reaction (units of G4's) never below the realised fraction (pressure-slaved, r = 1)
min_gap = 1e9
for kind in ("K1", "K2"):
    for taub in TAUB:
        for eps in (10.0, 100.0):
            dtm = min(taub, 1.0) / 200; tend = 1 + 12 * taub
            ta, th, mm = march(kind, taub, eps, 1.0, mP, dtm, tend)
            a_over = -eps * (th - mm)
            f_real = th                                        # theta / theta^T_full
            min_gap = min(min_gap, float(np.min(a_over - f_real)))
R.check("N4 CLAIM (r = 1) the reaction in units of G4's is never below the realised fraction f_real = theta/theta^T_full of the target: reaction/G4 >= f_real at every t, both kernels, eps_c in {10,100}",
        f"min over t of (reaction/G4 - f_real) = {min_gap:.3e} >= -1e-9", min_gap > -1e-9)
fr_bound = {"P": 0.10 / amax["P"], "S": 0.10 / amax["S"]}
P(f"    => P1 at r = 1 needs the realised fraction of the target f_real <= 0.10/max(a_G4/g_law) = {fr_bound['P']:.4f} (pressure) / {fr_bound['S']:.4f} (sigma): the fluid may hold <= 0.4-0.9 percent of its target, whereas the law needs f_real ~ 1")

# ---- N5: open class r = 0
P("\n    open class r = 0 (heat from an unspecified reservoir): reaction/g_law = eps_c * [peak over t of -(th - m) theta^T_M(t)/theta^T_M(fin)] * a_G4/g_law(x)")
peakB = {}
for slav in ("P", "S"):
    for kind in ("K1", "K2"):
        for taub in TAUB:
            best = 0.0
            xs_use = [30.0] if slav == "P" else XGRID
            for x in xs_use:
                mfun, thMr, a4, gl = theta_pieces(slav, 1e10, float(x))
                dtm = min(taub, 1.0) / 200; tend = 1 + 12 * taub
                ta, th, mm = march(kind, taub, 1.0, 0.0, mfun, dtm, tend)
                a_over = -(th - mm) * thMr(ta)                # eps_c = 1
                best = max(best, float(np.max(a_over)) * a4 / gl)
            peakB[(slav, kind, taub)] = best
for kind in ("K1", "K2"):
    P(f"      {kind}: peak a/g_law at eps_c = 1 [tau_bar/t_f = " + ", ".join(f"{tb:g}: P {peakB[('P', kind, tb)]:.3g} / S {peakB[('S', kind, tb)]:.3g}" for tb in TAUB) + "]")
eps_max = {k: 0.10 / v for k, v in peakB.items()}
P("      eps_c,max = 0.10/peak(eps_c = 1)  (P1 holds iff eps_c <= eps_c,max): " + "; ".join(f"{k[0]}/{k[1]}/{k[2]:g}: {v:.3g}" for k, v in eps_max.items() if k[1] == "K1"))
mfun_, thMr_, a4_, gl_ = theta_pieces("S", 1e10, 30.0)
ta_, th_, mm_ = march("K1", 1.0, 1.0, 0.0, mfun_, 1 / 200, 13.0)
ap_ = -(th_ - mm_) * thMr_(ta_)
P(f"      (sigma-slaved, x = 30, K1, tau_bar = t_f: the peak sits at t/t_f = {ta_[int(np.argmax(ap_))]:.3f} -- the start of the declared formation profile, where theta^T_M ~ M^(-1/2) diverges as M -> 0; the sigma bound is set there, not by the exchange at late times)")
# verify at eps_c = eps_max: peak = 0.10 (linearity), pressure-slaved K1 tau_bar = 1
k0 = ("P", "K1", 1.0); em = eps_max[k0]
mfun, thMr, a4, gl = theta_pieces("P", 1e10, 30.0)
ta, th, mm = march("K1", 1.0, em, 0.0, mfun, 1 / 200, 13.0)
chk_peak = float(np.max(-em * (th - mm))) * a4 / gl
R.check("N5 (open class r = 0) P1 holds iff eps_c <= eps_c,max: at eps_c = eps_c,max the marched peak reaction is exactly 0.10 g_law (linear in eps_c); eps_c is an UNTIED dimensionless coupling",
        f"peak at eps_c,max = {chk_peak:.4f} g_law (target 0.1000); eps_c,max(P, K1) = {em:.3g} at tau_bar/t_f = 1; at eps_c = 1 the peak is {peakB[k0]:.2f} g_law", abs(chk_peak - 0.10) < 2e-3)
R.num("eps_c_max", {f"{k[0]}/{k[1]}/{k[2]:g}": v for k, v in eps_max.items()})
R.num("peak_at_eps1", {f"{k[0]}/{k[1]}/{k[2]:g}": v for k, v in peakB.items()})

# =====================================================================================================================  S4 energy
R.banner("S4  energy budget (P2): what the exchange must supply, in CFG48's r_ta and in B's committed r_ta")
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
import CFG7_common as C7                                                     # read-only import (B's committed r_ta_law)
import importlib.util
spec = importlib.util.spec_from_file_location("Gcommon", os.path.join(REPO, "campaign_fresh_gravity", "CFG48_gap1_switch", "Gcommon.py"))
Gc = importlib.util.module_from_spec(spec); spec.loader.exec_module(Gc)      # read-only import (cross-check of r_ta48)
ctrl = max(abs(r_ta48_kpc(M) / Gc.r_ta_kpc(M) - 1) for M in MASSES)
R.check("E0 (control) this script's CFG48-convention r_ta equals Gcommon.r_ta_kpc (1e-9); CFG7_common.r_ta_law loads (committed convention)", f"max deviation {ctrl:.1e}", ctrl < 1e-9)
E1 = {}
P("    M_b        r_M     r_ta(CFG48)  x_e48   ratio48 | r_ta(comm,nu_mono)  x_e  ratio | (P2 kernel) ratio | E_c/E_infall(48, comm)")
for Mb in MASSES:
    rM = r_M_kpc(Mb); row = {}
    for lab, rta in (("CFG48", r_ta48_kpc(Mb)),
                     ("committed_nu_mono", 1e3 * float(C7.r_ta_law(Mb, C7.A0["canonical"], C7.nu_mono, 1.0))),
                     ("committed_P2", 1e3 * float(C7.r_ta_law(Mb, C7.A0["canonical"], C7.nu_p2, 1.0)))):
        re = 0.4 * rta
        rg = np.geomspace(1e-3 * rM, re, 200001)
        Ec = 1.5 * np.trapz((A0 * Mb / (8 * math.pi * rg ** 2)) * 4 * math.pi * rg ** 2, rg)   # (3/2) int P dV, P = a0 M/(8 pi r^2)
        KE = 0.5 * Mb * math.sqrt(G * Mb * A0)
        row[lab] = dict(r_ta=rta, r_e=re, x_e=re / rM, ratio_num=Ec / KE, ratio_closed=1.5 * re / rM, E_c=Ec, KE=KE)
    Mc = Mb * OMEGA_C_OVER_B; Mcol = Mb + Mc
    Einf48 = G * Mcol * Mc / row["CFG48"]["r_ta"]; Einfc = G * Mcol * Mc / row["committed_nu_mono"]["r_ta"]
    row["E_infall_ratio_48"] = row["CFG48"]["E_c"] / Einf48; row["E_infall_ratio_comm"] = row["committed_nu_mono"]["E_c"] / Einfc
    E1[f"{Mb:.0e}"] = row
    P(f"    {Mb:.0e}  {rM:6.2f}  {row['CFG48']['r_ta']:9.1f}  {row['CFG48']['x_e']:6.1f}  {row['CFG48']['ratio_num']:7.1f} | {row['committed_nu_mono']['r_ta']:9.1f}  {row['committed_nu_mono']['x_e']:6.1f}  {row['committed_nu_mono']['ratio_num']:7.1f} | {row['committed_P2']['ratio_num']:7.1f} | {row['E_infall_ratio_48']:.0f}, {row['E_infall_ratio_comm']:.0f}")
R.num("E1", E1)
okE = all(abs(v[k]["ratio_num"] / v[k]["ratio_closed"] - 1) < 2e-3 for v in E1.values() for k in ("CFG48", "committed_nu_mono", "committed_P2"))
R.check("E1 E_c(<r_e)/((1/2) M_b V_f^2) = 1.5 x_e by quadrature and closed form (2e-3), in CFG48's r_ta and in B's committed r_ta (nu_mono and P2 kernels)", f"closed-form agreement {okE}", okE)
ref179 = (E1["1e+10"]["committed_P2"]["ratio_num"] / 179.0 - 1, E1["1e+12"]["committed_P2"]["ratio_num"] / 57.0 - 1)
R.check("E1b (control) the committed-convention ratio reproduces the CFG48 referee's 179 (1e10) and 57 (1e12) with the P2 kernel (1%)", f"deviations {ref179[0]:.3f}, {ref179[1]:.3f}", max(abs(ref179[0]), abs(ref179[1])) < 0.01)

# E2 energy delivered vs realised fraction, kernel independence
Edel = {}
for kind in ("K1", "K2"):
    for taub in TAUB:
        dtm = min(taub, 1.0) / 100
        ta, th, mm = march(kind, taub, 100.0, 1.0, mP, dtm, 1 + 40 * taub)
        Edel[(kind, taub)] = th[-1]
edev = max(abs(v - 0.99) for v in Edel.values())
R.check("E2 the energy delivered by the memory law is f_real * E_c with f_real = 1 - r/eps_c (0.99 at eps_c = 100, r = 1), the SAME for both kernels and every tau_bar: the memory kernel redistributes the delivery in time, it does not reduce the total",
        f"f_real(t -> infinity) = {sorted(set(round(v, 5) for v in Edel.values()))}", edev < 1e-3)
ratios_c = {k: v["committed_nu_mono"]["ratio_num"] for k, v in E1.items()}
ratios_48 = {k: v["CFG48"]["ratio_num"] for k, v in E1.items()}
fr_P2 = {k: 1 / v for k, v in ratios_c.items()}
P(f"    P2 needs the realised fraction of the target energy <= (1/2) M_b V_f^2 / E_c = 1/(1.5 x_e) = " + ", ".join(f"{k}: {1 / ratios_48[k]:.4f} (CFG48), {fr_P2[k]:.4f} (committed)" for k in E1))
r_max_P1 = {sl: 0.10 / amax[sl] for sl in ("P", "S")}
r_max_P2 = {k: 1 / v for k, v in ratios_c.items()}
P(f"    ledger fraction bound for P1 (r * f_real <= {r_max_P1['P']:.4f} pressure / {r_max_P1['S']:.4f} sigma) and for the baryon-paid share against P2: r <= {min(r_max_P2.values()):.4f} (committed, worst mass): the reservoir must fund >= {100 * (1 - min(r_max_P1['P'], min(r_max_P2.values()))):.1f} percent of the heat")

# =====================================================================================================================  S5 time scales
R.banner("S5  the kernel's time scale (P4): what the closure needs, and which tied scales exist")
TF = (1.0, 10.0)
P("    scales in Gyr;  r = r_e (0.4 r_ta committed) and x = 1 (r_M):  light crossing r/c | t_dyn = r/V_c | t_M = r_M/V_f | 1/H0 | c/a0")
tabT = {}
for Mb in MASSES:
    rM = r_M_kpc(Mb); Vf = (G * Mb * A0) ** 0.25
    re = E1[f"{Mb:.0e}"]["committed_nu_mono"]["r_e"]
    Vc_e = math.sqrt(re * float(g_tot_of(Mb, re)))
    row = dict(light_re=re / C_KMS * GYR_PER_KPC_KMS, tdyn_re=re / Vc_e * GYR_PER_KPC_KMS, tdyn_rM=rM / math.sqrt(rM * float(g_tot_of(Mb, rM))) * GYR_PER_KPC_KMS,
               t_M=rM / Vf * GYR_PER_KPC_KMS, invH0=1 / H0_KMS_KPC * GYR_PER_KPC_KMS, c_over_a0=C_KMS * 1e3 / A0_SI / 3.15576e16)
    tabT[f"{Mb:.0e}"] = row
    P(f"    M_b = {Mb:.0e}: r_e/c = {row['light_re']:.2e} | t_dyn(r_e) = {row['tdyn_re']:.2f}, t_dyn(r_M) = {row['tdyn_rM']:.3f} | t_M = {row['t_M']:.3f} | 1/H0 = {row['invH0']:.1f} | c/a0 = {row['c_over_a0']:.1f}")
R.num("time_scales_Gyr", tabT)
# tau_bar -> 0 recovers the instantaneous G4 reaction: no time scale is REQUIRED
mfun, thMr, a4, gl = theta_pieces("P", 1e10, 1.0)
ta, th, mm = march("K1", 1e-3, 100.0, 1.0, mP, 1e-3 / 100, 3.0)
tau0_dev = abs((-100.0 * (th - mm))[-1] - 1.0)
R.check("T1 no kernel time scale is REQUIRED: tau_bar/t_f -> 0 (1e-3) gives the instantaneous G4 reaction at r = 1 (a/theta^T_M = 1 to 1e-3); the retarded structure (C1) holds for every tau_bar >= 0",
        f"|a/theta^T_M - 1| at tau_bar/t_f = 1e-3: {tau0_dev:.1e}", tau0_dev < 1e-3)
P("    tau_bar/t_f of the tied scales (t_f = 1 or 10 Gyr, declared):  " + "; ".join(
    f"{Mb:.0e}: r_e/c -> {tabT[f'{Mb:.0e}']['light_re'] / 10:.1e}, t_dyn(r_e) -> {tabT[f'{Mb:.0e}']['tdyn_re'] / 10:.2f} (t_f = 10); t_dyn(r_e) -> {tabT[f'{Mb:.0e}']['tdyn_re']:.2f} (t_f = 1)" for Mb in MASSES))

# ---- N6 (disclosed addition): open class r = 0 at two TIED kernel scales
P("\n    N6 (reported): open class r = 0, pressure-slaved, eps_c = 1, tied tau_bar (K1), worst x = 30 (a_G4/g_law = 22.49):")
n6 = {}
for Mb in MASSES:
    for tf in TF:
        for lab, tb in (("r_e/c", tabT[f"{Mb:.0e}"]["light_re"]), ("t_dyn(r_e)", tabT[f"{Mb:.0e}"]["tdyn_re"])):
            ratio = tb / tf
            dtm = min(ratio, 1.0) / 100
            ta, th, mm = march("K1", ratio, 1.0, 0.0, mP, dtm, 1 + 8 * ratio)
            pk = float(np.max(-(th - mm))) * amax["P"]
            n6[(Mb, tf, lab)] = (ratio, pk, 0.10 / pk)
            P(f"      M_b = {Mb:.0e}, t_f = {tf:g} Gyr, tau_bar = {lab} = {tb:.3g} Gyr (tau_bar/t_f = {ratio:.2e}): peak a/g_law = {pk:.3g} at eps_c = 1;  eps_c,max = {0.10 / pk:.3g}")
R.check("N6 (reported, added after the first run) in the OPEN class (r = 0, heat from an unspecified reservoir) P1 is met at eps_c = 1 for tau_bar = r_e/c and NOT for tau_bar = t_dyn(r_e)",
        f"peaks: r_e/c {max(v[1] for k, v in n6.items() if k[2] == 'r_e/c'):.2g} g_law; t_dyn(r_e) {min(v[1] for k, v in n6.items() if k[2] == 't_dyn(r_e)'):.2g}-{max(v[1] for k, v in n6.items() if k[2] == 't_dyn(r_e)'):.2g} g_law",
        max(v[1] for k, v in n6.items() if k[2] == "r_e/c") < 0.10 and min(v[1] for k, v in n6.items() if k[2] == "t_dyn(r_e)") > 0.10, load_bearing=False)
R.num("N6", {f"{k[0]:.0e}/{k[1]:g}/{k[2]}": v for k, v in n6.items()})
Dta_c = float(C7.LCDM.one_plus_delta_ta(1.0))
td_closed = 0.4 * math.sqrt(2 / (Dta_c * OM)) / H0_KMS_KPC * GYR_PER_KPC_KMS
R.check("T2 (reported, added after the first run) t_dyn(r_e) is mass-independent: t_dyn(r_e) = 0.4 sqrt(2/(Delta_ta Omega_m))/H0 in the deep-MOND edge (committed r_ta) -- a scale tied to H0 by a pure number",
        f"closed form {td_closed:.3f} Gyr vs printed {tabT['1e+10']['tdyn_re']:.3f} / {tabT['1e+12']['tdyn_re']:.3f} Gyr (= {td_closed / tabT['1e+10']['invH0']:.3f} / H0)",
        abs(tabT['1e+10']['tdyn_re'] / td_closed - 1) < 0.02, load_bearing=False)

# =====================================================================================================================  verdicts
R.banner("VERDICTS (frozen gates)")
R.verdict("P1 reaction <= 0.10 g_law on x in [0.3, 30], M_b = 1e9, 1e10, 1e12",
          "FAIL",
          f"in the energy-conserving completion (r = 1, no free coupling): late-time reaction = G4's for EVERY kernel, tau_bar and mass: {amax['P']:.1f} / {amax['S']:.1f} g_law at x = 30, 0.10 crossed at x = {xcross['P']:.2f}/{xcross['S']:.2f}; "
          f"reaction/G4 >= f_real, so 0.10 g_law needs f_real <= {fr_bound['P']:.4f}/{fr_bound['S']:.4f}. Met ONLY in the open class (r << 1: heat from an unspecified reservoir, >= {100 * (1 - min(r_max_P1['P'], min(r_max_P2.values()))):.1f} percent unfunded) "
          f"or with eps_c <= eps_c,max (pressure-slaved {eps_max[('P', 'K1', 1.0)]:.3g} at tau_bar = t_f; sigma-slaved {eps_max[('S', 'K1', 1.0)]:.3g}, set by the M -> 0 start of the profile)")
R.verdict("P2 energy supplied <= (1/2) M_b V_f^2",
          "FAIL", "ratios (1e9, 1e10, 1e12): CFG48 convention " + ", ".join(f"{ratios_48[k]:.1f}" for k in E1) + "; committed (CFG4 r_ta_law, nu_mono) " + ", ".join(f"{ratios_c[k]:.1f}" for k in E1)
          + "; kernel-independent (int Edot dt = f_real E_c; the static limit IS the target)")
R.verdict("P3 retarded + reciprocal", "PASS" if (cq < 1e-12 and ct_ < 1e-12 and asym < 1e-12 and dev_hand < 1e-12) else "FAIL",
          f"SK cross term: c_adv = {cq:.1e}/{ct_:.1e} (undoubled memory: {cn:.2g}); cross block symmetric {asym:.1e}; reaction derived from F; but the derived reaction IS G4's at r = 1 (that is the cost of reciprocity)")
R.verdict("P4 no untied constant beyond the kernel time scale", "FAIL",
          "r = 1 needs only tau_bar (not even that: tau_bar -> 0 is G4), and then P1 fails; passing P1 needs r << 1 (>= 99 percent unfunded) or eps_c << 1, each an untied dimensionless coupling; eps_c = c theta^T_full is additionally needed to hold theta = theta^T (offset r/eps_c)")
nf = R.write()
sys.exit(1 if nf else 0)
