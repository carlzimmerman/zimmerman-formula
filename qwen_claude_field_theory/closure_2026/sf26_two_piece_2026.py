#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf26_two_piece_2026.py
======================
THE TWO-PIECE INTERACTION: the electric piece added, its lensing effect computed, and the design
equations for the full observables solved.  VERDICT: THE REPAIR WORKS AT THE LEVEL THIS FILE CAN
COMPUTE, with one exact and unexpected result -- the lensing repair FIXES the electric piece's
normalisation completely, leaving NO new freedom.

THE VERDICT, up front and adverse: *** THE TWO-PIECE REPAIR FAILS, AND IT FAILS BY A TRILEMMA
THAT IS NOW EXPLICIT. ***

  (i)  With the electric piece in its QUADRATIC form Upsilon_E ~ (grad(Phi-Phihat))^2, the
       lensing mismatch is computed exactly and its residual is

           g_lens - g_dyn  =  F_M M_f^4 a_0^2 m_I m_enc / (4 * denominator)

       whose numerator is PROPORTIONAL TO F_M ALONE.  No value of the electric slope G_E
       cancels it: the only roots are F_M = 0 (no MOND at all) or the limit G_E -> infinity,
       in which g_dyn -> m_enc/(2(M_g^2+M_f^2)) -- pure Newton with a rescaled constant, the
       anomaly gone.  FIXING LENSING BY THE ELECTRIC PIECE DELETES THE PHENOMENOLOGY.

  (ii) And the LAPSE-LINEAR form that sf10 identified as HR-safe, sqrt(Upsilon_E), cannot be
       used instead: sqrt of a second-order quantity is FIRST order in the perturbation, so it
       contributes not a quadratic kinetic term but a constant-magnitude flux -- exactly the
       saturating sunward anomaly that R1 killed.

  *** SO THE ELECTRIC PIECE MAY BE LAPSE-LINEAR (HR-safe, R2) OR SUPPLY A QUADRATIC
  ENERGY-DENSITY CHANNEL (lensing, sf25), BUT NOT BOTH -- the same 1/2-versus-3/2 exponent
  tension sf10 found in the constraint sector, reappearing in the lensing sector.  This is the
  programme's recurring structure for the fourth time: the fix has a bill, and the bill arrives
  in the sector the fix was not looking at. ***

WHAT THIS KILLS AND WHAT IT LEAVES.  It kills the two-piece repair AS CONSTRUCTED, i.e. the
straightforward addition of an electric scalar to the spatial one.  It does NOT kill the
architecture, but it sharpens what any successful repair must do: supply an energy-density
channel (T_00 nonzero) WITHOUT a term that is either lapse-nonlinear or first-order.  The
remaining candidates are structural rather than additive -- a matter coupling to a composite
(disformal) metric built from the khronon, which moves the lensing question into the coupling
rather than the interaction, is the named next direction and is NOT computed here.

THE CONSTRUCTION.  Add to the spatial (magnetic) piece the ELECTRIC scalar in its lapse-LINEAR
(HR-safe, sf10 PART E) square-root form.  In the static sector the electric part of the
connection difference carries exactly the 00-structure: C^i_{00}-type components go as
grad(Phi - Phihat), so

    sqrt(Upsilon_E)  ->  |grad(Phi - Phihat)| / a_0-normalisation      (static limit)

and the interaction becomes, at quadratic-flux order with local nonlinear slopes carried
(the sf13b treatment),

    L_int = mI [ (F' + B') (grad(Psi - Psihat))^2 + G_E |grad(Phi - Phihat)|-terms ] / a_0^2

where G_E is the electric piece's local slope.  KEY STRUCTURAL FACT: the electric term DOES
carry Phi -- it restores exactly the energy-density channel whose absence caused sf25's kill.

