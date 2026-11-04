"""Neutral parents: physical scalar and all-fermion tree partial widths."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import numpy as np,json,math,time,resource
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/finite_matching_2026_11_01/two_loop'))
from model import build_model
from spectrum import d as DCOEF
from stationary import E,G,light

def adapt(U,values,C,complex_basis=False):
 U=U.copy();used=np.zeros(len(values),bool);errs=[]
 for i,v in enumerate(values):
  if used[i]:continue
  ids=np.where(abs(values-v)<1e-10*max(1,abs(v)))[0];used[ids]=True;old=U[:,ids]
  c=old.conj().T@C@old
  if complex_basis and abs(v)<1e-12:
   # Arbitrary unitary rotations preserve a strictly zero Takagi block.
   q,V=eigh(c);U[:,ids]=old@V;continue
  errs.append(float(np.max(abs(c.imag))))
  # Q squared is CP even, so real orthogonal rotations preserve Takagi.
  q,V=eigh(c.real);U[:,ids]=old@V
 return U,max(errs)

def atx(x):
 d=build_model(x,E,E,G,vertices=True);n=49;nf=73
 RY=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),d['R']);Q2=RY@RY
 QF=np.zeros((nf,nf),complex);QF[:n,:n]=Q2;QF[n:,n:]=Q2[1:25,1:25]
 CS=np.block([[Q2.real,-Q2.imag],[Q2.imag,Q2.real]])
 O,errS=adapt(d['O'],d['mS2'],CS);U,errF=adapt(d['U'],d['mF'],QF,True)
 qs=np.einsum('ia,ia->a',O,CS@O).real;qf=np.einsum('ia,ia->a',U.conj(),QF@U).real
 scalarphysical=(d['mS2']>1e-15)|(qs<.01)
 # Rotate precomputed cubic to charge-adapted basis.
 OR=d['O'].T@O;cubic=np.einsum('ia,jb,kc,ijk->abc',OR,OR,OR,d['cubic'],optimize=True)
 Em=d['E']@O;dy=np.zeros((nf,nf,len(qs)),complex);dy[:n,:n]=np.einsum('ijk,ka->ija',d['Y'],Em,optimize=True)
 dJ=math.sqrt(2)*G*np.einsum('ka,pki->pia',Em.conj(),d['R'],optimize=True);dy[n:,:n]=dJ;dy[:n,n:]=dJ.transpose(1,0,2)
 yy=np.einsum('Iu,Jv,IJa->uva',U,U,dy,optimize=True)
 mF=d['mF'];mS=np.sqrt(np.maximum(d['mS2'],0));ml=light(x)[0];lightcharged=(abs(mF-ml)<1e-8)&(qf>.1)
 assert sum(lightcharged)==12,(x,sum(lightcharged),qf[abs(mF-ml)<1e-8])
 rows=[]
 for a,M in enumerate(mS):
  if qs[a]>.01 or M<1e-12:continue
  z=mF/M;ri=z[:,None]**2;rj=z[None,:]**2;phase=np.sqrt(np.maximum(0,(1-ri-rj)**2-4*ri*rj));allow=(z[:,None]+z[None,:]<1)
  y=yy[:,:,a];wf=M/(16*math.pi)*phase*(abs(y)**2*(1-ri-rj)-2*(y*y).real*z[:,None]*z[None,:])*allow
  lightwidth=float(wf[np.ix_(lightcharged,lightcharged)].sum())
  if lightwidth<1e-25:continue
  z=mS/M;phaseS=np.sqrt(np.maximum(0,(1-z[:,None]**2-z[None,:]**2)**2-4*z[:,None]**2*z[None,:]**2));ok=(z[:,None]+z[None,:]<1)&scalarphysical[:,None]&scalarphysical[None,:]
  ws=cubic[a]**2/(32*math.pi*M)*phaseS*ok
  rows.append(dict(scalar_index=a,mass=M,to_light_charged_fermions=lightwidth,to_all_fermions=float(wf.sum()),to_neutral_fermions=float(wf[np.ix_(qf<.01,qf<.01)].sum()),to_charged_fermions=float(wf[np.ix_(qf>.1,qf>.1)].sum()),to_all_physical_scalars=float(ws.sum()),to_neutral_scalars=float(ws[np.ix_(qs<.01,qs<.01)].sum()),to_charged_scalars=float(ws[np.ix_(qs>.1,qs>.1)].sum()),neutral_scalar_daughters=[dict(i=int(i),j=int(j),mi=float(mS[i]),mj=float(mS[j]),width=float(ws[i,j]*(1 if i==j else 2))) for i in range(len(qs)) for j in range(i,len(qs)) if qs[i]<.01 and qs[j]<.01 and ws[i,j]>1e-23]))
 return dict(x=x,charge_basis_imaginary_error=max(errS,errF),Takagi_error=float(np.max(abs(U.T@d['MF']@U-np.diag(mF)))),parents=rows)
def main(out):
 t=time.monotonic();rows=[atx(x) for x in (0,.26895,3,10,25)]
 checks={'charge_basis_CP_real':max(r['charge_basis_imaginary_error'] for r in rows)<1e-9,'adapted_Takagi':max(r['Takagi_error'] for r in rows)<1e-9,'nonnegative_widths':all(p[k]>-1e-20 for r in rows for p in r['parents'] for k in ('to_all_fermions','to_all_physical_scalars','to_neutral_scalars'))}
 result=dict(claim_id='TK08_NEUTRAL_BRANCHING',checks=checks,cases=rows,runtime_seconds=time.monotonic()-t,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Tree physical scalar and fermion partial widths; charged Goldstone zeros excluded. VV and Vscalar final widths not included. Immediate neutral daughters can subsequently return to charged states; branching to neutral scalars is not a proven irreversible annihilation.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
