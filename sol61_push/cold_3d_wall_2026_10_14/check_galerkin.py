import sys,json,itertools
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import eigvalsh
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
root=Path('sol61_push/cold_3d_wall_2026_10_14')
geo=json.loads((root/'geometry_run_v2/calculation/results.json').read_text())
names=['B','px','py','pz','hxx','hyy','hzz','hxy','hxz','hyz'];syms={n:s.Symbol(n,real=True) for n in names};R=s.sympify(geo['normal_Ricci'],locals=syms);rf=s.lambdify([syms[n] for n in names],R,'numpy')
pairs=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
wave=np.array(list(itertools.product([-1,0,1],repeat=3)),dtype=float)/10
nodes=np.array(list(itertools.product(np.arange(5)*2*np.pi/5,repeat=3)))
base=np.exp(1j*wave@(nodes*10).T);P=len(wave);Q=len(nodes);nv=16*P
zeros=lambda:np.zeros((nv,Q),dtype=complex)
def calc(V):
 cos=np.cos(nodes);sin=np.sin(nodes);one=1+cos;ell=10.
 prof=np.prod(one,axis=1)/8;b=V*(1-prof)
 bp=np.array([V*sin[:,i]*np.prod(np.delete(one,i,axis=1),axis=1)/(8*ell) for i in range(3)])
 bh=np.zeros((3,3,Q))
 for i in range(3):
  bh[i,i]=V*cos[:,i]*np.prod(np.delete(one,i,axis=1),axis=1)/(8*ell**2)
  for j in range(i):
   k=3-i-j;bh[i,j]=bh[j,i]=-V*sin[:,i]*sin[:,j]*one[:,k]/(8*ell**2)
 H=np.stack([np.array(rf(b[n],*bp[:,n],bh[0,0,n],bh[1,1,n],bh[2,2,n],bh[0,1,n],bh[0,2,n],bh[1,2,n]),dtype=float) for n in range(Q)],axis=-1)
 S=[[zeros() for j in range(3)] for i in range(3)];Sd=[[zeros() for j in range(3)] for i in range(3)]
 def block(a):
  rr=zeros();rr[a*P:(a+1)*P]=base;return rr
 for a,(i,j) in enumerate(pairs):S[i][j]=S[j][i]=block(a);Sd[i][j]=Sd[j][i]=block(10+a)
 alpha=block(6);vv=[block(7+i) for i in range(3)]
 # Derivativesactonbasiscoefficients,multiplicationbyvariablebcomesafter.
 def der(a,i):return a*(1j*np.tile(wave[:,i],16))[:,None]
 gradS=[[[der(S[i][j],k) for j in range(3)] for i in range(3)] for k in range(3)]
 gradv=[[der(vv[j],i) for j in range(3)] for i in range(3)]
 tr=sum(S[i][i] for i in range(3));gradtr=[der(tr,i) for i in range(3)];gradalpha=[der(alpha,i) for i in range(3)]
 E0=np.zeros((3,3,Q))
 for i in range(3):E0[i,2]-=bp[i];E0[2,i]-=bp[i]
 T0=sum(E0[i,i] for i in range(3));E02=np.einsum('ikn,kjn->ijn',E0,E0)
 E1=[[Sd[i][j]-b*gradS[2][i][j]-gradv[i][j]-gradv[j][i]-S[2][j]*bp[i]-S[i][2]*bp[j] for j in range(3)] for i in range(3)]
 def gr(a,c,w=1.):
  if not np.any(w):return 0
  return (a.conj()*w)@c.T/Q
 def w2(w):return gr(alpha,alpha,w)-.5*gr(alpha,tr,w)+.125*gr(tr,tr,w)-.25*sum(gr(S[i][j],S[j][i],w) for i in range(3) for j in range(3))
 trE1=sum(E1[i][i] for i in range(3));trSE0=sum(S[i][j]*E0[j,i] for i in range(3) for j in range(3));T1=trE1-trSE0
 F2=sum(gr(E1[i][j],E1[j][i]) for i in range(3) for j in range(3))
 F2-=2*sum(gr(vv[k],sum(E0[i,j]*gradS[k][j][i] for i in range(3) for j in range(3))) for k in range(3))
 F2-=4*sum(gr(S[k][j],gradv[i][k],E0[i,j]) for i in range(3) for j in range(3) for k in range(3))
 F2-=4*sum(gr(S[i][j],E1[k][i],E0[j,k]) for i in range(3) for j in range(3) for k in range(3))
 F2+=2*sum(gr(S[i][j],S[j][k],E02[k,i]) for i in range(3) for j in range(3) for k in range(3))
 F2+=sum(gr(S[i][j],S[k][l],E0[j,k]*E0[l,i]) for i in range(3) for j in range(3) for k in range(3) for l in range(3))
 F2-=gr(T1,T1)
 # -2T0*T2 includes all3D E2(trace)andnonzeroThetaStar terms.
 F2+=2*sum(gr(vv[k],gradtr[k],T0) for k in range(3))
 F2+=4*sum(gr(S[k][i],gradv[i][k],T0) for i in range(3) for k in range(3))
 F2+=2*sum(gr(S[i][j],E1[j][i],T0) for i in range(3) for j in range(3))
 F2-=2*sum(gr(S[i][j],S[j][k],T0*E0[k,i]) for i in range(3) for j in range(3) for k in range(3))
 F1=2*sum(E0[i,j]*E1[j][i]-E02[i,j]*S[j][i] for i in range(3) for j in range(3))-2*T0*T1
 F0=sum(E0[i,j]**2 for i in range(3) for j in range(3))-T0**2
 M=(F2+gr(.5*tr-alpha,F1)+w2(F0))/8
 divS=[sum(gradS[i][i][j] for i in range(3)) for j in range(3)]
 M+=(-.25*sum(gr(gradS[k][i][j],gradS[k][i][j]) for k in range(3) for i in range(3) for j in range(3))+.25*sum(gr(v,v) for v in gradtr)+.5*sum(gr(v,v) for v in divS)-.5*sum(gr(divS[j],gradtr[j]) for j in range(3))+sum(gr(gradalpha[i],gradtr[i]-divS[i]) for i in range(3)))/2
 Hs=H[1:,1:];Hn=H[0,1:];Ht=H[0,0]
 B1=-2*sum(vv[i]*Hn[i] for i in range(3));M+=.5*sum(gr(vv[i],vv[j],Hs[i,j]) for i in range(3) for j in range(3))+.5*gr(.5*tr-alpha,B1)+.5*w2(Ht)
 for i in range(3):
  for j in range(3):
   M-=.5*sum(gr(S[i][k],S[k][j],Hs[j,i]) for k in range(3))
   M+=.5*gr(alpha+.5*tr,S[i][j],Hs[j,i])
   if i==j:M-=.5*(.125*gr(tr,tr,Hs[j,i])-.25*sum(gr(S[k][l],S[l][k],Hs[j,i]) for k in range(3) for l in range(3))+.5*gr(alpha,tr,Hs[j,i]))
 M+=.5*gr(alpha,alpha,1-Ht)+.5*sum(gr(vv[i],vv[j],4*(i==j)-Hs[i,j]) for i in range(3) for j in range(3))-gr(alpha,sum(vv[i]*Hn[i] for i in range(3)))
 M-=.5*sum(gr(S[i][j],S[i][j]) for i in range(3) for j in range(3))
 for i in range(3):M+=-sum(gr(vv[j],S[i][j],Hn[i]) for j in range(3))+.5*gr(vv[i],tr,Hn[i])
 dtheta=T1/2-alpha*T0/2;M+=.5*gr(dtheta,dtheta)+.5*sum(gr(a,a) for a in gradalpha)
 M+=sum(gr(Sd[i][j]-b*gradS[2][i][j],Sd[i][j]-b*gradS[2][i][j]) for i in range(3) for j in range(3))/2-sum(gr(gradS[k][i][j],gradS[k][i][j]) for k in range(3) for i in range(3) for j in range(3))/4
 Hfull=M+M.conj().T
 idx=np.r_[np.arange(6*P),np.arange(10*P,16*P)];nn=np.arange(6*P,10*P)
 reduced=Hfull[np.ix_(idx,idx)]-Hfull[np.ix_(idx,nn)]@np.linalg.solve(Hfull[np.ix_(nn,nn)],Hfull[np.ix_(nn,idx)])
 kin=reduced[6*P:,6*P:];pot=-reduced[:6*P,:6*P]
 # Assemblejointkinetic/nondynamic square independentlyofF0/F1/F2 expansion.
 Y=[[Sd[i][j]-gradv[i][j]-gradv[j][i]-alpha*E0[i,j] for j in range(3)] for i in range(3)]
 Jmat=sum(gr(Y[i][j],Y[i][j]) for i in range(3) for j in range(3))/8+sum(gr(Sd[i][j],Sd[i][j]) for i in range(3) for j in range(3))/2+.5*gr(alpha,alpha)+2*sum(gr(v,v) for v in vv)+.5*sum(gr(a,a) for a in gradalpha)
 jn=np.arange(6*P,16*P);err=float(np.max(abs(Hfull[np.ix_(jn,jn)]-(Jmat+Jmat.conj().T)[np.ix_(jn,jn)])))
 assert err<1e-10,('jointidentity',V,err);checks.append('independentcompletedjointsquare '+str(V))
 gram=sum(gr(S[i][j],S[i][j]) for i in range(3) for j in range(3))[:6*P,:6*P];dg=sum(gr(gradS[k][i][j],gradS[k][i][j]) for k in range(3) for i in range(3) for j in range(3))[:6*P,:6*P]
 # Conditionsuseactualsupnormsampleupperbounds analyticalfortrigprofile.
 Bg=V;gg=3*V*V/(4*ell**2);jj=np.sqrt(9/8)*V/ell**2;eta=10*((1+V)*jj+gg);a=1/8-2.5*Bg**2;c=.5-13*gg-1.5*eta
 assert a>0 and c>0;checks.append('analytictrigcondition '+str(V))
 margins={'kinetic_minus_proofbound':float(eigvalsh(kin-gram)[0]),'restoring_minus_proofbound':float(eigvalsh(pot-2*(a*dg+c*gram))[0]),'staticnegative_minus_proofbound':float(eigvalsh(-Hfull[:6*P,:6*P]-2*(a*dg+c*gram))[0])}
 assert min(margins.values())>-1e-9,margins;checks.append('threeproofbounds '+str(V))
 ferr=None
 if V==0:
  actual=eigvalsh(pot,kin);pred=[]
  for kk in wave:
   q=kk.dot(kk);pred +=[(3*q+2+2/(q+1))/5,(q+2)*(q+4)/(2*(q+5)),(q+2)*(q+8)/(2*(q+10)),(q+2)*(q+8)/(2*(q+10)),3*q/5+s.Rational(4,5),3*q/5+s.Rational(4,5)]
  pred=np.sort(np.array(pred,dtype=float));ferr=float(np.max(abs(actual-pred)));assert ferr<1e-9,ferr;checks.append('independentflat6modebenchmark')
 return {'V':V,'basis_modes':P,'quadrature_points':Q,'ell':ell,'maxabsThetaStar':float(np.max(abs(T0/2))),'minK':float(eigvalsh(kin)[0]),'minG':float(eigvalsh(pot)[0]),'joint_identity_error':err,'bounds':margins,'flat_spectrum_error':ferr,'static_gradient_margin':a,'static_mass_margin':c}
rows=[calc(V) for V in (0.,.05,.1)]
result={'claim':'C3W-002','checks_passed':len(checks),'rows':rows,'scope':'Complete finite3DperiodicGalerkincontrol,notR3proof. Targettrigcoefficientdegree<=2,5pointperaxisquadratureexacttodegree4; binary64 tolerance remains.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
