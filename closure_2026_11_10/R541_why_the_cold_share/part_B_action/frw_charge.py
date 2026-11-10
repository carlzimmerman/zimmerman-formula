import sympy as sp
t=sp.symbols('t'); K,mu,Lam,C,rb0,x,y,z=sp.symbols('K mu_K Lambda C rho_b0 x y z',positive=True)
N=sp.Function('N')(t); a=sp.Function('a')(t); tau=sp.Function('tau')(t)
Q=sp.diff(tau,t)/N
# minisuperspace of action (A) with P=0 (E1 + isotropy), F(0)=0, W(0)=0; 2K=8piG
L_grav=(-6*a*sp.diff(a,t)**2/N - 2*Lam*N*a**3)/(4*K)    # sqrt(-g)(R-2Lam)/4K up to total derivative
L_K=N*a**3*mu**2*(Q-1)**2/(2*K)
L_m=-N*a**3*rb0/a**3                                    # dust baryons: -sqrt(-g) rho_b
L=L_grav+L_K+L_m
print("tau is cyclic (dL/dtau = 0):", sp.diff(L,tau)==0)
p_tau=sp.simplify(sp.diff(L,sp.diff(tau,t)))
print("first integral p_tau =", p_tau, " -> a^3 mu^2 (Q-1)/K = C, C unconstrained")
# Friedmann constraint = dL/dN = 0 ; read off rho_K
Ham=sp.simplify(sp.diff(L,N).subs(N,1))
rhoK=sp.simplify(-sp.diff(L_K,N).subs(N,1)/a**3)
qs=sp.symbols('q')
print("rho_K(Q) =", sp.factor(rhoK.subs(sp.diff(tau,t),qs)), " (record: mu^2(Q^2-1)/2K)")
Qsol=1+C*K/(mu**2*a**3)
rho_on=sp.simplify((mu**2*(qs**2-1)/(2*K)).subs(qs,Qsol))
print("on shell rho_K =", sp.expand(rho_on))
H=sp.symbols('H')
fried=sp.Eq(3*H**2/(2*K), rb0/a**3+rho_on+Lam/(2*K))
print("Friedmann:", fried)
print("Solve Friedmann for C (it only trades C for H):", sp.solve(fried,C)[:1])
# Ratio R = rho_K/rho_b at Q->1 (late): (C/a^3)/(rb0/a^3) = C/rb0  constant
print("late R =", sp.limit(rho_on*a**3/rb0, a, sp.oo) if False else sp.simplify(sp.series(rho_on.subs(a,1/z),z,0,4).removeO()*1/(rb0*z**3)))

# Leaf identity: for P tangent to leaves, Pi = nabla.P - P.A = (1/sqrt h) d_i(sqrt h P^i)
# static metric ds^2=-N^2dt^2+h_ij dx dx, diagonal h for the check
Nx=sp.Function('N')(x,y,z); h1,h2,h3=[sp.Function(f'h{i}')(x,y,z) for i in (1,2,3)]
P=[sp.Function(f'P{i}')(x,y,z) for i in (1,2,3)]; X=[x,y,z]
sqg=Nx*sp.sqrt(h1*h2*h3); sqh=sp.sqrt(h1*h2*h3)
divP=sum(sp.diff(sqg*P[i],X[i]) for i in range(3))/sqg
A=[sp.diff(sp.log(Nx),X[i]) for i in range(3)]   # A_i = d_i ln N (A_m=-h d l, l=ln Q=-ln N)
Pi=divP-sum(P[i]*A[i] for i in range(3))
print("Pi - D_iP^i =", sp.simplify(Pi-sum(sp.diff(sqh*P[i],X[i]) for i in range(3))/sqh))
# charge density part (1/Q) nabla_m[(1+g Pi)P^m], Q=1/N, integrated with sqrt h:
g=sp.symbols('gamma_L'); Y=[(1+g*Pi)*P[i] for i in range(3)]
term=sqh*Nx*sum(sp.diff(sqg*Y[i],X[i]) for i in range(3))/sqg
print("sqrt(h)*(1/Q)div[(1+gPi)P] - d_i(N sqrt h (1+gPi)P^i) =", sp.simplify(term-sum(sp.diff(Nx*sqh*Y[i],X[i]) for i in range(3))))

# baryon-current coupling eps * J_B^m d_m tau with div J_B=0 is a total derivative:
f=sp.Function('f')(t); nB0=sp.symbols('n_B0')
LB=sp.symbols('eps')*(nB0/a**3)*a**3*sp.diff(tau,t)   # sqrt(-g) J_B^t d_t tau, J_B^t = n_B/N, n_B a^3 = const
print("eps*J_B.dtau term in minisuperspace =", sp.simplify(LB), "-> d/dt(eps n_B0 tau): total derivative, E3 unchanged")
