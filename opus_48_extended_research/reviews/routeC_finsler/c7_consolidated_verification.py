"""Route C / step 7. Consolidated sympy verification of every load-bearing claim. PASS/FAIL."""
import sympy as sp

results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ")+name)

a, a0, gbar, GM, r = sp.symbols('a a_0 g_bar GM r', positive=True)

# 1. mu_fw limits
x = sp.symbols('x', positive=True)
mu = (sp.sqrt(1+4*x**2)-1)/(2*x)
check("mu_fw(inf)=1 (Newtonian)", sp.limit(mu,x,sp.oo)==1)
check("mu_fw(0+)~x (deep-MOND)", sp.series(mu,x,0,2).removeO()==x)

# 2. MI law inverts to g_obs exactly
mi = a*mu.subs(x,a/a0)
sol = sp.solve(sp.Eq(sp.simplify(mi),gbar),a)
check("a*mu_fw(a/a0)=g_bar => a=sqrt(g_bar^2+g_bar a0)",
      any(sp.simplify(s-sp.sqrt(gbar**2+gbar*a0))==0 for s in sol))

# 3. T(a) primitive: dT/da = a*mu_fw exactly
T = -a*a0/2 + a*sp.sqrt(4*a**2+a0**2)/4 + a0**2*sp.asinh(2*a/a0)/8
check("dT/da = a*mu_fw(a/a0)", sp.simplify(sp.diff(T,a)-mi)==0)

# 4. T'' != 0 everywhere (nondegenerate => Ostrogradski applies)
Tpp = sp.simplify(sp.diff(T,a,2))
check("T''(a)=2a/sqrt(4a^2+a0^2) > 0 for a>0 (nondegenerate)",
      sp.simplify(Tpp - 2*a/sp.sqrt(4*a**2+a0**2))==0)

# 5. G(a)=a*mu_fw not polynomial in a (=> no linear-in-a / 2nd-order local Lagrangian)
G = -a0/2 + sp.sqrt(4*a**2+a0**2)/2
check("a*mu_fw(a/a0) NOT polynomial in a", not G.is_polynomial(a))

# 6. Chang-Li Finsler-MOND law == framework g_obs (the MG sibling degeneracy)
a_CL = (GM/r**2)*sp.sqrt((r**2+GM/a0)/(GM/a0))
gb = GM/r**2
check("Chang-Li Finsler law == sqrt(g_bar^2+g_bar a0)",
      sp.simplify(a_CL - sp.sqrt(gb**2+gb*a0))==0)

# 7. limits of g_obs
go = sp.sqrt(gbar**2+gbar*a0)
check("g_obs->g_bar as a0->0 (Newtonian)", sp.limit(go,a0,0)==gbar)
check("g_obs->sqrt(g_bar a0) as g_bar->0 (deep-MOND/BTFR)",
      sp.limit(go/sp.sqrt(gbar*a0),gbar,0)==1)

print("\n"+"="*50)
n_pass = sum(p for _,p in results); n = len(results)
print(f"{n_pass}/{n} checks PASS")
print("ALL PASS" if n_pass==n else "SOME FAIL -- review")
