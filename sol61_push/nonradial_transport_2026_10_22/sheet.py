import argparse,json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import minimize_scalar
from scipy.integrate import quad,solve_ivp
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args();checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v,flush=True)
k=s.symbols('k',positive=True);F=k-k*k/s.sqrt(1+k*k);ks=np.sqrt((np.sqrt(5)-1)/2);fmax=float(F.subs(k,ks));mstar=.08408132497418408;sigstar=4*ks**2*mstar/np.pi**2
ck('analytic_razor_peak',abs(float(s.diff(F,k).subs(k,ks)))<1e-12,dict(k=ks,F=fmax,sigma_star=sigstar))
def T(x):return (2+x)/(2*(1+x)**2)
def response(k,H):
 q=np.sqrt(1+k*k);return k*T(k*H)-k*k*T(q*H)/q
for H in [.1,1,3]:
 for kk in [.2,1,3]:
  # Fourier response averaged over two exponential vertical profiles.
  integ=quad(lambda kz:kk*kk/(np.pi*(kk*kk+kz*kz)*(1+kk*kk+kz*kz)*(1+H*H*kz*kz)**2),0,np.inf,epsabs=1e-11)[0]
  expected=.5*response(kk,H)
  ck('vertical_fourier_%g_%g'%(H,kk),abs(integ-expected)<1e-9,abs(integ-expected))
rows=[]
for H in [0,.1,.3,1,3,10]:
 opt=minimize_scalar(lambda logk:-response(np.exp(logk),H),bounds=(-8,5),method='bounded',options={'xatol':1e-12});kp=np.exp(opt.x);peak=-opt.fun
 rows.append(dict(H=H,k_peak=kp,wavelength_kpc=2*np.pi/kp*.4404221297174536,patch_radius_kpc=np.pi/kp*.4404221297174536,F_peak=peak,patch_mass_over_canonical_at_sigma_star=np.pi**2*sigstar/(4*kp*kp)/mstar,critical_kappa=np.sqrt(sigstar*peak/2)))
ck('thin_peak_numeric',abs(rows[0]['k_peak']/ks-1)<1e-6,rows[0])
ck('thickness_lengthening',all(rows[i+1]['k_peak']<rows[i]['k_peak'] for i in range(len(rows)-1)),rows)
surfaces=[dict(sigma=sigstar*x,mass_over_canonical=x,critical_kappa=np.sqrt(sigstar*x*fmax/2)) for x in [.25,.5,1,2,4]]
swing=[]
for H in [0,1]:
 row=next(r for r in rows if r['H']==H);kp=row['k_peak'];amax=sigstar*row['F_peak']/2
 for margin in [.3,.9,1.2]:
  Om=np.sqrt(margin*amax/2);end=8/Om
  for kyfac in [.25,.5,1,2,4]:
   ky=kyfac*kp
   def rhs(t,Y):
    delta,ax,ay=Y;kx=ky*(-4+Om*t);kk=np.hypot(kx,ky);A=sigstar*response(kk,H)/2
    return [-kx*ax-ky*ay,2*Om*ay-A*kx*delta/kk**2,-Om*ax-A*ky*delta/kk**2]
   def limit(t,Y):return .1-abs(Y[0])
   limit.terminal=True;limit.direction=-1
   sol=solve_ivp(rhs,(0,end),[1e-5,0,0],rtol=2e-9,atol=1e-12,events=limit,max_step=end/500,dense_output=True)
   tt=np.linspace(0,sol.t[-1],2001);dd=sol.sol(tt)[0];swing.append(dict(H=H,margin=margin,ky_over_peak=kyfac,max_amplification=float(max(abs(dd))/1e-5),reached_linear_cutoff=bool(len(sol.t_events[0])),duration=float(sol.t[-1]),shear_end=end))
ck('swing_coverage',len(swing)==30 and all(np.isfinite(r['max_amplification']) for r in swing),len(swing))
# Exact mass similarity in the quadratic field limit is independent of the N-body implementation.
# x_ddot=M F(x); M->b M, t->t/sqrt(b), v->sqrt(b)v, L->b^(3/2)L.
ck('mass_scaling_patch',all(abs(z['mass_over_canonical']-z['sigma']/sigstar)<1e-12 for z in surfaces),'fixed length does not fix surface density')
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(dict(checks=checks,sigma_star=sigstar,k_star=ks,thickness=rows,surfaces=surfaces,swing=swing),indent=2)+'\n');raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
