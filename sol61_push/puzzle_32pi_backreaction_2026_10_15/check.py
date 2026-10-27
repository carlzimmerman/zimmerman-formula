import sympy as s,json
r,M=s.symbols('r M',positive=True)
N=s.Function('N')(r);nu=s.Function('nu')(r)
# Einstein tensor components for metric -exp(2nu)dt²+dr²/N+r²dOmega².
Gtt=(N-1)/r**2+s.diff(N,r)/r
Grr=(N-1)/r**2+2*N*s.diff(nu,r)/r
Gaa=N*(s.diff(nu,r,2)+s.diff(nu,r)**2+s.diff(nu,r)/r)+s.diff(N,r)*(s.diff(nu,r)/2+1/(2*r))
checks=[]
def check(name,e):
    assert s.simplify(e)==0,name
    checks.append(name)
L=r**2*s.exp(nu)*s.sqrt(N)*s.diff(nu,r)
check('lapse divergence from Einstein tensor',s.diff(L,r)-r**2*s.exp(nu)/(2*s.sqrt(N))*(-Gtt+Grr+2*Gaa))
U,k=s.symbols('U k',real=True)
rho=k/2+U;pr=k/2-U;pt=-k/2-U
check('static scalar active density',rho+pr+2*pt+2*U)
Np=(1-N)/r-r*rho/M**2
nup=(1-N)/(2*r*N)+r*pr/(2*M**2*N)
u=r**2*U/M**2
check('metric weight identity',1+r*nup+r*Np/(2*N)-(1-u)/N)
a,w,D,S,t=s.symbols('a w D S t',real=True)
# d/dlog(r) equations: a_dot=-D*a-t, w_dot=-D*w-S; t=u/N.
vc=(a+w)/(1+w)
vc_dot=s.diff(vc,a)*(-D*a-t)+s.diff(vc,w)*(-D*w-S)
expected=(-D*(a+w)-t*(1+w)-S*(1-a))/(1+w)**2
check('physical circular speed derivative',vc_dot-expected)
check('physical logarithmic slope',vc_dot/vc/(1+w)-(-D/(1+w)**2-(t*(1+w)+S*(1-a))/((a+w)*(1+w)**2)))
uu,nn=s.symbols('u n',positive=True)
reduced=vc_dot.subs({D:(1-uu)/nn,t:uu/nn})
check('potential-independent speed sign',reduced+((a+w)/nn+(uu/nn+S)*(1-a))/(1+w)**2)
check('exact physical slope upper bound',reduced/vc/(1+w)+1/(nn*(1+w)**2)+(uu/nn+S)*(1-a)/((a+w)*(1+w)**2))
# Independent known-vacuum benchmark: Schwarzschild-de Sitter.
mu,H=s.symbols('mu H',positive=True)
Nb=1-2*mu/r-H**2*r**2
nub=s.log(Nb)/2
sub={N:Nb,nu:nub}
check('SdS lapse flux',L.subs(sub).doit()-(mu-H**2*r**3))
check('SdS potential source',s.diff(L.subs(sub).doit(),r)+3*H**2*r**2)
print(json.dumps({'exact_checks':checks,'claim':'Conditional exact backreaction monotonicity, with physical Jordan circular speed','condition':'N>0, U>=0, positive branch and vacuum outer boundary, timelike circular orbit','non_claims':['No boundary-value existence proof','No numerical galaxy fit','No unique coefficient selection','No theorem for alternative scalar branches or boundary data']},indent=2))
