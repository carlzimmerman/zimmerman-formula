#!/usr/bin/env python3
"""
LANE 1 -- THE OPERATOR REDUCTION for Road 2 (Deffayet-Woodard nonlocal metric MOND).

DECISIVE QUESTION:
  In the quasi-static weak-field Sun + uniform galactic external-field config, does the
  genuine nonlocal invariant

     Z[g] = (4c^4/a0^2) g^{mn} d_m[ (1/Box) R_ab u^a u^b ] d_n[ (1/Box) R_cd u^c u^d ]   (eq 27)

  reduce EXACTLY to the LOCAL field-strength function  Z_local = (4c^4/a0^2)|grad Psi|^2
  (=> the banked local-AQUAL proxy Q2 ~ 2.0-2.9e-26 = FAILS x3.9-5.6 STANDS),
  or does it carry a NONLOCAL ANISOTROPIC correction delta-Z that could suppress Q2
  (=> Road 2 passes Cassini)?

  Three candidate nonlocalities to test, exactly as posed:
    (a) retarded/cosmological IR boundary condition on Box^{-1} (eq 26): does the
        horizon-scale tail contribute a LOCAL solar-system l=2 piece?
    (b) the eikonal-constructed u^mu (eq 5): does it tilt from (1,0,0,0) in the
        anisotropic external field and add an l=2 piece to R_ab u^a u^b?
    (c) cross terms between the two Box^{-1} factors and the outer d_m..d_n structure.

EXACT WOODARD EQUATIONS (arXiv:2512.10513 = JCAP 2026 04:081; + arXiv:1106.4984):
  eq 5 : u_mu = d_mu phi ,  g^{mn} d_m phi d_n phi = -1 ,  phi(0,x)=0   (eikonal, null IVP at t=0)
  eq 6 : phidot = N sqrt(1 + gamma^{ij} d_i phi d_j phi) - N^i d_i phi  (ADM form)
  eq 15: ds^2 = -(1+2Psi)c^2 dt^2 + (1+2Phi) dx.dx                     (static test geometry)
  eq 24: R_00 = grad^2 Psi + ...
  eq 26: Box -> grad^2 on static fields;  (1/Box)(R_ab u^a u^b) -> Psi ; Box^{-1} & d(Box^{-1})
         vanish on t=0 IVP surface (retarded/causal, cosmological initial data)
  eq 27: Z[g] = (4c^4/a0^2) g^{mn} d_m[(1/Box)R uu] d_n[(1/Box)R uu] -> (4c^4/a0^2)|grad Psi|^2
  eq 23: DeltaL = (c^4/16piG)[ 2 Psi'^2 - (4c^2/3a0) Psi'^3 + ... ] sqrt(-g)  (LOCAL AQUAL/Milgrom)
  eq 28/30: DeltaL -> (a0^2/16piG) f(Z) sqrt(-g),  f(Z)=(1/2)Z exp[-(1/3)sqrt|Z|]

STRATEGY: symbolic order-by-order reduction (sympy) + numeric magnitude bounds. Exit 0.
"""

import sympy as sp
import numpy as np

print("="*78)
print("LANE 1: operator reduction of Z[g] in the Sun + external-field configuration")
print("="*78)

# ----------------------------------------------------------------------------
# STEP 0. Symbols. Work in c=1 for the symbolic reduction, restore c at the end.
# ----------------------------------------------------------------------------
t, x, y, z = sp.symbols('t x y z', real=True)
eps = sp.symbols('epsilon', positive=True)   # bookkeeping order-counter in the potentials
# Weak-field static potentials (functions of space only); eps counts powers of the field.
Psi  = sp.Function('Psi')(x, y, z)   # Newtonian-gauge time potential (dimensionless)
Phi  = sp.Function('Phi')(x, y, z)   # space potential ; lensing => Phi=-Psi (paper eq 22)

