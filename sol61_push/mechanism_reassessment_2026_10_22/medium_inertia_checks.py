import numpy as np
from scipy.special import wofz
from scipy.optimize import root
import sympy as s
import json,sys

def R(z):return 1+z*1j*np.sqrt(np.pi)*wofz(z)
rows=[]
for A,guess in [(.3,1-1j),(1,1.4-.6j),(3,1.9-.25j),(10,2.7-.04j),(20,3.5-.003j),(40,4.65-1e-7j)]:
 def f(v):
  d=1+A*R(v[0]+1j*v[1]);return [d.real,d.imag]
 sol=root(f,[guess.real,guess.imag],tol=1e-11);z=sol.x[0]+1j*sol.x[1]
 rows.append(dict(A=A,success=bool(sol.success),real=float(z.real),imag=float(z.imag),residual=float(abs(1+A*R(z))),amplitude_efold_periods=float(z.real/(-2*np.pi*z.imag))))
r1,r2,v1,v2=s.symbols('r1 r2 v1 v2',positive=True)
r=r1+r2;j=r1*v1+r2*v2;v=j/r
variance=(r1*(v1-v)**2+r2*(v2-v)**2)/r
checks={'kinetic_split':s.simplify((r1*v1*v1+r2*v2*v2)/2-j*j/(2*r)-r*variance/2)==0}
k,h,gamma,dr=s.symbols('k h gamma dr',positive=True)
checks['density_energy']=s.simplify((h+gamma*k*k)*(dr/k)**2/2-(h/k**2+gamma)*dr*dr/2)==0
rho,sp,grad,gN,rest=s.symbols('rho s2 rhoprime gN R',positive=True)
force=-gN+rest-gamma*grad
checks['warm_balance']=s.simplify((rho*force-sp*grad).subs(rest,gN+(sp/rho+gamma)*grad))==0
# Density1, current0 in both; variance differs.
cold=[(1.,0.)];streams=[(.5,-1.),(.5,1.)]
mom=lambda fs:[sum(a*v**n for a,v in fs) for n in [0,1,2]]
mc,ms=mom(cold),mom(streams)
checks['nonclosure_witness']=mc[:2]==ms[:2] and mc[2]!=ms[2]
checks['roots']=all(x['residual']<1e-9 and x['imag']<0 for x in rows)
checks['static_positive']=all(1+x['A']>0 for x in rows)
GM,a0,rad,ss,K=s.symbols('GM a0 radius sigma2 K',positive=True)
rM=s.sqrt(GM/a0)
rho_law=a0*rM/(K*rad**2)
h_law=2*K*rM/rad
AA=rho_law*h_law/(k*k*ss)
epswarm=2*ss*rad/GM
checks['damping_pressure_tradeoff']=s.simplify(AA*epswarm-4/(k*rad)**2)==0
checks={k:bool(v) for k,v in checks.items()}
out=dict(checks=checks,all_pass=all(checks.values()),roots=rows,cold_moments=mc,multistream_moments=ms,scope='identified medium local kinetic model; no live halo or selector')
with open(sys.argv[1],'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
