"""Martin hep-ph/0111209v2 vacuum masters; loop factors excluded.

I(x,y,z,Q2), J(x,Q2), J2(x,y,Q2) return ordinary floats and cache calls.
Arguments are nonnegative squared masses and a positive squared scale.
Negative masses are rejected, never clipped or absolute-valued.
I_mp/J_mp offer explicit arbitrary precision using the active mpmath context.
"""
from functools import lru_cache
import math

import mpmath as mp
import numpy as np
from scipy.special import spence


def _float_args(values,Q2):
    v=tuple(float(x) for x in values);q=float(Q2)
    if not all(math.isfinite(x) and x>=0 for x in v):
        raise ValueError('Squared masses must be finite and nonnegative')
    if not math.isfinite(q) or q<=0:
        raise ValueError('Q2 must be finite and strictly positive')
    return v,q


def _mp_args(values,Q2):
    v=tuple(mp.mpf(x) for x in values);q=mp.mpf(Q2)
    if not all(mp.isfinite(x) and x>=0 for x in v):
        raise ValueError('Squared masses must be finite and nonnegative')
    if not mp.isfinite(q) or q<=0:
        raise ValueError('Q2 must be finite and strictly positive')
    return v,q


def J_mp(x,Q2=1):
    (x,),q=_mp_args((x,),Q2)
    return x*(mp.log(x)-mp.log(q)-1) if x else mp.mpf(0)


def I_mp(x,y,z,Q2=1):
    """Real nonnegative-mass sunset; arbitrary precision, no loop factor."""
    args,q=_mp_args((x,y,z),Q2);x,y,z=sorted(args)
    if not z:return mp.mpf(0)
    lz=mp.log(z)-mp.log(q)
    if not y:return z*(-lz**2/2+2*lz-mp.mpf('2.5')-mp.pi**2/6)
    ly=mp.log(y)-mp.log(q)
    if not x:
        if y==z:return z*(-lz**2+4*lz-5)
        # Source Eq2.26 with its first positive argument chosen largest.
        return ((z-y)*(mp.polylog(2,y/z)-mp.log(z/y)*(mp.log(z-y)-mp.log(q))
                        +lz**2/2-mp.pi**2/6)
                -mp.mpf('2.5')*(z+y)+2*z*lz+2*y*ly-z*lz*ly)
    lx=mp.log(x)-mp.log(q)
    R=mp.sqrt(x*x+y*y+z*z-2*(x*y+x*z+y*z))
    if R==0:
        xi=mp.mpf(0)
    else:
        # Rationalized source arguments avoid subtractive loss for x/z small.
        u=2*x/(z+x-y+R);v=2*y/(z+y-x+R)
        xi=R*(2*mp.log(u)*mp.log(v)-mp.log(x/z)*mp.log(y/z)
              -2*mp.polylog(2,u)-2*mp.polylog(2,v)+mp.pi**2/3)
    val=((x-y-z)*ly*lz+(y-x-z)*lx*lz+(z-x-y)*lx*ly)/2
    val+=2*(x*lx+y*ly+z*lz)-mp.mpf('2.5')*(x+y+z)-xi/2
    scale=(x+y+z)*(1+abs(lx)+abs(ly)+abs(lz))**2
    if abs(mp.im(val))>mp.power(10,-mp.mp.dps+8)*max(scale,mp.mpf(1)):
        raise ArithmeticError('Sunset branch left a resolved imaginary residual')
    return mp.re(val)


@lru_cache(maxsize=65536)
def _J_cached(x,Q2):
    return x*(math.log(x)-math.log(Q2)-1) if x else 0.


def J(x,Q2=1.):
    (x,),q=_float_args((x,),Q2)
    return _J_cached(x,q)


def J2(x,y,Q2=1.):
    return J(x,Q2)*J(y,Q2)


@lru_cache(maxsize=65536)
def _I_cached(x,y,z,Q2):
    if not z:return 0.
    ell=math.log(z)-math.log(Q2)
    if not y:return z*(-ell*ell/2+2*ell-2.5-math.pi**2/6)
    if not x:
        if y==z:return z*(-ell*ell+4*ell-5)
        r=y/z
        if r<1e-12:
            with mp.workdps(60):return float(I_mp(x,y,z,Q2))
        lr=math.log(r);ly=ell+lr
        return z*((1-r)*(float(spence(1-r))+lr*(ell+math.log1p(-r))
                          +ell*ell/2-math.pi**2/6)
                  -2.5*(1+r)+2*ell+2*r*ly-ell*ly)
    r=x/z;s=y/z
    if r<1e-12 or abs(ell)>100:
        with mp.workdps(60):return float(I_mp(x,y,z,Q2))
    lr=math.log(r);ls=math.log(s);lx=ell+lr;ly=ell+ls
    delta=r*r+s*s+1-2*(r*s+r+s)
    R=np.sqrt(complex(delta))
    if R==0:xi=0j
    else:
        u=2*r/(1+r-s+R);v=2*s/(1+s-r+R)
        xi=R*(2*np.log(u)*np.log(v)-lr*ls-2*spence(1-u)-2*spence(1-v)+math.pi**2/3)
    val=((r-s-1)*ly*ell+(s-r-1)*lx*ell+(1-r-s)*lx*ly)/2
    val+=2*(r*lx+s*ly+ell)-2.5*(r+s+1)-xi/2
    scale=(r+s+1)*(1+abs(lx)+abs(ly)+abs(ell))**2
    if abs(val.imag)>1e-12*max(1.,scale):
        with mp.workdps(60):return float(I_mp(x,y,z,Q2))
    return float(z*val.real)


def I(x,y,z,Q2=1.):
    args,q=_float_args((x,y,z),Q2)
    return _I_cached(*sorted(args),q)


def fSSS(x,y,z,Q2=1.):return -I(x,y,z,Q2)
def fSS(x,y,Q2=1.):return J2(x,y,Q2)
def fFFS(x,y,z,Q2=1.):
    return J2(x,y,Q2)-J2(x,z,Q2)-J2(y,z,Q2)+(x+y-z)*I(x,y,z,Q2)
def fbarFFS(x,y,z,Q2=1.):return 2*I(x,y,z,Q2)


def cache_info():return {'I':_I_cached.cache_info(),'J':_J_cached.cache_info()}
def clear_cache():_I_cached.cache_clear();_J_cached.cache_clear()
