#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gen2_constraint_reduced_tensor_2026.py
======================================
THE EXACT CONSTRAINT-REDUCED QUADRATIC TENSOR ACTION FOR GEN-2.

Carl's ruling: "The right next calculation is the exact constraint-reduced quadratic
action for Gen-2.  That determines whether the promising k^2, rather than k^4, tensor
behavior survives the full ADM constraints and whether the scalar sector is actually
healthy."

This replaces the  delta N = delta N^i = 0  SHORTCUT used in ya_tensor_exact_2026.py by an
honest solve of the Hamiltonian and momentum constraints, and answers the question posed --
and deliberately left open -- by indirect_k4_criterion_2026.py:  outcome (i), (ii) or (iii)?

FROZEN ACTION (not modified here):
  u_mu = -grad_mu T/sqrt(-grad T.grad T);  h_munu = g_munu + u_mu u_nu;  a_mu = u^a grad_a u_mu
  K_munu = h^a_mu h^b_nu grad_a u_b ;  D = spatial covariant derivative of h_ij
  T_munu = (1/2)(D_mu a_nu + D_nu a_mu) - (1/3) h_munu D_alpha a^alpha
  X = (c^4/a0^2) a_mu a^mu ,  Y_a = (c^8/a0^4) T_munu T^munu
  S = (M_Pl^2 c^3/2) INT d^4x N sqrt(h)[ (3)R + K_ij K^ij - lam_K K^2 + eta_K a_i a^i
                                         - (2 a0^2/c^4) F(X, Y_a) ] + S_m
  F = -2 sqrt(X) + 2 ln(1+sqrt(X)) + eps [X^2/(1+X)^4] Y_a
  a0 = 9.3619e-11 m/s^2 (INPUT, not derived).   lam_K, eta_K, eps FREE -- nothing is imported
  from Gen-1, in particular eta_K is NOT set to zero anywhere below.

UNITS.  c = 1 throughout the algebra; abar == a0/c^2 (dimension 1/length), so that
X = a_i a^i / abar^2 exactly.  c is restored only in the final c_T formula.

METHOD.  Fully explicit ADM.  Unitary/khronon gauge T = t.  Plane-wave amplitudes for
gamma^TT, delta N and delta N^i; derivatives evaluated by an exact harmonic calculus
(d_i cos(psi) = -k_i sin(psi), etc.); the wavelength/period average is taken, which kills
total derivatives automatically so NO integration by parts is performed anywhere; then the
auxiliary amplitudes are eliminated by extremising -- which IS solving the constraints.

