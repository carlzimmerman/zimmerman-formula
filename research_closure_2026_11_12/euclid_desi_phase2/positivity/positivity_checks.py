"""Scoped spherical positivity checks; no observational likelihood fitted."""
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / 'input.json').read_text())
G = DATA['constants']['G']
MSUN = DATA['constants']['Msun']
KPC = DATA['constants']['kpc']
R = np.asarray(DATA['values']['R_D'], dtype=float) * KPC
M = np.asarray(DATA['values']['M_D'], dtype=float) * 1e11 * MSUN
ERR_LOW = np.asarray(DATA['values']['M_EL'], dtype=float) * 1e11 * MSUN
ERR_HIGH = np.asarray(DATA['values']['M_EH'], dtype=float) * 1e11 * MSUN


def baryon_mass(radius, mass_dynamic, acceleration, law):
    gravity = G * mass_dynamic / radius**2
    if law == 'simple_mu':
        gb = gravity**2 / (gravity + acceleration)
    else:
        # Rationalized positive root avoids subtraction at large acceleration.
        gb = 2 * gravity**2 / (np.sqrt(acceleration**2 + 4*gravity**2) + acceleration)
    return radius**2 * gb / G


def dynamic_mass(radius, mass_baryon, acceleration, law):
    gb = G * mass_baryon / radius**2
    gravity = ((gb + np.sqrt(gb**2 + 4*acceleration*gb))/2 if law == 'simple_mu'
               else np.sqrt(gb**2 + acceleration*gb))
    return radius**2 * gravity / G


def interval_witness(acceleration, expansion, law):
    ml = np.maximum(M - expansion*ERR_LOW, np.finfo(float).tiny)
    mu = M + expansion*ERR_HIGH
    lower = baryon_mass(R, ml, acceleration, law)
    upper = baryon_mass(R, mu, acceleration, law)
    chosen = np.maximum.accumulate(lower)
    gap = chosen - upper
    feasible = bool(np.max(gap) <= 1e-12 * float(np.max(M)))
    recovered = dynamic_mass(R, chosen, acceleration, law)
    return dict(feasible=feasible,
                largest_positive_baryon_interval_gap_Msun=float(max(0, np.max(gap))/MSUN),
                witness_baryon_Msun=(chosen/MSUN).tolist() if feasible else None,
                witness_dynamic_Msun=(recovered/MSUN).tolist() if feasible else None,
                witness_monotone=bool(np.all(np.diff(chosen) >= 0)),
                witness_in_box=bool(np.all(recovered >= ml-1e-12*M) and
                                    np.all(recovered <= mu+1e-12*M)) if feasible else None)


def minimum_expansion(acceleration, law):
    lo, hi = 0., 8.
    if interval_witness(acceleration, lo, law)['feasible']:
        return 0.
    if not interval_witness(acceleration, hi, law)['feasible']:
        return None
    for _ in range(70):
        mid = (lo+hi)/2
        if interval_witness(acceleration, mid, law)['feasible']:
            hi = mid
        else:
            lo = mid
    return hi


