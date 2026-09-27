#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP2 -- RELATIVISTIC CONSISTENCY OF THE C-H/K CORE: the full preferred-frame PPN with the heat-filter sector, moving-source
tracking, and the root tension between tracking and Planck-era cosmology.

ROOT (coordinator's redirect, 2026-09-26).  The AeST-type host is not re-derived here (generalized AeST dies on alpha_1:
closure_2026/GEN_AEST_PPN_VERDICT.md).  FP2 is rooted in the UNGATED C-H/K core: astra's C-H action
(closure_2026/g03_covariant_action_2026/ACTION.md, FULL_VARIATION.md) plus the Blas-Pujolas-Sibiryakov khronon terms of
g03_audit_2026/L340 with beta = 0, the leaf-average lambda-term of L350 G5 / chk_v0_2026 CV2, and the kernel nu_mono.
In units c = 1 (x0 = ct; alpha = a0/c^2; the source terms carry 16 pi G):

  I = (1/16 pi G) Int d^4x sqrt(-g) {  R - 2 Lambda
        + 2 h^{mn} (D_m U - a_m)(D_n U - a_n)                                   C-H chassis (U auxiliary, a_m = D_m ln N)
        + 2 alpha^2 q( h^{mn} D_m W_b D_n W_b / alpha^2 )                         C-H kernel on the filtered field, q' = nu_mono - 1
        + Int_0^b dz L (d_z W - Delta_h W) + lambda_0 (W_0 - U)                   C-H heat filter, b = xi^2/2
        + alpha_c a_m a^m - c_2 (K - <K>_h)^2   }                                 BPS khronon (beta = 0), leaf-averaged lambda-term
      + GHY caps + S_m[g, psi]                                                   matter minimally coupled to g only
  n_m = -d_m tau/sqrt(X) is the clock's unit normal, h = g + n n, K = nabla.n, <K>_h the proper-volume leaf average.

RE-DERIVED HERE: the quadratic action, c_T = 1 on flat space, gamma, alpha_1..3, tracking, health, the FRW equations.
INHERITED (cited, not re-derived): beta = 1 at 1PN for the khronometric sector (KM3, static O(m^2) equations); c_T = 1 on
FRW (L351 W5; A3's argument is leaf by leaf); the Solar-System xi floors 0.045/0.049 pc (canonical/alt, nu_mono, Saturn
monopole binding; L340 S1 -- the static-limit lane owns them); L341's ungated growth failure (sigma_8 18-27).

