"""Exact linear Newton-gauge ideal-fluid closure on pinned homogeneous action.
No microscopic photon transport or cold identity assertion. x=ln a, M=1.
"""
import importlib.util,pathlib
import numpy as np
parent=pathlib.Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('audited_homogeneous_equations',parent/'equations.py');bg=importlib.util.module_from_spec(spec);spec.loader.exec_module(bg)

def rows(x,b,z,xi,k,drop_trace=False):
 c1,c2,q1,q2,_=b;dc1,dc2,dq1,dq2,Phi,dd,vd,dr,vr=z
 u=bg.quantities(x,b,xi);F=u['F'];fd=u['Fdot'];H=u['H'];R=u['R'];E=u['E'];rd=u['rho_d'];rr=u['rho_r'];p2=k*k*np.exp(-2*x)
 df=2*(c1*dc1+c2*dc2);dF=-2*xi*df;dFd=-4*xi*(q1*dc1+q2*dc2+c1*dq1+c2*dq2)
 Psi=Phi-dF/F;dE=2*(q1*dq1+q2*dq2)-2*Psi*E
 density=rd*dd+rr*dr+dE;momentum=rd*vd+4*rr*vr/3-2*(q1*dc1+q2*dc2)
 Z=(-momentum+dFd-H*dF-fd*Psi)/(2*F);Pdot=Z-H*Psi
 Psidot=Pdot-dFd/F+dF*fd/(F*F)
 dB=(12*xi*xi-2*xi)*df;dR=(rd*dd+2*(6*xi-1)*dE-R*dB)/u['B']
 if drop_trace:dR=0*dR
 C00=2*F*p2*Phi+6*F*H*Z+density-(p2+3*H*H)*dF-3*H*dFd+3*fd*Pdot+6*H*fd*Psi
 W=(Phi+Psi)/2
 CW=2*F*p2*W+density-3*H*momentum-6*H*H*dF+3*fd*Z
 dqd1=-3*H*dq1-(p2+xi*R)*dc1+q1*(Psidot+3*Pdot)-2*xi*R*c1*Psi-xi*c1*dR
 dqd2=-3*H*dq2-(p2+xi*R)*dc2+q2*(Psidot+3*Pdot)-2*xi*R*c2*Psi-xi*c2*dR
 dz=np.array([dq1,dq2,dqd1,dqd2,Pdot,3*Pdot+p2*vd,-Psi,4*Pdot+4*p2*vr/3,H*vr-Psi-dr/4])
 scale=abs(2*F*p2*Phi)+abs(density)+abs(3*H*momentum)+abs(6*H*H*dF)+abs(3*fd*Z)
 return {'background':u,'dzdt':dz,'Phi':Phi,'Psi':Psi,'W':W,'deltaF':dF,'deltaFdot':dFd,'deltaE':dE,'deltaq':momentum,'deltarho':density,'deltaR':dR,'Phi_dot':Pdot,'Z':Z,'C00':C00,'CW':CW,'constraint_scale':scale,'dust_comoving':dd-3*H*vd,'p2':p2}

def rhs(x,y,xi,k,drop_trace=False):
 b=y[:5];z=y[5:];u=rows(x,b,z,xi,k,drop_trace)
 return np.concatenate([bg.rhs(x,b,xi),u['dzdt']/u['background']['H']])

def initial(xi,k,mode,dust_only=False):
 b=bg.initial(xi);u=bg.quantities(0,b,xi);H=u['H'];F=u['F'];fd=u['Fdot'];E=u['E'];L=b[0]*b[3]-b[1]*b[2]
 z=np.zeros(9);omega=H
 if mode=='phase':z[2]=-b[1]*omega;z[3]=b[0]*omega;source=2*L*omega
 elif mode=='dust':z[5]=1;source=u['rho_d']
 else:raise ValueError(mode)
 den=2*F*k*k-2*E-3*fd*fd/(2*F)
 if den<=0:raise ValueError('initial constraint denominator not positive')
 z[4]=0 if (dust_only and mode=='phase') else -source/den
 return np.concatenate([b,z]),{'omega':omega,'L':L,'denominator':den,'source':source}
