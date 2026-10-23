"""Independent evolution/convergence checks and actual-source representability."""
from pathlib import Path
import json,sys
import numpy as np
from scipy.linalg import eigh
from scipy.integrate import solve_ivp
from quantum_fock_solver import Model
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
checks={};rows=[]
for cut in [12.,14.]:
 mo=Model(energy_cut=cut,number_cut=10,charge=2,volume=100.)
 state=np.zeros(12,dtype=int);state[[1,4,7]]=1;i=mo.index[tuple(state)]
 final=np.zeros(12,dtype=int);final[[0,2]]=1;f=mo.index[tuple(final)]
 h=mo.hamiltonian().toarray();ev,U=eigh(h);ts=np.linspace(0,10000,101);phase=np.exp(-1j*ts[:,None]*ev);ps=(phase*U[i])@U.T
 # Genuine non-Gaussian, two-time connected number correlation; no factorization.
 obs=mo.states[:,6:9].sum(axis=1);obse=(U.T*obs)@U
 bs=(phase*U[i])@obse.T;bs*=phase.conj()
 mean=np.sum(abs(ps)**2*obs,axis=1)
 conn=bs.conj()@bs.T-mean[:,None]*mean[None,:]
 statistical=conn.real;spectral=-2*conn.imag
 np.savez_compressed(O/('two_time_cut%d.npz'%cut),times=ts,F=statistical,rho=spectral,mean_nX=mean)
 var=np.sum(abs(ps)**2*obs**2,axis=1)-mean**2
 row=dict(energy_cut=cut,states=len(mo.states),probability=abs(ps[:,f])**2,mean=mean,max_quantum_spectral_correlation=float(np.max(abs(spectral))),equal_time_variance_error=float(np.max(abs(np.diag(statistical)-var))))
 rows.append(row)
 checks['F_symmetric_cut%d'%cut]=np.max(abs(statistical-statistical.T))<1e-12
 checks['rho_antisymmetric_cut%d'%cut]=np.max(abs(spectral+spectral.T))<1e-12
 checks['equal_time_variance_cut%d'%cut]=row['equal_time_variance_error']<1e-12
 print(cut,len(mo.states),flush=True)
prob_rel=float(np.max(abs(rows[1]['probability']-rows[0]['probability']))/np.max(rows[1]['probability']))
# Time-dependent nonlinear Hamiltonian: independent DOP853 vs midpoint unitary.
mo=Model(energy_cut=8,number_cut=8,charge=0,volume=100.)
h0=mo.hamiltonian().toarray();ev,U=eigh(h0);ground=U[:,0].astype(complex)
a=lambda t:1+.1*(1-np.cos(np.pi*t/2))
ref=solve_ivp(lambda t,y:-1j*(mo.hamiltonian(a(t))@y),(0,2),ground,method='DOP853',rtol=1e-11,atol=1e-13)
errs=[]
for steps in [40,80]:
 history=mo.evolve(ground,np.linspace(0,2,steps+1),scale_factor=a)
 errs.append(float(np.linalg.norm(history[-1]-ref.y[:,-1])))
checks['midpoint_second_order']=3.5<errs[0]/errs[1]<4.5
checks['adaptive_success']=ref.success
# Stationary interacting ground state must not be called production from bare vacuum.
static=mo.evolve(ground,np.linspace(0,20,21));stationary=float(np.max(abs(abs(static)**2-abs(ground)**2)))
# Use the same 1e-10 unitary-propagation tolerance as the main benchmark.
checks['interacting_ground_stationary']=stationary<1e-10
# Existing conformal source quadrature means cannot fit into a low-occupation box.
raw=np.fromfile(P/'coupled_fragmentation_96_run/fine96_initial.bin',dtype='<f8');n=int(raw[0]);box=raw[1];q,v=raw[9:].reshape(2,4,n,n,n).mean(axis=(2,3,4));lam=.00881292
minimum=box**3*abs(q*v)/lam
source=dict(mean_q=q.tolist(),mean_v=v.tolist(),minimum_mean_displacement_occupation_over_positive_reference_frequencies=minimum.tolist(),interpretation='Representation bound in an undisplaced conformal oscillator basis, NOT physical particle abundance in a super-Hubble state. Displacing or squeezing the basis can remove this particular cost, but does not supply the missing nonlinear many-mode evolution.')
checks['source_outside_small_fock_cut']=float(minimum.max())>1e4
out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),cutoff_probability_max_relative_difference=prob_rel,rows=[{k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in r.items()} for r in rows],midpoint_errors=errs,ground_state_probability_drift=stationary,source_representation=source,scope='Finite-mode benchmark validation, not evidence of thermalization or a cold relic. Time-dependent test scale factor is a numerical test function, not the cosmological source history.')
(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2));sys.exit(0 if out['all_pass'] else 1)
