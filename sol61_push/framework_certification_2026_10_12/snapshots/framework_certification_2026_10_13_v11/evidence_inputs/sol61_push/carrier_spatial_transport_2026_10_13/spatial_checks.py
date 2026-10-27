"""Conditional seven-population angular quadrature with a LIVE source species."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import xlogy

HERE=Path(__file__).resolve().parent
m=1.;eps=.01;beta=.1;coupling=.001
M=2*m/np.sqrt(1-eps*eps);boost=1/np.sqrt(1-beta*beta)
Delta=M*M-4*m*m;lambda_rep=.001
lambda_tot=coupling*coupling/Delta+lambda_rep
Gamma0=coupling*coupling*eps/(8*np.pi*M);Gamma_lab=Gamma0/boost
energies=[];momenta=[]
for axis in range(3):
    n=np.eye(3)[axis]
    for sign in [1,-1]:
        energies.append(boost*M/2*(1+sign*beta*eps*n[2]))
        momenta.append([sign*M*eps*n[0]/2,sign*M*eps*n[1]/2,
                        boost*M/2*(beta+sign*eps*n[2])])
energies=np.array(energies+[boost*M]);momenta=np.array(momenta+[[0,0,boost*beta*M]])
vel=momenta/energies[:,None]
mass=np.array([m]*6+[M]);charge=np.array([1.]*6+[2.])
stress=momenta[:,:,None]*momenta[:,None,:]/energies[:,None,None]
for j in range(3):
    b=np.zeros(7);b[2*j:2*j+2]=1;b[6]=-1
    assert abs(energies@b)<1e-12 and np.max(np.abs(momenta.T@b))<1e-12 and charge@b==0
assert np.max(np.abs(energies*energies-(momenta*momenta).sum(axis=1)-mass*mass))<1e-12

def simulate(N,kind='main'):
    dx=2*np.pi/N;grid=np.arange(N)*dx
    x,y,z=np.meshgrid(grid,grid,grid,indexing='ij')
    n=np.array([.001*(1+.05*np.sin(x+2*y+z+i)) for i in range(6)]+
               [.02*(1+.1*np.cos(x)*np.cos(y)*np.cos(z))])
    if kind=='empty':n[:6]=0
    if kind=='inverse':n[:6]=.02;n[6]=0
    initial=n.copy();y0=n.ravel()
    def reactions(n):
        ns=n[6];r=np.zeros_like(n);rates=[]
        for j in range(3):
            a=n[2*j];b=n[2*j+1]
            J=(ns*(1+a)*(1+b)-(1+ns)*a*b)/3
            if kind=='off':J=np.zeros_like(J)
            r[2*j]+=J;r[2*j+1]+=J;r[6]-=J;rates.append(J)
        return r,np.array(rates)
    def rhs(t,state):
        n=state.reshape(7,N,N,N);out=reactions(n)[0]
        for species in range(7):
            for axis,v in enumerate(vel[species]):
                if v>=0:d=(n[species]-np.roll(n[species],1,axis=axis))/dx
                else:d=(np.roll(n[species],-1,axis=axis)-n[species])/dx
                out[species]-=v*d
        return out.ravel()
    initial_rate=rhs(0,y0).reshape(7,N,N,N).sum(axis=(1,2,3))*dx**3
    residuals={'charge':float(charge@initial_rate),'energy':float(energies@initial_rate),
               'momentum':(momenta.T@initial_rate).tolist()}
    assert max(abs(residuals['charge']),abs(residuals['energy']),np.max(np.abs(residuals['momentum'])))<1e-10
    sol=solve_ivp(rhs,(0,2),y0,method='DOP853',rtol=2e-10,atol=2e-12,t_eval=np.linspace(0,2,81))
    assert sol.success,sol.message
    alln=sol.y.reshape(7,N,N,N,-1)
    counts=alln.sum(axis=(1,2,3))*dx**3
    q=charge@counts;energy=energies@counts;p=momenta.T@counts
    K=(energies-mass)@counts;rest=mass@counts
    errors={'charge_absolute':float(np.max(np.abs(q-q[0]))),
            'energy_relative':float(np.max(np.abs(energy-energy[0]))/max(1,abs(energy[0]))),
            'momentum_absolute':float(np.max(np.abs(p-p[:,[0]])))}
    assert max(errors.values())<=1e-8 and alln.min()>=-1e-9
    rho=np.einsum('i,iabct->abct',charge,alln)
    densitychange=float(dx**3*np.abs(rho[:,:,:,-1]-rho[:,:,:,0]).sum())
    if kind in ['main','off','empty']:assert densitychange>1e-8
    sourcechange=float(counts[6,-1]-counts[6,0]);daughterchange=float(counts[:6,-1].sum()-counts[:6,0].sum())
    if kind in ['main','empty']:assert sourcechange<0 and daughterchange>0
    if kind=='inverse':assert sourcechange>0 and daughterchange<0
    if kind=='off':assert abs(sourcechange)<1e-10 and abs(daughterchange)<1e-10
    kinetic_identity=float(K[-1]-K[0]+(M-2*m)*sourcechange)
    assert abs(kinetic_identity)<1e-8
    stress_change=np.einsum('ijk,i->jk',stress,counts[:,-1]-counts[:,0])
    eig=np.linalg.eigvalsh(stress_change)
    if kind in ['main','empty']:assert eig.min()>=-1e-9
    if kind=='inverse':assert eig.max()<=1e-9
    clipped=np.maximum(alln,0)
    entropy=(xlogy(1+clipped,1+clipped)-xlogy(clipped,clipped)).sum(axis=(0,1,2,3))*dx**3
    assert np.diff(entropy).min()>=-1e-8
    np.savez_compressed(HERE/('spatial_run/final_%s_N%s.npz'%(kind,N)),initial=initial,final=alln[:,:,:,:,-1],energies=energies,momenta=momenta,velocities=vel)
    return {'N':N,'kind':kind,'initial_invariant_residuals':residuals,'errors':errors,
            'minimum_sampled_occupation':float(alln.min()),'L1_charge_density_change':densitychange,
            'source_number_change':sourcechange,'daughter_number_change':daughterchange,
            'kinetic_energy_change':float(K[-1]-K[0]),'particle_rest_energy_change':float(rest[-1]-rest[0]),
            'kinetic_identity_error':kinetic_identity,'kinetic_stress_change_eigenvalues':eig.tolist(),
            'minimum_sampled_entropy_increment':float(np.diff(entropy).min())},alln[:,:,:,:,-1]

main8,last8=simulate(8);main16,last16=simulate(16)
empty,_=simulate(8,'empty');inverse,_=simulate(8,'inverse');off,_=simulate(8,'off')
result={'conditional_parameters':{'m':m,'M':M,'epsilon':eps,'beta':beta,'g':coupling,
         'lambda_rep':lambda_rep,'lambda_tot':lambda_tot,'Gamma0':Gamma0,'Gamma_lab':Gamma_lab,
         'time_units':'1/Gamma_lab','length_units':'c/Gamma_lab','occupation_cell_weight_diagnostic':1},
         'cases':[main8,main16,empty,inverse,off],
         'two_grid_final_occupation_RMS_difference':float(np.sqrt(np.mean((last8-last16[:,::2,::2,::2])**2))),
         'scope':'Conditional finite angular/occupation-cell closure retaining chi, no gravity, field-to-kinetic proof, physical cell normalization or selector.'}
(HERE/'spatial_run/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
