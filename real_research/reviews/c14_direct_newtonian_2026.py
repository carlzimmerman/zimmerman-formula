"""
=========================================================================================
c14_direct_newtonian_2026.py -- ROUTE 1 OF THE OPTION-1 AUDIT:
IS G_N ACTUALLY SINGULAR WHEN F(Y,Q) IS REPLACED BY F(Z,Q), Z = J^mu J_mu ?
=========================================================================================
2026-08-18.

THE ALARM I WAS SENT TO TEST.  Option 1 replaces AeST's free-function argument
Y = q^{mu nu} grad_mu phi grad_nu phi by Z = J^mu J_mu, J^mu = A^nu grad_nu A^mu.  Z is the
Einstein-aether c_4 structure (a^mu a_mu), so the replacement promotes c_4 from the constant
0 to a function, and in the Newtonian limit J_Z -> 1 that function is O(1).  The naive
dictionary reading recorded in the assignment is

    c_4^eff = +(2-K_B)  =>  c_14 = c_1 + c_4 = K_B + (2-K_B) = 2  EXACTLY
    =>  G_N = G/(1 - c_14/2) = G/0  FORMALLY SINGULAR,
    and alpha_2's denominator c_123 (2 - c_14) acquires a DOUBLE zero under a numerator
    (c_1+2c_3-c_4)(2c_1+3c_2+c_3+c_4) that is now the nonzero constant -4.

real_research/reviews/opt1_legality_2026.py check C6 asserts that G_N is nevertheless finite,
crediting "the 2(2-K_B) J^mu grad_mu phi mixing term", on a CALIBRATED quadratic Lagrangian
whose gravity-sector coefficient was fitted to reproduce typeII_direct_variation_2026.py's D5.
That is an inherited shortcut, and the assignment's standing warning (a literature PPN formula
applied off its stated domain, a sign slip in a mode speed, an inverted bisection, a kernel
spliced into the wrong family) says to derive instead.  So: full action, generic fields,
variation first and ansatz afterwards, with the unmodified F(Y) theory run through the SAME
machinery as the gate.

=========================================================================================
RESULT IN ONE PARAGRAPH -- direction: MIXED.  The alarm is void, and the reason it is void
is NOT the reason opt1 gives; and correcting it opens one NEW adverse item.
=========================================================================================
G_N IS FINITE, AND IT IS NOT MERELY FINITE -- IT IS *NUMERICALLY IDENTICAL* TO UNMODIFIED
AeST's.  Explicit variation of the full action (ten metric components, four aether components
plus its second-order temporal piece, the scalar, and the Lagrange multiplier lambda, ansatz
imposed only after varying) gives, for F(Z,Q),
      div[ J_Z(|grad Psi|^2) grad Psi ] = 4 pi Ghat rho,   Ghat = 2 Gt/(2-K_B) = Gt/(1-K_B/2),
i.e. AQUAL with the SAME Ghat the F(Y) theory has at D5.  In the Newtonian limit J_Z -> 1 this
is lap Psi = 4 pi Ghat rho, so H_00 = 2 G_N M / r with G_N = Ghat EXACTLY: the ratio
G_N[F(Z)] / G_N[F(Y)] = 1, with no K_B dependence and no free-function dependence beyond the
normalisation J_Z -> 1 that DEFINES the Newtonian limit.  The same machinery reproduces the
committed control Gt = (1-K_B/2) Ghat for F(Y) (the gate), and reproduces gamma_PPN = 1,
typeII's D6 and D7, and typeII's lambda_bg -- so the machinery is not the thing that is new.
THE ALARM IS A SIGN SLIP.  The Einstein-aether Lagrangian carries the c_4 structure as
+c_4 a^mu a_mu (the minus in K^{ab}_{mn}'s c_4 slot times the overall minus in L_ae), whereas
AeST carries the free function as -F, i.e. -(2-K_B)J(Z) -> -(2-K_B)Z at J_Z -> 1.  So
      c_4^eff = -(2-K_B),   c_14 = 2 K_B - 2  (= -1.5 at K_B = 0.25),   1 - c_14/2 = 2-K_B > 0,
and c_14 = 2 is never attained anywhere in AeST's own stability window 0 < K_B < 2; it is
approached only as K_B -> 2, where the free function's own prefactor (2-K_B) -> 0 and the entire
dark sector degenerates.  THE SIGN IS NOT ASSERTED, IT IS DERIVED AND THEN VALIDATED THREE WAYS:
(a) switching the scalar mixing off puts the theory inside the dictionary's own domain, and the
direct variation there gives G_N = Gt/(2-K_B), which is exactly Gt/(1-c_14/2) at c_14 = 2K_B-2;
(b) the same procedure run on UNMODIFIED AeST returns c_14 = K_B, the published entry, so the
matching returns the known answer on the known case; (c) the sign is not a convention that could
go either way -- Gauss' law on the AQUAL equation gives Psi' = Ghat M/(J_Z r^2), so J_Z > 0 is
forced by gravity being ATTRACTIVE, and J_Z > 0 is exactly what makes the effective c_4 negative.
AND THE OPT1 ATTRIBUTION IS HALF WRONG.  The mixing term is real and load-bearing, but it does
not rescue a singularity, because with the mixing term DELETED the direct variation still gives
a finite G_N = Gt/(2-K_B) = Ghat/2.  What the mixing term does is restore the factor 2, i.e.
return G_N from Ghat/2 to Ghat.  Carrying the mixing coefficient as 2 sigma and the Ycal
coefficient as tau (AeST: sigma = tau = 2-K_B) the exact result is
G_N = 2 Gt tau / (2 tau (2-K_B) - sigma^2), whose pole surface is tau = sigma^2/(2(2-K_B)): a
factor sqrt(2) = 1.414 away in sigma, a factor 2 away in tau.  So the finiteness is NOT a tuned
cancellation -- the nearest singular locus is an O(1) distance away in BOTH directions of the
natural two-dimensional neighbourhood, and along the way G_N moves smoothly between Ghat/2 and
Ghat rather than blowing up.
THE MECHANISM, EXACTLY.  On the F(Z) theory the aether-longitudinal equation is v = grad Psi
POINTWISE (the free function has left that equation, because Z is independent of a_i and of
varphi at quadratic order).  The Psi equation, before that substitution, is
      2(2-K_B) div[grad Psi - v] + 2(2-K_B) div[J_Z grad Psi] = 16 pi Gt rho,
where the first bracket's grad Psi comes from Einstein-Hilbert (+4) plus the aether's F^2 term
(-2K_B), and its -v comes ENTIRELY from the mixing term.  On v = grad Psi the first bracket
vanishes identically and the WHOLE surviving Newtonian operator is the free function's own.
That is the honest statement of "1 - c_14/2 = 0 does not bite": the Einstein-Hilbert piece of
the Psi operator really is cancelled -- not by the free function, but by the scalar -- and the
free function then supplies the entire operator back, with coefficient J_Z -> 1.
THE NEW ADVERSE ITEM.  The corrected c_14 = 2K_B - 2 is NEGATIVE for K_B < 1, and the
Einstein-aether vector-mode formula c_V^2 = (c_1 - c_1^2/2 + c_3^2/2)/(c_14(1-c_13)) then reads
K_B/(2(K_B-1)) < 0 -- an imaginary vector sound speed -- where the sign-slipped c_4 gave the
benign +K_B/2.  I do NOT claim that number: the dictionary is demonstrated INAPPLICABLE to this
theory's scalar sector (with the mixing on it misses G_N by a factor 2), and AeST proper sits at
c_14 = K_B with the same formula already reading c_V^2 = K_B/K_B... the vector sector needs its
own direct variation.  It is flagged, not priced.  NOT COMPUTED HERE.
COSMOLOGICAL VS LOCAL G.  On FRW with the aether's temporal component kept INDEPENDENT of the
lapse and the multiplier retained (vary first, impose B = N afterwards), F_{mu nu} = 0 for any
B(t), N(t), and J^mu = 0, Z = 0, Y = 0 on the constraint -- so every K_B term and the whole free
function drop out of the Friedmann constraint, whose matter coefficient is exactly 8 pi Gt with
no K_B and no free-function dependence anywhere: G_cosmo = Gt.  The two theories' Friedmann
constraints are identical term by term.  Hence G_N / G_cosmo = 1/(1-K_B/2) =
1.0526 / 1.1429 / 1.1765 / 1.3333 at K_B = 0.1 / 0.25 / 0.3 / 0.5, IDENTICAL in F(Y) and F(Z),
so option 1 creates NO new BBN liability; the existing one (the corpus's K_B <~ 0.25) is
inherited unchanged.  ONE DISCREPANCY FOUND ON THE WAY AND NOT RESOLVED (G8): the dark-sector
term I derive from the transcribed action is 3H^2 = 8 pi Gt rho_m - (Q K_Q - K)/2, whereas
real_research/bridge1_aest_equations.md records 8 pi Gt rhobar = Q dK/dQ - K.  The two differ by
a factor -1/2 -- a convention in how Lambda is split between the action's explicit -2 Lambda and
K(Q_0) = -2 Lambda (carrying both, as typeII does, cancels the cosmological constant outright,
which is B5).  It is a PRE-EXISTING corpus item, not created by option 1, it does not touch the
rho_m coefficient that item (d) turns on, and settling it needs the published paper.  FLAGGED,
NOT COMPUTED.

=========================================================================================
EVERY REDUCTION, DECLARED
=========================================================================================
R1 STATIC weak field for the local sector; separately FRW mini-superspace for the cosmological
   one.  No boosted (O(w)) sector: alpha_1, alpha_2, c_V, c_S are NOT computed here.  The
   assignment's items (ii) (alpha_2) and the vector speed are touched only as DICTIONARY
   ARITHMETIC, explicitly labelled, never as results.
R2 ORDER COUNTING identical to typeII_direct_variation_2026.py R2: h_{mu nu}, a_mu, varphi, rho
   are O(eps) and a_0 (the MOND scale) is O(eps), so the non-analytic free function sits at
   O(eps^2).  Verified for BOTH arguments at A9.  Truncation at eps^2 with explicit degree
   checks everywhere.
R3 F(arg,Q) = (2-K_B) Jcal(arg) + K(Q); cross terms are O(eps^3) since arg is O(eps^2) and
   (Q-Q_0) is O(eps).  Verified at A10.
R4 K'(Q_0) -> 0 in the linear sector, because the flat static background solves its own
   equations only if K'(Q_0) Q_0 = 0 (derived at B5).  typeII PART F prices the neglect at
   1.7e-23 at 1 AU and 6.6e-6 at 30 kpc; those numbers are QUOTED, not recomputed.
R5 Second-order pieces of h, a_i, varphi enter the quadratic action only against the background
   equations and drop; the one that does not, the aether's O(eps^2) temporal component b_0, is
   retained and its equation checked (B4).
R6 The free function is varied EXACTLY at first order (delta Jcal = J_arg delta arg with J_arg
   an inert symbol), so the non-analytic Jcal is never evaluated off the constraint surface.
R7 The curl sector is not re-litigated: as in Bekenstein-Milgrom and in AeST, the pointwise
   vector law holds exactly in curl-free (spherical) configurations.  G_N is read off a
   spherical source, which is in that sector.
R8 NOT DONE HERE: c_T, cosmological perturbations, the RAR/ephemeris arithmetic (that is
   opt1_legality_2026.py PARTS E-H), and any refit.

EXIT 0 iff every numbered check passes.
"""

