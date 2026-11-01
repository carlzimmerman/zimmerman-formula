#!/usr/bin/env python3
"""Canonical radial energy screen, not a kinetic growing-mode solver."""
import importlib.util
import json
import resource
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh

HERE=Path(__file__).resolve().parent


def load_radial():
    spec=importlib.util.spec_from_file_location('fr01_radial_v2',HERE/'radial_stability_v2.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def stretch_controls():
    rows=[]
    for A,D in [(0.,0.),(1.,1.),(2.,-1.),(-.4,.8),(.25,0.)]:
        target=8./9*(A-D)**2
        estimates=[];positive=True
        for h in [.001,.0005,.00025]:
            def difference(t):
                a,b=1+t*A,1+t*D
                return (a**-2+2*b**-2)/3-(a*b*b)**(-2./3)
            dd=(difference(h)+difference(-h)-2*difference(0))/h**2
            estimates.append(dd)
            positive=positive and difference(h)>-1e-14 and difference(-h)>-1e-14
        richardson=(4*estimates[-1]-estimates[-2])/3
        error=abs(richardson-target)/max(1.,abs(target))
        rows.append({'A':A,'D':D,'exact_hessian':target,'finite_differences':estimates,
                     'richardson_estimate':richardson,
                     'scaled_error':error,'passed':bool(error<3e-7 and positive)})
    return {'rows':rows,'passed':all(x['passed'] for x in rows)}


def shear_matrix(m,sol,R,nq):
    r,w=m.quadrature(0,R,nq)
    psi,dp,s,ds,n,dn=m.state(sol,r)
    dif=[]
    for j in range(12):
        xi,dxi,xir=m.displacement(j,r,R)
        dif.append(dxi-xir)
    dif=np.array(dif)
    return (dif*(w*r*r*(4./3)*n*psi))@dif.T


def one_case(m,pc,eps):
    src=m.source_module();loc,guess=src.local_solution(pc)
    baseline,sol=src.solve_case(pc,eps,loc,guess,refine=True)
    if not baseline['passed']:raise RuntimeError('baseline invalid')
    R=baseline['radius']
    sc=[m.scalar_response(j,sol,R,eps,3e-7) for j in range(12)]
    allrows=[];allchecks=[]
    for nq in [256,512]:
        Q,I,parts,errors,samples=m.matrices(sol,R,eps,sc,nq)
        shear=shear_matrix(m,sol,R,nq);K=Q+shear
        fvals,fvec=eigh(Q,I);fv=fvec[:,0]
        rows=[]
        for nb in [4,8,12]:
            val,vec=eigh(K[:nb,:nb],I[:nb,:nb]);v=vec[:,0]
            pieces={k:float(v@a[:nb,:nb]@v) for k,a in parts.items()}
            pieces['kinetic_shear']=float(v@shear[:nb,:nb]@v)
            scale=sum(abs(x) for x in pieces.values())
            rows.append({'basis_size':nb,'minimum_rayleigh':float(val[0]),
                         'scaled_margin':float(val[0]/scale),'pieces':pieces,
                         'vector':v.tolist()})
        checks={'positive_semidefinite_shear':np.linalg.eigvalsh(shear)[0]>-1e-10,
                'homology_no_shear':abs(shear[0,0])<1e-14,
                'kinetic_minimum_not_below_fluid':rows[-1]['minimum_rayleigh']>=fvals[0]-1e-10,
                'nested_nonincrease':all(rows[j+1]['minimum_rayleigh']<=rows[j]['minimum_rayleigh']+1e-8 for j in range(2)),
                'scalar_response_identity':errors['scalar_response_identity']<3e-5,
                'mass_variation':errors['mass_variation']<3e-5}
        allrows.append({'quadrature':nq,'nested':rows,
                        'old_fluid_minimum':float(fvals[0]),
                        'shear_cost_on_fluid_vector':float(fv@shear@fv),
                        'kinetic_curvature_on_fluid_vector':float(fv@K@fv),
                        'checks':checks})
        allchecks.extend(checks.values())
    lo,hi=[x['nested'][-1]['minimum_rayleigh'] for x in allrows]
    refinement=abs(lo-hi)/max(1.,abs(hi))<3e-4
    adverse=allrows[-1]['nested'][-1]['scaled_margin'] < -1e-5
    good=bool(all(allchecks) and refinement)
    return {'psi_c':pc,'epsilon':eps,'evaluations':allrows,
            'quadrature_refinement_pass':bool(refinement),'controls_pass':good,
            'verdict':('NUMERICAL_CONTROL_FAILURE' if not good else
                       'ACCESSIBLE_KINETIC_ENERGY_SADDLE_IN_TESTED_FAMILY' if adverse else
                       'NO_NEGATIVE_KINETIC_DIRECTION_IN_TESTED_FAMILY')}


def main():
    out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
    m=load_radial()
    result={'assertion_tested':'Exact canonical radial shear correction and six finite-family kinetic energy screens.',
            'stretch_controls':stretch_controls(),'cases':[],
            'non_claims':['No full kinetic eigenmode or stability theorem','No nonlinear vacuum completion','No universal positivity from finite Ritz spaces']}
    try:
        for pc in [.8,.95,.99]:
            for eps in [.0001,.01]:
                row=one_case(m,pc,eps);result['cases'].append(row)
                print(pc,eps,row['verdict'],row['evaluations'][-1]['nested'][-1]['minimum_rayleigh'],flush=True)
        result['all_controls_pass']=result['stretch_controls']['passed'] and all(x['controls_pass'] for x in result['cases'])
    except Exception as exc:
        import traceback
        result['exception']=repr(exc);result['traceback']=traceback.format_exc();result['all_controls_pass']=False
    result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out.write_text(json.dumps(result,indent=2,allow_nan=False,default=m.json_default)+'\n')
    return 0 if result['all_controls_pass'] else 1


if __name__=='__main__':sys.exit(main())
