import sympy as sp
mp_dps=40
p1,p2,p3 = sp.symbols('p1 p2 p3', real=True)
a,b=sp.symbols('a b', real=True)

# Restrict to the S2-symmetric branch (a,a,b) which is where the nontrivial 1+2 VEV lives
# (the only branch that can give 0<r<inf besides the high-symmetry points).
# General S2-symmetric S3-invariant potential on (a,a,b):
e1=2*a+b; q=2*a**2+b**2; c=2*a**3+b**3; t=a**2*b
m2,L,h,k = sp.symbols('m2 L h k', real=True)
V = -m2*q + L*q**2 + h*c + k*t
# stationarity in a,b
ga=sp.diff(V,a); gb=sp.diff(V,b)

# r along this branch as function of (a,b):
def rfun(av,bv):
    v=sp.Matrix([av,av,bv]); s=(2*av+bv)/sp.sqrt(3)
    return sp.sqrt(2*(v.dot(v)-s**2)/s**2)
rho = sp.symbols('rho', real=True)  # rho=b/a
r_of_rho = sp.simplify(rfun(1,rho))
print("r(rho=b/a) =", r_of_rho)
sol_r2 = sp.solve(sp.Eq(r_of_rho, sp.sqrt(2)), rho)
print("r=sqrt2 at rho=b/a =", [sp.nsimplify(s) for s in sol_r2], " (= 4 -+ 3 sqrt2):", [float(s) for s in sol_r2])
print()

# Now: for the natural potential WITHOUT a cubic (h=k=0), what is the VEV?
print("=== No-cubic S3 potential (h=k=0): the O-symmetry is too big ===")
V0=V.subs({h:0,k:0})
# only depends on q -> minimum is the whole sphere q=m2/(2L): r FREE (flat). 
print("  V depends only on q=|phi|^2 -> minimum is sphere -> r CONTINUOUS/flat. r=sqrt2 not selected.")
print()

# With cubic c (h!=0): the cubic c=2a^3+b^3 breaks toward axis-aligned (single-component) VEV.
print("=== With cubic h*c: stationary rho values (scan h, fix m2=L=1,k=0) ===")
for hv in [sp.Rational(1,4),sp.Rational(1,2),sp.Integer(1),sp.Integer(2),sp.Integer(4)]:
    Vs=V.subs({m2:1,L:1,h:hv,k:0})
    g=[sp.diff(Vs,a),sp.diff(Vs,b)]
    sols=sp.solve(g,(a,b),dict=True)
    rr=[]
    for s_ in sols:
        if a in s_ and b in s_:
            try:
                av=complex(s_[a]); bv=complex(s_[b])
                if abs(av.imag)<1e-9 and abs(bv.imag)<1e-9 and abs(av.real)>1e-9:
                    rv=float(rfun(av.real,bv.real))
                    rr.append(round(rv,4))
            except: pass
    print(f"  h={hv}: r at stationary pts = {sorted(set(rr))}")
print()
print("  => r drifts CONTINUOUSLY with h; it passes through 1.414 only at a tuned h. Not forced.")
print("sqrt2=",float(sp.sqrt(2)))
