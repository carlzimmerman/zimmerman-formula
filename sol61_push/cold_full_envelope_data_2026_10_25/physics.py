"""Spherical diagnostics only; pc, km/s, Msun. No action bridge implied."""
import math
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.special import ndtr
from numpy.polynomial.legendre import leggauss
G=.00430091
A0={'canonical':9.3603e-11*3.085677581491367e10,'alt':1.1312e-10*3.085677581491367e10}
def project(R,a,gfun,beta=0.,nr=4096,nz=128):
 r=np.geomspace(.001,1e7,nr);nu=(1+(r/a)**2)**(-2.5)
 integ=-cumulative_trapezoid((nu*gfun(r)*r**(2*beta))[::-1],r[::-1],initial=0)[::-1]
 pressure=r**(-2*beta)*integ
 x,w=leggauss(nz);t=(x+1)*math.pi/4;w=w*math.pi/4
 z=a*np.tan(t);jac=a/np.cos(t)**2;rr=np.sqrt(R[:,None]**2+z*z)
 pp=np.interp(np.log(rr),np.log(r),pressure);nn=(1+(rr/a)**2)**(-2.5)
 return np.sum(w*jac*(1-beta*R[:,None]**2/rr**2)*pp,axis=1)/np.sum(w*jac*nn,axis=1)
def g_cold(q,r,dm):
 # A discrete spherical-shell diagnostic. No cold mass added to baryonic Xi.
 ix=np.searchsorted(r,q,side='right');cdf=np.r_[0,np.cumsum(dm)]
 return G*cdf[ix]/np.maximum(q*q,1e-300)
def shell_potential(q,r,dm):
 ix=np.searchsorted(r,q,side='right');cdf=np.r_[0,np.cumsum(dm)];outer=np.r_[np.cumsum((dm/r)[::-1])[::-1],0]
 return -G*(np.divide(cdf[ix],q,out=np.zeros_like(np.asarray(q,dtype=float)),where=np.asarray(q)>0)+outer[ix])
def window_logpdf(v,mean,var,lo,hi):
 norm=np.maximum(ndtr((hi-mean)/np.sqrt(var))-ndtr((lo-mean)/np.sqrt(var)),1e-300)
 return -.5*(np.log(2*np.pi*var)+(v-mean)**2/var)-np.log(norm)
def baryon_g(r,ms,aa,foot):
 gn=sum(G*ms/len(aa)*r/(r*r+a*a)**1.5 for a in aa)
 return .5*(gn+np.sqrt(gn*gn+4*A0[foot]*gn))
def plummer_g(r,m,b):return G*m*r/(r*r+b*b)**1.5
