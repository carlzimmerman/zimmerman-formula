"""Linear minimal-coupling quantum production from an asymptotic in-vacuum."""
import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
rows=[]
for mass in [1.,2.2]:
 for tau in [.2,1.,3.]:
  for k in [.05,.2,.5,1.,2.,5.]:
   values=[]
   for tol in [1e-8,2e-10]:
    end=14*tau;win=np.sqrt(k*k+mass*mass);wout=np.sqrt(k*k+4*mass*mass)
    def rhs(t,y):
     z=t/tau;th=np.tanh(z);sech2=1-th*th;a=1.5+.5*th;app=-sech2*th/tau**2
     w2=k*k+mass*mass*a*a-app/a
     return [y[1],-w2*y[0]]
    y0=np.array([1/np.sqrt(2*win),-1j*np.sqrt(win/2)],complex)
    sol=solve_ivp(rhs,[-end,end],y0,rtol=tol,atol=tol*.01,method='DOP853')
    u,up=sol.y[:,-1];alpha=(wout*u+1j*up)/np.sqrt(2*wout);beta=(wout*u-1j*up)/np.sqrt(2*wout)
    values.append(dict(tolerance=tol,n=float(abs(beta)**2),wronskian=float(-2*np.imag(u.conjugate()*up)),bogoliubov_identity=float(abs(alpha)**2-abs(beta)**2),steps=len(sol.t),success=bool(sol.success)))
   rows.append(dict(mass=mass,tau=tau,k=k,late_speed=float(k/np.sqrt(k*k+4*mass*mass)),values=values,absolute_refinement_difference=abs(values[0]['n']-values[1]['n'])))
# Static-background negative control, same in/out frequency.
w=np.sqrt(1+.25);s=solve_ivp(lambda t,y:[y[1],-w*w*y[0]],[-10,10],[1/np.sqrt(2*w)+0j,-1j*np.sqrt(w/2)],rtol=2e-10,atol=2e-12,method='DOP853');u,up=s.y[:,-1];control=float(abs((w*u-1j*up)/np.sqrt(2*w))**2)
checks=dict(solved=all(v['success'] for r in rows for v in r['values']),wronskian=all(abs(r['values'][-1]['wronskian']-1)<1e-7 for r in rows),refinement=all(r['absolute_refinement_difference']<1e-5*max(1,r['values'][-1]['n']) for r in rows),static_vacuum=control<1e-15)
out=dict(checks=checks,all_pass=all(checks.values()),static_control_n=control,rows=rows,scope='36 selected modes, two masses, three prescribed expansion rates; leading quadratic minimal coupling; no abundance integral, backreaction or cosmological fit')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
