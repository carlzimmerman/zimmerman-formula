import sympy as sp

u0, u1 = sp.symbols('u0 u1', real=True)

# static-NR invariant forms (a=|grad dPhi|^2 coeff, b=|grad dPsi|^2 coeff, x=cross), from probe A:
# T1(3,7,0) T2(1,1,-2) T3(1,9,-6) T4(-1,-1,0) T5(-1,-3,4)
T = {1:(3,7,0), 2:(1,1,-2), 3:(1,9,-6), 4:(-1,-1,0), 5:(-1,-3,4)}

# ghost-free 2-dim subspace parameterization claimed: (c1..c5)=(-u0,-u1/2,-u1/2,u0,u1)
c = {1:-u0, 2:-u1/sp.Integer(2), 3:-u1/sp.Integer(2), 4:u0, 5:u1}

a = sp.expand(sum(c[i]*T[i][0] for i in range(1,6)))
b = sp.expand(sum(c[i]*T[i][1] for i in range(1,6)))
x = sp.expand(sum(c[i]*T[i][2] for i in range(1,6)))
print("a (MOND accel scalar) =", a, "  claimed -4u0-2u1 ->", sp.simplify(a-(-4*u0-2*u1))==0)
print("b (lensing source)    =", b, "  claimed -8u0-8u1 ->", sp.simplify(b-(-8*u0-8*u1))==0)
print("x (cross)             =", x, "  claimed  8u1    ->", sp.simplify(x-(8*u1))==0)

# MOND-alive direction T4-T1 : c=(-1,0,0,1,0) -> (u0,u1)=(1,0)
print("\nMOND direction (u0,u1)=(1,0):  a =", a.subs({u0:1,u1:0}), " b =", b.subs({u0:1,u1:0}), " (claimed a=-4,b=-8)")

# a=0 (no-MOND) locus
sol = sp.solve(sp.Eq(a,0), u1)[0]
print("\na=0 locus: u1 =", sol, " -> coeff vector:", [sp.simplify(c[i].subs(u1,sol)) for i in range(1,6)], " (claimed u0*(-1,1,1,1,-2))")
bx = (sp.simplify(b.subs(u1,sol)), sp.simplify(x.subs(u1,sol)))
print("a=0 static form (b,x) =", bx, " (claimed (8u0,-16u0)); ratio to T4-T5=(2,-4)? ->",
      sp.simplify(bx[0]/2 - bx[1]/(-4))==0)
