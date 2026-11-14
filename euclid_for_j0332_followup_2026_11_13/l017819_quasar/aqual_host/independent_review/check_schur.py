"""Independent full augmented BVLS versus production Schur/NNLS on small QPs."""
import sys,json,argparse,numpy as np
from pathlib import Path
from types import SimpleNamespace
from scipy import optimize,linalg
sys.dont_write_bytecode=True
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent));import positive_profiles as pp

def main(output):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);rows=[];original=pp.oc.FixedState
 for factor in [1.,1000.]:
  i,j=np.indices((17,8));D=np.sin((i+1)*(j+2)*.17)+np.cos((i+2)*(j+1)*.11);D[:,4]*=factor;truth=np.array([-.7,.3,.6,-.4,-.2/factor,.8,-.1,.05]);y=D@truth+.02*np.sin(np.arange(17));R=np.diag([2.,3.,4.,2.]);R[0,1]=R[1,0]=-.4;nu=np.array([1e-8,1e-8,1e-8,.01]);H0=D.T@D;b=D.T@y
  st=SimpleNamespace(H0=H0,b=b,n=4,ns=2,nu=nu,R=R,template={'params':[0.]*8,'lens':np.zeros(17)},y=y,W=D,D=D,edges=np.ones((2,2),bool))
  pp.oc.FixedState=lambda obj,fn:st
  prod=pp.PositiveState(None,None)
  for ll in [0.,2.,4.]:
   r=prod.evaluate(ll,True);Q=linalg.block_diag(np.exp(ll)*R,np.diag(nu));A=np.vstack([D,linalg.cholesky(Q,lower=False)]);target=np.r_[y,np.zeros(8)];lb=np.r_[np.zeros(4),np.full(4,-np.inf)];alt=optimize.lsq_linear(A,target,bounds=(lb,np.full(8,np.inf)),method='bvls',tol=1e-12,max_iter=1000);coeferr=float(np.max(abs(r['coef']-alt.x)));objective=.5*(np.sum((y-D@alt.x)**2)+alt.x@Q@alt.x);delta=float(r['penalized_MAP_objective']-objective)
   assert alt.success and coeferr<2e-7 and abs(delta)<1e-9
   rows.append({'nuisance_column_scale':factor,'loglambda':ll,'max_coefficient_difference':coeferr,'objective_difference':delta,'production_scaled_KKT':r['projected_gradient_scaled_inf'],'production_nuisance_gradient':r['nuisance_gradient_inf'],'source_min':float(r['coef'][:4].min()),'nuisance_min':float(r['coef'][4:].min()),'active_source_nodes':int(np.sum(r['coef'][:4]==0))})
 pp.oc.FixedState=original
 raw=json.loads((B.parent/'positive_01/result.json').read_text());cases=[]
 for f in raw['fixtures']:
  for c in f['cases']:
   a=c['aqual'];s=c['sie'];assert 'score' not in a and 'score' not in s
   assert abs(a['penalized_MAP_objective']-.5*(a['chi2']+a['prior_penalty']))<1e-8
   assert abs(c['delta_penalized_MAP_objective']-(a['penalized_MAP_objective']-s['penalized_MAP_objective']))<1e-8
   cases.append({'fixture':f['fixture'],'loglambda':c['loglambda'],'logmass_total':c['logmass_total'],'delta_chi2':c['delta_chi2'],'delta_penalized_MAP_objective':c['delta_penalized_MAP_objective'],'min_AQUAL_nuisance_light_amplitude':min(a['linear_flux_lens_A_B_sky'][:3]),'min_SIE_nuisance_light_amplitude':min(s['linear_flux_lens_A_B_sky'][:3]),'AQUAL_scaledKKT':a['projected_gradient_scaled_inf'],'SIE_scaledKKT':s['projected_gradient_scaled_inf'],'mass_boundary':c['mass_boundary'],'scan_edge':c['scan_edge'],'direct_exact_mass_delta_objective':None if c['direct_exact_mass_check'] is None else c['direct_exact_mass_check']['delta_penalized_MAP_objective']})
 (out/'result.json').write_text(json.dumps({'synthetic_cases':rows,'actual_result_arithmetic_checks':cases,'non_claims':['No largefitreplication','SyntheticNNLSdoesnotvalidateAQUALPDE/operatorphysics','AllobjectivedifferencesareconditionalMAPnotmarginalevidence']},indent=2));print(json.dumps({'synthetic_cases':rows,'actual':cases},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
