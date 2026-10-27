import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);args=pa.parse_args()
eta=.005;fb=1/6.364;fc=1-fb;ell=.0004404221297174536;N0=-np.log(1101)
checks=[]
def ck(name,passed,value):checks.append(dict(name=name,passed=bool(passed),value=float(value)))
mode=[]
for J in np.geomspace(1e-4,1e4,17):
 for q in np.geomspace(1e-3,1e3,49):
  B=1+q*q-eta*J*(1-q*q);D=np.hypot(B,2*np.sqrt(eta*J));x=2*J/(B+D) if B>=0 else (D-B)/(2*eta)
  resid=abs(eta*x*x+B*x-J)/(J+abs(B*x)+eta*x*x)
  mode.append(dict(J=float(J),q=float(q),x=float(x),quasistatic=float(J/(1+q*q)),residual=float(resid)))
ck('cold_polynomial_residual',max(x['residual'] for x in mode)<1e-12,max(x['residual'] for x in mode))
ck('cold_inertia_no_faster',max(x['x']/x['quasistatic'] for x in mode)<=1+1e-10,max(x['x']/x['quasistatic'] for x in mode))
# Independent 6-dimensional first-order matrix for b,c,u=divP.
two=[]
for J in [1e-3,.1,1,100]:
 for q in [.01,.1,1,10,100]:
  A=np.zeros((6,6));A[0,1]=A[2,3]=A[4,5]=1
  A[1,0]=A[3,0]=fb*J;A[1,2]=fc*J;A[3,2]=fc*J*(1-q*q);A[3,4]=q*q
  A[5,2]=q*q*fc*J/eta;A[5,4]=-(1+q*q)/eta
  vals=np.linalg.eigvals(A);s=max(vals.real)
  Q=J*np.array([[fb,fc],[fb,fc/(1+q*q)]]);sq=np.sqrt(max(np.linalg.eigvalsh(np.diag([np.sqrt(fb),np.sqrt(fc)])@Q@np.diag([1/np.sqrt(fb),1/np.sqrt(fc)]))))
  two.append(dict(J=J,q=q,s=float(s),quasistatic=float(sq),max_imag_growing=float(max([abs(v.imag) for v in vals if v.real>1e-7],default=0))))
ck('twofluid_inertia_no_faster',max(x['s']/x['quasistatic'] for x in two)<1+1e-7,max(x['s']/x['quasistatic'] for x in two))
G=6.67430e-11;mpc=3.085677581491367e22;ms=1.98847e30;rhocrit=3*(67.4*1000/mpc)**2/(8*np.pi*G)*mpc**3/ms;rhom=.315*rhocrit

def growth(k,z,tol):
 def f(N,y):
  b,bp,c,cp=y;S=1/(1+(k*ell/np.exp(N))**2)
  return [bp,-.5*bp+1.5*(fb*b+fc*c),cp,-.5*cp+1.5*(fb*b+fc*S*c)]
 sol=solve_ivp(f,(N0,-np.log(1+z)),[1.]*4,method='DOP853',rtol=tol,atol=tol*1e-3)
 assert sol.success
 return sol.y[:,-1]
rows=[]
for M in sorted(list(np.geomspace(1e5,1e11,13))+[1.0952264e7]):
 R=(3*M/(4*np.pi*rhom))**(1/3);k=1/R
 for z in [10,20,30,100]:
  y=growth(k,z,1e-10);y2=growth(k,z,1e-8);dust=1101/(1+z)
  rows.append(dict(M=float(M),R_L_Mpc=float(R),k=float(k),z=z,cold_growth=float(y[2]),baryon_growth=float(y[0]),dust_growth=dust,cold_retained=float(y[2]/dust),initial_delta_for_onset=float(1/y[2]),repeat=float(max(abs(y-y2)/np.maximum(abs(y),1e-15)))))
ck('growth_repeat',max(x['repeat'] for x in rows)<1e-6,max(x['repeat'] for x in rows))
dusterr=max(abs(growth(0,z,1e-11)[2]/(1101/(1+z))-1) for z in [10,20,30,100]);ck('dust_reference',dusterr<1e-9,dusterr)
ck('positive_growth_dust_ceiling',max(x['cold_retained'] for x in rows)<=1,max(x['cold_retained'] for x in rows))
Path(args.output).write_text(json.dumps(dict(checks=checks,cold_modes=mode,twofluid_modes=two,rows=rows,rho_m0=rhom),indent=2)+'\n')
