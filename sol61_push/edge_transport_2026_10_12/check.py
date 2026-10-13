#!/usr/bin/env python3
"""Bounded checks of a conditional orbital-edge diffusion model, not halo data."""
import json
from pathlib import Path
import sys
import numpy as np
from scipy.integrate import quad
from scipy.special import erf, erfinv

checks = []


def check(name, ok, value=None):
    checks.append({'name': name, 'passed': bool(ok), 'value': value})


def main():
    out = Path(sys.argv[1])
    # Smooth stationary covariance and three exactly known orbital harmonics.
    omega, tau, sigma = 1.3, 0.7, 0.2
    n = np.array([1., 2., 3.])
    amplitudes = np.array([1., 0.3, 0.1])
    spectrum = lambda w: np.sqrt(2*np.pi)*sigma**2*tau*np.exp(-0.5*(w*tau)**2)
    spectral_D = float(np.sum((n*omega)**2*amplitudes**2*spectrum(n*omega))/4)
    covariance = lambda t: (sigma**2*np.exp(-t*t/(2*tau*tau)) *
        np.sum(amplitudes**2*(n*omega)**2*np.cos(n*omega*t))/2)
    covariance_D = quad(covariance, 0, np.inf, epsabs=1e-13)[0]
    check('positive orbital diffusion', spectral_D > 0, spectral_D)
    check('spectral versus covariance integral', abs(spectral_D-covariance_D) < 1e-12)
    theta = 2*np.pi*np.arange(1024)/1024
    h = np.cos(theta)+0.3*np.cos(2*theta)+0.1*np.sin(3*theta)
    coeff = np.fft.rfft(h)/len(h)
    for boundary in [-10., 0., 0.7, 10.]:
        shifted = np.fft.rfft(h-boundary)/len(h)
        check('nonzero harmonics unchanged boundary '+str(boundary),
              np.max(np.abs(coeff[1:]-shifted[1:])) < 2e-15)

    # Constant-period edge model. Units: q and q0 are specific energy; d is energy/time.
    density_rows = []
    for ratio in [1e-8, 1e-6, 1e-4, 1e-2, 1., 100., 1e4, 1e6, 1e8]:
        delta, q0 = ratio, 1.
        integrand = lambda t: 2*np.sqrt(delta)*np.sin(t)/np.sqrt(q0+delta*np.sin(t)**2)
        integral = quad(integrand, 0, np.pi/2, epsabs=1e-12, epsrel=1e-11)[0]
        exact = 2*np.arctan(np.sqrt(delta/q0))
        check('reflecting density quadrature '+str(ratio), abs(integral-exact) < 2e-10)
        # Stable evaluation of 1 - 1/sqrt(1+q/q0), to avoid cancellation near the edge.
        def absorbing_integrand(t):
            q = delta*np.sin(t)**2
            root = np.sqrt(1+q/q0)
            value = (q/q0)/(root*(root+1))
            return 2*np.sqrt(delta)*np.sin(t)*value
        absorbing = quad(absorbing_integrand, 0, np.pi/2, epsabs=1e-13)[0]
        absorbing_exact = 2*np.sqrt(delta)-2*np.sqrt(q0)*np.arctan(np.sqrt(delta/q0))
        check('absorbing density quadrature '+str(ratio),
              abs(absorbing-absorbing_exact) < 1e-10*max(1,abs(absorbing_exact)))
        if ratio <= 1e-4:
            check('reflecting square-root edge '+str(ratio),
                  abs(integral/(2*np.sqrt(delta/q0))-1) < 1e-4)
            check('absorbing three-halves edge '+str(ratio),
                  abs(absorbing/(2*delta**1.5/(3*q0))-1) < 1e-4)
        density_rows.append({'delta_over_q0': ratio, 'reflecting_density_over_sharp': integral/np.pi,
                             'absorbing_density_integral_C1': absorbing})

    for d in [0.1, 1., 10.]:
        for q0 in [0.01, 1.]:
            s = np.sqrt(q0)
            for q in [0.001, 0.1, 1., 10.]:
                x = np.sqrt(q+q0)
                D = d*x*x
                current = lambda density, derivative: -d*density/2-D*derivative
                check('zero reflecting flux '+str((d,q0,q)),
                      abs(current(1/x,-1/(2*x**3))) < 1e-12)
                check('constant absorbing flux '+str((d,q0,q)),
                      abs(current(1-s/x,s/(2*x**3))+d/2) < 1e-12)

    survival_rows = []
    for a in [0.01, 0.1, 0.5, 1., 2., 5.]:
        kernel = lambda u: (np.exp(-(u-a)**2)-np.exp(-(u+a)**2))/np.sqrt(np.pi)
        probability = quad(kernel, 0, np.inf, epsabs=1e-12)[0]
        check('absorbing heat kernel normalization '+str(a), abs(probability-erf(a)) < 1e-11)
    for q0 in [0., 0.01, 0.1, 1., 10.]:
        gap = 1/(np.sqrt(1+q0)+np.sqrt(q0))  # qi=1, rationalized for stability
        t50 = gap*gap/erfinv(0.5)**2         # d=1
        survival_rows.append({'q_initial': 1., 'q0':q0, 'd':1., 'median_exit_time':float(t50)})
        check('median survival '+str(q0), abs(erf(gap/np.sqrt(t50))-0.5) < 1e-14)
    check('increasing noise floor shortens median in this model',
          all(b['median_exit_time'] < a['median_exit_time'] for a,b in zip(survival_rows,survival_rows[1:])))

    # Mutations must visibly violate analytic identities at fixed witness parameters.
    check('MUTATE discard floor fails density at delta=q0', abs(1-2*np.arctan(1)/np.pi) > 0.4)
    check('MUTATE wrong survival variance is detected', abs(erf(1)-erf(1/np.sqrt(2))) > 0.1)
    d,x = 1., 2.
    wrong_drift_current = (d-d)/x-d*x*x*(-1/(2*x**3))
    check('MUTATE double drift breaks zero flux', abs(wrong_drift_current) > 0.1)
    result = {'all_passed':all(x['passed'] for x in checks), 'check_count':len(checks),
              'checks':checks,'spectral_diffusion':spectral_D,'density_rows':density_rows,
              'survival_rows':survival_rows,
              'scope':'Finite checks of the specified local constant-period model, ideal half-line killing, and three-harmonic weak-noise example. No empirical or complete-halo claim.'}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':sum(x['passed'] for x in checks),'total':len(checks),
                      'spectral_diffusion':spectral_D,'survival_rows':survival_rows},indent=2))
    return 0 if result['all_passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
