"""Orthogonal force/energy quadrature and reciprocity checks."""
import json
import sys
from pathlib import Path
import numpy as np
from assembly import Live,PROFILES

rows=[]
for i,(_,mass,b,_) in enumerate(PROFILES):
    models=[Live(mass,b,n=12,nq=nq) for nq in (256,512,1024,2048)]
    r=models[0].r0
    reference=models[-1].energy(r,.3)
    for m,nq in zip(models,(256,512,1024,2048)):
        e,g,gx,d=m.energy(r,.3)
        eg,gg,_,dg=m.energy(r,0,True)
        # Newtonian self-energy has degree -1 in all shell radii.
        virial=abs(np.dot(r,gg)+eg)/abs(eg)
        # The potential is an independent mass derivative of the field integral.
        phi=abs(.5*np.dot(m.m,dg['phi'])-eg)/abs(eg)
        rows.append(dict(profile_index=i,nq=nq,virial_relative_error=float(virial),
            potential_identity_relative_error=float(phi),
            energy_difference_to_2048=float(abs(e-reference[0])/abs(reference[0])),
            force_difference_to_2048=float(np.linalg.norm(g-reference[1])/np.linalg.norm(reference[1]))))

balance=[]
for f in (0,.3,.95):
    m=Live(1e8,1,n=12,f=f)
    for x in (0,.1,.5,.9,1.):
        for direction in (-1,1):
            r=m.r0;v=m.v0*direction;N=len(r)
            en,g,gx,d=m.energy(r,x);y=np.r_[r,v,x,0.,0.];dy=m.rhs(0,y)
            total=np.dot(g-m.m*m.l2/r**3,v)+np.dot(m.m*v,dy[N:2*N])+gx*dy[2*N]+dy[2*N+1]
            work=gx*dy[2*N]-dy[2*N+2]+m.eta*dy[2*N]**2
            balance.append(dict(f=f,x=x,direction=direction,energy_error=float(abs(total)/(abs(en)/m.tdyn)),
                work_error=float(abs(work)/(abs(en)/m.tdyn)),heat=float(dy[2*N+1])))
assert max(z['energy_error'] for z in balance)<1e-9
assert max(z['work_error'] for z in balance)<1e-9
assert min(z['heat'] for z in balance)>=0
out=dict(quadrature=rows,reciprocity=balance)
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(max_energy_identity=max(z['energy_error'] for z in balance),
    max_work_identity=max(z['work_error'] for z in balance),
    max_512_force_difference=max(z['force_difference_to_2048'] for z in rows if z['nq']==512))))
