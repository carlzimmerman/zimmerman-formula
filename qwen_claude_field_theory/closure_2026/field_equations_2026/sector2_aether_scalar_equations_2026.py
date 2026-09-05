#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sector2_aether_scalar_equations_2026.py
=======================================
SECTOR 2 of the first-principles field-equation derivation of THE_GENERALIZED_COMPLETION action
(qwen_claude_field_theory/closure_2026/THE_GENERALIZED_COMPLETION.md):

    (a) the AETHER equation  delta S / delta A^nu = 0  with the multiplier lambda solved,
    (b) the SCALAR equation  delta S / delta phi = 0  as a CONSERVATION LAW  nabla_mu J^mu = 0
        with the current J^mu written out (promotion term F_Q kept: the v9 novelty).

METHOD (derive, do not transcribe).  The aether+scalar bracket of the action is coded in JET SPACE
for FULLY GENERAL fields A^mu(t,x,y,z), phi(t,x,y,z), lambda(t,x,y,z) on a fixed background metric.
The Euler-Lagrange operator is applied mechanically (no hand IBP), divided by sqrt(-g), and compared
term by term with the COVARIANT expressions claimed below, on TWO backgrounds:
    * Minkowski (every derivative structure exercised, Christoffels vanish),
    * FRW with lapse, g = diag(-N(t)^2, a^2, a^2, a^2) (Christoffel/connection structure exercised).
Mutation controls (drop a term, flip a coefficient) MUST make the comparison fail, so the checks
are capable of failing.  All couplings symbolic: K_B, c2, c4, the drag coefficient c_J, the
Y-coefficient c_Y (the doc sets c_J = c_Y = 2 - K_B; they are kept separate so the controls can
tell them apart), and a generic scalar Lagrangian L_s(Y,Q) (polynomial with independent
coefficients, so F_Y and F_Q are structurally distinguishable).  Part 4 then evaluates F_Y, F_Q for
the ACTUAL L_s of the doc (exponential-kernel G, DBI K, bump B, promotion a0^2(Q) = -kappa^2 G K).

CONVENTIONS: signature (-,+,+,+); c = 1; A_mu A^mu = -1 enforced by +lambda(A^2+1);
a^mu = A^nu nabla_nu A^mu; Q = A^mu nabla_mu phi; Y = (g^{mu nu}+A^mu A^nu) nabla_mu phi nabla_nu phi;
G(y) = y^2 + 2(1+y)e^{-y} - 2, y = sqrt(Y)/a0; K(Q) = -M^4 sqrt(1 - mu^2 (Q-Q0)^2/M^4);
a0^2(Q) = -kappa^2 G K(Q) (c=1); B(u) = u/(1+u)^2.

THE BRACKET VARIED (metric held fixed; the Einstein-Hilbert and matter parts do not contain A, phi):
    L = -(K_B/2) F_{mn}F^{mn} + c2 (nabla.A)^2 + c4 a_m a^m + lambda (A_m A^m + 1)
        + 2 c_J a^m nabla_m phi - c_Y Y + L_s(Y, Q),          c_J = c_Y = 2 - K_B in the doc,
    L_s(Y,Q) = (a0^2(Q)/8 pi G) G(sqrt(Y)/a0(Q)) + sigma_K K(Q) + Acal B(Y/a0^2(Q)) (Q-Q0)^2 .
sigma_K is the sign/normalisation with which K enters (the doc writes "-2K(Q)", i.e. sigma_K = -2;
see sector2_conserved_charge_dust_2026.py for why the physically consistent value has sigma_K > 0).

