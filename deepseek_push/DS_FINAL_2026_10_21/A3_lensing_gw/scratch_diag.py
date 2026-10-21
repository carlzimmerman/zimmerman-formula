import sympy as s, time
r = s.symbols('r', positive=True)
K, beta, eta, gamma, a0 = s.symbols('K beta eta gamma a0', positive=True)
NV, NP, NPP, FV, FP, FPP = s.symbols('NV NP NPP FV FP FPP', positive=True)
PV, PP, PPP = s.symbols('PV PP PPP', positive=True)
rho = s.Function('rho')(r); rho1 = s.symbols('rho1', positive=True)
sq = s.sqrt(FV)
R3 = -2*FPP/FV**2 + s.Rational(3,2)*FP**2/FV**3 - 4*FP/(r*FV**2)
u = K*PV/sq
W = a0**2/K*(-u/a0 - s.log(1-u/a0))
d = PP/FV + 2*PV/(r*FV) + FP*PV/(2*FV**2)
Lag = 4*s.pi*r**2*(NV*FV**s.Rational(3,2)*(R3/(4*K) - W - (gamma/2)*d**2) + sq*PV*NP - rho*NV)
def Dt(e):
    out = s.diff(e, r)
    for v, dv, ddv in ((NV,NP,NPP),(FV,FP,FPP),(PV,PP,PPP)):
        out += s.diff(e,v)*dv + s.diff(e,ddv)*ddv
    return out
EN = s.cancel((Dt(s.diff(Lag,NP)) - s.diff(Lag,NV))/(4*s.pi*r**2))
EF = s.cancel((s.diff(Lag,FV) - Dt(s.diff(Lag,FP)) + Dt(Dt(s.diff(Lag,FPP))))/(4*s.pi*r**2))
EP = s.cancel((s.diff(Lag,PV) - Dt(s.diff(Lag,PP)))/(4*s.pi*r**2))
m = s.symbols('m', positive=True)
Nsch = (1-m/r)/(1+m/r); fsch = (1+m/r)**4
sub_schw = {PV:0,PP:0,PPP:0,rho:0,NV:Nsch,NP:s.diff(Nsch,r),NPP:s.diff(Nsch,r,2),
            FV:fsch,FP:s.diff(fsch,r),FPP:s.diff(fsch,r,2)}
for nm, E in (('EN',EN),('EF',EF),('EP',EP)):
    res = E.subs(sub_schw)
    num, den = s.fraction(s.cancel(res))
    print(nm, 'simplify:', s.simplify(res) == 0, ' numerator:', s.simplify(num) == 0)
    for pt in ({r:s.Rational(7,3), m:s.Rational(2,5), K:s.Rational(3,7)},
               {r:s.Integer(11), m:s.Integer(3), K:s.Rational(1,2)}):
        try:
            print('   pt ->', s.nsimplify(s.cancel(res.subs(pt))), end='')
        except Exception as ex:
            print('   pt fail', ex, end='')
    print()
# first order
n1,n2 = s.Function('n1')(r), s.Function('n2')(r)
h1,h2 = s.Function('h1')(r), s.Function('h2')(r)
p1,p2 = s.Function('p1')(r), s.Function('p2')(r)
eps = s.symbols('eps', positive=True)
SUB = {}
for (v,dv,ddv),(a_,b_,bg) in (((NV,NP,NPP),(n1,n2,1)),((FV,FP,FPP),(h1,h2,1)),((PV,PP,PPP),(p1,p2,0))):
    SUB[v] = bg + eps*a_ + eps**2*b_
    SUB[dv] = eps*s.diff(a_,r) + eps**2*s.diff(b_,r)
    SUB[ddv] = eps*s.diff(a_,r,2) + eps**2*s.diff(b_,r,2)
SUB[rho] = eps*rho1
def order(E,k):
    ser = s.series(s.expand(E.subs(SUB)), eps, 0, 3).removeO()
    return s.expand(s.expand(ser).coeff(eps,k))
E1 = {nm:order(E,1) for nm,E in (('N',EN),('f',EF),('P',EP))}
E2 = {nm:order(E,2) for nm,E in (('N',EN),('f',EF),('P',EP))}
lap = lambda g_: s.diff(g_,r,2) + 2*s.diff(g_,r)/r
print('E1N*2 =', s.expand(2*E1['N']))
print('cand  =', s.expand(2*K*(rho1 + s.diff(p1,r) + 2*p1/r) + lap(h1)))
print('E1f*4K =', s.expand(4*K*E1['f']))
print('E1P*K =', s.expand(E1['P']*K))
Ef2 = s.expand(4*K*E2['f'])
zero1 = {n1:s.S.Zero,h1:s.S.Zero,p1:s.S.Zero}
lin2 = s.expand(s.expand(Ef2.subs(zero1)).doit())
quad = s.expand(s.expand(Ef2-lin2).doit())
print('lin2 =', lin2)
print('quad_gr =', s.expand(quad.subs({p1:0,gamma:0})))
print('quad_p  =', s.expand(s.expand(quad - quad.subs({p1:0,gamma:0}))))
