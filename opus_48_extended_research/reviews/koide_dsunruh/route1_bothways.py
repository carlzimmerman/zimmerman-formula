import sympy as sp
mp_dps=40
a,b = sp.symbols('a b', real=True)
rho = sp.symbols('rho', real=True)

# ---- BOTH-WAYS STEELMAN 1: is d=s (equal split, r=sqrt2) an EXTREMUM of any natural
# ratio-invariant built WITHOUT 2/3?  The candidate "energy" functions:
#   f1 = d^2/s^2  (doublet/singlet power ratio)  -> monotone in rho, no interior extremum at 1
#   f2 = d^2 * s^2 / (d^2+s^2)^2  (a natural normalized product; max at d=s!)  <-- steelman
#   f3 = q-based ratios
print("=== STEELMAN: does any natural invariant EXTREMIZE at d=s (=> r=sqrt2)? ===")
# parametrize by t=d^2/s^2 (>=0). r^2 = 2 t. r=sqrt2 <=> t=1 <=> d=s.
t = sp.symbols('t', positive=True)
# f2: product over sum-square: g(t)= t/(1+t)^2  (treat d^2=t, s^2=1)
g2 = t/(1+t)**2
dg2=sp.diff(g2,t); ext=sp.solve(dg2,t)
print("  f2 = d^2 s^2/(d^2+s^2)^2  extremum at t=d^2/s^2 =", ext, " => r=sqrt(2t)=", [sp.sqrt(2*e) for e in ext])
print("    *** t=1 => d=s => r=sqrt2 EXACT.  But is f2 a *forced* potential? ***")
print("    f2 is MAXIMIZED at equal split. This is the ONLY natural single-knob extremum at r=sqrt2.")
print("    Q: does any FLAVOR DYNAMICS produce V ~ -f2 (or +f2) with NO 2/3 input? See below.")
print()

# Is f2 = d^2 s^2/(d^2+s^2)^2 expressible as a ratio of S3 invariants WITHOUT 2/3?
# d^2 = q - s^2, s^2 = e1^2/3. In terms of e1,q:
#   s^2 = e1^2/3 ;  d^2 = q - e1^2/3.  f2 = (q-e1^2/3)(e1^2/3)/q^2... let's see
e1,q = sp.symbols('e1 q', real=True)
s2=e1**2/3; d2=q-e1**2/3
f2_inv = sp.simplify(d2*s2/(d2+s2)**2)
print("  f2 in invariants =", f2_inv, "  (note d2+s2=q)")
f2_inv2 = sp.simplify(d2*s2/q**2)
print("  = (q - e1^2/3)(e1^2/3)/q^2 =", f2_inv2)
print("  -> a clean ratio of e1^2 and q. NO 2/3 appears. Its max IS at d=s.")
print()
print("  *** CRITICAL CHECK: is maximizing d^2 s^2/q^2 a NATURAL dynamical principle, or")
print("      is it reverse-engineered from wanting d=s?  An extremum of a PRODUCT d^2*s^2")
print("      at FIXED q is the AM-GM point d^2=s^2 -- a GENERIC 'maximize the product")
print("      subject to fixed sum' result, NOT specific to flavor. Check it's AM-GM: ***")
# maximize d2*s2 subject to d2+s2 = q fixed -> Lagrange -> d2=s2. Pure AM-GM.
lam=sp.symbols('lam'); D,S=sp.symbols('D S',positive=True)
Lg = D*S - lam*(D+S-q)
sol=sp.solve([sp.diff(Lg,D),sp.diff(Lg,S),sp.diff(Lg,lam)],(D,S,lam),dict=True)
print("   max(D*S | D+S=q): ", [(sp.simplify(s_[D]),sp.simplify(s_[S])) for s_ in sol], " => D=S => d=s. AM-GM.")
