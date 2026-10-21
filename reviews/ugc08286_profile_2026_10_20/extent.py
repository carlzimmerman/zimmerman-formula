"""Declared radial-support gate: compact extra disk versus extended source."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from kernel.disk_kernel import build_annular_kernel

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
p=Path(__file__).resolve().parent
d=np.loadtxt(p/'data/UGC08286_rotmod.dat');r,v,ev,vg,vd=d[:,:5].T
foot=json.loads((p.parents[1]/'real_research/derivation_chain_2026/FP0_core_postulates_results.json').read_text())['numbers']
a0s={'canonical':foot['a0_canonical'],'alt':foot['a0_rho_total']}
gas=np.sign(vg)*vg**2;b=gas+.5*vd**2
beam=6.5e3*30*np.pi/(180*3600);h=.196*1.05**.633
rows=[]
for cut in r:
    for hf in (.5,1,2):
        for divisor in (4,8):
            n=int(np.ceil(cut/(beam/divisor)));e=np.linspace(0,cut,n+1)
            A=build_annular_kernel(r,e,h*hf,order=192)*1e9
            for footing,a0 in a0s.items():
                base=(b+np.sqrt(b*b+4*a0*r*3.0857e19/1e6*b))/2
                for nsig in (1,2):
                    lo=np.maximum(v-nsig*ev,0)**2-base;hi=(v+nsig*ev)**2-base
                    M=np.r_[A,-A];bounds=np.r_[hi,-lo]
                    ans=linprog(np.ones(n),A_ub=M,b_ub=bounds,bounds=(0,None),method='highs')
                    q=dict(cut_kpc=float(cut),height_factor=hf,beam_divisor=divisor,
                           annuli=n,footing=footing,nsigma=nsig,status=int(ans.status),
                           success=bool(ans.success))
                    if ans.success:
                        q.update(minimum_mass_msun=float(ans.fun*1e9),
                            max_primal_violation=float(max(np.max(M@ans.x-bounds),-np.min(ans.x),0)))
                    elif ans.status==2:
                        # Sufficient finite-matrix exclusion certificate:
                        # u>=0, M^T u>=0, bounds.u<0.
                        cert=linprog(bounds,A_ub=-M.T,b_ub=np.zeros(n),
                            A_eq=np.ones((1,len(bounds))),b_eq=[1.],bounds=(0,None),method='highs')
                        if cert.success:
                            q['certificate']=dict(u=cert.x.tolist(),
                               negative_margin_v2=float(bounds@cert.x),
                               max_sign_violation=float(max(-np.min(M.T@cert.x),-np.min(cert.x),0)),
                               normalization=float(cert.x.sum()))
                    rows.append(q)
summary={}
for footing in a0s:
    for nsig in (1,2):
        selected=[q for q in rows if q['footing']==footing and q['nsigma']==nsig]
        first=[]
        for hf in (.5,1,2):
            for div in (4,8):
                ok=[q for q in selected if q['success'] and q['height_factor']==hf and q['beam_divisor']==div]
                first.append(dict(height_factor=hf,beam_divisor=div,
                     first_feasible_cut_kpc=min((q['cut_kpc'] for q in ok),default=None)))
        summary[f'{footing}_{nsig}']=first
result=dict(assertion_tested='On 17 observed-radius support cuts, six fixed height/resolution controls each, determine positive finite extra-disk feasibility and sufficient finite-matrix negative certificates under the same fixed .5 stellar baseline.',
            rationale='Determine whether an allowed residual can be a compact central remnant or requires a radially extended source. No new halo profile or smoothing fitted.',
            summary=summary,cases=rows,case_count=len(rows),
            limitations='Finite annular basis and fixed SPARC baseline only; projected data/systematic and covariance caveats remain. Error boxes are not joint confidence. Height is prescribed, not measured extra-component geometry. Off-grid or different3D sources are not universally excluded.')
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(summary,indent=2))
