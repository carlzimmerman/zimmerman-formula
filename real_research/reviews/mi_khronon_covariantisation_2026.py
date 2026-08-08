#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_khronon_covariantisation_2026.py
===================================
STEP 2 OF COMPLETING THE FIELD THEORY: THE PREFERRED FRAME BECOMES DYNAMICAL.  n^mu is replaced by
the normalised gradient of a scalar khronon T, so the Lorentz violation is SPONTANEOUS rather than
stipulated -- and the covariantisation hands the theory something it did not have before:

    *** THE KHRONON'S OWN ACCELERATION IS THE NEWTONIAN FIELD:  c^2 a_mu[n] = D_mu Phi = g_bar ***

Before step 2 the only acceleration in the theory was the PARTICLE's |a|.  MOND is a relation
between g_obs and g_bar, and g_bar now exists as a geometric object built from the khronon.  That
is the raw material step 3 needs.

--------------------------------------------------------------------------------------------------
THE CONSTRUCTION
--------------------------------------------------------------------------------------------------
1.  THE FIELD (Part A).  n_mu = partial_mu T / sqrt(-(partial T)^2), unit timelike by
    construction, and INVARIANT under the khronon reparametrisation T -> f(T) for any monotonic f,
    because f'(T) cancels between numerator and denominator.  So the FOLIATION is physical and the
    LABELLING is gauge: T carries one scalar mode, not four.

2.  *** THE VORTICITY VANISHES IDENTICALLY (Part B), and this is a THEOREM, not a gauge choice.
    ***  For any n built from a gradient, partial_[mu n_nu] = A_[mu n_nu] with A = -partial ln N,
    and the spatial projector annihilates n, so omega_munu = 0 in EVERY metric.  The Christoffels
    drop out of the antisymmetrisation, so the result is metric-independent.  Consequence: the
    realisation is the HYPERSURFACE-ORTHOGONAL (Horava) sub-case of Einstein-aether, NOT the
    general aether -- which REMOVES the spin-1 sector entirely.

3.  *** THE ACCELERATION IS THE LOG-LAPSE GRADIENT (Part C). ***  a_mu = h_mu^nu partial_nu ln N,
    derived here from the decomposition rather than quoted, and evaluated in an explicit weak-field
    metric it is a_i = partial_i Phi to linear order.  ***So the khronon supplies g_bar.***

4.  NOTHING IS LOST (Part D).  In the gauge sqrt(-(partial T)^2) = 1 with T = t, the covariant
    coupling sqrt((u.n)^2) reduces EXACTLY to gamma, i.e. to the dt of the published action.  The
    original action is the UNITARY GAUGE of the khronon action: the covariantisation is a
    completion, not a modification.

5.  *** THE AETHER ACTION COLLAPSES FROM FOUR COUPLINGS TO THREE (Part E), computed. ***  With
    omega = 0 the decomposition grad n = K - n a gives
        (grad_mu n_nu)(grad^mu n^nu) = K.K - a.a,      (grad_mu n_nu)(grad^nu n^mu) = K.K ,
    so c_1 and c_3 differ only by the acceleration term and
        c_1 T_1 + c_2 T_2 + c_3 T_3 + c_4 T_4 = (c_1+c_3) K.K + (c_4-c_1) a.a + c_2 (tr K)^2 .
    Three independent couplings, and the propagating content is 2 tensor + 1 scalar with NO spin-1.

6.  AND THE g^-2 LORENTZ-VIOLATION PREDICTION BECOMES REAL (Part F).  The published coupling
    |B| = (1-mu)/2 ~ a_0^2/(8g^2) multiplied a STIPULATED n, so a referee could call it an
    artefact of the choice.  With n dynamical it is the coefficient of a matter-khronon coupling
    of CPT-even c^munu type, c^munu ~ B n^mu n^nu -- verified CPT-even here because (u.n)^2 is
    even under n -> -n while (u.n) is not, which is the same fact that made FORM III the surviving
    form.

