#!/usr/bin/env python3
"""A real free-energy mechanism in a toy medium; not a dark-sector completion.

Cold equal-density charged beams +/-v with fixed neutralizing background.
Omega_p refers to TOTAL beam density. Saturation omega_bounce=gamma is a
declared heuristic, not a computed nonlinear saturation law.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


def matrix(k,v=1.):
    # q/m=-1, total n=1, epsilon=1 => total Omega_p=1.
    # E = i(n_plus+n_minus)/k from Fourier Poisson.
    M=np.zeros((4,4),dtype=complex)
    for n,u,speed in [(0,1,v),(2,3,-v)]:
        M[n,n]=-1j*k*speed; M[n,u]=-1j*k/2
        M[u,u]=-1j*k*speed
        M[u,0]=-1j/k; M[u,2]=-1j/k
    return M


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    args=ap.parse_args(); checks=[]; rows=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}",flush=True)
    om,K,P=sp.symbols('omega K Omega_p',positive=True)
    dielectric=1-P**2/2*((om-K)**-2+(om+K)**-2)
    numerator=sp.factor(dielectric*(om-K)**2*(om+K)**2)
    expected=om**4-(2*K*K+P*P)*om*om+K**4-P*P*K*K
    check('cold_beam_dispersion',sp.simplify(numerator-expected)==0,str(numerator))
    lower=K*K+P*P/2-P*sp.sqrt(P*P+8*K*K)/2
    upper=K*K+P*P/2+P*sp.sqrt(P*P+8*K*K)/2
    check('two_exact_branches',sp.simplify(expected.subs(om**2,lower))==0 and sp.simplify(expected.subs(om**2,upper))==0,'omega_minus^2 can be negative; no finite gravity forcing is required')
    optimum=sp.sqrt(sp.Rational(3,8))*P
    check('maximum_growth_stationary',sp.simplify(sp.diff(-lower,K).subs(K,optimum))==0,'K_max=sqrt(3/8) Omega_p')
    check('maximum_growth_value',sp.simplify((-lower).subs(K,optimum)-P*P/8)==0,'gamma_max=Omega_p/(2 sqrt(2))')
    check('growth_curvature_negative',sp.simplify(sp.diff(-lower,K,2).subs(K,optimum))<0,'unique nonzero maximum on 0<K<Omega_p')
    # Load-bearing orthogonal implementation: linear fluid matrix, not roots
    # of the preceding scalar quartic.
    for k in (.01,.2,math.sqrt(3/8),.9,1.2,2.,10.):
        vals=np.linalg.eigvals(matrix(k))
        growth=float(np.max(vals.real))
        low=k*k+.5-.5*math.sqrt(1+8*k*k)
        pred=math.sqrt(-low) if low<0 else 0.
        rows.append(dict(k_v_over_total_plasma_frequency=k,growth=growth,analytic_growth=pred))
        check(f'fluid_matrix_growth_k={k}',abs(growth-pred)<2e-12,f'matrix={growth:.12g}, dispersion={pred:.12g}')
    stationary=np.linalg.eigvals(matrix(math.sqrt(3/8),v=0))
    check('zero_stream_speed_control',np.max(stationary.real)<1e-7,'stationary cold plasma has no exponential growing mode')
    kmax=math.sqrt(3/8); M=matrix(kmax)
    vals,vecs=np.linalg.eig(M); j=np.argmax(vals.real); rate=float(vals[j].real)
    eigenvector=vecs[:,j]/np.linalg.norm(vecs[:,j])
    fits=[]
    for seed in (1e-8,-1e-8,2e-8):
        ts=np.linspace(0,12,121)
        sol=solve_ivp(lambda t,y:M@y,(0,12),seed*eigenvector,t_eval=ts,method='DOP853',rtol=1e-10,atol=1e-16)
        amplitude=np.linalg.norm(sol.y,axis=0)
        fitted=float(np.polyfit(ts,np.log(amplitude),1)[0])
        fits.append(dict(seed=seed,rate=fitted,final_amplitude=float(amplitude[-1])))
        check(f'time_domain_growth_seed={seed}',sol.success and abs(fitted-rate)<2e-8,f'fit={fitted:.12g}, expected={rate:.12g}; finite noise selects phase, not growth rate')
    v=sp.symbols('v',positive=True)
    accel=sp.simplify((P*P/8)/(optimum/v))
    check('bounce_saturation_ansatz',sp.simplify(accel-P*v/(2*sp.sqrt(6)))==0,'IF omega_bounce^2=k a and omega_bounce=gamma_max, a=Omega_p v/(2sqrt(6))')
    eta,rho,G=sp.symbols('eta rho G',positive=True)
    mapped=sp.simplify(accel.subs(P,sp.sqrt(8*sp.pi*G*eta*eta*rho)))
    check('hypothetical_dipole_frequency_mapping',sp.simplify(mapped/(v*sp.sqrt(G*rho))-eta*sp.sqrt(sp.pi/3))==0,'extra mapping Omega_p^2=8piG eta^2 rho; force mapping to galaxy a0 has NOT been derived')
    required=math.sqrt(3/(4*math.pi))
    check('coefficient_requires_velocity_density_selection',abs(required*math.sqrt(math.pi/3)-.5)<1e-15,f'eta sqrt(rho/rho_Lambda) v/c must equal {required:.12g}; not selected by this toy')
    data=dict(checks=checks,dispersion=str(expected),growth_rows=rows,time_domain=fits,
              ansatz_acceleration=str(accel),mapped_acceleration=str(mapped),
              verdict='Relative streaming can genuinely pump growing modes. This establishes a possible class of pumps, not MOND, nonlinear saturation, chirality, or 32pi.',
              limitations=['Cold electrostatic plasma with a fixed neutralizer; not the full non-Abelian medium','Total-density plasma-frequency convention','No nonlinear saturation simulated','Bounce condition is heuristic','All longitudinal dipoles are parallel in a single wave and give zero cross product','Vacuum frequency and MOND acceleration identifications are additional assumptions','No universal velocity or density selected'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    failed=sum(not x['passed'] for x in checks)
    print(f'{len(checks)-failed}/{len(checks)} checks pass; theory and 32pi OPEN.')
    return int(failed>0)


if __name__=='__main__': raise SystemExit(main())
