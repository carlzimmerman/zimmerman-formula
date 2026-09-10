#!/usr/bin/env python3
"""Follow the pressure-canceling clock solution into its quadratic kinetic gate."""
import json
import sympy as sp
import mpmath as mp
from inverse_entropy_clock import derive


def main():
    _,d=derive()
    A,B,Q,H,M,m=d['A'],d['B'],d['Q'],d['H'],d['M'],d['m']
    slope,Omega,v=sp.symbols('s Omega_m v',positive=True)
    # Construct m=m0 a^s, Q=Qc/(1+m), exactly dust+Lambda background.
    e=Q*m/(1+m)*(-slope+sp.Rational(3,2)*Omega)
    e_log_prime=slope-2*slope*m/(1+m)-sp.Rational(9,2)*Omega*(1-Omega)/(-slope+sp.Rational(3,2)*Omega)
    bp=d['Bprime'].subs({d['mn']:slope*m,d['mnn']:slope**2*m})
    flow=v*(bp/B+e_log_prime+3)
    flow=sp.factor(flow.subs(B,-3*A*v/e).subs(A,3*M*H**2*Omega/(Q*(1+m))))
    coefficient=sp.factor(flow/(v*(1-v)))
    logistic=(v not in coefficient.free_symbols)
    # s=2 admits an explicit global-in-a solution on the dust+Lambda background.
    aa,R,shape=sp.symbols('a R shape',positive=True)
    vv=(1+4*R*aa**3)/(1+(4*R+shape)*aa**3)
    closed_residual=sp.factor(aa*sp.diff(vv,aa)-flow.subs({slope:2,Omega:1/(1+R*aa**3),v:vv}))
    if closed_residual!=0:raise AssertionError('closed kinetic profile does not solve the inverse equation')
    rhs=sp.lambdify((A,B,Q,H,M,m,d['mn'],d['mnn']),d['Bprime'],'mpmath',cse=True)
    mp.mp.dps=70
    def profile(x):
        av=mp.exp(x); mass=mp.mpf('0.1')*av**2; qv=1/(1+mass)
        avar=mp.mpf('0.1')/av**3; om=1/(1+7*av**3)
        hv2=(mp.mpf('0.7')+mp.mpf('0.1')/av**3)/3
        ev=qv*mass/(1+mass)*(mp.mpf('1.5')*om-2)
        value=(1+28*av**3)/(1+57*av**3)
        bv=-3*avar*value/ev
        return av,mass,qv,avar,om,hv2,ev,value,bv
    rows=[]
    for j in range(37):
        x=mp.log(10)*(-6+mp.mpf(j)/4)
        av,mass,qv,avar,om,hv2,ev,value,bv=profile(x)
        derivative=mp.diff(lambda xx:profile(xx)[-1],x)
        expected=rhs(avar,bv,qv,mp.sqrt(hv2),mp.mpf(1),mass,2*mass,4*mass)
        error=abs(derivative-expected)/max(mp.mpf(1),abs(derivative),abs(expected))
        fv=bv*ev+3*avar
        D= qv*avar*mass**2/(1+mass)
        if not (bv>0 and ev<0 and fv>0 and 0<value<1 and error<mp.mpf('1e-55')):
            raise AssertionError('constructed profile fails its inverse equation or kinetic domain')
        kinetic=[]
        for kh in (mp.mpf('0.001'),mp.mpf(1),mp.mpf(1000)):
            kk=kh**2*hv2
            kval=bv-fv**2/(ev*fv-kk*D/hv2)
            if not kval>0:raise AssertionError('finite-k kinetic sign')
            kinetic.append(str(kval))
        rows.append(dict(a=str(av),m=str(mass),v=str(value),B=str(bv),e=str(ev),f=str(fv),
                         B_equation_relative_residual=str(error),kinetic_samples=kinetic))
    print(json.dumps(dict(normalized_kinetic_variable='v=-B e/(3 A); 0<v<1 gives B>0 and f=B e+3 A>0 when e<0',
                         e=str(e),v_flow=str(flow),logistic_coefficient=str(coefficient),
                         logistic=logistic,closed_s2_profile=str(vv),closed_profile_residual=str(closed_residual),
                         profile_samples=rows,precision_digits=mp.mp.dps,domain='s>3/2; 0<Omega_m<=1; m>0',
                         scope='Quadratic r=0 pressureless branch; not nonlinear health or a MOND construction'),indent=2))


if __name__=='__main__':main()
