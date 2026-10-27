import argparse,json
from pathlib import Path
import numpy as np
from pinning import Pin,PROFILES,h
from angular_gate import s,Fp

def potential(m,x):
    q=h(x);u=m.u(q);M=np.dot(m.m,q)
    terms=m.a*(u/(1-u)+20*m.C*s(x)*Fp(u))
    mu=np.cumsum(terms[::-1])[::-1]-(1-m.own)*terms+m.tail_mu(M)
    diff=np.diff(x);u_mid=m.Amid@q
    mu+=m.Amid.T@(.5*m.links*Fp(u_mid)*diff**2)/m.m
    mu+=.5*m.ell2*m.gamma(M)[1]*x[-1]**2
    return q*(mu-m.epsilon*m.B)

def checks():
    m=Pin(6e10,3,n=64,epsilon=1e5);x=np.linspace(.9,.1,m.n);mu=potential(m,x)
    direction=m.m*np.cos(np.arange(m.n)+.2);old=m.m.copy();oldA=m.A.copy();oldAm=m.Amid.copy();eps=1e-5
    es=[]
    for sign in [1,-1]:
        ratio=1+sign*eps*direction/old;m.m=old*ratio;m.A=oldA*ratio[None,:];m.Amid=oldAm*ratio[None,:]
        es.append(m.energy_grad(x)[0])
    err=abs((es[0]-es[1])/(2*eps)-mu@direction)/max(abs(mu@direction),1)
    assert err<1e-6
    return dict(mass_potential_fd_relative=err)

def analyze(m,row):
    x=np.array(row['x']);q=h(x);p=potential(m,x);aint=-np.gradient(p,m.r,edge_order=2)
    inner=(m.r>=.5*m.b)&(m.r<=min(5*m.b,.4*m.R));res=(aint-m.g0)/m.g0
    # Same discretization, pure T and no binding/barrier/interface gradient.
    from response_stiffness import Response
    ref=Pin(m.mass,m.b*m.rm,m.n,Rjb=m.Rjb,epsilon=0,c=m.c)
    pref=potential(ref,np.ones(m.n));aref=-np.gradient(pref,ref.r,edge_order=2)
    control=float(max(abs((aref-ref.g0)[inner]/ref.g0[inner])))
    crossings=np.where((q[:-1]>=.5)&(q[1:]<.5))[0]
    restoration=None
    if len(crossings):
        j=crossings[-1];R=np.interp(.5,[q[j+1],q[j]],[m.r[j+1],m.r[j]])
        width=.15*m.R;v=-np.gradient(x,m.r)*np.exp(-((m.r-R)/width)**4)
        H=m.hessian(x);E,g=m.energy_grad(x);k=float(v@H@v);step=1e-4*min(np.diff(m.r))
        ep=m.energy_grad(x+step*v)[0];em=m.energy_grad(x-step*v)[0];kfd=(ep+em-2*E)/step**2
        restoration=dict(radius_kpc=float(R*m.rm),linear_force=float(-v@g),stiffness=float(k),fd_stiffness=float(kfd),fd_relative=abs(kfd-k)/max(abs(k),1e-20),coordinate='dimensionless R=r/rM; energy unit=Mb*a0*rM')
    row.update(full_matter_force_max_relative=float(max(abs(res[inner]))),full_matter_force_rms_relative=float(np.sqrt(np.mean(res[inner]**2))),control_force_max_relative=control,restoration=restoration,force_r=aint.tolist(),gravity=m.g0.tolist())
    return row

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=dict(checks=checks(),runs=[])
    _,mass,b,_=PROFILES[2]
    for rj,c in [(5,.03),(8,.03),(8,.1)]:
        for n in [128,256]:
            m=Pin(mass,b,n,rj,1e5,c);r=analyze(m,m.solve('all'));out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['x','r','C','force_r','gravity']},flush=True)
