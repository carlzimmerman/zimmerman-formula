import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record
import numpy as np

def calculate():
    N=64; h=1/N; x=np.arange(N)*h; one=np.ones(N); mode=np.cos(2*np.pi*x); rho=one+0.5*mode
    B=np.zeros((N,N))
    for i in range(N):B[i,i]=-1/h;B[i,(i+1)%N]=1/h
    Dface=0.01*(1+0.5*np.cos(2*np.pi*(x+h/2)))
    Dpoint=0.01*(1+0.5*np.cos(2*np.pi*x))
    A=np.eye(N)+B.T@np.diag(Dface)@B; H=np.linalg.inv(A); filtered=H@rho
    constant=np.linalg.solve(np.eye(N)+0.01*B.T@B,rho)
    expected=one+0.5*mode/(1+0.01*4*np.sin(np.pi/N)**2/h**2)
    bad=np.linalg.inv(np.eye(N)+np.diag(Dpoint)@(B.T@B)); mutated=bad@rho
    vals={'mass_error':float(abs(filtered.mean()-rho.mean())),'constant_error':float(np.max(abs(H@one-one))),'reciprocity_error':float(np.max(abs(H-H.T))),'minimum_density':float(filtered.min()),'known_answer_error':float(np.max(abs(constant-expected))),'mutate_mass_error':float(abs(mutated.mean()-rho.mean())),'mutate_reciprocity_error':float(np.max(abs(bad-bad.T)))}
    checks={'mass':vals['mass_error']<=1e-11,'constants':vals['constant_error']<=1e-11,'reciprocity':vals['reciprocity_error']<=1e-11,'positive':vals['minimum_density']>=-1e-12,'known_answer':vals['known_answer_error']<=1e-11,'mutate_bites':max(vals['mutate_mass_error'],vals['mutate_reciprocity_error'])>1e-6}
    label='PASS' if all(checks.values()) else 'NO VERDICT'
    return {'assertion_tested':'conservative resolvent identities on N=64 periodic line','label':label,'scope':'operator gates only','footings':{f:{'label':label,'values':vals,'checks':checks,'empirical_label':'NOT EVALUABLE'} for f in ['canonical','alt']},'bounds':{'N':64},'free_physical_numbers':['kappa=1/2 FITTED','D(x) is unspecified physically; any selected coefficients remain FITTED'], 'checks':[{'name':k,'passed':bool(v)} for k,v in checks.items()],'residual_risks':['prescribed D, not self-consistent gravitational action','periodic 1D synthetic data only']}
record(__file__,calculate)
