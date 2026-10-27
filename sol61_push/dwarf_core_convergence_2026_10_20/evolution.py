"""Nested quiet phase sampling and fourth-order Hamiltonian stepping.

The physical collision operator is separate and only receives positive time.
The deterministic integrator uses the signed Yoshida/Forest–Ruth composition
of three second-order leapfrog maps. Discrete host receipts follow each kick.
"""
import numpy as np
from scipy.special import ndtri
from scipy.stats import qmc

G=.004498638185693768
MSTAR=574272.9377001019
MCOLD=53.64*MSTAR


def quiet_phases(count,seed):
    if count<1 or count&(count-1):
        raise ValueError('quiet raw phase count must be a positive power of two')
    return qmc.Sobol(d=6,scramble=True,seed=seed).random_base2(int(np.log2(count)))


def unit_ball(raw):
    raw=np.asarray(raw)
    radius=np.cbrt(raw[:,0]);z=2.*raw[:,1]-1.;phi=2.*np.pi*raw[:,2]
    transverse=np.sqrt(np.maximum(0.,1.-z*z))
    return radius[:,None]*np.c_[transverse*np.cos(phi),transverse*np.sin(phi),z]


def vector_J(x,v,m):
    return np.sum(np.cross(x,m[:,None]*v),axis=0)


def initial_conditions(ncold,nstar,seed,eps,gravity):
    """Same continuous initial law as v1, with nested raw quiet phases.

    Independent cold/star streams keep raw point prefixes nested. Normalizing
    velocity moments for each finite sample is recorded, so normalized particle
    velocities are not falsely claimed to be identical across N.
    """
    rawc=quiet_phases(ncold//2,seed);raws=quiet_phases(nstar//2,seed+1)
    xc=unit_ball(rawc)*[2000.,1600.,1200.]
    angle=np.deg2rad(37.);rot=np.array([[np.cos(angle),-np.sin(angle),0.],[np.sin(angle),np.cos(angle),0.],[0.,0.,1.]])
    xc=xc@rot.T;xc=np.r_[xc,-xc]
    fmax=(1500./np.sqrt(1500.**2+193.22**2))**3
    u=np.clip(raws[:,0]*fmax,1e-15,1.-1e-15)
    radius=193.22/np.sqrt(u**(-2./3.)-1.)
    ball=unit_ball(raws);direction=ball/np.linalg.norm(ball,axis=1)[:,None]
    xs=direction*radius[:,None];xs=np.r_[xs,-xs]
    x=np.r_[xc,xs];m=np.r_[np.full(ncold,MCOLD/ncold),np.full(nstar,MSTAR/nstar)]
    cold=np.arange(ncold+nstar)<ncold;a,U,_=gravity(x,m,eps)
    v=np.zeros_like(x);axis=np.array([1.,1.,2.])/np.sqrt(6.);details={}
    for label,mask,raw,ratio in [('cold',cold,rawc,.2),('stars',~cold,raws,1.)]:
        xx=x[mask];mm=m[mask]
        w=ndtri(np.clip(raw[:,3:],1e-15,1.-1e-15));w=np.r_[w,-w]
        inertia=np.eye(3)*np.sum(mm*np.sum(xx*xx,axis=1))-(xx*mm[:,None]).T@xx
        w-=np.cross(np.linalg.solve(inertia,vector_J(xx,w,mm)),xx)
        vir=float(np.sum(mm[:,None]*xx*a[mask]));target=.5*ratio*abs(vir)
        frot=.1 if label=='cold' else 0.
        w*=np.sqrt((1-frot)*target/(.5*np.sum(mm[:,None]*w*w)))
        if frot:
            rotation=np.cross(axis,xx)
            rotation*=np.sqrt(frot*target/(.5*np.sum(mm[:,None]*rotation*rotation)))
            w+=rotation
        v[mask]=w
        details[label]=dict(virial_W=vir,kinetic=float(.5*np.sum(mm[:,None]*w*w)),virial_ratio=ratio,ordered_fraction=frot)
    details.update(total_self_potential=float(U),cold_mass=MCOLD,stellar_mass=MSTAR,
                   sampling='nested scrambled6D Sobol; independent species streams; antithetic phase pairs',
                   cold_phase_seed=seed,stellar_phase_seed=seed+1)
    return x,v,m,cold,details


def h4_step(x,v,dt,force,state=None,kick_receipt=None):
    """In-place fourth-order deterministic map, returning final force state.

    state[0] is total acceleration. Remaining state entries belong to caller;
    tests and the production driver use (a,U,phi,host_a,host_potential).
    """
    if dt<=0.:raise ValueError('physical outer timestep must be positive')
    w1=1./(2.-2.**(1./3.));w0=1.-2.*w1
    state=force(x) if state is None else state
    def kick(delta,current):
        before=v.copy() if kick_receipt is not None else None
        v[:]+=delta*current[0]
        if kick_receipt is not None:kick_receipt(x,before,v,current,delta)
    kick(.5*w1*dt,state)
    for drift,k in [(w1,.5*(w1+w0)),(w0,.5*(w0+w1)),(w1,.5*w1)]:
        x[:]+=drift*dt*v
        state=force(x)
        kick(k*dt,state)
    return state
