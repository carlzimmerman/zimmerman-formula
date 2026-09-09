#!/usr/bin/env python3
"""IC8 phase-action family: passive-direction tensor kinetic decoupling.

Same fixed MOND primitive, clock and homogeneous trace potential as IC6.
The shear kinetic coefficient is redesigned, not borrowed from IC7.
Numerics use m=h0=1, kappa=6. A quartic correction is derived anew.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as s
import ic6_even_characteristics as old
from ic7_curvature_square import determinant_cutoff

BASE = "0aa6e0cef9f8b9f0e6fc7129bedfa12ef055914e"


@lru_cache(None)
def build():
    vol, l1, l2, l3, xi, u = variables = s.symbols("logV lambda1 lambda2 lambda3 xi u", real=True)
    z, slope = s.symbols("logB3 slope", real=True)
    rho, tau = s.symbols("rho tau", real=True)
    ell = s.log(s.Rational(9, 5))
    T = -s.Rational(27, 16)+54/(5*ell)
    b, alpha = -T/9-s.Rational(3, 8), 81/(8*T*T)
    U = lambda c: (1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2
    a02 = 27*s.exp(-s.Rational(1, 2))/(8*ell*ell)
    Lambda = 6*s.exp(-s.Rational(1, 2))-a02*U(s.Rational(4, 9))
    w, E = (u-1)*xi, s.exp((4-3*u)*xi)
    passive_invariant = xi+b*u-s.Rational(1, 4)-2*b/3
    J = s.exp((4-3*u)*xi-s.Rational(1, 2)-slope*passive_invariant)
    K = 2*s.exp(s.Rational(1, 2)+slope*passive_invariant)
    htrace = -E*rho*rho/3+s.exp((3*u-2)*xi)*(Lambda+a02*U(u*u))-3*s.exp((3*u-4)*xi)
    h = K*tau+htrace
    trace = l1+l2+l3
    tf2 = l1*l1+l2*l2+l3*l3-trace*trace/3
    H = s.exp(vol)*h.subs({rho: trace*s.exp(-vol), tau: tf2*s.exp(-2*vol)}, simultaneous=True)
    c = s.exp(u*xi)*J
    C = s.exp(vol-2*z)*c
    Cderivatives = s.Matrix([C, 2*s.diff(C, vol), s.diff(C, vol)-2*C]
                            +[s.diff(C, x) for x in (l1, l2, l3, xi, u)])
    aux = s.Matrix([s.diff(H, x) for x in (xi, u)])
    Hgrad = s.Matrix([s.diff(H, x) for x in variables])
    data = s.Matrix(list(s.hessian(H, variables))+list(Cderivatives)+list(aux)+[J, alpha, b]+list(Hgrad))
    evaluate = s.lambdify(variables+(z, slope), data, "mpmath", cse=True)
    aux_evaluate = s.lambdify(variables+(slope,), aux, "mpmath", cse=True)
    Dt = lambda f: s.diff(f, u)-b*s.diff(f, xi)
    M = s.Matrix([[s.diff(htrace, rho, 2)/4+K/12, Dt(s.diff(htrace, rho))/2],
                  [Dt(s.diff(htrace, rho))/2, Dt(Dt(htrace))]])
    cv = s.Matrix([s.diff(c, rho)/2, Dt(c)])
    coefficient = s.lambdify((rho, xi, u, slope), s.Matrix(list(M)+list(cv)), "mpmath", cse=True)
    Q1, Q2, Q3, Rhat = s.symbols("Q1 Q2 Q3 Rhat", real=True)
    Q = Q1+Q2+Q3
    Qtf2 = Q1*Q1+Q2*Q2+Q3*Q3-Q*Q/3
    L = (s.exp(xi+3*w+vol)*(J*(Qtf2+Rhat)/2-Q*Q/3-Lambda-a02*U(u*u))
         +3*s.exp(-xi+3*w+vol))
    Lvars = (Q1, Q2, Q3, Rhat, xi, u, vol)
    Ldata = s.Matrix(list(s.hessian(L, Lvars))+[s.diff(L, x) for x in Lvars])
    Levaluate = s.lambdify(Lvars+(slope,), Ldata, "mpmath", cse=True)
    return dict(variables=variables, rho=rho, tau=tau, xi=xi, u=u, slope=slope,
                H=H, h=h, htrace=htrace, K=K, J=J, c=c, M=M, cv=cv,
                b=b, T=T, evaluate=evaluate, aux_evaluate=aux_evaluate,
                coefficient=coefficient, Levaluate=Levaluate)


def at_point(point, slope):
    values = build()["evaluate"](*point, slope)
    H = mp.matrix([[values[6*i+j] for j in range(6)] for i in range(6)])
    vol, l1, l2, l3, xi, u, z = point
    return dict(point=point, slope=slope, momenta=[l1, l2, l3], xi=xi, u=u, H=H,
                C=list(values[36:44]), auxiliary_residual=list(values[44:46]),
                J=values[46], alpha=values[47], b=values[48], Hgradient=list(values[49:55]),
                auxiliary_gradient_coefficient=mp.exp(vol+u*xi-2*z),
                physical_light_speed_squared=mp.exp(2*(2-u)*xi-2*z))


def state(kind="sheared", slope=None, permutation=(0, 1, 2)):
    slope = -mp.mpf(1)/4 if slope is None else mp.mpf(slope)
    if kind in ("isotropic", "isotropic_neighbor"):
        j = mp.mpf(1) if kind == "isotropic" else mp.mpf("1.007")
        momenta = [-mp.exp(-mp.mpf(1)/2)*j]*3
    elif kind == "sheared":
        raw = list(map(mp.mpf, ("-0.6424435072183933", "-0.622272178918671", "-0.5676134368548011")))
        momenta = [raw[i] for i in permutation]
    else:
        raise ValueError("Unknown state family")
    equations = lambda xi, u: tuple(build()["aux_evaluate"](0, *momenta, xi, u, slope))
    xi, u = mp.findroot(equations, (mp.mpf(1)/4, mp.mpf(2)/3), tol=mp.mpf("1e-65"))
    return at_point([mp.mpf(0), *momenta, xi, u, mp.mpf(0)], slope)


def quartic_coefficient(bg):
    rho = sum(bg["momenta"])*mp.exp(-bg["point"][0])
    values = build()["coefficient"](rho, bg["xi"], bg["u"], bg["slope"])
    M = mp.matrix([[values[0], values[1]], [values[2], values[3]]])
    v = mp.matrix(list(values[4:6]))
    reference = build()["coefficient"](-3*mp.exp(-mp.mpf(1)/2), mp.mpf(1)/4, mp.mpf(2)/3, bg["slope"])
    Mstar = mp.matrix([[reference[0], reference[1]], [reference[2], reference[3]]])
    theta = determinant_cutoff(mp.det(M)/mp.det(Mstar))
    coefficient = theta*(v.T*(M**-1)*v)[0]/8 if theta else mp.mpf(0)
    return dict(M=M, v=v, coefficient=coefficient, theta=theta)


def correction(bg, k):
    result = mp.matrix(2, 2)
    result[0, 0] = 32*mp.exp(bg["point"][0]-4*bg["point"][6])*quartic_coefficient(bg)["coefficient"]*k**4
    return result


def reduced(bg, k):
    H = old.pencil(bg, k, eigenvalues=False)["reduced"]
    H[:2, :2] += correction(bg, k)
    return H


def conditions(bg):
    result = old.asymptotic_conditions(bg)
    result["S4"] += correction(bg, mp.mpf(1))
    return result


def evolution(bg, k, step=None, point_builder=None, correction_builder=None):
    point_builder = at_point if point_builder is None else point_builder
    correction_builder = correction if correction_builder is None else correction_builder
    step = mp.mpf("1e-30") if step is None else step
    # Only the uncorrected C block changes on these flat backgrounds; Cdot
    # does not enter the exact momentum-eliminated second-order equation.
    H = old.pencil(bg, k, eigenvalues=False)["reduced"]
    tangent = old.homogeneous_tangent(bg)
    point = [x+1j*step*v for x, v in zip(bg["point"], tangent)]
    Hshift = old.pencil(point_builder(point, bg["slope"]), k, eigenvalues=False)["reduced"]
    derivative = mp.matrix([[mp.im(Hshift[i, j])/step for j in range(4)] for i in range(4)])
    C, B, A = H[:2, :2]+correction_builder(bg, k), H[:2, 2:4], H[2:4, 2:4]
    Adot, Bdot, invA = derivative[2:4, 2:4], derivative[:2, 2:4], A**-1
    D = B.T+Adot*invA-A*B*invA
    E = Bdot.T-Adot*invA*B.T-A*C+A*B*invA*B.T
    companion = mp.matrix(4, 4)
    companion[:2, 2:4] = mp.eye(2)
    companion[2:4, :2], companion[2:4, 2:4] = E, D
    poles = mp.eig(companion, left=False, right=False)
    light = bg["physical_light_speed_squared"]
    return dict(D=D, E=E, poles=poles, speed_squares=[-x*x/(k*k*light) for x in poles],
                null_factor=mp.det(-E/(k*k)-light*mp.eye(2)))


@lru_cache(None)
def symbolic_identities():
    data = build()
    xi, u, rho, b, K = (data[x] for x in ("xi", "u", "rho", "b", "K"))
    Dt = lambda f: s.diff(f, u)-b*s.diff(f, xi)
    # Generic shear principal-axis block. The tensor momentum decouples
    # from (scalar momentum, passive auxiliary) if K_rho=Dt K=0.
    a, d, f, source = s.symbols("a d f source", nonzero=True)
    mass = s.Matrix([[a, 0, d], [0, K, 0], [d, 0, f]])
    v = s.Matrix([0, 0, source])
    response = mass.inv()*v
    sub = mass.extract([0, 2], [0, 2])
    sub_source = s.Matrix([0, source])
    scalar_square = (sub_source.T*sub.inv()*sub_source)[0]
    return {
        "trace_derivative": s.diff(K, rho),
        "passive_derivative": s.simplify(Dt(K)),
        "kinetic_definition": s.powsimp(K*data["J"]/(2*s.exp((4-3*u)*xi)), combine="exp")-1,
        "odd_physical_cone": s.powsimp(K*data["c"]/(2*s.exp((4-2*u)*xi)), combine="exp")-1,
        "tensor_curvature_momentum_response": s.simplify(response[1]),
        "three_variable_quartic_equals_scalar_block": s.simplify((v.T*mass.inv()*v)[0]-scalar_square),
        "quartic_cancellation": s.simplify(-4*(v.T*mass.inv()*v)[0]+32*scalar_square/8),
        "passive_hessian_independent_of_shear": s.simplify(Dt(Dt(data["h"]))-Dt(Dt(data["htrace"]))),
    }


def lagrangian_bridge(bg, k, L_evaluate=None, correction_builder=None):
    """Vary the independently Legendre-derived compact baseline L8.

    The curvature-square term contributes minus its quadratic Hamiltonian
    term at flat R=0; no exact nonlinear trace elimination is asserted.
    """
    L_evaluate = build()["Levaluate"] if L_evaluate is None else L_evaluate
    correction_builder = correction if correction_builder is None else correction_builder
    xi, u = bg["xi"], bg["u"]
    vol, z = bg["point"][0], bg["point"][6]
    rates = [x/2 for x in bg["Hgradient"][1:4]]
    n_inv, spatial = mp.exp(-xi), mp.exp(-2*(u-1)*xi-2*z)
    vals = L_evaluate(*([v*n_inv for v in rates]+[0, xi, u, vol, bg["slope"]]))
    Hess = mp.matrix([[vals[7*i+j] for j in range(7)] for i in range(7)])
    grad = list(vals[49:56])
    # zeta,gamma,rho,zeta_dot,gamma_dot,rho_dot,delta_xi,delta_u,beta_z.
    linear = mp.matrix(7, 9)
    for i in (0, 1):
        linear[i, 3], linear[i, 4] = n_inv, n_inv*(mp.mpf(1)/2 if i == 0 else -mp.mpf(1)/2)
    linear[2, 5], linear[2, 8] = n_inv, -n_inv
    for i in range(3):
        linear[i, 6] = -rates[i]*n_inv
    linear[3, 0] = 4*k*k*spatial
    linear[4, 6], linear[5, 7], linear[6, 0], linear[6, 2] = 1, 1, 2, 1
    matrix = linear.T*Hess*linear

    def product(i, j, value):
        matrix[i, j] += value
        matrix[j, i] += value

    for i in range(3):
        value = grad[i]*n_inv
        if i in (0, 1):
            sign = mp.mpf(1)/2 if i == 0 else -mp.mpf(1)/2
            product(8, 0, value)
            product(8, 1, value*sign)
            product(6, 3, -value)
            product(6, 4, -value*sign)
        else:
            product(8, 2, value)
            product(6, 5, -value)
            product(6, 8, value)
        product(6, 6, value*rates[i]/2)
    R = grad[3]*spatial*k*k
    product(0, 0, -6*R)
    product(1, 1, -R/2)
    product(0, 2, -4*R)
    product(0, 6, -8*(u-1)*R)
    product(0, 7, -8*xi*R)
    direction = mp.matrix([0, 0, 0, 0, 0, 0, 1, bg["b"], 0])
    matrix += 2*bg["auxiliary_gradient_coefficient"]*bg["alpha"]*k*k*direction*direction.T
    keep = (0, 1, 3, 4, 6, 7, 8)
    gauged = mp.matrix([[matrix[i, j] for j in keep] for i in keep])
    L = gauged[:4, :4]-gauged[:4, 4:7]*(gauged[4:7, 4:7]**-1)*gauged[4:7, :4]
    L[:2, :2] -= correction_builder(bg, k)
    H = old.pencil(bg, k, eigenvalues=False)["reduced"]
    H[:2, :2] += correction_builder(bg, k)
    C, B, A = H[:2, :2], H[:2, 2:4], H[2:4, 2:4]
    mass = A**-1
    expected = mp.matrix(4, 4)
    expected[:2, :2], expected[:2, 2:4] = B*mass*B.T-C, -B*mass
    expected[2:4, :2], expected[2:4, 2:4] = -mass*B.T, mass
    return L-expected


def report():
    mp.mp.dps = 80
    rows = []
    for kind in ("isotropic", "isotropic_neighbor", "sheared"):
        permutations = ((0, 1, 2), (1, 2, 0), (2, 0, 1)) if kind == "sheared" else ((0, 1, 2),)
        for permutation in permutations:
            bg = state(kind, permutation=permutation)
            high = conditions(bg)
            value = evolution(bg, mp.mpf("1e5"))
            rows.append(dict(kind=kind, permutation=permutation, xi=mp.nstr(bg["xi"], 18),
                             u=mp.nstr(bg["u"], 18), J=mp.nstr(bg["J"], 18),
                             G2_residual=mp.nstr(mp.norm(high["G2"]), 6), S4_residual=mp.nstr(mp.norm(high["S4"]), 6),
                             speed_squared=[mp.nstr(x, 24) for x in value["speed_squares"]],
                             physical_null_factor=mp.nstr(value["null_factor"], 24)))
    return dict(base=BASE, candidate="IC8", status="OPEN", slope="-1/4",
                exact_checks={k: s.simplify(v) == 0 for k, v in symbolic_identities().items()},
                actual_backgrounds=rows,
                nonclaims=["Not complete relativistic MOND", "Not a general-direction characteristic theorem",
                           "No automatic transfer of IC6 scalar waves or nonlinear constraints",
                           "Remaining light cone, stability, PPN, galactic matching and full evolution must be checked"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-closure", action="store_true")
    args = parser.parse_args()
    data = report()
    print(json.dumps(data, indent=2))
    if not all(data["exact_checks"].values()):
        return 1
    return 2 if args.require_full_closure else 0


if __name__ == "__main__":
    raise SystemExit(main())
