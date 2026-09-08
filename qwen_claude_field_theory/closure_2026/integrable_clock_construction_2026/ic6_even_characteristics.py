#!/usr/bin/env python3
"""Bounded instantaneous IC6 even canonical pencil; evolution scope explicit."""
from functools import lru_cache
import argparse
import hashlib
import json
from pathlib import Path
import time
import platform

import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent
BASE = "0b75e72bf5797e451beb258847ade528cd9c4551"
INPUTS = {
    "TENSOR_BALANCE.md": "9f08824e080a9989c5773cc0d85e53b573b7d69e2e2236d780b6ddf3051ce81c",
    "IC5_ACTION.md": "3a466a7e4d29431bddb9c50a5aff0394c7188f434d562a36cf4c548615396987",
    "IC4_ACTION.md": "cb37292e21e0b1fbeef59a20f7800cb3d32c0cd20a46d36fd286cc3dd0f467a8",
}


@lru_cache(None)
def build():
    v, l1, l2, l3, xi, u = variables = s.symbols("volume_log lambda1 lambda2 lambda3 xi u", real=True)
    zscale = s.Symbol("log_B3", real=True)
    ell = s.log(s.Rational(9, 5))
    T = -s.Rational(27, 16)+54/(5*ell)
    alpha = s.Rational(81, 8)/T**2
    b = -T/9-s.Rational(3, 8)
    a_star = 3-81/(4*T)
    pR = s.Rational(8, 3)+4*a_star/3
    qR = -1-3*pR/8
    F = 3*(pR*(xi-s.Rational(1, 4))+qR*(u-s.Rational(2, 3)))/(16*ell**2)
    U = lambda c: (1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2
    a02 = 27*s.exp(-s.Rational(1, 2))/(8*ell**2)
    Lambda = 6*s.exp(-s.Rational(1, 2))-a02*U(s.Rational(4, 9))
    trace = l1+l2+l3
    tf2 = l1*l1+l2*l2+l3*l3-trace*trace/3
    w = (u-1)*xi
    J = 1+s.exp(-6*w-2*v)*trace*trace*F/a02
    H = (2*s.exp((4-3*u)*xi-v)*(tf2/J-trace*trace/6)
         +s.exp(v+(3*u-2)*xi)*(Lambda+a02*U(u*u))-3*s.exp(v+(3*u-4)*xi))
    Hessian = s.hessian(H, variables)
    C = s.exp(v+u*xi-2*zscale)*J
    # Perturbations change total log V by 2*zeta+rho and log B3 by rho.
    Cderivatives = s.Matrix([C, 2*s.diff(C, v), s.diff(C, v)-2*C]
                            +[s.diff(C, z) for z in (l1, l2, l3, xi, u)])
    aux = s.Matrix([s.diff(H, z) for z in (xi, u)])
    data = s.Matrix(list(Hessian)+list(Cderivatives)+list(aux)+[J, alpha, b, F]
                    +[s.diff(H, variable) for variable in variables])
    evaluate = s.lambdify(variables+(zscale,), data, modules="mpmath", cse=True)
    aux_evaluate = s.lambdify(variables, aux, modules="mpmath", cse=True)
    Q1, Q2, Q3, Rhat = s.symbols("Q1 Q2 Q3 Rhat", real=True)
    qtrace = Q1+Q2+Q3
    Y = Rhat+Q1*Q1+Q2*Q2+Q3*Q3-qtrace*qtrace/3
    K = 1+3*F*Y/(2*a02)
    L = (s.exp(xi+3*w+v)*(Y/2-qtrace*qtrace/(3*K)-Lambda-a02*U(u*u))
         +3*s.exp(-xi+3*w+v))
    Lvariables = (Q1, Q2, Q3, Rhat, xi, u, v)
    Ldata = s.Matrix(list(s.hessian(L, Lvariables))+[s.diff(L, z) for z in Lvariables])
    Levaluate = s.lambdify(Lvariables, Ldata, modules="mpmath", cse=True)
    return dict(variables=variables, H=H, Hessian=Hessian, aux=aux,
                evaluate=evaluate, aux_evaluate=aux_evaluate, J=J, F=F,
                Levaluate=Levaluate)


def state(kind="sheared"):
    if kind == "isotropic":
        momenta = [-mp.exp(-mp.mpf(1)/2)]*3
        xi, u = mp.mpf(1)/4, mp.mpf(2)/3
    else:
        if kind == "isotropic_neighbor":
            momenta = [-mp.exp(-mp.mpf(1)/2)*mp.mpf("1.007")]*3
        else:
            momenta = list(map(mp.mpf, ("-0.6424435072183933", "-0.622272178918671", "-0.5676134368548011")))
        qfun = lambda n, a: tuple(build()["aux_evaluate"](0, *momenta, n, a))
        xi, u = mp.findroot(qfun, (mp.mpf("0.24275"), mp.mpf("0.66359")), tol=mp.mpf("1e-65"))
    return at_point([mp.mpf(0), *momenta, xi, u, mp.mpf(0)])


def at_point(point):
    v, l1, l2, l3, xi, u, zscale = point
    momenta = [l1, l2, l3]
    values = build()["evaluate"](*point)
    H = mp.matrix(6, 6)
    for i in range(6):
        for j in range(6):
            H[i, j] = values[6*i+j]
    C = list(values[36:44])
    return dict(point=point, momenta=momenta, xi=xi, u=u, H=H, C=C,
                auxiliary_residual=list(values[44:46]),
                J=values[46], alpha=values[47], b=values[48], F=values[49],
                Hgradient=list(values[50:56]),
                auxiliary_gradient_coefficient=mp.exp(v+u*xi-2*zscale),
                physical_light_speed_squared=mp.exp(2*(2-u)*xi-2*zscale))


def pencil(background, k, eigenvalues=True):
    """Eliminate actual linear shift constraint and actual two auxiliaries.

    Columns are (zeta,gamma,p_zeta,p_gamma,n,v). Rows of the source Hessian
    are (log V,lambda1,lambda2,lambda3,xi,u). Gauge rho=0 is used only after
    varying the shift: delta lambda3=(lambda10+lambda20)zeta
    +(lambda10-lambda20)gamma/2. The canonical symplectic pair is exact.
    """
    l1, l2, l3 = background["momenta"]
    transform = mp.matrix(6, 6)
    transform[0, 0] = 2
    transform[1, 2], transform[1, 3] = mp.mpf(1)/4, mp.mpf(1)/2
    transform[2, 2], transform[2, 3] = mp.mpf(1)/4, -mp.mpf(1)/2
    transform[3, 0], transform[3, 1] = l1+l2, (l1-l2)/2
    transform[4, 4], transform[5, 5] = 1, 1
    nongradient = transform.T*background["H"]*transform
    C0, Cz, Cr, Cl1, Cl2, Cl3, Cxi, Cu = background["C"]
    deltaC = mp.matrix([Cz+Cl3*(l1+l2), Cl3*(l1-l2)/2,
                       (Cl1+Cl2)/4, (Cl1-Cl2)/2, Cxi, Cu])
    gradient = mp.matrix(6, 6)
    gradient[0, 0] = 6*C0
    gradient[1, 1] = C0/2
    for i in range(6):
        gradient[0, i] -= 2*deltaC[i]
        gradient[i, 0] -= 2*deltaC[i]
    aux_direction = mp.matrix([0, 0, 0, 0, 1, background["b"]])
    gradient -= 2*background["auxiliary_gradient_coefficient"]*background["alpha"]*(aux_direction*aux_direction.T)
    total = nongradient+k*k*gradient
    physical = total[:4, :4]
    mixed = total[:4, 4:6]
    auxiliary = total[4:6, 4:6]
    auxiliary_response = -auxiliary**-1*mixed.T
    reduced = physical+mixed*auxiliary_response
    symplectic = mp.matrix([[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]])
    generator = symplectic*reduced
    eigenvalues = mp.eig(generator, left=False, right=False) if eigenvalues else []
    speed_squares = [-ev*ev/(k*k*background["physical_light_speed_squared"]) for ev in eigenvalues]
    return dict(total=total, nongradient=nongradient, gradient=gradient,
                reduced=reduced, auxiliary=auxiliary,
                auxiliary_response=auxiliary_response,
                auxiliary_EL_residual=auxiliary*auxiliary_response+mixed.T,
                generator=generator, eigenvalues=eigenvalues, speed_squares=speed_squares)


def homogeneous_tangent(background):
    gradient = background["Hgradient"]
    vdot = sum(gradient[1:4])/2
    lambdadot = -gradient[0]/2
    canonical = mp.matrix([vdot, lambdadot, lambdadot, lambdadot])
    qdot = -(background["H"][4:6, 4:6]**-1)*background["H"][4:6, :4]*canonical
    return [vdot, lambdadot, lambdadot, lambdadot, qdot[0], qdot[1], gradient[3]/2]


def compact_lagrangian_bridge(background, k):
    """Independent variation of compact L, including lapse/u/shift response.

    Real cosine metric/scalar modes and sine shift mode are twice averaged.
    B below denotes the cosine amplitude of partial_z beta; the beta times
    perturbation-gradient terms are retained to obtain the actual constraint.
    """
    xi, u = background["xi"], background["u"]
    volume, zscale = background["point"][0], background["point"][6]
    rates = [value/2 for value in background["Hgradient"][1:4]]
    lapse_inverse = mp.exp(-xi)
    spatial_factor = mp.exp(-2*(u-1)*xi-2*zscale)
    arguments = [rate*lapse_inverse for rate in rates]+[0, xi, u, volume]
    data = build()["Levaluate"](*arguments)
    Lhess = mp.matrix(7, 7)
    for i in range(7):
        for j in range(7):
            Lhess[i, j] = data[7*i+j]
    Lgrad = list(data[49:56])
    # Perturbation order: zeta,gamma,rho,zeta_t,gamma_t,rho_t,n,v,B.
    linear = mp.matrix(7, 9)
    for i in (0, 1):
        linear[i, 3] = lapse_inverse
        linear[i, 4] = lapse_inverse*(mp.mpf(1)/2 if i == 0 else -mp.mpf(1)/2)
    linear[2, 5], linear[2, 8] = lapse_inverse, -lapse_inverse
    for i in range(3):
        linear[i, 6] = -rates[i]*lapse_inverse
    linear[3, 0] = 4*k*k*spatial_factor
    linear[4, 6], linear[5, 7] = 1, 1
    linear[6, 0], linear[6, 2] = 2, 1
    matrix = linear.T*Lhess*linear

    def product(i, j, coefficient):
        matrix[i, j] += coefficient
        matrix[j, i] += coefficient

    for i in range(3):
        coefficient = Lgrad[i]*lapse_inverse
        if i in (0, 1):
            sign = mp.mpf(1)/2 if i == 0 else -mp.mpf(1)/2
            product(8, 0, coefficient)
            product(8, 1, coefficient*sign)
            product(6, 3, -coefficient)
            product(6, 4, -coefficient*sign)
        else:
            product(8, 2, coefficient)
            product(6, 5, -coefficient)
            product(6, 8, coefficient)
        product(6, 6, coefficient*rates[i]/2)
    curvature = Lgrad[3]*spatial_factor*k*k
    product(0, 0, -6*curvature)
    product(1, 1, -curvature/2)
    product(0, 2, -4*curvature)
    product(0, 6, -8*(u-1)*curvature)
    product(0, 7, -8*xi*curvature)
    gradient_direction = mp.matrix([0, 0, 0, 0, 0, 0, 1, background["b"], 0])
    matrix += 2*background["auxiliary_gradient_coefficient"]*background["alpha"]*k*k*(gradient_direction*gradient_direction.T)
    # The shift is still varied below, after rho=rho_t=0 as spatial gauge.
    keep = (0, 1, 3, 4, 6, 7, 8)
    gauged = mp.matrix([[matrix[i, j] for j in keep] for i in keep])
    response = -(gauged[4:7, 4:7]**-1)*gauged[4:7, :4]
    reduced = gauged[:4, :4]+gauged[:4, 4:7]*response
    Hred = pencil(background, k, eigenvalues=False)["reduced"]
    C, B, A = Hred[:2, :2], Hred[:2, 2:4], Hred[2:4, 2:4]
    M = A**-1
    expected = mp.matrix(4, 4)
    expected[:2, :2] = B*M*B.T-C
    expected[:2, 2:4] = -B*M
    expected[2:4, :2] = -M*B.T
    expected[2:4, 2:4] = M
    return dict(reduced=reduced, expected=expected, residual=reduced-expected,
                auxiliary_response=response,
                auxiliary_EL_residual=gauged[4:7, 4:7]*response+gauged[4:7, :4])


def evolving_pencil(background, k, step=mp.mpf("1e-30")):
    """Exact coefficient formula, numerically differentiated along actual flow.

    The time derivative is of the constrained canonical Hamiltonian, including
    the actual auxiliary multipliers and background B3. The small complex-step
    derivative is checked against another step in tests; it is not interval
    arithmetic. Freezing the original canonical generator is a mutation.
    """
    reduced = pencil(background, k, eigenvalues=False)["reduced"]
    tangent = homogeneous_tangent(background)
    shifted = [x+1j*step*dx for x, dx in zip(background["point"], tangent)]
    shifted_reduced = pencil(at_point(shifted), k, eigenvalues=False)["reduced"]
    derivative = mp.matrix(4, 4)
    for i in range(4):
        for j in range(4):
            derivative[i, j] = mp.im(shifted_reduced[i, j])/step
    C, B, A = reduced[:2, :2], reduced[:2, 2:4], reduced[2:4, 2:4]
    Adot, Bdot = derivative[2:4, 2:4], derivative[:2, 2:4]
    Ainv = A**-1
    D = B.T+Adot*Ainv-A*B*Ainv
    E = Bdot.T-Adot*Ainv*B.T-A*C+A*B*Ainv*B.T
    companion = mp.matrix(4, 4)
    companion[:2, 2:4] = mp.eye(2)
    companion[2:4, :2], companion[2:4, 2:4] = E, D
    poles = mp.eig(companion, left=False, right=False)
    return dict(D=D, E=E, Adot=Adot, Bdot=Bdot, derivative=derivative,
                tangent=tangent, poles=poles,
                speed_squares=[-pole*pole/(k*k*background["physical_light_speed_squared"]) for pole in poles])


def asymptotic_conditions(background):
    """Exact matrix formula for k^4 stiffness and omega*k^2 integrability.

    The formula uses the two-by-two rank-one auxiliary-gradient inverse,
    before numerical evaluation. A0,B2,C4 denote leading blocks in
    Hred=[[C,B],[B.T,A]], with A~A0, B~k²B2, C~k4 C4.
    """
    raw = pencil(background, mp.mpf(1), eigenvalues=False)
    H0, H1 = raw["nongradient"], raw["gradient"]
    Q0 = H0[4:6, 4:6]
    X0, X1 = H0[:4, 4:6], H1[:4, 4:6]
    direction = mp.matrix([1, background["b"]])
    sigma = -2*background["auxiliary_gradient_coefficient"]*background["alpha"]
    R = Q0**-1
    d = (direction.T*R*direction)[0]
    P = R*direction*direction.T*R/d
    Rinf = R-P
    R1, R2 = P/(sigma*d), -P/(sigma*d)**2
    T2 = -X1*Rinf*X1.T
    T1 = H1[:4, :4]-X1*Rinf*X0.T-X0*Rinf*X1.T-X1*R1*X1.T
    T0 = H0[:4, :4]-X0*Rinf*X0.T-X1*R1*X0.T-X0*R1*X1.T-X1*R2*X1.T
    A0, B2, C4 = T0[2:4, 2:4], T1[:2, 2:4], T2[:2, :2]
    M = A0**-1
    N2 = M*B2.T
    S4 = C4-B2*M*B2.T
    G2 = -N2+N2.T
    g = G2[0, 1]
    determinant_mass = mp.det(M)
    # In this principal-axis family S4 is rank one; this is checked in tests.
    stiffness_trace = M[1, 1]*S4[0, 0]+M[0, 0]*S4[1, 1]-2*M[0, 1]*S4[0, 1]
    z_squared = -(stiffness_trace+g*g)/determinant_mass
    rr_coefficient = -S4[0, 0]*mp.exp(4*background["point"][6])/32
    rr_only_z_squared = -g*g/determinant_mass
    return dict(A0=A0, B2=B2, C4=C4, M0=M, N2=N2, S4=S4, G2=G2,
                z_squared=z_squared, Rbar_squared_density_coefficient=rr_coefficient,
                Rbar_squared_only_z_squared=rr_only_z_squared,
                auxiliary_gradient_rank_one_residual=H1[4:6, 4:6]-sigma*direction*direction.T,
                quartic_H=T2, quadratic_H=T1, constant_H=T0)


@lru_cache(None)
def exact_trace_branch():
    """Analytic sign of quartic scalar stiffness just off the isotropic witness.

    Generic Schur algebra and kinetic Hessian are derived rather than fitted.
    T is the frozen positive constant, kept symbolic for the sign proof.
    """
    T = s.Symbol("T", positive=True)
    mass = -s.Matrix([[24, -27], [-27, 2*T+s.Rational(135, 8)]])
    source = s.Matrix([-12, s.Rational(9, 2)])
    tangent = s.simplify(-mass.inv()*source)
    pR, qR = s.Rational(20, 3)-27/T, -s.Rational(7, 2)+81/(8*T)
    Jprime = s.factor((pR*tangent[0]+qR*tangent[1])/2)
    b = -T/9-s.Rational(3, 8)
    hpchi = s.simplify(-2*b-s.Rational(3, 4))
    gchi = s.factor(-2*s.exp(s.Rational(1, 6))*(-b*(s.Rational(2, 3)+pR/2)+s.Rational(1, 4)+qR/2))
    hpp_prime = -s.exp(s.Rational(1, 2))*Jprime/6
    gp_prime = 2*s.exp(s.Rational(2, 3))*Jprime/3

    # Full kinetic density at fixed q: J=1+D*pi^2, no frozen-J differentiation.
    l1, l2, l3, D, E, trace = s.symbols("lambda1 lambda2 lambda3 D E trace", real=True)
    pi = l1+l2+l3
    kinetic = 2*E*((l1*l1+l2*l2+l3*l3-pi*pi/3)/(1+D*pi*pi)-pi*pi/6)
    direction = s.Matrix([s.Rational(1, 4), s.Rational(1, 4), 0])
    hpp = (direction.T*s.hessian(kinetic, (l1, l2, l3))*direction)[0]
    hpp = s.factor(hpp.subs({l1: trace/3, l2: trace/3, l3: trace/3}))
    hpp_expected = E*(1/(1+D*trace*trace)-1)/6

    # Null auxiliary chi points along (-b,1); its gradient term is absent.
    hpp0, hpx, hxx, gp, gx = s.symbols("hpp h_p_chi h_chi_chi g_p g_chi", real=True)
    A = hpp0-hpx*hpx/hxx
    B = gp-gx*hpx/hxx
    C = -gx*gx/hxx
    quartic = s.factor(C-B*B/A)
    expected = -(hpp0*gx*gx-2*hpx*gp*gx+hxx*gp*gp)/(hpp0*hxx-hpx*hpx)
    derivative = s.factor((hpp_prime*gchi*gchi-2*hpchi*gp_prime*gchi)/(hpchi*hpchi))
    closed = -s.exp(s.Rational(5, 6))*(5*T-27)*(8*T-27)*(8*T+27)/(18*T*T*(4*T-27))
    residuals = {
        "homogeneous_constraint_tangent": s.simplify(mass*tangent+source),
        "actual_kinetic_hpp": s.factor(hpp-hpp_expected),
        "scalar_quartic_Schur_formula": s.factor(quartic-expected),
        "J_trace_derivative": s.factor(Jprime+4*(5*T-27)/(3*(4*T-27))),
        "null_auxiliary_momentum_coupling": s.factor(hpchi-2*T/9),
        "null_auxiliary_curvature_source": s.factor(gchi+s.exp(s.Rational(1, 6))*(8*T-27)/9),
        "quartic_trace_derivative": s.factor(derivative-closed),
    }
    return dict(T=T, tangent=tangent, Jprime=Jprime, hpp=hpp,
                hpp_prime=hpp_prime, gp_prime=gp_prime, hpchi=hpchi, gchi=gchi,
                quartic_formula=quartic, S4_prime=closed, residuals=residuals,
                sign_domain="T>27/4 => S4_prime<0; actual frozen T satisfies this domain")


def stringify(value):
    if isinstance(value, dict):
        return {str(key): stringify(item) for key, item in value.items()}
    if isinstance(value, mp.matrix):
        return stringify(value.tolist())
    if isinstance(value, (list, tuple)):
        return [stringify(item) for item in value]
    if isinstance(value, (mp.mpf, mp.mpc)):
        return mp.nstr(value, 30)
    return value


def run():
    mp.mp.dps = 80
    started = time.monotonic()
    hashes = {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in INPUTS}
    if hashes != INPUTS:
        raise RuntimeError("Frozen IC6 action inputs changed")
    output = {}
    for kind in ("isotropic", "isotropic_neighbor", "sheared"):
        initial = state(kind)
        entries = []
        for k in map(mp.mpf, ("10", "100", "1000", "10000")):
            result = pencil(initial, k)
            evolving = evolving_pencil(initial, k)
            bridge = compact_lagrangian_bridge(initial, k)
            entries.append(dict(k=k, speed_squares=result["speed_squares"],
                                evolving_speed_squares=evolving["speed_squares"],
                                auxiliary_EL_max=mp.norm(result["auxiliary_EL_residual"], p=mp.inf),
                                compact_L_bridge_relative_residual=mp.norm(bridge["residual"], mp.inf)/max(1, mp.norm(bridge["expected"], mp.inf)),
                                compact_auxiliary_shift_EL_max=mp.norm(bridge["auxiliary_EL_residual"], mp.inf)))
        asymptotic = asymptotic_conditions(initial)
        output[kind] = dict(xi=initial["xi"], u=initial["u"], J=initial["J"],
                            initial_momenta=initial["momenta"], tangent=homogeneous_tangent(initial),
                            auxiliary_residual=initial["auxiliary_residual"], pencil=entries,
                            asymptotic={key: asymptotic[key] for key in ("A0", "N2", "S4", "G2", "z_squared", "Rbar_squared_density_coefficient", "Rbar_squared_only_z_squared")})
    exact = exact_trace_branch()
    exact_passed = all(all(s.simplify(v) == 0 for v in (list(expr) if isinstance(expr, s.MatrixBase) else [expr])) for expr in exact["residuals"].values())
    return stringify(dict(base_commit=BASE, input_hashes=hashes,
                          own_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                          software=dict(python=platform.python_version(), sympy=s.__version__, mpmath=mp.__version__),
                          precision_decimal_digits=80, runtime_seconds=time.monotonic()-started,
                          status="Numerically verified reduced even-sector pencil on specified actual homogeneous data; IC6 completion not certified",
                          all_background_causality_proved=False,
                          replacement_action_constructed=False,
                          exact_trace_branch_checks_passed=exact_passed,
                          exact_trace_branch_S4_derivative=str(exact["S4_prime"]),
                          domain="eta=1, J_T>0, K6!=0, k_z!=0; m=h0=1, kappa=6; diagonal Bianchi I with the stated real momenta",
                          data=output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-all-background-causality", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(), indent=2))
    raise SystemExit(2 if args.require_all_background_causality else 0)
