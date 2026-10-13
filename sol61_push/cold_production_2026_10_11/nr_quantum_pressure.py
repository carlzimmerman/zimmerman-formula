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
def check(n,e,tol):checks.append(dict(name=n,error=float(e),passed=bool(abs(e)<tol)))
r2=cubic*cubic/(gap*quartic)
bminus=(1-1/math.sqrt(1-r2))/2;bplus=(1+1/math.sqrt(1-r2))/2
rows=[]
for Q in [2,4,6,8,10]:
 bs=basis(Q);low1=basis(Q-1);low2=basis(Q-2)
 A=[lower(bs,low1,j) for j in [0,1]];B=[lower(bs,low2,j) for j in [2,3]];AA=[lower(bs,low2,j,2) for j in [0,1]]
 T0=.07*(A[0]-A[1]).T@(A[0]-A[1])+.035*(B[0]-B[1]).T@(B[0]-B[1])
 X=sum(b.T@b for b in B);W0=sum(C*(b.T@aa+aa.T@b) for b,aa in zip(B,AA));Y0=sum(K*aa.T@aa for aa in AA)
 for a in [.1,1.,10.,1e3]:
  T=T0/a**2;W=W0/a**1.5;Y=Y0/a**3;D=T+X+W+Y;PV=2*T/3+W/2+Y
  for name,mat in [('pressure upper',bplus*D-PV),('pressure lower',PV-bminus*D),('charge lower',PV+r2*Q/8*np.eye(len(bs)))]:
   err=min(0,float(np.linalg.eigvalsh(mat).min()));check(name+str((Q,a)),err,1e-8)
  step=1e-5
  energy=lambda l:T0*np.exp(-2*l)+X+W0*np.exp(-1.5*l)+Y0*np.exp(-3*l)
  num=-(energy(math.log(a)+step)-energy(math.log(a)-step))/(6*step)
  check('volume derivative '+str((Q,a)),np.max(abs(num-PV))/max(1,np.max(abs(PV))),1e-8)
 rows.append(dict(Q=Q,dimension=len(bs)))
ratios=[1,10,1e3,1e6]
d0=gap/(2*m);history=[]
for a in ratios:
 dmax=d0+3*r2*gap/(8*m)*math.log(a)
 history.append(dict(expansion_ratio=a,excess_over_mQ_upper=dmax,absolute_pressure_over_total_density_upper=bplus*dmax/(1+dmax),rms_speed_over_c_upper=math.sqrt(2*dmax)))
out=dict(r_squared=r2,beta_minus=bminus,beta_plus=bplus,rows=rows,expansion_bounds=history,checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['Regulated NR Hamiltonian with prescribed homogeneous monotonic expansion','Not a renormalized relativistic theorem or a guarantee of small sound speed','Global pressure and kinetic moments only; no halo or structure formation prediction','Upper bounds not predicted realized values'])
(p/'nr_quantum_pressure_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
