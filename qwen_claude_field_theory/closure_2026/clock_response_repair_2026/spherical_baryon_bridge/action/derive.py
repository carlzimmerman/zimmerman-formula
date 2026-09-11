#!/usr/bin/env python3
"""Exact spherical action audit in tau=t; no radial metric gauge is fixed.

Run: python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/
     spherical_baryon_bridge/action/derive.py
Uses exact SymPy rational-function and formal constitutive-jet algebra.
Prints JSON; no data fitting, finite differencing, or files written.
"""
import json
import platform
import time

import sympy as s

started = time.monotonic()
t, r = s.symbols("t r", real=True)
M2, Lambda, gamma = s.symbols("M2 Lambda gamma", real=True)
names = ("N", "v", "A", "R", "c")
jets = {(f, i, j): s.Symbol(f + "t" * i + "r" * j)
        for f in names for i in range(4) for j in range(4-i)}
N, v, A, R, c = (jets[f, 0, 0] for f in names)
Nt, Nr, At, Ar, Rt, Rr, vt, vr, ct, u, ur = (
    jets[f, i, j] for f, i, j in
    [("N",1,0),("N",0,1),("A",1,0),("A",0,1),("R",1,0),
     ("R",0,1),("v",1,0),("v",0,1),("c",1,0),("c",0,1),("c",0,2)])
Q = (ct-v*u)/N
Y = u**2/A**2
X = Q**2-Y
k = (At/A-v*Ar/A-vr)/N
h = (Rt/R-v*Rr/R)/N
D = (ur+(2*Rr/R-Ar/A)*u)/A**2
Yr = 2*u*ur/A**2-2*Ar*u**2/A**3

# Independent constitutive jets implement the exact chain rule for arbitrary
# C^2 P(X,t), W(Y,t), V(t); no polynomial constitutive law is assumed.
P, PX, PXX, Pt, PXt = s.symbols("P P_X P_XX P_t P_Xt")
W, WY, WYY, Wt, WYt = s.symbols("W W_Y W_YY W_t W_Yt")
V, Vt = s.symbols("V V_t")


def partial(expr, z):
    return (s.diff(expr, z) + s.diff(expr, P)*PX*s.diff(X,z)
            + s.diff(expr, PX)*PXX*s.diff(X,z)
            + s.diff(expr, W)*WY*s.diff(Y,z)
            + s.diff(expr, WY)*WYY*s.diff(Y,z))


def total(expr, axis):
    out = s.diff(expr, (t, r)[axis])
    for (f,i,j), z in jets.items():
        successor = (f, i+(axis==0), j+(axis==1))
        if successor in jets:
            out += partial(expr,z)*jets[successor]
        elif z in expr.free_symbols:
            raise ValueError("Insufficient jet order: " + str(z))
    if axis == 0:
        out += (s.diff(expr,P)*Pt+s.diff(expr,PX)*PXt
                +s.diff(expr,W)*Wt+s.diff(expr,WY)*WYt+s.diff(expr,V)*Vt)
    return s.expand(out)


def dt(expr):
    return total(expr,0)


def dr(expr):
    return total(expr,1)


def zero(expr):
    return s.cancel(s.expand(expr)) == 0


checks = {}


def check(name, expr):
    checks[name] = zero(expr)
    if not checks[name]:
        raise AssertionError(name + ": " + str(s.factor(expr)))


def euler(L, f):
    ans = partial(L,jets[f,0,0])
    for i,j in [(1,0),(0,1),(2,0),(1,1),(0,2)]:
        term = partial(L,jets[f,i,j])
        for _ in range(i):
            term = dt(term)
        for _ in range(j):
            term = dr(term)
        ans += (-1)**(i+j)*term
    return s.expand(ans)


B = -s.Rational(2,3)*Q**3*(k+2*h)+2*Q*k*Y+2*Q**2*D+u*Yr/A**2
H = -M2*(2*k*h+h**2+Lambda)+P-V+gamma*B
Lsp = M2*(N*A+N*Rr**2/A+2*Nr*R*Rr/A)
L = Lsp+N*A*R**2*H+A*R**2*W
Hk = -2*M2*h+gamma*(-s.Rational(2,3)*Q**3+2*Q*Y)
Hh = -2*M2*(k+h)-s.Rational(4,3)*gamma*Q**3
HQ = 2*Q*PX+gamma*(-2*Q**2*(k+2*h)+2*k*Y+4*Q*D)
PA, PR, p = R**2*Hk, A*R*Hh, A*R**2*HQ
HA = 2*Y*PX/A+gamma*(-4*Q*k*Y/A-4*Q**2*D/A
          +2*Q**2*Ar*u/A**4-8*u**2*ur/A**5+10*Ar*u**3/A**6)
