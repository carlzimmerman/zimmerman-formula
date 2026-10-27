"""Fixed-charge radial amplitude Hessian after local response minimization.
Finite discretized static test only; all angular/dynamic claims excluded.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import simpson
from scipy.sparse.linalg import LinearOperator,eigsh
out=Path(sys.argv[1]);assert out.is_dir();base=Path(__file__).parent
parent=base/'phase_interface_probe_run_001';data=json.loads((parent/'results.json').read_text())
checks=[];runs=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
for row in data['runs']:
 if row['refinement']!=2:continue
 R=row['R_initial_guess'];source=row['source_strength'];omega=row['omega']
 profile=np.load(parent/('profile_R'+str(int(R))+'_S'+str(source)+'.npz'))
 spline=CubicSpline(profile['r'],profile['f']);L=float(profile['r'][-1]);I=4*math.pi*simpson(profile['r']**2*profile['f']**2,x=profile['r'])
 for nodes in (800,1600):
  dr=L/(nodes+1);r=np.arange(1,nodes+1)*dr;f=spline(r);s=f*f/.5
  K=.1*(1-s)**2;B=s;D=source*r/(1+r*r)**1.5
  p=2*D/(K+np.sqrt(K*K+4*B*D)+1e-300)
  sf=4*f;Ws=.1*(s-1)*p*p+p**3/3
  Wff=.1*p*p*sf*sf+4*Ws
  Wfp=(.2*(s-1)*p+p*p)*sf;Wpp=K+2*B*p
  local=Wff-np.divide(Wfp*Wfp,Wpp,out=np.zeros_like(Wfp),where=Wpp>1e-250)
  U=2-12*f*f+30*f**4-2*omega**2+local
  diagonal=4/dr**2+U;off=-2/dr**2;u=r*f;rank=32*math.pi*omega**2/I*dr
  def mv(v):
   w=diagonal*v+rank*u*np.dot(u,v);w[1:]+=off*v[:-1];w[:-1]+=off*v[1:];return w
  operator=LinearOperator((nodes,nodes),matvec=mv,dtype=float)
  eigen,vec=eigsh(operator,k=3,which='SA',tol=1e-9,maxiter=20000,v0=np.sin(math.pi*r/L))
  order=np.argsort(eigen);eigen=eigen[order];vec=vec[:,order]
  residuals=[float(np.linalg.norm(mv(vec[:,i])-eigen[i]*vec[:,i])) for i in range(3)]
  check('eigenvector residual '+str((R,source,nodes)),max(residuals)<1e-7)
  # Positivity is retained as a scientific flag, not a forced assertion.
  runs.append({'R_initial_guess':R,'source_strength':source,'nodes':nodes,'dr':dr,'lowest_three_eigenvalues':eigen.tolist(),'max_absolute_eigen_residual':max(residuals),'positive_sampled_radial_curvature':bool(eigen[0]>0)})
# Coupling dictionary/tradeoff is structural, not a fitted gravity comparison.
result={'runs':runs,'checks':checks,'Newtonian_dictionary':{'C':1,'K0':.1,'exterior_to_interior_bare_scalar_inverse_square_coefficient':11.,'exterior_extra_relative_to_bare_scalar':10.,'tradeoff':'K0>1/(C eta) to suppress exterior scalar enhancement below eta; finite droplet core shifts s-1~1/R in selected units, giving interior quadratic/cubic ratio~K0/(sqrt(beta source) R). Conditional thin-wall estimate.'},'non_claims':['No continuum spectral certificate, angular stability, P kinetic action/hyperbolicity, nonlinear/quantum stability or actual GR solution','Host-only free-particle binding is not proof of full sourced stability','Selected sextic/switching functions and charge inventory are new inputs']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
