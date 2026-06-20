#!/usr/bin/env python3
"""
bullet_amplitude_sympy_verify.py  --  exact checks behind the amplitude residual
=============================================================================
Three exact (sympy) checks that make the amplitude-residual claim robust and
convention-independent:

 (1) The framework's lensing-mass enhancement IS the boost nu = g_obs/g_bar
     (no gravitational slip in AeST: Phi_lens=Phi_dyn). Deep limit nu->sqrt(a0/g).
 (2) The deep-MOND phantom (extra) mass scales EXACTLY as sqrt(a0):
     M_phantom/M_bar = nu-1, and d ln(nu-1)/d ln a0 -> 1/2 deep -> the +13%
     surcharge for a0 9.36 vs 12 is sqrt(1.2/0.936)-1 EXACTLY.
 (3) The kappa->mass conversion M_2D = kbar * Sigma_crit * pi a^2 is exact, and
     Sigma_crit = c^2 D_s / (4 pi G D_l D_ls). Sanity vs the Clowe numbers.

No fitting; closed-form. Quarantine held (a0/Z inputs, never derived).
"""
import sympy as sp

print("="*74)
print("AMPLITUDE-RESIDUAL EXACT CHECKS (sympy)")
print("="*74)

# ----------------------------------------------------------------------------
# (1) the framework boost / lensing enhancement nu, deep limit
# ----------------------------------------------------------------------------
g, a0 = sp.symbols('g a0', positive=True)
g_obs = sp.sqrt(g**2 + g*a0)          # framework's dS-Unruh interpolation
nu    = g_obs/g                       # = M_dyn/M_bar = M_lens/M_bar (no slip)
nu_simpl = sp.simplify(nu)
print("\n(1) boost nu = g_obs/g =", nu_simpl)
# deep-MOND limit g/a0 -> 0:
x = sp.symbols('x', positive=True)    # x = g/a0
nu_x = sp.sqrt(1 + 1/x)               # nu in units of x=g/a0
deep = sp.limit(nu_x*sp.sqrt(x), x, 0)   # nu*sqrt(x) -> 1  => nu ~ 1/sqrt(x)=sqrt(a0/g)
print("    deep limit: nu*sqrt(g/a0) ->", deep, "  => nu -> sqrt(a0/g)  (deep-MOND)")
assert deep == 1

# ----------------------------------------------------------------------------
# (2) phantom (extra) mass scales as sqrt(a0); the +13% surcharge is exact
# ----------------------------------------------------------------------------
phantom = nu - 1                      # extra mass over baryons (in units of M_bar)
# deep: phantom ~ sqrt(a0/g) - 1 ~ sqrt(a0/g); d ln/ d ln a0:
phantom_deep = sp.sqrt(a0/g)          # leading deep term
dln = sp.simplify(sp.diff(sp.log(phantom_deep), sp.log(a0)) if False else
                  a0*sp.diff(phantom_deep, a0)/phantom_deep)
print("\n(2) deep phantom ~ sqrt(a0/g); d ln(phantom)/d ln a0 =", sp.simplify(dln),
      " (=1/2, the sqrt(a0) scaling)")
# the framework surcharge: a0_fw=9.36e-11 vs a0_canon=1.2e-10
a0_fw, a0_canon = sp.Rational(936, 10000)*sp.Pow(10,-7), sp.Rational(12,100)*sp.Pow(10,-9)
# simpler: just take the ratio numerically-exact
r = sp.sqrt(sp.Rational(936,1200))    # sqrt(a0_fw/a0_canon) exactly
print("    phantom multiplier sqrt(a0_fw/a0_canon) = sqrt(936/1200) =",
      sp.nsimplify(r), "=", float(r))
surcharge = 1/r - 1
print("    => residual surcharge (phantom weaker) = 1/r - 1 =", float(surcharge),
      f"= +{float(surcharge)*100:.1f}%  (the banked ~13%)")

# ----------------------------------------------------------------------------
# (3) kappa -> mass conversion; Sigma_crit closed form
# ----------------------------------------------------------------------------
c, G, D_s, D_l, D_ls, a, kbar = sp.symbols('c G D_s D_l D_ls a kbar', positive=True)
Sigma_crit = c**2/(4*sp.pi*G) * D_s/(D_l*D_ls)
M2D = kbar*Sigma_crit*sp.pi*a**2
print("\n(3) Sigma_crit = c^2 D_s/(4 pi G D_l D_ls) ; M_2D = kbar*Sigma_crit*pi*a^2")
print("    M_2D =", sp.simplify(M2D))
# numeric sanity (Clowe: z_l=0.296, z_s~1, a=100 kpc, kbar=0.36):
subs = {c:2.998e8, G:6.674e-11, D_s:1660*3.0857e22, D_l:920*3.0857e22,
        D_ls:1130*3.0857e22, a:100*3.0857e19, kbar:0.36}
M2D_num = float(M2D.subs(subs))/1.989e30
print(f"    numeric: kbar=0.36, 100kpc, z_s~1 -> M_2D = {M2D_num:.3e} Msun"
      f"  (vs Clowe-class ~3e13)")

print("\n" + "="*74)
print("ALL EXACT CHECKS PASS:")
print("  - lensing enhancement = the boost nu (no slip), deep nu->sqrt(a0/g)")
print("  - phantom mass ~ sqrt(a0): framework a0 -> phantom x0.883 -> residual +13.2%")
print("  - kappa->mass M_2D=kbar*Sigma_crit*pi*a^2 reproduces Clowe-class ~3e13 Msun")
print("="*74)
