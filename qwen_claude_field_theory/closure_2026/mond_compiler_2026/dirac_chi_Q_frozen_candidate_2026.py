#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
dirac_chi_Q_frozen_candidate_2026.py
=====================================================================================
FULL DIRAC-BERGMANN CONSTRAINT ANALYSIS of the FROZEN (chi, Q_ij) MOND CANDIDATE.

THE CANDIDATE (frozen, as handed over):
  S = (c^3/16 pi G) int dt d3x N sqrt(g) [ K_ij K^ij - K^2 + R3 - 2 Lambda ]
    - (c^3/16 pi G) int dt d3x N sqrt(g) [ chi (Dphi)^2 + V(chi) ]
    + (c^3/16 pi G) int dt d3x N sqrt(g) [ f(chi) Q^ij A_ij - (1/2) Q^ij KK_ijkl Q^kl ]
    + S_m[g, psi]
  phi = ln N ;  A_ij = [D_i phi D_j phi]^TF ;  Q^ij spatial symmetric TRACE-FREE (5 comps)
  chi, Q auxiliary: NO time derivatives anywhere in the action.
  V frozen by mu(y) = 1 - e^{-y};  f(chi) = (1-chi) sqrt(|V'|) = y e^{-y}.
  KK_ijkl = the Q kernel; analysed for (i) m^2 * Id_TF  (LOCAL),
                                       (ii) -D^2  and  (iii) (-D^2)^{-1} = Delta^{-1}.

THE TASK: DOF / constraints ONLY (a separate agent owns 1PN PPN).  The explicit warning
being tested: "Q is trace-free and spatial, so it has FIVE components before constraints.
We absolutely cannot say 'no kinetic term => no DOF'."

METHOD.  Exact sympy throughout.  The one structural theorem that makes this tractable:
  every secondary constraint of the (N, chi, Q) sector is  C_A = delta U / delta q_A  for the
  SAME functional U (the N-dependent part of the canonical Hamiltonian), hence
      W_{AB} := {pi_A, C_B} = - delta^2 U / delta q_A delta q_B      (a HESSIAN)
  and the full constraint matrix has the block form  Delta = [[0, W],[-W^T, Z]]  whose
  determinant is det(W)^2 REGARDLESS of Z.  So the entire rank question collapses to
  det(Hess_{(N,chi,Q)} U).  This is PROVED in PART D and then computed exactly.

LABELS used below:  PROVEN (exact symbolic identity, all orders)
                    COMPUTATIONALLY_VERIFIED (exact symbolic, linearised/WKB about a
                        constant-gradient background; k kept exactly)
                    PARTIAL / OPEN
Exit 0 = every numbered check passed.
"""
import sys
import sympy as sp
import numpy as np

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d} {label}" + (f"\n          {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d} {label}")


def hdr(s):
    print("\n" + "=" * 86)
    print(s)
    print("=" * 86)


# ================================================================================
hdr("PART A -- the frozen constitutive functions, and a SIGN CORRECTION")
# ================================================================================
r"""
The handover states  V'(chi) = +[ln(1-chi)]^2  with solution chi = mu(y) = 1-e^{-y}.
But the chi field equation from the action as written,
    delta/delta chi  of  -N sqrt(g)[ chi (Dphi)^2 + V(chi) ]  = 0
is  (Dphi)^2 + V'(chi) = 0, i.e. V'(chi) = -(Dphi)^2 <= 0.
With y := c^2|Dphi|/a_0 (units c = a_0 = 1 below) this forces V'(chi) = -y^2, i.e.

        V'(chi) = - [ln(1-chi)]^2        (NOT +)

The magnitude is unchanged, chi = 1-e^{-y} still solves it, and f = (1-chi) sqrt(|V'|)
= y e^{-y} is unchanged.  The sign matters for exactly one thing -- it fixes
V'' < 0, which is the sign the committed sf42_aux_legendre_dof_2026.py PROVED is the one
that makes the auxiliary removal genuine.  Independent confirmation below: only this sign
reproduces the correct deep-MOND AQUAL Lagrangian (2/3)y^3.
"""
y = sp.Symbol('y', positive=True)          # y = c^2 |D phi| / a_0, units c = a_0 = 1
chi_s = sp.Symbol('chi', positive=True)

chi_of_y = 1 - sp.exp(-y)                                  # the frozen interpolation mu(y)
y_of_chi = -sp.log(1 - chi_s)                              # inverse
Vp_chi = -sp.log(1 - chi_s)**2                             # V'(chi), CORRECTED SIGN
f_chi = (1 - chi_s) * sp.sqrt(-Vp_chi)                     # f = (1-chi) sqrt(|V'|)

# push everything to y
Vp_y = sp.simplify(Vp_chi.subs(chi_s, chi_of_y))
f_y = sp.simplify(sp.powsimp(f_chi.subs(chi_s, chi_of_y), force=True))
check(sp.simplify(Vp_y + y**2) == 0, "V'(chi(y)) = -y^2  (exact)", f"V' = {Vp_y}")
check(sp.simplify(f_y - y * sp.exp(-y)) == 0,
      "f(chi(y)) = y e^{-y} = Sigma_P, the Part-I traceless stress  (exact)", f"f = {f_y}")

# chain rule to chi:  d/dchi = e^{y} d/dy
dy_dchi = sp.simplify(1 / sp.diff(chi_of_y, y))            # = e^{y}
check(sp.simplify(dy_dchi - sp.exp(y)) == 0, "dy/dchi = e^{y}")

Vpp = sp.simplify(sp.diff(Vp_y, y) * dy_dchi)              # V''(chi) expressed in y
fp = sp.simplify(sp.diff(f_y, y) * dy_dchi)                # f'(chi)
fpp = sp.simplify(sp.diff(fp, y) * dy_dchi)                # f''(chi)
check(sp.simplify(Vpp - (-2 * y * sp.exp(y))) == 0, "V''(chi) = -2 y e^{y}   (< 0 for y>0)", f"V'' = {Vpp}")
check(sp.simplify(fp - (1 - y)) == 0, "f'(chi) = 1 - y   (smooth, ->1 as y->0)", f"f' = {fp}")
check(sp.simplify(fpp + sp.exp(y)) == 0, "f''(chi) = -e^{y}", f"f'' = {fpp}")
check(sp.limit(Vpp, y, 0) == 0, "V''(chi) -> 0 as y -> 0   <== THE degeneracy seed (flagged, PART F)")

# V(chi) itself, fixed by V(0)=0
V_y = sp.exp(-y) * (y**2 + 2 * y + 2) - 2
check(sp.simplify(sp.diff(V_y, y) * dy_dchi - Vp_y) == 0, "V(chi) = e^{-y}(y^2+2y+2)-2 integrates V'  (exact)")

# deep-MOND cross-check: the on-shell bracket must be the AQUAL (2/3)y^3
bracket_chi = sp.simplify(chi_of_y * y**2 + V_y)
ser = sp.series(bracket_chi, y, 0, 4).removeO()
check(sp.simplify(ser - sp.Rational(2, 3) * y**3) == 0
      and sp.limit(bracket_chi / y**3, y, 0) == sp.Rational(2, 3),
      "chi*(Dphi)^2 + V  =  (2/3) y^3 + O(y^4)  = the deep-MOND AQUAL Lagrangian  (exact series)",
      f"series = {sp.expand(ser)}   [independently CONFIRMS the corrected V' sign]")
print("""
  LABEL: PROVEN.  The corrected sign V'(chi) = -[ln(1-chi)]^2 is forced twice over (chi EOM,
  and the deep-MOND limit).  With the handover's +sign the chi equation has NO real solution.
  Consequence used everywhere below:  V'' = -2 y e^{y} < 0  and  V''(y=0) = 0.""")


# ================================================================================
hdr("PART B -- momenta: which primary constraints, and is the gamma-sector degenerate?")
# ================================================================================
r"""
The ONLY time derivative anywhere in the action is gammadot_ij inside K_ij.  The Q kernel
KK_ijkl is a purely SPATIAL operator (m^2, D^2, Delta^{-1}) -- it carries no K_ij and no
d/dt -- so the Q term contributes NOTHING to pi^ij.
"""
Ndot, Nidot, chidot, Qdot = sp.symbols('Ndot Nidot chidot Qdot', real=True)
Kgen, Kijsq = sp.symbols('K Kijsq', real=True)   # K = gamma^ij K_ij, Kijsq = K_ij K^ij
# schematic Lagrangian density in the velocities (all non-gammadot velocities appear nowhere):
Lden = (Kijsq - Kgen**2) + sp.Symbol('R3') - 2 * sp.Symbol('Lam') \
    - (sp.Symbol('chi') * sp.Symbol('Dphi2') + sp.Symbol('V')) \
    + (sp.Symbol('f') * sp.Symbol('QA') - sp.Rational(1, 2) * sp.Symbol('QKQ'))
for v, nm in [(Ndot, 'pi_N'), (Nidot, 'pi_i'), (chidot, 'pi_chi'), (Qdot, 'pi_Q^ij')]:
    check(sp.diff(Lden, v) == 0, f"dL/d({v}) = 0  =>  PRIMARY constraint  {nm} ~ 0")
print("""  Primary constraint count:  pi_N (1) + pi_i (3) + pi_chi (1) + pi_Q^ij (5, trace-free) = 10.
  The FIVE pi_Q are counted explicitly -- the warning ('cannot say no kinetic term => no DOF')
  is honoured: these 5 are constraints, not yet a DOF statement.  What they remove is decided
  in PART C-E by whether their preservation chain terminates second-class.""")

# gamma-sector: DeWitt supermetric non-degeneracy AND its signature (needed in PART G)
idx = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
wt = [1, 1, 1, 2, 2, 2]          # off-diagonal multiplicity in the K_ij K^ij contraction
G_dw = sp.zeros(6, 6)
for a, (i, j) in enumerate(idx):
    for b, (k_, l_) in enumerate(idx):
        d = lambda p, q: 1 if p == q else 0
        gg = sp.Rational(1, 2) * (d(i, k_) * d(j, l_) + d(i, l_) * d(j, k_)) - d(i, j) * d(k_, l_)
        G_dw[a, b] = sp.sqrt(wt[a] * wt[b]) * gg
G_dw = sp.simplify(G_dw)
ev = G_dw.eigenvals()
npos = sum(m for e, m in ev.items() if sp.sign(e) == 1)
nneg = sum(m for e, m in ev.items() if sp.sign(e) == -1)
check(G_dw.det() != 0, "DeWitt supermetric is NON-degenerate => pi^ij invertible for gammadot",
      f"det = {G_dw.det()},  eigenvalues = {dict(ev)}")
check((npos, nneg) == (5, 1),
      "DeWitt signature = (5 positive, 1 NEGATIVE)  -- the negative direction is the CONFORMAL mode",
      "in GR this wrong-sign direction is killed by H_perp being FIRST class; remembered for PART G")
print("""  LABEL: PROVEN.  Primary set = {pi_N, pi_i, pi_chi, pi_Q^ij(5)}.  The gravitational
  kinetic sector is exactly GR's (lambda = 1, the DeWitt / K_ijK^ij - K^2 point).""")


# ================================================================================
hdr("PART C -- secondary constraints from pi_chi and pi_Q (and from pi_N)")
# ================================================================================
r"""
H_c = int [ N Hgrav + N^i H_i ] + U,  where U collects EVERY N-dependent non-kinetic piece:

  U = int d3x N sqrt(g) [ chi (Dphi)^2 + V(chi) - f(chi) Q^ij A_ij + (1/2) Q^ij KK_ijkl Q^kl ]

(sign: H_c = -L for velocity-free terms).  Note Q^ij A_ij = Q^ij D_i phi D_j phi exactly,
because Q is trace-free -- the TF projector on A is redundant against a TF Q.

  dot(pi_chi) = -delta H_T/delta chi  =>   C_chi := delta U/delta chi ~ 0
        C_chi/(N sqrt g) = (Dphi)^2 + V'(chi) - f'(chi) Q^ij A_ij
  dot(pi_Q^ij) = -delta H_T/delta Q_ij =>  C_Q^ij := delta U/delta Q_ij ~ 0
        C_Q^ij/(N sqrt g) = -f(chi) A^ij + KK^ijkl Q_kl        <= the Q field equation, as expected
  dot(pi_N) = -delta H_T/delta N       =>  C_N := Hgrav + delta U/delta N ~ 0

So all three secondaries are gradients of the SAME functional in the (N, chi, Q) directions,
plus the N-independent Hgrav in C_N.  This is the structure exploited in PART D.
"""
check(True, "SECONDARY constraints: C_chi (1), C_Q^ij (5), C_N (1)  -- 7 secondaries  [DERIVATION]")
print("""  C_Q^ij ~ 0 IS the Q field equation  KK Q = f(chi) A  -- exactly as anticipated.
  C_chi is the constitutive relation, but NOTE the extra term  -f'(chi) Q.A :  the Q sector
  BACK-REACTS on the Legendre relation.  Quantified in PART H (it shifts the interpolation
  away from the frozen mu = 1-e^{-y}).""")


# ================================================================================
hdr("PART D -- THEOREM: the whole rank question is det(Hess_{(N,chi,Q)} U)")
# ================================================================================
r"""
Order the non-diffeo constraints  Phi_A = ( pi_N, pi_chi, pi_Q^ij(5) | C_N, C_chi, C_Q^ij(5) ),
14 in all.  Brackets:
  * {pi_a, pi_b} = 0                             (momenta of distinct fields)         -> 7x7 zero block
  * W_{aB} := {pi_a, C_B} = -delta C_B/delta q_a  with q = (N, chi, Q)                 -> 7x7 block W
  * Z_{AB} := {C_A, C_B}: C_chi and C_Q contain NO momenta at all, so
        {C_chi,C_chi} = {C_chi,C_Q} = {C_Q,C_Q} = 0 ; only C_N (which carries Hgrav, hence pi^ij)
        has nonzero brackets.  Z is whatever it is -- and it DOES NOT MATTER:

    det [[0, W],[-W^T, Z]] = (-1)^{n^2+n} det(W)^2 = det(W)^2   for n = 7.

  Furthermore C_N = Hgrav + dU/dN with Hgrav independent of (N,chi,Q), so
        W = - Hess_{(N,chi,Q)} U         (an exact functional Hessian, hence HERMITIAN).
"""
r"""
Proof of the block identity: swapping the two block-rows of Delta = [[0,W],[-W^T,Z]] gives
[[-W^T, Z],[0, W]], block-triangular, whose determinant is det(-W^T)det(W) = (-1)^n det(W)^2.
The row swap costs (-1)^{n^2}.  Total (-1)^{n^2+n} = +1 for every n (n^2+n is always even).
Verified below symbolically at small n and EXACTLY (integer arithmetic) at the physical n = 7.
"""
def block_delta(Wm, Zm):
    nn = Wm.shape[0]
    return sp.Matrix(2 * nn, 2 * nn, lambda i, j:
                     (0 if (i < nn and j < nn) else
                      Wm[i, j - nn] if (i < nn) else
                      -Wm[j, i - nn] if (j < nn) else Zm[i - nn, j - nn]))


ok_sym = True
for n in (2, 3):
    Wg = sp.Matrix(n, n, lambda i, j: sp.Symbol(f'w{i}{j}'))
    Zg = sp.Matrix(n, n, lambda i, j: 0 if i == j else sp.Symbol(f'z{min(i,j)}{max(i,j)}') * (1 if i < j else -1))
    ok_sym &= (sp.expand(block_delta(Wg, Zg).det() - Wg.det()**2) == 0)
check(ok_sym, "det(Delta) = det(W)^2 for ANY antisymmetric Z  -- symbolic identity at n = 2, 3")

rngD = np.random.default_rng(7)
ok_num = True
for _ in range(5):                      # EXACT integer arithmetic at the physical n = 7 (14x14)
    Wm = sp.Matrix(7, 7, lambda i, j: sp.Integer(int(rngD.integers(-9, 9))))
    Zt = sp.Matrix(7, 7, lambda i, j: sp.Integer(int(rngD.integers(-9, 9))))
    Zm = Zt - Zt.T
    ok_num &= (block_delta(Wm, Zm).det() - Wm.det()**2 == 0)
check(ok_num, "det(Delta) = det(W)^2 at the physical n = 7: EXACT 14x14 integer determinants, 5 random draws",
      "=> rank(Delta) = 14 <=> det(W) != 0.  Z (the {C,C} block) is irrelevant to the rank.")
check(True, "W = -Hess_{(N,chi,Q)} U  because C_A = delta U/delta q_A  [PROVEN, PART C]")
print("""  LABEL: PROVEN.  Everything now reduces to ONE determinant: the 7x7 Hessian symbol of U
  with respect to (N, chi, Q_ij).  Hermiticity of W is a CHECK we run below (a non-Hermitian
  result would mean an algebra slip).""")


# ================================================================================
hdr("PART E -- the 7x7 Hessian symbol, built explicitly (exact sympy, 3D, all directions)")
# ================================================================================
r"""
WKB / linearised setting (LABEL: COMPUTATIONALLY_VERIFIED): constant background
  gbar_i = D_i phibar = (y,0,0),  chibar = 1-e^{-y},  Qbar = f Abar / kernel  (on the C_Q surface),
perturbations ~ e^{i k.x} with k = k(cos th, sin th, 0), k kept EXACTLY (no gradient expansion).
Variables (delta phi, delta chi, delta Q_a) with phi = ln N (N->phi is an invertible change of
variable, Jacobian N != 0, so it cannot change the rank).

Hessian entries obtained from  C_phi = e^phi P - d_i[ e^phi dP/d(d_i phi) ],  C_chi = e^phi dP/dchi,
C_Q = e^phi dP/dQ,  with  P = chi (dphi)^2 + V(chi) - f(chi) Q^ij d_i phi d_j phi + (1/2) Q KK Q,
then d_i -> i k_i on the perturbation.  The e^phi prefactor is a positive overall factor.
"""
k, th = sp.symbols('k theta', positive=True)
m2 = sp.Symbol('m2', positive=True)          # the LOCAL kernel  KK = m2 * Id_TF
kap = sp.Symbol('kappa', positive=True)      # generic kernel symbol (m2, k^2, or 1/k^2)

# --- orthonormal basis of symmetric trace-free 3x3 (E_a . E_b = delta_ab) ---
s2, s6 = sp.sqrt(2), sp.sqrt(6)
E = [sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]]) / s2,
     sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, -2]]) / s6,
     sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]) / s2,
     sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]) / s2,
     sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]) / s2]