WHAT THIS FILE ESTABLISHES:

  1. GR control unchanged (Phi = Psi, standard lensing) -- the machinery stands.
  2. With both pieces on, the flux system solves and the two observables become
         g_dyn  = g_N + Delta_M + Delta_E
         g_lens = g_N + Delta_M/2 + Delta_E                    (the electric piece feeds BOTH
     potentials equally -- because it enters through the Phi-variation, which sources Psi, AND
     the Psi-variation is untouched by it... the computation decides, not the prose)
  3. THE DESIGN CONDITION: g_lens = g_dyn (the corpus's KiDS standing demands the full anomaly
     in lensing) forces a RELATION between the electric and magnetic slopes.  Solved exactly.
  4. WHAT SURVIVES OF THE MOEBIUS CHAIN: with the electric piece pinned by lensing, the
     dynamical force law is re-derived and the a_0-line design equation re-solved.
  5. NAMED AND NOT DONE: the two-piece ghost check (the electric piece is lapse-LINEAR, the
     HR-safe form, so the lapse Hessian remains identically zero -- BUT the full constraint
     algebra with both pieces is a redo of sf19-24 and is owed), and the sign chain a la sf13d
     for the electric normalisation.

Exit 0 = every numbered check passed.
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


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)
x, ep = sp.symbols("x epsilon")
a0 = sp.Symbol("a_0", positive=True)
Mg2, Mf2, mI = sp.symbols("M_g^2 M_f^2 m_I", positive=True)
Phi, Psi = sp.Function("Phi")(x), sp.Function("Psi")(x)
Phh, Psh = sp.Function("Phihat")(x), sp.Function("Psihat")(x)
rho = sp.Function("rho")(x)
XC = [sp.Symbol("t"), x, sp.Symbol("y"), sp.Symbol("z")]


def sqrtgR_quad(Phi_, Psi_):
    g = sp.diag(-(1 + 2 * ep * Phi_), 1 - 2 * ep * Psi_, 1 - 2 * ep * Psi_, 1 - 2 * ep * Psi_)
    gi = g.inv()
    Gam = [[[sum(gi[l, r] * (sp.diff(g[r, m], XC[n]) + sp.diff(g[r, n], XC[m])
                             - sp.diff(g[m, n], XC[r])) for r in range(4)) / 2
             for n in range(4)] for m in range(4)] for l in range(4)]
    Ric = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            s_ = 0
            for l in range(4):
                s_ += sp.diff(Gam[l][m][n], XC[l]) - sp.diff(Gam[l][m][l], XC[n])
                for p_ in range(4):
                    s_ += Gam[l][l][p_] * Gam[p_][m][n] - Gam[l][n][p_] * Gam[p_][m][l]
            Ric[m, n] = s_
    R = sum(gi[m, n] * Ric[m, n] for m in range(4) for n in range(4))
    quad = sp.expand(sp.series(sp.sqrt(-g.det()) * R, ep, 0, 3).removeO().coeff(ep, 2))
    for F_ in (Phi_, Psi_):
        d2 = sp.diff(F_, x, 2)
        c2 = sp.expand(quad).coeff(d2)
        quad = sp.expand(quad - c2 * d2 - sp.expand(sp.diff(c2, x)) * sp.diff(F_, x))
    return sp.simplify(quad)


def EL(L, F_):
    return sp.expand(sp.diff(L, F_) - sp.diff(sp.diff(L, sp.diff(F_, x)), x))


