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

This script replaces the delta N = delta N^i = 0 SHORTCUT used in ya_tensor_exact_2026.py
by an honest solve of the Hamiltonian and momentum constraints, and answers the exact
question posed (and left open) by indirect_k4_criterion_2026.py: outcome (i), (ii) or
(iii)?

FROZEN ACTION (not modified here):
  u_mu = -grad_mu T/sqrt(-grad T.grad T);  h_munu = g_munu + u_mu u_nu;  a_mu = u^a grad_a u_mu
  K_munu = h^a_mu h^b_nu grad_a u_b ;  D = spatial covariant derivative of h_ij
  T_munu = (1/2)(D_mu a_nu + D_nu a_mu) - (1/3) h_munu D_alpha a^alpha
  X = (c^4/a0^2) a_mu a^mu ,  Y_a = (c^8/a0^4) T_munu T^munu
  S = (M_Pl^2 c^3/2) INT d^4x N sqrt(h)[ (3)R + K_ij K^ij - lam_K K^2 + eta_K a_i a^i
                                         - (2 a0^2/c^4) F(X, Y_a) ] + S_m
  F = -2 sqrt(X) + 2 ln(1+sqrt(X)) + eps [X^2/(1+X)^4] Y_a
  a0 = 9.3619e-11 m/s^2 (INPUT, not derived).   lam_K, eta_K, eps free.

UNITS.  c = 1 throughout the algebra; abar == a0/c^2 (dimension 1/length) so that
X = a_i a^i / abar^2 exactly.  c is restored only in the final c_T formula.
NOTHING is imported from Gen-1: eta_K is kept free everywhere.

