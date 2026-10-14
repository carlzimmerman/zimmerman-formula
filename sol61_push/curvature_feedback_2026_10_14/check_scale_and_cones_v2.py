import json,sys,math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import minimize_scalar
import background as B
out=Path(sys.argv[1]);out.mkdir(exist_ok=False)
checks=[]
def ck(n,v):
 checks.append({'name':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
def eq(n,v):ck(n,s.simplify(v)==0)
h,hd,d,dd,v,S,g=s.symbols('H Hdot Fdot Fddot phi_dot matter_enthalpy Fphi')
w1=1+8*h*d;w2=2*h+24*h*h*d;w3=-9*h*h+s.Rational(3,2)*v*v-144*h**3*d;w4=1+8*dd
w1d=8*hd*d+8*h*dd;w2d=2*hd+48*h*hd*d+24*h*h*dd
D4=4*w1*w3+9*w2*w2
num=3*(2*w1*w1*w2*h-w2*w2*w4+4*w1*w1d*w2-2*w1*w1*w2d)-6*w1*w1*S
rayS=-2*w1*hd-v*v-8*h*h*(dd-h*d)
reduced=1+128*g*g*h*h*(w1*hd-2*h*h*(dd-h*d))/(w1*(w1+96*g*g*h**4))
eq('positive scalar kinetic factorization',D4.subs(d,g*v)-6*v*v*((w1+96*g*g*h**4).subs(d,g*v)))
eq('raw matter sound formula reduction',(num/(w1*D4)).subs(S,rayS).subs(d,g*v)-reduced.subs(d,g*v))
cone=1+32*g*g*h*h*(6*w1*hd+v*v+S)/(w1*(w1+96*g*g*h**4))
eq('NEC growth and cone identity',(reduced-cone).subs(S,rayS))
eq('GR limit of characteristic speed',reduced.subs(g,0)-1)

def scan(sol,lam,eta,scale):
 tt=np.unique(np.concatenate([sol.t,np.linspace(0,sol.t[-1],10001)]));ys=sol.sol(tt);rows=[];raw_errors=[]
 for i,state in enumerate(ys.T):
  p,v,c,w,r,h,N=state;acc,hd,Q,Ft,det=B.detail(state,lam,eta,scale);fp,fpp=B.coupling(p,eta,scale);fd=fp*v;fdd=fpp*v*v+fp*acc;D=Q+96*fp*fp*h**4
  cs=1+128*fp*fp*h*h*(Q*hd-2*h*h*(fdd-h*fd))/(Q*D)
  kin=2*Q*D/(2+24*h*fd)**2
  rows.append([cs,kin,hd,Q,Ft,Ft/Q])
  if i%37==0 and abs(v/h)>1e-3:
   w2=2*h+24*h*h*fd;w3=-9*h*h+1.5*v*v-144*h**3*fd
   w1d=8*hd*fd+8*h*fdd;w2d=2*hd+48*h*hd*fd+24*h*h*fdd
   raw=(3*(2*Q*Q*w2*h-w2*w2*Ft+4*Q*w1d*w2-2*Q*Q*w2d)-6*Q*Q*(w*w+4*r/3))/(Q*(4*Q*w3+9*w2*w2))
   raw_errors.append(abs(raw-cs))
 a=np.array(rows)
 return {'min_scalar_speed_squared':float(min(a[:,0])),'max_scalar_speed_squared':float(max(a[:,0])),'min_normalized_scalar_kinetic':float(min(a[:,1])),'max_tensor_speed_squared':float(max(a[:,5])),'max_Hdot':float(max(a[:,2])),'raw_formula_max_abs_error':float(max(raw_errors)) if raw_errors else None},tt,a

def refine_FT_minimum(sol,lam,eta,scale):
 times=np.unique(np.concatenate([sol.t,np.linspace(0,min(500.,sol.t[-1]),10001)]))
 values=np.array([B.detail(sol.sol(t),lam,eta,scale)[3] for t in times]);i=int(np.argmin(values))
 lo=times[max(0,i-1)];hi=times[min(len(times)-1,i+1)]
 opt=minimize_scalar(lambda t:B.detail(sol.sol(t),lam,eta,scale)[3],bounds=(lo,hi),method='bounded',options={'xatol':1e-10})
 ck('continuous FT extremum optimizer succeeds',opt.success)
 return {'value':float(opt.fun),'time':float(opt.x),'sampled_value':float(values[i]),'bracket':[float(lo),float(hi)]}

original=(B.MI,B.GAMMA)
try:
 cold=[]
 for lam in [1.,100.,10000.]:
  sol,row=B.evolve(lam=lam,end=5000,rtol=2e-12,atol=1e-15)
  screen,_,_=scan(sol,lam,.1,None)
  ck('cold scalar kinetic screen lambda='+str(lam),screen['min_normalized_scalar_kinetic']>0)
  ck('cold scalar gradient screen lambda='+str(lam),screen['min_scalar_speed_squared']>.9)
  ck('cold raw/reduced characteristic agreement lambda='+str(lam),screen['raw_formula_max_abs_error']<1e-5)
  cold.append({'lam':lam,**screen})
 eta=3*np.exp(4)/(2*.01*16);scale_rows=[]
 for hi in [.032,.04,.06,.08,.1,.2,.5]:
  B.MI=hi*np.sqrt(6)/15;B.GAMMA=.05*B.MI
  sol,row=B.evolve(lam=0,eta=eta,scale=1,end=2000,rtol=2e-10,atol=1e-13)
  row.update(initial_H_target=hi,inflaton_mass=B.MI,inflaton_decay_rate=B.GAMMA)
  ck('scale scan constraint Hi='+str(hi),row['max_Friedmann_relative_residual']<1e-6)
  if hi in [.032,.04]:ck('slow source tensor screen reaches end Hi='+str(hi),row['termination']=='end time')
  else:ck('faster source hits tensor gradient boundary Hi='+str(hi),row['termination']=='tensor gradient zero')
  scale_rows.append(row)
 B.MI=.04*np.sqrt(6)/15;B.GAMMA=.05*B.MI
 sol,rescue=B.evolve(lam=0,eta=eta,scale=1,end=30000,rtol=2e-10,atol=1e-13)
 ck('slow formation completes extended interval',rescue['termination']=='end time')
 rescue['FT_continuous_minimum']=refine_FT_minimum(sol,0,eta,1)
 ck('slow formation positive tensor coefficients',min(rescue['min_QT'],rescue['FT_continuous_minimum']['value'])>.05)
 ck('extended trajectory approaches nonzero de Sitter point',abs(rescue['end_phi']-2)<1e-4 and abs(rescue['end_H']/math.sqrt(.04/6)-1)<1e-4)
 screen,tt,arr=scan(sol,0,eta,1);rescue['principal_diagnostic']=screen
 ck('slow formation scalar gradient diagnostic',screen['min_scalar_speed_squared']>.8)
 ck('slow formation scalar kinetic diagnostic',screen['min_normalized_scalar_kinetic']>0)
 ck('rescue uses increasing Hubble rate',screen['max_Hdot']>0)
 ck('rescued path is not matter-cone subluminal',screen['max_scalar_speed_squared']>1.5)
 ck('raw/reduced rescued characteristic agreement',screen['raw_formula_max_abs_error']<1e-5)
 refsol,ref=B.evolve(lam=0,eta=eta,scale=1,end=30000,rtol=2e-12,atol=1e-15)
 ref['FT_continuous_minimum']=refine_FT_minimum(refsol,0,eta,1)
 ck('refined slow path completes',ref['termination']=='end time')
 ck('refined slow path positive tensor coefficients',min(ref['min_QT'],ref['FT_continuous_minimum']['value'])>.05)
 ck('rescued endpoint refinement',abs(ref['end_phi']-rescue['end_phi'])<1e-6)
 ck('rescued minimum FT refinement',abs(ref['FT_continuous_minimum']['value']-rescue['FT_continuous_minimum']['value'])<1e-5)
 # Store a compact history; include transient and late approach.
 ts=np.unique(np.concatenate([np.linspace(0,500,3001),np.linspace(500,30000,5901)]));yy=sol.sol(ts);kin=[];cs=[];ct=[]
 for state in yy.T:
  p,v,c,w,r,h,N=state;ac,hd,Q,Ft,de=B.detail(state,0,eta,1);fp,fpp=B.coupling(p,eta,1);fd=fp*v;fdd=fpp*v*v+fp*ac
  cs.append(1+128*fp*fp*h*h*(Q*hd-2*h*h*(fdd-h*fd))/(Q*(Q+96*fp*fp*h**4)));ct.append(Ft/Q)
 history={'time':ts.tolist(),'phi':yy[0].tolist(),'H':yy[5].tolist(),'scalar_speed_squared':cs,'tensor_speed_squared':ct}
 result={'passed':len(checks),'checks':checks,'cold_principal_diagnostics':cold,'initial_curvature_scan':scale_rows,'slow_formation':rescue,'refined_slow_formation':ref,'exact_source_free_implication':'For canonical scalar+F(phi)GB with QT>0, D>0 and Fphi!=0, Hdot>0 implies cS^2>1. Healthy minimally coupled perfect-fluid extension uses S>=0. Reheating-model application is conditional on its lower-derivative matter principal closure.','scope':'No stable causal unified tether theory established. Positive numerical principal diagnostics are not full covariant reheating, nonlinear, UV, scalar spectrum or observational certificates.'}
 (out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'history.json').write_text(json.dumps(history)+'\n');print(json.dumps(result,indent=2))
finally:B.MI,B.GAMMA=original