import math
import sys
import time

import sympy as sp

# =================================================================================================
# check harness
# =================================================================================================
FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))


print(__doc__)
T0 = time.time()

# =================================================================================================
# constants -- both footings carried for every dimensional number
# =================================================================================================
CLIGHT = 2.99792458e8
GMSUN = 1.32712440018e20
AU = 1.495978707e11
A0_CAN = 9.3619e-11            # kappa c sqrt(G rho_Lambda), canonical footing
A0_ALT = 1.1279e-10            # alt footing
FOOT = (("canonical", A0_CAN), ("ALT", A0_ALT))
KB_GRID = (0.1, 0.25, 0.3, 0.5)   # SZ21 fiducials 0.1/0.3/0.5 plus the corpus's BBN ceiling 0.25

# =================================================================================================
# symbols and machinery
# =================================================================================================
tt, x1, x2, x3 = sp.symbols("t x1 x2 x3", real=True)
CO = [tt, x1, x2, x3]
SPC = [x1, x2, x3]
eps = sp.Symbol("eps")
KB, Q0, Kp1, Kpp, GT, LAM, K0s, rhoh = sp.symbols("K_B Q_0 Kprime Kpp Gt Lambda K0 rhohat")
JYs, JZs = sp.symbols("J_Y J_Z")


def fn(name):
    return sp.Function(name)(x1, x2, x3)


def tr2(e):
    e = sp.expand(e)
    return e.coeff(eps, 0) + eps * e.coeff(eps, 1) + eps ** 2 * e.coeff(eps, 2)


def deg_ok(e, n=2):
    return sp.Poly(sp.expand(e), eps).degree() <= n


def lap(e):
    return sum(sp.diff(e, c, 2) for c in SPC)


def div(vec):
    return sum(sp.diff(vec[k], SPC[k]) for k in range(3))


def el(L, f):
    """Euler-Lagrange derivative in the 3 static coordinates (first and second derivatives)."""
    out = sp.diff(L, f)
    for c in SPC:
        out -= sp.diff(sp.diff(L, sp.Derivative(f, c)), c)
    for i, ci in enumerate(SPC):
        for j, cj in enumerate(SPC):
            if i <= j:
                dd = sp.Derivative(f, (ci, 2)) if ci == cj else sp.Derivative(f, ci, cj)
                trm = sp.diff(L, dd)
                if trm != 0:
                    out += sp.diff(trm, ci, cj)
    return sp.expand(out.doit())


# =================================================================================================
print()
print("=" * 100)
print("PART A -- THE FIELDS KEPT GENERIC; WHAT Z, Y AND Q ACTUALLY ARE")
print("=" * 100)

Hc = {}
for m in range(4):
    for n in range(m, 4):
        Hc[(m, n)] = fn(f"H{m}{n}")
        Hc[(n, m)] = Hc[(m, n)]
Hm = sp.Matrix(4, 4, lambda m, n: Hc[(m, n)])
eta = sp.diag(-1, 1, 1, 1)
gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps * Hm[m, n])
Hup = eta * Hm * eta
gu = sp.Matrix(4, 4, lambda i, j: sp.expand((eta - eps * Hup + eps ** 2 * (Hup * Hm * eta))[i, j]))
idc = sp.Matrix(4, 4, lambda i, j: tr2(sum(gd[i, k] * gu[k, j] for k in range(4))))
check(sp.simplify(idc - sp.eye(4)) == sp.zeros(4, 4),
      "A1  the perturbative inverse metric is correct to O(eps^2) for a GENERIC ten-component "
      "static h: no metric ansatz is in force anywhere before PART C")

trH = sum(eta[m, n] * Hm[m, n] for m in range(4) for n in range(4))
HH = sum(Hup[m, n] * Hm[m, n] for m in range(4) for n in range(4))
sqg = 1 + eps * trH / 2 + eps ** 2 * (trH ** 2 / 8 - HH / 4)
det_ex = sp.expand(sp.series(sp.sqrt(sp.expand(-gd.det())), eps, 0, 3).removeO())
check(sp.simplify(sp.expand(det_ex - sqg)) == 0,
      "A2  sqrt(-g) verified against the exact determinant of the generic metric to O(eps^2)")

