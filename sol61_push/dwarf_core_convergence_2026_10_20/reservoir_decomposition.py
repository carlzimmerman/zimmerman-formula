"""Exact kinematic partition of fixed particle reservoirs from saved states.

Jspin is about each group's own centre/bulk. Jcentre is its orbital motion
about the all-original-particle COM. Uallocated is half the full-field
potential assigned to its particles, including half each cross-group pair;
it is not an isolated binding energy or a local host-work receipt.
"""
import numpy as np

def decompose(x,v,m,phi,groups):
    x,v,m,phi=map(np.asarray,(x,v,m,phi));cover=np.zeros(len(m),int)
    X=np.average(x,weights=m,axis=0);V=np.average(v,weights=m,axis=0)
    totalJ=np.cross(x-X,m[:,None]*(v-V)).sum(0)
    totalE=float(.5*np.sum(m[:,None]*(v-V)**2)+.5*(m@phi));out={}
    for label,mask in groups.items():
        mask=np.asarray(mask,bool);cover+=mask;M=float(m[mask].sum())
        if M<=0:raise ValueError('nonempty positive-mass groups required')
        R=np.average(x[mask],weights=m[mask],axis=0);B=np.average(v[mask],weights=m[mask],axis=0)
        spin=np.cross(x[mask]-R,m[mask,None]*(v[mask]-B)).sum(0)
        orbital=np.cross(R-X,M*(B-V))
        kin=float(.5*np.sum(m[mask,None]*(v[mask]-B)**2));korbit=float(.5*M*np.sum((B-V)**2));U=float(.5*(m[mask]@phi[mask]))
        out[label]=dict(mass=M,centre=R.tolist(),bulk=B.tolist(),Jspin=spin.tolist(),Jcentre=orbital.tolist(),Jallocated=(spin+orbital).tolist(),Kwithin=kin,Kcentre=korbit,Uallocated=U,Eallocated=kin+korbit+U)
    if not np.all(cover==1):raise ValueError('groups must partition all original particles exactly once')
    return {'groups':out,'global':dict(COM=X.tolist(),VCOM=V.tolist(),Jinternal=totalJ.tolist(),Einternal=totalE),
            'closure':dict(J_norm=float(np.linalg.norm(sum((np.array(g['Jallocated']) for g in out.values()),np.zeros(3))-totalJ)),
                           energy=float(sum(g['Eallocated'] for g in out.values())-totalE))}