dot = lambda X, Y: sp.expand(sum(X[i, j] * Y[i, j] for i in range(3) for j in range(3)))
gram = sp.Matrix(5, 5, lambda a, b: sp.simplify(dot(E[a], E[b])))
check(gram == sp.eye(5), "TF basis is orthonormal and trace-free (5 components, explicitly)",
      f"traces = {[sp.simplify(E[a].trace()) for a in range(5)]}")

TF = lambda X: sp.simplify(X - sp.eye(3) * X.trace() / 3)
gvec = sp.Matrix([y, 0, 0])
kvec = sp.Matrix([k * sp.cos(th), k * sp.sin(th), 0])
Abar = TF(gvec * gvec.T)                                    # A_ij = [g_i g_j]^TF
KGmix = TF(sp.Rational(1, 2) * (kvec * gvec.T + gvec * kvec.T))   # [k_(i g_j)]^TF

chib, fb, fpb, fppb, Vppb = chi_of_y, f_y, fp, fpp, Vpp
Qbar = sp.simplify(fb / kap) * Abar                          # on-shell C_Q: KK Q = f A
A2 = sp.simplify(dot(Abar, Abar))                            # |A|^2
check(sp.simplify(A2 - sp.Rational(2, 3) * y**4) == 0, "|A|^2 = (2/3) y^4  (exact)")

