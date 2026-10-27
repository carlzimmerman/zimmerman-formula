import sympy as s,json
u,a,alpha,mu,M,kappa,k0,y,q,X=s.symbols('u a alpha mu M kappa k0 y q X',positive=True)
checks=[]
def ck(name,expr):
    assert s.simplify(expr)==0,(name,expr)
    checks.append(name)
gN=u*u/(a-u)
Fx=alpha**2*u/(a-u)
ck('static force equation',Fx*u/alpha**2-gN)
speed=1+u*s.diff(Fx,u)/Fx
ck('force slope characteristic identity',speed-u*s.diff(gN,u)/gN)
ck('exact characteristic speed',speed-(2*a-u)/(a-u))
ck('speed exceeds two gap',speed-2-u/(a-u))
# y=sqrt(X), q=a M/(alpha mu^2); valid 0<y<q.
F=alpha**2*(-y*y-2*q*y-2*q*q*s.log(1-y/q))
ck('reconstructed action derivative',s.diff(F,y)/(2*y)-alpha**2*y/(q-y))
ck('cubic small gradient coefficient',s.limit(F/y**3,y,0)-2*alpha**2/(3*q))
ck('zero vacuum kinetic',s.limit(alpha**2*y/(q-y),y,0))
# F_X=kappa sqrt(X), u=alpha mu^2 sqrt(X)/M.
a0=alpha**3*mu**2/(kappa*M)
ck('emergent acceleration', (kappa*M*u/(alpha*mu**2))*u/alpha**2-u*u/a0)
lam=s.symbols('lam',positive=True)
ck('vacuum response ratio', (lam*mu**4/M**2)/a0**2-lam*kappa**2/alpha**6)
# Healthy linear regulator produces an asymptotically linear force response.
regular=k0*u/alpha**2+u*u/a
ck('regulated weak gradient force ratio',s.limit(regular/u,u,0)-k0/alpha**2)
ck('regulator crossover acceleration',regular.subs(u,a*k0/alpha**2)-2*a*(k0/alpha**2)**2)
Psi,Phi,chi=s.symbols('Psi Phi chi',real=True)
ck('conformal lensing cancellation',(Psi+alpha*chi/M)+(Phi-alpha*chi/M)-(Psi+Phi))
print(json.dumps({'count':len(checks),'checks':checks,'scope':'Static weak-field conformal P(X) response, spacelike gradient, negligible potential, scalar stress neglected in Newtonian metric'},indent=2))
