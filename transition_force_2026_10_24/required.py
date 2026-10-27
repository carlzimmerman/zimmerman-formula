import sys,json,argparse
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'material_interface_2026_10_24'))
from mixed_carrier import Mixed,transfer_species
from joint import RESERVOIR,law
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('material_interface_2026_10_24/run_final_recovery/base_192.json').read_text());m=Mixed(n=96,domain=12,beta=.5,K=15,charge=0);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);rad=m.r.numpy()*m.rm;gb=m.r.numpy()/(m.r.numpy()**2+m.b**2)**1.5;ids=np.where((rad>=1.5)&(rad<=50))[0];A=m.A.numpy()[ids];rhs=law(gb[ids])-gb[ids];J=np.c_[A,np.zeros_like(A)]
 cons=[dict(type='eq',fun=lambda a:sum(a[:96])-RESERVOIR,jac=lambda a:np.r_[np.ones(96),np.zeros(96)]),dict(type='eq',fun=lambda a:J@a-rhs,jac=lambda a:J),dict(type='ineq',fun=m.cap,jac=m.capjac)]
 op=minimize(m.direct,v,jac=True,method='SLSQP',bounds=[(1e-12,RESERVOIR)]*96+[(0,1)]*96,constraints=cons,options=dict(ftol=1e-14,maxiter=1600));E,g=m.direct(op.x);r=m.report(np.r_[np.log(op.x[:96]),op.x[96:]]);active=op.x[:96]>1e-7;mu=g[:96];force=-np.gradient(mu,m.r.numpy());mask=(rad>=1.5)&(rad<=50);out={'status':'Externally constrained diagnostic, not a free equilibrium or a constitutive correction','optimizer':{'success':bool(op.success),'message':str(op.message),'iterations':int(op.nit)},'law_constraint_max':float(max(abs(J@op.x-rhs))),'mass_constraint':float(abs(sum(op.x[:96])-RESERVOIR)),'energy':E,'r_kpc':rad.tolist(),'original_mass_chemical_potential':mu.tolist(),'unbalanced_material_acceleration_a0':force.tolist(),'max_unbalanced_acceleration_a0_in_law_window':float(max(abs(force[mask]))),'state':r};dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['state','r_kpc','original_mass_chemical_potential','unbalanced_material_acceleration_a0']},indent=2))
