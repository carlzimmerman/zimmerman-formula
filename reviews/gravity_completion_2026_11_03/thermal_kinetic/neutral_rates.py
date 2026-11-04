"""Actual tree neutral-scalar -> charged-light-fermion partial widths."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.linalg import eigh
from scipy.special import kv
from scipy.integrate import quad
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/finite_matching_2026_11_01/two_loop'))
from model import build_model
from spectrum import d as DCOEF
from stationary import light,E,G

def one(x,ts,mus):
 data=build_model(x,E,E,G,vertices=False);n=49;nf=73
 RY=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),data['R']);Q2=RY@RY
 QF=np.zeros((nf,nf),complex);QF[:n,:n]=Q2;QF[n:,n:]=Q2[1:25,1:25]
 m,dm=light(x)
 if x==0:
  uu=data['U'][:,data['mF']<1e-10];v,U=eigh(uu.conj().T@QF@uu);ul=uu@U[:,v>.1]
 else:ul=data['U'][:,abs(data['mF']-m)<1e-8*max(1,m)]
 assert ul.shape[1]==12,ul.shape
 charge_error=float(np.max(abs(ul.conj().T@QF@ul-np.eye(12)*5/12)))
 # Adapt scalar degeneracies to residual U1 charge squared.
 O=data['O'].copy();ms=data['mS2'];CS=np.block([[Q2.real,-Q2.imag],[Q2.imag,Q2.real]])
 used=np.zeros(len(ms),bool)
 for i,m2 in enumerate(ms):
  if used[i]:continue
  ids=np.where(abs(ms-m2)<1e-10*max(1,m2))[0];used[ids]=True;old=O[:,ids];cc,uu=eigh(old.T@CS@old);O[:,ids]=old@uu
 Em=data['E']@O
 dy=np.zeros((nf,nf,len(ms)),complex);dy[:n,:n]=np.einsum('ijk,ka->ija',data['Y'],Em,optimize=True)
 dJ=math.sqrt(2)*G*np.einsum('ka,pki->pia',Em.conj(),data['R'],optimize=True)
 dy[n:,:n]=dJ;dy[:n,n:]=dJ.transpose(1,0,2)
 yy=np.einsum('Iu,Jv,IJa->uva',ul,ul,dy,optimize=True)
 qcharge=np.einsum('ia,ia->a',O,CS@O)
 widths=[]
 for a,m2 in enumerate(ms):
  if m2<=0 or qcharge[a]>.01 or m2<4*m*m:continue
  mass=math.sqrt(m2);r=m*m/m2;Y=yy[:,:,a]
  width=mass/(16*math.pi)*math.sqrt(max(0,1-4*r))*float(np.sum(abs(Y)**2*(1-2*r)-2*(Y*Y).real*r))
  if width<1e-25:continue
  widths.append(dict(scalar_index=a,mass_over_mu=mass,width_over_mu=width,yukawa_norm2=float(np.sum(abs(Y)**2))))
 rates=[]
 for t in ts:
  # Parent MB approximation; actual masses enter and all open neutral parents
  # are included. For Tc=.004--.005 parents satisfy M/T >=~4.
  density_frozen=24*3*1.202056903159594/(4*math.pi**2)*t**3
  density_eq=24*t**3/(2*math.pi**2)*quad(lambda p:p*p*math.exp(-math.sqrt(p*p+(m/t)**2))/(1+math.exp(-math.sqrt(p*p+(m/t)**2))),0,70)[0]
  gamma=sum(q['mass_over_mu']**2*t/(2*math.pi**2)*kv(1,q['mass_over_mu']/t)*q['width_over_mu'] for q in widths)
  rate=2*gamma/density_eq
  # Existing U1 -> two massless U1 photons, NR limit only, per same component.
  alpha=G*G*(5/12)/(4*math.pi)
  direct=(3*1.202056903159594/(2*math.pi**2))*t**3*math.pi*alpha**2/(m*m) if m/t>3 else None
  rows=[]
  for kind,mu in mus.items():
   H=math.sqrt(math.pi**2*106.75/90)*(t*mu/.02)**2/2.435e18
   rows.append(dict(kind=kind,H_GeV=H,inverse_equilibrium_loss_rate_GeV=rate*mu,inverse_rate_over_H=rate*mu/H,inverse_rate_over_origin_roll=rate/1.825e-6,U1_NR_direct_rate_GeV=None if direct is None else direct*mu,U1_NR_direct_over_H=None if direct is None else direct*mu/H))
  rates.append(dict(t=t,m_over_t=m/t,frozen_number_mu3=density_frozen,equilibrium_number_mu3=density_eq,inverse_reaction_density_mu4=gamma,comparisons=rows))
 return dict(x=x,light_mass_over_mu=m,charge_matrix_error=charge_error,open_neutral_scalar_count=len(widths),neutral_scalar_partial_widths=widths,rates=rates)

def main(out):
 start=time.monotonic();mus={'canonical':544638.2663769713,'protected':18170662.111498855}
 rows=[one(x,[.00466,.004,.003,.002,.001],mus) for x in (0,.184443,.26895,1,3,5,10,20,25)]
 checks={'12_charged_Weyls':True,'U1_charge_squared':max(r['charge_matrix_error'] for r in rows)<1e-10,'positive_partial_widths':all(q['width_over_mu']>0 for r in rows for q in r['neutral_scalar_partial_widths'])}
 result=dict(claim_id='TK08_ACTUAL_NEUTRAL_INVERSE_DECAYS',checks=checks,cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Exact rigid tree neutral scalar to 12 light charged Weyls partial widths and equilibrium detailed-balance reaction densities with Maxwell-Boltzmann parent approximation. This is not the nonequilibrium inverse-decay rate for a heavy frozen FD population; no all-channel collision solution. U1 direct channel only is not a total annihilation upper bound.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