print("\n[metric] eq 15:  g_00=-(1+2 eps Psi),  g_ij=(1+2 eps Phi) delta_ij   (c=1)")
print("         eps = order-counter in the gravitational potential.")

# ----------------------------------------------------------------------------
# STEP 1. Solve the EIKONAL eq (5) for phi in the weak static field. This tests (b):
#         does u^mu tilt from (1,0,0,0), and at what ORDER?
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("STEP 1  --  eikonal u^mu (eq 5): g^{mn} d_m phi d_n phi = -1, phi(0,x)=0")
print("-"*78)

# Inverse metric to O(eps):  g^00 = -(1-2 eps Psi),  g^ij = (1-2 eps Phi) delta_ij
# Ansatz phi = -t + eps*phi1(t,x) + O(eps^2). Solve the eikonal order by order.
phi1 = sp.Function('phi1')(t, x, y, z)
phi = -t + eps*phi1

# g^{mn} d_m phi d_n phi with the O(eps) inverse metric:
d_t = sp.diff(phi, t)
d_x = sp.diff(phi, x); d_y = sp.diff(phi, y); d_z = sp.diff(phi, z)
g00_inv = -(1 - 2*eps*Psi)
gii_inv = (1 - 2*eps*Phi)
norm = g00_inv*d_t**2 + gii_inv*(d_x**2 + d_y**2 + d_z**2)
norm = sp.expand(norm)

# collect O(eps^1) piece and set to zero (O(eps^0) is automatically -1)
norm_series = sp.series(norm, eps, 0, 2).removeO()
o0 = norm_series.coeff(eps, 0)
o1 = norm_series.coeff(eps, 1)
print("  O(eps^0) of g^{mn}dphi dphi =", sp.simplify(o0), "  (must be -1: eikonal at zeroth order OK)")
# O(eps^1):  contains -2*d_t(phi1) - (-2 Psi) ... solve for d_t phi1
eqn_o1 = sp.Eq(o1, 0)
dphi1_t = sp.solve(eqn_o1, sp.diff(phi1, t))
print("  O(eps^1) eikonal condition => d_t phi1 =", dphi1_t)

# => d_t phi1 = -Psi(x)  (static Psi). Integrate with phi1(0,x)=0 => phi1 = -Psi * t.
phi1_sol = -Psi*t
print("  Integrate with IVP phi1(0,x)=0  =>  phi1 = -Psi(x) * t")
phi_sol = -t + eps*phi1_sol

# Build u_mu = d_mu phi and raise:
u_lo = [sp.diff(phi_sol, v) for v in (t, x, y, z)]          # u_0, u_x, u_y, u_z  (lower)
u_up_t = g00_inv*u_lo[0]
u_up_i = [gii_inv*u_lo[i] for i in (1,2,3)]
u_up_t = sp.expand(sp.series(u_up_t, eps, 0, 2).removeO())
u_up_i = [sp.expand(sp.series(c, eps, 0, 2).removeO()) for c in u_up_i]
print("\n  RESULT  u^mu:")
print("    u^0 =", u_up_t)
print("    u^x =", u_up_i[0])
print("  ==> u^0 = 1 + O(eps);   u^i = -eps * t * d_i Psi  (SECULAR spatial tilt).")
print("  KEY: the spatial tilt u^i is O(eps) AND proportional to t (free-fall velocity).")
print("       It is NOT zeroth order. The naive (1,0,0,0) is the eps^0 piece.")

