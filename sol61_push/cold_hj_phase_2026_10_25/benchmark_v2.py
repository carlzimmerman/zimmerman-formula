import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import pathlib,sys,json,numpy as np
from adaptive_v2 import Grid,Radial,Adaptive
rows=[]
for n,dt,omit in [(16,.01,False),(24,.01,False),(32,.01,False),(32,.005,False),(48,.01,False),(32,.005,True)]:
 g=Grid(n,7,1.5);eta=.12;kap=.3;T=.4;rad=Radial(g)
 def S(t,r):
  aa=1+1j*kap/eta;z=1+1j*eta*aa*t
  return -1.5*eta*np.angle(z)-eta*np.imag(aa/z)*r*r/2
 ev=Adaptive(g,eta,rad,S(0,rad.R),gravity=False,omit_gauge=omit);u=np.exp(-g.r*g.r/2)*g.sv;q=abs(u)**2*(g.xyz[0]>0);phi=ev.potential(u);h0=ev.moments(u,phi);gauge=0.;bond=0.
 for it in range(round(T/dt)):
  u,q,phi,d=ev.step(u,q,phi,it*dt,dt,analytic=S);gauge+=d['gauge_absolute'];bond=max(bond,d['bond'])
 aa=1+1j*kap/eta;z=1+1j*eta*aa*T;exact=z**(-1.5)*np.exp(-aa*g.r*g.r/(2*z))*g.sv;physical=u*np.exp(1j*ev.value/eta);h=ev.moments(u,phi)
 rows.append(dict(n=n,dt=dt,omit_gauge=omit,L2=float(np.linalg.norm(physical-exact)/np.linalg.norm(exact)),physical_energy_drift=(h['E']-h0['E'])/h0['E'],gauge_absolute_relative=gauge/h0['E'],mass_drift=h['M']-h0['M'],tag_excess=float(np.max(q-abs(u)**2)),bond_residual=bond))
# Godunov HJ has an independent pre-caustic quadratic solution away from boundaries.
g=Grid(8,8,1.5);hj=[]
for nr in (257,513,1025):
 rad=Radial(g,nr);k=.1;T=.5;S=-k*rad.R**2/2;init=S.copy()
 for _ in range(50):S,_=rad.advance(S,np.zeros_like(S),T/50)
 exact=-k/(1-k*T)*rad.R**2/2;mask=(rad.R>1)&(rad.R<6);hj.append(dict(nr=nr,max_error=float(np.max(abs(S[mask]-exact[mask])))))
out=dict(wave_cases=rows,HJ_cases=hj);pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
assert rows[1]['L2']<rows[0]['L2'] and rows[2]['L2']<rows[1]['L2'] and rows[4]['L2']<rows[2]['L2']
assert rows[-1]['L2']>rows[3]['L2']*10
assert hj[2]['max_error']<hj[1]['max_error']<hj[0]['max_error']
assert all(abs(r['mass_drift'])<1e-10 and r['tag_excess']<1e-10 and r['bond_residual']<1e-10 for r in rows)