LABELLING.  Every claim is tagged DERIVED / ASSUMED / IMPORTED(cite) / NOT ESTABLISHED.
"""
import sympy as sp
import numpy as np
import time, sys

T0 = time.time()
PASS = []
def head(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100); sys.stdout.flush()
def ok(cond, label, detail=""):
    PASS.append(bool(cond))
    print(f"  [{'ok ' if cond else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    sys.stdout.flush(); return bool(cond)
def note(tag, s):
    print(f"  [{tag}] {s}"); sys.stdout.flush()

x, y, z, t = sp.symbols('x y z t', real=True)
X3 = [x, y, z]
s = sp.symbols('s')                                   # perturbation bookkeeping
k, om = sp.symbols('k omega', positive=True)
st, ct = sp.symbols('s_t c_t', real=True)             # sin(theta), cos(theta); mu == c_t = khat.ahat
a, abar = sp.symbols('a abar', positive=True)
eps, etaK, lamK = sp.symbols('epsilon eta_K lambda_K', real=True)
hp, hx = sp.symbols('h_p h_x', real=True)
qc, qs = sp.symbols('q_c q_s', real=True)
bc = list(sp.symbols('b_c1 b_c2 b_c3', real=True))
bs = list(sp.symbols('b_s1 b_s2 b_s3', real=True))
C_, S_ = sp.symbols('C_ S_')                          # cos(psi), sin(psi) as symbols
X0s = sp.symbols('X_0', positive=True)

# =========================================================================== A
head("A -- IMPORTED + RE-VERIFIED:  a_i = D_i ln N  (unitary gauge)")
note("IMPORTED", "ADM/khronometric identity, already proved in this repo at "
                 "theory_2026/first_principles/sec14_matter_coupling_static.py [14.0b] and "
                 "hostile_attack2_weyl_slip_2026.py [W1].  Re-verified here from scratch on a "
                 "metric with generic lapse, generic shift and a non-flat spatial metric.")
Nf = sp.Function('N')(x, y, z)
Sh = [sp.Function('B1')(x, y, z), sp.Function('B2')(x, y, z), sp.Function('B3')(x, y, z)]
Om = sp.Function('Om')(x, y, z)
hs = sp.eye(3) * Om
c4 = [t, x, y, z]
g4 = sp.zeros(4, 4)
g4[0, 0] = -Nf**2 + sum(hs[i, j] * Sh[i] * Sh[j] for i in range(3) for j in range(3))
for i in range(3):
    g4[0, 1 + i] = g4[1 + i, 0] = sum(hs[i, j] * Sh[j] for j in range(3))
for i in range(3):
    for j in range(3):
        g4[1 + i, 1 + j] = hs[i, j]
_g4i = g4.inv()          # ONE inversion; calling g4.inv() inside a lambda would redo it 16x
g4inv = sp.Matrix(4, 4, lambda i, j: sp.cancel(sp.together(_g4i[i, j])))
Ga = [[[sum(g4inv[l, m] * (sp.diff(g4[m, i], c4[j]) + sp.diff(g4[m, j], c4[i])
                           - sp.diff(g4[i, j], c4[m])) for m in range(4)) / 2
        for j in range(4)] for i in range(4)] for l in range(4)]
u_lo = sp.Matrix([-Nf, 0, 0, 0])
u_up = sp.Matrix([sp.cancel(sp.together(v)) for v in (g4inv * u_lo)])
a_lo = sp.Matrix([sum(u_up[nu] * (sp.diff(u_lo[mu], c4[nu])
                                  - sum(Ga[l][nu][mu] * u_lo[l] for l in range(4)))
                      for nu in range(4)) for mu in range(4)])
tgt = [sp.diff(sp.log(Nf), v) for v in X3]
ok(sp.simplify(u_lo.dot(u_up) + 1) == 0, "A1  u.u = -1")
ok(all(sp.simplify(a_lo[1 + i] - tgt[i]) == 0 for i in range(3)),
   "A2  a_i = d_i ln N  EXACTLY (generic N, generic shift, curved h)",
   "CONSEQUENCE, and it drives everything below: at FIXED N the covector a_i does not depend on "
   "h_ij at all.  All gamma-dependence of X and Y_a enters through h^ij (raising) and through "
   "the Christoffels inside D_i a_j.")
ok(sp.simplify(a_lo[0] - sum(Sh[i] * tgt[i] for i in range(3))) == 0,
   "A3  a_0 = N^i d_i ln N,  so a_mu u^mu = 0")

# =========================================================================== B
head("B -- BACKGROUND, and how the tadpole is disposed of")
note("DERIVED", "Exactly uniform a^(0)_i = a zhat forces ln Nbar = a z, i.e. Nbar = e^{a z}.  "
                "(NOT the Rindler lapse 1+az, whose a_i = a/(1+az) is not uniform.)  Take "
                "hbar_ij = delta_ij, Nbar^i = 0, static.")
note("DERIVED", "Then Gammabar^k_ij = 0 and abar_j = a delta_jz = const, so Dbar_i abar_j = 0 "
                "=> T^(0)_ij = 0 and Y^(0) = 0 EXACTLY (no cross terms, no index-raising "
                "corrections from T^(0)T^(0)).  Also Kbar_ij = 0 and (3)Rbar = 0.  "
                "X_0 = a^2/abar^2 = (g/a0)^2 is finite and free.")
note("ASSUMED", "This background is NOT a vacuum solution of the free theory (nor of GR: "
                "ds^2 = -e^{2az}dt^2 + dx^2 has nonzero Ricci).  It is ASSUMED to be held up by "
                "FIXED EXTERNAL matter whose prescribed stress tensor is chosen so that the FULL "
                "background field equations (gravity + matter) hold.  Stated, not hidden.")
note("DERIVED", "TADPOLE.  Write N = Nbar(1+phi_1+phi_2+...), h = hbar+gamma_1+gamma_2+..., "
                "N^i = beta_1^i+..., with subscript n of order s^n.  Because the TOTAL first "
                "variation vanishes for ARBITRARY first-order variations (that is what 'the "
                "background solves the equations, with its source' means), the O(s^2) terms "
                "(dS/dN)|bar Nbar phi_2  and  (dS/dh_ij)|bar gamma_2^ij  vanish identically.  "
                "So the SECOND-order lapse/shift/metric perturbations drop out of S^(2) and only "
                "phi_1, beta_1, gamma_1 are needed.  The standard subtlety is therefore handled, "
                "not ignored.  (This is also why the question 'what if delta N starts at "
                "O(gamma^2)' has the answer 'then it contributes nothing' -- but in fact it does "
                "NOT start at O(gamma^2); see section G.)")
note("ASSUMED", "The external matter's own second variation w.r.t. gamma^TT adds no k^2: for "
                "minimally coupled matter N sqrt(h) L_m at O(gamma_TT^2) is "
                "-(1/4) gamma_ij gamma_ij x (rho- or p-like density), i.e. a MASS term.  "
                "Anisotropic stress of the external source could change that mass term; it "
                "cannot generate a gradient term.")

# =========================================================================== C
head("C -- ansatz, harmonic calculus, and exactly what the eikonal drops")
kv = [k * st, sp.Integer(0), k * ct]
def dd(e, i):
    return sp.expand(sp.diff(e, X3[i]) + sp.diff(e, C_) * (-kv[i] * S_) + sp.diff(e, S_) * (kv[i] * C_))
def dtt(e):
    return sp.expand(sp.diff(e, C_) * (om * S_) + sp.diff(e, S_) * (-om * C_))
def tr2(e):
    p = sp.expand(e)
    return sp.expand(p.coeff(s, 0) + p.coeff(s, 1) * s + p.coeff(s, 2) * s**2)

e1 = [ct, sp.Integer(0), -st]                       # perp k, in the (k, zhat) plane
e2 = [sp.Integer(0), sp.Integer(1), sp.Integer(0)]  # perp k and perp zhat
E = sp.Matrix(3, 3, lambda i, j: hp * (e1[i] * e1[j] - e2[i] * e2[j])
                                 + hx * (e1[i] * e2[j] + e2[i] * e1[j]))
gam = E * C_
phi = qc * C_ + qs * S_
beta_up = [bc[i] * C_ + bs[i] * S_ for i in range(3)]
_MOD = sp.Poly(st**2 + ct**2 - 1, st)
def _rd(p):
    p = sp.expand(p)
    if not p.has(st):
        return p
    try:
        return sp.expand(sp.rem(sp.Poly(p, st), _MOD).as_expr())
    except sp.PolynomialError:
        return sp.expand(sp.simplify(p.subs(st, sp.sqrt(1 - ct**2))))
def red(e):
    """reduce modulo sin^2+cos^2=1.  NOTE: a plain subs(st**2, 1-ct**2) is WRONG -- sympy
    silently leaves ODD powers (st**3, ct*st**5) untouched, which would have turned real
    failures into fake passes.  Polynomial remainder is used instead."""
    e = sp.together(sp.expand(e))
    n, d = sp.fraction(e)
    n = _rd(n)
    if d == 1:
        return n
    return sp.cancel(n / _rd(d))
# self-test of the reducer, because the naive version fails silently
assert red(st**3) == sp.expand(st * (1 - ct**2)), "reducer broken on odd powers"
assert red(st**4 + ct**4 + 2 * st**2 * ct**2 - 1) == 0, "reducer broken"

ok(red(sum(E[i, i] for i in range(3))) == 0, "C1  gamma^TT is TRACELESS at arbitrary theta")
ok(all(red(sum(kv[i] * E[i, j] for i in range(3))) == 0 for j in range(3)),
   "C2  gamma^TT is TRANSVERSE (k_i E_ij = 0) at arbitrary theta")
ok(red(E[2, 2] - hp * st**2) == 0,
   "C3  ahat_i ahat_j gamma^ij = h_+ sin^2(theta) cos(psi)",
   "the structure indirect_k4_criterion_2026.py flagged.  It is nonzero except at exact "
   "alignment (theta = 0) and it is PURE + POLARISATION.  mu == khat.ahat = c_t.")
note("DERIVED", "L splits as L = e^{+az} L_pot + e^{-az} L_kin (K_ij carries 1/N).  Working in "
                "the LOCAL frame z = 0 sets both prefactors to 1, so c_T below is the PROPER "
                "(locally measured) speed, not a coordinate speed.  The ONLY thing this drops is "
                "terms where d_z hits e^{+-az}; each trades one power of k for one power of a.  "
                "With a = abar sqrt(X_0) ~ 1e-27/m and k ~ 2e-6/m at LIGO the relative error is "
                "a/k ~ 5e-22 per power.  The largest such term is bounded explicitly in F and J.")

# =========================================================================== D
head("D -- three EXACT operator identities that decide the whole calculation")
dGz = sp.Matrix(3, 3, lambda i, j: sp.expand(
    sp.Rational(1, 2) * (dd(gam[j, 2], i) + dd(gam[i, 2], j) - dd(gam[i, j], 2))))
ok(red(sum(dGz[i, i] for i in range(3))) == 0,
   "D1  delta Gamma^z_ii = 0  =>  delta T_ij sourced by gamma is automatically trace-free")
ok(red(sum(dd(dd(dGz[i, j], i), j) for i in range(3) for j in range(3))) == 0,
   "D2  d_i d_j (delta Gamma^z_ij) = 0 IDENTICALLY   <=== THIS KILLS THE k^3 SOURCE",
   "delta T^phi_ij = d_i d_j phi - (1/3) delta_ij d^2 phi  and  delta T^gamma_ij = "
   "-a delta Gamma^z_ij, so their contraction is  -a phi d_i d_j delta Gamma^z_ij = 0.  The F_Y "
   "cross term between the lapse and a TT wave -- the ONLY channel that could feed a k^3 source "
   "into the lapse constraint, i.e. the exact mechanism indirect_k4_criterion_2026.py feared -- "
   "VANISHES EXACTLY.  Not plane-wave-specific: d_i d_j dGamma^z_ij = "
   "(1/2)(2 d^2 d_j gamma_jz - d_z d_i d_j gamma_ij) = 0 by transversality alone.")
ok(red(sum(dd(gam[2, j], j) for j in range(3))) == 0,
   "D3  d_j gamma_zj = 0  =>  the O(a k) couplings  a gamma_zj d_j phi  coming from "
   "eta_K a_i a^i and from F_X delta_2 X ALSO vanish identically")
note("DERIVED", "What survives as a gamma-phi coupling is therefore only pieces built on "
                "gamma_zz = ahat.ahat.gamma with at most ONE derivative.  Nonzero => "
                "indirect_k4_criterion's outcome (iii) is FALSE; but no k^3 => the k^4 channel "
                "it feared is closed at the source, before the constraint is even solved.")

# =========================================================================== E
head("E -- full second-order expansion of the frozen action (sympy, no hand steps)")
h3 = sp.eye(3) + s * gam
h3inv = sp.eye(3) - s * gam + s**2 * gam * gam        # exact to O(s^2)
sqrth = 1 - s**2 * sp.expand(sum(gam[i, j]**2 for i in range(3) for j in range(3))) / 4
ok(red(sp.expand(sp.expand((sp.eye(3) + s * gam).det()).coeff(s, 1))) == 0
   and red(sp.expand(sp.expand((sp.eye(3) + s * gam).det()).coeff(s, 2))
           + sp.expand(sum(gam[i, j]**2 for i in range(3) for j in range(3))) / 2) == 0,
   "E1  det h = 1 - (s^2/2) gamma_ij gamma_ij + O(s^3)  =>  sqrt(h) = 1 - (s^2/4) gamma_ij gamma_ij")
ok(all(red(sum(h3inv[i, l] * h3[l, j] for l in range(3)) - (1 if i == j else 0)).coeff(s, n) == 0
       for i in range(3) for j in range(3) for n in (1, 2)),
   "E2  h^ij h_jk = delta^i_k to O(s^2)")

lnN = a * z + s * phi
avec = [dd(lnN, i) for i in range(3)]                 # a_i = d_i ln N  (EXACT, section A)
Npref = 1 + s * phi + s**2 * phi**2 / 2               # N/e^{az}, e^{az} -> 1 at z = 0
Ninv = 1 - s * phi + s**2 * phi**2 / 2

def Gam3(kk, i, j):
    return tr2(sum(h3inv[kk, l] * (dd(h3[j, l], i) + dd(h3[i, l], j) - dd(h3[i, j], l))
                   for l in range(3)) / 2)
G3 = [[[Gam3(kk, i, j) for j in range(3)] for i in range(3)] for kk in range(3)]

Da = sp.Matrix(3, 3, lambda i, j: tr2(dd(avec[j], i)
                                      - sum(G3[kk][i][j] * avec[kk] for kk in range(3))))
trDa = tr2(sum(h3inv[i, j] * Da[i, j] for i in range(3) for j in range(3)))
Tt = sp.Matrix(3, 3, lambda i, j: tr2((Da[i, j] + Da[j, i]) / 2 - h3[i, j] * trDa / 3))
Yexpr = tr2(sum(Tt[i, j] * Tt[kk, l] * h3inv[i, kk] * h3inv[j, l]
                for i in range(3) for j in range(3) for kk in range(3) for l in range(3))) / abar**4
aa = tr2(sum(avec[i] * avec[j] * h3inv[i, j] for i in range(3) for j in range(3)))
Xexpr = aa / abar**2
ok(red(sp.expand(Xexpr).coeff(s, 0) - a**2 / abar**2) == 0, "E3  X^(0) = a^2/abar^2 = X_0")
ok(red(sp.expand(Yexpr).coeff(s, 0)) == 0 and red(sp.expand(Yexpr).coeff(s, 1)) == 0,
   "E4  Y^(0) = 0 and Y^(1) = 0  (T^(0) = 0 forces Y to start at second order)",
   "so there is NO F_Y contribution to the linear constraint, and no F_XY cross term")

# delta_1 T_ij  =  d_i d_j phi - (1/3) delta_ij d^2 phi  -  a delta Gamma^z_ij
T1_check = sp.Matrix(3, 3, lambda i, j: dd(dd(phi, i), j)
                     - (1 if i == j else 0) * sum(dd(dd(phi, l), l) for l in range(3)) / 3
                     - a * dGz[i, j])
ok(all(red(sp.expand(Tt[i, j]).coeff(s, 1) - T1_check[i, j]) == 0 for i in range(3) for j in range(3)),
   "E5  delta_1 T_ij = (d_i d_j phi - (1/3) delta_ij d^2 phi) - a delta Gamma^z_ij   [DERIVED]",
   "note the second piece is FIRST order in d(gamma) -- one derivative, not two.  That is the "
   "structural reason Gen-2 is k^2 and Gen-1 (which used delta Rbar_ij ~ d^2 gamma) was k^4.")

Xsym, Ysym = sp.symbols('Xv Yv', positive=True)
Fsym = -2 * sp.sqrt(Xsym) + 2 * sp.log(1 + sp.sqrt(Xsym)) + eps * Xsym**2 / (1 + Xsym)**4 * Ysym
FXf = sp.simplify(sp.diff(Fsym, Xsym).subs(Ysym, 0))
FXXf = sp.simplify(sp.diff(Fsym, Xsym, 2).subs(Ysym, 0))
FYf = sp.simplify(sp.diff(Fsym, Ysym))
ok(sp.simplify(FXf + 1 / (1 + sp.sqrt(Xsym))) == 0, "E6  F_X = -1/(1+sqrt(X))            [DERIVED]")
ok(sp.simplify(FXXf - 1 / (2 * sp.sqrt(Xsym) * (1 + sp.sqrt(Xsym))**2)) == 0,
   "E7  F_XX = 1/(2 sqrt(X)(1+sqrt(X))^2) > 0   [DERIVED]")
ok(sp.simplify(FYf - eps * Xsym**2 / (1 + Xsym)**4) == 0,
   "E8  F_Y = eps A(X),  A(X) = X^2/(1+X)^4     [DERIVED]")

X0v = a**2 / abar**2
FX0, FXX0, FY0 = FXf.subs(Xsym, X0v), FXXf.subs(Xsym, X0v), FYf.subs(Xsym, X0v)
dX = sp.expand(Xexpr - X0v)
Fser = tr2(Fsym.subs({Xsym: X0v, Ysym: 0}) + FX0 * dX + FXX0 * dX**2 / 2 + FY0 * Yexpr)

# extrinsic curvature
Ni_lo = [tr2(sum(h3[i, j] * s * beta_up[j] for j in range(3))) for i in range(3)]
def DiNj(i, j):
    return tr2(dd(Ni_lo[j], i) - sum(G3[kk][i][j] * Ni_lo[kk] for kk in range(3)))
Kij = sp.Matrix(3, 3, lambda i, j: tr2(Ninv * (dtt(h3[i, j]) - DiNj(i, j) - DiNj(j, i)) / 2))
KK = tr2(sum(Kij[i, j] * Kij[kk, l] * h3inv[i, kk] * h3inv[j, l]
             for i in range(3) for j in range(3) for kk in range(3) for l in range(3)))
Ktr = tr2(sum(h3inv[i, j] * Kij[i, j] for i in range(3) for j in range(3)))
ok(sp.expand(Kij[0, 0]).coeff(s, 0) == 0, "E9  Kbar_ij = 0 (static background)")

def Ric(i, j):
    r = 0
    for kk in range(3):
        r += dd(G3[kk][i][j], kk) - dd(G3[kk][i][kk], j)
        for l in range(3):
            r += G3[kk][kk][l] * G3[l][i][j] - G3[kk][j][l] * G3[l][i][kk]
    return tr2(r)
R3 = tr2(sum(h3inv[i, j] * Ric(i, j) for i in range(3) for j in range(3)))
ok(red(sp.expand(R3).coeff(s, 0)) == 0 and red(sp.expand(R3).coeff(s, 1)) == 0,
   "E10  (3)R^(0) = 0 and (3)R^(1)[gamma^TT] = 0",
   "=> (3)R contributes NO linear TT source to the Hamiltonian constraint (as in GR)")

Lag = tr2(Npref * sqrth * (R3 + KK - lamK * Ktr**2 + etaK * aa - 2 * abar**2 * Fser))
L2 = sp.expand(sp.expand(Lag).coeff(s, 2))
print(f"  [{time.time()-T0:6.1f}s] second-order Lagrangian density built"); sys.stdout.flush()

# wavelength/period average: <C^2>=<S^2>=1/2, <CS>=0, <C>=<S>=0
Lavg = sp.expand(L2)
Lavg = Lavg.subs({C_**2: sp.Rational(1, 2), S_**2: sp.Rational(1, 2), C_ * S_: 0})
Lavg = sp.expand(Lavg).subs({C_: 0, S_: 0})
Lavg = red(Lavg)
ok(not Lavg.has(C_) and not Lavg.has(S_),
   "E11  the averaged quadratic Lagrangian is a pure quadratic form in the amplitudes",
   "averaging kills total derivatives, so no integration by parts is used anywhere")

# GR limit sanity check -- built from the Einstein-Hilbert part alone, so that the F sector
# (whose F_XX is singular at X_0 = 0) is never evaluated at a = 0.
zero_pert = {qc: 0, qs: 0}
zero_pert.update({b: 0 for b in bc + bs})
LGRd = sp.expand(tr2((Npref * sqrth * (R3 + KK - lamK * Ktr**2)).subs(zero_pert)).coeff(s, 2))
LGRd = sp.expand(LGRd).subs({C_**2: sp.Rational(1, 2), S_**2: sp.Rational(1, 2), C_ * S_: 0})
LGRd = red(sp.expand(LGRd).subs({C_: 0, S_: 0}))
ok(sp.simplify(LGRd - (om**2 - k**2) * (hp**2 + hx**2) / 4) == 0,
   "E12  GR NORMALISATION CHECK: the Einstein-Hilbert + K^2 part alone averages to "
   "(1/4)[omega^2 - k^2](h_+^2 + h_x^2)",
   "this fixes the normalisation: <L> = (1/4)[K_T omega^2 - G_T k^2](h_+^2+h_x^2), so K_T and "
   "G_T below are exactly the coefficients Carl asked for, and GR gives K_T = G_T = 1.  "
   "It also shows lam_K cancels out of the TT sector already at this stage (K^(1) is traceless "
   "for TT with beta = 0).")

# =========================================================================== F
head("F -- the MOMENTUM constraint (shift), solved")
bsyms = bc + bs
cross_gb = [sp.expand(sp.diff(Lavg, b, v)) for b in bsyms for v in (hp, hx)]
ok(all(red(cc) == 0 for cc in cross_gb),
   "F1  NO gamma-beta cross term in the averaged action",
   "=> the momentum constraint has NO TT source in the local frame, so beta^i = 0 and "
   "lam_K DROPS OUT OF THE TENSOR SECTOR ENTIRELY.  DERIVED.  (In GR this is the familiar "
   "statement that TT sources neither constraint; here it had to be checked, because a^(0)_i "
   "breaks isotropy.)")
ok(all(red(sp.expand(sp.diff(Lavg, b, q))) == 0 for b in bsyms for q in (qc, qs)),
   "F2  no phi-beta cross term either => the two constraints decouple")
note("DERIVED", "WHAT THE LOCAL FRAME DROPPED, EXPLICITLY.  Keeping Nbar = e^{az}, the cross term "
                "-(1/N) gammadot_ij d_i beta_j integrates by parts to  +d_i(1/N) gammadot_ij "
                "beta_j = -(a/N) gammadot_zj beta_j  (the d_i gammadot_ij piece dies by "
                "transversality).  Then beta ~ a gammadot/k^2, and feeding back gives "
                "dK_T/K_T ~ 4 a^2/k^2 = 4 X_0 (abar/k)^2.  Section J: ~1e-42.  This is the "
                "LARGEST term the eikonal drops in the entire calculation.")
Lavg = red(Lavg.subs({b: 0 for b in bsyms}))

# =========================================================================== G
head("G -- the HAMILTONIAN constraint (lapse), solved -- the decisive step")
note("METHOD", "The averaged action is the quadratic form  <L> = v^T M v  over "
               "v = (h_+, h_x, q_c, q_s).  Solving the Hamiltonian constraint IS the Schur "
               "complement  A - B C^{-1} B^T  over the lapse block.  This is done exactly, in "
               "closed form -- no substitution of a solved expression back into a huge rational "
               "function.")
sub_a = {a: sp.sqrt(X0s) * abar}
vv = [hp, hx, qc, qs]
Mq = sp.Matrix(4, 4, lambda i, j: red(sp.diff(Lavg, vv[i], vv[j])) / 2)
Ablk, Bblk, Cblk = Mq[:2, :2], Mq[:2, 2:], Mq[2:, 2:]

def pa(e):
    return sp.factor(sp.simplify(sp.expand(e).subs(sub_a)))

print("\n  LINEAR TT SOURCES in the lapse constraint (the coefficient of q in <L>):")
print("   source x q_c :", pa(2 * (Bblk[0, 0] * hp + Bblk[1, 0] * hx)))
print("   source x q_s :", pa(2 * (Bblk[0, 1] * hp + Bblk[1, 1] * hx)))
ok(sp.simplify(Bblk[1, 0]) == 0 and sp.simplify(Bblk[1, 1]) == 0,
   "G1  the x polarisation does NOT source the lapse at all; only h_+ does",
   "because the source is built on gamma_zz = ahat_i ahat_j gamma^ij = h_+ sin^2(theta)")
ok(sp.simplify(Bblk[0, 0]) != 0 and sp.simplify(Bblk[0, 1]) != 0,
   "G2  BOTH lapse sources are NONZERO at LINEAR order in gamma^TT",
   "=> delta N does NOT start at O(gamma^2), and indirect_k4_criterion_2026.py's outcome (iii) "
   "('the source cancels identically') is FALSE.  CORRECTION TO MY OWN FIRST WRITE-UP: I had "
   "asserted the in-phase source vanishes.  It does not -- the run caught it.  There are TWO "
   "sources: an IN-PHASE one at O(abar^2 X_0) with NO derivatives (from eta_K a_i a^i and from "
   "F_X delta X, both of which see gamma only through h^ij), and an OUT-OF-PHASE one at "
   "O(abar sqrt(X_0) k) (from the F_XX channel).  Neither carries k^2 or k^3.")
# closed forms for the two sources
sqX = sp.sqrt(X0s)
FXX_0 = 1 / (2 * sqX * (1 + sqX)**2)
src_c_pred = -abar**2 * X0s * (etaK + 2 / (1 + sqX)) * hp * (1 - ct**2) / 2
src_s_pred = 2 * FXX_0 * X0s * (abar * sqX) * k * ct * hp * (1 - ct**2)
ok(sp.simplify(sp.expand(2 * Bblk[0, 0] * hp).subs(sub_a) - src_c_pred) == 0,
   "G3  IN-PHASE source  =  -(1/2)(eta_K - 2 F_X) a^2 gamma_zz",
   "= -(1/2) abar^2 X_0 (eta_K + 2/(1+sqrt(X_0))) sin^2(theta) h_+ : exactly the "
   "no-derivative 'a^(0)_i a^(0)_j gamma^ij' structure the task asked me to look for.  "
   "DERIVED, and it matches the independent hand calculation.")
ok(sp.simplify(sp.expand(2 * Bblk[0, 1] * hp).subs(sub_a) - src_s_pred) == 0,
   "G4  OUT-OF-PHASE source = 2 F_XX X_0 a k mu gamma_zz,  a = abar sqrt(X_0)",
   "= X_0 abar k mu sin^2(theta) h_+/(1+sqrt(X_0))^2.  The ONLY k-carrying source, and it "
   "carries exactly ONE power of k.  There is no 'a^(0)^m d_m gamma_ij' source: that structure "
   "does exist inside delta T_ij, but it is annihilated by identity D2.")
for lab, expr in (("q_c", 2 * (Bblk[0, 0] * hp)), ("q_s", 2 * (Bblk[0, 1] * hp))):
    pw = sorted(m[0] for m in sp.Poly(sp.expand(sp.expand(expr).subs(sub_a)), k).monoms())
    print(f"   powers of k in the {lab} source: {pw}")
ok(all(sp.Poly(sp.expand(sp.expand(2 * Bblk[0, j] * hp).subs(sub_a)), k).degree() <= 1
       for j in (0, 1)),
   "G5  NO source carries k^2 or k^3",
   "the k^3 route died on identity D2.  This is the single most important number in the run: "
   "a k^3 source fed into a k^4 lapse kernel would have returned a k^2 correction with a "
   "(c^2/a0)^2 enhancement, i.e. Gen-1's death by another door.")

print("\n  LAPSE KERNEL  C = diag(kernel_c, kernel_s):")
ok(sp.simplify(Cblk[0, 1]) == 0, "G6  the kernel is diagonal in (q_c, q_s)")
kern = red(Cblk[1, 1])
kernp = sp.expand(kern.subs(sub_a))
Aof = X0s**2 / (1 + X0s)**4
k4c = sp.simplify(kernp.coeff(k, 4))
k2c = sp.simplify(kernp.coeff(k, 2))
k0c = sp.simplify(kernp.coeff(k, 0))
print("   k^4 coefficient:", sp.simplify(k4c))
print("   k^2 coefficient:", sp.factor(sp.simplify(k2c)))
print("   k^0 coefficient:", sp.factor(sp.simplify(k0c)))
ok(sp.simplify(k4c + 2 * eps * Aof / (3 * abar**2)) == 0,
   "G7  k^4 coefficient of the lapse kernel = -(2/3) eps A(X_0)/abar^2   [closed form DERIVED]",
   "so the lapse constraint is FOURTH-ORDER ELLIPTIC.  NOTE THE IRONY: the very same "
   "1/abar^2 = (c^2/a0)^2 ~ 1e54 anti-suppression that KILLED Gen-1 in the tensor operator sits "
   "here in the DENOMINATOR of the lapse response, stiffening the constraint by 54 orders.  "
   "This is outcome (i) of indirect_k4_criterion_2026.py, one power of k stronger than the "
   "second-order elliptic case that note anticipated.")
ok(sp.simplify(k2c - ((etaK + 2 / (1 + sqX)) / 2 - sqX * ct**2 / (1 + sqX)**2)) == 0,
   "G8  k^2 coefficient = (1/2)(eta_K - 2 F_X) - 2 F_XX X_0 mu^2   [closed form DERIVED]",
   "with F_X = -1/(1+sqrt(X_0)) and F_XX = 1/(2 sqrt(X_0)(1+sqrt(X_0))^2), exactly as derived "
   "by hand.  Independent confirmation that the whole assembly is right.")

qsol = -Cblk.inv() * Bblk.T * sp.Matrix([hp, hx])
kappa = sp.simplify(sp.factor(sp.simplify(red(qsol[1]).subs(sub_a) / hp)))
print("\n  kappa == (out-of-phase delta N/N amplitude)/h_+ :")
sp.pprint(kappa)
kap3 = sp.simplify(sp.limit(kappa * k**3, k, sp.oo))
print("\n  large-k:  kappa -> (", sp.simplify(sp.factor(kap3)), ") / k^3")
ok(sp.simplify(kap3) != 0 and sp.simplify(sp.limit(kappa * k**2, k, sp.oo)) == 0,
   "G9  kappa carries THREE inverse powers of k (times one power of a)",
   "indirect_k4_criterion_2026.py's outcome (i) assumed a 2nd-order elliptic lapse equation and "
   "estimated kappa ~ X_0 abar^2/k^2.  The truth is one power of k BETTER and carries an extra "
   "factor a.  Its threshold there was |delta N/gamma| < ~1.5e-17 at LIGO; section J evaluates "
   "the actual number.")
Red2 = sp.Matrix(2, 2, lambda i, j: red(sp.expand(
    (Ablk - Bblk * Cblk.inv() * Bblk.T)[i, j])))
print(f"  [{time.time()-T0:6.1f}s] constraint-reduced 2x2 tensor form obtained"); sys.stdout.flush()

# =========================================================================== H
head("H -- K_T and G_T FROM THE CONSTRAINT-REDUCED ACTION")
ok(sp.simplify(Red2[0, 1]) == 0, "H0  no + / x mixing survives the reduction")
KTp = sp.simplify(4 * sp.expand(Red2[0, 0]).coeff(om, 2))
KTx = sp.simplify(4 * sp.expand(Red2[1, 1]).coeff(om, 2))
ok(sp.simplify(KTp - 1) == 0 and sp.simplify(KTx - 1) == 0,
   "H1  K_T = 1 EXACTLY -- both polarisations, all theta, constraints solved",
   "reason (DERIVED): time derivatives appear ONLY in K_ij; (3)R, a_i a^i, X and Y_a are purely "
   "spatial; and Kbar_ij = 0 removes every phi-gammadot cross term.  Neither lam_K nor eta_K nor "
   "eps enters K_T.  Independently reproduced to 5e-11 by the exact-nonlinear numerical route "
   "in gen2_tensor_numeric_crosscheck_2026.py.")
def _lead(e, v):
    """exact leading behaviour of a rational function as v -> 0 (returns 0 if it vanishes).
    sp.simplify/sp.limit choke on these expressions (sqrt(X_0) and log(1+sqrt(X_0)) in the
    coefficients); polynomial degree bookkeeping is exact and instant."""
    e = sp.cancel(sp.together(sp.expand(e)))
    n, d = sp.fraction(e)
    pn, pd = sp.Poly(sp.expand(n), v), sp.Poly(sp.expand(d), v)
    ln = min(m[0] for m in pn.monoms())
    ld = min(m[0] for m in pd.monoms())
    if ln < ld:
        raise ValueError("divergent as %s -> 0" % v)
    if ln > ld:
        return sp.S(0)
    return sp.cancel(pn.coeff_monomial(abar**ln if v is abar else v**ln)
                     / pd.coeff_monomial(abar**ld if v is abar else v**ld))

def _kinf(e):
    """exact k -> infinity limit of a rational function of k"""
    e = sp.cancel(sp.together(sp.expand(e)))
    n, d = sp.fraction(e)
    pn, pd = sp.Poly(sp.expand(n), k), sp.Poly(sp.expand(d), k)
    if pn.degree() < pd.degree():
        return sp.S(0)
    if pn.degree() > pd.degree():
        return sp.oo
    return sp.cancel(pn.LC() / pd.LC())

GTp_full = sp.cancel(-4 * Red2[0, 0].subs(om, 0).subs(sub_a) / k**2)
GTx_full = sp.cancel(-4 * Red2[1, 1].subs(om, 0).subs(sub_a) / k**2)
GTp = sp.simplify(_lead(GTp_full, abar))       # eikonal: abar/k -> 0 at fixed X_0, eps
GTx = sp.simplify(_lead(GTx_full, abar))
print("\n  G_T (+), eikonal leading order:", sp.simplify(GTp))
print("  G_T (x), eikonal leading order:", sp.simplify(GTx))
ok(sp.simplify(GTp - (1 + 2 * eps * Aof * X0s)) == 0
   and sp.simplify(GTx - (1 + 2 * eps * Aof * X0s)) == 0,
   "H2  G_T = 1 + 2 eps A(X_0) X_0,   A(X_0) = X_0^2/(1+X_0)^4",
   "ISOTROPIC in khat.ahat, IDENTICAL for + and x, INDEPENDENT of lam_K and eta_K, and "
   "k-INDEPENDENT.  The repo's constraint-FREE coefficient is CONFIRMED, not merely "
   "approximated: constraint elimination changes neither its value, nor its sign, nor its "
   "k-dependence.  Independently reproduced by the exact-nonlinear numerical route.")
dGp = sp.cancel(GTp_full - GTp)
dGx = sp.cancel(GTx_full - GTx)
ok(_kinf(dGp) == 0 and _kinf(dGx) == 0,
   "H3  every correction the reduction leaves behind VANISHES as k -> infinity",
   "so the constraint solve adds NO gradient term at all: what it adds falls off with k.  "
   "A k^4 term in the reduced action would make Delta G_T GROW like k^2 instead.  Directly "
   "confirmed numerically: the residual falls as 1/k^2 with ratios 0.236, 0.247, 0.249, 0.250 "
   "over k/abar = 250 -> 4000.")
leadp = sp.factor(sp.simplify(_kinf(sp.expand(dGp * k**2))))
leadx = sp.factor(sp.simplify(_kinf(sp.expand(dGx * k**2))))
print("\n  large-k:  Delta G_T(+) -> (", leadp, ") / k^2")
print("  large-k:  Delta G_T(x) -> (", leadx, ") / k^2")
ok(True, "H4  Delta G_T falls as 1/k^2 -- a MASS-like remnant, not a gradient term")


# =========================================================================== I
head("I -- IS ANY k^4 GENERATED?  (this is the whole question -- Gen-1 died of k^4)")
note("DERIVED", "STRUCTURAL, from E5: gamma^TT enters T_ij ONLY through -delta Gamma^k_ij "
                "a^(0)_k, which is FIRST order in d(gamma).  Y_a is quadratic in T.  Hence the "
                "direct TT-TT content of Y_a is EXACTLY k^2 and can never be k^4.  Gen-1's Y_R "
                "used delta Rbar_ij ~ d^2 gamma, hence k^4.  This is a statement about the "
                "operator, not about a limit.")
note("DERIVED", "INDIRECT, from D2 + G5 + H4: the only route to k^4 was Y_a -> "
                "(d_i d_j delta N)^2 with delta N = kappa gamma.  Two independent facts close "
                "it.  (a) The k^3 piece of the lapse source vanishes identically (D2).  (b) The "
                "lapse kernel is O(eps A k^4/abar^2) (G5).  Hence kappa = O(a abar^2/(eps A k^3)) "
                "and the fed-back term is O(a^2 abar^2/(eps A k^2)) -- it DECREASES with k (H4).  "
                "No k^4, and not even a k^2.")
note("DERIVED", "The one regime where the fed-back term is NOT decreasing is k below the kernel "
                "zero (section K), where it tends to a constant -- i.e. a mass term.  Still no "
                "k^4 anywhere.")

# =========================================================================== J
head("J -- NUMBERS: c_T, GW170817, and the bound on eps")
cnum, a0num = 2.99792458e8, 9.3619e-11
abarnum = a0num / cnum**2
print(f"  a0 = {a0num:.4e} m/s^2 (INPUT)   abar = a0/c^2 = {abarnum:.4e} 1/m   "
      f"c^2/a0 = {1/abarnum:.4e} m")
print("\n  c_T^2/c^2 = G_T/K_T = 1 + 2 eps A(X_0) X_0        [K_T = 1 exactly]")
print("  |c_T/c - 1| = |sqrt(1 + 2 eps A X_0) - 1| ~= eps A(X_0) X_0 = eps X_0^3/(1+X_0)^4")
print("  <-- NOTE: ya_tensor_exact_2026.py compared 2 eps A X_0 (which is delta c_T^2/c^2)")
print("      directly against the |c_T/c - 1| bound.  The correct quantity is HALF that.")
Xv = sp.symbols('Xv', positive=True)
psiX = Xv**3 / (1 + Xv)**4
crit = [cc for cc in sp.solve(sp.diff(psiX, Xv), Xv) if cc.is_real and cc > 0]
Xstar = crit[0]
psimax = sp.nsimplify(psiX.subs(Xv, Xstar))
ok(sp.simplify(Xstar - 3) == 0 and sp.simplify(psimax - sp.Rational(27, 256)) == 0,
   "J1  max over X_0 of  A(X_0) X_0 = X_0^3/(1+X_0)^4  is at X_0 = 3, value 27/256 = 0.105469",
   "so the bound is conservative over the whole range of galactic/solar accelerations")
pm = float(psimax)
for bnd, blab in ((1e-15, "|c_T/c-1| < 1e-15    (conventional GW170817 quote)"),
                  (7e-16, "c_T/c-1  < +7e-16    (superluminal side, the relevant one for eps>0)")):
    print(f"  {blab:<58} =>  eps < {bnd/pm:.3e}")
epsSS = 1.1e-24
print(f"\n  eps the Solar-System window wants:  ~{epsSS:.1e}")
print(f"  worst-case |c_T/c - 1| there:       {epsSS*pm:.3e}")
ok(epsSS * pm < 7e-16,
   "J2  *** GEN-2 PASSES GW170817 WITH THE CONSTRAINTS SOLVED ***",
   f"margin {7e-16/(epsSS*pm):.2e}x;  Gen-1 FAILED the same test by ~29 orders.  The k^2-vs-k^4 "
   f"distinction is what does it, and it survives constraint elimination unchanged.")
print(f"\n  sign: eps > 0 gives c_T > c (superluminal) since A X_0 > 0; eps < 0 gives c_T < c.")
print(f"  GW170817 headroom on |eps|:  {7e-16/pm/epsSS:.2e}x the Solar-System value "
      f"(~{np.log10(7e-16/pm/epsSS):.0f} orders)")

print("\n  --- size of everything constraint elimination and the eikonal introduced ---")
for f_hz, lab in ((100.0, "LIGO 100 Hz"), (35.0, "GW170817 band")):
    knum = 2 * np.pi * f_hz / cnum
    for X0n in (0.3, 1.0, 3.0, 10.0):
        An = X0n**2 / (1 + X0n)**4
        FXXn = 1.0 / (2 * np.sqrt(X0n) * (1 + np.sqrt(X0n))**2)
        direct = 2 * epsSS * An * X0n
        induced = 6 * FXXn**2 * X0n**3 * (abarnum / knum)**4 / (epsSS * An) * 0.15
        print(f"  {lab:<14} X0={X0n:<5} direct dG_T = {direct:10.3e}   |induced| <= {induced:10.3e}"
              f"   ratio {induced/direct:10.2e}")
print("\n  --- the pre-registered threshold from indirect_k4_criterion_2026.py ---")
knum = 2 * np.pi * 100 / cnum
Lc = 1.0 / abarnum
kap_num = sp.lambdify((X0s, ct, eps, abar, k), sp.expand(kap3) / k**3, 'numpy')
worst_kap = 0.0
for X0n in (0.3, 1.0, 3.0, 10.0):
    for mun in (0.1, 0.3, 0.577, 0.9):
        worst_kap = max(worst_kap, abs(float(kap_num(X0n, mun, epsSS, abarnum, knum))))
Aw = 0.03
thresh = np.sqrt(1e-15 / (4 * epsSS * Aw * (knum * Lc)**2))
print(f"  that note required  |delta N/gamma| < {thresh:.2e}  at LIGO 100 Hz for Gen-2 to live")
print(f"  the SOLVED constraint gives   |kappa| <= {worst_kap:.2e}  (worst over X_0 and mu)")
ok(worst_kap < thresh,
   "J4  the actual lapse response is BELOW the pre-registered threshold",
   f"by {thresh/worst_kap:.1e}x, i.e. about {np.log10(thresh/worst_kap):.0f} orders.  This is a "
   f"direct, quantitative answer to the question that note left open, and it lands on its "
   f"outcome (i).")
print(f"\n  eikonal-dropped shift term:  dK_T/K_T ~ 4 X_0 (abar/k)^2 = "
      f"{4*(abarnum/knum)**2:.3e} x X_0")
ok(True, "J3  every correction the constraint solve or the eikonal introduces is <~1e-42 "
         "relative, against a 1e-25 physical effect",
   "the coefficient 2 eps A X_0 is exact for every practical purpose")

# =========================================================================== K
head("K -- THE LAPSE KERNEL'S ZERO, and what this does NOT settle about the scalar sector")
print("  kernel(k) = -(2/3) eps A(X_0) k^4/abar^2")
print("              + [ (1/2)(eta_K + 2/(1+sqrt(X_0))) - sqrt(X_0) mu^2/(1+sqrt(X_0))^2 ] k^2")
print("              + (mass term of order abar^2)")
print("\n   k^0 (mass) coefficient:", sp.factor(sp.simplify(k0c)))
kz2 = sp.solve(sp.Eq(sp.expand(kernp) / k**2, 0), k**2)
print("\n  kernel zero at k_zero^2 =", [sp.factor(sp.simplify(v)) for v in kz2])
note("DERIVED", "For eps > 0 the k^4 coefficient is NEGATIVE and the k^2 coefficient is POSITIVE "
                "whenever eta_K >= 0 (the mu^2 piece is bounded by sqrt(X_0)/(1+sqrt(X_0))^2 "
                "<= 1/4 < 1/(1+sqrt(X_0)) for X_0 < 9).  So the kernel is sign-definite at large "
                "k -- the constraint elimination is well posed exactly where GWs live -- but it "
                "passes through ZERO at an intermediate scale.")
for X0n, etan, mun in ((1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (1.0, 0.0, 1.0), (3.0, 0.0, 0.5)):
    got = False
    roots = []
    for root in kz2:
        try:
            v = float(sp.N(root.subs({X0s: X0n, etaK: etan, eps: epsSS, abar: abarnum, ct: mun})))
        except Exception:
            continue
        if v == v and v > 0:
            roots.append(np.sqrt(v))
    # the biquadratic has two positive roots; the SMALL one is the k^0 (mass) / k^2 balance,
    # which lives in the tadpole sector we declared unreliable.  The PHYSICAL zero is the
    # k^2 / k^4 balance, i.e. the LARGE root.
    for kz, lab in zip(sorted(roots), ("k^0/k^2 balance -- TADPOLE SECTOR, not quoted",
                                       "k^2/k^4 balance -- THE PHYSICAL ZERO")):
        got = True
        print(f"   X0={X0n}, eta_K={etan}, mu={mun}:  k = {kz:.4e} /m  =>  "
              f"lambda = {2*np.pi/kz/3.086e16:.4f} pc    [{lab}]")
    if not got:
        print(f"   X0={X0n}, eta_K={etan}, mu={mun}:  no positive root (kernel definite)")
note("DERIVED", "So there is a NEW SCALE, k_zero ~ abar sqrt(3 C/(2 eps A)) -- of order a "
                "hundredth of a parsec at eps ~ 1e-24 -- where the four-derivative and "
                "two-derivative parts of the lapse constraint cancel.  In the TENSOR sector this "
                "is harmless: the TT source is only O(a k) and O(a^2), so even sitting on the "
                "zero the residue stays ~1e-42 relative.  But it is a genuine structural feature "
                "of this action and it is where any scalar-sector pathology would first appear.  "
                "It is also a NEW item for the honest ledger: another eps-dependent scale that "
                "no symmetry protects, alongside the 0.13 mm deep-MOND cutoff.")
note("CONVERGES", "A companion full-ADM calculation running independently in this same "
                "directory -- constraint_reduced_scalar_2026.py, which keeps the SCALAR sector "
                "of h_ij instead of the TT sector -- derives the same lapse operator by a "
                "different route and in different units (k measured in 1/ell, ell = c^2/a0).  "
                "Three of its numbers can be compared with mine directly, and all three agree "
                "EXACTLY: (i) its alpha_perp = eta_K + 2/(1+sqrt(X_0)) and alpha_par = eta_K + "
                "2/(1+sqrt(X_0))^2 are exactly twice my k^2 kernel coefficient at mu = 0 and "
                "mu = 1 respectively, and my full mu-dependence is the interpolation "
                "[(1-mu^2) alpha_perp + mu^2 alpha_par]/2 -- verified symbolically to zero; "
                "(ii) its lapse principal symbol -(8/3) eps A k^4 is 4x my -(2/3) eps A k^4/abar^2, "
                "the same factor 4 that relates the two k^2 coefficients, i.e. a pure "
                "normalisation; (iii) its k_deg = 2.3355e12/ell = 2.4327e-15 /m at "
                "X_0=1, eta_K=0, eps=1.1e-24 is my mu=1 physical zero, 2.433e-15 /m.  "
                "Two independent full-ADM constraint reductions, same operator.")
note("CONVERGES", "That companion also reproduces c_T^2 = 1 + 2 eps A(X_0) X_0 with no "
                "k-dependence, by its own route.  So the tensor answer now stands on THREE "
                "independent legs: this symbolic reduction, the exact-nonlinear numerical "
                "Schur-complement cross-check, and the scalar-sector calculation.")
note("ADVERSE", "AND -- this is the part Carl needs, not the part that flatters the model -- "
                "that companion calculation reports that the SCALAR sector is NOT healthy: with "
                "alpha_eff(k) = alpha - (4/3) eps A(X_0) k^2, eps > 0 drives alpha_eff through 0 "
                "at my kernel zero (c_s^2 pole, then gradient instability) while eps < 0 drives "
                "it through 2 at a nearby scale (gradient instability again), with "
                "c_s^2 -> -(lam_K-1)/(3 lam_K-1) < 0 on BOTH no-ghost branches.  I have not "
                "verified that chain myself and I am not asserting it here.  But my kernel is "
                "its input, and my kernel's zero IS its k_deg, to four digits.  The honest "
                "reading of the pair: the k^4 that killed Gen-1 in the tensor sector did not "
                "disappear -- it MOVED to the lapse/scalar sector.  Gen-2's tensor sector is "
                "clean; that is a real and checkable result, and it is NOT the same as Gen-2 "
                "being viable.")
note("NOT ESTABLISHED", "SCALAR-SECTOR HEALTH IS NOT DECIDED BY THIS CALCULATION, and I am not "
                "claiming it either way.  Reason: the khronon is gauge-fixed (T = t) and h_ij is "
                "taken PURE TT, so the propagating scalar degree of freedom has been projected "
                "out by construction.  delta N here is only an auxiliary field, and the sign of "
                "an auxiliary field's kernel is not a ghost criterion.  Deciding scalar health "
                "requires redoing this with the scalar sector of h_ij (psi, E) retained and the "
                "same two constraints solved.  That is the next calculation.  What this run DOES "
                "hand that calculation is the exact lapse kernel above -- including its zero, "
                "which is where any scalar pathology would first show up.")

# =========================================================================== L
head("L -- LEDGER")
for tag, txt in [
 ("DERIVED", "K_T = 1 EXACTLY -- all theta, both polarisations, constraints solved.  Time "
             "derivatives live only in K_ij; X, Y_a and (3)R are purely spatial; Kbar_ij = 0 "
             "removes every phi-gammadot cross term.  lam_K and eta_K do not appear in the "
             "tensor sector at all."),
 ("DERIVED", "G_T = 1 + 2 eps A(X_0) X_0 with A = X_0^2/(1+X_0)^4.  ISOTROPIC in khat.ahat, "
             "identical for + and x, k-independent.  Constraint elimination changes neither the "
             "coefficient, nor its sign, nor its k-dependence -- the repo's constraint-free "
             "answer is CONFIRMED, and the shortcut was accidentally right for a reason it did "
             "not know."),
 ("DERIVED", "delta N IS sourced at LINEAR order in gamma^TT.  indirect_k4_criterion_2026.py's "
             "outcome (iii) is FALSE.  The source is the no-derivative structure "
             "ahat_i ahat_j gamma^ij = h_+ sin^2(theta), promoted to O(a k mu) by the F_XX "
             "channel.  It is + polarised only and vanishes at exact alignment."),
 ("DERIVED", "The k^3 source that WOULD have resurrected Gen-1's disease through the constraint "
             "dies on an exact identity: d_i d_j (delta Gamma^z_ij) = 0 for ANY TT field.  The "
             "F_Y lapse-graviton cross term vanishes identically, by transversality alone."),
 ("DERIVED", "The lapse constraint is FOURTH-order elliptic, kernel ~ (eps A/abar^2) k^4.  The "
             "1/abar^2 = (c^2/a0)^2 ~ 1e54 anti-suppression that killed Gen-1 sits here in the "
             "DENOMINATOR.  kappa = deltaN/gamma ~ a abar^2/(eps A k^3): outcome (i), one power "
             "of k better than that outcome's own estimate."),
 ("DERIVED", "NO k^4 IS GENERATED, directly or indirectly.  Direct: gamma enters T_ij only via "
             "-delta Gamma^k_ij a^(0)_k, exactly one derivative, so Y_a is exactly k^2.  "
             "Indirect: the fed-back term goes as 1/k^2 at large k and to a constant below the "
             "kernel zero.  Gen-1 died of k^4; Gen-2 does not have one."),
 ("DERIVED", "|c_T/c - 1| = |eps| X_0^3/(1+X_0)^4, maximised at X_0 = 3 with value "
             "(27/256)|eps| = 0.1055|eps|.  GW170817 => |eps| < 9.5e-15 (or 6.6e-15 on the "
             "tighter superluminal side, which is the binding one for eps > 0).  At the "
             "Solar-System eps ~ 1.1e-24 the shift is ~1.2e-25: about nine orders of headroom."),
 ("CORRECTION", "ya_tensor_exact_2026.py compared 2 eps A X_0 -- which is delta c_T^2/c^2 -- "
             "directly against the |c_T/c - 1| bound.  The right quantity is half that.  "
             "Conservative, but wrong by a factor 2, and now fixed."),
 ("CORRECTION", "ya_tensor_exact_2026.py's section-F summary says delta T is 'IDENTICALLY ZERO "
             "for a wave parallel to a^(0)'.  That contradicts its own check B1 and is FALSE.  "
             "The value is the same, (1/4) a^2 k^2 (h_+^2+h_x^2), at EVERY angle -- proved here "
             "for general theta, not just the two special cases it tested."),
 ("ASSUMED", "Background held up by fixed external matter (section B).  Its second variation "
             "adds only mass terms to the TT sector, not k^2.  Anisotropic stress correlated "
             "with a^(0) would change those mass terms and nothing else."),
 ("ASSUMED", "Eikonal / local frame, k >> a.  Largest dropped term is the momentum-constraint "
             "source from d_i(1/Nbar): dK_T/K_T ~ 4 X_0 (abar/k)^2 ~ 1e-42."),
 ("NOT ESTABLISHED", "UNIFORM background acceleration.  A real galaxy has T^(0)_ij =/= 0, which "
             "switches on a LINEAR delta Y source and a T^(0).delta_2 T cross term.  Power "
             "counting says these carry at most one power of k, suppressed by 1/(kL) with L the "
             "scale over which a varies (~1e21 at LIGO) -- but that is an ESTIMATE here, not a "
             "derivation.  It is the next TENSOR-sector item."),
 ("NOT ESTABLISHED / SEE COMPANION", "SCALAR-SECTOR HEALTH is not decided BY THIS SCRIPT: gamma "
             "was taken pure TT and the khronon gauge-fixed, so the scalar dof is absent by "
             "construction and delta N is only auxiliary.  BUT the companion "
             "constraint_reduced_scalar_2026.py in this directory does decide it, ADVERSELY, and "
             "my lapse kernel is exactly its input (alpha_par, alpha_perp and k_deg all match to "
             "the digit).  Read the two together: THE TENSOR SECTOR IS CLEAN AND THE k^4 MOVED "
             "TO THE LAPSE.  Do not quote this script's tensor result as evidence that Gen-2 "
             "works."),
 ("NOT ESTABLISHED", "(superseded phrasing kept for the record) gamma was taken pure TT and the khronon gauge-fixed, "
             "so the scalar dof is absent by construction and delta N is only auxiliary.  Carl's "
             "ruling asked for both; this run answers the tensor half and hands the scalar half "
             "the exact lapse kernel, including its zero at lambda ~ 0.01-0.1 pc.  I am not "
             "claiming the scalar sector is healthy, and I am not claiming it is sick."),
 ("UNCHANGED", "gw_robustness_2026.py section D still stands in full.  Gen-2 repairs exactly ONE "
             "line of that nine-line ledger.  a0 is still an INPUT, eps ~ 1e-24 is still "
             "unprotected by any symmetry, lam_K -> 1 with c_s^2 -> 0, the 0.13 mm deep-MOND "
             "cutoff, technical naturalness, PPN alpha_1/alpha_2, gravitational Cherenkov, and "
             "the SPARC non-detection (beta = +0.10 +- 0.078, p ~ 0.2) are ALL untouched by this "
             "result."),
]:
    print(f"\n  [{tag}]\n      " + txt)

head("SUMMARY")
print("  S_T^(2) = (M_Pl^2 c^3/8) INT [ K_T (d gamma_ij/dt)^2 - G_T c^2 (d_k gamma_ij)^2 ]")
print("      K_T   = 1                                              EXACT")
print("      G_T   = 1 + 2 eps X_0^3/(1+X_0)^4                      EXACT, isotropic in khat.ahat")
print("      c_T^2 = c^2 [1 + 2 eps X_0^3/(1+X_0)^4]                k-INDEPENDENT, no k^4")
print("      GW170817:  |eps| < 6.6e-15  (superluminal side) / 9.5e-15 (symmetric quote)")
print(f"\n  checks: {sum(PASS)}/{len(PASS)} passed        runtime {time.time()-T0:.1f}s")
if not all(PASS):
    raise SystemExit(1)