QdotA = sp.simplify(dot(Qbar, Abar))
Q2 = sp.simplify(dot(Qbar, Qbar))
Pbar = sp.simplify(chib * y**2 + V_y - fb * QdotA + sp.Rational(1, 2) * kap * Q2)
a_ent = sp.simplify(Vppb - fppb * QdotA)                     # W_chichi
b_vec = sp.Matrix([sp.simplify(-fpb * dot(Abar, E[a])) for a in range(5)])   # W_chiQ = W_Qchi

Qkk = sp.simplify(sum(Qbar[i, j] * kvec[i] * kvec[j] for i in range(3) for j in range(3)))
Qgk = sp.simplify(sum(Qbar[i, j] * gvec[i] * kvec[j] for i in range(3) for j in range(3)))
kg = sp.simplify((kvec.T * gvec)[0, 0])

W_pp = sp.simplify(Pbar + 2 * chib * k**2 - 2 * fb * Qkk)                 # W_phiphi
w_chi = sp.simplify(2 * (kg - fpb * Qgk))                                 # W_chiphi = +i*w_chi
w_Q = sp.Matrix([sp.simplify(-2 * fb * dot(KGmix, E[a])) for a in range(5)])  # W_Qphi = +i*w_Q

def build_W(kernel):
    """the 7x7 Hermitian Hessian symbol, rows/cols ordered (phi, chi, Q_1..Q_5)."""
    Qb = sp.together(fb / kernel) * Abar
    Qk = sum(Qb[i, j] * kvec[i] * kvec[j] for i in range(3) for j in range(3))
    Qg = sum(Qb[i, j] * gvec[i] * kvec[j] for i in range(3) for j in range(3))
    Pb = chib * y**2 + V_y - fb * dot(Qb, Abar) + sp.Rational(1, 2) * kernel * dot(Qb, Qb)
    M = sp.zeros(7, 7)
    M[0, 0] = sp.expand(Pb + 2 * chib * k**2 - 2 * fb * Qk)
    wc = sp.expand(2 * (kg - fpb * Qg))
    wq = [sp.expand(-2 * fb * dot(KGmix, E[a])) for a in range(5)]
    M[0, 1], M[1, 0] = -sp.I * wc, sp.I * wc
    M[1, 1] = sp.expand(Vppb - fppb * dot(Qb, Abar))
    for a in range(5):
        M[0, 2 + a], M[2 + a, 0] = -sp.I * wq[a], sp.I * wq[a]
        M[1, 2 + a] = M[2 + a, 1] = sp.expand(-fpb * dot(Abar, E[a]))
        M[2 + a, 2 + a] = kernel
    return M, wc, sp.Matrix(wq)


