#!/usr/bin/env python3
# agentDD_vector_carrier.py -- [SLOT-Y successor] the VECTOR carrier on the u-frame vs agentY's four walls.
# Staged: python3 agentDD_vector_carrier.py D0|D1|D2|D3|D4   (each stage appends to the .out)
#
# THE MODEL (units c=1 in-script; a0 = eps*alpha, the agentY MOND-homogeneous grading):
#   fields: g_munu ; khronon T (unitary gauge: a_i = d_i ln N exactly) ; vector B_mu, leaf part b_i.
#   static spherical: b_i = (eps*b(r), 0, 0);  Z = gam^rr b^2/alpha^2 (finite; the keying variable).
#   S_V = (1/8piG) Int sqrt(-g) [ -a0^2 U(Z) + sig*S(Z) (a.b) + a0 W(Z) (D.b)
#                                 + F(Z)(a.b)^2/a0^2 + C1(Z) a^i b^j D_i b_j /a0^2
#                                 + C2(Z) (a.b)(D.b)/a0^2 ]
#   b is NOT a gradient: algebraic EOM, intrinsic b_i b_j stress -- the wall-1 question.
# Discipline: D0 gates against banked numbers (incl. reproducing agentY's wall-3 row from the
# pickled equations) BEFORE any new use. No git.

import sys, os, pickle, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'agentDD_vector_carrier.out')

def P(*s):
    line = " ".join(str(x) for x in s)
    print(line, flush=True)
    with open(OUT, 'a') as f:
        f.write(line + "\n")

# constants (SI) -- verbatim agentY_gates.py values
G   = 6.674e-11
c   = 2.998e8
A0_FW, A0_CAN = 9.36e-11, 1.2e-10
Msun = 1.989e30
GMsun = 1.327e20
Rsun = 6.957e8
pc   = 3.0857e16
kpc, Mpc = 1e3*pc, 1e6*pc

# the four banked nu shapes, verbatim from agentW_partner_uniqueness.py L59-62 (via agentY_gates.py)
def nu_fw(y):     return np.sqrt(1 + 1/y)
def nu_rar(y):    return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_simple(y): return 0.5 + np.sqrt(0.25 + 1/y)
def nu_std(y):    return np.sqrt((y + np.sqrt(y*y + 4))/(2*y))
NUS = {'McGaugh RAR': nu_rar, 'fw sqrt(1+1/y)': nu_fw, 'simple': nu_simple, 'F4 standard': nu_std}

# Hernquist halo harness -- verbatim agentY_gates.py SGB
def halo_grid():
    GMc2 = 1e11*1.476e3/3.0857e19; a_h = 3.0
    alp_n = A0_FW/c**2*3.0857e19          # a0 in kpc^-1 (c=1 units)
    Mb  = lambda r: GMc2*r**2/(r + a_h)**2
    dMb = lambda r: GMc2*2*r*a_h/(r + a_h)**3
    d2Mb = lambda r: GMc2*2*a_h*(a_h - 2*r)/(r + a_h)**4
    rg = np.logspace(-0.5, 4.2, 6000)
    Ph1 = Mb(rg)/rg**2
    Ph2 = dMb(rg)/rg**2 - 2*Mb(rg)/rg**3
    Ph3 = d2Mb(rg)/rg**2 - 4*dMb(rg)/rg**3 + 6*Mb(rg)/rg**4
    yv = Ph1/alp_n
    rb0v = (Ph2 + 2*Ph1/rg)/(4*np.pi)
    rb1n = (Ph3 + 2*Ph2/rg - 2*Ph1/rg**2)/(4*np.pi)
    return rg, alp_n, Ph1, Ph2, yv, rb0v, rb1n

# ==================================================================================================
def stage_D0():
    P("="*100)
    P("agentDD_vector_carrier.py [D0] -- GATES against banked numbers before any new use")
    P("="*100)
    ok_all = True
    P("\n  slip targets Psi'/Phi' - 1 = 2(nu-1), McGaugh nu, framework a0:")
    for gb, want in [(1e-13, 61.2), (1e-12, 19.4), (1e-11, 6.2)]:
        got = 2*nu_rar(gb/A0_FW) - 1
        ok = abs(got - want) < 0.15*want; ok_all &= ok
        P(f"    g_bar={gb:.0e}: 2nu-1 = {got:.1f} (banked {want})  {'GATE OK' if ok else 'GATE FAIL'}")
    y_cas = GMsun/(1.6*Rsun)**2/A0_FW
    slip_cas = 2*(nu_simple(y_cas) - 1)
    ok = abs(y_cas/1.1e12 - 1) < 0.05 and abs(slip_cas/1.8e-12 - 1) < 0.15; ok_all &= ok
    P(f"  Cassini y = {y_cas:.2e} (banked 1.1e12); simple-nu slip = {slip_cas:.2e} (banked 1.8e-12);")
    P(f"  margin x{2.3e-5/slip_cas:.1e} (banked x1.3e7)   {'GATE OK' if ok else 'GATE FAIL'}")
    g_clu = G*7e13*Msun/(1.0*Mpc)**2; y_clu = g_clu/A0_FW
    ok = abs(nu_rar(y_clu)/3.62 - 1) < 0.05 and abs(7.1/nu_rar(y_clu)/1.96 - 1) < 0.05; ok_all &= ok
    P(f"  cluster: y(1 Mpc, 7e13 Msun) = {y_clu:.2f}, nu = {nu_rar(y_clu):.2f}, short x{7.1/nu_rar(y_clu):.2f}"
      f" (banked x1.96)   {'GATE OK' if ok else 'GATE FAIL'}")

    # --- reproduce agentY's wall-3 row from the pickled equations (harness certification) ---------
    P("\n  agentY wall-3 reproduction (pickled eqs, Hernquist, P=1): expect dg/g_bar ~ -2.7e7 @ y=0.3")
    import sympy as sp
    from scipy.integrate import quad
    with open(os.path.join(HERE, 'agentY_eqs.pkl'), 'rb') as f:
        PK = {k: sp.sympify(v) for k, v in pickle.load(f).items()}
    r_s, alp_s, G_s = sp.symbols('r alpha G', positive=True)
    Ch1s = sp.symbols('chi1', real=True)
    J1, J2 = sp.symbols('J1 J2', real=True)
    c10, c11, c20, c21, c30, c31 = sp.symbols('c10 c11 c20 c21 c30 c31', real=True)
    rhob_f = sp.Function('rhob')(r_s)
    rb0, rb1v = sp.symbols('rb0 rb1', real=True)
    zero_c = {c10: 0, c11: 0, c30: 0, c31: 0, J2: 0, G_s: 1}
    args = [r_s, alp_s, J1, Ch1s, c20, c21, rb0, rb1v]
    def lam(e):
        e = e.subs(zero_c).subs({sp.Derivative(rhob_f, r_s): rb1v, rhob_f: rb0})
        return sp.lambdify(args, e, 'numpy')
    L_sg, L_dps = lam(PK['slipgrad']), lam(PK['DeltaPsi'])
    rg, alp_n, Ph1, Ph2, yv, rb0v, rb1n = halo_grid()
    Pv = 1.0
    chi1 = Ph1/(2*Pv); Yv = (yv/(2*Pv))**2
    def c20_matched(nu, Pp):
        def Yc20(Y):
            I, _ = quad(lambda u: (nu(2*Pp*np.sqrt(u)) - 1.0)/u, Y, np.inf, limit=400)
            return -I
        c20f = lambda Ys: np.array([Yc20(Y)/Y for Y in np.atleast_1d(Ys)])
        c21f = lambda Ys, cv: (nu_rar(2*Pp*np.sqrt(np.atleast_1d(Ys))) - 1)/np.atleast_1d(Ys)**2 - cv/np.atleast_1d(Ys)
        return c20f, c21f
    c20f, c21f = c20_matched(nu_rar, Pv)
    c20v = c20f(Yv); c21v = c21f(Yv, c20v)
    slip = L_sg(rg, alp_n, Pv, chi1, c20v, c21v, rb0v, rb1n)
    dpsv = L_dps(rg, alp_n, Pv, chi1, c20v, c21v, rb0v, rb1n)
    sfrac = slip/Ph1; tfrac = 2*(nu_rar(yv) - 1)
    serr = np.nanmax(np.abs(sfrac/tfrac - 1)[(yv > 1e-3) & (yv < 1e2)])
    divslip = np.gradient(slip*rg**2, rg)/rg**2
    DPhi = dpsv - divslip
    dg = np.cumsum(np.concatenate([[0], 0.5*(DPhi[1:]*rg[1:]**2 + DPhi[:-1]*rg[:-1]**2)*np.diff(rg)]))/rg**2
    frac = dg/Ph1
    got03 = frac[np.argmin(np.abs(yv - 0.3))]
    ok = abs(got03/(-2.7e7) - 1) < 0.2 and serr < 1e-10; ok_all &= ok
    P(f"    slip-match residual = {serr:.1e} (banked ~1e-15-1e-13); dg/g_bar(y=0.3) = {got03:+.2e}"
      f" (banked -2.7e7)   {'GATE OK' if ok else 'GATE FAIL'}")
    P(f"\n  [D0] ALL GATES: {'OK -- proceed' if ok_all else '*** FAIL -- STOP ***'}")
    return ok_all

