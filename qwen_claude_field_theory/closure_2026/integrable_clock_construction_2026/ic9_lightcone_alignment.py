#!/usr/bin/env python3
"""IC9: optical auxiliary alignment, no curvature-square counterterm.

This is a new action, not IC6 or IC7 with reused physical passes. The exact
plateau Hamiltonian and compact Lagrangian are differentiated independently.
The original MOND primitive/trace potential and matter metric are retained.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as s
import ic6_even_characteristics as geometry
import ic8_shear_integrability as mechanics

BASE = "0aa6e0cef9f8b9f0e6fc7129bedfa12ef055914e"


@lru_cache(None)
def build():
    trace_model = mechanics.build()
    vol, l1, l2, l3, xi, u = variables = trace_model["variables"]
    rho, tau = trace_model["rho"], trace_model["tau"]
    z, interface_slope = s.symbols("logB3 interface_slope", real=True)
    S = s.Symbol("S", real=True)
    optical = (2-u)*xi
    K = 2*s.exp(optical+s.Rational(1, 6))
    c = s.exp(optical-s.Rational(1, 6))
    J = s.exp(-2*(u-1)*xi-s.Rational(1, 6))
    alpha = 81/(8*trace_model["T"]**2)
    htrace = trace_model["htrace"]
    h = K*tau+htrace
    trace = l1+l2+l3
    shear2 = l1*l1+l2*l2+l3*l3-trace*trace/3
    H = s.exp(vol)*h.subs({rho: trace*s.exp(-vol), tau: shear2*s.exp(-2*vol)}, simultaneous=True)
    C = s.exp(vol-2*z)*c
    Cderivatives = s.Matrix([C, 2*s.diff(C, vol), s.diff(C, vol)-2*C]
                            +[s.diff(C, x) for x in (l1, l2, l3, xi, u)])
    aux = s.Matrix([s.diff(H, x) for x in (xi, u)])
    # |D S|²=(2-u)² |Dxi - xi/(2-u) Du|²; both factors vary.
    effective_alpha, effective_b = alpha*(2-u)**2, -xi/(2-u)
    data = s.Matrix(list(s.hessian(H, variables))+list(Cderivatives)+list(aux)
                    +[J, effective_alpha, effective_b]+[s.diff(H, x) for x in variables])
    evaluate = s.lambdify(variables+(z,), data, "mpmath", cse=True)
    aux_evaluate = s.lambdify(variables, aux, "mpmath", cse=True)
    Ltrace = htrace.subs(xi, S/(2-u))
    Ks, cs = K.subs(xi, S/(2-u)), c.subs(xi, S/(2-u))
    B = alpha*s.exp(u*S/(2-u))
    Lrr, Lrt, Ltt = s.diff(Ltrace, rho, 2), s.diff(Ltrace, rho, u), s.diff(Ltrace, u, 2)
    kinetic_scalar = Ks/12+Lrr/4-Lrt**2/(4*Ltt)
    gradient_scalar = 2*(s.diff(cs, S)**2/B-cs)
    principal_eval = s.lambdify((rho, S, u), s.Matrix([kinetic_scalar, Ks, gradient_scalar, cs/2,
                                                     s.exp(2*S), Ltt, B]), "mpmath", cse=True)
    Q1, Q2, Q3, Rhat = s.symbols("Q1 Q2 Q3 Rhat", real=True)
    Q = Q1+Q2+Q3
    Qtf2 = Q1*Q1+Q2*Q2+Q3*Q3-Q*Q/3
    # Potential reconstructed from the same nongradient trace density.
    Cpot = (htrace+s.exp((4-3*u)*xi)*rho*rho/3+3*s.exp((3*u-4)*xi))/s.exp((3*u-2)*xi)
    w = (u-1)*xi
    L = s.exp(xi+3*w+vol)*(J*(Qtf2+Rhat)/2-Q*Q/3-Cpot)+3*s.exp(-xi+3*w+vol)
    Lvars = (Q1, Q2, Q3, Rhat, xi, u, vol)
    Ldata = s.Matrix(list(s.hessian(L, Lvars))+[s.diff(L, x) for x in Lvars])
    Levaluate = s.lambdify(Lvars+(interface_slope,), Ldata, "mpmath", cse=True)
    return dict(variables=variables, xi=xi, u=u, rho=rho, tau=tau, S=S, optical=optical,
                H=H, h=h, K=K, c=c, J=J, alpha=alpha, Ltrace=Ltrace, Ks=Ks, cs=cs,
                Lrr=Lrr, Lrt=Lrt, Ltt=Ltt, kinetic_scalar=kinetic_scalar,
                gradient_scalar=gradient_scalar, B=B, evaluate=evaluate,
                aux_evaluate=aux_evaluate, principal_eval=principal_eval, Levaluate=Levaluate)


def at_point(point, slope=1):
    if slope != 1:
        raise ValueError("IC9 is the fixed conformal-Einstein member, slope=1")
    values = build()["evaluate"](*point)
    vol, l1, l2, l3, xi, u, z = point
    return dict(point=point, slope=mp.mpf(1), momenta=[l1, l2, l3], xi=xi, u=u,
                H=mp.matrix([[values[6*i+j] for j in range(6)] for i in range(6)]),
                C=list(values[36:44]), auxiliary_residual=list(values[44:46]), J=values[46],
                alpha=values[47], b=values[48], Hgradient=list(values[49:55]),
                auxiliary_gradient_coefficient=mp.exp(vol+u*xi-2*z),
                physical_light_speed_squared=mp.exp(2*(2-u)*xi-2*z))


def state(kind="sheared", permutation=(0, 1, 2)):
    if kind in ("isotropic", "isotropic_neighbor"):
        j = mp.mpf(1) if kind == "isotropic" else mp.mpf("1.007")
        momenta = [-mp.exp(-mp.mpf(1)/2)*j]*3
    elif kind == "sheared":
        raw = list(map(mp.mpf, ("-0.6424435072183933", "-0.622272178918671", "-0.5676134368548011")))
        momenta = [raw[i] for i in permutation]
    else:
        raise ValueError("Unknown background")
    equations = lambda xi, u: tuple(build()["aux_evaluate"](0, *momenta, xi, u))
    xi, u = mp.findroot(equations, (mp.mpf(1)/4, mp.mpf(2)/3), tol=mp.mpf("1e-65"))
    return at_point([mp.mpf(0), *momenta, xi, u, mp.mpf(0)])


def principal(bg):
    V, z = mp.exp(bg["point"][0]), bg["point"][6]
    rho, S = sum(bg["momenta"])/V, (2-bg["u"])*bg["xi"]
    A, K, gradient, tensor_gradient, light, Ltt, B = build()["principal_eval"](rho, S, bg["u"])
    return dict(A0=mp.matrix([[A/V, 0], [0, K/V]]),
                C2=V*mp.exp(-2*z)*mp.matrix([[gradient, 0], [0, tensor_gradient]]),
                scalar_speed_squared=A*gradient/light,
                tensor_speed_squared=K*tensor_gradient/light, passive_hessian=Ltt,
                tensor_kinetic_mass=V/K, scalar_kinetic_mass=V/A, B=B)


def absent_curvature_square(bg, k):
    # The IC9 action contains no Rbar² term. The computed uncorrected Schur
    # complement, not this empty correction, establishes S4=B2=0.
    return mp.matrix(2, 2)


def evolution(bg, k, step=None):
    return mechanics.evolution(bg, k, step, point_builder=at_point,
                               correction_builder=absent_curvature_square)


def lagrangian_bridge(bg, k):
    return mechanics.lagrangian_bridge(bg, k, L_evaluate=build()["Levaluate"],
                                       correction_builder=absent_curvature_square)


@lru_cache(None)
def symbolic_identities():
    data = build()
    xi, u, S, rho = (data[x] for x in ("xi", "u", "S", "rho"))
    # True fixed-S differentiation includes the xi/(2-u) coefficient's jet.
    Dt = lambda f: s.diff(f, u)+xi/(2-u)*s.diff(f, xi)
    w, Ktrace, Ktf2, Rbar, m = s.symbols("w Ktrace Ktf2 Rbar m", real=True)
    J = s.exp(-2*w-s.Rational(1, 6))
    transformed = m*s.exp(4*w)*(J*s.exp(-2*w)*(Ktf2+Rbar)/2-s.exp(-2*w)*Ktrace**2/3)
    effective_m = m*s.exp(-s.Rational(1, 6))
    conformal = effective_m*(Ktf2+Rbar)/2-m*s.exp(2*w)*Ktrace**2/3
    p, q, pt, qt, j = s.symbols("p q pt qt j", nonzero=True)
    phase = 2*pt*qt+2*p*q/3-2*pt**2/(m*j)+p*p/(3*m)
    stationary = {p: -m*q, pt: m*j*qt/2}
    return {
        "optical_scalar_is_physical_light_ratio": s.expand(data["optical"]-(xi-(u-1)*xi)),
        "K_passive_derivative": s.simplify(Dt(data["K"])),
        "c_passive_derivative": s.simplify(Dt(data["c"])),
        "K_trace_derivative": s.diff(data["K"], rho),
        "c_trace_derivative": s.diff(data["c"], rho),
        "tensor_light_ratio": s.powsimp(data["K"]*data["c"]/(2*s.exp(2*data["optical"])), combine="exp")-1,
        "passive_trace_only_density": s.simplify(Dt(data["h"])-Dt(data["h"]-data["K"]*data["tau"])),
        "conformal_Einstein_plus_trace_term": s.simplify(transformed-conformal),
        "trace_momentum_EL": s.simplify(s.diff(phase, p).subs(stationary)),
        "tensor_momentum_EL": s.simplify(s.diff(phase, pt).subs(stationary)),
        "exact_compact_Legendre": s.simplify(phase.subs(stationary)-m*j*qt**2/2+m*q*q/3),
        "coordinate_inverse": s.simplify((S+2*w)/(S+w)-1-w/(S+w)),
    }


@lru_cache(None)
def witness_reduction():
    """Exact k!=0 scalar reduction, including the expanding background's jets.

    m=h0=V(reference)=1. x=e^(2/3) k_comoving^2/barA^2 and
    p_zeta=V exp(-1/2) P; P is NOT a canonical momentum. The k->0
    limit of this gauge reduction is not the independent homogeneous sector.
    """
    data = build()
    vol, l1, l2, l3, xi, u = data["variables"]
    f = s.exp(-s.Rational(1, 2))
    witness = {vol: 0, l1: -f, l2: -f, l3: -f,
               xi: s.Rational(1, 4), u: s.Rational(2, 3)}
    # Linear momentum constraint and spatial gauge, in (zeta,P,dxi,du).
    transform = s.zeros(6, 4)
    transform[0, 0], transform[1, 1], transform[2, 1] = 2, f/4, f/4
    transform[3, 0], transform[4, 2], transform[5, 3] = -2*f, 1, 1
    raw = transform.T*s.hessian(data["H"], data["variables"]).subs(witness, simultaneous=True)*transform/f
    x, T, alpha, ell = s.symbols("x T alpha ell", positive=True)

    def clean(value):
        value = s.expand_log(value, force=True).subs(s.log(5), 2*s.log(3)-ell)
        return s.factor(s.simplify(value).subs(ell, 54/(5*(T+s.Rational(27, 16)))))

    raw = raw.applyfunc(clean)
    optical_gradient = s.Matrix([s.diff(data["optical"], q).subs(witness) for q in (xi, u)])
    spatial = s.zeros(4)
    spatial[0, 0] = -2
    for j in range(2):
        spatial[0, 2+j] = spatial[2+j, 0] = -2*optical_gradient[j]
    spatial[2:4, 2:4] = -2*alpha*optical_gradient*optical_gradient.T
    total = raw+x*spatial
    reduced = (total[:2, :2]-total[:2, 2:4]*total[2:4, 2:4].inv()*total[2:4, :2]).applyfunc(s.factor)
    a, b, c = reduced[1, 1], reduced[0, 1], reduced[0, 0]
    # Hamilton's equations: A=a/(V f), B=b, C=V f c;
    # Vdot=3V, xdot=-2x, zeta_ddot=D*zeta_dot+E*zeta.
    D = s.factor(-3-2*x*s.diff(a, x)/a)
    E = s.factor(-2*x*s.diff(b, x)+(3+2*x*s.diff(a, x)/a)*b-a*c+b*b)
    return dict(x=x, T=T, alpha=alpha, raw=raw, spatial=spatial,
                reduced=reduced, a=a, b=b, c=c, D=D, E=E)


@lru_cache(None)
def potential_repair():
    """Test one potential-only repair that makes the scalar kinetic local.

    Add a quadratic auxiliary potential with zero value/first jet at the
    witness, replacing its negative auxiliary Hessian by -mass. This is a
    different trial action; none of IC9's measured speeds are transferred.
    """
    data = witness_reduction()
    x, alpha = data["x"], data["alpha"]
    raw = data["raw"].copy()
    mass = s.Matrix([[24, -6], [-6, s.Rational(27, 16)]])
    raw[2:4, 2:4] = -mass
    total = raw+x*data["spatial"]
    reduced = (total[:2, :2]-total[:2, 2:4]*total[2:4, 2:4].inv()*total[2:4, :2]).applyfunc(s.factor)
    a, b, c = reduced[1, 1], reduced[0, 1], reduced[0, 0]
    E = s.factor(-2*x*s.diff(b, x)+(3+2*x*s.diff(a, x)/a)*b-a*c+b*b)
    optical = s.Matrix([s.Rational(4, 3), -s.Rational(1, 4)])
    v = raw[2:4, 1]
    d = (optical.T*(-mass).inv()*optical)[0]
    expected = 2*a*x*(1+2*d*(1-alpha)*x)/(1-2*alpha*d*x)
    numerator, denominator = s.fraction(E)
    # The analytic pole is at negative x; solve() would discard it because
    # physical x was declared positive. Retain the formal polynomial root.
    if s.degree(denominator, x) != 1:
        raise ValueError("Expected a linear denominator for this trial")
    pole = -denominator.subs(x, 0)/s.diff(denominator, x)
    residue = s.factor(numerator.subs(x, pole)/s.diff(denominator, x).subs(x, pole))
    return dict(x=x, alpha=alpha, mass=mass, a=a, E=E, d=d,
                orthogonality=s.factor((v.T*(-mass).inv()*optical)[0]),
                locality_identity=s.factor(E-expected), uncancelled_pole_residue=residue)


@lru_cache(None)
def clock_response():
    """Physical-clock scalar on the constant-S witness, k!=0 only.

    The bracket is V exp(-1/2) times {delta S, delta S_dot}_reduced.
    A nonpolynomial response is flagged, not silently promoted to a full
    spacetime/retarded-response no-go theorem.
    """
    data = witness_reduction()
    x = data["x"]
    total = data["raw"]+x*data["spatial"]
    solution = (-total[2:4, 2:4].inv()*total[2:4, :2]).applyfunc(s.factor)
    optical = s.Matrix([[s.Rational(4, 3), -s.Rational(1, 4)]])
    response = (optical*solution).applyfunc(s.factor)
    z, p = response
    zdot = -2*x*s.diff(z, x)+z*data["b"]-p*data["c"]
    pdot = -2*x*s.diff(p, x)+z*data["a"]-p*(data["b"]+3)
    bracket = s.factor(z*pdot-p*zdot)
    return dict(x=x, response=response, bracket=bracket,
                constraint_residual=(total[2:4, 2:4]*solution+total[2:4, :2]).applyfunc(s.factor))


def report():
    mp.mp.dps = 80
    rows = []
    for kind in ("isotropic", "isotropic_neighbor", "sheared"):
        permutations = ((0, 1, 2), (1, 2, 0), (2, 0, 1)) if kind == "sheared" else ((0, 1, 2),)
        for permutation in permutations:
            bg = state(kind, permutation)
            high = geometry.asymptotic_conditions(bg)
            exact = principal(bg)
            rows.append(dict(kind=kind, permutation=permutation, xi=mp.nstr(bg["xi"], 20), u=mp.nstr(bg["u"], 20),
                             J=mp.nstr(bg["J"], 20), auxiliary_residual=mp.nstr(mp.norm(mp.matrix(bg["auxiliary_residual"])), 8),
                             B2_residual=mp.nstr(mp.norm(high["B2"]), 8), S4_residual=mp.nstr(mp.norm(high["S4"]), 8),
                             scalar_speed_squared=mp.nstr(exact["scalar_speed_squared"], 24),
                             tensor_speed_squared=mp.nstr(exact["tensor_speed_squared"], 24),
                             scalar_mass=mp.nstr(exact["scalar_kinetic_mass"], 24),
                             passive_hessian=mp.nstr(exact["passive_hessian"], 24)))
    finite = witness_reduction()
    return dict(base=BASE, candidate="IC9", full_theory="OPEN",
                exact_checks={k: s.simplify(v) == 0 for k, v in symbolic_identities().items()},
                homogeneous_principal_results=rows,
                finite_wave_equation={key: str(finite[key]) for key in ("a", "b", "c", "D", "E")},
                finite_wave_status="Rational k!=0 equation; UV health is not a physical-locality certificate. IR growing band requires interpretation.",
                potential_only_trial={key: str(potential_repair()[key]) for key in ("a", "E", "uncancelled_pole_residue")},
                clock_response_bracket=str(clock_response()["bracket"]),
                nonclaims=["No full nonlinear causal evolution", "No full Dirac/physical DOF certification",
                           "No all-wavelength physical locality", "No transition, zero-field, PPN or galactic matching certificate",
                           "No empirical or universal novelty claim"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-closure", action="store_true")
    args = parser.parse_args()
    result = report()
    print(json.dumps(result, indent=2))
    if not all(result["exact_checks"].values()):
        return 1
    return 2 if args.require_full_closure else 0


if __name__ == "__main__":
    raise SystemExit(main())
