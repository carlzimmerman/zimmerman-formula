#!/usr/bin/env python3
"""Finite-source axisymmetric exponential AQUAL, varied before discretization.

Units: length b, acceleration a0, potential a0*b, source mass M.
eta=GM/(a0*b²). The source and tracer are the same prescribed spherical
profile, normalized to unit mass. This is a nonrelativistic action diagnostic,
not a demonstrated reduction of the repository's relativistic P/W action.

Minimize ∫R dR dz [G(|grad Phi|)/2+4pi eta rho Phi], with Dirichlet
boundary data and natural regularity at the axis. Q1 finite elements and
Gauss quadrature give a symmetric variational Hessian. No mu floor is used.
"""
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy.integrate import quad, cumulative_trapezoid
from scipy.interpolate import PchipInterpolator
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def mu(y):
    return -np.expm1(-np.asarray(y))


def primitive(y):
    y=np.asarray(y,dtype=float)
    # Integrate the exponential power series before subtracting O(y²) terms.
    coefficients=[2*(-1)**(n+1)/(math.factorial(n)*(n+2)) for n in range(1,17)]
    small=y**3*np.polynomial.polynomial.polyval(y,coefficients)
    return np.where(y<1.,small,y*y+2*((1+y)*np.exp(-y)-1))


def invert_mu(source):
    s=np.asarray(source,dtype=float)
    if np.any(s<0): raise ValueError('source must be nonnegative')
    x=np.sqrt(s)+s
    for _ in range(30):
        den=mu(x)+x*np.exp(-x)
        step=np.divide(x*mu(x)-s,den,out=np.zeros_like(x),where=den>0)
        new=x-step
        new=np.where(new<0,x/2,new)
        if np.max(abs(new-x)/np.maximum(x,1e-150))<3e-15:
            x=new;break
        x=new
    return x


class Plummer:
    @staticmethod
    def density(r): return 3/(4*np.pi)*(1+np.asarray(r)**2)**(-2.5)
    @staticmethod
    def mass(r): return np.asarray(r)**3/(1+np.asarray(r)**2)**1.5


def spherical_virial(eta,newtonian=False,profile=None):
    """One-component global second moment, not a finite-aperture observable."""
    p=profile or Plummer()
    def integrand(r):
        gN=eta*p.mass(r)/(r*r)
        g=gN if newtonian else float(invert_mu(gN))
        return 4*np.pi/3*p.density(r)*g*r**3
    return quad(integrand,0,np.inf,epsabs=1e-11,epsrel=1e-9,limit=200)[0]


class Mesh:
    def __init__(self,nr=49,nz=97,extent=32.,quadrature=3):
        if nr<3 or nz<3 or extent<=0: raise ValueError('invalid mesh')
        self.nr,self.nz,self.extent=nr,nz,extent
        scale=np.arcsinh(extent)
        rr=np.sinh(np.linspace(0,scale,nr))
        zz=np.sinh(np.linspace(-scale,scale,nz))
        R,Z=np.meshgrid(rr,zz,indexing='ij')
        self.nodes=np.column_stack((R.ravel(),Z.ravel()))
        i,j=np.meshgrid(np.arange(nr-1),np.arange(nz-1),indexing='ij')
        self.ids=np.stack((i*nz+j,(i+1)*nz+j,(i+1)*nz+j+1,i*nz+j+1),axis=-1).reshape(-1,4)
        corners=self.nodes[self.ids]
        dr=corners[:,1,0]-corners[:,0,0]
        dz=corners[:,3,1]-corners[:,0,1]
        x,w=np.polynomial.legendre.leggauss(quadrature)
        shape=[];grad=[];weight=[]
        for a,wa in zip(x,w):
            for b,wb in zip(x,w):
                shape.append(np.array([(1-a)*(1-b),(1+a)*(1-b),(1+a)*(1+b),(1-a)*(1+b)])/4)
                dR=np.array([-(1-b),(1-b),(1+b),-(1+b)])/2
                dZ=np.array([-(1-a),-(1+a),(1+a),(1-a)])/2
                grad.append(np.stack((dR[None,:]/dr[:,None],dZ[None,:]/dz[:,None]),axis=-1))
                weight.append(wa*wb*dr*dz/4)
        self.shape=np.array(shape)
        self.grad=np.stack(grad,axis=1)
        self.points=np.einsum('qa,eac->eqc',self.shape,corners)
        self.weight=np.stack(weight,axis=1)*self.points[:,:,0]
        boundary=(R==rr[-1])|(Z==zz[0])|(Z==zz[-1])
        self.free=np.flatnonzero(~boundary.ravel())
        self.fixed=np.flatnonzero(boundary.ravel())
        self.rows=np.repeat(self.ids,4,axis=1).ravel()
        self.cols=np.tile(self.ids,(1,4)).ravel()


