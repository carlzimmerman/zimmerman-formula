"""Local nodal-ring fermion toy: cubic determinant and IR rounding."""
from pathlib import Path
import json, math
import numpy as np
from scipy.integrate import quad
from scipy.special import expit
P=Path(__file__).parent
sx=np.array([[0,1],[1,0]],complex);sy=np.array([[0,-1j],[1j,0]]);sz=np.diag([1.,-1.]); eye=np.eye(2)
gam=[np.kron(sx,eye),np.kron(sz,eye),np.kron(sy,sx),np.kron(sy,sy),np.kron(sy,sz)]
checks={}
for i in range(5):
 for j in range(5):
  checks[f'clifford_{i}_{j}']=bool(np.max(abs(gam[i]@gam[j]+gam[j]@gam[i]-2*(i==j)*np.eye(4)))<1e-13)
for k in [(2.,0.,0.),(1.,.5,.2),(0.,0.,1.)]:
 for pol in [(0.,0.,0.),(.1,.2,.3),(.3,-.1,.2)]:
  d=(k[0]**2+k[1]**2-4)/2
  H=d*gam[0]+k[2]*gam[1]+sum(pol[j]*gam[j+2] for j in range(3))
  E=math.sqrt(d*d+k[2]**2+sum(t*t for t in pol))
  checks[f'spectrum_{k}_{pol}']=bool(np.max(abs(np.linalg.eigvalsh(H)-np.array([-E,-E,E,E])))<1e-12)
# Divide potential by A=N*m_star/(2*pi*v). Delta is fermion gap.
cubic=[]
for delta in [.1,1.,2.]:
 for ratio in [10.,100.,1000.]:
  cutoff=ratio*delta
  integrand=lambda q:delta**4/(2*(math.hypot(q,delta)+q)**2)
  val=quad(integrand,0,cutoff,epsabs=1e-12,epsrel=1e-11)[0]
  # Differentiate the original cutoff band energy with analytic quadratic subtraction.
  derivative=delta*(delta-delta**2/(math.hypot(cutoff,delta)+cutoff))
  step=1e-4*delta
  def potential(m):return quad(lambda q:m**4/(2*(math.hypot(q,m)+q)**2),0,cutoff,epsabs=1e-12)[0]
  diff=(potential(delta+step)-potential(delta-step))/(2*step)
  checks[f'derivative_{delta}_{ratio}']=abs(diff/derivative-1)<1e-7
  checks[f'cubic_limit_{delta}_{ratio}']=abs(val/delta**3-1/3)<.13/ratio
  cubic.append(dict(gap=delta,cutoff_over_gap=ratio,cubic_over_A=val/delta**3))
thermal=[]
for x in [.01,.1,1.,3.,10.,30.]:
 # T=1, delta=x. At mu=0 both particles and holes contribute.
 delta=x
 numeric=delta**2+2*delta*quad(lambda E:expit(-E),delta,np.inf,epsabs=1e-12)[0]
 analytic=delta**2+2*delta*np.logaddexp(0.,-delta)
 checks[f'thermal_{x}']=abs(numeric/analytic-1)<1e-11
 thermal.append(dict(gap_over_T=x,force_over_zero_T=float(analytic/delta**2)))
doped=[]
for delta in [.01,.1,.5,1.,2.]:
 mu=1.
 correction=0 if delta>=mu else delta*quad(lambda E:1.,delta,mu)[0]
 derivative=delta**2+correction
 checks[f'chemical_potential_{delta}']=abs(derivative-delta*max(delta,mu))<1e-12
 doped.append(dict(gap_over_mu=delta,force_over_zero_mu=derivative/delta**2))
result=dict(checks=checks,all_pass=all(checks.values()),cubic=cubic,thermal=thermal,doped=doped,
 conventions='hbar=1; N counts negative-energy bands (N=2 for 4x4 Hamiltonian); A=N*m_star/(2*pi*v); subtract analytic quadratic at zero T and mu.',
 non_claims=['No cosmological realization of nodal-ring medium','No symmetry enforcing critical quadratic coefficient','No gradient or dynamical determinant computed','No prediction of vacuum density','No observational evidence for this dark medium'])
(P/'nodal_ring_run'/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(all_pass=result['all_pass'],checks=len(checks),cubic=cubic,thermal=thermal,doped=doped),indent=2))
assert result['all_pass']
