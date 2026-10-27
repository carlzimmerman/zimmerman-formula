"""Complete cubic quasi-static CC density action, not bare vertex plus damping."""
import itertools
import numpy as np
from vertex import dispersion

def cc_vertex(k1,k2,rho,u,kappa,volume,eta):
 ks=[np.asarray(k1,float),np.asarray(k2,float),np.asarray(k1,float)+np.asarray(k2,float)];om=np.array([dispersion(k,rho,u,kappa) for k in ks])/np.sqrt(1+eta);squares=np.array([k@k for k in ks]);A=np.sqrt(rho*squares/(2*om*(1+eta)));B=om*A/(rho*squares);d12=ks[0]@ks[1];d13=ks[0]@ks[2];d23=ks[1]@ks[2];vel=A[0]*B[1]*B[2]*d23+A[1]*B[0]*B[2]*d13+A[2]*B[0]*B[1]*d12;quant=-kappa*np.prod(A)/(4*rho*rho)*(d23+d13-d12);mom=[ks[0],ks[1],-ks[2]];sign=[1,1,-1];summation=0.
 for i,j,l in itertools.permutations(range(3)):
  summation+=sign[i]*sign[l]*om[i]*om[l]*(2+mom[i]@mom[l]/squares[l])/squares[i]
 added=eta/(rho*rho)*np.prod(A)*summation;z=[k[2] for k in ks];C=(3*u-1)/(1-u)**3*np.prod(z)+1/(1-u)**2*(z[0]*d23+z[1]*d13+z[2]*d12);response=-1j*C*np.prod(A)/np.prod(squares)
 return {'V':(vel+quant+added+response)/np.sqrt(volume),'velocity':vel/np.sqrt(volume),'quantum':quant/np.sqrt(volume),'nonlinear_inertia':added/np.sqrt(volume),'response':response/np.sqrt(volume),'omega':om,'A':A}