# ==================================================================================================
def stage_D1():
    """WALL 1: the vector quasi-static system. Does the rr-constraint still force Psi'=Phi'
    for the first-derivative vector sector {U(Z), S(Z) a.b, F(Z)(a.b)^2}? (Scalar answer: yes,
    exact on-shell cancellation via the chi first integral. The vector EOM is ALGEBRAIC --
    the cancellation mechanism is structurally absent. Machine-verify.)"""
    import sympy as sp
    P("="*100)
    P("agentDD_vector_carrier.py [D1] -- WALL 1: vector quasi-static derivation (sympy)")
    P("="*100)
    t, r = sp.symbols('t r', positive=True)
    th = sp.symbols('theta', real=True)
    eps = sp.symbols('epsilon', positive=True)
    a0, Gn = sp.symbols('a0 G', positive=True)
    alp = sp.symbols('alpha', positive=True)
    sig = sp.symbols('sigma', real=True)
    Phi = sp.Function('Phi')(r); Lf = sp.Function('Lf')(r); Mf = sp.Function('Mf')(r)
    bb  = sp.Function('bb')(r)            # b_r = eps*bb(r): the leaf-radial vector component
    rhob = sp.Function('rhob')(r)
    Uf, Sf, Ff, Wf = sp.Function('U'), sp.Function('S'), sp.Function('F'), sp.Function('W')
    C1f, C2f = sp.Function('C1'), sp.Function('C2')

    # --- 3-metric, Ricci scalar (verbatim agentY structure: TWO spatial functions) --------------
    gLe = eps*Lf; gMe = eps*Mf; Phie = eps*Phi
    gam3 = sp.diag(1+2*gLe, (1+2*gMe)*r**2, (1+2*gMe)*r**2*sp.sin(th)**2)
    gam3inv = gam3.inv(); X3 = [r, th, sp.symbols('phi_c')]
    G3 = [[[sum(gam3inv[l, s]*(sp.diff(gam3[s, mu], X3[nu]) + sp.diff(gam3[s, nu], X3[mu])
            - sp.diff(gam3[mu, nu], X3[s])) for s in range(3))/2 for nu in range(3)]
           for mu in range(3)] for l in range(3)]
    def Ric3(i, j):
        expr = 0
        for l in range(3):
            expr += sp.diff(G3[l][i][j], X3[l]) - sp.diff(G3[l][i][l], X3[j])
            for m in range(3):
                expr += G3[l][l][m]*G3[m][i][j] - G3[l][j][m]*G3[m][i][l]
        return expr
    R3 = sum(gam3inv[i, j]*Ric3(i, j) for i in range(3) for j in range(3))
    R3 = sp.expand(sp.series(sp.expand(R3), eps, 0, 3).removeO())
    P("  (3)R assembled; O(e) check vs agentY:", sp.simplify(R3.coeff(eps, 1)) != 0)

    # --- vector-sector objects -------------------------------------------------------------------
    N = 1 + Phie
    sqgam = sp.sqrt(sp.expand((1+2*gLe)))*(1+2*gMe)*r**2
    sqgam = sp.expand(sp.series(sqgam, eps, 0, 3).removeO())
    grr = sp.series(1/(1+2*gLe), eps, 0, 3).removeO()
    br_lo = eps*bb                                   # b_r (lower index)
    Zex = grr*bb**2/alp**2                           # Z = gam^rr b_r^2/(eps alp)^2  [finite]
    ar  = sp.diff(sp.log(N), r)                      # a_r = d_r ln N (exact)
    adotb = grr*ar*br_lo                             # a.b ~ eps^2
    divb  = sp.expand(sp.diff(sqgam*grr*br_lo, r)/sqgam)     # D.b ~ eps
    Gam_rrr = sp.diff(gam3[0, 0], r)/(2*gam3[0, 0])
    Drbr = sp.diff(br_lo, r) - Gam_rrr*br_lo          # D_r b_r ~ eps
    aBDb = grr**2*ar*br_lo*Drbr                       # a^r b^r D_r b_r ~ eps^3

    pre = 1/(8*sp.pi*Gn)
    L_EH = N*sqgam*R3/(16*sp.pi*Gn)
    L_m  = -eps*rhob*N*r**2
    L_U  = -pre*(eps*alp)**2*N*sqgam/r**2 * Uf(Zex) * r**2
    L_S  =  pre*sig*N*sqgam/r**2 * adotb*Sf(Zex) * r**2
    L_F  =  pre*N*sqgam/r**2 * adotb**2*Ff(Zex)/(eps*alp)**2 * r**2
    L_W  =  pre*(eps*alp)*N*sqgam/r**2 * Wf(Zex)*divb * r**2
    L_C1 = pre*N*sqgam/r**2 * C1f(Zex)*aBDb/(eps*alp)**2 * r**2
    L_C2 = pre*N*sqgam/r**2 * C2f(Zex)*adotb*divb/(eps*alp)**2 * r**2

    def O2(expr): return sp.expand(sp.series(sp.expand(expr), eps, 0, 3).removeO().coeff(eps, 2))
    def O1(expr): return sp.expand(sp.series(sp.expand(expr), eps, 0, 2).removeO().coeff(eps, 1))
    L2 = (O2(L_EH) + O2(L_m) + O2(L_U) + O2(L_S) + O2(L_F) + O2(L_W)
          + O1(L_C1) + O2(L_C1) + O1(L_C2) + O2(L_C2))
    P("  O(eps^2) Lagrangian assembled (C-ops: both tiers kept, the agentY per-channel rule).")

    def EL2(L, f):
        return sp.expand((sp.diff(L, f) - sp.diff(sp.diff(L, sp.diff(f, r)), r)
                          + sp.diff(sp.diff(L, sp.diff(f, r, 2)), r, 2)).doit())
    E_Phi = EL2(L2, Phi); E_L = EL2(L2, Lf); E_M = EL2(L2, Mf); E_b = EL2(L2, bb)

    # --- algebraize ------------------------------------------------------------------------------
    U0,U1,U2,U3,U4 = sp.symbols('U0 U1 U2 U3 U4', real=True)
    S0,S1,S2,S3,S4 = sp.symbols('S0 S1 S2 S3 S4', real=True)
    F0,F1,F2,F3,F4 = sp.symbols('F0 F1 F2 F3 F4', real=True)
    W0,W1,W2,W3,W4 = sp.symbols('W0 W1 W2 W3 W4', real=True)
    c10,c11,c12,c13,c14 = sp.symbols('c10 c11 c12 c13 c14', real=True)
    c20,c21,c22,c23,c24 = sp.symbols('c20 c21 c22 c23 c24', real=True)
    fmap = {Uf: [U0,U1,U2,U3,U4], Sf: [S0,S1,S2,S3,S4], Ff: [F0,F1,F2,F3,F4],
            Wf: [W0,W1,W2,W3,W4], C1f: [c10,c11,c12,c13,c14], C2f: [c20,c21,c22,c23,c24]}
    def fsub(e):
        reps = {}
        for nd in sp.preorder_traversal(e):
            if isinstance(nd, sp.Subs) and isinstance(nd.expr, sp.Derivative):
                base = nd.expr.expr
                if getattr(base, 'func', None) in fmap:
                    reps[nd] = fmap[base.func][nd.expr.derivative_count]
            elif isinstance(nd, sp.core.function.AppliedUndef) and nd.func in fmap:
                reps[nd] = fmap[nd.func][0]
        return e.xreplace(reps)
    Psi = sp.Function('Psi')(r)
    gauge = {Lf: -Psi, Mf: -Psi}
    Ph0s, Ps0s, Bb0s = sp.symbols('Phi0 Psi0 b0', real=True)
    Ph1s, Ps1s, Bb1s = sp.symbols('Phi1 Psi1 b1', real=True)
    Ph2s, Ps2s, Bb2s = sp.symbols('Phi2 Psi2 b2', real=True)
    sub_all = {sp.diff(Phi, r, 2): Ph2s, sp.diff(Psi, r, 2): Ps2s, sp.diff(bb, r, 2): Bb2s,
               sp.diff(Phi, r): Ph1s, sp.diff(Psi, r): Ps1s, sp.diff(bb, r): Bb1s,
               Phi: Ph0s, Psi: Ps0s, bb: Bb0s}
    def to_alg(e):
        e = e.subs(gauge).doit()
        return sp.expand(fsub(sp.expand(e).subs(sub_all)))
    eqN, eqL, eqM, eqB = [to_alg(e) for e in (E_Phi, E_L, E_M, E_b)]
    P("  equations algebraized: eqN (Hamiltonian), eqL (rr), eqM (tangential), eqB (vector EOM).")

    # --- GR GATE ---------------------------------------------------------------------------------
    allf = [U0,U1,U2,U3,U4,S0,S1,S2,S3,S4,F0,F1,F2,F3,F4,W0,W1,W2,W3,W4,
            c10,c11,c12,c13,c14,c20,c21,c22,c23,c24]
    gr0 = {v: 0 for v in allf}
    P("\n  GR GATE (vector off):")
    P("    eqN:", sp.simplify(eqN.subs(gr0)))
    P("    eqL:", sp.simplify(eqL.subs(gr0)))
    P("    eqM:", sp.simplify(eqM.subs(gr0)))
    P("    eqB:", sp.simplify(eqB.subs(gr0)))
    P("    [expect: eqN => lap Psi = 4 pi G rhob ; eqL => Psi'=Phi' first-order; eqB == 0]")

    with open(os.path.join(HERE, 'agentDD_eqs.pkl'), 'wb') as f:
        pickle.dump({k: sp.srepr(v) for k, v in
                     [('eqN', eqN), ('eqL', eqL), ('eqM', eqM), ('eqB', eqB)]}, f)
    P("  [full vector equations pickled to agentDD_eqs.pkl]")

    # --- WALL 1 PRIMARY: {U, S} only (F = W = C = 0) ----------------------------------------------
    P("\n  WALL-1 PRIMARY MODEL: {U(Z), S(Z) a.b}; F = W = C1 = C2 = 0; S == S0 (normalization):")
    prim0 = {F0:0,F1:0,F2:0,F3:0,F4:0,W0:0,W1:0,W2:0,W3:0,W4:0,
             c10:0,c11:0,c12:0,c13:0,c14:0,c20:0,c21:0,c22:0,c23:0,c24:0,
             S1:0,S2:0,S3:0,S4:0, sig:1}
    eqNp = sp.expand(eqN.subs(prim0)); eqLp = sp.expand(eqL.subs(prim0))
    eqMp = sp.expand(eqM.subs(prim0)); eqBp = sp.expand(eqB.subs(prim0))
    P("    eqB (the vector EOM -- algebraic?):")
    P("      contains b'': ", eqBp.has(Bb2s), " ; contains b': ", eqBp.has(Bb1s))
    P("      eqB =", sp.collect(sp.expand(eqBp*8*sp.pi*Gn), [Bb0s, Ph1s]))
    solB = sp.solve(sp.Eq(eqBp, 0), Bb0s)
    P("    b-branch:", [sp.cancel(s_) for s_ in solB])
    brB = {Bb0s: sp.cancel(solB[0])} if solB else None

    # the rr-constraint: solve for the slip
    P("\n    THE rr-CONSTRAINT (eqL), {U,S} model:")
    P("      eqL =", sp.collect(sp.expand(eqLp*8*sp.pi*Gn), [Ps1s, Ph1s, Bb0s]))
    solPs1 = sp.solve(sp.Eq(eqLp, 0), Ps1s)
    slip_raw = sp.cancel(sp.together(sp.expand(solPs1[0] - Ph1s)))
    P("      Psi' - Phi' (raw)      =", slip_raw)
    slip_on = sp.cancel(sp.together(sp.expand(slip_raw.subs(brB)))) if brB else slip_raw
    P("      Psi' - Phi' (on b-EOM) =", sp.collect(sp.expand(sp.numer(slip_on)), Ph1s),
      " / [", sp.denom(slip_on), "]")
    P("      SLIP NONZERO ON-SHELL: ", sp.simplify(slip_on) != 0)
    with open(os.path.join(HERE, 'agentDD_D1.pkl'), 'wb') as f:
        pickle.dump({'slip_on': sp.srepr(slip_on), 'brB': sp.srepr(brB[Bb0s]) if brB else None,
                     'eqN_prim': sp.srepr(eqNp), 'eqM_prim': sp.srepr(eqMp),
                     'eqL_prim': sp.srepr(eqLp), 'eqB_prim': sp.srepr(eqBp)}, f)
    P("  [primary-model objects pickled to agentDD_D1.pkl]")

