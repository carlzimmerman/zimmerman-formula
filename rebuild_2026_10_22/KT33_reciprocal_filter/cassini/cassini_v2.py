#!/usr/bin/env python3
"""Fixed-width reciprocal Gaussian Cassini calculation; import-safe, no refits.

Dimensionless r is in r_M=sqrt(GM/a0). q_hessian_signed is the signed STF zz Hessian
in a0/r_M units; the archived KT16/KT25 convention is Q2=3 q a0/(2 r_M).
Both an integrated flux kernel and analytic phantom-density Hessian are used.
See README.md for the derivation and finite-domain surface term.
"""
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import numpy as np
from scipy.special import erf, gammainc

GM = 6.6743e-11 * 1.98892e30
GEXT = 2.32e-10
CEILING = 5.2e-27
A0 = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}
AU = 1.495978707e11
EPS = 0.5
SQRT2PI = math.sqrt(2 / math.pi)


def gaussian_field(r, sigma):
    """Newton gradient magnitude for a unit normalized Gaussian source."""
    r = np.asarray(r, dtype=float)
    if sigma == 0:
        return 1 / r**2
    if sigma < 0:
        raise ValueError('Gaussian sigma must be nonnegative')
    # Regularized gamma form equals erf(x/sqrt2)-sqrt(2/pi)x exp(-x²/2),
    # and avoids catastrophic cancellation at small x.
    return gammainc(1.5, 0.5 * (r / sigma)**2) / r**2


def kernel_weight(r, sigma):
    """r³(f''-f'/r)/3, f=erf(r/(sqrt2 sigma))/r; sigma=0 is 1/r."""
    r = np.asarray(r, dtype=float)
    if sigma == 0:
        return np.ones_like(r)
    if sigma < 0:
        raise ValueError('Gaussian sigma must be nonnegative')
    return gammainc(2.5, 0.5 * (r / sigma)**2)


def kernel_weight_prime(r, sigma):
    r = np.asarray(r, dtype=float)
    if sigma == 0:
        return np.zeros_like(r)
    x = r / sigma
    return SQRT2PI * np.exp(-0.5 * x*x) * x**4 / (3 * sigma)


def nu_minus_one(h):
    # Rationalized simple nu-1, stable at arbitrarily large positive field.
    h = np.maximum(h, np.finfo(float).tiny)
    return 1 / (h * (np.sqrt(0.25 + 1 / h) + 0.5))


@lru_cache(maxsize=None)
def angular_rule(nm):
    return np.polynomial.legendre.leggauss(nm)


def inner_surface_limit(eta, sigma_source, sigma_outer):
    """Analytic r->0 lower surface for fixed eta>0; vanishes if outer>0."""
    if sigma_source == 0 or sigma_outer > 0 or eta == 0:
        return 0.
    c = SQRT2PI/(3*sigma_source**3)
    return -2*c/(15*eta*math.sqrt(.25+1/eta))


