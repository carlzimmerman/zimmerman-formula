"""Conditional light-field stochastic inflation, with the existing potential.
Coarse field starts at zero; vacuum horizon-crossing noise builds its variance.
This is not a post-inflation phase-space or particle spectrum calculation.
"""
import json,sys
from pathlib import Path
import numpy as np
H=1.3445177278709404e10;m=.001;M=2*m*np.sqrt(1+.02**2);g=2.168e-6;lam=.00881292
patches=4096;dt=.02;duration=60.;rng=np.random.default_rng(20261022)
coarse=np.zeros((patches,4));fine=coarse.copy()
def drift(z):
    f1,f2,x1,x2=z.T;r2=f1*f1+f2*f2;c=np.sqrt(2)*g/H
    return -np.array([(m/H)**2*f1+c*(x1*f1+x2*f2)+lam*r2*f1,
        (m/H)**2*f2+c*(-x1*f2+x2*f1)+lam*r2*f2,
        (M/H)**2*x1+(g/H)/np.sqrt(2)*(f1*f1-f2*f2),
        (M/H)**2*x2+c*f1*f2]).T/3
for j in range(round(duration/dt)):
    n1=rng.standard_normal(fine.shape)*np.sqrt(dt/2)/(2*np.pi)
    n2=rng.standard_normal(fine.shape)*np.sqrt(dt/2)/(2*np.pi)
    coarse+=dt*drift(coarse)+n1+n2
    fine+=dt/2*drift(fine)+n1
    fine+=dt/2*drift(fine)+n2
def stats(z):
    phi2=np.sum(z[:,:2]**2,axis=1)/2;x2=np.sum(z[:,2:]**2,axis=1)/2
    return dict(phi_variance=float(np.mean(phi2)),X_variance=float(np.mean(x2)),
        X_variance_sem=float(np.std(x2,ddof=1)/np.sqrt(patches)),
        phi_variance_sem=float(np.std(phi2,ddof=1)/np.sqrt(patches)),
        X_amplitude_quantiles_GeV=(H*np.sqrt(np.quantile(x2,[.1,.5,.9]))).tolist(),
        phi_quartic_energy_per_H4=float(lam*np.mean(phi2**2)),
        X_above_tachyon_threshold_fraction=float(np.mean(H*np.sqrt(x2)>m*m/(2*g))))
a,b=stats(coarse),stats(fine);expected_X=duration/(4*np.pi**2)
expected_phi=np.sqrt(3)/(2*np.sqrt(2)*np.pi**1.5*np.sqrt(lam))
checks=dict(grid_refinement=abs(a['phi_variance']/b['phi_variance']-1)<.005,
    free_X_variance=abs(b['X_variance']-expected_X)<5*b['X_variance_sem'],
    finite=bool(np.isfinite(fine).all()))
out=dict(checks=checks,all_pass=all(checks.values()),H_inf_GeV=H,N_e=duration,patches=patches,
    coarse=a,fine=b,free_X_expected_variance=expected_X,asymptotic_phi_expected_variance=expected_phi,
    final_field_samples_over_H=fine.tolist(),
    scope='Leading stochastic light-field approximation, imposed de Sitter history and 60 e-folds; fields only, no conjugate momenta, local charge, particle yield, conversion or galaxy formation claim.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='final_field_samples_over_H'},indent=2));sys.exit(0 if out['all_pass'] else 1)
