"""Finite-xi Newton-gauge EdS equations, x=log(t/ti), ti=M=1 in numeric control.
State (u,ux,v,vx,delta,wd,Phi), wd=v_d/t, chi=chi0(1+u+iv).
No quasistatic or fixed dust-source approximation. Initial mixed00 constraint required.
"""
import numpy as np

def coefficients(x,xi,A,k,M=1.):
 r=2*A*np.exp(-x);P=k*k*np.exp(2*x/3);F=M-xi*r;B=M+xi*(6*xi-1)*r;w=np.sqrt(4*xi/3-.25)
 return r,P,F,B,w

def quantities(x,y,xi,A,k,M=1.):
 u,U,v,V,d,wd,phi=y;r,P,F,B,w=coefficients(x,xi,A,k,M)
 df=-2*xi*r*u;dfx=-2*xi*r*(U-u);fx=xi*r;psi=phi-df/F
 phix=(-4*M*wd/3+r*(-u/2+w*v)+dfx-2*df/3-(4*F/3+fx)*psi)/(2*F)
 psix=phix-dfx/F+df*fx/F**2
 RR=(4*M*d/3+(1-6*xi)*r*(U-2*w*V+8*xi*psi/3))/B
 C=(4*M-xi*r)*phix+8*M*psi/3+2*F*P*phi-(4/3+P)*df-2*dfx+r*(-U/2+w*V+4*xi*u/3)+4*M*d/3
 return {'r':r,'P':P,'F':F,'B':B,'omega':w,'deltaF':df,'deltaFx':dfx,'Psi':psi,'Phix':phix,'Psix':psix,'t2deltaR':RR,'C00':C,'Weyl':(phi+psi)/2,'density_comoving':d-2*wd}

def rhs(x,y,xi,A,k,M=1.):
 u,U,v,V,d,wd,phi=y;z=quantities(x,y,xi,A,k,M);p=z['P'];w=z['omega'];psi=z['Psi'];phix=z['Phix'];psix=z['Psix']
 return np.array([U,2*w*V-p*u-(psix+3*phix)/2-8*xi*psi/3-xi*z['t2deltaR'],V,-2*w*U-p*v+w*(psix+3*phix),3*phix+p*wd,-psi-wd,phix])

def constrained_initial(xi,A,k,M=1.,delta=1.,phase=0.):
 # GR growing dust velocity seed, no initial radial/phase perturbation except declared phase.
 P=k*k;wd=2*delta/(3*P+4);y=np.array([0.,0.,phase,0.,delta,wd,0.])
 c0=quantities(0.,y,xi,A,k,M)['C00'];y[-1]=1.;c1=quantities(0.,y,xi,A,k,M)['C00']
 y[-1]=-c0/(c1-c0)
 return y
