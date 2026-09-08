#!/usr/bin/env python3
"""Explicit IC7 curvature-square action coefficient, not a closure certificate.

Uses the SAME IC6 density and its derivatives. Units m=h0=V_reference=1,
kappa=6 are the frozen IC6 expanding-witness normalization. The coefficient
is a field function, not a fit to wave eigenvalues. No empirical data used.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as s
import ic6_even_characteristics as old


@lru_cache(None)
def build():
    base = old.build()
    volume_log, l1, l2, l3, xi, u = base["variables"]
    rho, tau = s.symbols("rho tau", real=True)
    ell = s.log(s.Rational(9, 5))
    T = -s.Rational(27, 16)+54/(5*ell)
    b = -T/9-s.Rational(3, 8)
    substitution = {volume_log: 0, l1: rho/3, l2: rho/3, l3: rho/3}
    J = base["J"].subs(substitution, simultaneous=True)
    E = s.exp((4-3*u)*xi)
    h = base["H"].subs(substitution, simultaneous=True)+2*E*tau/J
    c = s.exp(u*xi)*J
    Dt = lambda f: s.diff(f, u)-b*s.diff(f, xi)
    M = s.Matrix([[s.diff(h, rho, 2)/4+s.diff(h, tau)/12, Dt(s.diff(h, rho))/2],
                  [Dt(s.diff(h, rho))/2, Dt(Dt(h))]]).subs(tau, 0)
    v = s.Matrix([s.diff(c, rho)/2, Dt(c)])
    evaluate = s.lambdify((rho, xi, u), s.Matrix(list(M)+list(v)), modules="mpmath", cse=True)
    return dict(h=h, c=c, M=M, v=v, evaluate=evaluate, rho=rho, xi=xi, u=u)


def trace_state(j, volume="1", zscale="0"):
    V = mp.mpf(volume)
    momenta = [-V*mp.exp(-mp.mpf(1)/2)*mp.mpf(j)]*3
    qfun = lambda xi, u: tuple(old.build()["aux_evaluate"](mp.log(V), *momenta, xi, u))
    q = mp.findroot(qfun, (mp.mpf(1)/4, mp.mpf(2)/3), tol=mp.mpf("1e-65"))
    return old.at_point([mp.log(V), *momenta, q[0], q[1], mp.mpf(zscale)])


def coefficient(background):
    rho = sum(background["momenta"])*mp.exp(-background["point"][0])
    values = build()["evaluate"](rho, background["xi"], background["u"])
    M = mp.matrix([[values[0], values[1]], [values[2], values[3]]])
    v = mp.matrix(list(values[4:6]))
    reference = build()["evaluate"](-3*mp.exp(-mp.mpf(1)/2), mp.mpf(1)/4, mp.mpf(2)/3)
    reference_M = mp.matrix([[reference[0], reference[1]], [reference[2], reference[3]]])
    ratio = mp.det(M)/mp.det(reference_M)
    cutoff = determinant_cutoff(ratio)
    # Explicit zero extension: never evaluate an inverse at determinant zero.
    value = cutoff*(v.T*(M**-1)*v)[0]/8 if cutoff else mp.mpf(0)
    return dict(M=M, v=v, c7=value, determinant_ratio=ratio, cutoff=cutoff)


def determinant_cutoff(ratio):
    distance = abs(ratio-1)
    if distance <= mp.mpf(1)/4:
        return mp.mpf(1)
    if distance >= mp.mpf(1)/2:
        return mp.mpf(0)
    x = 4*(distance-mp.mpf(1)/4)
    left, right = mp.exp(-1/x), mp.exp(-1/(1-x))
    return right/(left+right)


def coefficient_bridge(background):
    """Independent full canonical Hessian, including all trace-free derivatives."""
    result = old.pencil(background, mp.mpf(1), eigenvalues=False)
    V, z = mp.exp(background["point"][0]), background["point"][6]
    W = mp.matrix(6, 2)
    W[2, 0], W[4, 1], W[5, 1] = V, -background["b"], 1
    fullM = W.T*result["nongradient"]*W/V
    fullg = W.T*result["gradient"][:, 0]/(V*mp.exp(-2*z))
    invariant = coefficient(background)
    return dict(mass_residual=fullM-invariant["M"],
                source_residual=fullg+2*invariant["v"])


@lru_cache(None)
def symbolic_bridges():
    a, b, d, v1, v2 = s.symbols("a b d v1 v2")
    M = s.Matrix([[a, b], [b, d]])
    v = s.Matrix([v1, v2])
    c7 = (v.T*M.inv()*v)[0]/8
    S4 = -4*(v.T*M.inv()*v)[0]
    eps, R1, R2, c0, c1, c2, V = s.symbols("epsilon R1 R2 c0 c1 c2 V")
    action = V*(c0+eps*c1+eps**2*c2)*(eps*R1+eps**2*R2)**2
    xi, w = s.symbols("xi w", real=True)
    k, B3 = s.symbols("k B3", nonzero=True)
    result = {
        "general_schur_cancellation": s.factor(S4+32*c7),
        "quadratic_action_variation": s.diff(action, eps, 2).subs(eps, 0)-2*V*c0*R1**2,
        "curvature_factor_32": 2*V*c0*(4*k*k/B3**2)**2-32*V*c0*k**4/B3**4,
        "homogeneous_value": action.subs(eps, 0),
        "homogeneous_first_jet": s.diff(action, eps).subs(eps, 0),
        "witness_second_jet": s.diff(action, eps, 2).subs({eps: 0, c0: 0}),
        "covariant_measure": s.exp(xi+3*w)*s.exp(w-xi)-s.exp(4*w),
    }
    actual = build()
    witness = {actual["rho"]: -3*s.exp(-s.Rational(1, 2)),
               actual["xi"]: s.Rational(1, 4), actual["u"]: s.Rational(2, 3)}
    actual_M = actual["M"].subs(witness, simultaneous=True).applyfunc(s.simplify)
    actual_v = actual["v"].subs(witness, simultaneous=True).applyfunc(s.simplify)
    T = -s.Rational(27, 16)+54/(5*s.log(s.Rational(9, 5)))
    result.update(witness_M11=actual_M[0, 0], witness_M12=actual_M[0, 1]-2*T/9,
                  witness_determinant=actual_M.det()+4*T*T/81, witness_v1=actual_v[0],
                  witness_c7_numerator=(actual_v.T*actual_M.adjugate()*actual_v)[0])
    return {key: s.simplify(value) for key, value in result.items()}


def correction_matrix(background, k, factor=1):
    correction = mp.matrix(2, 2)
    correction[0, 0] = (32*factor*mp.exp(background["point"][0]-4*background["point"][6])
                         *coefficient(background)["c7"]*k**4)
    return correction


def repaired_pencil(background, k, factor=1):
    result = old.pencil(background, k, eigenvalues=False)
    correction = correction_matrix(background, k, factor)
    reduced = mp.matrix(result["reduced"])
    reduced[:2, :2] += correction
    return dict(reduced=reduced, correction=correction)


def repair_conditions(background, factor=1):
    previous = old.asymptotic_conditions(background)
    return dict(S4=previous["S4"]+correction_matrix(background, mp.mpf(1), factor),
                G2=previous["G2"], M0=previous["M0"])


def evolving_pencil(background, k):
    """Delta C alone changes E by -A Delta C; background and A,B unchanged.

    Cdot is absent in the exact second-order Euler equation. The old module
    computes Adot and Bdot along the actual constrained homogeneous flow.
    """
    previous = old.evolving_pencil(background, k)
    repaired = repaired_pencil(background, k)
    A = repaired["reduced"][2:4, 2:4]
    E, D = previous["E"]-A*repaired["correction"], previous["D"]
    companion = mp.matrix(4, 4)
    companion[:2, 2:4] = mp.eye(2)
    companion[2:4, :2], companion[2:4, 2:4] = E, D
    poles = mp.eig(companion, left=False, right=False)
    return dict(E=E, D=D, poles=poles,
                speed_squares=[-p*p/(k*k*background["physical_light_speed_squared"]) for p in poles])


def lagrangian_bridge(background, k):
    # Independent compact IC6 L, fully varied before eliminating shift/aux.
    independent = old.compact_lagrangian_bridge(background, k)["reduced"]
    independent[:2, :2] -= correction_matrix(background, k)
    H = repaired_pencil(background, k)["reduced"]
    C, B, A = H[:2, :2], H[:2, 2:4], H[2:4, 2:4]
    M = A**-1
    result = mp.matrix(4, 4)
    result[:2, :2], result[:2, 2:4] = B*M*B.T-C, -B*M
    result[2:4, :2], result[2:4, 2:4] = -M*B.T, M
    return independent-result


def report():
    mp.mp.dps = 80
    rows = []
    for j in ("0.998", "1", "1.002", "1.007"):
        bg = trace_state(j)
        cf = coefficient(bg)
        conditions = repair_conditions(bg)
        evolution = evolving_pencil(bg, mp.mpf("1e5"))
        rows.append(dict(trace_ratio=j, c7=mp.nstr(cf["c7"], 22),
                         determinant_cutoff=mp.nstr(cf["cutoff"], 8),
                         determinant_M=mp.nstr(mp.det(cf["M"]), 22),
                         auxiliary_residual=mp.nstr(mp.norm(mp.matrix(bg["auxiliary_residual"])), 8),
                         quartic_residual=mp.nstr(mp.norm(conditions["S4"]), 8),
                         mass_eigenvalues=[mp.nstr(x, 18) for x in mp.eigsy(conditions["M0"], eigvals_only=True)],
                         speed_squared=[mp.nstr(x, 24) for x in evolution["speed_squares"]]))
    shear = repair_conditions(old.state("sheared"))
    checks = {name: s.simplify(value) == 0 for name, value in symbolic_bridges().items()}
    return dict(candidate="IC7", full_theory="OPEN", units="m=h0=1, kappa=6",
                exact_bridge_checks=checks, isotropic_samples=rows,
                shear_gyro_remaining=mp.nstr(shear["G2"][0, 1], 22),
                shear_quartic_remaining=mp.nstr(shear["S4"][0, 0], 22),
                nonclaims=["No full physical scalar/vector/tensor closure", "No interval-certified sample speeds",
                           "No sheared or general inhomogeneous stability", "No observational or novelty claim"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-closure", action="store_true")
    args = parser.parse_args()
    result = report()
    print(json.dumps(result, indent=2))
    if not all(result["exact_bridge_checks"].values()):
        return 1
    return 2 if args.require_full_closure else 0


if __name__ == "__main__":
    raise SystemExit(main())
