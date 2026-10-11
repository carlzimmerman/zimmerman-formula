"""Orbit-average capture from a bounded 3D incoming DF in a prescribed source.

Spherical orientation averaging is exact; (r,E,mu) are quadrature sampled.
No target density enters evolution or weights. G=M=1, final Plummer b=.05.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from scipy.special import beta
from numpy.polynomial.legendre import leggauss

BI, BF, RESERVOIR = .5, .05, .001
CHECKS = []


def check(name, passed, value=None):
    CHECKS.append(dict(name=name, passed=bool(passed), value=value))


def gauss(n, lo, hi):
    x, w = leggauss(n)
    return lo+(hi-lo)*(x+1)/2, w*(hi-lo)/2


def incoming(n):
    r, wr = gauss(n, 1.5, 2.5)
    e, we = gauss(n, .02, .8)
    s, ws = gauss(4*n, 0., 1.)
    rr, ee, ss = np.meshgrid(r, e, s, indexing='ij')
    rw, ew, sw = np.meshgrid(wr, we, ws, indexing='ij')
    rr, ee, ss = rr.ravel(), ee.ravel(), ss.ravel()
    v = np.sqrt(2*(ee+1/np.sqrt(rr*rr+BI*BI)))
    mu = ss*ss-1
    # d^3x d^3v = 8 pi^2 r^2 v dr dE dmu; dmu=2s ds.
    volumes = 8*np.pi**2*rr*rr*v*(rw*ew*sw).ravel()*2*ss
    def radial_volume(x):
        potential_depth = 1/np.sqrt(x*x+BI*BI)
        return x*x*(2*np.sqrt(2)/3)*((.8+potential_depth)**1.5-(.02+potential_depth)**1.5)
    full_volume = 8*np.pi**2*quad(radial_volume, 1.5, 2.5, epsabs=1e-11, epsrel=1e-12)[0]
    fmax = RESERVOIR/full_volume
    weights = volumes*fmax
    z = np.column_stack((rr, np.zeros(len(rr)), v*mu,
                         v*np.sqrt(1-mu*mu), np.zeros(len(rr))))
    return z, weights, float(fmax), ee


def shape(t, duration):
    u = np.clip(t/duration, 0., 1.)
    return BI+(BF-BI)*(3*u*u-2*u*u*u), (BF-BI)*6*u*(1-u)/duration


def evolve(z, duration, refined=False):
    def rhs(t, flat):
        q = flat.reshape(-1, 5)
        b, bd = shape(t, duration)
        den = (np.sum(q[:, :2]**2, axis=1)+b*b)**1.5
        out = np.column_stack((q[:, 2:4], -q[:, :2]/den[:, None], b*bd/den))
        return out.ravel()
    sol = solve_ivp(rhs, (0., duration), z.ravel(), method='DOP853',
                    rtol=2e-12 if refined else 1e-10,
                    atol=2e-14 if refined else 1e-12,
                    max_step=.01 if refined else .02)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[:, -1].reshape(-1, 5)


def orbit(energy, angular, b, edges, order=96):
    """Radial probability CDF, with both integrable endpoint singularities removed."""
    j2 = angular*angular
    def v2(r):
        return 2*(energy+1/np.sqrt(r*r+b*b))-j2/(r*r)
    hi = max(1., 2*j2)
    while hi**4/(hi*hi+b*b)**1.5 < j2:
        hi *= 2
    rc = brentq(lambda r: r**4/(r*r+b*b)**1.5-j2, 1e-15, hi, xtol=1e-14)
    assert v2(rc) > 0
    rp = brentq(v2, 1e-15, rc, xtol=1e-14)
    ra = brentq(v2, rc, -1/energy*(1+1e-10), xtol=1e-14)
    mid, half = (ra+rp)/2, (ra-rp)/2
    nodes, weights = leggauss(order)
    def integral(theta):
        if theta == 0:
            return 0.
        q = (nodes+1)*theta/2
        radii = rp+half*(1-np.cos(q))
        speed2 = v2(radii)
        if np.any(speed2 <= 0):
            raise ArithmeticError('Nonpositive radial speed at interior quadrature point')
        return float(np.sum(weights*half*np.sin(q)/np.sqrt(speed2))*theta/2)
    denom = integral(np.pi)
    cdf = []
    for radius in edges:
        if radius <= rp:
            cdf.append(0.)
        elif radius >= ra:
            cdf.append(1.)
        else:
            theta = np.arccos(np.clip((mid-radius)/half, -1., 1.))
            cdf.append(integral(theta)/denom)
    return np.array(cdf), dict(peri=float(rp), apo=float(ra), period=float(2*denom))


def target_mass(radii, repaired):
    # Same log-tail definition as orbit_selection/check.py, implemented locally.
    yp = brentq(lambda y: np.expm1(np.sqrt(y))-.5*np.sqrt(y)*np.exp(np.sqrt(y)), 1., 10.)
    def h(y):
        return y/np.expm1(np.sqrt(y))
    def hp(y):
        x = np.sqrt(y)
        return 1/np.expm1(x)-.5*x*np.exp(x)/np.expm1(x)**2
    coefficient = h(yp)/20
    ys = brentq(lambda y: hp(y)-coefficient/(y+yp), 1., yp)
    r = np.asarray(radii)
    mb = r**3/(r*r+BF*BF)**1.5
    y = mb/(r*r)  # a0=1 only for a declared diagnostic overlay.
    excess = 1/np.expm1(np.sqrt(y))
    if repaired:
        tail = (h(ys)+coefficient*np.log((y+yp)/(ys+yp)))/y
        excess = np.where(y <= ys, excess, tail)
    return mb*excess


def cell(n, duration, edges, refined=False):
    z, weights, fmax, ein = incoming(n)
    out = evolve(z, duration, refined)
    e = .5*np.sum(out[:, 2:4]**2, axis=1)-1/np.sqrt(np.sum(out[:, :2]**2, axis=1)+BF*BF)
    j = z[:, 0]*z[:, 3]
    jf = out[:, 0]*out[:, 3]-out[:, 1]*out[:, 2]
    error = float(np.max(np.abs(e-ein-out[:, 4])))
    name = f'n{n}_T{duration}'
    check(name+'_work', error < 1e-7, error)
    jerr = float(np.max(np.abs(j-jf)))
    check(name+'_j', jerr < 1e-7, jerr)
    check(name+'_mass_quadrature', abs(np.sum(weights)-RESERVOIR)<1e-8,
          float(abs(np.sum(weights)-RESERVOIR)/RESERVOIR))
    captured = e < -1e-7
    masses = [np.zeros(len(edges)), np.zeros(len(edges))]
    records = []
    for k in np.flatnonzero(captured):
        base, rec = orbit(e[k], j[k], BF, edges, 96)
        fine, _ = orbit(e[k], j[k], BF, edges, 192)
        masses[0] += weights[k]*base
        masses[1] += weights[k]*fine
        records.append(dict(energy=float(e[k]), angular=float(j[k]), mass=float(weights[k]), **rec))
    total = float(np.sum(weights[captured]))
    discrepancy = float(np.max(np.abs(masses[0]-masses[1]))/max(total, 1e-30))
    check(name+'_radial_quadrature', discrepancy < 2e-5, discrepancy)
    check(name+'_cdf_monotone', np.all(np.diff(masses[1]) >= -1e-15))
    check(name+'_cdf_mass_bound', np.all(masses[1] <= total+1e-15))
    # Normalized annular shape comparison removes only an amplitude for diagnosis.
    # It does not fit a0 or claim a dynamically self-consistent target halo.
    shape_scores = {}
    mask = (edges >= .05) & (edges <= .4)
    observed = masses[1][mask]
    if observed[-1] > observed[0]:
        observed_shape = (observed-observed[0])/(observed[-1]-observed[0])
        for label, repaired in [('exponential', False), ('repaired', True)]:
            mt = target_mass(edges[mask], repaired)
            target_shape = (mt-mt[0])/(mt[-1]-mt[0])
            shape_scores[label] = dict(max_cdf_difference=float(np.max(np.abs(observed_shape-target_shape))),
                                       normalized_target=target_shape.tolist(),
                                       normalized_observed=observed_shape.tolist(),
                                       target_is_monotone=bool(np.all(np.diff(mt)>=0)))
    return dict(n=n, duration=duration, parcels=len(z), fmax=fmax,
                captured_parcels=int(np.sum(captured)), captured_mass=total,
                captured_fraction=total/RESERVOIR, work_error=error, angular_error=jerr,
                minimum_abs_energy=float(np.min(np.abs(e))), mass_below= masses[1].tolist(),
                radial_quadrature_relative_error=discrepancy, shape_scores=shape_scores,
                orbits=records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    # Kepler radial time measure is independently known from eccentric anomaly.
    radii = np.array([.4, .5, .8, 1., 1.4, 1.6])
    cdf, rec = orbit(-.5, .8, 0., radii, 192)
    anomaly = np.arccos(np.clip((1-radii)/.6, -1., 1.))
    exact = (anomaly-.6*np.sin(anomaly))/np.pi
    check('kepler_period', abs(rec['period']-2*np.pi)<1e-7, rec['period'])
    check('kepler_cdf', float(np.max(np.abs(cdf-exact))) < 1e-7)
    check('uniform_anomaly_wrong_measure_rejected', np.max(np.abs(anomaly/np.pi-exact))>.1)
    # Independent positive Abel reconstruction of the required endpoint powers.
    endpoint = []
    for gamma in (.25, 1/3):
        p = 1.5+gamma
        norm = 1/(4*np.pi*np.sqrt(2)*beta(1.5, gamma))
        for delta in (1e-4, 1e-8):
            # epsilon in [0,1-delta], t=(Psi-epsilon)/delta.
            upper = (1-delta)/delta
            # t=u/(1-u), keeping the endpoint near infinity well conditioned.
            cap = upper/(1+upper)
            integ = quad(lambda u: u**.5*(1-u)**(gamma-1), 0., cap,
                         epsabs=1e-10, epsrel=1e-10)[0]
            ratio = 4*np.pi*np.sqrt(2)*norm*integ
            endpoint.append(dict(gamma=gamma, delta=delta, rho_to_leading_ratio=ratio))
        check('abel_endpoint_'+str(gamma), abs(endpoint[-1]['rho_to_leading_ratio']-1)<.015,
              endpoint[-1]['rho_to_leading_ratio'])
    edges = np.array([.01,.02,.03,.05,.07,.1,.14,.2,.28,.4,.6,1.,2.,4.,8.,16.,32.,64.,128.])
    rows = []
    for duration in (2., 8.):
        for n in (4, 6):
            row = cell(n, duration, edges)
            rows.append(row)
            print('cell', n, duration, row['captured_fraction'], row['shape_scores'], flush=True)
    ref = cell(4, 2., edges, refined=True)
    orig = rows[0]
    check('integrator_capture_mass', abs(ref['captured_mass']-orig['captured_mass'])<1e-12)
    check('integrator_profile', np.max(np.abs(np.array(ref['mass_below'])-orig['mass_below']))<1e-9)
    result = dict(base_revision='a5e6e3696c2fe80dfcd1932c633f371f4b08d3c1',
                  incoming_df='constant f0 on r in[1.5,2.5], E in[.02,.8], inward velocity hemisphere; zero elsewhere',
                  reservoir_mass=RESERVOIR, edges=edges.tolist(),
                  target_exponential=target_mass(edges, False).tolist(),
                  target_repaired=target_mass(edges, True).tolist(), cells=rows,
                  refined=ref, abel_checks=endpoint, checks=CHECKS,
                  assertions=len(CHECKS), passed=sum(c['passed'] for c in CHECKS))
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print('checks', result['passed'], '/', result['assertions'])
    raise SystemExit(0 if result['passed']==result['assertions'] else 1)


if __name__ == '__main__':
    main()
