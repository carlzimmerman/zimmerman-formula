"""Local WKB pure-T cubic vertex of a stated 3D continuation of radial energy."""
import numpy as np

def dispersion(k,rho,u,kappa):
 k=np.asarray(k);ks=k@k;parallel=1/(1-u)**2;transverse=1/(1-u);direction=k[2]**2/ks
 return np.sqrt(rho*((transverse-1)+(parallel-transverse)*direction)+kappa*ks*ks/4)
def vertex(k1,k2,rho,u,kappa,volume):
 ks=[np.asarray(k1),np.asarray(k2),np.asarray(k1)+np.asarray(k2)];om=np.array([dispersion(v,rho,u,kappa) for v in ks]);k2s=np.array([v@v for v in ks]);A=np.sqrt(rho*k2s/(2*om));B=np.sqrt(om/(2*rho*k2s));d12=ks[0]@ks[1];d13=ks[0]@ks[2];d23=ks[1]@ks[2];vel=A[0]*B[1]*B[2]*d23+A[1]*B[0]*B[2]*d13+A[2]*B[0]*B[1]*d12;quant=-kappa/(4*rho*rho)*np.prod(A)*(d23+d13-d12)
 C1=(3*u-1)/(1-u)**3;C2=1/(1-u)**2;z=[v[2] for v in ks];C=C1*np.prod(z)+C2*(z[0]*d23+z[1]*d13+z[2]*d12);response=-1j*C*np.prod(A)/np.prod(k2s)
 return {'omega':om,'A':A,'V':(vel+quant+response)/np.sqrt(volume),'V_velocity':vel/np.sqrt(volume),'V_quantum':quant/np.sqrt(volume),'V_response':response/np.sqrt(volume)}
def equal_resonance(q,rho,u,kappa):
 gap=rho*(1/(1-u)-1);a=kappa/4;s4=3*gap/a+4*q**4;cos=np.sqrt(s4)/(2*q*q)-1
 if cos>1+1e-12:return None
 cos=np.clip(cos,-1,1);return np.array([q,0.,0.]),np.array([q*cos,q*np.sqrt(1-cos*cos),0.])
