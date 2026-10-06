"""Actual homogeneous nonminimal complex carrier+dust+radiation; x=ln(a), M=1.
State(Rechi,Imchi,Rechidot,Imchidot,elapsedproper_time). No radiation R0 prescription.
"""
import numpy as np
RD0=4/3;RR0=.01*RD0

def quantities(x,y,xi,M=1.):
 cr,ci,qr,qi,_=y;f=cr*cr+ci*ci;D=cr*qr+ci*qi;E=qr*qr+qi*qi;F=M-2*xi*f;fd=-4*xi*D;B=F+12*xi*xi*f
 rd=RD0*np.exp(-3*x);rr=RR0*np.exp(-4*x);tot=rd+rr+E;disc=np.sqrt(fd*fd+4*F*tot/3)
 H=(2*tot/(3*(disc+fd))) if np.real(fd)>=0 else (-fd+disc)/(2*F)
 R=(rd+2*(6*xi-1)*E)/B;hd=R/6-2*H*H
 Q=np.exp(3*x)*(cr*qi-ci*qr);constraint=3*F*H*H+3*fd*H-tot
 return {'f':f,'D':D,'E':E,'F':F,'Fdot':fd,'B':B,'H':H,'R':R,'Hdot_trace':hd,'rho_d':rd,'rho_r':rr,'Q':Q,'friedmann':constraint,'friedmann_scale':3*abs(F*H*H)+3*abs(fd*H)+abs(tot),'rho_carrier':3*M*H*H-rd-rr,'p_carrier':-M*(2*hd+3*H*H)-rr/3}

def rhs(x,y,xi):
 z=quantities(x,y,xi);cr,ci,qr,qi,_=y;H=z['H'];R=z['R']
 return np.array([qr/H,qi/H,-3*qr-xi*R*cr/H,-3*qi-xi*R*ci/H,1/H])

def initial(xi,S=.4):
 f=S/(8*xi**2);amp=np.sqrt(f);omega=np.sqrt(4*xi/3-.25)
 return np.array([amp,0.,-.5*amp,omega*amp,0.])

def geometric_R_complex_step(x,y,xi):
 # Differentiate solvedconstraintH along actualrhs, independentlyof traceHdot formula.
 dy=rhs(x,y,xi);eps=1e-22
 dHdx=np.imag(quantities(x+1j*eps,np.array(y,dtype=complex)+1j*eps*dy,xi)['H'])/eps
 H=quantities(x,y,xi)['H'];return 6*(H*dHdx+2*H*H)
