"""CT09 charge-adapted 1->2 tree network and NR gauge annihilation baseline."""
import os,sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
 os.environ[key]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/finite_matching_2026_11_01/two_loop'))
from model import build_model
from spectrum import d as DCOEF,T
E=.003;G=math.sqrt(29/200)*E;A=math.sqrt(2/(31*E))

def adapt(U,values,C):
 U=U.copy();used=np.zeros(len(values),bool)
 for i,v in enumerate(values):
  if used[i]:continue
  ids=np.where(abs(values-v)<1e-10*max(1,abs(v)))[0];used[ids]=True;old=U[:,ids]
  c=old.conj().T@C@old
  # Orthogonal change preserves a nonzero degenerate Takagi block.
  w,V=eigh(c if abs(v)<1e-12 else c.real);U[:,ids]=old@V
 return U

def one(x,e=E):
 g=math.sqrt(29/200)*e;aa=math.sqrt(2/(31*e));d=build_model(x,e,e,g,vertices=True)
 RY=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),d['R']);Q2=RY@RY
 QF=np.zeros((73,73),complex);QF[:49,:49]=Q2;QF[49:,49:]=Q2[1:25,1:25]
 CS=np.block([[Q2.real,-Q2.imag],[Q2.imag,Q2.real]])
 O=adapt(d['O'],d['mS2'],CS);U=adapt(d['U'],d['mF'],QF)
 qs=np.einsum('ia,ia->a',O,CS@O).real;qf=np.einsum('ia,ia->a',U.conj(),QF@U).real
 mS=np.sqrt(np.maximum(d['mS2'],0));mF=d['mF'];phys=(d['mS2']>1e-15)|(qs<.01)
 RS=d['O'].T@O;RF=d['U'].conj().T@U
 c3=np.einsum('ia,jb,kc,ijk->abc',RS,RS,RS,d['cubic'],optimize=True)
 yy=np.einsum('iu,jv,ka,ijk->uva',RF,RF,RS,d['yukawa'],optimize=True)
 # Every channel is a physical ordered-sum convention with identical factor.
 channels={};widths=np.zeros(171);neutral_massless=np.where((qf<.01)&(mF<1e-12))[0]
 for a,M in enumerate(mS):
  if not phys[a] or M<1e-12:continue
  z=mF/M;ri=z[:,None]**2;rj=z[None,:]**2
  lam=np.sqrt(np.maximum(0,(1-ri-rj)**2-4*ri*rj));allow=z[:,None]+z[None,:]<1-1e-12;y=yy[:,:,a]
  wf=M/(16*math.pi)*lam*(abs(y)**2*(1-ri-rj)-2*(y*y).real*z[:,None]*z[None,:])*allow
  z=mS/M;ri=z[:,None]**2;rj=z[None,:]**2
  lam=np.sqrt(np.maximum(0,(1-ri-rj)**2-4*ri*rj));allow=(z[:,None]+z[None,:]<1-1e-12)&phys[:,None]&phys[None,:]
  ws=c3[a]**2/(32*math.pi*M)*lam*allow
  ch=[]
  for i,j in zip(*np.where(np.triu(wf)>1e-26)):
   ch.append((float(wf[i,j]*(1 if i==j else 2)),98+int(i),98+int(j),'FF'))
  for i,j in zip(*np.where(np.triu(ws)>1e-26)):
   ch.append((float(ws[i,j]*(1 if i==j else 2)),int(i),int(j),'SS'))
  channels[a]=ch;widths[a]=sum(w for w,*_ in ch)
 for i,M in enumerate(mF):
  if M<1e-12:continue
  z=mF/M;t=mS/M;ri=z[:,None]**2;rs=t[None,:]**2
  lam=np.sqrt(np.maximum(0,(1-ri-rs)**2-4*ri*rs));allow=(z[:,None]+t[None,:]<1-1e-12)&phys[None,:]
  y=yy[i]
  wf=M/(16*math.pi)*lam*(abs(y)**2*(1+ri-rs)+2*(y*y).real*z[:,None])*allow
  ch=[(float(wf[j,a]),98+int(j),int(a),'FS') for j,a in zip(*np.where(wf>1e-26))]
  channels[98+i]=ch;widths[98+i]=sum(w for w,*_ in ch)
 # Mass DAG cascade. Terminal = tree-stable w.r.t. included FFS/SSS exits.
 mass=np.r_[mS,mF];charged=np.r_[qs>.1,qf>.1];terminal=np.zeros((171,171))
 for i in np.argsort(mass):
  ch=channels.get(int(i),[])
  if not ch:terminal[i,i]=1
  else:
   for w,j,k,_ in ch:
    assert mass[j]<mass[i]+1e-12 and mass[k]<mass[i]+1e-12
    terminal[i]+=(w/widths[i])*(terminal[j]+terminal[k])
 expected=terminal@charged.astype(float)
 ml=np.linalg.eigvalsh([[e*x/2,-e*aa/2,5*g*aa],[-e*aa/2,0,5*g*x],[5*g*aa,5*g*x,0]])[1]
 light=np.where((qf>.1)&(abs(mF-ml)<1e-8))[0];assert len(light)==12
 chargedScalars=sorted(set(round(float(mS[a]),12) for a in np.where(phys&(qs>.1))[0]))
 minS=chargedScalars[0]
 def compact_parent(i):
  ch=channels.get(i,[]);out={}
  for w,j,k,typ in ch:
   category=typ+('_charged' if charged[j] or charged[k] else '_neutral')
   out[category]=out.get(category,0)+w
  return dict(index=int(i),kind='S' if i<98 else 'F',mass=float(mass[i]),width=float(widths[i]),partial_widths=out,terminal_charged_multiplicity=float(expected[i]),terminal_neutral_massive_multiplicity=float(terminal[i,(~charged)&(mass>1e-12)].sum()),terminal_neutral_massless_multiplicity=float(terminal[i,(~charged)&(mass<1e-12)].sum()))
 lightS=np.where(phys&(qs>.1)&(abs(mS-minS)<1e-8))[0]
 parents=[]
 for a in range(98):
  if qs[a]>.01 or not phys[a] or mS[a]<1e-12:continue
  tolight=sum(w for w,j,k,typ in channels.get(a,[]) if typ=='FF' and j-98 in light and k-98 in light)
  tocscalar=sum(w for w,j,k,typ in channels.get(a,[]) if typ=='SS' and j in lightS and k in lightS)
  if True:
   p=compact_parent(a);p['to_light_pair']=tolight;p['to_light_scalar_pair']=tocscalar
   p['terminal_daughters']=[dict(index=int(j),mass=float(mass[j]),charged=bool(charged[j]),expected_number=float(terminal[a,j])) for j in np.where(terminal[a]>1e-8)[0]]
   parents.append(p)
 lf=[]
 for i in light:
  p=compact_parent(98+int(i));p['to_massless_neutral_F_plus_charged_S']=sum(w for w,j,k,typ in channels.get(98+int(i),[]) if j-98 in neutral_massless and qs[k]>.1)
  lf.append(p)
 # Group-degenerate summary; retain each raw parent for reproducibility.
 groups=[]
 for p in sorted(parents,key=lambda a:a['mass']):
  if groups and abs(p['mass']-groups[-1]['mass'])<1e-9:
   groups[-1]['multiplicity']+=1
  else:
   groups.append(dict(mass=p['mass'],multiplicity=1,width=p['width'],to_light_pair=p['to_light_pair'],partial_widths=p['partial_widths'],terminal_charged_multiplicity=p['terminal_charged_multiplicity'],terminal_neutral_massive_multiplicity=p['terminal_neutral_massive_multiplicity'],terminal_neutral_massless_multiplicity=p['terminal_neutral_massless_multiplicity']))
 checks=dict(charge_adaptation=float(max(np.max(abs(qs-np.round(qs/(5/12))*(5/12))),np.max(abs(qf-np.round(qf/(5/12))*(5/12)))))<1e-9,Takagi=float(np.max(abs(U.T@d['MF']@U-np.diag(mF))))<1e-9,nonnegative_all_widths=bool(min(widths)>-1e-23),physical_charged_scalars=int(sum(phys&(qs>.1)))==36,charged_Weyls=int(sum(qf>.1))==36)
 return dict(x=float(x),e=float(e),m_light_F=float(ml),charged_scalar_mass_groups=chargedScalars,m_light_S=minS,m_light_vector=float(math.sqrt(max(d['mV2']))),light_F_mean_width=float(np.mean(widths[98+light])),light_F_mean_to_massless_gaugino_S=float(np.mean([p['to_massless_neutral_F_plus_charged_S'] for p in lf])),light_F_terminal_charged=float(np.mean(expected[98+light])),light_F=lf,neutral_parent_groups=groups,neutral_parents=parents,checks=checks)