def main(outdir):
    r, a, slope = sp.symbols('r a s', positive=True)
    gf = sp.Function('g')(r)
    mb = r*r*gf*gf/(gf+a)
    derivative = sp.diff(mb, r).subs(sp.diff(gf, r), slope*gf/r)
    symbolic = {
        'simple_density_sign': sp.simplify(derivative-r*gf**2*((2+slope)*gf+2*(1+slope)*a)/(gf+a)**2) == 0,
    }
    x = sp.symbols('x', positive=True)
    t = sp.symbols('t', positive=True)
    # At local bound use s=-1-t, 0<t<1. Quadratic: a/g=(1-t)/sqrt(t).
    abound = (1-t)/sp.sqrt(t)
    gb_over_g = sp.sqrt(t)
    symbolic['quadratic_bound_force_relation'] = sp.simplify(gb_over_g**2+abound*gb_over_g-1) == 0
    symbolic['quadratic_bound_zero_mass_slope'] = sp.simplify((1-t)*gb_over_g-t*abound) == 0
    # Both limiting flat-force profiles retain nonnegative density for arbitrary a.
    symbolic['simple_flat_force_positive'] = sp.simplify((2+slope)*x+2*(1+slope)).subs(slope,-1) == x

    mass1, mass2, g1, g2 = sp.symbols('M1 M2 g1 g2', positive=True)
    difference = mass2*g2/(g2+a)-mass1*g1/(g1+a)
    symbolic['simple_finite_shell_identity'] = sp.simplify(difference*(g1+a)*(g2+a) -
        (g1*g2*(mass2-mass1)+a*(mass2*g2-mass1*g1))) == 0

    pairs = []
    finite_crossing_residuals = []
    for i in range(len(R)):
        for j in range(i+1, len(R)):
            g1n, g2n = G*M[i]/R[i]**2, G*M[j]/R[j]**2
            record = {'i':i,'j':j,'r_kpc':[float(R[i]/KPC),float(R[j]/KPC)]}
            if M[j] > M[i] and M[j]/R[j] < M[i]/R[i]:
                asc = g1n*g2n*(M[j]-M[i])/(M[i]*g1n-M[j]*g2n)
                meq = math.sqrt((M[i]**2*R[j]**2-M[j]**2*R[i]**2)/(R[j]**2-R[i]**2))
                aq = g1n*(M[i]/meq-meq/M[i])
                record.update(simple_mu_bound=asc,quadratic_bound=aq)
                for law, bound in [('simple_mu',asc),('quadratic',aq)]:
                    masses = baryon_mass(R[[i,j]], M[[i,j]], bound, law)
                    finite_crossing_residuals.append(float(abs(masses[1]-masses[0])/max(masses)))
                    below = baryon_mass(R[[i,j]],M[[i,j]],bound*0.99,law)
                    above = baryon_mass(R[[i,j]],M[[i,j]],bound*1.01,law)
                    if not (below[1]>=below[0] and above[1]<above[0]):
                        raise AssertionError('Finite-shell crossing sign failed')
            else:
                record.update(simple_mu_bound=None,quadratic_bound=None)
            pairs.append(record)

    rows=[]
    for law in ['simple_mu','quadratic']:
        for accel in [9.36e-11,1.13e-10]:
            inferred = baryon_mass(R,M,accel,law)
            boxes = {str(v):interval_witness(accel,v,law) for v in [0,0.5,1,2]}
            rows.append(dict(law=law,a0=accel,central_baryon_Msun=(inferred/MSUN).tolist(),
                             central_decreasing_shell_indices=np.flatnonzero(np.diff(inferred)<0).tolist(),
                             minimum_marginal_interval_expansion=minimum_expansion(accel,law),boxes=boxes))
            assert all(not x['feasible'] or x['witness_in_box'] for x in boxes.values())

    # Orthogonal finite witness: in the isolated flat-speed family, both the
    # acceleration and all no-slip metric observables stay fixed as a varies.
    rr=np.geomspace(.1,100,100);v2=2.
    flatchecks=[]
    for aa in [.01,.1,1.,10.,100.]:
        mass=v2*v2*rr/(v2+aa*rr) # G=1
        gb=mass/rr**2
        rebuilt=(gb+np.sqrt(gb**2+4*aa*gb))/2
        flatchecks.append(dict(a0=aa,max_relative_g_error=float(np.max(abs(rebuilt/(v2/rr)-1))),
                               positive_density=bool(np.all(v2**3/(v2+aa*rr)**2>0))))
    result=dict(assertion_tested='Scoped positive-baryon necessary conditions and marginal-box feasibility; not a likelihood or theory exclusion.',
                symbolic_checks={k:bool(v) for k,v in symbolic.items()},
                finite_pairs=pairs,maximum_finite_crossing_relative_residual=max(finite_crossing_residuals),
                rows=rows,flat_family=flatchecks,
                caveats=['Spherical isolated algebraic laws only; EFE invalidates inversion.',
                         'DESI proxy profile carries tracer/model/calibration assumptions and unavailable radial covariance.',
                         'Marginal interval expansion is a deterministic feasibility measure, not sigma or p-value.',
                         'A feasible monotone baryon profile is not an independently observed stellar/gas distribution.',
                         'Positivity constrains physical baryons here, not effective phantom source density.'])
    assert all(symbolic.values())
    assert result['maximum_finite_crossing_relative_residual'] < 1e-12
    assert all(x['max_relative_g_error']<1e-12 and x['positive_density'] for x in flatchecks)
    out=ROOT/outdir;out.mkdir(exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('symbolic',len(symbolic),'pairs',len(pairs),'rows',len(rows))
    for row in rows:print(row['law'],row['a0'],row['minimum_marginal_interval_expansion'],row['central_decreasing_shell_indices'])


if __name__=='__main__':
    main(sys.argv[1])
