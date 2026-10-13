"""Regular outgoing-null packet crosses the old cosmological horizon."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,simpson,cumulative_trapezoid
from scipy.optimize import brentq

ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True)
OUT=Path(ap.parse_args().output_dir)
root=Path(__file__).parent
src=json.loads((root/'source_snapshot/self_gravity_results.json').read_text())
case=next(c for c in src['cases'] if c['b']==1000)
b=1000;Y=case['Y'];C=Y**2/(2*b);E=np.sqrt(1-C)
def B(x):return 1-C*(2/(3*x)+x*x/3)
def S(x):return np.sqrt(C)*(x-1)*np.sqrt((x+2)/(3*x))
xh=brentq(B,1+1e-8,2*np.sqrt(3/C),xtol=1e-13)
assert C*(2/(3*xh*xh)-2*xh/3)<0
labels=np.linspace(.98*xh,.99*xh,257);times=np.array([0,.025,.05,.075,.1])
f0=np.sin(np.pi*(labels-labels[0])/(labels[-1]-labels[0]))**2
w0=labels**2/(E+S(labels));charge0=float(simpson(w0*f0,x=labels))
def field(x):
 H=np.sqrt((x+2)/(3*x));Hp=-1/(3*x*x*H)
 sv=S(x);sp=np.sqrt(C)*(H+(x-1)*Hp)
 V=sv*(E+sv)/np.sqrt(C)
 Vp=sp*(E+2*sv)/np.sqrt(C)
 reaction=(E+sv)/np.sqrt(C)*(2*sv/x+sp)
 return V,Vp,reaction
def rhs(t,y):
 x,j,n=y.reshape(3,-1);V,Vp,reaction=field(x)
 return np.concatenate([V,Vp,-reaction])
initial=np.concatenate([labels,np.zeros_like(labels),np.zeros_like(labels)])
stages=[]
for tight in [False,True]:
 sol=solve_ivp(rhs,(0,.1),initial,t_eval=times,method='DOP853',rtol=2e-13 if tight else 2e-11,atol=2e-15 if tight else 2e-13)
 assert sol.success,sol.message
 stages.append(sol.y.reshape(3,len(labels),len(times)))
diff=float(np.max(abs(stages[0]-stages[1])));assert diff<1e-7
x,logj,logn=stages[-1];J=np.exp(logj);f=f0[:,None]*np.exp(logn)
w=x*x/(E+S(x));expected=f0[:,None]*w0[:,None]/w/J
identity=float(np.max(abs(f-expected))/(1+np.max(abs(f))));assert identity<1e-8
assert x.min()>=.97*xh and x.max()<=1.2*xh
assert x[:,-1].min()>xh and np.all(B(x[:,0])>0) and np.all(B(x[:,-1])<0)
records=[]
for i,time in enumerate(times):
 q=float(simpson(w[:,i]*f[:,i]*J[:,i],x=labels));err=abs(q-charge0)/charge0
 assert err<1e-8
 records.append({'lambda':float(time),'charge_shape_flux':q,'relative_error':err,'min_x_over_xh':float(x[:,i].min()/xh),'max_x_over_xh':float(x[:,i].max()/xh),'peak_shape':float(f[:,i].max())})

# Metric response remains finite even where background B=0.
alpha=1e-8
mass=b*C*E*cumulative_trapezoid(w*f*J,x=labels,axis=0,initial=0)
beta=b*C*cumulative_trapezoid(x*f*J/(E+S(x))**2,x=labels,axis=0,initial=0)
mass_error=float(np.max(abs(mass-mass[:,[0]])));assert mass_error<1e-8
deltaB=-2*alpha*mass/x;delta_beta=alpha*beta
assert np.max(abs(deltaB))<1e-6 and np.max(abs(delta_beta))<1e-6
probes=[]
for offset in [1e-2,1e-4,1e-6,1e-8]:
 for side in [-1,1]:
  xp=xh*(1+side*offset);bp=B(xp);sp=S(xp)
  qout_r=1/(E+sp)
  norm=2*E*qout_r-bp*qout_r*qout_r
  assert abs(norm-1)<1e-12 and np.isfinite(qout_r)
  probes.append({'relative_offset':side*offset,'B':float(bp),'outgoing_qr_over_Q':float(qout_r),'incoming_qr_over_Q':float((E+sp)/bp),'incoming_observer_boost':float(2*E*E/bp-1)})
np.savez_compressed(OUT/'profiles.npz',labels=labels,times=times,x=x,chi_shape=f,Jacobian=J,weight=w,mass_per_alpha=mass,beta_per_alpha=beta)
result={'all_passed':True,'b':b,'Y':Y,'C':C,'E':float(E),'xh':xh,'coordinates':'x=r/R,lambda=u sqrt(8piG rho0), outgoing null cuts','max_refinement_difference':diff,'transport_identity_relative_scale_error':identity,'charge_shape_flux0':charge0,'times':records,'horizon_probes':probes,'linear_metric':{'alpha':alpha,'chi':'X0*alpha*shape','max_abs_deltaB':float(np.max(abs(deltaB))),'max_abs_delta_beta':float(np.max(abs(delta_beta))),'mass_tail_per_alpha':float(mass[-1,-1]),'comoving_mass_error':mass_error},'scope':'linear packet and metric response in regular future EF chart, shifted horizon allowed; null-cut charge is current flux, not static proper-slice energy'}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_passed':True,'xh':xh,'final_time':records[-1],'max_refinement_difference':diff,'linear_metric':result['linear_metric']}))