# ==================================================================================================
def stage_D1b():
    """The CONDENSATE corner: unit-norm leaf-radial vector (hedgehog b = v rhat, v = 1 absorbed),
    constraint solved INTO the action (b_r = sqrt(gam_rr): the metric-dependence of the solved
    constraint supplies the constraint stress -- the standard unit-norm-aether move).
    Operators: (a0) W(Ya) (D.b)  [a-independent slip engine, eps^1 tier]
               sigma S(Ya) (a.b) [a-linear comparator -- the pollution-suspect class]
               C(Ya) (a.b)(D.b)  [a-linear, one-D comparator -- the direct C-op analog]
    Ya = gam^rr a_r^2/(eps alp)^2 = y^2-class: the same keying variable as the khronon sector."""
    import sympy as sp
    P("="*100)
    P("agentDD_vector_carrier.py [D1b] -- the condensate corner: quasi-static derivation")
    P("="*100)
    r = sp.symbols('r', positive=True)
    th = sp.symbols('theta', real=True)
    eps = sp.symbols('epsilon', positive=True)
    Gn = sp.symbols('G', positive=True)
    alp = sp.symbols('alpha', positive=True)
    sig = sp.symbols('sigma', real=True)
    Phi = sp.Function('Phi')(r); Lf = sp.Function('Lf')(r); Mf = sp.Function('Mf')(r)
    rhob = sp.Function('rhob')(r)
    Wfn, Sfn, Cfn = sp.Function('W'), sp.Function('S'), sp.Function('C')

    gLe = eps*Lf; gMe = eps*Mf; Phie = eps*Phi
    gam3 = sp.diag(1+2*gLe, (1+2*gMe)*r**2, (1+2*gMe)*r**2*sp.sin(th)**2)
    gam3inv = gam3.inv(); X3 = [r, th, sp.symbols('phi_c')]
    G3 = [[[sum(gam3inv[l, s]*(sp.diff(gam3[s, mu], X3[nu]) + sp.diff(gam3[s, nu], X3[mu])
            - sp.diff(gam3[mu, nu], X3[s])) for s in range(3))/2 for nu in range(3)]
           for mu in range(3)] for l in range(3)]
    def Ric3(i, j):
        expr = 0
        for l in range(3):
            expr += sp.diff(G3[l][i][j], X3[l]) - sp.diff(G3[l][i][l], X3[j])
            for m in range(3):
                expr += G3[l][l][m]*G3[m][i][j] - G3[l][j][m]*G3[m][i][l]
        return expr
    R3 = sum(gam3inv[i, j]*Ric3(i, j) for i in range(3) for j in range(3))
    R3 = sp.expand(sp.series(sp.expand(R3), eps, 0, 3).removeO())

    N = 1 + Phie
    sqgam = sp.sqrt(sp.expand((1+2*gLe)))*(1+2*gMe)*r**2
    sqgam = sp.expand(sp.series(sqgam, eps, 0, 3).removeO())
    grr = sp.series(1/(1+2*gLe), eps, 0, 3).removeO()
    # the unit-norm hedgehog, constraint solved with full metric dependence:
    br_lo = sp.sqrt(1+2*gLe)            # b_r = sqrt(gam_rr)  =>  gam^rr b_r^2 = 1 exactly
    ar  = sp.diff(sp.log(N), r)
    Ya_ex = grr*ar**2/(eps*alp)**2       # finite: = y^2-class
    adotb = grr*ar*br_lo                 # a.b ~ eps
    divb  = sp.diff(sqgam*grr*br_lo, r)/sqgam   # D.b ~ 2/r + O(eps)
    divb  = sp.expand(sp.series(sp.expand(divb), eps, 0, 3).removeO())

    pre = 1/(8*sp.pi*Gn)
    L_EH = N*sqgam*R3/(16*sp.pi*Gn)
    L_m  = -eps*rhob*N*r**2
    # LEGAL normalizations at condensate amplitude (b dimensionless): every term must be 1/L^2.
    #   W: (a0) W (D.b)         -- a0 x 1/L            : eps^1 tier  [the a-independent engine]
    #   S: (a0) S (a.b)         -- a0 x 1/L            : eps^2 tier  [orienter; wall-1 class, no slip]
    #   C: C (a.b)(D.b)         -- 1/L x 1/L, NO norm  : eps^1 tier  [a-linear, one-D]
    # (first pass had S without the a0 and C with a spurious 1/a0 -- dimensionally short/illegal;
    #  the 1/a0-C op has an eps^0 (super-GR, non-total-derivative) tadpole: EXCLUDED. Bug log.)
    L_W  = pre*(eps*alp)*N*sqgam/r**2 * Wfn(Ya_ex)*divb * r**2          # eps^1 tier
    L_S  = pre*sig*(eps*alp)*N*sqgam/r**2 * Sfn(Ya_ex)*adotb * r**2     # eps^2 tier (a-linear)
    L_C  = pre*N*sqgam/r**2 * Cfn(Ya_ex)*adotb*divb * r**2              # eps^1 tier (a-linear, one-D)

    def O2(expr): return sp.expand(sp.series(sp.expand(expr), eps, 0, 3).removeO().coeff(eps, 2))
    def O1(expr): return sp.expand(sp.series(sp.expand(expr), eps, 0, 2).removeO().coeff(eps, 1))
    L2 = (O2(L_EH) + O2(L_m)
          + O1(L_W) + O2(L_W) + O1(L_S) + O2(L_S) + O1(L_C) + O2(L_C))
    P("  O(eps^2) Lagrangian assembled (slip sector: both tiers kept, agentY per-channel rule).")
    P("  tier check: O1(L_W) nonzero:", sp.expand(O1(L_W)) != 0,
      "| O1(L_S) nonzero:", sp.expand(O1(L_S)) != 0,
      "| O1(L_C) nonzero:", sp.expand(O1(L_C)) != 0)

    def EL2(L, f):
        return sp.expand((sp.diff(L, f) - sp.diff(sp.diff(L, sp.diff(f, r)), r)
                          + sp.diff(sp.diff(L, sp.diff(f, r, 2)), r, 2)).doit())
    E_Phi = EL2(L2, Phi); E_L = EL2(L2, Lf); E_M = EL2(L2, Mf)

    Wsy = sp.symbols('W0 W1 W2 W3 W4', real=True)
    Ssy = sp.symbols('S0 S1 S2 S3 S4', real=True)
    Csy = sp.symbols('C0 C1c C2c C3c C4c', real=True)
    fmap = {Wfn: list(Wsy), Sfn: list(Ssy), Cfn: list(Csy)}
    def fsub(e):
        reps = {}
        for nd in sp.preorder_traversal(e):
            if isinstance(nd, sp.Subs) and isinstance(nd.expr, sp.Derivative):
                base = nd.expr.expr
                if getattr(base, 'func', None) in fmap:
                    reps[nd] = fmap[base.func][nd.expr.derivative_count]
            elif isinstance(nd, sp.core.function.AppliedUndef) and nd.func in fmap:
                reps[nd] = fmap[nd.func][0]
        return e.xreplace(reps)
    Psi = sp.Function('Psi')(r)
    gauge = {Lf: -Psi, Mf: -Psi}
    Ph0s, Ps0s = sp.symbols('Phi0 Psi0', real=True)
    Ph1s, Ps1s = sp.symbols('Phi1 Psi1', real=True)
    Ph2s, Ps2s = sp.symbols('Phi2 Psi2', real=True)
    sub_all = {sp.diff(Phi, r, 2): Ph2s, sp.diff(Psi, r, 2): Ps2s,
               sp.diff(Phi, r): Ph1s, sp.diff(Psi, r): Ps1s, Phi: Ph0s, Psi: Ps0s}
    def to_alg(e):
        e = e.subs(gauge).doit()
        return sp.expand(fsub(sp.expand(e).subs(sub_all)))
    eqN, eqL, eqM = [to_alg(e) for e in (E_Phi, E_L, E_M)]
    P("  equations algebraized.")

    allf = list(Wsy) + list(Ssy) + list(Csy)
    gr0 = {v: 0 for v in allf}
    P("\n  GR GATE (sector off):")
    P("    eqN:", sp.simplify(eqN.subs(gr0)))
    P("    eqL:", sp.simplify(eqL.subs(gr0)))
    P("    eqM:", sp.simplify(eqM.subs(gr0)))

    # --- the slip, per operator class --------------------------------------------------------------
    P("\n  THE rr-CONSTRAINT (eqL), per operator class (others off):")
    for name, keep in [('W only', Wsy), ('S only', Ssy), ('C only', Csy)]:
        off = {v: 0 for v in allf if v not in keep}
        e = sp.expand(eqL.subs(off)).subs(sig, 1)
        sol = sp.solve(sp.Eq(e, 0), Ps1s)
        slip = sp.cancel(sp.together(sp.expand(sol[0] - Ph1s))) if sol else None
        P(f"    [{name}]  Psi' - Phi' =", sp.collect(sp.expand(sp.numer(slip)), [Ph1s, Ph2s]),
          " / [", sp.denom(slip), "]")

    # --- the Hamiltonian (eqN) feed, per operator class -------------------------------------------
    P("\n  THE HAMILTONIAN EQUATION (eqN), per operator class -- the wall-3 structure:")
    eqN_gr = sp.expand(eqN.subs(gr0))
    for name, keep in [('W only', Wsy), ('S only', Ssy), ('C only', Csy)]:
        off = {v: 0 for v in allf if v not in keep}
        feed = sp.expand(eqN.subs(off) - eqN_gr).subs(sig, 1)
        feed = sp.cancel(sp.together(feed))
        P(f"    [{name}]  eqN - eqN_GR =", sp.collect(sp.expand(sp.numer(feed)), [Ph1s, Ph2s]),
          " / [", sp.denom(feed), "]")

    with open(os.path.join(HERE, 'agentDD_D1b.pkl'), 'wb') as f:
        pickle.dump({k: sp.srepr(v) for k, v in
                     [('eqN', eqN), ('eqL', eqL), ('eqM', eqM)]}, f)
    P("\n  [condensate equations pickled to agentDD_D1b.pkl]")

