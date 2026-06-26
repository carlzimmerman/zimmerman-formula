import sympy as sp
import mpmath as mp
mp.mp.dps = 40

# ============================================================
# Minimize natural S3-invariant potentials and read off r = sqrt(2)*d/s at the VEV.
# We work in the (s, d) reduced coordinates by S3 symmetry: a generic S3 VEV can be
# rotated to the "1+2" form. But to see ALL stationary points we minimize over full phi.
# We test a LADDER of increasingly general natural potentials.
# ============================================================
p1,p2,p3 = sp.symbols('p1 p2 p3', real=True)
phi = sp.Matrix([p1,p2,p3])
e1 = p1+p2+p3
q  = p1**2+p2**2+p3**2
c  = p1**3+p2**3+p3**3
t  = p1*p2*p3

def r_of(sol):
    # sol is a dict {p1:..,p2:..,p3:..}; compute r
    v = sp.Matrix([sol[p1],sol[p2],sol[p3]])
    s = (v[0]+v[1]+v[2])/sp.sqrt(3)
    if s == 0:
        return sp.oo
    d2 = sp.simplify(v.dot(v) - s**2)
    return sp.simplify(sp.sqrt(2*d2/s**2))

# --------- Potential A: pure O(3)-symmetric Mexican hat (NO S3-breaking beyond singlet)
# V = -mu^2 |phi|^2 + lam |phi|^4 . Minimum is a SPHERE |phi|=const -> r CONTINUOUS (any).
print("=== A: O(3) Mexican hat V=-mu^2 q + lam q^2 ===")
print("  Minimum |phi|^2 = mu^2/(2 lam): a 2-sphere. r is UNCONSTRAINED (any value 0..inf).")
print("  -> r=sqrt2 NOT selected; flat direction. NULL.\n")

# --------- Potential B: standard S3 doublet+singlet renormalizable potential
# The canonical A4/S3 flavon potential. Use invariants e1, q, c, t.
# V = m1 e1^2 + m2 q + g e1 q + h c + k t + l1 q^2 + l2 e1^4 + ...
# Minimize a representative natural choice and scan.
print("=== B: S3 renormalizable V (e1,q,c,t,quartics) — find stationary VEVs ===")
mq, lqq, hc, kt = sp.symbols('mq lqq hc kt', real=True)
# A clean, natural Z3/S3 potential with a cubic that prefers an aligned direction:
V = -mq*q + lqq*q**2 + hc*c + kt*t
gradV = [sp.diff(V,v) for v in (p1,p2,p3)]
# Solve stationarity for representative couplings (set scale mq=1,lqq=1; scan hc,kt)
import itertools
print("  Scanning cubic couplings (hc,kt); reporting r at real stationary points with s!=0:")
seen=set()
for hcv in [sp.Integer(0), sp.Rational(1,2), sp.Integer(1), sp.Integer(2), -sp.Integer(1)]:
    for ktv in [sp.Integer(0), sp.Integer(1), sp.Integer(3), -sp.Integer(2)]:
        Vs = V.subs({mq:1,lqq:1,hc:hcv,kt:ktv})
        g = [sp.diff(Vs,v) for v in (p1,p2,p3)]
        try:
            sols = sp.solve(g,(p1,p2,p3),dict=True)
        except Exception as e:
            continue
        for sol in sols:
            if not all(v in sol for v in (p1,p2,p3)):
                continue
            try:
                vals=[complex(sol[p1]),complex(sol[p2]),complex(sol[p3])]
            except Exception:
                continue
            if any(abs(z.imag)>1e-9 for z in vals): 
                continue
            if all(abs(z)<1e-12 for z in vals):
                continue
            rr = r_of({p1:sp.nsimplify(vals[0].real),p2:sp.nsimplify(vals[1].real),p3:sp.nsimplify(vals[2].real)})
            try: rv=float(rr)
            except: rv=None
            key=(hcv,ktv,None if rv is None else round(rv,4))
            if key in seen: continue
            seen.add(key)
            print(f"   hc={hcv} kt={ktv}: VEV~{[round(z.real,4) for z in vals]}  r={None if rv is None else round(rv,5)}")
print()
print("sqrt2 =", float(sp.sqrt(2)))
