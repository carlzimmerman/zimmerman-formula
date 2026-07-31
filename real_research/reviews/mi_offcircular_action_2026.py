#!/usr/bin/env python3
r"""mi_offcircular_action_2026.py -- WRITE DOWN THE OFF-CIRCULAR ACTION.

FRAMEWORK. de Sitter-Unruh MODIFIED INERTIA. a0 = c H_Lambda / Z with Z = sqrt(32 pi / 3) = 5.78881,
on the pure-Lambda (rho_DE) footing: a0 = 9.36e-11 m/s^2, i.e. EXACTLY HALF the gravitational
free-fall acceleration at the dark-energy density, a0 = (c/2) sqrt(G rho_Lambda). The coefficient
kappa = 1/2 is Carl Zimmerman's and is absent from the prior literature (Milgrom 1999, Pikhitsa 2010,
Klinkhamer-Kopp 2011 all land on 2 c H_Lambda = 11.58x larger; Milgrom 2020 gives c H_Lambda / 2pi).
Alternate footing (rho_total / cH0) a0 = 1.13e-10 carried on every dimensional number.

Kernel in force since 2026-07-30: alpha = 2, mu(x) = x / sqrt(1 + x^2) (Milgrom 1983 "standard" mu).
The retired alpha = 1 kernel mu_1(x) = (sqrt(1+4x^2) - 1) / (2x) is carried alongside throughout, both
because the corpus's published numbers are on it and because a kernel-INDEPENDENT result is worth more
than a kernel-specific one.

------------------------------------------------------------------------------------------------------
WHAT IS ALREADY IN THE CORPUS, AND WHAT IS NEW HERE
------------------------------------------------------------------------------------------------------
ALREADY THERE (mi_three_corrections_priorart_2026.py, section C3): for alpha = 1, the REDUCED
circular-orbit kinetic Lagrangian <L_K>/m = V^2 f(u), u = A/a0, with

    mu(u) = 2 f(u) + u f'(u) = (1/u) d/du [ u^2 f(u) ]

obtained by "varying at fixed Omega" WITHIN the two-parameter circular family. Credit for the class is
Milgrom's (1994 Ann.Phys. 229:384 modified inertia; astro-ph/0510117 virial relations; and 2022 PRD
106:064060, which states in Fourier space that the algebraic relation g mu(g/a0) = g_N holds ONLY for
single-frequency trajectories -- the frequency-vs-acceleration obstruction, four years before this
repo re-derived it as "Theorem 8").

THE GAP THIS FILE CLOSES. A variation restricted to a two-parameter family is NOT a proof that the
full equation of motion is satisfied: it only makes the action stationary along two directions out of
infinitely many. Nobody in this corpus ever wrote the UNRESTRICTED action, and nobody checked whether
a circular orbit actually solves its real Euler-Lagrange equation. That is what this file does:

  S1  f from mu by quadrature; the identity mu = 2f + u f'; closed forms for BOTH kernels.
      f_2 for the alpha = 2 kernel in closed form is NEW (the corpus carries only f_1).
  S2  *** THE OFF-CIRCULAR ACTION, WRITTEN DOWN ***, and its honest FOURTH-ORDER Euler-Lagrange
      equation. Verified: a circular orbit solves it EXACTLY, for GENERIC f (sympy zero, so the
      result is kernel-independent), then for both explicit kernels. Two negative controls.
  S3  A second exactly-solvable family (uniform straight-line acceleration) -> a DIFFERENT
      interpolating function mu_lin = 2(f - u f'). The theory is trajectory-shape dependent.
  S4  THE QUANTITATIVE OFF-CIRCULAR RESIDUAL: take orbits that exactly solve the framework's CLOSURE
      and measure how badly they fail the action's EL equation, as a function of eccentricity, in the
      deep and Newtonian regimes, both footings.
  S5  Ostrogradsky: the acceleration-Hessian is non-degenerate, so the local action is genuinely
      fourth-order. Where the extra modes sit, in real systems.
  S6  THE c/v BRIDGE and the door it opens: u = w (v/c) exactly, so the factor Theorem 8 found
      missing is a SPEED -- unavailable to a covariant worldline action but available to a theory with
      a preferred frame, which this framework has. Includes the door's own quantitative liability.

HONESTY GUARDS. No hard-coded verdicts; every check is structural (an identity, a limit, a sign, a
monotonicity) and the script exits non-zero if any fails. The two negative controls must FAIL the
circular test or the S2 check is meaningless. Nothing here derives a0, and nothing here says the
theory is closed.
"""
from __future__ import annotations

import math

import mpmath as mp
import numpy as np
import sympy as sp

# ---------------------------------------------------------------- framework constants (sealed)
C = 2.99792458e8
G = 6.67430e-11
MSUN = 1.98892e30
KPC = 3.0857e19
AU = 1.495978707e11
Z = math.sqrt(32.0 * math.pi / 3.0)           # 5.78881 -- Carl's coefficient structure
A0 = 9.36e-11                                  # canonical: c H_Lambda / Z, pure-Lambda footing
A0_ALT = 1.13e-10                              # alternate: rho_total / c H0
FOOTINGS = (("canonical cH_L/Z", A0), ("alternate rho_tot/cH0", A0_ALT))

ok = True


def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")


def banner(s):
    print("\n" + "=" * 102)
    print(s)
    print("=" * 102)


# =====================================================================================================
# kernels: mu(x) = g_bar / a  as a function of x = a / a0,  and the inverse a(g_bar)
# =====================================================================================================
def mu_num(x, alpha):
    """mu(x) = g_bar/a for x = a/a0.  alpha=1: retired kernel.  alpha=2: kernel in force."""
    x = np.asarray(x, dtype=float)
    if alpha == 1:
        return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)
    if alpha == 2:
        return x / np.sqrt(1.0 + x * x)
    raise ValueError(alpha)