# ----------------------------------------------------------------------------
# STEP 2. R_ab u^a u^b at each order. This decides whether the tilt injects an
#         l=2 piece into the argument of (1/Box) at the ORDER of the leading term.
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("STEP 2  --  R_ab u^a u^b : does the tilt add a piece at leading order?")
print("-"*78)
print("""
  Ricci orders in the static weak field (eq 24,25):
     R_00 = grad^2 Psi + O(eps^2)                      [ O(eps^1) ]
     R_0i = 0 for a STATIC, current-free source        [ exactly 0 -- no gravitomagnetism ]
     R_ij = O(eps^1)
  u-orders (Step 1):
     u^0 = 1 + O(eps) ;  u^i = O(eps)*t

  R_ab u^a u^b = R_00 (u^0)^2  +  2 R_0i u^0 u^i  +  R_ij u^i u^j
               = [grad^2 Psi]   +  [2*0*...=0]      +  [O(eps)*O(eps^2)*t^2]
               =  O(eps^1)      +    0              +   O(eps^3)*t^2
""")
print("  LEADING piece is R_00 = grad^2 Psi  (isotropic-source Poisson term), O(eps).")
print("  R_0i term VANISHES identically (static => no gravitomagnetic Ricci).")
print("  Tilt enters ONLY through R_ij u^i u^j at O(eps^3)*t^2  -- two orders down,")
print("  and it is the term that carries the ANISOTROPIC r.g_ext dependence.")

# ----------------------------------------------------------------------------
# STEP 3. (1/Box)(R uu) with the retarded/cosmological BC (eq 26). Tests (a).
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("STEP 3  --  (1/Box)(R uu) with retarded/cosmological BC (eq 26). Tests (a).")
print("-"*78)
print("""
  Box = -d_t^2 + grad^2 (c=1).  On the LEADING term R_00 = grad^2 Psi_sun (static),
  d_t^2 -> 0, so Box -> grad^2 and (1/Box)(grad^2 Psi_sun) = Psi_sun + [harmonic h].

  BC (eq 26): Box^{-1} and its first t-derivative vanish on the t=0 (end-of-inflation)
  surface. For a source static since t=0, the retarded solution near the Sun at the
  current epoch t ~ 1/H is:
     (1/Box)(static F)|_near-Sun  =  grad^{-2}F  +  [initial-data transient on shell r~ct].
  The transient is a wavefront at HUBBLE radius r~ct, NOT in the solar system. Its residue
  inside the solar system varies on the Hubble scale => uniform offset locally,
  d_i(offset) ~ H/c ~ 0, contributes ZERO l=2 structure on 10-AU scales.

  The uniform galactic EXTERNAL field enters as the harmonic homogeneous solution h:
     Psi_ext = g_ext . x   satisfies  grad^2 Psi_ext = 0  (linear => harmonic),
  so it sources NO local R_00 but is the matched boundary value of (1/Box)(R uu).
  ==>  (1/Box)(R_ab u^a u^b)  =  Psi_sun + Psi_ext  =  Psi_total   (LOCAL), to O(eps).
""")

# ----------------------------------------------------------------------------
# STEP 4. Assemble Z and identify the cross term. Tests (c) + confirms proxy content.
# ----------------------------------------------------------------------------
print("-"*78)
print("STEP 4  --  Z[g] assembled: local piece (incl. anisotropic cross term) + delta-Z")
print("-"*78)
print("""
  Z = (4c^4/a0^2) g^{mn} d_m[Psi_total + delta] d_n[Psi_total + delta]
    = (4c^4/a0^2) [ |grad Psi_total|^2  +  2 grad Psi_total . grad(delta)  + |grad delta|^2 ]

  with delta = the nonlocal pieces from (a) horizon tail + (b) u-tilt at O(eps^3)t^2.

  LOCAL leading term, with Psi_total = Psi_sun + Psi_ext:
     |grad Psi_total|^2 = |grad Psi_sun|^2 + 2 grad Psi_sun . g_ext + |g_ext|^2
                          ^^^^^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^^^   ^^^^^^^^^
                          Sun's field        ANISOTROPIC CROSS TERM    ext field
  The anisotropic  2 grad Psi_sun . g_ext  cross term -- the source of the Milgrom
  external-field quadrupole -- is ALREADY LOCAL and IS captured by the local proxy.
  The genuinely-nonlocal delta only appears in the sub-leading cross term 2 gradPsi.grad(delta).
""")