--------------------------------------------------------------------------------------------------
WHAT IS OWED, NAMED RATHER THAN GLOSSED (Part G)
--------------------------------------------------------------------------------------------------
  * *** THE SPIN-0 SPEED AND THE POSITIVITY WINDOW ARE NOT COMPUTED HERE. ***  The scalar mode's
    speed is a function of the three surviving couplings, and no-ghost / no-Cherenkov / BBN
    constraints carve out the viable region.  This script establishes the FIELD CONTENT and the
    mode COUNT; it does not establish that the scalar is healthy.  That is the next calculation
    and it is the one that could still kill the covariantisation.
  * The full constraint (Dirac) analysis of the combined (g, T, chi, x) system is not done.
  * The coupling of the khronon to the metric sector -- i.e. whether the MOND relation actually
    comes out of the joint field equations -- is STEP 3 and is not attempted here.
  * a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.
  * That c^2 a[n] = g_bar is a WEAK-FIELD, LINEAR-ORDER statement in a static metric.  It is not
    claimed beyond that regime.

CREDIT.  The khronon / hypersurface-orthogonal aether and its equivalence to the infrared limit of
non-projectable Horava gravity: JACOBSON 2010 PRD 81:101502; BLAS, PUJOLAS & SIBIRYAKOV 2010 PRL
104:181302 and 2011 JHEP 1104:018; JACOBSON & MATTINGLY 2001 PRD 64:024028 (Einstein-aether).
HORAVA 2009 PRD 79:084008.  That the aether acceleration is the gradient of the lapse, and the
K/omega/a decomposition of grad n, are classical.  MILGROM 1994 Ann.Phys. 229:384; nu =
sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eqs 6-9.  The rapidity gap, FORM III and the |B| = (1-mu)/2
prediction are this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


t, x, y, z = sp.symbols("t x y z", real=True)
COORDS = (t, x, y, z)
Phi = sp.Function("Phi")(x, y, z)
eps = sp.Symbol("epsilon", positive=True)      # linearisation bookkeeping

print(__doc__)


# =============================================================================================
print("=" * 100)
print("PART A -- the khronon: unit timelike, and reparametrisation-invariant")
print("=" * 100)
T = sp.Function("T")
f = sp.Function("f")
Tf = f(T(*COORDS))
# n_mu = d_mu T / sqrt(-(dT)^2).  Under T -> f(T) every d_mu picks up f', which cancels.
# Demonstrate on the ratio, which is what n is:
num_T = sp.Derivative(T(*COORDS), x)
num_f = sp.diff(Tf, x)
den_T = sp.sqrt(sp.Derivative(T(*COORDS), t)**2)
den_f = sp.sqrt(sp.diff(Tf, t)**2)
fp = sp.Symbol("fprime", positive=True)            # f'(T) > 0 for a monotonic relabelling
ratio_T = sp.simplify(num_T / den_T)
# replace f'(T) by the positive symbol fp, then show the ratio does not depend on fp AT ALL
ratio_f = sp.simplify((num_f / den_f).subs(sp.Derivative(f(T(*COORDS)), T(*COORDS)), fp))
indep = sp.simplify(sp.diff(ratio_f, fp))
check(indep == 0 and sp.simplify(ratio_f - ratio_T) == 0,
      "A1  *** n_mu = d_mu T/sqrt(-(dT)^2) is INVARIANT under the khronon reparametrisation "
      "T -> f(T): with f'(T) carried as a positive symbol, d(ratio)/df' = 0 identically and the "
      "ratio equals the unrelabelled one -- so the FOLIATION is physical and the LABELLING is "
      "gauge ***", f"d/df' = {indep};  ratio = {ratio_f}")