CHECKS
  A1 THE QUADRATIC ACTION, DERIVED: the full core in unitary gauge on flat space (ADM EH + chassis + kernel + khronon terms,
     symbolic second variation) gives Euler-Lagrange equations identical to L340's hand-typed block, term by term; the
     transverse shift is GR's; the C-H sector carries no time derivative and no shift (L330 M1 reproduced).
  A2 THE HEAT FILTER ELIMINATED EXACTLY: solving the z-equations of (W, L, lambda_0) gives W_b = S U, lambda_0 = -S dq/dW_b,
     S = e^{-b k^2}, so the U-equation gains 4 S^2 C k^2 U: the kernel acts with C_eff = S^2 C; and the constitutive
     coefficients follow from q' = nu - 1: C_T = nu - 1, C_L = nu - 1 + y nu'.
  A3 c_T = 1: the tensor sector of the full core is GR's (omega^2 = k^2, positive kinetic term); no C-H or khronon term
     reaches it at quadratic order.
  B1 CONTROL (GR): the moving-source pipeline is Lorentz invariant at O(v^0) and O(v^2).
  B2 CONTROL (literature): with the C-H sector off (C_eff = 0) the pipeline returns Yagi et al. 2014's khronometric
     alpha_1 = -4 alpha_c and alpha_2 = alpha_c (alpha_c - c_2 + 2 alpha_c c_2)/(c_2 (2 - alpha_c)) exactly.
  B3 THE FULL PPN OF THE CORE (with the C-H sector, heat filter included): gamma = 1 for every C_eff; alpha_3 = 0 (the O(v)
     g_0j and O(v^2) g_00 readings of alpha_1 agree); alpha_1 = -4 alpha_c - 8 C_eff/(1 + C_eff); alpha_2 in closed form,
     containing KM2's tracking amplification C_eff^2 (2 + 3 c_2)/(c_2 (1 + C_eff)).
  B4 THE NUMBERS where the bounds live (1 AU for LLR alpha_1; R_sun and a 10 km pulsar for alpha_2), nu_mono at the
     Galactic field on both footings, xi at the binding floor: the C-H parts are <= 1e-11; |alpha_1| < 1e-5 and
     |alpha_2| < 1.6e-9 then CONSTRAIN alpha_c <= 3.2e-9 (the khronometric part).
  B5 (reported) the preferred-frame coefficients in the MOND regime (xi k << 1): alpha_1 -> -8C/(1+C), alpha_2 ~ C^2/c_2.
  C1 TRACKING (the L330 gate): det M(0) != 0 iff c_2 != 0, and the omega -> 0 response is the static MOND solution;
     control c_2 = 0: det M(0) = 0 and the response is Newtonian (the frozen phantom).
  C2 THE TRACKING MODE, exact: c_s^2 = c_2 (2 - alpha_c (1+C))/((2 + 3c_2)(2C + alpha_c (1+C))); KM2's amplification law
     is the exact Bardeen-lapse ratio of this block.
  C3 HEALTH on the static MOND background: every (y, direction) cell of nu_mono has one mode with omega^2 > 0 and positive
     Krein energy; the nu_RAR control (C_L < 0) is a tachyon or ghost.
  C4 THE TRACKING FLOOR: c_s >= 3 x 600 km/s where C <= 100 needs c_2 >= 7.29e-3 (L340's number, re-derived).
  D1 FRW BACKGROUND from the action: the leaf-averaged term leaves Friedmann GR's (c_2 absent); the plain -c_2 K^2 gives
     H^2 (1 + 3 c_2/2) (L350 G1's G_cos, control).
  D2 THE ROOT TENSION, linear order: with the leaf average, c_2 enters the linear FRW equations ONLY through
     Q = (K - <K>)^(1) = (k^2/a^2 - 3 Hdot) pi - 3 H Phi - 3 Psidot; the dust equations are c_2-free; the khronon equation
     reads c_2 * 2a^3 (k^2/a^2 - 3Hdot) Q = 2 alpha_c k^2 d/dt[a (Phi - pidot)], so c_2 Q = O(alpha_c): linear cosmology is
     c_2-independent up to O(alpha_c).  Control: the plain -c_2 K^2 fails this in every equation.
  D3 THE NUMBERS: the quasi-static growth coupling is G_eff/G_cos = 1/(1 - alpha_c/2) with the leaf average (vs
     (1 + 3c_2/2)/(1 - alpha_c/2) plain); sigma_8 shifts by ~1e-9 (leaf) vs +4.1% at the tracking floor (plain).  The
     published Horava caps constrain an effect the leaf-averaged core does not have: the tracking window c_2 >= 7.29e-3
     is not excluded at linear order, and L340's BBN ceiling (0.067, also a G_cos effect) is gone.
  D4 (reported) what the leaf average does NOT fix: the UNGATED core's C-H sector at zero gradient has C = nu - 1 -> oo
     (no linear cosmology; L341's growth failure is c_2-independent), and the tracking speed there -> 0.
  W  the ledger.
MUTATE=1 replaces the leaf-averaged lambda-term by the plain -c_2 K^2 (L340's original term): D1, D2 and D3 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/derivation_chain_2026/FP2_relativistic_consistency.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP2_relativistic_consistency" + ("_MUTATE" if MUTATE else "")
OUT = {"lane": "FP2", "mutate": MUTATE, "root": "ungated C-H/K core (C-H + BPS khronon, beta = 0, leaf-averaged lambda-term, nu_mono)",
       "checks": {}, "numbers": {}, "ledger": []}
CH = []
T0 = time.time()


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 112 + "\n" + t + "\n" + "=" * 112)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


P(__doc__.split("CHECKS")[0].strip())
CORE_TERM = "plain" if MUTATE else "leaf"
if MUTATE:
    P("\n  *** MUTATE=1: the core's lambda-term is the PLAIN -c_2 K^2 (no leaf average): D1, D2, D3 must FAIL ***")

# ---------------------------------------------------------------------------------------------- inputs from the chain
cc, Gn, MSUN, PC, AU_M = 299792458.0, 6.67430e-11, 1.98892e30, 3.0856775814913673e16, 1.495978707e11
fp0 = os.path.join(HERE, "FP0_core_postulates_results.json")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
if os.path.exists(fp0):
    n0 = json.load(open(fp0))["numbers"]
    A0 = {"canonical": n0["a0_canonical"], "alt": n0["a0_rho_total"]}
l340 = os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion_results.json")
XI_FLOOR = {"canonical": 0.0451, "alt": 0.0489}
L340N = {}
if os.path.exists(l340):
    L340N = json.load(open(l340))["numbers"]
    s1 = L340N["S1"]
    XI_FLOOR = {f: max(s1[f"{f}/nu_mono"]["xi_Q2"], s1[f"{f}/nu_mono"]["xi_M"]) for f in ("canonical", "alt")}
GEXT = 2.32e-10          # the Galaxy's observed field at the Sun (L340 S1)
A1_BOUND, A2_BOUND = 1.0e-5, 1.6e-9
P(f"\n  inputs: a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2 (FP0); xi floors {XI_FLOOR['canonical']:.4f} / "
  f"{XI_FLOOR['alt']:.4f} pc (L340 S1, nu_mono, binding of Q2 and Saturn monopole); |alpha_1| < {A1_BOUND}, |alpha_2| < {A2_BOUND}")

# ---------------------------------------------------------------------------------------------- the kernel nu_mono (L340's definition)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)


Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])


def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 / (-np.expm1(-np.sqrt(y)))


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y


def CT_of(nuf, y):
    return nuf(y) - 1.0


def CL_of(nuf, y):
    y = np.asarray(y, float); e = 1e-5
    return ((y * (1 + e)) * nuf(y * (1 + e)) - (y * (1 - e)) * nuf(y * (1 - e))) / (2 * y * e) - 1.0


rep = L340N.get("A1", {})
kern_ok = abs(Y_P - rep.get("y_p", Y_P)) < 1e-6 and abs(H_P - rep.get("h_p", H_P)) < 1e-6
P(f"  nu_mono rebuilt: y_p = {Y_P:.4f}, h_p = {H_P:.4f} (L340 recorded {rep.get('y_p', float('nan')):.4f}, "
  f"{rep.get('h_p', float('nan')):.4f}); identical: {kern_ok}")

# ============================================================================================== A2 heat filter + constitutive
banner("A2  THE HEAT FILTER ELIMINATED EXACTLY, and the kernel's constitutive coefficients from q")
zz, bb, kk, Cq, Uv, lam0 = sp.symbols('z b k C U lambda_0', positive=True)
Wz, Lz = sp.Function('W')(zz), sp.Function('L')(zz)
# one real Fourier mode on a flat leaf (Delta_h -> -k^2); per-mode quadratic kernel 2 C k^2 W_b^2 (q'' terms are the C_L part)
bulkL = Lz * (sp.diff(Wz, zz) + kk**2 * Wz)
elz = {str(e_.lhs - e_.rhs) for e_ in euler_equations(bulkL, [Wz, Lz], zz)}
Wsol = sp.dsolve(sp.Eq(sp.diff(Wz, zz) + kk**2 * Wz, 0), Wz).rhs                  # from the L-equation
Lsol = sp.dsolve(sp.Eq(-sp.diff(Lz, zz) + kk**2 * Lz, 0), Lz).rhs                  # from the W-equation (bulk)
C1s, C2s = sorted(Wsol.free_symbols - {zz, kk}, key=str)[0], sorted(Lsol.free_symbols - {zz, kk}, key=str)[0]
Wsol = Wsol.subs(C1s, Uv)                                                           # lambda_0: W(0) = U
Wb = Wsol.subs(zz, bb)
kern = 2 * Cq * kk**2 * Wb**2
# boundary terms of the z-integration by parts: +L(b) dW(b) - L(0) dW(0); W(b): L(b) + d kern/dW_b = 0; W(0): -L(0) + lambda_0 = 0
Lb_val = -sp.diff(2 * Cq * kk**2 * sp.Symbol('Wb')**2, sp.Symbol('Wb')).subs(sp.Symbol('Wb'), Wb)
C2val = sp.solve(sp.Eq(Lsol.subs(zz, bb), Lb_val), C2s)[0]
Lsol = Lsol.subs(C2s, C2val)
lam0_val = sp.simplify(Lsol.subs(zz, 0))
res_bulk = [sp.simplify(sp.diff(Wsol, zz) + kk**2 * Wsol), sp.simplify(-sp.diff(Lsol, zz) + kk**2 * Lsol)]
# reduced action for U: heat-pair terms on shell + kernel
heat_on_shell = sp.simplify(sp.integrate((Lsol * (sp.diff(Wsol, zz) + kk**2 * Wsol)), (zz, 0, bb)))
reduced = sp.simplify(heat_on_shell + kern)
target = 2 * Cq * kk**2 * sp.exp(-2 * bb * kk**2) * Uv**2
# the force on U: dI/dU from lambda_0 (W_0 - U) is -lambda_0; compare with d(reduced)/dU
forceU = sp.simplify(-lam0_val - sp.diff(reduced, Uv))
P(f"    W(z) = {Wsol};  L(z) = {sp.simplify(Lsol)};  lambda_0 = {lam0_val}")
P(f"    bulk residuals {res_bulk};  heat terms on shell = {heat_on_shell};  reduced U-action - 2 C k^2 e^(-2bk^2) U^2 = "
  f"{sp.simplify(reduced - target)};  -lambda_0 - dI_red/dU = {forceU}")
# constitutive coefficients from q' = nu - 1 (generic nu), Hessian of 2 q(|p|^2) at p = (0, 0, s)
s_, p1, p2, p3 = sp.symbols('s p1 p2 p3', positive=True)
nuF = sp.Function('nu')
Yq = sp.Symbol('Y', positive=True)
qp = lambda Y_: nuF(sp.sqrt(Y_)) - 1                                                # q'(Y)
pp = sp.Matrix([p1, p2, p3])
# second-order expansion of q(|p|^2) around p_bg = (0, 0, s): Hessian = 2 q' delta + 4 q'' p p
qpp = sp.diff(qp(Yq), Yq)
Hq = sp.Matrix(3, 3, lambda i, j: (2 * qp(Yq) * (1 if i == j else 0) + 4 * qpp * [0, 0, s_][i] * [0, 0, s_][j])).subs(Yq, s_**2)
CTsym = sp.simplify(Hq[0, 0] / 2); CLsym = sp.simplify(Hq[2, 2] / 2)
CL_target = nuF(s_) - 1 + s_ * sp.diff(nuF(s_), s_)
ok_a2 = (all(r_ == 0 for r_ in res_bulk) and heat_on_shell == 0 and sp.simplify(reduced - target) == 0 and forceU == 0
         and sp.simplify(CTsym - (nuF(s_) - 1)) == 0 and sp.simplify(CLsym - CL_target) == 0 and kern_ok)
P(f"    C_T = {CTsym};  C_L = {sp.simplify(CLsym)}")
check("A2 the heat-filter pair is eliminated exactly: W_b = e^{-bk^2} U, lambda_0 = -e^{-bk^2} dq/dW_b, the heat terms vanish "
      "on shell, and the U-equation carries the kernel with C_eff = e^{-2bk^2} C = e^{-xi^2 k^2} C; from q' = nu - 1 the "
      "constitutive coefficients are C_T = nu - 1 and C_L = nu - 1 + y nu' (nu_mono rebuilt = L340's)",
      f"reduced action - target = {sp.simplify(reduced - target)}; force mismatch {forceU}; C_T {CTsym}; C_L - target "
      f"{sp.simplify(CLsym - CL_target)}", ok_a2,
      "C-H's filter is a leafwise elliptic constraint: in the linear theory it only rescales the constitutive tensor by "
      "e^{-xi^2 k_perp^2}, k_perp the wavenumber on the clock's leaves")

# ============================================================================================== A1 the quadratic action
banner("A1  THE QUADRATIC ACTION OF THE CORE, DERIVED (unitary gauge tau = t, flat background, symbolic second variation)")
t, x, y, z = sp.symbols('t x y z', real=True)
X3 = (x, y, z)
eb = sp.Symbol('e_b')
al, c2, Ce = sp.symbols('alpha_c c_2 C_eff', real=True)
nf, pf, Bf, Sf, Uf = [sp.Function(s)(t, x, y, z) for s in ('n', 'psi', 'B', 'S', 'U')]
Nl = sp.exp(eb * nf)
gam = sp.diag(*[sp.exp(-2 * eb * pf)] * 3)
gin = gam.inv()
Ni = [eb * (sp.diff(Bf, X3[0]) + Sf), eb * sp.diff(Bf, X3[1]), eb * sp.diff(Bf, X3[2])]
Gm3 = [[[sum(gin[a, d] * (sp.diff(gam[d, b], X3[c]) + sp.diff(gam[d, c], X3[b]) - sp.diff(gam[b, c], X3[d])) for d in range(3)) / 2
         for c in range(3)] for b in range(3)] for a in range(3)]
DN = [[sp.diff(Ni[j], X3[i]) - sum(Gm3[kq][i][j] * Ni[kq] for kq in range(3)) for j in range(3)] for i in range(3)]
Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(gam[i, j], t) - DN[i][j] - DN[j][i]) / (2 * Nl))
Kup = gin * Kij * gin
KK = sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3))
trK = sum(gin[i, j] * Kij[i, j] for i in range(3) for j in range(3))


def Ric3(b_, c_):
    return sum(sp.diff(Gm3[a][b_][c_], X3[a]) - sp.diff(Gm3[a][b_][a], X3[c_]) +
               sum(Gm3[a][a][d] * Gm3[d][b_][c_] - Gm3[a][c_][d] * Gm3[d][b_][a] for d in range(3)) for a in range(3))


R3 = sum(gin[b_, c_] * Ric3(b_, c_) for b_ in range(3) for c_ in range(3))
ai = [sp.diff(sp.log(Nl), xi_) for xi_ in X3]                      # a_i = D_i ln N
aa = sum(gin[i, j] * ai[i] * ai[j] for i in range(3) for j in range(3))
Ui = [sp.diff(eb * Uf, xi_) for xi_ in X3]
chassis = 2 * sum(gin[i, j] * (Ui[i] - ai[i]) * (Ui[j] - ai[j]) for i in range(3) for j in range(3))
kernel2 = 2 * Ce * sum(gin[i, j] * Ui[i] * Ui[j] for i in range(3) for j in range(3))   # A2: the filtered kernel's quadratic form
# on flat space K_bar = 0 and <K^(1)> = 0 for k != 0: the leaf-averaged and plain lambda-terms coincide at quadratic order here
Lfull = Nl * sp.exp(-3 * eb * pf) * (KK - trK**2 + R3 + al * aa - c2 * trK**2 + chassis + kernel2)
L2f = sp.expand((sp.diff(Lfull, eb, 2) / 2).subs(eb, 0))
ELf = euler_equations(L2f, [nf, pf, Bf, Sf, Uf], [t, x, y, z])
kq_, wq_ = sp.symbols('k omega', real=True)
An, Ap, AB, AS, AU = sp.symbols('A_n A_psi A_B A_S A_U')
phs = sp.exp(sp.I * (kq_ * z - wq_ * t))
fsub = {nf: An * phs, pf: Ap * phs, Bf: AB * phs, Sf: AS * phs, Uf: AU * phs}
ELk = [sp.expand(sp.simplify((e_.lhs - e_.rhs).subs(fsub).doit() / phs)) for e_ in ELf]
names5 = ["n", "psi", "B", "S", "U"]
for nm, e_ in zip(names5, ELk):
    P(f"    dL/d{nm:4s}: {sp.factor(e_)}")
