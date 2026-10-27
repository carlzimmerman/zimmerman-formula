import argparse,json
from pathlib import Path
import numpy as np
import sympy as s
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args();checks=[];rows=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v)
y,k,ep,rho=s.symbols('y k ep rho',positive=True)
A=1+k*k-ep*rho*(1-k*k)
# y=gamma^2. Density growth: y=rho-rho*k^2*(1+ep*y)/(1+k^2+ep*y).
poly=s.expand((y-rho)*(1+k*k+ep*y)+rho*k*k*(1+ep*y))
ck('dispersion_polynomial',s.expand(poly-(ep*y*y+A*y-rho))==0,poly)
ck('A_monotone',s.simplify(s.diff(A,k)-2*k*(1+ep*rho))==0,'dA/dk positive')
for ee in [.001,.005,.02]:
 for rr in [.01,.1,1]:
  kk=np.geomspace(1e-3,1e3,300);aa=1+kk**2-ee*rr*(1-kk**2);gg=2*rr/(aa+np.sqrt(aa*aa+4*ee*rr));res=np.max(abs(gg-(rr-rr*kk**2*(1+ee*gg)/(1+kk**2+ee*gg))))
  ck('branch_%g_%g'%(ee,rr),np.all(np.diff(gg)<0) and res<1e-12 and abs(gg[0]/rr-1)<2e-6,res)
  rows.append(dict(eps=ee,rho0=rr,k=kk.tolist(),gamma_squared=gg.tolist()))
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(dict(checks=checks,rows=rows),indent=2)+'\n');raise SystemExit(0 if all(z['passed'] for z in checks) else 1)
