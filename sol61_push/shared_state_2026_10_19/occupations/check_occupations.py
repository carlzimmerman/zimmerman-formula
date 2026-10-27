#!/usr/bin/env python3
"""Small algebra controls, not an original-model equilibrium simulation."""
import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad


def close(a, b, tol=2e-10):
    assert abs(a-b) <= tol*max(1., abs(a), abs(b)), (a, b, tol)


def oscillator_controls():
    # Complete three-coordinate surrogate. All units are dimensionless.
    stiffness = np.array([[2.0, -.3, .1], [-.3, 3.1, -.2], [.1, -.2, .9]])
    source = np.array([.7, -.4, 1.2])
    eig, vectors = np.linalg.eigh(stiffness)
    assert np.all(eig > 0.)
    omega = np.sqrt(eig)
    c = vectors.T @ source
    d2 = c*c/(2*omega)
    chi = float(np.sum(2*d2/omega))
    close(chi, source @ np.linalg.solve(stiffness, source))
    close(np.sum(omega*d2), np.dot(source, source)/2)
    rows = []
    checks = 3
    for beta in (.4, 1., 4.):
        occupation = 1/np.expm1(beta*omega)
        energies = omega*occupation
        derivative = -np.sum(omega**2*occupation*(1+occupation))
        assert derivative < 0
        checks += 1
        for om, dd, nb in zip(omega, d2, occupation):
            r = math.exp(-beta*om)
            # Direct infinite-ladder sums bounded by r^400, not a truncated
            # oscillator Hamiltonian with a spurious commutator at its top.
            pp = (1-r)*r**np.arange(401)
            absorption = sum(pp[n]*(n+1)*dd for n in range(400))
            emission = sum(pp[n+1]*(n+1)*dd for n in range(400))
            close(absorption, dd*(nb+1))
            close(emission, dd*nb)
            close(absorption-emission, dd)
            assert r**400*401 < 1e-55
            checks += 4
        eps = 1e-5
        eplus = np.sum(omega/np.expm1((beta+eps)*omega))
        eminus = np.sum(omega/np.expm1((beta-eps)*omega))
        close((eplus-eminus)/(2*eps), derivative, 2e-8)
        checks += 1
        rows.append({'beta': beta, 'occupation': occupation.tolist(),
                     'excitation_energy': float(sum(energies)),
                     'denergy_dbeta': float(derivative), 'chi': chi})
    pulse = []
    for tau in (.3, 1.2):
        g0 = .07
        for om, dd in zip(omega, d2):
            numerical = quad(lambda t: g0*math.exp(-t*t/(2*tau*tau))*math.cos(om*t),
                             -np.inf, np.inf, epsabs=1e-13)[0]
            exact = math.sqrt(2*math.pi)*g0*tau*math.exp(-.5*om*om*tau*tau)
            close(numerical, exact)
            pulse.append({'tau': tau, 'omega': float(om),
                          'produced_count': float(dd*exact*exact)})
            checks += 1
    return {'dimension': 3, 'omega': omega.tolist(), 'c': c.tolist(),
            'd2': d2.tolist(), 'thermal': rows, 'pulse': pulse, 'checks': checks}


