"""CE-FM-007: complete instantaneous energy accounting for a declared Newtonian receiver.
This is a comparison update, not a derived horizon/capture action.
Variable mass packets are supported; spherical capture has zero net vector momentum.
"""
import numpy as np

def w(u):
    u=np.asarray(u,float)
    if np.any((u<0)|(u>=1)):raise ValueError('outside saturating domain')
    val=np.empty_like(u);small=u<.05
    val[small]=sum(u[small]**n/n for n in range(3,25))
    val[~small]=-u[~small]**2/2-u[~small]-np.log1p(-u[~small])
    return val

def energy(r,v,dm,central_mass,full=True):
    r,v,dm=map(lambda a:np.asarray(a,float),(r,v,dm))
    if len(r)==0:return 0.
    order=np.argsort(r);r=r[order];v=v[order];dm=dm[order]
    enclosed=np.cumsum(dm)
    kinetic=.5*np.sum(dm*v*v);Newton=-central_mass*np.sum(dm/r)
    if full:
        if np.any(enclosed/r**2>=1):raise ValueError('shell state violates full wall')
        nodes,weights=np.polynomial.legendre.leggauss(128)
        bounds=np.concatenate(([0.],1/r[::-1]));lo,hi=bounds[:-1],bounds[1:]
        q=(hi+lo)[:,None]/2+(hi-lo)[:,None]*nodes[None,:]/2
        field=np.sum((hi-lo)/2*np.sum(weights[None,:]*w(enclosed[::-1,None]*q*q)/q**4,axis=1))
    else:
        next_inv=np.concatenate((r[1:]**-3,[0.]))
        field=np.sum(enclosed**3*(r**-3-next_inv))/9
    return float(kinetic+Newton+field)

def capture(r,v,dm,hit,source_mass,bh_mass,c2,radiated_energy=0.,full=True):
    """Capture the declared hit set, solving receiver mass-energy balance algebraically.
    c2 is c^2 in velocity units, not inferred from the theory. Radiation is a stated input.
    Fixed source/baryons remain an external static comparison background.
    """
    r,v,dm=map(lambda a:np.asarray(a,float),(r,v,dm));hit=np.asarray(hit,bool)
    oldE=energy(r,v,dm,source_mass+bh_mass,full)
    packet=float(np.sum(dm[hit]));keep=~hit
    newr,newv,newdm=r[keep],v[keep],dm[keep]
    # Reference energy adds packet rest mass only. Exact energy is linear in additional central mass.
    reference=energy(newr,newv,newdm,source_mass+bh_mass+packet,full)
    B=float(np.sum(newdm/newr)) if len(newr) else 0.
    if c2<=B:raise ValueError('outside weak-gravity receiver approximation')
    correction=(oldE-reference-radiated_energy)/(c2-B)
    delta_bh=packet+correction
    if delta_bh<0:raise ValueError('receiver loses mass despite declared capture; new physics required')
    newE=energy(newr,newv,newdm,source_mass+bh_mass+delta_bh,full)
    residual=(delta_bh-packet)*c2+newE-oldE+radiated_energy
    return dict(r=newr,v=newv,dm=newdm,bh_mass=bh_mass+delta_bh,delta_bh=delta_bh,
                packet_mass=packet,mass_defect=correction,energy_before=oldE,energy_after=newE,
                radiated_energy=radiated_energy,energy_balance_residual=float(residual),binding_coefficient=B)
