"""Full reaction reversibility, local-moment nulls and separate-force checks."""
import json
import sys
from pathlib import Path
import numpy as np
from capture_v3 import Capture,local_moments,reaction_impulse,checks

base=checks();m=Capture(1e8,1,n=32,nq=512,beta=4)
m.state[32:36]=True
E,a,_=m.energy_force(m.x,m.state)
force=m.m[:,None]*a
base['net_force']=float(np.linalg.norm(np.sum(force,axis=0)))
base['net_torque']=float(np.linalg.norm(np.sum(np.cross(m.x,force),axis=0)))
base['translation_energy_error']=abs(m.energy_force(m.x+[13,-8,2],m.state)[0]-E)/abs(E)
assert max(base['net_force'],base['net_torque'],base['translation_energy_error'])<1e-10

# Identical mass/position/velocity, different state: force must differ.
x=m.x.copy();x[40]=x[32];state=m.state.copy();state[40]=False
_,a,_=m.energy_force(x,state)
rad=x[32]-np.average(x,axis=0,weights=m.m)
sep=float((a[32]-a[40])@rad/np.linalg.norm(rad))
assert sep>0
base['T_minus_F_outward_acceleration']=sep

# Check actual field jump and full environment-dependent barrier reversal.
i=40;j=0;S,_,_,_=m.basis(m.x)
M=S@(m.m*m.state);tot=m.m@m.state;e0,_=m.field(M,tot)
e1,_=m.field(M+m.m[i]*S[:,i],tot+m.m[i]);delta=e1-e0
normal=m.x[i]-m.x[j];normal/=np.linalg.norm(normal)
mu=m.m[i]*m.m[j]/(m.m[i]+m.m[j]);speed=np.sqrt(2*100*delta/mu)
v=m.v.copy();v[i]=v[j]-speed*normal
c0=local_moments(m.x[i],m.x[:m.n],v[:m.n],m.m[:m.n])['C']
vi,vj,kn=reaction_impulse(v[i],v[j],m.m[i],m.m[j],normal,delta)
vnew=v.copy();vnew[i]=vi;vnew[j]=vj
c1=local_moments(m.x[i],m.x[:m.n],vnew[:m.n],m.m[:m.n])['C']
B=m.beta*.5*(c0+c1)*abs(delta)
ri,rj,kr=reaction_impulse(-vi,-vj,m.m[i],m.m[j],normal,-delta)
vrev=-vnew.copy();vrev[i]=ri;vrev[j]=rj
cr0=local_moments(m.x[i],m.x[:m.n],-vnew[:m.n],m.m[:m.n])['C']
cr1=local_moments(m.x[i],m.x[:m.n],vrev[:m.n],m.m[:m.n])['C']
Br=m.beta*.5*(cr0+cr1)*abs(delta)
assert kn>=delta+B and kr>=Br
reverse_error=max(np.max(abs(ri+v[i])),np.max(abs(rj+v[j])))
assert reverse_error<1e-10 and abs(B-Br)<1e-10
base.update(finite_field_jump=float(delta),full_inverse_velocity_error=float(reverse_error),
            reversal_barrier_error=float(abs(B-Br)))

rng=np.random.default_rng(991);nulls=[]
for flat in (1,.25):
    for n in (32,64):
        for spin in (0,2):
            vals=[]
            for repeat in range(400):
                xb=rng.normal(size=(n,3));xb[:,2]*=flat
                vb=rng.normal(size=(n,3))+np.cross([0,0,spin],xb)
                vals.append(local_moments(np.zeros(3),xb,vb,np.ones(n)/n)['C'])
            nulls.append(dict(flat=flat,n=n,spin=spin,mean_C=float(np.mean(vals)),
                    median_C=float(np.median(vals)),p90_C=float(np.quantile(vals,.9))))

out=dict(checks=base,moment_calibration=nulls,nonclaim='Finite-neighbor estimator has residual sampling noise; not a galaxy classifier')
out['calibration_pass']=all(row['mean_C']<.05 and row['p90_C']<.1 if row['spin']==0 else row['mean_C']>.5 for row in nulls)
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
