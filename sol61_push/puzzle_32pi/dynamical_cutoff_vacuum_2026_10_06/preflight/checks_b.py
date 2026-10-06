"""Same-vacuum-sector canonical cutoff: exact positivity and bounded rolling test."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.interpolate import PchipInterpolator
import sympy as sp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['stationary','universal_tracking','deSitter']);args=ap.parse_args();rows=[]
def ck(name,flag,detail=''):rows.append({'name':name,'passed':bool(flag),'detail':str(detail)})
def potential(T):
 scale=np.sqrt(T) if T<1 else 1.
 def hi(v,weighted=False):
  th=np.pi/2*np.sin(np.pi*v/2)**2; jac=np.pi**2/2*np.sin(np.pi*v/2)*np.cos(np.pi*v/2)
  y=T*np.tan(th);ss=np.sqrt(1+1/y); val=jac/((ss+1)*scale)
  return val*(1+.5*(1-1/ss)) if weighted else val
 i=quad(hi,0,1,epsabs=2e-10,epsrel=2e-10,limit=150)[0]
 j=quad(lambda v:hi(v,True),0,1,epsabs=2e-10,epsrel=2e-10,limit=150)[0]
 return 2*T*scale*i,j/i
# Symbolic derived homogeneous and autonomous equations, not a borrowed tracking theorem.
n,ga,p,w,x,z=sp.symbols('n ga p w x z',positive=True);s=p*sp.sqrt(n*(n-1)/ga)/2
E=2*x*x+(1+w)*(1-x*x-z*z);fx=-n*x-s*z*z+n*E*x/2;fz=s*x*z+n*E*z/2
xs=-s/n;zs2=1-xs*xs
ck('scalar_fixedpoint_x',sp.simplify(fx.subs(z*z,zs2).subs(x,xs))==0)
ck('scalar_fixedpoint_z',sp.simplify((fz/z).subs(z*z,zs2).subs(x,xs))==0)
xt=-n*(1+w)/(2*s);zt2=n*ga*(1-w*w)/((n-1)*p*p)
ck('tracking_fixedpoint_x',sp.simplify(fx.subs(z*z,zt2).subs(x,xt))==0)
ck('tracking_fixedpoint_z',sp.simplify((fz/z).subs(z*z,zt2).subs(x,xt))==0)
J=sp.Matrix([fx,fz]).jacobian([x,z]);Jt=J.subs(x,xt).subs(z*z,zt2)
ck('tracking_trace_negative',sp.simplify(sp.trace(Jt)-n*(w-1)/2)==0)
det=sp.expand(J.det()).subs(z*z,zt2).subs(x,xt);expected=n*n*(1-w*w)/2*(1-2*n*ga*(1+w)/((n-1)*p*p));ck('tracking_determinant',sp.simplify(det-expected)==0)
# Direct original y integral versus transformed integral.
vals=[]
for T in [1e-6,.01,1.,8.,128.915,256.,1e6]:
 A,ps=potential(T);vals.append({'T':T,'A':A,'A_u':A*ps,'log_slope':ps});ck('strict_positive_Au_'+str(T),A>0 and 1<ps<1.5)
 if .01<=T<=256:
  def f(y):return 2/(np.sqrt(1+1/y)+1)/(1+(y/T)**2)
  direct=quad(f,0,np.inf,epsabs=2e-9,epsrel=1e-10,limit=200)[0];ck('independent_integral_'+str(T),abs(A/direct-1)<2e-9)
Alo,plo=potential(1e-12);Ahi,phi=potential(1e9)
ck('smallT_amplitude',abs(Alo/(np.sqrt(2)*np.pi*1e-18)-1)<1e-5)
ck('smallT_slope',abs(plo-1.5)<1e-5)
ck('largeT_amplitude',abs(Ahi/(np.pi/2*1e9)-1)<1e-6)
ck('largeT_slope',abs(phi-1)<1e-6)
ugrid=np.linspace(-55,10,350);ptab=PchipInterpolator(ugrid,[potential(float(np.exp(u)))[1] for u in ugrid])
rolling=[]
for gamma,wb in [(.1,0.),(.5,0.),(2.,0.),(.1,1/3)]:
 counter=[0];nn=3;rr=np.sqrt(nn*(nn-1)/gamma)
 def rhs(N,y):
  counter[0]+=1
  if counter[0]>12000:raise RuntimeError('RHS cap')
  xx,zz,u=y;pp=float(ptab(np.clip(u,ugrid[0],ugrid[-1])));ee=2*xx*xx+(1+wb)*(1-xx*xx-zz*zz);ss=pp*rr/2
  return [-nn*xx-ss*zz*zz+nn*ee*xx/2,ss*xx*zz+nn*ee*zz/2,rr*xx]
 sol=solve_ivp(rhs,[0,45],[0,.1,np.log(128.915)],method='DOP853',rtol=3e-10,atol=2e-12,dense_output=True)
 xx,zz,u=sol.y[:,-1];Om=xx*xx+zz*zz;pp=1.5;Omtrack=2*nn*gamma*(1+wb)/((nn-1)*pp*pp)
 if Omtrack<1:target=[-np.sqrt(nn*gamma/(nn-1))*(1+wb)/pp,np.sqrt(nn*gamma*(1-wb*wb)/((nn-1)*pp*pp))];kind='tracking'
 else:target=[-pp/2*np.sqrt((nn-1)/(nn*gamma)),np.sqrt(1-pp*pp*(nn-1)/(4*nn*gamma))];kind='scalar'
 rolling.append({'gamma':gamma,'fluid_w':wb,'kind':kind,'end_x':float(xx),'end_z':float(zz),'end_u':float(u),'end_T':float(np.exp(u)),'Omega_scalar':float(Om),'target_xz':target,'RHS_calls':counter[0],'initial_T':128.915,'efolds':45})
 ck('rolling_integrator_'+str((gamma,wb)),sol.success)
 ck('rolling_attractor_'+str((gamma,wb)),max(abs(xx-target[0]),abs(zz-target[1]))<2e-4)
 ck('rolling_cutoff_runaway_'+str((gamma,wb)),u< -15)
if args.control=='stationary':ck('false_finite_cutoff_stationary',abs(potential(128.915)[0]*potential(128.915)[1])<1e-9)
if args.control=='universal_tracking':ck('false_tracking_fraction_independent_stiffness',abs(rolling[0]['Omega_scalar']-rolling[3]['Omega_scalar'])<1e-5)
if args.control=='deSitter':ck('false_rolling_future_deSitter',abs(rolling[2]['end_x'])<1e-5)
res={'checks':rows,'passed':sum(r['passed'] for r in rows),'total':len(rows),'potential_values':vals,'rolling':rolling,'control':args.control,'scope':'vacuum-sector canonical coincidence, no healthy fullcovariant/source continuation; late smallT homogeneous extension only'};out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':res['passed'],'total':res['total'],'failed':[r for r in rows if not r['passed']],'rolling':rolling}));raise SystemExit(not all(r['passed'] for r in rows))
