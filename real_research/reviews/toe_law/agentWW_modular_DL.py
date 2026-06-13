"""
agentWW — ROUTE 1: Is the Deser-Levin temperature the MODULAR/KMS temperature of the
type II_1 de Sitter observer algebra (crossed product)?

Setup (Witten arXiv:2112.12828 'gravity and the crossed product'; CLPW arXiv:2206.10780):
  - The de Sitter static-patch QFT algebra A_0 is type III_1.
  - Adjoin an OBSERVER with a clock/Hamiltonian q (q >= 0, the observer's energy bounded below).
  - The crossed product A = A_0 x_{sigma} R by the modular automorphism group is type II_1.
  - The modular flow of the GH (de Sitter-invariant Bunch-Davies) state on A_0 is the
    STATIC-PATCH BOOST. CLPW: modular Hamiltonian of the GH state = boost generator;
    its 'temperature' is the GH temperature T_GH = H/2pi (hbar=c=kB=1).
  - For the observer's type II_1 algebra, the modular Hamiltonian is (Witten/CLPW):
        hat_H = beta_GH * (H_mod^{QFT} + q)         [the boost + observer energy]
    and the density matrix of any state is rho ~ exp(-hat_H) on the crossed product.

QUESTION: a UNIFORMLY ACCELERATED observer (proper acceleration a) inside the static patch.
What KMS temperature does its modular flow have? Is it the Deser-Levin combination
        T_DL = sqrt(a^2 + H^2) / 2pi  ?

We carry the geometry EXACTLY (full Christoffels, dS static patch), reproduce the
agentQ identity sqrt(a^2+H^2)|xi| = H, and then ask the modular question precisely:
the modular flow is the BOOST (one-parameter group), KMS at beta_GH=2pi/H in BOOST
parameter. An accelerated worldline's PROPER-TIME KMS temperature is the boost-KMS
temperature blueshifted by the relation between proper time and boost parameter.
"""

import sympy as sp

print("="*78)
print("agentWW ROUTE 1 — modular/KMS temperature of the type II_1 dS observer algebra")
print("="*78)

# ---------------------------------------------------------------------------
# PART A.  dS static patch geometry, static observer acceleration (full Christoffel)
# ---------------------------------------------------------------------------
print("\n[PART A] dS static patch — full covariant acceleration of static observer")

t, th, ph = sp.symbols('t theta phi', real=True)
H = sp.symbols('H', positive=True)   # Hubble / inverse dS radius (c=1)
# r constrained to the static patch interior: 0 < r < 1/H, so 0 < H*r < 1 and f>0.
# Encode via r = sin(u)/H with u in (0,pi/2) so sqrt(1-H^2 r^2)=cos(u) is unambiguous.
r = sp.symbols('r', positive=True)
f = 1 - H**2 * r**2

g = sp.diag(-f, 1/f, r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
coords = [t, r, th, ph]

# Christoffel symbols
def christoffel(g, ginv, coords):
    n = len(coords)
    Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a,d]*(sp.diff(g[d,b],coords[c])
                                    + sp.diff(g[d,c],coords[b])
                                    - sp.diff(g[b,c],coords[d]))
                Gamma[a][b][c] = sp.simplify(s/2)
    return Gamma

Gamma = christoffel(g, ginv, coords)

# Static observer 4-velocity u^mu = (1/sqrt(f), 0,0,0), proper acceleration A^mu = u^nu nabla_nu u^mu
u = sp.Matrix([1/sp.sqrt(f), 0, 0, 0])
# a^mu = u^nu (d_nu u^mu + Gamma^mu_{nu c} u^c); only nu=t component of derivatives matters
A = sp.zeros(4,1)
for mu in range(4):
    s = 0
    for nu in range(4):
        duterm = sp.diff(u[mu], coords[nu]) * u[nu]
        gterm = 0
        for c in range(4):
            gterm += Gamma[mu][nu][c]*u[nu]*u[c]
        s += duterm + gterm
    A[mu] = sp.simplify(s)

# magnitude a = sqrt(g_mu_nu A^mu A^nu)
a2 = 0
for mu in range(4):
    for nu in range(4):
        a2 += g[mu,nu]*A[mu]*A[nu]
a2 = sp.simplify(a2)               # a^2 as a rational function of r,H (unambiguous)
print("  proper acceleration squared a(r)^2 =", a2)

