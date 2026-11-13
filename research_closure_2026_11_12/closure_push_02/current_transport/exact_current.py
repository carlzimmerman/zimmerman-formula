#!/usr/bin/env python3
"""Direct flat 1+1 jet Euler variation of gated QX17, not reuse of its EL output."""
import argparse
import json
import time
import sympy as sp
import mpmath as mp


def main(output):
    start=time.perf_counter();mp.mp.dps=35
    a,b,aa,ab,bb,p0,p1,p0t,p0x,p1t,p1x,lam=sp.symbols('a b aa ab bb p0 p1 p0t p0x p1t p1x lam')
    syms=[a,b,aa,ab,bb,p0,p1,p0t,p0x,p1t,p1x,lam]
    Q=sp.sqrt(a*a-b*b)
    dl=[(a*aa-b*ab)/Q**2,(a*ab-b*bb)/Q**2]
    Pd=-p0*dl[0]+p1*dl[1]
    Pi=-p0t+p1x+Pd
    C,alpha,beta,gamma,w=map(sp.Rational,['.7','.3','.2','.4','.6'])
    H=C*(Q-1)**2*(1+alpha*Pi+beta*Pi**2)
    L=H-Pd-w*(-p0*p0+p1*p1)/2-gamma*Pi**2/2+lam*(a*p0-b*p1)/Q
    fn=lambda e:sp.lambdify(syms,e,'mpmath',cse=True)
    tau_first=[fn(sp.diff(L,z)) for z in (a,b)]
    tau_second={(0,0):fn(sp.diff(L,aa)),(0,1):fn(sp.diff(L,ab)),(1,1):fn(sp.diff(L,bb))}
    pp=[[fn(sp.diff(L,p)),fn(sp.diff(L,pt)),fn(sp.diff(L,px))]
        for p,pt,px in [(p0,p0t,p0x),(p1,p1t,p1x)]]
    t,x=sp.symbols('t x')
    clock=t+sp.Rational(1,20)*t*t+sp.Rational(1,25)*t*x+sp.Rational(1,30)*x*x+sp.Rational(1,70)*t*x*x
    ta,tb=sp.diff(clock,t),sp.diff(clock,x)
    P1=2+x+sp.Rational(1,5)*t+sp.Rational(3,10)*t*x+sp.Rational(1,10)*t*t
    P0=tb*P1/ta  # enforce tangency on test fields, AFTER unconstrained variation
    LF=sp.Rational(2,5)+t/7-x/9+t*x/11
    expressions=[ta,tb,sp.diff(clock,t,2),sp.diff(clock,t,x),sp.diff(clock,x,2),P0,P1,
                 sp.diff(P0,t),sp.diff(P0,x),sp.diff(P1,t),sp.diff(P1,x),LF]
    field=sp.lambdify((t,x),expressions,'mpmath',cse=True)
    qfn,pifn=fn(Q),fn(Pi)
    def derivative(f,point,direction):
        return mp.diff(f,point,tuple(int(k==direction) for k in range(2)))
    def jets(point):return field(*point)
    def geom(point):
        j=jets(point);q=qfn(*j);pi=pifn(*j)
        return j,q,pi,[j[0]/q,-j[1]/q],[-j[5],j[6]]
    def gate_parts(q,pi,mutation):
        hq=2*mp.mpf('.7')*(q-1)*(1+mp.mpf('.3')*pi+mp.mpf('.2')*pi*pi)
        hpi=mp.mpf('.7')*(q-1)**2*(mp.mpf('.3')+mp.mpf('.4')*pi)
        B=1+mp.mpf('.4')*pi-(0 if mutation=='omit_gate_Pi' else hpi)
        if mutation=='ungated_HQ':hq=2*mp.mpf('.7')*(q-1)
        return hq,B
    def sigma(point,mutation):
        j,q,pi,n,P=geom(point);hq,B=gate_parts(q,pi,mutation)
        def bp(c):
            def f(*z):
                _,q1,pi1,_,P1=geom(z)
                return gate_parts(q1,pi1,mutation)[1]*P1[c]
            return f
        return hq+sum(derivative(bp(c),point,c) for c in range(2))/q
    def current(c,mutation):
        def f(*z):
            j,q,pi,n,P=geom(z)
            flux=0 if mutation=='omit_leaf_flux' else j[-1]*P[c]/q
            return n[c]*sigma(z,mutation)-flux
        return f
    rows=[]
    for point0 in [('0.13','0.17'),('0.27','-0.11'),('-0.09','0.24')]:
        point=tuple(map(mp.mpf,point0));j,q,pi,n,P=geom(point)
        assert q>0 and pi>0
        direct=-sum(derivative(lambda *z,ff=f:ff(*jets(z)),point,c) for c,f in enumerate(tau_first))
        for (c,d),f in tau_second.items():
            orders=[0,0];orders[c]+=1;orders[d]+=1
            direct+=mp.diff(lambda *z,ff=f:ff(*jets(z)),point,tuple(orders))
        comparisons={}
        for mutation in ['none','omit_gate_Pi','omit_leaf_flux','ungated_HQ']:
            candidate=-sum(derivative(current(c,mutation),point,c) for c in range(2))
            comparisons[mutation]=float(abs(direct-candidate))
        pres=[]
        for c in range(2):
            direct_p=pp[c][0](*j)-sum(derivative(lambda *z,ff=pp[c][d+1]:ff(*jets(z)),point,d) for d in range(2))
            def blog(*z):
                _,qq,ppi,_,_=geom(z)
                return gate_parts(qq,ppi,'none')[1]
            _,B=gate_parts(q,pi,'none')
            sign=-1 if c==0 else 1
            candidate=sign*(-B*fn(dl[c])(*j)+derivative(blog,point,c))-mp.mpf('.6')*P[c]+j[-1]*n[c]
            pres.append(float(abs(direct_p-candidate)))
        rows.append({'point':list(point0),'Q':float(q),'Pi':float(pi),'clock_residual_abs':comparisons,
                     'polarization_residual_abs':pres,'current_spatial':float(current(1,'none')(*point)),
                     'leaf_flux_spatial':float(-j[-1]*P[1]/q)})
    # P variation above intentionally uses high-precision derivatives throughout.
    checks={'exact_clock_current':max(r['clock_residual_abs']['none'] for r in rows)<1e-24,
            'gate_Pi_mutant_rejected':min(r['clock_residual_abs']['omit_gate_Pi'] for r in rows)>1e-7,
            'leaf_flux_mutant_rejected':min(r['clock_residual_abs']['omit_leaf_flux'] for r in rows)>1e-7,
            'ungated_HQ_mutant_rejected':min(r['clock_residual_abs']['ungated_HQ'] for r in rows)>1e-7,
            'polarization_equation':max(max(r['polarization_residual_abs']) for r in rows)<1e-12}
    result={'checks':checks,'all_pass':all(checks.values()),'rows':rows,'runtime_seconds':time.perf_counter()-start,
            'scope':'3 deterministic tangent configurations on Pi>0 in flat1+1; generic tensor derivation is separate',
            'direct_L':'C(Q-1)^2(1+alpha Pi+beta Pi^2)-P.dlnQ-W-gamma Pi^2/2+lambda n.P'}
    from pathlib import Path
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['all_pass']


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
