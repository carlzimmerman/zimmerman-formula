#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CV2 -- V0 FOR THE C-H/K BRANCH, STEP 2: THE COVARIANT ACTION, AND THREE OF ITS REDUCTIONS.

THE ACTION (signature -+++, x0 = ct; C-H's clock tau, n_mu = -d_mu tau/sqrt(X), N = X^-1/2, h = g + n n, K, a_mu = D_mu ln N,
Delta_h the leaf Laplace-Beltrami operator, <.>_h the proper-volume leaf average, alpha = a0/c^2; ACTION.md for C-H's
fields, filter, caps and endpoint terms, unchanged):
  I_V0 = c^3/(16 pi G) Int d^4x sqrt(-g) {
           R - 2 Lambda + 2 h^{mu nu}(D_mu U - a_mu)(D_nu U - a_nu)                          C-H's chassis
           + alpha_c a_mu a^mu - c_2 (K - <K>_h)^2                                            L340's BPS terms, L350's leaf average
           + 2 alpha^2 f q(h^{mu nu} D_mu W_b D_nu W_b / alpha^2)                              the region kernel, nu_mono's q
           + Int_0^b dz L (d_z W - Delta_h W) + lambda_0 (W_0 - Y)                            C-H's heat flow, started from Y
           + 2 Psi [(Delta_h - m^2 (1 - f)) Y - f Delta_h (U - V)] - 2 sigma m^2 (1 - f) Y^2   the region field (L361, lifted)
           + 2 Lam_d [Delta_h V - (4 pi G/c^4)(eps_d - <eps_d>_h)] }                          L353's pair, eps_d = n n T_d
         + GHY caps + S_matter[g] + S_dark[g; the dark state]
  f = F(R^(3) + sigma_ij sigma^ij, K; Lambda) is the gate (its functional form and normalisation are the dark-energy thread's
  piece; CV3 varies it).  Every added field (Y, Psi, V, Lam_d) is a leafwise auxiliary like C-H's W, L, lambda_0.

WHAT THIS LANE CHECKS
  B1 [the non-relativistic limit, sympy] on the static branch tau = x0, ds^2 = -e^{2 phi} c^2 dt^2 + e^{-2 psi} dx^2: the
     leaf curvature of the conformally flat leaf, computed from Christoffel symbols, makes N sqrt(h) R^(3) =
     e^{phi - psi}(2|grad psi|^2 - 4 grad phi.grad psi) + a total derivative; the psi equation gives psi = phi; and at leading
     order the whole action, with U = u/c^2, Y = w/c^2, V = v/c^2 and the multipliers scaled by 1/c^2, is CV1's Lagrangian
     exactly (every term, every factor of c).
  B2 [reduction (iii): L340's static block] on a gate-on plateau (f = 1 with every derivative zero, Lean CV1
     gate_flat_above_one), M = 0 and no dark state, the Psi constraint Delta_h (Y - U) = 0 fixes Y = U + const for EVERY leaf
     metric, so V0 IS C-H/K there.  Checked on L340's own unitary block (its E-list copied verbatim, extended by Y and Psi):
     the 6x6 determinant is a nonzero constant times L340's 4x4 determinant at every omega, and the omega -> 0 responses of
     psi, phi, beta and U are L340's (static MOND solution, no frozen mode).  The leaf average changes no k != 0 mode.
  B3 [FRW with the leaf average, minisuperspace] with the gate off (t = 0, f = 0 to every order) the auxiliaries' own
     equations are solved by Y = Psi = 0 and V = Lam_d = 0, U homogeneous; their contribution to the metric equations
     vanishes there; alpha_c a^2 = 0 and (K - <K>)^2 = 0 identically; so the Friedmann equation is GR's,
     H^2 = 8 pi G rho/3 + Lambda c^2/3 (G_cos = G).  Control: the plain -c_2 K^2 gives H^2 (1 + 3 c_2/2) = ... (L350 G1).
  B4 [the dark source on a closed leaf] Delta_h V = (4 pi G/c^4)(eps_d - <eps_d>) is solvable on a torus for a positive
     density (spectral solve, residual at machine level); the unprojected source is not (its zero mode is nonzero).
  MUTATE=1 drops the leaf average (-c_2 K^2): B3's G_cos = G must FAIL.  rc = 1.