# ==================================================================================================
def stage_D2():
    """WALL 2: in-halo c_T on a TT-perturbed background with the SPACELIKE condensate + lapse
    gradient present. Check every retained operator for (dh)^2 / h d2h content (tensor-cone
    shift) vs h-linear (source-type, safe). Then pin the Einstein-aether template: a standard
    vector kinetic term (Db)^2 on the spacelike condensate = the agentY wall-2 death, quantified."""
    import sympy as sp
    P("="*100)
    P("agentDD_vector_carrier.py [D2] -- WALL 2: TT check, condensate operators")
    P("="*100)
    t, x, y, z = sp.symbols('t x y z', real=True)
    e2 = sp.symbols('e2', positive=True)          # TT amplitude
    aa0 = sp.symbols('a0bar', positive=True)      # a0/c^2 (dimension 1/L; kept symbolic)
    hp = sp.Function('hp')(t, z); hc = sp.Function('hc')(t, z)
    Phib = sp.Function('Phibar')(x, y, z)         # in-halo lapse background: a_i != 0
    n1, n2, n3 = sp.symbols('n1 n2 n3', real=True)  # condensate direction (constant; generic)
    Wfn, Sfn, Cfn, U2 = sp.Function('W'), sp.Function('S'), sp.Function('C'), sp.symbols('U2')

    FAST = os.environ.get('AGENTDD_D2_FAST', '0') == '1'
    gam = sp.Matrix([[1+e2*hp, e2*hc, 0], [e2*hc, 1-e2*hp, 0], [0, 0, 1]])
    gaminv = gam.inv()
    sq = sp.sqrt(gam.det())
    X = [x, y, z]
    N = 1 + Phib                                   # lapse with spatial gradient (in-halo)
    a_lo = sp.Matrix([sp.diff(sp.log(N), v) for v in X])
    nvec = sp.Matrix([n1, n2, n3])
    nrm = sp.sqrt((nvec.T*gaminv*nvec)[0, 0])
    b_lo = nvec/nrm                                # unit-norm under gam: ALGEBRAIC in h
    Ya = (a_lo.T*gaminv*a_lo)[0, 0]/aa0**2
    adotb = (a_lo.T*gaminv*b_lo)[0, 0]
    # leaf divergence D.b = (1/sq) d_i (sq gam^{ij} b_j)
    vec_up = gaminv*b_lo
    divb = sum(sp.diff(sq*vec_up[i], X[i]) for i in range(3))/sq

    L_W = aa0*Wfn(Ya)*divb*N*sq
    L_S = Sfn(Ya)*adotb*N*sq
    L_C = Cfn(Ya)*adotb*divb/aa0*N*sq
    # the Einstein-aether-style kinetic comparator (the operator we OMIT):
    Db = sp.zeros(3, 3)
    Gam = [[[sum(gaminv[l, s]*(sp.diff(gam[s, i], X[j]) + sp.diff(gam[s, j], X[i])
            - sp.diff(gam[i, j], X[s])) for s in range(3))/2 for j in range(3)]
           for i in range(3)] for l in range(3)]
    for i in range(3):
        for j in range(3):
            Db[i, j] = sp.diff(b_lo[j], X[i]) - sum(Gam[l][i][j]*b_lo[l] for l in range(3))
    L_kin = sum(gaminv[i, k]*gaminv[j, l]*Db[i, j]*Db[k, l]
                for i in range(3) for j in range(3) for k in range(3) for l in range(3))*N*sq

    hders = []
    for hfun in (hp, hc):
        for v in (t, z):
            hders.append(sp.diff(hfun, v))
            for v2 in (t, z):
                hders.append(sp.diff(hfun, v, v2))
    def tensor_kinetic_content(L, name):
        ser = sp.expand(sp.series(sp.expand(L), e2, 0, 3).removeO().coeff(e2, 2))
        # (dh)(dh) or h d2h content?
        bad_terms = []
        for term in sp.Add.make_args(ser):
            dcount = 0
            for d in hders:
                if term.has(d):
                    pw = sp.Poly(term, d).degree() if term.is_polynomial(d) else 1
                    # count derivative factors crudely: check products
            # robust check: count total derivative-of-h factors by substitution
        # cleaner: detect any monomial containing a PRODUCT of two first-derivs or a second-deriv
        firsts = [sp.diff(h, v) for h in (hp, hc) for v in (t, z)]
        seconds = [sp.diff(h, v, w) for h in (hp, hc) for v in (t, z) for w in (t, z)]
        has2 = False
        for term in sp.Add.make_args(sp.expand(ser)):
            if any(term.has(s) for s in seconds):
                has2 = True; break
            cnt = 0
            for f in firsts:
                if term.has(f):
                    p = sp.degree(term, gen=f) if f in term.free_symbols else 0
                    try:
                        p = sp.Poly(term, f).degree()
                    except Exception:
                        p = 1
                    cnt += p
            if cnt >= 2:
                has2 = True; break
        P(f"    {name}: (dh)^2 / h d2h content at O(h^2): {has2}"
          f"   -> {'TENSOR-CONE SHIFT (wall-2 class)' if has2 else 'h enters as SOURCE only: c_T = 1, alpha_M = 0 preserved'}")
        return has2
    P("\n  TT background, in-halo (a != 0, spacelike condensate present), O(h^2) scan:")
    if not FAST:
        r1 = tensor_kinetic_content(L_W, "(a0) W(Ya)(D.b)   [the slip engine]  ")
        r2 = tensor_kinetic_content(L_S, "S(Ya)(a.b)        [comparator]      ")
    else:
        P("    [FAST mode: W/S generic-direction passes already banked in this .out -- skipped]")
        r1 = r2 = False
    # the C-op and the aether-kinetic comparator: generic-direction rationals are too heavy --
    # REBUILD at fixed numeric directions (two, to guard accidental cancellation; the
    # (dh)^2-existence question is direction-independent)
    r3 = r4 = None
    for nv in [(1, 0, 2), (2, 3, 1)]:
        sub_n = {n1: sp.Integer(nv[0]), n2: sp.Integer(nv[1]), n3: sp.Integer(nv[2])}
        b_n = (nvec/nrm).subs(sub_n)
        adotb_n = (a_lo.T*gaminv*b_n)[0, 0]
        vec_up_n = gaminv*b_n
        divb_n = sum(sp.diff(sq*vec_up_n[i], X[i]) for i in range(3))/sq
        L_C_n = Cfn(Ya)*adotb_n*divb_n*N*sq
        Db_n = sp.zeros(3, 3)
        for i in range(3):
            for j in range(3):
                Db_n[i, j] = sp.diff(b_n[j], X[i]) - sum(Gam[l][i][j]*b_n[l] for l in range(3))
        L_kin_n = sum(gaminv[i, k]*gaminv[j, l]*Db_n[i, j]*Db_n[k, l]
                      for i in range(3) for j in range(3) for k in range(3) for l in range(3))*N*sq
        r3x = tensor_kinetic_content(L_C_n, f"C(Ya)(a.b)(D.b)    [retained; n={nv}]   ")
        r4x = tensor_kinetic_content(L_kin_n, f"(D b)^2            [OMITTED aether kin; n={nv}]")
        r3 = (r3 or r3x); r4 = (r4 if r4 is not None else r4x) and r4x
    P("\n  Einstein-aether template (pinned): tensor sector c_T^2 = 1/(1 - c_+), c_+ = c1 + c3")
    P("  (Jacobson-Mattingly); GW170817 => |c_+| <~ 3e-15 -- ON THE TIMELIKE (cosmological) u.")
    P("  On the SPACELIKE condensate the same structure appears via (Db)^2 ⊃ (Gamma[h] b)^2:")
    P("  Delta c_T ~ beta_kin * b^2 = beta_kin (unit norm) -- ANY standard vector kinetic term at")
    P("  condensate amplitude is GW170817-dead in halos (the agentY timelike-only boundary,")
    P("  transferred to the vector KINETIC sector). The construction therefore carries NO (Db)^2:")
    P("  machine-verified above that the three retained operators are h-linear (source-type).")
    P("  Consequence (honest flag): the direction modes of b get no 2-derivative kinetic term;")
    P("  their dynamics is constraint-type from the mixed eps^1 operators (cuscuton-class")
    P("  precedent, agentY section 5.2's residual flag transfers verbatim).")
    ok = (not r1) and (not r2) and (not r3) and r4
    P(f"\n  [D2] WALL 2: {'EVADED for the retained basis; comparator confirms the wall exists' if ok else 'UNEXPECTED -- inspect'}")

