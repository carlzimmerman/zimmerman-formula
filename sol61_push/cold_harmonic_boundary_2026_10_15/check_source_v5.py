import sys,json
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
N,b,h,rho,al,eps=s.symbols('N b h rho alpha eps',real=True)
checks=[]
def ck(n,e):
 assert s.simplify(e)==0,(n,e)
 checks.append(n)
j=s.Matrix(s.symbols('j0:3',real=True));dv=s.Matrix(s.symbols('v0:3',real=True));bv=s.Matrix([0,0,b])
qa,qb,qc,qd,qe,qf=s.symbols('qa qb qc qd qe qf',real=True)
Q=s.Matrix([[qa,qd,qe],[qd,qb,qf],[qe,qf,qc]])
sa,sb,sc,sd,se,sf=s.symbols('sa sb sc sd se sf',real=True)
Stress=s.Matrix([[sa,sd,se],[sd,sb,sf],[se,sf,sc]])
F0=bv.dot(j)-rho;f=-j;A=(F0*s.eye(3)-Stress)/2
var=al*(F0+bv.dot(f))-f.dot(dv)+F0*s.trace(Q)/2-s.trace(A*Q)
ck('all ten ADM source variations',var-(-al*rho+j.dot(dv)+s.trace(Stress*Q)/2))
for v in [al,*list(dv),qa,qb,qc,qd,qe,qf]:
 ck('source coefficient '+str(v),s.diff(var-(-al*rho+j.dot(dv)+s.trace(Stress*Q)/2),v))
# Local lapse/shift Hessian: old zero-quadratic-clock strain vs proper B potential.
v1,v2,v3=s.symbols('v1 v2 v3',real=True);V=s.Matrix([v1,v2,v3]);r2=V.dot(V)
old=h*(2*r2-r2*r2/2)/N**3;new=2*h*r2/N
variables=[N,v1,v2,v3]
Ho=s.hessian(old,variables).subs({v2:0,v3:0});Hn=s.hessian(new,variables)
oldschur=s.factor(Ho[0,0]-Ho[0,1]**2/Ho[1,1])
ck('old potential Schur exact',oldschur-(-12*h*v1**2*(v1**2+2)/(N**5*(2-3*v1**2))))
ck('new potential homogeneous null vector',s.trace((Hn*s.Matrix([N,v1,v2,v3])).T*(Hn*s.Matrix([N,v1,v2,v3]))))
ck('new potential determinant',Hn.det())
# Include arbitrary target Bstar and spatial potential: still degree one in lapse/shift.
bs,vc=s.symbols('bs vc',real=True)
proper=2*h*((v1/N-bs)**2+(v2/N)**2+(v3/N)**2)*N-N*vc
ck('target-subtracted proper potential homogeneity',N*s.diff(proper,N)+sum(V[i]*s.diff(proper,V[i]) for i in range(3))-proper)
P=s.Matrix(s.symbols('P0:3',real=True));ss=s.Matrix(s.symbols('s0:3',real=True));Hg=s.symbols('Hg',real=True)
# Pure EH plus proper B,C source: beta=N*s factors exact canonical Hamiltonian.
Hcanon=N*Hg+V.dot(P)-2*h*r2/N
ck('nonlinear canonical lapse factor',Hcanon.subs({v1:N*ss[0],v2:N*ss[1],v3:N*ss[2]})-N*(Hg+ss.dot(P)-2*h*ss.dot(ss)))
# Controller source of the proper F(B,C) inverse source for b=Lambda*sigma.
La,M=s.symbols('Lambda M',real=True)
xx,yy,zz=s.symbols('x y z',real=True);sig=s.Function('sigma')(xx,yy,zz)
lap=s.diff(sig,xx,2)+s.diff(sig,yy,2);grad=s.diff(sig,xx)**2+s.diff(sig,yy)**2
jz=M*M*La*lap/2;rr=-M*M*La*La*grad/4
Fval=La*sig*jz-rr
partial=s.diff(Fval,La)-jz*sig
want=M*M*La*(s.diff(sig**2,xx,2)+s.diff(sig**2,yy,2))/4
ck('proper source controller partial',partial-want)
Jx=M*M*La*s.diff(sig**2,xx)/4;Jy=M*M*La*s.diff(sig**2,yy)/4
ck('controller current cancellation',partial-s.diff(Jx,xx)-s.diff(Jy,yy))
ck('controller background source alternate',partial-(La*sig*s.diff(jz,La)-s.diff(rr,La)))
# Independent ADM Hamiltonian/momentum evaluation of the source components.
coords=[xx,yy,zz];bb=La*sig
KK=s.Matrix(3,3,lambda i,j:-(s.diff(bb,coords[i])*(1 if j==2 else 0)+s.diff(bb,coords[j])*(1 if i==2 else 0))/2)
rhoADM=M*M*(s.trace(KK)**2-s.trace(KK*KK))/2
jj=s.Matrix([M*M*(s.diff(s.trace(KK),coords[i])-sum(s.diff(KK[i,j],coords[j]) for j in range(3))) for i in range(3)])
ck('ADM normal energy source',rhoADM-rr)
ck('ADM momentum z source',jj[2]-jz)
ck('ADM momentum x source',jj[0]+M*M*La*s.diff(sig,xx,zz)/2)
ck('ADM momentum y source',jj[1]+M*M*La*s.diff(sig,yy,zz)/2)
# Exact reduced Hamiltonian of the displayed quadratic proper-velocity completion.
rootg=s.symbols('sqrtgamma',positive=True);Fsp=s.symbols('Fsp',real=True)
ff=s.Matrix(s.symbols('f0:3',real=True));BS=s.Matrix(s.symbols('Bstar0:3',real=True))
ww=-ss-BS
properF=Fsp+ff.dot(ww)+2*h*ww.dot(ww)
Hs=Hg+ss.dot(P)-rootg*properF
sstar=-BS+(P/rootg+ff)/(4*h)
sub={ss[i]:sstar[i] for i in range(3)}
pred=Hg-BS.dot(P)-rootg*Fsp+(P+rootg*ff).dot(P+rootg*ff)/(8*h*rootg)
ck('exact proper source reduced Hamiltonian',Hs.subs(sub)-pred)
for i in range(3):ck('proper shift equation '+str(i),s.diff(Hs,ss[i]).subs(sub))
res={'claim_id':'CHB-003','checks_passed':len(checks),'old_zero_clock_potential_schur':str(oldschur),'proper_potential':'N sqrt(gamma) F(Phi,C,B), B=-beta/N','source_jets':{'F0':str(F0),'F_B':str(f),'F_C':str(A)},'controller_source':'Mp^2 Lambda Delta_perp(sigma^2)/4; spatial positive current cancels at constant Lambda','scope':'Exact source-jet ADM variation and potential-sector lapse homogeneity for pure EH+F(B,C). Does not prove secondary constraint, nonlinear ghost freedom, or applicability after adding derivative-elastic operators.'}
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(res,indent=2))
