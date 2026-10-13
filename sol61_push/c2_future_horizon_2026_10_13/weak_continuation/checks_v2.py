"""Same-law de Sitter weak-phase nonuniqueness control, not physical formation."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import quad

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
OUT=Path(ap.parse_args().output);checks=[]
def eq(name,e):
 e=s.simplify(e);assert e==0,(name,e)
 checks.append({'name':name,'passed':True})
t,x,y,z=s.symbols('t x y z',real=True)
H,Q,c,G,a=s.symbols('H Q c G a',positive=True)
A=s.exp(H*t);co=[t,x,y,z]
g=s.diag(1,-A**2,-A**2,-A**2);inv=g.inv();gam={}
for i in range(4):
 for j in range(4):
  for k in range(4):
   v=s.simplify(sum(inv[i,l]*(s.diff(g[l,k],co[j])+s.diff(g[l,j],co[k])-s.diff(g[j,k],co[l])) for l in range(4))/2)
   if v!=0:gam[i,j,k]=v
def C(i,j,k):return gam.get((i,j,k),s.S.Zero)
def Ric(i,j):return s.simplify(sum(s.diff(C(k,i,j),co[k])-s.diff(C(k,i,k),co[j])+sum(C(k,k,l)*C(l,i,j)-C(k,j,l)*C(l,i,k) for l in range(4)) for k in range(4)))
ric=s.diag(*[Ric(i,i) for i in range(4)])
scalar=s.simplify(s.trace(inv*ric));gmix=s.simplify(inv*(ric-g*scalar/2))
for i in range(4):eq('deSitter_Einstein_'+str(i),gmix[i,i]-3*H**2)
rho0=3*H**2/(8*s.pi*G)
eq('same_offset_Einstein_relation',3*H**2-8*s.pi*G*rho0)
omega=s.sqrt(Q**2+c**2/A**2)
radius=s.sqrt(x*x+y*y+z*z)
grad=s.Matrix([s.diff(-c*radius,v) for v in [x,y,z]])
eq('inside_spatial_gradient_norm',(grad.T*grad)[0]-c*c)
Xin=(omega**2-c*c/A**2)/2;Xout=Q**2/2;X0=Q**2/2
eq('inside_X0',Xin-X0);eq('outside_X0',Xout-X0)
for name,X in [('inside',Xin),('outside',Xout)]:
 px=a*(X-X0);P=-rho0+a*(X-X0)**2/2
 eq(name+'_zero_shift_current_coefficient',px)
 eq(name+'_zero_canonical_momentum',A**3*px*(omega if name=='inside' else Q))
 eq(name+'_vacuum_stress_offset',-P-rho0)
eq('positive_front_speed_rationalization',A*(omega-Q)/c-c/(A*(omega+Q)))
eq('upper_test_viscosity_violation',omega-Q-c*c/(A*A*(omega+Q)))
r,D=s.symbols('r D',positive=True)
Rb=D/c
phase_norm=4*s.pi*s.integrate((D-c*r)**2*r*r,(r,0,Rb))
grad_norm=4*s.pi*s.integrate(c*c*r*r,(r,0,Rb))
velocity_norm=4*s.pi*s.integrate((omega-Q)**2*r*r,(r,0,Rb))
eq('relative_phase_L2_comoving',phase_norm-2*s.pi*D**5/(15*c**3))
eq('relative_gradient_L2_comoving',grad_norm-4*s.pi*D**3/(3*c))
eq('relative_velocity_L2_comoving',velocity_norm-4*s.pi*(omega-Q)**2*D**3/(3*c**3))
proof_obligation={'name':'weak_distributional_argument','status':'analytical proof and independent audit required; not a machine-executed identity','scope':'theta continuous/Lipschitz; first weak derivatives bounded; X0 almost everywhere makes flux0 and stressrho0g as equivalence classes; formal proof in PROOF.txt'}

records=[]
for amp in [.1,.5,1.]:
 cases=[]
 for time in [1e-6,1e-4,.01,.1,.25]:
  def integrand(t):
   v=amp*amp*np.exp(-2*t)
   return v/(np.sqrt(1+v)+1)
  base=quad(integrand,0,time,epsabs=1e-12,epsrel=1e-10)[0]
  tight=quad(integrand,0,time,epsabs=1e-14,epsrel=1e-12)[0]
  assert abs(base-tight)<1e-11 and tight>0
  av=np.exp(time);om=np.sqrt(1+amp*amp/(av*av));speed=av*integrand(time)/amp
  assert 0<speed<1
  rb=tight/amp
  norms={'phase_L2_squared_proper':av**3*2*np.pi*tight**5/(15*amp**3),'physical_gradient_L2_squared_proper':av*4*np.pi*tight**3/(3*amp),'relative_velocity_L2_squared_proper':av**3*4*np.pi*integrand(time)**2*tight**3/(3*amp**3)}
  H1=np.sqrt(norms['phase_L2_squared_proper']+norms['physical_gradient_L2_squared_proper'])
  L2v=np.sqrt(norms['relative_velocity_L2_squared_proper'])
  if time==1e-6:assert H1<1e-7 and L2v<1e-7
  probes=[]
  for fraction in [.25,.75,1.25,2.]:
   wt=om if fraction<1 else 1.
   pr=-amp if fraction<1 else 0.
   value=(wt*wt-pr*pr/(av*av))/2
   assert abs(value-.5)<1e-12
   probes.append({'radius_over_Rb':fraction,'X':float(value),'shift_current':0,'canonical_momentum':0})
  assert integrand(time)>0
  cases.append({'t':time,'D':float(tight),'radius_comoving':float(rb),'proper_front_speed':float(speed),'quadrature_difference':abs(base-tight),'norms':norms,'relative_H1_proper':float(H1),'relative_velocity_L2_proper':float(L2v),'upper_test_residual':float(integrand(time)),'gradient_sup_comoving':amp,'probes':probes})
 records.append({'gradient_amplitude_over_Q':amp,'times':cases})
result={'all_passed':True,'exact_check_count':len(checks),'checks':checks,'separate_proof_obligation':proof_obligation,'diagnostic_units':{'H':1,'Q':1,'X0':.5,'rho0_relation':'3H²/(8piG); no additional cosmological term'},'numeric_controls':records,'claim':'multiple Lipschitz/a.e-X0 divergence-form weak phases share smooth phase/canonical initial data and relative/local H1xL2 trace; not strongC1 or classical/viscosity nonuniqueness','nonclaims':['No predicted physical bubble creation','Not a static-core postcaustic continuation theorem','No physical UV/quantum completion']}
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_passed':True,'exact_check_count':len(checks),'amplitudes':[r['gradient_amplitude_over_Q'] for r in records],'max_initial_H1':max(r['times'][0]['relative_H1_proper'] for r in records)}))
