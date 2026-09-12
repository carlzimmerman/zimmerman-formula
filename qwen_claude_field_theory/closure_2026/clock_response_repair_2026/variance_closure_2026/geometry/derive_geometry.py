#!/usr/bin/env python3
"""Exact finite-order geometry and constrained-state closure checks.

No action coefficient is fitted or changed. The physical definition is
Y=(g^{mu nu}+n^mu n^nu) chi_mu chi_nu, n_mu=-tau_mu/s,
s^2=-g^{mu nu}tau_mu tau_nu, with signature -+++.
"""
import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time
import unittest

import sympy as s


def symmetric_symbols(prefix):
    return s.Matrix(4, 4, lambda i, j: s.Symbol(
        f"{prefix}{min(i,j)}{max(i,j)}", real=True))


def contraction_coefficients(left, metric, right):
    """Coefficients of a bilinear contraction, truncated at epsilon^2."""
    return [s.expand(sum((left[i].T * metric[j] * right[k])[0]
                        for i in range(3) for j in range(3) for k in range(3)
                        if i+j+k == order)) for order in range(3)]


@lru_cache(maxsize=1)
def projected_geometry():
    a, s0 = s.symbols("a sbar", positive=True)
    q = s.Symbol("q", real=True)
    chi1 = s.Matrix(s.symbols("sigma_t sigma_x sigma_y sigma_z", real=True))
    tau1 = s.Matrix(s.symbols("pi_t pi_x pi_y pi_z", real=True))
    chi2 = s.Matrix(s.symbols("sigma2_t sigma2_x sigma2_y sigma2_z", real=True))
    tau2 = s.Matrix(s.symbols("pi2_t pi2_x pi2_y pi2_z", real=True))
    chi0, tau0 = s.Matrix([q, 0, 0, 0]), s.Matrix([s0, 0, 0, 0])
    g0 = s.diag(-1, a**-2, a**-2, a**-2)
    metric = [g0, symmetric_symbols("h"), symmetric_symbols("j")]
    chi, tau = [chi0, chi1, chi2], [tau0, tau1, tau2]
    cc = contraction_coefficients(chi, metric, chi)
    tc = contraction_coefficients(tau, metric, chi)
    ss = [-x for x in contraction_coefficients(tau, metric, tau)]
    # Y=(cc*ss+tc^2)/ss. Its numerator has zero epsilon^0 and ^1.
    numerator = [s.expand(sum(cc[j]*ss[order-j] + tc[j]*tc[order-j]
                              for j in range(order+1))) for order in range(3)]
    y2 = s.factor(numerator[2] / ss[0])
    spatial = chi1[1:, 0] - q/s0*tau1[1:, 0]
    expected = (spatial.T*spatial)[0]/a**2
    # Independently expand projected covector r_mu=chi_mu+(tc/ss)tau_mu.
    ratio0 = tc[0]/ss[0]
    ratio1 = tc[1]/ss[0] - tc[0]*ss[1]/ss[0]**2
    r1 = (chi1 + ratio0*tau1 + ratio1*tau0).applyfunc(s.simplify)
    T = s.symbols("T_x T_y T_z", real=True)
    transformed = spatial.subs({**{chi1[i+1]:chi1[i+1]-q*T[i] for i in range(3)},
                                **{tau1[i+1]:tau1[i+1]-s0*T[i] for i in range(3)}},
                               simultaneous=True)
    checks = {
        "background_projection_zero": numerator[0] == 0,
        "linear_projection_zero": numerator[1] == 0,
        "arbitrary_metric_and_second_order_fields_cancel": s.expand(y2-expected) == 0,
        "projected_covector_time_component_zero": r1[0] == 0,
        "projected_covector_spatial_components": all(s.expand(r1[i+1]-spatial[i]) == 0 for i in range(3)),
        "independent_projector_norm": s.expand((r1.T*g0*r1)[0]-expected) == 0,
        "linear_time_gauge_invariance": all(s.expand(transformed[i]-spatial[i]) == 0 for i in range(3)),
    }
    return dict(checks=checks, Y2=str(y2), projected_covector=[str(x) for x in r1],
                symbols=dict(a=a, q=q, sbar=s0), expression=y2,
                metric_symbols=set(metric[1].free_symbols | metric[2].free_symbols),
                second_order_symbols=set(chi2.free_symbols | tau2.free_symbols))