def microcanonical_controls():
    # All partitions of exact integer energy for the stated two modes.
    rows = []
    checks = 0
    for energy in (0, 1, 2, 3, 4, 7, 10):
        # Occupation bounds follow from energy positivity; no shell is missed.
        shell = [(n1, n2) for n1 in range(energy+1)
                 for n2 in range(energy//2+1) if n1+2*n2 == energy]
        expected_size = energy//2+1
        assert len(shell) == expected_size
        mean = np.mean(shell, axis=0)
        close(mean[1], (energy//2)/2)
        close(mean[0]+2*mean[1], energy)
        checks += 3
        rows.append({'energy': energy, 'shell_size': len(shell), 'mean': mean.tolist()})
    return {'frequencies': [1, 2], 'shells': rows, 'checks': checks}


def finite_quantum_controls():
    # Exact finite Hilbert space, generic odd source. It is not a claim that
    # this four-state model is derived from Phi/X or a physical gravity source.
    h0 = np.diag([0., .9, 1.7, 2.8])
    parity = np.diag([1., -1., 1., -1.])
    dipole = np.array([[0., .6, 0., -.2], [.6, 0., .3, 0.],
                       [0., .3, 0., .7], [-.2, 0., .7, 0.]])
    close(np.linalg.norm(parity@dipole@parity+dipole), 0.)
    dnorm = np.linalg.norm(dipole, 2)
    radius = .9/(2*dnorm)
    checks = 1

    def values(g, beta):
        ev, u = np.linalg.eigh(h0-g*dipole)
        mat = u.T@dipole@u
        if beta is None:
            probabilities = np.array([1., 0., 0., 0.])
            free = ev[0]
        else:
            zweights = np.exp(-beta*(ev-ev[0]))
            probabilities = zweights/sum(zweights)
            free = ev[0]-math.log(sum(zweights))/beta
        return free, float(np.dot(probabilities, np.diag(mat)))

    rows = []
    for beta, g in itertools.product((None, .4, 1.5, 6.), (.002, .01, .07, .2)):
        assert g < radius
        fp, pp = values(g, beta)
        fm, pm = values(-g, beta)
        close(fp, fm)
        close(pp, -pm)
        epsilon = 1e-5
        derivative = -(values(g+epsilon, beta)[0]-values(g-epsilon, beta)[0])/(2*epsilon)
        close(pp, derivative, 3e-8)
        checks += 4
        rows.append({'beta': beta, 'g': g, 'P': pp})
    # Positive gaps and parity: zero-field static Kubo equals finite-field slope.
    ev, u = np.linalg.eigh(h0)
    mat = u.T@dipole@u
    for beta in (None, .4, 1.5, 6.):
        if beta is None:
            p = np.array([1., 0., 0., 0.])
        else:
            p = np.exp(-beta*ev)
            p /= sum(p)
        spectral = sum(2*(p[a]-p[b])*mat[a,b]**2/(ev[b]-ev[a])
                       for a in range(4) for b in range(a+1, 4))
        numerical = values(1e-5, beta)[1]/1e-5
        close(spectral, numerical, 2e-9)
        close(np.dot(p, np.diag(mat)), 0.)
        checks += 2
    return {'dimension': 4, 'bounded_source_norm': float(dnorm),
            'guaranteed_local_radius': float(radius), 'rows': rows, 'checks': checks}


def cutoff_controls():
    # Diagnostic TLS spectrum in a=p_sat=1 units; it is explicitly imposed.
    def weight(x):
        return x/(1+x*x)**1.5

    def response(g, low, high):
        if g == 1.:
            return .5*(1/(1+low*low)-1/(1+high*high))
        return g/(g*g-1)*(math.sqrt((g*g+low*low)/(1+low*low))
                          -math.sqrt((g*g+high*high)/(1+high*high)))

    rows, checks = [], 0
    for low, high, g in itertools.product((.01, .2), (3., 100.), (.03, .1, 1., 5., 10.)):
        numerical = quad(lambda x: weight(x)*g/math.sqrt(g*g+x*x), low, high,
                         epsabs=1e-12, epsrel=1e-12)[0]
        exact = response(g, low, high)
        close(numerical, exact)
        target = g/(1+g)
        ir = low*low*(1+g)/(2*g)
        uv = (1+g)*(1-high/math.sqrt(1+high*high))
        error = (target-exact)/target
        assert -1e-13 <= error <= ir+uv+1e-12
        checks += 2
        rows.append({'low': low, 'high': high, 'g': g,
                     'P': exact, 'relative_error': error, 'upper_bound': ir+uv})
    slope_rows = []
    for low in (.001, .01, .1):
        high = 100.
        slope = high/math.sqrt(1+high*high)-low/math.sqrt(1+low*low)
        cubic = -.5*quad(lambda x: weight(x)/x**3, low, high,
                         epsabs=1e-9, epsrel=1e-11)[0]
        aa = lambda x: math.sqrt(1+x*x)/x+x/math.sqrt(1+x*x)
        exact_cubic = .5*(aa(high)-aa(low))
        close(cubic, exact_cubic, 2e-10)
        close(quad(lambda x: weight(x)/x, low, high, epsabs=1e-12)[0], slope)
        slope_rows.append({'low': low, 'slope': slope, 'cubic': cubic,
                           'minus_2low_cubic': -2*low*cubic})
        checks += 2
    bound = .01**2*(1+.1)/(2*.1)+11*(1-100/math.sqrt(10001))
    assert bound < .00110
    checks += 1
    thermal = []
    for beta, alpha in itertools.product((.4, 1., 5.), (0., 1/3)):
        # d(Delta)=Delta^-alpha; soft endpoint integrable for these controls.
        susceptibility = quad(lambda x: math.tanh(beta*x**(1-alpha))/(1+x*x)**1.5,
                              0, np.inf, epsabs=2e-11)[0]
        assert 0 < susceptibility < 1
        thermal.append({'beta': beta, 'd_exponent': -alpha,
                        'thermal_susceptibility': susceptibility})
        checks += 1
    return {'rows': rows, 'slope_and_cubic': slope_rows, 'thermal_tls': thermal,
            'window_example_bound': bound, 'checks': checks}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    arguments = parser.parse_args()
    result = {'scope': 'Finite algebra and quadrature controls only; not shared-state formation',
              'oscillators': oscillator_controls(),
              'microcanonical': microcanonical_controls(),
              'finite_quantum': finite_quantum_controls(),
              'cutoff_tls_diagnostic': cutoff_controls()}
    result['checks'] = sum(result[x]['checks'] for x in
                           ('oscillators', 'microcanonical', 'finite_quantum', 'cutoff_tls_diagnostic'))
    result['status'] = 'passed'
    Path(arguments.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'checks': result['checks'],
                      'window_error_bound': result['cutoff_tls_diagnostic']['window_example_bound']}))
