#!/usr/bin/env python3
r"""
FRIED-CHICKEN req 5 (matter conservation) for the Deffayet-Woodard 2026 nonlocal MOND
(arXiv:2512.10513), attacked through its LOCALIZED action.

THE LOCALIZED ACTION (all auxiliaries; c=1, kappa = 16 pi G):
  S = INT d^4x sqrt(-g) { (1/kappa)[R - a0^2 M]
                          - g^{ab} d_a xi d_b X - xi R_ab u^a u^b          (X = Box^{-1} R_uu, multiplier xi)
                          + lambda (g^{ab} u_a u_b + 1)                     (mimetic clock, u_a = d_a phi)
                          - (M + f(Z)) g^{ab} u_a d_b nu                    (transport of Q = M+f, multiplier nu)
                          - (1/2)(d psi)^2 - V(psi) }                       (minimally coupled matter)
  Z = (4/a0^2) g^{ab} d_a X d_b X.
Euler-Lagrange equations reproduce every defining equation of DW 2026:
  d/d xi     : Box X = R_ab u^a u^b                       (DW eq 26-27, before choosing the retarded inverse)
  d/d nu     : nabla_a[(M+f) u^a] = 0                      (DW eq 33 transport)
  d/d lambda : (d phi)^2 = -1                              (DW eq 5)
  d/d M      : u.d nu = -a0^2/kappa
  d/d X      : Box xi = -(8/a0^2) nabla_a[(u.d nu) f'(Z) nabla^a X]     (the RESPONSE field)
  d/d phi    : nabla_a[-2 lambda u^a + 2 xi R^a_b u^b + (M+f) nabla^a nu] = 0   (clock response)
DW / DEW-2014 (arXiv:1405.0393 eq 16-21) DEFINE the causal field equations as exactly these local
equations with retarded (null t=0) data on every auxiliary.  The repo's standing objection
(FRIED_CHICKEN_VERDICT 09-01, DW_TRANSITION_CONSERVATION_VERDICT) was: the retarded box^{-1} is not
the Euler-Lagrange operator of the single-copy NONLOCAL action (its adjoint is advanced), so Noether
does not automatically give nabla^mu E_mu nu = 0  =>  req 5 NOT-COMPUTED.

THIS SCRIPT computes it.  Diffeomorphism invariance of the LOCAL action gives the off-shell identity
      2 nabla^mu E_{mu nu} + sum_A E_A d_nu Phi_A  == 0                                   (*)
with E_{mu nu} = (1/sqrt-g) dS/dg^{mu nu}, E_A = (1/sqrt-g) dS/dPhi_A for every scalar Phi_A.
(*) holds for ANY field configuration, so on any solution of the auxiliary equations -- retarded,
advanced, or anything else -- nabla^mu E^{grav}_{mu nu} = 0 identically, and the metric equation
E^{grav} = T/2 is consistent iff nabla^mu T_mu nu = 0, which is the matter Euler-Lagrange equation.
The boundary-condition choice never enters (*).  We verify (*) by brute force:
  * covariant E_{mu nu} derived analytically from the action (incl. the delta R_ab term),
  * cross-checked against the direct Euler-Lagrange variation of the reduced Lagrangian (catches sign/
    factor errors in the analytic formulas),
  * (*) evaluated component by component on a 4-function metric  diag(-N^2, A^2, C^2, D^2)(t,x) with all
    seven fields (X, xi, phi, lambda, M, nu, psi) arbitrary functions of (t,x), for a generic cubic f(Z)
    with symbolic coefficients AND for an undefined function f,
  * mutation controls: a non-covariant transport term, a sign flip in E, and DROPPING THE CLOCK-RESPONSE
    (mimetic multiplier) term all break (*) -- so the test can fail, and the clock-response stress is
    REQUIRED for conservation (DW's equations must contain it).
Every check can fail; exit status 1 on any failure.
"""
import sys
import time
import sympy as sp
from dw_tensor_toolkit_2026 import Geometry, euler_lagrange

t0 = time.time()
checks = []


def check(name, ok, detail=""):
    checks.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))


def hdr(s):
    print("\n" + "=" * 96 + "\n" + s + "\n" + "=" * 96)


t, x, y, z = sp.symbols('t x y z', real=True)
coords = [t, x, y, z]
a0, kap = sp.symbols('a0 kappa', positive=True)
c1, c2, c3 = sp.symbols('c1 c2 c3', real=True)

