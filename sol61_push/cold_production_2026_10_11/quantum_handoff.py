"""Finite-box Gaussian vacuum evolution and a stated Wigner handoff prescription."""
import json,math,itertools
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
m=params['m_eV'];u=params['u'];eps=params['epsilon'];R=params['M_eV']/m;kappa=params['kappa'];dq=.4
pairs=[]
for idx in itertools.product(range(-5,6),repeat=3):
    if idx>(0,0,0) and 0<sum((dq*j)**2 for j in idx)<=4:pairs.append(idx)
q2=np.sum((dq*np.array(pairs))**2,axis=1);K=len(pairs)
Ns=params['rho_source_eV4']/params['M_eV']*(2*math.pi/(dq*m*u))**3
w=np.full(K,1/Ns)
d=2*(u*u*q2-u*u)/(eps*(np.sqrt(1+u*u*q2)+math.sqrt(1+u*u)))
def rhs(t,y):
    B=y[0];C=y[1:K+1];F=y[K+1:].real;S=F.sum();Z=C.sum()
    pair=B+kappa*Z;normal=d+4*kappa*S
    return np.r_[-1j*C.sum(),-1j*normal*C-1j*pair*(2*F+w),-2*np.imag(np.conj(pair)*C)]
def event(target):
    def ev(t,y):return y[K+1:].real.sum()-target
    ev.direction=1;ev.terminal=target==.001
    return ev
init=np.zeros(2*K+1,complex);init[0]=1
sol=solve_ivp(rhs,(0,100),init,method='DOP853',rtol=1e-10,atol=np.r_[1e-13,w*1e-7,w*1e-7],max_step=.05,events=[event(x) for x in [1e-5,1e-4,1e-3]])
checks=[];states=[]
def check(n,b,v=None):checks.append(dict(name=n,passed=bool(b),value=v))
check('integration',sol.success)
for target,ts,ys in zip([1e-5,1e-4,1e-3],sol.t_events,sol.y_events):
    check('handoff reached '+str(target),len(ts)==1)
    y=ys[0];B=y[0];C=y[1:K+1];F=y[K+1:].real
    err=abs(abs(B)**2+F.sum()-1)
    relative=float(np.max(abs(abs(C)-np.sqrt(np.maximum(0,F*(F+w))))/(F+w)))
    check('charge '+str(target),err<1e-8,float(err))
    check('pure-covariance projection small '+str(target),relative<1e-6,relative)
    states.append(dict(target=target,x=float(ts[0]),B=[float(B.real),float(B.imag)],F=F.tolist(),C_real=C.real.tolist(),C_imag=C.imag.tolist(),max_relative_covariance_projection=relative))
# A spectral construction avoids catastrophic subtraction of squeezed variances.
rng=np.random.default_rng(471901);F=np.array(states[1]['F']);C=np.array(states[1]['C_real'])+1j*np.array(states[1]['C_imag'])
# Test the most amplified pair using many independent draws, not a normalized realization.
j=int(np.argmax(F));s=(F[j]+w[j]/2)/2;mag=math.sqrt(F[j]*(F[j]+w[j]))/2
large=(s+mag)/2;small=(w[j]/4)**2/(2*(s+mag))
u1=(rng.normal(size=100000)+1j*rng.normal(size=100000))/math.sqrt(2)
u2=(rng.normal(size=100000)+1j*rng.normal(size=100000))/math.sqrt(2)
left=math.sqrt(large)*u1+math.sqrt(small)*u2
right=np.exp(1j*np.angle(C[j]))*(math.sqrt(large)*u1.conjugate()-math.sqrt(small)*u2.conjugate())
variance=float(np.mean(abs(left)**2));cov=np.mean(left*right);desired=mag*np.exp(1j*np.angle(C[j]))
check('sample variance',abs(variance/s-1)<.02,variance/s-1)
check('sample anomalous covariance',abs(cov/desired-1)<.02,float(abs(cov/desired-1)))
out=dict(parameters=dict(m=m,u=u,epsilon=eps,R=R,kappa=kappa,dq=dq,source_quanta=Ns,pair_weight=float(w[0]),pair_count=K),pairs=pairs,states=states,checks=checks,all_pass=all(c['passed'] for c in checks),sample_check=dict(draws=100000,pair_index=j,occupation=float(F[j]/w[j])),non_claims=['Finite fixed box and no expansion','Gaussian early evolution','Pure covariance projection and classical source adjustment are declared approximations','Not full quantum-classical error control'])
(p/'quantum_handoff_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['pairs','states']},indent=2))
for state in states:print(json.dumps({k:state[k] for k in ['target','x','B','max_relative_covariance_projection']}))
assert out['all_pass']
