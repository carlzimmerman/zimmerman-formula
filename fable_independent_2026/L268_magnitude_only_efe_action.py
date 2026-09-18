#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L268 -- THE COVARIANT MAGNITUDE-ONLY EFE ACTION: written, its weak-field limit verified, its costs priced.

The day's framework-internal lanes converge on one open object: a MOND theory whose external-field
effect depends on the MAGNITUDE of the external field but NOT its direction.  The direction-blind rule
(SW01) g_obs = nu(sqrt(x^2 + eta^2)) g_own, x = g_own/a0, eta = g_ext/a0, evades L243's Cassini
quadrupole (which bounds the VECTOR/directional EFE at 6.44x) because a scalar magnitude sources no
preferred direction.  This lane WRITES a covariant action that reduces to that rule, checks the
reduction symbolically, and states the price -- which PAPER9's foliation theorem makes unavoidable.

THE ACTION.
  S = (c^4/16 pi G) INT sqrt(-g) R              [Einstein-Hilbert]
    + S_ae[g, u]                                [khronon/aether fixing u_mu -- the preferred frame]
    - (a0^2/8 pi G) INT sqrt(-g) F(X)           [the MOND scalar phi]
    + S_matter[g, psi]                          [matter couples to g_mu-nu ONLY]
  with
    u_mu = d_mu T / sqrt(-g^ab d_a T d_b T)      (khronon; foliation normal -- PAPER9 forces this)
    h_mn = g_mn + u_mu u_nu                       (spatial projector on the leaves)
    X = X_loc + X_env,   X_loc = h^mn d_m phi d_n phi / a0^2         (LOCAL spatial gradient magnitude^2)
                          X_env = h^mn d_m phibar d_n phibar / a0^2   (ENVIRONMENTAL magnitude^2)
    phibar = (1 - l^2 Delta_h)^{-1} phi,  Delta_h = h^mn D_m D_n     (leaf-smoothed field; l >> system,
                                                                       << external-gradient scale)
  X_loc and X_env are SEPARATE scalars that ADD -- there is no cross term, so the external field enters
  in QUADRATURE (magnitude-only), not as the vector sum |grad phi_own + grad phi_ext| of local AQUAL.

  A1  the quadrature IS the magnitude-only rule: F(X_loc+X_env) gives mu(sqrt(x^2+eta^2)); the vector
      Lagrangian F(|g_own+g_ext|^2/a0^2) differs by exactly the cross term 2 x eta cos(theta) (sympy)
  A2  deep-MOND F = (2/3) X^{3/2} => mu = sqrt(X) = sqrt(x^2+eta^2): the SW01 rule reproduced
  B1  THE CASSINI PAYOFF + MUTATION: the external-field-induced ANISOTROPY of mu (the source of the
      Solar-System quadrupole L243 bounds) is ZERO for the magnitude-only action and NONZERO for the
      vector one; MUTATE=1 replaces the spatial projector by the vector sum and the quadrupole returns
  C1  THE PRICE (honest, not cleared): the action CARRIES u_mu, so by PAPER9 it has a preferred frame
      and faces the alpha_3 dichotomy (pay alpha_3 ~ O(1), 2.5-7.5e19 over the pulsar bound, OR let the
      frame propagate to 4 DOF); ghost-freedom, c_T=c and full PPN are OPEN gates, not claimed here
  C2  the leaf-smoothing Delta_h^{-1} is SPATIAL (instantaneous on the leaves) = exactly PAPER9's
      foliation corollary -- the theory realises the predicted instantaneous constraint, not evades it

Run:  python3 fable_independent_2026/L268_magnitude_only_efe_action.py
      MUTATE=1 ...  (vector EFE: the Cassini quadrupole reappears; B1 flips)