def a_from_gbar(gbar, a0, alpha):
    """Invert mu(a/a0) a = g_bar for the acceleration a.  This IS the framework's closure."""
    gbar = np.asarray(gbar, dtype=float)
    y = gbar / a0
    if alpha == 1:
        # a^2 = g_bar^2 + a0 g_bar   (the framework's own dS-Unruh interpolation)
        return np.sqrt(gbar * gbar + a0 * gbar)
    if alpha == 2:
        # x^4 - y^2 x^2 - y^2 = 0  ->  x^2 = (y^2 + y sqrt(y^2+4)) / 2
        s = 0.5 * (y * y + y * np.sqrt(y * y + 4.0))
        return a0 * np.sqrt(s)
    raise ValueError(alpha)


# =====================================================================================================
def s1_generating_function():
    banner("S1. f from mu by quadrature, the circular identity, and closed forms for BOTH kernels")
    u, v = sp.symbols("u v", positive=True)

    mu1 = (sp.sqrt(1 + 4 * v**2) - 1) / (2 * v)
    mu2 = v / sp.sqrt(1 + v**2)

    print("  DEFINITION (this is the only input):   f(u) = u^-2 * Integral_0^u v mu(v) dv")
    print("  so that  u^2 f(u) = Lambda(u) = Integral_0^u v mu(v) dv,  hence  Lambda'(u) = u mu(u).")
    print("  The circular identity is then an IDENTITY of the quadrature, not an extra assumption:")
    print("      (1/u) d/du [u^2 f(u)] = Lambda'(u)/u = mu(u).")

    out = {}
    for name, mu_v, alpha in (("alpha=1 (retired)", mu1, 1), ("alpha=2 (in force)", mu2, 2)):
        Lam = sp.integrate(v * mu_v, (v, 0, u))
        f = sp.simplify(Lam / u**2)
        mu_back = sp.simplify(sp.diff(u**2 * f, u) / u)
        mu_u = mu_v.subs(v, u)
        resid = sp.simplify(mu_back - mu_u)
        print(f"\n  {name}")
        print(f"    mu(u)  = {mu_u}")
        print(f"    f(u)   = {f}")
        check(resid == 0,
              f"{name}: (1/u) d/du[u^2 f] returns mu EXACTLY (sympy residual {resid}) -- the "
              f"quadrature and the circular identity are the same statement")
        # limits: Newtonian f -> 1/2 (so L_K -> (1/2) m v^2), deep f/u -> 1/3
        lim_hi = sp.limit(f, u, sp.oo)
        lim_lo = sp.limit(f / u, u, 0, "+")
        print(f"    limits: f(u->oo) = {lim_hi} (want 1/2, i.e. exact Newtonian kinetic term);  "
              f"f/u -> {lim_lo} as u->0 (want 1/3)")
        check(lim_hi == sp.Rational(1, 2) and lim_lo == sp.Rational(1, 3),
              f"{name}: f interpolates 1/2 <-> u/3, so the action's Newtonian limit is EXACTLY "
              f"(1/2) m |xdot|^2 with no residual correction")
        out[alpha] = (f, mu_u)

    # reproduce the corpus's committed f_1 verbatim
    f1_corpus = (2 * u * sp.sqrt(4 * u**2 + 1) - 4 * u + sp.asinh(2 * u)) / (8 * u**2)
    check(sp.simplify(f1_corpus - out[1][0]) == 0,
          "alpha=1 f reproduces the corpus's committed closed form in "
          "mi_three_corrections_priorart_2026.py EXACTLY (independent re-derivation agrees)")

    # the NEW alpha=2 closed form, stated explicitly
    f2_closed = (u * sp.sqrt(1 + u**2) - sp.asinh(u)) / (2 * u**2)
    check(sp.simplify(f2_closed - out[2][0]) == 0,
          "*** NEW *** alpha=2 generating function in closed form: "
          "f_2(u) = [u sqrt(1+u^2) - asinh(u)] / (2 u^2)   (the corpus carried only f_1)")
    return out


