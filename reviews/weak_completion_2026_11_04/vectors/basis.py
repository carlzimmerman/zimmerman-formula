"""Actual canonical gauge currents, physical scalar projection, and SVV vertices.

All masses and widths in mu units. Gauge tr(t_A t_B)=delta_AB/2.
Only canonical physical scalar columns survive; no Goldstone is a gas species.
"""
import os,sys,math
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3];OLD=ROOT/'reviews/collision_completion_2026_11_04'
sys.path.insert(0,str(OLD/'cascades'))
from network import state,adapt,build_model,DCOEF,T

def real_generator(q):
 return np.array([np.block([[1j*r.imag,1j*r.real],[-1j*r.real,1j*r.imag]]) for r in q])

def build(x,e=.003):
 d=build_model(x,e,e,math.sqrt(29/200)*e,vertices=True);R=d['R']
 un=np.array([a for a,t in enumerate(T) if np.max(abs(t@np.diag([2,2,2,-3,-3])-np.diag([2,2,2,-3,-3])@t))<1e-12])
 RY=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),R);Q2=RY@RY;C=np.einsum('aij,ajk->ik',R[un],R[un])
 def fe(c):
  z=np.zeros((73,73),complex);z[:49,:49]=c;z[49:,49:]=c[1:25,1:25];return z
 def se(c):return np.block([[c.real,-c.imag],[c.imag,c.real]])
 QS,CS=se(Q2),se(C);QF,CF=fe(Q2),fe(C)
 O=adapt(d['O'],d['mS2'],QS);O=adapt(O,d['mS2']+np.einsum('ia,ia->a',O,QS@O).real,CS)
 U=adapt(d['U'],d['mF'],QF);U=adapt(U,d['mF']+np.einsum('ia,ia->a',U.conj(),QF@U).real,CF)
 GP=np.diag(np.r_[np.zeros(49),np.ones(24)]);uv=d['mF']+np.einsum('ia,ia->a',U.conj(),QF@U).real+10*np.einsum('ia,ia->a',U.conj(),CF@U).real
 U=adapt(U,uv,GP)
 # Resolve the three massless adjoint irreps before forming vector group traces.
 V=adapt(d['Ov'],d['mV2'],C[1:25,1:25]);mV=np.sqrt(np.maximum(d['mV2'],0));cv=np.einsum('ia,ij,ja->a',V,C[1:25,1:25],V).real
 q=np.einsum('ai,ajk->ijk',V,R);qs=np.einsum('ia,kij,jb->kab',O,real_generator(q),O,optimize=True);qf=np.einsum('ia,kij,jb->kab',U.conj(),np.array([fe(t) for t in q]),U,optimize=True)
 qv=np.einsum('ia,kij,jb->kab',V,q[:,1:25,1:25],V,optimize=True)
 Em=d['E']@O;rz=np.einsum('aij,j->ai',R,d['z']);re=np.einsum('aij,jk->aik',R,Em)
 K=2*d['g']**2*(np.einsum('pia,qi->apq',re.conj(),rz)+np.einsum('pi,qia->apq',rz.conj(),re)).real;K=np.einsum('pi,apq,qj->aij',V,K,V,optimize=True)
 RS=d['O'].T@O;RF=d['U'].conj().T@U
 cube=np.einsum('ia,jb,kc,ijk->abc',RS,RS,RS,d['cubic'],optimize=True);yuk=np.einsum('iu,jv,ka,ijk->uva',RF,RF,RS,d['yukawa'],optimize=True)
 s=state(x,e,False);physical=s['physical'][:98];massive=np.where(mV>1e-9)[0];massless=np.where(mV<1e-9)[0]
 gold=math.sqrt(2)*np.r_[-rz.imag.T,rz.real.T]@V[:,massive];gold/=np.linalg.norm(gold,axis=0)[None,:];G=O.T@gold
 cg=np.einsum('aij,ak->kij',cube,G);yg=np.einsum('ija,ak->kij',yuk,G)
 # Gauge invariance predicts the scalar/Goldstone amplitude up to common sign.
 rhs=d['g']*(d['mS2'][None,:,None]-d['mS2'][None,None,:])*qs[massive].imag/mV[massive,None,None]
 mask=physical[:,None]&physical[None,:];sw=min(np.max(abs((cg-rhs)[:,mask])),np.max(abs((cg+rhs)[:,mask])))
 # Goldstone Majorana vertex fixed by divergence of the actual Weyl current.
 yr=d['g']*(d['mF'][None,:,None]*qf[massive]+d['mF'][None,None,:]*qf[massive].conj())/mV[massive,None,None]
 # Allow the canonical Goldstone's uniform i phase and tangent orientation.
 fw=min(np.max(abs(yg-v*yr)) for v in (1,-1,1j,-1j))
 controls=dict(gold_orthonormal=float(np.max(abs(G.T@G-np.eye(12)))),gold_physical_overlap=float(np.max(abs(G[physical]))),scalar_Goldstone_Ward=float(sw),fermion_Goldstone_Ward=float(fw),Takagi=float(np.max(abs(U.T@d['MF']@U-np.diag(d['mF'])))),physical_mixed_SVV=float(np.max(abs(K[np.ix_(np.where(physical)[0],massless,massive)]))),massless_VSS_mass_commutator=float(np.max(abs(qs[massless]*(d['mS2'][None,:,None]-d['mS2'][None,None,:])))),massless_VFF_mass_commutator=float(np.max(abs(qf[massless]*(d['mF'][None,:,None]-d['mF'][None,None,:])))),Majorana_vector_axial_interference=float(np.max(abs((1j*qf.imag)*qf.real))))
 vgroups={'Vc':massive,'V8':np.where((mV<1e-9)&(abs(cv-3)<1e-6))[0],'V3':np.where((mV<1e-9)&(abs(cv-2)<1e-6))[0],'V1':np.where((mV<1e-9)&(abs(cv)<1e-6))[0]}
 return dict(d=d,s=s,qs=qs,qf=qf,qv=qv,K=K,cube=cube,yuk=yuk,gold=G,vgroups=vgroups,controls=controls,mV=mV)

