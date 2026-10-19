#!/usr/bin/env python3
"""Exact Cartesian derivation of the ten-channel static J1 vector operator."""
import argparse,json,time
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--result',required=True);args=p.parse_args();start=time.monotonic()
t=s.symbols('t',positive=True); nx,ny,nz=s.symbols('nx ny nz',real=True); ns=[nx,ny,nz];n=s.Matrix(ns);e=s.eye(3);pol=e[:,2]
k=s.symbols('k');h=s.symbols('h');kp=s.symbols('kp');hp=s.symbols('hp')
def dr(q):return q.diff(t)+q.diff(k)*kp+q.diff(h)*hp
def simp(q):
 num,den=s.fraction(s.together(q));num=s.rem(s.Poly(s.expand(num),nz),s.Poly(nz*nz+nx*nx+ny*ny-1,nz)).as_expr();return s.cancel(num/den)
def spatial(v,i):return s.Matrix([n[i]*dr(v[a])+sum((s.KroneckerDelta(i,j)-n[i]*n[j])*s.diff(v[a],ns[j])/t for j in range(3)) for a in range(3)])
A=[(1-k)/t*e[:,i].cross(n) for i in range(3)];Phi=h*n
A.append(Phi)
def cov(v,i):return spatial(v,i)+A[i].cross(v) if i<3 else Phi.cross(v)
F=[[s.zeros(3,1) for j in range(4)] for i in range(4)]
for i in range(4):
 for j in range(i+1,4):
  val=(spatial(A[j],i) if i<3 else s.zeros(3,1))-(spatial(A[i],j) if j<3 else s.zeros(3,1))+A[i].cross(A[j])
  F[i][j]=val.applyfunc(simp);F[j][i]=-F[i][j]
# Basis tensors use rows spatial i and columns adjoint a.
spatial_basis=[nz*s.eye(3), n*pol.T,pol*n.T,n*n.T*nz,s.Matrix(3,3,lambda i,a:sum(s.LeviCivita(i,a,b)*pol[b] for b in range(3))),n*(n.cross(pol)).T,n.cross(pol)*n.T]
B=[]
for a in spatial_basis:B.append(s.Matrix.vstack(a,s.zeros(1,3)))
for a in [pol,n*nz,n.cross(pol)]:B.append(s.Matrix.vstack(s.zeros(3,3),a.T))
def moment(power):
 if any(v%2 for v in power):return s.Integer(0)
 out=s.Integer(1)
 for v in power:out*=s.factorial2(v-1) if v else 1
 return out/s.factorial2(sum(power)+1)
def angular(q):
 num,den=s.fraction(s.together(q));P=s.Poly(s.expand(num),nx,ny,nz)
 return s.cancel(sum(co*moment(po) for po,co in P.terms())/den)
def dot(a,b):return sum(a[i,j]*b[i,j] for i in range(4) for j in range(3))
G=s.Matrix(10,10,lambda i,j:angular(dot(B[i],B[j])))
assert G.det()!=0
Gi=G.inv();columns=[]
for b in range(10):
 aa=B[b]/t;out=s.zeros(4,3)
 for mu in range(4):
  v=aa[mu,:].T
  lap=sum((cov(cov(v,nu),nu) for nu in range(4)),s.zeros(3,1))
  spin=sum((F[mu][nu].cross(aa[nu,:].T) for nu in range(4)),s.zeros(3,1))
  out[mu,:]=((-lap-2*spin)*t).T
 out=out.applyfunc(simp)
 coeff=Gi*s.Matrix([angular(dot(a,out)) for a in B])
 residual=out-sum((B[i]*coeff[i] for i in range(10)),s.zeros(4,3))
 assert all(simp(v)==0 for v in residual),b
 columns.append(coeff)
 print('Projected Cartesian vector column',b,flush=True)
V=s.Matrix.hstack(*columns)
assert all(s.cancel(v)==0 for v in G*V-(G*V).T)
# Actual BPS field is anti-self-dual in epsilon1234=+1 conventions.
subbps={kp:-k*h,hp:(1-k*k)/t**2}
for i,j,kk in [(0,1,2),(1,2,0),(2,0,1)]:
 assert all(s.cancel(v.subs(subbps))==0 for v in F[i][j]+F[kk][3])
print('Gram symmetry and exact BPS anti-self-duality verified',flush=True)
# Origin orbital matrix from A=Phi=0 and exact G-orthonormal eigenvectors.
A0=s.simplify(t*t*V.subs({k:1,h:0,kp:0,hp:0}))
Scols=[];ls=[]
for eigen,mult,vectors in sorted(A0.eigenvects(),key=lambda v:v[0]):
 ell=next(l for l in range(4) if l*(l+1)==eigen)
 for vec in vectors:
  for old in Scols:vec-=old*(old.T*G*vec)[0]
  vec=s.simplify(vec/s.sqrt((vec.T*G*vec)[0]));Scols.append(vec);ls.append(ell)
S=s.Matrix.hstack(*Scols);assert S.shape==(10,10)
assert s.simplify(S.T*G*S)==s.eye(10)
assert s.simplify(S.inv()*A0*S)==s.diag(*[l*(l+1) for l in ls])
# Seven tangential/A4 Dirichlet rows; normal trace in p,n nz,n cross p basis.
T=s.zeros(7,10)
for i,j in enumerate([0,2,4,6,7,8,9]):T[i,j]=1
N=s.zeros(3,10);N[0,1]=1;N[1,0]=N[1,2]=N[1,3]=1;N[2,4]=-1;N[2,5]=1
stack=T.col_join(N);assert stack.det()!=0
normal_basis=[pol,n*nz,n.cross(pol)]
for b in range(10):
 contraction=(n.T*B[b][:3,:]).T
 assert all(simp(v)==0 for v in contraction-sum((normal_basis[j]*N[j,b] for j in range(3)),s.zeros(3,1)))
refcoeff=s.factor((T*S).col_join(N*S*s.diag(*[l+2 for l in ls])).det())
print('Regular origins',ls,'reference boundary determinant constant',refcoeff,flush=True)
def strings(mat):return [[s.sstr(mat[i,j]) for j in range(mat.cols)] for i in range(mat.rows)]
result={'variables':['t','k','h','kp','hp'],'basis':['delta_ia nz','n_i p_a','p_i n_a','n_i n_a nz','epsilon_iab p_b','n_i(n cross p)_a','(n cross p)_i n_a','A4:p_a','A4:n_a nz','A4:(n cross p)_a'],'Gram':strings(G),'V_raw':strings(V),'origin_A0':strings(A0),'S_Gorthonormal':strings(S),'origin_l':ls,'Dirichlet_T':strings(T),'normal_N':strings(N),'reference_boundary_constant':s.sstr(refcoeff),'reference_boundary_x_power':sum(l+1 for l in ls)-3,'exact_checks':['all ten Cartesian Hessian projections close in ansatz','G V is symmetric','Fij=-epsilonijk Fk4 on BPS equations','G-orthonormal origin matrix has correct eigenchannels','all ten normal contractions reproduce N','wall 7D+3R matrix has full rank'],'runtime_seconds':time.monotonic()-start,'sympy_version':s.__version__}
Path(args.result).write_text(json.dumps(result,indent=2)+'\n')
print('Exact derivation completed',result['runtime_seconds'],flush=True)
