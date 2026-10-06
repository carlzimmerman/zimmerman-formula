"""Exact exterior ODE copied from frozen integrate.py; importable helper."""
import math
K=H=1.
def response(gs,A):
 g=abs(gs);ss=math.hypot(g,A/2);wg=g*g/(ss+A/2);wgg=g/ss
 ug=2*K*(gs-math.copysign(wg,gs))
 if g/A<1e-3: leg=2*g**3/(3*A)-4*g**5/(5*A**3)+12*g**7/(7*A**5)
 else:leg=(g*ss-A*A/4*math.asinh(2*g/A))/2
 pressure=2*K*(leg-g*g/2);u=pressure+gs*ug
 return u,ug,2*K*(1-wgg),pressure,wg

def equations(r,y,eta,A):
 N=math.exp(y[0]);B=math.exp(y[1]);w=y[2];kk=y[3];V=-w*H*r*N;P=N*kk/r;c=3*K*eta*H*H;b=2*K*eta*H;veff=3*K*H*H
 gs=P/(N*B);u,ug,ugg,press,wg=response(gs,A);S=2*c*math.log(N)-veff+u
 BP=B*(-P/N-b*r*P/(2*K*V))
 VP=N/(2*K*r*V)*(-K*(N-(N+2*r*P)/B**2+V*V/N-2*r*V*V*P/N**2)-N*r*r*(S-gs*ug)+b*r*r*V*P/N)
 T=2*B*r*V*VP+2*r*BP*V*V+B*V*V
 ENrest=K*(B-1/B+2*r*BP/B**2+T/N**2)+B*r*r*(S+2*c-gs*ug)+b*B*r*r*(VP+BP/B*V+2*V/r)/N
 PP=N*B/(r*r*ugg)*(ENrest-2*r*ug+r*r*ugg*gs*(P/N+BP/B))
 derivative=[kk,r*BP/B,w*(r*VP/V-1-kk),kk+r*r*PP/N-kk*kk]
 gp=PP/(N*B)-gs*(P/N+BP/B)
 # Independent stationary current, not copied from the EL residual combination.
 jrq=b*(P/B**2-3*H*V-V/N*(VP+(BP/B+2/r)*V))+V/(B*r*r)*(2*r*ug+r*r*ugg*gp)
 F=N*N-B*B*V*V
 Fp=2*N*P-2*B*BP*V*V-2*B*B*V*VP
 circspeed=r*Fp/(2*F)
 return derivative,dict(N=N,B=B,w=w,k=kk,V=V,gclock=abs(gs),Wg=wg,F=F,circular_speed2=circspeed,qjr=jrq,theta_over_3H=-(VP+BP/B*V+2*V/r)/(3*H*N),Ugg=ugg,proposed_flux_ratio=wg*r*r)
