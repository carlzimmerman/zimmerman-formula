#!/usr/bin/env python3
"""Second-order physical-coordinate Hessians for the stretched full3D box."""
import math,os
import numpy as np
from scipy.optimize import brentq
import bullet_source as B

def expanded_alpha(half_width_kpc):
    target=4000.*3/math.sinh(3)
    if half_width_kpc<target:raise ValueError('No positive mapping alpha for requested centre spacing')
    return float(brentq(lambda a:half_width_kpc*a/math.sinh(a)-target,1e-8,30.,xtol=1e-13))

class Grid:
    def __init__(self,n,half_width_kpc=4000.,alpha=3.,centre_kpc=(0.,0.,0.)):
        if not isinstance(n,int) or n<4 or n%2:raise ValueError('Even interval count>=4 required')
        if n>16 and not os.environ.get('HEAVYQ_JOB_ID'):raise RuntimeError('N>16 grid requires heavyq')
        if half_width_kpc<=0 or alpha<=0:raise ValueError('Positive box and mapping required')
        self.n=n;self.half_width_kpc=float(half_width_kpc);self.alpha=float(alpha);self.centre_kpc=np.asarray(centre_kpc,float)
        if self.centre_kpc.shape!=(3,):raise ValueError('Three centre coordinates required')
        u=np.linspace(-1,1,n+1);self.offset=half_width_kpc/B.L0_KPC*np.sinh(alpha*u)/math.sinh(alpha)
        self.axes=[self.offset+c/B.L0_KPC for c in self.centre_kpc];self.shape=(n+1,)*3;self.interior=(n-1,)*3
        hm=self.offset[1:-1]-self.offset[:-2];hp=self.offset[2:]-self.offset[1:-1]
        first=[-hp/(hm*(hm+hp)),(hp-hm)/(hm*hp),hm/(hp*(hm+hp))]
        second=[2/(hm*(hm+hp)),-2/(hm*hp),2/(hp*(hm+hp))]
        self.first=[];self.second=[]
        for axis in range(3):
            shape=[1,1,1];shape[axis]=n-1
            self.first.append([v.reshape(shape) for v in first]);self.second.append([v.reshape(shape) for v in second])
    def coordinates(self):return np.meshgrid(*self.axes,indexing='ij',sparse=True)
    def with_interior(self,values):
        out=np.zeros(self.shape);out[1:-1,1:-1,1:-1]=np.asarray(values).reshape(self.interior);return out

def hessian(grid,phi):
    phi=np.asarray(phi)
    if phi.shape!=grid.shape:raise ValueError('Field/grid shape mismatch')
    centre=phi[1:-1,1:-1,1:-1];parts=[]
    shifts=[slice(None,-2),slice(1,-1),slice(2,None)]
    def view(changes):
        indices=[shifts[1]]*3
        for axis,position in changes:indices[axis]=shifts[position]
        return phi[tuple(indices)]
    # Three-point nonuniform physical derivatives exactly differentiate any
    # quadratic, unlike applying a discrete chain rule to sinh coordinates.
    for axis in range(3):
        parts.append(grid.second[axis][0]*(view([(axis,0)])-centre)+grid.second[axis][2]*(view([(axis,2)])-centre))
    for a,b in [(0,1),(0,2),(1,2)]:
        mixed=np.zeros(grid.interior)
        for i in (0,2):
            for j in (0,2):
                difference=view([(a,i),(b,j)])-view([(a,i)])-view([(b,j)])+centre
                mixed+=grid.first[a][i]*grid.first[b][j]*difference
        parts.append(mixed)
    return parts

def operator(h,epsilon):
    xx,yy,zz,xy,xz,yz=h
    return epsilon*(xx+yy+zz)+2*(xx*yy+xx*zz+yy*zz-xy*xy-xz*xz-yz*yz)

def jacobian_product(h,dh,epsilon):
    xx,yy,zz,xy,xz,yz=h;dx,dy,dz,dxy,dxz,dyz=dh
    return (epsilon+2*(yy+zz))*dx+(epsilon+2*(xx+zz))*dy+(epsilon+2*(xx+yy))*dz-4*(xy*dxy+xz*dxz+yz*dyz)

def principal_min(h,epsilon,chunk=8):
    xx,yy,zz,xy,xz,yz=h;minimum=math.inf
    for lo in range(0,xx.shape[0],chunk):
        sl=slice(lo,lo+chunk);shape=xx[sl].shape;matrix=np.empty(shape+(3,3))
        matrix[...,0,0]=epsilon+2*(yy[sl]+zz[sl]);matrix[...,1,1]=epsilon+2*(xx[sl]+zz[sl]);matrix[...,2,2]=epsilon+2*(xx[sl]+yy[sl])
        matrix[...,0,1]=matrix[...,1,0]=-2*xy[sl];matrix[...,0,2]=matrix[...,2,0]=-2*xz[sl];matrix[...,1,2]=matrix[...,2,1]=-2*yz[sl]
        minimum=min(minimum,float(np.linalg.eigvalsh(matrix)[...,0].min()))
    return minimum

def selector(h,mutate=False):
    xx,yy,zz,xy,xz,yz=h;norm2=xx*xx+yy*yy+zz*zz+2*(xy*xy+xz*xz+yz*yz)
    determinant=xx*yy*zz+2*xy*xz*yz-xx*yz*yz-yy*xz*xz-zz*xy*xy
    out=np.zeros_like(norm2);np.divide(3*math.sqrt(3)*determinant,norm2**1.5,out=out,where=norm2>0)
    return (-out if mutate else out),np.sqrt(norm2)
