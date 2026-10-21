"""Read-only reconstruction of saved finite LP assertions and null-source ray."""
import argparse, json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import linprog

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
packet=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(packet))
from kernel.disk_kernel import build_annular_kernel
result=json.loads((packet/'inversion_run/results.json').read_text())
arrays=np.load(packet/'inversion_run/matrices.npz')
d=np.loadtxt(packet/'data/UGC08286_rotmod.dat')
R,V,eV,Vg,Vd,Vb,SB=d[:,:7].T
foot=json.loads((packet.parents[1]/'real_research/derivation_chain_2026/FP0_core_postulates_results.json').read_text())['numbers']
a0s={'canonical':foot['a0_canonical'],'alt':foot['a0_rho_total']}
gas=Vg*np.abs(Vg)
samples={'all17':np.arange(17),'alternate_even':np.arange(0,17,2),'alternate_odd':np.arange(1,17,2)}

def intervals(q,idx):
    n=q['nsigma'];return np.maximum(0,V[idx]-n*eV[idx])**2,(V[idx]+n*eV[idx])**2
def baseline(a0):
    b=gas+.5*Vd**2;return (b+np.sqrt(b*b+4*a0*R*3.0857e19/1e6*b))/2
def metrics(q,C,b,c):
    x=np.array(q['x']);y=np.array(q['dual_marginals'])
    return {'primal_violation':float(max(0,np.max(C@x-b),-np.min(x))),
        'dual_violation':float(max(0,np.max(y),np.max(C.T@y-c))),
        'duality_gap':float(c@x-b@y),
        'stored_objective_error':float(abs(c@x-q['objective'])),
        'stored_dual_objective_error':float(abs(b@y-q['dual_objective']))}

extra=[]
for q in result['extra_results']:
    A=arrays[q['model_key']];lo,hi=intervals(q,np.arange(17));base=baseline(a0s[q['footing']])
    C=np.r_[A,-A]*1e9;rhs=np.r_[hi-base,base-lo];c=np.ones(A.shape[1])
    row={'model_key':q['model_key'],'footing':q['footing'],'nsigma':q['nsigma'],'success':q['success']}
    if q['success']:
        row.update(metrics(q,C,rhs,c))
        row['predicted_vector_error']=float(np.max(np.abs(A@np.array(q['masses_msun'])-q['predicted_extra_v2'])))
    else:
        re=linprog(c,A_ub=C,b_ub=rhs,bounds=(0,None),method='highs-ds')
        row['independent_solver_status']=int(re.status);row['status_agrees']=int(re.status)==q['status']
    extra.append(row)

stellar=[]
for q in result['stellar_results']:
    idx=samples[q['sampling']];df=q['distance_factor'];B=arrays[q['model_key']][idx]*df
    lo,hi=intervals(q,idx);a=a0s[q['footing']]*R[idx]*df*3.0857e19/1e6
    low=lo**2/(lo+a)-gas[idx]*df;high=hi**2/(hi+a)-gas[idx]*df
    n=B.shape[1];m=len(idx)
    C=np.r_[np.c_[B,np.zeros(m)],np.c_[-B,np.zeros(m)],np.c_[np.eye(n),-np.ones(n)]]
    rhs=np.r_[high,-low,np.zeros(n)];c=np.r_[np.zeros(n),1.]
    row={k:q[k] for k in ['model_key','footing','nsigma','distance_control','sampling','success']}
    if q['success']:
        row.update(metrics(q,C,rhs,c))
        row['predicted_vector_error']=float(np.max(np.abs(B@np.array(q['Upsilon'])-q['predicted_stellar_v2'])))
        # For any z, interval feasibility and 0<=U<=u imply
        # u >= min_interval z^T t / sum_j max((B^T z)_j,0).
        y=np.asarray(q['dual_marginals'],dtype=np.longdouble)
        z=y[:m]-y[m:2*m]
        num=np.maximum(z,0)@np.asarray(low,dtype=np.longdouble)+np.minimum(z,0)@np.asarray(high,dtype=np.longdouble)
        den=np.maximum(np.asarray(B,dtype=np.longdouble).T@z,0).sum()
        row['interval_support_ceiling_lower_bound']=float(num/den) if den>0 else None
        row['ceiling_gap_vs_support_bound']=q['required_pointwise_ceiling']-row['interval_support_ceiling_lower_bound'] if den>0 else None
    else:
        re=linprog(c,A_ub=C,b_ub=rhs,bounds=(0,None),method='highs-ds')
        row['independent_solver_status']=int(re.status);row['status_agrees']=int(re.status)==q['status']
    stellar.append(row)

fid=result['fiducial_extra'];A=arrays[fid['model_key']];edges=arrays[fid['model_key']+'_edges'];n=A.shape[1]
# Unit ray in 1e9 Msun, requiring exact zero target-force in the floating matrix.
ray=linprog(np.zeros(n),A_eq=np.r_[A*1e9,np.ones((1,n))],b_eq=np.r_[np.zeros(17),1.],bounds=(0,None),method='highs-ds')
null={'success':bool(ray.success),'status':int(ray.status),'source_bins':n,
    'last_cell_width_kpc':float(edges[-1]-edges[-2]),'median_cell_width_kpc':float(np.median(np.diff(edges)))}
if ray.success:
    x=ray.x;Ka=build_annular_kernel(R,edges,fid['height_kpc'],method='adaptive')
    Rdense=np.unique(np.r_[np.linspace(.01,8.07,501),R])
    Kdense=build_annular_kernel(Rdense,edges,fid['height_kpc'],order=384)
    f=Kdense@(x*1e9)
    null.update(ray_fraction=x.tolist(),min_fraction=float(x.min()),sum_fraction=float(x.sum()),
        fixed_target_residual_v2=float(np.max(np.abs(A@(x*1e9)))),
        adaptive_target_residual_v2=float(np.max(np.abs(Ka@(x*1e9)))),
        dense_target_max_abs_v2_per_1e9Msun=float(np.max(np.abs(f))),
        dense_target_min_v2=float(f.min()),dense_target_max_v2=float(f.max()),
        dense_target_r_kpc=Rdense.tolist(),dense_target_v2_per_1e9Msun=f.tolist())

def aggregate(rows):
    out={'count':len(rows),'success_count':sum(q['success'] for q in rows)}
    good=[q for q in rows if q['success']]
    for k in ['primal_violation','dual_violation','duality_gap','stored_objective_error','stored_dual_objective_error','predicted_vector_error']:
        out['max_abs_'+k]=max(abs(q[k]) for q in good)
    return out
out={'assertion_tested':'Independently rebuild all saved LP constraints and numerical primal-dual residuals; recompute unsuccessful statuses; derive a scalar support-function lower bound for each saved stellar ceiling; test one nonnegative sampled-force null ray.',
    'extra_summary':aggregate(extra),'stellar_summary':aggregate(stellar),
    'extra_checks':extra,'stellar_checks':stellar,'fiducial_null_ray':null,
    'non_claims':['No exact or interval quadrature certificate','Floating null ray implies numerical sampled-force degeneracy, not force-free continuum density','No universal physical exclusion']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'extra_summary':out['extra_summary'],'stellar_summary':out['stellar_summary'],
    'null_summary':{k:v for k,v in null.items() if not isinstance(v,list)}},indent=2))
