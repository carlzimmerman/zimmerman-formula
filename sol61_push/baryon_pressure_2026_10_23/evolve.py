import numpy as np
from gas import Radial
def evolve(n=256,amp=.03,zi=1100,zend=10,size=1,cfl=.6):
 m=Radial(n,amp,zi,size);xc=m.x0.copy();xb=m.r+m.baryon_ratio*m.disp;pc=m.Hi*m.disp.copy();pb=pc.copy()*m.baryon_ratio;P,c,res=m.static(xc);eps=1e-4;Pp,cp,rp=m.static(xc+eps*m.disp,np.exp(eps));Pm,cm,rm=m.static(xc-eps*m.disp,np.exp(-eps));Q=m.Hi*(Pp-Pm)/(2*eps);V=m.Hi*(cp-cm)/(2*eps)
 t=m.ti;end=t*((1+zi)/(1+zend))**1.5;A=1;state=m.evaluate(xc,xb,P,c,A,pc,pb,Q,V);E0=state[4];work=0.;rows=[];step=0;nextN=0;maxscale=state[6]['scale'];maxerr=0;reason='endpoint';reflections=0
 try:
  while t<end*(1-1e-12):
   A=(t/m.ti)**(2/3);H=2/(3*t);fc,fb,fP,fchi,E,W,d=state;maxscale=max(maxscale,d['scale']);err=abs(E-E0-work)/max(maxscale,1e-30);maxerr=max(maxerr,err)
   if np.log(A)>=nextN:
    rows.append(dict(z=(1+zi)/A-1,step=step,work_error=err,**d,**m.mass_diagnostics(xc,A)));nextN+=.15
   dt=min(cfl*np.sqrt(m.eta)/np.sqrt(1+6/(A*m.dx)**2),.01/H,end-t);pc+=dt*fc/2;pb+=dt*fb/2;Q+=dt*fP/2;V+=dt*fchi/2;tn=t+dt;An=(tn/m.ti)**(2/3);I2=3*m.ti**(4/3)*(t**(-1/3)-tn**(-1/3));I3=m.ti**2*(1/t-1/tn)
   xc+=pc*I2;xb+=pb*I2
   if min(xb)<=0 or np.any(np.diff(xb)<=0):raise ValueError("gas_shell_crossing")
   for x,v in [(xc,pc),(xb,pb)]:
    neg=x<0;reflections+=int(sum(neg));x[neg]*=-1;v[neg]*=-1
    if max(x)>m.R:raise ValueError('matter_outer_boundary')
   P+=Q*I3;c+=V*I3;mid=m.evaluate(xc,xb,P,c,An,pc,pb,Q,V);pc+=dt*mid[0]/2;pb+=dt*mid[1]/2;Q+=dt*mid[2]/2;V+=dt*mid[3]/2;state=m.evaluate(xc,xb,P,c,An,pc,pb,Q,V);work+=.5*(W+state[5])*np.log(An/A);t=tn;step+=1
 except ValueError as e:reason=str(e)
 A=(t/m.ti)**(2/3);d=state[6];err=abs(state[4]-E0-work)/max(maxscale,d['scale'],1e-30);maxerr=max(maxerr,err);rows.append(dict(z=(1+zi)/A-1,step=step,work_error=err,**d,**m.mass_diagnostics(xc,A)))
 return dict(parameters=dict(n=n,amp=amp,zi=zi,zend=zend,size=size,cfl=cfl,gamma=m.gamma,xe=m.xe,baryon_ratio=m.baryon_ratio,pressure=m.pressure,cold_mass_Msun=float(m.mc.sum()*m.M0)),reason=reason,initial_residuals=[res,rp,rm],rows=rows,max_work_error=float(maxerr),reflections=reflections,final=dict(xc=xc.tolist(),xb=xb.tolist(),pc=pc.tolist(),pb=pb.tolist(),P=P.tolist(),chi=c.tolist(),Q=Q.tolist(),V=V.tolist(),time=t))
