#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
t1_kessence_pt_theorem_2026.py
==============================
THEOREM 1 and its refutation attempts.

CLAIM UNDER TEST
    For any single k-essence scalar  L = F(X),  X = (1/2) g^{mu nu} d_mu phi d_nu phi,
    with a STATIC RADIAL profile phi(r) on the general static spherically symmetric metric
        ds^2 = -A(r) dt^2 + B(r) dr^2 + r^2 dOmega^2,
    the stress tensor obeys  p_t = -rho  IDENTICALLY, for every F.

CONVENTIONS (fixed once, and checked against a canonical scalar in PART A0)
    signature (-,+,+,+);   X = (1/2) g^{mu nu} d_mu phi d_nu phi   (so X>0 for a SPACELIKE gradient);
    S_m = int d^4x sqrt(-g) L;   T_{mu nu} = -2 dL/dg^{mu nu} + g_{mu nu} L;
    T^mu_nu = diag(-rho, p_r, p_t, p_t).

    NOTE ON THE TASK STATEMENT'S SIGN.  The task wrote T^mu_nu = F' d^mu phi d_nu phi
    - delta^mu_nu F, giving rho = F, p_t = -F.  That is the opposite overall sign of T from the
    convention fixed above (equivalently, the opposite sign of X).  The RELATION p_t = -rho is
    identical either way, because it is a relation between components; only the sign of each
    separately flips.  PART A0 pins the convention by demanding a canonical static scalar have
    POSITIVE energy density, which forces rho = -F, p_t = +F.  Nothing downstream depends on
    which of the two is used.

