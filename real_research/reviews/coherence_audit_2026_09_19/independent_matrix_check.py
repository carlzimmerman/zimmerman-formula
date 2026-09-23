import sympy as s, json, hashlib, pathlib, sys
root=pathlib.Path(__file__).resolve().parents[3]
t,x,y,z=s.symbols('t x y z', real=True); k,w=s.symbols('k omega', real=True)
KB,c14,c2,Q0,beta,xi,F1,F2=s.symbols('K_B c14 c_2 Q_0 beta xi F_1 F_2',real=True); c=2-KB
Psi,b,Phi,T,P=[s.Function(n)(t,x) for n in ['Psi','b','Phi','T','P']]
fs=[Psi,b,Phi,T,P]; X=lambda f:s.diff(f,x); D=lambda f:s.diff(f,t)
U=P-Q0*T
C=X(X(P))+Q0*X(b)+3*Q0*D(Phi)
theta=-X(X(T))-X(b)-3*D(Phi)
L=-6*D(Phi)**2+2*X(Phi)**2-4*X(Psi)*X(Phi)-4*D(Phi)*X(b)
L+=c14*X(Psi-D(T))**2-c2*theta**2+2*c*X(Psi-D(T))*X(U)-c*beta*X(U)**2
L+=F1*(Q0*b**2/2-Q0*X(T)**2/2-3*Q0*Phi*Psi+3*Phi*D(P)+(b+X(T))*X(P))-F2*(D(P)-Q0*Psi)**2/2
L-=c*xi**2*C**2
amps=s.symbols('A0:5'); wave=s.exp(s.I*(k*x-w*t)); sub=dict(zip(fs,[v*wave for v in amps]))
def EL(L,f):
 out=s.diff(L,f)
 for der in L.atoms(s.Derivative):
  if der.expr==f:
   vs=[v for v,count in der.variable_count for _ in range(count)]
   out+=(-1)**len(vs)*s.diff(s.diff(L,der),*vs)
 return s.expand(out)
M=s.zeros(5)
for i,f in enumerate(fs):
 eq=s.expand(EL(L,f).subs(sub).doit()/wave)
 for j,A in enumerate(amps):M[i,j]=s.simplify(eq.coeff(A))
data=json.loads((root/'real_research/clock_2026/L287_dirac_count_clock_lapse_results.json').read_text())
loc={str(v):v for v in [k,w,KB,c14,c2,Q0,beta,xi,F1,F2]}; loc['I']=s.I
old=s.Matrix(5,5,lambda i,j:s.sympify(data['M_entries'][f'{i}{j}'],locals=loc))
assert all(s.simplify(e)==0 for e in M-old)
print('Independent quadratic reconstruction: all 25 entries match')
g=s.Matrix([s.I*w,s.I*k,0,-1,-Q0])
assert all(s.simplify(e)==0 for e in M*g)
print('Correct time-gauge residual:',[s.factor(e) for e in M*g])
print('F1=0 correct gauge kernel:',all(s.simplify(e.subs(F1,0))==0 for e in M*g))
print('Generic determinant skipped; nonzero symbolic null vector already proves singularity')

print('Projected-gradient trace identity:',s.simplify(C+Q0*theta-X(X(U))))
# Independent direct Christoffel evaluation for homogeneous lapse-FRW.
a=s.Function('a')(t); N=s.Function('N')(t); ph=s.Function('ph')(t); coords=[t,x,y,z]
gmet=s.diag(-N**2,a**2,a**2,a**2); gi=gmet.inv(); nd=s.Matrix([-N,0,0,0]); nu=gi*nd
q=gi+nu*nu.T; dp=s.Matrix([s.diff(ph,v) for v in coords]); V=dp+nd*(nu.dot(dp))
Gamma=[[[s.simplify(sum(gi[l,r]*(s.diff(gmet[r,m],coords[n])+s.diff(gmet[r,n],coords[m])-s.diff(gmet[m,n],coords[r])) for r in range(4))/2) for n in range(4)] for m in range(4)] for l in range(4)]
Hess=s.Matrix(4,4,lambda m,n:s.diff(ph,coords[m],coords[n])-sum(Gamma[l][m][n]*dp[l] for l in range(4)))
Cbg=s.simplify(sum(q[m,n]*Hess[m,n] for m in range(4) for n in range(4)))
print('FRW V:',list(V));print('FRW implemented C:',Cbg)
assert V==s.zeros(4,1)
assert s.simplify(Cbg+3*s.diff(a,t)*s.diff(ph,t)/(a*N**2))==0
print('Versions:',sys.version.split()[0],s.__version__)
for rel in ['qwen_claude_field_theory/closure_2026/THE_ACTION_2026-09-05.md','real_research/clock_2026/L287_dirac_count_clock_lapse.py','real_research/clock_2026/clock_action_build.py','real_research/clock_2026/L287_dirac_count_clock_lapse_results.json']:
 print('sha256',hashlib.sha256((root/rel).read_bytes()).hexdigest(),rel)