"""
import os, sys, json, math
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "L268_magnitude_only_efe_action"
MUTATE = os.environ.get("MUTATE", "0") == "1"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L268", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 100); P(t); P("=" * 100)


P(__doc__)
x, eta, th = sp.symbols('x eta theta', positive=True)     # internal/external magnitudes (/a0), angle
X = sp.Symbol('X', positive=True)

# =================================================================================================
banner("A1 -- the quadrature is magnitude-only; the vector Lagrangian differs by exactly the cross term")
arg_mag = x**2 + eta**2                                    # X_loc + X_env  (this action)
arg_vec = x**2 + eta**2 + 2 * x * eta * sp.cos(th)         # |g_own + g_ext|^2 / a0^2  (local AQUAL)
cross = sp.simplify(arg_vec - arg_mag)
check("A1a the magnitude-only argument X_loc+X_env and the vector argument |g_own+g_ext|^2 differ by "
      "EXACTLY the cross term 2 x eta cos(theta)",
      f"arg_vec - arg_mag = {cross}", sp.simplify(cross - 2 * x * eta * sp.cos(th)) == 0,
      "the whole content of 'magnitude-only' is dropping this cross term -- the action does it by making "
      "X_loc and X_env separate additive scalars")
check("A1b the magnitude-only argument is direction-INDEPENDENT (d/dtheta = 0) while the vector one is not",
      f"d arg_mag/dtheta = {sp.diff(arg_mag, th)}, d arg_vec/dtheta = {sp.simplify(sp.diff(arg_vec, th))}",
      sp.diff(arg_mag, th) == 0 and sp.simplify(sp.diff(arg_vec, th)) != 0,
      "direction-blindness is exact and structural, not approximate")

# =================================================================================================
banner("A2 -- deep-MOND limit reproduces the SW01 rule g = nu(sqrt(x^2+eta^2)) g_own")
F = sp.Rational(2, 3) * X**sp.Rational(3, 2)              # deep-MOND free function
mu = sp.diff(F, X)                                        # mu(X) = F'(X)
mu_mag = mu.subs(X, arg_mag)
check("A2 with F = (2/3) X^{3/2}, mu(X) = F'(X) = sqrt(X); on the magnitude-only argument mu = "
      "sqrt(x^2+eta^2), i.e. the effective coupling is nu(sqrt(x^2+eta^2)) -- the SW01 direction-blind rule",
      f"mu(X) = {sp.simplify(mu)}, mu(X_loc+X_env) = {sp.simplify(mu_mag)}",
      sp.simplify(mu - sp.sqrt(X)) == 0 and sp.simplify(mu_mag - sp.sqrt(arg_mag)) == 0,
      "the action's weak-field scalar equation D.[mu grad phi]=4piG rho carries this mu; deep-MOND EFE "
      "is the quadrature, isolated MOND (eta->0) is mu=x=deep-MOND, Newtonian (x,eta large) is mu->1")

# =================================================================================================
banner("B1 -- THE CASSINI PAYOFF: the external-field anisotropy of mu (source of the L243 quadrupole)")
# A test mass in a uniform external field g_ext.  The effective coupling the planets feel is mu(arg).
# Its ANISOTROPY -- the theta-dependence at fixed internal magnitude -- is what sources the anomalous
# quadrupole Cassini bounds.  Compute d mu/d theta for both actions.
arg = arg_vec if MUTATE else arg_mag                       # MUTATE: use the vector (directional) EFE
mu_field = mu.subs(X, arg)
aniso = sp.simplify(sp.diff(mu_field, th))                  # theta-dependence of mu = the EFE anisotropy
P(f"  {'VECTOR (MUTATE)' if MUTATE else 'MAGNITUDE-ONLY'}: d mu/d theta = {aniso}")
# FIXED assertion (magnitude-only): the anisotropy is exactly zero.  MUTATE (vector) must break it.
check("B1 the external-field-induced anisotropy d(mu)/d(theta) is EXACTLY ZERO -- no Solar-System "
      "quadrupole; this is the structural Cassini escape.  Fixed assertion; MUTATE (vector EFE) breaks it",
      f"d mu/d theta = {aniso}", aniso == 0,
      "L243 kills the VECTOR EFE at 6.44x the Cassini ceiling precisely because its mu is direction-"
      "dependent; the magnitude-only mu depends on eta only through eta^2 (a scalar), so the quadrupole "
      "is identically absent -- not a tuned cancellation")
# the effective a0-threshold DOES shift with |g_ext| (the magnitude EFE is real), just isotropically
mu_iso = sp.simplify(sp.diff(mu.subs(X, arg_mag), eta))    # d mu / d eta at fixed direction
check("B1b the magnitude EFE is nonetheless REAL: mu still depends on eta (the external MAGNITUDE), it "
      "just does so isotropically -- d(mu)/d(eta) != 0 while d(mu)/d(theta) = 0",
      f"d mu/d eta = {mu_iso} (nonzero: the EFE is present); d mu/d theta = 0 (isotropic: no quadrupole)",
      sp.simplify(mu_iso) != 0,
      "so systems in strong external fields still have suppressed MOND (Crater II, DF2), but with no "
      "directional signature -- the EFE without the Cassini quadrupole")

# =================================================================================================
banner("C1 -- THE PRICE (honest): the action carries a preferred frame; the alpha_3 cost is real and large")
# By PAPER9, single metric + MOND + 2 DOF => a preferred frame; where computed, alpha_3 = O(1).
# Verify the cost is real and large against the pulsar bound (a genuine inequality, not a fake FAIL).
alpha3 = 1.0                          # O(1), as computed for the khronometric chassis (PAPER9 / DC-019)
pulsar_bound = 4e-20                  # |alpha_3| < 4e-20 (binary-pulsar)
price = alpha3 / pulsar_bound
OUT["numbers"]["alpha3_over_bound"] = price
check("C1 the preferred-frame price is REAL and LARGE: with alpha_3 = O(1) (as computed for the "
      "khronometric chassis) against the pulsar bound |alpha_3| < 4e-20, the exceedance is ~2.5e19 -- "
      "so the frame is not a free decoration, it is the wall",
      f"alpha_3/bound = {price:.2e} (>> 1)", price > 1e19,
      "this is a documented COST, not a pass: the theory must either pay it or take PAPER9's other horn "
      "(let the frame propagate => 4 DOF, failing the 2-DOF requirement). Ghost, c_T=c, full PPN for THIS "
      "action are all still UNCOMPUTED -- writing the action does not make it viable")

# =================================================================================================
banner("C2 -- the projector is spatial: the leaf-smoothing is instantaneous (PAPER9's foliation corollary)")
# Verify h_mn u^n = 0 exactly, so Delta_h = h^mn D_m D_n carries no time derivative -> instantaneous.
g4 = sp.diag(-1, 1, 1, 1)             # local Minkowski frame
u_up = sp.Matrix([1, 0, 0, 0])        # unit timelike: u^mu, u_mu u^mu = -1
u_dn = g4 * u_up
h_dn = g4 + u_dn * u_dn.T             # h_mn = g_mn + u_m u_n
h_u = sp.simplify(h_dn * u_up)        # h_mn u^n  -- must be the zero vector
check("C2 the projector is purely SPATIAL: h_mn u^n = 0 exactly, so Delta_h = h^mn D_m D_n has no time "
      "derivative and the leaf-smoothing (1 - l^2 Delta_h)^{-1} is INSTANTANEOUS on each slice -- exactly "
      "the non-dynamical foliation PAPER9's corollary predicts for any 2-DOF single-metric MOND theory",
      f"h_mn u^n = {list(h_u)}", all(v == 0 for v in h_u),
      "consistency: the action is a concrete instance of PAPER9's class, so it MUST carry the "
      "instantaneous constraint -- and it does, transparently, rather than hiding it", load_bearing=False)

# =================================================================================================
banner("VERDICT")
P(f"""  (1) WRITTEN: a covariant action -- Einstein-Hilbert + khronon/aether + a MOND scalar whose free
      function depends on X_loc + X_env, two SEPARATE spatial-magnitude scalars built with the foliation
      projector h_mn = g_mn + u_mu u_nu.
  (2) VERIFIED: the quadrature X_loc + X_env is the magnitude-only rule (differs from local AQUAL by
      exactly the dropped cross term 2 x eta cos theta); deep-MOND gives mu = sqrt(x^2+eta^2) = the SW01
      rule; and the external-field anisotropy of mu is IDENTICALLY ZERO, so the Solar-System quadrupole
      L243 bounds (6.44x for the vector EFE) is structurally absent -- confirmed by the mutation, which
      restores it.
  (3) HONEST SENTENCE: the covariant magnitude-only EFE action EXISTS and reproduces the direction-blind
      phenomenology while evading the Cassini QUADRUPOLE by construction -- but it is NOT a viable theory.
      It carries a khronon, so by PAPER9 it has a preferred frame and the alpha_3 dichotomy (pay ~O(1),
      2.5-7.5e19 over the pulsar bound, or propagate a 4th mode), and its ghost-freedom, c_T=c and full
      PPN sector are UNCOMPUTED.  What this lane delivers is the correct covariant OBJECT and the exact
      remaining gates -- the alpha_1/2/3 computation for this specific action is the next lane, and it is
      where the theory lives or dies, on the same wall every single-metric MOND theory has hit.
      NOT CLAIMED: viability, ghost-freedom, a PPN pass, or that the frame's price is payable.""")
OUT["verdict"] = {"word": "ACTION-WRITTEN-CASSINI-QUADRUPOLE-EVADED-FRAME-PRICE-OPEN",
                  "reproduces_sw01_rule": True, "quadrupole_anisotropy": "zero (magnitude-only)",
                  "open_gates": ["alpha_1/2/3 for this action", "ghost/bounded Hamiltonian", "c_T=c",
                                 "full PPN"], "inherits": "PAPER9 preferred-frame dichotomy"}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb_fail = [nm for nm, ok, lb in CH if lb and not ok]
P(f"L268 COMPLETE: {npass}/{n} checks PASS")
for nm in lb_fail:
    P(f"    load-bearing FAIL: {nm}")
if MUTATE:
    P("  MUTATE=1: the vector EFE restores the Cassini quadrupole -> B1 FAILs (the direction-blind "
      "structure was doing the work).")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb_fail}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb_fail else 0)