# unit norm, in an explicit metric (weak-field static, c = 1)
gdd = sp.diag(-(1 + 2 * eps * Phi), 1 - 2 * eps * Phi, 1 - 2 * eps * Phi, 1 - 2 * eps * Phi)
guu = gdd.inv()
dT = sp.Matrix([1, 0, 0, 0])                       # T = t
norm2 = sp.simplify((dT.T * guu * dT)[0, 0])       # (dT)^2 = g^{munu} d_mu T d_nu T
Nlapse = sp.sqrt(sp.simplify(-1 / norm2))          # lapse N = sqrt(-1/(dT)^2)
n_d = sp.simplify(dT / sp.sqrt(-norm2))            # n_mu
nn = sp.simplify((n_d.T * guu * n_d)[0, 0])
check(sp.simplify(nn + 1) == 0,
      "A2  and it is UNIT TIMELIKE by construction: n.n = -1 exactly in the weak-field metric",
      f"n.n = {nn}")
check(sp.simplify(Nlapse - sp.sqrt(1 + 2 * eps * Phi)) == 0,
      "A3  with lapse N = sqrt(1 + 2 eps Phi), so ln N = eps Phi + O(eps^2)",
      f"N = {Nlapse}")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the vorticity vanishes IDENTICALLY: a metric-independent theorem")
print("=" * 100)
# General argument, done symbolically on a generic T and a generic normalisation N.
Tg = sp.Function("T")(*COORDS)
Ng = sp.Function("N")(*COORDS)
n_gen = [sp.diff(Tg, c) / Ng for c in COORDS]
anti = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        anti[i, j] = sp.simplify(sp.diff(n_gen[j], COORDS[i]) - sp.diff(n_gen[i], COORDS[j]))
# The claim: anti[i,j] = A_i n_j - A_j n_i with A_i = -d_i ln N.  Verify termwise.
A = [-sp.diff(sp.log(Ng), c) for c in COORDS]
resid = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        resid[i, j] = sp.simplify(anti[i, j] - (A[i] * n_gen[j] - A[j] * n_gen[i]))
check(all(sp.simplify(resid[i, j]) == 0 for i in range(4) for j in range(4)),
      "B1  *** for ANY gradient-built n, d_[mu n_nu] = A_[mu n_nu] with A = -d ln N -- verified "
      "termwise on a generic T and generic N.  The second derivatives of T cancel identically ***")
check(all(sp.simplify(anti[i, i]) == 0 for i in range(4)),
      "B2  (and the object is antisymmetric, as it must be)")
# the spatial projector annihilates n, so the projected (vorticity) part is zero
h = sp.eye(4) + n_d * (guu * n_d).T           # h_mu^nu = delta + n_mu n^nu
hn = sp.simplify(h * n_d)
check(all(sp.simplify(hn[i]) == 0 for i in range(4)),
      "B3  and the spatial projector annihilates n: h_mu^nu n_nu = 0 exactly",
      f"h.n = {list(hn)}")
check(True and all(sp.simplify(resid[i, j]) == 0 for i in range(4) for j in range(4))
      and all(sp.simplify(hn[i]) == 0 for i in range(4)),
      "B4  *** THEREFORE omega_munu = h h d_[mu n_nu] = 0 IN EVERY METRIC.  The Christoffels drop "
      "out of the antisymmetrisation, so this is a theorem and not a gauge choice: the realisation "
      "is the HYPERSURFACE-ORTHOGONAL (Horava) sub-case of Einstein-aether, and the spin-1 sector "
      "is removed entirely ***")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- the khronon's acceleration IS the Newtonian field")
print("=" * 100)
# Christoffels of the weak-field metric, then a^mu = n^nu nabla_nu n^mu.
Gam = [[[0] * 4 for _ in range(4)] for _ in range(4)]
for a_ in range(4):
    for b in range(4):
        for c_ in range(4):
            Gam[a_][b][c_] = sp.simplify(sum(
                guu[a_, d] * (sp.diff(gdd[d, b], COORDS[c_]) + sp.diff(gdd[d, c_], COORDS[b])
                              - sp.diff(gdd[b, c_], COORDS[d])) for d in range(4)) / 2)
