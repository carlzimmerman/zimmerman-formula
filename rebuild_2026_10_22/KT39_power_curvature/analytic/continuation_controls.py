"""Bounded finite controls for the two explicitly adaptive KT39 powers."""
import argparse,json
from pathlib import Path
import numpy as np
import law
from radial_reference import radial_force


def run():
    g=np.array([.3,-.6,.8]);H=np.array([[.2,.1,-.1],[.1,-.3,.2],[-.1,.2,.4]])
    v=np.array([.2,.5,-.4]);K=np.array([[.7,-.4,.3],[-.4,.5,.6],[.3,.6,-.2]])
    rows=[]
    for p in (1.125,1.25):
        h=1e-5;t=law.tensor_terms(g,H,.7,a0=1.2,p=p)
        fd=(law.tensor_terms(g+h*v,H+h*K,.7,a0=1.2,p=p)['energy']-law.tensor_terms(g-h*v,H-h*K,.7,a0=1.2,p=p)['energy'])/(2*h)
        exact=2*np.sum((t['A']+g)*v)+2*np.sum(t['B']*K)
        energy_error=float(abs(fd-exact)/max(1.,abs(exact)))
        norms=[np.linalg.norm(law.tensor_terms(np.array([0.,0.,2.48]),e*H,1.,p=p)['B'])/e for e in (1e-6,1e-10)]
        predicted=(1e-4)**(2*p-2);hzero_error=float(abs(norms[1]/norms[0]/predicted-1))
        weak=[]
        for lam in (1e-8,1e-12,1e-16):
            t=law.tensor_terms(lam*g,lam*H,.8,p=p);target=g/np.sqrt(np.linalg.norm(g))
            weak.append(float(np.linalg.norm((t['A']+lam*g)/np.sqrt(lam)-target)/np.linalg.norm(target)))
        k=.7;ell=.8;r=np.array([1e-6,2e-6]);z0=(3*ell**2*k**2)**p
        t=radial_force(r,k*r,np.full_like(r,k),np.zeros_like(r),ell,p=p)
        expected=k*(law.R(z0)-(2*p/3)*law.zRprime(z0))
        core_error=float(np.max(abs(t['total']/r/expected-1)))
        r=np.array([1e-4,2e-4]);t=radial_force(r,1/r**2,-2/r**3,6/r**4,1.,p=p)
        expected=(2-p*(2+3*p)/3)*6**(-p/2)*r**(3*p-2)
        point_error=float(np.max(abs(t['phantom']/expected-1)))
        passed=energy_error<1e-7 and hzero_error<1e-6 and weak[-1]<1e-3 and all(a>b for a,b in zip(weak,weak[1:])) and core_error<1e-8 and point_error<1e-4
        rows.append(dict(p=p,energy_derivative_scaled_error=energy_error,H_zero_scaling_relative_error=hzero_error,weak_scaling_errors=weak,core_relative_error=core_error,point_relative_error=point_error,passed=passed))
    return dict(rows=rows,all_checks_pass=all(r['passed'] for r in rows),qualification='Finite controls and declared rates; no dynamic health or global regularity conclusion')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();result=run()
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result,indent=2))
    if not result['all_checks_pass']:raise SystemExit(1)
