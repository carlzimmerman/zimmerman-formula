import argparse,json
from pathlib import Path
import numpy as np
from octree import leaves,cell_pairs
from kinetic import Kinetic

def manufactured(nspace,nvel,kind,seed,width=2.):
    rng=np.random.default_rng(seed)
    x=rng.uniform(-1,1,(2*nspace,3)) if kind=='uniform' else rng.normal(size=(2*nspace,3))
    x=np.repeat(x,nvel,axis=0);n=nspace*nvel;v=rng.normal(size=x.shape);m=np.full(2*n,1/n)
    tree=leaves(x,width,16*nvel)
    ids=np.concatenate([ids for ids,_,_ in tree]);assert np.array_equal(np.sort(ids),np.arange(len(x)))
    for ids,h,lo in tree:assert np.all(x[ids]>=lo-1e-12) and np.all(x[ids]<=lo+h+1e-12)
    i,j,normal,speed,dist,volume=cell_pairs(x,v,n,tree,seed)
    keep=j>=n
    overlap=float(np.sum(m[i[keep]]*m[j[keep]]/volume[keep]))
    flux=float(np.sum(m[i[keep]]*m[j[keep]]*speed[keep]/volume[keep]))
    ref=1/8 if kind=='uniform' else 1/(8*np.pi**1.5)
    return dict(overlap=overlap,flux=flux,overlap_reference=ref,flux_reference=ref/np.sqrt(np.pi),cells=len(tree))

def main():
    out={'manufactured':[]}
    for kind in ('uniform','gaussian'):
        for ns,nv,width in ((64,2,2.),(256,2,2.),(1024,2,2.),(256,4,2.),(1024,2,1.)):
            rows=[manufactured(ns,nv,kind,s,width) for s in range(70,86)]
            density=np.array([r['overlap']/r['overlap_reference'] for r in rows]);flux=np.array([r['flux']/r['flux_reference'] for r in rows])
            out['manufactured'].append(dict(kind=kind,nspace=ns,nvel=nv,max_width=width,seeds=16,density_ratio_mean=float(density.mean()),density_ratio_se=float(density.std(ddof=1)/4),flux_ratio_mean=float(flux.mean()),flux_ratio_se=float(flux.std(ddof=1)/4),mean_cells=float(np.mean([r['cells'] for r in rows]))))
    s=Kinetic(1e8,1,nspace=8,nvel=1)
    e,_,_=s.energy_force(s.x,s.state);k=s.kinetic(s.v)
    x=np.repeat(s.x,2,axis=0);v=np.repeat(s.v,2,axis=0);s.m=np.repeat(s.m/2,2)
    e2,_,_=s.energy_force(x,np.zeros(len(x),dtype=bool));k2=s.kinetic(v)
    out['uncharged_velocity_replication_energy_error']=abs(e2+k2-e-k);assert out['uncharged_velocity_replication_energy_error']<1e-12
    # Fixed partition: boost and rotation covariance away from coincident points.
    rng=np.random.default_rng(92);x=rng.normal(size=(32,3));v=rng.normal(size=(32,3));tree=leaves(x,2,16)
    a=cell_pairs(x,v,16,tree);b=cell_pairs(x,v+[40,-15,2],16,tree)
    out['boost_rate_error']=float(max(abs(a[3]-b[3])));assert out['boost_rate_error']<1e-12
    R=np.linalg.qr(rng.normal(size=(3,3)))[0];c=cell_pairs(x@R.T,v@R.T,16,tree)
    out['fixed_partition_rotation_rate_error']=float(max(abs(a[3]-c[3])));assert out['fixed_partition_rotation_rate_error']<1e-12
    # A local kinetic event through production code, all other sites separated.
    s=Kinetic(1e8,1,nspace=8,nvel=1,max_width=1.)
    s.x[:]=np.arange(16)[:,None]*np.array([3.,0,0]);s.x[0]=[.1,.1,.1];s.x[8]=[.2,.1,.1];s.v[:]=0;s.v[8]=[-20,0,0]
    e,_,_=s.energy_force(s.x,s.state);old=e+s.kinetic(s.v);s.collide(1e10);e,_,_=s.energy_force(s.x,s.state)
    out['forced_capture_state']=bool(s.state[8]);out['forced_capture_energy_error']=abs(e+s.kinetic(s.v)+s.Q-old)
    assert s.state[8] and out['forced_capture_energy_error']<1e-10
    out['forced_capture_stats']=s.stats
    # Test genuine adaptivity without conflating grid changes with conservation.
    x=np.r_[rng.uniform(-1,1,(64,3)),rng.normal(scale=.03,size=(64,3))]
    widths=[h for _,h,_ in leaves(x,2,16)]
    out['adaptive_width_range']=[min(widths),max(widths)];assert min(widths)<max(widths)
    return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=main()
    Path(a.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps(out,indent=2))
