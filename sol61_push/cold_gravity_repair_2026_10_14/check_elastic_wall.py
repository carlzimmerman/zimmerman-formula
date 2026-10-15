import json,sys
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import eigvalsh
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
x=s.symbols('x',real=True);bb=s.Function('b')(x);coords=(s.symbols('t'),x,s.symbols('y'),s.symbols('z'))
g=s.Matrix([[-1+bb**2,0,0,bb],[0,1,0,0],[0,0,1,0],[bb,0,0,1]]);gi=g.inv()
Ga=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[k])+s.diff(g[d,k],coords[c])-s.diff(g[k,c],coords[d])) for d in range(4))/2) for c in range(4)] for k in range(4)] for a in range(4)]
Ric=s.Matrix(4,4,lambda a,c:s.simplify(sum(s.diff(Ga[d][a][c],coords[d])-s.diff(Ga[d][a][d],coords[c])+sum(Ga[d][d][e]*Ga[e][a][c]-Ga[d][c][e]*Ga[e][a][d] for e in range(4)) for d in range(4))))
b0,b1,b2=s.symbols('b0 b1 b2');Ric=Ric.subs({s.diff(bb,x,2):b2,s.diff(bb,x):b1,bb:b0})
ricfun=s.lambdify((b0,b1,b2),Ric,'numpy')
# TraceK*=0; independently verify normal acceleration is zero on target.
U=s.Matrix([1,0,0,-bb]);Uc=s.Matrix([-1,0,0,0])
for m in range(4):
 acc=s.simplify(sum(U[n]*(s.diff(Uc[m],coords[n])-sum(Ga[k][n][m]*Uc[k] for k in range(4))) for n in range(4)))
 assert acc==0;checks.append('target acceleration zero '+str(m))