D_ = -sp.I * wq_
eps_ = -c2
E340 = {"n": -4 * kq_**2 * Ap - 4 * kq_**2 * (AU - An) + 2 * al * kq_**2 * An,
        "psi": 4 * kq_**2 * Ap - 4 * kq_**2 * An - D_ * (-12 * D_ * Ap + 4 * kq_**2 * AB + 6 * eps_ * (3 * D_ * Ap - kq_**2 * AB)),
        "B": 4 * kq_**2 * D_ * Ap - 2 * eps_ * kq_**2 * (3 * D_ * Ap - kq_**2 * AB),
        "U": 4 * kq_**2 * (AU - An) + 4 * kq_**2 * Ce * AU}
diffs = {nm: sp.simplify(sp.expand(ELk[names5.index(nm)] - E340[nm])) for nm in ("n", "psi", "B", "U")}
shift_T = sp.simplify(ELk[3] - AS * kq_**2)
U_free = (not ELk[4].has(wq_)) and (not ELk[4].has(AB)) and (not ELk[4].has(AS))
check("A1 the symbolically derived quadratic action of the full core gives L340's block EXACTLY (lapse, trace, longitudinal "
      "shift, U), the transverse shift is GR's (k^2 S = source), and U's equation has no time derivative and no shift "
      "(L330 M1: the C-H sector is instantaneous and momentum-free on its own)",
      f"residuals vs L340: {diffs}; transverse shift - k^2 S = {shift_T}; U equation free of omega and shift: {U_free}; "
      f"{time.time() - T0:.1f} s", all(v_ == 0 for v_ in diffs.values()) and shift_T == 0 and U_free,
      "L340 typed its block from astra's ADM principal block; here it is varied out of the action, chassis and filter included")

# ============================================================================================== A3 tensor sector
banner("A3  c_T = 1: the tensor sector of the full core")
hp_, hx_ = [sp.Function(s)(t, z) for s in ('h_p', 'h_x')]
gamT = sp.Matrix([[1 + eb * hp_, eb * hx_, 0], [eb * hx_, 1 - eb * hp_, 0], [0, 0, 1]])
ginT = gamT.inv()
GmT = [[[sum(ginT[a, d] * (sp.diff(gamT[d, b], X3[c]) + sp.diff(gamT[d, c], X3[b]) - sp.diff(gamT[b, c], X3[d])) for d in range(3)) / 2
         for c in range(3)] for b in range(3)] for a in range(3)]
KijT = sp.Matrix(3, 3, lambda i, j: sp.diff(gamT[i, j], t) / 2)                    # N = 1, shift 0 for the TT block
KupT = ginT * KijT * ginT
KKT = sum(KijT[i, j] * KupT[i, j] for i in range(3) for j in range(3))
trKT = sum(ginT[i, j] * KijT[i, j] for i in range(3) for j in range(3))


def Ric3T(b_, c_):
    return sum(sp.diff(GmT[a][b_][c_], X3[a]) - sp.diff(GmT[a][b_][a], X3[c_]) +
               sum(GmT[a][a][d] * GmT[d][b_][c_] - GmT[a][c_][d] * GmT[d][b_][a] for d in range(3)) for a in range(3))


R3T = sum(ginT[b_, c_] * Ric3T(b_, c_) for b_ in range(3) for c_ in range(3))
sqT = sp.sqrt(gamT.det())
# U = 0, n = 0 in the TT block: chassis and kernel vanish identically; alpha_c a^2 = 0 (a_i = 0); the lambda-term sees tr K
LT = sp.expand((sp.diff(sqT * (KKT - trKT**2 + R3T - c2 * trKT**2), eb, 2) / 2).subs(eb, 0))
ELT = euler_equations(LT, [hp_, hx_], [t, z])
AT = sp.Symbol('A_T')
ELTk = [sp.factor(sp.simplify((e_.lhs - e_.rhs).subs({hp_: AT * sp.exp(sp.I * (kq_ * z - wq_ * t)), hx_: 0}).doit()
                                / sp.exp(sp.I * (kq_ * z - wq_ * t)))) for e_ in ELT[:1]]
wsol = sp.solve(ELTk[0].subs(AT, 1), wq_)
kin = sp.expand(LT).coeff(sp.Derivative(hp_, t)**2)
P(f"    TT Euler-Lagrange (h_+ = A e^(i(kz - wt))): {ELTk[0]};  omega roots {wsol};  coefficient of (d_t h_+)^2 in L: {kin}")
ok_a3 = set(wsol) == {kq_, -kq_} and sp.simplify(kin - sp.Rational(1, 2)) == 0 and not LT.has(c2) and not LT.has(al)
check("A3 c_T = 1 EXACTLY: the tensor modes obey omega^2 = k^2 with GR's positive kinetic term (1/2)(d_t h_+)^2 (gamma_xx = 1 + h_+); c_2, alpha_c "
      "and the C-H sector are absent from the tensor sector at quadratic order (tr K is blind to TT modes; a_i and U are scalar)",
      f"roots {wsol}; kinetic coefficient {kin}; c_2 in L_TT: {LT.has(c2)}", ok_a3,
      "GW170817 is met by construction on flat space (and on FRW, where the same argument holds leaf by leaf; L351 W5)")

# ============================================================================================== B the full PPN
banner("B   THE FULL PREFERRED-FRAME PPN OF THE CORE (moving source in the khronon frame, exact in v, boosted to rest)")
kB, wB, vB, GA, muB = sp.symbols('k omega v G_ae mu', real=True)
dl = sp.Symbol('dlnC', real=True)
ELB = [e_.subs({kq_: kB, wq_: wB}) for e_ in ELk]
Pf = 1 / (16 * sp.pi * GA)
gmB = 1 / sp.sqrt(1 - vB**2)
kpB = sp.symbols('kp', positive=True)
BOOST = {kB: kpB * sp.sqrt(1 + (gmB**2 - 1) * muB**2), wB: gmB * kpB * muB * vB}
MB = sp.symbols('M', positive=True)


def ms_solve(rho, sub):
    """a source moving at v through the khronon frame: rho carries momentum rho v and stress rho v^2; U is sourced only
    through the metric (the phantom is the C-H sector's own response, not an inserted source)."""
    J_long, Pi = rho * wB, rho * vB**2
    eqs = [sp.Eq(Pf * ELB[0].subs(sub), rho), sp.Eq(Pf * ELB[1].subs(sub), Pi), sp.Eq(Pf * ELB[2].subs(sub), sp.I * J_long),
           sp.Eq(ELB[4].subs(sub), 0)]
    s_ = sp.solve(eqs, [An, Ap, AB, AU], dict=True)
    return s_[0] if s_ else None


S_PER_J = sp.solve(sp.Eq(Pf * ELB[3] + 1, 0), AS)[0]


def h00_rest(sol, rho):
    PhiB = sol[An] - sp.I * wB * sol[AB]
    S_dot_v = S_PER_J * rho * (vB**2 - wB**2 / kB**2)
    h = gmB**2 * (-2 * PhiB - 2 * vB**2 * sol[Ap] + 2 * S_dot_v)
    return gmB * h.subs(BOOST)


def v2_parts(expr):
    s_ = sp.expand(sp.series(expr, vB, 0, 3).removeO())
    return sp.simplify(s_.coeff(vB, 0)), sp.factor(sp.simplify(s_.coeff(vB, 2).subs(muB, 0))), sp.factor(sp.simplify(s_.coeff(vB, 2).coeff(muB, 2)))


# B1 GR control
solGR = sp.solve([sp.Eq(Pf * ELB[0].subs({al: 0, Ce: 0}), gmB * MB), sp.Eq(Pf * ELB[1].subs({al: 0, Ce: 0}), gmB * MB * vB**2),
                  sp.Eq(Pf * ELB[2].subs({al: 0, Ce: 0}), sp.I * gmB * MB * wB), sp.Eq(ELB[4].subs({al: 0, Ce: 0}), 0)],
                 [An, Ap, AB, AU], dict=True)[0]
hGR = sp.simplify(h00_rest(solGR, gmB * MB) / (8 * sp.pi * GA * MB / kpB**2))
hGR = sp.limit(hGR, c2, 0)
o0g, isog, anig = v2_parts(hGR)
check("B1 CONTROL (GR limit alpha_c = c_2 = C = 0): the rest-frame h'_00 of the moving source equals the static 8 pi G M/k^2 "
      "at O(v^0) and O(v^2): the boost/Jacobian/contraction pipeline is Lorentz invariant",
      f"O(1) {o0g}; O(v^2) isotropic {isog}, anisotropic {anig}", o0g == 1 and isog == 0 and anig == 0)