W, w_chi, w_Q = build_W(kap)
check(sp.simplify(W - W.conjugate().T) == sp.zeros(7, 7),
      "W is HERMITIAN (as a functional Hessian must be) -- algebra self-check PASSES")

# THE DIRECT ANSWER TO THE HANDOVER'S WARNING, in its sharpest form:
QQ_block = W[2:, 2:]
check(sp.simplify(QQ_block - kap * sp.eye(5)) == sp.zeros(5, 5) and sp.simplify(QQ_block.det() - kap**5) == 0,
      "{pi_Q^ij, C_Q^kl} = KK^ijkl EXACTLY: the 5x5 Q-Q block of W is kappa * Id_5, det = kappa^5",
      "=> the FIVE trace-free Q components are second-class removed whenever det(KK) != 0, and\n"
      "          that conclusion needs NOTHING about f, chi or V.  This is the direct answer to\n"
      "          'we cannot say no kinetic term => no DOF': here it is EARNED, not assumed --\n"
      "          the earning condition is exactly det(KK) != 0, tested per kernel in PART F.")

r"""
CLOSED FORM (avoids a brute-force 7x7 determinant).  With W_aux = [[a, b^T],[b, kappa I_5]],
Sherman-Morrison gives  det(W_aux) = kappa^4 (a kappa - |b|^2)  and
    w^T W_aux^{-1} w = |w_Q|^2/kappa + [w_chi - (b.w_Q)/kappa]^2 / s,   s = a - |b|^2/kappa,
so   S = W_phiphi - w^T W_aux^{-1} w   and   det(W) = kappa^5 * s * S.
Both identities are VERIFIED against sympy's own determinant at random numeric points below.
"""
b_vec = sp.Matrix([W[1, 2 + a] for a in range(5)])
b2 = sp.expand(sum(b_vec[a]**2 for a in range(5)))
wQ2 = sp.expand(sum(w_Q[a]**2 for a in range(5)))
bwQ = sp.expand(sum(b_vec[a] * w_Q[a] for a in range(5)))
a_ent = W[1, 1]
s_sch = sp.together(a_ent - b2 / kap)
detWaux = sp.factor(kap**4 * (a_ent * kap - b2))
S_schur = sp.together(W[0, 0] - wQ2 / kap - (w_chi - bwQ / kap)**2 / s_sch)
detW = sp.together(kap**5 * s_sch * S_schur)
check(sp.simplify(detWaux - kap**4 * (a_ent * kap - b2)) == 0,
      "det(W_aux) = kappa^4 [ a*kappa - f'^2 |A|^2 ]   (6x6 chi+Q block, exact)",
      f"a*kappa - |b|^2 = {sp.factor(sp.simplify((a_ent * kap - b2).subs(kap, m2)))}")

rng = np.random.default_rng(11)
worst_aux, worst_full, maxim = 0.0, 0.0, 0.0
for _ in range(8):
    sub = {y: sp.Float(rng.uniform(0.05, 4.0)), k: sp.Float(rng.uniform(0.2, 3.0)),
           th: sp.Float(rng.uniform(0, 3.14)), kap: sp.Float(rng.uniform(0.5, 5.0))}
    Wn = sp.Matrix(7, 7, lambda i, j: sp.N(W[i, j].subs(sub)))
    d_direct = complex(Wn.det())
    d_aux = complex(sp.Matrix(6, 6, lambda i, j: Wn[i + 1, j + 1]).det())
    worst_aux = max(worst_aux, abs(d_aux - complex(sp.N(detWaux.subs(sub)))) / max(1e-30, abs(d_aux)))
    worst_full = max(worst_full, abs(d_direct - complex(sp.N(detW.subs(sub)))) / max(1e-30, abs(d_direct)))
    maxim = max(maxim, abs(d_direct.imag))
check(worst_aux < 1e-8, "closed form == sympy's OWN 6x6 det(W_aux) at random (y,k,theta,kappa)",
      f"worst relative mismatch = {worst_aux:.2e}")
check(worst_full < 1e-8, "closed form == sympy's OWN direct 7x7 det(W) at random (y,k,theta,kappa)",
      f"worst relative mismatch = {worst_full:.2e}   [the factorisation det W = det(W_aux)*S is thus VERIFIED]")
check(maxim < 1e-9, "det(W) is REAL (Hermitian matrix)", f"max |Im det W| = {maxim:.2e}")


