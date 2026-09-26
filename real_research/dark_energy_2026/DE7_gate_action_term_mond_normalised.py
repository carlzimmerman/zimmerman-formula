#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE7 -- THE VACUUM GATE VARIED AS AN ACTION TERM, AT THE COUPLING THE MOND SECTOR SUPPLIES.

DE1-DE6 priced the vacuum gate as a PRESCRIBED switch.  In the C-H/K branch's one action (V0; the author's
2026-09-26 decision keeps that branch) the gate is a term of the action, so it must be varied.  Its variation
adds curvature-squared pieces to the gravitational operator.  The lead track's environment-gate report (uncommitted
at the time of writing: real_research/closure_doors_2026_09_26/environment_gate/) worked this out for a CONSTANT
declared coupling B = b M^2 Lambda in an isotropic, frozen-coefficient ADM principal sector.  It found a wrong-sign
k^4 term on part of the transition, repaired it with a concave curvature term C(R), and proved LOOSE sufficient
inequalities.  The cross-thread review (XR3 K6, committed 05627f376) put the MOND-normalised coupling at galaxy
gate edges at b ~ 3e-8 (z = 0.5) to 2.6e-4 (z = 4).  Its sufficient window then needed c2 above L340's range from
z ~ 3, and it said so: "the actual reduced operator at the MOND-normalised B has to be computed".  This lane
computes it, along the actual transition of actual galaxies, at every redshift where galaxies exist.

THE GATE ON THE KHRONON LEAVES (general exponent p, transition width w, regulator eps; c = 1)
  R = R^(3) + sigma_ij sigma^ij  (shear-completed: keeps c_T = 1, L351),   K = the leaf's mean curvature,
  s(R, K) = (9/4) 3^p Lambda^p R / (Omega_L0^p x_c0 D^((1+p)/2)),   D = K^4 + eps Lambda^2,
  t = (s - 1)/(2w) + 1/2,   f = W(t),   W(t) = g(t)/(g(t) + g(1 - t)),  g = e^(-1/t) (t > 0), 0 otherwise.
  s = u/x_c0 with u = x~ [Omega_L(K)/Omega_L0]^p the DE1/DE2 vacuum-gate variable (Omega_L(K) = 3 Lambda/K^2,
  x~ = 9R/(4K^2)).  p = 1, w = 1 is the lead track's gate with x_c = Omega_L0 x_c0.  f = 1/2 at u = x_c0 (DE1's
  edge); the transition spans x_c0(1 - w) < u < x_c0(1 + w).
  The action term: S_G = int N sqrt(gamma) B f(R, K), with B = dL/df the Lagrangian density the gate multiplies.
  Its constitutive part, in the region kernel's own chassis (CV1's q-form, QUMOND sign), is
  B = M^2 a0^2 q(y^2),  q(y^2) = 2 int_0^y h(s) ds,  h = y (nu_mono - 1),  y = g_N/a0,  M^2 = 1/(8 pi G),
  so b = B/(M^2 Lambda) = (a0/c^2)^2 q/Lambda (= q/(32 pi) at kappa = 1/2; x 1.45 on the alt footing).