# B2/B3 the full core
solF = ms_solve(gmB * MB, {})
hF = h00_rest(solF, gmB * MB)
hF = hF.subs(Ce, Ce * (1 + dl * (gmB**2 - 1) * muB**2))            # C_eff lives on the khronon leaves: |k|^2 = kp^2 (1 + (g^2-1) mu^2)
h0F = sp.simplify(hF.subs(vB, 0))
ratioF = sp.simplify(hF / h0F)
o0F, AisoF, CaniF = v2_parts(ratioF)
alpha2_full = sp.factor(CaniF)
alpha1_h00 = sp.factor(-2 * AisoF)
yagi2 = al * (al - c2 + 2 * al * c2) / (c2 * (2 - al))
b2_ok = sp.simplify(alpha2_full.subs(Ce, 0) - yagi2) == 0 and sp.simplify(alpha1_h00.subs(Ce, 0) + 4 * al) == 0 and o0F == 1
check("B2 CONTROL (literature): with the C-H sector off the same pipeline returns Yagi, Blas, Barausse & Yunes 2014's "
      "khronometric alpha_1 = -4 alpha_c and alpha_2 = alpha_c (alpha_c - c_2 + 2 alpha_c c_2)/(c_2 (2 - alpha_c)) EXACTLY",
      f"alpha_2(C=0) - Yagi = {sp.simplify(alpha2_full.subs(Ce, 0) - yagi2)}; alpha_1(C=0) + 4 alpha_c = "
      f"{sp.simplify(alpha1_h00.subs(Ce, 0) + 4 * al)}", b2_ok)
# alpha_1 independently from the transverse g'_0j at O(v): h'_0j^T = v^T (-2 n - 2 psi) + S^T, static
sol0 = ms_solve(MB, {vB: 0})
s0 = {kk_: sp.simplify(vv_.subs({vB: 0, wB: 0})) for kk_, vv_ in sol0.items()}
U_obs = sp.simplify(-s0[An])                                          # h_00 = -2 n = 2 U
h0jT_per_v = sp.simplify(-2 * s0[An] - 2 * s0[Ap] + S_PER_J * MB)
alpha1_g0j = sp.factor(sp.simplify(-2 * h0jT_per_v / U_obs))
gamma_ppn = sp.simplify(s0[Ap] / s0[An])
alpha3 = sp.factor(sp.simplify(alpha1_h00 - alpha1_g0j))
alpha1_closed = -4 * al - 8 * Ce / (1 + Ce)
alpha2_lead = sp.factor(sp.limit(alpha2_full, al, 0))
amp_term = Ce**2 * (2 + 3 * c2) / (c2 * (1 + Ce))
P(f"    static: U = -n = {sp.factor(U_obs)};  gamma = psi/n = {gamma_ppn}")
P(f"    alpha_1 (g_00, O(v^2)) = {alpha1_h00};  alpha_1 (g_0j, O(v)) = {alpha1_g0j};  alpha_3 = difference = {alpha3}")
P(f"    alpha_2 = {alpha2_full}")
P(f"    alpha_2 at alpha_c -> 0: {alpha2_lead}  [= C^2 (2+3c_2)/(c_2 (1+C)) + C (dlnC - 1)/(1+C)]")
b3_ok = (gamma_ppn == 1 and alpha3 == 0 and sp.simplify(alpha1_h00 - alpha1_closed) == 0
         and sp.simplify(alpha2_lead - (amp_term + Ce * (dl - 1) / (1 + Ce))) == 0)
OUT["numbers"]["B3"] = {"alpha_1": str(alpha1_h00), "alpha_2": str(alpha2_full), "alpha_2_alpha_c_to_0": str(alpha2_lead),
                        "gamma": str(gamma_ppn), "alpha_3": str(alpha3)}
check("B3 THE FULL PPN OF THE CORE, derived with the C-H sector and its filter live (C_eff = e^{-xi^2 k^2} C): gamma = 1 for "
      "every C_eff; alpha_3 = 0 (the O(v) g_0j and O(v^2) g_00 readings of alpha_1 agree); alpha_1 = -4 alpha_c - 8 C_eff/(1 + "
      "C_eff) EXACTLY; alpha_2 -> C_eff^2 (2+3c_2)/(c_2(1+C_eff)) + C_eff (dlnC - 1)/(1+C_eff) as alpha_c -> 0",
      f"gamma {gamma_ppn}; alpha_3 {alpha3}; alpha_1 - closed form {sp.simplify(alpha1_h00 - alpha1_closed)}; alpha_2 lead - "
      f"form {sp.simplify(alpha2_lead - (amp_term + Ce * (dl - 1) / (1 + Ce)))}", b3_ok,
      "-8 C_eff/(1 + C_eff) is the phantom's missing transverse momentum (the c_2 channel is longitudinal); the C_eff^2/c_2 "
      "term is KM2's tracking amplification; both scale with the filtered constitutive coefficient")

# B4 numbers where the bounds live
banner("B4  THE NUMBERS AT THE SCALES OF THE BOUNDS (both footings; xi at the binding floor; nu_mono at the Galactic field)")
F1 = lambda r, xi: math.erf(r / (2 * xi)) - (r / (xi * math.sqrt(math.pi))) * math.exp(-r * r / (4 * xi * xi)) \
    if r / xi > 1e-3 else (r / xi)**3 / (6 * math.sqrt(math.pi))                                   # gradient ratio, e^{-xi^2 k^2}
F2 = lambda r, xi: (r / xi)**3 * math.exp(-r * r / (4 * xi * xi)) / (4 * math.sqrt(math.pi))       # xi^2 k^2 e^{-xi^2 k^2}
F4 = lambda r, xi: F1(r, math.sqrt(2) * xi)                                                        # e^{-2 xi^2 k^2}
C2_REF = [7.29e-3, 0.067, 1.0]
AC_MAX = 3.2e-9
B4 = {}
worst1 = worst2 = 0.0
for foot, a0 in A0.items():
    ye = brentq(lambda e_: float(nu_mono(e_)) * e_ - GEXT / a0, 1e-9, GEXT / a0 * 1.5, xtol=1e-14)
    Cs = max(float(CT_of(nu_mono, ye)), float(CL_of(nu_mono, ye)))
    xi = XI_FLOOR[foot] * PC
    for lab, r in (("1 AU (LLR alpha_1)", AU_M), ("R_sun (solar-spin alpha_2)", 6.957e8), ("10 km (pulsar alpha_2)", 1.0e4)):
        a1ch = 8 * Cs * F1(r, xi)
        for c2v in C2_REF:
            a2ch = Cs**2 * (2 + 3 * c2v) / c2v * F4(r, xi) + Cs * (F1(r, xi) + F2(r, xi))
            worst1, worst2 = max(worst1, a1ch), max(worst2, a2ch)
            B4[f"{foot}|{lab}|c2={c2v}"] = {"y_e": ye, "C": Cs, "alpha1_CH": a1ch, "alpha2_CH": a2ch}
        P(f"    {foot:9s} y_e = {ye:.3f}, C = {Cs:.3f}, xi = {XI_FLOOR[foot]:.4f} pc;  {lab:26s}: |alpha_1^CH| = {a1ch:.2e};  "
          f"|alpha_2^CH| (c_2 = {C2_REF[0]}) = {Cs**2*(2+3*C2_REF[0])/C2_REF[0]*F4(r, xi) + Cs*(F1(r, xi)+F2(r, xi)):.2e}")
# the khronometric part and the constraint on alpha_c
a1k = 4 * AC_MAX
a2k = [abs(float(yagi2.subs({al: AC_MAX, c2: c2v}))) for c2v in C2_REF]
ac_bound = min(A1_BOUND / 4, min(brentq(lambda a_: abs(float(yagi2.subs({al: a_, c2: c2v}))) - A2_BOUND, 1e-15, 1e-6) for c2v in C2_REF))
P(f"    khronometric part at alpha_c = {AC_MAX:.1e}: |alpha_1| = {a1k:.2e}; |alpha_2| = " + ", ".join(f"{v_:.2e}" for v_ in a2k)
  + f" (c_2 = {C2_REF});  the bounds require alpha_c <= {ac_bound:.2e}")
OUT["numbers"]["B4"] = {"cells": B4, "worst_alpha1_CH": worst1, "worst_alpha2_CH": worst2, "alpha_c_bound": ac_bound}
check("B4 at the scales where the bounds live the C-H sector's preferred-frame leakage is <= 1e-11 (the Gaussian filter leaves "
      "a harmonic core ~ (r/xi)^3 inside xi), so |alpha_1| < 1e-5 and |alpha_2| < 1.6e-9 are the khronometric ones and "
      "CONSTRAIN alpha_c <= 3.2e-9 (L340's window edge, re-derived with the C-H sector live)",
      f"worst |alpha_1^CH| {worst1:.1e}, worst |alpha_2^CH| {worst2:.1e} (both footings, c_2 {C2_REF}); alpha_c bound {ac_bound:.2e}",
      worst1 < 1e-11 and worst2 < 1e-11 and 3.0e-9 < ac_bound < 3.3e-9,
      "alpha_c is not derived: it is a free coupling the PPN bounds cap.  Leakage uses isotropic C = max(C_T, C_L) at the "
      "Galactic field and drops O(background gradient/k) ~ 1e-16 terms; real-space (r/xi)^3 cores of the three kernel "
      "shapes (e^{-xi^2k^2}, xi^2k^2 e^{-xi^2k^2}, e^{-2xi^2k^2}) convert the k-space closed forms")
# B5 MOND regime (reported)
rowsB5 = []
for Cv in (0.5, 1.0, 10.0, 100.0):
    for c2v in (7.29e-3, 1.0):
        a1v = float(alpha1_closed.subs({al: 0, Ce: Cv}))
        a2v = float(alpha2_lead.subs({Ce: Cv, c2: c2v, dl: 0}))
        rowsB5.append((Cv, c2v, a1v, a2v))
