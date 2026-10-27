"""Qualify larger positive physical macrosteps on the accepted smooth branch."""
import argparse,json,time
from pathlib import Path
import numpy as np
from dynamics import model,load
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();base=Path('sustained_transport_2026_10_26/run_continue_second');z=load(base/'state.npz');m=model();E0=m.full_energy(*z);M0=float(np.sum(abs(z[0])**2));Q0=m.charge(z[0],z[4]);rows=[]
for h in [.0025,.005,.01,.02]:
 m=model();zz=tuple(x.copy() for x in z);start=time.monotonic();r=m.full_step(*zz,h/m.tdyn);an,xn,pn,cn,vn,ds,dq,info=r;accepted=info['fixed_point_error']<1e-9 and not info.get('substep_failed',False)
 row={'h_Myr':h,'root_accepted':bool(accepted),'residual':info['fixed_point_error'],'seconds':time.monotonic()-start,'energy_defect':m.full_energy(an,xn,pn,cn,vn)+ds-E0,'mass_defect':float(np.sum(abs(an)**2))-M0,'charge_defect':m.charge(an,vn)+dq-Q0,'substep_failed':info.get('substep_failed',False)}
 if accepted:
  fine=model();zf=tuple(x.copy() for x in z);err=False
  for j in range(round(h/.00125)):
   r2=fine.full_step(*zf,.00125/fine.tdyn)
   if r2[-1]['fixed_point_error']>1e-9 or r2[-1].get('substep_failed',False):err=True;break
   zf=r2[:5]
  if not err:
   row.update(relative_material_L2_difference=float(np.linalg.norm(an-zf[0])/np.linalg.norm(zf[0])),total_density_L1_difference=float(np.sum(abs(np.sum(abs(an)**2,axis=0)-np.sum(abs(zf[0])**2,axis=0)))),boundary_difference_kpc=m.diagnostics(an,xn,cn,vn)['boundary_kpc']-fine.diagnostics(zf[0],zf[1],zf[3],zf[4])['boundary_kpc'],wave_energy_difference=m.diagnostics(an,xn,cn,vn)['wave_energy']-fine.diagnostics(zf[0],zf[1],zf[3],zf[4])['wave_energy'])
 rows.append(row)
out={'base_time_Myr':json.loads((base/'results.json').read_text())['completed_time_Myr'],'cases':rows,'non_claim':'One-step qualification, not long-time convergence. Failed roots remain rejected. New state is the C4 quiet continuation, not the old internally mismatched branch.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
