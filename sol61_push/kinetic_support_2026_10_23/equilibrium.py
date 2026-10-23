import numpy as np
from scipy.integrate import solve_bvp,simpson

def solve(M=.08408132497418408,K=.05,R=24,n=600,tol=1e-6,guess=None):
 r=np.linspace(0,R,n);a=max(.4,5*K/M**(1/3))
 if guess is None:
  phi=-M/np.sqrt(r*r+a*a);g=M*r/(r*r+a*a)**1.5;h=.2*M*np.exp(-r)/max(a,1);P=.2*M*r*np.exp(-r)/max(a,1);chi=1+M*M*np.exp(-.2*r);z=-.2*(chi-1)*r/(r+1)
  y=np.array([phi,g,h,P,chi,z]);mu=np.array([-M/(2*a)])
 else:y=guess.sol(r);mu=guess.p
 def fun(r,y,p):
  phi,g,h,P,c,z=y;rho=np.maximum((p[0]-phi-h)/(2.5*K),0)**1.5
  return np.array([g,rho,-P/np.maximum(1-abs(P),1e-4),rho-c*h,z,(.005*(c-1)-.5*h*h)/.125])
 def bc(l,b,p):return np.array([l[1],l[3],l[5],b[0]+R*b[1],R*R*b[1]-M,b[3]/(1-abs(b[3]))-(1+1/R)*b[2],b[5]+(.2+1/R)*(b[4]-1)])
 S=np.zeros((6,6));S[1,1]=S[3,3]=S[5,5]=-2
 sol=solve_bvp(fun,bc,r,y,p=mu,S=S,tol=tol,max_nodes=20000)
 rr=np.linspace(0,R,4097);v=sol.sol(rr);rho=np.maximum((sol.p[0]-v[0]-v[2])/(2.5*K),0)**1.5;mass=simpson(rho*rr*rr,x=rr);cum=np.cumsum((rho*rr*rr)[:-1]+(rho*rr*rr)[1:])*(rr[1]-rr[0])/2;cum=np.r_[0,cum];r50=np.interp(.5*M,cum,rr)
 result=dict(M=M,K=K,R=R,tol=tol,success=bool(sol.success),message=sol.message,residual=float(max(sol.rms_residuals)),mu=float(sol.p[0]),mass=float(mass),mass_error=float(abs(mass/M-1)),r50=float(r50),edge=float(rr[np.where(rho>rho.max()*1e-8)[0][-1]]) if max(rho)>0 else 0.,rho0=float(rho[0]),Pmax=float(max(abs(v[3]))),chi0=float(v[4,0]),n_nodes=len(sol.x),r=rr.tolist(),rho=rho.tolist(),fields=v.tolist())
 return sol,result
if __name__=='__main__':
 import argparse,json
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--K',type=float,default=.05);p.add_argument('--mass',type=float,default=.08408132497418408);p.add_argument('--R',type=float,default=24);a=p.parse_args();s,r=solve(M=a.mass,K=a.K,R=a.R);json.dump(r,open(a.output,'w'),indent=2);print({k:v for k,v in r.items() if k not in ['r','rho','fields']})
