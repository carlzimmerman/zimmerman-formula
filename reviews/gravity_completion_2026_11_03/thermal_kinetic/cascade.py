"""Focused origin neutral daughter cascade, exact tree vertices."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource,numpy as np
from branching import adapt,build_model,E,G,DCOEF
HERE=Path(__file__).resolve().parent
def main(out):
 start=time.monotonic();d=build_model(0,E,E,G,vertices=True);n=49;nf=73
 RY=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),d['R']);Q2=RY@RY;QF=np.zeros((nf,nf),complex);QF[:n,:n]=Q2;QF[n:,n:]=Q2[1:25,1:25]
 CS=np.block([[Q2.real,-Q2.imag],[Q2.imag,Q2.real]]);O,es=adapt(d['O'],d['mS2'],CS);U,ef=adapt(d['U'],d['mF'],QF,True)
 qs=np.einsum('ia,ia->a',O,CS@O).real;qf=np.einsum('ia,ia->a',U.conj(),QF@U).real
 phys=(d['mS2']>1e-15)|(qs<.01);mS=np.sqrt(np.maximum(d['mS2'],0));mF=d['mF'];OR=d['O'].T@O;cubic=np.einsum('ia,jb,kc,ijk->abc',OR,OR,OR,d['cubic'],optimize=True)
 Em=d['E']@O;dy=np.zeros((nf,nf,len(qs)),complex);dy[:n,:n]=np.einsum('ijk,ka->ija',d['Y'],Em,optimize=True);dJ=math.sqrt(2)*G*np.einsum('ka,pki->pia',Em.conj(),d['R'],optimize=True);dy[n:,:n]=dJ;dy[:n,n:]=dJ.transpose(1,0,2);yy=np.einsum('Iu,Jv,IJa->uva',U,U,dy,optimize=True)
 rows=[]
 for a,M in enumerate(mS):
  if qs[a]>.01 or M<.001:continue
  z=mF/M;ri=z[:,None]**2;rj=z[None,:]**2;phase=np.sqrt(np.maximum(0,(1-ri-rj)**2-4*ri*rj));ok=z[:,None]+z[None,:]<1;y=yy[:,:,a];wf=M/(16*math.pi)*phase*(abs(y)**2*(1-ri-rj)-2*(y*y).real*z[:,None]*z[None,:])*ok
  z=mS/M;phase=np.sqrt(np.maximum(0,(1-z[:,None]**2-z[None,:]**2)**2-4*z[:,None]**2*z[None,:]**2));ok=(z[:,None]+z[None,:]<1)&phys[:,None]&phys[None,:];ws=cubic[a]**2/(32*math.pi*M)*phase*ok
  rows.append(dict(index=a,mass_over_mu=M,to_neutral_fermions=float(wf[np.ix_(qf<.01,qf<.01)].sum()),to_charged_fermions=float(wf[np.ix_(qf>.1,qf>.1)].sum()),to_neutral_scalars=float(ws[np.ix_(qs<.01,qs<.01)].sum()),to_charged_scalars=float(ws[np.ix_(qs>.1,qs>.1)].sum()),charged_scalar_daughter_masses=sorted(set((round(float(mS[i]),8),round(float(mS[j]),8)) for i in range(len(qs)) for j in range(i,len(qs)) if qs[i]>.1 and qs[j]>.1 and ws[i,j]>1e-25))))
 controls={'charge_basis_CP_real':max(es,ef)<1e-9,'physical_SU3_A_scalar_octet_identified':sum(abs(q['mass_over_mu']-.021997067)<1e-7 for q in rows)==8}
 result=dict(claim_id='TK08_ORIGIN_NEUTRAL_CASCADE',checks={k:bool(v) for k,v in controls.items()},parents=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Origin tree scalar/fermion cascade widths only. Vector final states and loop-mediated radiation channels omitted. Massless charged Goldstones excluded; neutral massless collective pair retained.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));assert all(controls.values())
if __name__=='__main__':main(sys.argv[1])
