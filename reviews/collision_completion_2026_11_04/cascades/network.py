"""CC10 physical grouped FFS/SSS reaction data; all masses/rates in mu units.

The group populations assume incoherence inside exactly degenerate blocks.
The four singlet scalars additionally carry per-final-group absorptive matrices.
"""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import math,json,time,resource
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/finite_matching_2026_11_01/two_loop'))
from model import build_model
from spectrum import d as DCOEF,T
E=.003

def adapt(U,values,C):
 U=U.copy();used=np.zeros(len(values),bool)
 for i,v in enumerate(values):
  if used[i]:continue
  ids=np.where(abs(values-v)<1e-10*max(1,abs(v)))[0];used[ids]=True;old=U[:,ids]
  c=old.conj().T@C@old
  _,V=eigh(c if abs(v)<1e-12 else c.real);U[:,ids]=old@V
 return U

def state(x,e=E,vertices=True):
 d=build_model(x,e,e,math.sqrt(29/200)*e,vertices=vertices)
 R=d['R'];RY=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),R);Q2=RY@RY
 # All unbroken SU3 x SU2 x U1 generators; Casimir = 3,2,0 for neutral reps.
 un=[a for a,t in enumerate(T) if np.max(abs(t@np.diag([2,2,2,-3,-3])-np.diag([2,2,2,-3,-3])@t))<1e-12]
 C=np.einsum('aij,ajk->ik',R[un],R[un])
 def fextend(c):
  out=np.zeros((73,73),complex);out[:49,:49]=c;out[49:,49:]=c[1:25,1:25];return out
 def sextend(c):return np.block([[c.real,-c.imag],[c.imag,c.real]])
 QF,CF=fextend(Q2),fextend(C);QS,CS=sextend(Q2),sextend(C)
 O=adapt(d['O'],d['mS2'],QS);O=adapt(O,d['mS2']+np.einsum('ia,ia->a',O,QS@O).real,CS)
 U=adapt(d['U'],d['mF'],QF);U=adapt(U,d['mF']+np.einsum('ia,ia->a',U.conj(),QF@U).real,CF)
 # Separate the tree Goldstino from the raw U1 gaugino in the zero block.
 GP=np.diag(np.r_[np.zeros(49),np.ones(24)])
 uv=d['mF']+np.einsum('ia,ia->a',U.conj(),QF@U).real+10*np.einsum('ia,ia->a',U.conj(),CF@U).real
 U=adapt(U,uv,GP)
 qs=np.einsum('ia,ia->a',O,QS@O).real;qf=np.einsum('ia,ia->a',U.conj(),QF@U).real
 cs=np.einsum('ia,ia->a',O,CS@O).real;cf=np.einsum('ia,ia->a',U.conj(),CF@U).real
 gf=np.einsum('ia,ia->a',U.conj(),GP@U).real
 mass=np.r_[np.sqrt(np.maximum(d['mS2'],0)),d['mF']];charged=np.r_[qs>.1,qf>.1]
 physical=np.r_[(d['mS2']>1e-15)|(qs<.01),np.ones(73,bool)]
 cas=np.r_[cs,cf];gp=np.r_[np.zeros(98),gf];groups=[];mapping=np.full(171,-1,int)
 # Group by representation and mass, then give mass-ordered stable identities.
 for kind,inds in (('S',range(98)),('F',range(98,171))):
  for rep,condition in (('c',charged),('8',(~charged)&(abs(cas-3)<1e-6)),('3',(~charged)&(abs(cas-2)<1e-6)),('1',(~charged)&(abs(cas)<1e-6))):
   eligible=[i for i in inds if physical[i] and condition[i]];local=[]
   for i in sorted(eligible,key=lambda j:mass[j]):
    gauge=int(kind=='F' and mass[i]<1e-12 and gp[i]>.5)
    match=next((z for z in local if abs(z['mass']-mass[i])<1e-9 and z['raw_gaugino']==gauge),None)
    if match is None:local.append(dict(indices=[int(i)],mass=float(mass[i]),raw_gaugino=gauge))
    else:match['indices'].append(int(i))
   for rank,z in enumerate(local):
    z.update(id=kind+rep+'_'+str(rank),kind=kind,rep=rep,charged=rep=='c',degeneracy=len(z['indices'])*(1 if kind=='S' else 2),mass=float(np.mean(mass[z['indices']])),q2=float(np.mean(np.r_[qs,qf][z['indices']])),casimir=float(np.mean(cas[z['indices']])))
    mapping[z['indices']]=len(groups);groups.append(z)
 assert np.all(mapping[physical]>=0)
 out=dict(x=float(x),e=float(e),groups=groups,mapping=mapping,mass=mass,charged=charged,physical=physical,mV=float(math.sqrt(max(d['mV2']))),checks=dict(charged_real_scalars=int(sum(physical[:98]&charged[:98]))==36,charged_Weyls=int(sum(charged[98:]))==36,excluded_Goldstones=int(sum(~physical))==12,Takagi_error=float(np.max(abs(U.T@d['MF']@U-np.diag(d['mF'])))),charge_spectrum_error=float(max(np.max(abs(qs-np.round(qs/(5/12))*(5/12))),np.max(abs(qf-np.round(qf/(5/12))*(5/12)))))))
 if vertices:
  RS=d['O'].T@O;RF=d['U'].conj().T@U
  out['c3']=np.einsum('ia,jb,kc,ijk->abc',RS,RS,RS,d['cubic'],optimize=True)
  out['yy']=np.einsum('iu,jv,ka,ijk->uva',RF,RF,RS,d['yukawa'],optimize=True)
 return out