HAr = -2*gamma*u*(Q**2+Y)/A**3
HR = -4*gamma*Q**2*Rr*u/(A**2*R**2)
HRr = 4*gamma*Q**2*u/(A**2*R)
metric_compact = {
    "N": M2*(A+Rr**2/A-dr(2*R*Rr/A))+A*R**2*(H-k*Hk-h*Hh-Q*HQ),
    "v": A*dr(PA)-Rr*PR-u*p,
    "A": M2*(N-N*Rr**2/A**2-2*Nr*R*Rr/A**2)
         +N*R**2*H+N*A*R**2*HA-(N*k+vr)*PA+R**2*(W-2*Y*WY)
         -dt(PA)-dr(-v*PA+N*A*R**2*HAr),
    "R": 2*M2*Nr*Rr/A+2*N*A*R*H+N*A*R**2*HR-N*h*PR+2*A*R*W
         -dt(PR)-dr(2*M2*(N*Rr+Nr*R)/A-v*PR+N*A*R**2*HRr),
}
j = -v*p+2*N*R**2/A*(u*(-PX+WY/N)+gamma*(2*Q*k*u-2*Q*dr(Q)
                                   -Nr*(Q**2+Y)/N-2*Rr*Y/R))
check("scalar_time_momentum", partial(L,ct)-p)
check("scalar_radial_flux", partial(L,u)-dr(partial(L,ur))-j)
E = {f:euler(L,f) for f in names}
third_jets = {z for (field,i,j),z in jets.items() if i+j == 3}
for field, equation in E.items():
    checks['third_derivatives_cancel_'+field] = not bool(s.cancel(equation).free_symbols & third_jets)
    if not checks['third_derivatives_cancel_'+field]:
        raise AssertionError('uncancelled third derivative in '+field)
for f, compact in metric_compact.items():
    check("unfixed_euler_"+f,E[f]-compact)
check("unfixed_euler_chi_conservation",E["c"]+dt(p)+dr(j))

# Direct divergence definition of the four-dimensional scalar d'Alembertian.
box = (-dt(A*R**2*Q)+dr(A*R**2*v*Q+N*R**2*u/A))/(N*A*R**2)
covp = A*R**2*(2*Q*(PX+gamma*box)+gamma*(dt(X)-v*dr(X))/N)
covj = -v*covp+N*R**2/A*(-2*u*(PX+gamma*box)-gamma*dr(X))+2*R**2*u*WY/A
F = 2*gamma*R**2*Q*u/A
check("covariant_time_current_improvement",p-covp-dr(F))
check("covariant_radial_current_improvement",j-covj+dt(F))

# ADM cubic equality to original gamma X box(chi) with explicit boundary flux.
# The covariant density equals ADM density + dt(Bt) + dr(Br).
Bt = A*R**2*gamma*(-Q**3/s.Integer(3)+Q*Y)
Br = -v*Bt-N*A*R**2*gamma*(Q**2+Y)*u/A**2
check("covariant_cubic_boundary_identity",N*A*R**2*gamma*X*box-N*A*R**2*gamma*B-dt(Bt)-dr(Br))
R3 = 2/R**2*(1-Rr**2/A**2-2*R*jets["R",0,2]/A**2+2*R*Rr*Ar/A**3)
check("einstein_spatial_boundary_identity",M2*N*A*R**2*R3/2-Lsp+dr(2*M2*N*R*Rr/A))

# Independent 2D Christoffel contraction, then the exact spherical warped-
# product scalar curvature; checks the full Einstein ADM boundary signs.
g2 = s.Matrix([[-N**2+A**2*v**2,A**2*v],[A**2*v,A**2]])
gi = s.Matrix([[-1/N**2,v/N**2],[v/N**2,1/A**2-v**2/N**2]])
dd = (dt,dr)
G = {(i,j,l):s.cancel(sum(gi[i,m]*(dd[j](g2[m,l])+dd[l](g2[m,j])
             -dd[m](g2[j,l])) for m in range(2))/2)
     for i in range(2) for j in range(2) for l in range(2)}