@lru_cache(maxsize=1)
def unitary_adm():
    N, s0 = s.symbols("N sbar", positive=True)
    shift = s.Matrix(s.symbols("beta_x beta_y beta_z", real=True))
    spatial_inverse = s.Matrix(3, 3, lambda i,j: s.Symbol(
        f"h_inv_{min(i,j)}{max(i,j)}", real=True))
    inverse = s.zeros(4)
    inverse[0,0] = -1/N**2
    inverse[0,1:] = shift.T/N**2
    inverse[1:,0] = shift/N**2
    inverse[1:,1:] = spatial_inverse-shift*shift.T/N**2
    chi = s.Matrix(s.symbols("chi_t chi_x chi_y chi_z", real=True))
    tau = s.Matrix([s0, 0, 0, 0])
    clock_norm = -(tau.T*inverse*tau)[0]
    projected = (chi.T*inverse*chi)[0] + (tau.T*inverse*chi)[0]**2/clock_norm
    target = (chi[1:,0].T*spatial_inverse*chi[1:,0])[0]
    phase, k, a, sigma = s.symbols("phase k a sigma", real=True)
    cosine_y = k**2*sigma**2*s.sin(phase)**2/a**2
    average = s.integrate(cosine_y, (phase, 0, 2*s.pi))/(2*s.pi)
    return dict(checks={
        "unitary_ADM_exact_projection": s.expand(projected-target) == 0,
        "cosine_period_average_half": s.simplify(average-k**2*sigma**2/(2*a**2)) == 0,
    }, exact_unitary_Y=str(target), cosine_local_Y2=str(cosine_y), cosine_average_Y2=str(average))


@lru_cache(maxsize=1)
def constrained_obstruction():
    # This is the sparsity and density column of the frozen action reduction,
    # not a surrogate oscillator. Akin is distinct from the six-state Aop.
    Akin, D, E, L, R, jrd, rhod = s.symbols("Akin D E L R jr_dot rho_dot", real=True)
    q, m, p, H, x, r = s.symbols("q M2 p H x r", real=True)
    matrix = s.Matrix([[Akin, 0, 0, D], [0, R, 0, -jrd],
                       [0, 0, 1, -rhod], [E, 0, 0, L]])
    density_source = s.Matrix([0, 0, 3*H, 1/(2*m)])
    solved_density = matrix.inv()*(-density_source)
    delta = Akin*L-E*D
    lapse_density = -Akin/(2*m*delta)
    op05 = q*lapse_density
    op00 = s.Symbol("Aop00", real=True)
    y = p*x*x
    rate_plus = -2*H*y+2*p*x*(op00*x+op05*r)
    rate_minus = -2*H*y+2*p*x*(op00*x-op05*r)
    witness_plus = s.Matrix([x,0,0,0,0,r])
    witness_minus = s.Matrix([x,0,0,0,0,-r])
    Cplus = witness_plus*witness_plus.T
    Cminus = witness_minus*witness_minus.T
    b = s.Matrix(s.symbols("b0:6", real=True))
    return dict(checks={
        "constraint_matrix_determinant": s.factor(matrix.det()-R*delta) == 0,
        "action_density_lapse_column": s.factor(solved_density[3]-lapse_density) == 0,
        "full_density_column_satisfies_constraints": all(s.factor(v) == 0 for v in matrix*solved_density+density_source),
        "same_variance_rank_one_covariances": Cplus[0,0] == Cminus[0,0] == x*x,
        "opposite_density_cross_correlation": Cplus[0,5] == -Cminus[0,5] == x*r,
        "positive_semidefinite_outer_product": s.expand((b.T*Cplus*b)[0]-(b.dot(witness_plus))**2) == 0,
        "nonzero_derivative_gap_formula": s.factor(rate_plus-rate_minus-4*p*x*r*op05) == 0,
    }, determinant=str(s.factor(matrix.det())), lapse_density=str(lapse_density),
        Aop_0_density=str(op05), derivative_gap=str(s.factor(rate_plus-rate_minus)),
        assumptions=["M2>0", "a>0", "sbar>0", "k>0", "W != 0", "R != 0",
                     "Delta=Akin*L-E*D != 0", "q*Akin*x*r != 0"])


@lru_cache(maxsize=1)
def variance_transport():
    H, p, q = s.symbols("H p q", real=True)
    ell = s.Matrix(1,6,s.symbols("ell0:6", real=True))
    op = s.Matrix(6,6,lambda i,j:s.Symbol(f"A{i}{j}", real=True))
    op[0,:] = q*ell
    op[0,1] += 1
    cov = s.Matrix(6,6,lambda i,j:s.Symbol(f"C{min(i,j)}{max(i,j)}", real=True))
    cdot = op*cov+cov*op.T
    vdot = s.expand(-2*H*p*cov[0,0]+p*cdot[0,0])
    target = -2*H*p*cov[0,0]+2*p*(cov[1,0]+q*(ell*cov[:,0])[0])
    u = s.Matrix(s.symbols("u0:6", real=True))
    direct = -2*H*p*u[0]**2+2*p*u[0]*(op*u)[0]
    rank_one = vdot.subs({cov[i,j]:u[i]*u[j] for i in range(6) for j in range(i,6)})
    # Arbitrary real Aop: a one-mode rate factors through p*u0^2 iff the
    # five u0*uj cross coefficients vanish. This check exposes all five.
    generic = s.Matrix(1,6,s.symbols("a0:6", real=True))
    generic_rate = s.expand(-2*H*p*u[0]**2+2*p*u[0]*(generic*u)[0])
    cross = [s.diff(generic_rate,u[0],u[j]) for j in range(1,6)]
    return dict(checks={
        "covariance_transport_identity": s.expand(vdot-target) == 0,
        "rank_one_matches_direct_state_derivative": s.expand(rank_one-direct) == 0,
        "all_five_closure_cross_coefficients": all(s.expand(cross[j-1]-2*p*generic[j]) == 0 for j in range(1,6)),
    }, variance_rate=str(vdot), cross_coefficients=[str(c) for c in cross])


