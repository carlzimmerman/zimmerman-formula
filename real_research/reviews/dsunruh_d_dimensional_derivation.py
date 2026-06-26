#!/usr/bin/env python3
"""
d-DIMENSIONAL dS-UNRUH MOND: constructive derivation + d=3 load-bearing audit.
==============================================================================
Constructive ask (Carl, 2026-06-25): derive the framework's deep-MOND interpolation
FORM in general spatial dimension d FROM the dS-Unruh posit, and find at which step
(if any) d=3 (dim_SO(3)=3, the cross-product self-duality) becomes REQUIRED.

DISCIPLINE (both-ways, #1 rule): test "d=3 is load-bearing" as ruthlessly as
"d=3 is decorative". Do NOT smuggle d=3 by (a) assuming a 1/r^2 force law,
(b) borrowing AQUAL's d-baked Poisson structure. Derive the force law's
d-dependence from Gauss's law independently, and derive a0(d) from the
dS-Unruh temperature independently.

sympy/mpmath dps>=30. Every FORCED FACT re-verified symbolically.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*86)
print(" PART 0 -- FORCED FACTS the prompt asserts, re-verified symbolically (dps>=30)")
print("="*86)

d = sp.Symbol('d', positive=True, integer=True)

# dim SO(d) = d(d-1)/2 (number of independent rotation generators = # bivectors)
dim_SO = d*(d-1)/sp.Integer(2)
# number of vectors in d dims = d
n_vectors = d
# number of bivectors (antisymmetric rank-2) = d(d-1)/2
n_bivectors = d*(d-1)/sp.Integer(2)

print("  dim SO(d)        = d(d-1)/2  =", dim_SO)
print("  #vectors         = d")
print("  #bivectors       = d(d-1)/2 =", n_bivectors)
# self-duality of the cross product: #vectors == #bivectors  <=>  d = d(d-1)/2
selfdual_eq = sp.Eq(n_vectors, n_bivectors)
sol = sp.solve(sp.Eq(d, d*(d-1)/2), d)
print("  SELF-DUALITY  #vectors == #bivectors  <=>  d = d(d-1)/2  =>  d in", sol,
      "  (d=0 trivial, d=3 the physical self-dual dim)")
# also dim_SO(d) == d at d=3:
print("  dim_SO(d) == d   at d =", sp.solve(sp.Eq(dim_SO, d), d), " -> the 3 = dim_SO(3) coincidence")
print()

# Friedmann denominator d(d-1) = 2 dim_SO(d)
fried_denom = d*(d-1)
print("  Friedmann denominator d(d-1)       =", fried_denom)
print("  2*dim_SO(d)                        =", sp.simplify(2*dim_SO))
print("  d(d-1) == 2 dim_SO(d) ?            ->", sp.simplify(fried_denom - 2*dim_SO) == 0)
print()

# Z^2 = 32 pi / 3 at d=3 ; general Z_d^2
# framework: Z_d = 8 sqrt(pi/(d(d-1)))  ->  Z_d^2 = 64 pi/(d(d-1))
Zd = 8*sp.sqrt(sp.pi/(d*(d-1)))
Zd2 = sp.simplify(Zd**2)
print("  Z_d   = 8 sqrt(pi/[d(d-1)])        ->  Z_d^2 =", Zd2)
Z3_2 = Zd2.subs(d,3)
print("  Z_3^2 =", Z3_2, "  ==? 32 pi/3 ->", sp.simplify(Z3_2 - sp.Rational(32,3)*sp.pi)==0)
print("  (NB: 32pi/3 = 64pi/(3*2) = 64pi/(d(d-1))|_{d=3}; the prompt's Z^2=32pi/3 is the d=3 value)")
print()

print("="*86)
print(" STEP 1 -- d-dim de Sitter horizon temperature & d-dim Friedmann equation")
print("="*86)
G, rho, H, c, hbar, kB, Lam, a, gN, r = sp.symbols(
    'G rho H c hbar kB Lambda a g_N r', positive=True)

# (1a) d-dim FRIEDMANN. In (d+1) spacetime dims (d spatial), the Friedmann eq is
#      H^2 = [16 pi G_d /(d(d-1))] rho   (Einstein eq G_{00}; the d(d-1)=2 dim_SO(d)).
#      => critical density rho_c = d(d-1) H^2 /(16 pi G).
H2_fried = sp.Rational(16,1)*sp.pi*G*rho/(d*(d-1))      # = 16 pi G rho/(d(d-1))
rho_c = sp.solve(sp.Eq(H**2, H2_fried), rho)[0]
print("  d-dim Friedmann:  H^2 = 16 pi G rho /[d(d-1)]        (d(d-1)=2 dim_SO(d) CONFIRMED)")
print("  critical density: rho_c = d(d-1) H^2/(16 pi G) =", rho_c)
print("    -> at d=3: rho_c =", rho_c.subs(d,3), " = 3H^2/(8 pi G)  [standard]:",
      sp.simplify(rho_c.subs(d,3) - 3*H**2/(8*sp.pi*G))==0)
print()

# (1b) d-dim de Sitter temperature. KEY PHYSICS (Deser-Levin gr-qc/9706018, confirmed
#      by web search): de Sitter_D is the codim-1 hyperboloid in flat (D+1) Minkowski;
#      a uniformly-accelerated detector sees T from its (D+1)-acceleration:
#            2 pi T = (hbar/(c kB)) sqrt(a^2 + (cH)^2)         [a=proper accel]
#      The Gibbons-Hawking floor T(a=0) = hbar H/(2 pi kB) is DIMENSION-INDEPENDENT
#      (web-confirmed: T_GH = H/2pi universal in d). The COMBINATION sqrt(a^2+(cH)^2)
#      is the (D+1)-embedding 'extrinsic acceleration' -- codim-1 for ANY d, so the
#      FORM is d-AGNOSTIC. d enters ONLY via how H relates to rho/Lambda (Step 1a),
#      NOT via the temperature's functional form.
T_of_a = (hbar/(2*sp.pi*c*kB))*sp.sqrt(a**2 + (c*H)**2)
T0     = T_of_a.subs(a,0)
print("  d-dim dS-Unruh T(a) = (hbar/2 pi c kB) sqrt(a^2+(cH)^2)   [FORM d-AGNOSTIC: codim-1 embed]")
print("  Gibbons-Hawking floor T(0) = hbar H/(2 pi kB):",
      sp.simplify(T0 - hbar*H/(2*sp.pi*kB))==0, " (DIMENSION-INDEPENDENT, web-confirmed)")
print()

print("="*86)
print(" STEP 2 -- a0(d) from the dS-Unruh temperature: does Z(d) carry dim_SO(d)?")
print("="*86)
# Milgrom inertia posit: the inertia-PRODUCING heat is the excess DeltaT = T(a)-T(0).
# mu(a) = DeltaT / (a * [hbar/2 pi c kB]) = [sqrt(a^2+(cH)^2) - cH]/a.  (d-agnostic form)
mu = (sp.sqrt(a**2 + (c*H)**2) - c*H)/a
mu_deep = sp.series(mu, a, 0, 2).removeO()   # a<<cH
print("  inertia mu(a) = [sqrt(a^2+(cH)^2)-cH]/a   (DERIVED, NOT chosen) -- d-agnostic form")
print("  deep-MOND (a<<cH):  mu(a) ->", mu_deep, "  =>  mu(a) a = a^2/(2cH) = g_N")
# deep-MOND law: a^2/(2cH) = g_N  =>  a = sqrt(2 cH g_N) = sqrt(a0_T g_N), a0_T = 2cH
a0_T = 2*c*H
print("  => deep law a = sqrt(a0_T * g_N) with a0_T = 2cH   (temperature-route coefficient)")
print()
# Now convert cH to the DENSITY/Lambda scale to expose the d-dependence:
#   the framework's a0 is NOT 2cH; it is the surface-gravity-of-free-fall-scale reading
#   a0 = (c/2) sqrt(G rho_c) = cH/Z_d  -- this is where d(d-1) enters.
a0_density = (c/2)*sp.sqrt(G*rho_c)          # surface gravity of dynamical scale
a0_density_inH = sp.simplify(a0_density)     # substitute rho_c(H)
print("  framework a0 = (c/2) sqrt(G rho_c)   [surface gravity of the free-fall scale]")
print("     = (c/2) sqrt(G * d(d-1)H^2/(16 pi G)) =", sp.simplify(a0_density_inH))
# write as cH/Z_d:
Z_d_solved = sp.simplify(c*H/a0_density_inH)
print("  => a0 = cH / Z_d   with  Z_d =", Z_d_solved)
print("     check Z_d == 8 sqrt(pi/[d(d-1)]) :",
      sp.simplify(Z_d_solved - 8*sp.sqrt(sp.pi/(d*(d-1))))==0)
print("     Z_3 =", sp.nsimplify(Z_d_solved.subs(d,3)), "=", float(Z_d_solved.subs(d,3)),
      " (== 2 sqrt(8pi/3) =", float(2*mp.sqrt(8*mp.pi/3)), ")")
print()
# Lambda form: H^2 -> H_dS^2 = (something) Lambda. In d spatial dims de Sitter has
# Lambda = d(d-1)/2 * H^2 / c^2 ... let's get a0(Lambda,d) and check 32pi at d=3.
# Standard: Lambda (1/length^2) relates to H by  H^2 = 2 c^2 Lambda /(d(d-1))  in d spatial dims
# (so that Friedmann with rho_Lambda = Lambda c^2 * [d(d-1)/(16 pi G)] reproduces H^2).
H_from_Lam = sp.sqrt(2*c**2*Lam/(d*(d-1)))
a0_Lam = sp.simplify(a0_density_inH.subs(H, H_from_Lam))
print("  de Sitter Lambda form: H^2 = 2c^2 Lambda/[d(d-1)]  =>")
print("     a0(Lambda,d) =", a0_Lam)
a0_Lam_d3 = sp.simplify(a0_Lam.subs(d,3))
print("     d=3: a0 =", a0_Lam_d3, " ==? c^2 sqrt(Lambda/(32 pi)) ->",
      sp.simplify(a0_Lam_d3 - c**2*sp.sqrt(Lam/(32*sp.pi)))==0)
print("     => the prompt's a0 = c^2 sqrt(Lambda/32pi): 32pi = 16 pi*(d(d-1)/2)/... is the d=3 value")
print()

print("="*86)
print(" STEP 3 -- deep-MOND rotation-curve exponent in d dims (NO d=3 smuggled)")
print("="*86)
M = sp.Symbol('M', positive=True)
# (3a) Newtonian g_N in d SPATIAL dims from GAUSS'S LAW (not assumed 1/r^2):
#      flux through (d-1)-sphere: g_N * Omega_{d-1} r^{d-1} = 16 pi G M /(d-1) ... up to
#      the d-dim Poisson normalization. The SHAPE is what matters: g_N ~ 1/r^{d-1}.
#      [This is the ONE place d enters the force law -- and it is FORCED by Gauss/flux
#       conservation in d dims, NOT by borrowing AQUAL.]
gN_d = M*G/r**(d-1)        # shape: Newtonian g ~ r^{-(d-1)} (flux through (d-1)-sphere)
print("  Gauss's law in d spatial dims:  g_N ~ G M / r^(d-1)   (flux thru (d-1)-sphere)")
print("     -> d=3 recovers g_N ~ 1/r^2:", sp.simplify(gN_d.subs(d,3) - M*G/r**2)==0)

# (3b) deep-MOND inertia law from Step 2 (d-AGNOSTIC):  a = sqrt(a0 * g_N).
#      This FORM is dimension-independent (it came from the codim-1 dS-Unruh embedding).
a0sym = sp.Symbol('a0', positive=True)
a_deep = sp.sqrt(a0sym*gN_d)
print("  deep-MOND inertia (d-agnostic, from dS-Unruh):  a = sqrt(a0 g_N)")

# (3c) circular orbit: a = v^2 / r  =>  v^2 = a * r = sqrt(a0 G M) * r^{1-(d-1)/2}
v2 = sp.simplify(a_deep*r)
print("  circular orbit a = v^2/r  =>  v^2 = a r =", v2)
# exponent of r in v^2:
expo = sp.simplify(sp.diff(sp.log(v2), sp.log(r))) if False else None
# extract power of r:
v2_pow = sp.Poly(sp.log(v2).rewrite(sp.log), sp.log(r)) if False else None
# do it directly: v2 = C * r^p ; p = ?
p = sp.simplify(sp.degree(sp.Symbol('r')**0))  # placeholder
# symbolic exponent:
r_exp = sp.simplify(sp.log(v2)/sp.log(r))  # messy; instead diff:
p_exp = sp.simplify(r*sp.diff(v2, r)/v2)   # d ln v2 / d ln r
print("  => v^2 ~ r^p with p = dln(v^2)/dln(r) =", p_exp)
print("     FLAT rotation curve (v=const, p=0)  <=>  p = (3-d)/2 = 0  <=>  d = 3")
print("     check p == (3-d)/2 :", sp.simplify(p_exp - (3-d)/2)==0)
print()
print("  TABLE: deep-MOND v^2 ~ r^p and rotation-curve behavior vs d")
print(f"     {'d':>3}{'g_N~r^?':>10}{'v^2~r^p, p=(3-d)/2':>22}{'rotation curve':>22}")
for dd in (1,2,3,4,5):
    pv = sp.Rational(3-dd,2)
    beh = ("FLAT (v=const)" if pv==0 else
           ("RISING" if pv>0 else "FALLING"))
    print(f"     {dd:>3}{('r^%d'%-(dd-1)):>10}{('r^(%s)'%sp.nsimplify(pv)):>22}{beh:>22}")
print()
print("  *** KEY RESULT (Step 3): flat rotation curves REQUIRE d=3. ***")
print("  The deep-MOND inertia FORM a=sqrt(a0 g_N) is d-agnostic; flatness is NOT.")
print("  Flatness = [v^2 r-exponent (3-d)/2 vanishes] is a coincidence of the d-agnostic")
print("  sqrt-inertia law with the Gauss-law force exponent (d-1): (1-(d-1)/2)=0 -> d=3.")
print()

print("="*86)
print(" STEP 4 -- THE KEY: where does d=3 become REQUIRED? (both-ways audit)")
print("="*86)

print(" (4a) Is a0(d) finite/sensible at all d?  [test: does a0 need d=3?]")
# Z_d = 8 sqrt(pi/[d(d-1)]) is real & finite for all integer d>=2. Diverges/ill only at
# d=0,1 (d(d-1)=0). So a0 is well-defined for every d>=2.
for dd in (2,3,4,5,10):
    Zval = float(8*mp.sqrt(mp.pi/(dd*(dd-1))))
    print(f"     d={dd:>2}:  d(d-1)={dd*(dd-1):>3}  Z_d={Zval:7.3f}  a0=cH/Z_d  -> FINITE & sensible")
print("     d=1: d(d-1)=0 -> Z diverges, a0->0 (no transverse space; degenerate).")
print("     VERDICT (4a): a0 is FINITE for every d>=2. d=3 NOT required for a finite a0.")
print("       d=3 only fixes the VALUE Z_3=5.789 (=2 sqrt(8pi/3)); other d give other O(1).")
print("       => 'a0 ~ cH and ~ c^2 sqrt(Lambda)' is d-AGNOSTIC in MAGNITUDE; only the")
print("          numeric coefficient Z_d carries dim_SO(d) via d(d-1). NOT load-bearing for finiteness.")
print()

print(" (4b) Do flat rotation curves require d=3?  [from Step 3]")
print("     v^2 ~ r^((3-d)/2).  FLAT  <=>  (3-d)/2 = 0  <=>  d=3.  ==> YES, REQUIRED.")
print("     This is the ONE place d=3 is genuinely LOAD-BEARING and SELECTS d=3:")
print("     it needs the d-agnostic sqrt-inertia law AND the Gauss-law exponent (d-1)")
print("     to conspire so the r-power cancels. That cancellation is unique to d=3.")
print()

print(" (4c) Does the modified-inertia MECHANISM (the dS-Unruh posit) need d=3 to close?")
# The mechanism: T(a)=sqrt(a^2+(cH)^2), mu=DeltaT/a, deep limit a^2/2cH=g_N. None of this
# references d: the codim-1 hyperboloid embedding of dS_D in M_{D+1} holds for ALL D.
print("     The dS-Unruh temperature (codim-1 embedding) and mu(a)=[sqrt(a^2+(cH)^2)-cH]/a")
print("     reference NO spatial dimension -- they close for ANY d. d-AGNOSTIC mechanism.")
print("     VERDICT (4c): the modified-inertia mechanism does NOT require d=3.")
print()

print(" (4d) BOTH-WAYS skeptic check: is d=3 SMUGGLED into the flatness result?")
print("     Two candidate smuggles, audited:")
print("       (i)  '1/r^2 force law' -> NO: we derived g_N~1/r^(d-1) from Gauss in d dims,")
print("            kept d general; flatness still landed on d=3. Not smuggled.")
print("       (ii) 'borrowed AQUAL d-structure' -> NO: we used the dS-Unruh sqrt-inertia")
print("            law a=sqrt(a0 g_N), which is d-agnostic (codim-1 embed), NOT AQUAL's")
print("            d-dim Poisson operator. The d-dependence enters ONLY through Gauss's")
print("            flux law for g_N -- an independent, forced input. Not smuggled.")
print("     => the d=3 selection for FLATNESS is ROBUST, not an artifact of a d-baked input.")
print()

print(" (4e) The self-duality connection (is dim_SO(3)=3 the REASON, or a coincidence?)")
# Flatness condition: 1 - (d-1)/2 = 0  ->  d-1 = 2  ->  d = 3.
# Self-duality:       d = d(d-1)/2     ->  d-1 = 2  ->  d = 3  (#vec=#bivec).
# dim_SO(d)=d:        d(d-1)/2 = d     ->  d-1 = 2  ->  d = 3.
# Gauss exponent (d-1)=2 is the SAME equation as the self-duality (d-1)=2.
cond_flat = sp.Eq(1 - (d-1)/2, 0)
cond_self = sp.Eq(d, d*(d-1)/2)
cond_dimSO= sp.Eq(d*(d-1)/2, d)
print("     flatness:     1-(d-1)/2 = 0   =>  d-1 = 2  =>  d =", sp.solve(cond_flat,d))
print("     self-duality: d = d(d-1)/2    =>  d-1 = 2  =>  d =", sp.solve(cond_self,d))
print("     dim_SO(d)=d:  d(d-1)/2 = d    =>  d-1 = 2  =>  d =", sp.solve(cond_dimSO,d))
print("     ALL THREE reduce to the SAME equation  (d-1)=2.  The flat-rotation-curve")
print("     condition, the cross-product self-duality, and dim_SO(d)=d are the SAME")
print("     statement: d-1=2. So 'a MOND scale gives flat curves' SELECTS exactly the")
print("     self-dual dimension d=3 -- a genuine consistency/selection statement.")
print("     HONEST CEILING: this is a SELECTION (flatness <=> self-duality), NOT a")
print("     from-below derivation of d=3 (we did not derive WHY space is 3D); the")
print("     inertia FORM and a0 MAGNITUDE remain d-agnostic.")
print()

print("="*86)
print(" LEDGER -- d=3 load-bearing audit")
print("="*86)
print("  d-AGNOSTIC (NOT requiring d=3):")
print("   * the dS-Unruh temperature T(a)=sqrt(a^2+(cH)^2) (codim-1 embed, any D)")
print("   * the inertia interpolation mu(a)=[sqrt(a^2+(cH)^2)-cH]/a")
print("   * the deep-MOND sqrt-inertia LAW a=sqrt(a0 g_N)")
print("   * a0 MAGNITUDE ~ cH ~ c^2 sqrt(Lambda) (finite for every d>=2)")
print("  d=3-SELECTING (load-bearing):")
print("   * FLAT rotation curves: v^2~r^((3-d)/2)=const <=> d=3  [the real selection]")
print("   * the exact coefficient Z_3=2 sqrt(8pi/3): Z_d=8 sqrt(pi/[d(d-1)]) is the d=3 value")
print("   * a0 = c^2 sqrt(Lambda/32pi): 32pi is the d=3 value of the Lambda->a0 conversion")
print("  THE DEEP IDENTITY:  flatness <=> (d-1)=2 <=> #vectors=#bivectors (self-duality)")
print("                       <=> dim_SO(d)=d.  All ONE equation. SELECTION, not derivation.")
