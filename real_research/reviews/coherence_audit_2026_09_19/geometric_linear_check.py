import sympy as s
x0,x1,x2,x3=s.symbols('t x y z',real=True); X=[x0,x1,x2,x3]; e,Q0=s.symbols('epsilon Q0',real=True)
Psi,b,Phi,T,P=[s.Function(n)(x0,x1) for n in ['Psi','b','Phi','T','P']]
g=s.diag(-(1+e*Psi)**2,(1-e*Phi)**2,(1-e*Phi)**2,(1-e*Phi)**2);g[0,1]=g[1,0]=e*b
gi=g.inv(); tau=x0+e*T; phi=Q0*x0+e*P
Dt=s.Matrix([s.diff(tau,v) for v in X]); Dp=s.Matrix([s.diff(phi,v) for v in X]); norm=-(Dt.T*gi*Dt)[0]
nd=-Dt/s.sqrt(norm);nu=gi*nd;q=gi+nu*nu.T;Q=(nu.T*Dp)[0];V=Dp+nd*Q
lin=lambda f:s.simplify(s.diff(f,e).subs(e,0))
G=[[[sum(gi[l,r]*(s.diff(g[r,m],X[n])+s.diff(g[r,n],X[m])-s.diff(g[m,n],X[r])) for r in range(4))/2 for n in range(4)] for m in range(4)] for l in range(4)]
H=s.Matrix(4,4,lambda i,j:s.diff(phi,X[i],X[j])-sum(G[r][i][j]*Dp[r] for r in range(4)))
D=s.Matrix(4,4,lambda i,j:s.diff(V[j],X[i])-sum(G[r][i][j]*V[r] for r in range(4)))
qmix=s.eye(4)+nd*nu.T
A=qmix*D*qmix.T
C=sum(q[i,j]*H[i,j] for i in range(4) for j in range(4))
print('n_dn first:',[lin(f) for f in nd]);print('n_up first:',[lin(f) for f in nu]);print('V first:',[lin(f) for f in V]);print('A spatial first:',s.Matrix(3,3,lambda i,j:lin(A[i+1,j+1])))
print('Code C first:',lin(C))
assert s.simplify(lin(A[1,1])-s.diff(P-Q0*T,x1,2))==0
assert s.simplify(lin(C)-(s.diff(P,x1,2)+Q0*s.diff(b,x1)+3*Q0*s.diff(Phi,x0)))==0
print('Direct geometric first-order assertions passed')
