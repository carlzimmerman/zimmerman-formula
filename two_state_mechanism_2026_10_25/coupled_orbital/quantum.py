import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh


def evolve(cutoff,ratio):
    M=100.;K=10.;kap=1.;Q=1.;d=.2
    omega=np.sqrt((K+kap*Q*Q)/M);x0=np.sqrt(1/(2*M*omega));g=-kap*d*Q*x0
    b=np.diag(np.sqrt(np.arange(1,cutoff)),1);x=x0*(b+b.T)
    sx=np.array([[0,1],[1,0]]);sz=np.diag([1.,-1.]); eye=np.eye(cutoff)
    H=np.kron(ratio*omega/2*sz,eye)+np.kron(np.eye(2),omega*(b.T@b+.5*eye))
    H+=g*np.kron(sx,b+b.T)+kap*d*d/2*np.eye(2*cutoff)
    w,v=eigh(H);initial=np.zeros(2*cutoff);initial[0]=1
    times=np.linspace(0,np.pi/abs(g),801)
    states=v@((v.conj().T@initial)[:,None]*np.exp(-1j*w[:,None]*times[None,:]))
    pe=np.sum(abs(states[:cutoff])**2,axis=0)
    nb=np.sum(abs(states.reshape(2,cutoff,-1))**2*np.arange(cutoff)[None,:,None],axis=(0,1))
    energy=np.real(np.sum(states.conj()*(H@states),axis=0))
    spin=np.real(np.sum(states.conj()*(np.kron(sx,eye)@states),axis=0))
    displacement=np.real(np.sum(states.conj()*(np.kron(np.eye(2),x)@states),axis=0))
    edge=np.sum(abs(states.reshape(2,cutoff,-1)[:,-2:,:])**2,axis=(0,1))
    idx=int(np.argmin(pe));sample=range(0,len(times),20)
    return dict(cutoff=cutoff,detuning_ratio=ratio,omega=omega,coupling=g,
                minimum_excited_population=float(pe[idx]),time_of_minimum=float(times[idx]),
                phonon_number_at_minimum=float(nb[idx]),
                rwa_transfer_time=float(np.pi/(2*abs(g))),
                max_energy_error=float(np.max(abs(energy-energy[0]))),
                norm_error=float(np.max(abs(np.sum(abs(states)**2,axis=0)-1))),
                max_sigma_x=float(np.max(abs(spin))),max_mean_x=float(np.max(abs(displacement))),
                maximum_edge_population=float(np.max(edge)),
                times=times[list(sample)].tolist(),excited=pe[list(sample)].tolist(),phonons=nb[list(sample)].tolist())

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    rows=[evolve(n,r) for n in [16,24] for r in [.5,1.,2.]]
    diff=max(np.max(abs(np.array(rows[i]['excited'])-np.array(rows[i+3]['excited']))) for i in range(3))
    assert diff<1e-10
    assert max(r['max_energy_error'] for r in rows)<1e-12
    assert max(r['norm_error'] for r in rows)<1e-12
    assert max(r['maximum_edge_population'] for r in rows)<1e-12
    result=dict(runs=rows,cutoff_agreement=float(diff),mean_field_excited_population=1.)
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    for r in rows: print(r['cutoff'],r['detuning_ratio'],r['minimum_excited_population'],r['time_of_minimum'],r['max_energy_error'])
if __name__=='__main__':main()
