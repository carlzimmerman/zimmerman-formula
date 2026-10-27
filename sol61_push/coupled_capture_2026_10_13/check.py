import json,math,cmath,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
T=10;sigma=.5

def controls(t,C,K,J):
 if t>=T:R,Rp,Rpp=1.,0.,0.
 else:
  s=t/T;R=10*s**3-15*s**4+6*s**5
  Rp=(30*s*s-60*s**3+30*s**4)/T
  Rpp=(60*s-180*s*s+120*s**3)/T**2
 F=Rp+.5*R+1j*sigma*R;P=cmath.sqrt(F)
 Pp=(Rpp+(.5+1j*sigma)*Rp)/(2*P) if t>0 else math.sqrt(30/T**3)
 D=(sigma-C*R*R)/2;Z=-1j*R
 E=Pp+(K/2+1j*D)*P+1j*J*Z*P.conjugate()
 return R,P,Pp,D,E

def run(C,K,J,imbalance):
 calls=[0]
 def rhs(t,y):
  calls[0]+=1
  if calls[0]>150000:raise RuntimeError('evaluation cap')
  ep,eq,ez=[complex(*y[i:i+2]) for i in [0,2,4]]
  R,P,Pp,D,E=controls(t,C,K,J);Z=-1j*R
  dp=-(K/2+1j*D)*ep-1j*J*(Z*eq.conjugate()+ez*P.conjugate()+ez*eq.conjugate())+imbalance*E
  dq=-(K/2+1j*D)*eq-1j*J*(Z*ep.conjugate()+ez*P.conjugate()+ez*ep.conjugate())-imbalance*E
  dz=-(.5+1j*sigma)*ez-1j*C*(abs(ez)**2-2*R*ez.imag)*(Z+ez)-1j*(P*(ep+eq)+ep*eq)
  return [v for z in [dp,dq,dz] for v in [z.real,z.imag]]
 def lost(t,y):return .1-max(math.hypot(*y[i:i+2]) for i in [0,2,4])
 lost.terminal=True;lost.direction=-1
 try:sol=solve_ivp(rhs,[0,20],np.zeros(6),method='Radau',rtol=2e-8,atol=1e-11,max_step=.1,events=lost)
 except RuntimeError:
  return dict(status='inconclusive-evaluation-cap',C=C,K=K,J=J,imbalance=imbalance)
 assert sol.success
 errors=np.sqrt(sol.y[::2]**2+sol.y[1::2]**2)
 R=controls(sol.t[-1],C,K,J)[0]
 return dict(status='completed',C=C,K=K,J=J,imbalance=imbalance,reached_end=bool(sol.t[-1]>=20),
  stop_time=float(sol.t[-1]),max_optical_amplitude_error=float(np.max(errors[:2])),max_matter_amplitude_error=float(max(errors[2])),
  terminal_matter_population=float(sol.y[4,-1]**2+(sol.y[5,-1]-R)**2),rhs_evaluations=sol.nfev)

p=Path(__file__).parent;nr=json.loads((p/'INPUT_RESONANCE.json').read_text());w=json.loads((p/'INPUT_WIDTHS.json').read_text());ref=next(r for r in w['rows'] if r['epsilon']==1e-4 and r['x']==2/7)
gamma=w['benchmark']['nonradiative_width_s_inv']+w['benchmark']['radiative_width_s_inv'];hb=6.582119569e-16
m=1e6;delta=5.;M=2000005.;n=2/7*delta*m*m/1e-6;u=(1+2/7-math.sqrt((1-2/7)**2+4e-4*2/7))/2
Vg=math.sqrt(ref['photon_rate_correction']*((1-u)/ref['omega_over_delta'])**4)
g=n/(2*m*(10*M)**3)*Vg;wp=delta*ref['omega_over_delta']/2
rows=[];stability=[]
for r in nr['physical']:
 eta=r['excited_action_over_daughter_density'];C=r['shift_over_full_linewidth'];J=g*wp*math.sqrt(eta*n)/math.sqrt(2*M)/(hb*gamma)
 for kap in [299792458/.01,1e6]:
  K=kap/gamma
  # Maximum antisymmetric discriminant over the entire amplitude ramp, analytic quadratic.
  v=min(1,max(0,(2*J*J+C*sigma)/(C*C)))
  discr=J*J*v-(sigma-C*v)**2/4
  maxgrowth=-K/2+math.sqrt(max(discr,0))
  stability.append(dict(eta=eta,photon_loss_s_inv=kap,C=C,K=K,J=J,max_antisymmetric_growth=maxgrowth,critical_R=math.sqrt(v)))
  if eta<=1e-9:
   row=run(C,K,J,1e-6);row.update(eta=eta,photon_loss_s_inv=kap);rows.append(row);print(row,flush=True)