def quadrupole(eta, sigma_source, sigma_outer, nr=20000, nm=200,
               rmin=1e-7, rmax=1e5, newtonian=False):
    """Compute signed q by flux and density routes with the same finite domain.

    A radial reference is subtracted before each angular sum: its polynomial
    integral vanishes exactly. This suppresses cancellation at tiny/large r.
    Memory is bounded by a 256-by-nm chunk, not nr-by-nm matrices.
    """
    if eta < 0 or min(sigma_source, sigma_outer) < 0 or rmin <= 0 or rmax <= rmin:
        raise ValueError('Invalid domain or Gaussian width')
    log_r = np.linspace(math.log(rmin), math.log(rmax), nr)
    r = np.exp(log_r)
    mu, w = angular_rule(nm)
    mu = mu[None, :]
    p = 3*mu*mu-1
    f1 = np.zeros(nr)
    f2 = np.zeros(nr)
    fd = np.zeros(nr)
    surface = np.zeros(nr)
    for start in range(0, nr, 256):
        sl = slice(start, min(start+256,nr))
        rr = r[sl, None]
        g = gaussian_field(rr, sigma_source)
        divg = np.zeros_like(rr) if sigma_source == 0 else SQRT2PI*np.exp(-.5*(rr/sigma_source)**2)/sigma_source**3
        gp = divg - 2*g/rr
        h = np.sqrt((g+eta*mu)**2 + eta*eta*(1-mu*mu))
        h0 = np.hypot(g, eta)
        if newtonian:
            aa = np.zeros_like(h)
            dd = np.zeros_like(h)
        else:
            a = nu_minus_one(h)
            a0 = nu_minus_one(h0)
            aa = a-a0
            dn = -0.5/(h*h*np.sqrt(.25+1/h))
            dn0 = -0.5/(h0*h0*np.sqrt(.25+1/h0))
            d = a*divg + (dn/h)*(gp*(g+eta*mu)**2 + eta*eta*g*(1-mu*mu)/rr)
            d0 = a0*divg + (dn0/h0)*(gp*g*g + eta*eta*g/rr)
            dd = d-d0
        t = kernel_weight(rr[:,0], sigma_outer)
        tp = kernel_weight_prime(rr[:,0], sigma_outer)
        b = (aa*(eta*(3*mu-5*mu**3)+g*(1-3*mu*mu))) @ w
        c = (aa*(g+eta*mu)*p) @ w
        dp = (dd*p) @ w
        f1[sl] = 1.5*t*b/r[sl]
        f2[sl] = 0.5*tp*c
        fd[sl] = -0.5*t*dp
        surface[sl] = .5*t*c/r[sl]
    q1 = float(np.trapz(f1, log_r))
    q2 = float(np.trapz(f2, log_r))
    qd = float(np.trapz(fd, log_r))
    boundary = float(surface[-1]-surface[0])
    q = q1+q2
    return dict(q_flux_signed=q, q_hessian_signed=q-boundary, q_density_signed=qd, weighted_old_term=q1,
                gaussian_derivative_term=q2, boundary_term=boundary,
                analytic_inner_surface=0. if newtonian else inner_surface_limit(eta,sigma_source,sigma_outer),
                flux_density_difference=q-boundary-qd,
                sigma_source=sigma_source, sigma_outer=sigma_outer,
                nr=nr, nm=nm, rmin=rmin, rmax=rmax)


def legacy_source_only(eta, xi=EPS, nr=20000, nm=200):
    """Literal KT25 integrand, stable chunking only; retains signed output."""
    u = np.linspace(math.log(1e-7), math.log(1e5), nr)
    r = np.exp(u)
    mu, w = angular_rule(nm)
    mm = mu[None,:]
    f = np.zeros(nr)
    for start in range(0,nr,256):
        sl = slice(start,min(start+256,nr))
        rr = r[sl]
        x = rr/xi
        g = np.empty_like(rr)
        small = x < 1e-3
        g[~small] = (erf(x[~small]/math.sqrt(2))-SQRT2PI*x[~small]*np.exp(-x[~small]**2/2))/rr[~small]**2
        g[small] = SQRT2PI/3*rr[small]/xi**3
        g = g[:,None]
        a = .5+np.sqrt(.25+1/np.maximum(np.sqrt(eta*eta+g*g+2*eta*g*mm),1e-300))-1
        f[sl] = (a*(eta*(3*mm-5*mm**3)+g*(1-3*mm*mm)))@w
    return 1.5*float(np.trapz(f/r,u))


