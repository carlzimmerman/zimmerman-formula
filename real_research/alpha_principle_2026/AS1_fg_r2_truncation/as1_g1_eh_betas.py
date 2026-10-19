"""AS1 gate G1 (EH limit of the derivation, symbolic) and the gauge/convention selection.

Usage: python3 as1_g1_eh_betas.py
Exit 0 iff the machinery validations pass AND G1 selects a gauge/convention combination; exit 1 otherwise (in particular when
G1 fails for all four declared combinations, which makes the lane NOT COMPLETED).

Derivation (as frozen in AS1_PREREGISTRATION.md):
 * Truncation f(R) = (2 Lambda - R)/(16 pi G) + b R^2; G1 is the EH limit, implemented as the EH truncation (b = 0 and no d_t b terms).
 * Background S^4, York decomposition h = h^TT + D xi + D xi + (DD - g D^2/4) sigma + g h/4; second variation of int sqrt(g) f(R) in York
   variables, gauge fixing and ghosts transcribed from Codello-Percacci-Rahmede arXiv:0805.2909 sec. VII eqs (grop), (xiquadratic),
   (scalarpart), (ghop) with d = 4.  Background harmonic gauge chi_nu = D^mu h_mu nu - (1+rho)/4 D_nu h, rho = 1 (= Eichhorn-Versteegen beta = 1),
   gauge-fixing weight G_mu nu = alpha_CPR g_mu nu with alpha_CPR = Z_N / alpha_EV (alpha_EV = 1 -> alpha_CPR = Z_N; alpha_EV = 0 -> limit
   alpha_CPR -> infinity).  Jacobians J_V = Delta - R/4, J_S = Delta (Delta - R/3), J_c = Delta are exponentiated and regulated (CPR sec. VII).
 * Regulator: Litim, type I applied to each York-decomposed operator: Gamma^(2)(Delta) + R_k = Gamma^(2)(P_k(Delta)) (CPR eq. (9) form; every
   -D^2 replaced by P_k); the regulator carries the field's own Z_N.  d_t R_k with or without the eta_N terms (d_t Z_N = -eta_N Z_N).
 * Heat-kernel expansion on S^4 to the order needed here (b_0, b_2), threshold integrals Q_n in closed form for the Litim cutoff.
   Excluded modes enter only b_4 and higher on S^4 (CPR appendix, table 'taba6' note), so they do not affect G1.
 * Matter: minimally coupled N_S scalars, N_D Dirac fermions, N_V gauge vectors, regulated by the same frozen rule (type I: the bare
   Laplacian is replaced by P_k, curvature endomorphisms stay in the denominators: vectors in Feynman gauge Delta + Ric, Dirac D-slash^2 =
   Delta + R/4).  The natural-operator (type II) regulator that Dona-Eichhorn-Percacci 1311.2898 used for matter is computed as a DIAGNOSTIC only.
"""
import sys
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from scipy.optimize import fsolve
import as1_common as C
import as1_g1_fg_flat as FG

R, lam, g, eta, z, D, a = sp.symbols("R lambda g eta_N z D a", real=True)
NS, ND, NV = sp.symbols("N_S N_D N_V", real=True)
Zs = sp.Symbol("Z", positive=True)
fails = []


def chk(tag, ok, msg, gating=True):
    print(("  [PASS] " if ok else ("  [FAIL] " if gating else "  [NOTE] ")) + tag + "  " + msg)
    if gating and not ok:
        fails.append(tag)


# ---------------- heat-kernel coefficients on S^4 (b_0, b_2/R) ----------------
# unconstrained Laplacians: tr b_2 = tr(1) R/6
HK = {"S": (1, sp.Rational(1, 6)), "V": (4, sp.Rational(2, 3)), "Sym": (10, sp.Rational(5, 3)), "spinor": (4, sp.Rational(2, 3)),
      "TF": (9, sp.Rational(3, 2))}
