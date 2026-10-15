import json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh,null_space
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def step(x):
 y=np.zeros_like(x);y[x>=1]=1;m=(x>0)&(x<1);z=x[m];u=np.exp(-1/z);v=np.exp(-1/(1-z));y[m]=u/(u+v);return y
def run(N,q,kind="staged",strength=4,period=32,aux_rcond=1e-10,clockmass=1,shear=0):
 z=np.linspace(-period/2,period/2,N,endpoint=False);freq=2*np.pi*np.fft.fftfreq(N,d=period/N)
 D=np.fft.ifft(1j*freq[:,None]*np.fft.fft(np.eye(N),axis=0),axis=0).real
 h=1-step((abs(z)-3)/2);theta=1-step((abs(z)-7)/4)
 if kind=="massless":h=np.zeros(N)
 if kind=="uniform":h=np.ones(N);theta=np.ones(N)
 kap=strength*theta
 nv=16*N
 def block(i):
  a=np.zeros((nv,N),complex);a[i*N:(i+1)*N]=np.eye(N);return a
 def der(a,i):return 1j*q*a if i==0 else (np.zeros_like(a) if i==1 else a@D.T)
 def gr(a,b,w=1):return (a.conj()*w)@b.T/N
 pairs=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
 Q=[[None]*3 for _ in range(3)];U=[[None]*3 for _ in range(3)]
 for a,(i,j) in enumerate(pairs):Q[i][j]=Q[j][i]=block(a);U[i][j]=U[j][i]=block(10+a)
 alpha=block(6);v=[block(7+i) for i in range(3)]
 E=[[U[i][j]-der(v[j],i)-der(v[i],j) for j in range(3)] for i in range(3)]
 tr=sum(Q[i][i] for i in range(3));trE=sum(E[i][i] for i in range(3));div=[sum(der(Q[i][j],i) for i in range(3)) for j in range(3)]
 M=(sum(gr(E[i][j],E[i][j]) for i in range(3) for j in range(3))-gr(trE,trE))/8+gr(trE,trE,theta)/8
 M+=sum(gr(U[i][j],U[i][j],kap) for i in range(3) for j in range(3))/8
 M-=sum(gr(der(Q[i][j],k),der(Q[i][j],k),kap) for i in range(3) for j in range(3) for k in range(3))/16
 M+=(-sum(gr(der(Q[i][j],k),der(Q[i][j],k)) for i in range(3) for j in range(3) for k in range(3))+sum(gr(der(tr,k),der(tr,k)) for k in range(3))+2*sum(gr(x,x) for x in div)-2*sum(gr(div[k],der(tr,k)) for k in range(3)))/8
 M+=sum(gr(der(alpha,k),der(tr,k)-div[k]) for k in range(3))/2
 M+=gr(alpha,alpha,h*clockmass)/2+2*sum(gr(x,x,h) for x in v)-sum(gr(Q[i][j],Q[i][j],h) for i in range(3) for j in range(3))/2
 M+=shear*sum(gr(der(v[j],i),der(v[j],i),theta) for i in range(3) for j in range(3))/2
 H=M+M.conj().T
 qi=np.arange(6*N);ai=np.arange(6*N,7*N);vi=np.arange(7*N,10*N);ui=np.arange(10*N,16*N)
 active=np.flatnonzero(h*clockmass>1e-12);zero=np.flatnonzero(h*clockmass<=1e-12)
 C=H[np.ix_(ai[zero],qi)];Z=(null_space(C,rcond=1e-10) if C.shape[0] else np.eye(6*N))
 Ar=H[np.ix_(ai[active],ai[active])];V=H[np.ix_(vi,vi)]
 vv,ve=np.linalg.eigh(V);vtol=max(1e-14,np.max(abs(vv))*aux_rcond);pos=vv>vtol;vn=ve[:,~pos]
 assert vv.min()>-vtol,('negative shift auxiliary',N,q,vv.min())
 vp=(ve[:,pos]/vv[pos])@ve[:,pos].conj().T
 nullcouple=float(np.max(abs(vn.conj().T@H[np.ix_(vi,ui)]@Z))) if vn.shape[1] else 0.
 # Shift null directions are genuine velocity multipliers, not invertible auxiliaries.
 # For nonzero-frequency modes their integrated constraint also acts on Q.
 # Work in the sector with zero integration constants; record the extra rank.
 olddim=Z.shape[1]
 shiftC=vn.conj().T@H[np.ix_(vi,ui)]
 if vn.shape[1]:
  C=np.vstack([C,shiftC]);Z=(null_space(C,rcond=1e-10) if C.shape[0] else np.eye(6*N))
 nullafter=float(np.max(abs(shiftC@Z))) if vn.shape[1] else 0.
 assert nullafter<1e-8,('shift multiplier residual',N,q,nullafter)
 K=H[np.ix_(ui,ui)]-H[np.ix_(ui,vi)]@vp@H[np.ix_(vi,ui)]
 G=-H[np.ix_(qi,qi)]+H[np.ix_(qi,ai[active])]@np.linalg.solve(Ar,H[np.ix_(ai[active],qi)])
 kr=Z.conj().T@K@Z;gg=Z.conj().T@G@Z
 ek=eigvalsh(kr);eg=eigvalsh(gg)
 benchmark=None
 if kind=="uniform":
  actual=eigvalsh(gg,kr);pred=[]
  for zz in freq:
   q2=q*q+zz*zz
   pred += [(q2+4+2*q2*q2)/5,(1+q2/2)*(q2+4)/(q2+5)]+[(1+q2/2)*(q2+8)/(q2+10)]*2+[(3*q2+4)/5]*2
  benchmark=float(np.max(abs(actual-np.sort(pred))))
  assert benchmark<1e-8,('uniform exact spectrum',benchmark)
  checks.append('uniform all six exact spectrum')
 if kind=="massless":
  fields=np.array([[U[i][j][ui] for j in range(3)] for i in range(3)])
  f=np.fft.fft(fields,axis=-1);tt=np.zeros_like(f)
  for j,zz in enumerate(freq):
   kk=np.array([q,0.,zz]);P=np.eye(3)-np.outer(kk,kk)/kk.dot(kk)
   ff=f[:,:,:,j];trp=np.einsum('ij,ijb->b',P,ff)
   tt[:,:,:,j]=np.einsum('ia,jc,acb->ijb',P,P,ff)-P[:,:,None]*trp[None,None,:]/2
  tt=np.fft.ifft(tt,axis=-1)
  expected=sum(gr(tt[i,j],tt[i,j])+gr(fields[i,j],fields[i,j],kap) for i in range(3) for j in range(3))/4
  benchmark=float(np.max(abs(Z.conj().T@(K-expected)@Z)))
  assert benchmark<1e-8,('massless independent kinetic identity',benchmark)
  checks.append('massless independent TT kinetic identity')
 constraint_kinetic_margin=None;constraint_static_error=None
 if clockmass==0:
  fields=np.array([[U[i][j][ui] for j in range(3)] for i in range(3)])
  f=np.fft.fft(fields,axis=-1);tt=np.zeros_like(f)
  for j,zz in enumerate(freq):
   kk=np.array([q,0.,zz]);P=np.eye(3)-np.outer(kk,kk)/kk.dot(kk)
   ff=f[:,:,:,j];trp=np.einsum('ij,ijb->b',P,ff)
   tt[:,:,:,j]=np.einsum('ia,jc,acb->ijb',P,P,ff)-P[:,:,None]*trp[None,None,:]/2
  tt=np.fft.ifft(tt,axis=-1)
  bound=sum(gr(tt[i,j],tt[i,j])+gr(fields[i,j],fields[i,j],kap) for i in range(3) for j in range(3))/4
  constraint_kinetic_margin=float(eigvalsh(Z.conj().T@(K-bound)@Z)[0])
  assert constraint_kinetic_margin>-1e-8,('constraint kinetic proof bound',constraint_kinetic_margin)
  expectedG=sum(gr(der(tt[i,j],d),der(tt[i,j],d))+gr(der(fields[i,j],d),der(fields[i,j],d),kap/2) for i in range(3) for j in range(3) for d in range(3))/4
  expectedG+=sum(gr(fields[i,j],fields[i,j],h) for i in range(3) for j in range(3))
  constraint_static_error=float(np.max(abs(Z.conj().T@(G-expectedG)@Z)))
  assert constraint_static_error<1e-8,('constraint exact static proof',constraint_static_error)
  checks.extend(['independent constraint kinetic lower bound '+str((N,q)),'independent constraint static identity '+str((N,q))])
 if clockmass==1 and shear==0:
  assert ek[0]<-.01,('old ghost control failed',ek[0]);checks.append('old negative kinetic control reproduced')
 # Positive/negative decisions are finite variational evidence, not continuum proof.
 checks.extend(['shift positive semidefinite '+str((N,q)),'shift null compatibility '+str((N,q))])
 row={'constraint_kinetic_margin':constraint_kinetic_margin,'constraint_static_error':constraint_static_error,'clockmass':clockmass,'shear':shear,'period':period,'aux_rcond':aux_rcond,'benchmark_error':benchmark,'kind':kind,'kappa_strength':strength,'N':N,'transverse_q':q,'active_lapse_nodes':len(active),'lapse_constraints_rank':6*N-Z.shape[1],'admissible_dimension':Z.shape[1],'min_kinetic':float(ek[0]),'min_restoring':float(eg[0]),'min_shift':float(vv[0]),'shift_nullity':int((~pos).sum()),'nullcoupling_before_extra_constraints':nullcouple,'nullcoupling_after_extra_constraints':nullafter,'extra_shift_constraint_rank':olddim-Z.shape[1],'smallest_shift_eigenvalues':[float(z) for z in vv[:8]],'negative_kinetic_count':int((ek < -1e-8).sum()),'negative_restoring_count':int((eg < -1e-8).sum()),'constraint_residual':float(np.max(abs(C@Z))) if C.shape[0] else 0.}
 return row
rows=[run(N,q,clockmass=cm,shear=sh) for N,q,cm,sh in [(31,.5,1,0),(31,.1,0,0),(31,.5,0,0),(31,3.,0,0),(31,17.,0,0),(61,.5,0,0),(31,.5,1,1),(31,3.,1,1),(61,.5,1,1)]]
result={'claim_id':'CHB-002','rows':rows,'checks_passed':len(checks),'constraint_sector':'All lapse constraints and all shift-null velocity constraints, integrated with zero constants for Q; nonzero-frequency mode audit. Not a proof for arbitrary nonzero integration charges.','method':'Periodic Fourier variational differentiation, nodal coefficient quadrature; full lapse multiplier nullspace and shift Schur reduction. A=0, compact shift/spatial h, staged theta/kappa. Clock-mass and shear-gradient strengths explicitly varied per row. Finite binary64 evidence only; coefficient quadrature has aliasing and periodic-image errors.','non_claim':'No continuum or spherical-wall certification; no measured material or powered engine.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