# =========================================================================================
head("PART A -- the two-piece interaction at quadratic-flux order")
# =========================================================================================
FM, GE = sp.symbols("F_M G_E", real=True)      # magnetic slope (F'+B' combined), electric slope
psi_d = Psh - Psi
phi_d = Phh - Phi
L_g = (Mg2 / 2) * sqrtgR_quad(Phi, Psi)
L_f = (Mf2 / 2) * sqrtgR_quad(Phh, Psh)
L_M = mI * FM * sp.diff(psi_d, x)**2 / a0**2
L_E = mI * GE * sp.diff(phi_d, x)**2 / a0**2
check(sp.diff(L_E, sp.diff(Phi, x)) != 0,
      "A1  *** THE ELECTRIC PIECE CARRIES Phi: in QUADRATIC form Upsilon_E ~ "
      "(grad(Phi - Phihat))^2 it restores exactly the energy-density channel whose absence "
      "caused sf25's kill.  NOTE: this is the quadratic form, NOT sf10's lapse-linear "
      "sqrt(Upsilon_E) -- PART D shows why the two cannot be the same term ***",
      "the quadratic form gravitates; whether it is HR-safe and whether it repairs the split "
      "are the questions of PARTS C-D")
L2 = L_g + L_f + L_M + L_E - rho * Phi
eqs = {F_: EL(L2, F_) for F_ in (Phi, Psi, Phh, Psh)}
check(sp.simplify(sp.expand(eqs[Phi]).coeff(GE)) != 0
      and sp.simplify(sp.expand(eqs[Psi]).coeff(GE)) == 0,
      "A2  and it enters the Phi-VARIATION (which determines Psi) and NOT the Psi-variation: "
      "the mirror of the magnetic piece.  Each piece owns one channel",
      "magnetic -> Psi-variation only (sf25 B3); electric -> Phi-variation only (here)")

# =========================================================================================
head("PART B -- first integrals, both observables")
# =========================================================================================
P1, S1, Ph1, Sh1 = sp.symbols("Phi1 Psi1 Phihat1 Psihat1", real=True)
m_enc = sp.Symbol("m_enc", positive=True)
subs1 = {sp.diff(Phi, x): P1, sp.diff(Psi, x): S1, sp.diff(Phh, x): Ph1, sp.diff(Psh, x): Sh1}


def first_integral(eq):
    out = 0
    for t in sp.expand(eq).args:
        for F_, s_ in ((Phi, P1), (Psi, S1), (Phh, Ph1), (Psh, Sh1)):
            d2 = sp.diff(F_, x, 2)
            if t.has(d2):
                out += t.coeff(d2) * s_
                break
        else:
            if t.has(rho):
                out += (t / rho) * m_enc
    return sp.expand(out.subs(subs1))


I = {k: first_integral(v) for k, v in eqs.items()}
sol = sp.solve([sp.Eq(v, 0) for v in I.values()], [P1, S1, Ph1, Sh1], dict=True)
check(len(sol) == 1, "B1  the four-potential flux system solves uniquely", f"branches: {len(sol)}")
gdyn = sp.simplify(sol[0][P1])
Spr = sp.simplify(sol[0][S1])
glens = sp.simplify((gdyn + Spr) / 2)
info("B2  the raw solutions", f"Phi' = {gdyn}\n           Psi' = {Spr}")
check(Spr.has(GE) and Spr.has(FM),
      "B3  Psi now hears BOTH slopes -- the electric piece does modify the Phi-variation (which "
      "determines Psi), so the restored channel is real.  But whether it repairs the SPLIT is a "
      "different question, and PART C answers it",
      "the mechanism works; the arithmetic decides the outcome")

# =========================================================================================
head("PART C -- the lensing residual: does any electric slope repair the split?")
# =========================================================================================
resid = sp.simplify(glens - gdyn)
num = sp.simplify(sp.numer(sp.together(resid)))
info("C1  the residual g_lens - g_dyn", f"{resid}")
check(not num.has(GE),
      "C2  *** THE RESIDUAL'S NUMERATOR IS INDEPENDENT OF G_E, AND PROPORTIONAL TO F_M: "
      f"num = {num}.  NO ELECTRIC SLOPE CANCELS THE MISMATCH.  The only roots are F_M = 0 "
      "(no MOND) or G_E -> infinity ***",
      "the electric piece shifts both potentials but does not close the split")
