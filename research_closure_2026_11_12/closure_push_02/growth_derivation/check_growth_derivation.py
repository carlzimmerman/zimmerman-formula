#!/usr/bin/env python3
"""Independent action-to-density identities and a finite-q ODE comparison."""
import argparse
import json
from pathlib import Path
import platform
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    checks = []

    def exact(name, expression):
        residual = s.simplify(expression)
        checks.append({'name': name, 'passed': residual == 0, 'residual': str(residual)})

    q, mu, K, k, n, h, hd, hdd, qd, qdd = s.symbols('q mu K k n h hd hdd qd qdd', positive=True)
    F = mu**2*(q-1)**2/(2*K)
    charge = s.diff(F, q)
    rho = q*charge-F
    exact('rho_charge_distinction', rho-charge*(q+1)/2)
    exact('enthalpy', rho+F-q*charge)
    A = (mu**2*q**2+k**2)/K
    alpha = s.symbols('alpha')
    drho = -q**2*s.diff(F, q, 2)*alpha-k**2*alpha/K
    exact('density_lapse', drho+A*alpha)
    exact('pressure_ratio', (-q*charge*alpha)/drho-q*charge/A)
    B = qd/q-hd/h
    Bd = qdd/q-qd**2/q**2-hdd/h+hd**2/h**2
    exact('density_friction', B+2*h+hd/h-(2*h+qd/q))
    background = Bd+(2*h+hd/h)*B
    exact('cold_background_jeans', background.subs({qd: 0, qdd: 0, hdd: -3*h*hd})+2*hd-3*hd)
    exact('cold_pressure_gravity_cancellation', K*n-K*n*k**2/(mu**2+k**2)-K*n*mu**2/(mu**2+k**2))
    G = s.symbols('Gamma', nonnegative=True)
    Ag = mu**2/K+k**2/(K+G*k**2)
    exact('smooth_stiffness_A_derivative', s.diff(Ag, G)+k**4/(K+G*k**2)**2)

    # Independent NR canonical elimination: Pi auxiliary, charge and Poisson.
    X, Pi, dn, db, rb = s.symbols('X Pi dn db rb')
    L = mu**2*X**2/(2*K)+X*Pi-K*Pi**2/(2*k**2)
    pi_sol = s.solve(s.diff(L, Pi), Pi)[0]
    Leff = s.simplify(L.subs(Pi, pi_sol))
    exact('canonical_polarization_elimination', pi_sol-k**2*X/K)
    exact('canonical_charge', s.diff(Leff, X)-(mu**2+k**2)*X/K)
    dark_source = K*(rb*db+dn)-K*k**2*dn/(mu**2+k**2)
    exact('two_fluid_dark_source', dark_source-K*(rb*db+mu**2*dn/(mu**2+k**2)))
    exact('baryon_forcing_not_suppressed', s.diff(dark_source, db)-K*rb)
    fb, f, lam = s.symbols('fb f lam')
    M = s.Matrix([[(1-fb)*f, fb], [1-fb, fb]])
    exact('source_characteristic', (M-lam*s.eye(2)).det()-(lam**2-((1-fb)*f+fb)*lam-fb*(1-fb)*(1-f)))
    exact('GR_joint_growing_eigenvalue', (M-s.eye(2)).det().subs(f, 1))

    # Prove the first-order action-to-density change of variables directly.
    t = s.symbols('t')
    Ht, qt, Dt, kt, Zt = [s.Function(v)(t) for v in ['H', 'q', 'D', 'k', 'Z']]
    Y = -qt*Dt/Ht
    first = s.diff(Y, t)+qt*kt**2*Zt/Ht**2
    target = -qt/Ht*(s.diff(Dt, t)+(s.diff(qt,t)/qt-s.diff(Ht,t)/Ht)*Dt-kt**2*Zt/Ht)
    exact('action_to_density_first_order', first-target)
    # A mutation control: removing polarization is not algebraically equivalent.
    mutation_residual = s.simplify((1-k**2/mu**2)-mu**2/(mu**2+k**2))
    mutation_witness = float(mutation_residual.subs({k: 2, mu: 1}))
    checks.append({'name': 'missing_polarization_mutation_detected', 'passed': mutation_witness != 0, 'residual_at_k2_mu1': mutation_witness})

    # Finite-q exact background: K=1, mu=2, q=1+0.001 a^-3, rho_Lambda=0.7.
    N = s.symbols('N', real=True)
    qN = 1+s.Rational(1, 1000)*s.exp(-3*N)
    hn = s.sqrt(s.Rational(2, 3)*(2*(qN**2-1)+s.Rational(7, 10)))
    kn = s.Rational(7, 10)*s.exp(-N)
    nn = 4*(qN-1)
    An = 4*qN**2+kn**2
    u = s.diff(hn, N)/hn
    b = s.diff(qN, N)/qN-u
    P = u+2+s.diff(qN, N)/qN
    V = qN*nn/An*kn**2/hn**2+s.diff(b, N)+(2+2*u)*b
    coeff = s.lambdify(N, [qN, hn, kn, nn, An, b, P, V], 'numpy')
    start, end = -np.log(5.0), 0.0
    initial = coeff(start)
    q0, h0, k0, _, _, b0, _, _ = initial
    delta0, derivative0 = 1.0, 0.8
    zeta0 = h0*h0/(k0*k0)*(derivative0+b0*delta0)
    y0 = -q0/h0*delta0

    def action_rhs(nlog, y):
        qq, hh, kk, nq, aa, _, _, _ = coeff(nlog)
        return [hh*nq/aa*y[1], -qq*kk*kk/(hh**3)*y[0]]

    def density_rhs(nlog, y):
        *_, pp, vv = coeff(nlog)
        return [y[1], -pp*y[1]-vv*y[0]]

    grid = np.linspace(start, end, 401)
    action = solve_ivp(action_rhs, [start, end], [zeta0, y0], method='DOP853', rtol=2e-11, atol=2e-13, t_eval=grid)
    density = solve_ivp(density_rhs, [start, end], [delta0, derivative0], method='DOP853', rtol=2e-11, atol=2e-13, t_eval=grid)
    qc, hc, *_ = coeff(grid)
    mapped = -hc/qc*action.y[1]
    error = np.max(np.abs(mapped-density.y[0]))/max(1.0, np.max(np.abs(density.y[0])))
    checks.append({'name': 'finite_q_action_density_ODE_agreement', 'passed': bool(action.success and density.success and error < 2e-9), 'relative_max_error': float(error), 'samples': 401})

    I0 = 4.037e-8
    rows = []
    for mass in [198.25, 25120.0]:
        offset = I0*(1+3400)**3/(2*mass*mass)
        rows.append({'mu_per_Mpc': mass, 'q_minus_1_at_z3400': offset, 'w_at_z3400': offset/(2+offset), 'z_q_minus_1_equals_1': (2*mass*mass/I0)**(1/3)-1,
                     'crossovers': [{'k_com_per_Mpc': wave, 'z_half': mass/wave-1, 'f_at_z3400': mass*mass/(mass*mass+(wave*3401)**2)} for wave in [0.2, 2.0, 20/3]]})
    exponents = []
    for suppression in [0.0, 0.5, 1.0]:
        baryon_fraction = .16
        a11 = (1-baryon_fraction)*suppression
        eigenvalue = (a11+baryon_fraction+np.sqrt((a11-baryon_fraction)**2+4*baryon_fraction*(1-baryon_fraction)))/2
        exponent = (-1+np.sqrt(1+24*eigenvalue))/4
        exponents.append({'f': suppression, 'baryon_fraction': baryon_fraction, 'lambda_plus': float(eigenvalue), 'p_plus': float(exponent)})
    checks.append({'name': 'EdS_recovery', 'passed': abs(exponents[-1]['p_plus']-1) < 1e-14})
    result = {'passed': all(c['passed'] for c in checks), 'checks': checks,
              'finite_q_ODE': {'K': 1, 'mu': 2, 'q_minus_1_today': .001, 'rho_Lambda': .7, 'k_com': .7, 'z_start': 4, 'z_end': 0, 'method': 'DOP853', 'rtol': 2e-11, 'atol': 2e-13, 'relative_max_error': float(error)},
              'background_I0_per_Mpc2': I0, 'diagnostic_rows': rows, 'frozen_f_EdS_diagnostics': exponents,
              'software': {'python': platform.python_version(), 'sympy': s.__version__, 'numpy': np.__version__, 'scipy': scipy.__version__},
              'non_claims': ['No integrated two-component growth prediction', 'No CMB or radiation transfer', 'No likelihood or new lower-mu bound', 'No Frechet linearization of literal Pi-positive stiffness']}
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'passed': result['passed'], 'checks': len(checks), 'finite_q_ODE_error': float(error)}))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