RESULTS (each certified below; SOLID = sympy identity on both backgrounds with controls):
  (E1) aether equation, E_nu = 0, with
       E_nu = 2 K_B nabla^m F_{m nu} - 2 c2 nabla_nu(nabla.A)
              + 2 c4 [ a_r nabla_nu A^r - nabla_m (A^m a_nu) ]
              + 2 c_J [ (nabla_nu A^r) nabla_r phi - nabla_m (A^m nabla_nu phi) ]
              - 2 c_Y Q nabla_nu phi + (2 F_Y Q + F_Q) nabla_nu phi + 2 lambda A_nu
  (E2) lambda = (1/2) A^nu Ecal_nu   (Ecal = E without the lambda term), which on the constraint
       surface (A_m nabla_n A^m = 0) reduces to
       lambda = K_B A^nu nabla^m F_{m nu} - c2 A.nabla(nabla.A) + 2 c4 a^2
                + c_J [ 2 a.nabla phi - nabla_m(Q A^m) ] - c_Y Q^2 + (F_Y Q + F_Q/2) Q ;
       the physical (lambda-free) aether equation is the projection P^mu_nu E^nu = 0.
  (E3) scalar equation  nabla_mu J^mu = 0  with
       J^mu = 2 c_J a^mu + 2 (F_Y - c_Y) (g^{mu nu} + A^mu A^nu) nabla_nu phi + F_Q A^mu ,
       a consequence of shift symmetry (dL/dphi = 0 identically; control: adding V(phi) gives
       nabla_mu J^mu = -V'(phi)).
  (E4) for the doc's L_s:  F_Y = mu(y)/(8 pi G) + Acal (Q-Q0)^2 B'(Y/a0^2)/a0^2,  mu = 1 - e^{-y};
       F_Q = sigma_K K'(Q) + 2 Acal B(Y/a0^2)(Q-Q0)
             - kappa^2 K'(Q) { [e^{-y}(y^2+2y+2) - 2]/(8 pi) - G Acal (Q-Q0)^2 (Y/a0^4) B'(Y/a0^2) } ,
       the last line being the promotion's contribution (proportional to K'(Q) = the charge density
       up to sigma_K: "charge-suppressed", stage 17 A4); it vanishes at Y = 0 (FRW) and tends to
       +kappa^2 K'(Q)/(4 pi) in the Newtonian regime y -> infinity.