# York relations on S^4 (CPR eqs (vt), (ttt)): Tr_V e^{-s Delta} = Tr_VT e^{-s Delta} + Tr_S e^{-s(Delta - R/4)} - (excluded modes, b_4+);
# Tr_Sym = Tr_TT + Tr_VT e^{-s(Delta - 5R/12)} + Tr_S e^{-s Delta} + Tr_S e^{-s(Delta - 2R/3)} - (excluded modes, b_4+).
# A shift Delta -> Delta - c R changes b_2 by + c b_0 R.
b2_VT = HK["V"][1] - (HK["S"][1] + sp.Rational(1, 4) * HK["S"][0])
b0_VT = HK["V"][0] - HK["S"][0]
b2_TT = HK["Sym"][1] - (b2_VT + sp.Rational(5, 12) * b0_VT) - HK["S"][1] - (HK["S"][1] + sp.Rational(2, 3) * HK["S"][0])
b0_TT = HK["Sym"][0] - b0_VT - 2 * HK["S"][0]
HK["VT"] = (b0_VT, b2_VT)
HK["TT"] = (b0_TT, b2_TT)


def Q(n, W):
    """Q_n[W] = (1/Gamma(n)) int_0^inf dz z^(n-1) W(z); every W used here vanishes for z > k^2 = 1 (Litim)."""
    return sp.integrate(z**(n - 1) * W, (z, 0, 1)) / sp.gamma(n)


def trace(field, W):
    """(16 pi^2 / Vol) Tr_field W(Delta) to first order in R: b0 Q_2(W) + R (b0 Q_2(dW/dR) + b2 Q_1(W)), W evaluated with P = 1 on [0,1]."""
    b0, b2 = HK[field]
    W = sp.sympify(W)
    W0 = sp.simplify(W.subs(R, 0))
    W1 = sp.simplify(sp.diff(W, R).subs(R, 0))
    return sp.simplify(b0 * Q(2, W0)), sp.simplify(b0 * Q(2, W1) + b2 * Q(1, W0))


# ---------------- f(R) second variation in York variables (CPR sec. VII, d = 4) ----------------
def hessian_blocks(f, f1, f2, alp, rho):
    rho = sp.Integer(rho)   # exact rationals (a Python int here produced float 1/16 in the second run)
    TT = -sp.Rational(1, 2) * (f1 * (D - R / 3) + f)
    XI = (D - R / 4) * (alp * (D - R / 4) + R / 2 * f1 - f)
    Hhh = sp.Rational(1, 8) * (sp.Rational(9, 2) * f2 * (D - R / 3)**2 + sp.Rational(3, 2) * f1 * (D - R / 3) - R / 2 * f1 + f) + rho**2 / 16 * alp * D
    Hhs = sp.Rational(3, 16) * (3 * f2 * (D - R / 3) + f1 + rho * alp) * D * (D - R / 3)
    Hss = sp.Rational(3, 8) * (sp.Rational(3, 2) * f2 * D * (D - R / 3) + f1 * D / 2 + R / 2 * f1 - f + sp.Rational(3, 2) * (D - R / 3) * alp) * D * (D - R / 3)
    return TT, XI, sp.Matrix([[Hhh, Hhs], [Hhs, Hss]])


def W_block(H, with_eta, alpha_inf):
    """W(z) = tr[ H(P)^{-1} d_t R_k ], P = 1, d_t P = 2; eta terms: d_t Z = -eta Z with H homogeneous of degree 1 in Z."""
    Hm = H if isinstance(H, sp.MatrixBase) else sp.Matrix([[H]])
    HP = Hm.subs(D, 1)
    dR = 2 * sp.diff(Hm, D).subs(D, 1)
    if with_eta:
        dR = dR - eta * (HP - Hm.subs(D, z))
    W = sp.simplify((HP.inv() * dR).trace())
    if alpha_inf:
        lead = sp.simplify(sp.limit(W / a, a, sp.oo))
        if lead != 0:            # the alpha -> 0 (a -> infinity) limit does not exist: W grows like a
            DIVERGENT.append(sp.factor(lead))
            return sp.nan
        W = sp.limit(W, a, sp.oo)
    else:
        W = W.subs(a, 1)
    return sp.simplify(W)


DIVERGENT = []


