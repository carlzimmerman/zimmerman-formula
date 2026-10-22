import sympy as sp
r, K, a0, gam, Lam = sp.symbols('r K a0 gamma Lambda', positive=True)
m = sp.Symbol('m', positive=True)
N = sp.Function('N')(r); f = sp.Function('f')(r); P = sp.Function('P')(r)
R3 = -2*sp.diff(f, r, 2)/f**2 + sp.Rational(3, 2)*sp.diff(f, r)**2/f**3 - 4*sp.diff(f, r)/(r*f**2)
u = K*P
W = (a0**2/K)*(-u/a0 - sp.log(1 - u/a0))
d = f**sp.Rational(-3, 2)*(1/r**2)*sp.diff(r**2*sp.sqrt(f)*P, r)
rho = sp.Function('rho')(r)
L = 4*sp.pi*r**2*(N*f**sp.Rational(3, 2)*(R3/(4*K) - W - gam*d**2/2) + sp.sqrt(f)*P*sp.diff(N, r) - rho*N*f**sp.Rational(3, 2))
EN = sp.diff(L, N) - sp.diff(sp.diff(L, sp.diff(N, r)), r)
EP = sp.diff(L, P) - sp.diff(sp.diff(L, sp.diff(P, r)), r)
Ef = (sp.diff(L, f) - sp.diff(sp.diff(L, sp.diff(f, r)), r) + sp.diff(sp.diff(L, sp.diff(f, r, 2)), r, 2))
# ---- lapse equation -> (H)
EN_s = sp.simplify(EN/(4*sp.pi*r**2*f**sp.Rational(3, 2)))
H_res = sp.simplify(EN_s + (R3 - 2*Lam - 4*K*(rho + d + W + gam*d**2/2))/(4*K))
print("EL_N / (4 pi r^2 f^(3/2)) =", sp.simplify(EN_s))
print("(H) residual (EL_N vs H):", sp.simplify(H_res.subs(Lam, 0)))
# ---- P equation
EP_s = sp.simplify(EP/(4*sp.pi*r**2*sp.sqrt(f)))
print("\nEL_P simplified:", sp.simplify(EP_s))
# A33 (P-sph): n1(1+gamma d) + gamma d' = K W'(u) ;  build residual with n1 = N'/N, f=1
N1 = sp.Function('N1')(r)
Wp = a0*u/(a0 - u)/K
# at f = 1: d = P' + 2P/r
d1 = sp.diff(P, r) + 2*P/r
EP_f1 = sp.simplify(EP_s.subs({f: 1, sp.Derivative(f, r): 0, sp.Derivative(f, r, 2): 0, sp.Derivative(f, r, 3): 0,
                               sp.Derivative(N, r): N1, sp.Derivative(N, r, 2): 0}))
target = (N1*(1 + gam*d1) + gam*sp.diff(d1, r) - Wp)
print("EP at f=1:", sp.simplify(EP_f1))
print("EP - (target times factor):", sp.simplify(EP_f1/target) if target != 0 else None)
# ---- exact Schwarzschild regression
Ns = (1 - m/r)/(1 + m/r); fs = (1 + m/r)**4
sub = {N: Ns, f: fs, P: 0, rho: 0, Lam: 0}
print("\nexact isotropic Schwarzschild:")
print("  EL_N:", sp.simplify(EN.subs(sub)))
print("  EL_P:", sp.simplify(EP.subs(sub)))
print("  EL_f:", sp.simplify(Ef.subs(sub)))