P("    MOND regime (xi k << 1, dlnC = 0):  " + "; ".join(f"C={r_[0]:g}, c2={r_[1]:g}: a1 {r_[2]:+.2f}, a2 {r_[3]:+.3g}" for r_ in rowsB5))
v620 = 620e3 / cc
amp620 = {(r_[0], r_[1]): r_[3] * v620**2 for r_ in rowsB5}
P(f"    sizes at 620 km/s: gravitomagnetic lensing correction ~ |alpha_1| v_los/4 <= {8 * v620 / 4:.1e}; the alpha_2 term is "
  f"KM2's amplification alpha_2 v_par^2: " + "; ".join(f"C={k_[0]:g}, c2={k_[1]:g}: {v_:.1e}" for k_, v_ in amp620.items()))
OUT["numbers"]["B5"] = {"rows": rowsB5, "alpha2_v620sq": {f"C={k_[0]:g},c2={k_[1]:g}": v_ for k_, v_ in amp620.items()}}
check("B5 (reported, a prediction) in the MOND regime the phantom's preferred-frame imprint is O(1) in alpha_1 (-8C/(1+C): no "
      "transverse momentum; <= 0.4% on lensing at 620 km/s) and C^2(2+3c_2)/(c_2(1+C)) in alpha_2 (KM2's amplification): "
      "~12% in C ~ 100 outskirts at the tracking floor c_2 = 7.29e-3 and v_par = 620 km/s, 0.2% at c_2 = 1 -- with the "
      "cosmological cap gone (D), raising c_2 is how the action suppresses it",
      "; ".join(f"C={k_[0]:g},c2={k_[1]:g}: {v_:.1e}" for k_, v_ in amp620.items()), True, load_bearing=False)

# ============================================================================================== C tracking and health
banner("C   TRACKING (the L330 gate) AND HEALTH, from the derived block")
wT, kT = sp.symbols('omega k', positive=True)
Rs = sp.Symbol('R')
ELC = {nm: e_.subs({kq_: kT, wq_: wT}) for nm, e_ in zip(names5, ELk)}
XC = [Ap, An, AB, AU]; rowsC = ['psi', 'n', 'B', 'U']
MC = sp.Matrix([[sp.expand(sp.diff(ELC[r_], x_)) for x_ in XC] for r_ in rowsC])
herm = all(sp.expand(MC[i, j] - sp.conjugate(MC[j, i]).subs({sp.conjugate(al): al, sp.conjugate(c2): c2, sp.conjugate(Ce): Ce})) == 0
           for i in range(4) for j in range(4))
SC = sp.Matrix([0, Rs, sp.I * wT * Rs, 0])                            # conserved source: lapse R, momentum constraint -D R
detC = sp.factor(sp.expand(MC.det(method='berkowitz')))


def cramer(Mx, Sx, i):
    Mi = Mx.copy(); Mi[:, i] = Sx
    return sp.cancel(sp.expand(Mi.det(method='berkowitz')) / sp.expand(Mx.det(method='berkowitz')))


solC = [cramer(MC, SC, i) for i in range(4)]
psiN = -Rs / (4 * kT**2)


def lim0(expr):
    num, den = sp.fraction(sp.cancel(expr))
    return sp.factor(sp.cancel(num.subs(wT, 0) / den.subs(wT, 0)))


limsC = [lim0(v_ / psiN) for v_ in solC]
static = sp.factor((1 + Ce) / (1 - al * (1 + Ce) / 2))
det0 = sp.factor(detC.subs(wT, 0))
M0 = MC.subs(c2, 0)
det0c = sp.factor(sp.expand(M0.det(method='berkowitz')).subs(wT, 0))
num0, den0 = sp.fraction(sp.cancel(cramer(M0, SC, 0) / psiN))
ctrl_resp = sp.factor(sp.Poly(num0, wT).TC() / sp.Poly(den0, wT).TC())
P(f"    M Hermitian: {herm};  det M = {detC}")
P(f"    omega -> 0: psi, n, B, U / psi_N = {limsC};  static MOND (1+C)/(1 - alpha_c (1+C)/2) = {static};  det M(0) = {det0}")
P(f"    control c_2 = 0: det M(0) = {det0c};  omega -> 0+ response psi/psi_N = {ctrl_resp} (Newtonian: frozen phantom)")
c1_ok = (herm and sp.simplify(limsC[0] - static) == 0 and sp.simplify(limsC[1] - static) == 0 and limsC[2] == 0
         and det0 != 0 and det0.has(c2) and det0c == 0 and ctrl_resp == 1)
check("C1 TRACKING: with the c_2 channel the omega -> 0 response of every field is the static MOND solution and det M(0) is "
      "proportional to c_2 (no frozen mode); without it det M(0) = 0 and the response is Newtonian (L330's frozen phantom)",
      f"psi -> {limsC[0]} psi_N; det M(0) = {det0}; control det 0, response {ctrl_resp}", c1_ok)
u = sp.Symbol('u', positive=True); U2 = sp.Symbol('U2', positive=True)
roots = sp.solve(sp.numer(sp.together(detC.subs(wT, sp.sqrt(U2) * kT))), U2)
cs2_exact = sp.factor(roots[0]) if len(roots) == 1 else None
cs2_km2 = c2 / (Ce * (2 + 3 * c2))
km2 = 1 - 3 * u**2 / (Ce + 1) + Ce / (Ce + 1) * u**2 / (cs2_km2 - u**2)
PhiBC = solC[1] - sp.I * wT * solC[2]
ratC = sp.cancel(PhiBC.subs(wT, u * kT) / PhiBC.subs(wT, 0))
km2_diff = sp.simplify(sp.cancel(ratC.subs(al, 0) - km2))
cs2_lim = sp.simplify(cs2_exact.subs(al, 0) - cs2_km2) if cs2_exact is not None else None
P(f"    the one mode: omega^2/k^2 = {cs2_exact};  at alpha_c = 0 minus c_2/(C(2+3c_2)): {cs2_lim}")
P(f"    Bardeen-lapse ratio Phi_B(u)/Phi_B(0) at alpha_c = 0 minus KM2's law: {km2_diff}")
check("C2 THE TRACKING MODE, exact: c_s^2 = c_2 (2 - alpha_c(1+C))/((2+3c_2)(2C + alpha_c(1+C))) -> c_2/(C(2+3c_2)); KM2's "
      "amplification law R = 1 - 3u^2/(C+1) + [C/(C+1)] u^2/(c_s^2 - u^2) is the exact Bardeen-lapse ratio of this block",
      f"c_s^2 = {cs2_exact}; limit residual {cs2_lim}; KM2 residual {km2_diff}", cs2_exact is not None and cs2_lim == 0 and km2_diff == 0)
# C3 health (Krein) on the static MOND background: C_T and C_L of the kernel at each y
Mf = sp.lambdify((wT, kT, Ce, c2, al), MC, "numpy")
cs2f = sp.lambdify((Ce, c2, al), cs2_exact, "numpy")


def mode_health(Cv, c2v, acv):
    W2 = float(cs2f(Cv, c2v, acv))
    if not np.isfinite(W2) or W2 <= 0:
        return "TACHYON"
    w0 = math.sqrt(W2)
    Mn = lambda ww: np.array(Mf(ww, 1.0, Cv, c2v, acv), dtype=complex)
    ev, vec = np.linalg.eigh(Mn(w0)); vv = vec[:, np.argmin(abs(ev))]; hh = 1e-6 * max(1.0, w0)
    s_ = float(np.real(np.conj(vv) @ ((Mn(w0 + hh) - Mn(w0 - hh)) / (2 * hh)) @ vv))
    return "ok" if s_ > 0 else "GHOST"


ysH = np.logspace(-3, 4, 57)
bad = []
for yv in ysH:
    for lab, Cv in (("T", float(CT_of(nu_mono, yv))), ("L", float(CL_of(nu_mono, yv)))):
        for c2v in (7.29e-3, 1.0):
            hs = mode_health(Cv, c2v, 1e-9)
            if hs != "ok":
                bad.append((round(float(yv), 4), lab, c2v, hs))
mink = [mode_health(0.0, c2v, 1e-9) for c2v in (7.29e-3, 1.0)]          # C = 0: Minkowski with no MOND background
if any(m_ != "ok" for m_ in mink):
    bad.append(("Minkowski", "C=0", mink))
ctrl_h = mode_health(float(CL_of(nu_rar, 10.0)), 7.29e-3, 1e-9)
P(f"    nu_mono, alpha_c = 1e-9, c_2 = 7.29e-3 and 1: unhealthy (y, direction, c_2) cells {len(bad)} {bad[:4]};  Minkowski (C = 0): "
  f"{mink};  control nu_RAR C_L(y=10) = {float(CL_of(nu_rar, 10.0)):+.4f}: {ctrl_h}")
check("C3 HEALTH on Minkowski (C = 0) and on the static MOND background (frozen coefficients, both constitutive directions, "
      "y = 1e-3..1e4): every cell has one scalar mode with omega^2 > 0 and positive Krein energy (tensor: A3; vector: a "
      "constraint, A1); the non-monotone control (nu_RAR's C_L < 0) is a tachyon or a ghost",
      f"{len(bad)} unhealthy cells of {2 * 2 * len(ysH)}; control {ctrl_h}", len(bad) == 0 and ctrl_h in ("TACHYON", "GHOST"),
      "the monotone phantom law is what health needs (L340 H2/H3), now from the derived block")
