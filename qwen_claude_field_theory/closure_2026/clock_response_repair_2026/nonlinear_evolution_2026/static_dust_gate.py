#!/usr/bin/env python3
"""Exact stationary-matter gate from the SAME minimally coupled dust action.

Stationarity of the conserved density makes radial flux constant; a regular
center makes that constant zero. Positive density, lapse and metric then force
zero radial velocity. The independently varied momentum equation forces N'=0.
This excludes a static single-stream spherical dust galaxy, not a rotating or
velocity-dispersed baryonic galaxy and not all solutions of the clock action.
"""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sympy as s


def derive():
    path=Path(__file__).resolve().parent.parent/'spherical_baryon_bridge/action/matter.py'
    spec=importlib.util.spec_from_file_location('varied_dust_gate',path)
    m=importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(m)
    N,A,R,rho,w,Nr=s.symbols('N A R rho w Nr',positive=True)
    # Use a free signed radial velocity rather than the positive placeholder.
    w=s.symbols('w',real=True)
    replacement={m.N:N,m.A:A,m.R:R,m.rho:rho,m.q:w,m.v:0,
                 s.diff(m.N,m.r):Nr,s.diff(m.A,m.r):s.symbols('Ar',real=True),
                 s.diff(m.v,m.r):0}
    flux=s.simplify(m.jd.subs(m.tht,m.N*s.sqrt(1+m.q*m.q/(m.A*m.A)))
                    .subs(replacement,simultaneous=True))
    momentum=s.simplify(m.transport_rhs.subs(replacement,simultaneous=True))
    check={
        'flux_from_varied_action':s.simplify(flux+N*R**2*rho*w/A)==0,
        'flux_has_unique_rest_root':s.solve(flux,w)==[0],
        'rest_transport_from_varied_action':s.simplify(momentum.subs(w,0)-Nr)==0,
        'nonzero_lapse_gradient_fails_stationarity':momentum.subs(w,0)!=0,
        'moving_dust_not_excluded':s.simplify(flux.subs(w,1))!=0,
    }
    if not all(check.values()):raise AssertionError(check)
    return {'checks':check,'radial_flux':str(flux),'rest_radial_momentum_rate':str(momentum.subs(w,0)),
            'analytic_bridge':'stationary continuity -> constant flux; regular center -> flux=0',
            'assumptions':['static spherical metric, zero shift','single-stream irrotational dust',
                           'stationary conserved dust density','regular center, no central sink',
                           'positive density on the considered interval; N,A,R>0 away from center'],
            'verdict':'no stationary positive-density dust branch with nonzero N_r',
            'non_claims':['not a gravity-action no-go','not an exclusion of rotating galaxies',
                          'not an exclusion of collisionless velocity dispersion or fluid pressure']}

if __name__=='__main__':print(json.dumps(derive(),indent=2))