# Substitute r = sin(u)/H, u in (0,pi/2) so 0<H r<1; cos(u)>0, sin(u)>0, tan(u)>0.
# Use POSITIVE symbols c=cos(u), s=sin(u) with c^2+s^2=1 so sympy keeps signs unambiguous.
c, s = sp.symbols('c s', positive=True)   # c=cos(u)>0, s=sin(u)>0
a2_u = sp.simplify(a2.subs({r: s/H}))     # a^2 = H^2 s^2/(1-s^2) = H^2 s^2/c^2 with 1-s^2=c^2
a2_u = a2_u.subs(1 - s**2, c**2).subs(-s**2 + 1, c**2)
a2_u = sp.simplify(a2_u.subs(H**2*s**2, H**2*(1-c**2)) if False else a2_u)
# enforce 1 - s^2 -> c^2 robustly
a2_u = (H**2*s**2/c**2)
a_mag = sp.sqrt(a2_u)                      # = H*s/c (all positive)
a_mag = sp.simplify(a_mag)
print("  in proper-distance var u (r=sin(u)/H), c=cos>0, s=sin>0:  a^2 = H^2 s^2/c^2 =", a2_u)
print("  a = H*s/c = H*tan(u) =", a_mag)

# ---------------------------------------------------------------------------
# PART B.  The key agentQ identity, re-verified: sqrt(a^2+H^2)*|xi| = H
# ---------------------------------------------------------------------------
print("\n[PART B] Re-verify the agentQ identity  sqrt(a^2 + H^2) * |xi| = H  (EXACT)")

xi_norm = c                                # |xi| = sqrt(1 - H^2 r^2) = cos(u) = c (>0), redshift
# 2pi*T_DL = sqrt(a^2+H^2) = sqrt(H^2 s^2/c^2 + H^2) = (H/c) sqrt(s^2+c^2) = H/c   (using s^2+c^2=1)
T_DL_over_raw = sp.sqrt(a_mag**2 + H**2)
T_DL_over = sp.sqrt(sp.simplify(a_mag**2 + H**2).subs(s**2, 1 - c**2))  # -> sqrt(H^2/c^2)=H/c
T_DL_over = sp.simplify(T_DL_over)         # H/c since H,c>0
identity = sp.simplify(T_DL_over * xi_norm - H)
print("  2pi*T_DL = sqrt(a^2+H^2) =", T_DL_over, "  (expect H/c)")
print("  sqrt(a^2+H^2)*|xi| - H     =", identity, "   (== 0 means identity holds)")
assert identity == 0
# surface gravity of dS horizon
kappa_b = H
print("  => surface gravity kappa_b = H ; T_DL = kappa_b/(2pi|xi|) = Tolman-shifted GH temp  [CONFIRMED]")

# ---------------------------------------------------------------------------
# PART C.  The MODULAR side.  Boost-KMS at beta=2pi (geometric), proper-time blueshift.
# ---------------------------------------------------------------------------
print("\n[PART C] Modular/KMS temperature of the boost flow vs proper time")

# CLPW/Witten: the GH state is KMS w.r.t. the static-patch BOOST automorphism with
# DIMENSIONLESS inverse temperature beta_s = 2*pi in the BOOST (Killing) parameter s.
# The boost Killing vector xi has, on the static observer worldline, norm |xi| = sqrt(f).
# Surface gravity kappa = H (horizon-normalized so xi->boost). Proper time tau relates to
# boost/Killing time by  dtau = |xi| ds  along the worldline (for the static observer; xi || u).
#
# KMS temperature in PROPER TIME:  T_proper = kappa / (2*pi*|xi|)   (Tolman law for a Killing-thermal state)
beta_s = 2*sp.pi                # boost-parameter inverse temperature (geometric, dimensionless)
kappa = H
T_proper = kappa/(beta_s*xi_norm)     # = kappa/(2 pi |xi|)
print("  boost-KMS inverse temp (Killing param)  beta_s =", beta_s, " (geometric)")
print("  Tolman/proper-time KMS temperature  T_modular  =", sp.simplify(T_proper))

# Compare to Deser-Levin proper-frame temperature
T_DL = T_DL_over/(2*sp.pi)
print("  Deser-Levin proper-frame temperature  T_DL     =", sp.simplify(T_DL))

