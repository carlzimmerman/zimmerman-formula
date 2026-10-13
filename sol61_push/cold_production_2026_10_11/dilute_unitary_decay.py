"""Unitary one-source / daughter-pair continuum approximation; finite-band convergence."""
import json,math
from pathlib import Path
import numpy as np
from scipy.sparse import diags,coo_matrix
from scipy.sparse.linalg import expm_multiply
p=Path(__file__).parent
a=json.loads((p/'dilute_decay_v2_run/results.json').read_text())['rows'][-1]
m=a['m_eV'];M=a['M_eV'];width=a['source_width_eV'];u=math.sqrt(M*M/(4*m*m)-1)
checks=[];rows=[]
def ck(n,b):checks.append(dict(name=n,passed=bool(b)))
for L,dx in [(50,.2),(100,.2),(200,.2),(400,.2),(400,.1)]:
    N=int(round(2*L/dx));x=-L+(np.arange(N)+.5)*dx
    # Gamma(E)/Gamma(M) from same vacuum two-body phase space, on finite near-resonant band.
    E=M+width*x
    gamma_ratio=(M/E)*np.sqrt(1-4*m*m/(E*E))/math.sqrt(1-4*m*m/(M*M))
    J=gamma_ratio/(2*math.pi)
    v=np.sqrt(J*dx)
    # Principal-value subtraction fixes the continuum real self-energy at x=0.
    bare=float(np.sum((J-1/(2*math.pi))/x)*dx)
    H=diags(np.r_[bare,x],format='csr')
    indices=np.arange(1,N+1)
    H+=coo_matrix((np.r_[v,v],(np.r_[np.zeros(N,dtype=int),indices],np.r_[indices,np.zeros(N,dtype=int)])),shape=(N+1,N+1)).tocsr()
    initial=np.zeros(N+1,complex);initial[0]=1
    ts=np.linspace(0,10,101)
    y=expm_multiply(-1j*H,initial,start=0,stop=10,num=101,traceA=-1j*float(H.diagonal().sum()))
    norms=np.sum(abs(y)**2,axis=1);survival=abs(y[:,0])**2
    energies=np.real(np.sum(np.conj(y)*(H@y.T).T,axis=1))
    normerr=float(np.max(abs(norms-1)));enerr=float(np.max(abs(energies-bare)))
    ck('unit norm '+str((L,dx)),normerr<1e-9)
    ck('total Hamiltonian energy '+str((L,dx)),enerr<1e-8)
    ck('below recurrence time '+str((L,dx)),10<2*math.pi/dx)
    rows.append(dict(L=L,dx=dx,pair_modes=N,recurrence_time_in_lifetimes=2*math.pi/dx,bare_source_shift_in_widths=bare,norm_error=normerr,energy_error_in_widths=enerr,max_absolute_survival_deviation_from_exponential=float(np.max(abs(survival-np.exp(-ts)))),survival_at_1=float(survival[10]),survival_at_5=float(survival[50]),survival_at_10=float(survival[-1]),daughter_pair_probability_at_10=float(np.sum(abs(y[-1,1:])**2))))
ck('largest bandwidth close to exponential',rows[-1]['max_absolute_survival_deviation_from_exponential']<.005)
ck('spectral spacing refinement',abs(rows[-1]['survival_at_5']-rows[-2]['survival_at_5'])<1e-6)
ck('bandwidth improves approximation',rows[-1]['max_absolute_survival_deviation_from_exponential']<rows[0]['max_absolute_survival_deviation_from_exponential'])
out=dict(parameters=a,rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),scope='Closed Hermitian star Hamiltonian in one-source/pair subspace; finite near-resonant band; real on-shell self-energy subtraction; coupling fixed by vacuum spectral density',non_claims=['No full relativistic QFT or ultraviolet completion','Quartic pair rescattering and many-source correlations omitted','No source preparation or halo/cosmological prediction'])
(p/'dilute_unitary_decay_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
