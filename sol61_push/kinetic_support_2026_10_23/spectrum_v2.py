import numpy as np
from scipy.linalg import eigh,null_space
from equilibrium import solve

def modes(sol,K,R=24,n=400,lmax=8):
 edges=np.linspace(0,R,n+1);dr=R/n;r=(edges[:-1]+edges[1:])/2;w=np.diff(edges**3)/3;s=np.sqrt(w);v=sol.sol(r);rho=np.maximum((sol.p[0]-v[0]-v[2])/(2.5*K),0)**1.5;mask=rho>max(rho)*1e-7;ix=np.where(mask)[0];h=v[2];chi=v[4];P=sol.sol(edges[1:-1])[3];at=1-abs(v[3]);ar=(1-abs(P))**2
 def op(l,coef,potential,outer):
  L=np.diag(potential.copy());k=edges[1:-1]**2*coef/dr
  for j in range(n-1):
   L[j,j]+=k[j]/w[j];L[j+1,j+1]+=k[j]/w[j+1];L[j,j+1]-=k[j]/np.sqrt(w[j]*w[j+1]);L[j+1,j]-=k[j]/np.sqrt(w[j]*w[j+1])
  # Robin evaluated across half cell using linear face extrapolation.
  L[-1,-1]+=R*R*outer/(1+outer*dr/2)/w[-1]
  return L
 results=[]
 for l in range(lmax+1):
  q=l*(l+1)/r**2;G=op(l,np.ones(n-1),q,(l+1)/R)
  # At large R use exact decaying modified-spherical-Bessel logarithmic derivatives.
  from scipy.special import spherical_kn
  bh=-spherical_kn(l,R,derivative=True)/spherical_kn(l,R)
  bc=-.2*spherical_kn(l,.2*R,derivative=True)/spherical_kn(l,.2*R)
  B=op(l,np.ones(n-1)*.125,.005+.125*q,bc)*1 # outer coefficient must carry d
  # op's outer flux assumed coefficient1: repair d for B.
  B[-1,-1]-=.875*R*R*bc/(1+bc*dr/2)/w[-1]
  H=op(l,ar,chi+at*q,bh)+h[:,None]*np.linalg.solve(B,np.diag(h))
  unit=np.eye(n)[:,ix];response=np.linalg.solve(H,unit)-np.linalg.solve(G,unit);D=(5/3)*K*rho[ix]**(-1/3)
  Hess=np.diag(D)+response[ix,:];Hess=(Hess+Hess.T)/2
  if l==0:
   Z=null_space(s[ix][None,:]);Hess=Z.T@Hess@Z
  vals,vec=eigh(Hess,subset_by_index=[0,min(3,len(Hess)-1)])
  record=dict(l=l,eigenvalues=vals.tolist())
  if l==1:
   drho=-1.5*np.sqrt(np.maximum((sol.p[0]-v[0]-v[2])/(2.5*K),0))/(2.5*K)*(v[1]-v[3]/(1-abs(v[3])))
   trans=drho[ix]*s[ix];trans/=np.linalg.norm(trans);record['translation_overlap']=float(abs(trans@vec[:,0]));record['translation_rayleigh']=float(trans@Hess@trans);Z=null_space(trans[None,:]);record['projected_min']=float(eigh(Z.T@Hess@Z,eigvals_only=True,subset_by_index=[0,0])[0])
  results.append(record)
 Dmin=float(min((5/3)*K*rho[ix]**(-1/3)));rmax=float(r[ix[-1]]+dr/2)
 return dict(n=n,R=R,cells_in_matter=len(ix),modes=results,Dmin=Dmin,support_grid_radius=rmax,all_l_above_sufficient_bound=float(rmax*rmax/Dmin),bound_statement='l(l+1)>support_radius^2/Dmin implies positive density Hessian from kinetic minus gravity alone')
