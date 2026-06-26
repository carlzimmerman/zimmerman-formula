import sympy as sp
import mpmath as mp
mp.mp.dps = 40

# ============================================================
# GEOMETRY SETUP (no 2/3 inputted; just establishing the map r <-> config)
# Koide Q = (sum m)/(sum sqrt m)^2.  Let x_i = sqrt(m_i) >= 0.
# Q = (sum x^2)/(sum x)^2 = 1/(3 cos^2 theta) where theta = angle of x-vector to (1,1,1).
# Brannen circulant: x_k = M(1 + r cos(phi + 2pi k/3)).
# Identity (phase-independent): Q = 1/3 + r^2/6.
# So Q=2/3 <=> r=sqrt2 <=> cos^2(theta)= 1/(3*(2/3)) = 1/2  (45 deg).
# We DO NOT assume 2/3. We just track WHERE a potential's minimum lands in r.
# ============================================================
r, phi, M, k = sp.symbols('r phi M k', real=True)
x = [M*(1 + r*sp.cos(phi + 2*sp.pi*k/3)) for k in range(3)]
p1 = sum(x)                       # sum x
p2 = sum([xi**2 for xi in x])     # sum x^2
Q = sp.simplify(p2/p1**2)
print("Q(r,phi) simplified =", Q)
# verify phase independence
for pv in [0, sp.Rational(3,10), 1, 2]:
    print("  phi=",pv," Q=", sp.simplify(Q.subs(phi,pv)))

Q0 = sp.simplify(Q.subs(phi,0))
print("Q = 1/3 + r^2/6 ? ", sp.simplify(Q0 - (sp.Rational(1,3)+r**2/6)) == 0)

# cos^2 theta to (1,1,1)
xv = sp.Matrix(x).subs(phi,0)
ones = sp.Matrix([1,1,1])
cos2 = sp.simplify((xv.dot(ones))**2/((xv.dot(xv))*(ones.dot(ones))))
print("cos^2(theta) =", cos2)
print("at r=sqrt2: cos2 =", sp.simplify(cos2.subs(r, sp.sqrt(2))), " (=1/2 expect)")
print("Q at r=sqrt2 =", sp.simplify(Q0.subs(r, sp.sqrt(2))))