# Orthogonal conservation identity and direct-vs-error RHS at a nonzero perturbation.
C=26.3;K=6.;J=.7;t=3.;R,P,Pp,D,E=controls(t,C,K,J);ep=1e-4+2e-4j;eq=-2e-4+1e-4j;ez=3e-5-2e-5j
pp=P+ep;qq=P+eq;z=-1j*R+ez
Dp=-(K/2+1j*D)*pp-1j*J*z*qq.conjugate()+E
Dq=-(K/2+1j*D)*qq-1j*J*z*pp.conjugate()+E
Dz=-(.5+1j*(sigma-C*R*R+C*abs(z)**2))*z-1j*pp*qq
weighted=2*(pp.conjugate()*Dp+qq.conjugate()*Dq+2*J*z.conjugate()*Dz).real
balance=2*(E*(pp.conjugate()+qq.conjugate())).real-K*(abs(pp)**2+abs(qq)**2)-2*J*abs(z)**2
assert abs(weighted-balance)<1e-12
transformed=-(K/2+1j*D)*ep-1j*J*(-1j*R*eq.conjugate()+ez*P.conjugate()+ez*eq.conjugate())
assert abs(Dp-Pp-transformed)<1e-12
# Quantum-seeded resonant matter-pair amplifier, with equal number loss kappa_p.
pair_checks=[]
for loss in [0,1,1.99,2.01,3,10]:
 L=np.array([[-loss,2,0],[2,-loss,1],[0,0,0.]])
 exact=expm(3*L)@np.array([0.,0.,1.])
 sol=solve_ivp(lambda t,y:[-loss*y[0]+2*y[1],2*y[0]-loss*y[1]+1],[0,3],[0,0],rtol=1e-11,atol=1e-12)
 error=float(np.linalg.norm(sol.y[:,-1]-exact[:2]));assert error<1e-7
 if loss==0:assert abs(exact[0]-math.sinh(3)**2)<1e-10
 pair_checks.append(dict(number_loss_over_gain=loss,pair_occupation_at_gain_time_3=float(exact[0]),ode_error=error,
  stationary_occupation=2/(loss*loss-4) if loss>2 else None))
A=abs(ref['amplitude_dimensionless']);vg=ref['group_velocity_dimensionless']*math.sqrt(delta/m)*299792458.
pair_physical=[]
for eta in [1e-12,1e-9,1e-6]:
 mu=delta*A*math.sqrt(eta)/hb
 pair_physical.append(dict(eta=eta,pair_gain_s_inv=mu,maximum_escape_length_m=vg/(2*mu),
  one_cm_number_growth_s_inv=2*mu-vg/.01))
out=dict(matter_pair_checks=pair_checks,matter_pair_physical=pair_physical,phonon_group_velocity_m_s=vg,cases=rows,antisymmetric_scan=stability,balance_residual=abs(weighted-balance),
 scope='Combined nonlinear three-mode feedforward capture with fixed optical resonance and loss. No spatial continuum, confinement or full effective-action normal form.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
