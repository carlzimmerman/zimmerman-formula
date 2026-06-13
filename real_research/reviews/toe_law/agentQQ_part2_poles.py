import sympy as sp
import mpmath as mp
mp.mp.dps = 40

omega, w0, g, c = sp.symbols('omega omega0 gamma c', real=True, positive=True)
omegaC = sp.symbols('omega', real=True)  # the running freq (allow negative)
chi = c/(w0**2 - omegaC**2 - sp.I*g*omegaC)

den = w0**2 - omegaC**2 - sp.I*g*omegaC
poles = sp.solve(den, omegaC)
print("Poles of chi(omega) in omega-plane:")
for p in poles:
    print("   omega =", sp.nsimplify(p), "   Im part for g,w0>0:", sp.simplify(sp.im(p.subs({w0:1,g:sp.Rational(1,5)}))))

print("\n=> Both poles have Im(omega) = -gamma/2 < 0 (LHP) for gamma>0, INDEPENDENT of sign(c).")
print("   So negative residue c<0 (active gain) keeps the response CAUSAL (poles LHP).")
print("   Anti-damping gamma<0 would flip Im(omega)>0 (UHP) => exponential runaway.\n")

# Im chi on real axis, c=-1 (active gain)
print("Im chi(omega) for c=-1 (active), w0=1, gamma=0.2:")
chiN = (-1)/(1 - omegaC**2 - sp.I*sp.Rational(1,5)*omegaC)
f = sp.lambdify(omegaC, chiN, 'mpmath')
for wv in [0.5,0.9,1.0,1.1,1.5]:
    val = f(wv)
    print(f"   omega={wv}: Im chi={float(mp.im(val)):+.4f} (neg=>active)   Re chi={float(mp.re(val)):+.4f}")

# Verify the DC ordering this produces: chi(0) vs chi(inf)
chi0 = float(chiN.subs(omegaC,0))
print(f"\n  chi(0)={chi0:+.4f}, chi(inf)=0 (decays). With negative residue, chi(0)<chi(inf)")
print("  => this is the INVERTED MOND ordering. Active gain delivers BOTH the X2 ordering")
print("     AND the negative spectral weight PP needs. SAME object.")
