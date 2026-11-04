"""Coherent constant-singlet pole: exact tree absorptive and C-production matrices."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.linalg import eigh
from pole_network import one,build_model,adapt,DCOEF,E,G
MP=math.sqrt(.006);XP=math.sqrt(.006/E**2-2/(31*E))

def main(out):
 start=time.monotonic();d=build_model(XP,E,E,G,vertices=True)
 RY=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),d['R']);Q2=RY@RY;QF=np.zeros((73,73),complex);QF[:49,:49]=Q2;QF[49:,49:]=Q2[1:25,1:25];CS=np.block([[Q2.real,-Q2.imag],[Q2.imag,Q2.real]])
 O=adapt(d['O'],d['mS2'],CS);U=adapt(d['U'],d['mF'],QF);qs=np.einsum('ia,ia->a',O,CS@O).real;qf=np.einsum('ia,ia->a',U.conj(),QF@U).real
 mS=np.sqrt(np.maximum(d['mS2'],0));mF=d['mF'];phys=(mS>1e-12)|(qs<.01);P=np.where((abs(mS-MP)<1e-8)&(qs<.01))[0];assert len(P)==4
 low=min(mS[phys&(qs>.1)]);L=np.where((qs>.1)&(abs(mS-low)<1e-8))[0];assert len(L)==12
 RS=d['O'].T@O;RF=d['U'].conj().T@U;c3=np.einsum('ia,jb,kc,ijk->abc',RS,RS,RS,d['cubic'],optimize=True);yy=np.einsum('iu,jv,ka,ijk->uva',RF,RF,RS,d['yukawa'],optimize=True)
 ci=c3[P];y=yy[:,:,P].transpose(2,0,1);z=mF/MP;ri=z[:,None]**2;rj=z[None,:]**2;phase=np.sqrt(np.maximum(0,(1-ri-rj)**2-4*ri*rj));allow=z[:,None]+z[None,:]<1-1e-10
 fmat=MP/(16*math.pi)*(np.einsum('aij,bij,ij->ab',y,y.conj(),phase*(1-ri-rj)*allow).real-2*np.einsum('aij,bij,ij->ab',y,y,phase*z[:,None]*z[None,:]*allow).real)
 z=mS/MP;ri=z[:,None]**2;rj=z[None,:]**2;phase=np.sqrt(np.maximum(0,(1-ri-rj)**2-4*ri*rj));allow=(z[:,None]+z[None,:]<1-1e-10)&phys[:,None]&phys[None,:]
 smat=np.einsum('aij,bij,ij->ab',ci,ci,phase*allow)/(32*math.pi*MP)
 gamma=(fmat+smat);cL=ci[:,L][:,:,L];prod=np.einsum('aij,bij->ab',cL,cL)/len(L)**2
 eg,V=eigh(gamma);Grot=V.T@prod@V;off=Grot-np.diag(np.diag(Grot));comm=float(np.linalg.norm(gamma@prod-prod@gamma)/(np.linalg.norm(gamma)*np.linalg.norm(prod)))
 # Exact on-pole v=0 resolvent inclusive-neutral cross section, physical pair.
 sigma=2/(low*MP**2)*float(np.trace(prod@np.linalg.inv(gamma)))
 cauchy=2/(low*MP**2)*float(np.trace(prod))/min(eg)
 table=[]
 for vr in (0,1e-6,1e-5,3e-5,1e-4,3e-4,.001,.003,.01,.03,.1):
  ss=4*low**2+low**2*vr**2;root=math.sqrt(ss);beta=math.sqrt(max(0,1-4*low**2/ss));gin=len(L)**2*prod*beta/(32*math.pi*root)
  DD=np.linalg.inv((ss-MP**2)*np.eye(4)+1j*MP*(gamma+gin))
  value=2/low*float(np.trace(prod@DD@gamma@DD.conj().T).real)
  table.append(dict(vrel=vr,sigma_pair_v_mu_minus2=value,gamma_C_trace=float(np.trace(gin))))
 # All other 1->2 tree decays have neutral daughters here, and no massive V
 # channel is kinematically open. Do not substitute a parent equilibrium bath.
 net=one(XP);parents=[p for p in net['neutral_parents'] if abs(p['mass']-MP)<1e-8]
 checks=dict(width_PSD=min(eg)>0,production_PSD=min(eigh(prod,eigvals_only=True))>-1e-19,diagonal_width_control=max(abs(gamma[i,i]-next(p['width'] for p in parents if p['index']==P[i])) for i in range(4))<1e-17,pole_scalar_mass=abs(2*low-MP)<1e-12,all_parent_exits_neutral=max(p['terminal_charged_multiplicity'] for p in parents)<1e-10,atrest_below_cauchy=sigma<cauchy*(1+1e-12))
 result=dict(claim_id='CT09_COHERENT_CHARGED_SCALAR_POLE',checks={k:bool(v) for k,v in checks.items()},xpole=XP,Mpole=MP,mC=low,parent_indices=P.tolist(),Gamma_other_matrix_mu=gamma.tolist(),production_Gram_mu2=prod.tolist(),Gamma_other_eigenvalues_mu=eg.tolist(),production_Gram_in_width_basis_mu2=Grot.tolist(),relative_commutator=comm,offdiagonal_production_norm=float(np.linalg.norm(off)),kappa_effective_squared_mu2=float(2*np.trace(prod)),sigma_pair_v_at_rest_mu_minus2=sigma,cauchy_upper_at_rest_mu_minus2=cauchy,velocity_table=table,scope='Leading rigid tree fourfold exact-degenerate scalar pole, absorptive matrix all open SSS/FFS channels, complete tree vector closure atpole. Physicalpair cross section averaged over6particle and6antiparticle components. No thermal selfenergy, finite-width mixing beyond absorptive tree matrix, retunedgravity packet or cosmologicalyieldsolution.',runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','xpole','Gamma_other_eigenvalues_mu','relative_commutator','kappa_effective_squared_mu2','sigma_pair_v_at_rest_mu_minus2','cauchy_upper_at_rest_mu_minus2','runtime_seconds')}));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