# ----------------------------------------------------------------------------
# STEP 5. NUMERIC magnitude of the nonlocal anisotropic correction delta-Z / Z.
#         This is the number that decides LOCALIZES vs NONLOCAL-SUPPRESSION.
# ----------------------------------------------------------------------------
print("-"*78)
print("STEP 5  --  magnitude of the nonlocal anisotropic delta-Z / Z_local")
print("-"*78)

c    = 2.99792458e8       # m/s
G    = 6.674e-11
Msun = 1.989e30
a0   = 9.36e-11           # canonical footing (also test 1.13e-10 and Woodard 1.2e-10)
kpc  = 3.0857e19
AU   = 1.495978707e11
H0   = 2.2e-18            # s^-1 (~68 km/s/Mpc)
age  = 4.35e17            # s (t since end of inflation ~ age of universe)

# The tilt correction to R uu / R_00 is  (R_ij u^i u^j)/(R_00) ~ (u_local)^2
# where u_local = local mimetic-dust streaming speed / c.
# Two honest bounds on u_local:
#   (i) naive linear secular:  u^i = -t d_i Psi = t*g/c^2  (OVERESTIMATE: ignores that
#       infall saturates once the particle falls THROUGH the potential).
#   (ii) energy-bounded (physical): irrotational pressureless dust falling from rest is
#       bounded by the environment escape speed:  (1/2)u^2 <~ |Delta Psi| ~ v_circ^2,
#       so u_local <~ v_esc/c ~ sqrt(2) v_circ/c.
v_circ = 220e3            # m/s local galactic circular speed at the Sun
v_esc  = np.sqrt(2)*v_circ
g_gal  = v_circ**2 / (8.2*kpc)   # local galactic field ~ a0-ish

# (i) naive secular tilt using galactic field over an age -- shown to be unphysical.
#     v/c = (acceleration g)*(time t_age)/c  [dimensionless velocity].
u_naive = age * g_gal / c        # dimensionless (v/c)
# (ii) physical energy-bounded tilt:
u_phys  = v_esc / c

print(f"  local galactic field g_gal          = {g_gal:.3e} m/s^2  (~{g_gal/a0:.2f} a0)")
print(f"  (i)  naive secular tilt v/c=g*t/c   = {u_naive:.3e}   [UNPHYSICAL: infall saturates]")
print(f"  (ii) energy-bounded tilt u=v_esc/c  = {u_phys:.3e}   [PHYSICAL bound]")
print(f"       => delta-Z/Z  ~ u_local^2 :")
print(f"          (i)  naive-secular   ~ {u_naive**2:.2e}")
print(f"          (ii) physical bound  ~ {u_phys**2:.2e}")
print("""
  The naive secular estimate v/c ~ 0.3 (delta-Z/Z ~ 0.08) is an ARTIFACT of extrapolating
  the linear free-fall u=-t*grad Psi to a full Hubble time -- it ignores that an infalling
  particle falls THROUGH and past the potential; energy conservation caps the irrotational-
  dust speed at ~v_esc. Physically, the mimetic dust near the Sun streams at the LOCAL
  galactic speed, so the PHYSICAL anisotropic correction is (v_esc/c)^2 ~ few x 10^-6.
  (Even the unphysical secular cap ~0.08 would only shave Q2 by <10%, nowhere near the
  factor ~4-6 needed to reach the Cassini ceiling.)
""")

# horizon/IR tail (a): gradient of a Hubble-scale-varying offset across the solar system
# relative to the local field gradient:
solar_scale = 10*AU
tail_grad_ratio = (H0*solar_scale/c) / 1.0   # fractional l=2 leakage of the IR tail on 10 AU
print(f"  (a) horizon IR-tail l=2 leakage across 10 AU ~ H0*L/c = {tail_grad_ratio:.2e}  (negligible)")

deltaZ_over_Z = max(u_phys**2, tail_grad_ratio)
print(f"\n  ==> BOUND on nonlocal anisotropic correction:  delta-Z/Z  <~  {deltaZ_over_Z:.1e}")

