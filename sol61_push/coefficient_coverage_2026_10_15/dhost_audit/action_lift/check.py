import sympy as s,json
b,ph,ps,phx,psx,M2,A,q,rho=s.symbols('b ph ps phx psx M2 A q rho',real=True)
checks={}
def ck(n,e):
 checks[n]=s.factor(e)==0
 assert checks[n],n
# Linear potential dictionary induced by C(X), at background C=1.
pt=(1-b)*ph;st=ps+b*ph
Lgrad=M2*((psx+b*phx)**2-2*(1-b)*phx*(psx+b*phx))
ck('spatial constraint',s.diff(Lgrad,psx)-2*M2*(psx-(1-2*b)*phx))
ck('reduced gradient',Lgrad.subs(psx,(1-2*b)*phx)+M2*(1-b)**2*phx**2)
ck('slip map',st.subs(ps,(1-2*b)*ph)-pt)
ck('lensing map',(ph+(1-2*b)*ph)/2-(1-b)*ph)
# Seed clock P(Y)=-V0+A/2*(Y+q^2)^2, Y negative timelike.
Y,V0,eps,dotpi,gradpi2=s.symbols('Y V0 eps dotpi gradpi2',real=True)
P=-V0+A*(Y+q**2)**2/2
ck('vacuum pressure',P.subs(Y,-q**2)+V0)
ck('zero vacuum current',s.diff(P,Y).subs(Y,-q**2))
ck('vacuum density',(2*Y*s.diff(P,Y)-P).subs(Y,-q**2)-V0)
Ypert=-(q+eps*dotpi)**2+eps**2*gradpi2
ck('fixed metric scalar quadratic',s.expand(P.subs(Y,Ypert)).coeff(eps,2)-2*A*q**2*dotpi**2)
Ylapse=-q**2/(1+eps*pt)**2
ck('lapse quadratic',s.diff(P.subs(Y,Ylapse),eps,2).subs(eps,0)/2-2*A*q**4*pt**2)
Lred=-M2*(1-b)**2*phx**2+2*A*q**4*(1-b)**2*ph**2-rho*ph
phxx=s.symbols('phxx')
EL=s.diff(Lred,ph)-s.diff(Lred,phx,2)*phxx
ck('static sourced equation',EL-(2*M2*(1-b)**2*phxx+4*A*q**4*(1-b)**2*ph-rho))
ck('rational lensing factor',(1-b).subs(b,-s.Rational(1,4))-s.Rational(5,4))
# Invertible power conformal map: log derivative dlog(Y)/dlog(-X)=1-b.
x,q2=s.symbols('x q2',positive=True)
C=(x/q2)**b;yy=-x/C
ck('inverse Jacobian',s.diff(yy,x)*x/yy-(1-b))
print(json.dumps({'count':len(checks),'checks':checks,'scope':'Conformal dictionary, seed vacuum and leading static quadratic reduction; no full perturbation health or MOND law'},indent=2))
