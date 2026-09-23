#!/usr/bin/env python3
"""Actual nonlinear deep-QUMOND source, angular projection and radial Green solve.

Compact spherical positive baryonic profiles. No Taylor expansion of nu is used.
Only the odd angular modes enter the reported axial force difference.
The retained angular modes and quadrature orders are finite, and are compared.
"""
import json
import math
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss, legval
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
rows = []
for strength, power in [(0.02, 2), (0.08, 2), (0.02, 4), (0.08, 4)]:
    coefficients = [(-1)**j*math.comb(power, j)/(2*j+3) for j in range(power+1)]
    normalization = sum(coefficients)

    def q_and_dq(r):
        if r >= 1:
            return strength/r**2, -2*strength/r**3
        mass = sum(c*r**(2*j+3) for j, c in enumerate(coefficients))/normalization
        dm = r*r*(1-r*r)**power/normalization
        return strength*mass/r**2, strength*(dm/r**2-2*mass/r**3)

    for angular_order, lmax in [(32, 5), (64, 7), (96, 9)]:
        # Integrate odd part on positive cos(theta), avoiding cancellation of
        # the much larger even source. ge_N=1; nu(n)=n^-1/2; ge=nu_e=1.
        nodes0, weights0 = leggauss(angular_order)
        nodes, weights = (nodes0+1)/2, weights0/2
        radial_order = angular_order*2
        radial_nodes, radial_weights = leggauss(radial_order)
        legs = {ell: legval(nodes, [0]*ell+[1]) for ell in range(1, lmax+1, 2)}

        def source_mode(r, ell):
            q, dq = q_and_dq(r)
            base_minus = 1+q*q-2*q*nodes
            logratio = np.log1p(4*q*nodes/base_minus)
            nu_diff = base_minus**(-0.25)*np.expm1(-0.25*logratio)
            w_diff = base_minus**(-1.25)*np.expm1(-1.25*logratio)
            w_sum = base_minus**(-1.25)*(2+np.expm1(-1.25*logratio))
            lap_n = dq+2*q/r
            even_hessian_contraction = dq*(q*q+nodes*nodes)+q/r*(1-nodes*nodes)
            source_difference = lap_n*nu_diff-0.5*(even_hessian_contraction*w_diff
                                                        +2*q*dq*nodes*w_sum)
            return (2*ell+1)/2*float(np.dot(weights, source_difference*legs[ell]))

        def integral(func, lo, hi):
            xs = lo+(hi-lo)*(radial_nodes+1)/2
            return (hi-lo)/2*float(np.dot(radial_weights, [func(float(x)) for x in xs]))

        interior = {ell: integral(lambda x: x**(ell+2)*source_mode(x, ell), 0, 1)
                    for ell in legs}

        def asymmetry(r):
            answer = 0.0
            for ell in legs:
                inside = interior[ell]+integral(
                    lambda u: math.exp((ell+3)*u)*source_mode(math.exp(u), ell), 0, math.log(r))
                # The u=1/x transform places the infinite tail on a finite
                # interval and keeps its small value at explicit precision.
                outside_scaled = r*integral(lambda u: u**(ell-3)*source_mode(r/u, ell), 0, 1)
                derivative = ((ell+1)*inside/r**(ell+2)-ell*outside_scaled)/(2*ell+1)
                answer -= derivative
            return answer

        radii = [4.0, 8.0, 16.0, 32.0, 64.0, 128.0]
        a = {r: asymmetry(r) for r in radii}
        for r in radii[:4]:
            n2 = 2*r**4/(3*strength**2)*(a[r]-8*a[2*r])
            n3 = -2*r**4/(3*strength**2)*(a[r]-40*a[2*r]+256*a[4*r])
            rows.append(dict(strength=strength, density_power=power,
                             angular_order=angular_order, lmax=lmax, r=r,
                             radial_quadrature_order=radial_order,
                             two_radius=n2, three_radius=n3,
                             target=0.5, error=n3-0.5))

for strength, power in [(0.02, 2), (0.08, 2), (0.02, 4), (0.08, 4)]:
    selected = [x for x in rows if x['strength'] == strength and x['density_power'] == power]
    fine = [x for x in selected if x['angular_order'] == 96]
    assert abs(fine[-1]['error']) < 1e-6, fine[-1]
    assert abs(fine[-1]['error']) < abs(fine[0]['error'])/30, fine
    at_large_r = [x['three_radius'] for x in selected if x['r'] == 32]
    assert max(at_large_r)-min(at_large_r) < 1e-7, at_large_r

result = {'status': 'nonlinear deep-QUMOND finite-mode Green solve verified within stated bounds',
          'cases': rows, 'case_count': len(rows),
          'largest_radius_max_error': max(abs(x['error']) for x in rows if x['r'] == 32),
          'source': 'rho proportional to (1-r^2)^p on 0<=r<1, p=2 or 4; zero outside',
          'units': 'G=ge_N=nu_e=ge=1; total baryonic mass=0.02 or 0.08',
          'nu': 'n^(-1/2), evaluated exactly rather than Taylor expanded',
          'bounds': {'angular_quadrature_orders': [32, 64, 96], 'odd_lmax': [5, 7, 9],
                     'radial_quadrature_orders': [64, 128, 192],
                     'estimator_radii': [4, 8, 16, 32], 'force_radii': [4, 8, 16, 32, 64, 128]},
          'non_claims': ['No global nonlinear AQUAL solve', 'No exact infinite-mode error bound',
                         'No observational validation']}
(OUT/'global_qumond.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'case_count': len(rows), 'largest_radius_max_error': result['largest_radius_max_error']}, indent=2))
