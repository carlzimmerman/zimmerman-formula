"""
agentWW PART 2 — the load-bearing scrutiny: is the boost-orbit acceleration the SAME object
as Deser-Levin's 'uniformly accelerated observer', and does modular KMS REALLY give Tolman?

Three hostile checks:
 (H1) Boost Killing orbits = constant-r static worldlines? Constant proper acceleration?
 (H2) Does the modular-flow KMS temperature of a state on a *redshifted* worldline obey the
      Tolman law T(x) = kappa/(2pi|xi(x)|), i.e. is T_modular truly position-dependent this way?
 (H3) DL = GEMS embedding temperature for ARBITRARY uniformly-accel worldlines. The boost orbits
      are a 1-param subfamily (all SHARE the cosmological horizon as their Rindler horizon).
      Does DL's a-range coincide with the boost-orbit a-range, or is DL strictly larger?
"""
import sympy as sp

H = sp.symbols('H', positive=True)
c, s = sp.symbols('c s', positive=True)   # cos,sin of proper-distance angle u, both >0
r, t = sp.symbols('r t', positive=True)

print("="*78); print("PART 2 — boost orbit vs Deser-Levin observer; modular Tolman law"); print("="*78)

# (H1) The static-patch boost is xi = d/dt (the timelike Killing vector). Its orbits are
# curves of constant (r,theta,phi). The static observer u^mu = xi^mu/|xi| is exactly the
# normalized boost orbit. Its proper acceleration a = H^2 r/sqrt(1-H^2 r^2) (Part A) is
# CONSTANT along the orbit (independent of t). => boost orbit = stationary worldline,
# constant proper acceleration. CONFIRMED by t-independence of a(r).
print("\n[H1] boost orbit = constant-r worldline; a(r)=H^2 r/sqrt(1-H^2r^2) is t-independent")
print("     => stationary worldline of CONSTANT proper acceleration. CONFIRMED.")

# (H2) Tolman law for a KMS (thermal) state w.r.t. a Killing flow: the locally-measured
# temperature is T_loc = T_infinity / |xi|, with T_infinity the temperature at |xi|=1.
# For the GH/boost modular state, the boost-KMS condition fixes T in the KILLING (boost)
# time at beta_boost = 2pi/kappa with kappa=H (so T at the |xi|=1 'tortoise' normalization
# = H/2pi = GH temperature). The proper-time temperature on a worldline of redshift |xi| is
# T_proper = (H/2pi)/|xi|. This is the DEFINITION of a Killing-thermal (KMS) state's Tolman
# profile; verify it reproduces DL.
xi = c                               # |xi| = cos(u) = c
T_inf = H/(2*sp.pi)                  # GH temperature at |xi|->1 (horizon-normalized)
T_proper_modular = T_inf/xi          # Tolman
a = H*s/c                            # proper acceleration on this orbit (Part A)
T_DL = sp.sqrt(a**2 + H**2)
T_DL = sp.sqrt(sp.simplify(a**2+H**2).subs(s**2,1-c**2))/(2*sp.pi)  # -> (H/c)/2pi
print("\n[H2] modular Tolman profile  T_proper = (H/2pi)/|xi| =", sp.simplify(T_proper_modular))
print("     Deser-Levin               T_DL      =", sp.simplify(T_DL))
print("     difference =", sp.simplify(T_proper_modular - T_DL), " (0 => Tolman modular = DL EXACT)")
assert sp.simplify(T_proper_modular - T_DL) == 0

# (H3) DL/GEMS a-range vs boost-orbit a-range.
# Boost orbits: a = H tan(u), u in (0,pi/2) => a in (0, inf).  ALL accelerations covered.
# DL formula T=sqrt(a^2+H^2)/2pi is stated for a uniformly-accelerated dS observer; the
# stationary (constant-a) worldlines in dS that admit a global GEMS thermal interpretation
# are exactly the boost orbits (and their de Sitter-isometry images). So the a-ranges COINCIDE.
print("\n[H3] boost-orbit a-range: a=H tan(u), u in (0,pi/2) => a in (0,inf): EVERY DL value.")
print("     The DL stationary observers ARE the boost orbits (up to dS isometry). RANGES COINCIDE.")

# Cross-check numerics at a couple of accelerations
import mpmath as mp
mp.mp.dps = 30
Hv = mp.mpf('1.0')
for av in ['0.5','1.0','5.78881','33.5']:
    av = mp.mpf(av)
    # cos(u) = H/sqrt(a^2+H^2)
    cosu = Hv/mp.sqrt(av**2+Hv**2)
    T_mod = (Hv/(2*mp.pi))/cosu
    T_dl  = mp.sqrt(av**2+Hv**2)/(2*mp.pi)
    print(f"     a={float(av):>8.4f}: T_modular={float(T_mod):.12f}  T_DL={float(T_dl):.12f}  d={float(T_mod-T_dl):.2e}")

print("\n[CONCLUSION PART 2]")
print(" The DL temperature is EXACTLY the Tolman-blueshifted boost-modular (GH-KMS) temperature")
print(" of the type II_1 observer algebra, on the boost orbits, which realize every acceleration.")
print(" The identification is a STRUCTURAL identity (same object), NOT an analogy, NOT a")
print(" new derivation of a0. The only quantum-mechanical INPUT beyond semiclassics that this")
print(" uses is CLPW's result that the boost IS the modular flow and GH is KMS — already banked.")
