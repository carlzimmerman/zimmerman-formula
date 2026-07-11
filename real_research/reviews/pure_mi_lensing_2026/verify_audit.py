import numpy as np, sympy as sp

print("="*68)
print("AUDIT 1: disformal photon cone vs GW170817 (Obstruction 2 / case B)")
print("="*68)
# g_photon = g + B u u ; g=diag(-1,1,1,1), u_mu=(-1,0,0,0) -> g~=diag(-1+B,1,1,1)
# photon dispersion: g~^{mn}k_m k_n=0. Inverse of diag(-1+B,1,1,1) tt-comp=1/(-1+B)
B,w,k=sp.symbols('B omega k',real=True)
# -(1/(1-B)) w^2 + k^2 = 0  ->  (w/k)^2 = 1-B   (phase speed^2 for photon)
cph2 = 1-B                     # careful: inverse metric tt = 1/(B-1) = -1/(1-B)
cgw2 = 1                       # gravitons ride g (passive frame)
print("photon c^2 on g~ =", cph2, " ; graviton c^2 on g =", cgw2)
print("GW170817 bound |cgw/c -1| < ~1e-15  => |B/2| < 1e-15 => B<2e-15 -> ~0")
# lensing bending angle extra piece from disformal ~ B * (potential): B~0 => 0
for Btest in [0, 1e-15, 1e-6, 0.1]:
    split = abs(sp.sqrt(1-Btest)-1)
    print(f"  B={Btest:>7}: |c_gamma/c-1|={float(split):.3e}"
          + ("  <-GW-SAFE, but lensing enhancement ~B ~ 0" if split<1e-14 else "  <-GW-EXCLUDED"))
print("=> GW-surviving corner (B->0) IS the no-lensing corner. Case B DEAD.\n")

print("="*68)
print("AUDIT 2: case C -- is the ~1e7 under-lensing deficit REAL or manufactured?")
print("="*68)
# Modified INERTIA leaves the field eqn (Poisson) UNMODIFIED: rho source is baryonic.
# The only extra stress-energy MI can add is the inertial/kinetic term, which is
# (v/c)^2 suppressed vs rest-mass. Lensing needs an ORDER-1 potential enhancement
# (phantom-DM ~ baryonic rest mass). So MI sources ~(v/c)^2 of what's needed.
for name,v in [("dwarf 30km/s",3e4),("MW 150km/s",1.5e5),("cluster 1000km/s",1e6)]:
    supp=(v/2.998e8)**2
    print(f"  {name:18s}: (v/c)^2 = {supp:.2e}  -> deficit ~ 1/{1/supp:.1e}")
print("MW ~2.5e-7 -> ~4e6 ~ the banked '~1e7 too weak'. Deficit = (v/c)^2 kinematic")
print("suppression of inertial stress-energy. PHYSICALLY ROBUST, not manufactured.\n")

print("="*68)
print("AUDIT 3: partial split (metric nu^a, inertia nu^(1-a)) -- does a<1 under-lens")
print("         AND is it forced by rotation-curve consistency? (Obstruction 3)")
print("="*68)
y=sp.symbols('y',positive=True); nu=sp.sqrt(1+1/y); a=sp.symbols('a',real=True)
# orbits: a_obs = (metric nu^a) applied then inertia divides by mu=nu^-(1-a):
#   a_obs = nu^a * g_bar / (nu^-(1-a)) = nu^a * nu^(1-a) * g_bar = nu * g_bar  (any a) GOOD
a_orbit = nu**a * nu**(1-a)
print("  orbit response (any a):  a_obs/g_bar =", sp.simplify(a_orbit),
      " = nu  (rotation curves fine for ANY a)")
# photons: feel ONLY the metric enhancement nu^a (no inertia). Need full nu.
# lensing 'correctness' ratio = nu^a / nu = nu^(a-1).
print("  photon lensing gets nu^a; needs nu  => ratio nu^(a-1):")
for av in [0.0,0.5,0.9,1.0]:
    r=nu.subs(y,sp.Rational(1,100))**(av-1)  # deep-MOND y=0.01
    print(f"    a={av}: lensing/needed at y=0.01 = {float(r):.3f}"
          +("  correct" if abs(float(r)-1)<1e-9 else "  UNDER-lenses"))
print("  a=1 => correct lensing BUT then inertia^(1-a)=nu^0=1 => mu=1 => NO MI.")
print("=> only a=1 lenses, and a=1 kills MI. Any MI (a<1) under-lenses. Case A=MG.\n")

print("="*68)
print("AUDIT 4: exhaustiveness -- can a photon couple to a 4th 'home'?")
print("="*68)
print("""Any photon coupling that affects bending defines an EFFECTIVE optical metric
(the principal symbol of the modified Maxwell eqs). Modulo a conformal factor
(4D conformal invariance -> zero extra bending, Obstruction 1), that optical
metric is EITHER the shared g (no enhancement) OR distinct from g (a second
cone -> splits from the graviton cone -> GW170817, Obstruction 2). A non-metric
coupling (birefringent/dispersive) gives frequency-dependent bending, unobserved,
and still cone-splits. => no 4th home at geometric-optics level. Trilemma EXHAUSTS.""")
print("AUDIT COMPLETE.")