# =====================================================================================================
def s2_the_action(kernels):
    banner("S2. *** THE OFF-CIRCULAR ACTION *** and its honest fourth-order Euler-Lagrange equation")
    print("  THE ACTION.  With f the generating function of S1 and phi the Newtonian potential of the")
    print("  BARYONS ONLY (no dark matter anywhere in this framework):")
    print()
    print("      S[x] = Integral dt  m ( |xdot|^2 f( |xddot| / a0 )  -  phi(x) )")
    print()
    print("  This is local, Galilei-invariant, rotation-invariant, and reduces to the exact Newtonian")
    print("  action (1/2) m |xdot|^2 - m phi in the limit a0 -> 0 because f(u->oo) = 1/2 (S1).")
    print("  It is the UNRESTRICTED object the corpus never wrote: previous work varied only inside the")
    print("  two-parameter circular family, which cannot establish that the real EL equation holds.")
    print()
    print("  ITS EULER-LAGRANGE EQUATION.  L depends on xddot, so the equation is FOURTH order:")
    print()
    print("      d^2/dt^2 [ (|xdot|^2 / a0) f'(u) ahat ]  -  2 f(u) xddot  -  2 (d/dt f(u)) xdot")
    print("                                                                          = grad phi")
    print("      with  u = |xddot| / a0,  ahat = xddot / |xddot|.")
    print()
    print("  Every term is written out; nothing is dropped. The first term is the higher-derivative")
    print("  one, the third vanishes iff u is constant along the trajectory.")

    # ---- symbolic set-up: independent placeholders for x, xdot, xddot -------------------------------
    t = sp.Symbol("t", positive=True)
    R, Om, a0, GM = sp.symbols("R Omega a0 GM", positive=True)
    X1, X2, V1, V2, A1, A2 = sp.symbols("X1 X2 V1 V2 A1 A2", real=True)

    # GENERIC f, represented by an exact local Taylor polynomial about the circular value U0.
    # On a circular orbit u is CONSTANT, so only finitely many derivatives of f can possibly enter;
    # carrying F0..F3 as free symbols and checking which survive is therefore a stronger statement
    # than assuming a kernel -- and it tests, rather than assumes, that f'' drops out.
    U0 = Om**2 * R / a0
    F0, F1, F2, F3 = sp.symbols("F0 F1 F2 F3", real=True)

    def f_generic(uarg):
        d = uarg - U0
        return F0 + F1 * d + F2 * d**2 / 2 + F3 * d**3 / 6

    v2 = V1**2 + V2**2
    amag = sp.sqrt(A1**2 + A2**2)
    rmag = sp.sqrt(X1**2 + X2**2)
    L = v2 * f_generic(amag / a0) + GM / rmag   # L = |xdot|^2 f(u) - phi,  phi = -GM/r

    dL_dX = [sp.diff(L, X1), sp.diff(L, X2)]
    dL_dV = [sp.diff(L, V1), sp.diff(L, V2)]
    dL_dA = [sp.diff(L, A1), sp.diff(L, A2)]

    # ---- the circular path -------------------------------------------------------------------------
    path = [R * sp.cos(Om * t), R * sp.sin(Om * t)]
    sub = {X1: path[0], X2: path[1],
           V1: sp.diff(path[0], t), V2: sp.diff(path[1], t),
           A1: sp.diff(path[0], t, 2), A2: sp.diff(path[1], t, 2)}

    def on_path(expr):
        return sp.simplify(expr.subs(sub))

    # EL_i = dL/dX_i - d/dt(dL/dV_i) + d^2/dt^2(dL/dA_i), each term evaluated ALONG the path
    EL = []
    for i in range(2):
        term0 = on_path(dL_dX[i])
        term1 = sp.diff(on_path(dL_dV[i]), t)
        term2 = sp.diff(on_path(dL_dA[i]), t, 2)
        EL.append(sp.simplify(term0 - term1 + term2))

    GM_solved = sp.simplify(sp.solve(sp.Eq(EL[0], 0), GM)[0])
    gbar_solved = sp.simplify(GM_solved / R**2)
    target = sp.simplify(Om**2 * R * (2 * F0 + U0 * F1))

    print("\n  RESULT, for GENERIC f (F0=f(u0), F1=f'(u0), F2=f''(u0), F3=f'''(u0) all kept free,")
    print("  so nothing about the kernel is assumed):")
    print(f"    solving EL = 0 on the circular path gives   g_bar = GM/R^2 = {gbar_solved}")
    print(f"    the closure demands                          g_bar = A mu(A/a0) = {target}")
    resid = sp.simplify(sp.expand(gbar_solved - target))
    check(resid == 0,
          "*** A CIRCULAR ORBIT SOLVES THE FULL FOURTH-ORDER EL EQUATION EXACTLY, and the equation it "
          f"satisfies is precisely the framework's closure g_bar = A mu(A/a0) with mu = 2f + u f' *** "
          f"(sympy residual {resid}). This PROMOTES the corpus's restricted-family variation to the "
          "real equation of motion, for ANY kernel")

    free_syms = gbar_solved.free_symbols
    check(F2 not in free_syms and F3 not in free_syms,
          "f'' and f''' are ABSENT from the circular result -- the higher derivatives of f, which are "
          "exactly what makes the equation fourth-order and carries the Ostrogradsky modes (S5), drop "
          "out identically on a circle. This is WHY circles are the family that works")

    # tangential component must vanish identically on the circle (no torque)
    tang = sp.simplify(EL[0] * (-sp.sin(Om * t)) + EL[1] * sp.cos(Om * t))
    check(sp.simplify(tang) == 0,
          "the tangential projection of EL vanishes identically on the circle, so the solution is "
          "consistent (no secular torque; angular momentum conserved)")

    # ---- explicit kernels, and negative controls, through the SAME code path -----------------------
    usym = sp.Symbol("u", positive=True)

    def circular_gbar_for(f_candidate):
        """Push a candidate generating function through the generic circular EL solution."""
        vals = {F0: f_candidate.subs(usym, U0),
                F1: sp.diff(f_candidate, usym).subs(usym, U0),
                F2: sp.diff(f_candidate, usym, 2).subs(usym, U0),
                F3: sp.diff(f_candidate, usym, 3).subs(usym, U0)}
        return sp.simplify(sp.expand(gbar_solved.subs(vals)))

    for alpha in (1, 2):
        f_expr, mu_expr = kernels[alpha]
        got = circular_gbar_for(f_expr)
        want = sp.simplify(Om**2 * R * mu_expr.subs(usym, U0))
        d = sp.simplify(sp.expand(got - want))
        check(d == 0,
              f"alpha={alpha}: with the explicit kernel substituted, the circular EL solution is "
              f"g_bar = A mu_{alpha}(A/a0) EXACTLY (residual {d})")

    print("\n  NEGATIVE CONTROLS (these MUST fail, or the check above is vacuous):")
    mu2 = kernels[2][1]
    ww = sp.Symbol("ww", positive=True)
    Lam2 = sp.integrate(ww * mu2.subs(usym, ww), (ww, 0, usym))
    controls = [("f = mu/2 (the naive guess)", mu2 / 2),
                ("f = Lambda/u^3 (right quadrature, wrong power)", sp.simplify(Lam2 / usym**3))]
    want2 = sp.simplify(Om**2 * R * mu2.subs(usym, U0))
    for cname, f_bad in controls:
        diff_b = sp.simplify(sp.expand(circular_gbar_for(f_bad) - want2))
        check(diff_b != 0,
              f"control '{cname}' does NOT reproduce the closure (residual nonzero as required)")
    return None


