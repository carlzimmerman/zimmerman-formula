"""Unitary preparation diagnostic; work from prescribed field is explicit."""
import argparse,json
import numpy as np
CHI=11.220184543019636

def ramp(N,T,ef,dt):
    u,w=np.polynomial.legendre.leggauss(N);u=(u+1)/2;w=w/2;weights=CHI*u*w
    r=np.zeros((N,3));r[:,0]=-1
    count=int(round(T/dt));assert abs(count*dt-T)<1e-12
    work=0.;maxledger=0.
    for j in range(count):
        E0=ef*np.sin(np.pi*j/(2*count))**2;Em=ef*np.sin(np.pi*(j+.5)/(2*count))**2;E1=ef*np.sin(np.pi*(j+1)/(2*count))**2
        P0=weights@r[:,2]
        b=np.column_stack((u,np.zeros(N),-np.full(N,Em)));mag=np.linalg.norm(b,axis=1);axis=b/mag[:,None]
        angle=2*mag*dt;c=np.cos(angle)[:,None];s=np.sin(angle)[:,None]
        r=r*c+np.cross(axis,r)*s+axis*np.sum(axis*r,axis=1)[:,None]*(1-c)
        P1=weights@r[:,2]
        work+=(Em-E0)*P0+(E1-Em)*P1
        energy=weights@(u*(r[:,0]+1)-E1*r[:,2])
        maxledger=max(maxledger,abs(energy+work))
    b=np.column_stack((u,np.zeros(N),-np.full(N,ef)));axis=b/np.linalg.norm(b,axis=1)[:,None]
    projection=np.sum(axis*r,axis=1)
    Pdiag=weights@(projection*axis[:,2]);Peq=CHI*ef*(np.hypot(1,ef)-ef)
    source_eq=CHI*ef-Peq;source_diag=CHI*ef-Pdiag
    return dict(N=N,ramp_time=T,field=ef,dt=dt,final_P=float(weights@r[:,2]),diagonal_ensemble_P=float(Pdiag),equilibrium_P=float(Peq),
        source_relative_error=float((source_diag-source_eq)/source_eq),
        excited_particle_fraction=float((weights@((1+projection)/2))/sum(weights)),
        maximum_bloch_norm_error=float(np.max(abs(np.sum(r*r,axis=1)-1))),
        maximum_energy_plus_source_work_error=float(maxledger),source_work=float(work))

p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
rows=[ramp(64,T,e,.1) for e in [.01,.1] for T in [1.,10.,100.,1000.]]
refine=[ramp(N,1000.,.01,dt) for N,dt in [(64,.05),(128,.1),(128,.05)]]
with open(a.output,'w') as f:json.dump(dict(runs=rows,refinement=refine),f,indent=2,allow_nan=False)
print(json.dumps(dict(runs=rows,refinement=refine)))