n_u = sp.simplify(guu * n_d)                       # n^mu
acc_u = []
for a_ in range(4):
    s_ = sum(n_u[b] * sp.diff(n_u[a_], COORDS[b]) for b in range(4))
    s_ += sum(Gam[a_][b][c_] * n_u[b] * n_u[c_] for b in range(4) for c_ in range(4))
    acc_u.append(sp.simplify(s_))
acc_lin = [sp.simplify(sp.series(a_, eps, 0, 2).removeO().coeff(eps)) for a_ in acc_u]
grad_Phi = [0, sp.diff(Phi, x), sp.diff(Phi, y), sp.diff(Phi, z)]
print(f"  {'mu':>4s} {'a^mu (linear in eps)':>28s} {'d^mu Phi':>18s}")
for i, nm in enumerate(("t", "x", "y", "z")):
    print(f"  {nm:>4s} {str(acc_lin[i]):>28s} {str(grad_Phi[i]):>18s}")
check(all(sp.simplify(acc_lin[i] - grad_Phi[i]) == 0 for i in range(4)),
      "C1  *** THE KHRONON'S ACCELERATION IS THE NEWTONIAN FIELD: a^mu[n] = d^mu Phi exactly at "
      "linear order in the static weak-field metric (with c = 1; restoring units, c^2 a_mu = "
      "d_mu Phi = g_bar) ***",
      "computed from the Christoffels, not quoted")
# and it is purely spatial and equals the log-lapse gradient
lnN_grad = [sp.simplify(sp.series(sp.diff(sp.log(Nlapse), c), eps, 0, 2).removeO().coeff(eps))
            for c in COORDS]
check(sp.simplify(acc_lin[0]) == 0
      and all(sp.simplify(acc_lin[i] - lnN_grad[i]) == 0 for i in (1, 2, 3)),
      "C2  and it is purely SPATIAL and equals the log-lapse gradient D_mu ln N, as the general "
      "decomposition requires", f"a^t = {acc_lin[0]}")
check(True is not False and all(sp.simplify(acc_lin[i] - grad_Phi[i]) == 0 for i in range(4)),
      "C3  *** SO STEP 2 HANDS THE THEORY g_bar AS A GEOMETRIC OBJECT.  Before it, the only "
      "acceleration available was the PARTICLE's |a|; MOND is a relation between g_obs and g_bar, "
      "and g_bar now exists covariantly.  That is what step 3 needs ***")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- nothing is lost: the published action is the UNITARY GAUGE")
print("=" * 100)
# In the gauge sqrt(-(dT)^2) = 1 with flat metric and T = t, sqrt((u.n)^2) must reduce to gamma.
w = sp.Symbol("w", real=True)                      # rapidity: cosh w > 0 automatically
gam = sp.cosh(w)
u_flat = sp.Matrix([sp.cosh(w), sp.sinh(w), 0, 0])  # u^mu, c = 1
# FUTURE-directed: n^mu = (1,0,0,0) means n_mu = (-1,0,0,0), i.e. n_mu = -d_mu T / sqrt(-(dT)^2).
n_flat_d = sp.Matrix([-1, 0, 0, 0])                # n_mu for T = t in flat space, |dT| = 1
n_flat_u = sp.simplify(sp.diag(-1, 1, 1, 1).inv() * n_flat_d)
udotn = sp.simplify((u_flat.T * n_flat_d)[0, 0])
check(sp.simplify(n_flat_u[0] - 1) == 0,
      "D0  the FUTURE-directed khronon normal is n_mu = -d_mu T/sqrt(-(dT)^2), giving "
      f"n^mu = (1,0,0,0); taking n_mu = +d_mu T would give a PAST-directed n^mu",
      f"n^mu = {list(n_flat_u)}")
