"""Restricted homologous-path energy envelope; not a general lower bound."""
import argparse,json
from pathlib import Path
import numpy as np
from experiment import Inertial,phase,PROFILES

def envelope(index,f,ns=401,nx=101):
    _,mass,b,_=PROFILES[index]
    m=Inertial(mass,b,f=f,n=12,nq=512)
    E0=m.observe(0,m.initial())['energy']
    E,_,_,info=m.energy(m.r0,0)
    Ug=info['ug']; A=.5*np.dot(m.m,m.l2/m.r0**2)
    S,_=m.kernel(m.r0);Mc=S@m.md; kap=m.kappa
    # The full radial quadrature, including the inverse-radius tail.
    z0=np.r_[Mc/(kap*m.grid**2),5.364*m.tail_t**2/kap]
    vol=np.r_[m.weights*m.grid**2,m.tail_w/m.tail_t**4]*kap**2
    scales=np.geomspace(.02,30,ns)
    rows=[]
    for x in np.linspace(0,1,nx):
        q,_,s,_=phase(x)
        z=q*z0[None,:]/scales[:,None]**2
        valid=np.max(z,axis=1)<1
        zz=z[valid];ss=scales[valid]
        # Stable log remainder; tiny-z series avoids cancellation.
        W=np.empty_like(zz);small=zz<.01
        W[small]=sum(zz[small]**k/k for k in range(2,10))
        W[~small]=-np.log1p(-zz[~small])-zz[~small]
        fields=ss**3*((W+20*f*f*s*zz**2/(1-zz))@vol)
        total=Ug/ss+A/ss**2+fields
        k=int(np.argmin(total))
        rows.append(dict(x=float(x),q=float(q),min_energy=float(total[k]),scale=float(ss[k]),
                         edge=bool(k in (0,len(ss)-1))))
    # Quadrature homology cross-check against direct energy at scaled radii.
    tests=[]
    for s,x in [(1,.2),(2,.6),(.8,.1)]:
        r=m.r0*s
        direct=m.energy(r,x)[0]+A/s**2
        q,_,bar,_=phase(x);zz=q*z0/s**2
        if max(zz)>=1:continue
        W=np.where(zz<.01,sum(zz**k/k for k in range(2,10)),-np.log1p(-zz)-zz)
        transformed=Ug/s+A/s**2+s**3*np.dot(vol,W+20*f*f*bar*zz**2/(1-zz))
        tests.append(abs(direct-transformed)/max(abs(direct),1e-10))
    return dict(profile=index,f=f,initial_energy=E0,initial_baryon_rotation=float(.5*np.dot(m.mb,m.l2/m.r0**2)),
        crest_of_minima=max(r['min_energy'] for r in rows),endpoint_min=rows[-1]['min_energy'],
        restricted_path_energy_excluded=bool(max(r['min_energy'] for r in rows)>E0),
        homology_crosscheck=max(tests),rows=rows)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--ns',type=int,default=401)
    args=ap.parse_args();rows=[envelope(i,f,args.ns) for i in range(4) for f in (.3,.95)]
    Path(args.output).write_text(json.dumps(dict(scope='Common homology family only; numerical minimum is not certified',runs=rows),indent=2)+'\n')
    for r in rows:print({k:v for k,v in r.items() if k!='rows'})
