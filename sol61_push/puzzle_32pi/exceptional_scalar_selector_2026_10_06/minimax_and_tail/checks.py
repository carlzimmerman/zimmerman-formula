import argparse,json,pathlib,sys
import sympy as s,mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',default='none');a=ap.parse_args();mp.mp.dps=50;rows=[];values={}
def ck(n,v):rows.append({'name':n,'pass':bool(v)})
x,z,L,c,d,j,j1,j2,R=s.symbols('x z L c d j j1 j2 R',positive=True)
ck('cosh_addition',s.expand_trig(s.cosh(z+L))-s.cosh(z)*s.cosh(L)-s.sinh(z)*s.sinh(L)==0)
h=j**s.Rational(1,2)/s.sqrt(c+d*j*j)
ck('turnover_derivative',s.simplify(s.diff(h,j)/h-(c-d*j*j)/(2*j*(c+d*j*j)))==0)
q,t=s.symbols('q t',positive=True);e=(q-1)/(q+1)
ck('balanced_minimum',s.simplify(2/(q+1)-(1-e))==0)
ck('balanced_maximum',s.simplify(2*q/(q+1)-(1+e))==0)
ck('geometric_center_endpoints',s.simplify((c/j1+d*j1).subs(c,d*j1*j2)-(c/j2+d*j2).subs(c,d*j1*j2))==0)
for rr in [10,100]:
 ll=mp.log(rr);qstar=mp.sqrt(mp.cosh(ll/2));eps=(qstar-1)/(qstar+1);values[str(rr)]={'q':str(qstar),'epsilon':str(eps)}
 ck('error_positive_'+str(rr),eps>0)
 ck('sharp_q_'+str(rr),abs(qstar**2-(mp.sqrt(rr)+1/mp.sqrt(rr))/2)<mp.mpf('1e-48'))
 for zz in [-ll,-ll/2,0,ll/4,ll/2,3*ll/4,ll,2*ll]:
  if 0<=zz<=ll:qr=mp.sqrt(mp.cosh(max(zz,ll-zz)))
  else:aa=min(abs(zz),abs(zz-ll));qr=mp.sqrt(mp.cosh(aa+ll)/mp.cosh(aa))
  ck('turnover_global_grid_'+str(rr)+'_'+str(zz),qr>=qstar-mp.mpf('1e-48'))
 # centered shape and optimal amplitude, continuous theorem in report
 hmin=1/mp.sqrt(mp.cosh(ll/2));amp=2/(1+hmin)
 errs=[abs(amp/mp.sqrt(mp.cosh(ll*i/40-ll/2))-1) for i in range(41)]
 ck('attainment_'+str(rr),max(errs)<=eps+mp.mpf('1e-48'))
 ck('endpoints_balance_'+str(rr),abs(errs[0]-errs[20])<mp.mpf('1e-48'))
ck('one_decade_floor',mp.mpf(values['10']['epsilon'])<mp.mpf('.01') if a.control=='one_percent' else mp.mpf(values['10']['epsilon'])>mp.mpf('.13'))
ratio2=(j2/j1)*(c-d*j1*j1)/(c-d*j2*j2)
ck('opposite_ratio_excess',s.simplify(ratio2-j2/j1-d*j2*(j2*j2-j1*j1)/(j1*(c-d*j2*j2)))==0)
ck('opposite_cannot_improve',mp.sqrt(10)<mp.mpf(values['10']['q']) if a.control=='opposite_better' else mp.sqrt(10)>mp.mpf(values['10']['q']))
alpha,lam,A,y=s.symbols('alpha lam A y',positive=True)
u=j/s.sqrt(c+d*j*j);integrand=alpha*u.subs(j,lam*A*y)/A
ck('saturating_tail_limit',s.limit(integrand,y,s.oo)==alpha/(A*s.sqrt(d)))
ck('tail_not_integrable',s.limit(integrand,y,s.oo)==0 if a.control=='finite_tail' else s.limit(integrand,y,s.oo)>0)
ck('canonical_integrand_linear',s.simplify(alpha*lam*y/s.sqrt(c)/y-alpha*lam/s.sqrt(c))==0)
ck('small_source_scalar_linear',s.limit(u/j,j,0)==1/s.sqrt(c))
res={'checks':rows,'passed':sum(r['pass'] for r in rows),'failed':sum(not r['pass'] for r in rows),'control':a.control,'minimax':values,'grid_scope':'8 turnover positions and41 field points perR, corroboration only'}
pathlib.Path(a.output).parent.mkdir(parents=True,exist_ok=True);pathlib.Path(a.output).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res));sys.exit(bool(res['failed']))
