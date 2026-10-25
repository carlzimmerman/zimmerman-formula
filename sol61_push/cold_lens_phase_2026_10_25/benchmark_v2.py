import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,pathlib,sys,time,numpy as np
from lens import Grid,Lens,VariableAxis
P=pathlib.Path(__file__).resolve().parent
# 3D analytic chirped Gaussian: full accelerated, time-dependent lens phase.
rows=[]
for n,dt,omit in [(16,.01,False),(24,.01,False),(32,.01,False),(32,.005,False),(48,.01,False),(64,.01,False),(32,.005,True)]:
 g=Grid(n,7,1.5);eta=.12;beta=.3;acc=.2;T=.4
 p=[np.zeros_like(g.r) for _ in range(3)];ev=Lens(g,eta,p,beta,acc,gravity=False,omit_compensation=omit)
 u=np.exp(-g.r**2/2)*g.sv;q=abs(u)**2*(g.xyz[0]>0);phi=ev.potential(u);h0=ev.moments(u,phi,0);bond=0
 for it in range(round(T/dt)):u,q,phi,e=ev.step(u,q,phi,it*dt,dt);bond=max(bond,e)
 a,ad,_=ev.scale(T);aa=1+1j*beta/eta;den=1+1j*eta*aa*T
 psi=den**(-1.5)*np.exp(-aa*(a*g.r)**2/(2*den));exact=a**1.5*psi*np.exp(-1j*a*ad*g.r**2/(2*eta))*g.sv
 h=ev.moments(u,phi,T);rows.append(dict(n=n,dt=dt,omit_compensation=omit,L2=float(np.linalg.norm(u-exact)/np.linalg.norm(exact)),relative_energy_drift=(h['E']-h0['E'])/h0['E'],mass_drift=h['M']-h0['M'],tag_excess=float(np.max(q-abs(u)**2)),bond_residual=bond))
print(json.dumps(rows,indent=2));out=pathlib.Path(sys.argv[1]);out.write_text(json.dumps(dict(cases=rows),indent=2)+'\n')
assert rows[1]['L2']<rows[0]['L2'] and rows[2]['L2']<rows[1]['L2']
assert rows[-1]['L2']>rows[-2]['L2']*3
assert all(abs(r['mass_drift'])<1e-10 and r['tag_excess']<1e-10 and r['bond_residual']<1e-10 for r in rows)

assert rows[5]["L2"]<rows[4]["L2"]<rows[2]["L2"]
assert abs(rows[5]["relative_energy_drift"])<.01
