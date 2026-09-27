#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP5 -- GATE G-2 ON THE UNGATED C-H/K CORE: the canonical degree-of-freedom count, linear well-posedness, "a0 as a
field", and the free constants the core carries.

WHY.  The derivation chain is re-rooted in the ungated C-H/K core.  Its canonical count has no owner on the record
(real_research/cross_thread_review_2026_09_26/XR3_obligations.md, requirement 2).  XC2 reduced strong hyperbolicity to
GR + the BPS khronon without settling it.  XC5 E6 found that the response around an open zero-field region scales as
sqrt(eps).  This lane counts the modes from the action's own quadratic form, locates every rank change, and says what the
nonlocal heat filter adds.  It then asks whether any term of the core can tie a0 to Lambda, and lists the core's
constants with their status.

THE CORE (varied here exactly as written; nothing is added by hand):
    I = c^3/(16 pi G) Int d^4x sqrt(-g) { R - 2 Lambda + 2 h^{mn}(D_m U - a_m)(D_n U - a_n)
          + 2 alpha^2 q(h^{mn} D_m W_b D_n W_b / alpha^2) + Int_0^b dz L (d_z W - Delta_h W) + lambda_0 (W_0 - U)
          + alpha_c a_m a^m - c_2 (K - <K>_h)^2 } + GHY + S_m[g]
The first line is astra's C-H action (qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md:95-106).
The khronon terms are L340's BPS terms with beta = 0 (real_research/g03_audit_2026/L340_filtered_khronon_completion.py:9),
with L350's proper-volume leaf average (as in real_research/chk_v0_2026/CV2_covariant_action.py).  The clock tau gives
n_m = -d_m tau / sqrt(X), N = X^{-1/2}, a_m = D_m ln N, K = nabla_m n^m.  The kernel is nu_mono: nu_RAR up to the splice
y_s = 2.3374, then the phantom floor h' = 0.05 h_p/(y + y_p) (L340 A1).  In this lane q'(s^2) = nu_mono(s) - 1, alpha = a0/c^2,
and b = xi^2/2.  There is no gate, no L353/L361 pair and no dark state: this is the ungated core.

