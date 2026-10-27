"""Resolve the truncated cold profile-1 alpha-3 history farther inward."""
import json
import sys
from pathlib import Path
import numpy as np
from assembly import Live

out=dict(scope='Targeted cold domain extension, 5 initial dynamical times',runs=[])
for nq in (1024,2048):
    m=Live(1e8,1,n=12,nq=nq,f=.95,alpha=3)
    edges=np.geomspace(m.r0.min()*1e-5,m.rmax,nq+1)
    mid=(edges[1:]+edges[:-1])/2;width=np.diff(edges)/2
    m.grid=np.ravel(np.column_stack([mid-width/np.sqrt(3),mid+width/np.sqrt(3)]))
    m.weights=np.repeat(width,2);m.rmin=edges[0]
    en,grad,_,_=m.energy(m.r0,0)
    vc2=m.r0*grad/m.m
    m.l2=.1*vc2*m.r0**2;m.v0=-.3*np.sqrt(vc2)
    half=float(np.interp(.5,np.cumsum(m.mb[:m.n]),m.r0[:m.n]))
    menc=float(np.interp(half,m.grid,m.kernel(m.r0)[0]@m.m))
    m.tdyn=np.sqrt(half**3/menc);m.Gamma=10/m.tdyn;m.eta=.01*abs(en)*m.tdyn
    try:
        row=m.run(duration=5,rtol=2e-8)
    except (ValueError,RuntimeError) as err:
        row=dict(status='failed',reason=str(err))
    row.update(nq=nq,profile_index=1,support=.1,inner_scale=1e-5)
    out['runs'].append(row)
    Path(sys.argv[1]).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in row.items() if k not in ('history','final_radii','final_radial_v')}),flush=True)
