#!/usr/bin/env python3
"""Direct ADM/gate checks and regular constrained initial-data witnesses.

This is a scalar-principal calculation, not an all-wavelength or global-halo test.
Usage: python3 check_coupled.py --output-dir run_001 [--mutate mixed|stiffness|time_cross]
"""
import argparse
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s


def symbolic(mutation):
    alpha,z,d,q,p,gamma=s.symbols('alpha z d q p gamma', real=True)
    H0,Hq,Hp,Hqq,Hqp,Hpp=s.symbols('H0 Hq Hp Hqq Hqp Hpp', real=True)
    Q=q/(1+alpha)
    Pi=(p+d)*s.exp(-3*z)
    dq,dp=Q-q,Pi-p
    H=H0+Hq*dq+Hp*dp+Hqq*dq*dq/2+Hqp*dq*dp+Hpp*dp*dp/2
    density=(1+alpha)*s.exp(3*z)*(H-Pi-gamma*Pi*Pi/2)
    zero={alpha:0,z:0,d:0}
    A0=q*q*Hqq
    c=1+gamma*p-Hp+q*Hqp
    D=Hpp-gamma
    if mutation=='mixed': c=1+gamma*p+q*Hqp
    if mutation=='stiffness': D=Hpp
    checks={
        'gate_lapse_hessian':s.simplify(s.diff(density,alpha,2).subs(zero)-A0)==0,
        'gate_mixed_hessian':s.simplify(s.diff(density,alpha,d).subs(zero)+c)==0,
        'gate_Pi_hessian':s.simplify(s.diff(density,d,2).subs(zero)-D)==0,
        'metric_Pi_mixing':s.simplify(s.diff(density,z,d).subs(zero)+3*p*(Hpp-gamma))==0,
    }
    # This L is obtained from KijKij-K² and the just-differentiated matter density.
    M,h,k,w,cc,DD,AA=s.symbols('M h k w c D A', nonzero=True,real=True)
    beta,zd,zz,aa,dd=s.symbols('beta zd zz aa dd',real=True)
    v=zd-h*aa
    # Independently contract the ADM Eij tensor before taking its second variation.
    epsilon=s.symbols('epsilon',real=True)
    E=s.diag(h+epsilon*(zd+k*k*beta),h+epsilon*zd,h+epsilon*zd)
    EH=M/(2*(1+epsilon*aa))*(s.trace(E*E)-s.trace(E)**2)
    EH2=s.diff(EH,epsilon,2).subs(epsilon,0)/2
    checks['Einstein_Kij_contraction']=s.simplify(EH2-(-3*M*v*v-2*M*k*k*beta*v))==0
    L=-3*M*v*v-2*M*k*k*beta*v+AA*aa*aa/2-cc*aa*dd+(DD-w/k**2)*dd*dd/2
    L+=M*k*k*zz*zz+2*M*k*k*aa*zz
    constraints=[s.diff(L,x) for x in (beta,dd,aa)]
    solved=s.solve(constraints,(aa,dd,beta),dict=True)[0]
    reduced=s.factor(L.subs(solved))
    kinetic=s.factor(s.diff(reduced,zd,2))
    expected=(AA+cc*cc*k*k/(w-DD*k*k))/h**2
    checks['direct_three_constraint_reduction']=s.simplify(kinetic-expected)==0
    checks['momentum_constraint']=s.simplify(solved[aa]-zd/h)==0
    # Differentiate the spatial-curvature cross term with time-dependent a,h,k_phys.
    adot,Hdot,kk=s.symbols('adot Hdot kk', real=True)
    a=s.symbols('a',positive=True)
    cross=a**3*2*M*kk/h
    crossdot=s.diff(cross,a)*a*h+s.diff(cross,kk)*(-2*h*kk)+s.diff(cross,h)*Hdot
    gradient=a**3*M*kk-crossdot/2
    if mutation=='time_cross': gradient=a**3*M*kk
    checks['Einstein_time_cross_gradient']=s.simplify(gradient-a**3*M*kk*Hdot/h**2)==0
    # Exact partial Legendre calculation, independent of its proposed Schur formula.
    nn=s.symbols('n',real=True)
    energy=(nn-cc*dd)**2/(2*AA)+(w/k**2-DD)*dd**2/2
    dsol=s.solve(s.diff(energy,dd),dd)[0]
    enn=s.factor(s.diff(energy.subs(dd,dsol),nn,2))
    checks['Hamiltonian_inverse']=s.simplify(enn-1/(AA+cc*cc*k*k/(w-DD*k*k)))==0
    # Stress and principal partial Legendre transform from the exact density.
    rho=-s.diff(density,alpha).subs(zero)
    pressure=s.diff(density,z).subs(zero)/3
    checks['central_energy_from_lapse']=s.simplify(rho-(q*Hq-H0+p+gamma*p*p/2))==0
    checks['central_pressure_from_metric']=s.simplify(pressure-(H0-p*Hp+gamma*p*p/2))==0
    localHessian=s.hessian(density,(alpha,d)).subs(zero)
    legendreSchur=localHessian[0,0]-localHessian[0,1]**2/localHessian[1,1]
    checks['principal_partial_Legendre']=s.simplify(legendreSchur-(q*q*Hqq-(1+gamma*p-Hp+q*Hqp)**2/(Hpp-gamma)))==0
    # The FRW full auxiliary Hessian actually is singular at the excluded P pole.
    auxiliary=s.hessian(L,(aa,dd,beta))
    det=s.factor(auxiliary.det())
    checks['auxiliary_pole_not_divided_through']=s.simplify(det.subs(DD,w/k**2))==0
    # q->infinity family limit, with all fixed stiffness/Pi_c terms retained.
    C,Pc,u,S,Sp,Spp=s.symbols('C Pc u S Sp Spp',positive=True)
    cf=1+gamma*u*Pc+C*(q*q-1)*Sp/Pc
    Df=C*(q-1)**2*Spp/Pc**2-gamma
    Ainf=2*C*q*q*S-cf*cf/Df
    limit=s.limit(Ainf/(C*q*q),q,s.oo)
    checks['family_large_q_limit']=s.simplify(limit-(2*S-Sp*Sp/Spp))==0
    # Weak-offset u=1 condition, r=H_Q/Pi; fixed gate, negligible gamma.
    r=s.symbols('r',positive=True)
    roots=s.solve(s.Eq(1-(1-3*r)**2/(s.Rational(3,2)*r*r),0),r)
    return dict(checks=checks, gate_A0=str(A0),gate_c=str(c),gate_D=str(D),
                reduced_kinetic=str(kinetic),auxiliary_determinant=str(det),
                Hamiltonian_nn=str(enn),family_limit=str(limit),
                weak_offset_u1_roots=[str(x) for x in roots])