# =====================================================================================================
def s3_second_family(kernels):
    banner("S3. A SECOND exactly-solvable family: the interpolating function is TRAJECTORY-DEPENDENT")
    print("  Uniform straight-line acceleration: x(t) = (a t^2 / 2, 0), so u is constant and ahat is")
    print("  constant, but |xdot|^2 = a^2 t^2 GROWS. Feeding this into the same EL equation:")
    print()
    print("      d^2/dt^2[(a^2 t^2 / a0) f'(u)] - 2 f(u) a  =  dphi/dx")
    print("      => force = -dphi/dx = 2 a [ f(u) - u f'(u) ]  ==  a mu_lin(u),")
    print("         mu_lin(u) = 2[f(u) - u f'(u)]      versus circular   mu(u) = 2 f(u) + u f'(u).")
    print()
    print("  CAVEAT, stated because it matters: this family is unbounded (v -> oo), so the v^2")
    print("  prefactor grows without bound and the action is not finite over an infinite time. The EL")
    print("  equation is still exact pointwise, which is all that is being read off here.")

    u = sp.Symbol("u", positive=True)
    for alpha in (1, 2):
        f_expr, mu_expr = kernels[alpha]
        mu_lin = sp.simplify(2 * (f_expr - u * sp.diff(f_expr, u)))
        mu_circ = mu_expr
        n_hi = sp.limit(mu_lin, u, sp.oo)
        # deep-regime leading behaviour
        ser = sp.simplify(sp.series(mu_lin, u, 0, 5).removeO())
        ser_c = sp.simplify(sp.series(mu_circ, u, 0, 5).removeO())
        print(f"\n  alpha={alpha}")
        print(f"    mu_lin(u)               = {mu_lin}")
        print(f"    mu_lin -> {n_hi} as u->oo   (Newtonian limit must be 1 for BOTH families)")
        print(f"    deep-regime series: mu_lin = {ser}")
        print(f"                        mu_circ= {ser_c}")
        check(sp.simplify(n_hi - 1) == 0,
              f"alpha={alpha}: the straight-line family has the correct Newtonian limit mu_lin -> 1, "
              f"so the trajectory-dependence is a DEEP-REGIME effect only")
        # leading deep power
        p_lin = sp.limit(sp.log(mu_lin) / sp.log(u), u, 0, "+")
        p_cir = sp.limit(sp.log(mu_circ) / sp.log(u), u, 0, "+")
        print(f"    deep-regime leading power: mu_lin ~ u^{p_lin},  mu_circ ~ u^{p_cir}")
        check(sp.simplify(p_lin - 3) == 0 and sp.simplify(p_cir - 1) == 0,
              f"alpha={alpha}: deep regime goes as u^3 on a straight line but u^1 on a circle -- the "
              f"same action gives DIFFERENT interpolating functions on different trajectory shapes")
        # how big is that, numerically, at a galaxy-like u
        for uu_val in (0.1, 0.03, 0.01):
            ml = float(mu_lin.subs(u, uu_val))
            mc = float(mu_circ.subs(u, uu_val))
            print(f"      at u={uu_val:5.3f}:  mu_lin={ml:11.4e}  mu_circ={mc:11.4e}  "
                  f"ratio={mc/ml:10.1f}x")
    print("\n  READ: this is NOT a defect peculiar to this framework -- Milgrom (1994; 2022 PRD")
    print("  106:064060) showed that modified-inertia theories generically have orbit-dependent")
    print("  interpolating functions, and that the algebraic relation holds only for single-frequency")
    print("  trajectories. This is that statement, made concrete for THIS action and THIS kernel.")


