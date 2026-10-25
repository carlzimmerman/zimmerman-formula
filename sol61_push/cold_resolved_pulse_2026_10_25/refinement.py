"""Isometric angular interpolation of a saved complex field; no radial remap."""
import hashlib,json,pathlib,numpy as np
from scipy.special import eval_legendre
from scipy.interpolate import CubicSpline
from gauss import Sphere
from lean import Sphere as CN
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1]

def load(nt=48,nf=96):
 seed=P/'runs/draco_joint_s05';meta=json.loads(pathlib.Path(str(seed)+'.json').read_text());saved=np.load(str(seed)+'.npz');h=meta['history'][-1]
 assert meta['status'] in ['stopped soft wall budget','finished requested finite interval']
 assert max(abs(h['E_relative_error']),abs(h['Jz_relative_error']),h['angular_edge_fraction'],h['azimuth_edge_fraction'])<.01 and h['boundary_fraction']<1e-4
 assert meta['inputs_before']==meta['inputs_after']
 for q,digest in meta['inputs_after'].items():assert hashlib.sha256((ROOT/q).read_bytes()).hexdigest()==digest
 units=meta['physical'];eta=units['eta_code'];raw=np.load(ROOT/'sol61_push/cold_envelope_formation_2026_10_24/runs/draco_escape_long_fields.npz');r,v,lm=[raw[k] for k in ['r','initial','lm']];j=next(j for j,x in enumerate(lm) if tuple(x)==(0,0));valid=(r<21.8)&(abs(v[:,j])>1e-20);rv=r[valid];sp=CubicSpline(rv,eta*np.unwrap(np.angle(v[valid,j])))
 def phase(x,der=0):
  if der:return np.where(x<=rv[-1],sp(x,1),sp(rv[-1],1))
  return np.where(x<=rv[-1],sp(x),sp(rv[-1])+sp(rv[-1],1)*(x-rv[-1]))
 old=CN(256,40,64,eta=eta,phase=phase);new=Sphere(256,nt,nf,eta=eta,phase=phase);assert nt>=old.nt and nf>=old.nf
 for k,q in dict(r=old.r,w=old.w,mu=old.mu,aw=old.aw,S=old.phase).items():assert np.array_equal(saved[k],q)
 assert np.array_equal(old.r,new.r) and np.array_equal(old.w,new.w) and np.array_equal(old.phase,new.phase)
 u=saved['u'];pot=old.poisson(u);om=old.moments(u,pot);rk0=float(np.real(np.vdot(u,old.radial_apply(u))));bf=np.fft.fft(u,axis=2,norm='ortho');B=np.zeros((len(new.r),nt,nf),complex);ll=np.arange(old.nt);Qo=np.sqrt(old.wmu)[:,None]*np.array([eval_legendre(l,old.mu) for l in ll]).T*np.sqrt((2*ll+1)/2)[None,:];Qn=np.sqrt(new.wmu)[:,None]*np.array([eval_legendre(l,new.mu) for l in ll]).T*np.sqrt((2*ll+1)/2)[None,:]
 for k,m in enumerate(old.m):
  target=np.flatnonzero(new.m==m);assert len(target)==1;B[:,:,target[0]]=(bf[:,:,k]@Qo)@Qn.T
 un=np.fft.ifft(B,axis=2,norm='ortho');del B,bf
 radial=float(np.max(abs(np.sum(abs(un)**2,axis=(1,2))-np.sum(abs(u)**2,axis=(1,2)))));pn=new.poisson(un);nm=new.moments(un,pn);rk1=float(np.real(np.vdot(un,new.radial_apply(un))));scale=om['K']+abs(om['W']);diagnostic=dict(seed='draco_joint_s05',seed_absolute_T=h['t'],old_grid=[256,40,64],new_grid=[256,nt,nf],old_moments=om,new_moments=nm,radial_mass_error=radial,global_mass_error=nm['M']-om['M'],Jz_error=nm['Jz']-om['Jz'],radial_K_error=rk1-rk0,K_jump_relative=(nm['K']-om['K'])/scale,W_jump_relative=(nm['W']-om['W'])/scale,scope='same complex angular polynomial/Fourier field, changed quadrature/operator bandwidth; no mass normalization; conditional seed, not re-evolved formation')
 assert max(radial,abs(diagnostic['global_mass_error']),abs(diagnostic['Jz_error']),abs(diagnostic['radial_K_error']))<1e-11
 assert max(abs(diagnostic['K_jump_relative']),abs(diagnostic['W_jump_relative']))<.01
 return new,un,pn,units,diagnostic
