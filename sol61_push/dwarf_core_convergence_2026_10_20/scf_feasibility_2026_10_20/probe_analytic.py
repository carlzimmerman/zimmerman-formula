"""Bounded continuum core/cusp spatial-resolution tests, no dynamics."""
import os
for k in ('OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import argparse,json,resource,time
from pathlib import Path
import numpy as np
from scf_backend import load_agama,G


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    agama=load_agama();M=1.e7;a=300.
    r=np.unique(np.r_[np.geomspace(1.,3000.,81),[5.,10.,15.,20.,25.,30.,50.,75.,100.,300.]])
    xyz=np.c_[r,np.zeros_like(r),np.zeros_like(r)]
    result=dict(kind='analytic continuum basis controls, not trajectory admission',actual_nice=os.getpriority(os.PRIO_PROCESS,0),
        agama_version=str(agama.__version__),native_threads=2,numerical_kernel='Newtonian Poisson basis; no Plummer pairsoftening',cases=[])
    start=time.monotonic()
    for label,gamma in [('Plummer_core',None),('Hernquist_cusp',1.),('Dehnen_1.5_cusp',1.5)]:
        if gamma is None:
            source=agama.Potential(type='Plummer',mass=G*M,scaleRadius=a)
            truth_phi=-G*M/np.sqrt(r*r+a*a);truth_force=G*M*r/(r*r+a*a)**1.5
            truth_rho=3*G*M/(4*np.pi*a**3)*(1+r*r/a**2)**-2.5
        else:
            source=agama.Potential(type='Dehnen',mass=G*M,scaleRadius=a,gamma=gamma)
            truth_phi=-G*M/(a*(2-gamma))*(1-(r/(r+a))**(2-gamma))
            truth_force=G*M*r**(1-gamma)/(r+a)**(3-gamma)
            truth_rho=(3-gamma)*G*M*a/(4*np.pi*r**gamma*(r+a)**(4-gamma))
        for eta in (.5,1.,2.):
            for n in (16,32,64):
                t=time.monotonic()
                basis=agama.Potential(type='BasisSet',density=source,symmetry='None',lmax=8,mmax=8,nmax=n,eta=eta,r0=a)
                phi,acc=basis.eval(xyz,pot=True,acc=True);rho=basis.density(xyz)
                ferr=np.abs((-acc[:,0]-truth_force)/truth_force)
                derr=np.abs((rho-truth_rho)/truth_rho)
                keep=(r>=25)&(r<=75)
                row=dict(truth=label,eta=eta,nmax=n,requested_lmax=8,analytic_truth_spherical=True,
                    seconds=time.monotonic()-t,force_max_relative_25_75=float(ferr[keep].max()),
                    density_max_relative_25_75=float(derr[keep].max()),potential_max_relative=float(np.max(abs((phi-truth_phi)/truth_phi))),
                    force_relative_at_radii={str(float(R)):float(ferr[np.flatnonzero(r==R)[0]]) for R in [5.,10.,25.,50.,75.]},
                    density_negative_any=bool(np.any(rho<0)))
                result['cases'].append(row)
                result['elapsed_seconds']=time.monotonic()-start
                result['maxrss_bytes_macos']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(row),flush=True)


if __name__=='__main__':main()