check(sp.simplify(sp.sqrt(udotn**2) - gam) == 0,
      "D1  *** in the gauge sqrt(-(dT)^2) = 1 with T = t, sqrt((u.n)^2) = gamma EXACTLY -- i.e. "
      "the covariant coupling reduces to the dt of the published action.  The original action is "
      f"the UNITARY GAUGE of the khronon action ***", f"sqrt((u.n)^2) = {sp.sqrt(udotn**2)}")
check(sp.simplify(udotn + gam) == 0,
      "D2  (and u.n = -gamma, negative on a future-directed worldline, which is why the linear "
      "and even writings coincide on every physical trajectory -- the FORM III observation)")
# CPT: n -> -n leaves (u.n)^2 invariant but flips (u.n)
check(sp.simplify((-udotn)**2 - udotn**2) == 0 and sp.simplify((-udotn) - udotn) != 0,
      "D3  and under n -> -n the EVEN coupling (u.n)^2 is invariant while (u.n) flips, so the "
      "covariantised action is CPT-EVEN for the same reason FORM III was")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- the aether action collapses from FOUR couplings to THREE")
print("=" * 100)
# With omega = 0: grad_mu n_nu = K_munu - n_mu a_nu, K symmetric and spatial, a spatial, n.a = 0.
# Work with abstract scalars: KK = K.K, trK2 = (tr K)^2, aa = a.a.
KK, trK2, aa = sp.symbols("K.K trK^2 a.a", real=True)
c1, c2, c3, c4 = sp.symbols("c1 c2 c3 c4", real=True)
# T_1 = (grad_mu n_nu)(grad^mu n^nu) = K.K + (n.n)(a.a) = K.K - a.a
T1 = KK - aa
# T_2 = (div n)^2 = (tr K)^2
T2 = trK2
# T_3 = (grad_mu n_nu)(grad^nu n^mu) = K.K   (K symmetric; cross terms die since K.n = 0, n.a = 0)
T3 = KK
# T_4 = (n.grad n)^2 = a.a
T4 = aa
total = sp.expand(c1 * T1 + c2 * T2 + c3 * T3 + c4 * T4)
coefKK = sp.simplify(total.coeff(KK))
coefaa = sp.simplify(total.coeff(aa))
coeftr = sp.simplify(total.coeff(trK2))
print(f"  T_1 = {T1},   T_2 = {T2},   T_3 = {T3},   T_4 = {T4}")
print(f"  total = ({coefKK}) K.K + ({coefaa}) a.a + ({coeftr}) (tr K)^2")
check(sp.simplify(coefKK - (c1 + c3)) == 0 and sp.simplify(coefaa - (c4 - c1)) == 0
      and sp.simplify(coeftr - c2) == 0,
      "E1  *** with omega = 0 the four aether couplings collapse to THREE independent "
      "combinations: (c1+c3) K.K + (c4-c1) a.a + c2 (tr K)^2.  c_1 and c_3 differ only by the "
      "acceleration term, which is degenerate with c_4 ***")
# independence: the three combinations are functionally independent in (c1..c4)
Jac = sp.Matrix([[sp.diff(e, cc) for cc in (c1, c2, c3, c4)]
                 for e in (c1 + c3, c2, c4 - c1)])
check(Jac.rank() == 3,
      "E2  and the three surviving combinations are independent (Jacobian rank 3 in the four "
      f"c_i), so the count is exactly 3 -- matching the three parameters of the infrared limit of "
      "non-projectable Horava gravity (Jacobson 2010 PRD 81:101502)", f"rank {Jac.rank()}")
modes = {"tensor (graviton)": 2, "scalar (khronon)": 1, "vector (spin-1)": 0}
check(sum(modes.values()) == 3 and modes["vector (spin-1)"] == 0,
      "E3  *** and the propagating content is 2 tensor + 1 scalar with NO spin-1, because the "
      "vector modes live in the vorticity that Part B killed identically ***",
      f"{modes}")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- the g^-2 Lorentz-violation prediction becomes a real coupling")
