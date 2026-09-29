"""p09: vacuum self-consistency route.  Suppose Lambda is NOT independent: the dark-energy density is the vacuum value of the a0-sector's own
potential.  Action (G = c = 1):   S = (1/16 pi) Int sqrt(-g) [ R - 2 a0^2 U(phi) + kinetic(phi) ],   the MOND normalisation a0^2/(8 pi G) (Poisson's 4 pi G).
On shell at a stationary point phi_v of U in a constant-field vacuum:  Lambda_eff = a0^2 U(phi_v),  rho = Lambda_eff/(8 pi) = a0^2 U_v/(8 pi).
Puzzle:  G rho = 4 a0^2  <=>  U_v = 32 pi.
Checks: (1) the on-shell identity (Friedmann + scalar eq);  (2) U_v = 32 pi is the exact self-consistency condition;
(3) for potentials with algebraic coefficients the stationary value is algebraic (minimal polynomials), 32 pi is not (integer-relation search, controls);
(4) where a pi CAN enter: a Gaussian filter / heat-kernel normalisation (4 pi b)^(-3/2) (the repo's S_h = exp(b Lap)) -- so the no-go is scoped to LOCAL algebraic potentials.
"""
import sympy as sp, mpmath as mp, sys
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)

# (1) FRW with constant scalar at a stationary point of U
phi=sp.symbols('phi'); a0=sp.symbols('a0',positive=True)
U=sp.Function('U')
Lam_eff=a0**2*U(phi)
rho=Lam_eff/(8*sp.pi)
H2=sp.Rational(8,3)*sp.pi*rho
chk("1 constant-field vacuum: H^2 = Lambda_eff/3 with Lambda_eff = a0^2 U_v", sp.simplify(H2-Lam_eff/3)==0)
# (2) self-consistency: G rho = 4 a0^2
Uv=sp.symbols('U_v',positive=True)
sol=sp.solve(sp.Eq(a0**2*Uv/(8*sp.pi),4*a0**2),Uv)
chk("2 G rho = 4 a0^2  <=>  U_v = 32 pi", sol==[32*sp.pi])

# (3) algebraic potentials -> algebraic vacuum values
u=sp.symbols('u',real=True)
tests={"quartic  u^4/4 - u^2/2 + 3/5 (min at u^2=1)":sp.Rational(1,4)*u**4-u**2/2+sp.Rational(3,5),
       "rational (u^2+1)^2/(u^2+3) - 2":(u**2+1)**2/(u**2+3)-2,
       "sextic   u^6 - 3u^4 + 2u^2 + 7/3":u**6-3*u**4+2*u**2+sp.Rational(7,3)}
allalg=True
for nm,Ux in tests.items():
    crit=[c for c in sp.solve(sp.diff(Ux,u),u) if c.is_real]
    for c in crit:
        v=sp.nsimplify(sp.simplify(Ux.subs(u,c)))
        try:
            mpoly=sp.minimal_polynomial(v,sp.Symbol('x'))
            alg=True
        except Exception as ex:
            alg=False
        allalg=allalg and alg
        print("   %-46s stationary U_v = %s  (algebraic, degree %d)"%(nm,sp.simplify(v),sp.degree(mpoly,sp.Symbol('x')) if alg else -1))
chk("3a stationary values of algebraic-coefficient potentials are algebraic numbers", allalg)
mp.mp.dps=60
tgt=32*mp.pi
found=None
for d in range(1,9):
    rel=mp.findpoly(tgt,d,maxcoeff=10**5,maxsteps=100000)
    if rel: found=(d,rel); break
chk("3b integer-relation search finds no polynomial of degree <= 8, coefficients <= 1e5, with root 32 pi (evidence; transcendence of pi is Lindemann 1882)", found is None)
ctrl=mp.findpoly(mp.sqrt(2)*3+1,2,maxcoeff=10**3)
chk("3c control: the same search finds the minimal polynomial of 3 sqrt2 + 1 (degree 2)", ctrl is not None)

# (4) where a pi can enter: heat-kernel filter normalisation
b,k,r=sp.symbols('b k r',positive=True)
ker=sp.integrate(sp.exp(-b*k**2)*k**2*sp.sin(k*r)/(k*r),(k,0,sp.oo))
gauss=sp.integrate(sp.exp(-r**2/(4*b))*r**2,(r,0,sp.oo))*4*sp.pi/(4*sp.pi*b)**sp.Rational(3,2)
chk("4 heat kernel exp(b Lap) has unit-normalised kernel (4 pi b)^(-3/2) exp(-r^2/4b): pi enters through a Gaussian integral (nonlocal filter), not through a local potential", sp.simplify(gauss-1)==0)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
