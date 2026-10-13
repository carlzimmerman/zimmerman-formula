"""Isotropic nonrelativistic three-wave kinetics, conservative finite energy grid."""
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
m=params['m_eV'];g=params['cubic_g_eV'];u=params['u']
c=299792458.;hbev=1.054571817e-34/1.602176634e-19;hc=hbev*c;year=365.25*86400
rho=1e-21*c*c/1.602176634e-19*hc**3;n=rho/m;sigma=200000/c;r=sigma/u
A=(2*math.pi)**1.5*n/(m*sigma)**3
GammaNR=g*g*u/(16*math.pi*m);timeGyr=hbev/(2*GammaNR*A)/year/1e9

checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
def run(N,emax):
 de=emax/N;e=(np.arange(N)+.5)*de;ec=(np.arange(2*N)+1)*de
 pp=np.sqrt(2*e);pc=2*np.sqrt(np.maximum(ec-1,0));wp=pp*de;wc=2*pc*de
 i,j=np.indices((N,N));ss=i+j
 mask=((e[:,None]+e[None,:]-2)**2<=4*e[:,None]*e[None,:]) & (ec[ss]>1)
 ii=i[mask];jj=j[mask];kk=ss[mask];valid=wc>0
 c12=(e[ii]+e[jj]-2)/(pp[ii]*pp[jj])
 c1=(pc[kk]**2+pp[ii]**2-pp[jj]**2)/(2*pc[kk]*pp[ii])
 c2=(pc[kk]**2+pp[jj]**2-pp[ii]**2)/(2*pc[kk]*pp[jj])
 check('triangle momentum projection',np.max(abs(pc[kk]*c1-pp[ii]-pp[jj]*c12))<1e-12)
 check('triangle source projection',np.max(abs(pp[ii]*c1+pp[jj]*c2-pc[kk]))<1e-12)
 def rhs(t,z):
  a=z[:N];b=z[N:3*N];a1=z[3*N:4*N];b1=z[4*N:]
  d1=a[jj]-b[kk];d2=a[ii]-b[kk];d3=a[ii]+a[jj]+1/A
  flux=de*de*(a[ii]*a[jj]-b[kk]*d3)
  da=-(np.bincount(ii,weights=flux,minlength=N)+np.bincount(jj,weights=flux,minlength=N))/wp
  db=np.zeros(2*N);tmp=np.bincount(kk,weights=flux,minlength=2*N);db[valid]=tmp[valid]/wc[valid]
  first=de*de*(d1*a1[ii]+d2*a1[jj]*c12-d3*b1[kk]*c1)
  second=de*de*(d1*a1[ii]*c12+d2*a1[jj]-d3*b1[kk]*c2)
  src=de*de*(d1*a1[ii]*c1+d2*a1[jj]*c2-d3*b1[kk])
  da1=-(np.bincount(ii,weights=first,minlength=N)+np.bincount(jj,weights=second,minlength=N))/wp
  db1=np.zeros(2*N);temp=np.bincount(kk,weights=src,minlength=2*N);db1[valid]=temp[valid]/wc[valid]
  return np.r_[da,db,da1,db1]
 aa=1/(e+.7);bb=1/(ec+1.4)
 boost=np.r_[aa,bb,aa*aa*pp,bb*bb*pc];dz=rhs(0,boost)
 check('equilibrium boost zero mode',np.max(abs(dz[3*N:]))<1e-12)
 initial=np.exp(-e/r**2);C=float(np.dot(wp*pp*pp*initial,e)/np.sum(wp*pp*pp*initial))
 dipole=initial*pp*(e-C)
 y0=np.r_[initial,np.zeros(2*N),dipole,np.zeros(2*N)]
 ts=np.linspace(0,20,201)
 sol=solve_ivp(rhs,(0,20),y0,t_eval=ts,method='DOP853',rtol=2e-9,atol=1e-12,max_step=.1)
 check('integration',sol.success)
 a=sol.y[:N];b=sol.y[N:3*N];a1=sol.y[3*N:4*N];b1=sol.y[4*N:]
 Q=wp@a+2*wc@b;E=(wp*e)@a+(wc*ec)@b
 momentum=(wp*pp)@a1+(wc*pc)@b1
 # Common angular factor 1/3 is omitted from both current and its normalization.
 current=(wp*e*pp)@a1+(wc*ec*pc/2)@b1
 qerr=float(max(abs(Q/Q[0]-1)));eerr=float(max(abs(E/E[0]-1)));perr=float(max(abs(momentum))/abs(current[0]))
 check('charge',qerr<1e-9);check('energy',eerr<1e-9);check('zero net momentum',perr<1e-9)
 snapshots=[dict(tau=float(ts[k]),time_Gyr=float(ts[k]*timeGyr),heat_current_ratio=float(current[k]/current[0]),source_charge_fraction=float(2*wc@b[:,k]/Q[0])) for k in [0,10,50,100,200]]
 return dict(N=N,emax=emax,charge_error=qerr,energy_error=eerr,momentum_error_over_initial_current=perr,initial_heat_current=float(current[0]),initial_dipole_C=C,snapshots=snapshots)
runs=[run(64,8.),run(128,8.),run(256,8.),run(256,16.)]
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,runs=runs,non_claims=['Linear dipole collision response on evolving homogeneous bath','No spatial streaming or gravitational dynamics','No thermal conductivity, diffusion coefficient or halo heat-flow prediction','No full continuum or closure validation'])
(p/'kinetic_heat_current_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));print('Checks:',len(checks));assert out['all_pass']
