#!/usr/bin/env python3
"""Bounded exact dual identities and a one-harmonic actual-kernel saddle."""
import argparse,json,math
from pathlib import Path
import sympy as s
import numpy as np
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
    def exact(name,e):
        v=s.factor(s.simplify(e));assert v==0,(name,v)
        checks[name]={'passed':True,'residual':str(v),'kind':'exact'}
    def bounded(name,error,tol):
        assert np.isfinite(error) and error<tol,(name,error,tol)
        checks[name]={'passed':True,'absolute_error':float(error),'tolerance':tol,'kind':'bounded_numeric'}
    z,t,U,m,v2,k,g=s.symbols('z t U m v2 k g',positive=True)
    F=1+(t-1)**4/t**2
    exact('reciprocal_vacuum_symmetry',F-F.subs(t,1/t))
    exact('reciprocal_vacuum_convexity_factor',s.diff(F,t,2)-2*(t-1)**2*(t*t+2*t+3)/t**4)
    for n in range(4):
        exact('vacuum_at_one_derivative_'+str(n),s.diff(F,t,n).subs(t,1)-(1 if n==0 else 0))
    # Exact one-mode quadratic saddle, with normalized eigenfunction.
    H=(2*m*k+v2)*z*z/2+2*m*k*U*z-g*U*U/2
    zsol=-2*m*k*U/(2*m*k+v2)
    I=-H.subs(z,zsol)
    exact('canonical_Z_elimination',s.diff(H,z).subs(z,zsol))
    exact('dual_positive_Schur',s.diff(I,U,2)-(g+(2*m*k)**2/(2*m*k+v2)))
    exact('raw_saddle_Hessian_negative_determinant',s.hessian(H,(U,z)).det()+g*(2*m*k+v2)+(2*m*k)**2)
    exact('zero_vacuum_curvature_auxiliary_kernel',s.diff(I,U,2).subs({v2:0,g:0})-2*m*k)
    x=s.symbols('x');N=s.Function('N')(x);W=s.Function('W')(x)
    exact('global_compensator_boundary_identity',N*(s.diff(W,x,2)+s.diff(N,x)*s.diff(W,x)/N)-s.diff(N*s.diff(W,x),x))
    r=s.symbols('r',real=True)
    Gr=7*r**5-14*r**6+10*r**7-s.Rational(5,2)*r**8
    exact('ramp_convexity_factor',s.diff(Gr,r,2)-140*r**3*(1-r)**3)
    exact('ramp_linear_lower_bound_factor',Gr-r+s.Rational(1,2)-(1-r)**5*(5*r**3+5*r**2+3*r+1)/2)
    # Actual XC4 primitive; integrate low branch after y=u^2 substitution.
    def hR(y):
        y=np.asarray(y);q=np.sqrt(y)
        return np.divide(y,np.expm1(q),out=np.zeros_like(y,dtype=float),where=q>0)
    def dhR(y):
        q=np.sqrt(y);e=np.expm1(q)
        return (2*e-q*(1+e))/(2*e*e)
    yp=brentq(dhR,2.,3.);hp=float(hR(yp));b=.05*hp
    ys=brentq(lambda yy:dhR(yy)-b/(yy+yp),2.,yp);hs=float(hR(ys))
    nodes,weights=leggauss(64);nodes=(nodes+1)/2;weights=weights/2
    def low_primitive(y):
        y=np.asarray(y);q=np.sqrt(y)[...,None]*nodes
        integ=2*q*hR(q*q)
        return np.sqrt(y)*np.sum(integ*weights,axis=-1)
    Iys=float(low_primitive(ys))
    def primitive(y):
        y=np.asarray(y);low=low_primitive(np.minimum(y,ys));above=y>ys
        high=Iys+hs*(y-ys)+b*((y+yp)*np.log((y+yp)/(ys+yp))-(y-ys))
        return np.where(above,high,low)
    def hm(y):
        y=np.asarray(y);return np.where(y<=ys,hR(y),hs+b*np.log((y+yp)/(ys+yp)))
    def dhm(y):
        y=np.asarray(y);safe=np.maximum(y,1e-20)
        return np.where(y<=ys,dhR(safe),b/(y+yp))
    bounded('XC4_splice_value_control',abs(ys-2.3374124053),1e-9)
    for yy in [.01,1.,3.,10.]:
        step=1e-5*max(yy,.01)
        bounded('primitive_derivative_'+str(yy),abs(float((primitive(yy+step)-primitive(yy-step))/(2*step))-float(hm(yy))),2e-8)
    # Variational one-harmonic leaf integrals, not a collocation PDE solve.
    mm=1.;vv=.3;ell=.2;xi=.4;theta=.05;delta=.02;beta=.8;sk=math.exp(-xi*xi/2)
    def make_gate(n):
        q,w=leggauss(n);xx=math.pi*(q+1);ww=w/2;si=np.sin(xx);co=np.cos(xx)
        def gate(u):
            p=-sk*u*si;pu=-sk*si;y=np.abs(p)
            J=4*primitive(y);jp=4*hm(y)*np.sign(p)
            Y=J-ell*sk*u*co-theta;v=Y/delta;vr=np.clip(v,0,1)
            f=35*vr**4-84*vr**5+70*vr**6-20*vr**7
            G=np.where(Y<=0,0,np.where(Y>=delta,Y-delta/2,delta*(7*vr**5-14*vr**6+10*vr**7-2.5*vr**8)))
            Gpp=140*vr**3*(1-vr)**3/delta
            Yp=jp*pu-ell*sk*co
            E=.5*mm*np.dot(ww,G)
            Ep=.5*mm*np.dot(ww,f*Yp)
            Epp=.5*mm*np.dot(ww,f*4*dhm(y)*pu*pu+Gpp*Yp*Yp)
            ungated=.5*mm*np.dot(ww,jp*pu)
            return E,Ep,Epp,float(np.max(Y)),ungated
        return gate
    gate=make_gate(768)
    def f0(z,e0):
        rr=math.sqrt(1-z*z);R=1/rr
        C=-z/(rr*(1+rr))
        Cp=-1/(rr*(1+rr))-z*z*(1+2*rr)/(rr**3*(1+rr)**2)
        Vmean=4+z*z/2-4*R+R**3
        Vprime=z*(1-4*R**3+3*R**5)
        Vsecond=1-4*R**3+3*R**5+z*z*(-12*R**5+15*R**7)
        # Second derivative of C from exact symbolic expression below.
        Cpp=-z*(3+6*rr+2*rr*rr-2*rr**3)/(rr**5*(1+rr)**2)
        return (.5*mm*z*z+e0*(R+beta*C)+vv*Vmean,
                mm*z+e0*(z/rr**3+beta*Cp)+vv*Vprime,
                mm+e0*((1+2*z*z)/rr**5+beta*Cpp)+vv*Vsecond)
    # Exact derivatives of the elementary harmonic mean expressions.
    zz=s.symbols('zz',real=True);RR=(1-zz**2)**s.Rational(-1,2);CC=(1-RR)/zz
    ss=s.sqrt(1-zz*zz)
    exact('harmonic_reciprocal_C_second',s.diff(CC,zz,2)+zz*(3+6*ss+2*ss*ss-2*ss**3)/(ss**5*(1+ss)**2))
    cases=[]
    for e0 in [.01,2.,20.]:
        def z_of(u):return brentq(lambda zz:f0(zz,e0)[1]+mm*u,-1+1e-9,1-1e-9,xtol=1e-13)
        def ip(u):return gate(u)[1]-mm*z_of(u)
        u=brentq(ip,-100,100,xtol=2e-12);zz=z_of(u);eg,ep,epp,ymax,ung=gate(u)
        hess=epp+mm*mm/f0(zz,e0)[2]
        residual=max(abs(f0(zz,e0)[1]+mm*u),abs(ep-mm*zz))
        bounded('joint_saddle_residual_epsilon_'+str(e0),residual,2e-9)
        step=1e-5
        bounded('dual_Hessian_finite_difference_epsilon_'+str(e0),abs((ip(u+step)-ip(u-step))/(2*step)-hess),3e-5)
        assert hess>0 and abs(zz)<1
        cases.append({'epsilon_exc_mean':e0,'U_amplitude':u,'Z_amplitude':zz,'minimum_t':1-abs(zz),'gate_argument_max':ymax,'dual_Hessian':hess,'joint_residual':residual,'ungated_J_derivative':ung,'gated_derivative':ep})
    low=cases[0]
    assert low['gate_argument_max']<0 and low['gated_derivative']==0 and abs(low['ungated_J_derivative'])>1e-5
    checks['exact_inactive_vs_ungated_negative_control']={'passed':True,'kind':'bounded_numeric','gate_max':low['gate_argument_max'],'gated':low['gated_derivative'],'ungated':low['ungated_J_derivative']}
    out={'claim_id':'CD26_5_DUAL_AUXILIARY','number_of_checks':len(checks),'checks':checks,'one_harmonic_cases':cases,
         'parameters':{'m':mm,'V0':vv,'ell':ell,'xi':xi,'theta':theta,'delta':delta,'beta':beta,'quadrature_nodes':768,'kernel_low_primitive_nodes':64},
         'scope':['Finite one-harmonic variational control only; no mesh/PDE convergence claim','Exact symbolic dual Schur and mean formulas','Analytic finite-spectral-space existence/uniqueness separately proved in report','Not physical baryonic response or global gravity evolution']}
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'number_of_checks':len(checks),'all_passed':True,'one_harmonic_cases':cases},indent=2))

if __name__=='__main__':main()