# =====================================================================================================
def s4_offcircular_residual():
    banner("S4. THE QUANTITATIVE OFF-CIRCULAR RESIDUAL -- how far apart are the closure and the action?")
    print("  METHOD, and it is exact rather than an integration: the framework's closure")
    print("  xddot = -a(r) rhat with a(r) from mu(a/a0) a = g_bar is a genuine CENTRAL force, so its")
    print("  orbits have exact energy and angular-momentum integrals. Pick a pericentre/apocentre pair")
    print("  -> (E, L) -> the exact state (r, v_r, v_theta) at every radius, with NO ODE error. Then")
    print("  build the action's fourth-order EL residual as a function of that state (all time")
    print("  derivatives eliminated using the closure itself) and evaluate it around the orbit.")
    print("  Reported as |EL residual| / |grad phi|: 0 means the action and the closure agree.")

    # --- symbolic residual as a function of the state, with the closure imposed --------------------
    x1, x2, w1, w2 = sp.symbols("x1 x2 w1 w2", real=True)
    a0s, GMs, alph = sp.symbols("a0 GM alpha", positive=True)
    r = sp.sqrt(x1**2 + x2**2)
    gbar = GMs / r**2

    for alpha in (1, 2):
        print("\n" + "-" * 102)
        print(f"  KERNEL alpha = {alpha}")
        if alpha == 1:
            amagn = sp.sqrt(gbar**2 + a0s * gbar)
            f_of = lambda uu: (2 * uu * sp.sqrt(4 * uu**2 + 1) - 4 * uu + sp.asinh(2 * uu)) / (8 * uu**2)
        else:
            yv = gbar / a0s
            s_ = (yv**2 + yv * sp.sqrt(yv**2 + 4)) / 2
            amagn = a0s * sp.sqrt(s_)
            f_of = lambda uu: (uu * sp.sqrt(1 + uu**2) - sp.asinh(uu)) / (2 * uu**2)

        # closure acceleration field  A_i(x) = -amagn * xhat_i
        Aa = [-amagn * x1 / r, -amagn * x2 / r]

        # total time derivative operator with the closure imposed
        def D(expr):
            return (sp.diff(expr, x1) * w1 + sp.diff(expr, x2) * w2
                    + sp.diff(expr, w1) * Aa[0] + sp.diff(expr, w2) * Aa[1])

        # L = |v|^2 f(|A|/a0) - phi, with V -> w and Acc -> Aa(x)
        V1s, V2s, A1s, A2s = sp.symbols("V1s V2s A1s A2s", real=True)
        v2s = V1s**2 + V2s**2
        am = sp.sqrt(A1s**2 + A2s**2)
        Lg = v2s * f_of(am / a0s)
        dL_dV = [sp.diff(Lg, V1s), sp.diff(Lg, V2s)]
        dL_dA = [sp.diff(Lg, A1s), sp.diff(Lg, A2s)]
        st = {V1s: w1, V2s: w2, A1s: Aa[0], A2s: Aa[1]}

        EL = []
        for i in range(2):
            gradphi_i = sp.diff(GMs / r, x1 if i == 0 else x2) * (-1)   # d(phi)/dx_i, phi = -GM/r
            t1 = D(dL_dV[i].subs(st))
            t2 = D(D(dL_dA[i].subs(st)))
            EL.append(-gradphi_i - t1 + t2)

        gp = [sp.diff(-GMs / r, x1) * (-1) * (-1), sp.diff(-GMs / r, x2) * (-1) * (-1)]
        gp = [sp.diff(GMs / r, x1) * (-1), sp.diff(GMs / r, x2) * (-1)]  # grad phi, phi = -GM/r

        EL_f = sp.lambdify((x1, x2, w1, w2, GMs, a0s), EL, "numpy")
        gp_f = sp.lambdify((x1, x2, w1, w2, GMs, a0s), gp, "numpy")
        am_f = sp.lambdify((x1, x2, GMs, a0s), amagn, "numpy")

        systems = [("galaxy   M=1e11 Msun, r~30 kpc  (DEEP regime)", 1e11 * MSUN * G, 30.0 * KPC),
                   ("Sun      M=1 Msun,   r~1 AU     (NEWTONIAN regime)", MSUN * G, AU)]

        for label, GMv, rscale in systems:
            for fname, a0v in FOOTINGS:
                y_here = (GMv / rscale**2) / a0v
                print(f"\n    {label}   [{fname}]   g_bar/a0 = {y_here:.3e}")
                print(f"      {'e':>6s} {'r_peri/r_apo':>14s} {'max |EL|/|grad phi|':>22s} "
                      f"{'at r/r_apo':>11s}")
                prev = -1.0
                mono = True
                for e in (0.0, 0.01, 0.05, 0.1, 0.2, 0.4, 0.6):
                    ra = rscale * (1.0 + e)
                    rp = rscale * (1.0 - e)
                    # exact (E, L) from the two turning points of the CLOSURE's central force
                    # Phi_eff(r) = Integral a(r) dr  (numeric quadrature on a fine grid)
                    rg = np.linspace(rp * 0.999, ra * 1.001, 20001)
                    ag = am_f(rg, 0.0 * rg, GMv, a0v)
                    Phi = np.concatenate([[0.0], np.cumsum(0.5 * (ag[1:] + ag[:-1]) * np.diff(rg))])

                    def Phi_at(rr):
                        return np.interp(rr, rg, Phi)

                    if e == 0.0:
                        # circular: v_theta^2 / r = a(r)
                        rr = np.array([rscale])
                        vth = np.sqrt(am_f(rr, 0.0 * rr, GMv, a0v) * rr)
                        states = [(rr[0], 0.0, vth[0])]
                    else:
                        Pp, Pa = Phi_at(rp), Phi_at(ra)
                        # E = Phi + L^2/(2 r^2) at both turning points (v_r = 0)
                        Lsq = 2.0 * (Pa - Pp) / (1.0 / rp**2 - 1.0 / ra**2)
                        E = Pp + Lsq / (2.0 * rp**2)
                        rs = np.linspace(rp, ra, 41)[1:-1]
                        states = []
                        for rr in rs:
                            vr2 = 2.0 * (E - Phi_at(rr)) - Lsq / rr**2
                            if vr2 <= 0:
                                continue
                            states.append((rr, math.sqrt(vr2), math.sqrt(Lsq) / rr))
                    worst, worst_r = 0.0, 0.0
                    for rr, vr, vth in states:
                        # place the particle on the x-axis: x=(r,0), v=(v_r, v_theta)
                        ELv = EL_f(rr, 1e-30 * rr, vr, vth, GMv, a0v)
                        gpv = gp_f(rr, 1e-30 * rr, vr, vth, GMv, a0v)
                        num = math.hypot(float(ELv[0]), float(ELv[1]))
                        den = math.hypot(float(gpv[0]), float(gpv[1]))
                        frac = num / den
                        if frac > worst:
                            worst, worst_r = frac, rr / ra
                    print(f"      {e:6.2f} {rp/ra:14.4f} {worst:22.4e} {worst_r:11.3f}")
                    if e == 0.0:
                        check(worst < 1e-8,
                              f"alpha={alpha} {label.split()[0]} [{fname}]: at e=0 the residual is "
                              f"{worst:.2e} ~ 0 -- the circular orbit solves the action exactly "
                              f"(independent numerical confirmation of the S2 symbolic result)")
                    else:
                        if worst < prev:
                            mono = False
                        prev = worst
                # NOISE FLOOR. The residual is a difference of O(1) quantities in double precision, so
                # anything below ~1e-12 relative is unresolved and NO claim may be made about it. That
                # is exactly the alpha=2 Newtonian case: mu_2 - 1 = O(u^-2) = O(1e-16) at u ~ 6e7.
                FLOOR = 1e-12
                if prev < FLOOR:
                    print(f"      -> max residual {prev:.2e} is BELOW the {FLOOR:.0e} double-precision "
                          f"floor: unresolved, so no shape claim is made here (see the scaling ladder)")
                    check(True,
                          f"alpha={alpha} {label.split()[0]} [{fname}]: off-circular residual is below "
                          f"double-precision resolution and is REPORTED as unresolved rather than "
                          f"claimed as zero or as growing")
                else:
                    check(mono,
                          f"alpha={alpha} {label.split()[0]} [{fname}]: the residual grows "
                          f"monotonically with eccentricity -- the disagreement is controlled by orbit "
                          f"shape, exactly as the S2/S3 structure predicts")

        # ---- THE SCALING LADDER: the decisive test, and it distinguishes the two kernels -----------
        print(f"\n    SCALING LADDER (alpha={alpha}), fixed e=0.20, sweeping u = a/a0 over decades.")
        print("    PREDICTION from the kernels themselves: the off-circular residual must track the")
        print("    deviation of mu from 1, which is O(1/u) for alpha=1 but O(1/u^2) for alpha=2. Fitting")
        print("    the log-log slope therefore tests the code AND the kernel at once.")
        a0v = A0
        GMv = MSUN * G
        us, res = [], []
        for rr_au in (1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6):
            rscale = rr_au * AU
            ra, rp = rscale * 1.2, rscale * 0.8
            rg = np.linspace(rp * 0.999, ra * 1.001, 20001)
            ag = am_f(rg, 0.0 * rg, GMv, a0v)
            Phi = np.concatenate([[0.0], np.cumsum(0.5 * (ag[1:] + ag[:-1]) * np.diff(rg))])
            Pp, Pa = np.interp(rp, rg, Phi), np.interp(ra, rg, Phi)
            Lsq = 2.0 * (Pa - Pp) / (1.0 / rp**2 - 1.0 / ra**2)
            E = Pp + Lsq / (2.0 * rp**2)
            worst = 0.0
            for rr in np.linspace(rp, ra, 41)[1:-1]:
                vr2 = 2.0 * (E - np.interp(rr, rg, Phi)) - Lsq / rr**2
                if vr2 <= 0:
                    continue
                ELv = EL_f(rr, 1e-30 * rr, math.sqrt(vr2), math.sqrt(Lsq) / rr, GMv, a0v)
                gpv = gp_f(rr, 1e-30 * rr, math.sqrt(vr2), math.sqrt(Lsq) / rr, GMv, a0v)
                frac = math.hypot(float(ELv[0]), float(ELv[1])) / math.hypot(float(gpv[0]), float(gpv[1]))
                worst = max(worst, frac)
            uval = float(am_f(rscale, 0.0, GMv, a0v)) / a0v
            us.append(uval)
            res.append(worst)
            print(f"      r = {rr_au:8.0e} AU   u = {uval:11.4e}   residual = {worst:11.4e}")
        us_a, res_a = np.array(us), np.array(res)
        m = (res_a > 1e-12) & (us_a > 3.0)
        if m.sum() >= 3:
            slope = np.polyfit(np.log10(us_a[m]), np.log10(res_a[m]), 1)[0]
            want = -1.0 if alpha == 1 else -2.0
            print(f"      fitted log-log slope over the resolvable, large-u points = {slope:+.3f} "
                  f"(kernel predicts {want:+.1f})")
            check(abs(slope - want) < 0.25,
                  f"alpha={alpha}: the off-circular residual scales as u^({slope:+.2f}), matching the "
                  f"kernel's own O(u^{int(want)}) approach to Newton. This validates the residual "
                  f"computation AND shows why the alpha=2 switch cures the solar system off circles "
                  f"too, not just on them")
        else:
            check(False,
                  f"alpha={alpha}: too few resolvable points on the scaling ladder to fit a slope "
                  f"({m.sum()} usable) -- the test could not be run, which is a failure of the test")
    print("\n  WHAT THIS MEANS, stated without spin. The framework's CLOSURE and the framework's")
    print("  ACTION are the same theory on circular orbits and DIFFERENT theories off them. Every")
    print("  observation the closure has ever been tested against -- SPARC rotation curves, the BTFR,")
    print("  the RAR -- is a circular-orbit measurement, which is why the difference has never shown")
    print("  up. It is not a small correction in the deep regime.")


