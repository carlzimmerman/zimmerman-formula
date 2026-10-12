"""Positive operator identity for a regulated number-conserving NR carrier."""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
p=Path(__file__).parent
par=json.loads((p/'detuned_carrier_run/results.json').read_text())['parameters']
m=par['m_eV'];M=par['M_eV'];g=par['cubic_g_eV'];lam=par['lambda_'];gap=4*m*m*par['u']**2/(M+2*m)
cubic=g/(2*m*math.sqrt(2*M));quartic=lam/(4*m*m)
residual=quartic-cubic*cubic/gap
# A two-cell regulator chosen to make dimensionless conversion 0.4.
volume=(cubic/(.4*gap))**2;C=cubic/(gap*math.sqrt(volume));K=quartic/(gap*volume)
def basis(Q):
 return [(a0,a1,b0,b1) for a0 in range(Q+1) for a1 in range(Q+1-a0) for b0 in range((Q-a0-a1)//2+1) for b1 in range((Q-a0-a1)//2+1) if a0+a1+2*(b0+b1)==Q]
def lower(src,dst,mode,power=1):
 lookup={s:i for i,s in enumerate(dst)};A=np.zeros((len(dst),len(src)))
 for j,s in enumerate(src):
  if s[mode]<power:continue
  v=list(s);v[mode]-=power;fac=math.sqrt(math.prod(range(s[mode]-power+1,s[mode]+1)))
  A[lookup[tuple(v)],j]=fac
 return A
checks=[]
def check(n,err,tol):checks.append(dict(name=n,error=float(err),passed=bool(abs(err)<tol)))
check('positive residual',min(0,residual),1e-30)
rows=[]
for Q in [2,4,6,8,10]:
 bs=basis(Q);low1=basis(Q-1);low2=basis(Q-2)
 A=[lower(bs,low1,j) for j in [0,1]]
 B=[lower(bs,low2,j) for j in [2,3]]
 AA=[lower(bs,low2,j,2) for j in [0,1]]
 T=.07*(A[0]-A[1]).T@(A[0]-A[1])+.035*(B[0]-B[1]).T@(B[0]-B[1])
 H=T.copy();positive=T.copy()
 for j in [0,1]:
  H+=B[j].T@B[j]+C*(B[j].T@AA[j]+AA[j].T@B[j])+K*AA[j].T@AA[j]
  D=B[j]+C*AA[j];positive+=D.T@D+(K-C*C)*AA[j].T@AA[j]
 check('square identity Q'+str(Q),np.max(abs(H-positive)),1e-12)
 values,vectors=eigh(H)
 check('positive Hamiltonian Q'+str(Q),min(0,float(values.min())),1e-12)
 initial=np.zeros(len(bs));Ns=Q//2
 for j,(a0,a1,b0,b1) in enumerate(bs):
  if a0+a1==0:initial[j]=math.sqrt(math.comb(Ns,b0)/2**Ns)
 times=np.linspace(0,100,501);state=vectors@((vectors.T@initial)[:,None]*np.exp(-1j*values[:,None]*times))
 energy=np.einsum('it,ij,jt->t',state.conj(),H,state).real
 kinetic=np.einsum('it,ij,jt->t',state.conj(),T,state).real
 daughter=np.array([s[0]+s[1] for s in bs])@abs(state)**2/Q
 check('source initial excess Q'+str(Q),energy[0]-Ns,1e-12)
 check('energy conservation Q'+str(Q),max(abs(energy-energy[0])),1e-10)
 check('kinetic bound Q'+str(Q),max(0,float(max(kinetic-energy))),1e-10)
 rows.append(dict(Q=Q,dimension=len(bs),minimum_excess_eigenvalue_in_gap_units=float(values.min()),maximum_daughter_charge_fraction=float(max(daughter)),maximum_kinetic_over_initial_excess=float(max(kinetic)/Ns),endpoint_daughter_fraction=float(daughter[-1])))
out=dict(parameters=par,NR_coefficients=dict(gap_eV=gap,cubic=cubic,quartic=quartic,positive_quartic_residual=residual,regulator_cell_volume_eV_minus3=volume,dimensionless_cubic=C,dimensionless_quartic=K),rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),initial_excess_over_mQ=gap/(2*m),charge_weighted_rms_velocity_bound_over_c=math.sqrt(gap/m),non_claims=['Regulated leading NR Hamiltonian, not renormalized relativistic QFT','Two-cell evolution checks algebra and spontaneous quantum conversion only; not production yield or spatial continuum dynamics','Kinetic-energy bound is not a full pressure, sound-speed, transport or halo-law bound','Source charge and energy prescribed'])
(p/'nr_quantum_bound_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
