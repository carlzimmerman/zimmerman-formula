"""Auxiliary-mode elimination, barrier bounds and post-hoc robustness checks."""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from angular_gate import Field,PROFILES,moment_C


def ev(field,f,beta):
    curv,_=field.stability(beta,field.kinematics(f)['C'])
    D=field.mobility_denom
    return float(eigh_tridiagonal((curv+np.diag(field.Lmat))/D,
        np.diag(field.Lmat,1)/np.sqrt(D[:-1]*D[1:]),select='i',select_range=(0,0),
        eigvals_only=True,lapack_driver='stebz',tol=1e-10)[0])


# Positive auxiliary strain: z^2+r(z-S)^2 -> r/(1+r) S^2.
aux_errors=[]
for ratio in np.logspace(-8,8,65):
    for x in np.linspace(0,2,41):
        S=np.sin(np.pi*x)/np.pi
        z=ratio/(1+ratio)*S
        actual=z*z+ratio*(z-S)**2
        expected=ratio/(1+ratio)*S*S
        aux_errors.append(abs(actual-expected))
assert max(aux_errors)<1e-12

# Mean counterrotation has zero vorticity just like zero mean pressure support.
vel=np.array([[0,10,0],[0,-10,0]])
counter_C=moment_C(np.zeros((3,3)),vel,np.array([1.,0,0]),np.eye(3))
assert counter_C==0

rows=[]; sensitivities=[]
for i,(_,mass,b,_) in enumerate(PROFILES):
    field=Field(mass,b,128,30,grid='uniform');C=field.kinematics(.95)['C']
    xs=np.linspace(0,1,501)
    energies=np.array([field.energy_grad(np.full(128,x),20,C)[0] for x in xs])
    barrier=max(0.,float(energies.max()-energies[-1]))
    endpoint_ev=ev(field,.95,20)
    trials=[]
    if endpoint_ev>0:
        for seed in (.9,.5):
            r=field.evolve(.95,20,seed,gradient_damping=True)
            trials.append(dict(seed=seed,q_final=r['tethered_mass_fraction'],
                               energy_error=r['energy_receiver_balance_max']))
    rows.append(dict(profile_index=i,uniform_path_barrier_over_T_energy=barrier/energies[-1],
                     uniform_path_barrier_dimensionless=barrier,
                     uniform_path_x_at_max=float(xs[np.argmax(energies)]),
                     lowest_endpoint_eigenvalue=endpoint_ev,
                     caveat='Upper bound on an escape barrier; spatial nucleation may be cheaper',
                     finite_amplitude_trials=trials,
                     x_path=xs.tolist(),energy_over_T_energy=(energies/energies[-1]).tolist()))
    for beta in (16.,20.,24.):
        for length in (24.,30.,36.):
            m=Field(mass,b,128,length,grid='uniform')
            sensitivities.append(dict(profile_index=i,beta=beta,length_kpc=length,
                low_streaming_ev=ev(m,.3,beta),high_streaming_ev=ev(m,.95,beta)))

result=dict(auxiliary_elimination_max_absolute_error=max(aux_errors),
    counterrotating_streams_C=counter_C,
    counterrotation_prediction='No protection from this vorticity-only ordered-motion statistic',
    profiles=rows,posthoc_sensitivity=sensitivities,
    nonclaim='No thermal lifetime or absolute physical transition rate is inferred')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('profiles','posthoc_sensitivity')},indent=2))
for row in rows: print(json.dumps({k:v for k,v in row.items() if k not in ('x_path','energy_over_T_energy')},indent=2))
