import os,sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import json,math,time,resource
from pathlib import Path
import mpmath as mp
from scipy.optimize import brentq
import solve as m
mp.mp.dps=100
HERE=Path(__file__).resolve().parent
CACHE={}

def core(t,n=29):
 t=mp.mpf(str(t));s=mp.log(t);key=(mp.nstr(t,40),n)
 if key in CACHE:return CACHE[key]
 x=m.X0*t;leading=31*mp.sqrt(3)*m.MP*m.E**mp.mpf('2.5')/(4*m.Z)*mp.diff(lambda tt:m.cw(m.X0*tt,m.E,m.E,mp.sqrt(mp.mpf(29)/200)*m.E)/m.E**2,t)
 y0=m.F0/mp.sqrt(3);p0=m.MP/leading
 def eq(U,V,Y,K):
  u=U*m.A0;v=V*x;p=p0/K;y=y0*Y
  f=lambda ss,uu,vv:m.potential(ss,uu,vv,p,y,n)
  return (mp.diff(lambda uu:f(s,uu,v),u)*m.A0/m.E**2,mp.diff(lambda vv:f(s,u,vv),v)*x/m.E**2,(f(s,u,v)-m.DE/(leading*K)**4)/m.E**2,mp.diff(lambda ss:f(ss,u,v),s)/(m.E**2*mp.mpf('1e-5')))
 ja=m.cf('ja',s,n);jb=m.cf('jb',s,n)
 U,V,Y,K=mp.findroot(eq,(-ja/(120*m.E)/m.A0,-jb/(120*m.E/31)/x,1,1),tol=mp.mpf('1e-85'),maxsteps=30)
 u=U*m.A0;v=V*x;p=p0/K;y=y0*Y;mu=leading*K
 f=lambda ss,uu,vv:m.potential(ss,uu,vv,p,y,n)
 H=mp.matrix([[mp.diff(lambda uu:f(s,uu,v),u,2),mp.diff(lambda uu:mp.diff(lambda vv:f(s,uu,vv),v),u)],[0,mp.diff(lambda vv:f(s,u,vv),v,2)]]);H[1,0]=H[0,1]
 C=mp.matrix([mp.diff(lambda ss:mp.diff(lambda uu:f(ss,uu,v),u),s),mp.diff(lambda ss:mp.diff(lambda vv:f(ss,u,vv),v),s)])
 ns=-mp.lu_solve(H,C);Vss=mp.diff(lambda ss:f(ss,u,v),s,2)+(C.T*ns)[0]
 A=x*x+30*ns[0]**2+30*(x+ns[1])**2+m.cf('rgraph',s,n)
 B,F,zn=m.phase(s,u,v,p,y);F+=m.cf('kgraph',s,n)
 m2=mu*mu*Vss/(2*A);a2=mu*mu*B/(2*F)
 tree,kk,ww,fn=m.sg(s,u,v,p,y,parts=True);m32=mu*mp.exp(kk/(2*p*p))*abs(ww)/p**2;Fbreak=mu*mu*mp.exp(kk/(2*p*p))*mp.sqrt(fn)
 # Fixed-order reduced rigid action, also supplying the exact-leading-tilt control.
 def rigid(ss):return m.one(ss)+m.cf('U2diag',ss,n)-m.cf('ja',ss,n)**2/(240*m.E)-m.cf('jb',ss,n)**2/(240*m.E/31)
 rs=mp.diff(rigid,s);ry=mp.sqrt((m.F0*m.F0+rigid(s)-rs)/3);mutilt=m.MP*rs/(4*x*ry)
 result=dict(t=t,s=s,n=n,x=x,u=u,v=v,p=p,y=y,mu=mu,A=A,Fmetric=F,m2=m2,a2=a2,m32=m32,Fbreak=Fbreak,Vss=Vss,normal_s=ns,relative_mu_exact_vs_finite_tilt=mu/mutilt-1,mu_finite_tilt=mutilt,root_residual=max(abs(z) for z in eq(U,V,Y,K)))
 CACHE[key]=result;return result

