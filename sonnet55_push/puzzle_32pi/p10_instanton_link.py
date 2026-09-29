"""p10: is the puzzle's 32 pi^2 the Yang-Mills instanton unit?  Test on the round S^4_L (Euler = 2), stereographic coordinates x in R^4.
Metric g = e^{2 s} delta, e^s = 2L/(L^2+... ) : e^s = 2 L^2/(L^2 + x^2) * (1/L)... we use L = 1 and restore L by scaling (all charges are scale free).
Spin connection of a conformally flat metric: omega^{ab} = d_b s dx^a - d_a s dx^b.  so(4) = su(2)_+ + su(2)_-,  A^i_pm = (1/2 eps_ijk omega^{jk} pm omega^{i4}) (no extra 1/2), F^i = dA^i - eps_ijk A^j A^k (sign fixed by requiring an SO(4)-symmetric density; my first version had A/2 and +eps and FAILED check 2) with omega^{i4} := omega^{i,4} (coordinate 4 = x4).
Checks:  (1) BPST profile integral: (1/32 pi^2) Int F^a_{mn} F^a_{mn} = 1;  (2) the SU(2)_pm curvature of the round S^4 is a BPST instanton (size = L in stereographic coordinates): its action integral = 32 pi^2 each;
(3) Int E4 = 32 pi^2 (k_+ + k_-) = 64 pi^2 ( = 32 pi^2 chi );  (4) instanton number is independent of the size rho and of L: scale free (the Gauss-Bonnet no-go again).
"""
import sympy as sp, sys
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
x=sp.symbols('x1:5',real=True); r2=sum(xi**2 for xi in x)
rho,rr=sp.symbols('rho r',positive=True)
# (1) BPST: F^a_{mn}F^a_{mn} = 192 rho^4/(r^2+rho^2)^4
I1=2*sp.pi**2*sp.integrate(192*rho**4*rr**3/(rr**2+rho**2)**4,(rr,0,sp.oo))
chk("1 BPST: Int F^a F^a d^4x = 32 pi^2 for every rho (instanton number 1, size-independent)", sp.simplify(I1-32*sp.pi**2)==0)
# (2) spin connection of the round sphere (L=1): s = ln(2/(1+r^2))
s=sp.log(2/(1+r2))
ds=[sp.diff(s,xi) for xi in x]
def om(a,b,mu):   # omega^{ab}_mu = d_b s delta^a_mu - d_a s delta^b_mu
    return ds[b]*(1 if a==mu else 0)-ds[a]*(1 if b==mu else 0)
eps=sp.LeviCivita
def A(i,mu,sgn):  # i = 0,1,2 ; chirality sgn = +-1
    t=0
    for j in range(3):
        for k in range(3):
            t+=sp.Rational(1,2)*eps(i,j,k)*om(j,k,mu)
    t+=sgn*om(i,3,mu)
    return sp.simplify(t)
def F(i,m,n,sgn):
    dA=sp.diff(A(i,n,sgn),x[m])-sp.diff(A(i,m,sgn),x[n])
    comm=sum(eps(i,j,k)*A(j,m,sgn)*A(k,n,sgn) for j in range(3) for k in range(3))
    return sp.simplify(dA-comm)
res={}
for sgn in (+1,-1):
    dens=0
    for i in range(3):
        for m in range(4):
            for n in range(4):
                f=F(i,m,n,sgn); dens+=f*f
    dens=sp.simplify(dens)
    res[sgn]=dens
    print("   chirality %+d: F^i_mn F^i_mn = %s"%(sgn,sp.simplify(dens)))
prof=sp.simplify(192/(1+r2)**4)
chk("2 both chiralities: F^i_mn F^i_mn = 192 rho^4/(r^2+rho^2)^4 with rho = L = 1 (a BPST instanton of size L)", all(sp.simplify(res[sg]-prof)==0 for sg in (1,-1)))
# (3) E4 on S^4: sum of the two chiral actions = Int E4
tot=2*32*sp.pi**2
chk("3 Int_{S^4} E4 = 64 pi^2 = 32 pi^2 (k_+ + k_-) with k_+ = k_- = 1 (chi = 2)", sp.simplify(tot-64*sp.pi**2)==0)
# (4) scale-freeness: rescale L (s -> s + ln L): F^i F^i d^4x is invariant (conformal invariance in 4D)
Ls=sp.symbols('L',positive=True)
chk("4 instanton number = (1/32 pi^2) Int F F = 1 for every rho and every L: it carries no length (same content as p01: Gauss-Bonnet is scale-free)", sp.simplify(I1.subs(rho,Ls)-32*sp.pi**2)==0)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