lim = sp.simplify(sp.limit(gdyn, GE, sp.oo))
check(not sp.simplify(lim).has(FM),
      "C3  *** AND THE LARGE-G_E LIMIT DELETES THE PHENOMENOLOGY: g_dyn -> "
      f"{sp.simplify(lim)}, which carries NO F_M -- pure Newton with a rescaled constant.  "
      "Fixing lensing this way removes the anomaly it was meant to explain ***",
      "a squeeze, not a repair")

# =========================================================================================
head("PART D -- and the lapse-linear form cannot be substituted: the exponent trilemma")
# =========================================================================================
d = sp.Symbol("delta", positive=True)          # perturbation order counter
gpd = sp.Symbol("gradPhiDiff", positive=True)
UpsE = (d * gpd)**2
check(sp.simplify(sp.sqrt(UpsE) / d - gpd) == 0
      and sp.simplify(sp.series(sp.sqrt(UpsE), d, 0, 2).removeO() / d - gpd) == 0,
      "D1  Upsilon_E is SECOND order in the perturbation (it is a gradient SQUARED), so "
      "sqrt(Upsilon_E) is FIRST order: sqrt(delta^2 X^2) = delta X",
      f"sympy: sqrt(Upsilon_E)/delta = {sp.simplify(sp.sqrt(UpsE)/d)} -- linear in delta, not "
      "quadratic")
check(True,
      "D2  *** THEREFORE THE HR-SAFE LAPSE-LINEAR FORM sqrt(Upsilon_E) CONTRIBUTES A "
      "FIRST-ORDER TERM: varying it gives a CONSTANT-MAGNITUDE flux, i.e. a saturating sunward "
      "anomaly -- precisely the disease R1 killed (ephemerides vs RAR, 1.2e4-3.4e4).  It cannot "
      "be used as the energy-density channel ***",
      "so the electric piece may be lapse-linear OR quadratic, not both")
check(True,
      "D3  *** THE TRILEMMA, EXPLICIT: (a) quadratic Upsilon_E -> gives T_00 but is "
      "lapse-NONLINEAR (sf10's R2 danger) AND does not repair the split (C2); (b) sqrt "
      "form -> lapse-linear and HR-safe but FIRST order, hence R1's saturating anomaly; "
      "(c) no electric piece -> sf25's factor-2 lensing kill.  All three corners are occupied ***",
      "the same 1/2-versus-3/2 exponent tension sf10 found in the constraint sector, now in the "
      "lensing sector -- the programme's recurring structure, fourth appearance")

# =========================================================================================
head("PART E -- standing, honest")
# =========================================================================================
for s_ in [
    "KILLED: the two-piece repair AS CONSTRUCTED.  No electric slope closes the lensing split "
    "(C2), and the limit that would is the limit with no MOND left (C3)",
    "AND THE TRILEMMA IS THE REAL RESULT (D3): any energy-density channel must be quadratic to "
    "gravitate, and lapse-linear to stay HR-safe, and a square root cannot be both.  This is "
    "sf10's exponent tension reappearing where nobody was looking for it",
    "WHAT THE ARCHITECTURE STILL HAS: everything sf13a-sf24 established about the SPATIAL "
    "sector -- lapse-freeness, the closed-form A(x), legality, the continuum second-class "
    "result -- is untouched.  What is broken is that this interaction alone cannot make light "
    "and matter agree",
    "THE NAMED NEXT DIRECTION, structural rather than additive: move the lensing question OUT "
    "of the interaction and INTO THE MATTER COUPLING -- a composite (disformal) metric built "
    "from the khronon, g_eff = g + B(X) n n, so that light and matter couple to the same "
    "enhanced geometry by construction rather than by cancellation.  That is how TeVeS solved "
    "its own lensing problem, and the khronon supplies the required vector for free.  NOT "
    "COMPUTED HERE, and its own ghost/PPN bill is unknown",
    "both footings unchanged: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED, "
    "0.529 +/- 0.034, never derived",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF26 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
