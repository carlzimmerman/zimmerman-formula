import json,math,sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

def rhs(y,g,E):
 a,c,b=y[0]+1j*y[1],y[2]+1j*y[3],y[4]+1j*y[5]
 z=[-.5*a-1j*b*c.conjugate()+E,-.5*c-1j*b*a.conjugate()+E,-g/2*b-1j*a*c]
 return np.array([v for w in z for v in [w.real,w.imag]])
def state(a,c,g): return np.array([a,0,c,0,0,-2*a*c/g])
def jac(y,g,E):
 # Exact Jacobian for this quadratic vector field via symmetric differences.
 h=1e-4
 return np.column_stack([(rhs(y+h*np.eye(6)[j],g,E)-rhs(y-h*np.eye(6)[j],g,E))/(2*h) for j in range(6)])
rows=[]
for g in [.1,1,10]:
 for ratio in [.1,.5,.9,1.1,2,5]:
  E=ratio*math.sqrt(g)/2
  A=brentq(lambda a:.5*a+2*a**3/g-E,0,2*E)
  y=state(A,A,g);J=jac(y,g,E);eig=np.linalg.eigvals(J)
  assert np.linalg.norm(rhs(y,g,E))<1e-10
  # Antisymmetric real optical perturbation has an independently derived eigenvalue.
  v=np.array([1,0,-1,0,0,0]);growth=-.5+2*A*A/g
  assert np.linalg.norm(J@v-growth*v)<1e-9
  assert (max(eig.real)>0)==(ratio>1)
  row=dict(gamma_over_kappa=g,pump_over_threshold=ratio,symmetric_amplitude=A,
   symmetric_max_growth=float(max(eig.real)),analytic_antisymmetric_growth=growth)
  if ratio>1:
   aa=E+math.sqrt(E*E-g/4);cc=E-math.sqrt(E*E-g/4)
   ya=state(aa,cc,g);ev=np.linalg.eigvals(jac(ya,g,E))
   assert np.linalg.norm(rhs(ya,g,E))<1e-10 and max(ev.real)<0
   row.update(asymmetric_amplitudes=[aa,cc],asymmetric_max_growth=float(max(ev.real)),matter_occupation=ya[5]**2)
  rows.append(row)
# Actual nonlinear evolution selects the symmetry-broken branch after a seed.
g=1;E=1;A=brentq(lambda a:.5*a+2*a**3-E,0,2)
y=state(A,A,g);y[0]+=1e-4;y[2]-=1e-4
sol=solve_ivp(lambda t,y:rhs(y,g,E),[0,150],y,rtol=1e-10,atol=1e-12)
target=state(E+math.sqrt(E*E-.25),E-math.sqrt(E*E-.25),g)
error=float(np.linalg.norm(sol.y[:,-1]-target));assert sol.success and error<1e-7
# Charge-weighted energy balance along actual trajectory.
res=[]
for y in sol.y.T[::max(1,len(sol.t)//30)]:
 dy=rhs(y,g,E);weights=np.array([1,1,1,1,2,2])
 lhs=2*np.dot(weights*y,dy)
 balance=2*E*(y[0]+y[2])-sum(y[:4]**2)-2*g*sum(y[4:]**2)
 res.append(abs(lhs-balance))
assert max(res)<1e-12
old=json.loads((Path(__file__).parent/'INPUT_WIDTHS.json').read_text())
r=next(v for v in old['rows'] if v['epsilon']==1e-4 and v['x']==2/7)
m=1e6;M=2000005.;delta=5.;x=2/7;eps=1e-4;n=x*delta*m*m/1e-6
u=(1+x-math.sqrt((1-x)**2+4*eps*x))/2
Vg=math.sqrt(r['photon_rate_correction']*((1-u)/r['omega_over_delta'])**4)
geff=n/(2*m*(10*M)**3)*Vg;wp=delta*r['omega_over_delta']/2
hb=6.582119569e-16;hc=1.973269804e-7;eV=1.602176634e-19;c=299792458.
gamma=old['benchmark']['nonradiative_width_s_inv']+old['benchmark']['radiative_width_s_inv']
physical=[]
for kap in [c/.01,1e6,1,1e-3]:
 uc=(kap*hb)*(gamma*hb)*M/(2*geff**2*wp)
 nsc=(kap*hb)**2*M/(2*geff**2*wp**2)
 physical.append(dict(photon_number_loss_s_inv=kap,per_beam_intracavity_threshold_W_m2=uc*eV/hc**3*c,
  critical_excitation_fraction=nsc/n,qualification='Prescribed mode loss, not an engineered cavity or free-space propagation solution.'))
out=dict(physical_thresholds=physical,rows=rows,nonlinear_final_error=error,max_energy_balance_residual=max(res),
 scope='Resonant equal-drive three-mode truncation with photon loss kappa=1 and coupling h=1. No spatial continuum, confinement or laboratory cavity derived.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print('18 branch comparisons; nonlinear error',error,'energy residual',max(res))