pairs=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
def calc(N,V,ky,kz):
 ell=2.;xx=np.arange(N)*2*np.pi*ell/N;b=V*np.sin(xx/ell);bp=V/ell*np.cos(xx/ell);bpp=-b/ell**2
 wave=np.fft.fftfreq(N,d=ell/N)
 Der=np.fft.ifft(1j*wave[:,None]*np.fft.fft(np.eye(N),axis=0),axis=0).real
 nv=16*N;eye=np.eye(nv,dtype=complex);zero=np.zeros((nv,N),dtype=complex);S=[[zero.copy() for j in range(3)] for i in range(3)];Sd=[[zero.copy() for j in range(3)] for i in range(3)]
 for a,(i,j) in enumerate(pairs):S[i][j]=S[j][i]=eye[:,a*N:(a+1)*N];Sd[i][j]=Sd[j][i]=eye[:,(10+a)*N:(11+a)*N]
 alpha=eye[:,6*N:7*N];vv=[eye[:,(7+i)*N:(8+i)*N] for i in range(3)]
 ds=[[S[i][j]@Der.T for j in range(3)] for i in range(3)];dv=[v@Der.T for v in vv];da=alpha@Der.T
 tr=sum(S[i][i] for i in range(3));dtr=sum(ds[i][i] for i in range(3));dott=sum(Sd[i][i] for i in range(3))
 E0=np.zeros((3,3,N));E0[0,2]=E0[2,0]=-bp;E02=np.einsum('ikn,kjn->ijn',E0,E0)
 der=lambda a,i: a@Der.T if i==0 else 1j*(ky if i==1 else kz)*a
 gradS=[[[der(S[i][j],k) for j in range(3)] for i in range(3)] for k in range(3)]
 gradv=[[der(vv[j],i) for j in range(3)] for i in range(3)]
 E1=[[Sd[i][j]-1j*kz*b*S[i][j]-gradv[i][j]-gradv[j][i]-(S[2][j]*bp if i==0 else 0)-(S[i][2]*bp if j==0 else 0) for j in range(3)] for i in range(3)]
 def gr(a,c,w=1.):return (a.conj()*w)@c.T/N
 def w2(w):return gr(alpha,alpha,w)-.5*gr(alpha,tr,w)+.125*gr(tr,tr,w)-.25*sum(gr(S[i][j],S[j][i],w) for i in range(3) for j in range(3))
 trE1=sum(E1[i][i] for i in range(3));trSE0=sum(S[i][j]*E0[j,i] for i in range(3) for j in range(3))
 F2=sum(gr(E1[i][j],E1[j][i]) for i in range(3) for j in range(3))
 F2-=2*sum(gr(vv[k],sum(E0[i,j]*gradS[k][j][i] for i in range(3) for j in range(3))) for k in range(3))
 F2-=4*sum(gr(S[k][j],gradv[i][k],E0[i,j]) for i in range(3) for j in range(3) for k in range(3))
 F2-=4*sum(gr(S[i][j],E1[k][i],E0[j,k]) for i in range(3) for j in range(3) for k in range(3))
 F2+=2*sum(gr(S[i][j],S[j][k],E02[k,i]) for i in range(3) for j in range(3) for k in range(3))
 F2+=sum(gr(S[i][j],S[k][l],E0[j,k]*E0[l,i]) for i in range(3) for j in range(3) for k in range(3) for l in range(3))
 F2-=gr(trE1-trSE0,trE1-trSE0)
 F1=2*sum(E0[i,j]*E1[j][i]-E02[i,j]*S[j][i] for i in range(3) for j in range(3))
 M=(F2+gr(.5*tr-alpha,F1)+w2(2*bp**2))/8
 divS=[sum(gradS[i][i][j] for i in range(3)) for j in range(3)]
 gradtr=[der(tr,i) for i in range(3)];gradalpha=[der(alpha,i) for i in range(3)]
 M+=(-.25*sum(gr(gradS[k][i][j],gradS[k][i][j]) for k in range(3) for i in range(3) for j in range(3))+.25*sum(gr(v,v) for v in gradtr)+.5*sum(gr(v,v) for v in divS)-.5*sum(gr(divS[j],gradtr[j]) for j in range(3))+sum(gr(gradalpha[i],gradtr[i]-divS[i]) for i in range(3)))/2
 H=np.stack([np.array(ricfun(float(bi),float(bpi),float(bppi)),dtype=float) for bi,bpi,bppi in zip(b,bp,bpp)],axis=-1)
 Hs=H[1:,1:];Hn=np.stack([H[0,i+1]-b*H[3,i+1] for i in range(3)]);Ht=H[0,0]-2*b*H[0,3]+b*b*H[3,3]
 B1=-2*sum(vv[i]*Hn[i] for i in range(3));M+=.5*sum(gr(vv[i],vv[j],Hs[i,j]) for i in range(3) for j in range(3))+.5*gr(.5*tr-alpha,B1)+.5*w2(Ht)
 d2=.125*gr(tr,tr)-.25*sum(gr(S[i][j],S[j][i]) for i in range(3) for j in range(3))
 for i in range(3):
  for j in range(3):
   M-=.5*sum(gr(S[i][k],S[k][j],Hs[j,i]) for k in range(3))
   M+=.5*gr(alpha+.5*tr,S[i][j],Hs[j,i])
   if i==j:M-=.5*(.125*gr(tr,tr,Hs[j,i])-.25*sum(gr(S[k][l],S[l][k],Hs[j,i]) for k in range(3) for l in range(3))+.5*gr(alpha,tr,Hs[j,i]))
 # Exact quadratic framed strains on background: S00=2alpha,S0i=vi,Sij=-sij.
 M+=.5*gr(alpha,alpha,1-Ht)+.5*sum(gr(vv[i],vv[j],4*(i==j)-Hs[i,j]) for i in range(3) for j in range(3))-gr(alpha,sum(vv[i]*Hn[i] for i in range(3)))
 M-=.5*sum(gr(S[i][j],S[i][j]) for i in range(3) for j in range(3))
 for i in range(3):M+=-sum(gr(vv[j],S[i][j],Hn[i]) for j in range(3))+.5*gr(vv[i],tr,Hn[i])
 dk=.5*(dott-1j*kz*b*tr)-sum(gradv[i][i] for i in range(3));M+=.5*gr(dk,dk)+.5*sum(gr(a,a) for a in gradalpha)
 M+=sum(gr(Sd[i][j]-1j*kz*b*S[i][j],Sd[i][j]-1j*kz*b*S[i][j]) for i in range(3) for j in range(3))/8-sum(gr(gradS[k][i][j],gradS[k][i][j]) for k in range(3) for i in range(3) for j in range(3))/16
 Hess=M+M.conj().T
 idx=np.r_[np.arange(6*N),np.arange(10*N,16*N)];nn=np.arange(6*N,10*N)
 reduced=Hess[np.ix_(idx,idx)]-Hess[np.ix_(idx,nn)]@np.linalg.solve(Hess[np.ix_(nn,nn)],Hess[np.ix_(nn,idx)])
 kin=reduced[6*N:,6*N:];pot=-reduced[:6*N,:6*N];mix=reduced[6*N:,:6*N]
 km=eigvalsh(kin);pm=eigvalsh(pot);errs=None
 if V==0:
  actual=eigvalsh(pot,kin);pred=[]
  for k in wave:
   q=k*k+ky*ky+kz*kz;pred +=[3*q/4+1+1/(q+1),q/2+2,q/2+32/(q+16),q/2+32/(q+16),3*q/4+2,3*q/4+2]
  errs=float(np.max(abs(actual-np.sort(pred))/np.maximum(1,abs(actual))))
  assert errs<1e-8,('flat spectrum',N,errs)
  checks.append('independent full ADM flat spectrum N'+str(N))
 checks.append('Schur Hamiltonian recorded '+str((N,V,ky,kz)))
 return {'N':N,'V':V,'ky':ky,'kz':kz,'ell':ell,'min_kinetic_eigenvalue':float(km[0]),'min_potential_eigenvalue':float(pm[0]),'positive_reduced_energy':bool(km[0]>1e-9 and pm[0]>1e-9),'max_abs_mixed_entry':float(np.max(abs(mix))),'flat_relative_spectrum_error':errs,'lapse_shift_min_eigenvalue':float(eigvalsh(Hess[np.ix_(nn,nn)])[0])}
rows=[]
for N in (9,17,25):
 for ky,kz in ((0.,0.),(0.,1.),(1.,0.),(1.,1.),(.5,1.),(1.,.5),(0.,10.),(0.,20.),(0.,50.),(0.,100.)):
  for V in (0.,.1,.3,.6):rows.append(calc(N,V,ky,kz))
result={'claim':'CGR-010','checks_passed':len(checks),'rows':rows,'scope':'Finite periodic planar background, complex transverse Fourier modes at specified ky,kz; positive matrices not continuum3D spherical wall proof. Raw nodal coefficient products alias; flat spectrum is independent benchmark.','Ricci':str(Ric)}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