def assemble(mesh,phi,eta,profile=None,newtonian=False,hessian=True,external=0.):
    p=profile or Plummer()
    internal=np.einsum('eqac,ea->eqc',mesh.grad,phi[mesh.ids])
    background=np.array([0.,-external])
    g=internal+background
    y=np.linalg.norm(g,axis=-1)
    mm=np.ones_like(y) if newtonian else mu(y)
    rho=p.density(np.linalg.norm(mesh.points,axis=-1))
    source=4*np.pi*eta*rho
    if external:
        # Constant external flux has zero weak divergence. Subtract it before
        # assembly, using a stable norm difference when internal << external.
        delta_y=(np.sum(internal*internal,axis=-1)-2*external*internal[:,:,1])/(y+external)
        delta_mu=np.zeros_like(y) if newtonian else -np.exp(-external)*np.expm1(-delta_y)
        flux=mm[:,:,None]*internal+delta_mu[:,:,None]*background
    else:
        flux=mm[:,:,None]*g
    local=np.einsum('eq,eqc,eqac->ea',mesh.weight,flux,mesh.grad)
    local+=np.einsum('eq,eq,qa->ea',mesh.weight,source,mesh.shape)
    residual=np.bincount(mesh.ids.ravel(),weights=local.ravel(),minlength=len(phi))
    matrix=None
    if hessian:
        dot=np.einsum('eqac,eqc->eqa',mesh.grad,g)
        slope=np.zeros_like(y) if newtonian else np.divide(np.exp(-y),y,out=np.zeros_like(y),where=y>0)
        hh=np.einsum('eq,eq,eqac,eqbc->eab',mesh.weight,mm,mesh.grad,mesh.grad)
        hh+=np.einsum('eq,eq,eqa,eqb->eab',mesh.weight,slope,dot,dot)
        matrix=coo_matrix((hh.ravel(),(mesh.rows,mesh.cols)),shape=(len(phi),len(phi))).tocsr()
    return residual,matrix,g,rho


def isolated_potential(radius,eta,profile=None,newtonian=False):
    p=profile or Plummer()
    # Only gradients are physical: choose the central potential equal to zero.
    grid=np.r_[0.,np.geomspace(1e-8,max(2.,float(np.max(radius))*1.01),8001)]
    source=np.divide(eta*p.mass(grid),grid**2,out=np.zeros_like(grid),where=grid>0)
    g=source if newtonian else invert_mu(source)
    integral=cumulative_trapezoid(g,grid,initial=0.)
    return PchipInterpolator(grid,integral)(radius)


def boundary_potential(mesh,eta,external,profile=None,newtonian=False):
    R,Z=mesh.nodes.T
    radius=np.hypot(R,Z)
    if external==0:
        return isolated_potential(radius,eta,profile,newtonian)
    if newtonian and profile is None:
        return -eta/np.sqrt(1+radius**2)-external*Z
    mm=1. if newtonian else float(mu(external))
    L=0. if newtonian else external*np.exp(-external)/mm
    return -external*Z-eta/(mm*np.sqrt(1+Z*Z+(1+L)*R*R))


def virial(mesh,g,rho,external):
    """Stationary global tracer virial tensor; existence of a DF not proved."""
    internal=g.copy();internal[:,:,1]+=external
    weight=2*np.pi*mesh.weight*rho
    mass=float(np.sum(weight))
    perp=float(np.sum(weight*mesh.points[:,:,0]*internal[:,:,0]/2))
    parallel=float(np.sum(weight*mesh.points[:,:,1]*internal[:,:,1]))
    net_force=np.sum(weight[:,:,None]*internal,axis=(0,1))
    # Do not renormalize away missing outer tracer mass.
    return dict(virial_perpendicular=perp,virial_parallel=parallel,
                virial_trace=2*perp+parallel,quadrature_mass=mass,
                net_force_z=float(net_force[1]))