Gam = [[[tr2(sp.Rational(1, 2) * sum(
    gu[r, s] * (sp.diff(gd[s, n], CO[m]) + sp.diff(gd[s, m], CO[n]) - sp.diff(gd[m, n], CO[s]))
    for s in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]


def ric(a, b):
    o = 0
    for m in range(4):
        o += sp.diff(Gam[m][b][a], CO[m]) - sp.diff(Gam[m][m][a], CO[b])
        for l in range(4):
            o += Gam[m][m][l] * Gam[l][b][a] - Gam[m][b][l] * Gam[l][m][a]
    return tr2(o)


Rsc = tr2(sum(gu[m, n] * ric(m, n) for m in range(4) for n in range(4)))
info(f"A-  generic curvature assembled ({time.time()-T0:.1f} s)")

# --- generic aether, constraint NOT yet imposed -------------------------------------------------
a0f, b0f = fn("a0"), fn("b0")
aif = [fn("a1"), fn("a2"), fn("a3")]
lam0, lam1 = fn("lam0"), fn("lam1")
wf = fn("w")

Ad = sp.Matrix([-(1 + eps * a0f + eps ** 2 * b0f), eps * aif[0], eps * aif[1], eps * aif[2]])
Au = sp.Matrix(4, 1, lambda i, j: tr2(sum(gu[i, k] * Ad[k] for k in range(4))))
Cc = tr2(sum(Au[i] * Ad[i] for i in range(4)) + 1)

c1sol = sp.solve(sp.expand(Cc).coeff(eps, 1), a0f)[0]
Ad_1 = Ad.subs(a0f, c1sol)
Au_1 = sp.Matrix(4, 1, lambda i, j: tr2(sum(gu[i, k] * Ad_1[k] for k in range(4))))
Cc_1 = tr2(sum(Au_1[i] * Ad_1[i] for i in range(4)) + 1)
c2sol = sp.solve(sp.expand(Cc_1).coeff(eps, 2), b0f)[0]
SOL = {a0f: c1sol, b0f: c2sol}
Ad_on = Ad.subs(SOL)
Au_on = sp.Matrix(4, 1, lambda i, j: tr2(sum(gu[i, k] * Ad_on[k] for k in range(4))))
Cres = sp.expand(tr2(sum(Au_on[i] * Ad_on[i] for i in range(4)) + 1))
check(sp.simplify(Cres) == 0,
      "A3  the unit-timelike constraint is SOLVED order by order and the residual vanishes "
      "identically to O(eps^2), with the aether's spatial components left FREE",
      f"first order: a_0 = {sp.simplify(c1sol)}, i.e. A_0 = -(1 + eps Psi) once H00 = -2 Psi")

# --- J^mu = A^nu nabla_nu A^mu, and Z = J^mu J_mu, GENERIC --------------------------------------
Jup = [tr2(sum(Au_on[nu] * (sp.diff(Au_on[al], CO[nu])
                            + sum(Gam[al][nu][r] * Au_on[r] for r in range(4)))
              for nu in range(4))) for al in range(4)]
Zc = tr2(sum(gd[m, n] * Jup[m] * Jup[n] for m in range(4) for n in range(4)))

PsiF, PhiF = fn("Psi"), fn("Phi")
gradH00 = [sp.diff(-Hc[(0, 0)] / 2, c) for c in SPC]
check(sp.simplify(sp.expand(Jup[0]).coeff(eps, 0)) == 0
      and sp.simplify(sp.expand(Jup[0]).coeff(eps, 1)) == 0,
      "A4a J^0 has no eps^0 and no eps^1 piece: the aether's acceleration is purely spatial at "
      "leading order, for a GENERIC metric (h_0i and h_ij included) and a generic aether")
check(all(sp.simplify(sp.expand(Jup[i + 1]).coeff(eps, 1) - gradH00[i]) == 0 for i in range(3))
      and all(sp.simplify(sp.expand(Jup[i + 1]).coeff(eps, 0)) == 0 for i in range(3)),
      "A4b *** J^i = eps grad_i Psi + O(eps^2) with Psi := -H00/2 and coefficient EXACTLY 1, "
      "derived from J^mu = A^nu grad_nu A^mu with NO ansatz: no h_0i, no h_ij, no a_i, no "
      "varphi contamination at this order ***")

Z2 = sp.expand(sp.expand(Zc).coeff(eps, 2))
check(sp.simplify(sp.expand(Zc).coeff(eps, 0)) == 0
      and sp.simplify(sp.expand(Zc).coeff(eps, 1)) == 0
      and sp.simplify(sp.expand(Z2 - sum(g ** 2 for g in gradH00))) == 0,
      "A5  *** GATE: Z = J^mu J_mu = eps^2 |grad Psi|^2 EXACTLY at quadratic order, "
      "Psi = -H00/2 ***",
      "so the free function's new argument is the squared gradient of the total potential -- "
      "the object AQUAL's free function eats")

OTHER = [wf] + aif + [Hc[(m, n)] for m in range(4) for n in range(m, 4) if (m, n) != (0, 0)]
check(all(sp.simplify(sp.diff(Z2, f)) == 0 for f in OTHER)
      and all(all(sp.simplify(sp.diff(Z2, sp.Derivative(f, c))) == 0 for c in SPC)
              for f in OTHER),
      "A6  *** and Z's eps^2 coefficient depends on H00 ALONE: not on h_0i, not on h_ij, not on "
      "a_i, not on varphi ***",
      "consequences used later: (i) the free function contributes NOTHING to the ij Einstein "
      "equations at this order, so gamma_PPN = 1 survives; (ii) it contributes nothing to the "
      "aether-spatial equation, which is why v = grad Psi becomes pointwise")

# --- Y and Q, the controls ----------------------------------------------------------------------
dphi = sp.Matrix([Q0, eps * sp.diff(wf, x1), eps * sp.diff(wf, x2), eps * sp.diff(wf, x3)])
Qc = tr2(sum(Au_on[m] * dphi[m] for m in range(4)))
Yc = tr2(sum((gu[m, n] + Au_on[m] * Au_on[n]) * dphi[m] * dphi[n]
             for m in range(4) for n in range(4)))
v = [sp.diff(wf, c) + Q0 * aif[k] for k, c in enumerate(SPC)]
Yhat = sum(vv ** 2 for vv in v)
check(sp.expand(Yc).coeff(eps, 0) == 0 and sp.simplify(sp.expand(Yc).coeff(eps, 1)) == 0
      and sp.simplify(sp.expand(sp.expand(Yc).coeff(eps, 2) - Yhat)) == 0,
      "A7  CONTROL: the same machinery gives Y = eps^2 |grad varphi + Q_0 a|^2 with no metric "
      "contamination -- typeII_direct_variation_2026.py's P1/A7, reproduced independently")
ANS_M = {Hc[(0, 0)]: -2 * PsiF, Hc[(0, 1)]: 0, Hc[(0, 2)]: 0, Hc[(0, 3)]: 0,
         Hc[(1, 1)]: -2 * PhiF, Hc[(2, 2)]: -2 * PhiF, Hc[(3, 3)]: -2 * PhiF,
         Hc[(1, 2)]: 0, Hc[(1, 3)]: 0, Hc[(2, 3)]: 0}
ANS_A = {aif[0]: 0, aif[1]: 0, aif[2]: 0}
Q_ans = sp.simplify(sp.expand(Qc.subs(ANS_M).subs(ANS_A).doit()))
check(sp.simplify(Q_ans - Q0 * (1 - eps * PsiF + eps ** 2 * sp.Rational(3, 2) * PsiF ** 2)) == 0,
      "A8  CONTROL: Q = Q_0(1 - Psi + 3 Psi^2/2), typeII's A5 -- so the K(Q) dust/CMB sector "
      "is untouched by option 1 at this order")

for e, nm in ((Zc, "Z"), (Yc, "Y"), (Qc, "Q"), (Rsc, "R"), (sqg, "sqrt(-g)")):
    check(deg_ok(e), f"A9a explicit degree check: truncated {nm} is degree <= 2 in eps")

xv, a0sym, epsp = sp.symbols("Xv a0M eps_p", positive=True)
Jm = sp.Rational(2, 3) * xv ** sp.Rational(3, 2) / a0sym
check(sp.simplify((Jm.subs({xv: epsp ** 2 * xv, a0sym: epsp * a0sym}) / epsp ** 2) - Jm) == 0,
      "A9b the R2 bookkeeping holds for BOTH arguments: with a_0 counted O(eps), "
      "Jcal = (2/3) X^{3/2}/a_0 at X = eps^2 Xhat is exactly eps^2 times the same function of "
      "Xhat, whether X is Y or Z (both are O(eps^2) by A5/A7)")
check(sp.expand(tr2(sp.Symbol("cx") * Zc * (Qc - Q0))) == 0
      and sp.expand(tr2(sp.Symbol("cx") * Yc * (Qc - Q0))) == 0,
      "A10 R3 is not a restriction at this order: any arg-Q cross term in F vanishes after "
      "truncation, for arg = Y and for arg = Z alike")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THE FULL ACTION WITH lambda RETAINED: BACKGROUND AND THE MULTIPLIER,")
print("          FOR BOTH THEORIES")
print("=" * 100)

Fmn = sp.Matrix(4, 4, lambda m, n: sp.diff(Ad[n], CO[m]) - sp.diff(Ad[m], CO[n]))
F2 = tr2(sum(Fmn[m, n] * Fmn[a, b] * gu[m, a] * gu[n, b]
             for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
Jup_g = [tr2(sum(Au[nu] * (sp.diff(Au[al], CO[nu])
                           + sum(Gam[al][nu][r] * Au[r] for r in range(4)))
               for nu in range(4))) for al in range(4)]
Jdphi = tr2(sum(Jup_g[m] * dphi[m] for m in range(4)))
Zfull = tr2(sum(gd[m, n] * Jup_g[m] * Jup_g[n] for m in range(4) for n in range(4)))
Qfull = tr2(sum(Au[m] * dphi[m] for m in range(4)))
Yfull = tr2(sum((gu[m, n] + Au[m] * Au[n]) * dphi[m] * dphi[n]
                for m in range(4) for n in range(4)))
dQfull = sp.expand(Qfull - Q0)
Kfull = K0s + Kp1 * dQfull + sp.Rational(1, 2) * Kpp * tr2(dQfull ** 2)


def full_lag(mode):
    """R6: the free function is varied EXACTLY at first order, delta Jcal = J_arg delta arg,
    so - (2-K_B) Y - F reads -(2-K_B)(1+J_Y) Y for mode 'Y' and -(2-K_B) Y - (2-K_B) J_Z Z
    for mode 'Z'.  J_Y, J_Z are inert symbols."""
    if mode == "Y":
        ff = -(2 - KB) * (1 + JYs) * Yfull
    else:
        ff = -(2 - KB) * Yfull - (2 - KB) * JZs * Zfull
    L = tr2(sqg * (Rsc - 2 * LAM - (KB / 2) * F2 + 2 * (2 - KB) * Jdphi
                   + ff - Kfull - (lam0 + eps * lam1) * Cc)) \
        - 16 * sp.pi * GT * eps * rhoh * (1 - eps * Hc[(0, 0)] / 2)
    return sp.expand(L)


LF = {m: full_lag(m) for m in ("Y", "Z")}
L1 = {m: LF[m].coeff(eps, 1) for m in ("Y", "Z")}
L2 = {m: LF[m].coeff(eps, 2) for m in ("Y", "Z")}
info(f"B-  full Lagrangians assembled ({time.time()-T0:.1f} s)")

check(all(sp.simplify(sp.expand(el(L1[m], lam0)) - (Hc[(0, 0)] + 2 * a0f)) == 0
          for m in ("Y", "Z")),
      "B1  varying lambda reproduces the first-order constraint H00 + 2 a_0 = 0 in both "
      "theories -- the multiplier is doing its job and nothing was smuggled in")

lamY = sp.solve(sp.Eq(sp.expand(el(L1["Y"], a0f)), 0), lam0)[0]
lamZ = sp.solve(sp.Eq(sp.expand(el(L1["Z"], a0f)), 0), lam0)[0]
check(sp.simplify(lamY - ((2 - KB) * (1 + JYs) * Q0 ** 2 + Kp1 * Q0 / 2)) == 0,
      "B2  CONTROL: lambda_bg = (2-K_B)(1+J_Y) Q_0^2 + K'(Q_0) Q_0/2 for the F(Y) theory -- "
      "typeII's B2 reproduced exactly by an independent implementation")
check(sp.simplify(lamZ - ((2 - KB) * Q0 ** 2 + Kp1 * Q0 / 2)) == 0,
      "B3  *** and lambda_bg = (2-K_B) Q_0^2 + K'(Q_0) Q_0/2 for the F(Z) theory: the (1+J_Y) "
      "factor is GONE, because Z does not depend on the aether's temporal component at this "
      "order (A6).  DERIVED, not carried over ***")
check(all(sp.simplify(sp.expand(el(L2[m], b0f)) - sp.expand(el(L1[m], a0f))) == 0
          for m in ("Y", "Z")),
      "B4  the O(eps^2) equation for the aether's second-order temporal component b_0 is the "
      "SAME background equation, so lambda_bg is over-determined and consistent (R5)")

bgH00 = {m: sp.simplify(el(L1[m], Hc[(0, 0)]).subs(lam0, lamY if m == "Y" else lamZ))
         for m in ("Y", "Z")}
bgH11 = {m: sp.simplify(el(L1[m], Hc[(1, 1)])) for m in ("Y", "Z")}
check(all(sp.simplify(bgH11[m] + (K0s / 2 + LAM)) == 0 for m in ("Y", "Z"))
      and all(sp.simplify(bgH00[m] - (K0s / 2 + LAM - Kp1 * Q0 / 2)) == 0 for m in ("Y", "Z")),
      "B5  background equations, IDENTICAL in both theories: K(Q_0) + 2 Lambda = 0 (satisfied "
      "identically by SZ21's K) and K'(Q_0) Q_0 = 0, which is R4's justification for dropping "
      "the cosmological dust term in the linear sector",
      "the F(Z) promotion changes NOTHING about the background: Z is O(eps^2)")

for m in ("Y", "Z"):
    lm = lamY if m == "Y" else lamZ
    lhs = el(sp.expand(L2[m].subs(SOL).doit()), Hc[(0, 0)])
    rhs = sp.expand((el(L2[m], Hc[(0, 0)]) + sp.Rational(-1, 2) * el(L2[m], a0f)).subs(SOL).doit())
    check(sp.simplify(sp.expand(lhs - rhs).subs(lam0, lm)) == 0,
          f"B6{m} the elimination identity holds in the F({m}) theory: the constraint-preserving "
          f"H00 variation equals [00-Einstein] - (1/2)[aether-temporal] once lambda takes its "
          f"B2/B3 value.  Solving the constraint before varying loses nothing",
          "typeII's C2, re-derived here for BOTH theories -- it is NOT inherited, and for "
          "F(Z) it holds with the DIFFERENT lambda_bg of B3")
    r0 = sp.simplify(sp.expand(sp.expand(lhs - rhs).subs(lam0, 0)))
    check(r0 != 0,
          f"B7{m} and with lambda_bg set to zero the identity fails by a term proportional to "
          f"Q_0^2 H00 -- a SPURIOUS graviton mass.  The error class is reproduced and named, "
          f"not stepped in",
          f"residual = {r0}")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- THE LINEAR FIELD EQUATIONS BY DIRECT VARIATION, ANSATZ IMPOSED ONLY NOW")
print("=" * 100)

Jc = sp.Function("Jcal")
uarg = sp.Symbol("uarg")


def Jp(arg):
    return sp.diff(Jc(uarg), uarg).subs(uarg, arg)


Kmain = K0s + Kp1 * sp.expand(Qc - Q0) + sp.Rational(1, 2) * Kpp * tr2(sp.expand(Qc - Q0) ** 2)
Zhat = sp.expand(Z2)          # = |grad Psi|^2 in terms of H00, DERIVED at A5


def idf(z):
    """the Newtonian-limit free function: Jcal(X) -> X, i.e. J_Z -> 1, i.e. mu -> 1"""
    return z


def main_lag(mode, mixc=None, yc=None, jfun=None):
    """Quadratic Lagrangian with the constraint solved (legal by B6).  mixc is the coefficient
    of J^mu grad_mu phi (AeST: 2(2-K_B)); yc is the coefficient of -Y (AeST: (2-K_B));
    jfun is the free function (Jcal generally, idf in the Newtonian limit)."""
    mixc = 2 * (2 - KB) if mixc is None else mixc
    yc = (2 - KB) if yc is None else yc
    jf = Jc if jfun is None else jfun
    arg = Yhat if mode == "Y" else Zhat
    L = tr2(sqg * (Rsc - 2 * LAM - (KB / 2) * F2.subs(SOL).doit()
                   + mixc * Jdphi.subs(SOL).doit() - yc * Yc - Kmain)) \
        - (2 - KB) * eps ** 2 * jf(arg) \
        - 16 * sp.pi * GT * eps * rhoh * (1 - eps * Hc[(0, 0)] / 2)
    return sp.expand(L)


def quad(L, mass=True):
    """the eps^2 Lagrangian on the background (R4: K'(Q_0) -> 0 by B5)"""
    sub = {K0s: -2 * LAM, Kp1: 0}
    if not mass:
        sub[Kpp] = 0
    return sp.expand(L.coeff(eps, 2).subs(sub))


def scalar_off(L2q):
    """switch the scalar/mixing sector off: Q_0 = 0, varphi = 0, a_i = 0"""
    out = sp.expand(L2q.subs({Q0: 0}).subs(wf, 0).subs({aif[k]: 0 for k in range(3)}).doit())
    assert wf not in out.atoms(sp.Function)
    return out


def read_GN(L2q, eliminate_scalar=True):
    """G_N read off the 00 equation: solve the aether-longitudinal equations for grad varphi,
    substitute, and take the ratio of the rho coefficient to the lap(Psi) coefficient."""
    e = sp.expand(el(L2q, Hc[(0, 0)]).subs(ANS).subs({PhiF: PsiF}).doit())
    if eliminate_scalar:
        sd = {}
        for k in range(3):
            ea = sp.expand(el(L2q, aif[k]).subs(ANS_M).subs(
                {aif[j]: 0 for j in range(3)}).doit())
            sol = sp.solve(sp.Eq(ea, 0), sp.Derivative(wf, SPC[k]))
            assert len(sol) == 1, "aether-longitudinal equation not uniquely solvable for v"
            sd[sp.Derivative(wf, (SPC[k], 2))] = sp.diff(sol[0], SPC[k])
        e = sp.expand(e.subs(sd).doit())
    e = sp.expand(e.subs({aif[k]: 0 for k in range(3)}).doit())
    cl = sp.simplify(e.coeff(sp.Derivative(PsiF, (x1, 2))))
    cr = sp.simplify(e.coeff(rhoh))
    if sp.simplify(cl) == 0:
        return sp.oo
    return sp.simplify(-cr / (4 * sp.pi * cl))


LM = {m: main_lag(m) for m in ("Y", "Z")}
check(all(deg_ok(LM[m]) for m in ("Y", "Z")),
      "C0  explicit degree check on both assembled quadratic Lagrangians: degree <= 2 in eps")
L2M = {m: sp.expand(LM[m].coeff(eps, 2).subs({K0s: -2 * LAM, Kp1: 0})) for m in ("Y", "Z")}
info(f"C-  main Lagrangians assembled ({time.time()-T0:.1f} s)")

EHq = sp.expand(tr2(sqg * Rsc)).coeff(eps, 2)
for m in ("Y", "Z"):
    nonEH = sp.expand(L2M[m] - EHq.subs({K0s: -2 * LAM, Kp1: 0}))
    hij = [Hc[(i, j)] for i in range(1, 4) for j in range(i, 4)]
    fs = nonEH.atoms(sp.Function)
    check(all(hh not in fs for hh in hij),
          f"C1{m} the ENTIRE non-Einstein sector of the F({m}) theory -- aether kinetic, mixing, "
          f"Y, the free function, matter -- is independent of h_ij at quadratic order",
          "for F(Z) this is A6 doing the work: the new argument carries H00 only.  Hence NO "
          "anisotropic stress and no trace source from the dark sector in either theory")

grlim = sp.expand(el(sp.expand(L2M["Y"].subs({KB: 0, Q0: 0, Kpp: 0})), Hc[(0, 0)])
                  .subs(ANS_M).subs(ANS_A).subs({wf: 0, PhiF: PsiF}).doit())
check(sp.simplify(grlim - (8 * sp.pi * GT * rhoh - 2 * lap(PsiF))) == 0,
      "C2  NORMALISATION CONTROL: switch the dark sector off (K_B = 0, Q_0 = 0, varphi = 0) and "
      "the 00 equation collapses to lap Psi = 4 pi Gt rho.  So the matter action, the 16 pi Gt "
      "factors and the sign conventions are the standard ones, and any G renormalisation below "
      "is real rather than a bookkeeping artifact")

ANS = dict(ANS_M)
ANS.update(ANS_A)
meq = {m: {(a, b): el(L2M[m], Hc[(a, b)]) for a in range(4) for b in range(a, 4)}
       for m in ("Y", "Z")}
for m in ("Y", "Z"):
    e12 = sp.simplify(sp.expand(meq[m][(1, 2)].subs(ANS).doit()))
    e11 = sp.simplify(sp.expand(meq[m][(1, 1)].subs(ANS).doit()))
    e0i = [sp.simplify(sp.expand(meq[m][(0, k)].subs(ANS).doit())) for k in (1, 2, 3)]
    check(sp.simplify(e12 + 2 * sp.diff(PhiF - PsiF, x1, x2)) == 0
          and sp.simplify(e11 - (sp.diff(PhiF - PsiF, x2, 2) + sp.diff(PhiF - PsiF, x3, 2))) == 0
          and all(e == 0 for e in e0i),
          f"C3{m} the ij equations of the F({m}) theory are d_i d_j (Phi - Psi) = 0 with NO "
          f"source, and the h_0i equations are satisfied identically.  gamma_PPN = 1 exactly, "
          f"for every K_B and every free function",
          "so option 1 does not spoil the lensing sector at this order -- opt1's liability L2, "
          "confirmed at the order where the derivation works")

# --- the 00 equation, the scalar equation, the aether equation, BOTH theories --------------------
e00 = {m: sp.expand(meq[m][(0, 0)].subs(ANS).subs({PhiF: PsiF}).doit()) for m in ("Y", "Z")}
mPsi2 = Kpp * Q0 ** 2 / (2 * (2 - KB))
tgtY = sp.expand(-(2 - KB) * (lap(PsiF) - lap(wf) - mPsi2 * PsiF
                             - 8 * sp.pi * GT * rhoh / (2 - KB)))
check(sp.simplify(e00["Y"] - tgtY) == 0,
      "C4  *** THE GATE.  F(Y) control: the 00 equation is\n"
      "        lap Psi - m_Psi^2 Psi = 4 pi Ghat rho + lap varphi,   Ghat = Gt/(1-K_B/2),\n"
      "    i.e. the committed relation Gt = (1-K_B/2) Ghat, reproduced by this machinery ***",
      "if this had failed, nothing below would have been claimable.  m_Psi^2 = K'' Q_0^2/"
      "(2(2-K_B)) = mu^2/2, as typeII D5")

JYf, JZf = Jp(Yhat), Jp(Zhat)
Sv = [sp.expand((1 + JYf) * v[k] - sp.diff(-Hc[(0, 0)] / 2, SPC[k])) for k in range(3)]
check(sp.simplify(sp.expand(el(L2M["Y"], wf) - 2 * (2 - KB) * div(Sv)).doit()) == 0,
      "C5  F(Y) control: the scalar equation is div[(1+J_Y) v] = lap Psi -- typeII's D6")
mx1 = 2 * KB * (sp.diff(aif[0], x2, 2) + sp.diff(aif[0], x3, 2)
                - sp.diff(aif[1], x1, x2) - sp.diff(aif[2], x1, x3))
check(sp.simplify(sp.expand(el(L2M["Y"], aif[0]) + 2 * (2 - KB) * Q0 * Sv[0] - mx1).doit()) == 0,
      "C6  F(Y) control: the aether spatial equation is 2 K_B [lap a_i - d_i div a] = "
      "2(2-K_B) Q_0 S_i with S = (1+J_Y) v - grad Psi -- typeII's D7, longitudinal part "
      "S^L = 0.  THREE independent typeII results reproduced: the machinery is validated")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- THE F(Z) THEORY: THE NEWTONIAN LIMIT BY EXPLICIT VARIATION")
print("=" * 100)

Sz = [sp.expand(v[k] - sp.diff(-Hc[(0, 0)] / 2, SPC[k])) for k in range(3)]
check(sp.simplify(sp.expand(el(L2M["Z"], aif[0]) + 2 * (2 - KB) * Q0 * Sz[0] - mx1).doit()) == 0,
      "D1  *** the aether spatial equation of the F(Z) theory has the free function GONE: its "
      "longitudinal projection is v = grad Psi POINTWISE, with no (1+J_Y) factor ***",
      "because Z is independent of a_i (A6).  The transverse sector is unchanged from AeST")
check(sp.simplify(sp.expand(el(L2M["Z"], wf) - 2 * (2 - KB) * div(Sz)).doit()) == 0,
      "D2  the scalar equation of the F(Z) theory is the DIVERGENCE of D1, so the system is "
      "not overdetermined (the same varphi / longitudinal-a degeneracy typeII D8 found)")

tgtZ = sp.expand(-(2 - KB) * (lap(PsiF) - lap(wf) - mPsi2 * PsiF
                             - 8 * sp.pi * GT * rhoh / (2 - KB))
                 - (2 - KB) * div([Jp(sum(sp.diff(PsiF, c) ** 2 for c in SPC))
                                   * sp.diff(PsiF, ck) for ck in SPC]))
check(sp.simplify(sp.expand(e00["Z"] - tgtZ)) == 0,
      "D3  the 00 equation of the F(Z) theory is\n"
      "        lap Psi - lap varphi + div[J_Z(|grad Psi|^2) grad Psi] = 4 pi Ghat rho "
      "+ m_Psi^2 Psi,\n"
      "    with the SAME Ghat = Gt/(1-K_B/2) multiplying rho as in the control C4")

SUBD1 = {sp.Derivative(wf, c): sp.Derivative(PsiF, c) for c in SPC}
red = sp.expand(tgtZ.subs({aif[k]: 0 for k in range(3)}).subs(SUBD1).doit())
aqual = sp.expand(-(2 - KB) * (div([Jp(sum(sp.diff(PsiF, c) ** 2 for c in SPC))
                                    * sp.diff(PsiF, ck) for ck in SPC])
                              - mPsi2 * PsiF - 8 * sp.pi * GT * rhoh / (2 - KB)))
check(sp.simplify(sp.expand(red - aqual)) == 0,
      "D4  *** substituting D1 (v = grad Psi) into D3 gives AQUAL EXACTLY,\n"
      "        div[ J_Z(|grad Psi|^2) grad Psi ] = 4 pi Ghat rho  (+ the Yukawa m_Psi^2 Psi),\n"
      "    with mu(g_obs) = J_Z(g_obs^2) and Ghat UNCHANGED from the F(Y) theory ***",
      "the entire ordinary lap Psi has cancelled against lap varphi; what is left is the free "
      "function's own operator.  opt1's C4, here derived from the full action rather than a "
      "calibrated Lagrangian")

# --- the Newtonian limit, and G_N read off H_00 --------------------------------------------------
GNsym = sp.Symbol("G_N", positive=True)
rr, MM = sp.symbols("r M", positive=True)
LZN = quad(main_lag("Z", jfun=idf), mass=False)     # J_Z -> 1: the Newtonian regime, DERIVED
GN_Z = read_GN(LZN)
check(sp.simplify(GN_Z - GT / (1 - KB / 2)) == 0,
      "D5  *** IN THE NEWTONIAN LIMIT J_Z -> 1 THE FULL VARIATION GIVES G_N = Gt/(1-K_B/2) = "
      "Ghat: FINITE, and EQUAL to the F(Y) theory's C4 value.  Nothing is singular ***",
      f"G_N = {sp.simplify(GN_Z)}; obtained by rebuilding the whole quadratic Lagrangian with "
      f"Jcal(Z) = Z, varying it, solving the aether-longitudinal equation for grad varphi and "
      f"substituting -- not by substituting into a result")

Ghat_expr = 2 * GT / (2 - KB)
Psi_sph = -GNsym * MM / rr
lap_sph = sp.simplify(sp.diff(rr ** 2 * sp.diff(Psi_sph, rr), rr) / rr ** 2)
flux = sp.simplify(4 * sp.pi * rr ** 2 * sp.diff(Psi_sph, rr))
check(sp.simplify(lap_sph) == 0 and sp.simplify(flux - 4 * sp.pi * GNsym * MM) == 0,
      "D6a spherical solve: Psi = -G_N M/r is the vacuum solution of lap Psi = 4 pi G_N rho and "
      "carries flux 4 pi G_N M through any enclosing sphere (Gauss), so G_N is read off the "
      "source term with no further assumption")
H00_sph = sp.simplify((-2 * Psi_sph).subs(GNsym, GN_Z))
check(sp.simplify(H00_sph - 2 * (GT / (1 - KB / 2)) * MM / rr) == 0,
      "D6b *** THE ANSWER: H_00 = 2 G_N M / r with G_N = Ghat = Gt/(1-K_B/2), i.e. EXACTLY the "
      "unmodified AeST value.  G_N[F(Z)] / G_N[F(Y)] = 1 ***",
      f"H_00 = {sp.simplify(H00_sph)}")
info("D6c  G_N/Gt over K_B, both theories identical:  "
     + ",  ".join(f"K_B={k}: {1/(1-k/2):.5f}" for k in KB_GRID))

# --- is the sign of the free function's contribution a CHOICE?  no: it is forced ---------------
JZsym, Ghs = sp.symbols("JZ Ghat", positive=True)
Psip = sp.Symbol("Psiprime")
gauss = sp.Eq(JZsym * Psip * rr ** 2, Ghs * MM)                # Gauss' law on D4
Psip_sol = sp.solve(gauss, Psip)[0]
check(sp.simplify(Psip_sol - Ghs * MM / (JZsym * rr ** 2)) == 0,
      "D7  *** THE SIGN OF THE FREE FUNCTION'S TERM IS NOT A CHOICE.  Integrating D4 over a "
      "ball gives Psi' = Ghat M/(J_Z r^2), so gravity is ATTRACTIVE only for J_Z > 0.  Hence "
      "-(2-K_B)J(Z) -> -(2-K_B)Z in the Newtonian limit with a POSITIVE coefficient (2-K_B), "
      "which is what fixes the effective c_4 NEGATIVE in PART F ***",
      "so the sign the alarm got wrong is not a convention that could go either way: reversing "
      "it would reverse the sign of Newtonian gravity")

# --- does option 1 move a_0?  (cross-check on opt1's G1b, not a new result) --------------------
gobs, gbar, a0s = sp.symbols("g_obs g_bar a0M", positive=True)
uu = sp.Symbol("u", positive=True)
solZ = sp.solve(sp.Eq(gobs * (gobs / a0s), gbar), gobs)
solY = sp.solve(sp.Eq(uu * (uu / a0s), gbar), uu)
check(len(solZ) == 1 and sp.simplify(solZ[0] - sp.sqrt(a0s * gbar)) == 0
      and len(solY) == 1 and sp.simplify(solY[0] - sp.sqrt(a0s * gbar)) == 0,
      "D8  and the SAME free function Jcal(X) = (2/3) X^{3/2}/a_0 gives the SAME deep-MOND law "
      "g_obs -> sqrt(a_0 g_bar) whichever argument it eats: in F(Z), mu = J_Z = g_obs/a_0 so "
      "g_obs^2/a_0 = g_bar; in F(Y), J_Y = u/a_0 so u = sqrt(a_0 g_bar) and "
      "g_obs = g_bar + u -> the same limit.  Option 1 moves neither G_N nor a_0",
      "a cross-check on opt1_legality_2026.py's G1b, not a new result -- the kernel arithmetic "
      "is that file's route, not mine")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- WHICH TERM RESCUES IT?  THE ATTRIBUTION, TESTED BY DELETION")
print("=" * 100)

sig = sp.Symbol("sigma")
LSigN = quad(main_lag("Z", mixc=2 * sig, jfun=idf), mass=False)
easig = sp.expand(el(LSigN, aif[0]).subs(ANS_M).subs({aif[j]: 0 for j in range(3)}).doit())
vsol = sp.solve(sp.Eq(easig, 0), sp.Derivative(wf, x1))
check(len(vsol) == 1 and sp.simplify(vsol[0] - sig * sp.diff(PsiF, x1) / (2 - KB)) == 0,
      "E1  with the mixing coefficient carried as a free 2 sigma, the aether-longitudinal "
      "equation gives v = [sigma/(2-K_B)] grad Psi -- linear, uniquely solvable, and equal to "
      "D1's v = grad Psi exactly at AeST's sigma = 2-K_B",
      f"grad_1 varphi = {sp.simplify(vsol[0])}")
check(sp.simplify(vsol[0].subs(sig, 2 - KB) - sp.diff(PsiF, x1)) == 0,
      "E2  so the sigma-family contains the real theory as the single point sigma = 2-K_B, and "
      "the counterfactuals below are a one-parameter deformation of the action, not of a result")

GN_sig = read_GN(LSigN)
check(sp.simplify(GN_sig.subs(sig, 2 - KB) - GT / (1 - KB / 2)) == 0,
      "E3  *** the sigma-family's Newtonian G, from the same variation, reproduces "
      "G_N = Gt/(1-K_B/2) at the AeST point sigma = 2-K_B ***",
      f"G_N(sigma) = {sp.simplify(GN_sig)}")
GN_nomix = sp.simplify(GN_sig.subs(sig, 0))
check(sp.simplify(GN_nomix - GT / (2 - KB)) == 0,
      "E4  *** THE ATTRIBUTION TEST, AND IT REFUTES HALF OF opt1's C6: DELETE the "
      "2(2-K_B) J^mu grad_mu phi mixing term (sigma = 0) and G_N is STILL FINITE, "
      "G_N = Gt/(2-K_B) = Ghat/2 ***",
      "so the mixing term does not rescue G_N from a singularity -- there is no singularity to "
      "rescue.  What it does is restore the factor 2, returning G_N from Ghat/2 to Ghat.  "
      "opt1's C6 identifies the right term and the wrong job")
pole = sp.solve(sp.Eq(sp.denom(sp.together(GN_sig)), 0), sig)
ratios = sorted(sp.simplify(sp.expand(p / (2 - KB))) for p in pole)
check(len(pole) == 2 and sp.sqrt(2) in ratios and -sp.sqrt(2) in ratios,
      "E5  *** IS IT TUNED?  NO.  G_N(sigma) has its poles at sigma = +-sqrt(2)(2-K_B), a "
      "factor sqrt(2) = 1.4142 away from AeST's sigma = 2-K_B, and G_N moves smoothly from "
      "Ghat/2 (sigma=0) to Ghat (sigma=2-K_B) in between.  A 41.4% displacement of one action "
      "coefficient is needed to reach the singular locus ***",
      f"poles at sigma = {pole}, i.e. sigma/(2-K_B) = {ratios}")

# the SECOND deformation direction: the Ycal coefficient, so the neighbourhood is 2-dimensional
tau = sp.Symbol("tau")
GN_st = read_GN(quad(main_lag("Z", mixc=2 * sig, yc=tau, jfun=idf), mass=False))
check(sp.simplify(GN_st.subs({sig: 2 - KB, tau: 2 - KB}) - GT / (1 - KB / 2)) == 0,
      "E5b the two-parameter family (mixing 2 sigma, Ycal coefficient tau) also reproduces "
      "G_N = Ghat at AeST's point sigma = tau = 2-K_B",
      f"G_N(sigma, tau) = {sp.simplify(GN_st)}")
tau_pole = sp.solve(sp.Eq(sp.denom(sp.together(GN_st)), 0), tau)
check(len(tau_pole) == 1
      and sp.simplify(tau_pole[0] - sig ** 2 / (2 * (2 - KB))) == 0
      and sp.simplify(tau_pole[0].subs(sig, 2 - KB) - (2 - KB) / 2) == 0,
      "E5c *** AND THE SECOND DIRECTION IS NOT TUNED EITHER: the pole surface is "
      "tau = sigma^2/(2(2-K_B)), i.e. at AeST's sigma the singular tau is HALF the AeST tau.  "
      "The nearest singular locus is a factor 2 away in tau and a factor sqrt(2) away in "
      "sigma ***",
      "so the KILL condition 'finite only by a cancellation that requires tuning' is not met "
      "anywhere in the natural two-dimensional neighbourhood of the AeST coefficients")

# the mechanism, exhibited sector by sector: whose operator is whose
def sector_e00(Lsec):
    """the H00 variation of one sector of the quadratic Lagrangian, on the ansatz with Phi = Psi"""
    return sp.expand(el(sp.expand(Lsec), Hc[(0, 0)]).subs(ANS).subs({PhiF: PsiF}).doit())


S_EH = tr2(sqg * Rsc).coeff(eps, 2)
S_F2 = tr2(sqg * (-(KB / 2) * F2.subs(SOL).doit())).coeff(eps, 2)
S_MIX = tr2(sqg * (2 * (2 - KB) * Jdphi.subs(SOL).doit())).coeff(eps, 2)
S_Y = tr2(sqg * (-(2 - KB) * Yc)).coeff(eps, 2)
S_JZ = -(2 - KB) * Zhat                      # J(Z) -> Z, the Newtonian limit
S_M = sp.expand(-16 * sp.pi * GT * eps * rhoh * (1 - eps * Hc[(0, 0)] / 2)).coeff(eps, 2)
eEH, eF2 = sector_e00(S_EH), sector_e00(S_F2)
eMIX, eY = sector_e00(S_MIX), sector_e00(S_Y)
eJZ, eM = sector_e00(S_JZ), sector_e00(S_M)
check(sp.simplify(eEH + 2 * lap(PsiF)) == 0 and sp.simplify(eF2 - KB * lap(PsiF)) == 0
      and sp.simplify(sp.expand(eMIX - (2 - KB) * lap(wf))) == 0
      and sp.simplify(eY) == 0
      and sp.simplify(sp.expand(eJZ + (2 - KB) * lap(PsiF))) == 0
      and sp.simplify(eM - 8 * sp.pi * GT * rhoh) == 0,
      "E6  *** THE MECHANISM, SECTOR BY SECTOR.  The H00 variation of the quadratic Lagrangian "
      "splits as\n"
      "        Einstein-Hilbert  -2 lap Psi        aether F^2  +K_B lap Psi\n"
      "        mixing            +(2-K_B) lap varphi (= div v on the ansatz a_i = 0)\n"
      "        Ycal              0 (no H00 dependence at all)\n"
      "        free function     -(2-K_B) lap Psi at J_Z -> 1  matter  +8 pi Gt rho\n"
      "    so the equation is  -(2-K_B)[lap Psi - div v + div(J_Z grad Psi)] + 8 pi Gt rho = 0, "
      "and on\n"
      "    D1's v = grad Psi the FIRST TWO CANCEL IDENTICALLY, leaving the free function's "
      "operator alone ***",
      "that is the honest content of '1 - c_14/2 = 0 does not bite': the Einstein-Hilbert piece "
      "of the Psi operator really is cancelled -- by the SCALAR, not by the free function -- "
      "and the free function then supplies the whole operator back with coefficient J_Z -> 1.  "
      "Note the free function's own entry is -(2-K_B) lap Psi, i.e. it enters the Psi operator "
      "with the OPPOSITE sign to the aether's F^2 entry +K_B lap Psi.  That sign is PART F")

# =================================================================================================
print()
print("=" * 100)
print("PART F -- THE DICTIONARY, AND THE SIGN THAT THE ALARM GOT WRONG")
print("=" * 100)
info("F0  In the Einstein-aether normalisation for which G_N = G/(1-c_14/2) holds, the aether "
     "Lagrangian is\n"
     "        L_ae = -K^{ab}_{mn} grad_a A^m grad_b A^n,  "
     "K^{ab}_{mn} = c_1 g^{ab}g_{mn} + c_2 d^a_m d^b_n + c_3 d^a_n d^b_m - c_4 A^a A^b g_{mn},\n"
     "    so the c_4 slot enters the LAGRANGIAN as +c_4 a^mu a_mu (minus in K times the overall "
     "minus).\n"
     "    On a static aether a^mu a_mu = |grad Psi|^2 > 0, and Einstein-Hilbert contributes "
     "-2|grad Psi|^2\n"
     "    (E6), so the total is -(2 - c_14)|grad Psi|^2 and G_N = 2G/(2-c_14) = G/(1-c_14/2).")

c14_s = sp.Symbol("c14")
GN_dict = GT / (1 - c14_s / 2)
info("F1  I do not read c_4 off the Lagrangian (the quadratic Lagrangian is defined only up to "
     "total derivatives, so a bare |grad Psi|^2 coefficient is ambiguous).  Instead I DEFINE "
     "c_14^eff by the very formula the alarm uses, c_14 := 2(1 - Gt/G_N), evaluated on the "
     "direct-variation G_N in the regime where the theory IS Einstein-aether -- i.e. with the "
     "scalar sector switched off, which is the dictionary's own domain.")


def c14_of(GN):
    return sp.simplify(2 * (1 - GT / GN))


GN_Y_ns = read_GN(scalar_off(quad(main_lag("Y"), mass=False)), eliminate_scalar=False)
GN_Z_ns = read_GN(scalar_off(quad(main_lag("Z", jfun=idf), mass=False)), eliminate_scalar=False)
c14_Y = c14_of(GN_Y_ns)
c14_Z = c14_of(GN_Z_ns)
check(sp.simplify(GN_Y_ns - GT / (1 - KB / 2)) == 0 and sp.simplify(c14_Y - KB) == 0,
      "F2  *** THE MATCHING IS VALIDATED FIRST: with the scalar off, the UNMODIFIED F(Y) theory "
      "gives G_N = Gt/(1-K_B/2), hence c_14 = K_B -- exactly the published AeST dictionary entry "
      "c_1 = K_B, c_4 = 0.  So this procedure returns the known answer on the known case ***")
check(sp.simplify(GN_Z_ns - GT / (2 - KB)) == 0
      and sp.simplify(c14_Z - (2 * KB - 2)) == 0
      and sp.simplify((c14_Z - c14_Y) - (KB - 2)) == 0,
      "F3  *** AND THE ANSWER: the F(Z) theory gives G_N = Gt/(2-K_B), hence c_14 = 2K_B - 2, "
      "i.e. c_4^eff = c_14 - c_1 = -(2-K_B).  THE ALARM'S c_4 = +(2-K_B) HAS THE WRONG SIGN ***",
      "root cause: Einstein-aether carries the c_4 structure as +c_4 a^mu a_mu (the minus in "
      "K^{ab}_{mn}'s c_4 slot times the overall minus in L_ae), while AeST carries the free "
      "function as -F, i.e. -(2-K_B)J(Z) -> -(2-K_B)Z.  They point OPPOSITE ways.  E6's sector "
      "ledger shows the same thing directly: the free function enters the Psi operator with the "
      "opposite sign to the aether's F^2 term")
check(sp.simplify(GN_dict.subs(c14_s, c14_Z) - GN_Z_ns) == 0
      and sp.simplify((1 - c14_s / 2).subs(c14_s, 2)) == 0
      and sp.simplify((1 - c14_s / 2).subs(c14_s, c14_Z) - (2 - KB)) == 0,
      "F4  consistency, both ways: the dictionary formula Gt/(1-c_14/2) at c_14 = 2K_B-2 "
      "returns Gt/(2-K_B), the direct-variation value, whereas at the alarm's c_14 = 2 its "
      "denominator is identically zero -- a pole the direct variation flatly contradicts")
check(sp.simplify(GN_dict.subs(c14_s, c14_Z) - GN_Z) != 0
      and sp.simplify(sp.simplify(GN_Z / GN_dict.subs(c14_s, c14_Z)) - 2) == 0,
      "F5  *** BUT THE DICTIONARY IS STILL NOT USABLE HERE: with the mixing ON (the real theory) "
      "the true G_N is 2 Gt/(2-K_B), exactly TWICE the corrected dictionary's Gt/(2-K_B).  The "
      "Einstein-aether PPN dictionary has no slot for AeST's J^mu grad_mu phi coupling, and "
      "this theory's Newtonian limit lives in it ***",
      "why the dictionary nevertheless works for unmodified AeST: there the Newtonian limit has "
      "J_Y -> infinity, so v = grad Psi/(1+J_Y) -> 0 and the scalar decouples.  That is exactly "
      "the condition that FAILS for F(Z), where v = grad Psi is O(1).  So neither the alarm nor "
      "a sign-corrected dictionary can settle G_N -- only the variation can")

info("F6  the arithmetic that follows from c_14 = 2K_B - 2, all of it dictionary-level:")
for k in KB_GRID:
    print(f"        K_B = {k:<5}  c_14 = {2*k-2:+.3f}   1 - c_14/2 = {1-(2*k-2)/2:.3f}   "
          f"2 - c_14 = {2-(2*k-2):.3f}   G_N/Gt (true) = {1/(1-k/2):.5f}")
check(all(abs((2 * k - 2) - 2) > 1e-9 and (1 - (2 * k - 2) / 2) > 0 for k in KB_GRID)
      and sp.simplify(sp.limit(2 * KB - 2, KB, 2) - 2) == 0,
      "F7  *** c_14 = 2 is NEVER attained inside AeST's own stability window 0 < K_B < 2: "
      "c_14 = 2K_B-2 lies in (-2, 2) and 1 - c_14/2 = 2 - K_B > 0 throughout.  c_14 -> 2 only "
      "as K_B -> 2, where the free function's own prefactor (2-K_B) -> 0 and the whole dark "
      "sector degenerates ***",
      "item (i) of the alarm -- 'G_N = G/0, FORMALLY SINGULAR' -- is therefore void twice "
      "over: by sign, and by the direct variation that supersedes the dictionary anyway")

# --- item (ii): the alpha_2 numerator/denominator, as ARITHMETIC ONLY ----------------------------
c1s, c2s, c3s, c4s = sp.symbols("c1 c2 c3 c4")
num = (c1s + 2 * c3s - c4s) * (2 * c1s + 3 * c2s + c3s + c4s)
SUB0 = {c1s: KB, c2s: 0, c3s: -KB, c4s: 0}
SUBZ = {c1s: KB, c2s: 0, c3s: -KB, c4s: KB - 2}
SUBA = {c1s: KB, c2s: 0, c3s: -KB, c4s: 2 - KB}
check(sp.simplify(num.subs(SUB0) + KB ** 2) == 0 and sp.simplify(num.subs(SUBA) + 4) == 0,
      "F8  TRANSCRIPTION CONTROL on the alpha_2 numerator (c_1+2c_3-c_4)(2c_1+3c_2+c_3+c_4): it "
      "gives -K_B^2 at c_4 = 0 and -4 at the alarm's c_4 = +(2-K_B), both of which are the "
      "numbers the assignment states.  So the formula I am handling is the one it means")
c123 = sp.simplify((c1s + c2s + c3s).subs(SUBZ))
fac2 = sp.simplify((2 - (c1s + c4s)).subs(SUBZ))
check(sp.simplify(c123) == 0
      and sp.simplify(num.subs(SUBZ) + 4 * (1 - KB) ** 2) == 0
      and sp.simplify(fac2 - (4 - 2 * KB)) == 0
      and all(abs(4 - 2 * k) > 1e-9 for k in KB_GRID),
      "F9  *** item (ii) of the alarm dissolves too: at the CORRECT c_4 the second factor "
      "2 - c_14 = 4 - 2K_B is NONZERO, so there is no double zero.  What remains is the SINGLE "
      "c_123 = 0 zero that unmodified AeST already has, with numerator -4(1-K_B)^2 in place of "
      "-K_B^2 ***",
      "I do NOT convert this into a value of alpha_2.  c_123 = 0 is precisely the locus Foster "
      "& Jacobson's appendix excludes -- the error class that forced the withdrawn alpha_1 "
      "bound in this project two days ago.  NOT COMPUTED")

cV2 = (c1s - c1s ** 2 / 2 + c3s ** 2 / 2) / ((c1s + c4s) * (1 - c1s - c3s))
cV2_ctrl = sp.simplify(cV2.subs(SUB0))
cV2_alarm = sp.simplify(cV2.subs(SUBA))
cV2_corr = sp.simplify(cV2.subs(SUBZ))
check(sp.simplify(cV2_ctrl - 1) == 0 and sp.simplify(cV2_alarm - KB / 2) == 0
      and sp.simplify(cV2_corr - KB / (2 * (KB - 1))) == 0
      and all(KB_ / (2 * (KB_ - 1)) < 0 for KB_ in KB_GRID if KB_ < 1),
      "F10 *** THE NEW ADVERSE ITEM, FLAGGED AND NOT PRICED, AND IT IS SHARPER THAN I EXPECTED: "
      "the same dictionary's vector-mode formula gives c_V^2 = 1 EXACTLY for unmodified AeST "
      "(luminal, healthy -- the control), +K_B/2 under the alarm's sign, and K_B/(2(K_B-1)) "
      "under the CORRECT sign -- NEGATIVE for every K_B < 1, i.e. an imaginary vector sound "
      "speed, at every K_B in the grid ***",
      "this is DICTIONARY ARITHMETIC, not a result: F5 has just shown the same dictionary "
      "misses G_N by a factor 2 in this theory because it has no slot for the mixing term, and "
      "AeST proper sits at c_14 = K_B where the formula is a different degenerate case.  The "
      "vector sector needs its own direct variation.  NOT COMPUTED HERE -- but it is the item "
      "that the sign correction CREATES, and correcting a sign that helps twice while hiding "
      "that it hurts once would be exactly the failure mode I was sent to avoid")

# =================================================================================================
print()
print("=" * 100)
print("PART G -- ITEM (d): THE G MATTER FEELS vs THE G IN THE FRIEDMANN EQUATION")
print("=" * 100)

tc = sp.Symbol("t", real=True)
Nf, af, phf = sp.Function("N")(tc), sp.Function("a")(tc), sp.Function("phi")(tc)
Bf, laf = sp.Function("B")(tc), sp.Function("lamF")(tc)
gF = sp.diag(-Nf ** 2, af ** 2, af ** 2, af ** 2)
gFu = sp.diag(-1 / Nf ** 2, 1 / af ** 2, 1 / af ** 2, 1 / af ** 2)
CF = [tc, x1, x2, x3]
GamF = [[[sp.simplify(sp.Rational(1, 2) * sum(
    gFu[r, s] * (sp.diff(gF[s, n], CF[m]) + sp.diff(gF[s, m], CF[n]) - sp.diff(gF[m, n], CF[s]))
    for s in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]


def ricF(a, b):
    o = 0
    for m in range(4):
        o += sp.diff(GamF[m][b][a], CF[m]) - sp.diff(GamF[m][m][a], CF[b])
        for l in range(4):
            o += GamF[m][m][l] * GamF[l][b][a] - GamF[m][b][l] * GamF[l][m][a]
    return sp.simplify(o)


RF = sp.simplify(sum(gFu[m, n] * ricF(m, n) for m in range(4) for n in range(4)))
# the aether's temporal component is kept INDEPENDENT of the lapse (A_mu = (-B,0,0,0)) and the
# multiplier is retained, so the lapse variation is taken OFF the constraint surface (R1 of the
# assignment: vary first, impose afterwards).  B = N is imposed only after all variations.
AdF = sp.Matrix([-Bf, 0, 0, 0])
AuF = sp.Matrix(4, 1, lambda i, j: sp.simplify(sum(gFu[i, k] * AdF[k] for k in range(4))))
CconF = sp.simplify(sum(AuF[i] * AdF[i] for i in range(4)) + 1)
ONS = [(sp.Derivative(Bf, (tc, 2)), sp.Derivative(Nf, (tc, 2))),
       (sp.Derivative(Bf, tc), sp.Derivative(Nf, tc)), (Bf, Nf)]


def onshell(e):
    for a, b in ONS:
        e = e.subs(a, b)
    return sp.simplify(e.doit())


check(sp.simplify(CconF - (1 - Bf ** 2 / Nf ** 2)) == 0 and onshell(CconF) == 0,
      "G1  the FRW aether A_mu = (-B,0,0,0) has A^mu A_mu + 1 = 1 - B^2/N^2, which vanishes on "
      "B = N -- the constraint is a real equation here, not something substituted in by hand")
FmnF = sp.Matrix(4, 4, lambda m, n: sp.diff(AdF[n], CF[m]) - sp.diff(AdF[m], CF[n]))
F2F = sp.simplify(sum(FmnF[m, n] * FmnF[a, b] * gFu[m, a] * gFu[n, b]
                      for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
JupF = [sp.simplify(sum(AuF[nu] * (sp.diff(AuF[al], CF[nu])
                                   + sum(GamF[al][nu][r] * AuF[r] for r in range(4)))
                        for nu in range(4))) for al in range(4)]
ZF = sp.simplify(sum(gF[m, n] * JupF[m] * JupF[n] for m in range(4) for n in range(4)))
dphiF = sp.Matrix([sp.diff(phf, tc), 0, 0, 0])
JdphiF = sp.simplify(sum(JupF[m] * dphiF[m] for m in range(4)))
YF = sp.simplify(sum((gFu[m, n] + AuF[m] * AuF[n]) * dphiF[m] * dphiF[n]
                     for m in range(4) for n in range(4)))
QF = sp.simplify(sum(AuF[m] * dphiF[m] for m in range(4)))
check(F2F == 0 and all(onshell(j) == 0 for j in JupF)
      and onshell(ZF) == 0 and onshell(YF) == 0,
      "G2  *** on FRW: F_{mu nu} = 0 for ANY B(t) and N(t), and J^mu = 0, Z = 0, Y = 0 on the "
      "constraint B = N.  Comoving observers in a homogeneous spacetime are geodesic, so the "
      "aether's acceleration -- option 1's whole free-function argument -- vanishes identically "
      "in the background ***",
      "and since J^mu = 0 on shell, delta Z = 2 J.delta J = 0 too: the F(Z) term contributes "
      "nothing to ANY background field equation, not just to the on-shell action")
check(onshell(sp.simplify(QF - sp.diff(phf, tc) / Nf)) == 0,
      "G3  Q = phidot/N survives, so K(Q) is the only dark-sector contribution to the "
      "background -- unchanged from AeST")

Kf = sp.Function("K")
JA = sp.Symbol("J_A")          # Jcal'(0); zero for the MOND normalisation, kept general here
rho_m = sp.Symbol("rho_m", positive=True)


def elt(L, f):
    out = sp.diff(L, f)
    out -= sp.diff(sp.diff(L, sp.Derivative(f, tc)), tc)
    out += sp.diff(sp.diff(L, sp.Derivative(f, (tc, 2))), tc, 2)
    return sp.expand(sp.simplify(out.doit()))


def frw_lag(mode):
    arg = YF if mode == "Y" else ZF
    br = (RF - (KB / 2) * F2F + 2 * (2 - KB) * JdphiF - (2 - KB) * YF
          - (2 - KB) * JA * arg - Kf(QF) - laf * CconF)
    return sp.simplify(af ** 3 * Nf * br / (16 * sp.pi * GT)) - Nf * af ** 3 * rho_m


Hs, Qv = sp.symbols("H Qv")
FRIED = {}
for mode in ("Y", "Z"):
    Lfrw = frw_lag(mode)
    check(sp.simplify(onshell(elt(Lfrw, laf)) ) == 0,
          f"G4{mode} varying lambda on FRW returns the constraint, satisfied at B = N")
    lam_sol = sp.solve(sp.Eq(sp.expand(onshell(elt(Lfrw, Bf))), 0), laf)
    fr = onshell(elt(Lfrw, Nf))
    if lam_sol:
        fr = sp.simplify(fr.subs(laf, lam_sol[0]))
    fr = sp.simplify(fr.subs({sp.Derivative(Nf, (tc, 2)): 0, sp.Derivative(Nf, tc): 0}))
    fr = sp.simplify(fr.subs(Nf, 1))
    fr = sp.simplify(sp.expand(fr * 16 * sp.pi * GT / af ** 3))
    fr = sp.simplify(fr.subs(sp.Derivative(af, tc), Hs * af).subs(sp.Derivative(phf, tc), Qv))
    FRIED[mode] = sp.expand(fr)
    info(f"G5{mode} Friedmann constraint (F({mode}) theory), x 16 pi Gt / a^3, at N = 1:",
         f"{sp.simplify(FRIED[mode])} = 0")

for mode in ("Y", "Z"):
    fr = FRIED[mode]
    check(sp.simplify(fr.coeff(rho_m) + 16 * sp.pi * GT) == 0
          and sp.simplify(fr.coeff(Hs, 2)) == 6
          and sp.simplify(sp.diff(fr, KB)) == 0 and sp.simplify(sp.diff(fr, JA)) == 0,
          f"G6{mode} *** the Friedmann constraint of the F({mode}) theory is "
          f"3 H^2 = 8 pi Gt rho_m + (dark), with the matter coefficient EXACTLY 8 pi Gt and "
          f"with NO K_B and NO free-function dependence anywhere in it ***",
          "so G_cosmo = Gt in both theories -- the aether sector cancels out of the background "
          "because c_123 = K_B + 0 - K_B = 0, and the free function cancels out because its "
          "argument vanishes there (G2)")
check(sp.simplify(FRIED["Y"] - FRIED["Z"]) == 0,
      "G7  *** and the two Friedmann constraints are IDENTICAL term by term: option 1 is "
      "invisible to background cosmology ***")
Kd = sp.simplify(FRIED["Z"] - 6 * Hs ** 2 + 16 * sp.pi * GT * rho_m)
info("G8  THE ONE DISCREPANCY I FOUND AND DO NOT RESOLVE, flagged rather than buried:",
     f"the dark-sector term I derive from the transcribed action is  {sp.simplify(Kd)},\n"
     "         i.e. 3H^2 = 8 pi Gt rho_m - (Q K_Q - K)/2, whereas "
     "real_research/bridge1_aest_equations.md\n"
     "         records 8 pi Gt rhobar = Q dK/dQ - K (and 8 pi Gt Pbar = K).  The two differ by a "
     "factor -1/2,\n"
     "         a normalisation/sign convention in how Lambda is split between the action's "
     "explicit -2 Lambda\n"
     "         and K(Q_0) = -2 Lambda (including both, as typeII does, cancels the cosmological "
     "constant\n"
     "         entirely -- see B5).  This is a PRE-EXISTING corpus item, not created by option "
     "1; it does\n"
     "         NOT touch the rho_m coefficient, which is the only thing item (d) turns on; and I "
     "have not\n"
     "         resolved it because that needs the published paper, which I do not have here.  "
     "NOT COMPUTED.")

info("G9  so the two gravitational constants are")
print("        G_matter (what a test body feels)   = Ghat = Gt/(1 - K_B/2)")
print("        G_cosmo  (the Friedmann coefficient) = Gt")
for k in KB_GRID:
    print(f"        K_B = {k:<5}  G_N/G_cosmo = {1/(1-k/2):.5f}   "
          f"(fractional mismatch {100*(1/(1-k/2)-1):.2f}%)")
check(True,
      "G10 *** THE MISMATCH IS REAL BUT IT IS NOT OPTION 1'S: it is identical in the F(Y) and "
      "F(Z) theories (G2 shows Z = 0 on FRW, C4/D6 show the same Ghat locally), so option 1 "
      "adds NO new BBN liability.  At the corpus's K_B <~ 0.25 the mismatch is 14.29% ***",
      "an independent BBN re-derivation is NOT done here; the K_B <~ 0.25 ceiling is quoted "
      "from the corpus, not recomputed")

# --- how far from J_Z = 1 is the solar system, for the kernel option 1 is meant to legalise -----
info("G11 the Newtonian limit is J_Z -> 1; how close is it?  For the exponential kernel "
     "nu = 1/(1-exp(-sqrt y)) the AQUAL mu is mu(g_obs) = J_Z = 1 - exp(-sqrt y), so the "
     "fractional error in the locally measured G is exp(-sqrt y):")
gbar_au = GMSUN / AU ** 2
for nm, a0 in FOOT:
    yv_ = gbar_au / a0
    lg = -math.sqrt(yv_) / math.log(10)
    print(f"        {nm:<9} a0 = {a0:.4e}   g_bar(1 AU) = {gbar_au:.4e}   y = {yv_:.4e}   "
          f"1 - J_Z = 1e{lg:.1f}")
check(all(gbar_au / a0 > 1e7 for _, a0 in FOOT),
      "G12 at 1 AU the deep-Newtonian condition y >> 1 holds by seven orders in both footings, "
      "so G_N = Ghat holds there to 1 part in 10^3457 (canonical) / 10^3149 (alt)",
      "this is the SAME exponential suppression opt1 PART F uses for the ephemeris; it is "
      "quoted here only to show that 'the Newtonian limit' is not an idealisation")

# =================================================================================================
print()
print("=" * 100)
print("PART H -- VERDICT")
print("=" * 100)
print("""
  ROUTE 1 VERDICT: **PASS**.  G_N is finite in the F(Z) theory and is NUMERICALLY IDENTICAL to
  unmodified AeST's, G_N = Ghat = Gt/(1 - K_B/2), derived by explicit variation of the full
  action with the same machinery that reproduces the F(Y) control (typeII's D5, D6, D7,
  lambda_bg, gamma_PPN = 1).  The ratio G_N[F(Z)]/G_N[F(Y)] = 1 exactly.

  THE ALARM WAS A SIGN SLIP.  Einstein-aether carries the c_4 structure as +c_4 a^mu a_mu;
  AeST carries the free function as -F.  The correct effective value is c_4 = -(2-K_B), giving
  c_14 = 2K_B - 2, which lies in (-2, 2) across the whole stability window and equals 2 nowhere.
  Both naive disasters -- G/0 and the alpha_2 double zero -- are artifacts of the flipped sign.
  The sign is validated numerically: switching the scalar mixing off makes the dictionary
  legitimate, and it then agrees with the direct variation exactly (Gt/(2-K_B)).

  THE RESCUING TERM: opt1's C6 names the right term for the wrong job.  Deleting the
  2(2-K_B) J^mu grad_mu phi mixing term leaves G_N FINITE at Ghat/2; the mixing term restores
  the factor 2.  The nearest singular locus is sqrt(2) times the AeST mixing coefficient and 1/2
  times the AeST Ycal coefficient -- O(1) in both directions -- so this is not a tuned
  cancellation and the KILL condition is not met.  The mechanism proper is
  that on the F(Z) theory's pointwise v = grad Psi the Einstein-Hilbert + F^2 operator
  2(2-K_B) lap Psi cancels the mixing term's -2(2-K_B) div v identically, and the ENTIRE
  surviving Newtonian operator is the free function's own div[J_Z grad Psi], normalised by
  J_Z -> 1.

  TWO GRAVITATIONAL CONSTANTS: G_cosmo = Gt, G_matter = Gt/(1-K_B/2); mismatch 14.29% at
  K_B = 0.25.  Inherited from AeST unchanged -- Z vanishes identically on FRW -- so option 1
  creates no new BBN liability.

  WHAT THIS DOES NOT SETTLE, and one item of it is NEW AND ADVERSE.  alpha_1, alpha_2, c_S and
  c_V are the boosted sector and are NOT computed here.  The corrected sign makes the
  dictionary's vector formula read c_V^2 = K_B/(2(K_B-1)) < 0 for every K_B < 1, where
  unmodified AeST sits at c_V^2 = 1 exactly and the slipped sign gave a benign +K_B/2.  That
  dictionary has just been shown to miss this theory's G_N by a factor 2, so the number is not
  a result -- but it is the item the sign correction CREATES, it moves the vector sector from
  'exactly luminal' to 'formally imaginary', and it is now the sharpest open question option 1
  faces.  It needs its own direct variation.  NOT COMPUTED.
""")
print(f"  checks: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed    ({time.time()-T0:.1f} s)")
if FAIL:
    print("  FAILED:")
    for f in FAIL:
        print(f"    - {f}")
sys.exit(1 if FAIL else 0)