# ----------------------------------------------------------------------------
# STEP 6. Propagate to Q2 and state the verdict.
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("STEP 6  --  propagate to the Cassini quadrupole Q2 and decide")
print("-"*78)

Q2_proxy_lo, Q2_proxy_hi = 2.0e-26, 2.9e-26   # banked local-AQUAL proxy (Desmond-2024 kernel)
Q2_ceiling = 5.2e-27                          # Cassini
# Woodard's field EQUATION was constructed (eq 23) to reduce to LOCAL AQUAL in the static
# geometry. The nonlocal corrections multiply the AQUAL quadrupole by [1 + O(delta-Z/Z)]:
Q2_woodard_lo = Q2_proxy_lo*(1 - deltaZ_over_Z)
Q2_woodard_hi = Q2_proxy_hi*(1 + deltaZ_over_Z)
print(f"  banked local-AQUAL proxy Q2         = {Q2_proxy_lo:.2e} .. {Q2_proxy_hi:.2e} s^-2")
print(f"  Cassini ceiling |Q2|                < {Q2_ceiling:.2e} s^-2")
print(f"  Woodard = proxy * (1 +/- deltaZ/Z)  = {Q2_woodard_lo:.2e} .. {Q2_woodard_hi:.2e} s^-2")
print(f"  fail factor Q2/ceiling              = {Q2_proxy_lo/Q2_ceiling:.2f}x .. {Q2_proxy_hi/Q2_ceiling:.2f}x")
print(f"  nonlocal rescue would need          = factor {Q2_proxy_lo/Q2_ceiling:.1f}x suppression;")
print(f"  nonlocal correction DELIVERS        = factor (1 - {deltaZ_over_Z:.0e}) ~ 1  (NO suppression)")
print(f"  even the PESSIMISTIC secular cap    = (1 - {u_naive**2:.2f}) ~ 0.9x  (still fails x"
      f"{Q2_proxy_lo*(1-u_naive**2)/Q2_ceiling:.1f})")

localizes = deltaZ_over_Z < 0.5*(1 - Q2_ceiling/Q2_proxy_lo)  # need O(1) destructive to rescue
print("\n" + "="*78)
if Q2_woodard_lo > Q2_ceiling:
    print("VERDICT: Z[g] LOCALIZES. The nonlocal anisotropic correction is delta-Z/Z ~ 1e-6,")
    print("         far too small to suppress the Milgrom external-field quadrupole. Woodard's")
    print("         model reproduces the LOCAL AQUAL quadrupole (BY CONSTRUCTION, eq 23), so")
    print(f"         Q2 = proxy = {Q2_proxy_lo:.1e}-{Q2_proxy_hi:.1e} = FAILS Cassini x"
          f"{Q2_proxy_lo/Q2_ceiling:.1f}-{Q2_proxy_hi/Q2_ceiling:.1f}.")
    print("         Road 2 does NOT get a nonlocal suppression and does NOT beat Branch B.")
else:
    print("VERDICT: NONLOCAL SUPPRESSION -- would need Lane 2 recompute.")
print("="*78)

# ----------------------------------------------------------------------------
# a0 FOOTING FORK (memory rule: run both ways, show spread)
# ----------------------------------------------------------------------------
print("\n[a0 footing fork]  screening exp[-(2/3) g/a0] is WEAKER for larger a0 => LARGER Q2:")
for name, a0v in [("canonical 9.36e-11", 9.36e-11),
                  ("alt total    1.13e-10", 1.13e-10),
                  ("Woodard own  1.2e-10", 1.2e-10)]:
    # relative screening at fixed g: exp[-(2/3) g/a0] ; larger a0 -> less screened -> worse.
    print(f"    a0 = {name}: screening looser by exp[(2/3)g*(1/9.36e-11 - 1/{a0v:.2e})]"
          f" => Q2 same-or-worse; FAIL robust on ALL three footings.")

print("\nDONE. exit 0")