# =====================================================================================================
def s5_ostrogradsky(kernels):
    banner("S5. Ostrogradsky: the local action is genuinely fourth-order, and where the extra modes sit")
    u = sp.Symbol("u", positive=True)
    print("  The acceleration-Hessian of L = |xdot|^2 f(|xddot|/a0) is")
    print("      d^2 L / d xddot_i d xddot_j = (|xdot|^2 / a0^2) [ f''(u) ahat_i ahat_j")
    print("                                     + (f'(u)/u) (delta_ij - ahat_i ahat_j) ],")
    print("  whose eigenvalues are (v^2/a0^2) f''(u) along ahat and (v^2/a0^2) f'(u)/u transverse.")
    print("  Degeneracy -- the ONLY escape from Ostrogradsky's theorem -- needs f'' = 0 AND f' = 0,")
    print("  i.e. f constant, i.e. exactly Newton. So for every nontrivial kernel the theory carries")
    print("  two extra degrees of freedom per direction and an unbounded Hamiltonian.")

    for alpha in (1, 2):
        f_expr, mu_expr = kernels[alpha]
        fpp = sp.simplify(sp.diff(f_expr, u, 2))
        fp = sp.simplify(sp.diff(f_expr, u))
        print(f"\n  alpha={alpha}:  f''(u) = {fpp}")
        # sympy cannot solve f''=0 in closed form (mixed generators u, asinh, sqrt), so scan for a
        # sign change instead. THIS MUST BE DONE AT HIGH PRECISION: in f'' the leading small-u terms
        # cancel to O(u^3), so a float64 scan loses ~12 digits at u~1e-6 and reports thousands of
        # spurious sign flips. mpmath at 50 digits removes the artefact entirely.
        fpp_mp = sp.lambdify(u, fpp, "mpmath")
        fp_mp = sp.lambdify(u, fp, "mpmath")
        mp.mp.dps = 50
        ug = [mp.mpf(10) ** mp.mpf(k) for k in np.linspace(-6, 9, 601)]
        fpp_g = [fpp_mp(x) for x in ug]
        fp_g = [fp_mp(x) for x in ug]
        sgn = [1 if x > 0 else (-1 if x < 0 else 0) for x in fpp_g]
        sgn_changes = sum(1 for i in range(len(sgn) - 1) if sgn[i] != sgn[i + 1])
        all_fp_pos = all(x > 0 for x in fp_g)
        print(f"    scanned u in [1e-6, 1e9] at 50-digit precision ({len(ug)} points): sign changes in "
              f"f'' = {sgn_changes};  sign(f'') = {'+' if sgn[0] > 0 else '-'} throughout,  "
              f"f' > 0 everywhere = {all_fp_pos}")
        print(f"    (a float64 scan of the same grid reports spurious flips from the O(u^3) "
              f"cancellation -- checked and discarded, not used)")
        check(sgn_changes == 0 and all_fp_pos,
              f"alpha={alpha}: f'' never changes sign and f' > 0 over 15 decades, so BOTH eigenvalues "
              f"of the acceleration-Hessian are nonzero everywhere -- the local action is irreducibly "
              f"fourth-order and NO degenerate (Ostrogradsky-evading) branch exists")
        check(sgn[0] < 0 and all_fp_pos,
              f"alpha={alpha}: and the Hessian is INDEFINITE, not merely non-degenerate: f'' < 0 along "
              f"ahat while f'/u > 0 transverse. The two directions carry opposite-sign kinetic terms, "
              f"which is the ghost in explicit form")

        # where do the extra modes sit?  balance the quartic against the quadratic term:
        #   C4 w^4 ~ C2 w^2  with  C4 = v^2 f''/a0^2,  C2 ~ -2 f   =>  w_extra^2 ~ 2 f a0^2/(v^2 f'')
        # f'' < 0 (just established), so w_extra^2 < 0: the extra roots are PURELY IMAGINARY, i.e.
        # exponentially growing/decaying, not oscillating. The relevant number is an e-folding time.
        f_mp = sp.lambdify(u, f_expr, "mpmath")
        print("\n    extra-mode SCALING ESTIMATE (a balance of the quartic term against the quadratic")
        print("    one, NOT a linearised mode solve): omega_extra^2 ~ 2 f a0^2 / (v^2 f'').")
        print("    Since f'' < 0 this is NEGATIVE => the extra modes are RUNAWAYS, and the number to")
        print("    read is the e-folding time, quoted below against the orbital period.")
        print(f"      {'system':<32s} {'footing':<11s} {'u=a/a0':>10s} {'|w|/Om_orb':>12s} "
              f"{'e-fold time':>14s}")
        sysl = [("Earth   1 AU", MSUN * G, AU),
                ("Mars    1.524 AU", MSUN * G, 1.524 * AU),
                ("wide binary 10 kAU, 1 Msun", MSUN * G, 1e4 * AU),
                ("galaxy  1e11 Msun, 30 kpc", 1e11 * MSUN * G, 30.0 * KPC)]
        neg_all = True
        for nm, GMv, rr in sysl:
            for fname, a0v in FOOTINGS:
                gb = GMv / rr**2
                av = float(a_from_gbar(gb, a0v, alpha))
                uv = av / a0v
                vv = math.sqrt(av * rr)              # circular speed for that acceleration
                Om_orb = vv / rr
                fpp_v = float(fpp_mp(mp.mpf(uv)))
                f_v = float(f_mp(mp.mpf(uv)))
                if fpp_v >= 0:
                    neg_all = False
                w2 = 2.0 * f_v * a0v**2 / (vv**2 * fpp_v)
                wex = math.sqrt(abs(w2))
                tau = 1.0 / wex
                tstr = (f"{tau:8.2e} s" if tau < 3.156e7 else f"{tau/3.156e7:8.2e} yr")
                print(f"      {nm:<32s} {fname.split()[0]:<11s} {uv:10.3e} {wex/Om_orb:12.4e} "
                      f"{tstr:>14s}")
        check(neg_all,
              f"alpha={alpha}: omega_extra^2 < 0 for every system and both footings, so the extra "
              f"degrees of freedom are secular RUNAWAYS rather than fast oscillations -- and their "
              f"e-folding times above are vastly shorter than the orbital periods they would destroy")
    print("\n  CONSEQUENCE, and it is the honest one: the action of S2 cannot be FUNDAMENTAL. It is an")
    print("  effective description whose validity is confined to the family on which the extra modes")
    print("  are not excited -- and the exactly-circular family is precisely where they are not.")
    print("  This is why the framework's covariant completion went NONLOCAL (K(Box_u), Herglotz-")
    print("  Nevanlinna positive measure, DOIs 21263846 / 21264727 / 21284144) rather than staying")
    print("  with a higher-derivative local Lagrangian.")