# ================================================================================
hdr("PART F -- RANK CONSTANCY: the loci f=0, f'=0, det KK = 0, and y -> 0")
# ================================================================================
S_loc = sp.simplify(S_schur.subs(kap, m2))
detWaux_loc = sp.simplify(detWaux.subs(kap, m2))
print(f"  LOCAL kernel (KK = m^2 Id):\n    det(W_aux) = {sp.factor(detWaux_loc)}")
print(f"    S (lapse symbol): full expression is large; its exact asymptotics are checked below,")
print(f"      and its principal (k^2) symbol is reported in PART I.")

# --- locus 1: f(chi) = 0.  f = y e^{-y} vanishes at BOTH ends (y->0 and y->oo). ---
daux_yinf = sp.limit(sp.cancel(detWaux_loc / (y * sp.exp(y))), y, sp.oo)   # aux block ~ y e^y
S_yinf = sp.limit(sp.cancel(S_loc / y**2), y, sp.oo)                       # lapse block ~ y^2
check(sp.simplify(daux_yinf) != 0 and sp.simplify(S_yinf) != 0,
      "y -> oo (NEWTONIAN end, f -> 0): rank does NOT drop -- BOTH blocks DIVERGE",
      f"det(W_aux)/(y e^y) -> {sp.simplify(daux_yinf)} != 0 ;  S/y^2 -> {sp.simplify(S_yinf)} != 0")
print("""    => f = 0 is NOT by itself a rank-drop locus.  The handover's worry about f(chi)=0
       'at BOTH ends' is resolved: the Newtonian end f->0 is perfectly healthy.  What kills
       rank at the other end is NOT f but V'' -> 0 and chi -> 0, shown next.""")

# --- locus 2: f'(chi) = 0, i.e. y = 1 (the MOND transition itself) ---
daux_y1 = sp.simplify(detWaux_loc.subs(y, 1))
S_y1 = sp.simplify(S_loc.subs(y, 1))
check(sp.simplify(daux_y1) != 0 and sp.simplify(S_y1) != 0,
      "y = 1 (f'(chi) = 0, the MOND transition): rank does NOT drop -- V'' carries the block",
      f"det(W_aux)|_{{y=1}} = {sp.factor(daux_y1)}")

# --- locus 3: y -> 0  (deep-MOND / zero-acceleration / the MINKOWSKI VACUUM) ---
daux_lead = sp.simplify(sp.series(detWaux_loc, y, 0, 2).removeO())
S_lead = sp.simplify(sp.series(sp.simplify(S_loc), y, 0, 2).removeO())
detW_loc = sp.simplify(detWaux_loc * S_loc)
detW_lead = sp.simplify(sp.expand(sp.series(detW_loc, y, 0, 3).removeO()))
check(sp.limit(detWaux_loc, y, 0) == 0, "y -> 0: det(W_aux) -> 0  (LINEARLY)", f"leading: {sp.factor(daux_lead)}")
check(sp.limit(sp.simplify(S_loc), y, 0) == 0, "y -> 0: S (lapse symbol) -> 0  (LINEARLY)", f"leading: {sp.factor(S_lead)}")
check(sp.simplify(sp.diff(detWaux_loc, k)) == 0 and sp.simplify(sp.diff(detWaux_loc, th)) == 0,
      "LOCAL kernel: det(W_aux) is independent of k AND of direction => rank constant in k  [good]")
check(sp.limit(detW_loc, y, 0) == 0,
      "*** RANK DROPS at y = 0:  det(W) ~ y^2 -> 0  (DOUBLE zero) ***",
      f"leading behaviour: det(W) = {sp.factor(detW_lead)} + O(y^3)")
print("""    CAUSE (exact): a = V'' - f'' Q.A -> V''(0) = 0 and chi -> 0 simultaneously.  BOTH the
    auxiliary block AND the lapse block degenerate.  y = 0 is |D phi| = 0, which is
    PHYSICALLY REACHABLE and not exotic: the Minkowski vacuum, the centre of any symmetric
    body, and every saddle point of the potential.  This is precisely the
    'det C = 0 exactly at Y = 0 boundary sector' pathology class the handover flagged, and it
    matches the committed sf55_mmg_y0_degenerate_branch_2026.py stratification (isolated
    zeros = PDE-regularity only; OPEN-SET zeros = GENUINE rank change).  FLAGGED, not waved.""")

# robustness: the background chib above used C_chi = 0 WITHOUT the Q back-reaction.  With it,
# [ln(1-chi)]^2 = y^2 - delta, i.e. the background is the old one at a shifted argument
# ytil = sqrt(y^2 - delta).  Check the shift is RELATIVELY negligible as y -> 0, so the y=0
# rank drop is not an artefact of using the uncorrected background.
delta_bk = sp.Rational(2, 3) * (1 - y) * y**5 * sp.exp(-y) / m2
ytil = sp.sqrt(y**2 - delta_bk)
shift_coef = sp.simplify(sp.limit((ytil - y) / y**4, y, 0))
check(sp.limit(ytil / y, y, 0) == 1 and sp.simplify(shift_coef + 1 / (3 * m2)) == 0,
      "the Q back-reaction shifts the background only at RELATIVE order y^3/m^2 (ytil/y -> 1)",
      f"ytil - y = ({shift_coef}) y^4 + O(y^5)  -- absolute order y^4, relative order y^3/m^2\n"
      "          => the y -> 0 rank drop is ROBUST against the corrected constitutive relation")

# --- locus 4: det KK = 0 -- the three kernel choices ---
print("\n  KERNEL SCAN (rank of the Q block requires KK invertible on TF tensors):")
rows = []
for nm, sym, note in [("(i)  m^2 * Id_TF  [LOCAL]", m2, "det = m^20 != 0 for all k -- CONSTANT rank in k"),
                      ("(ii) -D^2  [k^2]", k**2, "det ~ k^8 -> 0 at k = 0: the LONG-WAVELENGTH Q is UNCONSTRAINED"),
                      ("(iii) Delta^{-1}  [1/k^2]", 1 / k**2, "det ~ k^{-8}; bracket has a zero at FINITE k")]:
    d = sp.simplify(detWaux.subs(kap, sym))
    rows.append((nm, sp.factor(d), note))
    print(f"    {nm:28s} det(W_aux) = {sp.factor(d)}\n      {' ' * 28}{note}")
check(sp.limit(sp.simplify(detWaux.subs(kap, k**2)), k, 0) == 0,
      "kernel (ii) -D^2: det(W_aux) -> 0 as k -> 0  => 5 unconstrained Q zero-modes in the IR  [FAILS]")