# fields (all functions of (t,x))
N, A, C, D = [sp.Function(n)(t, x) for n in ('N', 'A', 'C', 'D')]
X, xi, phi, lam, M, nu, psi = [sp.Function(n)(t, x) for n in ('X', 'xi', 'phi', 'lam', 'M', 'nu', 'psi')]
Vpot = sp.Function('V')


def build_all(f_of, transport_covariant=True, drop_clock_response=False, flip_sign=False):
    """Return (Lagrangian density, E_munu Matrix, dict of E_A, geometry, misc)."""
    g = sp.diag(-N**2, A**2, C**2, D**2)
    G = Geometry(g, coords)
    gi = G.gi
    sqrtg = N * A * C * D                       # exact for this chart (all functions positive)
    n = 4
    u = G.grad(phi)                             # u_a
    uu = G.raise1(u)                            # u^a
    dX, dxi, dnu, dpsi = G.grad(X), G.grad(xi), G.grad(nu), G.grad(psi)
    usq = G.dot(u, u)
    if transport_covariant:
        W = G.dot(u, dnu)                       # u^a d_a nu
    else:
        W = sp.diff(phi, t) * sp.diff(nu, t)    # MUTATION: no metric -> not a scalar
    Z = (4 / a0**2) * G.dot(dX, dX)
    fZ = f_of(Z)
    Zs = sp.Symbol('Zs')
    fp = sp.diff(f_of(Zs), Zs).subs(Zs, Z)      # f'(Z)
    Q = M + fZ
    Ruu = sum(G.Ric[a, b] * uu[a] * uu[b] for a in range(n) for b in range(n))

    L = sqrtg * ((G.Rs - a0**2 * M) / kap
                 - G.dot(dxi, dX) - xi * Ruu
                 + lam * (usq + 1)
                 - Q * W
                 - sp.Rational(1, 2) * G.dot(dpsi, dpsi) - Vpot(psi))

    # ---------------- covariant E_{mu nu} = (1/sqrt-g) dS/dg^{mu nu} ----------------
    E = sp.zeros(n, n)
    # delta R_ab term with V^{ab} = -xi u^a u^b:
    #   -nabla_a nabla_(mu V_nu)^a + (1/2) Box V_munu
    #   + (1/2) g_munu nabla_a nabla_b V^{ab}.
    # The signs follow from varying with respect to the INVERSE metric.  A useful
    # oracle is V^{ab}=F g^{ab}: after also varying V, this must reproduce
    # F G_mn + (g_mn Box - nabla_m nabla_n)F.
    Vlow = [[-xi * u[a] * u[b] for b in range(n)] for a in range(n)]
    dV = G.cov(Vlow, 2)               # dV[c][a][b] = nabla_c V_ab
    ddV = G.cov(dV, 3)                # ddV[d][c][a][b] = nabla_d nabla_c V_ab
    def boxV(mu, nv):
        return sum(gi[d, c] * ddV[d][c][mu][nv] for d in range(n) for c in range(n))
    def divdivV():
        return sum(gi[d, a] * gi[c, b] * ddV[d][c][a][b] for a in range(n) for b in range(n) for c in range(n) for d in range(n))
    ddivV = divdivV()
    def nab_nab_V(mu, nv):   # nabla_alpha nabla_mu V_nu^alpha = g^{alpha beta} nabla_alpha nabla_mu V_{nu beta}
        return sum(gi[al, be] * ddV[al][mu][nv][be] for al in range(n) for be in range(n))
    for mu in range(n):
        for nv in range(mu, n):
            e = G.Ein[mu, nv] / kap
            e += (a0**2 / (2 * kap)) * M * g[mu, nv]
            e += -sp.Rational(1, 2) * (dxi[mu] * dX[nv] + dxi[nv] * dX[mu]) + sp.Rational(1, 2) * g[mu, nv] * G.dot(dxi, dX)
            # explicit metric dependence of -xi R_ab u^a u^b (u^a = g^{ab} u_b) and sqrt-g
            Ru = [sum(G.Ric[a, b] * uu[b] for b in range(n)) for a in range(n)]   # R_ab u^b
            e += sp.Rational(1, 2) * g[mu, nv] * xi * Ruu - xi * (u[mu] * Ru[nv] + u[nv] * Ru[mu])
            # delta R_ab contribution
            e += -sp.Rational(1, 2) * (nab_nab_V(mu, nv) + nab_nab_V(nv, mu)) + sp.Rational(1, 2) * boxV(mu, nv) \
                 + sp.Rational(1, 2) * g[mu, nv] * ddivV
            # mimetic clock
            if not drop_clock_response:
                e += lam * u[mu] * u[nv] - sp.Rational(1, 2) * g[mu, nv] * lam * (usq + 1)
            # transport sector
            if transport_covariant:
                e += -sp.Rational(1, 2) * Q * (u[mu] * dnu[nv] + u[nv] * dnu[mu]) + sp.Rational(1, 2) * g[mu, nv] * Q * W
            else:
                e += sp.Rational(1, 2) * g[mu, nv] * Q * W
            e += -W * fp * (4 / a0**2) * dX[mu] * dX[nv]
            # matter
            e += -sp.Rational(1, 2) * dpsi[mu] * dpsi[nv] + sp.Rational(1, 2) * g[mu, nv] * (sp.Rational(1, 2) * G.dot(dpsi, dpsi) + Vpot(psi))
            if flip_sign and mu == nv == 0:
                e -= 2 * (a0**2 / (2 * kap)) * M * g[mu, nv]   # MUTATION: wrong sign of one term in E_tt
            E[mu, nv] = e
            E[nv, mu] = e

    # ---------------- auxiliary Euler-Lagrange E_A = (1/sqrt-g) dS/dPhi_A ----------------
    EA = {}
    EA[xi] = G.box(X) - Ruu
    EA[X] = G.box(xi) + (8 / a0**2) * G.div_vec_upper([W * fp * v for v in G.raise1(dX)])
    EA[M] = -a0**2 / kap - W
    EA[nu] = G.div_vec_upper([Q * v for v in uu])
    EA[lam] = usq + 1
    Rup_u = [sum(gi[a, b] * sum(G.Ric[b, c] * uu[c] for c in range(n)) for b in range(n)) for a in range(n)]  # R^a_b u^b
    J = [(-2 * lam * uu[a] if not drop_clock_response else 0) + 2 * xi * Rup_u[a] + Q * G.raise1(dnu)[a] for a in range(n)]
    EA[phi] = G.div_vec_upper(J)
    EA[psi] = G.box(psi) - sp.diff(Vpot(psi), psi)
    return L, E, EA, G, dict(sqrtg=sqrtg, g=g, gi=gi)