CHECKS
  K0 CONTROL  the second-order ADM Lagrangian (built from the action in unitary gauge) is invariant under all three
              linearised spatial diffeomorphisms: the Noether identity M(w,k).v_xi = 0 holds exactly.
  K1 CONTROL  with a generic BPS triple (xi_B, lambda_B, eta) and no MOND sector the machine reproduces the published
              healthy extension (Blas, Pujolas & Sibiryakov 2010/2011): c_T^2 = xi_B, c_s^2 = xi(l-1)(2 xi - eta)/(eta(3l-1)),
              G_N/G = 1/(xi_B - eta/2).
  K2 CONTROL  at the record's action (c_CH = 2), L340 H1's committed static zero set alpha_c(1 + C) = 2 and its static gain
              (1 + C)/(1 - alpha_c(1 + C)/2) are reproduced in this lane's gauge.
  K3 CONTROL  FRW minisuperspace: the plain -c_2 K^2 gives G_cos = G/(1 + 3c_2/2) (L350 G1); the leaf average gives G_cos = G.
  A1 the unitary-gauge velocity content, from the covariant definitions on generic polynomial fields: n.n = -1,
     a_m a^m = h^{ij} d_i lnN d_j lnN, h^{mn} dU dU = h^{ij} d_iU d_jU, K = h^{ij}(hdot_ij - 2 D_(i N_j))/(2N), and
     Delta_h F = h^{mn} nabla_m nabla_n F + K n(F) = (1/sqrt h) d_i(sqrt h h^{ij} d_j F).  Only the hdot_ij are velocities.
  A2 the Legendre map: the kinetic Hessian of K_ij K^ij - lambda K^2 has eigenvalues 2 (x5) and 2(1 - 3 lambda).  The leaf
     average makes lambda = 1 + c_2 on k != 0 and lambda = 1 on k = 0, so the map is invertible on every mode.
  A3 the auxiliary sector is second class.  The heat block's determinant does not depend on the kernel.  The (N, U) Hessian
     is positive on nu_mono's whole range.  The Dirac bookkeeping gives 3 local degrees of freedom for every z-resolution.
  B1 THE COUNT: deg_w det M = 4 (tensor) + 0 (vector) + 2 (scalar), so N = 3 (2 tensor + 1 khronon scalar).  This holds for
     1-4 explicit heat points and random parameter draws, with det M not identically zero (no residual gauge).
  B2 the nonlocal filter adds no modes and no first-class constraints.  Its Schur complement is exactly the tangent
     sigma_n(k)^2 C, with sigma_n = (1 + b k^2/n)^(-n) -> exp(-b k^2).
  B3 the reduced khronon: kinetic coefficient (2 + 3c_2)/(2 c_2) > 0 (no ghost for c_2 > 0);
     w^2 = c_2 (2 - E) k^2 / (E (2 + 3 c_2)) with E(C) = alpha_c + 2 C c_CH/(c_CH + 2C); tensor det ~ (w^2 - k^2)^2, c_T = 1.
  B4 the exceptional surfaces, located: E = 0 (the lapse becomes a multiplier and the scalar is lost), c_2 = 0 (frozen,
     w = 0), lambda = 1/3 (no kinetic term), E = 2 (static-gain pole, w = 0).  nu_mono's C > 0 excludes 1 + C <= 0.
  C1 the nonzero-field branch is healthy (0 < E < 2) for every field above g* = y* a0, y*_T ~ (alpha_c/2)^2 (XR3 K4 reproduced).
  C2 ZERO FIELD, the exact leaf problem at fixed lapse (1-D, nu_mono): at an open zero-field region U is pinned
     (dU' ~ eps^2) and the lapse feels the full C-H coefficient (R -> 1).  At a nonzero field the response is linear with
     R = C_L/(1 + C_L).  This is the canonical face of XC5 E6's sqrt(eps).
  C3 ZERO FIELD, the formal linearisation: E_inf = c_CH + alpha_c = 2 + alpha_c > 2.  This is BPS khronometric gravity
     outside its window 0 < alpha < 2: w^2 < 0 at EVERY k (the filter cannot help at C = inf), with a growth rate
     proportional to k, so the linearisation is Hadamard ill-posed; the static gain is -2/alpha_c.
     Because E runs from alpha_c (Newtonian end) to alpha_c + c_CH (zero field), no alpha_c fits both ends (the alpha-pincer).
  C4 (reported) finite amplitude: below y* the unstable band is bounded, k_max xi = sqrt(ln(C/C*)), and it saturates at
     y ~ y*.
  C6 (reported) the only in-core exit from the pincer, c_CH = 2(1 - delta) with delta > alpha_c/2, priced against the
     static law.  It is not adopted: it is a new constant and it leaves the growth excess.
  C5 the principal symbol off open zero-field regions (k xi -> inf) is GR + BPS(alpha_c, c_2, beta = 0): real, distinct
     physical cones (c, c_s) and an elliptic lapse, with no complex characteristic.  A strongly hyperbolic nonlinear
     formulation stays OPEN.
  D1 FRW: every MOND, C-H, alpha_c and leaf-average term vanishes on the homogeneous background, and the Friedmann equation
     3H^2 = Lambda + 8 pi G rho does not contain a0.  The lapse constraint is local, so no dust integration constant appears.
  D2 statics: q -> q + const leaves the field equations unchanged (the zero mode; k01 K1 in C-H form).
  D3 a0 promoted to a field sigma: d_sigma[2 sigma^2 q(Z/sigma^2)] vanishes identically at Z = 0 (a flat direction on FRW)
     and is > 0 at every Z > 0 for nu_mono.  No stationary MOND field exists without a potential put in by hand.
  D4 the khronon's only background scale is K = 3H (and <K> = K).  Tying a0 to it gives a0 ~ H(z), the rival footing,
     +0.576 dex at z = 2.5, which L37 kills at recombination (read from the committed output).
  D5 the record: k01 (no equation relates a0 to Lambda) and k04 (the four-form leaves a free ratio), read from committed outputs.
  E  (reported) the core's constants, each with a status, with values read from the committed L340/L350 results.
  W  (reported) the ledger.
MUTATE=1 changes the C-H coefficient 2 -> 2(1 - 1e-3).  The zero-field sector then sits inside the BPS window, so C3
(and C1's crossing) must FAIL (rc = 1).  This shows the zero-field verdict is computed from the action's actual
coefficient, not written in.

SCOPE.  The count is exact at the level of the primary structure (A1, A2) and the second-class algebra (A3).  B-C are
linear, at frozen coefficients and principal weak-field order (the L340 block's order): background gradients of order
a0/c^2 and O(Phi/c^2) clock terms are dropped (L340 D1-D4/H4 cover those; H4's alpha_min is inherited in A3).  The
nonlinear well-posedness of GR + BPS khronon is not settled here.  Both a0 footings are carried: 9.3603e-11 and 1.1312e-10.

Run from the repository root:  python3 real_research/derivation_chain_2026/FP5_dof_and_a0_field.py
"""
import os, re, sys, json, math, time, random
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP5_dof_and_a0_field" + ("_MUTATE" if MUTATE else "")
OUT = {"lane": "FP5", "gate": "G-2", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []
T0 = time.time()

# inputs (FP0's canonical pair)
c_SI, G_SI = 299792458.0, 6.67430e-11
MPC = 3.0856775814913673e22
H0_KMS, OM_L, OM_M = 67.4, 0.6847, 0.3153
KAPPA = 0.5
DELTA_MUT = 1.0e-3
C_CH = sp.Integer(2) if not MUTATE else 2 * (1 - sp.Rational(1, 1000))   # the C-H coefficient of |DU - a|^2
PC = 3.0856775814913673e16
YR = 3.15576e7


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)


def check(name, measured, ok, load_bearing=True):
    CH.append((name, bool(ok), load_bearing))
    OUT["checks"][name] = {"ok": bool(ok), "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")


def rd(rel):
    p = os.path.join(REPO, rel)
    return open(p, errors="replace").read() if os.path.exists(p) else None


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P(f"\n  *** MUTATE=1: C-H coefficient 2 -> 2(1 - {DELTA_MUT:g}) = {float(C_CH)}; C3 (zero-field verdict) must FAIL ***")

# ------------------------------------------------------------------------------------------------ footings
H0 = H0_KMS * 1e3 / MPC
rho_c = 3 * H0 ** 2 / (8 * math.pi * G_SI)
rho_L = OM_L * rho_c
A0 = {"canonical": KAPPA * c_SI * math.sqrt(G_SI * rho_L), "alt": KAPPA * c_SI * math.sqrt(G_SI * rho_c)}
LAMBDA_SI = 8 * math.pi * G_SI * rho_L / c_SI ** 2                       # 1/m^2
OUT["numbers"]["a0"] = A0

# ------------------------------------------------------------------------------------------------ the kernel nu_mono (closed form)
DELTA_FLOOR = 0.05


def h_rar(y):
    return y / math.expm1(math.sqrt(y)) if y > 0 else 0.0


def dh_rar(y):
    s = math.sqrt(y); e = math.expm1(s)
    return (1.0 / e) * (1.0 - 0.5 * s * (e + 1.0) / e)


Y_P = brentq(dh_rar, 1.0, 5.0); H_P = h_rar(Y_P)
Y_S = brentq(lambda y: dh_rar(y) - DELTA_FLOOR * H_P / (y + Y_P), 1.0, Y_P); H_S = h_rar(Y_S)


def h_mono(y):
    return h_rar(y) if y <= Y_S else H_S + DELTA_FLOOR * H_P * math.log((y + Y_P) / (Y_S + Y_P))


def CL(y):                      # longitudinal tangent d(y nu)/dy - 1 = h'(y)
    return dh_rar(y) if y <= Y_S else DELTA_FLOOR * H_P / (y + Y_P)


def CT(y):                      # transverse tangent nu - 1 = h/y
    return h_mono(y) / y


_HS = quad(lambda v: 2 * v ** 3 / math.expm1(v) if v > 0 else 0.0, 0, math.sqrt(Y_S), epsabs=0, epsrel=1e-13)[0]


def H_mono(s):                  # Int_0^s h ; q(s^2) = 2 H(s) in units alpha = 1
    if s <= Y_S:
        return quad(lambda v: 2 * v ** 3 / math.expm1(v) if v > 0 else 0.0, 0, math.sqrt(s), epsabs=0, epsrel=1e-13)[0]
    return _HS + H_S * (s - Y_S) + DELTA_FLOOR * H_P * ((s + Y_P) * math.log((s + Y_P) / (Y_S + Y_P)) - (s - Y_S))


P(f"\n  nu_mono: y_p = {Y_P:.4f}, h_p = {H_P:.4f} a0, splice y_s = {Y_S:.4f}, floor slope {DELTA_FLOOR}; "
  f"canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2")

# ================================================================================================ the ADM machine
t, z = sp.symbols('t z', real=True)
eps = sp.Symbol('epsilon')
w, k = sp.symbols('omega k', positive=True)
xiB, lamB, eta, cCH, Cs, c2, ac = sp.symbols('xi_B lambda_B eta c_CH C c_2 alpha_c', real=True)
dz = sp.Symbol('Delta_z', positive=True)


def Fn(n):
    return sp.Function(n)(t, z)


hp, hc, hs, Hxz, Hyz, Hzz = (Fn(q) for q in ('hp', 'hc', 'hs', 'Hxz', 'Hyz', 'Hzz'))
phi, nx, ny, nzf, u = (Fn(q) for q in ('phi', 'nx', 'ny', 'nz', 'u'))
BASE = [hp, hc, Hxz, Hyz, Hzz, hs, phi, nx, ny, nzf, u]
BASEN = ['hp', 'hc', 'Hxz', 'Hyz', 'Hzz', 'hs', 'phi', 'nx', 'ny', 'nz', 'u']


def tr(e, n=2):
    e = sp.expand(e)
    return sum(e.coeff(eps, i) * eps ** i for i in range(n + 1))


def adm_L2():
    """Second-order unitary-gauge ADM Lagrangian of  N sqrt(h)[xi_B R3 + K_ij K^ij - lambda_B K^2 + eta a^2 + c_CH |DU - a|^2]
    around flat space, fields depending on (t, z) (k along z)."""
    H = sp.Matrix([[hs + hp, hc, Hxz], [hc, hs - hp, Hyz], [Hxz, Hyz, Hzz]])
    h = sp.eye(3) + eps * H
    hinv = (sp.eye(3) - eps * H + eps ** 2 * H * H).applyfunc(tr)
    trH, trH2 = H.trace(), (H * H).trace()
    sqrth = 1 + eps * trH / 2 + eps ** 2 * (trH ** 2 / 8 - trH2 / 4)
    N = 1 + eps * phi
    invN = 1 - eps * phi + eps ** 2 * phi ** 2
    Nup = sp.Matrix([nx, ny, nzf]) * eps
    Ndn = (h * Nup).applyfunc(tr)
    d = lambda e, i: 0 if i < 2 else sp.diff(e, z)
    Gam = [[[tr(sum(hinv[kk, l] * (d(h[l, j], i) + d(h[l, i], j) - d(h[i, j], l)) for l in range(3)) / 2)
             for j in range(3)] for i in range(3)] for kk in range(3)]
    DN = sp.Matrix(3, 3, lambda i, j: tr(d(Ndn[j], i) - sum(Gam[kk][i][j] * Ndn[kk] for kk in range(3))))
    Kij = sp.Matrix(3, 3, lambda i, j: tr((sp.diff(h[i, j], t) - DN[i, j] - DN[j, i]) * invN / 2))
    Kup = (hinv * Kij * hinv).applyfunc(tr)
    KK = tr(sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3)))
    Ktr = tr(sum(hinv[i, j] * Kij[i, j] for i in range(3) for j in range(3)))

    def Ric(i, j):
        e = sum(d(Gam[kk][i][j], kk) for kk in range(3)) - sum(d(Gam[kk][i][kk], j) for kk in range(3))
        e += sum(Gam[kk][kk][l] * Gam[l][i][j] for kk in range(3) for l in range(3))
        e -= sum(Gam[kk][j][l] * Gam[l][i][kk] for kk in range(3) for l in range(3))
        return tr(e)
    R3 = tr(sum(hinv[i, j] * Ric(i, j) for i in range(3) for j in range(3)))
    lnN = eps * phi - eps ** 2 * phi ** 2 / 2
    az = sp.diff(lnN, z)
    a2 = tr(hinv[2, 2] * az ** 2)
    CHt = tr(hinv[2, 2] * (eps * sp.diff(u, z) - az) ** 2)
    Lg = tr(N * sqrth * (xiB * R3 + KK - lamB * Ktr ** 2 + eta * a2 + cCH * CHt))
    return Lg.coeff(eps, 1), Lg.coeff(eps, 2)


def fourier_matrix(L2, fields):
    """Hermitian M(w,k) of the quadratic action S2 = Int X^dagger M X for plane waves exp(i(kz - wt)); total derivatives drop."""
    L2 = sp.expand(L2)
    atoms = {}
    for a in L2.atoms(sp.Derivative):
        atoms[a] = (a.expr, sum(cn for v, cn in a.variable_count if v == t), sum(cn for v, cn in a.variable_count if v == z))
    for f in fields:
        atoms[f] = (f, 0, 0)
    items = list(atoms.items())
    syms = [sp.Symbol(f'S{i}') for i in range(len(items))]
    rep = {a: s for (a, _), s in zip(items, syms)}
    Ls = sp.expand(L2.xreplace({a: rep[a] for a in sorted(rep, key=lambda q: -sp.count_ops(q))}))
    idx = {f: i for i, f in enumerate(fields)}
    M = sp.zeros(len(fields), len(fields))
    fac = lambda nt, nzz: (-sp.I * w) ** nt * (sp.I * k) ** nzz
    for mon, cf in sp.Poly(Ls, *syms).terms():
        ids = [i for i, e in enumerate(mon) for _ in range(e)]
        if len(ids) != 2:
            raise ValueError("non-quadratic term in L2")
        (fa, ta, za), (fb, tb, zb) = items[ids[0]][1], items[ids[1]][1]
        M[idx[fb], idx[fa]] += cf * fac(ta, za) * sp.conjugate(fac(tb, zb))
    return ((M + M.H) / 2).applyfunc(sp.expand)


def heat_terms(n):
    ws = [Fn(f'w{j}') for j in range(n + 1)]
    ls = [Fn(f'l{j}') for j in range(n)]
    lam0 = Fn('lam0')
    Lh = sum(ls[j] * ((ws[j + 1] - ws[j]) - dz * sp.diff(ws[j + 1], z, 2)) for j in range(n))   # Int dz L (d_z W - Lap W), implicit Euler
    Lh += lam0 * (ws[0] - u) + 2 * Cs * sp.diff(ws[-1], z) ** 2                                   # lambda_0 (W_0 - U) + MOND tangent on W_b
    return Lh, ws + ls + [lam0], [f'w{j}' for j in range(n + 1)] + [f'l{j}' for j in range(n)] + ['lam0']


P("\n  building the second-order ADM Lagrangian from the action ...")
L1, L2 = adm_L2()
M_base = fourier_matrix(L2, BASE)
P(f"  done ({time.time() - T0:.1f} s); first-order part (must be a total derivative): {sp.simplify(L1)}")

# ================================================================================================ K0
banner("K0  CONTROL: the quadratic action is the correct gauge-invariant one (linearised spatial diffeomorphisms)")


def gvec(pairs, names):
    v = sp.zeros(len(names), 1)
    for nm, val in pairs:
        v[names.index(nm)] = val
    return v


gauge = {'xi_x': [('Hxz', sp.I * k), ('nx', -sp.I * w)], 'xi_y': [('Hyz', sp.I * k), ('ny', -sp.I * w)],
         'xi_z': [('Hzz', 2 * sp.I * k), ('nz', -sp.I * w)]}
g_ok = {g: (M_base * gvec(p, BASEN)).applyfunc(sp.simplify) == sp.zeros(len(BASEN), 1) for g, p in gauge.items()}
from sympy.calculus.euler import euler_equations
l1_td = all(sp.simplify(e_.lhs) == 0 for e_ in euler_equations(L1, BASE, [t, z]))    # a total derivative <=> every EL derivative vanishes
check("K0 CONTROL the second-order ADM Lagrangian built from the action is invariant under xi_x, xi_y, xi_z (M v_xi = 0 "
      "exactly) and its first-order part is a total derivative",
      f"M v_xi = 0: {g_ok}; L1 = {sp.simplify(L1)}", all(g_ok.values()) and l1_td)

# gauge fixing (complete, algebraic): H_xz = H_yz = H_zz = 0
KEEP = [i for i, nm in enumerate(BASEN) if nm not in ('Hxz', 'Hyz', 'Hzz')]
Mg = M_base.extract(KEEP, KEEP); NG = [BASEN[i] for i in KEEP]
TENS, VECT, SCAL = ['hp', 'hc'], ['nx', 'ny'], ['hs', 'phi', 'nz', 'u']
blk = lambda M, nm, names: M.extract([nm.index(q) for q in names], [nm.index(q) for q in names])
MS0 = blk(Mg, NG, SCAL)                                    # scalar block, no MOND tangent yet
MS = MS0.copy(); MS[3, 3] += 2 * Cs * k ** 2               # continuum form: tangent C_eff on U (filter absorbed, B2)
Ce = sp.Symbol('C_e', real=True)
MSe = MS.subs(Cs, Ce)

# ================================================================================================ K1
banner("K1  CONTROL: the published BPS healthy extension (no MOND sector)")
MT = blk(Mg, NG, TENS); MV = blk(Mg, NG, VECT)
detT = sp.factor(MT.det()); detV = sp.factor(MV.det())
cT2 = sp.solve(sp.Eq(MT[0, 0], 0), w ** 2) if False else sp.solve(MT[0, 0].subs(w, sp.sqrt(sp.Symbol('W'))), sp.Symbol('W'))
M_bps = MS0.subs(cCH, 0)                                   # U decouples; its row is zero -> drop it
M_bps = M_bps.extract([0, 1, 2], [0, 1, 2])
Wsym = sp.Symbol('W')
cs2 = sp.solve(M_bps.det().subs(w, sp.sqrt(Wsym)), Wsym)
cs2_pub = xiB * (lamB - 1) * (2 * xiB - eta) * k ** 2 / (eta * (3 * lamB - 1))
# static G_N: source rho couples to the lapse phi (-rho phi); GR (eta = 0, xi = 1) normalises
rho = sp.Symbol('rho')
Mstat = M_bps.subs(w, 0)
sol_stat = Mstat.LUsolve(sp.Matrix([0, rho / 2, 0]))
phi_stat = sp.simplify(sol_stat[1])
gn_ratio = sp.simplify(phi_stat / phi_stat.subs({xiB: 1, eta: 0}))
k1_ok = (cT2 and sp.simplify(cT2[0] - xiB * k ** 2) == 0 and len(cs2) == 1 and sp.simplify(cs2[0] - cs2_pub) == 0
         and sp.simplify(gn_ratio - 1 / (xiB - eta / 2)) == 0 and sp.simplify(MT[0, 0].coeff(w, 2) - sp.Rational(1, 2)) == 0)
check("K1 CONTROL the machine reproduces BPS: c_T^2 = xi_B, c_s^2 = xi_B(lambda_B - 1)(2 xi_B - eta)/(eta(3 lambda_B - 1)), "
      "G_N/G = 1/(xi_B - eta/2), positive tensor kinetic term",
      f"c_T^2 k^2 = {cT2}; c_s^2 k^2 = {[sp.factor(s_) for s_ in cs2]}; G_N/G = {gn_ratio}; det(vector) = {detV}", k1_ok)
OUT["numbers"]["K1"] = {"cT2": str(cT2), "cs2": str(cs2), "GN_over_G": str(gn_ratio)}

# ================================================================================================ K2
banner("K2  CONTROL: L340 H1's committed static zero set and static gain, at the record's action (c_CH = 2)")
CORE = {xiB: 1, lamB: 1 + c2, eta: ac}
MSc2 = MSe.subs(CORE).subs(cCH, 2)
det0 = sp.factor(MSc2.det().subs(w, 0))
Cz = sp.solve(det0, Ce)
j340 = json.load(open(os.path.join(REPO, "real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json")))
det0_340 = sp.sympify(j340["numbers"]["H1"]["det0"], locals={"c_2": c2, "k": k, "C": Ce, "alpha_c": ac})
Cz340 = sp.solve(det0_340, Ce)
sol_s = MSc2.subs(w, 0).LUsolve(sp.Matrix([0, rho / 2, 0, 0]))
gain = sp.factor(sp.simplify(sol_s[1] / sol_s[1].subs({Ce: 0, ac: 0})))
gain340 = (1 + Ce) / (1 - ac * (1 + Ce) / 2)
k2_ok = (len(Cz) == 1 and len(Cz340) == 1 and sp.simplify(Cz[0] - Cz340[0]) == 0 and sp.simplify(gain - gain340) == 0)
check("K2 CONTROL det M(0) vanishes exactly where L340's committed det0 does (alpha_c(1 + C) = 2), and the static lapse "
      "gain is L340's (1 + C)/(1 - alpha_c(1 + C)/2)",
      f"this lane: det M(0) = {det0}, zero at C = {Cz}; L340 (committed): C = {Cz340}; gain = {gain}", k2_ok)

# ================================================================================================ K3
banner("K3  CONTROL: FRW minisuperspace -- the plain K^2 and the leaf average")
tt = sp.Symbol('t')
aF = sp.Function('a', positive=True)(tt); NF = sp.Function('N', positive=True)(tt)
Lam_, kap4 = sp.symbols('Lambda kappa_4', positive=True)
rho_m = sp.Function('rho_m', positive=True)(aF)
Hn = sp.diff(aF, tt) / (aF * NF)                          # K_ij = a adot delta_ij / N ; K = 3 adot/(a N)
KijKij, Ktr_F = 3 * Hn ** 2, 3 * Hn


def frw_H2(leaf_avg):
    lam_term = 0 if leaf_avg else c2 * Ktr_F ** 2      # (K - <K>)^2 = 0 on a homogeneous leaf
    L = NF * aF ** 3 * (KijKij - Ktr_F ** 2 - lam_term - 2 * Lam_) - 2 * kap4 * NF * aF ** 3 * rho_m
    EN = sp.diff(L, NF)                                  # the lapse equation (no N-dot anywhere: a constraint)
    Hsq = sp.Symbol('Hsq', positive=True)
    return sp.solve(sp.simplify(EN.subs(NF, 1).subs(sp.diff(aF, tt), aF * sp.sqrt(Hsq))), Hsq)[0]


H2_plain, H2_leaf = sp.simplify(frw_H2(False)), sp.simplify(frw_H2(True))
gcos_plain = sp.simplify(H2_plain / H2_leaf)
k3_ok = (sp.simplify(H2_leaf - (Lam_ + kap4 * rho_m) / 3) == 0 and sp.simplify(gcos_plain - 1 / (1 + sp.Rational(3, 2) * c2)) == 0)
check("K3 CONTROL on FRW the plain -c_2 K^2 gives H^2 (1 + 3c_2/2) = (Lambda + 8 pi G rho)/3 (L350 G1) and the leaf "
      "average gives GR's Friedmann equation (L350 G5 / CV2 B3)",
      f"leaf average: 3H^2 = {sp.simplify(3 * H2_leaf)}; plain: H^2/H^2_leaf = {gcos_plain}", k3_ok)

# ================================================================================================ A1
banner("A1  THE VELOCITY CONTENT IN UNITARY GAUGE (covariant definitions on generic polynomial fields, exact)")
tq, xq, yq, zq = sp.symbols('t x y z', real=True); X4 = [tq, xq, yq, zq]
R_ = sp.Rational
Nq = 1 + R_(1, 7) * tq * xq + R_(1, 11) * xq ** 2 + R_(1, 13) * tq ** 2
Nxq = R_(1, 5) * tq + R_(1, 9) * xq ** 2 - R_(1, 17) * tq * xq
Nyq = R_(1, 19) * xq - R_(1, 23) * tq * xq ** 2
hq = sp.Matrix([[1 + R_(1, 3) * xq ** 2 + R_(1, 29) * tq * xq, R_(1, 31) * tq + R_(1, 37) * xq, 0],
                [R_(1, 31) * tq + R_(1, 37) * xq, 1 + R_(1, 41) * tq ** 2 + R_(1, 43) * xq, 0],
                [0, 0, 1 + R_(1, 47) * tq * xq ** 2]])
hqi = hq.inv()
Nupq = sp.Matrix([Nxq, Nyq, 0]); Ndnq = hq * Nupq
g4 = sp.zeros(4, 4); g4[0, 0] = -Nq ** 2 + (Nupq.T * Ndnq)[0]
gi4 = sp.zeros(4, 4); gi4[0, 0] = -1 / Nq ** 2
for i in range(3):
    g4[0, i + 1] = g4[i + 1, 0] = Ndnq[i]
    gi4[0, i + 1] = gi4[i + 1, 0] = Nupq[i] / Nq ** 2
    for j in range(3):
        g4[i + 1, j + 1] = hq[i, j]
        gi4[i + 1, j + 1] = hqi[i, j] - Nupq[i] * Nupq[j] / Nq ** 2
PTS = [{tq: R_(1, 3), xq: R_(2, 5)}, {tq: R_(-3, 7), xq: R_(5, 4)}, {tq: R_(2, 1), xq: R_(-1, 6)}]
inv_ok = all(sp.simplify((g4 * gi4).subs(p_) - sp.eye(4)) == sp.zeros(4, 4) for p_ in PTS)
dg = [[[sp.diff(g4[a_, b_], X4[c_]) for c_ in range(4)] for b_ in range(4)] for a_ in range(4)]
Gm = [[[sum(gi4[l, r] * (dg[r][m][n] + dg[r][n][m] - dg[m][n][r]) for r in range(4)) / 2 for n in range(4)] for m in range(4)]
      for l in range(4)]
ndn = [-Nq, 0, 0, 0]                                                   # n_m = -d_m tau/sqrt(X) at tau = t
nup = [sum(gi4[m, a_] * ndn[a_] for a_ in range(4)) for m in range(4)]
hup = [[gi4[m, n] + nup[m] * nup[n] for n in range(4)] for m in range(4)]
Dn = [[sp.diff(ndn[b_], X4[a_]) - sum(Gm[l][a_][b_] * ndn[l] for l in range(4)) for b_ in range(4)] for a_ in range(4)]
acc = [sum(nup[a_] * Dn[a_][b_] for a_ in range(4)) for b_ in range(4)]
a2cov = sum(acc[b_] * sum(gi4[m, b_] * acc[m] for m in range(4)) for b_ in range(4))
lnNq = sp.log(Nq)
a2adm = sum(hqi[i, j] * sp.diff(lnNq, X4[i + 1]) * sp.diff(lnNq, X4[j + 1]) for i in range(3) for j in range(3))
Kcov = sum(gi4[a_, b_] * Dn[a_][b_] for a_ in range(4) for b_ in range(4))
X3 = [xq, yq, zq]
G3 = lambda kk, a_, b_: sum(hqi[kk, l] * (sp.diff(hq[l, a_], X3[b_]) + sp.diff(hq[l, b_], X3[a_]) - sp.diff(hq[a_, b_], X3[l]))
                            for l in range(3)) / 2
D3N = lambda i, j: sp.diff(Ndnq[j], X3[i]) - sum(G3(kk, i, j) * Ndnq[kk] for kk in range(3))
Kadm = sum(hqi[i, j] * (sp.diff(hq[i, j], tq) - D3N(i, j) - D3N(j, i)) / (2 * Nq) for i in range(3) for j in range(3))
Uq = R_(1, 3) * tq ** 2 + R_(2, 7) * tq * xq + R_(1, 5) * xq ** 3        # a U with Udot != 0
hdU = sum(hup[m][n] * sp.diff(Uq, X4[m]) * sp.diff(Uq, X4[n]) for m in range(4) for n in range(4))
hdUadm = sum(hqi[i, j] * sp.diff(Uq, X4[i + 1]) * sp.diff(Uq, X4[j + 1]) for i in range(3) for j in range(3))
Fq = R_(1, 2) * tq ** 2 * xq + R_(3, 5) * xq ** 2 - R_(1, 7) * tq ** 3
nn2 = [[sp.diff(Fq, X4[a_], X4[b_]) - sum(Gm[l][a_][b_] * sp.diff(Fq, X4[l]) for l in range(4)) for b_ in range(4)] for a_ in range(4)]
Lapcov = sum(hup[a_][b_] * nn2[a_][b_] for a_ in range(4) for b_ in range(4)) + Kcov * sum(nup[a_] * sp.diff(Fq, X4[a_]) for a_ in range(4))
shq = sp.sqrt(hq.det())
Lapadm = sum(sp.diff(shq * sum(hqi[i, j] * sp.diff(Fq, X4[j + 1]) for j in range(3)), X4[i + 1]) for i in range(3)) / shq
nnorm = sum(ndn[a_] * nup[a_] for a_ in range(4))
res = {}
for nm_, e_ in (("n.n + 1", nnorm + 1), ("a^2 - ADM", a2cov - a2adm), ("K - ADM", Kcov - Kadm),
                ("h dU dU - ADM", hdU - hdUadm), ("Delta_h identity", Lapcov - Lapadm)):
    res[nm_] = max(abs(complex(sp.N(e_.subs(p_), 40))) for p_ in PTS)
a1_ok = inv_ok and all(v_ < 1e-30 for v_ in res.values())
check("A1 in unitary gauge (tau = t) the covariant pieces are the manifestly velocity-free ADM expressions: n.n = -1, a^2 = "
      "h^ij d_i lnN d_j lnN, h^mn dU dU = h^ij d_iU d_jU (no Udot), Delta_h F has no Fdot, and K enters through hdot_ij only",
      f"max residual over 3 exact points: {', '.join(f'{k_}: {v_:.1e}' for k_, v_ in res.items())}; inverse metric exact {inv_ok}",
      a1_ok)
P("    => velocities: hdot_ij only.  N, N^i, U, W(z), L(z), lambda_0 carry none: primary constraints pi_N, pi_{N^i}, pi_U, pi_W(z), "
  "pi_L(z), pi_lambda0 ~ 0.")

# ================================================================================================ A2
banner("A2  THE LEGENDRE MAP (DeWitt kinetic form, leaf average mode by mode)")
Kc = sp.symbols('K11 K22 K33 K12 K13 K23', real=True)
lam = sp.Symbol('lambda', real=True)
Km = sp.Matrix([[Kc[0], Kc[3], Kc[4]], [Kc[3], Kc[1], Kc[5]], [Kc[4], Kc[5], Kc[2]]])
Lkin = sum(Km[i, j] ** 2 for i in range(3) for j in range(3)) - lam * Km.trace() ** 2
Hk = sp.hessian(Lkin, Kc)
ev = {sp.simplify(e_): m_ for e_, m_ in Hk.eigenvals().items()}
# the leaf average on a periodic leaf: -c2 (K - <K>)^2 removes exactly the k = 0 part of -c2 K^2 (Parseval), numerically
rng = np.random.default_rng(5)
Kx = rng.normal(size=256) + 0.7
lhs = np.mean((Kx - Kx.mean()) ** 2); Kh = np.fft.fft(Kx) / Kx.size
rhs = np.sum(np.abs(Kh[1:]) ** 2)
lam_k = {"k != 0": 1 + c2, "k = 0": 1}
detK = {kk: sp.factor(Hk.subs(lam, v_).det()) for kk, v_ in lam_k.items()}
a2_ok = (ev.get(2) == 2 and ev.get(4) == 3 and any(sp.simplify(e_ - 2 * (1 - 3 * lam)) == 0 for e_ in ev)
         and abs(lhs - rhs) < 1e-12 and sp.simplify(detK["k = 0"]) != 0 and sp.solve(detK["k != 0"], c2) == [sp.Rational(-2, 3)])
check("A2 the kinetic Hessian of K_ij K^ij - lambda K^2 (independent components) is positive on the traceless part "
      "(eigenvalues 2 x2 diagonal, 4 x3 off-diagonal) and 2(1 - 3 lambda) on the trace; the leaf average removes exactly the "
      "k = 0 part of c_2 K^2, so lambda = 1 + c_2 on k != 0 and 1 on k = 0: the Legendre map is invertible on every mode "
      "unless c_2 = -2/3",
      f"eigenvalues {ev}; Parseval |lhs - rhs| = {abs(lhs - rhs):.1e}; det(k=0) = {detK['k = 0']}; det(k!=0) = {detK['k != 0']}",
      a2_ok)

# ================================================================================================ A3
banner("A3  THE AUXILIARY SECTOR IS SECOND CLASS (heat block, (N, U) block, Dirac bookkeeping)")
heat_det, schur_ok = {}, {}
for n in (1, 2, 3, 4):
    Lh, hf, hn = heat_terms(n)
    Mn = fourier_matrix(L2 + Lh, BASE + hf)
    names = BASEN + hn
    keep = [i for i, nm in enumerate(names) if nm not in ('Hxz', 'Hyz', 'Hzz')]
    Mn = Mn.extract(keep, keep); nms = [names[i] for i in keep]
    Aix = [nms.index(q) for q in SCAL]; Bix = [nms.index(q) for q in hn]
    MBB = Mn.extract(Bix, Bix)
    heat_det[n] = sp.factor(MBB.det())
    Meff = (Mn.extract(Aix, Aix) - Mn.extract(Aix, Bix) * MBB.LUsolve(Mn.extract(Aix, Bix).H)).applyfunc(sp.simplify)
    tgt = MS0.copy(); tgt[3, 3] += 2 * Cs * k ** 2 * (1 + dz * k ** 2) ** (-2 * n)
    schur_ok[n] = (Meff - tgt).applyfunc(sp.simplify) == sp.zeros(4, 4)
    OUT["numbers"].setdefault("A3_heat_det", {})[n] = str(heat_det[n])
heat_free = all(not heat_det[n].has(Cs) and heat_det[n] != 0 for n in heat_det)
# (N, U) Hessian = the (phi, u) block of the scalar matrix at fixed canonical data
HNU = MSe.subs(CORE).extract([1, 3], [1, 3])
detNU = sp.factor(HNU.det())
Cg = np.logspace(-8, 12, 400)
nu_range_ok = all(float(detNU.subs({k: 1, cCH: C_CH, ac: a_, Ce: c_})) > 0 for a_ in (9.6e-14, 3.2e-9) for c_ in Cg[::20])
nU_zero = sp.factor(detNU.subs(Ce, 0))
# Dirac bookkeeping per point with n heat points
nh = sp.Symbol('n', positive=True, integer=True)
dimP = 12 + 2 + 6 + 2 + 2 * (nh + 1) + 2 * nh + 2
N_FC, N_SC = 6, 2 + 2 + 2 * (nh + 1) + 2 * nh + 2
Nphys = sp.simplify((dimP - 2 * N_FC - N_SC) / 2)
a3_ok = heat_free and all(schur_ok.values()) and nu_range_ok and Nphys == 3
check("A3 the heat block (W, L, lambda_0) has a kernel-independent determinant (1 + Dz k^2)^(2n)/4^(n+1) (nonzero) for n = 1-4, "
      "so its pairs are second class; the (N, U) Hessian det is > 0 on nu_mono's range (C > 0) at both alpha_c ends; "
      "Dirac count (12 + 2 + 6 + 2 + 2(n+1) + 2n + 2 - 2 x 6 - (8 + 4n))/2 = 3 for every n",
      f"heat det: {', '.join(f'n={n}: {heat_det[n]}' for n in heat_det)}; det(N,U) = {detNU} (at C = 0: {nU_zero}); "
      f"N_phys = {Nphys}", a3_ok)
aminL = j340["numbers"]["H4"]
alpha_min = max(v_["alpha_min"] for v_ in aminL.values() if isinstance(v_, dict) and "alpha_min" in v_)
P(f"    note: at C -> 0 the (N, U) determinant is alpha_c c_CH k^4, so its positivity against the O(Phi/c^2) clock terms "
  f"needs alpha_c >= alpha_min = {alpha_min:.2e} (L340 H4, committed) -- inherited, inside the window.")

# ================================================================================================ B1
banner("B1  THE COUNT: det M(w, k) degrees, explicit heat points, random draws")
rnd = random.Random(20260926)
rows_b1 = []
for n in (1, 2, 3, 4):
    Lh, hf, hn = heat_terms(n)
    Mn = fourier_matrix(L2 + Lh, BASE + hf)
    names = BASEN + hn
    keep = [i for i, nm in enumerate(names) if nm not in ('Hxz', 'Hyz', 'Hzz')]
    Mn = Mn.extract(keep, keep); nms = [names[i] for i in keep]
    S_ = [nms.index(q) for q in SCAL + hn]; T_ = [nms.index(q) for q in TENS]; V_ = [nms.index(q) for q in VECT]
    off = all(Mn[i, j] == 0 for grp in (T_, V_, S_) for i in grp for j in range(len(nms)) if j not in grp)
    for draw in range(4):
        vals = {xiB: 1, lamB: 1 + sp.Rational(rnd.randint(1, 90), 1000), eta: sp.Rational(rnd.randint(1, 900), 1000),
                cCH: C_CH, Cs: sp.Rational(rnd.randint(1, 5000), 97), dz: sp.Rational(rnd.randint(1, 50), 211),
                k: sp.Rational(rnd.randint(20, 300), 100)}
        if draw == 3:                                   # the physical corner: alpha_c ~ 1e-9, deep-MOND tangent, Planck-cap c_2
            vals.update({eta: sp.Rational(1, 10 ** 9), Cs: sp.Integer(10 ** 6), lamB: 1 + sp.Rational(63, 100000)})
        degs = []
        for grp in (T_, V_, S_):
            dd = sp.expand(Mn.extract(grp, grp).subs(vals).det(method='berkowitz'))
            degs.append(sp.Poly(dd, w).degree() if dd != 0 else -1)
        rows_b1.append((n, draw, degs, off))
b1_ok = all(r[2] == [4, 0, 2] and r[3] for r in rows_b1)
for r in rows_b1[::3]:
    P(f"    n = {r[0]} heat points: deg_w det (tensor, vector, scalar) = {r[2]} (blocks decoupled: {r[3]})")
check("B1 for 1-4 explicit heat points, 3 random parameter draws plus the physical corner (alpha_c = 1e-9, C = 1e6, c_2 = "
      "6.3e-4) each: deg_w det = 4 (tensor) + 0 (vector, det != 0) + 2 "
      "(scalar), det not identically zero => N = 3: two tensor modes and one khronon scalar, no vector mode",
      f"{len(rows_b1)} cases, all degrees [4, 0, 2]: {b1_ok}", b1_ok)
OUT["numbers"]["B1"] = [{"n": r[0], "degs": r[2]} for r in rows_b1]

# ================================================================================================ B2
banner("B2  WHAT THE NONLOCAL FILTER ADDS: nothing but the tangent's filter factor")
bb, kk_ = 0.5, np.array([0.3, 1.0, 2.0, 3.0])
conv = {nn: float(np.max(np.abs((1 + bb * kk_ ** 2 / nn) ** (-nn) / np.exp(-bb * kk_ ** 2) - 1))) for nn in (4, 64, 4096, 262144)}
b2_ok = all(schur_ok.values()) and conv[262144] < 1e-4 and conv[262144] < conv[4096] < conv[64] < conv[4]
check("B2 the Schur complement of the heat block equals the continuum scalar block with C -> sigma_n(k)^2 C, sigma_n = "
      "(1 + b k^2/n)^(-n) -> exp(-b k^2) = exp(-xi^2 k^2/2) (both filters, S and S^dagger): the filter adds no mode, no "
      "free data and no first-class constraint",
      f"Schur == sigma_n^2 C for n = 1-4: {schur_ok}; max |sigma_n/exp(-bk^2) - 1| at b = 0.5: {conv}", b2_ok)

# ================================================================================================ B3
banner("B3  THE REDUCED KHRONON: no ghost, its dispersion, c_T = 1")
MSc = MSe.subs(CORE)
detS = sp.factor(MSc.det())
Psc = sp.Poly(sp.expand(detS), w)
Wr = sp.solve(detS.subs(w, sp.sqrt(Wsym)), Wsym)
E_C = ac + 2 * Ce * cCH / (cCH + 2 * Ce)
disp_t = c2 * (2 - E_C) * k ** 2 / (E_C * (2 + 3 * c2))
disp_ok = len(Wr) == 1 and sp.simplify(Wr[0] - disp_t) == 0
# kinetic coefficient of the reduced scalar (Schur complement onto hs at fixed k)
red = sp.simplify(MSc[0, 0] - (MSc.extract([0], [1, 2, 3]) * MSc.extract([1, 2, 3], [1, 2, 3]).inv()
                                * MSc.extract([1, 2, 3], [0]))[0, 0])
kin = sp.factor(sp.expand(red).coeff(w, 2))
kin_ok = sp.simplify(kin - (2 + 3 * c2) / (2 * c2)) == 0
Eform = sp.simplify(((MSc[1, 1] - MSc[1, 3] ** 2 / MSc[3, 3]) / k ** 2))
Eform_ok = sp.simplify(Eform - E_C) == 0
tens_ok = sp.simplify(detT.subs(xiB, 1) - (w ** 2 - k ** 2) ** 2 / 4) == 0
check("B3 the reduced khronon has kinetic coefficient (2 + 3c_2)/(2c_2) > 0 for c_2 > 0 (no ghost) and w^2 = c_2(2 - E)k^2/"
      "(E(2 + 3c_2)), E(C) = alpha_c + 2 C c_CH/(c_CH + 2C): the C-H sector renormalises the BPS alpha; tensors: det = "
      "(w^2 - k^2)^2/4, c_T = 1",
      f"kinetic = {kin}; w^2 = {sp.factor(Wr[0]) if Wr else None}; E(C) from the Schur complement = {Eform}; tensor det = {detT.subs(xiB, 1)}",
      disp_ok and kin_ok and Eform_ok and tens_ok)
OUT["numbers"]["B3"] = {"kinetic": str(kin), "omega2": str(Wr), "E": str(Eform)}

# ================================================================================================ B4
banner("B4  THE EXCEPTIONAL SURFACES (rank changes), located symbolically")
lead = sp.factor(Psc.coeff_monomial(w ** 2))
d_E0 = sp.expand(detS.subs({ac: 0, Ce: 0}))
d_c20 = sp.factor(detS.subs(c2, 0))
d_l13 = sp.expand(detS.subs(c2, sp.Rational(-2, 3)))
E2_root = sp.simplify(disp_t.subs(Ce, sp.solve(sp.Eq(E_C, 2), Ce)[0])) if sp.solve(sp.Eq(E_C, 2), Ce) else None
cases = {"E = 0 (alpha_c = C = 0)": sp.Poly(d_E0, w).degree() if d_E0 != 0 else -1,
         "lambda = 1/3 (c_2 = -2/3)": sp.Poly(d_l13, w).degree() if d_l13 != 0 else -1}
frozen = sp.simplify(d_c20 / w ** 2).has(w) is False and d_c20.has(w)
b4_ok = cases["E = 0 (alpha_c = C = 0)"] == 0 and cases["lambda = 1/3 (c_2 = -2/3)"] == 0 and frozen and E2_root == 0
check("B4 the only rank changes: E = 0 (the lapse becomes a multiplier, the scalar is lost: deg 0), lambda = 1/3 (deg 0), "
      "c_2 = 0 (det ~ w^2: the frozen mode, L340 H1's control), E = 2 (w = 0: the static-gain pole); nu_mono's C > 0 "
      "keeps 1 + C > 0 and E >= alpha_c > 0 everywhere a field exists",
      f"leading coefficient = {lead}; degrees at E = 0 / lambda = 1/3: {cases}; c_2 = 0: det = {d_c20}; w^2 at E = 2: {E2_root}",
      b4_ok)

# ================================================================================================ C1
banner("C1  THE NONZERO-FIELD BRANCH: where is 0 < E < 2 (nu_mono, both directions, both alpha_c ends)")
Cstar_expr = sp.solve(sp.Eq(E_C, 2), Ce)
AC_ENDS = {"alpha_min (L340 H4)": float(j340["numbers"]["P1"]["alpha_c_min"]), "alpha_c max (L340 P1)": float(j340["numbers"]["P1"]["alpha_c_max"])}
E_num = lambda C_, a_: a_ + 2 * C_ * float(C_CH) / (float(C_CH) + 2 * C_)
ystar = {}
for lab, a_ in AC_ENDS.items():
    cst = [float(s_.subs({ac: sp.Rational(a_), cCH: C_CH})) for s_ in Cstar_expr]     # exact: c_CH - 2 + alpha cancels in floats
    cst = [c_ for c_ in cst if c_ > 0]
    for dname, Cf in (("T", CT), ("L", CL)):
        if not cst:
            ystar[(lab, dname)] = None
            continue
        f = lambda ly: Cf(10 ** ly) - cst[0]
        ystar[(lab, dname)] = 10 ** brentq(f, -80, 0, xtol=1e-12)
xr3 = rd("real_research/cross_thread_review_2026_09_26/XR3_checks.out") or ""
xr3_T = [float(v_) for v_ in re.findall(r"transverse N = 0 at y = ([0-9.e+-]+)", xr3)]
ys_grid = np.logspace(-15, 12, 541)
Emin, Emax = 10.0, -10.0
for a_ in AC_ENDS.values():
    for yv in ys_grid:
        for Cf in (CT, CL):
            e_ = E_num(Cf(yv), a_); Emin = min(Emin, e_); Emax = max(Emax, e_)
for (lab, dname), yv in ystar.items():
    if yv is not None:
        P(f"    {lab:24s} {dname}: E crosses 2 at y* = {yv:.4e}  ->  g* = {yv * A0['canonical']:.3e} (canonical) / "
          f"{yv * A0['alt']:.3e} m/s^2 (alt)")
    else:
        P(f"    {lab:24s} {dname}: E never reaches 2 (no crossing)")
P(f"    over y in [1e-15, 1e12] (both directions, both alpha_c ends): E in [{Emin:.3e}, {Emax:.9f}]")
y1e3 = CT(1e-3); Eg = E_num(y1e3, AC_ENDS["alpha_c max (L340 P1)"])
P(f"    context (not this gate): a linear cosmological perturbation at y ~ 1e-3 has E_T = {Eg:.4f}, static gain "
  f"1/(1 - E/2) = {1 / (1 - Eg / 2):.1f} -- the ungated core's growth excess (L341)")
ok_c1 = (all(v_ is not None for v_ in ystar.values()) and len(xr3_T) == 2
         and abs(ystar[("alpha_min (L340 H4)", "T")] / xr3_T[0] - 1) < 0.01 and abs(ystar[("alpha_c max (L340 P1)", "T")] / xr3_T[1] - 1) < 0.01
         and 0 < Emin and Emax < 2)
check("C1 on the nonzero-field branch the khronon is healthy (0 < E < 2) for every field above g* = y* a0; y*_T reproduces XR3 "
      "K4's committed values (2.316e-27, 2.560e-18) to < 1%; E stays in (0, 2) over y = 1e-15 .. 1e12",
      f"y*_T = {ystar[('alpha_min (L340 H4)', 'T')]}, {ystar[('alpha_c max (L340 P1)', 'T')]} vs XR3 {xr3_T}; "
      f"E range {Emin:.2e} .. {Emax:.9f}", ok_c1)
OUT["numbers"]["C1"] = {f"{a}|{d}": v_ for (a, d), v_ in ystar.items()}

# ================================================================================================ C2
banner("C2  ZERO FIELD, the exact leaf problem at fixed lapse (1-D, nu_mono): U is pinned, the lapse feels the C-H term")
hv = np.vectorize(h_mono)
cCHf = float(C_CH)


def leaf_solve(e_, g0, npts=256):
    x_ = (np.arange(npts) + 0.5) * 2 * np.pi / npts
    dphi = -e_ * np.sin(x_); phip = g0 + dphi

    def p_of(mu):
        lo = np.full(npts, -10.0 * (abs(g0) + abs(e_) + 1)); hi = -lo
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            f = 2 * cCHf * (mid - phip) + 4 * np.sign(mid) * hv(np.abs(mid)) - mu
            lo = np.where(f < 0, mid, lo); hi = np.where(f >= 0, mid, hi)
        return 0.5 * (lo + hi)
    if g0 == 0:
        mu = 0.0
    else:
        mu0 = 4 * h_mono(g0); span = 4 * e_ * (cCHf + 4)
        mu = brentq(lambda m_: p_of(m_).mean() - g0, mu0 - span, mu0 + span, xtol=1e-15)
    p = p_of(mu); dp = p - g0
    dH = np.array([H_mono(abs(pi)) if g0 == 0 else quad(h_mono, g0, pi, epsabs=0, epsrel=1e-12)[0] for pi in p])
    dE = (cCHf * (dp - dphi) ** 2 + 4 * dH).mean()
    return float(np.abs(dp).max()), float(dE / (cCHf * (dphi ** 2).mean()))


pin = {}
for g0 in (0.0, 0.01, 1.0):
    es = (1e-2, 1e-3, 1e-4, 1e-5, 1e-6) if g0 == 0 else (1e-3, 1e-4, 1e-5)
    rows = [(e_,) + leaf_solve(e_, g0) for e_ in es]
    sl = float(np.polyfit(np.log([r[0] for r in rows]), np.log([r[1] for r in rows]), 1)[0])
    Rexp = 1.0 if g0 == 0 else 2 * CL(g0) / (cCHf + 2 * CL(g0))
    pin[g0] = dict(slope=sl, R=[r[2] for r in rows], R_expected=Rexp)
    P(f"    background y0 = {g0:<5g}: |dU'| slope {sl:.3f};  R = " + ", ".join(f"{r[2]:.6f}" for r in rows)
      + f"   (expected -> {Rexp:.6f})")
xc5 = json.load(open(os.path.join(REPO, "real_research/extra_crispy_2026/XC5_lapse_weighted_convexity_results.json")))
xc5_slope = xc5["numbers"]["E6"]["rows"]["nu_mono"]["slope"]
sq = [h_mono(e_) for e_ in (1e-4, 1e-6, 1e-8)]
sq_slope = float(np.polyfit(np.log([1e-4, 1e-6, 1e-8]), np.log(sq), 1)[0])
c2_ok = (abs(pin[0.0]["slope"] - 2) < 0.02 and abs(pin[0.0]["R"][-1] - 1) < 1e-5
         and all(abs(pin[g]["slope"] - 1) < 0.01 and abs(pin[g]["R"][-1] / pin[g]["R_expected"] - 1) < 1e-4 for g in (0.01, 1.0))
         and abs(xc5_slope + 0.5) < 0.01 and abs(sq_slope - 0.5) < 0.01)
check("C2 at an open zero-field region the leaf problem pins U (|dU'| ~ eps^2) and the lapse feels the full C-H coefficient "
      "(R -> 1: the C = inf member of the frozen family); at a nonzero field the response is linear (slope 1) with R = "
      "2C_L/(c_CH + 2C_L); the phantom's source response h(eps) ~ eps^(1/2) is the other face (XC5 E6's committed slope -1/2)",
      f"zero field: slope {pin[0.0]['slope']:.3f}, R -> {pin[0.0]['R'][-1]:.7f}; y0 = 0.01: R {pin[0.01]['R'][-1]:.6f} vs "
      f"{pin[0.01]['R_expected']:.6f}; y0 = 1: R {pin[1.0]['R'][-1]:.6f} vs {pin[1.0]['R_expected']:.6f}; h(eps) slope "
      f"{sq_slope:.3f}; XC5 E6 slope {xc5_slope:.4f}", c2_ok)
OUT["numbers"]["C2"] = {str(k_): v_ for k_, v_ in pin.items()}

# ================================================================================================ C3
banner("C3  ZERO FIELD, the formal linearisation: BPS khronometric gravity with alpha_eff = c_CH + alpha_c")
E_inf = sp.limit(Eform.subs(cCH, C_CH), Ce, sp.oo)
c2_ends = {"Planck cap (L350)": 6.3e-4, "L340 floor": float(j340["numbers"]["P1"]["c2_min"]), "BBN ceiling": float(j340["numbers"]["P1"]["c2_max"])}
rows3 = []
w2_inf = sp.simplify(c2 * (2 - E_inf) / (E_inf * (2 + 3 * c2)))                   # exact, before any float
for la, a_ in AC_ENDS.items():
    Ei_m2 = float((E_inf - 2).subs(ac, sp.Rational(a_)))
    for lc, c2v in c2_ends.items():
        w2k2 = float(w2_inf.subs({ac: sp.Rational(a_), c2: sp.Rational(c2v)}))
        rows3.append((la, lc, Ei_m2, w2k2, math.sqrt(-w2k2) if w2k2 < 0 else 0.0))
MSm = MSe.subs(CORE).subs(cCH, C_CH).subs(w, 0)                    # this action's own static block
sol_m = MSm.LUsolve(sp.Matrix([0, rho / 2, 0, 0]))
gain_own = sp.simplify(sol_m[1] / sol_m[1].subs({Ce: 0, ac: 0}))
gain_inf = sp.simplify(sp.limit(gain_own, Ce, sp.oo))
for r in rows3:
    P(f"    {r[0]:24s} c_2 = {r[1]:18s}: E_inf - 2 = {r[2]:+.4e}; w^2/k^2 = {r[3]:+.3e}; growth rate / (k c) = {r[4]:.3e}")
P(f"    w^2/k^2 at C -> inf (exact) = {sp.factor(w2_inf)};  static gain at C -> inf: {gain_inf}")
detinf = sp.factor(sp.limit(detS.subs(cCH, C_CH) / Ce, Ce, sp.oo))            # the count survives the zero-field limit
deg_inf = sp.Poly(sp.expand(detinf), w).degree()
kin_inf = kin                                                                      # (2 + 3c_2)/(2c_2): C-independent
P(f"    zero-field limit of det/C = {detinf}  (deg_w = {deg_inf}: still 3 modes); khronon kinetic coefficient {kin_inf} "
  f"(C-independent): the zero-field failure is a gradient instability, not a ghost")
E0 = sp.limit(Eform.subs(cCH, C_CH), Ce, 0)
pincer = sp.solve([ac > 0, E_inf < 2], ac)                                         # both ends of E inside BPS's window?
P(f"    THE ALPHA-PINCER: E runs monotonically from E(C=0) = {E0} (Newtonian end) to E(C=inf) = {E_inf} (zero field); "
  f"both inside (0, 2) requires {sp.And(ac > 0, E_inf < 2)} -> solution set: {pincer}")
ill = all(r[2] > 0 and r[3] < 0 for r in rows3) and deg_inf == 2 and pincer in (False, sp.false)
check("C3 at an open zero-field region the formal linearisation is BPS khronometric gravity with alpha_eff = lim_{C->inf} E = "
      "c_CH + alpha_c > 2 (outside BPS's window 0 < alpha < 2): w^2 < 0 at every k for every (alpha_c, c_2) in the windows, "
      "growth rate proportional to k (no filter cut-off at C = inf) => Hadamard ill-posed; the ungated core has no "
      "well-posed linearisation on its own FRW background; and since E runs from alpha_c to alpha_c + c_CH, no alpha_c puts "
      "both ends inside the window (the alpha-pincer)",
      f"E_inf = {E_inf}; min over windows of -w^2/k^2 = {min(-r[3] for r in rows3):.3e}; count at C = inf: deg {deg_inf}; "
      f"all outside: {ill}", ill)
OUT["numbers"]["C3"] = {"E_inf": str(E_inf), "rows": rows3, "static_gain_inf": str(gain_inf)}

# ================================================================================================ C4
banner("C4  (reported) finite amplitude: the band is bounded below y*, and it saturates at y ~ y*")
XI_PC = {"canonical": float(j340["numbers"]["S1"]["canonical/nu_mono"]["xi_M"]), "alt": float(j340["numbers"]["S1"]["alt/nu_mono"]["xi_M"])}
c4 = []
if not MUTATE:
    a_top, c2_top = AC_ENDS["alpha_c max (L340 P1)"], c2_ends["BBN ceiling"]          # the fastest corner of the windows
    Cst = float(Cstar_expr[0].subs({ac: sp.Rational(a_top), cCH: C_CH}))
    for m_ in (2, 10, 40):
        yv = ystar[("alpha_c max (L340 P1)", "T")] * 10 ** (-m_)
        C0 = CT(yv)
        kmax_xi = math.sqrt(math.log(C0 / Cst))
        kx = np.linspace(1e-3, kmax_xi, 400)
        Ek = a_top + 2 * C0 * np.exp(-kx ** 2) / (1 + C0 * np.exp(-kx ** 2))
        gam = kx * np.sqrt(np.clip(c2_top * (Ek - 2) / (Ek * (2 + 3 * c2_top)), 0, None))
        gmax = float(gam.max())                                          # in units c/xi
        tau_yr = (XI_PC["canonical"] * PC / c_SI) / gmax / YR
        c4.append((m_, yv, kmax_xi, gmax, tau_yr))
        P(f"    y = y*/1e{m_:<3d} = {yv:.2e}: unstable band k xi < {kmax_xi:.2f}; max growth {gmax:.2e} c/xi -> e-fold "
          f"{tau_yr:.2e} yr at xi = {XI_PC['canonical']:.3f} pc")
    P(f"    saturation: once the perturbation's own field exceeds g* ~ {ystar[('alpha_c max (L340 P1)', 'T')] * A0['canonical']:.1e} m/s^2 "
      f"(canonical) E drops below 2; physical cosmological perturbations (y ~ 1e-3) never enter the band")
check("C4 (reported) below y* the unstable band is bounded (k_max xi = sqrt(ln(C/C*)), growing only logarithmically) and "
      "the instability saturates at y ~ y*: harmless in amplitude, but the exact FRW is not a perturbative background",
      f"{[(r[0], round(r[2], 2), f'{r[4]:.1e} yr') for r in c4]}", True, load_bearing=False)
OUT["numbers"]["C4"] = c4

# ================================================================================================ C6
banner("C6  (reported) the one exit from the pincer inside the core: c_CH = 2(1 - delta) -- priced, not adopted")
c6 = []
if not MUTATE:
    Ms_d = lambda cch: MSe.subs(CORE).subs(cCH, cch).subs(w, 0)
    gain_of = lambda cch: sp.simplify(Ms_d(cch).LUsolve(sp.Matrix([0, rho / 2, 0, 0]))[1] / Ms_d(2).LUsolve(sp.Matrix([0, rho / 2, 0, 0]))[1].subs({Ce: 0, ac: 0}))
    g_ref = sp.lambdify((Ce, ac), gain_of(2))
    for dl in (sp.Rational(1, 10 ** 8), sp.Rational(1, 10 ** 6), sp.Rational(1, 10 ** 4)):
        gd = sp.lambdify((Ce, ac), gain_of(2 * (1 - dl)))
        a_top = AC_ENDS["alpha_c max (L340 P1)"]
        dlog = {yv: math.log10(gd(CL(yv), a_top) / g_ref(CL(yv), a_top)) for yv in (1e-4, 1e-3, 1.0)}
        Einf_d = 2 * (1 - float(dl)) + a_top
        c6.append((float(dl), Einf_d, dlog, 1 / (float(dl) - a_top / 2) if float(dl) > a_top / 2 else float('inf')))
        P(f"    delta = {float(dl):.0e}: E_inf = 2 - {2 * float(dl) - a_top:.2e} (< 2: inside); static MOND law shift "
          + ", ".join(f"{dv:+.1e} dex at y = {yv:g}" for yv, dv in dlog.items())
          + f"; zero-field static gain 1/(delta - alpha_c/2) = {c6[-1][3]:.2e}")
    P("    reading: alpha_c/2 < delta << sqrt(y_min) keeps the RAR (the shift is ~ delta C_L ~ delta/sqrt(y)); it breaks C-H's exact"
      "\n    Newtonian normalisation of U (Delta u = 4 pi G rho holds only at c_CH = 2) and it does NOT cure the ungated growth excess"
      "\n    (E ~ 1.94 at y ~ 1e-3, L341): a new constant, recorded as the price of the only in-core exit, not adopted.")
check("C6 (reported) the pincer's in-core exit c_CH = 2(1 - delta), alpha_c/2 < delta, restores the zero-field window at a "
      "static-law cost ~ delta/sqrt(y) and leaves the growth excess: priced, not adopted",
      f"{[(r[0], round(r[1], 12), {k_: f'{v_:+.1e}' for k_, v_ in r[2].items()}) for r in c6]}", True, load_bearing=False)
OUT["numbers"]["C6"] = c6

# ================================================================================================ C5
banner("C5  THE PRINCIPAL SYMBOL off open zero-field regions (k xi -> inf): GR + BPS(alpha_c, c_2, beta = 0)")
cs_rng = []
for a_ in AC_ENDS.values():
    for c2v in (c2_ends["Planck cap (L350)"], c2_ends["BBN ceiling"]):
        cs_rng.append(math.sqrt(c2v * (2 - a_) / (a_ * (2 + 3 * c2v))))
E_princ = sp.limit(Eform.subs(cCH, C_CH), Ce, 0)
Wpr = sp.solve(detS.subs(Ce, 0).subs(w, sp.sqrt(Wsym)), Wsym)
distinct = all(v_ > 1.0 for v_ in cs_rng)
c5_ok = (sp.simplify(E_princ - ac) == 0 and len(Wpr) == 1 and sp.simplify(Wpr[0] - c2 * (2 - ac) * k ** 2 / (ac * (2 + 3 * c2))) == 0
         and distinct and tens_ok)
check("C5 at k xi -> inf (finite tangent) the filter removes the MOND block (E -> alpha_c): the principal symbol is GR + "
      "BPS with real, distinct physical cones c_T = 1 and c_s = sqrt(c_2(2 - alpha_c)/(alpha_c(2 + 3c_2))) plus an elliptic "
      "lapse => the linear frozen problem is hyperbolic-elliptic with no complex characteristic (gauge-invariant dispersion "
      "level); a strongly hyperbolic formulation of the nonlinear GR + BPS system (gauge included) stays OPEN",
      f"E(k xi -> inf) = {E_princ}; c_s/c over the windows = {min(cs_rng):.3e} .. {max(cs_rng):.3e} (XC1 A9: 4.4e2-7.9e5)", c5_ok)
OUT["numbers"]["C5"] = {"cs_over_c": [min(cs_rng), max(cs_rng)]}

# ================================================================================================ D1
banner("D1  a0 AS A FIELD -- FRW: which terms survive the homogeneous background?")
# every added term evaluated from its covariant definition on flat FRW with a free lapse N(t) and homogeneous U, W
tf = sp.Symbol('t'); af = sp.Function('a', positive=True)(tf); Nf = sp.Function('N', positive=True)(tf)
Uf, Wf = sp.Function('U')(tf), sp.Function('W')(tf)
XF = [tf] + list(sp.symbols('x1 x2 x3'))
gF = sp.diag(-Nf ** 2, af ** 2, af ** 2, af ** 2); giF = gF.inv()
dgF = [[[sp.diff(gF[a_, b_], XF[c_]) for c_ in range(4)] for b_ in range(4)] for a_ in range(4)]
GF = [[[sum(giF[l, r] * (dgF[r][m][n] + dgF[r][n][m] - dgF[m][n][r]) for r in range(4)) / 2 for n in range(4)] for m in range(4)]
      for l in range(4)]
nF_dn = [-Nf, 0, 0, 0]; nF_up = [sum(giF[m, a_] * nF_dn[a_] for a_ in range(4)) for m in range(4)]
hF = [[giF[m, n] + nF_up[m] * nF_up[n] for n in range(4)] for m in range(4)]
DnF = [[sp.diff(nF_dn[b_], XF[a_]) - sum(GF[l][a_][b_] * nF_dn[l] for l in range(4)) for b_ in range(4)] for a_ in range(4)]
accF = [sum(nF_up[a_] * DnF[a_][b_] for a_ in range(4)) for b_ in range(4)]
a2F = sp.simplify(sum(accF[b_] * sum(giF[m, b_] * accF[m] for m in range(4)) for b_ in range(4)))
KF = sp.simplify(sum(giF[a_, b_] * DnF[a_][b_] for a_ in range(4) for b_ in range(4)))
hdUF = sp.simplify(sum(hF[m][n] * sp.diff(Uf, XF[m]) * sp.diff(Uf, XF[n]) for m in range(4) for n in range(4)))
nnW = [[sp.diff(Wf, XF[a_], XF[b_]) - sum(GF[l][a_][b_] * sp.diff(Wf, XF[l]) for l in range(4)) for b_ in range(4)] for a_ in range(4)]
LapW = sp.simplify(sum(hF[a_][b_] * nnW[a_][b_] for a_ in range(4) for b_ in range(4)) + KF * sum(nF_up[a_] * sp.diff(Wf, XF[a_]) for a_ in range(4)))
K_spatial = sorted(str(s_) for s_ in KF.free_symbols if str(s_) in ('x1', 'x2', 'x3'))   # K constant on the leaf => K = <K>_h
checks_d1 = {"q(0) = 2H(0)": H_mono(0.0), "a_m a^m": a2F, "C-H |DU - a|^2 (h dU dU, a = 0)": hdUF, "Delta_h W": LapW,
             "(K - <K>_h)^2: spatial dependence of K": len(K_spatial)}
d1_ok = all(v_ == 0 for v_ in checks_d1.values()) and sp.simplify(KF - 3 * sp.diff(af, tf) / (af * Nf)) == 0 \
        and sp.simplify(H2_leaf - (Lam_ + kap4 * rho_m) / 3) == 0
check("D1 on FRW every MOND, C-H, alpha_c and leaf-average term vanishes identically, so the Friedmann equation is 3H^2 = "
      "Lambda + 8 pi G rho with no a0; the lapse constraint is local (A3: second class at k != 0, first class at k = 0), so "
      "no dust integration constant appears -- the core carries no dark mass",
      f"terms on the homogeneous leaf: {checks_d1}; K = {KF}; 3H^2 = {sp.simplify(3 * H2_leaf)}", d1_ok)

# ================================================================================================ D2
banner("D2  statics: the primitive's constant is a zero mode (k01 K1, in C-H form)")
xs = sp.Symbol('x', real=True)
Pp, Up, Ps = (sp.Function(q)(xs) for q in ('Phi', 'U', 'Psi'))
qf = sp.Function('q'); Cq = sp.Symbol('C_q'); rho_s = sp.Symbol('rho_s')
from sympy.calculus.euler import euler_equations
Lst = 2 * sp.diff(Ps, xs) ** 2 - 4 * sp.diff(Pp, xs) * sp.diff(Ps, xs) + 2 * (sp.diff(Up, xs) - sp.diff(Pp, xs)) ** 2 \
      + ac * sp.diff(Pp, xs) ** 2 + 2 * qf(sp.diff(Up, xs) ** 2) - rho_s * Pp
E1 = euler_equations(Lst, [Ps, Pp, Up], xs)
E2 = euler_equations(Lst + 2 * Cq, [Ps, Pp, Up], xs)
d2_ok = all(sp.simplify(a_.lhs - b_.lhs) == 0 for a_, b_ in zip(E1, E2)) and not any(e_.lhs.has(qf(sp.diff(Up, xs) ** 2)) and
                                                                                   not e_.lhs.has(sp.Derivative) for e_ in E1)
check("D2 the static field equations contain q only through q' (invariant under q -> q + const): the MOND primitive's "
      "additive constant -- the only place a vacuum energy could hide -- is a free zero mode; C-H fixes it by q(0) = 0, a choice",
      f"EL(q) == EL(q + C): {d2_ok}", d2_ok)

# ================================================================================================ D3
banner("D3  promote alpha = a0/c^2 to a field sigma: its equation has no stationary MOND solution")
sg, Zs, zeta = sp.symbols('sigma Z zeta', positive=True)
d3_sym = True
for qtest in (zeta ** sp.Rational(3, 4) + zeta ** 2 / 7, sp.log(1 + zeta) * zeta ** sp.Rational(1, 3)):   # generic test primitives
    lhs_ = sp.diff(2 * sg ** 2 * qtest.subs(zeta, Zs / sg ** 2), sg)
    rhs_ = (4 * sg * (qtest - zeta * sp.diff(qtest, zeta))).subs(zeta, Zs / sg ** 2)
    d3_sym = d3_sym and sp.simplify(lhs_ - rhs_) == 0
svals = np.logspace(-10, 6, 161)
gvals = [(2 * H_mono(s_) - s_ * h_mono(s_)) / s_ ** 1.5 for s_ in svals]      # (q - Z q')/s^(3/2) at Z = s^2, alpha = 1
d3_ok = d3_sym and min(gvals) > 0 and H_mono(0.0) == 0 and abs(gvals[0] - 1 / 3) < 1e-3
check("D3 d_sigma[2 sigma^2 q(Z/sigma^2)] = 4 sigma [q - (Z/sigma^2) q'], which is identically 0 at Z = 0 (a flat direction: "
      "FRW does not fix sigma) and > 0 at every Z > 0 for nu_mono ((q - Z q')/s^(3/2) > 0 over s = 1e-10..1e6, -> 1/3 in deep "
      "MOND): the field equation forces Z = 0 (no MOND) unless a potential V(sigma) is put in by hand -- which is P1 declared",
      f"symbolic identity (two test primitives) {d3_sym}; (q - Z q')/s^1.5: min {min(gvals):.3e} at s = "
      f"{svals[int(np.argmin(gvals))]:.1e}, deep-MOND value {gvals[0]:.4f}", d3_ok)

# ================================================================================================ D4
banner("D4  the khronon's only background scale is K = 3H: tying a0 to it is the rival footing")
KF1 = sp.simplify(KF.subs(Nf, 1).doit())                     # D1's covariant K at unit lapse
Ez = lambda zz: math.sqrt(OM_M * (1 + zz) ** 3 + OM_L)
dex25 = math.log10(Ez(2.5))
l37 = rd("fable_independent_2026/L37_recombination_footing.out") or ""
l37_rival_dead = re.search(r"^\s*\[FAIL\] S8b\s+VERDICT: does the RIVAL footing", l37, re.M) is not None
d4_ok = sp.simplify(KF1 - 3 * sp.diff(af, tf) / af) == 0 and abs(dex25 - 0.576) < 2e-3 and l37_rival_dead
check("D4 on FRW K = nabla.n = 3 adot/a = 3H and <K> = K: the only dynamical background scale; a0 ~ c<K> gives a0(z)/a0(0) = "
      "E(z) (+0.576 dex at z = 2.5), the rival footing that L37 kills at recombination (committed S8b = FAIL)",
      f"K_FRW (N = 1) = {KF1}; log10 E(2.5) = {dex25:.3f}; L37 S8b rival verdict FAIL found: {l37_rival_dead}", d4_ok)

# ================================================================================================ D5
banner("D5  the record: k01 (no equation relates a0 to Lambda) and k04 (the four-form leaves a free ratio)")
k01 = rd("kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.out") or ""
k04 = rd("kappa_closure/k04_four_form_promotion_consistency.out") or ""
k01_ok = re.search(r"\[PASS\] K2 \[theorem, FLRW\].*no equation of the action relates a0 to Lambda", k01) is not None
k04_ok = re.search(r"\[FAIL\] F2 \[coefficient\] the action fixes the ratio Z/beta\^2", k04) is not None
kap_alt = A0["alt"] / (c_SI * math.sqrt(G_SI * rho_L))
lam_a2 = {f: LAMBDA_SI / (a_ / c_SI ** 2) ** 2 for f, a_ in A0.items()}
check("D5 k01's committed K2 (outcome 3: with Lambda explicit no equation relates a0 to Lambda) and k04's committed F2 (the "
      "four-form links the scales but kappa becomes a free coupling ratio) both stand; in the core's variables P1 is the "
      "declared relation Lambda/alpha^2 = 8 pi/kappa^2",
      f"k01 K2 PASS found {k01_ok}; k04 F2 FAIL found {k04_ok}; Lambda/alpha^2 = {lam_a2['canonical']:.3f} (32 pi = "
      f"{32 * math.pi:.3f}, kappa = 1/2, canonical) / {lam_a2['alt']:.3f} (kappa = {kap_alt:.3f}, alt)",
      k01_ok and k04_ok and abs(lam_a2["canonical"] / (32 * math.pi) - 1) < 1e-9)
OUT["numbers"]["D5"] = {"Lambda_over_alpha2": lam_a2, "kappa_alt": kap_alt}

# ================================================================================================ E
banner("E  (reported) THE CORE'S CONSTANTS, each with its status (values from the committed L340/L350 results)")
j350 = json.load(open(os.path.join(REPO, "real_research/g03_audit_2026/L350_chk_cosmological_G_gate_results.json")))
ceil350 = [r_["c2_ceiling"] for r_ in j350["numbers"]["G2"]["rows"] if isinstance(r_.get("c2_ceiling"), (int, float)) and r_["c2_ceiling"] == r_["c2_ceiling"]]
S1 = j340["numbers"]["S1"]
CONST = [
    ("G (Einstein-Hilbert)", "measured", "G_N = G/(1 - alpha_c/2) (K1); fixed by the laboratory G"),
    ("Lambda", "measured (fixed constant, not a field)", f"rho_Lambda = {rho_L:.3e} kg/m^3 (Omega_L = {OM_L})"),
    ("a0 = alpha c^2 (kappa)", "declared input; kappa = 1/2 FITTED",
     f"P1: Lambda/alpha^2 = 8 pi/kappa^2; a0 = {A0['canonical']:.4e} (canonical) / {A0['alt']:.4e} (alt, kappa = {kap_alt:.3f})"),
    ("xi (b = xi^2/2)", "bounded knob",
     f"Solar-System floors {S1['canonical/nu_mono']['xi_Q2']:.4f}/{S1['canonical/nu_mono']['xi_M']:.4f} pc (canonical), "
     f"{S1['alt/nu_mono']['xi_Q2']:.4f}/{S1['alt/nu_mono']['xi_M']:.4f} pc (alt) (L340 S1); discs untouched up to ~100 pc (G03 spec S3)"),
    ("alpha_c", "bounded knob (CONSTRAINT window)",
     f"[{AC_ENDS['alpha_min (L340 H4)']:.2e}, {AC_ENDS['alpha_c max (L340 P1)']:.1e}] (L340 H4 lobes / P1 alpha_2); must be > 0 "
     f"(hyperbolicity, XC2 B6) -- and that is what puts zero field outside the BPS window (C3)"),
    ("c_2", "bounded knob, in tension (OPEN)",
     f"L340 window [{c2_ends['L340 floor']:.2e}, {c2_ends['BBN ceiling']:.3f}] vs Planck-era ceilings on the plain K^2 "
     f"[{min(ceil350):.1e}, {max(ceil350):.1e}] (L350 G2); the leaf average removes the background bound only; the "
     f"perturbation bound is not computed"),
    ("beta (BPS K_ij K^ij)", "fixed = 0", "GW170817: c_T = 1 exactly (B3)"),
    ("c_CH = 2", "fixed by the static normalisation", "Delta u = 4 pi G rho; at zero field it is exactly BPS's alpha = 2 edge (C3)"),
    ("nu_mono shape", "chosen function (POSTULATED)",
     f"nu_RAR below the splice y_s = {Y_S:.4f}; floor slope delta = {DELTA_FLOOR} above (C^1,1 splice, XR3 K1)"),
    ("heat filter, leaf average", "structural choices (POSTULATED)", "no constants beyond xi"),
    ("dark state / dark initial data", "ABSENT (OPEN)", "the core's FRW is GR + Lambda (D1); CMB and clusters need a dark mass it does not carry"),
]
for nm_, st_, note in CONST:
    P(f"    {nm_:32s} {st_:40s} {note}")
check("E (reported) the core's constants: 2 measured (G, Lambda), 1 fitted coupling (kappa), 3 bounded knobs (xi, alpha_c, c_2), "
      "2 fixed structural numbers (beta = 0, c_CH = 2), 1 kernel-shape constant (delta = 0.05), and no dark sector",
      f"{len(CONST)} rows", True, load_bearing=False)
OUT["numbers"]["E"] = [dict(constant=a_, status=b_, note=c_) for a_, b_, c_ in CONST]

# ================================================================================================ W
banner("W  THE LEDGER")
zf = "FAILS" if ill else "OPEN"
LEDGER = [
    ("G-2a", "canonical count of the ungated C-H/K core: 2 tensor + 1 khronon scalar, 0 vector (N = 3)", "DERIVED",
     "A1-A3 (primary structure, second-class auxiliaries, Dirac bookkeeping) + B1 (deg det, frozen principal order)"),
    ("G-2b", "the nonlocal heat filter (W, L, lambda_0) adds no mode, no free data, no first-class constraint", "DERIVED",
     "A3 (kernel-independent heat determinant) + B2 (Schur complement = sigma_n^2 C)"),
    ("G-2c", "leaf average: lambda = 1 + c_2 on k != 0, GR on k = 0; Legendre map invertible on every mode", "DERIVED", "A2, K3"),
    ("G-2d", "no ghost (c_2 > 0) and c_T = 1", "DERIVED", "B3"),
    ("G-2e", "gradient stability on the nonzero-field branch: 0 < E < 2 above g* = y* a0 (y* ~ (alpha_c/2)^2)", "DERIVED", "C1"),
    ("G-2f", "well-posed linearisation at an open zero-field region (the ungated core's own FRW)", zf,
     "C2 (U pinned) + C3 (alpha_eff = 2 + alpha_c > 2: Hadamard ill-posed); amplitude saturates at y ~ y* (C4)"),
    ("G-2g", "nonlinear strong hyperbolicity of GR + BPS khronon (alpha_c > 0, beta = 0, lambda = 1 + c_2)", "OPEN",
     "C5 settles the linear frozen symbol only"),
    ("L2b", "a0 as a field: a0 tied to Lambda by the core's own dynamics", "POSTULATED",
     "D1-D5: no term links them; a free a0-field is flat on FRW and kills MOND in galaxies; K = 3H gives the dead rival"),
    ("L0c", "kappa = 1/2 (Lambda/alpha^2 = 32 pi)", "FITTED", "D5; k01-k03"),
    ("K-xi", "filter length xi", "CONSTRAINT", "E: Solar-System floors 0.031/0.045 pc canonical, <= ~100 pc"),
    ("K-ac", "khronon alpha_c", "CONSTRAINT", "E: [9.6e-14, 3.2e-9]"),
    ("K-c2", "khronon c_2 (tracking floor vs Planck-era ceilings on perturbations)", "OPEN", "E: L340 vs L350"),
    ("K-dark", "dark mass as a state of the core's fields", "OPEN", "D1: absent from the core"),
]
for k_, what, st_, why in LEDGER:
    P(f"    {k_:7s} {st_:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================ verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
ys_top = ystar.get(('alpha_c max (L340 P1)', 'T'))
P("  COUNT: the ungated C-H/K core propagates 3 local degrees of freedom -- two tensor modes at c and one khronon scalar --\n"
  "  and no vector mode.  U, W(z), L(z), lambda_0, the lapse and the shift are auxiliary; the heat filter adds only\n"
  "  second-class pairs and multiplies the MOND tangent by sigma(k)^2; the leaf average makes k = 0 exactly GR.\n"
  "  HEALTH: no ghost for c_2 > 0; the C-H sector renormalises the BPS alpha to E = alpha_c + 2C c_CH/(c_CH + 2C), healthy\n"
  "  for 0 < E < 2, i.e. at every field above g* = y* a0 " + (f"(y* <= {ys_top:.1e})." if ys_top else "(no crossing at this c_CH).") + "\n"
  f"  ZERO FIELD: at an open zero-field region U is pinned and the lapse feels the full C-H coefficient: alpha_eff = {E_inf},\n"
  + ("  outside BPS's window -- Hadamard ill-posed: the ungated core's own FRW has no well-posed linearisation (a canonical\n"
     "  face of XC5's sqrt(eps)); the gate's exact off-plateau, needed anyway for growth (L341), is what removes it.\n"
     if ill else "  inside BPS's window at this coefficient (the MUTATE control).\n")
  + "  a0 AS A FIELD: no term of the core ties a0 to Lambda; P1 stays a declared input and kappa = 1/2 stays fitted.")
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results.json".replace("_MUTATE_results", "_results_MUTATE")), "w"), indent=1,
          default=str)
P(f"\n  {len(CH) - n_fail}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote "
  f"{SLUG.replace('_MUTATE', '')}_results{'_MUTATE' if MUTATE else ''}.json  ({time.time() - T0:.0f} s)")
sys.exit(0 if n_fail == 0 else 1)
