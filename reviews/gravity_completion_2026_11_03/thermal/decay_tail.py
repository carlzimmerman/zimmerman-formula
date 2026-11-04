"""TH07C actual U1 messenger Yukawas; no assumed final FD population."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
from scipy.special import kv,zeta
from scipy.integrate import quad
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import build_model,ext_basis
CAN=json.loads((HERE.parent/'canonical/run_highprecision/result.json').read_text());PRO=json.loads((HERE.parent/'protected/run_export_002/result.json').read_text());STATIC=json.loads((HERE/'run_static_001/result.json').read_text())
E=.003;G=math.sqrt(29/200)*E;MP=2.435e18;XI=.02;GS=106.75

def main(out):
 start=time.monotonic();points=[];checks={}
 for kind in ['canonical','protected']:
  if kind=='canonical':p=CAN['candidate'];mu=p['mu_GeV'];X=p['R_GeV']/mu/math.sqrt(31);mchi=p['gauginos_GeV']['U1']
  else:p=PRO['preferred_row'];mu=float(PRO['normalized_packet']['constants']['MU']);X=float(p['X_GeV'])/mu;mchi=p['photino_GeV']
  Tlim=next(p for p in STATIC['points'] if p['kind']==kind)['spins'][1]['TD_GeV']
  d=build_model(X,E,E,G,vertices=False);ext,C=ext_basis(d);u=ext[:,np.where(abs(C)<1e-7)[0][0]];n=len(d['z']);nf=len(d['mF'])
  rz=np.einsum('aij,j->ai',d['R'],d['z']);Gold=np.concatenate([-rz.imag,rz.real],axis=1).T
  Q= np.linalg.svd(Gold,full_matrices=False)[0][:,:12]
  ids=np.where(d['mS2']>0)[0];On=d['O'][:,ids];Z=null_space(np.vstack([Q.T,On.T]),rcond=1e-9)
  O=np.column_stack([On,Z]);ms=np.r_[np.sqrt(d['mS2'][ids]),np.zeros(Z.shape[1])];mf=d['mF'];Em=d['E']@O
  dy=np.zeros((nf,nf,len(ms)),complex);dy[:n,:n]=np.einsum('ijk,ka->ija',d['Y'],Em)
  dJ=math.sqrt(2)*G*np.einsum('ka,pki->pia',Em.conj(),d['R']);dy[n:,:n]=dJ;dy[:n,n:]=dJ.transpose(1,0,2)
  yy=np.einsum('I,JK,IJk->Kk',u,d['U'],dy,optimize=True);ysq=abs(yy)**2
  # External Weyl normalization and real scalar S Yukawa conventions fixed in derivation.
  GSarr=np.zeros(len(ms));GFarr=np.zeros(len(mf))
  channels=[]
  for i in range(len(mf)):
   for j in range(len(ms)):
    if ysq[i,j]<1e-24:continue
    if ms[j]>mf[i] and ms[j]>0:
     width=ysq[i,j]*ms[j]*mu/(8*math.pi)*(1-mf[i]**2/ms[j]**2)**2;GSarr[j]+=width;parent='S';M=ms[j]*mu;D=mf[i]*mu
    elif mf[i]>ms[j] and mf[i]>0:
     width=ysq[i,j]*mf[i]*mu/(16*math.pi)*(1-ms[j]**2/mf[i]**2)**2;GFarr[i]+=width;parent='F';M=mf[i]*mu;D=ms[j]*mu
    else:continue
    if width>1e-30:channels.append(dict(parent=parent,M_GeV=float(M),daughter_GeV=float(D),y2=float(ysq[i,j]),Gamma_GeV=float(width)))
  sourceS=ms[GSarr>1e-30]*mu;sourceF=mf[GFarr>1e-30]*mu;gamS=GSarr[GSarr>1e-30];gamF=GFarr[GFarr>1e-30]
  masses=np.r_[sourceS,sourceF];widths=np.r_[gamS,gamF];degs=np.r_[np.ones(len(sourceS)),np.full(len(sourceF),2)]
  rates=[]
  for TR in (Tlim*.25,Tlim*.5,Tlim*.75,Tlim):
   H=math.sqrt(math.pi**2*GS/90)*(TR/XI)**2/MP
   gamma=float(np.sum(degs*masses*masses*TR*widths*kv(1,masses/TR)/(2*math.pi**2)))
   nchi=3*zeta(3)/(2*math.pi**2)*TR**3
   # MB thermal-parent dilute source. Inverse reactions can only reduce zero-initial-chi source.
   pref=45*MP*XI**5/(4*math.pi**4*GS*math.sqrt(math.pi**2*GS/90))
   ints=np.array([quad(lambda x:x**3*kv(1,x),float(m/TR),np.inf,epsabs=1e-120,epsrel=1e-9)[0] for m in masses])
   Y=float(pref*np.sum(degs*widths/masses**2*ints))
   rates.append(dict(TR_D_GeV=TR,TR_SM_GeV=TR/XI,H_GeV=H,gamma_chi_GeV4=gamma,chemical_source_over_nchiH=gamma/nchi/H,Y_dilute_MB_fixed_cold_vacuum=Y,target_Y=4.36e-10/mchi,fraction_target=Y*mchi/4.36e-10))
  # All-state overestimate with all292 physical dof at the lightest charged scalar.
  # Tree norm bound is background/basis independent; final gate is still leading decay-source scope.
  Rgen=np.einsum('a,aij->ij',u[n:].real,d['R']);trace=float(np.trace(Rgen@Rgen).real)
  frob_bound=2*G*G*trace
  Mmin=min(ch['daughter_GeV'] for ch in channels if ch['daughter_GeV']>0)
  cwidth=100*E*E # deliberately much looser than measured/Frobenius scalar-fermion current norm
  pref=45*MP*XI**5/(4*math.pi**4*GS*math.sqrt(math.pi**2*GS/90));integral=quad(lambda x:x**3*kv(1,x),Mmin/Tlim,np.inf,epsabs=1e-120,epsrel=1e-10)[0]
  envelope=292*pref*cwidth/Mmin*integral
  checks[kind+'_physical_scalar86']=len(ms)==86
  checks[kind+'_physical_goldstone_removed']=float(np.max(abs(Q.T@O)))<1e-8
  checks[kind+'_Yukawa_norm_bounded']=float(np.sum(ysq))<=frob_bound*(1+1e-10)
  checks[kind+'_dilute_chi_tail']=max(r['chemical_source_over_nchiH'] for r in rates)<1e-3
  checks[kind+'_source_tiny']=rates[-1]['fraction_target']<1e-6
  points.append(dict(kind=kind,X_over_mu=X,mu_GeV=mu,mchi_GeV=mchi,cold_branch_Tlim_GeV=Tlim,scalar_count=len(ms),Goldstone_projector_residual=float(np.max(abs(Q.T@O))),zero_scalar_physical_count=Z.shape[1],U1_chiral_charge_trace=trace,U1_Yukawa_norm_total=float(np.sum(ysq)),U1_Yukawa_norm_all_real_scalar_bound=frob_bound,nonzero_decay_channel_entries=len(channels),min_source_parent_GeV=float(min(masses)),width_sum_GeV=float(sum(GSarr)+sum(GFarr)),max_scalar_width_GeV=float(max(GSarr)),max_fermion_width_GeV=float(max(GFarr)),channels=channels,rates=rates,conservative_all292_width_ratio_assumption=cwidth,conservative_Mmin_GeV=Mmin,conservative_envelope_Y=envelope,conservative_envelope_fraction_target=envelope*mchi/4.36e-10))
 result=dict(claim_id='TH07C_ACTUAL_MESSENGER_DECAY_TAIL',checks={k:bool(v) for k,v in checks.items()},inputs=dict(e=E,g=G,xi_external=XI,SM_gstar=GS,target_mchiY_GeV=4.36e-10),points=points,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actual leading physical scalar/fermion two-body U1 photino vertices; MB initial-equilibrium-parent source, zero initial chi, fixed cold vacuum, constant xi and gSM. Not all-orders inclusive rate, full bath kinetics, or evolved companion abundance. Broad envelope is conditional on stated width-ratio bound; no derived bath.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=result['checks'],runtime=result['runtime_seconds'],points=[{k:v for k,v in p.items() if k not in ['channels']} for p in points])));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
