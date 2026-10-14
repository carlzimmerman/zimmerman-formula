"""Fixed-Q current sum rule diagnostic; not a bound along a varying-Q curve."""
import json, sys, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
prior=json.loads(Path('sol61_push/phonon_current_source_2026_10_14/run/results.json').read_text())
a=prior['assumptions']; mr=a['MR_eV']; checks=[]
def ck(name,error,tol):
    assert error<=tol,(name,error,tol)
    checks.append(dict(name=name,error=float(error),tolerance=tol))
# Orthogonal tensor-factor operators commute exactly in the finite surrogate.
# Sum all final-state squared amplitudes independently as column norms.
N=18
lower=np.diag(np.sqrt(np.arange(1,N)),1)
x=(lower+lower.T)/math.sqrt(2)
p=1j*(lower.T-lower)/math.sqrt(2)
for q in [.1,1.,3.]:
    U=expm(1j*q*x)
    ck('unitarity',np.max(abs(U.conj().T@U-np.eye(N))),2e-14)
    for i,j in [(0,0),(2,3),(5,8)]:
        amp=np.outer(U[:,i],p[:,j])
        summed=float(np.sum(abs(amp)**2))
        moment=float(np.vdot(p[:,j],p[:,j]).real)
        ck('complete_transverse_strength',abs(summed-moment),2e-13)
        ck('harmonic_momentum_moment',abs(moment-(j+.5)),2e-14)
# Kinematic coefficient at P=0 for nonnegative excitation energy.
# W(delta)/W(0)=(1+x)/(1+2x)^2 <= 1 for x=delta/mr>=0.
for xval in [0.,1e-10,1e-5,.1,1.,100.]:
    w=(1+xval)/(1+2*xval)**2
    ck('excitation_kernel_ceiling',max(0.,w-1),0.)
    ck('ceiling_gap_identity',abs(((1+2*xval)**2-(1+xval))-(3*xval+4*xval*xval)),1e-10)
# A normalized response at each q does not bound its sampled diagonal by 1.
# Eight very narrow positive peaks over a tiny relative momentum interval.
qvals=1.+np.arange(8)*1e-6
response=np.exp(-.5*((qvals[:,None]-qvals[None,:])/1e-7)**2)
response/=response.sum(axis=0)
ck('response_column_normalization',np.max(abs(response.sum(axis=0)-1)),1e-15)
diagonal=float(np.trace(response))
assert diagonal>7.99
# This is an abstract response-family counterexample, not a realizable target.
alpha=1/137.035999084; hc=1.973269804e-7
speak=a['photon_flux_per_s']/(math.sqrt(2*math.pi)*a['photon_RMS_eV'])
C=a['column_per_m2']*hc**2*a['branching']*speak*alpha*a['g_per_eV']**2*a['Z']**2/(8*math.pi*mr**2)*prior['acceptance_volume_eV3']
# Vperp2 is sum of the two transverse velocity variances, in units of c^2.
for row in prior['rows']:
    frozen=C*row['omega_eV']/a['M_eV']
    ck('harmonic_leading_recovery',abs(frozen/row['leading_transverse_pairs_per_s']-1),1e-14)
# Finite-P purely kinematic upper envelope, excluding response Q-dependence.
pmax=2*math.sqrt(.02-.002)
b=math.sqrt(mr*mr+pmax*pmax)-pmax
# For E>=mr, P<=pmax, -t=2 omega(E-Pu)-mr^2.
# The report uses only the exact P=0 proof; no full finite-P inequality asserted.
result=dict(coefficient_pairs_per_s_per_Vperp2=C,
    nonrel_velocity_diagnostic=dict(Vperp2=1e-4,rate_pairs_per_s=C*1e-4),
    required_Vperp2_for_one_pair_per_year=1/(365.25*86400*C),
    abstract_varying_Q_diagonal=diagonal,
    checks=checks,passed=len(checks),
    scope='Frozen-Q, leading-small-P strength diagnostic; not a physical all-target bound')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