def table(x,e=E,derivative=True):
 s=state(x,e);groups=s['groups'];mass=s['mass'];physical=s['physical'];mp=s['mapping'];mS=mass[:98];mF=mass[98:];c3=s['c3'];yy=s['yy'];raw=[];channel_matrices={}
 for a,M in enumerate(mS):
  if not physical[a] or M<1e-12:continue
  z=mF/M;ri=z[:,None]**2;rj=z[None,:]**2;phase=np.sqrt(np.maximum(0,(1-ri-rj)**2-4*ri*rj));allow=z[:,None]+z[None,:]<1-1e-12;y=yy[:,:,a]
  wf=M/(16*math.pi)*phase*(abs(y)**2*(1-ri-rj)-2*(y*y).real*z[:,None]*z[None,:])*allow
  z=mS/M;ri=z[:,None]**2;rj=z[None,:]**2;phase=np.sqrt(np.maximum(0,(1-ri-rj)**2-4*ri*rj));allow=(z[:,None]+z[None,:]<1-1e-12)&physical[:98,None]&physical[None,:98]
  ws=c3[a]**2/(32*math.pi*M)*phase*allow
  for values,offset,typ in ((wf,98,'FF'),(ws,0,'SS')):
   for i,j in zip(*np.where(np.triu(values)>1e-27)):
    raw.append((a,i+offset,j+offset,float(values[i,j]*(1 if i==j else 2)),typ))
 for i,M in enumerate(mF):
  if M<1e-12:continue
  z=mF/M;t=mS/M;ri=z[:,None]**2;rs=t[None,:]**2;phase=np.sqrt(np.maximum(0,(1-ri-rs)**2-4*ri*rs));allow=(z[:,None]+t[None,:]<1-1e-12)&physical[None,:98];y=yy[i]
  wf=M/(16*math.pi)*phase*(abs(y)**2*(1+ri-rs)+2*(y*y).real*z[:,None])*allow
  for j,a in zip(*np.where(wf>1e-27)):raw.append((98+i,98+j,a,float(wf[j,a]),'FS'))
 agg={}
 for a,j,k,w,typ in raw:
  key=(int(mp[a]),*sorted((int(mp[j]),int(mp[k]))),typ);agg[key]=agg.get(key,0.)+w/len(groups[mp[a]]['indices'])
 channels=[]
 for (a,j,k,typ),w in sorted(agg.items()):
  if w<1e-25:continue
  A,J,K=(groups[i] for i in (a,j,k));nq=int(J['charged'])+int(K['charged'])-int(A['charged'])
  assert (not A['charged'] and nq in (0,2)) or (A['charged'] and nq==0)
  channels.append(dict(parent=A['id'],daughters=[J['id'],K['id']],width=w,kind=typ,carrier_delta=nq))
 if derivative:
  step=1e-4;plus={g['id']:g for g in state(x+step,e,False)['groups']};minus={g['id']:g for g in state(max(0,x-step),e,False)['groups']};dx=(x+step)-max(0,x-step)
 for a,A in enumerate(groups):
  A['width']=sum(z['width'] for z in channels if z['parent']==A['id'])
  A['vector_kinematically_possible']=bool(A['mass']>s['mV'])
  if derivative:
   # Stable identities are representation and mass-rank based away from crossings.
   A['dm2_dx']=(plus[A['id']]['mass']**2-minus[A['id']]['mass']**2)/dx
   A['dm_dx']=A['dm2_dx']/(2*A['mass']) if A['mass']>1e-12 else 0.
 # Empty-state terminal statistics, for validation only, never as evolution sink.
 terminal={}
 for A in sorted(groups,key=lambda z:z['mass']):
  rows=[z for z in channels if z['parent']==A['id']]
  if not rows:terminal[A['id']]={A['id']:1.}
  else:
   z={}
   for c in rows:
    for daughter in c['daughters']:
     for key,num in terminal[daughter].items():z[key]=z.get(key,0.)+c['width']/A['width']*num
   terminal[A['id']]=z
 by={g['id']:g for g in groups}
 for A in groups:
  A['terminal_charged']=sum(v*by[k]['charged'] for k,v in terminal[A['id']].items())
  A['terminal_multiplicities']=terminal[A['id']]
 # Per-channel singlet absorptive matrices in the actual adapted basis.
 P=[i for i in range(98) if physical[i] and not s['charged'][i] and abs(mS[i]-math.sqrt(2*e))<1e-8]
 if len(P)==4:
  M=float(mS[P[0]]);ci=c3[P];y=yy[:,:,P].transpose(2,0,1)
  for typ,offset,ms in (('FF',98,mF),('SS',0,mS)):
   z=ms/M;ri=z[:,None]**2;rj=z[None,:]**2;phase=np.sqrt(np.maximum(0,(1-ri-rj)**2-4*ri*rj));allow=z[:,None]+z[None,:]<1-1e-12
   if typ=='SS':allow&=physical[:98,None]&physical[None,:98]
   for j,J in enumerate(groups):
    if (J['kind']=='F')!=(typ=='FF'):continue
    for k in range(j,len(groups)):
     K=groups[k]
     if K['kind']!=J['kind']:continue
     ids=np.array(J['indices'])-offset;kds=np.array(K['indices'])-offset;mask=np.zeros_like(phase);mask[np.ix_(ids,kds)]=1
     if j!=k:mask[np.ix_(kds,ids)]=1
     fact=phase*allow*mask
     if typ=='SS':mat=np.einsum('aij,bij,ij->ab',ci,ci,fact)/(32*math.pi*M)
     else:mat=M/(16*math.pi)*(np.einsum('aij,bij,ij->ab',y,y.conj(),fact*(1-ri-rj)).real-2*np.einsum('aij,bij,ij->ab',y,y,fact*z[:,None]*z[None,:]).real)
     if np.linalg.norm(mat)>1e-24:channel_matrices[J['id']+'|'+K['id']]=mat.tolist()
 return dict(x=float(x),e=float(e),groups=groups,channels=channels,singlet_indices=P,singlet_channel_Gamma=channel_matrices,m_vector=s['mV'],checks=s['checks'],raw_channel_count=len(raw),coverage='Every physical tree FFS/SSS state, all 12 charged Goldstones removed; massive-vector and loop exits omitted; diagonal group populations require decoherence except supplied singlet channel matrices.')

