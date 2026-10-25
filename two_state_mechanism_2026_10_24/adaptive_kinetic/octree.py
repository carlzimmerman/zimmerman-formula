"""Occupied-leaf adaptive octree; empty space is not assigned invented mass."""
import numpy as np

def leaves(x,max_width=2.,target=16,min_width=None,origin=None):
    origin=np.zeros(3) if origin is None else np.asarray(origin)
    min_width=max_width/8 if min_width is None else min_width
    extent=2.**np.ceil(np.log2(max(np.max(np.abs(x-origin))+1e-10,max_width/2)))
    stack=[(np.arange(len(x)),origin-extent,2*extent,0)];out=[]
    while stack:
        ids,lo,width,depth=stack.pop()
        if depth<24 and width>min_width*(1+1e-12) and (width>max_width*(1+1e-12) or len(ids)>target):
            half=width/2;bits=(x[ids]>=lo+half).astype(int);code=bits@[1,2,4]
            for c in np.unique(code):
                off=np.array([c&1,(c>>1)&1,(c>>2)&1])*half
                stack.append((ids[code==c],lo+off,half,depth+1))
        else:out.append((ids,width,lo))
    return out

def cell_pairs(x,v,n,tree,seed=11):
    ii=[];jj=[];vol=[]
    for ids,width,_ in tree:
        a,b=np.triu_indices(len(ids),1);i=ids[a];j=ids[b]
        keep=(i<n);ii.extend(i[keep]);jj.extend(j[keep]);vol.extend([width**3]*int(sum(keep)))
    i=np.array(ii,dtype=int);j=np.array(jj,dtype=int);volume=np.array(vol)
    if not len(i):return i,j,np.empty((0,3)),np.empty(0),np.empty(0),volume
    dr=x[j]-x[i];dist=np.linalg.norm(dr,axis=1);normal=dr/np.maximum(dist,1e-30)[:,None]
    for p in np.flatnonzero(dist<1e-12):
        # Fixed isotropic normal for coincident velocity samples; no RNG changes
        # during trial timesteps. Equal positions guarantee zero pair torque.
        rng=np.random.default_rng(int(seed+104729*i[p]+1000003*j[p]));z=rng.normal(size=3);normal[p]=z/np.linalg.norm(z)
    incoming=np.maximum(-np.sum((v[j]-v[i])*normal,axis=1),0.)
    return i,j,normal,incoming,dist,volume
