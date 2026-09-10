#!/usr/bin/env python3
"""Exact vacuum inverse homogeneity; no empirical gravity normalization.

The geometry symbols below are independent of the amplitude scale. The
formulae are the regular closed inverse at base f109d3d8ce1cdab6b5f63bea75bca83a8d4798f9.
They have the stated meaning only on its nonzero-denominator physical chart.
"""
from functools import lru_cache
import sympy as s


@lru_cache(None)
def model():
    r,B,F,X,U=s.symbols('r B F X U',positive=True)
    g,b,rho,ry=s.symbols('g b rho ry',real=True)
    w,f=s.symbols('w f',nonzero=True)
    j=s.Symbol('j',real=True)
    p=s.sqrt(B*U);Q=2*X+U;aa=g+2/r
    P=(2*w*aa+s.Rational(3,2)*w*w/F)/B
    L=2*F*rho+2*w*(g+b)/B+3*w*w/(F*B)
    S=2*F*aa*rho+4*w*(r*g-1)/(r*r*B)
    gamma=p*r*S/(2*Q*w)
    W=B*(L-X*r*S/Q)/2
    H=((2/r+w/F)*U-(2*g+w/F)*X)/p
    kappa=2*P/F+H*gamma
    Rrad=aa+s.Rational(3,2)*w/F
    A=s.Matrix([-2*gamma*Rrad/p,-gamma/U])
    coord=s.Symbol('y',real=True)
    variables=(X,F,coord,U,w)
    L0=s.Matrix([1,0,0,-2,0])
    L1=s.Matrix([0,1,1/(ry*w),-2*g*Q/w,W/w])
    scale_vector=s.Matrix([0,F,0,0,w])
    return dict(r=r,B=B,F=F,X=X,U=U,g=g,b=b,rho=rho,ry=ry,w=w,f=f,j=j,
        p=p,Q=Q,P=P,L=L,S=S,gamma=gamma,W=W,H=H,kappa=kappa,Rrad=Rrad,A=A,
        Dcoord=1+r*w/(2*F),Dfield=2*(F-X*f),z=w/f,zr=W/f-j*(w/f)**2/f,
        variables=variables,L0=L0,L1=L1,scale_vector=scale_vector)


def derivative(expression,variables,vector):
    return sum(s.diff(expression,x)*v for x,v in zip(variables,vector))


def bracket(left,right,variables):
    return s.Matrix([derivative(r,variables,left)-derivative(l,variables,right)
                     for l,r in zip(left,right)])


F_SCALE_WEIGHTS={
    'P':1,'L':1,'S':1,'W':1,'kappa':0,'gamma':0,'H':0,'Rrad':0,
    'Dcoord':0,'Dfield':1,'z':0,'zr':0,
}

CLOCK_SCALE_WEIGHTS={
    'P':0,'L':0,'S':0,'W':0,'kappa':0,'gamma':-s.Rational(1,2),
    'H':s.Rational(1,2),'Rrad':0,'Dcoord':0,'Dfield':0,'z':1,'zr':1,
}
