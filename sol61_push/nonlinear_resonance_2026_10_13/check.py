import json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
x=2/7;eps=1e-4;k=x/4;c3=.5*math.sqrt(eps*x)
u=(1+x-math.sqrt((1-x)**2+4*eps*x))/2;B=-c3/(1-u);Q=1+2*B*B;d=1-4*k*Q
omega0=math.sqrt((2*d+48*k*B*B-24*c3*B)*(2*d+16*k*B*B-8*c3*B))/2

def orbit(s,rtol):
 def H(X,Y):
  p=X*X+Y*Y;return d*p+4*k*p*p+2*c3*Q*X-4*c3*X*p
 def rhs(t,z):
  X,Y,S=z;p=X*X+Y*Y
  dx=d*Y+8*k*p*Y-4*c3*X*Y
  dy=-d*X-8*k*p*X-c3*Q+2*c3*(3*X*X+Y*Y)
  return [dx,dy,Y*dx/math.pi]
 def cross(t,z):return z[1]
 cross.direction=-1
 sol=solve_ivp(rhs,[0,3*2*math.pi/omega0],[B+s,0,0],events=cross,rtol=rtol,atol=rtol*1e-3,max_step=.08)
 assert sol.success and len(sol.t_events[0])>=3
 times=sol.t_events[0];states=sol.y_events[0];T=times[2]-times[1];I=states[2,2]-states[1,2]
 drift=max(abs(H(a,b)-H(B+s,0)) for a,b in sol.y[:2].T)
 assert drift<1e-11
 return dict(displacement=s,action=I,frequency=2*math.pi/T,shift_per_action=(2*math.pi/T-omega0)/I,energy_drift=drift)
rows=[orbit(s,2e-12) for s in [.001,.003,.01,.03]]
refine=orbit(.003,2e-13);assert abs(refine['shift_per_action']-rows[1]['shift_per_action'])<1e-6
# Independent zero-mixing limit H=d*p+4*k*p^2 gives omega=d+8*k*I exactly.
aa=d+24*k*B*B-12*c3*B;bb=d+8*k*B*B-4*c3*B
sx=(bb/aa)**.25;sy=1/sx;Cubic=16*k*B-4*c3
avg4=4*k*(3/8*(sx**4+sy**4)+.25*sx*sx*sy*sy)
avg3sq=Cubic**2*(5*sx**6+2*sx**4*sy**2+sx**2*sy**4)/16
coefficient=2*(avg4-3*avg3sq/(2*omega0))
assert abs(coefficient-rows[0]['shift_per_action'])<1e-7
assert abs(coefficient/(8*k)-1)<.002
old=json.loads((Path(__file__).parent/'INPUT_WIDTHS.json').read_text());gamma=sum(old['benchmark'][v] for v in ['nonradiative_width_s_inv','radiative_width_s_inv'])
hb=6.582119569e-16;delta=5;m=1e6;gamma_nat=hb*gamma
# Static real-amplitude response at optical standing-wave wavenumber.
q=omega0*math.sqrt(delta/m)
K=np.array([[q*q/2+x,2*c3],[2*c3,q*q/4+1-u]])
sus=np.linalg.solve(K,-np.array([2*B,1.]));assert np.linalg.norm(K@sus+np.array([2*B,1]))<1e-12
physical=[]
for eta in [1e-12,1e-9,1e-6]:
 dc=-gamma_nat/delta*math.sqrt(eta) # natural n=delta=1 after scaling, |Vg|~1 approximation
 dn=2*sus[0]*dc
 shift=delta*coefficient*eta
 C=shift/gamma_nat
 reduction=brentq(lambda r:r*(1+4*C*C*r*r)-1,0,1,xtol=1e-15)
 physical.append(dict(fixed_frequency_population_reduction=reduction,fixed_frequency_actual_action_fraction=eta*reduction,excited_action_over_daughter_density=eta,estimated_nonlinear_shift_Hz=shift/(2*math.pi*hb),
  shift_over_full_linewidth=shift/gamma_nat,
  fixed_unshifted_pump_intensity_multiplier=math.sqrt(1+4*(shift/gamma_nat)**2),
  static_fractional_density_modulation=float(dn),leading_static_bare_gap_shift_over_linewidth=abs(delta*x*dn/gamma_nat)))
# Independent nonlinear drive integration at the smallest tabulated detuning.
C=physical[0]['shift_over_full_linewidth']
def driven(t,y):
 a=y[0]+1j*y[1];da=-(.5+1j*C*abs(a)**2)*a-.5j
 return [da.real,da.imag]
sol=solve_ivp(driven,[0,80],[0,0],rtol=1e-10,atol=1e-12)
err=abs(sum(sol.y[:,-1]**2)-physical[0]['fixed_frequency_population_reduction'])
assert sol.success and err<1e-8
out=dict(nonlinear_drive_population_error=err,omega0=omega0,rows=rows,refinement=refine,nonlinear_coefficient=coefficient,physical=physical,
 half_linewidth_action_fraction=gamma_nat/(2*delta*coefficient),
 scope='Fixed-charge homogeneous classical Hamiltonian action-frequency shift; static linear spatial susceptibility; action extrapolation to tiny populations. Not full driven PDE or nonlinear kinetic solution.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
