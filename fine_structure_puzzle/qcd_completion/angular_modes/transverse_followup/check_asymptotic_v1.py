#!/usr/bin/env python3
"""Exact far-field/domain algebra; does not assume connection ranks are proved."""
import argparse,json,time
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--operator',required=True);p.add_argument('--intertwiners',required=True);p.add_argument('--result',required=True);args=p.parse_args();start=time.monotonic()
t=s.symbols('t',positive=True);k,h,kp,hp=s.symbols('k h kp hp');z=s.symbols('z',positive=True);q=s.symbols('q');D=json.loads(Path(args.operator).read_text());I=json.loads(Path(args.intertwiners).read_text())
G=s.Matrix(D['Gram']);S=s.Matrix(D['S_Gorthonormal']);Si=S.T*G;V=s.Matrix(D['V_raw']).applyfunc(s.cancel);N=s.Matrix(D['normal_N']);T=s.Matrix(D['Dirichlet_T'])
Z=s.zeros(10,3)
for a,b in enumerate([1,3,5]):Z[b,a]=1
PN=Z*N;PD=s.eye(10)-PN
assert PN*PN==PN and G*PN==(G*PN).T
far=V.subs({k:0,h:1-1/t,kp:0,hp:1/t**2}).applyfunc(s.expand);M0=far.applyfunc(lambda a:a.coeff(t,0));M1=far.applyfunc(lambda a:a.coeff(t,-1));M2=far.applyfunc(lambda a:a.coeff(t,-2))
assert M1==-2*M0 and M0*M2==M2*M0 and M0*PN==PN*M0
# Exact translation reduced field, verified against independently Cartesian-derived H.
K=2*t*z/(z*z-1);H=(z*z+1)/(z*z-1)-1/t
sub={k:K,h:H,kp:-K*H,hp:(1-K*K)/t**2}
def dt(a):return a.diff(t)+z*a.diff(z)
def dm(a):return a.applyfunc(dt)
vr=V.subs(sub);tr=s.zeros(10,1);tr[4]=-K*H;tr[6]=-t*(1-K*K)/t**2+K*H;tr[7]=K*H;tr[8]=t*(1-K*K)/t**2-K*H
assert all(s.cancel(a)==0 for a in vr*tr-dm(dm(tr)))
A=s.Matrix(I['intertwiner_A_raw'])[:,:3];B=s.Matrix(I['intertwiner_B_raw'])[:,:3].subs(sub)
assert all(s.cancel(a)==0 for a in -A.T*G*dm(tr)+B.T*G*tr)
assert s.simplify(N*tr)==s.Matrix([0,0,K*H])
print('Exact translation zero equation, background gauge and finite wall traces checked',flush=True)
# Select physical far-field eigenvectors without using numerical eigenvectors.
eye=s.eye(10);v0=eye[:,2];v6=(3*eye[:,3]-eye[:,2])/s.sqrt(2);vg=(eye[:,6]+2*eye[:,8])/s.sqrt(2);vd=-eye[:,6]+eye[:,8]
assert all(s.simplify((a.T*G*b)[0])==s.KroneckerDelta(i,j) for i,a in enumerate([v0,v6,vg,vd]) for j,b in enumerate([v0,v6,vg,vd]))
for vec,C in [(v0,0),(v6,6),(vg,2),(vd,2)]:assert M0*vec==s.zeros(10,1) and s.simplify(M2*vec-C*vec)==s.zeros(10,1)
blocks=[]
for inds,neutrals in [([0,1,2,3,9],[(v0,1),(v6,3)]),([4,5,6,7,8],[(vg,2),(vd,-1)])]:
 MM=M0.extract(inds,inds);CC=M2.extract(inds,inds);GG=G.extract(inds,inds)
 one=[vec for val,mul,vs in MM.eigenvects() if val==1 for vec in vs];Q=s.Matrix.hstack(*one);Csmall=(Q.T*GG*Q).inv()*Q.T*GG*CC*Q
 charged=[];cent=[]
 for val,mul,vs in sorted(Csmall.eigenvects(),key=lambda a:a[0]):
  for vv in vs:
   vv=Q*vv;vv=vv/s.sqrt((vv.T*GG*vv)[0]);full=s.zeros(10,1)
   for i,jj in enumerate(inds):full[jj]=vv[i]
   charged.append(full);cent.append(val)
 assert cent==[0,2,6]
 cols=[]
 for vv,C in zip(charged,cent):
  a1=(2-C)/2;a2=(6-C)*a1/4;ff=1+a1*q+a2*q*q;ffp=-a1*q*q-2*a2*q**3
  col=vv*ff+PN*vv*ffp;cols.append(col.extract(inds,[0]))
 for vv,pow0 in neutrals:
  col=PD*vv+(pow0+1)*q*PN*vv;cols.append(col.extract(inds,[0]))
 boundary=s.Matrix.hstack(*cols);det=s.factor(boundary.det());poly=s.Poly(det,q);power=min(v[0][0] for v in poly.terms());lead=poly.coeff_monomial(q**power);coef1=s.cancel(poly.coeff_monomial(q**(power+1))/lead)
 assert power==(1 if inds[0]==0 else 0)
 assert coef1==-1 # each charged C0,2,6 triple contributes -1/t
 blocks.append({'raw_indices':inds,'charged_centrifugal_eigenvalues':list(map(int,cent)),'neutral_powers':[p for v,p in neutrals],'normalized_boundary_polynomial':s.sstr(s.cancel(det/(lead*q**power))),'boundary_leading_q_power':power,'relative_inverse_radius_coefficient':s.sstr(coef1)})
 print('Asymptotic boundary block',inds,'power',power,'relative1/x',coef1,flush=True)
result={'exact_checks':['PN is Gram-orthogonal rank3 projection','far-field charge projector commutes with normal wall projection','far-field Coulomb coefficient is -2 times charged mass projector','far-field mass and centrifugal matrices commute','translation solves actual vector zero equation and G=0','translation normal wall trace is purely Kh and hence exponentially small','far-field neutral vectors are Gram-orthonormal eigenvectors','each 5block asymptotic mixed boundary determinant has nonzero leading coefficient and relative1/x=-1'],'blocks':blocks,'conditional_conclusion':{'if':['only J1 L2 zero direction per magnetic quantum number is the translation','neutral regular connection has no additional non-L2 zero-energy resonance after the exact neutral gauge-gradient condition','the exponentially decaying offdiagonal coefficients permit the stated charged/neutral outer basis matching with error smaller than1/x'],'then_log_D_vector':'6x-22log x+C-2/x+O(x^-2)','then_log_Z_J1':'-3x+15log x+Cprime+3/x+O(x^-2)','status':'conditional; finite matrix algebra does not establish the listed global connection hypotheses'},'translation_raw_reduced':[s.sstr(v) for v in tr],'translation_Dirichlet_trace':[s.sstr(v) for v in T*tr],'translation_Robin_trace':[s.sstr(s.cancel(v)) for v in N*(dm(tr)+tr/t)],'runtime_seconds':time.monotonic()-start}
Path(args.result).write_text(json.dumps(result,indent=2)+'\n');print('Exact asymptotic algebra done',result['runtime_seconds'],flush=True)
