#!/usr/bin/env python3
"""Exact local principal-action audit. No metric identification or global solution."""
import sympy as S

e, Q, a, b, st, sx, pt, px = S.symbols('e Q a b st sx pt px', real=True)
P1, P2, W0, W1, W2 = S.symbols('P_X P_XX W W_Y W_YY', real=True)
checks = []
def eq(name, lhs, rhs=0):
    residual = S.factor(S.simplify(lhs-rhs))
    assert residual == 0, (name, residual)
    checks.append(name)
    print('PASS', name)

# Frozen Minkowski background tau=t, chi=Qt+a*x+b*y.
# Wave gradients lie along x. This is general after spatial rotation.
clock_s = S.sqrt((1+e*pt)**2-e**2*px**2)
X = (Q+e*st)**2-(a+e*sx)**2-b**2
Y = -X+((1+e*pt)*(Q+e*st)-e*px*(a+e*sx))**2/clock_s**2
def order(expr, n):
    return S.simplify(S.diff(expr,e,n).subs(e,0)/S.factorial(n))
x1,x2,y1,y2 = order(X,1),order(X,2),order(Y,1),order(Y,2)
eq('X first variation', x1, 2*(Q*st-a*sx))
eq('X second coefficient', x2, st**2-sx**2)
eq('Y first variation', y1, 2*a*(sx-Q*px))
L2 = S.expand(P1*x2+P2*x1**2/2+W1*y2+W2*y1**2/2+pt*W1*y1-W0*px**2/2)
# st*px and pt*sx have equal integrals for constant coefficients;
# their difference is a spacetime divergence, hence no clock kinetic term.
boundary = 2*W1*a*(pt*sx-st*px)
K=P1+2*Q**2*P2
A=-P1+W1+2*(P2+W2)*a**2
T=W1+2*W2*a**2
D=Q**2*W1-W0/2+(W1+2*Q**2*W2)*a**2
target=K*st**2-4*Q*P2*a*st*sx+A*sx**2-2*Q*T*sx*px+D*px**2
eq('quadratic action including clock derived from exact invariants',L2-boundary,target)
eq('clock has no quadratic time kinetic coefficient',S.diff(L2,pt,2))
Aeff=S.factor(A-Q**2*T**2/D)
eq('clock Schur complement',target.subs(px,Q*T*sx/D),K*st**2-4*Q*P2*a*st*sx+Aeff*sx**2)

U,d,ell,m0,Yv=S.symbols('U d ell m0 Y',positive=True)
Xv=S.symbols('X',real=True)
P=-U*S.log((U-2*d*Xv)/m0)/2
W=U+2*d*ell*(S.sqrt(1+Yv/ell)-1)
p1=S.diff(P,Xv).subs(Xv,Q**2-Yv)
p2=S.diff(P,Xv,2).subs(Xv,Q**2-Yv)
w1,w2=S.diff(W,Yv),S.diff(W,Yv,2)
family={P1:p1,P2:p2,W0:W,W1:w1,W2:w2}
F=P.subs(Xv,-Yv)+W
mu=2*S.diff(F,Yv)
C=-mu
eq('L205 algebra correct but canonical stiffness opposite',C,2*(p1.subs(Q,0)-w1))
eq('zero-gradient response cancels',mu.subs(Yv,0))
eq('generic leading L205 coefficient',S.diff(mu,Yv).subs(Yv,0),4*d**2/U-d/ell)
eq('tuned leading quartic-gradient coefficient',S.diff(mu,Yv,2).subs({Yv:0,U:4*d*ell})/2,d/(4*ell**2))
eq('high-gradient coefficient tends to zero',S.limit(mu,Yv,S.oo))
eq('high-gradient leading response',S.limit(S.sqrt(Yv)*mu,Yv,S.oo),2*d*S.sqrt(ell))
longitudinal=mu+2*Yv*S.diff(mu,Yv)
eq('high-gradient longitudinal leading response',S.limit(Yv*longitudinal,Yv,S.oo),U)
eq('Q=0 clock/scalar mixing vanishes',(-2*Q*T).subs(Q,0))
eq('timelike clock-reduced Y=0 stiffness vanishes',Aeff.subs(a,0).subs(family).subs(Yv,0))
eq('timelike fixed-clock Y=0 stiffness nonzero',(-2*A).subs(a,0).subs(family).subs(Yv,0),4*d**2*Q**2/(U-2*d*Q**2))
eq('clock transverse Schur form',Aeff.subs(a,0),-P1+W1*W0/(W0-2*Q**2*W1))
for label,vals,expected_sign in [
    ('L205 purported healthy point actually unstable',{U:1,d:1,ell:1,Yv:S.Rational(1,100)},-1),
    ('reversed sign supplies local spatial health',{U:10,d:1,ell:1,Yv:S.Rational(1,100)},1),
]:
    transverse=S.N(C.subs(vals),30)
    radial=S.N((-longitudinal).subs(vals),30)
    assert expected_sign*transverse>0 and expected_sign*radial>0
    print('PASS',label, 'C_T=',transverse,'C_L=',radial)
    checks.append(label)
print('DERIVED_L2_MOD_BOUNDARY =',target)
print('CLOCK_REDUCED_SPATIAL_A =',Aeff)
print('ALL',len(checks),'CHECKS PASSED')