def invariants(x,e=.003):
 b=build(x,e);s=b['s'];groups=s['groups'];out=[];g2=b['d']['g']**2
 # A,B store squared currents per raw parent (parent spin already averaged
 # by the covariant tensors). Scalar-vector K stores squared SVV coupling.
 for vi,ids in b['vgroups'].items():
  for i,I in enumerate(groups):
   if I['kind'] not in ('S','F'):continue
   ii=np.array(I['indices'])-(98 if I['kind']=='F' else 0)
   for j,J in enumerate(groups):
    if J['kind']!=I['kind']:continue
    jj=np.array(J['indices'])-(98 if J['kind']=='F' else 0)
    q=b['qs' if I['kind']=='S' else 'qf'][np.ix_(ids,ii,jj)]
    A=float(g2*np.sum(abs(q)**2));B=float(g2*np.sum((q*q).real))
    if A>1e-25:out.append(dict(kind='VSS' if I['kind']=='S' else 'VFF',vector=vi,i=I['id'],j=J['id'],A=A,B=B,n_i=len(ii),n_j=len(jj),n_v=len(ids)))
  if vi=='Vc':
   for I in groups:
    if I['kind']!='S':continue
    value=float(np.sum(b['K'][np.ix_(np.array(I['indices']),ids,ids)]**2))
    if value>1e-25:out.append(dict(kind='SVV',vector=vi,i=I['id'],K2=value,n_i=len(I['indices']),n_v=len(ids)))
 return dict(x=float(x),e=e,groups=groups,invariants=out,controls=b['controls'],vector_masses={k:float(np.mean(b['mV'][v])) for k,v in b['vgroups'].items()},vector_degeneracies={k:len(v) for k,v in b['vgroups'].items()})
