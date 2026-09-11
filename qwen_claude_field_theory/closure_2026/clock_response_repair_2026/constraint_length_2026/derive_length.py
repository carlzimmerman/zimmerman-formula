#!/usr/bin/env python3
"""Extract a spatial filter from the existing action, then reconstruct Psi.

No fitted coefficients, empirical likelihood or nonlinear halo claim. The
metric response reported here is an initial slice u=udot=0, not a static halo.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import numpy as np
import sympy as s

HERE = Path(__file__).resolve().parent


def extract_filter(D, E, k, a):
    D, E = s.sympify(D), s.sympify(E)
    D0, E0 = D.subs(k, 0), E.subs(k, 0)
    D2 = s.factor(s.diff(D, k, 2).subs(k, 0)/2)
    E2 = s.factor(s.diff(E, k, 2).subs(k, 0)/2)
    if s.factor(D-D0-D2*k*k) != 0 or s.factor(E-E0-E2*k*k) != 0:
        raise ValueError('constraint and field mixing must be affine in k squared')
    if D0 == 0 or D2 == 0:
        raise ValueError('zero mass/gradient requires the unreduced constraint')
    return dict(D0=s.factor(D0), D2=D2, E0=s.factor(E0), E2=E2,
                ell2=s.factor(a*a*D2/D0), shift=s.factor(E2/D2),
                remaining_u=s.factor(E0-E2*D0/D2))


def run():
    spec = importlib.util.spec_from_file_location('finite_action', HERE.parent/'cubic_finite_wavelength/derive.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    prior, c = module.derive()
    a,H,q,M,gamma,k,A,U,B0,qd = [c[v] for v in ('a','H','q','M','gamma','k','A','U','B0','qd')]
    D,E,J,A0 = [c[v] for v in ('constraint','field_mixing','velocity_mixing','pre_zeta_kinetic')]
    filt = extract_filter(D,E,k,a)
    z,u,ud,f = s.symbols('z u ud f',real=True)
    L = D*z*z/2 + J*z*ud + E*z*u + f*z + A0*ud*ud/2
    zsol = s.solve(s.diff(L,z),z)[0]
    w = zsol + filt['shift']*u
    filter_error = s.factor((1+filt['ell2']*k*k/a**2)*w-(J*ud+filt['remaining_u']*u+f)/(-filt['D0']))
    eliminated = L.subs(z,zsol)
    kinetic_error = s.factor(s.diff(eliminated,ud,2)-c['kinetic'])
    # Deliberately reversed Laplacian sign must not satisfy the same equation.
    wrong = (1-filt['ell2']*k*k/a**2)*w-(J*ud+filt['remaining_u']*u+f)/(-filt['D0'])
    witness = {val:s.Integer(1) for val in wrong.free_symbols}
    witness[gamma]=0
    wrong_sign = wrong.subs(witness)
    checks = dict(prior_action=all(prior['checks'].values()), varied_filter=filter_error==0,
                  varied_kinetic=kinetic_error==0,
                  wrong_laplacian_rejected=wrong_sign.is_finite is True and wrong_sign!=0)
    # Derive conserved baryon forcing and metric from the original ADM action.
    raw = c['quadratic_action']; names={str(v):v for v in raw.free_symbols}
    rz,rzd,rs,rsd,n,b = [names[v] for v in ('z','zd','sigma','sd','n','b')]
    C = s.symbols('C',real=True)
    hd = -(q*A+U)/(2*M)
    bg = {names['P']:0,names['PX']:A/(2*q)+3*gamma*q*H,
          names['PXX']:(B0-A/q)/(4*q*q),names['W']:U-2*gamma*q*q*qd,
          names['WY']:A*U/(2*q*(q*A+U)),names['V']:U,
          names['Lambda']:3*H*H-(q*A+U)/M}
    sourced = raw.subs(bg)-C*n/2
    F = s.hessian(sourced,(n,b))
    force = s.Matrix([s.diff(sourced,v).subs({n:0,b:0}) for v in (n,b)])
    nsol,bsol = (-F.inv()*force).applyfunc(s.factor)
    for var in (n,b):
        checks['raw_Euler_'+str(var)] = s.factor(s.diff(sourced,var).subs({n:nsol,b:bsol},simultaneous=True))==0
    transform = {rs:u+q/H*rz,rsd:ud+q/H*rzd+(qd/H-q*hd/H**2)*rz}
    nt=s.factor(nsol.subs(transform,simultaneous=True))
    fz=s.factor(C*(-hd/H**2-s.diff(nt,rz))/2)
    # Psi is obtained independently from spatial curvature and the solved shift.
    beta=s.factor((-a*a*bsol/k).subs(transform,simultaneous=True))
    psi=s.factor(-rz-H*beta)
    zi=-(fz/D)  # u=udot=0 on the specified initial slice; not p=0.
    psi_initial=psi.subs({rz:zi,u:0,ud:0},simultaneous=True)
    checks['Psi_no_zeta_velocity'] = rzd not in psi_initial.free_symbols
    psi_newton=-C/(2*M*a*k*k)  # reference Poisson response in these conventions.
    response=psi_initial/psi_newton
    m,v=s.symbols('m v',positive=True)
    station={U:m*q*A,B0:A/q*(1+2/m)}
    zero_braiding={gamma:0}
    length0=s.factor(filt['ell2'].subs(zero_braiding).subs(station))
    response0=s.factor(response.subs(zero_braiding).subs(station))
    # The existing profile equation, not a newly reconstructed function.
    qflow=-3*H*q*m*v/(m+2)-A*m*q*q/(2*M*H)
    length_flow=s.factor(H*H*length0.subs(qd,qflow))
    response_flow=s.factor(response0.subs(qd,qflow))
    Omega,x=s.symbols('Omega x',positive=True)
    response_dimensionless=s.factor(response_flow.subs(A,3*M*H*H*Omega/(q*(1+m))).subs(k,x*a*H))
    predicted_length=m*(m+2)/(9*(m+1)*v*(1-v))
    predicted_response=1+(9*Omega*(1-v)/(2*m))/(x*x+1/length_flow)
    checks['compact_length_from_action']=s.factor(length_flow-predicted_length)==0
    checks['compact_metric_from_action']=s.factor(response_dimensionless-predicted_response)==0
    # These expressions are exported for the separate Lean algebraic bound.
    # They are NOT a derivation of the profile or its freely chosen initial data.
    # Read the irreducible denominator of the actual metric, not the auxiliary
    # length alone. A numerator cancellation could otherwise fake screening.
    point={a:1,M:1,H:s.sqrt(s.Rational(4,15)),q:s.Rational(10,11),
           A:s.Rational(1,10),U:s.Rational(1,110),B0:s.Rational(231,100),
           qd:-5*s.sqrt(s.Rational(4,15))/77-1/(242*s.sqrt(s.Rational(4,15)))}
    rows=[]
    for g in (s.Integer(0),s.Rational(1,1000000)):
        pp=dict(point);pp[gamma]=g
        l2=filt['ell2'].subs(pp)
        D0=filt['D0'].subs(pp);D2=filt['D2'].subs(pp)
        reduced=s.cancel(response.subs(pp),extension=s.sqrt(15))
        numerator,denominator=s.fraction(reduced)
        denominator_ratio=s.cancel(denominator/(D0+D2*k*k),extension=s.sqrt(15))
        remainder=s.rem(numerator,denominator,k)
        checks['metric_denominator_survives_'+str(g)]=(k not in denominator_ratio.free_symbols and
            s.Poly(denominator,k).degree()==2 and s.simplify(remainder)!=0)
        high_k=s.limit(reduced,k,s.oo)
        responses=[]
        for ratio in (s.Rational(1,100),s.Integer(1),s.Integer(100),s.Integer(10000),s.Integer(100000)):
            kval=ratio*pp[H]*pp[a]
            responses.append(dict(k_over_aH=str(ratio),Psi_over_reference=str(s.N(response.subs(pp).subs(k,kval),40))))
        rows.append(dict(gamma=str(g),ell_H=str(s.N(pp[H]*s.sqrt(l2),40)),
                         D0=str(s.N(D0,30)),D2=str(s.N(D2,30)),
                         exact_Psi_response=str(reduced),high_k_response=str(high_k),
                         responses=responses))
    # Independently obtain Phi=n+betadot, retaining actual field acceleration.
    # u=udot=0 does NOT imply uddot=0: canonical p=fv and pdot=fu.
    profile_spec=importlib.util.spec_from_file_location('clock_profile',HERE.parent/'nonlinear_transport/stationary.py')
    profile_module=importlib.util.module_from_spec(profile_spec)
    profile_spec.loader.exec_module(profile_module)
    _,profile_rhs=profile_module.symbolic()
    parts=[A0,J,E,D,fz/C,-s.diff(nt,ud)/2,-s.diff(nt,u)/2,
           s.diff(beta,rz),s.diff(beta,ud),s.diff(beta,C),s.diff(nt,rz),s.diff(nt,rzd)]
    fn=s.lambdify((a,H,q,M,gamma,k,A,U,B0,qd),parts,'numpy',cse=True)
    ks=np.geomspace(.01,1e5,29)*float(point[H])
    def coefficient_map(primitive,gs):
        xx,lm,lv=primitive
        av=np.exp(xx);mv=np.exp(lm);vv=1/(1+np.exp(-lv))
        qv=1/(1+mv);AA=.1/av**3;UU=mv*qv*AA;HH=np.sqrt((.7+AA)/3)
        BB=AA/qv*(1+2/mv);qqd=-3*AA*HH*vv/BB-qv*UU/(2*HH)
        aa,jj,ee,dd,ff,fv0,fu0,bz,bv,bc,nz,nzd=fn(av,HH,qv,1,gs,ks,AA,UU,BB,qqd)
        return aa-jj*jj/dd,fv0-jj*ff/dd,fu0-ee*ff/dd,jj,dd,ff,bz,bv,bc,nz,nzd,HH
    primitive=np.array([0.,math.log(.1),0.])
    direction=float(point[H])*np.array([1.,*profile_rhs(.1,.5,.125)])
    metric=[]
    for gs in (0.,1e-6):
        af,fv,fu,jj,dd,ff,bz,bv,bc,nz,nzd,HH=coefficient_map(primitive,gs)
        zv=-ff/dd;betav=bz*zv+bc;psiv=-zv-HH*betav
        def moving_slice(h):
            aa,pfv,_,pj,pd,pf,pbz,pbv,pbc,*_=coefficient_map(primitive+h*direction,gs)
            velocity=(fv+h*fu-pfv)/aa
            zz=-(pj*velocity+pf)/pd
            return zz,pbz*zz+pbv*velocity+pbc
        estimates=[]
        for step in (1e-16,1e-20,1e-24):
            zz,bb=moving_slice(1j*step)
            zdv=zz.imag/step;bdv=bb.imag/step
            estimates.append(nz*zv+nzd*zdv+bdv)
        scale=np.maximum(np.abs(psiv),1e-30)
        slip=float(np.max(np.abs(estimates[-1]-psiv)/scale))
        refinement=float(np.max(np.abs(estimates[-1]-estimates[-2])/scale))
        fd_errors=[]
        for step in (1e-3,5e-4):
            qm,bm=moving_slice(-step);qp,bp=moving_slice(step)
            qmm,bmm=moving_slice(-2*step);qpp,bpp=moving_slice(2*step)
            zdt=(qmm-8*qm+8*qp-qpp)/(12*step)
            bdt=(bmm-8*bm+8*bp-bpp)/(12*step)
            fd_errors.append(float(np.max(np.abs(nz*zv+nzd*zdt+bdt-estimates[-1])/scale)))
        checks['initial_metric_slip_'+str(gs)]=slip<1e-8 and refinement<1e-10 and max(fd_errors)<1e-7
        metric.append(dict(gamma=gs,modes=len(ks),maximum_relative_Phi_Psi_difference=slip,
                           complex_step_refinement=refinement,finite_difference_errors=fd_errors,
                           interpretation='initial linear force/lensing response; no evolved halo'))
    assert all(checks.values()),checks
    return dict(checks=checks,filter={key:str(val) for key,val in filt.items()},
        fz=str(fz),initial_Psi_response=str(response),
        gamma_zero_stationary_ell_squared=str(length0),
        gamma_zero_stationary_initial_Psi_response=str(response0),
        gamma_zero_profile_ellH_squared=str(length_flow),
        gamma_zero_profile_Psi_response=str(response_dimensionless),
        points=rows,
        independent_metric=metric,
        scope='Exact quadratic finite-nonzero-k constraint and initial-slice spatial Bardeen response; fixed background',
        non_claims=['Initial Phi and Psi derived numerically; not a static halo or PPN calculation.',
                    'Not nonlinear dust depletion, MOND, CMB, a k=0 constraint count, or global stability.',
                    'No observational calibration or novelty certification.'],full_theory_status='OPEN')


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path)
    args=parser.parse_args();result=run()
    if args.result_file:args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:val for key,val in result.items() if key not in
        ('filter','initial_Psi_response','gamma_zero_stationary_initial_Psi_response')},indent=2))