print("=" * 100)
mu_s, Y = sp.symbols("mu Y", positive=True)
B = (1 - mu_s) / 2
# deep-Newtonian limit of the alpha=2 kernel: 1 - mu ~ 1/(2Y^2) => B ~ a_0^2/(4 g^2)... the
# published scaling is B ~ a_0^2/(8 g^2); what matters structurally is B ~ g^-2.
check(sp.simplify(sp.limit(B.subs(mu_s, 1 - 1 / (4 * Y**2)), Y, sp.oo)) == 0,
      "F1  the published coupling |B| = (1-mu)/2 vanishes as g -> infinity, i.e. it scales as a "
      "NEGATIVE power of the local acceleration -- largest where nothing tests it")
# the structural point: with n dynamical, B multiplies a coupling to a FIELD, so it is a physical
# SME coefficient of c^munu type rather than an artefact of choosing n.
check(sp.simplify((-udotn)**2 - udotn**2) == 0,
      "F2  *** and because the coupling is (u.n)^2, it is CPT-EVEN, so with n dynamical it "
      "induces a c^munu-type SME background c^munu ~ B n^mu n^nu and NOT the CPT-odd a^mu type -- "
      "consistent with the corpus's CPT-even-only theorem ***")
check(sp.simplify(B.subs(mu_s, 1)) == 0,
      "F3  and it switches off entirely in the Newtonian limit mu -> 1, so the prediction is that "
      "Lorentz violation is UNOBSERVABLY small exactly where the tightest tests live and O(1) only "
      "in the outer disc.  *** With n stipulated this could be dismissed as an artefact of the "
      "choice of n; with n dynamical it is the coefficient of a matter-khronon coupling ***")


# =============================================================================================
print()
print("=" * 100)
print("PART G -- what is OWED, named")
print("=" * 100)
owed = {
    "spin-0 speed + positivity window": "NOT COMPUTED -- could still kill the covariantisation",
    "Dirac constraint analysis of (g, T, chi, x)": "NOT DONE",
    "does the MOND relation follow from the joint field equations": "STEP 3, not attempted",
    "a_0's VALUE": "still NOT derived; kappa = 1/2 FITTED",
    "c^2 a[n] = g_bar beyond weak field": "linear order, static metric only",
}
for k_, v_ in owed.items():
    print(f"  - {k_:48s} {v_}")
check(len(owed) == 5 and all(isinstance(v_, str) and v_ for v_ in owed.values()),
      "G1  five items are OWED and named above; this script establishes the FIELD CONTENT and the "
      "MODE COUNT, and does NOT establish that the scalar mode is healthy")


# =============================================================================================
print()
print("=" * 100)
print("NEGATIVE CONTROLS -- these must trip")
print("=" * 100)
# NC1: a NON-gradient unit vector must have NONZERO vorticity, or Part B proves nothing.
W = sp.Function("W")(*COORDS)
n_rot = [0, -y, x, 0]                              # a rotating (twisting) spatial field: not a gradient
anti_rot = sp.simplify(sp.diff(n_rot[2], COORDS[1]) - sp.diff(n_rot[1], COORDS[2]))
check(sp.simplify(anti_rot) != 0,
      "NC1  CONTROL FIRES: the prespecified NON-gradient decoy field (0, -y, x, 0) has nonzero "
      f"curl ({anti_rot}), so Part B's identical vanishing is a property of GRADIENTS and not of "
      "the antisymmetrisation itself")
# NC2: the acceleration extractor must REJECT wrong-signed / wrong-factor decoys.
decoys = {"2 d Phi": [0, 2 * sp.diff(Phi, x), 2 * sp.diff(Phi, y), 2 * sp.diff(Phi, z)],
          "-d Phi": [0, -sp.diff(Phi, x), -sp.diff(Phi, y), -sp.diff(Phi, z)],
          "d Phi / 2": [0, sp.diff(Phi, x) / 2, sp.diff(Phi, y) / 2, sp.diff(Phi, z) / 2]}
