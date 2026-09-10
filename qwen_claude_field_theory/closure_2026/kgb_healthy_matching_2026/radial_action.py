#!/usr/bin/env python3
"""Varied static radial action for the luminal quadratic DHOST extension.

This gauge-reduced variation supplies necessary radial equations, NOT the
missing off-diagonal metric equation, full canonical closure, or stability.
X is an auxiliary variable constrained to -(grad phi)^2/2; it is not counted
as an independently certified propagating or nonpropagating degree of freedom.
"""
import argparse,json
from functools import lru_cache
from pathlib import Path
import sympy as s

@lru_cache(None)
def build():
    names='r q N N1 N2 B B1 B2 p p1 p2 X X1 X2 lam lam1 F f j P Px Gx Gxx D Dx'
    v=dict(zip(names.split(),s.symbols(names,nonzero=True)))
    r,q,N,B,p,X,lam,F,f,P,Gx,D=[v[k] for k in ('r','q','N','B','p','X','lam','F','f','P','Gx','D')]
    N1,N2,B1,p1,z=[v[k] for k in ('N1','N2','B1','p1','X1')]
    pairs=[(v[k],v[k+'1']) for k in ('N','B','p','X','lam')]
    pairs += [(v[k+'1'],v[k+'2']) for k in ('N','B','p','X')]
    pairs += [(F,f*z),(f,v['j']*z),(P,v['Px']*z),(Gx,v['Gxx']*z),(D,v['Dx']*z)]
    def dr(expr):return s.diff(expr,r)+sum(s.diff(expr,k)*value for k,value in pairs)
    measure=N*s.sqrt(B)*r*r;g=N1/N;b=B1/(2*B)
    box=(p1+(g-b+2/r)*p)/B
    L3=-box*p*z/B;L4=z*z/B;L5=p*p*z*z/(B*B)
    A4=3*f*f/(2*F)-(F-X*f)*D/F-X*X*D*D/(2*F)
    A5=-(f+X*D)*D/F
    constraint=X-q*q/(2*N*N)+p*p/(2*B)
    Ricci=2*(1-1/B)/(r*r)-4*g/(B*r)+2*B1/(B*B*r)-2*N2/(N*B)+N1*B1/(N*B*B)
    LR=2*N*F*(B-1)/s.sqrt(B)+2*r*N*F*B1/B**s.Rational(3,2)+2*r*r*f*z*N1/s.sqrt(B)
    boundary=-2*r*r*F*N1/s.sqrt(B)
    L=LR+measure*(P+Gx*p*z/B+D*L3+A4*L4+A5*L5+lam*constraint)
    EL={k:s.factor(s.diff(L,v[k])-dr(s.diff(L,v[k+'1']))) for k in ('N','B')}
    # X variation must vary the action functions, not just explicit X factors.
    dX=s.diff(L,X)+sum(s.diff(L,k)*value for k,value in
        [(F,f),(f,v['j']),(P,v['Px']),(Gx,v['Gxx']),(D,v['Dx'])])
    EL['X']=s.factor(dX-dr(s.diff(L,z)))
    EL['lam']=s.diff(L,lam)
    current=s.factor(s.diff(L,p)-dr(s.diff(L,p1)))
    return dict(symbols=v,measure=measure,L=L,LR=LR,Ricci=Ricci,box=box,
        A4=A4,A5=A5,L3=L3,L4=L4,L5=L5,EL=EL,current=current,
        EH_boundary_residual=s.factor(measure*F*Ricci-LR-dr(boundary)))

def run():
    a=build()
    return dict(convention='X=-grad(phi)^2/2, ds2=-N^2 dt2+B dr2+r2 dOmega2, phi=q t+psi(r), p=psi_prime',
        coefficients={k:str(a[k]) for k in ('A4','A5')},
        radial_density=str(a['L']),Euler_Lagrange={k:str(value) for k,value in a['EL'].items()},
        scalar_current=str(a['current']),scalar_equation='d(current)/dr = 0',
        EH_boundary_residual=str(a['EH_boundary_residual']),
        scope='Necessary diagonal static radial equations with auxiliary X. The omitted metric shift/angular variations and temporal Dirac preservation remain required. No MOND/PPN/health solution claimed.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    payload=json.dumps(run(),indent=2)+'\n'
    if args.result_file:args.result_file.write_text(payload)
    else:print(payload)
