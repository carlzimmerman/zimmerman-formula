import argparse,json
from pathlib import Path
import numpy as np
from radial_v2 import Radial
p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args();m=Radial(128,.03);P,c,res=m.static(m.x0);x=m.x0.copy();zero=np.zeros_like(x);z=np.zeros_like(P);rho,_,_=m.dep(x,m.mc);checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=float(v)))
ck('mass',abs(np.sum(rho*m.vol)/m.mc.sum()-1)<1e-12,abs(np.sum(rho*m.vol)/m.mc.sum()-1))
f=np.sin(m.r);g=np.cos(m.edge);err=abs(np.sum(m.vol*f*m.div(g))+np.sum(m.ev*m.grad(f)*g));ck('adjoint',err<1e-12,err)
s=m.evaluate(x,x,P,c,1,zero,zero,z,zero);j=40;step=1e-8;xp=x.copy();xm=x.copy();xp[j]+=step;xm[j]-=step;fd=(m.evaluate(xp,x,P,c,1,zero,zero,z,zero)[4]-m.evaluate(xm,x,P,c,1,zero,zero,z,zero)[4])/(2*step);err=abs(fd+m.mc[j]*s[0][j])/max(abs(fd),1e-15);ck('particle_force',err<1e-5,err)
rr=(rho-m.mc.sum()/m.vol.sum());h=(rr-m.div(P))/c;phase=.5*h*h-m.alpha*(c-1)+m.d*m.div(m.grad(c));err=np.linalg.norm(phase*np.sqrt(m.vol))/max(np.linalg.norm(.5*h*h*np.sqrt(m.vol)),1e-30);ck('phase_stationarity',err<1e-6,err);ck('P_stationarity',res<1e-6,res)
der=[]
for eps in [1e-4,1e-3]:
 pp,cp,_=m.static(x+eps*m.disp,np.exp(eps));pm,cm,_=m.static(x-eps*m.disp,np.exp(-eps));der.append(((pp-pm)/(2*eps),(cp-cm)/(2*eps)))
for i,name in enumerate(['P','chi']):
 err=np.linalg.norm(der[0][i]-der[1][i])/max(np.linalg.norm(der[1][i]),1e-30);ck('tangent_'+name,err<.001,err)
u=Radial(128,0);zero=np.zeros_like(u.r);zz=np.zeros_like(u.edge);s=u.evaluate(u.r,u.r,zz,np.ones_like(u.r),1,zero,zero,zz,zero);err=max(np.max(abs(f)) for f in s[:4]);ck('null_force',err<1e-7,err)
Path(a.output).write_text(json.dumps(dict(checks=checks),indent=2)+'\n')