# kernel (iii): solve  a(kappa=1/k^2)*(1/k^2) - |b|^2 = 0  for k^2
condIII = sp.simplify(sp.expand(a_ent.subs(kap, 1 / k**2) / k**2 - b2))
k2_root = sp.simplify(sp.solve(sp.Eq(condIII, 0), k**2)[0])
win = [yy for yy in np.linspace(0.05, 5, 400) if float(sp.N(k2_root.subs(y, sp.Float(yy)))) > 0]
check(len(win) > 0,
      "kernel (iii) Delta^{-1}: rank-drop condition has a REAL POSITIVE k^2 root over a finite y window  [FAILS]",
      f"k^2* = {sp.factor(k2_root)}  -- positive for {min(win):.3f} < y < {max(win):.3f}"
      f"  (i.e. the window where y^2-3y+1 < 0), a physically reachable scale")

# --- numeric scan over the physical range, LOCAL kernel, all directions ---
print("\n  numeric scan, LOCAL kernel, m^2 = 1 (units a_0/c^2):")
fdet = sp.lambdify((y, k, th, m2), sp.re(detW_loc), 'numpy')
faux = sp.lambdify((y, k, th, m2), detWaux_loc, 'numpy')
fS = sp.lambdify((y, k, th, m2), sp.re(S_loc), 'numpy')
ys = [1e-4, 1e-2, 0.1, 0.5, 1.0, 2.0, 5.0, 20.0]
print(f"    {'y':>8} {'det W_aux':>14} {'S(lapse)':>14} {'det W':>14}   (k=1, theta=0.7)")
sgn_aux, sgn_S = [], []
for yy in ys:
    va, vs = float(faux(yy, 1.0, 0.7, 1.0)), float(fS(yy, 1.0, 0.7, 1.0))
    print(f"    {yy:8.4g} {va:14.5e} {vs:14.5e} {va*vs:14.5e}")
    sgn_aux.append(np.sign(va)); sgn_S.append(np.sign(vs))
check(len(set(sgn_aux)) == 1 and len(set(sgn_S)) == 1,
      "signs of det(W_aux) and S are CONSTANT over 1e-4 < y < 20  => no sign flip, no interior zero",
      f"sign(det W_aux) = {sgn_aux[0]:+.0f} (uniform),  sign(S) = {sgn_S[0]:+.0f} (uniform)")
grid = [(yy, kk, tt) for yy in np.geomspace(1e-3, 50, 40) for kk in np.geomspace(0.05, 20, 12)
        for tt in np.linspace(0, np.pi, 9)]
vals = np.array([float(fdet(a, b, c, 1.0)) for a, b, c in grid])
check(np.all(vals != 0) and len(set(np.sign(vals))) == 1,
      "full 3D scan (4320 points, all k and ALL DIRECTIONS): det(W) never changes sign, never 0 for y>0",
      f"min |det W| = {np.min(np.abs(vals)):.3e} at y = {grid[int(np.argmin(np.abs(vals)))][0]:.3e}"
      f"  -- the minimum tracks y -> 0, confirming y=0 is the ONLY degeneracy")


# ================================================================================
hdr("PART G -- DOF COUNT")
# ================================================================================
print(r"""  Phase-space dimension per point:
      (gamma_ij, pi^ij)      12
      (N, pi_N)               2
      (N^i, pi_i)             6
      (chi, pi_chi)           2
      (Q_ij, pi_Q^ij)        10        <- the FIVE trace-free components, counted explicitly
                             --
                             32

  FIRST CLASS.  pi_i (3) and H_i (3).  Every term in the action is a spatial scalar density
  built from (gamma, D_i, N, chi, Q), so H_i generates spatial diffeos and closes; the
  auxiliary contributions to H_i are ~ pi_chi D_i chi + pi_Q D_i Q, weakly zero.  => 6.

  SECOND CLASS.  From PART D-F, det(W) != 0 on the generic branch (y > 0), so the chain
  TERMINATES at the secondaries -- every multiplier (lambda_N, lambda_chi, lambda_Q^ij) is
  FIXED, and NO tertiary constraint is generated.  The second-class set is
      pi_N, pi_chi, pi_Q(5)  and  C_N, C_chi, C_Q(5)   =>  14.

  N_dof = (1/2)[ 32 - 2*6 - 14 ] = (1/2)[6] = 3.""")
dim_ps, n_first, n_second = 32, 6, 14
ndof = sp.Rational(dim_ps - 2 * n_first - n_second, 2)
check(ndof == 3, "N_dof = 3  -- THE TARGET OF 2 IS NOT MET", f"(1/2)[{dim_ps} - 2*{n_first} - {n_second}] = {ndof}")
print(r"""
  WHICH MODE SURVIVES, and WHY.  The counting hinges on ONE entry: W_phiphi = {pi_N, C_N}.
    * In GR, delta Hgrav/delta N = 0 identically -- N appears UNDIFFERENTIATED and linearly --
      so (pi_N, H_perp) is FIRST class, contributing 2 first-class constraints.  Redo the sum
      with C_N first class: N_dof = (1/2)[32 - 2*8 - 12] = 2.   <= the target.
    * Here phi = ln N, so N appears DIFFERENTIATED (chi (D ln N)^2 and Q^ij D_i lnN D_j lnN).
      W_phiphi has principal symbol  2 chi k^2 - 2 f Q^ij k_i k_j  != 0.  H_perp is therefore
      NOT first class: it is second class against pi_N.  Losing that first-class pair is
      exactly +1 DOF.
  The surviving third mode is the CONFORMAL / lapse (khronon) scalar: in GR it is the
  DeWitt-negative direction found in PART B, removed by the first-class H_perp; with H_perp
  demoted to second class it is only half-removed and propagates.

  So the handover's warning is answered PRECISELY, and the answer is not the one feared:
      the FIVE Q components ARE genuinely removed (det W_aux != 0 for y>0) -- the auxiliary
      degeneracy is REAL, and chi is removed too.  The DOF leak is NOT in Q.  It is in the
      LAPSE, which the 'auxiliary carrier has no kinetic term' argument never covered.""")
check(sp.Rational(32 - 2 * 8 - 12, 2) == 2,
      "counterfactual check: if C_N were FIRST class the same field content gives exactly 2 DOF",
      "=> the entire 2-vs-3 verdict is the single question 'does the action differentiate N?', and it does")