def solve(eta,external,nr=49,nz=97,extent=None,newtonian=False,profile=None,
          tolerance=3e-10,maxiter=40):
    if eta<=0 or external<0: raise ValueError('eta>0, external>=0 required')
    if extent is None: extent=max(32.,8*np.sqrt(eta)/external) if external else 32.
    started=time.perf_counter()
    mesh=Mesh(nr,nz,extent)
    # Store the internal potential; never differentiate a large affine field
    # numerically and then subtract it to recover the tiny internal gradient.
    phi=boundary_potential(mesh,eta,external,profile,newtonian)+external*mesh.nodes[:,1]
    density=(profile or Plummer()).density(np.linalg.norm(mesh.points,axis=-1))
    load=np.einsum('eq,eq,qa->ea',mesh.weight,4*np.pi*eta*density,mesh.shape)
    load=np.bincount(mesh.ids.ravel(),weights=load.ravel(),minlength=len(phi))
    norm=max(np.linalg.norm(load[mesh.free]),1e-30)
    history=[]
    for iteration in range(maxiter):
        residual,H,g,rho=assemble(mesh,phi,eta,profile,newtonian,external=external)
        err=float(np.linalg.norm(residual[mesh.free])/norm)
        history.append(err)
        if err<tolerance: break
        step=np.zeros_like(phi)
        step[mesh.free]=spsolve(H[mesh.free][:,mesh.free],-residual[mesh.free])
        accepted=False
        for half in range(18):
            trial=phi+step*2.**(-half)
            rr=assemble(mesh,trial,eta,profile,newtonian,hessian=False,external=external)[0]
            if np.linalg.norm(rr[mesh.free])<np.linalg.norm(residual[mesh.free]):
                phi=trial;accepted=True;break
        if not accepted: break
    residual,_,g,rho=assemble(mesh,phi,eta,profile,newtonian,hessian=False,external=external)
    err=float(np.linalg.norm(residual[mesh.free])/norm)
    result=dict(eta=eta,external=external,nr=nr,nz=nz,extent=extent,newtonian=newtonian,
                profile=type(profile or Plummer()).__name__,converged=err<tolerance,
                residual_relative=err,iterations=iteration,residual_history=history,
                runtime_seconds=time.perf_counter()-started,
                source_load=float(np.sum(load)),
                # Sum reactions equals total load by exact partition of unity.
                boundary_flux_balance=float(np.sum(residual[mesh.fixed])/np.sum(load)),
                **virial(mesh,g,rho,external))
    return result


def jacobian_check():
    mesh=Mesh(7,13,8.)
    R,Z=mesh.nodes.T
    phi=-.06/np.sqrt(1+R*R+Z*Z)-.15*Z
    vector=np.sin(.7*R+.2*Z);vector[mesh.fixed]=0
    _,H,_,_=assemble(mesh,phi,.06)
    epsilon=1e-6
    finite=(assemble(mesh,phi+epsilon*vector,.06,hessian=False)[0]-
            assemble(mesh,phi-epsilon*vector,.06,hessian=False)[0])/(2*epsilon)
    exact=H@vector
    anti=H-H.T
    return dict(relative_error=float(np.linalg.norm((finite-exact)[mesh.free])/np.linalg.norm(exact[mesh.free])),
                symmetry_error=float(np.max(abs(anti.data))) if anti.nnz else 0.)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--eta',type=float,default=.06)
    parser.add_argument('--external',type=float,default=.17)
    parser.add_argument('--nr',type=int,default=49)
    parser.add_argument('--nz',type=int,default=97)
    parser.add_argument('--extent',type=float)
    parser.add_argument('--newtonian',action='store_true')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=solve(args.eta,args.external,args.nr,args.nz,args.extent,args.newtonian)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['converged'] else 1)