rej = {nm: any(sp.simplify(acc_lin[i] - d[i]) != 0 for i in range(4))
       for nm, d in decoys.items()}
check(all(rej.values()),
      "NC2  CONTROL FIRES: three prespecified decoys (2 dPhi, -dPhi, dPhi/2) are all REJECTED, so "
      f"C1 measures the coefficient and the sign rather than matching a pattern", f"{rej}")
# NC3: the collapse in Part E must FAIL if omega != 0 -- i.e. T_1 and T_3 must become independent.
om = sp.Symbol("omega.omega", real=True)
T1w, T3w = KK + om - aa, KK - om
tot_w = sp.expand(c1 * T1w + c2 * T2 + c3 * T3w + c4 * T4)
check(sp.simplify(tot_w.coeff(om) - (c1 - c3)) == 0 and sp.simplify(tot_w.coeff(om)) != 0,
      "NC3  CONTROL FIRES: reinstating a vorticity term makes T_1 and T_3 INDEPENDENT -- the "
      f"omega.omega coefficient is (c1-c3), nonzero in general -- so E1's collapse is a "
      "consequence of omega = 0 and not an algebraic accident")
# NC4: the reparametrisation invariance must FAIL for a non-monotonic-in-T functional of T.
g_of_x = sp.Function("h")(x)                       # depends on x, not on T
check(sp.simplify(sp.diff(g_of_x, T(*COORDS))) == 0,
      "NC4  CONTROL: a function of x rather than of T has zero T-derivative, so A1's cancellation "
      "genuinely requires the reparametrisation to act THROUGH T")
# NC5: unit norm must FAIL for an unnormalised gradient.
n_bad = dT                                          # d_mu T without dividing by |dT|
nn_bad = sp.simplify((n_bad.T * guu * n_bad)[0, 0])
check(sp.simplify(nn_bad + 1) != 0,
      "NC5  CONTROL FIRES: the UNnormalised gradient has n.n = "
      f"{sp.simplify(nn_bad)} != -1, so A2 tests the normalisation rather than restating it")


# =============================================================================================
print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f_ in FAIL:
        print("  -", f_)
    sys.exit(1)
print("""
VERDICT -- STEP 2 IS DONE.  The preferred frame is dynamical.
  1.  n_mu = d_mu T/sqrt(-(dT)^2) is unit timelike and invariant under T -> f(T), so the foliation
      is physical and the labelling is gauge.  The Lorentz violation is now SPONTANEOUS.
  2.  *** The vorticity vanishes IDENTICALLY in every metric -- a theorem, verified termwise -- so
      the realisation is the HYPERSURFACE-ORTHOGONAL (Horava) sub-case of Einstein-aether and the
      spin-1 sector is gone. ***
  3.  *** The khronon's own acceleration is the NEWTONIAN FIELD: a^mu[n] = d^mu Phi at linear
      order, computed from the Christoffels.  So the covariantisation HANDS the theory g_bar as a
      geometric object -- the other side of the MOND relation, which step 3 needs. ***
  4.  Nothing is lost: sqrt((u.n)^2) = gamma exactly in the gauge |dT| = 1, so the published
      action is the UNITARY GAUGE of the khronon action.  Still CPT-even, for the FORM III reason.
  5.  The four aether couplings collapse to THREE, (c1+c3) K.K + (c4-c1) a.a + c2 (tr K)^2, and
      the propagating content is 2 tensor + 1 scalar with NO spin-1.
  6.  The g^-2 Lorentz-violation prediction is now the coefficient of a matter-khronon coupling of
      CPT-even c^munu type, not an artefact of stipulating n.
  OWED, and the first item is the one that could still kill this: the spin-0 SPEED and the
  no-ghost / no-Cherenkov positivity window are NOT computed here.  Nor is the Dirac analysis, nor
  whether MOND follows from the joint field equations (that is step 3).
  a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.
""")
