#!/usr/bin/env python3
"""Stationary pressureless log/sqrt clock sector: action, profile ODE, local cone tests.

No MOND or empirical certificate. The homogeneous zero sound speed is a boundary;
its two-sided local stability requires a stationary restoring coefficient.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import expit
import sympy as s

HERE=Path(__file__).resolve().parent


def symbolic():
    spec=importlib.util.spec_from_file_location('entropy_inverse',HERE.parent/'finite_evolution/inverse_entropy_clock.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    _,d=module.derive()
    A,Q,B,m,mn,mnn,H,M=[d[x] for x in ('A','Q','B','m','mn','mnn','H','M')]
    X,U,q,ds=s.symbols('X U q d',positive=True)
    p0=A/(2*q);db=A*U/(2*q*(q*A+U));D0=U-2*q*q*db
    restoring_derivative=(B-A/q)*D0/(4*q*q)-2*db*p0
    stationarity=s.solve(restoring_derivative,B)[0]
    assert s.factor(stationarity-A/q-2*A*A/U)==0
    P=-U*s.log((U-2*ds*X)/(U-2*ds*q*q))/2
    px=s.diff(P,X);pxx=s.diff(P,X,2)
    assert s.factor(pxx-2*px*px/U)==0
    assert s.factor(px*(U-2*ds*X)-ds*U)==0 # exactly zero homogeneous restoring term for all regular X
    assert s.factor(px.subs({X:q*q,ds:db})-p0)==0
    assert s.factor((2*px+4*q*q*pxx).subs({X:q*q,ds:db})-stationarity)==0
    # Impose the NEW necessary coefficient in the previously derived finite-k inverse.
    br=A/Q*(1+2/m)
    bd=s.diff(br,A)*(-3*A)+s.diff(br,Q)*(-Q*mn/(1+m))+s.diff(br,m)*mn
    m2=s.solve(s.factor(d['Bprime'].subs(B,br)-bd),mnn)[0]
    O,v=s.symbols('Omega v',real=True)
    m2=m2.subs(A,3*M*H*H*O/(Q*(1+m)))
    vexpr=(m+2)*(mn-s.Rational(3,2)*O*m)/(3*m*(m+1))
    mflow=s.factor(s.solve(v-vexpr,mn)[0])
    vp=s.diff(vexpr,m)*mn+s.diff(vexpr,mn)*m2+s.diff(vexpr,O)*(-3*O*(1-O))
    vflow=s.factor(vp.subs(mn,mflow))
    # General-angle principal matrix from direct first-derivative expansion.
    ep,pt,pxi,st,sxi,g,h,w0,wy,wyy,p1,p2,pa,sa,vel=s.symbols('ep pt pxi st sxi g h W WY WYY PX PXX pa sa vel',real=True)
    norm=s.sqrt((1+ep*pt)**2-ep**2*pxi**2)
    qe=((1+ep*pt)*(Q+ep*st)-ep*pxi*(g+ep*sxi))/norm
    ye=-(Q+ep*st)**2+(g+ep*sxi)**2+h*h+qe*qe
    xe=(Q+ep*st)**2-(g+ep*sxi)**2-h*h
    deltaX=xe-(Q*Q-g*g-h*h);deltaY=ye-(g*g+h*h)
    lag=p1*deltaX+p2*deltaX**2/2+norm*(w0+wy*deltaY+wyy*deltaY**2/2)
    l2=s.expand(s.diff(lag,ep,2).subs(ep,0)/2)
    actual=s.hessian(l2.subs({pt:-vel*pa,pxi:pa,st:-vel*sa,sxi:sa}),(pa,sa))
    wr=wy+2*g*g*wyy;clock=w0-2*g*g*wy-2*Q*Q*wr
    expected=s.Matrix([[-clock,-2*Q*wr],[-2*Q*wr,(2*p1+4*Q*Q*p2)*vel**2+8*Q*g*p2*vel-2*p1+4*g*g*p2+2*wr]])
    assert all(s.factor(x)==0 for x in actual-expected)
    assert s.Poly(actual.det(),vel).degree()<=2
    # Real Hamiltonian self-bracket cancellation, independent of the chosen P.
    xvar,yvar=s.symbols('Q_argument Y_argument',real=True)
    assert s.simplify(-2*xvar*s.diff(P.subs(X,xvar*xvar-yvar),yvar)-s.diff(P.subs(X,xvar*xvar-yvar),xvar))==0
    return dict(stationarity_B=str(stationarity),P=str(P),m_flow=str(mflow),v_flow=str(vflow),
        local_symbol=str(actual),full_angle_symbol_check=True,exact_homogeneous_restoring_identity=True),s.lambdify((m,v,O),(s.factor(mflow/m),s.factor(vflow/(v*(1-v)))),'math',cse=True)


def main():
    facts,rhs=symbolic()
    def ode(x,y):return rhs(math.exp(y[0]),expit(y[1]),1/(1+7*math.exp(3*x)))
    grid=np.linspace(-6*math.log(10),3*math.log(10),37)
    def integrate(method,rtol,atol):
        result=[]
        for end in (grid[0],grid[-1]):
            run=solve_ivp(ode,(0,end),[math.log(.1),0.],method=method,rtol=rtol,atol=atol,dense_output=True)
            if not run.success:raise AssertionError(run.message)
            result.append(run)
        return result
    runs=integrate('DOP853',1e-11,1e-12);controls=integrate('Radau',2e-12,2e-13)
    mismatch=max(np.max(np.abs(runs[int(x>=0)].sol(x)-controls[int(x>=0)].sol(x))) for x in grid)
    if not mismatch<1e-7:raise AssertionError('profile integrators disagree')
    mp.mp.dps=70;rows=[];profiles=[]
    for x in grid:
        lu,lv=runs[int(x>=0)].sol(x)
        mass=mp.exp(float(lu));vv=1/(1+mp.exp(-float(lv)));av=mp.exp(float(x))
        q=1/(1+mass);A=mp.mpf('.1')/av**3;U=mass*q*A;d=A*mass/(2*q*(1+mass));ell=q*q*mass/2
        B=A/q*(1+2/mass)
        assert mass>0 and 0<vv<1 and B>0
        profiles.append(dict(a=str(av),m=str(mass),v=str(vv),B=str(B)))
        for shift in (mp.mpf('-.5'),mp.mpf(0),mp.mpf('.5')):
            Q=q*mp.sqrt(1+shift*mass/(1+mass))
            for ratio in (mp.mpf('.001'),mp.mpf('.01'),mp.mpf('.1'),mp.mpf('.5'),mp.mpf('.9')):
                Y=(ratio*Q)**2;den=U-2*d*(Q*Q-Y)
                PX=d*U/den;PXX=2*d*d*U/(den*den)
                z=mp.sqrt(1+Y/ell);W=U+2*d*Y/(z+1);WY=d/z;WYY=-d/(2*ell*z**3)
                for angle in (mp.mpf(0),mp.mpf('.5'),mp.mpf(1)):
                    gp=ratio*Q*angle;wr=WY+2*gp*gp*WYY;S=W-2*gp*gp*WY-2*Q*Q*wr
                    kin=2*PX+4*Q*Q*PXX;lin=8*Q*gp*PXX
                    const=-2*PX+4*gp*gp*PXX+2*wr+4*Q*Q*wr*wr/S
                    disc=lin*lin-4*kin*const
                    roots=[(-lin-mp.sqrt(disc))/(2*kin),(-lin+mp.sqrt(disc))/(2*kin)] if disc>=0 else None
                    good=bool(den>0 and S>0 and kin>0 and roots is not None and max(abs(r) for r in roots)<=1)
                    rows.append(dict(a=str(av),Q_squared_offset_fraction=str(shift),gradient_over_Q=str(ratio),
                        direction_cosine=str(angle),domain_denominator=str(den),clock_elliptic_symbol=str(S),
                        kinetic=str(kin),discriminant=str(disc),speeds=None if roots is None else [str(r) for r in roots],passed=good))
    return dict(symbolic=facts,profile=profiles,integrator_log_coordinate_disagreement=float(mismatch),
        cases=rows,passed=sum(r['passed'] for r in rows),total=len(rows),arithmetic_digits=mp.mp.dps,
        caveats=['70-digit characteristic arithmetic on a float64 integrated profile; not a rigorous interval ODE enclosure',
          'No universal cone proof, global elliptic inverse, nonlinear caustic/strong-coupling proof, radiation or MOND completion',
          'No baryon data or empirical likelihood was used'],full_theory_status='OPEN')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);a=p.parse_args()
    result=main();encoded=json.dumps(result,indent=2)+'\n'
    if a.result_file:a.result_file.write_text(encoded)
    print(json.dumps({k:result[k] for k in ('passed','total','integrator_log_coordinate_disagreement','full_theory_status')}))
