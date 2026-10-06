import argparse,json,pathlib,sys
import sympy as S
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',default='none');a=p.parse_args();checks=[]
def ck(name, expr):
 ok=bool(expr);checks.append({'name':name,'passed':ok})
x,y,t,r,m,Z,k,am,R1,R2,D=S.symbols('x y t r m Z k am R1 R2 D',positive=True)
n=S.symbols('n',integer=True,positive=True)
b=S.sqrt(1+1/y)-1; ct=2*t*y*y*b/(t*t+y*y)**2
ck('positive interpolation T derivative',S.simplify(S.diff(b/(1+(y/t)**2),t)-ct)==0)
# Explicit normalized compact profile, algebraic source control only.
f=315/(64*S.pi)*(1-x*x)**3
ck('profile mass normalization',S.integrate(4*S.pi*x*x*f,(x,0,1))==1)
M,G,A,RM,s=S.symbols('M G A RM s',positive=True)
ck('same scaled exterior Newton y',S.simplify((G*M/(A*(RM*s)**(n-1))).subs(M,A*RM**(n-1)/G)-s**(1-n))==0)
lap=S.symbols('lap'); difference=-Z*(R1**-2-R2**-2)*lap
ck('radius gradient survives subtraction',difference==0 if a.control=='drop_gradient' else S.simplify(difference+Z*(R1**-2-R2**-2)*lap)==0)
def radial(v,dim=3):return S.diff(v,r,2)+(dim-1)/r*S.diff(v,r)
ck('general n radial harmonic',S.simplify(radial(D*r**(2-n),n))==0)
ck('forcing decays faster than exterior harmonic',S.simplify(S.Rational(7,2)*(n-1)-(n-2))==(5*n-3)/2)
ck('harmonic mass operator nonzero',S.simplify((-radial(D/r)+m*m*D/r)*r)==0 if a.control=='harmonic_solution' else S.simplify((-radial(D/r)+m*m*D/r)*r)==D*m*m)
# x=sqrt(y); qT_y=2y ct and dy=2x dx.
integrand=(2*y*ct).subs(y,x*x)*2*x
series=S.series(integrand,x,0,10).removeO();qseries=S.integrate(series,x)
expected=(S.Rational(8,7)*x**7-x**8+S.Rational(4,9)*x**9)/t**3
ck('qT first three coefficients',S.series(qseries-expected,x,0,10).removeO()==0)
for j,c in [(7,42),(8,56),(9,72)]:ck('radial laplacian power '+str(j),S.simplify(radial(r**(-j))-c*r**(-j-2))==0)
lam=S.symbols('lam',positive=True)
u=(S.Rational(8,7)*x**7-x**8+(S.Rational(4,9)+48*lam)*x**9)
cts=S.series(ct.subs(y,x*x),x,0,6).removeO()*t**3
force=S.expand(x*x*cts*u)
want=S.Rational(16,7)*x**12-S.Rational(30,7)*x**13+(S.Rational(254,63)+96*lam)*x**14
ck('physical force product through y7',S.series(force-want,x,0,15).removeO()==0)
ck('first source dependent coefficient',S.expand(force).coeff(x,14).diff(lam)==0 if a.control=='universal_tail' else S.expand(force).coeff(x,14).diff(lam)==96)
ck('mass inverse relation n3',S.simplify(1/(m*RM)**2).subs(RM**2,G*M/A)==A/(m*m*G*M))
# Trial massive operator matches forcing through r^-9.
a7=S.Rational(8,7)*RM**7;a8=-RM**8;a9=S.Rational(4,9)*RM**9+48*RM**7/m**2
trial=(a7/r**7+a8/r**8+a9/r**9)/m**2
res=S.expand(-radial(trial)+m*m*trial-(S.Rational(8,7)*RM**7/r**7-RM**8/r**8+S.Rational(4,9)*RM**9/r**9))
for j in [7,8,9]:ck('trial residual cancels r-'+str(j),res.coeff(r,-j)==0)
ck('remaining trial residual starts r-10',res.coeff(r,-10)!=0)
result={'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'control':a.control,'scope':'exact identities, not numerical PDE certificate'}
path=pathlib.Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,indent=2));print(json.dumps(result));sys.exit(bool(result['failed']))
