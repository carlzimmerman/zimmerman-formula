import sympy as sp
mp_dps=40
p1,p2,p3 = sp.symbols('p1 p2 p3', real=True)

def r_exact(v):
    v=sp.Matrix(v)
    s=(v[0]+v[1]+v[2])/sp.sqrt(3)
    if sp.simplify(s)==0: return sp.oo
    d2=sp.simplify(v.dot(v)-s**2)
    return sp.simplify(sp.sqrt(2*d2/s**2))

print("=== The natural S3 symmetry-breaking VEV alignments (residual subgroups) ===")
aligns = {
 "(1,1,1) democratic, S3 unbroken":      (1,1,1),
 "(1,1,-1)":                              (1,1,-1),
 "(0,1,1) two-equal, S2 residual":        (0,1,1),
 "(0,0,1) single, S2 residual":           (0,0,1),
 "(1,1,0)":                               (1,1,0),
 "(2,-1,-1) doublet pure (s=0)":          (2,-1,-1),
 "(1,-1,0) doublet pure (s=0)":           (1,-1,0),
 "(1,1,-2)":                              (1,1,-2),
}
for name,v in aligns.items():
    rr=r_exact(v)
    Q = sp.Rational(1,3)+rr**2/6 if rr!=sp.oo else sp.oo
    print(f"  {name:42s} r={str(rr):10s}  Q={Q}")

print()
print("sqrt2 =", float(sp.sqrt(2)), "  -- which alignment gives r=sqrt2 (i.e. d=s)?")
# r=sqrt2 <=> d^2=s^2 <=> doublet magnitude == singlet magnitude.
# Solve for a VEV of form (a,a,b) (S2-symmetric, the generic 1+2 breaking) what ratio gives r=sqrt2
a,b=sp.symbols('a b',real=True)
v=sp.Matrix([a,a,b])
s=(2*a+b)/sp.sqrt(3); d2=v.dot(v)-s**2
cond = sp.simplify(sp.Eq(2*d2/s**2, 2))   # r^2=2
sol=sp.solve(cond,b)
print("  For VEV (a,a,b): r=sqrt2 requires b =", sol, " (in units of a)")
for bs in sol:
    print("    -> VEV (1,1,%s); check r="%bs, r_exact([1,1,bs]))