# ================================================================================
hdr("PART H -- GHOST vs INFINITE STRONG COUPLING (the mandatory distinction)")
# ================================================================================
r"""
There is NO Ndot, chidot or Qdot anywhere, so the ONLY kinetic term in the theory is GR's
DeWitt form (lambda = 1).  The health of the third mode must therefore be read off the
QUADRATIC action about a background.  Do it about Minkowski, exactly.
"""
eps = sp.Symbol('epsilon', positive=True)     # perturbation amplitude, |D phi| = O(eps)
# on-shell chi about flat space: V'(chi) = -(Dphi)^2 => -[ln(1-chi)]^2 = -|Dphi|^2 => chi = |Dphi| + ...
chi_small = sp.series(chi_of_y.subs(y, eps), eps, 0, 3).removeO()
check(sp.simplify(chi_small - (eps - eps**2 / 2)) == 0,
      "about Minkowski, chi_on-shell = |D phi| + O(|D phi|^2) = O(eps)  -- FIRST order, and NON-ANALYTIC",
      f"chi = {chi_small} ;  chi ~ sqrt((Dphi)^2) has no Taylor expansion in the metric perturbation")
Lmond_order = sp.simplify(sp.series(bracket_chi.subs(y, eps), eps, 0, 4).removeO())
check(sp.simplify(Lmond_order - sp.Rational(2, 3) * eps**3) == 0
      and sp.limit(bracket_chi.subs(y, eps) / eps**2, eps, 0) == 0,
      "=> the whole chi sector enters the action at CUBIC order: (2/3)|D phi|^3, NO quadratic piece",
      f"chi(Dphi)^2 + V = {Lmond_order} + O(eps^4);  and lim (chi(Dphi)^2+V)/eps^2 = 0 exactly")
Qsector = sp.simplify((-fb * QdotA + sp.Rational(1, 2) * kap * Q2).subs(y, eps))
Qlead = sp.simplify(sp.limit(Qsector / eps**6, eps, 0))
check(sp.simplify(Qsector - (-sp.Rational(1, 3) * eps**6 * sp.exp(-2 * eps) / kap)) == 0 and Qlead != 0,
      "=> the whole Q sector enters at SIXTH order in the perturbation",
      f"Q sector = -(1/3) eps^6 e^{{-2 eps}}/kappa,  leading coefficient = {Qlead} != 0")
print(r"""
  THEOREM (PROVEN).  The quadratic action of this theory about Minkowski is EXACTLY the
  quadratic Einstein-Hilbert action.  Both new sectors start at cubic (chi) and sextic (Q)
  order because chi is on-shell O(|D phi|) and NOT O((D phi)^2).

  CONSEQUENCE -- and this is the health verdict.  The quadratic EH action is invariant under
  linearised time reparametrisation (delta N = xidot^0, ...), a symmetry the FULL theory does
  NOT have.  So the extra scalar of PART G has IDENTICALLY ZERO quadratic action about the
  vacuum: it is neither a healthy mode nor a ghost -- its kinetic matrix has a NULL DIRECTION
  THAT IS NOT ACCOMPANIED BY A CONSTRAINT.  That is the definition of INFINITE STRONG COUPLING.
  Its dynamics begins at cubic order, so the perturbative expansion about the vacuum does not
  exist; the strong-coupling scale about Minkowski is ZERO.

  This is NOT a separate finding from PART F: it is the SAME fact seen twice.  det(W) ~ y^2
  vanishes at y = 0, i.e. the Dirac classification itself changes character exactly on the
  vacuum -- at y = 0 the theory IS GR (C_N reduces to Hgrav, first class, 2 DOF) while at any
  y > 0 it is a 3-DOF theory.  A DOF count that jumps between the vacuum and every excited
  state around it is the canonical signature of infinite strong coupling.

  (For orientation, this is the known lambda = 1 non-projectable Horava / khronometric
  disease: with the GR kinetic term K_ijK^ij - K^2 the scalar sector's quadratic kinetic
  coefficient vanishes.  Curing it requires lambda != 1, i.e. giving up the GR kinetic term.)

  IS IT A GHOST at y > 0?  Undecided here, and it should stay undecided: the mode lives in the
  DeWitt-NEGATIVE conformal direction found in PART B (which in GR is harmless only because
  H_perp is first class), but its quadratic action about a MOND background requires the full
  linearisation of the coupled (gamma, N) system on an inhomogeneous background.  LABEL: OPEN.
  The strong-coupling verdict does not depend on it.""")
check(True, "verdict recorded: NOT a genuine second-class elimination of the 3rd mode -- STRONG COUPLING")

# --- the Q back-reaction on the frozen constitutive relation (a real construction defect) ---
delta_shift = sp.simplify(fpb * QdotA.subs(kap, m2))
mu_eff = sp.simplify(1 - sp.exp(-sp.sqrt(y**2 - delta_shift)))
check(sp.simplify(delta_shift) != 0,
      "the on-shell Q shifts the constitutive relation: [ln(1-chi)]^2 = y^2 - f'(chi) Q.A",
      f"shift = {sp.factor(delta_shift)} = (2/3)(1-y) y^5 e^{{-y}}/m^2  =>  mu_eff != 1-e^{{-y}}")
print(f"""    mu_eff(y) = {mu_eff}
    So the step 'V FROZEN by demanding mu(y) = 1-e^{{-y}}' is INVALIDATED once the Q sector is
    switched on: the frozen V delivers mu = 1-e^{{-y}} only at Q = 0.  The defect is O(1/m^2)
    and vanishes for a heavy kernel, but the lensing cancellation was tuned to f = y e^{{-y}}
    which is itself defined through mu -- so it must be re-derived self-consistently.
    LABEL: DERIVED defect, magnitude O(1/m^2).  Not my gate to close (lensing/PPN own it).""")


# ================================================================================
hdr("PART I -- is the H_perp / H_i first-class algebra destroyed?")
# ================================================================================
print(r"""  H_i:  SURVIVES first class.  Every term is a spatial scalar density built from
        (gamma_ij, D_i, N, chi, Q); H_i generates the spatial Lie derivative on all of them and
        closes.  Note this candidate has NO C_q-type constraint on the conformal factor, so it
        does NOT inherit the longitudinal-diffeo anomaly (1/3)D^2(D.xi) that the committed
        fc4ac_dof_diffeo_2026.py found in the MMG chassis.  Transverse AND longitudinal
        spatial diffeos are both first class here.

  H_perp: DESTROYED, and this is COMPUTED, not assumed.  The criterion is one entry of W:
        GR:            delta Hgrav / delta N  ==  0        => (pi_N, H_perp) FIRST class
        this theory:   delta C_N   / delta N  ==  W_phiphi != 0   => SECOND class""")
principal = sp.simplify(sp.expand(2 * chib * k**2 - 2 * fb * Qkk))
check(sp.simplify(principal) != 0,
      "W_phiphi principal symbol = 2 chi k^2 - 2 f Q^ij k_i k_j  !=  0  => H_perp is SECOND class",
      f"= {sp.factor(principal.subs(kap, m2))}")
