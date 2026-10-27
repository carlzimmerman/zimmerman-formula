import argparse,json
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);args=pa.parse_args()
eta=.005;B=.125;A=.005;fb=1/6.364;fc=1-fb;ell=.0004404221297174536;t0=.012074272908402984;H0=67.4*1000/3.085677581491367e22*365.25*86400*1e9;Om=.315;Ni=-np.log(1101);Nf=-np.log(11)
G=6.67430e-11;mpc=3.085677581491367e22;Ms=1.98847e30;rhom=.315*3*(67.4*1000/mpc)**2/(8*np.pi*G)*mpc**3/Ms
quad={}
def potential(p,n=32,nonlinear=True):
 if not nonlinear:return p*p/4,p/2
 if n not in quad:
  x,w=roots_legendre(n);quad[n]=(np.sin((x+1)*np.pi/4),w/2)
 s,w=quad[n];v=np.minimum(abs(p)*s,1-1e-12)
 return float(np.sum(w*(-v-np.log1p(-v)))),float(np.sum(w*p*s*s/(1-v)))
def bg(N,k):
 a=np.exp(N);H=H0*np.sqrt(Om)*a**(-1.5)*t0;J=1.5*H*H
 return H,fb*J,fc*J,k*ell/a,np.exp(3*(N-Ni))
def energywork(N,y,k,nl):
 db,vb,dc,vc,p,vp,c,vs=y[:8];H,Jb,Jc,q,w=bg(N,k);c=max(c,.01);E=Jc*dc-q*p;W,_=potential(p,nonlinear=nl)
 T=w*(Jb*(H*vb)**2+Jc*(H*vc)**2)/(4*q*q);Ug=-w*(Jb*db+Jc*dc)**2/(4*q*q);Tf=w*(eta*(H*vp)**2/4+B*(H*vs)**2/2);UW=w*W;Uc=w*A*(c-1)**2/2;Um=w*E*E/(4*c)
 en=T+Ug+Tf+UW+Uc+Um;work=-2*T-Ug-3*Tf+3*(UW+Uc+Um)+w*E*(-3*Jc*dc+q*p)/(2*c)
 return en,work,abs(T)+abs(Ug)+abs(Tf)+abs(UW)+abs(Uc)+abs(Um)
def initial(k,amp,state):
 H,Jb,Jc,q,w=bg(Ni,k)
 def chi(p):
  e=Jc*amp-q*p
  return brentq(lambda c:c*c*(c-1)-e*e/(4*A),1,1+(e*e/(4*A))**(1/3)+1e-8)
 p=0;c=1
 if state=='stationary':
  def f(p):return 2*potential(p)[1]-q*(Jc*amp-q*p)/chi(p)
  if f(.95)<0:return None
  p=brentq(f,0,.95,xtol=1e-13);c=chi(p)
 return [amp,amp,amp,amp,p,0,c,0,0]
def calc(M,amp,state,nl,tol):
 k=(4*np.pi*rhom/(3*M))**(1/3);y0=initial(k,amp,state)
 if y0 is None:return dict(M=M,amp=amp,state=state,nonlinear=nl,status='initial_p_outside_test_domain')
 def rhs(N,y):
  db,vb,dc,vc,p,vp,c,vs,work=y;H,Jb,Jc,q,w=bg(N,k);c=max(c,.01);E=Jc*dc-q*p;grav=Jb*db+Jc*dc;W,Wp=potential(p,nonlinear=nl)
  return [vb,-.5*vb+grav/(H*H),vc,-.5*vc+(grav-q*q*E/c)/(H*H),vp,-1.5*vp+(-2*Wp+q*E/c)/(eta*H*H),vs,-1.5*vs+(-A*(c-1)+E*E/(4*c*c))/(B*H*H),energywork(N,y,k,nl)[1]]
 def density(N,y):return .3-max(abs(y[0]),abs(y[2]))
 def polar(N,y):return .95-abs(y[4])
 def phase(N,y):return y[6]-.05
 for e in [density,polar,phase]:e.terminal=True;e.direction=-1
 sol=solve_ivp(rhs,(Ni,Nf),y0,method='DOP853',rtol=tol,atol=tol*1e-3,events=[density,polar,phase],dense_output=True)
 assert sol.success,sol.message
 ns=np.linspace(Ni,sol.t[-1],1001);ys=sol.sol(ns);energies=np.array([energywork(n,y,k,nl) for n,y in zip(ns,ys.T)]);initialE=energywork(Ni,y0,k,nl)[0];err=np.max(abs(energies[:,0]-initialE-ys[8]))/max(np.max(energies[:,2]),1e-30)
 stop='endpoint'
 for name,e in zip(['density_limit','polarization_limit','phase_limit'],sol.t_events):
  if len(e):stop=name
 return dict(M=M,amp=amp,state=state,nonlinear=nl,status=stop,z_end=float(np.exp(-sol.t[-1])-1),delta_b=float(ys[0,-1]),delta_c=float(ys[2,-1]),Pmax=float(max(abs(ys[4]))),chi_min=float(min(ys[6])),chi_max=float(max(ys[6])),initial_P=y0[4],initial_chi=y0[6],energy_work_error=float(err),nfev=sol.nfev)
def tracking_initial(k,amp):
 y=initial(k,amp,'stationary');H,Jb,Jc,q,w=bg(Ni,k);p=y[4];c=y[6];E=Jc*amp-q*p
 # Along the specified initial delta_N=delta: d(Jc delta)/dN=-2 Jc delta.
 # Differentiate equilibrium equations with unknown p_N and chi_N.
 step=1e-5;Wpp=(potential(p+step)[1]-potential(p-step)[1])/(2*step)
 mat=np.array([[2*Wpp+q*q/c,q*E/(c*c)],[q*E/(2*c*c),A+E*E/(2*c**3)]])
 explicitE=-2*Jc*amp+q*p
 # F1=2W'-qE/c; F2=A(c-1)-E²/(4c²).
 rhs=np.array([-q*E/c+q*explicitE/c,E*explicitE/(2*c*c)])
 v=np.linalg.solve(mat,rhs);y[5]=float(v[0]);y[7]=float(v[1]);return y
old_initial=initial
def initial(k,amp,state):
 return tracking_initial(k,amp) if state=='tracking' else old_initial(k,amp,state)
Nf=0.
rows=[]
for k in [1]:
 M=4*np.pi*rhom/(3*k**3)
 for state in ['tracking']:
  r=calc(M,1e-6,state,True,1e-10);r['k']=k;r['retained_total']=(fb*r['delta_b']+fc*r['delta_c'])/(1101e-6);rows.append(r)
checks=[dict(name='large_scale_work',passed=max(x['energy_work_error'] for x in rows)<1e-5,value=max(x['energy_work_error'] for x in rows)),dict(name='all_reach_present',passed=all(x['status']=='endpoint' for x in rows),value=len(rows))]
Path(args.output).write_text(json.dumps(dict(checks=checks,rows=rows),indent=2)+'\n')
