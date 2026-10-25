"""Periodic two-component Schrodinger-Poisson-Coulomb mean-field evolution."""
import argparse
import json
import numpy as np

def evolve(N,dt,Q=.7,eps=.1,duration=.5):
    a=np.arange(N)*2*np.pi/N
    x,y,z=np.meshgrid(a,a,a,indexing='ij')
    k=np.fft.fftfreq(N,1/N)
    kx,ky,kz=np.meshgrid(k,k,k,indexing='ij');k2=kx*kx+ky*ky+kz*kz
    inv=np.zeros_like(k2);inv[k2>0]=1/k2[k2>0]
    mass=np.array([1.,eps]);charge=np.array([1.,-1.])
    psi=np.array([np.sqrt(1+.02*np.cos(x)+.01*np.cos(y))*np.exp(.01j*np.sin(z)),
                  np.sqrt(1+.015*np.cos(x)-.01*np.cos(y))*np.exp(-.01j*np.sin(z))])
    def potential(p):
        density=abs(p)**2
        nc=np.einsum('s,sijk->ijk',charge,density)
        nm=np.einsum('s,sijk->ijk',mass,density)
        vc=np.fft.ifftn(np.fft.fftn(nc)*inv).real
        vm=np.fft.ifftn(np.fft.fftn(nm)*inv).real
        return (charge[:,None,None,None]*vc-mass[:,None,None,None]*vm)/(2*Q),vc,vm
    def measure(p):
        d=abs(p)**2
        potential_p,vc,vm=potential(p)
        nc=np.einsum('s,sijk->ijk',charge,d)
        nm=np.einsum('s,sijk->ijk',mass,d)
        kinetic=sum(Q/mass[s]*np.sum(k2*abs(np.fft.fftn(p[s]))**2)/N**6 for s in range(2))
        uc=np.mean(nc*vc)/(4*Q);ug=-np.mean(nm*vm)/(4*Q)
        return dict(energy=float(kinetic+uc+ug),kinetic=float(kinetic),electric=float(uc),gravity=float(ug),
                    number=np.mean(d,axis=(1,2,3)).tolist(),
                    density_cosine_amplitudes=[float(2*np.mean((d[s]-1)*np.cos(x))) for s in range(2)])
    steps=int(round(duration/dt));assert abs(steps*dt-duration)<1e-12
    kinphase=np.exp(-1j*(Q/mass[:,None,None,None])*k2*dt)
    first=measure(psi);energies=[first['energy']];number_errors=[]
    for j in range(steps):
        V,_,_=potential(psi);psi*=np.exp(-.5j*dt*V)
        psi=np.fft.ifftn(np.fft.fftn(psi,axes=(1,2,3))*kinphase,axes=(1,2,3))
        V,_,_=potential(psi);psi*=np.exp(-.5j*dt*V)
        obs=measure(psi);energies.append(obs['energy'])
        number_errors.append(max(abs(np.array(obs['number'])-first['number'])))
    scale=first['kinetic']+abs(first['electric'])+abs(first['gravity'])
    return dict(N=N,dt=dt,Q=Q,epsilon=eps,duration=duration,initial=first,final=obs,
        max_energy_error_over_initial_absolute_components=float(max(abs(np.array(energies)-energies[0]))/scale),
        max_species_number_error=float(max(number_errors))),psi

def main(path):
    rows=[];states={}
    for N in [12,18,24]:
        for dt in [.01,.005,.0025]:
            row,p=evolve(N,dt);rows.append(row);states[N,dt]=p
    refinement=[]
    for N in [12,18,24]:
        refinement.append(dict(N=N,coarse_medium=float(np.linalg.norm(states[N,.01]-states[N,.005])/np.linalg.norm(states[N,.005])),
            medium_fine=float(np.linalg.norm(states[N,.005]-states[N,.0025])/np.linalg.norm(states[N,.0025]))))
    result=dict(runs=rows,time_refinement=refinement)
    with open(path,'w') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(result))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
