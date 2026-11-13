#!/usr/bin/env python3
"""Exact PIK1 constrained quadratic check and scoped FRM1 counterexamples.

This computes the added matter action, not the Einstein-Hilbert scalar action.
The principal-sector health calculation fixes the metric and freezes q(t)>1.
Spatial FRW scale factor is set to 1 at the evaluation time (physical k).
gamma_L=0: the original one-sided Pi_+ stiffness has no global quadratic
Taylor form at Pi=0 and is not silently replaced by a two-sided stiffness.
"""
import argparse
import json
from pathlib import Path

import sympy as s


def calculate(mutation=None):
    checks = []

    def equal(name, actual, expected=0):
        residual = s.simplify(s.expand(actual - expected))
        checks.append({"name": name, "passed": residual == 0,
                       "residual": str(residual)})
        return residual

    def truth(name, value):
        checks.append({"name": name, "passed": bool(value), "value": str(value)})

    x, eps = s.symbols("x epsilon", real=True)
    q, C, K, pc = s.symbols("q C K Pi_c", positive=True)
    s1, s2 = s.symbols("S1 S2", real=True)
    alpha, zeta, p = [s.Function(n)(x) for n in ("alpha", "zeta", "p")]
    F0 = C * (q - 1)**2
    F1 = 2 * C * (q - 1)
    F2 = 2 * C
    B = (F0 - q * F1) * s1 / pc
    D = F0 * s2 / pc**2

    # Exact unitary constraints: tau=tau(t), Q=q/N, P^0=0,
    # Pi=(sqrt(h))^-1 d_i(sqrt(h) P^i). A conformal h=e^(2zeta)I
    # captures its determinant perturbation; lapse/shift cancel from Q sqrt(-g).
    N, z, P = [s.Function(n)(x) for n in ("N", "z", "P")]
    sqrt_h = s.exp(3*z)
    Pi = s.diff(P, x) + 3*P*s.diff(z, x)
    exact_prefactor = N*sqrt_h*C*(q/N - 1)**2
    exact_added = exact_prefactor*(s.exp(-Pi/pc) - 1)
    perturb = {N: 1 + eps*alpha, z: eps*zeta, P: eps*p}
    expanded_exact = exact_added.subs(perturb).doit()
    exact_l1 = s.simplify(s.diff(expanded_exact, eps).subs(eps, 0))
    exact_l2 = s.simplify(s.diff(expanded_exact, eps, 2).subs(eps, 0)/2)
    Bexp, Dexp = B.subs(s1, -1), D.subs(s2, 1)
    candidate_B = 0 if mutation == "drop-mixed" else Bexp
    candidate_D = 0 if mutation == "drop-divergence-square" else Dexp
    bulk_l2 = candidate_B*alpha*s.diff(p, x) + candidate_D*s.diff(p, x)**2/2
    boundary_l2 = -3*F0/pc*s.diff(zeta*p, x)
    equal("exact_first_order_is_spatial_boundary", exact_l1, -F0*s.diff(p, x)/pc)
    equal("exact_quadratic_equals_bulk_plus_boundary", exact_l2, bulk_l2 + boundary_l2)

    # Independent order of operations: vary the full nonlinear gate FIRST,
    # linearize its Euler derivatives, compare with variation of candidate L2.
    def euler(L, field):
        return s.diff(L, field) - s.diff(s.diff(L, s.diff(field, x)), x)

    direct_linear = {}
    for name, field, perturbation in [("lapse", N, alpha), ("polarization", P, p), ("metric_trace", z, zeta)]:
        direct = euler(exact_added, field).subs(perturb).doit()
        direct = s.simplify(s.diff(direct, eps).subs(eps, 0))
        via_l2 = s.simplify(euler(bulk_l2, perturbation))
        equal("direct_variation_vs_quadratic_" + name, direct, via_l2)
        direct_linear[name] = str(direct)

    # General Taylor coefficients, independent from the exponential check.
    generic_added = exact_prefactor*(s1*Pi/pc + s2*Pi**2/(2*pc**2))
    generic_l2 = s.simplify(s.diff(generic_added.subs(perturb).doit(), eps, 2).subs(eps, 0)/2)
    equal("general_gate_coefficients", generic_l2,
          B*alpha*s.diff(p, x) + D*s.diff(p, x)**2/2
          + 3*F0*s1/pc*s.diff(zeta*p, x))
    equal("B_closed_form", B, C*(1-q*q)*s1/pc)

    # Direct constrained clock expansion on Minkowski, tau=q t+epsilon*pi.
    # Jets v=pi_t, w=pi_x obey w_t=v_x. P^x=epsilon*p and
    # P^0=-tau_x P^x/tau_t enforces n.P=0 before expansion.
    v, w, pp, vt, vx, wx, pt, px = s.symbols("v w p vt vx wx pt px", real=True)
    T, X = q + eps*v, eps*w
    Q = s.sqrt(T*T - X*X)
    Px = eps*pp
    P0 = -X*Px/T

    def dt(expr):
        return s.diff(expr, v)*vt + s.diff(expr, w)*vx + s.diff(expr, pp)*pt

    def dx(expr):
        return s.diff(expr, v)*vx + s.diff(expr, w)*wx + s.diff(expr, pp)*px

    direct_Pi = (dt(Q*P0) + dx(Q*Px))/Q
    pi1 = s.simplify(s.diff(direct_Pi, eps).subs(eps, 0))
    pi2 = s.simplify(s.diff(direct_Pi, eps, 2).subs(eps, 0)/2)
    equal("constrained_Pi_first_order", pi1, px)
    equal("constrained_Pi_second_order", pi2, -w*pt/q)
    q2 = s.simplify(s.diff(Q, eps, 2).subs(eps, 0)/2)
    equal("clock_rate_second_order", q2, -w*w/(2*q))
    # A_x=n^mu d_mu n_x. n^0=T/Q, n^x=-X/Q, n_x=-X/Q.
    n0, nx = T/Q, -X/Q
    Ax = n0*dt(nx) + nx*dx(nx)
    ax1 = s.simplify(s.diff(Ax, eps).subs(eps, 0))
    equal("clock_acceleration_first_order", ax1, -vx/q)
    clock_raw = F2*v*v/2 - F1*w*w/(2*q) - pp*vx/q - K*pp*pp/2
    clock_raw += F1*s1*v*px/pc + F0*s1*pi2/pc + D*px*px/2
    clock_bulk = F2*v*v/2 - F1*w*w/(2*q) + (1-B)*v*px/q - K*pp*pp/2 + D*px*px/2
    # raw-bulk = -(v_x p+v p_x)/q + F0*S1/(q pc)*[-d_t(wp)+d_x(vp)].
    boundary_clock = -(vx*pp + v*px)/q + F0*s1/(q*pc)*(-(vx*pp+w*pt)+(vx*pp+v*px))
    equal("clock_quadratic_modulo_explicit_boundaries", clock_raw-clock_bulk, boundary_clock)
    equal("gauge_mixing_agrees_alpha_minus_pi_dot_over_q", (F1-F0/q)*s1/pc, -B/q)

    # Auxiliary longitudinal P, frozen-background fixed-metric principal sector.
    k2, velocity, amp = s.symbols("k_squared velocity P_amplitude", positive=True)
    A = 1-B
    denom = K-D*k2
    coupling = A/q
    keff = F2 + coupling**2*k2/denom
    omega2 = s.factor((F1/q)*k2/keff)
    mode_L = F2*velocity**2/2 + coupling*s.sqrt(k2)*velocity*amp - denom*amp**2/2
    p_stationary = s.solve(s.diff(mode_L, amp), amp)[0]
    equal("auxiliary_elimination_by_completion_square",
          mode_L.subs(amp, p_stationary), keff*velocity**2/2)
    equal("dispersion_determinant", omega2*(F2*denom+coupling**2*k2)-(F1/q)*k2*denom)
    exp_values = {q: 2, C: 1, K: 1, pc: 1, s1: -1, s2: 1, k2: s.Rational(3,2)}
    ghost_K = s.simplify(keff.subs(exp_values))
    ghost_w2 = s.simplify(omega2.subs(exp_values))
    equal("exponential_negative_kinetic_witness", ghost_K, -1)
    equal("exponential_negative_frequency_witness", ghost_w2, -s.Rational(3,2))
    # For any A != 0 and D>0, K_eff diverges to -infinity just above k_*.
    eta = s.symbols("eta", positive=True)
    scaled_limit = s.limit(eta*keff.subs(k2, K*(1+eta)/D), eta, 0, dir="+")
    equal("generic_above_threshold_negative_kinetic_coefficient", scaled_limit, -A*A/(q*q*D))
    u = s.symbols("u", real=True)
    flat_gate = s.exp(-u**3)
    equal("flat_gate_first_derivative_zero", s.diff(flat_gate,u).subs(u,0))
    equal("flat_gate_second_derivative_zero", s.diff(flat_gate,u,2).subs(u,0))
    equal("flat_gate_restores_baseline_kinetic", keff.subs({s1:0,s2:0}), F2+k2/(q*q*K))
    # Original failing witness must now be retained as a positive non-boundary test.
    periodic = s.integrate(s.cos(x)**2/2, (x, 0, 2*s.pi))
    equal("historical_periodic_witness_nonzero", periodic, s.pi/2)
    truth("historical_invisibility_hypothesis_refuted", periodic != 0)

    # FRM1: restricted baryon-loss ceiling, then counterexamples outside it.
    U, fb = s.symbols("u fb", positive=True)
    loss_X = (s.sqrt(1+4*U*fb)-1)/(2*fb)
    equal("baryon_loss_rationalized", loss_X, 2*U/(1+s.sqrt(1+4*U*fb)))
    equal("baryon_loss_limit", s.limit(loss_X, fb, 0, dir="+"), U)
    merge_X = s.sqrt(5)-1  # f_C=2, f_b=1, u=1
    truth("permitted_charge_transport_exceeds_restricted_ceiling", merge_X > 1)
    contracted_X = (s.sqrt(401)-1)/2  # g_b,f=g_bar/100, f_C=f_b=1
    truth("free_formation_field_exceeds_restricted_ceiling", contracted_X > 1)

    return {
        "status": "PASS" if all(c["passed"] for c in checks) else "FAIL",
        "mutation": mutation,
        "checks": checks,
        "formulas": {"B": str(s.factor(B)), "D": str(D), "unitary_bulk_L2": str(B*alpha*s.diff(p,x)+D*s.diff(p,x)**2/2),
                     "direct_linear_euler_exponential": direct_linear,
                     "clock_kinetic": str(s.factor(keff)), "clock_omega_squared": str(omega2),
                     "clock_constraint_denominator": str(denom)},
        "health": {"scope": "fixed metric, q frozen >1, gamma_L=0, physical k; not coupled-gravity health",
                   "exponential_witness": {"q":2,"C":1,"K":1,"Pi_c":1,"k_squared":"3/2","K_eff":str(ghost_K),"omega_squared":str(ghost_w2)},
                   "conclusion":"Generic exponential gate has a negative-kinetic/negative-frequency band just above K/D in this principal sector; flat-at-origin gate remains unexcluded."},
        "non_claims": ["No completed cluster/galaxy pipeline or numerical field solution",
                       "No full coupled Einstein-lapse-shift scalar spectrum",
                       "No global Taylor replacement of the original one-sided Pi_+ stiffness",
                       "No physical calibration of Pi_c or ultraviolet cutoff",
                       "No derived halo retention, formation epoch or amount"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--mutation", choices=["drop-mixed", "drop-divergence-square"])
    args = parser.parse_args()
    result = calculate(args.mutation)
    for check in result["checks"]:
        print(("PASS" if check["passed"] else "FAIL") + " " + check["name"] + ": " + check.get("residual", check.get("value", "")))
    print(result["health"]["conclusion"])
    print("STATUS=" + result["status"])
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