"""
import sys
import time
import sympy as sp

T0 = time.time()
FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""), flush=True)
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""), flush=True)


print(__doc__)

# ------------------------------------------------------------------------------------------------
# symbols
# ------------------------------------------------------------------------------------------------
t, x, y, z = sp.symbols("t x y z", real=True)
X = [t, x, y, z]
KB, c2, c4, cJ, cY = sp.symbols("K_B c_2 c_4 c_J c_Y", real=True)
ca, cb, cc, cd, ce, cf = sp.symbols("c_a c_b c_c c_d c_e c_f", real=True)   # generic L_s coeffs


def Ls_generic(Yv, Qv):
    """Generic scalar Lagrangian: independent coefficients so F_Y and F_Q are distinguishable."""
    return ca * Yv ** 2 + cb * Yv * Qv + cc * Qv ** 3 + cd * Qv + ce * Yv + cf * Yv * Qv ** 2


def FY_generic(Yv, Qv):
    return 2 * ca * Yv + cb * Qv + ce + cf * Qv ** 2


def FQ_generic(Yv, Qv):
    return cb * Yv + 3 * cc * Qv ** 2 + cd + 2 * cf * Yv * Qv


# fields as Functions (for the covariant "claim") and as jet symbols (for the EL operator)
A = [sp.Function(f"A{i}")(*X) for i in range(4)]
phi = sp.Function("phi")(*X)
lam = sp.Function("lam")(*X)
Aj = [sp.Symbol(f"A{i}") for i in range(4)]
dAj = [[sp.Symbol(f"A{i}_{a}") for a in range(4)] for i in range(4)]
phij = sp.Symbol("phi")
dphij = [sp.Symbol(f"phi_{a}") for a in range(4)]
lamj = sp.Symbol("lam")
JET2FUN = {Aj[i]: A[i] for i in range(4)}
JET2FUN.update({dAj[i][a]: sp.diff(A[i], X[a]) for i in range(4) for a in range(4)})
JET2FUN[phij] = phi
JET2FUN.update({dphij[a]: sp.diff(phi, X[a]) for a in range(4)})
JET2FUN[lamj] = lam


def christoffel(g, ginv):
    Gam = [[[sp.S(0)] * 4 for _ in range(4)] for _ in range(4)]
    for m in range(4):
        for n in range(4):
            for r in range(4):
                s = 0
                for sg in range(4):
                    if ginv[m, sg] == 0:
                        continue
                    s += ginv[m, sg] * (sp.diff(g[sg, n], X[r]) + sp.diff(g[sg, r], X[n])
                                        - sp.diff(g[n, r], X[sg]))
                Gam[m][n][r] = sp.simplify(s / 2)
    return Gam


class Geometry:
    """All building blocks on a fixed diagonal background, for either jet or Function fields."""

    def __init__(self, g):
        self.g = g
        self.ginv = g.inv()
        self.sqrtg = sp.sqrt(-g.det())
        self.Gam = christoffel(g, self.ginv)

    def blocks(self, Aup, dA, ph, dph, second=None):
        """Aup[i]: A^i; dA[i][a] = d_a A^i; dph[a] = d_a phi.  Returns dict of covariant objects.
        If `second` is None the fields are jet symbols (first derivatives only)."""
        g, ginv, Gam = self.g, self.ginv, self.Gam
        Alow = [sum(g[m, n] * Aup[n] for n in range(4)) for m in range(4)]
        # nabla_n A^m
        DA = [[dA[m][n] + sum(Gam[m][n][r] * Aup[r] for r in range(4)) for m in range(4)]
              for n in range(4)]                                    # DA[n][m] = nabla_n A^m
        aup = [sum(Aup[n] * DA[n][m] for n in range(4)) for m in range(4)]
        alow = [sum(g[m, n] * aup[n] for n in range(4)) for m in range(4)]
        # F_{mn} = d_m A_n - d_n A_m  (A_n = g_{nr} A^r; metric depends on t only)
        dAlow = [[sum(sp.diff(g[n, r], X[m]) * Aup[r] + g[n, r] * dA[r][m] for r in range(4))
                  for n in range(4)] for m in range(4)]              # dAlow[m][n] = d_m A_n
        F = [[dAlow[m][n] - dAlow[n][m] for n in range(4)] for m in range(4)]
        Fup = [[sum(ginv[m, r] * ginv[n, s] * F[r][s] for r in range(4) for s in range(4))
                for n in range(4)] for m in range(4)]
        F2 = sum(F[m][n] * Fup[m][n] for m in range(4) for n in range(4))
        divA = sum(DA[m][m] for m in range(4))
        Q = sum(Aup[m] * dph[m] for m in range(4))
        P = [[ginv[m, n] + Aup[m] * Aup[n] for n in range(4)] for m in range(4)]
        Y = sum(P[m][n] * dph[m] * dph[n] for m in range(4) for n in range(4))
        a2 = sum(alow[m] * aup[m] for m in range(4))
        AA = sum(Alow[m] * Aup[m] for m in range(4))
        adphi = sum(aup[m] * dph[m] for m in range(4))
        return dict(Alow=Alow, DA=DA, aup=aup, alow=alow, F=F, Fup=Fup, F2=F2, divA=divA,
                    Q=Q, P=P, Y=Y, a2=a2, AA=AA, adphi=adphi)


def lagrangian(b, lamv, Ls):
    return (-(KB / 2) * b["F2"] + c2 * b["divA"] ** 2 + c4 * b["a2"] + lamv * (b["AA"] + 1)
            + 2 * cJ * b["adphi"] - cY * b["Y"] + Ls(b["Y"], b["Q"]))


def claim_aether(geo, b, lamv, FY, FQ, dph, ddph, mutate=None):
    """The covariant aether equation E_nu (lower index) built from Function-valued blocks."""
    g, ginv, Gam, sqrtg = geo.g, geo.ginv, geo.Gam, geo.sqrtg
    Aup, DA, aup, alow, Fup, divA, Q = (b["A"], b["DA"], b["aup"], b["alow"], b["Fup"],
                                        b["divA"], b["Q"])
    # nabla_m F^{m b} = (1/sqrtg) d_m (sqrtg F^{m b})
    divF_up = [sum(sp.diff(sqrtg * Fup[m][bb], X[m]) for m in range(4)) / sqrtg for bb in range(4)]
    divF_low = [sum(g[n, bb] * divF_up[bb] for bb in range(4)) for n in range(4)]
    # nabla_m a_n  and  nabla_m nabla_n phi  (covariant derivatives of covectors)
    Da = [[sp.diff(alow[n], X[m]) - sum(Gam[r][m][n] * alow[r] for r in range(4)) for n in range(4)]
          for m in range(4)]
    Dph = [[ddph[m][n] - sum(Gam[r][m][n] * dph[r] for r in range(4)) for n in range(4)]
           for m in range(4)]
    E = []
    for n in range(4):
        T1 = 2 * KB * divF_low[n]
        T2 = -2 * c2 * sp.diff(divA, X[n])
        T3a = sum(alow[r] * DA[n][r] for r in range(4))
        T3b = divA * alow[n] + sum(Aup[m] * Da[m][n] for m in range(4))     # nabla_m (A^m a_n)
        T3 = 2 * c4 * (T3a - T3b)
        T4 = 2 * lamv * b["Alow"][n]
        T5a = sum(DA[n][r] * dph[r] for r in range(4))
        T5b = divA * dph[n] + sum(Aup[m] * Dph[m][n] for m in range(4))    # nabla_m (A^m d_n phi)
        T5 = 2 * cJ * (T5a - T5b)
        T6 = -2 * cY * Q * dph[n]
        T7 = (2 * FY * Q + FQ) * dph[n]
        if mutate == "drop_FQ":
            T7 = 2 * FY * Q * dph[n]
        elif mutate == "drop_c4_grad":
            T3 = 2 * c4 * (-T3b)
        elif mutate == "flip_c2":
            T2 = -T2
        elif mutate == "drop_cY":
            T6 = 0
        elif mutate == "KB_coeff_1":
            T1 = KB * divF_low[n]
        elif mutate == "drop_drag_grad":
            T5 = 2 * cJ * (-T5b)
        E.append(T1 + T2 + T3 + T4 + T5 + T6 + T7)
    return E


def claim_current(b, FY, FQ, dph, mutate=None):
    Aup, aup, P, Q = b["A"], b["aup"], b["P"], b["Q"]
    J = []
    for m in range(4):
        drag = 2 * cJ * aup[m]
        grad = 2 * (FY - cY) * sum(P[m][n] * dph[n] for n in range(4))
        chg = FQ * Aup[m]
        if mutate == "drop_drag":
            drag = 0
        elif mutate == "drop_FQ":
            chg = 0
        elif mutate == "P_to_g":
            grad = 2 * (FY - cY) * sum(b["ginv"][m, n] * dph[n] for n in range(4))
        J.append(drag + grad + chg)
    return J


def run_background(name, g, Ls, FY, FQ):
    print()
    print("=" * 100)
    print(f"BACKGROUND: {name}   g = diag({g[0,0]}, {g[1,1]}, {g[2,2]}, {g[3,3]})")
    print("=" * 100)
    geo = Geometry(g)
    sqrtg = geo.sqrtg
    # ---- jet-space Lagrangian density and EL operator -------------------------------------------
    bj = geo.blocks(Aj, dAj, phij, dphij)
    Ldens = sp.expand(sqrtg * lagrangian(bj, lamj, Ls))
    t1 = time.time()
    EL_A = []
    for n in range(4):
        e = sp.diff(Ldens, Aj[n])
        for a in range(4):
            e -= sp.diff(sp.diff(Ldens, dAj[n][a]).subs(JET2FUN), X[a])
        EL_A.append(sp.expand(e.subs(JET2FUN) / sqrtg))
    e = sp.diff(Ldens, phij)
    dL_dphi = e                                                        # shift-symmetry witness
    for a in range(4):
        e -= sp.diff(sp.diff(Ldens, dphij[a]).subs(JET2FUN), X[a])
    EL_phi = sp.expand(e.subs(JET2FUN) / sqrtg)
    EL_lam = sp.expand(sp.diff(Ldens, lamj).subs(JET2FUN) / sqrtg)
    info(f"jet-space Euler-Lagrange operator applied ({time.time()-t1:.1f}s); "
         f"|L| = {len(sp.Add.make_args(Ldens))} terms")

    # ---- covariant claim built from Function-valued fields ---------------------------------------
    dA_fun = [[sp.diff(A[i], X[a]) for a in range(4)] for i in range(4)]
    dph = [sp.diff(phi, X[a]) for a in range(4)]
    ddph = [[sp.diff(phi, X[m], X[n]) for n in range(4)] for m in range(4)]
    bf = geo.blocks(A, dA_fun, phi, dph)
    bf["A"] = A
    bf["ginv"] = geo.ginv
    FYv, FQv = FY(bf["Y"], bf["Q"]), FQ(bf["Y"], bf["Q"])

    def zero(expr):
        e = sp.expand(expr)
        if e == 0:
            return True
        return sp.simplify(e) == 0

    # constraint equation
    check(zero(EL_lam - (bf["AA"] + 1)), "E_lambda:  A_mu A^mu + 1 = 0 (the multiplier enforces unit norm)")

    # (E1) aether equation
    Ecl = claim_aether(geo, bf, lam, FYv, FQv, dph, ddph)
    ok = all(zero(EL_A[n] - Ecl[n]) for n in range(4))
    check(ok, "(E1) delta S/delta A^nu == 2K_B nabla^m F_{m nu} - 2c2 nabla_nu(nabla.A) "
              "+ 2c4[a_r nabla_nu A^r - nabla_m(A^m a_nu)] + 2c_J[(nabla_nu A^r)d_r phi - nabla_m(A^m d_nu phi)] "
              "- 2c_Y Q d_nu phi + (2F_Y Q + F_Q) d_nu phi + 2 lambda A_nu   [all four components]")
    for mut in ["drop_FQ", "drop_c4_grad", "flip_c2", "drop_cY", "KB_coeff_1", "drop_drag_grad"]:
        Em = claim_aether(geo, bf, lam, FYv, FQv, dph, ddph, mutate=mut)
        bad = any(not zero(EL_A[n] - Em[n]) for n in range(4))
        check(bad, f"      control [{mut}]: the mutated aether equation FAILS the comparison")

    # (E2) lambda
    Ecal = [Ecl[n] - 2 * lam * bf["Alow"][n] for n in range(4)]
    lam_sol = sp.Rational(1, 2) * sum(A[n] * Ecal[n] for n in range(4))
    # the unsimplified solve is an identity: substituting back, A^nu E_nu == 0 for any field config
    resid = sum(A[n] * Ecl[n] for n in range(4)).subs(lam, lam_sol)
    check(zero(resid), "(E2) lambda = (1/2) A^nu Ecal_nu solves A^nu E_nu = 0 identically (off the constraint too)")
    # the simplified form on the constraint surface A.A = -1  (=> A_m nabla_n A^m = 0)
    divF_up = [sum(sp.diff(sqrtg * bf["Fup"][m][bb], X[m]) for m in range(4)) / sqrtg for bb in range(4)]
    divF_low = [sum(g[n, bb] * divF_up[bb] for bb in range(4)) for n in range(4)]
    divQA = sum(sp.diff(sqrtg * bf["Q"] * A[m], X[m]) for m in range(4)) / sqrtg
    lam_simp = (KB * sum(A[n] * divF_low[n] for n in range(4))
                - c2 * sum(A[n] * sp.diff(bf["divA"], X[n]) for n in range(4))
                + 2 * c4 * bf["a2"]
                + cJ * (2 * bf["adphi"] - divQA)
                - cY * bf["Q"] ** 2 + (FYv * bf["Q"] + FQv / 2) * bf["Q"])
    # impose the constraint: A^0 = sqrt(1 + g_ij A^i A^j)/N  (exact), then compare
    A0c = sp.sqrt(1 + sum(g[i, i] * A[i] ** 2 for i in range(1, 4))) / sp.sqrt(-g[0, 0])
    d = (lam_sol - lam_simp).subs(A[0], A0c).doit()
    d = sp.simplify(d)
    if d != 0:
        # fall back to exact random-rational spot checks (still capable of failing)
        import random
        random.seed(7)
        atoms = sorted(d.atoms(sp.Derivative) | d.atoms(sp.Function), key=str)
        vals = {}
        ok2 = True
        for trial in range(3):
            sub = {}
            for at in d.atoms(sp.Derivative):
                sub[at] = sp.Rational(random.randint(-9, 9), random.randint(1, 5))
            for fn in [A[1], A[2], A[3], phi, lam]:
                sub[fn] = sp.Rational(random.randint(-9, 9), random.randint(1, 5))
            for fn in g.atoms(sp.Function):
                sub[fn] = sp.Rational(random.randint(1, 9), random.randint(1, 5))
            for at in list(d.atoms(sp.Derivative)):
                pass
            val = sp.simplify(d.subs(sub).subs({t: sp.Rational(1, 3), x: sp.Rational(2, 7),
                                                y: sp.Rational(-1, 5), z: sp.Rational(3, 11)}))
            ok2 = ok2 and (val == 0)
        d = 0 if ok2 else d
    check(d == 0, "(E2) on the constraint surface: lambda = K_B A^nu nabla^m F_{m nu} - c2 A.nabla(nabla.A) + 2c4 a^2 "
                  "+ c_J[2 a.dphi - nabla_m(Q A^m)] - c_Y Q^2 + (F_Y Q + F_Q/2) Q")
    # control: the simplified lambda is NOT an identity off the constraint (the A.nabla A = 0 step matters)
    d_off = sp.expand(lam_sol - lam_simp)
    check(d_off != 0, "      control: the simplified lambda differs OFF the constraint surface (identity used: A_m nabla_n A^m = 0)")

    # (E3) scalar equation as a conservation law
    check(zero(dL_dphi), "(E3) dL/dphi == 0 identically: phi enters only through nabla phi (shift symmetry)")
    Jcl = claim_current(bf, FYv, FQv, dph)
    divJ = sum(sp.diff(sqrtg * Jcl[m], X[m]) for m in range(4)) / sqrtg
    check(zero(EL_phi + divJ), "(E3) delta S/delta phi == -nabla_mu J^mu with "
                               "J^mu = 2c_J a^mu + 2(F_Y - c_Y)(g^{mu nu}+A^mu A^nu) d_nu phi + F_Q A^mu")
    for mut in ["drop_drag", "drop_FQ", "P_to_g"]:
        Jm = claim_current(bf, FYv, FQv, dph, mutate=mut)
        divJm = sum(sp.diff(sqrtg * Jm[m], X[m]) for m in range(4)) / sqrtg
        check(not zero(EL_phi + divJm), f"      control [{mut}]: the mutated current FAILS the comparison")
    # shift-breaking control: L -> L - V(phi)
    V = sp.Function("V")
    Ldens_V = Ldens - sqrtg * V(phij)
    eV = sp.diff(Ldens_V, phij)
    for a in range(4):
        eV -= sp.diff(sp.diff(Ldens_V, dphij[a]).subs(JET2FUN), X[a])
    EL_phi_V = sp.expand(eV.subs(JET2FUN) / sqrtg)
    check(zero(EL_phi_V + divJ + sp.Derivative(V(phi), phi).doit().subs(phij, phi)) or
          zero(EL_phi_V + divJ + sp.diff(V(phij), phij).subs(phij, phi)),
          "      control: with an explicit potential V(phi) the law becomes nabla_mu J^mu = -V'(phi) != 0 "
          "(conservation <=> shift symmetry)")
    print(f"  ({time.time()-T0:.1f}s elapsed)")
    return geo, bf, Ecl, Jcl, lam_simp


# ================================================================================================
print("=" * 100)
print("PART 1-3 -- derivation by mechanical Euler-Lagrange on general fields, two backgrounds")
print("=" * 100)
gM = sp.diag(-1, 1, 1, 1)
run_background("Minkowski", gM, Ls_generic, FY_generic, FQ_generic)

Nf = sp.Function("N", positive=True)(t)
af = sp.Function("a", positive=True)(t)
gF = sp.diag(-Nf ** 2, af ** 2, af ** 2, af ** 2)
geoF, bF, EclF, JclF, lamF = run_background("FRW with lapse", gF, Ls_generic, FY_generic, FQ_generic)

# ================================================================================================
print()
print("=" * 100)
print("PART 3b -- the FRW reduction of the current: J^0 sqrt(-g) = a^3 F_Q(0, Q), a.dphi = 0, Y = 0")
print("=" * 100)
phib = sp.Function("phibar")(t)
frw_sub = {A[0]: 1 / Nf, A[1]: 0, A[2]: 0, A[3]: 0, phi: phib}
JF = [sp.simplify(Jm.subs(frw_sub).doit()) for Jm in JclF]
Yf = sp.simplify(bF["Y"].subs(frw_sub).doit())
Qf = sp.simplify(bF["Q"].subs(frw_sub).doit())
af_ = [sp.simplify(am.subs(frw_sub).doit()) for am in bF["aup"]]
check(Yf == 0 and all(v == 0 for v in af_), "on FRW with the comoving unit aether: Y = 0 and a^mu = 0 (geodesic aether)",
      f"Q = {Qf}")
check(sp.simplify(JF[0] * Nf * af ** 3 - af ** 3 * FQ_generic(0, Qf)) == 0 and all(v == 0 for v in JF[1:]),
      "sqrt(-g) J^0 = a^3 F_Q(Y=0, Q = phidot/N),  J^i = 0:  nabla_mu J^mu = 0  <=>  d/dt[a^3 F_Q(0,Q)] = 0")
# the FRW aether equation: spatial components vanish identically, time component fixes lambda
EF = [sp.simplify(En.subs(frw_sub).doit()) for En in EclF]
check(all(v == 0 for v in EF[1:]), "FRW: spatial aether equations vanish identically (comoving aether is a solution)")
lamFRW = sp.solve(EF[0], lam)[0]
print("  lambda on FRW =", sp.simplify(lamFRW))

# ================================================================================================
print()
print("=" * 100)
print("PART 4 -- F_Y and F_Q for the ACTUAL L_s of the doc, promotion included (the v9 novelty)")
print("=" * 100)
Ys, Qs, kap, G, Ac, Q0, M4, mu, sK = sp.symbols("Y Q kappa G Acal Q_0 M4 mu sigma_K", positive=True)
a0sq = sp.Symbol("a0sq", positive=True)      # a0^2 treated as an independent slot first
Kfun = -M4 * sp.sqrt(1 - mu ** 2 * (Qs - Q0) ** 2 / M4)          # beta = 1 DBI
a0sq_of_Q = -kap ** 2 * G * Kfun                                   # the promotion (INPUT)
ys = sp.sqrt(Ys) / sp.sqrt(a0sq)
Gk = ys ** 2 + 2 * (1 + ys) * sp.exp(-ys) - 2
Bf = lambda u: u / (1 + u) ** 2
Ls_slot = a0sq / (8 * sp.pi * G) * Gk + sK * Kfun + Ac * Bf(Ys / a0sq) * (Qs - Q0) ** 2
Ls_real = Ls_slot.subs(a0sq, a0sq_of_Q)

# F_Y
FY_real = sp.diff(Ls_real, Ys)
yv = sp.Symbol("y", positive=True)
FY_target = (1 - sp.exp(-yv)) / (8 * sp.pi * G) + Ac * (Qs - Q0) ** 2 * sp.diff(Bf(yv ** 2), yv) / (2 * yv) / a0sq
d = sp.simplify((FY_real.subs(a0sq_of_Q, a0sq) - FY_target).subs(Ys, yv ** 2 * a0sq))
check(d == 0, "(E4) F_Y = mu(y)/(8 pi G) + Acal (Q-Q0)^2 B'(Y/a0^2)/a0^2,  mu(y) = 1 - e^{-y}, y = sqrt(Y)/a0(Q)",
      "the spec's primitive: dG/dY = (1 - e^{-y})/a0^2")

# F_Q by the chain rule through the promotion
FQ_real = sp.diff(Ls_real, Qs)
FQ_chain = (sp.diff(Ls_slot, Qs) + sp.diff(Ls_slot, a0sq) * sp.diff(a0sq_of_Q, Qs)).subs(a0sq, a0sq_of_Q)
check(sp.simplify(FQ_real - FQ_chain) == 0,
      "(E4) F_Q = dL_s/dQ|_{a0 fixed} + (dL_s/d a0^2)(d a0^2/dQ): the promotion term is a chain-rule piece")
dLG_da0sq = sp.simplify(sp.diff(a0sq / (8 * sp.pi * G) * Gk, a0sq).subs(Ys, yv ** 2 * a0sq))
target = (sp.exp(-yv) * (yv ** 2 + 2 * yv + 2) - 2) / (8 * sp.pi * G)
check(sp.simplify(dLG_da0sq - target) == 0,
      "(E4) d/d(a0^2)[(a0^2/8piG) G(sqrt(Y)/a0)] = [e^{-y}(y^2+2y+2) - 2]/(8 pi G)  (= G - y G'/2, closed form)")
check(sp.series(target * 8 * sp.pi * G, yv, 0, 4).removeO() == -yv ** 3 / 3 and sp.limit(target * 8 * sp.pi * G, yv, sp.oo) == -2,
      "(E4) that bracket is -y^3/3 as y -> 0 (deep MOND; vanishes on FRW, Y = 0) and -> -2 as y -> inf (Newtonian)")
Kp = sp.diff(Kfun, Qs)
promo = sp.simplify((sp.diff(Ls_slot, a0sq) * sp.diff(a0sq_of_Q, Qs)).subs(a0sq, a0sq_of_Q))
promo_target = -kap ** 2 * Kp * (target - G * Ac * (Qs - Q0) ** 2 * (Ys / a0sq ** 2)
                                 * sp.diff(Bf(sp.Symbol("u")), sp.Symbol("u")).subs(sp.Symbol("u"), Ys / a0sq))
d = sp.simplify((promo.subs(a0sq_of_Q, a0sq) - promo_target.subs(a0sq_of_Q, a0sq)).subs(Ys, yv ** 2 * a0sq))
check(d == 0, "(E4) promotion piece of F_Q = -kappa^2 K'(Q) { [e^{-y}(y^2+2y+2)-2]/(8 pi) - G Acal (Q-Q0)^2 (Y/a0^4) B'(Y/a0^2) }",
      "proportional to K'(Q) = (charge density)/sigma_K: charge-suppressed backreaction (stage 17 A4)")
FQ_Y0 = sp.simplify(FQ_real.subs(Ys, 0))
check(sp.simplify(FQ_Y0 - sK * Kp) == 0,
      "(E4) F_Q(Y=0, Q) = sigma_K K'(Q) EXACTLY: on FRW neither the promotion nor the bump touches the charge",
      "G(0) = 0 and B(0) = 0")
ratio_newt = sp.simplify(sp.limit((promo / (sK * Kp)).subs(Ac, 0).subs(Ys, yv ** 2 * a0sq).subs(a0sq_of_Q, a0sq), yv, sp.oo))
check(sp.simplify(ratio_newt - kap ** 2 / (4 * sp.pi * sK)) == 0,
      f"(E4) Newtonian-regime renormalisation of the charge-to-field relation: F_Q -> sigma_K K'(Q)[1 + kappa^2/(4 pi sigma_K)]; "
      f"at kappa = 1/2, sigma_K = 1 that is 1 + 1/(16 pi) = {float(1 + 1/(16*sp.pi)):.4f}",
      "a smooth, y-dependent 2% renormalisation between the FRW (y=0) and Newtonian (y>>1) values")

print()
print("=" * 100)
print("THE DISPLAYED EQUATIONS (Sector 2)")
print("=" * 100)
print(r"""
  (E1)  AETHER EQUATION  (delta S / delta A^nu = 0), with c_J = c_Y = 2 - K_B in the doc's action:
        2 K_B nabla^mu F_{mu nu}  -  2 c2 nabla_nu (nabla_mu A^mu)
        + 2 c4 [ a_rho nabla_nu A^rho - nabla_mu (A^mu a_nu) ]                 <- c4 a^2 term
        + 2(2-K_B) [ (nabla_nu A^rho) nabla_rho phi - nabla_mu (A^mu nabla_nu phi) ]   <- drag term
        - 2(2-K_B) Q nabla_nu phi  +  (2 F_Y Q + F_Q) nabla_nu phi  +  2 lambda A_nu  =  0
        The c4 term and the drag term are the SAME operator, a^mu V_mu with V = c4 a + (2-K_B) nabla phi:
        both enter through delta a^mu = (nabla_nu A^mu) delta A^nu + A^nu nabla_nu delta A^mu, i.e. as
        (nabla_nu A^rho) V_rho - nabla_mu (A^mu V_nu); the drag therefore puts nabla nabla phi into the
        aether equation (and, reciprocally, nabla nabla A into the scalar equation through J ⊃ 2(2-K_B) a^mu).

  (E2)  MULTIPLIER  lambda = (1/2) A^nu Ecal_nu  (Ecal = E1 without the lambda term); on A.A = -1:
        lambda = K_B A^nu nabla^mu F_{mu nu} - c2 A^nu nabla_nu (nabla.A) + 2 c4 a^2
                 + (2-K_B) [ 2 a^mu nabla_mu phi - nabla_mu (Q A^mu) ] - (2-K_B) Q^2 + (F_Y Q + F_Q/2) Q .
        Physical aether equation = the transverse projection (g^mu_nu + A^mu A_nu) E^nu = 0 (3 equations).

  (E3)  SCALAR EQUATION = CONSERVATION LAW  nabla_mu J^mu = 0,
        J^mu = 2(2-K_B) a^mu  +  2 [ F_Y - (2-K_B) ] (g^{mu nu} + A^mu A^nu) nabla_nu phi  +  F_Q A^mu .
        On FRW (comoving aether): a^mu = 0, Y = 0, so sqrt(-g) J^0 = a^3 F_Q(0,Q) = a^3 sigma_K K'(Q):
        d/dt [ a^3 sigma_K K'(Q) ] = 0  -- the conserved shift charge.

  (E4)  F_Y = (1 - e^{-y})/(8 pi G) + Acal (Q-Q0)^2 B'(Y/a0^2)/a0^2 ,
        F_Q = sigma_K K'(Q) + 2 Acal B(Y/a0^2) (Q-Q0)
              - kappa^2 K'(Q) { [e^{-y}(y^2+2y+2) - 2]/(8 pi) - G Acal (Q-Q0)^2 (Y/a0^4) B'(Y/a0^2) } ,
        with y = sqrt(Y)/a0(Q), a0^2(Q) = -kappa^2 G K(Q)  [the promotion: INPUT, a definitional choice].
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed   ({time.time()-T0:.1f}s)")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
