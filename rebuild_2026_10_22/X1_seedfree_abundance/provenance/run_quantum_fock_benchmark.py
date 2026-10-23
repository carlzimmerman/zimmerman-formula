"""Original-action Hamiltonian absorption benchmark, not a cosmological bath."""
from pathlib import Path
import json,sys
import numpy as np
from scipy.linalg import eigh
from quantum_fock_solver import Model
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
rows=[];checks={}
for cut in [8.,10.,12.]:
 model=Model(energy_cut=cut,number_cut=8,charge=2,volume=100.)
 ini=np.zeros(12,dtype=int);ini[[1,4,7]]=1
 fin=np.zeros(12,dtype=int);fin[[0,2]]=1
 i=model.index[tuple(ini)];f=model.index[tuple(fin)];E=model.free[i]
 den=E-model.free;inv=np.zeros_like(den);mask=abs(den)>1e-10;inv[mask]=1/den[mask]
 h3=model.H3.toarray();h4=model.H4.toarray()
 mixed=float(np.sum((h3[f]*h4[:,i]+h4[f]*h3[:,i])*inv)*model.g*model.lam)
 cubic=float((h3[f]*inv)@h3@(inv*h3[:,i])*model.g**3)
 M=model.M;p=model.p;Ef=(M+2)/2
 d=np.array([M*(M+2),-2*M,-2*M]);dx=np.array([(M+2)**2-M*M,-M*(M+1),-M*(M+1)])
 norm=np.sqrt((2*M)*2*2*(2*Ef)**2)*model.volume**1.5
 expected_mixed=8*model.g*model.lam*np.sum(1/d)/norm
 expected_cubic=8*model.g**3*np.sum(1/(d*dx))/norm
 row=dict(energy_cut=cut,states=len(model.states),mixed_Hamiltonian=mixed,mixed_covariant=expected_mixed,cubic_Hamiltonian=cubic,cubic_covariant=expected_cubic,mixed_relative_error=abs(mixed/expected_mixed-1),cubic_relative_error=abs(cubic/expected_cubic-1))
 rows.append(row);print(row,flush=True)
 if cut==12:
  # Full original vertices, not effective reaction added a second time.
  h=model.hamiltonian().toarray();evals,evecs=eigh(h)
  times=np.linspace(0,10000,1001);phase=np.exp(-1j*times[:,None]*evals)
  hist=(phase*evecs[i])@evecs.T;back=(phase*evecs[f])@evecs.T
  n,corr=model.occupation_correlations(hist)
  prob=abs(hist[:,f])**2;inverse=abs(back[:,i])**2
  energy=np.real(np.einsum('ti,ij,tj->t',hist.conj(),h,hist,optimize=True))
  boundary=np.sum(abs(hist[:,model.free>cut-2])**2,axis=1)
  diag=np.column_stack((times,prob,inverse,n.sum(axis=1),corr[:,1,4],boundary,energy))
  np.savetxt(O/'unitary_history.csv',diag,delimiter=',',header='time_m_inverse,P_absorption,P_inverse,mean_total_particles,connected_phi0_antiphi0,upper_shell_probability,energy',comments='')
  dynamics=dict(max_absorption_probability=float(prob.max()),max_inverse_difference=float(np.max(abs(prob-inverse))),max_norm_error=float(np.max(abs(np.sum(abs(hist)**2,axis=1)-1))),energy_relative_drift=float(np.ptp(energy)/abs(energy[0])),max_upper_shell_probability=float(boundary.max()),max_abs_connected_population_covariance=float(np.max(abs(corr[:,1,4]))),scope='Few-mode recurrence dynamics from a specified scattering test state. Not cosmological initial state or thermalization; probability is NOT a continuum rate.')
  checks.update(Hermitian=np.max(abs(h-h.T))<1e-13,unitarity=dynamics['max_norm_error']<1e-10,energy=dynamics['energy_relative_drift']<1e-10,inverse_reciprocity=dynamics['max_inverse_difference']<1e-12)
checks.update(mixed_tree_complete=rows[-1]['mixed_relative_error']<1e-10,cubic_tree_complete=rows[-1]['cubic_relative_error']<1e-10)
out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),amplitude_checks=rows,dynamics=dynamics,scope='Normal-ordered finite-box Galerkin Hamiltonian. No cosmological source preparation, thermal bath, quantum continuum renormalization, or surviving abundance. No separately added reaction rate.')
(O/'results.json').write_text(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
