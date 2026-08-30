import sympy as sp
u0,u1=sp.symbols('u0 u1')
# ghost-free (bg-indep, lapse-velocity-free) subspace element in (T1..T5) basis:
c=sp.Matrix([-u0,-u1/2,-u1/2,u0,u1])
# static-NR (a,b,x) coefficient rows from Part 2:
A=sp.Matrix([3,1,1,-1,-1]); B=sp.Matrix([7,1,9,-1,-3]); Xc=sp.Matrix([0,-2,-6,0,4])
a=(A.T*c)[0]; b=(B.T*c)[0]; x=(Xc.T*c)[0]
print("ghost-free subspace static-NR form: a=",sp.expand(a)," b=",sp.expand(b)," x=",sp.expand(x))
# the a=0 sub-line:
sol=sp.solve(sp.Eq(a,0),u1)[0]; print("a=0  <=>  u1 =",sol)
cline=c.subs(u1,sol); print("a=0 coeff vector (u0=1):",list(cline.subs(u0,1)))
formline=(sp.expand(a.subs(u1,sol)),sp.expand(b.subs(u1,sol)),sp.expand(x.subs(u1,sol)))
print("a=0 line static-NR form (a,b,x):",[f.subs(u0,1) for f in formline]," vs EH/GR (0,2,-4) -> proportional?",
      sp.simplify(formline[1].subs(u0,1)/2 - formline[2].subs(u0,1)/(-4))==0)
# a MOND direction (a!=0), e.g. u0=1,u1=0:
print("\nsample MOND direction u0=1,u1=0: coeff vector",list(c.subs({u0:1,u1:0})),
      " form (a,b,x)=",(sp.Rational(a.subs({u0:1,u1:0})),sp.Rational(b.subs({u0:1,u1:0})),sp.Rational(x.subs({u0:1,u1:0}))))
print("  -> a!=0 => carries the MOND |grad dPhi|^2 acceleration scalar, and is OFF the f(Q)/EH line.")
