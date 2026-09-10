#!/usr/bin/env python3
"""Exact-form common-j discriminator for the supplied local EF pencils.

Mathematical hypotheses: beta>0, R<0, K=K0+A*j,
T=beta*(K-I), fixed real b, and the stated strict null-cone criterion.
Numerical callers inherit uncertainty in their principal coefficients.
Pass sqrt=sympy.sqrt and exact inputs to retain algebraic endpoints.
"""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Pencil:
    K0: object
    A: object
    I: object
    R: object
    b: object
    beta: object
    label: str = ''


def stationary_polynomial(t,I,R,c,beta):
    return beta*c*t*t-(beta*I+(1+beta)*R)*t+(1+beta)*c


def lower_bound(I,R,b,beta,*,sqrt=math.sqrt):
    """Return max L(t), maximizing t, and complete branch classification."""
    if not all(math.isfinite(float(x)) for x in (I,R,b,beta)):
        raise ValueError('finite real coefficient data required')
    if beta<=0 or R>=0:
        raise ValueError('this reduction requires beta>0 and R<0')
    c=abs(b);S=beta*I+(1+beta)*R
    if c==0:
        if S>0:t,sector=0,'endpoint_zero'
        elif S<0:t,sector=1,'endpoint_one'
        else:t,sector=0,'constant'
    elif S<=c*(1+2*beta):t,sector=1,'endpoint_one'
    else:
        # Rationalized smaller root avoids S-sqrt(S²-small) cancellation.
        t=2*c*(1+beta)/(S+sqrt(S*S-4*beta*(1+beta)*c*c))
        sector='interior'
    D=1+beta*(1-t*t)
    L=(beta*I*(1-t*t)+2*c*t-R*t*t)/D
    return dict(lower=L,t=t,sector=sector,S=S)


def pencil_interval(p,*,sqrt=math.sqrt):
    if not all(math.isfinite(float(x)) for x in (p.K0,p.A)):
        raise ValueError('finite real affine coefficients required')
    bound=lower_bound(p.I,p.R,p.b,p.beta,sqrt=sqrt)
    lo,hi=bound['lower'],p.I
    out=dict(label=p.label,K_lower=lo,K_upper=hi,extremum=bound)
    if lo>=hi:
        return dict(out,status='empty',lower=None,upper=None,reason='empty K interval')
    if p.A==0:
        healthy=lo<p.K0<hi
        return dict(out,status='nonempty' if healthy else 'empty',
                    lower=-math.inf if healthy else None,
                    upper=math.inf if healthy else None,
                    reason='fixed healthy pencil' if healthy else 'fixed unhealthy pencil')
    ends=((lo-p.K0)/p.A,(hi-p.K0)/p.A)
    return dict(out,status='nonempty',lower=min(ends),upper=max(ends),reason='open affine preimage')


def common_interval(pencils,*,sqrt=math.sqrt):
    """Intersect open intervals; never choose a different j for each pencil."""
    pencils=list(pencils)
    if not pencils:raise ValueError('at least one actual or explicitly labeled test pencil required')
    rows=[pencil_interval(p,sqrt=sqrt) for p in pencils]
    if any(x['status']=='empty' for x in rows):
        return dict(status='empty',lower=None,upper=None,witness=None,pencils=rows)
    lo=max(x['lower'] for x in rows);hi=min(x['upper'] for x in rows)
    if lo>=hi:return dict(status='empty',lower=lo,upper=hi,witness=None,pencils=rows)
    if math.isinf(float(lo)) and math.isinf(float(hi)):j=0
    elif math.isinf(float(lo)):j=hi-1
    elif math.isinf(float(hi)):j=lo+1
    else:j=(lo+hi)/2
    return dict(status='nonempty',lower=lo,upper=hi,witness=j,pencils=rows)


def direct_health(p,j):
    """Independent minimization of q at fixed j, not maximization of L."""
    K=p.K0+p.A*j;T=p.beta*(K-p.I);c=abs(p.b)
    points=[0,1]
    if p.R>T:
        vertex=c/(p.R-T)
        if 0<vertex<1:points.append(vertex)
    margin=min(K+T-2*c*t+(p.R-T)*t*t for t in points)
    return dict(K=K,T=T,margin=margin,
                healthy=bool(K>0 and p.R<0 and T<0 and K>c and margin>0))
