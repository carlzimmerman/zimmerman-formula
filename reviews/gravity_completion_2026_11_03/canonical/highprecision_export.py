import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,time,resource
from pathlib import Path
import mpmath as mp
import nearfold as nf
m=nf.m;HERE=Path(__file__).resolve().parent

def main(path):
 start=time.monotonic();r=nf.core(m.T,29);mp.mp.dps=100
 parameters={k:mp.nstr(r[k],110) for k in ('t','s','u','v','p','y','mu')}
 parameters.update(e=mp.nstr(m.E,110),z0=mp.nstr(m.Z,110),Mp_GeV=mp.nstr(m.MP,110),rhoDE_GeV4=mp.nstr(m.DE,110),nodes=29)
 coefficients={k:[str(z) for z in v] for k,v in m.DATA['fits']['29'].items()};payload=dict(parameters=parameters,coefficient_strings=coefficients,coefficient_domain=[str(z) for z in m.DATA['domain']],coefficient_e0=str(m.DATA['e0']),powers={k:str(v) for k,v in m.DATA['powers'].items()})
 # A serialization boundary is intentional. Independent reconstruction uses
 # parsed exported values only, and more arithmetic precision than the solver.
 payload=json.loads(json.dumps(payload));mp.mp.dps=120;p=payload['parameters'];e=mp.mpf(p['e']);z0=mp.mpf(p['z0']);MP=mp.mpf(p['Mp_GeV']);rho=mp.mpf(p['rhoDE_GeV4']);s,u,v,P,Y,mu=[mp.mpf(p[k]) for k in ('s','u','v','p','y','mu')];a0=mp.sqrt(2/(31*e));x0=z0/mp.sqrt(31*e)
 def coeff(k,ss):
  domain=list(map(mp.mpf,payload['coefficient_domain']));zz=(2*ss-sum(domain))/(domain[1]-domain[0]);co=list(map(mp.mpf,payload['coefficient_strings'][k]));T0=mp.mpf(1);T1=zz;value=co[0]+co[1]*T1
  for c in co[2:]:T0,T1=T1,2*zz*T1-T0;value+=c*T1
  return value*(e/mp.mpf(payload['coefficient_e0']))**mp.mpf(payload['powers'][k])
 def potential(ss,uu,vv):
  x=x0*mp.exp(ss);a=a0+uu;b=x+vv;w=P*Y+x-15*e*x*a*a+15*e*a*a*b;K=x*x+30*a*a+30*b*b
  sg=mp.exp(K/P**2)*((1-15*e*a*a+x*w/P**2)**2+30*a*a*(e*x-e*b-w/P**2)**2+30*(e*a*a/2+b*w/P**2)**2-3*w*w/P**2)
  return sg+m.cw(x,e,e,mp.sqrt(mp.mpf(29)/200)*e)+coeff('ja',ss)*uu+coeff('jb',ss)*vv+coeff('U2diag',ss)
 V=potential(s,u,v)*mu**4;grad=[mp.diff(lambda ss:potential(ss,u,v),s),mp.diff(lambda uu:potential(s,uu,v),u),mp.diff(lambda vv:potential(s,u,vv),v)]
 controls=dict(serialized_net_V_GeV4=mp.nstr(V,100),DE_relative_reconstruction_error=mp.nstr(abs(V/rho-1),30),max_dimensionless_stationarity_residual=mp.nstr(max(abs(g) for g in grad),30),Mp_over_mu_relative_consistency=mp.nstr(abs(P*mu/MP-1),30),t_vs_exp_s_relative_consistency=mp.nstr(abs(mp.exp(s)/mp.mpf(p['t'])-1),30))
 checks=dict(serialized_DE_reproduces=abs(V/rho-1)<mp.mpf('1e-25'),serialized_stationary=max(abs(g) for g in grad)<mp.mpf('1e-90'),scale_consistent=abs(P*mu/MP-1)<mp.mpf('1e-95'))
 out=dict(claim_id='CANONICAL_SERIALIZED_HIGH_PRECISION_VACUUM',checks=checks,export=payload,controls=controls,candidate=nf.clean(r),runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Reconstructs the tuned finite truncated action from the exported110-digit inputs; does not predict rhoDE or bound omitted loops')
 Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(controls,indent=2));print(checks);assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