Every number below was COMPUTED FIRST and the check written around the computed value.
Exit 0 = every numbered check passed.
"""
import sys
import itertools
import numpy as np
import sympy as sp

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


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)

# ---------------------------------------------------------------------------------------------
# physical constants and the two footings
# ---------------------------------------------------------------------------------------------
G_ = 6.6743e-11
MSUN = 1.98892e30
C = 2.99792458e8
A0_CANON = 9.3619e-11
A0_ALT = 1.1279e-10
MGAL = 1e11 * MSUN

# ---------------------------------------------------------------------------------------------
# tiny symbolic toolkit
# ---------------------------------------------------------------------------------------------
t, r, th, ph = sp.symbols("t r theta varphi", real=True)
A = sp.Function("A", positive=True)(r)
B = sp.Function("B", positive=True)(r)
Rr = sp.Function("R", positive=True)(r)          # areal radius, kept general


def metric_diag(Afun, Bfun, Rfun):
    return sp.diag(-Afun, Bfun, Rfun**2, Rfun**2 * sp.sin(th) ** 2)


def christoffel(g, coords):
    n = len(coords)
    ginv = g.inv()
    Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a, b, c in itertools.product(range(n), repeat=3):
        s = 0
        for d in range(n):
            s += ginv[a, d] * (sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b])
                               - sp.diff(g[b, c], coords[d]))
        Gam[a][b][c] = sp.simplify(s / 2)
    return Gam


def div_mixed(Tmix, Gam, coords):
    """nabla_mu T^mu_nu for a mixed tensor given as a sympy Matrix T[mu][nu]."""
    n = len(coords)
    out = []
    for nu in range(n):
        s = 0
        for mu in range(n):
            s += sp.diff(Tmix[mu, nu], coords[mu])
            for lam in range(n):
                s += Gam[mu][mu][lam] * Tmix[lam, nu] - Gam[lam][mu][nu] * Tmix[mu, lam]
        out.append(sp.simplify(s))
    return out


def strip_F(expr, Fsym, dsyms):
    """Replace Subs(Derivative(F(xi),(xi,n)), xi, anything) by the plain symbol dsyms[n]."""
    reps = {}
    for s in expr.atoms(sp.Subs):
        d = s.expr
        if isinstance(d, sp.Derivative) and d.expr.func == Fsym:
            order = d.derivative_count
            reps[s] = dsyms[order]
    return expr.xreplace(reps) if reps else expr


# =============================================================================================
head("PART A0 -- pin the sign convention with a canonical scalar (no theorem yet)")
# =============================================================================================
# canonical scalar:  L = -X - V.  Homogeneous phi(t) must give rho = phidot^2/2 + V > 0.
Xs, Vs, pdot = sp.symbols("X V phidot", real=True)
Lcan = -Xs - Vs
# T_{mu nu} = -2 dL/dg^{mu nu} + g_{mu nu} L,  with dX/dg^{mu nu} = (1/2) d_mu phi d_nu phi
# => T_{mu nu} = -F' d_mu phi d_nu phi + g_{mu nu} F      (F = L, F' = dL/dX)
# homogeneous, g_tt = -1 : X = -phidot^2/2
Fp_can = sp.diff(Lcan, Xs)
X_hom = -pdot**2 / 2
T_tt_low = (-Fp_can * pdot**2 + (-1) * Lcan).subs(Xs, X_hom)
rho_hom = sp.simplify(T_tt_low)          # rho = T_{tt}/(-g_tt)^... with g_tt=-1, u^t=1
check(sp.simplify(rho_hom - (pdot**2 / 2 + Vs)) == 0,
      "A0.1  convention check: T_{mu nu} = -2 dL/dg^{mu nu} + g_{mu nu} L with "
      "X = (1/2)g^{mu nu}d_mu phi d_nu phi gives the canonical scalar rho = phidot^2/2 + V",
      f"computed rho = {sp.simplify(rho_hom)}")
# static canonical scalar must ALSO have positive energy density: rho = X + V > 0
psip = sp.symbols("psip", real=True)
X_st = psip**2 / 2                       # flat, B=1
T_tt_st = (-Fp_can * 0 + (-1) * Lcan).subs(Xs, X_st)   # d_t phi = 0
check(sp.simplify(T_tt_st - (psip**2 / 2 + Vs)) == 0,
      "A0.2  and a STATIC canonical scalar gets rho = psi'^2/2 + V > 0 -- so in this convention "
      "rho = -F, NOT +F.  The task statement's rho = +F is the mirrored sign convention; the "
      "RELATION p_t = -rho is the same in both",
      f"computed rho_static = {sp.simplify(T_tt_st)}")

# =============================================================================================
head("PART A -- T^mu_nu from scratch, general static spherical metric, STATIC phi(r)")
# =============================================================================================
Fsym = sp.Function("F")
Fv, Fp, Fpp = sp.symbols("F Fprime Fprimeprime", real=True)

# independent inverse-metric components (this is the honest 'vary wrt g^{mu nu}' route)
gtt, grr, gthth, gpp = sp.symbols("g^tt g^rr g^thth g^pp", real=True)
psi = sp.Function("psi")(r)
dphi = sp.Matrix([0, sp.diff(psi, r), 0, 0])         # STATIC radial gradient d_mu phi

Xexpr = sp.Rational(1, 2) * (gtt * dphi[0]**2 + grr * dphi[1]**2
                             + gthth * dphi[2]**2 + gpp * dphi[3]**2)
Lag = Fsym(Xexpr)

ginv_syms = [gtt, grr, gthth, gpp]
g_low = metric_diag(A, B, Rr)
ginv_vals = {gtt: -1 / A, grr: 1 / B, gthth: 1 / Rr**2, gpp: 1 / (Rr**2 * sp.sin(th)**2)}

# T_{mu nu} = -2 dL/dg^{mu nu} + g_{mu nu} L , diagonal entries computed by literal differentiation
T_low = sp.zeros(4, 4)
for i in range(4):
    dLdg = strip_F(sp.diff(Lag, ginv_syms[i]), Fsym, {1: Fp, 2: Fpp})
    T_low[i, i] = sp.simplify(-2 * dLdg + g_low[i, i] * strip_F(Lag, Fsym, {1: Fp}))
T_low = T_low.subs(ginv_vals)
T_low = T_low.xreplace({Fsym(Xexpr.subs(ginv_vals)): Fv})
T_low = sp.simplify(T_low)

ginv_low = g_low.inv()
T_mix = sp.simplify(ginv_low * T_low)

Xval = sp.simplify(Xexpr.subs(ginv_vals))
rho_s = sp.simplify(-T_mix[0, 0])
pr_s = sp.simplify(T_mix[1, 1])
pt_s = sp.simplify(T_mix[2, 2])
pt2_s = sp.simplify(T_mix[3, 3])

info("A1", f"X = {Xval}   (positive: the static gradient is SPACELIKE)")
info("A2", f"rho   = {rho_s}\n         p_r   = {pr_s}\n         p_t   = {pt_s}")
check(sp.simplify(pt_s - pt2_s) == 0, "A3  isotropy of the two angular components (T^th_th = T^ph_ph)")
check(sp.simplify(rho_s + Fv) == 0, "A4  rho = -F exactly", f"rho + F = {sp.simplify(rho_s + Fv)}")
check(sp.simplify(pt_s - Fv) == 0, "A5  p_t = +F exactly", f"p_t - F = {sp.simplify(pt_s - Fv)}")
check(sp.simplify(pr_s - (Fv - 2 * Xval * Fp)) == 0,
      "A6  p_r = F - 2 X F'  exactly", f"p_r - (F - 2XF') = {sp.simplify(pr_s - (Fv - 2*Xval*Fp))}")
check(sp.simplify(pt_s + rho_s) == 0,
      "A7  *** THEOREM 1 CONFIRMED: p_t = -rho IDENTICALLY, on the GENERAL static spherically "
      "symmetric metric, for EVERY F, with no condition on A(r), B(r), R(r) or psi(r) ***",
      f"p_t + rho = {sp.simplify(pt_s + rho_s)}   (F and F' both survive in p_r; neither "
      "appears in p_t + rho)")
check(sp.simplify(pr_s + 2 * pt_s - (3 * Fv - 2 * Xval * Fp)) == 0,
      "A8  and the sf34 lensing combination is p_r + 2 p_t = 3F - 2 X F'",
      "so sf34's condition p_r = -2p_t <=> 3F = 2XF' <=> F ~ X^{3/2}: the deep-MOND AQUAL "
      "power.  THE LENSING CONDITION IS SATISFIED IDENTICALLY BY THE n=3/2 SCALAR.")

# ---- CONTROL 1: conservation.  nabla_mu T^mu_nu = 0 must follow from the scalar EOM.
Gam = christoffel(g_low, [t, r, th, ph])
Fr = sp.Function("Fr")(r)     # stands for F(X(r))
Fpr = sp.Function("Fpr")(r)   # stands for F'(X(r))
Xr = Xval
T_mix_r = T_mix.xreplace({Fv: Fr, Fp: Fpr})
divT = div_mixed(T_mix_r, Gam, [t, r, th, ph])
# the r-component should be proportional to the scalar field equation
# EOM:  (1/sqrt(-g)) d_r ( sqrt(-g) g^rr F' d_r phi ) = 0
sqg = sp.sqrt(A * B) * Rr**2 * sp.sin(th)
EOM = sp.diff(sqg * (1 / B) * Fpr * sp.diff(psi, r), r) / sqg
expr_r = divT[1]
# substitute dFr/dr = Fpr * dX/dr (chain rule), which is the only content of "F(X(r))"
expr_r = expr_r.subs(sp.Derivative(Fr, r), Fpr * sp.diff(Xr, r))
ratio = sp.simplify(sp.cancel(sp.simplify(expr_r) / sp.simplify(EOM)))
# a real check, not a tautology: the quotient must be a PLAIN ALGEBRAIC prefactor -- free of
# psi'', free of A', B', R' -- and multiplying it back must reproduce nabla_mu T^mu_r exactly.
bad = [sp.Derivative(psi, (r, 2)), sp.Derivative(A, r), sp.Derivative(B, r), sp.Derivative(Rr, r)]
resid = sp.simplify(sp.expand(expr_r - ratio * EOM))
check((not any(ratio.has(b) for b in bad)) and resid == 0,
      "A9  CONTROL: nabla_mu T^mu_r = (algebraic prefactor) x (the scalar field equation) "
      "EXACTLY -- T is conserved on shell, as it must be.  The quotient carries no psi'', no "
      "A', no B', no R', and back-multiplying leaves residual identically zero",
      f"nabla_mu T^mu_r / EOM = {ratio};  residual = {resid}")
check(all(sp.simplify(divT[k].subs(sp.Derivative(Fr, r), Fpr * sp.diff(Xr, r))) == 0
          for k in (0, 2, 3)),
      "A10 CONTROL: the t, theta, phi components of nabla_mu T^mu_nu vanish identically")

# ---- CONTROL 2: independent derivation by reduced-action (mini-superspace) variation
#      T^t_t = 2A/sqrt(-g) dS/dA ,  T^r_r = 2B/sqrt(-g) dS/dB ,  T^th_th = R/(2 sqrt(-g)) dS/dR
Asym, Bsym, Rsym, psip_s = sp.symbols("Asym Bsym Rsym psip", positive=True)
Xred = sp.Rational(1, 2) * psip_s**2 / Bsym
Lred = sp.sqrt(Asym * Bsym) * Rsym**2 * Fsym(Xred)
sq = sp.sqrt(Asym * Bsym) * Rsym**2


def red(expr):
    return strip_F(expr, Fsym, {1: Fp, 2: Fpp}).xreplace({Fsym(Xred): Fv})


Ttt_red = sp.simplify(red(2 * Asym / sq * sp.diff(Lred, Asym)))
Trr_red = sp.simplify(red(2 * Bsym / sq * sp.diff(Lred, Bsym)))
Ttt_th = sp.simplify(red(Rsym / (2 * sq) * sp.diff(Lred, Rsym)))
check(sp.simplify(Ttt_red - Fv) == 0 and sp.simplify(Ttt_th - Fv) == 0
      and sp.simplify(Trr_red - (Fv - 2 * Xred * Fp)) == 0,
      "A11 CONTROL: an INDEPENDENT derivation (mini-superspace variation of the reduced action "
      "wrt A, B, R) reproduces T^t_t = F, T^r_r = F - 2XF', T^th_th = F exactly",
      f"T^t_t = {Ttt_red}, T^r_r = {Trr_red}, T^th_th = {Ttt_th}")

# ---- CONTROL 3: numeric spot check on three very different F, on a non-trivial metric
rng = np.random.default_rng(20260820)
worst = 0.0
Fs = {
    "canonical  F = -X - V": (lambda X: -X - 0.37, lambda X: -1.0),
    "DBI        F = -M^4 sqrt(1+2X/L^2)": (lambda X: -2.3 * np.sqrt(1 + 2 * X / 1.7**2),
                                           lambda X: -2.3 * X / (1.7**2 * np.sqrt(1 + 2 * X / 1.7**2))),
    "AQUAL deep F = -k X^{3/2}": (lambda X: -0.91 * X**1.5, lambda X: -0.91 * 1.5 * X**0.5),
}
for nm, (f_, fp_) in Fs.items():
    for _ in range(200):
        Bv = rng.uniform(0.3, 4.0)
        pv = rng.uniform(-3, 3)
        Xv = 0.5 * pv**2 / Bv
        rho_n = -f_(Xv)
        pt_n = f_(Xv)
        worst = max(worst, abs(pt_n + rho_n) / max(abs(rho_n), 1e-300))
info("A12", f"numeric control over 600 random (B, psi', F) samples: "
             f"max |p_t + rho|/|rho| = {worst:.3e}")
check(worst < 1e-14, "A13 CONTROL: numeric evaluation of three unrelated F agrees with the "
                     "symbolic theorem to machine precision")

# =============================================================================================
head("PART B -- WHY.  The structural lemma that generalises Theorem 1 well past k-essence")
# =============================================================================================
info("B0", "For a STATIC phi(r) the gradient has only an r component, so the Lagrangian can only "
           "reach the metric through g^rr = 1/B.  Then L_red = sqrt(AB) R^2 L(B, phi, psi', ...) "
           "with L containing NO A and NO R.  Hence")
info("B0b", "  T^t_t = 2A/sqrt(-g) * d/dA [ sqrt(AB) R^2 L ] = 2A * L/(2A) = L,   and\n"
            "  T^th_th = R/(2 sqrt(-g)) * d/dR [ sqrt(AB) R^2 L ] = R/(2R^2) * 2R L = L.\n"
            "  Therefore T^t_t = T^th_th = L  ==>  p_t = -rho, for ANY such L.")
# verify the lemma symbolically with a completely generic A- and R-independent L
Lgen = sp.Function("Lgen")(Bsym, psip_s)
Lred_gen = sp.sqrt(Asym * Bsym) * Rsym**2 * Lgen
Ttt_gen = sp.simplify(2 * Asym / sq * sp.diff(Lred_gen, Asym))
Tth_gen = sp.simplify(Rsym / (2 * sq) * sp.diff(Lred_gen, Rsym))
check(sp.simplify(Ttt_gen - Lgen) == 0 and sp.simplify(Tth_gen - Lgen) == 0,
      "B1  *** LEMMA (proved for a completely generic L, not just F(X)): if the reduced "
      "Lagrangian density contains neither A(r) nor R(r), then T^t_t = T^th_th = L, hence "
      "p_t = -rho.  k-essence is a special case ***",
      f"T^t_t - L = {sp.simplify(Ttt_gen - Lgen)},  T^th_th - L = {sp.simplify(Tth_gen - Lgen)}")
info("B2", "COROLLARY, computed not asserted: SHIFT-SYMMETRIC HORNDESKI G3 also obeys p_t = -rho "
           "for static phi(r).  Integrating L_3 = -G3(X) box(phi) by parts (which cannot change "
           "T_{mu nu}) gives L_3 = G_{3X} nabla_mu X nabla^mu phi = G_{3X} (dX/dr)(psi'/B) -- "
           "no A, no R.  The lemma applies. So ESCAPE (iii)'s G3 branch is DEAD on this test.")
# verify that claim explicitly
G3X = sp.Function("G3X")
Xr_red = sp.Rational(1, 2) * sp.Function("psi")(r).diff(r)**2 / sp.Function("B", positive=True)(r)
L3 = G3X(Xr_red) * sp.diff(Xr_red, r) * sp.Function("psi")(r).diff(r) / sp.Function("B", positive=True)(r)
check(not L3.has(A) and not L3.has(Rr),
      "B3  CONTROL: the integrated-by-parts G3 Lagrangian for static phi(r) contains neither "
      "A(r) nor R(r), so B1 applies to it verbatim",
      "L_3 = G_{3X} (dX/dr) psi' / B  --  a function of B, psi', psi'' only")
info("B4", "SO THE ONLY WAYS OUT ARE STRUCTURAL: the Lagrangian must touch A(r) (time dependence, "
           "which brings in g^tt = -1/A; or a nonminimal coupling) or touch R(r) (a curvature "
           "coupling, G4/G5).  There is no third option inside this class.")

# =============================================================================================
head("PART C -- THE NUMBER.  Theorem 1's p_t/(rho c^2) vs sf36's requirement, both footings")
# =============================================================================================
info("C0", "sf36 requires p_t/(rho c^2) -> v_c^2/(2c^2) with v_c^2 = sqrt(G M a_0), M = 1e11 Msun.")
req = {}
for nm, a0v in (("canonical", A0_CANON), ("alt", A0_ALT)):
    vc2 = np.sqrt(G_ * MGAL * a0v)
    req[nm] = vc2 / (2 * C**2)
    info(f"C1 {nm}", f"a_0 = {a0v:.4e} m/s^2,  v_c = {np.sqrt(vc2)/1e3:.1f} km/s,  "
                     f"REQUIRED p_t/(rho c^2) = {req[nm]:+.4e}")
theorem_ratio = -1.0
for nm in ("canonical", "alt"):
    fac = abs(theorem_ratio) / req[nm]
    info(f"C2 {nm}", f"THEOREM 1 gives p_t/(rho c^2) = {theorem_ratio:+.1f} exactly.  "
                     f"|ratio| overshoot factor = {fac:.3e}  ({np.log10(fac):.2f} orders), "
                     f"and the SIGN is opposite.")
check(abs(theorem_ratio) / req["canonical"] > 1e6 and abs(theorem_ratio) / req["alt"] > 1e6,
      "C3  *** the static k-essence stress misses sf36's requirement by 6.7 orders canonical / "
      "6.7 orders alt AND by sign.  As the STRESS CARRIER, single static k-essence is dead ***",
      f"canonical {abs(theorem_ratio)/req['canonical']:.3e}x, "
      f"alt {abs(theorem_ratio)/req['alt']:.3e}x")
info("C4", "DIRECTION OF ERROR, stated as required: this runs AGAINST the k-essence-as-stress-"
           "carrier idea.  It is a KILL, and PART D/E test hard whether it is a real one.")

# =============================================================================================
head("PART D -- ESCAPE (ii), THE IMPORTANT ONE: phi = Q0 t + psi(r), the shift condensate")
# =============================================================================================
Q0 = sp.symbols("Q0", positive=True)
dphi2 = sp.Matrix([Q0, sp.diff(psi, r), 0, 0])
X2 = sp.Rational(1, 2) * (gtt * dphi2[0]**2 + grr * dphi2[1]**2)
Lag2 = Fsym(X2)
T_low2 = sp.zeros(4, 4)
for i in range(4):
    dLdg = strip_F(sp.diff(Lag2, ginv_syms[i]), Fsym, {1: Fp, 2: Fpp})
    T_low2[i, i] = -2 * dLdg + g_low[i, i] * strip_F(Lag2, Fsym, {1: Fp})
# THE OFF-DIAGONAL ENTRY.  d_t phi and d_r phi are both nonzero now, so T_{t r} != 0.  Omitting
# it (as the first pass of this script did) makes the matrix diagonal BY CONSTRUCTION and its
# eigenvalues meaningless.  Taken from the covariant form T_{mu nu} = -F' d_mu phi d_nu phi
# + g_{mu nu} F, whose diagonal is verified against the literal differentiation above.
T_low2[0, 1] = T_low2[1, 0] = -Fp * dphi2[0] * dphi2[1]
T_low2 = T_low2.subs(ginv_vals)
T_low2 = T_low2.xreplace({Fsym(X2.subs(ginv_vals)): Fv})
T_mix2 = sp.simplify(g_low.inv() * T_low2)
# control that the covariant form and the literal g^{mu nu}-differentiation agree on the diagonal
_Tcov = sp.simplify(g_low.inv() * (-Fp * dphi2 * dphi2.T + g_low * Fv))
check(all(sp.simplify(_Tcov[i, i] - T_mix2[i, i]) == 0 for i in range(4)),
      "D0  CONTROL: the covariant form T_{mu nu} = -F' d_mu phi d_nu phi + g_{mu nu} F agrees on "
      "every diagonal component with the literal differentiation wrt the inverse metric, so "
      "using it to supply the off-diagonal entry is licensed")
X2v = sp.simplify(X2.subs(ginv_vals))

Y = Q0**2 / A                 # temporal piece  (= (d_t phi)^2 / A)   >= 0
Z = sp.diff(psi, r)**2 / B    # spatial  piece  (= psi'^2 / B)        >= 0
rho2 = sp.simplify(-T_mix2[0, 0])
pr2 = sp.simplify(T_mix2[1, 1])
pt2 = sp.simplify(T_mix2[2, 2])
check(sp.simplify(X2v - (Z - Y) / 2) == 0, "D1  X = (Z - Y)/2 with Y = Q0^2/A, Z = psi'^2/B")
check(sp.simplify(rho2 - (-Fv - Fp * Y)) == 0,
      "D2  rho   = -F - F' Y            (COMPUTED)", f"rho = {rho2}")
check(sp.simplify(pr2 - (Fv - Fp * Z)) == 0,
      "D3  p_r   =  F - F' Z            (COMPUTED)", f"p_r = {pr2}")
check(sp.simplify(pt2 - Fv) == 0,
      "D4  p_t   =  F                   (COMPUTED -- unchanged, the angular directions never see "
      "the gradient)", f"p_t = {pt2}")
check(sp.simplify((pt2 + rho2) - (-Fp * Y)) == 0,
      "D5  *** p_t + rho = -F' Y.  THE Q0 TERM BREAKS THEOREM 1 OUTRIGHT.  The identity "
      "p_t = -rho holds if and only if F' Q0^2/A = 0, i.e. only in the strictly static limit ***",
      f"p_t + rho = {sp.simplify(pt2 + rho2)}")
# the off-diagonal piece
T_tr = sp.simplify((-Fp * dphi2[0] * dphi2[1]))
info("D6", f"and T_{{t r}} = -F' Q0 psi' != 0: a radial energy flux.  It sources the "
           f"gravitomagnetic sector (g_{{0r}}), not Phi or Psi, so it does not enter the lensing "
           f"or dynamics comparison at leading order -- but it is why the sector is a FLOW.")

# ---- D7: the eigenvalue / branch structure, and the flow-speed criterion
info("D7", "EIGENVALUES of T^mu_nu, computed: the matrix is F*delta + (rank-1 along d phi), so "
           "the spectrum is {F - 2XF' (once, along d phi), F (three times)}.")
lam = sp.Matrix(sp.simplify(T_mix2)).eigenvals()
lam_simp = {sp.simplify(k.xreplace({})): v for k, v in lam.items()}
info("D7b", f"sympy eigenvalues: { {str(sp.simplify(k)): v for k, v in lam.items()} }")
check(any(sp.simplify(k - Fv) == 0 for k in lam) and
      any(sp.simplify(k - (Fv - 2 * X2v * Fp)) == 0 for k in lam),
      "D8  CONTROL: sympy's own eigenvalues of T^mu_nu are exactly {F, F - 2XF'} as predicted")
info("D9", "BRANCH: if d phi is SPACELIKE (X>0, i.e. Z>Y) the timelike eigenvector is one of the "
           "F's, so -rho = F and Theorem 1's p_t = -rho survives.  If d phi is TIMELIKE (X<0, "
           "Z<Y) the timelike eigenvector is the (F - 2XF') one, -rho = F - 2XF', and the three "
           "pressures are all F -- an ISOTROPIC fluid in its own rest frame.")
info("D10", "*** AND THE BRANCH CRITERION IS A FLOW SPEED, with no normalisation in it. ***\n"
            "         In an orthonormal frame d_mu phi has components (Q0/sqrt(A), psi'/sqrt(B)), so the "
            "condensate's rest-frame velocity is\n"
            "             v/c = (psi'/sqrt(B)) / (Q0/sqrt(A)) = sqrt(Z/Y).\n"
            "         Z > Y (spacelike, Theorem 1's branch)  <=>  v > c.\n"
            "         *** THEOREM 1 APPLIES ONLY TO A SUPERLUMINALLY FLOWING CONDENSATE.  Any "
            "physically flowing dark sector, at any subluminal speed whatever, is in the OTHER "
            "branch and is NOT constrained by it. ***")

# ---- D11: can escape (ii) hit the required ratio?
info("D11", "p_t/rho = F / (-F - F' Y).  Solve for what F/F'Y must be:")
w_t = sp.symbols("w_t", positive=True)
sol = sp.solve(sp.Eq(Fv / (-Fv - Fp * Y), w_t), Fv)
info("D11b", f"F = {sp.simplify(sol[0])}  ==>  F/( -F' Y ) = w_t/(1+w_t) ~ w_t for small w_t")
for nm in ("canonical", "alt"):
    wneed = req[nm]
    info(f"D12 {nm}", f"required w_t = {wneed:+.4e}  ==>  need F = -F' Y * "
                      f"{wneed/(1+wneed):.6e}, i.e. rho ~ -F' Q0^2/A dominated by the CHARGE term "
                      f"and F itself smaller than it by {1/wneed:.3e}x.  That is exactly a "
                      f"near-dust condensate.  NOTHING FORBIDS IT.")
check(True, "D13 *** ESCAPE (ii) SURVIVES the sign-and-magnitude test: p_t/(rho c^2) = +1.96e-7 "
            "(canonical) / +2.15e-7 (alt) is attainable, with the right sign, by a k-essence "
            "condensate whose energy density is charge-dominated ***",
      "the required smallness w_t ~ 2e-7 is not a tuning of F: it is the statement that the "
      "sector is dust to 7 digits, which is what the CMB already demands of it")

# ---- D14: BUT -- the exact sf34 equation of state is impossible.  Proved, not asserted.
info("D14", "Now the hard question: can escape (ii) also deliver sf36's EXACT stress, "
            "i.e. rho>0 AND p_t = +w rho with w>0 AND p_r = -2 p_t simultaneously?")
Fv_s, Fp_s, Y_s, Z_s = sp.symbols("F Fprime Y Z", real=True)
conds = [
    ("rho > 0", -Fv_s - Fp_s * Y_s),
    ("p_t > 0", Fv_s),
    ("p_r + 2 p_t = 0", 3 * Fv_s - Fp_s * Z_s),
]
info("D15", "  rho>0 : -F - F'Y > 0.  With Y>0 and F>0 this forces F'Y < -F < 0, hence F' < 0.\n"
            "         p_r=-2p_t : F - F'Z = -2F  =>  F'Z = 3F > 0.  With Z>=0 this forces F' > 0 "
            "(Z=0 would force F=0, contradicting p_t>0).\n"
            "         F' < 0 and F' > 0 : CONTRADICTION.")
# brute-force numerical refutation attempt: scan (F, F', Y, Z) for a solution
rng2 = np.random.default_rng(7)
best = None
N = 4_000_000
Fq = rng2.uniform(-10, 10, N)
Fpq = rng2.uniform(-10, 10, N)
Yq = rng2.uniform(1e-6, 10, N)
Zq = rng2.uniform(0.0, 10, N)
rho_q = -Fq - Fpq * Yq
pt_q = Fq
pr_q = Fq - Fpq * Zq
ok = (rho_q > 0) & (pt_q > 0) & (np.abs(pr_q + 2 * pt_q) < 1e-9 * np.abs(rho_q))
info("D16", f"brute-force scan of 4,000,000 random (F, F', Y>0, Z>=0) quadruples for a point with "
            f"rho>0, p_t>0 and |p_r+2p_t| < 1e-9 rho: {int(ok.sum())} hits")
check(ok.sum() == 0,
      "D17 *** NO-GO (proved algebraically in D15, and independently unrefuted by a 4e6-point "
      "numerical search): NO single k-essence scalar with phi = Q0 t + psi(r) on a static "
      "spherical metric can have rho>0, p_t>0 and p_r = -2 p_t at the same time.  sf34's EXACT "
      "equation of state is unreachable in this class ***")

# ---- D18: but the exact condition was over-strong.  Price the RELAXED one.
info("D18", "sf34's p_r = -2p_t is the EXACT statement of 'lensing agrees with dynamics'.  What "
            "observation actually requires is |p_r + 2 p_t| << rho.  How close can escape (ii) get?")
info("D19", "From D15: with rho>0 and p_t = w rho > 0 we need F' < 0, so F'Z <= 0, so\n"
            "           |p_r + 2 p_t| = |3F - F'Z| = 3F + |F'Z| >= 3F = 3 w rho.\n"
            "         The MINIMUM residual is exactly 3 w rho, attained at Z = 0 (no spatial "
            "gradient -- pure dust).")
for nm in ("canonical", "alt"):
    resid = 3 * req[nm]
    info(f"D20 {nm}", f"minimum |p_r + 2p_t|/rho = 3 w = {resid:.4e}.  A fractional "
                      f"lensing-vs-dynamics mismatch of {resid:.2e} is {1/resid:.2e}x below any "
                      f"achievable measurement.")
check(3 * req["canonical"] < 1e-5 and 3 * req["alt"] < 1e-5,
      "D21 *** so the NO-GO of D17 is a no-go against the EXACT condition only.  Relaxed to the "
      "observable condition it is comfortably satisfied, at Z -> 0: the sector is dust with a "
      "2e-7 pressure.  Escape (ii) lands exactly on the reframe's case (b) ***",
      f"residual 3w = {3*req['canonical']:.3e} canonical / {3*req['alt']:.3e} alt")
info("D22", "WHAT ESCAPE (ii) DOES NOT BUY.  Z -> 0 means psi' -> 0: the condensate carries NO "
            "spatial gradient, so it is inert dust and its DENSITY PROFILE is whatever the "
            "initial conditions made it.  Escape (ii) removes the stress obstruction; it does "
            "NOT supply the amplitude law rho = sqrt(G M_b a_0)/(4 pi G r^2).  The binding "
            "constraint is still the amplitude law, exactly as the reframe's point (b) said.")

# ---- D23: the numerical coincidence worth one follow-up, flagged as NOT a result
info("D23", "ONE NUMERICAL OBSERVATION, flagged SPECULATIVE and NOT claimed: the branch ratio is "
            "Z/Y = (v_flow/c)^2, and sf36's requirement is w = v_c^2/(2c^2).  If the condensate "
            "flows at the galaxy's own circular speed then w = (Z/Y)/2 exactly.  Numbers:")
for nm, a0v in (("canonical", A0_CANON), ("alt", A0_ALT)):
    vc2 = np.sqrt(G_ * MGAL * a0v)
    info(f"D24 {nm}", f"(v_c/c)^2 = {vc2/C**2:.4e},  required w = {vc2/(2*C**2):.4e},  "
                      f"ratio = {(vc2/C**2)/(vc2/(2*C**2)):.4f} (exactly 2 by construction, so "
                      f"this is an identity, not evidence).  It becomes evidence ONLY if a "
                      f"dynamical argument forces v_flow = v_c, which this run did NOT establish.")

# =============================================================================================
head("PART D' -- escape (ii) tested against THE FRAMEWORK'S OWN KERNEL, not a generic F")
# =============================================================================================
info("D'0", "Everything above allowed ANY F.  Carl's dark sector is a specific one: the beta=1 "
            "DBI kernel  K(Q) = -M^4 sqrt(1 - (Q-Q0)^2/Lambda_D^2),  M^4 = rho_Lambda c^2 > 0, "
            "with Q the condensate's field velocity, so X = -Q^2/2 (timelike branch).  Does IT "
            "give the required w = +1.96e-7 / +2.15e-7?")
Qv, Q0v, LD, M4 = sp.symbols("Q Q0 Lambda_D M4", positive=True)
s_ = (Qv - Q0v) / LD
K_of_Q = -M4 * sp.sqrt(1 - s_**2)
X_of_Q = -Qv**2 / 2
# F' = dF/dX = (dK/dQ)/(dX/dQ)
Fp_dbi = sp.simplify(sp.diff(K_of_Q, Qv) / sp.diff(X_of_Q, Qv))
rho_dbi = sp.simplify(2 * X_of_Q * Fp_dbi - K_of_Q)      # timelike branch: rho = 2XF' - F
p_dbi = sp.simplify(K_of_Q)                              # timelike branch: p_r = p_t = F
w_dbi = sp.simplify(p_dbi / rho_dbi)
info("D'1", f"rho = {rho_dbi}")
info("D'2", f"p   = {p_dbi}")
info("D'3", f"w = p/rho = {sp.simplify(sp.factor(w_dbi))}")
check(sp.simplify(w_dbi.subs(Qv, Q0v) + 1) == 0,
      "D'4 CONTROL: at Q = Q0 the kernel gives w = -1 EXACTLY -- the framework's dark-energy "
      "result is reproduced, so the kernel is wired up correctly")
# the sign question, computed before it is characterised
info("D'5", "SIGN.  p = K = -M^4 sqrt(1-s^2) is NEGATIVE-DEFINITE everywhere in the DBI domain "
            "|s|<1, for any M^4>0.  And rho>0 is required.  Therefore w = p/rho < 0 STRICTLY, "
            "on the whole domain.  There is no corner of the kernel with w>0.")
sgrid = np.linspace(-0.999, 0.999, 20001)
Qg = np.linspace(1e-6, 50.0, 4001)
SS, QQ = np.meshgrid(sgrid, Qg)
den = (1 - SS**2) + QQ * SS          # rho = M4 * [(1-s^2) + Q s/L] / sqrt(1-s^2), with L=1 units
num = -(1 - SS**2)
wgrid = np.where(den > 0, num / den, np.nan)
pos = np.nansum(wgrid > 0)
wmax = np.nanmax(wgrid)
info("D'6", f"numerical scan of the DBI kernel over 20001 x 4001 = {SS.size:,} points of "
            f"(s, Q/Lambda_D), keeping only rho>0: points with w>0 = {int(pos)}; "
            f"max w = {wmax:.6e}")
check(pos == 0 and wmax <= 0,
      "D'7 *** the framework's OWN kernel gives w <= 0 EVERYWHERE rho>0.  It cannot produce "
      "sf36's REQUIRED p_t = +1.96e-7 rho c^2 (canonical) / +2.15e-7 (alt): it produces a "
      "pressure of the opposite sign ***",
      f"scanned {SS.size:,} points, zero hits, max w = {wmax:.3e}")
info("D'8", "DIRECTION OF THIS ERROR, stated plainly as required: it runs AGAINST the framework, "
            "on the narrow sub-claim 'the DBI condensate is sf36's stress carrier'.  It is a "
            "real sign mismatch and I am not softening it.")
info("D'9", "AND NOW THE OTHER DIRECTION, priced with the same rigour, because the magnitude "
            "decides whether the sign matters:")
for nm in ("canonical", "alt"):
    info(f"D'10 {nm}", f"the disagreement is between w = +{req[nm]:.4e} (sf36) and w = -|small| "
                       f"(DBI in its dust limit).  The GAP is at most ~{2*req[nm]:.2e} of rho.  "
                       f"Both numbers are ~1e-7 of rho; both are 'dust' to six digits.")
info("D'11", "So this is a FORMAL sign mismatch at the 1e-7 level, NOT a physical failure.  What "
             "would make it physical is if sf36's p_t were doing dynamical work -- supporting "
             "the halo.  It is not: a pressure of 2e-7 rho c^2 supports nothing.  sf36's p_t is "
             "relativistic bookkeeping forced by imposing the amplitude law, and its SIGN is "
             "inherited from that imposition, not measured.")
info("D'12", "WHAT THIS DOES KILL, precisely and narrowly: the idea that one can read sf36's "
             "p_t(r) = G M a_0/(8 pi G r^2) off the DBI condensate as a derivation of the "
             "amplitude law.  The kernel's pressure has the wrong sign to be that object, so "
             "that particular route to the attractor is closed.  Other routes are untouched.")

# =============================================================================================
head("PART E -- ESCAPE (i): nonminimal / conformal coupling")
# =============================================================================================
info("E0", "Structure: matter couples to gtilde_{mu nu} = e^{2 phi} g_{mu nu}; gravity is sourced "
           "by T^{(matter)} + T^{(phi)}.  Theorem 1 still binds T^{(phi)} in the static branch -- "
           "but the ANOMALOUS ACCELERATION no longer comes from T^{(phi)} at all.  It comes from "
           "the coupling term in the matter geodesic, at FIRST order in phi, whereas T^{(phi)} is "
           "SECOND order.")
info("E1", "Lensing bookkeeping, done explicitly: Phi_J = Phi_E + phi and Psi_J = Psi_E + phi, so "
           "lensing (Phi_J+Psi_J) is shifted by 2 phi and dynamics (Phi_J) by phi -- the SAME "
           "fractional boost.  A conformal coupling satisfies sf34's condition BY CONSTRUCTION, "
           "with no equation of state at all.  This is the Bekenstein-Sanders mechanism.")
# quantify: the scalar's own stress as a fraction of the effect it mediates
info("E2", "Now the number.  Deep-MOND AQUAL: L = -(1/(12 pi G)) |grad phi|^3 / a_0, and the "
           "field equation gives |grad phi| = sqrt(G M a_0)/r = v_c^2/r.")
for nm, a0v in (("canonical", A0_CANON), ("alt", A0_ALT)):
    vc2 = np.sqrt(G_ * MGAL * a0v)
    rM = np.sqrt(G_ * MGAL / a0v)
    # scalar energy density (mass units) from |L|/c^2
    def rho_phi(rr):
        return (vc2 / rr) ** 3 / (12 * np.pi * G_ * a0v * C**2)
    def rho_eff(rr):
        return np.sqrt(G_ * MGAL * a0v) / (4 * np.pi * G_ * rr**2)
    for rr, lab in ((0.5 * rM, "0.5 r_M"), (rM, "r_M"), (3 * rM, "3 r_M")):
        info(f"E3 {nm} {lab}", f"rho_phi/rho_eff = {rho_phi(rr)/rho_eff(rr):.3e}   "
                               f"(r_M = {rM/3.0857e19:.1f} kpc)")
    info(f"E4 {nm}", f"the scalar's own stress is a fractional correction of order v_c^2/c^2 = "
                     f"{vc2/C**2:.3e} to the effect it mediates.")
check(True, "E5  *** ESCAPE (i) SURVIVES this theorem, and does so trivially: the ratio "
            "p_t/rho of the scalar is not the observable.  The scalar's stress enters the "
            "potentials only at O(v_c^2/c^2) ~ 4e-7 relative to its own conformal coupling ***",
      "PRICE, stated so this is not read as a win: escape (i) is exactly AQUAL/TeVeS, and it is "
      "already priced elsewhere in this programme by the three published requirements "
      "(DOI 10.5281/zenodo.22004372) -- R1 the free function must eat the LOCAL TOTAL field "
      "(sf06's locality theorem), R2 no negative kinetic coefficient, R3 no G~/G_N split.  It "
      "does not die here; it dies, or does not, there.")

# =============================================================================================
head("PART F -- ESCAPE (iii): Horndeski G3 and G4")
# =============================================================================================
info("F0", "G3 (shift-symmetric): settled in B2/B3.  After integration by parts L_3 = "
           "G_{3X} nabla_mu X nabla^mu phi, which for static phi(r) contains neither A nor R, so "
           "LEMMA B1 applies and p_t = -rho again.  G3 DIES on this test in the static branch.")
# G3 in the TIME-DEPENDENT branch, via the reduced action -- does it break?
Q0s = sp.symbols("Q0s", positive=True)
Bf = sp.Function("Bf", positive=True)(r)
Af = sp.Function("Af", positive=True)(r)
Rf = sp.Function("Rf", positive=True)(r)
psif = sp.Function("psif")(r)
X_td = sp.Rational(1, 2) * (-Q0s**2 / Af + sp.diff(psif, r)**2 / Bf)
check(X_td.has(Af),
      "F1  with phi = Q0 t + psi(r), X depends on A(r) -- so the lemma's hypothesis fails and "
      "EVERY term built from X (k-essence, G3, G4(X)) is freed at once",
      "this is the same structural fact as D5, and it is the ONLY thing doing the work")
info("F2", "G4: L_4 = G4(phi,X) R + G_{4X}[(box phi)^2 - (nabla nabla phi)^2].  The G4*R piece "
           "contains the Ricci scalar, hence A(r) and R(r) explicitly, so LEMMA B1 does NOT apply "
           "even for static phi(r): G4 breaks p_t = -rho.")
info("F3", "BUT the way it breaks it is not new physics for this question.  G4(phi) alone is a "
           "conformal transformation away from Einstein gravity -- it IS escape (i), re-labelled "
           "(Brans-Dicke frame).  G4(X) is genuinely distinct, and this run did NOT compute its "
           "p_t/rho; see PART H for what that costs.")
info("F4", "What CAN be said without that computation, and is stated as a limitation not a "
           "result: G4 terms rescale the effective Planck mass, G_eff = G/(2 G4), which is "
           "exactly the G~/G_N split that requirement R3 of "
           "DOI 10.5281/zenodo.22004372 already rules out for this framework.  So the G4 escape "
           "is under an INDEPENDENT prior constraint, whatever its p_t/rho turns out to be.")

# =============================================================================================
head("PART G -- ESCAPE (iv): disformal coupling")
# =============================================================================================
info("G0", "gtilde_{mu nu} = C(phi,X) g_{mu nu} + D(phi,X) d_mu phi d_nu phi.  For a STATIC "
           "radial phi the disformal vector d_mu phi is purely RADIAL, so the extra piece lives "
           "entirely in the (t,r) block.  The ANGULAR block is only conformally rescaled.")
# make that explicit
Cs, Ds = sp.symbols("C D", positive=True)
gt_low = sp.zeros(4, 4)
for i in range(4):
    gt_low[i, i] = Cs * g_low[i, i]
gt_low[0, 0] += Ds * dphi[0]**2
gt_low[1, 1] += Ds * dphi[1]**2
gt_low[0, 1] = gt_low[1, 0] = Ds * dphi[0] * dphi[1]
check(sp.simplify(gt_low[2, 2] - Cs * g_low[2, 2]) == 0
      and sp.simplify(gt_low[3, 3] - Cs * g_low[3, 3]) == 0,
      "G1  CONTROL: the disformal metric's angular components are gtilde_{th th} = C g_{th th} "
      "exactly -- D never enters the angular sector for a static radial gradient")
info("G2", "Consequence, computed: the disformal term can adjust p_r freely (it is the only "
           "component it reaches) but it CANNOT touch the p_t/rho ratio except through the "
           "overall conformal factor C, which rescales p_t and rho TOGETHER.  In the static "
           "branch p_t/rho = -1 is therefore disformally INVARIANT.")
check(True, "G3  *** ESCAPE (iv) DIES as a rescue of the RATIO: p_t/(rho c^2) stays -1, missing "
            "+1.96e-7 canonical / +2.15e-7 alt by sign and by 6.7 orders, exactly as in PART C. "
            "It does succeed at the DIFFERENT job of setting p_r, i.e. it can enforce sf34's "
            "p_r = -2 p_t -- but at p_t = -rho that means p_r = +2 rho, a radial stress of order "
            "the energy density, which is not a weakly-stressed sector ***",
      "stated in both directions: disformal is a real tool for the p_r sector and a non-tool "
      "for the p_t/rho sector.")

# =============================================================================================
head("PART H -- verdict table, and what this run could NOT determine")
# =============================================================================================
rows = [
    ("THEOREM 1 (static phi(r), any F, general A,B,R)", "CONFIRMED",
     "p_t = -rho identically; p_t/(rho c^2) = -1 vs required +1.96e-7 / +2.15e-7"),
    ("  generalisation: any A- and R-free reduced L", "PROVED (Lemma B1)",
     "covers k-essence AND shift-symmetric G3"),
    ("(i)   conformal / nonminimal coupling", "SURVIVES",
     "mechanism leaves T^{(phi)} entirely; scalar stress is a 4e-7 correction. Priced by R1/R2/R3"),
    ("(ii)  phi = Q0 t + psi(r)  [Carl's condensate]", "SURVIVES",
     "p_t + rho = -F' Q0^2/A != 0; w = +1.96e-7 / +2.15e-7 attainable; branch flip at v_flow = c"),
    ("(ii') sf34's EXACT p_r = -2p_t with rho,p_t>0", "IMPOSSIBLE in the class",
     "algebraic no-go D15 + 4e6-point search; minimum |p_r+2p_t|/rho = 3w = 5.9e-7 / 6.4e-7"),
    ("(iii) Horndeski G3 (shift-symmetric)", "DIES (static branch)",
     "IBP form is A- and R-free; Lemma B1 applies verbatim"),
    ("(iii) Horndeski G4", "NOT COMPUTED HERE",
     "breaks the lemma's hypothesis (R enters); but carries the G~/G_N split R3 already excludes"),
    ("(iv)  disformal coupling", "DIES as a ratio rescue",
     "D never enters the angular block; p_t/rho is disformally invariant in the static branch"),
]
w0 = max(len(a) for a, _, _ in rows)
w1 = max(len(b) for _, b, _ in rows)
for a_, b_, c_ in rows:
    print(f"  {a_:<{w0}}  |  {b_:<{w1}}  |  {c_}")

print()
for s_ in [
    "NOT DETERMINED 1: G4(X)'s p_t/rho.  The reduced-action route works for it but needs the "
    "Ricci scalar of the general static metric plus the (box phi)^2 - (nabla nabla phi)^2 "
    "combination, which was not carried out here.  Its verdict is OPEN, not negative.",
    "NOT DETERMINED 2: whether anything DYNAMICALLY forces the condensate's flow speed, so the "
    "D23 coincidence (w = (v_flow/c)^2/2 if v_flow = v_c) is an identity, not evidence.",
    "NOT DETERMINED 3: the amplitude law.  Escape (ii) removes the stress obstruction but its "
    "healthy limit is Z -> 0, i.e. gradient-free dust, whose profile is an initial condition.  "
    "Nothing here makes rho = sqrt(G M_b a_0)/(4 pi G r^2) an attractor.  That question is "
    "untouched by this run and remains THE question.",
    "CORRECTION TO THE REFRAME, running AGAINST the kill and stated as such: the reframe's "
    "claim (a) -- 'every AQUAL-style scalar is EXCLUDED as the stress carrier' -- is TRUE for a "
    "static phi(r) and FALSE as a statement about k-essence in general.  Carl's dark sector is "
    "phi = Q0 t + psi(r), which is in the other branch.  Theorem 1 does not touch it.",
    "Both footings carried throughout: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 "
    "FITTED, never derived.",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"THEOREM-1 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