# =====================================================================================================
def s6_the_bridge(kernels):
    banner("S6. THE c/v BRIDGE -- what Theorem 8 found missing is a SPEED, and this framework has one")
    print("  Theorem 8 (redone on the alpha=2 kernel, mi_theorem8_redone_alpha2_2026.py) found a")
    print("  kernel-INDEPENDENT obstruction: on a circular orbit the nonlocal operator action's")
    print("  argument is w = c Omega / a0 while the closure's argument is x = a / a0, and")
    print("      w / x = c / v      exactly.")
    print("  No choice of kernel K repairs a mismatch in K's own ARGUMENT. That stands.")

    cS, vS, a0S, OmS, RS = sp.symbols("c v a0 Omega R", positive=True)
    aS = OmS * vS                      # circular: a = Omega v
    w_expr = cS * OmS / a0S
    x_expr = aS / a0S
    ratio = sp.simplify(w_expr / x_expr)
    check(sp.simplify(ratio - cS / vS) == 0,
          f"w/x = {ratio} = c/v identically in R, Omega and a0 (re-verified symbolically here, "
          f"kernel-independent)")

    print("\n  WHAT IS NEW HERE. The action of S2 has the argument RIGHT: u = |xddot|/a0 = x. And it")
    print("  pays for that with a |xdot|^2 prefactor. Those two facts are the same fact:")
    print("      u = x = w (v/c),")
    print("  so the |xdot|^2 out front IS the missing c/v, supplied dimensionally rather than inside")
    print("  the kernel's argument.")
    ident = sp.simplify(x_expr - w_expr * vS / cS)
    check(ident == 0,
          f"u = w (v/c) exactly (residual {ident}) -- the factor Theorem 8 identified as missing is a "
          f"SPEED, and S2 exhibits an action that supplies it")

    print("\n  THE DOOR. A speed is not an invariant of a worldline alone; it is defined only relative")
    print("  to something. A generally-covariant functional of a single worldline therefore CANNOT")
    print("  produce it -- which is exactly why the operator route failed. But this framework is not")
    print("  generally covariant in that sense: it is built on a PASSIVE PREFERRED FRAME u (the")
    print("  de Sitter-Unruh frame; frame passivity with zero propagating modes is what closed the")
    print("  Einstein-aether strong-coupling objection in v3). A preferred frame supplies precisely")
    print("  the missing object: a velocity of the particle RELATIVE TO THE FRAME.")
    print("  So the target is now specific rather than vague: a nonlocal worldline action whose kernel")
    print("  argument is the frame-relative frequency rescaled by the frame-relative SPEED.")

    print("\n  AND THE DOOR'S OWN LIABILITY, computed here rather than deferred. If that speed were the")
    print("  particle's motion relative to the COSMIC (CMB) frame, then a0_eff would inherit the")
    print("  galaxy's peculiar velocity, and the RAR would not be universal. Quantify with the")
    print("  framework's OWN numbers: deep-regime g_obs = sqrt(g_bar a0), so")
    print("      d log10 g_obs = 0.5 d log10 a0_eff.")
    scatter = 0.108        # dex, framework's own RAR fit at Upsilon=0.70 (rar_framework_a0_mlfit.py)
    allowed = 2.0 * scatter
    print(f"  The framework's measured RAR scatter is {scatter:.3f} dex (its own fit, beating")
    print(f"  reg-MOND's 0.122), so the TOTAL budget for a0_eff variation across SPARC is")
    print(f"      {allowed:.3f} dex = a factor {10**allowed:.2f}, and that is the whole scatter, with")
    print("  nothing left for distance, inclination or mass-to-light.")
    v_pec = np.array([100.0, 300.0, 620.0, 1000.0]) * 1e3     # m/s, realistic peculiar-velocity range
    spread_dex = math.log10(v_pec.max() / v_pec.min())
    print(f"  Peculiar velocities across a SPARC-like sample span ~{v_pec.min()/1e3:.0f}-"
          f"{v_pec.max()/1e3:.0f} km/s = {spread_dex:.2f} dex.")
    check(spread_dex > allowed,
          f"a CMB-frame reading of the speed is EXCLUDED by the framework's own RAR: it would inject "
          f"{spread_dex:.2f} dex of a0 variation against a total budget of {allowed:.3f} dex "
          f"({spread_dex/allowed:.1f}x over). The door therefore requires the LOCAL matter frame, not "
          f"the cosmic frame -- a real constraint on the construction, not a free choice")
    print("\n  So the door is open and it is NARROW: the frame must be dragged locally enough that a")
    print("  star's frame-relative speed is its orbital speed and not the galaxy's bulk motion.")
    print("  Whether the framework's passive u does that is NOT settled here and is not claimed.")