# C4 the tracking floor
vtrk, Cmax = 3 * 600e3 / cc, 100.0
c2_floor = float(sp.solve(sp.Eq(cs2_km2.subs(Ce, Cmax), vtrk**2), c2)[0])
P(f"    c_s >= 3 x 600 km/s where C <= {Cmax:.0f}:  c_2 >= {c2_floor:.4e}  (L340: {L340N.get('P1', {}).get('c2_min', float('nan')):.4e})")
reach = []
for c2v in (7.29e-3, 0.067, 1.0, 10.0):
    Cm = c2v / ((2 + 3 * c2v) * vtrk**2)
    ymin = brentq(lambda y_: float(CT_of(nu_mono, y_)) - Cm, 1e-14, 10.0)
    reach.append((c2v, Cm, ymin))
P("    tracking reach (largest C, i.e. deepest y, where 600 km/s is tracked with margin 3): " +
  "; ".join(f"c_2 = {r_[0]:g}: C <= {r_[1]:.0f}, y >= {r_[2]:.1e}" for r_ in reach))
OUT["numbers"]["C4"] = {"c2_floor": c2_floor, "reach": reach}
check("C4 THE TRACKING FLOOR re-derived from the exact mode: c_s >= 3 x 600 km/s where C <= 100 needs c_2 >= 7.29e-3 "
      "(a CONSTRAINT on the action's c_2); with no cosmological ceiling larger c_2 extends tracking to deeper MOND",
      f"c_2 >= {c2_floor:.3e}; reach {[(r_[0], round(r_[1]), f'{r_[2]:.1e}') for r_ in reach]}",
      abs(c2_floor - 7.2888e-3) < 2e-6)

# ============================================================================================== D the root tension (FRW)
banner(f"D   THE ROOT TENSION: linear FRW perturbations of the khronon sector, derived ({CORE_TERM} lambda-term; the other is the control)")
tq, xq, yq, zq = sp.symbols('t x y z', real=True)
X4 = (tq, xq, yq, zq)
e = sp.Symbol('e')
alc, c2c, Gc, Lam = sp.symbols('alpha_c c_2 G Lambda', real=True)
a = sp.Function('a', positive=True)(tq)
rb = sp.Function('rhobar', positive=True)(tq)
Phi, Psi, Bq, Eq, piq, th, dq = [sp.Function(s)(tq, xq) for s in ('Phi', 'Psi', 'B', 'E', 'pi', 'theta', 'delta')]
FIELDS = [Phi, Psi, Bq, Eq, piq, th, dq]


def ser(expr, n=2):
    ex = sp.expand(expr)
    return sp.Add(*[ex.coeff(e, i) * e**i for i in range(n + 1)])


def powser(Xe, p_):
    Xe = sp.expand(Xe); X0, X1, X2 = Xe.coeff(e, 0), Xe.coeff(e, 1), Xe.coeff(e, 2)
    uu = (e * X1 + e**2 * X2) / X0
    return ser(X0**p_ * (1 + p_ * uu + p_ * (p_ - 1) / 2 * uu**2))


g4 = sp.zeros(4, 4)
g4[0, 0] = -(1 + 2 * e * Phi)
g4[0, 1] = g4[1, 0] = e * a * sp.diff(Bq, xq)
g4[1, 1] = a**2 * (1 - 2 * e * Psi + 2 * e * sp.diff(Eq, xq, 2))
g4[2, 2] = a**2 * (1 - 2 * e * Psi)
g4[3, 3] = a**2 * (1 - 2 * e * Psi)
gb4 = g4.subs(e, 0); hm4 = (g4 - gb4) / e; gbi4 = gb4.inv()
gi4 = (gbi4 - e * gbi4 * hm4 * gbi4 + e**2 * gbi4 * hm4 * gbi4 * hm4 * gbi4).applyfunc(ser)
sqg4 = powser(-ser(g4.det()), sp.Rational(1, 2))
Gam4 = [[[sp.expand(ser(sum(gi4[l, s] * (sp.diff(g4[s, m], X4[n]) + sp.diff(g4[s, n], X4[m]) - sp.diff(g4[m, n], X4[s])) for s in range(4)) / 2))
          for n in range(4)] for m in range(4)] for l in range(4)]


def Ric4(m, n):
    return sum(sp.diff(Gam4[l][m][n], X4[l]) - sp.diff(Gam4[l][m][l], X4[n]) +
               sum(Gam4[l][l][s] * Gam4[s][m][n] - Gam4[l][n][s] * Gam4[s][m][l] for s in range(4)) for l in range(4))


R4 = sp.expand(ser(sum(gi4[m, n] * Ric4(m, n) for m in range(4) for n in range(4))))
tau4 = tq + e * piq
dtau4 = [sp.diff(tau4, v_) for v_ in X4]
Xk4 = sp.expand(ser(-sum(gi4[m, n] * dtau4[m] * dtau4[n] for m in range(4) for n in range(4))))
isX4 = powser(Xk4, -sp.Rational(1, 2))
n_dn4 = [sp.expand(ser(-dtau4[m] * isX4)) for m in range(4)]
n_up4 = [sp.expand(ser(sum(gi4[m, s] * n_dn4[s] for s in range(4)))) for m in range(4)]
K4 = sp.expand(ser(sum(sp.diff(sp.expand(ser(sqg4 * n_up4[m])), X4[m]) for m in range(4)) * powser(sqg4, -1)))
acc4 = [sp.expand(ser(sum(n_up4[s] * (sp.diff(n_dn4[m], X4[s]) - sum(Gam4[l][s][m] * n_dn4[l] for l in range(4))) for s in range(4)))) for m in range(4)]
aa4 = sp.expand(ser(sum(gi4[m, s] * acc4[m] * acc4[s] for m in range(4) for s in range(4))))
Hq = sp.diff(a, tq) / a
Kbar = 3 * Hq
# the leaf average is a function of the leaf label tau: <K>(tau) = K_bar(t + e pi) + O(e^2) (the O(e^2) part multiplies zero)
dK_leaf = ser(K4 - (Kbar + e * piq * sp.diff(Kbar, tq) + e**2 * piq**2 * sp.diff(Kbar, tq, 2) / 2))
Td = tq + e * th
dTd = [sp.diff(Td, v_) for v_ in X4]
rho4 = rb * (1 + e * dq)
Ldust = -rho4 / 2 * sqg4 * (sum(gi4[m, s] * dTd[m] * dTd[s] for m in range(4) for s in range(4)) + 1)   # Brown-Kuchar dust


def frw_system(term):
    Lc2 = -c2c * sqg4 * (dK_leaf**2 if term == "leaf" else K4**2)
    Lt = sp.expand(ser(sqg4 * (R4 - 2 * Lam + alc * aa4) + Lc2 + 16 * sp.pi * Gc * Ldust))
    L1, L2 = Lt.coeff(e, 1), Lt.coeff(e, 2)
    bgE = [sp.simplify(ee.lhs - ee.rhs) for ee in euler_equations(L1, FIELDS, [tq, xq])]
    rbs = sp.solve(bgE[0], rb)[0]                                       # Friedmann (vary the lapse)
    adds = sp.solve(bgE[1].subs(rb, rbs), sp.diff(a, tq, 2))[0]         # acceleration (vary the scale)
    ELq = euler_equations(L2, FIELDS, [tq, xq])
    kF = sp.Symbol('k', positive=True)
    amp = {F: sp.Function(F.func.__name__ + 'k')(tq) for F in FIELDS}

    def fourier(ex):
        for F in FIELDS:
            ex = ex.subs(F, amp[F] * sp.exp(sp.I * kF * xq))
        return sp.expand(sp.simplify(ex.doit() * sp.exp(-sp.I * kF * xq)))

    def bgsub(ex):
        ex = ex.subs({amp[Bq]: 0, amp[Eq]: 0}).doit()
        ex = ex.subs(sp.diff(a, tq, 3), sp.diff(adds, tq)).subs(sp.diff(a, tq, 2), adds).subs(rb, rbs)
        ex = ex.subs(sp.diff(a, tq, 2), adds)
        return sp.expand(sp.simplify(ex))

    Eg = [bgsub(fourier(ee.lhs - ee.rhs)) for ee in ELq]
    Q1 = dK_leaf.coeff(e, 1) if term == "leaf" else K4.coeff(e, 1)
    Qk = bgsub(fourier(Q1))
    return dict(bg=bgE, rbs=rbs, adds=adds, Eg=Eg, Qk=Qk, amp=amp, k=kF)


SYS = {tm: frw_system(tm) for tm in ("leaf", "plain")}
P(f"    both systems derived ({time.time() - T0:.1f} s)")
Hs = sp.Symbol('H', positive=True)


def friedmann_c2(sysd):
    """8 pi G rho_bar a^2 in terms of adot^2: its c_2-dependence is the background's"""
    return sp.factor(sp.expand(8 * sp.pi * Gc * sysd["rbs"] * a**2))


fr = {tm: friedmann_c2(SYS[tm]) for tm in SYS}
for tm in SYS:
    P(f"    [{tm:5s}] Friedmann: 8 pi G rho_bar a^2 = {fr[tm]};  acceleration: a_tt = {sp.factor(SYS[tm]['adds'])}")
core = SYS[CORE_TERM]
d1_core = not fr[CORE_TERM].has(c2c)
d1_ctrl = fr["plain"].has(c2c) and sp.simplify(fr["plain"].subs(sp.diff(a, tq), Hs * a) / (a**2 * Hs**2)
                                                - (3 * (1 + sp.Rational(3, 2) * c2c) - Lam / Hs**2)) == 0
check("D1 THE FRW BACKGROUND from the action: the core's lambda-term leaves the Friedmann equation GR's (c_2 absent: "
      "G_cos = G); control: the plain -c_2 K^2 gives 8 pi G rho_bar = 3H^2 (1 + 3c_2/2) - Lambda (L350 G1)",
      f"core ({CORE_TERM}) c_2 in Friedmann: {fr[CORE_TERM].has(c2c)}; plain control reproduces L350 G1: {d1_ctrl}", d1_core and d1_ctrl,
      "the leaf average removes the background effect behind every published Horava cosmological cap")
