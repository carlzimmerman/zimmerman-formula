#!/usr/bin/env python3
"""Derive a conserved test-baryon source from the varied finite-wave clock action.

This is linear response on the SAME repaired background, not a nonlinear MOND
construction. C=a^3 delta-rho_k is constant; no time-switched external force.
"""
import argparse
import importlib.util
import json
from functools import lru_cache
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def derive():
    previous, c = load('vacuum_wave', HERE.parent/'cubic_finite_wavelength/derive.py').derive()
    L = c['quadratic_action']
    names = {str(v): v for v in L.free_symbols}
    z, zd, sigma, sd, n, b = [names[v] for v in ('z','zd','sigma','sd','n','b')]
    a,H,q,M,gamma,k,A,U,B0,qd = [c[v] for v in ('a','H','q','M','gamma','k','A','U','B0','qd')]
    C,u,ud = s.symbols('C u ud', real=True)
    hd = -(q*A+U)/(2*M)
    r = q/H
    rd = qd/H-q*hd/H**2
    bg = {names['P']:0, names['PX']:A/(2*q)+3*gamma*q*H,
          names['PXX']:(B0-A/q)/(4*q*q), names['W']:U-2*gamma*q*q*qd,
          names['WY']:A*U/(2*q*(q*A+U)), names['V']:U,
          names['Lambda']:3*H*H-(q*A+U)/M}
    Lb = L.subs(bg)
    sourced = Lb-C*n/2
    F = s.hessian(sourced,(n,b))
    forcing = s.Matrix([s.diff(sourced,v).subs({n:0,b:0}) for v in (n,b)])
    solution = (-F.inv()*forcing).applyfunc(s.factor)
    nsol, bsol = solution
    zero = {n:nsol,b:bsol}
    checks = {f'actual_auxiliary_Euler_{v}':s.factor(s.diff(sourced,v).subs(zero,simultaneous=True))==0 for v in (n,b)}
    checks['source_does_not_change_lapse'] = s.diff(nsol,C)==0
    checks['no_quadratic_density_term'] = s.factor(F.inv()[0,0])==0
    nvac = nsol.subs(C,0)
    vacuum_solution = {n:nvac,b:bsol.subs(C,0)}
    reduced_source = s.factor(sourced.subs(zero,simultaneous=True)-Lb.subs(vacuum_solution,simultaneous=True))
    checks['source_reduction_from_raw_action'] = s.factor(reduced_source+C*nvac/2)==0
    transform = {sigma:u+r*z,sd:ud+r*zd+rd*z}
    nt = s.factor(nsol.subs(transform,simultaneous=True))
    Theta = H+gamma*q**3/M
    Qmix = gamma*q*q/(M*Theta)
    nz = s.factor(s.diff(nt,z))
    nu = s.factor(s.diff(nt,u))
    checks['transformed_lapse_velocity'] = s.factor(s.diff(nt,zd)-1/H)==0
    checks['transformed_lapse_clock_velocity'] = s.factor(s.diff(nt,ud)-Qmix)==0
    # Integration by parts of -C zd/(2H), with Cdot=0 and Hdot retained.
    fz = s.factor(C*(-hd/H**2-nz)/2)
    fv0 = s.factor(-C*Qmix/2)
    fu0 = s.factor(-C*nu/2)
    J,E,D = [c[v] for v in ('velocity_mixing','field_mixing','constraint')]
    fv = s.factor(fv0-J*fz/D)
    fu = s.factor(fu0-E*fz/D)
    zsol = -(J*ud+E*u+fz)/D
    # Differentiate the z-eliminated source directly, not assigned forcing.
    before = D*z*z/2 + z*(J*ud+E*u+fz)+fv0*ud+fu0*u
    after = s.expand(before.subs(z,zsol))
    checks['zeta_Euler_with_source'] = s.factor(s.diff(before,z).subs(z,zsol))==0
    checks['effective_velocity_source'] = s.factor(s.diff(after,ud).subs({u:0,ud:0})-fv)==0
    checks['effective_position_source'] = s.factor(s.diff(after,u).subs({u:0,ud:0})-fu)==0
    checks['zero_source_is_previous_action'] = fv.subs(C,0)==0 and fu.subs(C,0)==0
    # Stable metric reconstruction; beta=-a² b/k is derived from the shift.
    beta = -a*a*bsol/k
    bhat = B0-6*gamma*q*H+6*gamma**2*q**4/M
    ef = sd-q*nsol
    beta_independent = -(M*z+gamma*q*q*sigma)/(M*Theta)+a*a*(q*bhat*ef+3*Theta*A*sigma+C/a**3)/(2*k*k*M*Theta)
    checks['independent_shift_formula'] = s.factor(beta-beta_independent)==0
    et = s.factor(ef.subs(transform,simultaneous=True))
    T = s.factor(a*a*(q*bhat*et+3*Theta*A*(u+r*z)+C/a**3)/(2*k*k*M*Theta))
    checks['stable_shift_decomposition'] = s.factor(beta.subs(transform,simultaneous=True)+z/H+Qmix*u-T)==0
    # Bardeen potentials from independent lapse and spatial metric, not assigned.
    qmixdot = s.factor(s.diff(Qmix,H)*hd+s.diff(Qmix,q)*qd)
    phi_z = s.factor(nz+hd/H**2)
    phi_u = s.factor(nu-qmixdot)
    checks['stable_Phi_cancellation'] = s.factor(nt-(zd/H+Qmix*ud+nz*z+nu*u))==0
    # Conservation of O(epsilon) comoving dust on the unperturbed FLRW metric.
    checks['background_dust_continuity'] = s.factor(s.diff(C/a**3,a)*a*H+3*H*C/a**3)==0
    wrong = s.factor(s.diff(Lb+C*n/2,n).subs(zero,simultaneous=True))
    source_is_nonzero = s.factor(fz/C)!=0 or s.factor(fv/C)!=0 or s.factor(fu/C)!=0
    facts = dict(checks=checks,source_is_nonzero=source_is_nonzero,
        wrong_source_sign_rejected=wrong!=0,source_action='-C*n/2; C=a³ delta-rho constant',
        lapse=str(nsol),shift_potential=str(beta),source_zeta=str(fz),source_velocity=str(fv),source_field=str(fu),
        stable_Phi='(nz+Hdot/H²) z + (nu-Qmix_dot) u + Tdot',
        stable_Psi='H*Qmix*u-H*T',
        physical_initial_data='u=0 and udot=0; canonical p=fv initially, not p=0',
        scope='O(epsilon) conserved test baryons and metric response on the fixed background; not a finite-mass galaxy solution or MOND derivation',
        full_theory_status='OPEN')
    c.update(C=C,u=u,ud=ud,z=z,fz=fz,fv=fv,fu=fu,z_solution=zsol,
        T=T,Qmix=Qmix,phi_z=phi_z,phi_u=phi_u,nz=nz,nu=nu,
        lapse=nsol,shift=beta,Theta=Theta)
    return facts,c


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path)
    args=parser.parse_args();facts,_=derive()
    if args.result_file:args.result_file.write_text(json.dumps(facts,indent=2)+'\n')
    print(json.dumps(facts,indent=2))
    raise SystemExit(int(not all(facts['checks'].values()) or not facts['wrong_source_sign_rejected']))
