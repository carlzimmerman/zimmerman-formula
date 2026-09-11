#!/usr/bin/env python3
"""Unrestricted scalar-shear quadratic action with separately varied matter.

Fixed action: EH + P(X,tau)-V(tau)+sqrt(Xtau)W(Y,tau)+gamma X Box chi.
Ordinary radiation Cr Xr^2 and irrotational dust are minimally coupled.
delta(tau)=0, background N=1 in proper time, tau_dot=sbar need not be one.
Arbitrary background jets are retained, not fitted.
No scalar shear equation is discarded before variation. This is not a CMB run.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sympy as s


@lru_cache(maxsize=1)
def construct():
    names='a H Hd q qd qdd sbar sbard M2 gamma k P PX PXX PXXX Pt Ptt PXt PXXt V Vt Vtt W Wt WY WYt Cr qr qrd rho rhod'
    v=dict(zip(names.split(),s.symbols(names,real=True)))
    for field in ('z','e','sigma','rad','theta','drho','n','b'):
        for suffix in ('','d','dd'):v[field+suffix]=s.Symbol(field+suffix,real=True)
    # Short aliases retain the established sigma/time-mode and dust notation.
    v['sd']=v['sigmad'];v['td']=v['thetad']
    a,H,q,M,g,k=(v[x] for x in ('a','H','q','M2','gamma','k'))
    z,e,zd,ed,n,b,sig,sd,rad,rd,theta,td=(v[x] for x in
        ('z','e','zd','ed','n','b','sigma','sd','rad','radd','theta','td'))
    P,PX,PXX,V,W,WY=(v[x] for x in ('P','PX','PXX','V','W','WY'))
    ep,c,sn=s.symbols('epsilon cosine sine',real=True)
    N=1+ep*n*c;A=a*s.exp(ep*(z+2*e)*c);B=a*s.exp(ep*(z-e)*c)
    vol=A*B*B;shift=ep*b*sn;shift_x=ep*k*b*c
    ax=-ep*k*(z+2*e)*sn;bx=-ep*k*(z-e)*sn
    bxx=-ep*k*k*(z-e)*c
    Kx=(H+ep*(zd+2*ed)*c-shift*ax-shift_x)/N
    Ky=(H+ep*(zd-ed)*c-shift*bx)/N
    trace=Kx+2*Ky
    R3=(-4*bxx-6*bx*bx+4*ax*bx)/(A*A)
    cx=-ep*k*sig*sn;Q=(q+ep*sd*c-shift*cx)/N
    Y=cx*cx/(A*A);X=Q*Q-Y
    lapchi=(-ep*k*k*sig*c+(2*bx-ax)*cx)/(A*A)
    cubic=g*(-s.Rational(2,3)*Q**3*trace+2*Q*Kx*Y+2*Q*Q*lapchi)
    # grad chi dot grad Y starts at third order on the homogeneous background.
    eh=N*vol*M*(Kx*Kx+2*Ky*Ky-trace*trace+R3)/2
    clock=N*vol*(P+PX*(X-q*q)+PXX*(X-q*q)**2/2-V+cubic)+vol*v['sbar']*(W+WY*Y)
    qr=v['qr'];rx=-ep*k*rad*sn
    Xr=(qr+ep*rd*c-shift*rx)**2/N**2-rx*rx/A**2
    radiation=N*vol*v['Cr']*Xr**2
    tx=-ep*k*theta*sn
    Xd=(1+ep*td*c-shift*tx)**2/N**2-tx*tx/A**2
    dust=N*vol*(v['rho']+ep*v['drho']*c)*(Xd-1)/2
    moments={(0,0):1,(1,0):0,(0,1):0,(2,0):s.Rational(1,2),
             (0,2):s.Rational(1,2),(1,1):0}
    def quadratic(raw):
        expr=s.expand(s.diff(raw,ep,2).subs(ep,0)/2)
        return s.expand(sum(coef*moments[powers] for powers,coef in s.Poly(expr,c,sn).terms()))
    pieces={key:quadratic(raw) for key,raw in
            dict(einstein=eh,clock=clock,radiation=radiation,dust=dust).items()}
    # Cosmological constant has no shear and is retained as its own term.
    Lambda=s.Symbol('Lambda',real=True);v['Lambda']=Lambda
    pieces['lambda']=quadratic(-N*vol*M*Lambda)
    L2=s.expand(sum(pieces.values()))
    rates={a:a*H,H:v['Hd'],q:v['qd'],v['qd']:v['qdd'],v['sbar']:v['sbard'],
           P:v['sbar']*v['Pt']+2*q*v['qd']*PX,PX:v['sbar']*v['PXt']+2*q*v['qd']*PXX,
           PXX:v['sbar']*v['PXXt']+2*q*v['qd']*v['PXXX'],V:v['sbar']*v['Vt'],
           v['Pt']:v['sbar']*v['Ptt']+2*q*v['qd']*v['PXt'],v['Vt']:v['sbar']*v['Vtt'],
           W:v['sbar']*v['Wt'],WY:v['sbar']*v['WYt'],qr:v['qrd'],v['rho']:v['rhod']}
    for field in ('z','e','sigma','rad','theta','drho','n','b'):
        rates[v[field]]=v[field+'d'];rates[v[field+'d']]=v[field+'dd']
    def dt(expr):return s.expand(sum(s.diff(expr,x)*xd for x,xd in rates.items()))
    def el(expr,field):return s.expand(s.diff(expr,v[field])-dt(s.diff(expr,v[field+'d'])))
    euler={field:el(L2,field) for field in ('z','e','sigma','rad','theta','drho','n','b')}
    dq=sd-q*n;dk=3*zd-3*H*n-k*b;lap=-k*k*sig/a**2
    rho0=2*q*q*PX-P+V-6*g*H*q**3
    p0=P-V+v['sbar']*W+2*g*q*q*v['qd'];j0=2*q*PX-6*g*H*q*q
    drho=s.expand(-2*s.diff(pieces['clock'],n)/a**3-3*z*rho0)
    momentum=s.expand(2*s.diff(pieces['clock'],b)/(a**3*k))
    dp=s.expand(2*el(pieces['clock'],'z')/(3*a**3)-(n+3*z)*p0)
    Bchi=2*PX+4*q*q*PXX
    rho_target=(q*Bchi-18*g*H*q*q)*dq-2*g*q**3*dk+2*g*q*q*lap
    momentum_target=j0*sig+2*g*q*q*dq
    p_target=(2*q*PX+4*g*q*v['qd'])*dq+2*g*q*q*dt(dq)-n*(v['sbar']*W+2*g*q*q*v['qd'])
    shear=a*a*(3*ed/k**2-b/k)
    Phi=n+dt(shear);Psi=e-z-H*shear
    laplace=lambda expr:-k*k*expr/a**2
    Etau=v['Pt']-v['Vt']-3*H*W
    delta_Etau=2*q*v['PXt']*dq-W*dk+2*q*WY*lap
    dj=(Bchi-12*g*H*q)*dq-2*g*q*q*dk+2*g*q*lap
    divj=dt(j0)+3*H*j0
    delta_divj=(dt(dj)+3*H*dj+j0*dk-n*dt(j0)
                +(-2*PX+2*v['sbar']*WY+2*g*(v['qd']+3*H*q))*lap-2*g*q*laplace(dq))
    m=-momentum
    ward=dict(energy=s.expand(dt(drho)-n*dt(rho0)+3*H*(drho+dp)+(rho0+p0)*dk+laplace(m)
                             -q*delta_divj-dq*divj+v['sbar']*delta_Etau-v['sbar']*n*Etau),
              momentum=s.expand(dt(m)+3*H*m+(rho0+p0)*n+dp+divj*sig),
              scalar_EL=s.expand(euler['sigma']+a**3*(delta_divj+(n+3*z)*divj)/2))
    jr=4*v['Cr']*qr**3;djr=12*v['Cr']*qr**2*(rd-qr*n)
    divr=dt(jr)+3*H*jr
    delta_divr=dt(djr)+3*H*djr+jr*dk-n*dt(jr)-4*v['Cr']*qr**2*laplace(rad)
    jd=v['rho'];djd=v['drho']+jd*(td-n);divd=dt(jd)+3*H*jd
    delta_divd=dt(djd)+3*H*djd+jd*dk-n*dt(jd)-jd*laplace(theta)
    ward['radiation_EL']=s.expand(euler['rad']+a**3*(delta_divr+(n+3*z)*divr)/2)
    ward['dust_EL']=s.expand(euler['theta']+a**3*(delta_divd+(n+3*z)*divd)/2)
    # Genuine homogeneous isotropic mode has cos=1, sin=0, no scalar shear;
    # it is not the finite-k period average evaluated blindly at zero.
    raw0=eh+clock+radiation+dust-N*vol*M*Lambda
    homogeneous=s.expand((s.diff(raw0,ep,2).subs(ep,0)/2).subs({k:0,c:1,sn:0,e:0,ed:0}))
    radiation_rho=3*v['Cr']*qr**4
    friedmann=3*M*H*H-M*Lambda-rho0-v['rho']-radiation_rho
    ray=2*M*v['Hd']+rho0+p0+v['rho']+4*v['Cr']*qr**4
    radiation_cont=dt(radiation_rho)+4*H*radiation_rho
    dust_cont=v['rhod']+3*H*v['rho']
    preservation=dt(Etau)
    background_matrix,background_rhs=s.linear_eq_to_matrix([ray,divj,preservation],
                                                            [v['Hd'],v['qd'],v['sbar']])
    background=dict(friedmann=friedmann,clock_constraint=Etau,raychaudhuri=ray,
                    chi_current=divj,clock_preservation=preservation,
                    radiation_continuity=radiation_cont,dust_continuity=dust_cont,
                    velocity_order=['Hdot','qdot','tau_dot'],matrix=background_matrix,rhs=background_rhs,
                    determinant=s.factor(background_matrix.det()),
                    checks=dict(friedmann_preservation=s.expand(dt(friedmann)-3*H*ray+q*divj
                                     -v['sbar']*Etau+dust_cont+radiation_cont)))
    # Momentum normalisation divides by k. Its homogeneous numerator is
    # exported and checked separately; no division at k=0 is performed.
    return dict(s=v,dt=dt,euler=euler,action=L2,**pieces,
                rho_delta=drho,rho_target=s.expand(rho_target),
                momentum=momentum,momentum_target=s.expand(momentum_target),
                pressure_delta=dp,pressure_target=s.expand(p_target),
                rho0=rho0,p0=p0,j0=j0,dq=dq,dk=dk,lap=lap,
                Phi=Phi,Psi=Psi,slip=s.expand(Phi-Psi),ward=ward,
                current_delta=dj,current_equation=delta_divj,clock_equation=delta_Etau,
                homogeneous_action=homogeneous,background=background,
                projected_gradient=dict(background=s.simplify(Y.subs(ep,0)),
                    first_order=s.simplify(s.diff(Y,ep).subs(ep,0)),
                    second_order=s.simplify(s.diff(Y,ep,2).subs(ep,0)/2)))


def export(d):
    v=d['s'];checks={name:s.expand(d[key]-d[target])==0 for name,key,target in
        [('density','rho_delta','rho_target'),('pressure','pressure_delta','pressure_target'),
         ('momentum','momentum','momentum_target')]}
    checks['shear_slip']=s.expand(d['euler']['e']+v['M2']*v['a']*v['k']**2*d['slip'])==0
    checks.update({name:expr==0 for name,expr in d['ward'].items()})
    checks.update({name:expr==0 for name,expr in d['background']['checks'].items()})
    if not all(checks.values()):raise AssertionError(checks)
    return dict(action=str(d['action']),pieces={x:str(d[x]) for x in ('einstein','clock','radiation','dust','lambda')},
                euler={x:str(y) for x,y in d['euler'].items()},
                stress={x:str(d[x]) for x in ('rho0','p0','j0','rho_delta','pressure_delta','momentum')},
                potentials={x:str(d[x]) for x in ('Phi','Psi','slip')},checks=checks,
                clock_constraint=str(d['clock_equation']),current_delta=str(d['current_delta']),
                current_equation=str(d['current_equation']),
                homogeneous_isotropic_action=str(d['homogeneous_action']),
                background={key:(value if key=='velocity_order' else str(value))
                            for key,value in d['background'].items()},
                projected_gradient={key:str(value) for key,value in d['projected_gradient'].items()},
                scope='Exact scalar quadratic action on homogeneous background, arbitrary fixed constitutive jets; no CMB transfer or MOND law',
                full_theory_status='OPEN')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args();result=export(construct())
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
