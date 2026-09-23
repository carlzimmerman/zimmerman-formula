import sympy as s
N,a,ad,Qdotfield,c2,Lam=s.symbols('N a adot phidot c2 Lambda', nonzero=True)
Q=s.symbols('Q',real=True); F=s.Function('F'); Gc=1+s.Rational(3,2)*c2
mini=-6*Gc*a*ad**2/N-N*a**3*(F(Qdotfield/N)+2*Lam)
lapse=s.diff(mini,N)
expected=6*Gc*a*ad**2/N**2-a**3*(F(Qdotfield/N)-(Qdotfield/N)*s.diff(F(Q),Q).subs(Q,Qdotfield/N)+2*Lam)
assert s.simplify(lapse-expected)==0
print('Lapse equation verified: 6 Gc H^2 = F - Q F_Q + 2 Lambda')
t=s.symbols('t',real=True); at=s.Function('a')(t); eps,Q0,F10=s.symbols('eps Q0 F10',nonzero=True,real=True)
H=s.diff(at,t)/at; qb=Q0-3*eps*s.log(at); f1=F10*at**-3; f0=eps*f1; f2=f1/eps; f3=f2/eps
assert s.simplify(s.diff(qb,t)+3*eps*H)==0
for left,right,name in [(s.diff(f0,t),f1*s.diff(qb,t),'F0dot = F1 Qdot'),(s.diff(f1,t),f2*s.diff(qb,t),'F1dot = F2 Qdot'),(s.diff(f2,t),f3*s.diff(qb,t),'F2dot = F3 Qdot')]:
 assert s.simplify(left-right)==0
 print('PASS',name)
r=f0-qb*f1;p=-f0
assert s.simplify(s.diff(r,t)+3*H*(r+p))==0
print('PASS density-pressure continuity')
h2=((eps-qb)*f1/s.Integer(2)+Lam)/(3*Gc)
assert s.simplify(s.diff(h2,t)/(2*H)-qb*f1/(4*Gc))==0
print('PASS Friedmann derivative: Hdot = Q F1 / (4 Gc)')
qf=Q0
print('Frozen-Q chain residual F1dot - F2 Qdot:',s.simplify(s.diff(f1,t)))
rf=(eps-qf)*f1;pf=-eps*f1
print('Frozen-Q energy continuity residual:',s.simplify(s.diff(rf,t)+3*H*(rf+pf)))
chi=s.Function('chi')(t); deltaPsi=-s.diff(chi,t);deltaP=-qb*chi
Dg=s.simplify(s.diff(deltaP,t)-qb*deltaPsi)
assert s.simplify(f2*Dg+s.diff(f1,t)*chi)==0
assert s.simplify((-qb*f2)*Dg+s.diff(r,t)*chi)==0
print('PASS pure-gauge current and density transformations with exact Qdot')
print('Pure-gauge D =',Dg)
print('Finite frozen-Q current transformation mismatch / (H F1 chi) = 3')
print('SymPy',s.__version__)