WHAT THIS LANE CHECKS
  S1 [sympy] the general-p/w gate derivatives reduce to the lead track's p = 1 expressions exactly (control).
  S2 [sympy, INDEPENDENT] the quadratic ADM action is re-derived from scratch on a plane-wave scalar ansatz
     (gamma = e^(2 zeta) delta, lapse 1 + n, shift d_i beta, background expansion K0, the Ricci scalar from the
     Christoffel symbols).  Its principal part equals the lead track's declared density term by term, and the
     remainder is k-free.  Eliminating shift and lapse exactly, the reduced operator's k -> infinity kinetic and
     k^4 coefficients are 9F/2 and 4 E_* (x-averaged normalisation), with
     Z = M^2 + 2 G_R, C = -M^2 (2/3 + c2) + G_KK, D = G_RK, E = G_RR,  Delta = C + 2Z/3,
     F = (2Z/3) C/Delta,  E_* = E - D^2/Delta,  for the total leaf function G = B f + C(R).
  S3 [sympy] the gate's first variations (for the V0 writer), each checked against a direct Euler-Lagrange
     computation on an ansatz: lapse (Kantowski-Sachs), momentum (1-d shift on a conformal leaf), metric curvature
     part (static conformal leaf, lapse N(x)), metric kinetic part (Kantowski-Sachs, both scale factors).
  T1 [theorem, Lean DE7] any C^2 gate with an off-plateau (f = 0) and an on-plateau (f = 1) has f'' > 0 somewhere
     and f'' < 0 somewhere on its transition (mean value theorem twice).  With the gate's argument linear in R,
     E = B f'' t_R^2 there, and E_* >= E whenever Delta < 0 (the no-ghost branch).  So with no repair term, a
     gate multiplying any B != 0 has E_* > 0 -- a wrong-sign k^4 term, growth rate proportional to k^2, i.e.
     Hadamard ill-posed -- somewhere on every transition.  This holds for every smooth gate shape, not only W.
  C1 [control] the edge couplings b(z) reproduce XR3 K6 (p = 1, x_c0 = 2.5, 1e11 Msun, canonical) to 5%.
  C2 [control] the lead track's own midpoint witness (R/Lambda = 8/27, K/sqrt(Lambda) = 1, eps = x_c = 1,
     b = 1e-10, eta = 1e-6, c2 = 1/50): Z, Delta, E_*, F reproduce its recorded 35-digit values to 1e-9.
  U1 [load-bearing] along REAL galaxy transitions (point-mass baryons, nu_mono phantom, R from the upper-branch
     density contrast on CMC leaves K = 3H(z)), the UNREPAIRED gate has E_* > 0 on part of every transition
     computed: z = 0-12, M_b = 1e9-1e12, both footings, five window cells, w = 1, 0.5, 0.25.
  R1 [load-bearing, pre-declared hypothesis H1] with the lead track's Lambda-scaled concave repair
     C(R) = -eta M^2 [R arctan(R/Lambda) - (Lambda/2) ln(1 + R^2/Lambda^2)], the smallest eta that makes
     E_* < 0 (with Z > 0, Delta < 0) across the transition is BELOW the repair's own ceiling
     eta < 3 c2/(2 pi) (voids: R -> -infinity must keep Delta < 0) at c2 = 7.3e-3 (L340's floor), for every
     z <= 4 edge of 1e11 Msun canonical, p = 1, x_c0 = 2.5, w = 1.  (XR3's sufficient inequalities needed c2
     above 0.067 from z ~ 3 for the same edges.)
  R2 [reported] eta_min(z) for every case and the highest redshift z_wp to which the window stays open, per cell,
     mass, footing, w and c2 in {7.3e-3, 0.067}; the B < 0 and b x {0.3, 3} sensitivities.
  S4 [sympy] the static trace-free metric equation (S3's E^ij, first order) gives psi - phi = 2 dG_R/M^2: lensing sees
     (phi + psi)/2 and dynamics phi, so any spatial variation of G_R -- the gate's B f_R or a repair's C_R -- is slip.
  N2 [reported] the varied gate's own slip on the real transitions: max |g_lens - g_dyn|/g_dyn per z (1e11).
  N3 [reported] the Lambda-scaled repair's slip at KiDS-epoch lenses (z = 0.25, 1e10-1e12): C_R falls by
     eta arctan(R_1/2) across each transition, so a 10% lensing = dynamics limit caps eta (a rigorous bound via
     int g_dyn dr <= int nu g_N dr), and hence the redshift of the edges that repair can stabilise.
  N4 [reported] the floor for ANY metric-only repair: at one epoch every system's transition sits at the same R,
     so -C_RR >= max_systems B f_RR there; each lens then carries slip >= I_max/2, I_max = int B_max f_RR dR over the
     lower half, set by the most massive bound system (1e12 galaxies or 1e14 clusters).
  N1 [reported, indicative, NOT gates] the repair's structural cost.  Any R-only concave repair has
     C_R(+inf) - C_R(-inf) = int C_RR dR < 0, so the coefficient of R^(3) + sigma^2 differs between over- and
     under-dense leaves; the arctan form saturates at |delta rho| ~ rho_L, so this is a sign-dependent Newton
     coupling of relative size pi eta wherever |delta rho| >> rho_L (all structure, and the CMB epoch), and a
     local G = G/(1 - pi eta) inside bound regions against G_cos = G.  L350's Planck reading of G_cos/G_N
     (|G_cos/G_N - 1| <= 1.5 x (0.63-2.9)e-3) would read pi eta <= that: eta <~ 3e-4 to 1.4e-3.  This is an
     analogy for scale only; the operator's own cosmology is not computed.
  M1 [the doors, for CV1's A6 obligation] contrast door (R^(3) + sigma^2): FRW is off-plateau for every w <= 1.
     absolute door (R^(3) + sigma^2 + (2/3) K^2 - 2 Lambda = 16 pi G rho + 2 sigma^2 in GR's constraint): FRW is
     off-plateau iff x_c0 (1 - w) >= max_z (3/2) Omega_m(z) [Omega_L(z)/Omega_L0]^p (reported per cell), and its
     repaired eta_min is reported.  matter-only door: no metric-only form (on the lensing = dynamics sector R^(3)
     reads rho_dyn, phantom included); it is DE4's lower static branch of the same geometric term.

  MUTATE=1 prescribes the gate (drops its second variation: f_RR = f_RK = f_KK = 0, the lead track's "prescribed
  mask" control).  U1 must then FAIL (E_* = 0, no wrong-sign k^4 term).  rc = 1.

SCOPE.  The isotropic frozen-coefficient principal sector the lead track declared: wavelengths short against the
transition width and the horizon.  B is frozen at its local constitutive value.  Only its size enters the k^4
coefficient: the MOND field's own perturbation is slaved by an elliptic constraint in CV1's chassis, so it
enters at lower order in k (argued here, not computed).  The auxiliary parts of dL/df (CV1's Psi and w terms) are
the V0 writer's; the b x {0.3, 3} scan brackets them.  K0 = 3H(z) at the galaxy, as DE1/L352 took: CMC-like leaves
under the leaf-averaged c2 term.  Point-mass baryons.  eps = 1 (the lead track's declared test value).  Criterion B
(the author's 09-26 decision) allows the positive k^4 dispersion's unbounded group speed along leaves (Horava-type
Lifshitz scaling), so the lead track's section-4 all-frequency cone objection is not applied here.  Stability
(Z > 0, F > 0, E_* < 0) is required.  Not a full well-posedness proof and not a cosmology of the repaired action.

Run from the repository root:  python3 real_research/dark_energy_2026/DE7_gate_action_term_mond_normalised.py
"""
import os, sys, json, math, time, io, contextlib, random
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE7_gate_action_term_mond_normalised"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE7", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the gate is PRESCRIBED (f_RR = f_RK = f_KK = 0); U1 must FAIL ***")

# ------------------------------------------------------------------ L352's constants and kernel, loaded unedited
P52 = os.path.join(REPO, "real_research", "g03_audit_2026", "L352_switch_gauss_compensation.py")
L52 = {"__name__": "l352", "__file__": P52}
_s52 = open(P52).read().split('banner("Z1')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_s52, L52)
c_, G_, MS = L52["c"], L52["G"], 1.98892e30
H0, Om, OL, Or, rho_crit0, A0 = L52["H0"], L52["Om"], L52["OL"], L52["Or"], L52["rho_crit0"], L52["A0"]
LYG, YG, HM, DH = L52["LYG"], L52["YG"], L52["HM"], L52["DH"]
KPC = L52["Mpc"] / 1e3
E2 = lambda z: Om * (1 + z) ** 3 + OL + Or * (1 + z) ** 4
LAMc2 = 3 * OL * H0 ** 2                                     # Lambda c^2 [s^-2]
RHO_L = OL * rho_crit0
# q(y^2) = 2 int_0^y h(s) ds on L352's own grid (below 1e-14 the deep-MOND tail (2/3) y^1.5 is negligible)
QG = 2.0 * ((2.0 / 3.0) * YG[0] ** 1.5 + np.concatenate([[0.0], np.cumsum(0.5 * (HM[1:] + HM[:-1]) * np.diff(YG))]))
h_of = lambda y: np.interp(np.log10(y), LYG, HM)
dh_of = lambda y: np.interp(np.log10(y), LYG, DH)
q_of = lambda y: np.interp(np.log10(y), LYG, QG)
AH = {f: (a0 / c_ ** 2) ** 2 / (LAMc2 / c_ ** 2) for f, a0 in A0.items()}     # (a0/c^2)^2/Lambda
P(f"\n  L352 loaded: H0 = {H0:.5e} s^-1, Om = {Om:.5f}, OL = {OL:.5f}; kernel nu_mono (h on a 1e-14..1e14 grid)")
P(f"  (a0/c^2)^2/Lambda: canonical {AH['canonical']:.5e} (1/(32 pi) = {1 / (32 * math.pi):.5e}), alt {AH['alt']:.5e}")

# ============================================================================================ S1 the gate
banner("S1  THE GATE ON THE LEAVES: general p, w, eps -- derivatives, and the lead track's p = 1 control")
Rs, Ks = sp.symbols("R K", real=True)
Ls, es, xc0s, OL0s, ps, ws = sp.symbols("Lambda epsilon x_c0 Omega_L0 p w", positive=True)
Ds = Ks ** 4 + es * Ls ** 2
s_expr = sp.Rational(9, 4) * 3 ** ps * Ls ** ps * Rs / (OL0s ** ps * xc0s * Ds ** ((1 + ps) / 2))
t_expr = (s_expr - 1) / (2 * ws) + sp.Rational(1, 2)
tR, tK = sp.diff(t_expr, Rs), sp.diff(t_expr, Ks)
tRR, tKK, tRK = sp.diff(t_expr, Rs, 2), sp.diff(t_expr, Ks, 2), sp.diff(t_expr, Rs, Ks)
# lead track's p = 1, w = 1 argument (check_gate_adm.py): t = a R/(2 x_c d), a = 27 Lambda/4, x_c = Omega_L0 x_c0
xc_s = OL0s * xc0s
t_lead = sp.Rational(27, 4) * Ls * Rs / (2 * xc_s * Ds)
sub1 = {ps: 1, ws: 1}
res = [sp.simplify(e.subs(sub1) - l) for e, l in [
    (t_expr, t_lead), (tK, -4 * t_lead * Ks ** 3 / Ds), (tKK, 4 * t_lead * Ks ** 2 * (5 * Ks ** 4 - 3 * es * Ls ** 2) / Ds ** 2),
    (tRK, -4 * Ks ** 3 * sp.diff(t_lead, Rs) / Ds), (tRR, 0)]]
P(f"    residuals vs the lead track's t, t_K, t_KK, t_RK, t_RR at p = w = 1: {res}")
check("S1 the general-p/w gate argument and its derivatives reduce to the lead track's p = 1 expressions exactly",
      res, all(r == 0 for r in res),
      "t is linear in R (t_RR = 0) for every p and w; the half-activation point is u = x_c0 (DE1's edge)")
# general closed forms used numerically (hat units: R/Lambda, K/sqrt(Lambda))
_hat = {Ls: 1}
t_f = sp.lambdify((Rs, Ks, es, xc0s, OL0s, ps, ws), t_expr.subs(_hat), "numpy")
tR_f = sp.lambdify((Rs, Ks, es, xc0s, OL0s, ps, ws), tR.subs(_hat), "numpy")
tK_f = sp.lambdify((Rs, Ks, es, xc0s, OL0s, ps, ws), tK.subs(_hat), "numpy")
tKK_f = sp.lambdify((Rs, Ks, es, xc0s, OL0s, ps, ws), tKK.subs(_hat), "numpy")
tRK_f = sp.lambdify((Rs, Ks, es, xc0s, OL0s, ps, ws), tRK.subs(_hat), "numpy")


def Wd(t):
    """W, W', W'' of the lead track's smooth step (exact zero outside (0, 1))."""
    t = np.asarray(t, float)
    inside = (t > 0) & (t < 1)
    tt = np.where(inside, t, 0.5)
    ell = 1 / tt - 1 / (1 - tt)
    W = np.where(ell > 0, np.exp(-np.clip(ell, 0, 700)) / (1 + np.exp(-np.clip(ell, 0, 700))), 1 / (1 + np.exp(np.clip(ell, -700, 0))))
    gq = 1 / tt ** 2 + 1 / (1 - tt) ** 2
    gp = -2 / tt ** 3 + 2 / (1 - tt) ** 3
    W1 = W * (1 - W) * gq
    W2 = W * (1 - W) * ((1 - 2 * W) * gq ** 2 + gp)
    W = np.where(t >= 1, 1.0, np.where(t <= 0, 0.0, W))
    return W, np.where(inside, W1, 0.0), np.where(inside, W2, 0.0)


ts_ = sp.Symbol("t", positive=True)
W_sym = 1 / (1 + sp.exp(1 / ts_ - 1 / (1 - ts_)))
_chk = [(float(sp.diff(W_sym, ts_, n).subs(ts_, sp.Rational(3, 10)).evalf(30)), float(Wd(0.3)[n])) for n in range(3)]
P(f"    W, W', W'' at t = 0.3 (sympy vs closed form): {[(round(a, 12), round(b, 12)) for a, b in _chk]}")
assert all(abs(a - b) < 1e-9 * max(1, abs(a)) for a, b in _chk)

# ============================================================================= S2 the independent quadratic action
banner("S2  INDEPENDENT RE-DERIVATION: the quadratic ADM action on a plane-wave scalar ansatz, then the reduction")
x_ = sp.Symbol("x", real=True); eb = sp.Symbol("e_b"); k_ = sp.Symbol("k", positive=True)
A_, Ad_, Nn_, Bb_ = sp.symbols("A A_dot n_1 beta_1", real=True)
K0_, M2_, c2_, al_, Lm_ = sp.symbols("K0 M2 c2 alpha Lambda_", real=True)
G0_, GR_, GK_, GRR_, GRK_, GKK_ = sp.symbols("G0 G_R G_K G_RR G_RK G_KK", real=True)
CS = sp.cos(k_ * x_)
zeta = eb * A_ * CS; zeta_t = eb * Ad_ * CS
Nl = 1 + eb * Nn_ * CS
Nlow = [sp.diff(eb * Bb_ * CS, x_), sp.S.Zero, sp.S.Zero]
gam = sp.diag(*[sp.exp(2 * zeta)] * 3); ginv = gam.inv()
gdot = 2 * (K0_ / 3 + zeta_t) * gam                          # background expansion K0 = 3 H frozen at a = 1
dd = lambda e, i: sp.diff(e, x_) if i == 0 else sp.S.Zero
Gam = [[[sp.simplify(sum(ginv[a, l] * (dd(gam[l, j], i) + dd(gam[l, i], j) - dd(gam[i, j], l)) for l in range(3)) / 2)
         for j in range(3)] for i in range(3)] for a in range(3)]
Ric = sp.zeros(3)
for i in range(3):
    for j in range(3):
        Ric[i, j] = sum(dd(Gam[a][i][j], a) - dd(Gam[a][i][a], j)
                        + sum(Gam[a][a][l] * Gam[l][i][j] - Gam[a][j][l] * Gam[l][i][a] for l in range(3)) for a in range(3))
R3 = sp.simplify(sum(ginv[i, j] * Ric[i, j] for i in range(3) for j in range(3)))
DN = sp.Matrix(3, 3, lambda i, j: dd(Nlow[j], i) - sum(Gam[a][i][j] * Nlow[a] for a in range(3)))
Kij = (gdot - DN - DN.T) / (2 * Nl)
Kup = ginv * Kij * ginv
Ktr = sum(ginv[i, j] * Kij[i, j] for i in range(3) for j in range(3))
sig2 = sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3)) - Ktr ** 2 / 3
acc2 = sum(ginv[i, j] * dd(sp.log(Nl), i) * dd(sp.log(Nl), j) for i in range(3) for j in range(3))
Rt = R3 + sig2; dK = Ktr - K0_
Gx = G0_ + GR_ * Rt + GK_ * dK + GRR_ * Rt ** 2 / 2 + GRK_ * Rt * dK + GKK_ * dK ** 2 / 2
Lag = Nl * sp.exp(3 * zeta) * (M2_ / 2 * (R3 + sig2 - (sp.Rational(2, 3) + c2_) * Ktr ** 2 + al_ * acc2 - 2 * Lm_) + Gx)
L2 = sp.expand(sp.series(Lag, eb, 0, 3).removeO().coeff(eb, 2))
L2 = sp.expand(sp.integrate(L2, (x_, 0, 2 * sp.pi / k_)) * k_ / (2 * sp.pi))       # x-average of the plane wave
P(f"    R^(3) on the ansatz (from the Christoffel symbols): {R3}   [{time.time() - T0:.0f}s]")
# the lead track's declared principal density, x-averaged (factor 1/2), s = lap(beta) = -k^2 beta_1, r = 4 k^2 zeta
Zs = M2_ + 2 * GR_; Cs = -M2_ * (sp.Rational(2, 3) + c2_) + GKK_; Dsy = GRK_; Es = GRR_
s_sh = -k_ ** 2 * Bb_; kap = 3 * Ad_ - s_sh - K0_ * Nn_; rr_ = 4 * k_ ** 2 * A_
lead = sp.Rational(1, 2) * (Zs / 3 * s_sh ** 2 + Cs / 2 * kap ** 2 + Dsy * rr_ * kap + Es / 2 * rr_ ** 2 + Zs * k_ ** 2 * A_ ** 2
                            + 2 * Zs * k_ ** 2 * Nn_ * A_ + al_ * M2_ / 2 * k_ ** 2 * Nn_ ** 2)
rem = sp.expand(L2 - lead)
P(f"    remainder (independent - lead track's principal density): {sp.collect(rem, [A_, Nn_, Ad_])}")
s2a = (rem.free_symbols.isdisjoint({k_, Bb_})) and sp.Poly(rem, A_, Ad_, Nn_).total_degree() == 2
# exact elimination of shift and lapse, then the k -> infinity principal coefficients
solv = sp.solve([sp.diff(L2, Bb_), sp.diff(L2, Nn_)], [Bb_, Nn_], dict=True)[0]
Lred = sp.expand(sp.simplify(L2.subs(solv)))
Akin = sp.simplify(sp.diff(Lred, Ad_, 2))
Vpot = sp.simplify(Lred.subs(Ad_, 0) / A_ ** 2)
Delta_s = Cs + 2 * Zs / 3; F_s = (2 * Zs / 3) * Cs / Delta_s; Estar_s = Es - Dsy ** 2 / Delta_s
uu = sp.Symbol("u", positive=True)
lim_kin = sp.simplify(sp.limit(Akin.subs(k_, 1 / uu), uu, 0) - sp.Rational(9, 2) * F_s)
lim_k4 = sp.simplify(sp.limit((Vpot / k_ ** 4).subs(k_, 1 / uu), uu, 0) - 4 * Estar_s)
P(f"    reduced kinetic (k -> inf) - 9F/2 = {lim_kin};  reduced V/k^4 (k -> inf) - 4 E_* = {lim_k4}   [{time.time() - T0:.0f}s]")
check("S2 INDEPENDENT: the quadratic ADM action re-derived on a plane-wave ansatz equals the lead track's principal density "
      "(k-free, shift-free remainder), and the exact shift/lapse reduction has k->inf kinetic 9F/2 and k^4 coefficient 4 E_*",
      f"remainder k-free: {s2a}; kinetic residual {lim_kin}; k^4 residual {lim_k4}",
      s2a and lim_kin == 0 and lim_k4 == 0,
      "the remainder holds only background-measure pieces (G0, G_K, Lambda, K0^2) -- lower order in k")
OUT["numbers"]["S2_remainder"] = str(sp.collect(rem, [A_, Nn_, Ad_]))

# ======================================================================== S3 the first variations, for the V0 writer
banner("S3  THE GATE'S FIRST VARIATIONS (for V0): lapse, momentum, metric -- each against a direct Euler-Lagrange run")
tt_ = sp.Symbol("t", real=True)
cg = sp.symbols("g1:7", real=True)
def Gtest(R, K):        # a generic non-polynomial leaf function G(R, K): the identities are linear in G and its derivatives
    return sp.exp(cg[0] * R + cg[1] * K) * (1 + cg[2] * R * K) + cg[3] * R ** 3 + cg[4] * K ** 4 / (1 + cg[5] * R ** 2)
r1, k1 = sp.symbols("r1 k1", real=True)
Gg = Gtest(r1, k1); GgR, GgK, GgRR = sp.diff(Gg, r1), sp.diff(Gg, k1), sp.diff(Gg, r1, 2)
at = lambda e, R, K: e.subs({r1: R, k1: K}, simultaneous=True)
rng = random.Random(20260926)
def numzero(expr, subs, n=4, scale=None):
    """largest |expr| over n random rational coupling draws (40 digits), relative to |scale| when given."""
    worst = 0.0
    for _ in range(n):
        vals = {s: sp.Rational(rng.randint(1, 9), rng.randint(5, 13)) * (1 if rng.random() < 0.7 else -1) for s in subs}
        v = abs(complex(sp.N(expr.subs(vals), 40)))
        if scale is not None:
            v = v / max(abs(complex(sp.N(scale.subs(vals), 40))), 1e-300)
        worst = max(worst, v)
    return worst
# (a) lapse and (d) metric kinetic part: Kantowski-Sachs, gamma = diag(a^2, b^2, b^2 sin^2)
Af, Bf, Nf = [sp.Function(n)(tt_) for n in ("a", "b", "N")]
Ha, Hb = sp.diff(Af, tt_) / Af, sp.diff(Bf, tt_) / Bf
R3ks = 2 / Bf ** 2
Kks = (Ha + 2 * Hb) / Nf
s2ks = sp.Rational(2, 3) * (Ha - Hb) ** 2 / Nf ** 2
Lks = Nf * Af * Bf ** 2 * at(Gg, R3ks + s2ks, Kks)
lapse_direct = sp.diff(Lks, Nf)
lapse_formula = Af * Bf ** 2 * (at(Gg, R3ks + s2ks, Kks) - 2 * s2ks * at(GgR, R3ks + s2ks, Kks) - Kks * at(GgK, R3ks + s2ks, Kks))
# metric: E^ij = sqrt(g)[N g^ij G/2 + N G_R(-R^ij - 2 K^i_k K^kj + (2/3) K K^ij) - N G_K K^ij + D^iD^j(N G_R) - g^ij D^2(N G_R)]
#              - d_t(sqrt(g) P^ij/2),   P^ij = 2 G_R sigma^ij + G_K g^ij   (no shift; homogeneous here so the D terms vanish)
Kmix = sp.diag(Ha / Nf, Hb / Nf, Hb / Nf)                     # K^i_j
gdn = sp.diag(Af ** 2, Bf ** 2, Bf ** 2)                     # sin^2 dropped (overall factor)
gup = gdn.inv(); Kup_ks = Kmix * gup
Rup = sp.diag(0, 1 / Bf ** 4, 1 / Bf ** 4)                   # R^ij of line x 2-sphere of radius b
sgup = Kup_ks - Kks * gup / 3
GRv, GKv, Gv = at(GgR, R3ks + s2ks, Kks), at(GgK, R3ks + s2ks, Kks), at(Gg, R3ks + s2ks, Kks)
sqg = Af * Bf ** 2
Eup = sqg * (Nf * gup * Gv / 2 + Nf * GRv * (-Rup - 2 * Kmix * Kup_ks + sp.Rational(2, 3) * Kks * Kup_ks) - Nf * GKv * Kup_ks) \
      - sp.diff(sqg * (2 * GRv * sgup + GKv * gup) / 2, tt_)
EL = lambda L, f: sp.diff(L, f) - sp.diff(sp.diff(L, sp.diff(f, tt_)), tt_)
met_a = EL(Lks, Af) - 2 * Af * Eup[0, 0]
met_b = EL(Lks, Bf) - 4 * Bf * Eup[1, 1]
tf = {Af: sp.exp(sp.Rational(3, 10) * tt_) * (1 + tt_ ** 2 / 5), Bf: 2 + sp.sin(tt_) / 3, Nf: 1 + tt_ / 7}
def on_ks(e, sc):
    e, sc = e.subs(tf).doit(), sc.subs(tf).doit()
    return numzero(e.subs(tt_, sp.Rational(7, 10)), list(cg), scale=sc.subs(tt_, sp.Rational(7, 10)))
res_lapse = numzero((lapse_direct - lapse_formula).subs(tf).doit().subs(tt_, sp.Rational(1, 3)), list(cg),
                    scale=lapse_direct.subs(tf).doit().subs(tt_, sp.Rational(1, 3)))
res_ma, res_mb = on_ks(met_a, EL(Lks, Af)), on_ks(met_b, EL(Lks, Bf))
P(f"    relative residuals -- lapse: |dL/dN - sqrt(g)[G - 2 sigma^2 G_R - K G_K]|/|dL/dN| = {res_lapse:.1e};  metric (a, b): {res_ma:.1e}, {res_mb:.1e}   "
  f"[{time.time() - T0:.0f}s]")
# (b) momentum: static conformal leaf gamma = e^(2 zeta(x)) delta, lapse N(x), shift N_x = v(t, x) (lower index)
zf, Nx, vf = sp.Function("zeta")(x_), sp.Function("Nl")(x_), sp.Function("v")(tt_, x_)
gamc = sp.diag(*[sp.exp(2 * zf)] * 3); gic = gamc.inv()
Gc = [[[sp.simplify(sum(gic[a, l] * (dd(gamc[l, j], i) + dd(gamc[l, i], j) - dd(gamc[i, j], l)) for l in range(3)) / 2)
        for j in range(3)] for i in range(3)] for a in range(3)]
Ricc = sp.zeros(3)
for i in range(3):
    for j in range(3):
        Ricc[i, j] = sum(dd(Gc[a][i][j], a) - dd(Gc[a][i][a], j)
                         + sum(Gc[a][a][l] * Gc[l][i][j] - Gc[a][j][l] * Gc[l][i][a] for l in range(3)) for a in range(3))
R3c = sp.simplify(sum(gic[i, j] * Ricc[i, j] for i in range(3) for j in range(3)))
Nlc = [vf, sp.S.Zero, sp.S.Zero]
DNc = sp.Matrix(3, 3, lambda i, j: dd(Nlc[j], i) - sum(Gc[a][i][j] * Nlc[a] for a in range(3)))
Kc = -(DNc + DNc.T) / (2 * Nx)
Kcu = gic * Kc * gic
Kct = sum(gic[i, j] * Kc[i, j] for i in range(3) for j in range(3))
s2c = sp.expand(sum(Kc[i, j] * Kcu[i, j] for i in range(3) for j in range(3)) - Kct ** 2 / 3)
sqc = sp.exp(3 * zf)
Lc = Nx * sqc * at(Gg, R3c + s2c, Kct)
vx = sp.diff(vf, x_)
mom_direct = sp.diff(Lc, vf) - sp.diff(sp.diff(Lc, vx), x_)
Pup = 2 * at(GgR, R3c + s2c, Kct) * (Kcu - Kct * gic / 3) + at(GgK, R3c + s2c, Kct) * gic
divP = sum(dd(Pup[i, 0], i) for i in range(3)) + sum(Gc[i][i][a] * Pup[a, 0] for i in range(3) for a in range(3)) \
       + sum(Gc[0][i][a] * Pup[i, a] for i in range(3) for a in range(3))
mom_formula = sqc * divP
tfx = {zf: sp.sin(x_) / 4 + x_ / 9, Nx: 1 + sp.cos(2 * x_) / 5, vf: sp.sin(x_ + tt_ / 3) / 3 + x_ ** 2 / 11}
_pt = {x_: sp.Rational(3, 7), tt_: sp.Rational(1, 5)}
res_mom = numzero((mom_direct - mom_formula).subs(tfx).doit().subs(_pt), list(cg), scale=mom_direct.subs(tfx).doit().subs(_pt))
# (c) metric curvature part: static conformal leaf, no shift: E_zeta = 2 sqrt(g)[(3/2) N G - N G_R R3 - 2 D^2(N G_R)]
Lcs = Nx * sqc * at(Gg, R3c, 0)
zp, zpp = sp.diff(zf, x_), sp.diff(zf, x_, 2)
ELz = sp.diff(Lcs, zf) - sp.diff(sp.diff(Lcs, zp), x_) + sp.diff(sp.diff(Lcs, zpp), x_, 2)
phi = Nx * at(GgR, R3c, 0)
lap_phi = sum(gic[i, j] * (dd(dd(phi, j), i) - sum(Gc[a][i][j] * dd(phi, a) for a in range(3))) for i in range(3) for j in range(3))
curv_formula = 2 * sqc * (sp.Rational(3, 2) * Nx * at(Gg, R3c, 0) - Nx * at(GgR, R3c, 0) * R3c - 2 * lap_phi)
res_curv = numzero((ELz - curv_formula).subs(tfx).doit().subs(x_, sp.Rational(2, 5)), list(cg),
                   scale=ELz.subs(tfx).doit().subs(x_, sp.Rational(2, 5)))
P(f"    momentum: |EL_v - sqrt(g) D_i P^ix| = {res_mom:.1e};  curvature part: |EL_zeta - formula| = {res_curv:.1e}   "
  f"[{time.time() - T0:.0f}s]")
worst_var = max(res_lapse, res_ma, res_mb, res_mom, res_curv)
check("S3 the gate's first variations (lapse, momentum, metric curvature part, metric kinetic part) equal direct "
      "Euler-Lagrange computations on their ansatze (generic non-polynomial G, random rational couplings, 40 digits, "
      "residual relative to the Euler-Lagrange expression)",
      f"worst relative residual {worst_var:.1e}", worst_var < 1e-25,
      "lapse: sqrt(g)[G - 2 sigma^2 G_R - K G_K]; momentum: sqrt(g) D_i(2 G_R sigma^ij + G_K g^ij); metric: see docstring")

# ============================================================================ S4 the slip: lensing vs dynamics
banner("S4  LENSING vs DYNAMICS: the static trace-free metric equation fixes psi - phi = 2 dG_R/M^2")
es_ = sp.Symbol("e_s")
ph_s, ze_s, ch_s = [sp.Function(n)(x_) for n in ("phi_s", "zeta_s", "chi_s")]
gss = sp.diag(*[sp.exp(2 * es_ * ze_s)] * 3); gis_ = gss.inv()
Gss = [[[sp.simplify(sum(gis_[a, l] * (dd(gss[l, j], i) + dd(gss[l, i], j) - dd(gss[i, j], l)) for l in range(3)) / 2)
         for j in range(3)] for i in range(3)] for a in range(3)]
Rs_ = sp.zeros(3)
for i in range(3):
    for j in range(3):
        Rs_[i, j] = sum(dd(Gss[a][i][j], a) - dd(Gss[a][i][a], j)
                        + sum(Gss[a][a][l] * Gss[l][i][j] - Gss[a][j][l] * Gss[l][i][a] for l in range(3)) for a in range(3))
NLR = (1 + es_ * ph_s) * (M2_ / 2 + es_ * ch_s)               # N L_R, L_R = M^2/2 + G_R, G_R = e chi(x) a given field
DDn = sp.Matrix(3, 3, lambda i, j: dd(dd(NLR, j), i) - sum(Gss[a][i][j] * dd(NLR, a) for a in range(3)))
Xup = -(1 + es_ * ph_s) * (M2_ / 2 + es_ * ch_s) * (gis_ * Rs_ * gis_) + gis_ * DDn * gis_
trX = sum(gss[i, j] * Xup[i, j] for i in range(3) for j in range(3))
XTF = Xup - gis_ * trX / 3
lin_tf = sp.simplify(sp.series(XTF[0, 0], es_, 0, 2).removeO().coeff(es_, 1))
expect = sp.Rational(2, 3) * sp.diff(M2_ / 2 * (ph_s + ze_s) + ch_s, x_, 2)
slip_res = sp.simplify(lin_tf - expect)
P(f"    trace-free xx part at first order: {lin_tf}")
P(f"    minus (2/3) d^2/dx^2 [ (M^2/2)(phi - psi) + G_R ]  (psi = -zeta):  {slip_res}")
check("S4 the static trace-free metric equation (the S3-verified E^ij) gives (M^2/2)(phi - psi) + dG_R = harmonic, i.e. "
      "psi - phi = 2 dG_R/M^2: lensing sees (phi + psi)/2, dynamics phi, so they differ by dG_R/M^2 (exact at first order)",
      f"residual {slip_res}", slip_res == 0,
      "any spatial variation of the total leaf function's G_R -- the gate's B f_R or a repair's C_R -- is gravitational slip")

# ============================================================================================ T1 the theorem
banner("T1  ANY smooth plateau gate has a wrong-sign k^4 term somewhere on its transition unless a repair dominates")
tg = np.linspace(1e-4, 1 - 1e-4, 200001)
_, W1g, W2g = Wd(tg)
pos, neg = tg[W2g > 0], tg[W2g < 0]
P(f"    W'' > 0 on t in ({pos.min():.3f}, {pos.max():.3f}), W'' < 0 on ({neg.min():.3f}, {neg.max():.3f}); "
  f"max W'' t^2 on the lower half = {float(np.max(W2g * tg ** 2 * (tg < 0.5))):.4f} at t = {tg[np.argmax(W2g * tg ** 2 * (tg < 0.5))]:.3f}")
dstar = sp.simplify(Estar_s - Es + Dsy ** 2 / Delta_s)
check("T1 (i) W'' takes both signs on (0, 1) [Lean DE7: every C^2 plateau gate does]; (ii) E_* - E = -D^2/Delta, "
      ">= 0 on the no-ghost branch Delta < 0 [Lean]",
      f"W'' > 0 on ({pos.min():.3f}, 0.5), < 0 on (0.5, {neg.max():.3f}); symbolic residual {dstar}",
      pos.size > 0 and neg.size > 0 and dstar == 0,
      "so B f'' t_R^2 > 0 somewhere for either sign of B, and E_* > 0 there: growth rate ~ sqrt(16 E_*/(9F)) k^2")
W2MAXT2 = float(np.max(W2g * tg ** 2 * (tg < 0.5)))
OUT["numbers"]["T1"] = {"W2_pos_interval": [float(pos.min()), float(pos.max())], "max_W2_t2_lower_half": W2MAXT2}

# =================================================================================== the coefficients on a transition
C2S = (7.3e-3, 0.067)                                         # L340's tracking floor and window top (leaf-averaged c2)
EPS = 1.0


def gate_derivs(Rh, Kh, xc0, p, w, absolute=False, prescribed=None):
    """t and the gate's derivatives f_R, f_RR, f_RK, f_KK (hat units: R/Lambda, K/sqrt(Lambda)).  absolute=True: the
    gate reads R_abs = R + (2/3) K^2 - 2 (Lambda = 1); prescribed (MUTATE): no second variation."""
    if prescribed is None:
        prescribed = MUTATE
    Ra = (Rh + 2 * Kh ** 2 / 3 - 2.0) if absolute else Rh
    t = t_f(Ra, Kh, EPS, xc0, OL, p, w)
    tr, tk = tR_f(Ra, Kh, EPS, xc0, OL, p, w), tK_f(Ra, Kh, EPS, xc0, OL, p, w)
    tkk, trk = tKK_f(Ra, Kh, EPS, xc0, OL, p, w), tRK_f(Ra, Kh, EPS, xc0, OL, p, w)
    if absolute:                                              # chain rule through R_abs(R, K); t is linear in R_abs
        aK = 4 * Kh / 3
        tkk = tkk + 2 * aK * trk + (4.0 / 3) * tr
        tk = tk + aK * tr
    _, W1, W2 = Wd(t)
    fR = W1 * tr
    fRR = W2 * tr ** 2
    fRK = W2 * tr * tk + W1 * trk
    fKK = W2 * tk ** 2 + W1 * tkk
    if prescribed:
        fRR, fRK, fKK = 0.0 * fRR, 0.0 * fRK, 0.0 * fKK
    return t, fR, fRR, fRK, fKK


def assemble(Rh, gd, b, eta, c2, sgnB=1.0):
    """Z, Delta, E_*, F (units M^2, M^2/Lambda) for G = B f + C(R), B = sgnB b M^2 Lambda, C the Lambda-scaled repair."""
    t, fR, fRR, fRK, fKK = gd
    B = sgnB * b
    CR, CRR = -eta * np.arctan(Rh), -eta / (1 + Rh ** 2)
    Z = 1 + 2 * (B * fR + CR)
    Cc = -(2.0 / 3 + c2) + B * fKK
    Dd = B * fRK
    Dl = Cc + 2 * Z / 3
    with np.errstate(divide="ignore", invalid="ignore"):
        F = (2 * Z / 3) * Cc / Dl
        Es = B * fRR + CRR - Dd ** 2 / Dl
    return Z, Dl, Es, F


# ============================================================================================ C2 lead-track control
banner("C2  CONTROL: the lead track's midpoint witness, recomputed from this lane's own coefficients")
xc0_w = 1.0 / OL                                              # x_c = Omega_L0 x_c0 = 1
_gw = gate_derivs(np.array([8 / 27]), 1.0, xc0_w, 1.0, 1.0, prescribed=False)
Zw, Dw, Ew, Fw = assemble(np.array([8 / 27]), _gw, 1e-10, 1e-6, 1 / 50)
LEAD = {"Z": 0.99999942456410589874825626312711899, "Delta": -0.020000383423929400834495824581920671,
        "E": -0.00000091929382091038438219572426957174414, "F": 22.888436912413043270827572209011945}
mine = {"Z": float(Zw[0]), "Delta": float(Dw[0]), "E": float(Ew[0]), "F": float(Fw[0])}
rel = {k: abs(mine[k] / LEAD[k] - 1) for k in LEAD}
P(f"    this lane: {mine}\n    lead track (35-digit): Z {LEAD['Z']:.15f}, Delta {LEAD['Delta']:.15f}, E_* {LEAD['E']:.10e}, F {LEAD['F']:.12f}")
check("C2 CONTROL: at the lead track's midpoint witness this lane's Z, Delta, E_*, F reproduce its recorded values",
      {k: f"{v:.1e}" for k, v in rel.items()}, max(rel.values()) < 1e-9,
      "same operator, independent code path (S2 derived it; S1 the gate derivatives)")

# ============================================================================ the transition of a real galaxy at z
FEET = ("canonical", "alt")
YGRID = np.logspace(-9, 4, 6001)


def transition(z, Mb, foot, p, xc0, w, absolute=False):
    """hat R and K along a point-mass galaxy's upper-branch profile (CMC leaf K = 3H(z)), b(y), restricted to the
    gate's transition 0 < t < 1 (plus the flanks for the unrepaired sign)."""
    a0 = A0[foot]
    H = H0 * math.sqrt(E2(z))
    Kh = math.sqrt(9 * H ** 2 / LAMc2)
    y = YGRID
    r = np.sqrt(G_ * Mb * MS / (y * a0))
    rho_dyn = Mb * MS * (h_of(y) - y * dh_of(y)) / (2 * math.pi * r ** 3 * y)
    rho_bar = Om * rho_crit0 * (1 + z) ** 3
    Rh = 2 * (rho_dyn - rho_bar) / RHO_L
    t = t_f((Rh + 2 * Kh ** 2 / 3 - 2.0) if absolute else Rh, Kh, EPS, xc0, OL, p, w)
    b = AH[foot] * q_of(y)
    return y, r, Rh, Kh, b, t


def eta_min_case(z, Mb, foot, p, xc0, w, c2, sgnB=1.0, bscale=1.0, absolute=False):
    y, r, Rh, Kh, b, t = transition(z, Mb, foot, p, xc0, w, absolute)
    m = (t > 0) & (t < 1)
    if not m.any():
        return None
    yy, RR, bb, rk = y[m], Rh[m], bscale * b[m], r[m] / KPC
    gd = gate_derivs(RR, Kh, xc0, p, w, absolute)
    t0 = gd[0]
    Z0, D0, E0, F0 = assemble(RR, gd, bb, 0.0, c2, sgnB)
    good0 = (E0 < 0) & (D0 < 0) & (Z0 > 0) & (F0 > 0)
    lo = np.zeros_like(RR); hi = np.full_like(RR, 0.3)      # eta < 1/pi keeps Z > 0; the ceiling is <= 0.032 anyway
    for _ in range(64):                                       # bisection in eta at every point (monotone on [0, 0.3])
        mid = 0.5 * (lo + hi)
        Zm, Dm, Em, Fm = assemble(RR, gd, bb, mid, c2, sgnB)
        ok = (Em < 0) & (Dm < 0) & (Zm > 0) & (Fm > 0)
        hi = np.where(ok, mid, hi); lo = np.where(ok, lo, mid)
    need = np.where(good0, 0.0, hi)
    i = int(np.argmax(need))
    bad = E0 > 0
    has_mid = t0.min() < 0.5 < t0.max()
    mid_of = lambda arr: float(np.interp(0.5, t0, arr)) if has_mid else None
    return {"eta_min": float(need[i]), "t_at": float(t0[i]), "y_at": float(yy[i]), "b_at": float(bb[i]),
            "unrep_Emax": float(np.max(E0)), "unrep_bad_frac": float(np.mean(bad)),
            "unrep_t_bad": [float(t0[bad].min()), float(t0[bad].max())] if bad.any() else None,
            "y_edge": mid_of(yy), "b_edge": mid_of(bb), "Kh": float(Kh), "Rh_mid": mid_of(RR),
            "r_edge_kpc": mid_of(rk), "F_at": float(F0[i]), "E_at": float(E0[i])}


# ============================================================================================ C1 XR3's couplings
banner("C1  CONTROL: the MOND-normalised edge coupling b(z) against XR3 K6 (p = 1, x_c0 = 2.5, 1e11 Msun, canonical)")
XR3 = {0.5: 3.09e-08, 1.0: 1.75e-07, 1.5: 8.67e-07, 2.0: 3.61e-06, 2.5: 1.27e-05, 3.0: 3.88e-05, 3.5: 1.06e-04, 4.0: 2.61e-04}
c1rows, c1dev = [], 0.0
for z, bx in XR3.items():
    rr = eta_min_case(z, 1e11, "canonical", 1.0, 2.5, 1.0, C2S[0])
    dev = rr["b_edge"] / bx - 1
    c1dev = max(c1dev, abs(dev))
    c1rows.append((z, rr["y_edge"], rr["b_edge"], bx, dev))
    P(f"    z = {z:3.1f}: y_edge {rr['y_edge']:.3e} (r_e = {rr['r_edge_kpc']:.1f} kpc), b = {rr['b_edge']:.3e} vs XR3 {bx:.2e} ({dev:+.1%})")
check("C1 CONTROL: this lane's edge coupling reproduces XR3 K6's b(z) at z = 0.5-4 to 5%",
      f"max |dev| = {c1dev:.1%}", c1dev < 0.05,
      "XR3 used DE1's numeric edge ratios and 1/(32 pi); this lane the upper-branch profile with the mean-density term")
OUT["numbers"]["C1"] = c1rows

# ================================================================================ U1 / R1 / R2 the real transitions
banner("U1 R1 R2  THE REAL TRANSITIONS: unrepaired sign, the repair's minimal strength, and the window's reach")
ZS = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0]
MBS = [1e9, 1e10, 1e11, 1e12]
CELLS = [(1.0, 2.005), (1.0, 2.5), (1.0, 2.975), (0.5, 3.39), (1.9042, 2.3497)]
WS = [1.0, 0.5, 0.25]
TAB = {}
for (p, xc0) in CELLS:
    for w in WS:
        for foot in FEET:
            for Mb in MBS:
                for z in ZS:
                    for c2 in C2S:
                        rr = eta_min_case(z, Mb, foot, p, xc0, w, c2)
                        TAB[(p, xc0, w, foot, Mb, z, c2)] = rr
P(f"    {len(TAB)} transitions computed   [{time.time() - T0:.0f}s]")
have = [v for v in TAB.values() if v is not None]
u1_all = all(v["unrep_Emax"] > 0 for v in have)
u1_frac = [v["unrep_bad_frac"] for v in have]
bad_t = [v["unrep_t_bad"] for v in have if v["unrep_t_bad"]]
P(f"    unrepaired E_* > 0 on {sum(v['unrep_Emax'] > 0 for v in have)}/{len(have)} transitions; wrong-sign fraction of each "
  f"transition {min(u1_frac):.2f}-{max(u1_frac):.2f}; t-range of the wrong sign "
  f"{min(b[0] for b in bad_t) if bad_t else float('nan'):.3f}-{max(b[1] for b in bad_t) if bad_t else float('nan'):.3f}")
check("U1 at MOND normalisation the UNREPAIRED gate has E_* > 0 (wrong-sign k^4, Hadamard ill-posed) on part of EVERY "
      "real transition computed (z 0-12, M_b 1e9-1e12, both footings, 5 window cells, w = 1, 0.5, 0.25)",
      f"{sum(v['unrep_Emax'] > 0 for v in have)}/{len(have)}", u1_all and len(have) > 0,
      "T1's theorem made concrete: the lower (outer) half of every transition, where W'' > 0")

# baseline table: p = 1, x_c0 = 2.5, w = 1, 1e11, both footings
P("\n    BASELINE (p = 1, x_c0 = 2.5, w = 1, M_b = 1e11): eta_min along the transition vs the ceiling 3 c2/(2 pi)")
ETAMAX = {c2: 3 * c2 / (2 * math.pi) for c2 in C2S}
P(f"    ceilings: c2 = {C2S[0]}: eta < {ETAMAX[C2S[0]]:.3e};  c2 = {C2S[1]}: eta < {ETAMAX[C2S[1]]:.3e}")
for foot in FEET:
    for z in ZS:
        rr = TAB[(1.0, 2.5, 1.0, foot, 1e11, z, C2S[0])]
        if rr is None: continue
        P(f"    {foot:9s} z = {z:4.1f}: r_e = {rr['r_edge_kpc'] if rr['r_edge_kpc'] else float('nan'):7.1f} kpc, "
          f"y_edge = {rr['y_edge'] if rr['y_edge'] else float('nan'):.2e}, b_edge = {rr['b_edge'] if rr['b_edge'] else float('nan'):.2e}; "
          f"eta_min = {rr['eta_min']:.2e} (at t = {rr['t_at']:.2f}, y = {rr['y_at']:.2e})")
h1 = [TAB[(1.0, 2.5, 1.0, "canonical", 1e11, z, C2S[0])]["eta_min"] for z in ZS if z <= 4.0]
check("R1 [H1, pre-declared] with the lead track's Lambda-scaled concave repair, the minimal eta at every z <= 4 edge "
      "(1e11 canonical, p = 1, x_c0 = 2.5, w = 1) lies below the repair's own ceiling 3 c2/(2 pi) at c2 = 7.3e-3",
      f"max eta_min(z <= 4) = {max(h1):.2e} vs ceiling {ETAMAX[C2S[0]]:.2e}", max(h1) < ETAMAX[C2S[0]],
      "XR3's sufficient inequalities needed c2 > 0.067 from z ~ 3; the actual operator needs far less")


def z_wp(p, xc0, w, foot, Mb, c2, sgnB=1.0, bscale=1.0):
    last = None
    for z in ZS:
        rr = TAB.get((p, xc0, w, foot, Mb, z, c2)) if (sgnB == 1.0 and bscale == 1.0) else \
            eta_min_case(z, Mb, foot, p, xc0, w, c2, sgnB, bscale)
        if rr is None: continue
        if rr["eta_min"] >= 3 * c2 / (2 * math.pi):
            return last, z
        last = z
    return last, None


P("\n    z_wp: the highest listed z to which the repaired window stays open (first failing z in brackets)")
ZWP = {}
for (p, xc0) in CELLS:
    for w in WS:
        for c2 in C2S:
            row = []
            for foot in FEET:
                for Mb in MBS:
                    zo, zf_ = z_wp(p, xc0, w, foot, Mb, c2)
                    ZWP[f"{p}/{xc0}/{w}/{c2}/{foot}/{Mb:.0e}"] = [zo, zf_]
                    row.append(f"{foot[:3]} {Mb:.0e}: {zo if zo is not None else '-'}" + (f" [{zf_}]" if zf_ is not None else "+"))
            P(f"    p = {p:<6} x_c0 = {xc0:<6} w = {w:<4} c2 = {c2:<6}: " + "; ".join(row))
OUT["numbers"]["z_wp"] = ZWP

# sensitivities on the baseline
P("\n    SENSITIVITY (baseline, canonical, 1e11, c2 = 7.3e-3): B < 0 (the bad half is the inner one), b x 0.3 and x 3")
SENS = {}
for lab, sg, bs in (("B<0", -1.0, 1.0), ("b x 0.3", 1.0, 0.3), ("b x 3", 1.0, 3.0)):
    row = []
    for z in (1.0, 2.5, 4.0, 6.0, 8.0):
        rr = eta_min_case(z, 1e11, "canonical", 1.0, 2.5, 1.0, C2S[0], sg, bs)
        row.append((z, rr["eta_min"]))
    SENS[lab] = row
    P(f"    {lab:8s}: " + ", ".join(f"z = {z}: {e:.2e}" for z, e in row))
OUT["numbers"]["sensitivity"] = SENS

check("R2 (reported) eta_min and the window's reach z_wp per cell, mass, footing, w and c2; sensitivities",
      "see tables and results JSON", True, load_bearing=False)

# ================================================================================= N2-N4 lensing vs dynamics (slip)
banner("N2 N3 N4  LENSING vs DYNAMICS AT GATE TRANSITIONS (S4's slip on the real profiles)")
CC2 = c_ ** 2


def slip_case(z, Mb, foot, p, xc0, w, eta=0.0, gate=True):
    """(lensing - dynamics) potential Pi = G_R/M^2 = b Lambda f_R - eta arctan(R/Lambda) along the transition; returns
    max |c^2 dPi/dr| / (nu g_N) -- relative to the ungated MOND acceleration, an upper bound on g_dyn, so the ratio is
    conservative where the gate is partly off -- the transition's radii, R_hat at t = 1/2 and int nu g_N dr."""
    y, r, Rh, Kh, b, t = transition(z, Mb, foot, p, xc0, w)
    m = (t > 0) & (t < 1)
    ym, rm, Rm, bm, tm = y[m], r[m], Rh[m], b[m], t[m]
    gd = gate_derivs(Rm, Kh, xc0, p, w, prescribed=False)
    Pi = (bm * gd[1] if gate else 0.0 * bm) - eta * np.arctan(Rm)
    a0 = A0[foot]
    gN = ym * a0
    nu = 1 + h_of(ym) / ym
    gmond = nu * gN                                           # >= g_dyn = g_N (1 + f (nu - 1)): the MOND level, conservative
    ratio = CC2 * np.abs(np.gradient(Pi, rm)) / gmond
    o = np.argsort(rm)
    I_nu = float(np.trapz((nu * gN)[o], rm[o]))                 # >= int g_dyn dr over the transition
    return {"max_ratio": float(np.max(ratio)), "r_half": float(np.interp(0.5, tm, rm)), "r0": float(rm.max()),
            "r1": float(rm.min()), "R_half": float(np.interp(0.5, tm, Rm)), "I_nu": I_nu, "Pi_span": float(np.ptp(Pi)),
            "vf2": float(math.sqrt(G_ * Mb * MS * a0))}


P("    N2 -- the gate's own slip (no repair), baseline cell, 1e11 Msun: max |g_lens - g_dyn|/(nu g_N) on the transition")
N2 = {}
for foot in FEET:
    row = []
    for z in ZS:
        sc = slip_case(z, 1e11, foot, 1.0, 2.5, 1.0)
        N2[f"{foot}/{z}"] = sc
        row.append(f"z={z:g}: {sc['max_ratio']:.2g}")
    P(f"    {foot:9s} " + ", ".join(row))
OUT["numbers"]["N2"] = N2
check("N2 (reported) the varied gate's own slip: lensing and dynamics differ in every transition layer by the gradient "
      "of B f_R/M^2 (S4); max ratio at z = 0.25 / 2.5 / 4 / 6 (canonical, 1e11)",
      f"{N2['canonical/0.25']['max_ratio']:.2g} / {N2['canonical/2.5']['max_ratio']:.2g} / {N2['canonical/4.0']['max_ratio']:.2g} / "
      f"{N2['canonical/6.0']['max_ratio']:.2g}", True, load_bearing=False)

P("\n    N3 -- the Lambda-scaled repair's slip around KiDS-epoch lenses (z = 0.25), with eta sized for edges at z_t")
ZL_K = 0.25
N3 = {}
etas = {zt: TAB[(1.0, 2.5, 1.0, "canonical", 1e11, zt, C2S[0])]["eta_min"] for zt in (0.5, 1.0, 1.5, 2.0, 2.5, 4.0, 6.0)}
for Mb in (1e10, 1e11, 1e12):
    for foot in FEET:
        base = slip_case(ZL_K, Mb, foot, 1.0, 2.5, 1.0, 0.0, gate=False)
        # rigorous lower bound on the max ratio over [r_1/2, r_0]: arctan(R) falls by arctan(R_1/2) there (t = 0 is R = 0),
        # so c^2 eta arctan(R_1/2) <= int |Delta g| dr <= max_ratio x int g_dyn dr <= max_ratio x int nu g_N dr
        eta10 = 0.1 * base["I_nu"] / (CC2 * math.atan(base["R_half"]))
        rows = {}
        for zt, et in etas.items():
            scn = slip_case(ZL_K, Mb, foot, 1.0, 2.5, 1.0, et, gate=False)
            rows[zt] = scn["max_ratio"]
        reach = max([zt for zt, et in etas.items() if et <= eta10], default=None)
        N3[f"{Mb:.0e}/{foot}"] = {"eta_at_10pct_bound": eta10, "max_ratio_by_zt": rows, "z_reach": reach}
        P(f"    lens {Mb:.0e} {foot:9s}: 10% lensing = dynamics needs eta <= {eta10:.2e} (rigorous bound); max ratio for eta(z_t) "
          + ", ".join(f"{zt:g}: {v:.2g}" for zt, v in rows.items()) + f";  edges repairable up to z_t = {reach}")
OUT["numbers"]["N3"] = {"eta_min_by_zt": etas, "cases": N3}
worst_reach = min((v["z_reach"] if v["z_reach"] is not None else 0.0) for v in N3.values())
check("N3 (reported) the lead track's Lambda-scaled repair: its C_R = -eta M^2 arctan(R/Lambda) falls by eta arctan(R_1/2) "
      "across every lens's transition, a lensing-dynamics slip of relative size ~ eta (c/v_f)^2; keeping it below 10% at "
      "KiDS lenses (1e10-1e12, z = 0.25) caps eta, and so caps the redshift of the edges it can repair",
      f"lowest reach over lenses/footings: z_t = {worst_reach}", True,
      "the repair's slip is O(eta) in potential against galaxy potentials O(v_f^2/c^2) ~ 1e-7-1e-6", load_bearing=False)

P("\n    N4 -- ANY metric-only repair: at a given epoch every system's transition sits at the same R (the gate reads (R, K)),")
P("    so C_RR(R, K) <= -max_systems B f_RR there; a lens g then carries a slip >= I_max/2 over its transition,")
P("    I_max = int_lower-half B_max f_RR dR, set by the most massive bound system at that epoch.  Floor on the max ratio:")
N4 = {}
for zq in (0.25, 1.0, 2.0):
    for Mmax in (1e12, 1e14):
        y, r, Rh, Kh, b, t = transition(zq, Mmax, "canonical", 1.0, 2.5, 1.0)
        m = (t > 0) & (t < 0.5)
        gd = gate_derivs(Rh[m], Kh, 2.5, 1.0, 1.0, prescribed=False)
        o = np.argsort(Rh[m])
        Imax = float(np.trapz((b[m] * np.maximum(gd[2], 0.0))[o], Rh[m][o]))
        row = []
        for Mg in (1e9, 1e10, 1e11, 1e12):
            sg = slip_case(zq, Mg, "canonical", 1.0, 2.5, 1.0, 0.0, gate=False)
            fl = CC2 * 0.5 * Imax / sg["I_nu"]
            N4[f"{zq}/{Mmax:.0e}/{Mg:.0e}"] = fl
            row.append(f"{Mg:.0e}: {fl:.2g}")
        P(f"    z = {zq:4.2f}, most massive system {Mmax:.0e} Msun (I_max = {Imax:.2e}): floor per lens " + ", ".join(row))
OUT["numbers"]["N4"] = N4
check("N4 (reported) the floor for ANY metric-only repair: lensing-dynamics slip in each lens's transition layer, set by "
      "the most massive bound system's B at that epoch (canonical, p = 1, x_c0 = 2.5, w = 1)",
      f"z = 0.25, clusters (1e14) setting B_max: 1e11 lens {N4['0.25/1e+14/1e+11']:.2g}, 1e10 lens {N4['0.25/1e+14/1e+10']:.2g}; "
      f"galaxies (1e12) setting it: 1e11 lens {N4['0.25/1e+12/1e+11']:.2g}", True,
      "the floor scales with B_max: it is the constitutive coupling of the largest bound regions, not the lens's own", load_bearing=False)

# ================================================================================================ N1 the repair's cost
banner("N1  THE REPAIR'S STRUCTURAL COST (indicative, not gates)")
P("    any R-only concave repair: C_R(+inf) - C_R(-inf) = int C_RR dR < 0 -- the R^(3)+sigma^2 coefficient differs")
P("    between over- and under-dense leaves.  The arctan form: C_R = -eta M^2 arctan(R/Lambda) -> -/+ (pi/2) eta M^2, i.e.")
P("    a Newton coupling G/(1 -/+ pi eta) wherever |delta rho| >> rho_L (every bound structure; CMB-epoch perturbations,")
P("    where |R|/Lambda = 2 |delta| rho_bar/rho_L ~ 1e4 for delta ~ 1e-5 at z ~ 1100).  Scale analogy (L350):")
CAPS = (math.pi ** -1 * 1.5 * 0.63e-3, math.pi ** -1 * 1.5 * 2.9e-3)
P(f"    pi eta <= |G_cos/G_N - 1| cap 1.5 x (0.63-2.9)e-3  =>  eta <~ {CAPS[0]:.1e} to {CAPS[1]:.1e}")
cross = {}
for foot in FEET:
    zc = [None, None]
    for j, cap in enumerate(CAPS):
        for z in ZS:
            rr = TAB[(1.0, 2.5, 1.0, foot, 1e11, z, C2S[0])]
            if rr and rr["eta_min"] > cap:
                zc[j] = z; break
    cross[foot] = zc
    P(f"    baseline {foot}: eta_min first exceeds the tighter/looser indicative caps at z = {zc[0]} / {zc[1]}")
OUT["numbers"]["N1"] = {"caps": CAPS, "first_z_over_caps": cross}
check("N1 (reported, indicative) the repair's sign-dependent coupling and the redshift where the needed eta reaches "
      "the L350-analog scale", cross, True, load_bearing=False)

# ======================================================================================================= M1 the doors
banner("M1  THE DOORS (CV1's A6 obligation): which homogeneous backgrounds sit on the off-plateau")
P("    contrast door: R = R^(3) + sigma^2 = 0 on flat FRW => s = 0 => t = (w - 1)/(2w) <= 0 for w <= 1: f and every")
P("    derivative vanish on the background and in its perturbation theory to all orders (exact).")
zz = np.linspace(0, 20, 200001)
DOORS = {}
for (p, xc0) in CELLS:
    uF = 1.5 * Om * (1 + zz) ** 3 / E2(zz) * (1.0 / E2(zz)) ** p
    umax, zmax = float(uF.max()), float(zz[np.argmax(uF)])
    wmax = 1 - umax / xc0
    DOORS[f"{p}/{xc0}"] = {"u_FRW_max": umax, "at_z": zmax, "w_max": wmax}
    P(f"    absolute door, cell (p = {p}, x_c0 = {xc0}): u_FRW = (3/2) Om(z) E^-2p peaks at {umax:.4f} (z = {zmax:.2f}) "
      f"=> off-plateau iff w <= {wmax:.3f}")
# the absolute door's own repaired strength (baseline cell, w at its FRW-safe maximum, rounded down)
wabs = math.floor(DOORS["1.0/2.5"]["w_max"] * 100) / 100
ab = []
for z in (0.5, 1.0, 2.0, 2.5, 4.0):
    rr = eta_min_case(z, 1e11, "canonical", 1.0, 2.5, wabs, C2S[0], absolute=True)
    ab.append((z, None if rr is None else rr["eta_min"], None if rr is None else rr["unrep_Emax"] > 0))
P(f"    absolute door, baseline cell, w = {wabs}: (z, eta_min, unrepaired wrong-sign) = {ab}")
P("    matter-only door: no metric-only form.  On the lensing = dynamics sector (KiDS requires it) the leaf curvature is")
P("    R^(3) = 16 pi G rho_dyn (phantom included; S2's R^(3) linear part is -4 lap zeta), so every functional of leaf")
P("    invariants reads rho_dyn.  The matter-only reading is the LOWER static branch of the same geometric term (DE4's")
P("    bistable band), selected by history; a term reading u^mu u^nu T_mu nu couples matter to the khronon (requirement 11).")
OUT["numbers"]["doors"] = {"absolute_w_max": DOORS, "absolute_baseline": ab}
check("M1 (reported) the doors' homogeneous backgrounds: contrast off-plateau for all w <= 1; absolute off-plateau iff "
      "w <= w_max(cell); matter-only has no metric-only action form (a branch, not a term)",
      {k: round(v["w_max"], 3) for k, v in DOORS.items()}, True, load_bearing=False)

# ============================================================================================================ summary
banner("SUMMARY")
nlb = sum(1 for n, ok, lb in CH if lb and not ok)
P(f"  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}   [{time.time() - T0:.0f}s]")
OUT["numbers"]["baseline"] = {f"{foot}/{z}": TAB[(1.0, 2.5, 1.0, foot, 1e11, z, C2S[0])] for foot in FEET for z in ZS}
OUT["numbers"]["eta_ceiling"] = ETAMAX
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"  wrote {os.path.basename(fn)}")
sys.exit(1 if nlb else 0)
