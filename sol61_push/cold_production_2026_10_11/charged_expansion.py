"""Check exact FLRW identities and a charge-energy comparison bound."""
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
p=Path(__file__).parent
m=1.;u=.1;Delta=4*u*u;M=math.sqrt(4+Delta);g=.03;H0=.003
checks=[]
def check(n,b,v=None):checks.append(dict(name=n,passed=bool(b),value=v))
def background(t):
    a=math.sqrt(1+2*H0*t);H=H0/a**2;Hd=-2*H*H
    return a,H,Hd

def rhs(t,y):
    phi,chi,dp,dc=y;a,H,Hd=background(t)
    vp=m*m*phi+2*g*chi*phi.conjugate()+2*g*g/Delta*abs(phi)**2*phi
    vc=M*M*chi+g*phi**2
    return np.array([dp,dc,-3*H*dp-vp,-3*H*dc-vc])
y0=np.array([.02+0j,1+0j,-1j*m*.02,-1j*M],complex)
sol=solve_ivp(rhs,(0,1000),y0,method='DOP853',rtol=2e-10,atol=2e-12,t_eval=np.linspace(0,1000,2001),max_step=.2)
Es=[];Qs=[];etas=[];errors=[];bounds=[];state=[]
for t,y in zip(sol.t,sol.y.T):
    phi,chi,dp,dc=y;a,H,Hd=background(t);vol=a**3
    z=math.sqrt(Delta)*chi;w=g/math.sqrt(Delta)*phi**2;U=abs(z+w)**2
    kinetic=abs(dp)**2+abs(dc)**2;V=m*m*abs(phi)**2+4*m*m*abs(chi)**2+U
    E=vol*(kinetic+V);Q=vol*(1j*(phi.conjugate()*dp-dp.conjugate()*phi)+2j*(chi.conjugate()*dc-dc.conjugate()*chi)).real
    S=vol*(phi.conjugate()*dp+chi.conjugate()*dc).real
    pressure=vol*(kinetic-V);R=vol*(w.conjugate()*(z+w)).real
    dy=rhs(t,y)
    Sd=3*H*S+vol*(kinetic+(phi.conjugate()*dy[2]+chi.conjugate()*dy[3]).real)
    errors.append(abs(pressure-Sd-R)/(1+E))
    Es.append(E);Qs.append(Q);etas.append(1-m*Q/E);state.append((S,pressure,R,H,Hd))
E0=Es[0];Q0=Qs[0];logB0=math.log(E0/(m*Q0))+math.log1p(3*H0/m)-math.log1p(-3*H0/m)
for t,E in zip(sol.t,Es):
    a,H,_=background(t)
    bounds.append(m*Q0*math.exp(logB0+.75*u*u/(1-3*H0/m)*math.log(a)))
check('integration completed',sol.success)
check('comoving charge',max(abs(np.array(Qs)/Q0-1))<1e-7,float(max(abs(np.array(Qs)/Q0-1))))
check('virial identity',max(errors)<1e-12,max(errors))
check('positive charge excess',min(etas)>=-1e-8,min(etas))
check('energy comparison bound',max(np.array(Es)-bounds)<1e-7,float(max(np.array(Es)-bounds)))
for i,(E,(S,PV,R,H,Hd)) in enumerate(zip(Es,state)):
    # Exact E'=-3H PV and S'=PV-R imply F'=3H'S-3HR.
    Fdot=3*Hd*S-3*H*R
    upper=(3*abs(Hd)/m+.75*H*u*u)*E
    if Fdot>upper+1e-10:check('differential bound point '+str(i),False)
# Physical benchmark is a comparison-bound evaluation, not this ODE parameter set.
up=.001;hp=1.378199482812902e-11;ratio=1000001.;eta0=up*up/(math.sqrt(1+up*up)*(1+math.sqrt(1+up*up)))
log_energy_ratio=-math.log1p(-eta0)+math.log1p(3*hp)-math.log1p(-3*hp)+.75*up*up/(1-3*hp)*math.log(ratio)
eta_bound=-math.expm1(-log_energy_ratio)
out=dict(checks=checks,all_pass=all(c['passed'] for c in checks),ode_parameters=dict(m=m,u=u,g=g,H0=H0,end_time=1000,seed_phi=.02),ode_final_eta=etas[-1],ode_max_eta=max(etas),benchmark=dict(initial_eta=eta0,H0_over_m=hp,scale_factor_ratio=ratio,eta_bound=eta_bound,energy_over_mQ_bound=math.exp(log_energy_ratio),averaged_pressure_bulk_bound=2*eta_bound/3+math.sqrt(2*eta_bound*(eta_bound+up*up))),non_claims=['Homogeneous ODE is a check, not cosmological production simulation','General theorem requires smooth solutions and monotonically decreasing nonnegative H','No quantum or galaxy-law derivation'])
(p/'charged_expansion_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
