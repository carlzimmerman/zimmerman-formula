"""Exact spherical reduction of KT37, for smooth isolated source diagnostics."""
import numpy as np
import law


def plummer_fields(r,GM,a):
    r=np.asarray(r,dtype=float);q=r*r+a*a
    g=GM*r/q**1.5
    gp=GM*(a*a-2*r*r)/q**2.5
    gpp=GM*r*(6*r*r-9*a*a)/q**3.5
    return g,gp,gpp


def radial_force(r,g,gp,gpp,ell,a0=1.,newtonian=False):
    r,g,gp,gpp=np.broadcast_arrays(np.asarray(r,float),np.asarray(g,float),np.asarray(gp,float),np.asarray(gpp,float))
    if np.any(r<=0):raise ValueError('radial formula requires r>0; use analytic central limit')
    if newtonian:
        zero=np.zeros_like(g)
        return dict(total=g,phantom=zero,A=zero,Br=zero,Bt=zero,energy=g*g,x=g*g/a0**2,z=g*g/a0**2)
    x=g*g/a0**2;z=x+ell**2/a0**2*(gp*gp+2*(g/r)**2)
    if np.any(z<=0):raise ValueError('joint zero jet needs the continuous tensor limit')
    rm=law.Rminus1(z);d=law.zRprime(z);f=x/z;rp=d/z
    rpp=law.Rsecond(z)
    c=rm+f*d;coefficient=ell**2*f*d
    xp=2*g*gp/a0**2
    zp=xp+2*ell**2/a0**2*(gp*gpp+2*(g/r)*(gp/r-g/r**2))
    coefficient_prime=ell**2*(xp*rp+x*rpp*zp)
    A=c*g;Br=coefficient*gp;Bt=coefficient*g/r
    phantom=A-coefficient_prime*gp-coefficient*(gpp+2*gp/r-2*g/r**2)
    return dict(total=g+phantom,phantom=phantom,A=A,Br=Br,Bt=Bt,
                energy=g*g*(1+rm),x=x,z=z)