SCOPE.  The gate is a prescribed function of the leaf geometry here: its metric/clock variation (the B dF terms) is CV3.
B2 is the frozen-coefficient block at principal order, as L340's; B1 is leading weak-field order, as ACTION.md's.  The
dark state is a slot: its own action and its survival of stream crossing under criterion B (XR3 calc 7) are not here.

Run from the repository root:  python3 real_research/chk_v0_2026/CV2_covariant_action.py
"""
import os, sys, json, math, time, warnings
import numpy as np
import sympy as sp
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "CV2", "CV2_covariant_action"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()


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
    P("\n  *** MUTATE=1: the leaf average is dropped (-c_2 K^2); B3's G_cos = G must FAIL ***")

# ============================================================================================ B1 the NR limit
banner("B1  THE NON-RELATIVISTIC LIMIT: the covariant action on the static branch, leading order, every factor of c")
X3 = sp.symbols("x y z", real=True)
ph, ps = sp.Function("phi")(*X3), sp.Function("psi")(*X3)
# leaf metric h_ij = e^{-2 psi} delta_ij: Ricci scalar from Christoffel symbols
hmat = sp.exp(-2 * ps) * sp.eye(3); hinv = hmat.inv()
Gam = [[[sum(hinv[i, l] * (sp.diff(hmat[l, j], X3[k]) + sp.diff(hmat[l, k], X3[j]) - sp.diff(hmat[j, k], X3[l]))
             for l in range(3)) / 2 for k in range(3)] for j in range(3)] for i in range(3)]
def Ric(j, k):
    return sp.simplify(sum(sp.diff(Gam[i][j][k], X3[i]) - sp.diff(Gam[i][j][i], X3[k])
                           + sum(Gam[i][i][l] * Gam[l][j][k] - Gam[i][k][l] * Gam[l][j][i] for l in range(3))
                           for i in range(3)))
R3 = sp.simplify(sum(hinv[j, k] * Ric(j, k) for j in range(3) for k in range(3)))
grad = lambda F: [sp.diff(F, xx) for xx in X3]
dot = lambda A, B: sum(a_ * b_ for a_, b_ in zip(A, B))
lap = lambda F: sum(sp.diff(F, xx, 2) for xx in X3)
EH = sp.exp(ph) * sp.exp(-3 * ps) * R3                                   # N sqrt(h) R^(3)  (K = 0 on the static branch)
claim = sp.exp(ph - ps) * (2 * dot(grad(ps), grad(ps)) - 4 * dot(grad(ph), grad(ps)))
# the difference must be a total divergence: 4 div(e^{phi - psi} grad psi)
tdiv = sum(sp.diff(4 * sp.exp(ph - ps) * sp.diff(ps, xx), xx) for xx in X3)
eh_ok = sp.simplify(sp.expand(EH - claim - tdiv)) == 0
P(f"    R^(3)[e^(-2 psi) delta] = {sp.simplify(R3 * sp.exp(-2 * ps))} e^(2 psi);  N sqrt(h) R^(3) - claim - 4 div(e^(phi-psi) grad psi) = 0: {eh_ok}")
# leading order: every field small, O(eps); keep the O(eps^2) density
eps = sp.symbols("epsilon", positive=True)
c_, G_, a0_, m_ = sp.symbols("c G a0 m", positive=True)
f_, sg_, M2_ = sp.symbols("f sigma M2", real=True)
Phi, u, w, v, PsiN, lamN, psiM = [sp.Function(n)(*X3) for n in ("Phi", "u", "w", "v", "Psi", "lam", "psim")]
rhob, rhod, rhodbar, rhobbar = sp.symbols("rho_b rho_d rhobar_d rhobar_b", real=True)
Zs = sp.symbols("Z", positive=True)
qf = sp.Function("q")
# covariant integrand pieces at leading order: sqrt(-g) h^{ij} -> delta, Delta_h -> lap, e^{phi-psi} -> 1 at O(eps^2)
Ub, Yb, Vb = u / c_ ** 2, w / c_ ** 2, v / c_ ** 2                      # U = u/c^2, Y = w/c^2, V = v/c^2
Psib, Lamb = PsiN / c_ ** 2, lamN / c_ ** 2
phib, psib = Phi / c_ ** 2, psiM / c_ ** 2                                # metric potentials
alpha = a0_ / c_ ** 2
braces = (2 * dot(grad(psib), grad(psib)) - 4 * dot(grad(phib), grad(psib))             # EH after the total derivative
          + 2 * dot([gu - gp for gu, gp in zip(grad(Ub), grad(phib))], [gu - gp for gu, gp in zip(grad(Ub), grad(phib))])
          + 2 * alpha ** 2 * f_ * qf(dot(grad(w), grad(w)) / c_ ** 4 / alpha ** 2)
          + 2 * Psib * (lap(Yb) - M2_ * Yb - f_ * lap(Ub - Vb)) - 2 * sg_ * M2_ * Yb ** 2
          + 2 * Lamb * (lap(Vb) - 4 * sp.pi * G_ / c_ ** 4 * (rhod - rhodbar) * c_ ** 2))
dens = c_ ** 4 / (16 * sp.pi * G_) * braces                              # c^3/(16 pi G) d^4x = c^4/(16 pi G) dt d^3x
matter = -(rhob + rhod) * Phi                                            # minimally coupled dust at leading order: -rho c^2 (phi) per c^2 ... = -rho Phi
L_cov = sp.expand(dens + matter)
# psi equation: vary psim, solve psi = Phi
EL_psi = sp.euler_equations(L_cov, [psiM], X3)[0].lhs
psi_eq_ok = sp.simplify(EL_psi.subs(psiM, Phi).doit()) == 0
L_red = sp.expand(L_cov.subs(psiM, Phi).doit())
# CV1's Lagrangian in the same notation (S = 1 at this order: the filter acts inside q, unchanged)
L_cv1 = (-(rhob + rhod) * Phi - (2 * dot(grad(Phi), grad(u)) - dot(grad(u), grad(u))) / (8 * sp.pi * G_)
         + a0_ ** 2 * f_ * qf(dot(grad(w), grad(w)) / a0_ ** 2) / (8 * sp.pi * G_)
         + PsiN * (lap(w) - M2_ * w - f_ * lap(u - v)) / (8 * sp.pi * G_)
         + lamN * (lap(v) - 4 * sp.pi * G_ * (rhod - rhodbar)) / (8 * sp.pi * G_)
         - sg_ * M2_ * w ** 2 / (8 * sp.pi * G_))
nr_diff = sp.simplify(sp.expand(L_red - L_cv1))
P(f"    psi equation solved by psi = Phi: {psi_eq_ok};  (covariant action on the static branch) - (CV1's Lagrangian) = {nr_diff}")
# the dark component's extra coupling: -dL/d rho_d = Phi + lam/2 (as in CV1)
coupling = sp.simplify(-sp.diff(L_red, rhod))
P(f"    dark component's coupling from the covariant pair: -dL/d rho_d = {coupling}")
OUT["numbers"]["B1"] = {"eh_identity": eh_ok, "psi_eq": psi_eq_ok, "difference": str(nr_diff), "coupling": str(coupling)}
check("B1 at leading weak-field order the covariant action is CV1's Lagrangian exactly: the leaf curvature gives "
      "e^(phi-psi)(2|grad psi|^2 - 4 grad phi.grad psi) + a divergence, psi = Phi, and every added term lands with its "
      "factors of c", f"EH identity {eh_ok}; psi = Phi {psi_eq_ok}; difference {nr_diff}; coupling {coupling}",
      eh_ok and psi_eq_ok and nr_diff == 0 and sp.simplify(coupling - (Phi + lamN / 2)) == 0,
      "psi = Phi at this order is lensing = dynamics for both species (the pair and the region field add no psi source)")

# ============================================================================================ B2 L340's static block
banner("B2  REDUCTION (iii): ON A GATE-ON PLATEAU V0 IS C-H/K, AND L340's BLOCK IS RECOVERED")
k, C, c2, ac, om = sp.symbols('k C c_2 alpha_c omega', real=True)
psi_, phi_, beta_, U_, R_ = sp.symbols('psi phi beta U R')
Y_, Pc_ = sp.symbols('Y Psi_c')
D = -sp.I * om
epsl = -c2


def block340(C_, eps_, ac_):                                      # L340 H1's E-list, verbatim (a2 = a3 = g = 0)
    E = [4*k**2*psi_ - 4*k**2*phi_ - D*(-12*D*psi_ + 4*k**2*beta_ + 6*eps_*(3*D*psi_ - k**2*beta_)),
         -4*k**2*psi_ - 4*k**2*(U_ - phi_) + 2*ac_*k**2*phi_ - R_,
         4*k**2*D*psi_ - 2*eps_*k**2*(3*D*psi_ - k**2*beta_) + D*R_,
         4*k**2*(U_ - phi_) + 4*k**2*C_*U_]
    return E


def blockV0(C_, eps_, ac_):
    """V0 on the plateau: the kernel acts on Y (2 k^2 C Y^2 in L_2), the constraint 2 Psi Delta_h (Y - U) -> -2 k^2 Psi (Y - U)."""
    E = block340(C_, eps_, ac_)
    E[3] = 4*k**2*(U_ - phi_) + 2*k**2*Pc_                         # delta U: the kernel's 4k^2 C U is replaced by the constraint force
    E.append(4*k**2*C_*Y_ - 2*k**2*Pc_)                            # delta Y
    E.append(-2*k**2*(Y_ - U_))                                    # delta Psi
    return E


def mat(E, X):
    M = sp.Matrix([[sp.diff(e_, x_) for x_ in X] for e_ in E])
    S = sp.Matrix([-e_.subs({x_: 0 for x_ in X}) for e_ in E])
    return M, S


X4, X6 = [psi_, phi_, beta_, U_], [psi_, phi_, beta_, U_, Y_, Pc_]
M4, S4 = mat(block340(C, epsl, ac), X4)
M6, S6 = mat(blockV0(C, epsl, ac), X6)
# exact elimination of (Y, Psi): the Schur complement of the omega-independent (Y, Psi) block
Ablk, Bblk, Cblk, Dblk = M6[:4, :4], M6[:4, 4:], M6[4:, :4], M6[4:, 4:]
schur = sp.simplify(Ablk - Bblk * Dblk.inv() * Cblk)
schur_same = sp.simplify(schur - M4) == sp.zeros(4, 4)
src_same = sp.simplify(S6[:4, 0] - Bblk * Dblk.inv() * S6[4:, 0] - S4) == sp.zeros(4, 1)
ratio = sp.factor(Dblk.det())                                      # det M6 = det(D) det(Schur) = det(D) det M4
ratio_ok = sp.simplify(sp.diff(ratio, om)) == 0 and sp.simplify(ratio) != 0
same = [schur_same, src_same]
sol4 = M4.LUsolve(S4)
psiN = -R_ / (4 * k ** 2)
num_, den_ = sp.fraction(sp.cancel(sp.together(sol4[0] / psiN)))
lim_psi = sp.factor(sp.cancel(num_.subs(om, 0) / den_.subs(om, 0)))
static_psi = sp.factor((1 + C) / (1 - ac * (1 + C) / 2))
det0 = sp.factor(sp.simplify((ratio * M4.det()).subs(om, 0)))
P(f"    det M_V0(omega) / det M_L340(omega) = {ratio}  (independent of omega and nonzero: the same modes)")
P(f"    eliminating (Y, Psi) exactly: Schur complement = L340's matrix {schur_same}; reduced source = L340's {src_same}")
P(f"    omega -> 0: psi/psi_N = {lim_psi}  (L340's static MOND solution {static_psi});  det M_V0(0) = {det0}")
OUT["numbers"]["B2"] = {"det_ratio": str(ratio), "same_responses": same, "psi_limit": str(lim_psi), "det0": str(det0)}
check("B2 on a gate-on plateau V0 reduces to C-H/K: the 6x6 block's determinant is an omega-independent nonzero factor "
      "times L340's, the responses of psi, phi, beta, U are L340's, and the omega -> 0 limit is its static MOND solution "
      "with no frozen mode", f"det ratio {ratio}; same responses {same}; psi -> {lim_psi}; det(0) = {det0}",
      ratio_ok and all(same) and sp.simplify(lim_psi - static_psi) == 0 and det0 != 0,
      "Delta_h(Y - U) = 0 gives Y = U + const for every leaf metric, so the elimination is exact nonlinearly, not only in "
      "this block; the leaf average equals -c_2 K^2 on every k != 0 mode (L350 G5); L340's H2/H3 health carries over")

# ============================================================================================ B3 FRW
banner("B3  FRW WITH THE LEAF AVERAGE (minisuperspace): the gate off, the auxiliaries off, GR's Friedmann equation")
t = sp.symbols("t", real=True)
a, Nl = sp.Function("a")(t), sp.Function("N")(t)
Yt, Pst, Vt, Lt, Ut = [sp.Function(n)(t) for n in ("Y", "Psi", "V", "Lam", "U")]
Lam_, c2s, acs, m2s, sgs = sp.symbols("Lambda c_2 alpha_c m2 sigma", real=True)
rho0 = sp.symbols("rho0", positive=True)
Hc = sp.diff(a, t) / (Nl * a)                                            # H/c with x0 = c t absorbed: K = 3 H (per unit x0)
K = 3 * Hc
Kbar = K                                                                  # on FRW the leaf average of K is K itself
fg = 0                                                                    # gate off: t = 0 (Lean CV1: f = 0 with every derivative)
lav = (sp.Integer(0) if not MUTATE else K ** 2)                           # (K - <K>)^2, or K^2 without the leaf average
sqrtg = Nl * a ** 3
# leaf-intrinsic aux terms on a homogeneous leaf: Delta_h of a homogeneous field = 0
aux = (2 * Pst * ((0 - m2s * (1 - fg)) * Yt - fg * 0) - 2 * sgs * m2s * (1 - fg) * Yt ** 2
       + 2 * Lt * (0 - 0))                                                # eps_d - <eps_d> = 0 on a homogeneous leaf
Lmini = (sqrtg * (-6 * Hc ** 2 - 2 * Lam_ - c2s * lav + aux)             # K_ij K^ij - K^2 = 3H^2 - 9H^2 = -6 H^2; a_mu = 0; D U = 0
         - 16 * sp.pi * G_ / c_ ** 4 * sqrtg * rho0 * c_ ** 2 / a ** 3)   # dust: -sqrt(-g) rho c^2, in units of c^3/(16 pi G)
eqN = sp.simplify(sp.diff(Lmini, Nl))                                     # the lapse (Hamiltonian) constraint
eqs_aux = [sp.simplify(sp.diff(Lmini, F_)) for F_ in (Yt, Pst, Lt)]
sol_aux = sp.solve(eqs_aux[:2], [Yt, Pst], dict=True)
eqN0 = sp.simplify(eqN.subs({Yt: 0, Pst: 0, Lt: 0}).subs(Nl, 1))
H2 = sp.symbols("H2", positive=True)
Hsol = sp.solve(sp.Eq(eqN0.subs(sp.diff(a, t) ** 2, H2 * a ** 2), 0), H2)
target = 8 * sp.pi * G_ * rho0 / (3 * a ** 3 * c_ ** 2) + Lam_ / 3      # (H/c)^2 = 8 pi G rho/(3 c^2) + Lambda/3
gcos_ratio = sp.simplify(Hsol[0] / target) if Hsol else None
aux_force = sp.simplify(sp.diff(sqrtg * aux, Nl).subs({Yt: 0, Pst: 0, Lt: 0}))
P(f"    auxiliary equations on FRW: {eqs_aux};  solution {sol_aux}  (Lam_d: its equation is 0 = 0, V a gauge constant)")
P(f"    auxiliary contribution to the lapse constraint at Y = Psi = Lam_d = 0: {aux_force}")
P(f"    Friedmann: (H/c)^2 = {sp.simplify(Hsol[0]) if Hsol else None};  ratio to 8 pi G rho/(3c^2) + Lambda/3: {gcos_ratio}")
OUT["numbers"]["B3"] = {"aux_solution": str(sol_aux), "aux_force": str(aux_force), "H2": str(Hsol), "ratio": str(gcos_ratio)}
check("B3 on FRW the gate is off, the auxiliaries vanish consistently and exert no force, alpha_c a^2 = 0 and the leaf "
      "average removes the c_2 term: the Friedmann equation is GR's, G_cos = G",
      f"aux solution {sol_aux}; aux force {aux_force}; H^2 ratio {gcos_ratio}",
      sol_aux == [{Yt: 0, Pst: 0}] and aux_force == 0 and gcos_ratio == 1,
      "L350 G5 from the action: the Planck-era bound on c_2 (<= 0.6-2.9e-3) no longer conflicts with L340's tracking floor "
      "7.3e-3 at the background level; perturbations with k != 0 still carry c_2 (the review's recheck item)")

# ============================================================================================ B4 the dark source on a closed leaf
banner("B4  THE DARK SOURCE ON A CLOSED LEAF: projected vs unprojected (spectral solve on a torus)")
NT = 64
xs = np.arange(NT) / NT
XX, YY, ZZ = np.meshgrid(xs, xs, xs, indexing="ij")
rho_pos = 1.0 + 0.8 * np.exp(-((XX - 0.4) ** 2 + (YY - 0.5) ** 2 + (ZZ - 0.6) ** 2) / 0.01)   # positive everywhere
kk = 2 * np.pi * np.fft.fftfreq(NT, d=1.0 / NT)
KX, KY, KZ = np.meshgrid(kk, kk, kk, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2
def solve_poisson(src):
    sh = np.fft.fftn(src)
    zero_mode = abs(sh[0, 0, 0]) / src.size
    with np.errstate(divide="ignore", invalid="ignore"):
        vh = np.where(K2 > 0, -sh / K2, 0.0)
    v_ = np.real(np.fft.ifftn(vh))
    lapv = np.real(np.fft.ifftn(-K2 * np.fft.fftn(v_)))
    return zero_mode, float(np.max(np.abs(lapv - src)) / np.max(np.abs(src)))
zm_p, res_p = solve_poisson(rho_pos - rho_pos.mean())
zm_u, res_u = solve_poisson(rho_pos)
P(f"    projected source eps - <eps>: zero mode {zm_p:.1e}, residual |lap V - src|/|src| = {res_p:.1e}")
P(f"    unprojected source eps > 0:    zero mode {zm_u:.2f} -> no periodic solution (residual {res_u:.2f})")
OUT["numbers"]["B4"] = {"projected": [zm_p, res_p], "unprojected": [zm_u, res_u]}
check("B4 the projected dark source is solvable on a closed leaf for a positive density and the unprojected one is not",
      f"projected residual {res_p:.1e}; unprojected zero mode {zm_u:.2f}, residual {res_u:.2f}",
      res_p < 1e-10 and zm_u > 0.5 and res_u > 0.1,
      "the mean belongs to the FRW background (the lead track's CD26-4 made the same point for the carrier coupling)")

banner("VERDICT")
P(f"""  V0 for the C-H/K branch, written as one covariant action on C-H's leaves: C-H's chassis, L340's BPS terms with L350's
  leaf average, the region kernel read through a leafwise field Y (L361, lifted, sigma declared), L353's pair with the
  projected dark source, and the gate f as a prescribed function of the leaf geometry.  Its static weak-field limit is
  CV1's Lagrangian exactly (B1), so reductions (i) and (ii) at prescribed f carry over from CV1; on a gate-on plateau it
  IS C-H/K, so L340's block and its health are recovered (B2, reduction (iii)); on FRW the gate and every auxiliary are
  off and the Friedmann equation is GR's (B3); the dark source is well posed on closed leaves only when projected (B4).
  Left for CV3: the gate varied as an action term.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
