"""Follow-up discriminator: static nonaxisymmetric scattering without spin work."""
import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rotor',HERE/'experiment.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def main(output):
    cells=[]
    for nphase in [24,48]:
        for j in [.05,.3]:
            # Exact reflection and inversion symmetry, with identical +/-j
            # pairs. Recompute speeds to keep each E=E0 in the pair field.
            phase=np.repeat((np.arange(nphase)+.5)*2*np.pi/nphase,2)
            angular=np.tile([j,-j],nphase)
            n=len(phase)
            er=np.stack([np.cos(phase),np.sin(phase)],axis=-1)
            et=np.stack([-np.sin(phase),np.cos(phase)],axis=-1)
            pos=m.R0*er
            phi,_=m.field(pos,0.,'pair')
            vr=-np.sqrt(2*(m.E0-phi)-(angular/m.R0)**2)
            vel=vr[:,None]*er+(angular/m.R0)[:,None]*et
            z0=np.r_[0.,0.,0.,0.,0.,0.,pos.ravel(),vel.ravel()]
            sol=solve_ivp(m.rhs('pair',n),(0,40),z0,method='DOP853',
                          dense_output=True,rtol=1e-10,atol=1e-12,max_step=.02)
            m.check('solve_%s_%s'%(nphase,j),sol.success)
            d=m.diagnostics(sol,n,'pair',40,.01)
            fine=m.diagnostics(sol,n,'pair',40,.005)
            m.check('detector_%s_%s'%(nphase,j),all(d['cuts'][str(r)]['inward_by_particle']==fine['cuts'][str(r)]['inward_by_particle']
                    and d['cuts'][str(r)]['outward']==fine['cuts'][str(r)]['outward'] for r in m.RADII))
            d=fine
            zz=sol.sol(np.linspace(0,40,4001)).T
            R,V,theta,L=zz[:,:2],zz[:,2:4],zz[:,4],zz[:,5]
            pos=zz[:,6:6+2*n].reshape(-1,n,2)
            vel=zz[:,6+2*n:].reshape(-1,n,2)
            phi,_=m.field(pos-R[:,None,:],theta,'pair')
            Ei=.5*np.sum(vel*vel,axis=-1)+phi
            max_dE=float(np.max(abs(Ei-Ei[0])))
            max_omega=float(np.max(abs(L/m.I)))
            for quantity in ['max_H_error','max_J_error','max_P_error']:
                m.check('invariant_%s_%s_%s'%(nphase,j,quantity),d[quantity]<2e-8,d[quantity])
            m.check('reflection_keeps_rest_%s_%s'%(nphase,j),max_omega<1e-8,max_omega)
            m.check('individual_energy_%s_%s'%(nphase,j),max_dE<2e-6,max_dE)
            d.update(n=n,nphase=nphase,j_initial=j,max_omega=max_omega,max_individual_E_error=max_dE,nfev=sol.nfev)
            cells.append(d)
            print(json.dumps(dict(n=n,j=j,max_omega=max_omega,max_dE=max_dE,
                  inward=[d['cuts'][str(r)]['inward'] for r in m.RADII])),flush=True)
    result=dict(cells=cells,assertions=len(m.CHECKS),passed=sum(c['passed'] for c in m.CHECKS),checks=m.CHECKS)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(assertions=result['assertions'],passed=result['passed'])))
    if result['assertions']!=result['passed']:
        print(json.dumps([c for c in m.CHECKS if not c['passed']],indent=2))
        raise SystemExit(1)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    main(p.parse_args().output)