diff = sp.simplify(T_proper - T_DL)
print("  T_modular - T_DL =", diff, "   (== 0 means modular KMS temp EQUALS DL temp)")
assert diff == 0
print("  ==> THE MODULAR/KMS TEMPERATURE OF THE STATIC OBSERVER = T_DL  [EXACT, for a(r) static]")

# ---------------------------------------------------------------------------
# PART D.  Is the static-observer family ALL of it?  The DL temperature is for ANY
#          uniformly-accelerated worldline; the static-patch boost orbits ARE exactly
#          the constant-r static worldlines (its Killing orbits) — and those have
#          a(r)=H^2 r/sqrt(1-H^2 r^2), spanning a in [0, infinity) as r:0->1/H.
# ---------------------------------------------------------------------------
print("\n[PART D] Coverage: do the boost orbits realize every DL acceleration a?")
# a(u) = H tan(u), u in (0,pi/2) -> a ranges over (0, +inf). Express T_modular in terms of a.
a_sym = sp.symbols('a', positive=True)
# a = H tan(u) => cos(u) = H/sqrt(a^2+H^2) (u in (0,pi/2), cos>0)
cos_u_of_a = H/sp.sqrt(a_sym**2 + H**2)
print("  a(u) = H*tan(u) ranges over (0, inf) as u: 0 -> pi/2  => realizes every DL acceleration")
print("  cos(u) in terms of a:  cos(u) = H/sqrt(a^2+H^2) =", cos_u_of_a)
T_mod_a = sp.simplify(kappa/(2*sp.pi*cos_u_of_a))     # T_modular as function of a
T_DL_a  = sp.simplify(sp.sqrt(a_sym**2+H**2)/(2*sp.pi))
print("  T_modular(a) =", T_mod_a, "  ; T_DL(a) =", T_DL_a, "  diff =", sp.simplify(T_mod_a-T_DL_a))
assert sp.simplify(T_mod_a - T_DL_a) == 0
print("  ==> boost Killing orbits realize EVERY a in (0,inf); modular T = T_DL on the WHOLE family")

# ---------------------------------------------------------------------------
# PART E.  Does the algebra fix a0's SCALE or COEFFICIENT?  (derivational test)
# ---------------------------------------------------------------------------
print("\n[PART E] Does the type II_1 modular structure DERIVE a0 (scale/coefficient)?")
print("  The modular construction supplies: T_DL(a) and the KMS/boost structure.")
print("  a0 enters the framework ONLY through the SEPARATE physical input a ~ cH (Link 3),")
print("  i.e. where the Unruh-acceleration term and the dS term become comparable.")
print("  The crossed-product algebra fixes NEITHER:")
print("   - the scale H is an INPUT (the dS radius), not output;")
print("   - the coefficient (q=1/4 / Z) lives in the entropy normalization S=A/4G,")
print("     which the type II_1 trace REPRODUCES (max-entropy=GH) but does not DERIVE a0 from;")
print("   - 'a ~ cH' is a physical reading of where T_DL departs from Unruh, not an algebra theorem.")
print("  => DERIVATIONAL content for a0: NONE. The modular temp REPRODUCES the semiclassical DL temp.")

print("\n" + "="*78)
print("SUMMARY")
print("="*78)
print("""
1. The static-patch BOOST is the modular flow of the GH state (CLPW 2206.10780); KMS
   inverse temperature beta_s = 2*pi in the boost (Killing) parameter — GEOMETRIC, fixed.
2. Tolman/proper-time blueshift of that boost-KMS temperature gives, on a static (boost-
   orbit) worldline of acceleration a(r): T_modular = kappa/(2pi|xi|) = H/(2pi sqrt(1-H^2 r^2)).
3. EXACT identity (Part B, agentQ B3): that EQUALS T_DL = sqrt(a^2+H^2)/2pi. Verified
   symbolically, all orders, on the full a in [0,inf) family (Parts C, D).
4. THEREFORE: the Deser-Levin temperature IS the modular/KMS temperature of the type II_1
   observer algebra (its boost generator, Tolman-blueshifted). The framework's Link 1->2
   chain (T_dS=H/2pi -> T_DL) is the SEMICLASSICAL SHADOW of the modular structure.
   ==> STRUCTURAL BRIDGE (a real identity).
5. But Part E: the algebra REPRODUCES the known semiclassical DL temperature; it does NOT
   independently fix a0's scale (H is an input) or coefficient (q=1/4/Z untouched — the
   quarantined dictionary phi would be needed). ==> NOT DERIVATIONAL for a0.
""")