def clean(r,with_gaugino=True):
 mu=r['mu'];s=r['s'];R=mu*mp.sqrt(31)*r['x'];ms=mp.sqrt(r['m2']) if r['m2']>0 else mp.mpf(0)
 out=dict(nodes=r['n'],t=float(r['t']),mu_GeV=float(mu),R_GeV=float(R),m_sigma_GeV=float(ms),m_sigma2_GeV2=float(r['m2']),m_phase_GeV=float(mp.sqrt(r['a2'])),m32_GeV=float(r['m32']),F_tree_SUGRA_GeV2=float(r['Fbreak']),A_over_R2=float(r['A']/(31*r['x']**2)),F_over_R2=float(r['Fmetric']/(31*r['x']**2)),reduced_log_curvature=float(r['Vss']),relative_mu_exact_vs_finite_tilt=float(r['relative_mu_exact_vs_finite_tilt']),root_scaled_max_residual=mp.nstr(r['root_residual'],12))
 if with_gaugino:
  masses=m.gauginos(s);out['gauginos_GeV']={k:float(v*mu) for k,v in masses.items()};out['m_sigma_over_photino']=float(ms/(masses['U1']*mu));out['gaugino_log_slopes']={}
  for hh in ('.005','.0025'):
   h=mp.mpf(hh);zs=[m.gauginos(s+j*h) for j in (-2,-1,0,1,2)]
   out['gaugino_log_slopes'][hh]={k:float((zs[0][k]-8*zs[1][k]+8*zs[3][k]-zs[4][k])/(12*h*masses[k])) for k in masses}
 return out

def main(out):
 start=time.monotonic();folds=[];rows=[];controls=[]
 for n in (21,29):
  tf=brentq(lambda t:float(core(t,n)['m2']),1.265,1.269,xtol=2e-14)
  folds.append(clean(core(tf,n)))
  # The physical threshold masses vary smoothly; calculate the target roots
  # with direct threshold evaluations, not a fictitious constant cchi.
  for ratio in (2.01,2.1,3.,4.,10.):
   def cond(t):
    r=core(t,n);chi=m.gauginos(r['s'])['U1']*r['mu'];return float(r['m2']-mp.mpf(str(ratio))**2*chi**2)
   root=brentq(cond,tf-.002,tf-1e-12,xtol=2e-14);r=core(root,n);row=clean(r);row['target_ratio']=ratio;row['distance_to_fold']=tf-root;rows.append(row)
  print('completed fold',n,tf,flush=True)
 # Analytic Schur mass vs the frozen finite-stencil candidate.
 r=core(m.T,29);old=json.load(open(HERE/'run_solve/result.json'))['points'][-1]
 controls.append(dict(check='analytic_Schur_vs_stencil_candidate',mass_relative_difference=abs(float(mp.sqrt(r['m2']))/old['rows'][-1]['m_sigma_GeV']-1)))
 fold_difference=abs(folds[1]['t']-folds[0]['t']);root_differences=[dict(ratio=q,delta_t=abs(rows[i+5]['t']-rows[i]['t']),mass_relative_difference=abs(rows[i+5]['m_sigma_GeV']/rows[i]['m_sigma_GeV']-1)) for i,q in enumerate((2.01,2.1,3.,4.,10.))]
 checks=dict(folds_agree=fold_difference<1e-8,threshold_roots_match=max(abs(r['m_sigma_over_photino']/r['target_ratio']-1) for r in rows)<1e-6,positive_phase=all(r['m_phase_GeV']>0 for r in rows),ratio_roots_stable=all(r['distance_to_fold']>0 for r in rows),Schur_control=controls[0]['mass_relative_difference']<1e-7)
 result=dict(claim_id='CANONICAL_FINE_NEARFOLD',checks=checks,folds=folds,threshold_points=rows,fold_node_difference=fold_difference,root_node_differences=root_differences,controls=controls,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['Root and interpolation convergence are numerical errors, not an all-orders fold uncertainty.','Uncomputed three-loop rigid and gravity loop matching remain outside the finite action.','Near-fold radial mass is selected by tuning t; no dynamics selects this tuning.'])
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','fold_node_difference','root_node_differences','runtime_seconds','peak_rss_bytes_macos')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