@lru_cache(maxsize=1)
def frozen_action_map():
    """Compare the independent geometry/reconstruction to the existing action."""
    path = Path(__file__).resolve().parents[2]/"cosmological_bridge_2026/derive.py"
    spec = importlib.util.spec_from_file_location("variance_frozen_bridge_derive",path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    d = module.construct()
    v = d["s"]
    a,q,k,g = (v[name] for name in ("a","q","k","gamma"))
    p = k*k/(a*a)
    F = 2*q*v["PXt"]/v["W"]
    G = -2*q*v["WY"]*p/v["W"]
    B = 2*v["PX"]+4*q*q*v["PXX"]
    Rv = q*B-18*g*v["H"]*q*q-2*g*q**3*F
    Rs = -2*g*q**3*G-2*g*q*q*p
    cosine_y = p*v["sigma"]**2*s.Symbol("sine",real=True)**2
    clock_target = -v["W"]*(d["dk"]-F*d["dq"]-G*v["sigma"])
    density_target = Rv*d["dq"]+Rs*v["sigma"]-2*g*q**3*(d["dk"]-F*d["dq"]-G*v["sigma"])
    return dict(checks={
        "frozen_action_gradient_matches_covariant_expansion": s.expand(d["projected_gradient"]["second_order"]-cosine_y) == 0,
        "frozen_action_clock_constraint_map": s.expand(d["clock_equation"]-clock_target) == 0,
        "frozen_action_density_reconstruction": s.expand(d["rho_delta"]-density_target) == 0,
        "frozen_action_sigma_velocity_map": s.expand(d["dq"]+q*v["n"]-v["sigmad"]) == 0,
    }, source=str(path), clock_F=str(F), clock_G=str(G),
        gradient=str(d["projected_gradient"]["second_order"]))


def build_result():
    geometry = projected_geometry()
    results = {"projection": {k:v for k,v in geometry.items() if k not in
                 {"symbols","expression","metric_symbols","second_order_symbols"}},
               "unitary_ADM": unitary_adm(), "action_constraint_obstruction": constrained_obstruction(),
               "variance_transport": variance_transport(), "frozen_action_map":frozen_action_map()}
    checks = {f"{section}.{key}":value for section,data in results.items()
              for key,value in data["checks"].items()}
    if not all(checks.values()):
        raise AssertionError({k:v for k,v in checks.items() if not v})
    results.update(checks=checks, check_count=len(checks),
                   exact_domain="Rational-function identities over R; stated denominators nonzero",
                   scope="Second-order geometric coefficient and exact transport of the linear six-state system",
                   non_claims=["No nonlinear averaged MOND closure", "No exclusion of asymptotic attractors",
                               "No primordial spectrum or initial covariance prediction",
                               "No coefficient reconstruction or new particle species",
                               "No claim that a formal finite-order expansion controls finite-amplitude errors"])
    return results


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-file", type=Path)
    parser.add_argument("--run-tests", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()
    if args.run_tests:
        suite = unittest.TestLoader().discover(str(Path(__file__).resolve().parent), pattern="test_*.py")
        tests = unittest.TextTestRunner(verbosity=2).run(suite)
        if not tests.wasSuccessful():
            raise SystemExit(1)
    result = build_result()
    if args.run_tests:
        result["unit_tests"] = dict(run=tests.testsRun, failures=len(tests.failures), errors=len(tests.errors))
    result["software"] = {"python":platform.python_version(),"sympy":s.__version__}
    result["runtime_seconds"] = time.perf_counter()-started
    result["command_argv"] = [sys.executable, *sys.argv]
    root = Path(__file__).resolve().parents[5]
    frozen = Path(__file__).resolve().parents[2]
    inputs = [Path(__file__).resolve(), Path(__file__).resolve().with_name("test_geometry.py"),
              frozen/"cosmological_bridge_2026/derive.py",
              frozen/"cosmological_bridge_2026/transfer_evolve.py",
              frozen/"nonlinear_evolution_2026/constitutive.py"]
    result["input_hashes"] = {str(path.relative_to(root)):sha256(path) for path in inputs}
    if args.result_file:
        args.result_file.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
