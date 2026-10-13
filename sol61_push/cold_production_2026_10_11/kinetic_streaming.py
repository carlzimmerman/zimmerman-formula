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

from scipy.special import eval_legendre,spherical_jn
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
def run(wavelength,L,collisions=True):
 N=64;de=8/N;e=(np.arange(N)+.5)*de;ec=(np.arange(2*N)+1)*de
 pp=np.sqrt(2*e);pc=2*np.sqrt(np.maximum(ec-1,0));wp=pp*de;wc=2*pc*de;valid=wc>0
 i,j=np.indices((N,N));ss=i+j
 mask=((e[:,None]+e[None,:]-2)**2<=4*e[:,None]*e[None,:]) & (ec[ss]>1)
 ii=i[mask];jj=j[mask];kk=ss[mask]
 c12=(e[ii]+e[jj]-2)/(pp[ii]*pp[jj]);c1=(pc[kk]**2+pp[ii]**2-pp[jj]**2)/(2*pc[kk]*pp[ii]);c2=(pc[kk]**2+pp[jj]**2-pp[ii]**2)/(2*pc[kk]*pp[jj])
 P12=np.array([eval_legendre(l,c12) for l in range(L+1)]);P1=np.array([eval_legendre(l,c1) for l in range(L+1)]);P2=np.array([eval_legendre(l,c2) for l in range(L+1)])
 qwave=2*math.pi*u*c*(timeGyr*1e9*year)/(wavelength*3.0856775814913673e19)
 phases=np.linspace(0,3,61);ts=phases/(qwave*r);speeds=np.r_[pp,pc/2]
 def rhs(t,z):
  a=z[:N];b=z[N:3*N];h=z[3*N:].reshape(L+1,3*N);dh=np.zeros_like(h);da=np.zeros(N);db=np.zeros(2*N)
  if collisions:
   d1=a[jj]-b[kk];d2=a[ii]-b[kk];d3=a[ii]+a[jj]+1/A
   flux=de*de*(a[ii]*a[jj]-b[kk]*d3)
   da=-(np.bincount(ii,weights=flux,minlength=N)+np.bincount(jj,weights=flux,minlength=N))/wp
   tmp=np.bincount(kk,weights=flux,minlength=2*N);db[valid]=tmp[valid]/wc[valid]
   for l in range(L+1):
    ha=h[l,:N];hb=h[l,N:]
    f1=de*de*(d1*ha[ii]+d2*ha[jj]*P12[l]-d3*hb[kk]*P1[l])
    f2=de*de*(d1*ha[ii]*P12[l]+d2*ha[jj]-d3*hb[kk]*P2[l])
    fc=de*de*(d1*ha[ii]*P1[l]+d2*ha[jj]*P2[l]-d3*hb[kk])
    dh[l,:N]=-(np.bincount(ii,weights=f1,minlength=N)+np.bincount(jj,weights=f2,minlength=N))/wp
    tmp=np.bincount(kk,weights=fc,minlength=2*N);dh[l,N:][valid]=tmp[valid]/wc[valid]
  for l in range(L+1):
   if l:dh[l]+=qwave*speeds*l/(2*l-1)*h[l-1]
   if l<L:dh[l]-=qwave*speeds*(l+1)/(2*l+3)*h[l+1]
  return np.r_[da,db,dh.reshape(-1)]
 initial=np.exp(-e/r**2);ct=float((wp*initial)@e/(r*r*np.sum(wp*initial)))
 h=np.zeros((L+1,3*N));h[0,:N]=initial*(e/r**2-ct)
 y0=np.r_[initial,np.zeros(2*N),h.reshape(-1)]
 sol=solve_ivp(rhs,(0,ts[-1]),y0,t_eval=ts,method='DOP853',rtol=1e-8,atol=2e-12,max_step=min(.1,ts[-1]/40))
 check('integration',sol.success)
 bgQ=wp@sol.y[:N]+2*wc@sol.y[N:3*N];bgE=(wp*e)@sol.y[:N]+(wc*ec)@sol.y[N:3*N]
 check('background charge',max(abs(bgQ/bgQ[0]-1))<1e-9);check('background energy',max(abs(bgE/bgE[0]-1))<1e-9)
 hs=sol.y[3*N:].reshape(L+1,3*N,-1)
 eq=(wp*e)@hs[0,:N]+(wc*ec)@hs[0,N:];nq=wp@hs[0,:N]+2*wc@hs[0,N:]
 errors=[]
 for idx in [0,20,40,60]:
  dd=rhs(ts[idx],sol.y[:,idx])[3*N:].reshape(L+1,3*N)
  mom=(wp*pp)@hs[1,:N,idx]+(wc*pc)@hs[1,N:,idx]
  curr=(wp*e*pp)@hs[1,:N,idx]+(wc*ec*pc/2)@hs[1,N:,idx]
  errors.extend([abs(wp@dd[0,:N]+2*wc@dd[0,N:]+qwave*mom/3),abs((wp*e)@dd[0,:N]+(wc*ec)@dd[0,N:]+qwave*curr/3)])
 check('Fourier charge and energy continuity',max(errors)<1e-9)
 free=np.array([(wp*e*h[0,:N])@spherical_jn(0,qwave*pp*t) for t in ts])/eq[0]
 if not collisions:check('collisionless Bessel benchmark',max(abs(eq/eq[0]-free))<1e-6)
 return dict(wavelength_kpc=wavelength,Lmax=L,collisions=collisions,end_time_Gyr=float(ts[-1]*timeGyr),energy_contrast_ratio=(eq/eq[0]).tolist(),free_energy_contrast_ratio=free.tolist(),charge_contrast_over_initial_energy=(nq/eq[0]).tolist(),max_collision_difference=float(max(abs(eq/eq[0]-free))),continuity_residual=max(errors),phase=phases.tolist())
runs=[run(10,24,False),run(10,12),run(10,24),run(1000,12),run(1000,24)]
comparisons=[]
for aa,bb in [(runs[1],runs[2]),(runs[3],runs[4])]:
 err=float(max(abs(np.array(aa['energy_contrast_ratio'])-np.array(bb['energy_contrast_ratio']))))
 check('angular refinement',err<1e-4);comparisons.append(dict(wavelength_kpc=aa['wavelength_kpc'],max_angular_difference=err))
out=dict(all_pass=all(z['passed'] for z in checks),checks=checks,runs=runs,comparisons=comparisons,non_claims=['Linear Fourier perturbation about evolving homogeneous bath','No gravity, boundaries, condensate or energy-grid convergence','Not a conductivity determination or halo profile'])
(p/'kinetic_streaming_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(all_pass=out['all_pass'],checks=len(checks),comparisons=comparisons,runs=[dict(wavelength_kpc=z['wavelength_kpc'],Lmax=z['Lmax'],collisions=z['collisions'],end_time_Gyr=z['end_time_Gyr'],max_collision_difference=z['max_collision_difference'],end_energy_ratio=z['energy_contrast_ratio'][-1],free_end=z['free_energy_contrast_ratio'][-1],continuity_residual=z['continuity_residual']) for z in runs]),indent=2));assert out['all_pass']