def coefficients(q,Pi,C,Pc,gamma):
    u=Pi/Pc
    S=math.exp(-u**3)
    Sp=-3*u*u*S
    Spp=(9*u**4-6*u)*S
    x=q-1
    H=C*x*x*S
    Hq=2*C*x*S
    Hqq=2*C*S
    Hp=C*x*x*Sp/Pc
    Hqp=2*C*x*Sp/Pc
    Hpp=C*x*x*Spp/Pc**2
    c=1+gamma*Pi-Hp+q*Hqp
    D=Hpp-gamma
    A0=q*q*Hqq
    Ainf=A0-c*c/D
    rho=q*Hq-H+Pi+gamma*Pi*Pi/2
    pressure=H-Pi*Hp+gamma*Pi*Pi/2
    return dict(H=H,Hq=Hq,Hqq=Hqq,Hp=Hp,Hqp=Hqp,Hpp=Hpp,
                c=c,D=D,A0=A0,Ainfinity=Ainf,rho_without_W=rho,
                pressure_at_center=pressure,n_eff=rho+pressure,
                scalar_speed_squared=(rho+pressure)/Ainf)


def background(gamma,kind):
    K,C,Pc,a0,q,p=1.,1e6,1.,1.,1.+1e-6,1.
    center=coefficients(q,p,C,Pc,gamma)
    h=math.sqrt(2*K*center['rho_without_W']/3)
    D0=center['D']
    radius=1e-5
    start=radius*1e-5
    # Exact central series through the first nonzero correction in each variable.
    pi2=-K*p/(6*D0)
    rho2=center['c']*pi2+K*p*p/18
    psi4=-K*rho2/40
    initial=[1+psi4*start**4,4*psi4*start**3,
             p*start/3+pi2*start**3/5,p+pi2*start**2]

    def W(v):
        z=K*v/a0
        return a0*a0/K*(-z-math.log1p(-z))

    def Wv(v):
        return K*v/(1-K*v/a0)

    def rhs(r,y):
        psi,deriv,v,Pi=y
        cf=coefficients(q,Pi,C,Pc,gamma)
        rho=cf['rho_without_W']+W(v)
        return [deriv,psi**5*(6*h*h-4*K*rho)/8-2*deriv/r,
                psi*psi*Pi-2*v/r-4*deriv*v/psi,
                -Wv(v)*psi*psi/cf['D']]

    sol=solve_ivp(rhs,(start,radius),initial,method='DOP853',rtol=2e-12,
                  atol=[1e-15,1e-20,1e-17,1e-13],dense_output=True,max_step=radius/30)
    assert sol.success,sol.message
    sample=np.linspace(radius*.1,radius*.9,41)
    step=radius*1e-3
    # Derivatives taken from the integrated fields, not by substituting rhs again.
    def derivative(r):
        return (-sol.sol(r+2*step)+8*sol.sol(r+step)-8*sol.sol(r-step)+sol.sol(r-2*step))/(12*step)
    residuals={'hamiltonian_relative':[],'divergence_relative':[],'P_constraint_relative':[]}
    for r in sample:
        psi,psip,v,Pi=sol.sol(r)
        numerical=derivative(r)
        cf=coefficients(q,float(Pi),C,Pc,gamma)
        rho=cf['rho_without_W']+W(float(v))
        R3=-8*(numerical[1]+2*psip/r)/psi**5
        residuals['hamiltonian_relative'].append(abs(R3+6*h*h-4*K*rho)/(4*K*abs(rho)))
        div=(numerical[2]+2*v/r+4*psip*v/psi)/psi**2
        residuals['divergence_relative'].append(abs(div-Pi)/abs(Pi))
        pres=-cf['D']*numerical[3]-Wv(float(v))*psi**2
        residuals['P_constraint_relative'].append(abs(pres)/max(abs(Wv(float(v))*psi**2),1e-20))
    max_res={k:float(max(v)) for k,v in residuals.items()}
    assert max_res['hamiltonian_relative']<1e-9,max_res
    assert max_res['divergence_relative']<1e-7,max_res
    assert max_res['P_constraint_relative']<5e-5,max_res
    values=sol.sol(np.linspace(start,radius,101))
    assert float(values[3].min())>0
    assert float(np.max(K*np.abs(values[2])/a0))<1
    assert center['n_eff']>0
    if kind=='unstable': assert center['Ainfinity']<0
    else: assert center['Ainfinity']>0 and center['D']<0
    modes=[]
    for k in [1e6,1e7,1e8]:
        Ak=center['A0']+center['c']**2*k*k/(K-center['D']*k*k)
        rate=math.sqrt(abs(center['scalar_speed_squared']))*k
        modes.append(dict(k=k,k_times_patch_radius=k*radius,
                          finite_k_kinetic_to_limit=Ak/center['Ainfinity'],
                          principal_growth_or_frequency=rate,
                          rate_over_expansion=rate/h))
    assert abs(modes[-1]['finite_k_kinetic_to_limit']-1)<1e-8
    return dict(status='regular constrained initial data; scalar principal only',
                kind=kind,parameters=dict(K=K,C=C,Pi_c=Pc,a0=a0,q=q,Pi0=p,gamma=gamma),
                expansion=h,expansion_derivative=-K*center['n_eff'],center=center,
                patch_radius=radius,solver_steps=len(sol.t),constraints=max_res,
                momentum_constraint='identically zero: D_j[K^j_i-delta^j_i K]=0 for constant h; matter ADM action shift-independent',
                min_Pi=float(values[3].min()),max_Pi=float(values[3].max()),
                max_KP_over_a0=float(np.max(K*np.abs(values[2])/a0)),
                maximum_relative_Pi_variation=float(np.max(np.abs(values[3]/p-1))),
                modes=modes,
                interpretation=('Unbounded high-k scalar growth on this admissible constrained state'
                                if kind=='unstable' else 'Positive scalar principal kinetic/gradient; finite wavelengths and nonlinear stability unproved'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--mutate',choices=['mixed','stiffness','time_cross'])
    args=parser.parse_args()
    here=Path(__file__).resolve().parent
    repo=here.parents[2]
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    started=time.time()
    result={'mutation':args.mutate,'symbolic':symbolic(args.mutate)}
    ok=all(result['symbolic']['checks'].values())
    if ok:
        result['unstable_flat_gate']=background(1e-8,'unstable')
        result['surviving_principal_example']=background(1e-5,'healthy_principal')
    result['status']='PASS' if ok else 'FAILED'
    dest=out/'result.json'
    dest.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    source_paths=[Path(__file__).resolve(),here/'CONTRACT.md',here/'DERIVATION.md',
                  here/'FAMILY_OBSTRUCTION.md',here/'SOURCE_CHECK.md',
                  repo/'closure_2026_11_06/QX17_covariant_field_equations/RESULT.md',
                  repo/'research_closure_2026_11_12/combined_route/pik1_corrections/RESULT.md',
                  repo/'fable52_push/TPA1_two_phase_action/EQUATIONS.md',
                  repo/'fable52_push/SCS1_static_clock_coupled_stability/RESULT.md']
    manifest={'state':'COMPLETED' if ok else 'FAILED','exit_code':0 if ok else 1,
              'base_checkpoint':'2207a1df48348f01ca1084d4add5d214c55d0e7e',
              'argv':sys.argv,'elapsed_seconds':time.time()-started,
              'environment':{'python':platform.python_version(),'numpy':np.__version__,
                             'scipy':scipy.__version__,'sympy':s.__version__},
              'inputs':{str(p.relative_to(repo)):sha(p) for p in source_paths},
              'outputs':{'result.json':sha(dest)},
              'scope':'Exact symbolic ADM identities and finite numerical constrained-data witnesses; scalar principal only'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return 0 if ok else 1


if __name__=='__main__':
    sys.exit(main())
