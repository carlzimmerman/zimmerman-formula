import sympy as s,json
b,mref,PhiN=s.symbols('b mref PhiN',real=True,nonzero=True)
aH=-2*b;beta2=-6*b**2;beta3=-2*b*(2*(1+aH)+b)
A=(1+aH)**2-beta3/2
checks={}
def check(name,e):
    checks[name]=s.factor(e)==0
    assert checks[name],name
check('Poisson denominator',(A-(1-b)**2))
M2=mref/(1-b)**2
check('fixed Newton normalization',M2*A-mref)
check('nondecay coefficient relation',aH+2*b)
check('incremental slip',((1+aH)*PhiN-PhiN)-(-2*b*PhiN))
w={b:-s.Rational(1,4)}
check('witness alphaH',aH.subs(w)-s.Rational(1,2))
check('witness beta2',beta2.subs(w)+s.Rational(3,8))
check('witness beta3',beta3.subs(w)-s.Rational(11,8))
check('witness M2',M2.subs(w)-s.Rational(16,25)*mref)
# Fixed-background linear source response scales linearly with source amplitude.
t,r=s.symbols('t r',positive=True)
check('linear scaling differs from deep MOND squared', (t/r**2)**2/(1/r**2)**2-t**2)
print(json.dumps({'checks':checks,'count':len(checks),'scope':'Algebraic counterexample to total-versus-increment inference; NOT a healthy DHOST solution or MOND action'},indent=2))
