#!/usr/bin/env python3
"""Integral of a regular even cubic-in-r² jet, with zero primitive at r=0."""
import numpy as np
from numpy.polynomial import polynomial as poly
from scipy.interpolate import CubicSpline


def integrate_even_jet(r,source):
    r=np.asarray(r,dtype=float);source=np.asarray(source,dtype=float)
    if r.ndim!=1 or source.shape!=r.shape or len(r)<4 or r[0]!=0 or np.any(np.diff(r)<=0):
        raise ValueError('increasing radial nodes starting at zero are required')
    if not np.all(np.isfinite(r)) or not np.all(np.isfinite(source)):
        raise ValueError('finite radial nodes and source required')
    fit=CubicSpline(r*r,source)
    integral=np.zeros(len(r))
    for i,step in enumerate(np.diff(r)):
        # Local coordinate u=r-r_i: r²-r_i²=2r_i u+u².
        # Avoid subtracting two large global polynomial primitives.
        z_offset=np.array([0.,2*r[i],1.])
        coefficients=np.zeros(7)
        for j in range(4):
            term=fit.c[j,i]*poly.polypow(z_offset,3-j)
            coefficients[:len(term)]+=term
        antiderivative=np.r_[0.,coefficients/np.arange(1,8)]
        integral[i+1]=integral[i]+poly.polyval(step,antiderivative)
    return integral
