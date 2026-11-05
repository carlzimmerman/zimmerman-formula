#!/usr/bin/env python3
"""Combined enclosed-mass positive branch; no nonlinear superposition."""
import math
import numpy as np
from scipy.integrate import cumulative_simpson
from scipy.interpolate import PchipInterpolator
import bullet_source as B

def radial_derivative(r,epsilon,rows=None):
    r=np.asarray(r,float)
    q=B.spherical_mass(r*B.L0_KPC,rows)/(4*math.pi*B.RHO_REF*B.L0_KPC**3)
    return B.positive_root(r,q,epsilon)

def radial_eigenvalues(r,epsilon,rows=None):
    r=np.asarray(r,float)
    rows=B.components() if rows is None else np.asarray(rows,float)
    # The radial approximation puts every centre at the origin.
    recentered=rows.copy();recentered[:,2:]=0.
    source=B.density(r*B.L0_KPC,0.,0.,recentered)/B.RHO_REF
    y=radial_derivative(r,epsilon,rows)
    tangent=np.zeros_like(r);np.divide(y,r,out=tangent,where=r>0)
    # Solve 6 lambda^2 + 3 epsilon lambda = S(0) without cancellation.
    central=2*source/(3*epsilon+np.sqrt(9*epsilon**2+24*source))
    tangent=np.where(r==0,central,tangent)
    # Differentiate epsilon*r^2*y+2*r*y^2=Q, with Q'=r^2*S.
    radial=(source-2*epsilon*tangent-2*tangent*tangent)/(epsilon+4*tangent)
    radial=np.where(r==0,tangent,radial)
    return radial,tangent

class RadialPotential:
    def __init__(self,epsilon,max_radius,points=8192,rows=None):
        if epsilon<=0 or max_radius<=1e-6 or points<4:raise ValueError('Invalid radial table domain')
        self.epsilon=float(epsilon);self.max_radius=float(max_radius)
        self.rows=B.components() if rows is None else np.asarray(rows,float)
        radii=np.geomspace(1e-6,max_radius,points)
        derivative=radial_derivative(radii,epsilon,self.rows)
        central=float(radial_eigenvalues(0.,epsilon,self.rows)[0])
        # Missing central interval is analytic to O(r_min^4).
        initial=.5*central*radii[0]**2
        potential=cumulative_simpson(derivative,x=radii,initial=0.)+initial
        self.interpolator=PchipInterpolator(np.r_[0.,radii],np.r_[0.,potential],extrapolate=False)
    def __call__(self,r):
        r=np.asarray(r,float)
        if np.any(~np.isfinite(r)) or np.any(r<0) or np.any(r>self.max_radius):raise ValueError('Radius outside boundary table')
        return self.interpolator(r)