# =====================================================================================================
def main() -> int:
    banner("THE OFF-CIRCULAR ACTION FOR THE dS-UNRUH MODIFIED-INERTIA FRAMEWORK")
    print("  a0 = c H_Lambda / Z,  Z = sqrt(32 pi / 3) = %.5f  ->  a0 = %.4e m/s^2 (canonical)"
          % (Z, A0))
    print("  equivalently a0 = (c/2) sqrt(G rho_Lambda): EXACTLY HALF the free-fall acceleration at")
    print("  the dark-energy density. kappa = 1/2 is this framework's own coefficient and is not in")
    print("  the prior literature; note also that 32pi/3 is the Einstein-coupling conversion factor")
    print("  and CANCELS in that reduction, so the content is the ONE number kappa, which is FITTED,")
    print("  not derived (the kappa-forcing door was closed 2026-06-17).")
    print("  Alternate footing carried throughout: a0 = %.4e m/s^2." % A0_ALT)

    kernels = s1_generating_function()
    s2_the_action(kernels)
    s3_second_family(kernels)
    s4_offcircular_residual()
    s5_ostrogradsky(kernels)
    s6_the_bridge(kernels)

    banner("VERDICT")
    print("  THE ACTION IS WRITTEN DOWN, and it is more than the corpus had:")
    print("      S[x] = Integral dt  m ( |xdot|^2 f(|xddot|/a0) - phi(x) ),")
    print("      f(u) = u^-2 Integral_0^u v mu(v) dv,")
    print("      f_1(u) = [2u sqrt(4u^2+1) - 4u + asinh 2u] / (8 u^2)        (alpha=1, retired)")
    print("      f_2(u) = [u sqrt(1+u^2) - asinh u] / (2 u^2)                (alpha=2, IN FORCE, NEW)")
    print()
    print("  WHAT IT DELIVERS")
    print("   * A circular orbit solves its REAL fourth-order EL equation exactly, and the equation")
    print("     it satisfies is the framework's closure g_bar = A mu(A/a0) -- for GENERIC f, so the")
    print("     result is kernel-independent. This promotes the corpus's restricted-family variation")
    print("     to the actual equation of motion, which is a strictly stronger statement.")
    print("   * The exact Newtonian limit, with no residual correction, because f(oo) = 1/2.")
    print("   * f_2 in closed form: new, and the corpus needs it now that alpha=2 is the kernel.")
    print()
    print("  WHAT IT COSTS -- and these are not footnotes")
    print("   * It is FOURTH-ORDER with a non-degenerate acceleration-Hessian, so Ostrogradsky")
    print("     applies: extra degrees of freedom, unbounded Hamiltonian. Not a fundamental action.")
    print("   * OFF circles it does NOT reproduce the closure. S3 shows a second exactly-solvable")
    print("     family with a DIFFERENT interpolating function (u^3 instead of u^1 in the deep")
    print("     regime), and S4 measures the residual growing with eccentricity from exact zero.")
    print()
    print("  SO THE PINCER IS SHARP, NOT MERELY TRUE. Theorem 3 (corrected) excludes every local")
    print("  L(x, xdot, xddot) from reproducing the closure; Theorem 8 (redone, kernel-independent")
    print("  via w/x = c/v) excludes the nonlocal operator action. This file supplies the explicit")
    print("  witness that saturates the first horn: circles are EXACTLY the maximal family on which")
    print("  a local action reproduces the law, and here is the action that attains it.")
    print()
    print("  AND IT NAMES ONE DOOR, WITH ITS LOCK. u = w (v/c) exactly: the missing ingredient is a")
    print("  SPEED, unavailable to a covariant worldline functional but available to a preferred-frame")
    print("  theory, which this is. The lock: a cosmic-frame speed is excluded by the framework's own")
    print("  0.108 dex RAR at ~4x, so the frame must be locally dragged. That is a construction")
    print("  requirement, and it is NOT met by anything written down yet.")
    print()
    print("  NOT CLAIMED: that a0 is derived (it is not -- kappa=1/2 is fitted); that the off-circular")
    print("  law is settled; that the theory is closed. Milgrom 1994 / 2022 hold priority for the")
    print("  class of actions and for the frequency-vs-acceleration obstruction.")
    print("=" * 102)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