Ric2 = {(i,j):s.cancel(sum(dd[m](G[m,i,j])-dd[j](G[m,i,m])
         +sum(G[m,i,j]*G[l,m,l]-G[l,i,m]*G[m,j,l] for l in range(2))
         for m in range(2))) for i in range(2) for j in range(2)}
curv2 = s.cancel(sum(gi[i,j]*Ric2[i,j] for i in range(2) for j in range(2)))
Rvec = (Rt,Rr)
gradR2 = sum(gi[i,j]*Rvec[i]*Rvec[j] for i in range(2) for j in range(2))
boxR = sum(dd[i](N*A*sum(gi[i,j]*Rvec[j] for j in range(2))) for i in range(2))/(N*A)
curv4 = curv2+2/R**2-4*boxR/R-2*gradR2/R**2
Eg_t = M2*A*R**2*(k+2*h)
Eg_r = -v*Eg_t-M2*R**2*Nr/A-2*M2*N*R*Rr/A
check("covariant_einstein_boundary_identity",M2*N*A*R**2*curv4/2
      -(Lsp-M2*N*A*R**2*(2*k*h+h**2))-dt(Eg_t)-dr(Eg_r))


def pullback(expr, replacements, extra=None):
    sub = {z:s.diff(replacements[f],t,i,r,j) for (f,i,j),z in jets.items()}
    if extra:
        sub.update(extra)
    return s.cancel(s.expand(expr.subs(sub, simultaneous=True)))


q = s.symbols("q")
flat = {"N":s.S.One,"v":s.S.Zero,"A":s.S.One,"R":r,"c":q*t}
flat_pressure = P-V+W-M2*Lambda
for f, target in {"N":r**2*(P-V-2*q**2*PX-M2*Lambda),"v":0,
                  "A":r**2*flat_pressure,"R":2*r*flat_pressure,
                  "c":-2*q*r**2*PXt}.items():
    check("Minkowski_"+f,pullback(E[f],flat)-target)
check("Minkowski_time_current",pullback(p,flat)-2*q*r**2*PX)
check("Minkowski_radial_current",pullback(j,flat))

a, n, f = (s.Function(z)(t) for z in ("a","n","f"))
flrw = {"N":n,"v":s.S.Zero,"A":a,"R":a*r,"c":f}
Hb, Qb = s.diff(a,t)/(n*a),s.diff(f,t)/n
rho = 2*Qb**2*PX-P+V-6*gamma*Hb*Qb**3
pressure = P-V+W/n+2*gamma*Qb**2*s.diff(Qb,t)/n
spatial = M2*(2*s.diff(Hb,t)/n+3*Hb**2-Lambda)+pressure
for field,target in {"N":a**3*r**2*(3*M2*Hb**2-M2*Lambda-rho),"v":0,
                      "A":n*a**2*r**2*spatial,"R":2*n*a**2*r*spatial}.items():
    check("FLRW_"+field,pullback(E[field],flrw)-target)
check("FLRW_time_current",pullback(p,flrw)-a**3*r**2*(2*Qb*PX-6*gamma*Hb*Qb**2))
check("FLRW_radial_current",pullback(j,flrw))

# Gamma zero: direct first-derivative P/W variation, with both clock gradients.
L0 = Lsp+N*A*R**2*(-M2*(2*k*h+h**2+Lambda)+P-V)+A*R**2*W
for field in names:
    check("gamma_zero_"+field,E[field].subs(gamma,0)-euler(L0,field))
check("gamma_zero_density",(metric_compact["N"]-M2*(A+Rr**2/A-dr(2*R*Rr/A))
      -A*R**2*(M2*(2*k*h+h**2-Lambda)+P-V-2*Q**2*PX)).subs(gamma,0))

print(json.dumps({"status":"passed", "domain":"exact rational functions and arbitrary smooth constitutive jets",
    "conventions":"signature -+++, Kij=+0.5 Lie_n hij, action density per 4pi, N,A,R nonzero",
    "checks":checks,"check_count":len(checks),"python":platform.python_version(),
    "sympy":s.__version__,"runtime_seconds":round(time.monotonic()-started,3),
    "non_claims":["no full nonspherical DOF count","no exterior/interior solution existence",
                  "no MOND or PPN inference","no cosmological background matching"]},indent=2))
