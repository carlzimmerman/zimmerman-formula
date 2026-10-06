"""Retarded auxiliary/full-FRW and frozen-background local-source audit."""
import argparse,json,math,platform
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import scipy,sympy as s,mpmath as mp
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mutation',choices=['none','Box_constant','drop_spatial','local_G_equals_F_initial'],default='none');arg=p.parse_args();out=Path(arg.out);out.mkdir(parents=True,exist_ok=True)
checks=[]
def ck(name,ok,detail):checks.append({'name':name,'passed':bool(ok),'detail':detail})
t,H,al=s.symbols('t H alpha',positive=True);n=s.symbols('n',integer=True,positive=True);AH=n*(n-1)*H**2/2;R=n*(n+1)*H**2
X=-(n+1)*(H*t-(1-s.exp(-n*H*t))/n)
Xd=s.diff(X,t);Xdd=s.diff(Xd,t)
ck('retarded_exact_dS_Box_equation',s.simplify(-Xdd-n*H*Xd-R)==0,{'X':str(X)})
ck('retarded_initial_data',s.simplify(X.subs(t,0))==0 and s.simplify(Xd.subs(t,0))==0,{})
ck('constant_vacuum_not_constant_Box_inverse',s.simplify(Xd)!=0 if arg.mutation!='Box_constant' else s.simplify(Xd)==0,{'Xdot':str(Xd)})
F=1+2*al*X;Y=al*X
E00=AH*F+n*H*s.diff(F,t)+s.diff(X,t)*s.diff(Y,t)/2
Esp=-AH*F-s.diff(F,t,2)-(n-1)*H*s.diff(F,t)+s.diff(X,t)*s.diff(Y,t)/2
initial_sum=s.simplify((E00+Esp).subs(t,0))
ck('linear_exact_dS_requires_alpha_zero',s.simplify(initial_sum-2*al*R)==0 and initial_sum!=0 if arg.mutation!='drop_spatial' else initial_sum==0,{'E00_plus_Esp_at_initial':str(initial_sum),'E00_secular_slope':str(s.limit(s.diff(E00,t),t,s.oo))})
# Full nonlinear exact-dS reduction; F0 fixed by initial Friedmann constraint.
f,F0=s.symbols('F F0');Fp,Fpp,xy=s.symbols('Fdot Fddot XdotYdot')
constraint=n*(n-1)*H**2*(f-F0)/2+n*H*Fp+xy/2
accel=H*Fp-Fpp+xy
reduced=s.expand(2*constraint.subs(xy,s.solve(accel,xy)[0]))
ck('general_exact_dS_F_equation',s.simplify(reduced-(Fpp+(2*n-1)*H*Fp+n*(n-1)*H**2*(f-F0)))==0,{'equation':str(reduced)})
lam=s.symbols('lambda');ck('dS_reduction_roots',s.simplify(lam**2+(2*n-1)*H*lam+n*(n-1)*H**2-(lam+H*n)*(lam+H*(n-1)))==0,{})
# frozen quasi-static local trace and force equations (n>=3).
Fb,pb,kappa,rho=s.symbols('Fbar p kappa rho',nonzero=True);D=(n-1)*Fb-4*n*pb
dR=2*kappa*rho/D;lapF=2*pb*dR
lapPhi=(kappa*rho+lapF)/(Fb*(n-1));lapPsi=(n-2)*lapPhi-lapF/Fb
Gdyn=s.simplify(lapPsi/(kappa*rho*(n-2)/(n-1)))
ck('general_dimension_local_force',s.simplify(Gdyn-(1/Fb)*(1-4*pb/((n-2)*D)))==0,{'G_Newton_dyn_over_G_Newton_bare':str(s.factor(Gdyn))})
G4=s.simplify(Gdyn.subs(n,3));ck('four_dimension_local_force',s.simplify(G4-(Fb-8*pb)/(Fb*(Fb-6*pb)))==0,{'Gdyn':str(G4)})
ck('local_force_not_just_Einstein_prefactor',s.simplify(G4-1/Fb)!=0 if arg.mutation!='local_G_equals_F_initial' else s.simplify(G4-1/Fb)==0,{})
ck('four_dimension_lensing',s.simplify((lapPhi+lapPsi).subs(n,3)-kappa*rho/Fb)==0,{})
cap=(n-1)**2/(n*(n-2));gain=s.simplify(Gdyn*Fb)
ck('frozen_prefactor_force_bound_identity',s.simplify(cap-gain-(n-1)*Fb/(n*(n-2)*D))==0,{'restriction':'n>=3,Fbar>0,D>0; EHprefactor not evolving vacuum response'})
# A legitimate saturating escape: f=beta(1-exp X), solve all background equations.
rows=[]
def integrate(nn,beta,rtol,m0=0):
 AA=nn*(nn-1)/2.;Kvac=AA # kappa rho chosen to give initial GR H=1; f(0)=0.
 def rhs(time,v):
  HH,xx,xd,yy,yd,mm=v;ex=math.exp(xx);ff=beta*(1-ex);fp=-beta*ex;fpp=fp;FF=1+ff+yy;fd=fp*xd+yd;den=(nn-1)*FF-4*nn*fp
  hd=((nn+1)*HH*fd-fpp*xd*xd+2*nn*(nn+1)*fp*HH*HH+xd*yd-AA*mm)/den
  ric=2*nn*hd+nn*(nn+1)*HH*HH
  return [hd,xd,-nn*HH*xd-ric,yd,-nn*HH*yd-ric*fp,-nn*HH*mm]
 times=np.linspace(0,80,801)
 sol=solve_ivp(rhs,[0,80],[math.sqrt(1+m0),0,0,0,0,m0],rtol=rtol,atol=rtol*.01,method='DOP853',t_eval=times,max_step=.25)
 assert sol.success
 HH,xx,xd,yy,yd,mm=sol.y;ex=np.exp(xx);ff=beta*(1-ex);fp=-beta*ex;FF=1+ff+yy;fd=fp*xd+yd
 residual=(AA*HH*HH*FF+nn*HH*fd+.5*xd*yd-Kvac*(1+mm))/Kvac
 dd=(nn-1)*FF-4*nn*fp
 dyn=(1/FF)*(1-4*fp/((nn-2)*dd)) if nn>2 else np.full_like(FF,np.nan)
 row={'n_spatial':nn,'beta':beta,'initial_matter_to_vacuum_ratio':m0,'matter_final':float(mm[-1]),'H_final':float(HH[-1]),'F_final':float(FF[-1]),'Y_final':float(yy[-1]),'f_prime_final':float(fp[-1]),'constraint_relative_error_max':float(np.max(np.abs(residual))),'min_F':float(FF.min()),'min_trace_denominator':float(dd.min()),'late_Hdot':float(rhs(80,sol.y[:,-1])[0]),'Einstein_vacuum_coefficient_over_G_EH_bare_final':float(1/(HH[-1]*0+FF[-1])),'G_Newton_dyn_over_G_Newton_bare_final':float(dyn[-1]) if nn>2 else None,'G_Newton_dyn_over_G_Newton_bare_initial':float(dyn[0]) if nn>2 else None,'H2F_final':float(HH[-1]**2*FF[-1])}
 return row,sol
