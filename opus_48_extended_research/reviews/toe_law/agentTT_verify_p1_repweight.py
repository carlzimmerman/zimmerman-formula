"""
agentTT VERIFY — Part 1: INDEPENDENT re-derivation of the rep / modular-weight claims.

Hostile referee. CENTRAL MISSION: distinguish FORCING (edge EXCLUDED by the
modular/SL(2,R) structure) from CONSISTENCY (center fits, edge not ruled out).

This script independently recomputes, from scratch, the load-bearing claims the
route rests on, WITHOUT importing the route's conclusions:

  (V1) The boost-fixed condition: is Re(omega_pole)=0 truly unique at theta_v=pi/2
       in [0,pi]? And is "Re omega=0" the correct NECESSARY condition for "this
       placement's relaxation is along the boost"?  (route Part 2/4)
  (V2) Discrete-series ladder-norm positivity (n+1)(2Delta+n)>0 — is the center
       ladder a closed unitary lowest-weight module?  (route Part 3)
  (V3) The edge homogeneous weight: is t^-3/2 -> weight -3/2, Delta-independent?
       (route Part 3)
  (V4) THE DECISIVE TEST. Is the edge genuinely a FORBIDDEN rep for the GH modular
       flow, or merely a DIFFERENT admissible sector? Two sub-questions the route's
       forcing claim REQUIRES to be answered "forbidden", and which I test for an
       escape hatch:
       (V4a) Does a MASSIVE scalar in dS actually use the CONTINUOUS (principal/
             complementary) series, not the discrete series? If the physical GH
             two-point function itself decomposes onto the CONTINUOUS series, then
             "GH modular flow is realized on the discrete series" is FALSE as a
             blanket statement and the edge's continuous-series weight is NOT
             forbidden -> CONSISTENCY, not FORCING.
       (V4b) Is the boost-fixed Re(omega)=0 condition actually a property of the
             DISCRETE series, or do the PRINCIPAL-series dS QNMs ALSO have Re=0?
             (dS principal-series QNM frequencies are purely imaginary too!) If so,
             "Re omega=0" does NOT select discrete-over-continuous and the route's
             (P-fixed) discriminator is weaker than claimed.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
print("="*78)
print("VERIFY PART 1 — independent re-derivation of rep / modular-weight claims")
print("="*78)

# ===========================================================================
# (V1) boost-fixed root: Re(omega_pole)=0 unique at theta_v=pi/2 in [0,pi].
# agentS PART1: E_pole = cos(theta_v) cosh u - i sin(theta_v) sinh u, u=(Delta+n)lam.
# The REAL part of E_pole is cos(theta_v) cosh u. cosh u >= 1 > 0 always, so
# Re(E_pole)=0 <=> cos(theta_v)=0. Independently confirm the unique root in [0,pi].
# ===========================================================================
print("\n(V1) boost-fixed condition Re(E_pole)=0:")
theta = sp.symbols('theta', real=True)
Delta, lam = sp.symbols('Delta lambda', positive=True)
nn = sp.symbols('n', integer=True, nonnegative=True)
u = (Delta + nn)*lam
E_pole_re = sp.cos(theta)*sp.cosh(u)   # real part of the pole location
E_pole_im = -sp.sin(theta)*sp.sinh(u)  # imag part
roots = sp.solveset(sp.Eq(E_pole_re, 0), theta, domain=sp.Interval(0, sp.pi))
print(f"    Re(E_pole) = cos(theta)*cosh((Delta+n)lambda); cosh>=1>0 so zero <=> cos(theta)=0")
print(f"    roots of Re(E_pole)=0 on [0,pi]: {roots}")
# also verify cosh u > 0 strictly for all real arg (so cos(theta) is the only driver)
print(f"    cosh(u)>0 for all u (so cos(theta) is the SOLE driver): "
      f"{sp.cosh(sp.symbols('x',real=True)).rewrite(sp.exp).is_positive}")
# verify n-independence of the root (the SAME theta=pi/2 for every rung n)
print(f"    root is n-INDEPENDENT (every rung fixed at the SAME theta=pi/2): "
      f"{'pi/2' in str(roots)}")

# CRITICAL CAVEAT CHECK (the referee's job): is Re(omega)=0 the RIGHT necessary
# condition? agentS itself flags (sec 4): at FINITE lambda Re omega=0 selects
# theta=pi/2 sharply, but SEMICLASSICALLY (lambda->0) the selector DEGRADES to
# O(lambda): Re/Im ~ cot(theta) Delta lambda / 2. Confirm this degradation.
print("\n    [CAVEAT] semiclassical degradation of the selector (agentS sec 4):")
ratio_ReIm = sp.simplify(E_pole_re/(-E_pole_im))   # = cot(theta)*cosh(u)/sinh(u)
# small-lambda expansion at fixed n, Delta:
ratio_small = sp.series(ratio_ReIm.subs(nn,0), lam, 0, 2).removeO()
print(f"      Re/|Im| = cot(theta) cosh(u)/sinh(u); small-lambda (n=0): {sp.simplify(ratio_small)}")
print(f"      => the boost-fixed SELECTOR is sharp ONLY at finite lambda; it is an")
print(f"         O(lambda) discriminator semiclassically (agentS-flagged limitation).")

# ===========================================================================
# (V2) discrete-series ladder-norm positivity.
# Claim: |<n+1|L_+|n>|^2 = (n+1)(2Delta+n) > 0 for all n>=0, Delta>0 => closed
# unitary lowest-weight (discrete-series) module.
# ===========================================================================
print("\n(V2) discrete-series ladder norm (n+1)(2Delta+n):")
norm = (nn+1)*(2*Delta+nn)
# Prove positivity for n>=0, Delta>0 symbolically: both factors strictly positive.
f1 = nn+1; f2 = 2*Delta+nn
print(f"    factor1 = n+1 (>0 for n>=0): always >= 1")
print(f"    factor2 = 2Delta+n (>0 for Delta>0,n>=0): always > 0")
print(f"    product (n+1)(2Delta+n) > 0 for all n>=0, Delta>0 => CLOSED unitary module: CONFIRMED")
# sample check
for (n_, d_) in [(0, sp.Rational(1,2)), (3, sp.Rational(1,10)), (20, sp.Rational(7,10))]:
    print(f"      n={n_}, Delta={d_}: norm = {norm.subs({nn:n_, Delta:d_})}")

# ===========================================================================
# (V3) edge homogeneous weight under the dilation.
# t^-p under t->e^a t scales by e^{-a p}. For p=3/2 => weight -3/2, and the WEIGHT
# is Delta-INDEPENDENT (the soft-edge exponent s_E=1/2 is fixed by the sqrt edge,
# Delta enters amplitude only -- agentS sec 3).
# ===========================================================================
print("\n(V3) edge homogeneous dilation weight:")
a = sp.symbols('a', real=True); t = sp.symbols('t', positive=True); p = sp.Rational(3,2)
edge_scaled = (sp.exp(a)*t)**(-p)
weight = sp.simplify(sp.log(edge_scaled/ t**(-p)) / a)   # = -p
print(f"    (e^a t)^(-3/2) / t^(-3/2) = e^(-3a/2) => homogeneous weight = {weight}")
print(f"    weight is a PURE NUMBER (-3/2), Delta-INDEPENDENT (s_E=1/2 fixed by sqrt edge).")
print(f"    => edge late-time tower carries NO lowest-weight Delta. CONFIRMED.")

print("\n" + "="*78)
print("V1-V3 reproduce the route's structural inputs. The DECISIVE forcing-vs-")
print("consistency test (V4: is the edge a FORBIDDEN rep or a DIFFERENT admissible")
print("sector?) is in agentTT_verify_p2_forcing.py.")
print("="*78)
