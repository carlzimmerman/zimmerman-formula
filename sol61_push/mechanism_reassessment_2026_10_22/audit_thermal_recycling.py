"""Orthogonal threshold, detailed-balance, thermodynamics and fast-limit checks."""
import json,sys
from pathlib import Path
import numpy as np
from scipy.special import kve
from scipy.integrate import solve_ivp,cumulative_trapezoid
from scipy.interpolate import PchipInterpolator
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
# Load the declared reusable prefix, without executing its run loop.
ns={'__file__':str(P/'thermal_recycling_evolution.py'),'__name__':'kinetic_audit_library'}
exec(compile((P/'thermal_recycling_evolution.py').read_text().split('\ncases={}')[0],str(P/'thermal_recycling_evolution.py'),'exec'),ns)
m,M,g,lam=[ns[x] for x in ['m','M','g','lam']];Hs=ns['Hs'];state=ns['state'];rate=ns['rate'];species=ns['species'];checks={};detail={}
# Exact quantum statistical identities at conserved external energies.
for alpha in [.1,.5,1.]:
 T=.0005
 f=lambda E,mu:1/np.expm1((E-mu)/T)
 fp=f(M,alpha*T);fx=f(M,2*alpha*T)
 pair_ratio=fp**2*(1+fx)**2/(fx**2*(1+fp)**2)
 incoming=f(1.5*m,alpha*T);outgoing=f(3*m,alpha*T)
 ratio42=outgoing**2*(1+incoming)**4/(incoming**4*(1+outgoing)**2)
 parent=f(M,2*alpha*T);daughter=f(M/2,alpha*T)
 decay_ratio=daughter**2*(1+parent)/(parent*(1+daughter)**2)
 checks['Bose_detailed_balance_'+str(alpha)]=max(abs(pair_ratio/np.exp(-2*alpha)-1),abs(ratio42/np.exp(-2*alpha)-1),abs(decay_ratio-1))<1e-12
# Thermodynamic Jacobian by independent centered differences.
errs=[]
for T,eta in [(m/2,-2),(m/10,-3),(m/1000,-4)]:
 n,nx,W,U,pr,J=state(T,eta)
 h=1e-5
 for col in [0,1]:
  plus=state(T*np.exp(h) if col==0 else T,eta+h if col==1 else eta)
  minus=state(T*np.exp(-h) if col==0 else T,eta-h if col==1 else eta)
  fd=(np.array(plus[2:4])-np.array(minus[2:4]))/(2*h)
  errs.append(float(np.max(abs(fd/J[:,col]-1))))
checks['thermodynamic_jacobian']=max(errs)<2e-6;detail['jacobian_max_relative_error']=max(errs)
# Independent entropy conservation/production from stored trajectories.
for name in ['full','no_loss']:
 h=np.genfromtxt(P/'thermal_recycling_evolution_run'/(name+'.csv'),delimiter=',',names=True)
 ent=[];rho=[];pressure=[]
 for T,eta in zip(h['T'],h['eta']):
  n,nx,W,U,pr,J=state(T,eta);alpha=eta+m/T
  ent.append((m*W+U+pr)/T-alpha*W);rho.append(m*W+U);pressure.append(pr)
 N=h['N'];comS=np.array(ent)*np.exp(3*N)
 if name=='no_loss':checks['no_loss_entropy_conservation']=np.max(abs(comS/comS[0]-1))<2e-5
 else:checks['nonnegative_entropy_production']=np.min(np.diff(comS))/comS[0]>-1e-8
 # Integrated continuity, with the expected finite quadrature error on stored output.
 er=np.array(rho)*np.exp(3*N)+cumulative_trapezoid(3*np.array(pressure)*np.exp(3*N),N,initial=0)
 checks[name+'_integrated_energy']=np.max(abs(er/er[0]-1))<1e-4
 detail[name+'_integrated_energy_error']=float(np.max(abs(er/er[0]-1)))
# Independent finite-rate decay system, common MB temperature, before the fast constraint.
ref=np.genfromtxt(P/'thermal_recycling_evolution_run/fine.csv',delimiter=',',names=True)
refT=float(PchipInterpolator(ref['N'],ref['T'])(1));refW=float(PchipInterpolator(ref['N'],ref['nPhi']+2*ref['nX'])(1))
T0=m/2;n0,nx0,W0,U0,pr0,J0=state(T0,-2)
finite=[]
for fast in [100.,1000.,10000.]:
 def rhs(N,y):
  n,nx,T=np.exp(y);H=Hs*np.exp(-2*N)
  nq=m*m*T/np.pi**2*kve(2,m/T)*np.exp(-m/T);xq=M*M*T/np.pi**2*kve(2,M/T)*np.exp(-M/T)
  # Total charge-balanced densities. Inverse reactions included separately.
  C,sv=rate(T)
  decay=fast*(nx-xq*(n/nq)**2)
  ann=.5*sv/H*(nx*nx-(xq/nq)**2*n*n)
  loss=C/H*(n**4-nq*nq*n*n)
  cn=2*decay+ann-loss;cx=-decay-ann
  ep=m*kve(1,m/T)/kve(2,m/T)+3*T;ex=M*kve(1,M/T)/kve(2,M/T)+3*T
  step=T*1e-5
  e=lambda ma,temp:ma*kve(1,ma/temp)/kve(2,ma/temp)+3*temp
  dp=(e(m,T+step)-e(m,T-step))/(2*step);dx=(e(M,T+step)-e(M,T-step))/(2*step)
  dT=(-3*T*(n+nx)-ep*cn-ex*cx)/(n*dp+nx*dx)
  return [-3+cn/n,-3+cx/nx,dT/T]
 sol=solve_ivp(rhs,(0,1),np.log([n0,nx0,T0]),method='Radau',rtol=2e-8,atol=1e-10,max_step=.03)
 if not sol.success:raise RuntimeError(sol.message)
 n,nx,T=np.exp(sol.y[:,-1]);finite.append({'Gamma_decay_over_H':fast,'relative_T_error':abs(T/refT-1),'relative_W_error':abs((n+2*nx)/refW-1)})
checks['finite_decay_converges']=finite[-1]['relative_W_error']<finite[0]['relative_W_error'] and finite[-1]['relative_T_error']<finite[0]['relative_T_error']
checks['fast_limit_agreement']=max(finite[-1]['relative_T_error'],finite[-1]['relative_W_error'])<.002
detail['finite_decay']=finite
z=np.exp(-2);detail['fixed_T_mu_Bose_forward_contact_bound']=(1-z)**-6;detail['fixed_T_mu_Bose_forward_pair_bound']=(1-z*z)**-2*(1-z)**-2
out={'checks':{k:bool(v) for k,v in checks.items()},'all_pass':bool(all(checks.values())),'details':detail,'scope':'Audit of conditional kinetic closure and reaction bookkeeping. Does not validate source thermalization or supply missing off-shell cubic collision terms.'};(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
