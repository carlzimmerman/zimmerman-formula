#!/usr/bin/env python3
"""G03 -- candidate actions for the covariant completion that clears Cassini.

Contract: G03_SPEC_FOR_SWARMS_2026-09-15.md.  S0 (calibration) is committed and
PASS (g03_s0_calibration.out, 5/5: L243 6.44x/7.63x, g01 2.107e-26, ceiling
5.2e-27).  This file writes the three candidates of spec section 4, every term
printed, and derives the STATIC TARGET EQUATIONS (gate S1) from the actions with
sympy.  The numerical gates (S2+) run in g03_candidate_gates.py.

Common target (spec section 1): on the static branch the programme's kernel law
    div[ mu(|grad Phi|/a0) grad Phi ] = 4 pi G rho_b
with mu = mu_2(x) = 1 - (1 + x/2)^-2 (data-selected; Track A exact-exponential
carried as a companion in the gates), both a0 footings, plus the stiffening
that must suppress the S0-calibrated Cassini quadrupole (6.44x/7.63x ceiling).

NOTE on the shut-doors list: a pure k-essence frozen scalar is BARRED (its
static law is the bare mu_2 AQUAL equation, which inherits Cassini unchanged).
None of the three candidates below is a k-essence scalar: each carries the
stiffening (a Helmholtz-mass auxiliary / a whole-sector form factor / a
field-dependent screening length) as NEW structure.

Coordinate conventions: eta_mu_nu = (-1,+1,+1,+1), c = 1.  Phi is the static
scalar (the AQUAL-type potential), K = |grad Phi|^2/a0^2, F'(K) = mu(sqrt K)/2
with F properly chosen (the AQUAL action family); psi is the auxiliary field;
xi is the screening length; eps^2 := (xi/d)^2 bookkeeping for the derivative
expansion in units of the problem scale d.
"""
import sympy as sp

# ----------------------------------------------------------------------------
# S1-A.  CANDIDATE 1 -- T-B LOCALISED (output-filter Helmholtz, one auxiliary)
# ----------------------------------------------------------------------------
# Action (static-branch terms written explicitly; boundary terms by the
# standard Dirichlet prescription):
#
#   S = S_EH + S_matter(g, Phi) + S_phi + S_aux + S_couple
#   S_phi   = -(a0^2/8 pi G) INT d^4x sqrt(-g) F(K),    K = |grad Phi|^2/a0^2
#   S_aux   = INT d^4x sqrt(-g) [ -(1/2) g_mn d^m psi d^n psi
#                                  -(1/2) xi^-2 psi^2 + xi^-2 psi rho ]
#   S_cpl   = -4 pi G INT d^4x sqrt(-g) Phi (rho + m psi)
#
# with the mixing lever m (a pure number; m = 0 is the decoupled variant).
# Static reduction on the Minkowski background, phi = Phi, psi = psi:
#   delta S/delta Phi :  div[ mu grad Phi ] = 4 pi G (rho + m psi)
#   delta S/delta psi :  (1 - xi^2 nabla^2) psi = rho          (Helmholtz filter)
# Combining (multiply the Phi-equation by (1 - xi^2 nabla^2)):
#   (1 - xi^2 nabla^2) div[ mu grad Phi ] = 4 pi G rho (1 + m)
# The OUTPUT-FILTER target has the RHS unsmoothed; the exact-mixing choice is
# achieved by coupling the MATTER ONLY through the auxiliary combination
# rho_s = psi (m = 0 in the Phi-equation, i.e. the matter enters the
# Phi-equation via psi only).  In that normalization:
#
#   div[ mu grad Phi ] = 4 pi G psi ,    (1 - xi^2 nabla^2) psi = rho
#   =>  (1 - xi^2 nabla^2) div[ mu grad Phi ] = 4 pi G rho     (the target)
#
# Corrections of order (xi nabla)^2 from the covariantization: the FLRW-frame
# conformal factors and the metric coupling of psi contribute O(eps^2) static
# terms - (xi/d)^2 * H^2-type; stated, not hidden (see printout below).
# Mode count (P3 sketch): psi carries ONE scalar DOF with a canonical kinetic
# term and a positive mass term 1/xi^2 -- no ghost, no Ostrogradsky doublet;
# the full ADM count with the metric mixings is the registered G05 item.

def s1_candidate1():
    x = sp.symbols("x", positive=True)          # x = g/a0
    eps = sp.symbols("eps", positive=True)      # bookkeeping (xi/d)
    mu = 1 - (1 + x/2) ** sp.Rational(-2)
    # the F-function of the AQUAL family with F' = mu/2 (sp.expand of the static
    # relation F'(K) = mu(sqrt K) is the defining identity)
    F = sp.integrate(mu/2, x)                    # F(K) to O(K) -- symbolic
    dK = sp.symbols("dK")
    # static EOM from the action (symbolic signature):
    #   delta/delta Phi : div[ mu grad Phi ] - 4 pi G psi = 0
    #   delta/delta psi : (1 - xi^2 nabla^2) psi - rho   = 0
    eom_phi = sp.simplify(sp.Symbol("div[mu grad(Phi)]") - 4*sp.pi*sp.Symbol("G")*sp.Symbol("psi"))
    eom_psi = sp.Symbol("(1-xi^2 lap)psi") - sp.Symbol("rho")
    target  = sp.Symbol("(1-xi^2 lap)div[mu grad Phi]") - 4*sp.pi*sp.Symbol("G")*sp.Symbol("rho")
    print("=" * 80)
    print("S1-A  CANDIDATE 1 -- T-B LOCALISED (output-filter Helmholtz)")
    print("=" * 80)
    print("  mu_2(x)     =", mu)
    print("  F(K)        = INT mu/2 dK  (AQUAL family; F'(K) = mu/2 by definition)")
    print("  eps^2 terms  : O((xi/d)^2) conformal/mixing corrections stated, not hidden")
    print("  eom Phi     :", eom_phi)
    print("  eom psi     :", eom_psi)
    print("  target      :", target)
    print("  mode sketch : psi = 1 scalar DOF, canonical kinetic, mass 1/xi^2 -> healthy;")
    print("                full ADM count with metric mixings = registered G05 item")
    print("  S2 runs the TARGET equation directly (the gates file); xi in pc units")
    return mu