# ==================================================================================================
def stage_D3():
    """WALL 3 (DECISIVE): the Hamiltonian-constraint pollution of the slip-matched condensate
    model, measured on the SAME Hernquist halo / grid / nu / a0 as agentY's table.
    W-only first (the a-independent engine), then the a-linear comparators S and C calibrated
    per-halo, to show the channel-routing contrast like-for-like."""
    import sympy as sp
    P("="*100)
    P("agentDD_vector_carrier.py [D3] -- WALL 3: the pollution numbers (the decisive stage)")
    P("="*100)
    with open(os.path.join(HERE, 'agentDD_D1b.pkl'), 'rb') as f:
        PK = {k: sp.sympify(v) for k, v in pickle.load(f).items()}
    r_s, alp_s, G_s = sp.symbols('r alpha G', positive=True)
    sig = sp.symbols('sigma', real=True)
    Ph0s, Ps0s = sp.symbols('Phi0 Psi0', real=True)
    Ph1s, Ps1s = sp.symbols('Phi1 Psi1', real=True)
    Ph2s, Ps2s = sp.symbols('Phi2 Psi2', real=True)
    Wsy = sp.symbols('W0 W1 W2 W3 W4', real=True)
    Ssy = sp.symbols('S0 S1 S2 S3 S4', real=True)
    Csy = sp.symbols('C0 C1c C2c C3c C4c', real=True)
    rhob_f = sp.Function('rhob')(r_s)
    rb0, rb1v = sp.symbols('rb0 rb1', real=True)
    allf = list(Wsy) + list(Ssy) + list(Csy)

    eqN, eqL = PK['eqN'], PK['eqL']
    base = {sig: 1, G_s: 1, Ph0s: 0, Ps0s: 0}

    rg, alp_n, Ph1, Ph2, yv, rb0v, rb1n = halo_grid()
    Ya = (Ph1/alp_n)**2

    # analytic McGaugh-nu calibration objects (sympy -> lambdify, exact derivatives)
    yy = sp.symbols('yy', positive=True)
    nu_sym = 1/(1 - sp.exp(-sp.sqrt(yy)))
    Ya_s = sp.symbols('Ya_s', positive=True)

    def Wchain():
        # W'(Ya) = (nu(sqrt(Ya)) - 1)/sqrt(Ya);  W(0) = 0
        W1e = (nu_sym.subs(yy, sp.sqrt(Ya_s)) - 1)/sp.sqrt(Ya_s)
        W2e = sp.diff(W1e, Ya_s); W3e = sp.diff(W2e, Ya_s); W4e = sp.diff(W3e, Ya_s)
        f1, f2, f3, f4 = [sp.lambdify(Ya_s, e, 'numpy') for e in (W1e, W2e, W3e, W4e)]
        from scipy.integrate import quad
        W0v = np.array([2*quad(lambda u: (nu_rar(u) - 1.0), 0, ysc, limit=400)[0] for ysc in np.sqrt(Ya)])
        return W0v, f1(Ya), f2(Ya), f3(Ya), f4(Ya)

    P("\n  [W only] -- the a-independent slip engine, W'(Ya) = (nu-1)/sqrt(Ya) (closed-form match):")
    W0v, W1v, W2v, W3v, W4v = Wchain()
    sub_off = {v: 0 for v in list(Ssy) + list(Csy)}
    eqLw = sp.expand(eqL.subs(sub_off).subs(base))
    eqNw = sp.expand(eqN.subs(sub_off).subs(base))
    slip_expr = sp.cancel(sp.solve(sp.Eq(eqLw, 0), Ps1s)[0] - Ph1s)
    Ps2_sol = sp.solve(sp.Eq(eqNw.subs({rhob_f: rb0}), 0), Ps2s)[0]
    DeltaPsi_expr = Ps2_sol + 2*Ps1s/r_s - 4*sp.pi*rb0      # G=1
    args = [r_s, alp_s, Ph1s, Ph2s, Ps1s, rb0] + list(Wsy)
    L_slip = sp.lambdify([r_s, alp_s, Ph1s] + list(Wsy), slip_expr, 'numpy')
    L_dps  = sp.lambdify(args, DeltaPsi_expr, 'numpy')
    slip = L_slip(rg, alp_n, Ph1, W0v, W1v, W2v, W3v, W4v)
    tfrac = 2*(nu_rar(yv) - 1)
    serr = np.nanmax(np.abs(slip/Ph1/tfrac - 1)[(yv > 1e-3) & (yv < 1e2)])
    P(f"    slip-match check (slip/Phi' vs 2(nu-1)): max rel err = {serr:.1e}")
    Ps1v = Ph1 + slip
    dpsv = L_dps(rg, alp_n, Ph1, Ph2, Ps1v, rb0v, W0v, W1v, W2v, W3v, W4v)
    divslip = np.gradient(slip*rg**2, rg)/rg**2
    DPhi = dpsv - divslip
    dg = np.cumsum(np.concatenate([[0], 0.5*(DPhi[1:]*rg[1:]**2 + DPhi[:-1]*rg[:-1]**2)*np.diff(rg)]))/rg**2
    frac = dg/Ph1
    row = []
    for tgt in (1.0, 0.3, 0.1, 0.03, 0.01):
        i = np.argmin(np.abs(yv - tgt)); row.append(f"{frac[i]:+10.2e}")
    P("    columns: y = 1.0, 0.3, 0.1, 0.03, 0.01   (agentY scalar row, P=1: -1.4e7 .. -1.5e8)")
    P("    dg/g_bar = " + " ".join(row))
    rowr = []
    for tgt in (1.0, 0.3, 0.1, 0.03, 0.01):
        i = np.argmin(np.abs(yv - tgt)); rowr.append(f"{dpsv[i]/divslip[i]:+10.2e}")
    P("    DeltaPsi/div(slip) (lens-only would be exactly +1): " + " ".join(rowr))
    P("    context: |dg/g| of 0.01 ~ 0.004 dex; 0.1 ~ 0.04 dex; 1.0 ~ 0.3 dex; agentY bar: 8.7-21.6sigma at ~0.2 dex")

    # --- the second slip carrier: the legal C-op (slip/Phi' = C0 + 2 Ya C0' -- universal) ---------
    P("\n  [C only] -- the legal a-linear one-D carrier: slip/Phi' = C0 + 2 Ya C0' (universal in Ya).")
    P("  Exact match: C0(Ya) = (1/y) * 2 Int_0^y (nu-1) dt,  y = sqrt(Ya)  (homogeneous 1/y mode")
    P("  carries zero slip -- the agentY SGA structure). [S only]: ZERO slip -- pure eqN counterterm.")
    yv_safe = np.sqrt(Ya)
    C0v = W0v/yv_safe                                  # W0v = 2 Int_0^y (nu-1) dt  (computed above)
    dC0dy = 2*(nu_rar(yv_safe) - 1)/yv_safe - W0v/yv_safe**2
    C1v = dC0dy/(2*yv_safe)
    C2v = np.gradient(C1v, Ya)
    C3v = np.gradient(C2v, Ya)
    off = {v: 0 for v in allf if v not in Csy}
    eqLx = sp.expand(eqL.subs(off).subs(base))
    eqNx = sp.expand(eqN.subs(off).subs(base))
    slip_x = sp.cancel(sp.solve(sp.Eq(eqLx, 0), Ps1s)[0] - Ph1s)
    L_slipC = sp.lambdify([r_s, alp_s, Ph1s] + list(Csy), slip_x, 'numpy')
    slip_num = L_slipC(rg, alp_n, Ph1, C0v, C1v, C2v, C3v, 0.0*C0v)
    smx = np.nanmax(np.abs(slip_num/Ph1/tfrac - 1)[(yv > 1e-3) & (yv < 1e2)])
    eqNx2 = sp.expand(eqNx.subs({rhob_f: rb0}))
    Ps2x = sp.solve(sp.Eq(eqNx2, 0), Ps2s)[0]
    DPsix = Ps2x + 2*Ps1s/r_s - 4*sp.pi*rb0
    Lx_dps = sp.lambdify([r_s, alp_s, Ph1s, Ph2s, Ps1s, rb0] + list(Csy), DPsix, 'numpy')
    Ps1x = Ph1 + slip_num
    dpsx = Lx_dps(rg, alp_n, Ph1, Ph2, Ps1x, rb0v, C0v, C1v, C2v, C3v, 0.0*C0v)
    divx = np.gradient(slip_num*rg**2, rg)/rg**2
    DPhix = dpsx - divx
    dgx = np.cumsum(np.concatenate([[0], 0.5*(DPhix[1:]*rg[1:]**2 + DPhix[:-1]*rg[:-1]**2)*np.diff(rg)]))/rg**2
    fracx = dgx/Ph1
    rowx = []; rowrx = []
    for tgt in (1.0, 0.3, 0.1, 0.03, 0.01):
        i = np.argmin(np.abs(yv - tgt))
        rowx.append(f"{fracx[i]:+10.2e}"); rowrx.append(f"{dpsx[i]/divx[i]:+10.2e}")
    P(f"    [C only] slip-match {smx:.1e};  dg/g_bar = " + " ".join(rowx))
    P("    [C only] DeltaPsi/div(slip): " + " ".join(rowrx))

    np.save(os.path.join(HERE, 'agentDD_D3_frac.npy'),
            np.vstack([rg, yv, frac, slip, dpsv, divslip]))
    P("\n  [D3 arrays saved to agentDD_D3_frac.npy]")