# D2 the structural theorem
names7 = ['Phi', 'Psi', 'B', 'E', 'pi', 'theta', 'delta']


def structural(sysd):
    amp, Qk = sysd["amp"], sysd["Qk"]
    pisol = sp.solve(Qk, amp[piq])[0]

    def on_Q0(ex):
        r_ = ex
        for n_ in (3, 2, 1):
            r_ = r_.subs(sp.diff(amp[piq], tq, n_), sp.diff(pisol, tq, n_))
        r_ = r_.subs(amp[piq], pisol).doit()
        r_ = r_.subs(sp.diff(a, tq, 3), sp.diff(sysd["adds"], tq)).subs(sp.diff(a, tq, 2), sysd["adds"]).subs(sp.diff(a, tq, 2), sysd["adds"])
        return sp.simplify(r_)

    res = {}
    for nm, ee in zip(names7, sysd["Eg"]):
        ec2 = sp.expand(sp.diff(ee, c2c))
        res[nm] = 0 if ec2 == 0 else on_Q0(ec2)
    dust_free = all(sp.diff(sysd["Eg"][names7.index(nm)], c2c) == 0 for nm in ("theta", "delta"))
    return res, dust_free, pisol


st = {tm: structural(SYS[tm]) for tm in SYS}
for tm in SYS:
    P(f"    [{tm:5s}] c_2-part of each equation on Q = 0: " + ", ".join(f"{nm}: {'0' if r_ == 0 else 'NONZERO'}" for nm, r_ in st[tm][0].items())
      + f";  dust equations c_2-free: {st[tm][1]}")
Qc = SYS["leaf"]["Qk"]
P(f"    Q (leaf) = {sp.collect(Qc, [SYS['leaf']['amp'][piq]])}")
# the khronon equation: c_2 part and alpha_c part
Epi = SYS[CORE_TERM]["Eg"][names7.index('pi')]
Epi_c2 = sp.factor(sp.diff(Epi, c2c)); Epi_al = sp.factor(sp.diff(Epi, alc))
ampL = SYS[CORE_TERM]["amp"]; kL = SYS[CORE_TERM]["k"]
Epi_rest = sp.simplify(Epi - c2c * sp.diff(Epi, c2c) - alc * sp.diff(Epi, alc))
Qexpr = SYS[CORE_TERM]["Qk"]
ratio_c2 = sp.simplify(Epi_c2 / Qexpr)
P(f"    [{CORE_TERM}] khronon equation: c_2-part = {Epi_c2}")
P(f"                              alpha_c-part = {Epi_al};  remainder = {Epi_rest};  c_2-part / Q = {ratio_c2}")
phi_al = sp.factor(sp.diff(SYS[CORE_TERM]["Eg"][0], alc))
P(f"    [{CORE_TERM}] lapse (Hamiltonian) equation alpha_c-part = {phi_al};  Psi/E/B equations alpha_c-parts: " +
  ", ".join(str(sp.simplify(sp.diff(SYS[CORE_TERM]['Eg'][names7.index(nm)], alc))) for nm in ('Psi', 'E', 'B')))
core_struct = all(r_ == 0 for r_ in st[CORE_TERM][0].values()) and st[CORE_TERM][1]
ctrl_struct = any(r_ != 0 for r_ in st["plain"][0].values()) and not st["plain"][1]
pi_ok = Epi_rest == 0 and not ratio_c2.has(ampL[Phi]) and not ratio_c2.has(ampL[Psi]) and not ratio_c2.has(ampL[piq])
check("D2 THE ROOT TENSION AT LINEAR ORDER (khronon + dust, the MOND sector off in the linear web -- the ungated sector has "
      "no linearisation there, D4): with the core's lambda-term, c_2 enters every linear FRW equation ONLY through "
      "Q = (K - <K>)^(1) = (k^2/a^2 - 3 Hdot) pi - 3 H Phi - 3 Psidot (all c_2-parts vanish on Q = 0), the dust equations "
      "carry no c_2, and the khronon equation is [c_2 x (k^2/a^2 - 3Hdot) x Q] + [alpha_c x d/dt(a(Phi - pidot))] = 0, so "
      "c_2 Q = O(alpha_c): the linear cosmology is c_2-independent up to O(alpha_c).  Control: the plain -c_2 K^2 fails this "
      "in every equation, including the dust's",
      f"core ({CORE_TERM}): all c_2-parts vanish on Q = 0: {all(r_ == 0 for r_ in st[CORE_TERM][0].values())}, dust c_2-free: "
      f"{st[CORE_TERM][1]}, khronon c_2-part / Q = {ratio_c2}; plain control fails: {ctrl_struct}",
      core_struct and ctrl_struct and pi_ok,
      "the leaf-averaged lambda-term is inert on cosmological perturbations because the khronon relaxes its leaves to "
      "constant mean curvature (Q -> 0) and the leaf average removes the only k = 0 channel; c_2 acts where Q is sourced by "
      "something the khronon cannot absorb -- a moving MOND phantom (C1), not the linear web.  Assumes the khronon's fast "
      "mode (omega^2 ~ (c_2/alpha_c) k^2/a^2) is not excited (adiabatic initial data); if excited it oscillates at >> H")
# D3 the numbers: quasi-static growth coupling and sigma_8
# L350 G3's growth convention, reimplemented (read-only reuse): Planck-2018 densities with radiation, D = D' = 1 at
# z = 1000, the Friedmann-normalised Omega_m(a) and H(a) an observer infers; mu multiplies the Poisson source only
_h = 0.6736; _ob, _oc = 0.02237, 0.1200; _T = 2.7255; _Neff = 3.046
_H0 = 100 * _h * 1e3 / (PC * 1e6); _rhoc = 3 * _H0**2 / (8 * math.pi * Gn)
_Og = (4 * 5.670374419e-8 * _T**4 / cc**3) / _rhoc; OR_ = _Og * (1 + _Neff * (7 / 8) * (4 / 11)**(4 / 3))
OM_ = (_ob + _oc) / _h**2; OL_ = 1 - OM_ - OR_