def W_log(J):
    """d_t of a regulated determinant factor J(Delta) with no couplings: W = 2 d/dP ln J(P) at P = 1."""
    return sp.simplify(2 * sp.diff(sp.log(J), D).subs(D, 1))


def gravity_rhs(alpha_ev, with_eta, scheme="Ib"):
    """(A0, A1): (16 pi^2/Vol) d_t Gamma_k = A0 + A1 R from metric fluctuations, Jacobians and ghosts."""
    Z = Zs
    f, f1, f2 = Z * (2 * lam - R), -Z, 0
    alp = Z * a
    if scheme == "Ia":   # validation only: CPR type Ia in the alpha = 1 de Donder gauge (undecomposed, minimal operator)
        A = [0, 0]
        for fld, W in (("TF", 2 / (1 - 2 * lam + sp.Rational(2, 3) * R)), ("S", 2 / (1 - 2 * lam))):
            t = trace(fld, sp.Rational(1, 2) * W)
            A = [A[0] + t[0], A[1] + t[1]]
        t = trace("V", -2 / (1 - R / 4))
        return sp.simplify(A[0] + t[0]), sp.simplify(A[1] + t[1])
    TT, XI, S = hessian_blocks(f, f1, f2, alp, 1)
    ainf = (alpha_ev == 0)
    parts = []
    parts.append(("TT", sp.Rational(1, 2), "TT", W_block(TT, with_eta, ainf)))
    parts.append(("xi", sp.Rational(1, 2), "VT", W_block(XI, with_eta, ainf)))
    parts.append(("(h,sigma)", sp.Rational(1, 2), "S", W_block(S, with_eta, ainf)))
    parts.append(("J_V", -sp.Rational(1, 2), "VT", W_log(D - R / 4)))
    parts.append(("J_S", -sp.Rational(1, 2), "S", W_log(D * (D - R / 3))))
    parts.append(("ghost c^T", -1, "VT", W_log(D - R / 4)))
    parts.append(("ghost c + J_c", -1, "S", sp.simplify(W_log(D * (D - R / 2)) - W_log(D))))
    A0 = A1 = 0
    detail = []
    if any(W is sp.nan for _, _, _, W in parts):
        return None, None, [(nm, "DIVERGENT" if W is sp.nan else "", "") for nm, _, _, W in parts]
    for name, wgt, fld, W in parts:
        t0, t1 = trace(fld, wgt * W)
        A0 += t0
        A1 += t1
        detail.append((name, sp.simplify(t0), sp.simplify(t1)))
    return sp.simplify(A0), sp.simplify(A1), detail


def matter_rhs(kind):
    """(A0, A1) per species, frozen type I reading ('I'), or the natural-operator type II of Dona-Eichhorn-Percacci ('II', diagnostic),
    or York-decomposed vectors with type I ('Ib', diagnostic)."""
    sc = trace("S", sp.Rational(1, 2) * 2)
    if kind == "I":
        di = trace("spinor", -sp.Rational(1, 2) * 2 / (1 + R / 4))
        v = trace("V", sp.Rational(1, 2) * 2 / (1 + R / 4))
        gh = trace("S", -2)
        ve = (v[0] + gh[0], v[1] + gh[1])
    elif kind == "Ib":
        di = trace("spinor", -sp.Rational(1, 2) * 2 / (1 + R / 4))
        v = trace("VT", sp.Rational(1, 2) * 2 / (1 + R / 4))
        gh = trace("S", -2)
        ve = (v[0] + gh[0], v[1] + gh[1])
    else:   # type II: heat kernel of the natural operators, b_2(D-slash^2) = 4(R/6 - R/4), b_2(Delta + Ric) = 4R/6 - R
        di = (-sp.Rational(1, 2) * 4 * Q(2, 2), -sp.Rational(1, 2) * (4 * sp.Rational(1, 6) - 1) * Q(1, 2))
        v = (sp.Rational(1, 2) * 4 * Q(2, 2), sp.Rational(1, 2) * (sp.Rational(2, 3) - 1) * Q(1, 2))
        gh = trace("S", -2)
        ve = (v[0] + gh[0], v[1] + gh[1])
    A0 = NS * sc[0] + ND * di[0] + NV * ve[0]
    A1 = NS * sc[1] + ND * di[1] + NV * ve[1]
    return sp.expand(A0), sp.expand(A1)


