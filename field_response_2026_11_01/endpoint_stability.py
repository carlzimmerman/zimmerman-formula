#!/usr/bin/env python3
import importlib.util
import json
import resource
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh

HERE=Path(__file__).resolve().parent


def load(name):
    s=importlib.util.spec_from_file_location(name,HERE/(name+'.py'))
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def main():
    out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
    r=load('radial_stability_v2');k=load('kinetic_screen_v2');e=load('endpoint_reconstruction')
    result={'assertion_tested':'Three completed dilute baryon endpoints screened for radial energy signs; no new parameter scan.','cases':[]}
    try:
        for pc,fam in [(.2,'weak_diffuse'),(.2,'strong_compact'),(.4,'weak_diffuse')]:
            obj=e.reconstruct_endpoint(pc,fam);sol=obj['solution'];R=obj['record']['radius'];eps=.01
            sc=[r.scalar_response(j,sol,R,eps,3e-7) for j in range(12)]
            rows=[]
            for nq in [256,512]:
                Q,I,parts,errors,samples=r.matrices(sol,R,eps,sc,nq)
                shear=k.shear_matrix(r,sol,R,nq)
                fluid=eigh(Q,I,eigvals_only=True)[0];kinetic=eigh(Q+shear,I,eigvals_only=True)[0]
                rows.append({'quadrature':nq,'fluid_minimum_rayleigh':float(fluid),
                             'kinetic_minimum_rayleigh':float(kinetic),'errors':errors})
            checks={'reconstruction':max(obj['reconstruction_relative_differences'].values())<5e-5,
                    'positive_inertia':np.linalg.eigvalsh(I)[0]>0,
                    'fluid_refinement':abs(rows[0]['fluid_minimum_rayleigh']-fluid)/max(1.,abs(fluid))<3e-4,
                    'kinetic_refinement':abs(rows[0]['kinetic_minimum_rayleigh']-kinetic)/max(1.,abs(kinetic))<3e-4,
                    'scalar_identity':errors['scalar_response_identity']<3e-5,
                    'mass_variation':errors['mass_variation']<3e-5}
            row={'baseline_psi_c':pc,'family':fam,'epsilon':eps,'final_psi_c':obj['record']['psi_c'],
                 'evaluations':rows,'checks':checks,'reconstruction_relative_differences':obj['reconstruction_relative_differences'],
                 'verdict':'NO_NEGATIVE_DIRECTION_IN_TESTED_ENDPOINT_SPACES' if min(fluid,kinetic)>0 else 'NEGATIVE_ENERGY_DIRECTION_FOUND'}
            result['cases'].append(row);print(pc,fam,row['verdict'],fluid,kinetic,flush=True)
        result['all_controls_pass']=all(all(c['checks'].values()) for c in result['cases'])
    except Exception as exc:
        import traceback
        result['exception']=repr(exc);result['traceback']=traceback.format_exc();result['all_controls_pass']=False
    result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out.write_text(json.dumps(result,indent=2,default=r.json_default,allow_nan=False)+'\n')
    return 0 if result['all_controls_pass'] else 1


if __name__=='__main__':sys.exit(main())