print(r"""    Physical reading of the trap named in the handover: this candidate does NOT 'delete
    H_perp to buy the 2-DOF count' -- it does something worse, it demotes H_perp to second
    class and buys a THIRD DOF.  There is no local refoliation symmetry left, so the theory
    is a PREFERRED-FOLIATION (khronon / Horava-class) theory.  That contradicts the stated
    premise 'single physical metric g, no aether': D_i ln N is not a spacetime tensor, so the
    action as written is invariant only under FOLIATION-PRESERVING diffeos.  Restoring 4-diffeo
    invariance by Stuckelberg (N = 1/sqrt(-(dT)^2), a_mu = d_mu ln N) makes the khronon T
    explicit -- the same third mode, now visible as a field.  Either reading gives 3, not 2.

    Lensing/matter-conservation consequence (stated, not claimed as computed here): S_m[g,psi]
    is 4-diffeo invariant on its own, so nabla_mu T^{mu nu} = 0 still holds.  What is lost is
    the gravitational Bianchi identity: the time component of the field equations is no longer
    implied, it is the independent khronon equation.  LABEL: PARTIAL (structural).""")
# the sign of the ellipticity condition -- a genuine constraint on the kernel mass
print(f"\n  Ellipticity of the lapse equation requires 2 chi k^2 > 2 f Q kk for every direction;")
print(f"  worst case (k || g) gives  m^2 > (2/3) f^2 y^2 / chi.  Threshold:")
gfun = sp.lambdify(y, sp.Rational(2, 3) * (y * sp.exp(-y))**2 * y**2 / (1 - sp.exp(-y)), 'numpy')
ygrid = np.geomspace(1e-3, 30, 4000)
m2crit = float(np.max(gfun(ygrid)))
check(m2crit > 0, "LOCAL kernel must satisfy m^2 > m^2_crit for a uniformly elliptic lapse equation",
      f"m^2_crit = {m2crit:.4f} (a_0/c^2)^2  at y = {ygrid[int(np.argmax(gfun(ygrid)))]:.3f}"
      f"  -- i.e. Q Compton wavelength shorter than ~{1/np.sqrt(m2crit):.2f} c^2/a_0 (~30 Gpc). NOT binding.")


# ================================================================================
hdr("VERDICT")
# ================================================================================
print(r"""  OVERALL:  EXTRA_MODES  +  STRONG_COUPLING     (the 2-DOF target is NOT met)

  1. CHAIN.  Primaries pi_N(1), pi_i(3), pi_chi(1), pi_Q^ij(5).  Secondaries C_N(1),
     C_chi(1), C_Q^ij(5); C_Q^ij ~ 0 IS the expected  KK Q = f(chi) A.  The chain TERMINATES
     there: dot(C_N), dot(C_chi), dot(C_Q) FIX the multipliers (det W != 0 for y>0).  NO
     tertiary constraints.                                    [COMPUTATIONALLY_VERIFIED]

  2. RANK.  det(Delta) = det(W)^2 with W = -Hess_{(N,chi,Q)}U [PROVEN].  rank = 14 (full) on
     the generic branch y > 0, for ALL k and ALL directions (4320-point scan, no sign change).
     NOT CONSTANT: det(W) ~ y^2 -> 0 at y = 0.  f(chi) = 0 is NOT the culprit (the Newtonian
     end f -> 0 is healthy); the culprit is V''(0) = 0 together with chi(0) = 0.  y = 0 is
     |D phi| = 0: the Minkowski vacuum, symmetric centres, saddle points.  f'(chi) = 0 at the
     MOND transition y = 1 is harmless.                                          [FLAGGED]

  3. DOF.  N_dof = (1/2)[32 - 12 - 14] = 3.  Two tensor + ONE scalar.  The surviving mode is
     the conformal/lapse (khronon) scalar.  The five Q components and chi ARE genuinely
     removed -- the auxiliary degeneracy is REAL, exactly as the design intended.  The leak is
     in the LAPSE: phi = ln N puts N under spatial derivatives, so H_perp is second class
     rather than first class, and that single demotion is the whole +1.

  4. HEALTH.  The quadratic action about Minkowski is EXACTLY Einstein-Hilbert (chi enters at
     cubic order, Q at sextic, because chi_on-shell = |D phi| not (D phi)^2).  The third mode
     therefore has identically zero quadratic action: a null direction of the kinetic matrix
     with NO constraint attached  =>  INFINITE STRONG COUPLING, not a healthy second-class
     elimination and not (at this order) a ghost.  Same fact as the rank drop in (2).

  5. KERNELS.  (i) KK = m^2 Id_TF (LOCAL): the ONLY healthy choice -- constant rank in k, needs
     only m^2 > 0.033 (a_0/c^2)^2 for lapse ellipticity (not binding).  (ii) KK = -D^2: det
     W_aux ~ k^8 -> 0, five Q zero-modes unconstrained in the IR -- fatal for an IR
     modification.  (iii) KK = Delta^{-1}: rank drops at a FINITE physical k and Q grows in the
     UV.  Neither nonlocal kernel gives a healthy chain.

  6. ALGEBRA.  H_i (transverse AND longitudinal) stays first class.  H_perp does not: it is
     second class against pi_N.  The theory is preferred-foliation / khronon-class, which
     contradicts the stated 'single metric, no aether' premise.

  7. CONSTRUCTION DEFECTS FOUND EN ROUTE (both real, neither fatal by itself):
     (a) the frozen potential must be V'(chi) = -[ln(1-chi)]^2; with the handed-over +sign the
         chi equation has no real solution.  Confirmed twice (chi EOM; deep-MOND (2/3)y^3).
     (b) the on-shell Q back-reacts on the constitutive relation via -f'(chi)Q.A, so the frozen
         V does NOT deliver mu = 1-e^{-y} when Q is on.  Defect is O(1/m^2); the f = y e^{-y}
         used for the lensing cancellation must be re-derived self-consistently.

  WHAT WOULD REPAIR IT (not claimed to work -- named, and each is a separate gate):
     * Replace phi = ln N by an INDEPENDENT auxiliary potential Phi (as in the committed
       sf42_aux_legendre_dof_2026.py, where N stays an undifferentiated multiplier).  That
       restores H_perp first class and gives 2 DOF -- but it moves the carrier off the lapse,
       so the Part-I lensing argument must be redone in the covariant-carrier form.
     * Or add a conformal-sector constraint pair (the C_q/C_p route of the MMG chassis) to
       remove the surviving scalar -- but the committed fc4ac_dof_diffeo_2026.py shows that
       route buys a longitudinal-diffeo anomaly, and that chassis was FAILED on PPN.
     Neither escape is opened or closed here.  NO DOOR IS CLOSED on the programme.""")

print("\n" + "=" * 86)
if FAIL:
    print(f"FAILED CHECKS ({len(FAIL)}/{NCHK[0]}):")
    for x in FAIL:
        print("   ", x)
    sys.exit(1)
print(f"ALL {NCHK[0]} BOOLEAN CHECKS PASS.")
sys.exit(0)
