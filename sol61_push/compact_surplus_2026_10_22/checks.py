import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,solve_bvp,quad
from scipy.optimize import brentq
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
checks=[];rows=[]
def ck(n,b,v):
 checks.append(dict(name=n,passed=bool(b),value=v));print(n,b,v,flush=True)
def interior(sc,lam,bm,tol):
 eps=1e-9;d=(3*bm+sc+lam*sc**3)/3
 def f(x,Y):
  z=max(Y[0],0)/x**2;y=(z+np.sqrt(z*z+4*z))/2
  return [x*x*(3*bm/(1+x*x)**2.5+Y[1]+lam*Y[1]**3),-y]
 def end(x,Y):return Y[1]
 end.terminal=True;end.direction=-1
 sol=solve_ivp(f,(eps,3.5),[d*eps**3,sc-2/3*np.sqrt(d)*eps**1.5],events=end,dense_output=True,rtol=tol,atol=tol*1e-7,max_step=.02,method='DOP853')
 assert sol.success and len(sol.t_events[0])==1
 return sol,float(sol.t_events[0][0])
def exterior(R,w0,lam,offset,tol):
 L=R+offset;x=R+(L-R)*np.linspace(0,1,220)**2
 def fun(x,Y):
  s,w=Y
  return np.array([-w/(1-w),-2*w/x-s-lam*s**3])
 def bc(ya,yb):return np.array([ya[1]-w0,yb[0]-yb[1]*L/(L+1)])
 w=w0*np.exp(R-x)*(R/x)**2*(x+1)/(R+1)
 guess=np.array([w*x/(x+1),w])
 sol=solve_bvp(fun,bc,x,guess,tol=tol,max_nodes=18000)
 if not sol.success:raise RuntimeError(sol.message)
 return sol

def one(sc,lam,bm,tol,offset):
 ins,Rzero=interior(sc,lam,bm,tol*.01)
 def vals(R):
  Q,s=ins.sol(R);z=Q/R**2;y=(z+np.sqrt(z*z+4*z))/2
  return s,y,y/(1+y)
 def residual(R):
  s,y,w=vals(R);ex=exterior(R,w,lam,offset,tol)
  return s-ex.y[0,0]
 R=brentq(residual,Rzero*1e-4,Rzero*(1-1e-7),xtol=tol*.01,rtol=tol*.01)
 ss,yy,ww=vals(R);ex=exterior(R,ww,lam,offset,tol)
 mt=R*R*yy;mb=bm*R**3/(1+R*R)**1.5;mc=mt-mb
 def rho(x):
  Q,s=ins.sol(x);z=Q/x**2;y=(z+np.sqrt(z*z+4*z))/2
  # Differentiate q(y); q'=y(2+y)/(1+y)^2.
  B=3*bm/(1+x*x)**2.5
  yp=(B+s+lam*s**3-2*z/x)/(y*(2+y)/(1+y)**2)
  return yp+2*y/x-B
 integ=quad(lambda x:x*x*rho(x),1e-10,R,epsabs=1e-9,epsrel=1e-7)[0]
 grid=np.geomspace(1e-8*R,R,400)
 # KKT: psi=Phi+h >= mu in vacuum. Compute its derivative and integral.
 xx=np.linspace(R,R+offset,800);s,w=ex.sol(xx)
 gc=(mc+bm*xx**3/(1+xx*xx)**1.5)/xx**2
 gap_prime=gc-w/(1-w)
 # Outside cold support, Phi includes all baryons, also beyond R.
 phi=-mc/xx-bm/np.sqrt(1+xx*xx)
 mu=-mc/R-bm/np.sqrt(1+R*R)+ss
 gap=phi+s-mu
 # Project actual cold density and mass, not e or polarization separately.
 proj=[]
 for frac in [.1,.5,.9,1.1,2.,10.]:
  b=frac*R
  if b<R:
   sigma=2*quad(lambda z:rho(np.hypot(b,z)),0,np.sqrt(R*R-b*b),epsabs=1e-8)[0]
   menc=quad(lambda x:x*x*rho(x),1e-10,b,epsabs=1e-9)[0]
   cyl=menc+quad(lambda x:x*x*rho(x)*(1-np.sqrt(max(0,1-b*b/x**2))),b,R,epsabs=1e-9)[0]
  else:sigma=0.;cyl=mc
  # Sigma unit M0/(4pi ell^2); mean Sigma in same units =4Mcyl/b^2.
  proj.append(dict(R_over_edge=frac,Sigma=sigma,DeltaSigma=4*cyl/b**2-sigma,cyl_mass=cyl))
 return dict(s_center=sc,lambda_phase=lam,baryon_mass=bm,R=R,R_zero=Rzero,mass_c=mc,mass_total_inside=mt,s_edge=ss,w_edge=ww,rho_edge=float(rho(R)),rho_min=float(min(rho(grid))),mass_integral_error=abs(integ-mc)/mc,mu=mu,min_gap=float(min(gap)),min_gap_derivative=float(min(gap_prime)),match_error=abs(residual(R)),projection=proj)
for sc in [.01,.1,1.,10.]:
 for lam in [0.,1.]:
  for bm in [0.,1.]:
   try:
    r=one(sc,lam,bm,2e-5,20);r2=one(sc,lam,bm,2e-7,30)
    err=max(abs(r[k]-r2[k])/max(abs(r2[k]),1e-10) for k in ['R','mass_c','s_edge'])
    r2['repeat_error']=err;rows.append(r2)
    ck('matched_%g_%g_%g'%(sc,lam,bm),err<3e-4 and r2['rho_min']>0 and r2['mass_integral_error']<2e-5 and r2['min_gap']>-1e-6 and r2['mu']<0,dict(R=r2['R'],mass=r2['mass_c'],error=err,gap=r2['min_gap']))
   except Exception as e:
    ck('solver_%g_%g_%g'%(sc,lam,bm),False,str(e))
ck('coverage',len(rows)==16,len(rows))
if rows:
 ck('positive_density_jump',all(r['rho_edge']>0 for r in rows),min(r['rho_edge'] for r in rows))
 ck('positive_surplus_at_edge',all(r['s_edge']>0 and r['R']<r['R_zero'] for r in rows),min(r['s_edge'] for r in rows))
 ck('projected_outer_mass',all(abs(p['DeltaSigma']*(p['R_over_edge']*r['R'])**2/4-r['mass_c'])<1e-8*max(1,r['mass_c']) for r in rows for p in r['projection'] if p['R_over_edge']>1),len(rows)*3)
out=dict(checks=checks,rows=rows,units='length ell0; mass a0 ell0^2/G; density a0/(4piG ell0); projected density a0/(4piG)',status='passed' if all(c['passed'] for c in checks) else 'failed')
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