def physical(out, a0):
    rm = math.sqrt(GM/a0)
    pref = 1.5*a0/rm
    out = dict(out)
    out.update(Q2_signed_s_minus_2=out['q_hessian_signed']*pref,
               Q2_abs_s_minus_2=abs(out['q_hessian_signed'])*pref,
               x_ceiling=abs(out['q_hessian_signed'])*pref/CEILING,
               cassini_pass=abs(out['q_hessian_signed'])*pref <= CEILING)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    archive = json.loads((root/'rebuild_2026_10_22/KT25_eps_equals_kappa/kt25.json').read_text())
    presets = [('baseline',dict(nr=20000,nm=200)),
               ('double_resolution',dict(nr=40000,nm=400)),
               ('expanded_domain',dict(nr=40000,nm=400,rmin=1e-8,rmax=1e6)),
               ('angular_refinement',dict(nr=40000,nm=800,rmin=1e-8,rmax=1e6))]
    results = dict(operator='Phi_N[rho] + S Phi_ph[S rho]',
                   conventions='fixed Gaussian sigma; q_hessian_signed is STF zz Hessian; Q2_signed=1.5 a0/rM q_hessian_signed; q_flux_signed retains historical by-parts integral before its boundary correction',
                   constants=dict(GM=GM,GEXT=GEXT,ceiling=CEILING,eps=EPS,a0=A0),
                   footings={}, checks={})
    checks = results['checks']
    for foot,a0 in A0.items():
        eta = GEXT/a0
        rm = math.sqrt(GM/a0)
        rows = results['footings'][foot] = dict(a0=a0,eta=eta,rM_AU=rm/AU,xi_AU=EPS*rm/AU,arms={})
        for arm,source,outer in [('plain_qumond',0.,0.),('source_only_hessian',EPS,0.),('reciprocal',EPS,EPS)]:
            rows['arms'][arm] = {name:physical(quadrupole(eta,source,outer,**params),a0) for name,params in presets}
            series = rows['arms'][arm]
            best = series['angular_refinement']
            print(foot,arm,'q_hessian_signed',best['q_hessian_signed'],'Q2_signed',best['Q2_signed_s_minus_2'],'x_ceiling',best['x_ceiling'],flush=True)
            shifts = {name:abs(row['q_hessian_signed']/best['q_hessian_signed']-1) for name,row in series.items()}
            checks[f'{foot}|{arm}|refinement'] = dict(passed=max(shifts.values())<1e-3,relative_to_finest=shifts,tolerance=1e-3)
            disagreements = {name:abs(row['flux_density_difference']) for name,row in series.items()}
            checks[f'{foot}|{arm}|independent_density'] = dict(passed=disagreements['angular_refinement']<2e-5,absolute_q_difference=disagreements,tolerance=2e-5)
        old = legacy_source_only(eta)
        old_abs = archive[f'cassini|{foot}|0.5']['q']
        rows['legacy_source_only_flux_control'] = dict(q_flux_signed=old,Q2_flux_signed_s_minus_2=1.5*a0/rm*old,x_ceiling=1.5*a0/rm*abs(old)/CEILING,archived_x_ceiling=archive[f'cassini|{foot}|0.5']['x_ceiling'],note='Reproduces KT25 integral, which omits the nonzero inner boundary for a smooth source; not the physical source-only Hessian.')
        checks[f'{foot}|archived_source_only'] = dict(passed=abs(abs(old)-old_abs)<2e-10,absolute_error=abs(abs(old)-old_abs),archived_q_abs=old_abs,new_literal_q_signed=old)
        stable = rows['arms']['source_only_hessian']['baseline']['q_flux_signed']
        checks[f'{foot}|stable_vs_legacy_source'] = dict(passed=abs(stable-old)<2e-8,absolute_error=abs(stable-old),tolerance=2e-8)
        controls = {}
        for arm,source,outer in [('plain',0.,0.),('source_only_hessian',EPS,0.),('reciprocal',EPS,EPS)]:
            controls[arm] = quadrupole(eta,source,outer,nr=1000,nm=40,newtonian=True)
        rows['newtonian_controls'] = controls
        checks[f'{foot}|nu_equals_one'] = dict(passed=all(c['q_hessian_signed']==c['q_density_signed']==0 for c in controls.values()))
        zero = quadrupole(eta,0.,0.)
        checks[f'{foot}|zero_width'] = dict(passed=zero=={k:v for k,v in rows['arms']['plain_qumond']['baseline'].items() if k in zero},q_hessian_signed=zero['q_hessian_signed'])
        spherical = quadrupole(0.,EPS,EPS,nr=1000,nm=40)
        checks[f'{foot}|zero_external_field'] = dict(passed=max(abs(spherical['q_hessian_signed']),abs(spherical['q_density_signed']))<1e-14,q_hessian_signed=spherical['q_hessian_signed'],q_density_signed=spherical['q_density_signed'],tolerance=1e-14)
    results['all_checks_pass'] = all(row['passed'] for row in checks.values())
    results['outcome'] = 'conditional on numerical tolerances; finite Cassini diagnostic only'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(results,indent=2,allow_nan=False)+'\n')
    print('all_checks_pass',results['all_checks_pass'],flush=True)
    if not results['all_checks_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