def simplify0(expr):
    """Robust zero test for rational expressions in the field derivatives (with possible Subs atoms)."""
    e = sp.together(sp.expand(expr))
    num, den = sp.fraction(e)
    return sp.expand(num)


def main():
    # =====================================================================================
    hdr("PART 1 -- build the localized DW action, covariant E_{mu nu}, auxiliary E_A  (generic cubic f)")
    # =====================================================================================
    fpoly = lambda Zv: c1 * Zv + c2 * Zv**2 + c3 * Zv**3
    L, E, EA, G, misc = build_all(fpoly)
    sqrtg, g, gi = misc['sqrtg'], misc['g'], misc['gi']
    print(f"  built in {time.time()-t0:.1f}s")

    # =====================================================================================
    hdr("PART 2 -- VARIATION CROSS-CHECK: direct Euler-Lagrange of the reduced density vs covariant formulas")
    # =====================================================================================
    # metric functions: dS/dq = sqrt-g E_{mu nu} d g^{mu nu}/d q
    proj = {N: (0, 2 / N**3), A: (1, -2 / A**3), C: (2, -2 / C**3), D: (3, -2 / D**3)}
    for q, (i, dgdq) in proj.items():
        lhs = euler_lagrange(L, q, [t, x])
        rhs = sqrtg * E[i, i] * dgdq
        res = simplify0(lhs - rhs)
        check(f"metric variation wrt {q.func.__name__}: reduced EL == sqrt-g E_{i}{i} dg^{i}{i}/dq", res == 0)
    for q in (X, xi, phi, lam, M, nu, psi):
        lhs = euler_lagrange(L, q, [t, x])
        res = simplify0(lhs - sqrtg * EA[q])
        check(f"auxiliary/matter variation wrt {q.func.__name__}: reduced EL == sqrt-g E_A", res == 0)
    print(f"  ({time.time()-t0:.1f}s)")

    # =====================================================================================
    hdr("PART 3 -- THE NOETHER IDENTITY  2 nabla^mu E_{mu nu} + sum_A E_A d_nu Phi_A == 0  OFF-SHELL")
    # =====================================================================================
    divE = G.div_sym_lower(E)
    fields = [X, xi, phi, lam, M, nu, psi]
    ident = []
    for nv in range(2):     # y,z components vanish identically by the chart symmetry
        I = 2 * divE[nv] + sum(EA[q] * sp.diff(q, coords[nv]) for q in fields)
        Ired = simplify0(I)
        ident.append(Ired)
        check(f"identity component nu={coords[nv]} vanishes identically (off-shell, cubic f)", Ired == 0)
    # teeth: the pure divergence does NOT vanish off-shell (so the E_A terms are load-bearing)
    for nv in range(2):
        d = simplify0(2 * divE[nv])
        check(f"2 nabla^mu E_{{mu {coords[nv]}}} alone is NOT identically zero off-shell (teeth)", d != 0)
    print(f"  ({time.time()-t0:.1f}s)")

    # on the auxiliary shell only (matter OFF-shell): 2 nabla^mu E^grav_munu = -E_psi d_nu psi  <=> nabla^mu T_munu = E_psi d_nu psi
    # i.e. matter conservation is exactly the matter Euler-Lagrange equation, and baryons feel nothing else.
    Tm = sp.zeros(4, 4)
    dpsi = G.grad(psi)
    for mu in range(4):
        for nv in range(4):
            Tm[mu, nv] = dpsi[mu] * dpsi[nv] - g[mu, nv] * (sp.Rational(1, 2) * G.dot(dpsi, dpsi) + Vpot(psi))
    divT = G.div_sym_lower(Tm)
    for nv in range(2):
        res = simplify0(divT[nv] - EA[psi] * sp.diff(psi, coords[nv]))
        check(f"matter sector alone: nabla^mu T_{{mu {coords[nv]}}} == E_psi d_nu psi  (conservation <=> matter EOM)", res == 0)

    # =====================================================================================
    hdr("PART 4 -- MUTATION CONTROLS (each must BREAK the identity)")
    # =====================================================================================
    def identity_residuals(**kw):
        Lm, Em, EAm, Gm, mm = build_all(fpoly, **kw)
        dv = Gm.div_sym_lower(Em)
        out = []
        for nv in range(2):
            I = 2 * dv[nv] + sum(EAm[q] * sp.diff(q, coords[nv]) for q in fields)
            out.append(simplify0(I))
        return out

    r1 = identity_residuals(transport_covariant=False)
    check("M1 non-covariant transport term (u^t d_t nu without the metric) BREAKS the identity", any(r != 0 for r in r1))
    r2 = identity_residuals(flip_sign=True)
    check("M2 sign flip of the a0^2 M g_munu term in E_tt BREAKS the identity", any(r != 0 for r in r2))
    r3 = identity_residuals(drop_clock_response=True)
    check("M3 DROPPING the clock-response (mimetic multiplier lambda u_mu u_nu) stress BREAKS the identity",
          any(r != 0 for r in r3), "=> DW's causal equations MUST carry the clock-response stress to be conserved")
    print(f"  ({time.time()-t0:.1f}s)")

    # =====================================================================================
    hdr("PART 5 -- same identity with an UNDEFINED f(Z) (no polynomial assumption)")
    # =====================================================================================
    fgen = sp.Function('f')
    Lu, Eu, EAu, Gu, mu_ = build_all(lambda Zv: fgen(Zv))
    dvu = Gu.div_sym_lower(Eu)
    for nv in range(2):
        I = 2 * dvu[nv] + sum(EAu[q] * sp.diff(q, coords[nv]) for q in fields)
        I = I.doit()
        Ired = simplify0(I)
        if Ired != 0:
            Ired = sp.simplify(Ired)
        check(f"identity component nu={coords[nv]} vanishes identically for undefined f(Z)", Ired == 0)
    print(f"  ({time.time()-t0:.1f}s)")

    # =====================================================================================
    hdr("PART 6 -- retarded vs advanced is a choice of SOLUTION of a hyperbolic local equation, not of the equation")
    # =====================================================================================
    # principal part of the xi-equation E_X in xi is the d'Alembertian: coefficient of xi_tt is g^{tt} = -1/N^2
    coef_xitt = sp.simplify(sp.diff(EA[X], sp.Derivative(xi, t, t)))
    coef_xixx = sp.simplify(sp.diff(EA[X], sp.Derivative(xi, x, x)))
    check("E_X is a wave equation for the response xi: coeff(xi_tt) = g^tt, coeff(xi_xx) = g^xx (hyperbolic)",
          sp.simplify(coef_xitt - gi[0, 0]) == 0 and sp.simplify(coef_xixx - gi[1, 1]) == 0,
          f"{coef_xitt}, {coef_xixx}")
    coef_Xtt = sp.simplify(sp.diff(EA[xi], sp.Derivative(X, t, t)))
    check("E_xi is a wave equation for X: coeff(X_tt) = g^tt", sp.simplify(coef_Xtt - gi[0, 0]) == 0)
    # 1+1 explicit: a compactly supported source; retarded and advanced particular solutions both solve Box X = J
    tt, xx, s, r = sp.symbols('tt xx s r', real=True)
    Jsrc = sp.exp(-tt**2 - xx**2)          # smooth source (Gaussian), Box = -d_t^2 + d_x^2 on Minkowski
    # Duhamel: X_ret(t,x) = -(1/2) INT_{-inf}^{t} ds INT_{x-(t-s)}^{x+(t-s)} J(s,r) dr ; X_adv = -(1/2) INT_t^{inf} ds INT_{x-(s-t)}^{x+(s-t)} J
    # verify by differentiation under the integral (sympy) that both satisfy -X_tt + X_xx = J
    def duhamel(kind):
        if kind == 'ret':
            inner = sp.integrate(Jsrc.subs({tt: s, xx: r}), (r, xx - (tt - s), xx + (tt - s)))
            return -sp.Rational(1, 2) * sp.Integral(inner, (s, -sp.oo, tt))
        inner = sp.integrate(Jsrc.subs({tt: s, xx: r}), (r, xx - (s - tt), xx + (s - tt)))
        return -sp.Rational(1, 2) * sp.Integral(inner, (s, tt, sp.oo))
    for kind in ('ret', 'adv'):
        Xk = duhamel(kind)
        box = -sp.diff(Xk, tt, 2) + sp.diff(Xk, xx, 2)
        res = sp.simplify((box - Jsrc).doit())
        check(f"1+1 Duhamel {kind} solution satisfies the SAME local equation Box X = J", res == 0, f"residual={res}")
    print(f"  ({time.time()-t0:.1f}s)")

    # =====================================================================================
    hdr("VERDICT")
    # =====================================================================================
    print(f"""
      [SOLID]  The localized DW-2026 action is a diffeomorphism-invariant LOCAL functional of (g, X, xi, phi,
               lambda, M, nu, psi).  Its Noether identity  2 nabla^mu E_munu + sum_A E_A d_nu Phi_A == 0  holds
               OFF-SHELL, verified component-wise on a 4-function (t,x) metric with all seven fields arbitrary,
               for generic cubic f and for undefined f.  Analytic E_munu cross-checked against direct variation.
      [SOLID]  Corollary for THIS SYNTHESIZED LOCAL ACTION: on ANY solution of its auxiliary equations --
               retarded, advanced, or any other -- nabla^mu E^grav_munu = 0 identically, so the metric equation
               E^grav_munu = T_munu/2 is consistent, and nabla^mu T_munu = E_psi d_nu psi vanishes on the matter
               shell.  Baryons couple to g only.  => FRIED-CHICKEN req 5 (matter conservation as a consequence of
               the action) = PASS for this local representative.  The identity is boundary-condition blind.
               This does NOT prove that the local theory with independent auxiliaries is canonically equivalent
               to DW's metric-only retarded functional; that is a separate nonlocal prescription.
      [SOLID]  Mutation M3: conservation REQUIRES the clock-response stress lambda u_mu u_nu (the mimetic
               multiplier).  DW 2026 never writes the synthesized model's field equations; DEW 2014 eq (17) does
               include the analogous clock-response (psi and the u u u u R normalization term).  Any implementation
               that varies only the explicit metric dependence and treats phi[g] as inert is NOT conserved.
      SCOPE:   this settles CONSISTENCY (req 5), not degree-of-freedom content (req 2) -- see the Dirac script.
      checks passed: {sum(checks)}/{len(checks)}   runtime {time.time()-t0:.1f}s
    """)
    sys.exit(0 if all(checks) else 1)


if __name__ == '__main__':
    main()
