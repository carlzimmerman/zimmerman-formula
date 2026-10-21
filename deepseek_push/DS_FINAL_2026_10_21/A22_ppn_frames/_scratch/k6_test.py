import sympy as sp
w, B1 = sp.symbols('w B1', real=True)
PhiS, PsiS = sp.symbols('Phi Psi', real=True)
mT2 = (1 - 2*PhiS - 2*w*B1 - w**2*(1 + 2*PsiS))/(1 - w**2)
lnN = sp.Rational(1, 2)*sp.log(1 - w**2) - sp.Rational(1, 2)*sp.log(1 - 2*PhiS - 2*w*B1 - w**2*(1 + 2*PsiS))
s = sp.series(lnN, w, 0, 3).removeO()
print(sp.expand(s))
print("coef w^2:", sp.simplify(sp.expand(s).coeff(w, 2)))
print("B=0, Psi=Phi:", sp.simplify(sp.expand(s).coeff(w, 2).subs({B1: 0, PsiS: PhiS})))
