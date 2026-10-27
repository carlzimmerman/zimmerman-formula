import argparse,json
from pathlib import Path
import numpy as np
from dynamics import model,load,field,radius,Rdot,Rddot,perturb
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();dest=Path(args.output)
m=model();base=load('infall_pump_2026_10_25/run_smooth_infall/state.npz');out={'base_time_Myr':5.7,'cases':[],'perturbations_are_response_probes_not_formation_seeds':True}
for d in [0.,-.01,.01,-.005,.005]:
 z,meta=(base,{'actual_displacement_kpc':0.}) if d==0 else perturb(m,base,d)
 a,x,cp,c,v=z;f=field(m,z);mt=abs(a[0])**2;md=2*np.real(np.conj(a)*f[0]);_,S,b,cov,U,G=m.transfer(a,x,c)
 charge_derivative=float(np.sum((m.g+2*m.g2*mt/m.vol)*md[0]));assert abs(charge_derivative-np.sum(S))<1e-8*max(1.,abs(charge_derivative))
 row={'displacement':d,'meta':meta,'radius_kpc':radius(m,a),'Rdot_kpc_Myr':Rdot(m,z),'Rddot_checks_kpc_Myr2':{str(e):Rddot(m,z,e) for e in [1e-7,3e-8,1e-8]},'energy':m.full_energy(*z),'joint':m.diagnostics(a,x,c,v),'integrated_source':float(np.sum(S)),'material_charge_derivative':charge_derivative}
 out['cases'].append(row)
 if d in [-.01,0.,.01]:np.savez_compressed(dest.with_name('state_'+str(d)+'.npz'),a=a,alpha=x,carrier_p=cp,chi=c,pi=v)
for delta in [.01,.005]:
 plus=next(x for x in out['cases'] if x['displacement']==delta);minus=next(x for x in out['cases'] if x['displacement']==-delta)
 out['omega2_'+str(delta)+'_Myr-2']=-((plus['Rddot_checks_kpc_Myr2']['1e-08']-minus['Rddot_checks_kpc_Myr2']['1e-08'])/(2*delta))
dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='cases'})
