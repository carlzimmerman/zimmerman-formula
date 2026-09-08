#!/usr/bin/env python3
"""IC6 odd tensor characteristics on diagonal anisotropic plane backgrounds.

Exact second jets of actual metric geometry and the actual phase density.
The even mixed system and arbitrary-background causality remain OPEN.
No frozen auxiliary Hessian is interpreted as a physical characteristic.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform
import time

import sympy as s

HERE = Path(__file__).resolve().parent
BASE = "0b75e72bf5797e451beb258847ade528cd9c4551"
INPUTS = {
    "TENSOR_BALANCE.md": "9f08824e080a9989c5773cc0d85e53b573b7d69e2e2236d780b6ddf3051ce81c",
    "IC5_ACTION.md": "3a466a7e4d29431bddb9c50a5aff0394c7188f434d562a36cf4c548615396987",
    "IC4_ACTION.md": "cb37292e21e0b1fbeef59a20f7800cb3d32c0cd20a46d36fd286cc3dd0f467a8",
    "tensor_balance_completion.py": "c76736fb053af6a96b54d96f9577c8600a753380fce1e7187b1ec5ee9d5d28e4",
    "nonlinear_square_completion.py": "4c9a79caa9a6d54a6a5f006440886f54b9092d68978249fb79f95a0f73229ece",
}


def clean(expr):
    if isinstance(expr, s.MatrixBase):
        return expr.applyfunc(lambda item: s.factor(s.cancel(item)))
    return s.factor(s.cancel(expr))


@lru_cache(None)
def geometry():
    """Christoffel/Ricci and extrinsic-curvature jets, with all background jets.

    x,y are Killing directions. All A_i,N,w may depend on t,z. The physical
    cross-polarization metric is D exp(epsilon*gamma*E_xy) D. Truncating the
    exponential and its inverse through epsilon**2 exactly determines the
    quadratic action; this is not a small-background-shear approximation.
    """
    eps, g, gt, gz, gzz = s.symbols("epsilon gamma gamma_t gamma_z gamma_zz", real=True)
    A = s.symbols("A1:4", positive=True)
    H = s.symbols("H1:4", real=True)  # H_i = partial_t log A_i
    L = s.symbols("L1:4", real=True)  # L_i = partial_z log A_i
    Lp = s.symbols("Lp1:4", real=True)
    N = s.Symbol("N", positive=True)
    wt, wz, wzz = s.symbols("w_t w_z w_zz", real=True)
    E = s.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    D, Di = s.diag(*A), s.diag(*(1/a for a in A))
    metric = D*(s.eye(3)+eps*g*E+eps**2*g*g*E*E/2)*D
    inverse = Di*(s.eye(3)-eps*g*E+eps**2*g*g*E*E/2)*Di

    def jet(expr):
        expanded = s.expand(expr)
        return sum(expanded.coeff(eps, i)*eps**i for i in range(3))

    def dz(expr):
        return s.expand(gz*s.diff(expr, g)+gzz*s.diff(expr, gz)
                        +wzz*s.diff(expr, wz)
                        +sum(a*l*s.diff(expr, a)+lp*s.diff(expr, l)
                             for a, l, lp in zip(A, L, Lp)))

    def derivative(expr, direction):
        return dz(expr) if direction == 2 else s.S.Zero

    connection = [[[jet(sum(inverse[i, b]*(derivative(metric[b, j], k)
                           +derivative(metric[b, k], j)-derivative(metric[j, k], b))
                           for b in range(3))/2)
                    for k in range(3)] for j in range(3)] for i in range(3)]
    ricci = s.Matrix(3, 3, lambda i, j: jet(sum(
        derivative(connection[a][i][j], a)-derivative(connection[a][i][a], j)
        +sum(connection[a][a][b]*connection[b][i][j]
             -connection[a][j][b]*connection[b][i][a] for b in range(3))
        for a in range(3))))
    curvature = clean(jet(s.trace(inverse*ricci)))
    metric_t = s.diag(*H)*metric+metric*s.diag(*H)+gt*metric.diff(g)
    qmixed = (inverse*metric_t/(2*N)-wt*s.eye(3)/N).applyfunc(jet)
    qtrace = clean(jet(s.trace(qmixed)))
    qtf2 = clean(jet(s.trace(qmixed*qmixed)-qtrace*qtrace/3))
    # det(exp(g E))=exp(g tr E)=1 exactly. Check its second jet as well.
    volume = s.prod(A)
    laplacian_w = clean(jet(dz(volume*inverse[2, 2]*wz)/volume))
    w_gradient_squared = clean(jet(inverse[2, 2]*wz*wz))
    rhat = curvature+4*laplacian_w-2*w_gradient_squared
    expected_R2 = -(gz*gz+(L[0]-L[1])**2*g*g)/(2*A[2]**2)
    expected_QTF2 = (gt*gt+(H[0]-H[1])**2*g*g)/(2*N*N)
    coefficient = lambda expr, degree: clean(s.expand(expr).coeff(eps, degree))
    residuals = {
        "inverse_second_jet": (metric*inverse-s.eye(3)).applyfunc(jet),
        "determinant_second_jet": clean(jet(metric.det())-volume**2),
        "volume_generator_trace": s.trace(E),
        "clock_laplacian_unperturbed": clean(laplacian_w-(wzz+(L[0]+L[1]-L[2])*wz)/A[2]**2),
        "clock_gradient_unperturbed": clean(w_gradient_squared-wz*wz/A[2]**2),
        "R_first_jet": coefficient(curvature, 1),
        "R_second_jet": clean(coefficient(curvature, 2)-expected_R2),
        "Q_trace": clean(qtrace-(sum(H)-3*wt)/N),
        "QTF_first_jet": coefficient(qtf2, 1),
        "QTF_second_jet": clean(coefficient(qtf2, 2)-expected_QTF2),
    }
    return dict(eps=eps, gamma=g, gamma_t=gt, gamma_z=gz, gamma_zz=gzz,
                A=A, H=H, L=L, Lp=Lp, N=N, wt=wt, wz=wz, wzz=wzz,
                metric=metric, inverse=inverse, curvature=curvature,
                R0=coefficient(curvature, 0), R1=coefficient(curvature, 1),
                R2=coefficient(curvature, 2), Q=qtrace,
                QTF0=coefficient(qtf2, 0), QTF1=coefficient(qtf2, 1),
                QTF2=coefficient(qtf2, 2), Rhat=rhat, volume=volume,
                Y0=coefficient(rhat+qtf2, 0),
                Y2=coefficient(rhat+qtf2, 2), residuals=residuals)


def odd_phase_coefficients(balance=True):
    """Actual cross momentum EL; balance=False is the IC5 mutation control."""
    m, J, N, A3 = s.symbols("m J N A3", positive=True)
    r, gt, gz = s.symbols("P_xy gamma_t gamma_z", real=True)
    # tr(P_TF**2) contains 2 P_xy**2; 2 P:Q contains 4 P_xy Q_xy.
    denom = J if balance else s.S.One
    phase = 2*r*gt/N-4*r*r/(m*denom)-m*J*gz*gz/(4*A3*A3)
    solution = s.solve(s.diff(phase, r), r)[0]
    reduced = clean(phase.subs(r, solution))
    kinetic = clean(2*N*N*s.diff(reduced, gt, 2)/m)
    gradient = clean(-2*A3*A3*s.diff(reduced, gz, 2)/m)
    return dict(m=m, J=J, r=r, N=N, A3=A3, gt=gt, gz=gz, phase=phase,
                P_solution=solution, reduced=reduced,
                EL_residual=clean(s.diff(phase, r).subs(r, solution)),
                kinetic=kinetic, gradient=gradient,
                physical_speed_squared=clean(gradient/kinetic))


@lru_cache(None)
def phase_and_mixed_hessian():
    m, a02 = s.symbols("m a0_squared", positive=True)
    p, Q, F, R = s.symbols("p Q F Rhat", real=True)
    q = s.symbols("Qtf1:6", real=True)
    momenta = s.symbols("Ptf1:6", real=True)
    J = 1+p*p*F/(m*m*a02)
    phase = (2*sum(pi*qi for pi, qi in zip(momenta, q))+2*p*Q/3
             -2*sum(pi*pi for pi in momenta)/(m*J)+p*p/(3*m)+m*J*R/2)
    solutions = {pi: m*J*qi/2 for pi, qi in zip(momenta, q)}
    after_tf = clean(phase.subs(solutions, simultaneous=True))
    Y, Y2, dq, dy = s.symbols("Y Y_second delta_Q delta_Y", real=True)
    K = 1+3*F*Y/(2*a02)
    p_solution = -m*Q/K
    after_tf_Y = m*Y/2+2*p*Q/3+p*p*K/(3*m)
    reduced = clean(after_tf_Y.subs(p, p_solution))
    fY = clean(s.diff(reduced, Y))
    J_reduced = 1+F*Q*Q/(a02*K*K)
    hessian = clean(s.hessian(reduced, (Y, Q)))
    trace_square = -m*(dq-3*F*Q*dy/(2*a02*K))**2/(3*K)
    quadratic_mixed = (s.Matrix([dy, dq]).T*hessian*s.Matrix([dy, dq]))[0]/2
    df = s.Symbol("delta_F", real=True)
    delta_K = 3*(F*dy+Y*df)/(2*a02)
    full_hessian = clean(s.hessian(reduced, (Y, Q, F)))
    full_vector = s.Matrix([dy, dq, df])
    full_quadratic = (full_vector.T*full_hessian*full_vector)[0]/2
    full_square = -m*(dq-Q*delta_K/K)**2/(3*K)+m*Q*Q*df*dy/(2*a02*K*K)
    eps = s.Symbol("epsilon", real=True)
    p2 = clean(s.diff(p_solution, Y)*Y2)
    shifted_p = p_solution+eps*eps*p2
    perturbed_EL = s.diff(after_tf_Y, p).subs({Y: Y+eps*eps*Y2, p: shifted_p}, simultaneous=True)
    # q[-1] is the orthonormal cross component. It vanishes on diagonal data.
    parity_zero = {q[-1]: 0, momenta[-1]: 0}
    mixed_odd = s.Matrix([s.diff(phase, momenta[-1], variable).subs(parity_zero)
                         for variable in (p, F, R)+momenta[:-1]])
    residuals = {
        "five_momentum_EL": s.Matrix([clean(s.diff(phase, pi).subs(solutions, simultaneous=True))
                                      for pi in momenta]),
        "TF_elimination": clean(after_tf-after_tf_Y.subs(Y, R+sum(qi*qi for qi in q))),
        "p_EL": clean(s.diff(after_tf_Y, p).subs(p, p_solution)),
        "envelope_p": clean(s.diff(after_tf, p)-s.diff(phase, p).subs(solutions, simultaneous=True)),
        "f_Y_equals_mJ_over_2": clean(fY-m*J_reduced/2),
        "odd_momentum_mixed_Hessian": clean(mixed_odd),
        "trace_second_jet_EL": clean(s.diff(perturbed_EL, eps, 2).subs(eps, 0)),
        "rank_one_determinant": clean(hessian.det()),
        "rank_one_square": clean(quadratic_mixed-trace_square),
        "full_F_Hessian_square_and_cross_term": clean(full_quadratic-full_square),
    }
    return dict(m=m, a02=a02, p=p, Q=Q, F=F, R=R, Y=Y, Y2=Y2, K=K,
                J=J, J_reduced=J_reduced, p_solution=p_solution, p_second=p2,
                phase=phase, reduced=reduced, fY=fY, hessian=hessian,
                delta_Q=dq, delta_Y=dy, rank_one_square=trace_square,
                delta_F=df, full_hessian=full_hessian,
                full_F_quadratic=full_square,
                residuals=residuals)


@lru_cache(None)
def homogeneous_branch():
    """Exact IFT hypothesis at the frozen witness; shear is a free data parameter.

    m=V=h0=1 are units. The Hamiltonian is reconstructed from the action,
    not imported from the earlier solver. No continuum inhomogeneous existence
    conclusion is drawn from this finite homogeneous constraint calculation.
    """
    xi, u, pi, shear = s.symbols("xi u bar_pi shear_parameter", real=True)
    ell = s.log(s.Rational(9, 5))
    T = -s.Rational(27, 16)+54/(5*ell)
    a_star = 3-81/(4*T)
    p_R = s.Rational(8, 3)+4*a_star/3
    q_R = -1-3*p_R/8
    F = 3*(p_R*(xi-s.Rational(1, 4))+q_R*(u-s.Rational(2, 3)))/(16*ell**2)
    U = lambda c: (1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2
    a02 = 27*s.exp(-s.Rational(1, 2))/(8*ell**2)
    Lambda = 6*s.exp(-s.Rational(1, 2))-a02*U(s.Rational(4, 9))
    w = (u-1)*xi
    J = 1+s.exp(-6*w)*pi*pi*F/a02
    H0 = (-s.exp((4-3*u)*xi)*pi*pi/3
          +s.exp((3*u-2)*xi)*(Lambda+a02*U(u*u))
          -3*s.exp((3*u-4)*xi))
    shear_term = 4*s.exp((4-3*u)*xi)*shear*shear/J
    witness = {xi: s.Rational(1, 4), u: s.Rational(2, 3),
               pi: -3*s.exp(-s.Rational(1, 2)), shear: 0}
    normalize = lambda expression: s.simplify(expression.subs(witness)*s.exp(s.Rational(1, 2)))
    constraints = s.Matrix([normalize(s.diff(H0, variable)) for variable in (xi, u)])
    hessian = s.hessian(H0, (xi, u)).applyfunc(normalize)
    expected = -s.Matrix([[24, -27], [-27, 2*T+s.Rational(135, 8)]])
    shear_jets = s.Matrix([s.simplify(s.diff(shear_term, variable).subs(shear, 0))
                          for variable in (xi, u, pi)])
    residuals = {
        "homogeneous_constraints_at_witness": constraints,
        "homogeneous_auxiliary_Hessian": (hessian-expected).applyfunc(s.simplify),
        "homogeneous_Hessian_determinant": s.simplify(hessian.det()-12*(4*T-27)),
        "homogeneous_shear_first_jets": shear_jets,
    }
    return dict(T=T, F=F, J=J, H=H0+shear_term, hessian=hessian,
                determinant=s.simplify(hessian.det()),
                determinant_numeric=float(hessian.det()),
                shear_second_at_witness=s.simplify(s.diff(shear_term, shear, 2).subs(witness)),
                residuals=residuals)


@lru_cache(None)
def derive():
    g, p = geometry(), phase_and_mixed_hessian()
    m, J = p["m"], s.Symbol("J_background", positive=True)
    N, A3 = g["N"], g["A"][2]
    measure = N*g["volume"]
    L2 = clean(measure*m*J*g["Y2"]/2)
    kinetic = clean(2*N*N*s.diff(L2, g["gamma_t"], 2)/(m*measure))
    gradient = clean(-2*A3*A3*s.diff(L2, g["gamma_z"], 2)/(m*measure))
    # A direct flat, constant-coefficient benchmark independent of the metric
    # jet routine: h_xy is the only polarization and P_xy is varied explicitly.
    direct = odd_phase_coefficients()
    h = homogeneous_branch()
    residuals = dict(g["residuals"])
    residuals.update(p["residuals"])
    residuals.update(h["residuals"])
    residuals.update(odd_kinetic=clean(kinetic-J), odd_gradient=clean(gradient-J),
                     odd_physical_speed=clean(gradient/kinetic-1),
                     direct_phase_EL=direct["EL_residual"],
                     direct_phase_speed=clean(direct["physical_speed_squared"]-1))
    # Pointwise symbol: k_z/A3 and omega/N are the physical frequency readouts.
    omega, k = s.symbols("omega k_z", real=True)
    characteristic = clean(J*(-omega*omega/(N*N)+k*k/(A3*A3)))
    return dict(geometry=g, phase=p, homogeneous=h, J=J, L2=L2,
                kinetic=kinetic, gradient=gradient,
                physical_speed_squared=clean(gradient/kinetic),
                characteristic=characteristic, residuals=residuals)


def encode(value):
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, s.MatrixBase):
        return encode(value.tolist())
    if isinstance(value, (tuple, list)):
        return [encode(item) for item in value]
    if isinstance(value, s.Basic):
        return str(value)
    return value


def is_zero(value):
    entries = list(value) if isinstance(value, s.MatrixBase) else [value]
    return all(s.simplify(entry) == 0 for entry in entries)


def run():
    started = time.monotonic()
    actual_hashes = {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in INPUTS}
    if actual_hashes != INPUTS:
        raise RuntimeError("Frozen IC6 action/source inputs changed")
    data = derive()
    return encode(dict(
        base_commit=BASE, input_hashes=actual_hashes,
        own_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        software=dict(python=platform.python_version(), sympy=s.__version__),
        coefficient_domain="exact rational functions over real jet symbols; exact log(9/5) homogeneous constants",
        perturbation_bound="second order in one cross polarization; no expansion in background anisotropy or spatial gradients",
        domain="eta=1, J_T>0, K6!=0, N>0, A_i>0, 0<u<1; on-shell diagonal backgrounds depending on t,z with zero shift",
        exact_checks_passed=all(is_zero(value) for value in data["residuals"].values()),
        exact_residuals=data["residuals"],
        odd_L2=data["L2"], characteristic=data["characteristic"],
        physical_speed_squared=data["physical_speed_squared"],
        positive_coefficient=data["J"],
        mixed_Y_Q_hessian=data["phase"]["hessian"],
        rank_one_mixed_square=data["phase"]["rank_one_square"],
        full_F_mixed_quadratic=data["phase"]["full_F_quadratic"],
        homogeneous_auxiliary_determinant=data["homogeneous"]["determinant"],
        full_all_background_causality_proved=False,
        even_physical_characteristics_eliminated=False,
        nonlinear_inhomogeneous_solution_existence_proved=False,
        conclusion="Exact odd-sector luminality on the stated symmetry class; nearby anisotropic homogeneous solutions follow by IFT and a smooth finite Hamiltonian ODE. Full IC6 remains OPEN.",
        runtime_seconds=time.monotonic()-started,
    ))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-all-background-causality", action="store_true")
    args = parser.parse_args()
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(1 if not result["exact_checks_passed"] else
                     2 if args.require_all_background_causality else 0)
