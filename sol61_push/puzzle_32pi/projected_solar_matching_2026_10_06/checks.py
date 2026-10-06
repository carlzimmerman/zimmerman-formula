"""Bounded nonlinear NR Solar matching experiment with preserved raw profiles."""
import argparse,json,time,sys
from pathlib import Path
import numpy as np
from solver import solve,mu_x,nu_y,T,GM,A0,X,INV
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mode',choices=['main','fine'],default='main');ap.add_argument('--control',choices=['omit_half','transfer_QUMOND','no_source']);args=ap.parse_args();outpath=Path(args.out);outpath.parent.mkdir(parents=True,exist_ok=True);rows=[];results=[]
def ck(n,v,detail=''):rows.append({'name':n,'passed':bool(v),'detail':str(detail)})
def persist(incomplete=True):outpath.write_text(json.dumps({'incomplete':incomplete,'mode':args.mode,'control':args.control,'checks':rows,'cases':results},indent=2)+'\n')
# Source inverse safety: actual mapping and a sufficient global analytic bound.
ys=np.exp(np.linspace(-18,18,4001));xs=ys*(2*nu_y(ys)-1);err=np.max(np.abs(mu_x(xs)*xs/ys-1));ck('inverse_table_residual',err<2e-8,err)
lower=1-9/(8*np.sqrt(3)*T);ck('analytic_global_inverse_lower_bound',lower>.99,lower)
if args.control:cases=[('controlcase',dict(nr=120,nt=64,rmin=.0025,rmax=40,tol=1e-10,mass=0. if args.control=='no_source' else 1.))]
elif args.mode=='fine':cases=[('coarse',dict(nr=160,nt=80,rmin=.00125,rmax=40,tol=1e-10)),('fine',dict(nr=320,nt=160,rmin=.00125,rmax=40,tol=1e-10))]
else:cases=[('coarse',dict(nr=120,nt=64,rmin=.0025,rmax=40,tol=1e-10)),('medium',dict(nr=200,nt=96,rmin=.0025,rmax=40,tol=1e-10)),('reference',dict(nr=240,nt=128,rmin=.0025,rmax=40,tol=1e-10)),('source_half',dict(nr=214,nt=96,rmin=.00125,rmax=40,tol=1e-10)),('domain_double',dict(nr=229,nt=96,rmin=.00125,rmax=80,tol=1e-10)),('tight',dict(nr=240,nt=128,rmin=.0025,rmax=40,tol=1e-12)),('Newton',dict(nr=100,nt=48,rmin=.0025,rmax=40,tol=1e-11,linear=True)),('zero_source',dict(nr=100,nt=48,rmin=.0025,rmax=40,tol=1e-11,mass=0.)),('cutoff8_nonselected',dict(nr=200,nt=96,rmin=.0025,rmax=40,tol=1e-10,kernel_T=8.)),('cutoff256_nonselected',dict(nr=200,nt=96,rmin=.0025,rmax=40,tol=1e-10,kernel_T=256.))]
try:
 for name,cfg in cases:
  r=solve(**cfg,wall=40,maxiter=140);r['name']=name;results.append(r)
  ck(name+'_Picard_converged',r['converged'],r['last_update'])
  ck(name+'_actual_nonlinear_residual',r['nonlinear_residual_scaled']<1e-9,r['nonlinear_residual_scaled'])
  mass=r['mass'];ck(name+'_conserved_source_flux',max(abs(v-mass) for v in r['mass_flux_range']+[r['mass_flux_outer']])<2e-7,r['mass_flux_range'])
  ck(name+'_no_zero_mu_face',r['min_mu_face']>1e-5,r['min_mu_face'])
  ck(name+'_inner_fit_nodes',r['fits']['(0.01, 0.025)']['nodes']>=5)
  coeff=r['fits']['(0.01, 0.025)']['A2_star'];correct=-1.5*coeff*A0/np.sqrt(GM/A0)
  ck(name+'_physical_half_Q2_dictionary',abs(r['Q2_visible_SI']-correct)<1e-38)
  if mass==0 or r['linear']:ck(name+'_no_spurious_quadrupole',abs(r['Q2_visible_SI'])<1e-31,r['Q2_visible_SI'])
  else:
   w=r['fits'];spread=abs(w['(0.01, 0.025)']['A2_star']-w['(0.015, 0.035)']['A2_star'])/abs(coeff);ck(name+'_inner_window_stability',spread<.005,spread)
  persist()
except Exception as exc:
 ck('execution_guard_or_solver_failure',False,repr(exc));persist();print(json.dumps({'error':repr(exc),'completed_cases':len(results)}));sys.exit(2)
lookup={r['name']:r for r in results}
def rel(a,b):return abs(a-b)/abs(b)
if args.control=='omit_half':
 c=results[0]['fits']['(0.01, 0.025)']['A2_star'];wrong=-3*c*A0/np.sqrt(GM/A0);ck('false_star_alone_is_visible_Q2',rel(wrong,results[0]['Q2_visible_SI'])<1e-3)
elif args.control=='transfer_QUMOND':ck('false_QUMOND_p57_Q2_transfers',rel(results[0]['Q2_visible_SI'],2.199e-26)<.05)
elif args.control=='no_source':ck('false_Sun_quadrupole_survives_without_source',abs(results[0]['Q2_visible_SI'])>1e-26)
elif args.mode=='fine':ck('fine_resolution_stability',rel(lookup['coarse']['Q2_visible_SI'],lookup['fine']['Q2_visible_SI'])<.015)
else:
 q=lambda name:lookup[name]['Q2_visible_SI']
 ck('coarse_medium_refinement',rel(q('coarse'),q('reference'))<.025)
 ck('medium_reference_refinement',rel(q('medium'),q('reference'))<.01)
 ck('source_radius_sensitivity',rel(q('source_half'),q('medium'))<.01)
 ck('outer_domain_sensitivity',rel(q('domain_double'),q('source_half'))<.01)
 ck('Picard_tolerance_sensitivity',rel(q('tight'),q('reference'))<1e-6)
 ck('conditional_Q2_above_updated_observational_scale',q('reference')>1e-26)
final={'passed':sum(x['passed'] for x in rows),'total':len(rows),'checks':rows,'cases':results,'control':args.control,'mode':args.mode,'incomplete':False,'scope':'bounded conservative nonlinear NR projectedstar matching; empirical convergence, not continuumerrorcertificate/fullcovhealth'};outpath.write_text(json.dumps(final,indent=2)+'\n');print(json.dumps({'passed':final['passed'],'total':final['total'],'failed':[x for x in rows if not x['passed']],'cases':[{k:r[k] for k in ['name','Q2_visible_SI','elapsed','iterations']} for r in results]}));sys.exit(not all(x['passed'] for x in rows))
