"""Compare refined and larger_steps-angle histories at the same physical N."""
import sys,json,time,math,resource
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3]

def main(out,new_path,old_path):
 start=time.monotonic();new=json.loads(Path(new_path).read_text());old=json.loads(Path(old_path).read_text());data=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json').read_text());groups=data['cases'][0]['groups'];q=np.array(new['case']['q']);W=np.array(new['case']['W']);n=len(q);deg=np.array([g['degeneracy'] for g in groups]);eta=np.repeat([1 if g['kind']=='S' else -1 for g in groups],n);measure=(deg[:,None]*W[None,:]/(2*math.pi**2)).ravel();Ynew=np.array(new['state']['Y']);Yold=np.array(old['state']['Y']);fold=Yold/measure
 if 'Z' in new['state']:
  z=np.array(new['state']['Z'])/measure;holes=np.array(new['state']['hole_flags'],bool);fnew=np.where(holes,1-z,z);available=np.where(holes,z,1+eta*fnew)
 else:fnew=Ynew/measure;available=1+eta*fnew
 a=new['case']['history'][-1];b=old['case']['history'][-1];fields={key:dict(refined=float(a[key]),larger_steps=float(b[key]),difference=float(a[key]-b[key]),relative_difference=float(a[key]/b[key]-1) if b[key] else None) for key in ('N','Tc_over_mu','x_inner','x_outer','x_minimum','action','omega','energy','Y_charged','charged_fraction','charged_force','neutral_force')};yn=Ynew.reshape(-1,n);yo=Yold.reshape(-1,n);fn=fnew.reshape(-1,n);fo=fold.reshape(-1,n);yieldfactor=.02**3/(2*math.pi**2/45*106.75);rows=[]
 for i,g in enumerate(groups):
  nn=float(sum(yn[i]));no=float(sum(yo[i]));rows.append(dict(group=g['id'],refined_yield=nn*yieldfactor,larger_steps_yield=no*yieldfactor,yield_relative_difference=nn/max(no,1e-300)-1,number_weighted_L1=float(sum(abs(yn[i]-yo[i]))/max(no,1e-300)),normalized_shape_L1=float(sum(abs(yn[i]/max(nn,1e-300)-yo[i]/max(no,1e-300)))),refined_max_f=float(max(fn[i])),larger_steps_max_f=float(max(fo[i])),refined_q_at_max_f=float(q[np.argmax(fn[i])]),larger_steps_q_at_max_f=float(q[np.argmax(fo[i])]),soft_q=q[q<.1].tolist(),refined_soft_f=fn[i,q<.1].tolist(),larger_steps_soft_f=fo[i,q<.1].tolist()))
 checks=dict(common_N=abs(a['N']-b['N'])<1e-13,common_grid=bool(np.array_equal(q,np.array(old['case']['q'])) and np.array_equal(W,np.array(old['case']['W']))),refined_checks=all(new['checks'].values()),finite_profiles=bool(np.all(np.isfinite(Ynew)) and np.all(np.isfinite(Yold)))),
 checks=checks[0];result=dict(claim_id='CC10_CORRECTED_HISTORY_TIME_REFINEMENT',checks={k:bool(v) for k,v in checks.items()},fields=fields,groups=rows,refined_independent_work_residual=a.get('independent_energy_work_residual'),refined_minimum_fermion_availability=float(min(available[eta<0])),refined_max_fermion_f=float(max(fnew[eta<0])),larger_steps_max_fermion_f=float(max(fold[eta<0])),all_number_weighted_L1=float(sum(abs(Ynew-Yold))/sum(abs(Yold))),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Same-N refinement comparison: both histories share fresh002 and the analytic-angular8phase model. The adaptive2e-4 cap is compared with fixed5e-5 cap after that ancestor. The earlier prefix remains shared and unrefined; this comparison does not prove time convergence or identify a physical candidate.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print('fields',fields)
 for r in rows:
  if r['group'] in ('F1_1','F3_0','F8_0'):print(r)
 assert all(result['checks'].values()),result['checks']
if __name__=='__main__':main(*sys.argv[1:])