for nn in [2,3,4]:
 for beta in [0,.05,.2]:
  row,sol=integrate(nn,beta,2e-10);rows.append(row)
  ck('saturating_full_FRW_constraint',row['constraint_relative_error_max']<1e-7,{'n':nn,'beta':beta,'error':row['constraint_relative_error_max']})
  ck('saturating_asymptotic_dS',abs(row['late_Hdot'])<1e-9 and abs(row['H2F_final']-1)<1e-7,{'n':nn,'beta':beta,'H2F':row['H2F_final']})
  ck('saturating_positive_background_coefficients',row['min_F']>0 and row['min_trace_denominator']>0,{'n':nn,'beta':beta,'not_claim':'not full perturbation stability'})
  if nn>2:ck('late_relative_vacuum_Newton_renormalizations_coincide',abs(row['G_Newton_dyn_over_G_Newton_bare_final']-row['Einstein_vacuum_coefficient_over_G_EH_bare_final'])<1e-12,{'n':nn,'beta':beta})
row1,ss=integrate(3,.2,2e-10);row2,_=integrate(3,.2,2e-12)
ck('ODE_tolerance_control',abs(row1['H_final']-row2['H_final'])<1e-9 and abs(row1['F_final']-row2['F_final'])<1e-9,{'H_difference':row1['H_final']-row2['H_final'],'F_difference':row1['F_final']-row2['F_final']})
memory_row,memory_sol=integrate(3,.2,2e-10,m0=10)
ck('past_matter_history_changes_late_response',abs(memory_row['F_final']-row1['F_final'])>.01 and memory_row['matter_final']<1e-20 and memory_row['constraint_relative_error_max']<1e-7,{'vacuum_initial_history':row1,'matter_initial_history':memory_row})
np.savez_compressed(out/'saturating_n3_beta02.npz',t=ss.t,state=ss.y)
result={'all_passed':all(c['passed'] for c in checks),'checks':checks,'saturating_rows':rows,'memory_control':memory_row,'mutation':arg.mutation,'software':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':s.__version__},'non_claims':['No MOND acceleration source or32pi selector','No complete retarded nonlocal stability proof','Local response frozen-background subhorizon approximation','Exact initial-dS obstruction does not exclude a late-dS attractor after history']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if result['all_passed'] else 1)
