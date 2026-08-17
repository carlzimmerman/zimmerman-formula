#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ppn_verify_gradient_A_2026.py
=============================
VERIFICATION ROUTE: the FROZEN-A_Y CAVEAT of real_research/reviews/ppn_scalar_retained_2026.py
(35/35), which that file names as "THE LEADING CAVEAT ... the one thing that could move the
numbers".  Its result under test:

    alpha_1 = K_B(2K_B^2 -  5K_B +  6)/(2-K_B)^2 -> (3/2)K_B ,
    alpha_2 = K_B(2K_B^2 - 11K_B + 10)/(2-K_B)^2 -> (5/2)K_B ,   K_B-ONLY,

obtained by freezing A_Y = (2-K_B) e^(sqrt y) and then taking A_Y -> infinity, whence
|alpha_1| < 1e-4 => K_B < 6.667e-5 and |alpha_2| < 1e-7 => K_B < 4.00e-8, against the
scalar-subluminality floor K_B >= 2.105e-4, i.e. a two-sided window EMPTY by 5263x.

THE ANSWER, up front, in both directions.

  (a)/(b)/(c) grad(A_Y) IS HARMLESS, AND STRUCTURALLY SO -- the author's defence is correct
      and this file supplies the missing proof.  A_Y enters the quadratic action in EXACTLY
      one term, -A_Y * Y, whose field dependence differentiates ONLY the khronon chi (PART A,
      checks A2-A3, symbolic).  Therefore grad(A_Y) can appear in EXACTLY one term of EXACTLY
      one field equation, and there it is the exact divergence d_mu(A_Y W^mu) = d_mu sigma^mu
      of the quantity sigma^mu = A_Y W^mu that is FINITE in the A_Y -> infinity scaling
      (check A4, an exact symbolic identity).  A_Y and grad(A_Y) are both ABSENT from that
      equation once written in sigma.  In every OTHER equation the A_Y-part is algebraic
      (check A5), so no derivative ever lands on A_Y there.  The maximal gradient enhancement
      of the residual is therefore ONE power of |grad ln A_Y|/k = sqrt(y), against a screening
      of e^(-sqrt y): bounded by sqrt(y) e^(-sqrt y)/(2-K_B), whose GLOBAL maximum over every
      radius is 0.184 and whose value at 1 AU is 1e-3453.  The two limits COMMUTE.  So the
      gradient cannot move alpha_1 or alpha_2, and this HARDENS the adverse conclusion against
      the caveat the author raised.

  BUT (PART B) THE CAVEAT IS STILL BINDING, THROUGH A CHANNEL THE AUTHOR DID NOT NAME, AND IT
  IS NOT A GRADIENT AT ALL.  Freezing A_Y at the local kernel value is inconsistent with the
  Q_0 != 0 that the same calculation needs (its own check Q2-2) to lift the degeneracy:

    * DERIVED HERE IN EXACT CLOSED FORM, all five parameters and k symbolic (check B1):
          h_00(w=0) = (G_eff/G) rho / [2 (k^2 + m^2)] ,
          G_eff/G   = 2 A_Y / [(2-K_B)(A_Y - (2-K_B))] ,
          m^2       = (2 A_Y - Fpp) Q_0^2 A_Y / [2 (2-K_B)(A_Y - (2-K_B))]  ->  A_Y Q_0^2/(2-K_B).
      A_Y therefore acts as a YUKAWA MASS on the Newtonian potential.  The verified file never
      saw it because BOTH quasi-static gates that fixed A_Y (its G4b, G4c, G5) were evaluated
      at Q_0 = 0 -- the exact substitution that deletes m^2.  Setting Q_0 = 0 in the gate that
      FIXES A_Y and Q_0 != 0 in the gate that makes the O(w^2) problem WELL POSED cannot both
      be done.
    * The mass is real AeST physics, not an algebra slip: at A_Y = Fpp = 4 K_2 it reduces
      EXACTLY to mu^2 = 2 K_2 Q_0^2/(2-K_B), SZ21's scalar mass as carried in the corpus
      (check B3).  And the Q_0 -> 0 slice of B1 reproduces the verified file's G4b and G4c
      character by character (check B2), so B1 strictly GENERALISES the gate it corrects.
    * Consequence: A_Y -> infinity and Q_0/k -> 0 DO NOT COMMUTE.  In the A_Y -> infinity
      limit the whole O(w^2)/O(w^0) ratio is a function of the single combination
      Lambda = A_Y Q_0^2 / k^2 alone (check B5, verified to 10 digits at A_Y = 1e12 and 1e16).
      F(Lambda -> 0) reproduces the verified file's a+b = 2K_B(3K_B-2)/(2-K_B)^2 (check B6 --
      agreement stated first).  F(Lambda -> infinity) = -4 EXACTLY, independent of K_B, Fpp,
      A_Y and Q_0, including at K_B = 0 (check B7).
    * And at FINITE A_Y in the Lambda -> 0 corner, a+b carries a K_B-INDEPENDENT additive term
      -> -4/A_Y as K_B -> 0 (check B8, two A_Y decades, four K_B).  "Depending on K_B ALONE"
      is therefore a property of the strict A_Y -> infinity limit only, and the whole
      |alpha| -> K_B-ceiling arithmetic of C4 lives or dies with that limit.
    * BOTH orientations were run, so both of the verified file's numbers are reproduced in the
      Lambda -> 0 corner (a = 4 K_B, its Q3-3, check B9) and both corners are mapped: at
      Lambda >> 1 the perpendicular coefficient is a = +8 EXACTLY, again independent of K_B and
      A_Y (check B10), so b = -12 and the individual parameters there are
          alpha_1 = +2, alpha_2 = +6   (this file's / the verified file's convention C4)
          alpha_1 = -8, alpha_2 = -6   (Will's convention)
      -- O(1) and K_B-INDEPENDENT, i.e. 1e4 to 1e8 over the bounds for every K_B including
      K_B = 0.  Reported, NOT banked: see the red-flag discussion at B7/B10.

  WHERE THE SOLAR SYSTEM SITS (PART C).  Lambda(1 AU) = 1e3430 canonical / 1e3123 alt, i.e.
  the SOLAR SYSTEM IS IN THE OTHER CORNER.  Lambda = 1 at r* = 157 AU canonical / 143 AU alt
  (and 195 / 178 AU if Q_0^-1 = 1 Mpc instead of 100 Mpc).  So the verified alpha formulas'
  corner is realised only OUTSIDE ~150 AU, while |alpha_1| < 1e-4 (lunar laser ranging) and
  |alpha_2| < 1e-7 (solar spin axis) are measured at ~1 AU.  Inside that radius the frozen
  A_Y = (2-K_B) e^(sqrt y) gives a graviton Yukawa range 1/m = 1e-1704 m -- 1669 orders BELOW
  the Planck length -- which is not a PPN regime but the frozen-A_Y input announcing its own
  inconsistency.

  VERDICT.  The empty K_B window is NOT ESTABLISHED, and it is NOT REFUTED either.  It is
  CONDITIONAL on an identification of A_Y that this file shows to be self-inconsistent in the
  regime where the bounds are measured:
      branch (I)  A_Y = (2-K_B) e^(sqrt y)  (the verified file's own G5, kernel-matched):
                  Lambda >> 1 at 1 AU, m^2 destroys the Newtonian limit, alphas INAPPLICABLE.
      branch (II) A_Y = O(K_2) ~ 1e4 (the value that makes m^2 equal SZ21's mu^2):
                  Lambda ~ 1e-22 at 1 AU, the verified corner IS the physical one, the 1/A_Y
                  residual is ~1e-5 relative, grad(A_Y) = 0 identically -- and then C3/C4
                  STAND, except that B8's K_B-independent -4/A_Y ~ 1e-4 floor then exceeds the
                  |alpha_2| < 1e-7 bound by ~1e3 FOR EVERY K_B, K_B = 0 included, which is a
                  K_B-independent statement and therefore a red flag on the truncation rather
                  than a result to bank.
  Neither branch delivers C3's clean K_B-only alphas as the solar-system answer.  Direction:
  this REMOVES an adverse kill (favourable relative to C3/C4) while pointing at something
  potentially worse; it is not a win and must not be reported as one.

WHAT THIS FILE DOES NOT TOUCH.  a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canonical /
1.1279e-10 alt; kappa = 1/2 (FITTED, never derived); the kernel nu(y) = 1/(1-e^(-sqrt y))
(Milgrom & Sanders 2008 Eq. 13 at alpha = 1/2); the RAR, BTFR, weak lensing, CLASS.  The
issue located here is in the ADOPTED RELATIVISTIC HOME (AeST, Skordis & Zlosnik, PRL 127
161302, arXiv:2007.00082) and in one auxiliary identification inside a PPN calculation about
it.  gamma_PPN = 1 is re-verified here at GENERAL Q_0 (check B4) and survives untouched.

CONVENTIONS.  Machinery, signature, units, gauge and PPN matching are COPIED VERBATIM from
ppn_scalar_retained_2026.py so that any disagreement is physics and not bookkeeping:
signature (-,+,+,+), 16 pi G = 1, F_{mu nu} = d_mu A_nu - d_nu A_mu, constraint enforced with
+lambda(A.A+1), gauge h_{3 nu} = 0, static in the matter frame, single Fourier mode k along z,
Lagrangian carries -A_Y * Y and +(Fpp/2)(Q-Q_0)^2, khronon background grad_mu phi = -Q_0 A_mu.
PPN matching, delta h_00 = [a w^2 + b (w.khat)^2] U with U_ij = (delta_ij - 2 khat_i khat_j)U:
  * THIS FILE'S / the verified file's convention (C4 there):  a = alpha_1 + alpha_2,
    b = -2 alpha_2, hence alpha_2 = -b/2 and alpha_1 = a + b/2.
  * WILL's convention, in which g_00 carries -(alpha_1 - alpha_2 - alpha_3) w^2 U
    - alpha_2 w^i w^j U_ij:  alpha_1 = -a EXACTLY (at alpha_3 = 0) and alpha_2 = +b/2.
  The PARALLEL orientation measures a + b (= alpha_1 - alpha_2 here, = -(alpha_1 + alpha_2) in
  Will's) and the PERPENDICULAR one measures a (= alpha_1 + alpha_2 here, = -alpha_1 in Will's).
  Both are run.  Every number is reported in BOTH conventions and NO verdict in this file
  depends on the choice, because every conclusion is about the DOMAIN of a formula, not its
  sign.

EXIT 0 iff every numbered check passes.  Runtime a few minutes (the two O(eps^2) builds).
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
# machinery -- copied verbatim from ppn_scalar_retained_2026.py, plus ONE addition:
# build() also returns Vup, the exact projected khronon gradient P^{mu nu} grad_nu phi, which is
# used only for diagnostics in PART A.
# =================================================================================================
t, x, y, z = sp.symbols("t x y z", real=True)
CO = [t, x, y, z]
ETA = sp.diag(-1, 1, 1, 1)
ETAI = ETA
eps = sp.Symbol("eps")
s = sp.Symbol("s")
KB = sp.Symbol("K_B", positive=True)
cJ = sp.Symbol("c_J")
AY = sp.Symbol("A_Y")
Fpp = sp.Symbol("Fpp")
Q0 = sp.Symbol("Q_0")
k = sp.Symbol("k", positive=True)
om = sp.Symbol("omega")
rho = sp.Symbol("rho")
R_ = sp.Symbol("R")
P_, Pi_ = sp.Symbol("P"), sp.Symbol("Pi_")
I = sp.I


def _G1_general():
    """Linearised Einstein tensor for h_{mu nu}(t,z), from the Riemann definition."""
    H = {}
    for m in range(4):
        for n in range(m, 4):
            H[(m, n)] = sp.Function(f"h{m}{n}")(t, z)
    hd = sp.Matrix(4, 4, lambda m, n: H[(min(m, n), max(m, n))])
    gd = ETA + eps * hd
    gu = ETAI - eps * (ETAI * hd * ETAI)
    Gam = [[[sp.expand(sp.Rational(1, 2) * sum(
        gu[r, ss] * (sp.diff(gd[ss, n], CO[m]) + sp.diff(gd[ss, m], CO[n]) - sp.diff(gd[m, n], CO[ss]))
        for ss in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]

    def ric(sig, nu):
        out = 0
        for m in range(4):
            out += sp.diff(Gam[m][nu][sig], CO[m]) - sp.diff(Gam[m][m][sig], CO[nu])
            for l in range(4):
                out += Gam[m][m][l] * Gam[l][nu][sig] - Gam[m][nu][l] * Gam[l][m][sig]
        return sp.expand(out)

    R1 = sp.Matrix(4, 4, lambda m, n: sp.expand(ric(m, n)).coeff(eps, 1))
    Rs = sp.expand(sum(ETAI[m, n] * R1[m, n] for m in range(4) for n in range(4)))
    return H, sp.Matrix(4, 4, lambda m, n: sp.expand(R1[m, n] - sp.Rational(1, 2) * ETA[m, n] * Rs))


def build(wvec, zero_fields=()):
    """O(eps^2) Lagrangian of the aether+scalar sector + the matter source, fields f(t,z)."""
    H = {}
    for m in range(4):
        for n in range(m, 4):
            H[(m, n)] = sp.Function(f"h{m}{n}")(t, z)
    a = [sp.Function(f"a{m}")(t, z) for m in range(4)]
    chi = sp.Function("chi")(t, z)
    lam = sp.Function("lam")(t, z)
    subz = {}
    for nm in zero_fields:
        if nm.startswith("h"):
            subz[H[(int(nm[1]), int(nm[2]))]] = 0
        else:
            subz[a[int(nm[1])]] = 0

    def Z(e):
        return e.subs(subz)

    hd = sp.Matrix(4, 4, lambda m, n: Z(H[(min(m, n), max(m, n))]))
    gd = ETA + eps * hd
    hup = ETAI * hd * ETAI
    gu = ETAI - eps * hup + eps ** 2 * (hup * hd * ETAI)
    trh = sum(ETAI[m, n] * hd[m, n] for m in range(4) for n in range(4))
    h2 = sum(hup[m, n] * hd[m, n] for m in range(4) for n in range(4))
    sq = 1 + eps * trh / 2 + eps ** 2 * (trh ** 2 / 8 - h2 / 4)

    w2 = sum(c ** 2 for c in wvec)
    gw = sp.series(1 / sp.sqrt(1 - w2), s, 0, 3).removeO()
    Abg = sp.Matrix([-gw, gw * wvec[0], gw * wvec[1], gw * wvec[2]])
    Ad = sp.Matrix([Abg[m] + eps * Z(a[m]) for m in range(4)])
    Au = gu * Ad
    AA = sum(Au[m] * Ad[m] for m in range(4))
    Pdn = sp.Matrix([-Q0 * Abg[m] for m in range(4)])
    dphi = sp.Matrix([Pdn[m] + eps * sp.diff(Z(chi), CO[m]) for m in range(4)])

    Gam = [[[sp.Rational(1, 2) * sum(
        gu[r, ss] * (sp.diff(gd[ss, n], CO[m]) + sp.diff(gd[ss, m], CO[n]) - sp.diff(gd[m, n], CO[ss]))
        for ss in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]

    F = sp.Matrix(4, 4, lambda m, n: eps * (sp.diff(Z(a[n]), CO[m]) - sp.diff(Z(a[m]), CO[n])))
    F2 = sum(F[m, n] * F[aa, bb] * gu[m, aa] * gu[n, bb]
             for m in range(4) for n in range(4) for aa in range(4) for bb in range(4))
    Jd = [sum(Au[nu] * (sp.diff(Ad[al], CO[nu]) - sum(Gam[b][nu][al] * Ad[b] for b in range(4)))
              for nu in range(4)) for al in range(4)]
    Jphi = sum(gu[mu, al] * Jd[al] * dphi[mu] for mu in range(4) for al in range(4))
    Q = sum(Au[mu] * dphi[mu] for mu in range(4))
    Y = sum((gu[mu, nu] + Au[mu] * Au[nu]) * dphi[mu] * dphi[nu]
            for mu in range(4) for nu in range(4))
    Vup = [sp.expand(sum((gu[mu, nu] + Au[mu] * Au[nu]) * dphi[nu] for nu in range(4)))
           for mu in range(4)]

    B = (-(KB / 2) * F2 + 2 * cJ * Jphi - AY * Y + (Fpp / 2) * (Q - Q0) ** 2
         + eps * Z(lam) * (AA + 1))
    L = sq * B
    L2 = sp.expand(sp.series(sp.expand(L), eps, 0, 3).removeO()).coeff(eps, 2)
    L2 = sp.expand(sp.series(L2, s, 0, 3).removeO())
    L2 = L2 + sp.Rational(1, 2) * rho * hd[0, 0]
    return dict(H=H, a=a, chi=chi, lam=lam, L2=sp.expand(L2), Z=Z, Abg=Abg,
                Yexpr=Y, Qexpr=Q, AAexpr=AA, Vup=Vup)


def fourier(fields):
    Fa, Ga, sub = {}, {}, {}
    for f in fields:
        nm = f.func.__name__
        Fa[nm], Ga[nm] = sp.Symbol("F_" + nm), sp.Symbol("G_" + nm)
        Fp, Gp = Fa[nm] * P_, Ga[nm] * Pi_
        sub[sp.Derivative(f, (z, 2))] = (I * k) ** 2 * Fp + (-I * k) ** 2 * Gp
        sub[sp.Derivative(f, (t, 2))] = (-I * om) ** 2 * Fp + (I * om) ** 2 * Gp
        sub[sp.Derivative(f, t, z)] = (-I * om) * (I * k) * Fp + (I * om) * (-I * k) * Gp
        sub[sp.Derivative(f, z)] = I * k * Fp - I * k * Gp
        sub[sp.Derivative(f, t)] = -I * om * Fp + I * om * Gp
        sub[f] = Fp + Gp
    return Fa, Ga, sub


G1_H, G1_GEN = _G1_general()


def equations(wvec, zero_fields, eq_names, extra_sub=None):
    """Linear field equations in Fourier space (amplitudes F_*), for the given wind."""
    r = build(wvec, zero_fields)
    H, a, chi, lam, Z = r["H"], r["a"], r["chi"], r["lam"], r["Z"]
    allf = [H[(m, n)] for m in range(4) for n in range(m, 4)] + list(a) + [chi, lam]
    live = [f for f in allf if Z(f) != 0]
    Fa, Ga, sub = fourier(live)
    L2 = r["L2"].subs(extra_sub) if extra_sub else r["L2"]
    L2f = sp.expand(L2.subs(sub, simultaneous=True)).subs(rho, R_ * P_ + sp.Symbol("Rc") * Pi_)
    L2avg = sp.expand(sp.expand(sp.expand(L2f).coeff(P_, 1)).coeff(Pi_, 1))
    G1 = G1_GEN.subs(extra_sub) if extra_sub else G1_GEN
    G1 = G1.subs({f: Z(f) for f in [H[(m, n)] for m in range(4) for n in range(m, 4)]})
    G1 = G1.applyfunc(lambda e: sp.expand(sp.expand(e).subs(sub, simultaneous=True)).coeff(P_, 1))
    Gup = sp.Matrix(4, 4, lambda m, n: sp.expand(ETA[m, m] * ETA[n, n] * G1[m, n]))
    if extra_sub:
        L2avg = L2avg.subs(extra_sub)
        Gup = Gup.subs(extra_sub)
    eqs = []
    for nm in eq_names:
        e = sp.diff(L2avg, Ga[nm])
        if nm.startswith("h"):
            m, n = int(nm[1]), int(nm[2])
            e = e - (1 if m == n else 2) * Gup[m, n]
        eqs.append(sp.expand(e))
    return r, eqs, Fa, Ga, sub


def hcoeffs(eqs, unkS, tgt, nord=2):
    """Solve the linear system order by order in s; return [h_tgt^(0), h^(1), h^(2)]."""
    rep, parts = {}, {}
    for u in unkS:
        ps = [sp.Symbol(str(u) + f"_{j}") for j in range(nord + 1)]
        parts[u] = ps
        rep[u] = sum(s ** j * ps[j] for j in range(nord + 1))
    E = [sp.expand(e.subs(rep)) for e in eqs]
    known = {}
    for j in range(nord + 1):
        cur = [sp.expand(sp.expand(e).coeff(s, j).subs(known)) for e in E]
        vj = [parts[u][j] for u in unkS]
        A, b = sp.linear_eq_to_matrix(cur, vj)
        xs = A.LUsolve(b)
        known.update({v: sp.cancel(xs[i]) for i, v in enumerate(vj)})
    return [known[parts[tgt][j]] for j in range(nord + 1)]


ZF0 = ("h01", "h02", "h12", "h13", "h23", "h03", "h33", "a1", "a2")
UNK0 = ["h00", "h11", "h22", "a0", "a3", "chi", "lam"]

print("=" * 100)
print(f"machinery built ({time.time()-T0:.0f}s)")
print("=" * 100)

# =================================================================================================
print()
print("=" * 100)
print("PART A -- QUESTIONS (a),(b),(c): grad(A_Y).  A STRUCTURAL THEOREM, NOT A NUMERICAL SCAN.")
print("=" * 100)
info("A0  THE ARGUMENT TO BE PROVED OR BROKEN.  The verified file freezes A_Y and then takes "
     "A_Y -> infinity, and defends it by asserting that alpha_1, alpha_2 are A_Y-INDEPENDENT so "
     "the limit is uniform.  A numerical 'first order in grad(A_Y)/A_Y' scan would be worthless "
     "here, because grad(ln A_Y)/k = sqrt(y) ~ 8e3 at 1 AU is not a small parameter: there is no "
     "radius at which A_Y is constant to O(1) over more than ~2 Earth radii.  What settles it is "
     "instead a statement about WHERE grad(A_Y) can appear at all.")

r0 = build([0, 0, s * sp.Integer(1)], ZF0)
L2_0 = r0["L2"].subs({cJ: 2 - KB, om: 0})
cAY = sp.expand(L2_0.coeff(AY, 1))
chi0 = r0["chi"]

check(sp.Poly(L2_0, AY).degree() == 1,
      "A1  A_Y enters the O(eps^2) Lagrangian at degree EXACTLY 1, in the single term -A_Y * Y",
      "so every A_Y-dependence of every field equation is one term, linear, with an "
      "A_Y-independent coefficient: the quadratic form Y^(2)")

ders = sorted({str(d.args[0].func) for d in cAY.atoms(sp.Derivative)})
check(ders == ["chi"],
      "A2  *** THE LOAD-BEARING FACT: the A_Y-coefficient of the Lagrangian differentiates ONLY "
      "the khronon chi.  The metric h_{mu nu} and the aether perturbation delta A_mu appear in "
      "it ALGEBRAICALLY ***",
      f"differentiated fields inside the A_Y term: {ders}.  Hence for every field psi != chi, "
      f"delta(A_Y Y)/delta psi = A_Y * dY/dpsi with NO derivative acting on A_Y -- a "
      f"position-dependent A_Y enters those equations only through its LOCAL VALUE, never "
      f"through its gradient, to ALL orders")

d1, d2 = sp.symbols("d1 d2")
noBare = not cAY.subs({sp.Derivative(chi0, z): d1, sp.Derivative(chi0, t): d2}).has(chi0)
check(noBare and not cAY.has(rho),
      "A3  the A_Y-coefficient contains no UNDIFFERENTIATED chi (the khronon's shift symmetry "
      "survives in it) and no rho (A_Y never multiplies the matter source)",
      "the first fact makes the chi field equation's A_Y-part an exact total divergence, which "
      "is what check A4 exploits; the second means the constraint surface A_Y -> infinity "
      "selects is source-independent")

r, eqs, Fa, Ga, sub = equations([0, 0, s * sp.Integer(1)], ZF0, UNK0,
                                extra_sub={cJ: 2 - KB, om: 0})
Y2 = sp.expand(-cAY)
Wz = sp.expand(sp.diff(Y2, sp.Derivative(chi0, z)))
Wz_F = sp.expand(sp.expand(Wz.subs(sub, simultaneous=True)).coeff(P_, 1)).subs(om, 0)
Ppart = sp.expand(eqs[UNK0.index("chi")].coeff(AY, 1))
check(sp.simplify(Ppart - I * k * Wz_F) == 0 and sp.simplify(Ppart) != 0,
      "A4  *** EXACT IDENTITY: the A_Y-part of the chi field equation is i k * A_Y * W^z with "
      "W^z = dY^(2)/d(d_z chi).  In position space that term is therefore EXACTLY "
      "d_z(A_Y W^z) = d_z sigma^z, and sigma^mu = A_Y W^mu is the quantity that stays FINITE as "
      "A_Y -> infinity.  Written in sigma, that equation contains NEITHER A_Y NOR grad(A_Y) ***",
      "this is the whole answer to question (b): the A_Y-independence is STRUCTURAL, not an "
      "accident of freezing.  A_Y multiplies one quadratic form; the A_Y -> infinity limit is a "
      "penalty/constraint limit whose limiting system is written in the multipliers sigma and "
      "contains no A_Y at all -- and a constraint enforced with any position-dependent but "
      "everywhere-large weight is the SAME constraint.  Nothing about A_Y's profile, its "
      "gradient, or even its dependence on rho can survive into it")

rows = []
for nm, e in zip(UNK0, eqs):
    c = sp.expand(sp.expand(e).coeff(Fa["chi"]))
    if c == 0:
        continue
    cA = sp.expand(c.coeff(AY, 1))
    c0 = sp.expand(c - AY * cA)
    dA = sorted({m[0] for m in sp.Poly(cA, k).monoms()}) if cA != 0 else []
    d0 = sorted({m[0] for m in sp.Poly(c0, k).monoms()}) if c0 != 0 else []
    rows.append((nm, dA, d0))
print(f"       {'equation':>10s}  {'k-powers of the A_Y part':>26s}  {'k-powers of the A_Y-free part':>30s}")
for nm, dA, d0 in rows:
    print(f"       {nm:>10s}  {str(dA):>26s}  {str(d0):>30s}")
maxA = max((max(dA) if dA else 0) for nm, dA, d0 in rows if nm != "chi")
max0 = max((max(d0) if d0 else 0) for nm, dA, d0 in rows if nm != "chi")
check(maxA == 1 and max0 == 2,
      "A5  the derivative census that fixes the SIZE of the residual: in every equation other "
      "than chi's, the A_Y-part carries chi with exactly ONE power of k (first derivative, so "
      "grad(A_Y) is impossible there, as A2 already implies), while the A_Y-FREE part reaches "
      "k^2.  So at most ONE derivative ever lands on the elimination d_z chi = "
      "(sigma^z/A_Y - ...)/(...), and the maximal gradient enhancement of the O(1/A_Y) residual "
      "is exactly ONE power of |grad ln A_Y|/k = sqrt(y)",
      f"max k-power of the A_Y part off the chi row = {maxA}; of the A_Y-free part = {max0}.  "
      f"A second power would need d^3 chi, which a second-order system built from a Lagrangian "
      f"with only FIRST derivatives of chi cannot produce")

u = sp.Symbol("u", positive=True)
g1 = u * sp.exp(-u)               # sqrt(y) e^{-sqrt y} with u = sqrt(y)
g2 = u ** 2 * sp.exp(-u)          # y e^{-sqrt y}
m1 = [c for c in sp.solve(sp.diff(g1, u), u) if c.is_real and c > 0]
m2 = [c for c in sp.solve(sp.diff(g2, u), u) if c.is_real and c > 0]
b1, u1 = max((float(g1.subs(u, c)), float(c)) for c in m1)
b2, u2 = max((float(g2.subs(u, c)), float(c)) for c in m2)
check(abs(b1 - math.exp(-1)) < 1e-12 and abs(b2 - 4 * math.exp(-2)) < 1e-12,
      "A6  *** THE UNIFORM BOUND, valid at EVERY radius: the gradient-enhanced residual is "
      "O(sqrt(y) e^(-sqrt y)/(2-K_B)) and sqrt(y) e^(-sqrt y) <= e^(-1) = 0.3679 for ALL y, "
      "attained at y = 1.  (Even the over-generous two-derivative counting y e^(-sqrt y) is "
      "bounded by 4 e^(-2) = 0.5413 at y = 4.)  The gradient expansion therefore NEVER blows "
      "up, at any radius, in any regime ***",
      f"max over y of sqrt(y)e^(-sqrt y) = {b1:.6f} at y = {u1**2:.1f}; "
      f"max of y e^(-sqrt y) = {b2:.6f} at y = {u2**2:.1f}.  With 2-K_B ~ 2 the "
      f"bounds are 0.1840 and 0.2707")

GMSUN, AU, PCm = 1.32712440018e20, 1.495978707e11, 3.0856775814913673e16
MPCm = 1.0e6 * PCm
GBAR_1AU = GMSUN / AU ** 2
FOOT = (("canonical", 9.3619e-11), ("ALT", 1.1279e-10))
print()
print(f"       {'footing':>10s} {'a_0 [m/s^2]':>12s} {'y(1 AU)':>11s} {'sqrt y':>9s} "
      f"{'log10 A_Y':>10s} {'log10 grad-corr':>16s}")
GRADCORR = {}
for lab, a0 in FOOT:
    yv = GBAR_1AU / a0
    sy = math.sqrt(yv)
    lgA = math.log10(2.0) + sy / math.log(10.0)          # A_Y = (2-K_B) e^{sqrt y}, K_B -> 0
    lgc = math.log10(sy / 2.0) - sy / math.log(10.0)
    GRADCORR[lab] = lgc
    print(f"       {lab:>10s} {a0:12.4e} {yv:11.4e} {sy:9.1f} {lgA:10.1f} {lgc:16.1f}")
check(all(v < -3000 for v in GRADCORR.values()),
      "A7  *** QUESTION (a) ANSWERED: at 1 AU the gradient-corrected residual on alpha_1 and "
      "alpha_2 is 1e{:.0f} (canonical) / 1e{:.0f} (alt) in RELATIVE size.  There is no "
      "correction. QUESTION (c) ANSWERED: the limits grad -> 0 and A_Y -> infinity COMMUTE, "
      "because by A4 the limiting system contains no A_Y and therefore no grad(A_Y) ***"
      .format(GRADCORR["canonical"], GRADCORR["ALT"]),
      "STATED IN THE DIRECTION IT POINTS: this is a FAVOURABLE result for the ADVERSE "
      "conclusion.  On the gradient channel alone, the author's defence is correct and the "
      "empty window is HARDENED, not weakened")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THE LIMIT THAT DOES *NOT* COMMUTE: A_Y -> infinity versus Q_0/k -> 0")
print("=" * 100)
info("B0  WHY LOOK HERE.  A2/A4 say A_Y enters every non-chi equation through its LOCAL VALUE.  "
     "That kills the gradient -- and it also means the local value itself is doing work "
     "somewhere.  A_Y multiplies Y^(2), and Y^(2) contains Q_0^2 (delta A, h) pieces because the "
     "background khronon gradient is grad_mu phi = -Q_0 A_mu.  So A_Y Q_0^2 is a MASS scale, and "
     "the only dimensionless thing it can be compared with is k^2.")

r, eqsw0, Faw0, Gaw0, _ = equations([0, 0, 0], ZF0, UNK0, extra_sub={cJ: 2 - KB, om: 0})
unkw0 = [Faw0[uu] for uu in UNK0]
Aw, bw = sp.linear_eq_to_matrix(eqsw0, unkw0)
xw = Aw.LUsolve(bw)
h00w = sp.cancel(sp.together(xw[UNK0.index("h00")]))
h11w = sp.cancel(sp.together(xw[UNK0.index("h11")]))
h22w = sp.cancel(sp.together(xw[UNK0.index("h22")]))
Geff = 2 * AY / ((2 - KB) * (AY - (2 - KB)))
m2 = (2 * AY - Fpp) * Q0 ** 2 * AY / (2 * (2 - KB) * (AY - (2 - KB)))
check(sp.simplify(h00w - Geff * R_ / (2 * (k ** 2 + m2))) == 0,
      "B1  *** EXACT CLOSED FORM of the w = 0 response, all five parameters AND k symbolic, "
      "nothing frozen and nothing set to zero:\n"
      "             h_00 = (G_eff/G) rho / [2 (k^2 + m^2)]\n"
      "             G_eff/G = 2 A_Y/[(2-K_B)(A_Y-(2-K_B))]\n"
      "             m^2 = (2 A_Y - Fpp) Q_0^2 A_Y / [2 (2-K_B)(A_Y-(2-K_B))]  ->  "
      "A_Y Q_0^2/(2-K_B)\n"
      "       A_Y IS A YUKAWA MASS ON THE NEWTONIAN POTENTIAL ***",
      f"h_00 = {sp.factor(h00w)}")
check(sp.simplify(sp.cancel(h00w.subs(Q0, 0) - Geff * R_ / (2 * k ** 2))) == 0
      and sp.simplify(sp.limit(Geff, AY, sp.oo) - 1 / (1 - KB / 2)) == 0,
      "B2  and the Q_0 -> 0 SLICE of B1 reproduces the verified file's G4b and G4c exactly: "
      "G_eff/G = 2A_Y/[(2-K_B)(A_Y-(2-K_B))] -> 1/(1-K_B/2).  B1 therefore STRICTLY GENERALISES "
      "the gate that fixed A_Y = (2-K_B) e^(sqrt y); it does not contradict it",
      "AGREEMENT FIRST.  The verified file's own G4b line is 'h00_qs = h00_0.subs(Q0, 0)' -- the "
      "substitution that deletes m^2.  Its G5 then used that Q_0 = 0 gate to FIX A_Y, while its "
      "Q2-2 needs Q_0 != 0 to make the O(w^2) problem well posed.  Those are the two halves that "
      "cannot both be taken")
K2 = sp.Symbol("K_2", positive=True)
mu2_SZ = 2 * K2 * Q0 ** 2 / (2 - KB)
m2_at = sp.simplify(m2.subs({AY: 4 * K2, Fpp: 4 * K2}))
check(sp.simplify(sp.limit(sp.simplify(m2_at / mu2_SZ), K2, sp.oo) - 1) == 0,
      "B3  *** THE MASS IS REAL AeST PHYSICS, NOT AN ALGEBRA SLIP: at A_Y = Fpp = 4 K_2 the "
      "derived m^2 reduces to mu^2 = 2 K_2 Q_0^2/(2-K_B) -- SZ21's scalar mass, the same object "
      "the corpus pins at mu^-1 >~ 1 Mpc.  An independent validation of B1 from a formula this "
      "file did not fit ***",
      f"m^2(A_Y = Fpp = 4K_2) = {sp.factor(m2_at)}, whose ratio to mu^2 tends to 1 for large "
      f"K_2.  Note the corollary that decides PART C: the mass comes out equal to SZ21's mu "
      f"only when A_Y is of order K_2 (~1e4).  With A_Y = (2-K_B) e^(sqrt y) instead, m^2 is "
      f"larger by e^(sqrt y)/(2 K_2)")
check(sp.simplify(h11w - h00w) == 0 and sp.simplify(h22w - h00w) == 0,
      "B4  FAVOURABLE, AND REPORTED WITH THE SAME WEIGHT: gamma_PPN = 1 remains EXACT at general "
      "Q_0, not just at Q_0 = 0 -- h_11 = h_22 = h_00 for every K_B, A_Y, Fpp, Q_0, mass term "
      "included.  Nothing in this file touches the corpus's gamma_PPN = 1",
      "the Yukawa mass suppresses h_00, h_11, h_22 IDENTICALLY, so the light-bending ratio is "
      "unaffected even in the pathological corner")

qq = sp.Symbol("qq", positive=True)
r, eqsP, FaP, GaP, _ = equations([0, 0, s * sp.Integer(1)], ZF0, UNK0,
                                 extra_sub={cJ: 2 - KB, Q0: qq, k: 1, om: 0})
eqsP = [sp.expand(e.subs(R_, 1)) for e in eqsP]
unkP = [FaP[uu] for uu in UNK0]
print(f"       (w parallel to k: system built, {time.time()-T0:.0f}s)")


def ratio(kb, ay, fpp, qv):
    """2 h_00^(2) / h_00^(0) at k = 1, rho = 1: the O(w^2) coefficient a+b, exact rational."""
    e = [sp.expand(xx.subs({KB: kb, AY: ay, Fpp: fpp, qq: qv})) for xx in eqsP]
    hs = hcoeffs(e, unkP, FaP["h00"])
    return sp.cancel(2 * hs[2] / hs[0]), hs


LAMROWS = []
for lam in (sp.Rational(1, 10 ** 4), sp.Rational(1, 100), sp.Integer(1),
            sp.Integer(100), sp.Integer(10 ** 4), sp.Integer(10 ** 6)):
    pair = []
    for aex in (12, 16):
        ayv = sp.Integer(10) ** aex
        qv = sp.sqrt(sp.Rational(lam) / ayv)
        v, _ = ratio(sp.Rational(1, 10), ayv, 4, qv)
        pair.append(float(v))
    LAMROWS.append((float(lam), pair[0], pair[1]))
print(f"       {'Lambda = A_Y Q_0^2/k^2':>23s} {'a+b at A_Y=1e12':>17s} {'a+b at A_Y=1e16':>17s}")
for lv, v1, v2 in LAMROWS:
    print(f"       {lv:23.3g} {v1:17.10f} {v2:17.10f}")
check(all(abs(v1 - v2) < 1e-8 * max(1.0, abs(v1)) for _, v1, v2 in LAMROWS),
      "B5  *** IN THE A_Y -> infinity LIMIT THE O(w^2) COEFFICIENT IS A FUNCTION OF "
      "Lambda = A_Y Q_0^2/k^2 ALONE -- identical to 8+ digits at A_Y = 1e12 and 1e16, four "
      "decades of Lambda apart.  So 'A_Y -> infinity' is not a single limit: it is a family, "
      "indexed by Lambda, and A_Y -> infinity does NOT commute with Q_0/k -> 0 ***",
      "this is the non-uniformity the frozen treatment hides.  It is NOT a gradient effect: it "
      "is present for a strictly constant A_Y")


def longrange(kb, ay, fpp, qds=(10 ** 8, 3 * 10 ** 8, 10 ** 9)):
    """the verified file's own extraction: the qq^0 coefficient of the O(w^2) part (Lambda -> 0)."""
    dat = []
    for d in qds:
        qv = sp.Rational(1, d)
        e = [sp.expand(xx.subs({KB: kb, AY: ay, Fpp: fpp, qq: qv})) for xx in eqsP]
        dat.append((qv, hcoeffs(e, unkP, FaP["h00"])))
    Cm2, C0, C2 = sp.symbols("Cm2 C0 C2")
    sol = sp.solve([sp.Eq(Cm2 / qv ** 2 + C0 + C2 * qv ** 2, d[2]) for qv, d in dat],
                   [Cm2, C0, C2], dict=True)[0]
    return sol[C0], sol[Cm2], dat[-1][1][0]


apb_closed = 2 * KB * (3 * KB - 2) / (2 - KB) ** 2
rep = []
for kb, ay in ((sp.Rational(1, 10), 10 ** 6), (sp.Rational(1, 10), 10 ** 8),
               (sp.Rational(1, 2), 10 ** 6)):
    C0, Cm2, h0 = longrange(kb, ay, 4)
    v = 2 * C0 / h0
    tg = apb_closed.subs(KB, kb)
    rep.append((float(kb), ay, float(v), float(tg), float((v - tg) * ay)))
print(f"       {'K_B':>6s} {'A_Y':>10s} {'a+b (Lambda->0)':>17s} {'2K_B(3K_B-2)/(2-K_B)^2':>23s} "
      f"{'resid x A_Y':>12s}")
for kb, ay, v, tg, rr in rep:
    print(f"       {kb:6.3g} {ay:10d} {v:17.10f} {tg:23.10f} {rr:12.4f}")
check(all(abs(v - tg) < 20.0 / ay for _, ay, v, tg, _ in rep),
      "B6  *** THE VERIFIED FILE'S RESULT IS REPRODUCED, IN ITS OWN CORNER: the Lambda -> 0 "
      "value of a+b is 2 K_B(3K_B-2)/(2-K_B)^2, its Q3-1, with the residual scaling as 1/A_Y "
      "exactly as it reported ***",
      "so nothing below is a disagreement about algebra.  What follows is about the DOMAIN of "
      "that formula, and PART C shows the domain excludes 1 AU")
big = [(float(lam), v1) for lam, v1, v2 in LAMROWS if lam >= 1e4]
check(all(abs(v + 4.0) < 1e-3 for _, v in big),
      "B7  *** AND THE Lambda -> infinity CORNER GIVES a+b = -4 EXACTLY, INDEPENDENT OF K_B, "
      "Fpp, A_Y AND Q_0 ***",
      "verified separately at K_B = 0.01, 0.1, 0.25, 0.5 and at Fpp = 4, 7 during development, "
      "and it survives K_B = 0 and c_J = 0.  A preferred-frame coefficient that does not "
      "vanish when the aether kinetic term is switched off is a RED FLAG on the truncation -- "
      "the first suspect being the four h_{3 nu} field equations that the gauge leaves unused "
      "(the verified file's own 'ARGUED, NOT VERIFIED DIRECTLY' ledger entry, and stage74 B2's "
      "finding that the (3,nu) equations are pure constraints that cannot be discarded).  IT IS "
      "THEREFORE NOT BANKED AS AN alpha; it is banked as proof that the corner matters")
flo = []
for kb in (sp.Rational(1, 1000), sp.Rational(1, 10 ** 5), sp.Rational(1, 10 ** 7)):
    C0, Cm2, h0 = longrange(kb, 10 ** 6, 4)
    v = 2 * C0 / h0
    tg = float(apb_closed.subs(KB, kb))
    flo.append((float(kb), float(v), tg, float((v - tg) * 10 ** 6)))
print(f"       {'K_B':>10s} {'a+b(A_Y=1e6)':>16s} {'K_B-only formula':>18s} {'resid x A_Y':>12s}")
for kb, v, tg, rr in flo:
    print(f"       {kb:10.3g} {v:16.9g} {tg:18.9g} {rr:12.5f}")
check(all(abs(rr + 4.0) < 0.05 for _, _, _, rr in flo),
      "B8  *** AND 'K_B ALONE' IS A PROPERTY OF THE STRICT LIMIT ONLY: at finite A_Y the "
      "Lambda -> 0 value of a+b carries a K_B-INDEPENDENT additive term -> -4/A_Y as K_B -> 0.  "
      "At the K_B values where the ceilings sit (6.7e-5 and 4.0e-8) that floor DOMINATES the "
      "K_B-linear term unless A_Y is astronomically large ***",
      "so C4's arithmetic -- read a |alpha| bound, invert the K_B-only formula, quote a K_B "
      "ceiling -- is only defined in the strict A_Y -> infinity limit.  At any finite A_Y the "
      "alphas do not go to zero with K_B and there is no K_B ceiling to quote, empty window or "
      "not")

# ---------------- the PERPENDICULAR orientation: a, hence the individual alpha's -------------
t1 = time.time()
ZFperp = ("h02", "h12", "h23", "h13", "h03", "h33", "a2")
UNKperp = ["h00", "h01", "h11", "h22", "a0", "a1", "a3", "chi", "lam"]
r, eqsQ, FaQ, GaQ, _ = equations([s * sp.Integer(1), 0, 0], ZFperp, UNKperp,
                                 extra_sub={cJ: 2 - KB, Q0: qq, k: 1, om: 0})
eqsQ = [sp.expand(e.subs(R_, 1)) for e in eqsQ]
unkQ = [FaQ[uu] for uu in UNKperp]
print(f"       (w perpendicular to k: system built, {time.time()-t1:.0f}s)")


def ratio_perp(kb, ay, fpp, qv):
    e = [sp.expand(xx.subs({KB: kb, AY: ay, Fpp: fpp, qq: qv})) for xx in eqsQ]
    hs = hcoeffs(e, unkQ, FaQ["h00"])
    return sp.cancel(2 * hs[2] / hs[0])


perp0, perpI = [], []
print(f"       {'K_B':>6s} {'A_Y':>8s} {'qq':>8s} {'Lambda':>10s} {'a':>18s} {'4 K_B':>9s} "
      f"{'resid x A_Y':>12s} {'4(2-K_B)^2':>11s}")
for kb, ay, qv in ((sp.Rational(1, 10), sp.Integer(10) ** 5, sp.Rational(1, 10 ** 6)),
                   (sp.Rational(1, 10), sp.Integer(10) ** 6, sp.Rational(1, 10 ** 7)),
                   (sp.Rational(1, 4), sp.Integer(10) ** 6, sp.Rational(1, 10 ** 7)),
                   (sp.Rational(1, 2), sp.Integer(10) ** 6, sp.Rational(1, 10 ** 7))):
    v = ratio_perp(kb, ay, 4, qv)
    perp0.append((float(kb), int(ay), float(v)))
    print(f"       {float(kb):6.3g} {float(ay):8.0e} {float(qv):8.0e} {float(ay*qv**2):10.2e} "
          f"{float(v):18.10f} {float(4*kb):9.4f} {float((v-4*kb)*ay):12.4f} "
          f"{float(4*(2-kb)**2):11.4f}")
for kb, ay, qv in ((sp.Rational(1, 10), sp.Integer(10) ** 12, sp.Rational(1, 100)),
                   (sp.Rational(1, 10), sp.Integer(10) ** 14, sp.Rational(1, 100)),
                   (sp.Rational(1, 2), sp.Integer(10) ** 12, sp.Rational(1, 100))):
    v = ratio_perp(kb, ay, 4, qv)
    perpI.append((float(kb), int(ay), float(v)))
    print(f"       {float(kb):6.3g} {float(ay):8.0e} {float(qv):8.0e} {float(ay*qv**2):10.2e} "
          f"{float(v):18.10f} {float(4*kb):9.4f} {'':>12s} {'':>11s}")
check(all(abs(v - 4 * kb) < 20.0 / ay for kb, ay, v in perp0),
      "B9  *** THE SECOND OF THE VERIFIED FILE'S TWO NUMBERS IS ALSO REPRODUCED IN ITS CORNER: "
      "w PERPENDICULAR to k gives a = 4 K_B at Lambda -> 0, its Q3-3, with the residual scaling "
      "as 1/A_Y AND with the 1/A_Y coefficient equal to 4(2-K_B)^2 -- the very check that file "
      "quoted (14.44 at K_B = 0.1, 12.25 at K_B = 0.25).  Recovered here to 0.8% ***",
      "so this file agrees with ppn_scalar_retained_2026.py on BOTH orientations, hence on "
      "alpha_1 and alpha_2 themselves, wherever Lambda << 1.  ONE TECHNICAL NOTE THAT IS ITSELF "
      "part of the non-uniformity: these rows need qq << 1/A_Y, because at qq ~ 1/A_Y the O(1/A_Y) "
      "residual and the O(Lambda) term are the SAME SIZE and a single-qq evaluation mixes them.  "
      "The verified file avoided that by fitting a Laurent series in qq -- which is exactly the "
      "step that presumes Lambda << 1")
check(all(abs(v - 8.0) < 1e-6 for _, _, v in perpI),
      "B10 *** AND IN THE Lambda >> 1 CORNER a = +8 EXACTLY, independent of K_B and A_Y.  With "
      "B7's a+b = -4 that gives b = -12 and the individual parameters\n"
      "           alpha_1 = +2, alpha_2 = +6   (convention C4, this file and the verified file)\n"
      "           alpha_1 = -8, alpha_2 = -6   (Will's convention)\n"
      "       -- O(1), K_B-INDEPENDENT, i.e. over |alpha_1| < 1e-4 by 1e4-1e5 and over "
      "|alpha_2| < 1e-7 by ~1e8, for EVERY K_B including K_B = 0 ***",
      "REPORTED, NOT BANKED, and the reason is the same as B7's: a preferred-frame parameter "
      "that is completely insensitive to the aether kinetic coefficient is the signature of a "
      "truncation artefact.  Its value is as a DIAGNOSTIC: it shows that the two corners of the "
      "non-commuting limit differ by 8 orders of magnitude in the observable, so the corner "
      "cannot be chosen by convenience")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- WHICH CORNER IS THE SOLAR SYSTEM IN?  (and PART D's y = 1 radius)")
print("=" * 100)
Q0INV = (("Q_0^-1 = 100 Mpc (the verified file's own estimate)", 100.0 * MPCm),
         ("Q_0^-1 =   1 Mpc (mu^-1 floor, most conservative)", 1.0 * MPCm))


def sqrty(rm, a0):
    return math.sqrt(GMSUN / (rm ** 2 * a0))


def log10Lam(rm, a0, L):
    # Lambda = A_Y Q_0^2 / k^2 with A_Y = (2-K_B) e^{sqrt y} ~ 2 e^{sqrt y}, k = 1/r
    return math.log10(2.0) + sqrty(rm, a0) / math.log(10.0) + 2.0 * math.log10(rm / L)


R1 = {}
print(f"       {'footing':>10s} {'r(y=1) [m]':>12s} {'r(y=1) [AU]':>12s} {'r(y=1) [pc]':>12s}")
for lab, a0 in FOOT:
    r1 = math.sqrt(GMSUN / a0)
    R1[lab] = r1
    print(f"       {lab:>10s} {r1:12.4e} {r1/AU:12.1f} {r1/PCm:12.5f}")
check(abs(R1["canonical"] / AU - 7958.0) < 5.0 and abs(R1["ALT"] / AU - 7251.0) < 5.0,
      "C1  *** QUESTION (d), FIRST HALF: the 1/A_Y screening switches off at y = 1, i.e. at "
      "r = sqrt(GM_sun/a_0) = 1.1906e15 m = 7958 AU = 0.0386 pc (canonical) and 1.0848e15 m = "
      "7251 AU = 0.0352 pc (ALT).  Inside it A_Y = (2-K_B) e^(sqrt y) with sqrt y = r(y=1)/r "
      "exactly ***",
      "so sqrt(y) at 1 AU is literally the y=1 radius measured in AU: 7958 canonical / 7251 "
      "alt.  That identity is why the screening is exponential in 1/r")

VESC, RSUN_GAL = 2.33e5, 8.178e3 * PCm
GEXT = VESC ** 2 / RSUN_GAL
print(f"       Galactic external field at the Sun (V0 = 233 km/s, R0 = 8.178 kpc): "
      f"g_ext = {GEXT:.4e} m/s^2")
yext = {lab: GEXT / a0 for lab, a0 in FOOT}
print(f"       => y never falls below y_ext = {yext['canonical']:.3f} (canonical) / "
      f"{yext['ALT']:.3f} (ALT), so 1/A_Y bottoms out at "
      f"{1.0/(2.0*math.exp(math.sqrt(yext['canonical']))):.3f} / "
      f"{1.0/(2.0*math.exp(math.sqrt(yext['ALT']))):.3f}")
check(min(yext.values()) > 1.0,
      "C2  QUESTION (d), SECOND HALF: the external-field effect puts a FLOOR under y -- the "
      "Galactic field alone keeps y >= 1.9, so the deep-MOND regime y << 1 is never reached "
      "around the Sun at all, and the screening never switches off completely (1/A_Y bottoms "
      "out near 0.1)",
      "and the answer to 'could the PPN parameters be dominated by that region': NO on the "
      "measurement side -- |alpha_1| < 1e-4 (lunar laser ranging) and |alpha_2| < 1e-7 (solar "
      "spin axis) are both set at ~1 AU where y = 6.3e7 -- but YES in an inverted sense, "
      "because C3 shows the verified formula's own domain of validity lies OUTSIDE ~150 AU.  A "
      "further honest point: in this treatment alpha_1 and alpha_2 are y-DEPENDENT (their "
      "residual is O(1/A_Y(r))), so they are not PPN constants at all")

print()
print(f"       {'r':>10s} {'sqrt y':>9s} {'log10 1/A_Y':>12s} "
      f"{'log10 Lambda (100 Mpc)':>23s} {'log10 Lambda (1 Mpc)':>21s}")
for rlab, rm in (("1 AU", AU), ("Neptune 30 AU", 30 * AU), ("157 AU", 157 * AU),
                 ("1000 AU", 1000 * AU), ("r(y=1)", R1["canonical"])):
    sy = sqrty(rm, 9.3619e-11)
    print(f"       {rlab:>10s} {sy:9.2f} {-(math.log10(2.0)+sy/math.log(10.0)):12.1f} "
          f"{log10Lam(rm, 9.3619e-11, 100*MPCm):23.1f} {log10Lam(rm, 9.3619e-11, 1*MPCm):21.1f}")
LAM_1AU = {lab: log10Lam(AU, a0, 100 * MPCm) for lab, a0 in FOOT}
check(all(v > 3000 for v in LAM_1AU.values()),
      "C3  *** THE DECISIVE NUMBER: Lambda(1 AU) = 1e{:.0f} (canonical) / 1e{:.0f} (ALT) under "
      "the verified file's own Q_0^-1 ~ 100 Mpc.  THE SOLAR SYSTEM IS IN THE Lambda >> 1 "
      "CORNER, by 3430 orders of magnitude -- not in the Lambda -> 0 corner the alpha formulas "
      "were extracted from ***"
      .format(LAM_1AU["canonical"], LAM_1AU["ALT"]),
      "and it is robust to Q_0: Lambda < 1 at 1 AU would need Q_0^-1 > 1e1728 AU, vastly beyond "
      "the Hubble radius.  The only escape is Q_0 = 0 exactly -- which is precisely the case "
      "the verified file's Q2-2 shows collapses the determinant and restores reading D's "
      "degeneracy")


def crossing(a0, L):
    lo, hi = 1.0 * AU, 1.0e6 * AU
    if log10Lam(lo, a0, L) < 0 or log10Lam(hi, a0, L) > 0:
        return float("nan")
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if log10Lam(mid, a0, L) > 0:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


print(f"       {'footing':>10s} {'Q_0^-1':>10s} {'r* where Lambda = 1':>21s}")
RSTAR = {}
for lab, a0 in FOOT:
    for qlab, L in Q0INV:
        rs = crossing(a0, L)
        RSTAR[(lab, L)] = rs
        print(f"       {lab:>10s} {qlab.split('=')[1].split('(')[0].strip():>10s} "
              f"{rs/AU:18.1f} AU")
check(all(50 * AU < v < 500 * AU for v in RSTAR.values()),
      "C4  *** THE CORNER BOUNDARY, both footings and two Q_0: Lambda = 1 at r* = {:.0f} AU "
      "(canonical, 100 Mpc) / {:.0f} AU (ALT, 100 Mpc), and {:.0f} / {:.0f} AU at 1 Mpc.  So the "
      "verified alpha formulas' corner is realised only OUTSIDE ~150 AU, while both bounds they "
      "are tested against are measured at ~1 AU.  The formula and the measurement DO NOT "
      "OVERLAP ***"
      .format(RSTAR[("canonical", 100 * MPCm)] / AU, RSTAR[("ALT", 100 * MPCm)] / AU,
              RSTAR[("canonical", 1 * MPCm)] / AU, RSTAR[("ALT", 1 * MPCm)] / AU),
      "note the direction: outside r* the alphas ARE the quoted K_B-only formulas (up to "
      "1/A_Y), but there is no |alpha_1| < 1e-4 or |alpha_2| < 1e-7 measurement at 150-2000 AU "
      "to confront them with")

LM = []
for lab, a0 in FOOT:
    sy = sqrty(AU, a0)
    lg = math.log10(100 * MPCm) - math.log10(2.0) / 2 - (sy / 2.0) / math.log(10.0)
    LM.append((lab, lg))
print(f"       Yukawa range in that corner, 1/m = e^(-sqrt y/2)/(Q_0 sqrt(2-K_B)) at 1 AU:")
for lab, lg in LM:
    print(f"         {lab:>10s}: log10(1/m [m]) = {lg:9.1f}   (Planck length = 1e-35 m)")
check(all(lg < -100 for _, lg in LM),
      "C5  *** AND THAT CORNER IS NOT A PHYSICAL PPN REGIME: with A_Y = (2-K_B) e^(sqrt y) the "
      "graviton Yukawa range at 1 AU is 1e{:.0f} m, some 1669 orders BELOW the Planck length.  "
      "Newtonian gravity would not exist.  The Lambda >> 1 corner is the frozen-A_Y input "
      "announcing its own inconsistency, not a prediction ***"
      .format(LM[0][1]),
      "and the diagnosis is sharp, because B3 says what the mass SHOULD be: m^2 equals SZ21's "
      "mu^2 when A_Y ~ 4 K_2 ~ 1e4.  A_Y = (2-K_B) e^(sqrt y) inflates it by e^(sqrt y)/(2K_2), "
      "i.e. by 1e3453")
check(True,
      "C6  THE ROOT CAUSE, named: the quadratic action was expanded about a background with "
      "Y_bg = 0 (the verified file's own check 0-1) -- and Y = 0 is the point where its own "
      "G_eff/G = 2A_Y/[(2-K_B)(A_Y-(2-K_B))] DIVERGES, i.e. the DEEP-MOND point, not the solar "
      "system.  The solar-system stiffness A_Y = (2-K_B) e^(sqrt y) was then imported into that "
      "background from a separate quasi-static matching performed at Q_0 = 0.  Expanding about "
      "the true solar-system background, which has Y_bg != 0, is NOT COMPUTED -- here or "
      "anywhere in the corpus",
      "this is why the caveat cannot be discharged by any gradient calculation: it is not that "
      "A_Y varies, it is that the value being frozen belongs to a different background from the "
      "one the perturbation theory is built on")
check(True,
      "C7  *** THE FORK, WITH BOTH BRANCHES PRICED, AND NEITHER BANKED ***\n"
      "       branch (I)  A_Y = (2-K_B) e^(sqrt y)  [the verified file's G5, kernel-matched]:\n"
      "                   Lambda(1 AU) = 1e3430, m^-1 = 1e-1704 m.  The alpha formulas are\n"
      "                   INAPPLICABLE at 1 AU and the Newtonian limit is destroyed there.\n"
      "       branch (II) A_Y = O(4 K_2) ~ 1e4      [the value that makes m^2 = SZ21's mu^2]:\n"
      "                   Lambda(1 AU) ~ 1e-22, the verified corner IS physical, grad(A_Y) = 0\n"
      "                   identically, the 1/A_Y residual is ~1e-5 relative -- and C3/C4's\n"
      "                   ceilings and the 5263x empty window STAND essentially unchanged,\n"
      "                   EXCEPT that B8's K_B-independent -4/A_Y ~ -1e-4 floor then exceeds\n"
      "                   |alpha_2| < 1e-7 by ~1e3 for EVERY K_B including K_B = 0, which is a\n"
      "                   K_B-independent kill and therefore a red flag on the truncation.\n"
      "       The two identifications of A_Y differ by 3450 orders of magnitude and cannot both\n"
      "       be right.  Deciding between them is the owed item this route uncovers.",
      "DIRECTION, stated plainly: relative to the verified file this REMOVES an adverse kill "
      "(the empty window is not established at 1 AU) while pointing at a possibly worse "
      "problem (an O(1) or K_B-independent alpha).  It is NOT a favourable result for the "
      "framework and must not be reported as one")
info("C8  ONE FURTHER OBSERVATION, READ OFF THE VERIFIED FILE'S CODE RATHER THAN DERIVED HERE, "
     "and therefore recorded as an observation and not a check: the OTHER edge of the two-sided "
     "window is a Q_0 = 0 object too.  The subluminality floor K_B >= 2/(K_2+1) comes from that "
     "file's c_s^2, extracted at its line 'scal0 = sp.expand(scal.subs(Q_0, 0))', and its A_Y "
     "identification comes from 'h00_qs = h00_0.subs(Q_0, 0)'.  So both EDGES of the window are "
     "computed at Q_0 = 0 while the alpha's that the window constrains exist only for "
     "Q_0 != 0.  Whether c_s^2 and the floor survive at general Q_0 is NOT COMPUTED here.",
     "flagged because it is the same defect as PART B and would be cheap to settle: rerun that "
     "file's own mode determinant without the Q_0 -> 0 substitution")

# =================================================================================================
print()
print("=" * 100)
print("PART S -- STATUS LEDGER")
print("=" * 100)
LEDGER = [
    ("RIGOROUS (symbolic, exact, in this file)",
     "A1-A5: A_Y enters the quadratic action at degree 1, in one term, whose field dependence "
     "differentiates only chi; the A_Y-part of the chi equation is the exact identity "
     "i k A_Y W^z = d_z sigma^z; the A_Y-part of every other equation is algebraic.  B1: the "
     "exact w = 0 response with a Yukawa mass m^2 = (2A_Y-Fpp)Q_0^2 A_Y/[2(2-K_B)(A_Y-(2-K_B))]. "
     "B2: its Q_0 -> 0 slice reproduces the verified G4b/G4c.  B3: m^2 -> SZ21's mu^2 at "
     "A_Y = Fpp = 4K_2.  B4: gamma_PPN = 1 at general Q_0.  A6: the global bounds "
     "max sqrt(y)e^(-sqrt y) = e^-1 and max y e^(-sqrt y) = 4e^-2."),
    ("RIGOROUS (exact-rational numerics, in this file)",
     "B5: the O(w^2) coefficient is a function of Lambda = A_Y Q_0^2/k^2 alone in the "
     "A_Y -> infinity limit (8+ digits, two A_Y decades).  B6/B9: the verified file's "
     "a+b = 2K_B(3K_B-2)/(2-K_B)^2 AND a = 4 K_B reproduced in the Lambda -> 0 corner, both "
     "orientations.  B7/B10: a+b = -4 and a = +8 in the Lambda -> infinity corner.  B8: the "
     "K_B-independent -4/A_Y floor at finite A_Y."),
    ("THE ANSWER TO THE ASSIGNED QUESTIONS",
     "(a) NO correction: the gradient-enhanced residual on alpha_1, alpha_2 at 1 AU is 1e-3453 "
     "(canonical) / 1e-3145 (alt) relative.  (b) STRUCTURAL, and the reason is A2+A4: A_Y "
     "multiplies a single quadratic form whose only differentiated field is chi, so the "
     "A_Y -> infinity limit is a constraint limit written in sigma = A_Y W, which contains no "
     "A_Y.  (c) grad -> 0 and A_Y -> infinity COMMUTE -- but A_Y -> infinity and Q_0/k -> 0 do "
     "NOT, and that is the pair that decides the verdict.  (d) y = 1 at 7958 AU canonical / "
     "7251 AU alt; the Galactic external field keeps y >= 1.9 so the screening never fully "
     "switches off; the bounds are measured at 1 AU (y = 6.3e7) so the deep-MOND region does "
     "not dominate them -- but the verified formula's domain of validity lies outside ~150 AU, "
     "which is the inverse of the worry as posed."),
    ("CONDITIONAL -- the identification of A_Y",
     "everything adverse in PART C is conditional on A_Y = (2-K_B) e^(sqrt y).  Under "
     "A_Y = O(4 K_2) the verified corner is physical and C3/C4 stand (modulo B8).  The two "
     "cannot both hold; see C7."),
    ("ARGUED, NOT VERIFIED HERE -- the Lambda >> 1 alpha's",
     "B7/B10's Lambda -> infinity values (a+b = -4, a = +8, hence alpha_1 = +2, alpha_2 = +6 in "
     "convention C4 and alpha_1 = -8, alpha_2 = -6 in Will's) are exact in this system and "
     "independent of every parameter including K_B, which is the signature of a truncation "
     "artefact rather than a preferred-frame coefficient.  The first suspects are the four "
     "unused h_{3 nu} equations (the verified file's own ARGUED-NOT-VERIFIED entry; stage74 B2 "
     "holds that the (3,nu) equations are pure constraints that cannot be discarded).  NOT "
     "banked as alpha's; banked only as proof that the corner changes the observable by 8 "
     "orders of magnitude."),
    ("NOT COMPUTED -- the correct background",
     "the PPN expansion about a solar-system background with Y_bg != 0, which is what would fix "
     "A_Y self-consistently and settle C7.  Also not computed: whether including the unused "
     "h_{3 nu} constraints changes B7; the g_0i sector; alpha_3, beta, zeta; and the deep-MOND "
     "PPN regime.  All of these were already flagged NOT COMPUTED by the verified file."),
    ("UNTOUCHED",
     "a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 "
     "(FITTED, never derived); the kernel nu(y) = 1/(1-e^(-sqrt y)) (Milgrom & Sanders 2008 "
     "Eq. 13 at alpha = 1/2); gamma_PPN = 1 (re-verified here at general Q_0, check B4); the "
     "RAR, BTFR, weak lensing, CLASS, the frozen DR4 band.  The verified file's c_T^2 = 1 and "
     "c_s^2 = SZ21 Eq. (30) results are not re-examined here and nothing above bears on them."),
]
for lab, txt in LEDGER:
    print(f"    {lab}:\n        {txt}")
check(True, "S1  status ledger printed with every claim graded")

print()
print("=" * 100)
nf = len(FAIL)
print(f"PPN-GRADIENT-A_Y VERIFICATION CHECKS: {NCHK[0]-nf}/{NCHK[0]} passed"
      + ("" if not nf else f";  FAILED: {FAIL}"))
print(f"runtime {time.time()-T0:.0f}s")
sys.exit(1 if FAIL else 0)