def growth_D(mu, z_i=1000.0):
    Ez = lambda A: math.sqrt(OR_ / A**4 + OM_ / A**3 + OL_)
    dlnH = lambda A: 0.5 * (-4 * OR_ / A**4 - 3 * OM_ / A**3) / Ez(A)**2
    s_ = solve_ivp(lambda Nn, Y: [Y[1], 1.5 * mu * (OM_ / math.exp(3 * Nn) / Ez(math.exp(Nn))**2) * Y[0] - (2 + dlnH(math.exp(Nn))) * Y[1]],
                   (math.log(1 / (1 + z_i)), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-10, atol=1e-14)
    return s_.y[0][-1]


def growth_ratio(mu):
    return growth_D(mu) / growth_D(1.0)


# the quasi-static coupling from the derived equations: sub-horizon, Q = 0, pidot -> 0, Psidot = Phidot = 0, thetadot = Phi
def qs_mu(sysd):
    amp = sysd["amp"]; kF = sysd["k"]
    lam_s = sp.Symbol('lam', positive=True)                          # k -> k/lam, delta -> delta/lam^2: sub-horizon ordering
    Ephi, Epsi = sysd["Eg"][0], sysd["Eg"][1]
    qs = {sp.diff(amp[Psi], tq): 0, sp.diff(amp[Psi], tq, 2): 0, sp.diff(amp[Phi], tq): 0,
          sp.diff(amp[th], tq): amp[Phi], sp.diff(amp[th], tq, 2): 0, sp.diff(amp[piq], tq): 0, sp.diff(amp[piq], tq, 2): 0}
    Ps, Fs, ds = sp.symbols('Psi_s Phi_s delta_s')
    out = []
    for Eq_ in (Ephi, Epsi):
        ex = Eq_.subs(qs).subs(amp[piq], 0)
        ex = ex.subs({amp[Psi]: Ps, amp[Phi]: Fs, amp[dq]: ds, amp[th]: 0})
        ex = sp.expand(ex.subs({kF: kF / lam_s, ds: ds / lam_s**2}) * lam_s**2)
        out.append(sp.expand(ex.subs(lam_s, 0)))
    sol_ = sp.solve(out, [Ps, Fs], dict=True)[0]
    # Poisson: k^2 Psi / a^2 = -4 pi G_eff rho_bar delta ; G_eff / G_cos with rho_bar from the system's own Friedmann
    Geff_over_G = sp.simplify(-sol_[Ps] * kF**2 / (a**2 * 4 * sp.pi * Gc * sysd["rbs"] * ds))
    slip = sp.simplify(sol_[Fs] / sol_[Ps])
    return Geff_over_G, slip


mu = {tm: qs_mu(SYS[tm]) for tm in SYS}
G_over_Gcos = {tm: sp.simplify(fr[tm].subs(sp.diff(a, tq), Hs * a) / (a**2) / (3 * Hs**2 - Lam)) for tm in SYS}
mu_growth = {}
for tm in SYS:
    # growth source relative to GR at the same H: (G_eff rho_bar)/(G rho_bar_GR) = (G_eff/G) x (8 pi G rho_bar)/(3H^2 - Lambda)
    # = G_eff/G_cos, since 8 pi G rho_bar = (G/G_cos)(3H^2 - Lambda)
    mu_growth[tm] = sp.simplify(mu[tm][0] * G_over_Gcos[tm])
    P(f"    [{tm:5s}] quasi-static: G_eff/G = {sp.nsimplify(mu[tm][0])}, slip Phi/Psi = {sp.nsimplify(mu[tm][1])};  growth source / "
      f"GR's = {sp.factor(sp.nsimplify(mu_growth[tm]))}")
ALC, C2F = 3.2e-9, c2_floor                                          # the window's alpha_c edge and C4's tracking floor
mu_core = float(mu_growth[CORE_TERM].subs({alc: ALC, c2c: C2F, Lam: 0, Hs: 1}))
mu_plain = float(mu_growth["plain"].subs({alc: ALC, c2c: C2F, Lam: 0, Hs: 1}))
mu_plain_hi = float(mu_growth["plain"].subs({alc: ALC, c2c: 0.067, Lam: 0, Hs: 1}))
dsig_core = growth_ratio(mu_core) - 1.0
dsig_plain = growth_ratio(mu_plain) - 1.0
l350g3 = None
try:
    l350g3 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L350_chk_cosmological_G_gate_results.json")))["numbers"]["G3"]["rows"][0]
except Exception:
    pass
s8_l350 = (l350g3["sigma8"] / 0.811 - 1) if l350g3 else float("nan")
P(f"    at alpha_c = {ALC:.1e}, c_2 = {C2F}: growth-source ratio core {mu_core - 1:+.3e} -> sigma_8 {dsig_core:+.3e};  plain "
  f"{mu_plain - 1:+.3e} -> sigma_8 {dsig_plain:+.3%}  (L350 G3 recorded {s8_l350:+.3%} at its c_2 = {l350g3['c2'] if l350g3 else '?'});  "
  f"plain at c_2 = 0.067: {mu_plain_hi - 1:+.3e}")
OUT["numbers"]["D3"] = {"G_eff_over_G": {tm: str(mu[tm][0]) for tm in SYS}, "slip": {tm: str(mu[tm][1]) for tm in SYS},
                        "growth_source_ratio": {tm: str(mu_growth[tm]) for tm in SYS}, "core_mu_minus_1": mu_core - 1,
                        "core_dsigma8": dsig_core, "plain_mu_minus_1": mu_plain - 1, "plain_dsigma8": dsig_plain}
d3_ok = (abs(mu_core - 1) < 1e-8 and abs(dsig_core) < 1e-7 and sp.simplify(mu[CORE_TERM][1] - 1) == 0 and 0.03 < dsig_plain < 0.05
         and (l350g3 is None or abs(dsig_plain - s8_l350) < 2e-4))
check("D3 THE NUMBERS: the core's quasi-static growth coupling is G_eff/G_cos = 1/(1 - alpha_c/2) with no slip, so sigma_8 "
      "moves by ~1e-9 across the whole tracking window; the plain term gives (1 + 3c_2/2)/(1 - alpha_c/2), +4.1% on sigma_8 "
      "at the tracking floor (L350 G3's growth convention, reproduced) -- the effect every Planck-era Horava cap constrains.  The tracking window "
      "c_2 >= 7.29e-3 is therefore NOT excluded at linear order, and L340's BBN ceiling (a G_cos effect) is gone",
      f"core: mu - 1 = {mu_core - 1:+.2e}, d sigma_8 = {dsig_core:+.2e}, slip {mu[CORE_TERM][1]}; plain: mu - 1 = {mu_plain - 1:+.3e}, "
      f"d sigma_8 = {dsig_plain:+.2%}", d3_ok,
      "linear-order statement from the derived equations; a Boltzmann-level fit of the leaf-averaged core has not been run (OPEN)")
# D4 what the leaf average does not fix (reported)
ysmall = np.array([1e-4, 1e-6, 1e-8])
Csmall = CT_of(nu_mono, ysmall)
csk = [cc * math.sqrt(1.0 / (3 * Cv)) / 1e3 for Cv in Csmall]        # c_2 -> oo limit of c_s
P(f"    the ungated core at small gradient: C_T = nu_mono - 1 = {', '.join(f'{v_:.0f}' for v_ in Csmall)} at y = 1e-4/1e-6/1e-8 "
  f"(C ~ y^-1/2 -> oo); the tracking speed's c_2 -> oo ceiling c/sqrt(3C) = {', '.join(f'{v_:.0f}' for v_ in csk)} km/s")
check("D4 (reported) the leaf average does NOT fix the ungated core's own cosmology: at zero gradient the kernel's linear "
      "coefficient C = nu - 1 diverges (q is C^1, not C^2, at p = 0), so the core has no linear FRW sector and L341's growth "
      "failure (sigma_8 18-27) stands, independently of c_2; the owed piece is the vacuum gate (the cosmology lane's), and "
      "at any gradient the tracking speed is capped by c/sqrt(3C)",
      f"C_T {Csmall.tolist()} at y {ysmall.tolist()}; c_s cap {[round(v_) for v_ in csk]} km/s", True, load_bearing=False)

# ============================================================================================== W ledger
banner("W   THE LEDGER: what this lane settles for the C-H/K core")
LEDGER = [
    ("L3-FP2", "root action for the relativistic lanes: the ungated C-H/K core (C-H + BPS khronon, beta = 0, leaf-averaged "
               "lambda-term, nu_mono)", "POSTULATED", "coordinator's choice after the root-action map; the leaf average and "
                                                      "alpha_c a^2, c_2 terms are chosen, not derived"),
    ("L5a", "the heat filter in the linear theory: C_eff = e^{-xi^2 k^2} C, C_T = nu - 1, C_L = nu - 1 + y nu'", "DERIVED", "A2, sympy dsolve"),
    ("L5b", "the core's quadratic action = L340's block; C-H sector instantaneous and shift-free", "DERIVED", "A1, symbolic second variation"),
    ("L7", "tensor speed c_T = 1 (GW170817)", "DERIVED", "A3: omega^2 = k^2, no C-H or khronon term in the TT sector"),
    ("L6a", "PPN gamma = 1", "DERIVED", "B3 (every C_eff); KM3 at 1PN"),
    ("L6b", "PPN beta = 1", "DERIVED", "KM3 P2 (inherited; the C-H sector is filtered off at 1 AU, B4)"),
    ("L6c", "PPN alpha_3 = 0", "DERIVED", "B3: the g_0j and g_00 readings of alpha_1 agree with the C-H sector live"),
    ("L6d", "PPN alpha_1 = -4 alpha_c - 8 C_eff/(1+C_eff)", "DERIVED", "B3 closed form; B4 C-H part <= 1e-11 at 1 AU"),
    ("L6e", "PPN alpha_2 (closed form, KM2 amplification inside)", "DERIVED", "B3; B2 reproduces Yagi+14 at C = 0"),
    ("L6f", "alpha_c <= 3.2e-9 (|alpha_1| < 1e-5, |alpha_2| < 1.6e-9)", "CONSTRAINT", "B4; alpha_c is a free coupling"),
    ("L8a", "moving-source tracking (L330 gate): the omega -> 0 response is static MOND iff c_2 != 0", "DERIVED", "C1, C2"),
    ("L8b", "health on the static MOND background needs the monotone kernel nu_mono", "DERIVED", "C3 (Krein, frozen coefficients)"),
    ("L8c", "tracking floor c_2 >= 7.29e-3 (3 x 600 km/s where C <= 100)", "CONSTRAINT", "C4"),
    ("L9a", "Planck-era cap on c_2 vs the tracking floor: the leaf-averaged lambda-term is c_2-inert in linear cosmology "
            "(G_eff/G_cos = 1/(1 - alpha_c/2), no slip); the published caps do not apply", "DERIVED",
     "D1-D3 (linear equations, MOND sector off in the web); a Boltzmann-level fit is owed"),
    ("L9b", "c_2 upper edge (BBN 0.067 in L340) -- removed with G_cos = G; no ceiling found at linear order", "OPEN",
     "D3; strong coupling / nonlinear khronon not checked here"),
    ("L9c", "the ungated core's own linear cosmology (C -> oo at zero gradient)", "FAILS",
     "D4 + L341 (sigma_8 18-27, inherited); needs the vacuum gate -- independent of c_2"),
    ("L10", "nonlinear well-posedness, strong coupling of the full core", "OPEN", "XC1-XC3 scoped it; not re-derived here"),
]
for k_, what, status, basis in LEDGER:
    P(f"    {k_:7s} {status:11s} {what}  --  {basis}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger of this lane", f"{len(LEDGER)} links", True, load_bearing=False)

# ============================================================================================== verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P(f"""  The C-H/K core, varied as one action: its quadratic sector is L340's block (A1), the heat filter only rescales the
  constitutive tensor by e^(-xi^2 k^2) (A2), and c_T = 1 exactly (A3).  The full PPN with the C-H sector live gives gamma = 1,
  alpha_3 = 0, alpha_1 = -4 alpha_c - 8 C_eff/(1 + C_eff) and a closed-form alpha_2 carrying KM2's amplification (B3); at the
  scales of the bounds the filter leaves <= 1e-11 of it, so the bounds are the khronometric ones and cap alpha_c <= 3.2e-9
  (B4).  Tracking holds iff c_2 != 0 (C1-C2), the monotone kernel is healthy (C3), and tracking needs c_2 >= 7.29e-3 (C4).
  The root tension does not survive linear order: the leaf-averaged lambda-term enters the linear FRW equations only
  through Q = (K - <K>)^(1), which the khronon drives to O(alpha_c/c_2), so linear cosmology is c_2-independent
  (G_eff/G_cos = 1/(1 - alpha_c/2), no slip) and the Planck-era caps -- which constrain the plain term's G_cos -- do not
  apply (D1-D3).  What the leaf average does not fix is the ungated core's own cosmology (C -> oo at zero gradient,
  L341), which is c_2-independent and belongs to the vacuum gate (D4).  Time {time.time() - T0:.0f} s.""")
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"FP2_relativistic_consistency_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {len(CH) - sum(1 for _, ok, _ in CH if not ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