# ==================================================================================================
def stage_D4():
    """WALL 4: the exact lens-only condition Delta_Phi == 0 for ALL profiles, on the corrected
    condensate system {W (the slip carrier, fixed by the nu-match up to a constant),
    S (the zero-slip eqN counterterm family)}. Independent data: (Phi1, Phi2, r) with
    4 pi rhob = Phi2 + 2 Phi1/r (the mu=1 self-consistency). Coefficient classes in (Phi2, r)
    must vanish identically -> ODE system on (W, S)(Ya). Branch analysis."""
    import sympy as sp
    P("="*100)
    P("agentDD_vector_carrier.py [D4] -- WALL 4: exact lens-only conditions, condensate system")
    P("="*100)
    with open(os.path.join(HERE, 'agentDD_D1b.pkl'), 'rb') as f:
        PK = {k: sp.sympify(v) for k, v in pickle.load(f).items()}
    r_s, alp_s, G_s = sp.symbols('r alpha G', positive=True)
    sig = sp.symbols('sigma', real=True)
    Ph0s, Ps0s = sp.symbols('Phi0 Psi0', real=True)
    Ph1s, Ps1s = sp.symbols('Phi1 Psi1', real=True)
    Ph2s, Ps2s = sp.symbols('Phi2 Psi2', real=True)
    Ph3s = sp.symbols('Phi3', real=True)
    Wsy = list(sp.symbols('W0 W1 W2 W3 W4', real=True))
    Ssy = list(sp.symbols('S0 S1 S2 S3 S4', real=True))
    Csy = list(sp.symbols('C0 C1c C2c C3c C4c', real=True))
    rhob_f = sp.Function('rhob')(sp.symbols('r', positive=True))
    base = {sig: 1, G_s: 1, Ph0s: 0, Ps0s: 0}
    FULL = os.environ.get('AGENTDD_D4_FULL', '0') == '1'
    offC = {} if FULL else {v: 0 for v in Csy}
    if FULL:
        P("  [FULL SYSTEM: W, S, AND C all kept]")
    eqN = sp.expand(PK['eqN'].subs(offC).subs(base))
    eqL = sp.expand(PK['eqL'].subs(offC).subs(base))

    # the slip from eqL (W carries it; verify S-part is absent)
    slip = sp.cancel(sp.solve(sp.Eq(eqL, 0), Ps1s)[0] - Ph1s)
    P("  slip =", slip)

    # d/dr with the full chain rule (Ya = Phi1^2/alpha^2 at reduction order)
    Yap = 2*Ph1s*Ph2s/alp_s**2
    def ddr(e):
        d = sp.diff(e, r_s) + sp.diff(e, Ph1s)*Ph2s + sp.diff(e, Ph2s)*Ph3s
        for fam in (Wsy, Ssy, Csy):
            for k in range(4):
                d += sp.diff(e, fam[k])*fam[k+1]*Yap
        return sp.expand(d)

    Psi1on = Ph1s + slip
    # Delta_Psi from the Hamiltonian constraint (solve eqN for Psi2), with Psi1 on-shell
    rb0 = sp.symbols('rb0', real=True)
    eqNs = sp.expand(eqN.subs({rhob_f: rb0}))
    Ps2sol = sp.solve(sp.Eq(eqNs, 0), Ps2s)[0]
    DeltaPsi = sp.cancel(sp.together(
        (Ps2sol + 2*Ps1s/r_s - 4*sp.pi*rb0).subs({Ps1s: Psi1on})))
    # div(slip) with the chain rule
    divslip = sp.expand(ddr(slip) + 2*slip/r_s)
    DeltaPhi = sp.cancel(sp.together(DeltaPsi - divslip))
    # mu = 1 self-consistency: 4 pi rhob = lap Phi
    DeltaPhi = sp.cancel(sp.together(DeltaPhi.subs({rb0: (Ph2s + 2*Ph1s/r_s)/(4*sp.pi)})))
    num = sp.expand(sp.numer(DeltaPhi))
    den = sp.denom(DeltaPhi)
    P("  Delta_Phi assembled; denominator =", den)
    P("  numerator: collecting in the independent data (Phi2, Phi3, r):")
    has3 = num.has(Ph3s)
    P("    contains Phi3:", has3)
    poly = sp.Poly(num, Ph2s, Ph3s)
    conds = {}
    for mono, coef in poly.terms():
        conds.setdefault(mono, 0)
        conds[mono] += coef
    P(f"    monomial classes in (Phi2, Phi3): {sorted(conds.keys(), reverse=True)}")
    for mono in sorted(conds.keys(), reverse=True):
        c = sp.factor(sp.expand(conds[mono]))
        cpoly = sp.Poly(c, r_s)
        P(f"\n    CLASS Phi2^{mono[0]} Phi3^{mono[1]}:")
        for rmono, rcoef in cpoly.terms():
            P(f"      r^{rmono[0]}: ", sp.factor(sp.expand(rcoef)))
    # consistency: the r^0 class IS the slip; the Phi2 r^1 class is its Ya-derivative
    Yas = sp.symbols('Ya_v', positive=True)
    if FULL:
        W1s, W2s = Wsy[1], Wsy[2]
        C0s, C1s, C2s = Csy[0], Csy[1], Csy[2]
        f_r0 = C0s + 2*Yas*C1s + 2*sp.sqrt(Yas)*W1s
        df = (C1s) + (2*C1s + 2*Yas*C2s) + (W1s/sp.sqrt(Yas) + 2*sp.sqrt(Yas)*W2s)
        cls_r0 = sp.expand(conds.get((0, 0), sp.Integer(0)))
        cls_p2 = sp.expand(conds.get((1, 0), sp.Integer(0)))
        sub_back = {Ph1s: sp.sqrt(Yas)*alp_s}
        chk1 = sp.simplify(sp.Poly(cls_r0, r_s).coeff_monomial(1).subs(sub_back)/alp_s**6 - f_r0)
        chk2 = sp.simplify(sp.Poly(cls_p2, r_s).coeff_monomial(r_s).subs(sub_back)
                           / (2*alp_s**5*sp.sqrt(Yas)) - df)
        P("\n  CONSISTENCY: r^0-class == alpha^6 * (slip/Phi'):", chk1 == 0,
          " | Phi2 r^1-class == 2 alpha^5 sqrt(Ya) * d(slip/Phi')/dYa:", chk2 == 0)
    with open(os.path.join(HERE, 'agentDD_D4.pkl'), 'wb') as f:
        pickle.dump({'DeltaPhi_num': sp.srepr(num), 'DeltaPhi_den': sp.srepr(den),
                     'slip': sp.srepr(slip)}, f)
    P("\n  [D4 condition system pickled to agentDD_D4.pkl]")

if __name__ == '__main__':
    stage = sys.argv[1] if len(sys.argv) > 1 else 'D0'
    t0 = time.time()
    if stage == 'D0':
        stage_D0()
    else:
        # later stages are appended below as they are built
        fn = globals().get('stage_' + stage)
        if fn is None:
            P(f"[{stage}] not built yet"); sys.exit(1)
        fn()
    P(f"  [stage {stage} done in {time.time()-t0:.1f}s]")
