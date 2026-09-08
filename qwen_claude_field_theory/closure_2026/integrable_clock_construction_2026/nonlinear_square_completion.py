#!/usr/bin/env python3
"""IC-5: explicit nonlinear square completion of the IC-4 Hamiltonian.

Base 6708f1e3e. Exact identities plus a periodic, variational finite-grid
auxiliary solve. Neither the grid nor auxiliary coercivity proves full
physical causality, PPN, or a complete gravitational/matter DOF classification.
The entire Hamiltonian, including the smooth transition, is defined here.
"""
import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import platform

import numpy as np
import sympy as s

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "IC4_ACTION.md"


def potential(c):
    return (1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2


def activation(r):
    """Even smooth plateau: 1 for |r^2-1|<=1/4, 0 for |r^2-1|>=1/2.

    With E(t)=exp(-1/t) for t>0 and 0 otherwise, this equals
    E(1/4-(r^2-1)^2)/(E(1/4-(r^2-1)^2)+E((r^2-1)^2-1/16)).
    The denominator is strictly positive; evaluation avoids underflow.
    """
    distance2 = (r*r-1.)**2
    if distance2 <= 1./16.:
        return 1.
    if distance2 >= 1./4.:
        return 0.
    log_ratio = -1./(distance2-1./16.)+1./(1./4.-distance2)
    if log_ratio >= 0:
        x = math.exp(-log_ratio)
        return x/(1.+x)
    return 1./(1.+math.exp(log_ratio))


@lru_cache(None)
def derive():
    m, vol, h0, a02, kappa = s.symbols("m vol h0 a0_squared kappa", positive=True)
    xi, u, trace, shear2, R, Lam = s.symbols("xi u pi shear_squared Rbar Lambda", real=True)
    ax, au = s.symbols("Dxi Du", real=True)
    T, ell = s.symbols("Tcal ell", positive=True)
    sigma = s.Rational(1, 3)
    e = s.Rational(1, 8)
    d = -9*e/T
    alpha = 81*e/T**2
    beta = 2*d-s.Rational(1, 3)-3*alpha/4
    gamma = e-s.Rational(1, 16)+9*alpha/64-3*d/4
    b = s.factor((beta+s.Rational(1, 3))/(2*alpha))
    a_star = 3-81/(4*T)
    pR = s.Rational(8, 3)+4*a_star*sigma
    qR = -1-3*pR/8
    F = 3*(pR*(xi-s.Rational(1, 4))+qR*(u-s.Rational(2, 3)))/(16*ell**2)
    w = (u-1)*xi
    J = 3*(alpha*ax**2+beta*ax*au+gamma*au**2)/(4*ell**2)
    Z = s.exp(-2*w)*(J+F*R)/a02
    kinetic_trace = -s.exp((4-3*u)*xi)*trace**2/(3*m*vol)
    kinetic_shear = 2*s.exp((4-3*u)*xi)*shear2/(m*vol)
    Hpotential = m*vol*s.exp((3*u-2)*xi)*(Lam+a02*potential(u*u))
    Hpotential -= kappa*vol*s.exp((3*u-4)*xi)/2
    Hcurvature = -m*vol*s.exp(u*xi)*R/2
    Hstatic_gradient = -m*vol*s.exp(u*xi)*(2*u*xi*ax*au+xi**2*au**2)
    D = -s.exp((6-5*u)*xi)*trace**2/(2*m*vol*a02)
    Hsquare = -m*vol*s.exp(u*xi)*alpha*(ax+b*au)**2
    Hbase = kinetic_trace+kinetic_shear+Hpotential+Hcurvature
    eta = s.Symbol("eta", real=True)
    H5 = Hbase+D*F*R+(1-eta)*(Hstatic_gradient+D*J)+eta*Hsquare
    H4 = kinetic_shear+kinetic_trace/(1-3*Z/2)+Hpotential+Hcurvature+Hstatic_gradient
    Hlinear = Hbase+Hstatic_gradient+D*(J+F*R)
    r = -trace*s.exp((4-3*u)*xi)/(3*m*vol*h0)

    f = s.exp(-s.Rational(1, 2))
    a02_witness = 27*h0*h0*f/(8*ell**2)
    witness = {xi:s.Rational(1, 4), u:s.Rational(2, 3), trace:-3*m*vol*f*h0,
               a02:a02_witness, kappa:6*m*h0*h0, shear2:0, R:0}
    normalized_G = s.Matrix([[alpha, (beta+s.Rational(1, 3))/2],
                             [(beta+s.Rational(1, 3))/2, gamma+s.Rational(1, 16)]])
    square_matrix = s.hessian(alpha*(ax+b*au)**2, (ax, au))/2
    square_hessian = 2*square_matrix
    gradient_match = (normalized_G-square_matrix).applyfunc(s.factor)
    witness_gradient_difference = s.factor((Hsquare-Hstatic_gradient-D*J).subs(witness))
    rational_remainder = s.factor(H4-Hlinear-kinetic_trace*(3*Z/2)**2/(1-3*Z/2))
    curvature_coefficient_match = s.factor(s.diff(Hlinear-Hbase-Hstatic_gradient, R)-D*F)
    static_difference = H5.subs(eta, 0)-H4
    static_first_jets = [s.simplify(expr.subs(trace, 0)) for expr in
                        [static_difference]+[s.diff(static_difference, q)
                        for q in (trace, xi, u, vol, R, ax, au, shear2)]]
    homogeneous_difference = s.simplify((H5-H4).subs({ax:0, au:0, R:0}))

    active, passive, da, dt = s.symbols("s_active t_passive Ds Dt", real=True)
    coordinates = {xi:active-b*passive, u:passive, ax:da-b*dt, au:dt}
    square_transformed = s.simplify(Hsquare.subs(coordinates, simultaneous=True))
    passive_gradient_derivative = s.diff(square_transformed, dt)
    coordinate_jacobian = s.Matrix([active-b*passive, passive]).jacobian((active, passive))
    # Differentiate at fixed metric and canonical momenta, THEN insert witness.
    Hnongrad = Hbase+D*F*R
    Lam_witness = 6*h0*h0*f-a02_witness*potential(s.Rational(4, 9))
    mass = -s.hessian(Hnongrad, (xi, u))
    mass = mass.subs(Lam, Lam_witness).subs(witness)/(m*vol*f*h0*h0)
    mass = mass.applyfunc(lambda v: s.simplify(v.subs(s.log(s.Rational(5, 9)), -ell)))
    mass = mass.applyfunc(lambda v: s.factor(v.subs(1/ell, 5*(T+s.Rational(27, 16))/54)))
    mass_transformed = (coordinate_jacobian.T*mass*coordinate_jacobian).applyfunc(s.factor)
    mass_matrix = mass

    # Direct trace Legendre inversion on eta=1; tensor components use the
    # separately derived six-component transform in nonlinear_hamiltonian.py.
    V, C, zr = s.symbols("V C Z_R", real=True)
    trace_factor = 1+3*zr/2
    Ltrace = -2*C*V*V/(3*trace_factor)
    p_derived = s.diff(Ltrace, V)*s.Rational(3, 2)
    Vsol = s.solve(s.Eq(trace, p_derived), V)[0]
    Htrace_legendre = s.factor((2*trace*V/3-Ltrace).subs(V, Vsol))
    legendre_residuals = [s.factor(Htrace_legendre+trace_factor*trace**2/(6*C)),
                         s.factor(Vsol+trace_factor*trace/(2*C)),
                         s.factor(s.diff(Ltrace, V, 2)+4*C/(3*trace_factor))]

    # Covariant phase-space density: P^{mu nu} is a six-component symmetric
    # tensor tangent to the clock leaves. No derivative of P enters its EL.
    p, ptf2, Rh, ap, up = s.symbols("p_physical PTF_squared Rhat a_physical Du_physical", real=True)
    Jphysical = J.subs({ax:ap, au:up})
    Hcov5 = 2*(ptf2-p*p/6)/m+m*(Lam+a02*potential(u*u))-kappa*s.exp(-2*xi)/2-m*Rh/2
    Hcov5 -= p*p*F*Rh/(2*m*a02)
    Hcov5 -= (1-eta)*(m*(2*u*xi*ap*up+xi*xi*up*up)+p*p*Jphysical/(2*m*a02))
    Hcov5 -= eta*m*alpha*(ap+b*up)**2
    covariant_substitution = {trace:vol*s.exp(3*w)*p,
                              shear2:vol**2*s.exp(6*w)*ptf2,
                              R:s.exp(2*w)*Rh, ax:s.exp(w)*ap, au:s.exp(w)*up}
    Hconverted = s.expand(H5.subs(covariant_substitution, simultaneous=True)/(s.exp(xi+3*w)*vol))
    covariant_bridge = dict(
        hamiltonian_density=s.simplify(Hconverted-Hcov5),
        symplectic_density=s.simplify(s.exp(5*w)*2*s.exp(xi-2*w)/(s.exp(xi+3*w))-2),
        activation_argument=s.simplify(r.subs(trace, vol*s.exp(3*w)*p)+s.exp(xi)*p/(3*m*h0)))
    Qt, Qs, Pt = s.symbols("Q_trace Q_tensor P_tensor", real=True)
    Kfac = 1+3*F*Rh/(2*a02)
    phase_kinetic = 2*Pt*Qs+2*p*Qt/3-2*Pt**2/m+Kfac*p*p/(3*m)
    covariant_momenta = s.solve([s.diff(phase_kinetic, v) for v in (Pt, p)], (Pt, p), dict=True)[0]
    covariant_reduced = s.simplify(phase_kinetic.subs(covariant_momenta))
    covariant_elimination = dict(
        tensor=s.simplify(covariant_momenta[Pt]-m*Qs/2),
        trace=s.simplify(covariant_momenta[p]+m*Qt/Kfac),
        lagrangian=s.simplify(covariant_reduced-m*Qs**2/2+m*Qt**2/(3*Kfac)))

    # Direct second epsilon variation of P(s,t)+A(s,t)|Ds|^2, not a
    # principal-symbol-only test. Retains the mixed 4 A_q delta q Ds Ddelta s.
    eps, ws, wt, gs, dws = s.symbols("epsilon delta_s delta_t grad_s grad_delta_s", real=True)
    # Independent unrestricted two-jets suffice for this pointwise identity;
    # this avoids SymPy's unevaluated dummy mixed-derivative substitutions.
    pjets = s.symbols("P0 Ps Pt Pss Pst Ptt", real=True)
    ajets = s.symbols("A0 As At Ass Ast Att", real=True)
    def two_jet(coeff):
        return coeff[0]+coeff[1]*active+coeff[2]*passive+coeff[3]*active**2/2+coeff[4]*active*passive+coeff[5]*passive**2/2
    Pfun, Afun = two_jet(pjets), two_jet(ajets)
    perturb = {active:active+eps*ws, passive:passive+eps*wt}
    density_eps = Pfun.subs(perturb, simultaneous=True)+Afun.subs(perturb, simultaneous=True)*(gs+eps*dws)**2
    second_variation = s.diff(density_eps, eps, 2).subs(eps, 0).doit()
    W = s.Matrix([ws, wt])
    expected_second_variation = (W.T*(s.hessian(Pfun, (active, passive))+s.hessian(Afun, (active, passive))*gs**2)*W)[0]
    expected_second_variation += 4*(s.diff(Afun, active)*ws+s.diff(Afun, passive)*wt)*gs*dws+2*Afun*dws**2
    second_variation_residual = s.simplify(second_variation-expected_second_variation)
    xyz = s.symbols("x y z", real=True)
    amp = s.Symbol("epsilon_TT", real=True)
    Pi_seed = s.diag(trace/3+amp*s.cos(xyz[2]), trace/3-amp*s.cos(xyz[2]), trace/3)
    TT_momentum_constraint = s.Matrix([-2*sum(s.diff(Pi_seed[i, j], xyz[j]) for j in range(3)) for i in range(3)])
    return locals()


@lru_cache(None)
def numerical():
    d = derive()
    return solve_auxiliary_density(d, d["Hnongrad"])


def solve_auxiliary_density(d, Hnongrad):
    """Solve actual discrete -H auxiliary variation for TT initial momentum.

    Periodic z in [0,2pi), bar h=delta, pi=-3 exp(-1/2), and
    pi_TF=diag(eps cos z,-eps cos z,0). The spatial momentum constraint
    vanishes analytically. No matter source, empirical data, or time evolution.
    """
    ell_value = s.log(s.Rational(9, 5))
    T_value = -s.Rational(27, 16)+54/(5*ell_value)
    constants = {d["m"]:1, d["vol"]:1, d["h0"]:1, d["kappa"]:6,
                 d["ell"]:ell_value, d["T"]:T_value,
                 d["a02"]:27*s.exp(-s.Rational(1, 2))/(8*ell_value**2),
                 d["trace"]:-3*s.exp(-s.Rational(1, 2)), d["R"]:0}
    constants[d["Lam"]] = 6*s.exp(-s.Rational(1, 2))-constants[d["a02"]]*potential(s.Rational(4, 9))
    active, passive = d["active"], d["passive"]
    P = (-Hnongrad).subs(d["coordinates"], simultaneous=True).subs(constants)
    A = (d["m"]*d["vol"]*s.exp(d["u"]*d["xi"])*d["alpha"]).subs(d["coordinates"], simultaneous=True).subs(constants)
    q = (active, passive)
    gradient = s.lambdify((active, passive, d["shear2"]), [s.diff(P, v) for v in q], "numpy")
    hessian = s.lambdify((active, passive, d["shear2"]), s.hessian(P, q), "numpy")
    Ai, Aj, si, ti, sj, tj, step = s.symbols("Ai Aj si ti sj tj dz", real=True)
    edge = (A.subs({active:si, passive:ti})+A.subs({active:sj, passive:tj}))*(sj-si)**2/(2*step**2)
    edge_variables = (si, ti, sj, tj)
    edge_gradient = s.lambdify((*edge_variables, step), [s.diff(edge, v) for v in edge_variables], "numpy")
    edge_hessian = s.lambdify((*edge_variables, step), s.hessian(edge, edge_variables), "numpy")
    b = float(d["b"].subs(d["T"], T_value))
    q0 = np.array([.25+b*2/3, 2/3])
    epsilon = .035
    records, solutions = [], {}
    for size in (16, 32, 64):
        mesh = 2*np.pi*np.arange(size)/size
        step_value = 2*np.pi/size
        shear = 2*epsilon**2*np.cos(mesh)**2
        initial = np.tile(q0, (size, 1))

        def variation(values):
            grad = np.array([gradient(*values[i], shear[i]) for i in range(size)], dtype=float).reshape(-1)
            mat = np.zeros((2*size, 2*size))
            for i in range(size):
                mat[2*i:2*i+2, 2*i:2*i+2] += np.asarray(hessian(*values[i], shear[i]), dtype=float)
                j = (i+1) % size
                ids = [2*i, 2*i+1, 2*j, 2*j+1]
                args = (*values[i], *values[j], step_value)
                grad[ids] += np.asarray(edge_gradient(*args), dtype=float).reshape(4)
                mat[np.ix_(ids, ids)] += np.asarray(edge_hessian(*args), dtype=float)
            return grad, mat

        values = initial.copy()
        residuals = []
        for iteration in range(16):
            grad, mat = variation(values)
            residuals.append(float(np.max(np.abs(grad))))
            if residuals[-1] < 1e-11:
                break
            direction = np.linalg.solve(mat, -grad).reshape(size, 2)
            for exponent in range(14):
                proposed = values+direction*2.**(-exponent)
                if not np.all((proposed[:, 1] > 0) & (proposed[:, 1] < 1)):
                    continue
                new_grad, _ = variation(proposed)
                if np.max(np.abs(new_grad)) < residuals[-1]:
                    values = proposed
                    break
            else:
                break
        grad, mat = variation(values)
        xi_values = values[:, 0]-b*values[:, 1]
        rvalues = np.exp(-.5+(4-3*values[:, 1])*xi_values)
        records.append(dict(nodes=size, iterations=iteration, residual=float(np.max(np.abs(grad))),
                            initial_residual=residuals[0], residual_history=residuals,
                            smallest_hessian_eigenvalue=float(np.linalg.eigvalsh(mat)[0]),
                            symmetry_error=float(np.max(np.abs(mat-mat.T))),
                            maximum_departure_of_r_from_one=float(np.max(np.abs(rvalues-1))),
                            xi_range=[float(np.min(xi_values)), float(np.max(xi_values))],
                            u_range=[float(np.min(values[:, 1])), float(np.max(values[:, 1]))]))
        solutions[size] = np.column_stack((xi_values, values[:, 1]))
    return dict(records=records, epsilon=epsilon, periodic_length=2*math.pi,
                all_converged=all(v["residual"] < 1e-10 for v in records),
                maximum_residual=max(v["residual"] for v in records),
                minimum_hessian_eigenvalue=min(v["smallest_hessian_eigenvalue"] for v in records),
                maximum_departure_of_r_from_one=max(v["maximum_departure_of_r_from_one"] for v in records),
                refinement_difference_16_32=float(np.max(np.abs(solutions[16]-solutions[32][::2]))),
                refinement_difference_32_64=float(np.max(np.abs(solutions[32]-solutions[64][::2]))),
                inhomogeneous_auxiliary_amplitude=float(np.ptp(solutions[64][:, 0])),
                non_claim="Finite variational grid, not a continuum or evolution proof; no empirical observations used.")


def run(include_numeric=True):
    d = derive()
    residuals = dict(gradient_match=list(d["gradient_match"]),
                     rational_remainder=d["rational_remainder"],
                     witness_gradient_difference=d["witness_gradient_difference"],
                     curvature_coefficient_match=d["curvature_coefficient_match"],
                     static_first_jets=d["static_first_jets"],
                     homogeneous_difference=d["homogeneous_difference"],
                     passive_gradient_derivative=s.diff(d["square_transformed"], d["dt"]),
                     legendre=d["legendre_residuals"],
                     covariant_bridge=list(d["covariant_bridge"].values()),
                     covariant_elimination=list(d["covariant_elimination"].values()),
                     second_variation=d["second_variation_residual"],
                     TT_momentum=list(d["TT_momentum_constraint"]))
    flat = [x for value in residuals.values() for x in (value if isinstance(value, list) else [value])]
    result = dict(candidate="IC-5 nonlinear square completion", base="6708f1e3e695a99f3fc3f121e14528f68ace641c",
                  input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  python=platform.python_version(), sympy=s.__version__, numpy=np.__version__,
                  exact_residuals={key:[str(x) for x in value] if isinstance(value, list) else str(value)
                                   for key, value in residuals.items()},
                  exact_checks_passed=all(v == 0 for v in flat),
                  mass_matrix=str(d["mass"]), mass_determinant=str(s.factor(d["mass"].det())),
                  nonlinear_square_rank=d["square_matrix"].rank(),
                  algebraic_coordinate="t=u; active s=xi+b*u; b="+str(d["b"]),
                  full_theory_closed=False,
                  remaining=["Nonlinear physical characteristics and matter/clock classification",
                             "Transition-region health and galactic/cosmological matching",
                             "Full PPN, zero-field limit and realistic cosmology"])
    if include_numeric:
        result["numerical"] = numerical()
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbolic-only", action="store_true")
    parser.add_argument("--require-full-closure", action="store_true")
    args = parser.parse_args(argv)
    result = run(not args.symbolic_only)
    print(json.dumps(result, indent=2, allow_nan=False))
    if not result["exact_checks_passed"]:
        return 1
    if not args.symbolic_only and not result["numerical"]["all_converged"]:
        return 1
    return 2 if args.require_full_closure else 0


if __name__ == "__main__":
    raise SystemExit(main())
