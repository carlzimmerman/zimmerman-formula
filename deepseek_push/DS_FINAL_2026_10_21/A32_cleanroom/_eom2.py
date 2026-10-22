import sympy as sp

t, kk = sp.symbols('t k', real=True)
a = sp.Function('a')(t)
sig = sp.Function('sigma')(t)
Lam = sp.symbols('Lambda', real=True)
Kc = sp.Symbol('K', positive=True)

# averaged quadratic Lagrangian per mode, from _eom.py (verified against exact ADM pieces):
# L2 = a/(16K) [ (2L s^2 + sdot^2) a^2 + 8 a s sdot adot + (6 adot^2 - k^2) s^2 ]
L2 = a/(16*Kc)*((2*Lam*sig**2 + sp.diff(sig, t)**2)*a**2
                + 8*a*sig*sp.diff(sig, t)*sp.diff(a, t)
                + (6*sp.diff(a, t)**2 - kk**2)*sig**2)

s, sd = sp.symbols('s sd')
Ls = L2.subs({sp.diff(sig, t, 2): sp.Symbol('sdd'), sp.diff(sig, t): sd, sig: s})
Ls = Ls.subs({sp.diff(a, t, 2): sp.Symbol('add'), sp.diff(a, t): sp.Symbol('ad'), a: sp.Symbol('A')})

dLds = sp.diff(Ls, s)
dLdsd = sp.diff(Ls, sd)
# d/dt of dL/dsd, with s, sd, A, ad functions of t
dLdsd_t = (sp.diff(dLdsd, s)*sd + sp.diff(dLdsd, sd)*sp.Symbol('sdd')
           + sp.diff(dLdsd, sp.Symbol('A'))*sp.Symbol('ad')
           + sp.diff(dLdsd, sp.Symbol('ad'))*sp.Symbol('add'))
EL = sp.simplify(dLds - dLdsd_t)
back = {sp.Symbol('A'): a, sp.Symbol('ad'): sp.diff(a, t), sp.Symbol('add'): sp.diff(a, t, 2),
        s: sig, sd: sp.diff(sig, t), sp.Symbol('sdd'): sp.diff(sig, t, 2)}
EL = sp.simplify(EL.subs(back))
print("EL =", EL)
H = sp.diff(a, t)/a
target = sp.diff(sig, t, 2) + 3*H*sp.diff(sig, t) + kk**2*sig/a**2
print("\nEL / (a^3/(8K)) =", sp.simplify(sp.expand(EL*8*Kc/a**3)))
q = sp.simplify(sp.expand(EL*8*Kc/a**3))
print("\nmass-term = (q - target) =", sp.simplify(q - target))
print("\nusing 3H^2=8piG rho+Lambda, 2Hdot+3H^2=-8piGp+Lambda -> mass = 2(2Hdot+3H^2-Lambda):")
print("  2*(2*Hdot + 3H^2 - Lam) with Hdot=d/dt(ad/A):", sp.simplify(2*(2*(sp.diff(a,t,2)/a - (sp.diff(a,t)/a)**2) + 3*H**2 - Lam)))