def betas_from_rhs(A0, A1, with_eta):
    """LHS: Gamma = int sqrt(g) (2 Lambda - R)/(16 pi G):  eta_N/(16 pi g) = A1/(16 pi^2);  d_t lambda = -2 lambda + eta lambda + g A0/(2 pi)."""
    if with_eta:
        A1e = sp.expand(A1)
        e_sol = sp.solve(sp.Eq(eta, g * A1e / sp.pi), eta)[0]
    else:
        e_sol = sp.simplify(g * A1 / sp.pi)
    bg = sp.simplify((2 + e_sol) * g)
    bl = sp.simplify((-2 * lam + eta * lam + g * A0 / (2 * sp.pi)).subs(eta, e_sol))
    return bg, bl, e_sol


def ev_betas():
    d = 1 - 2 * lam
    G, L = g, lam
    bG = 2 * G + G**2 / (6 * sp.pi) * (2 * ND + NS - 4 * NV) - G**2 / (6 * sp.pi) * (14 + 6 / d + 9 / d**2)
    bL = (-2 * L + G / (4 * sp.pi) * (NS - 4 * ND + 2 * NV) + G / (6 * sp.pi) * L * (2 * ND + NS - 4 * NV)
          - 3 * G / (2 * sp.pi) - 7 * G * L / (3 * sp.pi) - 3 * G / (4 * sp.pi * d**2) + 7 * G / (4 * sp.pi * d))
    return bG, bL


def coeff_table(bG, bL):
    """beta_G = 2G + G^2/pi [c_S N_S + c_D N_D + c_V N_V + c_grav];  beta_L = -2L + L*eta + ...: report G/pi and G^2/pi coefficients."""
    out = {}
    eG = sp.expand(sp.simplify((bG - 2 * g) * sp.pi / g**2))
    eL = sp.expand(sp.simplify((bL + 2 * lam) * sp.pi / g))
    for nm, sym in (("N_S", NS), ("N_D", ND), ("N_V", NV)):
        out[("betaG", nm)] = sp.simplify(eG.coeff(sym))
        out[("betaL", nm)] = sp.simplify(eL.coeff(sym))
    out[("betaG", "grav")] = sp.simplify(eG.subs({NS: 0, ND: 0, NV: 0}))
    out[("betaL", "grav")] = sp.simplify(eL.subs({NS: 0, ND: 0, NV: 0}))
    return out


def fixed_points(bG, bL, SM):
    fG = sp.lambdify((g, lam), bG.subs(SM), "numpy")
    fL = sp.lambdify((g, lam), bL.subs(SM), "numpy")
    roots = set()
    for G0 in np.linspace(0.1, 10, 12):
        for L0 in np.linspace(-12, 0.45, 15):
            try:
                with np.errstate(all="ignore"):
                    sol, info, ier, _ = fsolve(lambda x: [fG(*x), fL(*x)], [G0, L0], full_output=True, xtol=1e-13)
            except Exception:
                continue
            if ier == 1 and sol[0] > 1e-6 and abs(1 - 2 * sol[1]) > 1e-3 and max(abs(fG(*sol)), abs(fL(*sol))) < 1e-10:
                roots.add((round(float(sol[0]), 5), round(float(sol[1]), 5)))
    return sorted(roots)


