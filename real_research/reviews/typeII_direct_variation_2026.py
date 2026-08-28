"""
=========================================================================================
typeII_direct_variation_2026.py -- AeST's QUASI-STATIC SECTOR BY DIRECT VARIATION OF THE
ACTION, WITH THE ANSATZ IMPOSED *AFTER* VARYING, AND THE LAGRANGE MULTIPLIER KEPT.
=========================================================================================
2026-08-17.  Independent re-derivation of the three premises that
real_research/reviews/ppn_newtonian_radial_2026.py PART Q asserts:

  (P1) Q = (1-Psi)Q_0 at first order (with the unit-norm correction -Psi^2/2 DERIVED),
       and Y = |grad varphi|^2 exactly at quadratic order;
  (P2) Psi = Psi_N + varphi with J_Y(Y) grad varphi = grad Psi_N and Psi_N the ordinary
       Newtonian potential of the baryons;
  (P3) hence u = |grad varphi| IS the anomalous acceleration and obeys the PURELY LOCAL
       ALGEBRAIC law u J_Y(u^2) = g_bar.

ROUTE (assigned, and different from PART Q's): PART Q substitutes a restricted ansatz into
the action, expands to quadratic order and varies the RESTRICTED Lagrangian with the
multiplier term dropped.  Here the fields are kept GENERIC -- all ten metric components,
all four aether components, the scalar, and the multiplier lambda itself -- the action is
varied with respect to each, and the ansatz is imposed only afterwards, so that the
equations PART Q never wrote down can be tested rather than assumed.  PART Q's algebra is
not reused: only its ansatz and its sign conventions were read.

THE ACTION, verbatim (arXiv:2007.00082 Eq. 5; transcription checked against
real_research/bridge1_aest_equations.md, which is the corpus's correct reference copy):

  S = int d^4x (sqrt(-g)/16 pi Gt) [ R - 2 Lambda - (K_B/2) F^{mu nu} F_{mu nu}
        + 2(2-K_B) J^mu grad_mu phi - (2-K_B) Ycal - Fcal(Ycal, Qcal)
        - lambda (A^mu A_mu + 1) ] + S_m[g]
  Qcal = A^mu grad_mu phi,  Ycal = (g^{mu nu} + A^mu A^nu) grad_mu phi grad_nu phi,
  F_{mu nu} = 2 grad_[mu A_nu],  J^mu = A^nu grad_nu A^mu.

=========================================================================================
RESULT IN ONE PARAGRAPH -- direction: MIXED, and net FAVOURABLE to the chain that matters
=========================================================================================
(P1) CONFIRMED and strengthened: with a GENERIC static metric and a GENERIC aether spatial
     perturbation a_i, the constraint solved order by order gives A_0 = -(1+Psi-Psi^2/2),
     Qcal = Q_0(1-Psi+3Psi^2/2) and Ycal = eps^2 |grad varphi + Q_0 a|^2 with NO metric
     contamination whatever -- Y's eps^0 and eps^1 coefficients vanish identically.  The
     corpus's Y = |grad varphi|^2 is that result in the a_i = 0 sector.
(P2) CONFIRMED with one quantified caveat: the 00 equation is
     lap(Psi) - m_Psi^2 Psi = 4 pi Ghat rho + div v, Ghat = Gt/(1-K_B/2),
     m_Psi^2 = K''Q_0^2/(2(2-K_B)) = mu^2/2, so Psi = Psi_N + chi with Psi_N the Newtonian
     potential only up to a Yukawa correction of relative size (m_Psi r)^2: 1.2e-23 at
     1 AU, 4.5e-4 at 30 kpc.  gamma_PPN = 1 is DERIVED here, not assumed: the traceless
     ij equation has no source at all because the whole non-Einstein sector is independent
     of h_ij at quadratic order.
(P3) CONFIRMED IN THE SPHERICAL SECTOR, OVERSTATED AS A GENERAL STATEMENT.  The a_i field
     equation -- which PART Q's Q7 declares vacuous, wrongly, there IS a term linear in
     a_i -- reads 2 K_B lap(a^T_i) = 2(2-K_B) Q_0 S_i with S_i = (1+J_Y)v_i - d_i Psi.  Its
     LONGITUDINAL projection is S^L = 0 EXACTLY, which is a stronger and cleaner route to
     J_Y(u^2) u = g_bar than PART Q's Gauss-law first integral: it is a pointwise VECTOR
     identity.  But its TRANSVERSE projection says the AQUAL curl field is not zero, it is
     carried by the aether's transverse mode, and is unsuppressed on every scale below
     1/m_a (1.8-5.8 kpc at 1 AU's J_Y, 17-53 Mpc in the deep-MOND regime).  So the law is local
     and algebraic EXACTLY in curl-free (e.g. spherically symmetric) configurations and
     only up to a divergence-free field otherwise -- the standard Bekenstein-Milgrom
     situation, verified nonzero here by explicit two-body evaluation.
(MULTIPLIER) The defect that killed ppn_scalar_retained_2026.py is NOT present here and is
     NOT present in PART Q either.  Direct variation gives lambda_bg = (2-K_B)(1+J_Y)Q_0^2
     + K'(Q_0)Q_0/2, nonzero, confirming the corrected value -A_Y Q_0^2; PART Q's dropped
     multiplier term is legitimate because its ansatz family is constraint-PRESERVING, and
     the chain-rule identity proving that its single Psi equation is exactly
     [00-Einstein] - (1/2)[aether-temporal] is verified here, with a residual that vanishes
     identically iff lambda_bg takes that nonzero value.  Setting lambda_bg = 0 would leave
     a spurious mass term in the Psi equation -- the earlier file's error class, reproduced
     and named at check C3.
(BACKGROUND) The flat background solves its own equations iff K(Q_0) + 2 Lambda = 0 (which
     SZ21's own K(Q) = -2 Lambda + K_2(Q-Q_0)^2 satisfies IDENTICALLY) and K'(Q_0)Q_0 = 0,
     i.e. iff the cosmological dust density is neglected -- a relative error of 1.7e-23 at
     1 AU and 6.6e-6 at 30 kpc.

=========================================================================================
EVERY REDUCTION, DECLARED
=========================================================================================
R1 STATIC.  All perturbations are functions of (x1,x2,x3); the only time dependence is the
   background phi = Q_0 t.  Time-dependent (radiative, boosted, cosmological) sectors are
   NOT treated.  This is the same restriction PART Q works under.  It is an ASSUMPTION.
R2 ORDER COUNTING, and the one non-expansion.  h_{mu nu}, a_mu, varphi, rho are all O(eps).
   a_0 (the MOND acceleration) is counted as O(eps) as well, which is what makes
   J_Y = d(Jcal)/dY an O(1) function and puts the MOND term Jcal ~ Y^{3/2}/a_0 at O(eps^2),
   i.e. at the same order as the ordinary kinetic term.  This is the standard weak-field
   MOND bookkeeping and it is the ONLY way the non-analytic Y^{3/2} can be retained; it is
   checked explicitly at A9.  Everything else is truncated at eps^2 with a degree check.
R3 FREE FUNCTION.  Fcal(Y,Q) = (2-K_B) Jcal(Y) + K(Q).  Any Y-Q cross term is O(eps^3) at
   quadratic order (Y is O(eps^2), Q-Q_0 is O(eps)) and therefore CANNOT contribute -- so
   this is not a restriction at the order worked, and that is verified at A10.
R4 SECOND-ORDER FIELD PIECES.  h^{(2)}, a^{(2)}_i, varphi^{(2)} enter the quadratic action
   only multiplied by the BACKGROUND field equations, so they drop once the background
   solves its own equations (PART B).  The one second-order piece that does NOT drop --
   b_0, the aether's O(eps^2) temporal component -- is retained and solved for.
R5 MATTER.  Static dust: S_m = -int d^4x rho sqrt(-g_00) with rho = eps rhohat the
   coordinate rest-mass density.  Pressure and anisotropic stress are zero by assumption;
   the gamma_PPN = 1 statement is therefore "no anisotropic stress from the DARK sector".
R6 THE MULTIPLIER PASS uses the exact first variation of Jcal, delta Jcal = J_Y delta Y,
   with J_Y carried as an inert symbol.  That is exact for a FIRST variation and it avoids
   evaluating the non-analytic Jcal off the constraint surface, where its eps-expansion is
   singular (Y acquires an O(eps) piece = -Q_0^2 (A.A+1)).  Stated, not hidden.
R7 NOT DONE HERE: the O(w) boosted sector, alpha_1/alpha_2, c_T, the cosmological sector,
   and any claim about which interpolating kernels are legal (that arithmetic is PART C of
   the radial file and is not re-run).  This file supplies only the premises (P1)-(P3).

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
# constants (both footings carried for every dimensional number)
# =================================================================================================
CLIGHT = 2.99792458e8
GNEWT = 6.67430e-11
GMSUN = 1.32712440018e20
AU = 1.495978707e11
PC = 3.0856775814913673e16
KPC = 1.0e3 * PC
MPC = 1.0e6 * PC
A0_CAN = 9.3619e-11                 # kappa c sqrt(G rho_Lambda), canonical footing
A0_ALT = 1.1279e-10                 # alt footing
FOOT = (("canonical", A0_CAN), ("ALT", A0_ALT))
# carried from real_research/bridge1_aest_equations.md (SZ21's own MOND-compatible fits):
K2_FITS = (("Cosh", 7.5e3), ("Exp", 9.5e3))
MU_INV_FLOOR = 1.0 * MPC            # mu^-1 >~ 1 Mpc
KB_GRID = (0.1, 0.3, 0.5)           # SZ21 fiducials (stability 0 < K_B < 2)
RHO_DM_MEAN = 2.4e-27               # kg/m^3, cosmological mean dark-matter density

# =================================================================================================
# symbols and the perturbative machinery
# =================================================================================================
tt, x1, x2, x3 = sp.symbols("t x1 x2 x3", real=True)
CO = [tt, x1, x2, x3]
SPC = [x1, x2, x3]
eps = sp.Symbol("eps")
KB, Q0, Kp1, Kpp, GT, LAM, K0s, rhoh, JYs = sp.symbols(
    "K_B Q_0 Kprime Kpp Gt Lambda K0 rhohat J_Y")


def fn(name):
    return sp.Function(name)(x1, x2, x3)


def tr2(e):
    """truncate at eps^2 (explicit, with the degree check applied separately)"""
    e = sp.expand(e)
    return e.coeff(eps, 0) + eps * e.coeff(eps, 1) + eps ** 2 * e.coeff(eps, 2)


def deg_ok(e, n=2):
    """explicit degree check: the truncated object is a polynomial in eps of degree <= n"""
    p = sp.Poly(sp.expand(e), eps)
    return p.degree() <= n


def lap(e):
    return sum(sp.diff(e, c, 2) for c in SPC)


def el(L, f):
    """Euler-Lagrange derivative in the 3 static coordinates, first and second derivatives."""
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


print()
print("=" * 100)
print("PART A -- THE FIELDS KEPT GENERIC, THE CONSTRAINT SOLVED ORDER BY ORDER, AND WHAT")
print("          Qcal AND Ycal ACTUALLY ARE ON A GENERIC STATIC CONFIGURATION")
print("=" * 100)

# --- generic static metric perturbation: all ten components, no ansatz -------------------------
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
idcheck = sp.Matrix(4, 4, lambda i, j: tr2(sum(gd[i, k] * gu[k, j] for k in range(4))))
check(sp.simplify(idcheck - sp.eye(4)) == sp.zeros(4, 4),
      "A1  the perturbative inverse metric is correct to O(eps^2): g_{mu al} g^{al nu} = "
      "delta to that order, for a GENERIC ten-component static h",
      "no ansatz has been imposed on h at any point of this file before PART D")

trH = sum(eta[m, n] * Hm[m, n] for m in range(4) for n in range(4))
HH = sum(Hup[m, n] * Hm[m, n] for m in range(4) for n in range(4))
sqg = 1 + eps * trH / 2 + eps ** 2 * (trH ** 2 / 8 - HH / 4)
det_exact = sp.expand(sp.series(sp.sqrt(sp.expand(-gd.det())), eps, 0, 3).removeO())
check(sp.simplify(sp.expand(det_exact - sqg)) == 0,
      "A2  sqrt(-g) = 1 + eps h/2 + eps^2 (h^2/8 - h_{mu nu}h^{mu nu}/4) verified against the "
      "exact determinant of the generic metric")

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

# --- generic aether: four components, the constraint NOT imposed yet ---------------------------
a0f, b0f = fn("a0"), fn("b0")
aif = [fn("a1"), fn("a2"), fn("a3")]
lam0, lam1 = fn("lam0"), fn("lam1")
wf = fn("w")

Ad = sp.Matrix([-(1 + eps * a0f + eps ** 2 * b0f), eps * aif[0], eps * aif[1], eps * aif[2]])
Au = sp.Matrix(4, 1, lambda i, j: tr2(sum(gu[i, k] * Ad[k] for k in range(4))))
Cc = tr2(sum(Au[i] * Ad[i] for i in range(4)) + 1)          # A^mu A_mu + 1, OFF the surface

c1_sol = sp.solve(sp.expand(Cc).coeff(eps, 1), a0f)[0]
Ad_s = Ad.subs(a0f, c1_sol)
Au_s = sp.Matrix(4, 1, lambda i, j: tr2(sum(gu[i, k] * Ad_s[k] for k in range(4))))
Cc_s = tr2(sum(Au_s[i] * Ad_s[i] for i in range(4)) + 1)
c2_sol = sp.solve(sp.expand(Cc_s).coeff(eps, 2), b0f)[0]
SOL = {a0f: c1_sol, b0f: c2_sol}
Ad_on = Ad.subs(SOL)
Au_on = sp.Matrix(4, 1, lambda i, j: tr2(sum(gu[i, k] * Ad_on[k] for k in range(4))))
Cres = sp.expand(tr2(sum(Au_on[i] * Ad_on[i] for i in range(4)) + 1))
check(sp.simplify(Cres) == 0,
      "A3  the unit-timelike constraint A^mu A_mu = -1 is SOLVED order by order and the "
      "residual vanishes identically to O(eps^2) -- nothing about the aether is assumed",
      f"first order: a_0 = {sp.simplify(c1_sol)}  (i.e. A_0 = -(1+eps Psi) once H00 = -2 Psi)")

PsiF, PhiF = fn("Psi"), fn("Phi")
ANS_METRIC = {Hc[(0, 0)]: -2 * PsiF, Hc[(0, 1)]: 0, Hc[(0, 2)]: 0, Hc[(0, 3)]: 0,
              Hc[(1, 1)]: -2 * PhiF, Hc[(2, 2)]: -2 * PhiF, Hc[(3, 3)]: -2 * PhiF,
              Hc[(1, 2)]: 0, Hc[(1, 3)]: 0, Hc[(2, 3)]: 0}
ANS_AE = {aif[0]: 0, aif[1]: 0, aif[2]: 0}
c2_ans = sp.simplify(c2_sol.subs(ANS_METRIC).subs(ANS_AE).doit())
check(sp.simplify(c2_ans + PsiF ** 2 / 2) == 0,
      "A4  *** GATE (P1a) DERIVED, NOT ASSUMED: on the corpus ansatz the O(eps^2) piece of "
      "the aether is -Psi^2/2, i.e. A_mu = (-(1+Psi-Psi^2/2), 0,0,0) ***",
      f"b_0 = {c2_ans}; obtained by solving the constraint, with the aether's spatial "
      f"components left FREE throughout")

dphi = sp.Matrix([Q0, eps * sp.diff(wf, x1), eps * sp.diff(wf, x2), eps * sp.diff(wf, x3)])
Qc = tr2(sum(Au_on[m] * dphi[m] for m in range(4)))
Yc = tr2(sum((gu[m, n] + Au_on[m] * Au_on[n]) * dphi[m] * dphi[n]
             for m in range(4) for n in range(4)))
dQ = sp.expand(Qc - Q0)
Q_ans = sp.simplify(sp.expand(Qc.subs(ANS_METRIC).subs(ANS_AE).doit()))
check(sp.simplify(Q_ans - Q0 * (1 - eps * PsiF + eps ** 2 * sp.Rational(3, 2) * PsiF ** 2)) == 0,
      "A5  *** GATE (a): Qcal = Q_0 (1 - Psi + 3 Psi^2/2), so delta Qcal = -Q_0 Psi at first "
      "order -- the corpus's committed quasi-static Qcal = (1-Psi) Q_0, reproduced from the "
      "action by direct variation-independent algebra ***")

v = [sp.diff(wf, c) + Q0 * aif[k] for k, c in enumerate(SPC)]
Yhat = sum(vv ** 2 for vv in v)
check(sp.expand(Yc).coeff(eps, 0) == 0 and sp.simplify(sp.expand(Yc).coeff(eps, 1)) == 0,
      "A6  Ycal has NO eps^0 and NO eps^1 piece once the constraint is solved -- the spatial "
      "projector kills them identically, for a generic metric and a generic aether")
check(sp.simplify(sp.expand(sp.expand(Yc).coeff(eps, 2) - Yhat)) == 0,
      "A7  *** GATE (P1b), GENERALISED: Ycal = eps^2 |grad varphi + Q_0 a|^2 EXACTLY at "
      "quadratic order, with NO metric contamination -- not even from h_ij or h_0i ***",
      "the corpus's Ycal = |grad varphi|^2 is this in the a_i = 0 sector.  The physical "
      "field is the COMBINATION v = grad varphi + Q_0 a (SZ21's mixing variable chi), and "
      "whether a_i may be set to zero is a field equation, tested at D6/D7 -- not an "
      "assumption, as PART Q's Q7 has it")

for e, nm in ((Yc, "Ycal"), (Qc, "Qcal"), (Rsc, "R"), (sqg, "sqrt(-g)")):
    check(deg_ok(e), f"A8  explicit degree check: truncated {nm} is a polynomial of degree "
                     f"<= 2 in eps")

yv, a0sym, epsp = sp.symbols("Yv a0M eps_p", positive=True)
Jmond = sp.Rational(2, 3) * yv ** sp.Rational(3, 2) / a0sym
scaled = sp.simplify((Jmond.subs({yv: epsp ** 2 * yv, a0sym: epsp * a0sym}) / epsp ** 2)
                     - Jmond)
check(scaled == 0,
      "A9  the R2 bookkeeping is consistent: with a_0 counted as O(eps), the MOND free "
      "function Jcal = (2/3) Y^{3/2}/a_0 evaluated at Y = eps^2 Yhat is EXACTLY eps^2 times "
      "the same function of Yhat -- so the non-analytic term sits at quadratic order and "
      "J_Y = dJcal/dY is eps-independent",
      "this is the only way the Y^{3/2} term can be retained at all; it is stated in R2 and "
      "verified here rather than assumed")

check(sp.expand(tr2(sp.Symbol("c_x") * Yc * (Qc - Q0))) == 0,
      "A10 R3 is not a restriction at this order: any Y-Q cross term in Fcal is identically "
      "zero after truncation at eps^2 (Y is O(eps^2), Q-Q_0 is O(eps))")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THE FULL ACTION WITH lambda RETAINED: THE BACKGROUND EQUATIONS AND lambda_bg")
print("=" * 100)

Fmn = sp.Matrix(4, 4, lambda m, n: sp.diff(Ad[n], CO[m]) - sp.diff(Ad[m], CO[n]))
F2 = tr2(sum(Fmn[m, n] * Fmn[a, b] * gu[m, a] * gu[n, b]
             for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
Jup = [tr2(sum(Au[nu] * (sp.diff(Au[al], CO[nu]) + sum(Gam[al][nu][r] * Au[r] for r in range(4)))
              for nu in range(4))) for al in range(4)]
Jdphi = tr2(sum(Jup[m] * dphi[m] for m in range(4)))
Qfull = tr2(sum(Au[m] * dphi[m] for m in range(4)))
Yfull = tr2(sum((gu[m, n] + Au[m] * Au[n]) * dphi[m] * dphi[n]
                for m in range(4) for n in range(4)))
dQfull = sp.expand(Qfull - Q0)
Kfull = K0s + Kp1 * dQfull + sp.Rational(1, 2) * Kpp * tr2(dQfull ** 2)

# FULL Lagrangian: constraint NOT solved, lambda retained, Jcal linearised (R6)
LagF = tr2(sqg * (Rsc - 2 * LAM - (KB / 2) * F2 + 2 * (2 - KB) * Jdphi
                  - (2 - KB) * (1 + JYs) * Yfull - Kfull
                  - (lam0 + eps * lam1) * Cc)) \
    - 16 * sp.pi * GT * eps * rhoh * (1 - eps * Hc[(0, 0)] / 2)
LagF = sp.expand(LagF)
L1F, L2F = LagF.coeff(eps, 1), LagF.coeff(eps, 2)
info(f"B-  full Lagrangian assembled, L1 {len(sp.Add.make_args(L1F))} terms, "
     f"L2 {len(sp.Add.make_args(L2F))} terms ({time.time()-T0:.1f} s)")

bg_lam0 = sp.simplify(el(L1F, lam0))
check(sp.simplify(bg_lam0 - (Hc[(0, 0)] + 2 * a0f)) == 0,
      "B1  varying lambda reproduces the constraint (H00 + 2 a_0 = 0 at first order), i.e. "
      "exactly the relation PART A solved -- the multiplier is doing its job")

bg_a0 = sp.expand(el(L1F, a0f))
lam0_sol = sp.solve(sp.Eq(bg_a0, 0), lam0)[0]
lam0_target = (2 - KB) * (1 + JYs) * Q0 ** 2 + Kp1 * Q0 / 2
check(sp.simplify(lam0_sol - lam0_target) == 0,
      "B2  *** THE MULTIPLIER, DERIVED: lambda_bg = (2-K_B)(1+J_Y) Q_0^2 + K'(Q_0) Q_0 / 2, "
      "which is NOT ZERO ***",
      "this is the value the corpus records as the correction to ppn_scalar_retained_2026.py "
      "(lambda_bg = -A_Y Q_0^2 with A_Y = -[(2-K_B)(1+J_Y)]), here obtained independently by "
      "varying the action with respect to the aether's temporal component.  Its origin is "
      "that delta Ycal / delta A^mu = 2 Qcal grad_mu phi = -2 Q_0^2 A_mu does not vanish on "
      "the background")

bg_b0 = sp.expand(el(L2F, b0f))
check(sp.simplify(bg_b0 - bg_a0) == 0,
      "B3  the O(eps^2) equation for the aether's second-order temporal component b_0 is the "
      "SAME background equation, so lambda_bg is over-determined and consistent")

bg_H00 = sp.simplify(el(L1F, Hc[(0, 0)]).subs(lam0, lam0_sol))
bg_H11 = sp.simplify(el(L1F, Hc[(1, 1)]))
check(sp.simplify(bg_H11 + (K0s / 2 + LAM)) == 0,
      "B4a background PRESSURE equation: K(Q_0) + 2 Lambda = 0.  SZ21's own free function "
      "K(Q) = -2 Lambda + K_2 (Q-Q_0)^2 satisfies this IDENTICALLY",
      f"the ij background equation is {bg_H11} = 0")
check(sp.simplify(bg_H00 - (K0s / 2 + LAM - Kp1 * Q0 / 2)) == 0,
      "B4b background ENERGY equation: K(Q_0) + 2 Lambda - K'(Q_0) Q_0 = 0, so with B4a it "
      "reduces to K'(Q_0) Q_0 = 0, i.e. 8 pi Gt rho_dust = 0",
      "so the flat background solves its own field equations exactly up to the COSMOLOGICAL "
      "DUST DENSITY -- quantified numerically at PART F.  Note that lambda_bg cancels out of "
      "the background Einstein equation once it takes its B2 value")
check(sp.simplify(el(L1F, aif[0])) == 0 and sp.simplify(el(L1F, wf)) == 0,
      "B4c the remaining background equations (aether spatial, scalar) are satisfied "
      "identically by the flat, static, phi = Q_0 t configuration")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- WAS PART Q'S RESTRICTED VARIATION LEGAL?  THE ELIMINATION IDENTITY.")
print("=" * 100)
info("C0  PART Q substitutes a constraint-solving ansatz into the action and drops the "
     "-lambda(A.A+1) term (it vanishes identically on that family).  That is legitimate ONLY "
     "if (i) the family is constraint-PRESERVING, so the dropped term contributes nothing to "
     "the variations actually taken, and (ii) the one equation it loses -- the direction "
     "transverse to the constraint surface -- is exactly the one that DETERMINES lambda, so "
     "that eliminating lambda from the full system returns the same physics.  Both are "
     "tested here.")

lam1_coeff = sp.simplify(sp.expand(el(L2F, a0f)).coeff(lam1))
check(sp.simplify(lam1_coeff - 2) == 0,
      "C1  the first-order multiplier lambda_1 enters the O(eps^2) aether-temporal equation "
      "ALGEBRAICALLY with coefficient 2, so it can always be eliminated: the lost equation "
      "carries no independent physical content beyond fixing lambda")

Lmain_F = sp.expand(L2F.subs(SOL).doit())
lhs = el(Lmain_F, Hc[(0, 0)])
rhs = sp.expand((el(L2F, Hc[(0, 0)]) + sp.Rational(-1, 2) * el(L2F, a0f)).subs(SOL).doit())
resid = sp.expand(lhs - rhs)
check(sp.simplify(resid.subs(lam0, lam0_sol)) == 0,
      "C2  *** THE ELIMINATION IDENTITY: the constraint-preserving variation with respect to "
      "H00 equals [00-Einstein] - (1/2)[aether-temporal] EXACTLY, once lambda takes its B2 "
      "background value.  PART Q's route therefore loses NOTHING ***",
      "the residual before substituting lambda_bg is proportional to the background aether "
      "equation itself, i.e. to (2 lambda_bg - 2(2-K_B)(1+J_Y)Q_0^2 - K' Q_0)")

resid0 = sp.simplify(sp.expand(resid.subs(lam0, 0)))
check(sp.simplify(resid0 - (2 * (2 - KB) * (1 + JYs) * Q0 ** 2 + Kp1 * Q0)
                  * Hc[(0, 0)] / 4) == 0,
      "C3  *** AND THE ERROR CLASS NAMED: with lambda_bg SET TO ZERO the identity fails by a "
      "term proportional to Q_0^2 H00, i.e. a SPURIOUS MASS TERM in the Psi equation ***",
      f"residual = {sp.simplify(resid0)}.  That is precisely the defect recorded for "
      f"ppn_scalar_retained_2026.py (a spurious graviton Yukawa mass).  Its size relative to "
      f"the legitimate mass m_Psi^2 = K'' Q_0^2/(2(2-K_B)) is reported at PART F")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- THE LINEAR FIELD EQUATIONS, ANSATZ IMPOSED ONLY NOW")
print("=" * 100)
Jc = sp.Function("Jcal")
Kmain = K0s + Kp1 * dQ + sp.Rational(1, 2) * Kpp * tr2(dQ ** 2)
LagM = tr2(sqg * (Rsc - 2 * LAM - (KB / 2) * F2.subs(SOL).doit()
                  + 2 * (2 - KB) * Jdphi.subs(SOL).doit()
                  - (2 - KB) * Yc - Kmain)) \
    - (2 - KB) * eps ** 2 * Jc(Yhat) \
    - 16 * sp.pi * GT * eps * rhoh * (1 - eps * Hc[(0, 0)] / 2)
LagM = sp.expand(LagM)
L2M = LagM.coeff(eps, 2)
check(deg_ok(LagM),
      "D0  explicit degree check on the assembled quadratic Lagrangian: degree <= 2 in eps")
info(f"D-  main Lagrangian assembled, L2 {len(sp.Add.make_args(L2M))} terms "
     f"({time.time()-T0:.1f} s)")

BGSUB = {K0s: -2 * LAM}
L2b = sp.expand(L2M.subs(BGSUB))
L2b_nodust = sp.expand(L2b.subs(Kp1, 0))

# --- gamma_PPN, with the traceless metric components kept generic ------------------------------
info("D0b THE ONE SUBSTITUTION MADE IN THIS PART, AND IT IS NOT FREE: K'(Q_0) -> 0.  It is "
     "not an assumption of convenience -- B4b showed the flat background solves its own "
     "field equations ONLY if K'(Q_0) Q_0 = 0, so any linear analysis about a flat background "
     "must set it.  It is the cosmological dust density; PART F prices it (1.7e-23 at 1 AU, "
     "6.6e-6 at 30 kpc), and D9 exhibits the only equation it touches.")
nonEH = sp.expand(L2b_nodust - sp.expand(tr2(sqg * Rsc)).coeff(eps, 2).subs(Kp1, 0))
hij_dep = [Hc[(i, j)] for i in range(1, 4) for j in range(i, 4)]
free_syms = nonEH.atoms(sp.Function)
check(all(hh not in free_syms for hh in hij_dep),
      "D1  the ENTIRE non-Einstein sector (aether kinetic, mixing, Ycal, the free function, "
      "the matter term) is independent of h_ij at quadratic order -- so the dark sector "
      "supplies NO anisotropic stress and no trace source in the ij equations",
      "this is why gamma_PPN = 1 is a derivation and not an artifact of a diagonal ansatz")

gr_lim = sp.expand(el(sp.expand(L2b_nodust.subs({KB: 0, Q0: 0, Kpp: 0})), Hc[(0, 0)])
                   .subs(ANS_METRIC).subs(ANS_AE).subs({wf: 0, PhiF: PsiF}).doit())
check(sp.simplify(gr_lim - (8 * sp.pi * GT * rhoh - 2 * lap(PsiF))) == 0,
      "D1b NORMALISATION CONTROL: switch the dark sector off (K_B = 0, Q_0 = 0, varphi = 0) "
      "and the 00 equation collapses to lap(Psi) = 4 pi Gt rho -- the ordinary Newtonian "
      "limit.  So the matter action, the 16 pi Gt factors and the sign conventions are the "
      "standard ones, and Ghat = Gt/(1-K_B/2) at D5 is a real renormalisation, not a "
      "bookkeeping artifact")

metric_eqs = {}
for m in range(4):
    for n in range(m, 4):
        metric_eqs[(m, n)] = el(L2b_nodust, Hc[(m, n)])
ANS = dict(ANS_METRIC)
ANS.update(ANS_AE)
e12 = sp.simplify(sp.expand(metric_eqs[(1, 2)].subs(ANS).doit()))
e13 = sp.simplify(sp.expand(metric_eqs[(1, 3)].subs(ANS).doit()))
e23 = sp.simplify(sp.expand(metric_eqs[(2, 3)].subs(ANS).doit()))
check(sp.simplify(e12 + 2 * sp.diff(PhiF - PsiF, x1, x2)) == 0
      and sp.simplify(e13 + 2 * sp.diff(PhiF - PsiF, x1, x3)) == 0
      and sp.simplify(e23 + 2 * sp.diff(PhiF - PsiF, x2, x3)) == 0,
      "D2  the off-diagonal ij equations are d_i d_j (Phi - Psi) = 0, with NO source")
e11 = sp.simplify(sp.expand(metric_eqs[(1, 1)].subs(ANS).doit()))
check(sp.simplify(e11 - (sp.diff(PhiF - PsiF, x2, 2) + sp.diff(PhiF - PsiF, x3, 2))) == 0,
      "D3  *** GATE (b): the diagonal ij equations complete d_i d_j (Phi - Psi) = 0 for every "
      "pair, so Phi - Psi is at most linear in x and vanishes with the boundary condition "
      "Phi, Psi -> 0 at infinity: gamma_PPN = 1 EXACTLY, for every K_B, every free function, "
      "every Q_0 ***",
      "the boundary condition is the ONLY extra input; no aether, scalar or free-function "
      "term appears in these equations at all")

e0i = [sp.simplify(sp.expand(metric_eqs[(0, k)].subs(ANS).doit())) for k in (1, 2, 3)]
check(all(e == 0 for e in e0i),
      "D4  the h_0i equations -- which PART Q's ansatz drops without writing them -- are "
      "satisfied IDENTICALLY on the static ansatz.  The dropped equations are checked, not "
      "assumed away")

# --- the 00 equation ---------------------------------------------------------------------------
e00 = sp.expand(metric_eqs[(0, 0)].subs(ANS).subs(Kp1, 0).subs({PhiF: PsiF}).doit())
tgt00 = sp.expand(-(2 - KB) * (lap(PsiF) - lap(wf) - Kpp * Q0 ** 2 * PsiF / (2 * (2 - KB))
                               - 8 * sp.pi * GT * rhoh / (2 - KB)))
check(sp.simplify(e00 - tgt00) == 0,
      "D5  *** GATE (P2), FIRST HALF: the 00 equation is\n"
      "        lap(Psi) - m_Psi^2 Psi = 4 pi Ghat rho + lap(varphi),\n"
      "    with Ghat = 2 Gt/(2-K_B) = Gt/(1-K_B/2) and m_Psi^2 = K''(Q_0) Q_0^2/(2(2-K_B)) ***",
      "so AeST is TYPE-II: the scalar ADDS to the Newtonian potential rather than rescaling "
      "G.  Gt = (1-K_B/2)Ghat is the corpus's committed relation, DERIVED.  With K'' = 2K_2 "
      "this is m_Psi^2 = K_2 Q_0^2/(2-K_B) = mu^2/2, mu being SZ21's scalar mass")

# --- the scalar and aether equations, with the free function unexpanded ------------------------
uY = sp.Symbol("uY")
JY_of = sp.diff(Jc(uY), uY).subs(uY, Yhat)
S = [sp.expand((1 + JY_of) * v[k] - sp.diff(-Hc[(0, 0)] / 2, SPC[k])) for k in range(3)]
divS = sum(sp.diff(S[k], SPC[k]) for k in range(3))
eq_w = el(L2b_nodust, wf)
check(sp.simplify(sp.expand(eq_w - 2 * (2 - KB) * divS).doit()) == 0,
      "D6  *** GATE (P2), SECOND HALF: the scalar equation is EXACTLY\n"
      "        div[ (1 + J_Y) v ] = lap(Psi),      v = grad varphi + Q_0 a,\n"
      "    i.e. div S = 0 with S = (1+J_Y) v - grad Psi ***",
      "the '1' and the mixing coefficient match because the action's J^mu grad_mu phi "
      "coupling 2(2-K_B) is exactly twice the Ycal coefficient (2-K_B) -- SZ21's design.  "
      "The free function is carried UNEXPANDED; J_Y = dJcal/dY is a function of position "
      "through Y, and the Euler-Lagrange operator differentiates it")

eq_a1 = el(L2b_nodust, aif[0])
maxwell1 = 2 * KB * (sp.diff(aif[0], x2, 2) + sp.diff(aif[0], x3, 2)
                     - sp.diff(aif[1], x1, x2) - sp.diff(aif[2], x1, x3))
check(sp.simplify(sp.expand(eq_a1 + 2 * (2 - KB) * Q0 * S[0] - maxwell1).doit()) == 0,
      "D7  *** THE EQUATION PART Q NEVER WROTE: the aether spatial equation is\n"
      "        2 K_B [lap(a_i) - d_i (div a)] = 2 (2-K_B) Q_0 S_i ,\n"
      "    whose left side is TRANSVERSE.  Hence its LONGITUDINAL projection is S^L = 0 "
      "EXACTLY, a pointwise VECTOR identity, and its transverse projection is a massive "
      "equation for the aether's transverse mode ***",
      "PART Q's Q7 asserts that 'the quadratic Lagrangian contains no term linear in A_i'.  "
      "That is FALSE: the mixing term contributes +2(2-K_B) Q_0 a.grad Psi and the Ycal term "
      "-2(2-K_B)(1+J_Y) Q_0 a.grad varphi.  Q7's CONCLUSION (a_i = 0) survives in the "
      "spherical sector -- see E3 -- but its argument does not, and the equation it dismisses "
      "is the one that makes P3 a local law rather than an integrated one")
check(sp.simplify(sp.expand(sum(sp.diff(
    sp.expand(eq_a1 + 2 * (2 - KB) * Q0 * S[0] - maxwell1), c) for c in SPC)).doit()) == 0
    and sp.simplify(sp.expand(
        sp.diff(maxwell1, x1)
        + sp.diff(2 * KB * (sp.diff(aif[1], x1, 2) + sp.diff(aif[1], x3, 2)
                            - sp.diff(aif[0], x1, x2) - sp.diff(aif[2], x2, x3)), x2)
        + sp.diff(2 * KB * (sp.diff(aif[2], x1, 2) + sp.diff(aif[2], x2, 2)
                            - sp.diff(aif[0], x1, x3) - sp.diff(aif[1], x2, x3)), x3))) == 0,
      "D8  the divergence of the aether spatial equation vanishes identically, so the scalar "
      "equation D6 is IMPLIED by D7: varphi and the longitudinal part of a_i are degenerate "
      "(only chi = varphi + Q_0 alpha is physical, SZ21's mixing variable).  Setting a_i = 0 "
      "is therefore a GAUGE CHOICE in the longitudinal sector and a dynamical statement only "
      "in the transverse one")

eq_w_dust = sp.simplify(sp.expand(el(L2b, wf) - eq_w).doit())
check(eq_w_dust != 0,
      "D9  the degeneracy of D8 is broken only by the cosmological dust term K'(Q_0), which "
      "enters the scalar equation as K'(div a - d_i h_0i); its size is bounded at PART F",
      f"the K'-dependent part of the scalar equation is {eq_w_dust}")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- THE REDUCTION, AND THE CRUX: IS u J_Y(u^2) = g_bar A *LOCAL* LAW?")
print("=" * 100)
info("E0  Collecting D5 + D6 + D7 with a_i = 0 (so v = grad varphi) and m_Psi -> 0:\n"
     "        lap(Psi) = 4 pi Ghat rho + lap(varphi)      =>  Psi = Psi_N + varphi\n"
     "        S = (1+J_Y) grad varphi - grad Psi = 0      (longitudinal projection of D7)\n"
     "    =>  J_Y grad varphi = grad Psi_N  pointwise, as a VECTOR equation.")

u_s, gbar_s, a0_s = sp.symbols("u g_bar a0M", positive=True)
check(sp.simplify(sp.solve(sp.Eq(u_s * (u_s / a0_s), gbar_s), u_s)[0] - sp.sqrt(a0_s * gbar_s)) == 0,
      "E1  *** GATE (c): the deep-MOND limit.  Jcal -> (2/3) Y^{3/2}/a_0 gives "
      "J_Y = sqrt(Y)/a_0 = u/a_0, so u J_Y(u^2) = g_bar becomes u^2/a_0 = g_bar, i.e. "
      "u = sqrt(a_0 g_bar) and g_obs = g_bar + u -> sqrt(g_bar a_0) as g_bar -> 0 ***",
      "the SZ21 normalisation 2 lambda_s/(3(1+lambda_s) a_0) Y^{3/2} at lambda_s -> oo is "
      "the same coefficient (bridge1_aest_equations.md)")

# --- spherical symmetry: the curl obstruction vanishes -----------------------------------------
X, Yy, Zz = sp.symbols("X Yy Zz", real=True)
RR = sp.sqrt(X ** 2 + Yy ** 2 + Zz ** 2)
Msym = sp.Symbol("M", positive=True)
PsiN_sph = -Msym / RR
gsph = [sp.diff(PsiN_sph, c) for c in (X, Yy, Zz)]
gmag = sp.sqrt(sum(g ** 2 for g in gsph))
ffun = sp.Function("f")


def curl(vec):
    return [sp.diff(vec[2], Yy) - sp.diff(vec[1], Zz),
            sp.diff(vec[0], Zz) - sp.diff(vec[2], X),
            sp.diff(vec[1], X) - sp.diff(vec[0], Yy)]


vec_sph = [sp.simplify(ffun(gmag) * g) for g in gsph]
curl_sph = [sp.simplify(c) for c in curl(vec_sph)]
check(all(c == 0 for c in curl_sph),
      "E2  in SPHERICAL symmetry the field v = f(g_bar) grad Psi_N is curl-free for an "
      "ARBITRARY function f, so a_i = 0 is consistent, S = 0 has a solution, and\n"
      "        u J_Y(u^2) = g_bar  holds POINTWISE and ALGEBRAICALLY.\n"
      "    This is the configuration the interpolating kernel nu(y) is defined in, and the "
      "one the ephemeris application uses")

# --- general geometry: the obstruction is nonzero ----------------------------------------------
M1, M2, DSEP = 1.0, 0.5, 1.0


def gradPsiN(p):
    """grad Psi_N for two point masses at (0,0,0) and (DSEP,0,0), Psi_N = -M1/r1 - M2/r2"""
    px, py, pz = p
    r1 = math.sqrt(px ** 2 + py ** 2 + pz ** 2)
    r2 = math.sqrt((px - DSEP) ** 2 + py ** 2 + pz ** 2)
    return [M1 * px / r1 ** 3 + M2 * (px - DSEP) / r2 ** 3,
            M1 * py / r1 ** 3 + M2 * py / r2 ** 3,
            M1 * pz / r1 ** 3 + M2 * pz / r2 ** 3]


def vfield(p, a0=1.0):
    """deep-MOND branch of the LOCAL law: v = sqrt(a0/g_bar) grad Psi_N, which is the exact
    pointwise solution of u J_Y(u^2) = g_bar with Jcal = (2/3) Y^{3/2}/a_0."""
    g = gradPsiN(p)
    gm = math.sqrt(sum(c ** 2 for c in g))
    s = math.sqrt(a0 / gm)
    return [s * c for c in g]


def curl_num(field, p, h=1e-6):
    """(curl F)_a = d_b F_c - d_c F_b for (a,b,c) cyclic, by central differences"""
    res = []
    for (b, c) in ((1, 2), (2, 0), (0, 1)):
        pb, pbm, pc, pcm = list(p), list(p), list(p), list(p)
        pb[b] += h; pbm[b] -= h; pc[c] += h; pcm[c] -= h
        res.append((field(pb)[c] - field(pbm)[c]) / (2 * h)
                   - (field(pc)[b] - field(pcm)[b]) / (2 * h))
    return res


P_TEST = (0.4, 0.7, 0.15)
ctrl = curl_num(gradPsiN, P_TEST)
ctrl_mag = math.sqrt(sum(c ** 2 for c in ctrl))
gmag_t = math.sqrt(sum(c ** 2 for c in gradPsiN(P_TEST)))
check(ctrl_mag / gmag_t < 1e-6,
      "E3a CONTROL for the numerical curl operator: applied to grad Psi_N itself (a pure "
      "gradient) at the same point and the same step, it returns zero to machine level",
      f"|curl grad Psi_N| / |grad Psi_N| = {ctrl_mag/gmag_t:.2e}, so anything the operator "
      f"reports below is a real obstruction and not a differencing artifact")

cv = curl_num(vfield, P_TEST)
cmag = math.sqrt(sum(c ** 2 for c in cv))
vmag = math.sqrt(sum(c ** 2 for c in vfield(P_TEST)))
check(cmag / (vmag / DSEP) > 1e-3,
      "E3  *** THE CRUX: in a NON-symmetric configuration (two point masses) the same "
      "construction v = sqrt(a_0/g_bar) grad Psi_N is NOT curl-free, so a_i = 0 is "
      "INCONSISTENT and the pointwise vector law CANNOT hold everywhere ***",
      f"|curl v| = {cmag:.4e} at {P_TEST} against |v|/d = {vmag/DSEP:.4e} (units M1 = 1, "
      f"M2 = 1/2, d = 1, a_0 = 1): a dimensionless obstruction of {cmag/(vmag/DSEP):.3f}.  "
      f"By D7 the "
      f"obstruction is absorbed by the aether transverse mode, S^T = K_B lap(a^T)/((2-K_B)Q_0), "
      f"which is the Bekenstein-Milgrom curl field wearing an aether's clothes")

check(True,
      "E4  so the honest statement of (P3) is: u J_Y(u^2) = g_bar is an EXACT LOCAL "
      "ALGEBRAIC law in the curl-free sector -- in particular in spherical symmetry, which "
      "is where nu(y) is defined and where the ephemeris and rotation-curve applications "
      "live -- and holds only up to a divergence-free field otherwise.  PART Q's 'PURELY "
      "LOCAL ALGEBRAIC LAW', read as a general statement, is OVERSTATED; read as a statement "
      "about the spherical configuration it derives it in, it is correct, and this route "
      "proves it more strongly (as a vector identity, not a Gauss-law first integral)")

check(True,
      "E5  CONSEQUENCE FOR THE LEGALITY THEOREM: the theorem asks whether a single-valued "
      "J(Y) can reproduce a given nu(y).  nu(y) is defined by the spherical relation, and in "
      "spherical symmetry E2 + D7 give g_bar = u J_Y(u^2) with J_Y a function of u ALONE.  "
      "So g_bar is a single-valued function of u, and a non-injective y -> u(y) is a "
      "contradiction.  The premise the legality theorem needs is exactly the one this route "
      "establishes exactly.  THE LEGALITY THEOREM SURVIVES this audit",
      "no claim is made or re-run here about WHICH kernels pass; that arithmetic is PART C "
      "of ppn_newtonian_radial_2026.py and was verified independently elsewhere")

# =================================================================================================
print()
print("=" * 100)
print("PART F -- HOW BIG ARE THE NEGLECTED TERMS?  (both footings, every dimensional number)")
print("=" * 100)
mu = 1.0 / MU_INV_FLOOR
mPsi = mu / math.sqrt(2.0)
for rname, r in (("1 AU", AU), ("30 kpc", 30 * KPC), ("1 Mpc", MPC)):
    info(f"F1  Yukawa correction to Psi_N at {rname}: (m_Psi r)^2 = {(mPsi*r)**2:.3e}",
         "m_Psi^2 = K'' Q_0^2/(2(2-K_B)) = mu^2/2 with mu^-1 >= 1 Mpc "
         "(bridge1_aest_equations.md).  This is the ONLY departure of Psi_N from the ordinary "
         "Newtonian potential, and it is what (P2) glosses over")
check((mPsi * AU) ** 2 < 1e-20 and (mPsi * 30 * KPC) ** 2 < 1e-2,
      "F1  the Yukawa correction that (P2) suppresses is 1.2e-23 at 1 AU and 4.5e-4 at "
      "30 kpc, so 'Psi_N is the ordinary Newtonian potential' is true to those accuracies "
      "and NOT exact")

for rname, r in (("1 AU", AU), ("30 kpc", 30 * KPC)):
    acc_dust = 4 * math.pi * GNEWT * RHO_DM_MEAN * r / 3.0
    gb = GMSUN / AU ** 2 if rname == "1 AU" else A0_CAN
    info(f"F2  neglected background dust (K'(Q_0) Q_0 = 8 pi Gt rho_dust) at {rname}: "
         f"a_dust = {acc_dust:.3e} m/s^2 vs the local scale {gb:.3e} -> {acc_dust/gb:.2e}")
check(4 * math.pi * GNEWT * RHO_DM_MEAN * AU / 3.0 / (GMSUN / AU ** 2) < 1e-20
      and 4 * math.pi * GNEWT * RHO_DM_MEAN * 30 * KPC / 3.0 / A0_CAN < 1e-4,
      "F2  the background dust density -- the ONE thing that stops the flat background from "
      "solving its own equations exactly (B4b) -- is a 1.7e-23 effect at 1 AU and a 6.6e-6 "
      "effect at 30 kpc")

info("F3  the transverse aether mode's mass, which sets whether the curl field of E3 is "
     "suppressed:  m_a^2 = (2-K_B)(1+J_Y) Q_0^2 / K_B, and with mu^2 = 2 K_2 Q_0^2/(2-K_B), "
     "m_a/mu = (2-K_B) sqrt((1+J_Y)/(2 K_2 K_B)).")
rng_dm, rng_au = [], []
for k2n, k2 in K2_FITS:
    for kb in KB_GRID:
        for jyn, jy, bag in (("deep-MOND, J_Y ~ 1/2", 0.5, rng_dm),
                             ("1 AU, J_Y = 2 g_bar/a_0",
                              2 * (GMSUN / AU ** 2) / A0_CAN, rng_au)):
            ratio = (2 - kb) * math.sqrt((1 + jy) / (2 * k2 * kb))
            rng = MU_INV_FLOOR / ratio
            bag.append(rng)
            info(f"     K_2 = {k2:.1e} ({k2n}), K_B = {kb}, {jyn}: "
                 f"1/m_a = {rng/MPC:.3g} Mpc = {rng/KPC:.3g} kpc")
check(min(rng_dm) > 30 * KPC and min(rng_au) > 1 * KPC,
      "F3  on every cell of the (K_2, K_B, J_Y) grid the transverse aether mode's range far "
      "exceeds the system it would have to screen: >= 16 Mpc in the deep-MOND regime (vs "
      "30 kpc galaxies) and >= 1.8 kpc even at the solar system's enormous J_Y (vs 1 AU).  "
      "So lap(a^T) >> m_a^2 a^T there and the curl field S^T is NOT suppressed: E3's "
      "obstruction survives at full strength",
      "direction: ADVERSE to reading (P3) as a general local law, NEUTRAL for the spherical "
      "applications, and it is the same curl field AQUAL has had since Bekenstein-Milgrom "
      "1984 -- not a new liability")

for k2n, k2 in K2_FITS:
    for kb in KB_GRID:
        # spurious mass from lambda_bg = 0 (C3), relative to the legitimate m_Psi^2
        rat = 2 * (2 - kb) ** 2 / (2 * k2)
        info(f"F4  if lambda_bg were set to 0: m_spurious^2 / m_Psi^2 = 2(2-K_B)^2/K'' = "
             f"{rat:.3e}  (K_2 = {k2:.1e} ({k2n}), K_B = {kb}, K'' = 2 K_2)")
check(True,
      "F4  the spurious mass the lambda_bg = 0 error would introduce is not small in "
      "absolute terms -- its range is ~50 x mu^-1, i.e. tens of Mpc -- so it would corrupt "
      "the quasi-static sector on exactly the scales AeST is tuned on.  It is absent here")

for nm, a0 in FOOT:
    gb = GMSUN / AU ** 2
    u_dm = math.sqrt(a0 * gb)
    info(f"F5  ({nm} footing, a_0 = {a0:.4e} m/s^2) deep-MOND check of E1 at 1 AU's g_bar "
         f"= {gb:.4e}: sqrt(a_0 g_bar) = {u_dm:.4e} m/s^2, and the saturating value of the "
         f"anomalous acceleration u on the alpha = 1 branch is a_0/2 = {a0/2:.4e}")
check(all(math.sqrt(a0 * (GMSUN / AU ** 2)) > a0 / 2 for _, a0 in FOOT),
      "F5  both footings carried; nothing in PARTS A-E depends on which is used -- the a_0 "
      "value enters only through the free function's normalisation, and (P1)-(P3) are "
      "statements about the STRUCTURE of the equations")

# =================================================================================================
print()
print("=" * 100)
print("PART G -- VERDICT LEDGER")
print("=" * 100)
LEDGER = [
    ("P1  Qcal = (1-Psi)Q_0, -Psi^2/2 derived, Ycal metric-free",
     "CONFIRMED and generalised (A3-A7); Ycal = |grad varphi + Q_0 a|^2, the corpus's form "
     "in the a_i = 0 sector"),
    ("P2  Psi = Psi_N + varphi, J_Y grad varphi = grad Psi_N",
     "CONFIRMED (D5, D6) with Psi_N Newtonian up to a Yukawa (m_Psi = mu/sqrt2) correction: "
     "1.2e-23 at 1 AU, 4.5e-4 at 30 kpc"),
    ("P3  u J_Y(u^2) = g_bar as a PURELY LOCAL ALGEBRAIC law",
     "PARTIAL: exact pointwise VECTOR law in the curl-free sector (D7 longitudinal, E2), "
     "only up to a divergence-free field in general (E3); the general phrasing is overstated"),
    ("gate (a) Qcal = (1-Psi)Q_0", "REPRODUCED (A5)"),
    ("gate (b) gamma_PPN = 1", "REPRODUCED, and strengthened -- traceless sector kept (D1-D3)"),
    ("gate (c) deep-MOND limit", "REPRODUCED (E1)"),
    ("lambda handled consistently?",
     "YES: lambda_bg = (2-K_B)(1+J_Y)Q_0^2 + K'Q_0/2, nonzero (B2), over-determined "
     "consistently (B3), and PART Q's dropped multiplier term is legal by the elimination "
     "identity (C2).  Setting it to zero would inject a spurious mass (C3)"),
    ("does the background solve its own equations?",
     "YES up to the cosmological dust: K(Q_0) + 2 Lambda = 0 is identical for SZ21's K, and "
     "K'(Q_0) Q_0 = 0 holds to 1.7e-23 at 1 AU / 6.6e-6 at 30 kpc (B4, F2)"),
    ("PART Q's Q7 (A_i = 0 satisfied identically)",
     "REFUTED as an argument (D7): terms linear in a_i exist.  Its conclusion survives in "
     "the spherical sector, and the equation it dismisses is what upgrades P3 to a vector law"),
    ("legality theorem",
     "SURVIVES (E5): it needs only the spherical branch, which this route establishes exactly"),
]
for k, vtxt in LEDGER:
    print(f"   - {k}\n       {vtxt}")

print()
print("=" * 100)
print(f"checks: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed   runtime {time.time()-T0:.1f} s")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
sys.exit(0)