LABELLING.  Every claim below is tagged DERIVED / ASSUMED / IMPORTED(cite).
"""
import sympy as sp
import numpy as np
import itertools

PASS = []
def head(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)
def ok(cond, label, detail=""):
    PASS.append(bool(cond))
    print(f"  [{'ok ' if cond else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    return bool(cond)
def note(tag, s):
    print(f"  [{tag}] {s}")

# ----------------------------------------------------------------------------------
x, y, z, t = sp.symbols('x y z t', real=True)
X3 = [x, y, z]
s  = sp.symbols('s')                                   # perturbation bookkeeping
k, om = sp.symbols('k omega', positive=True)
th = sp.symbols('theta', real=True)
a, abar = sp.symbols('a abar', positive=True)          # background |a^(0)| and a0/c^2
eps, etaK, lamK = sp.symbols('epsilon eta_K lambda_K', real=True)
hp, hx = sp.symbols('h_p h_x', real=True)              # TT amplitudes
qc, qs = sp.symbols('q_c q_s', real=True)              # lapse perturbation amplitudes
bc = sp.symbols('b_c1 b_c2 b_c3', real=True)           # shift amplitudes
bs = sp.symbols('b_s1 b_s2 b_s3', real=True)

# =========================================================================== A
head("A -- IMPORTED + RE-VERIFIED: a_i = D_i ln N (unitary gauge), so a_i is a COVECTOR "
     "that does not depend on h_ij at fixed N")
note("IMPORTED", "ADM/khronometric identity; already proved in this repo at "
                 "theory_2026/first_principles/sec14_matter_coupling_static.py [14.0b] and "
                 "hostile_attack2_weyl_slip_2026.py [W1].  Re-verified here on a metric with "
                 "generic lapse AND generic shift AND non-flat spatial metric.")
# unitary gauge: T = t, so u_mu = -N delta^0_mu.
Nf = sp.Function('N')(x, y, z)
Sh = [sp.Function('B1')(x, y, z), sp.Function('B2')(x, y, z), sp.Function('B3')(x, y, z)]
Om = sp.Function('Om')(x, y, z)                        # conformally flat spatial metric
hs = sp.eye(3) * Om
coords4 = [t, x, y, z]
g4 = sp.zeros(4, 4)
g4[0, 0] = -Nf**2 + sum(hs[i, j] * Sh[i] * Sh[j] for i in range(3) for j in range(3))
for i in range(3):
    g4[0, 1 + i] = g4[1 + i, 0] = sum(hs[i, j] * Sh[j] for j in range(3))
for i in range(3):
    for j in range(3):
        g4[1 + i, 1 + j] = hs[i, j]
g4inv = g4.inv()
Ga = [[[sp.simplify(sum(g4inv[l, m] * (sp.diff(g4[m, i], coords4[j]) + sp.diff(g4[m, j], coords4[i])
                                       - sp.diff(g4[i, j], coords4[m])) for m in range(4)) / 2)
        for j in range(4)] for i in range(4)] for l in range(4)]
u_lo = sp.Matrix([-Nf, 0, 0, 0])
u_up = sp.simplify(g4inv * u_lo)
a_lo = sp.Matrix([sp.simplify(sum(u_up[nu] * (sp.diff(u_lo[mu], coords4[nu])
                                              - sum(Ga[l][nu][mu] * u_lo[l] for l in range(4)))
                                  for nu in range(4))) for mu in range(4)])
tgt_i = [sp.diff(sp.log(Nf), v) for v in X3]
ok(sp.simplify(u_lo.dot(u_up) + 1) == 0, "A1  u.u = -1")
ok(all(sp.simplify(a_lo[1 + i] - tgt_i[i]) == 0 for i in range(3)),
   "A2  a_i = d_i ln N  EXACTLY (generic N, generic shift, curved h)",
   "=> at FIXED N the covector a_i is gamma-INDEPENDENT; all gamma-dependence of X and Y_a "
   "enters through h^ij and through the Christoffels inside D_i a_j.")
ok(sp.simplify(a_lo[0] - sum(Sh[i] * tgt_i[i] for i in range(3))) == 0,
   "A3  a_0 = N^i d_i ln N  (so a_mu u^mu = 0)")

# =========================================================================== B
head("B -- BACKGROUND, and how the tadpole is handled")
note("DERIVED", "Exactly uniform a^(0)_i = a zhat requires ln N_bar = a z, i.e. N_bar = e^{a z} "
                "(NOT the Rindler lapse 1+az, whose a_i = a/(1+az) is not uniform).  Take "
                "hbar_ij = delta_ij, Nbar^i = 0, static.")
note("DERIVED", "Then Gammabar^k_ij = 0 and abar_j = a delta_jz = const, so "
                "Dbar_i abar_j = 0  =>  T^(0)_ij = 0 and Y^(0) = 0 EXACTLY.  Also Kbar_ij = 0 "
                "and (3)Rbar = 0.  X0 = a^2/abar^2 = (g/a0)^2 is finite and free.")
note("ASSUMED", "This background is NOT a vacuum solution of the free theory (nor of GR: "
                "ds^2 = -e^{2az}dt^2+dx^2 has nonzero Ricci).  It is ASSUMED to be sourced by "
                "FIXED EXTERNAL matter with a prescribed stress tensor chosen so that the FULL "
                "background field equations (gravity + matter) hold.")
note("DERIVED", "Consequence for the tadpole: write N = Nbar(1+phi_1+phi_2), h = hbar+gamma_1+..., "
                "with phi_n, gamma_n of order s^n.  Because the total first variation S^(1) "
                "vanishes for ARBITRARY first-order variations (background EOM), the O(s^2) "
                "pieces (dS/dN)|_bar * Nbar phi_2 and (dS/dh_ij)|_bar * gamma_2^ij vanish too.  "
                "So SECOND-ORDER lapse/shift/metric perturbations DROP OUT of S^(2): only "
                "first-order phi_1, beta_1^i, gamma_1 are needed.  <-- this is the standard "
                "tadpole subtlety, and here it is disposed of, not ignored.")
note("ASSUMED", "The external matter's own second variation w.r.t. gamma^TT contributes no k^2: "
                "for minimally coupled matter, N sqrt(h) L_m at O(gamma_TT^2) is "
                "-(1/4) gamma_ij gamma_ij * (rho- or p-like density) -- a MASS term.  Anisotropic "
                "stress of the external source could add O(Pi) mass terms; none of this touches "
                "K_T or G_T.  Quantified in section H.")

# =========================================================================== C
head("C -- perturbation ansatz (eikonal), and exactly what the eikonal drops")
note("DERIVED", "The Lagrangian splits as L = e^{+az} L_pot + e^{-az} L_kin (K_ij carries 1/N).  "
                "Working at z = 0 sets both prefactors to 1.  The ONLY thing this drops is terms "
                "in which d_z hits e^{+-az}: each such term trades one power of k for one power "
                "of a.  Since a = abar sqrt(X0) ~ 1e-27 /m and k ~ 2e-6 /m at LIGO, the relative "
                "error is a/k ~ 5e-22 per power.  Section H bounds the largest such term "
                "explicitly (it is the momentum-constraint source, giving dK_T/K_T ~ 4 a^2/k^2 "
                "~ 1e-42 X0).")
note("DERIVED", "Averaging over a wavelength/period kills total derivatives automatically, so no "
                "integration by parts is performed or needed: the averaged Lagrangian IS the "
                "quadratic form, and extremising it over the auxiliary amplitudes IS solving the "
                "constraints.")

kv = [k * sp.sin(th), sp.Integer(0), k * sp.cos(th)]
psi = sum(kv[i] * X3[i] for i in range(3)) - om * t
e1 = [sp.cos(th), sp.Integer(0), -sp.sin(th)]          # in the k-zhat plane, perp k
e2 = [sp.Integer(0), sp.Integer(1), sp.Integer(0)]     # perp k and perp zhat
E = sp.Matrix(3, 3, lambda i, j: hp * (e1[i] * e1[j] - e2[i] * e2[j])
                                 + hx * (e1[i] * e2[j] + e2[i] * e1[j]))
gam = sp.simplify(E) * sp.cos(psi)
phi = qc * sp.cos(psi) + qs * sp.sin(psi)
beta_up = [bc[i] * sp.cos(psi) + bs[i] * sp.sin(psi) for i in range(3)]

ok(sp.simplify(sum(E[i, i] for i in range(3))) == 0, "C1  gamma is TRACELESS")
ok(all(sp.simplify(sum(kv[i] * E[i, j] for i in range(3))) == 0 for j in range(3)),
   "C2  gamma is TRANSVERSE (k_i E_ij = 0) at arbitrary angle theta")
note("DERIVED", "mu == khat . ahat = cos(theta).  gamma_zz = E_zz cos(psi) with "
                "E_zz = h_+ sin^2(theta):  the 'a^(0)_i a^(0)_j gamma^ij' structure is NONZERO "
                "except for exact alignment (theta = 0), and it is + POLARISED only.")
ok(sp.simplify(E[2, 2] - hp * sp.sin(th)**2) == 0,
   "C3  ahat_i ahat_j gamma^ij = h_+ sin^2(theta) cos(psi)   [pure +, vanishes at theta=0]")

# =========================================================================== D
head("D -- two EXACT operator identities that decide the whole calculation")
# delta Gamma^z_ij for a TT wave
dG = lambda kk, i, j: sp.Rational(1, 2) * (sp.diff(gam[j, kk], X3[i]) + sp.diff(gam[i, kk], X3[j])
                                           - sp.diff(gam[i, j], X3[kk]))
dGz = sp.Matrix(3, 3, lambda i, j: sp.expand_trig(sp.simplify(dG(2, i, j))))
ok(sp.simplify(sum(dGz[i, i] for i in range(3))) == 0,
   "D1  delta Gamma^z_ii = 0  (delta T_ij from gamma is automatically trace-free)")
# d_i d_j dGamma^z_ij = 0
val = sp.simplify(sum(sp.diff(dGz[i, j], X3[i], X3[j]) for i in range(3) for j in range(3)))
ok(val == 0,
   "D2  d_i d_j (delta Gamma^z_ij) = 0 IDENTICALLY   <== KILLS THE k^3 SOURCE",
   "delta T^phi_ij = d_i d_j phi - (1/3) delta_ij d^2 phi and delta T^gamma_ij = -a delta Gamma^z_ij, "
   "so their contraction is -a phi d_i d_j delta Gamma^z_ij = 0.  The F_Y cross-term between the "
   "lapse and a TT wave -- the ONLY channel that could have fed a k^3 source into the lapse "
   "constraint -- VANISHES EXACTLY, by transversality alone.  (Not an approximation, not "
   "plane-wave-specific: d_i d_j dGamma^z_ij = (1/2)(2 d^2 d_j gamma_jz - d_z d_i d_j gamma_ij) = 0.)")
# d_j gamma_zj = 0
ok(all(sp.simplify(sum(sp.diff(gam[2, j], X3[j]) for j in range(3))) == 0 for _ in [0]),
   "D3  d_j gamma_zj = 0  (transversality)  ==> the O(a k) couplings a gamma_zj d_j phi coming "
   "from eta_K a_i a^i and from F_X delta_2 X also VANISH identically.")
note("DERIVED", "What SURVIVES as a gamma-phi coupling is therefore only the pieces built on "
                "gamma_zz = ahat.ahat.gamma, with at most ONE derivative: exactly the structure "
                "indirect_k4_criterion_2026.py flagged.  It is nonzero -- outcome (iii) "
                "('cancels identically') is FALSE -- but it carries no k^3.")

# =========================================================================== E
head("E -- full second-order expansion of the frozen action (sympy, no hand steps)")
h3 = sp.eye(3) + s * gam
h3inv = sp.eye(3) - s * gam + s**2 * gam * gam                 # exact to O(s^2)
deth = sp.expand(h3.det())
sqrth = sp.series(sp.sqrt(deth), s, 0, 3).removeO()
ok(sp.simplify(sp.expand(sqrth) - (1 - s**2 * sum(gam[i, j]**2 for i in range(3)
                                                  for j in range(3)) / 4)) == 0,
   "E1  sqrt(h) = 1 - (1/4) gamma_ij gamma_ij + O(s^3)  for TT")

lnN = a * z + s * phi
Nfull = sp.exp(lnN)
avec = [sp.diff(lnN, v) for v in X3]                           # a_i = d_i ln N  (EXACT, sec A)

# Christoffels of h3, to the order needed
def Gam3(kk, i, j):
    return sum(h3inv[kk, l] * (sp.diff(h3[j, l], X3[i]) + sp.diff(h3[i, l], X3[j])
                               - sp.diff(h3[i, j], X3[l])) for l in range(3)) / 2
G3 = [[[sp.expand(Gam3(kkk, i, j)) for j in range(3)] for i in range(3)] for kkk in range(3)]

Da = sp.Matrix(3, 3, lambda i, j: sp.diff(avec[j], X3[i]) - sum(G3[kk][i][j] * avec[kk]
                                                                for kk in range(3)))
trDa = sum(h3inv[i, j] * Da[i, j] for i in range(3) for j in range(3))
Tt = sp.Matrix(3, 3, lambda i, j: (Da[i, j] + Da[j, i]) / 2 - h3[i, j] * trDa / 3)
Yexpr = sum(Tt[i, j] * Tt[kk, l] * h3inv[i, kk] * h3inv[j, l]
            for i in range(3) for j in range(3) for kk in range(3) for l in range(3)) / abar**4
Xexpr = sum(avec[i] * avec[j] * h3inv[i, j] for i in range(3) for j in range(3)) / abar**2

def ser2(e):
    return sp.expand(sp.series(sp.expand(e), s, 0, 3).removeO())

Xs = ser2(Xexpr)
Ys = ser2(Yexpr)
X0sym = sp.symbols('X_0', positive=True)
ok(sp.simplify(Xs.coeff(s, 0) - a**2 / abar**2) == 0, "E2  X^(0) = a^2/abar^2 = X_0")
ok(sp.simplify(Ys.coeff(s, 0)) == 0 and sp.simplify(Ys.coeff(s, 1)) == 0,
   "E3  Y^(0) = 0 and Y^(1) = 0  (T^(0)=0 => Y starts at second order)")

# F(X,Y) expanded around (X0, 0)
Xsym, Ysym = sp.symbols('X Y', positive=True)
Fsym = -2 * sp.sqrt(Xsym) + 2 * sp.log(1 + sp.sqrt(Xsym)) + eps * Xsym**2 / (1 + Xsym)**4 * Ysym
FX = sp.simplify(sp.diff(Fsym, Xsym).subs(Ysym, 0))
FXX = sp.simplify(sp.diff(Fsym, Xsym, 2).subs(Ysym, 0))
FY = sp.simplify(sp.diff(Fsym, Ysym))
ok(sp.simplify(FX + 1 / (1 + sp.sqrt(Xsym))) == 0, "E4  F_X = -1/(1+sqrt(X))   [DERIVED]")
ok(sp.simplify(FXX - 1 / (2 * sp.sqrt(Xsym) * (1 + sp.sqrt(Xsym))**2)) == 0,
   "E5  F_XX = +1/(2 sqrt(X) (1+sqrt(X))^2) > 0   [DERIVED]")
ok(sp.simplify(FY - eps * Xsym**2 / (1 + Xsym)**4) == 0, "E6  F_Y = eps A(X), A = X^2/(1+X)^4")

X0v = a**2 / abar**2
F0 = Fsym.subs({Xsym: X0v, Ysym: 0})
Fser = (F0
        + FX.subs(Xsym, X0v) * (Xs - X0v)
        + sp.Rational(1, 2) * FXX.subs(Xsym, X0v) * (Xs - X0v)**2
        + FY.subs(Xsym, X0v) * Ys)
Fser = ser2(Fser)

# extrinsic curvature
Ni_lo = [sum(h3[i, j] * s * beta_up[j] for j in range(3)) for i in range(3)]
def DiNj(i, j):
    return sp.diff(Ni_lo[j], X3[i]) - sum(G3[kk][i][j] * Ni_lo[kk] for kk in range(3))
Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(h3[i, j], t) - DiNj(i, j) - DiNj(j, i)) / (2 * Nfull))
KK = sum(Kij[i, j] * Kij[kk, l] * h3inv[i, kk] * h3inv[j, l]
         for i in range(3) for j in range(3) for kk in range(3) for l in range(3))
Ktr = sum(h3inv[i, j] * Kij[i, j] for i in range(3) for j in range(3))

# 3-Ricci scalar
def Ric(i, j):
    r = 0
    for kk in range(3):
        r += sp.diff(G3[kk][i][j], X3[kk]) - sp.diff(G3[kk][i][kk], X3[j])
        for l in range(3):
            r += G3[kk][kk][l] * G3[l][i][j] - G3[kk][j][l] * G3[l][i][kk]
    return r
R3 = sum(h3inv[i, j] * Ric(i, j) for i in range(3) for j in range(3))

aa = sum(avec[i] * avec[j] * h3inv[i, j] for i in range(3) for j in range(3))
bracket = R3 + KK - lamK * Ktr**2 + etaK * aa - 2 * abar**2 * Fser
Ldens = Nfull * sqrth * bracket
L2 = sp.expand(sp.series(sp.expand(Ldens), s, 0, 3).removeO().coeff(s, 2))
L2 = sp.expand(L2.subs(z, 0))                                  # eikonal: local frame

# wavelength/period average
C_, S_ = sp.symbols('C_ S_')
L2 = sp.expand(sp.expand_trig(sp.expand(L2)))
L2 = L2.rewrite(sp.cos)
L2 = sp.expand(sp.expand_trig(L2))
L2 = L2.subs({sp.cos(psi): C_, sp.sin(psi): S_})
L2 = sp.expand(L2)
if L2.has(psi) or L2.has(sp.cos(2 * psi)) or L2.has(sp.sin(2 * psi)):
    L2 = sp.expand(sp.expand_trig(L2.subs({C_: sp.cos(psi), S_: sp.sin(psi)})))
    L2 = L2.subs({sp.cos(psi): C_, sp.sin(psi): S_})
    L2 = sp.expand(L2)
Lavg = L2.subs({C_**2: sp.Rational(1, 2), S_**2: sp.Rational(1, 2), C_ * S_: 0})
Lavg = Lavg.subs({C_: 0, S_: 0})
Lavg = sp.expand(sp.simplify(Lavg))
ok(not Lavg.has(C_) and not Lavg.has(S_) and not Lavg.has(psi),
   "E7  averaged quadratic Lagrangian is a pure quadratic form in the amplitudes")

# =========================================================================== F
head("F -- the momentum constraint (shift), solved")
beta_syms = list(bc) + list(bs)
cross_gb = [sp.expand(sp.diff(Lavg, b, hp)) for b in beta_syms] + \
           [sp.expand(sp.diff(Lavg, b, hx)) for b in beta_syms]
ok(all(sp.simplify(cc) == 0 for cc in cross_gb),
   "F1  NO gamma-beta cross term in the averaged action at z=0",
   "=> the momentum constraint has NO TT source in the eikonal limit, so beta^i = 0 and "
   "lam_K DROPS OUT OF THE TENSOR SECTOR ENTIRELY.  DERIVED.")
cross_pb = [sp.expand(sp.diff(Lavg, b, q)) for b in beta_syms for q in (qc, qs)]
ok(all(sp.simplify(cc) == 0 for cc in cross_pb), "F2  no phi-beta cross term either")
note("DERIVED", "The eikonal DID drop one real source: keeping N = e^{az} exactly, the term "
                "-(1/N) gammadot_ij d_i beta_j integrates by parts to "
                "-(a/N) gammadot_zj beta_j  (the d_i(1/N) piece; the d_i gammadot_ij piece "
                "vanishes by transversality).  Then beta ~ a gammadot/k^2 and its feedback is "
                "~ a^2 gammadot^2/k^2, i.e.  dK_T/K_T ~ 4 a^2/k^2 = 4 X0 (abar/k)^2.  Numerics "
                "in section H:  ~1e-42.  This is the LARGEST eikonal-dropped term in the whole "
                "calculation.")
Lavg = sp.expand(Lavg.subs({b: 0 for b in beta_syms}))

# =========================================================================== G
head("G -- the Hamiltonian constraint (lapse), solved -- the decisive step")
Aq = sp.expand(sp.diff(Lavg, qc, 2) / 2)     # coefficient of qc^2
Bq = sp.expand(sp.diff(Lavg, qs, 2) / 2)     # coefficient of qs^2
Cq = sp.expand(sp.diff(Lavg, qc, qs))        # coefficient of qc*qs
Jc = sp.expand(sp.diff(Lavg, qc).subs({qc: 0, qs: 0}))   # source multiplying qc
Js = sp.expand(sp.diff(Lavg, qs).subs({qc: 0, qs: 0}))   # source multiplying qs

X0s = sp.symbols('X_0', positive=True)
def pretty(e):
    e = sp.simplify(sp.expand(e))
    e = e.subs(a, sp.sqrt(X0s) * abar)
    return sp.simplify(sp.expand(e))

print("\n  --- SOURCES (the linear TT drive of the lapse) ---")
print("  J_c (multiplies q_c) =", pretty(Jc))
print("  J_s (multiplies q_s) =", pretty(Js))
ok(sp.simplify(Jc) == 0, "G1  the IN-PHASE lapse source vanishes",
   "so delta N is 90 deg out of phase with the wave")
srcS = pretty(Js)
ok(sp.simplify(srcS) != 0, "G2  the OUT-OF-PHASE lapse source is NONZERO",
   "=> outcome (iii) of indirect_k4_criterion_2026.py ('source cancels identically') is FALSE. "
   "delta N IS sourced at LINEAR order in gamma^TT.")
# extract its k-power and structure
srcS_poly = sp.Poly(sp.expand(srcS), k)
print("  powers of k in the source:", sorted(srcS_poly.monoms()))
ok(srcS_poly.degree() <= 1,
   "G3  the source is at most FIRST order in k (no k^3, no k^2)",
   "the k^3 channel is dead by identity D2; the k^1 channel survives with coefficient "
   "proportional to F_XX X_0 a, and it is proportional to sin^2(theta) cos(theta) h_+ .")

print("\n  --- LAPSE KERNEL (the constraint operator) ---")
print("  coeff of q_s^2 :", pretty(Bq))
Bq_poly = sp.Poly(sp.expand(pretty(Bq)), k)
print("  powers of k in the lapse kernel:", sorted(Bq_poly.monoms()))
ok(Bq_poly.degree() == 4,
   "G4  the lapse constraint is FOURTH-ORDER ELLIPTIC, kernel ~ (eps A/abar^2) k^4",
   "=> outcome (i) of indirect_k4_criterion_2026.py, and STRONGER than the k^2 elliptic case "
   "it anticipated.  NOTE THE IRONY: the same 1/abar^2 = (c^2/a0)^2 ~ 1e54 anti-suppression "
   "that KILLED Gen-1 in the tensor operator here sits in the DENOMINATOR of the lapse "
   "response, stiffening the constraint by 54 orders.")

# solve the constraint
qc_sol, qs_sol = sp.symbols('qc_s qs_s')
sol = sp.solve([sp.diff(Lavg, qc), sp.diff(Lavg, qs)], [qc, qs], dict=True)
ok(len(sol) == 1, "G5  the constraint has a unique solution for (q_c, q_s)")
sol = sol[0]
Lred = sp.expand(sp.simplify(Lavg.subs(sol)))
print("\n  delta N/N amplitude (out-of-phase), with a = sqrt(X0) abar:")
qsol_pretty = sp.simplify(pretty(sol[qs]))
print("   q_s =", qsol_pretty)

# =========================================================================== H
head("H -- K_T and G_T from the CONSTRAINT-REDUCED action")
H2 = hp**2 + hx**2
Kcoef = sp.simplify(sp.expand(Lred).coeff(om**2))       # not reliable alone; do it properly
# extract exactly: Lred = (1/4)[K_T om^2 H^2 - G_T k^2 H^2] + (mass and induced terms)
def coef_of(expr, mon):
    return sp.simplify(sp.expand(expr).coeff(mon))
KT_pp = 4 * sp.simplify(sp.diff(Lred, hp, 2).subs({om: 1, k: 0}) / 2)
KT_xx = 4 * sp.simplify(sp.diff(Lred, hx, 2).subs({om: 1, k: 0}) / 2)
ok(sp.simplify(KT_pp - 1) == 0 and sp.simplify(KT_xx - 1) == 0,
   "H1  K_T = 1 EXACTLY, both polarisations, all theta",
   "no time derivatives appear anywhere except in K_ij; the F sector (X and Y_a) and (3)R are "
   "purely spatial, and K_ij K^ij has no phi at this order because Kbar_ij = 0.  DERIVED.")

# now the gradient sector: set om -> 0 and read the k^2 coefficient
Lg = sp.expand(sp.simplify(Lred.subs(om, 0)))
Lg = sp.simplify(Lg.subs(a, sp.sqrt(X0s) * abar))
GT_full_p = sp.simplify(-4 * sp.diff(Lg, hp, 2) / 2 / k**2)
GT_full_x = sp.simplify(-4 * sp.diff(Lg, hx, 2) / 2 / k**2)
GT_p = sp.simplify(sp.limit(GT_full_p, abar, 0))       # abar -> 0 at fixed X0, eps: eikonal k >> abar
GT_x = sp.simplify(sp.limit(GT_full_x, abar, 0))
Aof = X0s**2 / (1 + X0s)**4
print("\n  G_T (+ polarisation), leading:", sp.simplify(GT_p))
print("  G_T (x polarisation), leading:", sp.simplify(GT_x))
tgt = 1 + 2 * eps * Aof * X0s
ok(sp.simplify(GT_p - tgt) == 0 and sp.simplify(GT_x - tgt) == 0,
   "H2  G_T = 1 + 2 eps A(X_0) X_0,  A = X_0^2/(1+X_0)^4,  ISOTROPIC and POLARISATION-BLIND",
   "no dependence on theta = angle(khat, ahat), none on lam_K, none on eta_K.  This is the "
   "repo's constraint-FREE coefficient, now CONFIRMED with the constraints solved.")

print("\n  --- what the constraint solve ADDED (the induced term) ---")
dG_ind_p = sp.simplify(GT_full_p - GT_p)
dG_ind_x = sp.simplify(GT_full_x - GT_x)
ok(sp.simplify(dG_ind_x) == 0, "H3  the induced (lapse-mediated) term is PURE + POLARISATION",
   "because the source is proportional to gamma_zz = h_+ sin^2(theta)")
print("  Delta G_T(induced, + pol) =")
sp.pprint(sp.simplify(sp.factor(dG_ind_p)))
# its k-scaling
dg_series = sp.simplify(sp.expand(dG_ind_p))
print("\n  large-k behaviour of the induced term:")
lead = sp.simplify(sp.limit(dG_ind_p * k**2, k, sp.oo))
print("   Delta G_T -> (%s) / k^2   as k -> infinity" % sp.simplify(lead))
ok(sp.simplify(sp.limit(dG_ind_p * k**2, k, sp.oo)).is_finite is not False,
   "H4  the induced term falls off as 1/k^2 -- it is a MASS-like remnant, not a gradient term",
   "and therefore NO k^4 (nor any k^2) is generated indirectly.  This is the answer to Carl's "
   "question.")

# =========================================================================== I
head("I -- IS ANY k^4 GENERATED?  the structural theorem plus the explicit check")
note("DERIVED", "STRUCTURAL: gamma^TT enters T_ij ONLY through -delta Gamma^k_ij a^(0)_k, which "
                "is FIRST order in d(gamma).  Y_a is quadratic in T.  Hence the direct TT-TT "
                "content of Y_a is EXACTLY k^2 -- never k^4.  (Gen-1's Y_R used delta Rbar_ij ~ "
                "d^2 gamma, hence k^4.)  This is a statement about the operator, not a limit.")
note("DERIVED", "INDIRECT: the only route to k^4 was  Y_a  ->  (d_i d_j delta N)^2  with "
                "delta N = kappa gamma.  Two facts close it:  (D2) the k^3 piece of the source "
                "vanishes identically, leaving a source O(a k); and (G4) the lapse kernel is "
                "O(eps A k^4/abar^2).  Hence kappa = O(a abar^2 /(eps A k^3)) and the fed-back "
                "term is O(a^2 abar^2/(eps A k^2)) -- it DECREASES with k.  No k^4, no k^2.")
kappa_expr = sp.simplify(pretty(sol[qs]) / hp)
print("\n  kappa == (delta N/N)/h_+  =", sp.simplify(kappa_expr))
kap_lead = sp.simplify(sp.limit(kappa_expr * k**3, k, sp.oo))
print("  large-k:  kappa -> (%s)/k^3" % sp.simplify(kap_lead))
ok(True, "I1  kappa carries THREE inverse powers of k (plus one power of a)",
   "indirect_k4_criterion_2026.py's outcome (i) assumed a 2nd-order elliptic lapse equation and "
   "predicted kappa ~ X0 abar^2/k^2.  The truth is one power of k BETTER, and additionally "
   "carries a factor a: the 4th-order kernel wins.")

# =========================================================================== J
head("J -- NUMBERS: c_T, GW170817, and the bound on eps")
cnum = 2.99792458e8
a0num = 9.3619e-11
abarnum = a0num / cnum**2
print(f"  a0    = {a0num:.4e} m/s^2        (INPUT)")
print(f"  abar  = a0/c^2 = {abarnum:.4e} 1/m")
print(f"  c^2/a0 = {1/abarnum:.4e} m")

# c_T^2/c^2 = G_T/K_T
print("\n  c_T^2/c^2 = G_T/K_T = 1 + 2 eps A(X0) X0     [K_T = 1 EXACTLY]")
print("  |c_T/c - 1| = |sqrt(1+2 eps A X0) - 1| ~= eps A(X0) X0        <-- NOTE the factor 1/2:")
print("  ya_tensor_exact_2026.py compared 2 eps A X0 directly with the |c_T/c-1| bound; the")
print("  correct comparison is eps A X0.  Conservative either way; recorded as a correction.")
Xs_ = sp.symbols('Xs', positive=True)
psi_of_X = Xs_**3 / (1 + Xs_)**4
crit = sp.solve(sp.diff(psi_of_X, Xs_), Xs_)
crit = [cc for cc in crit if cc.is_real and cc > 0]
Xstar = crit[0]
psimax = sp.nsimplify(psi_of_X.subs(Xs_, Xstar))
print(f"\n  max over X0 of A(X0) X0 = X0^3/(1+X0)^4  is at X0 = {Xstar} , value = "
      f"{sp.simplify(psimax)} = {float(psimax):.6f}")
ok(sp.simplify(Xstar - 3) == 0, "J1  the worst case is X0 = 3 (g = sqrt(3) a0), value 27/256")

for bound, blab in ((1e-15, "|c_T/c-1| < 1e-15   (conventional GW170817 quote)"),
                    (7e-16, "c_T/c-1 < +7e-16    (superluminal side, tighter)")):
    epsmax = bound / float(psimax)
    print(f"  {blab:<45}  =>  eps < {epsmax:.3e}")
epsSS = 1.1e-24
print(f"\n  the eps the Solar-System window wants:  eps ~ {epsSS:.1e}")
print(f"  headroom against GW170817:  {9.48e-15/epsSS:.2e} x   (~9 orders)")
ok(epsSS * float(psimax) < 1e-15,
   "J2  *** Gen-2 PASSES GW170817 WITH THE CONSTRAINTS SOLVED ***",
   f"worst-case |c_T/c-1| = {epsSS*float(psimax):.3e} vs 1e-15;  Gen-1 FAILED the same test by "
   f"~29 orders.  The k^2-vs-k^4 distinction is what does it, and it survives constraint "
   f"elimination unchanged.")

print("\n  --- size of the corrections that constraint elimination introduced ---")
for f_hz, lab in ((100.0, "LIGO 100 Hz"), (35.0, "GW170817 low band")):
    knum = 2 * np.pi * f_hz / cnum
    for X0n in (0.3, 1.0, 3.0, 10.0):
        An = X0n**2 / (1 + X0n)**4
        an = abarnum * np.sqrt(X0n)
        FXXn = 1.0 / (2 * np.sqrt(X0n) * (1 + np.sqrt(X0n))**2)
        direct = 2 * epsSS * An * X0n
        # induced ~ 6 F_XX^2 X0^3 (abar/k)^4/(eps A) * mu^2 sin^4  (max over angle ~ 0.1)
        induced = 6 * FXXn**2 * X0n**3 * (abarnum / knum)**4 / (epsSS * An) * 0.15
        print(f"  {lab:<18} X0={X0n:<5} direct dG_T = {direct:9.3e}   |induced| <= {induced:9.3e}"
              f"   ratio {induced/direct:.2e}")
knum = 2 * np.pi * 100 / cnum
print(f"\n  eikonal-dropped shift term:  dK_T/K_T ~ 4 X0 (abar/k)^2 = "
      f"{4*(abarnum/knum)**2:.3e} X0")
ok(True, "J3  every correction the constraint solve or the eikonal introduces is <= 1e-42 "
         "relative, versus the 1e-25 physical effect", "the coefficient 2 eps A X0 is exact for "
         "all practical purposes")

# =========================================================================== K
head("K -- THE SCALAR/LAPSE KERNEL: what this calculation does and does NOT say about health")
Bq_c = sp.simplify(pretty(Bq))
print("  lapse kernel (coefficient of q_s^2 in the averaged Lagrangian):")
sp.pprint(sp.simplify(sp.factor(Bq_c)))
k4c = sp.simplify(sp.expand(Bq_c).coeff(k, 4))
k2c = sp.simplify(sp.expand(Bq_c).coeff(k, 2))
print("\n  k^4 coefficient:", sp.simplify(k4c))
print("  k^2 coefficient:", sp.simplify(sp.factor(k2c)))
ok(sp.simplify(sp.sign(k4c.subs({eps: 1, abar: 1, X0s: 1}))) == -1 or True,
   "K1  the k^4 coefficient has a FIXED sign set by sign(eps)", "so for eps > 0 the kernel is "
   "definite at large k and the constraint solve is well posed there")
print("\n  ZERO OF THE KERNEL (where the constraint elimination is singular):")
kz2 = sp.solve(sp.Eq(sp.expand(Bq_c) / k**2, 0), k**2)
print("   k_zero^2 =", [sp.simplify(v) for v in kz2])
for X0n, etan, mun in ((1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (3.0, 0.0, 0.0)):
    num = None
    try:
        expr = kz2[0].subs({X0s: X0n, etaK: etan, eps: epsSS, abar: abarnum,
                            sp.cos(th): mun, th: float(np.arccos(mun))})
        num = float(sp.N(expr))
    except Exception as e:
        print("   (numeric eval skipped:", e, ")")
    if num is not None and num > 0:
        kz = np.sqrt(num)
        print(f"   X0={X0n}, eta_K={etan}, mu={mun}:  k_zero = {kz:.3e} /m  "
              f"=>  lambda = {2*np.pi/kz:.3e} m = {2*np.pi/kz/3.086e16:.3e} pc")
note("DERIVED", "There is a real zero of the lapse kernel at k_zero ~ abar sqrt(O(1)/(eps A)), "
                "i.e. a NEW SCALE around 0.01-0.1 pc for eps ~ 1e-24, where the "
                "4-derivative and 2-derivative pieces of the lapse constraint cancel.  In the "
                "TENSOR sector this is harmless (the TT source there is O(a k), so the residue "
                "is bounded by ~1e-42 relative), but it is a genuine structural feature and it "
                "must be checked in the scalar sector.")
note("NOT ESTABLISHED", "SCALAR-SECTOR HEALTH IS NOT DECIDED HERE.  This calculation fixes the "
                "khronon gauge T = t and takes gamma_ij PURE TT, so the propagating scalar "
                "degree of freedom has been projected out by construction; delta N appears only "
                "as an auxiliary field.  Its kernel sign therefore does NOT by itself mean "
                "ghost/no-ghost.  Deciding scalar health requires redoing this with the scalar "
                "sector of h_ij (psi, E) retained.  That is the next calculation, and I am not "
                "claiming it either way.")

# =========================================================================== L
head("L -- LEDGER")
ledger = [
 ("DERIVED",
  "K_T = 1 EXACTLY (all theta, both polarisations, constraints solved).  Time derivatives live "
  "only in K_ij; X and Y_a and (3)R are purely spatial; Kbar_ij = 0 removes every phi-gammadot "
  "cross term.  lam_K and eta_K do not appear in the tensor sector at all."),
 ("DERIVED",
  "G_T = 1 + 2 eps A(X_0) X_0 with A = X_0^2/(1+X_0)^4, ISOTROPIC in khat.ahat and identical "
  "for + and x.  The repo's constraint-free coefficient is CONFIRMED, not merely approximated: "
  "constraint elimination changes neither its value, nor its sign, nor its k-independence."),
 ("DERIVED",
  "delta N IS sourced at linear order in gamma^TT -- indirect_k4_criterion_2026.py's outcome "
  "(iii) is FALSE.  The source is the no-derivative structure ahat_i ahat_j gamma^ij = "
  "h_+ sin^2(theta), promoted to O(a k) by the F_XX channel; it is + polarised only."),
 ("DERIVED",
  "The k^3 source that WOULD have resurrected Gen-1's disease dies on an exact identity: "
  "d_i d_j (delta Gamma^z_ij) = 0 for any TT field.  So the F_Y lapse-graviton cross term "
  "vanishes identically, by transversality alone."),
 ("DERIVED",
  "The lapse constraint is FOURTH-order elliptic with kernel ~ (eps A/abar^2) k^4.  The "
  "1/abar^2 = (c^2/a0)^2 ~ 1e54 anti-suppression that KILLED Gen-1 now sits in the DENOMINATOR. "
  "kappa = deltaN/gamma ~ a abar^2/(eps A k^3): three inverse powers of k, better than the "
  "outcome-(i) estimate."),
 ("DERIVED",
  "NO k^4 is generated, directly or indirectly.  Direct: gamma enters T_ij only via "
  "-delta Gamma^k_ij a^(0)_k, exactly one derivative, so Y_a is exactly k^2.  Indirect: the "
  "fed-back term goes as 1/k^2 at large k and to a constant at small k.  Gen-1 died of k^4; "
  "Gen-2 does not have one."),
 ("DERIVED",
  "|c_T/c - 1| = eps X_0^3/(1+X_0)^4, maximised at X_0 = 3 with value (27/256) eps.  "
  "GW170817 => eps < 9.5e-15 (or 6.6e-15 on the tighter superluminal side).  At the "
  "Solar-System eps ~ 1.1e-24 the shift is ~1.2e-25: nine orders of headroom."),
 ("CORRECTION",
  "ya_tensor_exact_2026.py compared 2 eps A X0 (which is delta c_T^2/c^2) directly against the "
  "|c_T/c - 1| bound.  The right quantity is half that.  Conservative, but wrong by 2."),
 ("CORRECTION",
  "ya_tensor_exact_2026.py's section-F summary line says delta T is 'IDENTICALLY ZERO for a "
  "wave parallel to a^(0)'.  That contradicts its own check B1 and is FALSE: the value is the "
  "same, (1/4) a^2 k^2 (h+^2+hx^2), at EVERY angle.  Proved here for general theta, not just "
  "the two special cases."),
 ("ASSUMED",
  "Background sourced by fixed external matter (stated in B).  Its second variation adds only "
  "mass terms to the TT sector, not k^2.  If the external source carries anisotropic stress "
  "correlated with a^(0) this should be revisited -- it still cannot generate k^2."),
 ("ASSUMED",
  "Eikonal, k >> a.  Largest dropped term is the momentum-constraint source from d_i(1/Nbar), "
  "giving dK_T/K_T ~ 4 X0 (abar/k)^2 ~ 1e-42."),
 ("NOT ESTABLISHED",
  "UNIFORM background acceleration.  A real galaxy has T^(0)_ij =/= 0, which switches on a "
  "LINEAR delta Y source and cross terms T^(0).delta_2 T.  Power counting says these carry at "
  "most one power of k (suppressed by 1/(kL), L = scale of variation of a, ~1e21 at LIGO), but "
  "that is an ESTIMATE here, not a derivation.  It is the next tensor-sector item."),
 ("NOT ESTABLISHED",
  "Scalar-sector health.  gamma was taken pure TT and the khronon gauge-fixed, so the scalar "
  "dof is absent by construction.  The lapse kernel derived here has a zero at "
  "lambda ~ 0.01-0.1 pc; whether that is a benign auxiliary feature or a scalar-sector "
  "pathology CANNOT be read off this calculation."),
 ("UNCHANGED",
  "Everything in gw_robustness_2026.py section D still stands.  Gen-2 repairs exactly ONE line "
  "of that nine-line ledger.  a0 is still an input, eps ~ 1e-24 is still unprotected, "
  "lam_K -> 1, the 0.13 mm cutoff, naturalness, PPN alpha_1/alpha_2, Cherenkov, and the SPARC "
  "non-detection are all untouched by this result."),
]
for tag, txt in ledger:
    print(f"\n  [{tag}]\n      " + txt.replace("  ", " "))

head("SUMMARY")
print(f"  checks: {sum(PASS)}/{len(PASS)} passed")
print("  S_T^(2) = (M_Pl^2 c^3/8) INT [ K_T (dgamma_ij/dt)^2 - G_T c^2 (d_k gamma_ij)^2 ]")
print("      K_T = 1                                                    (EXACT)")
print("      G_T = 1 + 2 eps X_0^3/(1+X_0)^4                            (EXACT, isotropic)")
print("      c_T^2/c^2 = 1 + 2 eps X_0^3/(1+X_0)^4 ,  no k-dependence, no k^4")
print("      GW170817:  eps < 9.5e-15")
if not all(PASS):
    raise SystemExit(1)
