import argparse,json
from pathlib import Path
import numpy as np
from model import Model
pa=argparse.ArgumentParser();pa.add_argument('--output');args=pa.parse_args();m=Model(8,.001);xc=m.x0.copy();xb=xc.copy();P,c,res=m.fields(xc);eps=1e-4;zero=np.zeros_like(xc);Z=np.zeros_like(P);z=np.zeros_like(c)
checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=float(v)))
rc,_,_=m.dep(xc,m.mc);rb,_,_=m.dep(xb,m.mb);masserr=max(abs(m.vol*rc.sum()/(m.mc*len(xc))-1),abs(m.vol*rb.sum()/(m.mb*len(xb))-1));ck('separate_mass_conservation',masserr<1e-12,masserr)
y=m.evaluate(xc,xb,P,c,1,zero,zero,Z,z);j=13;axis=1;dx=1e-6;xp=xc.copy();xm=xc.copy();xp[j,axis]+=dx;xm[j,axis]-=dx;fd=(m.evaluate(xp,xb,P,c,1,zero,zero,Z,z)[4]-m.evaluate(xm,xb,P,c,1,zero,zero,Z,z)[4])/(2*dx);err=abs(fd+m.mc*y[0][j,axis])/max(abs(fd),abs(m.mc*y[0][j,axis]),1e-16);ck('particle_action_force',err<1e-5,err)
# Hamiltonian partial at fixed canonical momenta and particle coordinates.
pc=np.ones_like(xc)*.001;pb=-pc*.2;Q=np.ones_like(P)*.0003;V=np.ones_like(c)*.0002
s=m.evaluate(xc,xb,P,c,1,pc,pb,Q,V);fd=(m.evaluate(xc,xb,P,c,np.exp(dx),pc,pb,Q,V)[4]-m.evaluate(xc,xb,P,c,np.exp(-dx),pc,pb,Q,V)[4])/(2*dx);err=abs(fd-s[5])/max(abs(fd),abs(s[5]),1e-15);ck('expansion_partial',err<1e-6,err)
# Independently vary the preparation difference step.
derivatives=[]
for e in [1e-4,1e-3]:
 pp,cp,rp=m.fields(xc+e*m.disp,np.exp(e));pm,cm,rm=m.fields(xc-e*m.disp,np.exp(-e));derivatives.append(((pp-pm)/(2*e),(cp-cm)/(2*e)))
for i,name in enumerate(['P','chi']):
 err=np.linalg.norm(derivatives[0][i]-derivatives[1][i])/max(np.linalg.norm(derivatives[1][i]),1e-14);ck('initial_tangent_'+name,err<.01,err)
# A null perturbation is a force-free expanding homogeneous state.
u=Model(8,0);P0,c0,_=u.fields(u.x0);state=u.evaluate(u.x0,u.x0,P0,c0,1,np.zeros_like(u.x0),np.zeros_like(u.x0),np.zeros_like(P0),np.zeros_like(c0));norm=max(np.max(abs(v)) for v in state[:4]);ck('homogeneous_null_force',norm<1e-8,norm)
Path(args.output).write_text(json.dumps(dict(checks=checks),indent=2)+'\n')
