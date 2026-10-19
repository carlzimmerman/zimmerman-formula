#!/usr/bin/env python3
"""Independent algebraic benchmarks; never import target implementation."""
import argparse,json,math,sys,time
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--operator',required=True);p.add_argument('--finite-result',required=True);p.add_argument('--result',required=True);args=p.parse_args()
start=time.monotonic();d=json.loads(Path(args.operator).read_text());finite=json.loads(Path(args.finite_result).read_text())
t=s.symbols('t',positive=True);k,h,kp,hp=s.symbols('k h kp hp');z=s.symbols('z',positive=True);loc={'t':t,'k':k,'h':h,'kp':kp,'hp':hp}
def mat(key):return s.Matrix([[s.sympify(q,locals=loc) for q in row] for row in d[key]])
G=mat('Gram');V=mat('V_raw').applyfunc(s.cancel);A0=mat('origin_A0');S=mat('S_Gorthonormal');T=mat('Dirichlet_T');N=mat('normal_N');ls=d['origin_l'];checks={}
def equal(name,a,b):
 res=a-b
 assert all(s.cancel(v)==0 for v in res),name
 checks[name]=True
# Independent raw Gram and orbital Laplacian, color index first.
Gi=s.zeros(10);Gi[:4,:4]=s.Matrix([[1,s.Rational(1,3),s.Rational(1,3),s.Rational(1,3)],[s.Rational(1,3),1,s.Rational(1,3),s.Rational(1,3)],[s.Rational(1,3),s.Rational(1,3),1,s.Rational(1,3)],[s.Rational(1,3),s.Rational(1,3),s.Rational(1,3),s.Rational(1,3)]])
Gi[4:7,4:7]=s.Matrix([[2,s.Rational(2,3),-s.Rational(2,3)],[s.Rational(2,3),s.Rational(2,3),0],[-s.Rational(2,3),0,s.Rational(2,3)]])
Gi[7:10,7:10]=s.Matrix([[1,s.Rational(1,3),0],[s.Rational(1,3),s.Rational(1,3),0],[0,0,s.Rational(2,3)]])
# target B5 = independent T5-T6+T7 and target B4=-T5.
C=s.zeros(10)
for row,col,val in [(0,0,1),(2,1,1),(1,2,1),(3,3,1),(4,4,-1),(4,5,1),(5,5,-1),(6,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1)]:C[row,col]=val
equal('independent angular Gram',C.T*Gi*C,G)
Ai=s.diag(2,2,2,12,0,6,6,0,6,2)
Ai[0,3]=Ai[1,3]=Ai[2,3]=-2
Ai[4,5]=-2;Ai[4,6]=2;Ai[7,8]=-2
equal('independent orbital matrix',C.inv()*Ai*C,A0)
equal('canonical orthonormality',S.T*G*S,s.eye(10))
equal('canonical centrifugal eigenvalues',S.inv()*A0*S,s.diag(*[ell*(ell+1) for ell in ls]))
equal('angular symmetry',G*V,(G*V).T)
Ni=s.zeros(3,10);Ni[0,2]=1;Ni[1,0]=Ni[1,1]=Ni[1,3]=1;Ni[2,4]=1
equal('independent normal trace',Ni*C,N)
assert T.rank()==7 and N.rank()==3 and T.col_join(N).rank()==10
checks['mixed wall has 7D plus 3R']=True
reference=s.factor((T*S).col_join(N*S*s.diag(*[ell+2 for ell in ls])).det())
assert reference==s.Rational(5103,8)
assert sum(ell+1 for ell in ls)-3==20
checks['free mixed reference 5103 x20 /8']=True
K=2*t*z/(z*z-1);HH=(z*z+1)/(z*z-1)-1/t
sub={k:K,h:HH,kp:-K*HH,hp:(1-K*K)/t**2}
def rat(q):return s.cancel(q.subs(sub))
def dt(q):return s.diff(q,t)+z*s.diff(q,z)
def dm(m):return m.applyfunc(dt)
Vr=V.applyfunc(rat)
# Independently derived exact translation a_mu=p_j F_jmu, in target reduced basis.
U=s.zeros(10,1);U[4]=-k*h;U[6]=-(1-k*k)/t+k*h;U[7]=k*h;U[8]=(1-k*k)/t-k*h
Ur=U.applyfunc(rat)
equal('exact translation H a=0',-dm(dm(Ur))+Vr*Ur,s.zeros(10,1))
# Translation wall traces: T U=(-kh, ..., kh, b*t-kh), hence not Dirichlet.
assert s.simplify((T*U)[2]+k*h)==0 and s.simplify((T*U)[4]-k*h)==0
checks['translation has nonzero finite wall Dirichlet traces']=True
# Manually derived gauge-gradient on c=(f*p+g*q*n+j*w), Ughost=t(f,g,j).
Ag=s.zeros(10,3);Bg=s.zeros(10,3)
Ag[1,0]=Ag[3,1]=Ag[5,2]=1
Bg[0,0]=-(1-k)/t;Bg[0,1]=k/t
Bg[1,0]=-1/t
Bg[2,0]=(1-k)/t;Bg[2,1]=1/t
Bg[3,1]=-(k+2)/t
Bg[4,2]=-1/t;Bg[5,2]=-2/t;Bg[6,2]=(1-k)/t
Bg[7,2]=-h;Bg[8,2]=h;Bg[9,0]=h
# Ghost U_RE from the independently known Cartesian covariant scalar expression.
UG=s.Matrix([[(2+2*k*k)/t**2,-2*s.sqrt(2)*k/t**2,0],[-2*s.sqrt(2)*k/t**2,h*h+(1+k*k)/t**2,0],[0,0,h*h+(1+k*k)/t**2]])
L=s.Matrix([[0,1/s.sqrt(2),0],[1,-1/s.sqrt(2),0],[0,0,1/s.sqrt(2)]])
Mq=(L*UG*L.inv()).applyfunc(s.cancel);Mr=Mq.applyfunc(rat);Br=Bg.applyfunc(rat)
equal('gauge H P=P M derivative coefficients',Vr*Ag-2*dm(Br)-Ag*Mr,s.zeros(10,3))
equal('gauge H P=P M value coefficients',Vr*Br-dm(dm(Br))-Ag*dm(Mr)-Br*Mr,s.zeros(10,3))
equal('Dirichlet ghost gives vector D wall',T*Ag,s.zeros(7,3))
equal('Dirichlet ghost gives vector R wall',N*(Bg+Ag/t),s.zeros(3,3))
# Independently check background gauge of translation via integration-by-parts adjoint.
Gq=L.T*s.Matrix([[s.Rational(1,3),0,0],[0,s.Rational(1,3),0],[0,0,s.Rational(1,3)]])*L
# Instead use exact Gram of p, qn, w; divergence vanishes iff Pdag U=0.
Gq=Gi[7:10,7:10]
div=-Ag.T*G*dm(Ur)+Br.T*G*Ur
equal('translation background gauge G=0',div,s.zeros(3,1))
# Stored arithmetic only: this does not reproduce numerical integration.
for row,case in zip(finite['summary'],finite['numerical_cases'][5:]):
 assert row['x']==case['x'] and row['log_D_vector']==case['log_D_vector']
 ghost=float(row['log_D_ghost_per_m']);vector=row['log_D_vector']
 assert abs(row['log_Gaussian_J1']-3*(ghost-vector/2))<1e-11
 assert abs(row['log_D_transverse_per_m']-(vector-ghost))<1e-11
 assert row['passes_declared_finite_stability_criteria']
checks['recorded multiplicity and ghost arithmetic']=True
result={'checks':checks,'reference_boundary_constant':str(reference),'reference_x_power':20,'translation_raw_reduced':[s.sstr(v) for v in U],'gauge_gradient_derivative':[[str(v) for v in row] for row in Ag.tolist()],'gauge_gradient_value':[[str(v) for v in row] for row in Bg.tolist()],'finite_radii_reviewed':[v['x'] for v in finite['summary']],'numerical_integration_repeated':False,'runtime_seconds':time.monotonic()-start,'software':{'python':sys.version.split()[0],'sympy':s.__version__},'non_claims':['No ODE accuracy certification','No asymptotic coefficient or physical normalization']}
Path(args.result).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':checks,'runtime_seconds':result['runtime_seconds']},indent=2))