def signed_lift(data):
 """Charge-conjugation-symmetric lift. g counts scalar real/spin-Weyl states."""
 species=[];by={g['id']:g for g in data['groups']};channels=[]
 for g in data['groups']:
  for sign in ((1,-1) if g['charged'] else (0,)):
   z=dict(g);z.update(id=g['id']+('+' if sign==1 else '-' if sign==-1 else ''),charge=sign,degeneracy=g['degeneracy']/(2 if sign else 1));species.append(z)
 for c in data['channels']:
  p=c['parent'];j,k=c['daughters'];P,J,K=(by[t] for t in (p,j,k))
  if P['charged']:
   for sign,suffix in ((1,'+'),(-1,'-')):
    channels.append(dict(c,parent=p+suffix,daughters=[j+(suffix if J['charged'] else ''),k+(suffix if K['charged'] else '')]))
  elif J['charged']:
   if j==k:channels.append(dict(c,parent=p,daughters=[j+'+',k+'-']))
   else:
    for sj,sk in (('+','-'),('-','+')):channels.append(dict(c,parent=p,daughters=[j+sj,k+sk],width=c['width']/2))
  else:channels.append(dict(c))
 return species,channels

def two_body(M,m1,m2,P,cosine):
 """Exact parent-frame isotropic node, boosted along z; returns four-vectors."""
 q=math.sqrt(max(0,(M*M-(m1+m2)**2)*(M*M-(m1-m2)**2)))/(2*M)
 e1=(M*M+m1*m1-m2*m2)/(2*M);e2=M-e1;E=math.sqrt(M*M+P*P);ga=E/M;v=P/E
 st=math.sqrt(max(0,1-cosine*cosine));p1=np.array([ga*(e1+v*q*cosine),q*st,0.,ga*(q*cosine+v*e1)]);p2=np.array([ga*(e2-v*q*cosine),-q*st,0.,ga*(-q*cosine+v*e2)])
 return np.array([E,0.,0.,P]),p1,p2

def main(out):
 start=time.monotonic();rows=[]
 for x in (0.18444259422092926,3.,5.,10.,20.,25.399,25.4000254000381,30.):
  r=table(x);rows.append(r);print(x,len(r['groups']),len(r['channels']),flush=True)
 checks=dict(all_charge_counts=all(r['checks']['charged_real_scalars'] and r['checks']['charged_Weyls'] and r['checks']['excluded_Goldstones'] for r in rows),Takagi=max(r['checks']['Takagi_error'] for r in rows)<1e-9,charge=max(r['checks']['charge_spectrum_error'] for r in rows)<1e-9)
 result=dict(claim_id='CC10_GROUPED_CASCADE_NETWORK',cases=rows,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
