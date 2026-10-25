"""Hamiltonian variation/reversibility and asymmetric-state box-size probe."""
import argparse,json
import numpy as np
from experiment import Model

def step(model,p,dt):
    p=p*np.exp(-.5j*dt/model.h*model.potential(p))
    phase=np.exp(-1j*dt*model.h/(2*model.ms[:,None,None,None])*model.k2)
    p=np.fft.ifftn(np.fft.fftn(p,axes=(1,2,3))*phase,axes=(1,2,3))
    return p*np.exp(-.5j*dt/model.h*model.potential(p))

def checks():
    m=Model(N=24,h=.5,eps=.1);p=m.initial(.5,.05)
    x,y,z=m.xyz;d=np.array([np.exp(-m.r**2/6)*(1+.3j*np.sin(y)),np.exp(-m.r**2/5)*(.2+.2j*np.cos(x))])
    kinetic=np.fft.ifftn(np.fft.fftn(p,axes=(1,2,3))*m.k2,axes=(1,2,3))*m.h**2/(2*m.ms[:,None,None,None])
    hp=kinetic+m.potential(p)*p
    analytic=2*np.real(np.sum(np.conj(d)*hp))*m.dv
    errors=[]
    for a in [1e-4,1e-5,1e-6]:
        finite=(m.measure(p+a*d)['energy']-m.measure(p-a*d)['energy'])/(2*a)
        errors.append(abs(finite-analytic)/max(1,abs(analytic)))
    reversed=step(m,step(m,p,.01),-.01)
    reverse_error=float(np.linalg.norm(reversed-p)/np.linalg.norm(p))
    assert min(errors)<1e-8 and reverse_error<1e-12
    return dict(Hamiltonian_derivative_relative_errors=errors,time_reversal_relative_error=reverse_error)

def probe(N,L,spin):
    m=Model(N=N,L=L,h=.5,eps=.1);p=m.initial(spin);a=m.measure(p)
    maxerror=0.
    for j in range(100):
        p=step(m,p,.01)
        if (j+1)%5==0:
            r=m.measure(p);maxerror=max(maxerror,abs(r['energy']-a['energy'])/a['absolute_energy_scale'])
    d,rm,*_=m.fields(p)
    return dict(N=N,L=L,spin=spin,initial=a,final=r,max_energy_error=maxerror,
        final_edge_mass=float(np.sum(rm*(m.r>L/2-1.5))*m.dv))

p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
r=dict(checks=checks(),box_runs=[probe(N,L,s) for N,L in [(32,16),(48,24)] for s in [0.,.5]])
with open(args.output,'w') as f:json.dump(r,f,indent=2,allow_nan=False)
print(json.dumps(r['checks']))