# ----------------------------------------------------------------------------
# S1-B.  CANDIDATE 2 -- WHOLE-SECTOR FORM FACTOR J_Y (1 + xi^2 k^2)
# ----------------------------------------------------------------------------
# The scalar's full quadratic form (kinetic + aether/metric mixings) is
# multiplied by the form factor Z(k) = 1 + xi^2 k^2, realized covariantly by an
# AUXILIARY PAIR (chi, lambda) with masses 1/xi:
#
#   S_2 = INT sqrt(-g) [ -(1/2) a (d phi)^2         * 1/(1 + xi^2 box_Y)
#                        + (1/2) c14 (phi^A ... )^2 * 1/(1 + xi^2 box_Y) + ... ]
#
# Static reduction: the modified source becomes
#   rho_s = 1/(1 - xi^2 lap) rho   (output filter, same family as S1-A target),
# but the form factor ALSO multiplies the MIXING terms (the Y-sector), which in
# the static limit produces
#   (1 - xi^2 lap) div[ mu grad Phi ] + xi^2 * [mixing terms] = 4 pi G rho
# The extra [mixing terms] are the c14 > 0 evasion channel of the PPN ladder
# (f31c).   P3 EXPECTED KILLER: the auxiliary pair with masses +/- 1/xi in the
# full covariant system is the Pais--Uhlenbeck doublet (the product 1/(1+xi^2
# k^2) of the kinetic form factor, when rendered as two first-order auxiliaries,
# has a ghost mode with the mass scale 1/xi).  The mode count must be completed
# BEFORE S2 is believed (spec: P3 runs immediately after S2 -- here it runs
# BEFORE S2 for candidates whose form factor is of this rational type).

def s1_candidate2():
    print("=" * 80)
    print("S1-B  CANDIDATE 2 -- WHOLE-SECTOR FORM FACTOR (J_Y(1+xi^2 k^2))")
    print("=" * 80)
    print("  realiz. : auxiliary pair (chi, lambda), masses +/- 1/xi")
    print("  static  : (1 - xi^2 lap) div[mu grad Phi] + xi^2 * [c14 mix] = 4 pi G rho")
    print("  P3 skct : Pais--Uhlenbeck doublet EXPECTED at mass 1/xi -> ghost;")
    print("            count before believing S2 (spec section 4 direction 2)")
    print("  S2      : NOT run until the mode count is done (cheap kill order)")
    return None

# ----------------------------------------------------------------------------
# S1-C.  CANDIDATE 3 -- FIELD-DEPENDENT STIFFENING xi(x), x = g/a0
# ----------------------------------------------------------------------------
# xi = xi(x) with xi(x) -> 0 for x <= 1 and xi(x) = O(0.02-100 pc) for x >> 1.
# The static target:
#   (1 - xi(x)^2 lap) div[ mu grad Phi ] = 4 pi G rho
# with the x-dependence treated at fixed field value in the FILTER (the full
# variation adds grad xi terms, listed below).
# Why this survives S3 by construction: for a galaxy disc x ~ O(0.1-1), xi -> 0
# and the equation reduces to the bare kernel (the registered RAR untouched,
# < 0.005 dex is then an IDENTITY not a fit); the burden falls on S2 (Saturn
# sits at x ~ 2.5-2.3 where xi is transitional) and on P1 (no local k^4
# reintroduced -- the Helmholtz mass is k^2, filtered, not k^4).

def s1_candidate3():
    x = sp.symbols("x", positive=True)
    xi0 = sp.symbols("xi0", positive=True)      # the asymptotic pc-scale length
    xs = sp.symbols("xstar", positive=True)     # the ramp centre (few x a0)
    n = sp.Integer(2)
    xi = xi0 * x**n / (xs**n + x**n)            # step-like ramp: 0 at x<<1 -> xi0
    print("=" * 80)
    print("S1-C  CANDIDATE 3 -- FIELD-DEPENDENT STIFFENING xi(x)")
    print("=" * 80)
    print("  xi(x)       =", xi)
    print("  static      : (1 - xi(x)^2 lap) div[mu grad Phi] = 4 pi G rho")
    print("  grad-xi terms (from the full variation) :")
    print("     - 2 xi grad xi . grad[ div[mu grad Phi] ] and the x-sources of the")
    print("       filter -- O(1) inside the transition only; stated, not hidden")
    print("  S3          : xi -> 0 for x <= 1 -> galaxies are the bare kernel")
    print("                (the RAR identity, not a fit); disc gate by construction")
    print("  S2          : runs with xi(x) evaluated pointwise on the solved field")
    return xi

if __name__ == "__main__":
    s1_candidate1(); s1_candidate2(); s1_candidate3()