if __name__ == "__main__":
    print("MODE: NORMAL (no MUTATE control is pre-registered for this script)")
    SM = {NS: 4, ND: sp.Rational(45, 2), NV: 12}

    print("\nV  validations of the machinery (gating)")
    chk("V3", HK["VT"] == (3, sp.Rational(1, 4)) and HK["TT"] == (5, -sp.Rational(5, 6)),
        f"S^4 York heat-kernel coefficients derived from the unconstrained ones: VT (b0, b2/R) = {HK['VT']}, TT = {HK['TT']} "
        "(CPR table taba6: (3, 1/4), (5, -5/6))")
    Z = Zs
    TT, XI, S = hessian_blocks(Z * (2 * lam - R), -Z, 0, Z, 1)
    kin = [sp.simplify(TT - Z / 2 * (D + sp.Rational(2, 3) * R - 2 * lam)), sp.simplify(XI - Z * (D - R / 4) * (D + R / 4 - 2 * lam)),
           sp.simplify(S[0, 0] + Z / 8 * (D - 2 * lam)), sp.simplify(S[0, 1]), sp.simplify(S[1, 1] - sp.Rational(3, 8) * Z * D * (D - R / 3) * (D - 2 * lam))]
    chk("V1", all(x == 0 for x in kin), "CPR f(R) York Hessian at f = Z(2 Lambda - R), alpha_CPR = Z, rho = 1 equals CPR's EH York operators (kinIb, d = 4)")
    F0, F1, F2, alpS = sp.symbols("f0 f1 f2 alphaS")
    TTg, XIg, Sg = hessian_blocks(F0, F1, F2, 0, 1)
    onshell = {F0: R * F1 / 2}
    v = Sg.subs(onshell) * sp.Matrix([-D, 1])
    chk("V2", sp.simplify(XIg.subs(onshell)) == 0 and all(sp.simplify(x) == 0 for x in v),
        "on shell (2 f = R f') the f-part of the Hessian annihilates the pure-gauge xi and (h, sigma) = (-Delta, 1) directions, any f''")
    A0, A1, _ = gravity_rhs(1, False, "Ib")
    chk("V4", sp.simplify(A0 - (1 + 8 * lam) / (1 - 2 * lam)) == 0 and
        sp.simplify(A1 + (105 - 212 * lam + 200 * lam**2) / (24 * (1 - 2 * lam)**2)) == 0,
        f"type Ib, alpha = 1 de Donder, no eta: A0 = {sp.factor(A0)}, A1 = {sp.factor(A1)}; CPR sec. IV.B: A1_CPR = pi A0, B1_CPR = pi A1 "
        "with A0 = (1+8L)/(1-2L), A1 = -(105-212L+200L^2)/(24(1-2L)^2)")
    A0a, A1a = gravity_rhs(1, False, "Ia")
    chk("V5", sp.simplify(A0a - (1 + 8 * lam) / (1 - 2 * lam)) == 0 and
        sp.simplify(A1a + (11 - 18 * lam + 28 * lam**2) / (3 * (1 - 2 * lam)**2)) == 0,
        f"type Ia, alpha = 1 (Reuter), no eta: A1 = {sp.factor(A1a)}; CPR eq. (betasIa) at eta = 0: -(11-18L+28L^2)/(3(1-2L)^2)")

    print("\nE-V (4.8)-(4.9): symbolic transcription checked against lane B's numeric implementation (b1_reproduce_literature.py, by import)")
    b1 = C.laneB_b1()
    bGev, bLev = ev_betas()
    fG = sp.lambdify((g, lam), bGev.subs(SM)); fL = sp.lambdify((g, lam), bLev.subs(SM))
    rng = np.random.default_rng(12345)
    pts = [(rng.uniform(0.1, 6), rng.uniform(-8, 0.4)) for _ in range(20)]
    err = max(max(abs(fG(G_, L_) - b1.betas([G_, L_])[0]), abs(fL(G_, L_) - b1.betas([G_, L_])[1])) for G_, L_ in pts)
    chk("V6", err < 1e-12, f"transcription equals b1.betas at 20 random points (max abs diff {err:.1e})")
    ev_tab = coeff_table(bGev, bLev)

    print("\nG1  per declared combination: derived EH-limit beta functions vs E-V (4.8)-(4.9)")
    print("    coefficient convention: beta_G = 2G + (G^2/pi) [c_S N_S + c_D N_D + c_V N_V + c_grav(L)],  beta_L = -2L + (G/pi) [...] (no-eta case)")
    matI = matter_rhs("I")
    fg_checks, fg_res, _ = FG.run_all(mutate1=False)
    combo_pass = {}
    d = 1 - 2 * lam
    for (ab, weta) in FG.COMBOS:
        tag = f"(alpha,beta)={ab}, {'WITH eta_N' if weta else 'no eta'}"
        DIVERGENT.clear()
        A0g, A1g, det = gravity_rhs(ab[0], weta, "Ib")
        if A0g is None:
            print(f"\n  --- {tag}")
            print(f"    the alpha -> 0 limit of d_t Gamma_k does not exist in this convention: blocks {[n for n, s_, _ in det if s_]}")
            print(f"    leading term of W (per unit a = 1/alpha) as alpha -> 0: {DIVERGENT}  (proportional to eta_N; the regulated gauge-fixing")
            print("    term's eta_N piece, a Z_N [A(P_k) - A(Delta)], is not aligned with the null direction of A(P_k) in the (h, sigma) sector)")
            A0n, A1n, _ = gravity_rhs(ab[0], False, "Ib")
            print(f"    its eta_N-independent part equals the no-eta combination (A0 = {sp.factor(A0n)}, A1 = {sp.factor(A1n)}); since eta_N = O(G),")
            print("    the O(G) terms of beta_Lambda would be fixed by these eta-free parts, which already differ from E-V (see the no-eta combination).")
            chk("G1(i) " + tag, False, "flow undefined (alpha -> 0 limit diverges); cannot reproduce (4.8)-(4.9)")
            chk("G1(ii) " + tag, False, "no flow, no fixed point")
            ok_iii = fg_res[(ab, weta)]["match"]
            chk("G1(iii) " + tag, ok_iii, f"f_g = {sp.factor(fg_res[(ab, weta)]['fg'])} (from as1_g1_fg_flat.py); E-V: G(1-4L)/(4 pi (1-2L)^2)")
            combo_pass[(ab, weta)] = False
            continue
        bG, bL, esol = betas_from_rhs(A0g + matI[0], A1g + matI[1], weta)
        print(f"\n  --- {tag}")
        print(f"    gravity sector (16 pi^2/Vol) d_t Gamma = A0 + A1 R:  A0 = {sp.factor(A0g)},  A1 = {sp.factor(A1g)}")
        for nm, t0, t1 in det:
            print(f"        {nm:14s} A0 {str(sp.factor(t0)):40s} A1 {sp.factor(t1)}")
        ok_i = sp.simplify(bG - bGev) == 0 and sp.simplify(bL - bLev) == 0
        if not weta:
            tab = coeff_table(bG, bL)
            for key in tab:
                same = sp.simplify(tab[key] - ev_tab[key]) == 0
                print(f"    {key[0]:5s} {key[1]:5s}: derived {str(sp.factor(tab[key])):45s} E-V {str(sp.factor(ev_tab[key])):45s} {'==' if same else 'DIFFERENT'}")
        else:
            A1e = sp.expand(A1g + matI[1])
            print(f"    eta_N-dependence of the R-coefficient: dA1/d eta_N = {sp.factor(sp.diff(A1e, eta))}  (nonzero -> beta_G is not polynomial in G, "
                  "E-V (4.8) is)")
            print(f"    beta_G = {sp.factor(bG.subs(SM))}")
        # O(G) term of beta_Lambda from the gravity sector alone (eta-independent at this order): a_0 counting
        lin0 = sp.simplify((sp.diff(bL, g).subs(g, 0)).subs({lam: 0, NS: 0, ND: 0, NV: 0}))
        lin0ev = sp.simplify((sp.diff(bLev, g).subs(g, 0)).subs({lam: 0, NS: 0, ND: 0, NV: 0}))
        print(f"    O(G) coefficient of beta_Lambda at Lambda = 0, gravity sector (pure a_0 count): derived {lin0} = (1/2pi) x {sp.simplify(lin0*2*sp.pi)},"
              f" E-V {lin0ev} = (1/2pi) x {sp.simplify(lin0ev*2*sp.pi)}")
        chk("G1(i) " + tag, ok_i, "every coefficient of (4.8)-(4.9), matter and gravity parts, exactly")
        roots = fixed_points(bG, bL, SM)
        evr = (2.7262, -3.7583)
        ok_ii = any(abs(r[0] - evr[0]) < 1e-3 and abs(r[1] - evr[1]) < 1e-3 for r in roots)
        chk("G1(ii) " + tag, ok_ii, f"SM fixed point(s) of the derived system: {roots}; E-V (2.726, -3.758) to 1e-3")
        ok_iii = fg_res[(ab, weta)]["match"]
        chk("G1(iii) " + tag, ok_iii, f"f_g = {sp.factor(fg_res[(ab, weta)]['fg'])} (from as1_g1_fg_flat.py); E-V: G(1-4L)/(4 pi (1-2L)^2)")
        combo_pass[(ab, weta)] = ok_i and ok_ii and ok_iii
    # G1 sub-results are the gate outcome, not machinery failures: remove them from 'fails' and decide the gate below
    fails[:] = [f_ for f_ in fails if not f_.startswith("G1(")]

    print("\nDiagnostics (not gating)")
    print("  D1  vacuum (a_0) term of the gravity sector, i.e. the G A0/(2 pi) part of beta_Lambda: E-V (G/2pi)(3/(1-2L) - 4);")
    for al in (0, 1):
        A0g, _, _ = gravity_rhs(al, False, "Ib")
        print(f"      alpha = {al}: (G/2pi)({sp.factor(A0g)})  -> at L = 0: {A0g.subs(lam, 0)}  (E-V at L = 0: -1; two graviton polarisations x 1/2 = +1)")
    print("      E-V's value equals (5 TT + 1 scalar modes at -2 Lambda)/2 minus the full vector ghost (4), i.e. the gauge-mode/Jacobian part")
    print("      (+2 in alpha = 0) is absent; no declared combination with every -D^2 of Gamma^(2) (gauge fixing included) regulated produces it.")
    A0a, A1a = gravity_rhs(1, False, "Ia")
    gh_Ia = trace("V", -2 / (1 - R / 4))[1]
    gh_Ib = trace("VT", -2 / (1 - R / 4))[1] + trace("S", -2 / (1 - R / 2))[1]
    print(f"  D2  constant 14 in E-V (4.8): ghost R-coefficient -Tr_V[d_tR/(P-Ric)] undecomposed (type Ia) = {gh_Ia} -> 6 x {-gh_Ia} = {-6*gh_Ia};"
          f" York-decomposed (type Ib) = {gh_Ib} -> {-6*gh_Ib}")
    for kind in ("I", "Ib", "II"):
        mA0, mA1 = matter_rhs(kind)
        print(f"  D3  matter, regulator reading '{kind}': A1 per species = scalar {mA1.coeff(NS)}, Dirac {mA1.coeff(ND)}, vector {mA1.coeff(NV)};"
              f" A0 = scalar {mA0.coeff(NS)}, Dirac {mA0.coeff(ND)}, vector {mA0.coeff(NV)}"
              + ("   <- E-V/DEP matter (type II)" if kind == "II" else ""))
    print("      E-V (4.8) matter: beta_G matter = G^2/(6 pi)(N_S + 2 N_D - 4 N_V) <-> A1 = (1/6, 1/3, -2/3); beta_L matter <-> A0 = (1/2, -2, 1).")
    matII = matter_rhs("II")
    for (ab, weta) in FG.COMBOS[:1] + FG.COMBOS[2:3]:
        A0g, A1g, _ = gravity_rhs(ab[0], weta, "Ib")
        bG2, bL2, _ = betas_from_rhs(A0g + matII[0], A1g + matII[1], weta)
        print(f"  D4  (alpha,beta)={ab}, no eta, with the type II matter of E-V instead of the frozen type I: SM fixed points {fixed_points(bG2, bL2, SM)}")

    sel = [k for k, v in combo_pass.items() if v]
    print("\nG1 SELECTION")
    if not sel:
        print("  no declared gauge/convention combination passes G1 (i)-(iii)  ->  LANE AS1: NOT COMPLETED (stop; no R^2 fixed point, f_g*, P or class)")
        fails.append("G1: no combination passes")
    else:
        pick = ((0, 1), False) if len(sel) > 1 and ((0, 1), False) in sel else sel[0]
        print(f"  passing: {sel}; selected (tie-break rule if needed): {pick}")
    print("\nCHECKS FAILED:", fails if fails else "none")
    sys.exit(1 if fails else 0)
